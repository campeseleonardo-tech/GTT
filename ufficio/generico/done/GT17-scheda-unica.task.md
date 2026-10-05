id: GT17-scheda-unica
title: Mappa: una scheda al clic uguale per tutto
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT17-scheda-unica
base_branch: GT16-temi
allowed: [scripts/mappa_template.html]
motore: gratis
modello: @forte
approved: yes
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py;data, run_py:scripts/04_genera_mappa.py]
checks_warn: [contains_all:agenti/GT17-scheda-unica/RAPPORTO.md;Come provarlo]
---
Context: GTT is Leo's interactive map of Torino public transport. scripts/04_genera_mappa.py builds mappa_torino.html from scripts/mappa_template.html. Read MEMORIA_PROGETTO.md (rules and Leo's decisions: always keep measured vs timetable/estimated distinct) and docs/PIANO_UI_E_SCENARI.md (the approved plan; follow Leo's answers to its questions if present in MEMORIA_PROGETTO.md, otherwise the provisional choices). The template is big: use SMALL EDIT blocks and copy every SEARCH text exactly; never rewrite the file.

Do step GT17 of docs/PIANO_UI_E_SCENARI.md: make every click card (stop, line, 5T sensor, census section, municipality) follow the single 4-part structure of "### Struttura unica per tutte le schede informative al clic": header with name and a data-source badge ([MISURATO] / [PROGRAMMATO] / [CENSIMENTO] / [STIMATO]); main value in large text with a short status; max 3-4 detail lines; an expandable "approfondimento" (e.g. the next departures for stops). Write ONE small helper function that builds the card and use it everywhere; keep all the information that exists today (move it into the right part, do not lose it). Do not change themes or data.
Mark changes with // [agente GT17]. Write agenti/GT17-scheda-unica/RAPPORTO.md in Italian with "## Come provarlo" (which elements to click and what each card should show).
