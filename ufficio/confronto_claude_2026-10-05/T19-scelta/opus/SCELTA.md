origine: agente T19-scelta · stato: bozza

# Scelta del miglioramento per stanotte (T19-scelta)

Fonti lette: `agenti/T18-idee-a/IDEE.md`, `agenti/T18-idee-b/IDEE.md`, `agenti/T18-idee-c/IDEE.md` (tutti e tre presenti), `web/app.js`, `web/style.css`, `web/index.html`. Nulla è stato eseguito: le osservazioni sul codice vengono dalla sola lettura.

## Confronto

| Idea | Proposta da | Valore | Difficolta' |
|---|---|---|---|
| Ripasso degli sbagli (lista per gioco degli item sbagliati + sessione "Ripassa") | b (idea 1), c (idea 1) | alto: si ripete proprio cio' che si sbaglia | MEDIA |
| Evidenziare la differenza fra frase sbagliata e corretta in "Trova l'errore" | a (idea 6), c (idea 3) | medio-alto | MEDIA (diff fra parole) |
| Offline / installabile (service worker, PWA) | b (idea 7), c (idea 8) | medio | MEDIA; da_verificare: non funziona aprendo il file da disco (`file://`); richiede un nuovo file `web/sw.js` |
| Selezione adattiva "spaced repetition lite" | b (idea 3) | alto | MEDIA-ALTA; dipende dal ripasso |
| Riepilogo di fine sessione con lista errori | b (idea 8) | medio | MEDIA |
| Mostrare l'articolo giusto dopo la risposta | a (idea 2) | basso: **gia' fatto** (`rispondi` in `giocoArticoli` mostra gia' "articolo + parola" e la traduzione) | - |
| Serie corrente + migliore nella barra | a (idea 1) | basso: **gia' fatto** (`aggiornaBarra`: "Serie: n · Record: m") | - |
| Tornare alla home se si cambia livello durante il gioco | a (idea 4) | basso: il filtro livello e' solo nella home, durante il gioco non e' visibile | FACILE |
| Percentuale di giuste per gioco | a (idea 5) | basso | FACILE |
| Messaggio "Progressi azzerati" | a (idea 7) | basso | FACILE |
| Intestazioni / ARIA della vista gioco | a (idea 8), c (problema 7) | medio (accessibilita') | FACILE-MEDIA |
| Tastiera completa e niente ridisegno in "Rimetti in ordine" | b (idea 2) | medio (accessibilita') | MEDIA-ALTA (riscrive `giocoFrasi`) |
| Export / import dei progressi | b (idea 4) | medio (non insegna tedesco) | FACILE |
| Aiuti progressivi (hint) | b (idea 5) | medio | MEDIA |
| Validazione di `data.js` all'avvio + incolla JSON | b (idea 6), vicino a c (problemi 2 e 6) | medio, soprattutto per Leo | MEDIA |
| Suite di test con node | c (idea 2) | alto per la sicurezza dei cambi | FACILE, ma crea file fuori da `web/` |
| Difficolta' graduale per numero di blocchi | c (idea 4) | medio | FACILE |
| Dire quando l'ordine e' una "alternativa" valida | c (idea 5) | medio | FACILE |
| Obiettivo giornaliero + giorni di fila | c (idea 6) | medio (motivazione) | MEDIA |
| "Le tue parole" (rubrica personale) | c (idea 7) | medio; si sovrappone al ripasso | MEDIA |

## Scelta

**Ripasso degli sbagli**: proposta da due modelli su tre (b e c, entrambi come idea preferita), realizzabile toccando solo `web/app.js`, `web/index.html` e `web/style.css`, senza nessun nuovo contenuto tedesco (riusa i record gia' in `data.js`).

Come funziona per chi impara:
- ogni risposta sbagliata (o "Mostra la soluzione") mette quell'item in una lista di ripasso del suo gioco;
- in home compare una sezione "Ripassa i tuoi sbagli" con un pulsante per gioco e il numero di item da ripassare;
- il pulsante apre lo stesso gioco di sempre, ma pescando solo fra gli item della lista;
- quando un item viene indovinato al primo tentativo, esce dalla lista; quando la lista e' vuota il gioco dice "Hai ripassato tutto" e propone di tornare alla home.

Versione "piccola" per stanotte (cosa NON fa): niente pesi adattivi, niente date, niente riepilogo di fine sessione. Il ripasso sta in una **chiave separata** del browser (scelta del modello c), cosi' il formato dei progressi esistenti (`langue_progress_v1`) non cambia.

## Brief per chi la realizza

File da toccare: solo `web/app.js`, `web/index.html`, `web/style.css`. Nessun altro file.

### 1. `web/app.js`, sezione 1 (funzioni pure) - aggiungere
1. `nuovoRipasso()` -> `{ versione: 1, giochi: { articoli: {}, frasi: {}, errori: {} } }`. Ogni gioco e' un oggetto `{ [id]: volte }` (volte = numero di sbagli, intero >= 1).
2. `sistemaRipasso(grezzo)`: come `sistemaProgresso`, costruisce un ripasso valido da un oggetto qualsiasi: tiene solo le chiavi di `GIOCHI`, solo id stringa non vuoti, solo `volte` intere >= 1 (usare `interoSicuro`), al massimo 50 id per gioco (se sono di piu' tenere quelli con `volte` piu' alto).
3. `aggiornaRipasso(ripasso, gioco, id, giusta)`: se `id` non e' una stringa non vuota non fa nulla; se `giusta` -> `delete ripasso.giochi[gioco][id]`; altrimenti `volte + 1` (o 1 se nuovo) e poi applica il tetto di 50 (togliendo l'id con `volte` piu' basso, ma mai quello appena aggiunto). Restituisce `ripasso`.
4. `idDaRipassare(ripasso, gioco)` -> lista degli id del gioco.
5. Aggiungere queste 4 funzioni a `module.exports`, **senza togliere** nessuna delle funzioni gia' esportate.

### 2. `web/app.js`, sezione 2 (salvataggio) - aggiungere
- `const CHIAVE_RIPASSO = 'langue_ripasso_v1';`
- `caricaRipasso(storage)` e `salvaRipasso(storage, ripasso)` copiando la struttura di `caricaProgresso` / `salvaProgresso` (sempre dentro try/catch, mai eccezioni verso l'esterno).

### 3. `web/app.js`, sezione 3 (interfaccia) - modificare
1. In `avviaSito`: `let ripasso = caricaRipasso(storage);` subito dopo `progresso`. In `salva()` salvare anche il ripasso (l'avviso di salvataggio resta com'e': basta il risultato di `salvaProgresso`).
2. `creaSessione(gioco, alProssimo)`: `sessione.registra(giusta)` diventa `sessione.registra(giusta, id)`; dentro, dopo `registraRisposta(...)` chiamare `aggiornaRipasso(ripasso, gioco, id, giusta)` e poi `salva()` (una sola volta).
3. Nei tre giochi passare l'id: `sessione.registra(giusta, corrente.id)` in `giocoArticoli.rispondi`, `sessione.registra(true/false, corrente.id)` nei tre punti di `giocoFrasi` (`controllaClick` due volte, `mostraSoluzione` una), `sessione.registra(scelta.corretta, corrente.id)` in `giocoErrori.rispondi`. Restano invariate le regole esistenti (in "Rimetti in ordine" conta solo il primo controllo: quindi un item sbagliato al primo controllo e poi corretto resta nella lista, ed e' giusto cosi').
4. Nuova funzione `disponibiliRipasso(gioco)` = `disponibili(gioco)` filtrata sugli id in `idDaRipassare(ripasso, gioco)`. Rispetta quindi anche il filtro di livello.
5. Ogni gioco riceve un parametro `modoRipasso` (booleano). **Attenzione**: oggi i giochi sono collegati con `addEventListener('click', giocoArticoli)`, che passa l'evento come primo argomento. Collegarli invece con funzioni esplicite: `function () { giocoArticoli(false); }` per le schede normali e `function () { giocoArticoli(true); }` per i pulsanti di ripasso (idem per frasi ed errori).
6. In modo ripasso, dentro `prossima()` di ogni gioco: ricalcolare il pool con `disponibiliRipasso(gioco)` a ogni domanda (gli item indovinati spariscono subito). Se il pool e' vuoto: `svuota(sessione.corpo)`, `sessione.messaggio('ok', [{ testo: 'Hai ripassato tutto: bravo!', classe: 'esito' }])` e nessuna domanda (non chiamare `scegliCasuale` con lista vuota: oggi `corrente.parola` andrebbe in errore). In modo normale il pool resta quello calcolato una volta, come adesso.
7. Titolo della vista in modo ripasso: titolo del gioco + " – ripasso" (es. "Der, die o das? – ripasso"), cosi' si capisce dove si e'.
8. `aggiornaHome()`: per ogni gioco aggiornare il pulsante `ripassa-<gioco>`: testo "<nome gioco> (n)" con n = `disponibiliRipasso(g).length`, `disabled` se n = 0. Se tutti e tre sono 0 mostrare la nota `ripasso-vuoto`.
9. Pulsante `azzera`: dopo l'azzeramento dei progressi azzerare anche il ripasso (`ripasso = nuovoRipasso()`) e cambiare il testo della conferma in "Vuoi azzerare tutti i progressi e la lista di ripasso salvati in questo browser?" (scelta provvisoria, vedi DOMANDE.md).

### 4. `web/index.html` - aggiungere
Dopo la `</ul>` dei giochi e prima della sezione "I tuoi progressi":
```html
<section class="ripasso" aria-labelledby="titolo-ripasso">
  <h2 id="titolo-ripasso">Ripassa i tuoi sbagli</h2>
  <p class="nota">Qui tornano solo le domande che hai sbagliato. Quando le indovini, escono dalla lista.</p>
  <p class="nota" id="ripasso-vuoto" hidden>Per ora non c&rsquo;&egrave; niente da ripassare.</p>
  <div class="ripasso-bottoni">
    <button type="button" id="ripassa-articoli" class="btn">Der, die o das?</button>
    <button type="button" id="ripassa-frasi" class="btn">Rimetti in ordine</button>
    <button type="button" id="ripassa-errori" class="btn">Trova l&rsquo;errore</button>
  </div>
</section>
```
(I pulsanti stanno fuori dalle schede: una `<button>` non puo' contenerne un'altra.)

### 5. `web/style.css` - aggiungere
- `.ripasso` con lo stesso aspetto di `.progressi` (carta, bordo, raggio, padding).
- `.ripasso-bottoni { display: flex; flex-wrap: wrap; gap: 0.6rem; }`
- `.ripasso-bottoni .btn:disabled { opacity: 0.6; }`
Usare solo le variabili esistenti (`--carta`, `--bordo`, `--raggio`...), cosi' il tema scuro funziona da solo.

### Cosa NON deve cambiare
- Il formato e la chiave di `langue_progress_v1`, `nuovoProgresso`, `sistemaProgresso`, `registraRisposta`, `riepilogo`: i progressi gia' salvati devono continuare a funzionare.
- Il comportamento dei giochi in modo normale (domande, messaggi, conteggi, serie).
- Nessun `innerHTML`: costruire tutto con `el()` / `bottone()` come il resto del file.
- Nessun contenuto tedesco nuovo, nessun file di dati toccato (`data.js`, `contenuti/`, `words_db.json`, `archivio/`).
- Nessuna libreria, nessuna rete, nessun nuovo file.

### Come controllarlo (a mano, nel browser)
1. Aprire `web/index.html`: la sezione "Ripassa i tuoi sbagli" mostra tre pulsanti disattivati e la nota "niente da ripassare".
2. Giocare a "Der, die o das?" e sbagliare 2 parole apposta; tornare alla home: il pulsante dice "(2)" ed e' attivo.
3. Aprire il ripasso: escono solo quelle 2 parole; indovinarne una e premere Avanti: resta solo l'altra; indovinare anche quella: compare "Hai ripassato tutto".
4. In "Rimetti in ordine" premere "Mostra la soluzione": la frase entra nel ripasso.
5. Ricaricare la pagina: i numeri del ripasso restano; i progressi di prima sono identici.
6. Cambiare livello in A1: il numero del ripasso conta solo gli item A1.
7. "Azzera i progressi": anche il ripasso torna a zero.
8. Con il localStorage bloccato (finestra privata in alcuni browser) il sito non deve dare errori: il ripasso vale solo per la pagina aperta.
9. Se il runner ha un controllo con node sulle funzioni esportate, deve continuare a trovare tutte quelle di prima.

Da verificare prima di iniziare: che i record dentro `web/data.js` abbiano davvero il campo `id` (gli id del tipo `art-0201`, `fra-0001`, `err-0001` esistono nei file di contenuto, ma `data.js` non l'ho letto). Se un record non ha `id`, non entra nel ripasso (punto 1.3), senza errori.

## Idee scartate e perche'

- **Mostrare l'articolo giusto (a-2)** e **serie corrente + migliore (a-1)**: gia' presenti nel codice attuale.
- **Tornare alla home cambiando livello (a-4)**: il filtro livello si vede solo nella home, quindi il problema descritto non si verifica.
- **Diff della frase in "Trova l'errore" (a-6, c-3)**: proposta da due modelli e utile, ma serve un confronto parola per parola con casi limite (errori di ordine, maiuscole): meglio come task successiva, si sposa bene con il ripasso.
- **Offline / PWA (b-7, c-8)**: proposta da due modelli, ma richiede un nuovo file `web/sw.js` (fuori dai tre file ammessi) e non funziona aprendo la pagina da disco; dipende da come verra' pubblicato il sito.
- **Selezione adattiva (b-3)**, **riepilogo di fine sessione (b-8)**, **"Le tue parole" (c-7)**: costruiscono sopra il ripasso; prima va fatto il ripasso semplice.
- **Tastiera completa in "Rimetti in ordine" (b-2)**: riscrive tutto `giocoFrasi`, troppo per una notte. Nota: il "bug" descritto (dopo "Ricomincia" la risposta giusta non viene conteggiata) e' in realta' una regola voluta (`registrata`: conta solo il primo controllo).
- **Maiuscole ignorate in `normalizzaFrase` (problema b-3)**: e' una scelta documentata nel commento della funzione (i blocchi hanno forma fissa), non un errore.
- **Suite di test (c-2)**: utilissima, ma crea un file fuori da `web/`; da fare in una task a parte, idealmente subito dopo.
- **Validazione di `data.js` (b-6)**, **export/import (b-4)**, **hint (b-5)**, **obiettivo giornaliero (c-6)**, **difficolta' graduale (c-4)**, **alternative esplicite (c-5)**, **percentuale (a-5)**, **messaggio di azzeramento (a-7)**, **accessibilita' intestazioni (a-8)**: valide ma con meno effetto sull'apprendimento, oppure piccole migliorie da raggruppare in una task di rifinitura.
- **Piccolo bug reale da tenere in lista** (c, problema 4): dopo "Mostra la soluzione" i blocchi in `rimasti` restano attivi (in `disegna` si disattivano solo quelli in `costruita`). Correzione di una riga, da fare in una task separata per non mescolare i cambi.
