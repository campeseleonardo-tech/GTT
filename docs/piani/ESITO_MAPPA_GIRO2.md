# Esito — mappa, giro 2 (21/10/2026)

Piano: `PIANO_MAPPA.md`, sezioni 4 e 5. File: `scripts/04_genera_mappa.py`, `scripts/mappa_template.html`,
`scripts/86_prepara_pubblicazione.py`. Mappa: 13.061.568 → 13.138.524 byte (13,1 MB; +0,08 MB per i dati dei sensori).

## Per punto

| Punto | Esito | Note |
|---|---|---|
| Velocità bus su tutti i giorni dello storico | OK | Tolto `VEL_GIORNI = 28` e il filtro sulla data. Storico in sola lettura (`file:…?mode=ro`, già così). Lo storico è lungo solo 18 giorni, quindi i numeri non cambiano (stesse 4.983.330 righe lette). |
| AVVISO se un tipo di giorno ha meno di 3 giorni | OK | Stampato dal 04: **solo 2 sabati** (13 feriali, 3 domeniche). In mappa il testo dice «2 sabati (pochi: dato provvisorio)». |
| Sensori da `velocita_5t.json` dentro la mappa | OK | Nuovo `D.t5` (97 sensori con dati, 6.662 celle affidabili); `stat.js` non è più caricato dalla mappa né copiato dallo script 86. Il file `velocita_5t.json` è del 18/10 (periodo 9-18/10, 6 feriali, 2 sabati, 2 domeniche): **non ho rilanciato lo script 26**; va rilanciato prima di rigenerare se si vogliono giorni nuovi. |
| Legenda «media di N giorni feriali/sabati/domeniche» | OK | Sia per i bus sia per i sensori; scheda del sensore «Media di». |
| «Tutti i servizi» in «Servizi a portata», predefinita | OK | Prima voce del menu, scelta all'apertura del tema. |
| Punteggio 0-100 = media dei percentili dei 5 gruppi | OK | Percentile a posizione media su tutte le 8.317 sezioni della mappa; valore mancante = 0 servizi. Calcolato a parte per «a piedi» e per «coi mezzi» (per ogni ora). |
| Legenda verde→rosso, 5 classi | OK | Cinque gruppi con lo stesso numero di sezioni (soglie 20, 34, 41, 62, 79 a piedi); estremi «meno serviti / più serviti». |
| Clic sulla sezione: 5 numeri | OK | Punteggio + per ogni gruppo servizi raggiungibili e «più di N% delle sezioni». Provato in Chromium: sezione cliccata = 75, uguale al calcolo indipendente in Python (75,2). |

Scelta di metodo (AVVISO, diversa dal piano): il punteggio si calcola **nel browser** all'avvio, non nel 04, per non aggiungere
~8.000 × 25 numeri alla mappa (peso, giro 4). Nessun campo nuovo in `D.sezioni`, quindi niente da aggiungere alla proiezione `sez`.
Chi cambia l'ora richiama già `aggiornaLegenda()` (il punteggio coi mezzi dipende dall'ora; «Quando» compare con «Mezzi pubblici»).

## Sezioni di controllo (a piedi 15' e coi mezzi 45' alle 8; valori = servizi raggiungibili, tra parentesi la posizione 0-100)

| Sezione | Abitanti | A piedi: punteggio | Scuole | Salute | Negozi | Fermate | Verde | Coi mezzi: punteggio |
|---|---|---|---|---|---|---|---|---|
| **Centrale** — Torino, Piazza Castello (12720000081) | 221 | **92** | 60 (97) | 46 (100) | 4.242 (99) | 104 (96) | 98 (68) | **93** |
| **Periferica** — Torino, Falchera (12720002764) | 558 | **48** | 7 (46) | 6 (45) | 191 (54) | 42 (55) | 40 (39) | 47 |
| **Periferica** — Torino, Mirafiori Sud (12720002788) | 1.888 | **46** | 7 (46) | 7 (49) | 152 (52) | 36 (51) | 33 (35) | 56 |
| **Cintura** — Venaria Reale (12920000068) | 336 | **38** | 7 (46) | 5 (41) | 14 (33) | 28 (43) | 27 (30) | 40 |
| Cintura — Rivoli, vicino al centro (12190000004) | 170 | 59 | 16 (61) | 16 (72) | 231 (56) | 36 (51) | 73 (56) | **34** |

Medie su tutte le sezioni: Torino 71,5 (a piedi) e 73,6 (mezzi); cintura 29,7 e 27,7. I numeri hanno senso: centro altissimo (92-93),
periferia di Torino a metà (46-56), cintura bassa; a Rivoli, paese con centro compatto, a piedi va bene (59) ma coi mezzi crolla (34).
In mappa, in tutta l'area di Torino prevale il verde e la cintura è rossa, con isole più chiare nei comuni grandi.

## Prove

- `python scripts\04_genera_mappa.py`: OK.
- `python scripts\prova_pagine_r6.py --senza-screenshot`: **0 errori** su 13 pagine.
- Chromium: legenda del tema, clic su una sezione (scheda con i 5 numeri), tema «Velocità e traffico» senza `stat.js` (`window.STAT` assente), legende «Media di 13 giorni feriali» / «2 sabati (pochi: dato provvisorio)», fonti con le date dei sensori.

## Da sapere

- **AVVISO** — `velocita_5t.json` è del 18/10: i sensori arrivano al 18/10, i bus al 21/10. Rilanciare lo script 26 prima del prossimo giro, se serve.
- **AVVISO** — «Tutti i servizi» fuori Torino usa servizi OpenStreetMap, meno completi: nota già in legenda.
- Non fatto, come richiesto: sezioni 3 e 6-8.
