# loader.py
import json
from pathlib import Path
from typing import List, Dict, Tuple

DATA_PATH = Path(__file__).parent / "data" / "italian_articles.json"
FALLBACK = [
    {"id":"fb-1","word":"casa","language":"it","correct_article":"la"},
    {"id":"fb-2","word":"libro","language":"it","correct_article":"il"},
    {"id":"fb-3","word":"amico","language":"it","correct_article":"l'"}
]
DATASET_VERSION = "1.0"

def load_dataset(path: Path = DATA_PATH) -> Tuple[List[Dict], str]:
    """
    Load dataset from local JSON file. If file missing or invalid, return fallback.
    Returns (dataset, version)
    """
    try:
        if not path.exists():
            return FALLBACK, "fallback"
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or len(raw) == 0:
            return FALLBACK, "fallback"
        # Basic validation: ensure required fields
        validated = []
        for it in raw:
            if not isinstance(it.get("word"), str) or not isinstance(it.get("correct_article"), str):
                continue
            validated.append(it)
        if len(validated) == 0:
            return FALLBACK, "fallback"
        return validated, DATASET_VERSION
    except Exception as e:
        # Log exception as needed; return fallback
        return FALLBACK, "fallback"