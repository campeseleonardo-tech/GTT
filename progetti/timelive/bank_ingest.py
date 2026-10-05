# bank_ingest.py - MVP: Ingestione transazioni bancarie da MeinElba
"""
Scopo:
- Transformare le transazioni bancarie esportate (CSV) in un dataset JSON auto-documentato
- Supportare pruning minimo per campi essenziali: data, importo, valuta, destinatario, riferimento, fonte
- Produrre output deterministico in Output/: bank_history_dataset.json e bank_history_summary.json

Nota:
- Il design segue l'architettura di spotify_ingest.py per coerenza e facilità di estensione.
- Attiva pruning in-script tramite PRUNE_ACTIVE/PRUNE_KEEP_FIELDS, con fallback se non presenti in config.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Import config (percorsi e nomi file). Se config non disponibile, usa fallback.
try:
    from config import (
        PRUNE_ACTIVE,
        PRUNE_KEEP_FIELDS,
        SPOTIFY_DATASET_PATH,  # conservato per coerenza, non utilizzato direttamente
        BANK_INPUT_FILENAME,
        BANK_OUTPUT_DATASET_FILENAME,
        BANK_OUTPUT_SUMMARY_FILENAME,
        OUTPUT_DIR,
        INPUT_BANK_DIR,
        SOURCE_NAME,
    )
except Exception:
    PRUNE_ACTIVE = False
    PRUNE_KEEP_FIELDS = ["source_file", "source_year", "record_index_in_source", "date_parsed", "amount", "currency", "recipient"]
    BANK_INPUT_FILENAME = "meinElba_transactions_...csv"
    BANK_OUTPUT_DATASET_FILENAME = "bank_history_dataset.json"
    BANK_OUTPUT_SUMMARY_FILENAME = "bank_history_summary.json"
    OUTPUT_DIR = Path(r"C:\Users\campe\Desktop\Timelive\Output")
    INPUT_BANK_DIR = Path(r"C:\Users\campe\Desktop\Timelive\Input\Bank")
    SOURCE_NAME = "bank"

# Preparazione directory di output
OUTPUT_DIR = Path(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Percorso input effettivo
INPUT_BANK_DIR = Path(INPUT_BANK_DIR)

# Campi di base per i record normalizzati
BASE_FIELDS = [
    "source_file",
    "source_year",
    "record_index_in_source",
    "date_parsed",
    "end_time_parsed",
    "amount",
    "currency",
    "recipient",
    "description",
    "media_type",
]

# Funzione di pruning in-script (minimo MVP)
def apply_pruning(record: Dict[str, Any]) -> Dict[str, Any]:
    if not PRUNE_ACTIVE:
        return record
    pruned: Dict[str, Any] = {}
    for k in PRUNE_KEEP_FIELDS:
        if k in record:
            pruned[k] = record[k]
    # Always preserve audit fields if missing
    for k in ["source_file", "source_year", "record_index_in_source"]:
        pruned.setdefault(k, record.get(k))
    return pruned

# Parsing di una riga CSV: robusto ma semplice
def parse_line(line: List[str]) -> Dict[str, Any] | None:
    if len(line) < 6:
        return None

    raw_date = line[0].strip()
    description = line[1].strip().strip('"')
    second_date = line[2].strip()
    amount_str = line[3].strip().replace('.', '').replace(',', '.')  # 23,80 -> 23.80
    currency = line[4].strip()
    end_time_str = line[5].strip()

    # Date/time parsing
    date_parsed = None
    end_time_parsed = None
    try:
        date_parsed = datetime.strptime(raw_date, "%d.%m.%Y")
    except Exception:
        pass
    try:
        end_time_parsed = datetime.strptime(end_time_str, "%d.%m.%Y %H:%M:%S:%f")
    except Exception:
        try:
            end_time_parsed = datetime.strptime(end_time_str, "%d.%m.%Y %H:%M:%S")
        except Exception:
            end_time_parsed = None

    # Destinatario/descrizione
    recipient = "Unknown"
    if "Payment recipient:" in description:
        recipient = description.split("Payment recipient:", 1)[1].split(";", 1)[0].strip()
    elif "Recipient:" in description:
        recipient = description.split("Recipient:", 1)[1].split(";", 1)[0].strip()
    elif "ONLINE BANKING" in description.upper():
        recipient = description

    # Importo
    try:
        amount = float(amount_str) if amount_str else 0.0
    except Exception:
        try:
            amount = float(str(amount_str).replace(",", "."))
        except Exception:
            amount = 0.0

    record: Dict[str, Any] = {
        "source_file": "meinElba_transactions_...csv",
        "source_year": date_parsed.year if date_parsed else None,
        "record_index_in_source": None,
        "date_parsed": date_parsed.isoformat() if date_parsed else None,
        "end_time_parsed": end_time_parsed.isoformat() if end_time_parsed else None,
        "amount": amount,
        "currency": currency,
        "recipient": recipient,
        "description": description,
        "media_type": "bank_transaction",
    }
    return record

def load_bank_file(path: Path) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";", quotechar='"')
            for idx, row in enumerate(reader):
                if not row or all(not cell.strip() for cell in row):
                    continue
                rec = parse_line(row)
                if rec:
                    rec["record_index_in_source"] = idx
                    records.append(rec)
    except Exception as e:
        # Ritorno un record di errore per logging a valle
        records.append({
            "source_file": path.name,
            "record_index_in_source": None,
            "date_parsed": None,
            "end_time_parsed": None,
            "amount": None,
            "currency": None,
            "recipient": None,
            "description": f"ERRORE DI LETTURA: {e}",
            "media_type": "bank_transaction",
        })
    return records

def collect_input_files(input_dir: Path) -> List[Path]:
    if not input_dir.exists():
        return []
    files = sorted(input_dir.glob("*.csv"))
    return files

def build_dataset_payload(records: List[Dict[str, Any]] , file_reports=None, ignored_files=None, errors=None, warnings=None) -> Dict[str, Any]:
    payload = {
        "_metadata": {
            "dataset_name": SOURCE_NAME,
            "generated_by": "bank_ingest.py MVP",
            "version": "0.1",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "_schema": {
            "fields": BASE_FIELDS,
        },
        "records": records,
        "_field_examples": {
            "date_parsed": "2023-08-01T00:00:00",
            "amount": 23.80,
            "currency": "EUR",
        },
        "top_analyses": {},
    }
    return payload

def write_json(path: Path, payload: Dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

def ingest_bank_history() -> Dict[str, Any]:
    input_files = collect_input_files(INPUT_BANK_DIR)
    all_records: List[Dict[str, Any]] = []
    if not input_files:
        return {
            "status": "skipped",
            "reason": f"Nessun file CSV trovato in {INPUT_BANK_DIR}",
            "files_found": 0,
            "files_processed": 0,
            "records_processed": 0,
            "outputs": {},
            "errors": [],
            "warnings": [],
            "ignored_files": []
        }

    for file_path in input_files:
        recs = load_bank_file(file_path)
        for r in recs:
            r["source_file"] = file_path.name
        all_records.extend(recs)

    # Pruning (in-script) se attivo
    pruned_records = [apply_pruning(r) for r in all_records]

    dataset_payload = build_dataset_payload(pruned_records)

    bank_dataset_path = OUTPUT_DIR / BANK_OUTPUT_DATASET_FILENAME
    bank_summary_path = OUTPUT_DIR / BANK_OUTPUT_SUMMARY_FILENAME

    write_json(bank_dataset_path, dataset_payload)

    # Sommario minimale
    total = sum((r.get("amount") or 0.0) for r in pruned_records)
    top_recipients = {}
    for r in pruned_records:
        k = r.get("recipient")
        top_recipients[k] = top_recipients.get(k, 0.0) + (r.get("amount") or 0.0)

    summary = {
        "_metadata": dataset_payload.get("_metadata"),
        "total_amount": total,
        "top_recipients": top_recipients,
        "records_count": len(pruned_records),
    }
    write_json(bank_summary_path, summary)

    return {
        "status": "ok",
        "records": len(pruned_records),
        "dataset_path": str(bank_dataset_path),
        "summary_path": str(bank_summary_path),
        "files_found": len(input_files),
        "files_processed": len(input_files),
        "outputs": {
            "dataset": str(bank_dataset_path),
            "summary": str(bank_summary_path),
        },
    }

if __name__ == "__main__":
    result = ingest_bank_history()
    print(result)
