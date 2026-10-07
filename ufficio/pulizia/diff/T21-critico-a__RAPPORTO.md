# Rapporto T21-critico-a

origine: agente T21-critico-a · stato: bozza

## Cosa ho fatto
- Letti: `agenti/T20-esegui-a/DIFF.patch`, `agenti/T19-scelta/SCELTA.md`, `web/app.js`.
- Scritto `agenti/T21-critico-a/CRITICA.md` con le 4 sezioni richieste (brief, errori, rischi, voto).

## Cosa ho controllato
- Lo scope delle 5 nuove funzioni di debito: `debito`, `storage` e `aggiornaHome` sono locali a `avviaSito`, non globali; le funzioni top-level `aggiungiDebito`/`rimuoviDebito`/`getDebitiPerGioco` li usano → `ReferenceError` al primo errore nei 3 giochi.
- Il punto esatto in cui il crash blocca l'UI (dopo `sessione.registra`, prima di `messaggio`/`mostraAvanti`).
- Le tre funzioni `giocoRipasso*` (mai chiamate, logica invertita o assente) e `avviaRipassoGenerale` (tipografia `currente`, ricorsione infinita `mostraFrase`→`disegnaFrase`, id non verificati, `corrente.testo_de` undefined, progressi non aggiornati).
- La scheda `gioca-ripasso` in `index.html` e l'aggiornamento del contatore in `aggiornaHome`.

## Scelte
- Nessuna modifica a file esistenti: task di sola critica.
- "Critico" interpretato come: un errore per voce con nome di funzione e riga del diff; niente elogi generici.

## Per Leo
- Il codice di T20 va rifiutato e rifatto: i 3 giochi si bloccano al primo errore e il ripasso non salva mai i debiti (scheda sempre disabilitata).
- Ambiguità del brief: punto 5 chiede una sola scheda, punto 4 chiede "il gioco corrispondente". Ho aperto una domanda in `DOMANDE.md` (misto vs per-gioco).
- Suggerimento (non applicato, appartiene a Leo): chiarire nel brief di T19 se il ripasso è misto o per-gioco, per evitare che il rifacimento ripeta la stessa deviazione.
