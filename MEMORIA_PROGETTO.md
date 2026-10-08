# Memoria del progetto GTT

Ultimo aggiornamento: 8 ottobre 2026. Fatto oggi: integrazione OMI completata in mappa (O1–O5) + verifiche; in precedenza riordino cartelle, inventario ISTAT, tema Pendolari sistemato, famiglie e abitazioni per sezione (A1–A2).
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
  - `data/raw/`: file scaricati (GTFS, feed tempo reale, 5T, zone statistiche).
  - `data/raw/istat/`: dati ISTAT, divisi per tema (vedi sezione ISTAT sotto).
  - `data/processed/`: file prodotti dagli script (sezioni, pendolari).
  - `data/storico.sqlite`: archivio della raccolta continua (165 MB l'8/10). Non spostare mentre la raccolta gira.
  - `data/live.js`, `data/stat.js`, `data/replay_*.js`, `data/agg_cache.json`: generati ogni minuto/5 minuti dalla raccolta, usati dalla mappa.
- `docs/`: solo documenti di testo (fonti, diagnosi, richieste, piani). Niente dati grezzi.
- `logs/`: log della raccolta (non su git).

## Decisioni prese

- Pagina HTML locale, senza server esterno. Dati locali (SQLite), nessun cloud.
- Raccolta continua dei dati: per ora sul PC (funziona, vedi sotto), più avanti sul Raspberry Pi (192.168.8.200) se serve.
- Nessuna costruzione della mappa finché i dati non sono ispezionati.
- Gli script trovano da soli la cartella GTT: i dati vanno in `data\raw`, i rapporti in `docs`, ovunque si lanci lo script.
- Provare gli script su copie; i file in `data/raw` non si modificano.
- Per il progetto si tiene solo quello che serve: doppioni e file inutili si tolgono .
- Documenti: niente README o file di passaggio separati. Tutto va in questo file.
- Sezioni di censimento cambiate tra 2011 e 2021: accettato un accorpamento approssimato.
- Richieste dati (MTM, telefonia): rimandate a più avanti (bozze in `docs/`).
- Direzione del progetto: ancora da decidere con Leo (tra simulare le infrastrutture, mappa con gamification, raccolta dati).

## Dati verificati

- GTFS GTT statico: valido dal 1/10/2026 al 31/1/2027 (versione 20261002). 215 linee, 7.045 fermate, 966.946 passaggi programmati.
- Posizioni dei mezzi GTT (tempo reale): funzionano. Circa 407-408 mezzi ogni minuto (dato del log dell'8/10). Il feed non ha il trip_id: il mezzo si lega alla linea, non alla corsa.
- Ritardi GTT (trip_update): il file era vuoto di notte (4/10). Di giorno NON ancora verificato.
- Avvisi GTT: file di 134 KB, non ancora decodificato.
- Feed 5T flussi: 112 sensori, su un'area più ampia di Torino. Molti hanno accuracy=0 e flusso 0 (4/10). Non si sa ancora se accuracy=0 vuol dire "nessun dato" o "sensore spento".
- Zone statistiche Torino (CSV e shapefile, dati del 2011): 94 zone.
- Pendolarismo ISTAT 2021 (lavoro e studio): verificato con lo script 04 l'8/10. Numeri uguali alle note: Torino lavoro entrano 138.605, escono 71.297, dentro 212.249; studio entrano 48.730, escono 6.373, dentro 120.148.
- Sezioni di censimento 2021 (Torino): 6.916 sezioni a Torino, 848.748 abitanti; 8.317 sezioni abitate entro 18 km, 1.557.493 abitanti (script 05 e 04).
- Quotazioni OMI 2025/2 (Agenzia delle Entrate): VERIFICATO l'8/10. Provincia di Torino, 312 comuni, 953 zone, 3.119 righe di valori; Torino 47 zone; 14 tipologie edilizie. Join CSV-KML verificato (47=47). Piano di integrazione nella sezione "Piano OMI".
- Raccolta in background: verificata dal log dell'8/10 (5T ogni 5 minuti, mezzi GTT ogni minuto, nessuna interruzione vista). Il file `storico.sqlite` cresce.

## Dati NON verificati

- Qualità dei dati di giorno: ritardi, sensori 5T con accuracy=0, numero di mezzi in ora di punta. Dal 8/10 la raccolta ha già dati diurni: da analizzare.
- Esistenza di dati su bici/sharing, parcheggi, treni (SFM): non trovati.
- Dati ISTAT sugli addetti (dove si lavora) a livello di sezione: non risultano.
- Windows: finestra settimanale, anti-stop e avvio automatico non provati (testati solo su Linux).
- Lo sfondo della mappa (mattonelle OpenStreetMap, CARTO, Esri) non è stato provato dal mio ambiente, che non raggiunge i server delle mattonelle.

## ISTAT - inventario (aggiornato 8/10/2026)

Regola: ogni volta che si scarica o si sposta un file ISTAT, si aggiorna questa sezione.

### Dove stanno i file

- `data/raw/istat/pendolarismo_2021/`
  - `matrix_pendoLAVORO_2021.txt` (12,6 MB): pendolari lavoro, comune contro comune, tabulazione con tab. Usato da script 04.
  - `matrix_pendoSTUDIO_2021.txt` (3,4 MB): pendolari studio, stesso formato. Usato da script 04. È una stima con modelli statistici, non un conteggio diretto.
  - `leggimi_file_matrix_pendoLAVORO_2021.doc`, `leggimi_file_matrix_pendoSTUDIO_2021.doc`: descrizione delle colonne.
- `data/raw/istat/2011_sezioni/`
  - `per_provincia/`: 110 zip della matrice pendolarismo 2011 per sezione di censimento, una per provincia di ORIGINE (dove vive il pendolare). Il file di Torino è `Piemonte_Torino_pendolarismo_2011.zip` (5,7 MB): dentro c'è `Piemonte_Torino_pendolarismo_2011.csv` (120 MB) e la nota metodologica PDF.
  - ATTENZIONE: gli altri zip NON sono inutili. Contengono i pendolari che entrano a Torino da altre province (verificato l'8/10: `Piemonte_Asti` ha 7.802 righe con destinazione Torino, 9.112 pendolari; `Lombardia_Milano` ha 967 righe, 976 pendolari). Non cancellarli.
  - `nazionale/`: `matrix_pendo2011_10112014.txt` (293 MB, matrice nazionale 2011), con il `.doc` di spiegazione e la cartella "Pendolo 2011 documenti_utili" (classificazioni comuni e questionari). Non ancora confrontato con gli zip provinciali.
- `data/raw/istat/basi_territoriali_2021/`
  - `R01_21.zip` (74 MB): basi territoriali del Piemonte, con confini (SHP) e tabelle di popolazione per sezione. Usato da script 05. Il file è identico al vecchio duplicato, verificato con hash.
- `data/raw/istat/altro/`
  - `Dati_regionali_2021/`: indicatori per sezione 2021, R01 (Piemonte) a R20 (tutte le regioni), più il tracciato. Solo R01 ha un uso potenziale per Torino; gli altri non servono al progetto. Non usato da nessuno script.
  - `MatriciContiguita_Province_2019_2025/`: contiguità tra province 2019-2025 (xlsx). Non usato. Per ora non serve.
- `data/raw/istat/storiche/`
  - `matrici_pendolarismo_1991/` (Pen_91It.txt, 92 MB) e `matrici_pendolarismo_2001/` (matrix_pendo2001.txt, 166 MB) con i leggimi. Non usati. Non servono al progetto attuale.
- `data/raw/istat/documentazione/`
  - Note tecniche PDF: nota metodologica pendolarismo sub-comunale 2011, nota sulla matrice di contiguità 2025, nota tecnica sulle matrici delle distanze (maggio 2023).

### Cosa c'è e cosa si sa

- Pendolarismo 2021 (lavoro e studio): c'è, comune contro comune. Niente mezzo, niente orario, niente zone dentro Torino. Chi si sposta almeno tre giorni a settimana, al 31/12/2021. Torino = codice 001272. Totale Italia lavoro 19.565.808 persone, studio 9.279.329.
- Pendolarismo 2011 per sezione: c'è per tutte le province (zip). Ogni riga è un flusso origine→destinazione: sezione di censimento di residenza, sezione di lavoro/studio, e numero di studenti, lavoratori e totale. NON ci sono mezzo di trasporto né fascia oraria (verificato sul tracciato del file). Lo script 07 NON lo legge ancora (vedi sotto).
- Basi territoriali 2021 Piemonte: c'è (confini e popolazione per sezione).
- Pendolarismo 2011 nazionale: c'è, ma non ancora confrontato con gli zip provinciali.
- Tempi di viaggio tra comuni (matrice 2021): NON scaricata. Solo la nota tecnica (per stimare i ritardi dovuti al traffico tra comuni).
- Addetti per sezione (dove si lavora): NON risultano.
- Pendolarismo 2021 per mezzo e fascia oraria: NON disponibile (nel file 2021 ci sono solo comune e numero).

### Problemi aperti sui file ISTAT

- Script 07 (`scripts/07_elabora_matrici_pendolarismo.py`) cerca un zip unico `docs/matrici-pendolarismo-sezione-censimento-2011.zip` che non esiste, e cerca i file 2021 in `docs/`. Il suo output `data/processed/pendolarismo_torino_cintura.json` è vuoto (`{"2011": [], "2021": []}`). Non è usato dalla mappa. Va riscritto o tolto (decisione di Leo).
- `data/processed/od_per_fascia.json` contiene solo `{}`: non ha un uso noto. Da controllare.

## Mappa (aggiornata 8/10/2026)

`mappa_torino.html` generata da `scripts/04_genera_mappa.py` (+ `scripts/mappa_template.html`). Tutto in un file, motore di mappa scritto a mano, sfondo da internet.

- Livelli: sezioni di censimento (3 colorazioni: poca offerta per abitante, passaggi/ora, abitanti/km²; grigio = nessun passaggio), zone, linee, fermate, traffico 5T, mezzi GTT reali, corse simulate, pendolari, segnalazioni, dati raccolti.
- Corse simulate: ogni corsa degli orari GTT (feriali 13.683, sabato 10.747, domenica 6.981) si muove a velocità costante lungo il tracciato. STIMA dagli orari, NON posizione reale.
- Sfondi: chiara (OSM schiarito), stradale (OSM), satellite (Esri). CARTO non si usa (richiede chiave).
- Comandi: giorno tipo, slider al minuto, play/pausa, velocità 1x-240x, zoom, filtro per linea, colore linee per corse/ora o per mezzi reali rispetto al previsto.
- Il tema Pendolari era vuoto fino all'8/10 (script 04 cercava zip che non c'erano). Ora legge i txt in `data/raw/istat/pendolarismo_2021`: i numeri coincidono con le note.
- Scenari alternativi: script `scripts/07_elabora_scenario.py` e `scripts/calcola_simulazione.py` (usati in `data/scenari/`).
- Limiti: traffico misurato solo in 112 punti; resto stimato. Domanda: residenti (popolazione di notte) e pendolari 2021, senza orari. Fuori Torino mancano altri operatori e treni (il rosso in cintura può essere mancanza di dati). Bici e pedoni: nessun dato. Distinguere sempre "misurato" da "stimato".
- Google Maps: non usato. Servirebbe una chiave API a pagamento, creata da Leo.

## Raccolta in background

- `scripts/03_raccolta_continua.py`: SQLite `data/storico.sqlite` (tabelle sensori_5t, flussi_5t, mezzi_gtt, errori). 5T ogni 300 s, mezzi GTT ogni 60 s. Senza librerie esterne.
- `scripts/supervisore.py`: avvio nascosto all'accesso a Windows, riavvio dopo 30 s, log mensili in `logs/`, impedisce lo stop del PC, finestra domenicale dopo le 20:00 ("continuiamo?"; nessuna risposta in 1 ora = continua; No = ferma, con file `data/STOP_RACCOLTA.txt`), avviso oltre 10 GB. Ogni minuto lancia `06_dati_live.py`, ogni 15 minuti statistiche e replay.
- Comandi: `installa_raccolta.bat`, `stato_raccolta.bat`, `ferma_raccolta.bat`, `riavvia_raccolta.bat`. `raccolta_continua.bat` è solo manuale.
- Scelte dell'utente: avvio automatico, nessuna finestra; log mensili conservati senza limite; dati senza limite di tempo.
- Stato all'8/10 (dal log): raccolta attiva e regolare.

## Pulizia dell'8/10/2026 (cosa è stato fatto)

- Tolti da git: `README.md`, `PASSAGGIO_CONSEGNE.md`. Il loro contenuto utile è in questo file.
- Cancellati: `scripts/data/` (duplicato di R01_21.zip), `scripts/__pycache__/`, `docs/R01_21/` (copia estratta di R01_21.zip, stesse dimensioni), `docs/BT21-sez-M04/` (file sbagliato, POP21=0, come già scritto), `__MACOSX` e file `Thumbs.db`, `._*`, `.DS_Store`.
- Spostati: tutti i dati ISTAT da `docs/` a `data/raw/istat/` (vedi inventario).
- Script 04 corretto: legge i txt in `data/raw/istat/pendolarismo_2021/` e accetta anche zip. Test: la mappa è stata rigenerata, i numeri pendolari sono uguali alle note, il file contiene il valore atteso.
- `.gitignore`: tolta la riga che ignorava `mappa_torino.html` (committato a parte).
- Da cancellare insieme alla cartella `docs/istat/`: `NOTE_FILE_ISTAT.md` (ora in questo file), `LEGGIMI.txt`, `RISULTATI_ELABORAZIONE.md` (template mai compilato).

## Da decidere con Leo (non ancora fatto)

- Spazio in più usato da dati che il progetto non usa: `storiche/` (1991, 2001: circa 270 MB), `Dati_regionali_2021/` R02-R20 (circa 190 MB), la matrice nazionale 2011 NON si toglie (ha mezzo e orario). Gli zip per provincia non si tolgono.
- Script 07 e `od_per_fascia.json` (vedi problemi aperti sopra).

## Dati: cosa si può usare e cosa manca (8/10/2026)

Usabili subito:
- Pendolari 2021 comune contro comune (lavoro e studio): già in mappa. Dà i flussi con la cintura, ma non dentro Torino.
- Pendolari 2011 per sezione (tutti gli zip): flussi sezione→sezione, ideali per la domanda dentro Torino. Senza mezzo né ora.
- Basi territoriali 2021 Piemonte (R01): popolazione e confini per sezione. Già in uso (script 05).
- Dati regionali 2021 R01 (Piemonte): indicatori per sezione (da leggere: possibili età, famiglie, ecc.). Non ancora aperti.
- Raccolta propria (storico.sqlite): mezzi GTT ogni minuto, sensori 5T ogni 5 minuti. È il dato più prezioso che cresce ogni giorno.
- GTFS GTT: orari programmati, tracciati, fermate.
- Zone statistiche Torino (94 zone, dati 2011, senza popolazione).

Dati importanti che mancano:
1. Domanda per ora (chi sale a che ora, a che fermata): né ISTAT né GTT pubblici lo danno. È il dato che più cambierebbe la mappa. Strade possibili: dati di validazione biglietti GTT (chiesti all'azienda), oppure dati aggregati di telefonia mobile (bozza già scritta in `docs/richiesta_dati_telefonia.md`).
2. Mezzo di trasporto e orario: CORRETTO l'8/10 dopo lettura del tracciato. La matrice NAZIONALE 2011 li ha (record tipo L): mezzo (12 categorie, treno, tram, metro, bus, auto, bici, a piedi...), orario di uscita (4 fasce: prima delle 7:15, 7:15-8:14, 8:15-9:14, dopo le 9:14), tempo di viaggio (4 classi). Livello: comune di residenza -> comune di lavoro/studio, tutta Italia, anno 2011. NON a livello di sezione. Per Torino i dati sono su comuni, non sulle sezioni.
3. Pendolari 2021 per sezione: non pubblici a livello di sezione. Solo comune.
4. Tempi di viaggio stradali (matrice 2021): la nota tecnica c'è, la matrice no. Serve per stimare il traffico tra comuni.
5. Ritardi GTT di giorno: il feed `trip_update` era vuoto di notte; da verificare sui dati diurni già raccolti.
6. Offerta fuori GTT: treni (SFM), altri bus provinciali, bici e sharing, parcheggi. Non trovati.
7. Attrattori (scuole, uffici, ospedali, centri commerciali): non scaricati. Possibili fonti aperte da cercare.
8. Dati turistici ed eventi: nessuno.

## Piano di implementazione: nuovi dati nella mappa (rifatto l'8/10/2026)

Stato al 8/10 (sera): A1 e A2 FATTE e committate (sezioni con famiglie "f" e abitazioni "ab", commit a7e6d13; 04 le passa alla mappa, mappa rigenerata con 8.317 sezioni con f/ab, commit c677cbf). A0, A3, A4, A5 da fare. Il piano OMI (sezione qui sotto) ha la priorità su queste.

Regole decise da Leo (valgono per ogni dato futuro):
- R1. Solo dati facili. Niente circoscrizioni e niente tabelle nel pannello. Le informazioni extra stanno nel passaggio del mouse (tooltip) e nella scheda al click.
- R2. Dati di anni diversi: se un dato più vecchio si può riassumere in quello più recente, si mostra solo il più recente. Il dato vecchio si mostra solo se contiene informazione che il recente non ha.
- R3. Tolleranza nei merge tra anni: un codice non agganciato non blocca il merge. Si scrive nel log quante persone o righe non si sono agganciate e quali codici. Il merge si ferma solo se la quota non agganciata supera il 2% del totale (costante `TOLL_MERGE = 0.02` in 04; soglia scelta da me, si cambia lì).

Conseguenze verificate:
- Pendolari 2011 per comune: NON si mostrano. Hanno lo stesso livello del 2021 (comune) ma sono più vecchi: R2 li esclude.
- Flussi 2011 dentro Torino (sezione→sezione, 355.525 pendolari Torino→Torino): NON si mostrano ora. Restano in archivio per le simulazioni future. Non si possono riassumere nel 2021 (le sezioni 2011 e 2021 non hanno un codice in comune).
- Quindi la mappa, con i dati 2011, oggi non cambia.

Dati da mostrare ora (tutti 2021):
- D1. Famiglie e abitazioni per sezione 2021, nel file `SEZ_R01_21.csv` già dentro `R01_21.zip`. Verificato l'8/10 su Torino: 6.916 sezioni, 848.748 abitanti (uguale alla memoria), 433.469 famiglie, 502.615 abitazioni occupate, 36.242 edifici. Nessuna sezione con più famiglie che abitanti.
- D2. Pendolari 2021 per comune: già in mappa (tema Pendolarismo). Si aggiunge il passaggio del mouse. Lo studio è una stima con modelli statistici: va detto nel tooltip.
- D3. Indicatori regionali 2021 per sezione (`data/raw/istat/altro/Dati_regionali_2021/R01_indicatori_2021_sezioni.xlsx`): contenuto ancora non letto. Si mostrano solo quelli che Leo sceglie dopo la fase A0.

Fasi (ogni fase: eseguire, controllare i numeri, aggiornare questa memoria, commit):

A0. Ispezione (sola lettura). Leggere con la libreria standard le intestazioni di R01 (il file è uno zip di XML: leggere `xl/workbook.xml` e la prima riga di ogni foglio). Stampare nel log le colonne. Stop: Leo sceglie al massimo 3 indicatori. Nessun numero viene inventato.

A1. 05 (`05_prepara_sezioni.py`): in `sezioni_torino.json` aggiungere per ogni sezione `"f"` (FAM21) e `"ab"` (ABI21). Eseguire 05 una volta.
  Controlli: numero sezioni di Torino ancora 6.916; somma abitanti ancora 848.748; somma famiglie Torino 433.469; nessuna sezione con famiglie > abitanti.

A2. 04 (`04_genera_mappa.py`): passare `f` e `ab` nell'elenco `sezioni` (oggi passa solo p, a, g, c). Nel log: totali di Torino.
  Controllo: nell'HTML generato compare il totale 433469 (o 433.469 formattato) come valore delle famiglie.

A3. Template (`mappa_template.html`): al passaggio del mouse su una sezione, tooltip con abitanti, famiglie, abitazioni, badge "ISTAT 2021 (residenti di notte)". Il click apre la scheda sezione (`schedaSezione`) con gli stessi numeri. Verificare nel codice (`cercaTip`) se il tooltip sulle sezioni esiste già; se no, aggiungerlo come per le fermate (`tipTxt`).

A4. Template: al passaggio del mouse su un comune nel tema Pendolarismo, tooltip con entrano/escono per lavoro e studio, badge "ISTAT 2021" e "studio = stima". Controllare prima se `cercaTip` ha già il ramo del tema Pendolari; altrimenti aggiungerlo.

A5. Indicatori scelti in A0: stesse regole di A1-A4. Un indicatore per volta, con commit separato.

A6. Verifica:
  - Eseguire 05 (una volta) e 04. Leggere il log: totali e valori attesi di ogni fase.
  - Controllare che `mappa_torino.html` contenga i valori attesi.
  - Se il browser integrato è disponibile, aprire la mappa, passare il mouse su una sezione e su un comune, fare uno screenshot. Se non è disponibile, dire a Leo cosa aprire e cosa deve vedere.

A7. Memoria e commit: a ogni fase, aggiornare l'inventario e lo stato in questo file, un commit per fase.

Non si fa in questo piano: pendolari 2011 per comune, flussi 2011 dentro Torino, circoscrizioni, tabelle nel pannello.

Rischi da dichiarare sulla mappa:
- Famiglie e abitazioni 2021 sono il censimento dei residenti: non dicono chi si sposta.
- Il tooltip dice "residenti", non "persone in movimento".
- Gli indicatori regionali vanno scelti solo se sono 2021 e spiegati in una riga.

Archivio per le simulazioni future (non mostrato ora): matrice 2011 sezione→sezione (tutti gli zip per provincia), con il limite che non ha il mezzo né l'ora. Matrice nazionale 2011 (293 MB): TENERLA. Ha mezzo, orario e tempo di viaggio per comune (vedi punto 2 dei dati mancanti). Non è un doppione degli zip.

## OMI: valore immobiliare nella mappa (FATTO 8/10/2026)

Dato: Quotazioni OMI (Agenzia delle Entrate), semestre 2025/2. Valori di mercato e locazione €/m² per zona OMI e tipologia edilizia. Valori ordinari (pregio/degrado esclusi): **non è la stima di un singolo immobile**.

File raw (sola lettura, non toccare): `data/raw/QIP1445919_CMPLRD98T08F335C/` (CSV + KML).

Implementazione:
- `scripts/08_prepara_omi.py` → `data/processed/omi_zone.json` (area mappa: 69 comuni, 68 coperti; manca solo Moncucco Torinese 5070 = 1,4% < 2%).
- `scripts/04_genera_mappa.py` carica `omi_zone.json` in `dati["omi"]`.
- `scripts/mappa_template.html`: tema **"Valore immobiliare (OMI)"**, tendina tipologia, legenda, tooltip e scheda al click.

Numeri verificati:
- Log mappa: **68 comuni OMI**, **251 zone** (nell'area).
- Torino: **47 zone**.
- Zona Torino B1 **ROMA**: tipologia **ab** (abitazioni civili) **2900–4400 €/m²**; locazione **10,5–15,7 €/m²**.

Commit principali (ramo prova):
- O1: `483830b` (preparazione OMI corretta)
- O2: `d009b81` (integrazione in 04)
- O3: `af3a776` (tema OMI + legenda + tendina)
- O4: `36c61bf` (tooltip + scheda OMI)
- O5: `17003bf` (verifica finale + rigenerazione mappa)

## Prossimi passi (in ordine)

1. [x] OMI: integrazione completa in mappa (O1–O5).
2. [ ] Analisi dei dati diurni della raccolta (dall'8/10): sensori 5T con accuracy=0, ritardi GTT (trip_update) di giorno.
3. [ ] (CAMBIATO l'8/10) La matrice nazionale 2011 NON si confronta per cancellarla: ha mezzo e orario, che gli zip non hanno. Va TENUTA. Ora è nel piano come dato candidato (da decidere con Leo, vedi "Da decidere").
4. [ ] Usare la matrice 2011 per sezione (flussi sezione→sezione, senza mezzo né orario) per il livello Domanda dentro Torino. Per l'ora serve un dato che non abbiamo (vedi "Dati mancanti" in fondo).
5. [ ] Scaricare, se serve, la matrice dei tempi di viaggio 2021 (a mano, sul PC).
6. [ ] Indicatore combinato "punti critici" (poca offerta + traffico lento + scostamenti), con etichetta "dati scarsi" sotto 72 ore di storico.
7. [ ] Dopo una-due settimane di dati: traffico tipico affidabile, simulazione calibrata sui sensori 5T (misurato e stimato sempre distinti).
8. [ ] Richieste dati (MTM IMQ 2022, telefonia): bozze in `docs/`.
9. [ ] Eventuale passaggio sul Raspberry Pi e condivisione della mappa (per ora solo uso personale).

## Piano per fasi

1. Verifica dei dati e riordino (in corso: riordino fatto l'8/10).
2. Raccolta continua (in corso).
3. Mappa statica: offerta (passaggi GTT per ora) contro domanda (popolazione e pendolarismo). Fatto in forma parziale.
4. Simulazione animata tarata sui conteggi reali.
5. Punti critici da dati misurati dopo qualche settimana di raccolta.

## Limiti e rischi da ricordare

- Il sistema non è ancora una simulazione del traffico reale: le corse sono stimate dagli orari.
- Il dato di domanda non ha orari né mezzi (solo i pendolari 2021 per comune, e i residenti).
- Il progetto è di studio: niente dati personali, niente invio di niente a nome di Leo.
