id: GT04-risposta1
title: correzione di GT04 dopo la tua risposta
project: gtt
tier: small
priority: 1
per_te: Applica la tua risposta ("A tenere") al lavoro di GT04, solo dove serve.
origine: risposta di Leo 2026-10-05 02:43
data_level: 0
profile: profiles/gtt.md
repo: C:\Users\campe\Desktop\GTT
branch: GT04-risposta1
allowed: [scripts/04_genera_mappa.py, scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
---
Leo answered a question asked during task GT04-velocita (velocita' commerciale MISURATA dei mezzi GTT per linea e ora (dallo storico)).
Question: Soglie colori velocità (12/16/20 km/h) vanno bene?
Your provisional choice was: A
Leo's answer: A tenere
Where it applies: mappa_template.html velClasse
Update ONLY what this answer changes, keep everything else exactly as it is, keep 'origine' and 'stato' fields unchanged. Do not ask new questions unless really needed.
