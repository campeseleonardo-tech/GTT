#!/usr/bin/env python3
"""
76_verifiche_r6v2.py  -  Risultato 6 v2, PASSO 9: verifiche indipendenti.

Cosa fa
-------
Rifà con un metodo diverso i calcoli piu' importanti del Risultato 6 v2 e controlla che
i risultati coincidano:
  1. numero di luoghi (raggruppamento con cKDTree + componenti connesse);
  2. b2 e c2 di 5 luoghi a caso (seme 20261018), rifatti dai file originali;
  3. la firma di riempimento di Porta Susa FS e Venchi Unica, rifatta con pandas;
  4. la superficie di 3 parcheggi OpenStreetMap vicino a Fermi, rifatta con shapely in
     EPSG:32632;
  5. la copertura dei 5 interscambi ufficiali a 200 m sulle fermate della versione 1;
  6. stato di git: nessun commit, nessun file esistente modificato.

Cosa legge
----------
  i file di output dei passi 1-8 e i dati originali (GTFS, IMQ, database, OSM)

Cosa scrive
-----------
  docs/RAPPORTO_R6V2_VERIFICHE.txt

Come si lancia
--------------
  python scripts\\76_verifiche_r6v2.py
"""
import csv
import io
import json
import math
import random
import sqlite3
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import osmium
import pandas as pd
from pyproj import Transformer
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from shapely.geometry import Polygon

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
V1 = RADICE / "data" / "processed" / "risultato6_interscambio.json"
LUOGHI = RADICE / "data" / "processed" / "risultato6_v2" / "luoghi.json"
SEGNALI = RADICE / "data" / "processed" / "risultato6_v2" / "segnali.json"
RIEMPIMENTO = RADICE / "data" / "processed" / "risultato6_v2" / "riempimento.json"
PARCHEGGI = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi.json"
GTFS = RADICE / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"
SPOSTAMENTI = RADICE / "data" / "processed" / "imq" / "spostamenti.csv"
DB = RADICE / "data" / "storico_backup.sqlite"
PBF = RADICE / "data" / "otp" / "rete" / "torino_cintura.osm.pbf"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_VERIFICHE.txt"

LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0
SEME = 20261018
ORE_PENDOLARI = (6, 7, 8, 9, 16, 17, 18, 19)
FERMI = (45.0766, 7.5903)


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def proietta(lon, lat):
    return (lon * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF)), lat * FATTORE_GRADI_M)


# --- 1: raggruppamento con cKDTree + componenti connesse --------------------------------

def verifica_luoghi(luoghi_attesi):
    dati = json.loads(V1.read_text(encoding="utf-8"))
    fermate = [f for f in dati["fermate"] if f.get("lat") is not None]
    xy = np.array([proietta(f["lon"], f["lat"]) for f in fermate])
    albero = cKDTree(xy)
    # raggio un po' piu' largo (la proiezione piana sbaglia di ~0,4%), poi filtro esatto
    candidate = np.array(sorted(albero.query_pairs(41.0)))
    vere = [(i, j) for i, j in candidate
            if haversine_m(fermate[i]["lat"], fermate[i]["lon"],
                           fermate[j]["lat"], fermate[j]["lon"]) <= 40.0]
    coppie = np.array(vere) if vere else np.zeros((0, 2), dtype=np.int64)
    if len(coppie):
        grafo = coo_matrix((np.ones(len(coppie)), (coppie[:, 0], coppie[:, 1])),
                           shape=(len(fermate), len(fermate)))
        n, _ = connected_components(grafo, directed=False)
    else:
        n = len(fermate)
    return len(fermate), n, luoghi_attesi


# --- 2: b2 e c2 a mano -------------------------------------------------------------------

def verifica_b2_c2(luoghi, segnali_campione):
    z = zipfile.ZipFile(GTFS)
    attivi = set()
    with z.open("calendar.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r["monday"] == "1" and r["start_date"] <= "20261012" <= r["end_date"]:
                attivi.add(r["service_id"])
    with z.open("calendar_dates.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r["date"] == "20261012":
                if r["exception_type"] == "1":
                    attivi.add(r["service_id"])
                elif r["exception_type"] == "2":
                    attivi.discard(r["service_id"])
    trip = set()
    with z.open("trips.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r["service_id"] in attivi:
                trip.add(r["trip_id"])
    ore = defaultdict(lambda: defaultdict(int))
    with z.open("stop_times.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r["trip_id"] in trip:
                ore[r["stop_id"]][int(r["departure_time"].split(":")[0]) % 24] += 1

    sp = pd.read_csv(SPOSTAMENTI, sep=";", encoding="utf-8-sig", dtype=str)
    sp["PESO"] = pd.to_numeric(sp["PESO"].str.replace(",", ".", regex=False), errors="coerce")
    sp["minuti"] = pd.to_numeric(sp["ORA_PAR"].str[:2], errors="coerce") * 60 + \
        pd.to_numeric(sp["ORA_PAR"].str[3:5], errors="coerce")
    par = sp["COD_PAR"].fillna("").str.strip()
    arr = sp["COD_ARR"].fillna("").str.strip()
    maschera = (sp["MEZZO1"].isin(["03", "04", "21"]) & (par != "")
                & ~par.str.startswith("Q") & arr.str.startswith("Q")
                & sp["minuti"].between(360, 599))
    c2 = {}
    for _, riga in sp[maschera].iterrows():
        for zona in (riga["COD_PAR"].strip(), riga["COD_ARR"].strip()):
            c2[zona] = c2.get(zona, 0.0) + riga["PESO"]

    esiti = []
    for l in luoghi:
        b2 = sum(ore[sid].get(h, 0) for sid in l["stop_ids"] for h in ORE_PENDOLARI) / 8.0
        c2v = c2.get(l["zona_imq"])
        seg = segnali_campione[l["id_luogo"]]
        esiti.append({"id_luogo": l["id_luogo"], "nome": l["nome"], "zona": l["zona_imq"],
                      "b2_rifatto": round(b2, 3), "b2_segnale": seg["b2"],
                      "c2_rifatto": round(c2v, 1) if c2v is not None else None,
                      "c2_segnale": seg["c2"]})
    return esiti


# --- 3: firma con pandas -----------------------------------------------------------------

def _ultima_domenica(anno, mese):
    from datetime import date, timedelta
    d = date(anno, mese, 31)
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


def firma_pandas(nome):
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    occ = pd.read_sql_query("select * from occupazione_pk", con)
    par = pd.read_sql_query("select * from parcheggi_5t", con)
    con.close()
    occ = occ[occ["stato"] == 1].dropna(subset=["liberi"])
    occ = occ.merge(par, on="id", how="inner")
    tot = occ["totale_y"].fillna(occ["totale_x"])
    occ["occ"] = (1 - occ["liberi"] / tot).clip(0, 1)
    occ["dt"] = pd.to_datetime(occ["generato_utc"].str[:19])
    a = occ["dt"].dt.year.iloc[0]
    inizio = pd.Timestamp(a, 3, _ultima_domenica(a, 3).day, 1)
    fine = pd.Timestamp(a, 10, _ultima_domenica(a, 10).day, 1)
    occ["loc"] = occ["dt"] + pd.to_timedelta(
        np.where((occ["dt"] >= inizio) & (occ["dt"] < fine), 2, 1), unit="h")
    uno = occ[occ["nome"] == nome].copy()
    uno["giorno"] = uno["loc"].dt.date
    uno["weekend"] = uno["loc"].dt.weekday >= 5
    conteggi = uno.groupby(["giorno", "weekend"]).size().reset_index(name="n")
    validi = conteggi[conteggi["n"] >= 230]
    feriali = set(validi[~validi["weekend"]]["giorno"])
    weekend = set(validi[validi["weekend"]]["giorno"])
    uno = uno[uno["giorno"].isin(feriali | weekend)]
    uno["ora"] = uno["loc"].dt.hour
    def media(giorni, ore):
        sel = uno[uno["giorno"].isin(giorni) & uno["ora"].isin(ore)]
        return sel["occ"].mean() if len(sel) else None
    N = media(feriali, (2, 3, 4))
    G = media(feriali, tuple(range(10, 16)))
    W = media(weekend, tuple(range(10, 16)))
    orarie = uno[uno["giorno"].isin(feriali)].groupby("ora")["occ"].mean()
    ampiezza = orarie.max() - orarie.min() if len(orarie) >= 2 else 0.0
    if len(feriali) < 2:
        firma = "dati_insufficienti"
    elif ampiezza < 0.05:
        firma = "dato_bloccato"
    elif G - N >= 0.20 and (not weekend or G - W >= 0.10):
        firma = "pendolare"
    elif N - G >= 0.10:
        firma = "residenziale"
    elif G - N >= 0.20 and weekend and G - W < 0.10:
        firma = "destinazione"
    else:
        firma = "misto"
    return {"giorni_validi": len(validi), "N": round(N, 4), "G": round(G, 4),
            "W": round(W, 4) if W is not None else None, "ampiezza": round(ampiezza, 4),
            "firma": firma}


# --- 4: superficie OSM con shapely in EPSG:32632 ----------------------------------------

def superfici_osm(ids):
    aree = {}
    class Lettore(osmium.SimpleHandler):
        def way(self, w):
            if w.id not in ids:
                return
            punti = [(nd.location.lon, nd.location.lat) for nd in w.nodes if nd.location.valid()]
            if len(punti) >= 3:
                aree[w.id] = punti
    Lettore().apply_file(str(PBF), locations=True)
    tr = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
    esiti = []
    for oid, punti in aree.items():
        x, y = tr.transform([p[0] for p in punti], [p[1] for p in punti])
        esiti.append((oid, Polygon(zip(x, y)).area))
    return esiti


def main():
    for p in (V1, LUOGHI, SEGNALI, RIEMPIMENTO, PARCHEGGI, GTFS, SPOSTAMENTI, DB, PBF):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    righe = []
    righe.append("RAPPORTO R6 v2 — VERIFICHE INDIPENDENTI (Passo 9)")
    righe.append(f"metodo diverso da quello dei passi 1-8, seme {SEME}")
    righe.append("")

    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))
    segnali = {s["id_luogo"]: s for s in json.loads(SEGNALI.read_text(encoding="utf-8"))["luoghi"]}

    print("1) numero di luoghi con un altro metodo...")
    n_fermate, n_luoghi, atteso = verifica_luoghi(luoghi["n_luoghi"])
    ok = n_luoghi == luoghi["n_luoghi"]
    print(f"   fermate {n_fermate}, luoghi {n_luoghi} (Passo 1: {luoghi['n_luoghi']}) -> "
          f"{'UGUALE' if ok else 'DIVERSO'}")
    righe.append("1) Numero di luoghi, con cKDTree 40 m + componenti connesse (metodo diverso)")
    righe.append(f"   fermate: {n_fermate}; luoghi: {n_luoghi}; Passo 1: {luoghi['n_luoghi']}; "
                 f"{'COINCIDONO' if ok else 'NON COINCIDONO'}")
    righe.append("")

    print("2) b2 e c2 di 5 luoghi a caso...")
    random.seed(SEME)
    campione = random.sample(luoghi["luoghi"], 5)
    esiti = verifica_b2_c2(campione, segnali)
    righe.append("2) b2 e c2 rifatti dai file originali per 5 luoghi a caso")
    tutti_ok = True
    for e in esiti:
        ok_b2 = abs((e["b2_rifatto"] or 0) - (e["b2_segnale"] or 0)) < 0.01
        ok_c2 = (e["c2_rifatto"] is None and e["c2_segnale"] is None) or (
            e["c2_rifatto"] is not None and e["c2_segnale"] is not None
            and abs(e["c2_rifatto"] - e["c2_segnale"]) < 1.0)
        tutti_ok = tutti_ok and ok_b2 and ok_c2
        righe.append(f"   {e['id_luogo']} {e['nome'][:34]:34s} zona={e['zona'] or '-':5s} "
                     f"b2 {e['b2_rifatto']} (file {e['b2_segnale']}) "
                     f"c2 {e['c2_rifatto']} (file {e['c2_segnale']}) -> "
                     f"{'OK' if ok_b2 and ok_c2 else 'DIVERSO'}")
    righe.append(f"   esito: {'tutti uguali' if tutti_ok else 'ci sono differenze'}")
    righe.append("")

    print("3) firma di Porta Susa FS e Venchi Unica con pandas...")
    riemp = {r["nome"]: r for r in json.loads(RIEMPIMENTO.read_text(encoding="utf-8"))["parcheggi"]}
    righe.append("3) Firma di riempimento rifatta con pandas, direttamente dal database")
    for nome in ("PORTA SUSA FS", "VENCHI UNICA"):
        f = firma_pandas(nome)
        r = riemp[nome]
        ok = (f["firma"] == r["firma"]
              and abs((f["G"] or 0) - (r["G_giorno_feriale"] or 0)) < 0.002
              and abs((f["N"] or 0) - (r["N_notte_feriale"] or 0)) < 0.002)
        righe.append(f"   {nome}: firma {f['firma']} (file {r['firma']}); "
                     f"N {f['N']} (file {r['N_notte_feriale']}), G {f['G']} (file {r['G_giorno_feriale']}) "
                     f"-> {'UGUALE' if ok else 'DIVERSO'}")
    righe.append("")

    print("4) superficie di 3 parcheggi OSM vicino a Fermi...")
    parcheggi = json.loads(PARCHEGGI.read_text(encoding="utf-8"))["parcheggi"]
    vicini = [p for p in parcheggi if p["fonti"] == ["OSM"] and p["id_osm"] is not None
              and p["superficie_m2"] and p["parking"] != "underground"
              and haversine_m(FERMI[0], FERMI[1], p["lat"], p["lon"]) <= 500]
    vicini.sort(key=lambda p: -p["superficie_m2"])
    scelti = vicini[:3]
    righe.append("4) Superficie di 3 parcheggi OpenStreetMap vicino a Fermi, rifatta con shapely "
                 "in EPSG:32632")
    if len(scelti) < 3:
        righe.append("   ATTENZIONE: meno di 3 parcheggi OSM con superficie vicino a Fermi")
    superfici = dict(superfici_osm({p["id_osm"] for p in scelti}))
    for p in scelti:
        nuova = superfici.get(p["id_osm"])
        if nuova is None:
            righe.append(f"   OSM {p['id_osm']}: non ritrovato nel PBF")
            continue
        diff = abs(nuova - p["superficie_m2"]) / p["superficie_m2"]
        righe.append(f"   OSM {p['id_osm']}: {p['superficie_m2']:.0f} m2 (file) contro "
                     f"{nuova:.0f} m2 (shapely UTM32) -> differenza {100 * diff:.2f}% "
                     f"{'OK' if diff <= 0.02 else 'TROPPO DIVERSA'}")
    righe.append("")

    print("5) copertura dei 5 ufficiali a 200 m sulle fermate v1...")
    dati = json.loads(V1.read_text(encoding="utf-8"))
    ufficiali = [p for p in dati["parcheggi"] if p.get("interscambio")]
    critiche = [f for f in dati["fermate"] if f.get("fermata_critica")]
    coperte = [f for f in critiche if any(
        haversine_m(f["lat"], f["lon"], p["lat"], p["lon"]) <= 200 for p in ufficiali)]
    righe.append("5) Copertura dei 5 interscambi ufficiali a 200 m, sulle fermate della v1")
    righe.append(f"   fermate critiche {len(critiche)}, coperte {len(coperte)}, "
                 f"scoperte {len(critiche) - len(coperte)} -> "
                 f"{'come la v1 (17)' if len(coperte) == 17 else 'DIVERSO dalla v1 (17)'}")
    righe.append("")

    print("6) stato di git...")
    try:
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=RADICE,
                                capture_output=True, text=True).stdout.strip()
        stato = subprocess.run(["git", "status", "--short"], cwd=RADICE,
                               capture_output=True, text=True).stdout
        nuovi = [r[3:].strip() for r in stato.splitlines() if r.startswith("??")]
        modificati = [r[3:].strip() for r in stato.splitlines() if r and r[1] != "?"]
        ultimo = subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"],
                                cwd=RADICE, capture_output=True, text=True).stdout.strip()
    except OSError as e:
        branch, stato, nuovi, modificati, ultimo = "-", "", [], [], f"errore: {e}"
    righe.append("6) Stato di git")
    righe.append(f"   ramo: {branch}; ultimo commit: {ultimo}")
    righe.append(f"   file modificati (tracciati da git): {len(modificati)}")
    for m in modificati:
        righe.append(f"     MODIFICATO: {m}")
    righe.append(f"   file nuovi non tracciati: {len(nuovi)}")
    for m in nuovi:
        righe.append(f"     nuovo: {m}")

    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print(f"Scritto: {RAPPORTO}")


if __name__ == "__main__":
    sys.exit(main())
