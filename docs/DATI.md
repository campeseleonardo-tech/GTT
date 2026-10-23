# Dati del progetto

Dove deve stare ogni file di `data/`: in git, nella Release di GitHub, come riassunto o fuori. La parte fra i segnaposto la riscrive `scripts/96_inventario_dati.py`; sotto, nella sezione «Decisioni di Leo», si scrivono le decisioni (non viene toccata).

<!-- INVENTARIO:INIZIO -->

*Inventario scritto da `scripts/96_inventario_dati.py` il 23/10/2026 sulla cartella `data/`. Le proposte sono automatiche (regole in testa allo script): decide Leo, fonte per fonte (piano 2, passo 3).*

### Totali per posto

| Posto | File | Peso (MB) | Cosa vuol dire |
|---|---|---|---|
| git | 259 | 137,2 | dentro il repository |
| Release | 220 | 872,4 | zip nella Release di GitHub |
| riassunto | 2 | 2.712,1 | dello storico si tengono solo i riassunti (script 97) |
| fonte | 336 | 147,7 | non si pubblica: si riscarica dalla fonte (IMQ, OMI) |
| fuori | 432 | 320,9 | nessuno lo cita: non si pubblica |
| **tutto** | 1249 | 4.190,4 | |

Avvisi: file in «git» sopra 50 MB: 0.

### Per cartella

| Cartella | File | Peso (MB) | git | Release | riassunto | fonte | fuori |
|---|---|---|---|---|---|---|---|
| `data/(radice di data)` | 33 | 2.813,7 | 4 | 2 | 1 | 0 | 26 |
| `data/IMQ2013-22_zone_camp_TO` | 6 | 0,1 | 0 | 0 | 0 | 6 | 0 |
| `data/IMQ2022_opendata_web` | 1 | 59,9 | 0 | 0 | 0 | 1 | 0 |
| `data/IMQ2022_zone_camp_noTO` | 7 | 5,8 | 0 | 0 | 0 | 7 | 0 |
| `data/backup` | 2 | 22,6 | 0 | 0 | 0 | 0 | 2 |
| `data/backup/risultato6_v2_prima_correzioni` | 19 | 18,1 | 0 | 0 | 0 | 0 | 19 |
| `data/catalogo` | 6 | 4,4 | 6 | 0 | 0 | 0 | 0 |
| `data/otp/jdk-25.0.4.1+1-jre` | 320 | 179,1 | 0 | 0 | 0 | 0 | 320 |
| `data/otp/rete` | 2 | 32,4 | 0 | 2 | 0 | 0 | 0 |
| `data/processed` | 66 | 80,4 | 48 | 5 | 0 | 0 | 13 |
| `data/processed/accessibilita_parziale` | 48 | 1,8 | 0 | 0 | 0 | 0 | 48 |
| `data/processed/accessibilita_parziale_test` | 3 | 0,0 | 0 | 0 | 0 | 0 | 3 |
| `data/processed/catalogo` | 7 | 4,4 | 6 | 1 | 0 | 0 | 0 |
| `data/processed/imq` | 6 | 11,1 | 0 | 0 | 0 | 6 | 0 |
| `data/processed/rapporto_gtt` | 105 | 5,4 | 104 | 1 | 0 | 0 | 0 |
| `data/processed/risultato6_v2` | 24 | 19,6 | 24 | 0 | 0 | 0 | 0 |
| `data/processed/traffico_c` | 37 | 66,9 | 32 | 4 | 1 | 0 | 0 |
| `data/processed/traffico_d` | 40 | 166,2 | 28 | 12 | 0 | 0 | 0 |
| `data/raw` | 45 | 38,9 | 0 | 45 | 0 | 0 | 0 |
| `data/raw/IMQ2022_opendata_web` | 2 | 59,9 | 0 | 0 | 0 | 2 | 0 |
| `data/raw/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024` | 1 | 0,1 | 0 | 1 | 0 | 0 | 0 |
| `data/raw/ex_quartieri` | 6 | 0,1 | 0 | 6 | 0 | 0 | 0 |
| `data/raw/istat` | 139 | 557,3 | 0 | 139 | 0 | 0 | 0 |
| `data/raw/omi_2025_2` | 314 | 10,9 | 0 | 0 | 0 | 314 | 0 |
| `data/ref` | 2 | 0,0 | 1 | 0 | 0 | 0 | 1 |
| `data/scenari` | 3 | 17,8 | 1 | 2 | 0 | 0 | 0 |
| `data/storico_riassunti` | 5 | 13,5 | 5 | 0 | 0 | 0 | 0 |

### Per file

Le cartelle con più di 30 file sono in una riga sola (elenco completo: rilanciare lo script e guardare `--data`).

#### `data/(radice di data)`

33 file, 2.813,7 MB (git: 4, Release: 2, riassunto: 1, fuori: 26). Letti da: 04_genera_mappa.py, 06_dati_live.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py, 31_rapporto_fatti.py (+23). Scritti da: 06_dati_live.py, 30_rapporto_estrai.py, RACCOLTA_GIORNALIERA.bat, supervisore.py.

#### `data/IMQ2013-22_zone_camp_TO`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2013-22_zone_camp_TO.cpg` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2013-22_zone_camp_TO.dbf` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2013-22_zone_camp_TO.prj` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2013-22_zone_camp_TO.qmd` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2013-22_zone_camp_TO.shp` | 0,1 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2013-22_zone_camp_TO.shx` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |

#### `data/IMQ2022_opendata_web`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_opendata_web.accdb` | 59,9 | 13_esporta_imq.ps1 | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |

#### `data/IMQ2022_zone_camp_noTO`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_zone_camp_noTO.cpg` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.dbf` | 0,2 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.prj` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.qix` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.qmd` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.shp` | 5,5 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |
| `IMQ2022_zone_camp_noTO.shx` | 0,0 | — | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo) |

#### `data/backup`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `mappa_torino_prima_correzioni.html` | 22,6 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+12) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `schede_risultati_prima_correzioni.js` | 0,1 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+12) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |

#### `data/backup/risultato6_v2_prima_correzioni`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `eventi.json` | 0,0 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+12) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `istat2011_proporzioni.json` | 0,0 | 73_segnali_criticita.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi_funzione.json` | 1,2 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `riempimento.json` | 0,0 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py (+1) | 71_parcheggi_riempimento.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `segnali.json` | 2,1 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `istat2011_proporzioni.json` | 0,0 | 04_genera_mappa.py, 24_importanza_vie.py, 26_velocita_5t.py, 27_risultato4_regolarita.py (+12) | FETCH_LEOPI_E_VELOCITA_5T.bat, RACCOLTA_GIORNALIERA.bat | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `mappa_r6.json` | 0,3 | 04_genera_mappa.py, 79_dati_mappa_r6.py, prova_pagine.py, schede_risultati.py | 79_dati_mappa_r6.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `parcheggi_funzione.json` | 1,8 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `porte.json` | 0,3 | 41_zone_punti.py, 49_v3_punti_domanda.py, 50_v3_assegnazione.py, 62_v4_modello.py (+5) | 41_zone_punti.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `riempimento.json` | 0,1 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py (+1) | 71_parcheggi_riempimento.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |
| `segnali.json` | 2,7 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | fuori | strumento (Java), copia di sicurezza, prova o cache: non e' un dato del progetto; nome |

#### `data/catalogo`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `commercio.js` | 2,8 | 11_prepara_catalogo.py, 18_accessibilita.py, 20_servizi_osm.py, 49_v3_punti_domanda.py (+3) | — | git | la mappa lo carica quando si apre «Luoghi della città»; via nome senza estensione |
| `istruzione.js` | 0,1 | 87_popolarita_zone.py | — | git | la mappa lo carica quando si apre «Luoghi della città»; nome |
| `reti.js` | 1,2 | — | 11_prepara_catalogo.py | git | la mappa lo carica quando si apre «Luoghi della città»; nome |
| `salute.js` | 0,1 | 04_genera_mappa.py, 11_prepara_catalogo.py, 15_prepara_zone_imq.py, 18_accessibilita.py (+10) | 04_genera_mappa.py, 11_prepara_catalogo.py | git | la mappa lo carica quando si apre «Luoghi della città»; via cartella |
| `servizi.js` | 0,0 | 95_case_fragilita_servizi.py, prova_scheda_case.py, schede_risultati.py | 95_case_fragilita_servizi.py, prova_scheda_case.py | git | la mappa lo carica quando si apre «Luoghi della città»; nome |
| `sicurezza_sport.js` | 0,1 | 11_prepara_catalogo.py, 49_v3_punti_domanda.py, 87_popolarita_zone.py, mappa_template.html (+1) | — | git | la mappa lo carica quando si apre «Luoghi della città»; via nome senza estensione |

#### `data/otp/jdk-25.0.4.1+1-jre`

320 file, 179,1 MB (fuori: 320). Letti da: 01_scarica_dati.py, 04_genera_mappa.py, 05_prepara_sezioni.py, 06_dati_live.py, 100_ore_del_giorno.py, 11_prepara_catalogo.py (+67). Scritti da: 04_genera_mappa.py, 88_confronto_auto_sensori.py, 98_prepara_release.py, TRAFFICO_RILANCIA_SENSORI.bat.

#### `data/otp/rete`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `gtt_gtfs_20261003_224530.zip` | 11,7 | 18_accessibilita.py, 21_risultato1_vuoti.py, 25_risultato6_interscambio.py, 27_risultato4_regolarita.py (+7) | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |
| `torino_cintura.osm.pbf` | 20,6 | 17_taglia_osm.py, 18_accessibilita.py, 20_servizi_osm.py, 24_importanza_vie.py (+11) | — | Release | archivio o documento grezzo (zip, pdf, pbf...): non va in git; nome |

#### `data/processed`

66 file, 80,4 MB (git: 48, Release: 5, fuori: 13). Letti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 100_ore_del_giorno.py, 14_prepara_imq.py, 15_prepara_zone_imq.py (+63). Scritti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 16_prepara_imq_mappa.py (+32).

#### `data/processed/accessibilita_parziale`

48 file, 1,8 MB (fuori: 48). Letti da: 18_accessibilita.py, ACCESSIBILITA_24ORE.bat, R1_PIEDI_5_10.bat, rifai_tutto.py. Scritti da: —.

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
| `comuni.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py, 15_prepara_zone_imq.py | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `interviste.csv` | 4,0 | 13_esporta_imq.ps1, 14_prepara_imq.py | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `mezzi.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py, 16_prepara_imq_mappa.py | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `scopi.csv` | 0,0 | 13_esporta_imq.ps1 | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `spostamenti.csv` | 7,1 | 13_esporta_imq.ps1, 14_prepara_imq.py, 16_prepara_imq_mappa.py, 40_domanda_imq.py (+5) | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `zone_camp.csv` | 0,0 | 13_esporta_imq.ps1, 14_prepara_imq.py | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |

#### `data/processed/rapporto_gtt`

105 file, 5,4 MB (git: 104, Release: 1). Letti da: 04_genera_mappa.py, 16_prepara_imq_mappa.py, 23_vulnerabilita_incrocio.py, 29_risultato2_metro_notte.py, 30_rapporto_estrai.py, 31_rapporto_fatti.py (+7). Scritti da: 04_genera_mappa.py, 16_prepara_imq_mappa.py, 23_vulnerabilita_incrocio.py, 29_risultato2_metro_notte.py, 30_rapporto_estrai.py, 31_rapporto_fatti.py (+1).

#### `data/processed/risultato6_v2`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `auto_passaggio.json` | 0,3 | 81_auto_di_passaggio.py, 83_fermate_importanti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py | 81_auto_di_passaggio.py | git | nome |
| `auto_passaggio.npz` | 0,2 | 81_auto_di_passaggio.py, 88_confronto_auto_sensori.py | 81_auto_di_passaggio.py | git | nome |
| `confronto_sensori.json` | 0,0 | — | 88_confronto_auto_sensori.py | git | nome |
| `eventi.json` | 0,0 | 04_genera_mappa.py, 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py (+16) | 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py, 72_nodi_tp.py (+1) | git | via cartella |
| `fermate_importanti.json` | 0,1 | 83_fermate_importanti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py | 83_fermate_importanti.py | git | nome |
| `istat2011_proporzioni.json` | 0,0 | 73_segnali_criticita.py | — | git | via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | git | nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | git | nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | git | nome |
| `parcheggi_funzione.json` | 1,2 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | git | nome |
| `riempimento.json` | 0,0 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py (+1) | 71_parcheggi_riempimento.py | git | nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | git | nome |
| `segnali.json` | 2,1 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | git | nome |
| `istat2011_proporzioni.json` | 0,0 | 04_genera_mappa.py, 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py (+16) | 68_luoghi_fermate.py, 69_parcheggi_inventario.py, 71_parcheggi_riempimento.py, 72_nodi_tp.py (+1) | git | via cartella |
| `luoghi.json` | 1,1 | 68_luoghi_fermate.py, 72_nodi_tp.py, 73_segnali_criticita.py, 77_strade_comuni.py (+5) | 68_luoghi_fermate.py | git | nome |
| `mappa_r6.json` | 0,3 | 04_genera_mappa.py, 79_dati_mappa_r6.py, prova_pagine.py, schede_risultati.py | 79_dati_mappa_r6.py | git | nome |
| `nodi.json` | 1,6 | 72_nodi_tp.py, 73_segnali_criticita.py, 80_porte_interscambio.py, 83_fermate_importanti.py (+2) | 72_nodi_tp.py | git | nome |
| `parcheggi.json` | 1,9 | 69_parcheggi_inventario.py, 72_nodi_tp.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py (+4) | 69_parcheggi_inventario.py | git | nome |
| `parcheggi_adatti.json` | 0,8 | 82_parcheggi_adatti.py, 84_risultato6_parcheggi.py, 85_verifiche_correzioni.py, 87_popolarita_zone.py | 82_parcheggi_adatti.py | git | nome |
| `parcheggi_funzione.json` | 1,8 | 72_nodi_tp.py, 82_parcheggi_adatti.py | 72_nodi_tp.py | git | nome |
| `porte.json` | 0,3 | 41_zone_punti.py, 49_v3_punti_domanda.py, 50_v3_assegnazione.py, 62_v4_modello.py (+5) | 41_zone_punti.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py | git | nome |
| `riempimento.json` | 0,1 | 71_parcheggi_riempimento.py, 72_nodi_tp.py, 80_porte_interscambio.py, 84_risultato6_parcheggi.py (+1) | 71_parcheggi_riempimento.py | git | nome |
| `scenari.json` | 0,2 | 80_porte_interscambio.py, 83_fermate_importanti.py | — | git | nome |
| `segnali.json` | 2,7 | 73_segnali_criticita.py, 80_porte_interscambio.py, 81_auto_di_passaggio.py, 83_fermate_importanti.py (+1) | 73_segnali_criticita.py | git | nome |

#### `data/processed/traffico_c`

37 file, 66,9 MB (git: 32, Release: 4, riassunto: 1). Letti da: 39_fattibilita_rete.py, 40_domanda_imq.py, 41_zone_punti.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+26). Scritti da: 39_fattibilita_rete.py, 40_domanda_imq.py, 41_zone_punti.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+11).

#### `data/processed/traffico_d`

40 file, 166,2 MB (git: 28, Release: 12). Letti da: 33_flusso_sensori.py, 36_abbinamento_posizione.py, 37_traffico_AB.py, 42_instradamento.py, 43_segmenti_corridoi.py, 44_taratura_validazione.py (+19). Scritti da: 33_flusso_sensori.py, 42_instradamento.py, 50_v3_assegnazione.py, 56_build_rete_lanes.py, 57_assi_tratte.py, 58_corsie.py (+9).

#### `data/raw`

45 file, 38,9 MB (Release: 45). Letti da: 11_prepara_catalogo.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 18_accessibilita.py, 21_risultato1_vuoti.py, 25_risultato6_interscambio.py (+11). Scritti da: 11_prepara_catalogo.py, 25_risultato6_interscambio.py, 69_parcheggi_inventario.py.

#### `data/raw/IMQ2022_opendata_web`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `IMQ2022_opendata_web.accdb` | 59,9 | 13_esporta_imq.ps1 | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); nome |
| `IMQ2022_opendata_web_metodologia.txt` | 0,0 | 13_esporta_imq.ps1, scarica_dati.py | — | fonte | IMQ 2022 e OMI: licenza non chiara, non si pubblica; si riscarica dalla fonte (decisione di Leo); via cartella |

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

139 file, 557,3 MB (Release: 139). Letti da: 04_genera_mappa.py, 05_prepara_sezioni.py, 08_prepara_omi.py, 14_prepara_imq.py, 15_prepara_zone_imq.py, 16_prepara_imq_mappa.py (+24). Scritti da: 04_genera_mappa.py, costruisci_prove_stile.py.

#### `data/raw/omi_2025_2`

314 file, 10,9 MB (fonte: 314). Letti da: 08_prepara_omi.py, scarica_dati.py. Scritti da: —.

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

#### `data/storico_riassunti`

| File | MB | Legge | Scrive | Posto | Nota |
|---|---|---|---|---|---|
| `anagrafica.json` | 0,0 | 97_riassunti_storico.py, riassunti_storico.py | — | git | riassunti dello storico (script 97): vanno in git; nome |
| `ora_tipica.json` | 0,2 | 97_riassunti_storico.py, riassunti_storico.py | — | git | riassunti dello storico (script 97): vanno in git; nome |
| `parcheggi_2026-10.json.gz` | 0,0 | 26_velocita_5t.py, 27_risultato4_regolarita.py, 70_risultato9_attesa.py, 71_parcheggi_riempimento.py (+5) | — | git | riassunti dello storico (script 97): vanno in git; via cartella |
| `passaggi_2026-10.zip` | 13,0 | 26_velocita_5t.py, 27_risultato4_regolarita.py, 70_risultato9_attesa.py, 71_parcheggi_riempimento.py (+5) | — | git | riassunti dello storico (script 97): vanno in git; via cartella |
| `sensori5t_2026-10.json.gz` | 0,3 | 26_velocita_5t.py, 27_risultato4_regolarita.py, 70_risultato9_attesa.py, 71_parcheggi_riempimento.py (+5) | — | git | riassunti dello storico (script 97): vanno in git; via cartella |

<!-- INVENTARIO:FINE -->

## Decisioni di Leo

Prese il 22/10/2026, dopo l'inventario sui dati veri. Lo script 96 le applica da solo (posto «fonte» e «fuori»): le tabelle sopra si aggiornano al prossimo lancio.

| Cosa | Deciso | Perché / come si rifà |
|---|---|---|
| **IMQ 2022**: file originale (`.accdb`), spostamenti e interviste (`data/processed/imq/*.csv`), zone di campionamento | **fonte**: non entrano né in git né nella Release; si riscaricano dalla fonte | Licenza non indicata (© Agenzia, «per studio e ricerca»). Indirizzo: pagina «open data IMQ 2022» di MTM (in `docs/FONTI_DATI.md`); poi gli script 13-16 rifanno i file. Leo scrive all'Agenzia per chiedere il permesso |
| **OMI**: file grezzi (`data/raw/omi_2025_2/`) | **fonte**: non si pubblicano; si riscaricano a mano | Nessuna licenza esplicita, solo «citare la fonte». Procedura: servizio Forniture dati OMI, semestre 2025/2, provincia di Torino |
| **File del Pi** (`live.js`, `stat.js`, `agg_cache.json`, `replay_*.js`, `get_*.xml`) | **fuori** | Servivano alla vecchia mappa live; la mappa non usa più dati live |
| Java di OTP, `data/backup/`, cache e prove | **fuori** | Strumenti, copie e avanzi, non dati |
| ISTAT, OpenStreetMap (estratto), GTFS GTT e copie dei GTFS di scenario | **Release** | CC BY 4.0 / ODbL / CC BY: con citazione (OSM con ODbL). Leo controlla a mano la licenza della scheda GTFS statico |
| Dati delle pagine, risultati e riferimenti piccoli | **git** | come proposto dall'inventario |
| Storico SQLite | **riassunti** (script 97) | piano 2, passo 4 |

Ancora aperti: il PDF del rapporto di sostenibilità GTT 2025 (`rapporto_di_sostenibilita_2025.pdf`, 3 MB: oggi in Release, ma è un documento di GTT di cui la licenza non è stata controllata);
i numeri aggregati dell'IMQ dentro `mappa_torino.html` (restano con la citazione, da confermare con l'Agenzia); `IMQ2022_opendata_web.accdb` esiste due volte (`data/` e `data/raw/`, 60 MB l'una): se non serve la copia, cancellare a mano quella fuori da `raw`.
