# spotify_ingest.py
# -----------------------------------------------------------------------------
# Scopo del file
# -----------------------------------------------------------------------------
# MVP di ingest Spotify: legge i file di input, normalizza/trasforma i dati,
# genera due output JSON:
#  - dataset_minimo.json   (dati minimi, pronti per LLM/analisi rapida)
#  - dataset_full.json     (dataset secondario completo, con metadati e log)
#
# Standard:
#  * tutti i timestamp trasformati in ISO 8601 UTC
#  * tutte le durate conservate in secondi ove possibile
#  * tutti i campi testuali principali in lowercase
#  * device mantenuto separato da media_type
#  * event_number globale per sorgente: spotify_1, spotify_2, ...
#  * duplicati rimossi automaticamente
#  * errori stampati solo in terminale e registrati nel full
#  * dataset_full conserva i dati raw per auditing e analisi approfondite
#
# -----------------------------------------------------------------------------

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


# -----------------------------------------------------------------------------
# Config: percorsi
# -----------------------------------------------------------------------------

try:
    from config import SPOTIFY_INPUT_DIR, SPOTIFY_DATASET_PATH, SPOTIFY_SUMMARY_PATH
except Exception:
    SPOTIFY_INPUT_DIR = Path("Input/Spotify")
    SPOTIFY_DATASET_PATH = Path("Output/spotify_history_dataset_min.json")
    SPOTIFY_SUMMARY_PATH = Path("Output/spotify_history_summary.json")


# -----------------------------------------------------------------------------
# Costanti di comportamento
# -----------------------------------------------------------------------------

SKIP_LIKE_THRESHOLD_MS = 30_000
BEGIN_END_TIMESTAMP_FIELDS = ["ts", "endTime"]


# -----------------------------------------------------------------------------
# Utility: normalizzazione e parsing
# -----------------------------------------------------------------------------

def normalize_string(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def safe_int(value, default=0):
    if value is None:
        return default

    if isinstance(value, bool):
        return int(value)

    try:
        return int(value)
    except Exception:
        try:
            return int(float(str(value)))
        except Exception:
            return default


def to_iso_utc(dt):
    """Converte datetime in ISO 8601 UTC con 'Z' finale."""

    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return (
            dt.astimezone(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )

    return ""


def parse_end_time(value):
    """
    Robusta conversione di una data/ora in ISO8601 UTC.
    Ritorna stringa o ''.
    """

    if value is None:
        return ""

    text = str(value).strip()

    if not text:
        return ""

    # Try direct ISO
    try:
        # Supporta anche timestamp terminanti con Z
        normalized_text = text.replace("Z", "+00:00").replace("z", "+00:00")

        dt = datetime.fromisoformat(normalized_text)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return to_iso_utc(dt)

    except Exception:
        pass

    # Try common formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return to_iso_utc(dt)

        except Exception:
            continue

    return ""


def extract_year_from_filename(path):
    name = Path(path).name

    m = re.search(
        r"_(\d{4})(?:_\d+)?\.json$",
        name,
        re.IGNORECASE
    )

    if not m:
        return 0

    return safe_int(m.group(1), 0)


def detect_media_type(path):
    name = Path(path).name.lower()

    if "streaming_history_audio_" in name:
        return "audio"

    if "streaming_history_video_" in name:
        return "video"

    return "unknown"


# -----------------------------------------------------------------------------
# Parsing: caricamento file
# -----------------------------------------------------------------------------

def load_json_file(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ndjson_file(path):
    records = []

    with Path(path).open("r", encoding="utf-8") as f:

        for idx, line in enumerate(f, start=1):

            s = line.strip()

            if not s:
                continue

            try:
                records.append(json.loads(s))

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"NDJSON error at line {idx}: {exc}"
                ) from exc

    return records


def load_spotify_file(path):

    # Prima prova JSON classico
    try:

        payload = load_json_file(path)

        if isinstance(payload, list):
            return payload

        if (
            isinstance(payload, dict)
            and isinstance(payload.get("records"), list)
        ):
            return payload["records"]

        raise ValueError("JSON structure non riconosciuta.")

    except Exception as json_exc:

        # Poi NDJSON
        try:
            return load_ndjson_file(path)

        except Exception as ndjson_exc:
            raise ValueError(
                f"Failed JSON e NDJSON: "
                f"{json_exc} | {ndjson_exc}"
            ) from ndjson_exc


# -----------------------------------------------------------------------------
# Normalizzazione record Spotify
# -----------------------------------------------------------------------------

def build_record(raw, source_file):
    """
    Trasforma record raw in un dizionario normalizzato.
    """

    if not isinstance(raw, dict):
        raw = {"raw_value": raw}

    source_path = Path(source_file)

    source_year = extract_year_from_filename(source_path)
    media_type = detect_media_type(source_path)

    # -------------------------------------------------------------------------
    # Timestamp
    # -------------------------------------------------------------------------

    ts_candidates = []

    if isinstance(raw, dict):

        if "ts" in raw:
            ts_candidates.append(raw.get("ts"))

        if "endTime" in raw:
            ts_candidates.append(raw.get("endTime"))

        if "timestamp" in raw:
            ts_candidates.append(raw.get("timestamp"))

    end_ts_raw = (
        ts_candidates[0]
        if ts_candidates
        else raw.get("endTime")
        or raw.get("ts")
        or raw.get("timestamp")
        or ""
    )

    end_time_parsed = parse_end_time(end_ts_raw)

    # -------------------------------------------------------------------------
    # Track / Artist / Album
    # -------------------------------------------------------------------------

    artist = normalize_string(
        raw.get("artistName")
        or raw.get("master_metadata_album_artist_name")
    )

    track = normalize_string(
        raw.get("trackName")
        or raw.get("master_metadata_track_name")
    )

    album = normalize_string(
        raw.get("master_metadata_album_album_name")
    )

    # -------------------------------------------------------------------------
    # Duration
    # -------------------------------------------------------------------------

    ms_played = safe_int(
        raw.get(
            "msPlayed",
            raw.get("ms_played", 0)
        ),
        default=0
    )

    played_seconds = round(ms_played / 1000.0, 3)
    played_minutes = round(ms_played / 60000.0, 3)

    # -------------------------------------------------------------------------
    # Device
    #
    # Spotify può fornire "platform" nei dataset.
    # Se non disponibile, fallback sul media_type.
    # -------------------------------------------------------------------------

    device = normalize_string(
        raw.get("platform")
        or raw.get("device")
        or media_type
    )

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    track_identity = f"{artist} - {track}"

    # -------------------------------------------------------------------------
    # Record normalizzato
    # -------------------------------------------------------------------------

    normalized = dict(raw)

    normalized.update({

        "begin_timestamp": "",

        "end_timestamp": end_time_parsed or "",

        "track": track,

        "album": album,

        "artist": artist,

        "device": device,

        "media_type": media_type,

        "played_seconds": played_seconds,

        "played_minutes": played_minutes,

        "source_file": source_path.name,

        "source_year": source_year,

        "record_index_in_source": 0,

        "track_identity": track_identity,

        "raw": raw,

        "event_number": "",

    })

    return normalized


# -----------------------------------------------------------------------------
# Input file detection
# -----------------------------------------------------------------------------

def is_relevant_spotify_history_file(path):

    name = Path(path).name

    return (
        re.match(
            r"^Streaming_History_(Audio|Video)_(\d{4})(?:_(\d+))?\.json$",
            name,
            re.IGNORECASE
        )
        is not None
    )


def collect_input_files(input_dir):

    input_path = Path(input_dir)

    relevant = []
    ignored = []

    if not input_path.exists():
        return relevant, ignored

    for p in input_path.iterdir():

        if not p.is_file():
            continue

        if is_relevant_spotify_history_file(p):
            relevant.append(p)

        else:
            ignored.append(p)

    # Ordinamento deterministico
    relevant.sort(
        key=lambda x: (
            extract_year_from_filename(x),
            detect_media_type(x),
            x.name.lower()
        )
    )

    ignored.sort(
        key=lambda x: x.name.lower()
    )

    return relevant, ignored


# -----------------------------------------------------------------------------
# Deduplicazione
# -----------------------------------------------------------------------------

def get_deduplication_key(record):
    """
    Identifica un ascolto in modo stabile.

    La combinazione timestamp + track + artist + durata
    evita di eliminare ascolti realmente distinti dello stesso brano.
    """

    return (
        record.get("end_timestamp", ""),
        record.get("track", ""),
        record.get("artist", ""),
        safe_int(
            record.get("msPlayed", record.get("ms_played", 0)),
            0
        )
    )


def deduplicate_records(records):
    """
    Rimuove automaticamente record completamente ridondanti.
    Mantiene il primo record incontrato.
    """

    unique_records = []
    seen = set()
    duplicates = 0

    for record in records:

        key = get_deduplication_key(record)

        if key in seen:
            duplicates += 1
            continue

        seen.add(key)
        unique_records.append(record)

    return unique_records, duplicates


# -----------------------------------------------------------------------------
# Output: dataset minimo e dataset completo
# -----------------------------------------------------------------------------

def build_min_record(record, event_number):

    return {
        "begin_timestamp": record.get(
            "begin_timestamp", ""
        ),

        "end_timestamp": record.get(
            "end_timestamp", ""
        ),

        "track": record.get(
            "track", ""
        ),

        "album": record.get(
            "album", ""
        ),

        "artist": record.get(
            "artist", ""
        ),

        "device": record.get(
            "device",
            record.get("media_type", "")
        ),

        "played_seconds": record.get(
            "played_seconds", 0
        ),

        "played_minutes": record.get(
            "played_minutes", 0
        ),

        "event_number": event_number,
    }


def build_full_record(record, include_raw=True):

    full = dict(record)

    if not include_raw:
        full.pop("raw", None)

    # Se raw è vuoto, non serve conservarlo
    if "raw" in full and not full["raw"]:
        full.pop("raw", None)

    # Fallback device
    if "device" not in full:
        full["device"] = full.get("media_type", "")

    return full


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

def log_message(
    logs,
    level,
    message,
    file=None,
    details=None
):

    entry = {
        "level": level,
        "message": str(message),
        "file": str(file) if file else "",
        "details": details or {}
    }

    logs.append(entry)


# -----------------------------------------------------------------------------
# JSON output
# -----------------------------------------------------------------------------

def write_json(path, payload):

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            payload,
            f,
            ensure_ascii=False,
            indent=2
        )


def write_json_gz(path, payload):

    import gzip

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with gzip.open(
        path.as_posix() + ".gz",
        "wt",
        encoding="utf-8"
    ) as f:

        json.dump(
            payload,
            f,
            ensure_ascii=False,
            indent=2
        )


# -----------------------------------------------------------------------------
# Schema
# -----------------------------------------------------------------------------

def build_dataset_schema():

    return {

        "minimum_fields": [
            "begin_timestamp",
            "end_timestamp",
            "track",
            "album",
            "artist",
            "device",
            "played_seconds",
            "played_minutes",
            "event_number"
        ],

        "full_fields": [
            "begin_timestamp",
            "end_timestamp",
            "track",
            "album",
            "artist",
            "device",
            "media_type",
            "played_seconds",
            "played_minutes",
            "source_file",
            "source_year",
            "record_index_in_source",
            "event_number",
            "track_identity",
            "raw"
        ],

        "notes": (
            "dataset_minimo per LLM rapidi; "
            "dataset_full per auditing, analytics "
            "e integrazione avanzata."
        ),

        "timestamp_standard": (
            "ISO 8601 UTC con Z finale"
        ),

        "duration_standard": (
            "secondi come unita principale; "
            "played_minutes mantenuto per compatibilita"
        ),

        "event_number_standard": (
            "identificatore progressivo per sorgente, "
            "es. spotify_1, spotify_2"
        )

    }


# -----------------------------------------------------------------------------
# Timestamp effettivi
# -----------------------------------------------------------------------------

def get_effective_timestamps(rec):

    """
    Determina begin/end.

    Spotify fornisce principalmente il timestamp di fine ascolto
    e la durata in millisecondi.

    begin = end - durata.
    """

    end = rec.get("end_timestamp") or ""

    if not end:
        return "", ""

    end_iso = parse_end_time(end)

    if not end_iso:
        return "", ""

    played_seconds = rec.get(
        "played_seconds",
        0
    )

    try:

        dt_end = datetime.fromisoformat(
            end_iso.replace("Z", "+00:00")
        )

        if dt_end.tzinfo is None:
            dt_end = dt_end.replace(
                tzinfo=timezone.utc
            )

        dt_begin = (
            dt_end
            - timedelta(seconds=float(played_seconds))
        )

        begin = to_iso_utc(dt_begin)

        return begin, end_iso

    except Exception:

        return "", end_iso


# -----------------------------------------------------------------------------
# Ingestione: main entry point
# -----------------------------------------------------------------------------

def ingest_spotify_history():

    """
    Entry point:

    - legge Input/Spotify
    - normalizza/trasforma i record
    - rimuove duplicati
    - ordina cronologicamente
    - assegna event_number spotify_1, spotify_2, ...
    - genera dataset minimo e full
    - stampa/logga gli errori
    """

    relevant_files, ignored_paths = collect_input_files(
        SPOTIFY_INPUT_DIR
    )

    ignored_files = [
        p.name
        for p in ignored_paths
    ]

    if not SPOTIFY_INPUT_DIR.exists():

        print(
            "Warning: Input/Spotify non esiste."
        )

        return {

            "files_found": 0,

            "files_processed": 0,

            "records_min": 0,

            "records_full": 0,

            "outputs": {
                "dataset_min": str(
                    SPOTIFY_DATASET_PATH
                ),
                "dataset_full": str(
                    SPOTIFY_DATASET_PATH
                )
            },

            "summary": {}

        }

    # -------------------------------------------------------------------------
    # Strutture temporanee
    # -------------------------------------------------------------------------

    all_records = []

    logs = []

    errors = []

    event_number_counter = 1

    # -------------------------------------------------------------------------
    # Elaborazione file
    # -------------------------------------------------------------------------

    for source_path in relevant_files:

        try:

            raw_records = load_spotify_file(
                source_path
            )

            if not isinstance(
                raw_records,
                list
            ):
                raise ValueError(
                    "Loaded payload is not a list of records."
                )

            file_minutes = 0.0

            for idx, raw in enumerate(
                raw_records
            ):

                try:

                    rec = build_record(
                        raw,
                        source_path
                    )

                    rec[
                        "record_index_in_source"
                    ] = idx

                    begin_ts, end_ts = (
                        get_effective_timestamps(rec)
                    )

                    rec[
                        "begin_timestamp"
                    ] = begin_ts

                    rec[
                        "end_timestamp"
                    ] = end_ts

                    file_minutes += float(
                        rec.get(
                            "played_minutes",
                            0.0
                        )
                    )

                    all_records.append(rec)

                except Exception as exc:

                    print(
                        f"[error] "
                        f"{source_path.name}: "
                        f"{exc}"
                    )

                    errors.append({

                        "file": source_path.name,

                        "error_type":
                            "record_process_error",

                        "message": str(exc)

                    })

            # File-level log

            logs.append({

                "file": source_path.name,

                "records": len(raw_records),

                "minutes": round(
                    file_minutes,
                    3
                )

            })

        except Exception as exc:

            print(
                f"[error] "
                f"{source_path.name}: "
                f"{exc}"
            )

            errors.append({

                "file": source_path.name,

                "error_type":
                    "file_load_error",

                "message": str(exc)

            })

    # -------------------------------------------------------------------------
    # Deduplicazione
    # -------------------------------------------------------------------------

    records_unique, duplicates_removed = (
        deduplicate_records(all_records)
    )

    # -------------------------------------------------------------------------
    # Ordinamento cronologico
    #
    # I record vengono ordinati PRIMA di assegnare event_number.
    # In questo modo spotify_1 è sempre il primo evento cronologico.
    # -------------------------------------------------------------------------

    records_unique.sort(
        key=lambda x: (
            x.get(
                "end_timestamp",
                ""
            ),
            x.get(
                "begin_timestamp",
                ""
            ),
            x.get(
                "record_index_in_source",
                0
            )
        )
    )

    # -------------------------------------------------------------------------
    # Assegnazione event_number
    # -------------------------------------------------------------------------

    records_min = []
    records_full = []

    for rec in records_unique:

        event_number = (
            f"spotify_{event_number_counter}"
        )

        event_number_counter += 1

        rec[
            "event_number"
        ] = event_number

        records_min.append(
            build_min_record(
                rec,
                event_number
            )
        )

        records_full.append(
            build_full_record(
                rec,
                include_raw=True
            )
        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    generated_at = to_iso_utc(
        datetime.now(timezone.utc)
    )

    # -------------------------------------------------------------------------
    # Dataset minimo
    # -------------------------------------------------------------------------

    dataset_min = {

        "_metadata": {

            "dataset_name":
                "spotify_history_dataset_min",

            "generated_at":
                generated_at,

            "script_name":
                "spotify_ingest.py",

            "description": (
                "Dataset minimo per analisi rapide "
                "e LLM su Raspberry Pi. "
                "Contiene gli attributi essenziali "
                "degli ascolti Spotify."
            )

        },

        "_schema":
            build_dataset_schema(),

        "records":
            records_min

    }

    # -------------------------------------------------------------------------
    # Dataset full
    # -------------------------------------------------------------------------

    dataset_full = {

        "_metadata": {

            "dataset_name":
                "spotify_history_dataset_full",

            "generated_at":
                generated_at,

            "script_name":
                "spotify_ingest.py",

            "description": (
                "Dataset completo con metadata, "
                "raw data, log ed errori. "
                "Utilizzato per auditing, analytics "
                "e integrazione avanzata."
            )

        },

        "_schema": {

            "fields": [
                "begin_timestamp",
                "end_timestamp",
                "track",
                "album",
                "artist",
                "device",
                "media_type",
                "played_seconds",
                "played_minutes",
                "source_file",
                "source_year",
                "record_index_in_source",
                "event_number",
                "track_identity",
                "raw"
            ]

        },

        "records":
            records_full,

        "logs":
            logs,

        "warnings":
            [],

        "errors":
            errors,

        "summary":
            {}

    }

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    min_path = Path(
        SPOTIFY_DATASET_PATH
    )

    full_path = (
        min_path.with_name(
            "spotify_history_dataset_full.json"
        )
    )

    summary = {

        "files_found":
            len(relevant_files),

        "files_ignored":
            ignored_files,

        "records_raw":
            len(all_records),

        "duplicates_removed":
            duplicates_removed,

        "records_min":
            len(records_min),

        "records_full":
            len(records_full),

        "minutes_total":
            round(
                sum(
                    r.get(
                        "played_minutes",
                        0.0
                    )
                    for r in records_full
                ),
                3
            ),

        "seconds_total":
            round(
                sum(
                    r.get(
                        "played_seconds",
                        0.0
                    )
                    for r in records_full
                ),
                3
            ),

        "datasets": {

            "min":
                str(min_path),

            "full":
                str(full_path),

            "summary":
                str(SPOTIFY_SUMMARY_PATH)

        }

    }

    dataset_full[
        "summary"
    ] = summary

    # -------------------------------------------------------------------------
    # Scrittura output
    # -------------------------------------------------------------------------

    write_json(
        min_path,
        dataset_min
    )

    write_json(
        full_path,
        dataset_full
    )

    # Summary separato
    write_json(
        Path(SPOTIFY_SUMMARY_PATH),
        summary
    )

    # -------------------------------------------------------------------------
    # Result
    # -------------------------------------------------------------------------

    result = {

        "success":
            True,

        "input_directory":
            str(SPOTIFY_INPUT_DIR),

        "output_directory":
            str(Path("Output")),

        "files_found":
            len(relevant_files),

        "files_processed":
            len(relevant_files),

        "records_processed_raw":
            len(all_records),

        "duplicates_removed":
            duplicates_removed,

        "records_processed_min":
            len(records_min),

        "records_processed_full":
            len(records_full),

        "outputs": {

            "dataset_min":
                str(min_path),

            "dataset_full":
                str(full_path),

            "summary":
                str(SPOTIFY_SUMMARY_PATH)

        },

        "stats": {

            "total_files":
                len(relevant_files),

            "total_records_raw":
                len(all_records),

            "total_duplicates_removed":
                duplicates_removed,

            "total_records_min":
                len(records_min),

            "total_records_full":
                len(records_full),

            "total_minutes":
                round(
                    sum(
                        r.get(
                            "played_minutes",
                            0.0
                        )
                        for r in records_full
                    ),
                    3
                ),

            "total_seconds":
                round(
                    sum(
                        r.get(
                            "played_seconds",
                            0.0
                        )
                        for r in records_full
                    ),
                    3
                )

        },

        "errors":
            errors,

        "logs":
            logs,

        "file_reports":
            []

    }

    return result


# -----------------------------------------------------------------------------
# Esecuzione diretta
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    res = ingest_spotify_history()

    if res.get(
        "files_found",
        0
    ) == 0:

        print(
            "Nessun file valido trovato "
            "in Input/Spotify. "
            "Copia i file e riprova."
        )

    else:

        print(
            "Ingest completato."
        )

        print(
            f"Dataset_min: "
            f"{res['outputs']['dataset_min']}"
        )

        print(
            f"Dataset_full: "
            f"{res['outputs']['dataset_full']}"
        )

        print(
            f"Summary: "
            f"{res['outputs']['summary']}"
        )

        print(
            f"Record elaborati: "
            f"{res['records_processed_raw']}"
        )

        print(
            f"Duplicati rimossi: "
            f"{res['duplicates_removed']}"
        )

        print(
            f"Record finali: "
            f"{res['records_processed_min']}"
        )