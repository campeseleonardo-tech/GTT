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
     Classi: sotto 1,5 «conviene», da 1,5 a 2 «poco», oltre 2 «non conviene».

Come si lancia
--------------
  python scripts\\93_tp_contro_auto.py --prova 10        (10 zone: scrive file con suffisso _prova)
  python scripts\\93_tp_contro_auto.py                   (tutte le zone; ripartibile: salva a tappe)
  Opzioni: --fattore 1.5   --lotto 20

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
FATTORE_PREDEFINITO = 1.5
MIN_PARCHEGGIO = 5.0
FATTORI_SENS = (1.3, 1.8)
SOGLIA_CONVIENE, SOGLIA_NON = 1.5, 2.0
QUOTA_MIN_COLLEGATA = 0.5           # meta' del peso delle coppie di punti con collegamento
AVVISO_QUOTA_NON_CONVIENE = 0.60

# percorsi noti (lat, lon), gli stessi dello script 50b; il primo e' il controllo della Fase 5
CASTELLO = (45.0703, 7.6869)
NOTI = [("Piazza Castello → Collegno", CASTELLO, (45.0721, 7.5717)),
        ("Piazza Castello → Venaria Reale", CASTELLO, (45.1352, 7.6330)),
        ("Piazza Castello → Settimo Torinese", CASTELLO, (45.1395, 7.7703)),
        ("Piazza Castello → Moncalieri", CASTELLO, (45.0005, 7.6810)),
        ("Piazza Castello → Orbassano", CASTELLO, (45.0070, 7.5373)),
        ("Piazza Castello → Rivoli", CASTELLO, (45.0709, 7.5167))]


def classe(rapporto):
    return "conviene" if rapporto < SOGLIA_CONVIENE else ("poco" if rapporto <= SOGLIA_NON else "non conviene")


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

    def nodo_vicino(lat, lon):
        d2 = (xy[:, 0] - lat) ** 2 + (xy[:, 1] - lon) ** 2
        return int(np.argmin(d2))

    nodi_extra = [(nodo_vicino(a[0], a[1]), nodo_vicino(b[0], b[1])) for _, a, b in extra]
    nodi = sorted({p["nodo"] for z in zone.values() for p in z["punti"]} | {n for c in nodi_extra for n in c})
    t = {}
    for i in range(0, len(nodi), 25):
        gruppo = nodi[i:i + 25]
        dist = dijkstra(M, indices=gruppo)[:, nodi]
        for k, a in enumerate(gruppo):
            for j, b in enumerate(nodi):
                t[(a, b)] = float(dist[k, j])
    return t, nodi_extra


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
    from shapely.geometry import Point
    elenco = []                                       # (id, lat, lon)
    for cod, z in zone.items():
        for k, p in enumerate(z["punti"]):
            elenco.append((f"{cod}_{k}", p["lat"], p["lon"]))
    for k, (_, a, b) in enumerate(extra):
        elenco.append((f"NOTO{k}_A", a[0], a[1]))
        elenco.append((f"NOTO{k}_B", b[0], b[1]))
    ids = [e[0] for e in elenco]
    firma = f"{len(ids)}-{round(sum(e[1] + e[2] for e in elenco), 5)}-{GIORNO}-{PARTENZA}-{FINESTRA_MIN}-{TEMPO_MAX_MIN}"
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
                               transport_modes=[TM.TRANSIT, TM.WALK],
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", type=int, default=0, help="usa solo le N zone con piu' auto in uscita")
    ap.add_argument("--fattore", type=float, default=FATTORE_PREDEFINITO)
    ap.add_argument("--lotto", type=int, default=20, help="origini per chiamata r5py (e per salvataggio)")
    args = ap.parse_args()
    t_inizio = time.time()
    c = comuni.Controlli()

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
    log(f"zone: {len(zone)} con punti; auto del mattino fra le zone incluse: {totale_zone:,.0f}")

    log("D2: tempi in auto sulla rete del modello del traffico ...")
    t_auto, nodi_extra = matrice_auto(zone, NOTI)
    log("D1: tempi coi mezzi pubblici (r5py) ...")
    ids, T = matrice_tp(zone, NOTI, args.lotto, log)
    pos = {i: k for k, i in enumerate(ids)}

    # ---- tempi per coppia di zone
    cod = sorted(zone)
    coppie = []
    senza_link = []
    auto_senza = 0.0
    intra = 0.0
    for a in cod:
        for b in cod:
            v = auto.get((a, b), 0.0)
            if a == b:
                intra += v
                continue
            ta = tempo_zone_auto(zone[a], zone[b], t_auto) / 60.0           # minuti, flusso libero
            tp, quota = tempo_zone_tp(zone[a], a, zone[b], b, pos, T)
            if tp is None or quota < QUOTA_MIN_COLLEGATA:
                auto_senza += v
                senza_link.append({"da": a, "a": b, "auto": round(v, 1), "auto_libero_min": round(ta, 1), "quota_collegata": round(quota, 2)})
                continue
            coppie.append({"da": a, "a": b, "auto": v, "tp_min": tp, "libero_min": ta, "quota_collegata": quota})

    def punta(libero, f):
        return libero * f + MIN_PARCHEGGIO

    def riepilogo(f):
        tot = sum(p["auto"] for p in coppie)
        per = defaultdict(float)
        n_per = defaultdict(int)
        for p in coppie:
            k = classe(p["tp_min"] / punta(p["libero_min"], f))
            per[k] += p["auto"]
            n_per[k] += 1
        return {"fattore": f, "auto_collegate": round(tot), "auto": {k: round(v) for k, v in per.items()},
                "coppie": dict(n_per), "quota_non_conviene": per["non conviene"] / tot if tot else 0.0,
                "quota_conviene": per["conviene"] / tot if tot else 0.0}

    base = riepilogo(args.fattore)
    sens = [riepilogo(f) for f in FATTORI_SENS]
    for p in coppie:
        p["auto_punta_min"] = punta(p["libero_min"], args.fattore)
        p["rapporto"] = p["tp_min"] / p["auto_punta_min"]
        p["classe"] = classe(p["rapporto"])
    auto_coll = sum(p["auto"] for p in coppie)

    peggiori = sorted((p for p in coppie if p["classe"] == "non conviene"), key=lambda p: -p["auto"])[:15]
    per_zona = []
    for a in cod:
        mie = [p for p in coppie if p["da"] == a]
        tot = sum(p["auto"] for p in mie)
        nc = sum(p["auto"] for p in mie if p["classe"] == "non conviene")
        per_zona.append({"zona": a, "nome": zone[a]["nome"], "auto_uscita": round(tot), "auto_non_conviene": round(nc),
                         "quota_non_conviene": (nc / tot if tot else None)})
    per_zona.sort(key=lambda z: -(z["quota_non_conviene"] or 0))

    # ---- controllo di buon senso: percorsi noti
    noti = []
    for k, (nome, a, b) in enumerate(NOTI):
        libero = t_auto[(nodi_extra[k][0], nodi_extra[k][1])] / 60.0
        tp = T[pos[f"NOTO{k}_A"], pos[f"NOTO{k}_B"]]
        noti.append({"nome": nome, "auto_libero_min": libero, "auto_punta_min": punta(libero, args.fattore),
                     "auto_punta_13": punta(libero, 1.3), "auto_punta_18": punta(libero, 1.8),
                     "tp_min": (float(tp) if tp == tp else None)})

    # ---- controlli
    c("nessun tempo negativo o nullo fra zone diverse",
      all(p["tp_min"] > 0 and p["libero_min"] > 0 for p in coppie), bloccante=True)
    c("coppie senza collegamento coi mezzi entro 120 minuti (contate a parte)", True,
      dettaglio=f"{len(senza_link)} coppie, {auto_senza:,.0f} auto")
    somma = auto_coll + auto_senza + intra
    c("somma delle auto = totale IMQ 06-10 delle zone incluse", abs(somma - totale_zone) < 1e-6 * max(totale_zone, 1),
      dettaglio=f"{somma:,.0f} / {totale_zone:,.0f} (collegate {auto_coll:,.0f}, senza collegamento {auto_senza:,.0f}, dentro la zona {intra:,.0f})",
      bloccante=True)
    cast = noti[0]
    c("Piazza Castello → Collegno in auto di punta nella fascia 20-35 minuti", 20 <= cast["auto_punta_min"] <= 35,
      dettaglio=f"{cast['auto_libero_min']:.1f} minuti a flusso libero, {cast['auto_punta_min']:.1f} di punta (fattore {args.fattore})")
    if base["quota_non_conviene"] > AVVISO_QUOTA_NON_CONVIENE:
        c(f"AVVISO: piu' del {int(AVVISO_QUOTA_NON_CONVIENE * 100)}% delle auto e' su coppie «non conviene»", False,
          dettaglio=f"{100 * base['quota_non_conviene']:.1f}%: da spiegare")

    nomi = {k: v["nome"] for k, v in zone.items()}
    titolo = {"auto_collegate": round(auto_coll), "auto_non_conviene": base["auto"].get("non conviene", 0),
              "quota_non_conviene": base["quota_non_conviene"],
              "su_dieci": round(10 * base["quota_non_conviene"], 1)}
    prova = bool(args.prova)
    suff = "_prova" if prova else ""
    out = {
        "stimato": True,
        "parametri": {"giorno": str(GIORNO), "partenza": f"{PARTENZA:%H:%M}", "finestra_min": FINESTRA_MIN,
                      "tempo_max_min": TEMPO_MAX_MIN, "punti_per_zona": PUNTI_PER_ZONA, "ore_auto": list(ORE_MATTINO),
                      "fattore_punta": args.fattore, "minuti_parcheggio": MIN_PARCHEGGIO,
                      "soglie": [SOGLIA_CONVIENE, SOGLIA_NON], "n_zone": len(zone), "prova": prova},
        "titolo": titolo, "base": base, "sensibilita": sens,
        "peggiori": [{"da": p["da"], "a": p["a"], "da_nome": nomi[p["da"]], "a_nome": nomi[p["a"]], "auto": round(p["auto"]),
                      "tp_min": round(p["tp_min"], 1), "auto_punta_min": round(p["auto_punta_min"], 1),
                      "rapporto": round(p["rapporto"], 2)} for p in peggiori],
        "per_zona": per_zona,
        "coppie": [{"da": p["da"], "a": p["a"], "auto": round(p["auto"], 1), "tp_min": round(p["tp_min"], 1),
                    "auto_punta_min": round(p["auto_punta_min"], 1), "rapporto": round(p["rapporto"], 2),
                    "classe": p["classe"]} for p in sorted(coppie, key=lambda p: -p["auto"])],
        "senza_collegamento": senza_link, "dentro_zona_auto": round(intra),
        "noti": noti, "totale_auto_zone": round(totale_zone),
        "controlli": list(c.righe),
    }
    dest_json = OUT_JSON.with_name(OUT_JSON.stem + suff + ".json")
    dest_json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    r = [f"RAPPORTO TP CONTRO AUTO (Risultato 8, parte D, STIMATO){' - PROVA' if prova else ''}",
         f"generato: {dt.datetime.now().isoformat(timespec='seconds')}", "",
         f"Zone IMQ con punti: {len(zone)} (zone solo «porta» escluse); fino a {PUNTI_PER_ZONA} punti per zona, i piu' pesanti.",
         f"Tempi coi mezzi: r5py, giorno {GIORNO}, mediana delle partenze 7:45-8:15, mezzi pubblici + cammino, massimo {TEMPO_MAX_MIN} minuti.",
         f"Tempi in auto: rete del modello del traffico, flusso libero x {args.fattore} + {MIN_PARCHEGGIO:.0f} minuti (parcheggio e cammino).",
         f"Auto: viaggi IMQ in auto conducente, partenza 6-10, feriale. Totale fra le zone incluse: {totale_zone:,.0f}.",
         "", "TITOLO",
         f"  auto del mattino su coppie «non conviene» (TP oltre il doppio dell'auto): {titolo['auto_non_conviene']:,} su {titolo['auto_collegate']:,} "
         f"({100 * titolo['quota_non_conviene']:.1f}%, cioe' {titolo['su_dieci']:.1f} su 10)",
         f"  per classe: " + "; ".join(f"{k}: {v:,} auto in {base['coppie'].get(k, 0)} coppie" for k, v in base["auto"].items()),
         f"  senza collegamento TP entro {TEMPO_MAX_MIN} minuti (a parte): {len(senza_link)} coppie, {auto_senza:,.0f} auto; dentro la stessa zona (non confrontate): {intra:,.0f}",
         "", "SENSIBILITA' AL FATTORE DI PUNTA"]
    for s in [base] + sens:
        r.append(f"  fattore {s['fattore']}: «non conviene» {100 * s['quota_non_conviene']:.1f}% delle auto, «conviene» {100 * s['quota_conviene']:.1f}%")
    r += ["", "LE 15 COPPIE PEGGIORI PER AUTO COINVOLTE (non conviene)",
          "  da → a | auto | TP min | auto di punta min | rapporto"]
    for p in out["peggiori"]:
        r.append(f"  {p['da_nome']} → {p['a_nome']} | {p['auto']:,} | {p['tp_min']:.0f} | {p['auto_punta_min']:.0f} | {p['rapporto']:.1f}")
    r += ["", "PER ZONA: quota delle auto in uscita su coppie «non conviene» (prime 15)"]
    for z in per_zona[:15]:
        r.append(f"  {z['nome']}: {100 * (z['quota_non_conviene'] or 0):.0f}% di {z['auto_uscita']:,} auto")
    r += ["", "CONTROLLO DI BUON SENSO: percorsi noti (minuti)",
          "  percorso | auto flusso libero | auto di punta | auto di punta 1,3-1,8 | mezzi pubblici"]
    for n in noti:
        r.append(f"  {n['nome']} | {n['auto_libero_min']:.1f} | {n['auto_punta_min']:.1f} | {n['auto_punta_13']:.1f}-{n['auto_punta_18']:.1f} | "
                 + (f"{n['tp_min']:.0f}" if n["tp_min"] is not None else "nessun collegamento"))
    r += ["", "CONTROLLI"] + [f"  {x}" for x in c.righe]
    r += ["", "LIMITI: tempi TP da orario programmato (ottimisti); auto senza code vere (fattore fisso e 5 minuti per parcheggiare); "
              "il centro di ogni zona e' una media di punti, non una casa; IMQ e' un'indagine campionaria."]
    dest_rapp = RAPPORTO.with_name(RAPPORTO.stem + suff + ".txt")
    dest_rapp.write_text("\n".join(r) + "\n", encoding="utf-8")
    log(f"scritto {dest_json.relative_to(RADICE)} e {dest_rapp.relative_to(RADICE)} ({time.time() - t_inizio:.0f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
