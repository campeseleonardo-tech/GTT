# ESITO C3 — riassunti dello storico, .gitignore, Release, scaricamento (cloud, 22/10/2026)

Piano 2, passi 4-7. Ramo della sessione `claude/ecstatic-faraday-nuy8hv`. Prima di cominciare: rami controllati (nessun lavoro fuori da `prova`).

## Cosa è stato fatto
1. **Script 97 `97_riassunti_storico.py`** + modulo `riassunti_storico.py` (sola lettura sullo storico). Scrive in `data/storico_riassunti/`:
   - `passaggi_AAAA-MM.zip` (script 27 e 70): per ogni giorno, i passaggi alle fermate misurati con il **GPS** (e quelli del **feed** dei ritardi, per il confronto del 27), corse viste, copertura, minuti di raccolta per ora.
     Per passaggio: corsa, fermata (`stop_sequence`) e ritardo in millisecondi; linea, verso, fermata e orario programmato si ricavano dal GTFS. Colonne a differenze (si comprime molto): circa **3 byte per passaggio**.
   - `sensori5t_AAAA-MM.json.gz` (script 26): per giorno locale, sensore e ora, le somme dei flussi e delle velocità delle letture affidabili (accuratezza > 0).
   - `parcheggi_AAAA-MM.json.gz` (script 71): per giorno locale, parcheggio e ora, letture valide e somma dell'occupazione.
   - `anagrafica.json` (sensori e parcheggi) e **`ora_tipica.json`**: le posizioni di tutti i mezzi in un feriale tipico (quello con la mediana delle corse viste) fra le 7:30 e le 8:30, una ogni 30 secondi,
     coordinate in interi da 1e-5 gradi (la prima assoluta, poi le differenze); al massimo 300 KB (se serve si tiene un mezzo ogni N, e lo dice).
   Incrementale: rifà solo i mesi o i giorni nuovi (gli ultimi 2 giorni sempre); `--mese AAAA-MM`, `--solo passaggi|5t|parcheggi|ora`, `--rifai`. Controlli: righe lette e scritte che tornano, nessun valore negativo, date dentro la raccolta, posizioni dentro Torino.
2. **Script 27, 70, 26 e 71** leggono lo storico se c'è, altrimenti i riassunti (`--riassunti` per forzarlo). I calcoli non sono cambiati: lo storico passa per le stesse funzioni di prima (27: classe `SorgenteDb`; 26 e 71: la funzione di riassunto
   dello 97 usata al volo). Il rapporto dice la sorgente. Il controllo col GPS del 70 (solo il giorno di prova) dai riassunti legge il risultato calcolato dal 97.
3. **`.gitignore` nuovo**: `data/*` fuori, con eccezioni per `catalogo/`, `processed/`, `ref/`, `scenari/`, `storico_riassunti/`, `schede_risultati.js`; restano fuori `*.sqlite*`, cache (`accessibilita_parziale*`) e `processed/imq/` (IMQ: fonte). Le esclusioni
   file per file dentro le cartelle tenute le scrive `python scripts/96_inventario_dati.py --gitignore` fra i segnaposto `# >>> data` e `# <<< data`.
   **`scripts/controlla_pesi_git.py`** (anche dentro `prova_pagine.py`): nessun file in git sopra 50 MB (ERRORE), totale sotto 300 MB (ERRORE), file sopra 5 MB = AVVISO.
4. **Script 98 `98_prepara_release.py`**: crea in una cartella fuori da git (default `<progetto>_release` accanto al progetto) gli zip `dati-grezzi-istat-AAAA-MM`, `dati-grezzi-altri-AAAA-MM`, `dati-calcolati-AAAA-MM` (ciascuno sotto 1,9 GB,
   altrimenti diviso) con dentro `ELENCO.txt` e `SHA256SUMS`, più `SHA256SUMS.txt` (hash degli zip) e `LEGGIMI_RELEASE.txt`. Prende i file con posto «Release» dell'inventario: **IMQ e OMI non ci sono** (decisione di Leo).
5. **`scripts/scarica_dati.py`**: scarica `SHA256SUMS.txt` e gli zip dall'ultima Release (`https://github.com/campeseleonardo-tech/Turin-mobility/releases/latest/download/`), controlla gli hash (zip e singoli file), mette i file in `data/`,
   salta quelli uguali, non sovrascrive quelli diversi (AVVISO, `--sovrascrivi` per forzare), rifiuta percorsi fuori da `data/`; `--fonti` scarica anche le zone statistiche del Comune; alla fine scrive cosa resta a mano (IMQ, OMI). `--prova` non scarica.
6. Anche: `scripts/confronta_riassunti.py` (sul PC: confronto storico contro riassunti sui dati veri), `scripts/RIASSUNTI_STORICO.bat`, `scripts/prove/storico_finto.py` e `scripts/prove/prova_riassunti.py`.

## Prove (cloud, con uno storico FINTO: 7 giorni di ritardi e GPS, 6 di 5T e parcheggi, GTFS con 4 linee)
- `python scripts/prove/prova_riassunti.py`: lo script 97 sullo storico finto, poi 27, 70, 26 e 71 **dallo storico e dai riassunti**: JSON e rapporti **identici** (differenza massima 0,000000; i riassunti salvano il ritardo al millisecondo).
- Controllo contro il codice di prima: gli stessi script del commit precedente, sullo stesso storico finto, danno gli stessi JSON e rapporti (cambia solo il testo «fonte» di `velocita_5t.json`).
- `97 --prova`: tutti i controlli OK, ora tipica di 88 mezzi in 17 KB. `98 --prova` e `scarica_dati.py --url file://...`: zip creati e riaperti, hash OK, seconda esecuzione «già uguali», file diverso non sovrascritto, zip alterato scartato,
  percorso `data/../` rifiutato. `96 --prova --gitignore`: con `git add -A` finiscono in git solo i file «git» dell'inventario.
- `python -m py_compile` e `pyflakes` sui file nuovi e toccati: puliti.
- **Non provato** (nel cloud non ci sono i dati veri): i pesi veri, la durata, l'ora tipica sui dati veri, il confronto sui numeri veri. Sono il giro P3.

## Da sapere
- **Peso dei riassunti**: stima prudente 1-2 MB al giorno per `passaggi_*.zip` (GPS + feed), cioè 30-60 MB al mese: sono tanti per git (limite scelto: 300 MB in tutto). Il 97 stampa il peso vero. Se pesano troppo,
  la parte del feed (serve solo al «CONFRONTO COL FEED» del 27) si può togliere o spostare nella Release: dimmelo e lo faccio.
- Lo storico resta la fonte vera sul PC: i riassunti si rifanno con lo 97 dopo ogni raccolta (si può aggiungere a `RACCOLTA_GIORNALIERA.bat` quando i pesi sono noti).
- Il `.gitignore` ora ignora `data/` con `data/*`: **prima del commit controlla con `git status`**; il blocco `# >>> data` è vuoto finché non si lancia `96 --gitignore`.

## Giro P3 sul PC (comandi esatti)
Vedi il messaggio di chiusura. In breve: unire il ramo; `scripts\RIASSUNTI_STORICO.bat` (o `python scripts\97_riassunti_storico.py`, prima con `--mese 2026-10`); guardare i pesi; `python scripts\confronta_riassunti.py` (deve finire con «avvisi: 0»);
`python scripts\96_inventario_dati.py --gitignore`; `python scripts\controlla_pesi_git.py`; `python scripts\98_prepara_release.py`; caricare gli zip e `SHA256SUMS.txt` nella Release; commit e push.
