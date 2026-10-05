id: GT13-altre-citta
title: Studio: estendere la mappa ad altre citta'
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT13-altre-citta
base_branch: GT12-prossimi-passaggi
allowed: [docs/ALTRE_CITTA.md]
motore: gratis
modello: @gratis2
approved: yes
checks: [files_exist:docs/ALTRE_CITTA.md, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py]
checks_warn: [min_chars:docs/ALTRE_CITTA.md;2500, contains_all:docs/ALTRE_CITTA.md;## Cosa e' specifico di Torino oggi;## Dati che servono per una nuova citta';## Piano a passi;## Rischi]
---
Write docs/ALTRE_CITTA.md IN ITALIAN: a study on extending the map to other cities. Read MEMORIA_PROGETTO.md, docs/FONTI_DATI.md and scripts/04_genera_mappa.py.
Required sections (exact titles):
## Cosa e' specifico di Torino oggi  (list each Torino-specific thing and WHERE it lives: file and function/constant name, as found in the code you were given; say "non l'ho visto" if unsure)
## Dati che servono per una nuova citta'  (a table: dato | a cosa serve | formato tipico | dove si trova di solito, e.g. GTFS static, GTFS-Realtime, census sections, map tiles)
## Proposta: file di configurazione per citta'  (a small JSON example: name, center, zoom, data paths, stop id prefix, labels, timezone; and which parts of the code would read it)
## Piano a passi  (max 8 steps, each FACILE/MEDIO/DIFFICILE, ordered so Torino keeps working at every step)
## Rischi
You cannot browse: do NOT invent URLs or portal names. When you mention where data may be found, say "da verificare". Do not modify any file except docs/ALTRE_CITTA.md.
