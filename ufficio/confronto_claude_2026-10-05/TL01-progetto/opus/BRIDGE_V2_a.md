# llm_bridge v2 — progetto (bozza)

origine: agente TL01-progetto-a · stato: bozza · basato su `code/llm_bridge.py` (versione letta il 2026-10-05) e `docs/todo_table_routing_test.md`.
Nessun dato reale usato: tutti gli esempi sotto sono sintetici. Dove scrivo "da verificare" significa che la cosa NON è nel codice che ho letto.

---

## Come funziona oggi

- 3 tool generici: `list_tables`, `describe_table(table)`, `run_sql(query)`; nessun tool conosce un dominio specifico.
- `vault.db` è aperto in sola lettura (`mode=ro`); `run_sql` restituisce al massimo `SQL_ROW_LIMIT=200` righe e si ferma dopo `SQL_TIMEOUT_SECONDS=10` (progress handler).
- `validate_tool_call` accetta solo query che iniziano con `SELECT`/`WITH` e solo tabelle note a `ingest_engine.list_tables()`.
- `build_system_prompt()` inietta un INDICE COMPATTO di tutte le tabelle (row_count, nomi/tipi colonne, foreign_keys, colonna timestamp), senza semantic_note.
- `run_query()` è un loop di massimo `MAX_ITERATIONS=8` giri: il modello chiama tool o risponde in testo.
- Gate obbligatorio: un `run_sql` su una tabella non ancora passata da `describe_table` viene respinto (`describe_table_required`); le tabelle si estraggono con una regex FROM/JOIN (`_extract_referenced_tables`).
- Una chiamata identica alla precedente non viene rieseguita; dopo 8 giri Python restituisce l'ultimo risultato con avviso di risposta parziale.
- Se il modello scrive la chiamata come testo JSON, `_try_parse_malformed_tool_call` la recupera (contata in `malformed_tool_call_recoveries`).
- Backend intercambiabili dietro `LLMClient.chat()`: `OllamaClient` (locale, `num_ctx=8192`, `think=False`), `ClaudeAPIClient` e `TogetherAIClient` (cloud), `FakeLLM` (test).
- I client cloud ricevono l'intera conversazione, compresi i risultati di `run_sql` (righe reali): oggi non esiste nessuna politica su cosa esce.
- `QueryResult` registra risposta, iterazioni, chiamate e risultati dei tool; NON registra `prompt_eval_count`/`prompt_eval_duration` di Ollama.
- Osservazione: `ClaudeAPIClient.chat()` riceve `temperature` ma non la passa a `messages.create` (letto nel codice; effetto reale da verificare).
- Non letto: l'interno di `ingest_engine` (forma esatta di `describe_table`, `ColumnSpec.sensitive`), l'harness dei batch e il formato dei report → da verificare.

---

## Cosa cambia in v2

1. **Router di tabelle (nuovo passo prima del loop).** `route(domanda) -> [tabelle con punteggio]`. Se il router è abbastanza sicuro, le descrizioni complete (`describe_table`) delle tabelle scelte vengono iniettate subito e le tabelle entrano in `described_tables`, così il gate passa senza giri in più. Sotto soglia: si torna esattamente al comportamento attuale (indice compatto + describe_table a richiesta).
2. **Backend del router intercambiabili** (A embeddings, B modello locale, C ibrido, D cloud opzionale), tutti dietro la stessa interfaccia, scelti da configurazione.
3. **Politica online/offline L0/L1/L2**: un unico punto nel codice decide cosa può lasciare la macchina prima di ogni chiamata a un client cloud (o a un router cloud).
4. **Misure**: ogni chiamata registra i token/tempi di prefill di Ollama; il router registra punteggi, backend, latenza, fallback.
5. **Banco di prova del routing** separato dal loop: ground truth dalle ~66 domande del reference Sonnet, metriche top-1/top-3/recall@k, permutazioni, distrattori sintetici.
6. **Invariati**: i 3 tool, sola lettura, limiti righe/tempo, gate describe_table, recupero chiamate malformate, `LLMClient`. Il router è un'aggiunta disattivabile (`router=None` = comportamento di oggi).
7. **Obiettivo hardware**: progettato per hardware migliore (Mac Mini o simile); le prove restano possibili su Pi (lento) o in sandbox.

---

## Interfaccia del router di tabelle

Firme proposte (solo libreria standard + `requests` già usato da `OllamaClient`; file nuovo previsto: `code/table_router.py`, da creare in un passo successivo).

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Sequence

@dataclass(frozen=True)
class TableCard:
    """Testo che descrive UNA tabella al router. Costruito da describe_table, mai dalle righe."""
    table: str
    domain: Optional[str]          # oggi TableSpec non ha `domain` (commento nel codice): None finché non esiste
    text: str                      # nome + colonne + semantic_note (vedi Politica: in L1 può uscire)
    content_hash: str              # sha256 di `text`, per la cache degli embeddings

@dataclass
class TableScore:
    table: str
    score: float                   # 0..1, più alto = più probabile che serva

@dataclass
class RoutingResult:
    ranked: List[TableScore]       # tutte le tabelle candidate, ordinate
    selected: List[str]            # quelle da iniettare (può essere vuota)
    confident: bool                # False -> fallback all'indice compatto attuale
    backend: str                   # "A_embed", "B_llm", "C_hybrid", "D_cloud", "baseline_kw"
    elapsed_ms: float
    notes: Dict[str, object] = field(default_factory=dict)   # es. token di prefill, permutazione usata

class TableRouter(Protocol):
    name: str
    is_remote: bool                # True se manda qualcosa fuori dalla macchina (solo D)
    def route(self, question: str, cards: Sequence[TableCard], k: int = 3) -> RoutingResult: ...

def build_table_cards(conn, tables: Optional[List[str]] = None) -> List[TableCard]: ...
def make_router(config: dict) -> Optional["TableRouter"]: ...   # legge la sezione "router" della config
```

Backend:

- **Baseline (in più, stdlib pura)**: sovrapposizione di parole domanda/scheda. Serve solo come riferimento minimo per capire se A/B/C valgono il costo.
- **A — `EmbeddingRouter(model: str, host: str, cache_path: Path)`**: embeddings locali delle schede (calcolati una volta, cache per `content_hash`) e della domanda; punteggio = similarità coseno riportata a 0..1. Endpoint Ollama per embeddings e modello da usare: da verificare sulla versione installata.
- **B — `LLMChoiceRouter(llm: LLMClient, max_tables: int)`**: il modello locale (es. qwen3.5:4b) riceve la domanda e la lista numerata delle schede e risponde con i numeri. Punteggio: se Ollama espone probabilità dei token, usarle (da verificare); altrimenti frequenza di scelta su N ripetizioni con ordine delle tabelle permutato (attenua anche l'effetto ordine).
- **C — `HybridRouter(shortlist: EmbeddingRouter, chooser: LLMChoiceRouter, shortlist_n: int = 10)`**: A riduce a ~10 candidate, B sceglie tra quelle. Utile quando le tabelle sono centinaia (B da solo non entra nel contesto).
- **D — `CloudRouter`** (opzionale, futuro): stessa interfaccia, `is_remote=True`, consentito solo con politica ≥ L1.

Integrazione in `run_query` (firma proposta, compatibile con oggi):

```python
def run_query(question: str, llm: LLMClient, max_iterations: int = MAX_ITERATIONS,
              router: Optional[TableRouter] = None,
              policy: Optional["PrivacyPolicy"] = None) -> QueryResult: ...
```

- Se `router` c'è e `result.confident`: le uscite di `describe_table` delle tabelle `selected` vanno nel system prompt in un blocco "TABELLE PROBABILMENTE RILEVANTI" (scelta provvisoria: system prompt, non finte chiamate tool) e si aggiungono a `described_tables`. L'indice compatto resta, così il modello può ancora usare altre tabelle (passando dal gate).
- `confident` = punteggio della prima ≥ soglia E distacco dalla successiva ≥ margine. Valori iniziali segnaposto, da calibrare sui dati del test (vedi Metriche).
- `QueryResult` guadagna campi: `routing: Optional[RoutingResult]`, `policy_level`, `redactions`, `llm_stats` (lista per chiamata).

---

## Politica online/offline

Livelli (dal todo, resi operativi):

| Livello | Cosa può uscire | Client/router permessi |
|---|---|---|
| **L0** offline | niente | solo `OllamaClient` su host locale, router A/B/C locali; `ClaudeAPIClient`/`TogetherAIClient`/router D rifiutati con errore chiaro prima della chiamata |
| **L1** descrizioni | domanda + schema (indice compatto, uscite di `describe_table`) | client cloud ammessi, ma i risultati di `run_sql` vengono sostituiti prima dell'invio da `{"columns": [...], "row_count": N, "rows": "[non inviate: politica L1]"}`; le righe vere restano solo in locale in `QueryResult.tool_results` |
| **L2** risultati | anche i risultati di `run_sql`, con colonne `sensitive=True` redatte | client cloud ammessi |

Dove vive la configurazione: un file `config.json` come proposto nel todo (esistenza e posizione nel repo da verificare), sezione proposta:

```json
{
  "privacy": {
    "level": "L0",
    "per_domain": {"money": "L0"},
    "redaction": "placeholder",
    "local_hosts": ["localhost", "127.0.0.1"]
  },
  "router": {"backend": "none", "k": 3, "threshold": 0.6, "margin": 0.1}
}
```

Regole:
- **File mancante o illeggibile → L0** (si chiude, non si apre). Il livello per dominio può solo ABBASSARE quello globale, mai alzarlo. Granularità per colonna = il flag `sensitive` già presente in `ColumnSpec` (secondo il todo; da verificare in `ingest_engine`).
- **Un solo punto di controllo**: `apply_outbound_policy(messages, client, policy) -> (messages_da_inviare, redazioni)` chiamato in `run_query` prima di ogni `llm.chat` quando `client.is_remote` è True. Ogni `LLMClient` dichiara `is_remote`; `OllamaClient` è remoto se l'host non è in `local_hosts` (scelta provvisoria).
- **Redazione in L2**: i nomi delle colonne di un risultato sono quelli di `cursor.description`, cioè possono essere alias o espressioni (`SELECT controparte AS c`). La libreria standard Python non espone l'origine di una colonna risultato (da verificare). Regola prudente: per ogni tabella toccata dalla query che ha colonne sensibili, si redige ogni colonna risultato che (a) ha il nome di una colonna sensibile, oppure (b) non corrisponde esattamente a una colonna NON sensibile nota (alias/espressioni → redatte per default). Aggregati numerici puri (`COUNT(*)`, `SUM(importo)`) sono ammessi solo se il nome è riconoscibile; altrimenti redatti. Meglio redigere troppo che troppo poco.
- **Forma della redazione** (default provvisorio): `"[REDATTO]"`. Alternativa: pseudonimo stabile per conversazione (`persona_01`), con la tabella di corrispondenza tenuta solo in locale, così il modello cloud può ancora raggruppare/contare e la risposta viene ri-identificata in locale.
- **Attenzione L1**: le `semantic_note` possono contenere valori letterali reali (la regola del §3 chiede di elencarli, es. nomi di istituti). Quindi "solo descrizioni" non vuol dire "nessun dato personale". Proposta: un campo per-colonna o una lista di colonne le cui note non escono in L1 (decisione di Leo).
- Ogni `QueryResult` registra `policy_level` e quante redazioni sono state fatte; un'eventuale chiamata rifiutata è un errore esplicito, mai un silenzioso passaggio al locale.

---

## Metriche e come misurarle

**Ground truth.** Dai report del reference Sonnet (~66 domande): per ogni domanda, tabelle in `describe_table` + tabelle estratte dalle query `run_sql` con la stessa `_extract_referenced_tables` (stessi punti ciechi: join con virgola, sottoquery profonde). Formato dei report da verificare. Il risultato va in un file di ground truth con, per ogni domanda, `tables_needed`, `origine`, `stato: bozza` e `rivisto_da_leo: false`; Leo toglie a mano le tabelle esplorate inutilmente. Nessuna riga di dati nel file, solo testo delle domande e nomi di tabelle.

Metriche del router (per backend):
- **top-1**: la prima tabella è tra quelle necessarie.
- **top-3**: almeno una necessaria nelle prime 3.
- **recall@k** (k=1,3,5): quota di domande in cui TUTTE le tabelle necessarie sono nelle prime k — la metrica chiave per le domande cross-domain.
- **Robustezza all'ordine**: 5 permutazioni casuali (seme fisso) dell'elenco tabelle per domanda; si misura la quota di domande con la stessa top-1 in tutte le permutazioni e la variazione media dei punteggi.
- **Degrado con distrattori**: si aggiungono schede sintetiche (nomi/colonne/note inventati, compresi quasi-duplicati come `transactions_archivio`) per simulare 50, 100, 200 domini; si traccia recall@3 al crescere del numero.
- **Calibrazione**: per fasce di punteggio, quota di scelte corrette; serve a fissare soglia e margine di `confident`. Si riporta anche la **quota di fallback** a una data soglia.
- **Costo**: latenza del router (ms) e, per B/C, `prompt_eval_count`/`prompt_eval_duration`.

Metriche end-to-end (batch con e senza router, stesso modello):
- iterazioni medie, numero di `describe_table` e di errori `describe_table_required`, `hit_max_iterations`, risposte vuote, tempo per domanda.
- **Cache del prefisso Ollama**: registrare `prompt_eval_count` e `prompt_eval_duration` dalla risposta di `/api/chat` per ogni chiamata (campi della risposta Ollama: presenza nella versione installata da verificare). Se la cache funziona, dalla seconda chiamata della stessa domanda il conteggio di prefill deve calare nettamente. Attenzione: iniettare le tabelle del router nel system prompt cambia il prefisso a ogni domanda → misurare se questo annulla la cache.

---

## Ordine di lavoro

Passi piccoli, ognuno verificabile da solo e reversibile:

1. **Misure Ollama**: aggiungere a `AssistantTurn` un campo opzionale di statistiche e salvarle in `QueryResult`. Nessun cambio di comportamento.
2. **Politica in sola registrazione**: `apply_outbound_policy` calcola cosa verrebbe redatto/bloccato e lo scrive nel `QueryResult`, ma non blocca ancora (così i batch Sonnet di riferimento continuano a funzionare).
3. **Ground truth**: script che legge i report Sonnet e produce il file di ground truth in bozza; revisione manuale di Leo.
4. **Schede tabelle + distrattori sintetici**: `build_table_cards` e generatore di schede finte.
5. **Interfaccia `TableRouter` + baseline a parole chiave + banco di prova** con tutte le metriche (prima su FakeLLM/baseline, nessun modello).
6. **Backend A** (embeddings locali) e confronto con la baseline.
7. **Backend B** (scelta del modello locale) con permutazioni.
8. **Backend C** (ibrido) solo se A e B hanno punti deboli diversi.
9. **Calibrazione** di soglia e margine sul banco di prova.
10. **Integrazione in `run_query`** dietro `router=None` di default; batch A/B con e senza router.
11. **Attivare la politica** (dopo decisione di Leo sul default): L0 di default per l'uso normale, livello esplicito per i batch cloud.

---

## Dubbi aperti per Leo

1. Livello predefinito quando non si dice nulla: L0 (sicuro, ma i batch Sonnet vanno avviati con un livello esplicito) o L2?
2. Granularità: livello globale + abbassamento per dominio + flag per colonna va bene, o basta il globale?
3. In L1 le `semantic_note` possono contenere valori reali: escono comunque, o si marcano le note da non inviare?
4. Redazione in L2: `[REDATTO]` semplice o pseudonimi stabili ri-identificati in locale?
5. Iniezione delle tabelle scelte: nel system prompt (cambia il prefisso, forse rompe la cache) o come finte chiamate `describe_table` nei messaggi?
6. Un Ollama su un altro computer della rete di casa (es. futuro Mac Mini) conta come locale o come remoto?
7. Con router sicuro, l'indice compatto completo resta nel prompt o si toglie per risparmiare token?
8. Il backend D (cloud tipo Jev) va tenuto nell'interfaccia o escluso del tutto per ora?
9. Da verificare insieme: `ClaudeAPIClient` ignora il parametro `temperature` (non lo passa all'API) — è voluto?
