# Rapporto TL01-progetto-b — Progetto llm_bridge v2

**Data**: 2026-09-29  
**Agente**: TL01-progetto-b  
**Stato**: bozza consegnata

## Cosa ho fatto
- Letto `code/llm_bridge.py` (v1 attuale) e `docs/todo_table_routing_test.md` (direttive TODO).
- Scritto `docs/BRIDGE_V2_b.md` in italiano: design indipendente v2 focalizzato su rischi e cosa più semplice che possa funzionare.
- Struttura esatta delle 7 sezioni richieste: Come funziona oggi, Cosa cambia in v2, Interfaccia del router di tabelle, Politica online/offline, Metriche e come misurarle, Ordine di lavoro, Dubbi aperti per Leo.

## Cosa ho verificato (dal codice reale)
- v1 ha 3 tool: `list_tables`, `describe_table`, `run_sql`.
- Indice compatto iniettato in system prompt (~2k char su 16 tabelle reali).
- Gate `described_tables` enforza `describe_table` prima di `run_sql` (aggiunto 2026-09-15).
- `MAX_ITERATIONS=8`, `SQL_ROW_LIMIT=200`, `SQL_TIMEOUT_SECONDS=10.0`, `OLLAMA_NUM_CTX=8192`.
- Backend: `OllamaClient` (think=false), `ClaudeAPIClient`, `TogetherAIClient`, `FakeLLM`.
- `ColumnSpec.sensitive` **non verificato** in `ingest_engine` — marcato "da verificare" nel documento.
- Ollama `prompt_eval_count` / `prompt_eval_duration` **non loggati** attualmente — confermato dal TODO.

## Scelte (default reversibili presi per non bloccarsi)
1. **Protocollo `Router` separato** (non fuso in `run_query`) — più testabile, riutilizzabile.
2. **`NoOpRouter` come default** — v1 behavior invariato se flag `--router noop` o assente.
3. **Soglia confidence 0.65** — punto di partenza, da tarare su ground truth.
4. **Embedding model: `all-MiniLM-L6-v2`** — raccomandato per indipendenza da Ollama; alternativa `nomic-embed-text` via Ollama lasciata come opzione.
5. **Policy online/offline a 3 livelli (L0/L1/L2)** — granulosità globale + per dominio + per colonna (più restrittivo vince).
6. **Ground truth da report Sonnet (~66 domande)** — revisione manuale per marcare `necessary` vs `exploratory`.
6. **Metriche target**: Recall@3 ≥ 0.90 singolo dominio, Recall@5 ≥ 0.85 cross-domain, latenza router < 500ms su Pi.
7. **Ordine di lavoro**: Fase 0–2 prima (router + metriche), Fase 4 (policy) dopo.

## Da decidere da Leo (domande aperte → `DOMANDE.md`)
Creo `DOMANDE.md` con 8 domande chiuse (max 15 parole, 2-4 opzioni).

## Note
- Nessun codice scritto (solo documento design).
- Nessun dato reale usato — solo esempi sintetici.
- Tutti i valori numerici marcati "da verificare" dove non misurati su Pi.
