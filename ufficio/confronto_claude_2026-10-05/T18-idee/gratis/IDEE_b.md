# Idee per migliorare Langue (T18-idee-b)

Analisi del codice esistente (`web/index.html`, `web/app.js`, `web/style.css`, `SCHEMA.md`, `PROGETTO.md`) senza averlo eseguito. Il sito non è mai stato testato in browser.

---

## Problemi che vedo nel codice attuale

1. **`disegna()` in `giocoFrasi()` ricrea tutto il DOM a ogni click** (righe 400-470): perde il focus tastiera, sfarfalla su mobile, e `registrata`/`chiusa` non si resettano bene con "Ricomincia" dopo una risposta sbagliata → la risposta giusta successiva non viene conteggiata.

2. **`ordineMescolato()` (riga 68) usa confronto stringa con separatore `\u0001`**: se un blocco contiene quel carattere (improbabile ma possibile), il confronto fallisce e restituisce ordine originale.

3. **`normalizzaFrase()` (riga 56) ignora maiuscole/minuscole**: nasconde errori di capitalizzazione dei sostantivi (es. "ich" vs "Ich", "deutsch" vs "Deutsch") — cruciale in tedesco.

4. **`caricaProgresso()` / `salvaProgresso()` (righe 115-130) sincroni su ogni risposta**: `localStorage` blocca il main thread; su dispositivi lenti o storage pieno l'UI si pianta senza feedback.

5. **Nessuna validazione di `window.LANGUE_DATA` all'avvio** (riga 155): se `data.js` manca, ha sintassi errata, o campi obbligatori assenti, i giochi partono con array vuoti e l'avviso generico "Nessun contenuto" non dice *cosa* manca.

6. **Selezione item puramente casuale (`scegliCasuale`, riga 45)**: nessun adattamento alla storia dell'utente; item sbagliati più volte non riappaiono prima, item facili sprecano tempo.

7. **Gioco "Errori": entrambe le frasi visibili insieme** (riga 530) → confronto visivo banale (lunghezza, parole diverse) invece che conoscenza grammaticale; manca opzione "mostra solo una frase alla volta".

8. **Progresso solo aggregato (`riepilogo()`, riga 103)**: impossibile sapere *quali* parole/frasi/ errori danno problemi; niente "modalità ripasso errori".

9. **Nessun export/import progressi**: cambio browser/dispositivo = perdita totale; nessun backup manuale.

10. **Gioco "Articoli": niente plurali, niente "mostra risposta" senza penalità**: A1 richiede `die` plurale per tutti i generi; utente bloccato deve sbagliare apposta per vedere la soluzione.

11. **`avvisoSalvataggio` (riga 161) controlla `storage !== null` MA chiama `salvaProgresso` che scrive davvero**: se storage pieno, l'avviso appare *dopo* il tentativo fallito, non prima.

12. **CSS: `--focus: #ffb454` (dark mode) su `--carta: #1c212d`** → contrasto ~2.8:1, sotto WCAG AA (3:1 per UI); focus invisibile per alcuni utenti.

---

## Idee (8, ordinate per impatto/ fattibilità)

### 1. Tracciamento per-item + modalità "Ripassa i tuoi errori"
**Problema**: `progresso.giochi[g]` conta solo totali (riga 103). L'utente non sa *cosa* rivedere.
**Proposta**: Aggiungere in `progresso.giochi[g].perItem` un oggetto `{ [id]: { giusti: n, sbagliati: n, ultimaData: ts } }`. Nuovo pulsante in home "Ripassa errori" per gioco → pesca solo item con `sbagliati > 0` ordinati per frequenza errore.
**Effetto**: studio mirato, riparazione buchi concreti, sensazione di progresso tangibile.
**Difficoltà**: MEDIO
**File toccati**: `app.js` (`nuovoProgresso`, `sistemaProgresso`, `registraRisposta`, `riepilogo`, `avviaSito` home UI, `creaSessione` per filtro pool), `index.html` (pulsanti home), `style.css` (stile nuovo pulsante).

### 2. Navigazione tastiera completa nel gioco "Frasi"
**Problema**: `disegna()` ricrea bottoni blocchi a ogni click (riga 400); focus perso; nessun ordine logico Tab; "Ricomincia" lascia `registrata=true` → risposta giusta dopo non conteggiata (bug riga 455-460).
**Proposta**: Riscrivere `giocoFrasi` come *single-page state machine*: un unico render iniziale, poi sposta blocchi tra liste "disponibili" e "costruita" via `appendChild` (niente `svuota`/`appendChild` massivo). Gestione tastiera: `Tab`/`Shift+Tab` naviga blocchi, `Enter`/`Spazio` sposta, `Backspace` rimuove ultimo, `C` controlla, `R` ricomincia, `S` soluzione. Fix bug `registrata` resettandola in `prossima()` e in "Ricomincia".
**Effetto**: accessibilità reale (WCAG 2.1.1), velocità power-user, niente sfarfallio, bug fix incluso.
**Difficoltà**: MEDIO
**File toccati**: `app.js` (`giocoFrasi` intero), `style.css` (stati focus visibili per blocchi).

### 3. Selezione adattiva "spaced-repetition lite" (senza server)
**Problema**: `scegliCasuale` (riga 45) ignora storia utente; item facili e difficili stessa probabilità.
**Proposta**: Peso per item = `1 + sbagliati * 2 - giusti * 0.5` (min 0.1). `scegliCasualePesato(pool, pesi, rng, escludi)` usa cumulative weights. Pesi salvati in `progresso.giochi[g].perItem` (vedi Idea 1). Opzione in home "Modalità adattiva" (default off per A1 puristi).
**Effetto**: tempo speso dove serve, curva apprendimento più ripida, meno noia su item noti.
**Difficoltà**: MEDIO
**File toccati**: `app.js` (nuova funzione, `creaSessione` usa pesi se modalità attiva, `registraRisposta` aggiorna pesi), `index.html` (toggle home), `style.css`.

### 4. Export/Import progressi (file JSON)
**Problema**: Progressi bloccati nel browser; niente backup, niente sync dispositivi.
**Proposta**: Due pulsanti in sezione progressi home: "Scarica progressi" → `Blob` + `URL.createObjectURL` + click link `download="langue-progress-<data>.json"`; "Carica progressi" → `<input type="file" accept=".json" hidden>` + `FileReader` + `sistemaProgresso()` + `salva()`. Validazione schema `versione`, `livello`, `giochi`.
**Effetto**: proprietà dati utente, migrazione browser/dispositivo, backup prima pulizia cache.
**Difficoltà**: FACILE
**File toccati**: `app.js` (due funzioni export/import, collegamento UI), `index.html` (due bottoni + input file hidden), `style.css`.

### 5. Sistema hint progressivi (non-rivelatori)
**Problema**: Gioco Articoli: nessun aiuto prima di rispondere; Errore: due frasi a confronto visivo; Frasi: niente hint.
**Proposta**: Pulsante "Hint" (massimo 1 per domanda, conta come "tentativo assistito" in stats):
- Articoli: colora bordo bottone corretto (der=blu, die=rosso, das=verde) — codice colore genere, non risposta diretta.
- Frasi: evidenzia primo blocco corretto (bordo lampeggiante) o mostra primo carattere di ogni blocco.
- Errori: nasconde una frase; mostra "Questa frase ha un errore di [categoria]" (da `record.categoria`).
Hint disabilitato se "Modalità esame" attiva (nuovo toggle home).
**Effetto**: scaffolding pedagogico, riduce frustrazione, insegna pattern (genere → colore, categoria errore → attenzione mirata).
**Difficoltà**: MEDIO
**File toccati**: `app.js` (logica hint in ogni gioco, contatore `hintUsati` in sessione, stats), `index.html` (pulsante hint + toggle esame), `style.css` (stili hint attivo, colori genere).

### 6. Validazione robusta `data.js` all'avvio + fallback incolla JSON
**Problema**: `avviaSito()` (riga 155) assume `window.LANGUE_DATA` valido; malformazioni silenziose → giochi vuoti, avviso generico.
**Proposta**: Funzione `validaDati(grezzi)` che controlla: esistenza array `articoli`/`frasi`/`errori`; ogni record ha `id`, `tipo`, `livello`, `stato`, campi tipo-specifici obbligatori (per schema); `blocchi` length 4-9 e join = `testo_de`; `spiegazione_it` ≥ 20 char. Restituisce `{ validi: {}, errori: [] }`. Se errori: mostra elenco specifico in `avviso-dati` (es. "frasi: 3 record senza 'blocchi', 1 'testo_de' non match"). Pulsante "Incolla JSON corretto" → `textarea` + parsing + sostituzione `dati` in memoria (senza salvare su disco).
**Effetto**: debug immediato per Leo (che rilegge 20%), sito non si rompe per typo in data.js, recovery manuale senza rebuild.
**Difficoltà**: FACILE
**File toccati**: `app.js` (`validaDati`, `avviaSito` usa validazione), `index.html` (textarea + pulsante in avviso), `style.css`.

### 7. Service Worker offline-first (app shell + data.js)
**Problema**: Sito statico ma niente cache; offline = schermata bianca browser.
**Proposta**: `sw.js` con strategie: `index.html`, `style.css`, `app.js` → `cache-first` (precache install); `data.js` → `stale-while-revalidate` (serve cache, aggiorna in background); `POST`/`localStorage` non toccati. Registrazione in `index.html` inline script prima di `app.js`. Messaggio "Funziona offline" in footer se `navigator.serviceWorker.controller`.
**Effetto**: vero offline (treno, aereo), caricamento istantaneo repeat visit, PWA-ready senza manifest.
**Difficoltà**: MEDIO
**File toccati**: nuovo `web/sw.js`, `index.html` (registrazione SW + messaggio), `app.js` (nessuno, ma `data.js` deve essere cachable — già stesso dominio).

### 8. Schermata "Fine sessione" con riepilogo errori + deep link item
**Problema**: Feedback solo per domanda corrente; niente sintesi sessione; utente chiude gioco e perde contesto errori.
**Proposta**: Dopo N domande (default 10, configurabile) o click "Torna home" durante gioco → mostra schermata: "Sessione: 7/10 giuste. Errori: 3." Lista cliccabile: "✗ der Tisch (hai detto die) — riprova" → click riapre gioco *solo su quell'item* (modalità "ripassa questo"). Salvataggio `ultimaSessione` in progresso per revisita home.
**Effetto**: chiusura cognitiva, riparazione immediata, motivazione "ancora uno per chiudere bene".
**Difficoltà**: MEDIO
**File toccati**: `app.js` (`creaSessione` conta domande, `mostraFineSessione`, `riprendiItem(id)`), `index.html` (area messaggio estesa), `style.css` (layout lista errori sessione).

---

## La mia idea preferita e perché

**Idea 1: Tracciamento per-item + modalità "Ripassa i tuoi errori"**

**Perché**:
- Risolve il buco pedagogico più grande: l'utente *non sa cosa non sa*. Oggi vede "Giuste: 23, Sbagliate: 7" ma non *quali* 7.
- Abilita le Idee 3 (pesi adattivi) e 8 (riepilogo sessione) senza riscrivere tutto.
- Cambio minimo al data model (`progresso.giochi[g].perItem` oggetto piatto), retrocompatibile: `sistemaProgresso()` lo inizializza vuoto se assente.
- Leo (C1 tedesco) può verificare facilmente: apre DevTools → `localStorage.langue_progress_v1` → vede esattamente quali `id` hanno `sbagliati > 0` e controlla se il contenuto è colpa sua o dell'utente.
- Nessun nuovo contenuto tedesco, nessuna libreria, nessun server. Solo JS puro e un pulsante in più in home.
- Impatto percepito alto: "Finalmente ripasso *solo* quello che sbaglio" è la feature #1 che gli utenti A1-A2 chiedono in app tipo Anki/Quizlet.

**Seconda scelta**: Idea 2 (tastiera Frasi) — fixa un bug reale + accessibilità, ma impatto didattico minore.
**Terza**: Idea 4 (export/import) — banale da fare, alto valore "proprietà dati", ma non insegna tedesco.
