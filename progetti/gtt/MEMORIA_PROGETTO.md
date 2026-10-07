# Memoria del progetto GTT

Ultimo aggiornamento: 4 ottobre 2026 (mappa funzionante sul PC dell'utente). Tienila aggiornata: è il file da incollare/farmi leggere
all'inizio di ogni nuova sessione, così non si riparte da zero.

## Obiettivo

Mappa web interattiva di Torino (stile Google Maps, in HTML) con: domanda e offerta di mezzi,
punti critici, flussi in tempo reale (simulati dove non misurati), il più vicino possibile agli
orari veri. Per ora solo studio personale, forse da condividere. Tutti i mezzi e tutta l'area
possibile; si parte da Torino città più cintura.

## Decisioni prese

- Pagina HTML locale, senza server esterno.
- Raccolta continua dei dati reali: per ora sul PC, più avanti sul Raspberry Pi se necessario (192.168.8.200).
- Dati locali (SQLite), nessun cloud. Pochi token: i calcoli pesanti girano in Python, non in chat.
- Nessuna costruzione della mappa finché i dati non sono ispezionati.
- Gli script trovano da soli la cartella chiamata GTT: i dati vanno in `GTT\\data\\raw` e i rapporti in `GTT\\docs`, ovunque si lanci lo script.
- Provare gli script su copie: i file in `data/raw` non si toccano.

## Cosa è verificato (aggiornato 4/10/2026 con i file veri scaricati dall'utente)

- GTFS GTT statico: valido dal 1/10/2026 al 31/1/2027 (versione 20261002). 215 linee (tram, metro, bus, funicolare),
  7045 fermate, 966.946 passaggi programmati, 201.302 punti di tracciato. Le corse hanno direction_id.
- Posizioni dei mezzi GTT (tempo reale): funzionano. 110 mezzi su 58 linee il sabato sera alle 22:45. Ogni mezzo ha
  linea, coordinate e id veicolo, ma NON il trip_id: si lega alla linea, non alla corsa. Gli id linea coincidono con il GTFS.
- Ritardi corse GTT (trip_update): al momento della prova il file conteneva 0 corse. Da riprovare di giorno.
- Avvisi GTT: file di 134 KB, non ancora decodificato.
- Feed 5T flussi: 112 sensori (non 91), su un'area che va oltre Torino (lat 44,39-45,93; lng 7,48-8,89). Al momento
  della prova 83 sensori avevano accuracy=0 e flusso 0, e 29 avevano flusso > 0. Da riconfrontare di giorno: non so
  ancora se accuracy=0 significa "nessun dato" o "sensore spento". Il file usa uno schema XML con namespace.
- Zone statistiche Torino scaricate (CSV e shapefile, dati del 2011).
- ISTAT pendolarismo 2011 (scaricabile, non ancora scaricato): comune e sezione di censimento, con sesso, mezzo, fascia
  oraria di partenza, durata. Lavoro e studio.
- ISTAT pendolarismo 2021: lavoro solo nel browser dati ISTAT; studio (pubblicato 22/9/2026) è una stima a livello comunale.
- Basi territoriali ISTAT 2021: sezioni di censimento con popolazione/famiglie/abitazioni (Piemonte: R01_21.zip).
- PUMS Torino: dati del 2008 in PDF. Utile come confronto storico, non come base.

## Cosa NON è verificato

- Qualità dei dati di giorno (ritardi, sensori 5T, numero di mezzi in ora di punta): serve un campione diurno.
- Esistenza di dati su bici/sharing, parcheggi, treni (SFM): non trovati.
- Dati ISTAT sugli addetti (dove si lavora) a livello di sezione: non risultano.

## Limiti da ricordare quando si legge la mappa

- Il traffico è misurato solo in 91 punti; il resto è stima.
- La domanda per orario viene dal 2011 (residenti che vanno a lavorare o studiare): mancano turisti, acquisti, svago.
- Bici e pedoni: nessun dato.
- Distinguere sempre sulla mappa "misurato" da "stimato".

## Mappa (4/10/2026)

`mappa_torino.html` generata da `scripts/04_genera_mappa.py` (+ `mappa_template.html`). Tutto in un file, motore di mappa
scritto a mano (nessuna libreria), sfondo CARTO/OpenStreetMap da internet. Livelli: zone (passaggi/ora per km²), linee
(corse/ora), fermate (passaggi/ora), traffico 5T, mezzi GTT. Offerta per giorno tipo (feriale/sabato/domenica) e ora.
Proiezione delle zone verificata: area totale 130,0 km² (Torino ~130 km²) e coordinate corrette.
NON include la domanda (persone): le zone statistiche del Comune non hanno la popolazione; servono i dati ISTAT.
NON testata con lo sfondo reale (il mio ambiente non raggiunge i server delle mattonelle): provata solo con sfondo assente.
Il traffico e i mezzi sono una fotografia dell'ultimo scaricamento: per aggiornarli rilanciare 01 e 04.

## Stato

- Mappa funzionante: `mappa_torino.html`. Se la pagina appare bianca, la causa è il programma con cui si apre (anteprima che blocca
  gli script): aprirla con Chrome, Edge o Firefox. La pagina mostra un avviso giallo quando gli script non partono.
- Per aggiornarla: `01_scarica_dati.py`, poi `04_genera_mappa.py`, poi riaprire il file.
- Gli script vanno lanciati da `GTT\scripts`: trovano da soli la cartella GTT.

## Decisioni del 4/10/2026

- Primo passo: livello Domanda con ISTAT (matrice pendolarismo 2011 a livello di sezione di censimento, scaricata dall'utente a mano).
- Punti critici = poca offerta per la gente, traffico lento, mezzi in ritardo.
- Area: Torino e cintura.
- Raccolta continua: per ora sul PC (giorno e notte), poi sul Raspberry Pi se necessario (ultima parola del 4/10/2026).
- Sezioni di censimento cambiate tra 2011 e 2021: accettato un accorpamento approssimato.
- Richieste dati (MTM, telefonia): rimandate a più avanti.

## File ISTAT in cartella (4/10/2026)

- Arrivati: pendolarismo 2021 lavoro e studio (comune contro comune, niente mezzo/orario), note e "leggimi", note sulle matrici di contiguità e dei tempi di viaggio.
- Mancano: matrice 2011 a livello di sezione (download .crdownload incompleto), basi territoriali 2021 Piemonte (confini e popolazione).
- Dettagli in `docs/istat/NOTE_FILE_ISTAT.md`. Organizzazione cartelle: `data/raw/istat/...` per i dati, `docs/istat/` per i documenti.

## Prossimi passi (in ordine)

1. [ ] (dopo ISTAT) Campione diurno: rilanciare 01 di giorno (meglio ora di punta) e 02; guardare cosa significa accuracy=0 nei sensori 5T,
   e se i ritardi corse (trip_update) di giorno contengono dati.
2. [ ] Scaricare a mano i file ISTAT (vedi `docs/FONTI_DATI.md`): pendolarismo 2011 a livello di sezione, basi territoriali 2021
   Piemonte, pendolarismo lavoro 2021. Servono per la domanda.
3. [ ] Aggiungere alla mappa il livello Domanda (residenti e spostamenti per zona e fascia oraria) e un primo indicatore di
   punti critici (domanda alta contro offerta bassa, per ora e tipo di giorno).
4. [ ] Avviare la raccolta sul PC con `raccolta_continua.bat` (doppio clic; PC acceso e senza stop). Script 03 ora senza librerie, parte GTT provata su file reale (110 mezzi). Controllare dopo un giorno la dimensione di `data/storico.sqlite`.
5. [ ] Mandare le richieste dati (bozze in `docs/`): MTM per IMQ 2022; telefonia mobile.
6. [ ] Dopo qualche settimana di raccolta: mappa dei flussi reali, punti critici da dati misurati, simulazione dei flussi tarata
   sui sensori 5T (misurato e stimato sempre distinti sulla mappa).
7. [ ] Eventuale condivisione della mappa (per ora solo uso personale).

## Piano per fasi

1. Verifica dei dati (in corso).
2. Raccolta continua (5T ogni 5 minuti, mezzi GTT ogni ~60 secondi).
3. Mappa statica: offerta (passaggi GTT per ora) contro domanda (popolazione e pendolarismo).
4. Simulazione animata tarata sui conteggi reali.
5. Punti critici da dati misurati dopo qualche settimana di raccolta.

## Dati ISTAT 4/10/2026
- `Dati_regionali_2021.zip` = indicatori per sezione (R01 = Piemonte: Torino 4.292 sezioni, 848.748 abitanti), SENZA confini. Servono i confini `R01_21.zip` (https://www.istat.it/storage/cartografia/basi_territoriali/2021/R01_21.zip): da scaricare a mano, il mio ambiente non può.
- `BT21-sez-M04.zip` = sezioni di infrastrutture di trasporto (POP21=0): file sbagliato, non serve.
- Matrice pendolarismo 2011 per sezione: non trovata sulla pagina ISTAT; chiedere a micro.zone@istat.it o cercare nei dati del Censimento 2011.

## Livello Domanda (4/10/2026) - fatto in forma parziale
- `scripts/05_prepara_sezioni.py` legge `R01_21.zip` (nella cartella GTT) e crea `data/processed/sezioni_torino.json`: 14.127 sezioni entro 18 km da Torino (6.916 a Torino, 848.748 abitanti; 8.317 abitate in tutta l'area, 1,56 milioni di abitanti).
- Mappa: livello "Sezioni di censimento" con 3 colorazioni: poca offerta per abitante (passaggi/ora entro 400 m ogni 1000 abitanti entro 400 m), passaggi/ora entro 400 m, abitanti per km2. Grigio = nessun passaggio GTT programmato.
- Limiti: residenti = popolazione "di notte", non chi si sposta a quell'ora; fuori Torino mancano altri operatori e treni (il rosso puo' essere mancanza di dati); offerta = orari programmati.
- Ordine di lancio: 05 (una volta) -> 01 -> 04. Prossimo: pendolari/lavoratori/studenti (matrici ISTAT 2021 comune-comune gia' scaricate, 2011 per sezione da cercare), indicatore ritardi/traffico lento da dati raccolti.

## Mappa interattiva - aggiornamento 4/10/2026 (sera)
- Corse simulate: ogni corsa degli orari GTT (13.683 feriali, 10.747 sabato, 6.981 domenica) si muove a velocita' costante lungo il tracciato tra prima e ultima fermata. Stima dagli orari, NON posizione reale. Play/pausa, velocita' 1x-240x, orologio al minuto.
- Sfondi: chiara (CARTO), stradale (OSM), satellite (Esri); ripiego automatico su OSM se CARTO non carica. Filtro per linea. Pannello zoom: +, -, Torino, cintura, tasti + e -.
- NON fatto: puntini di persone (manca la matrice origine-destinazione per ora); richiesta con account Google Maps (vedi sotto).
- Google Maps: non usato. Servirebbe accedere con l'account personale e Google non offre l'export del traffico; la strada corretta, se vuoi, e' una chiave API di Google Maps Platform creata da te (a pagamento oltre la soglia gratuita).

## Raccolta in background (4/10/2026) - scelte dell'utente
- Avvio automatico all'accesso a Windows, senza finestra (file in "Esecuzione automatica"); impedisce lo stop del PC (schermo puo' spegnersi).
- Log in `logs/raccolta_AAAA-MM.log`, un file al mese, conservati senza limite. Riavvio automatico del raccoglitore dopo 30 s se si ferma.
- Promemoria: domenica dopo le 20:00, finestra "continuiamo?" con riepilogo; nessuna risposta in 1 ora = continua; "No" = si ferma (file `data/STOP_RACCOLTA.txt`).
- Avviso (finestra, una volta) se l'archivio supera 10 GB; dati senza altro limite di tempo.
- File: `scripts/supervisore.py`, `scripts/installa_sfondo.py`; doppio clic su `installa_raccolta.bat` (installa/avvia), `stato_raccolta.bat`, `ferma_raccolta.bat`, `riavvia_raccolta.bat`.
- Testato su Linux (riavvio, log, risposta No, file STOP); NON testato su Windows: finestra, anti-stop e avvio automatico da provare (`python supervisore.py --promemoria-ora`).

<!-- STATO DELL'UFFICIO: inizio. Questa parte la riscrive l'Ufficio dopo ogni task: non scrivere qui, scrivi sopra. -->
## Stato dell'Ufficio (aggiornato 05/10/2026 15:58)

### Piano
- [x] Base pronta (git, profilo, raccolta verificata) (fatto)
- [x] Mappa più chiara (sfondi, temi esclusivi, legenda misurato/stimato) (fatto) - GT01-sfondi, GT02-temi
- [ ] Velocità misurata dei mezzi (in corso) - GT04-velocita
- [ ] Domanda: pendolari ISTAT (in corso) - GT05-pendolari, GT19-elaborazione-matrici-pen
- [x] Punti critici v0 (fatto) - GT18-punti-critici-integrati
- [ ] Traffico tipico e simulazione tarata (dopo 1-2 settimane di dati) (da fare)
- [ ] Raspberry Pi / condivisione (da fare)

### Fatto di recente
- 2026-10-05 15:58 · GT19-elaborazione-matrici-pen: Creato script di elaborazione matricI pendolarismo ISTAT per Torino e cintura, con relativo rapporto e sintesi documentazione. File prodotto pronto in data/processed/.
- 2026-10-05 15:25 · GT18-punti-critici-integrati: Ho aggiunto un indice di criticità 0–100 per sezione di censimento, con contorno rosso (80 o più) nei 4 temi e il valore nella scheda al clic. · 2 domande per te
- 2026-10-05 15:00 · GT17-scheda-unica: Implementata la struttura unica standard a 4 sezioni per tutte le 7 schede informative al clic (fermate, linee, sensori 5T, sezioni di censimento, comuni, mezzi reali e zone statistiche) con funzione generatrice unica in scripts/mappa_template.html.
- 2026-10-05 14:54 · GT16-temi: Menu della mappa ridotto a 4 temi funzionali, aggiunta la sottoscelta per Servizio e abitanti e raggruppato il blocco temporale «Quando» in scripts/mappa_template.html.
- 2026-10-05 14:30 · GT15-piano-ui-scenari: Redatto docs/PIANO_UI_E_SCENARI.md con analisi completa di 9 temi e 16 controlli attuali, proposta a 4 temi unificati, struttura uniforme per le schede e architettura per scenari alternativi su base ISTAT.
- 2026-10-05 13:58 · GT14-verifica-passaggi: (il modello non ha scritto un riassunto)
- 2026-10-05 12:47 · GT12-prossimi-passaggi: Inserito 1 tag script e aggiornato 1 funzione di visualizzazione fermata (2 modifiche totali) per mostrare i prossimi passaggi alle fermate.
- 2026-10-05 03:31 · GT13-altre-citta: Creato docs/ALTRE_CITTA.md con studio completo (5 sezioni richieste) e rapportino in agenti/GT13-altre-citta/
- 2026-10-05 03:29 · GT12-prossimi-passaggi: non ha passato i controlli
- 2026-10-05 03:22 · GT05-risposta2: Creati 2 file (DOMANDE.md e RAPPORTO.md) con 1 domanda registrata e nessuna modifica al codice. · 1 domande per te
- 2026-10-05 03:16 · GT05-risposta1: Looking at this task, I need to understand what changed: Leo answered "sì, la scarico" to the question about downloading the ISTAT codici comuni table (PRO_COM → comune name).
- 2026-10-05 03:06 · GT04-risposta1: La risposta «A tenere» è applicata senza modifiche al codice: le soglie colori velocità restano 12/16/20 km/h (velClasse e legenda già coerenti).

### Decisioni di Leo (risposte alle domande)
- Vuoi i nomi dei comuni (tabella ISTAT codici)? -> **sì, la scarico**
- Colore di partenza del tema Pendolari? -> **per 1000 abitanti**
- Quanti comuni con linea nel tema Pendolari? -> **non capisco la domanda**
- «Segnalazioni adesso» anche nel tema Traffico? -> **sì**
- Nel tema Tempo reale accendere anche le linee sottili? -> **no**
- Tema Poca offerta: linee sottili a metà spessore va bene? -> **metà**
- Soglie colori velocità (12/16/20 km/h) vanno bene? -> **A tenere**
- Minimo campioni per colorare una linea? -> **20**
- Quanti comuni con linea nel tema Pendolari? -> **30**
- Nel tema Pendolarismo la criticità deve contare anche i pendolari? -> **A**
- Il contorno rosso va bene anche di notte, quando quasi tutto è critico? -> **A**

### Domande aperte: 0 (0 a risposta chiusa)
<!-- STATO DELL'UFFICIO: fine -->
