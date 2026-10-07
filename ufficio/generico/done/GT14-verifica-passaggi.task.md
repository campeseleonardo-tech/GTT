id: GT14-verifica-passaggi
title: Prossimi passaggi: controllo e correzione
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT14-verifica-passaggi
base_branch: GT12-prossimi-passaggi
allowed: [scripts/mappa_template.html]
motore: gratis
modello: @forte
approved: yes
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
checks_warn: [contains_all:agenti/GT14-verifica-passaggi/RAPPORTO.md;Come provarlo]
---
Context: GTT is Leo's interactive map of Torino public transport (scripts/04_genera_mappa.py builds mappa_torino.html from scripts/mappa_template.html). Read MEMORIA_PROGETTO.md (rules: always distinguish measured from estimated/timetable data).
An earlier free model (task GT12) added "Prossimi passaggi" to the stop card using window.ORARI from data/processed/orari_fermate.js (format in agenti/GT11-orari-fermate/ORARI.md; minutes after midnight, day types fer/sab/dom). Read agenti/GT12-prossimi-passaggi/RAPPORTO.md and the code marked // [agente GT12] in scripts/mappa_template.html.
Check that it really works: script tag with onerror fallback, correct day type (Mon-Fri fer, Sat sab, Sun dom), next 4 departures per line from the current time, tomorrow's first departures marked when fewer remain, HH:MM plus minutes from now, label "Orario programmato (non e' il tempo reale)", nothing shown and no error when data is missing, work done only on click. Fix ONLY real bugs with small EDIT blocks (copy SEARCH text exactly), marked // [agente GT14].
Write agenti/GT14-verifica-passaggi/RAPPORTO.md in Italian: what was wrong (or "niente"), and "## Come provarlo": the exact steps for Leo (regenerate the map, open it, click a stop, what he should see).
