# Esito — schede dei risultati, pagina di ingresso (21/10/2026)

Piano: `PIANO_SCHEDE.md` («Forma nuova»). Stato: **OK** = fatto e provato; **AVVISO** = fatto, con un limite da sapere.

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| Pagina dei risultati | OK | `simulazione.html` → `risultati.html` con `git mv`. Il vecchio indirizzo è una pagina minima che porta a `risultati.html` (anche con `#...`). Rimandi aggiornati: mappa (link «I risultati →»), script 86 (`FILE_FISSI`, README), prova delle pagine, `schede_risultati.py`, memoria, documenti. `git grep simulazione.html` non trova più nulla. |
| Forma nuova | OK | Ogni scheda ha il campo `forma`. In vista: etichetta, titolo-risposta, domanda in una riga, numero grande con spiegazione, un grafico principale, «Vedi sulla mappa», 3 punti chiave. Chiusi: altri grafici (al massimo 2), «Come l'abbiamo calcolato» (5 righe e criteri a 2 colonne), limiti (al massimo 4), «In English» (3 righe). |
| Parti tolte | OK | Non si mostrano più: «Il problema», «Prima e dopo», «Cosa cambia se lo cambiamo», «File del progetto», stato con le date, avvisi di sviluppo. I campi vecchi restano nel JSON. |
| Grafici nuovi | OK | Barre a 100% impilate (`pila100`) e linea per fasce orarie (`linea`). Le barre accettano un testo al posto del numero (classi di bisogno di R6). |
| Scheda R4 | OK | Come da richiesta. Parte chiusa sul calcolo con le 3 righe sul confronto con GTT e la frase sul 3,9%. «Quanto si aspetta alla fermata»: un punto chiave e un grafico, in una parte chiusa a parte. |
| Scheda R6 | OK | Barre dei 12 punti in 3 classi (terzili dei posti mancanti, 4+4+4), senza posti in grande. Riempimento degli interscambi di giorno e di notte (3 interscambi: Caio Mario e Fermi sono esclusi perché non affidabili). Criteri in 4 righe. Frase sul tempo mezzo pubblico contro auto nei limiti. |
| R1 e R8 | OK | Solo forma nuova, contenuti di oggi, testi accorciati. Cambieranno con `PIANO_RISULTATI.md` (parti A e D). |
| Pagina d'ingresso | OK | `index.html`: titolo, 3 righe, bottoni Mappa e Risultati, 4 riquadri letti da `data/schede_risultati.js`; ogni riquadro apre la scheda (`risultati.html#r4`). Aggiunta a `FILE_FISSI` dello script 86 (con anche il rimando `simulazione.html`). Funziona a 375 px. |
| Testi | OK | Lo script controlla ogni testo della forma: nessuna frase oltre 20 parole, nessuna delle parole vietate (Leo, giro, fase, versione, nomi di file, IMQ, Q001, 5T, GTFS). Risultato: 0 avvisi. |

## Titoli e numeri grandi

| Risultato | Titolo-risposta | Numero grande |
|---|---|---|
| R1 | Quasi tutti i torinesi hanno i servizi essenziali a 15 minuti a piedi | **1,3%** dei torinesi (10.919) non ha almeno uno dei 5 servizi a 15 minuti |
| R4 | I ritardi gravi sono circa il 5% dei passaggi | **5,4%** dei passaggi feriali arriva con oltre 10 minuti di ritardo |
| R6 | Servono parcheggi di scambio soprattutto su 12 assi d'ingresso | **179 fermate** importanti su 274, fuori dal centro, non hanno posti bastanti entro 400 metri a piedi |
| R8 | Quasi tutte le strade grandi di Torino hanno un mezzo pubblico vicino | **95,3%** dei km di strade grandi ha fermate frequenti vicine (327,3 su 343,3) |

## Prove

- `python scripts\schede_risultati.py`: 4 schede, 0 avvisi sui testi.
- `python scripts\86_prepara_pubblicazione.py`: `pubblica/` 12 file, 24,0 MB; README riscritto, 0 avvisi.
- `python scripts\prova_pagine_r6.py --senza-screenshot` e con `--cartella pubblica`: **0 errori su 18 pagine** (mappa, ingresso, 4 schede, elenco).
- Chromium, altezza della scheda chiusa, in schermate (1 = una schermata):

| | R1 | R4 | R6 | R8 |
|---|---|---|---|---|
| 1024 × 768 | 0,93 | 1,01 | 1,13 | 0,76 |
| 375 × 812 | 1,15 | 1,20 | 1,42 | 1,03 |

Tutte sotto una schermata e mezza; nessuno scroll orizzontale. Grafico a linea: etichette tagliate ai bordi, corrette; numeri nelle barre impilate mostrati solo sopra il 9%.

## AVVISO

- Una volta la prova ha dato «The browser is shutting down» (messaggio di chiusura di Edge, non dell'app); rifatta, 0 errori.
- R1: il grafico principale mostra i residenti senza il servizio, non ancora le soglie 5/10/15 minuti (`PIANO_RISULTATI.md`, parte A).
- R8: il grafico principale resta la barra km con o senza mezzo pubblico; la dispersione arriva con la parte D.
- R6: «Vedi sulla mappa» apre il tema dei parcheggi; R8 non ha un tema in mappa, quindi senza bottone.
- Le immagini della mappa per i riquadri dell'ingresso non ci sono (il piano le prevedeva): i riquadri hanno solo titolo e numero.
