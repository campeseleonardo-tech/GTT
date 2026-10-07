id: PV02-generatore
title: Generatore di preventivi piu' chiaro
project: preventivi
tier: small
priority: 1
repo: C:\Users\campe\Desktop\Projects\Preventivi_Gigi
branch: PV02-generatore
base_branch: PV01-ispeziona
allowed: [strumenti/genera_preventivo.py]
motore: gratis
modello: @gratis1
approved: yes
checks: [py_compile:strumenti/genera_preventivo.py, run_py:strumenti/verifica_preventivo.py]
checks_warn: [contains_all:agenti/PV02-generatore/RAPPORTO.md;genera_preventivo.py]
---
Goal: make the quote generator easier and safer to use. Edit ONLY strumenti/genera_preventivo.py (it already works: do not break it).
Context: the generator fills the [[...]] placeholders of the Word template "Preventivo Automatico/MOD_PREVENTIVO_v4_1.docx" with the values of a JSON file (see strumenti/dati_esempio.json) and writes a new .docx. The logo is a real picture in the page header and must stay byte-identical: the code must never touch anything except word/document.xml. Read agenti/PV01-ispeziona/ISPEZIONE.md for the structure.
Do these small changes with EDIT blocks (not by rewriting the whole file):
1. A clear Italian message (no traceback) if the JSON is missing, invalid, or a needed key is missing (say which key).
2. Optional third use: if the output path is a folder, name the file from the PROTOCOLLO value (replace characters not allowed in file names).
3. Short Italian comments explaining each function, because Leo is not a programmer.
Keep the standard library only. Then write agenti/PV02-generatore/RAPPORTO.md in Italian (what changed, how to run it: python strumenti/genera_preventivo.py dati.json uscita.docx).
