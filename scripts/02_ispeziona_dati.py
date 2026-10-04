#!/usr/bin/env python3
"""
02_ispeziona_dati.py  -  controlla cosa c'e' davvero nei file scaricati.

Legge gli ultimi file in data/raw e stampa un rapporto, e lo salva anche in
docs/RAPPORTO_ISPEZIONE.txt (cosi' puoi incollarlo nella chat).

Serve per: GTFS (date di validita', numero di linee e fermate), 5T (numero
di sensori, ora del dato), GTT tempo reale (numero di mezzi, ora del dato).
Per leggere i file GTT in tempo reale serve una libreria, da installare una volta:
    pip install gtfs-realtime-bindings
Se non la installi, il resto del rapporto funziona lo stesso.
"""
import csv
import io
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent

def trova_radice():
    """La cartella del progetto e' quella chiamata GTT, ovunque venga lanciato lo script."""
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    candidata = Path.home() / "Desktop" / "GTT"
    if candidata.is_dir():
        return candidata
    return AQUI.parent


RADICE = trova_radice()
RAW = RADICE / "data" / "raw"
DOCS = RADICE / "docs"
DOCS.mkdir(exist_ok=True)

righe = []


def p(testo=""):
    print(testo)
    righe.append(testo)


def ultimo(prefisso):
    trovati = sorted(RAW.glob(prefisso + "*"))
    return trovati[-1] if trovati else None


def csv_da_zip(z, nome):
    with z.open(nome) as f:
        return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))


def ispeziona_gtfs():
    p("== GTT orari programmati (GTFS) ==")
    f = ultimo("gtt_gtfs_")
    if not f:
        p("  file non trovato: lancia prima 01_scarica_dati.py")
        return
    p(f"  file: {f.name}  ({f.stat().st_size:,} byte)")
    with zipfile.ZipFile(f) as z:
        nomi = z.namelist()
        p(f"  contiene: {', '.join(nomi)}")
        if "feed_info.txt" in nomi:
            for r in csv_da_zip(z, "feed_info.txt"):
                p(f"  feed_info: {dict(r)}")
        else:
            p("  feed_info.txt assente (nessuna data di validita' dichiarata)")
        if "routes.txt" in nomi:
            p(f"  linee: {len(csv_da_zip(z, 'routes.txt'))}")
        if "stops.txt" in nomi:
            fermate = csv_da_zip(z, "stops.txt")
            p(f"  fermate: {len(fermate)}")
        if "calendar.txt" in nomi:
            cal = csv_da_zip(z, "calendar.txt")
            if cal:
                p(f"  calendar: da {min(r['start_date'] for r in cal)} a {max(r['end_date'] for r in cal)}")
        if "calendar_dates.txt" in nomi:
            cd = csv_da_zip(z, "calendar_dates.txt")
            if cd:
                p(f"  calendar_dates: da {min(r['date'] for r in cd)} a {max(r['date'] for r in cd)}")
        if "stop_times.txt" in nomi:
            with z.open("stop_times.txt") as fh:
                n = sum(1 for _ in fh) - 1
            p(f"  righe stop_times (passaggi programmati): {n:,}")
    p("  -> controlla che le date coprano oggi (" + datetime.now().strftime("%Y-%m-%d") + ")")


def nome_locale(tag):
    """Toglie lo schema XML dal nome: '{https://...}FDT_data' diventa 'FDT_data'."""
    return tag.rsplit("}", 1)[-1]


def ispeziona_5t():
    p("\n== 5T flussi di traffico ==")
    f = ultimo("5t_flussi_")
    if not f:
        p("  file non trovato")
        return
    radice = ET.parse(f).getroot()
    sensori = [e for e in radice.iter() if nome_locale(e.tag) == "FDT_data"]
    p(f"  file: {f.name}")
    p(f"  ora del dato (UTC): {radice.attrib.get('start_time')} -> {radice.attrib.get('end_time')}")
    p(f"  sensori: {len(sensori)}")

    def speedflow(s):
        for c in s:
            if nome_locale(c.tag) == "speedflow":
                return c.attrib
        return None

    acc0 = [s for s in sensori if s.attrib.get("accuracy") == "0"]
    con_flusso = [s for s in sensori if speedflow(s) and float(speedflow(s).get("flow", 0) or 0) > 0]
    p(f"  sensori con accuracy=0: {len(acc0)}")
    p(f"  sensori con flusso > 0: {len(con_flusso)}")
    strade = {s.attrib.get("Road_name") for s in sensori}
    p(f"  strade distinte: {len(strade)}")
    try:
        lat = [float(s.attrib["lat"]) for s in sensori]
        lng = [float(s.attrib["lng"]) for s in sensori]
        p(f"  area coperta: lat {min(lat):.3f}-{max(lat):.3f}, lng {min(lng):.3f}-{max(lng):.3f}")
    except (KeyError, ValueError):
        pass
    if sensori:
        p(f"  esempio: {dict(sensori[0].attrib)} speedflow: {speedflow(sensori[0])}")


def ispeziona_rt():
    p("\n== GTT tempo reale ==")
    try:
        from google.transit import gtfs_realtime_pb2
    except ImportError:
        p("  libreria mancante: nella console scrivi  %pip install gtfs-realtime-bindings  poi rilancia")
        return
    for prefisso, etichetta in [("gtt_vehicle_position_", "posizioni mezzi"),
                                ("gtt_trip_update_", "ritardi corse"),
                                ("gtt_alerts_", "avvisi")]:
        f = ultimo(prefisso)
        if not f:
            p(f"  {etichetta}: file non trovato")
            continue
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            feed.ParseFromString(f.read_bytes())
        except Exception as e:
            p(f"  {etichetta}: file non leggibile come GTFS-RT ({e})")
            continue
        ts = datetime.fromtimestamp(feed.header.timestamp, timezone.utc).isoformat() if feed.header.timestamp else "n/d"
        p(f"  {etichetta}: {len(feed.entity)} elementi, orario del feed {ts}")
        if feed.entity:
            e0 = feed.entity[0]
            if e0.HasField("vehicle"):
                v = e0.vehicle
                p(f"     esempio: linea {v.trip.route_id}, pos {v.position.latitude:.5f},{v.position.longitude:.5f}")


def main():
    ispeziona_gtfs()
    ispeziona_5t()
    ispeziona_rt()
    (DOCS / "RAPPORTO_ISPEZIONE.txt").write_text("\n".join(righe), encoding="utf-8")
    print(f"\nRapporto salvato in {DOCS / 'RAPPORTO_ISPEZIONE.txt'}")


if __name__ == "__main__":
    main()
