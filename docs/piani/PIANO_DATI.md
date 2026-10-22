# Piano 2 — Tutti i dati necessari su GitHub

Obiettivo (Leo, 22/10): **su GitHub c'è tutto quello che serve** per aprire le pagine e rifare i calcoli.
Decisione di Leo: **estratti nel repository + archivi grandi in una Release di GitHub**, con uno script che li scarica.

Limiti di GitHub da rispettare: file singolo < 100 MB (sopra 50 MB avvisa); repository consigliato < 1 GB;
file di una Release fino a 2 GB l'uno. Lo storico del Pi pesa 2,1 GB e cresce di circa 190 MB al giorno.

## Tre posti per i dati

| Posto | Cosa ci va | Esempi |
|---|---|---|
| **In git** (`data/…` tolto da `.gitignore` solo per le cartelle scelte) | file piccoli che servono alle pagine o sono il risultato dei calcoli; riferimenti scritti a mano | `data/schede_risultati.js`, `data/processed/orari_fermate.js`, `data/catalogo/*.js`, `data/ref/`, `data/scenari/`, i `*_riepilogo_mappa.json` e i JSON piccoli in `data/processed/` |
| **Release di GitHub** (archivi zip con data nel nome, es. `dati-grezzi-2026-10.zip`) | dati grezzi grandi e copie dello storico | GTFS GTT, estratto OSM, censimento e basi territoriali, IMQ, OMI, storico del Pi (copia compressa, una al mese) |
| **Si riscaricano dalla fonte** | dati grandi, liberi e sempre allo stesso indirizzo | se la licenza non permette di ripubblicarli, solo l'indirizzo e lo script che li scarica |

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **Inventario**: script `96_inventario_dati.py` che elenca ogni file di `data/` con peso e quali script lo leggono o lo scrivono (cerca i nomi nel codice); scrive `docs/DATI.md` con una proposta di posto (git / Release / fonte) | CLOUD (script) → PC (lancio) | piccolo |
| 2 | **Licenze delle fonti**, una per una, scritte in `docs/FONTI_DATI.md`: GTT GTFS e GTFS-RT, 5T, ISTAT, IMQ 2022 (Agenzia della Mobilità Piemontese), OMI (Agenzia delle Entrate: verificare se le quotazioni si possono ripubblicare o solo citare), catalogo aperTO, OSM (ODbL: i dati derivati da OSM vanno condivisi con la stessa licenza: va scritto) | CLOUD (ricerca) + Leo conferma | medio |
| 3 | **Decidere fonte per fonte** con l'inventario e le licenze (tabella in `docs/DATI.md`) | Leo + Claude | piccolo |
| 4 | **Estratti dello storico**: invece dei 2,1 GB, tabelle già aggregate che bastano ai calcoli dei risultati (es. passaggi per corsa e fermata dal GPS, medie per sensore 5T e ora, riempimento dei parcheggi per ora) in file compressi per mese; più **un'ora tipica di posizioni dei mezzi** per l'animazione della home (piano 4) | CLOUD (script) → PC (lancio) | medio |
| 5 | **`.gitignore` nuovo**: `data/raw/` e lo storico restano fuori; le cartelle scelte entrano. Controllo: nessun file sopra 50 MB, totale sotto 300 MB | CLOUD | piccolo |
| 6 | **Release**: script `97_prepara_release.py` che crea gli zip con l'elenco dei file e un codice di controllo (sha256) per ciascuno; Leo li carica nella pagina Releases di GitHub (a mano, o con `gh release upload` se installa la riga di comando di GitHub) | CLOUD (script) → PC + GITHUB | piccolo |
| 7 | **Scaricare tutto**: `scripts/scarica_dati.py` (estende lo 01) che prende gli zip della Release e le fonti pubbliche, controlla i codici e li mette nelle cartelle giuste | CLOUD | piccolo |
| 8 | **Prova da zero**: in una cartella vuota, `git clone` + `scarica_dati.py` + catena dei risultati → stessi numeri delle schede | CLOUD (con la Release pubblica) | medio |
| 9 | **Aggiornamento**: una volta al mese uno zip nuovo dello storico nella Release; i file in git si aggiornano quando si rifanno i risultati | PC (Leo) | ricorrente |

## Regole
- Nessun dato personale (i dati del progetto non ne hanno: posizioni dei mezzi, sensori, censimento per sezione).
- `data/raw` e lo storico restano in sola lettura: gli script nuovi copiano, non modificano.
- Prima del commit: `git status` e controllo dei pesi (passo 5).

## Domande aperte per Leo
- I file `.zip`, `.pdf` e `.doc` sono esclusi da git: alcuni servono ai calcoli (es. il PDF del rapporto GTT 2025 per lo
  script 30)? Si mettono nella Release.
- Lo storico completo (non solo gli estratti) ti interessa averlo pubblico, una copia al mese, o bastano gli estratti?
