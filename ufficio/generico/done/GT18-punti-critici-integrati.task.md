id: GT18-punti-critici-integrati
title: Punti critici integrati nei temi esistenti
project: gtt
tier: medium
priority: 2
data_level: 0
origine: chat pannello 2026-10-05 15:21
per_te: Integra l'indice di criticita' (domanda vs offerta) nei temi e nella scheda unica della mappa
profile: profiles/gtt.md
repo: C:\Users\campe\Desktop\GTT
branch: GT18-punti-critici-integrati
allowed: [scripts/04_genera_mappa.py, scripts/mappa_template.html, mappa_torino.html]
checks: [files_exist:scripts/04_genera_mappa.py;scripts/mappa_template.html;mappa_torino.html]
---
Calcola l'indice di criticita' (rapporto tra domanda/residenti e passaggi di mezzi GTT per zona). Integra la visualizzazione direttamente nei 4 temi e nei filtri gia' esistenti nella mappa, senza creare menu o controlli separati. Mostra l'indicatore di criticita' nella scheda unica al clic creata in GT17. Non toccare gli script di raccolta dati. La task e' finita quando la mappa evidenzia le zone critiche usando i controlli attuali e la scheda mostra il valore.
