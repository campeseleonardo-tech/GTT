id: GT02-temi
title: temi esclusivi (un solo colore d'area alla volta) + sovrapposizioni + legenda per tema
project: gtt
tier: medium
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\GTT
branch: GT02-temi
depends_on: [GT01-sfondi]
profile: profiles/gtt.md
allowed: [scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
approval_before: leo
approved: yes
---
Problem: today all layers are on together (sections + lines + stops + 5T + vehicles + simulated trips) and they overlap; sections and zones can both color the area. Leo decided: ONE THEME AT A TIME + OVERLAYS.
Edit ONLY scripts/mappa_template.html. Keep every existing feature reachable.
1. Replace the "Livelli" block with a "Tema" selector (big buttons or radio list, one active). Each theme = one area coloring (or none) + a preset of overlays + its own legend:
   - Nessuno: only background.
   - Offerta: sections colored by "passaggi/ora entro 400 m"; overlays Linee (corse/ora) + Fermate.
   - Domanda: sections colored by "abitanti per km²"; no line overlays.
   - Poca offerta per abitante: sections colored by the existing ratio; Linee thin.
   - Zone statistiche: the 94 zones (passaggi/ora per km²) instead of sections.
   - Traffico: no area coloring; 5T sensors as the main layer (bigger markers, colored by what live/stat data offer today; if no live data, say "nessun dato live: riavvia la raccolta").
   - Tempo reale: real GTT vehicles + simulated trips + "Segnalazioni adesso"; no area coloring.
   Design the code so later tasks can add themes in one place (a THEMES table: id, label, area function or null, overlay preset, legend function). Next tasks will add "Velocità" and "Pendolari".
2. "Sovrapposizioni" block below: checkboxes Linee, Fermate, Corse simulate, Mezzi reali, Sensori 5T, Replay. Choosing a theme sets them to its preset; Leo can still change them by hand. Never two area colorings at once (sections and zones are mutually exclusive).
3. Legend: show ONLY the active theme and active overlays. Each legend entry carries a tag MISURATO (5T, GTT vehicles), PROGRAMMATO (GTFS timetables), STIMATO/SIMULATO (simulated trips), CENSIMENTO (ISTAT). "dati scarsi" where history < 72 h (already exists: reuse it).
4. Area fills semi-transparent (around 0.45-0.55) so the satellite background stays visible; outlines thin.
5. Default theme at start: Offerta.
Performance: theme switch must not rebuild heavy data; only change what is drawn.
Report agenti/GT02-temi/RAPPORTO.md (Italian): the theme table, what moved where, and the exact clicks for Leo to test every theme and overlay.
