# -*- coding: utf-8 -*-
"""T01 - Pulizia della cartella Langue (script del runner, nessun agente).
Regole: nulla viene cancellato, solo SPOSTATO in archivio/vecchio_codice/ (git tiene la storia).
Il file dati principale words_db.json resta dov'e' e il suo hash prima/dopo deve coincidere."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import repo_tools as rt

repo = Path(sys.argv[1])
KEEP = repo / "words_db.json"
DEST = repo / "archivio" / "vecchio_codice"
MOVES = ["main.py", "app_ui.py", "ui", "core", "data", "words_db.txt",
         "requirements - Copy.txt", ".gitignore.py"]

errors = []
if not KEEP.exists():
    print("ERRORE: manca words_db.json"); sys.exit(1)
before = rt.sha256(KEEP)
n_before = len(json.loads(KEEP.read_text(encoding="utf-8"))["articles_game"]["de"])
print(f"words_db.json: sha256 {before[:16]}..., {n_before} sostantivi tedeschi")

# i duplicati devono essere identici al file principale, altrimenti non li considero 'duplicati'
blocked = set()
for dup, top in (("words_db.txt", "words_db.txt"), ("data/words_db.py", "data")):
    f = repo / dup
    if f.exists():
        same = rt.sha256(f) == before
        print(f"{dup}: {'identico' if same else 'DIVERSO'} a words_db.json")
        if not same:
            blocked.add(top)
            errors.append(f"{dup} non e' identico a words_db.json: non sposto '{top}', serve una decisione")

if blocked:
    for e in errors:
        print("ERRORE:", e)
    print("Non ho spostato nulla.")
    sys.exit(1)

DEST.mkdir(parents=True, exist_ok=True)
for name in MOVES:
    if name in blocked:
        print(f"SALTO {name}"); continue
    src = repo / name
    if not src.exists():
        print(f"gia' assente: {name}"); continue
    dst = DEST / name
    if dst.exists():
        errors.append(f"{dst} esiste gia': non sovrascrivo"); continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    print(f"spostato: {name} -> archivio/vecchio_codice/{name}")

(repo / "archivio" / "LEGGIMI.txt").write_text(
    "Vecchio codice di Langue (versione Flet / console), spostato qui dall'agente T01.\n"
    "Non e' usato dal nuovo sito. Dei vecchi file si riusano solo i dati (words_db.json) e la logica dei punteggi.\n"
    "Per tornare alla situazione precedente: git, ramo main.\n", encoding="utf-8")

after = rt.sha256(KEEP)
n_after = len(json.loads(KEEP.read_text(encoding="utf-8"))["articles_game"]["de"])
print(f"dopo: sha256 {after[:16]}..., {n_after} sostantivi")
if after != before or n_after != n_before:
    errors.append("words_db.json e' cambiato!")
if not (repo / ".gitignore").exists():
    errors.append("manca .gitignore")
for e in errors:
    print("ERRORE:", e)
sys.exit(1 if errors else 0)
