id: GT05-pendolari
title: tema Pendolari ISTAT 2021 (comune verso comune, lavoro e studio)
project: gtt
tier: medium
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT05-pendolari
depends_on: [GT04-velocita]
profile: profiles/gtt.md
allowed: [scripts/04_genera_mappa.py, scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Goal: new theme "Pendolari" with the ISTAT 2021 commuting matrices already in the project.
Read docs/istat/NOTE_FILE_ISTAT.md first. Files (READ ONLY, never move or modify): docs/matrix_pendoLAVORO_2021.zip and docs/matrix_pendoSTUDIO_2021.zip: tab-separated text inside the zip, columns = province and municipality of residence, province and municipality of work/study, number of commuters; comune contro comune, no mode, no hour; the study file is a model estimate. You cannot open them: write a robust parser in 04 (zipfile + csv, detect the header row and the columns by name/position, tolerate encodings latin-1/utf-8, print the detected columns and totals). Torino = PRO_COM 1272 (province 1, comune 272; PRO_COM = provincia*1000 + comune). Check: Torino work inflow should be about 138,605 and outflow about 71,297 (from the notes): print the values and, if far off, say so in the report.
1. In scripts/04_genera_mappa.py: for every comune present in data/processed/sezioni_torino.json (field "c" = PRO_COM, "p" = population): inflow to Torino and outflow from Torino, work and study separately, plus population and a population-weighted centroid from its sections. Sum the flows from comuni outside the map area as "altri comuni". Embed a compact object. If the zips are missing, skip and exit 0.
2. In scripts/mappa_template.html add theme "Pendolari" to the THEMES table: sections colored by their comune's value (choice: "verso Torino ogni 1000 abitanti" default, or absolute), straight flow lines from each comune centroid to Torino with width proportional to the flow (top 30 comuni, the others summarized in the legend), selector Lavoro / Studio / Entrambi and Entrano / Escono. Click on a comune: name if available (otherwise PRO_COM code), inflow, outflow, population. Legend tag CENSIMENTO + "ISTAT 2021, comune→comune, senza mezzo né orario; studio = stima".
3. Torino itself: show the internal flow (Torino→Torino) as a number in the legend, not as a line.
Report agenti/GT05-pendolari/RAPPORTO.md (Italian): detected columns, totals vs expected, choices, limits, clicks to test.
