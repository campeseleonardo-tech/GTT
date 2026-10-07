# chessdotcom_ingest.py
# =============================================================================
# CHESS.COM INGEST — Personal Data Vault (SQLite / ingest_engine.py, pilot
# domain for the 2026-09-14 architecture rebuild — see EVOLUTION_LOG.md)
# =============================================================================
#
# WHAT CHANGED FROM THE OLD (PRIMARY/FULL JSON) VERSION OF THIS FILE
# -----------------------------------------------------------------------
# * Output is now three tables in the single shared vault.db, not two JSON
#   files: games, game_moves, playing_sessions (timelive.md §3 — approved
#   schema, 2026-09-14 conversation).
# * PRUNE_LEVEL / PRIMARY_MAX_SIZE_MB / the recency "guarantee boost" are
#   GONE — there is no PRIMARY/FULL size budget to manage anymore (project
#   owner's decision, 2026-09-14: "fallo sparire del tutto").
# * moves_san lives in its own table (game_moves), one row per half-move,
#   instead of a field on the game record — chosen so a local LLM can
#   filter moves with plain SQL instead of parsing a JSON blob.
# * build_game_aggregations() (the old by_opponent/by_opening/by-win_method
#   breakdowns) is GONE. Every one of those breakdowns is now a plain
#   `GROUP BY` a model can write itself once it has SQL access — this is
#   also what closes chess_04 (win_method breakdown, EVOLUTION_LOG.md) as
#   a side effect of the migration, not a separate fix.
# * is_upset is stored as SQLite INTEGER (0/1), not a Python bool
#   serialized into JSON. This removes the boolean/string ambiguity that
#   was the leading suspect for chess_02 (EVOLUTION_LOG.md) — to be
#   confirmed once this runs against real data (task 5), not assumed here.
# * event_number (a string counter that RENUMBERED on every re-ingest —
#   a known, explicitly unresolved problem in the old system) is replaced
#   by game_id: a real SQLite auto-increment id that STAYS THE SAME across
#   re-ingests, because it's tied to each game's dedup_key, not to its
#   position in a list. See upsert_rows() in ingest_engine.py.
#
# WHAT DID NOT CHANGE
# -----------------------------------------------------------------------
# Every parsing/classification function below (PGN splitting, time control
# parsing, timestamp parsing, move/clock extraction, win_method/is_upset/
# result classification, the adaptive session-gap formula) is the same
# logic as the old file, validated against real data on 2026-09-11/12 (see
# the REAL DATA FINDINGS note further down) — only the plumbing around it
# changed. Nothing here re-guesses a threshold that was already measured.
# =============================================================================

from __future__ import annotations

import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ingest_engine import (
    ColumnSpec,
    TableSpec,
    NotabilityConfig,
    UpsertOutcome,
    IngestReport,
    confidence_rate,
    CONFIDENCE_NATIVE,
    CONFIDENCE_INFERRED_HIGH,
    CONFIDENCE_INFERRED_MEDIUM,
    CONFIDENCE_INFERRED_LOW,
    create_schema_for_table,
    upsert_rows,
    compute_notability_scores,
    recency_weight,
    group_into_sessions,
    register_table_spec,
)

logger = logging.getLogger("chessdotcom_ingest")


# ============================================================================
# CONFIGURATION — unchanged values from the old file unless noted
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Paths (same fallback pattern as every other file in this project;
# config.py itself is untouched for now — project owner's decision,
# 2026-09-14: "config lo aggiustiamo in un altro momento")
# ----------------------------------------------------------------------------
try:
    from config import CHESSDOTCOM_INPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    CHESSDOTCOM_INPUT_DIR = BASE_DIR / "Input" / "Chessdotcom"
CHESSDOTCOM_INPUT_DIR = Path(CHESSDOTCOM_INPUT_DIR)

SOURCE_PREFIX = "chessdotcom"

# ----------------------------------------------------------------------------
# CONFIG — User identity (timelive.md §3: native signal, highest priority).
# Kept as a list (see old file's note: more than one chess.com account over
# time is a real possibility the project owner flagged, not hypothetical).
# ----------------------------------------------------------------------------
CHESSDOTCOM_USERNAMES = ["leonardocampese"]

# ----------------------------------------------------------------------------
# CONFIG — Time control -> time_class (chess.com's own documented
# boundaries; deterministic threshold, no confidence_rate needed)
# ----------------------------------------------------------------------------
BULLET_MAX_BASE_SECONDS = 179
BLITZ_MAX_BASE_SECONDS = 599
RAPID_MAX_BASE_SECONDS = 1800

TIME_CONTROL_PLAIN_RE = re.compile(r"^(\d+)$")
TIME_CONTROL_INCREMENT_RE = re.compile(r"^(\d+)\+(\d+)$")
TIME_CONTROL_DAILY_RE = re.compile(r"^(\d+)/(\d+)$")

# ----------------------------------------------------------------------------
# CONFIG — Termination text -> win_method (structural keyword match, order
# matters, first match wins)
# ----------------------------------------------------------------------------
WIN_METHOD_KEYWORDS: List[Tuple[str, str]] = [
    ("checkmate", "checkmate"),
    ("resignation", "resignation"),
    ("won on time", "timeout"),
    ("won - game abandoned", "abandonment"),
    ("abandoned", "abandonment"),
    ("drawn by agreement", "agreement"),
    ("drawn by repetition", "repetition"),
    ("drawn by stalemate", "stalemate"),
    ("insufficient material", "insufficient_material"),
    ("50-move rule", "fifty_move_rule"),
    ("50 move rule", "fifty_move_rule"),
    ("timeout", "timeout"),
    ("stalemate", "stalemate"),
]

UPSET_RATING_THRESHOLD = 150
OPENING_SIGNATURE_PLY_DEPTH = 6

# ----------------------------------------------------------------------------
# CONFIG — Playing-session detection (timelive.md discussion 2026-09-14:
# "games" + "playing_sessions" — adaptive gap, unchanged formula, validated
# on real data 2026-09-11: elbow at ~15-20 min for this file's time control,
# NOT the naive 30/60 min a different domain might have reused by analogy).
# ----------------------------------------------------------------------------
SESSION_EXCLUDED_TIME_CLASSES = {"daily", "unlimited", "unknown"}
SESSION_GAP_BASE_SECONDS = 60
SESSION_GAP_TIME_CONTROL_MULTIPLIER = 1.5
SESSION_GAP_MIN_SECONDS = 180
SESSION_GAP_MAX_SECONDS = 1800
SESSION_MIN_GAMES = 2
SESSION_CONFIDENCE = CONFIDENCE_INFERRED_HIGH

# ----------------------------------------------------------------------------
# CONFIG — notability_score weights, games (unchanged from the old file —
# only the recency "guarantee boost" that used to sit alongside these was
# removed, per the 2026-09-14 decision to drop the whole budget concept)
# ----------------------------------------------------------------------------
NOTABILITY_WEIGHT_OPPONENT_RATING = 0.5
NOTABILITY_WEIGHT_RECENCY = 0.3
NOTABILITY_WEIGHT_UPSET_BONUS = 0.3
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60

# ----------------------------------------------------------------------------
# CONFIG — notability_score weights, playing_sessions. THIS IS NEW: the old
# system never scored sessions, only individual games. No prior value to
# preserve here — flagged to the project owner as an invented default, not
# a carried-over decision, needs explicit confirmation or a different
# formula (see chat response after this file).
# ----------------------------------------------------------------------------
SESSION_NOTABILITY_WEIGHT_GAME_COUNT = 0.5
SESSION_NOTABILITY_WEIGHT_RECENCY = 0.5
SESSION_NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60
SESSION_NOTABILITY_GAME_COUNT_CAP = 10  # game_count signal saturates at this many games


# ============================================================================
# TABLE DECLARATIONS (timelive.md §3 — the "contract" for this domain)
# ============================================================================

GAMES_TABLE = TableSpec(
    name="games",
    primary_key_column="game_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    foreign_keys={"session_id": "playing_sessions(session_id)"},
    columns=[
        ColumnSpec("game_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                    semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("timestamp_begin", "TEXT",
                    semantic_note="derived/estimated; equals timestamp_end when no clock data exists to estimate duration"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="canonical timestamp — native, when this game actually ended"),
        ColumnSpec("duration_seconds", "REAL",
                    semantic_note="only present when the PGN includes %clk annotations; None otherwise, never guessed"),
        ColumnSpec("duration_confidence_rate", "REAL"),
        ColumnSpec("source", "TEXT"),
        ColumnSpec("time_control_raw", "TEXT"),
        ColumnSpec("time_class", "TEXT", semantic_note="bullet/blitz/rapid/classical/daily/unlimited/unknown"),
        ColumnSpec("base_time_seconds", "INTEGER"),
        ColumnSpec("increment_seconds", "INTEGER"),
        ColumnSpec("white", "TEXT"),
        ColumnSpec("black", "TEXT"),
        ColumnSpec("user_side", "TEXT", semantic_note="white/black/ambiguous_self_play/unknown"),
        ColumnSpec("user_username", "TEXT"),
        ColumnSpec("opponent_username", "TEXT", entity_hint="person"),
        ColumnSpec("user_rating", "INTEGER"),
        ColumnSpec("opponent_rating", "INTEGER"),
        ColumnSpec("rating_diff", "INTEGER", semantic_note="user_rating - opponent_rating"),
        ColumnSpec("result_raw", "TEXT", semantic_note="PGN Result tag: 1-0 / 0-1 / 1/2-1/2"),
        ColumnSpec("result_for_user", "TEXT", semantic_note="win/loss/draw/unknown, from the user's own side"),
        ColumnSpec("termination_raw", "TEXT"),
        ColumnSpec("win_method", "TEXT",
                    semantic_note="checkmate/resignation/timeout/abandonment/agreement/repetition/stalemate/insufficient_material/fifty_move_rule/unknown"),
        ColumnSpec("is_upset", "INTEGER",
                    semantic_note="1 if the weaker-rated side (>=150 point gap) won or the stronger side lost, else 0"),
        ColumnSpec("ply_count", "INTEGER"),
        ColumnSpec("opening_signature", "TEXT", semantic_note="first 6 half-moves in SAN, a fingerprint — NOT a named opening (no ECO data available)"),
        ColumnSpec("session_id", "INTEGER", semantic_note="NULL if this game is not part of any detected playing session"),
        ColumnSpec("notability_score", "REAL"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

GAME_MOVES_TABLE = TableSpec(
    name="game_moves",
    primary_key_column="move_id",
    dedup_key_column=None,  # owned entirely by its parent game — see run_ingest()
    foreign_keys={"game_id": "games(game_id)"},
    columns=[
        ColumnSpec("move_id", "INTEGER"),
        ColumnSpec("game_id", "INTEGER", not_null=True),
        ColumnSpec("ply_number", "INTEGER", not_null=True, semantic_note="1-based, white plies odd, black plies even"),
        ColumnSpec("move_san", "TEXT", not_null=True),
        ColumnSpec("clock_seconds", "REAL", semantic_note="remaining clock time after this move, when the PGN includes %clk — usually NULL"),
    ],
)

PLAYING_SESSIONS_TABLE = TableSpec(
    name="playing_sessions",
    primary_key_column="session_id",
    dedup_key_column=None,  # fully rebuilt every ingest run — see run_ingest()
    canonical_timestamp_column="timestamp_begin",
    columns=[
        ColumnSpec("session_id", "INTEGER"),
        ColumnSpec("timestamp_begin", "TEXT", not_null=True),
        ColumnSpec("timestamp_end", "TEXT", not_null=True),
        ColumnSpec("duration_seconds", "INTEGER"),
        ColumnSpec("game_count", "INTEGER"),
        ColumnSpec("win_count", "INTEGER"),
        ColumnSpec("loss_count", "INTEGER"),
        ColumnSpec("draw_count", "INTEGER"),
        ColumnSpec("notability_score", "REAL"),
        ColumnSpec("confidence_rate", "REAL",
                    semantic_note="confidence that this grouping of games is really one sitting, not that the games themselves happened"),
    ],
)

# Registered at import time (not inside run_ingest()) so that just
# importing this module — e.g. from llm_bridge.py, to build a schema
# manifest for the model — is enough to know these tables' columns and
# semantic notes, without needing to actually run an ingest first.
register_table_spec(PLAYING_SESSIONS_TABLE)
register_table_spec(GAMES_TABLE)
register_table_spec(GAME_MOVES_TABLE)


# ============================================================================
# PARSING — file reading, PGN splitting (unchanged from the old file)
# ============================================================================

def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except Exception:
        return default


def to_iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def read_text_with_fallback_encoding(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    raise RuntimeError(f"Could not read {path} with any known encoding.")


def collect_input_files(input_dir: Path) -> List[Path]:
    if not input_dir.exists():
        return []
    return sorted(p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() == ".pgn")


_GAME_START_RE = re.compile(r"(?m)^\[Event\s")
_HEADER_LINE_RE = re.compile(r'^\[(\w+)\s+"([^"]*)"\]\s*$', re.MULTILINE)
_RESULT_TOKEN_RE = re.compile(r"\s*(1-0|0-1|1/2-1/2|\*)\s*$")
_CLOCK_RE = re.compile(r"\[%clk\s+(\d+):(\d{2}):(\d{2}(?:\.\d+)?)\]")
_MOVE_NUMBER_RE = re.compile(r"^\d+\.(\.\.)?$")
_END_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2}):(\d{2})\s+GMT([+-]\d{2})(\d{2})$")


def split_pgn_games(raw_text: str) -> List[str]:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    starts = [m.start() for m in _GAME_START_RE.finditer(text)]
    if not starts:
        return []
    blocks = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        block = text[start:end].strip()
        if block:
            blocks.append(block)
    return blocks


def parse_game_block(block: str) -> Tuple[Dict[str, str], str]:
    headers: Dict[str, str] = {}
    movetext_lines: List[str] = []
    for line in block.split("\n"):
        m = _HEADER_LINE_RE.match(line)
        if m:
            headers[m.group(1)] = m.group(2)
        elif line.strip():
            movetext_lines.append(line.strip())
    movetext = " ".join(movetext_lines)
    movetext = _RESULT_TOKEN_RE.sub("", movetext).strip()
    return headers, movetext


def parse_time_control(tc_raw: str) -> Tuple[Optional[int], Optional[int], str]:
    tc = normalize_string(tc_raw)
    if not tc or tc == "-":
        return None, None, "unlimited"
    m = TIME_CONTROL_DAILY_RE.match(tc)
    if m:
        return None, None, "daily"
    m = TIME_CONTROL_INCREMENT_RE.match(tc)
    if m:
        base = int(m.group(1))
        increment = int(m.group(2))
        return base, increment, _time_class_from_base_seconds(base)
    m = TIME_CONTROL_PLAIN_RE.match(tc)
    if m:
        base = int(m.group(1))
        return base, 0, _time_class_from_base_seconds(base)
    return None, None, "unknown"


def _time_class_from_base_seconds(base_seconds: int) -> str:
    if base_seconds <= BULLET_MAX_BASE_SECONDS:
        return "bullet"
    if base_seconds <= BLITZ_MAX_BASE_SECONDS:
        return "blitz"
    if base_seconds <= RAPID_MAX_BASE_SECONDS:
        return "rapid"
    return "classical"


def parse_end_timestamp(date_raw: str, end_time_raw: str) -> str:
    date_str = normalize_string(date_raw)
    end_str = normalize_string(end_time_raw)
    if not date_str or not end_str:
        return ""
    try:
        d = datetime.strptime(date_str, "%Y.%m.%d")
    except Exception:
        return ""
    m = _END_TIME_RE.match(end_str)
    if not m:
        return ""
    hour, minute, second, offset_h, offset_m = m.groups()
    dt = d.replace(hour=int(hour), minute=int(minute), second=int(second))
    offset = timedelta(hours=int(offset_h), minutes=int(offset_m) * (1 if int(offset_h) >= 0 else -1))
    dt_utc = dt - offset
    return to_iso_utc(dt_utc.replace(tzinfo=timezone.utc))


def extract_moves_and_clocks(movetext: str) -> Tuple[List[str], List[Optional[float]]]:
    clocks_in_order = [
        float(h) * 3600 + float(mi) * 60 + float(s)
        for h, mi, s in _CLOCK_RE.findall(movetext)
    ]
    text_no_comments = re.sub(r"\{[^}]*\}", "", movetext)
    tokens = text_no_comments.split()
    moves: List[str] = []
    for tok in tokens:
        if _MOVE_NUMBER_RE.match(tok):
            continue
        if tok in ("1-0", "0-1", "1/2-1/2", "*"):
            continue
        moves.append(tok)
    if clocks_in_order and len(clocks_in_order) != len(moves):
        clocks_in_order = []
    clocks: List[Optional[float]] = list(clocks_in_order) if clocks_in_order else [None] * len(moves)
    return moves, clocks


def build_opening_signature(moves: List[str], ply_depth: int) -> str:
    return " ".join(moves[:ply_depth])


def estimate_game_duration_seconds(
    moves: List[str],
    clocks: List[Optional[float]],
    base_time_seconds: Optional[int],
    increment_seconds: Optional[int],
) -> Optional[float]:
    if base_time_seconds is None or not moves or not any(c is not None for c in clocks):
        return None
    increment = increment_seconds or 0
    white_last: Optional[float] = None
    black_last: Optional[float] = None
    white_count = 0
    black_count = 0
    for idx, clk in enumerate(clocks):
        is_white_ply = (idx % 2 == 0)
        if is_white_ply:
            white_count += 1
        else:
            black_count += 1
        if clk is None:
            continue
        if is_white_ply:
            white_last = clk
        else:
            black_last = clk
    consumed_total = 0.0
    found_any = False
    if white_last is not None:
        consumed_total += max(base_time_seconds + increment * white_count - white_last, 0.0)
        found_any = True
    if black_last is not None:
        consumed_total += max(base_time_seconds + increment * black_count - black_last, 0.0)
        found_any = True
    if not found_any or consumed_total <= 0:
        return None
    return round(consumed_total, 1)


def identify_user_side(white: str, black: str, usernames_lower: set) -> str:
    w = (white or "").strip().lower()
    b = (black or "").strip().lower()
    w_match = w in usernames_lower
    b_match = b in usernames_lower
    if w_match and b_match:
        return "ambiguous_self_play"
    if w_match:
        return "white"
    if b_match:
        return "black"
    return "unknown"


def classify_win_method(termination_raw: str) -> str:
    text = (termination_raw or "").lower()
    for keyword, method in WIN_METHOD_KEYWORDS:
        if keyword in text:
            return method
    return "unknown"


def compute_result_for_user(result_raw: str, user_side: str) -> str:
    if user_side not in ("white", "black"):
        return "unknown"
    if result_raw == "1/2-1/2":
        return "draw"
    if result_raw == "1-0":
        return "win" if user_side == "white" else "loss"
    if result_raw == "0-1":
        return "win" if user_side == "black" else "loss"
    return "unknown"


# ============================================================================
# NORMALIZATION — record building (field names updated to the timestamp_*
# naming standard, timelive.md §4; is_upset now an int 0/1)
# ============================================================================

def build_record(
    headers: Dict[str, str],
    movetext: str,
    source_file: Path,
    record_index_in_source: int,
    usernames_lower: set,
) -> Dict[str, Any]:
    white = normalize_string(headers.get("White"))
    black = normalize_string(headers.get("Black"))
    result_raw = normalize_string(headers.get("Result"))
    termination_raw = normalize_string(headers.get("Termination"))

    timestamp_end = parse_end_timestamp(headers.get("Date", ""), headers.get("EndTime", ""))

    base_time_seconds, increment_seconds, time_class = parse_time_control(headers.get("TimeControl", ""))

    moves, clocks = extract_moves_and_clocks(movetext)
    ply_count = len(moves)
    opening_signature = build_opening_signature(moves, OPENING_SIGNATURE_PLY_DEPTH)

    duration_seconds = estimate_game_duration_seconds(moves, clocks, base_time_seconds, increment_seconds)
    duration_confidence = confidence_rate(CONFIDENCE_INFERRED_MEDIUM) if duration_seconds is not None else None

    if timestamp_end and duration_seconds is not None:
        try:
            end_dt = datetime.fromisoformat(timestamp_end.replace("Z", "+00:00"))
            timestamp_begin = to_iso_utc(end_dt - timedelta(seconds=duration_seconds))
        except Exception:
            timestamp_begin = timestamp_end
    else:
        timestamp_begin = timestamp_end

    user_side = identify_user_side(white, black, usernames_lower)
    if user_side == "white":
        user_username, opponent_username = white, black
        user_rating = safe_int(headers.get("WhiteElo"))
        opponent_rating = safe_int(headers.get("BlackElo"))
    elif user_side == "black":
        user_username, opponent_username = black, white
        user_rating = safe_int(headers.get("BlackElo"))
        opponent_rating = safe_int(headers.get("WhiteElo"))
    else:
        user_username, opponent_username = None, None
        user_rating, opponent_rating = None, None

    rating_diff = (
        user_rating - opponent_rating if user_rating is not None and opponent_rating is not None else None
    )

    result_for_user = compute_result_for_user(result_raw, user_side)
    win_method = classify_win_method(termination_raw)

    is_upset = False
    if rating_diff is not None and result_for_user in ("win", "loss"):
        if result_for_user == "win" and rating_diff <= -UPSET_RATING_THRESHOLD:
            is_upset = True
        elif result_for_user == "loss" and rating_diff >= UPSET_RATING_THRESHOLD:
            is_upset = True

    return {
        "timestamp_begin": timestamp_begin,
        "timestamp_end": timestamp_end,
        "duration_seconds": duration_seconds,
        "duration_confidence_rate": duration_confidence,
        "source": SOURCE_PREFIX,
        "time_control_raw": normalize_string(headers.get("TimeControl")),
        "time_class": time_class,
        "base_time_seconds": base_time_seconds,
        "increment_seconds": increment_seconds,
        "white": white,
        "black": black,
        "user_side": user_side,
        "user_username": user_username,
        "opponent_username": opponent_username,
        "user_rating": user_rating,
        "opponent_rating": opponent_rating,
        "rating_diff": rating_diff,
        "result_raw": result_raw,
        "result_for_user": result_for_user,
        "termination_raw": termination_raw,
        "win_method": win_method,
        "is_upset": int(is_upset),
        "ply_count": ply_count,
        "opening_signature": opening_signature,
        "session_id": None,  # filled in after session detection, see run_ingest()
        "source_file": source_file.name,
        "record_index_in_source": record_index_in_source,  # transient, dropped before insert
        "_moves": moves,      # transient, used to build game_moves rows only
        "_clocks": clocks,    # transient, same
    }


def build_dedup_key(record: Dict[str, Any]) -> str:
    """
    Single computed string, replacing the old composite-key tuple — see
    ingest_engine.py's upsert_rows() docstring for why. Same fields as the
    old system used (no [Link] header exists in this export — confirmed
    on real data, see REAL DATA FINDINGS in the old file's history).
    """
    return "|".join([
        (record.get("white") or "").strip().lower(),
        (record.get("black") or "").strip().lower(),
        record.get("timestamp_end") or "",
        record.get("time_control_raw") or "",
        record.get("result_raw") or "",
    ])


# ============================================================================
# NOTABILITY — games (unchanged formula), playing_sessions (new, see CONFIG)
# ============================================================================

def _compute_opponent_rating_percentiles(records: List[Dict[str, Any]]) -> None:
    """
    Attaches `_opponent_rating_percentile` (0..1) to each record, computed
    within its own time_class group. Precomputed rank dict, not
    list.index() in a loop (timelive.md §7: avoid O(n²) patterns).
    """
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("opponent_rating") is not None:
            groups[record.get("time_class", "unknown")].append(record)

    for _, group_records in groups.items():
        ratings_sorted = sorted(r["opponent_rating"] for r in group_records)
        n = len(ratings_sorted)
        rank_of_rating: Dict[int, int] = {}
        for idx, rating in enumerate(ratings_sorted):
            if rating not in rank_of_rating:
                rank_of_rating[rating] = idx
        for record in group_records:
            rank = rank_of_rating[record["opponent_rating"]]
            record["_opponent_rating_percentile"] = rank / max(n - 1, 1)


def apply_game_notability(records: List[Dict[str, Any]]) -> None:
    _compute_opponent_rating_percentiles(records)
    compute_notability_scores(
        records,
        NotabilityConfig(
            weight_functions={
                "opponent_rating": lambda r: r.get("_opponent_rating_percentile", 0.0),
                "recency": lambda r: recency_weight(r.get("timestamp_end"), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS),
                "upset_bonus": lambda r: 1.0 if r.get("is_upset") else 0.0,
            },
            weights={
                "opponent_rating": NOTABILITY_WEIGHT_OPPONENT_RATING,
                "recency": NOTABILITY_WEIGHT_RECENCY,
                "upset_bonus": NOTABILITY_WEIGHT_UPSET_BONUS,
            },
        ),
    )
    for record in records:
        record.pop("_opponent_rating_percentile", None)


def apply_session_notability(sessions: List[Dict[str, Any]]) -> None:
    """NEW — see CONFIG note above, no prior formula existed for sessions."""
    compute_notability_scores(
        sessions,
        NotabilityConfig(
            weight_functions={
                "game_count": lambda s: min(s.get("game_count", 0) / SESSION_NOTABILITY_GAME_COUNT_CAP, 1.0),
                "recency": lambda s: recency_weight(s.get("timestamp_end"), half_life_days=SESSION_NOTABILITY_RECENCY_HALF_LIFE_DAYS),
            },
            weights={
                "game_count": SESSION_NOTABILITY_WEIGHT_GAME_COUNT,
                "recency": SESSION_NOTABILITY_WEIGHT_RECENCY,
            },
        ),
    )


# ============================================================================
# PLAYING-SESSION DETECTION
# ============================================================================

def _session_gap_seconds_fn(previous: Dict[str, Any], current: Dict[str, Any]) -> float:
    next_base = current.get("base_time_seconds") or 0
    allowed = SESSION_GAP_BASE_SECONDS + SESSION_GAP_TIME_CONTROL_MULTIPLIER * next_base
    return max(SESSION_GAP_MIN_SECONDS, min(allowed, SESSION_GAP_MAX_SECONDS))


def detect_playing_sessions(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    `records` must be sorted chronologically already. Excludes daily/
    unlimited/unknown time-control games (no meaningful "still playing"
    gap exists for those — same as the old system). Returns a list of
    session dicts AND, as a side effect, sets `record["_session_index"]`
    on every record that ends up inside a session with >= SESSION_MIN_GAMES
    games (an index into the returned list — used by run_ingest() to
    resolve the real session_id once sessions are written to the DB).
    """
    live_records = [
        r for r in records
        if r.get("time_class") not in SESSION_EXCLUDED_TIME_CLASSES and r.get("timestamp_end")
    ]
    groups = group_into_sessions(
        live_records,
        timestamp_begin_field="timestamp_end",  # a game is treated as instantaneous for gap purposes
        timestamp_end_field="timestamp_end",
        gap_seconds_fn=_session_gap_seconds_fn,
    )

    sessions: List[Dict[str, Any]] = []
    for group in groups:
        if len(group) < SESSION_MIN_GAMES:
            continue

        session_index = len(sessions)
        begin_ts = group[0]["timestamp_end"]
        end_ts = group[-1]["timestamp_end"]
        begin_dt = datetime.fromisoformat(begin_ts.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_ts.replace("Z", "+00:00"))

        for r in group:
            r["_session_index"] = session_index

        sessions.append({
            "timestamp_begin": begin_ts,
            "timestamp_end": end_ts,
            "duration_seconds": round((end_dt - begin_dt).total_seconds()),
            "game_count": len(group),
            "win_count": sum(1 for r in group if r.get("result_for_user") == "win"),
            "loss_count": sum(1 for r in group if r.get("result_for_user") == "loss"),
            "draw_count": sum(1 for r in group if r.get("result_for_user") == "draw"),
            "confidence_rate": confidence_rate(SESSION_CONFIDENCE),
        })

    return sessions


# ============================================================================
# MAIN ENTRYPOINT — the contract ingest_engine.py's CLI expects
# ============================================================================

def run_ingest(conn, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    """
    1. create schema (playing_sessions and games first — games has a
       foreign key to playing_sessions; game_moves last — it points at games)
    2. read every *.pgn file, parse+classify every game (in memory)
    3. sort chronologically
    4. compute notability for games
    5. detect playing sessions (in memory) — note the whole raw input
       directory is re-read every run (chess.com's own export process
       naturally re-exports growing history, not just new games), so this
       in-memory pass already reflects the complete current dataset, same
       as the old system — no need to re-read anything back from the DB
    6. write playing_sessions FIRST (full rebuild every run — session_id
       is NOT stable across re-ingests, only game_id is; see chat
       explanation), to get real session_id values
    7. upsert games (stable game_id across re-ingests), resolving each
       game's session_id from step 6
    8. for games that were NEWLY inserted this run, also insert their
       moves into game_moves (skip for already-existing games, so a
       re-ingest never duplicates move rows even though game_moves has no
       dedup key of its own)
    """
    create_schema_for_table(conn, PLAYING_SESSIONS_TABLE)
    create_schema_for_table(conn, GAMES_TABLE)
    create_schema_for_table(conn, GAME_MOVES_TABLE)

    usernames_lower = {u.strip().lower() for u in CHESSDOTCOM_USERNAMES if u.strip()}
    input_files = collect_input_files(CHESSDOTCOM_INPUT_DIR)
    logger.info("found %d .pgn file(s) in %s", len(input_files), CHESSDOTCOM_INPUT_DIR)

    all_records: List[Dict[str, Any]] = []
    error_count = 0
    for source_path in input_files:
        try:
            raw_text = read_text_with_fallback_encoding(source_path)
            blocks = split_pgn_games(raw_text)
            logger.debug("%s: %d game block(s)", source_path.name, len(blocks))
            for idx, block in enumerate(blocks):
                try:
                    headers, movetext = parse_game_block(block)
                    record = build_record(headers, movetext, source_path, idx, usernames_lower)
                    all_records.append(record)
                except Exception as exc:
                    error_count += 1
                    logger.warning("%s game #%d: parse error: %s", source_path.name, idx, exc)
        except Exception as exc:
            error_count += 1
            logger.warning("%s: file read error: %s", source_path.name, exc)

    if error_count:
        logger.warning("%d game(s)/file(s) skipped due to errors — see warnings above", error_count)

    # Chronological sort — same tiebreakers as before (timestamp, then
    # source file, then position within that file), now used for
    # processing/insertion order rather than to assign a manual counter.
    all_records.sort(key=lambda r: (r.get("timestamp_end", ""), r.get("source_file", ""), r.get("record_index_in_source", 0)))

    for record in all_records:
        record["dedup_key"] = build_dedup_key(record)

    apply_game_notability(all_records)
    sessions = detect_playing_sessions(all_records)
    apply_session_notability(sessions)
    unknown_user_side_count = sum(1 for r in all_records if r.get("user_side") == "unknown")
    logger.info(
        "%d game(s) parsed, %d playing session(s) detected, %d game(s) with unrecognized user_side",
        len(all_records), len(sessions), unknown_user_side_count,
    )

    # --- 6. playing_sessions: full rebuild every run ---
    # Games still point at last run's session rows (session_id foreign
    # key), so those links must be cleared FIRST, or DELETE below fails
    # with a foreign-key error (found by actually running this twice
    # against the same data, not by inspection — see chat explanation).
    conn.execute("UPDATE games SET session_id = NULL")
    conn.execute("DELETE FROM playing_sessions")
    session_id_by_index: Dict[int, int] = {}
    for idx, session in enumerate(sessions):
        outcome = upsert_rows(conn, PLAYING_SESSIONS_TABLE, [session])[0]
        session_id_by_index[idx] = outcome.primary_key

    for record in all_records:
        session_index = record.pop("_session_index", None)
        record["session_id"] = session_id_by_index.get(session_index) if session_index is not None else None

    # --- 7. games: stable upsert ---
    game_outcomes: List[UpsertOutcome] = upsert_rows(conn, GAMES_TABLE, all_records)

    # --- 8. game_moves: only for newly-inserted games ---
    moves_inserted = 0
    for record, outcome in zip(all_records, game_outcomes):
        if not outcome.was_new:
            continue
        move_rows = [
            {
                "game_id": outcome.primary_key,
                "ply_number": i + 1,
                "move_san": san,
                "clock_seconds": clock,
            }
            for i, (san, clock) in enumerate(zip(record["_moves"], record["_clocks"]))
        ]
        if move_rows:
            upsert_rows(conn, GAME_MOVES_TABLE, move_rows)
            moves_inserted += len(move_rows)

    rows_inserted = sum(1 for o in game_outcomes if o.was_new) + len(sessions) + moves_inserted
    rows_already_present = sum(1 for o in game_outcomes if not o.was_new)

    return IngestReport(
        domain="chessdotcom",
        tables_written=["playing_sessions", "games", "game_moves"],
        rows_inserted=rows_inserted,
        rows_already_present=rows_already_present,
        dry_run=dry_run,
    )
