# Esito — R8 parte D: dove il mezzo pubblico non conviene rispetto all'auto (21/10/2026)

Piano: `PIANO_RISULTATI.md`, parte D (D1, D2, D3). Script nuovo `scripts/93_tp_contro_auto.py` (sola lettura). Prossimo numero libero: 94.
Stato: **OK** = fatto e provato; **AVVISO** = fatto, con un limite da sapere.

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| Unità | OK | 71 zone IMQ con punti in `punti.json` (le 141 zone solo «porta» sono fuori); fino a 5 punti per zona, i più pesanti, pesi rinormalizzati. Tempo fra due zone = media pesata dei tempi fra i punti. |
| D1 tempi coi mezzi | OK | r5py come lo script 18 (stesso GTFS, stessa rete OSM), giorno 2026-10-12, partenza 7:45 con finestra di 30 minuti (7:45-8:15, mediana), mezzi pubblici + cammino, massimo 120 minuti. Prova su 10 zone: 17 secondi. Calcolo completo (359 origini): **31 secondi**, quindi **nessun `.bat`** (il salvataggio a tappe c'è lo stesso: `data/processed/tp_contro_auto_parziale.npz`). |
| D2 tempi in auto | OK | Rete del modello del traffico, cammino minimo come nello script 42, flusso libero. Ora di punta = tempo × 1,5 + 5 minuti. Sensibilità con 1,3 e 1,8. |
| D3 confronto | OK | Rapporto = tempo coi mezzi / tempo in auto. Auto della coppia = viaggi IMQ in auto conducente, partenza 6-10 (ore 6, 7, 8, 9), feriale. Classi: sotto 1,5 conviene, 1,5-2 poco, oltre 2 non conviene. |
| Controlli dello script | OK | Nessun tempo negativo o nullo; somma delle auto = totale IMQ 06-10 delle zone incluse (465.534); coppie senza collegamento contate a parte. Un primo lancio si è fermato per un errore di arrotondamento di 1 auto nella somma: corretto. |
| Scheda R8 | OK | `forma_r8` legge `tp_contro_auto.json`: titolo, dispersione (nuovo tipo di grafico in `risultati.html`), 3 punti chiave, limiti, inglese. 0 avvisi sui testi. Il 95,3% delle strade grandi è una riga. |
| Prove | OK | 93 (prova e completo), `schede_risultati.py`, `04_genera_mappa.py` (13,5 MB), `prova_pagine_r6.py`: **0 errori su 18 pagine**. Scheda R8 in Chromium a 375 px: 1,28 schermate chiusa, nessuno scroll orizzontale. |

## Risultato

- Titolo: **«Per 9.9 auto su 10 del mattino il mezzo pubblico impiega più del doppio»**.
- Auto del mattino su coppie «non conviene»: **271,965 su 275,943 (98.6%)**.
  Per classe: non conviene 271,965 auto in 2484 coppie; poco 3,977 auto in 23 coppie; conviene 0.
- Sensibilità al fattore di punta: 1,3 → 99.2%; 1,5 → 98.6%; 1,8 → 91.4% (conviene 0.6%).
- A parte: 2,463 coppie senza collegamento coi mezzi entro 120 minuti (25,389 auto); 164,203 auto dentro la stessa zona (non confrontate).

## AVVISO: oltre il 60% delle auto è su coppie «non conviene» (98,6%)

Il controllo scatta e non è un errore dello script: le somme tornano e il tempo in auto passa il controllo di buon senso. Spiegazione:

1. **Il confronto è porta a porta contro un'auto a flusso libero.** Il tempo coi mezzi comprende cammino fino alla fermata, attesa e cambi; l'auto no. Anche senza il fattore di punta il rapporto mediano è 5,5 (nessuna coppia sotto 1,5). Col fattore 1,5 e i 5 minuti è 2,9.
2. **Il rapporto non distingue.** Con fattore 1,5 nessuna coppia sta sotto 1,5 (il minimo è 1,57); con fattore 1,8 «conviene» è solo lo 0,6% delle auto. La classe «non conviene» è quasi tutto: quello che informa è quanto sta sopra la linea del doppio (dispersione), non la classe.
3. **Il tempo coi mezzi pubblici è alto anche per tragitti brevi.** Media pesata: 58 minuti contro 20 in auto di punta. I tempi del TP vengono da un motore (R5), non da un calcolatore di percorsi reale: non li ho confrontati con uno.
4. **Mancano le code vere** (fattore fisso 1,5, lo stesso per tutte le coppie) **e la ricerca del parcheggio** (5 minuti fissi): l'auto è più lenta di così nelle coppie verso il centro. Il risultato è un ordine di grandezza, non una misura.

Cosa fare: tenere la scheda così com'è (ordine di grandezza e confronto fra coppie), o cambiare le soglie (per esempio 2,5 e 3,5). Decisione di Leo.

## Le 15 coppie peggiori per auto coinvolte

| # | Coppia | Auto | Mezzi pubblici (min) | Auto di punta (min) | Rapporto |
|---|---|---|---|---|---|
| 1 | Collegno → Grugliasco | 1.668 | 30 | 12 | 2.6 |
| 2 | Nichelino → Moncalieri | 1.408 | 54 | 17 | 3.2 |
| 3 | Torino. Crocetta → Torino. Centro | 1.355 | 23 | 10 | 2.2 |
| 4 | Grugliasco → Collegno | 1.348 | 30 | 12 | 2.5 |
| 5 | Torino. San Paolo → Torino. Centro | 1.342 | 35 | 13 | 2.7 |
| 6 | Torino. Mirafiori Nord → Torino. Santa Rita | 1.324 | 23 | 9 | 2.5 |
| 7 | Torino. San Donato → Torino. Centro | 1.269 | 21 | 10 | 2.1 |
| 8 | Torino. Barriera di Milano → Torino. Falchera | 1.208 | 28 | 11 | 2.5 |
| 9 | Rivoli → Collegno | 1.172 | 33 | 14 | 2.4 |
| 10 | Moncalieri → Torino. Nizza Millefonti | 1.149 | 46 | 18 | 2.6 |
| 11 | Torino. Mirafiori Sud → Torino. Mirafiori Nord | 1.108 | 42 | 15 | 2.8 |
| 12 | Rivalta di Torino → Torino. Centro | 1.082 | 84 | 35 | 2.4 |
| 13 | Torino. Parella → Torino. Pozzo Strada | 1.038 | 19 | 9 | 2.1 |
| 14 | Alpignano → Rivoli | 1.037 | 50 | 16 | 3.1 |
| 15 | Collegno → Rivoli | 1.029 | 32 | 14 | 2.4 |

## Controllo di buon senso: percorsi noti (minuti)

La coppia Piazza Castello → Collegno deve stare in auto di punta fra 20 e 35 minuti (Fase 5): **24.7 minuti (13.1 a flusso libero) → OK**. Fra parentesi, con fattore 1,3 e 1,8.

| Percorso | Auto, flusso libero | Auto di punta (1,3-1,8) | Mezzi pubblici |
|---|---|---|---|
| Piazza Castello → Collegno | 13.1 | 24.7 (22.0-28.6) | 50 |
| Piazza Castello → Venaria Reale | 12.7 | 24.1 (21.5-27.9) | 70 |
| Piazza Castello → Settimo Torinese | 14.4 | 26.6 (23.7-30.9) | 67 |
| Piazza Castello → Moncalieri | 11.4 | 22.1 (19.8-25.5) | 51 |
| Piazza Castello → Orbassano | 18.0 | 32.0 (28.4-37.4) | 79 |
| Piazza Castello → Rivoli | inf | inf (inf-inf) | 69 |

## Non fatto

- D4 (vista nuova «Dove i mezzi non convengono» nella mappa) e D5: non richiesti in questo passo.
- Per circoscrizione e per zona sulla scheda: la quota per zona è nel JSON (`per_zona`), non ancora mostrata.
