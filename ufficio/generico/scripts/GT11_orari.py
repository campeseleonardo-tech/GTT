# -*- coding: utf-8 -*-
"""
GT11_orari.py - script del runner (0 token). Uso: python GT11_orari.py <cartella GTT>
Crea data/processed/orari_fermate.js con TUTTI gli orari di partenza per fermata, linea e tipo di giorno (feriale / sabato / domenica),
presi dal GTFS gia' scaricato. Serve alla scheda di una fermata ("prossimi passaggi"). Non modifica nessun altro file.

Formato: window.ORARI={"v":versione,"t":["fer","sab","dom"],"s":{"<id fermata>":{"<linea>":[[minuti feriale],[minuti sabato],[minuti domenica]]}}};
I minuti sono dalla mezzanotte (oltre 1440 = dopo mezzanotte), ordinati. Riusa le stesse regole di 04_genera_mappa.py per i giorni tipo.
"""
import csv
import importlib.util
import io
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


def main():
    repo = Path(sys.argv[1]).resolve()
    sc = repo / "scripts" / "04_genera_mappa.py"
    spec = importlib.util.spec_from_file_location("genera_mappa", sc)
    gm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gm)                       # solo definizioni: main() non parte (c'e' il controllo __name__)
    ctl = repo / "agenti" / "GT11-orari-fermate"
    ctl.mkdir(parents=True, exist_ok=True)
    f = gm.ultimo("gtt_gtfs_")
    z = zipfile.ZipFile(f)
    info = gm.leggi_csv(z, "feed_info.txt")[0]
    giorni = gm.date_riferimento(gm.data_gtfs(info["feed_start_date"]), gm.data_gtfs(info["feed_end_date"]))
    cal = gm.leggi_csv(z, "calendar.txt")
    ecc = gm.leggi_csv(z, "calendar_dates.txt") if "calendar_dates.txt" in z.namelist() else []
    attivi = [gm.servizi_attivi(cal, ecc, giorni[k]) for k in gm.TIPI_GIORNO]
    rotte = {r["route_id"]: (r["route_short_name"] or r["route_id"]) for r in gm.leggi_csv(z, "routes.txt")}
    viaggi = {}
    for r in gm.leggi_csv(z, "trips.txt"):
        viaggi[r["trip_id"]] = (rotte.get(r["route_id"], r["route_id"]), tuple(r["service_id"] in a for a in attivi))
    out = defaultdict(lambda: defaultdict(lambda: [set(), set(), set()]))
    with z.open("stop_times.txt") as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding="utf-8-sig"))
        ix = {n: i for i, n in enumerate(next(rd))}
        i_t, i_d, i_a, i_s = ix["trip_id"], ix["departure_time"], ix["arrival_time"], ix["stop_id"]
        for r in rd:
            v = viaggi.get(r[i_t])
            if not v:
                continue
            ora = r[i_d] or r[i_a]
            if len(ora) < 5:
                continue
            try:
                minuti = int(ora[:2]) * 60 + int(ora[3:5])
            except ValueError:
                continue
            for k in range(3):
                if v[1][k]:
                    out[r[i_s]][v[0]][k].add(minuti)
    s = {sid: {ln: [sorted(x) for x in tre] for ln, tre in linee.items()} for sid, linee in out.items()}
    dest = repo / "data" / "processed"
    dest.mkdir(parents=True, exist_ok=True)
    js = "window.ORARI=" + json.dumps({"v": info.get("feed_version"), "t": gm.TIPI_GIORNO, "s": s}, separators=(",", ":")) + ";\n"
    (dest / "orari_fermate.js").write_text(js, encoding="utf-8")
    n_pass = sum(len(x) for linee in s.values() for tre in linee.values() for x in tre)
    giorni_txt = {k: str(v) for k, v in giorni.items()}
    (ctl / "ORARI.md").write_text(
        f"# GT11 - orari per fermata\n\nFeed: {f.name} (versione {info.get('feed_version')})\nGiorni tipo: {giorni_txt}\n"
        f"Fermate con orari: {len(s)}\nPassaggi totali (3 tipi di giorno): {n_pass}\nFile: data/processed/orari_fermate.js ({len(js) / 1e6:.1f} MB)\n",
        encoding="utf-8")
    print(f"fermate {len(s)}, passaggi {n_pass}, file {len(js) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
