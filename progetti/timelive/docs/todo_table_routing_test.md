# TODO — Test di "table routing" + modalità online/offline (2026-09-29)

Origine: articolo "Jev's Architecture Unmasked" (archerhume.com, 17 set 2026). Jev è un'API cloud chiusa che, dato uno stato + domande tipizzate, restituisce probabilità calibrate senza generare testo. Per Leo era solo una curiosità (nessun accesso a Jev, nessuna intenzione di adottarlo). Dell'articolo interessa l'IDEA (classificazione con probabilità invece di generazione), non il prodotto.

## Cosa fare
Costruire e far girare un test di accuratezza sulla SELEZIONE DELLE TABELLE: data una domanda dell'utente, quali tabelle di vault.db servono?

Ground truth gratuita: i report del reference Sonnet (~66 domande). Per ogni domanda, le tabelle toccate da run_sql/describe_table (da tool_calls_made) = tabelle "giuste". Da rivedere a mano dove Sonnet ha esplorato tabelle non necessarie.

Candidati da confrontare (tutti locali, nessun dato esce):
- A: embeddings locali sulle semantic_note/descrizioni delle tabelle
- B: modello locale (es. qwen3.5:4b) con scelta singola tra le tabelle
- C: ibrido A+B
- (opzionale) D: servizio cloud tipo Jev — solo se in futuro c'è accesso

Metriche: top-1, top-3, recall@k (TUTTE le tabelle necessarie nei primi k: conta per le domande cross-domain), robustezza all'ordine delle tabelle (permutazioni casuali — l'articolo mostra che l'ordine sposta le probabilità), e degrado con tabelle "distrattore" sintetiche (simulare 50–200 domini).

Se il router funziona: nuovo passo prima del loop di run_query(): route(question) -> [tabelle]; si iniettano direttamente i describe_table di quelle tabelle (e si aggiungono a described_tables, così il gate passa) -> meno round-trip. Sotto una soglia di confidenza: fallback all'indice compatto attuale. Da progettare come interfaccia con backend intercambiabili.

## Decisioni di Leo (2026-09-29)
- Il progetto va pensato per hardware MIGLIORE (che Leo non ha ancora, piano Mac Mini o simile), non per il Pi.
- Le prove si fanno comunque su Pi (latenza alta) o in sandbox con modelli leggermente migliori.
- Condividere descrizioni delle tabelle con un servizio online è accettabile MA deve essere una scelta esplicita: idea di una modalità di utilizzo ONLINE/OFFLINE, da espandere.

## Spunti per la modalità online/offline (da discutere)
- Oggi ClaudeAPIClient manda già al cloud anche i risultati delle query (righe reali), senza alcuna policy: l'"online" esiste già di fatto.
- Possibile policy a livelli: L0 niente esce; L1 escono solo domanda + descrizioni tabelle; L2 escono anche i risultati (con redazione delle colonne marcate sensitive=True in ColumnSpec).
- Da decidere: granularità (globale, per dominio o per colonna) e dove vive la configurazione (config.json).

## Altro spunto (non legato al cloud)
Verificare se la cache del prefisso del system prompt funziona in Ollama: registrare prompt_eval_count / prompt_eval_duration per ogni chiamata (oggi llm_bridge.py non lo fa).
