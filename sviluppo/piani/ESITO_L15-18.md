# Esito L15-L18 (24/10/2026, sessione cloud `claude/epic-clarke-6zdofk`)

Giri fatti in fila, come nel piano («Discussione di design», `PIANO_GRAFICA.md`). Partenza da `origin/prova` dopo L12 (2112dc6).
Prove: `python scripts/prova_pagine.py --playwright` (tutto, 0 errori) e, più veloce, `--solo-design` (solo `prova_design`: L15, L16, L17, L18).
Niente controlli grafici miei per Leo (li fa lui), niente telefono. Nessun numero dei risultati è cambiato: il numero grande di ogni scheda è uguale a prima
(99,2% · 6,41% · 179 · 1,9 volte · 79.598), la prova lo confronta con i dati.

## L15 — schede con meno rumore
Parti comuni (`scripts/schede/comune.py`, `risultati.html`):
- `circa()`, `circa_mila()`, `minuti_a_parole()`, `intero()`: il «~» sui numeri secondari (percentuali, minuti, rapporti interi; conteggi grandi «~222 mila»; il mezzo minuto a parole).
  Il numero grande, i conteggi piccoli e il testo del calcolo restano precisi.
- Via la pastiglia STIMATO/MISURATO… sotto il titolo e la riga «Limite: …» sotto il numero grande. Il tipo di dato è una riga a parole nella parte chiusa
  (`TIPO_DATO`, campo `tipo_dato`), che ora si chiama «Come è stato calcolato, e limiti» / «How it was calculated, and limits».
- Barre e quadratini a 100%: valori interi senza «~» (le barre con testo scritto usano `intero()`).
- Fasce: mattino (7-9), giorno (9-16), sera (16-19), **tarda sera (19-24)**; niente «punta» (la definizione «fuori punta» diventa «escluse le fasce 7-9 e 16-19»).
- `controlla_forma`: punti chiave oltre 25 parole segnalati, calcolo fino a 8 righe.

Schede, cosa si vede ora (prima → dopo):
1. Cerchi e punti con «~» e senza virgole («~68% · ~97% · ~99%»); «~222 mila residenti (~26%)»; la frase sulla stima del traffico (±28%) è passata nel calcolo.
2. «noi misuriamo» → impersonale; «Noi e GTT» → «GPS e dato ufficiale GTT» (barre intere: 2, 6, 5, 6, 6); fasce rinominate; il grafico dell'attesa diventa
   «Quanto si aspetta in più di quanto dice l'orario» (una barra per fascia, a destra «~6 min invece di ~5»); punto chiave «~1 minuto e mezzo in più».
3. Via «(stima)» dal titolo; punti: «68 … nessun parcheggio vicino, 111 troppo pochi» · «il primo dei 12 punti … ne mancano ~450» · «In 8 punti su 12, lasciata l'auto,
   il bus arriva in centro in al più 1,5 volte il tempo dell'auto»; tolto il grafico dei minuti di pareggio (ora una frase del calcolo: 16 minuti, 28 con la stima
   dei sensori); la storia dei parcheggi di scambio senza «pieno/a metà/non misurato» mescolati ai minuti («39 contro 30 in auto · pieno di giorno», «riempimento non noto»).
4. Domanda «Al mattino, quanto ci si mette in più coi mezzi pubblici che in auto?»; numero grande con una frase («il tempo dell'auto, per un viaggio tipico del mattino»);
   barre per fascia con la sola stima TomTom; linea ora per ora con una serie sola; «Le 12 coppie…» → «I tragitti dove coi mezzi pubblici si impiega più del doppio dell'auto»;
   47%, coppie escluse, verifica Google, 600 coppie e sensori 5T (rapporto 2,9; 97%) sono nel calcolo.
5. Solo «~129 mila persone» al posto di «129.285» (la scheda andava bene).

Traduzioni inglesi: `scripts/schede/testi.json` (tutte le frasi nuove; lo script non avvisa di frasi senza traduzione); `traduci.py` accetta il «~» nei valori.

## L16 — gara e area da sole
- `assets/gara.js`: nuovo modo «giro» (schede 3 e 4): nessun comando, le corse una dopo l'altra (scheda 3: i 12 punti poi i 5 interscambi; scheda 4: i 6 viaggi più frequenti),
  nome del luogo sopra e arrivo a destra (nome lungo: «…» e nome intero nel `title`), una sola auto (TomTom, parcheggio compreso), alle 8; all'arrivo i minuti, il distacco («+9 min»)
  e una frase di esito. Corsie più alte e larghe (disegno non schiacciato). Con «riduci movimento» tutte le corse ferme, una sotto l'altra. Il vecchio modo (con «Riparti»)
  resta solo per la gara piccola del pannello della mappa. Via select, ore e modo con più auto dal giro delle schede; `r6.py` e `r8.py` non scrivono più `ore`.
- `assets/area.js` riscritto: da Piazza Castello, auto TomTom, senza tendine, senza «Parti/Ferma», senza cursore e senza tabella. Da sola da 0 a 45 minuti in 13,5 s
  (prima 9 s fino a 60), pausa 3 s, ricomincia; «N minuti» scritto grande, le quote ~% accanto alle aree; ferma a 30 minuti con «riduci movimento».
  I dati delle altre zone restano in `data/area_tempi.js` (non usati). Nota sotto l'area: ~42% coi mezzi e ~90% in auto a 30 minuti (dati).

## L17 — home da scorrere
- `assets/progetto.js` (nuovo) + `assets/progetto.css` (nuovo): le sei tappe di `progetto.html`, con lo stesso codice e gli stessi testi: la prova ha confrontato il testo visibile
  di `progetto.html` in italiano e in inglese prima e dopo (identico). `Sito.traduci(radice)` traduce i pezzi scritti dal codice.
- Campi nuovi nelle schede: `chiave` (schede 4, 2, 5: «1,9 volte», «~6%», «~1 torinese su 10») e `numero.breve` (testo corto per i riquadri della home, al massimo 8 parole).
- `index.html`: parte 1 «In breve» (due frasi, tre numeri chiave con link alle schede, bottone «Apri la mappa»); parte 2 «I risultati in breve» (riquadri con anteprima animata,
  titolo, numero grande e testo breve; clic → `risultati.html#pN`); parte 3 «Il progetto» in fascia scura con bordo oro (`#progetto`, il link della barra porta lì).
  Sostituiti la lista «intro» e i due bottoni. `risultati.html` e `progetto.html` restano (si decide dopo se tenerle).
- Peso della home (index.html + script e stili propri): 0,58 MB (limite 1 MB).

## L18 — toro nel caricamento della mappa
- Variante B (le linee d'oro si disegnano in 1,5 s, poi l'oro riempie in 0,5 s) al posto del contorno di Torino; testo «Caricamento della mappa…»; resta almeno 2 secondi
  dall'apertura (`performance.now()`), con «riduci movimento» toro fermo e intero e nessuna attesa in più; coordinate intere (28 tracciati).
- Blocco sostituito in `scripts/mappa_template.html` e, con lo stesso testo, in `mappa_torino.html` (`04_genera_mappa.py` non gira nel cloud): i tre pezzi (stile, svg, chiusura)
  sono identici nei due file. Peso di `mappa_torino.html`: 5.904.056 → 5.958.364 byte (limite 5.906.557 + 54.637 del toro = 5.961.194).

## Prove
- `pyflakes scripts`: nessuna segnalazione; `node --check assets/*.js`: ok; `schede_risultati.py`: nessuna ATTENZIONE; `86_controlla_file_pagine.py --ci`: ok.
- `prova_pagine.py --playwright`: 0 errori su tutte le pagine; `prova_design` con quattro parti (L15 parole vietate IT/EN, punti chiave ≤ 25 parole, numero grande uguale ai dati;
  L16 nessun comando, testi nel disegno, corsie che non si toccano, nome che cambia, minuti dell'area che cambiano entro 3 s, riduci movimento; L17 numeri chiave, riquadri, 6 tappe,
  nessuna animazione, peso; L18 toro, almeno 2 s, riduci movimento, peso).
- Anteprime `assets/anteprime/r*.jpg` e immagini `assets/readme/*.jpg`: la prova le riscrive; le immagini del README sono state ripristinate (`git checkout -- assets/readme/`),
  le anteprime tenute solo dove il titolo è cambiato (scheda 3).

## Cosa resta aperto
- Sul PC: `RIFAI_MAPPA_E_SCHEDE.bat` (la mappa rigenerata dal template ha già il nuovo caricamento); `data/progetto.js` si riscrive solo dove c'è `omi_zone.json`.
- La gerarchia dei riquadri della home (ora tutti alla pari); tenere o togliere `risultati.html` e `progetto.html`; il nome della fascia 19-24 («tarda sera»);
  la domanda della scheda 5 (rimasta com'era); le immagini del README da rifare con la nuova home.
- La gara nel pannello della mappa usa ancora due auto (TomTom e sensori): fuori dallo scopo di questi giri.
