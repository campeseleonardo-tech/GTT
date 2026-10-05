from __future__ import annotations

import importlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple


try:
    from config import BASE_DIR, INPUT_DIR, OUTPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "Input"
    OUTPUT_DIR = BASE_DIR / "Output"


def estimate_json_size_bytes(payload: Any) -> int:
    return len(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    )


def write_json(path: Path, payload: Dict[str, Any]) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=False,
            separators=(",", ":"),
            default=str,
        )
    return path.stat().st_size


def check_full_size_warning(full_size_bytes: int, warning_gb: float = 0.5) -> Optional[str]:
    threshold_bytes = warning_gb * (1024 ** 3)
    if full_size_bytes > threshold_bytes:
        size_gb = full_size_bytes / (1024 ** 3)
        return (
            f"FULL dataset is approximately {size_gb:.2f} GB, over the "
            f"{warning_gb} GB warning threshold. Consider a more "
            f"aggressive prune_level if this becomes a recurring issue."
        )
    return None


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


CONFIDENCE_NATIVE = 1.0
CONFIDENCE_INFERRED_HIGH = 0.8
CONFIDENCE_INFERRED_MEDIUM = 0.5
CONFIDENCE_INFERRED_LOW = 0.2

_VALID_CONFIDENCE_VALUES = {
    CONFIDENCE_NATIVE,
    CONFIDENCE_INFERRED_HIGH,
    CONFIDENCE_INFERRED_MEDIUM,
    CONFIDENCE_INFERRED_LOW,
}


def confidence_rate(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    if value not in _VALID_CONFIDENCE_VALUES:
        raise ValueError(
            f"confidence_rate must be one of {sorted(_VALID_CONFIDENCE_VALUES)} "
            f"or None, got {value!r}. See timelive.md §27 for the standard scale."
        )
    return value


def compute_notability_scores(
    records: Sequence[Dict[str, Any]],
    weight_functions: Dict[str, Callable[[Dict[str, Any]], float]],
    weights: Dict[str, float],
    score_field: str = "notability_score",
) -> None:
    for record in records:
        score = 0.0
        for signal_name, weight in weights.items():
            fn = weight_functions.get(signal_name)
            if fn is None:
                continue
            try:
                score += weight * float(fn(record))
            except Exception:
                continue
        record[score_field] = round(score, 6)


def recency_weight(
    timestamp_iso: Optional[str],
    half_life_days: float,
    now: Optional[datetime] = None,
) -> float:
    ts = _parse_iso(timestamp_iso)
    if ts is None or half_life_days <= 0:
        return 0.0
    now = now or datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    age_days = max((now - ts).total_seconds() / 86400.0, 0.0)
    return 0.5 ** (age_days / half_life_days)


def select_within_size_budget(
    candidates: Sequence[Dict[str, Any]],
    target_bytes: Optional[int],
    soft_overflow_ratio: float = 0.10,
    rank_field: str = "notability_score",
    always_include_bytes: int = 0,
) -> List[Dict[str, Any]]:
    ranked = sorted(candidates, key=lambda r: r.get(rank_field, 0.0), reverse=True)

    if not target_bytes:
        return ranked

    overflow_bytes = target_bytes * soft_overflow_ratio
    selected: List[Dict[str, Any]] = []
    current_size = always_include_bytes

    for item in ranked:
        item_size = estimate_json_size_bytes(item)
        if current_size + item_size > target_bytes + overflow_bytes:
            break
        selected.append(item)
        current_size += item_size
        if current_size > target_bytes:
            break

    return selected


def deduplicate_records(
    records: Sequence[Dict[str, Any]],
    native_id_field: Optional[str],
    composite_key_fn: Callable[[Dict[str, Any]], Tuple],
) -> Tuple[List[Dict[str, Any]], int]:
    seen: set = set()
    result: List[Dict[str, Any]] = []
    duplicates_removed = 0

    for record in records:
        native_id = record.get(native_id_field) if native_id_field else None
        key = ("native", native_id) if native_id else ("composite", composite_key_fn(record))

        if key in seen:
            duplicates_removed += 1
            continue

        seen.add(key)
        result.append(record)

    return result, duplicates_removed


def group_by_time_and_compatibility(
    events: Sequence[Dict[str, Any]],
    timestamp_begin_field: str,
    timestamp_end_field: str,
    max_gap_seconds: float,
    is_compatible: Callable[[Dict[str, Any], Dict[str, Any]], bool],
) -> List[List[Dict[str, Any]]]:
    groups: List[List[Dict[str, Any]]] = []
    current_group: List[Dict[str, Any]] = []

    for event in events:
        if not current_group:
            current_group = [event]
            continue

        previous = current_group[-1]
        prev_end = _parse_iso(previous.get(timestamp_end_field) or previous.get(timestamp_begin_field))
        curr_begin = _parse_iso(event.get(timestamp_begin_field))
        gap_seconds = (curr_begin - prev_end).total_seconds() if (prev_end and curr_begin) else math.inf

        if gap_seconds <= max_gap_seconds and is_compatible(previous, event):
            current_group.append(event)
        else:
            groups.append(current_group)
            current_group = [event]

    if current_group:
        groups.append(current_group)

    return groups


def build_metadata(
    dataset_name: str,
    source: str,
    version: str,
    purpose: str,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {
        "dataset": dataset_name,
        "source": source,
        "version": version,
        "purpose": purpose,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        metadata.update(extra)
    return metadata


def build_schema(
    sections: Dict[str, str],
    field_notes: Optional[Dict[str, str]] = None,
    conventions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "sections": sections,
        "field_notes": field_notes or {},
        "conventions": conventions or [],
    }


def build_logic(
    normalization: str,
    deduplication: str,
    classification: str,
    pruning: str,
    grouping: Optional[str] = None,
    pattern_detection: Optional[str] = None,
    primary_full_relationship: str = (
        "PRIMARY is a notability-ranked, size-budgeted subset of the same "
        "processed data as FULL. Every PRIMARY record that has a fuller "
        "counterpart carries id_full_ref to retrieve it from FULL."
    ),
    interpretation_notes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "normalization": normalization,
        "deduplication": deduplication,
        "classification": classification,
        "pruning": pruning,
        "grouping": grouping,
        "pattern_detection": pattern_detection,
        "primary_full_relationship": primary_full_relationship,
        "interpretation_notes": interpretation_notes or [],
    }


INGEST_REGISTRY: List[Tuple[str, str, str]] = [
    ("spotify", "spotify_ingest", "ingest_spotify_history"),
    ("apple_health", "health_ingest", "ingest_health_history"),
    ("bank", "money_ingest", "ingest_bank_history"),
    ("maps", "maps_ingest", "ingest_maps_history"),
    ("whatsapp", "whatsapp_ingest", "ingest_whatsapp_history"),
    ("chessdotcom", "chessdotcom_ingest", "ingest_chessdotcom_history"),
]


def run_all_ingests(
    enabled_domains: Optional[Sequence[str]] = None,
    disabled_domains: Optional[Sequence[str]] = None,
    domain_overrides: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    overrides = domain_overrides or {}

    for domain_name, module_name, entrypoint_name in INGEST_REGISTRY:
        if enabled_domains is not None and domain_name not in enabled_domains:
            results[domain_name] = {"success": True, "status": "skipped", "reason": "not in enabled_domains"}
            continue
        if disabled_domains is not None and domain_name in disabled_domains:
            results[domain_name] = {"success": True, "status": "skipped", "reason": "in disabled_domains"}
            continue

        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            results[domain_name] = {
                "success": False,
                "status": "not_available",
                "reason": str(exc),
            }
            continue

        entrypoint = getattr(module, entrypoint_name, None)
        if entrypoint is None:
            results[domain_name] = {
                "success": False,
                "status": "entrypoint_missing",
                "reason": f"{module_name} has no function named {entrypoint_name}",
            }
            continue

        try:
            results[domain_name] = entrypoint(enabled=True, **overrides.get(domain_name, {}))
        except TypeError as exc:
            results[domain_name] = {
                "success": False,
                "status": "override_unsupported",
                "reason": str(exc),
            }
        except Exception as exc:
            results[domain_name] = {
                "success": False,
                "status": "failed",
                "reason": str(exc),
            }

    return results


if __name__ == "__main__":
    outcome = run_all_ingests()
    print(json.dumps(outcome, ensure_ascii=False, default=str))
    print()
    for domain, result in outcome.items():
        status = "OK" if result.get("success") else result.get("status", "FAILED")
        print(f"{domain}: {status}")
