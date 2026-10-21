# Esito — correzioni urgenti, `ANALISI_STATO.md` 5.1 punti 1-4 (21/10/2026)

Prima: ramo `prova`, albero pulito, pull e merge fast-forward di `origin/claude/vibrant-planck-cztsh9` (solo `ANALISI_STATO.md` e `MEMORIA_PROGETTO.md`), nessun conflitto.

| # | Punto | Esito | Note |
|---|---|---|---|
| 1 | Dato personale | OK | Cartella OMI rinominata con `mv` in `data/raw/omi_2025_2` (unico cambio in `data/raw`). Script 08 e `docs/FONTI_DATI.md` aggiornati; i due CSV si cercano per suffisso (`*_VALORI.csv`, `*_ZONE.csv`) perché anche i loro nomi portano un codice di richiesta. Email tolta dall'intestazione di 01, 03 e 12: resta «GTT-progetto-personale/0.1 (studio personale)». `git grep` per il vecchio nome, per il codice e per l'email: **nessun risultato**. Lo script 08 gira sul nuovo percorso (47 zone di Torino, controlli OK). La storia di git non è riscritta: il vecchio nome **resta nei commit passati** (decisione di Leo se pulirla). |
| 2 | README | OK | Numeri dei risultati tolti, al loro posto «Risultati in aggiornamento: vedi la pagina dei risultati» (italiano) e «Results being updated: see the results page.» (inglese). Stessa modifica nel testo dello script 86, che non legge più le schede per scrivere il README. «Leo» tolto da README e script 86. |
| 3 | Catalogo nella pubblicazione | OK | Lo script 86 copia `data/catalogo/*.js` in `pubblica/data/catalogo/` (6 file; `pubblica/` 23,6 MB). `prova_pagine_r6.py --cartella pubblica`: **0 errori su 13 pagine**; in più aperto «Luoghi della città» da `pubblica/` in Chromium: 6 gruppi, 10 dati nel primo gruppo. |
| 4 | «Tutti i servizi»: percentili separati | OK | Le sezioni di Torino si confrontano solo con quelle di Torino, quelle della cintura solo con quelle della cintura. Legenda: «Confronto con le zone di Torino … con le zone della cintura» (+ nota OpenStreetMap); scheda: «più di N% delle sezioni di Torino / della cintura». Mappa rigenerata (13,1 MB). |

## Punteggi delle 5 sezioni di controllo, rifatti (a piedi 15' | coi mezzi 45' alle 8; tra parentesi: giro 2)

| Sezione | A piedi | Coi mezzi | 5 gruppi a piedi: scuole · salute · negozi · fermate · verde (valore, percentile nell'area) |
|---|---|---|---|
| Centrale, Torino, Piazza Castello | **86** (92) | **85** (93) | 60 (94) · 46 (99) · 4.242 (98) · 104 (93) · 98 (47) |
| Periferica, Torino, Falchera | **12** (48) | **6** (47) | 7 (9) · 6 (13) · 191 (10) · 42 (14) · 40 (11) |
| Periferica, Torino, Mirafiori Sud | **11** (46) | **16** (56) | 7 (9) · 7 (16) · 152 (9) · 36 (12) · 33 (9) |
| Cintura, Venaria Reale | **68** (38) | **75** (40) | 7 (81) · 5 (69) · 14 (62) · 28 (75) · 27 (52) |
| Cintura, Rivoli, vicino al centro | **93** (59) | **64** (34) | 16 (99) · 16 (98) · 231 (98) · 36 (88) · 73 (83) |

Calcolo ripetuto in Python con la stessa regola e confermato in Chromium (legenda e scheda nuove).

**Cosa cambia, da sapere (AVVISO).** Con percentili separati la media dei punteggi è 50 sia in Torino sia in cintura: **i punteggi non sono più confrontabili fra le due aree**. Una sezione di cintura con 68 non è «meglio servita» di una torinese con 12: è meglio delle altre sezioni di cintura.
Anche dentro Torino la periferia scende molto (Falchera 12, Mirafiori Sud 11) perché ora si confronta con la sola Torino, dove il centro è molto servito. Il giro 2 aveva «centro alto, cintura bassa», che ora non vale più per costruzione; è il prezzo di togliere il falso rosso della cintura dovuto ai dati OpenStreetMap più poveri. Se serve far vedere anche il confronto fra le due aree, l'alternativa dell'analisi è la cintura in grigio per i gruppi OSM.

## Prove

- `python scripts\04_genera_mappa.py`: OK. `python scripts\prova_pagine_r6.py --senza-screenshot`: 0 errori su 13 pagine. `python scripts\86_prepara_pubblicazione.py`: OK, 0 avvisi.

## Pulizia

Cancellati `ESITO_DOCUMENTI.md`, `ESITO_MAPPA_GIRO1.md`, `ESITO_MAPPA_GIRO2.md`, `ESITO_R4_GTT.md` (giri già ricontrollati; i risultati vivono in `MEMORIA_PROGETTO.md`, `docs/R4_puntualita.md` e nei piani).
