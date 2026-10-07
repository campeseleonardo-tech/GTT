# PERSONAL DATA VAULT — ARCHITETTURA & LINEE GUIDA

Questo documento descrive **come funziona il progetto oggi** e **quali
regole valgono quando si aggiunge qualcosa di nuovo**. Non è un diario:
la cronologia, i risultati dei test contro modelli reali, i bug chiusi e
le idee parcheggiate vivono in `EVOLUTION_LOG.md`, non qui. Se una
sezione qui sotto smette di essere vera, si corregge sul posto — non si
aggiunge una nota "v.qualcosa" sopra, si riscrive la frase.

---

## 1. Visione

Un sistema locale-first che rende l'intera vita digitale dell'utente
disponibile, strutturata e interrogabile da un LLM — piccolo (locale) o
grande (cloud, per scelta esplicita), non un'infrastruttura pensata per
uno solo dei due.

Domini attivi oggi: spotify, apple health (disattivato per rumore nei
dati), money (banca + investimenti pubblici + mercati privati), maps,
whatsapp, chess.com (**spotify, money e chess.com sono migrati al nuovo
motore SQLite; apple health/maps/whatsapp sono ancora sul vecchio
sistema JSON PRIMARY/FULL** — vedi §8). Candidati futuri: calendario,
email, foto, facebook, nutrizione, Pokémon GO, PayPal (trovato dentro i
dati reali di money il 2026-09-14, integrazione deliberatamente
rimandata — vedi §8 ed `EVOLUTION_LOG.md`) — nessuno ancora ispezionato/
integrato (vedi §7 "Regole di decisione": i dati reali vengono prima
dello schema).

L'architettura deve reggere l'aggiunta di nuovi domini senza essere
ridisegnata ogni volta — non solo in teoria: deve essere concretamente
più leggero aggiungere un dominio oggi che scrivere ~1500 righe da zero.

---

## 2. Architettura

```text
RAW DATA (mai toccato, resta dell'utente)
  ↓
ADAPTER per dominio (parse_raw + eventuali hook di classificazione)
  ↓
INGEST ENGINE (ingest_engine.py) — un unico database SQLite (vault.db),
una o più tabelle per concetto di dominio
  ↓
BRIDGE (llm_bridge.py) — 3 tool universali: list_tables / describe_table / run_sql
  ↓
LLM (locale via Ollama, o cloud via API — vedi §6)
  ↓
(futuro, non costruito: automazioni / correlazione cross-dominio esplicita)
```

Differenza principale rispetto alla versione precedente di questo
progetto: non esiste più un output doppio PRIMARY/FULL scritto a mano
per dominio. Un dominio produce **una tabella SQL** (o poche, se il
dominio lo richiede — vedi §3); "dammi il minimo utile" e "dammi il
dettaglio" diventano query diverse sulla stessa tabella (`ORDER BY
notability_score`, o senza), non due file da tenere sincronizzati.

Motivo della scelta SQL: un tool di ricerca su misura per dominio, con
molti parametri opzionali da combinare (il vecchio `search()`), si è
dimostrato fragile anche con modelli capaci — non solo con modelli
piccoli (vedi `EVOLUTION_LOG.md`, test del 2026-09-14, caso `chess_02`).
SQL è uno dei linguaggi più rappresentati nell'addestramento di
qualunque LLM, piccolo o grande: si dà al modello uno strumento che già
sa usare, invece di insegnargli un'API nuova ogni volta.

---

## 3. Contratto di dominio

Questo è il cuore tecnico del documento: cosa deve esistere perché un
dominio (nuovo o migrato) sia valido.

**Obbligatorio, sempre codice — cambia per ogni provider:**
- `parse_raw(files) -> list[dict]` (una funzione per tabella, se il
  dominio ne dichiara più di una)

**Dichiarazione della tabella (dati, non codice, dove possibile):**
- nome tabella, colonne (nome, tipo, nota semantica quando il nome da
  solo non basta)
- quale colonna è il timestamp canonico (vedi §4, standard timestamp)
- quali colonne sono "entity hint" per join cross-dominio: location,
  controparte/persona, categoria — quando esistono per quel dominio, mai
  inventate per somigliare ad altri domini
- la formula/i pesi per `notability_score`

**Classificazione:**
- priorità (mai invertita): 1) segnale nativo, 2) segnale strutturale/
  deterministico, 3) inferenza controllata con `confidence_rate`, 4)
  `unknown`. Se il dato non supporta una classificazione affidabile,
  `unknown` batte una risposta inventata.
- regola dichiarativa (dato, es. tabella keyword→categoria) quando
  basta; funzione dedicata quando serve vera semantica di dominio (es.
  estrazione ISIN da testo libero per la banca, parsing di
  `Termination` per chess.com) — qui la ricchezza specifica del dominio
  resta intatta, non viene appiattita per uniformità.
- **un segnale nativo va preservato per intero, non solo in parte**:
  la migrazione di money ha trovato un caso reale in cui due valori
  nativi diversi (Trade Republic "BUY"/"SELL") mappavano alla stessa
  coppia (transaction_type, category) — la sola categoria derivata non
  bastava più a distinguerli, e il valore nativo grezzo era stato
  scartato durante la pulizia. Corretto preservandolo in `category_raw`
  (vedi `EVOLUTION_LOG.md`) — una lezione generale: quando la
  classificazione derivata perde informazione rispetto al dato nativo,
  il dato nativo va tenuto da qualche parte, non solo documentato come
  "da tenere a mente".
- **il valore letterale esatto va reso scopribile, non presunto**: il
  batch notturno del 2026-09-15 ha trovato 3 casi reali in cui un
  modello ha indovinato un valore plausibile ma sbagliato per un filtro
  di testo (es. `institution = "Sella"` invece del valore reale `"Banca
  Sella"`, `domain = "Amazon"` per una colonna che vale solo
  `'bank'`/`'investment'`) e ha letto zero righe come "nessun dato"
  invece di verificare il valore — vedi `EVOLUTION_LOG.md`. Lezione
  generale: quando i valori reali di una colonna testuale differiscono
  da come un utente la formulerebbe naturalmente (lingua, forma nativa
  esatta, sigla vs nome completo), il `semantic_note` deve elencare i
  valori letterali esatti quando sono pochi e fissi, o suggerire
  esplicitamente una query di scoperta (`SELECT DISTINCT ...`) quando
  non lo sono — non basta che il tipo/la colonna esista.

**Un dominio può dichiarare più tabelle**, non necessariamente una sola
— il dominio money (banca+investimenti pubblici+mercati privati) oggi
dichiara tre tabelle (`transactions`, `security_events`,
`private_market_legs`), collegate solo da campi condivisi (isin,
prossimità temporale), non da foreign key — vedi `money_ingest.py`. Un
dominio come "facebook" (post, messaggi, reazioni) probabilmente ne
richiederà diverse anch'esso, correlate da chiavi condivise.

**Deduplicazione:** id nativo quando esiste, altrimenti chiave
composita deterministica e documentata (mai rimuovere record solo
perché "sembrano" duplicati). Attenzione: un id nativo non è sempre
davvero unico da solo — money ha trovato un caso reale (Banca Sella,
vedi `EVOLUTION_LOG.md`) dove lo stesso id nativo è condiviso da due
righe legittimamente diverse (un dividendo e la sua ritenuta fiscale);
la chiave di dedup lì è id nativo + segno dell'importo, non il solo id.

**Scoperta file di input:** il matching dell'estensione file deve
essere case-insensitive — trovato un caso reale (PayPal, dentro money,
2026-09-14) di export con estensione `.CSV` maiuscola che un
`rglob("*.csv")` case-sensitive ignorava silenziosamente su Linux/il
Raspberry Pi, senza nessun errore o warning. Vedi `money_ingest.py`,
`collect_input_files()`.

---

## 4. Standard condivisi (si applicano a ogni dominio)

- **Naming**: stesso concetto → stesso nome (`timestamp_begin`,
  `timestamp_end`, `source`, `category`, `notability_score`,
  `confidence_rate`...). Concetti specifici del dominio → nomi
  specifici. Niente sinonimi inutili.
- **Timestamp**: ISO 8601 UTC di default. Un dominio può dichiarare
  un'eccezione esplicita e documentata (es. WhatsApp: timestamp naive,
  perché l'export non porta un offset affidabile) — mai un'eccezione
  silenziosa.
- **Source**: un solo valore, orientato macchina, mai un array. Le
  etichette leggibili da umani (istituto, piattaforma...) sono campi
  separati.
- **Unità**: sempre esplicite (`eur`, `km`, `seconds`...), mai
  conversioni silenziose, mai somme tra unità incompatibili. Valute
  restano native, nessuna conversione automatica.
- **Confidence rate**: scala fissa, unica per tutto il progetto —
  `1.0` nativo, `~0.8` inferenza ad alta confidenza, `~0.5` media,
  `~0.2` bassa, `null`/assente quando il valore non è un'inferenza.
- **Inference level**: parametro configurabile per dominio (stesso
  concetto, nome specifico del dominio) su 4 livelli: `none`,
  `conservative`, `balanced`, `aggressive`.
- **Grouping/sessioni**: la vicinanza temporale da sola non basta mai —
  serve tempo + relazione semantica. **La definizione stessa di
  "sessione" varia moltissimo da dominio a dominio** (chess.com: poche
  partite ravvicinate, soglia 15-20 min; Spotify: può durare ore, anche
  un'intera giornata di ascolto; Pokémon GO: più accessi nella stessa
  ora) — va definita e validata contro dati reali dominio per dominio,
  mai riusata per analogia da un altro dominio. In chess.com questo è
  già implementato come una funzione di soglia (non una costante fissa)
  passata dal dominio al motore condiviso — vedi `ingest_engine.py`,
  `group_into_sessions()`. Money non usa sessioni: le transazioni non
  hanno una nozione naturale di "sessione" (deciso esplicitamente in
  questa migrazione, non è stato dimenticato).

---

## 5. Il motore (`ingest_engine.py`)

Sostituisce il vecchio `main.py`. Possiede: la creazione/gestione dello
schema SQLite a partire dalla dichiarazione di tabella di un dominio, il
calcolo di `notability_score` (stessa logica di prima, ora scritta una
volta sola nel motore invece che duplicata per dominio), la
deduplicazione con **id stabile tra re-ingest** (il dominio calcola una
sola chiave di dedup, il motore usa `INSERT ... ON CONFLICT ... DO
UPDATE`: una riga già esistente mantiene il suo id ma **viene comunque
aggiornata** nei campi che possono cambiare da un ingest all'altro, es.
`session_id`, `notability_score` — non basta ritrovare l'id vecchio, se
non si aggiornano anche gli altri campi restano disallineati, bug reale
trovato e corretto durante la migrazione di chess.com), e la
generazione di `describe_table()` per il bridge direttamente dallo
schema SQL — niente più doppia dichiarazione manuale (una nell'ingest,
una nel bridge). Un dominio registra il proprio schema **a livello di
modulo** (non dentro la funzione di ingest), così il bridge può leggere
la struttura delle tabelle senza dover rilanciare un ingest.

## 6. Il bridge (`llm_bridge.py`)

Tre tool soli, universali per qualunque dominio:
- `list_tables()` — sostituisce il vecchio manifest per dominio
- `describe_table(table)` — colonne, tipi, note semantiche
- `run_sql(query)` — l'unico modo di leggere dati

Guardrail obbligatori (stesso spirito della validazione precedente,
adattato a SQL), tutti verificati con test reali (non solo scritti,
provati a rompere) sulla migrazione di chess.com:
- connessione **in sola lettura a livello di permessi del database**
  (SQLite aperto in modalità read-only, non un controllo testuale sulla
  query — un tentativo di scrittura viene rifiutato dal database stesso)
- limite di righe forzato lato Python (si prendono al massimo N righe
  dal risultato, mai riscrivendo la query del modello per aggiungere un
  `LIMIT`)
- timeout basato su un progress handler SQLite (l'unico modo reale di
  interrompere una query lenta a metà esecuzione in SQLite — il
  parametro `timeout` di una connessione controlla solo l'attesa su un
  lock, non il tempo di esecuzione)

Sia il limite di righe sia il timeout sono **valori segnaposto**
(2026-09-14: nessun dominio migrato finora, money incluso, è stato
usato per ritararli — vedi `EVOLUTION_LOG.md` per la dimensione del
system prompt misurata con money incluso) — un solo punto nel codice
per ciascuno, da ritarare quando si migrano domini più grandi.

Il system prompt include anche alcune regole comportamentali esplicite
motivate da errori reali osservati (non scritte in astratto): non usare
`run_sql` solo per contare le righe di un'intera tabella quando
`row_count` è già nello schema iniettato; non usare placeholder di
parametro (`?`/`:nome`) in SQL, dato che `run_sql` non fa binding, solo
valori letterali diretti; prima di filtrare una colonna testuale su un
valore non certo esatto, fare prima una query di scoperta
(`SELECT DISTINCT ...`) invece di indovinare la stringa e concludere
"nessun dato" da zero righe — vedi `EVOLUTION_LOG.md`, batch del
2026-09-15.

Il loop di `run_query()` prova anche a recuperare una tool-call che il
modello ha scritto come testo JSON invece che come vera chiamata
strutturata, prima di accettarla come risposta finale. Il percorso
primario richiede un JSON valido che nomini uno dei 3 tool reali. Se il
parsing stretto fallisce — caso reale frequente, fino a 8 domande su 58
in un singolo batch cross-dominio (virgolette SQL non escapate dentro
il JSON auto-scritto dal modello, a volte incoerentemente nello stesso
blob — vedi `EVOLUTION_LOG.md`) — un fallback a regex mirato riconosce
comunque la forma esatta `{"name": ..., "parameters"/"arguments":
{"query": "..."}}` per il tool `run_sql`, estrae nome e query grezza, e
normalizza le virgolette doppiamente escapate prima di eseguirla; non
tenta mai di interpretare il resto del blob come JSON generico, per non
rischiare falsi positivi su prosa normale che contiene una graffa.
Resta comunque una copertura per disegno, non universale: un blob che
non rispetta né il JSON stretto né questa forma esatta (es. un blob
genuinamente troncato, osservato una volta) non viene recuperato.
`QueryResult`/i report dei batch salvano anche il risultato di ogni
tool-call, non solo la query, per lo stesso motivo.

Backend del modello: locale (Ollama) di default, cloud via API
disponibile esplicitamente per confronti o per l'uso quotidiano se
scelto (vedi `EVOLUTION_LOG.md` per i numeri reali di costo/qualità
misurati) — mai una scelta implicita.

---

## 7. Regole di decisione

Quando le priorità confliggono, in ordine di massima: possesso dei
dati, interoperabilità, utilità semantica, efficienza di recupero,
tracciabilità, estensibilità, compatibilità con l'LLM, semplicità di
implementazione. Non è una formula meccanica, è un criterio per
sciogliere un conflitto reale quando capita.

- Preferire calcolo deterministico (Python/SQL) al calcolo fatto
  dall'LLM per tutto ciò che è meccanico; riservare l'LLM al
  ragionamento semantico.
- Quando incerti su una classificazione, `unknown` batte la certezza
  inventata.
- Evitare complessità non necessaria prima che serva davvero: niente
  vector database, embeddings, knowledge graph finché il problema di
  retrieval non lo richiede concretamente.
- **Dati reali prima dello schema**: mai progettare lo schema di un
  nuovo dominio senza aver prima ispezionato un export reale — sorprese
  strutturali (formati, redundanze, casi limite) sono la norma, non
  l'eccezione. Confermato di nuovo dalla migrazione di money: l'ipotesi
  iniziale ("i mercati privati saranno una fonte/file separato") era
  sbagliata — sono 8 righe incorporate nell'export di Trade Republic,
  visibile solo ispezionando i dati reali, non da un'assunzione
  ragionevole. Confermato una terza volta dal batch di test reale su
  money (2026-09-14): un gap di schema (BUY/SELL indistinguibili) e una
  quarta fonte dati mai vista (PayPal) sono emersi entrambi solo
  interrogando dati veri con un modello vero, non da una revisione del
  codice a tavolino.
- **Consolidare prima di estendere**: quando un batch di test reale
  trova più bug in un dominio esistente (schema e/o bridge), si
  corregge e si rivalida quel dominio prima di aggiungerne uno nuovo —
  deciso esplicitamente dal project owner dopo il batch cross-dominio
  del 2026-09-15 (3 domini esistenti da consolidare prima di riaprire
  PayPal o altri candidati, vedi §8).
- Evitare pattern O(n²) su operazioni applicate a un intero dataset.

---

## 8. Stato attuale

*(sezione viva — si sovrascrive, non si accumula)*

- **chess.com è stato il primo dominio migrato al nuovo motore SQLite**,
  completo: `ingest_engine.py`, `chessdotcom_ingest.py` (tabelle
  `games`, `game_moves`, `playing_sessions`), e `llm_bridge.py`
  aggiornato ai 3 tool universali. Validato contro i dati reali
  dell'utente (1.785 partite, 364 sessioni) e con un modello vero
  (llama3.2:3b su Raspberry Pi) rispondendo correttamente a una domanda
  reale via `run_sql`.
- I bug `chess_02` (filtro upset sempre vuoto) e `chess_04` (nessun
  breakdown per `win_method`) sono **chiusi**, verificati a mano contro
  i dati reali — non solo per assenza di errori, per lettura riga per
  riga dell'output SQL. Lo scarto 1.783 vs 1.785 partite è **chiuso**:
  1.785 è il numero corretto (confermato da `SELECT COUNT(*)`), 1.783
  era un effetto del vecchio bug di aggregazione, non un problema nei
  dati.
- **Spotify è il secondo dominio migrato**, completo: tabelle `plays` e
  `listening_sessions`, registrato in `DOMAIN_REGISTRY`. Validato con
  due modelli veri sul Raspberry Pi (llama3.2:3b e qwen2.5:3b, dati
  reali: 358.440 play, 17.445 sessioni, tre batch reali il 2026-09-14)
  — **nessun bug di ingest trovato in nessuno dei run**; gli errori
  osservati sono tutti di generazione SQL/ragionamento del modello
  (confusione tra colonne dal significato simile, valori di filtro
  inventati, aggregazioni sbagliate), non della pipeline. Dettaglio
  completo, incluso il confronto diretto llama3.2:3b vs qwen2.5:3b, in
  `EVOLUTION_LOG.md`.
- **Money è il terzo dominio migrato** (2026-09-14): banca (meinElba/
  Raiffeisen, Banca Sella) + investimenti pubblici e mercati privati
  (Trade Republic), tre tabelle (`transactions`, `security_events`,
  `private_market_legs`), nessuna foreign key tra loro. Costruito e
  testato in sandbox contro i 3 file reali dell'utente (2.449 righe
  meinElba, 358 righe utili Sella, 441 righe Trade Republic → 3.202
  transazioni + 38 security event + 8 leg di mercati privati): doppio
  run per idempotenza (secondo run 0 righe nuove), `PRAGMA
  integrity_check` ok, 0 violazioni foreign key, audit di privacy
  sull'intera tabella (0 IBAN residui trovati).
- Nella migrazione di money sono stati trovati e corretti **5 bug
  reali** (non ereditati silenziosamente): (1) il parsing dei
  timestamp meinElba con millisecondi falliva silenziosamente al 100%
  per un format-string sbagliato (fallback silenzioso a precisione
  giornaliera su ogni riga); (2) un IBAN non etichettato compariva in
  chiaro in una descrizione Trade Republic, non coperto dal redattore
  basato su etichetta "IBAN:"; (3) il nome file stesso dell'export
  meinElba incorporava l'IBAN del conto, copiato verbatim in
  `source_file` su 2.449 righe prima della correzione; (4) Trade
  Republic BUY e SELL erano indistinguibili nello schema — trovato dal
  primo batch reale, corretto preservando il tipo nativo in
  `category_raw`; (5) la scoperta dei file di input era
  case-sensitive (`rglob("*.csv")`), rendendo invisibili 8 file PayPal
  reali con estensione `.CSV` maiuscola — trovato ispezionando
  `Input/Money` su richiesta del project owner, non da un errore
  riportato. Dettagli completi in `EVOLUTION_LOG.md`.
- **Trovata una quarta fonte dati reale per money (PayPal), integrazione
  deliberatamente rimandata**: cartella `Input/Money/paypal/`, 8 file
  CSV reali (263 righe con dati veri), formato italiano a 79 colonne,
  con due rischi concreti non ancora risolti (doppio conteggio con i
  bonifici bancari già ingeriti; gestione degli stati "In sospeso").
  Decisione esplicita del project owner: rimandare a un round separato,
  non farlo insieme al fix del gap BUY/SELL, e — dopo il batch del
  2026-09-15 — non farlo comunque finché i 3 domini esistenti non sono
  consolidati (vedi punto successivo). Vedi `EVOLUTION_LOG.md`.
- **Batch cross-dominio notturno, tutti e 3 i domini migrati insieme
  (2026-09-15)**: 58 domande contro llama3.2:3b (chessdotcom+spotify+
  money), analizzate una per una contro il codice sorgente e i numeri
  reali noti. Il run parallelo su qwen2.5:3b è caduto per
  disconnessione SSH alla prima domanda — nessun confronto diretto
  possibile questo giro, da rifare con `nohup`/`tmux`. **Nessun bug di
  ingest nuovo trovato** — tutti gli errori osservati sono ancora di
  ragionamento/generazione SQL del modello o di gap di schema semantico
  esposto via `describe_table()`, non di dati sbagliati nel vault. Due
  classi di fix applicate (dettaglio completo in `EVOLUTION_LOG.md`):
  (1) il recupero di una tool-call scritta come testo JSON invece che
  come chiamata strutturata — già presente da spotify ma limitato al
  JSON sintatticamente valido — è stato esteso con un fallback a regex
  mirato per la forma `run_sql`/`{"query": "..."}` quando il JSON del
  modello stesso è malformato (virgolette non escapate), coprendo così
  8/58 casi osservati stanotte contro i 2/11 originari; (2) 4
  `semantic_note` di `money_ingest.py` (institution/domain/
  instrument_name/transaction_type) sono stati arricchiti con i valori
  letterali reali esatti, più una regola generale nel system prompt di
  `llm_bridge.py` che chiede una query di scoperta prima di filtrare su
  un valore testuale non certo — motivati da 3 casi reali di valore
  indovinato male (uno dei quali, `money_13` su NVIDIA, aveva prodotto
  una risposta **confermata falsa** dal project owner). Entrambi i file
  distribuiti al progetto claude.ai e al PC Windows
  (`C:\Users\campe\Desktop\Timelive\code\`) — **non ancora trasferiti
  al Raspberry Pi (manuale, da fare dall'utente) né validati con un
  batch reale**: prossimo passo naturale è rilanciare il batch (idealmente
  anche qwen2.5:3b) e verificare che gli 8 casi JSON e i 3 casi di
  valore letterale siano davvero risolti. Decisione esplicita del
  project owner: nessun nuovo dominio (PayPal incluso) finché questa
  validazione non è fatta — si consolidano prima i 3 domini esistenti.
- Trovato ma **non corretto** durante la migrazione di money (fuori
  scope, segnalato al project owner): il vero `config.json` sul disco
  dell'utente non è JSON valido — contiene una versione vecchia e
  ormai superata di `config.py` (solo Spotify). Ogni dominio, non solo
  money, sta già ricadendo silenziosamente sul dizionario di fallback
  dentro `config.py`. Vedi `EVOLUTION_LOG.md` e la nota "KNOWN ISSUE"
  in cima a `config.py`.
- Gli altri 3 domini (apple health disattivato, maps, whatsapp) sono
  ancora sul vecchio sistema JSON PRIMARY/FULL — si migrano **uno alla
  volta**, come chess.com/spotify/money: dati reali del dominio prima
  dello schema (§7), poi contratto §3, poi ingest, poi test con dati
  finti e reali, poi validazione col bridge. Il prossimo non è ancora
  stato scelto a data di oggi — e comunque non prima di aver consolidato
  i 3 domini esistenti (vedi sopra).
- File del vecchio sistema non ancora rimossi finché non tutti i domini
  sono migrati: `main.py`, i dataset JSON PRIMARY/FULL dei domini non
  ancora migrati (incluso il vecchio `money_ingest.py`/`bank_dataset*.json`,
  tenuti per riferimento/rollback). `batch_test_llm_bridge.py` è stato
  riportato ai 3 tool nuovi (2026-09-14, vedi `EVOLUTION_LOG.md`) e usato
  per i batch reali su spotify e money. `test_llm_bridge.py` invece
  parla ancora dei vecchi tool `search`/`resolve_full_ref`/
  `get_aggregation` — non ancora riscritto. `config.py` si ripulisce un
  dominio alla volta, insieme alla sua migrazione — non tutto insieme.

---

## 9. Storia ed evidenza

Tutto il resto — changelog per versione, i risultati reali dei batch di
test contro i modelli, le decisioni chiuse, le idee esplicitamente
parcheggiate per dopo (layer di confronto con standard esterni,
ambizione "JARVIS" di auto-miglioramento) — vive in `EVOLUTION_LOG.md`.
