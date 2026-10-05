# -*- coding: utf-8 -*-
"""T15 - Genera web/data.js per il sito statico, partendo dai file in contenuti/.
Script del runner (nessun agente). Non modifica i contenuti. Include TUTTI i record (anche "da_verificare"):
e' il sito (T16) che nasconde quelli da verificare, cosi' lo stato resta visibile nei dati."""
import json
import sys
from pathlib import Path

repo = Path(sys.argv[1])
cont = repo / "contenuti"
gruppi = {"articoli": ("parole.json", "parole_nuove.json", "parole_nuove_2.json"),
          "frasi": ("frasi.json", "frasi_2.json"),
          "errori": ("errori.json", "errori_2.json")}
out, conta = {}, {}
for chiave, files in gruppi.items():
    recs = []
    for f in files:
        p = cont / f
        if p.exists():
            recs += json.loads(p.read_text(encoding="utf-8"))
    out[chiave] = recs
    conta[chiave] = len(recs)
web = repo / "web"
web.mkdir(exist_ok=True)
testo = ("// Generato da scripts/T15_build_data.py dai file in contenuti/. NON modificare a mano: rilancia il task.\n"
         "window.LANGUE_DATA = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n")
(web / "data.js").write_text(testo, encoding="utf-8")
print("scritto web/data.js: " + ", ".join(f"{k} {v}" for k, v in conta.items()))
