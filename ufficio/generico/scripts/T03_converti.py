# -*- coding: utf-8 -*-
"""T03 - Converte i 200 sostantivi di words_db.json nello schema dei contenuti.
Script del runner (nessun agente). Non modifica words_db.json.
Livello: A1 di default per tutti (non verificato parola per parola): a campione lo controlla Leo."""
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
src = json.loads((repo / "words_db.json").read_text(encoding="utf-8"))["articles_game"]["de"]
out = []
for i, w in enumerate(src, start=1):
    out.append({
        "id": f"art-{i:04d}", "tipo": "articolo", "lingua": "de", "livello": "A1",
        "stato": "verificato", "origine": "importato", "fonte": "words_db.json (livello A1 di default)",
        "parola": w["word"], "articolo": w["correct_article"], "traduzione_it": w["translation"],
    })
dst = repo / "contenuti" / "parole.json"
dst.parent.mkdir(exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"scritti {len(out)} record in contenuti/parole.json")
