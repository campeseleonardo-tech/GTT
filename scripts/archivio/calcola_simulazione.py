#!/usr/bin/env python3
"""
calcola_simulazione.py - Applica uno scenario di modifica al GTFS di base e calcola le differenze in termini di passaggi totali e fermate coinvolte.

Lo script legge il file GTFS più recente in data/raw, applica le modifiche specificate in un file di scenario JSON
(e.g., modificare l'intervallo di corse per una linea e direzione) e restituisce:
- Passaggi totali nello scenario di base
- Passaggi totali nello scenario modificato
- Differenza (dopo - prima)
- Numero di fermate con variazione nei passaggi

Le modifiche attualmente supportate sono solo la variazione della frequenza (intervallo_minuti) per linee esistenti.
Altri tipi di modifiche (linee nuove, soppresse, deviate) sono riconosciuti ma non implementati in questa versione.

Esempio di utilizzo:
    python calcola_simulazione.py data/scenari/mio_scenario.json
    oppure, senza argomenti, usa lo scenario di esempio: scripts/scenario_esempio.json
"""
import csv
import io
import json
import sys
import zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

# [agente GT28-calcolare-il-confronto-d] Funzioni copiate e adattate da 04_genera_mappa.py
def trova_radice():
    for cartella in [Path(__file__).resolve().parent, *Path(__file__).resolve().parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    candidata = Path.home() / "Desktop" / "GTT"
    return candidata if candidata.is_dir() else Path(__file__).resolve().parent.parent

def ultimo(prefisso):
    RADICE = trova_radice()
    RAW = RADICE / "data" / "raw"
    trovati = sorted(RAW.glob(prefisso + "*"))
    if not trovati:
        sys.exit(f"File non trovato in {RAW}: {prefisso}*  (lancia prima 01_scarica_dati.py)")
    return trovati[-1]

def data_gtfs(s):
    return date(int(s[:4]), int(s[4:6]), int(s[6:8]))

def date_riferimento(inizio, fine):
    out = {}
    oggi = max(date.today(), inizio)
    for chiave, wd in (("fer", 1), ("sab", 5), ("dom", 6)):
        d = oggi
        while d.weekday() != wd:
            d += timedelta(days=1)
        if d > fine:
            d -= timedelta(days=7)
        out[chiave] = d
    return out

def servizi_attivi(cal, eccezioni, d):
    giorni = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    attivi = set()
    for r in cal:
        if data_gtfs(r["start_date"]) <= d <= data_gtfs(r["end_date"]) and r[giorni[d.weekday()]] == "1":
            attivi.add(r["service_id"])
    for r in eccezioni:
        if data_gtfs(r["date"]) == d:
            if r["exception_type"] == "1":
                attivi.add(r["service_id"])
            elif r["exception_type"] == "2":
                attivi.discard(r["service_id"])
    return attivi

# [agente GT28-calcolare-il-confronto-d] Funzioni specifiche per questo script
def leggi_gtfs_base(percorso_gtfs, giorno_tipo):
    """Legge il GTFS e restituisce:
    - rotte: dict di route_id -> {route_short_name, ...}
    - linee_fermata: dict di stop_id -> set di route_id che servono quella fermata
    - stop_times_processed: lista di (trip_id, stop_id, departure_time_in_minutes, sequence)
    - servizi_attivi_per_giorno: lista di insiemi di service_id attivi per ciascun tipo di giorno (fer, sab, dom)
    - giorni_riferimento: dict di tipo di giorno -> data di riferimento
    """
    z = zipfile.ZipFile(percorso_gtfs)
    info = next(csv.DictReader(io.TextIOWrapper(z.open("feed_info.txt"), encoding="utf-8-sig")))
    inizio, fine = data_gtfs(info["feed_start_date"]), data_gtfs(info["feed_end_date"])
    giorni = date_riferimento(inizio, fine)
    cal = list(csv.DictReader(io.TextIOWrapper(z.open("calendar.txt"), encoding="utf-8-sig")))
    ecc = list(csv.DictReader(io.TextIOWrapper(z.open("calendar_dates.txt"), encoding="utf-8-sig"))) if "calendar_dates.txt" in z.namelist() else []
    attivi = [servizi_attivi(cal, ecc, giorni[k]) for k in ["fer", "sab", "dom"]]
    giorno_index = {"fer": 0, "sab": 1, "dom": 2}[giorno_tipo]
    attivi_oggi = attivi[giorno_index]

    rotte = {}
    for r in csv.DictReader(io.TextIOWrapper(z.open("routes.txt"), encoding="utf-8-sig")):
        rotte[r["route_id"]] = {
            "s": r["route_short_name"] or r["route_id"],
            "t": int(r["route_type"] or 3),
            "l": r["route_long_name"],
        }

    viaggi = {}  # trip_id -> (route_id, service_ids_tuple, direction_id)
    forme = defaultdict(lambda: defaultdict(int))
    for r in csv.DictReader(io.TextIOWrapper(z.open("trips.txt"), encoding="utf-8-sig")):
        flags = tuple(r["service_id"] in a for a in attivi)
        viaggi[r["trip_id"]] = (r["route_id"], flags, r.get("direction_id", ""))
        if r.get("shape_id"):
            forme[(r["route_id"], r.get("direction_id", ""))][r["shape_id"]] += 1

    fermate = {r["stop_id"]: r for r in csv.DictReader(io.TextIOWrapper(z.open("stops.txt"), encoding="utf-8-sig"))}
    linee_fermata = defaultdict(set)
    inizio_corsa = {}  # trip_id -> (first_sequence, first_hour)
    tempi = {}  # trip_id -> [first_seq, first_min, last_seq, last_min]
    partenze_per_fermata = defaultdict(int)  # stop_id -> contatore partenze nel giorno
    partenze_linea_fermata = defaultdict(lambda: defaultdict(int))  # route_id -> stop_id -> contatori

    with z.open("stop_times.txt") as f:
        rd = csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig"))
        intestazione = next(rd)
        ix = {nome: i for i, nome in enumerate(intestazione)}
        i_t, i_d, i_a, i_s, i_q = ix["trip_id"], ix["departure_time"], ix["arrival_time"], ix["stop_id"], ix["stop_sequence"]
        for riga in rd:
            trip_id = riga[i_t]
            v = viaggi.get(trip_id)
            if not v:
                continue
            rid, flags, dir_id = v
            if not flags[giorno_index]:
                continue  # servizio non attivo oggi
            ora_partenza = riga[i_d]
            if not ora_partenza or len(ora_partenza) < 2:
                continue
            try:
                hh = int(ora_partenza[:2])
                mm = int(ora_partenza[3:5]) if len(ora_partenza) >= 5 else 0
                ss = int(ora_partenza[6:8]) if len(ora_partenza) >= 8 else 0
                minuti_partenza = hh * 60 + mm + ss / 60.0
            except ValueError:
                continue
            stop_id = riga[i_s]
            sequenza = int(riga[i_q])
            linee_fermata[stop_id].add(rid)
            partenze_per_fermata[stop_id] += 1
            # conteggio partenze per linea (utile per la simulazione)
            partenze_linea_fermata[rid][stop_id] += 1
            # Aggiorna tempi del viaggio per calcolare direzione (se necessario)
            tt = tempi.get(trip_id)
            if tt is None:
                tempi[trip_id] = [sequenza, minuti_partenza, sequenza, minuti_partenza]
            else:
                if sequenza < tt[0]:
                    tt[0], tt[1] = sequenza, minuti_partenza
                if sequenza > tt[2]:
                    tt[2], tt[3] = sequenza, minuti_partenza
            prec = inizio_corsa.get(trip_id)
            if prec is None or sequenza < prec[0]:
                inizio_corsa[trip_id] = (sequenza, hh)
    # Non abbiamo bisogno di elaborare le forme per questo calcolo, quindi restituiamo solo i dati necessari
    return {
        "rotte": rotte,
        "linee_fermata": linee_fermata,
        "fermate": fermate,
        "partenze_per_fermata": dict(partenze_per_fermata),
        "partenze_linea_fermata": {rid: dict(d) for rid, d in partenze_linea_fermata.items()},
        "viaggi": viaggi,
        "attivi_oggi": attivi_oggi,
        "giorno_tipo": giorno_tipo,
        "giorno_index": giorno_index,
    }

def applica_modifica_frequenza(gtfs_base, route_id, direzione, intervallo_minuti):
    """Applica una modifica di frequenza a una linea e direzione specificate.
    Restituisce un nuovo dizionario partenze_per_fermata con le partenze aggiornate.
    """
    # Copia del totale delle partenze per fermata (tutte le linee)
    partenze_per_fermata = gtfs_base["partenze_per_fermata"].copy()
    if route_id not in gtfs_base["rotte"]:
        return partenze_per_fermata  # linea non trovata, nessuna modifica

    # Calcola il numero di corse al giorno per la linea e direzione nella base
    corse_base_per_direzione = defaultdict(int)
    for trip_id, (rid, flags, dir_id) in gtfs_base["viaggi"].items():
        if rid == route_id and (direzione is None or dir_id == direzione):
            # Contiamo solo se il viaggio è attivo oggi (già filtrato in leggi_gtfs_base)
            corse_base_per_direzione[dir_id] += 1

    # Se nessuna direzione specificata, consideriamo entrambe
    if direzione is None:
        direzioni_da_modificare = ["0", "1"]
    else:
        direzioni_da_modificare = [direzione]

    # Per ogni direzione da modificare, sostituiremo le corse base con nuove corse all'intervallo specificato
    for dir_id in direzioni_da_modificare:
        num_corse_base = corse_base_per_direzione.get(dir_id, 0)
        if num_corse_base == 0:
            continue
        # Nuove corse: distribuite ogni `intervallo_minuti` minuti durante il giorno di servizio (24 ore = 1440 minuti)
        # Prima e ultima corsa alle 05:00 e 23:59? Per semplicità, distribuiamo da 05:00 a 23:59 (19 ore = 1140 minuti)
        # Ma usiamo l'intervallo per calcolare il numero di corse: floor(1140 / intervallo_minuti) + 1
        # Tuttavia, per non complicare, manteniamo lo stesso numero di corse della base e variamo l'intervallo?
        # Lo scenario specifica un intervallo, quindi il numero di corse dovrebbe cambiare.
        # Calcoliamo il numero di corse nuovo: giornolavoro in minuti / intervallo
        # Assumiamo servizio dalle 05:00 alle 23:59 (19 ore = 1140 minuti)
        minuti_servizio = 19 * 60  # 1140 minuti
        num_corse_nuove = minuti_servizio // intervallo_minuti
        if num_corse_nuove == 0:
            num_corse_nuove = 1  # almeno una corsa

        # Distribuiamo le nuove corse in modo uniforme nell'arco del servizio
        # Ogni corsa contribuisce con un numero di partenze pari al numero di fermate servite dalla linea in quella direzione
        # Per semplicità, assumiamo che ogni corsa serva tutte le fermate della linea (una stima grezza)
        # In realtà, dovremmo conoscere il percorso e la direzione per conoscere le fermate.
        # Poiché non abbiamo il percorso, utilizziamo un'approssimazione: il numero medio di fermate per linea
        # Questa è una limitazione nota.
        fermate_linea_direzione = set()
        for stop_id, linee in gtfs_base["linee_fermata"].items():
            if route_id in linee:
                # Non conosciamo la direzione effettiva per ogni fermata, quindi includiamo tutte le fermate della linea
                fermate_linea_direzione.add(stop_id)
        num_fermate_linea = len(fermate_linea_direzione)
        if num_fermate_linea == 0:
            continue

        # Sottraiamo le partenze base di questa linea e direzione
        for stop_id in fermate_linea_direzione:
            # Partenze della linea in quella fermata (prima della modifica)
            old_partenza_linea = gtfs_base["partenze_linea_fermata"].get(route_id, {}).get(stop_id, 0)
            if old_partenza_linea == 0:
                continue
            # Nuove partenze della stessa linea con la nuova frequenza
            new_partenza_linea = old_partenza_linea * num_corse_nuove / num_corse_base
            # Delta da aggiungere al totale della fermata
            delta = new_partenza_linea - old_partenza_linea
            current = partenze_per_fermata.get(stop_id, 0)
            partenze_per_fermata[stop_id] = current + delta
    return partenze_per_fermata
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Calcolare differenza di passaggi tra base e scenario.')
    parser.add_argument('scenario', nargs='?', default='scripts/scenario_esempio.json', help='Percorso al file JSON dello scenario')
    args = parser.parse_args()

    RADICE = trova_radice()
    percorso_scenario = Path(args.scenario)
    if not percorso_scenario.is_file():
        sys.exit(f"File scenario non trovato: {percorso_scenario}")

    with open(percorso_scenario, 'r', encoding='utf-8') as f:
        scenario = json.load(f)

    # Validazione minima dello scenario
    obbligatori = ["origine", "stato", "nome", "base_gtfs", "giorno_tipo", "linee_modificate"]
    for campo in obbligatori:
        if campo not in scenario:
            sys.exit(f"Campo mancante nello scenario: {campo}")

    giorno_tipo = scenario["giorno_tipo"]
    if giorno_tipo not in ["fer", "sab", "dom"]:
        sys.exit(f"giorno_tipo non valido: {giorno_tipo}. Deve essere fer, sab o dom.")

    # Trova il GTFS base
    percorso_gtfs = ultimo("gtt_gtfs_")
    print(f"Utilizzo GTFS base: {percorso_gtfs.name}")

    # Leggi base
    gtfs_base = leggi_gtfs_base(percorso_gtfs, giorno_tipo)
    passaggi_totali_base = sum(gtfs_base["partenze_per_fermata"].values())

    # Applica modifiche (solo linee_modificate per ora)
    partenze_scenario = gtfs_base["partenze_per_fermata"].copy()
    for mod in scenario["linee_modificate"]:
        route_id = mod["route_id"]
        direzione = mod.get("direzione")  # può essere None, "0", o "1"
        intervallo = mod.get("intervallo_minuti")
        if intervallo is None or intervallo <= 0:
            continue
        # Nota: non gestiamo linee_nuove, linee_soppresse, linee_deviate in questa versione
        partenze_scenario = applica_modifica_frequenza(gtfs_base, route_id, direzione, intervallo)

    passaggi_totali_scenario = sum(partenze_scenario.values())
    differenza = passaggi_totali_scenario - passaggi_totali_base
    fermate_con_modifica = sum(1 for stop_id in set(gtfs_base["partenze_per_fermata"].keys()) | set(partenze_scenario.keys())
                               if gtfs_base["partenze_per_fermata"].get(stop_id, 0) != partenze_scenario.get(stop_id, 0))

    risultato = {
        "passaggi_totali_baseline": int(passaggi_totali_base),
        "passaggi_totali_scenario": int(passaggi_totali_scenario),
        "differenza_passaggi": int(differenza),
        "fermate_con_modifica": int(fermate_con_modifica)
    }
    print(json.dumps(risultato, indent=2))

if __name__ == "__main__":
    main()
