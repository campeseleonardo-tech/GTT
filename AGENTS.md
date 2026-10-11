# GTT - mobilità e trasporti di Torino

## Per chi e perché
Progetto di Leo, di studio e da portfolio. Direzione decisa il 9/10/2026: capire come funziona la
città (chi va dove, dove mancano servizi, dove sono le criticità) e pochi scenari "cosa succede se"
sull'accessibilità. Gioco e simulatore universale esclusi. Dettagli in MEMORIA_PROGETTO.md.

## Memoria
La memoria del progetto è MEMORIA_PROGETTO.md (decisioni, limiti, cose da fare). Leggila all'inizio. Aggiornala alla fine se hai deciso o scoperto qualcosa. Non creare altri documenti di memoria o di passaggio. I piani di lavoro vanno in docs/ (es. docs/PIANO_ACCESSIBILITA.md).

## Come si lavora con Leo
Passo passo: un passo alla volta, decisioni importanti chieste prima, piccole scelte con valori predefiniti dichiarati. Spiegazioni semplici, senza gergo.

## Dati
Lo storico vero vive sul Raspberry Pi "leopi" (192.168.8.200); sul PC c'è la copia settimanale data/storico_backup.sqlite (oltre 300 MB). Non modificare i dati in data/raw e lo storico: leggili e basta. Per prove lunghe parti da un campione piccolo.

## Ramo git
Si lavora sul ramo "prova". Se all'inizio non sei su "prova", fermati e dillo a Leo.

## Python
Sul PC si usa il python nel PATH (Python 3.14). NON usare Anaconda: il suo modulo json è rotto. Sul Pi Python 3.13.

## Come provare
- Script Python: eseguili davvero e controlla che i numeri abbiano senso (ordini di grandezza, totali, valori negativi).
- Se non hai un terminale sul PC, prepara un .bat a doppio clic e di' a Leo cosa deve vedere alla fine.
- Mappa HTML: dopo averla rigenerata, controlla che il file sia aggiornato e contenga i dati attesi. Non puoi vederla: di' a Leo esattamente quale file aprire e cosa dovrebbe vedere.
