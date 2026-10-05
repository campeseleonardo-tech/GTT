# RAPPORTO – T23-prova-guidata

## Cosa ho fatto
- Letti: PROGETTO.md, web/index.html, web/app.js, web/style.css. Il file `web/data.js` NON mi è stato fornito: i contenuti concreti (parole/frasi/errori e quanti per livello) non posso verificarli; dove contava, nella prova l'ho segnato "da verificare".
- Creato `docs/PROVA_SITO.md`: prova guidata di circa 10 minuti in 11 passi per Chrome da fila a `web/index.html`: apertura/home, selettore livello, i 3 giochi con risposte sbagliate deliberate, ripasso (sottomenu + "sbagliato → torna in fila → scompare al giusto" + ritorno in home a lista vuota), reload F5 con numeri intatti, azzera, obiettivo giornaliero (marcato da verificare) e istruzioni F12/Console per copiare gli errori rossi. Ogni passo ha "cosa cliccare", "cosa dovresti vedere" e le caselle `[ ] ok` / `[ ] non va` + spazio Nota.
- Creato `DOMANDE.md` con 2 domande chiuse per Leo.
- Non ho toccato altri file (niente web/, niente PROGETTO.md).

## Cosa ho controllato (ragionando sul codice, senza eseguirlo)
- Sottomenu Ripasso: presente, un riquadro per gioco, bottone "Chiudi", giochi senza errori disattivati — coerente con la tua decisione (sottomenu 3 giochi).
- Ciclo "sbagliato → giusto → scompare": risposta giusta in ripasso toglie l'errore dai debiti e la barra "Rimasti" scende; risposta sbagliata lo tiene in coda (torna a essere chiesto); a lista vuota si torna in home.
- Persistenza: progressi in localStorage `langue_progress_v1`, debiti in `langue_debiti_v1`; il F5 dovrebbe lasciare i numeri invariati. I salvataggi sono protetti da try/catch ed esiste un avviso se il browser blocca il salvataggio.
- "Azzera i progressi" (nel codice attuale) azzera solo giusti/sbagliati/serie: i debiti di ripasso NON vengono cancellati.
- Obiettivo giornaliero: non lo vedo né in app.js né in index.html (nessun contatore "Oggi: X/5"); il "5" della tua risposta è in IDEE/decisioni, non implementato in web/.

## Scelte (piccole e reversibili)
- Passo "obiettivo giornaliero" impostato come "assente = come atteso" secondo il codice letto, così la prova non si blocca (domanda aperta in DOMANDE.md).
- Nel ripasso suggerisco di iniziare dal gioco con meno errori e preferire Errori/Articoli (più click in meno).
- Nel passo F12 ho inserito la riga opzionale `localStorage.clear()` per una ripartenza da zero totale (il pulsante "Azzera" non tocca i debiti).
- Ho messo il conteggio N del ripasso come "errori diversi" (stesso errore ripetuto non aggiunge contatore nel codice).

## Da te
- Rispondi le 2 domande in DOMANDE.md (obiettivo giornaliero; azzera + debiti).
- Suggerimento per PROGETTO.md (non l'ho modificato): nelle tue note o nello Stato segnare che "obiettivo giornaliero (idea 6)" non è ancora nel sito, così il prossimo task parte chiaro.
- Nessun blocco: non ho creato DECISIONS.md.
