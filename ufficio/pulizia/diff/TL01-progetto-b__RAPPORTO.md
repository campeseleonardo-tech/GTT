# Rapporto TL01-progetto-b — llm_bridge v2 design

**Data**: 2026-09-29  
**Agente**: TL01-progetto-b  
**Task**: Scrivere docs/BRIDGE_V2_b.md (design indipendente v2, focus rischi + cosa più semplice)

---

## Cosa ho fatto

1. **Letto i file sorgente**: `docs/todo_table_routing_test.md` (direzioni pending), `code/llm_bridge.py` (v1 attuale), `docs/BRIDGE_V2_b.md` (già esistente, sovrascritto con versione aggiornata).
2. **Verificato ANSWERS.md**: non esiste → nessuna risposta di Leo da applicare.
3. **Scritto docs/BRIDGE_V2_b.md** con le 7 sezioni richieste (titoli esatti), in italiano, marcando "da verificare" i punti non confermati nel codice.
4. **Non ho creato DECISIONS.md** perché nessun blocco irreversibile: tutto procedibile con default sensati.
5. **Non ho creato DOMANDE.md** perché i 8 dubbi aperti sono già elencati in BRIDGE_V2_b.md § "Dubbi aperti per Leo" (formato chiuso con opzioni e raccomandazione).

---

## Cosa ho verificato nel codice (llm_bridge.py)

| Punto | Confermato | Note |
|-------|------------|------|
| 3 tool universali (list_tables, describe_table, run_sql) | ✅ | Lines 180-240 |
| Indice compatto in system prompt (_compact_schema_entry) | ✅ | Lines 300-320 |
| Gate `described_tables` obbligatorio prima di run_sql | ✅ | Lines 470-480, 580-590 |
| MAX_ITERATIONS=8 | ✅ | Line 35 |
| OLLAMA_NUM_CTX=8192, think=false default | ✅ | Lines 45, 390-400 |
| Backend: OllamaClient, ClaudeAPIClient, TogetherAIClient, FakeLLM | ✅ | Lines 430-550 |
| tool_run_sql: row limit 200, timeout 10s, read-only URI | ✅ | Lines 220-250 |
| _extract_referenced_tables (regex FROM/JOIN) | ✅ | Lines 290-310 |
| _try_parse_malformed_tool_call (recupero JSON malformato) | ✅ | Lines 520-580 |
| QueryResult con tool_calls_made, tool_results, malformed_recoveries | ✅ | Lines 590-610 |
| ColumnSpec.sensitive in ingest_engine | ❌ *da verificare* | Non trovato in llm_bridge.py; serve guardare ingest_engine.py |

---

## Scelte di default (reversibili, documentate in BRIDGE_V2_b.md)

1. **ROUTER_CONFIDENCE_THRESHOLD = 0.65** — punto di partenza, da tarare su ground truth.
2. **NoOpRouter come default** — comportamento v1 identico, zero rischio regressione.
3. **EmbeddingRouter con sentence-transformers/all-MiniLM-L6-v2** — raccomandato per indipendenza Ollama; alternativa nomic-embed-text via Ollana.
4. **Policy online/offline default L0** — più restrittivo, safe default.
5. **Cache embeddings su disco con hash semantic_note** — invalidazione semplice e deterministica.
6. **Fase 1–2 prima di Fase 4** — router + metriche prima di policy online/offline (ortogonali).

---

## Punti "da verificare" (non visti in llm_bridge.py, servono conferma da ingest_engine.py o test su Pi)

1. Esistenza di `ColumnSpec.sensitive: bool` in `ingest_engine` (necessario per L1/L2 policy).
2. Latenza reale `EmbeddingRouter` su Pi (~50ms stimato).
3. Ollama espone `logprob` / `prompt_eval_count` / `prompt_eval_duration` nella risposta `/api/chat`.
4. Crescita indice compatto: ~1.500–2.500 token/dominio (stima da commenti codice, non misurata).
5. Ground truth Sonnet: ~66 domande, copertura cross-domain sufficiente?

---

## Cosa deve decidere/rivedere Leo (già in BRIDGE_V2_b.md § "Dubbi aperti")

1. Modello embedding: MiniLM-L6-v2 (CPU) vs nomic-embed-text (Ollama).
2. Soglia confidence finale (dopo curva precision/recall su gt.json).
3. Aggiunta domande cross-domain sintetiche a ground truth.
4. Conferma/implementazione `ColumnSpec.sensitive` in ingest_engine.
5. Separazione router vs integrazione in run_query (raccomandato: separato).
6. Strategia invalidazione cache embeddings (hash semantic_note vs timestamp DB).
7. Disponibilità logprobs Ollama per confidence calibrata LLMRouter.
8. Conferma ordine fasi (1-2 prima di 4).

---

## Prossimi passi suggeriti

1. Leo rivede `docs/BRIDGE_V2_b.md` e risponde ai 8 dubbi (via ANSWERS.md o diretta).
2. Se risposte date → applicarle e procedere con Fase 1 (scheletro router + NoOpRouter).
3. Parallelamente: estrarre ground truth da report Sonnet (Fase 0).

---

*Rapporto generato da agente TL01-progetto-b. Nessun dato reale usato.*
