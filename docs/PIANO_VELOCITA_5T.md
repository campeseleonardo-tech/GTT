# Piano — Velocità reale misurata dai sensori 5T (passo 4)

Scritto il 14/10/2026 per un agente. Da eseguire un passo alla volta, nell'ordine, senza saltare i
controlli. Se un controllo non torna: FERMATI e scrivi a Leo cosa hai visto (non inventare correzioni).

## Scopo

Oggi la mappa colora i sensori 5T solo con il dato **di adesso** (ultimi 5-15 minuti) e confronta
con un "valore tipico" calcolato sul Pi (`06_dati_live.py` → `data/stat.js`, campo `tipico`) che
**non scarta le letture inaffidabili** (accuratezza 0). Obiettivo di questo passo:

1. rifare il rapporto sulla qualità dei dati 5T su **tutti** i giorni raccolti (oggi è fermo ai
   primi 5 giorni, 4-8/10);
2. produrre un nuovo file `data/processed/velocita_5t.json`: per ogni sensore, velocità e flusso
   **tipici** per tipo di giorno × ora locale, usando **solo letture affidabili** [MISURATO];
3. (DOPO, non in questo giro) usarlo in mappa con lo slider dell'ora, come già si fa per la
   velocità commerciale dei bus.

## Regole (valgono per tutto il piano)

- Ramo git `prova`. Se non sei su `prova`, fermati. **Non fare commit**: decide Leo.
- Python del PATH (3.14): comando `python`. NON Anaconda.
- **Sola lettura** su `data/storico_backup.sqlite` (aprilo sempre con
  `sqlite3.connect("file:...?mode=ro", uri=True)`). Non toccare `data/raw/` né lo storico.
- **NON lanciare `scripts/04_genera_mappa.py`** e non toccare `mappa_torino.html` /
  `scripts/mappa_template.html`: è in corso il calcolo di accessibilità a 24 ore e
  `data/processed/accessibilita.json` oggi contiene solo una prova di 30 sezioni.
- Non lanciare nulla che usi R5/Java: il PC sta già facendo il calcolo di accessibilità.
- Solo libreria standard di Python (niente pandas).
- Ore locali: Europe/Rome calcolata a mano, **copiando** le funzioni `ultima_domenica`,
  `offset_roma`, `a_roma` da `scripts/09_analisi_dati_diurni.py` (niente `zoneinfo`).
- Tipo di giorno come nel resto del progetto: 0 = feriale (lun-ven), 1 = sabato, 2 = domenica.

## Decisioni già prese (valori predefiniti, non cambiarli)

| # | Decisione | Valore |
|---|---|---|
| D1 | Letture usate | solo quelle con riga in `accuratezza_5t` e `accuratezza > 0` (la tabella esiste dal 08/10 21:30 UTC: le letture prima non hanno accuratezza e si **escludono**) |
| D2 | Velocità tipica di una cella | media della velocità **pesata per il flusso** (Σ velocità×flusso / Σ flusso), solo letture con flusso > 0 — stesso metodo di `stat.js`, così si possono confrontare |
| D3 | Flusso tipico | media del flusso (veicoli/ora) su tutte le letture affidabili della cella, zeri compresi |
| D4 | Cella valida | almeno **2 giorni distinti** e almeno **6 letture** con flusso > 0; altrimenti la cella si scrive ma con `"ok": false` |
| D5 | Sensori | tutti i 109; campo `"urbano": true` se il nome strada contiene `(TO)` (sono 31) |

## Passo 1 — Copia aggiornata dello storico (lo fa Leo)

1. Chiedi a Leo di fare doppio clic su `scripts\backup_da_leopi.bat` e di dirti quando ha finito.
2. Controllo (lancialo tu):
   ```
   python -c "import sqlite3;c=sqlite3.connect('file:data/storico_backup.sqlite?mode=ro',uri=True);print(c.execute('select min(generato_utc),max(generato_utc),count(distinct generato_utc) from flussi_5t').fetchone());print(c.execute('select min(generato_utc),count(*) from accuratezza_5t').fetchone())"
   ```
   Atteso: la data massima della prima riga è **14/10 o successiva**; la seconda riga parte dal
   `2026-10-08T21:30`. Se la data massima è ancora `2026-10-11`, il backup non è stato aggiornato:
   fermati e dillo a Leo.

## Passo 2 — Rifare il rapporto di qualità 5T

1. Lancia: `python scripts\09_analisi_dati_diurni.py`
2. Non modificare lo script 09.
3. Controlli in `docs/RAPPORTO_ANALISI_5T.txt`:
   - prima riga: `DB (sola lettura): ...storico_backup.sqlite` (NON `storico.sqlite`);
   - `controllo conteggio flussi_5t: ... OK`;
   - `intervallo UTC` che arriva almeno al 13/10;
   - sezione "Copertura per giorno locale": un giorno per riga dal 04/10 in poi; annota i giorni
     con copertura sotto l'80% (es. il 13/10 sera ci fu uno spegnimento del Pi).
4. Annota in 3 righe: giorni coperti, giorni sotto l'80%, quanti feriali/sabati/domeniche.

## Passo 3 — Nuovo script `scripts/26_velocita_5t.py`

Scrivi lo script con questa struttura (docstring in italiano, stile degli altri script):

1. Costanti: `RADICE` (cartella `GTT`, come in 09), `DB = RADICE/"data"/"storico_backup.sqlite"`,
   `OUT = RADICE/"data"/"processed"/"velocita_5t.json"`,
   `RAPPORTO = RADICE/"docs"/"RAPPORTO_VELOCITA_5T.txt"`, `MIN_GIORNI = 2`, `MIN_LETTURE = 6`.
2. Argomento `--prova`: usa solo le letture dei primi 2 giorni locali dopo il 08/10 21:30 UTC.
3. Lettura (una sola query, in sola lettura):
   ```sql
   SELECT f.generato_utc, f.lcd1, f.flusso, f.velocita
   FROM flussi_5t f
   JOIN accuratezza_5t a ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
   WHERE a.accuratezza > 0 AND f.flusso IS NOT NULL
   ```
   e l'anagrafica: `SELECT lcd1, nome_strada, direzione, lat, lng FROM sensori_5t`.
4. Per ogni lettura: ora locale con `a_roma(...)`, `tipo` (0/1/2), `ora` (0-23), `giorno` (data
   locale). Accumula per (sensore, tipo, ora): Σ flusso, n letture, Σ velocità×flusso e Σ flusso
   solo per flusso > 0, n letture con flusso > 0, insieme dei giorni.
5. Per ogni cella: `v` = Σ(v×f)/Σf (arrotondata a 0,1; `null` se nessuna lettura con flusso > 0),
   `f` = Σflusso/n (arrotondato all'intero), `n` = letture, `g` = giorni distinti,
   `ok` = (g ≥ MIN_GIORNI e letture con flusso > 0 ≥ MIN_LETTURE).
6. Output JSON (compatto, `ensure_ascii=False`):
   ```json
   {"generato": "...", "fonte": "storico_backup.sqlite, solo letture con accuratezza>0",
    "tag": "MISURATO", "periodo": {"da": "...", "a": "..."}, "giorni": {"0": 4, "1": 1, "2": 1},
    "parametri": {"min_giorni": 2, "min_letture": 6},
    "sensori": {"<lcd1>": {"via": "...", "dir": "...", "lat": 45.1, "lon": 7.6, "urbano": true,
                "celle": {"0": {"7": {"v": 23.4, "f": 812, "n": 57, "g": 4, "ok": true}}}}}}
   ```
   Le chiavi di tipo e ora sono stringhe. Le celle senza letture non si scrivono.
7. Rapporto `docs/RAPPORTO_VELOCITA_5T.txt` con:
   - periodo, letture lette, letture scartate per accuratezza (contale con una query a parte:
     letture con accuratezza = 0), giorni per tipo;
   - sensori con almeno una cella `ok` (totale e urbani);
   - per i **10 sensori urbani** con più celle `ok`: via, direzione, velocità feriale alle 8, alle
     13, alle 18 e alle 3 (o `-` se la cella non è ok);
   - le 10 celle feriali urbane più lente (con `ok`), con via, ora e velocità.
8. Prima `python scripts\26_velocita_5t.py --prova`, controlla che giri senza errori e che il
   rapporto abbia senso; poi il giro vero `python scripts\26_velocita_5t.py`.

## Passo 4 — Controlli indipendenti (obbligatori, prima di dire "fatto")

1. **Ricalcolo a mano**: scegli 3 sensori urbani e per ciascuno 2 celle `ok` (es. feriale 8 e
   feriale 3). Per ognuna scrivi una query SQL diretta sullo storico con gli stessi filtri
   (attenzione all'ora locale: costruisci l'intervallo UTC di quell'ora per ogni giorno) e
   confronta `v` ed `f` con il JSON. Devono coincidere (differenze solo di arrotondamento).
2. **Confronto con `stat.js`**: il file `data/stat.js` (copiato dal Pi da `sync_da_leopi.bat`) ha
   `STAT.tipico[lcd1][tipo*24+ora] = [velocità, flusso/ora, ore]`. Per gli stessi 6 casi riporta
   i due valori affiancati. Ci si aspetta lo **stesso ordine di grandezza**; differenze grandi
   sono possibili solo dove il sensore ha molte letture con accuratezza 0 (dillo, con il numero).
3. **Buon senso** (scrivi l'esito di ognuno):
   - nessuna velocità < 0 o > 130 km/h; nessun flusso negativo;
   - sui corsi urbani la velocità alle 3 di notte è in genere **più alta** che alle 8 o alle 18;
   - il flusso alle 3 è in genere **molto più basso** che alle 8;
   - numero di celle `ok` per tipo: le domeniche/sabati ne hanno meno dei feriali (meno giorni).
4. Se un controllo non torna, non correggere a caso: fermati e descrivi il caso a Leo.

## Passo 5 — Consegna a Leo (poi Claude ricontrolla)

Scrivi a Leo, in parole semplici:
- giorni usati (per tipo) e quante letture scartate per accuratezza (%);
- quanti sensori hanno dati affidabili (totale e urbani);
- 3 esempi concreti (via, ora, velocità tipica) e le 3 celle più lente;
- l'esito di ogni controllo del passo 4;
- i file creati/modificati: `scripts/26_velocita_5t.py`, `data/processed/velocita_5t.json`,
  `docs/RAPPORTO_VELOCITA_5T.txt`, `docs/RAPPORTO_ANALISI_5T.txt`, `data/processed/analisi_5t.json`.

Aggiorna `MEMORIA_PROGETTO.md` solo nella sezione 4 (riga nuova "Velocità 5T tipica") e nella
sezione 6 (punto 3: cosa resta). Non aggiungere sezioni.

## Dopo (NON in questo giro): la mappa

Solo quando (a) Leo ha visto i numeri e (b) il calcolo di accessibilità a 24 ore è finito e la
mappa si può rigenerare. Idea, da dettagliare in un piano a parte: `04_genera_mappa.py` legge
`velocita_5t.json` e lo passa come `D.vel5t`; nel tema "Traffico e velocità" un selettore
"Adesso / Tipico all'ora scelta" colora i sensori con la cella `[S.dt][S.h]` (grigio se non `ok`),
con tag [MISURATO]. Regole da rispettare: chi cambia l'ora deve richiamare anche
`aggiornaLegenda()`; verifica finale aprendo davvero la pagina in un browser (non basta il
controllo di sintassi).
