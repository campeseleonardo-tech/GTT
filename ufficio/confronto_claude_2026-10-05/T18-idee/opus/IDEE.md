# Idee per migliorare Langue (agente T18-idee-a)

Origine: agente T18-idee-a · stato: bozza.
Base: lettura di `PROGETTO.md`, `SCHEMA.md`, `web/index.html`, `web/app.js`, `web/style.css`. Il sito NON e' stato eseguito: tutto quello che segue viene dalla lettura del codice. `web/data.js` non era tra i file forniti: i nomi delle chiavi (`articoli`, `frasi`, `errori`) sono da_verificare.

## Problemi che vedo nel codice attuale

1. **Una frase "giusta" puo' essere mostrata con le maiuscole sbagliate** (`normalizzaFrase`, `controllaOrdine`, `controllaClick`).
   `normalizzaFrase` mette tutto in minuscolo. Esempio dello SCHEMA: blocchi `["Ich", "lerne", "heute", "Deutsch"]`, alternativa `Heute lerne ich Deutsch`. Se il giocatore compone `heute lerne Ich Deutsch`, il confronto in minuscolo la accetta e `controllaClick` mostra "Giusto!" con `testi.join(' ')`, cioe' proprio la frase con `heute` minuscolo all'inizio e `Ich` maiuscolo in mezzo. Chi impara vede premiata una frase scritta male. Correzione semplice: nel messaggio mostrare la frase ammessa che ha fatto scattare il confronto (`testo_de` o l'alternativa), non quella composta.

2. **Dopo "Mostra la soluzione" i blocchi rimasti sembrano ancora cliccabili** (`disegna`, `mostraSoluzione`).
   Con `chiusa = true`, `disegna` disabilita solo i bottoni dentro `.costruita`; quelli in `.rimasti` restano attivi (cliccandoli `metti` non fa nulla perche' esce subito). Inoltre la soluzione appare solo come testo nel messaggio, mentre i blocchi restano nell'ordine sbagliato del giocatore: il confronto visivo "il mio ordine / l'ordine giusto" manca.

3. **Il riconoscimento del bottone scelto passa dal testo** (`rispondi` in `giocoArticoli` e in `giocoErrori`).
   Si confronta `b.textContent` con `scelto` / `scelta.testo`, mentre altri bottoni vengono rinominati con "✓ " nello stesso giro. Oggi funziona, ma e' fragile: basta un piccolo cambio (es. un'icona nel testo, due opzioni con lo stesso testo per un errore di dati) per marcare il bottone sbagliato. Piu' robusto: passare a `rispondi` il bottone stesso.

4. **Testo italiano marcato come tedesco** (`rispondi` in `giocoErrori`).
   La riga `'Frase corretta: ' + corrente.frase_corretta` ha `lingua: 'de'`: un lettore di schermo legge "Frase corretta" con pronuncia tedesca. Stessa cosa per le frasi/opzioni, che pero' sono interamente tedesche (ok).

5. **Estrazione casuale senza memoria** (`scegliCasuale`).
   Evita solo la domanda appena uscita. Con pochi record (es. filtro A2 nel gioco errori) la stessa domanda torna spesso; con 200 parole alcune non escono mai per molto tempo. Le parole sbagliate non tornano piu' spesso di quelle giuste.

6. **Il tasto "Indietro" del telefono fa uscire dal sito** (`mostraGioco`, `mostraHome`).
   Le due viste si scambiano con `hidden`, senza `history.pushState` ne' `#indirizzo`. Su Android il gesto "indietro" durante un gioco chiude la pagina invece di tornare alla home (i progressi sono salvati, ma l'esperienza e' brusca).

7. **I progressi sono solo totali** (`nuovoProgresso`, `sistemaProgresso`).
   Si salvano giuste/sbagliate/serie per gioco, nessun dato per singola parola o frase. `sistemaProgresso` ricostruisce l'oggetto da zero e butterebbe via campi nuovi: qualsiasi idea "per parola" richiede una versione 2 del formato con migrazione (lo segno perche' tocca i dati gia' salvati nel browser degli utenti di prova).

8. **Bottoni non scelti identici a quelli attivi** (`style.css`, regola `.btn:disabled { opacity: 1; }`).
   Dopo la risposta, il terzo articolo (ne' giusto ne' scelto) e' disabilitato ma ha lo stesso aspetto di un bottone attivo: si tocca e non succede nulla.

## Idee

In ordine di priorita' (prima = migliore rapporto effetto/fatica, secondo me).

### 1. Ripasso intelligente: chi sbaglia rivede, chi sa va avanti
- **Problema:** `scegliCasuale` pesca a caso; un errore non ha conseguenze sul futuro (punto 5 e 7 sopra).
- **Proposta:** per ogni record salvare in `localStorage` una "scatola" da 1 a 5 (metodo Leitner) e la data dell'ultima risposta: risposta giusta = scatola +1, sbagliata = scatola 1. La prossima domanda si sceglie pesando le scatole basse (es. scatola 1 peso 8, scatola 5 peso 1) e i record mai visti. Funzione pura nuova `scegliPesato(lista, statoPerId, rng)`, testabile con Node come le altre. In home: "Parole da ripassare: 23 · Sapute bene: 41".
- **Effetto per chi impara:** il tempo va dove serve; "die Butter" sbagliata tre volte torna finche' non entra. Da' anche un numero concreto di cose imparate, molto piu' motivante di "Giuste: 312".
- **Difficolta':** MEDIO (formato progressi versione 2 + migrazione in `sistemaProgresso`).
- **File toccati:** `web/app.js` (funzioni pure, `registraRisposta`, `aggiornaHome`, i tre `prossima`).

### 2. Partite da 10 domande con schermata finale "da rivedere"
- **Problema:** i giochi non finiscono mai; dopo 15 risposte non resta nulla in mano, e gli errori fatti spariscono appena si preme "Avanti".
- **Proposta:** ogni partita = 10 domande (barra "3/10"). Alla fine una schermata: punteggio, e la lista delle sole risposte sbagliate con la forma giusta (`die Butter – il burro`, la frase corretta, la soluzione dell'ordine). Pulsanti "Rigioca solo questi" e "Nuova partita".
- **Effetto per chi impara:** sessioni brevi adatte al telefono (2-3 minuti), un momento di chiusura e un ripasso immediato degli errori, che e' il momento in cui si fissano meglio.
- **Difficolta':** FACILE/MEDIO.
- **File toccati:** `web/app.js` (`creaSessione` tiene il conteggio e la lista errori; nuova funzione `mostraFinePartita`), `web/style.css`.

### 3. Ascolta: pronuncia con la voce del browser
- **Problema:** il sito e' solo da leggere; chi inizia non sa come si pronunciano "Brötchen" o "Zug", e la pronuncia e' la cosa che un italiano sbaglia di piu' all'inizio.
- **Proposta:** un bottone "🔊 Ascolta" accanto alla parola, alla frase corretta e alla soluzione, che usa `speechSynthesis` con `lang = 'de-DE'` (nessuna libreria, nessun server). Se il browser non ha una voce tedesca (`getVoices()` senza `de`), il bottone non compare. Opzione in home "leggi ad alta voce dopo ogni risposta".
- **Effetto per chi impara:** collega scritto e suono; nel gioco frasi aiuta a sentire dove va il verbo.
- **Difficolta':** FACILE (la disponibilita' della voce varia per sistema: da provare su telefono vero).
- **File toccati:** `web/app.js` (funzione `pronuncia(testo)` + bottone nei messaggi), `web/style.css`.

### 4. Modalita' revisione per Leo (indirizzo nascosto)
- **Problema:** tutti i contenuti sono "bozza"; Leo rilegge circa il 20% aprendo file JSON, che e' lento e scomodo dal telefono.
- **Proposta:** aprendo `index.html#revisione` compare una vista a schede: un record alla volta (parola con articolo, frase con blocchi e alternative, errore con spiegazione), tre bottoni "OK / Dubbio / Salta" e un campo nota. Le scelte restano nel browser; alla fine "Scarica la lista" crea un file `revisione.json` (Blob + link di download) con `id`, esito e nota, che un agente poi applica ai file di contenuto (cambiando solo `stato`, come dice SCHEMA). Il sito non modifica nessun dato.
- **Effetto per chi impara:** indiretto ma grande: contenuti verificati piu' in fretta = meno tedesco sbagliato imparato. Permette anche di nascondere ai principianti le voci segnate "Dubbio" subito.
- **Difficolta':** MEDIO.
- **File toccati:** `web/app.js` (nuova vista), `web/index.html` (una sezione `vista-revisione`), `web/style.css`.

### 5. Trova l'errore: evidenziare la parola che cambia
- **Problema:** dopo la risposta si vedono due frasi lunghe quasi uguali; l'occhio deve cercare da solo la differenza (`ein`/`einen`, posizione del verbo).
- **Proposta:** funzione pura `differenzaParole(sbagliata, corretta)` (confronto parola per parola con la sottosequenza comune piu' lunga, poche righe di JS) che restituisce i pezzi uguali/diversi. Nel messaggio finale: la frase sbagliata con la parola sbagliata barrata in rosso e la corretta con la parola giusta sottolineata in verde, piu' un simbolo (non solo colore). Costruzione sempre con `textContent` e `<span>`, come gia' fa il sito.
- **Effetto per chi impara:** vede in un colpo d'occhio *cosa* cambia, e la spiegazione in italiano si aggancia a quella parola.
- **Difficolta':** FACILE/MEDIO.
- **File toccati:** `web/app.js` (`giocoErrori` → `rispondi`, nuova funzione pura), `web/style.css`.

### 6. Rimetti in ordine: aiuto a gradini invece di "tutto o niente"
- **Problema:** oggi, se la frase e' sbagliata, si puo' solo riprovare alla cieca o vedere tutta la soluzione (punto 2 sopra).
- **Proposta:** dopo un "Controlla" sbagliato, i blocchi gia' nella posizione giusta diventano verdi e bloccati (si confronta con la frase ammessa piu' vicina tra `testo_de` e `alternative`). Bottone "Aiuto" che fissa il blocco successivo giusto. Le risposte con aiuto contano come "giuste con aiuto" (non spezzano la serie, ma non la allungano). Con "Mostra la soluzione" i blocchi si ridispongono nell'ordine giusto e tutti si disabilitano.
- **Effetto per chi impara:** capisce *quale* parte della frase sbaglia (spesso il verbo in seconda posizione o in fondo) invece di arrendersi.
- **Difficolta':** MEDIO (le alternative rendono "la posizione giusta" ambigua: si sceglie l'alternativa con piu' blocchi gia' a posto).
- **File toccati:** `web/app.js` (`controllaClick`, `mostraSoluzione`, `disegna`, nuova funzione pura `bloccheGiusti`), `web/style.css`.

### 7. Der, die o das al contrario: scrivi tu la parola
- **Problema:** il gioco articoli mostra sempre la parola tedesca: si allena il riconoscimento, mai il ricordo attivo ne' l'ortografia (maiuscola dei nomi, Umlaut).
- **Proposta:** interruttore nel gioco "Modalita': scegli / scrivi". In "scrivi" compare l'italiano (`traduzione_it`) e un campo dove digitare `der Tisch`. Il confronto e' tollerante e spiegato: `ae/oe/ue` accettati per `ä/ö/ü` e `ss` per `ß` con un avviso, nome minuscolo = "quasi: in tedesco i nomi si scrivono con la maiuscola". Tre bottoni `ä ö ü ß` sotto il campo per chi ha la tastiera italiana. Usa solo i dati gia' presenti.
- **Effetto per chi impara:** fissa articolo + parola insieme, nella direzione che serve per parlare (dall'italiano al tedesco).
- **Difficolta':** MEDIO (le traduzioni italiane possono essere ambigue: accettare piu' risposte non e' possibile senza nuovi dati, quindi si mostra la risposta attesa e un bottone "lo sapevo, conta giusta").
- **File toccati:** `web/app.js` (`giocoArticoli`, nuova funzione pura `confrontaScritta`), `web/style.css`.

### 8. Tasto Indietro, indirizzi e tastiera
- **Problema:** punto 6 sopra (Indietro esce dal sito) e su computer bisogna usare Tab/mouse per ogni risposta.
- **Proposta:** indirizzi `#articoli`, `#frasi`, `#errori` gestiti con l'evento `hashchange` (Indietro torna alla home, un link si puo' salvare tra i preferiti). Scorciatoie: `1/2/3` per der/die/das, `1/2` per le due frasi, `Invio` per Avanti/Controlla, `Backspace` per togliere l'ultimo blocco. Una riga in fondo al gioco che le elenca.
- **Effetto per chi impara:** meno attrito: su computer si fanno 30 parole in un minuto; su telefono non si perde il gioco con un gesto sbagliato.
- **Difficolta':** FACILE.
- **File toccati:** `web/app.js` (collegamenti in fondo a `avviaSito`, `mostraGioco`, `mostraHome`), `web/index.html` (eventuale riga di aiuto).

## La mia idea preferita e perche'

**L'idea 1, il ripasso intelligente.** Oggi il sito e' una buona "macchina di domande", ma non impara nulla da chi gioca: ogni risposta finisce in un contatore totale e la domanda dopo e' casuale. Con una scatola per record il sito diventa un vero allenatore: ripropone quello che non sai, lascia stare quello che sai e puo' dire "oggi hai 12 parole da ripassare", che e' anche il motivo migliore per tornare il giorno dopo. Costa poco (una funzione pura di scelta pesata, testabile con Node come le altre, e un formato dei progressi versione 2), non richiede contenuti nuovi, ed e' la base su cui poggiano bene le idee 2 ("rigioca solo questi") e 7. Va fatta presto, prima della prova con utenti, perche' cambia il formato salvato nel browser: farlo dopo vorrebbe dire migrare i progressi delle persone che hanno gia' provato.
