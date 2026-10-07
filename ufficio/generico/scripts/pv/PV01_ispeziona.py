# -*- coding: utf-8 -*-
"""
PV01_ispeziona.py - script del runner (0 token). Uso: python PV01_ispeziona.py <cartella Preventivi_Gigi>
1) Ispeziona MOD_PREVENTIVO_v4_1.docx (intestazioni, immagini, segnaposto) -> agenti/PV01-ispeziona/ISPEZIONE.md (+ copia xml/)
2) Installa in strumenti/ il verificatore, il generatore di riferimento e dati_esempio.json (se mancano).
Non modifica il modello Word ne' i preventivi veri.
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

QUI = Path(__file__).resolve().parent
repo = Path(sys.argv[1])
cands = sorted(repo.glob("**/MOD_PREVENTIVO*.docx"))
cands = [c for c in cands if "Preventivi_esempi" not in c.parts]
if not cands:
    print("modello MOD_PREVENTIVO*.docx non trovato"); sys.exit(1)
mod = cands[-1]
out = repo / "agenti" / "PV01-ispeziona"
(out / "xml").mkdir(parents=True, exist_ok=True)
righe = [f"# Ispezione del modello\n\nFile: `{mod.relative_to(repo)}`\n"]
with zipfile.ZipFile(mod) as z:
    righe.append("## Contenuto dello zip\n")
    for i in z.infolist():
        righe.append(f"- {i.filename} ({i.file_size} byte)")
    for nome in z.namelist():
        if nome.startswith("word/") and nome.endswith((".xml", ".rels")) and nome.count("/") == 1 or nome.startswith("word/_rels/"):
            (out / "xml" / nome.replace("/", "__")).write_bytes(z.read(nome))
    righe.append("\n## Immagini inline (logo)\n")
    for nome in z.namelist():
        if re.match(r"word/(header|footer)\d*\.xml$", nome) or nome == "word/document.xml":
            x = z.read(nome).decode("utf-8", "replace")
            for m in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"', x):
                righe.append(f"- {nome}: immagine {m.group(1)}x{m.group(2)} EMU")
    doc = z.read("word/document.xml").decode("utf-8", "replace")
    testo = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", doc)
    ph = sorted(set(re.findall(r"\[\[[^\]]*\]\]", "".join(testo))))
    righe.append("\n## Segnaposto nel corpo\n")
    righe += [f"- `{p}`" for p in ph] or ["- nessuno"]
righe.append("\nLogo: e' un'immagine vera dentro l'intestazione. Il generatore non la tocca (resta identica byte per byte).")
(out / "ISPEZIONE.md").write_text("\n".join(righe) + "\n", encoding="utf-8")

st = repo / "strumenti"
st.mkdir(exist_ok=True)
for src, dst in (("verifica_preventivo.py", "verifica_preventivo.py"), ("genera_preventivo_RIFERIMENTO.py", "genera_preventivo.py"),
                 ("genera_preventivo_RIFERIMENTO.py", "genera_preventivo_RIFERIMENTO.py")):
    if (QUI / src).exists() and not (st / dst).exists():
        shutil.copy2(QUI / src, st / dst)
if not (st / "dati_esempio.json").exists():
    shutil.copy2(QUI / "dati_esempio.json", st / "dati_esempio.json")
print("ok", mod)
