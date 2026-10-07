id: GT07-clic-fermate
title: scheda al clic per sezioni/zone (niente riquadro al passaggio) + fermate piu' piccole azzurre
project: gtt
tier: small
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT07-clic-fermate
depends_on: [GT06-pannello]
profile: profiles/gtt.md
allowed: [scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Leo's feedback: hovering shows too much (the census-section box pops up everywhere); stop dots are too big and the white border is ugly.
Edit ONLY scripts/mappa_template.html.
1. Census sections and statistical zones: NO tooltip on hover any more (only the cursor becomes a pointer over them). On CLICK (not on drag/pan: ignore clicks where the mouse moved more than ~5 px) open an info card ("scheda") with ALL the information currently shown in the tooltip for that section/zone (see mostraTip calls near "Sezione di censimento" and the zone one), plus the section's value for the active theme. The card stays open until Leo closes it (× button, Esc, or click on empty map) or clicks another section; highlight the selected section with a thin outline while the card is open. Card position: fixed, top-right under the zoom buttons, not covering the left panel, readable on a narrow window.
2. Other objects (stops, lines, 5T sensors, real vehicles, simulated trips) keep a SHORT hover tooltip (max 2 lines); their full details also go into the card on click. Existing click behaviours (e.g. comune click in Pendolari, line click in Velocità) must open the same card.
3. Stops (the Lfermate drawing, around "if(vis(\"Lfermate\") && view.zoom>=14)"): smaller dots (about 60% of today's size, still growing a little with passaggi/ora), NO white fill or white border: solid light blue (e.g. #4aa3df, slightly transparent), thin darker blue edge at most. Update the legend swatch to match. Keep the hit-test radius for hover/click usable (do not shrink it below ~6 px).
Report agenti/GT07-clic-fermate/RAPPORTO.md (Italian): choices (card position, colours, sizes), clicks to test (hover over a section: nothing; click: card; drag the map: no card; Esc closes; stops at zoom 14-17).
