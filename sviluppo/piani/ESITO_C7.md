# Esito C7 — gara bus contro auto (22/10/2026, cloud)

## Fatto
- **`assets/gara.js`**: componente comune `Gara.html({luoghi, scelto, compatto})`. Bus e auto partono insieme e corrono verso «Piazza Castello»; 1 minuto vero = 0,15 secondi; all'arrivo compaiono i minuti.
  L'auto ha due corsie quando la forbice è di almeno 1 minuto (auto veloce = fattore dei sensori, auto chiara = fattore di Google). Tendina con punti prioritari e interscambi (versione grande), bottone «Riparti»,
  testo scritto sotto (anche per il lettore di schermo). Con «riduci movimento»: barre ferme con i minuti. Parte da solo quando compare nella pagina; italiano e inglese.
- **Scheda 3**: la gara è il grafico principale (parte dal punto «dipende dal traffico», scelto dai dati, oggi Metro Massaua). Il grafico dei minuti di pareggio passa in «Altri grafici». `scripts/schede/r6.py`, `risultati.html` (tipo `gara`), `testi.json` (inglese).
- **Mappa**: `scripts/mappa_template.html`: la gara piccola compare nel pannello del punto prioritario e dell'interscambio (`r6Gara`). Il file `mappa_torino.html` **non è rigenerato** (nel cloud non ci sono i dati).
- Schede rigenerate (`data/schede_risultati.js`); numeri e testi italiani delle altre schede invariati.

## Prove
- `python scripts/prova_pagine.py`: 0 errori su 19 pagine.
- Browser headless: gara a metà e a fine corsa, computer chiaro, telefono scuro, «riduci movimento», cambio punto dalla tendina; pannello della mappa provato su una copia di `mappa_torino.html` con la stessa modifica (nessun errore). Nessuna nota di traduzione mancante.

## Cosa deve fare Leo sul PC
1. `git fetch origin claude/kind-brown-drqyhf` e `git merge --no-edit origin/claude/kind-brown-drqyhf`, poi `scripts\RIFAI_MAPPA_E_SCHEDE.bat`.
2. Aprire `risultati.html#p3`: la gara parte da sola, scegli altri punti dalla tendina. Aprire la mappa, tema «Parcheggi di scambio», cliccare un punto: nel pannello c'è la gara piccola.
3. Da guardare: velocità (0,15 s per minuto, la corsa più lunga dura circa 6 secondi), icone e colori, leggibilità sul telefono (scritte piccole).
