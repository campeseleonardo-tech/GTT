# ESITO C2 — inventario dei dati e licenze delle fonti (cloud, 22/10/2026)

Piano 2, passi 1 e 2. Ramo della sessione `claude/ecstatic-faraday-nuy8hv` (partito da `origin/prova`, nessun ramo con lavoro non unito).

## Cosa è stato fatto
1. **`scripts/96_inventario_dati.py`** (sola lettura): elenca ogni file di `data/` con il peso; cerca il nome del file nel codice (`scripts/*.py`, `.bat`, `.ps1`, `.sh`, `scripts/prove`,
   `mappa_template.html`, le tre pagine) e dice quali script lo **leggono** e quali lo **scrivono** (euristica sulle righe: `write_text`, `open(...,"w")`, `to_csv`, `dump`, `scp`, `copy`, `>`…).
   Se il nome non compare, prova la cartella che lo contiene («via cartella») e il nome senza estensione. Propone un posto: **riassunto** (SQLite dello storico), **Release** (`data/raw/`, oltre 50 MB,
   o sopra 5 MB letto solo dagli script), **git** (sotto 5 MB letto da pagine o script, o scritto da uno script dei risultati; sopra 5 MB solo se una pagina lo carica), **fuori** (nessuno lo cita).
   Scrive `docs/DATI.md` solo fra i segnaposto `<!-- INVENTARIO:INIZIO/FINE -->`: sotto resta la sezione «Decisioni di Leo» (provato: una seconda esecuzione non la tocca). Cartelle con più di 30 file in una riga sola.
   Tabelle: totali per posto, per cartella (con colonna «Deciso» vuota), per file. Opzione `--prova`: crea una `data/` finta (file sparsi con i pesi veri, nessun disco usato) in una cartella temporanea e scrive lì `DATI_prova.md`.
   Controlli: peso negativo e somma dei posti = bloccanti; file in «git» sopra 50 MB e file «fuori» = avvisi. Prossimo numero libero: **97**.
2. **`docs/FONTI_DATI.md`**: tabella nuova in testa con licenza, pagina ufficiale, «ripubblicare sì / con condizioni / NON CHIARO», citazione da scrivere e se ho letto io la pagina; tolte le note di lavoro vecchie
   («VERIFICATO/NON VERIFICATO», «da scaricare a mano», date di scarico).

## Risultato delle licenze (dettagli e link in `docs/FONTI_DATI.md`)
| Fonte | Licenza | Ripubblicare |
|---|---|---|
| GTT GTFS-RT | CC BY (scheda aperTO letta) | con condizioni |
| GTT GTFS orari | CC BY (regola aperTO + ricerca; **la scheda dà 403, non letta**) | con condizioni, da riconfermare |
| 5T traffico, parcheggi, ZTL | IODL 2.0 dichiarata da Muoversi a Torino (non per dataset; testo IODL non aperto: 403) | con condizioni |
| ISTAT | CC BY 4.0 | sì, con attribuzione |
| aperTO (Comune) | CC BY 4.0 salvo diversa indicazione, **da controllare dataset per dataset** | con condizioni |
| OpenStreetMap | ODbL (condivisione alle stesse condizioni) | con condizioni |
| **IMQ 2022** | **nessuna licenza indicata** (© Agenzia; matrici «per studio e ricerca») | **NON CHIARO** |
| **OMI** | **nessuna licenza esplicita**, solo citazione «Agenzia delle Entrate – OMI» | **NON CHIARO** |

## Prove (cloud, senza `data/`)
- `python scripts/96_inventario_dati.py --prova`: 114 file di codice letti, 51 file finti, totali git 8 (6,0 MB), Release 41 (349,7 MB), riassunto 1 (2.002,7 MB), fuori 1: tutti i controlli OK. Il file finto
  senza riferimenti finisce in «fuori»; il pbf da 114 MB e gli zip grandi in Release; `schede_risultati.js`, `orari_fermate.js`, `catalogo/*.js` in git. Senza `--prova` e senza `data/` si ferma con un messaggio chiaro.
- Limite noto dell'euristica: un nome citato in uno script che scrive e rilegge lo stesso file compare sia in «Legge» sia in «Scrive»; un nome costruito dal codice (f-string) si trova solo «via cartella».
  Le proposte vanno guardate da Leo, non applicate alla cieca.
- Non provato sui dati veri (nel cloud non ci sono): lo fa il giro P2.

## Cosa deve fare Leo (giro P2, sul PC)
Vedi i comandi nel messaggio di chiusura: unire il ramo, lanciare `python scripts\96_inventario_dati.py`, controllare i totali (storico ~2 GB in «riassunto», `data/raw` in «Release», le pagine in «git» pochi MB),
poi commit e push di `docs/DATI.md`, e decidere fonte per fonte (soprattutto IMQ, OMI e la conferma della licenza del GTFS statico e della IODL) scrivendo le decisioni nella sezione «Decisioni di Leo».
