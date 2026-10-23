# Esito L3 (23/10/2026, PC): bus contro auto a 4 ore del giorno

Scelte e regola del titolo come nel blocco L3 di `PROMPT_LAVORI.md`, non cambiate dopo aver visto i numeri.

## Durata
`--prova` (dati finti) e `--campione 10` (16-18 secondi per ora) prima; **calcolo intero in 208 secondi** (circa 1 minuto per ora, 381 origini r5py per ora): nessun `.bat` necessario. Comando nella fase «r6» di `rifai_tutto.py` dopo 94.

## Script 100 (`scripts/100_ore_del_giorno.py`, prossimo numero libero 101)
Riusa 93 e 94 (`comuni.carica_script`: `matrice_tp`, `matrice_auto`, `tempo_zone_*`, `riepilogo`, `punta`); i luoghi sono quelli di `r6_bus_contro_auto.json`; i parziali r5py sono uno per ora (`ore_del_giorno_parziale_*.npz`, fuori da git). Uscite: `data/processed/ore_del_giorno.json` (104 KB, per ora: 17 luoghi con tempi e pareggio, riepilogo delle coppie, le 100 coppie con più auto), `docs/rapporti/RAPPORTO_ORE_DEL_GIORNO.txt`.
Controlli: fattore alle 8 = 1,2 (come 93) ✔; fattore basso alle 8 = 2,1 ✔; alle 8 i tempi coi mezzi uguali a quelli di 94 (differenza massima 0,00 min su 17 luoghi) e di 93 (2.061 coppie, differenza massima 0,0) ✔; rapporto mediano alle 8 1,96 - 2,94 come 93 ✔; nessun tempo nullo, negativo o infinito ✔; 13:00 e 21:00 con auto più veloce ✔. **AVVISO**: i mezzi dai punti prioritari alle 21 non sono più lenti che alle 8 (mediana 34,5 contro 36,5 minuti): l'orario programmato non ha traffico e il tempo medio per il cambio conta poco.

## Tabella (coppie di zone Torino-Torino e Torino-cintura)
| Ora | Fattore sensori | Fattore Google scalato | Rapporto mediano (lenta - veloce) | Auto oltre 2 | Senza collegamento (auto) |
|---|---|---|---|---|---|
| 8:00 | 1,2 | 2,1 | 1,96 - 2,94 | 41% - 97% | 5.616 |
| 13:00 | 1,1 | 1,6 | 2,37 - 3,10 | 89% - 98% | 4.810 |
| 17:30 | 1,2 | 2,1 | 2,01 - 3,02 | 52% - 97% | 6.095 |
| 21:00 | 1,0 | 1,0 | 3,32 - 3,32 | 100% - 100% | 9.511 |

Punti prioritari del R6: pareggio mediano 21-28 minuti alle 8, 23-27 alle 13, 22-29 alle 17:30, 28 alle 21 (i due fattori coincidono); classi 0/1/11 a tutte le ore tranne alle 21 (0/0/12); interscambi 0/3/2, 0/2/3, 0/3/2, 0/0/5.

## Titolo della scheda 4
Regola: «a ogni ora» solo se a tutte le ore il rapporto mediano è entro ±0,3 da quello delle 8 con tutti e due i fattori. Alle 13 con il fattore lenta lo scarto è **+0,41** (2,37 contro 1,96) e alle 21 è +1,36: **il titolo resta «Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto»** e un punto chiave dice come cambia: «Nel giorno il rapporto mediano va da 2 a 3,3 (auto lenta) e da 2,9 a 3,3 (auto veloce)» (al posto delle 3 coppie peggiori, già nel grafico). Scheda 3: titolo invariato.

## Schede e gara
- `assets/gara.js`: un luogo può avere `ore` (campo facoltativo per corsa: `ora`); la gara corre le ore una dopo l'altra con l'ora scritta sopra la corsa e nella frase per il lettore di schermo; con «mini» e «riduci movimento» solo la prima. Etichette «traffico pesante/scorrevole» quando c'è l'ora. La gara piccola della mappa non cambia.
- Scheda 3: gara con le 4 ore per ognuno dei 17 luoghi (titolo «… alle 8, alle 13, alle 17:30 e alle 21 di un feriale»). Scheda 4: grafico a linea «Quante volte il tempo dell'auto, ora per ora» (2 serie) e gara dei 6 viaggi con le 4 ore, negli «Altri grafici» (che ora possono essere 4: `comune.py`). Home: invariata (area piccola nella 4, fermate nella 3, solo le 8 dove c'è la gara mini).
- Limite nuovo nelle schede 3 e 4 («Il rallentamento dell'auto alle altre ore viene dai sensori. Quello di Google si conosce solo alle 8 ed è stato scalato.»; due frasi perché una sola superava 20 parole), con traduzioni in `testi.json`. Se `ore_del_giorno.json` manca (o è campione/prova) le schede restano com'erano dopo L2.
- Giudizio di ogni ora nella gara del R6: stessa regola dello script 94 (rapporto ≤ 1,5; copiata in `r6.py` con un commento). Se i due fattori coincidono (21:00) il testo dice «circa X volte».

## Prove
pyflakes 0; `node --check`; schede 5, nessuna ATTENZIONE; `prova_traduzione` ok; `prova_pagine.py`: 0 errori su 20 pagine; nel browser integrato la gara delle schede 3 e 4 corre le 4 ore in fila (8:00 → 21:00) senza errori in console.

## Da guardare (Leo)
Schede 3 e 4: gara con le ore (nome, ora sopra la corsa; il giro passa al luogo dopo), linea ora per ora nella 4, frase sul cambiamento nel giorno nei punti chiave; la sera l'auto è una sola (i due fattori coincidono).
