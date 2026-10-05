id: GT15-piano-ui-scenari
title: Piano: mappa piu' semplice, dati di traffico e base per gli scenari
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT15-piano-ui-scenari
base_branch: GT14-verifica-passaggi
allowed: [docs/PIANO_UI_E_SCENARI.md]
motore: gratis
modello: @forte
approved: yes
checks: [files_exist:docs/PIANO_UI_E_SCENARI.md, git_unchanged:scripts;data]
checks_warn: [min_chars:docs/PIANO_UI_E_SCENARI.md;4000, contains_all:docs/PIANO_UI_E_SCENARI.md;## UI oggi;## UI proposta;## Base per gli scenari;## Ordine di lavoro]
---
Context: GTT is Leo's interactive map of Torino public transport (offer, demand, critical points, simulated vehicles). scripts/04_genera_mappa.py builds mappa_torino.html from scripts/mappa_template.html. Read MEMORIA_PROGETTO.md (goals, decisions, data, limits: always keep "measured" and "estimated/timetable" clearly distinct), docs/FONTI_DATI.md and scripts/mappa_template.html (only what you need to list layers, themes, controls and click cards).
Leo's feedback: the map has TOO MANY layers and themes, and the cards shown on click are CONFUSING (too much scattered information). Next he wants traffic data in the map and, above all, a BASE for alternative scenarios ("what would improve if line X changed"): he does not want to fix the metrics now; the base must allow adding metrics later (waiting time, coverage, travel times, crowding...).
Write docs/PIANO_UI_E_SCENARI.md IN ITALIAN, plain words (Leo is not a programmer), sections with exact titles:
## In breve (5 lines) | ## UI oggi (list every layer, theme, control and click card that exists, one line each) | ## UI proposta (what to remove, what to merge, max 4-5 themes, ONE consistent structure for all click cards; a simple sketch in text) | ## Dati di traffico (what is already collected: 5T sensors, vehicle positions, measured speeds; what is reliable; how to show it without confusing measured and estimated) | ## Base per gli scenari (how to represent a scenario as a modified copy of the timetable/lines without touching the real data; how to compute and compare indicators baseline vs scenario; which simple indicators can be computed with the data already available; what is missing) | ## Ordine di lavoro (small steps, each a possible separate agent task with the files it would touch) | ## Rischi e limiti.
Put at most 5 questions in DOMANDE.md, each with clear context (perche) and what each option changes (cambia), and always include an option "decidi tu". Do not modify any other file.
