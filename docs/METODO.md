# Metodo: dati, area, accessibilità, etichette e colori

Una pagina che vale per tutti i risultati. Le fonti con indirizzi e licenze sono in `docs/FONTI_DATI.md`; ogni
risultato ha il suo documento (`docs/R1_servizi.md`, `R2_metro_notte.md`, `R4_puntualita.md`, `R6_parcheggi.md`,
`R8_traffico.md`).

## Dati e area

- **Area:** Torino (848.748 residenti) più la cintura e la Città metropolitana (69 comuni, 1.557.493 abitanti,
  8.317 sezioni di censimento 2021). Torino e cintura non sono sempre confrontabili: dentro Torino i servizi vengono dal
  catalogo comunale, fuori da OpenStreetMap (più povero). Tabelle e mappe le tengono separate.
- **Orari:** GTFS GTT (215 linee, 7.045 fermate, versione 20261002, valido fino al 31/01/2027) in `data/raw/`.
- **Raccolta dal vivo** su un Raspberry Pi: posizioni dei mezzi GTT, ritardi (dal 10/10), traffico 5T, parcheggi 5T e
  ZTL (dal 14/10). La copia `data/storico_backup.sqlite` si aggiorna ogni giorno con `scripts\RACCOLTA_GIORNALIERA.bat`.
  Gli script leggono lo storico in sola lettura (`file:...?mode=ro`); `data/raw/` non si modifica.
- **Spostamenti:** indagine IMQ 2022 (101 zone MTM della Città metropolitana): ora × modo × scopo × origine/destinazione.
- **Ora locale:** tutte le conversioni UTC → ora italiana (ora legale: ultima domenica di marzo e di ottobre) passano da
  `scripts/comuni.py`, controllate su 35.040 istanti del 2026-2027.

## Etichette dei dati

Ogni numero porta il suo tag: **[MISURATO]** (raccolta sul campo), **[PROGRAMMATO]** (orario ufficiale), **[STIMATO]**
(modello), **[CENSIMENTO]**, **[DATI SCARSI]**. Gli scenari di simulazione portano l'avviso: «SIMULAZIONE SU ORARIO
PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale.» Niente dati personali; la vulnerabilità
si mostra solo con l'indice dedicato, mai per nazionalità.

## Motore di accessibilità (`scripts/18_accessibilita.py`)

- Motore R5 (Java) su rete stradale OpenStreetMap (`data/otp/rete/torino_cintura.osm.pbf`, tagliata da `17_taglia_osm.py`)
  e GTFS GTT. Per ogni sezione calcola quante destinazioni di ogni gruppo (scuole, salute, negozi e attività, fermate,
  verde) si raggiungono **a piedi in 15 minuti (80 m/min = 4,8 km/h)** e **col mezzo pubblico in 45 minuti**, per 24
  fasce orarie di un feriale di riferimento.
- Destinazioni vicine (celle di circa 50 m) accorpate con un peso. Servizi: catalogo comunale a Torino, OpenStreetMap
  fuori (`20_servizi_osm.py`).
- Il giro completo è lungo (ore) e salva a tappe in `data/processed/accessibilita_parziale/`; si rifà con
  `scripts\ACCESSIBILITA_24ORE.bat` solo se cambia il GTFS. **La firma dei parziali non contiene il percorso del GTFS:
  tra due lanci con GTFS diversi bisogna svuotare la cartella dei parziali** (il `.bat` del Risultato 2 lo fa).
- Uscite: `data/processed/accessibilita.json`, `docs/rapporti/RAPPORTO_ACCESSIBILITA.txt` (Torino e cintura sempre
  separate). Lo usano i Risultati 1, 2 e 6 e la mappa. Orario programmato: ottimista per definizione; di notte nessuna
  sezione è mai a zero (bus notturni), quindi si guarda il miglioramento, non la soglia zero.

## Standard tecnici

- **Prova delle pagine:** `python scripts\prova_pagine.py --senza-screenshot` (errori a runtime su mappa e scheda).
  `node --check` trova solo errori di sintassi: colori, legende e dati non disegnati si controllano aprendo la pagina.
- **Fermate e strade:** mai abbinare per nome, solo per coordinate. Un corso che cambia nome o comune è un solo asse;
  l'unità del traffico è la tratta d'asse.
- **Mappa:** un campo nuovo in `D.sezioni[i]` va aggiunto anche alla proiezione `sez` di `scripts/mappa_template.html`;
  chi cambia l'ora (`#ora`) richiama `aggiornaLegenda()`. Numeri in italiano (virgola decimale).
- **Controlli negli script:** si fermano solo per errori di struttura (file mancante, somme che non tornano, valori
  negativi); un numero diverso da quello atteso è un AVVISO. Funzioni comuni (distanze, ora legale, percentili, zona
  centrale Q001-Q009) in `scripts/comuni.py`. Ogni risultato ha una verifica su fatti noti.
- **Script 24:** corridoio = stesso nome + tratti collegati o entro circa 100-200 m; togliere «(TO)» dai nomi 5T.
- **Python:** quello del PATH (3.14), non Anaconda (il suo modulo `json` è rotto).

## Colori

Uguali in mappa e schede: gradiente «bene/male» = **verde → rosso**; quantità neutre (abitanti, spostamenti,
pendolari, prezzi) = **blu → arancione smorzati**; categorie = un colore per gruppo. Le legende scrivono sempre i
numeri (daltonismo).
