id: GT08-griglia-scala
title: griglia grigio chiaro adattiva allo zoom + barra della scala
project: gtt
tier: small
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT08-griglia-scala
depends_on: [GT07-clic-fermate]
profile: profiles/gtt.md
allowed: [scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Leo wants the map easier to read: a very light grey square grid that shows distances/geometry, plus a scale bar.
Edit ONLY scripts/mappa_template.html.
1. Grid in METRES (not degrees): square cells whose size adapts to zoom so that a cell is roughly 40-120 px on screen: 100 m, 250 m, 500 m, 1 km, 2 km, 5 km, 10 km. Very light grey thin lines (e.g. rgba(150,150,150,0.25), 1 px), drawn ABOVE the background and BELOW all data layers. Compute metres from the map projection at the current latitude (Torino ~45.07°); one draw per frame, no per-tile work.
2. Scale bar bottom-left of the MAP area (not covered by the panel; if the panel is open put it to the right of the panel or bottom-centre): a bar of a round length (e.g. 200 m, 500 m, 1 km, 2 km, 5 km) with its label, plus a small text "griglia: 500 m" with the current cell size.
3. Toggle "Griglia" (checkbox) in the "Sfondo e filtro" section, ON by default. The scale bar is always visible.
4. Must stay readable on satellite and on "Mappa chiara"; if the grid is invisible on one of them, choose a colour that works on both and say so in Scelte.
Report agenti/GT08-griglia-scala/RAPPORTO.md (Italian): sizes per zoom, colours, how the metres are computed, clicks to test (zoom in/out: cell size and scale change; toggle off; compare with a known distance, e.g. Piazza Castello–Porta Nuova ≈ 1.2 km).
