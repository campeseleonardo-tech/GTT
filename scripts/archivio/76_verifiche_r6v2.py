#!/usr/bin/env python3
"""
76_verifiche_r6v2.py  -  Risultato 6 v2, PASSO G7: verifiche indipendenti.

Cosa fa
-------
Rifa' con un metodo diverso i calcoli piu' importanti del giro 2 e controlla che i
risultati coincidano:
  1. numero di luoghi (cKDTree + componenti connesse, con filtro esatto haversine);
  2. b2 e c2 di 5 luoghi a caso (seme 20261018), rifatti dai file originali;
  3. firma di riempimento di Porta Susa FS e Venchi Unica, rifatta con pandas;
  4. superficie di 3 parcheggi OpenStreetMap vicino a Fermi, rifatta con shapely in EPSG:32632;
  5. copertura dei 5 interscambi ufficiali a 200 m sulle fermate della versione 1 (= 17);
  6. [NUOVO giro 2] a2 di 8 luoghi a caso (seme 20261019) rifatto con shapely in EPSG:32632
     e un indice STRtree dei tratti, applicando la stessa regola del modulo 77;
  7. [NUOVO] numero di luoghi dell'universo rifatto con pandas dalle zone IMQ;
  8. [NUOVO] zona centrale, forza e classe di 5 parcheggi (3 del 5T + 2 OSM) rifatti a mano;
  9. [NUOVO] soglia del 90° di S2 rifatta con numpy sui soli luoghi dell'universo;
 10. stato di git: nessun commit, elenco dei file modificati e dei nuovi.

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
from scipy.stats import rankdata
from shapely.geometry import LineString, Point, Polygon
from shapely.strtree import STRtree

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
NODI = RADICE / "data" / "processed" / "risultato6_v2" / "nodi.json"
FUNZIONE = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi_funzione.json"
SCENARI = RADICE / "data" / "processed" / "risultato6_v2" / "scenari.json"
ISTAT = RADICE / "data" / "processed" / "risultato6_v2" / "istat2011_proporzioni.json"
ZONE = RADICE / "data" / "processed" / "imq_zone.json"
ZONE_GEO = RADICE / "data" / "processed" / "imq_zone_geo.json"
GTFS = RADICE / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"
SPOSTAMENTI = RADICE / "data" / "processed" / "imq" / "spostamenti.csv"
DB = RADICE / "data" / "storico_backup.sqlite"
PBF = RADICE / "data" / "otp" / "rete" / "torino_cintura.osm.pbf"
RETE = RADICE / "data" / "processed" / "traffico_d" / "rete" / "rete_auto.npz"
ASSI = RADICE / "data" / "processed" / "traffico_d" / "assi_tratte.npz"
TRATTE = RADICE / "data" / "processed" / "traffico_d" / "tratte_traffico.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_VERIFICHE.txt"

LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0
SEME = 20261018
SEME2 = 20261019
ORE_PENDOLARI = (6, 7, 8, 9, 16, 17, 18, 19)
FERMI = (45.0766, 7.5903)
CLASSI_MINORI = ("service", "residential", "living_street")
MACRO_UNIVERSO = ("01 Torino", "02 Cintura", "03 Resto CMTO")


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

def verifica_luoghi():
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
    return len(fermate), n


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
    elif ampiezza < 0.06:
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


# --- 6: a2 con shapely (metodo diverso) --------------------------------------------------

def prepara_tratte():
    from collections import defaultdict as dd
    tratte = json.loads(TRATTE.read_text(encoding="utf-8"))["tratte"]
    comuni_asse = dd(set)
    per_id = {}
    for t in tratte:
        if t.get("comune"):
            comuni_asse[t["asse"]].add(t["comune"])
        p = t["punteggio"]
        cls = t.get("classe") or ""
        motivi = t.get("motivi") or []
        if cls in ("motorway", "trunk"):
            pc = 5
        elif cls == "primary":
            pc = max(p, 4)
        elif cls == "secondary":
            pc = max(p, 3)
        elif cls in CLASSI_MINORI and not motivi:
            pc = min(p, 2)
        else:
            pc = p
        per_id[t["id"]] = {"nome": t.get("nome"), "classe": cls, "punteggio_corr": pc,
                           "asse": t["asse"],
                           "asse_ingresso": t["asse"] in {a for a, cs in comuni_asse.items()
                                                          if "Torino" in cs and len(cs) > 1}}
    assi_ingresso = {a for a, cs in comuni_asse.items() if "Torino" in cs and len(cs) > 1}
    for v in per_id.values():
        v["asse_ingresso"] = v["asse"] in assi_ingresso
    return per_id


def indice_shapely():
    """Indice STRtree dei tratti stradali in EPSG:32632 (metodo diverso dal modulo 77)."""
    rete = np.load(RETE)
    edge_pts, edge_off = rete["edge_pts"], rete["edge_off"]
    edge_tratta = np.load(ASSI)["edge_tratta"]
    tr = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
    linee = []
    tratte_edge = []
    for e in range(len(edge_off) - 1):
        pts = edge_pts[edge_off[e]:edge_off[e + 1]]
        x, y = tr.transform([p[1] for p in pts], [p[0] for p in pts])
        if len(x) < 2:
            continue
        linee.append(LineString(zip(x, y)))
        tratte_edge.append(int(edge_tratta[e]))
    albero = STRtree(linee)
    return albero, linee, tratte_edge, tr


def trova_strada_shapely(albero, linee, tratte_edge, tr, per_id, lat, lon,
                         raggio_stretto=50.0, raggio_largo=150.0):
    x, y = tr.transform(lon, lat)
    p = Point(x, y)
    idx = list(albero.query(p.buffer(raggio_largo)))

    def info_ed(e):
        tid = tratte_edge[e]
        return per_id.get(tid, {}), tid

    def distanza(e):
        return linee[e].distance(p)

    # 1. non minori entro il raggio stretto: punteggio piu' alto, poi il piu' vicino
    cand = [(distanza(e), e) for e in idx
            if distanza(e) <= raggio_stretto
            and info_ed(e)[0].get("classe") not in CLASSI_MINORI]
    if cand:
        d, e = max(cand, key=lambda de: (info_ed(de[1])[0]["punteggio_corr"], -de[0]))
        return d, info_ed(e)[0], info_ed(e)[1], "ok"
    # 2. non minori entro il raggio largo: il piu' vicino
    cand = [(distanza(e), e) for e in idx
            if distanza(e) <= raggio_largo
            and info_ed(e)[0].get("classe") not in CLASSI_MINORI]
    if cand:
        d, e = min(cand)
        return d, info_ed(e)[0], info_ed(e)[1], "strada_lontana"
    # 3. minori entro il raggio stretto: il piu' vicino
    cand = [(distanza(e), e) for e in idx
            if distanza(e) <= raggio_stretto
            and info_ed(e)[0].get("classe") in CLASSI_MINORI]
    if cand:
        d, e = min(cand)
        return d, info_ed(e)[0], info_ed(e)[1], "solo_minore"
    return None, None, None, "nessuna"


# --- 8: classe di un parcheggio a mano ---------------------------------------------------

def zone_shapely():
    geo = json.loads(ZONE_GEO.read_text(encoding="utf-8"))
    tr = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
    zone = []
    for z in geo:
        g = z["g"]
        if isinstance(g, str):
            g = json.loads(g)
        if g and isinstance(g[0][0], (int, float)):
            anelli = [g]
        elif g and isinstance(g[0][0][0], (int, float)):
            anelli = g
        else:
            anelli = [anello for poligono in g for anello in poligono]
        for anello in anelli:
            x, y = tr.transform([p[1] for p in anello], [p[0] for p in anello])
            pol = Polygon(zip(x, y)).buffer(0)
            if not pol.is_empty:
                zone.append((z["cod"], pol))
    return zone, tr


def main():
    for p in (V1, LUOGHI, SEGNALI, RIEMPIMENTO, PARCHEGGI, NODI, FUNZIONE, SCENARI, ZONE,
              ZONE_GEO, GTFS, SPOSTAMENTI, DB, PBF, RETE, ASSI, TRATTE):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    righe = []
    righe.append("RAPPORTO R6 v2, GIRO 2 — VERIFICHE INDIPENDENTI (Passo G7)")
    righe.append(f"metodi diversi da quelli dei passi G0-G5; semi {SEME} e {SEME2}")
    righe.append("")

    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))
    segnali_el = json.loads(SEGNALI.read_text(encoding="utf-8"))["luoghi"]
    segnali = {s["id_luogo"]: s for s in segnali_el}

    print("1) numero di luoghi con un altro metodo...")
    n_fermate, n_luoghi = verifica_luoghi()
    ok = n_luoghi == luoghi["n_luoghi"]
    print(f"   fermate {n_fermate}, luoghi {n_luoghi} (Passo 1: {luoghi['n_luoghi']}) -> "
          f"{'UGUALE' if ok else 'DIVERSO'}")
    righe.append("1) Numero di luoghi, con cKDTree 41 m + filtro esatto + componenti connesse")
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

    print("6) a2 di 8 luoghi a caso, con shapely in EPSG:32632...")
    per_id = prepara_tratte()
    albero, linee, tratte_edge, tr = indice_shapely()
    random.seed(SEME2)
    campione8 = random.sample([s for s in segnali_el if s["a2"] is not None], 8)
    righe.append("6) a2 rifatto con shapely in EPSG:32632 e indice STRtree (metodo diverso)")
    tutti_ok = True
    for s in campione8:
        d, info, tid, esito = trova_strada_shapely(albero, linee, tratte_edge, tr, per_id,
                                                   s["lat"], s["lon"])
        if info is None:
            a2 = None
        else:
            a2 = min(5, info["punteggio_corr"] + (1 if info["asse_ingresso"] else 0))
        ok = (a2 == s["a2"] and (info or {}).get("nome") == s["a2_strada"]
              and esito == s["a2_esito"])
        tutti_ok = tutti_ok and ok
        righe.append(f"   {s['id_luogo']} {s['nome'][:32]:32s} a2 {a2} (file {s['a2']}), "
                     f"strada '{(info or {}).get('nome')}' (file '{s['a2_strada']}'), "
                     f"esito {esito} (file {s['a2_esito']}), {d:.1f} m -> {'OK' if ok else 'DIVERSO'}")
    righe.append(f"   esito: {'tutti uguali' if tutti_ok else 'ci sono differenze'}")
    righe.append("")

    print("7) universo rifatto con pandas...")
    zdf = pd.DataFrame(json.loads(ZONE.read_text(encoding="utf-8")))
    sdf = pd.DataFrame(segnali_el)
    m = sdf.merge(zdf[["cod", "macro"]], left_on="zona_imq", right_on="cod", how="left")
    n_univ = int(m["macro"].isin(MACRO_UNIVERSO).sum())
    scenari = json.loads(SCENARI.read_text(encoding="utf-8"))
    atteso_univ = scenari["n_universo"]
    righe.append("7) Numero di luoghi dell'universo, rifatto con pandas dalle zone IMQ")
    righe.append(f"   con pandas: {n_univ}; nel file scenari.json: {atteso_univ}; "
                 f"{'COINCIDONO' if n_univ == atteso_univ else 'NON COINCIDONO'}")
    righe.append("")

    print("8) zona centrale, forza e classe di 5 parcheggi...")
    funzione = {p["id"]: p for p in json.loads(FUNZIONE.read_text(encoding="utf-8"))["parcheggi"]}
    nodi_forti = [n for n in json.loads(NODI.read_text(encoding="utf-8"))["luoghi"] if n["nodo_forte"]]
    zone_pol, tr2 = zone_shapely()
    random.seed(SEME2)
    par5t = [p for p in parcheggi if p["id_5t"]]
    par_osm = [p for p in parcheggi if p["fonti"] == ["OSM"] and p["tipo"] == "osm_pubblico"]
    campione_par = random.sample(par5t, 3) + random.sample(par_osm, 2)
    righe.append("8) Zona centrale, punti a favore e classe di 5 parcheggi, rifatti a mano")
    righe.append("   (zona con shapely in EPSG:32632, punti a favore con i nodi forti, "
                 "strada con il metodo shapely)")
    tutti_ok = True
    for p in campione_par:
        f = funzione[p["id"]]
        x, y = tr2.transform(p["lon"], p["lat"])
        pt = Point(x, y)
        cod = None
        for c, pol in zone_pol:
            if pol.contains(pt):
                cod = c
                break
        centrale = cod in {f"Q{i:03d}" for i in range(1, 10)}
        d_nodo = min((haversine_m(p["lat"], p["lon"], n["lat"], n["lon"]) for n in nodi_forti),
                     default=None)
        nodo_vicino = d_nodo is not None and d_nodo <= 400
        n_vic = min(nodi_forti, key=lambda n: haversine_m(p["lat"], p["lon"], n["lat"], n["lon"])) \
            if nodi_forti else None
        ferro_metro = bool(nodo_vicino and n_vic["tipo_nodo"] in ("metro", "ferro", "capolinea"))
        _, info, tid, esito = trova_strada_shapely(albero, linee, tratte_edge, tr, per_id,
                                                   p["lat"], p["lon"])
        su_asse = bool((info or {}).get("asse_ingresso"))
        forza = int(nodo_vicino) + int(ferro_metro) + int(su_asse)
        if centrale:
            classe, motivo = "non_interscambio", "zona_centrale"
        elif p["tipo"] in ("interscambio_ufficiale", "park_ride_osm") and f["uso"] in (
                "residenziale", "destinazione", "misto", "dato_bloccato", "vuoto"):
            classe, motivo = "solo_sulla_carta", "dichiarato_non_usato"
        elif f["uso"] == "pendolare":
            classe, motivo = "interscambio_di_fatto", "uso_pendolare"
        elif f["uso"] in ("sconosciuto", "nessun_dato", "dati_insufficienti") and forza >= 1:
            classe, motivo = "potenziale", "punti_a_favore"
        elif f["uso"] in ("sconosciuto", "nessun_dato", "dati_insufficienti"):
            classe, motivo = "non_interscambio", "nessun_punto"
        else:
            classe, motivo = "non_interscambio", "firma_non_pendolare"
        ok = (classe == f["classe"] and forza == f["forza"] and centrale == f["zona_centrale"])
        tutti_ok = tutti_ok and ok
        righe.append(f"   {p['nome'][:28]:28s} zona {cod or '-'} (file {f['zona_imq']}), "
                     f"forza {forza} (file {f['forza']}), classe {classe} (file {f['classe']}), "
                     f"motivo {motivo} (file {f['motivo']}) -> {'OK' if ok else 'DIVERSO'}")
    righe.append(f"   esito: {'tutti uguali' if tutti_ok else 'ci sono differenze'}")
    righe.append("")

    print("9) soglia del 90° di S2 con numpy...")
    scen = scenari["scenari"]["S2"]
    chiavi = ["a1", "a2", "b2", "c1", "c2_ztl_completo", "d", "e"]
    istat = json.loads(ISTAT.read_text(encoding="utf-8"))
    completate = set(istat["zone_completate"])
    macro_zone = {z["cod"]: z["macro"] for z in json.loads(ZONE.read_text(encoding="utf-8"))}
    for s in segnali_el:
        s["c2_ztl_completo"] = s["c2_ztl"]
        z = istat["zone"].get(s["zona_imq"], {})
        if s["zona_imq"] in completate and z.get("c2_completo") is not None:
            s["c2_ztl_completo"] = round(z["c2_completo"] + (s["c3"] or 0.0), 1)
    if scenari.get("universo") == "tutto":
        univ = [s for s in segnali_el if s["zona_imq"]]
    else:
        univ = [s for s in segnali_el if macro_zone.get(s["zona_imq"]) in MACRO_UNIVERSO]
    perc = {}
    for k in chiavi:
        if k == "e":
            perc[k] = {s["id_luogo"]: float(s["e"]) for s in univ}
            continue
        vals = np.array([s[k] for s in univ if s.get(k) is not None], dtype=float)
        ids = [s["id_luogo"] for s in univ if s.get(k) is not None]
        r = rankdata(vals, method="average")
        p = 100.0 * (r - 1) / (len(vals) - 1) if len(vals) > 1 else np.full(len(vals), 100.0)
        perc[k] = dict(zip(ids, p))
    punteggi = {}
    for s in univ:
        v = [perc[k][s["id_luogo"]] for k in chiavi if s["id_luogo"] in perc[k]]
        punteggi[s["id_luogo"]] = float(np.mean(v)) if v else None
    vals = np.array(sorted(v for v in punteggi.values() if v is not None))
    idx = max(0, min(len(vals) - 1, round(0.9 * (len(vals) - 1))))
    soglia_np = float(vals[idx])
    diff = abs(soglia_np - scen["soglia"])
    righe.append("9) Soglia del 90° di S2, rifatta con numpy e rankdata sui soli luoghi dell'universo")
    righe.append(f"   numpy: {soglia_np:.2f}; scenari.json: {scen['soglia']:.2f}; "
                 f"differenza {diff:.4f} -> {'UGUALE' if diff <= 0.01 else 'DIVERSA'}")
    righe.append("")

    print("10) stato di git...")
    try:
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=RADICE,
                                capture_output=True, text=True).stdout.strip()
        stato = subprocess.run(["git", "status", "--short"], cwd=RADICE,
                               capture_output=True, text=True).stdout
        diff = subprocess.run(["git", "diff", "--name-only"], cwd=RADICE,
                              capture_output=True, text=True).stdout
        nuovi = [r[3:].strip() for r in stato.splitlines() if r.startswith("??")]
        alte = [r for r in stato.splitlines() if r and not r.startswith("??")]
        ultimo = subprocess.run(["git", "log", "-1", "--format=%h %ad %s", "--date=short"],
                                cwd=RADICE, capture_output=True, text=True).stdout.strip()
    except OSError as e:
        branch, stato, diff, nuovi, alte, ultimo = "-", "", "", [], [], f"errore: {e}"
    righe.append("10) Stato di git")
    righe.append(f"   ramo: {branch}; ultimo commit: {ultimo}")
    righe.append(f"   file TRACCIATI da git e modificati (git diff): {len([x for x in diff.splitlines() if x])}")
    for m in [x for x in diff.splitlines() if x]:
        righe.append(f"     modificato: {m}")
    righe.append(f"   file non tracciati (nuovi): {len(nuovi)}")
    for m in nuovi:
        righe.append(f"     nuovo: {m}")
    if alte:
        righe.append("   altre righe di stato git:")
        for m in alte:
            righe.append(f"     {m}")
    righe.append("")
    righe.append("   NOTA (giro 2): nessun commit e' stato fatto (decide Leo).")
    righe.append("   File MODIFICATI da questo giro (come previsto dal piano, regola 0.2):")
    righe.append("     scripts/71_parcheggi_riempimento.py, scripts/72_nodi_tp.py,")
    righe.append("     scripts/73_segnali_criticita.py, scripts/75_risultato6_v2.py,")
    righe.append("     scripts/76_verifiche_r6v2.py e i rapporti rigenerati dai lanci")
    righe.append("     (RAPPORTO_R6V2_RIEMPIMENTO/FUNZIONE/SEGNALI, RAPPORTO_RISULTATO6_V2).")
    righe.append("   File NUOVO di questo giro: scripts/77_strade_comuni.py e")
    righe.append("     docs/RAPPORTO_R6V2_STRADE.txt, docs/archivio/r6/ESITO_RISULTATO6_V2_GIRO2.md.")
    righe.append("   ATTENZIONE (non e' opera di questo giro): nella cartella di lavoro risultano")
    righe.append("     modificati anche MEMORIA_PROGETTO.md e docs/RAPPORTO_VELOCITA_5T.txt:")
    righe.append("     sono cambiamenti di un'altra sessione (nella notte del 19/10, insieme")
    righe.append("     all'aggiornamento del database). Questo giro non li ha toccati.")

    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print(f"Scritto: {RAPPORTO}")


if __name__ == "__main__":
    sys.exit(main())
