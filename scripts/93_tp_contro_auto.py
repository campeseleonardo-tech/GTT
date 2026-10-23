# -*- coding: utf-8 -*-
"""
scripts/93_tp_contro_auto.py - Risultato 8, parte D (D1, D2, D3): dove il mezzo pubblico non conviene rispetto all'auto.

Sola lettura sui dati. Unita': le zone IMQ che hanno punti in data/processed/traffico_c/punti.json (script 41); le zone
rappresentate solo da una «porta» restano fuori. Per ogni zona si tengono fino a 5 punti, i piu' pesanti per
popolazione (pesi rinormalizzati). Il tempo fra due zone e' la media dei tempi fra i loro punti, pesata con i pesi dei punti.

D1 - tempi coi mezzi pubblici: r5py come lo script 18 (stesso GTFS, stessa rete OSM tagliata), giorno 2026-10-12,
     partenza dalle 7:45 con finestra di 30 minuti (fino alle 8:15), mediana dei tempi della finestra;
     TravelTimeMatrix, mezzi pubblici + cammino, tempo massimo 120 minuti. Una coppia di zone e' «senza
     collegamento» se meno della meta' del peso delle coppie di punti ha un collegamento entro 120 minuti.
D2 - tempi in auto: rete del modello del traffico (scripts/rete_osm.py), cammino minimo come nello script 42,
     tempo a flusso libero. Ora di punta = tempo x FATTORE (predefinito 1,5) + 5 minuti per parcheggiare e camminare.
     Sensibilita' con 1,3 e 1,8. Controllo: Piazza Castello -> Collegno nella fascia 20-35 minuti (Fase 5).
D3 - confronto: rapporto = tempo coi mezzi / tempo in auto (di punta). Auto della coppia = viaggi IMQ in auto come
     conducente (domanda_auto.json dello script 40), partenza dalle 6 alle 10 (ore 6-9), giorno feriale.
     Nessuna soglia di «convenienza»: titolo = rapporto mediano pesato per le auto; auto per fasce FISSE del
     rapporto (sotto 1,5, 1,5-2, 2-3, oltre 3). Tre gruppi di coppie: (a) Torino-Torino, (b) Torino-cintura,
     (c) cintura-cintura; il risultato principale usa (a)+(b): fuori Torino mancano treni e bus di altre aziende.
     Cammino a 4,8 km/h. Punti agganciati alla parte principale della rete stradale. I due calcoli precedenti
     (cammino a 3,6 km/h) restano nel JSON sotto «precedenti», segnati come superati.

Come si lancia
--------------
  python scripts\\93_tp_contro_auto.py --prova 10        (10 zone: scrive file con suffisso _prova)
  python scripts\\93_tp_contro_auto.py                   (tutte le zone; ripartibile: salva a tappe)
  Opzioni: --fattore 1.2 (limite alto; se manca, si calcola dai sensori 5T)   --lotto 20

Uscite: data/processed/tp_contro_auto.json, docs/rapporti/RAPPORTO_TP_CONTRO_AUTO.txt
"""
import argparse
import datetime as dt
import importlib.util
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comuni  # noqa: E402
import rete_osm  # noqa: E402

RADICE = comuni.RADICE
PROC = RADICE / "data" / "processed"
TRAFFICO = PROC / "traffico_c"
OUT_JSON = PROC / "tp_contro_auto.json"
RAPPORTO = RADICE / "docs" / "rapporti" / "RAPPORTO_TP_CONTRO_AUTO.txt"
PARZIALE = PROC / "tp_contro_auto_parziale.npz"

GIORNO = dt.date(2026, 10, 12)
PARTENZA = dt.time(7, 45)
FINESTRA_MIN = 30
TEMPO_MAX_MIN = 120
PUNTI_PER_ZONA = 5
ORE_MATTINO = range(6, 10)          # partenza 06:00-09:59
VELOCITA_5T = PROC / "velocita_5t.json"
ORE_NOTTE = (2, 3, 4)               # strade libere: dalle 2 alle 5
ORA_PUNTA = 8
MIN_PARCHEGGIO = 5.0
FASCE = (1.5, 2.0, 3.0)             # fasce fisse del rapporto TP/auto, scelte dopo le prime prove (il metodo e' cambiato 4 volte il 21/10)
VEL_PIEDI_KMH = 4.8                 # 80 m al minuto, come lo script 18 e tutto il progetto (r5py di serie: 3,6)
QUOTA_MIN_COLLEGATA = 0.5           # meta' del peso delle coppie di punti con collegamento

# percorsi noti (lat, lon), gli stessi dello script 50b; il primo e' il controllo della Fase 5
CASTELLO = (45.0703, 7.6869)
# tempi in auto controllati a mano su Google Maps, martedi' 20/10 alle 8:00, partendo da Piazza Castello (minuti).
# I 2 percorsi di CONTROLLO_GOOGLE non entrano mai nel fattore.
# Google Maps, 6 percorsi controllati a mano: usato solo per il limite basso della forbice (fattore = mediana di (tempo Google - 5) / flusso libero)
GOOGLE_AUTO_MIN = {"Piazza Castello → Collegno": 19, "Piazza Castello → Venaria Reale": 31,
                   "Piazza Castello → Settimo Torinese": 38, "Piazza Castello → Moncalieri": 34,
                   "Piazza Castello → Orbassano": 44, "Piazza Castello → Rivoli": 38}
# due percorsi in piu', solo per il controllo (Google, 21/10): mezzi pubblici (min, max) e auto
CONTROLLI_GOOGLE = {"Corso Racconigi → Piazza Castello": {"auto": 29, "mezzi": (30, 35), "mezzi_nota": "mezzi pubblici"},
                    "Moncalieri → Lingotto": {"auto": 14, "mezzi": (30, 35), "mezzi_nota": "solo GTT; col treno 19-23"}}
SOGLIA_AVVISO_GOOGLE = 0.25
NOTI = [("Piazza Castello → Collegno", CASTELLO, (45.0721, 7.5717)),
        ("Piazza Castello → Venaria Reale", CASTELLO, (45.1352, 7.6330)),
        ("Piazza Castello → Settimo Torinese", CASTELLO, (45.1395, 7.7703)),
        ("Piazza Castello → Moncalieri", CASTELLO, (45.0005, 7.6810)),
        ("Piazza Castello → Orbassano", CASTELLO, (45.0070, 7.5373)),
        ("Piazza Castello → Rivoli", CASTELLO, (45.0709, 7.5167)),
        ("Corso Racconigi → Piazza Castello", (45.0650, 7.6440), CASTELLO),
        ("Moncalieri → Lingotto", (45.0005, 7.6810), (45.0270, 7.6600))]
N_NOTI_TARATURA = 6                 # i primi 6; gli altri sono solo controllo


def fattore_da_sensori():
    """Fattore di punta = mediana, sui sensori 5T con dati affidabili, di velocita' media fra le 2 e le 5 / velocita' alle 8
    (giorno feriale). Un sensore senza dati affidabili di notte o alle 8 resta fuori. Arrotondato a 0,1."""
    d = json.loads(VELOCITA_5T.read_text(encoding="utf-8"))
    valori = []
    for v in d["sensori"].values():
        celle = v["celle"].get("0")
        if not celle:
            continue
        notte = [celle[str(h)]["v"] for h in ORE_NOTTE if str(h) in celle and celle[str(h)]["ok"] and celle[str(h)]["v"]]
        punta8 = celle.get(str(ORA_PUNTA))
        if not notte or not punta8 or not punta8["ok"] or not punta8["v"]:
            continue
        valori.append(float(np.mean(notte)) / punta8["v"])
    x = np.array(valori)
    q = np.percentile(x, [0, 25, 50, 75, 100])
    stat = {"sensori_totali": len(d["sensori"]), "sensori_usati": len(x), "minimo": q[0], "q1": q[1], "mediana": q[2], "q3": q[3],
            "massimo": q[4], "periodo": d["periodo"], "giorni_feriali": d["giorni"]["0"]}
    return round(float(q[2]), 1), stat


def nome_zona(n):
    """'01 Torino- Mirafiori Nord' -> 'Torino, Mirafiori Nord'; 'RIVALTA DI TORINO' -> 'Rivalta di Torino'."""
    if n.startswith("01 Torino"):
        n = "Torino, " + n[len("01 Torino"):].strip(" -")
    return n.title().replace(" Di ", " di ").replace(", ", ", ")


def carica_zone(prova):
    punti = json.loads((TRAFFICO / "punti.json").read_text(encoding="utf-8"))["zone"]
    nomi = {z["cod"]: z["denom"] for z in json.loads((PROC / "imq_zone.json").read_text(encoding="utf-8"))}
    zone = {}
    for cod, elenco in punti.items():
        veri = [p for p in elenco if p["tipo"] != "porta"]
        if not veri:                                  # zona rappresentata solo da porte: fuori
            continue
        top = sorted(veri, key=lambda p: -p["peso"])[:PUNTI_PER_ZONA]
        tot = sum(p["peso"] for p in top)
        zone[cod] = {"nome": nome_zona(nomi.get(cod, cod)), "punti": [
            {"lat": p["lat"], "lon": p["lon"], "nodo": int(p["nodo"]), "peso": p["peso"] / tot} for p in top]}
    return zone


def carica_auto(zone):
    """auto della coppia (zona A, zona B) = viaggi IMQ in auto come conducente, ore 6-9, giorno feriale."""
    d = json.loads((TRAFFICO / "domanda_auto.json").read_text(encoding="utf-8"))
    coppie = defaultdict(float)
    for par, arr, ora, peso, _n in d["celle"]:
        if ora in ORE_MATTINO and par in zone and arr in zone:
            coppie[(par, arr)] += peso
    return coppie


def matrice_auto(zone, extra):
    """Tempi in auto (secondi, flusso libero) fra tutti i nodi dei punti e dei punti extra. Dict (nodo_a, nodo_b) -> s."""
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import dijkstra
    rete = rete_osm.carica(TRAFFICO / "rete")
    xy, archi = rete["nodi_xy"], rete["archi"]
    N = len(xy)
    src, dst, w = archi[:, 0].astype(np.int64), archi[:, 1].astype(np.int64), archi[:, 2].astype(np.float64)
    chiave = src * N + dst
    ordine = np.lexsort((w, chiave))                  # fra i duplicati il piu' veloce viene per primo
    chiave_s = chiave[ordine]
    primo = np.concatenate(([True], chiave_s[1:] != chiave_s[:-1]))
    sel = ordine[primo]
    tieni = src[sel] != dst[sel]
    M = csr_matrix((w[sel][tieni], (src[sel][tieni], dst[sel][tieni])), shape=(N, N))

    # parte principale della rete = la piu' grande componente fortemente connessa; i punti fuori da essa si agganciano al nodo piu' vicino dentro
    from scipy.sparse.csgraph import connected_components
    _, etichette = connected_components(M, directed=True, connection="strong")
    principale = np.argmax(np.bincount(etichette))
    nodi_princ = np.nonzero(etichette == principale)[0]
    xy_princ = xy[nodi_princ]
    spostati = {"n": 0, "su": 0, "max_m": 0.0}

    def nodo_vicino(lat, lon):
        d2 = (xy_princ[:, 0] - lat) ** 2 + (xy_princ[:, 1] - lon) ** 2
        return int(nodi_princ[int(np.argmin(d2))])

    def aggancia(nodo, lat, lon):
        spostati["su"] += 1
        if etichette[nodo] == principale:
            return nodo
        nuovo = nodo_vicino(lat, lon)
        spostati["n"] += 1
        spostati["max_m"] = max(spostati["max_m"], float(rete_osm.haversine_m(lat, lon, *xy[nuovo])))
        return nuovo

    for z in zone.values():
        for p in z["punti"]:
            p["nodo"] = aggancia(p["nodo"], p["lat"], p["lon"])
    nodi_extra = [(aggancia(int(np.argmin((xy[:, 0] - a[0]) ** 2 + (xy[:, 1] - a[1]) ** 2)), a[0], a[1]),
                   aggancia(int(np.argmin((xy[:, 0] - b[0]) ** 2 + (xy[:, 1] - b[1]) ** 2)), b[0], b[1])) for _, a, b in extra]
    nodi = sorted({p["nodo"] for z in zone.values() for p in z["punti"]} | {n for c in nodi_extra for n in c})
    t = {}
    for i in range(0, len(nodi), 25):
        gruppo = nodi[i:i + 25]
        dist = dijkstra(M, indices=gruppo)[:, nodi]
        for k, a in enumerate(gruppo):
            for j, b in enumerate(nodi):
                t[(a, b)] = float(dist[k, j])
    return t, nodi_extra, spostati


def tempo_zone_auto(za, zb, t):
    """media pesata dei tempi (secondi) fra i punti delle due zone."""
    tot = 0.0
    for p in za["punti"]:
        for q in zb["punti"]:
            tot += p["peso"] * q["peso"] * t[(p["nodo"], q["nodo"])]
    return tot


def avvia_r5py():
    spec = importlib.util.spec_from_file_location("acc18", AQUI / "18_accessibilita.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    rete, gpd = m.avvia_rete()
    return m, rete, gpd


def matrice_tp(zone, extra, lotto, log):
    """Tempi TP (minuti, mediana nella finestra 7:45-8:15) fra tutti i punti. Ripartibile.
    Ritorna (ids, T) con T[i, j] in minuti, nan = nessun collegamento entro 120 minuti."""
    import pandas as pd
    elenco = []                                       # (id, lat, lon)
    for cod, z in zone.items():
        for k, p in enumerate(z["punti"]):
            elenco.append((f"{cod}_{k}", p["lat"], p["lon"]))
    for k, (_, a, b) in enumerate(extra):
        elenco.append((f"NOTO{k}_A", a[0], a[1]))
        elenco.append((f"NOTO{k}_B", b[0], b[1]))
    ids = [e[0] for e in elenco]
    firma = f"{len(ids)}-{round(sum(e[1] + e[2] for e in elenco), 5)}-{GIORNO}-{PARTENZA}-{FINESTRA_MIN}-{TEMPO_MAX_MIN}-piedi{VEL_PIEDI_KMH}"
    n = len(ids)
    T = np.full((n, n), np.nan)
    fatti = np.zeros(n, dtype=bool)
    if PARZIALE.is_file():
        z = np.load(PARZIALE, allow_pickle=True)
        if str(z["firma"]) == firma:
            T, fatti = z["T"], z["fatti"]
            log(f"ripresa: {int(fatti.sum())} origini su {n} gia' calcolate")
        else:
            log("file parziale di un altro calcolo: lo ignoro")
    m18, rete, gpd = avvia_r5py()
    from r5py import TransportMode as TM
    from r5py import TravelTimeMatrix
    df = pd.DataFrame({"id": ids, "lat": [e[1] for e in elenco], "lon": [e[2] for e in elenco]})
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")
    quando = dt.datetime.combine(GIORNO, PARTENZA)
    posizione = {i: k for k, i in enumerate(ids)}
    da_fare = [k for k in range(n) if not fatti[k]]
    t0 = time.time()
    for i in range(0, len(da_fare), lotto):
        blocco = da_fare[i:i + lotto]
        orig = gdf.iloc[blocco]
        mat = TravelTimeMatrix(rete, origins=orig, destinations=gdf, departure=quando,
                               departure_time_window=dt.timedelta(minutes=FINESTRA_MIN),
                               transport_modes=[TM.TRANSIT, TM.WALK], speed_walking=VEL_PIEDI_KMH,
                               max_time=dt.timedelta(minutes=TEMPO_MAX_MIN))
        mat = pd.DataFrame(mat)
        col = "travel_time" if "travel_time" in mat.columns else "travel_time_p50"
        v = mat[col]
        if str(v.dtype).startswith("timedelta"):
            v = v.dt.total_seconds() / 60.0
        for a, b, x in zip(mat["from_id"], mat["to_id"], v):
            T[posizione[a], posizione[b]] = float(x) if x == x else np.nan
        fatti[blocco] = True
        np.savez_compressed(PARZIALE, T=T, fatti=fatti, firma=firma)
        log(f"  TP: {int(fatti.sum())}/{n} origini ({time.time() - t0:.0f} s)")
    return ids, T


def tempo_zone_tp(za, ca, zb, cb, ids_pos, T):
    """media pesata dei tempi TP (minuti) sulle coppie di punti raggiungibili; (tempo, quota di peso collegata)."""
    somma = peso = tot = 0.0
    for k, p in enumerate(za["punti"]):
        for h, q in enumerate(zb["punti"]):
            w = p["peso"] * q["peso"]
            tot += w
            x = T[ids_pos[f"{ca}_{k}"], ids_pos[f"{cb}_{h}"]]
            if x == x:
                somma += w * x
                peso += w
    return (somma / peso if peso else None), (peso / tot if tot else 0.0)


def mediana_pesata(coppie, f):
    """mediana del rapporto TP/auto pesata per le auto (fattore di punta f)."""
    v = sorted((p["tp_min"] / punta(p["libero_min"], f), p["auto"]) for p in coppie)
    tot = sum(w for _, w in v)
    if not v or tot <= 0:
        return None
    acc = 0.0
    for r, w in v:
        acc += w
        if acc >= tot / 2:
            return r
    return v[-1][0]


def punta(libero, f):
    return libero * f + MIN_PARCHEGGIO


def fasce(coppie, f):
    """auto e coppie per fascia FISSA di rapporto (scelte dopo le prime prove)."""
    tot = sum(p["auto"] for p in coppie)
    estremi = [0.0, *FASCE, float("inf")]
    out = []
    for lo, hi in zip(estremi[:-1], estremi[1:]):
        sel = [p for p in coppie if lo <= p["tp_min"] / punta(p["libero_min"], f) < hi]
        a = sum(p["auto"] for p in sel)
        out.append({"da": lo, "a": (None if hi == float("inf") else hi), "auto": round(a), "coppie": len(sel),
                    "pct": (100 * a / tot if tot else 0.0)})
    return out


def quota_oltre(coppie, f, soglia):
    tot = sum(p["auto"] for p in coppie)
    return sum(p["auto"] for p in coppie if p["tp_min"] / punta(p["libero_min"], f) >= soglia) / tot if tot else 0.0


def riepilogo(coppie, f):
    return {"fattore": f, "auto": round(sum(p["auto"] for p in coppie)), "coppie": len(coppie),
            "mediano": mediana_pesata(coppie, f), "fasce": fasce(coppie, f), "quota_oltre_2": quota_oltre(coppie, f, 2.0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", type=int, default=0, help="usa solo le N zone con piu' auto in uscita")
    ap.add_argument("--fattore", type=float, default=None, help="fattore di punta (se manca: dai sensori 5T)")
    ap.add_argument("--lotto", type=int, default=20, help="origini per chiamata r5py (e per salvataggio)")
    args = ap.parse_args()
    t_inizio = time.time()
    c = comuni.Controlli()
    fattore_sensori, stat_sensori = fattore_da_sensori()
    if args.fattore is None:
        args.fattore = fattore_sensori

    def log(m):
        print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

    zone = carica_zone(args.prova)
    auto = carica_auto(zone)
    totale_zone = sum(auto.values())
    if args.prova:
        uscita = defaultdict(float)
        for (a, b), v in auto.items():
            if a != b:
                uscita[a] += v
        tieni = set(sorted(uscita, key=lambda z: -uscita[z])[:args.prova])
        zone = {k: v for k, v in zone.items() if k in tieni}
        auto = carica_auto(zone)
        totale_zone = sum(auto.values())
    torino = {k for k, z in zone.items() if z["nome"].startswith("Torino,")}   # regola controllata sul file vero: coincide con i codici Q e con la macro «01 Torino»
    log(f"zone: {len(zone)} con punti ({len(torino)} di Torino); auto del mattino fra le zone incluse: {totale_zone:,.0f}")

    log("D2: tempi in auto sulla rete del modello del traffico ...")
    t_auto, nodi_extra, spostati = matrice_auto(zone, NOTI)
    log(f"  punti agganciati alla parte principale della rete: {spostati['n']} su {spostati['su']} spostati (distanza massima {spostati['max_m']:.0f} m)")
    # fattore del limite basso: Google Maps, 6 percorsi controllati a mano; usato solo per il limite basso della forbice
    liberi = [t_auto[(nodi_extra[k][0], nodi_extra[k][1])] / 60.0 for k in range(len(NOTI))]
    fattori_google = {nome: (GOOGLE_AUTO_MIN[nome] - MIN_PARCHEGGIO) / liberi[k] for k, (nome, _, _) in enumerate(NOTI) if nome in GOOGLE_AUTO_MIN}
    f_google = round(float(np.median(list(fattori_google.values()))), 1)
    # L6bis (24/10/2026): se c'e' il fattore del servizio di percorsi (script 101: tempo TomTom col traffico / nostro flusso libero, mediana delle coppie
    # alle 8), la seconda stima usa quello; il 2,1 di Google resta come controllo. La chiave JSON resta «fattore_basso_google» (nome storico).
    f_servizio = comuni.fattore_servizio("coppie", "08:00") if not args.prova else None
    f_basso = round(float(f_servizio), 2) if f_servizio else f_google
    fonte_basso = ("TomTom (script 101), mediana di fattore_rete delle coppie alle 8" if f_servizio else "Google Maps, 6 percorsi")
    log(f"  fattore alto (sensori 5T) {args.fattore:g}; seconda stima ({fonte_basso}) {f_basso:g}; Google a mano {f_google:g}")
    log("D1: tempi coi mezzi pubblici (r5py, cammino a 4,8 km/h) ...")
    ids, T = matrice_tp(zone, NOTI, args.lotto, log)
    pos = {i: k for k, i in enumerate(ids)}

    # ---- tempi per coppia di zone, in tre gruppi: (a) Torino-Torino, (b) Torino-cintura e cintura-Torino, (c) cintura-cintura
    def gruppo(a, b):
        n = (a in torino) + (b in torino)
        return "a" if n == 2 else ("b" if n == 1 else "c")

    cod = sorted(zone)
    coppie, senza_link = [], []
    intra = 0.0
    infiniti = 0
    for a in cod:
        for b in cod:
            v = auto.get((a, b), 0.0)
            if a == b:
                intra += v
                continue
            secondi = tempo_zone_auto(zone[a], zone[b], t_auto)
            if not np.isfinite(secondi):
                infiniti += 1
                continue
            ta = secondi / 60.0
            tp, quota = tempo_zone_tp(zone[a], a, zone[b], b, pos, T)
            g = gruppo(a, b)
            if tp is None or quota < QUOTA_MIN_COLLEGATA:
                senza_link.append({"da": a, "a": b, "gruppo": g, "auto": v, "auto_libero_min": round(ta, 1), "quota_collegata": round(quota, 2)})
                continue
            coppie.append({"da": a, "a": b, "gruppo": g, "auto": v, "tp_min": tp, "libero_min": ta, "quota_collegata": quota})
    f_alto = args.fattore                      # sensori 5T: auto piu' veloce, rapporto TP/auto piu' alto
    for p in coppie:
        p["auto_punta_min"] = punta(p["libero_min"], f_alto)
        p["rapporto"] = p["tp_min"] / p["auto_punta_min"]
        p["auto_punta_basso_min"] = punta(p["libero_min"], f_basso)
        p["rapporto_basso"] = p["tp_min"] / p["auto_punta_basso_min"]

    ab = [p for p in coppie if p["gruppo"] in ("a", "b")]
    gruppi = {}
    nomi_gruppi = {"a": "Torino-Torino", "b": "Torino-cintura (e cintura-Torino)", "c": "cintura-cintura",
                   "ab": "principale: Torino-Torino e Torino-cintura"}
    for g, elenco in (("a", [p for p in coppie if p["gruppo"] == "a"]), ("b", [p for p in coppie if p["gruppo"] == "b"]),
                      ("c", [p for p in coppie if p["gruppo"] == "c"]), ("ab", ab)):
        ss = [s for s in senza_link if (s["gruppo"] in g)]
        gruppi[g] = {"nome": nomi_gruppi[g], "auto": round(sum(p["auto"] for p in elenco)), "coppie": len(elenco),
                     "senza_collegamento": {"coppie": len(ss), "auto": round(sum(s["auto"] for s in ss))},
                     "limite_alto": riepilogo(elenco, f_alto), "limite_basso": riepilogo(elenco, f_basso)}
        if g == "c":
            gruppi[g]["nota"] = "dati del mezzo pubblico incompleti: mancano treni e bus di altre aziende"
    base = gruppi["ab"]
    # le coppie peggiori si scelgono col fattore basso (auto piu' lenta): quelle con rapporto oltre 2, in ordine di auto
    peggiori = sorted((p for p in ab if p["rapporto_basso"] >= 2.0), key=lambda p: -p["auto"])[:15]
    per_zona = []
    for a in cod:
        mie = [p for p in ab if p["da"] == a]
        tot = sum(p["auto"] for p in mie)
        oltre_alto = sum(p["auto"] for p in mie if p["rapporto"] >= 2.0)
        oltre_basso = sum(p["auto"] for p in mie if p["rapporto_basso"] >= 2.0)
        per_zona.append({"zona": a, "nome": zone[a]["nome"], "auto_uscita": round(tot),
                         "quota_oltre_2_alto": (oltre_alto / tot if tot else None), "quota_oltre_2_basso": (oltre_basso / tot if tot else None)})
    per_zona.sort(key=lambda z: -(z["quota_oltre_2_basso"] or 0))

    # ---- controllo di buon senso: percorsi noti
    noti = []
    for k, (nome, a, b) in enumerate(NOTI):
        libero = liberi[k]
        tp = T[pos[f"NOTO{k}_A"], pos[f"NOTO{k}_B"]]
        noti.append({"nome": nome, "auto_libero_min": libero, "auto_punta_min": punta(libero, f_alto),
                     "auto_punta_basso_min": punta(libero, f_basso),
                     "tp_min": (float(tp) if tp == tp else None), "controllo": k >= N_NOTI_TARATURA,
                     "google_auto_min": (GOOGLE_AUTO_MIN.get(nome) or CONTROLLI_GOOGLE.get(nome, {}).get("auto")),
                     "google_mezzi_min": (list(CONTROLLI_GOOGLE[nome]["mezzi"]) if nome in CONTROLLI_GOOGLE else None),
                     "google_mezzi_nota": (CONTROLLI_GOOGLE[nome]["mezzi_nota"] if nome in CONTROLLI_GOOGLE else None)})

    # ---- controlli
    c("nessun tempo negativo o nullo fra zone diverse",
      all(p["tp_min"] > 0 and p["libero_min"] > 0 for p in coppie), bloccante=True)
    c("nessun tempo infinito in auto fra zone", infiniti == 0 and all(np.isfinite(n["auto_libero_min"]) for n in noti),
      dettaglio=f"{infiniti} coppie di zone, {sum(1 for n in noti if not np.isfinite(n['auto_libero_min']))} percorsi noti; punti spostati: {spostati['n']} su {spostati['su']}",
      bloccante=True)
    auto_senza = sum(s["auto"] for s in senza_link)
    c("coppie senza collegamento coi mezzi entro 120 minuti (contate a parte, per gruppo)", True,
      dettaglio="; ".join(f"{g}: {gruppi[g]['senza_collegamento']['coppie']} coppie, {gruppi[g]['senza_collegamento']['auto']:,} auto" for g in "abc"))
    auto_coll = sum(p["auto"] for p in coppie)
    somma = auto_coll + auto_senza + intra
    c("somma delle auto = totale IMQ 06-10 delle zone incluse", abs(somma - totale_zone) < 1e-6 * max(totale_zone, 1),
      dettaglio=f"{somma:,.0f} / {totale_zone:,.0f} (collegate {auto_coll:,.0f}, senza collegamento {auto_senza:,.0f}, dentro la zona {intra:,.0f})",
      bloccante=True)
    cast = noti[0]
    c("Piazza Castello → Collegno in auto di punta nella fascia 20-35 minuti, con tutti e due i fattori",
      20 <= cast["auto_punta_min"] <= 35 and 20 <= cast["auto_punta_basso_min"] <= 35,
      dettaglio=f"{cast['auto_libero_min']:.1f} minuti a flusso libero; di punta {cast['auto_punta_min']:.1f} (fattore {f_alto:g}) e {cast['auto_punta_basso_min']:.1f} (fattore {f_basso:g})")

    # ---- confronto con Google Maps: i 6 percorsi servono al fattore del limite basso della forbice; i 2 di controllo no
    con_google = [n for n in noti if n["google_auto_min"] and n["nome"] in GOOGLE_AUTO_MIN]
    diff = [n["auto_punta_min"] - n["google_auto_min"] for n in con_google]
    diff_media = float(np.mean(diff))
    diff_basso = float(np.mean([n["auto_punta_basso_min"] - n["google_auto_min"] for n in con_google]))
    sotto = [n["nome"] for n in con_google if (n["google_auto_min"] - n["auto_punta_min"]) / n["google_auto_min"] > SOGLIA_AVVISO_GOOGLE]
    sotto_basso = [n["nome"] for n in con_google if (n["google_auto_min"] - n["auto_punta_basso_min"]) / n["google_auto_min"] > SOGLIA_AVVISO_GOOGLE]
    c(f"fattore alto (sensori): tempo di punta non sotto Google di oltre il {int(SOGLIA_AVVISO_GOOGLE * 100)}% in piu' di meta' dei percorsi",
      len(sotto) <= len(con_google) / 2,
      dettaglio=f"differenza media {diff_media:+.1f} minuti (nostro meno Google); percorsi molto sotto: {len(sotto)} su {len(con_google)} (atteso: e' la stima piu' favorevole all'auto)")
    c(f"fattore basso (Google): tempo di punta non sotto Google di oltre il {int(SOGLIA_AVVISO_GOOGLE * 100)}% in piu' di meta' dei percorsi",
      len(sotto_basso) <= len(con_google) / 2,
      dettaglio=f"differenza media {diff_basso:+.1f} minuti; percorsi molto sotto: {len(sotto_basso)} su {len(con_google)}")

    nomi = {k: v["nome"] for k, v in zone.items()}
    titolo = {"mediano_alto": base["limite_alto"]["mediano"], "mediano_basso": base["limite_basso"]["mediano"],
              "quota_oltre_2_alto": base["limite_alto"]["quota_oltre_2"], "quota_oltre_2_basso": base["limite_basso"]["quota_oltre_2"],
              "auto_collegate": base["auto"]}
    prova = bool(args.prova)
    suff = "_prova" if prova else ""
    precedenti = None
    if OUT_JSON.is_file() and not prova:
        vecchio = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        if "gruppi" not in vecchio:                    # primo calcolo (cammino a 3,6 km/h): si conserva una volta sola
            precedenti = {"nota": "calcolati con cammino a 3,6 km/h: superati",
                          "soglie_1_5_e_2": vecchio["precedenti"], "soglie_2_5_e_3_5": {"soglie": vecchio["parametri"]["soglie"], "base": vecchio["base"], "sensibilita": vecchio["sensibilita"]},
                          "noti": vecchio["noti"]}
        elif "fattori_sensibilita" not in vecchio["parametri"] and "fattore_basso_google" not in vecchio["parametri"]:
            precedenti = {**(vecchio.get("precedenti") or {}),
                          "fattore_1_5_fisso": {"nota": "fattore di punta 1,5 scelto a mano, prima della taratura sui sensori 5T",
                                                "gruppo_ab": vecchio["gruppi"]["ab"], "noti": vecchio["noti"]}}
        elif "fattore_basso_google" not in vecchio["parametri"]:   # versione con il solo fattore dei sensori e sensibilita' +-0,3
            precedenti = {**(vecchio.get("precedenti") or {}),
                          "fattore_sensori_con_sensibilita": {"nota": "solo fattore dei sensori 5T con sensibilita' +-0,3: sostituita dalla forbice",
                                                              "gruppo_ab": vecchio["gruppi"]["ab"], "noti": vecchio["noti"]}}
        else:
            precedenti = vecchio.get("precedenti")
    out = {
        "stimato": True,
        "parametri": {"giorno": str(GIORNO), "partenza": f"{PARTENZA:%H:%M}", "finestra_min": FINESTRA_MIN,
                      "tempo_max_min": TEMPO_MAX_MIN, "velocita_piedi_kmh": VEL_PIEDI_KMH, "punti_per_zona": PUNTI_PER_ZONA,
                      "ore_auto": list(ORE_MATTINO), "fattore_punta": f_alto, "fattore_basso_google": f_basso, "fattore_google_manuale": f_google,
                      "forbice": {"limite_alto": {"fattore": f_alto, "fonte": "sensori 5T"}, "limite_basso": {"fattore": f_basso, "fonte": fonte_basso}},
                      "fattore_sensori": stat_sensori, "fattori_google_per_percorso": fattori_google,
                      "minuti_parcheggio": MIN_PARCHEGGIO,
                      "fasce": list(FASCE), "n_zone": len(zone), "n_zone_torino": len(torino), "punti_spostati": spostati, "prova": prova},
        "titolo": titolo, "gruppi": gruppi,
        "peggiori": [{"da": p["da"], "a": p["a"], "da_nome": nomi[p["da"]], "a_nome": nomi[p["a"]], "gruppo": p["gruppo"], "auto": round(p["auto"]),
                      "tp_min": round(p["tp_min"], 1), "auto_punta_min": round(p["auto_punta_min"], 1),
                      "auto_punta_basso_min": round(p["auto_punta_basso_min"], 1),
                      "rapporto": round(p["rapporto"], 2), "rapporto_basso": round(p["rapporto_basso"], 2)} for p in peggiori],
        "per_zona": per_zona,
        "coppie": [{"da": p["da"], "a": p["a"], "gruppo": p["gruppo"], "auto": round(p["auto"], 1), "tp_min": round(p["tp_min"], 1),
                    "libero_min": round(p["libero_min"], 2),
                    "auto_punta_min": round(p["auto_punta_min"], 1), "rapporto": round(p["rapporto"], 2),
                    "auto_punta_basso_min": round(p["auto_punta_basso_min"], 1), "rapporto_basso": round(p["rapporto_basso"], 2)}
                   for p in sorted(coppie, key=lambda p: -p["auto"])],
        "senza_collegamento": [{**s, "auto": round(s["auto"], 1)} for s in senza_link], "dentro_zona_auto": round(intra),
        "noti": noti, "google": {"data": "martedì 20/10/2026 ore 8:00", "differenza_media_min": diff_media, "differenza_media_basso_min": diff_basso,
                                 "percorsi_molto_sotto": sotto, "percorsi_molto_sotto_basso": sotto_basso},
        "totale_auto_zone": round(totale_zone),
        "controlli": list(c.righe),
    }
    if precedenti:
        out["precedenti"] = precedenti
    dest_json = OUT_JSON.with_name(OUT_JSON.stem + suff + ".json")
    dest_json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    def riga_fasce(rr):
        return "; ".join(f"{('sotto ' + format(f['a'], 'g')) if f['da'] == 0 else (('oltre ' + format(f['da'], 'g')) if f['a'] is None else format(f['da'], 'g') + '-' + format(f['a'], 'g'))}: "
                         f"{f['auto']:,} auto ({f['pct']:.1f}%)" for f in rr["fasce"])

    r = [f"RAPPORTO TP CONTRO AUTO (Risultato 8, parte D, STIMATO){' - PROVA' if prova else ''}",
         f"generato: {dt.datetime.now().isoformat(timespec='seconds')}", "",
         f"Zone IMQ con punti: {len(zone)} (zone solo «porta» escluse; {len(torino)} di Torino); fino a {PUNTI_PER_ZONA} punti per zona, i piu' pesanti.",
         f"Tempi coi mezzi: r5py, giorno {GIORNO}, mediana delle partenze 7:45-8:15, mezzi pubblici + cammino a {VEL_PIEDI_KMH:g} km/h, massimo {TEMPO_MAX_MIN} minuti.",
         f"Tempi in auto: rete del modello del traffico, flusso libero x fattore di punta + {MIN_PARCHEGGIO:.0f} minuti (parcheggio e cammino). Il risultato e' dato con DUE STIME, non un minimo e un massimo:",
         f"  stima con il rallentamento dei sensori = fattore dei sensori 5T, {f_alto:g} (solo traffico, senza semafori e incroci: la piu' favorevole all'auto): mediana di (velocita' media 2-5 / velocita' alle 8, feriale) su {stat_sensori['sensori_usati']} sensori "
         f"con dati affidabili (su {stat_sensori['sensori_totali']}; periodo {stat_sensori['periodo']['da']} - {stat_sensori['periodo']['a']}, {stat_sensori['giorni_feriali']} giorni feriali);",
         f"    distribuzione fra sensori: minimo {stat_sensori['minimo']:.2f}, 1° quartile {stat_sensori['q1']:.2f}, mediana {stat_sensori['mediana']:.2f}, "
         f"3° quartile {stat_sensori['q3']:.2f}, massimo {stat_sensori['massimo']:.2f}.",
         f"  seconda stima = {fonte_basso}, fattore {f_basso:g}: " + ("tempo col traffico del servizio / nostro flusso libero (stessa grandezza del 2,1 di Google). " if f_servizio else "")
         + f"Google Maps a mano: mediana di (tempo Google - 5) / tempo a flusso libero sui 6 percorsi ({', '.join(format(x, '.2f') for x in fattori_google.values())}) = {f_google:g}.",
         f"Punti agganciati alla parte principale della rete: {spostati['n']} su {spostati['su']} spostati (distanza massima {spostati['max_m']:.0f} m).",
         f"Auto: viaggi IMQ in auto conducente, partenza 6-10, feriale. Totale fra le zone incluse: {totale_zone:,.0f}.",
         "Gruppi: (a) Torino-Torino, (b) Torino-cintura e cintura-Torino, (c) cintura-cintura. Il risultato principale usa (a)+(b).",
         f"Fasce fisse del rapporto (tempo coi mezzi / tempo in auto), scelte dopo le prime prove (il metodo e' cambiato 4 volte il 21/10): sotto {FASCE[0]:g}, {FASCE[0]:g}-{FASCE[1]:g}, {FASCE[1]:g}-{FASCE[2]:g}, oltre {FASCE[2]:g}.",
         "", "TITOLO (gruppi a+b): DUE STIME",
         f"  al mattino, coi mezzi pubblici si impiega da {titolo['mediano_basso']:.2f} a {titolo['mediano_alto']:.2f} volte il tempo dell'auto (rapporto mediano pesato per le auto; fattore {f_basso:g} - {f_alto:g})",
         f"  quota di auto con rapporto oltre 2: da {100 * titolo['quota_oltre_2_basso']:.1f}% a {100 * titolo['quota_oltre_2_alto']:.1f}% di {titolo['auto_collegate']:,} auto",
         "", "FASCE E MEDIANA PER GRUPPO (stima seconda | stima dei sensori)"]
    for g in ("a", "b", "ab", "c"):
        gg = gruppi[g]
        r.append(f"  ({g}) {gg['nome']}: {gg['coppie']} coppie, {gg['auto']:,} auto" + (f" - {gg['nota']}" if g == "c" else ""))
        for nome_l, chiave in (("seconda stima", "limite_basso"), ("stima dei sensori", "limite_alto")):
            rr = gg[chiave]
            r.append(f"      {nome_l}, fattore {rr['fattore']:g}: mediano {rr['mediano']:.2f}; oltre 2: {100 * rr['quota_oltre_2']:.1f}%")
            r.append(f"         {riga_fasce(rr)}")
        r.append(f"      senza collegamento entro {TEMPO_MAX_MIN} minuti (a parte): {gg['senza_collegamento']['coppie']} coppie, {gg['senza_collegamento']['auto']:,} auto")
    r += ["", f"LE 15 COPPIE PEGGIORI PER AUTO COINVOLTE (rapporto oltre 2 con la seconda stima, fattore {f_basso:g}; solo gruppi a e b)",
          "  da → a | auto | TP min | auto di punta min (basso-alto) | rapporto (basso-alto)"]
    for p in out["peggiori"]:
        r.append(f"  {p['da_nome']} → {p['a_nome']} | {p['auto']:,} | {p['tp_min']:.0f} | {p['auto_punta_basso_min']:.0f}-{p['auto_punta_min']:.0f} | {p['rapporto_basso']:.1f}-{p['rapporto']:.1f}")
    r += ["", "PER ZONA: quota delle auto in uscita con rapporto oltre 2, seconda stima - stima dei sensori (prime 15, gruppi a+b)"]
    for z in per_zona[:15]:
        r.append(f"  {z['nome']}: {100 * (z['quota_oltre_2_basso'] or 0):.0f}% - {100 * (z['quota_oltre_2_alto'] or 0):.0f}% di {z['auto_uscita']:,} auto")
    r += ["", "NOI CONTRO GOOGLE MAPS (martedì 20/10 alle 8:00; i 6 percorsi da Piazza Castello fissano il fattore basso, i 2 di controllo no)",
          f"  percorso | flusso libero | nostro di punta, fattore alto {f_alto:g} | nostro di punta, fattore basso {f_basso:g} | Google auto | differenza alto / basso (nostro - Google) | mezzi pubblici nostri"]
    for n in noti:
        if not n["google_auto_min"]:
            continue
        r.append(f"  {n['nome']}{' (solo controllo)' if n['controllo'] else ''} | {n['auto_libero_min']:.1f} | {n['auto_punta_min']:.1f} | {n['auto_punta_basso_min']:.1f} | {n['google_auto_min']} | "
                 f"{n['auto_punta_min'] - n['google_auto_min']:+.1f} / {n['auto_punta_basso_min'] - n['google_auto_min']:+.1f} | "
                 + (f"{n['tp_min']:.0f}" if n["tp_min"] is not None else "nessun collegamento")
                 + (f" (Google {n['google_mezzi_min'][0]}-{n['google_mezzi_min'][1]}, {n['google_mezzi_nota']})" if n["google_mezzi_min"] else ""))
    r.append(f"  differenza media sui 6 percorsi: fattore alto {diff_media:+.1f} minuti, fattore basso {diff_basso:+.1f} minuti")
    r += ["", "CONTROLLI"] + [f"  {x}" for x in c.righe]
    r += ["", "LIMITI: tempi TP da orario programmato (ottimisti); fuori Torino mancano treni e altre aziende (gruppo c a parte, gruppo b da leggere con cautela); "
              "la rete stradale non conta semafori e incroci: i tempi in auto sono stimati fra il rallentamento misurato dai sensori 5T e quello di Google Maps, piu' 5 minuti per parcheggiare; "
              "il centro di ogni zona e' una media di punti; IMQ e' un'indagine campionaria."]
    dest_rapp = RAPPORTO.with_name(RAPPORTO.stem + suff + ".txt")
    dest_rapp.write_text("\n".join(r) + "\n", encoding="utf-8")
    log(f"scritto {dest_json.relative_to(RADICE)} e {dest_rapp.relative_to(RADICE)} ({time.time() - t_inizio:.0f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
