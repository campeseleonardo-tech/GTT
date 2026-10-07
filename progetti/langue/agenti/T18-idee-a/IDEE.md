## Problemi che vedo nel codice attuale (bugs or fragile points you can actually point to: quote the function name)
- Nella funzione `disponibili` per il gioco 'frasi', il controllo `r.blocchi.length > 1` è troppo permissivo rispetto allo schema che richiede 4-9 elementi; potrebbe permettere record non validi se presenti nei dati.
- Nella funzione `eUsabile`, se un record mancasse del campo `stato` (obbligatorio per schema), verrebbe considerato utilizzabile poiché `undefined !== 'da_verificare'` restituisce true, creando un rischio di inclusione di dati non verificati.
## Idee (8 ideas, ranked; each: problema, proposta, effetto per chi impara, difficolta' FACILE/MEDIO/DIFFICILE, file toccati)
1. Problema: La barra-serie mostra solo la migliore serie mai raggiunta, non quella corrente della sessione, limitando il feedback motivazionale immediato.  
   Proposta: Mostrare sia la serie corrente che quella migliore nella barra-serie (es. "Serie corrente: 3 · Migliore: 5").  
   Effetto per chi impara: Aumenta la motivazione e il senso di progresso durante la sessione di gioco, incoraggiando a mantenere la concentrazione.  
   Difficoltà: FACILE  
   File toccati: web/app.js  

2. Problema: Nel gioco degli articoli, dopo una risposta errata l'utente vede solo che la sua scelta è sbagliata (con ✗) ma non vede immediatamente l'articolo corretto associato alla parola, rallentando l'apprendimento.  
   Proposta: Dopo ogni risposta (corretta o errata), mostrare sotto la parola grande l'articolo corretto e la parola in tedesco, rafforzando l'associazione visiva.  
   Effetto per chi impara: Migliora la memorizzazione dell'articolo tramite ripetizione immediata e chiara della correzione.  
   Difficoltà: MEDIO  
   File toccati: web/app.js, web/style.css  

3. Problema: Nel gioco delle frasi, un ordine sbagliato genera solo un messaggio generico senza indicazioni su quali blocchi siano fuori posto, rendendo difficile l'autocorrezione.  
   Proposta: Dopo un tentativo fallito, evidenziare i blocchi nella posizione sbagliata (ad esempio con sfondo giallo chiaro) nella frase costruita o nei blocchi rimanenti.  
   Effetto per chi impara: Fornisce un feedback mirato che aiuta l'utente a comprendere gli errori di ordine e a correggerli più efficacemente.  
   Difficoltà: MEDIO  
   File toccati: web/app.js, web/style.css  

4. Problema: Cambiare il livello tramite i radio button durante un gioco non interrompe la sessione corrente, rischiando di utilizzare contenuti non filtrati sul nuovo livello finché non si torna alla home.  
   Proposta: Quando il livello cambia, se si è in vista di gioco, tornare automaticamente alla home per garantire coerenza con il nuovo filtro.  
   Effetto per chi impara: Evita confusione e assicura che i giochi siano sempre adeguati al livello selezionato dall'utente.  
   Difficoltà: FACILE  
   File toccati: web/app.js  

5. Problema: Le statistiche per gioco nella home mostrano solo i conteggi grezzi (giusti, sbagliati, serie migliore) senza una metrica immediata di precisione, rendendo difficile valutare la performance relativa.  
   Proposta: Aggiungere alla statistica di ogni gioco la percentuale di risposte giuste (es. "Giuste: 8 · Sbagliate: 2 · Serie migliore: 4 · Precisione: 80%").  
   Effetto per chi impara: Permette di identificare rapidamente i punti di forza e debolezza in ogni gioco, guidando lo studio mirato.  
   Difficoltà: FACILE  
   File toccati: web/app.js  

6. Problema: Nel gioco degli errori, dopo una risposta errata l'utente vede la frase corretta e la spiegazione, ma non la frase sbagliata che aveva scelto, rendendo difficile il confronto diretto per capire l'errore.  
   Proposta: Nella fase di feedback, mostrare entrambe le frasi (quella sbagliata scelta e quella corretta), evidenziando le differenze chiave nella spiegazione (ad esempio tramite grassetto sulle parole errate).  
   Effetto per chi impara: Rafforza l'apprendimento tramite il confronto esplicito tra errore e correzione, facilitando la comprensione interna della regola grammaticale.  
   Difficoltà: FACILE  
   File toccati: web/app.js  

7. Problema: Dopo aver azzerato i progressi, non c'è alcun feedback visivo che confermi l'avvenuto azzeramento oltre all'aggiornamento della home, lasciando l'utente incerto sull'esito dell'operazione.  
   Proposta: Dopo l'azzeramento riuscito, mostrare un messaggio temporaneo (es. "Progressi azzerati") vicino al pulsante per 2 secondi prima di scomparire.  
   Effetto per chi impara: Fornisce conferma visiva immediata dell'azione, migliorando l'usabilità e la fiducia nell'interfaccia.  
   Difficoltà: FACILE  
   File toccati: web/app.js, web/style.css  

8. Problema: La struttura delle intestazioni nella vista-gioco non è ottimale per l'accessibilità (es. h1 con tabindex=-1 senza chiaro ruolo, potenziale gerarchia non logica), riducendo l'efficacia per gli utenti di tecnologie assistive.  
   Proposta: Rivedere la vista-gioco per garantire una gerarchia di intestazioni chiara (h1 per titolo gioco, h2 per istruzioni, h3 per suggerimenti) e aggiungere etichette aria-label o aria-describedby dove necessario.  
   Effetto per chi impara: Migliora l'esperienza per gli utenti con disabilità visive o motorie, rendendo il sito più inclusivo e conforme alle buone pratiche di accessibilità.  
   Difficoltà: MEDIO  
   File toccati: web/index.html, web/app.js  
## La mia idea preferita e perche'
L'idea che preferisco è la **numero 2** (mostrare l'articolo corretto sotto la parola grande nel gioco degli articoli dopo ogni risposta) perché affronta direttamente un momento critico di apprendimento: l'associazione tra parola tedesca e articolo. Fornendo immediatamente la correzione visiva accanto allo stimolo (la parola stessa), si rafforza il legame mnemonico in modo efficace e non intrusivo. Inoltre, è relativamente semplice da implementare (modifiche localizzate in una funzione e aggiustamenti di stile) e ha un impatto significativo sulla qualità dell'apprendimento senza richiedere nuovi contenuti o modifiche strutturali al sito.
