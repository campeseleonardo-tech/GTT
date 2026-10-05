Abbiamo modificato il file code/llm_bridge.py come segue:
1. Aggiunto due campi opzionali alla classe AssistantTurn: ollama_prompt_eval_count (int) e ollama_prompt_eval_duration (float).
2. Nel metodo OllamaClient.chat, dopo aver ricevuto la risposta da Ollama, estraiamo i campi "prompt_eval_count" e "prompt_eval_duration" e li impostiamo nell'oggetto AssistantTurn restituito.
3. Aggiunto un campo ollama_metrics alla classe QueryResult: una lista di dizionari, ciascuno con le chiavi 'prompt_eval_count' e 'prompt_eval_duration' (valori possono essere None se il campo non è presente nella risposta).
4. Nella funzione run_query, abbiamo aggiunto una lista locale ollama_metrics_list. Ad ogni iterazione, dopo aver ottenuto il turno dal modello, estraiamo i due campi dall'oggetto turno e li aggiungiamo alla lista.
5. Questa lista viene poi passata al costo oggetto QueryResult (sia nel ritorno anticipato che nel ritorno finale).

Leo dovrebbe guardare il campo ollama_metrics dell'oggetto QueryResult restituito da run_query per vedere i valori di prompt_eval_count e prompt_eval_duration per ogni chiamata a Ollama effettuata durante il processing di una domanda.
