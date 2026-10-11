#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import sys
import time
import zipfile
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SEZIONI = RADICE / "data/processed/sezioni_torino.json"
CATALOGO = RADICE / "data/processed/catalogo"
GTFS = RADICE / "data/raw/gtt_gtfs_20261003_224530.zip"
OSM_TAGLIATO = RADICE / "data/otp/rete/torino_cintura.osm.pbf"
JAVA_HOME = RADICE / "data/otp/jdk-25.0.4.1+1-jre"
OUT = RADICE / "data/processed/accessibilita.json"
RAPPORTO = RADICE / "docs/RAPPORTO_ACCESSIBILITA.txt"

CENTRO = (45.0716, 7.6869)
GRUPPI = ["scuole", "salute", "cibo", "fermate", "verde"]

TAG_VERDE = {
    "leisure": {"park", "garden", "playground", "pitch", "dog_park", "golf_course"},
    "landuse": {"cemetery", "forest", "grass", "recreation_ground", "village_green", "meadow"},
}

def log(msg):
    print(msg, flush=True)

def centroide(anello):
    """Centroide d'area di un anello [[lat,lon],...]; None se area nulla."""
    a = cx = cy = 0.0
    n = len(anello)
    for i in range(n - 1):
        x0, y0 = anello[i]
        x1, y1 = anello[i + 1]
        f = x0 * y1 - x1 * y0
        a += f
        cx += (x0 + x1) * f
        cy += (y0 + y1) * f
    if abs(a) < 1e-15:
        return None
    # anelli [lat,lon]: x=lat, y=lon -> centroide (lat, lon)
    return (cx / (3 * a), cy / (3 * a))

def carica_sezioni():
    sezioni = json.loads(SEZIONI.read_text(encoding="utf-8"))
    out = []
    for s in sezioni:
        if s.get("p", 0) <= 0 or not s.get("g"):
            continue
        cen = centroide(s["g"][0]) or (s["g"][0][0][0], s["g"][0][0][1])
        out.append({
            "id": s["id"],
            "comune": s["c"],
            "res": s["p"],
            "lat": cen[0],
            "lon": cen[1],
            "torino": s["c"] == 1272  # True if in Torino (comune 1272)
        })
    return out

def punti_da_catalogo(gruppo):
    d = json.loads((CATALOGO / f"{gruppo}.json").read_text(encoding="utf-8"))
    punti = []
    for ds in d["dati"]:
        for el in ds.get("elementi", []):
            try:
                punti.append((float(el[0]), float(el[1])))
            except (TypeError, ValueError, IndexError):
                continue
    return punti

def fermate_gtfs():
    import csv as csvmod
    fermate = []
    with zipfile.ZipFile(GTFS) as z:
        righe = z.read("stops.txt").decode("utf-8-sig").splitlines()
    lettori = csvmod.reader(righe)
    intest = next(lettori)
    i_la, i_lo = intest.index("stop_lat"), intest.index("stop_lon")
    i_lt = intest.index("location_type") if "location_type" in intest else None
    for c in lettori:
        if len(c) <= max(i_la, i_lo):
            continue
        if i_lt is not None and c[i_lt] not in ("", "0"):
            continue
        try:
            fermate.append((float(c[i_la]), float(c[i_lo])))
        except ValueError:
            continue
    return fermate

def verde_da_osm():
    import osmium
    punti = []

    class Verde(osmium.SimpleHandler):
        def way(self, w):
            if not w.is_closed():
                return
            if (w.tags.get("leisure") in TAG_VERDE["leisure"]
                    or w.tags.get("landuse") in TAG_VERDE["landuse"]):
                la = lo = 0.0
                n = 0
                for nd in w.nodes:
                    if nd.location.valid():
                        la += nd.location.lat
                        lo += nd.location.lon
                        n += 1
                if n >= 3:
                    punti.append((la / n, lo / n))

    Verde().apply_file(str(OSM_TAGLIATO), locations=True)
    return punti

def carica_destinazioni():
    dest = {
        "scuole": punti_da_catalogo("istruzione"),
        "salute": punti_da_catalogo("salute"),
        "cibo": punti_da_catalogo("commercio"),
        "fermate": fermate_gtfs(),
        "verde": verde_da_osm(),
    }
    for g in GRUPPI:
        log(f"  destinazioni {g}: {len(dest[g])}")
    return dest

def carica_servizi_osm_cintura():
    """Carica servizi da OSM nella cintura (fuori Torino)."""
    # Questo script crea data/processed/servizi_osm_cintura.json
    # E lo usa qui per evitare duplicare il codice
    import json
    os_path = Path("data/processed/servizi_osm_cintura.json")
    if os_path.exists():
        with open(os_path, 'r') as f:
            data = json.load(f)
        # Convert to format needed by script
        osm_servizi = {
            "scuole": [],
            "salute": [],
            "cibo": []
        }
        for group in ["scuole", "salute", "cibo"]:
            points = []
            for p in data["servizi"][group]:
                points.append((p["lat"], p["lon"]))
            osm_servizi[group] = points
        return osm_servizi
    return {}

def avvia_rete():
    os.environ["JAVA_HOME"] = str(JAVA_HOME)
    # heap fisso: la macchina ha 8 GB, Python e R5 devono convivere
    os.environ.setdefault("_JAVA_OPTIONS", "-Xmx3g")
    import geopandas as gpd
    from r5py import TransportNetwork
    log("Rete R5 in costruzione (prima volta: scarica r5.jar ~ 100 MB)...")
    t0 = time.time()
    rete = TransportNetwork(str(OSM_TAGLIATO), [str(GTFS)])
    log(f"Rete R5 pronta in {time.time()-t0:.0f} s")
    return rete, gpd

def gdf_da_punti(gpd, punti, id_prefisso):
    import pandas as pd
    from shapely.geometry import Point
    df = pd.DataFrame({"id": [f"{id_prefisso}{i}" for i in range(len(punti))],
                       "lat": [p[0] for p in punti], "lon": [p[1] for p in punti]})
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")

def matrice(rete, moduli, orig_gdf, dest_gdf, quando, max_time, **kwargs):
    # r5py 1.x: TravelTimeMatrix e' un GeoDataFrame calcolato al costruttore
    from r5py import TravelTimeMatrix
    return TravelTimeMatrix(
        rete, origins=orig_gdf, destinations=dest_gdf,
        departure=quando, transport_modes=moduli, max_time=max_time, **kwargs)

def lotti(origins, n):
    """Origini raggruppate a lotti spazialmente compatti (griglia + ordine)."""
    ordinate = sorted(origins, key=lambda o: (round(o["lat"] / 0.02), round(o["lon"] / 0.02)))
    for i in range(0, len(ordinate), n):
        yield ordinate[i:i + n]

def conto_per_origine(mat, orig_ids, dest_by_k, margine_gradi, origine_da_pos, cutoff_min):
    """Dal DataFrame r5py (from_id,to_id,travel_time) ricava i conteggi per
    sezione e gruppo. dest_by_k: {k_originale: (lat,lon,gruppo)}."""
    per_gruppo = {oid: {g: 0 for g in GRUPPI} for oid in orig_ids}
    for r in mat.itertuples(index=False):
        oid = str(r.from_id)
        tempo = r.travel_time
        # r5py restituisce Timedelta o minuti secondo versione: normalizzo a minuti
        if hasattr(tempo, "total_seconds"):
            tempo = tempo.total_seconds() / 60.0
        if tempo is None or (isinstance(tempo, float) and tempo != tempo):
            continue
        if tempo > cutoff_min:
            continue
        la, lo, g = dest_by_k[int(str(r.to_id).removeprefix("D"))]
        la0, lo0 = origine_da_pos[oid]
        if abs(la - la0) <= margine_gradi[0] and abs(lo - lo0) <= margine_gradi[1]:
            per_gruppo[oid][g] += 1
    return per_gruppo

def aggrega_punti(punti, margine_metri=50):
    """Raggruppa i punti in celle di ~margine_metri metri e crea punti medi con peso."""
    # Converti metri a gradi (1 grado ~ 111 km)
    margine_gradi = margine_metri / 111000.0
    points = []
    for lat, lon in points:
        # Trova la cella più vicina
        cell_lat = round(lat / margine_gradi) * margine_gradi
        cell_lon = round(lon / margine_gradi) * margine_gradi
        points.append((cell_lat, cell_lon, lat, lon))  # (cella_lat, cella_lon, lat_originale, lon_originale)
    
    # Raggruppa per cella
    cell_dict = {}
    for cell_lat, cell_lon, lat, lon in points:
        key = (cell_lat, cell_lon)
        if key not in cell_dict:
            cell_dict[key] = []
        cell_dict[key].append((lat, lon))
    
    # Crea punti medi con peso (numero di punti originali)
    aggregated = []
    for (cell_lat, cell_lon), pts in cell_dict.items():
        agg_lat = sum(p[0] for p in pts) / len(pts)
        agg_lon = sum(p[1] for p in pts) / len(pts)
        peso = len(pts)
        aggregated.append((cell_lat, cell_lon, peso))
    
    return aggregated

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campione", type=int, default=0)
    ap.add_argument("--ore", default="8,14,23,2")
    ap.add_argument("--giorno", default="2026-10-12")
    ap.add_argument("--cutoff-piedi", type=int, default=15)
    ap.add_argument("--cutoff-tp", type=int, default=45)
    ap.add_argument("--lotto-piedi", type=int, default=100)
    ap.add_argument("--lotto-tp", type=int, default=20)  # Ridotto da 40 a 20
    ap.add_argument("--giro-prova", action="store_true")
    ap.add_argument("--salva-tappe", action="store_true")  # Salva a tappe
    ap.add_argument("--margine-metri", type=int, default=50)  # Margine per aggregazione
    ap.add_argument("--velocita-piedi", type=float, default=80)  # 4.8 km/h = 80 m/min
    ap.add_argument("--velocita-tp", type=float, default=4.8)  # 4.8 km/h per margine TP
    args = ap.parse_args()
    args.ore = [int(x) for x in args.ore.split(",")]
    args.velocita_piedi = args.velocita_piedi / 1000 * 60  # converti km/h a m/min
    args.velocita_tp = args.velocita_tp / 1000 * 60  # converti km/h a m/min

    sezioni = carica_sezioni()
    log(f"Sezioni con residenti: {len(sezioni)}")
    if args.campione > 0:
        passo = max(1, len(sezioni) // args.campione)
        sezioni = sezioni[::passo][:args.campione]
        log(f"Campione: {len(sezioni)} sezioni (una ogni {passo})")

    dest = carica_destinazioni()
    osm_servizi = carica_servizi_osm_cintura()
    dest["cibo"].extend(osm_servizi["cibo"])  # Aggiungi cibo OSM
    dest["salute"].extend(osm_servizi["salute"])  # Aggiungi salute OSM
    dest["scuole"].extend(osm_servizi["scuole"])  # Aggiungi scuole OSM

    dest_piatti = [(la, lo, g) for g in GRUPPI for (la, lo) in dest[g]]
    log(f"Destinazioni totali: {len(dest_piatti)}")

    rete, gpd = avvia_rete()
    if args.giro_prova:
        log("Giro di prova: rete costruita, fermo qui.")
        return

    orig_gdf_tutte = gdf_da_punti(gpd, [(s["lat"], s["lon"]) for s in sezioni], "S")
    orig_gdf_tutte["id"] = [s["id"] for s in sezioni]
    dest_gdf_tutte = gdf_da_punti(gpd, [(p[0], p[1]) for p in dest_piatti], "D")
    origine_da_pos = {str(s["id"]): (s["lat"], s["lon"]) for s in sezioni}

    # margine in linea d'aria (lat,lon) oltre il cutoff + 20% di respiro
    km_piedi = args.cutoff_piedi * args.velocita_piedi / 1000.0  # metri/min -> km
    margine_piedi = (km_piedi / 111.32 * 1.2, km_piedi / 111.32 / 0.7071 * 1.2)
    margine_tp = (args.velocita_tp / 111.32, args.velocita_tp / 111.32 / 0.7071)

    risultati = {s["id"]: {
        "id": s["id"],
        "lat": round(s["lat"], 5),
        "lon": round(s["lon"], 5),
        "res": s["res"],
        "piedi": {},
        "tp": {}
    } for s in sezioni}

    giorno = dt.date.fromisoformat(args.giorno)

    # ---- A PIEDI (indipendente dall'ora: R5 a piedi non usa gli orari) 
    log(f"A piedi: cutoff {args.cutoff_piedi} min, velocità {args.velocita_piedi:.0f} m/min...")
    t0 = time.time()
    for n, lotto in enumerate(lotti(sezioni, args.lotto_piedi), 1):
        ids = [s["id"] for s in lotto]
        orig = orig_gdf_tutte[orig_gdf_tutte["id"].isin(ids)]
        la0 = min(s["lat"] for s in lotto) - margine_piedi[0]
        la1 = max(s["lat"] for s in lotto) + margine_piedi[0]
        lo0 = min(s["lon"] for s in lotto) - margine_piedi[1]
        lo1 = max(s["lon"] for s in lotto) + margine_piedi[1]
        dentro = [(k, p) for k, p in enumerate(dest_piatti) if la0 <= p[0] <= la1 and lo0 <= p[1] <= lo1]
        dest_gdf = dest_gdf_tutte.iloc[[k for k, _ in dentro]]
        dest_by_k = {k: (p[0], p[1], p[2]) for k, p in dentro}
        quando = dt.datetime.combine(giorno, dt.time(7, 0))
        m = matrice(rete, [osmium.r5.TransportMode.WALK],
                    orig, dest_gdf, quando, dt.timedelta(minutes=args.cutoff_piedi))
        conteggi = conto_per_origine(m, ids, dest_by_k, margine_piedi, origine_da_pos, args.cutoff_piedi)
        for oid, cg in conteggi.items():
            risultati[oid]["piedi"][str(args.cutoff_piedi)] = cg
        log(f"  lotto a piedi {n}: {len(lotto)} sezioni, {len(dest_by_k)} dest ({time.time()-t0:.0f} s)")
        if args.salva_tappe and n % 10 == 0:
            # Salva a tappe
            partial = {
                "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "avviso": "Calcolo a piedi parziale",
                "parametri": {
                    "giorno": args.giorno,
                    "ore": args.ore,
                    "cutoff_piedi_min": args.cutoff_piedi,
                    "cutoff_tp_min": args.cutoff_tp,
                    "velocita_piedi": args.velocita_piedi,
                    "lotto_piedi": args.lotto_piedi,
                    "campione": len(sezioni)
                },
                "gruppi": {g: len(dest[g]) for g in GRUPPI},
                "sezioni": [risultati[s["id"]] for s in sezioni[:n*args.lotto_piedi]]
            }
            partial_path = OUT.parent / f"accessibilita_parziale/piedi_{n//args.lotto_piedi}.json"
            partial_path.parent.mkdir(parents=True, exist_ok=True)
            with open(partial_path, 'w') as f:
                json.dump(partial, f, ensure_ascii=False, separators=(",", ":"))
            log(f"  Salvataggio tappe: {partial_path}")

    # ---- COL TRASPORTO PUBBLICO, per ora
    from r5py import TransportMode as TM
    for ora in args.ore:
        log(f"TP ore {ora:02d}:00, cutoff {args.cutoff_tp} min, velocità {args.velocita_tp:.0f} m/min...")
        t0 = time.time()
        for n, lotto in enumerate(lotti(sezioni, args.lotto_tp), 1):
            ids = [s["id"] for s in lotto]
            orig = orig_gdf_tutte[orig_gdf_tutte["id"].isin(ids)]
            la0 = min(s["lat"] for s in lotto) - margine_tp[0]
            la1 = max(s["lat"] for s in lotto) + margine_tp[0]
            lo0 = min(s["lon"] for s in lotto) - margine_tp[1]
            lo1 = max(s["lon"] for s in lotto) + margine_tp[1]
            dentro = [(k, p) for k, p in enumerate(dest_piatti) if la0 <= p[0] <= la1 and lo0 <= p[1] <= lo1]
            dest_gdf = dest_gdf_tutte.iloc[[k for k, _ in dentro]]
            dest_by_k = {k: (p[0], p[1], p[2]) for k, p in dentro}
            quando = dt.datetime.combine(giorno, dt.time(ora, 0))
            m = matrice(rete, [TM.TRANSIT, TM.WALK], orig, dest_gdf, quando,
                        dt.timedelta(minutes=args.cutoff_tp))
            conteggi = conto_per_origine(m, ids, dest_by_k, margine_tp, origine_da_pos, args.cutoff_tp)
            for oid, cg in conteggi.items():
                risultati[oid]["tp"][f"{ora:02d}"] = cg
            log(f"  lotto {ora:02d} #{n}: {len(lotto)} sezioni, {len(dest_by_k)} dest ({time.time()-t0:.0f} s)")
            if args.salva_tappe and n % 10 == 0:
                # Salva a tappe
                partial = {
                    "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                    "avviso": "Calcolo TP parziale",
                    "parametri": {
                        "giorno": args.giorno,
                        "ore": args.ore,
                        "cutoff_piedi_min": args.cutoff_piedi,
                        "cutoff_tp_min": args.cutoff_tp,
                        "velocita_tp": args.velocita_tp,
                        "lotto_tp": args.lotto_tp,
                        "campione": len(sezioni)
                    },
                    "gruppi": {g: len(dest[g]) for g in GRUPPI},
                    "sezioni": [risultati[s["id"]] for s in sezioni[(n-1)*args.lotto_tp:(n)*args.lotto_tp]]
                }
                partial_path = OUT.parent / f"accessibilita_parziale/tp_{ora}_{n//args.lotto_tp}.json"
                partial_path.parent.mkdir(parents=True, exist_ok=True)
                with open(partial_path, 'w') as f:
                    json.dump(partial, f, ensure_ascii=False, separators=(",", ":"))
                log(f"  Salvataggio tappe: {partial_path}")

    esito = {
        "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "avviso": "ORARIO PROGRAMMATO [STIMATO], non misurato: niente ritardi, capienze o domanda. Motore R5/r5py su GTFS + OSM tagliato (17).",
        "parametri": {
            "giorno": args.giorno,
            "ore": args.ore,
            "cutoff_piedi_min": args.cutoff_piedi,
            "cutoff_tp_min": args.cutoff_tp,
            "velocita_piedi": args.velocita_piedi,
            "velocita_tp": args.velocita_tp,
            "lotto_piedi": args.lotto_piedi,
            "lotto_tp": args.lotto_tp,
            "campione": len(sezioni),
            "margine_metri": args.margine_metri
        },
        "gruppi": {g: len(dest[g]) for g in GRUPPI},
        "sezioni": [risultati[s["id"]] for s in sezioni],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(esito, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    log(f"Scritto {OUT} ({OUT.stat().st_size/1e6:.1f} MB)")

    # ---- rapporto
    def mediana(vals):
        v = sorted(vals)
        return v[len(v) // 2] if v else 0

    righe = [
        "RAPPORTO ACCESSIBILITA' (orario programmato, STIMATO - motore R5)",
        f"generato: {esito['generato']}  giorno tipo: {args.giorno}  ore: {args.ore}",
        f"sezioni: {len(sezioni)}  cutoff a piedi: {args.cutoff_piedi} min  TP: {args.cutoff_tp} min",
        f"destinazioni: {esito['gruppi']}",
        "",
        "Servizi essenziali raggiungibili a piedi (mediane per gruppo):",
        f"  {args.cutoff_piedi} min: {mediana([r['piedi'][str(args.cutoff_piedi)][g] for r in esito['sezioni']]):.0f}"
    ]
    for ora in args.ore:
        chi = f"{ora:02d}"
        righe.append(f"TP {chi}:00 (mediana servizi totali entro {args.cutoff_tp} min): "
                     f"{mediana([sum(r['tp'][chi].values()) for r in esito['sezioni']]):.0f}")
    zero_notte = sum(1 for r in esito['sezioni'] if sum(r["tp"]["23"].values()) == 0)
    tot_piedi = sum(sum(r["piedi"][str(args.cutoff_piedi)].values()) for r in esito['sezioni'])
    if tot_piedi == 0:
        righe.insert(1, "ATTENZIONE: conteggio a piedi tutto a zero - controllare margini/rete!")
    righe += ["", f"Sezioni senza NESSUN servizio entro {args.cutoff_tp} min alle 23:00: {zero_notte}"]
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe), encoding="utf-8")
    log(f"Scritto {RAPPORTO}")

    # Previene il PC in sospensione durante il calcolo
    if sys.platform == "win32":
        import ctypes
        # Disabilita la sospensione del PC durante il calcolo
        user32 = ctypes.windll.user32
        power_attach_console = user32.GetConsoleWindow()
        if power_attach_console:
            user32.SetConsoleMode(power_attach_console, 0x0001)  # ENABLE_PROCESSED_INPUT

if __name__ == "__main__":
    main()