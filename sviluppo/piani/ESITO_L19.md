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
Rifatte con `prova_pagine.py --playwright` dalla home nuova (`assets/readme/*.jpg`). Le anteprime `assets/anteprime/` sono cambiate solo per la ricompressione: ripristinate.

## Prove
`node --check assets/*.js`, `pyflakes scripts`, `prova_pagine.py --playwright` (0 errori, `prova_link_mappa` OK), peso di `mappa_torino.html` entro 5.961.194 byte.

## Correzioni dopo la prova di Leo sul PC
- La gara delle schede non partiva (`t.parlatoGiro is not a function` dopo la pulizia di `gara.js`): corretto, la prova di design lo trova.
- Il toro non si disegnava: con `vector-effect:non-scaling-stroke` il tratteggio ignora `pathLength`. Ora lo spessore è in unità del disegno (`stroke-width:45`, il gruppo è scalato di 0,1: circa 1,5 px) e la linea si crea sul contorno.
