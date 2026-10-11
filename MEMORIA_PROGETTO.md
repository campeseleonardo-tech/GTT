# Memoria del progetto GTT

Ultimo aggiornamento: 11 ottobre 2026 (revisione completa con Leo: stato, pulizia, correzioni).
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
  - `storico_backup.sqlite`: copia settimanale dello storico del Pi (sezione 1); l'originale
    vive solo sul Pi.
  - `live.js`, `stat.js`, `replay_*.js`, `agg_cache.json`: file per la mappa, aggiornati dalla raccolta.
- `docs/`: solo testi (fonti, richieste, piani, rapporti). `logs/`: log (non su git).
- `data/otp/` (nome storico, ora serve a R5): `jdk-25.0.4.1+1-jre` (Java per r5py) e
  `rete/torino_cintura.osm.pbf` (taglio OSM di 17, 20,6 MB). Gli strumenti OTP sono stati tolti
  (11/10, `PULIZIA_GTT.bat`).
- Sul PC lo storico si legge da `data/storico_backup.sqlite` (copia settimanale dal Pi).
  `04_genera_mappa.py` (strato Velocità) e `09_analisi_dati_diurni.py` usano il backup e solo se
  manca il vecchio `data/storico.sqlite` (tolto l'11/10). Il Pi scrive sempre nel suo
  `storico.sqlite`: 03, 06, supervisore e `12 raccogli-db` NON vanno cambiati.

## Decisioni prese

- Pagina HTML locale senza server; dati locali (SQLite), nessun cloud.
- Raccolta continua sul Raspberry Pi "leopi" (sezione 1). È il patrimonio unico del progetto:
  lo storico GTT/5T non esiste altrove, il resto si riscarica.
- Direzione (9/10): portfolio su "capire" + scenari limitati sull'accessibilità; gioco e
  gamification esclusi.
- Calcolo dei percorsi con strumenti aperti esistenti, non riscritto da zero.
  Scelta finale (10/10): **R5 via r5py** (Conveyal R5, jar scaricato da r5py in
  `AppData\Local\r5py`). Prima prova con OpenTripPlanner 2.10: verificato sul server
  reale che OTP 2.10 non ha piu' le isocrone (GraphQL senza campo `isochrone`, REST
  legacy 404); r5py fa matrici origine->destinazione in batch, meglio dei poligoni
  per contare i servizi. Java: Temurin JRE 25 portatile in `data\otp\jdk-25.0.4.1+1-jre`
  (OTP 2.10 voleva Java 25, non 21; class file 69).
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
- Python: sul PC il `python` nel PATH (Python 3.14, `AppData\Local\Python\pythoncore-3.14-64`),
  3.13.5 sul Pi. NON usare Anaconda (`C:\Users\campe\anaconda3`, 3.8.8, fuori dal PATH): il suo
  modulo `json` è rotto (virgola in più in `lib\json\decoder.py` riga 353, ogni lettura JSON
  fallisce). Diagnosi dell'8/10; file di diagnosi tolto l'11/10.
- Comandi sul PC: Claude non ha un terminale sul PC (solo lettura/scrittura file). Ciò che va
  eseguito sul PC lo lancia Leo con un `.bat` a doppio clic preparato da Claude.
- Si tiene solo ciò che serve: doppioni e file inutili si tolgono.
- Sezioni 2011 e 2021: accettato un accorpamento approssimato.
- Richiesta a MTM / Agenzia Mobilità Piemontese: INVIATA da Leo (prima del 10/10): perimetro
  delle zone di campionamento IMQ e altre elaborazioni utili. In attesa di risposta. Telefonia e
  validazioni GTT: rimandate (bozza `docs/richiesta_dati_telefonia.md`).
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

## 1. Raccolta continua (Pi attivo; PC fermo dal 10/10)

Stato all'11/10 15:07: il Pi raccoglie (file della mappa aggiornati dalla sync). Backup dell'11/10
03:01 valido: 324 MB, 1.981.209 posizioni mezzi, 188.352 flussi 5T, 66.054 accuratezze,
133.007 trip_update (dal 10/10 13:17 UTC al 10/10 21:59 UTC), 178 avvisi, 71 errori.
DA VERIFICARE: i trip_update si fermano alle 21:59 UTC (mezzanotte locale) mentre i mezzi
continuano fino alle 00:55 UTC. Può essere il servizio notturno quasi nullo oppure `gtt-ritardi`
fermo: controllare con la verifica diurna (attività 4).

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
    `data/storico_copia_leopi.sqlite` (cancellata il 10/10 su richiesta).
  - Verificato: il DB cresce e genera `live.js`, `stat.js`, `agg_cache.json`, `replay_*.js`.
  - `gtt-raccolta` attivo e abilitato all'avvio; `Restart=always` in systemd.
  - Dal 10/10 ~15:17 anche `gtt-ritardi`, attivo e abilitato all'avvio: raccoglie ogni 60 s
    `trip_update` e `alerts` nelle tabelle `trip_update_gtt` e `avvisi_gtt` dello stesso DB.
    La decodifica GTFS-RT e' stata corretta: gli aggiornamenti per fermata sono il campo 2,
    il campo 3 e' il veicolo. Nella prima verifica, 1.424 osservazioni, 0 `delay`, ma
    `stop_time_update` presente nelle osservazioni (il campione era di pochi minuti).
  - Backup PC settimanale: `scripts/backup_da_leopi.py` usa l'API SQLite, copia via SCP,
    controlla `integrity_check`, conteggi e intervalli e sostituisce il file PC solo se valido.
    Attivita' Windows `GTT backup storico Pi`, domenica 03:00, `StartWhenAvailable`; prova
    manuale riuscita con `LastTaskResult=0`. Snapshot corrente `data/storico_backup.sqlite`
    (229.273.600 byte, `integrity_check=ok`; verifica 10/10 ~15:22).
  - Sync verso il PC: `scripts/sync_da_leopi.bat`, attività di Windows "GTT sync da leopi"
    ogni 5 minuti. Corretto il batch: prima nascondeva gli errori `scp` e restituiva sempre
    codice 0. Ora riporta gli errori; prova manuale e schedulata riuscite, hash SHA-256 uguali
    per live/stat/cache e tutti i replay.
  - Comandi raccolta: `systemctl status gtt-raccolta`, `journalctl -u gtt-raccolta -f`,
    `sudo systemctl stop|start|restart gtt-raccolta`.
  - Comandi ritardi: `systemctl status gtt-ritardi`, `journalctl -u gtt-ritardi -f`.
- **PC**: raccolta fermata il 10/10 ~15:23 con `installa_sfondo.py rimuovi`; file STOP presente,
  avvio automatico rimosso e nessun processo GTT rimasto. La sync mappa dal Pi continua.
- **Confronto PC/Pi (sola lettura, 10/10)**: schema identico per le cinque tabelle originali;
  0 chiavi 5T presenti solo sul PC, 109 presenti solo sul Pi. Per `mezzi_gtt`, senza chiave
  univoca, le letture PC avevano soltanto due snapshot non appaiati entro 30 s al Pi (scarti
  31 e 33 s in ~38 ore); nessun intervallo esclusivo PC rilevante. Merge completo non fatto,
  per evitare duplicati. Il feed mezzi ha avuto un lungo intervallo senza posizioni sia nel
  campione PC sia nel Pi; non risultavano posizioni PC aggiuntive da recuperare.
- `data/storico_copia_leopi.sqlite` (copia iniziale) cancellata il 10/10 su richiesta di Leo;
  il backup attuale e' `data/storico_backup.sqlite`.

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
  (rivista l'11/10: vedi sotto e attività 4).
- `12_ritardi_gtt.py` (libreria standard; non tocca lo storico né i grezzi; accetta `--db`):
  `raccogli` → `data/processed/ritardi_<giorno>.csv` (con `con_delay`, `con_stu`) +
  `avvisi_<giorno>.json`; `analizza` → corse per linea/ora, soppresse, match trip_id↔GTFS,
  sintesi avvisi, decodifica dei `.pb` alerts.
- Prova notturna: 1 corsa (67U, soppressa, match 1/1); 154 avvisi (cause top
  PROBLEMA_TECNICO 77, LAVORI 36; effetto top DEVIAZIONE 110; 3 con severità 4 fuori
  specifica, da chiarire; 17 linee e 1.093 fermate toccate).
- La raccolta una tantum sul PC del 9/10 si è fermata dopo ~3 h con 1 sola riga utile
  (`ritardi_20261009.csv`, 432 byte): superata dalla raccolta continua `gtt-ritardi` sul Pi.
- ATTENZIONE (11/10): la conclusione "il feed non pubblica ritardi" è nata con la decodifica
  sbagliata (campo 3 letto come aggiornamenti per fermata). Dopo la correzione del 10/10 gli
  `stop_time_update` ci sono. Il giudizio resta sospeso fino alla verifica diurna (attività 4).

## 8. Riordino e pulizia (8/10)

- Tolti da git `README.md` e `PASSAGGIO_CONSEGNE.md` (assorbiti qui); `mappa_torino.html` ora
  committata.
- Cancellati doppioni e file sbagliati (copie di R01_21, `BT21-sez-M04` con POP21=0, file di
  sistema), `07_elabora_matrici_pendolarismo.py` (rotto) con i suoi output vuoti, i
  `tmp_check_*.py`. Dati ISTAT spostati da `docs/` a `data/raw/istat/`.
- 11/10, seconda pulizia (decisa da Leo, eseguita con `PULIZIA_GTT.bat`): tolti strumenti OTP
  (`otp.jar`, `jdk-21...`, zip Temurin 21 e 25, `provagtfs/`, log del test OTP), estratto
  `nord-ovest-261008.osm.pbf` (riscaricabile da Geofabrik, il taglio resta), `storico.sqlite` del
  PC (superato dal backup), `istat/storiche/` (1991, 2001), R02–R20 degli indicatori regionali,
  `carta_sintesi_aree_dwg.zip`, `ATTIVA_GIT.bat`, il ramo git `GT23-pulizia-grafica-del-mode` e i
  documenti superati `QUALITA_DATI.md`, `PIANO_UI_E_SCENARI.md`, `diagnosi_json.md`,
  `richiesta_MTM_IMQ.md` (quanto serve è in questa memoria). La vecchia `docs/istat/` non esiste più.

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

## 12. Motore di percorsi R5 e taglio OSM (10/10)

- Scaricato da Geofabrik `nord-ovest-261008.osm.pbf` (564 MB, Nord-Ovest intero: Geofabrik
  non ha il Piemonte da solo). Cancellato l'11/10 dopo il taglio (riscaricabile).
- `scripts/17_taglia_osm.py` (pyosmium 4.3.1 via pip; NON include il comando `osmium`):
  due passate, tiene in RAM solo i nodi del riquadro. Riquadro Torino ~18 km + margine
  (lon 7.45-7.93, lat 44.90-45.24). Esce `data/otp/rete/torino_cintura.osm.pbf`:
  **20,6 MB**, 2.317.259 nodi, 326.489 way. Relazioni NON copiate (scelta dichiarata:
  ai percorsi servono strade, non multiparchi).
- Test OTP abbandonato: il feed GTFS era ok (grafo transit in 15 s, 7.043 fermate) ma OTP
  2.10 non ha le isocrone (vedi Decisioni).
- Verifiche fallite e corrette in cammino: OTP 2.10 vuole Java 25 (non 21); pyosmium 4.x
  ha `osmium.index.create_map("flex_mem")` (non piu' `.map.create_flex_mem`).
- R5: rete costruita in ~40 s (poi ~2 s con la cache); `r5-v7.5.1-r5py-all.jar` scaricato
  da r5py in `AppData\Local\r5py`. Prova su 5 sezioni: centro con 1412 negozi entro 15
  min a piedi, borgo periferico con zero: plausibile.

## 13. Accessibilita' per sezione (motore R5: giro completo FALLITO, da rifare)

- `scripts/18_accessibilita.py`: per ogni sezione con residenti (centroide del poligono):
  - A PIEDI 15 min: conteggio servizi per gruppo (scuole, salute, cibo, fermate, verde);
  - COL TP 45 min alle 8, 14, 23, 2 (lunedi' 2026-10-12, 126 servizi attivi verificati
    in calendar): conteggio per gruppo; le coppie oltre un margine in linea d'aria
    dall'origine non vengono contate (non possono stare nel cutoff).
- Destinazioni: catalogo istruzione (844), salute (475), commercio (31.405), fermate GTFS
  (7.043), verde = way chiuse OSM con tag leisure/landuse (12.072; il file aree verdi del
  GeoPortale resta la fonte migliore per dopo).
- Bug trovati e corretti: centroide con lat/lon invertite (sezioni fuori mappa, conteggi
  a zero), id sintetici contro id di censimento, indici di destinazione per sottoinsieme,
  `locations=True` per i way, conversione Timedelta->minuti, margine in metri non
  convertito in gradi.
- Campione 200 sezioni validato (`logs/accessibilita_campione.log`): mediane TP 8:00
  8250 servizi -> 02:00 1385; centro 1412 negozi a piedi; nessun conteggio negativo.
- Giro completo su 8317 sezioni lanciato il 10/10 ~19:40: FALLITO l'11/10 ~01:18 per memoria
  esaurita (`numpy ... Unable to allocate`, `logs/accessibilita_completo_err.log`). Fatti: a piedi
  in 6 min, ore 08 complete in 4,5 h (16.403 s, 208 lotti), ore 14 ferme al lotto 119/208. Lo
  script scrive solo alla fine: perso tutto. `accessibilita.json` contiene ancora il campione
  di 200. Cause: PC con 8 GB, Java a 3 GB, ogni lotto TP = tabella da ~1,9 milioni di righe
  (40 sezioni x ~47.000 destinazioni: il margine di 15 km non filtra quasi nulla), e altri due
  processi opencode attivi. Stima vera del giro completo: 9–10 h, non 5,5.
- Controllo dell'11/10 sul campione di 200 (99 sezioni in Torino, 101 fuori): il motore è
  corretto. In Torino R5 a piedi dà mediane cibo 686, scuole 16, salute 9, pari al ~91% del
  conteggio in linea d'aria entro 720 m (coerente con i 3,6 km/h predefiniti di r5py: 15 min =
  900 m di strada). Fuori Torino scuole/salute/cibo valgono 0 perché i cataloghi sono solo del
  Comune: le mediane basse del rapporto (cibo 9, scuole 0) mescolavano i due gruppi. 3 sezioni di
  Torino su 97 hanno R5 < 20% della linea d'aria (possibile aggancio alla rete, da guardare).
  Lo script calcola i margini a 4,8 km/h ma R5 cammina a 3,6: incoerenza innocua (margine più
  largo), da sistemare con la scelta della velocità. Piano: `docs/PIANO_ACCESSIBILITA.md`.
- Tutto ORARIO PROGRAMMATO [STIMATO]: niente ritardi, capienze o domanda.

## 14. Vulnerabilita' per sezione (fatto)

- `05_prepara_sezioni.py` esteso coi titoli di studio R01 2021 (P83 pop 9+, P86 senza
  titolo, P87 elementare, P88 media, P89 diploma, P90 terziaria; tracciato ISTAT
  verificato). Rieseguito: tutti i totali combaciano con la memoria (occupati 346.734,
  15-64 528.512, 5-14 69.900, 65+ 220.883, Torino 6.916 sezioni / 848.748 abitanti,
  area 1.557.493; aggancio 8317/8317). Torino: pop 9+ 792.797, senza titolo o solo
  elementare 16,1%.
- `scripts/19_vulnerabilita.py`: indice 0-100 per sezione = media pesata dei percentili
  di 4 componenti censimento (non occupati 15-64, senza titolo o solo elementare,
  affollamento abitazioni, quota 65+). Pesi regolabili con `--pesi`. Se esiste
  accessibilita.json, aggiunge serv/verde a piedi (bollino CENSIMENTO+STIMATO).
- Tre difetti trovati in prova e corretti:
  1. sezioni di 2-40 abitanti dominavano la classifica -> percentili PESATI per
     residenti + attutimento verso la media d'area (v=(k+m*lam)/(d+lam), lam=100
     persone, 20 abitazioni);
  2. 50 sezioni-RSA (case di riposo: es. 584 anziani, zero abitazioni) arrivavano in
     cima -> riconosciute (regola: ab=0, p>=20, 65+/p>0,8), escluse dal rango,
     marcate "istituzionale" nel JSON;
  3. il reddito non esiste per sezione: non entra (solo MEF per comune, altra scala).
- Uscite: `data/processed/vulnerabilita.json` (8267 residenziali + 50 istituzionali) +
  `docs/RAPPORTO_VULNERABILITA.txt`. Indice 1,1-98,9, mediana 48,3; il top-10 ora e'
  sezioni reali da 41-559 residenti.
- Decisione Leo (10/10): in mappa la voce unica "Criticità" raggruppa accessibilita' +
  offerta/linee + vulnerabilita'; il VALORE immobiliare NON e' una criticita' e resta
  un'analisi separata (punto OMI).

# ATTIVITÀ DA FARE (in ordine di priorità)

Ordine confermato da Leo l'11/10: accessibilità -> Criticità in mappa -> metro di notte.
Si procede passo passo, una cosa alla volta, con le decisioni chieste a Leo.

## Priorità alta

1. **Accessibilità — rifare il giro completo (sezione 13)**: piano in
   `docs/PIANO_ACCESSIBILITA.md`, APPROVATO l'11/10 (servizi cintura da OSM con script 20,
   salvataggio a tappe, meno memoria, 4,8 km/h, destinazioni accorpate, prova, giro di notte con
   il PC libero, controlli). Numerazione script: 20 = servizi OSM cintura, il prossimo libero è 21.
2. **Tema mappa "Criticità"**: una voce, 3 sotto-scelte: accessibilità (da 18, bollino
   [STIMATO]), offerta/linee già esistente spostata qui, vulnerabilità (da 19, [CENSIMENTO]).
   Assorbe la vecchia voce "Criticità 0-100". File: `scripts/mappa_template.html`,
   `scripts/04_genera_mappa.py`.
3. **Primo scenario: metro aperta di notte**: baseline notturna dall'accessibilità (ore 23 e 2).
   GTFS modificato con le corse notturne della metro e ricalcolo con R5. Uscita: minuti
   risparmiati x residenti + mappa prima/dopo con l'avviso obbligatorio (sotto). Costi e
   manutenzione notturna fuori dal modello (dichiararlo).
4. **Verifica diurna del feed ritardi (oggi 11/10, 20:15)**: attività Windows `GTT verifica
   ritardi diurna` (`scripts/verifica_ritardi_diurna.bat`): backup e analisi 08:00–20:00 locali in
   `docs/RAPPORTO_RITARDI_GTT.txt` (log `logs/verifica_ritardi_diurna.log`). Poi: (a) decidere se
   il feed ha ritardi veri; (b) capire se `gtt-ritardi` si ferma a mezzanotte; (c) correggere
   sezione 7, "Dati mancanti" 3 e attività 7; (d) togliere i file della prova del 9/10
   (`ritardi_20261009.csv`, `avvisi_20261009.json`, `ritardi_analisi.json`).

## Priorità media

5. **Interscambio Fermi**: flussi dalla cintura (pendolari 2021, IMQ) contro posti disponibili;
   l'occupazione reale va contata a mano qualche mattina.
6. **Verde e calore**: temperatura superficiale (Landsat) x alberate x residenti 65+. Aree verdi
   dallo shapefile `http://geoportale.comune.torino.it/geodati/zip/carta_sintesi_geo.zip`
   (EPSG:3003, CC BY 4.0; isolare "aree verdi"; in alternativa WFS/WMS del GeoPortale Piemonte,
   "Dati di base – Carta di sintesi – Aree").
7. **Affidabilità reale contro orario**: passaggi alle fermate ricostruiti dalle posizioni
   proiettate sui tracciati GTFS (o dai trip_update, se l'attività 4 conferma i ritardi);
   regolarità degli intervalli. Prova su 2–3 linee e verifica sul campo (~20 passaggi annotati).
8. **Città/cintura**: cercare di nuovo i GTFS dei treni SFM e dei bus extraurbani; servizi della
   cintura (cataloghi dei comuni o OSM).
9. **Congestione con 5T**: dove e quando la città si blocca; associazione accuratezza <-> flusso
   <-> ora con 7–14 giorni di nuovi campioni, feriali e weekend (finestra 15–22/10).
10. **Valore e accessibilità**: vicinanza a metro, parchi e servizi nei valori OMI (251 zone,
    analisi grossolana). Fuori dalla voce "Criticità"; dipende dall'attività 1.

## In attesa

11. **Risposta MTM / Agenzia Mobilità Piemontese** (richiesta inviata da Leo: zone di
    campionamento IMQ e altre elaborazioni utili). Serve a correggere i 7 quartieri su 23 che
    non coincidono con la zonizzazione IMQ.

## Priorità bassa / congelate

12. **Matrice tempi e distanze 2021**: `https://www.istat.it/storage/cartografia/matrici_distanze/Piemonte.zip`
    (km e minuti tra comuni, geografia 1/1/2021; nota tecnica in `data/raw/istat/documentazione/`).
    Solo se uno scenario tra comuni la richiede.
13. **MEF 2024**: normalizzare il codice comunale e confrontare copia locale (312 comuni) e ZIP
    nazionale (7.897). Solo confronti tra comuni.
14. **Anagrafe scuole 2026/27**: collegarla alle 610 sedi e chiarire il conteggio (410 statali
    + 195 paritarie col filtro provincia+comune, contro 431+196 del piano).
15. **Matrice 2011 sezione->sezione**: superata da IMQ; solo riferimento storico.
16. **Attività commerciali**: aggregato per categoria/area solo se serve.
17. **Richieste dati esterne**: validazione biglietti GTT e telefonia
    (`docs/richiesta_dati_telefonia.md`).
18. **Mappa statica offerta-domanda** come sintesi.

## Formato degli scenari e avviso obbligatorio (dal vecchio PIANO_UI, tolto l'11/10)

- Uno scenario è un file JSON in `data/scenari/<nome>.json` con SOLO le variazioni rispetto al
  GTFS di base: `nome`, `descrizione`, `base_gtfs` (nome esatto del file in `data/raw/`),
  `giorno_tipo` (`fer`/`sab`/`dom`), `linee_modificate` (`route_id` di routes.txt, `direzione`
  "0"/"1" o assente = entrambe, `intervallo_minuti` 1–120), `linee_nuove`, `linee_soppresse`,
  `linee_deviate`. Fermate solo per codice di stops.txt; un `route_id` nuovo non deve
  collidere. Lettura con `07_elabora_scenario.py` / `calcola_simulazione.py`.
- `simulazione.html` accetta solo l'USCITA dello script (il confronto), non il file di scenario.
- Indicatori subito calcolabili: passaggi/ora per fermata e sezione, attesa teorica (intervallo/2),
  residenti entro 400 m da servizio frequente, km-vettura; con R5 anche minuti risparmiati.
- Ogni mappa, scheda o esportazione di uno scenario mostra: "SIMULAZIONE SU ORARIO PROGRAMMATO —
  offerta potenziale calcolata sull'orario GTFS modificato; non tiene conto di traffico, ritardi,
  capienza, domanda effettiva, regolarità. Dati [PROGRAMMATO]/[STIMATO], non [MISURATO]."
- Bollini standard nelle schede: [MISURATO], [PROGRAMMATO], [STIMATO], [CENSIMENTO], [DATI SCARSI].
  I sensori 5T con accuratezza 0 non vanno mostrati come "strada libera".

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

## Prodotti pronti, NON ancora in mappa (10/10)

- `data/processed/vulnerabilita.json` + `docs/RAPPORTO_VULNERABILITA.txt`: indice 0-100
  per sezione (sezione 14), bollino [CENSIMENTO].
- `data/processed/accessibilita.json` + `docs/RAPPORTO_ACCESSIBILITA.txt`: servizi
  raggiungibili per sezione (sezione 13); al 10/10 sera il giro completo e' in corso,
  il file contiene il campione 200 finche' non finisce. Bollino [STIMATO].
- `data/processed/sezioni_torino.json` ora include i titoli di studio per sezione
  (ist9, i0, iel, im, isu, it).

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
- `istat/altro/`: `Dati_regionali_2021/` (solo R01 + tracciato; R02–R20 tolti l'11/10),
  `MatriciContiguita_Province_2019_2025/`.
- `istat/documentazione/`: note tecniche (pendolarismo 2011, contiguità 2025, distanze 2023).
- Altro: `gtt_gtfs_*.zip`, feed tempo reale (`*_vehicle_position_*`, `*_trip_update_*`,
  `*_alerts_*.pb`), `5t_flussi_*.xml`, `zone_statistiche_*`, OMI
  (`QIP1445919_CMPLRD98T08F335C/`), CSV del Comune, MEF (`Redditi_..._IRPEF_..._2024.zip` +
  cartella locale), `IMQ2022_opendata_web/` (Access + metodologia),
  `ex_quartieri/` + `ex_quartieri.zip` (23 quartieri di Torino, shapefile EPSG:3003),
  `StrutturaDati_PercorsiCiclabili.pdf`,
  `IMQ-2022_EP_REPORT-COMPLETO-2.1.pdf`.

## Presenti ma non usati

- **MEF 2024**: 7.897 record comunali nel ZIP; la copia locale (312 comuni) usa un codice
  comunale diverso (attività 13).
- **Contiguità provinciali**: non servono. Matrici 1991/2001 e R02–R20 tolte l'11/10.

---

# DATI MANCANTI

1. **Domanda per ora e fermata** (chi sale e quando): non pubblica. È il dato che più
   cambierebbe la mappa. Strade: validazione biglietti GTT o telefonia aggregata (attività 17).
2. **Pendolari 2021 per sezione**: non pubblici. Mezzo e orario esistono solo per comune e
   solo nel 2011.
3. **Ritardi GTT**: da chiarire con la verifica diurna (attività 4); se il feed non li ha,
   stimabili dalle posizioni (attività 7).
4. **Cintura**: orari di treni SFM e bus extraurbani non trovati; cataloghi dei comuni assenti
   (attività 8).
5. **Numeri sugli attrattori**: capienze, iscritti, visitatori ed eventi di scuole, ospedali,
   impianti, musei. Restano attrattori potenziali, non viaggi.
6. **Disponibilità in tempo reale** di sharing, ricarica e parcheggi (es. occupazione di
   Fermi, attività 5).
7. **Addetti per sezione** (dove si lavora).
8. **Da scaricare per le attività**: temperatura superficiale Landsat (6), matrice delle
   distanze (12). L'estratto OSM c'è già (taglio in `data/otp/rete/`).

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
- **Accessibilità (18)**: tutta [STIMATO] su orario programmato; velocità cammino
  predefinita di R5 non ancora verificata sul campo; le RSA sono escluse dall'indice di
  vulnerabilità e contate a parte; i rapporti di vulnerabilità sono attuititi verso la
  media d'area (lambda 100 persone / 20 abitazioni); il gruppo "cibo" usa tutte le 31.405
  attività del catalogo senza distinzione per categoria.
- **Criticità sociali**: la nazionalità mostrata come criticità rischia di stigmatizzare
  quartieri (es. Aurora, Barriera, Porta Palazzo). Usare indicatori di vulnerabilità.
- **Dati di anni diversi**: sezioni 2011 e 2021 senza codice comune (accorpamento
  approssimato). OMI sono valori ordinari per zona, non stime di singoli immobili.
- **Zone IMQ**: le 189 zone C/E/R (comuni) sono esatte; i 23 quartieri di Torino sono i confini
  del 1984 e non coincidono con la zonizzazione IMQ per 7 su 23 (sezione 10).
- **Storico**: l'originale vive sul Pi; sul PC c'è una copia settimanale (domenica 03:00). Si
  possono perdere al massimo ~7 giorni se la scheda del Pi si guasta.
- I `.bat` di raccolta sul PC (`installa_raccolta`, `stato`, `ferma`, `riavvia`,
  `raccolta_continua`) restano solo come ripiego se il Pi si guasta; le funzioni Windows del
  supervisore non sono mai state provate su Windows.
- **Accessibilità e cintura**: scuole, salute e cibo vengono dai cataloghi del solo Comune di
  Torino; fuori Torino verranno da OSM (decisione 11/10), fonte meno completa: al confine
  città/cintura cambia la fonte e va dichiarato, con il rapporto OSM/catalogo misurato in Torino.

---

# DA DECIDERE CON LEO

- Nessuna decisione aperta. Piano accessibilità approvato l'11/10 (cintura riempita con OSM,
  cammino 4,8 km/h, destinazioni accorpate a ~50 m, ore 08/14/23/02; più ore in futuro).
- Le decisioni dell'11/10 sono state prese: pulizia completa (eseguita con `PULIZIA_GTT.bat`),
  documenti superati tolti, ordine dei lavori confermato.
