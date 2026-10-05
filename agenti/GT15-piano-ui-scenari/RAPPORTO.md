# Rapporto dell'agente GT15-piano-ui-scenari

## Cosa ho fatto
- Ho analizzato a fondo `scripts/04_genera_mappa.py`, `scripts/mappa_template.html`, `MEMORIA_PROGETTO.md` e `docs/FONTI_DATI.md` per catalogare lo stato corrente della mappa e comprendere i limiti dei dati.
- Ho redatto il documento `docs/PIANO_UI_E_SCENARI.md` rispettando tutte le sezioni richieste, con termini chiari adatti a un lettore non programmatore.
- Nella sezione "UI oggi" ho censito nel dettaglio ogni singolo livello (8), tema (9), controllo (16) e scheda al clic (6) presente nel codice.
- Nella sezione "UI proposta" ho formulato la riduzione a 4 temi chiari, l'eliminazione dei temi ridondanti (es. zone 2011) e una struttura universale e standardizzata per le schede informative al clic con schema testuale.
- Nella sezione "Dati di traffico" ho distinto con precisione dati affidabili (GPS mezzi, sensori attivi, velocità storiche) e non affidabili (sensori muti, ritardi senza trip_id), indicando le regole visive per separare misurato e stimato.
- Nella sezione "Base per gli scenari" ho delineato un'architettura a varianti leggere (`data/scenari/`) che non tocca i dati base e calcola indicatori di offerta e popolazione servita.
- Nella sezione "Ordine di lavoro" ho programmato 5 passi chiari e sequenziali (GT16-GT20), indicando i file coinvolti per ciascuno.
- Ho registrato 4 domande chiuse con opzione "decidi tu" in `agenti/GT15-piano-ui-scenari/DOMANDE.md`.

## Scelte provvisorie adottate (default)
- 4 temi primari: 1) Servizio e abitanti, 2) Traffico e velocità, 3) Tempo reale e flotta, 4) Pendolarismo intercomunale.
- Unificazione dei dati di traffico 5T e velocità commerciale GTT nello stesso tema per confrontare la congestione stradale con il rallentamento del trasporto pubblico.
- Struttura dello scenario basata su file di varianti JSON/testo (es. aggiunta/modifica corse o fermate) senza duplicazione del dataset GTFS.
- Indicatore primario per gli scenari focalizzato sulla popolazione residente raggiunta entro 400 metri da un servizio frequente, dato che la matrice passeggeri per sezione non è disponibile.

## Cosa Leo deve decidere o valutare
- Verificare se la riorganizzazione a 4 temi risponde alle sue esigenze di semplicità d'uso (vedi prima domanda in `DOMANDE.md`).
- Confermare se preferisce il traffico 5T e la velocità delle linee GTT insieme nello stesso tema o separati.
- Esaminare l'ordine dei prossimi compiti (GT16 per i temi, GT17 per le schede, GT18 per il traffico, GT19 per il motore scenari, GT20 per la visualizzazione scenari).
