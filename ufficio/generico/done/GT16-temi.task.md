id: GT16-temi
title: Mappa: da 9 temi a 4
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT16-temi
base_branch: GT15-piano-ui-scenari
allowed: [scripts/mappa_template.html]
motore: gratis
modello: @forte
approved: yes
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py;data, run_py:scripts/04_genera_mappa.py]
checks_warn: [contains_all:agenti/GT16-temi/RAPPORTO.md;Come provarlo]
---
Context: GTT is Leo's interactive map of Torino public transport. scripts/04_genera_mappa.py builds mappa_torino.html from scripts/mappa_template.html. Read MEMORIA_PROGETTO.md (rules and Leo's decisions: always keep measured vs timetable/estimated distinct) and docs/PIANO_UI_E_SCENARI.md (the approved plan; follow Leo's answers to its questions if present in MEMORIA_PROGETTO.md, otherwise the provisional choices). The template is big: use SMALL EDIT blocks and copy every SEARCH text exactly; never rewrite the file.

Do step GT16 of docs/PIANO_UI_E_SCENARI.md ("## Ordine di lavoro"): reduce the theme menu to the 4 themes of "### I 4 temi proposti" (Servizio e abitanti with an inner choice: indice di servizio / solo offerta / solo residenti; Traffico e velocita'; Tempo reale e flotta; Pendolarismo). Remove "Zone statistiche 2011" from the menu (keep its code if removing it is risky, just hide it). Group the time controls ("Quando") in one block. Do NOT change data, calculations or click cards (that is GT17). Nothing that worked before may break: if a theme cannot be merged safely, keep it and explain why.
Mark changes with // [agente GT16]. Write agenti/GT16-temi/RAPPORTO.md in Italian: what changed, what was kept and why, and "## Come provarlo" (regenerate, open, what Leo should see).
