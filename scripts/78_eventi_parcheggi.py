#!/usr/bin/env python3
"""
78_eventi_parcheggi.py  -  Risultato 6 v2: i 4 luoghi di evento, i parcheggi e le fermate vicine.

Cosa fa
-------
1. Trova in OpenStreetMap le coordinate dei 4 luoghi di evento elencati in
   data/ref/eventi_luoghi.json (stadi, palasport, fiera). Il file NON contiene le
   coordinate: qui si cercano per nome OSM e si controllano contro le posizioni attese.
2. Per ogni luogo calcola, con distanze in linea d'aria (haversine):
   - quanti parcheggi e quanti posti ci sono entro 500 m e 1.000 m, e i 10 piu' grandi;
   - quante fermate del trasporto pubblico cadono entro 500 m e quante corse/ora ci sono
     la sera (ore 18-23) in un giorno feriale, un sabato e una domenica tipo;
   - i parcheggi di interscambio vicini entro 3.000 m (solo informazione);
   - quante auto ci si aspetta per un evento pieno e quante ne restano senza posto.

Cosa legge
----------
  data/ref/eventi_luoghi.json                          (i 4 luoghi e i parametri auto)
  data/otp/rete/torino_cintura.osm.pbf                 (OpenStreetMap, nomi e geometrie)
  data/processed/risultato6_v2/luoghi.json             (i 5.087 luoghi delle fermate)
  data/processed/risultato6_v2/parcheggi.json          (tutti i parcheggi censiti)
  data/processed/risultato6_v2/parcheggi_funzione.json (classe e punti a favore dei parcheggi)
  data/raw/gtt_gtfs_20261003_224530.zip                (orari programmati del trasporto)

Cosa scrive
-----------
  data/processed/risultato6_v2/eventi.json
  docs/RAPPORTO_R6V2_EVENTI.txt

Come si lancia
--------------
  python scripts\\78_eventi_parcheggi.py
"""
import csv
import io
import json
import math
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import osmium

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
EVENTI_REF = RADICE / "data" / "ref" / "eventi_luoghi.json"
PBF = RADICE / "data" / "otp" / "rete" / "torino_cintura.osm.pbf"
LUOGHI = RADICE / "data" / "processed" / "risultato6_v2" / "luoghi.json"
PARCHEGGI = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi.json"
FUNZIONE = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi_funzione.json"
GTFS = RADICE / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"
OUT_EVENTI = RADICE / "data" / "processed" / "risultato6_v2" / "eventi.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_EVENTI.txt"

# --- parametri del piano (NON cambiare) ---
TIPI_PARCHEGGIO = ("interscambio_ufficiale", "garage_5t", "park_ride_osm", "osm_pubblico")
RAGGIO_500 = 500.0
RAGGIO_1000 = 1000.0
RAGGIO_INTERSCAMBIO = 3000.0
GIORNI_SERA = ("feriale", "sabato", "domenica")
DATE_SERA = {"feriale": "20261012", "sabato": "20261017", "domenica": "20261018"}
ORE_SERA = (18, 19, 20, 21, 22, 23)
GIORNI_SETTIMANA = ["monday", "tuesday", "wednesday", "thursday", "friday",
                    "saturday", "sunday"]
# limiti attesi per il controllo delle coordinate (planimetria del piano)
LIMITI_TORINO = (44.95, 7.55, 45.16, 7.76)
POSIZIONI_ATTESE = {
    "allianz": (45.110, 7.641),
    "olimpico": (45.042, 7.650),
    "inalpi": (45.043, 7.652),
    "oval": (45.031, 7.663),
}
TOLLERANZA_M = 1500.0
LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def area_m2(punti):
    """Area di una via chiusa, con la formula del laccio in metri proiettati."""
    if len(punti) < 4:
        return 0.0
    kx = FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF))
    xs = [lon * kx for lat, lon in punti]
    ys = [lat * FATTORE_GRADI_M for lat, lon in punti]
    s = 0.0
    for i in range(len(xs)):
        j = (i + 1) % len(xs)
        s += xs[i] * ys[j] - xs[j] * ys[i]
    return abs(s) / 2.0


# --- PASSO E1: i luoghi di evento su OpenStreetMap --------------------------------

def tag_evento(tags):
    if tags.get("leisure") in ("stadium", "sports_centre", "sports_hall"):
        return True
    if tags.get("building") in ("stadium", "sports_hall", "yes"):
        return True
    if tags.get("amenity") in ("events_venue", "exhibition_centre"):
        return True
    if tags.get("tourism") == "attraction":
        return True
    if tags.get("man_made"):
        return True
    return False


class CercaLuoghi(osmium.SimpleHandler):
    def __init__(self, nomi_osm):
        super().__init__()
        self.nomi = [(id_luogo, nome.lower()) for id_luogo, nome in nomi_osm.items()]
        self.trovati = defaultdict(list)

    def _quale(self, tags):
        nome = (tags.get("name") or "").lower()
        if not nome:
            return None
        for id_luogo, osm_nome in self.nomi:
            if osm_nome in nome:
                return id_luogo
        return None

    def node(self, n):
        id_luogo = self._quale(n.tags)
        if id_luogo is None or not tag_evento(n.tags):
            return
        self.trovati[id_luogo].append({
            "id_osm": f"node {n.id}", "tipo_osm": "node",
            "lat": n.location.lat, "lon": n.location.lon, "area_m2": 0.0,
            "leisure": n.tags.get("leisure"), "name": n.tags.get("name"),
        })

    def way(self, w):
        id_luogo = self._quale(w.tags)
        if id_luogo is None or not tag_evento(w.tags):
            return
        punti = [(nd.location.lat, nd.location.lon) for nd in w.nodes if nd.location.valid()]
        if not punti:
            return
        self.trovati[id_luogo].append({
            "id_osm": f"way {w.id}", "tipo_osm": "way",
            "lat": sum(p[0] for p in punti) / len(punti),
            "lon": sum(p[1] for p in punti) / len(punti),
            "area_m2": area_m2(punti) if w.is_closed() else 0.0,
            "leisure": w.tags.get("leisure"), "name": w.tags.get("name"),
        })


def trova_luoghi_evento(luoghi_ref):
    """Ritorna {id: [candidati ordinati]} per i luoghi trovati e l'elenco dei non trovati."""
    nomi_osm = {l["id"]: l["osm_nome"] for l in luoghi_ref}
    handler = CercaLuoghi(nomi_osm)
    handler.apply_file(str(PBF), locations=True)
    scelti = {}
    mancanti = []
    for l in luoghi_ref:
        candidati = handler.trovati.get(l["id"], [])
        if not candidati:
            # Il piano dice FERMO. In OpenStreetMap (estratto per OTP) l'oggetto non ha
            # questo nome: NON inventiamo coordinate. Segnaliamo e proseguiamo con gli altri.
            mancanti.append(l["id"])
            continue
        candidati.sort(key=lambda c: (c["leisure"] == "stadium", c["area_m2"]), reverse=True)
        scelti[l["id"]] = candidati
    return scelti, mancanti


def controlla_coordinate(id_luogo, scelto):
    lat, lon = scelto["lat"], scelto["lon"]
    lat_min, lon_min, lat_max, lon_max = LIMITI_TORINO
    if not (lat_min <= lat <= lat_max and lon_min <= lon <= lon_max):
        sys.exit(f"PASSO E1: FERMO - {id_luogo} fuori dai confini di Torino "
                 f"({lat:.5f}, {lon:.5f})")
    if id_luogo in POSIZIONI_ATTESE:
        la, lo = POSIZIONI_ATTESE[id_luogo]
        d = haversine_m(lat, lon, la, lo)
        if d > TOLLERANZA_M:
            sys.exit(f"PASSO E1: FERMO - {id_luogo} a {d:.0f} m dal punto atteso "
                     f"(oltre {TOLLERANZA_M:.0f} m)")
        return d
    return None


# --- PASSO E2: fermate e orari del trasporto pubblico -----------------------------

def servizi_attivi(zf, giorno):
    import datetime
    data = datetime.date(int(giorno[:4]), int(giorno[4:6]), int(giorno[6:8]))
    colonna = GIORNI_SETTIMANA[data.weekday()]
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


def corse_sera_per_fermata():
    """Ritorna {giorno: {stop_id: [partenze per ora 0-23]}} per i tre giorni tipo."""
    zf = zipfile.ZipFile(GTFS)
    # per ogni giorno, le corse attive e a quale giorno appartengono
    giorno_per_corsa = defaultdict(list)
    for etichetta in GIORNI_SERA:
        attivi = servizi_attivi(zf, DATE_SERA[etichetta])
        with zf.open("trips.txt") as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                if r["service_id"] in attivi:
                    giorno_per_corsa[r["trip_id"]].append(etichetta)
    print(f"  corse attive nei tre giorni tipo: {len(giorno_per_corsa)}")
    ore = {g: defaultdict(lambda: [0] * 24) for g in GIORNI_SERA}
    with zf.open("stop_times.txt") as f:
        for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
            etichette = giorno_per_corsa.get(r["trip_id"])
            if not etichette:
                continue
            orario = r.get("departure_time") or r.get("arrival_time") or ""
            if not orario:
                continue
            try:
                ora = int(orario.split(":")[0]) % 24
            except ValueError:
                continue
            sid = r["stop_id"]
            for g in etichette:
                ore[g][sid][ora] += 1
    return ore


def corse_sera_luogo(ore_giorno, stop_ids):
    """Corse/ora medie (ore 18-23) per un insieme di fermate."""
    tot = 0
    for sid in stop_ids:
        v = ore_giorno.get(sid)
        if v:
            tot += sum(v[h] for h in ORE_SERA)
    return tot / len(ORE_SERA)


# --- PASSO E2: parcheggi vicini ---------------------------------------------------

def posti_di(p):
    if p.get("posti_dichiarati"):
        return p["posti_dichiarati"], "dichiarati"
    if p.get("posti_stimati"):
        return p["posti_stimati"], "stimati"
    return 0, "nessuno"


def parcheggi_vicini(evento, parcheggi):
    vicini = []
    for p in parcheggi:
        if p["tipo"] not in TIPI_PARCHEGGIO:
            continue
        d = haversine_m(evento["lat"], evento["lon"], p["lat"], p["lon"])
        if d > RAGGIO_1000:
            continue
        posti, origine = posti_di(p)
        vicini.append({
            "id": p["id"], "nome": p["nome"], "tipo": p["tipo"],
            "dist_m": round(d), "posti": posti, "posti_origine": origine,
            "a_pagamento": p.get("a_pagamento"),
        })
    entro500 = [v for v in vicini if v["dist_m"] <= RAGGIO_500]
    fuori500 = [v for v in vicini if v["dist_m"] > RAGGIO_500]
    return {
        "n_500": len(entro500),
        "posti_500": sum(v["posti"] for v in entro500),
        "solo_stimati_500": sum(1 for v in entro500 if v["posti_origine"] == "stimati"),
        "senza_posti_500": sum(1 for v in entro500 if v["posti_origine"] == "nessuno"),
        "n_1000": len(vicini),
        "posti_1000": sum(v["posti"] for v in vicini),
        "solo_stimati_1000": sum(1 for v in vicini if v["posti_origine"] == "stimati"),
        "senza_posti_1000": sum(1 for v in vicini if v["posti_origine"] == "nessuno"),
        "dieci_piu_grandi_1000": sorted(vicini, key=lambda v: -v["posti"])[:10],
    }


def interscambi_vicini(evento, funzione):
    """Parcheggi 'solo_sulla_carta' e 'potenziale' con forza >= 2 + i 5 ufficiali, entro 3 km."""
    sel = []
    for f in funzione:
        ufficiale = f["tipo"] == "interscambio_ufficiale"
        potente = f["classe"] == "solo_sulla_carta" or (
            f["classe"] == "potenziale" and (f["forza"] or 0) >= 2)
        if not (ufficiale or potente):
            continue
        d = haversine_m(evento["lat"], evento["lon"], f["lat"], f["lon"])
        if d > RAGGIO_INTERSCAMBIO:
            continue
        sel.append({
            "id": f["id"], "nome": f["nome"], "classe": f["classe"],
            "dist_m": round(d), "posti": f["posti"] or 0, "a_pagamento": f["a_pagamento"],
        })
    sel.sort(key=lambda v: -v["posti"])
    return sel


# --- main -------------------------------------------------------------------------

def main():
    for p in (EVENTI_REF, PBF, LUOGHI, PARCHEGGI, FUNZIONE, GTFS):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    ref = json.loads(EVENTI_REF.read_text(encoding="utf-8"))
    luoghi_ref = ref["luoghi"]
    quota_auto = ref["parametri_auto"]["quota_auto"]
    per_auto = ref["parametri_auto"]["persone_per_auto"]

    print("PASSO E1: cerco i luoghi di evento in OpenStreetMap...")
    scelti, mancanti = trova_luoghi_evento(luoghi_ref)
    posizioni = {}
    righe_e1 = []
    for l in luoghi_ref:
        candidati = scelti.get(l["id"])
        if not candidati:
            print(f"  {l['id']:9s} NON TROVATO in OSM (nome OSM atteso: '{l['osm_nome']}')")
            righe_e1.append(f"  {l['nome']}: NON TROVATO in OpenStreetMap col nome "
                            f"'{l['osm_nome']}' - FERMO per questo luogo, nessuna coordinata "
                            f"inventata (vedi limiti)")
            continue
        scelto = candidati[0]
        d_atteso = controlla_coordinate(l["id"], scelto)
        posizioni[l["id"]] = scelto
        print(f"  {l['id']:9s} {scelto['id_osm']:14s} {scelto['name']!r} "
              f"({scelto['lat']:.5f}, {scelto['lon']:.5f}) area={scelto['area_m2']:.0f} m2 "
              f"candidati={len(candidati)}")
        righe_e1.append(f"  {l['nome']}: {scelto['id_osm']} '{scelto['name']}' "
                        f"({scelto['lat']:.5f}, {scelto['lon']:.5f}) - "
                        f"{d_atteso:.0f} m dal punto atteso; {len(candidati)} candidati trovati")
    print("PASSO E1: " + ("OK" if not mancanti else f"PARZIALE - non trovati: {', '.join(mancanti)}"))
    righe_e1.append("")
    righe_e1.append("  Candidati trovati per ogni luogo (nome OSM | id | area):")
    for l in luoghi_ref:
        cand = scelti.get(l["id"], [])
        if not cand:
            continue
        righe_e1.append(f"    {l['nome']}: " + "; ".join(
            f"{c['name']} [{c['id_osm']}, {c['area_m2']:.0f} m2]" for c in cand))

    print("PASSO E2: leggo luoghi, parcheggi e funzione dei parcheggi...")
    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    parcheggi = json.loads(PARCHEGGI.read_text(encoding="utf-8"))["parcheggi"]
    funzione = json.loads(FUNZIONE.read_text(encoding="utf-8"))["parcheggi"]

    print("PASSO E2: conto le corse serali di feriale, sabato e domenica...")
    ore_sera = corse_sera_per_fermata()

    eventi = []
    for l in luoghi_ref:
        if l["id"] not in posizioni:
            continue
        scelto = posizioni[l["id"]]
        evento = {"id": l["id"], "nome": l["nome"], "tipo": l["tipo"],
                  "lat": round(scelto["lat"], 5), "lon": round(scelto["lon"], 5),
                  "id_osm": scelto["id_osm"], "capienza": l["capienza"],
                  "capienza_nota": l["capienza_nota"], "fonti": l["fonti"]}

        evento.update(parcheggi_vicini(evento, parcheggi))

        # fermate del trasporto pubblico entro 500 m
        fermate = [x for x in luoghi
                   if haversine_m(evento["lat"], evento["lon"], x["lat"], x["lon"]) <= RAGGIO_500]
        stop_ids = [sid for x in fermate for sid in x["stop_ids"]]
        evento["fermate_500"] = len(fermate)
        for g in GIORNI_SERA:
            evento[f"corse_ora_sera_{g}"] = round(corse_sera_luogo(ore_sera[g], stop_ids), 2)

        # parcheggi di interscambio vicini (solo informazione)
        evento["interscambi_vicini"] = interscambi_vicini(evento, funzione)

        # auto stimate e posti mancanti
        auto = l["capienza"] * quota_auto / per_auto
        evento["auto_stimate"] = round(auto)
        evento["auto_stimate_esatte"] = round(auto, 1)
        evento["mancano"] = max(0, evento["auto_stimate"] - evento["posti_1000"])
        eventi.append(evento)

    # --- controlli ---
    allianz = next((e for e in eventi if e["id"] == "allianz"), None)
    if allianz is not None:
        atteso_allianz = 41507 * quota_auto / per_auto
        if abs(allianz["auto_stimate"] - round(atteso_allianz)) > 1:
            sys.exit(f"PASSO E2: FERMO - auto stimate Allianz {allianz['auto_stimate']}, "
                     f"attese {round(atteso_allianz)}")
    for e in eventi:
        if e["mancano"] < 0:
            sys.exit(f"PASSO E2: FERMO - 'mancano' negativo per {e['id']}")
        if e["posti_500"] > e["posti_1000"]:
            sys.exit(f"PASSO E2: FERMO - posti 500 m > posti 1.000 m per {e['id']}")

    OUT_EVENTI.parent.mkdir(parents=True, exist_ok=True)
    OUT_EVENTI.write_text(json.dumps({
        "nota": "Coordinate dei luoghi trovate in OpenStreetMap dallo script 78; capienze "
                "[STIMATO] da fonti web; auto per evento = capienza x 50% / 2,5 [STIMATO]; "
                "corse/ora [PROGRAMMATO]; riempimento parcheggi [DATI SCARSI].",
        "attenzione": ("allianz manca: nell'estratto OpenStreetMap usato (torino_cintura.osm.pbf) "
                       "l'Allianz Stadium non ha un nome, quindi la ricerca per nome non lo trova. "
                       "Nessuna coordinata inventata. Vedi docs/RAPPORTO_R6V2_EVENTI.txt.")
        if mancanti else None,
        "parametri_auto": ref["parametri_auto"],
        "mancanti": [l["nome"] for l in luoghi_ref if l["id"] in mancanti],
        "eventi": eventi,
    }, ensure_ascii=False), encoding="utf-8")

    # --- rapporto ---
    righe = []
    righe.append("RAPPORTO R6 v2 - LUOGHI DI EVENTO, PARCHEGGI E FERMATE VICINE")
    righe.append("Distanze in linea d'aria (haversine). Generato da scripts/78_eventi_parcheggi.py.")
    righe.append("")
    righe.append("== Coordinate trovate in OpenStreetMap (controllate) ==")
    righe.extend(righe_e1)
    righe.append("")
    righe.append("== Tabella riassuntiva ==")
    righe.append("  evento | capienza | auto stimate | posti 500 m | posti 1.000 m | mancano | "
                 "fermate 500 m | corse/ora sera (fer/sab/dom)")
    for e in eventi:
        righe.append(
            f"  {e['nome'][:34]:34s} {e['capienza']:>7d} {e['auto_stimate']:>7d} "
            f"{e['posti_500']:>6d} {e['posti_1000']:>6d} {e['mancano']:>6d} "
            f"{e['fermate_500']:>5d}   {e['corse_ora_sera_feriale']:.1f} / "
            f"{e['corse_ora_sera_sabato']:.1f} / {e['corse_ora_sera_domenica']:.1f}")
    righe.append("")
    for e in eventi:
        righe.append(f"== {e['nome']} ({e['lat']:.5f}, {e['lon']:.5f}) ==")
        righe.append(f"  OSM: {e['id_osm']}, tipo {e['tipo']}")
        righe.append(f"  capienza {e['capienza']} [{e['capienza_nota']}]")
        righe.append(f"  auto stimate [STIMATO]: {e['auto_stimate']} "
                     f"(capienza x 0,5 / 2,5); mancano: {e['mancano']} posti entro 1.000 m")
        righe.append(f"  parcheggi aperti entro 500 m: {e['n_500']} ({e['posti_500']} posti; "
                     f"{e['solo_stimati_500']} con posti solo stimati, "
                     f"{e['senza_posti_500']} senza posti)")
        righe.append(f"  parcheggi aperti entro 1.000 m: {e['n_1000']} ({e['posti_1000']} posti; "
                     f"{e['solo_stimati_1000']} con posti solo stimati, "
                     f"{e['senza_posti_1000']} senza posti)")
        righe.append("  i 10 piu' grandi entro 1.000 m (nome | tipo | distanza | posti | origine | tariffa):")
        for v in e["dieci_piu_grandi_1000"]:
            righe.append(f"    {v['nome'][:32]:32s} {v['tipo'][:20]:20s} {v['dist_m']:>5d} m "
                         f"{v['posti']:>5d} {v['posti_origine']:>9s} a_pagamento={v['a_pagamento']}")
        righe.append(f"  fermate del trasporto pubblico entro 500 m: {e['fermate_500']}")
        righe.append(f"  corse/ora la sera (18-23) [PROGRAMMATO]: feriale "
                     f"{e['corse_ora_sera_feriale']:.2f}, sabato {e['corse_ora_sera_sabato']:.2f}, "
                     f"domenica {e['corse_ora_sera_domenica']:.2f}")
        righe.append("  parcheggi di interscambio vicini entro 3.000 m (solo informazione: "
                     "vicini in linea d'aria, NON un collegamento verificato; i 10 piu' grandi):")
        for v in e["interscambi_vicini"][:10]:
            righe.append(f"    {v['nome'][:32]:32s} {v['classe'][:18]:18s} {v['dist_m']:>5d} m "
                         f"{v['posti']:>5d} posti a_pagamento={v['a_pagamento']}")
        if not e["interscambi_vicini"]:
            righe.append("    nessuno")
        righe.append("")
    righe.append("== Limiti ==")
    if mancanti:
        righe.append("- ATTENZIONE: l'Allianz Stadium NON ha un nome nell'estratto OpenStreetMap usato"
                     " (torino_cintura.osm.pbf): la ricerca per nome non lo trova, quindi manca dai"
                     " dati. Il piano dice 'FERMO e non inventare coordinate': non e' stata inventata"
                     " nessuna posizione. Nella zona attesa (45,110; 7,641) ci sono vie chiuse senza"
                     " nome (es. way 119509840, ~69.000 m2, 53 m dal punto atteso) che sono l'impianto.")
    righe.append("- Le capienze vengono da fonti web diverse e qualche volta non concordano "
                 "(vedi le note di ogni luogo).")
    righe.append("- Le auto per evento sono ipotizzate: 50% di chi arriva in auto, 2,5 persone per "
                 "auto [STIMATO]. Non sono dati misurati.")
    righe.append("- I posti dei parcheggi stimati da OpenStreetMap hanno un errore di circa il 30%.")
    righe.append("- Non sappiamo nulla del parcheggio gratuito o abusivo lungo le strade.")
    righe.append("- Le distanze sono in linea d'aria, non a piedi.")
    righe.append("- Le corse sono gli orari programmati [PROGRAMMATO], non quelli reali.")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT_EVENTI}")
    print(f"Scritto: {RAPPORTO}")
    for e in eventi:
        print(f"  {e['id']:9s} auto={e['auto_stimate']:5d} posti500={e['posti_500']:5d} "
              f"posti1000={e['posti_1000']:5d} mancano={e['mancano']:5d} "
              f"fermate={e['fermate_500']:3d} sera(fer)={e['corse_ora_sera_feriale']:.1f}")


if __name__ == "__main__":
    sys.exit(main())
