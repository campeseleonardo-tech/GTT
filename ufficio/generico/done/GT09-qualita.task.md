id: GT09-qualita
title: Analisi qualita' dei dati raccolti
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT09-qualita
allowed: [docs/QUALITA_DATI.md]
motore: gratis
modello: @gratis1
approved: yes
script: GT09_qualita.py
agent: yes
checks: [files_exist:docs/QUALITA_DATI.md, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py]
checks_warn: [min_chars:docs/QUALITA_DATI.md;1800, contains_all:docs/QUALITA_DATI.md;## Cosa funziona;## Problemi trovati;## Cosa non sappiamo ancora;## Prossimi passi consigliati]
---
A script already ran and wrote agenti/GT09-qualita/STATISTICHE.md: numbers about the quality of the data collected so far (readings per hour, gaps, vehicles per hour, 5T sensor accuracy, errors). Read it carefully and write docs/QUALITA_DATI.md IN ITALIAN for Leo (not a programmer).
Required sections (use exactly these titles):
## Cosa funziona
## Problemi trovati  (each with: evidence = the numbers from STATISTICHE.md, why it matters for the map)
## Cosa non sappiamo ancora
## Prossimi passi consigliati  (max 6, ordered by value, each marked FACILE / MEDIO / DIFFICILE)
Known facts to check against the numbers: the table of GTT vehicles has the fields "corsa" and "velocita" always empty; many 5T sensors have accuracy 0. Do not invent numbers: quote only what is in STATISTICHE.md and say "non risulta" when the data does not say. Do not touch any script.
