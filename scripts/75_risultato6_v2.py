#!/usr/bin/env python3
"""
75_risultato6_v2.py  -  Risultato 6 v2, PASSO G5: universo, tre scenari e copertura.

Cosa fa
-------
1. Costruisce l'UNIVERSO: si valutano solo i luoghi della Citta' metropolitana di Torino
   (macro-aree "01 Torino", "02 Cintura", "03 Resto CMTO" delle zone IMQ). Le fermate del
   resto del Piemonte escono dai percentili e dalle soglie. I luoghi senza zona IMQ
   restano fuori (e vengono elencati nel rapporto).
2. Trasforma i segnali grezzi (Passo G2) in percentili 0-100 fra i soli luoghi
   dell'universo e calcola il punteggio di criticita' in tre scenari:
     S1 "riferimento v1, per luoghi" = a1, b1, c1      (solo per confronto)
     S2 "integrato"                  = a1, a2, b2, c1, c2_ztl, d, e
     S3 "solo nuovi"                 = a2, b2, c2_ztl, d, e
   NOTA del giro 2: b1 (corse nell'ora di punta della v1) e' sostituito da b2 (corse nelle
   ore dei pendolari, 6-10 e 16-20). E' critico il 10% con il punteggio piu' alto, fuori dal
   centro (Q001) e dentro l'universo.
3. Copertura dei luoghi critici: quanti hanno un parcheggio vicino, per quattro insiemi
   (U = 5 interscambi ufficiali; F = parcheggi "di fatto" + potenziali; P = parcheggi aperti
   con almeno 50 posti; F+S = F piu' i parcheggi "solo sulla carta") e tre raggi.
4. Confronti fra scenari e con il giro 1, sensibilita' ai singoli segnali, i 25 luoghi piu'
   scoperti di ogni scenario, i critici per zona IMQ (per il grafico della scheda).

Cosa legge
----------
  data/processed/risultato6_interscambio.json          (v1, per il controllo)
  data/processed/risultato6_v2/luoghi.json             (Passo 1)
  data/processed/risultato6_v2/segnali.json            (Passo G2)
  data/processed/risultato6_v2/nodi.json               (Passo 4: b_giorno)
  data/processed/risultato6_v2/parcheggi_funzione.json (Passo G3)
  data/processed/risultato6_v2/istat2011_proporzioni.json (Passo 7)
  data/processed/risultato6_v2/giro1/scenari.json      (confronto con il giro 1)
  data/processed/imq_zone.json                         (macro-aree delle zone)

Cosa scrive
-----------
  data/processed/risultato6_v2/scenari.json
  docs/RAPPORTO_RISULTATO6_V2.txt

Come si lancia
--------------
  python scripts\\75_risultato6_v2.py
  python scripts\\75_risultato6_v2.py --universo tutto     (per confronto)
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
V1 = RADICE / "data" / "processed" / "risultato6_interscambio.json"
LUOGHI = RADICE / "data" / "processed" / "risultato6_v2" / "luoghi.json"
SEGNALI = RADICE / "data" / "processed" / "risultato6_v2" / "segnali.json"
NODI = RADICE / "data" / "processed" / "risultato6_v2" / "nodi.json"
FUNZIONE = RADICE / "data" / "processed" / "risultato6_v2" / "parcheggi_funzione.json"
ISTAT = RADICE / "data" / "processed" / "risultato6_v2" / "istat2011_proporzioni.json"
GIRO1 = RADICE / "data" / "processed" / "risultato6_v2" / "giro1" / "scenari.json"
ZONE = RADICE / "data" / "processed" / "imq_zone.json"
OUT = RADICE / "data" / "processed" / "risultato6_v2" / "scenari.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_RISULTATO6_V2.txt"

PERCENTILE_CRITICHE = 90.0
ZONA_ESCLUSA = "Q001"
RAGGI = (100, 200, 400)
POSTI_MINIMI_P = 50
MACRO_UNIVERSO = ("01 Torino", "02 Cintura", "03 Resto CMTO")
LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0

SCENARI = {
    "S1": {"titolo": "riferimento v1, per luoghi", "segnali": ["a1", "b1", "c1"]},
    "S2": {"titolo": "integrato",
           "segnali": ["a1", "a2", "b2", "c1", "c2_ztl_scenari", "d", "e"]},
    "S3": {"titolo": "solo nuovi", "segnali": ["a2", "b2", "c2_ztl_scenari", "d", "e"]},
}
NOMI_SEGNALI = {"c2_ztl_scenari": "c2_ztl"}


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def proietta(lon, lat):
    return (lon * FATTORE_GRADI_M * math.cos(math.radians(LAT_RIF)), lat * FATTORE_GRADI_M)


def percentile_rank(valori):
    """Copia della funzione della versione 1: percentile 0-100, valori uguali -> stesso percentile."""
    chiavi = list(valori.keys())
    ordinati = sorted(chiavi, key=lambda k: valori[k])
    n = len(ordinati)
    if n <= 1:
        return {k: 100.0 for k in chiavi}
    rank = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and valori[ordinati[j + 1]] == valori[ordinati[i]]:
            j += 1
        for k in ordinati[i:j + 1]:
            rank[k] = (i + j) / 2
        i = j + 1
    return {k: 100.0 * rank[k] / (n - 1) for k in chiavi}


def soglia_90(valori):
    v = sorted(valori)
    idx = max(0, min(len(v) - 1, round(PERCENTILE_CRITICHE / 100 * (len(v) - 1))))
    return v[idx]


# --- controllo di riproducibilita' (fermate, versione 1) ---------------------------------

def controllo_v1():
    dati = json.loads(V1.read_text(encoding="utf-8"))
    fermate = dati["fermate"]
    a1 = {f["stop_id"]: f["punteggio_corridoio"] for f in fermate}
    b1 = {f["stop_id"]: f["corse_ora_punta"] for f in fermate}
    c1 = {f["stop_id"]: f["pendolari_raw"] for f in fermate}
    p_a1 = percentile_rank(a1)
    p_b1 = percentile_rank(b1)
    p_c1 = percentile_rank(c1)
    punteggi = {k: (p_a1[k] + p_b1[k] + p_c1[k]) / 3.0 for k in a1}
    soglia = soglia_90(list(punteggi.values()))
    ufficiali = [p for p in dati["parcheggi"] if p.get("interscambio")]
    critiche = [f for f in fermate
                if punteggi[f["stop_id"]] >= soglia and f.get("zona_imq") != ZONA_ESCLUSA]
    coperte = [f for f in critiche
               if any(haversine_m(f["lat"], f["lon"], p["lat"], p["lon"]) <= 200 for p in ufficiali)]
    return {"critiche": len(critiche), "coperte": len(coperte),
            "scoperte": len(critiche) - len(coperte),
            "soglia": round(soglia, 2),
            "v1_critiche": sum(1 for f in fermate if f.get("fermata_critica")),
            "v1_coperte": sum(1 for f in fermate if f.get("coperta"))}


# --- punteggi per luogo ------------------------------------------------------------------

def calcola_punteggi(segnali, chiavi):
    """Percentili per segnale fra i luoghi dell'universo, poi media dei disponibili.
    I segnali assenti per un luogo non entrano nella media (e vengono contati)."""
    percentili = {}
    for s in chiavi:
        if s == "e":
            percentili[s] = {l["id_luogo"]: float(l[s]) for l in segnali}
            continue
        valori = {l["id_luogo"]: l[s] for l in segnali if l.get(s) is not None}
        percentili[s] = percentile_rank(valori) if valori else {}
    punteggi = {}
    mancanti = {s: 0 for s in chiavi}
    for l in segnali:
        disponibili = []
        for s in chiavi:
            p = percentili[s].get(l["id_luogo"])
            if p is None:
                mancanti[s] += 1
            else:
                disponibili.append(p)
        punteggi[l["id_luogo"]] = sum(disponibili) / len(disponibili) if disponibili else None
    return punteggi, mancanti


def valuta_scenario(segnali, chiavi):
    """segnali = solo i luoghi dell'universo."""
    punteggi, mancanti = calcola_punteggi(segnali, chiavi)
    valori = [v for v in punteggi.values() if v is not None]
    soglia = soglia_90(valori)
    critici = [l for l in segnali
               if punteggi[l["id_luogo"]] is not None
               and punteggi[l["id_luogo"]] >= soglia
               and l["zona_imq"] != ZONA_ESCLUSA]
    per_luogo = {}
    for l in segnali:
        per_luogo[l["id_luogo"]] = {
            "punteggio": round(punteggi[l["id_luogo"]], 2)
            if punteggi[l["id_luogo"]] is not None else None,
            "segnali": {NOMI_SEGNALI.get(s, s): l.get(s) for s in chiavi},
        }
    return {"segnali": chiavi, "soglia": round(soglia, 2),
            "critici": [l["id_luogo"] for l in critici],
            "punteggi": per_luogo, "mancanti": mancanti}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universo", choices=("cmto", "tutto"), default="cmto",
                    help="cmto = solo Citta' metropolitana di Torino (default); tutto = tutte le fermate")
    args = ap.parse_args()

    for p in (V1, LUOGHI, SEGNALI, NODI, FUNZIONE, ISTAT, ZONE):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    print("CONTROLLO DI RIPRODUCIBILITA': rifaccio S1 per fermata con i valori della v1...")
    controllo = controllo_v1()
    print(f"  fermate critiche: {controllo['critiche']} (v1: {controllo['v1_critiche']}); "
          f"coperte: {controllo['coperte']} (v1: {controllo['v1_coperte']}); scoperte: {controllo['scoperte']}")
    if (controllo["critiche"], controllo["coperte"], controllo["scoperte"]) != (611, 17, 594):
        sys.exit("Controllo di riproducibilita' FALLITO (atteso 611 / 17 / 594) — FERMO.")

    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    segnali_tutti = json.loads(SEGNALI.read_text(encoding="utf-8"))["luoghi"]
    nodi = {n["id_luogo"]: n for n in json.loads(NODI.read_text(encoding="utf-8"))["luoghi"]}
    funz = json.loads(FUNZIONE.read_text(encoding="utf-8"))["parcheggi"]
    istat = json.loads(ISTAT.read_text(encoding="utf-8"))

    print("universo: leggo le macro-aree delle zone IMQ...")
    macro = {z["cod"]: z["macro"] for z in json.loads(ZONE.read_text(encoding="utf-8"))}
    senza_zona = [s for s in segnali_tutti if not s["zona_imq"]]
    fuori_per_macro = Counter()
    for s in segnali_tutti:
        if s["zona_imq"] and macro.get(s["zona_imq"]) not in MACRO_UNIVERSO:
            fuori_per_macro[macro.get(s["zona_imq"], "zona non elencata")] += 1
    if args.universo == "cmto":
        segnali = [s for s in segnali_tutti if macro.get(s["zona_imq"]) in MACRO_UNIVERSO]
    else:
        segnali = [s for s in segnali_tutti if s["zona_imq"]]
    print(f"  luoghi nell'universo ({args.universo}): {len(segnali)} su {len(segnali_tutti)}")
    print(f"  fuori per macro-area: {dict(fuori_per_macro)}; senza zona IMQ: {len(senza_zona)}")

    # c2_ztl completato dove le interviste sono poche (ISTAT 2011, solo proporzioni)
    completate = set(istat["zone_completate"])
    zone_istat = istat["zone"]
    for s in segnali_tutti:
        s["c2_ztl_completo"] = s["c2_ztl"]
        if s["zona_imq"] in completate and zone_istat.get(s["zona_imq"], {}).get("c2_completo") is not None:
            s["c2_ztl_completo"] = round(zone_istat[s["zona_imq"]]["c2_completo"] + (s["c3"] or 0.0), 1)
        s["c2_ztl_scenari"] = s["c2_ztl_completo"]
        s["b_giorno"] = nodi.get(s["id_luogo"], {}).get("b_giorno_corse_ora")

    print("calcolo i tre scenari...")
    risultati = {}
    for nome, ss in SCENARI.items():
        r = valuta_scenario(segnali, ss["segnali"])
        risultati[nome] = r
        print(f"  {nome}: {len(r['critici'])} luoghi critici, soglia {r['soglia']}")

    # --- copertura ---
    print("calcolo la copertura (parcheggi vicini ai luoghi critici)...")
    aperti = ("interscambio_ufficiale", "garage_5t", "park_ride_osm", "osm_pubblico")
    insiemi = {
        "U": [p for p in funz if p["tipo"] == "interscambio_ufficiale"],
        "F": [p for p in funz if p["classe"] in ("interscambio_di_fatto", "potenziale")],
        "P": [p for p in funz if p["tipo"] in aperti and (p["posti"] or 0) >= POSTI_MINIMI_P],
    }
    insiemi["F+S"] = insiemi["F"] + [p for p in funz if p["classe"] == "solo_sulla_carta"]
    alberi = {}
    for k, v in insiemi.items():
        if v:
            alberi[k] = cKDTree(np.array([proietta(p["lon"], p["lat"]) for p in v]))
    posizioni = {l["id_luogo"]: (l["lat"], l["lon"]) for l in segnali_tutti}
    tutti_parchi = [p for p in funz]
    xy_parchi = np.array([proietta(p["lon"], p["lat"]) for p in tutti_parchi]) if tutti_parchi else None
    albero_tutti = cKDTree(xy_parchi) if tutti_parchi else None

    copertura = {}
    coperti_f200 = {}
    for nome, r in risultati.items():
        copertura[nome] = {}
        coperti_f200[nome] = set()
        for insieme in ("U", "F", "P", "F+S"):
            copertura[nome][insieme] = {}
            for raggio in RAGGI:
                n = 0
                for idl in r["critici"]:
                    lat, lon = posizioni[idl]
                    xy = proietta(lon, lat)
                    if insieme in alberi and len(alberi[insieme].query_ball_point(xy, raggio)) > 0:
                        n += 1
                        if insieme == "F" and raggio == 200:
                            coperti_f200[nome].add(idl)
                copertura[nome][insieme][raggio] = n
    print("  coperti a 200 m:", {n: {k: copertura[n][k][200] for k in ("U", "F", "P", "F+S")}
                                 for n in risultati})

    # --- confronto fra scenari ---
    def insieme(nome):
        return set(risultati[nome]["critici"])

    comune = {f"{a}∩{b}": len(insieme(a) & insieme(b))
              for a, b in (("S1", "S2"), ("S1", "S3"), ("S2", "S3"))}
    dettaglio = {l["id_luogo"]: l for l in segnali_tutti}

    def riga_dettaglio(idl, punteggio):
        d = dettaglio[idl]
        seg = " ".join(f"{k}={d.get(k)}" for k in ("a1", "a2", "b1", "b2", "c1", "c2_ztl"))
        return {"id_luogo": idl, "nome": d["nome"], "zona_imq": d["zona_imq"],
                "punteggio": punteggio, "segnali": seg}

    confronti = {}
    for altra in ("S2", "S3"):
        entrano = sorted(insieme(altra) - insieme("S1"),
                         key=lambda i: -risultati[altra]["punteggi"][i]["punteggio"])[:15]
        escono = sorted(insieme("S1") - insieme(altra),
                        key=lambda i: -risultati["S1"]["punteggi"][i]["punteggio"])[:15]
        confronti[altra] = {
            "n_entrano": len(insieme(altra) - insieme("S1")),
            "n_escono": len(insieme("S1") - insieme(altra)),
            "entrano": [riga_dettaglio(i, risultati[altra]["punteggi"][i]["punteggio"]) for i in entrano],
            "escono": [riga_dettaglio(i, risultati["S1"]["punteggi"][i]["punteggio"]) for i in escono],
        }

    # --- confronto con il giro 1 ---
    confronto_giro1 = {}
    if GIRO1.exists():
        g1 = json.loads(GIRO1.read_text(encoding="utf-8"))["scenari"]
        for nome in ("S1", "S2", "S3"):
            vecchi = {c["id_luogo"]: c["punteggio"] for c in g1.get(nome, {}).get("critici", [])}
            nuovi = set(risultati[nome]["critici"])
            restano = nuovi & set(vecchi)
            entrano = nuovi - set(vecchi)
            escono = set(vecchi) - nuovi
            cambiati = sorted(
                ((abs(risultati[nome]["punteggi"][i]["punteggio"] - vecchi[i]), i) for i in restano),
                reverse=True)[:15]
            confronto_giro1[nome] = {
                "giro1_critici": len(vecchi), "critici": len(nuovi),
                "restano": len(restano), "entrano": len(entrano), "escono": len(escono),
                "piu_cambiati": [
                    {"id_luogo": i, "nome": dettaglio[i]["nome"], "zona_imq": dettaglio[i]["zona_imq"],
                     "giro1": vecchi[i], "giro2": risultati[nome]["punteggi"][i]["punteggio"]}
                    for _, i in cambiati],
            }
    else:
        print("  (nessun file del giro 1: salto il confronto)")

    # --- sensibilita' su S2 ---
    print("sensibilita' ai singoli segnali...")
    base = SCENARI["S2"]["segnali"]
    varianti = {
        "senza_a1": [s for s in base if s != "a1"],
        "senza_a2": [s for s in base if s != "a2"],
        "senza_b2": [s for s in base if s != "b2"],
        "senza_c1": [s for s in base if s != "c1"],
        "senza_c2_ztl": [s for s in base if s != "c2_ztl_scenari"],
        "senza_d": [s for s in base if s != "d"],
        "senza_e": [s for s in base if s != "e"],
        "c2_invece_di_c2_ztl": [s if s != "c2_ztl_scenari" else "c2" for s in base],
        "b_giorno_invece_di_b2": [s if s != "b2" else "b_giorno" for s in base],
        "b1_invece_di_b2": [s if s != "b2" else "b1" for s in base],
    }
    sensibilita = {}
    for nome, ss in varianti.items():
        r = valuta_scenario(segnali, ss)
        nuovo = set(r["critici"])
        vecchio = insieme("S2")
        sensibilita[nome] = {"segnali": [NOMI_SEGNALI.get(s, s) for s in ss], "critici": len(nuovo),
                             "entrano": len(nuovo - vecchio), "escono": len(vecchio - nuovo),
                             "cambiano": len(nuovo ^ vecchio), "in_comune": len(nuovo & vecchio)}
    if args.universo == "cmto":
        segnali_tutto = [s for s in segnali_tutti if s["zona_imq"]]
        r = valuta_scenario(segnali_tutto, base)
        nuovo = set(r["critici"])
        vecchio = insieme("S2")
        sensibilita["universo_tutto"] = {"segnali": [NOMI_SEGNALI.get(s, s) for s in base],
                                         "critici": len(nuovo), "entrano": len(nuovo - vecchio),
                                         "escono": len(vecchio - nuovo),
                                         "cambiano": len(nuovo ^ vecchio), "in_comune": len(nuovo & vecchio)}

    # --- i piu' scoperti (senza U ne' F a 400 m) ---
    print("cerco i luoghi critici piu' scoperti...")
    piu_scoperti = {}
    for nome, r in risultati.items():
        sel = []
        for idl in r["critici"]:
            lat, lon = posizioni[idl]
            xy = proietta(lon, lat)
            coperto = False
            for insieme_nome in ("U", "F"):
                if len(alberi[insieme_nome].query_ball_point(xy, 400)) > 0:
                    coperto = True
                    break
            if coperto:
                continue
            d_vicino, i_vicino = None, None
            if albero_tutti is not None:
                d, i = albero_tutti.query(xy)
                d_vicino, i_vicino = d, int(i)
            d = dettaglio[idl]
            sel.append({"id_luogo": idl, "nome": d["nome"], "zona_imq": d["zona_imq"],
                        "punteggio": r["punteggi"][idl]["punteggio"],
                        "segnali": " ".join(f"{k}={d.get(k)}" for k in
                                            ("a1", "a2", "b1", "b2", "c1", "c2_ztl", "d", "e")),
                        "parcheggio_vicino": tutti_parchi[i_vicino]["nome"] if i_vicino is not None else None,
                        "parcheggio_tipo": tutti_parchi[i_vicino]["tipo"] if i_vicino is not None else None,
                        "distanza_parcheggio_m": round(d_vicino) if d_vicino is not None else None})
        piu_scoperti[nome] = sorted(sel, key=lambda x: -x["punteggio"])[:25]

    # --- per zona ---
    print("conteggi per zona IMQ...")
    per_zona = {}
    for nome, r in risultati.items():
        z = {}
        for idl in r["critici"]:
            cod = dettaglio[idl]["zona_imq"] or "senza zona"
            z.setdefault(cod, {"critici": 0, "coperti_f200": 0})
            z[cod]["critici"] += 1
            if idl in coperti_f200[nome]:
                z[cod]["coperti_f200"] += 1
        per_zona[nome] = z

    # --- output ---
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "controllo_riproducibilita": controllo,
        "universo": args.universo,
        "universo_macro": list(MACRO_UNIVERSO),
        "n_universo": len(segnali),
        "n_fuori_universo": {k: v for k, v in fuori_per_macro.items()},
        "senza_zona": senza_zona,
        "parametri": {"percentile_critiche": PERCENTILE_CRITICHE, "zona_esclusa": ZONA_ESCLUSA,
                      "raggi": list(RAGGI), "posti_minimi_p": POSTI_MINIMI_P},
        "scenari": {n: {"titolo": SCENARI[n]["titolo"],
                        "segnali": [NOMI_SEGNALI.get(s, s) for s in r["segnali"]],
                        "soglia": r["soglia"], "n_critici": len(r["critici"]),
                        "critici": [{"id_luogo": i, **r["punteggi"][i]} for i in r["critici"]],
                        "mancanti": r["mancanti"],
                        "copertura": copertura[n]}
                    for n, r in risultati.items()},
        "confronti": comune,
        "entrano_escono": confronti,
        "confronto_giro1": confronto_giro1,
        "sensibilita": sensibilita,
        "piu_scoperti": piu_scoperti,
        "per_zona": per_zona,
        "insiemi_parcheggi": {k: len(v) for k, v in insiemi.items()},
    }, ensure_ascii=False), encoding="utf-8")

    # --- rapporto ---
    righe = []
    righe.append("RAPPORTO RISULTATO 6 v2, GIRO 2 — LUOGHI CRITICI E COPERTURA (Passo G5)")
    righe.append("Le fermate vicine sono unite in LUOGHI (fermate entro 40 m). Un luogo e' critico")
    righe.append("se sta nel 10% dei punteggi piu' alti, e' fuori dal centro (Q001) ed e' nell'universo.")
    righe.append(f"Universo: {args.universo} — {len(segnali)} luoghi su {len(segnali_tutti)} "
                 f"(macro-aree {', '.join(MACRO_UNIVERSO)}). Fuori: {dict(fuori_per_macro)} e "
                 f"{len(senza_zona)} luoghi senza zona IMQ.")
    righe.append("Le distanze sono in linea d'aria, non a piedi.")
    righe.append("")
    righe.append("CONTROLLO DI RIPRODUCIBILITA' (v1, fermata per fermata, tutte le 7.045 fermate): "
                 f"{controllo['critiche']} critiche, {controllo['coperte']} coperte, "
                 f"{controllo['scoperte']} scoperte — come la v1 (611 / 17 / 594): OK")
    righe.append("")
    righe.append("== Quadro d'insieme ==")
    righe.append("  scenario | segnali | luoghi critici | coperti U | coperti F | coperti P | coperti F+S (200 m)")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n} {SCENARI[n]['titolo']:22s} {', '.join(NOMI_SEGNALI.get(s, s) for s in SCENARI[n]['segnali']):28s} "
                     f"{len(risultati[n]['critici']):5d}   {copertura[n]['U'][200]:4d}   "
                     f"{copertura[n]['F'][200]:4d}   {copertura[n]['P'][200]:4d}   {copertura[n]['F+S'][200]:4d}")
    righe.append("")
    righe.append("  U = i 5 interscambi ufficiali")
    righe.append(f"  F = parcheggi 'interscambio_di_fatto' + 'potenziale' ({len(insiemi['F'])})")
    righe.append(f"  P = parcheggi aperti con almeno {POSTI_MINIMI_P} posti ({len(insiemi['P'])})")
    righe.append(f"  F+S = F piu' i 'solo_sulla_carta' ({len(insiemi['F+S'])})")
    righe.append("")
    righe.append("== Copertura completa per scenario, insieme e raggio ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n} ({len(risultati[n]['critici'])} critici):")
        for insieme_nome in ("U", "F", "P", "F+S"):
            righe.append(f"     {insieme_nome:3s}: " + "  ".join(
                f"{r} m -> {copertura[n][insieme_nome][r]}" for r in RAGGI))
    righe.append("")
    righe.append("== Confronto fra scenari ==")
    for n in ("S2", "S3"):
        righe.append(f"  S1 -> {n}: critici in comune {comune['S1∩' + n]}, "
                     f"entrano {confronti[n]['n_entrano']}, escono {confronti[n]['n_escono']}")
    righe.append(f"  S2 e S3 in comune: {comune['S2∩S3']}")
    righe.append("")
    for n in ("S2", "S3"):
        righe.append(f"  -- 15 luoghi che ENTRANO passando da S1 a {n}")
        for e in confronti[n]["entrano"]:
            righe.append(f"     {e['punteggio']:6.1f}  {e['nome'][:40]:40s} zona={e['zona_imq'] or '-'}  {e['segnali']}")
        righe.append(f"  -- 15 luoghi che ESCONO passando da S1 a {n}")
        for e in confronti[n]["escono"]:
            righe.append(f"     {e['punteggio']:6.1f}  {e['nome'][:40]:40s} zona={e['zona_imq'] or '-'}  {e['segnali']}")
        righe.append("")
    righe.append("== Confronto con il giro 1 ==")
    for n in ("S1", "S2", "S3"):
        g = confronto_giro1.get(n)
        if not g:
            continue
        righe.append(f"  {n}: giro 1 {g['giro1_critici']} critici -> giro 2 {g['critici']}; "
                     f"restano {g['restano']}, entrano {g['entrano']}, escono {g['escono']}")
        for c in g["piu_cambiati"][:15]:
            righe.append(f"     {c['giro1']:6.1f} -> {c['giro2']:6.1f}  {c['nome'][:40]:40s} zona={c['zona_imq'] or '-'}")
    righe.append("")
    righe.append("== Sensibilita': cosa cambia togliendo o sostituendo un segnale di S2 ==")
    righe.append(f"  S2 completo: {len(risultati['S2']['critici'])} luoghi critici")
    for nome, s in sensibilita.items():
        righe.append(f"  {nome:24s} critici {s['critici']:4d}  entrano {s['entrano']:3d}  "
                     f"escono {s['escono']:3d}  cambiano {s['cambiano']:3d}")
    righe.append("")
    righe.append("== I 25 luoghi critici piu' scoperti di ogni scenario (nessun parcheggio U o F a 400 m) ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  -- {n}: {len(piu_scoperti[n])} in tabella")
        for x in piu_scoperti[n]:
            righe.append(f"     {x['punteggio']:6.1f}  {x['nome'][:36]:36s} zona={x['zona_imq'] or '-':5s} "
                         f"piu' vicino: {str(x['parcheggio_vicino'])[:26]:26s} {x['distanza_parcheggio_m']} m")
        righe.append("")
    righe.append("== Luoghi critici per zona IMQ (F coperto a 200 m) ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  -- {n}: " + ", ".join(
            f"{z} {v['critici']}({v['coperti_f200']})"
            for z, v in sorted(per_zona[n].items(), key=lambda kv: -kv[1]["critici"])[:12]))
    righe.append("")
    righe.append("== Segnali mancanti per scenario (solo luoghi dell'universo) ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n}: " + ", ".join(f"{NOMI_SEGNALI.get(k, k)} {v}"
                                            for k, v in risultati[n]["mancanti"].items()))
    righe.append("")
    righe.append("== I 23 luoghi senza zona IMQ (fuori dall'universo: decide Leo che farne) ==")
    for s in senza_zona:
        righe.append(f"  {s['id_luogo']}  {s['nome'][:44]:44s} {s['lat']:.5f}, {s['lon']:.5f}")
    righe.append("")
    righe.append("== Limiti da tenere presenti ==")
    for testo in (
        "Riempimento: pochi giorni feriali [DATI SCARSI]; 4 parcheggi non trasmettono; "
        "soglie provvisorie; da rifare con almeno 5 giorni feriali.",
        "Parcheggi OpenStreetMap: elenco incompleto; posti stimati dalla superficie (~25 m2 a posto) "
        "[STIMATO]; tariffa spesso ignota; nessun riempimento per i parcheggi gratuiti (attorno a Fermi).",
        "La 'zona centrale' dei parcheggi (Q001-Q009) e' una scelta provvisoria: vedi la tabella di "
        "sensibilita' del rapporto del Passo G3.",
        "Pendolari IMQ: indagine campionaria, residenti 11-84 anni; la zona IMQ da' lo stesso valore a "
        "tutti i luoghi della zona; le zone con poche interviste sono completate con proporzioni ISTAT 2011.",
        "Importanza della strada (a2): punteggi della Fase 5 corretti per classe (primarie >= 4, "
        "secondarie >= 3) — la stima del traffico e' debole (±38%) e qui conta solo come ordine.",
        "Calo di velocita' (d): solo vicino a un sensore 5T (97 sensori usati, i valori anomali scartati).",
        "Distanze in linea d'aria, non a piedi. Corse da orario programmato [PROGRAMMATO].",
        "Universo: solo Citta' metropolitana di Torino; le fermate del resto del Piemonte non sono valutate.",
        "Treni: le stazioni vengono da OpenStreetMap; le frequenze dei treni non sono nei dati.",
    ):
        righe.append(f"  - {testo}")
    righe.append("")
    righe.append("Nessuno scenario e' indicato come migliore: li sceglie Leo.")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT}")
    print(f"Scritto: {RAPPORTO}")
    for n in ("S1", "S2", "S3"):
        print(f"  {n}: {len(risultati[n]['critici'])} critici, coperti U/F/P/F+S a 200 m: "
              f"{copertura[n]['U'][200]}/{copertura[n]['F'][200]}/{copertura[n]['P'][200]}/{copertura[n]['F+S'][200]}")


if __name__ == "__main__":
    sys.exit(main())
