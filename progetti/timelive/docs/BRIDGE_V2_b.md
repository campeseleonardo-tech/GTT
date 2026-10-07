# llm_bridge v2 — Progetto Indipendente (TL01-progetto-b)

**origine**: agente TL01-progetto-b  
**stato**: bozza

---

## Come funziona oggi

L'attuale `llm_bridge.py` (v1) espone **3 tool universali** al modello:
- `list_tables()` — elenco tabelle in `vault.db`
- `describe_table(table)` — colonne, tipi, note semantiche, row count, foreign key, timestamp canonico
- `run_sql(query)` — unica via per leggere dati (read-only enforced da SQLite URI `mode=ro`)

**Flusso per domanda** (`run_query`):
1. System prompt = indice compatto di **tutte** le tabelle (nome, row_count, colonne+tipi SQL, FK, timestamp canonico) — ~2.000 caratteri su 16 tabelle reali.
2. Il modello chiama `describe_table` sulle tabelle che ritiene rilevanti (obbligatorio per il gate `described_tables` in `run_query`: `run_sql` fallisce se riferisce a tabelle non ancora descritte).
3. Il modello scrive SQL, `run_sql` esegue con guardrail: row limit 200, timeout 10s, una sola statement.
4. Loop agentico fino a `MAX_ITERATIONS=8` (rialzato da 5 per il costo del gate `describe_table`).

**Backend supportati**: `OllamaClient` (locale, default `llama3.2:3b`, `num_ctx=8192`, `think=false`), `ClaudeAPIClient` (cloud, Anthropic), `TogetherAIClient` (cloud, OpenAI-compat), `FakeLLM` (test).

**Problemi noti (da codice e commenti)**:
- **Indice compatto sufficiente oggi**, ma cresce ~1.500–2.500 token per dominio aggiunto. Con 30–50 domini futuri, l'indice piatto potrebbe avvicinarsi a frazioni significative di `OLLAMA_NUM_CTX` (8192) — *da verificare*.
- **Nessun routing esplicito**: il modello scopre le tabelle dall'indice compatto e decide da solo quali `describe_table` chiamare. Spesso indovina male i nomi colonna (es. `media_owner_username` vs reale `owner_username` su `instagram_posts`) e recupera per tentativi.
- **Nessuna metrica di routing**: non si misura top-1/top-3/recall@k della selezione tabelle.
- **Modalità online/offline implicita**: `ClaudeAPIClient` e `TogetherAIClient` mandano già tutto al cloud (domanda, schema, risultati query, incluse colonne `sensitive=True`) senza policy configurabile.
- **Nessuna osservabilità prompt cache Ollama**: `prompt_eval_count` / `prompt_eval_duration` non vengono registrati.

---

## Cosa cambia in v2

**Obiettivo**: aggiungere un **router di tabelle** esplicito, intercambiabile, misurabile, che preceda il loop agentico e riduca i round-trip `describe_table` → `run_sql`. Mantenere l'architettura a 3 tool invariata.

**Principio guida**: la cosa più semplice che potrebbe funzionare per prima. Niente pipeline complesse, niente reranking, niente embedding se non servono.

**Cambiamenti minimi**:
1. **Nuovo step `route(question) -> List[TableRoute]`** prima di `run_query`. `TableRoute = (table_name, confidence, reason)`.
2. **Iniezione diretta dei `describe_table`** per le tabelle routate sopra soglia → si popolano in `described_tables` prima del primo turno → il modello salta i `describe_table` espliciti per quelle tabelle.
3. **Fallback**: se confidence < soglia, si usa l'indice compatto attuale (comportamento v1 invariato).
4. **Interfaccia router intercambiabile** (protocollo Python `Router`) con backend: `EmbeddingRouter`, `LLMRouter`, `HybridRouter`, `NoOpRouter` (default v1).
5. **Policy online/offline esplicita** (L0/L1/L2) applicata a ciò che esce dal processo: domanda, descrizioni tabelle, risultati query.
6. **Metriche di routing** collegate al ground truth dei report Sonnet (~66 domande, tabelle toccate da `tool_calls_made`).

**Rischi principali** (ordinati per impatto × probabilità):
| Rischio | Impatto | Prob. | Mitigazione v2 |
|---------|---------|-------|----------------|
| Router sbaglia tabelle → modello non ha `describe_table` → `run_sql` fallisce al gate | Alto | Media | Fallback automatico a indice compatto se confidence bassa; `NoOpRouter` sempre disponibile via flag CLI |
| Router aggiunge latenza > round-trip `describe_table` risparmiati | Medio | Alta | Misurare latenza router vs round-trip medio (target: router < 500ms su Pi); `EmbeddingRouter` con cache embeddings tabelle |
| Ground truth rumoroso (Sonnet ha esplorato tabelle inutili) | Medio | Alta | Revisione manuale delle ~66 domande; etichetta `necessary` vs `exploratory` per tabella |
| Policy online/offline non applicata a tutti i backend | Alto | Bassa | Centralizzare in `OutboundFilter` chiamato da ogni `LLMClient.chat()`; test unitario per L0/L1/L2 |
| Crescita indice compatto rompe `num_ctx` su molti domini | Medio | Media | v2 non peggiora; monitorare `prompt_eval_count`; piano B: indice a due livelli (dominio→tabelle) differito |
| Embedding model non allineato a semantic_note reali | Medio | Media | Usare stesso testo che finisce in `describe_table` (semantic_note + entity_hint); valutare `LLMRouter` come baseline |

---

## Interfaccia del router di tabelle

```python
# In un nuovo modulo, es. bridge/router.py
from dataclasses import dataclass
from typing import Protocol, List, Optional

@dataclass(frozen=True)
class TableRoute:
    table: str           # nome esatto da list_tables()
    confidence: float    # 0.0–1.0, calibrato per soglia operativa
    reason: str          # breve, per debug/log (es. "embedding cos=0.82", "llm choice")

class Router(Protocol):
    def route(self, question: str, available_tables: List[str]) -> List[TableRoute]:
        """Restituisce tabelle ordinate per confidence decrescente."""
        ...

    def warmup(self) -> None:
        """Pre-carica modelli/embeddings/index. Chiamato una volta all'avvio."""
        ...
```

**Backend concreti** (ognuno in proprio file, registrabili via factory):

| Backend | Descrizione | Input per routing | Output confidence | Note |
|---------|-------------|-------------------|-------------------|------|
| `NoOpRouter` | Restituisce lista vuota → fallback a indice compatto v1 | — | — | Default sicuro, zero dipendenze |
| `EmbeddingRouter` | Embedding locale (es. `sentence-transformers/all-MiniLM-L6-v2` o `nomic-embed-text` via Ollama) su `semantic_note` + `entity_hint` + `column_names` per tabella | Vettore domanda vs vettore tabella (mean pooling colonne) | Cosine similarity 0–1 | Cache embeddings tabelle su disco (invalidata se schema cambia); ~50ms su Pi *da verificare* |
| `LLMRouter` | Modello locale (es. `qwen3.5:4b` via Ollama) con prompt: "Scegli 1–3 tabelle rilevanti per: {question}. Tabelle: {compact_index}. Rispondi JSON: [{table, confidence, reason}]" | Indice compatto + domanda | Probabilità da logits / auto-reportata | Single-turn, no tool calls; `think=false`; temperatura 0.1 |
| `HybridRouter` | Combina: `EmbeddingRouter` top-5 → `LLMRouter` rerank su quelle 5 | Unione | Media pesata o `LLMRouter` finale | Più costoso, solo se embedding da solo non basta |

**Integrazione in `run_query`** (modifica minima):
```python
# All'inizio di run_query(), prima del loop:
routed = router.route(question, ingest_engine.list_tables())
high_conf = [r for r in routed if r.confidence >= ROUTER_CONFIDENCE_THRESHOLD]
for r in high_conf:
    # Iniettare describe_table direttamente, populare described_tables
    desc = tool_describe_table(r.table)
    if "error" not in desc:
        described_tables.add(r.table)
        # Opzionale: aggiungere al contesto del modello come messaggio tool-result sintetico
```
**Soglia default**: `ROUTER_CONFIDENCE_THRESHOLD = 0.65` (da tarare su ground truth). Sotto soglia → nessun `describe_table` pre-injected, comportamento v1.

**Ordine tabelle**: il router **deve** restituire ordine deterministico per confidence decrescente. Test di robustezza: permutare `available_tables` in input → output invariato.

---

## Politica online/offline

**Tre livelli** (configurabili globalmente, per dominio, o per colonna `sensitive`):

| Livello | Cosa PUÒ uscire dal processo | Cosa NON esce mai | Uso tipico |
|---------|------------------------------|-------------------|------------|
| **L0 — Air-gapped** | Nulla. Solo `OllamaClient` / `FakeLLM` ammessi. | Domanda, schema, risultati, tutto. | Default per dati sensibili (health, money, whatsapp). |
| **L1 — Schema-only** | Domanda + descrizioni tabelle (`describe_table` output, **senza** colonne `sensitive=True`). | Risultati query (righe reali), valori colonne sensibili. | Router cloud (es. futuro servizio tipo Jev), modelli cloud per solo routing. |
| **L2 — Full** | Domanda, schema, **risultati query** (righe reali). Colonne `sensitive=True` **redatte** (es. `[REDACTED]`). | Nulla (tutto esce ma redatto). | `ClaudeAPIClient`, `TogetherAIClient` per ragionamento complesso cross-domain. |

**Implementazione**: nuovo `OutboundFilter(policy: PolicyLevel, sensitive_columns: Set[TableColumn])` iniettato in ogni `LLMClient.chat()`:
- `OllamaClient` / `FakeLLM`: no-op (locale).
- `ClaudeAPIClient` / `TogetherAIClient`: prima di `requests.post`, filtra `messages`:
  - L0: solleva errore se client cloud usato.
  - L1: rimuove messaggi `tool` (risultati query); mantiene `system` (schema) e `user` (domanda); strip `sensitive` da `describe_table` results in history.
  - L2: mantiene tutto ma redige valori `sensitive` in `tool` messages.

**Configurazione**: `config.json` (nuovo file, non in repo, template in `config.example.json`):
```json
{
  "online_policy": "L0",
  "router": "embedding",
  "router_threshold": 0.65,
  "per_domain_policy": {
    "money": "L0",
    "health": "L0",
    "spotify": "L1",
    "chessdotcom": "L2"
  },
  "per_column_policy": {
    "transactions.iban": "L0",
    "health.heart_rate": "L0"
  }
}
```
*Nota*: `per_domain_policy` e `per_column_policy` fanno override su `online_policy` globale (più restrittivo vince).

---

## Metriche e come misurarle

**Ground truth**: report Sonnet esistenti (~66 domande). Per ogni domanda: tabelle toccate da `run_sql`/`describe_table` in `tool_calls_made` = `necessary_tables`. Revisione manuale per marcare `exploratory_tables` (Sonnet le ha toccate ma non servivano).

**Metriche primarie** (per router):
- **Top-1 accuracy**: la tabella #1 del router è in `necessary_tables`?
- **Top-3 accuracy**: almeno una delle prime 3 del router è in `necessary_tables`?
- **Recall@k**: `|necessary_tables ∩ top_k(router)| / |necessary_tables|` — **critico per cross-domain** (serve TUTTE le tabelle necessarie).
- **Precision@k**: `|necessary_tables ∩ top_k| / k` — evita tabelle distrattore.

**Metriche secondarie**:
- **Latenza router** (ms) vs round-trip `describe_table` risparmiati (ms).
- **Robustezza all'ordine**: stessa domanda, `available_tables` permutato 10 volte → output invariato (confidence ±0.02).
- **Degrado con distrattori**: aggiungere 50/100/200 tabelle sintetiche (nomi casuali, schema fittizio) → misurare recall@k.
- **Calibrazione confidence**: binning confidence vs accuracy empirica (reliability diagram).

**Come misurare** (script `eval_router.py`, da creare):
```bash
# 1. Estrai ground truth da report Sonnet
python -m bridge.eval_router extract-gt --report-path reports/sonnet_batch_*.json --out gt.json

# 2. Revisione manuale gt.json (aggiungi flag exploratory)

# 3. Esegui router su ogni domanda
python -m bridge.eval_router run --router embedding --gt gt.json --out results_embedding.json

# 4. Report aggregato
python -m bridge.eval_router report --results results_*.json --out router_metrics.md
```
Output `router_metrics.md` con tabelle markdown per confronto A/B/C.

**Target minimi per promuovere router a default** (da concordare con Leo):
- Recall@3 ≥ 0.90 su domini singoli
- Recall@5 ≥ 0.85 su cross-domain
- Latenza router < 500ms su Pi (media 10 run)
- Nessun regresso su accuracy risposta finale (confronto batch v1 vs v2+router)

---

## Ordine di lavoro

**Fase 0 — Preparazione (bloccante per metriche)**
- [ ] Estrarre ground truth dai report Sonnet (~66 domande) → `gt.json`
- [ ] Revisione manuale `gt.json`: marcare `necessary` vs `exploratory` per tabella
- [ ] Creare tabelle sintetiche "distrattore" (50, 100, 200) per test degrado

**Fase 1 — Scheletro router + NoOpRouter (1–2 giorni)**
- [ ] Nuovo modulo `bridge/router.py` con `Router` protocol, `TableRoute`, `NoOpRouter`
- [ ] Aggiungere `router` parameter a `run_query()` (default `NoOpRouter()`)
- [ ] Integrazione minima: pre-inject `describe_table` per tabelle sopra soglia
- [ ] Flag CLI `--router noop|embedding|llm|hybrid` per selezione backend
- [ ] Test: v1 behavior invariato con `--router noop`

**Fase 2 — EmbeddingRouter (2–3 giorni)**
- [ ] Scelta modello embedding: `sentence-transformers/all-MiniLM-L6-v2` (CPU, ~80MB, 384-dim) *o* `nomic-embed-text` via Ollama (già installato?) — **decisione Leo**
- [ ] Costruire corpus tabelle: per tabella, concatenare `semantic_note` + `entity_hint` + `column_names` da `describe_table`
- [ ] Cache embeddings su disco (`~/.cache/timelive/router_embeddings/{table}.npy`), invalidare su schema change (hash delle `semantic_note`)
- [ ] Misurare latenza su Pi, top-1/3/5, recall@k su ground truth

**Fase 3 — LLMRouter (1–2 giorni)**
- [ ] Prompt engineering: few-shot con 5–10 esempi da ground truth
- [ ] Parsing JSON robusto (riusare `_try_parse_malformed_tool_call` pattern)
- [ ] Confidence da logits se disponibili (Ollama `logprob`? *da verificare*), altrimenti auto-reportata
- [ ] Confronto A/B con EmbeddingRouter su ground truth

**Fase 4 — HybridRouter + Policy online/offline (2–3 giorni)**
- [ ] `HybridRouter`: embedding top-5 → LLM rerank
- [ ] `OutboundFilter` + `PolicyLevel` enum + config loader
- [ ] Applicare a `ClaudeAPIClient` / `TogetherAIClient` / `OllamaClient` (no-op)
- [ ] Test L0/L1/L2 con dati sintetici (nessun dato reale)

**Fase 5 — Metriche + Validazione end-to-end (2 giorni)**
- [ ] Script `eval_router.py` completo
- [ ] Batch confronto: v1 (no router) vs v2+EmbeddingRouter vs v2+LLMRouter vs v2+HybridRouter
- [ ] Misurare: accuracy risposta finale, latenza totale, tool calls/question, token usage
- [ ] Report finale per Leo con raccomandazione default

**Fase 6 — Osservabilità prompt cache Ollama (parallelo, 0.5 giorni)**
- [ ] Loggare `prompt_eval_count` / `prompt_eval_duration` da risposta Ollama (`payload.get("prompt_eval_count")` *da verificare*)
- [ ] Aggiungere a `QueryResult` o log strutturato

---

## Dubbi aperti per Leo

1. **Modello embedding per `EmbeddingRouter`**: `sentence-transformers/all-MiniLM-L6-v2` (locale, CPU, nessuna dipendenza Ollama, ~50ms su Pi *da verificare*) vs `nomic-embed-text` via Ollama (già in RAM se Ollama gira, ma consuma VRAM/RAM aggiuntiva). *Raccomandazione: MiniLM-L6-v2 per indipendenza da Ollama e footprint minimo.*
2. **Soglia confidence default**: `0.65` è un punto di partenza. Va tarata su ground truth. *Proposta: misurare precision/recall curve su gt.json e scegliere punto dove recall@k ≥ 0.90.*
3. **Ground truth**: i ~66 report Sonnet bastano? Servono domande cross-domain sintetiche aggiuntive? *Raccomandazione: iniziare con quelli, aggiungere 10–15 cross-domain manuali se recall@k basso.*
4. **Policy online/offline per colonna `sensitive`**: oggi `ColumnSpec.sensitive: bool` esiste in `ingest_engine`? *Da verificare nel codice. Se no, va aggiunto prima di L1/L2.*
5. **Router come passo separato vs integrato in `run_query`**: tenerlo separato (più testabile, riutilizzabile) o fondere? *Raccomandazione: separato, iniettato come dipendenza.*
6. **Caching embeddings**: invalidazione su schema change — usare hash delle `semantic_note` per tabella? O timestamp `vault.db`? *Raccomandazione: hash delle `semantic_note` concatenate (stabili se schema non cambia).*
7. **LLMRouter confidence**: Ollama espone logprobs per estrarre confidence calibrata? *Da verificare. Se no, usare auto-reportata nel JSON (meno affidabile).*
8. **Ordine di lavoro**: priorità Fase 1–2 (router funzionante + metriche) prima di Fase 4 (policy online/offline)? *Sì, policy è ortogonale e può arrivare dopo.*

---

*Documento scritto da agente TL01-progetto-b. Nessun dato reale usato. Tutti i valori numerici (latenze, token, soglie) sono stime da verificare su hardware reale.*
