# Esito pulizia script, .bat e memoria (passi 8, 9, 12 di PIANO_DOCUMENTI)

Fatto nel cloud, senza dati né Windows. Controllo con `git grep` per ogni nome cancellato: 0 risultati fuori da questo file.

## Script cancellati
- `scripts/archivio/` (tutta la cartella, 22 file). Prima spostati in `scripts/prove/`: `controllo_valori_giro4.js`, `estrai_dati_giro4.py`, `trasforma_dati_giro4.py`.
- `34_sensori_corridoi.py`: scrive `sensori_corridoi.json` (v1) che non legge nessuno; il v2 lo scrive il 36. Non è in nessun `.bat`.
- `89_proposta_fermate_importanti.py`: solo proposta (Leo ha scelto N 10, M 1.000); il 83 ne leggeva il rapporto per un controllo, tolto (ora il 83 non dipende da nessun rapporto).
- `90_verifica_ritardi_gps.py`, `91_risultato4_gps_prova.py`: prove chiuse; il 27 fa già tutto il calcolo sul GPS e non le importa; nessuna scheda legge le loro uscite. Commenti del 27 aggiornati.

## Candidati controllati e NON cancellati (uno per uno)
- **37**: scrive `traffico_stimato_AB.json`, letto da 43, 44, 50, 53, 62, 63, 65; lanciato da `TRAFFICO_RILANCIA_SENSORI.bat`.
- **49, 50**: 62 legge `punti_v3`, `domanda_v3`, `porte_v3` (49) e importa il 50; 53 legge `corridoi_v3`.
- **50b**: lanciato da `TRAFFICO_RILANCIA_SENSORI.bat`; `valutazione_v3.json` letto dal 53.
- **62**: `tratte_flusso.json` letto da 65 e 67. **63**: `valutazione_fase5.json` letto da 65, 66 e dalla scheda R8; lanciato da `TRAFFICO_RILANCIA_SENSORI.bat`.
- Altri non citati per nome ma tenuti: 15, 19, 23, 25, 35, 38b, 51, 52, 56-61, 68, 69, 86 (uscite lette da altri script o dalla mappa, o prime tappe di una catena).
- **30-32** (rapporto sostenibilità): restano, ma senza `.bat` (cancellati): si lanciano con `python scripts\30_rapporto_estrai.py` e seguenti; il 31 serve una chiave DeepSeek. Dubbio: sono lavoro chiuso, si possono cancellare se Leo vuole.
- **28-29** (R2 in pausa): restano, comandi nel `docs/R2_metro_notte.md`.

## `.bat`
- Cancellati: `PI_UN_SOLO_PROCESSO` (fatto il 20/10), `sync_da_leopi` (sostituito da `RACCOLTA_GIORNALIERA`), `RAPPORTO_1_ESTRAI`, `RAPPORTO_2_FATTI`, `RAPPORTO_3_RIASSUNTO` (lavoro chiuso),
  `RISULTATO2_METRO_NOTTE`, `RISULTATO2_RICALCOLA_NUMERI` (R2 in pausa), `FASE5_MODELLO` (modello V4 chiuso; i comandi per rifarlo sono in `docs/R8_traffico.md`).
- Tenuti: `RACCOLTA_GIORNALIERA`, `INSTALLA_RACCOLTA_GIORNALIERA`, `CONTROLLA_LEOPI`, `AGGIORNA_RACCOLTA_LEOPI`, `FETCH_LEOPI_E_VELOCITA_5T`, `ACCESSIBILITA_24ORE`, `R1_PIEDI_5_10`, `RISULTATO1_VUOTI`,
  `RISULTATO1_CANDIDATI`, `RISULTATO6_RIFAI`, `TRAFFICO_RILANCIA_SENSORI`, `TRAFFICO_RICALCOLA_MODELLO`. Non rinominati: i nomi sono citati nei documenti.
- Nuovo: `RIFAI_MAPPA_E_SCHEDE.bat` (04, schede_risultati, 86, prova_pagine_r6; log `logs\rifai_mappa_e_schede.log`, si ferma al primo errore, fine riga Windows). Attenzione: il 86 riscrive `README.md` nella radice.
  Non provato su Windows (nel cloud non c'è).

## Rimandi aggiornati
Documenti (`R2`, `R4`, `R6`, `R8`, `ANALISI_STATO`, `PIANO_DOCUMENTI`, esito giro 4), script (27, 31, 32, 80, 83, `AGGIORNA_RACCOLTA_LEOPI.bat`, `TRAFFICO_RILANCIA_SENSORI.bat`).

## Memoria
`MEMORIA_PROGETTO.md` riscritta in 120 righe, stesse 8 sezioni: tolti storia dei giri, date intermedie, lavori chiusi; mantenuti regole di Leo, limiti dei dati, stato di ogni risultato con i numeri di oggi.
Da rivedere da Leo: se qualcosa che gli sta a cuore è finito fuori (i dettagli sono in git, `git show HEAD~1:MEMORIA_PROGETTO.md`).

## Da fare sul PC
`python scripts\prova_pagine_r6.py` (0 errori) e, se si vuole, un lancio di prova di `scripts\RIFAI_MAPPA_E_SCHEDE.bat`.
