# Piano per un agente — Risultato 6, versione 2 (parcheggi di interscambio)

Scritto da Claude il 18/10/2026 per un altro modello (agente). Le decisioni sono di Leo e **non si cambiano**.
Fai **un passo alla volta, nell'ordine**. Ogni passo finisce con una riga nel file di esito:
`PASSO n: OK` oppure `PASSO n: FERMO – motivo`. Se un controllo non torna: **fermati**, scrivi cosa hai visto
e non inventare correzioni. Contesto e discussione: `docs/PIANO_RISULTATO6.md` (versione 1 e sezione
"Versione 2").

---

## 0. Regole (valgono per tutto il piano)

1. Cartella `C:\projects\Progetti\GTT`. Ramo git **`prova`**: controllalo con `git branch --show-current`;
   se non è `prova`, FERMATI. **Nessun commit** (decide Leo).
2. Python del PATH (3.14), comando `python`. **Non usare Anaconda.** Librerie già installate: numpy, scipy,
   pandas, shapely, pyproj, osmium. Non installarne altre.
3. **Sola lettura** su `data/storico_backup.sqlite` (aprilo sempre con
   `sqlite3.connect("file:data/storico_backup.sqlite?mode=ro", uri=True)`) e su tutto `data/raw/`.
4. **Non modificare nessun file esistente.** In particolare non toccare: `scripts/25_risultato6_interscambio.py`,
   `scripts/24_importanza_vie.py`, `scripts/schede_risultati.py`, `scripts/04_genera_mappa.py`,
   `scripts/mappa_template.html`, `mappa_torino.html`, `simulazione.html`, `MEMORIA_PROGETTO.md`,
   `data/processed/risultato6_interscambio.json`, i file in `data/processed/traffico_d/`.
   Scrivi **solo** i file nuovi elencati in questo piano.
5. Numeri degli script nuovi: **68, 69, 71, 72, 73, 74, 75, 76** (il 70 è già usato). Ogni script ha in cima una
   docstring in italiano semplice: cosa fa, cosa legge, cosa scrive, come si lancia.
6. Ogni script che lavora sulle fermate ha l'opzione `--prova` (prime 400 fermate per `stop_id`): lancialo
   prima con `--prova`, poi completo.
7. Ore: i dati del database sono in UTC. Ora italiana = UTC+2 fino al 25/10/2026 01:00 UTC, poi UTC+1. Usa
   questa regola (come `_locale()` in `scripts/04_genera_mappa.py`), **non** `zoneinfo`.
8. Distanze: formula dell'emisfero (haversine) in metri. Coordinate: attenzione all'ordine — nei file della
   ZTL i punti sono `[lon, lat]`, nelle zone IMQ `[lat, lon]`.
9. Fermate e strade **mai per nome**, solo per coordinate. I nomi servono solo per leggere i risultati.
10. Etichette dei dati: [MISURATO] (sensori, riempimenti), [PROGRAMMATO] (orari GTFS), [STIMATO] (calcoli
    nostri, posti stimati), [CENSIMENTO], [DATI SCARSI] (poche interviste o pochi giorni).
11. Tutti gli output vanno in `data/processed/risultato6_v2/` (creala) e i rapporti in `docs/`. Il file di esito è
    `docs/ESITO_RISULTATO6_V2.md`: crealo al Passo 0 e aggiornalo alla fine di ogni passo.
12. Lingua: italiano semplice in rapporti ed esito, niente gergo.

---

## 1. Cosa esiste già (versione 1)

- `scripts/25_risultato6_interscambio.py` → `data/processed/risultato6_interscambio.json` e
  `docs/RAPPORTO_RISULTATO6.txt`. Per ognuna delle **7.045 fermate** GTT tre segnali, ciascuno trasformato in
  percentile 0-100 (funzione `percentile_rank` dello script 25: valori uguali, stesso percentile), poi la media:
  - **a1** = punteggio 1-5 del corridoio più vicino entro 150 m (`punteggio_corridoio`, da
    `data/processed/importanza_vie.json`, script 24: massimo fra classe OSM, elenco a mano di Leo — minimo 4 — e
    sensore 5T con flusso alto — minimo 3; corridoi per nome);
  - **b1** = corse all'ora nell'ora di punta alla fermata (`corse_ora_punta`, GTFS, feriale 2026-10-12);
  - **c1** = pendolari IMQ della zona (`pendolari_raw`): somma degli spostamenti giornalieri, **tutti i mezzi,
    entrambe le direzioni**, che attraversano il confine Torino↔fuori e toccano la zona.
- Critica = punteggio ≥ 90° percentile (≥ 80,9) e fermata fuori dalla zona Q001 (centro).
  **611 fermate critiche**, 17 coperte (interscambio entro 200 m in linea d'aria), 594 scoperte.
- Interscambi "ufficiali": Stura, Caio Mario, Sofia, Venchi Unica (file del Comune) + Fermi (a mano).

Campi di ogni fermata in `risultato6_interscambio.json` → `fermate[]`: `stop_id, nome, lat, lon, corridoio,
punteggio_corridoio, distanza_corridoio_m, zona_imq, pendolari_raw, corse_ora_punta, perc_corridoio,
perc_corse_ora, perc_pendolari, punteggio_criticita, in_zona_esclusa, fermata_critica,
parcheggio_interscambio, distanza_interscambio_m, garage_vicini, coperta`.

## 2. Decisioni di Leo (fisse)

1. Si resta sulle **fermate**, ma le fermate vicine (due lati della via, più paline nello stesso punto) sono
   **un solo luogo**. Lo si dice sempre.
2. **I segnali della versione 1 restano** (a1, b1, c1); i nuovi si **aggiungono** o, dove sono la versione
   migliorata di uno vecchio, lo possono **sostituire**. La scelta finale la fa Leo guardando i 3 scenari.
3. **Niente interfaccia dinamica**: si preparano **al massimo 3 scenari** fissi. Niente mappa, niente scheda in
   questo giro.
4. **Tutti i parcheggi** (5T, Comune, OpenStreetMap), ognuno con una precisazione sul tipo e sui dati.
5. Nuova misura: **quanto ogni parcheggio fa davvero da interscambio** (posizione, uso orario, condizioni).
6. **Anteprima del riempimento** con i dati che ci sono (raccolta dal 14/10), segnata [DATI SCARSI].
7. **ISTAT 2011**: solo per ciò che cambia poco (quota di chi va in auto, orari di partenza) e solo come
   proporzioni per completare i dati IMQ 2022 dove le interviste sono poche. **Mai numeri assoluti del 2011.**
8. Distanza base 200 m; si riportano anche 100 e 400 m.

---

## 3. Passi

### PASSO 0 — Controlli iniziali

1. Ramo `prova` (regola 1). Crea `data/processed/risultato6_v2/` e `docs/ESITO_RISULTATO6_V2.md` con titolo,
   data, ora di inizio.
2. Controlla che esistano: `data/processed/risultato6_interscambio.json`, `data/processed/importanza_vie.json`,
   `data/processed/imq_od.json`, `data/processed/imq_zone_geo.json`, `data/processed/imq/spostamenti.csv`,
   `data/processed/imq/zone_camp.csv`, `data/processed/velocita_5t.json`,
   `data/processed/traffico_d/tratte.json`, `data/processed/traffico_d/tratte_traffico.json`,
   `data/processed/traffico_d/assi_tratte.npz`, `data/processed/traffico_d/rete/rete_auto.npz`,
   `data/processed/traffico_d/ztl_unificata.json`, `data/raw/gtt_gtfs_20261003_224530.zip`,
   `data/raw/5t_get_pk_20261014.xml`, `data/raw/parcheggi_accesso_controllato_csv.zip`,
   `data/otp/rete/torino_cintura.osm.pbf`,
   `data/raw/istat/2011_sezioni/nazionale/matrix_pendo2011_10112014.txt`.
   Se ne manca uno: FERMO.
3. Database: scrivi nell'esito la data più recente in `occupazione_pk.generato_utc` (atteso: almeno
   2026-10-18; se Leo ha già fatto il fetch del 19/10, più recente). Non è un motivo per fermarsi.
4. Non rilanciare nulla della versione 1: leggi solo i suoi output.

### PASSO 1 — Luoghi di fermata (script `68_luoghi_fermate.py`)

Scopo: raggruppare le fermate vicine in "luoghi".

1. Leggi `fermate[]` da `risultato6_interscambio.json` (7.045 fermate).
2. Unisci **a catena** le fermate entro **40 m** l'una dall'altra (union-find: se A è entro 40 m da B e B da C,
   A, B, C sono lo stesso luogo). Usa una griglia di celle di ~0,0005° per non confrontare tutte le coppie.
3. Per ogni luogo: `id_luogo` (L00001…, ordinati per latitudine poi longitudine), `lat`/`lon` = media delle
   fermate, `nome` = il nome di fermata più frequente (a parità, il più corto), `stop_ids`, `n_fermate`,
   `zona_imq` = zona IMQ del punto medio (con `imq_zone_geo.json`, punto nel poligono; se nessuna, quella della
   prima fermata), `in_centro` = zona_imq == "Q001", `critico_v1` = almeno una fermata con
   `fermata_critica` true, `coperto_v1` = almeno una fermata con `coperta` true.
4. Scrivi `data/processed/risultato6_v2/luoghi.json` e `docs/RAPPORTO_R6V2_LUOGHI.txt`.
5. **Controlli (attesi, ricalcolati da Claude):** 7.045 fermate → **5.080 luoghi** (±1%); luoghi con almeno
   una fermata critica v1 = **461** (±2%); con fermata coperta v1: 10-15. Se fuori: FERMO.
6. Nel rapporto: quante fermate per luogo (1, 2, 3, 4+), i 10 luoghi con più fermate (nome, n), e la frase
   "611 fermate critiche della versione 1 = N luoghi".

### PASSO 2 — Inventario di tutti i parcheggi (script `69_parcheggi_inventario.py`)

Fonti:
- **5T**: `data/raw/5t_get_pk_20261014.xml`, elementi `PK_data` (attributi `ID`, `Name`, `Total`, `lat`, `lng`).
  Togli quelli con "CAMPER" nel nome. Atteso: 41 con camper, **40** senza.
- **Comune**: `data/raw/parcheggi_accesso_controllato_csv.zip` → `parcheggi_accesso_controllato.csv`
  (separatore `;`, utf-8-sig). Campi utili: `DENOMINAZI`, `POSTI_TOT`, `POSTI_ROT` (a rotazione), `POSTI_ABB`
  (abbonamenti), `INTERSCAMB`, `PARK_RIDE`, `TIPOLOGIA`, `COORD_X`, `COORD_Y` (Gauss-Boaga EPSG:3003: converti
  con pyproj in lat/lon; **controllo**: Stura, Caio Mario, Sofia e Venchi Unica convertiti devono cadere entro
  300 m dal punto 5T con lo stesso nome, altrimenti prova `WKT_GEOM` e, se ancora no, FERMO). Atteso: **39** righe; interscambio = `INTERSCAMB`=="SI" o `PARK_RIDE`=="SI" → Stura,
  Caio Mario, Sofia, Venchi Unica.
- **Fermi**: interscambio ufficiale aggiunto a mano (è nel 5T, fuori Comune).
- **OpenStreetMap**: `data/otp/rete/torino_cintura.osm.pbf` con `osmium` (`apply_file(..., locations=True)`).
  Prendi nodi e vie con `amenity=parking`. Per le vie chiuse calcola centro (media dei punti) e **superficie**
  in m² (formula del laccio su coordinate proiettate in metri: x = lon·111.000·cos(45,07°), y = lat·111.000).
  Tag da salvare: `name`, `parking`, `capacity`, `fee`, `access`, `park_ride`, `building:levels`.
  Atteso: **~5.176** parcheggi, **25** con `park_ride=yes`, **586** con `capacity` numerica.

Regole:
1. **Abbinamento** (per non contare due volte): un parcheggio 5T/Comune e uno OSM sono lo stesso se il punto
   5T/Comune cade dentro il poligono OSM o è entro 60 m dal suo centro. Abbina 5T↔Comune per nome normalizzato
   (maiuscolo, senza spazi doppi) **e** distanza < 150 m. Tieni un solo record con tutte le fonti in `fonti`.
2. **Posti**: `posti_dichiarati` = 5T `Total` se c'è, altrimenti Comune `POSTI_TOT`, altrimenti OSM `capacity`.
   Se mancano tutti e il parcheggio OSM ha superficie: `posti_stimati` = superficie / 25 (× `building:levels` se
   presente, solo per `multi-storey`) → [STIMATO]. Se manca anche la superficie (nodo OSM): posti ignoti.
3. **Tariffa**: `a_pagamento` = true per tutti i parcheggi 5T e Comune; per OSM dal tag `fee` (`yes`/`no`),
   altrimenti "ignota".
4. **Tipo** (una sola voce, in quest'ordine): `interscambio_ufficiale` (5 ufficiali) · `garage_5t` (altri
   5T/Comune) · `park_ride_osm` (`park_ride=yes`) · `privato` (`access` in private/no) · `clienti`
   (`access=customers`) · `lungo_strada` (`parking` in street_side/lane/layby) · `osm_pubblico` (tutti gli
   altri).
5. Precisazione per tipo (campo `nota`), da scrivere uguale nel rapporto:
   - interscambio_ufficiale / garage_5t: "posti e riempimento dal 5T" (o "nessun riempimento trasmesso");
   - park_ride_osm: "segnato park&ride in OpenStreetMap; posti solo se indicati";
   - osm_pubblico: "parcheggio aperto da OpenStreetMap; posti dichiarati o stimati dalla superficie";
   - lungo_strada: "sosta lungo la strada: non contata nei posti";
   - clienti: "solo per clienti (es. centri commerciali): non contato";
   - privato: "privato: escluso".
6. Scrivi `data/processed/risultato6_v2/parcheggi.json` (un record per parcheggio: `id`, `nome`, `tipo`,
   `fonti`, `lat`, `lon`, `posti_dichiarati`, `posti_stimati`, `superficie_m2`, `a_pagamento`, `park_ride`,
   `id_5t`, `nota`) e `docs/RAPPORTO_R6V2_PARCHEGGI.txt` (conteggi per tipo, posti dichiarati e stimati per
   tipo, elenco dei 5 ufficiali con i parcheggi OSM entro 500 m: tipo, superficie, posti, tariffa).
7. **Controlli:** 40 parcheggi 5T, 39 Comune, 5 ufficiali trovati tutti; OSM ~5.176 e 25 park&ride. Entro
   500 m da Fermi (45,0766; 7,5903) atteso ~85.000 m² di parcheggi aperti, quasi tutti `fee=no`, incluso un
   sotterraneo di ~30.000 m² a ~180 m (verificato da Claude). Se molto diverso: FERMO.

### PASSO 3 — Riempimento e "firma" oraria (script `71_parcheggi_riempimento.py`) — ANTEPRIMA

Fonte: tabelle `parcheggi_5t (id, nome, lat, lng, totale)` e
`occupazione_pk (generato_utc, id, stato, totale, liberi, tendenza)` del database (sola lettura).

1. Usa solo le righe con `liberi` non nullo e `stato` = 1. Occupazione = 1 − liberi/totale, limitata a 0..1.
2. Ora italiana (regola 7). Giorno valido = giorno con almeno 230 letture per quel parcheggio (su ~288).
   Feriale = lunedì-venerdì; fine settimana = sabato e domenica.
3. Per ogni parcheggio, medie orarie (0-23) separate per feriale e fine settimana, poi:
   - **N** = occupazione media feriale 02:00-04:59; **G** = feriale 10:00-15:59; **M** = feriale 07:00-08:59;
     **W** = fine settimana 10:00-15:59 (se ci sono giorni validi);
   - **ampiezza** = media oraria feriale massima − minima.
4. **Firma** (prima regola che vale, soglie PROVVISORIE, le conferma Leo dopo l'anteprima):
   1. nessuna riga con `liberi` → `nessun_dato`;
   2. meno di 2 feriali validi → `dati_insufficienti`;
   3. ampiezza < 0,05 → `dato_bloccato`;
   4. G − N ≥ 0,20 e (W assente o G − W ≥ 0,10) → `pendolare`;
   5. N − G ≥ 0,10 → `residenziale`;
   6. G − N ≥ 0,20 e W presente e G − W < 0,10 → `destinazione`;
   7. altrimenti → `misto`.
   In più: `pieno` se G ≥ 0,85; `vuoto` se G < 0,15.
5. Scrivi `data/processed/risultato6_v2/riempimento.json` (per parcheggio: giorni validi, profilo orario
   feriale e weekend, N, G, M, W, ampiezza, firma, pieno/vuoto) e `docs/RAPPORTO_R6V2_RIEMPIMENTO.txt` con una
   tabella "occupazione % ogni 2 ore (feriale)" per tutti i parcheggi e la firma. In testa: "ANTEPRIMA
   [DATI SCARSI]: N giorni feriali, dal … al …".
6. **Controlli (attesi da Claude, 3 feriali 14-16/10):** Fermi, Racconigi, Unione Sovietica, V Padiglione =
   `nessun_dato`; Venchi Unica = `dato_bloccato` (~51% fisso); Sofia = `residenziale` (~55% notte, ~32%
   giorno); Porta Susa FS: ~36-39% di notte, ~80-88% di giorno; Caio Mario `vuoto` (1-2%); Stura ~79% notte,
   ~90% giorno (con queste soglie non risulta `pendolare`: va bene, scrivilo). Se Porta Susa FS non ha un ciclo
   giorno/notte chiaro: FERMO (vorrebbe dire ore sbagliate).

### PASSO 4 — Nodi di trasporto e servizio per luogo (script `72_nodi_tp.py`)

1. **Corse per fermata e ora** dal GTFS `data/raw/gtt_gtfs_20261003_224530.zip`, giorno **2026-10-12**
   (stesso della v1): servizi attivi da `calendar.txt` + `calendar_dates.txt`; per ogni `stop_times` di una
   corsa attiva conta la partenza nell'ora `departure_time` (ore ≥ 24 → modulo 24). Somma per luogo (Passo 1).
2. Per ogni luogo:
   - `b2` = (somma partenze nelle ore 6,7,8,9,16,17,18,19) / 8 → corse/ora nelle **ore dei pendolari**;
   - `b_giorno` = (somma ore 6-20) / 15;
   - `b1_luogo` = somma di `corse_ora_punta` (v1) delle fermate del luogo;
   - `metro` = il luogo contiene una fermata servita dalla linea con `route_type` = 1 (M1);
   - `capolinea` = nelle ore 6-9 partono dal luogo (primo `stop_sequence` della corsa) almeno 4 corse/ora in
     media.
3. **Stazioni dei treni** da OSM (stesso PBF): nodi o vie con `railway=station` o
   (`public_transport=station` e `train=yes`); escludi `station=subway` e `subway=yes`. Salva nome e posizione.
   `ferro` = luogo entro 300 m da una stazione.
4. **Nodo forte** = luogo con `metro` o `ferro` o `capolinea` o `b2` ≥ 20.
5. Scrivi `data/processed/risultato6_v2/nodi.json` e `docs/RAPPORTO_R6V2_NODI.txt` (quanti luoghi per tipo di
   nodo; elenco stazioni trovate; controllo: Porta Nuova, Porta Susa, Lingotto, Stura, Rebaudengo devono
   esserci tra le stazioni; tutte le stazioni della metro, da Fermi a Bengasi, devono avere `metro`).

### PASSO 5 — Quanto ogni parcheggio fa da interscambio (in `72_nodi_tp.py`, seconda parte)

Per ogni parcheggio di `parcheggi.json` con tipo diverso da `privato`, `clienti`, `lungo_strada`:
1. **Posizione**:
   - `dist_nodo_forte_m` = distanza dal nodo forte più vicino; `tipo_nodo` (metro/ferro/capolinea/frequente);
   - `su_asse_ingresso` = il tratto stradale più vicino entro 150 m appartiene a un asse d'ingresso. Calcolalo
     qui con lo stesso metodo descritto al Passo 6, punto 2 (geometria dei tratti, `edge_tratta`, definizione di
     asse d'ingresso), e salva l'elenco degli assi d'ingresso in `nodi.json` perché il Passo 6 lo riusi;
   - `fuori_centro` = non nella zona IMQ Q001;
   - **posizione buona** = `dist_nodo_forte_m` ≤ 400 e `fuori_centro`.
2. **Uso** = firma dal Passo 3 (solo parcheggi 5T); per gli altri "sconosciuto".
3. **Condizioni** = posti (dichiarati o stimati), `a_pagamento`.
4. **Classe** (prima regola che vale):
   1. posizione buona e firma `pendolare` → `interscambio_di_fatto`;
   2. tipo `interscambio_ufficiale` (o `park_ride_osm`) e firma in {residenziale, destinazione, vuoto,
      dato_bloccato, misto} → `solo_sulla_carta` (con la firma accanto);
   3. posizione buona e uso sconosciuto/nessun_dato/dati_insufficienti → `potenziale`;
   4. altrimenti → `non_interscambio`.
5. Aggiungi le classi a un nuovo file `data/processed/risultato6_v2/parcheggi_funzione.json` (non riscrivere
   `parcheggi.json`) e scrivi `docs/RAPPORTO_R6V2_FUNZIONE.txt`: per ogni classe quanti parcheggi e quanti posti;
   tabella dei 5 ufficiali e dei garage 5T con posizione, firma, tariffa, classe; i 20 `potenziale` con più
   posti (dichiarati o stimati), con tariffa.
6. Atteso (provvisorio): Venchi Unica e Sofia `solo_sulla_carta`; Fermi `potenziale`; i grandi parcheggi
   gratuiti OSM vicino a Fermi `potenziale`. Non è un motivo di arresto se diverso: scrivilo.

### PASSO 6 — Segnali di criticità per luogo (script `73_segnali_criticita.py`)

Per ogni luogo del Passo 1 calcola tutti i segnali qui sotto (valore grezzo). I percentili si fanno al Passo 8.

1. **Vecchi (v1), portati sui luoghi:**
   - `a1` = massimo di `punteggio_corridoio` delle fermate del luogo;
   - `b1` = `b1_luogo` (Passo 4);
   - `c1` = `pendolari_raw` della zona del luogo (stessa formula della v1: copia la funzione
     `punteggio_pendolari_per_zona` dallo script 25 senza modificarla, o caricala con `importlib`).
2. **a2 — importanza della strada dal lavoro sul traffico (Fase 5):**
   - geometria dei tratti: `traffico_d/rete/rete_auto.npz` (`edge_pts`, `edge_off`: i punti del tratto `e` sono
     `edge_pts[edge_off[e]:edge_off[e+1]]`, ordine lat, lon); tratta di ogni tratto: `traffico_d/assi_tratte.npz`
     → `edge_tratta` (−1 = nessuna);
   - dati delle tratte: `traffico_d/tratte_traffico.json` → `tratte[]` (`id`, `asse`, `comune`, `punteggio`,
     `classe`, `rango`, `veic_giorno`);
   - **asse d'ingresso** = asse che ha tratte con `comune` = "Torino" **e** tratte con un altro comune;
   - per il luogo: tratto più vicino entro 150 m (distanza punto-segmento) → la sua tratta → `a2` =
     min(5, `punteggio` + 1 se asse d'ingresso); `asse_ingresso` = sì/no; se nessun tratto entro 150 m, `a2` =
     mancante.
3. **b2** = dal Passo 4 (corse/ora nelle ore dei pendolari).
4. **c2 — auto che entrano a Torino al mattino (IMQ 2022, microdati):**
   - file `data/processed/imq/spostamenti.csv` (separatore `;`, utf-8-sig; `PESO` con la virgola decimale →
     sostituisci "," con "."). Zone: `Q…` = quartieri di Torino; `C…` cintura, `E…` resto della Città
     metropolitana, `R…` resto del Piemonte (fuori Torino);
   - spostamento "auto in entrata al mattino" = `MEZZO1` in {03, 04, 21} (auto da conducente, da passeggero,
     car sharing), `COD_PAR` non vuoto e **non** `Q…`, `COD_ARR` che inizia con `Q`, `ORA_PAR` fra 06:00 e 09:59;
   - per ogni zona: somma dei `PESO` di questi spostamenti che **toccano** la zona (come origine o come
     destinazione), come fa la v1; `c2` del luogo = valore della sua zona;
   - salva anche le interviste (righe) per zona; zona con meno di 30 interviste → `c2_scarso` = sì;
   - **controllo:** totale = **~95.300 spostamenti** (1.139 interviste). Se diverso di oltre 2%: FERMO.
5. **c3 — ZTL centrale:** come c2, ma solo gli spostamenti con `COD_ARR` in una zona IMQ che ha almeno il 10%
   della superficie dentro la ZTL **centrale** (`ztl_unificata.json`, zona `"centrale"`, poligoni `[lon, lat]`;
   intersezione con shapely in coordinate proiettate) e `ORA_ARR` fra 07:30 e 10:30. `c3` per zona come c2.
   Variante di c2: `c2_ztl` = c2 + c3 (chi va nella ZTL al mattino conta doppio, perché deve lasciare l'auto
   prima). Scrivi nel rapporto quali zone superano il 10%.
6. **d — calo di velocità sugli ingressi (5T):** `velocita_5t.json` → `sensori[lcd1].celle["0"][ora]` con `v`
   (km/h) e `ok`. Per ogni sensore: `v_notte` = media di `v` alle ore 2, 3, 4 con `ok`; `v_punta` = media alle
   ore 7, 8 con `ok`; servono almeno 2 ore valide per ciascuna, altrimenti scarta. `calo` = 1 − v_punta/v_notte
   (si confronta lo **stesso punto con se stesso**: limiti e semafori non contano). Per il luogo: `d` = calo
   massimo fra i sensori entro 300 m; altrimenti mancante. Rapporto: elenco dei sensori usati con il calo.
7. **e — nodo ferro/metro:** `e` = 100 se il luogo ha `metro` o `ferro` (Passo 4), altrimenti 0.
8. **f — auto che già oggi lasciano l'auto per un mezzo pubblico (solo informazione):** spostamenti con
   `MEZZO1` in {03, 04, 05, 21} e un mezzo successivo (`MEZZO2` o `MEZZO3`) in {06, 07, 08, 09, 12, 13, 19, 22};
   totale atteso **~24.500 al giorno, 299 interviste** (63% verso il treno, ~4.000 verso la metro). Riporta il
   totale, la ripartizione per secondo mezzo e la zona del cambio (`COD_2M`; vuota nel ~60% dei casi).
   **Non entra nei punteggi** [DATI SCARSI].
9. Scrivi `data/processed/risultato6_v2/segnali.json` (per luogo: tutti i segnali grezzi, i flag e i
   "mancante") e `docs/RAPPORTO_R6V2_SEGNALI.txt` (per ogni segnale: quanti luoghi lo hanno, minimo, mediana,
   massimo, i 10 luoghi più alti).

### PASSO 7 — ISTAT 2011: proporzioni per completare l'IMQ (script `74_istat2011_auto_orari.py`)

Scopo: solo **proporzioni** stabili, per le zone IMQ con poche interviste. Mai numeri assoluti del 2011.

1. File `data/raw/istat/2011_sezioni/nazionale/matrix_pendo2011_10112014.txt` (~307 MB: leggilo **riga per
   riga**). Ogni riga, divisa sugli spazi, ha: tipo record (`L`/`S`), tipo residenza, provincia di residenza
   (3 cifre), comune di residenza (3 cifre), sesso, motivo (1 studio, 2 lavoro), luogo (1 stesso comune, 2 altro
   comune, 3 estero), provincia di destinazione, comune di destinazione, stato estero, **mezzo** (2 cifre),
   **orario di uscita** (1 cifra), durata (1 cifra), stima del numero di persone (decimale), numero di persone
   (o `ND`). Esempio: `L 1 001 001  1 1 1 001 001 000 04 2 1 0000005.00 ND`.
2. Codici attesi (standard ISTAT 2011, **da verificare** nel `leggimi file matrix_pendo2011_10112014.doc` se
   leggibile): mezzo 01 treno, 02 tram, 03 metropolitana, 04 autobus urbano/filobus, 05 corriera/extraurbano,
   06 aziendale/scolastico, **07 auto conducente**, **08 auto passeggero**, 09 moto, 10 bici, 11 altro, 12 a
   piedi; orario 1 prima delle 7:15, 2 7:15-8:14, 3 8:15-9:14, 4 dopo le 9:14.
   **Controllo:** per chi va dalla cintura a Torino per lavoro, il codice 07 deve essere il più frequente. Se
   no: FERMO (vuol dire codici o colonne sbagliati).
3. Prendi solo le righe `L`, destinazione Torino (provincia 001, comune 272), residenza in un comune della
   Città metropolitana (provincia 001) diverso da Torino. PRO_COM = provincia·1000 + comune.
4. Per ogni comune di residenza: `quota_auto` = (07+08)/totale; `quota_orari` = ripartizione su 1-4.
5. Collega i comuni alle zone IMQ con `data/processed/imq/comuni.csv` (`COD1_ISTAT` = PRO_COM, `COD2` = zona).
   Per zona: proporzioni pesate sulle persone.
6. **Completamento di c2** (solo zone con `c2_scarso`): `c2_completo` = (spostamenti IMQ di quella zona verso
   Torino nelle ore 6-10, **tutti i mezzi**) × `quota_auto` 2011 della zona. Le altre zone tengono c2. Segna le
   zone completate.
7. Scrivi `data/processed/risultato6_v2/istat2011_proporzioni.json` e `docs/RAPPORTO_R6V2_ISTAT2011.txt`
   (per zona: quota auto 2011, quota auto IMQ 2022 dove le interviste bastano, differenza; zone completate).
   Nel rapporto la frase: "Dal 2011 si usano solo proporzioni (quota di chi va in auto, orari), mai numeri".

### PASSO 8 — Tre scenari e copertura (script `75_risultato6_v2.py`)

1. Percentili: per ogni segnale, percentile 0-100 fra **tutti i luoghi** che lo hanno (funzione
   `percentile_rank` della v1). `e` resta 0/100 così com'è.
2. Punteggio di un luogo in uno scenario = media dei percentili dei segnali dello scenario **disponibili** per
   quel luogo (se `a2` o `d` mancano, la media è sugli altri; scrivi quanti luoghi hanno segnali mancanti).
3. **Scenari (massimo 3):**
   - **S1 "come la v1, per luoghi"**: a1, b1, c1.
   - **S2 "integrato"** (vecchi + nuovi): a1, a2, b1, b2, c1, c2_ztl (con `c2_completo` dove serve), d, e.
   - **S3 "solo nuovi"** (i nuovi al posto dei vecchi): a2, b2, c2_ztl (completato), d, e.
4. Critico = punteggio ≥ 90° percentile dei punteggi di tutti i luoghi **e** luogo non in Q001 (i luoghi del
   centro restano nel calcolo dei percentili, come nella v1).
5. **Controllo di riproducibilità (obbligatorio, prima di tutto il resto):** rifai S1 **per fermata** (non per
   luogo) con i valori della v1 → devono uscire **611** critiche, **17** coperte, **594** scoperte. Se no: FERMO.
6. **Copertura** di un luogo critico: c'è un parcheggio dell'insieme X entro R m dal centro del luogo. Insiemi:
   - **U** = i 5 interscambi ufficiali;
   - **F** = `interscambio_di_fatto` + `potenziale` (Passo 5);
   - **P** = tutti i parcheggi aperti (tipi `interscambio_ufficiale`, `garage_5t`, `park_ride_osm`,
     `osm_pubblico`) con almeno 50 posti (dichiarati o stimati).
   Raggi R = 100, **200** (base), 400 m. Calcola tutte le combinazioni scenario × insieme × raggio.
7. Confronto fra scenari: quanti luoghi critici in ciascuno, quanti in comune (S1∩S2, S1∩S3, S2∩S3), i 15
   luoghi che **entrano** e i 15 che **escono** passando da S1 a S2 e da S1 a S3 (con nome, zona, segnali).
8. Effetto dei singoli dati nuovi (sensibilità): ripeti S2 togliendo **un** segnale nuovo alla volta (a2, b2,
   c2_ztl, d, e), con c2 al posto di c2_ztl, e con `b_giorno` (media di tutta la giornata) al posto di b2:
   quanti luoghi critici cambiano. Così si vede quanto apporta ognuno.
9. Scrivi `data/processed/risultato6_v2/scenari.json` (per scenario: parametri, luoghi critici con punteggio e
   segnali, coperture per insieme e raggio) e `docs/RAPPORTO_RISULTATO6_V2.txt`: in testa una tabella breve
   (scenario → luoghi critici → coperti U/F/P a 200 m), poi i confronti, la sensibilità, i limiti (sezione 5).

### PASSO 9 — Verifiche indipendenti (script `76_verifiche_r6v2.py`)

Rifai con un metodo diverso, e scrivi in `docs/RAPPORTO_R6V2_VERIFICHE.txt`:
1. Numero di luoghi del Passo 1 con un raggruppamento fatto in modo diverso (es. scipy `cKDTree` +
   componenti connesse) → deve coincidere.
2. Per 5 luoghi a caso (seme 20261018): ricalcola a mano b2 dal GTFS e c2 dai microdati IMQ → uguali.
3. Firma di Porta Susa FS e Venchi Unica rifatta con pandas direttamente dal database → uguale.
4. Per 3 parcheggi OSM vicino a Fermi: superficie ricalcolata con shapely in EPSG:32632 → entro il 2%.
5. Copertura U a 200 m di S1 per fermata = 17 (come la v1).
6. `git status`: nessun commit; nessun file esistente modificato (elenca i file nuovi).

### PASSO 10 — Esito

Completa `docs/ESITO_RISULTATO6_V2.md`:
1. Righe di stato `PASSO 0..9: OK/FERMO`.
2. Le decisioni che hai preso tu (dove il piano lasciava una scelta) e perché.
3. Numeri chiave: luoghi; parcheggi per tipo e posti; firme dell'anteprima; classi di funzione; per ogni
   scenario luoghi critici e coperti (U/F/P, 100/200/400 m); sensibilità dei segnali nuovi; auto → mezzo
   pubblico (f).
4. Anomalie e limiti (sezione 5), e ogni differenza dagli "attesi" di questo piano.
5. Durate e file creati.
6. **Non** modificare memoria, schede, mappa. Il passo successivo (scegliere lo scenario, fissare le soglie
   delle firme, preparare la scheda) lo fa Claude con Leo.

---

## 4. Cosa NON fare

- Non scegliere lo scenario finale e non scrivere che uno "è migliore": li presenti, decide Leo.
- Non toccare la scheda (`schede_risultati.py`), la mappa, `simulazione.html`, la memoria.
- Non usare i numeri assoluti ISTAT 2011.
- Non abbinare fermate, strade o parcheggi per nome (eccezione: 5T↔Comune, nome **e** distanza < 150 m).
- Non scaricare niente da internet.
- Non aggiungere bici, bike/car sharing e taxi: verranno più avanti, quando si guarderà tutta la mobilità insieme.

## 5. Limiti da scrivere nel rapporto

- Riempimento: pochi giorni [DATI SCARSI]; 4 parcheggi non trasmettono; soglie delle firme provvisorie.
- Parcheggi OSM: elenco incompleto; posti stimati dalla superficie (~25 m² a posto) [STIMATO]; tariffa spesso
  ignota; nessun riempimento per i parcheggi gratuiti (es. attorno a Fermi).
- Pendolari IMQ: indagine campionaria, solo residenti 11-84 anni; zone con poche interviste completate con le
  proporzioni ISTAT 2011.
- Velocità: solo dove c'è un sensore 5T.
- Distanze in linea d'aria, non a piedi.
- Corse da orario programmato [PROGRAMMATO].
- Treni: le stazioni vengono da OSM; le frequenze dei treni non sono nei dati (il GTFS GTT non ha i treni).
