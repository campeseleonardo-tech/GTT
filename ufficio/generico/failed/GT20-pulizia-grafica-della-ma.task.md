id: GT20-pulizia-grafica-della-ma
title: Pulizia grafica della mappa e integrazione della domanda ISTAT
project: gtt
tier: medium
priority: 2
data_level: 0
origine: chat pannello 2026-10-05 16:06
per_te: Pulisce la grafica della mappa, elimina i bordi rossi fissi e integra con ordine la domanda ISTAT.
profile: profiles/gtt.md
repo: C:\Users\campe\Desktop\GTT
branch: GT20-pulizia-grafica-della-ma
allowed: [mappa_torino.html, scripts/04_genera_mappa.py]
checks: [files_exist:mappa_torino.html;scripts/04_genera_mappa.py]
---
Rivedere lo stile di mappa_torino.html: 1) Aggiungere un tema pulito/neutro senza colori d'area invasivi; 2) Rimuovere i bordi rossi sempre visibili, mostrandoli solo se il livello è attivo o al clic; 3) Coordinare le sovrapposizioni per evitare conflitti visivi con i temi; 4) Integrare i dati della domanda ISTAT elaborati da GT19 con visualizzazione leggera e dettagli nella scheda al clic. Non rompere i controlli orari e i prossimi passaggi.
