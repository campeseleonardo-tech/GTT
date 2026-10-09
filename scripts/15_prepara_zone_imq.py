#!/usr/bin/env python3
"""15_prepara_zone_imq.py - Fasi 3 e 4 del piano IMQ 2022: geometria delle 212 zone.

Parte A (fase 3): i 23 quartieri di Torino da data/raw/ex_quartieri/ex_quartieri.shp
(EPSG:3003). Lettore shapefile in sola libreria standard (tipi 5 e 15, la Z si ignora;
parti e fori). Abbinamento zona<->quartiere per nome normalizzato (con ripiego su
IDQUART -> Q0xx). Verifiche: 23 id, area 128-132 km2, rapporto demografico.

Scrive data/processed/imq_zone_geo.json (il file viene completato dalla parte B).

Solo libreria standard. Uso: python scripts/15_prepara_zone_imq.py
"""

import json
import math
import struct
import sys
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for c in [AQUI, *AQUI.parents]:
        if c.name.lower() == "gtt":
            return c
    d = Path.home() / "Desktop" / "GTT"
    return d if d.is_dir() else AQUI.parent


RADICE = trova_radice()
QUARTIERI_SHP = RADICE / "data/raw/ex_quartieri/ex_quartieri.shp"
QUARTIERI_DBF = RADICE / "data/raw/ex_quartieri/ex_quartieri.dbf"
CONFINI_ZIP = RADICE / "data/raw/istat/confini_2022/Limiti01012022_g.zip"
SEZIONI = RADICE / "data/processed/sezioni_torino.json"
RESIDENTI = RADICE / "data/processed/imq_residenti.json"
ZONE = RADICE / "data/processed/imq_zone.json"
OUT = RADICE / "data/processed/imq_zone_geo.json"

CENTRO = (45.0703, 7.6869)   # Piazza Castello (stesso punto usato per il catalogo)
PRO_COM_TORINO = "001272"
AREA_MIN_KM2, AREA_MAX_KM2 = 128.0, 132.0


# ------------------------------------------------------------------ geometria
def gb_a_wgs84(E, N):
    """EPSG:3003 (Monte Mario / Italy zone 1) -> WGS84 (copia da 11_prepara_catalogo.py)."""
    a, f = 6378388.0, 1 / 297.0
    e2 = 2 * f - f * f
    ep2 = e2 / (1 - e2)
    k0, lon0 = 0.9996, math.radians(9.0)
    x, y = E - 1500000.0, N
    M = y / k0
    mu = M / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu) + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    C1 = ep2 * math.cos(phi1) ** 2
    T1 = math.tan(phi1) ** 2
    N1 = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    R1 = a * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    D = x / (N1 * k0)
    lat = phi1 - (N1 * math.tan(phi1) / R1) * (
        D ** 2 / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * ep2) * D ** 4 / 24
        + (61 + 90 * T1 + 298 * C1 + 45 * T1 ** 2 - 252 * ep2 - 3 * C1 ** 2) * D ** 6 / 720)
    lon = lon0 + (D - (1 + 2 * T1 + C1) * D ** 3 / 6
                  + (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 * ep2 + 24 * T1 ** 2) * D ** 5 / 120) / math.cos(phi1)
    n = a / math.sqrt(1 - e2 * math.sin(lat) ** 2)
    X, Y, Zc = n * math.cos(lat) * math.cos(lon), n * math.cos(lat) * math.sin(lon), n * (1 - e2) * math.sin(lat)
    X, Y, Zc = X - 104.1, Y - 49.1, Zc - 9.9
    aw, fw = 6378137.0, 1 / 298.257223563
    ew2 = 2 * fw - fw * fw
    p = math.hypot(X, Y)
    lat2 = math.atan2(Zc, p * (1 - ew2))
    for _ in range(6):
        nw = aw / math.sqrt(1 - ew2 * math.sin(lat2) ** 2)
        lat2 = math.atan2(Zc + ew2 * nw * math.sin(lat2), p)
    return math.degrees(lat2), math.degrees(math.atan2(Y, X))


def utm32n_a_wgs84(E, N):
    """UTM zona 32N su WGS84 -> lat/lon. Nessun cambio di datum (copia da 05)."""
    a, f = 6378137.0, 1 / 298.257223563
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    k0 = 0.9996
    x = E - 500000.0
    m = N / k0
    mu = m / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    phi1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu)
            + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
            + (151 * e1 ** 3 / 96) * math.sin(6 * mu) + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    C1 = ep2 * math.cos(phi1) ** 2
    T1 = math.tan(phi1) ** 2
    N1 = a / math.sqrt(1 - e2 * math.sin(phi1) ** 2)
    R1 = a * (1 - e2) / (1 - e2 * math.sin(phi1) ** 2) ** 1.5
    D = x / (N1 * k0)
    lat = phi1 - (N1 * math.tan(phi1) / R1) * (
        D ** 2 / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 ** 2 - 9 * ep2) * D ** 4 / 24
        + (61 + 90 * T1 + 298 * C1 + 45 * T1 ** 2 - 252 * ep2 - 3 * C1 ** 2) * D ** 6 / 720)
    lon = (D - (1 + 2 * T1 + C1) * D ** 3 / 6
           + (5 - 2 * C1 + 28 * T1 - 3 * C1 ** 2 + 8 * ep2 + 24 * T1 ** 2) * D ** 5 / 120) / math.cos(phi1)
    return math.degrees(lat), 9.0 + math.degrees(lon)


def area_con_segno(ring):
    s = 0.0
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def normalizza(s):
    s = unicodedata.normalize("NFKD", s.upper())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(c for c in s if c.isalnum())


# ------------------------------------------------------------------ lettori
def leggi_dbf(percorso):
    b = Path(percorso).read_bytes()
    n, hl, rl = struct.unpack("<IHH", b[4:12])
    campi, i = [], 32
    while b[i] != 0x0D:
        campi.append((b[i:i + 11].split(b"\0")[0].decode("latin-1"), b[i + 16]))
        i += 32
    righe = []
    for r in range(n):
        rec = b[hl + r * rl: hl + (r + 1) * rl]
        o, d = 1, {}
        for nome, ln in campi:
            d[nome] = rec[o:o + ln].decode("cp1252").strip()
            o += ln
        righe.append(d)
    return righe


def leggi_shp_poligoni(percorso):
    """Tipi 5 (Polygon) e 15 (PolygonZ, la Z ignorata). Ritorna lista di record:
    {"rings": [[(x,y),...], ...], "bbox": (xmin,ymin,xmax,ymax)} oppure None."""
    b = Path(percorso).read_bytes()
    recs = []
    off = 100
    while off + 8 <= len(b):
        clen = struct.unpack(">I", b[off + 4:off + 8])[0]
        rec_end = off + 8 + clen * 2
        stype = struct.unpack("<i", b[off + 8:off + 12])[0]
        if stype in (5, 15):
            xmin, ymin, xmax, ymax = struct.unpack("<4d", b[off + 12:off + 44])
            npart, npt = struct.unpack("<2i", b[off + 44:off + 52])
            parti = list(struct.unpack(f"<{npart}i", b[off + 52:off + 52 + 4 * npart]))
            p0 = off + 52 + 4 * npart
            pts = struct.unpack(f"<{2 * npt}d", b[p0:p0 + 16 * npt])
            bounds = parti + [npt]
            anelli = [[(pts[2 * i], pts[2 * i + 1]) for i in range(a, c)]
                      for a, c in zip(bounds, bounds[1:])]
            recs.append({"rings": anelli, "bbox": (xmin, ymin, xmax, ymax)})
        else:
            recs.append(None)
        off = rec_end
    return recs


def pip_anello(x, y, ring):
    """Ray casting: True se il punto e' dentro l'anello."""
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xi:
                inside = not inside
    return inside


def punto_in_record(x, y, rec):
    """Regola even-odd su tutti gli anelli del record (fori compresi)."""
    return sum(1 for ring in rec["rings"] if pip_anello(x, y, ring)) % 2 == 1


# ------------------------------------------------------------------ parte A
def parte_quartieri(zone_json):
    dbf = leggi_dbf(QUARTIERI_DBF)
    shp = leggi_shp_poligoni(QUARTIERI_SHP)
    recs = [r for r in shp if r is not None]
    if len(dbf) != len(recs):
        sys.exit(f"STOP: .dbf ({len(dbf)}) e .shp ({len(recs)}) non allineati")

    # nome identificativo: IDQUART oppure ID_QUART
    campo_id = "IDQUART" if "IDQUART" in dbf[0] else ("ID_QUART" if "ID_QUART" in dbf[0] else None)
    if campo_id is None or "DESCR" not in dbf[0]:
        sys.exit(f"STOP: campi attesi assenti nel .dbf: {list(dbf[0])}")

    # mappa nome normalizzato -> codice zona (solo i quartieri di Torino, macro 01 Torino)
    zone_torino = [z for z in zone_json if z["macro"].startswith("01 Torino")]
    nome_a_zona = {}
    for z in zone_torino:
        prefisso = z["macro"]
        resto = z["denom"]
        if resto.startswith(prefisso):
            resto = resto[len(prefisso):]
        nome_a_zona[normalizza(resto)] = z["cod"]

    ids, abbinamenti = [], {}
    for r in dbf:
        qid = int(r[campo_id])
        ids.append(qid)
        chiave = normalizza(r["DESCR"])
        cod = nome_a_zona.get(chiave)
        if cod is None:
            cod = f"Q{qid:03d}"     # ripiego: identificativo -> Q0xx
            metodo = "id"
        else:
            metodo = "nome"
        abbinamenti[cod] = {"qid": qid, "descr": r["DESCR"], "metodo": metodo}

    print(f"  quartieri: {len(dbf)}; id distinti: {len(set(ids))}")
    for cod, info in sorted(abbinamenti.items()):
        print(f"    {cod} qid={info['qid']:>2} ({info['metodo']}) {info['descr']}")

    # geometria in WGS84 + area in EPSG:3003
    out = {}
    wgs_recs = []
    area_tot = 0.0
    for k, rec in enumerate(recs):
        qid = ids[k]
        cod = next(c for c, info in abbinamenti.items() if info["qid"] == qid)
        anelli = [[(round(la, 5), round(lo, 5))
                   for la, lo in (gb_a_wgs84(x, y) for x, y in ring)]
                  for ring in rec["rings"]]
        wgs_recs.append({"rings": anelli})
        area = abs(sum(area_con_segno(ring) for ring in rec["rings"]))
        area_tot += area
        out[cod] = {"qid": qid, "g": [[[la, lo] for la, lo in ring] for ring in anelli],
                    "a": round(area / 1e6, 4)}
    area_km2 = area_tot / 1e6

    # rapporto demografico
    res = json.loads(RESIDENTI.read_text(encoding="utf-8"))["per_zona"]
    sez = json.loads(SEZIONI.read_text(encoding="utf-8"))
    pop_quart = defaultdict(float)
    sez_torino = 0
    for s in sez:
        if str(s["c"]) != "1272":
            continue
        sez_torino += 1
        vertici = [pt for ring in s["g"] for pt in ring]
        lat_c = sum(p[0] for p in vertici) / len(vertici)
        lon_c = sum(p[1] for p in vertici) / len(vertici)
        for k, rec in enumerate(wgs_recs):
            if punto_in_record(lat_c, lon_c, rec):
                cod = next(c for c, info in abbinamenti.items() if info["qid"] == ids[k])
                pop_quart[cod] += s["p"]
                break

    def tot_res(cod):
        zona = res.get(cod, {})
        return sum(v["v"] for sesso in zona.values() for v in sesso.values())

    rapporto = {}
    for cod in abbinamenti:
        pop = pop_quart.get(cod, 0.0)
        imq = tot_res(cod)
        rapporto[cod] = (imq / pop) if pop > 0 else float("nan")
    validi = sorted(r for r in rapporto.values() if r == r)
    mediana = validi[len(validi) // 2] if validi else float("nan")

    return {"zone": out, "area_km2": area_km2, "rapporto": rapporto,
            "mediana": mediana, "sez_torino": sez_torino, "pop_quart": pop_quart,
            "abbinamenti": abbinamenti, "ids": ids, "recs": recs}


def main():
    zone_json = json.loads(ZONE.read_text(encoding="utf-8"))
    a = parte_quartieri(zone_json)

    print(f"\n  area totale quartieri: {a['area_km2']:.2f} km2 (attesi {AREA_MIN_KM2}-{AREA_MAX_KM2})")
    print(f"  sezioni di Torino usate: {a['sez_torino']}; mediana rapporto: {a['mediana']:.3f}")
    for cod in sorted(a["rapporto"]):
        r = a["rapporto"][cod]
        scarto = abs(r - a["mediana"]) / a["mediana"] if a["mediana"] == a["mediana"] else float("nan")
        print(f"    {cod} pop2021={a['pop_quart'].get(cod,0):>7.0f} "
              f"rapporto={r:.3f} scarto={100*scarto:5.1f}%")

    esiti = []

    def check(nome, ok, dettaglio):
        esiti.append((nome, bool(ok)))
        print(f"[{'OK ' if ok else 'STOP'}] {nome}: {dettaglio}")

    check("23 id distinti", len(set(a["ids"])) == 23, f"{len(set(a['ids']))}")
    check("23 zone Q abbinate", len(a["abbinamenti"]) == 23 and
          all(c.startswith("Q") for c in a["abbinamenti"]), f"{len(a['abbinamenti'])}")
    check("area Torino 128-132 km2", AREA_MIN_KM2 <= a["area_km2"] <= AREA_MAX_KM2,
          f"{a['area_km2']:.2f} km2")
    fuori = [c for c in a["rapporto"] if a["rapporto"][c] == a["rapporto"][c]
             and abs(a["rapporto"][c] - a["mediana"]) / a["mediana"] > 0.15]
    check("rapporto demografico entro ±15% dalla mediana", not fuori,
          f"fuori: {fuori if fuori else 'nessuno'}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"q": {c: a["zone"][c]["g"] for c in a["zone"]}}, separators=(",", ":")),
                   encoding="utf-8")
    print(f"\n  scritto {OUT} (solo quartieri, provvisorio)")

    fallite = [n for n, ok in esiti if not ok]
    if fallite:
        sys.exit("STOP: verifiche fase 3 fallite: " + ", ".join(fallite))
    print("Tutte le verifiche di fase 3 superate.")


if __name__ == "__main__":
    main()
