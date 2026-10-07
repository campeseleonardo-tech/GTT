origine: agente T19-scelta · stato: bozza

# Scelta del miglioramento da fare stasera (T19-scelta)

Ho letto le idee di T18-idee-a, T18-idee-b, T18-idee-c e `web/app.js` (insieme a `web/style.css` e `web/index.html`). Non ho eseguito nulla.

## Confronto

| idea | proposta da | valore | difficolta' |
|---|---|---|---|
| Ripasso degli sbagli (ripetere solo gli item sbagliati) | b (idea 1, per-item + "Ripassa errori"), c (idea 1, "debiti") | alto: e' la funzione che aiuta davvero a imparare | MEDIO |
| Mostrare la differenza / entrambe le frasi in "Trova l'errore" | a (idea 6), c (idea 3) | medio: rende visibile l'errore | FACILE |
| Mostrare l'articolo corretto sotto la parola grande dopo la risposta | a (idea 2) | basso: dopo la risposta il messaggio mostra gia' "articolo + parola" (`de-grande`) | MEDIO (poco utile) |
| Serie corrente + migliore nella barra | a (idea 1) | basso: la barra mostra gia' "Serie: n · Record: m" in `aggiornaBarra` | FACILE |
| Precisione % per gioco nella home | a (idea 5) | basso-medio | FACILE |
| Evidenziare i blocchi fuori posto in "Rimetti in ordine" | a (idea 3) | medio | MEDIO |
| Tastiera completa / meno ridisegni in `giocoFrasi` | b (idea 2) | medio (accessibilita') | MEDIO |
| Selezione adattiva con pesi | b (idea 3) | medio, dipende dal tracciamento per-item | MEDIO |
| Esporta / importa progressi (JSON) | b (idea 4) | medio ("proprieta' dei dati") | FACILE |
| Suggerimenti progressivi (hint) | b (idea 5) | medio | MEDIO |
| Validazione di `data.js` all'avvio | b (idea 6), c (problemi 2 e 6), a (problemi) | medio, ma e' un controllo tecnico | FACILE |
| Service worker / PWA offline | b (idea 7), c (idea 8) | medio, ma richiede file nuovi e hosting http(s) | MEDIO |
| Fine sessione con riepilogo errori | b (idea 8) | medio | MEDIO |
| Test con Node per le funzioni pure | c (idea 2) | indiretto | FACILE, ma NON tocca `web/` |
| Difficolta' graduale per numero di blocchi | c (idea 4) | medio | FACILE |
| Obiettivo giornaliero + streak | c (idea 6) | medio | MEDIO |
| "Le tue parole" (vocabolario personale) | c (idea 7) | medio | MEDIO |
| Messaggio "alternativa valida" | c (idea 5) | basso-medio | FACILE |
| Cambio livello durante il gioco -> torna alla home | a (idea 4) | basso: i giochi usano il pool preso all'avvio, quindi non si rompe nulla | FACILE |
| Conferma dopo "Azzera i progressi" | a (idea 7) | basso | FACILE |

Unica idea proposta da due modelli con alto valore: il **ripasso degli sbagli** (b e c). Anche "mostrare la differenza in Trova l'errore" e' proposta da due modelli (a e c), ma e' una rifinitura. Leo ha gia' scritto (nel file di c) di voler fare tutte e tre le idee principali di c in task separate: il ripasso e' la prima.

## Scelta

**Ripasso degli sbagli**: il sito ricorda in modo semplice quali record hai sbagliato e offre in home un ripasso che ripropone solo quelli, finche' non li indovini.

Perche' questa:
- proposta da due modelli su tre;
- e' la prima scelta di b e di c: chi impara vede ripetuto proprio cio' che sbaglia;
- nessun nuovo contenuto tedesco: usa i record gia' presenti in `data.js` (tramite il loro `id`);
- rischio basso: usa una chiave separata del browser (`langue_debiti_v1`), quindi `langue_progress_v1` e `sistemaProgresso` NON vengono toccati; per annullare basta togliere la chiave;
- si fa solo in `web/app.js`, `web/style.css`, `web/index.html`.

Regole funzionali (scelte di default, modificabili da Leo):
1. Si registra un "debito" quando una domanda viene sbagliata alla PRIMA risposta (articoli ed errori: risposta sbagliata; frasi: prima verifica sbagliata o soluzione mostrata). Ogni debito e' `id -> volte` (quante volte e' stato sbagliato).
2. Il debito si toglie SOLO nella modalita' ripasso e SOLO se si indovina al primo tentativo.
3. Massimo 50 debiti per gioco; se si supera, si scarta quello con `volte` piu' basso (a parita' il piu' vecchio).
4. Il ripasso non filtra per livello (A1/A2): ripassa quello che hai sbagliato, qualunque sia il livello scelto in home.
5. Le risposte nel ripasso contano nelle statistiche normali, come le altre.
6. In home, sotto le tre schede: una riga "Ripasso" con tre bottoni, uno per gioco, ognuno con il numero di sbagli da ripassare, disattivato se zero.

## Brief per chi la realizza

Si modificano SOLO `web/app.js`, `web/style.css`, `web/index.html`. Non si modifica nessun altro file. Nessun contenuto tedesco nuovo. Tutto il testo dell'interfaccia e' in italiano. Non si usa mai `innerHTML` (il file usa solo `textContent`). Tutto il codice che tocca il browser resta dentro try/catch.

### Passo 1 - funzioni pure (sezione "1. FUNZIONI PURE" di app.js)
Aggiungere, dopo `riepilogo`, queste funzioni pure (niente accesso a `window`/`document`), e aggiungerle a `module.exports`:
- `const MAX_DEBITI = 50;`
- `nuoviDebiti()`: restituisce `{ articoli: {}, frasi: {}, errori: {} }` (usare `GIOCHI`).
- `sistemaDebiti(grezzo)`: restituisce un oggetto valido partendo da qualsiasi valore letto dal browser. Per ogni gioco in `GIOCHI` tiene solo le voci con chiave stringa non vuota e valore valido secondo `interoSicuro(v) >= 1`, altrimenti scarta la voce. Se `grezzo` non e' un oggetto, restituisce `nuoviDebiti()`. Rispettare il limite `MAX_DEBITI` per gioco.
- `aggiungiDebito(debiti, gioco, id)`: se `id` non e' una stringa non vuota, non fa nulla. Altrimenti incrementa `debiti[gioco][id]` di 1 (parte da 0). Se le voci superano `MAX_DEBITI`, elimina quella con `volte` piu' basso (a parita' la prima nell'ordine delle chiavi). Restituisce `debiti`.
- `saldaDebito(debiti, gioco, id)`: elimina `debiti[gioco][id]` se esiste. Restituisce `debiti`.
- `elencoRipasso(debiti, gioco, records)`: restituisce i record della lista `records` il cui `id` e' in `debiti[gioco]` ed `eUsabile(record)` e' vero, ordinati per `volte` decrescente (a parita' ordine originale). I debiti senza record corrispondente si ignorano (non si cancellano qui).

### Passo 2 - salvataggio (sezione "2. SALVATAGGIO NEL BROWSER")
- `const CHIAVE_DEBITI = 'langue_debiti_v1';`
- `caricaDebiti(storage)` e `salvaDebiti(storage, debiti)`: stesso schema di `caricaProgresso` / `salvaProgresso` (try/catch, `storage` nullo -> `nuoviDebiti()` / `false`), ma con la chiave `CHIAVE_DEBITI` e `sistemaDebiti`.
- NON cambiare `CHIAVE_PROGRESSI`, `nuovoProgresso`, `sistemaProgresso`, `caricaProgresso`, `salvaProgresso`.

### Passo 3 - stato dentro `avviaSito()`
- Dopo `let progresso = caricaProgresso(storage);` aggiungere `let debiti = caricaDebiti(storage);`.
- Funzione `salvaDeb()`: chiama `salvaDebiti(storage, debiti)` (se fallisce non serve altro avviso: l'avviso di salvataggio esistente resta quello dei progressi).
- Funzione `nRipasso(gioco)`: `elencoRipasso(debiti, gioco, dati[gioco]).length`.

### Passo 4 - `creaSessione`
Aggiungere un parametro opzionale e NON cambiare il resto: `creaSessione(gioco, alProssimo)` resta uguale. In `sessione.registra(giusta)` non cambiare nulla (le statistiche normali restano). La logica dei debiti va nei tre giochi (passo 5), non qui.

### Passo 5 - i tre giochi
Per ognuno (`giocoArticoli`, `giocoFrasi`, `giocoErrori`) aggiungere un parametro `ripasso` (booleano, default falso). Quindi `giocoArticoli(ripasso)` ecc. ATTENZIONE: i bottoni della home usano `addEventListener('click', giocoArticoli)`, che passerebbe l'evento come primo argomento; cambiare i tre collegamenti in funzioni freccia/anonime: `function () { giocoArticoli(false); }`.
- Il pool: in modalita' normale resta `disponibili('...')` (non cambiare `disponibili`). In ripasso il pool si ricalcola a ogni domanda con `elencoRipasso(debiti, gioco, dati[gioco])` (cosi' un item appena saldato non esce piu').
- In `prossima()`: se il pool e' vuoto (cosa possibile in ripasso, oppure in normale se qualcosa va storto), NON chiamare `scegliCasuale` su `null` e NON fare `corrente.parola`: mostrare nel corpo il messaggio `Ripasso finito: non hai piu' sbagli da ripassare. Bravo!` (usare l'apostrofo tipografico come nel resto del file), svuotare il messaggio, e tornare. Questo controllo vale anche per la modalita' normale.
- Titolo in ripasso: passare a `mostraGioco` il titolo normale con il prefisso `Ripasso: ` (es. `Ripasso: Der, die o das?`).
- Registrare il debito: nel punto in cui si registra la PRIMA risposta sbagliata. In `giocoArticoli.rispondi` e `giocoErrori.rispondi`: se `!giusta`, `aggiungiDebito(debiti, 'articoli' / 'errori', corrente.id); salvaDeb();`. In `giocoFrasi`: nei due punti con `if (!registrata) sessione.registra(false);` (ramo sbagliato di `controllaClick` e `mostraSoluzione`) aggiungere il debito solo quando `!registrata` (cioe' prima di impostare `registrata = true`).
- Saldare il debito (solo se `ripasso` e' vero): in `giocoArticoli.rispondi` e `giocoErrori.rispondi` quando `giusta` -> `saldaDebito(...); salvaDeb();`. In `giocoFrasi.controllaClick` ramo giusto, solo se `!registrata` (prima del `registrata = true`) -> `saldaDebito(debiti, 'frasi', corrente.id); salvaDeb();`.
- Nel ripasso, nel messaggio dopo la risposta giusta si puo' aggiungere una riga `Sbaglio saldato.` (aggiungere solo in ripasso e solo se giusta).
- NON cambiare: `ordineMescolato` e la sua chiamata, `controllaOrdine`, il disegno dei blocchi (`disegna`), `opzioniErrore`, `normalizzaFrase`, la gestione del focus, `mostraSoluzione` (a parte il debito), i testi esistenti dei messaggi.
- Attenzione al caso `corrente` non nullo ma record senza `id`: `aggiungiDebito` ignora gli `id` non validi, quindi non serve altro controllo.

### Passo 6 - home
- In `web/index.html`, subito dopo la `<ul class="giochi">...</ul>` e prima di `<section class="progressi">`, inserire:
  ```
  <section class="ripasso" aria-labelledby="titolo-ripasso">
    <h2 id="titolo-ripasso">Ripasso degli sbagli</h2>
    <p class="nota">Rifai solo le domande che hai sbagliato. Quando le indovini, escono dalla lista.</p>
    <div class="ripasso-bottoni">
      <button type="button" id="ripasso-articoli" class="btn"></button>
      <button type="button" id="ripasso-frasi" class="btn"></button>
      <button type="button" id="ripasso-errori" class="btn"></button>
    </div>
  </section>
  ```
- In `aggiornaHome()`, nel ciclo `GIOCHI.forEach`, impostare il testo e `disabled` dei tre bottoni: testo `Ripassa parole (n)`, `Ripassa frasi (n)`, `Ripassa errori (n)` con `n = nRipasso(g)`; `disabled = (n === 0)`.
- Collegare i tre bottoni: click -> `giocoArticoli(true)`, `giocoFrasi(true)`, `giocoErrori(true)`.
- `azzera`: dopo `progresso = nuovoProgresso()` azzerare anche `debiti = nuoviDebiti(); salvaDeb();` (la conferma dice gia' "tutti i progressi": va bene, aggiornare il testo della conferma in `... progressi e la lista degli sbagli ...`).
- `web/style.css`: aggiungere la classe `.ripasso` con lo stesso aspetto di `.progressi` (sfondo `--carta`, bordo, raggio, padding, margine) e `.ripasso-bottoni` come `display: flex; flex-wrap: wrap; gap: 0.6rem;`. Usare solo le variabili esistenti (`--carta`, `--bordo`, `--raggio`). Non modificare altre regole.

### Cosa NON deve cambiare
- La chiave `langue_progress_v1` e la struttura di `nuovoProgresso` / `sistemaProgresso` / `registraRisposta` / `riepilogo`.
- `data.js`, qualsiasi file in `contenuti/`, `words_db.json`, `archivio/`.
- `disponibili`, `filtraPerLivello`, `eUsabile`, il filtro livello e la barra della serie.
- Nessuna nuova libreria, nessuna rete, nessun `innerHTML`, nessun nuovo file.

### Come controllare (senza eseguire nel browser, il validatore e' del runner)
1. Rileggere `app.js` cercando: `giocoArticoli`, `giocoFrasi`, `giocoErrori` ricevono `ripasso` e i tre collegamenti dei bottoni in home passano `false` (non l'evento).
2. Verificare a mano con la logica: `aggiungiDebito(nuoviDebiti(), 'articoli', 'art-0001')` -> `{articoli: {'art-0001': 1}, ...}`; ripetuto -> 2; `saldaDebito` -> voce rimossa; con 51 id diversi se ne tengono 50; `sistemaDebiti('x')` e `sistemaDebiti({articoli: {a: 'x'}})` -> nessuna voce.
3. Verificare che con pool vuoto non ci sia nessun accesso a `corrente.parola` / `corrente.blocchi` su `null`.
4. Verificare che tutte le nuove funzioni pure siano in `module.exports` e non usino `window`/`document`.
5. Nel rapporto scrivere chiaramente che NON e' stato provato nel browser e che il test manuale va fatto da Leo: sbagliare 2 parole, tornare in home, controllare "Ripassa parole (2)", giocarle bene, controllare che scendano a 0; ricaricare la pagina e controllare che il numero resti.

## Idee scartate e perche'

- **Mostrare l'articolo corretto sotto la parola grande (a, idea 2)**: dopo la risposta il messaggio mostra gia' "articolo + parola" in grande (`de-grande`) e i pulsanti mostrano ✓/✗; il valore aggiunto e' minimo.
- **Serie corrente + migliore (a, idea 1)**: `aggiornaBarra` mostra gia' "Serie: n · Record: m". L'idea parte da un problema che non c'e'.
- **Cambio livello durante il gioco (a, idea 4)**: i giochi leggono il pool all'avvio e il filtro e' visibile solo nella home, quindi non c'e' vero rischio.
- **Diff / frase scelta in "Trova l'errore" (a idea 6, c idea 3)**: ottima, proposta da due modelli, ma e' una rifinitura; consigliata come task successivo (Leo l'ha gia' indicata fra le tre di c).
- **Precisione % per gioco (a, idea 5)**: utile ma poco didattica; la home mostra gia' la percentuale totale in `riepilogo`.
- **Evidenziare i blocchi fuori posto (a, idea 3)**: richiede di toccare `disegna`, che e' la parte piu' fragile del sito mai provata nel browser; meglio rimandare.
- **Tastiera completa / riscrittura di `giocoFrasi` (b, idea 2)**: riscrittura grande su codice mai eseguito; rischio alto per una sola notte. Il "bug" citato (la risposta giusta dopo "Ricomincia" non conteggiata) in realta' e' voluto: la prima verifica conta una sola volta.
- **Selezione adattiva (b, idea 3)**, **fine sessione (b, idea 8)**: dipendono dal tracciamento per-item; si possono fare dopo il ripasso, riusando i debiti.
- **Esporta / importa progressi (b, idea 4)**: bella ma non insegna tedesco; da fare in un task separato.
- **Hint progressivi (b, idea 5)**: cambia il significato delle statistiche (risposte assistite) e va deciso da Leo.
- **Validazione di `data.js` a runtime (b idea 6, c problemi 2 e 6)**: e' un controllo tecnico, il validatore del runner copre gia' i contenuti.
- **Service worker / PWA (b idea 7, c idea 8)**: richiede file nuovi (`sw.js`, manifest) e un hosting http(s); fuori dal perimetro (solo app.js, style.css, index.html) e da_verificare come verra' ospitato il sito.
- **Test con Node (c, idea 2)**: utile, ma non migliora il sito e richiede un file nuovo fuori da `web/`; da fare come task a parte.
- **Difficolta' graduale, obiettivo giornaliero + streak, "Le tue parole", messaggio "alternativa valida" (c)**: validi ma di valore minore del ripasso; le prime due cambiano l'esperienza di gioco e vanno decise da Leo.
- **Conferma dopo "Azzera i progressi" (a, idea 7)** e **intestazioni accessibili (a, idea 8)**: valore basso o poco chiaro.
- **Segnalati ma non scelti (problemi del codice)**: rischio di `scegliCasuale` su pool vuoto in `prossima()` (c); lo risolve il passo 5 del brief; `mostraSoluzione` conta come "sbagliato" (c) e' una scelta di Leo da confermare; i bottoni in `rimasti` restano attivi dopo la soluzione (c): da correggere in un task separato.
