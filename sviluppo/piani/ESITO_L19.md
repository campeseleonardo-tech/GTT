# Esito L19 (24/10/2026, sessione cloud `claude/epic-clarke-6zdofk`)

Partenza da `origin/prova` (ff6fbca) più il commit del piano «Dopo L15-L18».

## 1. Toro come il vecchio contorno
- Nel blocco `#caricamento` (stesso testo in `scripts/mappa_template.html` e in `mappa_torino.html`, controllato identico): una linea d'oro sottile corre sul contorno del toro,
  avanti e indietro (`car-disegna 2.4s ease-in-out infinite alternate`, `stroke-dasharray:1` con `pathLength="1"`), riempimento `rgba(143,176,234,.10)`, niente oro pieno
  (tolto `car-riempi`). Durata minima di 2 s invariata. Con «riduci movimento»: toro a linee fermo e intero, nessuna attesa in più.
- `prova_design` (L18) ora controlla: animazione `car-disegna`, ripetizione infinita e direzione `alternate`, riempimento non pieno; con riduci movimento nessuna animazione e tratteggio a 0.

## 2. Gara del pannello della mappa
- `r6Gara` (template e mappa): `Gara.html({giro:true, ...})` con la sola auto TomTom (`auto_basso_min`), nessun comando, come nelle schede.
- `assets/gara.js` ripulito: resta un solo modo (senza comandi, una corsa dopo l'altra; un luogo solo = la stessa corsa ripetuta); via select, «Riparti», modo a due auto e relativi stili.
- La prova controlla nel template e in `mappa_torino.html` che la chiamata sia `giro:true`, senza `auto_alto_min` né `compatto`.

## 3. Immagini del README
Rifatte con `prova_pagine.py --playwright` dalla home nuova (`assets/readme/*.jpg`); le anteprime `assets/anteprime/` tenute solo se cambiano davvero (vedi sotto).

## Prove
`node --check assets/*.js`, `pyflakes scripts`, `prova_pagine.py --playwright` (0 errori, `prova_link_mappa` OK), peso di `mappa_torino.html` entro 5.961.194 byte.
