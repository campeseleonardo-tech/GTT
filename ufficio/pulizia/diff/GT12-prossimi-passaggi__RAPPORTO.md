# Rapporto attività GT12-prossimi-passaggi

## Cosa è stato fatto
- Aggiunto caricamento dello script data/processed/orari_fermate.js con gestione di errore (window.ORARI=null) prima dello script principale della mappa.
- Modificato il blocco che genera la scheda/tooltip della fermata (cercaTip) per mostrare, quando disponibili, i prossimi 4 passaggi programmati per ciascuna linea che serve la fermata, con indicazione delle corse del giorno successivo se necessario.
- Rispettato il principio di onestà: i dati sono chiaramente etichettati come "Orario programmato (non è il tempo reale)" nella sezione dei prossimi passaggi.
- Le modifiche sono locali e non influiscono sul funzionamento esistente se il file di orari è mancante.

## Scelte
- Il formato di visualizzazione dei prossimi passaggi è: HH:MM (minuti da ora) con eventuale marca <small>(domani)</small> per le corse del giorno successivo.
- Se la fermata non ha linee individuabili tramite il nome in s.r, non vengono mostrati i passaggi (nessun errore).
- Il numero di prossimi passaggi mostrati è 4, o meno se non ci sono abbastanza corse oggi e domani (mostriamo comunque la prima di domani se necessario).
- La ricerca della linea ID corrispondente al nome viene fatta scorrendo D.rotte; si assume che i nomi in s.r corrispondano esattamente al campo .s di D.rotte.

## Cosa Leo deve decidere o review
- Verificare che la visualizzazione dei prossimi passaggi sia chiara e non confondibile con i dati in tempo reale.
- Eventualmente ajustare la soglia di 4 passaggi o il formato di visualizzazione.
