# Esito — Risultato 6 v2: eventi e dati per mappa e scheda

Piano eseguito: `docs/PIANO_RISULTATO6_EVENTI_DATI.md`.
Inizio lavori: **19/10/2026, ore 01:21**. Fine lavori: **19/10/2026, ore 01:33**. Ramo git: `prova`. **Nessun commit.**
Python del PATH (3.14). Nessuna libreria installata. Database e `data/raw` in sola lettura.

## Passi

- **PASSO E0: OK** — Ramo `prova`; tutti i file di input presenti. `scenari.S2.critici` = 378.
  `parcheggi_funzione.json`: 3.431 parcheggi con classi `interscambio_di_fatto` 0, `solo_sulla_carta` 4,
  `potenziale` 758 (come atteso).
- **PASSO E1: PARZIALE (3 luoghi su 4)** — trovati in OSM e controllati: Stadio Olimpico Grande Torino
  (way 652725229, 28 m dal punto atteso), Inalpi Arena (way 41753512, 170 m), Oval Lingotto
  (way 88289207, 472 m). **Allianz Stadium: NON TROVATO** (vedi Anomalie).
- **PASSO E2: OK** (per i 3 luoghi con coordinate).
- **PASSO E3: OK** — tutti i 4 controlli di copertura a 200 m tornano.
- **PASSO E4: OK** (tranne il punto 4.2 su Allianz, impossibile).
- **PASSO E5: questo documento.**

## Numeri chiave

### Luoghi di evento (da `data/processed/risultato6_v2/eventi.json`)

| Luogo | Capienza | Auto stimate [STIMATO] | Posti 500 m | Posti 1.000 m | Mancano | Fermate 500 m | Corse/ora sera fer/sab/dom [PROGRAMMATO] |
|---|---|---|---|---|---|---|---|
| Stadio Olimpico Grande Torino | 28.177 | 5.635 | 887 | 2.389 | 3.246 | 14 | 82,2 / 63,7 / 55,7 |
| Inalpi Arena | 13.000 | 2.600 | 887 | 2.593 | 7 | 16 | 90,0 / 73,0 / 62,8 |
| Oval Lingotto | 13.000 | 2.600 | 456 | 7.129 | 0 | 7 | 109,2 / 105,7 / 81,5 |
| **Allianz Stadium** | 41.507 | 8.301 (atteso) | — | — | — | — | — |

- Auto = capienza × 0,5 ÷ 2,5. Controllo Allianz: 41.507 × 0,5 ÷ 2,5 = 8.301 (il calcolo è nel codice,
  ma il luogo non entra nei dati perché manca la coordinata).
- Nessun valore negativo; `posti 500 m ≤ posti 1.000 m` in tutti i luoghi.
- Stadio Olimpico e Inalpi Arena sono a ~160 m l'uno dall'altro: condividono parte dei parcheggi vicini
  (per questo hanno gli stessi 887 posti entro 500 m).

### File per mappa e scheda (`data/processed/risultato6_v2/mappa_r6.json`)

- Dimensione: **541.186 byte (529 KB)**, sotto il limite di 1,5 MB. `punti_a_favore` **non** serviva
  toglierli.
- Contenuto: `scenario` S2 (378 critici, soglia 63,97, universo 4.425); `luoghi_critici` 378;
  `parcheggi` 813 (0 di fatto + 4 solo sulla carta + 758 potenziali + garage 5T); `ufficiali` 5;
  `zona_centrale` 9 zone (Q001-Q009); `eventi` 3; `riepilogo`.
- Controlli copertura a 200 m (attesi fra parentesi): `coperto_f200` 140 (140), `coperto_u200` 11 (11),
  `coperto_p200` 147 (147), `coperto_f200 oppure solo_sulla_carta` 144 (144).
- Parcheggi per classe: di fatto 0; solo sulla carta 4 (1.716 posti); potenziale 758 (56.566 posti);
  non interscambio 2.669 (159.597 posti).
- Firme del riempimento [DATI SCARSI]: pendolare 19, destinazione 7, misto 6, nessun dato 4,
  dato bloccato 3, residenziale 2. Giorni feriali validi: **15/10 e 16/10/2026** (2 su 4).
- Zone con più critici scoperti: C009 Moncalieri 36, Q009 Nizza Millefonti 33, Q003 Crocetta 23,
  Q023 Mirafiori Sud 22, Q005 Cenisia 18.
- I 4 "solo sulla carta": CAIO MARIO (dato bloccato), SOFIA (residenziale), STURA (misto),
  VENCHI UNICA (dato bloccato).
- Fuori universo: 23 luoghi senza zona IMQ; 639 luoghi (fermate GTT) esclusi perché fuori Città
  metropolitana.

## Anomalie e differenze dagli attesi

1. **Allianz Stadium non trovato (ostacolo principale).** Nell'estratto OpenStreetMap usato
   (`data/otp/rete/torino_cintura.osm.pbf`) **nessun oggetto ha un nome che contenga "Allianz Stadium"**.
   Verificato in modo indipendente: cercando "allianz"/"juventus" in *qualsiasi* tag (nome, alt_name,
   wikipedia, brand…) si trovano solo negozi e la fermata tram "Allianz Stadium Capolinea"
   (node 1427044890, 45,11164/7,63877, ~250 m dal punto atteso). Lo stadio **esiste come geometria ma
   senza nome**: la via chiusa più grande nella zona attesa è way 119509840 (~69.000 m², 53 m dal punto
   atteso), senza tag `name`.
   Il piano dice: *"Se non trovi un luogo: FERMO (non inventare coordinate)"*. **Non ho inventato
   coordinate.** Applicando la regola di lavoro del progetto ("se un passo è impossibile, salta quel
   passo, continua con gli altri e scrivilo nel resoconto") ho proseguito con gli altri 3 luoghi. Quindi
   **Allianz manca da `eventi.json` e da `mappa_r6.json`**, e il punto 4.2 di E4 (conteggi Allianz con
   pandas) non è stato eseguito. Serve una decisione di Leo/Claude: o dare un nome all'oggetto OSM, o
   autorizzare l'uso della way 119509840.
2. Nessun'altra differenza dagli attesi: tutti i controlli numerici del piano tornano.
3. Nota: `scenari.json` ha 25 voci in `piu_scoperti.S2`; ne ho usate le prime 10 come chiede il piano.

## Decisioni prese dove il piano lasciava una scelta

- **Allianz:** non inventare coordinate; continuare con gli altri 3 luoghi (vedi Anomalia 1).
- **E4.1:** i "5 luoghi a caso" scelti con `random.seed(20261019)` e `random.sample`; il "parcheggio più
  vicino" è quello dell'insieme **F** (di fatto + potenziali), lo stesso campo `parcheggio_f` del file.
- **`posti_origine`:** il piano prevede "dichiarati" o "stimati"; quando il parcheggio non ha né posti
  dichiarati né stimati ho scritto **"nessuno"** (24 parcheggi di 813).
- **`zona_centrale`:** struttura `{zone_centrali: [...], poligoni: [{cod, denom, anelli}]}` con i contorni
  semplificati con `shapely.simplify(0.0002)` e arrotondati a 5 decimali (ordine `[lat, lon]`).
- **Solo sulla carta:** i 4 parcheggi si abbinano al riempimento tramite `id_5t` preso da `parcheggi.json`
  (`parcheggi_funzione.json` non ha quel campo): senza questa correzione le firme restavano vuote.

## Verifiche indipendenti (PASSO E4)

- **E4.1 OK** — distanza luogo critico → parcheggio più vicino per 5 luoghi a caso, con `cKDTree` su
  coordinate proiettate in metri (x = lon·111.000·cos45,07°, y = lat·111.000): stesso parcheggio e
  differenza di distanza **≤ 2,61 m** (< 3 m) dal file.
- **E4.2 NON ESEGUITO** — richiedeva Allianz, che manca.
- **E4.3 OK** — coperti U/F/P/F+S a 200 m rifatti con numpy in un modo diverso (matrice di distanze
  vettoriale): **11 / 140 / 147 / 144**, come atteso.
- **E4.4 OK** — `json.load` di `mappa_r6.json` senza errori; dimensione 541.186 byte < 1,5 MB.
- **E4.5 OK** — `git status`: nessun commit (ultimo commit 7387285, precedente). Gli unici file esistenti
  modificati sono `MEMORIA_PROGETTO.md` e `docs/PIANO_RISULTATO6_V2_GIRO2.md`: **erano già modificati
  prima di iniziare** (presenti nel primo `git status`) e **non li ho toccati**.

## File creati

Nuovi (nessun file esistente modificato):

- `scripts/78_eventi_parcheggi.py`
- `scripts/79_dati_mappa_r6.py`
- `data/processed/risultato6_v2/eventi.json`
- `data/processed/risultato6_v2/mappa_r6.json` (in `data/`, non tracciato da git)
- `docs/RAPPORTO_R6V2_EVENTI.txt`
- `docs/RAPPORTO_R6V2_MAPPA_DATI.txt`
- `docs/ESITO_RISULTATO6_EVENTI_DATI.md` (questo file)

Non toccati: memoria, mappa (`mappa_template.html`, `04_genera_mappa.py`), schede (`simulazione.html`).

## Durate

Lavoro quasi tutto automatico (OpenStreetMap e GTFS): circa 15 minuti in tutto; ogni esecuzione dello
script 78 (lettura GTFS) ~1 minuto, lo script 79 pochi secondi.

## Cosa rimane da fare

1. Decidere la coordinata dell'Allianz Stadium (nome in OSM oppure uso della way 119509840) e rilanciare
   `78` + `79` per aggiungerlo a `eventi.json` e `mappa_r6.json`.
2. Scrivere il codice della mappa (nuovo tema) e la scheda in `simulazione.html`: lo fa Claude.
3. Aggiornare la memoria del progetto: **non l'ho fatto io** perché il piano lo vieta esplicitamente
   (lo fa Claude a fine giro).
