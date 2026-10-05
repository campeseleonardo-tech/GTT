PROJECT: GTT - interactive mobility map of Torino and its belt (personal study project of Leo). One local HTML page, no server, no external libraries: hand-written canvas map engine in plain JavaScript. Everything in Italian (interface, comments, reports). Leo is not a programmer: keep code simple and commented in Italian.

How the project works:
- scripts/04_genera_mappa.py reads the data (data/raw, data/processed) and fills scripts/mappa_template.html (the placeholder "__DATI__") -> writes mappa_torino.html. You edit the TEMPLATE and the scripts, never mappa_torino.html (it is generated; the runner regenerates it after your work).
- A data collector runs 24/7 on Leo's PC: scripts/supervisore.py starts scripts/03_raccolta_continua.py (SQLite data/storico.sqlite) and every minute loads scripts/06_dati_live.py, which writes data/live.js, data/stat.js, data/replay_*.js that the page rereads.
- Read MEMORIA_PROGETTO.md and PASSAGGIO_CONSEGNE.md (short) for context, docs/FONTI_DATI.md for data sources.

PROTECTED FILES - NEVER modify them, the live collector uses them right now: scripts/03_raccolta_continua.py, scripts/06_dati_live.py, scripts/supervisore.py, scripts/installa_sfondo.py, all *.bat files. If your task needs a change there, do NOT make it: describe the exact change in DECISIONS.md (STATUS: OPEN) and do the rest.
Never touch data/ (raw data, database), logs/, docs/*.zip. You may READ data/live.js, data/stat.js, data/processed/* to understand the data formats (read only small parts: some files are megabytes).

Rules:
- Honesty on the map: always distinguish MEASURED (5T sensors, real GTT vehicles) from ESTIMATED/SIMULATED (timetables, simulated trips). Short history (< 72 h) keeps the label "dati scarsi". Never present an estimate as a measurement.
- Only Python standard library in scripts (no pip packages). No external JS libraries, no new network calls except the existing tile backgrounds (CARTO must not be used: needs a key).
- Keep performance in mind: the page holds ~7,000 stops, ~8,300 census sections, ~14,000 trips; avoid work per frame that scales with all of them.
- Small, focused changes; keep existing features working. Mark your code with a comment `// [agente <task id>]` (or `# [agente <task id>]`) at the start of each new or changed block, so Leo can find it.
- You cannot run programs. The runner checks JavaScript syntax, Python syntax, and regenerates the map with 04_genera_mappa.py; it cannot click or see the page. In the report, list exactly what Leo should click to test it.
