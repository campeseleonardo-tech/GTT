# Rapporto sull'attività TL06-risposta1

## Cosa ho fatto
Ho verificato la sezione CLI (manual smoke-check) del file `code/llm_bridge.py` per confermare se stampa le misure prompt_eval, come richiesto nella domanda precedente TL06-log-ollama.

## Cosa ho controllato
Ho esaminato il blocco `if __name__ == "__main__":` e ho constatato che esso stampa:
- La domanda (Q: ...)
- La risposta (A: ...)
- Il numero di iterazioni e le chiamate agli strumenti
Non stampa le misure prompt_eval (disponibili in `result.llm_calls` ma non utilizzate nel CLI).

## Scelte
Non ho effettuato alcuna scelta perché non è stata necessaria alcuna modifica: il comportamento attuale è già conforme alla decisione di Leo (B: niente, solo nei dati).

## Cose da decidere o revisionare da parte di Leo
Nessuna. Il CLI già non stampa le misure prompt_eval, quindi non è richiesta alcuna azione.
