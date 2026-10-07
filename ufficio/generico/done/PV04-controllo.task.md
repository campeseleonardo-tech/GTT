id: PV04-controllo
title: Generatore: controllo finale e lista di prova
project: preventivi
tier: small
priority: 1
repo: C:\Users\campe\Desktop\Projects\Preventivi_Gigi
branch: PV04-controllo
base_branch: PV02-generatore
allowed: [strumenti/genera_preventivo.py, strumenti/PROVA_PREVENTIVO.md]
motore: gratis
modello: @forte
approved: yes
checks: [py_compile:strumenti/genera_preventivo.py, run_py:strumenti/verifica_preventivo.py, files_exist:strumenti/PROVA_PREVENTIVO.md]
checks_warn: [min_chars:strumenti/PROVA_PREVENTIVO.md;800]
---
Context: the quote generator strumenti/genera_preventivo.py fills the [[...]] placeholders of the Word template "Preventivo Automatico/MOD_PREVENTIVO_v4_1.docx" with the values of a JSON file (see strumenti/dati_esempio.json) and writes a new .docx. The logo is a real picture in the page header and must stay byte-identical: the code must never touch anything except word/document.xml. Read agenti/PV01-ispeziona/ISPEZIONE.md and agenti/PV02-generatore/RAPPORTO.md. Never use or invent real customer data: only the example data.
1. Review strumenti/genera_preventivo.py (changed by an earlier free model) for real bugs: wrong error messages, keys checked wrongly, file names from PROTOCOLLO, anything that could corrupt the .docx or the logo. Fix ONLY real bugs with small EDIT blocks (copy SEARCH text exactly). If everything is fine, do not change it.
2. Write strumenti/PROVA_PREVENTIVO.md IN ITALIAN for Leo (not a programmer): step-by-step test with the exact command, what to check in the output (all placeholders filled, logo visible and sharp, totals), how to open it in Word AND in LibreOffice, and what to write down if something is wrong. Checkboxes "[ ] ok / [ ] non va".
Write agenti/PV04-controllo/RAPPORTO.md in Italian: bugs found (or "nessuno") and what you changed.
