# Esito L2 (23/10/2026, PC): revisione grafica di Leo

AGGIORNA_RISULTATI = **sì** (scelta di Leo). I controlli grafici li fa Leo: qui solo che il codice giri.

## Passo 0: risultati rifatti con lo storico al 23/10 (commit a parte)
`rifai_tutto.py --da traffico`: 47 minuti, nessun errore. Prima → dopo (feriale):

| Risultato | Prima | Dopo |
|---|---|---|
| R4 oltre 5 minuti | 14,1% | 15,6% |
| R4 oltre 10 minuti | 5,44% | 6,19% (titolo: «circa il 6%») |
| R4 grappolo + buco | 20,9% | 21,6% |
| R4 attesa in più (bassa-alta) | 1,6-2,4 min | 1,5-1,7 min |
| R4 giorni / copertura GPS | 6 feriali, 78,3% | 8 feriali, 79,5% |
| R6 (274 fermate, 179 senza posti, 12 punti, pareggio 21-28') | uguale | uguale |
| R8 modello del traffico | V0: errore 38,4%, ρ 0,605, 20 sensori | **V4**: errore 28,3%, ρ 0,639, 22 sensori (scelto dalla regola fissata prima, script 63) |
| R8 tratte di Torino / molto traffico | 540 (soglia 11.720) / 180 | 611 / 204 (soglia 10.677) |
| R8 km serviti dal TP | 95,3% | 95,6% |
| R8 forbice mezzi/auto (da 1,96 a 2,94) | invariata (la tabella dei tempi non cambia) | invariata |
| R1 esposti al traffico (a meno di 100 m) | 190.255 (22,6%) | 222.179 (26,4%) |
| R10 | 79.598 (9,5%) | uguale |

**Due correzioni di codice scoperte dal rilancio** (il modello di R8 è cambiato):
- lo script 92 aveva la soglia «molto trafficata» scritta a mano (11.720): ora la legge dal R8 (`universo_torino.soglie.q66`); il controllo «92 = R8» dà 204 = 204;
- `scripts/schede/r8.py` leggeva sempre `traffico_d/v0` e `varianti.v0`: ora usa la variante scelta (`variante_traffico`); testo sul modello e secondo tratto «da guardare» (corso Casale al posto di corso Moncalieri) vengono dai dati. `docs/R4_puntualita.md`, `R8_traffico.md`, `R1_servizi.md` aggiornati. `docs/R6_parcheggi.md` dice ancora «±38%» perché R6 usa il modello semplice (script 81): non cambia.

## Dalla bozza `C14_bozza.patch` (applicata, 12 file su 16)
`assets/animazioni.js` (nuovo), `gara.js` (giro, nome partenza, arrivo, mini), `mezzi.js` (giorni dalla raccolta), `sito.js` (numeri che salgono, 2,6 s, forbice), `stile.css` (titolo oro, anteprima), `index.html`, `comune.py` (niente «english»), `home.py` (`INIZIO_RACCOLTA`), `r1.py`, `r4.py`, `r10.py` (titoli e animazioni), `traduci.py`.

## Rifatto a mano
- `risultati.html`: attributi dei numeri che salgono (`attrConta`), ordine della scheda (domanda → numero → animazione → 3 punti → grafico → mappa → «Altri grafici» aperti → extra aperta → **una sola** parte chiusa «Come l'abbiamo calcolato e limiti»), via «In English», gara con `giro`.
- `r6.py`: titolo «2 fermate importanti su 3…» (frazione dai dati), numero grande 179, animazione delle fermate, altri grafici = gara, pareggio, interscambi con lo stato di riempimento (la bozza si applicava quasi tutta; mancava solo togliere `val`/`pieni`, già tolti da C13).
- `r8.py`: **l'area che si espande è l'animazione principale** (`anima` di tipo «area»), la gara dei 6 viaggi tipici va negli «Altri grafici».
- `testi.json`: 20 voci esatte e 20 modelli presi dalla bozza + 1 mia (titolo della gara). `schede_risultati.py`: 0 ATTENZIONE.
- `assets/area.js`: **versione piccola** (`Area.html({compatto: true})`): niente comandi né tabella, le due mappe crescono da sole da 0 a 60 minuti e ricominciano mentre si vedono; con «riduci movimento» ferme a 30 minuti. La grande non è cambiata. `animazioni.js` ha il tipo «area».
- Miniature: tolte `fai_miniature` e `MINIATURE` da `prova_pagine.py` e la cartella `assets/miniature/`. `assets/anteprime/` e `assets/readme/` non toccate.

## Prove (solo funzionamento)
pyflakes 0; `node --check assets/*.js` ok; schede 5, nessuna ATTENZIONE; numeri delle animazioni = rapporti (scheda 1 68,3/96,8/99,2; scheda 3 95+111+68 = 274, 12 punti; scheda 2 15,6 e 6,19; scheda 5 10 omini, 1 acceso); `prova_pagine.py`: 0 errori su 20 pagine (con Edge: **senza Playwright non rifà le anteprime `r/N.html` e le immagini del README**, che quindi mostrano ancora le pagine di prima). Nel browser integrato: tutte e 5 le animazioni della home e delle schede partono (anche l'area piccola), nessun errore in console; ordine delle parti verificato nel DOM.

## Scelte mie
- Titolo scheda 2 «Circa il 6%…» perché il dato nuovo è 6,19% (la regola dice «da round»).
- Scheda 4: nelle schede l'area ha la sua didascalia (frase dei 30 minuti) al posto della nota del vecchio grafico.
- Gara scheda 3: nessun luogo ha «arrivo»: arriva sempre a Piazza Castello.

## Da guardare (Leo, computer e telefono, chiaro e scuro)
Home: titolo oro, frase dei giorni (21), 5 riquadri animati (area piccola nel 4), numeri che salgono piano senza virgola né %. Schede: niente «In English», una sola parte chiusa, titoli nuovi, 5 animazioni, gara della scheda 3 che gira da sola, area della scheda 4 in cima. Mappa: gara piccola nel pannello dei parcheggi come prima.
