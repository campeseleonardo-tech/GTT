# RAPPORTO — TL04-test-v2

origine: agente TL04-test-v2
stato: bozza

## Cosa ho fatto
- Ho creato il NUOVO file `code/test_table_router_policy.py` (test `unittest`, solo standard library): test per `code/table_router.py` e `code/privacy_policy.py`.
- Non ho modificato alcun file esistente. Nessun dato personale usato: solo dati sintetici in memoria. Nessuna rete, nessun Ollama, nessun database.

## Cosa ho verificato (copertura richiesta dalla task)
- `route(...)` restituisce esattamente `k` risultati (k=1, 2, 3, 10 e default=3).
- Su dati sintetici una tabella che combacia chiaramente si posiziona prima (caso `spotify_plays` e caso `chess_games`).
- Mescolare l'ordine delle tabelle non crasha (25 shuffle su `rank` + `shuffle_tables_evaluate`); il ranking resta indipendente dall'ordine (la migliore resta prima).
- La policy di default è L0 (`load_policy({})`).
- L1 blocca `query_results` (ma permette domanda + descrizioni tabelle).
- L2 redige le colonne `sensitive=True` con `"[omesso]"` (e non muta le righe in ingresso).
- `load_policy` con sezione `privacy` mancante (o con `level` mancante) → L0.
- Extra a bassa quota: `evaluate` restituisce le chiavi `top1`/`top3`/`recall_at_k` e, sui dati sintetici, vale 1.0.

## Come far girare
- Dalla root del progetto: `python -m unittest code/test_table_router_policy.py`
- (alternativa) `python code/test_table_router_policy.py`

## Scelte (default scelti, tutti reversibili)
- Import dei moduli sotto test via `sys.path` (la dir di `code/`), così il test funziona sia come `code.test_table_router_policy` sia lanciato direttamente; non ho aggiunto `__init__.py`.
- Set sintetico di 4 tabelle (spotify/money/chess/whatsapp) con domande costruite sui token esatti delle descrizioni, perché `KeywordBackend` non fa stemming (es. uso "brano" non "brani").
- Nel test sul mescolamento, oltre a "non crashare" asserto anche che la tabella migliore resti al primo posto (robustezza attesa, da documentare).

## Da rivedere / decidere (non bloccante, fuori scope di questa task)
- Il wiring del router dentro `run_query` (`route()` -> iniezione dei `describe_table` + `described_tables`) è un passo a sé, già descritto in `docs/todo_table_routing_test.md`: non l'ho toccato.
- Non ho toccato `PROGETTO.md` (è tuo, Leo). Suggerimento: a valle, potresti marcare `table_router`/`privacy_policy` come modulo in "bozza" nella linea guida — lo propongo qui, non lo applico io.
- I test sono unitari e non coprono i backend `EmbeddingBackend`/`LocalLLMBackend` (stub `NotImplementedError`, richiedono Ollama): da testare in un'altra sessione con il modello locale.
