origine: agente T18-idee-c · stato: bozza

# Idee per Langue (T18-idee-c)

Letto senza eseguire nulla: PROGETTO.md, SCHEMA.md, web/index.html, web/app.js, web/style.css.
Tutte le idee sono fattibili con HTML/CSS/JS puro: niente server, niente librerie, niente nuovo contenuto tedesco (i record restano in `data.js`, gestiti altrove).

## Problemi che vedo nel codice attuale

1. **Pool vuoto → crash latente in `prossima()`** (`giocoArticoli` e `giocoErrori`): se `disponibili()` restituisse una lista vuota, `scegliCasuale` restituisce `null` e `corrente.parola` fa `TypeError`. Oggi la protegge solo `btn.disabled` impostato in `aggiornaHome()`; un link che salta la home o una modifica al filtro lo renderebbe un crash reale.
2. **`disponibili()` non verifica la coerenza dei record**: per `frasi` non controlla che `r.blocchi` uniti diano `r.testo_de` (né che `traduzione_it` esista, che verrebbe stampato come `undefined` nel suggerimento); un refuso in `data.js` crea una domanda mai risolvibile, perché `controllaOrdine` confronta solo contro `testo_de` + `alternative`. Lo stesso per `articoli`: manca il controllo di `traduzione_it`. Il controllo esiste solo nel validatore dei contenuti, non a runtime.
3. **`mostraSoluzione()` conta come "sbagliato"**: se la domanda non era già stata conteggiata, guardare la soluzione fa crescere `sbagliati`; la home non distingue "errore" da "rinuncia".
4. **`disegna()` con `chiusa = true`**: dopo "Mostra la soluzione", i bottoni in `rimasti` restano visivamente attivi (un click non fa nulla perché `metti()` controlla `chiusa`): bottoni morti che sembrano vivi.
5. **Fallback di `ordineMescolato()`**: se con molti blocchi identici tutti i 20 tentativi di mescolamento coincidono con l'ordine giusto, la rotazione di riserva può comunque restituire l'ordine originale → frase "mescolata" già corretta.
6. **`avviso-dati` ambiguo**: si mostra anche quando `data.js` c'è ma `window.LANGUE_DATA` ha una forma sbagliata (le tre liste restano vuote per il default `[]` di `avviaSito`), col messaggio che incrimina solo il file mancante.
7. **Piccole accessibilità**: in `giocoFrasi` i bottoni in `rimasti` non hanno `aria-label` (quelli in `costruita` ce l'hanno); gli aggiornamenti di `barra-serie` non sono annunciati (solo `messaggio` ha `role="status"`).

## Idee

Raggruppate per impatto sull'apprendimento; idea 1 = quella che farei prima.

1. **"Ripasso degli sbagli" (lista dei debiti)**
   - Problema: `scegliCasuale` pesca dall'intero pool: le parole su cui incarti (es. *der Hund*) possono non ripresentarsi per molto; l'apprendimento richiede la ripetizione del proprio errore.
   - Proposta: a ogni risposta sbagliata o rinuncia si aggiunge `{gioco, id, volte}` in una chiave separata di localStorage (`langue_debiti_v1`, senza toccare `langue_progress_v1`). Nuova scheda in home "Ripasso (n)" che apre una sessione (ciclo riusa `creaSessione`) con quei soli record, ordinati per `volte` decrescente; a risposta giusta l'item viene rimosso. Tetto: 50 item per gioco.
   - Effetto per chi impara: ogni sbaglio viene "ripagato"; gli errori ricorrenti tornano fino a che non sono saldi — ripetizione spaziata in versione minimal.
   - Difficolta': MEDIO
   - File toccati: web/app.js (gestione debiti + sessione + scheda), web/index.html (scheda), web/style.css.

2. **Suite di test per le funzioni pure (nodo, senza librerie)**
   - Problema: il sito non è mai stato eseguito (T16: "Non l'ho eseguito") e il passo successivo è "Prova con utenti"; le funzioni `controllaOrdine`, `sistemaProgresso`, `ordineMescolato`, `registraRisposta` sono già pure ed esportate (`module.exports`) ma oggi nessuno le verifica.
   - Proposta: nuovo `testi/testi.js` eseguibili con `node`: 40-60 asserzioni deterministiche (es. `controllaOrdine` accetta una `alternative` valida ma rifiuta un blocco spostato; `sistemaProgresso({giusti:'x'})` → 0; `mescola` restituisce una permutazione; `differisciParole` dell'idea 3).
   - Effetto per chi impara: indiretto ma forte — permette di implementare le altre idee di questo elenco (e ogni futuro cambio) senza paura di rompere i giochi o le statistiche.
   - Difficolta': FACILE
   - File toccati: nuovo `testi/testi.js`; zero modifiche in `web/`.

3. **Diff visibile in "Trova l'errore" (evidenziare la parola cambiata)**
   - Problema: in `giocoErrori`, dopo la risposta il messaggio mostra `frase_corretta` e `spiegazione_it`, ma l'occhio non trova subito la differenza; con scarti minuti (*ein Hund* → *einen Hund*) ci si può perdere.
   - Proposta: funzione pura `differisciParole(a, b)` (diff a livello di parola, ~30 righe con lcs) che, in `giocoErrori`, evidenzia con `<mark>` la parola cambiata nella frase corretta e la parola errata nella frase sbagliata. Fallback: se la differenza supera la metà delle parole (es. errore di puro ordine), si mantiene la vista attuale.
   - Effetto per chi impara: l'errore diventa visibile, non solo spiegato; a A1/A2 si memora la "forma" dello sbaglio, non solo la regola in italiano.
   - Difficolta': FACILE
   - File toccati: web/app.js (diff + `giocoErrori`), web/style.css (stili dei `mark`).

4. **Difficoltà graduale in "Rimetti in ordine" (per numero di blocchi)**
   - Problema: in `giocoFrasi` il pool è uniforme: un principiante può ricevere al primo tentativo una frase di 9 blocchi; la difficoltà non cresce con l'abilità.
   - Proposta: pool ordinato per `blocchi.length`; funzione pura `sottogruppoPerDifficolta(pool, quota)` che espone solo una quota del pool, che cresce col percentuale di giuste del gioco (`giusti/(giusti+sbagliati)`): 40% all'inizio, 70% sopra 0.5, 100% sopra 0.8. `prossima()` pesca nel sottogruppo.
   - Effetto per chi impara: le prime sessioni sono frasi corte e vincenti; le frasi lunghe arrivano come premio, meno frustrazione e meno abbandono.
   - Difficolta': FACILE
   - File toccati: web/app.js (`giocoFrasi` + nuova funzione pura, testabile con l'idea 2).

5. **Riconoscere le `alternative` di ordine e dirlo esplicitamente**
   - Problema: `controllaOrdine` accetta già le `alternative`, ma al successo il messaggio è sempre "Giusto!": il giocatore non sa che il suo ordine era una variante valida; per l'ordine delle parole (nucleo di A2) quella informazione è essa stessa una lezione.
   - Proposta: `controllaOrdine` restituisce quale variante ha matchato; in `controllaClick`, se a matchare è una variante non canonica, si aggiunge una riga: "Anche quest'ordine è corretto: in tedesco esistono più frasi giuste con le stesse parole."
   - Effetto per chi impara: impara che l'ordine tedesco ha più di una forma giusta; meno paura di sbagliare "l'ordine".
   - Difficolta': FACILE
   - File toccati: web/app.js (`controllaOrdine`, `controllaClick`).

6. **Obiettivo giornaliero + streak ("giorni filati")**
   - Problema: la home mostra solo totali cumulativi (`riepilogo`): manca un traguardo a breve e una continuità, e l'uso "un po' al giorno" che il sito promette non ha un gancio visibile.
   - Proposta: chiave separata `langue_obiettivo_v1`: `{giorno, giustiOggi, streak}`. Riga in home: "Oggi: 7/10 · Streak: 4 giorni". Il giorno si chiude con 10 risposte giuste (tutti i giochi); la data va calcolata in fuso locale (niente `toISOString()`, che è UTC e sbaglia a mezzanotte).
   - Effetto per chi impara: crea l'abitudine quotidiana; il traguardo è visibile e la streak premia la regolarità.
   - Difficolta': MEDIO (logiche di cambio giorno; testabili con l'idea 2)
   - File toccati: web/app.js, web/index.html (riga in "I tuoi progressi"), web/style.css.

7. **"Le tue parole": vocabolario personale locale dal gioco articoli**
   - Problema: dopo "Der, die o das?" non resta memoria delle parole viste: chi vuole ripassare da solo ha solo i contatori, non la lista.
   - Proposta: a ogni domanda di `giocoArticoli` si aggiorna `{parola → {articolo, traduzione_it, volte, sbagliate}}` (massimo 200 entry; chiave `langue_rubrica_v1`). Nuova sezione in home "Le tue parole (n)": tabella ordinata per "sbagliate" discendente — es. "der Hund · cane · sbagliato 2 volte". Nessun nuovo contenuto tedesco: è uno specchio dei record già in `data.js`.
   - Effetto per chi impara: una lista personale di ripasso leggibile nei momenti brevi (trasporto, coda); rinforza l'associazione articolo+nome, il cuore di A1.
   - Difficolta': MEDIO
   - File toccati: web/app.js, web/index.html, web/style.css.

8. **Installabile e offline su telefono (PWA minimale)**
   - Problema: il sito è statico ma va ricaricato a ogni apertura: in treno o senza segnale (il momento classico "ripasso 5 minuti") non funziona; e non ha icona sulla home del telefono.
   - Proposta: `manifest.webmanifest` + `sw.js` di ~40 righe che in installazione mette in cache `index.html`, `app.js`, `style.css`, `data.js` e li serve dalla cache se offline; registrazione in `index.html`. da_verificare: i service worker non partono su `file://`, serve http(s) o localhost — dipende da come verrà hostato.
   - Effetto per chi impara: esperienza da app su telefono: icona, schermo intero, usabile offline; ideale per sessioni brevi e regolari.
   - Difficolta': MEDIO
   - File toccati: nuovi web/manifest.webmanifest, web/sw.js; piccolissimo cambio in web/index.html.

## La mia idea preferita e perche'

**"Ripasso degli sbagli" (idea 1)**, per questo ordine di ragioni:
- **Il più grande effetto reale sull'apprendimento**: attacca la curva del dimenticato costringendo a ripetere esattamente gli item su cui l'utente inciampa; le altre idee sono confort/sicurezza/motivazione, questa è imparare.
- **Zero nuovo contenuto**: riusa gli stessi record di `data.js`, nel rispetto della regola "niente nuovo contenuto tedesco qui".
- **Rischio basso e reversibile**: chiave separata in localStorage (non `langue_progress_v1`), cancellabile senza toccare i progressi; la sessione riusa `creaSessione` e i renderer esistenti.
- **Si compone**: va d'accordo con l'idea 3 (il diff rende l'errore "ri-leggibile" quando torna) e con l'idea 2 (la logica dei debiti è pura e testabile).
- Subito dopo la farei l'idea 2 (suite di test): è la rete di sicurezza per tutti gli altri interventi.
