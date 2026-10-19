# Esito R6 correzioni (piano `PIANO_R6_CORREZIONI.md`)

Eseguito il 19/10/2026 sul ramo `prova`. Nessun commit. `MEMORIA_PROGETTO.md` e `data/ref/*` non toccati.

## Esito per fase

- **FASE 1: OK.** Scritto `scripts/prova_pagine_r6.py`: apre le pagine con Edge headless (lanciato con PowerShell, perché da Python il browser esce subito senza output), legge il log, controlla il pannello `#jsoff` e il titolo della legenda, fa gli screenshot, conta le etichette e cerca gli identificatori `r6…` non definiti. **Il test ha trovato l'errore**: `ReferenceError: r6Data is not defined` su tutte e tre le viste. Per aprire direttamente una vista ho esteso `temaDaUrl` con `&vista=parcheggi|aree|mancano` (valore non valido → `parcheggi`), anche con `hashchange`.
- **FASE 2: OK.** `r6Data` definita accanto agli altri helper (da `2026-10-15` a `15/10`). Controllo statico: non resta nessun altro identificatore `r6…`/`R6…` non definito. Legenda robusta: se la legenda di un tema fallisce, mostra «Legenda non disponibile» e scrive l'errore in `console.error`. Test dopo la correzione: zero errori su 5 pagine.
- **FASE 3: OK.** Ogni nome compare una sola volta come etichetta: lo script 80 assegna `mostra_etichetta` a una sola area per nome (quella con più fermate; a parità la più a nord); le aree indicative non hanno etichetta. Il disegno a zoom < 13 usa solo queste.
- **FASE 4: OK.** Descrizioni in parole calcolate dal profilo (N = notte 2-5, G = giorno 10-16, W = weekend 10-16). Le regole del piano, in ordine, sono in `descrivi_profilo` in `80_porte_interscambio.py`. Le descrizioni arrivano a titoli dei grafici, comportamenti medi, dati della mappa e clic del parcheggio.
- **FASE 5: OK.** Nome pubblico «Parcheggi per lasciare l'auto» ovunque (il vecchio nome non compare più). Spiegati «nodo di trasporto importante», «IMQ 2022 sugli spostamenti» e «5T» alla prima citazione. Aggiunta in scheda la riga «Come leggere i tag». Legenda della vista «mancano» con i numeri letti dai dati (20 punti, 206 fermate su 378).
- **FASE 6: OK.** Rigenerati 80 → 79 → 04 → schede. `node --check` su `data/schede_risultati.js`, sugli script di `mappa_torino.html` e di `simulazione.html`: tutti OK. Prova finale: **zero errori**. Screenshot creati (vedi sotto).

## Errori a runtime: prima e dopo

| Pagina | Prima della correzione | Dopo |
|---|---|---|
| mappa, vista parcheggi | `ReferenceError: r6Data is not defined`; pannello `#jsoff` visibile | 0 |
| mappa, vista aree | stesso errore; pannello visibile | 0 |
| mappa, vista mancano | stesso errore; pannello visibile | 0 |
| mappa, tema servizio | 0 | 0 |
| scheda `simulazione.html` | 0 | 0 |

Identificatori `r6…`/`R6…` non definiti: prima **1** (`r6Data`), dopo **0**. (Il controllo statico ha anche segnalato due falsi positivi, `r6Vista` e `r6vista`, che erano chiavi di oggetto: esclusi.)

## Etichette della vista «aree»: prima e dopo

- **Prima**: 73 aree con un nome; 19 nomi ripetuti (per esempio Moncalieri 8 volte, Collegno 6, Parella 5). Il disegno ne mostrava molte insieme.
- **Dopo**: 22 etichette, tutte con nome diverso (nessun nome ripetuto). Il test lo verifica a ogni prova.

## Descrizioni dei profili (sei profili richiesti)

- **Stura** (589 posti): sempre quasi pieno: 80% di notte, 90% di giorno.
- **Lingotto** (3.100 posti): andamento irregolare: 3% di notte, 7% di giorno. Non è più «misto», ma non è la descrizione «sempre basso» che si potrebbe aspettare: l'ampiezza è 6,8 punti, appena sopra la soglia di 6 del piano.
- **Caio Mario** (418 posti): il valore non cambia (2%): forse il contatore è fermo. Il piano scrive 1%: il valore di giorno è 1,5, arrotondato a 2.
- **Sofia** (272 posti): è più pieno di notte che di giorno: 55% di notte, 32% di giorno.
- **Venchi Unica** (437 posti): sempre intorno al 51%.
- **Porta Susa FS** (123 posti): si riempie di giorno anche nel weekend: 37% di notte, 79% di giorno.

Comportamenti medi (solo gruppi con almeno 2 garage): si riempie nei giorni feriali (19 garage); si riempie di giorno anche nel weekend (7); è più pieno di notte che di giorno (2); il valore non cambia (2); andamento irregolare (5).

## Screenshot (per la scheda)

- `immagini/r6_parcheggi.png`: 486.181 byte
- `immagini/r6_aree.png`: 501.798 byte
- `immagini/r6_mancano.png`: 465.837 byte

Dimensioni tutte sopra i 20 KB (non sono pagine vuote). Ho guardato a occhio gli screenshot delle viste «aree» e «mancano»: la mappa si vede, la legenda è aperta, le etichette sono una per nome, i 20 punti sono numerati.

## Numeri di controllo (non cambiati)

378 fermate; 147 / 59 / 172 per classe; 73 aree (tra 55 e 110); auto in entrata 95.297 (±1); domanda 24.459 (±5); 212 parcheggi mostrati; 41 profili; soglia 10% = 378 fermate di S2. Nessun criterio, soglia o parametro cambiato.

## File modificati o creati

- Nuovo: `scripts/prova_pagine_r6.py`, `immagini/r6_parcheggi.png`, `immagini/r6_aree.png`, `immagini/r6_mancano.png`, `docs/ESITO_R6_CORREZIONI.md`.
- Modificati: `scripts/mappa_template.html` (r6Data, legenda robusta, vista da URL, etichette, descrizione nel clic, testi pubblici), `scripts/80_porte_interscambio.py` (etichette, descrizioni), `scripts/79_dati_mappa_r6.py` (campi nuovi), `scripts/04_genera_mappa.py` (stampa), `scripts/schede_risultati.py` (descrizioni, nodo di trasporto, tag, avviso).
- Rigenerati: `mappa_torino.html`, `data/schede_risultati.js`, `data/processed/risultato6_v2/porte.json`, `data/processed/risultato6_v2/mappa_r6.json`, `docs/RAPPORTO_R6_PORTE.txt`, `data/processed/risultato6_riepilogo_mappa.json`.
- Non toccati: `MEMORIA_PROGETTO.md`, `data/ref/*`, script 68-78, `data/raw`, lo storico.

## Anomalie e cose da sapere

1. **Il test vede la pagina, ma non la usa.** Controlla errori, pannello e legenda; non clicca. Clic, zoom e scheda vanno ancora controllati a mano (o da Claude nel browser).
2. **Il browser integrato non apre né `localhost` né il file.** Per questo la prova usa Edge headless (via PowerShell).
3. **Le descrizioni dei profili usano i numeri arrotondati**: Stura 80% invece di 79% (valore reale 79,5), Caio Mario 2% invece di 1%.
4. **Lingotto** è «andamento irregolare» e non «sempre basso»: è una conseguenza della regola, da discutere se si vuole un testo diverso.
5. Restano aperti come prima: 23 luoghi senza zona IMQ, la lista di parcheggi «sempre pieni» da verificare, e il fetch del 25/10 con la catena 71 → 72 → 73 → 75 → 76 → 80 → 79.
