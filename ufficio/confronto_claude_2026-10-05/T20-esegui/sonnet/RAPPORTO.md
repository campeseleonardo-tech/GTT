# Rapporto T20-esegui-a: Ripasso degli sbagli

Non ho potuto eseguire il sito: tutto quello che segue e' ragionato sul codice, non provato.

## Cosa ho cambiato
- **web/app.js**: nuove funzioni pure per la lista degli errori ("debiti"): `nuoviDebiti`, `sistemaDebiti`, `aggiungiDebito`, `rimuoviDebito`, `getDebitiPerGioco` (massimo 50 per gioco, i piu' vecchi si scartano; ordine: piu' sbagliati per primi). Salvataggio in una chiave separata `langue_debiti_v1` (`caricaDebiti`, `salvaDebiti`); la chiave dei progressi `langue_progress_v1` e l'oggetto `progresso` non sono stati toccati.
- **web/app.js**: nei tre giochi, ogni risposta sbagliata (o "Mostra la soluzione" nelle frasi) aggiunge il record alla lista. I tre giochi accettano ora un parametro `ripasso`; con `true` giocano solo gli errori da ripassare e una risposta giusta toglie il record dalla lista.
- **web/app.js**: `avviaRipasso()` fa il ripasso un gioco alla volta (parole, poi frasi, poi errori); quando non resta nulla torna alla home con il messaggio "Ripasso finito".
- **web/index.html**: nuova scheda "Ripasso" in home (con il numero tra parentesi e il dettaglio per gioco) e un messaggio di fine ripasso.
- **web/style.css**: solo un bordo tratteggiato per la scheda Ripasso.
- I tre pulsanti dei giochi ora usano funzioni anonime (altrimenti il click passava l'evento come "ripasso").
- Non ho toccato web/data.js ne' alcun contenuto. Tutto il codice nuovo o cambiato e' marcato `[agente T20-esegui-a]`.

## Cosa cliccare per provare
1. Apri `web/index.html`. La scheda "Ripasso" e' grigia con scritto "Nessun errore da ripassare".
2. Entra in "Der, die o das?" e sbaglia apposta un articolo. Torna alla home: la scheda diventa "Ripasso (1)" con "1 errore da ripassare" e "Parole: 1 · Frasi: 0 · Errori: 0".
3. In "Rimetti in ordine" clicca "Mostra la soluzione" e in "Trova l'errore" scegli la frase sbagliata: il numero sale a 3.
4. Clicca "Ripasso": il titolo e' "Ripasso: Der, die o das?" e compare la parola sbagliata. Rispondi giusto: la parola esce dalla lista. Passati tutti gli errori delle parole si passa alle frasi, poi agli errori.
5. Finiti tutti: ritorno alla home con "Ripasso finito: non hai piu' errori da ripassare. Bravo!" e la scheda di nuovo grigia.
6. Sbaglia ancora lo stesso item nel ripasso: resta nella lista e torna prima degli altri (conta quante volte e' stato sbagliato).
7. Chiudi e riapri la pagina: il numero della scheda Ripasso deve restare uguale (salvato nel browser).
8. "Azzera i progressi" ora azzera anche la lista del ripasso (il testo di conferma lo dice).
9. Prova anche i tre giochi normali dalla home: devono funzionare come prima.

## Scelte (default)
- Una sola scheda "Ripasso" per tutti i giochi (non tre), che passa da un gioco all'altro. Il brief parla di `avviaRipasso(gioco)` per gioco, ma indica anche un solo pulsante.
- Il ripasso ignora il filtro livello A1/A2.
- Nei tre giochi normali una risposta giusta NON toglie il record dalla lista: succede solo nel ripasso.
- Frasi: l'errore conta una volta per domanda (primo controllo sbagliato o rinuncia), come le statistiche. Nel ripasso la frase esce dalla lista solo se e' giusta al primo controllo.
- Le risposte date nel ripasso contano anche nelle statistiche e nella serie, come nei giochi normali.
- "Azzera i progressi" azzera anche la lista del ripasso.
- Gli item nella lista che non esistono piu' in data.js (o sono "da_verificare") non vengono contati ne' giocati.
- Ho scritto una piccola funzione `valido` che ripete le regole di `disponibili` senza filtro livello, per non modificare `disponibili`.

## Da controllare / da decidere
- **da_verificare**: non ho potuto vedere `web/data.js`. Il ripasso presuppone che ogni record abbia un campo `id` testuale (come da SCHEMA.md). Se manca, gli errori non vengono salvati e la scheda resta a 0.
- Il brief usa il nome "voli" in un punto: ho usato `volte` (refuso).
- Suggerimento per PROGETTO.md (e' tuo, non l'ho toccato): aggiungere "Ripasso degli sbagli" tra le funzioni del sito.
- Domande a risposta chiusa in `agenti/T20-esegui-a/DOMANDE.md`.
