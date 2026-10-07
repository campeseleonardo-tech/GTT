origine: agente GT09-qualita
stato: bozza

## Cosa funziona
- La raccolta dei dati dei mezzi GTT ha prodotto 233 399 righe di posizione, con un intervallo mediano di 61 secondi tra una lettura e l’altra. In ogni lettura si registrano da un minimo di 1 a un massimo di 261 veicoli, con una mediana di 201 veicoli per lettura, indicando una buona copertura della flotta.
- I sensori 5T hanno inviato 287 letture, con un intervallo mediano di 301 secondi (vicino al previsto 5 minuti). Di queste, il 79 % riporta un flusso di traffico maggiore di zero, e 97 sensori su 109 hanno mostrato almeno una misurazione di flusso positiva.
- Il sistema di logging degli errori ha registrato solo un singolo evento (HTTP 503) durante il periodo osservato, suggerendo che la connessione alle fonti dati è generalmente stabile.

## Problemi trovati
- **Campi corsa e velocità vuoti nei dati GTT**: tutte le 233 399 righe hanno il campo “corsa” vuoto e il campo “velocità” NULL (100 %). Questo impedisce di calcolare ritardi, velocità effettiva o di distinguere corse attive da veicoli fermi, limitando la realisticità della simulazione sulla mappa.
- **Lunghi buchi nelle letture dei mezzi GTT**: si osservano intervalli senza dati fino a 18,2 minuti (es. 04/10 00:55‑01:13), 11,1 minuti (due occorrenze) e altri minori. Durante questi periodi la mappa mostrerebbe posizioni obsolete o nessun veicolo, riducendo l’affidabilità del dato in tempo reale.
- **Accuratezza zero in molti sensori 5T**: 49 sensori su 109 (≈45 %) hanno accuratezza dichiarata 0,0. Non è noto se questo valore significhi “nessun dato disponibile” o “sensore spento”, il che rende difficile interpretare correttamente il livello di traffico riportato da quei sensori.
- **Sensori senza flusso mai misurato**: 12 sensori su 109 (≈11 %) non hanno mai mostrato flusso > 0. Potrebbero essere offline, mal configurati o posizionati in zone a traffico nullo, ma senza ulteriori informazioni non si può distinguerne la causa.
- **Limite dell’orario osservato**: le timestamp delle letture GTT si concentrano nelle ore notturne (dalle 23:43 alle 00:22 circa) e quelle dei 5T nelle stesse fasce. Non disponiamo ancora di un campione diurno, necessario per valutare il servizio nelle ore di punta.

## Cosa non sappiamo ancora
- Se l’accuratezza 0,0 dei sensori 5T indica l’assenza di dati o un sensore inattivo.
- Perché i campi “corsa” e “velocità” nei feed GTT sono sempre vuoti; se il provider li omette o se lo script di raccolta non li estrae correttamente.
- Come variano il numero di mezzi in servizio e la frequenza delle letture durante le ore diurne, soprattutto in fascia di punta.
- Se il singolo errore HTTP 503 è un caso isolato o un sintomo di problemi intermittenti di connettività alle API GTT.
- Se i sensori 5T con accuratezza 0,0 ma occasionalmente con flusso > 0 esistono (i dati mostrano che per accuratezza 0,0 le righe con flusso>0 sono 8 997 su 14 063 ≈ 64 %), il che richiede una interpretazione più fine.

## Prossimi passi consigliati
1. **FACILE** – Verificare la documentazione dei feed 5T (o contattare il provider) per capire il significato esatto dell’accuratezza 0,0 e se i sensori con quel valore sono semplicemente inattivi.  
2. **FACILE** – Pianificare un raccolto diurno (avviare gli script 01 e 02 in ora di punta) per ottenere un campione rappresentativo di traffico GTT e 5T durante il giorno.  
3. **MEDIO** – Indagare se il feed GTT in tempo reale fornisce i campi “trip_id” e “speed” e, nel caso, modificare lo script di raccolta per estrarli (se necessario, proporre la modifica in DECISIONS.md).  
4. **MEDIO** – Analizzare i buchi nelle letture GTT per verificare se sono associati a linee specifiche, orari o zone geografiche, allo scopo di capire se il problema è di copertura o di segnale.  
5. **DIFFICILE** – Sviluppare un metodo di stima della velocità dei veicoli a partire dalle posizioni consecutive (quando disponibili) per colmare almeno parzialmente l’assenza del campo “velocità”.  
6. **FACILE** – Migliorare il logging degli errori affinché catturi più dettagli (es. codici di risposta, messaggi di timeout) per individuare meglio eventuali problemi di connettività.
