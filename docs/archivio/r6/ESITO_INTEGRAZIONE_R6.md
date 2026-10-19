# Esito: integrazione Risultato 6 v2 in mappa e in `simulazione.html`

Piano: `docs/PIANO_INTEGRAZIONE_R6.md`. Eseguito il 19/10/2026 su ramo `prova`, senza commit.

FASE 1: OK
FASE 2: OK
FASE 3: OK (con una deviazione sulla distanza, vedi sotto)
FASE 4: OK (con deviazioni dichiarate sotto)
FASE 5: OK

## Controlli numerici

- Coperti a 200 m (browser, insieme e raggio cambiati dai menu): F 140, U 11, FS 144. Controllo del piano: **tornano**.
- Coperti F: 100 m 69, 400 m 228. Il riepilogo del file dice 229 a 400 m, ma il conteggio sui `dist_m` dei singoli luoghi dà 228. Differenza di un luogo nell'origine dei dati (script 79 o 75): **non corretta qui**, da controllare.
- Scoperti F a 200 m: 378 - 140 = 238, nella scheda e nella legenda.
- Parcheggi di fatto: 0. Potenziali 758 (56.566 posti). Solo sulla carta 4 (1.716 posti).
- Eventi: Olimpico auto 5.635, posti entro 1 km 2.389, mancano 3.246; coerenti con la formula del file.
- `node --check` su `mappa_torino.html` (script inline), `simulazione.html` e `data/schede_risultati.js`: OK.

## Fase 1 (colori in mappa)

- Costanti `PAL_VR`, `PAL_RV`, `PAL_NEU` definite **prima di `OMI_PAL`** (non nel punto ~609): altrimenti `OMI_PAL = PAL_NEU` darebbe errore di inizializzazione. Stessi valori del piano.
- Sostituzioni e lista completa: `docs/RAPPORTO_COLORI.txt`.
- Altri cambi di colore non previsti dal piano, tutti per coerenza: colore della legenda «Sensori 5T» (era viola, ora gradiente rosso-verde); flussi pendolari entrata/uscita (ora blu/arancio, erano viola/arancio-scuro); testo «Arancio = poca offerta» → «Rosso = poca offerta, verde = molta».
- Guida: aggiunto il paragrafo sui colori.

## Fase 2 (dati R6 in mappa)

- `04_genera_mappa.py`: caricamento di `mappa_r6.json` e chiave `r6` nel dizionario. Stampa: 378 luoghi, 813 parcheggi, 3 eventi.
- `R6` proiettato nel template; nessun altro tema cambiato.

## Fase 3 (tema «Parcheggi di interscambio»)

- Tema, tre opzioni (cosa vedere, quali parcheggi, distanza), disegno, tocco (eventi, parcheggi, luoghi), legenda, guida, link `#tema=interscambio`.
- **Deviazione 1, distanza.** La copertura confronta la distanza **arrotondata al metro** (`Math.round(d) <= raggio`). Senza, il caso «MASSAUA OVEST» a 200,006 m non risultava coperto e U restava a 10, mentre il file dice 11. Il file stesso lo conta come coperto (`dist_m` = 200).
- **Deviazione 2, legenda.** I conteggi per classe nella legenda sono quelli dei **parcheggi sulla mappa** (813: 758 potenziali, 4 solo sulla carta, 0 di fatto, 51 non interscambio), non quelli di `riepilogo.parcheggi_per_classe` (3.431 considerati, con 2.669 non interscambio). Così la legenda non dice una cosa e la mappa ne mostra un'altra. Nella scheda il riepilogo resta, con la nota che si tratta di tutti i parcheggi considerati.
- **Deviazione 3, universo.** La legenda scrive «su 4.425» leggendo `scenario.universo` (il file del piano non lo conteneva nel campo indicato, ma è nel file: `scenario.universo = 4425`).
- Il cerchio di copertura del parcheggio scelto è disegnato in `disegnaR6Sopra` (non nella cache di base), così il clic non richiede di ricalcolare lo sfondo.
- Nel tema, il menu «Quali parcheggi contano» con «Solo i 5 interscambi ufficiali» conta 11 a 200 m (verificato nel browser).
- Testi in italiano semplice; `[STIMATO]`, `[PROGRAMMATO]`, `[DATI SCARSI]` visibili nelle schede e nelle legende.

## Fase 4 (`simulazione.html`)

- Colori: variabili `--vr-*` e `--neu-*` in `:root`; `graficoBarre`, `graficoPila`, `TONI`, `PALETTE_PILA` aggiornati. Barra «prima» in blu chiaro anche quando la barra è rossa (piccola stonatura visiva, da decidere).
- Nuovo grafico `profilo` (curva 24 ore, `null` interrompe la linea), classe `largo`.
- **Deviazione 4, palette del profilo.** `PALETTE_LINEE` ha cinque colori (blu, arancio, grigio, viola, ocra): niente rosso e verde, perché sono giudizi e qui le serie sono categorie. Il piano diceva quattro colori con il rosso.
- **Deviazione 5, immagini.** Niente `loading="lazy"`: con il lazy l'errore «file mancante» arrivava solo allo scorrimento, e la sezione compariva vuota. Senza lazy, la sezione «Com'è fatta in mappa» sparisce appena si apre la scheda, se i file non ci sono (verificato: 0 immagini, sezione assente).
- Link «Apri la mappa» con `#tema=<id>` quando la scheda ha `mappa.id`.

## Fase 5 (scheda R6 v2)

- `scheda_r6_v2()` aggiunta; `scheda_r6` (v1) **non cancellata**; `main()` usa la v2 e scrive `risultato6_riepilogo_mappa.json`.
- Numeri della scheda letti solo da `mappa_r6.json` (somme e conteggi). Il 4.425 e la soglia 63,97 nel testo di metodo vengono da `docs/ESITO_RISULTATO6_V2_GIRO2.md` (verificati).
- Otto grafici (come da piano). Il grafico «Eventi» unisce tre misure in un solo elenco (auto, posti a 1 km, posti mancanti).
- Immagini: `immagini/r6_torino.png`, `immagini/r6_zoom.png`, `immagini/r6_evento.png` (le fa Leo; finché mancano la sezione non appare).

### Toni assegnati (da rivedere, come chiede il piano)

- R1, grafico «Residenti ... senza il servizio entro 15 minuti»: tutte le voci rosso (per il titolo con «senza»).
- R1, grafico «Residenti senza il servizio: oggi e con i punti nuovi»: rosso.
- R4, «Come arrivano i mezzi»: puntuali verde, in ritardo rosso; anticipo senza tono.
- R4, «Passaggi in ritardo oltre 5 minuti» (per fascia e per tipo di giorno) e «Le 10 linee più in ritardo»: rosso.
- R6 v2, pila coperti verde, scoperti rosso.
- R8, pila «Km di strade»: «con fermate frequenti vicine» verde, «con poco trasporto pubblico» rosso.
- Non assegnati, da decidere: R4 «Le 10 linee più irregolari»; R9 «Minuti in più di attesa»; R8 tratte e sensori.

## Verifica nel browser (fatta da Claude sul server locale `pagine-gtt`)

- `mappa_torino.html#tema=interscambio`: il tema si apre, legenda corretta, nessun errore in console, clic su parcheggio e su luogo critico apre la scheda giusta (con la copertura calcolata).
- `simulazione.html`: sei schede; la R6 ha 8 grafici, la curva 24 ore (5 linee: 4 interscambi + Porta Susa), link «Apri la mappa» a `#tema=interscambio`.
- Non verificato: schermo stretto (solo per dimensione CSS), R1/R4/R8 nel dettaglio dei colori.

## File modificati

- `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`, `simulazione.html`
- Generati: `mappa_torino.html` (23,9 MB, prima 23,4 MB), `data/schede_risultati.js`, `data/processed/risultato*_riepilogo_mappa.json`
- Nuovi: `docs/ESITO_INTEGRAZIONE_R6.md`, `docs/RAPPORTO_COLORI.txt`
- Copia di sicurezza `mappa_torino_prima_R6.html`: creata prima della rigenerazione e tolta a fine lavoro (come da piano, Fase 6)

## Limiti aperti

- Immagini per la scheda: da fare (Leo).
- Allianz Stadium: fuori (non trovato in OpenStreetMap con quel nome).
- Riempimento: solo 2 giorni feriali; ricalcolare dopo il fetch di domenica 25/10 (piano, Fase 6).
- Differenza di un luogo a 400 m tra riepilogo (229) e dati dei singoli luoghi (228): da controllare nello script 75/79.
