id: GT04-velocita
title: velocita' commerciale MISURATA dei mezzi GTT per linea e ora (dallo storico)
project: gtt
tier: medium
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT04-velocita
depends_on: [GT02-temi]
profile: profiles/gtt.md
allowed: [scripts/04_genera_mappa.py, scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Goal: new theme "Velocità" = measured commercial speed (stops included) of GTT vehicles, per line, day type and hour.
Data: data/storico.sqlite, table mezzi_gtt(letto_utc TEXT, ts_feed INTEGER, veicolo TEXT, linea TEXT, corsa TEXT, lat REAL, lng REAL, velocita REAL, direzione INTEGER), about 250 vehicles saved every 60 s since 2026-10-04. The live collector WRITES this database right now: open it ONLY read-only, exactly like 06_dati_live.py does: sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=30). Never write, never VACUUM, never create indexes. If the file is missing or locked, skip the speed layer and print a message (the script must still exit 0).
1. In scripts/04_genera_mappa.py add a function (standard library only) that:
   - reads the last 28 days (use the index on letto_utc), ordered by veicolo, ts_feed;
   - takes consecutive positions of the same vehicle on the same line with 20 s <= dt <= 180 s; distance = haversine;
   - drops jumps > 90 km/h (GPS glitches) and layovers (vehicle not moving > 5 min in a row, typical at terminus); short stops at stops stay in (commercial speed);
   - aggregates per linea x tipo giorno (feriale/sabato/domenica, Italian local time: copy the small DST helper logic from 06_dati_live.py into 04, do NOT import or edit 06) x hour: speed = total distance / total time, number of samples, number of distinct days;
   - adds to the embedded data a compact object (e.g. vel: {linea: {tipo: {ora: [kmh, campioni, giorni]}}}) plus first/last timestamp and total hours of history.
   Keep it fast: one pass over the rows, no per-row Python objects kept beyond the running sums.
2. In scripts/mappa_template.html add the theme "Velocità" to the THEMES table built by GT02: lines colored by measured speed for the selected day type and hour (sensible classes, e.g. < 12, 12-16, 16-20, > 20 km/h; list your choice in Scelte), grey = no data or too few samples (choose a minimum and list it). Clicking a line shows km/h, campioni, giorni, and the line's hours with data. Legend tag MISURATO + "dati scarsi" when history < 72 h or days < 3. Explain in the legend in one line: "velocità commerciale: include le fermate; si aggiorna rigenerando la mappa".
3. Do not change data/live.js/stat.js logic.
Report agenti/GT04-velocita/RAPPORTO.md (Italian): method, thresholds, the numbers 04 prints (make 04 print lines with data and hours of history: the runner saves its output in agenti/ULTIMO_SCRIPT.txt), limits (no trip_id, so no delay; vehicles in feed may be incomplete), clicks to test.
