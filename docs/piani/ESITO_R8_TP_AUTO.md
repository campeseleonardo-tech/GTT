# Esito — R8 parte D: dove il mezzo pubblico non conviene rispetto all'auto (21/10/2026)

Piano: `PIANO_RISULTATI.md`, parte D (D1, D2, D3). Script nuovo `scripts/93_tp_contro_auto.py` (sola lettura). Prossimo numero libero: 94.
Stato: **OK** = fatto e provato; **AVVISO** = fatto, con un limite da sapere.

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| Unità | OK | 71 zone IMQ con punti in `punti.json` (le 141 zone solo «porta» sono fuori); fino a 5 punti per zona, i più pesanti, pesi rinormalizzati. Tempo fra due zone = media pesata dei tempi fra i punti. |
| D1 tempi coi mezzi | OK | r5py come lo script 18 (stesso GTFS, stessa rete OSM), giorno 2026-10-12, partenza 7:45 con finestra di 30 minuti (7:45-8:15, mediana), mezzi pubblici + cammino, massimo 120 minuti. Prova su 10 zone: 17 secondi. Calcolo completo (359 origini): **31 secondi**, quindi **nessun `.bat`** (il salvataggio a tappe c'è lo stesso: `data/processed/tp_contro_auto_parziale.npz`). |
| D2 tempi in auto | OK | Rete del modello del traffico, cammino minimo come nello script 42, flusso libero. Ora di punta = tempo × 1,5 + 5 minuti. Sensibilità con 1,3 e 1,8. |
| D3 confronto | OK | Rapporto = tempo coi mezzi / tempo in auto. Auto della coppia = viaggi IMQ in auto conducente, partenza 6-10 (ore 6, 7, 8, 9), feriale. Classi (soglie cambiate il 21/10): sotto 2,5 conviene, 2,5-3,5 poco, oltre 3,5 non conviene. Il primo calcolo (1,5 e 2) resta nel JSON e nel rapporto, sotto «precedenti». |
| Controlli dello script | OK | Nessun tempo negativo o nullo; somma delle auto = totale IMQ 06-10 delle zone incluse (465.534); coppie senza collegamento contate a parte. Un primo lancio si è fermato per un errore di arrotondamento di 1 auto nella somma: corretto. |
| Scheda R8 | OK | `forma_r8` legge `tp_contro_auto.json`: titolo, dispersione (nuovo tipo di grafico in `risultati.html`), 3 punti chiave, limiti, inglese. 0 avvisi sui testi. Il 95,3% delle strade grandi è una riga. |
| Prove | OK | 93 (prova e completo), `schede_risultati.py`, `04_genera_mappa.py` (13,5 MB), `prova_pagine_r6.py`: **0 errori su 18 pagine**. Scheda R8 in Chromium a 375 px: 1,28 schermate chiusa, nessuno scroll orizzontale. |

## Risultato

- Titolo: **«Per 1 auto su 10 del mattino il mezzo pubblico impiega più di 3,5 volte l'auto»**.
- Auto del mattino su coppie «non conviene»: **27,844 su 275,943 (10.1%)**.
  Per classe: non conviene 27,844 auto in 306 coppie; poco 196,363 in 1840; conviene 51,736 in 361.
- Sensibilità al fattore di punta (soglie nuove): 1,3 → 22.1%; 1,5 → 10.1%; 1,8 → 5.0% (conviene 55.1%).
- **Soglie di prima (1,5 e 2), tenute per il confronto**: 1,3 → 99.2%; 1,5 → 98.6% (271,965 auto); 1,8 → 91.4%. Identici al primo calcolo.
- A parte: 2,463 coppie senza collegamento coi mezzi entro 120 minuti (25,389 auto); 164,203 auto dentro la stessa zona (non confrontate).

## Soglie cambiate (Leo, 21/10)

Con le soglie 1,5 e 2 il 98,6% delle auto era «non conviene» (AVVISO del controllo sopra il 60%): il rapporto distingueva poco, perché il tempo coi mezzi comprende cammino, attesa e cambi e l'auto è a flusso libero (rapporto mediano 2,9, minimo 1,57).
Con 2,5 e 3,5 la quota è 10.1% e il controllo non scatta. Il calcolo non è cambiato: i tempi e le coppie sono gli stessi, cambia solo la classe. I risultati con le soglie di prima sono nel JSON (`precedenti`) e nel rapporto, così alla fine si possono confrontare.
Resta vero che i tempi coi mezzi vengono da un motore (R5) e non da un calcolatore di percorsi reale: non li ho confrontati con uno. Mancano code vere (fattore fisso 1,5) e ricerca del parcheggio (5 minuti fissi).

## Le 15 coppie peggiori per auto coinvolte

| # | Coppia | Auto | Mezzi pubblici (min) | Auto di punta (min) | Rapporto |
|---|---|---|---|---|---|
| 1 | Leini → Caselle Torinese | 826 | 100 | 16 | 6.1 |
| 2 | Vinovo → Nichelino | 759 | 69 | 17 | 4.2 |
| 3 | Torino. Mirafiori Sud → Rivoli | 719 | 86 | 24 | 3.7 |
| 4 | Beinasco → Rivoli | 562 | 88 | 23 | 3.8 |
| 5 | Vinovo → Moncalieri | 539 | 90 | 22 | 4.1 |
| 6 | Volpiano → Settimo Torinese | 527 | 91 | 23 | 4.0 |
| 7 | Nichelino → Rivoli | 518 | 96 | 25 | 3.8 |
| 8 | Pianezza → Rivoli | 510 | 72 | 20 | 3.7 |
| 9 | Collegno → Venaria Reale | 473 | 73 | 21 | 3.5 |
| 10 | San Maurizio Canavese E Limitrofi → Cirie' | 470 | 82 | 16 | 5.0 |
| 11 | Volpiano → Leini | 439 | 89 | 16 | 5.7 |
| 12 | Torino. Madonna Del Pilone → Torino. Borgo Po E Cavoretto | 438 | 63 | 18 | 3.5 |
| 13 | Caselle Torinese → Leini | 438 | 100 | 17 | 6.0 |
| 14 | Nichelino → Vinovo | 415 | 64 | 17 | 3.8 |
| 15 | Vinovo → Torino. Mirafiori Sud | 383 | 86 | 20 | 4.4 |

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
