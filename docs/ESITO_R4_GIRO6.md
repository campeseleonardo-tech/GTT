# Esito Giro 6 del Risultato 4 (attese: via i giorni senza GPS)

**Esito complessivo: OK con 1 AVVISO** (nessun FERMO). Ramo `prova`, albero pulito, pull già aggiornato. Database in sola lettura.

| Passo | Esito |
|---|---|
| 1 - script 27: `giorni_gps_validi` | OK, con AVVISO (giorni esclusi diversi da quelli attesi) |
| 2 - script 70: stessi giorni, riepilogo | OK (bus 14.500 intervalli, sopra 10.000) |
| 3 - template: `ora=` senza `linea=` | OK |
| 4 - lanci | OK, 0 errori nella prova delle pagine |

## AVVISO - giorni esclusi
Il piano prevedeva che uscisse solo il 14/10. Applicando la regola scritta (corse viste almeno 0,5 x mediana del tipo) escono **tre** giorni:
- **14/10** (feriale): 1.605 corse viste, mediana del tipo 5.869;
- **18/10** (domenica): 716 corse viste, mediana 2.628. Con soli 2 domeniche la «mediana» è la media dei due giorni (716 e 4.540), quindi il giorno parziale esce e la domenica resta con 1 giorno (11/10);
- **21/10** (feriale): è comparso nel database (833 corse viste, giorno ancora parziale), quindi non era nei dati del Giro 5.
Nessuna correzione fatta: la regola è applicata come scritta. Se Leo preferisce tenere il 18/10, basta usare la mediana bassa dei giorni (non cambiato).

## Passo 1 - scripts/27_risultato4_regolarita.py: OK
- Aggiunte la costante `MIN_QUOTA_GIORNO_GPS = 0.5` e la funzione `giorni_gps_validi(con, giorni, trip_info)`: conta per giorno le corse viste nel GPS (stessa finestra 02-26 ore e stessa regola di `costruisci_passaggi_gps`: corsa nel GTFS, almeno 2 posizioni diverse) e tiene i giorni con almeno metà della mediana del loro tipo. Ritorna (giorni validi, esclusi con `giorno`, `corse_viste`, `mediana_tipo`).
- In `main`, con `--fonte gps` (non con `--prova`) i giorni esclusi non entrano negli aggregati; stampa su stderr «Giorno escluso (poco GPS)…». JSON: `"giorni_esclusi_gps"`; `giorni` conta solo i giorni usati; rapporto: riga «Giorni esclusi per poco GPS…» in COPERTURA DEL GPS.
- Giorni usati: 10, 11, 12, 13, 15, 16, 17, 19, 20/10 (6 feriali, 2 sabati, 1 domenica). Copertura GPS totale 78,3% (1.300.434 su 1.660.225).
- Controlli (uscita dello script):
```
  OK feriale: passaggi tram + metro + bus = citta' (944276 contro 944276)
  OK feriale: oltre 10 minuti (5.44%) <= oltre 5 minuti (14.1%)
  OK sabato: passaggi tram + metro + bus = citta' (244582 contro 244582)
  OK sabato: oltre 10 minuti (7.1%) <= oltre 5 minuti (16.8%)
  OK domenica: passaggi tram + metro + bus = citta' (111576 contro 111576)
  OK domenica: oltre 10 minuti (4.11%) <= oltre 5 minuti (12.0%)
  OK copertura GPS 78.3% (OK sopra 60%)
  OK oltre 5 minuti feriale col GPS: 14.1% (OK fra 8% e 25%)
  OK feriale: mediana -0.1 min fra -5 e +10
  OK sabato: mediana 0.3 min fra -5 e +10
  OK domenica: mediana -0.1 min fra -5 e +10
  OK corse osservate con almeno un passaggio di fine corsa: 88.0% (44976 su 51125; OK sopra 30%)
  OK linee utili: 54 linee da popolarita_zone.json
```

## Passo 2 - scripts/70_risultato9_attesa.py: OK
- Nuova costante `MIN_INTERVALLI_BUS_AVVISO = 10000`. Il giro completo usa `r4.giorni_gps_validi()` (stessi giorni dello 27; con `--prova` resta il solo 15/10), li scrive nel rapporto («Giorni esclusi per poco GPS…») e in JSON (`giorni_esclusi_gps`).
- In coda al rapporto «RIEPILOGO DEI DATI USATI (Giro 6)»: chiavi frequenti/usate e intervalli osservati e programmati per tram e bus, con OK/AVVISO sui bus. Uscita: chiavi 3.844 frequenti / 2.505 usate; tram 57.920 osservati (101.187 programmati); bus 14.500 osservati (28.302 programmati); **OK: bus sopra 10.000**.
- La soglia «dati scarsi» resta al 20%.

## Passo 3 - scripts/mappa_template.html: OK
`applicaLineaDaUrl()`: prima usciva subito se mancava `linea=`; ora legge `linea=` e `ora=` separatamente, applica la linea solo se c'è, e `ora=` vale anche da solo (esce solo se mancano entrambi). La mappa rigenerata contiene il nuovo codice (`if(!m && !mo) return`). Non provato a mano nel browser: coperto solo dalla prova delle pagine (0 errori).

## Passo 4 - lanci: OK
`27` -> `70` -> `04_genera_mappa.py` -> `schede_risultati.py` -> `prova_pagine_r6.py --senza-screenshot`: **0 errori sulle 13 pagine**. (Il primo lancio del 70 è fallito per un mio errore di sintassi nel riepilogo, corretto subito; l'esito sopra è dell'ultimo lancio.)

## Numeri prima/dopo
| Feriale | Prima (Giro 5) | Dopo (Giro 6) |
|---|---|---|
| giorni (feriali/sabati/domeniche) | 7/2/2 | 6/2/1 |
| passaggi | 885002 | 944276 |
| oltre 5 min % | 13.3 | 14.1 |
| oltre 10 min % | 5.05 | 5.44 |
| grappolo+buco % | 20.4 | 20.9 |
| mediana min | -0.1 | -0.1 |
| tram oltre5/oltre10/grap+buco | 13.0 / 5.12 / 25.5 | 14.4 / 5.66 / 26.7 |
| bus oltre5/oltre10/grap+buco | 13.4 / 5.03 / 16.8 | 14.0 / 5.38 / 17.1 |
| sabato oltre 5 % | 16.8 | 16.8 |
| domenica oltre 5 % | 11.4 | 12.0 |

| Attese feriale | Prima | Dopo |
|---|---|---|
| promessa_min | 4.85 | 4.73 |
| reale_min_bassa | 5.94 | 6.35 |
| reale_min_alta | 7.11 | 7.14 |
| in_piu_min_bassa | 1.09 | 1.62 |
| in_piu_min_alta | 2.26 | 2.4 |
| in_piu_pct_bassa | 22.2 | 34.1 |
| intervalli_osservati | 32825 | 72420 |
| corse_assenti_feed_pct | 14.5 | 13.3 |
| chiavi frequenti / usate | 3779 / 1133 | 3844 / 2505 |
| tram: promessa; in più bassa-alta; intervalli oss. | 4.83; 1.11-2.27; 32045 | 4.5; 1.77-2.4; 57920 |
| bus: promessa; in più bassa-alta; intervalli oss. | 5.52; 0.49-1.98; 780 | 5.58; 1.08-2.4; 14500 |

Il R4 cambia poco (oltre 5 min feriale da 13,3% a 14,1%), come previsto dal piano; l'attesa in più sale da 1,1–2,3 a 1,6–2,4 minuti e ora i bus pesano davvero (14.500 intervalli invece di 780).

MEMORIA_PROGETTO.md non toccata.
