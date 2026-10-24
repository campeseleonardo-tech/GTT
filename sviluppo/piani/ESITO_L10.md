# Esito del giro L10 (24/10/2026): home e schede, ritocchi

Fatto, voce per voce (analisi critica 3.3-3.5, 3.8-3.11, 1.13; regole nel blocco L10 di PROMPT_LAVORI.md):

- **3.11 Limite visibile.** Sotto il numero grande di ogni scheda (`risultati.html`, funzione `limiteVisibile`) c'è una riga «Limite: …» con il primo dei limiti della scheda. La scelta la fa il codice, non a mano: i limiti di ogni scheda sono già ordinati dal più importante (il primo dell'elenco), quindi nessuna scheda è stata riordinata. Alcuni primi limiti sono lunghi (scheda 4, scheda 3): si accorciano nello script della scheda se Leo lo vuole.
- **3.9 Piè di pagina.** «Dati dal 09/10 al 22/10/2026» al posto di «Dati aggiornati al»: il periodo è il più largo fra i tre di `comuni.PERIODO`, scritto da `schede_risultati.py` in `data/schede_risultati.js` (`window.SCHEDE_PERIODO`), letto da `Sito.dataAggiornamento`. Vale su home, risultati e progetto, in italiano e in inglese.
- **3.10 Contatori.** Home e progetto calcolano i giorni con la stessa funzione `Sito.giorniRaccolta` (da `inizio_raccolta`, 3/10/2026, a oggi); i passaggi GPS vengono dallo stesso file (`contatore()` in `schede/home.py`). Prima il progetto contava dal primo all'ultimo giorno con dati.
- **3.5 Gara.** All'arrivo, accanto al mezzo più lento, compare il distacco scritto («+5 min», in grassetto sotto il suo tempo); vale anche per la versione senza movimento e per le 4 ore. Non compare se il distacco è sotto 1 minuto.
- **3.4 Barre.** La colonna del numero ha la stessa larghezza in tutte le righe di un grafico (e in tutti i gruppi dei grafici a gruppi): le tracce hanno la stessa lunghezza. Controllato nel DOM sulla scheda 4: una sola larghezza per grafico, nessun numero tagliato.
- **3.8 Cursore.** `input[type=range]{accent-color:var(--oro)}` in `assets/stile.css`.
- **3.3 Riquadri.** Tre per riga, con 5 riquadri 3 + 2 centrati (con 6: 3 + 3); 2 per riga sotto 980 px, 1 sotto 720 px.
- **1.13 Colori in `docs/METODO.md`.** La sezione «Colori» dice ora verde acqua → granata e blu → oro (stile «Torino»). Il grafico metro/prezzi era già stato tolto in L9.
- **«Condividi» e «copia il link».** Tolto il pulsante da `risultati.html` con il suo codice. `git grep` fuori da `sviluppo/` non trova più «Condividi», «Link copiato», «Copia questo link», `finCondividi`. Restano **solo** `copiaLink` e `costruisciLink` nella mappa (`mappa_torino.html`, `scripts/mappa_template.html`): le toglie L11, che riscrive la mappa.

## Controlli
pyflakes zero; `node --check assets/*.js` senza errori; `schede_risultati.py` senza ATTENZIONE; `prova_pagine.py --playwright` 0 errori su 20 pagine. Verifica nel DOM (server locale, senza guardare la grafica): limite visibile presente, piè di pagina col periodo, nessun «Condividi», «+5 min» nella gara della scheda 4, tracce uguali, riquadri a 2+2+1 centrati alla larghezza del riquadro del browser (a 3 colonne sui monitor larghi).
Non fatto: controllo grafico (lo fa Leo).
