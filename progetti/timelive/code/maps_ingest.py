# maps_ingest.py
# =============================================================================
# MAPS INGEST — Personal Data Vault (Movement / Location domain)
# ingest_engine.py / vault.db version — sixth domain migrated
# =============================================================================
#
# CORRECTION TO THE MIGRATION BRIEF THIS FILE WAS BUILT FROM (2026-09-17):
# the brief for this session claimed maps had never been built on the old
# PRIMARY/FULL JSON system and that there was no legacy maps_ingest.py to
# port. That was wrong — a real, working maps_ingest.py (v4.1) already
# existed, had already been run against this same Timeline.json, and its
# output (output/maps_dataset.json, generated 2026-09-10) was sitting on
# disk. timelive.md §1/§8 and EVOLUTION_LOG.md's own "v4.1" entry both say
# plainly that maps is one of the three domains still on the OLD system,
# not a domain that was never built — the brief conflated "never migrated
# to ingest_engine.py" with "never built". Confirmed independently (not
# just trusting either the brief or the old file) by re-inspecting
# Timeline.json directly before writing anything here. Given that, THIS
# migration follows the same pattern as chess.com/spotify/money: port the
# old file's already-validated decisions, re-verify each against today's
# real export, don't re-derive from zero.
#
# INPUT FORMAT (re-verified against the real export, 2026-09-17 —
# timelive.md §7: real data before schema)
# -----------------------------------------------------------------------
# Google's "Timeline.json" export is a flat JSON list (2,994 entries as of
# 2026-09-17 — re-check this count, the project owner may export again).
# Each element covers one [startTime, endTime) span and carries EXACTLY
# ONE of three keys:
#
#   * "visit"        -> a stay at a place: hierarchyLevel, topCandidate
#                        {probability, semanticType, placeID, placeLocation
#                        as a "geo:<lat>,<lon>" string}, probability
#                        (segment-level). 940 of 2,994 entries.
#   * "activity"      -> a movement: topCandidate {type, probability},
#                        distanceMeters, start/end ("geo:<lat>,<lon>"),
#                        probability (segment-level). 753 of 2,994 entries.
#   * "timelinePath"  -> a raw GPS breadcrumb (a list of {point,
#                        durationMinutesOffsetFromStartTime}). 1,301 of
#                        2,994 entries, 12,234 raw points total (1-120
#                        points per entry, avg ~9.4). Re-confirmed the old
#                        file's finding: every timelinePath entry in this
#                        export is one CONTIGUOUS block after every
#                        visit/activity entry (index 1693 onward of 2,994)
#                        — this is effectively two concatenated arrays,
#                        not one chronological stream.
#
# Some Google export variants wrap the same flat records under
# {"semanticSegments": [...], "rawSignals": [...]} instead of a bare
# top-level list (today's real export is a bare list; both shapes are
# still supported defensively, see _load_timeline_entries). The much
# older nested "timelineObjects"/"activitySegment"/"placeVisit" format
# (pre-2024 Google Takeout) is explicitly OUT OF SCOPE — a structurally
# different schema that would need its own normalization branch.
#
# DECISION, reconfirmed with the project owner in this session:
# "timelinePath" is NOT ingested. Redundant with "activity" for the
# semantic-movement purpose this vault serves. Its skipped entry/point
# counts are logged (not silently dropped) for traceability, but not
# written to any table.
#
# REAL-DATA FINDING — semantic_type is meaningful more often than a
# single sample suggests: across all 940 visits in this export,
# semanticType is 'Unknown' 75.7% of the time, but 'Aliased Location'
# 16.2%, 'Home' 3.9%, 'Searched Address' 3.1%, and 'Work' 1.1% — a real
# quarter of visits carry a meaningful native label. Kept 100% VERBATIM
# (never lowercased/remapped) so distinct home-like labels stay
# distinguishable — see maps_labeled_places below, which has a real
# second-home label ("Home AT") that this same project owner's data
# already produces.
#
# REAL-DATA FINDING — activity_type (topCandidate.type): 8 distinct
# values in this export — 'in passenger vehicle' (63.5%), 'walking'
# (22.7%), 'cycling' (4.4%), 'in bus' (2.9%), 'in train' (2.8%), 'in
# subway' (2.5%), 'flying' (0.8%), 'in tram' (0.4%). Kept verbatim, same
# reasoning as semantic_type.
#
# REAL-DATA FINDING — dedup key verified collision-free: the composite
# key (event_type, begin_timestamp, end_timestamp, + place_id for visits
# / activity_type+distance_meters for activities) produces zero
# collisions across all 1,693 real visit+activity records in this
# export. Split per-table below (see compute_visit_dedup_key /
# compute_activity_dedup_key) since visit and activity now live in
# separate tables — mathematically the same key, just without the
# always-empty fields for the other type.
#
# REAL-DATA FINDING — date range: earliest entry 2025-05-18, latest
# 2026-09-05 (~15.5 months). The project owner has stated this export is
# NOT a complete history — real location data only goes back roughly a
# year. This matches Timeline/Settings.json's retentionControl (540-day
# retention window) found while exploring Input/Maps — that file is
# informational only, not ingested (see "OUT OF SCOPE THIS PASS" below).
# Missing older history is an export/retention limitation, not a parsing
# bug — not something to chase.
#
# TABLE SHAPE: two tables (maps_visits, maps_activities), not one flat
# table. visit and activity have almost entirely disjoint fields
# (place_id/semantic_type vs. activity_type/distance/start+end
# coordinates) — same reasoning the project already applied to
# money_ingest.py's transactions/security_events/private_market_legs and
# PayPal's dedicated table: a table where ~40% of columns are always
# NULL for every row is worse than two tables with no wasted columns.
# No foreign key between them — same "linked only by shared fields, not
# FK" pattern as money's three tables.
#
# GEO PARSING — two DIFFERENT native formats in this same domain, do not
# conflate them:
#   * Timeline.json uses "geo:<lat>,<lon>" strings (lat first) —
#     parse_geo_string().
#   * Labeled places.json (GeoJSON) uses "coordinates": [lon, lat]
#     (lon first — the GeoJSON spec's own order) — parse_geojson_point().
#     Verified against real data: Home's coordinates [7.5353208,
#     45.1148464] only make sense as lon=7.5353208/lat=45.1148464
#     (Pianezza, Italy is ~45°N 7.5°E); reading them in the other order
#     would silently misplace every labeled place. Both parsers return
#     (latitude, longitude) in that order regardless of the native
#     source order, so nothing downstream has to know about this.
# Both latitude/longitude columns are kept as parsed REAL columns AND the
# native string/array is preserved verbatim alongside where the source is
# a string (place_location_raw, start/end_location_raw) — timelive.md §3
# native-value-preservation precedent (money's category_raw).
#
# PRIVACY — raw lat/lon is more re-identifying than almost anything else
# in this vault (home, workplace, travel patterns all directly
# derivable). Explicit decision (this session): kept NATIVE, not rounded
# or generalized, every coordinate column marked ColumnSpec.sensitive=True
# — same treatment as PayPal's saldo / Instagram's DM content. A marker
# for a future handling layer, not an access control today.
#
# RE-EXPORT / REFRESH BEHAVIOUR — the project owner is not certain a
# fresh Timeline.json export always contains the FULL retained history
# from scratch; it could be a rolling/incremental window. No special
# handling was needed for this: ingest_engine.py's upsert_rows() is
# already additive-only by construction (INSERT ... existing row keeps
# its id but gets UPDATEd; nothing is ever DELETEd on re-ingest) for
# every domain, not just this one. Re-ingesting a narrower future export
# can only add/refresh rows, never silently drop ones already in the
# vault.
#
# BUSINESS LOGIC DELIBERATELY NOT PORTED FROM THE OLD FILE (project
# owner's explicit call, this session): the old maps_ingest.py also had
# is_home detection (semantic_type prefix match), trip detection (2h
# minimum duration between home visits), and notability_score. None of
# that is in this version — both tables normalize raw visit/activity
# rows only. Same reasoning instagram_ingest.py already established for
# dropping notability_score there: duration/distance/native-probability
# ARE real signals that could ground a formula later, but building one
# now would be exactly the "business logic" just deferred, not the
# data-first minimalism timelive.md §7 asks for. Revisit alongside trip
# detection in a future round if it proves useful against real queries.
#
# OUT OF SCOPE THIS PASS — Input/Maps is a full Google Takeout bundle,
# not just Timeline.json. Every file in it was actually opened and read
# (not assumed) before this decision. Only Timeline.json (visit/activity)
# and Labeled places.json are ingested here; everything else is
# documented, not built, per the project owner's explicit "as few tables
# as possible" call this session:
#   * Maps (your places)/Reviews.json — 22 real reviews 2017-2026 (coords,
#     date, 1-5 star rating, place name/address, free-text review,
#     sometimes structured Q&A). Genuinely rich, worth a maps_reviews
#     table in a future round.
#   * Maps (your places)/Saved Places.json — 5 rows, "want to go" places
#     with save date. 3 of 5 carry a (0,0) placeholder coordinate with an
#     explicit "no location available" comment — would need to become
#     NULL, not a literal 0,0, if ever ingested.
#   * Maps/Photos and videos/ — 15 geotagged photos/videos (2017-2024,
#     ~50MB of actual media that would NOT be ingested — only the .json
#     sidecars: photoTakenTime, lat/lon, title, view count). Would extend
#     real location history back to 2017, well before Timeline's
#     ~2025-05 start, if ever ingested.
#   * Maps/Traffic incident reports and votes/ — 19 tiny files
#     (contributionType + disruptionType, e.g. CONFIRM/POLICE), timestamp
#     only in the filename. Real but a very thin domain.
#   * Maps/Commute routes/Commute routes.json — 5 SAVED ROUTE CONFIGS
#     (e.g. home->work via TRANSIT with real leg-by-leg detail), NOT a
#     log of actual trips — no timestamps at all, doesn't fit this
#     vault's timestamp-based model. Recommended against ingesting even
#     in a future round, flagged rather than silently dropped.
#   * Timeline/Settings.json — Google account/device Timeline feature
#     settings (retention window, reporting toggles, device list). Not
#     personal history data, informational only (see "date range" finding
#     above for the one useful fact it contains).
#   * Maps/Added dishes products activities (1 row), Maps/Suggested edits
#     to business establishments (1 row), Maps/Commute settings,
#     Maps/Electric vehicle settings, Maps/Questions and Answers,
#     Maps/Requests for services, Maps/Vehicle profiles, Maps/Your local
#     followed places — all inspected directly: either genuinely empty or
#     a single row. No real content to ingest today.
#
# LABELED PLACES — the one addition beyond Timeline.json this pass. Only
# 3 rows (Home in Pianezza IT, Work in Mattighofen AT, and a second home
# "Home AT" in Salzburg) but high value: real ground truth for the
# multi-home case Timeline's own semantic_type labels only hint at, kept
# as its own tiny reference table (no canonical timestamp — it has none
# in the source — no notability_score, same minimalism as everywhere
# else this pass).
#
# CONVENTIONS (same as every other domain)
# -----------------------------------------------------------------------
#  * every timestamp is converted to ISO 8601 UTC
#  * durations in seconds (duration_seconds)
#  * duplicates are removed automatically (upsert_rows, stable ids across
#    re-ingests)
#
# HOW TO MODIFY ANYTHING
# -----------------------------------
# TableSpecs are declared at module level (timelive.md §5: a domain
# registers its schema at import time, not inside the ingest function).
# =============================================================================

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ingest_engine import (
    ColumnSpec,
    TableSpec,
    IngestReport,
    UpsertOutcome,
    create_schema_for_table,
    upsert_rows,
    register_table_spec,
)

logger = logging.getLogger("maps_ingest")


# ============================================================================
# CONFIGURATION
# ============================================================================

try:
    from config import MAPS_INPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    MAPS_INPUT_DIR = BASE_DIR / "Input" / "Maps"
MAPS_INPUT_DIR = Path(MAPS_INPUT_DIR)

SOURCE_PREFIX = "maps"


# ============================================================================
# HELPERS — timestamps, numbers, geo
# ============================================================================

def to_iso_utc(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return None


def _duration_seconds(begin_iso: Optional[str], end_iso: Optional[str]) -> Optional[float]:
    if not begin_iso or not end_iso:
        return None
    try:
        dt_begin = datetime.fromisoformat(begin_iso)
        dt_end = datetime.fromisoformat(end_iso)
        return round((dt_end - dt_begin).total_seconds(), 3)
    except ValueError:
        return None


def safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def safe_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


_GEO_STRING_RE = re.compile(r"^geo:(-?\d+\.?\d*),(-?\d+\.?\d*)$")


def parse_geo_string(value: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    """Timeline.json's native 'geo:<lat>,<lon>' strings — lat first. See
    module docstring's GEO PARSING note: do not conflate with
    parse_geojson_point's [lon, lat] order."""
    if not value:
        return None, None
    m = _GEO_STRING_RE.match(value.strip())
    if not m:
        return None, None
    return safe_float(m.group(1)), safe_float(m.group(2))


def parse_geojson_point(coordinates: Any) -> Tuple[Optional[float], Optional[float]]:
    """Labeled places.json's GeoJSON 'coordinates': [lon, lat] — the
    OPPOSITE order from parse_geo_string. See module docstring's GEO
    PARSING note for the real-data check that confirmed this order."""
    if not coordinates or len(coordinates) < 2:
        return None, None
    lon, lat = coordinates[0], coordinates[1]
    return safe_float(lat), safe_float(lon)


# ============================================================================
# SCHEMA — maps_visits / maps_activities / maps_labeled_places
# ============================================================================

MAPS_VISITS_TABLE = TableSpec(
    name="maps_visits",
    primary_key_column="visit_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="begin_timestamp",
    extra_indexed_columns=["semantic_type"],
    columns=[
        ColumnSpec("visit_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                   semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("begin_timestamp", "TEXT", not_null=True,
                   semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("end_timestamp", "TEXT", not_null=True, semantic_note="native, ISO 8601 UTC"),
        ColumnSpec("duration_seconds", "REAL"),
        ColumnSpec("place_id", "TEXT", entity_hint="location",
                   semantic_note="native — Google's own place id, stable across re-exports of the same real-world place"),
        ColumnSpec("semantic_type", "TEXT",
                   semantic_note="native, verbatim from Google, NEVER remapped/lowercased. Real values (2,994-entry export, 2026-09-17): 'Unknown' 75.7%, 'Aliased Location' 16.2%, 'Home' 3.9%, 'Searched Address' 3.1%, 'Work' 1.1%."),
        ColumnSpec("latitude", "REAL", entity_hint="location", sensitive=True,
                   semantic_note="native, parsed from placeLocation's 'geo:lat,lon' string"),
        ColumnSpec("longitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("place_location_raw", "TEXT", sensitive=True,
                   semantic_note="native 'geo:<lat>,<lon>' string, kept verbatim alongside the parsed latitude/longitude"),
        ColumnSpec("hierarchy_level", "INTEGER",
                   semantic_note="native — only '0' (918 visits) and '1' (22 visits) observed in this export"),
        ColumnSpec("candidate_probability", "REAL",
                   semantic_note="native — Google's own confidence in this specific place guess (topCandidate.probability); never folded into any derived score"),
        ColumnSpec("segment_probability", "REAL", semantic_note="native — Google's own segment-level probability"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

MAPS_ACTIVITIES_TABLE = TableSpec(
    name="maps_activities",
    primary_key_column="activity_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="begin_timestamp",
    extra_indexed_columns=["activity_type"],
    columns=[
        ColumnSpec("activity_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                   semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("begin_timestamp", "TEXT", not_null=True,
                   semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("end_timestamp", "TEXT", not_null=True, semantic_note="native, ISO 8601 UTC"),
        ColumnSpec("duration_seconds", "REAL"),
        ColumnSpec("activity_type", "TEXT",
                   semantic_note="native transport mode, verbatim from Google. Real values (this export): 'in passenger vehicle' 63.5%, 'walking' 22.7%, 'cycling' 4.4%, 'in bus' 2.9%, 'in train' 2.8%, 'in subway' 2.5%, 'flying' 0.8%, 'in tram' 0.4%."),
        ColumnSpec("distance_meters", "REAL", semantic_note="native unit: meters, never silently converted"),
        ColumnSpec("start_latitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("start_longitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("start_location_raw", "TEXT", sensitive=True, semantic_note="native 'geo:<lat>,<lon>' string"),
        ColumnSpec("end_latitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("end_longitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("end_location_raw", "TEXT", sensitive=True, semantic_note="native 'geo:<lat>,<lon>' string"),
        ColumnSpec("candidate_probability", "REAL", semantic_note="native — Google's own confidence in this transport-mode guess"),
        ColumnSpec("segment_probability", "REAL", semantic_note="native — Google's own segment-level probability"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

MAPS_LABELED_PLACES_TABLE = TableSpec(
    name="maps_labeled_places",
    primary_key_column="labeled_place_id",
    dedup_key_column="label",
    canonical_timestamp_column=None,  # no time axis in the source — a small reference table
    columns=[
        ColumnSpec("labeled_place_id", "INTEGER"),
        ColumnSpec("label", "TEXT", not_null=True,
                   semantic_note="native — the project owner's own label in Google Maps, e.g. 'Home', 'Work', or a second home-like label such as 'Home AT'. Used directly as this table's dedup key (Google Maps allows only one place per label)."),
        ColumnSpec("address", "TEXT", semantic_note="native"),
        ColumnSpec("latitude", "REAL", entity_hint="location", sensitive=True,
                   semantic_note="native, parsed from GeoJSON [lon, lat] coordinates — see module docstring's GEO PARSING note"),
        ColumnSpec("longitude", "REAL", entity_hint="location", sensitive=True),
        ColumnSpec("source_file", "TEXT"),
    ],
)

for _table in (MAPS_VISITS_TABLE, MAPS_ACTIVITIES_TABLE, MAPS_LABELED_PLACES_TABLE):
    register_table_spec(_table)


# ============================================================================
# FILE DISCOVERY — case-insensitive (timelive.md §3: real PayPal .CSV bug)
# ============================================================================

def _find_timeline_files(base_input_dir: Path) -> List[Path]:
    """
    Timeline.json lands directly under MAPS_INPUT_DIR (not in a per-export
    subfolder like instagram/money), as "Timeline.json" or a datestamped
    re-export the project owner may keep alongside an older copy (e.g.
    "Timeline-2026-09.json"). Matched on the FILENAME only, case-
    insensitively, non-recursively — Input/Maps/Timeline/Settings.json is a
    different file ("Settings.json") and can never match this pattern by
    accident.
    """
    if not base_input_dir.exists():
        return []
    return sorted(
        p for p in base_input_dir.iterdir()
        if p.is_file() and p.name.lower().startswith("timeline") and p.name.lower().endswith(".json")
    )


def _load_timeline_entries(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "semanticSegments" in data:
        # rawSignals (if present) is also timelinePath-shaped and already
        # excluded by the timelinePath-skip decision — never read here.
        return list(data.get("semanticSegments") or [])
    raise ValueError(
        f"{path}: unrecognized Timeline export shape (expected a bare list or a dict "
        f"with 'semanticSegments') — the pre-2024 nested 'timelineObjects' format is "
        f"explicitly out of scope, see module docstring"
    )


def _find_labeled_places_file(base_input_dir: Path) -> Optional[Path]:
    """Fixed Takeout path: Maps/My labeled places/Labeled places.json.
    Matched case-insensitively at each path segment (timelive.md §3)."""
    if not base_input_dir.exists():
        return None
    for maps_dir in base_input_dir.iterdir():
        if not maps_dir.is_dir() or maps_dir.name.lower() != "maps":
            continue
        for sub in maps_dir.iterdir():
            if sub.is_dir() and sub.name.lower() == "my labeled places":
                for f in sub.iterdir():
                    if f.is_file() and f.name.lower() == "labeled places.json":
                        return f
    return None


# ============================================================================
# NORMALIZATION — record building
# ============================================================================

def build_visit_record(raw: Dict[str, Any], source_file: str) -> Optional[Dict[str, Any]]:
    visit = raw.get("visit") or {}
    top_candidate = visit.get("topCandidate") or {}

    begin_iso = to_iso_utc(raw.get("startTime"))
    end_iso = to_iso_utc(raw.get("endTime"))
    if not begin_iso or not end_iso:
        logger.warning("%s: visit entry with unparseable startTime/endTime, skipped", source_file)
        return None

    place_id = top_candidate.get("placeID") or None
    place_location_raw = top_candidate.get("placeLocation") or None
    latitude, longitude = parse_geo_string(place_location_raw)

    return {
        "dedup_key": "|".join(["visit", begin_iso, end_iso, place_id or ""]),
        "begin_timestamp": begin_iso,
        "end_timestamp": end_iso,
        "duration_seconds": _duration_seconds(begin_iso, end_iso),
        "place_id": place_id,
        "semantic_type": top_candidate.get("semanticType") or None,
        "latitude": latitude,
        "longitude": longitude,
        "place_location_raw": place_location_raw,
        "hierarchy_level": safe_int(visit.get("hierarchyLevel")),
        "candidate_probability": safe_float(top_candidate.get("probability")),
        "segment_probability": safe_float(visit.get("probability")),
        "source_file": source_file,
    }


def build_activity_record(raw: Dict[str, Any], source_file: str) -> Optional[Dict[str, Any]]:
    activity = raw.get("activity") or {}
    top_candidate = activity.get("topCandidate") or {}

    begin_iso = to_iso_utc(raw.get("startTime"))
    end_iso = to_iso_utc(raw.get("endTime"))
    if not begin_iso or not end_iso:
        logger.warning("%s: activity entry with unparseable startTime/endTime, skipped", source_file)
        return None

    activity_type = top_candidate.get("type") or None
    distance_meters = safe_float(activity.get("distanceMeters"))
    start_raw = activity.get("start") or None
    end_raw = activity.get("end") or None
    start_lat, start_lon = parse_geo_string(start_raw)
    end_lat, end_lon = parse_geo_string(end_raw)

    dedup_key = "|".join([
        "activity", begin_iso, end_iso, activity_type or "",
        "" if distance_meters is None else repr(distance_meters),
    ])

    return {
        "dedup_key": dedup_key,
        "begin_timestamp": begin_iso,
        "end_timestamp": end_iso,
        "duration_seconds": _duration_seconds(begin_iso, end_iso),
        "activity_type": activity_type,
        "distance_meters": distance_meters,
        "start_latitude": start_lat,
        "start_longitude": start_lon,
        "start_location_raw": start_raw,
        "end_latitude": end_lat,
        "end_longitude": end_lon,
        "end_location_raw": end_raw,
        "candidate_probability": safe_float(top_candidate.get("probability")),
        "segment_probability": safe_float(activity.get("probability")),
        "source_file": source_file,
    }


def parse_timeline_files(base_input_dir: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], int, int]:
    """Returns (visit_records, activity_records, skipped_timelinepath_entries,
    skipped_timelinepath_points)."""
    visits: List[Dict[str, Any]] = []
    activities: List[Dict[str, Any]] = []
    skipped_entries = 0
    skipped_points = 0

    for path in _find_timeline_files(base_input_dir):
        entries = _load_timeline_entries(path)
        for raw in entries:
            if "visit" in raw:
                record = build_visit_record(raw, path.name)
                if record:
                    visits.append(record)
            elif "activity" in raw:
                record = build_activity_record(raw, path.name)
                if record:
                    activities.append(record)
            elif "timelinePath" in raw:
                skipped_entries += 1
                skipped_points += len(raw.get("timelinePath") or [])
            else:
                logger.warning(
                    "%s: entry with none of visit/activity/timelinePath, skipped (keys: %s)",
                    path.name, sorted(raw.keys()),
                )

    return visits, activities, skipped_entries, skipped_points


def parse_labeled_places(base_input_dir: Path) -> List[Dict[str, Any]]:
    path = _find_labeled_places_file(base_input_dir)
    if path is None:
        logger.info("no 'Labeled places.json' found under %s — maps_labeled_places will be empty", base_input_dir)
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = []
    for feature in data.get("features") or []:
        props = feature.get("properties") or {}
        label = props.get("name") or None
        if not label:
            continue
        geometry = feature.get("geometry") or {}
        latitude, longitude = parse_geojson_point(geometry.get("coordinates"))
        records.append({
            "label": label,
            "address": props.get("address") or None,
            "latitude": latitude,
            "longitude": longitude,
            "source_file": path.name,
        })
    return records


# ============================================================================
# ENTRY POINT
# ============================================================================

def run_ingest(conn, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    for table in (MAPS_VISITS_TABLE, MAPS_ACTIVITIES_TABLE, MAPS_LABELED_PLACES_TABLE):
        create_schema_for_table(conn, table)

    visits, activities, skipped_tp_entries, skipped_tp_points = parse_timeline_files(MAPS_INPUT_DIR)
    labeled_places = parse_labeled_places(MAPS_INPUT_DIR)

    logger.info(
        "parsed: %d visit(s), %d activity(ies), %d labeled place(s); "
        "%d timelinePath entries skipped by design (%d raw GPS points — see module docstring)",
        len(visits), len(activities), len(labeled_places), skipped_tp_entries, skipped_tp_points,
    )

    rows_inserted = 0
    rows_already_present = 0
    tables_written: List[str] = []

    for table, records in (
        (MAPS_VISITS_TABLE, visits),
        (MAPS_ACTIVITIES_TABLE, activities),
        (MAPS_LABELED_PLACES_TABLE, labeled_places),
    ):
        if not records:
            continue
        outcomes: List[UpsertOutcome] = upsert_rows(conn, table, records)
        rows_inserted += sum(1 for o in outcomes if o.was_new)
        rows_already_present += sum(1 for o in outcomes if not o.was_new)
        tables_written.append(table.name)

    return IngestReport(
        domain="maps",
        tables_written=tables_written,
        rows_inserted=rows_inserted,
        rows_already_present=rows_already_present,
        dry_run=dry_run,
    )
