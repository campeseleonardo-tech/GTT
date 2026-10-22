# Piano 2 — Tutti i dati necessari su GitHub

Obiettivo (Leo, 22/10): **su GitHub c'è tutto quello che serve** per aprire le pagine e rifare i calcoli.
Decisioni di Leo: **estratti nel repository + archivi grandi in una Release di GitHub**, con uno script che li scarica;
dello storico del Pi bastano **i dati già riassunti** (non la copia intera).

Limiti di GitHub: file singolo < 100 MB (sopra 50 MB avvisa); repository consigliato < 1 GB; file di una Release fino a 2 GB.

## Tre posti per i dati

| Posto | Cosa ci va | Esempi |
|---|---|---|
| **In git** (cartelle scelte di `data/`, tolte da `.gitignore`) | file piccoli che servono alle pagine o sono il risultato dei calcoli; riferimenti scritti a mano; **riassunti dello storico** | `data/schede_risultati.js`, `data/processed/orari_fermate.js`, `data/catalogo/*.js`, `data/ref/`, `data/scenari/`, JSON piccoli in `data/processed/`, `data/storico_riassunti/` |
| **Release di GitHub** (zip con la data nel nome, es. `dati-grezzi-2026-10.zip`) | dati grezzi grandi che servono ai calcoli | GTFS GTT usato, estratto OSM, basi territoriali e censimento, IMQ, OMI, PDF del rapporto GTT 2025 (script 30) |
| **Si riscaricano dalla fonte** | dati grandi la cui licenza non permette di ripubblicarli | solo indirizzo e script che li scarica |

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **FATTO (C2; lancio sul PC: P2)**: inventario: script `96_inventario_dati.py` che elenca ogni file di `data/` con peso e quali script lo leggono o lo scrivono; scrive `docs/DATI.md` con una proposta di posto (git / Release / fonte) | CLOUD (script) → PC (lancio) | piccolo |
| 2 | **FATTO (C2; Leo conferma)**: licenze delle fonti, una per una, in `docs/FONTI_DATI.md`: GTT GTFS e GTFS-RT, 5T, ISTAT, IMQ 2022, OMI (si possono ripubblicare le quotazioni o solo citare?), aperTO, OSM (ODbL: i dati derivati si condividono con la stessa licenza) | CLOUD (ricerca) + Leo conferma | medio |
| 3 | **FATTO (22/10, `docs/DATI.md`)**: decidere fonte per fonte con inventario e licenze (tabella in `docs/DATI.md`) | Leo + Claude | piccolo |
| 4 | **Riassunti dello storico** (script `97_riassunti_storico.py`): passaggi per corsa e fermata dal GPS (R4), medie per sensore 5T e ora (R8), riempimento dei parcheggi per ora (R6), un file compresso per mese; **gli script dei risultati leggono i riassunti** quando lo storico non c'è. Più **un'ora tipica di posizioni dei mezzi** (≤ 300 KB) per l'animazione della home (piano 4, A) | CLOUD (script) → PC (lancio) | medio |
| 5 | **`.gitignore` nuovo**: `data/raw/` e lo storico restano fuori; entrano le cartelle scelte. Controllo automatico: nessun file sopra 50 MB, totale sotto 300 MB | CLOUD | piccolo |
| 6 | **Release**: script `98_prepara_release.py` che crea gli zip con l'elenco dei file e un codice di controllo (sha256); Leo li carica nella pagina Releases | CLOUD (script) → PC + GITHUB | piccolo |
| 7 | **`scripts/scarica_dati.py`** (estende lo 01): scarica gli zip della Release e le fonti pubbliche, controlla i codici, mette i file al loro posto | CLOUD | piccolo |
| 8 | **Aggiornamento**: i riassunti si rifanno insieme ai risultati; uno zip nuovo nella Release solo se cambiano i dati grezzi (es. GTFS nuovo) | PC | ricorrente |

La prova finale «da zero» (clone + `scarica_dati.py` + `rifai_tutto.py` = stessi numeri) sta nel piano 5, passo 3.

## Regole
- Nessun dato personale (posizioni dei mezzi, sensori, censimento per sezione: nessuno lo è).
- `data/raw` e lo storico in sola lettura: gli script nuovi leggono e scrivono altrove.
- Prima del commit: `git status` e controllo dei pesi (passo 5).
