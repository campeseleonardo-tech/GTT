# Esito Giro 5 del Risultato 4 (tutto sul GPS)

**Esito complessivo: OK con 3 AVVISI** (nessun FERMO). Ramo `prova`, pull già aggiornato, albero pulito all'inizio. Database in sola lettura.

| Passo | Esito |
|---|---|
| 1 - script 27 sul GPS | OK |
| 2 - script 70 sul GPS | OK, con AVVISO 2 |
| 3 - mappa_template.html | OK |
| 4 - schede_risultati.py | OK (toccata anche la parte attese, come dal piano; vedi nota) |
| 5 - lanci | OK, 0 errori nella prova delle pagine |

## Avvisi
1. **14/10 quasi senza GPS**: solo 1.605 corse viste (contro 6.500-7.600 degli altri feriali). Il giorno entra nei 7 feriali ma pesa poco. Controllo: nessuna correzione fatta.
2. **Attese (script 70) molto più magre**: con la regola «oltre 20% di corse assenti = dati scarsi» e il GPS che manca per circa il 14,5% delle corse, le chiavi usate scendono da 3.254 a 1.133 e gli intervalli osservati da 147.925 a 32.825. I bus restano con soli 780 intervalli: la media delle attese ora è quasi tutta tram. Da decidere con Leo se alzare la soglia dei dati scarsi.
3. **Finestra del GPS dalle 02:00 locali** (come script 70/91): i passaggi fra mezzanotte e le 2 non sono misurati. La fascia «notte» è quindi solo parziale (già dichiarato nei limiti della scheda).

## Passo 1 - scripts/27_risultato4_regolarita.py: OK
- Portate dallo script 91 (con commento «dal Giro 4, script 91»): `_segmento`, `cerca_vincolata`, `passaggi_corsa`, costanti `DIST_GPS_M`, `SEGMENTO_MAX_S`, `MAX_RITARDO_VERO_MIN`. Script 91 invariato. Aggiunte `carica_fermate()` e `costruisci_passaggi_gps(con, giorno, trip_info, nome_linea, prog, fermate)`, che ritorna le stesse tuple di `costruisci_passaggi` più la copertura.
- `FONTE_ARRIVI = "gps"`, opzione `--fonte feed` (calcolo di prima).
- Con gps: aggregati dal GPS; dal feed solo città e modi in `"confronto_feed"` (con scarti D3 e `lettura_lontana_per_tipo`). JSON nuovo: `"fonte"`, `"copertura_gps"`, `"regole_gps"`; `"scarti"` ora contiene solo i passaggi GPS usati.
- Rapporto: riga in testa sul GPS, sezioni nuove COPERTURA DEL GPS e CONFRONTO COL FEED (dopo «I 3 NUMERI»), avviso finale e paragrafo sull'oltre 10 minuti adattati; le altre sezioni hanno gli stessi titoli. Tolto il paragrafo «ATTENZIONE… stima alta» (valeva solo per il feed).
- Prima: `Passaggi osservati (ultime letture)…`, `[MISURATO] dal feed GTFS-Realtime GTT; …`; dopo: `Passaggi con GPS valido: …`, `[MISURATO] con il GPS dei mezzi GTT …`.
- Controlli (uscita dello script):
```
  OK feriale: passaggi tram + metro + bus = citta' (885002 contro 885002)
  OK feriale: oltre 10 minuti (5.05%) <= oltre 5 minuti (13.3%)
  OK sabato: passaggi tram + metro + bus = citta' (244582 contro 244582)
  OK sabato: oltre 10 minuti (7.1%) <= oltre 5 minuti (16.8%)
  OK domenica: passaggi tram + metro + bus = citta' (126821 contro 126821)
  OK domenica: oltre 10 minuti (3.85%) <= oltre 5 minuti (11.4%)
  OK copertura GPS 77.3% (OK sopra 60%)
  OK oltre 5 minuti feriale col GPS: 13.3% (OK fra 8% e 25%)
  OK feriale: mediana -0.1 min fra -5 e +10
  OK sabato: mediana 0.3 min fra -5 e +10
  OK domenica: mediana -0.1 min fra -5 e +10
  OK corse osservate con almeno un passaggio di fine corsa: 86.9% (43677 su 50271; OK sopra 30%)
  OK linee utili: 54 linee da popolarita_zone.json
```
  Copertura per giorno (GPS valido / programmato): 10/10 79,2%, 11/10 74,7%, 12/10 75,6%, 13/10 73,5%, 14/10 74,3%, 15/10 77,9%, 16/10 82,1%, 17/10 78,5%, 18/10 67,7%, 19/10 70,5%, 20/10 83,1%; totale 77,3% (1.256.405 su 1.625.310).
- Durata: 2 min 28 s.

## Passo 2 - scripts/70_risultato9_attesa.py: OK (vedi avviso 2)
- `elabora_giorno(..., fermate)`: `stimato` da `r4.costruisci_passaggi_gps`; `nel_feed` = corse viste nel GPS; `linee_coperte` dalle linee di quelle corse.
- Rapporto: «assenti dal feed» -> «assenti dal GPS» (tolta la seconda cifra «assenti anche dal GPS», ora uguale alla prima); testi di Limiti/Esempi aggiornati; il «CONTROLLO COL GPS» resta con la nota «è un controllo del feed, non della fonte usata» e lavora sui passaggi stimati dal feed (non su quelli del GPS, che darebbero differenza zero).
- Durata: 1 min 10 s.

## Passo 3 - scripts/mappa_template.html: OK
```
-const r4Classe = v => v<2.5?0 : v<5?1 : v<7.5?2 : v<10?3 : 4;      // verde -> rosso con PAL_VR
+const r4Classe = v => v<10?0 : v<15?1 : v<20?2 : v<30?3 : 4;      // verde -> rosso con PAL_VR
-  const cl=["sotto 2,5%","2,5-5%","5-7,5%","7,5-10%","oltre 10%"];
+  const cl=["sotto 10%","10-15%","15-20%","20-30%","oltre 30%"];
-    +`<div class="et" style="display:block">Periodo ${r4Data(M.periodo.da)} - ${r4Data(M.periodo.a)}; una linea è colorata se ha almeno ${M.min_passaggi} passaggi osservati in quella fascia.`
+    +`<div class="et" style="display:block">Periodo ${r4Data(M.periodo.da)} - ${r4Data(M.periodo.a)}, misurato con il GPS dei mezzi; una linea è colorata se ha almeno ${M.min_passaggi} passaggi osservati in quella fascia.`
-   desc:"Quanti passaggi arrivano con più di 5 minuti di ritardo, linea per linea, nell'ora scelta con il cursore. Misurato dal feed GTT.",
+   desc:"Quanti passaggi arrivano con più di 5 minuti di ritardo, linea per linea, nell'ora scelta con il cursore. Misurato con il GPS dei mezzi.",

```
(più la riga del periodo: «…, misurato con il GPS dei mezzi»). Mappa rigenerata (`04_genera_mappa.py`, 1 min 9 s): contiene «sotto 10%» e «misurato con il GPS dei mezzi»; **linee colorate in mappa: 86** (erano 90).

## Passo 4 - scripts/schede_risultati.py: OK
- Metodo, risposta (confronto col feed dal JSON, oltre 10 minuti con il 2,3 di GTT), limiti (tolti i due del feed; aggiunti copertura dal JSON e i 60 metri), avviso e `in_english` allineati. Numeri tutti letti dal JSON (la distanza 60 m da `regole_gps`), salvo il 2,3 (`rif_gtt_ritardo10_pct`).
- Nota: nel piano si diceva «scheda R4 con la parte attese»: ho adattato anche i testi della scheda attese (`scheda_r9`: «assenti dal GPS», metodo, limiti, avviso, inglese) perché dicevano ancora «feed». In «limiti» della scheda R4 ho tolto anche la frase «manca circa 1 corsa su 5 (il 15/10: 80%…)» (numero scritto a mano, valeva per il feed) e l'ho sostituita con una frase senza numeri.
- Il testo «giorni non tutti interi» (`GIORNI_PARZIALI_R4`) resta quello verificato sul feed il 18/10.

## Passo 5 - lanci: OK
`27` (2 min 28 s) -> `70` (1 min 10 s) -> `04_genera_mappa.py` (1 min 9 s) -> `schede_risultati.py` -> `prova_pagine_r6.py --senza-screenshot` (1 min 5 s): **0 errori sulle 13 pagine** (mappa con tema puntualita: 0 righe di errore, scheda: 0).

## Numeri nuovi contro quelli di prima
| Feriale | Prima (feed) | Dopo (GPS) |
|---|---|---|
| passaggi | 1150666 | 885002 |
| oltre 5 min % | 5.2 | 13.3 |
| oltre 10 min % | 0.0 | 5.05 |
| grappolo+buco % | 10.5 | 20.4 |
| mediana min | -0.4 | -0.1 |
| tram: oltre 5 / oltre 10 / grappolo+buco | 4.6 / 0.0 / 13.8 | 13.0 / 5.12 / 25.5 |
| bus: oltre 5 / oltre 10 / grappolo+buco | 5.4 / 0.0 / 8.4 | 13.4 / 5.03 / 16.8 |

Fasce (feriale, % oltre 5 min)
Prima:
```
punta_mattina |   154642 |       44.7 |       51.3 |         4.0 |    -0.7 | 2.9
giorno        |   479464 |       39.2 |       55.3 |         5.6 |    -0.4 | 3.5
punta_sera    |   203749 |       42.2 |       52.2 |         5.6 |    -0.5 | 3.4
sera          |   215966 |       38.0 |       56.2 |         5.8 |    -0.3 | 3.6
notte         |    96845 |       38.0 |       58.7 |         3.3 |    -0.4 | 2.5
```
Dopo:
```
punta_mattina |   120916 |       39.2 |       48.6 |        12.2 |    -0.2 | 5.8
giorno        |   361366 |       37.1 |       48.3 |        14.7 |    -0.0 | 6.8
punta_sera    |   139060 |       39.1 |       45.4 |        15.5 |    -0.1 | 7.5
sera          |   153936 |       37.7 |       47.7 |        14.6 |    -0.0 | 6.7
notte         |   109724 |       44.2 |       50.5 |         5.4 |    -0.6 | 3.3
```

10 linee peggiori per ritardo
Prima:
```
 1. linea 17     19.6% in ritardo | 28160 passaggi | mediana 1.1 min | p90 6.8 min
 2. linea 6      12.7% in ritardo | 5408 passaggi | mediana 0.2 min | p90 5.6 min
 3. linea 66     12.6% in ritardo | 5158 passaggi | mediana 0.2 min | p90 5.6 min
 4. linea 68     10.3% in ritardo | 26639 passaggi | mediana 0.0 min | p90 5.1 min
 5. linea 61     10.1% in ritardo | 21770 passaggi | mediana 0.1 min | p90 5.0 min
 6. linea 60      8.9% in ritardo | 10403 passaggi | mediana 0.1 min | p90 4.6 min
 7. linea 33      8.8% in ritardo | 26691 passaggi | mediana 0.2 min | p90 4.7 min
 8. linea 32      8.2% in ritardo | 11129 passaggi | mediana 0.2 min | p90 4.4 min
 9. linea 76      8.1% in ritardo | 18076 passaggi | mediana 0.0 min | p90 4.4 min
10. linea 72      8.0% in ritardo | 13511 passaggi | mediana -0.1 min | p90 4.4 min
```
Dopo:
```
 1. linea 17     37.1% in ritardo | 25830 passaggi | mediana 2.4 min | p90 14.5 min
 2. linea 6      35.3% in ritardo | 4078 passaggi | mediana 1.9 min | p90 16.4 min
 3. linea 19     26.5% in ritardo | 3466 passaggi | mediana 1.9 min | p90 11.6 min
 4. linea 66     25.8% in ritardo | 4518 passaggi | mediana 1.3 min | p90 10.2 min
 5. linea 68     25.2% in ritardo | 15585 passaggi | mediana 0.7 min | p90 12.3 min
 6. linea 33     24.3% in ritardo | 21331 passaggi | mediana 1.3 min | p90 9.1 min
 7. linea 61     23.1% in ritardo | 18945 passaggi | mediana 0.9 min | p90 11.2 min
 8. linea 4      22.3% in ritardo | 55495 passaggi | mediana 0.8 min | p90 10.0 min
 9. linea 72     21.2% in ritardo | 10397 passaggi | mediana 0.4 min | p90 9.6 min
10. linea 60     19.0% in ritardo | 8130 passaggi | mediana 0.9 min | p90 9.4 min
```

Attesa (feriale, linee frequenti)
| | Prima | Dopo |
|---|---|---|
| promessa_min | 4.76 | 4.85 |
| reale_min_bassa | 5.36 | 5.94 |
| reale_min_alta | 6.33 | 7.11 |
| in_piu_min_bassa | 0.6 | 1.09 |
| in_piu_min_alta | 1.57 | 2.26 |
| in_piu_pct_bassa | 12.4 | 22.2 |
| intervalli_osservati | 147925 | 32825 |
| corse_assenti_feed_pct | 10.3 | 14.5 |
| chiavi frequenti / usate | 3780 / 3254 | 3779 / 1133 |

Confronto col feed (stesso calcolo, regole D1-D3): feriale oltre 5 5,2%, oltre 10 0,0%, grappolo+buco 10,5%; tram 4,6% / 0,0% / 13,8%; bus 5,4% / 0,0% / 8,4%.

Nota: sui soli 15 e 16/10 la prova del Giro 4 dava 15,4% oltre 5; su tutti i 7 feriali il GPS dà 13,3%: normale, i giorni sono diversi.

## git status (prima del commit)
```
 M docs/RAPPORTO_RISULTATO4.txt
 M docs/RAPPORTO_RISULTATO9_ATTESA.txt
 M mappa_torino.html
 M scripts/27_risultato4_regolarita.py
 M scripts/70_risultato9_attesa.py
 M scripts/mappa_template.html
 M scripts/schede_risultati.py
```
(`data/` ignorata da git: JSON e schede rigenerati in locale.) MEMORIA_PROGETTO.md non toccata.
