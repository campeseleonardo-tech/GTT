# Fonti dei dati e licenze

## Licenze delle fonti (controllate il 22/10/2026)

«Ripubblicare» = mettere i file di quella fonte nel repository pubblico o nella Release di GitHub. **sì** = la licenza lo permette; **con condizioni** = si può, ma
va rispettata la licenza (attribuzione, ecc.); **NON CHIARO** = la pagina ufficiale non lo dice e non ho indovinato (da chiedere alla fonte o da decidere prima di pubblicare).
«Letto» dice se ho letto io la pagina ufficiale o se il dato viene solo da una ricerca sul web.

| Fonte | Licenza dichiarata | Pagina ufficiale | Ripubblicare i file | Citazione da scrivere | Letto |
|---|---|---|---|---|---|
| **GTT orari programmati (GTFS)** | Creative Commons Attribution (CC BY): la scheda aperTO è di GTT; la regola generale di aperTO è CC BY 4.0 | [scheda aperTO](https://aperto.comune.torino.it/dataset/feed-gtfs-trasporti-gtt) | con condizioni (attribuzione) | «GTT – Gruppo Torinese Trasporti, GTFS, aperTO (CC BY)» | **riconfermata il 24/10/2026** aprendo la scheda aperTO (https://aperto.comune.torino.it/dataset/feed-gtfs-trasporti-gtt): licenza «Creative Commons Attribution» (opendefinition.org/licenses/cc-by), titolare GTT - Gruppo Torinese Trasporti; la pagina non scrive una formula di attribuzione precisa |
| **GTT tempo reale (GTFS-RT: posizioni, ritardi, avvisi)** | Creative Commons Attribution (link opendefinition.org/licenses/cc-by); titolare GTT | [scheda aperTO](https://aperto.comune.torino.it/dataset/feed-gtfs-real-time-trasporti-gtt) | con condizioni (attribuzione). Lo storico grezzo della raccolta non si pubblica: solo riassunti (piano 2) | «GTT – Gruppo Torinese Trasporti, GTFS Realtime, aperTO (CC BY)» | sì |
| **5T: flussi di traffico, parcheggi, ZTL** (opendata.5t.torino.it) | La pagina di Muoversi a Torino dichiara **IODL 2.0** (Italian Open Data License) per i dati dei suoi dataset, ma non una licenza per ogni singolo dataset; il sito dei dati 5T non ha pagine di note legali | [Muoversi a Torino – Open data](https://www.muoversiatorino.it/it/open-data/) | con condizioni (attribuzione). **Testo della IODL 2.0 riletto il 24/10/2026** (https://www.dati.gov.it/content/italian-open-data-license-v20, ultimo aggiornamento della pagina 5/5/2020): serve l'attribuzione (fonte e titolare, con copia o link della licenza); **non** impone la condivisione alle stesse condizioni; uso commerciale permesso; non si deve far credere che il riuso sia ufficiale o approvato dal titolare | «Città di Torino / 5T, dati aperti di Muoversi a Torino (IODL 2.0)» | pagina di Muoversi a Torino sì; testo della IODL sì (24/10/2026) |
| **ISTAT: censimento 2021, basi territoriali, pendolarismo, indicatori** | CC BY 4.0, «salvo diversa indicazione» (il piè di pagina del sito rimanda per errore alla versione 3.0) | [note legali ISTAT](https://www.istat.it/note-legali/) | sì (anche uso commerciale), con attribuzione e indicando le modifiche | «Fonte: Istat» + «elaborazione propria» | sì |
| **IMQ 2022 – indagine sugli spostamenti (Agenzia della mobilità piemontese, MTM)** | **Nessuna licenza indicata**: la pagina dei dati aperti dice solo che l'Agenzia «mette a disposizione di tutti» l'archivio, chiede di tenere conto dei pesi, e il piè di pagina è «© Agenzia della mobilità piemontese»; le matrici origine/destinazione sono «per finalità di studio e ricerca»; per i rapporti vale «diffusione consentita previa citazione della fonte» | [open data IMQ 2022](https://mtm.torino.it/it/dati-statistiche/indagini-old/indagine-imq-2021/open-data-imq-2022/) | **NON CHIARO** (i microdati: meglio non metterli nella Release finché l'Agenzia non risponde; i risultati aggregati con citazione sono più sicuri) | «Agenzia della mobilità piemontese (MTM), Indagine sulla mobilità delle persone e la qualità dei trasporti IMQ 2022» | sì |
| **OMI – quotazioni immobiliari e perimetri delle zone (Agenzia delle Entrate)** | **Nessuna licenza esplicita** sulla pagina delle quotazioni; chiede solo di citare la fonte; le condizioni delle «Forniture dati OMI» non le ho lette | [quotazioni OMI](https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/omi/banche-dati/quotazioni-immobiliari) | **NON CHIARO** (i file grezzi sono stati scaricati a mano da Leo; nella mappa si mostrano solo valori medi per zona) | «Agenzia delle Entrate – OMI» | sì (pagina), forniture no |
| **aperTO – Comune di Torino** (catalogo dei servizi, parcheggi, zone statistiche, ZTL, fermate metro, …) | CC BY 4.0 «salvo diversa indicazione»; riuso consentito a patto di citare sempre la fonte e, quando possibile, l'indirizzo della pagina originale | [informazioni aperTO](http://aperto.comune.torino.it/about) | con condizioni (attribuzione), **dataset per dataset**: la licenza di ogni singolo dataset non è ancora controllata | «Città di Torino, aperTO, [nome del dataset], CC BY 4.0» + indirizzo della pagina | regola generale sì; singoli dataset no |
| **OpenStreetMap** (rete stradale, servizi della cintura) | ODbL 1.0 | [copyright OSM](https://www.openstreetmap.org/copyright) | con condizioni: attribuzione e **condivisione alle stesse condizioni** (ODbL) per i dati derivati: un estratto tagliato si può ripubblicare sotto ODbL | «© contributori di OpenStreetMap» con link a openstreetmap.org/copyright e indicazione della licenza ODbL | sì |
| **Sfondi della mappa (Esri)** | non verificata qui | — | non si ripubblicano (si caricano dal browser) | «Esri, Maxar, Earthstar Geographics» (già nella mappa) | decisione di Leo: consentiti finché il progetto non è commerciale |

**Deciso da Leo il 22/10:** IMQ 2022 e OMI (NON CHIARO) non si pubblicano: restano fuori da git e dalla Release e si riscaricano dalla fonte (`docs/DATI.md`, «Decisioni di Leo»). **Esteso il 24/10 (giro L12):** fuori da git anche i file derivati che ricopiano le celle o le quotazioni della fonte (`data/processed/imq_*.json`, `omi_zone.json`, `traffico_c/domanda_auto.json`, `traffico_c/v3/domanda_v3.json`, `traffico_c/domanda_nodi.npz`); restano in git i risultati riassunti (schede, mappa, rapporti), con la fonte citata. Per rifare i file: scaricare la fonte come sotto e lanciare `python scripts/rifai_tutto.py --da dati` (OMI: script 08; IMQ: script 14, 15, 16; domanda: fase traffico). Se mancano, gli script si fermano e lo dicono. Da ricontrollare sulla pagina ufficiale: GTFS statico di GTT e testo della IODL 2.0.
Se manca la certezza, il dato resta fuori dalla Release e lo script che lo scarica dà solo l'indirizzo.

## Indirizzi e file

### Scaricate dallo script 01 e dalla raccolta sul Pi (script 03)

| Fonte | Indirizzo |
|---|---|
| GTT orari programmati (GTFS) | https://www.gtt.to.it/open_data/gtt_gtfs.zip |
| GTT posizioni mezzi (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/vehicle_position.aspx |
| GTT ritardi corse (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/trip_update.aspx |
| GTT avvisi (GTFS-RT) | https://percorsieorari.gtt.to.it/das_gtfsrt/alerts.aspx |
| 5T flussi di traffico (91 sensori, 5 minuti) | https://opendata.5t.torino.it/get_fdt |
| 5T parcheggi | https://opendata.5t.torino.it/get_pk |
| 5T ZTL | http://opendata.5t.torino.it/get_access_control |
| Zone statistiche Torino (dati del 2011) | http://geoportale.comune.torino.it/geodati/zip/zone_statistiche_csv.zip e ..._geo.zip |

Pagina di riferimento aperTO per GTT tempo reale: https://aperto.comune.torino.it/dataset/feed-gtfs-real-time-trasporti-gtt

### ISTAT

Pendolarismo 2021 (lavoro e studio, comune contro comune), matrici 2011 (110 zip per provincia + nazionale con mezzo e orario), basi territoriali 2021 Piemonte,
indicatori regionali 2021. Dove stanno i file e cosa contengono: inventario ISTAT in `sviluppo/MEMORIA_PROGETTO.md`; l'elenco dei file è in `docs/DATI.md`.

### OMI (Agenzia delle Entrate)

Quotazioni del semestre 2025/2 e perimetri delle zone OMI, provincia di Torino (312 comuni), in `data/raw/omi_2025_2/` (due CSV e `TO20252/` con i KML).
Scaricati a mano da Leo dal servizio Forniture dati OMI / GeoPOI. Non coperto: la provincia di Asti (Moncucco Torinese). Non toccare i file.

### IMQ 2022

Dati aperti dell'Agenzia in `data/raw/IMQ2022_opendata_web/`. Una richiesta di zone di campionamento e altre elaborazioni è stata inviata da Leo; risposta attesa.
Le zone di campionamento: «IMQ2013-22_zone_camp_TO» (Torino) e «IMQ2022_zone_camp_noTO» (resto del Piemonte) dalla stessa pagina.

### Rete stradale

OpenStreetMap, estratto Geofabrik Nord-Ovest, tagliato all'area Torino + cintura dallo script 17 in `data/otp/rete/torino_cintura.osm.pbf`.
L'estratto intero si riscarica da https://download.geofabrik.de/europe/italy/nord-ovest.html

### Costi del viaggio (giro L14, 24/10/2026)

Prezzi consultati il 24/10/2026 e scritti a mano in `data/ref/costi.json` (valore, fonte, indirizzo, data); lo script 103 non contiene prezzi. Si copiano solo i valori, mai tabelle o file:
- carburante: Osservatorio prezzi carburanti del Ministero delle imprese e del made in Italy, interrogazione di zona (https://carburanti.mise.gov.it/ospzSearch/zona), 107 impianti self entro 5 km da Piazza Castello; dato aperto del Ministero. I file CSV con lo storico (mimit.gov.it) non rispondono dal PC di Leo: la media delle 4 settimane non si è potuta fare;
- costo chilometrico ACI 2026: Tabelle nazionali ACI, Gazzetta Ufficiale n. 297 del 23/12/2025, supplemento ordinario n. 40 (atto ufficiale), due valori: Volkswagen Golf VIII 115 CV a benzina e a gasolio;
- consumo in città: schede tecniche WLTP a bassa velocità (autotijd.be per la benzina, km77.com per il gasolio), due valori;
- tariffe GTT (biglietti, abbonamenti) e sosta a pagamento: pagine ufficiali di GTT (gtt.to.it); le pagine non riportano la data dei prezzi.

### Tempi in auto col traffico (TomTom)

Servizio **TomTom Routing API** (piano gratuito, chiave personale in `config_locale.json`, fuori da git), usato dallo script 101 (L6, 24/10/2026):
per un insieme di percorsi di Torino, in due giorni feriali futuri (10 e 11/11/2026) a 4 ore del giorno, il tempo previsto col traffico tipico.
Si usano solo **rapporti** (tempo col traffico / nostro tempo a flusso libero; tempo col traffico / tempo senza traffico), per gruppo e ora.
**Attribuzione: dati di traffico TomTom** (scritta nelle schede 3 e 4). Le risposte grezze e i minuti **non si salvano né si pubblicano**
(`SALVA_GREZZI = False` nello script 101): in git ci sono solo statistiche per gruppo e ora e il fattore a due decimali dei percorsi di controllo.
**Da fare prima di unire in `main`: Leo legge le condizioni d'uso di TomTom** (cosa si può salvare e pubblicare, come citare).
Google Maps NON si usa da programma (le sue condizioni vietano la raccolta automatica): il 2,1 di Google viene da 6 percorsi controllati a mano il 20/10 e resta come confronto.


**Giro L8 (24/10/2026).** Dal giro L8 TomTom è la stima principale dell'auto (decisione di Leo, dopo L6bis). Richieste totali **2.371**: 1.200 di L6bis (percorsi base: 17 luoghi in entrata e uscita, 8 percorsi di controllo nei due sensi, 100 coppie di zone; martedì 10 e mercoledì 11/11/2026, ore 8:00, 13:00, 17:30 e 21:00) e **1.171 di L8** (coppie 101-600 alle 8, coppie 101-300 alle altre tre ore, Piazza Castello → 71 zone alle 8; solo martedì 10/11/2026). Si salvano **solo rapporti** (fattore_rete e congestione, 2 decimali, per percorso, per gruppo e ora) in `data/processed/tempi_traffico.json` e nel rapporto; **mai i minuti né le risposte grezze**; il file di ripresa è fuori da git. Ancora da fare prima di unire in `main`: leggere le condizioni d'uso di TomTom.
## Non pubbliche o non trovate

- Dati da telefonia mobile (TIM/Wind usati dall'Agenzia, Vodafone usati con il Politecnico): non pubblici, nessuna richiesta inviata (idea congelata).
- Non trovati: bici e sharing (ToBike, monopattini, car sharing), posti liberi nei parcheggi pubblici in tempo reale oltre ai garage 5T, feed dei treni urbani (SFM), dati orari ARPA (su aperTO ci sono solo medie annuali). Non vuol dire che non esistano.
- Dati storici di confronto: PUMS Torino 2008 (mappe PDF di flussi, sosta, incidenti, offerta TPL): non leggibili da programma senza digitalizzazione.
