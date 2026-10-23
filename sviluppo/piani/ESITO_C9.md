# Esito C9 — mappa (22/10/2026, cloud)

## Fatto (in `scripts/mappa_template.html`; `mappa_torino.html` rifatta con il template e gli stessi dati, 6,10 MB invece di 6,09)
- **F. Ore che scorrono**: bottone ▶ / ❚❚ accanto al cursore dell'ora (nei temi che cambiano con l'ora). Scorre dalle 6 alle 23 (cioè fino alle 24), un'ora al secondo; la legenda si aggiorna a ogni ora.
  Il «passaggio morbido» è una dissolvenza: prima del cambio si copia l'immagine di prima sopra la mappa e la si fa svanire in 0,85 secondi sull'ora nuova (vale per ogni tema, senza ridisegnare a metà).
  Si ferma se si tocca il cursore, il giorno, la mappa o si cambia tema; con «riduci movimento» niente dissolvenza.
- **L. Caricamento**: schermo scuro con il contorno di Torino che si disegna, «Carico la mappa…» e una barra che sale (anima con CSS e va al 100% quando la mappa è pronta), poi dissolvenza. Se la pagina ha un errore, il caricamento sparisce e si vede l'avviso rosso.
- **M. Telefono** (sotto 640 px): il pannello è un foglio che sale dal basso; chiuso mostra solo la maniglia e il tema scelto; si apre con la maniglia, si richiude toccando la mappa o aprendo una scheda. Le schede si aprono in alto. Prima il pannello spariva dietro un bottone «Temi».
- **M. Schede uniformi** (scelta mia, vale per tutti i temi perché sta nella funzione comune `creaScheda`): titolo = nome del posto, un riquadro col numero principale, **al massimo 5 righe di dettaglio** (le altre in «Altri dati (n)»), approfondimento richiudibile,
  **fonte e avvertenze in piccolo in fondo** (prima erano un riquadro arancione in alto).
- **M. «Copia il link di questa vista»**: nell'indirizzo finiscono tema, scelte delle tendine del tema (`o_<tendina>=valore`), giorno e ora (`dt`, `ora`), linea filtrata, zoom e centro (`z`, `c=lat,lon`). Aprendolo la mappa torna lì (provato: nuova pagina con il link copiato, stessi tema, scelta, ora e zoom).
  I vecchi indirizzi (`#tema=…&vista=…`, `&ora=8`) funzionano come prima.
- Dentro la mappa c'è anche la **gara piccola** di C7.

## Prove
- Pagina costruita con il template e i dati veri della mappa: tutti i 17 temi aperti su computer e telefono senza errori; ▶ (08:00 dopo 1 secondo, ferma a comando), copia link e riapertura, foglio su telefono (chiuso, aperto, richiuso, scheda in alto), scheda R6 con gara e «Altri dati».
- `python scripts/prova_pagine.py`: vedi la riga finale in fondo a questo file.
- Peso: `mappa_torino.html` 6,10 MB (+11 KB: caricamento, ▶, foglio, link). Il limite «6 MB di oggi» è rispettato come ordine di grandezza, non al byte: ditemi se vuoi che lo riduca.

## Da guardare sul PC (P5)
Velocità del ▶ e leggibilità della dissolvenza; foglio sul telefono (vista «telefono» del browser); testo del caricamento (la mappa carica in meno di un secondo qui, la barra si vedrà solo su computer lenti).
