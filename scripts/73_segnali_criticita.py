#!/usr/bin/env python3
"""
73_segnali_criticita.py  -  Risultato 6 v2, PASSO 6: i segnali di criticita' per luogo.

Cosa fa
-------
Per ogni LUOGO (gruppi di fermate del Passo 1) calcola i segnali grezzi di criticita':
  a1 - importanza del corridoio piu' vicino (dalla versione 1)
  a2 - importanza della strada dal lavoro sul traffico (+1 se e' un asse di ingresso a Torino)
  b1 - corse/ora di punta della versione 1 (sommate sul luogo)
  b2 - corse/ora nelle ore dei pendolari (dal Passo 4)
  c1 - pendolari IMQ della zona (come la versione 1)
  c2 - auto che entrano a Torino al mattino (microdati IMQ 2022)
  c3 - di quelle, quelle dirette in una zona dentro la ZTL centrale
  c2_ztl - c2 + c3 (chi va in ZTL al mattino conta doppio)
  d  - calo di velocita' all'ingresso (sensori 5T: ore di punta contro ore di notte)
  e  - il luogo ha metropolitana o stazione dei treni
  f  - auto che gia' oggi lasciano l'auto per un mezzo pubblico (solo informazione)
I valori grezzi qui; i percentili si fanno al Passo 8.

Cosa legge
----------
  data/processed/risultato6_interscambio.json       (v1)
  data/processed/risultato6_v2/luoghi.json          (Passo 1)
  data/processed/risultato6_v2/nodi.json            (Passo 4)
  data/processed/imq_od.json                        (pendolari per zona, v1)
  data/processed/imq/spostamenti.csv                (microdati IMQ 2022)
  data/processed/velocita_5t.json                   (calo di velocita' 5T)
  data/processed/traffico_d/...                     (strade, tratte, assi di ingresso)
  data/processed/traffico_d/ztl_unificata.json      (ZTL centrale)
  data/processed/imq_zone_geo.json                  (poligoni delle zone IMQ)

Cosa scrive
-----------
  data/processed/risultato6_v2/segnali.json
  docs/RAPPORTO_R6V2_SEGNALI.txt

Come si lancia
--------------
  python scripts\\73_segnali_criticita.py --prova   (prime 400 fermate, controllo rapido)
  python scripts\\73_segnali_criticita.py           (giro completo)
"""
import csv
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import argparse
import numpy as np
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
NODI = RADICE / "data" / "processed" / "risultato6_v2" / "nodi.json"
IMQ_OD = RADICE / "data" / "processed" / "imq_od.json"
SPOSTAMENTI = RADICE / "data" / "processed" / "imq" / "spostamenti.csv"
VELOCITA = RADICE / "data" / "processed" / "velocita_5t.json"
RETE = RADICE / "data" / "processed" / "traffico_d" / "rete" / "rete_auto.npz"
ASSI = RADICE / "data" / "processed" / "traffico_d" / "assi_tratte.npz"
TRATTE = RADICE / "data" / "processed" / "traffico_d" / "tratte_traffico.json"
ZTL = RADICE / "data" / "processed" / "traffico_d" / "ztl_unificata.json"
ZONE_GEO = RADICE / "data" / "processed" / "imq_zone_geo.json"
OUT = RADICE / "data" / "processed" / "risultato6_v2" / "segnali.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_SEGNALI.txt"

RAGGIO_STRADA_M = 150.0
RAGGIO_SENSORE_M = 300.0
QUOTA_ZTL = 0.10
LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0
MIN_INTERVISTE = 30
TOTALE_ATTESO_C2 = 95300.0
TOTALE_ATTESO_F = 24500.0


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def proietta(lon, lat):
    return (lon * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF)), lat * FATTORE_GRADI_M)


def minuti(orario):
    if not orario:
        return None
    try:
        h, m = orario.strip().split(":")
        return int(h) * 60 + int(m)
    except ValueError:
        return None


def peso(x):
    v = (x.get("PESO") or "").replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return 0.0


# --- c1: pendolari per zona (copia fedele dalla versione 1, script 25) --------------------

def punteggio_pendolari_per_zona():
    d = json.loads(IMQ_OD.read_text(encoding="utf-8"))
    od = d["od"]["tot"]
    punteggio = {}
    for o, dst, val, n, flag in od:
        if not o or not dst:
            continue
        o_torino, d_torino = o.startswith("Q"), dst.startswith("Q")
        if o_torino == d_torino:
            continue
        punteggio[o] = punteggio.get(o, 0.0) + val
        punteggio[dst] = punteggio.get(dst, 0.0) + val
    return punteggio


# --- a2: strade -------------------------------------------------------------------------

def carica_strade():
    rete = np.load(RETE)
    edge_pts = rete["edge_pts"]
    edge_off = rete["edge_off"]
    edge_tratta = np.load(ASSI)["edge_tratta"]
    tratte = json.loads(TRATTE.read_text(encoding="utf-8"))["tratte"]
    per_id = {t["id"]: t for t in tratte}
    from scipy.spatial import cKDTree
    px = edge_pts[:, 1] * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF))
    py = edge_pts[:, 0] * FATTORE_GRADI_M
    albero = cKDTree(np.column_stack([px, py]))
    punto_edge = np.zeros(len(edge_pts), dtype=np.int64)
    for e in range(len(edge_off) - 1):
        punto_edge[edge_off[e]:edge_off[e + 1]] = e
    return {"edge_pts": edge_pts, "edge_off": edge_off, "edge_tratta": edge_tratta,
            "per_id": per_id, "albero": albero, "punto_edge": punto_edge}


def dist_punto_segmento_m(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        t = 0.0
    else:
        t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy)


def strada_piu_vicina(lat, lon, strade, raggio_m=RAGGIO_STRADA_M):
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


# --- d: calo di velocita' ---------------------------------------------------------------

def cali_sensori():
    dati = json.loads(VELOCITA.read_text(encoding="utf-8"))
    cali = {}
    for lcd, s in dati["sensori"].items():
        celle = (s.get("celle") or {}).get("0")
        if not celle:
            continue
        v_notte = [celle[str(h)]["v"] for h in (2, 3, 4)
                   if str(h) in celle and celle[str(h)].get("ok")]
        v_punta = [celle[str(h)]["v"] for h in (7, 8)
                   if str(h) in celle and celle[str(h)].get("ok")]
        if len(v_notte) < 2 or len(v_punta) < 2:
            continue
        mn = sum(v_notte) / len(v_notte)
        mp = sum(v_punta) / len(v_punta)
        if mn <= 0:
            continue
        cali[lcd] = {"via": s.get("via"), "lat": s["lat"], "lon": s["lon"],
                     "v_notte": round(mn, 1), "v_punta": round(mp, 1),
                     "calo": round(1 - mp / mn, 4)}
    return cali


# --- c2 / c3: microdati IMQ -------------------------------------------------------------

def zone_c2_c3():
    righe = list(csv.DictReader(SPOSTAMENTI.open(encoding="utf-8-sig"), delimiter=";"))
    c2 = defaultdict(float)
    c2_int = defaultdict(int)
    c3 = defaultdict(float)
    totale_c2 = 0.0
    n_c2 = 0
    for x in righe:
        if x["MEZZO1"] not in ("03", "04", "21"):
            continue
        par = x["COD_PAR"].strip()
        arr = x["COD_ARR"].strip()
        if not par or par.startswith("Q"):
            continue
        if not arr.startswith("Q"):
            continue
        mp = minuti(x["ORA_PAR"])
        if mp is None or not (360 <= mp <= 599):
            continue
        p = peso(x)
        totale_c2 += p
        n_c2 += 1
        for z in (par, arr):
            c2[z] += p
            c2_int[z] += 1
    return righe, c2, c2_int, c3, totale_c2, n_c2


def quota_ztl_zone(zone_ztl):
    """Quali zone IMQ hanno almeno il 10% della superficie dentro la ZTL centrale."""
    geo = json.loads(ZONE_GEO.read_text(encoding="utf-8"))
    ztl = json.loads(ZTL.read_text(encoding="utf-8"))
    poligoni_ztl = []
    for z in ztl["zone"]:
        if z["nome"] == "centrale":
            for anello in z["poligoni"]:
                punti = [proietta(p[0], p[1]) for p in anello]
                if len(punti) >= 3:
                    poligoni_ztl.append(Polygon(punti).buffer(0))
    quota = {}
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
        try:
            pol = Polygon([proietta(p[1], p[0]) for p in anelli[0]]).buffer(0)
        except (ValueError, IndexError):
            continue
        if pol.area <= 0:
            continue
        inter = 0.0
        for pz in poligoni_ztl:
            if pol.intersects(pz):
                inter = max(inter, pol.intersection(pz).area)
        quota[z["cod"]] = inter / pol.area
    return quota


def zone_ztl_da_righe(righe, zone_ok):
    """c3: come c2 ma solo chi arriva in una zona con ZTL, fra 07:30 e 10:30."""
    c3 = defaultdict(float)
    n = 0
    tot = 0.0
    for x in righe:
        if x["MEZZO1"] not in ("03", "04", "21"):
            continue
        par = x["COD_PAR"].strip()
        arr = x["COD_ARR"].strip()
        if not par or par.startswith("Q") or not arr.startswith("Q"):
            continue
        mp = minuti(x["ORA_PAR"])
        if mp is None or not (360 <= mp <= 599):
            continue
        if arr not in zone_ok:
            continue
        ma = minuti(x["ORA_ARR"])
        if ma is None or not (450 <= ma <= 630):
            continue
        p = peso(x)
        tot += p
        n += 1
        for z in (par, arr):
            c3[z] += p
    return c3, tot, n


# --- f: auto che lasciano l'auto --------------------------------------------------------

MEZZI_PUBBLICI = ("06", "07", "08", "09", "12", "13", "19", "22")


def segnale_f(righe):
    tot = 0.0
    n = 0
    per_secondo = defaultdict(float)
    per_secondo_n = defaultdict(int)
    cambio = defaultdict(int)
    senza_cambio = 0
    for x in righe:
        if x["MEZZO1"] not in ("03", "04", "05", "21"):
            continue
        successivi = [m.strip() for m in (x["MEZZO2"], x["MEZZO3"])]
        primo = next((m for m in successivi if m in MEZZI_PUBBLICI), None)
        if primo is None:
            continue
        p = peso(x)
        tot += p
        n += 1
        per_secondo[primo] += p
        per_secondo_n[primo] += 1
        z = (x.get("COD_2M") or "").strip()
        if z:
            cambio[z] += 1
        else:
            senza_cambio += 1
    return {"totale": tot, "n": n, "per_secondo": per_secondo,
            "per_secondo_n": per_secondo_n, "cambio": cambio, "senza_cambio": senza_cambio}


# --- main -------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", action="store_true",
                    help="solo i luoghi delle prime 400 fermate per stop_id, per un controllo rapido")
    args = ap.parse_args()

    for p in (V1, LUOGHI, NODI, IMQ_OD, SPOSTAMENTI, VELOCITA, RETE, ASSI, TRATTE, ZTL, ZONE_GEO):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    print("carico i luoghi e i nodi...")
    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    nodi = {n["id_luogo"]: n for n in json.loads(NODI.read_text(encoding="utf-8"))["luoghi"]}

    dati_v1 = {f["stop_id"]: f for f in json.loads(V1.read_text(encoding="utf-8"))["fermate"]}
    if args.prova:
        stop_prova = set(sorted(dati_v1)[:400])
        luoghi = [l for l in luoghi if set(l["stop_ids"]) & stop_prova]
        print(f"[--prova] luoghi con le prime 400 fermate: {len(luoghi)}")
    print("c1: pendolari per zona (formula della v1)...")
    pend_zona = punteggio_pendolari_per_zona()

    print("c2: auto in entrata al mattino dai microdati IMQ...")
    righe, c2, c2_int, _c3, totale_c2, n_c2 = zone_c2_c3()
    print(f"  spostamenti: {totale_c2:.0f} ({n_c2} interviste)")
    if abs(totale_c2 - TOTALE_ATTESO_C2) / TOTALE_ATTESO_C2 > 0.02:
        sys.exit(f"c2 fuori dall'atteso (~{TOTALE_ATTESO_C2:.0f}): {totale_c2:.0f} — FERMO")

    print("c3: ZTL centrale — quali zone IMQ la contengono...")
    quota = quota_ztl_zone(None)
    zone_ok = {z for z, q in quota.items() if q >= QUOTA_ZTL}
    print(f"  zone con almeno il {QUOTA_ZTL:.0%} dentro la ZTL centrale: {sorted(zone_ok)}")
    c3, tot_c3, n_c3 = zone_ztl_da_righe(righe, zone_ok)
    print(f"  spostamenti verso quelle zone 07:30-10:30: {tot_c3:.0f} ({n_c3} interviste)")

    print("f: auto che lasciano l'auto per un mezzo pubblico...")
    f = segnale_f(righe)
    print(f"  totale {f['totale']:.0f} ({f['n']} interviste)")
    if abs(f["totale"] - TOTALE_ATTESO_F) / TOTALE_ATTESO_F > 0.05:
        print(f"  ATTENZIONE: diverso dall'atteso ~{TOTALE_ATTESO_F:.0f}")

    print("d: calo di velocita' dai sensori 5T...")
    cali = cali_sensori()
    print(f"  sensori usabili: {len(cali)}")

    print("a2: strade e assi di ingresso...")
    strade = carica_strade()
    assi_ingresso = set(json.loads(NODI.read_text(encoding="utf-8"))["assi_ingresso"])

    print("calcolo i segnali di tutti i luoghi...")
    sensori = [(c["lat"], c["lon"], lcd, c["calo"]) for lcd, c in cali.items()]
    segnali = []
    for l in luoghi:
        sid = l["stop_ids"]
        a1 = max((dati_v1[s]["punteggio_corridoio"] for s in sid if s in dati_v1), default=None)
        node = nodi.get(l["id_luogo"], {})
        b1 = node.get("b1_luogo")
        b2 = node.get("b2_corse_ora_pendolari")
        zona = l["zona_imq"]
        c1 = pend_zona.get(zona) if zona else None
        c2z = c2.get(zona) if zona else None
        c3z = c3.get(zona) if zona else None
        c2_ztl = (c2z + (c3z or 0.0)) if c2z is not None else None
        interviste = c2_int.get(zona, 0) if zona else 0

        d_asse, edge = strada_piu_vicina(l["lat"], l["lon"], strade)
        a2 = None
        asse_ing = None
        if edge is not None:
            tid = int(strade["edge_tratta"][edge])
            t = strade["per_id"].get(tid) if tid >= 0 else None
            if t is not None:
                asse_ing = t["asse"] in assi_ingresso
                a2 = min(5, t["punteggio"] + (1 if asse_ing else 0))
        d = None
        if sensori:
            vicini = [calo for (slat, slon, lcd, calo) in sensori
                      if haversine_m(l["lat"], l["lon"], slat, slon) <= RAGGIO_SENSORE_M]
            d = round(max(vicini), 4) if vicini else None

        segnali.append({
            "id_luogo": l["id_luogo"], "nome": l["nome"], "lat": l["lat"], "lon": l["lon"],
            "zona_imq": zona, "in_centro": l["in_centro"], "n_fermate": l["n_fermate"],
            "critico_v1": l["critico_v1"], "coperto_v1": l["coperto_v1"],
            "a1": a1, "a2": a2, "asse_ingresso": asse_ing,
            "b1": b1, "b2": b2,
            "c1": round(c1, 1) if c1 is not None else None,
            "c2": round(c2z, 1) if c2z is not None else None,
            "c2_interviste": interviste,
            "c2_scarso": bool(zona) and interviste < MIN_INTERVISTE,
            "c3": round(c3z, 1) if c3z is not None else None,
            "c2_ztl": round(c2_ztl, 1) if c2_ztl is not None else None,
            "d": d,
            "e": 100 if (node.get("metro") or node.get("ferro")) else 0,
            "metro": bool(node.get("metro")), "ferro": bool(node.get("ferro")),
            "mancante": [k for k in ("a1", "a2", "b1", "b2", "c1", "c2", "c2_ztl", "d")
                         if {"a1": a1, "a2": a2, "b1": b1, "b2": b2, "c1": c1, "c2": c2z,
                             "c2_ztl": c2_ztl, "d": d}[k] is None],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "c2_totale": round(totale_c2, 1), "c2_interviste": n_c2,
        "c3_totale": round(tot_c3, 1), "c3_interviste": n_c3,
        "zone_ztl": sorted(zone_ok), "quota_ztl_per_zona": {k: round(v, 3) for k, v in quota.items()},
        "f": {"totale": round(f["totale"], 1), "n": f["n"],
              "per_secondo": {k: round(v, 1) for k, v in f["per_secondo"].items()},
              "cambio": dict(f["cambio"]), "senza_cambio": f["senza_cambio"]},
        "sensori_usati": cali,
        "luoghi": segnali,
    }, ensure_ascii=False), encoding="utf-8")

    # --- rapporto ---
    righe_rep = []
    righe_rep.append("RAPPORTO R6 v2 — SEGNALI DI CRITICITA' PER LUOGO (Passo 6)")
    righe_rep.append(f"luoghi: {len(segnali)}")
    righe_rep.append("")
    righe_rep.append("== Per ogni segnale: quanti luoghi lo hanno, minimo, mediana, massimo ==")
    def riassunto(nome, chiave):
        vals = [s[chiave] for s in segnali if s.get(chiave) is not None]
        if not vals:
            righe_rep.append(f"  {nome:6s} nessun luogo")
            return
        righe_rep.append(f"  {nome:6s} {len(vals):5d} luoghi   min {min(vals):10.2f}   "
                         f"mediana {statistics.median(vals):10.2f}   max {max(vals):10.2f}")
    for nome, chiave in (("a1", "a1"), ("a2", "a2"), ("b1", "b1"), ("b2", "b2"),
                         ("c1", "c1"), ("c2", "c2"), ("c3", "c3"), ("c2_ztl", "c2_ztl"),
                         ("d", "d"), ("e", "e")):
        riassunto(nome, chiave)
    righe_rep.append("")
    righe_rep.append("== I 10 luoghi piu' alti per ogni segnale ==")
    for nome, chiave in (("a2", "a2"), ("b2", "b2"), ("c2_ztl", "c2_ztl"), ("d", "d")):
        righe_rep.append(f"  -- {nome}")
        for s in sorted([s for s in segnali if s.get(chiave) is not None],
                        key=lambda s: -s[chiave])[:10]:
            righe_rep.append(f"     {s[chiave]:10.2f}  {s['nome'][:42]:42s} zona={s['zona_imq'] or '-'}")
    righe_rep.append("")
    righe_rep.append("== Segnali mancanti ==")
    conta_manc = Counter()
    for s in segnali:
        for m in s["mancante"]:
            conta_manc[m] += 1
    for m in ("a1", "a2", "b1", "b2", "c1", "c2", "c2_ztl", "d"):
        righe_rep.append(f"  {m:6s} mancante in {conta_manc.get(m, 0)} luoghi")
    righe_rep.append("")
    righe_rep.append("== c2 e c3 (auto in entrata al mattino, IMQ 2022) ==")
    righe_rep.append(f"  c2: {totale_c2:.0f} spostamenti al giorno, {n_c2} interviste")
    righe_rep.append(f"  c3: {tot_c3:.0f} spostamenti al giorno verso la ZTL centrale 07:30-10:30, {n_c3} interviste")
    righe_rep.append("  zone IMQ che stanno almeno per il 10% dentro la ZTL centrale:")
    for z in sorted(zone_ok):
        righe_rep.append(f"     {z}: {100 * quota[z]:.1f}% della superficie")
    n_scarso = sum(1 for s in segnali if s["c2_scarso"])
    righe_rep.append(f"  zone con meno di {MIN_INTERVISTE} interviste (c2 'scarso'): {n_scarso} luoghi "
                     f"(saranno completate al Passo 7)")
    righe_rep.append("")
    righe_rep.append("== d: sensori 5T usati e loro calo di velocita' ==")
    righe_rep.append("  calo = 1 - velocita' ore 7-8 / velocita' ore 2-4 (stesso punto, quindi "
                     "limiti e semafori non contano)")
    for lcd, c in sorted(cali.items(), key=lambda kv: -kv[1]["calo"]):
        righe_rep.append(f"  {c['via'][:38]:38s} notte {c['v_notte']:5.1f} km/h  punta {c['v_punta']:5.1f} km/h  "
                         f"calo {c['calo']:.2f}")
    righe_rep.append("")
    righe_rep.append("== f: auto che GIA' OGGI lasciano l'auto per un mezzo pubblico (solo informazione) ==")
    righe_rep.append("  NON entra nei punteggi [DATI SCARSI]")
    righe_rep.append(f"  totale: {f['totale']:.0f} spostamenti al giorno, {f['n']} interviste")
    righe_rep.append("  per secondo mezzo:")
    for k, v in sorted(f["per_secondo"].items(), key=lambda kv: -kv[1]):
        righe_rep.append(f"     codice {k}: {v:.0f} spostamenti ({f['per_secondo_n'][k]} interviste)")
    righe_rep.append(f"  zona del cambio non indicata (COD_2M vuoto): {f['senza_cambio']} su {f['n']} "
                     f"({100 * f['senza_cambio'] / f['n']:.0f}%)")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe_rep) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT}")
    print(f"Scritto: {RAPPORTO}")
    for m in ("a2", "d"):
        print(f"  {m}: mancante in {conta_manc.get(m, 0)} luoghi")
    print(f"  luoghi con metro o ferro: {sum(1 for s in segnali if s['e'] == 100)}")


if __name__ == "__main__":
    sys.exit(main())
