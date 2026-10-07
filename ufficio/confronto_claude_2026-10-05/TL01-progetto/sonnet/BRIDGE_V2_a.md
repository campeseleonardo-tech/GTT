# Bridge v2 — progetto del router di tabelle e della politica online/offline

Origine: `docs/todo_table_routing_test.md` (2026-09-29) e lettura di `code/llm_bridge.py`.
Stato: bozza (origine: agente TL01-progetto-a). Nessun codice scritto, nessuna misura eseguita: tutti i numeri citati vengono dai commenti del codice o dal TODO. Quello che non ho visto nel codice è marcato "da verificare".
Dati di esempio: solo sintetici (nomi di tabella come `tabella_a`, domande inventate).

## Come funziona oggi

1. `run_query(question, llm, max_iterations=8)` costruisce `messages` = system prompt + domanda e fa un ciclo di al massimo `MAX_ITERATIONS = 8` giri.
2. Il system prompt (`build_system_prompt()`) contiene un indice compatto di TUTTE le tabelle: row_count, nomi e tipi SQL delle colonne, foreign_keys, colonna timestamp canonica. Niente `semantic_note`.
3. Tre tool: `list_tables`, `describe_table(table)`, `run_sql(query)`. Il DB è aperto in sola lettura (`mode=ro`), con limite righe `SQL_ROW_LIMIT = 200` e timeout `SQL_TIMEOUT_SECONDS = 10.0`.
4. Gate nel codice: un `run_sql` che cita (via regex FROM/JOIN, `_extract_referenced_tables`) una tabella non ancora in `described_tables` viene respinto con errore `describe_table_required`. Costo: un giro in più per ogni tabella nuova.
5. Altre protezioni: chiamata identica ripetuta di seguito = nota senza riesecuzione; recupero di tool call malformate scritte come testo (`_try_parse_malformed_tool_call`); se si esaurisce il limite giri, risposta parziale costruita da Python con l'ultimo risultato.
6. Backend dietro l'interfaccia `LLMClient.chat(messages, tools, temperature) -> AssistantTurn`: `OllamaClient` (default `llama3.2:3b`, `num_ctx=8192`, `think=False`), `ClaudeAPIClient`, `TogetherAIClient`, `FakeLLM` (test).
7. Con `ClaudeAPIClient` e `TogetherAIClient` l'intera conversazione, righe reali dei risultati SQL comprese, parte verso il cloud: non esiste nessuna policy o redazione (nel codice letto non ne ho viste).
8. `QueryResult` registra risposta, giri, `tool_calls_made`, `tool_results`, `hit_max_iterations`, recuperi malformati. Non registra tempi, `prompt_eval_count` né `prompt_eval_duration` (il TODO lo conferma).
9. Il flag `sensitive` esiste per colonna (citato nei commenti di `_compact_schema_entry`, che lo scarta dall'indice); la definizione di `ColumnSpec` sta in `ingest_engine.py`, che non ho letto: da verificare.
10. Non ho visto nessun file `config.json` letto da `llm_bridge.py`: da verificare se esiste altrove.

## Cosa cambia in v2

- **Nuovo passo `route(question)` prima del ciclo**: restituisce le tabelle probabili con un punteggio. Se la confidenza è sopra soglia, le descrizioni di quelle tabelle vengono iniettate subito nei `messages` e le tabelle entrano in `described_tables`, così il gate passa senza giri di `describe_table`. Obiettivo: meno round-trip.
- **Fallback**: sotto soglia (o router in errore) si comporta come oggi, con l'indice compatto completo. Il router non può mai peggiorare la v1 oltre il suo costo: se sbaglia con alta confidenza il modello vede comunque il tool `describe_table` e può chiamarlo da sé (da verificare in test che lo faccia, vedi metriche).
- **Politica online/offline** a tre livelli (L0/L1/L2) applicata in un unico punto, tra il ciclo e i backend cloud, con redazione delle colonne `sensitive=True`.
- **Strumentazione**: ogni chiamata Ollama registra `prompt_eval_count`, `prompt_eval_duration`, `eval_count`, durata totale; `QueryResult` guadagna campi di routing (tabelle suggerite, confidenza, backend, se il fallback è scattato).
- **Pensato per hardware migliore** (decisione di Leo, 2026-09-29): nessuna scelta di design dipende dal Pi. Le prove restano sul Pi o in sandbox.
- **Non cambia**: i tre tool, il gate, le guardie SQL, `LLMClient`, un unico `vault.db`. Il router è additivo e spegnibile (`router = None` = comportamento v1).

## Interfaccia del router di tabelle

Solo firme e dataclass, libreria standard. I backend sono intercambiabili come i client LLM: stesso protocollo, scelta da configurazione.

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, Sequence

@dataclass
class TableDoc:
    name: str
    description: str          # dalle semantic_note / descrizioni della tabella
    column_names: List[str]
    domain: Optional[str] = None   # da verificare: oggi TableSpec non ha il campo domain

@dataclass
class RouteResult:
    tables: List[str]              # ordinate per rilevanza, al massimo k
    scores: Dict[str, float]       # 0..1, stessa scala per tutti i backend
    confidence: float              # confidenza complessiva 0..1
    backend: str                   # "A" | "B" | "C" | "none"
    latency_ms: float = 0.0
    sent_off_machine: bool = False # True solo se il backend ha usato un servizio esterno

class TableRouter(Protocol):
    name: str
    def prepare(self, docs: Sequence[TableDoc]) -> None: ...      # indici/embedding una tantum
    def route(self, question: str, docs: Sequence[TableDoc], k: int = 3) -> RouteResult: ...

class EmbeddingRouter:        # backend A: embeddings locali su descrizioni tabelle
    def __init__(self, embed_fn, model: str = "da_scegliere"): ...

class LLMChoiceRouter:        # backend B: modello locale, scelta tra le tabelle
    def __init__(self, client: "LLMClient", shuffle: bool = True, seed: int = 0): ...

class HybridRouter:           # backend C: A preseleziona N candidate, B sceglie tra quelle
    def __init__(self, a: TableRouter, b: TableRouter, n_candidates: int = 8): ...

def build_router(cfg: Dict) -> Optional[TableRouter]: ...        # legge la sezione "router" della config

def apply_route(result: RouteResult, threshold: float,
                messages: list, described_tables: set) -> bool:
    """Se confidence >= threshold: aggiunge i describe_table delle tabelle
    suggerite a messages, le aggiunge a described_tables, ritorna True.
    Altrimenti ritorna False (fallback all'indice compatto)."""
```

Note di progetto:
- Backend A: embedding calcolati una volta per tabella (`prepare`) e salvati su disco; la domanda si confronta per coseno (calcolo con sola libreria standard, o numpy se già presente: da verificare). La scelta del modello di embedding è aperta.
- Backend B: nel prompt le tabelle compaiono in ordine casuale (seed registrato), perché l'articolo di origine mostra che l'ordine sposta le probabilità. Output richiesto: JSON con al massimo k nomi, validati contro `ingest_engine.list_tables()`; nomi inesistenti scartati.
- Backend C: A riduce 50-200 candidati a pochi, B sceglie tra quelli; confidenza = combinazione dichiarata e loggata.
- Backend D (cloud tipo Jev): fuori ambito, solo posto nel protocollo; richiederebbe L1 o superiore e imposterebbe `sent_off_machine=True`.
- Lo stesso router vale per domande cross-domain: restituisce più tabelle; conta il recall@k, non solo il top-1.
- Il router vede solo descrizioni e nomi di colonne: mai righe di dati. Le colonne `sensitive=True` hanno nomi e note visibili al router locale; per i backend online vale la politica sotto.

## Politica online/offline

Principio: l'uscita di dati dal computer è una scelta esplicita, mai un effetto collaterale della scelta del backend.

| Livello | Cosa può uscire | Backend consentiti |
|---|---|---|
| L0 (default) | niente | solo locali (Ollama, router A/B/C locali) |
| L1 | domanda dell'utente + descrizioni delle tabelle (nomi, colonne, note) | anche cloud, ma i risultati di `run_sql` NON tornano al cloud: vedi nota sotto |
| L2 | anche i risultati delle query (righe), con redazione delle colonne `sensitive=True` | anche cloud con ciclo completo |

Nota su L1 e ciclo agentico: nel ciclo attuale il modello cloud vede i risultati per decidere il passo successivo. In L1 quindi un modello cloud può fare solo routing/generazione di SQL, mentre l'esecuzione e la risposta restano locali. Il disegno completo di questo caso è un dubbio aperto (vedi sotto).

**Dove vive la configurazione**: un file `config.json` (come proposto dal TODO), letto una sola volta all'avvio da una funzione `load_policy()`. Proposta di struttura, da verificare contro eventuali file esistenti:

```json
{
  "policy": {
    "level": "L0",
    "per_domain": { "dominio_x": "L0" },
    "sensitive_mode": "redact"
  },
  "router": { "backend": "A", "threshold": 0.6, "k": 3 }
}
```

Regola di sicurezza: se il livello manca o il file non si legge, vale L0. Un livello per dominio può solo ABBASSARE quello globale, mai alzarlo. Il livello effettivo è mostrato all'avvio e salvato in ogni `QueryResult`.

**Dove si applica**: un wrapper `PolicyGate` che avvolge qualsiasi `LLMClient` cloud. `ClaudeAPIClient.chat` e `TogetherAIClient.chat` oggi ricevono `messages` interi; il wrapper filtra i `messages` prima della chiamata, senza toccare gli altri backend. Un client cloud costruito senza livello adeguato rifiuta di partire (errore chiaro), invece di mandare dati.

**Redazione delle colonne `sensitive=True`** (L2):
1. Si ricava l'insieme delle colonne sensibili da `describe_table` (campo `sensitive` per colonna: presenza nell'output da verificare).
2. In `tool_run_sql` il risultato locale resta completo (serve alla risposta locale e al log). Una copia redatta viene costruita per i `messages` destinati al cloud: valore sostituito da `"[redatto]"` per le colonne sensibili.
3. Limite noto: la redazione per nome di colonna funziona con `SELECT colonna`, ma può essere aggirata da alias (`SELECT colonna_sensibile AS x`), espressioni o `SELECT *` con join. Mitigazioni proposte: (a) in L2 la query viene riscritta/rifiutata se cita una colonna sensibile fuori da un aggregato; oppure (b) si usa `sqlite3.Connection.set_authorizer` per intercettare la lettura delle colonne sensibili a livello di motore (da verificare che regga con le viste e i join usati). Preferenza: (b), perché è applicato da SQLite e non da regex, nello stesso spirito delle guardie di sola lettura già presenti.
4. I testi liberi (campi non marcati) possono contenere dati personali: la redazione copre solo ciò che è marcato; la qualità della marcatura diventa quindi un requisito per L2.

**Cosa resta vero anche in L0**: i log locali (`QueryResult`, batch report) non escono.

## Metriche e come misurarle

Ground truth: i report del reference Sonnet (~66 domande). Per ogni domanda le tabelle "giuste" sono quelle toccate da `run_sql`/`describe_table` in `tool_calls_made`, poi riviste a mano dove Sonnet ha esplorato tabelle non necessarie (il file rivisto è l'etichetta ufficiale; la revisione tocca a Leo, vedi dubbi). Il formato dei report non l'ho visto: da verificare. Non servono dati reali: il test usa solo domande e nomi di tabella.

Metriche (stesso dataset per A, B, C):
- **top-1**: la prima tabella suggerita è tra quelle giuste.
- **top-3**: almeno una tabella giusta nelle prime 3.
- **recall@k**: TUTTE le tabelle giuste nelle prime k (decisivo per le domande cross-domain); riportata per k = 1, 3, 5.
- **robustezza all'ordine**: stesse domande con N permutazioni casuali dell'ordine delle tabelle (es. N = 10, seed fissi); misura = quota di domande con la stessa top-1 in tutte le permutazioni e variazione media dello score.
- **degrado con distrattori**: si aggiungono 50, 100, 200 tabelle sintetiche (nomi e descrizioni plausibili ma inventate, ad esempio `tabella_dominio_017`) e si ripetono top-1/recall@3. Curva metrica vs numero di tabelle.
- **calibrazione della soglia**: per diverse soglie, quota di domande instradate (sopra soglia) e accuratezza su quelle; scegliere la soglia che dà alta precisione con copertura accettabile.
- **effetto sul ciclo** (misura end-to-end, a parità di modello): numero medio di giri, numero di chiamate `describe_table`, quota di `hit_max_iterations`, quota risposte corrette contro il reference, latenza media per domanda. Confronto router attivo vs v1.
- **errori del router ad alta confidenza**: conteggio e analisi a mano (sono quelli che fanno più danno).
- **Prefix cache di Ollama** (spunto non legato al cloud): registrare per ogni chiamata `prompt_eval_count`, `prompt_eval_duration`, `eval_count`, `total_duration` (campi della risposta di `/api/chat`: presenza e nomi da verificare sulla versione di Ollama in uso). Ipotesi da verificare: dalla seconda chiamata della stessa conversazione `prompt_eval_count` cala se la cache del prefisso funziona. Va misurato con system prompt identico tra domande diverse.
- **Dove si scrivono**: un file di report batch per modello/backend, con seed e versione di config; nessuna riga di dati reali.

Confronto chiave: A e B hanno costi diversi (A veloce e senza generazione, B più flessibile ma lento sul Pi); C è giustificato solo se batte entrambi in recall@3 sui distrattori.

## Ordine di lavoro

Passi piccoli, ciascuno con un risultato verificabile. Primi due senza alcun effetto sul comportamento.

1. **Strumentazione**: registrare `prompt_eval_count`/`prompt_eval_duration`/durata in `OllamaClient.chat` e portarli in `QueryResult`. Nessun cambio di comportamento.
2. **Dataset di valutazione**: ricavare dai report del reference l'elenco domanda -> tabelle giuste; Leo rivede a mano le tabelle superflue.
3. **Banco di prova del router** (script separato, non dentro `run_query`): interfaccia `TableRouter` + `TableDoc` e metriche (top-1, top-3, recall@k) con un router banale di riferimento (es. corrispondenza di parole chiave) per avere una base di confronto.
4. **Backend A** (embeddings locali) e prime misure, compresi distrattori e permutazioni dove applicabili.
5. **Backend B** (modello locale, scelta singola con ordine casuale) e confronto con A.
6. **Backend C** (ibrido) solo se A e B mostrano punti di forza complementari.
7. **Integrazione nel ciclo**: `apply_route` prima del ciclo, dietro un flag di config (spento di default); misura end-to-end contro v1 su un sottoinsieme di domande.
8. **Politica L0/L1/L2**: `load_policy()`, `PolicyGate` sui client cloud, default L0, test con `FakeLLM` (verifica che in L0 non parta nessuna chiamata cloud).
9. **Redazione `sensitive=True`**: prima per colonne in uscita, poi l'authorizer di SQLite se i test sintetici mostrano che alias e join aggirano la prima versione.
10. **Revisione finale**: aggiornare la sezione "Come funziona oggi" e il foglio di progetto (modifiche proposte nel rapporto), spostare la cronologia dei test in `EVOLUTION_LOG.md`.

Regola per ogni passo: provare su copie, mai sull'originale; nessun dato personale reale nei test.

## Dubbi aperti per Leo

1. **Livello L1 con modello cloud**: in L1 non tornano i risultati al cloud, quindi il cloud può solo fare routing o scrivere SQL. Va bene limitare L1 a "routing online + esecuzione locale", oppure L1 non ti serve e bastano L0/L2?
2. **Granularità della policy**: globale / per dominio / per colonna. Proposta: globale con abbassamento per dominio, più colonne `sensitive` per L2. Basta, o vuoi anche la scelta per colonna?
3. **Config**: `config.json` esiste già nel progetto, o lo creo nuovo? (Non l'ho visto in `llm_bridge.py`.)
4. **Redazione colonne sensibili**: preferisci il blocco a livello di motore SQLite (più robusto, più lavoro) o la sostituzione dei valori nel risultato (più semplice, aggirabile con alias)?
5. **Etichette di valutazione**: chi rivede le tabelle "superflue" del reference Sonnet, e quanto ti pesa farlo a mano (~66 domande)?
6. **Soglia di confidenza**: preferisci poche scorciatoie ma molto sicure (soglia alta) o più risparmio di giri accettando qualche errore da fallback del modello?
7. **Campo `domain` su `TableSpec`**: oggi non esiste. Serve per un indice a due livelli e per la policy per dominio; lo aggiungiamo (tocca lo schema, quindi decisione tua) o lo rimandiamo?
8. **Modello di embedding per il backend A**: non scelto. Hai preferenze o vincoli (solo locale, spazio, lingua italiana)?
