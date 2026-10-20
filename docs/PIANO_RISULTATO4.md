# Piano — Risultato 4: puntualità e attese dei mezzi GTT [MISURATO] (con dentro l'ex Risultato 9)

Piano unico del risultato. In testa stato, decisioni e lavori; sotto la storia del Risultato 4 (parte A) e il
piano dell'ex Risultato 9 (parte B, prima `docs/PIANO_RISULTATO9_ATTESA.md`). Aggiornato da Claude il 20/10/2026
dopo l'analisi di Leo. **Nessuna modifica fatta al risultato**: è un piano.

## Stato attuale

- **Ritardi e irregolarità** (v2, 18/10, script 27): feriale 5,3% dei passaggi in ritardo oltre 5 minuti, 10,5% di
  coppie a grappolo o con buco sulle linee frequenti; dati 10-18/10. Rapporto `docs/RAPPORTO_RISULTATO4.txt`.
- **Attesa reale** (ex R9, v1, 18/10, script 70 che riusa il 27): sulle linee frequenti l'attesa promessa è 4,8
  minuti, quella reale 5,4-6,2 (0,6-1,5 in più). Rapporto `docs/RAPPORTO_RISULTATO9_ATTESA.txt`.
- Oggi sono due schede separate (R4 e R9) in `simulazione.html`.
- Problema trovato il 20/10: in cima alle «10 linee peggiori per ritardo» ci sono servizi speciali con poche
  corse (RV2 2.226 passaggi, VEX 276, LS1 333, 68+ 1.612) davanti a linee vere come la 17 (21.483 passaggi).

## Commenti di Leo (20/10) e fattibilità

| Commento | Cosa c'è già | Lavoro |
|---|---|---|
| R4 è semplice e pulito | — | — |
| **Pulsante** dalle linee peggiori alla **mappa con quella linea selezionata** (per vedere che giro fa) | La mappa ha già il campo «Mostra solo una linea» (`#filtroLinea`) e si apre già da indirizzo per tema (`#tema=…`) | Piccolo: leggere `#linea=17` dall'indirizzo e riempire il filtro; nella scheda un link per ogni linea della classifica |
| **Ritardo per km** della linea (se la tratta è lunghissima) | Lunghezza delle linee calcolabile dal GTFS (percorsi `shapes` o somma delle distanze fra fermate) | Piccolo-medio: una colonna nella classifica; attenzione, il ritardo cresce lungo la corsa, quindi meglio «ritardo a fine corsa / km» o «ritardo medio per fermata» |
| Linee che passano da **zone affollate** | Abitanti per sezione e spostamenti per zona IMQ già pronti | Medio: si appoggia alla «popolarità» delle zone (misura comune, vedi `docs/PIANO_RISULTATO6.md`) |
| **Bus contro tram** (ritardi, irregolarità) | Il GTFS distingue tram e bus (tipo di linea); i dati del 27 sono per linea | Piccolo: due righe in più (tram / bus) in tutte le tabelle |
| Bus contro tram: **efficienza, efficacia, costo** (solo idea) | Dal rapporto GTT 2025: passeggeri per modo (bus urbani 183,7 M, tram 52,7 M), flotta (819 bus, 180 tram), vetture-km totali (non per modo). Costi per modo: **non ci sono** | Solo idea: passeggeri per vettura sì; costi no senza una fonte nuova (si lega a `docs/PIANO_COSTI.md`) |
| **Accorpare R9 a R4** | Stessi dati, il 70 riusa il 27 | Piccolo: una scheda con due parti |

## Decisioni di Leo (20/10)

1. **Una sola scheda «Puntualità e attese»** (numero 4) con due parti: ritardi e irregolarità; attesa reale contro
   promessa. R9 smette di esistere come numero a sé (gli script 27 e 70 restano).
2. Nelle classifiche **solo linee ordinarie con almeno 2.000 passaggi** (default); i servizi speciali in una riga a
   parte.
3. Tutte le aggiunte qui sopra vanno nel piano come lavori, nell'ordine della tabella che segue.

**Come eseguirli**: i lavori 1-2 sono nel **Giro 1** (`docs/PIANO_GIRO1_RITOCCHI.md`), con il prompt pronto.
Gli altri si preparano dopo, uno per volta, con un prompt nello stesso stile.

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Classifiche: solo linee ordinarie (≥ 2.000 passaggi; regola per riconoscere le speciali da fissare guardando l'elenco: lettere nel nome, poche corse) | 27, 70 | piccolo |
| 2 | Una scheda con due parti; toglierne una dall'elenco; testo inglese unico; nelle fonti della scheda il piano diventa `docs/PIANO_RISULTATO4.md` (oggi cita ancora `PIANO_RISULTATO9_ATTESA.md`, spostato in archivio) | `schede_risultati.py` | piccolo |
| 3 | Tram contro bus in ogni tabella | 27, 70 | piccolo |
| 4 | Link linea → mappa (`#linea=`) | `mappa_template.html`, scheda | piccolo |
| 5 | Ritardo per km (o a fine corsa) | 27 | piccolo-medio |
| 6 | Rilancio con un mese di dati (metà novembre): 27, poi 70, poi schede | `.bat` | — |
| 7 | R4 in mappa: linee colorate per ritardo, con lo slider dell'ora | 04, template | medio |
| 8 | Linee e zone affollate (dopo la «popolarità» delle zone) | — | medio |
| 9 | Controllo con la realtà: il rapporto GTT 2025 dichiara il 2,3% di passaggi bus/tram in ritardo oltre 10 minuti; noi misuriamo oltre 5 minuti: calcolare anche oltre 10 e confrontare | 27 | piccolo |
| — | Solo idea: efficienza e costo bus contro tram | — | serve una fonte sui costi |

---

# PARTE A — storia del Risultato 4


Scritto il 14/10/2026 per un agente. Esegui i passi **nell'ordine**, uno alla volta. Ogni passo ha un
controllo: se non torna, **FERMATI** e scrivi a Leo cosa hai visto. Non inventare correzioni.

## La domanda

1. **Puntualità**: quanti passaggi dei mezzi GTT alle fermate arrivano con **più di 5 minuti di
   ritardo**? Su quali linee e a che ora va peggio?
2. **Regolarità**: sulle linee frequenti, quante volte i mezzi arrivano **a grappolo** (due attaccati)
   o lasciano un **buco** (attesa molto più lunga del previsto)?

## Regole (valgono sempre)

- Ramo git `prova` (se non ci sei, fermati). **Non fare commit**: decide Leo.
- `python` del PATH (3.14), niente Anaconda. Solo libreria standard (niente pandas).
- `data/storico_backup.sqlite` **solo in lettura**: `sqlite3.connect("file:data/storico_backup.sqlite?mode=ro", uri=True)`.
- Non toccare `data/raw/`, la mappa (`mappa_torino.html`, `scripts/mappa_template.html`) e
  `scripts/04_genera_mappa.py`. Non lanciare `04_genera_mappa.py`.
- Non lanciare nulla che usi R5/Java: il PC sta facendo un altro calcolo lungo.
- Scrivi solo questi file: `scripts/27_risultato4_regolarita.py`,
  `data/processed/risultato4_regolarita.json`, `docs/RAPPORTO_RISULTATO4.txt`, e alla fine due righe
  in `MEMORIA_PROGETTO.md` (passo 7).

## Come sono fatti i dati (già verificato, non serve ricontrollarlo)

- **Ritardi**: tabella `trip_update_gtt` in `data/storico_backup.sqlite`, una lettura circa ogni minuto
  dal 10/10. Colonne: `letto_utc`, `trip_id`, `start_date` (AAAAMMGG, data locale della corsa),
  `start_time`, `payload` (JSON). Esempio di `payload`:
  ```json
  {"trip":{"trip_id":"28373194U","start_time":"10:39:00","start_date":"20261014","rel":0},
   "stu":[{"seq":55,"arr":{"delay":249},"rel":0}],"ts":1791971630,"id":"28373194U"}
  ```
  Ogni elemento di `stu` è una fermata della corsa (`seq` = `stop_sequence` del GTFS). Dentro `arr`
  c'è **o** `delay` (ritardo in secondi, ~70% dei casi) **o** `time` (orario previsto di arrivo, in
  secondi epoch UTC, ~30%). La stessa corsa compare in molte letture di fila: il bus avanza e le
  `seq` crescono.
- **Orario programmato**: `data/raw/gtt_gtfs_20261003_224530.zip`, file `trips.txt` (`trip_id`,
  `route_id`, `direction_id`), `routes.txt` (`route_id`, `route_short_name`), `stop_times.txt`
  (`trip_id`, `stop_sequence`, `arrival_time`, `stop_id`). `arrival_time` è `HH:MM:SS` in ora locale e
  può superare 24:00 (corse dopo mezzanotte).
- **Ora locale**: dal 10/10 al 24/10 l'Italia è a UTC+2. Per sicurezza copia le funzioni
  `ultima_domenica`, `offset_roma`, `a_roma` da `scripts/09_analisi_dati_diurni.py`.
- Tipo di giorno: 0 = feriale (lun-ven), 1 = sabato, 2 = domenica.

## Decisioni già prese (non cambiarle)

| # | Regola | Valore |
|---|---|---|
| D1 | Passaggio osservato | per ogni (`trip_id`, `start_date`, `seq`) si tiene **solo l'ultima lettura** (la `letto_utc` più recente) in cui quella `seq` compare: è la più vicina all'arrivo vero |
| D2 | Ritardo del passaggio | se c'è `arr.delay`: `delay/60` minuti. Se c'è `arr.time`: `(time - orario_programmato)/60`, con orario programmato = mezzanotte locale di `start_date` + `arrival_time` del GTFS, convertito in UTC |
| D3 | Lettura affidabile | si scarta il passaggio se l'ultima lettura è lontana dall'arrivo stimato più di **10 minuti** (cioè \|arrivo stimato − letto_utc\| > 10 min) o se la corsa/seq non è nel GTFS. Conta e riporta quanti scarti |
| D4 | Classi di puntualità | **anticipo** se ritardo < −1 min; **puntuale** se −1 … +5 min; **in ritardo** se > +5 min |
| D5 | Arrivo stimato | orario programmato + ritardo (serve per la regolarità e per D3) |
| D6 | Linee frequenti | per la regolarità si considerano solo coppie con intervallo **programmato ≤ 15 minuti** |
| D7 | Classi di regolarità | per due passaggi consecutivi alla stessa fermata (stessa linea, stessa direzione, stesso giorno): **grappolo** se intervallo osservato < 0,5 × programmato; **buco** se > 2 × programmato; altrimenti **regolare** |
| D8 | Dati sufficienti | una linea entra nelle classifiche solo con **≥ 200 passaggi** osservati nel tipo di giorno (puntualità) e **≥ 100 coppie** (regolarità) |
| D9 | Fasce orarie | punta mattina 7-9, giorno 9-16, punta sera 16-19, sera 19-24, notte 0-7 (ora locale dell'arrivo programmato) |

## Passo 1 — Controllo di partenza

Lancia:
```
python -c "import sqlite3;c=sqlite3.connect('file:data/storico_backup.sqlite?mode=ro',uri=True);print(c.execute('select count(*),min(letto_utc),max(letto_utc),count(distinct start_date) from trip_update_gtt').fetchone())"
```
Atteso: circa 1 milione di righe, dal `2026-10-10` al `2026-10-14`. Annota il risultato.

## Passo 2 — Scrivere `scripts/27_risultato4_regolarita.py`

Struttura dello script (docstring in italiano che riassume domanda, decisioni D1-D9, input e output):

1. **Carica il GTFS** (una volta sola, dal file zip):
   - `trips.txt` → `trip_info[trip_id] = (route_id, direction_id)`;
   - `routes.txt` → `nome_linea[route_id] = route_short_name`;
   - `stop_times.txt` → `prog[(trip_id, stop_sequence)] = (secondi_da_mezzanotte, stop_id)`, dove
     `secondi = h*3600 + m*60 + s` (h può essere ≥ 24).
2. **Un giorno alla volta** (il PC ha poca memoria libera: NON caricare tutti i giorni insieme).
   Prendi l'elenco dei giorni con `SELECT DISTINCT start_date FROM trip_update_gtt ORDER BY 1` e, per
   ogni giorno, leggi solo le sue righe (`SELECT letto_utc, trip_id, payload FROM trip_update_gtt
   WHERE start_date = ? ORDER BY letto_utc`). Per ogni elemento di `stu` aggiorna un dizionario
   `ultimo[(trip_id, seq)] = (letto_utc, arr)`. Siccome le righe sono in ordine di tempo, alla fine
   resta l'ultima lettura (D1). Fai i punti 3 e 5 per quel giorno, conserva solo i numeri che servono
   ai totali (ritardi in minuti in liste per chiave, conteggi delle coppie), poi **svuota** `ultimo`
   e i passaggi del giorno prima di passare al successivo.
3. **Costruisce i passaggi** del giorno: per ogni chiave di `ultimo`:
   - se `(trip_id, seq)` non è in `prog` o `trip_id` non è in `trip_info` → scarto "fuori GTFS";
   - orario programmato UTC = mezzanotte locale di `start_date` + secondi, meno l'offset (UTC+2);
   - ritardo in minuti come D2; arrivo stimato come D5;
   - se \|arrivo stimato − letto_utc\| > 10 min → scarto "lettura lontana" (D3);
   - altrimenti salva il passaggio: linea (nome), direzione, stop_id, trip_id, start_date, tipo di
     giorno, fascia oraria (D9), orario programmato, arrivo stimato, ritardo, classe (D4).
4. **Puntualità**: per città e per (linea × tipo di giorno) e per (linea × tipo di giorno × fascia):
   numero di passaggi, % anticipo, % puntuale, % in ritardo, ritardo mediano e 90° percentile.
5. **Regolarità**: raggruppa i passaggi per (linea, direzione, stop_id, start_date). In ogni gruppo
   ordina per **orario programmato**; per ogni coppia di passaggi consecutivi calcola intervallo
   programmato e intervallo osservato (differenza degli arrivi stimati, in minuti). Tieni solo le
   coppie con programmato ≤ 15 min (D6) e classificale (D7). Per città e per (linea × tipo di
   giorno): numero di coppie, % grappolo, % buco, % regolare.
6. **Output JSON** `data/processed/risultato4_regolarita.json` (compatto, `ensure_ascii=False`):
   ```json
   {"generato":"...","tag":"MISURATO","periodo":{"da":"...","a":"..."},
    "giorni":{"0":3,"1":1,"2":1},"parametri":{"soglia_ritardo_min":5,"soglia_anticipo_min":-1,
    "max_lettura_lontana_min":10,"freq_max_min":15,"min_passaggi":200,"min_coppie":100},
    "scarti":{"fuori_gtfs":0,"lettura_lontana":0,"usati":0},
    "citta":{"0":{"passaggi":0,"anticipo":0.0,"puntuale":0.0,"ritardo":0.0,"mediana":0.0,"p90":0.0,
                  "coppie":0,"grappolo":0.0,"buco":0.0,"regolare":0.0}},
    "linee":{"<nome>":{"0":{...stessi campi...,"fasce":{"punta_mattina":{...}}}}}}
   ```
   Percentuali con una cifra decimale. I tipi di giorno senza dati non si scrivono.
7. **Rapporto** `docs/RAPPORTO_RISULTATO4.txt`, in quest'ordine:
   - periodo, giorni per tipo, passaggi usati e scarti (numeri e %);
   - **I 3 NUMERI** (feriale): % passaggi in ritardo > 5 min; % coppie a grappolo + % a buco sulle
     linee frequenti; ritardo mediano;
   - puntualità città per tipo di giorno e per fascia oraria (feriale);
   - **10 linee peggiori per % in ritardo** (feriale, solo con ≥ 200 passaggi);
   - **10 linee peggiori per % grappolo + buco** (feriale, solo con ≥ 100 coppie);
   - avviso finale: "[MISURATO] dal feed GTFS-Realtime GTT; il ritardo è quello stimato dal sistema
     GTT alla fermata nell'ultima lettura prima dell'arrivo; sabato e domenica con 1 solo giorno:
     [DATI SCARSI]."
8. Opzione `--prova`: usa solo `start_date = 20261013` e scrive il rapporto **solo a schermo** (non
   scrive i file).

## Passo 3 — Prova

`python scripts\27_risultato4_regolarita.py --prova`

Controlli (scrivi l'esito di ognuno). Riferimento: Claude ha provato le regole su 13/10 dalle 7 alle
10 e ha ottenuto ~9% fuori GTFS, ~3% letture lontane, mediana −0,4 min, 90° percentile 3,6 min,
5,5% in ritardo > 5 min. Sul giorno intero i numeri saranno simili, non identici.
- gira senza errori in pochi minuti;
- scarti "fuori GTFS" sotto il 25% (il GTFS è del 3/10, qualche corsa può mancare);
- ritardo mediano della città tra −1 e +3 minuti;
- % in ritardo > 5 min tra l'1% e il 30%;
- se uno di questi non torna: **FERMATI** e scrivi a Leo.

## Passo 4 — Giro completo

1. Controlla la memoria libera:
   `powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1KB)"`
   (numero in MB). Se è **sotto 800**, non lanciare il giro: fermati e scrivi a Leo che conviene
   aspettare la fine del calcolo di accessibilità (domattina).
2. `python scripts\27_risultato4_regolarita.py` (senza `--prova`). Controlla che abbia scritto i due
   file e annota quanto tempo ci ha messo.

## Passo 5 — Controlli indipendenti (obbligatori)

1. **Due passaggi a mano**: prendi 2 passaggi dal JSON/rapporto (uno con `arr.delay`, uno con
   `arr.time`). Per ciascuno, con una query SQL diretta trova l'ultima riga di `trip_update_gtt` di
   quella corsa e data in cui compare quella `seq`, leggi `arr` e ricalcola il ritardo a mano con
   l'orario del GTFS. Deve coincidere.
2. **Le due fonti si somigliano**: calcola il ritardo mediano separatamente per i passaggi con
   `delay` e per quelli con `time`. Devono essere simili (differenza sotto i 2 minuti); se no, dillo.
3. **Il ritardo cresce lungo la corsa**: ritardo mediano dei passaggi con `seq` ≤ 5 contro `seq` ≥ 30.
   Di solito il secondo è più alto.
4. **Le ore di punta vanno peggio**: % in ritardo feriale in punta (7-9, 16-19) contro notte (0-7).
5. **Una coppia a grappolo a mano**: prendi una coppia classificata "grappolo", riporta i due
   orari programmati e i due arrivi stimati e verifica la regola D7.
6. Somme: per la città, anticipo + puntuale + ritardo = 100% (±0,1); grappolo + buco + regolare = 100%.

## Passo 6 — Consegna a Leo (poi Claude ricontrolla)

Scrivi a Leo, in parole semplici e corte:
- i **3 numeri** (feriale);
- le 5 linee peggiori per ritardo e le 5 peggiori per irregolarità;
- l'esito di ognuno dei controlli del passo 5;
- scarti e limiti (giorni pochi, sabato/domenica scarsi);
- i file creati.

## Passo 7 — Memoria

In `MEMORIA_PROGETTO.md`: nella tabella della **sezione 4 (FATTO)** aggiungi una riga "Risultato 4
v1 (27)" con i 3 numeri; nella **sezione 6** aggiorna il punto del Risultato 4 con "fatto, da
controllare da Claude; resta la mappa". Non aggiungere sezioni, non toccare il resto.

## Dopo (NON in questo giro)

Mappa (colorare le linee per % in ritardo / irregolarità con lo slider dell'ora, come la velocità
commerciale già presente) e pagina in `simulazione.html`: piano a parte, dopo la rigenerazione della
mappa. Rilanciare lo script quando ci saranno più sabati e domeniche.

## Stato al 18/10/2026 (spostato qui dalla memoria)

- **Versione 2** [MISURATO], 10-18/10 (5 feriali, 2 sabati, 2 domeniche; giorni parziali 10, 12, 13, 18/10
  contati con le ore che hanno dati — scelta di Leo), 1.280.961 passaggi.
  **Feriale: 5,3% in ritardo > 5 min · 10,5% grappolo+buco · ritardo mediano −0,4 min · 39,9% in anticipo.**
  Sale rispetto alla v1 (4,2%) perché giovedì 15 e venerdì 16 sono andati peggio (ricontrollo indipendente
  giorno per giorno: stessa tendenza). La v1 aveva giorni a metà (il 12/10 solo pomeriggio); è conservata in
  `data/processed/risultato4_regolarita_v1.json` e `docs/archivio/RAPPORTO_RISULTATO4_v1.txt`. Scheda in `simulazione.html`.
- **Copertura del feed ritardi** (`trip_update_gtt`, dal 10/10, una lettura al minuto; verificata 18/10):
  `delay` di corsa mai presente; per ogni fermata `stop_time_update.arr` ha `delay` in secondi (~70%) o l'arrivo
  previsto `time` (~30%, da confrontare con l'orario GTFS). Raccolta 05-24 locali (niente notte); solo ~90 linee
  urbane, 108 linee mai presenti (extraurbane a 4 cifre, alcune notturne; 3.540 corse/giorno); sulle linee coperte
  c'è ~80% delle corse programmate (GPS `mezzi_gtt` 77%, almeno uno dei due 82%). Corse mancanti = saltate o non
  trasmesse, non distinguibili: il risultato misura solo le corse presenti nel feed.
- Il 18/10 il feed GTT (`percorsieorari.gtt.to.it`) non ha risposto dalle ~09:05: buco nei dati di quel giorno.


---

# PARTE B — ex Risultato 9: attesa promessa contro attesa reale [MISURATO]

> **Stato (20/10/2026): versione 1 fatta il 18/10, scheda in `simulazione.html`** (numeri nella sezione 9).
> Prossimo: rilancio con un mese di dati (metà novembre).

Scritto da Claude il 18/10/2026, da approvare con Leo prima di costruire (sezione 6: decisioni aperte).
Riparte dai dati e dallo script del Risultato 4 (`scripts/27_risultato4_regolarita.py`, `docs/PIANO_RISULTATO4.md`).

### 1. La domanda (in parole semplici)

Alla fermata l'orario promette, per esempio, un bus ogni 8 minuti: chi arriva a caso aspetta in media 4 minuti.
Se però i bus arrivano a coppie (grappolo) e poi lasciano un buco, l'attesa vera è più lunga, anche se il numero
di bus nell'ora è lo stesso. **Quanti minuti in più aspetta, in media, chi prende un bus o tram frequente a Torino?
Su quali linee, fermate e ore va peggio?**

Perché è rilevante: è la misura che usano le grandi aziende di trasporto per la regolarità delle linee frequenti
(Londra la pubblica come "Excess Wait Time"). Traduce il risultato 4 (percentuali di grappoli e buchi) in una cosa
che tutti capiscono: minuti persi alla fermata. Si calcola con dati che solo questo progetto raccoglie (feed GTT
salvato ogni minuto sul Raspberry Pi).

### 2. La formula (una sola, spiegata)

Per una fermata, una linea, un verso e una fascia oraria, con gli intervalli fra un passaggio e il successivo
h1, h2, ..., hn (in minuti):

- **attesa media** di chi arriva a caso = (h1² + h2² + ... + hn²) / (2 × (h1 + h2 + ... + hn))
- **attesa promessa** = la stessa formula con gli intervalli dell'orario ufficiale (GTFS)
- **attesa reale** = la stessa formula con gli intervalli osservati (arrivi stimati dal feed, come nel risultato 4)
- **attesa in più** = attesa reale − attesa promessa

Esempio: bus esattamente ogni 10 minuti → (10²+10²)/(2×20) = 5 minuti. Stessi 2 bus all'ora ma a coppie, con
intervalli 2 e 18 → (4+324)/(2×20) = 8,2 minuti. Stessa offerta, 3,2 minuti in più di attesa.

La formula vale per le linee **frequenti** (chi va alla fermata non guarda l'orario). Per le linee rare conta la
puntualità, che è già nel risultato 4.

### 3. Cosa sappiamo già dei dati (verificato da Claude il 18/10 sul backup del 18/10)

1. **Feed dei ritardi** (`trip_update_gtt`): dal 10/10, una lettura al minuto. Le giornate complete (06-24) sono
   11, 14, 15, 16 e 17/10; il 10, 12, 13 e 18/10 sono parziali (il 18 per un guasto del feed GTT dalle ~09:05).
   La raccolta si ferma ogni notte a mezzanotte locale e riparte verso le 5: la notte non è misurabile.
2. **Il feed copre solo le linee urbane.** Il 15/10: 90 linee con dati, **108 linee mai presenti** (3.540 corse
   al giorno: numeri a 4 cifre, cioè extraurbane, e alcune notturne). Il risultato vale solo per le linee coperte.
3. **Anche sulle linee coperte manca circa 1 corsa su 5.** Il 15/10, su 9.624 corse programmate delle 90 linee:
   80,1% nel feed dei ritardi, 77,1% nelle posizioni GPS (`mezzi_gtt`), 82,2% in almeno uno dei due. Le linee
   frequenti sono coperte meglio (linea 4: 369 su 380; linea 10: 251 su 260), ma per esempio la linea 2 ha 194 su 243.
   **Una corsa che manca può essere saltata davvero oppure non trasmessa: dai dati non si distingue.** Questo è il
   punto più delicato del metodo (sezione 4, punto 3, e decisione D1).
4. L'arrivo "osservato" è l'arrivo **stimato dal feed** nell'ultima lettura entro 10 minuti dal passaggio (regola
   D1-D5 del risultato 4), non un arrivo visto sul posto.

### 4. Metodo proposto (passi, ognuno con un controllo)

**Passo 1 — Linee e fasce.** Linee frequenti = intervallo programmato ≤ 12 minuti (almeno 5 passaggi all'ora) in
quella fascia, fermata e verso (D2). Fasce come nel risultato 4 (punta mattina 7-9, giorno 9-16, punta sera 16-19,
sera 19-24), più tipo di giorno. Solo le ore in cui la raccolta era attiva (almeno 50 minuti letti nell'ora).
*Controllo:* elenco delle linee frequenti con numero di fermate e passaggi programmati; confronto con le linee
frequenti già usate nel risultato 4.

**Passo 2 — Intervalli promessi e osservati.** Per ogni fermata-linea-verso-giorno si mettono in fila le corse
programmate e i loro arrivi stimati (dallo script 27, stessa lettura dei dati). *Controllo:* per 3 fermate
scelte a mano (una della linea 4, una della 15, una della 68) stampare la fila di orari promessi e stimati e rifare a
mano l'attesa promessa e reale.

**Passo 3 — Corse mancanti: una forbice, non un numero solo (D1).**
- *Stima bassa:* una corsa assente nel feed è considerata "non vista": l'intervallo si calcola solo tra corse
  consecutive entrambe osservate (si scartano i pezzi con buchi). Sottostima l'attesa se le corse mancanti erano
  saltate davvero.
- *Stima alta:* una corsa assente sia dal feed dei ritardi sia dal GPS mentre la raccolta era attiva è considerata
  **non effettuata**: l'intervallo reale salta da un bus all'altro. Sovrastima l'attesa se la corsa c'era ma non
  trasmetteva.
- Si pubblicano entrambe, con il numero principale = la stima bassa (prudente) e la forbice accanto.
*Controllo:* quota di corse mancanti per linea e fascia; se una linea ne ha più del 20% in una fascia, quella
fascia va in tabella "dati scarsi" e non entra nei numeri di testa.

**Passo 4 — Prova con il GPS (controllo indipendente del feed).** Su 2 linee frequenti (4 e 15) e circa 20
fermate, confrontare l'arrivo stimato dal feed con il momento in cui il GPS del mezzo (`mezzi_gtt`, posizione ogni
minuto) passa più vicino alla fermata. Se la differenza mediana supera 1 minuto, fermarsi e decidere con Leo.

**Passo 5 — Numeri.** Per linea-verso-fascia-tipo di giorno: attesa promessa, attesa reale (bassa e alta),
attesa in più in minuti e in %, numero di intervalli. Città: media pesata sul numero di passaggi programmati (non
abbiamo i passeggeri; D3). Classifiche: le 10 linee e le 20 fermate con più attesa in più (con almeno 30 intervalli).

**Passo 6 — Scheda in `simulazione.html`** (stesso formato delle altre, `scripts/schede_risultati.py`): numero
chiave, grafico per fascia oraria, classifica delle linee, prima/dopo "attesa promessa → attesa reale".
La mappa per fermate solo se Leo la vuole, dopo.

### 5. Uscite

`scripts/<numero libero>_risultato9_attesa.py` (il numero si sceglie quando l'agente della Fase 5 ha finito, per
non scontrarsi con i suoi 56+), `data/processed/risultato9_attesa.json`, `docs/RAPPORTO_RISULTATO9_ATTESA.txt`,
scheda nella pagina dei risultati. Calcolo leggero (come lo script 27: ~500 MB di memoria, pochi minuti).

### 6. Decisioni aperte (da chiedere a Leo, con il default proposto)

| # | Domanda | Default proposto |
|---|---|---|
| D1 | Corse mancanti | Forbice bassa/alta, numero principale = stima bassa |
| D2 | Cosa vuol dire "frequente" | ≤ 12 minuti di intervallo programmato (sensibilità: 10 e 15) |
| D3 | Peso per la media della città | Passaggi programmati (niente dati sui passeggeri) |
| D4 | Numero del risultato | Risultato 9 |
| D5 | Chi lo esegue | Claude, in questa cartella, dopo l'approvazione del piano |

### 7. Limiti da dichiarare già ora

- Arrivi stimati dal feed GTT, non osservati sul posto (verificati a campione col GPS, passo 4).
- Solo linee urbane presenti nel feed; niente extraurbane, niente notte.
- Corse mancanti: risultato dato come forbice.
- Chi arriva alla fermata "a caso": vero per le linee frequenti, non per chi guarda l'orario o l'app.
- Pochi giorni (vedi sezione 3): il risultato va rifatto quando ci sono più settimane di dati.

### 8. Effetto sul risultato 4 (scoperto preparando questo piano)

Anche il risultato 4 misura solo le corse presenti nel feed: se le corse mancanti sono in parte saltate davvero, la
puntualità reale è peggiore di quella misurata e i "buchi" sono sottostimati (una corsa saltata non crea un buco
nel conteggio, perché la coppia si calcola fra corse osservate). Va scritto fra i limiti del risultato 4.

### 9. Stato al 18/10/2026 (spostato qui dalla memoria)

**Versione 1** [MISURATO], 10-18/10, linee urbane frequenti (≤ 12 min), ore con raccolta attiva.
Feriale: attesa promessa 4,8 min, reale 5,4-6,2 → **0,6-1,5 min in più** (+13% stima bassa); sabato +0,8-1,4;
domenica troppo pochi dati. Peggiori: linea 68 (+1,3-3,0), 3, 56, 46, 62; fermate della 18 (Caio Mario,
Lingotto) e della 62. Controlli: GPS linee 4 e 15 (343 passaggi, scarto tipico 0,45 min, 70% entro 1 min); una
chiave rifatta da zero coincide (2,555 / 3,668 min). Lo script 70 riusa il 27 senza modificarlo. Scheda in
`simulazione.html`. Da rilanciare con più settimane di dati (27, poi 70, poi `schede_risultati.py`).
