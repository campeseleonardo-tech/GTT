#!/usr/bin/env python3
"""
86_prepara_pubblicazione.py  -  prepara una copia del portfolio che funziona da sola (Claude, 20/10/2026).
NON pubblica niente: crea solo la cartella pubblica/ (esclusa da git) e scrive README.md nella radice.

Cosa fa
-------
  1. Copia in pubblica/ le pagine (mappa_torino.html, simulazione.html) e tutti i file che caricano
     (data/stat.js, data/processed/orari_fermate.js, data/schede_risultati.js, data/replay_*.js,
     immagini/), con gli stessi percorsi relativi. Avvisa se un file manca.
  2. Scrive README.md (italiano, poi English) con un paragrafo per ogni risultato finito: domanda, numero
     principale e prima frase della risposta letti da data/schede_risultati.js (nessun numero scritto a mano);
     la parte inglese usa il campo in_english delle schede.
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
FILE_FISSI = ["mappa_torino.html", "simulazione.html", "data/stat.js", "data/processed/orari_fermate.js",
              "data/schede_risultati.js"]

INTRO_IT = """# Mobilità a Torino — come si muove la città

Progetto personale di analisi dei dati (Leo, 2026): chi va dove, dove mancano servizi, dove sono le criticità
del trasporto pubblico a Torino e nella Città metropolitana, e pochi scenari «cosa succede se».
Due pagine: **`mappa_torino.html`** (mappa con i temi) e **`simulazione.html`** (le schede dei risultati: domanda,
risposta, grafici, criteri, limiti).

Ogni numero porta un'etichetta: [MISURATO] = misura vera (sensori 5T, mezzi GTT registrati ogni minuto da un
Raspberry Pi dal 3/10/2026); [PROGRAMMATO] = orario ufficiale GTT; [STIMATO] = calcolo nostro su dati veri;
[DATI SCARSI] = pochi dati. Le simulazioni usano l'orario programmato: non tengono conto di traffico, ritardi,
capienza e domanda reale.

## I risultati
"""

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

Personal data-analysis project (Leo, 2026) on public transport and mobility in Turin, Italy: who travels where,
where services are missing, where the problems are, and a few "what if" scenarios. Two pages:
**`mappa_torino.html`** (interactive map) and **`simulazione.html`** (one card per result). The pages are in Italian;
every card has a short summary in English. Tags: [MISURATO] measured, [PROGRAMMATO] scheduled timetable,
[STIMATO] estimated, [DATI SCARSI] little data.

## Results
"""


def numero_it(v):
    """Numero all'italiana (10919 -> 10.919; 1.3 -> 1,3); il resto com'e'."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, float) and not v.is_integer():
        return f"{v:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{int(v):,}".replace(",", ".")


def leggi_schede():
    testo = SCHEDE.read_text(encoding="utf-8")
    inizio = testo.index("[")
    return json.loads(testo[inizio:testo.rstrip().rstrip(";").rindex("]") + 1])


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
    for src in sorted((RADICE / "data").glob("replay_*.js")):
        shutil.copy2(src, DEST / "data" / src.name)
        copiati += 1
    if (RADICE / "immagini").is_dir():
        shutil.copytree(RADICE / "immagini", DEST / "immagini")
    peso = sum(f.stat().st_size for f in DEST.rglob("*") if f.is_file())
    print(f"pubblica/: {copiati} file, {peso / 1e6:.1f} MB")

    schede = leggi_schede()
    it, en = [], []
    for s in schede:
        nk = s.get("numero_chiave") or {}
        titolo = f"Risultato {s.get('risultato', '')} — {s['titolo']}".strip(" —")
        riga = f"**{numero_it(nk.get('valore'))} {nk.get('unita', '')}** {nk.get('testo', '')}".strip() if nk else ""
        risposta = (s.get("risposta") or [""])[0]
        it.append(f"### {titolo}\n*{s.get('domanda', '')}*\n\n{riga}\n\n{risposta}\n")
        eng = s.get("in_english") or []
        c(f"riassunto in inglese per {titolo}", bool(eng))
        en.append(f"### Result {s.get('risultato', '')}\n" + (" ".join(eng) if eng else "*(English summary to be written)*") + "\n")
    README.write_text(INTRO_IT + "\n".join(it) + FONTI + INTRO_EN + "\n".join(en), encoding="utf-8")
    print(f"Scritto: {README} ({len(schede)} risultati); avvisi: {len(c.avvisi())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
