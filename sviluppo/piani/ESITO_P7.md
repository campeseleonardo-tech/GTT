# Esito P7 (23/10/2026, PC)

## Cosa è stato fatto
- `python scripts/rifai_tutto.py --elenco` e `--prova-secca`: 70 comandi in 12 fasi, tutti gli script esistono.
- **Correzione alla lista** (commit a parte): `17_taglia_osm.py` si ferma se manca `data/raw/nord-ovest-261008.osm.pbf` (l'OSM grezzo del Nord-Ovest non è su questo PC; l'estratto tagliato `data/otp/rete/torino_cintura.osm.pbf` c'è già). Ora la fase «dati» lo salta con un messaggio (`salta_se_manca=` nella nota del comando).
- **Fase «dati»** (05, 08, 11, 19, 20): rifatta, **tutto uguale** al commit salvo la data di generazione.
- **Fase «accessibilita»**: lanciata e **fermata a mano dopo 24 minuti**: l'orario 00 di 24 richiede circa 47 minuti, quindi il giro intero dura circa **19 ore**. Il GTFS (20261002) e i parametri non sono cambiati, quindi `accessibilita*.json` restano quelli del commit. Lasciare a Leo di notte, se vuole: `python scripts\rifai_tutto.py --solo accessibilita` (riprende dai parziali in `data/processed/accessibilita_parziale/`, rimasti sul disco).
- **Fasi «traffico», r1, r4, r8, r6, r10, schede, mappa, prova** (`--da traffico`): **tutte finite senza errori in 49 minuti**, `prova_pagine.py` 0 errori su 20 pagine, nessuna fase fuori ordine, nessun prerequisito mancante. Gli AVVISI del log sono quelli già noti (Porta Nuova 16 minuti invece di 15, sensori fuori rete, parcheggi senza linee, ecc.).

## Differenze rispetto al commit (NON committate)
Il rilancio dà numeri diversi in R4, R6 e R8 e **non l'ho tenuto**: ho ripristinato tutti i file com'erano nel commit. Le differenze vengono dai dati, non dal codice: gli script 26, 27, 33, 70, 71, 88 leggono lo storico vivo `data/storico_backup.sqlite`, che dal momento dei calcoli del 21-22/10 ha altri giorni (il backup è di oggi).
- **R4**: oltre 5 minuti 14,1% → 15,6%; oltre 10 minuti 5,44% → 6,19%; grappolo+buco 20,9% → 21,6%; anticipo 37,9% → 36,2% (7 feriali invece di 6 nel commit).
- **R8**: residenti vicino a strade molto trafficate 190.255 (22,6%) → 205.034 (24,4%); errore del modello ±38% → ±28% (i sensori hanno più giorni).
- **R6**: cambiano riempimento, porte e segnali (più giorni di parcheggi).
- Sono invece uguali: area che si espande, case × fragilità (R10), vulnerabilità, catalogo, R1 salvo la parte traffico.
Questi numeri nuovi sono già quelli che servirebbero per P8 (R4 con più dati); la decisione di aggiornare i risultati (e README, schede) è di Leo.

## Prova «da zero» (cartella temporanea fuori dal progetto)
`git clone` dell'ultimo `prova` (4d72f88) → `python scripts/scarica_dati.py` (Release `dati-2026-10`: 220 file scritti, hash OK) → `python scripts/rifai_tutto.py --solo schede,mappa`: **nessun errore**; `data/schede_risultati.js` e i cinque riepiloghi dei risultati sono **uguali al commit salvo le date**, `mappa_torino.html` differisce solo per una riga (la data).
Non provato da zero: le fasi che richiedono IMQ e OMI (a mano) e l'OSM grezzo.
