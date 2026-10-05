# Scheda progetto: Langue

Documento centrale del progetto: impostazioni, regole e stato. Tutto quello che sta SOPRA la riga "STATO DELL'UFFICIO" e' tuo: lo leggono anche gli agenti a ogni task. La parte sotto la aggiorna l'Ufficio da solo.

## Obiettivo
Sito per italiani che imparano il tedesco (A1-A2) con 3 giochi

## Per chi e contesto
(da scrivere: per chi e', cosa conta di piu', cosa evitare)

## Regole per gli agenti
PROJECT: Langue (provisional name). Static website (plain HTML/CSS/JS, no server) to help ITALIAN beginners (A1-A2) learn GERMAN. Interface and explanations are in ITALIAN. Progress is stored only in the user's browser.
Content types: "articolo" (noun + der/die/das + Italian translation), "frase" (German sentence split into blocks to reorder), "errore" (typical mistakes of Italians learning German: wrong sentence, corrected sentence, explanation in Italian), "consiglio" (media tips, later).
Quality rules:
- German must be correct, natural, standard (Hochdeutsch), A1-A2 vocabulary and grammar. If you are not sure about an article, a plural or a translation, do NOT include that item (or mark "da_verificare" and explain in "note" if the schema allows). Avoid nouns whose article varies by region or variant.
- Italian translations must be natural, not word-for-word.
- Never reproduce song lyrics, poems or passages from books; never invent titles, quotes or sources.
- The user (Leo) speaks German at C1 level and rereads about 20% of everything you produce: make that review easy (consistent formatting, short clear notes).
- Existing data of the user is never edited by you: words_db.json, contenuti/parole.json and everything under archivio/ stay untouched unless the task says so.

## Note e direzioni di Leo
(da scrivere)

<!-- STATO DELL'UFFICIO: inizio. Questa parte la riscrive l'Ufficio dopo ogni task: non scrivere qui, scrivi sopra. -->
## Stato dell'Ufficio (aggiornato 05/10/2026 13:57)

### Piano
- [x] Pulizia + schema (fatto) - T01-pulizia, T02-schema, T03-conversione
- [x] Contenuti v1 (fatto) - T07-parole, T08-frasi, T10-errori, T11-revisione
- [x] Contenuti v2 (fatto) - T12-parole2, T13-frasi2, T14-errori2
- [x] Sito (fatto) - T15-dati-web, T16-sito
- [ ] Prova con utenti (da fare)

### Fatto di recente
- 2026-10-05 13:57 · T22-ripasso-fix: (il modello non ha scritto un riassunto)
- 2026-10-05 13:51 · T22-ripasso-fix: Google AI Studio: errore 404
- 2026-10-05 13:51 · T23-prova-guidata: Google AI Studio: errore 404
- 2026-10-05 13:03 · T20-esegui-b: Implementato "Ripasso degli sbagli" con sottomenu 3 giochi, fixati bug critici (indice non avanzante, listener duplicati), aggiornati 3 file (index.html, app.js, style.css) e scritto RAPPORTO.md. · 2 domande per te
- 2026-10-05 12:53 · T21-risposta1: Modificato 1 file (web/app.js) per cambiare l'avvio del ripasso da sottomenu a sessione mista.
- 2026-10-05 12:50 · T20-risposta1: Aggiornato il bottone Ripasso per aprire un sottomenu con scelta tra i tre giochi di ripasso.
- 2026-10-05 12:45 · T21-critico-a: Critica di T20 scritta in agenti/T21-critico-a/CRITICA.md: 13 errori elencati per funzione e riga del diff, voto 1/5 (ripasso inoperante e 3 giochi bloccati al primo errore). · 1 domande per te
- 2026-10-05 12:23 · T20-esegui-b: Implementato "Ripasso degli sbagli" con tracciamento debiti per 3 giochi, nuova scheda in home, sessione di ripasso che rimuove item a risposta corretta; 4 file modificati (app.js, index.html, style.css, report). · 2 domande per te
- 2026-10-05 03:34 · T21-critico-b: L'implementazione presenta errori critici che impediscono il funzionamento del sistema di ripasso, con un voto di 2/5 dovuto a variabili non definite e deviazioni dalle specifiche.
- 2026-10-05 03:33 · T21-critico-a: non ha passato i controlli
- 2026-10-05 03:32 · T20-esegui-b: non ha passato i controlli
- 2026-10-05 03:29 · T18-risposta2: Ho portato a 5 l'obiettivo giornaliero nell'idea 6 di IDEE.md (prima era 10), cambiando 1 riga.

### Decisioni di Leo (risposte alle domande)
- quale idea di IDEE.md partiamo a implementare? -> **tutte e tre, ognuna in task separate. procedi a creare anche delle task per i problemi che vedi nel codice attuale. sempre come task indipendenti e separate.**
- che obiettivo giornaliero di default? -> **5**
- La scheda Ripasso mostra il totale debiti ma parte solo per articoli: va bene così? -> **Sì**
- Il bottone "Ripasso" in home deve avviare il ripasso per un gioco specifico (qual'è?) o aprire un sottomenu per scegliere? -> **B: sottomenu 3 giochi**
- Il ripasso: scheda unica mista o tre schede per gioco? -> **l'opzione piu semplice al momento, poi in un secondo  momento potremmo ampliarla**

### Domande aperte: 0 (0 a risposta chiusa)
<!-- STATO DELL'UFFICIO: fine -->
