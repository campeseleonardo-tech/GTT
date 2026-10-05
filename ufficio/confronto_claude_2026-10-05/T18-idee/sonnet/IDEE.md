# Idee per migliorare Langue (agente T18-idee-a, bozza)

Nota di metodo: ho solo letto `PROGETTO.md`, `SCHEMA.md`, `web/index.html`, `web/app.js`, `web/style.css`. Non ho visto `web/data.js` e non posso eseguire nulla: quello che scrivo viene dal ragionamento sul codice, non da una prova. Dove un punto dipende da cio' che non ho visto lo segno "da_verificare".

## Problemi che vedo nel codice attuale

Controllo di base: l'ordine di avvio di `app.js` sembra corretto (le funzioni sono "hoisted", le costanti `LIVELLI`, `GIOCHI`, `CHIAVE_PROGRESSI` sono definite prima della chiamata `avviaSito()`). Non ho trovato errori che blocchino l'avvio. I punti sotto sono fragilita' o limiti, non crash certi.

1. **`scegliCasuale(pool, null, corrente)`** (usata dai tre giochi): pesca "con rimessa", evita solo la domanda immediatamente precedente. Non esiste il concetto di "gia' vista": con 400 parole la stessa puo' tornare dopo 2 domande, con poche frasi a un livello ripete di continuo, e il giocatore non sa mai quanto contenuto ha esaurito. Le risposte sbagliate non influenzano cosa esce dopo.
2. **`sistemaProgresso` / `nuovoProgresso`**: ricostruiscono l'oggetto copiando solo i campi noti, quindi qualsiasi campo nuovo salvato in futuro viene cancellato al caricamento successivo. `versione: 1` viene scritto ma mai letto (nessuna migrazione). In piu' `progresso` viene letto una volta sola all'avvio e `salva()` riscrive tutto: con due schede del browser aperte vince l'ultima che salva e i conteggi dell'altra si perdono.
3. **`giocoFrasi` -> `metti` / `togli`**: dopo "Non e' ancora giusto" il messaggio resta sullo schermo mentre il giocatore sposta i blocchi (solo `Ricomincia` lo svuota). Il feedback e' anche solo binario: non dice quanti blocchi sono al posto giusto.
4. **`giocoFrasi` -> `disegna`**: a ogni tocco ricostruisce tutto il corpo del gioco e rimette il focus con `.focus()` su un bottone appena creato. Sui telefoni questo puo' far scorrere o saltare la pagina quando la zona "La tua frase" cresce su piu' righe (da_verificare: non provato su dispositivo).
5. **`giocoArticoli` -> `rispondi` e `giocoErrori` -> `rispondi`**: riconoscono i bottoni confrontando `textContent` (`b.textContent === corrente.articolo`, `b.textContent === scelta.testo`) mentre nello stesso ciclo il testo viene modificato con il prefisso "✓ ". Oggi funziona, ma e' fragile: basta cambiare un'etichetta (o avere due opzioni con lo stesso testo) per marcare il bottone sbagliato. In `giocoErrori` si usa anche una proprieta' inventata sull'elemento (`b._corretta`).
6. **`giocoArticoli` -> `prossima` e `giocoErrori` -> `prossima`**: il focus di partenza va al primo bottone (`riga.firstChild.focus()`, `gruppo.firstChild.focus()`). Con la tastiera, un Invio ripetuto o doppio sul tasto "Avanti" risponde subito "der" alla domanda dopo, senza volerlo (da_verificare: non provato).
7. **`opzioniErrore` / `giocoErrori`**: il gioco si chiama "Trova l'errore" ma offre sempre solo due frasi, quindi si indovina al 50%: il contatore "Giuste" e' gonfiato dal caso. Inoltre il campo `categoria` dei record errore (`articolo`, `ordine_verbo`, `genere`, `falsi_amici`, `preposizioni`, `altro`) non viene mai letto da `app.js`: dato presente e inutilizzato.
8. **`filtraPerLivello`**: con "Tutti" non filtra nulla, quindi passano anche i record con `livello` `B1` o `altro`, che lo `SCHEMA.md` ammette, mentre il sito promette A1-A2. Non so se in `data.js` ce ne siano (da_verificare). Inoltre `bozza` e `verificato` sono trattati allo stesso modo: il sito non puo' dare la precedenza ai contenuti riletti da Leo.
9. **`mostraHome` / `mostraGioco`**: cambiano solo `hidden`, non usano la cronologia del browser. Sul telefono il tasto Indietro di sistema esce dal sito e butta via la partita in corso; non si puo' neppure mandare a qualcuno il link diretto di un gioco.
10. **`avviaSito` -> `window.LANGUE_DATA`**: i dati si leggono solo da `window.LANGUE_DATA`. Se `data.js` lo definisse con `const LANGUE_DATA = ...` invece di `window.LANGUE_DATA = ...` o `var`, i dati non sarebbero visibili e comparirebbe l'avviso "Non trovo i contenuti" (da_verificare: non ho visto `data.js`; l'avviso esiste gia', quindi il guasto sarebbe almeno chiaro).
11. **Indizio involontario in `giocoFrasi`**: i blocchi mantengono le maiuscole originali e `controllaOrdine` le ignora; il blocco con la maiuscola iniziale rivela quasi sempre il primo della frase (e i sostantivi si riconoscono dalla maiuscola). Non e' un bug, ma conviene saperlo se si vuole alzare la difficolta'.
12. **`aggiornaHome` -> `riepilogo`**: la percentuale totale mescola tre giochi con probabilita' di indovinare diverse (3 scelte, 2 scelte, ordine). Il numero e' poco interpretabile; meglio una statistica per gioco o per categoria.

## Idee

Tutte fattibili con HTML/CSS/JS semplici, senza server, senza librerie e senza nuovi contenuti tedeschi (usano i dati che ci sono; l'idea 4 e' l'unica che tocca regole sulla lingua, vedi nota li').

### 1. Ripasso mirato: mazzo senza ripetizioni, sbagliate che ritornano, round da 10
- **Problema**: `scegliCasuale` pesca con rimessa (problema 1): niente completamento, niente ripasso di cio' che si sbaglia, nessun senso di "ho finito un giro".
- **Proposta**: al posto della pesca casuale, un "mazzo": all'inizio si mescola la lista, si pesca in ordine, e una domanda sbagliata viene rimessa nel mazzo 3-5 posizioni piu' avanti nella stessa sessione. Il gioco procede a round da 10 domande con una schermata finale ("8 su 10"; elenco delle sbagliate con la soluzione; pulsanti "Rifai le sbagliate" e "Altre 10"). Nel salvataggio si tiene, per ogni id, uno stato semplice (`mai vista` / `da ripassare` / `ok`), cosi' al round successivo le "da ripassare" escono per prime. Nella home: "Parole viste: 37 su 400". Servono nuove funzioni pure (`creaMazzo`, `prossimaDalMazzo`, `aggiornaScheda`) da esportare in `module.exports` e provare con Node come le altre; `sistemaProgresso` va esteso e `versione` portata a 2 con migrazione (problema 2).
- **Effetto per chi impara**: ripete davvero cio' che sbaglia, vede un traguardo (round e quota "viste"), la sessione ha un inizio e una fine. E' il cambiamento che sposta di piu' la memorizzazione.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js`, `web/style.css`, `web/index.html` (riga "viste" nelle schede; nessun nuovo dato).

### 2. Pronuncia con la voce tedesca del browser
- **Problema**: il sito e' tutto muto; per un italiano la pronuncia (ei/ie, ch, ü, la "r") e' meta' della difficolta' e le parole si ricordano meglio con l'orecchio.
- **Proposta**: un pulsante "Ascolta" che usa `speechSynthesis` / `SpeechSynthesisUtterance` con `lang = 'de-DE'`, velocita' leggermente ridotta. Compare dopo la risposta accanto a "der Tisch"-tipo (articolo + parola), alla frase completa nel gioco "Rimetti in ordine" e alla frase corretta in "Trova l'errore". Si controlla `'speechSynthesis' in window` e si aspetta l'evento `voiceschanged` (le voci si caricano in ritardo): se non c'e' una voce `de-*` il pulsante non compare (meglio nessun audio che una voce italiana che legge il tedesco). Opzionale: una scelta "Solo voci locali" (`voice.localService`) per non dipendere dalla rete.
- **Effetto per chi impara**: sente articolo e parola insieme, associa scritto e suono, puo' usare il sito anche ascoltando.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js` (piccola funzione `parla(testo)` e un pulsante in `sessione.messaggio`), `web/style.css`.
- **Attenzione**: su alcuni telefoni la voce tedesca viene scaricata dalla rete dal browser; il testo in home dice "niente tracciamento". Da_verificare se la frase resta onesta; vedi domanda a Leo.

### 3. "Tocca la parola sbagliata" al posto del 50% di fortuna
- **Problema**: problema 7: due frasi, si indovina; e la `categoria` del record non serve a niente.
- **Proposta**: si mostra solo la frase sbagliata, spezzata in parole-bottone, e si chiede di toccare la parola che non va. Le parole sbagliate si ricavano da un confronto automatico (LCS sulle parole, poche righe) tra `frase_sbagliata` e `frase_corretta`: per l'esempio dello `SCHEMA.md`, "Ich habe ein Hund." contro "Ich habe einen Hund." la parola da toccare e' "ein". Se la differenza non e' in una parola della frase sbagliata (manca una parola, o l'errore e' di ordine e il confronto non e' netto), quel record usa il vecchio modo a due scelte: nessuna perdita. Dopo la risposta: la frase corretta con le parole cambiate in grassetto e sottolineate (non solo colore), poi la `spiegazione_it`, e l'etichetta italiana della categoria ("Ordine del verbo", "Falsi amici", ...). Statistiche per categoria nel salvataggio: dopo almeno 5 risposte per categoria la home dice "Punto debole: preposizioni (3 giuste su 9)".
- **Effetto per chi impara**: deve riconoscere l'errore invece di scegliere fra due frasi, vede esattamente dove sta la differenza, scopre quali tipi di errore commette di piu'.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js` (nuove funzioni pure `confrontaParole`, `categoriaEtichetta`; `giocoErrori`; progressi), `web/style.css`, `web/index.html` (frase sulle statistiche di categoria).

### 4. Indizi sulle desinenze dopo "Der, die o das?"
- **Problema**: il gioco chiede di memorizzare l'articolo parola per parola; non insegna le poche regole che valgono per centinaia di parole.
- **Proposta**: una funzione pura `indizioArticolo(parola)` che guarda la fine della parola e, solo dopo la risposta, aggiunge una riga in italiano: "Indizio: le parole in -ung sono femminili (die)". Regole prudenti e con poche eccezioni: -ung, -heit, -keit, -schaft, -tion, -ität = die; -chen, -lein = das; -ling = der. Ci sono eccezioni note (per esempio parole in -chen che sono "der", come Kuchen) che vanno messe in una lista di esclusione. Il trucco in piu': l'indizio compare solo se l'articolo del record coincide con la regola; se NON coincide, non viene mostrato e `console.warn` segnala l'id. In pratica la stessa funzione, lanciata da Node su tutti i dati, e' un controllo di coerenza gratuito per Leo sulle parole sospette.
- **Effetto per chi impara**: passa dal "parola per parola" al "riconosco il tipo di parola": puo' indovinare l'articolo di parole mai viste.
- **Difficolta'**: FACILE
- **File toccati**: `web/app.js`, `web/style.css` (poco).
- **Attenzione per Leo**: l'elenco delle desinenze e' conoscenza della lingua scritta da me, non e' contenuto estratto dai dati: Leo (C1) deve rileggerlo e approvarlo prima, in particolare le eccezioni.

### 5. Feedback "dove sbaglio" nel gioco "Rimetti in ordine"
- **Problema**: problema 3: "Non e' ancora giusto" e basta; il messaggio resta mentre si sistema; chi sbaglia una volta rischia solo di riprovare a caso o di guardare la soluzione.
- **Proposta**: dopo "Controlla" sbagliato, ogni blocco messo viene marcato con un simbolo (✓ = posizione giusta, · = da spostare) e un testo "3 blocchi su 5 al posto giusto". Il confronto avviene sulle parole: si prende la soluzione (`testo_de` o una `alternative`) che coincide di piu' con la frase costruita e si controlla la posizione di ogni blocco. Il messaggio sparisce appena si tocca un blocco (`metti`/`togli` chiamano `sessione.messaggio('info', [])`). Facoltativo: dopo 2 tentativi un "Aiutino" che mette al posto giusto il primo blocco sbagliato.
- **Effetto per chi impara**: da "giusto/sbagliato" a "stai a meta' strada": vede la struttura (verbo in seconda posizione, ecc.) e impara per tentativi guidati, senza spegnersi.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js` (funzione pura `blocchiAlPosto`, `giocoFrasi`), `web/style.css`.

### 6. Tasto Indietro e link diretti ai giochi
- **Problema**: problema 9: su telefono "Indietro" fa uscire dal sito.
- **Proposta**: l'indirizzo cambia con il gioco (`#articoli`, `#frasi`, `#errori`, vuoto = home) e un ascoltatore `hashchange` mostra la vista giusta; "Torna alla home" e il tasto Indietro fanno la stessa cosa. All'apertura con un `#frasi` si parte da quel gioco, a patto che ci siano contenuti per il livello salvato (altrimenti home). Funziona anche aprendo il file da disco.
- **Effetto per chi impara**: il tasto Indietro fa quello che ci si aspetta; si puo' mandare a un amico "gioca a Der, die o das" con un link; chi ricarica la pagina nel mezzo di un gioco ci torna.
- **Difficolta'**: FACILE
- **File toccati**: `web/app.js` (`mostraHome`, `mostraGioco` e i collegamenti dei pulsanti).

### 7. Modalita' revisione e "Segnala" per la rilettura di Leo
- **Problema**: Leo rilegge circa il 20% dei contenuti, ma dal sito non puo' sapere quale record sta guardando, ne' ricordarsi quali erano dubbi; il piede dice gia' "alcuni potrebbero contenere errori".
- **Proposta**: un interruttore nel piede (o `#revisione`) che mostra sotto ogni domanda "id · stato" (es. `fra-0012 · bozza`) e un pulsante "Segnala questo". Gli id segnalati vanno in un elenco salvato nel browser (chiave separata dai progressi); nella home compare "Segnalati: 3" con "Copia elenco" (`navigator.clipboard`, con la cartella di testo selezionabile come alternativa se non e' disponibile) e "Svuota". Leo incolla l'elenco in un file o a un agente, che mette quei record in `da_verificare`. Lo stesso pulsante puo' stare nella versione per tutti. Da_verificare: se `data.js` contiene `id` e `stato` (`app.js` legge `stato`, ma non ho visto `id`).
- **Effetto per chi impara**: indiretto ma reale: i contenuti sbagliati vengono corretti piu' in fretta; chi trova un errore ha un modo di dirlo.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js`, `web/style.css`, `web/index.html` (piede e riga "Segnalati").

### 8. Salva e ricarica i progressi (file o codice) e giorni di fila
- **Problema**: i progressi vivono solo in `localStorage`; se si pulisce il browser, si cambia telefono o il browser li cancella, tutto sparisce. Su Safari i dati dei siti possono essere cancellati dopo un periodo di non uso (da_verificare i dettagli). Nulla invita a tornare il giorno dopo.
- **Proposta**: due pulsanti nel riquadro "I tuoi progressi": "Salva su file" (crea un `Blob` e un link `download`, nome tipo `langue-progressi.json`) e "Carica da file" (`input type=file` + `FileReader`, il contenuto passa da `sistemaProgresso`, che e' gia' fatta per sistemare dati rovinati). In alternativa un testo copia-incolla per chi non gestisce bene i file sul telefono. In piu' due campi: `ultimoGiorno` (data locale) e `giorniDiFila`, e in home "Giorni di fila: 4". Prima va risolto il problema 2 (campi nuovi non vengono scartati).
- **Effetto per chi impara**: non perde mesi di lavoro; ha un piccolo motivo per tornare ogni giorno senza account e senza tracciamento.
- **Difficolta'**: MEDIO
- **File toccati**: `web/app.js`, `web/index.html` (pulsanti e riga giorni di fila), `web/style.css`.

## La mia idea preferita e perche'

L'idea 1, il ripasso mirato con mazzo e round da 10. Oggi il sito e' un quiz che pesca a caso senza memoria: chi impara puo' giocare per un'ora senza mai ripassare le sue debolezze e senza mai "finire" nulla. Il mazzo con le sbagliate che ritornano e la quota "parole viste" trasformano le stesse parole e frasi, che gia' ci sono, in un percorso con progressi visibili, senza aggiungere una sola parola di tedesco. E' anche la base per le altre: le statistiche per categoria (idea 3), l'export dei progressi (idea 8) e la segnalazione (idea 7) hanno bisogno di salvare dati per record, quindi conviene fare prima la migrazione del salvataggio (problema 2) dentro questa idea.

Ordine che suggerisco per farle: 6 e 4 (FACILE, subito), poi 1 (con la migrazione di `sistemaProgresso`), poi 3, 5, 2, 7, 8.
