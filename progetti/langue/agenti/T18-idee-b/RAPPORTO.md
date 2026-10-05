# Rapporto T18-idee-b

## Cosa ho fatto
Letto i 5 file di riferimento (PROGETTO.md, SCHEMA.md, web/index.html, web/app.js, web/style.css) e analizzato il codice a freddo (senza eseguirlo) per individuare problemi concreti e proporre 8 idee migliorative fattibili in plain HTML/CSS/JS.

## Cosa ho controllato
- Struttura dati `LANGUE_DATA` e validazione assente all'avvio (`avviaSito` riga 155)
- Funzioni pure: `mescola`, `scegliCasuale`, `normalizzaFrase`, `controllaOrdine`, `ordineMescolato`, `opzioniErrore`, progressi
- Storage: `trovaStorage`, `caricaProgresso`, `salvaProgresso` (sincroni, ogni risposta)
- Tre giochi: `giocoArticoli`, `giocoFrasi`, `giocoErrori` — logica, UI, accessibilità, bug potenziali
- CSS: variabili, dark mode, focus-visible, reduced-motion, contrasto focus dark mode
- Schema contenuti: campi obbligatori, regole `blocchi`, `spiegazione_it`, `alternative`

## Scelte (default sensati usati)
- Idee limitate a **nessun nuovo contenuto tedesco**, **nessun server/libreria**, **solo file web/** e `app.js`/`index.html`/`style.css`.
- Difficoltà stimate: FACILE = <2h, MEDIO = 2-6h, DIFFICILE = >6h per un dev che conosce il codebase.
- Ordine idee: per impatto didattico × fattibilità, non per facilità.
- Bug segnalati (es. `registrata` non resettata in "Ricomincia" Frasi, `normalizzaFrase` ignora capitalizzazione) sono verificabili leggendo il codice.

## Per Leo: da decidere / rivedere
1. **Priorità**: quale idea sviluppare per prima? (La mia raccomandazione: Idea 1 → base per 3 e 8)
2. **Modalità adattiva (Idea 3)**: default ON o OFF? A1 puristi potrebbero volere ordine casuale puro.
3. **Hint (Idea 5)**: contano come "tentativo" nello score? Proposta: sì, contatore separato `hintUsati`.
4. **Service Worker (Idea 7)**: richiede HTTPS (localhost ok, file:// no). Va bene per deploy GitHub Pages/Netlify?
5. **Contrasto focus dark mode**: `--focus: #ffb454` su `--carta: #1c212d` è 2.8:1 (sotto WCAG AA). Cambiare `--focus` dark a `#ffcc00` (4.5:1) o `#ffd600`?

## Note
- File `data.js` non fornito:假设 è array di record conformi a `SCHEMA.md`.
- Nessun `ANSWERS.md` né `DECISIONS.md` esistenti in `agenti/T18-idee-b/`.
- Nessuna `DOMANDE.md` creata: le 5 questioni sopra sono nel rapporto per comodità Leo.
</parameter>
</invoke>
</minimax:tool_call>
