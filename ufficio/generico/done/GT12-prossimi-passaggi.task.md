id: GT12-prossimi-passaggi
title: Clic su fermata: prossimi passaggi
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT12-prossimi-passaggi
base_branch: GT11-orari-fermate
allowed: [scripts/mappa_template.html]
motore: gratis
modello: @gratis1
approved: yes
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
checks_warn: [contains_all:scripts/mappa_template.html;orari_fermate.js;[agente GT12];ORARI, min_chars:agenti/GT12-prossimi-passaggi/RAPPORTO.md;300]
---
Feature: when the user clicks a stop on the map, the stop card must also show "Prossimi passaggi" (next departures).
Data: a script already created data/processed/orari_fermate.js, which defines window.ORARI = {"v":..., "t":["fer","sab","dom"], "s":{ stopId: { lineId: [[minutes fer],[minutes sab],[minutes dom]] } }} (minutes after midnight, sorted). Read agenti/GT11-orari-fermate/ORARI.md for the exact format and the stop ids.
Edit ONLY scripts/mappa_template.html, with EDIT blocks (small, local changes; the file is big, do not rewrite it):
1. Load the data with a static tag placed before the main script: <script src="data/processed/orari_fermate.js" onerror="window.ORARI=null"></script>   (the page must keep working if the file is missing).
2. In the code that builds the stop card (find the place that handles a click on a stop), add a block: for each line serving the stop, the next 4 departures from the current local time (use today's day type: Mon-Fri "fer", Sat "sab", Sun/holiday "dom"; if fewer than 4 remain today, show the first of tomorrow with a small mark). Show the time as HH:MM and the minutes from now.
3. HONESTY RULE: these are TIMETABLE values, not measurements. Label the block clearly "Orario programmato (non e' il tempo reale)". Never mix them with measured data (5T sensors / real vehicles).
4. If window.ORARI is null or the stop is not in it, show nothing (no error).
5. Performance: do the work only on click, never per frame; no loops over all stops.
Mark every new or changed block with a comment // [agente GT12]. Write agenti/GT12-prossimi-passaggi/RAPPORTO.md in Italian: what you changed and exactly what Leo should click to test it.
