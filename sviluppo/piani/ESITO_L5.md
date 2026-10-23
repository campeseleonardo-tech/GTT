# Esito L5 — schede 1 e 4, testi onesti sui tempi in auto (24/10/2026)

## Cosa è cambiato
1. **Scheda 1** (`assets/animazioni.js`, `cerchi`): nel disegno SVG restano solo cerchi e casa (viewBox 270×270). Numeri e frasi sono HTML accanto (`.an-cer`, flex-wrap): sotto il disegno se la scheda è stretta; disegno al massimo 260 px, testo con `overflow-wrap:anywhere`. Stessi tempi dell'animazione (cerchi e righe in sequenza, numeri che salgono). Versione piccola (home): cerchi da 120 px e tre righe brevi «68,3% 5′», «96,8% 10′», «99,2% 15′», senza la frase lunga. «Riduci movimento»: tutto fermo e scritto. Provato nel browser (senza giudizio grafico): computer, righe dentro il contenitore, nessun scorrimento orizzontale; telefono 375 px, bordo destro delle righe a 336 px, nessun scorrimento.
2. **Scheda 4**: la gara non ha più le ore, solo le 8; gira da un viaggio all'altro. Nota: «alle 8 di un feriale», via la frase sulle altre ore. La linea «ora per ora» resta. Gara della scheda 3 invariata.
3. **Testi onesti** (schede 3 e 4, `docs/R8_traffico.md`, `docs/R6_parcheggi.md`, `testi.json`):
   - «limite basso / limite alto» e «auto lenta / veloce» → «stima con il rallentamento di Google» / «… dei sensori» (nelle gare: «Auto, stima Google» / «Auto, stima sensori»); «sta fra / stimati fra» → «due stime; il valore vero può stare anche fuori»;
   - via «decise/fissate prima dei numeri» dalla scheda 4 e dal documento R8, dove ora c'è: «Il metodo è cambiato 4 volte il 21/10 dopo le prime prove; le fasce sono state scelte dopo.» La regola ±0,3 del titolo resta, indicata come «fissata prima (blocco L3)»;
   - limite nelle schede 3 e 4: «Il rallentamento di Google è stato misurato su 6 percorsi in uscita dal centro. In entrata l'auto può essere più lenta.» (due frasi per il limite di 20 parole; per stare nei 4 limiti ho unito altri due limiti: scheda 4 «Fuori Torino mancano treni…» con «Senza i treni metropolitani…»; scheda 3 «costo del parcheggio» con «un solo punto per luogo»);
   - nomi JSON dei campi (`limite_basso`, `limite_alto`) invariati. Traduzioni in `testi.json`; in `traduci.py` tre parole nuove per le frasi con numeri («stima Google», «stima sensori», « o »).
   - Non toccato: «Soglie fissate prima dei numeri» della scheda 5 (R10), fuori dall'incarico.

## Testi SVG controllati (stima: caratteri × 0,6 × corpo, contro lo spazio fino al bordo del viewBox)
| Testo | Più lungo possibile | Stima | Spazio | Esito |
|---|---|---|---|---|
| cerchi (vecchio, nel disegno) | «tutti e 5 i servizi a 15 minuti a piedi», corpo 15 | 340 px da x=300 | 180 px | usciva: spostato in HTML |
| gara, nome corsia (x=8, corpo 13) | «Auto, stima sensori» 19 car. (EN «Car, sensor estimate») | 148 px | fino alla linea (388 px) | ok |
| gara, minuti a destra (x=404, corpo 15 grassetto) | «119 min» 7 car. | 63 px | 76 px | ok |
| gara, partenza in alto (x=8, corpo 14) | «Da Ponte Cavalieri Templari · 17:30» 35 car. | 294 px | 278 px prima dell'arrivo | **toccava l'arrivo**: ora corpo 12 se la stima supera lo spazio (gara.js) |
| gara, arrivo in alto (a destra, corpo 12) | «Piazza Castello» 15 car. | 108 px | – | ok |
| linea, etichette categorie (corpo 10, centrate) | «Autobus lento» ecc. fino a 20 car. (EN) | 120 px, mezzo = 60 | 56 px dal bordo | **usciva di 4 px nella prima e ultima**: ora centro tenuto a mezza larghezza dal bordo (risultati.html) |
| linea, valori e asse (corpo 10-11) | «1.234%» 6 car. | 40 px | 50 px | ok |
| dispersione, asse x (corpo 11, centrato) | 42 car. | 277 px | 422 px | ok |
| dispersione, asse y (ruotato, corpo 11) | 29 car. | 191 px | 194 px | ok, al limite |
| dispersione, etichette linee («1,5 volte», «il doppio») | 9 car. | 60 px | > 100 px | ok |
| fermate: nessun testo in SVG | – | – | – | ok |

`overflow:visible` su `.anima svg` **tolto**: non serve più (cerchi e gara non escono, le fermate hanno 40 unità di margine nel viewBox).

## Prove
pyflakes zero; `node --check assets/*.js` ok; `schede_risultati.py` nessuna ATTENZIONE; `04_genera_mappa`, `86_controlla_file_pagine` (0 da guardare) e `prova_pagine.py` (0 errori su 20 pagine; immagini di anteprima non fatte: manca Playwright). Ho lanciato i passi del `.bat` uno per uno (il `.bat` ha `pause`). `git grep` delle frasi vecchie: nessun testo rimasto (restano nomi di variabili e la scheda 5).

## Da guardare per Leo
Scheda 1 su computer e telefono (testo dentro la scheda, anche nella home); scheda 4 (gara alle 8 che cambia viaggio); testi delle schede 3 e 4 («due stime»).
