# Esito — R8 parte D: tempi coi mezzi pubblici contro auto, calcolo corretto (21/10/2026)

Piano: `PIANO_RISULTATI.md`, parte D. Script `scripts/93_tp_contro_auto.py`. Questa è la **seconda versione del calcolo**: la prima aveva due errori
(cammino a 3,6 km/h e coppie fra comuni della cintura senza treni e altre aziende) e due soglie scelte dopo aver visto i numeri.
Stato: **OK** = fatto e provato.

## Cosa è cambiato

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| 1 Velocità a piedi | OK | `speed_walking=4.8` nella chiamata r5py, come lo script 18 (80 m al minuto). La firma del file parziale ora comprende la velocità: il calcolo vecchio non viene riusato. |
| 2 Punti non collegati | OK | Zone e percorsi noti sono agganciati al nodo più vicino della più grande componente fortemente connessa della rete. **Spostati 1 punti su 359** (al massimo 52 m): è il punto del percorso noto verso Rivoli. Nuovo controllo: nessun tempo infinito in auto fra zone (0 coppie, 0 percorsi noti). |
| 3 Tre gruppi | OK | Zona «Torino» = nome che comincia con «Torino,» (dopo la pulizia di «01 Torino-»). Controllata sul file vero: coincide con i codici Q e con la macro «01 Torino» (23 zone su 71). Non ho usato la regola del comune 1272. (a) Torino-Torino, (b) Torino-cintura e cintura-Torino, (c) cintura-cintura. Il risultato principale è (a)+(b); (c) è a parte, con la scritta «dati del mezzo pubblico incompleti: mancano treni e bus di altre aziende». Le coppie senza collegamento sono contate per gruppo. |
| 4 Misure senza soglia | OK | Titolo = rapporto mediano pesato per le auto. Fasce fisse: sotto 1,5, 1,5-2, 2-3, oltre 3. Sensibilità al fattore di punta 1,3 / 1,5 / 1,8 sul mediano e sulle fasce. Tolte le classi «conviene / poco / non conviene» e le soglie 2,5 e 3,5. I due calcoli di prima sono nel JSON sotto `precedenti`, con la nota «calcolati con cammino a 3,6 km/h: superati». |
| 5 Scheda R8 | OK | Titolo-risposta, barre delle auto per fascia (gruppi a+b), dispersione con le linee a 1,5 e a 2, punti chiave (quota oltre 2, 3 coppie peggiori, 95,3% delle strade), limiti con la frase sui comuni della cintura. Testi senza avvisi. Chiusa, 1,03 schermate a 1024 px. |
| Prove | OK | 93 (prima `--prova 10`, poi completo: 50 secondi), `schede_risultati.py`, `04_genera_mappa.py` (13,5 MB), `prova_pagine_r6.py` (0 errori su 18 pagine). Controlli dello script tutti OK (somma delle auto = 465.534). |

## Risultato (gruppi a+b)

- **Titolo: «Al mattino, coi mezzi pubblici si impiega in media 2,5 volte il tempo dell'auto»** (rapporto mediano 2,52, 220.307 auto).
- Quota di auto con rapporto oltre 2: **91,0%**.
- Nessun numero dipende da una soglia scelta dopo: le fasce sono fisse.

### Fasce e mediana per gruppo (fattore di punta 1,5)

| Gruppo | Coppie | Auto | Rapporto mediano | sotto 1,5 | 1,5-2 | 2-3 | oltre 3 | Senza collegamento (a parte) |
|---|---|---|---|---|---|---|---|---|
| (a) Torino-Torino | 506 | 103.190 | 2,44 | 1.752 (1,7%) | 15.707 (15,2%) | 77.794 (75,4%) | 7.937 (7,7%) | 0 coppie, 0 auto |
| (b) Torino-cintura (e cintura-Torino) | 1555 | 117.117 | 2,58 | 0 (0,0%) | 2.408 (2,1%) | 101.678 (86,8%) | 13.032 (11,1%) | 653 coppie, 5.616 auto |
| (ab) principale: Torino-Torino e Torino-cintura | 2061 | 220.307 | 2,52 | 1.752 (0,8%) | 18.115 (8,2%) | 179.472 (81,5%) | 20.969 (9,5%) | 653 coppie, 5.616 auto |
| (c) cintura-cintura | 658 | 61.808 | 2,96 | 0 (0,0%) | 94 (0,2%) | 33.952 (54,9%) | 27.762 (44,9%) | 1598 coppie, 13.600 auto |

Nota: le colonne delle fasce sono «auto (% delle auto del gruppo)».

### Sensibilità al fattore di punta (gruppi a+b)

| Fattore | Rapporto mediano | Oltre 2 | sotto 1,5 | 1,5-2 | 2-3 | oltre 3 |
|---|---|---|---|---|---|---|
| 1,5 | 2,52 | 91,0% | 1.752 (0,8%) | 18.115 (8,2%) | 179.472 (81,5%) | 20.969 (9,5%) |
| 1,3 | 2,78 | 95,9% | 621 (0,3%) | 8.520 (3,9%) | 145.050 (65,8%) | 66.116 (30,0%) |
| 1,8 | 2,20 | 77,1% | 2.424 (1,1%) | 48.066 (21,8%) | 166.566 (75,6%) | 3.251 (1,5%) |

## Prima e dopo: percorsi noti (minuti)

Piazza Castello → Collegno coi mezzi scende da 50 a **47** (sotto i 50 di prima). In auto resta in fascia 20-35 (24.7). Rivoli in auto era «infinito», ora è 18.2 minuti a flusso libero.

| Percorso | Mezzi pubblici prima (3,6 km/h) | Mezzi pubblici dopo (4,8 km/h) | Auto, flusso libero | Auto di punta (1,3-1,8) |
|---|---|---|---|---|
| Piazza Castello → Collegno | 50 | 47 | 13.1 | 24.7 (22.0-28.6) |
| Piazza Castello → Venaria Reale | 70 | 64 | 12.7 | 24.1 (21.5-27.9) |
| Piazza Castello → Settimo Torinese | 67 | 62 | 14.4 | 26.6 (23.7-30.9) |
| Piazza Castello → Moncalieri | 51 | 48 | 11.4 | 22.1 (19.8-25.5) |
| Piazza Castello → Orbassano | 79 | 74 | 18.0 | 32.0 (28.4-37.4) |
| Piazza Castello → Rivoli | 69 | 66 | 18.2 | 32.3 (28.7-37.8) |

## Confronto con i calcoli superati

- Prima, soglie 1,5 e 2: «non conviene» 98,6% delle auto.
- Prima, soglie 2,5 e 3,5: «non conviene» 10,1% delle auto.
- Ora, senza soglie: rapporto mediano 2,52; oltre 2 il 91,0% delle auto. Il cammino corretto e il solo ambito Torino spostano il mediano da 2,9 a 2,5.
- Il gruppo (c) mostra la distorsione dei dati mancanti: mediano 2,96, 44,9% delle auto oltre 3, e 1598 coppie senza collegamento.

## Le 15 coppie peggiori per auto coinvolte (rapporto oltre 2, solo gruppi a e b)

«Peggiori» = quelle con più auto fra le coppie con rapporto oltre 2, come dice il piano; il rapporto di ognuna è nell'ultima colonna.

| # | Coppia | Auto | Mezzi pubblici (min) | Auto di punta (min) | Rapporto |
|---|---|---|---|---|---|
| 1 | Torino, San Paolo → Torino, Centro | 1.342 | 31 | 13 | 2,4 |
| 2 | Torino, Mirafiori Nord → Torino, Santa Rita | 1.324 | 19 | 9 | 2,1 |
| 3 | Torino, Barriera di Milano → Torino, Falchera | 1.208 | 24 | 11 | 2,2 |
| 4 | Moncalieri → Torino, Nizza Millefonti | 1.149 | 43 | 18 | 2,4 |
| 5 | Torino, Mirafiori Sud → Torino, Mirafiori Nord | 1.108 | 38 | 15 | 2,5 |
| 6 | Rivalta di Torino → Torino, Centro | 1.082 | 80 | 35 | 2,3 |
| 7 | Torino, Borgo Po E Cavoretto → Torino, Centro | 970 | 33 | 14 | 2,5 |
| 8 | Nichelino → Torino, Nizza Millefonti | 968 | 31 | 15 | 2,1 |
| 9 | Torino, Mirafiori Sud → Torino, Centro | 941 | 44 | 21 | 2,1 |
| 10 | Torino, Pozzo Strada → Grugliasco | 929 | 34 | 14 | 2,5 |
| 11 | Torino, Mirafiori Nord → Torino, Nizza Millefonti | 917 | 38 | 15 | 2,5 |
| 12 | Rivoli → Torino, Centro | 910 | 63 | 27 | 2,4 |
| 13 | Torino, Vanchiglia → Torino, Centro | 901 | 30 | 13 | 2,4 |
| 14 | Torino, Madonna Del Pilone → Torino, Vanchiglia | 894 | 35 | 12 | 2,8 |
| 15 | Torino, San Paolo → Torino, Crocetta | 893 | 22 | 10 | 2,3 |

## Da sapere

- Il gruppo (b) va letto con cautela: lato cintura mancano treni e altre aziende (653 coppie senza collegamento, 5.616 auto, escluse dal numero).
- I tempi coi mezzi vengono dal motore R5 sul solo orario GTT: non li ho confrontati con un calcolatore di percorsi reale.
- Non fatto: D4 (vista in mappa). La quota per zona è nel JSON (`per_zona`), non sulla scheda.
