# Rapporto T20-esegui-a – Ripasso degli sbagli

## Cosa ho fatto
Ho realizzato l'idea scelta in `agenti/T19-scelta/SCELTA.md`: il **Ripasso degli sbagli** ("debiti").
Ho toccato solo `web/index.html`, `web/app.js`, `web/style.css`, con modifiche piccole e locali. Ogni parte nuova o cambiata ha il commento `[agente T20-esegui-a]`. Nessun contenuto tedesco nuovo, `data.js` non toccato.

- **index.html**: nuova scheda "Ripasso" (bottone `gioca-ripasso`) in fondo alla lista dei giochi, con contatore (`conta-ripasso`) e dettaglio per gioco (`stat-ripasso`).
- **app.js**:
  - funzioni pure nuove (provabili con Node): `nuoviDebiti`, `tagliaDebiti`, `sistemaDebiti`, `aggiungiDebitoA`, `rimuoviDebitoDa`, `elencoDebiti`;
  - salvataggio in una chiave separata del browser `langue_debiti_v1` (`caricaDebiti`, `salvaDebiti`); i progressi `langue_progress_v1` non cambiano;
  - dentro il sito: `aggiungiDebito`, `rimuoviDebito`, `getDebitiPerGioco` (ordinati per numero di errori, max 50 per gioco; oltre 50 si scarta il più vecchio);
  - i tre giochi segnano il debito quando sbagli (e in "Rimetti in ordine" anche quando premi "Mostra la soluzione");
  - i tre giochi accettano una modalità "ripasso": stessa grafica e stessi tasti, ma pescano solo dai tuoi sbagli (prima quelli sbagliati più volte); se rispondi giusto, l'item esce dal ripasso; quando non resta niente compare "Nessun debito da ripassare" con i tasti "Torna al ripasso" / "Torna alla home";
  - "Azzera i progressi" ora svuota anche il ripasso.
- **style.css**: scheda Ripasso con bordo tratteggiato e titolo rosso, griglia per la scelta del gioco, piccola nota "ancora da ripassare".

## Come provarlo (cosa cliccare)
1. Apri `web/index.html` nel browser. La scheda **Ripasso** deve dire "Niente da ripassare…" ed essere disattivata.
2. Clicca **Der, die o das?** e scegli apposta un articolo sbagliato. Clicca **← Torna alla home**: la scheda Ripasso deve dire **1 da ripassare** e "Parole: 1".
3. Clicca **Rimetti in ordine**, poi **Mostra la soluzione**. Torna alla home: ora **2 da ripassare** ("Frasi: 1").
4. Clicca **Ripasso**: vedi i tre giochi con il loro numero; quelli a 0 sono disattivati. Clicca **Der, die o das? – 1 da ripassare**: deve comparire la parola che avevi sbagliato.
5. Rispondi giusto: la nota in alto passa a 0 alla domanda dopo; clicca **Avanti →** e compare "Nessun debito da ripassare in questo gioco". Clicca **Torna alla home**: ora **1 da ripassare**.
6. Prova il caso "sbaglio ancora": nel ripasso rispondi di nuovo male. L'item resta (e sale in cima, perché conta quante volte lo sbagli).
7. Ricarica la pagina: il contatore del Ripasso deve restare uguale (è salvato nel browser).
8. Clicca **Azzera i progressi** e conferma: il Ripasso torna a zero.

## Scelte (default che ho preso io)
- **Una sola scheda "Ripasso"** che apre una schermata dove scegli il gioco. Il brief chiedeva sia una scheda unica sia `avviaRipasso(gioco)`, e il listener proposto passava `progresso.livello` come gioco (sarebbe stato un errore): ho risolto così.
- Invece di una `creaSessioneRipasso` separata, ho aggiunto ai tre giochi un parametro `modo = 'ripasso'`: così si riusano esattamente i renderer esistenti senza copiarli.
- Il ripasso **ignora il filtro di livello** (come da brief): usa tutti i tuoi sbagli.
- Una risposta giusta nel gioco **normale** non toglie l'item dal ripasso: lo toglie solo una risposta giusta **nel ripasso**.
- In "Rimetti in ordine" il debito si conta **una volta per domanda** (più tentativi sbagliati sulla stessa frase = +1, non +3); esce dal ripasso solo se giusta al primo "Controlla".
- Le risposte date nel ripasso contano anche nelle statistiche normali del gioco (giuste/sbagliate/serie).
- "Azzera i progressi" svuota anche il ripasso.

## Da controllare / attenzione
- Non ho potuto eseguire il sito: è tutto ragionato sul codice, **non provato**.
- Il ripasso usa il campo `id` dei record in `data.js`. Non ho visto `data.js`: se i record lì non hanno `id`, gli sbagli non vengono registrati e la scheda resta a 0. Da verificare al primo test (passo 2).
- Se un record viene tolto o messo "da_verificare", il suo debito viene semplicemente ignorato (non si rompe nulla).

## Suggerimenti per la scheda progetto (PROGETTO.md, da fare a mano da Leo)
- Nel Piano si potrebbe aggiungere: "- [x] Ripasso degli sbagli (T19-scelta, T20-esegui)".
