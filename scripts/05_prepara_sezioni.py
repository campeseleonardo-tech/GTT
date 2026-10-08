#!/usr/bin/env python3
"""
05_prepara_sezioni.py - prepara le sezioni di censimento 2021 di Torino e cintura.

Legge  GTT/R01_21.zip  (confini ISTAT del Piemonte, UTM32N) oppure GTT/data/raw/istat/basi_territoriali_2021/R01_21.zip
e scrive  GTT/data/processed/sezioni_torino.json  (poligoni in lat/lon semplificati + abitanti POP21 per sezione).
Solo libreria standard di Python. Non scarica niente.
Uso:  python 05_prepara_sezioni.py            (cintura = default, vedi RAGGIO_KM)
"""
import json, math, struct, sys, zipfile, io
from pathlib import Path

AQUI = Path(__file__).resolve().parent
def trova_radice():
    for c in [AQUI, *AQUI.parents]:
        if c.name.lower() == "gtt":
            return c
    d = Path.home() / "Desktop" / "GTT"
    return d if d.is_dir() else AQUI.parent
RADICE = trova_radice()
CAND = [RADICE / "data/raw/istat/basi_territoriali_2021/R01_21.zip", RADICE / "R01_21.zip"]
ZIP = next((c for c in CAND if c.is_file()), None)
if ZIP is None:
    sys.exit("R01_21.zip non trovato in GTT (ne' in data/raw/istat/basi_territoriali_2021)")
OUT = RADICE / "data" / "processed" / "sezioni_torino.json"

CENTRO = (45.0703, 7.6869)   # Torino, piazza Castello
RAGGIO_KM = 18.0             # cintura: sezioni entro questa distanza dal centro
TOL_M = 4.0                  # semplificazione bordi (metri)
PRO_COM_TORINO = 1272

# --- UTM32N (WGS84) -> lat/lon
A, F = 6378137.0, 1 / 298.257223563
E2 = F * (2 - F); EP2 = E2 / (1 - E2); K0 = 0.9996
def utm_inv(x, y):
    x -= 500000.0
    m = y / K0
    mu = m / (A * (1 - E2/4 - 3*E2**2/64 - 5*E2**3/256))
    e1 = (1 - math.sqrt(1-E2)) / (1 + math.sqrt(1-E2))
    p = (mu + (3*e1/2 - 27*e1**3/32)*math.sin(2*mu) + (21*e1**2/16 - 55*e1**4/32)*math.sin(4*mu)
         + (151*e1**3/96)*math.sin(6*mu) + (1097*e1**4/512)*math.sin(8*mu))
    c1 = EP2*math.cos(p)**2; t1 = math.tan(p)**2
    n1 = A/math.sqrt(1-E2*math.sin(p)**2); r1 = A*(1-E2)/(1-E2*math.sin(p)**2)**1.5
    d = x/(n1*K0)
    lat = p - (n1*math.tan(p)/r1)*(d*d/2 - (5+3*t1+10*c1-4*c1*c1-9*EP2)*d**4/24
          + (61+90*t1+298*c1+45*t1*t1-252*EP2-3*c1*c1)*d**6/720)
    lon = (d - (1+2*t1+c1)*d**3/6 + (5-2*c1+28*t1-3*c1*c1+8*EP2+24*t1*t1)*d**5/120)/math.cos(p)
    return math.degrees(lat), 9.0 + math.degrees(lon)

def km(lat, lon):
    return math.hypot((lat-CENTRO[0])*111.2, (lon-CENTRO[1])*111.2*math.cos(math.radians(CENTRO[0])))

def dp(pts, tol):
    if len(pts) < 4: return pts
    keep = [False]*len(pts); keep[0] = keep[-1] = True
    st = [(0, len(pts)-1)]
    while st:
        a, b = st.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy) or 1e-9
        md, mi = 0, None
        for i in range(a+1, b):
            d = abs(dy*(pts[i][0]-x1) - dx*(pts[i][1]-y1))/L
            if d > md: md, mi = d, i
        if mi is not None and md > tol:
            keep[mi] = True; st += [(a, mi), (mi, b)]
    return [p for p, k in zip(pts, keep) if k]

def dp_anello(ring, tol):
    """Semplifica un anello chiuso: lo spezzo nel punto piu' lontano dall'inizio, cosi' la formula funziona."""
    if len(ring) < 6: return ring
    x0, y0 = ring[0]
    m = max(range(1, len(ring)-1), key=lambda i: (ring[i][0]-x0)**2 + (ring[i][1]-y0)**2)
    return dp(ring[:m+1], tol)[:-1] + dp(ring[m:], tol)

def leggi_dbf(b):
    n, hl, rl = struct.unpack("<IHH", b[4:12])
    campi, i = [], 32
    while b[i] != 0x0D:
        campi.append((b[i:i+11].split(b"\0")[0].decode(), b[i+16])); i += 32
    righe = []
    for r in range(n):
        rec = b[hl + r*rl: hl + (r+1)*rl]; o = 1; d = {}
        for nome, ln in campi:
            d[nome] = rec[o:o+ln].decode("latin-1").strip(); o += ln
        righe.append(d)
    return righe

def poligoni(b, k):
    """k-esimo record .shp -> lista di anelli [(x,y)]. Usa l'indice .shx fornito esternamente."""
    pass

def main():
    z = zipfile.ZipFile(ZIP)
    shp = z.read("SHP/R01_21_WGS84.shp"); shx = z.read("SHP/R01_21_WGS84.shx"); dbf = z.read("SHP/R01_21_WGS84.dbf")
    righe = leggi_dbf(dbf)
    n = (len(shx) - 100)//8
    assert n == len(righe), (n, len(righe))
    out, saltate = [], 0
    for k in range(n):
        off = struct.unpack(">i", shx[100+8*k:104+8*k])[0]*2
        tipo = struct.unpack("<i", shp[off+8:off+12])[0]
        if tipo == 0: continue
        xmin, ymin, xmax, ymax = struct.unpack("<4d", shp[off+12:off+44])
        la, lo = utm_inv((xmin+xmax)/2, (ymin+ymax)/2)
        r = righe[k]
        if km(la, lo) > RAGGIO_KM and int(r["PRO_COM"] or 0) != PRO_COM_TORINO:
            saltate += 1; continue
        npart, npt = struct.unpack("<2i", shp[off+44:off+52])
        parti = list(struct.unpack(f"<{npart}i", shp[off+52:off+52+4*npart])) + [npt]
        p0 = off+52+4*npart
        pts = struct.unpack(f"<{2*npt}d", shp[p0:p0+16*npt])
        anelli = []
        for a, b in zip(parti, parti[1:]):
            ring = [(pts[2*i], pts[2*i+1]) for i in range(a, b)]
            ring = dp_anello(ring, TOL_M)
            if len(ring) < 4: continue
            anelli.append([[round(c, 5) for c in utm_inv(x, y)] for x, y in ring])
        if not anelli: continue
        # area in km2 (formula dei lacci sull'anello esterno, UTM) 
        ex = [(pts[2*i], pts[2*i+1]) for i in range(parti[0], parti[1])]
        ar = abs(sum(ex[i][0]*ex[i+1][1]-ex[i+1][0]*ex[i][1] for i in range(len(ex)-1)))/2/1e6
        out.append({"id": r["SEZ21_ID"], "c": int(r["PRO_COM"]), "p": int(r["POP21"] or 0), "a": round(ar, 5),
                    "t": int(r["COD_TIPO_S"] or 0), "f": int(r["FAM21"] or 0), "ab": int(r["ABI21"] or 0), "g": anelli})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    tor = [s for s in out if s["c"] == PRO_COM_TORINO]
    print(f"Sezioni salvate: {len(out)} (Torino {len(tor)}, abitanti Torino {sum(s['p'] for s in tor)}); fuori area: {saltate}")
    print(f"Abitanti totali nell'area: {sum(s['p'] for s in out)}; file {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")
main()
