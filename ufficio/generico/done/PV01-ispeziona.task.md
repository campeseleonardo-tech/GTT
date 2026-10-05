id: PV01-ispeziona
title: Ispeziona il modello Word e installa gli strumenti
project: preventivi
tier: small
priority: 1
repo: C:\Users\campe\Desktop\Projects\Preventivi_Gigi
branch: PV01-ispeziona
allowed: []
motore: gratis
modello: @gratis1
approved: yes
script: pv/PV01_ispeziona.py
gitignore: [Preventivi_esempi/, Claude outputs/]
git_init: yes
checks: [files_exist:agenti/PV01-ispeziona/ISPEZIONE.md;strumenti/verifica_preventivo.py;strumenti/genera_preventivo.py;strumenti/dati_esempio.json]
---

