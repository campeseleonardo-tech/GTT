#!/usr/bin/env python3
"""
04_genera_mappa.py  -  costruisce la mappa interattiva  GTT/mappa_torino.html

Legge gli ULTIMI file in data/raw (quelli scaricati da 01_scarica_dati.py) e li
incorpora in un unico file HTML che si apre con un doppio clic nel browser.
Usa solo la libreria standard di Python. Non scarica niente da internet.

Per avere la mappa aggiornata:
    1) python 01_scarica_dati.py
    2) python 04_genera_mappa.py
    3) apri GTT/mappa_torino.html

Cosa mette nella mappa:
  - OFFERTA programmata GTT per ora e tipo di giorno (feriale/sabato/domenica):
    passaggi alle fermate, corse/ora per linea, passaggi/ora per km2 per zona.
  - TRAFFICO 5T: 5 minuti piu' recenti dei sensori.
  - MEZZI GTT: posizione dei mezzi all'ultimo aggiornamento.
  - ZONE STATISTICHE del Comune (94 zone).
  - SEZIONI DI CENSIMENTO 2021 (se presenti, da 05_prepara_sezioni.py): abitanti e offerta per abitante.
  La domanda per ORA non c'e' ancora: i residenti sono la popolazione 'di notte', non chi si sposta.
"""
import csv
import io
import json
import math
import re
import struct
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    candidata = Path.home() / "Desktop" / "GTT"
    return candidata if candidata.is_dir() else AQUI.parent


RADICE = trova_radice()
RAW = RADICE / "data" / "raw"
# il modello della pagina sta in GTT/scripts: lo cerco li' anche se questo script e' stato copiato altrove
TEMPLATE = next((c for c in (AQUI / "mappa_template.html", RADICE / "scripts" / "mappa_template.html") if c.is_file()),
                RADICE / "scripts" / "mappa_template.html")
USCITA = RADICE / "mappa_torino.html"
TIPI_GIORNO = ["fer", "sab", "dom"]
csv.field_size_limit(10**8)


def ultimo(prefisso):
    trovati = sorted(RAW.glob(prefisso + "*"))
    if not trovati:
        sys.exit(f"File non trovato in {RAW}: {prefisso}*  (lancia prima 01_scarica_dati.py)")
    return trovati[-1]


# ---------------------------------------------------------------- protobuf (senza librerie)
def _varint(b, i):
    r = s = 0
    while True:
        x = b[i]
        i += 1
        r |= (x & 0x7F) << s
        s += 7
        if not x & 0x80:
            return r, i


def _campi(b):
    i, out = 0, []
    while i < len(b):
        k, i = _varint(b, i)
        fn, wt = k >> 3, k & 7
        if wt == 0:
            v, i = _varint(b, i)
        elif wt == 1:
            v = b[i:i + 8]
            i += 8
        elif wt == 2:
            n, i = _varint(b, i)
            v = b[i:i + n]
            i += n
        elif wt == 5:
            v = b[i:i + 4]
            i += 4
        else:
            raise ValueError(f"tipo protobuf non gestito: {wt}")
        out.append((fn, wt, v))
    return out


def leggi_mezzi(percorso):
    """Posizioni mezzi GTT (GTFS-RT vehicle positions) -> (timestamp_feed, lista)."""
    top = _campi(percorso.read_bytes())
    ts = 0
    for f, w, v in top:
        if f == 1:
            for f2, w2, v2 in _campi(v):
                if f2 == 3:
                    ts = v2
    mezzi = []
    for f, w, v in top:
        if f != 2:
            continue
        ent = {f1: v1 for f1, w1, v1 in _campi(v)}
        if 4 not in ent:
            continue
        veh = {f1: v1 for f1, w1, v1 in _campi(ent[4])}
        if 2 not in veh:
            continue
        pos = {f1: v1 for f1, w1, v1 in _campi(veh[2])}
        if 1 not in pos or 2 not in pos:
            continue
        linea = ""
        if 1 in veh:
            for f1, w1, v1 in _campi(veh[1]):
                if f1 == 5:
                    linea = v1.decode("utf-8", "replace")
        vid = ""
        if 8 in veh:
            for f1, w1, v1 in _campi(veh[8]):
                if f1 == 1:
                    vid = v1.decode("utf-8", "replace")
        mezzi.append({
            "r": linea, "id": vid,
            "la": round(struct.unpack("<f", pos[1])[0], 5),
            "lo": round(struct.unpack("<f", pos[2])[0], 5),
            "ts": veh.get(5, ts),
        })
    return ts, mezzi


# ---------------------------------------------------------------- 5T
def nome_locale(tag):
    return tag.rsplit("}", 1)[-1]


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def leggi_5t(percorso):
    radice = ET.parse(percorso).getroot()
    sensori = []
    for e in radice.iter():
        if nome_locale(e.tag) != "FDT_data":
            continue
        a = e.attrib
        sf = next((c.attrib for c in e if nome_locale(c.tag) == "speedflow"), {})
        sensori.append({
            "id": a.get("lcd1"), "via": a.get("Road_name", ""), "dir": a.get("direction", ""),
            "la": num(a.get("lat")), "lo": num(a.get("lng")), "acc": num(a.get("accuracy")),
            "fl": num(sf.get("flow")), "v": num(sf.get("speed")), "per": num(a.get("period")) or 5,
        })
    meta = {k: radice.attrib.get(k) for k in ("generation_time", "start_time", "end_time")}
    return meta, [s for s in sensori if s["la"] is not None and s["lo"] is not None]


# ---------------------------------------------------------------- GTFS
def leggi_csv(z, nome):
    with z.open(nome) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))


def data_gtfs(s):
    return date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def date_riferimento(inizio, fine):
    """Un martedi', un sabato e una domenica tipici, dentro la validita' del feed."""
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


def semplifica(punti, tol):
    """Douglas-Peucker su lista di (lat, lon); tol in gradi."""
    if len(punti) < 3:
        return punti
    coslat = math.cos(math.radians(punti[0][0]))
    p = [(x * 1.0, y * coslat) for x, y in punti]
    tieni = [False] * len(p)
    tieni[0] = tieni[-1] = True
    pila = [(0, len(p) - 1)]
    while pila:
        a, b = pila.pop()
        ax, ay = p[a]
        bx, by = p[b]
        dx, dy = bx - ax, by - ay
        den = math.hypot(dx, dy)
        dmax, imax = 0.0, -1
        for i in range(a + 1, b):
            px, py = p[i]
            d = math.hypot(px - ax, py - ay) if den == 0 else abs(dy * (px - ax) - dx * (py - ay)) / den
            if d > dmax:
                dmax, imax = d, i
        if dmax > tol and imax > 0:
            tieni[imax] = True
            pila.append((a, imax))
            pila.append((imax, b))
    return [punti[i] for i in range(len(punti)) if tieni[i]]


def elabora_gtfs(percorso):
    z = zipfile.ZipFile(percorso)
    info = leggi_csv(z, "feed_info.txt")[0]
    inizio, fine = data_gtfs(info["feed_start_date"]), data_gtfs(info["feed_end_date"])
    giorni = date_riferimento(inizio, fine)
    cal = leggi_csv(z, "calendar.txt")
    ecc = leggi_csv(z, "calendar_dates.txt") if "calendar_dates.txt" in z.namelist() else []
    attivi = [servizi_attivi(cal, ecc, giorni[k]) for k in TIPI_GIORNO]

    rotte = {}
    for r in leggi_csv(z, "routes.txt"):
        rotte[r["route_id"]] = {"s": r["route_short_name"] or r["route_id"], "t": int(r["route_type"] or 3),
                                "l": r["route_long_name"], "f": [0] * 72}
    viaggi = {}
    forme = defaultdict(Counter)
    for r in leggi_csv(z, "trips.txt"):
        flags = tuple(r["service_id"] in a for a in attivi)
        viaggi[r["trip_id"]] = (r["route_id"], flags, r.get("direction_id", ""))
        if r.get("shape_id"):
            forme[(r["route_id"], r.get("direction_id", ""))][r["shape_id"]] += 1

    fermate = {r["stop_id"]: r for r in leggi_csv(z, "stops.txt")}
    dep = defaultdict(lambda: [0] * 72)
    linee_fermata = defaultdict(set)
    inizio_corsa = {}
    tempi = {}  # trip_id -> [seq_primo, minuti_partenza, seq_ultimo, minuti_arrivo]
    with z.open("stop_times.txt") as f:
        rd = csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig"))
        ix = {n: i for i, n in enumerate(next(rd))}
        i_t, i_d, i_a, i_s, i_q = ix["trip_id"], ix["departure_time"], ix["arrival_time"], ix["stop_id"], ix["stop_sequence"]
        for r in rd:
            v = viaggi.get(r[i_t])
            if not v:
                continue
            rid, flags, _dir = v
            ora = r[i_d] or r[i_a]
            if len(ora) < 2:
                continue
            hh = int(ora[:2]) % 24
            sid = r[i_s]
            seq = int(r[i_q])
            for k in range(3):
                if flags[k]:
                    dep[sid][k * 24 + hh] += 1
            linee_fermata[sid].add(rid)
            try:
                minuti = int(ora[:2]) * 60 + int(ora[3:5]) + int(ora[6:8]) / 60 if len(ora) >= 8 else int(ora[:2]) * 60 + int(ora[3:5])
            except ValueError:
                minuti = None
            if minuti is not None:
                tt = tempi.get(r[i_t])
                if tt is None:
                    tempi[r[i_t]] = [seq, minuti, seq, minuti]
                else:
                    if seq < tt[0]:
                        tt[0], tt[1] = seq, minuti
                    if seq > tt[2]:
                        tt[2], tt[3] = seq, minuti
            prec = inizio_corsa.get(r[i_t])
            if prec is None or seq < prec[0]:
                inizio_corsa[r[i_t]] = (seq, hh)
    for tid, (seq, hh) in inizio_corsa.items():
        rid, flags, _dir = viaggi[tid]
        for k in range(3):
            if flags[k]:
                rotte[rid]["f"][k * 24 + hh] += 1

    # tracciati: una forma per (linea, direzione), la piu' usata
    scelte = {key: c.most_common(1)[0][0] for key, c in forme.items()}
    servono = set(scelte.values())
    pts = defaultdict(list)
    with z.open("shapes.txt") as f:
        rd = csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig"))
        ix = {n: i for i, n in enumerate(next(rd))}
        for r in rd:
            if r[ix["shape_id"]] in servono:
                pts[r[ix["shape_id"]]].append((int(float(r[ix["shape_pt_sequence"]])),
                                               float(r[ix["shape_pt_lat"]]), float(r[ix["shape_pt_lon"]])))
    linee = []
    for (rid, d), sh in sorted(scelte.items()):
        seq = [(la, lo) for _, la, lo in sorted(pts.get(sh, []))]
        seq = semplifica(seq, 0.00010)
        if len(seq) >= 2 and rid in rotte:
            linee.append({"id": rid, "d": d, "p": [[round(a, 5), round(b, 5)] for a, b in seq]})

    # corse per la simulazione: linea+direzione -> indice del tracciato; partenza e arrivo in minuti dalla mezzanotte
    indice_linea = {(l["id"], l["d"]): i for i, l in enumerate(linee)}
    corse = [[], [], []]
    senza_forma = 0
    for tid, (rid, flags, d) in viaggi.items():
        tt = tempi.get(tid)
        if not tt or tt[2] == tt[0] or tt[3] <= tt[1]:
            continue
        i = indice_linea.get((rid, d))
        if i is None:
            i = next((indice_linea[k] for k in ((rid, "0"), (rid, "1"), (rid, "")) if k in indice_linea), None)
        if i is None:
            senza_forma += 1
            continue
        for k in range(3):
            if flags[k]:
                corse[k].append([i, round(tt[1], 1), round(tt[3], 1)])
    for c in corse:
        c.sort(key=lambda x: x[1])
    print(f"  corse simulabili (feriale/sabato/domenica): {[len(c) for c in corse]}; senza tracciato: {senza_forma}")

    stops = []
    for sid, dv in dep.items():
        s = fermate.get(sid)
        if not s or not s["stop_lat"] or not s["stop_lon"]:
            continue
        nomi = sorted({rotte[r]["s"] for r in linee_fermata[sid] if r in rotte})
        stops.append({"id": sid, "n": s["stop_name"], "la": round(float(s["stop_lat"]), 5),
                      "lo": round(float(s["stop_lon"]), 5), "r": ", ".join(nomi[:14]) + ("…" if len(nomi) > 14 else ""),
                      "d": dv})
    meta = {"versione": info.get("feed_version"), "inizio": str(inizio), "fine": str(fine),
            "giorni": {k: str(v) for k, v in giorni.items()},
            "n_linee": len(rotte), "n_fermate_totali": len(fermate)}
    # solo le linee con tracciato o con corse servono al browser
    rotte = {k: v for k, v in rotte.items() if any(v["f"]) or any(l["id"] == k for l in linee)}
    return meta, rotte, linee, stops, corse


# ---------------------------------------------------------------- zone (Gauss-Boaga -> WGS84)
def gb_a_wgs84(E, N):
    """EPSG:3003 (Monte Mario / Italy zone 1) -> WGS84, con traslazione geocentrica a 3 parametri."""
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
    # geodetiche (Hayford) -> geocentriche -> traslazione -> WGS84
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


def _parentesi(s):
    """Interpreta le parentesi annidate del WKT -> liste annidate; le foglie sono liste di (x, y)."""
    pila, corrente, buf = [], [], ""
    for ch in s:
        if ch == "(":
            pila.append(corrente)
            corrente = []
            buf = ""
        elif ch == ")":
            padre = pila.pop()
            if buf.strip():  # parentesi piu' interna: e' un anello di coordinate
                padre.append([tuple(float(t) for t in c.split()[:2]) for c in buf.split(",")])
            else:
                padre.append(corrente)
            buf = ""
            corrente = padre
        else:
            buf += ch
    return corrente[0]


def leggi_zone(percorso):
    z = zipfile.ZipFile(percorso)
    nome = next(n for n in z.namelist() if n.lower().endswith(".csv"))
    grezzo = z.read(nome)
    try:
        testo = grezzo.decode("utf-8-sig")
    except UnicodeDecodeError:
        testo = grezzo.decode("cp1252")  # il file del Comune non e' in UTF-8
    righe = list(csv.DictReader(io.StringIO(testo), delimiter=";"))
    zone = []
    for r in righe:
        wkt = r["WKT_GEOM"].strip()
        tipo = wkt.split("(")[0].strip().upper()
        nest = _parentesi(wkt[len(tipo):])
        poligoni = [nest] if tipo == "POLYGON" else nest
        area = 0.0
        out = []
        for poly in poligoni:
            anelli = []
            for k, anello in enumerate(poly):
                a2 = sum(anello[i][0] * anello[(i + 1) % len(anello)][1] - anello[(i + 1) % len(anello)][0] * anello[i][1]
                         for i in range(len(anello))) / 2
                area += abs(a2) if k == 0 else -abs(a2)
                ll = [gb_a_wgs84(x, y) for x, y in anello]
                ll = semplifica(ll, 0.00004)
                anelli.append([[round(a, 5), round(b, 5)] for a, b in ll])
            out.append(anelli)
        zone.append({"c": r["ZONASTAT"], "n": r["DENOM"], "km2": round(area / 1e6, 4), "g": out})
    return zone


def dentro(la, lo, zona):
    for poly in zona["g"]:
        n = 0
        for anello in poly:
            j = len(anello) - 1
            for i in range(len(anello)):
                yi, xi = anello[i]
                yj, xj = anello[j]
                if (xi > lo) != (xj > lo) and la < (yj - yi) * (lo - xi) / (xj - xi) + yi:
                    n += 1
                j = i
        if n % 2 == 1:
            return True
    return False


def assegna_zone(zone, stops):
    for z in zone:
        z["d"] = [0] * 72
        z["nf"] = 0
        lat = [p[0] for poly in z["g"] for anello in poly for p in anello]
        lon = [p[1] for poly in z["g"] for anello in poly for p in anello]
        z["_bb"] = (min(lat), max(lat), min(lon), max(lon))
    fuori = 0
    for s in stops:
        trovata = False
        for z in zone:
            b = z["_bb"]
            if b[0] <= s["la"] <= b[1] and b[2] <= s["lo"] <= b[3] and dentro(s["la"], s["lo"], z):
                z["nf"] += 1
                z["d"] = [a + c for a, c in zip(z["d"], s["d"])]
                trovata = True
                break
        if not trovata:
            fuori += 1
    for z in zone:
        del z["_bb"]
    return fuori


# ---------------------------------------------------------------- main
def main():
    print(f"Cartella del progetto: {RADICE}")
    if not TEMPLATE.is_file():
        sys.exit(f"Manca il modello della pagina: {TEMPLATE}\nLancia lo script da GTT\\scripts oppure copia li' mappa_template.html.")
    f_gtfs, f_5t = ultimo("gtt_gtfs_"), ultimo("5t_flussi_")
    f_vp, f_zone = ultimo("gtt_vehicle_position_"), ultimo("zone_statistiche_csv_")
    print("Uso questi file:", f_gtfs.name, f_5t.name, f_vp.name, f_zone.name, sep="\n  ")

    print("Leggo GTFS (qualche secondo)...")
    meta_gtfs, rotte, linee, stops, corse = elabora_gtfs(f_gtfs)
    print(f"  fermate con passaggi: {len(stops)}, linee con tracciato: {len(linee)}")
    meta5t, sensori = leggi_5t(f_5t)
    ts_vp, mezzi = leggi_mezzi(f_vp)
    print(f"  sensori 5T: {len(sensori)}, mezzi GTT: {len(mezzi)}")
    zone = leggi_zone(f_zone)
    fuori = assegna_zone(zone, stops)
    print(f"  zone: {len(zone)}; fermate fuori da ogni zona (altri comuni): {fuori}")

    sez, f_sez = [], RADICE / "data" / "processed" / "sezioni_torino.json"
    if f_sez.is_file():
        sez = [{"p": x["p"], "a": x["a"], "g": x["g"]} for x in json.loads(f_sez.read_text(encoding="utf-8")) if x["p"] > 0]
        print(f"  sezioni di censimento abitate: {len(sez)}, abitanti {sum(x['p'] for x in sez)}")
    else:
        print("  (sezioni di censimento non trovate: lancia 05_prepara_sezioni.py per il livello Domanda)")

    dati = {
        "meta": {
            "costruita_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "gtfs": meta_gtfs, "t5": meta5t, "mezzi_ts": ts_vp,
            "file": {"gtfs": f_gtfs.name, "t5": f_5t.name, "mezzi": f_vp.name, "zone": f_zone.name},
        },
        "rotte": rotte, "linee": linee, "fermate": stops, "sensori": sensori, "mezzi": mezzi, "zone": zone, "sezioni": sez, "corse": corse,
    }
    testo = json.dumps(dati, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace('"__DATI__"', testo)
    USCITA.write_text(html, encoding="utf-8")
    print(f"\nMappa creata: {USCITA}  ({USCITA.stat().st_size / 1e6:.1f} MB)")
    print("Aprila con doppio clic (serve internet solo per le mattonelle della cartina).")


if __name__ == "__main__":
    main()
