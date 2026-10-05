# Rapporto T20-esegui-a

## Cosa è stato fatto
- Implementato il sistema di "Ripasso degli sbagli" come da scelta T19-scelta.
- Aggiunte funzioni per gestire i debiti (aggiunta, rimozione, caricamento/salvataggio in localStorage sotto chiave `langue_debiti_v1`).
- Modificato i tre giochi per registrare un debito quando l'utente risponde sbagliato o chiede la soluzione.
- Creato una modalità di ripasso generale che presenta tutti i debiti raccolti, ordinati per frequenza di errore, e rimuove un debito alla risposta corretta.
- Aggiunto un nuovo pulsante in home "Ripasso (n)" che avvia la sessione di ripasso.
- Aggiornato l'home per mostrare il totale dei debiti e abilitare/disabilitare il pulsante.
- Tutti i cambiamenti sono limitati a `web/index.html`, `web/app.js`, `web/style.css` (nessuna modifica allo stile necessaria).
- Ogni nuova o modificata riga è marcata con commento `[agente T20-esegui-a]`.

## Scelte fatte (default)
- Il ripasso mostra tutti i debiti indipendentemente dal livello (come richiesto).
- Il limite massimo di debiti per gioco è 50; i debiti più vecchi (con minor conteggio) vengono scartati quando si supera il limite.
- La sessione di ripasso generale mescola i debiti di tutti i giochi e seleziona casualmente con peso proporzionale al numero di errori (più errori = più probabilità di essere mostrato).
- Quando il pulsante "Ripasso" è cliccato e non ci sono debiti, viene mostrato un messaggio "Nessun debito da ripassare" e si ritorna alla home dopo 1,5 secondi.
- Il contatore accanto al pulsante mostra il totale dei debiti (es. "12 da ripassare").

## Cosa deve verificare Leo
1. Assicurarsi di avere qualche contenuto nei giochi (articoli, frasi, errori) – ad esempio usando i dati già presenti.
2. Giocare a uno dei tre giochi e dare volontariamente alcune risposte sbagliate (o cliccare "Mostra la soluzione").
3. Dopo ogni risposta sbagliata, verificare che il numero accanto al pulsante "Ripasso" aumenti di 1.
4. Cliccare sul pulsante "Ripasso (n)" e verificare che si avvii una sessione che presenta l'ultimo errore fatto.
5. Nella sessione di ripasso, rispondere correttamente: il debito deve scomparire e il contatore in home deve diminuire.
6. Ripetere lo stesso errore più volte: il relativo debito deve salire in cima alla lista (più probabilità di essere selezionato) e il suo contatore interno aumentare.
7. Continuare fino a esaurire tutti i debiti: dovrebbe apparire il messaggio di completamento e ritorno alla home.
8. Ricaricare la pagina: i debiti devono persistere (salvati in localStorage).

## Note
- Non sono stati modificati i file di contenuto (data.js, JSON sotto contenuti/).
- Lo stile non è stato alterato perché le nuove schede ereditano già le regole esistenti.
