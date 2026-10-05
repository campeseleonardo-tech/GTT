id: GT05-risposta1
title: correzione di GT05 dopo la tua risposta
project: gtt
tier: small
priority: 1
per_te: Applica la tua risposta ("sì, la scarico") al lavoro di GT05, solo dove serve.
origine: risposta di Leo 2026-10-05 02:42
data_level: 0
profile: profiles/gtt.md
repo: C:\Users\campe\Desktop\GTT
branch: GT05-risposta1
allowed: [scripts/04_genera_mappa.py, scripts/mappa_template.html]
checks: [html_js_check:scripts/mappa_template.html, py_compile:scripts/04_genera_mappa.py, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py, run_py:scripts/04_genera_mappa.py]
---
Leo answered a question asked during task GT05-pendolari (tema Pendolari ISTAT 2021 (comune verso comune, lavoro e studio)).
Question: Vuoi i nomi dei comuni (tabella ISTAT codici)?
Your provisional choice was: no, bastano i codici
Leo's answer: sì, la scarico
Where it applies: scheda comune, tema Pendolari
Update ONLY what this answer changes, keep everything else exactly as it is, keep 'origine' and 'stato' fields unchanged. Do not ask new questions unless really needed.
