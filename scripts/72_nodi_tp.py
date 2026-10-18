#!/usr/bin/env python3
"""
72_nodi_tp.py  -  Risultato 6 v2, PASSI 4 e 5: nodi di trasporto e funzione dei parcheggi.

Cosa fa (Passo 4)
-----------------
Dal GTFS conta quante corse partono da ogni fermata in ogni ora del giorno feriale
2026-10-12, poi somma per LUOGO (gruppi di fermate vicine del Passo 1). Per ogni luogo
calcola:
  - b2 = corse/ora nelle ore dei pendolari (6-9 e 16-19);
  - b_giorno = corse/ora in tutta la giornata (6-20);
  - b1_luogo = somma delle corse/ora di punta della versione 1;
  - metro = il luogo ha una fermata della metropolitana (route_type = 1);
  - capolinea = dal luogo partono almeno 4 corse/ora fra le 6 e le 9 (prima fermata della corsa).
Dall'OpenStreetMap prende le stazioni dei treni e dice quali luoghi hanno una stazione
entro 300 m (ferro). Un luogo e' un "nodo forte" se ha metro o ferro o capolinea o b2 >= 20.

Cosa fa (Passo 5)
-----------------
Per ogni parcheggio aperto (non privato, non per clienti, non sosta lunga) dice quanto
fa davvero da interscambio: quanto e' vicino a un nodo forte, se e' su un asse di
ingresso, la sua firma di riempimento (Passo 3), i posti e la tariffa. Da qui una classe:
interscambio_di_fatto / solo_sulla_carta / potenziale / non_interscambio.

Cosa legge
----------
  data/raw/gtt_gtfs_20261003_224530.zip            (orari programmati)
  data/otp/rete/torino_cintura.osm.pbf             (stazioni dei treni)
  data/processed/risultato6_interscambio.json      (corse/ora di punta della v1)
  data/processed/risultato6_v2/luoghi.json         (Passo 1)
  data/processed/risultato6_v2/parcheggi.json      (Passo 2)
  data/processed/risultato6_v2/riempimento.json    (Passo 3)
  data/processed/traffico_d/rete/rete_auto.npz     (geometria delle strade)
  data/processed/traffico_d/assi_tratte.npz        (tratta di ogni tratto di strada)
  data/processed/traffico_d/tratte_traffico.json   (dati per tratta)
  data/processed/imq_zone_geo.json                 (zona IMQ, per "fuori centro")

Cosa scrive
-----------
  data/processed/risultato6_v2/nodi.json
  data/processed/risultato6_v2/parcheggi_funzione.json
  docs/RAPPORTO_R6V2_NODI.txt
  docs/RAPPORTO_R6V2_FUNZIONE.txt

Come si lancia
--------------
  python scripts\\72_nodi_tp.py --prova     (prime 400 fermate dei luoghi, controllo rapido)
  python scripts\\72_nodi_tp.py             (giro completo)
"""
import argparse
import csv
import io
import json
import math
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import osmium
from scipy.spatial import cKDTree

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
GTFS = RADICE / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"
PBF = RADICE / "data" / "otp" / "rete" / "torino_cintura.osm.pbf"
V1 = RADICE / "data" / "processed" / "risultato6_interscambio.json"
LUOGHI = RADICE / "data" / "processed" / "risultato6_v2" / "luoghi.json"
PARCHEGGI = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi.json"
RIEMPIMENTO = RADICE / "data" / "processed" / "risultato6_v2" / "riempimento.json"
ZONE_GEO = RADICE / "data" / "processed" / "imq_zone_geo.json"
RETE = RADICE / "data" / "processed" / "traffico_d" / "rete" / "rete_auto.npz"
ASSI = RADICE / "data" / "processed" / "traffico_d" / "assi_tratte.npz"
TRATTE = RADICE / "data" / "processed" / "traffico_d" / "tratte_traffico.json"
OUT_NODI = RADICE / "data" / "processed" / "risultato6_v2" / "nodi.json"
OUT_FUNZ = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi_funzione.json"
RAP_NODI = RADICE / "docs" / "RAPPORTO_R6V2_NODI.txt"
RAP_FUNZ = RADICE / "docs" / "RAPPORTO_R6V2_FUNZIONE.txt"

GIORNO_TIPO = "20261012"
GIORNI = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
ORE_PENDOLARI = (6, 7, 8, 9, 16, 17, 18, 19)
ORE_GIORNO = tuple(range(6, 21))
RAGGIO_FERRO_M = 300.0
SOGLIA_NODO_FREQUENTE = 20.0
RAGGIO_ASSE_M = 150.0
RAGGIO_NODO_PARCHEGGIO_M = 400.0
LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0
TIPI_ESCLUSI = ("privato", "clienti", "lungo_strada")


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def proietta(lon, lat):
    return (lon * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF)), lat * FATTORE_GRADI_M)


def dist_punto_segmento_m(px, py, ax, ay, bx, by):
    """Distanza in metri fra il punto (px,py) e il segmento (ax,ay)-(bx,by),
    tutti in coordinate piane in metri."""
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        t = 0.0
    else:
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy)


# --- Passo 4: GTFS -----------------------------------------------------------------------

def servizi_attivi(zf, giorno):
    import datetime
    data = datetime.date(int(giorno[:4]), int(giorno[4:6]), int(giorno[6:8]))
    colonna = GIORNI[data.weekday()]
    attivi = set()
    with zf.open("calendar.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r[colonna] == "1" and r["start_date"] <= giorno <= r["end_date"]:
                attivi.add(r["service_id"])
    try:
        with zf.open("calendar_dates.txt") as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                if r["date"] != giorno:
                    continue
                if r["exception_type"] == "1":
                    attivi.add(r["service_id"])
                elif r["exception_type"] == "2":
                    attivi.discard(r["service_id"])
    except KeyError:
        pass
    return attivi


def leggi_gtfs():
    """Ritorna (ore_per_fermata, prime_partenze, fermate_metro, fermate_gtfs)."""
    zf = zipfile.ZipFile(GTFS)
    attivi = servizi_attivi(zf, GIORNO_TIPO)
    print(f"  servizi attivi il {GIORNO_TIPO}: {len(attivi)}")

    tipo_route = {}
    with zf.open("routes.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            tipo_route[r["route_id"]] = r["route_type"]

    trip_route = {}
    with zf.open("trips.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            if r["service_id"] in attivi:
                trip_route[r["trip_id"]] = r["route_id"]
    print(f"  corse attive: {len(trip_route)}")

    fermate_gtfs = {}
    with zf.open("stops.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            try:
                fermate_gtfs[r["stop_id"]] = (float(r["stop_lat"]), float(r["stop_lon"]), r["stop_name"])
            except (TypeError, ValueError):
                continue

    ore = defaultdict(lambda: [0] * 24)
    prima_seq = {}
    prima_info = {}
    with zf.open("stop_times.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            tid = r["trip_id"]
            if tid not in trip_route:
                continue
            orario = r.get("departure_time") or r.get("arrival_time") or ""
            if not orario:
                continue
            try:
                ora = int(orario.split(":")[0]) % 24
            except ValueError:
                continue
            sid = r["stop_id"]
            ore[sid][ora] += 1
            try:
                seq = int(r["stop_sequence"])
            except ValueError:
                continue
            if tid not in prima_seq or seq < prima_seq[tid]:
                prima_seq[tid] = seq
                prima_info[tid] = (sid, ora)

    prime = defaultdict(lambda: [0] * 24)
    for tid, (sid, ora) in prima_info.items():
        prime[sid][ora] += 1

    fermate_metro = set()
    for tid, rid in trip_route.items():
        if tipo_route.get(rid) == "1":
            sid, _ = prima_info.get(tid, (None, None))
            if sid:
                fermate_metro.add(sid)
    with zf.open("stop_times.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            tid = r["trip_id"]
            if tid in trip_route and tipo_route.get(trip_route[tid]) == "1":
                fermate_metro.add(r["stop_id"])
    print(f"  fermate con metropolitana: {len(fermate_metro)}")
    return ore, prime, fermate_metro, fermate_gtfs


# --- Passo 4: stazioni dei treni da OSM ---------------------------------------------------

class Stazioni(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.trovate = []

    def _valuta(self, tag, lat, lon):
        if tag.get("railway") != "station" and not (
                tag.get("public_transport") == "station" and tag.get("train") == "yes"):
            return
        if tag.get("station") == "subway" or tag.get("subway") == "yes":
            return
        self.trovate.append({"nome": tag.get("name"), "lat": lat, "lon": lon})

    def node(self, n):
        self._valuta(n.tags, n.location.lat, n.location.lon)

    def way(self, w):
        if w.tags.get("railway") != "station" and not (
                w.tags.get("public_transport") == "station" and w.tags.get("train") == "yes"):
            return
        if w.tags.get("station") == "subway" or w.tags.get("subway") == "yes":
            return
        punti = [(nd.location.lat, nd.location.lon) for nd in w.nodes if nd.location.valid()]
        if not punti:
            return
        self._valuta(w.tags, sum(p[0] for p in punti) / len(punti),
                     sum(p[1] for p in punti) / len(punti))


def carica_stazioni():
    h = Stazioni()
    h.apply_file(str(PBF), locations=True)
    return h.trovate


# --- Passo 5: assi di ingresso e strade ---------------------------------------------------

def carica_strade():
    rete = np.load(RETE)
    edge_pts = rete["edge_pts"]
    edge_off = rete["edge_off"]
    assi = np.load(ASSI)
    edge_tratta = assi["edge_tratta"]
    tratte = json.loads(TRATTE.read_text(encoding="utf-8"))["tratte"]
    per_id = {t["id"]: t for t in tratte}
    comuni_asse = defaultdict(set)
    nome_asse = {}
    for t in tratte:
        comuni_asse[t["asse"]].add(t["comune"])
        nome_asse.setdefault(t["asse"], t.get("nome"))
    assi_ingresso = {a for a, cs in comuni_asse.items() if "Torino" in cs and len(cs) > 1}
    # albero dei punti estremi per trovare in fretta i tratti vicini
    px = np.empty(len(edge_pts))
    py = np.empty(len(edge_pts))
    px[:] = edge_pts[:, 1] * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF))
    py[:] = edge_pts[:, 0] * FATTORE_GRADI_M
    albero = cKDTree(np.column_stack([px, py]))
    punto_edge = np.zeros(len(edge_pts), dtype=np.int64)
    for e in range(len(edge_off) - 1):
        punto_edge[edge_off[e]:edge_off[e + 1]] = e
    return {"edge_pts": edge_pts, "edge_off": edge_off, "edge_tratta": edge_tratta,
            "per_id": per_id, "assi_ingresso": assi_ingresso, "nome_asse": nome_asse,
            "albero": albero, "punto_edge": punto_edge, "comuni_asse": comuni_asse}


def strada_piu_vicina(lat, lon, strade, raggio_m=RAGGIO_ASSE_M):
    """(distanza_m, indice_tratto) del tratto stradale piu' vicino entro raggio_m."""
    x, y = proietta(lon, lat)
    idx = strade["albero"].query_ball_point([x, y], raggio_m)
    if not idx:
        return None, None
    candidati = set(int(strade["punto_edge"][i]) for i in idx)
    migliore = (raggio_m, None)
    for e in candidati:
        pts = strade["edge_pts"][strade["edge_off"][e]:strade["edge_off"][e + 1]]
        for i in range(len(pts) - 1):
            ax, ay = proietta(pts[i][1], pts[i][0])
            bx, by = proietta(pts[i + 1][1], pts[i + 1][0])
            d = dist_punto_segmento_m(x, y, ax, ay, bx, by)
            if d < migliore[0]:
                migliore = (d, e)
    return migliore


# --- zone IMQ ---------------------------------------------------------------------------

def dentro_poligono(lat, lon, anelli):
    for anello in anelli:
        n = len(anello)
        dentro = False
        j = n - 1
        for i in range(n):
            yi, xi = anello[i]
            yj, xj = anello[j]
            if ((yi > lat) != (yj > lat)) and (
                lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-15) + xi
            ):
                dentro = not dentro
            j = i
        if dentro:
            return True
    return False


def carica_zone_imq():
    geo = json.loads(ZONE_GEO.read_text(encoding="utf-8"))
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
        lat_min = min(p[0] for anello in anelli for p in anello)
        lat_max = max(p[0] for anello in anelli for p in anello)
        lon_min = min(p[1] for anello in anelli for p in anello)
        lon_max = max(p[1] for anello in anelli for p in anello)
        zone.append({"cod": z["cod"], "anelli": anelli,
                     "bbox": (lat_min, lon_min, lat_max, lon_max)})
    return zone


def zona_di(lat, lon, zone):
    for z in zone:
        lat_min, lon_min, lat_max, lon_max = z["bbox"]
        if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
            continue
        if dentro_poligono(lat, lon, z["anelli"]):
            return z["cod"]
    return None


# --- main --------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", action="store_true",
                    help="limita i luoghi alle fermate delle prime 400 fermate per stop_id")
    args = ap.parse_args()

    for p in (GTFS, PBF, V1, LUOGHI, PARCHEGGI, RIEMPIMENTO, RETE, ASSI, TRATTE, ZONE_GEO):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    dati_v1 = json.loads(V1.read_text(encoding="utf-8"))
    corse_punta_v1 = {f["stop_id"]: f.get("corse_ora_punta", 0) for f in dati_v1["fermate"]}
    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    if args.prova:
        stop_prova = set(sorted(corse_punta_v1)[:400])
        luoghi = [l for l in luoghi if set(l["stop_ids"]) & stop_prova]
        print(f"[--prova] luoghi con le prime 400 fermate: {len(luoghi)}")

    print("Passo 4: leggo il GTFS (corse per fermata e ora)...")
    ore, prime, fermate_metro, fermate_gtfs = leggi_gtfs()

    print("Passo 4: leggo le stazioni dei treni da OpenStreetMap...")
    stazioni = carica_stazioni()
    print(f"  stazioni trovate: {len(stazioni)}")

    print("Passo 4: calcolo i segnali per luogo...")
    nodi = []
    for l in luoghi:
        tot = [0] * 24
        prim = [0] * 24
        for sid in l["stop_ids"]:
            v = ore.get(sid)
            if v:
                for h in range(24):
                    tot[h] += v[h]
            w = prime.get(sid)
            if w:
                for h in range(24):
                    prim[h] += w[h]
        b2 = sum(tot[h] for h in ORE_PENDOLARI) / len(ORE_PENDOLARI)
        b_giorno = sum(tot[h] for h in ORE_GIORNO) / len(ORE_GIORNO)
        b1_luogo = sum(corse_punta_v1.get(sid, 0) for sid in l["stop_ids"])
        metro = any(sid in fermate_metro for sid in l["stop_ids"])
        capolinea = sum(prim[h] for h in (6, 7, 8, 9)) / 4.0 >= 4.0
        ferro = any(haversine_m(l["lat"], l["lon"], s["lat"], s["lon"]) <= RAGGIO_FERRO_M
                    for s in stazioni)
        forte = metro or ferro or capolinea or b2 >= SOGLIA_NODO_FREQUENTE
        tipo_nodo = "metro" if metro else ("ferro" if ferro else (
            "capolinea" if capolinea else ("frequente" if b2 >= SOGLIA_NODO_FREQUENTE else None)))
        nodi.append({
            "id_luogo": l["id_luogo"], "nome": l["nome"], "lat": l["lat"], "lon": l["lon"],
            "zona_imq": l["zona_imq"], "in_centro": l["in_centro"], "n_fermate": l["n_fermate"],
            "b2_corse_ora_pendolari": round(b2, 3),
            "b_giorno_corse_ora": round(b_giorno, 3),
            "b1_luogo": b1_luogo,
            "metro": metro, "ferro": ferro, "capolinea": capolinea,
            "nodo_forte": forte, "tipo_nodo": tipo_nodo,
        })
    n_forti = sum(1 for n in nodi if n["nodo_forte"])

    print("Passo 5: calcolo gli assi di ingresso e le strade...")
    strade = carica_strade()
    print(f"  assi di ingresso (Torino + almeno un altro comune): {len(strade['assi_ingresso'])}")

    parcheggi = json.loads(PARCHEGGI.read_text(encoding="utf-8"))["parcheggi"]
    riemp = {r["id_5t"]: r for r in json.loads(RIEMPIMENTO.read_text(encoding="utf-8"))["parcheggi"]}
    zone = carica_zone_imq()

    print("Passo 5: calcolo posizione, uso e classe di ogni parcheggio...")
    nodi_forti = [n for n in nodi if n["nodo_forte"]]
    funzione = []
    for p in parcheggi:
        if p["tipo"] in TIPI_ESCLUSI:
            continue
        d_nodo, n_vicino = None, None
        for n in nodi_forti:
            dd = haversine_m(p["lat"], p["lon"], n["lat"], n["lon"])
            if d_nodo is None or dd < d_nodo:
                d_nodo, n_vicino = dd, n
        d_asse, edge = strada_piu_vicina(p["lat"], p["lon"], strade)
        su_asse = None
        nome_asse = None
        if edge is not None:
            tid = int(strade["edge_tratta"][edge])
            t = strade["per_id"].get(tid) if tid >= 0 else None
            if t is not None:
                su_asse = t["asse"] in strade["assi_ingresso"]
                nome_asse = t.get("nome")
        cod_zona = zona_di(p["lat"], p["lon"], zone)
        fuori_centro = cod_zona != "Q001"
        posizione_buona = bool(d_nodo is not None and d_nodo <= RAGGIO_NODO_PARCHEGGIO_M
                               and fuori_centro)
        r = riemp.get(p["id_5t"]) if p["id_5t"] else None
        uso = r["firma"] if r else "sconosciuto"
        posti = p["posti_dichiarati"] or p["posti_stimati"]
        if posizione_buona and uso == "pendolare":
            classe = "interscambio_di_fatto"
        elif p["tipo"] in ("interscambio_ufficiale", "park_ride_osm") and (
                uso in ("residenziale", "destinazione", "misto", "dato_bloccato")
                or (r and r["stato"] == "vuoto")):
            classe = "solo_sulla_carta"
        elif posizione_buona and uso in ("sconosciuto", "nessun_dato", "dati_insufficienti"):
            classe = "potenziale"
        else:
            classe = "non_interscambio"
        funzione.append({
            "id": p["id"], "nome": p["nome"], "tipo": p["tipo"],
            "lat": p["lat"], "lon": p["lon"],
            "dist_nodo_forte_m": round(d_nodo) if d_nodo is not None else None,
            "tipo_nodo": n_vicino["tipo_nodo"] if n_vicino else None,
            "zona_imq": cod_zona, "fuori_centro": fuori_centro,
            "posizione_buona": posizione_buona,
            "su_asse_ingresso": su_asse,
            "asse_ingresso_nome": nome_asse,
            "uso": uso, "posti": posti, "a_pagamento": p["a_pagamento"],
            "classe": classe,
        })

    OUT_NODI.parent.mkdir(parents=True, exist_ok=True)
    OUT_NODI.write_text(json.dumps({
        "giorno_tipo": GIORNO_TIPO,
        "ore_pendolari": list(ORE_PENDOLARI),
        "assi_ingresso": sorted(strade["assi_ingresso"]),
        "nomi_assi_ingresso": {str(a): strade["nome_asse"].get(a) for a in sorted(strade["assi_ingresso"])},
        "stazioni": stazioni,
        "luoghi": nodi,
    }, ensure_ascii=False), encoding="utf-8")
    OUT_FUNZ.parent.mkdir(parents=True, exist_ok=True)
    OUT_FUNZ.write_text(json.dumps({"parcheggi": funzione}, ensure_ascii=False), encoding="utf-8")

    # --- rapporti ---
    n_tipi = Counter(n["tipo_nodo"] for n in nodi if n["nodo_forte"])
    righe = []
    righe.append("RAPPORTO R6 v2 — NODI DI TRASPORTO (Passo 4)")
    righe.append(f"modalita': {'PROVA' if args.prova else 'completa'}")
    righe.append(f"luoghi: {len(nodi)}; nodi forti: {n_forti}")
    righe.append("un luogo e' nodo forte se ha metro, o una stazione entro 300 m, o e' capolinea,"
                 f" o ha almeno {SOGLIA_NODO_FREQUENTE:.0f} corse/ora nelle ore dei pendolari")
    righe.append(f"  per tipo: {dict(n_tipi)}")
    righe.append(f"  con b2 >= 20 senza altro motivo (frequente): "
                 f"{sum(1 for n in nodi if n['tipo_nodo'] == 'frequente')}")
    righe.append("")
    righe.append("== Stazioni dei treni trovate in OpenStreetMap ==")
    for s in sorted(stazioni, key=lambda s: (s["nome"] or "")):
        righe.append(f"  {s['nome'] or '(senza nome)':35s} {s['lat']:.5f}, {s['lon']:.5f}")
    controllo = ("Porta Nuova", "Porta Susa", "Lingotto", "Stura", "Rebaudengo")
    nomi_st = " | ".join((s["nome"] or "") for s in stazioni)
    righe.append("")
    righe.append("== Controllo delle stazioni attese ==")
    for c in controllo:
        righe.append(f"  {c}: {'trovata' if c.lower() in nomi_st.lower() else 'NON TROVATA'}")
    metro_luoghi = [n for n in nodi if n["metro"]]
    righe.append("")
    righe.append("== Luoghi con la metropolitana ==")
    righe.append(f"  totale: {len(metro_luoghi)}")
    for n in sorted(metro_luoghi, key=lambda n: n["nome"]):
        righe.append(f"  {n['nome'][:45]:45s} zona={n['zona_imq'] or '-'} b2={n['b2_corse_ora_pendolari']:.1f} "
                     f"tipo={n['tipo_nodo']}")
    righe.append("")
    righe.append("== Primi 25 nodi forti per corse/ora pendolari ==")
    for n in sorted(nodi, key=lambda n: -n["b2_corse_ora_pendolari"])[:25]:
        righe.append(f"  {n['b2_corse_ora_pendolari']:6.1f}  {n['nome'][:45]:45s} zona={n['zona_imq'] or '-':5s} "
                     f"{n['tipo_nodo'] or '-'}{' (NON forte)' if not n['nodo_forte'] else ''}")
    RAP_NODI.parent.mkdir(parents=True, exist_ok=True)
    RAP_NODI.write_text("\n".join(righe) + "\n", encoding="utf-8")

    conteggi = Counter(f["classe"] for f in funzione)
    posti_per_classe = Counter()
    for f in funzione:
        posti_per_classe[f["classe"]] += f["posti"] or 0
    righe = []
    righe.append("RAPPORTO R6 v2 — QUANTO OGNI PARCHEGGIO FA DA INTERSCAMBIO (Passo 5)")
    righe.append(f"parcheggi considerati (esclusi privati, per clienti e sosta lunga): {len(funzione)}")
    righe.append("  interscambio_di_fatto = posizione buona e uso pendolare")
    righe.append("  solo_sulla_carta    = dichiarato interscambio/park&ride ma uso non da pendolari")
    righe.append("  potenziale          = posizione buona ma uso sconosciuto o senza dati")
    righe.append("  non_interscambio    = tutto il resto")
    righe.append("")
    righe.append("== Quanti parcheggi e quanti posti per classe ==")
    for c in ("interscambio_di_fatto", "solo_sulla_carta", "potenziale", "non_interscambio"):
        righe.append(f"  {c:22s} {conteggi.get(c, 0):5d} parcheggi   posti {posti_per_classe.get(c, 0):6d}")
    righe.append("")
    righe.append("== I 5 interscambi ufficiali e i garage 5T ==")
    righe.append("  nome | tipo | dist. nodo forte | tipo nodo | su asse ingresso | firma | tariffa | classe")
    for f in sorted(funzione, key=lambda f: (f["tipo"] != "interscambio_ufficiale", f["tipo"], f["nome"])):
        if f["tipo"] not in ("interscambio_ufficiale", "garage_5t"):
            continue
        righe.append(f"  {f['nome'][:24]:24s} {f['tipo'][:22]:22s} "
                     f"{str(f['dist_nodo_forte_m']):>6} m {str(f['tipo_nodo'] or '-'):10s} "
                     f"{str(f['su_asse_ingresso']):5s} {f['uso']:18s} {str(f['a_pagamento']):6s} {f['classe']}")
    righe.append("")
    righe.append("== I 20 'potenziale' con piu' posti ==")
    potenziali = sorted([f for f in funzione if f["classe"] == "potenziale"],
                        key=lambda f: -(f["posti"] or 0))[:20]
    for f in potenziali:
        righe.append(f"  {str(f['posti'] or '-'):>5} posti  {f['nome'][:34]:34s} {f['tipo'][:14]:14s} "
                     f"{str(f['dist_nodo_forte_m']):>5} m da {str(f['tipo_nodo'] or '-'):10s} "
                     f"tariffa={f['a_pagamento']} uso={f['uso']}")
    RAP_FUNZ.parent.mkdir(parents=True, exist_ok=True)
    RAP_FUNZ.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT_NODI}")
    print(f"Scritto: {OUT_FUNZ}")
    print(f"Scritto: {RAP_NODI}")
    print(f"Scritto: {RAP_FUNZ}")
    print(f"nodi forti: {n_forti} su {len(nodi)}; tipi: {dict(n_tipi)}")
    print(f"classi parcheggi: {dict(conteggi)}")
    for nome in ("VENCHI UNICA", "SOFIA", "FERMI"):
        f = next((x for x in funzione if x["nome"] == nome), None)
        if f:
            print(f"  {nome}: {f['classe']} (uso={f['uso']}, dist={f['dist_nodo_forte_m']} m, "
                  f"tipo_nodo={f['tipo_nodo']}, fuori_centro={f['fuori_centro']})")


if __name__ == "__main__":
    sys.exit(main())
