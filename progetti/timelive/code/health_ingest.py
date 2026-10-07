# health_ingest.py
# =============================================================================
# APPLE HEALTH INGEST — Personal Data Vault (Health/HealthKit domain)
# =============================================================================
#
# STANDARD COMPLIANCE (see timelive.md)
# -----------------------------------------------------------------------
# This is the v5 rewrite of health_ingest.py, built on top of the shared
# library in main.py (timelive.md, Part VI). What changed relative to the
# previous version:
#
#   * Three output files (dataset, full dataset, summary) -> now exactly
#     two (timelive.md §11): applehealth_dataset.json (PRIMARY) and
#     applehealth_dataset_full.json (FULL). No separate summary file.
#   * `_schema` and `_logic` blocks were entirely missing -> now generated
#     via main.build_schema / main.build_logic (timelive.md §31, §37),
#     alongside the existing `_metadata`.
#   * PRIMARY selection used an ad hoc `session_priority()` scoring
#     function and a hand-rolled multi-section budget loop -> now uses
#     main.compute_notability_scores (weighted-sum signals matching the
#     exact same point scale as before, so behavior is preserved) plus
#     main.select_within_size_budget for the actual ranking/bin-packing,
#     called once per priority section in the same documented order as
#     before (sessions > sleep > cardio > daily activity > other
#     aggregations > individual events).
#   * `activity_confidence` was a continuous, domain-specific float
#     (0.35–1.0) -> now `confidence_rate` on the single fixed standard
#     scale shared by every domain (timelive.md §27: 1.0/0.8/0.5/0.2). The
#     richer `activity_inference` method string (explicit_workout /
#     metric_pattern / intensity_pattern / generic_activity) is preserved
#     as supplementary detail, it just no longer doubles as the confidence
#     value itself.
#   * Session grouping now also carries an explicit confidence_rate
#     (CONFIDENCE_INFERRED_HIGH), matching the treatment money_ingest gives
#     its refund groupings and spotify_ingest gives its listening sessions:
#     grouping is deterministic given the configured thresholds, but it is
#     still an assumption about what constitutes one real-world session.
#   * Session detection (`detect_sessions` / `session_compatible`) stays
#     DOMAIN-SPECIFIC rather than using main.py's generic
#     `group_by_time_and_compatibility` — same exception as
#     money_ingest's refund pairing. The generic framework takes a single
#     fixed `max_gap_seconds`; health's compatibility rule needs a
#     variable gap depending on the pair of events involved (tighter for
#     sleep, extended for activity+cardio combinations), which the
#     compatibility callback alone cannot express since it never sees the
#     actual gap. timelive.md §29 explicitly allows this.
#   * Deduplication and common I/O/size-estimation now come from main.py
#     instead of local reimplementations.
#
# OUTPUT FILES
# -----------------------------------------------------------------------
#     applehealth_dataset.json        -> PRIMARY (LLM-oriented, budget-aware)
#     applehealth_dataset_full.json   -> FULL    (analytical, normalized)
#
# DESIGN GOAL (unchanged)
# ------------
# RAW Apple Health XML is converted into two useful layers:
#
#   FULL
#       Analytical/intermediate dataset. Keeps the information needed to
#       answer questions PRIMARY cannot answer directly: normalized
#       events, temporal aggregations, sessions and daily summaries.
#
#   PRIMARY
#       Small, LLM-oriented dataset. NOT a mechanically pruned copy of
#       FULL — built from the most useful sessions/summaries, bounded by
#       PRIMARY_MAX_SIZE_MB.
#
# IMPORTANT DESIGN RULES (unchanged)
# ----------------------
# 1. Timestamps are the source of temporal information; year/month/day/
#    hour/weekday are never duplicated per event (timelive.md §18).
# 2. source and device are always scalar strings, never lists
#    (timelive.md §20).
# 3. A session can combine multiple underlying events/sources/devices. The
#    session receives one canonical source and one canonical device,
#    chosen deterministically from the contributors.
# 4. Activity type is inferred at BALANCED confidence by default: explicit
#    Apple workout information wins; otherwise metrics + duration +
#    intensity can infer a type. Ambiguous activity stays generic rather
#    than being invented.
# 5. PRIMARY_MAX_SIZE_MB is a TARGET, not a hard limit (timelive.md §15).
# 6. FULL is intentionally richer than PRIMARY; stable full_ref
#    identifiers let an LLM retrieve the corresponding FULL object.
# =============================================================================

from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------------------------------------------------------
# SHARED LIBRARY (main.py) — see timelive.md Part VI
# ----------------------------------------------------------------------------
from main import (
    write_json,
    estimate_json_size_bytes,
    check_full_size_warning,
    confidence_rate,
    CONFIDENCE_NATIVE,
    CONFIDENCE_INFERRED_HIGH,
    CONFIDENCE_INFERRED_MEDIUM,
    CONFIDENCE_INFERRED_LOW,
    compute_notability_scores as shared_compute_notability_scores,
    recency_weight,
    select_within_size_budget,
    deduplicate_records as shared_deduplicate_records,
    build_metadata,
    build_schema,
    build_logic,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Paths (with fallback if a central config.py is not available)
# ----------------------------------------------------------------------------
# NOTE: config.json + config.py hybrid described in timelive.md §33 does not
# exist yet; this fallback keeps the script runnable on its own, matching
# money_ingest.py / spotify_ingest.py / main.py's own fallback pattern.
# Filenames follow the exact `<domain>_dataset.json` /
# `<domain>_dataset_full.json` pattern required by timelive.md §11 (the
# previous version used "applehealth_history_dataset.json" and produced a
# third summary file, both corrected here).
try:
    from config import (
        HEALTH_INPUT_DIR,
        HEALTH_INPUT_FILE,
        HEALTH_OUTPUT_DATASET_PATH,
        HEALTH_OUTPUT_FULL_DATASET_PATH,
    )
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    HEALTH_INPUT_DIR = BASE_DIR / "Input" / "Apple Health"
    HEALTH_INPUT_FILE = HEALTH_INPUT_DIR / "export.xml"
    OUTPUT_DIR = BASE_DIR / "Output"
    HEALTH_OUTPUT_DATASET_PATH = OUTPUT_DIR / "applehealth_dataset.json"
    HEALTH_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / "applehealth_dataset_full.json"

HEALTH_INPUT_DIR = Path(HEALTH_INPUT_DIR)
HEALTH_INPUT_FILE = Path(HEALTH_INPUT_FILE)
HEALTH_OUTPUT_DATASET_PATH = Path(HEALTH_OUTPUT_DATASET_PATH)
HEALTH_OUTPUT_FULL_DATASET_PATH = Path(HEALTH_OUTPUT_FULL_DATASET_PATH)

SOURCE_PREFIX = "health"
DATASET_VERSION = "5.0"  # standardized on the main.py shared library

FULL_WARNING_SIZE_GB = 0.5

# ---------------------------------------------------------------------------
# PRUNING
# ---------------------------------------------------------------------------
# none       = keep every field on every record, unfiltered.
# light      = keep more individual events in FULL and allow more detail.
# medium     = default; high-frequency data is strongly aggregated.
# aggressive = remove more low-value granular events from FULL.
#
# PRUNE_LEVEL affects what is retained per-record in FULL. PRIMARY has its
# own independent size-budget selection below (timelive.md §15).
# ---------------------------------------------------------------------------
PRUNE_LEVEL = "medium"
VALID_PRUNE_LEVELS = {"none", "light", "medium", "aggressive"}

# ---------------------------------------------------------------------------
# PRIMARY SIZE TARGET
# ---------------------------------------------------------------------------
PRIMARY_MAX_SIZE_MB = 25.0
PRIMARY_SOFT_OVERFLOW_RATIO = 0.10  # allow roughly 10% over target if useful

# ---------------------------------------------------------------------------
# TEMPORAL AGGREGATION
# ---------------------------------------------------------------------------
# 300 = 5-minute windows. 60 -> 1 minute, 900 -> 15 minutes, 3600 -> 1 hour.
# Smaller buckets preserve more temporal detail but increase FULL size.
# ---------------------------------------------------------------------------
TEMPORAL_BUCKET_SECONDS = 300

# ---------------------------------------------------------------------------
# SESSION DETECTION
# ---------------------------------------------------------------------------
# Two compatible events are normally joined when the gap between the end of
# the previous event and the beginning of the next is <= this value.
SESSION_MAX_GAP_SECONDS = 10 * 60

# Strongly related activity/cardio events may bridge a longer gap.
SESSION_EXTENDED_GAP_SECONDS = 20 * 60

# Prevents an unreasonably long event from accidentally swallowing
# unrelated periods into one session.
SESSION_MAX_DURATION_SECONDS = 6 * 60 * 60

# Session grouping is deterministic given the thresholds above, but it is
# still an assumption about what constitutes one real-world session (e.g.
# a workout could genuinely pause for 15 minutes and resume). It therefore
# carries confidence_rate = CONFIDENCE_INFERRED_HIGH on the fixed standard
# scale (timelive.md §27), the same treatment money_ingest and
# spotify_ingest give their deterministic-given-criteria groupings.
SESSION_GROUPING_CONFIDENCE = CONFIDENCE_INFERRED_HIGH

# ---------------------------------------------------------------------------
# ACTIVITY INFERENCE
# ---------------------------------------------------------------------------
# balanced = explicit workout/activity metadata first, then metric pattern,
# duration and intensity. Ambiguous cases stay generic.
ACTIVITY_INFERENCE_LEVEL = "balanced"
VALID_ACTIVITY_INFERENCE_LEVELS = {"none", "conservative", "balanced", "aggressive"}

# ---------------------------------------------------------------------------
# GRANULAR / ACTIVITY METRICS
# ---------------------------------------------------------------------------
HIGH_FREQUENCY_METRICS = {
    "heart_rate",
    "resting_heart_rate",
    "walking_heart_rate_average",
    "heart_rate_variability",
    "steps",
}

ACTIVITY_METRICS = {
    "steps",
    "distance_walking_running",
    "distance_cycling",
    "distance_swimming",
    "active_energy",
    "exercise_time",
    "move_time",
    "stand_time",
    "flights_climbed",
}

# ---------------------------------------------------------------------------
# NOTABILITY WEIGHTS — sessions (timelive.md §16, §33)
# ---------------------------------------------------------------------------
# These weights reproduce the exact point scale of the previous ad hoc
# session_priority() function, now expressed as signals (0..1, or 0/1 for
# boolean-like signals) fed into main.compute_notability_scores. Reproducing
# the same scale means PRIMARY session selection behaves the same as
# before, while now going through the shared, documented mechanism.
NOTABILITY_WEIGHT_ACTIVITY_SPECIFICITY = 100.0  # not a generic/"physical_activity" label
NOTABILITY_WEIGHT_SLEEP = 90.0
NOTABILITY_WEIGHT_SPECIFIC_EXERCISE = 40.0      # running/cycling/swimming/hiking/strength/cardio
NOTABILITY_WEIGHT_HR_AVAILABLE = 25.0           # heart_rate_mode is continuous/sampled/resting
NOTABILITY_WEIGHT_DURATION = 30.0               # scaled by min(duration_minutes, 120) / 120
NOTABILITY_WEIGHT_EVENT_COUNT = 20.0            # scaled by min(event_count, 1000) / 1000
NOTABILITY_WEIGHT_HIGH_CONFIDENCE = 15.0        # confidence_rate >= CONFIDENCE_INFERRED_HIGH

# ---------------------------------------------------------------------------
# NOTABILITY WEIGHTS — aggregations / daily activity / individual events
# ---------------------------------------------------------------------------
# Cardio (heart rate) temporal aggregations are always ranked purely by
# recency (they are generically useful for "how was my heart rate lately"
# questions regardless of sample count). Other aggregations combine sample
# density with recency; daily activity and individual events are ranked by
# recency alone, replacing the previous fixed "last 500 records" slice with
# a proper budget-aware ranking.
AGGREGATION_WEIGHT_SAMPLES = 0.7
AGGREGATION_WEIGHT_RECENCY = 0.3
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 30  # health status/trends are time-sensitive


# ============================================================================
# HEALTHKIT SEMANTIC MAP
# ============================================================================
# This map is deliberately kept explicit for known Apple Health identifiers.
# Unknown identifiers still pass through infer_metric() and receive a
# generic fallback instead of being silently discarded.
# ============================================================================

SEMANTIC_TYPE_MAP = {
    "HKQuantityTypeIdentifierStepCount": ("activity", "steps", "count"),
    "HKQuantityTypeIdentifierDistanceWalkingRunning": ("activity", "distance_walking_running", "distance"),
    "HKQuantityTypeIdentifierDistanceCycling": ("activity", "distance_cycling", "distance"),
    "HKQuantityTypeIdentifierDistanceSwimming": ("activity", "distance_swimming", "distance"),
    "HKQuantityTypeIdentifierFlightsClimbed": ("activity", "flights_climbed", "count"),
    "HKQuantityTypeIdentifierActiveEnergyBurned": ("activity", "active_energy", "energy"),
    "HKQuantityTypeIdentifierBasalEnergyBurned": ("activity", "basal_energy", "energy"),
    "HKQuantityTypeIdentifierAppleExerciseTime": ("activity", "exercise_time", "duration"),
    "HKQuantityTypeIdentifierAppleStandTime": ("activity", "stand_time", "duration"),
    "HKQuantityTypeIdentifierAppleMoveTime": ("activity", "move_time", "duration"),
    "HKQuantityTypeIdentifierHeartRate": ("cardiovascular", "heart_rate", "heart_rate"),
    "HKQuantityTypeIdentifierRestingHeartRate": ("cardiovascular", "resting_heart_rate", "heart_rate"),
    "HKQuantityTypeIdentifierWalkingHeartRateAverage": ("cardiovascular", "walking_heart_rate_average", "heart_rate"),
    "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": ("cardiovascular", "heart_rate_variability", "time"),
    "HKQuantityTypeIdentifierOxygenSaturation": ("cardiovascular", "oxygen_saturation", "percentage"),
    "HKQuantityTypeIdentifierBloodPressureSystolic": ("cardiovascular", "blood_pressure_systolic", "pressure"),
    "HKQuantityTypeIdentifierBloodPressureDiastolic": ("cardiovascular", "blood_pressure_diastolic", "pressure"),
    "HKQuantityTypeIdentifierRespiratoryRate": ("respiratory", "respiratory_rate", "rate"),
    "HKQuantityTypeIdentifierForcedVitalCapacity": ("respiratory", "forced_vital_capacity", "volume"),
    "HKQuantityTypeIdentifierForcedExpiratoryVolume1": ("respiratory", "forced_expiratory_volume", "volume"),
    "HKQuantityTypeIdentifierBodyMass": ("body", "body_mass", "mass"),
    "HKQuantityTypeIdentifierHeight": ("body", "height", "length"),
    "HKQuantityTypeIdentifierBodyMassIndex": ("body", "body_mass_index", "index"),
    "HKQuantityTypeIdentifierBodyFatPercentage": ("body", "body_fat_percentage", "percentage"),
    "HKQuantityTypeIdentifierBodyTemperature": ("temperature", "body_temperature", "temperature"),
    "HKQuantityTypeIdentifierAppleSleepingWristTemperature": ("temperature", "sleeping_wrist_temperature", "temperature"),
    "HKQuantityTypeIdentifierDietaryEnergyConsumed": ("nutrition", "dietary_energy", "energy"),
    "HKQuantityTypeIdentifierDietaryProtein": ("nutrition", "dietary_protein", "mass"),
    "HKQuantityTypeIdentifierDietaryCarbohydrates": ("nutrition", "dietary_carbohydrates", "mass"),
    "HKQuantityTypeIdentifierDietaryFatTotal": ("nutrition", "dietary_fat", "mass"),
    "HKQuantityTypeIdentifierDietaryWater": ("nutrition", "dietary_water", "volume"),
    "HKCategoryTypeIdentifierSleepAnalysis": ("sleep", "sleep_analysis", "sleep"),
    "HKCategoryTypeIdentifierMindfulSession": ("mindfulness", "mindful_session", "duration"),
    "HKCategoryTypeIdentifierMenstrualFlow": ("reproductive", "menstrual_flow", "category"),
    "HKQuantityTypeIdentifierHeadphoneAudioExposure": ("environment", "headphone_audio_exposure", "sound"),
    "HKQuantityTypeIdentifierEnvironmentalAudioExposure": ("environment", "environmental_audio_exposure", "sound"),
}


# ============================================================================
# BASIC HELPERS
# ============================================================================

def normalize_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def parse_date(value: Any) -> Optional[datetime]:
    value = normalize_string(value)
    if not value:
        return None
    candidates = [value, value.replace("Z", "+00:00"), value.replace(" +", "+")]
    for candidate in candidates:
        try:
            dt_value = datetime.fromisoformat(candidate)
            if dt_value.tzinfo is None:
                dt_value = dt_value.replace(tzinfo=timezone.utc)
            return dt_value.astimezone(timezone.utc)
        except ValueError:
            pass
    for fmt in (
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f %z",
        "%Y-%m-%dT%H:%M:%S%z",
    ):
        try:
            dt_value = datetime.strptime(value, fmt)
            if dt_value.tzinfo is None:
                dt_value = dt_value.replace(tzinfo=timezone.utc)
            return dt_value.astimezone(timezone.utc)
        except ValueError:
            pass
    return None


def to_iso_utc(dt_value: Optional[datetime]) -> Optional[str]:
    if dt_value is None:
        return None
    if dt_value.tzinfo is None:
        dt_value = dt_value.replace(tzinfo=timezone.utc)
    return dt_value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_identifier(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return re.sub(r"_+", "_", value).strip("_")


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively drops None values and empty nested dicts/lists. Used
    throughout this file to keep output objects free of clutter without
    every builder function having to check each field individually.
    """
    output: Dict[str, Any] = {}
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, dict):
            nested = clean_dict(value)
            if nested:
                output[key] = nested
        elif isinstance(value, list):
            nested = [clean_dict(x) if isinstance(x, dict) else x for x in value if x is not None]
            nested = [x for x in nested if x != {}]
            if nested:
                output[key] = nested
        else:
            output[key] = value
    return output


def parse_device_string(device_string: Optional[str]) -> Dict[str, Any]:
    if not device_string:
        return {}
    text = str(device_string)
    patterns = {
        "device_name": r"name:([^,>]+)",
        "device_manufacturer": r"manufacturer:([^,>]+)",
        "device_model": r"model:([^,>]+)",
        "device_hardware_version": r"hardwareVersion:([^,>]+)",
        "device_firmware_version": r"firmwareVersion:([^,>]+)",
        "device_software_version": r"softwareVersion:([^,>]+)",
        "device_local_identifier": r"localIdentifier:([^,>]+)",
        "device_udid_identifier": r"UDIDeviceIdentifier:([^,>]+)",
    }
    result = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            value = normalize_string(match.group(1))
            if value:
                result[field] = value
    return result


def normalize_source_type(source_name: Optional[str], device_name: Optional[str], device_manufacturer: Optional[str]) -> str:
    text = " ".join(x for x in (source_name, device_name, device_manufacturer) if x).lower()
    for provider in ("polar", "garmin", "fitbit", "whoop", "oura", "apple", "withings", "suunto", "coros"):
        if provider in text:
            return provider
    return normalize_identifier(source_name) or "unknown"


def infer_metric(health_type: Optional[str], unit: Optional[str]) -> Dict[str, Optional[str]]:
    if health_type in SEMANTIC_TYPE_MAP:
        category, metric, value_type = SEMANTIC_TYPE_MAP[health_type]
        return {"category": category, "metric": metric, "value_type": value_type}
    normalized = normalize_identifier(health_type)
    if not normalized:
        return {"category": None, "metric": None, "value_type": None}
    if "sleep" in normalized:
        category = "sleep"
    elif any(x in normalized for x in ("heart", "blood_pressure", "oxygen", "cardio")):
        category = "cardiovascular"
    elif any(x in normalized for x in ("distance", "step", "energy", "exercise", "stand", "move", "flight", "activity")):
        category = "activity"
    elif any(x in normalized for x in ("body", "weight", "height", "mass")):
        category = "body"
    elif any(x in normalized for x in ("dietary", "nutrition")):
        category = "nutrition"
    elif "temperature" in normalized:
        category = "temperature"
    elif any(x in normalized for x in ("mindful", "meditation")):
        category = "mindfulness"
    else:
        category = "other"
    return {"category": category, "metric": normalized, "value_type": unit or "unknown"}


def normalize_unit(health_type: Optional[str], unit: Optional[str]) -> Optional[str]:
    fixed = {
        "HKQuantityTypeIdentifierStepCount": "count",
        "HKQuantityTypeIdentifierHeartRate": "count/min",
        "HKQuantityTypeIdentifierRestingHeartRate": "count/min",
        "HKQuantityTypeIdentifierWalkingHeartRateAverage": "count/min",
        "HKQuantityTypeIdentifierHeartRateVariabilitySDNN": "ms",
        "HKQuantityTypeIdentifierDistanceWalkingRunning": "m",
        "HKQuantityTypeIdentifierDistanceCycling": "m",
        "HKQuantityTypeIdentifierDistanceSwimming": "m",
        "HKQuantityTypeIdentifierBodyMass": "kg",
        "HKQuantityTypeIdentifierHeight": "m",
        "HKQuantityTypeIdentifierOxygenSaturation": "%",
        "HKQuantityTypeIdentifierBodyFatPercentage": "%",
    }
    return fixed.get(health_type, normalize_string(unit))


def get_xml_attribute(element: ET.Element, *names: str) -> Optional[str]:
    for name in names:
        value = element.attrib.get(name)
        if value is not None:
            return normalize_string(value)
    return None


# ============================================================================
# RECORD PARSING
# ============================================================================
# The normalized event schema is intentionally compact. Fields such as
# year/month/day/hour/source_file are removed because they duplicate
# timestamp or file-level metadata and make cross-dataset interoperability
# harder (timelive.md §18).
# ============================================================================

def parse_record_element(rec_el: ET.Element, record_index: int) -> Optional[Dict[str, Any]]:
    health_type = get_xml_attribute(rec_el, "type")
    if not health_type:
        return None

    begin_dt = parse_date(get_xml_attribute(rec_el, "startDate", "date"))
    end_dt = parse_date(get_xml_attribute(rec_el, "endDate"))
    creation_dt = parse_date(get_xml_attribute(rec_el, "creationDate"))
    if not begin_dt:
        return None

    value = safe_float(get_xml_attribute(rec_el, "value"))
    if value is not None and value.is_integer():
        value = int(value)

    unit = normalize_unit(health_type, get_xml_attribute(rec_el, "unit"))
    semantic = infer_metric(health_type, unit)
    source = get_xml_attribute(rec_el, "sourceName") or "unknown"
    source_version = get_xml_attribute(rec_el, "sourceVersion")
    device_info = parse_device_string(get_xml_attribute(rec_el, "device", "Device"))
    device = device_info.get("device_name") or "unknown"
    source_type = normalize_source_type(source, device, device_info.get("device_manufacturer"))

    duration = None
    if end_dt:
        duration = (end_dt - begin_dt).total_seconds()
        if duration < 0:
            duration = None
        elif duration.is_integer():
            duration = int(duration)

    return clean_dict({
        "event_number": None,
        "begin_timestamp": to_iso_utc(begin_dt),
        "end_timestamp": to_iso_utc(end_dt) or to_iso_utc(begin_dt),
        "duration_seconds": duration,
        "metric": semantic["metric"],
        "category": semantic["category"],
        "value_type": semantic["value_type"],
        "value": value,
        "unit": unit,
        "source": source,
        "source_type": source_type,
        "device": device,
        "device_model": device_info.get("device_model"),
        "device_manufacturer": device_info.get("device_manufacturer"),
        "source_version": source_version,
        "creation_timestamp": to_iso_utc(creation_dt),
        "record_index_in_source": record_index,
    })


def parse_workout_element(workout_el: ET.Element, workout_index: int) -> Optional[Dict[str, Any]]:
    """
    Parses an Apple Health <Workout> as explicit activity metadata. Apple
    exports can contain an explicit workout type, duration, distance and
    energy — stronger evidence for activity classification than inferring
    running/cycling/etc. only from heart rate or steps.
    """
    start = parse_date(get_xml_attribute(workout_el, "startDate"))
    end = parse_date(get_xml_attribute(workout_el, "endDate"))
    if not start:
        return None

    workout_type = get_xml_attribute(workout_el, "workoutActivityType")
    source = get_xml_attribute(workout_el, "sourceName") or "unknown"
    device_info = parse_device_string(get_xml_attribute(workout_el, "device", "Device"))
    device = device_info.get("device_name") or "unknown"
    duration = safe_float(get_xml_attribute(workout_el, "duration"))
    distance = safe_float(get_xml_attribute(workout_el, "totalDistance"))
    energy = safe_float(get_xml_attribute(workout_el, "totalEnergyBurned"))
    distance_unit = normalize_string(get_xml_attribute(workout_el, "totalDistanceUnit"))
    energy_unit = normalize_string(get_xml_attribute(workout_el, "totalEnergyBurnedUnit"))

    return clean_dict({
        "workout_id": f"workout_{workout_index}",
        "begin_timestamp": to_iso_utc(start),
        "end_timestamp": to_iso_utc(end) or to_iso_utc(start),
        "duration_seconds": int(duration * 60) if duration is not None else ((end - start).total_seconds() if end else 0),
        "activity_type_raw": normalize_identifier(workout_type) or "workout",
        "source": source,
        "source_type": normalize_source_type(source, device, device_info.get("device_manufacturer")),
        "device": device,
        "device_model": device_info.get("device_model"),
        "distance": distance,
        "distance_unit": distance_unit,
        "energy": energy,
        "energy_unit": energy_unit,
    })


# ============================================================================
# DEDUPLICATION (timelive.md §25, delegated to main.py)
# ============================================================================
# No native per-record id exists in Apple Health XML, so deduplication
# always uses a composite key (same pattern as spotify_ingest).

def _composite_dedup_key(record: Dict[str, Any]) -> Tuple[Any, ...]:
    return (
        record.get("metric"), record.get("begin_timestamp"),
        record.get("end_timestamp"), record.get("value"), record.get("unit"),
        record.get("source"), record.get("device"),
    )


def deduplicate_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    return shared_deduplicate_records(
        records,
        native_id_field=None,
        composite_key_fn=_composite_dedup_key,
    )


def sort_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(records, key=lambda r: (r.get("begin_timestamp") or "", r.get("end_timestamp") or ""))


def assign_event_numbers(records: List[Dict[str, Any]]) -> None:
    for i, record in enumerate(records, start=1):
        record["event_number"] = f"{SOURCE_PREFIX}_{i}"


def dt(value: Optional[str]) -> Optional[datetime]:
    return parse_date(value)


def bucket_start(timestamp: str, bucket_seconds: int) -> str:
    current = dt(timestamp)
    if not current:
        return timestamp
    epoch = int(current.timestamp())
    bucket = epoch - (epoch % bucket_seconds)
    return to_iso_utc(datetime.fromtimestamp(bucket, tz=timezone.utc)) or timestamp


# ============================================================================
# TEMPORAL AGGREGATIONS
# ============================================================================
# Aggregations are intentionally grouped by metric + source + device. This
# prevents values from different sensors being silently averaged together.
# Sessions later combine semantically compatible events across sources.
# ============================================================================

def aggregate_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str, Optional[str], Optional[str]], List[Dict[str, Any]]] = defaultdict(list)
    for record in records:
        metric = record.get("metric")
        if not metric or not record.get("begin_timestamp"):
            continue
        key = (
            bucket_start(record["begin_timestamp"], TEMPORAL_BUCKET_SECONDS),
            metric,
            record.get("source"),
            record.get("device"),
        )
        groups[key].append(record)

    output = []
    for i, (key, items) in enumerate(sorted(groups.items()), start=1):
        bucket, metric, source, device = key
        numeric = [x["value"] for x in items if isinstance(x.get("value"), (int, float))]
        begins = [x["begin_timestamp"] for x in items if x.get("begin_timestamp")]
        ends = [x["end_timestamp"] for x in items if x.get("end_timestamp")]
        category = items[0].get("category")
        unit = items[0].get("unit")

        agg = {
            "aggregation_id": f"agg_{i}",
            "aggregation_type": "temporal_bucket",
            "metric": metric,
            "category": category,
            "begin_timestamp": min(begins) if begins else bucket,
            "end_timestamp": max(ends) if ends else bucket,
            "source": source,
            "device": device,
            "samples": len(items),
            "event_numbers": [x["event_number"] for x in items if x.get("event_number")],
        }
        if unit:
            agg["unit"] = unit
        if numeric:
            agg.update({
                "sum": round(sum(numeric), 6),
                "average": round(sum(numeric) / len(numeric), 6),
                "min": min(numeric),
                "max": max(numeric),
            })
        output.append(clean_dict(agg))
    return output


def build_daily_activity(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    days: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for r in records:
        timestamp = r.get("begin_timestamp")
        if timestamp:
            day = timestamp[:10]
            if r.get("metric") in ACTIVITY_METRICS or r.get("category") in {"activity", "cardiovascular", "sleep"}:
                days[day].append(r)

    output = []
    for day in sorted(days):
        items = days[day]
        by_metric: Dict[str, float] = defaultdict(float)
        hr = []
        for r in items:
            value = r.get("value")
            if isinstance(value, (int, float)):
                by_metric[r.get("metric")] += value
                if r.get("metric") == "heart_rate":
                    hr.append(value)
        start = f"{day}T00:00:00Z"
        end = f"{day}T23:59:59Z"
        summary = {
            "summary_id": f"day_{day}",
            "begin_timestamp": start,
            "end_timestamp": end,
            "metrics": {},
            "event_count": len(items),
        }
        for metric in ACTIVITY_METRICS:
            if metric in by_metric:
                summary["metrics"][metric] = round(by_metric[metric], 6)
        if hr:
            summary["heart_rate"] = {
                "average": round(sum(hr) / len(hr), 2),
                "min": min(hr),
                "max": max(hr),
                "samples": len(hr),
            }
        output.append(clean_dict(summary))
    return output


# ============================================================================
# ACTIVITY TYPE INFERENCE (+ confidence_rate on the fixed standard scale)
# ============================================================================

def normalize_workout_activity(raw: Optional[str]) -> str:
    if not raw:
        return "physical_activity"
    text = raw.lower()
    replacements = {
        "running": "running", "run": "running",
        "walking": "walking", "walk": "walking",
        "cycling": "cycling", "cycle": "cycling",
        "swimming": "swimming", "swim": "swimming",
        "hiking": "hiking", "hike": "hiking",
        "functional_strength_training": "strength_training",
        "traditional_strength_training": "strength_training",
        "strength_training": "strength_training",
        "yoga": "yoga", "dance": "dance",
        "elliptical": "elliptical", "rowing": "rowing",
    }
    for key, label in replacements.items():
        if key in text:
            return label
    return "physical_activity"


def infer_activity_type(items: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> Tuple[str, Optional[float], str]:
    """
    Returns (activity_type, confidence_rate, inference_method).

    confidence_rate is on the fixed standard scale (timelive.md §27), not
    the previous continuous 0.35–1.0 scale: an explicit Apple Workout tag
    is genuinely native source data (CONFIDENCE_NATIVE); a strong metric
    pattern (cycling/swimming, unambiguous distance metric) is
    CONFIDENCE_INFERRED_HIGH; a weaker pattern (walking vs running cannot
    be distinguished, or steps-only) or an intensity-based guess is
    CONFIDENCE_INFERRED_MEDIUM; a bare fallback with only distance-like
    evidence, or no real evidence at all, is CONFIDENCE_INFERRED_LOW.
    inference_method is kept as supplementary detail explaining *why*,
    since collapsing several distinct original signals onto the same
    standard confidence band would otherwise lose that information.

    BUG FIX vs the previous version: sleep was never actually classified
    as activity_type "sleep" here, even though the rest of the file (the
    sleep_sessions filter in build_primary_dataset, the old
    session_priority's sleep bonus) assumed it could be. A session whose
    events are predominantly HKCategoryTypeIdentifierSleepAnalysis records
    (category == "sleep") is now explicitly recognized — this is a native,
    unambiguous structural signal (Apple's own category says "sleep"), so
    it gets CONFIDENCE_NATIVE, checked even before explicit workouts since
    Apple never tags a workout on top of a sleep record.
    """
    sleep_items = sum(1 for x in items if x.get("category") == "sleep")
    if items and sleep_items / len(items) > 0.5:
        return "sleep", confidence_rate(CONFIDENCE_NATIVE), "explicit_category"

    # Explicit Workout metadata is the strongest remaining evidence: native source data.
    if workouts:
        types = [normalize_workout_activity(w.get("activity_type_raw")) for w in workouts]
        if types:
            counts = Counter(types)
            activity = counts.most_common(1)[0][0]
            return activity, confidence_rate(CONFIDENCE_NATIVE), "explicit_workout"

    metrics = Counter(x.get("metric") for x in items)
    duration = max((x.get("duration_seconds") or 0) for x in items)
    total_distance = sum(
        float(x.get("value")) for x in items
        if x.get("metric") in {"distance_walking_running", "distance_cycling", "distance_swimming"}
        and isinstance(x.get("value"), (int, float))
    )
    hr_values = [x.get("value") for x in items if x.get("metric") == "heart_rate" and isinstance(x.get("value"), (int, float))]
    avg_hr = sum(hr_values) / len(hr_values) if hr_values else None

    if metrics["distance_cycling"] > 0:
        return "cycling", confidence_rate(CONFIDENCE_INFERRED_HIGH), "metric_pattern"
    if metrics["distance_swimming"] > 0:
        return "swimming", confidence_rate(CONFIDENCE_INFERRED_HIGH), "metric_pattern"
    if metrics["distance_walking_running"] > 0:
        # Without explicit workout metadata we cannot reliably distinguish
        # walk from run. balanced mode therefore uses a generic label.
        return "walking_running", confidence_rate(CONFIDENCE_INFERRED_MEDIUM), "metric_pattern"

    if metrics["steps"] > 0 and (avg_hr is not None or duration >= 20 * 60):
        return "walking_or_general_activity", confidence_rate(CONFIDENCE_INFERRED_MEDIUM), "metric_pattern"

    if metrics["heart_rate"] > 0 and avg_hr is not None and avg_hr >= 120 and duration >= 15 * 60:
        return "cardio_activity", confidence_rate(CONFIDENCE_INFERRED_MEDIUM), "intensity_pattern"

    if total_distance > 0:
        return "physical_activity", confidence_rate(CONFIDENCE_INFERRED_LOW), "generic_activity"

    return "physical_activity", confidence_rate(CONFIDENCE_INFERRED_LOW), "generic_activity"


# ============================================================================
# SESSION COMPATIBILITY + DETECTION
# ============================================================================
# A session is NOT defined by identical source/device — it is a
# semantic/time cluster. This matters for Apple Health because one real
# workout may have HR from a Polar strap, steps from an iPhone/Watch, and
# energy from Apple itself.
#
# This stays DOMAIN-SPECIFIC rather than using main.py's generic
# group_by_time_and_compatibility: the compatibility rule below needs a
# variable gap threshold depending on which pair of events is being
# compared (tight for sleep, extended for activity+cardio combinations),
# but the generic framework's compatibility callback never receives the
# actual gap value — it can only accept/reject a pair, with the gap
# threshold fixed once for the whole call. timelive.md §29 explicitly
# allows a domain to layer its own logic on top when the generic shape
# cannot express it (see also money_ingest's refund-pairing exception).
# ============================================================================

def category_compatible(a: str, b: str) -> bool:
    if a == b:
        return True
    compatible_pairs = {
        frozenset({"activity", "cardiovascular"}),
        frozenset({"activity", "sleep"}),  # only useful when timestamps really overlap
    }
    return frozenset({a, b}) in compatible_pairs


def session_compatible(previous: Dict[str, Any], current: Dict[str, Any], current_start: datetime) -> bool:
    prev_end = dt(previous.get("end_timestamp")) or dt(previous.get("begin_timestamp"))
    cur_start = current_start
    if not prev_end:
        return False
    gap = (cur_start - prev_end).total_seconds()
    if gap < 0:
        gap = 0
    if gap > SESSION_EXTENDED_GAP_SECONDS:
        return False

    ca, cb = previous.get("category"), current.get("category")
    ma, mb = previous.get("metric"), current.get("metric")

    if ca == "sleep" or cb == "sleep":
        return ca == cb and gap <= SESSION_MAX_GAP_SECONDS

    if not category_compatible(ca or "other", cb or "other"):
        return False

    same_metric = ma and mb and ma == mb
    activity_cardio = {ca, cb} == {"activity", "cardiovascular"}
    same_source = previous.get("source") == current.get("source")

    if gap <= SESSION_MAX_GAP_SECONDS and (same_metric or activity_cardio or same_source):
        return True
    if gap <= SESSION_EXTENDED_GAP_SECONDS and activity_cardio:
        return True
    return False


def detect_sessions(records: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not records:
        return []

    records_sorted = sorted(records, key=lambda r: r.get("begin_timestamp") or "")
    sessions_raw = []
    current: List[Dict[str, Any]] = []
    current_start = None
    current_end = None

    for record in records_sorted:
        start = dt(record.get("begin_timestamp"))
        end = dt(record.get("end_timestamp")) or start
        if not start:
            continue

        if not current:
            current = [record]
            current_start = start
            current_end = end
            continue

        candidate_ok = session_compatible(current[-1], record, start)
        candidate_duration = (end - current_start).total_seconds() if current_start else 0
        if candidate_ok and candidate_duration <= SESSION_MAX_DURATION_SECONDS:
            current.append(record)
            current_end = max(current_end or end, end)
        else:
            sessions_raw.append(current)
            current = [record]
            current_start = start
            current_end = end

    if current:
        sessions_raw.append(current)

    output = []
    for index, items in enumerate(sessions_raw, start=1):
        begin = min(x["begin_timestamp"] for x in items if x.get("begin_timestamp"))
        end = max(x["end_timestamp"] for x in items if x.get("end_timestamp"))
        begin_dt, end_dt = dt(begin), dt(end)
        if not begin_dt or not end_dt:
            continue
        related_workouts = []
        for workout in workouts:
            ws, we = dt(workout.get("begin_timestamp")), dt(workout.get("end_timestamp"))
            if not ws:
                continue
            we = we or ws
            # Overlap or <= 5 minutes distance means the workout is likely
            # the explicit activity descriptor for this event cluster.
            before = (begin_dt - we).total_seconds()
            after = (ws - end_dt).total_seconds()
            if before <= 5 * 60 and after <= 5 * 60:
                related_workouts.append(workout)

        output.append(build_session(index, items, related_workouts))
    return output


# ============================================================================
# SESSION BUILDER
# ============================================================================

def canonical_contributor(items: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Chooses ONE source and ONE device for interoperability. Contributors
    are scored by number of events, then by metric richness. This
    deliberately avoids arrays in source/device (timelive.md §20) while
    still producing a deterministic representative identity for the
    combined session.
    """
    score: Dict[Tuple[str, str], float] = defaultdict(float)
    for item in items:
        key = (item.get("source") or "unknown", item.get("device") or "unknown")
        score[key] += 1
        if item.get("metric") in {"heart_rate", "steps", "active_energy", "distance_walking_running", "distance_cycling", "distance_swimming"}:
            score[key] += 0.5
    if not score:
        return "unknown", "unknown"
    source, device = max(score, key=score.get)
    return source, device


def build_session(index: int, items: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> Dict[str, Any]:
    begin = min(x["begin_timestamp"] for x in items if x.get("begin_timestamp"))
    end = max(x["end_timestamp"] for x in items if x.get("end_timestamp"))
    begin_dt, end_dt = dt(begin), dt(end)
    duration = int((end_dt - begin_dt).total_seconds()) if begin_dt and end_dt else None

    activity_type, activity_confidence, inference_method = infer_activity_type(items, workouts)
    source, device = canonical_contributor(items)
    metrics: Dict[str, List[float]] = defaultdict(list)
    units: Dict[str, str] = {}
    for item in items:
        metric = item.get("metric")
        value = item.get("value")
        if metric:
            if isinstance(value, (int, float)):
                metrics[metric].append(value)
            if item.get("unit"):
                units[metric] = item["unit"]

    summary = {}
    for metric, values in metrics.items():
        if metric in {"heart_rate", "resting_heart_rate", "walking_heart_rate_average", "heart_rate_variability"}:
            summary[metric] = {
                "average": round(sum(values) / len(values), 2),
                "min": min(values),
                "max": max(values),
                "samples": len(values),
            }
        elif metric in ACTIVITY_METRICS:
            summary[metric] = {"total": round(sum(values), 6), "unit": units.get(metric), "samples": len(values)}
        else:
            summary[metric] = {"average": round(sum(values) / len(values), 6), "min": min(values), "max": max(values), "samples": len(values)}

    hr = metrics.get("heart_rate", [])
    if metrics.get("resting_heart_rate") and not hr:
        hr_mode = "resting"
    elif hr:
        hr_mode = "continuous" if len(hr) >= 10 else "sampled"
    else:
        hr_mode = "not_available"

    # Energy is kept as a numeric summary plus the unit actually present in
    # the source, avoiding an assumption of kcal when Apple exported
    # another unit.
    energy_unit = units.get("active_energy")

    return clean_dict({
        "session_id": f"session_{index}",
        "begin_timestamp": begin,
        "end_timestamp": end,
        "duration_seconds": duration,
        "activity_type": activity_type,
        "confidence_rate": activity_confidence,
        "activity_inference_method": inference_method,
        "grouping_confidence_rate": confidence_rate(SESSION_GROUPING_CONFIDENCE),
        "source": source,
        "device": device,
        "heart_rate_mode": hr_mode,
        "energy_unit": energy_unit,
        "event_count": len(items),
        "metrics": summary,
        "workout_count": len(workouts),
        "event_numbers": [x.get("event_number") for x in items if x.get("event_number")],
    })


# ============================================================================
# NOTABILITY SCORE — domain signals feeding the shared engine (main.py)
# ============================================================================
# These reproduce the previous ad hoc session_priority() point scale
# exactly, expressed as weighted signals for main.compute_notability_scores
# (timelive.md §16, §37), so PRIMARY session selection behaves the same as
# before while going through the shared, documented mechanism.

def _session_activity_specificity_signal(session: Dict[str, Any]) -> float:
    activity = session.get("activity_type", "physical_activity")
    return 0.0 if activity in {"physical_activity", "walking_or_general_activity"} else 1.0


def _session_sleep_signal(session: Dict[str, Any]) -> float:
    return 1.0 if session.get("activity_type") == "sleep" else 0.0


def _session_specific_exercise_signal(session: Dict[str, Any]) -> float:
    activity = session.get("activity_type")
    return 1.0 if activity in {"running", "cycling", "swimming", "hiking", "strength_training", "cardio_activity"} else 0.0


def _session_hr_available_signal(session: Dict[str, Any]) -> float:
    return 1.0 if session.get("heart_rate_mode") in {"continuous", "sampled", "resting"} else 0.0


def _session_duration_signal(session: Dict[str, Any]) -> float:
    duration_minutes = (session.get("duration_seconds") or 0) / 60.0
    return min(duration_minutes, 120.0) / 120.0


def _session_event_count_signal(session: Dict[str, Any]) -> float:
    return min(session.get("event_count", 0), 1000) / 1000.0


def _session_high_confidence_signal(session: Dict[str, Any]) -> float:
    return 1.0 if (session.get("confidence_rate") or 0) >= CONFIDENCE_INFERRED_HIGH else 0.0


def compute_session_notability_scores(sessions: List[Dict[str, Any]]) -> None:
    shared_compute_notability_scores(
        sessions,
        weight_functions={
            "activity_specificity": _session_activity_specificity_signal,
            "sleep": _session_sleep_signal,
            "specific_exercise": _session_specific_exercise_signal,
            "hr_available": _session_hr_available_signal,
            "duration": _session_duration_signal,
            "event_count": _session_event_count_signal,
            "high_confidence": _session_high_confidence_signal,
        },
        weights={
            "activity_specificity": NOTABILITY_WEIGHT_ACTIVITY_SPECIFICITY,
            "sleep": NOTABILITY_WEIGHT_SLEEP,
            "specific_exercise": NOTABILITY_WEIGHT_SPECIFIC_EXERCISE,
            "hr_available": NOTABILITY_WEIGHT_HR_AVAILABLE,
            "duration": NOTABILITY_WEIGHT_DURATION,
            "event_count": NOTABILITY_WEIGHT_EVENT_COUNT,
            "high_confidence": NOTABILITY_WEIGHT_HIGH_CONFIDENCE,
        },
    )


def compute_aggregation_notability_scores(aggregations: List[Dict[str, Any]]) -> None:
    """
    Used for non-cardio temporal aggregations: combines sample density with
    recency (previously a plain two-key sort by samples then timestamp).
    """
    max_samples = max((a.get("samples", 0) for a in aggregations), default=0) or 1
    shared_compute_notability_scores(
        aggregations,
        weight_functions={
            "samples": lambda a: a.get("samples", 0) / max_samples,
            "recency": lambda a: recency_weight(a.get("begin_timestamp"), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS),
        },
        weights={
            "samples": AGGREGATION_WEIGHT_SAMPLES,
            "recency": AGGREGATION_WEIGHT_RECENCY,
        },
    )


def compute_recency_only_scores(items: List[Dict[str, Any]], timestamp_field: str) -> None:
    """Used for cardio aggregations, daily activity, and individual events: pure recency ranking."""
    shared_compute_notability_scores(
        items,
        weight_functions={"recency": lambda x: recency_weight(x.get(timestamp_field), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS)},
        weights={"recency": 1.0},
    )


# ============================================================================
# FULL DATASET
# ============================================================================
# FULL contains richer information than PRIMARY, but it is still
# normalized. Raw XML is never copied into the output.
# ============================================================================

def build_full_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if PRUNE_LEVEL == "none" or PRUNE_LEVEL == "light":
        return records

    if PRUNE_LEVEL == "medium":
        # Removes technical metadata rarely useful for analytical
        # retrieval, while preserving one compact normalized representation.
        keep = {
            "event_number", "begin_timestamp", "end_timestamp", "duration_seconds",
            "metric", "category", "value_type", "value", "unit", "source",
            "source_type", "device", "device_model", "device_manufacturer",
            "creation_timestamp", "record_index_in_source",
        }
    elif PRUNE_LEVEL == "aggressive":
        keep = {
            "event_number", "begin_timestamp", "end_timestamp", "metric", "category",
            "value", "unit", "source", "device",
        }
    else:
        raise ValueError(f"Invalid PRUNE_LEVEL: {PRUNE_LEVEL}")

    return [{k: r[k] for k in keep if k in r} for r in records]


def build_full_payload(
    records: List[Dict[str, Any]],
    sessions: List[Dict[str, Any]],
    aggregations: List[Dict[str, Any]],
    daily_activity: List[Dict[str, Any]],
    workouts: List[Dict[str, Any]],
    duplicate_count: int,
) -> Dict[str, Any]:
    full_records = build_full_records(records)

    metadata = build_metadata(
        dataset_name="applehealth_dataset_full",
        source="Apple Health / HealthKit",
        version=DATASET_VERSION,
        purpose=(
            "Normalized, analytical representation of every Apple Health "
            "event, session, workout, and aggregation. Used when PRIMARY "
            "(applehealth_dataset.json) does not contain enough detail to "
            "answer the question."
        ),
        extra={
            "prune_level": PRUNE_LEVEL,
            "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
            "records_after_deduplication": len(records),
            "duplicates_removed": duplicate_count,
            "sessions": len(sessions),
            "temporal_aggregations": len(aggregations),
            "daily_activity_days": len(daily_activity),
            "workouts": len(workouts),
        },
    )

    schema = build_schema(
        sections={
            "records": (
                "Individual normalized HealthKit events. Each has "
                "event_number (stable id used for full_ref), "
                "begin_timestamp/end_timestamp, metric/category (from "
                "SEMANTIC_TYPE_MAP or a structural fallback), value+unit, "
                "source/source_type/device (always scalar, never arrays)."
            ),
            "workouts": (
                "Explicit Apple Workout entries: activity_type_raw, "
                "duration, distance, energy. Stronger evidence for "
                "activity classification than inferring from metrics "
                "alone — see sessions.confidence_rate."
            ),
            "sessions": (
                "Semantically and temporally clustered events (not "
                "necessarily same source/device). Carries both "
                "confidence_rate (how sure the activity_type "
                "classification is) and grouping_confidence_rate (how sure "
                "the grouping itself is a real single session). "
                "event_numbers points back to 'records'."
            ),
            "temporal_aggregations": (
                f"Fixed {TEMPORAL_BUCKET_SECONDS}-second buckets, grouped "
                "by metric+source+device so different sensors are never "
                "silently averaged together."
            ),
            "daily_activity": (
                "Per-day summaries of activity/cardiovascular/sleep "
                "metrics, plus a heart_rate summary block when samples "
                "are available."
            ),
        },
        conventions=[
            "source and device are always single scalar strings, never lists.",
            "confidence_rate follows the fixed scale documented in "
            "timelive.md §27 (1.0 native / 0.8 high / 0.5 medium / 0.2 low "
            "/ absent = not applicable).",
        ],
    )

    logic = build_logic(
        normalization=(
            "HealthKit type identifiers are mapped via SEMANTIC_TYPE_MAP "
            "for known types; unrecognized types fall through infer_metric() "
            "to a structural category guess rather than being dropped. "
            "source/device are parsed from Apple's device string and "
            "reduced to one canonical scalar pair per session via "
            "canonical_contributor (score by event count + metric richness)."
        ),
        deduplication=(
            "No native per-record id exists in the XML export, so "
            "deduplication always uses a composite key of "
            "(metric, begin_timestamp, end_timestamp, value, unit, source, "
            "device). Delegated to the shared mechanism in main.py."
        ),
        classification=(
            "Activity type inference priority: 1) explicit Apple Workout "
            "metadata (confidence_rate=1.0, native), 2) unambiguous "
            "distance metric — cycling/swimming (0.8), 3) ambiguous metric "
            "pattern — walking_running/steps, or intensity-based guess "
            "(0.5), 4) weak/no evidence fallback (0.2). "
            "activity_inference_method preserves which of these branches "
            "fired, since several distinct original signals now map onto "
            "the same standard confidence band."
        ),
        pruning=(
            "PRUNE_LEVEL controls which per-record fields survive in FULL "
            "(none/light: everything; medium: drops rarely-useful "
            "technical metadata; aggressive: keeps only the essentials). "
            "Never affects sessions/aggregations/daily_activity, which are "
            "always kept in full."
        ),
        grouping=(
            "A session groups events close in time AND semantically "
            "compatible: sleep only joins sleep within "
            f"{SESSION_MAX_GAP_SECONDS}s; activity+cardiovascular "
            f"combinations may bridge up to {SESSION_EXTENDED_GAP_SECONDS}s; "
            "same-metric or same-source events join within the normal gap. "
            "Implemented as domain-specific logic rather than through "
            "main.py's generic time-window grouping framework, because the "
            "gap threshold itself varies by event pair — see the module "
            "docstring. Every session carries grouping_confidence_rate=0.8: "
            "deterministic given the thresholds, but still an assumption "
            "about what constitutes one real-world session."
        ),
        pattern_detection=None,  # no recurring-pattern detection in this domain
        interpretation_notes=[
            "event_number_purpose: a stable identifier used ONLY to link "
            "dataset sections together (full_ref from PRIMARY, "
            "event_numbers in sessions/aggregations/daily_activity). Not "
            "meant to be 'readable' by an end user.",
            "energy_unit_policy: energy totals keep whatever unit the "
            "source actually reported rather than assuming kcal.",
            "heart_rate_mode: 'continuous' (>=10 samples), 'sampled' "
            "(<10 samples), 'resting' (only resting_heart_rate available), "
            "or 'not_available'.",
            "how_to_retrieve_detail_from_full: every 'full_ref' in PRIMARY "
            "corresponds to the matching id in this FULL file's "
            "sessions/temporal_aggregations/daily_activity/records "
            "sections, by the id scheme in that section (session_id, "
            "aggregation_id, summary_id, or event_number respectively).",
        ],
    )

    return clean_dict({
        "_metadata": metadata,
        "_schema": schema,
        "_logic": logic,
        "records": full_records,
        "workouts": workouts,
        "sessions": sessions,
        "temporal_aggregations": aggregations,
        "daily_activity": daily_activity,
    })


# ============================================================================
# PRIMARY DATASET
# ============================================================================
# PRIMARY is built as a relevance-ranked view of FULL. Priority when the
# budget is constrained (unchanged design):
#   1. significant sports/activity sessions
#   2. sleep
#   3. cardio / heart rate
#   4. daily activity
#   5. temporal aggregations
#   6. individual events
#
# Ranking within each section now goes through main.compute_notability_scores
# (or plain recency for sections that were already recency-sorted), and the
# actual size-budget selection is delegated to main.select_within_size_budget,
# called once per section with the running cumulative size carried forward —
# this reproduces the previous cross-section priority order while reusing
# the shared engine for the ranking + bin-packing mechanics.
# ============================================================================

def build_global_heart_rate_summary(records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    values = [r.get("value") for r in records if r.get("metric") == "heart_rate" and isinstance(r.get("value"), (int, float))]
    if not values:
        return None
    return {
        "metric": "heart_rate",
        "samples": len(values),
        "average": round(sum(values) / len(values), 2),
        "min": min(values),
        "max": max(values),
        "unit": "count/min",
    }


def build_primary_dataset(
    sessions: List[Dict[str, Any]],
    aggregations: List[Dict[str, Any]],
    daily_activity: List[Dict[str, Any]],
    records: List[Dict[str, Any]],
    full_payload_size_bytes: int,
) -> Dict[str, Any]:
    target_bytes = int(PRIMARY_MAX_SIZE_MB * 1024 * 1024) if PRIMARY_MAX_SIZE_MB else None
    soft_overflow_ratio = PRIMARY_SOFT_OVERFLOW_RATIO

    # --- Rank each section by the appropriate signal ---
    compute_session_notability_scores(sessions)
    ranked_sessions = sorted(sessions, key=lambda s: s.get("notability_score", 0.0), reverse=True)

    session_items = []
    for session in ranked_sessions:
        # PRIMARY deliberately uses a smaller vocabulary than FULL.
        # timestamp_begin/timestamp_end are the canonical PRIMARY names so
        # this dataset is easy to join with Spotify, bank, calendar, etc.
        # Fields useful for audit/debugging (inference method,
        # event_numbers, event_count) remain available in FULL instead.
        item = clean_dict({
            "session_id": session.get("session_id"),
            "timestamp_begin": session.get("begin_timestamp"),
            "timestamp_end": session.get("end_timestamp"),
            "duration_seconds": session.get("duration_seconds"),
            "activity_type": session.get("activity_type"),
            "confidence_rate": session.get("confidence_rate"),
            "source": session.get("source"),
            "device": session.get("device"),
            "heart_rate_mode": session.get("heart_rate_mode"),
            "energy_unit": session.get("energy_unit"),
            "metrics": session.get("metrics"),
            "notability_score": session.get("notability_score", 0.0),
            "full_ref": f"sessions/{session['session_id']}",
        })
        session_items.append(item)

    hr_metrics = {"heart_rate", "resting_heart_rate", "walking_heart_rate_average", "heart_rate_variability"}
    hr_aggs = [a for a in aggregations if a.get("metric") in hr_metrics]
    compute_recency_only_scores(hr_aggs, timestamp_field="begin_timestamp")
    hr_aggs.sort(key=lambda a: a.get("notability_score", 0.0), reverse=True)
    hr_aggs = [{**a, "full_ref": f"temporal_aggregations/{a['aggregation_id']}"} for a in hr_aggs]

    other_aggs = [a for a in aggregations if a.get("metric") not in hr_metrics]
    compute_aggregation_notability_scores(other_aggs)
    other_aggs.sort(key=lambda a: a.get("notability_score", 0.0), reverse=True)
    other_aggs = [{**a, "full_ref": f"temporal_aggregations/{a['aggregation_id']}"} for a in other_aggs]

    compute_recency_only_scores(daily_activity, timestamp_field="begin_timestamp")
    daily_items = [{**d, "full_ref": f"daily_activity/{d['summary_id']}"} for d in daily_activity]
    daily_items.sort(key=lambda d: d.get("notability_score", 0.0), reverse=True)

    hr_summary = build_global_heart_rate_summary(records)

    # --- Budget-filled selection, section by section, in priority order ---
    # (timelive.md §15/§16: notability-ranked, size-budgeted selection —
    # applied per section here to reproduce the documented cross-section
    # priority: sessions > sleep > cardio > daily > other aggregations.)
    selected: Dict[str, List[Dict[str, Any]]] = {}
    seen_session_ids: set = set()
    cumulative_size = 0

    def fill_section(name: str, candidates: List[Dict[str, Any]]) -> None:
        nonlocal cumulative_size
        chosen = select_within_size_budget(
            candidates,
            target_bytes=target_bytes,
            soft_overflow_ratio=soft_overflow_ratio,
            rank_field="notability_score",
            always_include_bytes=cumulative_size,
        )
        for item in chosen:
            item.pop("notability_score", None)
        selected[name] = chosen
        cumulative_size += sum(estimate_json_size_bytes(i) for i in chosen)

    fill_section("significant_sessions", session_items)
    seen_session_ids.update(s.get("session_id") for s in selected["significant_sessions"])

    # To avoid duplicating sleep sessions, only include ones not already
    # selected into significant_sessions.
    sleep_candidates = [
        s for s in session_items
        if s.get("activity_type") == "sleep" and s.get("session_id") not in seen_session_ids
    ]
    fill_section("sleep_sessions", sleep_candidates)

    fill_section("cardio_heart_rate", hr_aggs)
    fill_section("daily_activity", daily_items)
    fill_section("temporal_aggregations", other_aggs)

    # --- Individual events: lowest priority, only when there is still room ---
    # Replaces the previous fixed "last 500 records" slice with a proper
    # recency-based ranking bounded by whatever budget remains.
    if not target_bytes or cumulative_size < target_bytes:
        event_candidates = [r for r in records if r.get("metric") not in HIGH_FREQUENCY_METRICS]
        compute_recency_only_scores(event_candidates, timestamp_field="begin_timestamp")
        event_views = []
        for r in event_candidates:
            item = dict(r)
            item["full_ref"] = f"records/{r['event_number']}"
            event_views.append(item)
        fill_section("individual_events", event_views)
    else:
        selected["individual_events"] = []

    metadata = build_metadata(
        dataset_name="applehealth_dataset",
        source="Apple Health / HealthKit",
        version=DATASET_VERSION,
        purpose=(
            "Compact, LLM-oriented view of Apple Health data. Prioritizes "
            "significant sessions, sleep, cardio, daily activity, and "
            "aggregations over raw individual events. If the requested "
            "information is not here, retrieve it from "
            "applehealth_dataset_full.json via the full_ref field."
        ),
        extra={
            "prune_level": PRUNE_LEVEL,
            "primary_max_size_mb_target": PRIMARY_MAX_SIZE_MB,
            "full_dataset_size_bytes": full_payload_size_bytes,
        },
    )

    schema = build_schema(
        sections={
            "significant_sessions": (
                "Notability-ranked, budget-selected sessions (see "
                "temporal_aggregations for the ranking signals). "
                "full_ref points to sessions/<session_id> in FULL."
            ),
            "sleep_sessions": "Sleep sessions not already present in significant_sessions.",
            "cardio_heart_rate": "Heart-rate-family temporal aggregations, ranked by recency.",
            "daily_activity": "Per-day activity summaries, ranked by recency.",
            "temporal_aggregations": "Non-cardio temporal aggregations, ranked by sample density + recency.",
            "individual_events": (
                "Lowest-priority individual events (excludes high-frequency "
                "metrics already covered by aggregations), ranked by recency, "
                "included only while budget remains."
            ),
        },
    )

    logic = build_logic(
        normalization="See applehealth_dataset_full.json's _logic for full detail; PRIMARY reuses the same normalized records/sessions.",
        deduplication="Deduplication happens once, upstream of both PRIMARY and FULL — see applehealth_dataset_full.json's _logic.",
        classification="See applehealth_dataset_full.json's _logic for the activity-type inference priority and its confidence_rate mapping.",
        pruning=(
            f"Sections are filled in strict priority order (significant "
            f"sessions, sleep, cardio, daily activity, other aggregations, "
            f"individual events), each ranked by notability_score and "
            f"selected via main.select_within_size_budget against the "
            f"shared {PRIMARY_MAX_SIZE_MB}MB target with "
            f"{PRIMARY_SOFT_OVERFLOW_RATIO*100:.0f}% soft overflow. Cumulative "
            "size carries over between sections, so earlier, higher-"
            "priority sections are never starved by later ones."
        ),
        grouping="See applehealth_dataset_full.json's _logic for the session-grouping criteria.",
        interpretation_notes=[
            "why_generic_hr_summary: hr_summary (top-level) gives a global "
            "heart-rate picture so generic questions like 'how was my "
            "heart rate?' don't require finding one particular session or "
            "aggregation first.",
            "how_to_retrieve_detail: use full_ref to retrieve the full "
            "object from applehealth_dataset_full.json.",
        ],
    )

    payload = {
        "_metadata": metadata,
        "_schema": schema,
        "_logic": logic,
        "heart_rate_overall": hr_summary,
        "sessions": selected["significant_sessions"],
        "sleep": selected["sleep_sessions"],
        "cardio_heart_rate": selected["cardio_heart_rate"],
        "daily_activity": selected["daily_activity"],
        "temporal_aggregations": selected["temporal_aggregations"],
        "individual_events": selected["individual_events"],
    }
    payload["_metadata"]["estimated_content_bytes"] = estimate_json_size_bytes(payload)
    payload["_metadata"]["target_bytes"] = target_bytes
    payload["_metadata"]["selected_sessions"] = len(selected["significant_sessions"])
    payload["_metadata"]["selected_sleep_sessions"] = len(selected["sleep_sessions"])
    payload["_metadata"]["selected_hr_aggregations"] = len(selected["cardio_heart_rate"])
    payload["_metadata"]["selected_daily_activity"] = len(selected["daily_activity"])
    payload["_metadata"]["selected_temporal_aggregations"] = len(selected["temporal_aggregations"])
    payload["_metadata"]["selected_individual_events"] = len(selected["individual_events"])
    return clean_dict(payload)


# ============================================================================
# MAIN ENTRYPOINT
# ============================================================================

def ingest_health_history(
    enabled: bool = True,
    prune_level_override: Optional[str] = None,
    activity_inference_level_override: Optional[str] = None,
) -> Dict[str, Any]:
    """
    `enabled` / `*_override` are explicit-parameter overrides for the
    orchestrator (timelive.md §38) — main.run_all_ingests() sets these
    instead of ever mutating this module's globals from outside. When
    `enabled` is False, this function does no file I/O and returns
    immediately.
    """
    if not enabled:
        return {"success": True, "status": "skipped", "reason": "disabled via enabled=False"}

    global PRUNE_LEVEL, ACTIVITY_INFERENCE_LEVEL
    if prune_level_override is not None:
        PRUNE_LEVEL = prune_level_override
    if activity_inference_level_override is not None:
        ACTIVITY_INFERENCE_LEVEL = activity_inference_level_override

    if PRUNE_LEVEL not in VALID_PRUNE_LEVELS:
        raise ValueError(f"PRUNE_LEVEL must be one of: {', '.join(sorted(VALID_PRUNE_LEVELS))}")
    if ACTIVITY_INFERENCE_LEVEL not in VALID_ACTIVITY_INFERENCE_LEVELS:
        raise ValueError(f"ACTIVITY_INFERENCE_LEVEL must be one of: {', '.join(sorted(VALID_ACTIVITY_INFERENCE_LEVELS))}")

    xml_path = Path(HEALTH_INPUT_FILE)
    primary_path = Path(HEALTH_OUTPUT_DATASET_PATH)
    full_path = Path(HEALTH_OUTPUT_FULL_DATASET_PATH)

    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []

    if not xml_path.exists():
        return {
            "success": False,
            "status": "missing_input_file",
            "input_file": str(xml_path),
            "outputs": {"primary": str(primary_path), "full": str(full_path)},
        }

    records: List[Dict[str, Any]] = []
    workouts: List[Dict[str, Any]] = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for index, rec_el in enumerate(root.iter("Record"), start=1):
            record = parse_record_element(rec_el, index)
            if record:
                records.append(record)

        for index, workout_el in enumerate(root.iter("Workout"), start=1):
            workout = parse_workout_element(workout_el, index)
            if workout:
                workouts.append(workout)
    except Exception as exc:
        errors.append({"file": xml_path.name, "error_type": "xml_parse_error", "message": str(exc)})

    records, duplicate_count = deduplicate_records(records)
    records = sort_records(records)
    assign_event_numbers(records)

    aggregations = aggregate_records(records)
    daily_activity = build_daily_activity(records)
    sessions = detect_sessions(records, workouts)

    # Build FULL first because PRIMARY is conceptually a derived view of it.
    full_payload = build_full_payload(records, sessions, aggregations, daily_activity, workouts, duplicate_count)
    full_size_estimate = estimate_json_size_bytes(full_payload)

    full_size_warning = check_full_size_warning(full_size_estimate, warning_gb=FULL_WARNING_SIZE_GB)
    if full_size_warning:
        warnings.append({"warning_type": "full_dataset_large", "message": full_size_warning})
        full_payload["_metadata"]["warnings"] = warnings

    primary_payload = build_primary_dataset(
        sessions=sessions,
        aggregations=aggregations,
        daily_activity=daily_activity,
        records=records,
        full_payload_size_bytes=full_size_estimate,
    )

    # --- Write: ONLY these two files (timelive.md §11) ---
    primary_size = write_json(primary_path, primary_payload)
    full_size = write_json(full_path, full_payload)

    return {
        "success": True,
        "input_file": str(xml_path),
        "records_after_deduplication": len(records),
        "duplicates_removed": duplicate_count,
        "sessions": len(sessions),
        "temporal_aggregations": len(aggregations),
        "workouts": len(workouts),
        "primary_size_bytes": primary_size,
        "full_size_bytes": full_size,
        "prune_level": PRUNE_LEVEL,
        "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
        "errors": errors,
        "warnings": warnings,
        "outputs": {
            "primary": str(primary_path),
            "full": str(full_path),
        },
    }


if __name__ == "__main__":
    print(json.dumps(ingest_health_history(), ensure_ascii=False, indent=2, default=str))