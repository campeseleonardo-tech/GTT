# GTT - mobilità e trasporti di Torino

## Per chi e perché
Progetto di Leo, di studio e da portfolio. Direzione decisa il 9/10/2026: capire come funziona la
città (chi va dove, dove mancano servizi, dove sono le criticità) e pochi scenari "cosa succede se"
sull'accessibilità. Gioco e simulatore universale esclusi. Dettagli in sviluppo/MEMORIA_PROGETTO.md.

## Memoria
La memoria del progetto è sviluppo/MEMORIA_PROGETTO.md (decisioni, limiti, cose da fare). Leggila all'inizio. Aggiornala alla fine se hai deciso o scoperto qualcosa. Non creare altri documenti di memoria o di passaggio. I piani di lavoro vanno in sviluppo/piani/ (es. sviluppo/piani/PIANO_MAPPA.md).

## Come si lavora con Leo
Passo passo: un passo alla volta, decisioni importanti chieste prima, piccole scelte con valori predefiniti dichiarati. Spiegazioni semplici, senza gergo.

## Dati
Lo storico vero vive sul Raspberry Pi di casa ("leopi"; indirizzo, utente e chiave SSH stanno in config_locale.json nella radice, fuori da git: modello in scripts/config_locale.esempio.json); sul PC c'è la copia settimanale data/storico_backup.sqlite. Non modificare i dati in data/raw e lo storico: leggili e basta. Per prove lunghe parti da un campione piccolo.

## Ramo git
Sul PC di Leo si lavora sul ramo "prova": se all'inizio non sei su "prova", fermati e dillo a Leo.
In una sessione cloud (cartella diversa da `C:\projects\Progetti\GTT`, ramo `claude/...`) resta sul ramo della
sessione: Leo lo unisce poi in "prova". Nel cloud non ci sono `data/`, il Pi e Windows: fai le modifiche al codice
e lascia a Leo i passi che girano sui dati.
All'inizio di ogni lavoro controlla i rami: `python scripts/controlla_rami.py` (sul PC `scripts\CONTROLLA_RAMI.bat`). Se un ramo ha
commit non presenti in `origin/prova`, dillo a Leo prima di iniziare.

## Commit (Leo, 20/10/2026)
Alla fine del lavoro fai **sempre** commit e push da solo, con un messaggio chiaro:
- sul PC: `git add -A`, `git commit -m "..."`, `git pull --no-rebase origin prova`, `git push origin prova`;
- nel cloud: `git add -A`, `git commit -m "..."`, `git push -u origin <ramo della sessione>`.
Prima del commit controlla con `git status` che non entrino file da non salvare (`data/`, `.bak`, chiavi). Se il
pull dà un conflitto, fermati e dillo a Leo. Per i merge usa sempre `--no-edit` (altrimenti git apre un editor).

## Python
Sul PC si usa il python nel PATH (Python 3.14). NON usare Anaconda: il suo modulo json è rotto. Sul Pi Python 3.13.

## Come provare
- Script Python: eseguili davvero e controlla che i numeri abbiano senso (ordini di grandezza, totali, valori negativi).
- Se non hai un terminale sul PC, prepara un .bat a doppio clic e di' a Leo cosa deve vedere alla fine.
- Mappa HTML: dopo averla rigenerata, controlla che il file sia aggiornato e contenga i dati attesi. Non puoi vederla: di' a Leo esattamente quale file aprire e cosa dovrebbe vedere.
