id: GT19-elaborazione-matrici-pen
title: Elaborazione matrici pendolarismo ISTAT (sezioni 2011 e dati 2021)
project: gtt
tier: medium
priority: 2
data_level: 0
origine: chat pannello 2026-10-05 15:57
per_te: Estrae e prepara i dati sui pendolari per sezione 2011 e 2021 per Torino e cintura
profile: profiles/gtt.md
repo: C:\Users\campe\Desktop\GTT
branch: GT19-elaborazione-matrici-pen
allowed: [docs, scripts, data/processed]
---
Esamina i nuovi archivi in docs (in particolare matrici-pendolarismo-sezione-censimento-2011.zip e le matrici 2021). Estrai e filtra solo i dati relativi a Torino e cintura (provincia di Torino). Crea uno script Python dedicato in scripts/ che elabori questi flussi (origine, destinazione, orario/motivo dove presente) e salvi un file compatto in data/processed/. Aggiorna la documentazione in docs/ su tracciati record e volumi trovati. Non toccare storico.sqlite ne' la raccolta in corso. La task e' finita quando il file elaborato e' pronto e verificato con un rapporto sintetico.
