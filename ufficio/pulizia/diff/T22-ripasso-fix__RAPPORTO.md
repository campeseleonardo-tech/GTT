# Rapporto T22-ripasso-fix

origine: agente T22-ripasso-fix
stato: bozza

## Cosa ho fatto
Rilettura di `web/app.js` funzione per funzione, più controllo di `web/index.html` e `web/style.css`. Corretti 4 bug in `web/app.js`, con commento `// [agente T22]`. Non ho aggiunto funzioni né cambiato gli stili.

## Bug trovati (funzione, effetto, esito)
1. `caricaDebiti`: `volte` poteva diventare 0 con dati locali rovinati; ora è tenuto almeno a 1. Fatto.
2. `salva`: l'avviso di salvataggio non teneva conto del salvataggio dei debiti; ora si mostra anche se quel salvataggio fallisce. Fatto.
3. `creaSessioneRipasso.rimuoviDebitoCorrente`: dopo aver eliminato un debito, la barra "Rimasti" non si aggiornava; ora aggiorna il testo. Fatto.
4. `apriSottomenuRipasso`: il focus non finiva sulla prima voce disponibile del sottomenu; ora la cerca tra i tre pulsanti abilitati. Fatto.

## Come provarlo
Apri `web/index.html` nel browser. Clicca sulla scheda "Der, die o das?", scegli un articolo sbagliato, poi clicca "← Torna alla home". La scheda "Ripasso" deve mostrare 1 errore da ripassare. Clicca "Ripasso", poi "Ripasso Articoli"; rispondi correttamente e premi "Avanti →": dovresti tornare alla home con il contatore a 0. Per le frasi e gli errori ripeti lo stesso: crea prima uno sbaglio nel gioco normale, poi apri la voce di ripasso corrispondente e rispondi bene.
