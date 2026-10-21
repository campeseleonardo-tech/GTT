# Mobilità a Torino — come si muove la città

Progetto personale di analisi dei dati (2026): chi va dove, dove mancano servizi, dove sono le criticità
del trasporto pubblico a Torino e nella Città metropolitana, e pochi scenari «cosa succede se».
Si parte da **`index.html`**. Due pagine: **`mappa_torino.html`** (mappa con i temi) e **`risultati.html`** (le schede dei
risultati: risposta, grafico, punti chiave, calcolo, limiti).

Ogni numero porta un'etichetta: [MISURATO] = misura vera (sensori 5T, mezzi GTT registrati ogni minuto da un
Raspberry Pi dal 3/10/2026); [PROGRAMMATO] = orario ufficiale GTT; [STIMATO] = calcolo nostro su dati veri;
[DATI SCARSI] = pochi dati. Le simulazioni usano l'orario programmato: non tengono conto di traffico, ritardi,
capienza e domanda reale.

## I risultati

Risultati in aggiornamento: vedi la pagina dei risultati.

## Fonti e licenze
- GTT: orari (GTFS) e dati in tempo reale (GTFS-RT), dati aperti.
- 5T (sistema dei trasporti della Città di Torino): flussi di traffico, parcheggi, ZTL, dati aperti.
- ISTAT: censimento 2021 (sezioni), pendolarismo 2011 e 2021.
- Agenzia della Mobilità Piemontese: indagine IMQ 2022 (dati aperti).
- Agenzia delle Entrate — OMI: quotazioni immobiliari.
- Comune di Torino (aperTO): catalogo dei servizi, parcheggi.
- © contributori di OpenStreetMap (ODbL).
- Sfondi della mappa: **condizioni d'uso da verificare prima di pubblicare**.

## Limiti generali
Orario programmato per accessibilità e scenari; raccolta dei dati misurati iniziata il 3/10/2026 (parcheggi dal
14/10): le serie sono ancora brevi. Limiti di ogni risultato nella sua scheda.

## Come rifare i calcoli
Python 3 con le librerie di `requirements.txt`. Gli script sono in `scripts/`, numerati; i `.bat` lanciano le
catene (es. `scripts/RISULTATO6_RIFAI.bat`). I dati grezzi non sono nel repository (vedi `docs/FONTI_DATI.md`).

---

# Mobility in Turin — how the city moves (English)

Personal data-analysis project (2026) on public transport and mobility in Turin, Italy: who travels where,
where services are missing, where the problems are, and a few "what if" scenarios. Two pages:
**`mappa_torino.html`** (interactive map) and **`risultati.html`** (one card per result). The pages are in Italian;
every card has a short summary in English. Tags: [MISURATO] measured, [PROGRAMMATO] scheduled timetable,
[STIMATO] estimated, [DATI SCARSI] little data.

## Results

Results being updated: see the results page.
