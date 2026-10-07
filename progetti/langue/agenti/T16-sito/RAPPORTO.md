# Rapporto T16-sito

## Cosa ho fatto
Ho scritto il sito statico in `web/` (tre soli file: `index.html`, `style.css`, `app.js`). Usa `web/data.js` (non modificato) e non ha librerie né rete.

- **Home**: filtro livello (A1 / A2 / Tutti), tre schede-gioco con numero di contenuti disponibili e statistiche, riepilogo dei progressi, pulsante "Azzera i progressi" (con conferma).
- **Der, die o das?**: parola a caso, tre pulsanti der/die/das, feedback subito (✓/✗ e colore) con la traduzione italiana, contatore della serie e record.
- **Rimetti in ordine**: blocchi mescolati (mai nell'ordine giusto, se possibile); si tocca un blocco per metterlo nella frase, si tocca di nuovo per toglierlo. "Controlla" accetta `testo_de` o una delle `alternative`; `traduzione_it` è il suggerimento. Ci sono anche "Ricomincia" e "Mostra la soluzione".
- **Trova l'errore**: le due frasi in ordine casuale, poi si vede la frase corretta e `spiegazione_it`.
- Si usano solo i record con `stato` diverso da `da_verificare`.
- **Progressi**: solo in `localStorage`, chiave `langue_progress_v1`, sempre in try/catch. Se il browser lo blocca, il sito funziona e compare un avviso. Nella stessa chiave salvo anche il livello scelto.
- **Sicurezza**: nessun `innerHTML`, nessun `eval`; i testi dei dati entrano solo con `textContent`.
- **Testabilità**: le funzioni pure sono all'inizio di `app.js` (`mescola`, `scegliCasuale`, `controllaOrdine`, `ordineMescolato`, `filtraPerLivello`, progressi…) e sono esportate con `module.exports` se si usa Node (nel browser quella riga non fa nulla).
- **Accessibilità**: pulsanti di almeno 48 px, focus ben visibile, link "Vai al contenuto", area messaggi `aria-live`, il filtro livello usa radio nativi, tema chiaro/scuro automatico.

## Come aprirlo
Doppio clic su `web/index.html` (il file `web/data.js` deve restare accanto). Non serve un server.

## Cosa NON ho fatto / NON è testato
- **Non posso eseguire codice: niente è stato provato**, né nel browser né con Node. Ho solo riletto il codice. Il controllo del validatore del runner, se c'è, riguarda al massimo la forma dei file; il funzionamento va provato da Leo (almeno un giro per gioco, su telefono e su PC).
- Non ho provato il caso "localStorage bloccato" (è gestito nel codice, ma non verificato).
- Nessun test automatico scritto (non era tra i file consentiti).
- Aspetto grafico non visto: colori e spaziature vanno guardati.
- Nessun suono, nessuna ripetizione intelligente (le domande sono casuali, evitando solo di ripetere subito la stessa).

## Scelte
- **Confronto delle frasi ignorando TUTTE le maiuscole/minuscole**, non solo la prima lettera. Motivo: in `data.js` i blocchi hanno forma fissa (es. blocco `Ich`), mentre le `alternative` hanno "ich" a metà frase (es. «Heute lerne ich…»): con la sola prima lettera una risposta giusta verrebbe rifiutata. Il giocatore non può cambiare le maiuscole dei blocchi, quindi non c'è rischio di accettare ordini sbagliati.
- Un blocco come `Ich` resta scritto con la maiuscola anche a metà frase (è come sta nei dati).
- La serie (giuste di fila) vale per la sessione di gioco corrente e si azzera quando si esce; il record è salvato per gioco. In "Rimetti in ordine" conta solo il primo tentativo di ogni frase (se sbagli, poi correggi, resta un errore); anche "Mostra la soluzione" conta come errore.
- Le traduzioni degli articoli sono mostrate come nei dati (es. «Cane» con la maiuscola): se vuoi minuscole, va corretto nei dati, non nel sito.
- Il filtro livello "Tutti" include anche eventuali record B1/altro; A1 e A2 mostrano solo il proprio livello.
- Ho evitato una Content-Security-Policy nel file HTML: da `file://` può comportarsi in modo diverso nei vari browser e rischiava di bloccare il sito.
- Il nome "Langue" è provvisorio, come nel profilo del progetto; il piè di pagina avverte che i contenuti sono in bozza.

## Da guardare per Leo
- Se il filtro A2 dà abbastanza contenuti in tutti e tre i giochi (la scheda dice "Nessun contenuto per questo livello" e si disattiva se un gioco è vuoto).
- Provare "Rimetti in ordine" con una frase con `alternative` e controllare che un ordine alternativo venga accettato.
