# Dati del progetto

Dove deve stare ogni file di `data/`: in git, nella Release di GitHub, come riassunto o fuori. La parte fra i segnaposto la riscrive `scripts/96_inventario_dati.py`; sotto, nella sezione «Decisioni di Leo», si scrivono le decisioni (non viene toccata).

<!-- INVENTARIO:INIZIO -->

*Inventario scritto da `scripts/96_inventario_dati.py` il 22/10/2026 sulla cartella `data/`. Le proposte sono automatiche (regole in testa allo script): decide Leo, fonte per fonte (piano 2, passo 3).*

### Totali per posto

| Posto | File | Peso (MB) | Cosa vuol dire |
|---|---|---|---|
| git | 255 | 127,0 | dentro il repository |
| Release | 539 | 1.006,7 | zip nella Release di GitHub |
| riassunto | 2 | 2.395,4 | dello storico si tengono solo i riassunti (script 97) |
| fuori | 406 | 315,0 | nessuno lo cita: non si pubblica |
| **tutto** | 1202 | 3.844,2 | |

Avvisi: file in «git» sopra 50 MB: 0.

### Per cartella

| Cartella | File | Peso (MB) | git | Release | riassunto | fuori | Deciso |
|---|---|---|---|---|---|---|---|
| `data/(radice di data)` | 29 | 2.487,5 | 4 | 2 | 1 | 22 | |
| `data/IMQ2013-22_zone_camp_TO` | 6 | 0,1 | 0 | 0 | 0 | 6 | |
| `data/IMQ2022_opendata_web` | 1 | 59,9 | 0 | 1 | 0 | 0 | |
| `data/IMQ2022_zone_camp_noTO` | 7 | 5,8 | 0 | 0 | 0 | 7 | |
| `data/backup` | 2 | 22,6 | 0 | 0 | 0 | 2 | |
| `data/backup/risultato6_v2_prima_correzioni` | 19 | 18,1 | 0 | 0 | 0 | 19 | |
| `data/catalogo` | 6 | 4,4 | 5 | 1 | 0 | 0 | |
| `data/otp/jdk-25.0.4.1+1-jre` | 320 | 179,1 | 0 | 0 | 0 | 320 | |
| `data/otp/rete` | 2 | 32,4 | 0 | 2 | 0 | 0 | |
| `data/processed` | 59 | 79,1 | 45 | 5 | 0 | 9 | |
| `data/processed/accessibilita_parziale` | 17 | 1,1 | 0 | 0 | 0 | 17 | |
| `data/processed/accessibilita_parziale_test` | 3 | 0,0 | 0 | 0 | 0 | 3 | |
| `data/processed/catalogo` | 7 | 4,4 | 6 | 1 | 0 | 0 | |
| `data/processed/imq` | 6 | 11,1 | 5 | 1 | 0 | 0 | |
| `data/processed/rapporto_gtt` | 105 | 5,4 | 104 | 1 | 0 | 0 | |
| `data/processed/risultato6_v2` | 24 | 19,6 | 24 | 0 | 0 | 0 | |
| `data/processed/traffico_c` | 37 | 62,4 | 32 | 4 | 1 | 0 | |
| `data/processed/traffico_d` | 40 | 166,1 | 28 | 12 | 0 | 0 | |
| `data/raw` | 45 | 38,9 | 0 | 45 | 0 | 0 | |
| `data/raw/IMQ2022_opendata_web` | 2 | 59,9 | 0 | 2 | 0 | 0 | |
| `data/raw/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024` | 1 | 0,1 | 0 | 1 | 0 | 0 | |
| `data/raw/ex_quartieri` | 6 | 0,1 | 0 | 6 | 0 | 0 | |
| `data/raw/istat` | 139 | 557,3 | 0 | 139 | 0 | 0 | |
| `data/raw/omi_2025_2` | 314 | 10,9 | 0 | 314 | 0 | 0 | |
| `data/ref` | 2 | 0,0 | 1 | 0 | 0 | 1 | |
| `data/scenari` | 3 | 17,8 | 1 | 2 | 0 | 0 | |

### Per file

Le cartelle con più di 30 file sono in una riga sola (elenco completo: rilanciare lo script e guardare `--data`).

#### `data/(radice di data)`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `STOP_RACCOLTA.txt` | 0,0 | supervisore.py | supervisore.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `agg_cache.json` | 1,5 | RACCOLTA_GIORNALIERA.bat | 06_dati_live.py, RACCOLTA_GIORNALIERA.bat | git | nome |
| `get_fdt.xml` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `get_pk.xml` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `live.js` | 0,0 | 06_dati_live.py, RACCOLTA_GIORNALIERA.bat, supervisore.py | RACCOLTA_GIORNALIERA.bat | git | nome |
| `rapporto_di_sostenibilita_2025.pdf` | 3,1 | 31_rapporto_fatti.py | 30_rapporto_estrai.py | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |
| `replay_2026-10-04.js` | 3,6 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-05.js` | 6,7 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-06.js` | 5,2 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-07.js` | 4,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-08.js` | 6,2 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-09.js` | 3,1 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-10.js` | 3,1 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-11.js` | 3,6 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-12.js` | 5,7 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-13.js` | 5,1 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-14.js` | 6,4 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-15.js` | 6,2 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-16.js` | 6,8 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-17.js` | 4,5 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-18.js` | 0,6 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-19.js` | 2,5 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-20.js` | 6,6 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-21.js` | 6,6 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `replay_2026-10-22.js` | 1,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `schede_risultati.js` | 0,1 | RIFAI_MAPPA_E_SCHEDE.bat, index.html, prova_pagine.py, prova_scheda_case.py (+2) | schede_risultati.py | git | nome |
| `stat.js` | 0,2 | 04_genera_mappa.py, 06_dati_live.py, 26_velocita_5t.py, RACCOLTA_GIORNALIERA.bat (+1) | RACCOLTA_GIORNALIERA.bat | git | nome |
| `storico_backup.sqlite` | 2.395,3 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+6) | — | riassunto | storico della raccolta: si tengono i riassunti (script 97); nome |
| `supervisore_stato.json` | 0,0 | — | supervisore.py | Release | sopra 5 MB, letto solo dagli script; nome |

#### `data/IMQ2013-22_zone_camp_TO`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2013-22_zone_camp_TO.cpg` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2013-22_zone_camp_TO.dbf` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2013-22_zone_camp_TO.prj` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2013-22_zone_camp_TO.qmd` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2013-22_zone_camp_TO.shp` | 0,1 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2013-22_zone_camp_TO.shx` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |

#### `data/IMQ2022_opendata_web`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_opendata_web.accdb` | 59,9 | 13_esporta_imq.ps1 | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |

#### `data/IMQ2022_zone_camp_noTO`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_zone_camp_noTO.cpg` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.dbf` | 0,2 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.prj` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.qix` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.qmd` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.shp` | 5,5 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `IMQ2022_zone_camp_noTO.shx` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |

#### `data/backup`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `mappa_torino_prima_correzioni.html` | 22,6 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+7) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `schede_risultati_prima_correzioni.js` | 0,1 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+7) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |

#### `data/backup/risultato6_v2_prima_correzioni`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `eventi.json` | 0,0 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+7) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `istat2011_proporzioni.json` | 0,0 | 73_segnali_criticita.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi_funzione.json` | 1,2 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `riempimento.json` | 0,0 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | 71_parcheggi_riempimento.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `segnali.json` | 2,1 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `istat2011_proporzioni.json` | 0,0 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+7) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `mappa_r6.json` | 0,3 | 04_genera_mappa.py, 79_dati_mappa_r6.py, prova_pagine.py, schede_risultati.py | 79_dati_mappa_r6.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi_funzione.json` | 1,8 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `porte.json` | 0,3 | 41_zone_punti.py, 49_v3_punti_domanda.py, 50_v3_assegnazione.py, 62_v4_modello.py (+5) | 41_zone_punti.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `riempimento.json` | 0,1 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | 71_parcheggi_riempimento.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `segnali.json` | 2,7 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |

#### `data/catalogo`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `commercio.js` | 2,8 | 11_prepara_catalogo.py, 18_accessibilita.py, 20_servizi_osm.py, 49_v3_punti_domanda.py (+3) | — | git | via nome senza estensione |
| `istruzione.js` | 0,1 | 87_popolarita_zone.py | — | git | nome |
| `reti.js` | 1,2 | — | 11_prepara_catalogo.py | Release | sopra 5 MB, letto solo dagli script; nome |
| `salute.js` | 0,1 | 04_genera_mappa.py, 11_prepara_catalogo.py, 15_prepara_zone_imq.py, 18_accessibilita.py (+10) | 04_genera_mappa.py, 11_prepara_catalogo.py | git | via cartella |
| `servizi.js` | 0,0 | 95_case_fragilita_servizi.py, prova_scheda_case.py, schede_risultati.py | 95_case_fragilita_servizi.py, prova_scheda_case.py | git | nome |
| `sicurezza_sport.js` | 0,1 | 11_prepara_catalogo.py, 49_v3_punti_domanda.py, 87_popolarita_zone.py, mappa_template.html (+1) | — | git | via nome senza estensione |

#### `data/otp/jdk-25.0.4.1+1-jre`

320 file, 179,1 MB (fuori: 320). Letti da: 01_scarica_dati.py, 04_genera_mappa.py, 05_prepara_sezioni.py, 06_dati_live.py, 11_prepara_catalogo.py, 12_ritardi_gtt.py (+56). Scritti da: 04_genera_mappa.py, 88_confronto_auto_sensori.py, TRAFFICO_RILANCIA_SENSORI.bat.

#### `data/otp/rete`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `gtt_gtfs_20261003_224530.zip` | 11,7 | 18_accessibilita.py, 21_risultato1_vuoti.py, 25_risultato6_interscambio.py, 27_risultato4_regolarita.py (+7) | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |
| `torino_cintura.osm.pbf` | 20,6 | 17_taglia_osm.py, 18_accessibilita.py, 20_servizi_osm.py, 24_importanza_vie.py (+9) | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |

#### `data/processed`

59 file, 79,1 MB (git: 45, Release: 5, fuori: 9). Letti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 16_prepara_imq_mappa.py (+59). Scritti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 16_prepara_imq_mappa.py (+32).

#### `data/processed/accessibilita_parziale`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `piedi_000005.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000010.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000015.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000020.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000025.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000030.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000035.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000040.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000045.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000050.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000055.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000060.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000065.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000070.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000075.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000080.json` | 0,1 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `piedi_000084.json` | 0,0 | 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |

#### `data/processed/accessibilita_parziale_test`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `fase_x_000001.json` | 0,0 | — | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto |
| `fase_x_000002.json` | 0,0 | — | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto |
| `fase_x_000003.json` | 0,0 | — | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto |

#### `data/processed/catalogo`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `catalogo.json` | 0,0 | 04_genera_mappa.py, 11_prepara_catalogo.py | 11_prepara_catalogo.py | git | nome |
| `commercio.json` | 2,8 | 11_prepara_catalogo.py, 18_accessibilita.py, 20_servizi_osm.py, 49_v3_punti_domanda.py (+3) | — | git | via nome senza estensione |
| `istruzione.json` | 0,1 | 87_popolarita_zone.py | — | git | nome |
| `reti.json` | 1,2 | — | 11_prepara_catalogo.py | Release | sopra 5 MB, letto solo dagli script; nome |
| `salute.json` | 0,1 | 04_genera_mappa.py, 11_prepara_catalogo.py, 15_prepara_zone_imq.py, 18_accessibilita.py (+10) | 04_genera_mappa.py, 11_prepara_catalogo.py | git | via cartella |
| `servizi.json` | 0,0 | 95_case_fragilita_servizi.py, prova_scheda_case.py, schede_risultati.py | 95_case_fragilita_servizi.py, prova_scheda_case.py | git | nome |
| `sicurezza_sport.json` | 0,1 | 11_prepara_catalogo.py, 49_v3_punti_domanda.py, 87_popolarita_zone.py, mappa_template.html (+1) | — | git | via nome senza estensione |

#### `data/processed/imq`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `comuni.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py, 15_prepara_zone_imq.py | — | git | nome |
| `interviste.csv` | 4,0 | 13_esporta_imq.ps1, 14_prepara_imq.py | — | git | nome |
| `mezzi.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py, 16_prepara_imq_mappa.py | — | git | nome |
| `scopi.csv` | 0,0 | 13_esporta_imq.ps1 | — | git | nome |
| `spostamenti.csv` | 7,1 | 13_esporta_imq.ps1, 14_prepara_imq.py, 16_prepara_imq_mappa.py, 40_domanda_imq.py (+5) | — | Release | sopra 5 MB, letto solo dagli script; nome |
| `zone_camp.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py | — | git | nome |

#### `data/processed/rapporto_gtt`

105 file, 5,4 MB (git: 104, Release: 1). Letti da: 04_genera_mappa.py, 16_prepara_imq_mappa.py, 23_vulnerabilita_incrocio.py, 29_risultato2_metro_notte.py, 30_rapporto_estrai.py, 31_rapporto_fatti.py (+5). Scritti da: 04_genera_mappa.py, 16_prepara_imq_mappa.py, 23_vulnerabilita_incrocio.py, 29_risultato2_metro_notte.py, 30_rapporto_estrai.py, 31_rapporto_fatti.py (+1).

#### `data/processed/risultato6_v2`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `auto_passaggio.json` | 0,3 | 81_auto_di_passaggio.py, 83_fermate_importanti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py | 81_auto_di_passaggio.py | git | nome |
| `auto_passaggio.npz` | 0,2 | 81_auto_di_passaggio.py, 88_confronto_auto_sensori.py | 81_auto_di_passaggio.py | git | nome |
| `confronto_sensori.json` | 0,0 | schede_risultati.py | 88_confronto_auto_sensori.py | git | nome |
| `eventi.json` | 0,0 | 04_genera_mappa.py, 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py (+15) | 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py, 72_nodi_tp.py (+1) | git | via cartella |
| `fermate_importanti.json` | 0,1 | 83_fermate_importanti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py | 83_fermate_importanti.py | git | nome |
| `istat2011_proporzioni.json` | 0,0 | 73_segnali_criticita.py | — | git | via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | git | nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | git | nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | git | nome |
| `parcheggi_funzione.json` | 1,2 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | git | nome |
| `riempimento.json` | 0,0 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | 71_parcheggi_riempimento.py | git | nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | git | nome |
| `segnali.json` | 2,1 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | git | nome |
| `istat2011_proporzioni.json` | 0,0 | 04_genera_mappa.py, 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py (+15) | 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py, 72_nodi_tp.py (+1) | git | via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | git | nome |
| `mappa_r6.json` | 0,3 | 04_genera_mappa.py, 79_dati_mappa_r6.py, prova_pagine.py, schede_risultati.py | 79_dati_mappa_r6.py | git | nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | git | nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | git | nome |
| `parcheggi_adatti.json` | 0,8 | 82_parcheggi_adatti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py, 87_popolarita_zone.py | 82_parcheggi_adatti.py | git | nome |
| `parcheggi_funzione.json` | 1,8 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | git | nome |
| `porte.json` | 0,3 | 41_zone_punti.py, 49_v3_punti_domanda.py, 50_v3_assegnazione.py, 62_v4_modello.py (+5) | 41_zone_punti.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | git | nome |
| `riempimento.json` | 0,1 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | 71_parcheggi_riempimento.py | git | nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | git | nome |
| `segnali.json` | 2,7 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | git | nome |

#### `data/processed/traffico_c`

37 file, 62,4 MB (git: 32, Release: 4, riassunto: 1). Letti da: 39_fattibilita_rete.py, 40_domanda_imq.py, 41_zone_punti.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+25). Scritti da: 39_fattibilita_rete.py, 40_domanda_imq.py, 41_zone_punti.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+11).

#### `data/processed/traffico_d`

40 file, 166,1 MB (git: 28, Release: 12). Letti da: 33_flusso_sensori.py, 36_abbinamento_posizione.py, 37_traffico_AB.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+20). Scritti da: 33_flusso_sensori.py, 42_instradamento.py, 50_v3_assegnazione.py, 56_build_rete_lanes.py, 57_assi_tratte.py, 58_corsie.py (+9).

#### `data/raw`

45 file, 38,9 MB (Release: 45). Letti da: 11_prepara_catalogo.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 18_accessibilita.py, 21_risultato1_vuoti.py, 25_risultato6_interscambio.py (+11). Scritti da: 11_prepara_catalogo.py, 25_risultato6_interscambio.py, 69_parcheggi_inventario.py.

#### `data/raw/IMQ2022_opendata_web`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_opendata_web.accdb` | 59,9 | 13_esporta_imq.ps1 | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); nome |
| `IMQ2022_opendata_web_metodologia.txt` | 0,0 | 13_esporta_imq.ps1 | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); via cartella |

#### `data/raw/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.csv` | 0,1 | — | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md) |

#### `data/raw/ex_quartieri`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `ex_quartieri.dbf` | 0,0 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); nome |
| `ex_quartieri.lyr` | 0,0 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); via cartella |
| `ex_quartieri.prj` | 0,0 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); via cartella |
| `ex_quartieri.qml` | 0,0 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); via cartella |
| `ex_quartieri.shp` | 0,1 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); nome |
| `ex_quartieri.shx` | 0,0 | 15_prepara_zone_imq.py | — | Release | dato grezzo (controllare la licenza in docs/FONTI_DATI.md); via cartella |

#### `data/raw/istat`

139 file, 557,3 MB (Release: 139). Letti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 16_prepara_imq_mappa.py (+22). Scritti da: 04_genera_mappa.py.

#### `data/raw/omi_2025_2`

314 file, 10,9 MB (Release: 314). Letti da: 08_prepara_omi.py. Scritti da: —.

#### `data/ref`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `eventi_luoghi.json` | 0,0 | — | — | fuori | nessuno script e nessuna pagina lo cita: avanzo? |
| `parcheggi_osservazioni.json` | 0,0 | 80_porte_interscambio.py, 84_risultato6_parcheggi.py | — | git | nome |

#### `data/scenari`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `gtt_gtfs_notte15.zip` | 8,9 | 28_scenario_metro_notte.py | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |
| `gtt_gtfs_notte30.zip` | 8,9 | 28_scenario_metro_notte.py | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |
| `scenario_semplice_4.json` | 0,0 | 28_scenario_metro_notte.py, 29_risultato2_metro_notte.py, 31_rapporto_fatti.py, 73_segnali_criticita.py (+4) | — | git | via cartella |

<!-- INVENTARIO:FINE -->

## Decisioni di Leo

(da compilare: fonte per fonte, git / Release / fonte; piano 2, passo 3)
