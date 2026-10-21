#!/usr/bin/env python3
"""Prova dello script 95 senza data/: ricostruisce, dai DATI dentro mappa_torino.html, file nello stesso formato di quelli veri
(sezioni_torino.json, vulnerabilita.json, accessibilita.json, omi_zone.json, un GTFS con le sole fermate M1) in una cartella.
Le forme sono quelle semplificate della mappa (4 decimali): i numeri sono indicativi, non quelli del calcolo vero.
Uso: python scripts/prove/dati_da_mappa_95.py [mappa_torino.html] CARTELLA ; poi: python scripts/95_case_fragilita_servizi.py --radice CARTELLA"""
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("g04", AQUI.parent / "04_genera_mappa.py")
g04 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g04)

args = sys.argv[1:]
html = Path(args[0]) if len(args) == 2 else AQUI.parent.parent / "mappa_torino.html"
rad = Path(args[-1])
riga = next(x for x in html.read_text(encoding="utf-8").split("\n") if x.startswith("const DATI = "))
D = json.loads(riga[len("const DATI = "):].rstrip(";"))
S = D["sezioni"]
P = rad / "data" / "processed"
P.mkdir(parents=True, exist_ok=True)
(rad / "data" / "raw").mkdir(parents=True, exist_ok=True)


def anelli(testo):
    out = []
    for r in testo.split(" "):
        n = g04.decod_int(r)
        la = lo = 0
        pts = []
        for i in range(0, len(n), 2):
            la += n[i]
            lo += n[i + 1]
            pts.append([la / 1e4, lo / 1e4])
        pts.append(pts[0])
        out.append(pts)
    return out


sez, vul, acc = [], [], []
for i in range(S["n"]):
    sid = f"{S['c'][i]}{i:06d}"
    sez.append({"id": sid, "c": S["c"][i], "p": S["p"][i], "a": S["a"][i], "g": anelli(S["g"][i])})
    vul.append({"id": sid, "comune": S["c"][i], "res": S["p"][i], "v": S["v"][i], "c": {}, "tipo": "residenziale" if S["v"][i] is not None else "istituzionale"})
    a = S["acc"][i]
    if isinstance(a, str):
        n = g04.decod_int(a)
        piedi = {g: n[k] for k, g in enumerate(g04.GRUPPI_ACC)}
        acc.append({"id": sid, "piedi": {"15": piedi}})
(P / "sezioni_torino.json").write_text(json.dumps(sez), encoding="utf-8")
(P / "vulnerabilita.json").write_text(json.dumps({"sezioni": vul}), encoding="utf-8")
(P / "accessibilita.json").write_text(json.dumps({"sezioni": acc}), encoding="utf-8")
(P / "omi_zone.json").write_text(json.dumps(D["omi"]), encoding="utf-8")
metro = [f for f in D["fermate"] if f["n"].startswith("METRO") and f["r"].strip() == "M1"]
with zipfile.ZipFile(rad / "data" / "raw" / "gtt_gtfs_dalla_mappa.zip", "w") as zf:
    zf.writestr("routes.txt", "route_id,route_type\nM1,1\n")
    zf.writestr("trips.txt", "route_id,trip_id\nM1,t1\n")
    zf.writestr("stop_times.txt", "trip_id,stop_id\n" + "".join(f"t1,{f['id']}\n" for f in metro))
    zf.writestr("stops.txt", "stop_id,stop_lat,stop_lon\n" + "".join(f"{f['id']},{f['la']},{f['lo']}\n" for f in metro))
print(f"{len(sez)} sezioni, {len(acc)} con accessibilita', {len(metro)} fermate M1, {sum(len(c['zone']) for c in D['omi'] if c['c'] == 1272)} zone OMI di Torino in {rad}")
