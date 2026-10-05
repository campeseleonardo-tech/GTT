# test_smoke.py
# =============================================================================
# FAST SMOKE TEST — Personal Data Vault
# =============================================================================
#
# WHY THIS EXISTS
# -----------------------------------------------------------------------
# Running the real ingests against real exports (which can be hundreds of
# thousands of records) is slow and gives no useful signal about whether a
# code change is *correct* — by the time it finishes, you've lost your
# train of thought. This script instead:
#
#   1. builds tiny synthetic input files (a handful of records per domain)
#      in a throwaway temp folder,
#   2. runs each ingest directly against them,
#   3. checks a short list of structural invariants that matter (exactly
#      two output files, confidence_rate on the fixed standard scale,
#      required blocks present, etc.),
#   4. prints a clear PASS/FAIL per domain and exits non-zero on failure
#      (so it can be wired into a pre-commit hook or CI later if wanted).
#
# It does NOT replace running against real data — it only tells you "the
# pipeline is not obviously broken" in under a second, so you can iterate
# fast and save the slow real run for when the smoke test is green.
#
# HOW TO RUN
# -----------------------------------------------------------------------
#   Place this file in the same folder as main.py, money_ingest.py,
#   spotify_ingest.py, health_ingest.py (your "code" folder), then:
#
#       python3 test_smoke.py
#
#   No config.py or config.json is needed — this script points every
#   ingest at its own temporary Input/Output folders directly, so it never
#   touches your real Input/Output directories.
# =============================================================================

import importlib
import json
import shutil
import sys
import tempfile
import time
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

FAILURES = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


VALID_CONFIDENCE_VALUES = {1.0, 0.8, 0.5, 0.2, None}


def check_confidence_rates(obj, path="root"):
    """Recursively finds every 'confidence_rate' key and checks it is on
    the fixed standard scale (timelive.md §27), wherever it appears."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if "confidence_rate" in key and value not in VALID_CONFIDENCE_VALUES:
                check(False, f"{path}.{key} = {value!r} is not on the fixed confidence_rate scale")
            check_confidence_rates(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            check_confidence_rates(item, f"{path}[{i}]")


# =============================================================================
# MONEY
# =============================================================================

def test_money(tmp_root: Path):
    section("MONEY_INGEST")
    input_dir = tmp_root / "Input" / "Bank"
    output_dir = tmp_root / "Output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    # A handful of transactions: one recurring (Netflix x3), one salary
    # (keyword classification), one cash withdrawal (keyword), one
    # unusually large one (anomaly), enough to exercise every code path
    # without needing thousands of rows.
    (input_dir / "generic.csv").write_text(
        "Date,Description,Amount,Currency,Beneficiary\n"
        "01/08/2026,Netflix subscription,-12.99,EUR,Netflix\n"
        "01/07/2026,Netflix subscription,-12.99,EUR,Netflix\n"
        "01/06/2026,Netflix subscription,-12.99,EUR,Netflix\n"
        "05/08/2026,Stipendio Agosto,2100.00,EUR,Employer\n"
        "10/08/2026,ATM WITHDRAWAL,-100.00,EUR,\n"
        "12/08/2026,Big purchase,-5000.00,EUR,Luxury Store\n",
        encoding="utf-8",
    )

    import money_ingest
    importlib.reload(money_ingest)
    money_ingest.BANK_INPUT_DIR = input_dir
    money_ingest.BANK_OUTPUT_DATASET_PATH = output_dir / "bank_dataset.json"
    money_ingest.BANK_OUTPUT_FULL_DATASET_PATH = output_dir / "bank_dataset_full.json"

    t0 = time.time()
    result = money_ingest.ingest_bank_history()
    elapsed = time.time() - t0
    print(f"ran in {elapsed:.3f}s -> {result.get('records_processed')} records, "
          f"{result.get('recurring_patterns_found')} recurring pattern(s)")

    check(result.get("success") is True, "money: ingest did not report success")
    check(result.get("records_processed") == 6, f"money: expected 6 records, got {result.get('records_processed')}")
    check(result.get("recurring_patterns_found", 0) >= 1, "money: Netflix recurring pattern not detected")

    primary_path = output_dir / "bank_dataset.json"
    full_path = output_dir / "bank_dataset_full.json"
    check(primary_path.exists(), "money: bank_dataset.json was not written")
    check(full_path.exists(), "money: bank_dataset_full.json was not written")
    check(
        set(output_dir.glob("bank_dataset*.json")) == {primary_path, full_path},
        "money: found extra bank_dataset* files -- exactly two are required (timelive.md §11)",
    )

    full = json.loads(full_path.read_text(encoding="utf-8"))
    for block in ("_metadata", "_schema", "_logic"):
        check(block in full, f"money FULL: missing {block}")
    check(len(full.get("recurring_transactions", [])) >= 1, "money FULL: no recurring_transactions")
    check_confidence_rates(full, "money.full")

    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    check("notable_transactions" in primary, "money PRIMARY: missing notable_transactions")
    check(len(primary.get("notable_transactions", [])) > 0, "money PRIMARY: notable_transactions is empty")


# =============================================================================
# SPOTIFY
# =============================================================================

def test_spotify(tmp_root: Path):
    section("SPOTIFY_INGEST")
    input_dir = tmp_root / "Input" / "Spotify"
    output_dir = tmp_root / "Output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    base = datetime.now(timezone.utc) - timedelta(days=1)
    plays = []
    t = base
    for artist, track, ms in [
        ("Artist A", "Track One", 210_000),
        ("Artist A", "Track Two", 15_000),   # skip-like
        ("Artist B", "Track Three", 240_000),
    ]:
        t = t + timedelta(seconds=ms / 1000 + 5)
        plays.append({
            "ts": t.isoformat().replace("+00:00", "Z"),
            "master_metadata_album_artist_name": artist,
            "master_metadata_track_name": track,
            "ms_played": ms,
            "platform": "android",
        })
    (input_dir / "Streaming_History_Audio_2026_0.json").write_text(json.dumps(plays), encoding="utf-8")

    import spotify_ingest
    importlib.reload(spotify_ingest)
    spotify_ingest.SPOTIFY_INPUT_DIR = input_dir
    spotify_ingest.SPOTIFY_OUTPUT_DATASET_PATH = output_dir / "spotify_dataset.json"
    spotify_ingest.SPOTIFY_OUTPUT_FULL_DATASET_PATH = output_dir / "spotify_dataset_full.json"

    t0 = time.time()
    result = spotify_ingest.ingest_spotify_history()
    elapsed = time.time() - t0
    print(f"ran in {elapsed:.3f}s -> {result.get('records_processed')} plays, "
          f"{result.get('sessions_detected')} session(s)")

    check(result.get("success") is True, "spotify: ingest did not report success")
    check(result.get("records_processed") == 3, f"spotify: expected 3 plays, got {result.get('records_processed')}")
    check(result.get("sessions_detected", 0) >= 1, "spotify: expected at least 1 session (3 back-to-back plays)")

    primary_path = output_dir / "spotify_dataset.json"
    full_path = output_dir / "spotify_dataset_full.json"
    check(primary_path.exists(), "spotify: spotify_dataset.json was not written")
    check(full_path.exists(), "spotify: spotify_dataset_full.json was not written")
    check(
        set(output_dir.glob("spotify_dataset*.json")) == {primary_path, full_path},
        "spotify: found extra spotify_dataset* files -- exactly two are required (timelive.md §11)",
    )

    full = json.loads(full_path.read_text(encoding="utf-8"))
    for block in ("_metadata", "_schema", "_logic"):
        check(block in full, f"spotify FULL: missing {block}")
    check_confidence_rates(full, "spotify.full")

    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    check("notable_plays" in primary, "spotify PRIMARY: missing notable_plays")


# =============================================================================
# HEALTH
# =============================================================================

def test_health(tmp_root: Path):
    section("HEALTH_INGEST")
    input_dir = tmp_root / "Input" / "AppleHealth"
    output_dir = tmp_root / "Output"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    def fmt(d):
        return d.strftime("%Y-%m-%d %H:%M:%S +0000")

    base = datetime(2026, 8, 20, 7, 0, 0, tzinfo=timezone.utc)
    run_start, run_end = base, base + timedelta(minutes=30)
    sleep_start, sleep_end = base - timedelta(hours=8), base - timedelta(minutes=30)

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<HealthData locale="en_US">
<Workout workoutActivityType="HKWorkoutActivityTypeRunning" duration="30" durationUnit="min" sourceName="Apple Watch" startDate="{fmt(run_start)}" endDate="{fmt(run_end)}"/>
<Record type="HKQuantityTypeIdentifierHeartRate" sourceName="Apple Watch" unit="count/min" startDate="{fmt(run_start)}" endDate="{fmt(run_start)}" value="140"/>
<Record type="HKQuantityTypeIdentifierStepCount" sourceName="Apple Watch" unit="count" startDate="{fmt(run_start)}" endDate="{fmt(run_end)}" value="4000"/>
<Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Apple Watch" startDate="{fmt(sleep_start)}" endDate="{fmt(sleep_end)}" value="1"/>
</HealthData>
'''
    export_path = input_dir / "export.xml"
    export_path.write_text(xml, encoding="utf-8")

    import health_ingest
    importlib.reload(health_ingest)
    health_ingest.HEALTH_INPUT_FILE = export_path
    health_ingest.HEALTH_OUTPUT_DATASET_PATH = output_dir / "applehealth_dataset.json"
    health_ingest.HEALTH_OUTPUT_FULL_DATASET_PATH = output_dir / "applehealth_dataset_full.json"

    t0 = time.time()
    result = health_ingest.ingest_health_history()
    elapsed = time.time() - t0
    print(f"ran in {elapsed:.3f}s -> {result.get('records_after_deduplication')} records, "
          f"{result.get('sessions')} session(s)")

    check(result.get("success") is True, "health: ingest did not report success")
    check(result.get("sessions", 0) >= 2, f"health: expected at least 2 sessions (run + sleep), got {result.get('sessions')}")

    primary_path = output_dir / "applehealth_dataset.json"
    full_path = output_dir / "applehealth_dataset_full.json"
    check(primary_path.exists(), "health: applehealth_dataset.json was not written")
    check(full_path.exists(), "health: applehealth_dataset_full.json was not written")
    check(
        set(output_dir.glob("applehealth_dataset*.json")) == {primary_path, full_path},
        "health: found extra applehealth_dataset* files -- exactly two are required (timelive.md §11)",
    )

    full = json.loads(full_path.read_text(encoding="utf-8"))
    for block in ("_metadata", "_schema", "_logic"):
        check(block in full, f"health FULL: missing {block}")
    activity_types = {s.get("activity_type") for s in full.get("sessions", [])}
    check("running" in activity_types, f"health: no 'running' session found, got {activity_types}")
    check("sleep" in activity_types, f"health: no 'sleep' session found, got {activity_types}")
    check_confidence_rates(full, "health.full")

    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    check("sessions" in primary, "health PRIMARY: missing sessions")


# =============================================================================
# MAIN ORCHESTRATION
# =============================================================================

def test_main_orchestration(code_dir: Path):
    section("MAIN.PY ORCHESTRATION")
    import main
    importlib.reload(main)
    t0 = time.time()
    outcome = main.run_all_ingests()
    elapsed = time.time() - t0
    print(f"ran in {elapsed:.3f}s")
    for domain, res in outcome.items():
        print(f"  {domain}: {'OK' if res.get('success') else res.get('status', 'FAILED')}")
    check(isinstance(outcome, dict) and len(outcome) == 3, "main: run_all_ingests did not return all 3 domains")


def main_test_runner():
    code_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(code_dir))

    tmp_root = Path(tempfile.mkdtemp(prefix="pdv_smoke_"))
    print(f"Using throwaway temp folder: {tmp_root}")

    try:
        test_money(tmp_root)
    except Exception:
        FAILURES.append("money: raised an exception -- see traceback above")
        traceback.print_exc()

    try:
        test_spotify(tmp_root)
    except Exception:
        FAILURES.append("spotify: raised an exception -- see traceback above")
        traceback.print_exc()

    try:
        test_health(tmp_root)
    except Exception:
        FAILURES.append("health: raised an exception -- see traceback above")
        traceback.print_exc()

    try:
        test_main_orchestration(code_dir)
    except Exception:
        FAILURES.append("main: raised an exception -- see traceback above")
        traceback.print_exc()

    shutil.rmtree(tmp_root, ignore_errors=True)

    section("RESULT")
    if FAILURES:
        print(f"{len(FAILURES)} CHECK(S) FAILED:\n")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED.")
        sys.exit(0)


if __name__ == "__main__":
    main_test_runner()