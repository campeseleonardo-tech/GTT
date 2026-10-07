id: T01-pulizia
title: pulizia cartella (duplicati e vecchio codice in archivio/, .gitignore corretto)
project: langue
tier: small
priority: 1
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T01-pulizia
script: T01_pulizia.py
gitignore: [.venv/, __pycache__/, *.pyc, .env, node_modules/]
allowed: [main.py, app_ui.py, ui, core, data, words_db.txt, requirements - Copy.txt, .gitignore.py, .gitignore, archivio]
checks: [files_exist:.gitignore;archivio/LEGGIMI.txt;words_db.json, git_unchanged:words_db.json]
approval_before: leo
approved: yes
---
(Nessun agente: questo task e' uno script del runner, scripts/T01_pulizia.py.)
Cosa fa, in ordine: crea il ramo T01-pulizia, scrive .gitignore, committa lo stato attuale ("[runner] stato prima di T01-pulizia"), sposta in archivio/vecchio_codice/ i file: main.py, app_ui.py, ui/, core/, data/, words_db.txt, "requirements - Copy.txt", .gitignore.py. Lascia in posizione words_db.json (200 sostantivi) e ne confronta l'hash prima/dopo. Non cancella niente.
