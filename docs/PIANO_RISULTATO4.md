# Piano — Risultato 4: bus in ritardo e bus irregolari [MISURATO]

> **Stato (20/10/2026): versione 2 fatta il 18/10, scheda in `simulazione.html`.** Numeri e copertura dei dati
> nella sezione «Stato al 18/10/2026» in fondo. Prossimo: rilancio con un mese di dati (metà novembre).

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
