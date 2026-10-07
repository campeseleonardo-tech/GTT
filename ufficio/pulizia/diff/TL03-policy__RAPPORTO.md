# RAPPORTO — TL03-policy: privacy_policy.py

## Cosa ho fatto
Ho creato il file `code/privacy_policy.py` che implementa la policy online/offline per il Personal Data Vault, come richiesto dal task e discusso in `docs/todo_table_routing_test.md`.

## Cosa ho controllato
- Il file `llm_bridge.py` per capire come vengono usati i backend cloud (ClaudeAPIClient, TogetherAIClient) e quali dati transitano (domanda, descrizioni tabelle, risultati query).
- Il documento `docs/todo_table_routing_test.md` per i requisiti sui livelli L0/L1/L2 e la redazione delle colonne `sensitive=True`.
- La struttura delle ColumnSpec in `ingest_engine` (referenziata in llm_bridge.py) per il formato atteso di `columns` in `redact_rows`.

## Scelte fatte (default sensati)
1. **Livello default L0**: `load_policy` restituisce L0 quando la sezione "privacy" manca o `level` è assente/non valido — la scelta più sicura.
2. **Dominio per override**: il dominio è una stringa (es. "spotify", "money") che corrisponde al prefisso della tabella prima dell'underscore. Non ho hardcoded una lista di domini validi.
3. **Redazione solo a L2**: `redact_rows` applica la sostituzione "[omesso]" solo se il livello effettivo (con override) è ≥ L2. A L0/L1 restituisce le righe originali (il chiamante non dovrebbe inviarle comunque).
4. **Colonne sensibili**: rilevate da `col.get("sensitive") is True` — allineato a come `ColumnSpec` di `ingest_engine` espone il flag.
5. **Validazione stretta**: costruttore e `allows` sollevano `ValueError` per livelli/kind non validi, per fallire presto.
6. **Immutabilità**: `redact_rows` restituisce nuove liste/dizionari, non modifica gli input.

## Cosa Leo deve decidere/rivedere
- **Integrazione in llm_bridge.py**: dove e come istanziare/usare la Policy (es. in `run_query` prima di inviare messaggi al client cloud). Questo file fornisce solo la policy, non la sua integrazione.
- **Configurazione**: dove vive il `config_dict` passato a `load_policy` (ipotesi: `config.json` alla radice, ma non specificato).
- **Granularità override**: oggi è per dominio (prefisso tabella). Servirebbe per colonna? Per ora no, come da specifica.
- **Test di integrazione**: il self-test usa solo dati sintetici. Un test reale richiederebbe un vault.db popolato e un backend cloud configurato.

## Note
- Nessun dato reale usato nei test (solo dati sintetici: "Bohemian Rhapsody", "Queen", email finte).
- Codice solo standard library Python, nessuna dipendenza esterna.
- Commenti in italiano come richiesto.
