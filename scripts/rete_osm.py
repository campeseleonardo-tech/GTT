# -*- coding: utf-8 -*-
"""
scripts/rete_osm.py - rete stradale percorribile in auto ricavata dal taglio OSM
(data/otp/rete/torino_cintura.osm.pbf), per il metodo C del Risultato 8.

Perche' un grafo nostro e non r5py: il metodo C deve far passare ~milioni di
viaggi su TUTTA la rete e sommare i passaggi su ogni tratto. r5py serve a
calcolare percorsi puntuali (o matrici di tempi), non a fare un'assegnazione
di flusso su centinaia di origini: 500+ punti di partenza x 500+ di arrivo
sono centinaia di migliaia di percorsi da ricostruire, impraticabile.
Con un grafo in memoria + scipy.sparse.csgraph.dijkstra si calcola l'albero
dei cammini minimi una volta per ogni NODO di origine e i flussi si sommano
sull'albero con una somma di sottoalbero (vedi scripts/42_instradamento.py).

Cosa costruisce:
  - nodi = soli nodi "di giunzione" (fine di una strada o punto in comune fra
    due strade) piu' le estremita' di ogni way;
  - archi = tratti di way fra due nodi di giunzione, con lunghezza, tempo di
    percorrenza (da maxspeed OSM o da velocita' tipica per classe) e geometria
    completa (per abbinare i tratti ai corridoi e ai sensori);
  - ogni tratto e' un arco non orientato ("arco base") con 1 o 2 archi orientati
    (verso unico o doppio senso).

Non modifica nessun file del progetto se non quelli indicati in SALVA().
"""

import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

# --- classi di strada percorribili in auto e velocita' tipica (km/h) -------------
VELOCITA_DEFAULT = {
    "motorway": 120.0, "motorway_link": 60.0,
    "trunk": 100.0, "trunk_link": 60.0,
    "primary": 70.0, "primary_link": 50.0,
    "secondary": 60.0, "secondary_link": 40.0,
    "tertiary": 50.0, "tertiary_link": 35.0,
    "unclassified": 40.0, "residential": 30.0, "living_street": 15.0,
    "service": 20.0, "road": 30.0,
}
DRIVABILI = set(VELOCITA_DEFAULT)
# classi in cui, se manca il tag oneway, si assume senso unico (autostrade)
SENSO_UNICO_DEFAULT = {"motorway", "motorway_link", "trunk", "trunk_link"}

R_TERRA = 6371000.0


def haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_TERRA * math.asin(math.sqrt(a))


def parse_maxspeed(valore, default):
    """'50' -> 50; '30 mph' -> 48,3; 'IT:urban' -> default; 'walk' -> 7."""
    if valore is None:
        return default
    s = str(valore).strip().lower()
    if not s:
        return default
    if s in ("walk", "walking"):
        return 7.0
    if s in ("none", "signals", "variable"):
        return default
    m = re.search(r"\d+(?:[.,]\d+)?", s)
    if not m:
        return default
    v = float(m.group().replace(",", "."))
    if "mph" in s:
        v *= 1.60934
    if v <= 0:
        return default
    return v


def _oneway(tags, highway):
    """Ritorna 'avanti', 'indietro' o 'doppio' (verso lungo l'ordine dei nodi del way)."""
    v = (tags.get("oneway") or "").strip().lower()
    if v in ("yes", "true", "1"):
        return "avanti"
    if v in ("-1", "reverse"):
        return "indietro"
    if v in ("no", "false", "0"):
        return "doppio"
    if (tags.get("junction") or "").strip().lower() in ("roundabout", "circular"):
        return "avanti"
    if highway in SENSO_UNICO_DEFAULT:
        return "avanti"
    return "doppio"


def _accessibile(tags):
    for k in ("access", "motor_vehicle", "motorcar", "vehicle"):
        v = (tags.get(k) or "").strip().lower()
        if v in ("no", "private"):
            return False
    if (tags.get("highway") or "") in ("construction", "proposed", "abandoned"):
        return False
    return True


# --- costruzione -----------------------------------------------------------------

def costruisci(pbf, log=print, prova_bbox=None):
    """Legge il PBF e ritorna (nodi, archi_base, archi_orientati) come liste di dict.

    prova_bbox: (lat_min, lon_min, lat_max, lon_max) per limitare a un riquadro
    (solo per la prova rapida: taglia i way, non e' il giro vero).
    """
    import osmium

    t0 = time.time()
    modi = []          # un record per way percorribile
    conta_nodo = Counter()

    class Lettore(osmium.SimpleHandler):
        def way(self, w):
            hw = w.tags.get("highway")
            if hw not in DRIVABILI or not _accessibile(w.tags):
                return
            try:
                refs = [n.ref for n in w.nodes]
                pts = [(n.location.lat, n.location.lon) for n in w.nodes]
            except Exception:
                return
            if len(refs) < 2:
                return
            if prova_bbox:
                la0, lo0, la1, lo1 = prova_bbox
                if not any(la0 <= la <= la1 and lo0 <= lo <= lo1 for la, lo in pts):
                    return
            conta_nodo.update(refs)
            modi.append({
                "refs": refs, "pts": pts, "highway": hw,
                "nome": (w.tags.get("name") or "").strip() or None,
                "ref": (w.tags.get("ref") or "").strip() or None,
                "maxspeed": w.tags.get("maxspeed"),
                "verso": _oneway(w.tags, hw),
            })

    log(f"  lettura OSM ({Path(pbf).name}) ...")
    Lettore().apply_file(str(pbf), locations=True)
    log(f"  way percorribili: {len(modi):,}")

    # nodi di giunzione: usati da piu' di un way oppure estremi di un way
    giunzione = {n for n, c in conta_nodo.items() if c >= 2}
    for m in modi:
        giunzione.add(m["refs"][0])
        giunzione.add(m["refs"][-1])

    # id nodo -> indice compatto
    id_nodo = {}
    nodi = []

    def indice(nid, lat, lon):
        i = id_nodo.get(nid)
        if i is None:
            i = len(nodi)
            id_nodo[nid] = i
            nodi.append((lat, lon))
        return i

    archi_base = []   # {a,b,pts,len_m,t_s,highway,nome,ref,verso,ind_a,ind_b}
    for m in modi:
        refs, pts, hw = m["refs"], m["pts"], m["highway"]
        vel_default = VELOCITA_DEFAULT.get(hw, 30.0)
        vel = parse_maxspeed(m["maxspeed"], vel_default)
        vel_ms = max(vel, 5.0) / 3.6
        inizio = 0
        for i in range(1, len(refs)):
            if refs[i] not in giunzione and i != len(refs) - 1:
                continue
            if i == inizio:
                continue
            seg_pts = pts[inizio:i + 1]
            seg_refs = refs[inizio:i + 1]
            if len(seg_pts) >= 2:
                lung = 0.0
                for k in range(len(seg_pts) - 1):
                    lung += haversine_m(*seg_pts[k], *seg_pts[k + 1])
                if lung > 0.1:
                    archi_base.append({
                        "a": indice(seg_refs[0], *seg_pts[0]),
                        "b": indice(seg_refs[-1], *seg_pts[-1]),
                        "pts": seg_pts,
                        "len_m": lung,
                        "t_s": lung / vel_ms,
                        "highway": hw,
                        "nome": m["nome"],
                        "ref": m["ref"],
                        "verso": m["verso"],
                        "vel_kmh": vel,
                    })
            inizio = i

    log(f"  nodi di giunzione: {len(nodi):,}   tratti (archi base): {len(archi_base):,}   "
        f"({time.time()-t0:.1f} s)")

    # archi orientati (per il routing e per sommare i flussi nei due versi)
    archi = []   # (src, dst, peso_s, indice_arco_base, verso 0=avanti 1=indietro)
    for e, arco in enumerate(archi_base):
        if arco["verso"] in ("avanti", "doppio"):
            archi.append((arco["a"], arco["b"], arco["t_s"], e, 0))
        if arco["verso"] in ("indietro", "doppio"):
            archi.append((arco["b"], arco["a"], arco["t_s"], e, 1))

    nodi_xy = np.array(nodi, dtype=np.float64)
    return nodi, nodi_xy, archi_base, archi


def salva(cartella, nodi_xy, archi_base, archi):
    """Salva la rete in un .npz compatto (array) piu' un .json (nomi)."""
    cartella = Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    E = len(archi_base)
    # geometria dei tratti appiattita
    off = np.zeros(E + 1, dtype=np.int64)
    for e, arco in enumerate(archi_base):
        off[e + 1] = off[e] + len(arco["pts"])
    pts = np.empty((int(off[-1]), 2), dtype=np.float64)
    for e, arco in enumerate(archi_base):
        for k, (la, lo) in enumerate(arco["pts"]):
            pts[int(off[e]) + k] = (la, lo)
    # ATTENZIONE: i pesi (tempi) devono restare in virgola mobile. Se si
    # arrotondano a interi, molti tratti corti hanno tempo 0 e l'albero dei
    # cammini minimi si rompe (verificato il 17/10). Gli indici dei nodi
    # (fino a ~82.000) sono rappresentabili esattamente in float64.
    archi = np.array(archi, dtype=np.float64) if archi else np.zeros((0, 5), dtype=np.float64)
    np.savez_compressed(
        cartella / "rete_auto.npz",
        nodi_xy=nodi_xy,
        edge_a=np.array([a["a"] for a in archi_base], dtype=np.int64),
        edge_b=np.array([a["b"] for a in archi_base], dtype=np.int64),
        edge_len=np.array([a["len_m"] for a in archi_base], dtype=np.float64),
        edge_t=np.array([a["t_s"] for a in archi_base], dtype=np.float64),
        edge_off=off, edge_pts=pts,
        archi=archi,
    )
    (cartella / "rete_auto_metadati.json").write_text(json.dumps({
        "n_nodi": int(len(nodi_xy)), "n_archi_base": E, "n_archi_orientati": int(len(archi)),
        "nomi": [a["nome"] for a in archi_base],
        "highway": [a["highway"] for a in archi_base],
        "ref": [a["ref"] for a in archi_base],
        "verso": [a["verso"] for a in archi_base],
        "vel_kmh": [a["vel_kmh"] for a in archi_base],
        "stimato": False,
    }, ensure_ascii=False), encoding="utf-8")


def carica(cartella):
    """Ricarica la rete salvata. Ritorna un dict pronto per l'instradamento."""
    cartella = Path(cartella)
    z = np.load(cartella / "rete_auto.npz")
    meta = json.loads((cartella / "rete_auto_metadati.json").read_text(encoding="utf-8"))
    return {
        "nodi_xy": z["nodi_xy"],
        "edge_a": z["edge_a"], "edge_b": z["edge_b"],
        "edge_len": z["edge_len"], "edge_t": z["edge_t"],
        "edge_off": z["edge_off"], "edge_pts": z["edge_pts"],
        "archi": z["archi"], "meta": meta,
    }


def geometria_arco(rete, e):
    o0, o1 = int(rete["edge_off"][e]), int(rete["edge_off"][e + 1])
    return rete["edge_pts"][o0:o1]


def punto_medio(rete, e):
    p = geometria_arco(rete, e)
    # punto a meta' lunghezza del tracciato
    if len(p) == 1:
        return float(p[0, 0]), float(p[0, 1])
    d = np.array([haversine_m(*p[k], *p[k + 1]) for k in range(len(p) - 1)])
    tot = float(d.sum())
    if tot <= 0:
        return float(p[0, 0]), float(p[0, 1])
    meta = tot / 2
    acc = 0.0
    for k in range(len(p) - 1):
        if acc + d[k] >= meta:
            t = (meta - acc) / d[k] if d[k] > 0 else 0
            return (float(p[k, 0] + (p[k + 1, 0] - p[k, 0]) * t),
                    float(p[k, 1] + (p[k + 1, 1] - p[k, 1]) * t))
        acc += d[k]
    return float(p[-1, 0]), float(p[-1, 1])


def punti_medi(rete):
    return np.array([punto_medio(rete, e) for e in range(len(rete["edge_a"]))])


def tratto_piu_vicino(rete, lat, lon, medi=None, candidati=40):
    """(distanza_m, indice_tratto) del tratto stradale piu' vicino al punto.
    Prima filtra sui punti medi (veloce), poi misura la distanza vera sul
    tracciato dei migliori 40. Ritorna (inf, None) se non c'e' nulla."""
    if medi is None:
        medi = punti_medi(rete)
    d2 = (medi[:, 0] - lat) ** 2 + (medi[:, 1] - lon) ** 2
    ord_ = np.argsort(d2)[:candidati]
    best = (float("inf"), None)
    for e in ord_:
        d = distanza_punto_tracciato_m(lat, lon, geometria_arco(rete, int(e)))
        if d < best[0]:
            best = (d, int(e))
    return best


def distanza_punto_tracciato_m(lat, lon, pts):
    """Distanza minima (m) fra (lat,lon) e la polilinea pts (array Nx2)."""
    best = 1e18
    for k in range(len(pts) - 1):
        la1, lo1 = pts[k]
        la2, lo2 = pts[k + 1]
        # proiezione locale in metri
        mx = math.cos(math.radians(lat)) * 111320.0
        my = 110540.0
        px, py = (lon - lo1) * mx, (lat - la1) * my
        dx, dy = (lo2 - lo1) * mx, (la2 - la1) * my
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 <= 0 else max(0.0, min(1.0, (px * dx + py * dy) / L2))
        cx, cy = t * dx, t * dy
        d = math.hypot(px - cx, py - cy)
        if d < best:
            best = d
    return best
