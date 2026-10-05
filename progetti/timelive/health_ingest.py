# ============================================================================
# APPLE HEALTH INGEST V4
# ============================================================================
#
# DESIGN GOAL
# ------------
# RAW Apple Health XML is converted into two useful layers:
#
#   FULL
#       Analytical/intermediate dataset. It keeps the information needed to
#       answer questions that PRIMARY cannot answer directly. It contains
#       normalized events, temporal aggregations, sessions and daily summaries.
#
#   PRIMARY
#       Small, LLM-oriented dataset. It is NOT just a mechanically pruned
#       copy of FULL. It is built from the most useful sessions and summaries
#       and is constrained by PRIMARY_MAX_SIZE_MB.
#
# IMPORTANT DESIGN RULES
# ----------------------
# 1. Timestamps are the source of temporal information. We do not duplicate
#    year/month/day/hour/weekday fields in every event.
# 2. source and device are always scalar strings, never lists.
# 3. A session can combine multiple underlying events/sources/devices. The
#    session receives one canonical source and one canonical device selected
#    deterministically from the contributors.
# 4. Activity type is inferred at BALANCED confidence: explicit Apple workout
#    information wins; otherwise metrics + duration + intensity can infer a
#    type. Ambiguous activity remains generic instead of being invented.
# 5. PRIMARY is a TARGET size, not a hard limit. The selector tries to remain
#    below the target and may exceed it slightly when the next useful item is
#    worth keeping.
# 6. FULL is intentionally richer than PRIMARY. If an LLM cannot answer a
#    question from PRIMARY, it can use stable full_ref identifiers to retrieve
#    the corresponding FULL object.
#
# ============================================================================

from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================

try:
    from config import (
        HEALTH_INPUT_DIR,
        HEALTH_INPUT_FILE,
        HEALTH_OUTPUT_DATASET_PATH,
        HEALTH_OUTPUT_FULL_DATASET_PATH,
        HEALTH_OUTPUT_SUMMARY_PATH,
    )
except Exception:
    HEALTH_INPUT_DIR = Path(r"C:\Users\campe\Desktop\Timelive\Input\Apple Health")
    HEALTH_INPUT_FILE = HEALTH_INPUT_DIR / "export.xml"
    OUTPUT_DIR = Path(r"C:\Users\campe\Desktop\Timelive\Output")
    HEALTH_OUTPUT_DATASET_PATH = OUTPUT_DIR / "applehealth_history_dataset.json"
    HEALTH_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / "applehealth_history_dataset_full.json"
    HEALTH_OUTPUT_SUMMARY_PATH = OUTPUT_DIR / "applehealth_history_summary.json"

SOURCE_PREFIX = "health"
DATASET_VERSION = "4.0"

# ---------------------------------------------------------------------------
# PRUNING
# ---------------------------------------------------------------------------
# light      = keep more individual events in FULL and allow more detail.
# medium     = default; high-frequency data is strongly aggregated.
# aggressive = remove more low-value granular events from FULL.
#
# PRUNING affects what is retained in FULL. PRIMARY has its own independent
# size-budget selection below.
# ---------------------------------------------------------------------------
PRUNE_LEVEL = "medium"
VALID_PRUNE_LEVELS = {"light", "medium", "aggressive"}

# ---------------------------------------------------------------------------
# PRIMARY SIZE TARGET
# ---------------------------------------------------------------------------
# This is a TARGET, not a hard cap.
# The selector keeps adding useful objects until the estimated serialized size
# reaches the target. It may go slightly over when the next object is valuable.
# Set to 0 or None to disable the size budget.
# ---------------------------------------------------------------------------
PRIMARY_MAX_SIZE_MB = 25.0
PRIMARY_SOFT_OVERFLOW_RATIO = 0.10  # allow roughly 10% over target if useful

# ---------------------------------------------------------------------------
# TEMPORAL AGGREGATION
# ---------------------------------------------------------------------------
# 300 = 5-minute windows.
# Change this value only if a different temporal resolution is wanted:
#   60   -> 1 minute
#   900  -> 15 minutes
#   3600 -> 1 hour
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

# Events that are too long are prevented from accidentally swallowing unrelated
# periods. Increase only if long-running measurements should be one session.
SESSION_MAX_DURATION_SECONDS = 6 * 60 * 60

# ---------------------------------------------------------------------------
# ACTIVITY INFERENCE
# ---------------------------------------------------------------------------
# balanced = explicit workout/activity metadata first, then metric pattern,
# duration and intensity. Ambiguous cases stay generic.
ACTIVITY_INFERENCE_LEVEL = "balanced"
VALID_ACTIVITY_INFERENCE_LEVELS = {"conservative", "balanced", "aggressive"}

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


# ============================================================================
# HEALTHKIT SEMANTIC MAP
# ============================================================================
# This map is deliberately kept explicit for known Apple Health identifiers.
# Unknown identifiers still pass through infer_metric() and receive a generic
# fallback instead of being silently discarded.
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
            dt = datetime.fromisoformat(candidate)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            pass
    for fmt in (
        "%Y-%m-%d %H:%M:%S %z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f %z",
        "%Y-%m-%dT%H:%M:%S%z",
    ):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)
        except ValueError:
            pass
    return None


def to_iso_utc(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_identifier(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return re.sub(r"_+", "_", value).strip("_")


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    output = {}
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
# year/month/day/hour/source_file are removed because they duplicate timestamp
# or file-level metadata and make cross-dataset interoperability harder.
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
    """Parse an Apple Health <Workout> as explicit activity metadata.

    Apple exports can contain an explicit workout type, duration, distance and
    energy. This information is stronger evidence for activity classification
    than trying to infer running/cycling/etc. only from heart rate or steps.
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
# EVENT CLEANUP
# ============================================================================

def make_dedup_key(record: Dict[str, Any]) -> Tuple[Any, ...]:
    return (
        record.get("metric"), record.get("begin_timestamp"),
        record.get("end_timestamp"), record.get("value"), record.get("unit"),
        record.get("source"), record.get("device"),
    )


def deduplicate_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    seen = set()
    result = []
    duplicates = 0
    for record in records:
        key = make_dedup_key(record)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        result.append(record)
    return result, duplicates


def sort_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(records, key=lambda r: (r.get("begin_timestamp") or "", r.get("end_timestamp") or ""))


def assign_event_numbers(records: List[Dict[str, Any]]) -> None:
    for i, record in enumerate(records, start=1):
        record["event_number"] = f"{SOURCE_PREFIX}_{i}"


def dt(value: Optional[str]) -> Optional[datetime]:
    return parse_date(value)


def seconds_between(a: Optional[str], b: Optional[str]) -> Optional[float]:
    da, db = dt(a), dt(b)
    if not da or not db:
        return None
    return (db - da).total_seconds()


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
# Aggregations are intentionally grouped by metric + source + device.
# This prevents values from different sensors being silently averaged together.
# Sessions later combine semantically compatible events across sources.
# ============================================================================

def aggregate_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups = defaultdict(list)
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
    days = defaultdict(list)
    for r in records:
        timestamp = r.get("begin_timestamp")
        if timestamp:
            day = timestamp[:10]
            if r.get("metric") in ACTIVITY_METRICS or r.get("category") in {"activity", "cardiovascular", "sleep"}:
                days[day].append(r)

    output = []
    for day in sorted(days):
        items = days[day]
        by_metric = defaultdict(float)
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
# ACTIVITY TYPE INFERENCE
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


def infer_activity_type(items: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> Tuple[str, float, str]:
    # Explicit Workout metadata is the strongest evidence.
    if workouts:
        types = [normalize_workout_activity(w.get("activity_type_raw")) for w in workouts]
        if types:
            counts = Counter(types)
            activity = counts.most_common(1)[0][0]
            return activity, 1.0, "explicit_workout"

    metrics = Counter(x.get("metric") for x in items)
    duration = max((x.get("duration_seconds") or 0) for x in items)
    total_distance = sum(float(x.get("value")) for x in items if x.get("metric") in {"distance_walking_running", "distance_cycling", "distance_swimming"} and isinstance(x.get("value"), (int, float)))
    hr_values = [x.get("value") for x in items if x.get("metric") == "heart_rate" and isinstance(x.get("value"), (int, float))]
    avg_hr = sum(hr_values) / len(hr_values) if hr_values else None

    if metrics["distance_cycling"] > 0:
        return "cycling", 0.85, "metric_pattern"
    if metrics["distance_swimming"] > 0:
        return "swimming", 0.85, "metric_pattern"
    if metrics["distance_walking_running"] > 0:
        # Without explicit workout metadata we cannot reliably distinguish walk
        # from run. Balanced mode therefore uses a generic walking_running label.
        return "walking_running", 0.70, "metric_pattern"

    if metrics["steps"] > 0 and (avg_hr is not None or duration >= 20 * 60):
        return "walking_or_general_activity", 0.60, "metric_pattern"

    if metrics["heart_rate"] > 0 and avg_hr is not None and avg_hr >= 120 and duration >= 15 * 60:
        return "cardio_activity", 0.65, "intensity_pattern"

    if total_distance > 0:
        return "physical_activity", 0.50, "generic_activity"

    return "physical_activity", 0.35, "generic_activity"


# ============================================================================
# SESSION COMPATIBILITY + DETECTION
# ============================================================================
# A session is NOT defined by identical source/device. It is a semantic/time
# cluster. This is important for Apple Health because one real workout may have
# HR from a Polar strap, steps from an iPhone/Watch and energy from Apple.
#
# The exact rules are deliberately visible here so an AI can change them.
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
    current = []
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
            # Overlap or <= 5 minutes distance means the workout is likely the
            # explicit activity descriptor for this event cluster.
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
    """Choose ONE source and ONE device for interoperability.

    We score contributors by number of events, then by metric richness.
    This deliberately avoids arrays in source/device while still producing a
    deterministic representative identity for the combined session.
    """
    score = defaultdict(float)
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

    activity_type, confidence, inference_method = infer_activity_type(items, workouts)
    source, device = canonical_contributor(items)
    metrics = defaultdict(list)
    units = {}
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

    # Energy is kept as a numeric summary plus the unit actually present in the
    # source. This avoids assuming kcal when Apple exported another unit.
    energy_values = metrics.get("active_energy", [])
    energy_unit = units.get("active_energy")

    return clean_dict({
        "session_id": f"session_{index}",
        "begin_timestamp": begin,
        "end_timestamp": end,
        "duration_seconds": duration,
        "activity_type": activity_type,
        "activity_confidence": round(confidence, 2),
        "activity_inference": inference_method,
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
# FULL DATASET
# ============================================================================
# FULL contains richer information than PRIMARY, but it is still normalized.
# Raw XML is never copied into the output.
# ============================================================================

def build_full_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if PRUNE_LEVEL == "light":
        return records

    if PRUNE_LEVEL == "medium":
        # Remove technical metadata that is rarely useful for analytical
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


def build_full_payload(records, sessions, aggregations, daily_activity, workouts, duplicate_count):
    full_records = build_full_records(records)
    return clean_dict({
        "_metadata": {
            "dataset": "applehealth_history_dataset_full",
            "source": "Apple Health / HealthKit",
            "version": DATASET_VERSION,
            "purpose": "analytical_intermediate",
            "primary_is_derived_from_full": True,
        },
        "_configuration": {
            "prune_level": PRUNE_LEVEL,
            "temporal_bucket_seconds": TEMPORAL_BUCKET_SECONDS,
            "session_max_gap_seconds": SESSION_MAX_GAP_SECONDS,
            "session_extended_gap_seconds": SESSION_EXTENDED_GAP_SECONDS,
            "session_max_duration_seconds": SESSION_MAX_DURATION_SECONDS,
            "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
            "primary_max_size_mb": PRIMARY_MAX_SIZE_MB,
        },
        "statistics": {
            "records_after_deduplication": len(records),
            "duplicates_removed": duplicate_count,
            "sessions": len(sessions),
            "temporal_aggregations": len(aggregations),
            "daily_activity_days": len(daily_activity),
            "workouts": len(workouts),
        },
        "records": full_records,
        "workouts": workouts,
        "sessions": sessions,
        "temporal_aggregations": aggregations,
        "daily_activity": daily_activity,
    })


# ============================================================================
# PRIMARY DATASET
# ============================================================================
# PRIMARY is built as a relevance-ranked view of FULL.
# Priority when the budget is constrained (confirmed design):
#   1. significant sports/activity sessions
#   2. sleep
#   3. cardio / heart rate
#   4. daily activity
#   5. temporal aggregations
#   6. individual events
#
# A small amount of global/temporal HR information is promoted because generic
# questions such as "how was my heart rate?" should not require finding one
# particular session first.
# ============================================================================

def json_size_bytes(value: Any) -> int:
    return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def session_priority(session: Dict[str, Any]) -> float:
    activity = session.get("activity_type", "physical_activity")
    score = 0.0
    if activity not in {"physical_activity", "walking_or_general_activity"}:
        score += 100
    if activity in {"running", "cycling", "swimming", "hiking", "strength_training", "cardio_activity"}:
        score += 40
    if activity == "sleep":
        score += 90
    if session.get("heart_rate_mode") in {"continuous", "sampled", "resting"}:
        score += 25
    duration = session.get("duration_seconds") or 0
    score += min(duration / 60.0, 120) * 0.25
    score += min(session.get("event_count", 0), 1000) * 0.02
    if session.get("activity_confidence", 0) >= 0.8:
        score += 15
    return score


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


def build_primary_dataset(sessions, aggregations, daily_activity, records, full_payload_size_bytes: int) -> Dict[str, Any]:
    # Each object carries a stable full_ref. This is the bridge for a future
    # retrieval script: PRIMARY tells the LLM what is relevant; FULL supplies
    # detail only when needed.
    ranked_sessions = sorted(sessions, key=session_priority, reverse=True)
    session_items = []
    for session in ranked_sessions:
        # PRIMARY deliberately uses a smaller vocabulary than FULL.
        # timestamp_begin/timestamp_end are the canonical PRIMARY names so
        # this dataset is easier to join with Spotify, bank, calendar, etc.
        # Fields useful for audit/debugging (confidence, inference method,
        # event_numbers, event_count) remain available in FULL instead.
        item = clean_dict({
            "session_id": session.get("session_id"),
            "timestamp_begin": session.get("begin_timestamp"),
            "timestamp_end": session.get("end_timestamp"),
            "duration_seconds": session.get("duration_seconds"),
            "activity_type": session.get("activity_type"),
            "source": session.get("source"),
            "device": session.get("device"),
            "heart_rate_mode": session.get("heart_rate_mode"),
            "energy_unit": session.get("energy_unit"),
            "metrics": session.get("metrics"),
            "full_ref": f"sessions/{session['session_id']}",
        })
        session_items.append(item)

    # HR temporal aggregations are particularly useful for generic questions.
    hr_aggs = [a for a in aggregations if a.get("metric") in {"heart_rate", "resting_heart_rate", "walking_heart_rate_average", "heart_rate_variability"}]
    hr_aggs.sort(key=lambda x: x.get("begin_timestamp", ""), reverse=True)
    hr_aggs = [{**a, "full_ref": f"temporal_aggregations/{a['aggregation_id']}"} for a in hr_aggs]

    # Other aggregations are ranked by informational density: more samples and
    # more useful activity metrics first.
    other_aggs = [a for a in aggregations if a.get("metric") not in {"heart_rate", "resting_heart_rate", "walking_heart_rate_average", "heart_rate_variability"}]
    other_aggs.sort(key=lambda x: ((x.get("samples") or 0), x.get("begin_timestamp", "")), reverse=True)
    other_aggs = [{**a, "full_ref": f"temporal_aggregations/{a['aggregation_id']}"} for a in other_aggs]

    daily_items = [{**d, "full_ref": f"daily_activity/{d['summary_id']}"} for d in daily_activity]
    daily_items.sort(key=lambda x: x.get("begin_timestamp", ""), reverse=True)

    hr_summary = build_global_heart_rate_summary(records)

    sections = [
        ("significant_sessions", session_items),
        ("sleep_sessions", [x for x in session_items if x.get("activity_type") == "sleep"]),
        ("cardio_heart_rate", hr_aggs),
        ("daily_activity", daily_items),
        ("temporal_aggregations", other_aggs),
    ]

    selected = {"significant_sessions": [], "sleep_sessions": [], "cardio_heart_rate": [], "daily_activity": [], "temporal_aggregations": []}
    current_size = 0
    target = int(PRIMARY_MAX_SIZE_MB * 1024 * 1024) if PRIMARY_MAX_SIZE_MB else 0
    overflow = int(target * PRIMARY_SOFT_OVERFLOW_RATIO) if target else 0

    # To avoid duplicating sleep sessions, they are included in the sleep
    # section only if not already present in significant_sessions.
    seen_ids = set()
    for section_name, items in sections:
        if section_name == "sleep_sessions":
            items = [x for x in items if x.get("session_id") not in seen_ids]
        for item in items:
            if section_name == "significant_sessions" and item.get("session_id"):
                seen_ids.add(item["session_id"])
            candidate_size = json_size_bytes(item)
            if target and current_size + candidate_size > target:
                if current_size + candidate_size <= target + overflow:
                    selected[section_name].append(item)
                    current_size += candidate_size
                continue
            selected[section_name].append(item)
            current_size += candidate_size

    # Individual events are lowest priority and are only promoted when there is
    # still meaningful room. We prefer non-HR events because HR already has
    # dedicated aggregations above.
    if not target or current_size < target:
        event_candidates = [
            r for r in records
            if r.get("metric") not in HIGH_FREQUENCY_METRICS
        ]
        event_candidates = event_candidates[-500:]
        event_items = []
        for r in reversed(event_candidates):
            item = dict(r)
            item["full_ref"] = f"records/{r['event_number']}"
            event_items.append(item)
            if target and current_size + json_size_bytes(item) > target + overflow:
                break
            current_size += json_size_bytes(item)

        selected["individual_events"] = list(reversed(event_items))
    else:
        selected["individual_events"] = []

    payload = {
        "_metadata": {
            "dataset": "applehealth_history_dataset",
            "source": "Apple Health / HealthKit",
            "version": DATASET_VERSION,
            "purpose": "llm_primary_retrieval",
            "size_policy": "target_not_hard_limit",
            "full_dataset_size_bytes": full_payload_size_bytes,
        },
        "_configuration": {
            "prune_level": PRUNE_LEVEL,
            "primary_max_size_mb": PRIMARY_MAX_SIZE_MB,
            "primary_soft_overflow_ratio": PRIMARY_SOFT_OVERFLOW_RATIO,
            "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
        },
        "heart_rate_overall": hr_summary,
        "sessions": selected["significant_sessions"],
        "sleep": selected["sleep_sessions"],
        "cardio_heart_rate": selected["cardio_heart_rate"],
        "daily_activity": selected["daily_activity"],
        "temporal_aggregations": selected["temporal_aggregations"],
        "individual_events": selected["individual_events"],
    }
    payload["_statistics"] = {
        "estimated_content_bytes": json_size_bytes(payload),
        "target_bytes": target or None,
        "target_utilization": round(json_size_bytes(payload) / target, 3) if target else None,
        "selected_sessions": len(selected["significant_sessions"]),
        "selected_sleep_sessions": len(selected["sleep_sessions"]),
        "selected_hr_aggregations": len(selected["cardio_heart_rate"]),
        "selected_daily_activity": len(selected["daily_activity"]),
        "selected_temporal_aggregations": len(selected["temporal_aggregations"]),
        "selected_individual_events": len(selected["individual_events"]),
    }
    return clean_dict(payload)


# ============================================================================
# SUMMARY / I/O
# ============================================================================

def build_summary(records, sessions, aggregations, workouts, duplicate_count, primary_size, full_size):
    return clean_dict({
        "_metadata": {
            "dataset": "applehealth_history_summary",
            "source": "Apple Health / HealthKit",
            "version": DATASET_VERSION,
        },
        "statistics": {
            "records_after_deduplication": len(records),
            "duplicates_removed": duplicate_count,
            "sessions": len(sessions),
            "temporal_aggregations": len(aggregations),
            "workouts": len(workouts),
            "primary_size_bytes": primary_size,
            "full_size_bytes": full_size,
            "full_size_mb": round(full_size / 1024 / 1024, 2),
            "warning_full_over_500mb": full_size > 500 * 1024 * 1024,
            "metrics": dict(Counter(r.get("metric") for r in records if r.get("metric"))),
            "categories": dict(Counter(r.get("category") for r in records if r.get("category"))),
            "sources": dict(Counter(r.get("source") for r in records if r.get("source"))),
            "devices": dict(Counter(r.get("device") for r in records if r.get("device"))),
        },
        "_configuration": {
            "prune_level": PRUNE_LEVEL,
            "primary_max_size_mb": PRIMARY_MAX_SIZE_MB,
            "temporal_bucket_seconds": TEMPORAL_BUCKET_SECONDS,
            "session_max_gap_seconds": SESSION_MAX_GAP_SECONDS,
            "session_extended_gap_seconds": SESSION_EXTENDED_GAP_SECONDS,
            "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
        },
    })


def write_json(path: Path, payload: Dict[str, Any]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    return path.stat().st_size


def ingest_health_history() -> Dict[str, Any]:
    if PRUNE_LEVEL not in VALID_PRUNE_LEVELS:
        raise ValueError(f"PRUNE_LEVEL must be one of: {', '.join(sorted(VALID_PRUNE_LEVELS))}")
    if ACTIVITY_INFERENCE_LEVEL not in VALID_ACTIVITY_INFERENCE_LEVELS:
        raise ValueError(f"ACTIVITY_INFERENCE_LEVEL must be one of: {', '.join(sorted(VALID_ACTIVITY_INFERENCE_LEVELS))}")

    xml_path = Path(HEALTH_INPUT_FILE)
    primary_path = Path(HEALTH_OUTPUT_DATASET_PATH)
    full_path = Path(HEALTH_OUTPUT_FULL_DATASET_PATH)
    summary_path = Path(HEALTH_OUTPUT_SUMMARY_PATH)
    if not xml_path.exists():
        raise FileNotFoundError(f"Apple Health export not found: {xml_path}")

    records = []
    workouts = []
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

    records, duplicate_count = deduplicate_records(records)
    records = sort_records(records)
    assign_event_numbers(records)

    aggregations = aggregate_records(records)
    daily_activity = build_daily_activity(records)
    sessions = detect_sessions(records, workouts)

    # Build FULL first because PRIMARY is conceptually a derived view of it.
    full_payload = build_full_payload(
        records, sessions, aggregations, daily_activity, workouts, duplicate_count
    )
    full_size_estimate = json_size_bytes(full_payload)

    primary_payload = build_primary_dataset(
        sessions=sessions,
        aggregations=aggregations,
        daily_activity=daily_activity,
        records=records,
        full_payload_size_bytes=full_size_estimate,
    )

    primary_size = write_json(primary_path, primary_payload)
    full_size = write_json(full_path, full_payload)

    if full_size > 500 * 1024 * 1024:
        print(
            "WARNING: FULL dataset is larger than 0.5 GB. "
            "Consider increasing pruning/aggregation if this becomes a recurring issue."
        )

    summary_payload = build_summary(
        records, sessions, aggregations, workouts, duplicate_count,
        primary_size, full_size,
    )
    write_json(summary_path, summary_payload)

    return {
        "status": "success",
        "input_file": str(xml_path),
        "records_after_deduplication": len(records),
        "duplicates_removed": duplicate_count,
        "sessions": len(sessions),
        "temporal_aggregations": len(aggregations),
        "workouts": len(workouts),
        "primary_dataset": str(primary_path),
        "full_dataset": str(full_path),
        "summary": str(summary_path),
        "primary_size_mb": round(primary_size / 1024 / 1024, 2),
        "primary_target_mb": PRIMARY_MAX_SIZE_MB,
        "full_size_mb": round(full_size / 1024 / 1024, 2),
        "full_over_500mb": full_size > 500 * 1024 * 1024,
        "prune_level": PRUNE_LEVEL,
        "temporal_bucket_seconds": TEMPORAL_BUCKET_SECONDS,
        "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
    }


if __name__ == "__main__":
    print(json.dumps(ingest_health_history(), ensure_ascii=False, indent=2))
