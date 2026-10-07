id: GT11-orari-fermate
title: File con gli orari programmati di ogni fermata
project: gtt
tier: small
priority: 2
repo: C:\Users\campe\Desktop\GTT
branch: GT11-orari-fermate
base_branch: GT09-qualita
allowed: []
motore: gratis
modello: @gratis1
approved: yes
script: GT11_orari.py
checks: [files_exist:data/processed/orari_fermate.js;agenti/GT11-orari-fermate/ORARI.md, git_unchanged:scripts/03_raccolta_continua.py;scripts/06_dati_live.py;scripts/supervisore.py;scripts/installa_sfondo.py]
---

