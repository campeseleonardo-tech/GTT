# Esito C11 — la pagina «Il progetto» (23/10/2026, cloud)

## Fatto
- **`progetto.html`** (prima era un segnaposto): pagina a scorrimento, testo a sinistra e un disegno fisso a destra che cambia a ogni parte (su telefono il disegno sta in alto, fisso, sopra il testo). Stile comune, barra, IT/EN (come le altre pagine; link nella barra e in fondo a `risultati.html`, «Perché questo progetto»).
  Sei parti: **1 la promessa** (tesi 2020; punti vuoti → punti accesi) · **2 il sistema** (schema animato: sensori e GPS → Raspberry Pi → storico → script → pagine, con i giorni di raccolta e il numero di sensori) ·
  **3 chi abita dove** (mappa di Torino con le 5 zone in doppio svantaggio che si accendono, nomi scritti sopra) · **4 muoversi** (barre: l'auto = 1, i mezzi da 2 a 3 volte; rimandi alle schede 3 e 4) ·
  **5 quanto ci si può fidare** (barre: feed dei ritardi contro GPS) · **6 cosa manca e chi sono** (i livelli dell'IoT della tesi, l'ultimo tratteggiato: «business, manca»).
- **Nessun numero scritto a mano**: li legge dalle schede (`data/schede_risultati.js`: 2–3 volte, 21–28 minuti) e da **`data/progetto.js`** (nuovo, 14 KB, scritto da `scripts/schede/progetto.py` dentro `schede_risultati.py`): giorni e passaggi della raccolta (come il contatore della home), numero dei sensori, residenti e zone in doppio svantaggio (script 95) con i loro poligoni (zone OMI semplificate nel disegno del contorno di Torino), ritardi oltre 5 minuti col GPS e col feed (script 27).
  Quello che resta **scritto nel testo** (fatti storici, da rileggere): la tesi del 2020, «un mezzo con l'orologio tre anni avanti», «un feed fermo la mattina del 18 ottobre», «un contatore di parcheggio che non cambia mai».
- «Riduci movimento»: niente animazioni (punti accesi, barre già piene, nessun puntino che scorre), il disegno cambia comunque con lo scorrimento. Senza JavaScript i disegni restano in colonna sotto il testo. Peso: pagina 24 KB + `progetto.js` 14 KB + schede (già caricate dalle altre pagine): ben sotto 1,5 MB.
- `prova_pagine.py` e script 86 conoscono `progetto.html` (86 conosce anche `data/area_tempi.js`, caricato da `assets/area.js`: manca finché non gira il 99, avviso atteso).
- `prova_pagine.py` ora trova anche il Chromium nella cartella `chrome-linux64` (cloud).

## Prove (cloud)
Pagina aperta in Chromium a 1440 px, 390 px (telefono) e 1100 px con «riduci movimento» in inglese: 0 errori JavaScript; ogni parte fa comparire il suo disegno (uno solo attivo alla volta); numeri nei testi uguali a quelli dei file; mappa con 5 zone e nomi leggibili (le etichette che si sovrappongono si spostano).

## Testi da far rileggere a Leo
Sono in `progetto.html` (italiano nel corpo, inglese in `data-en`). Punti da guardare: «Per me è il risultato più forte, e non riguarda la tecnologia: come diceva la tesi, i problemi urbani sono sociali» (frase mia, dalla critica alla smart city nella tesi); la parte 5 («trabocchetti»); la parte 6 («Mancano: quante persone salgono davvero, quanto costa il servizio, i treni e le altre aziende»). Dubbio mio: il titolo della parte 4 dice «2–3 volte il tempo dell'auto», che è la forbice fra due fattori di punta (vedi scheda 4), non un singolo numero.

## Da fare sul PC
`scripts\RIFAI_MAPPA_E_SCHEDE.bat` (scrive anche `data/progetto.js`), poi aprire `progetto.html` e scorrere le sei parti (anche con la vista «telefono» del browser).
