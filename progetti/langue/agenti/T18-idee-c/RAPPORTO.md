origine: agente T18-idee-c · stato: bozza

# Rapporto – T18-idee-c

## Cosa ho fatto
- Letti: PROGETTO.md, SCHEMA.md, web/index.html, web/app.js, web/style.css (nessuna esecuzione: non posso far partire il sito).
- Creato `agenti/T18-idee-c/IDEE.md`: 7 problemi/punti fragili del codice citati per nome di funzione, 8 idee classificate (problema / proposta / effetto / difficolta' / file toccati) e la preferita con motivazione.
- Creato `agenti/T18-idee-c/DOMANDE.md` con 2 domande a risposta chiusa (idea da implementare per prima; default dell'obiettivo giornaliero).

## Cosa ho verificato (solo su codice)
- `controllaOrdine` confronta la frase del giocatore con `testo_de` + `alternative` dopo `normalizzaFrase` (case e spazi gestiti).
- `disponibili()` + `aggiornaHome()` disabilitano le schede a pool vuoto: copre il crash latente di `prossima()` (IDEE.md, problema 1), ma non la coerenza `blocchi`/`testo_de` (problema 2).
- `sistemaProgresso`/`interoSicuro` sanificano i dati letti da localStorage; il livello radio è validato contro `LIVELLI`; `avviso-dati` copre `data.js` assente o malformato ma con messaggio impreciso.
- Nessun nuovo contenuto tedesco creato, come richiesto dal task.

## Scelte (default piccoli e reversibili)
- Le nuove idee che salvano dati usano **chiavi localStorage separate** (`langue_debiti_v1`, `langue_obiettivo_v1`, `langue_rubrica_v1`): non modifico `langue_progress_v1`; si disattivano rimuovendo la chiave.
- Ranking delle idee per effetto sull'apprendimento / rischio di implementazione, non per sola difficolta'.
- Nelle "Scelte" di DOMANDE.md ho indicato i miei default (idea 1; 10 risposte/giorno) per poter lavorare senza fermarmi.

## Da decidere/rivedere da Leo
- Vedi DOMANDE.md (2 domande chiuse).
- Idea 8 (PWA): da_verificare il modo di hosting (serve http(s), non `file://`).
- Nessun suggerimento di modifica a PROGETTO.md o ai file del progetto: ho scritto solo dentro `agenti/T18-idee-c/`.
