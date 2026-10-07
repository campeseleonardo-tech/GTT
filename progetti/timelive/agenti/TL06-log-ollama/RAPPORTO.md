# RAPPORTO — TL06-log-ollama

origine: agente TL06-log-ollama
stato: bozza

## Cosa ho fatto
Ho realizzato solo la parte "Altro spunto" di `docs/todo_table_routing_test.md`:
registrare, per ogni chiamata a Ollama, i campi `prompt_eval_count` e
`prompt_eval_duration` che la risposta di Ollama porta già (per capire se la
cache del prefisso del system prompt funziona davvero).

Tutto in `code/llm_bridge.py`, punti marchiati `# [agente TL06]`:
1. `AssistantTurn` (il risultato di una singola chiamata al modello) ha due
   nuovi campi: `prompt_eval_count` (token del prompt valutati) e
   `prompt_eval_duration` (nanosecondi).
2. `OllamaClient.chat()` li legge dalla risposta con `.get(...)`: se il
   campo non c'è, resta `None`. Nessun modo di rompere il loop.
3. `run_query()` aggiunge per ogni chiamata un rigo
   `{"iteration", "prompt_eval_count", "prompt_eval_duration"}`.
4. `QueryResult` (risultato finale di una domanda) ha il nuovo campo
   `llm_calls`, accanto a quelli già in uso (`tool_calls_made`,
   `tool_results`): stesse regole, stessi default.

I backend cloud (Claude, Together) e il FakeLLM lasciano i valori a `None`.
Nessun altro comportamento è cambiato: stesso loop, stessi tool, stessi limiti.

## Dove guardare i numeri
- In Python, dopo una domanda:
  ```
  from code.llm_bridge import run_query, OllamaClient
  r = run_query("Quante tabelle ci sono?", OllamaClient())
  for c in r.llm_calls:
      print(c)
  ```
- Come lettura per la cache: nella stessa domanda (o nello stesso batch),
  il prompt delle chiamate 2 e seguenti comincia uguale a quello della
  chiamata 1 (stesso system prompt, stesso inizio). Se la cache sta
  lavorando, `prompt_eval_count` e `prompt_eval_duration` delle chiamate
  successive dovrebbero essere più piccoli di quelli della prima.
- **da_verificare** (io non ho accesso al Pi né al server): il significato
  esatto di `prompt_eval_count` con la cache attiva può variare tra versioni
  di Ollama (alcune contano tutti i token del prompt, altre solo quelli non
  in cache). Prima di trarre conclusioni, controlla `ollama --version` e la
  documentazione della versione usata.

## Cosa ho controllato
- Ho riletto l'intero `code/llm_bridge.py` fornito: l'unico punto in cui la
  risposta di Ollama viene letta è `OllamaClient.chat()`; lì ho aggiunto i
  due `.get(...)`.
- Sicurezza: default ovunque (campos `None`/lista vuota), `.get()` al posto
  di indici diretti, `getattr` con default nel loop. Se un campo non c'è,
  il comportamento è identico a prima.

## Scelte (piccole, reversibili)
- Nome del campo: `llm_calls` (invece di "ollama_metrics"), per fare
  parallelo con `tool_calls_made` e restare valido anche per backend cloud.
- Durata lasciata in nanosecondi, come la invia Ollama (convertire:
  `valore / 1000000000`); coerenza con lo standard del progetto
  "unità esplicite, mai conversioni silenziose".
- Non ho toccato la stampa finale del CLI (`python code/llm_bridge.py ...`):
  i numeri si vedono in `result.llm_calls`. Vedi la domanda in DOMANDE.md.

## Da Leo / prossimi passi
- Il report batch (il file che genera i JSON dei risultati, NON dentro
  `llm_bridge.py` — da verificare quale sia) non include ancora `llm_calls`:
  servirebbe una riga in più in quel file. Indicalo e lo aggiungo.
- Suggerimento per il foglio (non l'ho toccato, è tuo): una riga in §2/§6
  del progetto sul fatto che il bridge ora riporta le metriche di prefill
  di Ollama in `QueryResult.llm_calls`.
