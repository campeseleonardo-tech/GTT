# Memoria del progetto GTT

Ultimo aggiornamento: 8 ottobre 2026.
Questo è l'unico file di memoria e di passaggio. Non creare altri documenti di memoria.
Leggila all'inizio di ogni sessione e aggiornala alla fine.

## Obiettivo

Mappa web interattiva di Torino (stile Google Maps, in HTML) con: domanda e offerta di mezzi,
punti critici, flussi in tempo reale (simulati dove non misurati), il più vicino possibile agli
orari veri. Per ora solo studio personale, forse da condividere. Area: Torino città più cintura (entro 18 km).

## Struttura delle cartelle (dall'8/10/2026)

- `mappa_torino.html`: la mappa (si apre con doppio clic; generata da `scripts/04_genera_mappa.py`).
- `simulazione.html`: pagina separata della simulazione.
- `MEMORIA_PROGETTO.md`, `AGENTS.md`: questo file e le regole.
- `scripts/`: gli script Python e i file .bat/.py della raccolta. Nessuna cartella dati dentro scripts/.
- `data/` (non va su git): dati veri e generati.
  - `data/raw/`: file scaricati (GTFS, feed tempo reale, 5T, zone statistiche, CSV del Comune, OMI, ISTAT).
  - `data/raw/istat/`: dati ISTAT, divisi per tema (vedi "Dati presenti").
  - `data/processed/`: file prodotti dagli script (sezioni, pendolari, OMI, catalogo).
  - `data/processed/catalogo/`: indice e dati per gruppo del catalogo (script 11).
  - `data/catalogo/`: file `.js` per gruppo generati da 04, caricati dalla mappa su richiesta.
  - `data/storico.sqlite`: archivio della raccolta continua (165 MB l'8/10). Non spostare mentre la raccolta gira.
  - `data/live.js`, `data/stat.js`, `data/replay_*.js`, `data/agg_cache.json`: generati ogni minuto/5 minuti dalla raccolta, usati dalla mappa.
- `docs/`: solo documenti di testo (fonti, diagnosi, richieste, piani). Niente dati grezzi.
- `logs/`: log della raccolta (non su git).

## Decisioni prese (valgono per tutto il progetto)

- Pagina HTML locale, senza server esterno. Dati locali (SQLite), nessun cloud.
- Raccolta continua dei dati: per ora sul PC (funziona), più avanti sul Raspberry Pi (192.168.8.200) se serve.
- Nessuna costruzione della mappa finché i dati non sono ispezionati.
- Python scelto con Leo per le prove: interprete di sistema, versione 3.14.3 (8/10/2026).
- Gli script trovano da soli la cartella GTT: i dati vanno in `data\raw`, i rapporti in `docs`, ovunque si lanci lo script.
- Provare gli script su copie; i file in `data/raw` non si modificano.
- Per il progetto si tiene solo quello che serve: doppioni e file inutili si tolgono.
- Documenti: niente README o file di passaggio separati. Tutto va in questo file.
- Sezioni di censimento cambiate tra 2011 e 2021: accettato un accorpamento approssimato.
- Richieste dati (MTM, telefonia): rimandate a più avanti (bozze in `docs/`).
- Direzione del progetto: ancora da decidere con Leo (simulare le infrastrutture, mappa con gamification, raccolta dati).
- Catalogo: mappa e simulazioni leggono gli stessi file elaborati; la mappa carica un gruppo di dati solo quando viene chiesto; la sintesi unica tra le dimensioni (accessibilità, vulnerabilità, attrattori, affidabilità) è opzionale e successiva.
- Privacy: nei prodotti non entrano telefono, email, PEC, URL né nomi di persona (es. `NOME_ADD` delle attività commerciali, `PHONE` di IMQ).

### Regole per i nuovi dati nella mappa (R1–R3, decise da Leo)

- R1. Solo dati facili. Niente circoscrizioni e niente tabelle nel pannello. Le informazioni extra stanno nel tooltip e nella scheda al clic.
- R2. Anni diversi: se un dato più vecchio si può riassumere in quello più recente, si mostra solo il più recente. Il vecchio si mostra solo se contiene informazione che il recente non ha.
- R3. Tolleranza nei merge tra anni: un codice non agganciato non blocca il merge. Si registra nel log quante righe non si sono agganciate e quali codici. Il merge si ferma solo se la quota non agganciata supera il 2% (costante `TOLL_MERGE = 0.02` in 04).

---

# ATTIVITÀ FATTE

## 1. Riordino e verifica dei dati (8/10/2026)

- Tolti da git `README.md` e `PASSAGGIO_CONSEGNE.md` (contenuto utile assorbito qui).
- Cancellati duplicati e file sbagliati: `scripts/data/` (copia di R01_21.zip), `docs/R01_21/`, `docs/BT21-sez-M04/` (POP21=0), `__MACOSX`, `Thumbs.db`, `._*`, `.DS_Store`, `__pycache__`.
- Spostati tutti i dati ISTAT da `docs/` a `data/raw/istat/` (inventario sotto).
- `.gitignore`: tolta la riga che ignorava `mappa_torino.html` (ora committata).
- Da cancellare con la vecchia cartella `docs/istat/`: `NOTE_FILE_ISTAT.md` (assorbito qui), `LEGGIMI.txt`, `RISULTATI_ELABORAZIONE.md` (template mai compilato).

## 2. Raccolta continua (attiva)

- `scripts/03_raccolta_continua.py`: SQLite `data/storico.sqlite`, tabelle `sensori_5t`, `flussi_5t`, `mezzi_gtt`, `errori`. 5T ogni 300 s, mezzi GTT ogni 60 s. Senza librerie esterne.
- `scripts/supervisore.py`: avvio nascosto all'accesso a Windows, riavvio dopo 30 s, log mensili in `logs/`, impedisce lo stop del PC, finestra domenicale dopo le 20:00 ("continuiamo?"; nessuna risposta in 1 ora = continua; No = ferma, con file `data/STOP_RACCOLTA.txt`), avviso oltre 10 GB. Ogni minuto lancia `06_dati_live.py`, ogni 15 minuti statistiche e replay.
- Comandi: `installa_raccolta.bat`, `stato_raccolta.bat`, `ferma_raccolta.bat`, `riavvia_raccolta.bat`; `raccolta_continua.bat` è solo manuale.
- Scelte dell'utente: avvio automatico, nessuna finestra; log mensili conservati senza limite; dati senza limite di tempo.
- Stato all'8/10 (dal log): attiva e regolare, ~407–408 mezzi GTT localizzati ogni minuto. `storico.sqlite` cresce.

## 3. Mappa (funzionante)

`mappa_torino.html`, generata da `scripts/04_genera_mappa.py` + `scripts/mappa_template.html`. Tutto in un file, motore di mappa scritto a mano, sfondo da internet.

- Livelli: sezioni di censimento (offerta, densità e profilo residenti per occupazione/età), zone statistiche, linee, fermate, traffico 5T, mezzi GTT reali, corse simulate, pendolari, segnalazioni, valore immobiliare OMI, catalogo dei nuovi dati.
- Corse simulate: ogni corsa degli orari GTT (feriali 13.683, sabato 10.747, domenica 6.981) si muove a velocità costante lungo il tracciato. STIMA dagli orari, NON posizione reale.
- Sfondi: chiara (OSM schiarito), stradale (OSM), satellite (Esri). CARTO non si usa (richiede chiave). Google Maps non si usa (chiave a pagamento, da creare con Leo).
- Comandi: giorno tipo, slider al minuto, play/pausa, velocità 1×–240×, zoom, filtro per linea, colore linee per corse/ora o per mezzi reali rispetto al previsto.
- Scenari alternativi: `scripts/07_elabora_scenario.py`, `scripts/calcola_simulazione.py` (usati in `data/scenari/`); la simulazione si apre in `simulazione.html`.
- Correzioni l'8/10: 04 legge i txt in `data/raw/istat/pendolarismo_2021/` (e accetta zip) — i numeri pendolari tornano; corretto un errore che faceva perdere i campi nella conversione JS delle sezioni.

## 4. Sezioni di censimento e indicatori ISTAT 2021 (fatto)

Fasi A0–A7 del piano ISTAT: tutte fatte e verificate.

- A0: ispezione (sola lettura) delle 119 colonne-indicatore di R01, abbinate alle definizioni del tracciato.
- A1: `05_prepara_sezioni.py` aggiunge famiglie e abitazioni alle sezioni. Controllo: nessuna sezione con famiglie > abitanti.
- A2: `04_genera_mappa.py` passa famiglie e abitazioni alla mappa (commit `c677cbf`).
- A5: integrati P101 occupati residenti 15–64 (% sulla fascia), P15+P16 residenti 5–14, P27+P28+P29 residenti 65+.
- A6: verifica merge 8.317/8.317 sezioni abitate agganciate (0 mancanti), nessun valore negativo, coerenza tra fasce e popolazione; test Node della conversione JS superato.
- A3/A4 (tooltip sezione e tooltip pendolari): priorità secondaria, rinviati.
- D1 (dati 2021 presenti): famiglie e abitazioni per sezione. Torino: 6.916 sezioni, 848.748 abitanti, 433.469 famiglie, 502.615 abitazioni occupate, 36.242 edifici.
- D2: pendolari per comune già in mappa (tooltip secondario rinviato).
- D3: indicatori regionali 2021 P101/P15/P16/P27/P28/P29 in `sezioni_torino.json` e nella mappa.

## 5. OMI: valore immobiliare (fatto, O1–O5)

Quotazioni OMI (Agenzia delle Entrate) semestre 2025/2, €/m² per zona e tipologia edilizia. Valori ordinari (pregio/degrado esclusi): non è la stima di un singolo immobile.

- `scripts/08_prepara_omi.py` → `data/processed/omi_zone.json`; 04 la carica; tema "Valore immobiliare (OMI)" con tendina tipologia, legenda, tooltip e scheda.
- Verificato: 68 comuni e 251 zone nell'area mappa; Torino 47 zone; zona Torino B1 "ROMA" tipologia ab 2900–4400 €/m² (locazione 10,5–15,7 €/m²).
- Commit: O1 `483830b`, O2 `d009b81`, O3 `af3a776`, O4 `36c61bf`, O5 `17003bf`.

## 6. Catalogo dei nuovi dati comunali (fatto, gruppi 1–5)

- `scripts/11_prepara_catalogo.py` (sola lettura sui grezzi) → `data/processed/catalogo/catalogo.json` (indice con metadati e statistiche) + un file per gruppo. `04` scrive `data/catalogo/<gruppo>.js`, che la mappa carica su richiesta con `ricarica()` (come `live.js`/`stat.js`): la pagina resta leggera all'apertura.
- 44 dati in 6 gruppi completati: istruzione, salute, commercio, sicurezza/sport, reti, servizi. ~37.819 punti.
- Geometrie: i CSV usano `WKT_GEOM` in EPSG:3003 (Monte Mario / Italy zone 1), convertite in WGS84 con `gb_a_wgs84` di 04. Verificato su Piazza Castello (1396657, 4991756, ritorno esatto) e sulla scuola "VALLETTE A" (45.10352, 7.63338).
- Tema "Catalogo dei dati" in mappa: tendina del gruppo, caselle per singolo dato, legenda, tooltip/scheda dell'elemento e pulsante "i" con la scheda del dato (fonte, anno, licenza, formato, copertura, coordinate, record, duplicati, campi mancanti, anomalie). I gruppi voluminosi (attività 31.271 punti) si disegnano solo da zoom 14.
- Anomalie e controlli registrati: `mercati_tematici` ha COORD_X/Y ≈10 volte più piccole del WKT (si usa il WKT); 1 stazione car sharing fuori area (45.5597/8.0492, "Unità d'Italia"); `strutture_socio_assistenziali` ha 38 `IDCIVICO` ripetuti (non è un id univoco); mercati 42 record→57 elementi e zona blu 19→23 (poligoni multipli); `alberate` 131.994 alberi→1.928 aggregati per ambito (non si disegnano i singoli alberi).
- Anagrafe scuole 2026/27: col filtro provincia+comune TORINO risultano 410 statali e 195 paritari, non 431+196 come nel piano: da chiarire. Non è collegata alle 610 sedi geografiche.
- Verificato in Node (dati veri e funzioni reali del template): preparazione gruppi, ricerca elemento, punto-in-poligono, chiave di disegno. **Verificato a video da Leo l'8/10: funziona bene.**

## 7. Pulizia dei file (8/10/2026)

- Eliminati perché inutili o ridondanti: `scripts/07_elabora_matrici_pendolarismo.py` (rotto e non usato: cercava zip inesistenti; si riscriverà da capo solo se servirà la domanda 2011), i suoi output vuoti `data/processed/pendolarismo_torino_cintura.json` e `data/processed/od_per_fascia.json`, e i controlli temporanei `scripts/tmp_check_*.py` (erano della sessione OMI).
- NON toccati: `scripts/07_elabora_scenario.py` (usato dagli scenari), `scripts/09_analisi_dati_diurni.py` e `scripts/10_analisi_sensori_5t.py` (utili per l'analisi dei dati di giorno).

---

# ATTIVITÀ DA FARE (in ordine di priorità)

Nota generale (vale per la mappa e per i cataloghi): i dati del Comune di Torino coprono **solo la città**; mancano i cataloghi equivalenti dei comuni dell'area metropolitana. Quando studieremo come si muovono gli abitanti, attenzione al bias: la città è coperta, la cintura no.

## Priorità alta

1. **Analisi dei dati di giorno già raccolti (5T)**: profilo dei flussi e degli zeri per giorno/ora, mezzi in ora di punta. Prima va salvata l'accuratezza con ogni misura: oggi non c'è nello schema, quindi lo studio di `accuratezza=0` nel tempo non è possibile finché non si cambia la raccolta. Script di appoggio già presenti: `09_analisi_dati_diurni.py`, `10_analisi_sensori_5t.py`.
2. **Ritardi GTT**: acquisire campioni diurni di `trip_update` (non è nella raccolta continua), poi contare corse e ritardi. Decodificare anche gli avvisi GTT (134 KB).

## Priorità media

3. **Catalogo gruppo 6 — MEF 2024** (redditi IRPEF): normalizzare il codice comunale e confrontare la copia locale (312 comuni della provincia di Torino) con lo ZIP nazionale (7.897 record). Dato comunale: confronti tra comuni, NON per individuare quartieri poveri.
4. **Catalogo gruppo 6 — IMQ 2022** (database Access): esportare e aggregare per zona, scopo, ora e modo rispettando i pesi; escludere `PHONE` e gli identificativi individuali. Serve la geometria delle zone campionarie. IMQ copre anche la cintura (212 zone, 32 in cintura): utile per ridurre il bias città/cintura.
5. **Parchi da shapefile, non dal DWG**: scaricare `http://geoportale.comune.torino.it/geodati/zip/carta_sintesi_geo.zip` (ESRI Shapefile, EPSG:3003, licenza CC BY 4.0); contiene i temi aree verdi, fiumi, isolati e passerelle. Isolare il livello "aree verdi". In alternativa WFS/WMS dal GeoPortale Piemonte (record "Dati di base – Carta di sintesi – Aree"). Il DWG non serve più.
6. **Matrice di tempi di percorrenza e distanze 2021**: scaricare `Piemonte.zip` da `https://www.istat.it/storage/cartografia/matrici_distanze/Piemonte.zip` (CSV: distanze in km e tempi in minuti tra tutti i comuni della provincia e i 7.903 comuni italiani; geografia al 1/1/2021). La nota tecnica è già in `docs/`. Serve per stimare il traffico tra comuni. (Facoltativo: `MatriciContiguita_Comuni_2019_2025.zip` per la contiguità tra comuni, oggi abbiamo solo quella tra province.)
7. **Anagrafe scuole**: collegare le liste 2026/27 alle 610 sedi geografiche e chiarire il conteggio (410 statali + 195 paritarie col filtro provincia+comune, contro 431+196 del piano).

## Priorità bassa / da valutare

8. **Domanda dentro Torino dalla matrice ISTAT 2011 sezione→sezione**: ha senso? È del 9 ottobre 2011 (15 anni fa), senza mezzo né orario, e la città nel frattempo è cambiata. È l'unico dato sub-comunale di origine-destinazione disponibile. Proposta: usarlo solo come riferimento storico o per provare la meccanica della simulazione, non come domanda attuale. Non c'è più uno script: si riscrive solo se Leo decide di usarlo.
9. **Attività commerciali — aggregato spaziale per categoria**: accettata così com'è (conteggi in scheda/legenda, punti solo da zoom 14). Un vero aggregato per categoria/area si farà solo se serve.
10. **Bias città/cintura**: capire come aggiungere al catalogo i comuni dell'area metropolitana, perché oggi il confronto Torino/cintura è sbilanciato.

## Più avanti

11. **Richieste dati esterne**: validazione biglietti GTT (domanda reale per ora/fermata) e telefonia mobile (bozza in `docs/richiesta_dati_telefonia.md`).
12. **Raspberry Pi** per la raccolta; **direzione del progetto** (infrastrutture / gamification / raccolta dati); mappa statica offerta-domanda come sintesi.

## Domanda aperta per Leo

- Nel suo messaggio c'è un "6" da solo in fondo, dopo la frase "fammi domande se ti serve": non è chiaro. Se intendeva l'attività 6 (anagrafe scuole) o altro, lo dica e la aggiorno.

---

# DATI PRESENTI E VERIFICATI

## In mappa

- **GTFS GTT statico**: valido 1/10/2026–31/1/2027 (versione 20261002). 215 linee, 7.045 fermate, 966.946 passaggi programmati.
- **Mezzi GTT in tempo reale**: ~407–408 mezzi al minuto; il feed non ha il `trip_id` (il mezzo si lega alla linea, non alla corsa).
- **Traffico 5T**: 112 sensori, area più ampia di Torino. Salva le misure ma non l'accuratezza associata; `sensori_5t.accuratezza` tiene solo il valore più recente. Significato di accuratezza 0 non verificato.
- **Zone statistiche Torino**: 94 zone (dati 2011, senza popolazione).
- **Pendolarismo ISTAT 2021** (lavoro e studio, comune↔comune): Torino lavoro entrano 138.605, escono 71.297, dentro 212.249; studio entrano 48.730, escono 6.373, dentro 120.148 (numeri uguali alle note).
- **Sezioni di censimento 2021**: Torino 6.916 sezioni / 848.748 abitanti; area entro 18 km 8.317 sezioni abitate / 1.557.493 abitanti.
- **Indicatori regionali ISTAT R01** (2021) sulle 8.317 sezioni abitate (aggancio 100%): Torino 346.734 occupati 15–64 su 528.512 residenti 15–64 (65,6%), 69.900 residenti 5–14, 220.883 residenti 65+.
- **Famiglie e abitazioni** per sezione (2021): Torino 433.469 famiglie, 502.615 abitazioni occupate, 36.242 edifici.
- **OMI 2025/2**: provincia di Torino 312 comuni, 953 zone, 3.119 righe valori, 14 tipologie; in mappa 68 comuni / 251 zone; Torino 47 zone.
- **Catalogo comunale** (6 gruppi, 44 dati): istruzione (610 scuole, 29 università, servizi infanzia), salute (44 accessi ospedalieri, 37 consultori, 243 farmacie [dato ~2011], 151 strutture socio-assistenziali), commercio (31.271 attività, 42 mercati, 16 mercati tematici, 21 luoghi, 51 musei, 20 biblioteche, 26 cinema), sicurezza/sport (77 record in 6 file di pubblica sicurezza, 686 impianti sportivi), reti (143 aree pedonali, 4.151 tratti ciclabili, 58 percorsi accessibili, 23 fermate metro, 87 stazioni bike sharing, 83 car sharing, 95 ricarica elettrica, 39 parcheggi in struttura, 1.817 stalli disabili, 19 zone blu, 3 ZTL, 1.928 aggregati di alberate), servizi (164 sedi amministrative, 78 uffici postali, 15 anagrafici, 3 turistici).
- **Raccolta propria** (`storico.sqlite`): il dato più prezioso che cresce ogni giorno.

## In archivio (pronti, non ancora in mappa)

- **Pendolarismo ISTAT 2011 per sezione** (110 zip, uno per provincia di origine; Torino: `Piemonte_Torino_pendolarismo_2011.zip`, 5,7 MB → CSV da 120 MB): flussi sezione→sezione, ideali per la domanda dentro Torino; NON hanno mezzo né fascia oraria. Torino→Torino: 355.525 pendolari. NON cancellare gli zip delle altre province: contengono chi entra a Torino (es. `Piemonte_Asti` 9.112 pendolari; `Lombardia_Milano` 976).
- **Matrice nazionale 2011** (`matrix_pendo2011_10112014.txt`, 293 MB): TENERLA. Ha mezzo (12 categorie), orario di uscita (4 fasce) e tempo di viaggio (4 classi), a livello comunale, tutta Italia. Non è un doppione degli zip provinciali.
- **Basi territoriali 2021 Piemonte** (`R01_21.zip`): confini e popolazione per sezione (già in uso da 05).

## Inventario dei file grezzi ISTAT (`data/raw/istat/`)

- `pendolarismo_2021/`: `matrix_pendoLAVORO_2021.txt` (12,6 MB), `matrix_pendoSTUDIO_2021.txt` (3,4 MB, stima con modelli), con i `.doc` delle colonne. Usati da 04.
- `2011_sezioni/`: `per_provincia/` (110 zip), `nazionale/` (matrice 293 MB + "Pendolo 2011 documenti_utili").
- `basi_territoriali_2021/`: `R01_21.zip` (74 MB).
- `altro/`: `Dati_regionali_2021/` (R01–R20 + tracciato; R01 in uso), `MatriciContiguita_Province_2019_2025/` (xlsx).
- `storiche/`: `matrici_pendolarismo_1991/` (92 MB), `matrici_pendolarismo_2001/` (166 MB).
- `documentazione/`: note tecniche PDF (pendolarismo sub-comunale 2011, contiguità 2025, matrici delle distanze 2023).
- Altri grezzi in `data/raw/`: `gtt_gtfs_*.zip`, feed tempo reale GTT (`*_vehicle_position_*.pb`, `*_trip_update_*.pb`, `*_alerts_*.pb`), `5t_flussi_*.xml`, `zone_statistiche_*`, `QIP1445919_CMPLRD98T08F335C/` (OMI), i CSV del Comune (scuole, salute, commercio, sicurezza/sport, reti/servizi), `Redditi_..._IRPEF_..._2024.zip` + cartella locale (MEF), `IMQ2022_opendata_web/` (Access + metodologia), `carta_sintesi_aree_dwg.zip`, `StrutturaDati_PercorsiCiclabili.pdf`, `IMQ-2022_EP_REPORT-COMPLETO-2.1.pdf`.

## Dati presenti ma non utilizzati / da preparare

- **MEF 2024** (redditi IRPEF): ZIP nazionale 7.897 record comunali; la copia locale ha 312 comuni della provincia di Torino e usa una forma diversa del codice comunale; Torino ha una riga. Non ancora normalizzato né confrontato.
- **IMQ 2022** (mobilità, database Access): 41.933 interviste, 95.608 spostamenti, 212 zone campionarie. Contiene scopo, orari, origine/destinazione, mezzi e pesi campionari. Non ancora esportato; manca la geometria delle zone.
- **Carta di sintesi – Aree** (aree verdi, fiumi, isolati, passerelle): la versione DWG scaricata (`carta_sintesi_aree_dwg.zip`) non serve; esiste lo shapefile `carta_sintesi_geo.zip` (vedi attività 5).
- **Pendolarismo 1991 e 2001** (~270 MB), **Dati regionali 2021 R02–R20** (~190 MB), **Matrici di contiguità provinciali 2019–2025**: presenti, non servono al progetto attuale (da decidere se togliere).
- **Documentazione di supporto** (rapporto IMQ, PDF struttura piste ciclabili): non sono livelli di mappa.
- **Feed `trip_update`**: l'unico file salvato (3/10) è di 15 byte (solo intestazione); la raccolta continua non salva questo feed.

---

# DATI MANCANTI (che servirebbero)

1. **Domanda per ora e per fermata** (chi sale a che ora): né ISTAT né GTT pubblici la danno. È il dato che più cambierebbe la mappa. Strade: validazione biglietti GTT (da chiedere) o telefonia mobile aggregata (bozza in `docs/`).
2. **Pendolarismo 2021 per sezione**: non pubblico (solo comune).
3. **Mezzo e orario a livello di sezione**: disponibili solo a livello comunale e solo nel 2011 (matrice nazionale).
4. **Tempi di viaggio e distanze stradali 2021**: solo nota tecnica in `docs/`; manca la matrice `Piemonte.zip` (vedi attività 6).
5. **Ritardi GTT di giorno**: non raccolti (il feed `trip_update` non è nello storico).
6. **Offerta di altri operatori**: treni SFM e bus provinciali non trovati.
7. **Capienze, iscritti, flussi e calendari** di scuole, ospedali, impianti sportivi, musei: i luoghi ci sono (catalogo), i numeri no. Quindi restano attrattori potenziali, non conteggi di viaggi.
8. **Disponibilità in tempo reale** di sharing, ricarica e parcheggi: posizioni sì, posti/mezzi liberi no.
9. **Addetti per sezione** (dove si lavora): non risultano.
10. **Dati turistici ed eventi**: nessuno (musei presenti, visitatori no).
11. **Geometria delle zone campionarie IMQ**: da trovare per disegnare i flussi IMQ.
12. **Cataloghi dell'area metropolitana**: mancano i dati equivalenti (scuole, servizi, attività, ecc.) per i comuni della cintura: oggi ci sono solo quelli del Comune di Torino. Da tenere presente per non essere sbilanciati verso la città.

---

# LIMITI E RISCHI DA RICORDARE

- Il sistema non è ancora una simulazione del traffico reale: le corse sono stimate dagli orari.
- Il dato di domanda non ha orari né mezzi (pendolari 2021 per comune e residenti; pendolari 2011 per sezione senza mezzo né orario).
- Traffico misurato solo in 112 punti; il resto è stimato. Domanda = residenti (popolazione "di notte") e pendolari, non persone in movimento.
- Fuori Torino mancano altri operatori e treni: il rosso in cintura può essere solo mancanza di dati. Distinguere sempre "misurato" da "stimato".
- **Bias città/cintura**: i cataloghi dei luoghi (scuole, servizi, attività, ecc.) coprono solo Torino città. Analizzando come si muovono gli abitanti, la città risulterà più "ricca" di attrattori della cintura anche solo perché i dati della cintura mancano: non leggere questa differenza come una differenza reale.
- Il tooltip dice "residenti", non "persone in movimento". Famiglie e abitazioni sono il censimento dei residenti: non dicono chi si sposta.
- OMI sono valori ordinari per zona/tipologia: non è la stima di un singolo immobile.
- Geometrie dei nuovi dati comunali convertite da EPSG:3003: il dato di mercati_tematici ha COORD_X/Y errate (~10×) e si usa il WKT.
- Dati di anni diversi: le sezioni 2011 e 2021 non hanno codice in comune (accorpamento approssimato); la mappa mostra i dati 2011 solo se aggiungono informazione.
- Qualità dei dati di giorno non ancora analizzata (flussi 5T, zeri, accuratezza; ritardi GTT assenti).
- Windows: finestra settimanale, anti-stop e avvio automatico non provati (testati solo su Linux).
- Lo sfondo della mappa (mattonelle Esri/OSM) non è stato provato dal mio ambiente, che non raggiunge i server delle mattonelle; il browser del mio ambiente non apre `file://`. La mappa è stata comunque verificata a video da Leo (funziona).
- Il progetto è di studio: niente dati personali, niente invio di niente a nome di Leo.

---

# DA DECIDERE CON LEO (aperte)

- Spazio dati: togliere `storiche/` (1991, 2001, ~270 MB) e `Dati_regionali_2021/` R02–R20 (~190 MB)? La matrice nazionale 2011 NON si toglie (ha mezzo e orario); gli zip provinciali non si tolgono.
- Matrice ISTAT 2011 sezione→sezione per la domanda dentro Torino: usarla (come riferimento storico) o lasciarla in archivio? (vedi attività 8)
- Direzione del progetto: simulare le infrastrutture, mappa con gamification, o raccolta dati?
