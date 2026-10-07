## Confronto
| Idea | Proposta da | Valore | Difficoltà |
|------|-------------|--------|------------|
| Mostrare l'articolo corretto sotto la parola grande dopo ogni risposta nel gioco articoli | agente T18-idee-a | Alto | MEDIO |
| Tracciamento per-item + modalità "Ripassa i tuoi errori" (debito per gioco) | agente T18-idee-b | Alto | MEDIO |
| "Ripasso degli sbagli" (lista dei debiti con rimozione al successo) | agente T18-idee-c | Alto | MEDIO |
| Aggiungere percentuale di risposte giuste alle statistiche della home | agente T18-idee-a | Medio | FACILE |
| Export/Import dei progressi tramite file JSON | agente T18-idee-b | Medio | FACILE |

## Scelta
**Ripasso degli sbagli (lista dei debiti)** – l'idea proposta da entrambi gli agenti T18-idee-b e T18-idee-c. Si aggiunge una chiave separata in `localStorage` (`langue_debiti_v1`) che registra, per ogni gioco, gli item su cui l'utente ha risposto male o ha rinunciato. Una nuova scheda in home "Ripasso (n)" apre una sessione che presenta solo quei debiti, ordinati per frequenza di errore; ogni risposta corretta rimuove l'item dal debito. Il tutto si realizza modificando solo `web/app.js`, `web/style.css` e `web/index.html`, senza aggiungere contenuti tedeschi.

## Brief per chi la realizza
1. **app.js – nuove funzioni di debito**  
   - Aggiungere le costanti `CHIAVE_DEBITI = 'langue_debiti_v1'`.  
   - Funzioni: `caricaDebiti(storage)`, `salvaDebiti(storage, debito)`, `aggiungiDebito(gioco, id)`, `rimuoviDebito(gioco, id)`, `getDebitiPerGioco(gioco)` (restituisce array di `{id, volte}` ordinato per `volte` decrescente, max 50 per gioco).  
   - In `avviaSito` leggere i debiti insieme ai progressi.  

2. **app.js – registrazione dei debiti**  
   - Nella funzione `rispondi` di `giocoArticoli`, dopo `sessione.registra(giusta)`, se `!giusta` chiamare `aggiungiDebito('articoli', corrente.id)`.  
   - Nella funzione `controllaClick` di `giocoFrasi`, se la risposta è sbagliata (il primo `else`), chiamare `aggiungiDebito('frasi', corrente.id)`.  
   - Nella funzione `mostraSoluzione` di `giocoFrasi`, sempre chiamare `aggiungiDebito('frasi', corrente.id)` (contare la rinuncia come errore).  
   - Nella funzione `rispondi` di `giocoErrori`, se `!scelta.corretta`, chiamare `aggiungiDebito('errori', corrente.id)`.  
   - Nella funzione `mostraSoluzione` di `giocoErrori` (non presente, ma analogamente se aggiunta) vale lo stesso principio.  

3. **app.js – sessione di ripasso**  
   - Creare funzione `creaSessioneRipasso(gioco, alProssimo)` simile a `creaSessione` ma che:  
     * prende il pool da `getDebitiPerGioco(gioco)` (array di oggetti con `id` e `voli`);  
     * per ogni `id` recupera il record originale da `window.LANGUE_DATA[gioco]` tramite ricerca per `id`;  
     * mostra la domanda usando i renderer esistenti (es. per articoli mostra la parola grande e i bottoni articolo).  
   - Quando l'utente risponde correttamente, chiamare `rimuoviDebito(gioco, id)` e aggiornare il conteggio in home.  
   - Se il pool di debiti è vuoto, mostrare un messaggio "Nessun debito da ripassare" e tornare alla home.  

4. **app.js – avvio ripasso dalla home**  
   - Aggiungere funzione `avviaRipasso(gioco)` che chiama `creaSessioneRipasso(gioco, prossimaRipasso)` dove `prossimaRipasso` richiama nuovamente `avviaRipasso` per lo stesso gioco finché ci sono debiti, oppure torna alla home quando finiti.  
   - Collegare il nuovo bottone della home (vedi punto 5) a `avviaRipasso` con il gioco corrispondente (`articoli`, `frasi` o `errori`).  

5. **index.html – nuova scheda in home**  
   - Dentro `<ul class="giochi">` aggiungere un nuovo `<li>` con id `gioca-ripasso` e classe `scheda`.  
   - All'interno: `<span class="scheda-titolo">Ripasso</span>`, `<span class="scheda-desc">Rispondi nuovamente agli errori</span>`, `<span class="scheda-conta" id="conta-ripasso"></span>`, `<span class="scheda-stat" id="stat-ripasso"></span>`.  
   - Aggiungere listener: `document.getElementById('gioca-ripasso').addEventListener('click', function() { avviaRipasso(progresso.livello); });` (il livello è già nel progresso, ma la sessione di ripasso ignora il filtro livello e usa tutti i debiti indipendentemente dal livello).  

6. **style.css – eventuale aggiustamento**  
   - Nessuna modifica obbligatoria; la nuova scheda eredita già le regole `.scheda`. Se si desidera evidenziarla, si può aggiungere una regola specifica per `#gioca-ripasso` (facoltativo).  

7. **Cosa NON modificare**  
   - Non toccare la struttura dei giochi esistenti (`giocoArticoli`, `giocoFrasi`, `giocoErrori`) oltre alle chiamate di aggiunta/rimozione debito.  
   - Non alterare l'oggetto `progresso` né le chiavi di `localStorage` usate per i progressi (`langue_progress_v1`).  
   - Non introdurre nuovi contenuti tedeschi; i debiti riutilizzano i record già presenti in `data.js`.  

8. **Come verificare**  
   - Dopo una risposta sbagliata (o dopo aver cliccato "Mostra la soluzione") verificare che il contatore accanto alla scheda "Ripasso" aumenti di 1.  
   - Cliccare su "Ripasso (n)" e confermare che la sessione presenti l'item appena sbagliato.  
   - Rispondere correttamente in quella sessione: l'item deve scomparire dal debito e il contatore diminuire.  
   - Continuare a sbagliare lo stesso item: il contatore delle volte (`voli`) deve aumentare e l'item rimanere più in alto nella lista.  
   - Assicurarsi che il numero massimo di debiti per gioco non superi 50 (più vecchi vengono scartati quando si aggiunge un nuovo debito oltre il limite).  

## Idee scartate e perche'
- **Mostrare l'articolo corretto dopo risposta** (idea-a #2): utile ma impatto inferiore rispetto a un sistema di ripasso mirato; inoltre richiede solo modifiche di stile e testo, mentre il ripasso offre un beneficio di lungo periodo.  
- **Tracciamento per-item + modalità "Ripassa i tuoi errori"** (idea-b #1): praticamente identico alla scelta, ma la proposta dell'agente c è più precisa sulla rimozione al successo e sul limite di 50 item; abbiamo adottato quella versione perché è più completa e già testata mentalmente.  
- **Aggiungere percentuale di risposte giuste alle statistiche** (idea-a #5): facile da fare, ma fornisce solo una metrica globale senza guidare l'utente su cosa ripassare.  
- **Export/Import dei progressi** (idea-b #4): utile per la portabilità dei dati, ma non influisce direttamente sull'apprendimento quotidiano; inoltre richiederebbe nuovi pulsanti e gestione di file, mentre il ripasso si ottiene con modifiche più locali e immediato beneficio.  
- Altre idee (navigazione tastiera, hint, service worker, obiettivo giornaliero, ecc.) sono state scartate perché o richiedono nuovi file fuori dalle allowed paths (es. service worker, manifest, test) o hanno un impatto didattico inferiore rispetto al ripasso mirato degli errori.
