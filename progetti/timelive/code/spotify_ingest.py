# spotify_ingest.py
# =============================================================================
# SPOTIFY INGEST — Personal Data Vault (SQLite / ingest_engine.py, second
# domain migrated in the 2026-09-14 architecture rebuild — see
# EVOLUTION_LOG.md and timelive.md §8)
# =============================================================================
#
# WHAT CHANGED FROM THE OLD (PRIMARY/FULL JSON) VERSION OF THIS FILE
# -----------------------------------------------------------------------
# * Output is now one table (plus a sessions table) in the single shared
#   vault.db, not two JSON files. No more PRIMARY/FULL, no more
#   PRIMARY_MAX_SIZE_MB budget/selection logic, no more prune levels —
#   same "fallo sparire del tutto" decision already applied to chess.com.
# * REAL-DATA FINDING (2026-09-14, inspecting the user's actual "Extended
#   Streaming History" export — 33 files, 358,440 records, 2014-2026):
#   this export format is RICHER than what the old file used. It has a
#   genuinely NATIVE `skipped` boolean (populated on every single record
#   inspected) — so the old is_skipped_like duration-heuristic (<30s,
#   confidence_rate=0.5) is GONE. Per timelive.md §3's classification
#   priority (native beats inference), the real field wins outright. This
#   also means the `plays` table below needs NO confidence_rate column at
#   all: duration_seconds is native (ms_played, not estimated), skipped
#   is native, content_type is a native-field-presence check (see below),
#   and timestamp_begin is exact arithmetic (end - duration) rather than
#   an estimate — unlike chess.com, nothing in this domain is a genuine
#   inference.
# * NEW: a `content_type` column (track / episode / audiobook / unknown)
#   that did not exist in the old file at all. The old code only ever
#   split by media_type (audio/video, from the export filename) and left
#   episodes as "a play with null artist/track fields" — not a queryable
#   distinction. Real data shows this matters: media_type and content_type
#   are independent axes (the "Video" files contain a mix of music tracks
#   AND podcast episodes, not just music-as-video — confirmed by
#   inspection, not assumed).
# * Zero audiobook records were found anywhere in the real export (0 of
#   358,440) — the audiobook_* columns are kept anyway because the raw
#   export schema declares them (Spotify's own field set, not invented
#   here — see classify_content_type()), so a future export that does
#   include audiobooks needs no schema change.
# * DEDUP KEY CHANGE: now built from the NATIVE per-item URI
#   (spotify_track_uri / spotify_episode_uri / audiobook_*_uri) + ts +
#   ms_played, instead of the old artist/track DISPLAY NAME composite —
#   a real upgrade per timelive.md §3 ("native id quando esiste"), since
#   a URI is stable and a display name is not (covers, remasters, etc.).
#   REAL-DATA FINDING + PROJECT OWNER DECISION (2026-09-14): a narrow key
#   of just (ts, uri, ms_played) isn't unique — 362 groups (out of
#   358,440 records) shared it while differing in secondary/telemetry
#   fields (offline_timestamp, reason_start, reason_end, shuffle — never
#   in track/artist/duration). Widening the key to also include those
#   telemetry fields still left 184 groups (247 records) that are
#   BYTE-IDENTICAL across every single field the export provides — a
#   genuinely duplicate line inside one source file, not a distinguishable
#   second event. Project owner's explicit choice: every raw record stays
#   its own row, never merged into another — so the key also includes
#   source_file + record_index_in_source (position within that file).
#   This still keeps re-ingests stable/idempotent (re-parsing an unchanged
#   file reproduces the same file+index for the same JSON element, so a
#   later ingest run UPDATEs that row instead of duplicating it) while
#   guaranteeing two different elements — even byte-identical ones — never
#   collapse into one. Net effect: dedup_key_column now only ever catches
#   a true re-ingest of the same file, never "records that look alike".
# * ip_addr is NOT copied into vault.db (excluded on purpose, flagged for
#   confirmation — see chat response: unlike the raw export file, which
#   is never touched, vault.db is the thing a cloud LLM (ClaudeAPIClient)
#   directly queries via run_sql, so a column here is a real exposure
#   path a raw file sitting on disk is not). conn_country (2-letter
#   country code — much coarser) is kept.
#
# WHAT DID NOT CHANGE
# -----------------------------------------------------------------------
# Session gap threshold (20 minutes) and the "isolated play is not a
# session" rule (SESSION_MIN_TRACKS=2) are unchanged from the old file —
# but are now actually VALIDATED against the real data (timelive.md §7:
# "dati reali prima dello schema"), not just carried over. Real inter-play
# gap distribution (audio, 357,536 gaps): p90=364s (~6min), p95=1948s
# (~32min) — a clear elbow between those two points. 20 minutes sits
# inside that elbow zone, same as chess.com's already-validated 15-20min
# choice — kept, not re-guessed. See EVOLUTION_LOG.md-style note in chat
# response for the full percentile table.
# =============================================================================

from __future__ import annotations

import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ingest_engine import (
    ColumnSpec,
    TableSpec,
    NotabilityConfig,
    UpsertOutcome,
    IngestReport,
    create_schema_for_table,
    upsert_rows,
    compute_notability_scores,
    recency_weight,
    group_into_sessions,
    register_table_spec,
)

logger = logging.getLogger("spotify_ingest")


# ============================================================================
# CONFIGURATION
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Paths (same fallback pattern as chessdotcom_ingest.py)
# ----------------------------------------------------------------------------
try:
    from config import SPOTIFY_INPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    SPOTIFY_INPUT_DIR = BASE_DIR / "Input" / "Spotify"
SPOTIFY_INPUT_DIR = Path(SPOTIFY_INPUT_DIR)

SOURCE_PREFIX = "spotify"

# ----------------------------------------------------------------------------
# CONFIG — Session detection (timelive.md §4: grouping/sessions are never
# reused by analogy between domains — validated here on real data, see
# module docstring above for the actual percentile table).
# ----------------------------------------------------------------------------
SESSION_GAP_SECONDS = 20 * 60  # 20 minutes, flat (unlike chess.com's adaptive gap — no per-item signal like time_class exists here to make it adaptive)
SESSION_MIN_TRACKS = 2

# ----------------------------------------------------------------------------
# CONFIG — notability_score weights, plays. Same three-signal shape as the
# old file (duration / recency / not-skipped bonus), same weights — no
# real-data reason found to change the formula itself, only its inputs
# (not_skipped_bonus now reads the native `skipped` field directly instead
# of a duration heuristic).
# ----------------------------------------------------------------------------
NOTABILITY_WEIGHT_DURATION = 0.5
NOTABILITY_WEIGHT_RECENCY = 0.3
NOTABILITY_WEIGHT_NOT_SKIPPED_BONUS = 0.2
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60

# ----------------------------------------------------------------------------
# CONFIG — notability_score weights, listening_sessions. NEW, like
# chess.com's playing_sessions notability: no prior formula existed (the
# old file never scored sessions). INVENTED DEFAULT, NOT VALIDATED against
# real query patterns yet — flagged for confirmation, same as chess.com's
# equivalent was.
# ----------------------------------------------------------------------------
SESSION_NOTABILITY_WEIGHT_PLAY_COUNT = 0.5
SESSION_NOTABILITY_WEIGHT_RECENCY = 0.5
SESSION_NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60
SESSION_NOTABILITY_PLAY_COUNT_CAP = 20  # play_count signal saturates at this many plays — guessed, not measured


# ============================================================================
# TABLE DECLARATIONS (timelive.md §3 — the "contract" for this domain)
# ============================================================================

PLAYS_TABLE = TableSpec(
    name="plays",
    primary_key_column="play_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    foreign_keys={"session_id": "listening_sessions(session_id)"},
    extra_indexed_columns=["content_type", "media_type", "artist_name", "skipped"],
    columns=[
        ColumnSpec("play_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                    semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("timestamp_begin", "TEXT",
                    semantic_note="derived = timestamp_end - duration_seconds (exact, not estimated: duration_seconds is native)"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="canonical timestamp — native (Spotify's own 'ts', the moment playback ended/was reported)"),
        ColumnSpec("duration_seconds", "REAL",
                    semantic_note="native (from ms_played) — can legitimately be 0 (e.g. a play that never started)"),
        ColumnSpec("media_type", "TEXT",
                    semantic_note="'audio'/'video' — which export file this came from (which client surface logged it), NOT what was played; see content_type for that"),
        ColumnSpec("content_type", "TEXT",
                    semantic_note="'track'/'episode'/'audiobook'/'unknown' — derived from which native id field is populated (see classify_content_type); independent of media_type"),
        ColumnSpec("track_name", "TEXT"),
        ColumnSpec("artist_name", "TEXT", entity_hint=None),
        ColumnSpec("album_name", "TEXT"),
        ColumnSpec("track_uri", "TEXT"),
        ColumnSpec("episode_name", "TEXT"),
        ColumnSpec("show_name", "TEXT"),
        ColumnSpec("episode_uri", "TEXT"),
        ColumnSpec("audiobook_title", "TEXT"),
        ColumnSpec("audiobook_uri", "TEXT"),
        ColumnSpec("audiobook_chapter_title", "TEXT"),
        ColumnSpec("audiobook_chapter_uri", "TEXT"),
        ColumnSpec("platform", "TEXT", semantic_note="native device/platform string — format varies a lot across export vintages (e.g. 'ios' vs a full 'Android OS 4.4.4 API 19 (LGE, Nexus 5)' string), kept verbatim, never normalized"),
        ColumnSpec("conn_country", "TEXT", semantic_note="2-letter country code, native; coarser than the source export's ip_addr field, which is NOT copied into vault.db (see module docstring)"),
        ColumnSpec("reason_start", "TEXT", semantic_note="native, verbatim (e.g. 'trackdone', 'fwdbtn', 'clickrow', 'unknown' — 'unknown' is a real value Spotify itself reports, not a gap in this ingest)"),
        ColumnSpec("reason_end", "TEXT", semantic_note="native, verbatim"),
        ColumnSpec("shuffle", "INTEGER", semantic_note="native boolean, 0/1"),
        ColumnSpec("skipped", "INTEGER", semantic_note="native boolean, 0/1 — Spotify's own skip flag, not a heuristic (see module docstring)"),
        ColumnSpec("offline", "INTEGER", semantic_note="native boolean, 0/1"),
        ColumnSpec("offline_timestamp", "INTEGER", semantic_note="native raw field (unix seconds); observed non-null even when offline=0 in recent export vintages — meaning unclear from the data alone, kept as-is rather than reinterpreted"),
        ColumnSpec("incognito_mode", "INTEGER", semantic_note="native boolean, 0/1"),
        ColumnSpec("session_id", "INTEGER", semantic_note="NULL if this play is not part of any detected listening session"),
        ColumnSpec("notability_score", "REAL"),
        ColumnSpec("source", "TEXT"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

LISTENING_SESSIONS_TABLE = TableSpec(
    name="listening_sessions",
    primary_key_column="session_id",
    dedup_key_column=None,  # fully rebuilt every ingest run — see run_ingest()
    canonical_timestamp_column="timestamp_begin",
    columns=[
        ColumnSpec("session_id", "INTEGER"),
        ColumnSpec("timestamp_begin", "TEXT", not_null=True),
        ColumnSpec("timestamp_end", "TEXT", not_null=True),
        ColumnSpec("duration_seconds", "INTEGER"),
        ColumnSpec("media_type", "TEXT", semantic_note="a session never mixes audio and video plays — see is_compatible in detect_listening_sessions()"),
        ColumnSpec("play_count", "INTEGER"),
        ColumnSpec("distinct_artist_count", "INTEGER", semantic_note="counts distinct artist_name among track plays in the session; episodes/audiobooks don't contribute an artist"),
        ColumnSpec("skipped_count", "INTEGER"),
        ColumnSpec("total_played_seconds", "REAL"),
        ColumnSpec("notability_score", "REAL"),
        ColumnSpec("confidence_rate", "REAL",
                    semantic_note="confidence that this grouping of plays is really one sitting, not that the plays themselves happened"),
    ],
)

# Registered at import time (not inside run_ingest()) — same reasoning as
# chessdotcom_ingest.py: importing this module is enough for the bridge to
# know these tables' columns/semantic notes without running an ingest first.
register_table_spec(LISTENING_SESSIONS_TABLE)
register_table_spec(PLAYS_TABLE)


# ============================================================================
# PARSING — file reading
# ============================================================================

_FILENAME_RE = re.compile(r"^Streaming_History_(Audio|Video)_(\d{4})(?:_(\d+))?\.json$", re.IGNORECASE)


def detect_media_type(path: Path) -> str:
    m = _FILENAME_RE.match(path.name)
    return m.group(1).lower() if m else "unknown"


def extract_year_from_filename(path: Path) -> int:
    m = _FILENAME_RE.match(path.name)
    return int(m.group(2)) if m else 0


def collect_input_files(input_dir: Path) -> List[Path]:
    if not input_dir.exists():
        return []
    files = [p for p in input_dir.iterdir() if p.is_file() and _FILENAME_RE.match(p.name)]
    # Deterministic order: matters for the record_index_in_source tiebreak
    # used in the chronological sort below.
    files.sort(key=lambda p: (extract_year_from_filename(p), detect_media_type(p), p.name.lower()))
    return files


def load_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ndjson_file(path: Path) -> List[Any]:
    records = []
    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"NDJSON error at line {idx}: {exc}") from exc
    return records


def load_spotify_file(path: Path) -> List[Any]:
    """
    Every file actually inspected (33 files, 358,440 records, 2014-2026)
    was a plain JSON list. The NDJSON fallback below is defensive only —
    not observed in the real export — kept because a prior export vintage
    reportedly used it (see the old file's history) and a future export
    could again; timelive.md §7 says inspect real data, not assume a
    single format holds forever.
    """
    try:
        payload = load_json_file(path)
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict) and isinstance(payload.get("records"), list):
            return payload["records"]
        raise ValueError("Unrecognized JSON structure.")
    except Exception as json_exc:
        try:
            return load_ndjson_file(path)
        except Exception as ndjson_exc:
            raise ValueError(f"Failed as JSON and as NDJSON: {json_exc} | {ndjson_exc}") from ndjson_exc


# ============================================================================
# CLASSIFICATION — content_type (native-field-presence, not an inference)
# ============================================================================

def classify_content_type(raw: Dict[str, Any]) -> str:
    """
    Priority order matches which native id/name field is populated — this
    is a structural check on the raw record, not a guess (timelive.md §3
    priority level 1/2). Real-data note: every one of the 358,440
    inspected records fell into 'track' (358,005) or 'episode' (435);
    'audiobook' has never been observed but the raw export schema
    declares audiobook_title/audiobook_uri, so it's handled here rather
    than only added later if/when it appears.
    """
    if raw.get("master_metadata_track_name") is not None or raw.get("spotify_track_uri") is not None:
        return "track"
    if raw.get("episode_name") is not None or raw.get("spotify_episode_uri") is not None:
        return "episode"
    if raw.get("audiobook_title") is not None or raw.get("audiobook_uri") is not None:
        return "audiobook"
    return "unknown"


# ============================================================================
# NORMALIZATION — record building
# ============================================================================

def to_iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_ts(value: Any) -> str:
    """
    Every inspected 'ts' value was already ISO 8601 UTC with a 'Z' suffix
    (Spotify's current export format). Still parsed defensively rather
    than assumed, and re-serialized through to_iso_utc for a canonical
    representation — never raises, never fabricates a timestamp when one
    can't be parsed (timelive.md §4/§7).
    """
    if not value:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return to_iso_utc(dt)
    except Exception:
        return ""


def build_dedup_key(raw: Dict[str, Any], timestamp_end: str, ms_played: Optional[float],
                     content_type: str, source_file: str, record_index_in_source: int) -> str:
    """
    Native-id-based (timestamp_end + the item's own URI + ms_played),
    PLUS source_file + record_index_in_source unconditionally — see the
    module docstring's "DEDUP KEY CHANGE" note for the real-data findings
    and the project owner's explicit decision behind this (2026-09-14):
    every raw record is its own row, even a byte-identical one, and
    re-ingests stay stable because the same file+position always
    reproduces the same key for the same underlying JSON element.
    """
    uri = (
        raw.get("spotify_track_uri")
        or raw.get("spotify_episode_uri")
        or raw.get("audiobook_chapter_uri")
        or raw.get("audiobook_uri")
    )
    identity = uri if uri else "nouri:" + (
        raw.get("master_metadata_track_name")
        or raw.get("episode_name")
        or raw.get("audiobook_chapter_title")
        or raw.get("audiobook_title")
        or ""
    ).strip().lower()
    return "|".join([
        timestamp_end, identity, str(ms_played), source_file, str(record_index_in_source),
    ])


def build_record(raw: Any, source_path: Path, record_index_in_source: int) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raw = {}

    media_type = detect_media_type(source_path)
    content_type = classify_content_type(raw)

    timestamp_end = parse_ts(raw.get("ts"))

    ms_played_raw = raw.get("ms_played")
    ms_played = float(ms_played_raw) if isinstance(ms_played_raw, (int, float)) else None
    duration_seconds = round(ms_played / 1000.0, 3) if ms_played is not None else None

    if timestamp_end and duration_seconds is not None:
        try:
            end_dt = datetime.fromisoformat(timestamp_end.replace("Z", "+00:00"))
            timestamp_begin = to_iso_utc(end_dt - timedelta(seconds=duration_seconds))
        except Exception:
            timestamp_begin = timestamp_end
    else:
        timestamp_begin = timestamp_end

    def as_int_bool(value: Any) -> Optional[int]:
        return None if value is None else int(bool(value))

    dedup_key = build_dedup_key(raw, timestamp_end, ms_played, content_type, source_path.name, record_index_in_source)

    return {
        "timestamp_begin": timestamp_begin,
        "timestamp_end": timestamp_end,
        "duration_seconds": duration_seconds,
        "media_type": media_type,
        "content_type": content_type,
        "track_name": raw.get("master_metadata_track_name"),
        "artist_name": raw.get("master_metadata_album_artist_name"),
        "album_name": raw.get("master_metadata_album_album_name"),
        "track_uri": raw.get("spotify_track_uri"),
        "episode_name": raw.get("episode_name"),
        "show_name": raw.get("episode_show_name"),
        "episode_uri": raw.get("spotify_episode_uri"),
        "audiobook_title": raw.get("audiobook_title"),
        "audiobook_uri": raw.get("audiobook_uri"),
        "audiobook_chapter_title": raw.get("audiobook_chapter_title"),
        "audiobook_chapter_uri": raw.get("audiobook_chapter_uri"),
        "platform": raw.get("platform"),
        "conn_country": raw.get("conn_country"),
        "reason_start": raw.get("reason_start"),
        "reason_end": raw.get("reason_end"),
        "shuffle": as_int_bool(raw.get("shuffle")),
        "skipped": as_int_bool(raw.get("skipped")),
        "offline": as_int_bool(raw.get("offline")),
        "offline_timestamp": raw.get("offline_timestamp") if isinstance(raw.get("offline_timestamp"), int) else None,
        "incognito_mode": as_int_bool(raw.get("incognito_mode")),
        "session_id": None,  # filled in after session detection, see run_ingest()
        "source": SOURCE_PREFIX,
        "source_file": source_path.name,
        "dedup_key": dedup_key,
        "record_index_in_source": record_index_in_source,  # transient, dropped before insert
    }


# ============================================================================
# NOTABILITY — plays
# ============================================================================

def _compute_duration_percentiles(records: List[Dict[str, Any]]) -> None:
    """
    Attaches `_duration_percentile` (0..1), computed within each
    (media_type, content_type) group — NOT just media_type as the old
    file did. Real-data reason: episodes run far longer than tracks on
    average, so comparing a 3-minute song's duration against a 40-minute
    podcast episode inside the same percentile group would be misleading
    (timelive.md §7 spirit: don't blur groups that measure genuinely
    different things). Dict-based rank lookup, not list.index() in a
    loop — same O(n) vs O(n^2) reasoning as chess.com's percentile helper
    (timelive.md §7).
    """
    groups: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("duration_seconds") is not None:
            groups[(record.get("media_type"), record.get("content_type"))].append(record)

    for _, group_records in groups.items():
        durations_sorted = sorted(r["duration_seconds"] for r in group_records)
        n = len(durations_sorted)
        rank_of_duration: Dict[float, int] = {}
        for idx, duration in enumerate(durations_sorted):
            if duration not in rank_of_duration:
                rank_of_duration[duration] = idx
        for record in group_records:
            rank = rank_of_duration[record["duration_seconds"]]
            record["_duration_percentile"] = rank / max(n - 1, 1)


def apply_play_notability(records: List[Dict[str, Any]]) -> None:
    _compute_duration_percentiles(records)
    compute_notability_scores(
        records,
        NotabilityConfig(
            weight_functions={
                "duration": lambda r: r.get("_duration_percentile", 0.0),
                "recency": lambda r: recency_weight(r.get("timestamp_end"), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS),
                "not_skipped_bonus": lambda r: 0.0 if r.get("skipped") else 1.0,
            },
            weights={
                "duration": NOTABILITY_WEIGHT_DURATION,
                "recency": NOTABILITY_WEIGHT_RECENCY,
                "not_skipped_bonus": NOTABILITY_WEIGHT_NOT_SKIPPED_BONUS,
            },
        ),
    )
    for record in records:
        record.pop("_duration_percentile", None)


def apply_session_notability(sessions: List[Dict[str, Any]]) -> None:
    """NEW — see CONFIG note above, no prior formula existed for spotify sessions."""
    compute_notability_scores(
        sessions,
        NotabilityConfig(
            weight_functions={
                "play_count": lambda s: min(s.get("play_count", 0) / SESSION_NOTABILITY_PLAY_COUNT_CAP, 1.0),
                "recency": lambda s: recency_weight(s.get("timestamp_end"), half_life_days=SESSION_NOTABILITY_RECENCY_HALF_LIFE_DAYS),
            },
            weights={
                "play_count": SESSION_NOTABILITY_WEIGHT_PLAY_COUNT,
                "recency": SESSION_NOTABILITY_WEIGHT_RECENCY,
            },
        ),
    )


# ============================================================================
# LISTENING-SESSION DETECTION
# ============================================================================

def _session_gap_seconds_fn(previous: Dict[str, Any], current: Dict[str, Any]) -> float:
    return SESSION_GAP_SECONDS


def detect_listening_sessions(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    `records` must be sorted chronologically already. A session never
    mixes media_type (is_compatible below) — real-data reason: audio and
    video plays have very different gap distributions (median gap ~2.7min
    for audio vs ~31min for video in this export), so merging them would
    manufacture sessions that don't reflect one continuous listening
    experience. Returns session dicts and sets `record["_session_index"]`
    on every record ending up in a session with >= SESSION_MIN_TRACKS
    plays (same mechanism as chessdotcom_ingest.py's detect_playing_sessions).
    """
    live_records = [r for r in records if r.get("timestamp_end")]
    groups = group_into_sessions(
        live_records,
        timestamp_begin_field="timestamp_end",
        timestamp_end_field="timestamp_end",
        gap_seconds_fn=_session_gap_seconds_fn,
        is_compatible=lambda a, b: a.get("media_type") == b.get("media_type"),
    )

    sessions: List[Dict[str, Any]] = []
    for group in groups:
        if len(group) < SESSION_MIN_TRACKS:
            continue

        session_index = len(sessions)
        begin_ts = group[0]["timestamp_end"]
        end_ts = group[-1]["timestamp_end"]
        begin_dt = datetime.fromisoformat(begin_ts.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_ts.replace("Z", "+00:00"))

        for r in group:
            r["_session_index"] = session_index

        distinct_artists = {r.get("artist_name") for r in group if r.get("artist_name")}
        total_played_seconds = round(sum(r.get("duration_seconds") or 0.0 for r in group), 3)

        sessions.append({
            "timestamp_begin": begin_ts,
            "timestamp_end": end_ts,
            "duration_seconds": round((end_dt - begin_dt).total_seconds()),
            "media_type": group[0].get("media_type"),
            "play_count": len(group),
            "distinct_artist_count": len(distinct_artists),
            "skipped_count": sum(1 for r in group if r.get("skipped")),
            "total_played_seconds": total_played_seconds,
            "confidence_rate": 0.8,  # CONFIDENCE_INFERRED_HIGH — grouping is deterministic given the threshold, but still an assumption about what constitutes "one sitting"
        })

    return sessions


# ============================================================================
# MAIN ENTRYPOINT — the contract ingest_engine.py's CLI expects
# ============================================================================

def run_ingest(conn, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    """
    Same 8-step shape as chessdotcom_ingest.run_ingest(): schema first
    (listening_sessions before plays — FK), parse everything in memory,
    sort, notability, session detection, write sessions (full rebuild),
    then upsert plays (stable ids across re-ingests). No child table like
    chess.com's game_moves — a play has no natural sub-entity to normalize
    into a second table.
    """
    create_schema_for_table(conn, LISTENING_SESSIONS_TABLE)
    create_schema_for_table(conn, PLAYS_TABLE)

    input_files = collect_input_files(SPOTIFY_INPUT_DIR)
    logger.info("found %d Streaming_History_*.json file(s) in %s", len(input_files), SPOTIFY_INPUT_DIR)

    all_records: List[Dict[str, Any]] = []
    error_count = 0
    for source_path in input_files:
        try:
            raw_records = load_spotify_file(source_path)
            logger.debug("%s: %d record(s)", source_path.name, len(raw_records))
            for idx, raw in enumerate(raw_records):
                try:
                    record = build_record(raw, source_path, idx)
                    all_records.append(record)
                except Exception as exc:
                    error_count += 1
                    logger.warning("%s record #%d: parse error: %s", source_path.name, idx, exc)
        except Exception as exc:
            error_count += 1
            logger.warning("%s: file read error: %s", source_path.name, exc)

    if error_count:
        logger.warning("%d record(s)/file(s) skipped due to errors — see warnings above", error_count)

    all_records.sort(key=lambda r: (r.get("timestamp_end", ""), r.get("source_file", ""), r.get("record_index_in_source", 0)))

    apply_play_notability(all_records)
    sessions = detect_listening_sessions(all_records)
    apply_session_notability(sessions)

    content_type_counts = defaultdict(int)
    for r in all_records:
        content_type_counts[r.get("content_type")] += 1
    logger.info(
        "%d play(s) parsed (%s), %d listening session(s) detected",
        len(all_records), dict(content_type_counts), len(sessions),
    )

    # --- playing sessions: full rebuild every run (same reasoning as chessdotcom) ---
    conn.execute("UPDATE plays SET session_id = NULL")
    conn.execute("DELETE FROM listening_sessions")
    session_id_by_index: Dict[int, int] = {}
    for idx, session in enumerate(sessions):
        outcome = upsert_rows(conn, LISTENING_SESSIONS_TABLE, [session])[0]
        session_id_by_index[idx] = outcome.primary_key

    for record in all_records:
        session_index = record.pop("_session_index", None)
        record["session_id"] = session_id_by_index.get(session_index) if session_index is not None else None
        record.pop("record_index_in_source", None)

    # --- plays: stable upsert (see module docstring re: the 362 same-key groups) ---
    play_outcomes: List[UpsertOutcome] = upsert_rows(conn, PLAYS_TABLE, all_records)

    rows_inserted = sum(1 for o in play_outcomes if o.was_new) + len(sessions)
    rows_already_present = sum(1 for o in play_outcomes if not o.was_new)

    return IngestReport(
        domain="spotify",
        tables_written=["listening_sessions", "plays"],
        rows_inserted=rows_inserted,
        rows_already_present=rows_already_present,
        dry_run=dry_run,
    )