# Piano per un agente — Risultato 6 v2: eventi e dati per mappa e scheda

Scritto da Claude il 19/10/2026 per un altro modello (agente). Fa parte delle Fasi B2 e C1 di `docs/PIANO_RISULTATO6_FINALE.md`.
Le decisioni di Leo sono **fisse**: scenario **S2**, zona centrale dei parcheggi Q001-Q009, 25 m² a posto, auto per evento = capienza × 50% ÷ 2,5.
Fai **un passo alla volta**. Ogni passo finisce con una riga nell'esito: `PASSO En: OK` oppure `PASSO En: FERMO – motivo`. Se un controllo
non torna: **fermati**, scrivi cosa hai visto, non inventare correzioni. **Non scrivere codice della mappa** (`mappa_template.html`, `04_genera_mappa.py`):
quello lo fa Claude dopo.

## 0. Regole

1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (`git branch --show-current`; se non è `prova`, FERMATI). **Nessun commit.**
2. Python del PATH (3.14), `python`. **Non Anaconda.** Librerie già installate: numpy, scipy, pandas, shapely, pyproj, osmium. Non installarne altre.
3. Database `data/storico_backup.sqlite` e `data/raw/` in **sola lettura**. Non scaricare niente da internet.
4. **Non modificare nessun file esistente.** Scrivi solo i file nuovi di questo piano: `scripts/78_eventi_parcheggi.py`, `scripts/79_dati_mappa_r6.py`,
   `data/processed/risultato6_v2/eventi.json`, `data/processed/risultato6_v2/mappa_r6.json`, `docs/RAPPORTO_R6V2_EVENTI.txt`, `docs/RAPPORTO_R6V2_MAPPA_DATI.txt`,
   `docs/ESITO_RISULTATO6_EVENTI_DATI.md`. Mai toccare memoria, schede, mappa, `simulazione.html`.
5. Ogni script nuovo ha in cima una docstring in italiano semplice (cosa fa, cosa legge, cosa scrive, come si lancia) e gli stessi accorgimenti dei vostri
   predecessori: `trova_radice()`, haversine in metri, ordine coordinate (nei file ZTL `[lon, lat]`, nelle zone IMQ `[lat, lon]`).
6. Etichette: [STIMATO] per le auto per evento e i posti stimati dalla superficie; [PROGRAMMATO] per le corse; [DATI SCARSI] per il riempimento (2 feriali validi).
7. Italiano semplice in rapporti ed esito, niente gergo. Inizio lavori: crea `docs/ESITO_RISULTATO6_EVENTI_DATI.md` con data e ora.

## 1. Cosa esiste (input, tutti già prodotti)

- `data/ref/eventi_luoghi.json`: 4 luoghi (`allianz`, `olimpico`, `inalpi`, `oval`) con `nome`, `capienza`, `osm_nome`, fonti; `parametri_auto` (0,5 e 2,5). **Senza coordinate.**
- `data/processed/risultato6_v2/`: `luoghi.json` (5.087 luoghi: `id_luogo, nome, lat, lon, stop_ids, zona_imq, in_centro, …`), `parcheggi.json` (lista, o chiave `parcheggi`:
  `id, nome, tipo, lat, lon, posti_dichiarati, posti_stimati, superficie_m2, a_pagamento, id_5t, …`), `parcheggi_funzione.json` (chiave `parcheggi`: `id, nome, tipo, lat, lon, zona_imq,
  zona_centrale, forza, punti_a_favore, uso, posti, a_pagamento, classe, motivo, su_asse_ingresso, dist_nodo_forte_m, tipo_nodo`), `riempimento.json` (chiave `parcheggi`: `id_5t, nome, profilo_feriale{ora:valore},
  profilo_weekend, firma, giorni_validi, fragile, N_notte_feriale, G_giorno_feriale`; più `anteprima`, `etichetta`), `segnali.json`, `nodi.json`, `scenari.json`
  (`scenari.S2.critici[]`: `id_luogo, punteggio, segnali{…}`; `scenari.S2.soglia`; `per_zona.S2{zona:{critici,coperti_f200}}`; `piu_scoperti.S2`), `istat2011_proporzioni.json`.
- `data/processed/imq_zone.json` (lista: `cod, denom, macro, prov`), `data/processed/imq_zone_geo.json` (poligoni zone; attenzione all'ordine `[lat, lon]`).
- `data/raw/gtt_gtfs_20261003_224530.zip` (GTFS), `data/otp/rete/torino_cintura.osm.pbf` (OpenStreetMap).
- Per le funzioni su GTFS e OSM guarda `scripts/72_nodi_tp.py` (`servizi_attivi`, `leggi_gtfs`, lettura OSM con `osmium`): riusale **copiandole** nel tuo script o caricandole con
  `importlib` (non modificare il 72).

## 2. Passi

### PASSO E0 — Controlli
1. Ramo `prova`. Esistono tutti i file della sezione 1 (altrimenti FERMO).
2. `scenari.json`: `scenari.S2.critici` ha **378** elementi (altrimenti FERMO). `parcheggi_funzione.json`: 3.431 parcheggi con classi `interscambio_di_fatto` 0,
   `solo_sulla_carta` 4, `potenziale` 758 (altrimenti FERMO e scrivi i valori trovati).

### PASSO E1 — Coordinate dei luoghi di evento (script `78_eventi_parcheggi.py`, prima parte)
1. Per ogni luogo di `eventi_luoghi.json` cerca in OSM (`osmium`, nodi e vie con `locations=True`) gli elementi il cui `name` contiene `osm_nome` (senza maiuscole/minuscole)
   **e** che hanno uno di questi tag: `leisure` in (stadium, sports_centre, sports_hall), `building` in (stadium, sports_hall, yes), `amenity` in (events_venue, exhibition_centre), `tourism=attraction`,
   `man_made=...`. Se più elementi: preferisci quello con area più grande (via chiusa) o con `leisure=stadium`.
2. Centro = media dei punti della via (o il nodo). Salva `lat`, `lon`, `id_osm`, `tipo_osm`.
3. **Controlli (se non tornano: FERMO e scrivi cosa hai trovato):** il luogo dev'essere entro i confini di Torino (lat 44,95-45,16; lon 7,55-7,76) e vicino a quanto atteso:
   Allianz ≈ (45,110; 7,641), Stadio Olimpico Grande Torino ≈ (45,042; 7,650), Inalpi Arena ≈ (45,043; 7,652), Oval ≈ (45,031; 7,663), ciascuno entro **1,5 km**.
   Se non trovi un luogo: FERMO (non inventare coordinate).

### PASSO E2 — Parcheggi, fermate e interscambi vicini (`78_eventi_parcheggi.py`, seconda parte)
Per ogni luogo di evento (distanze haversine in linea d'aria):
1. **Parcheggi vicini** in `parcheggi.json`, tipi `interscambio_ufficiale`, `garage_5t`, `park_ride_osm`, `osm_pubblico` (escludi `privato`, `clienti`, `lungo_strada`):
   a 500 m e a 1.000 m: numero, **posti** = `posti_dichiarati` se c'è, altrimenti `posti_stimati`, altrimenti 0; scrivi anche quanti parcheggi hanno posti **solo stimati** e quanti **non hanno posti**.
   Elenco dei 10 più grandi entro 1.000 m (nome, tipo, distanza, posti, dichiarato/stimato, tariffa).
2. **Fermate TP**: luoghi di `luoghi.json` entro 500 m (numero) e **corse all'ora** medie nelle ore 18-23 per tre giorni tipo del GTFS: feriale `20261012`, sabato `20261017`, domenica `20261018`
   (servizi attivi da `calendar.txt` + `calendar_dates.txt`; conta le partenze per `stop_times` di ogni corsa attiva, ore ≥ 24 modulo 24; somma sui luoghi entro 500 m e dividi per 6). [PROGRAMMATO]
3. **Parcheggi di interscambio vicini** (solo informazione): entro 3.000 m, dai parcheggi con classe `solo_sulla_carta` o `potenziale` con `forza` ≥ 2 e dai 5 ufficiali: elenco dei 10 più grandi
   per posti (nome, classe, distanza, posti, tariffa). Scrivi chiaro che sono vicini in linea d'aria, **non** un collegamento TP verificato.
4. **Auto stimate** = `capienza` × `quota_auto` ÷ `persone_per_auto` (parametri da `eventi_luoghi.json`, **non** cambiarli); `mancano` = max(0, auto stimate − posti entro 1.000 m). [STIMATO]
5. Scrivi `data/processed/risultato6_v2/eventi.json` (per luogo: tutti i campi sopra + `fonti` + `capienza_nota`) e `docs/RAPPORTO_R6V2_EVENTI.txt` (una tabella riassuntiva
   evento → auto stimate → posti 500 m / 1.000 m → mancano → fermate e corse serali, poi il dettaglio per luogo, poi i limiti: capienze da fonti web diverse, parametri auto ipotizzati,
   nessun dato sul parcheggio gratuito/abusivo, posti OSM stimati ±30%, linea d'aria).
6. **Controlli:** auto stimate Allianz = 41.507 × 0,5 ÷ 2,5 = **8.301** (±1); nessun valore negativo; i posti entro 500 m ≤ posti entro 1.000 m. Differenze dagli attesi: scrivile.

### PASSO E3 — Dati per la mappa e la scheda (script `79_dati_mappa_r6.py`)
Scopo: un unico file piccolo che la mappa e la scheda leggono. Scenario **S2**. Tutto da file già prodotti; nessun calcolo nuovo sui dati grezzi, tranne distanze e conteggi.
1. `scenario`: `{"id": "S2", "titolo": "integrato", "segnali": […], "soglia": …, "n_critici": 378, "universo": 4425}` (da `scenari.json`).
2. `luoghi_critici` (378): `id, nome, lat, lon, zona_imq, n_fermate, punteggio, segnali` (da S2) più:
   - `parcheggio_f` = il parcheggio più vicino fra classi `interscambio_di_fatto` + `potenziale`: `id`, `nome`, `dist_m` (o `null` se oltre 2.000 m);
   - `parcheggio_u` = il più vicino fra i 5 ufficiali: `id`, `nome`, `dist_m`;
   - `coperto_f200` = `parcheggio_f.dist_m` ≤ 200; `coperto_u200` analogo; `coperto_p200` per l'insieme **P** (tutti i parcheggi aperti ≥ 50 posti, come in `scenari.json.insiemi_parcheggi`);
   - **Controllo:** somma di `coperto_f200` = **140**, `coperto_u200` = **11**, `coperto_p200` = **147**, `coperto_f200 oppure classe solo_sulla_carta entro 200 m` = **144** (F+S). Se no: FERMO.
3. `parcheggi`: tutti i parcheggi di `parcheggi_funzione.json` con classe `interscambio_di_fatto`, `solo_sulla_carta`, `potenziale`, **più** tutti i `garage_5t` (anche `non_interscambio`).
   Per ognuno: `id, nome, tipo, classe, motivo, lat, lon, zona_imq, zona_centrale, posti, posti_origine` (`"dichiarati"` o `"stimati"`, da `parcheggi.json`), `a_pagamento`, `forza`, `punti_a_favore`,
   `su_asse_ingresso`, `firma` e `profilo_feriale` (24 valori 0-1, ore italiane 0-23; da `riempimento.json` tramite `id_5t`; `null` se non c'è), `fragile`. Arrotonda lat/lon a 5 decimali e il profilo a 2.
   **Dimensione**: il file finale deve stare sotto **1,5 MB**; se supera, togli prima `punti_a_favore` poi riduci i decimali. Scrivi la dimensione nel rapporto.
4. `ufficiali`: i 5 interscambi ufficiali con `raggio_m: 200`.
5. `zona_centrale`: i poligoni delle zone IMQ **Q001-Q009** (da `imq_zone_geo.json`, ordine `[lat, lon]`), semplificati con `shapely.simplify(0.0002)` e arrotondati a 5 decimali; più
   l'elenco `zone_centrali: ["Q001",…,"Q009"]`.
6. `eventi`: da `eventi.json`: `id, nome, tipo, lat, lon, capienza, auto_stimate, posti_500, posti_1000, mancano, fermate_500, corse_ora_sera_{feriale,sabato,domenica}`.
7. `riepilogo` (per la scheda, tutti numeri interi o decimali già calcolati, con la fonte nel nome):
   - luoghi critici, coperti U/F/P/F+S a 100/200/400 m (da `scenari.json`);
   - parcheggi per classe: numero e posti (da `parcheggi_funzione.json`), e **per motivo** (`zona_centrale`, `nessun_punto`, `punti_a_favore`, `dichiarato_non_usato`, `firma_non_pendolare`);
   - firme del riempimento: conteggio per firma; giorni feriali validi e date;
   - **zone con più luoghi critici scoperti** (S2, coperti F a 200 m): le 10 con più scoperti: `zona, nome` (da `imq_zone.json`, campo `denom`), `critici`, `coperti_f200`, `scoperti`;
   - i 10 `piu_scoperti` di S2 (nome, zona, punteggio, parcheggio più vicino e distanza);
   - i 4 parcheggi `solo_sulla_carta` con firma, occupazione di giorno e di notte (`G_giorno_feriale`, `N_notte_feriale`), posti, tariffa;
   - il numero di luoghi senza zona IMQ fuori dall'universo (23) e le fermate GTT escluse perché fuori Città metropolitana (639 luoghi).
8. Scrivi `data/processed/risultato6_v2/mappa_r6.json` (con `generato`, `fonti`, `etichette` dei dati) e `docs/RAPPORTO_R6V2_MAPPA_DATI.txt` (cosa contiene, quanti elementi per sezione, dimensione, controlli).

### PASSO E4 — Verifiche indipendenti
Rifai con un metodo diverso e scrivi nell'esito:
1. Distanza luogo critico → parcheggio più vicino per **5 luoghi a caso** (seme 20261019) con `cKDTree` su coordinate proiettate in metri (x = lon·111.000·cos(45,07°), y = lat·111.000) invece di haversine:
   stesso parcheggio, distanza entro 3 m.
2. Conteggio dei parcheggi e posti entro 500 m e 1.000 m dell'Allianz Stadium rifatto con pandas: uguale al rapporto.
3. Coperti U/F/P/F+S a 200 m rifatti con numpy in un modo diverso: 11 / 140 / 147 / 144.
4. `python -c "import json; json.load(open('data/processed/risultato6_v2/mappa_r6.json', encoding='utf-8'))"` senza errori; dimensione < 1,5 MB.
5. `git status`: nessun commit e **nessun file esistente modificato**; elenca i file nuovi.

### PASSO E5 — Esito
In `docs/ESITO_RISULTATO6_EVENTI_DATI.md`: stato di ogni passo; le decisioni prese da te dove il piano lasciava una scelta; numeri chiave (auto stimate, posti entro 500/1.000 m, mancano, fermate e corse serali
per ognuno dei 4 luoghi; elementi e dimensione di `mappa_r6.json`); anomalie e differenze dagli attesi; file creati; durate. **Non** modificare memoria, mappa, schede.

## 3. Cosa NON fare
- Non scrivere codice della mappa o della scheda. Non cambiare i parametri delle auto (50%, 2,5), la zona centrale (Q001-Q009), lo scenario (S2).
- Non abbinare per nome (salvo il nome OSM dei 4 luoghi di evento, controllato con le coordinate attese).
- Non aggiungere altri luoghi di evento oltre ai 4 del file (Leo: per ora no).
- Non scaricare niente da internet, non installare librerie, non fare commit.
