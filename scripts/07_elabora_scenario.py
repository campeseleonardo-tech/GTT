# -*- coding: utf-8 -*-
"""
scripts/07_elabora_scenario.py - Motore base per scenari alternativi

Legge il GTFS di base applica un file di scenario in data/scenari/<nome>.json
e restituisce:
- passaggi totali baseline
- passaggi totali scenario
- differenza (dopo - prima)
- numero di fermate con variazione
- avviso di simulazione (obbligatorio)

Usage:
    python 07_elabora_scenario.py [nome_scenario]
Se omesso, usa scripts/scenario_esempio.json
"""

import json
import sys
from pathlib import Path

# Aggiunge la radice del progetto al path
import os
# Cambia alla radice del progetto (due livelli sopra scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.calcola_simulazione import (
    trova_radice,
    ultimo,
    leggi_gtfs_base,
    applica_modifica_frequenza,
)


def main():
    # Parsing argomenti
    args = sys.argv[1:]  # skip script name
    scenario_name = args[0] if args else "scenario_esempio"

    # Percorso dello scenario (cerca in data/scenari/ e scripts/)
    scenario_path = Path(f"data/scenari/{scenario_name}.json")
    if not scenario_path.is_file():
        scenario_path = Path(f"scripts/{scenario_name}.json")
    if not scenario_path.is_file():
        sys.exit(f"File scenario non trovato: {scenario_path}")

    # Leggi scenario
    with open(scenario_path, "r", encoding="utf-8") as f:
        scenario = json.load(f)

    # Validazione minima
    obbligatori = ["origine", "stato", "nome", "base_gtfs", "giorno_tipo", "linee_modificate"]
    for campo in obbligatori:
        if campo not in scenario:
            sys.exit(f"Campo obbligatorio mancante nello scenario: {campo}")

    giorno_tipo = scenario["giorno_tipo"]
    if giorno_tipo not in ["fer", "sab", "dom"]:
        sys.exit(f"giorno_tipo non valido: {giorno_tipo}. Deve essere fer, sab o dom.")

    # Trova il GTFS base
    percorso_gtfs = ultimo(scenario["base_gtfs"])
    print(f"Utilizzo GTFS base: {percorso_gtfs.name}")

    # Leggi base
    gtfs_base = leggi_gtfs_base(percorso_gtfs, giorno_tipo)
    passaggi_totali_base = sum(gtfs_base["partenze_per_fermata"].values())

    # Copia baseline e applica modifiche
    partenze_scenario = gtfs_base["partenze_per_fermata"].copy()
    for mod in scenario["linee_modificate"]:
        route_id = mod["route_id"]
        direzione = mod.get("direzione")
        intervallo = mod.get("intervallo_minuti")
        if intervallo is None or intervallo <= 0:
            continue
        # Applica modifica frequenza (supportata solo variazione frequenza per ora)
        partenze_scenario = applica_modifica_frequenza(
            gtfs_base, route_id, direzione, intervallo
        )

    passaggi_totali_scenario = sum(partenze_scenario.values())
    differenza = passaggi_totali_scenario - passaggi_totali_base
    fermate_con_modifica = sum(
        1
        for stop_id in set(gtfs_base["partenze_per_fermata"].keys()) | set(partenze_scenario.keys())
        if gtfs_base["partenze_per_fermata"].get(stop_id, 0) != partenze_scenario.get(stop_id, 0)
    )

    risultato = {
        "passaggi_totali_baseline": int(passaggi_totali_base),
        "passaggi_totali_scenario": int(passaggi_totali_scenario),
        "differenza_passaggi": int(differenza),
        "fermate_con_modifica": int(fermate_con_modifica),
        "giorno_tipo": giorno_tipo,
        "scenario_nome": scenario.get("nome", scenario_name),
        "linee_modificate": scenario.get("linee_modificate", []),
    }

    # Stampa risultati
    print(json.dumps(risultato, indent=2))

    # Avviso obbligatorio (va mostrato ovunque venga usato lo scenario)
    print(
        "\n⚠ SIMULAZIONE SU ORARIO PROGRAMMATO"
    )
    print(
        "I risultati mostrano l'offerta potenziale (passaggi/ora, residenti raggiunti, tempi di attesa teorici)"
    )
    print("calcolata applicando le variazioni indicate all'orario ufficiale GTFS.")
    print("Non tengono conto di: traffico reale, ritardi, capienza dei mezzi, domanda effettiva passeggeri, regolarità del servizio.")
    print("Un aumento di corse sulla carta non garantisce che i bus arrivino in orario.")
    print("Dati [PROGRAMMATO] / [STIMATO] — non [MISURATO].")


if __name__ == "__main__":
    main()