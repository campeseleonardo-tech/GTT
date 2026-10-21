#!/usr/bin/env python3
"""
86_prepara_pubblicazione.py  -  prepara una copia del portfolio che funziona da sola (Claude, 20/10/2026).
NON pubblica niente: crea solo la cartella pubblica/ (esclusa da git) e scrive README.md nella radice.

Cosa fa
-------
  1. Copia in pubblica/ le pagine (mappa_torino.html, simulazione.html) e tutti i file che caricano
     (data/processed/orari_fermate.js, data/schede_risultati.js, data/catalogo/*.js, immagini/), con gli stessi percorsi relativi. Avvisa se un file manca.
  2. Scrive README.md (italiano, poi English) senza i numeri dei risultati: al loro posto «Risultati in
     aggiornamento: vedi la pagina dei risultati» (i numeri vivono nelle schede di simulazione.html).
  3. Stampa il peso della cartella.

Come si lancia
--------------
  python scripts\\86_prepara_pubblicazione.py
  poi: python scripts\\prova_pagine_r6.py --cartella pubblica --senza-screenshot   (deve dare 0 errori)
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comuni  # noqa: E402

RADICE = comuni.RADICE
DEST = RADICE / "pubblica"
SCHEDE = RADICE / "data" / "schede_risultati.js"
README = RADICE / "README.md"
FILE_FISSI = ["mappa_torino.html", "simulazione.html", "data/processed/orari_fermate.js",
              "data/schede_risultati.js"]

INTRO_IT = """# Mobilità a Torino — come si muove la città

Progetto personale di analisi dei dati (2026): chi va dove, dove mancano servizi, dove sono le criticità
del trasporto pubblico a Torino e nella Città metropolitana, e pochi scenari «cosa succede se».
Due pagine: **`mappa_torino.html`** (mappa con i temi) e **`simulazione.html`** (le schede dei risultati: domanda,
risposta, grafici, criteri, limiti).

Ogni numero porta un'etichetta: [MISURATO] = misura vera (sensori 5T, mezzi GTT registrati ogni minuto da un
Raspberry Pi dal 3/10/2026); [PROGRAMMATO] = orario ufficiale GTT; [STIMATO] = calcolo nostro su dati veri;
[DATI SCARSI] = pochi dati. Le simulazioni usano l'orario programmato: non tengono conto di traffico, ritardi,
capienza e domanda reale.

## I risultati
"""

RISULTATI_IT = "\nRisultati in aggiornamento: vedi la pagina dei risultati.\n"
RISULTATI_EN = "\nResults being updated: see the results page.\n"

FONTI = """
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
"""

INTRO_EN = """
---

# Mobility in Turin — how the city moves (English)

Personal data-analysis project (2026) on public transport and mobility in Turin, Italy: who travels where,
where services are missing, where the problems are, and a few "what if" scenarios. Two pages:
**`mappa_torino.html`** (interactive map) and **`simulazione.html`** (one card per result). The pages are in Italian;
every card has a short summary in English. Tags: [MISURATO] measured, [PROGRAMMATO] scheduled timetable,
[STIMATO] estimated, [DATI SCARSI] little data.

## Results
"""


def main():
    c = comuni.Controlli()
    c("esiste data/schede_risultati.js (lancia prima schede_risultati.py)", SCHEDE.exists(), bloccante=True)
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    copiati = 0
    for rel in FILE_FISSI:
        src = RADICE / rel
        if c(f"file {rel}", src.exists()):
            (DEST / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, DEST / rel)
            copiati += 1
    # la mappa carica data/catalogo/<gruppo>.js quando si apre «Luoghi della città»
    for src in sorted((RADICE / "data" / "catalogo").glob("*.js")):
        (DEST / "data" / "catalogo").mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, DEST / "data" / "catalogo" / src.name)
        copiati += 1
    c("catalogo copiato (data/catalogo/*.js)", (DEST / "data" / "catalogo").is_dir())
    if (RADICE / "immagini").is_dir():
        shutil.copytree(RADICE / "immagini", DEST / "immagini")
    peso = sum(f.stat().st_size for f in DEST.rglob("*") if f.is_file())
    print(f"pubblica/: {copiati} file, {peso / 1e6:.1f} MB")

    # i numeri dei risultati non stanno nel README (invecchiano): ci sono nelle schede di simulazione.html
    README.write_text(INTRO_IT + RISULTATI_IT + FONTI + INTRO_EN + RISULTATI_EN, encoding="utf-8")
    print(f"Scritto: {README}; avvisi: {len(c.avvisi())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
