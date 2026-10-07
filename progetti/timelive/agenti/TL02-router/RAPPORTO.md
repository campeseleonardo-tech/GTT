# Rapporto di lavoro - agente TL02-router

## Sommario
È stato creato il nuovo file `code/table_router.py` con le seguenti funzionalità:
- Implementazione di `KeywordBackend` per il ranking di tabelle tramite word-overlap/TF-IDF puro Python.
- Stub per `EmbeddingBackend` e `LocalLLMBackend` che sollevano `NotImplementedError` con messaggi esplicativi in italiano.
- Funzione `route(question, tables, backend, k)` che restituisce una lista ordinata di (nome_tabella, punteggio).
- Funzione di valutazione `evaluate(backend, cases, tables, k)` che calcola top1, top3 e recall@k.
- Funzione `shuffle_tables_evaluate` per testare la robustezza all'ordine delle tabelle tramite shuffling ripetuto.
- Auto-test sotto `if __name__ == "__main__"` utilizzando dati sintetici (tabelle e domande inventate) e stampa delle metriche.

## Scelte
- Per il `KeywordBackend` è stata scelta una tokenizzazione semplice basata su espressioni regolari, rimozione di stopword italiani e conteggio TF-IDF.
- Lo shuffle nei test di robustezza utilizza un seme fisso (42) per garantire ripetibilità.
- Nell'auto-test sono state create 12 domande sintetiche e 5 tabelle rappresentative di domini migrati (spotify, money, chess, apple health, whatsapp).
- Il valore di default per `k` in `route` è 3, come richiesto.

## Note
Il codice è stato scritto utilizzando solo la libreria standard Python, senza dipendenze esterne, come richiesto.
Gli stub per i backends basati su embedding e LLM locale sono pronti per essere implementati in futuro quando saranno disponibili i modelli Ollama necessari.
L'auto-test dimostra il funzionamento di base e fornisce un punto di partenza per ulteriori ottimizzazioni.

## Limitazioni
- Il `KeywordBackend` non considera sinonimi o variazioni morfologiche (es. plurale/singolare).
- La valutazione si basa su dati sintetici; le prestazioni su dati reali devono essere verificate.
- Gli stub non effettuano alcun controllo di connessione a Ollama; sollevano immediatamente `NotImplementedError`.
