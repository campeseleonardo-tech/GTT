id: PV05-preventivo-finto
title: Preventivo finto completo e verifica automatica
project: preventivi
tier: small
priority: 1
repo: C:\Users\campe\Desktop\Projects\Preventivi_Gigi
branch: PV05-preventivo-finto
base_branch: PV04-controllo
allowed: [strumenti/esempi/finto_01.json, strumenti/prova_finta.py]
motore: gratis
modello: @forte
approved: yes
checks: [py_compile:strumenti/prova_finta.py, run_py:strumenti/prova_finta.py]
checks_warn: [contains_all:agenti/PV05-preventivo-finto/RAPPORTO.md;Come provarlo]
---
Context: strumenti/genera_preventivo.py fills the [[...]] placeholders of the Word template "Preventivo Automatico/MOD_PREVENTIVO_v4_1.docx" with the values of a JSON file (format: strumenti/dati_esempio.json) and writes a new .docx. The logo is a picture in the page header and must stay byte-identical. Read strumenti/genera_preventivo.py, strumenti/dati_esempio.json, agenti/PV01-ispeziona/ISPEZIONE.md and strumenti/PROVA_PREVENTIVO.md. NEVER use real customer data: everything must be clearly invented.
1. Write strumenti/esempi/finto_01.json: a realistic but INVENTED quote of an Italian electrician (e.g. renovation of the electrical system of a 2-room flat: new switchboard, sockets, lights, earthing, certification), same keys as dati_esempio.json, plausible quantities and prices, invented customer (write "CLIENTE DI PROVA" in the name).
2. Write strumenti/prova_finta.py (standard library only), runnable with no arguments from the repo root or from strumenti/: it runs genera_preventivo.py on esempi/finto_01.json into a temporary folder (tempfile, never inside the repo), then checks and prints in Italian: (a) the .docx opens as zip; (b) no "[[" left in word/document.xml; (c) every value of the JSON that should appear does appear; (d) the header image files (word/media/*) are byte-identical to the template's; (e) if the JSON has line items and a total, the total matches the sum. Print "OK" or the list of problems, and exit with code 1 if any check fails.
Write agenti/PV05-preventivo-finto/RAPPORTO.md in Italian, simple words, with "## Come provarlo" (exact command) and what each check means.
