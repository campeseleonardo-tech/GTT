# GT09 - statistiche sui dati raccolti (2026-10-05 02:38)

Database: data/storico.sqlite, 28.3 MB. Orari in UTC (Torino = UTC+2 d'estate, +1 d'inverno).

- tabella mezzi_gtt: 233399 righe
- tabella flussi_5t: 31283 righe
- tabella sensori_5t: 109 righe
- tabella errori: 1 righe

## Mezzi GTT (posizioni)
- letture: 1409, dal 2026-10-03 23:43 al 2026-10-05 00:22; intervallo mediano 61 s
- buchi piu' lunghi (nessuna lettura): 18.2 min da 04/10 00:55 a 04/10 01:13; 11.1 min da 04/10 21:35 a 04/10 21:46; 11.1 min da 04/10 01:16 a 04/10 01:27; 7.0 min da 04/10 00:37 a 04/10 00:44; 6.0 min da 03/10 23:49 a 03/10 23:55
- mezzi per lettura: minimo 1, mediana 201, massimo 261
- righe 233399; con corsa (trip) vuota: 233399 (100%); con velocita' non misurata (NULL): 233399 (100%); veicoli distinti 386, linee distinte 82
- letture per ora UTC: 00h:71, 01h:37, 02h:59, 03h:59, 04h:59, 05h:59, 06h:59, 07h:59, 08h:59, 09h:59, 10h:59, 11h:59, 12h:59, 13h:59, 14h:59, 15h:59, 16h:59, 17h:59, 18h:60, 19h:59, 20h:59, 21h:48, 22h:59, 23h:72
- mezzi medi in servizio per ora UTC: 00h:10, 01h:7, 02h:20, 03h:75, 04h:141, 05h:165, 06h:185, 07h:204, 08h:213, 09h:216, 10h:207, 11h:213, 12h:238, 13h:253, 14h:253, 15h:254, 16h:256, 17h:255, 18h:233, 19h:174, 20h:126, 21h:118, 22h:105, 23h:44

## Flussi 5T (sensori traffico)
- letture: 287, dal 2026-10-03 23:41 al 2026-10-05 00:37; intervallo mediano 301 s (atteso 300)
- sensori in anagrafica 109, visti nei dati 109
- accuratezza dichiarata (valore: n. sensori): 0.0: 49, 80.0: 2, 95.0: 18, 100.0: 40
- righe 31283; con flusso>0: 24687 (79%); con velocita'>0: 24687 (79%); flusso NULL 0; velocita' NULL 0
- sensori che hanno mostrato flusso>0 almeno una volta: 97 su 109
- per accuratezza (accuratezza: sensori, righe con flusso>0 / righe): 0.0: 49, 8997/14063; 80.0: 2, 574/574; 95.0: 18, 4826/5166; 100.0: 40, 10290/11480
- media per ora UTC (solo righe con flusso>0), formato ora: flusso/velocita': 00h:112.8/68.4, 01h:87.4/71.0, 02h:80.4/70.5, 03h:88.9/70.6, 04h:111.4/69.9, 05h:129.9/69.1, 06h:187.9/68.2, 07h:306.4/65.8, 08h:389.6/64.2, 09h:413.4/63.9, 10h:426.0/64.5, 11h:327.7/66.7, 12h:348.0/65.4, 13h:445.7/63.8, 14h:499.5/62.4, 15h:564.4/61.7, 16h:589.6/60.9, 17h:560.1/61.1, 18h:394.2/63.8, 19h:277.2/66.1, 20h:231.5/67.2, 21h:173.3/68.5, 22h:167.5/64.9, 23h:226.7/58.2

## Errori registrati dalla raccolta
- GTT: «HTTP Error 503: Service Unavailable» x1, dal 2026-10-04T21:30 al 2026-10-04T21:30

