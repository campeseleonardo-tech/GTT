id: T15-dati-web
title: dati per il sito (web/data.js) generati dai contenuti
project: langue
tier: small
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T15-dati-web
depends_on: [T12, T13, T14]
script: T15_build_data.py
allowed: [web/data.js]
checks: [files_exist:web/data.js, node_check:web/data.js]
approval_before: leo
approved: yes
---
(Nessun agente: script del runner scripts/T15_build_data.py.) Legge i file in contenuti/ e scrive web/data.js (window.LANGUE_DATA) per il sito statico. Nessuna modifica ai contenuti.
