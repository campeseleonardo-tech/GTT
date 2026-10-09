# Memoria del progetto GTT

Ultimo aggiornamento: 9 ottobre 2026.
Unico file di memoria e di passaggio (niente README o altri documenti di memoria).
Leggerlo all'inizio di ogni sessione e aggiornarlo alla fine.

## Obiettivo

Progetto di portfolio, fattibile e metodologicamente valido (riorientato con Leo il 9/10/2026,
sezione 9). Area: Torino più cintura (entro 18 km).

- Domanda di fondo: capire come funziona la città (chi va dove, perché e con che mezzo; dove
  mancano servizi; dove sono le criticità) e misurare l'effetto di scenari limitati (es.
  cambiare linee e orari del trasporto pubblico) su quantità misurabili.
- Problemi di partenza osservati da Leo: pochi parcheggi di interscambio a Fermi, metro chiusa
  di notte, molto traffico di auto nelle ore di punta.
- Ordine di lavoro: 1) capire; 2) scenari "cosa succede se" sull'accessibilità; 3) altri temi
  (interscambio, congestione, verde e calore, vulnerabilità). Il gioco tipo SimCity è escluso
  dallo sviluppo.
- Strumento: mappa web interattiva in HTML (stile Google Maps) con domanda e offerta di mezzi,
  punti critici e flussi in tempo reale (simulati dove non misurati). Studio e portfolio,
  forse da condividere.

Principi per gli scenari:

- Separare "cosa succede" (tempi di viaggio, residenti serviti, servizi raggiungibili,
  copertura per ora: misurabile) da "se è meglio" (pesi di valore, sempre visibili e
  regolabili dall'utente).
- Ancore oggettive per "mancano / ce ne sono troppi": standard urbanistici minimi per abitante
  (DM 1444/1968) e "città dei 15 minuti" (servizi essenziali raggiungibili a piedi).
- Uscita: esito sintetico a colpo d'occhio + mappa prima/dopo col dettaglio locale.
- L'effetto sul traffico di auto non è prevedibile in modo affidabile: solo ordini di
  grandezza, con le ipotesi dichiarate.

## Struttura delle cartelle

- `mappa_torino.html` (doppio clic; generata da `scripts/04_genera_mappa.py`), `simulazione.html`,
  `MEMORIA_PROGETTO.md`, `AGENTS.md`.
- `scripts/`: script Python e file .bat/.sh della raccolta. Nessuna cartella dati qui.
- `data/` (non su git):
  - `raw/`: grezzi scaricati, non si modificano; `raw/istat/` ISTAT per tema (inventario sotto).
  - `processed/`: prodotti dagli script; `processed/catalogo/` indice e gruppi del catalogo.
  - `catalogo/`: file `.js` per gruppo (da 04), caricati dalla mappa su richiesta.
  - `storico.sqlite`: archivio della raccolta (quello principale è sul Pi, sezione 1). Non
    spostare mentre la raccolta gira.
  - `live.js`, `stat.js`, `replay_*.js`, `agg_cache.json`: file per la mappa, aggiornati dalla raccolta.
- `docs/`: solo testi (fonti, diagnosi, richieste, piani, rapporti). `logs/`: log (non su git).

## Decisioni prese

- Pagina HTML locale senza server; dati locali (SQLite), nessun cloud.
- Raccolta continua sul Raspberry Pi "leopi" (sezione 1). È il patrimonio unico del progetto:
  lo storico GTT/5T non esiste altrove, il resto si riscarica.
- Direzione (9/10): portfolio su "capire" + scenari limitati sull'accessibilità; gioco e
  gamification esclusi.
- Calcolo dei percorsi con strumenti aperti esistenti (OpenTripPlanner o R5/r5py, su GTFS +
  OpenStreetMap), non riscritto da zero.
- Fonte principale per "chi va dove e perché": IMQ 2022 (per la domanda attuale supera la
  matrice 2011 sezione→sezione).
- Catalogo congelato: nessun nuovo dataset senza una domanda che lo richieda. Mappa e
  simulazioni leggono gli stessi file elaborati; la mappa carica un gruppo solo su richiesta;
  la sintesi unica tra dimensioni (accessibilità, vulnerabilità, attrattori, affidabilità) è
  opzionale e successiva.
- Criticità sociali: indice di vulnerabilità (istruzione, occupazione, affollamento delle
  abitazioni, servizi, verde), MAI la nazionalità come criticità in sé.
- Niente costruzione sulla mappa prima di aver ispezionato i dati. Script provati su copie;
  trovano da soli la cartella GTT (dati in `data\raw`, rapporti in `docs`).
- Python: interprete di sistema 3.14.3 sul PC, 3.13.5 sul Pi.
- Si tiene solo ciò che serve: doppioni e file inutili si tolgono.
- Sezioni 2011 e 2021: accettato un accorpamento approssimato.
- Richieste dati esterne (MTM, telefonia): rimandate (bozze in `docs/`).
- Privacy: niente dati personali; nei prodotti non entrano telefono, email, PEC, URL né nomi di
  persona (es. `NOME_ADD` delle attività, `PHONE` di IMQ). Niente invii a nome di Leo.

### Regole per i nuovi dati nella mappa (R1–R3, decise da Leo)

- R1. Solo dati facili. Niente circoscrizioni e niente tabelle nel pannello: le informazioni
  extra stanno nel tooltip e nella scheda al clic.
- R2. Anni diversi: se il dato vecchio si riassume nel recente, si mostra solo il recente; il
  vecchio solo se contiene informazione che il recente non ha.
- R3. Merge tra anni: un codice non agganciato non blocca il merge; si registrano nel log
  quante righe e quali codici. Il merge si ferma solo oltre il 2% non agganciato
  (`TOLL_MERGE = 0.02` in 04).

---

# ATTIVITÀ FATTE

## 1. Raccolta continua (attiva)

- `scripts/03_raccolta_continua.py` (solo libreria standard): 5T ogni 300 s, mezzi GTT ogni
  60 s; tabelle `sensori_5t`, `flussi_5t`, `accuratezza_5t`, `mezzi_gtt`, `errori`.
- `accuratezza_5t(generato_utc,lcd1,accuratezza)` dall'8/10 21:30: stessa transazione dei
  flussi, INSERT OR IGNORE (passato non riscritto, niente valori retroattivi), 0 distinto da
  NULL. Verificata sul DB vero: 109 righe per snapshot, coincidenti coi flussi.
- `scripts/supervisore.py`: lancia 03, ogni minuto `06_dati_live.py`, ogni 15 minuti
  statistiche e replay; riavvio dopo 30 s; log mensili e dati senza limite di tempo. Su
  Windows anche: avvio nascosto all'accesso, anti-stop del PC, finestra domenicale dopo le
  20:00 ("continuiamo?"; nessuna risposta in 1 h = continua; No = ferma con
  `data/STOP_RACCOLTA.txt`), avviso oltre 10 GB. Comandi PC: `installa_raccolta.bat`,
  `stato_raccolta.bat`, `ferma_raccolta.bat`, `riavvia_raccolta.bat` (`raccolta_continua.bat`
  solo manuale).
- **Raspberry Pi "leopi"** (192.168.8.200, utente `leopi`), attivo dal 9/10 ~01:25:
  - unit systemd `gtt-raccolta` → `/home/leopi/GTT/scripts/supervisore.py` (03 + 06); fuso
    Europe/Rome; log in `/home/leopi/GTT/logs/`; installato con `installa_leopi.sh`.
  - Accesso SSH con la chiave `%USERPROFILE%\.ssh\id_gtt_leopi` (senza password; WinSCP per i
    file); sudo senza password.
  - Storico copiato via backup API (191 MB, 124.805 flussi, verifica identica) in
    `/home/leopi/GTT/data/storico.sqlite`; copia di passaggio sul PC:
    `data/storico_copia_leopi.sqlite`.
  - Verificato: il DB cresce e genera `live.js`, `stat.js`, `agg_cache.json`, `replay_*.js`.
  - Sync verso il PC: `scripts/sync_da_leopi.bat`, attività di Windows "GTT sync da leopi"
    ogni 5 minuti.
  - Comandi: `systemctl status gtt-raccolta`, `journalctl -u gtt-raccolta -f`,
    `sudo systemctl stop|start|restart gtt-raccolta`.
- **Periodo parallelo**: anche il PC raccoglie e riscrive `live.js` ogni minuto, mentre la
  sync riporta quelli del Pi ogni 5': la mappa alterna le due fonti. Finisce quando Leo ferma
  la raccolta del PC (attività 1).

## 2. Mappa (funzionante, verificata a video da Leo)

- `mappa_torino.html` da `04_genera_mappa.py` + `mappa_template.html`: un solo file, motore di
  mappa scritto a mano, sfondo da internet.
- Livelli: sezioni di censimento (offerta, densità, profilo dei residenti), zone statistiche,
  linee, fermate, traffico 5T, mezzi GTT reali, corse simulate, pendolari, segnalazioni, OMI,
  mobilità IMQ 2022, catalogo.
- Corse simulate: ogni corsa degli orari (feriali 13.683, sabato 10.747, domenica 6.981) a
  velocità costante sul tracciato. STIMA dagli orari, NON posizione reale.
- Sfondi: chiara (OSM schiarito), stradale (OSM), satellite (Esri). Niente CARTO (chiave) né
  Google Maps (chiave a pagamento).
- Comandi: giorno tipo, slider al minuto, play/pausa, velocità 1×–240×, zoom, filtro per
  linea, colore linee per corse/ora o mezzi reali rispetto al previsto.
- Scenari: `07_elabora_scenario.py`, `calcola_simulazione.py` (in `data/scenari/`), aperti in
  `simulazione.html`.

## 3. Sezioni di censimento e indicatori ISTAT 2021 (fatto)

- Piano A0–A7 completato: ispezione delle 119 colonne di R01 col tracciato;
  `05_prepara_sezioni.py` aggiunge famiglie e abitazioni; 04 le passa alla mappa (commit
  `c677cbf`); integrati P101 (occupati 15–64), P15+P16 (5–14), P27+P28+P29 (65+) in
  `sezioni_torino.json` e nella mappa.
- Verifiche: aggancio 8.317/8.317 sezioni abitate, nessun negativo, nessuna sezione con
  famiglie > abitanti, fasce coerenti, test Node della conversione JS.
- Rinviati: tooltip sezione e tooltip pendolari (A3/A4).

## 4. OMI: valore immobiliare (fatto)

- Quotazioni OMI 2025/2, €/m² per zona e tipologia (valori ordinari, non la stima del singolo
  immobile). `08_prepara_omi.py` → `data/processed/omi_zone.json`; tema "Valore immobiliare
  (OMI)" con tendina tipologia, legenda, tooltip e scheda.
- Controllo: zona Torino B1 "ROMA", tipologia ab 2900–4400 €/m² (locazione 10,5–15,7).
  Commit `483830b`, `d009b81`, `af3a776`, `36c61bf`, `17003bf`.

## 5. Catalogo dei dati comunali (fatto)

- `11_prepara_catalogo.py` (sola lettura) → `catalogo.json` (indice con metadati e
  statistiche) + un file per gruppo; 04 scrive `data/catalogo/<gruppo>.js`, caricato su
  richiesta con `ricarica()`.
- Geometrie `WKT_GEOM` da EPSG:3003 a WGS84 con `gb_a_wgs84` (verificato su Piazza Castello e
  sulla scuola "VALLETTE A").
- Tema in mappa: tendina del gruppo, caselle per dato, legenda, tooltip/scheda e pulsante "i"
  con la scheda del dato (fonte, anno, licenza, copertura, record, anomalie). Gruppi
  voluminosi solo da zoom 14.
- Anomalie: `mercati_tematici` con COORD_X/Y ~10× più piccole (si usa il WKT); 1 car sharing
  fuori area; `strutture_socio_assistenziali` con 38 `IDCIVICO` ripetuti (non è un id);
  poligoni multipli (mercati 42→57, zona blu 19→23); alberate 131.994 alberi → 1.928
  aggregati per ambito.
- Verificato in Node e a video da Leo (8/10).

## 6. Analisi dei dati diurni 5T e GTT (8/10)

- `09_analisi_dati_diurni.py`: sola lettura del DB, ora locale Europe/Rome verificata al
  cambio d'ora, denominatori espliciti → `docs/RAPPORTO_ANALISI_5T.txt` (e `.md`),
  `data/processed/analisi_5t.json`. Ha sostituito 10 (eliminato: errore di sintassi e
  risultati fuorvianti). Accetta `--db`.
- Dati 4–8/10: 122.189 misure 5T in 1.121 snapshot, tutti completi; flusso=0 il 19,7%, NULL
  0%. GTT: 1.580.712 righe in 5.163 snapshot, 0 duplicati, 31 buchi >90 s; punte feriale alle
  08:00 (555,5 mezzi) e domenica alle 18:00 (255,7).
- Limiti: 5 giorni senza sabato; buco di ~16,7 h il 6–7/10 (PC spento); notte poco coperta;
  mezzi = mezzi localizzati dal feed, non flotta; sensori periferici sempre a 0; accuratezza
  dei flussi storici "non disponibile", mai attribuita a posteriori.

## 7. Ritardi GTT (9/10)

- Il feed `trip_update` NON pubblica ritardi (niente `delay` né `stop_time_update`; solo
  `trip_id`, `start_date`, `start_time`, `schedule_relationship`). Il file salvato il 3/10 era
  vuoto (15 byte). Scelta della notte del 9/10: per ora solo corse attive/soppresse + avvisi
  (rivista dall'attività 9).
- `12_ritardi_gtt.py` (libreria standard; non tocca lo storico né i grezzi; accetta `--db`):
  `raccogli` → `data/processed/ritardi_<giorno>.csv` (con `con_delay`, `con_stu`) +
  `avvisi_<giorno>.json`; `analizza` → corse per linea/ora, soppresse, match trip_id↔GTFS,
  sintesi avvisi, decodifica dei `.pb` alerts.
- Prova notturna: 1 corsa (67U, soppressa, match 1/1); 154 avvisi (cause top
  PROBLEMA_TECNICO 77, LAVORI 36; effetto top DEVIAZIONE 110; 3 con severità 4 fuori
  specifica, da chiarire; 17 linee e 1.093 fermate toccate).
- Raccolta una tantum in corso sul PC dal 9/10 ~00:35 (~20 h): `ritardi_20261009.csv`. La
  raccolta continua non salva questo feed.

## 8. Riordino e pulizia (8/10)

- Tolti da git `README.md` e `PASSAGGIO_CONSEGNE.md` (assorbiti qui); `mappa_torino.html` ora
  committata.
- Cancellati doppioni e file sbagliati (copie di R01_21, `BT21-sez-M04` con POP21=0, file di
  sistema), `07_elabora_matrici_pendolarismo.py` (rotto) con i suoi output vuoti, i
  `tmp_check_*.py`. Dati ISTAT spostati da `docs/` a `data/raw/istat/`.
- Ancora da cancellare con la vecchia `docs/istat/`: `NOTE_FILE_ISTAT.md`, `LEGGIMI.txt`,
  `RISULTATI_ELABORAZIONE.md`.

## 9. Riorientamento del progetto (9/10)

- Idee di partenza di Leo: simulatore stile SimCity con parametri di valore per ogni servizio
  e scenari di intervento (metro, parco, caserma...); chi va dove e perché; edifici che
  portano valore; criticità anche sociali; gioco partecipativo; verde e temperature.
- Esiti:
  - Simulatore universale con punteggio unico: NO (regole inventate, manca il modello di
    domanda, pesi soggettivi). SÌ in forma ridotta: scenari sull'accessibilità con pesi
    regolabili.
  - SÌ: Fermi e metro di notte come casi pilota; chi va dove (IMQ); verde e calore;
    indicatori di criticità; vulnerabilità al posto della nazionalità; OMI × accessibilità
    (grossolano).
  - Traffico di auto: sì per la diagnosi, no per la previsione.
  - Gioco escluso (avrebbe senso solo con budget e costi realistici, e raccoglierebbe
    preferenze, non soluzioni validate).
- Direzioni nuove: Torino per ora del giorno; confine città/cintura; affidabilità reale
  contro orario.
- Congelati: espansione del catalogo, approfondimento dell'accuratezza 5T, matrice 2011 come
  domanda attuale, matrici 1991/2001, MEF.

## 10. IMQ 2022: chi va dove e perché (fatto, 9/10)

- `13_esporta_imq.ps1` (Access→CSV, nessun dato personale), `14_prepara_imq.py` (aggregazione
  pesata per zona/scopo/ora/modo + matrice OD + residenti), `15_prepara_zone_imq.py` (geometria
  delle 212 zone: 23 quartieri EPSG:3003 + 189 comuni da confini ISTAT 2022), `16_prepara_imq_mappa.py`
  (prepara i dati per la mappa).
- Verifiche contro il report: totale 8.217.862,7 vs 8.217.863 (−0,000%); quota pubblico 5,65%
  (esatta); scopi allineati; 0 comuni non agganciati su 1.181; area Torino 130,18 km².
- In mappa: tema "Mobilità (IMQ 2022)" sulle 101 zone della Città metropolitana (23+32+46):
  choropleth (spostamenti per ora×modo, quote, residenti), ora dallo slider, al clic scheda e
  linee dei flussi OD. Prodotti: `imq_zone.json`, `imq_od.json`, `imq_aggregati.json`,
  `imq_residenti.json`, `imq_zone_geo.json`, `imq_mappa.json`. Limite dei quartieri del 1984 in
  "Limiti e rischi". Dettagli in `docs/RAPPORTO_IMQ.txt`.

## 11. Pulizia della mappa (9/10)

- Tutto in `scripts/mappa_template.html` (unico file di codice; `mappa_torino.html` rigenerato con
  04). Un commit per fase:
  - Temi ridotti da 9 a 7: «Zone critiche» assorbita in «Servizio e abitanti» (voce «Criticità
    0–100»), «Nessuno» tolto.
  - Rimossi i contorni rossi sulle sezioni critiche (flag `critici`): la criticità resta solo
    come colore di riempimento.
  - Hover uniforme: tooltip compatto (nome + 1-2 valori chiave) su ogni elemento, clic = scheda
    completa. Prima sezioni, zone e comuni non mostravano nulla al passaggio del mouse.
  - Pannello: «Guida e stato dei dati» unisce limiti e stato; la Legenda è un riquadro flottante
    separato (in basso a destra, richiudibile); «Segnalazioni adesso» compressa in un blocco chiuso.
  - «Sfondo» separato dai filtri; «Sovrapposizioni» ora è una tendina chiusa con le caselle, filtro
    «singola linea» compreso. Tolta la scelta del colore linee: una sola impostazione (spessore =
    corse/ora).
  - Area «Opzioni» unica e dichiarativa: ogni tema dichiara le sue scelte nel record `THEMES`
    (campo `opzioni`), il codice (`renderOpzioni`) le costruisce con lo stesso stile; il catalogo
    è incluso. Aggiungere un'opzione = una voce in `OPZIONI` + il suo id nel tema.
  - Trasparenze e contorni uniformi sui livelli a colori (sezioni, zone, OMI, IMQ); testi della
    guida accorciati.
- Verifica: sintassi JS con `node --check`; esecuzione con uno shim DOM e i dati veri (avvio +
  cambio di tutti i 7 temi + opzioni, senza errori). Il controllo visivo finale resta da fare da Leo.
- Bug trovato e corretto in prova: `disegna()` leggeva opzioni che ora esistono solo nel tema
  attivo (lettore sicuro `valOp`).

# ATTIVITÀ DA FARE (in ordine di priorità)

## Priorità alta

1. **Chiudere il passaggio al Pi**: fermare la raccolta del PC dopo il parallelo (~3 giorni
   feriali, decide Leo); impostare una copia periodica dello storico dal Pi al PC con la
   backup API (il Pi resta l'unica copia; serve anche alle analisi). Poi chiedere a Leo se
   cancellare `data/storico_copia_leopi.sqlite`.
2. **Chiudere i ritardi una tantum**: a raccolta finita (~20:30 del 9/10) lanciare
   `python scripts\12_ritardi_gtt.py analizza`, confermare sul campione diurno l'assenza di
   `delay`/`stop_time_update`, consolidare `docs/RAPPORTO_RITARDI_GTT.txt`.
3. **IMQ 2022 - residuo**: resta solo da decidere se chiedere all'Agenzia Mobilità Piemontese
   il perimetro delle zone di campionamento (i quartieri del 1984 non coincidono con la
   zonizzazione IMQ per 7 su 23). Bozza in `docs/richiesta_MTM_IMQ.md`.
4. **Accessibilità per sezione e per ora del giorno**: tempi di viaggio col trasporto
   pubblico (GTFS + OSM, con OpenTripPlanner o R5/r5py), es. alle 8, 14, 23 e 2. Da qui
   l'indicatore "città dei 15 minuti" per sezione col catalogo.
5. **Primo scenario: metro aperta di notte**: tempi notturni di oggi (bus notturni) contro
   metro aperta. Uscita: un numero sintetico (es. minuti risparmiati × residenti) + mappa
   prima/dopo. Poi una bozza di linea 2. Costi e manutenzione notturna restano fuori dal
   modello (dichiararlo).

## Priorità media

6. **Interscambio Fermi**: flussi dalla cintura (pendolari 2021, IMQ) contro posti
   disponibili; l'occupazione reale va contata a mano qualche mattina.
7. **Verde e calore**: temperatura superficiale (Landsat) × alberate × residenti 65+. Aree
   verdi dallo shapefile `http://geoportale.comune.torino.it/geodati/zip/carta_sintesi_geo.zip`
   (EPSG:3003, CC BY 4.0; isolare "aree verdi"; in alternativa WFS/WMS del GeoPortale
   Piemonte, record "Dati di base – Carta di sintesi – Aree"). Il DWG non serve.
8. **Indice di vulnerabilità per sezione**: indicatori R01 (es. istruzione, occupazione,
   abitanti per abitazione) + servizi e verde.
9. **Affidabilità reale contro orario**: passaggi alle fermate ricostruiti dalle posizioni
   proiettate sui tracciati GTFS; regolarità degli intervalli anche senza `trip_id`. Prova su
   2–3 linee e verifica sul campo (~20 passaggi annotati). Corregge anche l'ottimismo degli
   scenari basati sugli orari.
10. **Città/cintura**: cercare di nuovo i GTFS dei treni SFM e dei bus extraurbani; capire
    come aggiungere i cataloghi dei comuni della cintura.
11. **Congestione con 5T**: dove e quando la città si blocca; associazione accuratezza ↔
    flusso ↔ ora con 7–14 giorni di nuovi campioni, feriali e weekend (finestra 15–22/10).
12. **Valore e accessibilità**: vicinanza a metro, parchi e servizi nei valori OMI (251 zone,
    analisi grossolana).

## Priorità bassa / congelate

13. **Matrice tempi e distanze 2021**: `https://www.istat.it/storage/cartografia/matrici_distanze/Piemonte.zip`
    (km e minuti tra i comuni della provincia e i 7.903 comuni italiani, geografia al
    1/1/2021; nota tecnica in `docs/`; facoltativo `MatriciContiguita_Comuni_2019_2025.zip`).
    Solo se uno scenario tra comuni la richiede.
14. **MEF 2024**: normalizzare il codice comunale e confrontare copia locale (312 comuni) e ZIP
    nazionale (7.897). Solo confronti tra comuni, non quartieri.
15. **Anagrafe scuole 2026/27**: collegarla alle 610 sedi e chiarire il conteggio (410 statali
    + 195 paritarie col filtro provincia+comune, contro 431+196 del piano).
16. **Matrice 2011 sezione→sezione**: superata da IMQ; solo riferimento storico o prova della
    meccanica di simulazione. Script da riscrivere solo se Leo decide di usarla.
17. **Attività commerciali**: aggregato per categoria/area solo se serve (oggi conteggi in
    scheda e punti da zoom 14).

## Più avanti

18. **Richieste dati esterne**: validazione biglietti GTT e telefonia
    (`docs/richiesta_dati_telefonia.md`).
19. **Mappa statica offerta-domanda** come sintesi.

---

# DATI PRESENTI E VERIFICATI

## In mappa

- **GTFS GTT**: valido 1/10/2026–31/1/2027 (versione 20261002). 215 linee, 7.045 fermate,
  966.946 passaggi programmati.
- **Mezzi GTT in tempo reale**: ~306 mezzi localizzati per lettura (mediana 337, punta ~555,
  notte ~1–5); `trip_id` pieno nel ~31% delle righe: il mezzo si lega alla linea, alla corsa
  solo in parte.
- **Traffico 5T**: 109 sensori, area più ampia di Torino, snapshot completi. Accuratezza per
  misura solo dall'8/10 21:30; significato di accuratezza 0 non verificato.
- **Zone statistiche Torino**: 94 zone (2011, senza popolazione).
- **Pendolarismo ISTAT 2021** (comune↔comune): Torino lavoro entrano 138.605, escono 71.297,
  dentro 212.249; studio entrano 48.730, escono 6.373, dentro 120.148.
- **Sezioni 2021**: Torino 6.916 sezioni, 848.748 abitanti, 433.469 famiglie, 502.615
  abitazioni occupate, 36.242 edifici; area entro 18 km 8.317 sezioni abitate, 1.557.493
  abitanti.
- **Indicatori R01 2021** (aggancio 100%): Torino 346.734 occupati su 528.512 residenti 15–64
  (65,6%), 69.900 residenti 5–14, 220.883 residenti 65+.
- **OMI 2025/2**: provincia 312 comuni, 953 zone, 3.119 righe, 14 tipologie; in mappa 68 comuni
  e 251 zone (Torino 47).
- **Mobilità IMQ 2022** (in mappa): 101 zone CMTO; residenti 1.942.688; spostamenti in partenza
  4.263.592/giorno (pesati); ripartizione modale, scopi, ora di punta e flussi origine→
  destinazione. Fonte: Agenzia della Mobilità Piemontese / MTM.
- **Catalogo comunale** (44 dati, ~37.819 punti): istruzione (610 scuole, 29 università,
  servizi infanzia), salute (44 accessi ospedalieri, 37 consultori, 243 farmacie [dato
  ~2011], 151 strutture socio-assistenziali), commercio (31.271 attività, 42 mercati, 16
  mercati tematici, 21 luoghi, 51 musei, 20 biblioteche, 26 cinema), sicurezza/sport (77
  record di pubblica sicurezza, 686 impianti), reti (143 aree pedonali, 4.151 tratti
  ciclabili, 58 percorsi accessibili, 23 fermate metro, 87 bike sharing, 83 car sharing, 95
  ricarica, 39 parcheggi in struttura, 1.817 stalli disabili, 19 zone blu, 3 ZTL, 1.928
  aggregati di alberate), servizi (164 sedi amministrative, 78 uffici postali, 15 anagrafici,
  3 turistici).
- **Raccolta propria** (`storico.sqlite`): il dato più prezioso, cresce ogni giorno.

## In archivio (pronti, non in mappa)

- **Pendolarismo 2011 per sezione** (110 zip per provincia di origine; Torino 5,7 MB → CSV
  120 MB): unico origine-destinazione sub-comunale, senza mezzo né orario. Torino→Torino
  355.525. NON cancellare gli zip delle altre province (contengono chi entra a Torino, es.
  Asti 9.112, Milano 976).
- **Matrice nazionale 2011** (`matrix_pendo2011_10112014.txt`, 293 MB): TENERLA. Mezzo (12
  categorie), orario di uscita (4 fasce), tempo di viaggio (4 classi), livello comunale.
- **Basi territoriali 2021 Piemonte** (`R01_21.zip`): confini e popolazione per sezione (usate da 05).

## Grezzi (`data/raw/`)

- `istat/pendolarismo_2021/`: matrici lavoro (12,6 MB) e studio (3,4 MB, stima con modelli)
  con i `.doc` delle colonne (usate da 04).
- `istat/2011_sezioni/`: `per_provincia/` (110 zip), `nazionale/` (matrice + documenti).
- `istat/basi_territoriali_2021/`: `R01_21.zip` (74 MB).
- `istat/confini_2022/`: `Limiti01012022_g.zip` (confini ISTAT generalizzati al 1/1/2022; il
  file comuni è UTM 32N su WGS84; usato da 15 per le zone IMQ).
- `istat/altro/`: `Dati_regionali_2021/` (R01–R20 + tracciato; in uso solo R01),
  `MatriciContiguita_Province_2019_2025/`.
- `istat/storiche/`: matrici 1991 (92 MB) e 2001 (166 MB).
- `istat/documentazione/`: note tecniche (pendolarismo 2011, contiguità 2025, distanze 2023).
- Altro: `gtt_gtfs_*.zip`, feed tempo reale (`*_vehicle_position_*`, `*_trip_update_*`,
  `*_alerts_*.pb`), `5t_flussi_*.xml`, `zone_statistiche_*`, OMI
  (`QIP1445919_CMPLRD98T08F335C/`), CSV del Comune, MEF (`Redditi_..._IRPEF_..._2024.zip` +
  cartella locale), `IMQ2022_opendata_web/` (Access + metodologia),
  `ex_quartieri/` + `ex_quartieri.zip` (23 quartieri di Torino, shapefile EPSG:3003),
  `carta_sintesi_aree_dwg.zip` (inutile), `StrutturaDati_PercorsiCiclabili.pdf`,
  `IMQ-2022_EP_REPORT-COMPLETO-2.1.pdf`.

## Presenti ma non usati

- **MEF 2024**: 7.897 record comunali nel ZIP; la copia locale (312 comuni) usa un codice
  comunale diverso (attività 14).
- **Matrici 1991/2001, R02–R20, contiguità provinciali**: non servono (vedi "Da decidere").

---

# DATI MANCANTI

1. **Domanda per ora e fermata** (chi sale e quando): non pubblica. È il dato che più
   cambierebbe la mappa. Strade: validazione biglietti GTT o telefonia aggregata (attività 18).
2. **Pendolari 2021 per sezione**: non pubblici. Mezzo e orario esistono solo per comune e
   solo nel 2011.
3. **Ritardi GTT**: il feed non li pubblica; stimabili dalle posizioni (attività 9).
4. **Cintura**: orari di treni SFM e bus extraurbani non trovati; cataloghi dei comuni assenti
   (attività 10).
5. **Numeri sugli attrattori**: capienze, iscritti, visitatori ed eventi di scuole, ospedali,
   impianti, musei. Restano attrattori potenziali, non viaggi.
6. **Disponibilità in tempo reale** di sharing, ricarica e parcheggi (es. occupazione di
   Fermi, attività 6).
7. **Addetti per sezione** (dove si lavora).
8. **Da scaricare per le attività**: estratto OSM (4), temperatura superficiale Landsat (7),
   matrice delle distanze (13).

---

# LIMITI E RISCHI

- **Misurato o stimato**: le corse sono stimate dagli orari; il traffico è misurato solo in
  109 punti; la domanda sono residenti (popolazione "di notte") e pendolari, non persone in
  movimento (il tooltip dice "residenti"). Distinguere sempre "misurato" da "stimato".
- **Bias città/cintura**: cataloghi solo per Torino e niente altri operatori in cintura. La
  cintura sembra più povera o più "rossa" anche solo perché mancano i dati.
- **Qualità della raccolta** (sezione 6): campione breve, buchi notturni, accuratezza passata
  non disponibile. Vale per ogni uso futuro dei numeri.
- **Scenari**: l'esito "meglio/peggio" dipende dai pesi, da mostrare sempre; l'effetto sulle
  auto è solo un ordine di grandezza; uno scenario basato sugli orari è ottimista.
- **Criticità sociali**: la nazionalità mostrata come criticità rischia di stigmatizzare
  quartieri (es. Aurora, Barriera, Porta Palazzo). Usare indicatori di vulnerabilità.
- **Dati di anni diversi**: sezioni 2011 e 2021 senza codice comune (accorpamento
  approssimato). OMI sono valori ordinari per zona, non stime di singoli immobili.
- **Zone IMQ**: le 189 zone C/E/R (comuni) sono esatte; i 23 quartieri di Torino sono i confini
  del 1984 e non coincidono con la zonizzazione IMQ per 7 su 23 (sezione 10).
- **Copia unica**: finché non c'è la copia periodica (attività 1), lo storico vive solo sul Pi.
- Le funzioni Windows del supervisore (finestra settimanale, anti-stop, avvio automatico) non
  sono state provate su Windows; diventano irrilevanti quando resta solo il Pi.

---

# DA DECIDERE CON LEO

- Spazio dati: togliere `storiche/` (~270 MB) e R02–R20 (~190 MB)? La matrice nazionale 2011
  e gli zip provinciali restano.
- Primo caso pilota: metro di notte (proposta, usa solo dati già presenti) o Fermi?
- Strumento per i percorsi: OpenTripPlanner o R5/r5py?