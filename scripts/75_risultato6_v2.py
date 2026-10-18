#!/usr/bin/env python3
"""
75_risultato6_v2.py  -  Risultato 6 v2, PASSO 8: tre scenari e copertura.

Cosa fa
-------
Trasforma i segnali grezzi (Passo 6) in percentili 0-100 e calcola un punteggio di
criticita' per ogni LUOGO in tre scenari fissi:
  S1 "come la v1, per luoghi"  = a1, b1, c1
  S2 "integrato"               = a1, a2, b1, b2, c1, c2_ztl, d, e
  S3 "solo nuovi"              = a2, b2, c2_ztl, d, e
E' critico il luogo nel 10% con il punteggio piu' alto, fuori dal centro (Q001).
Prima di tutto rifa' il calcolo della v1 fermata per fermata: deve uscire lo stesso
numero di fermate critiche (611), altrimenti si ferma.
Poi per ogni scenario conta quanti luoghi critici hanno un parcheggio vicino, per tre
insiemi di parcheggi (ufficiali, di fatto/potenziali, tutti gli aperti con almeno 50
posti) e per tre raggi (100, 200, 400 m). Infine il confronto fra scenari e la
sensibilita' ai singoli segnali nuovi.

Cosa legge
----------
  data/processed/risultato6_interscambio.json     (v1, per il controllo)
  data/processed/risultato6_v2/luoghi.json        (Passo 1)
  data/processed/risultato6_v2/segnali.json       (Passo 6)
  data/processed/risultato6_v2/nodi.json          (Passo 4: b_giorno per la sensibilita')
  data/processed/risultato6_v2/parcheggi_funzione.json (Passo 5)
  data/processed/risultato6_v2/istat2011_proporzioni.json (Passo 7)

Cosa scrive
-----------
  data/processed/risultato6_v2/scenari.json
  docs/RAPPORTO_RISULTATO6_V2.txt

Come si lancia
--------------
  python scripts\\75_risultato6_v2.py
"""
import json
import math
import sys
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
OUT = RADICE / "data" / "processed" / "risultato6_v2" / "scenari.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_RISULTATO6_V2.txt"

PERCENTILE_CRITICHE = 90.0
ZONA_ESCLUSA = "Q001"
RAGGI = (100, 200, 400)
POSTI_MINIMI_P = 50
LAT_RIF = 45.07
FATTORE_GRADI_M = 111000.0

SCENARI = {
    "S1": {"titolo": "come la v1, per luoghi", "segnali": ["a1", "b1", "c1"]},
    "S2": {"titolo": "integrato", "segnali": ["a1", "a2", "b1", "b2", "c1", "c2_ztl", "d", "e"]},
    "S3": {"titolo": "solo nuovi", "segnali": ["a2", "b2", "c2_ztl", "d", "e"]},
}


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

def calcola_punteggi(luoghi, segnali, chiavi):
    """Percentili per segnale su tutti i luoghi che lo hanno, poi media dei disponibili."""
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
    return punteggi, percentili, mancanti


def valuta_scenario(luoghi, segnali, chiavi):
    punteggi, percentili, mancanti = calcola_punteggi(luoghi, segnali, chiavi)
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
            "segnali": {s: l.get(s) for s in chiavi},
        }
    return {"segnali": chiavi, "soglia": round(soglia, 2),
            "critici": [l["id_luogo"] for l in critici],
            "punteggi": per_luogo, "mancanti": mancanti}


def main():
    for p in (V1, LUOGHI, SEGNALI, NODI, FUNZIONE, ISTAT):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    print("CONTROLLO DI RIPRODUCIBILITA': rifaccio S1 per fermata con i valori della v1...")
    controllo = controllo_v1()
    print(f"  fermate critiche: {controllo['critiche']} (v1: {controllo['v1_critiche']}); "
          f"coperte: {controllo['coperte']} (v1: {controllo['v1_coperte']}); scoperte: {controllo['scoperte']}")
    if (controllo["critiche"], controllo["coperte"], controllo["scoperte"]) != (611, 17, 594):
        sys.exit("Controllo di riproducibilita' FALLITO (atteso 611 / 17 / 594) — FERMO.")

    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    segnali = json.loads(SEGNALI.read_text(encoding="utf-8"))["luoghi"]
    nodi = {n["id_luogo"]: n for n in json.loads(NODI.read_text(encoding="utf-8"))["luoghi"]}
    funz = json.loads(FUNZIONE.read_text(encoding="utf-8"))["parcheggi"]
    istat = json.loads(ISTAT.read_text(encoding="utf-8"))

    # c2_ztl completato dove le interviste sono poche
    completate = set(istat["zone_completate"])
    zone_istat = istat["zone"]
    for s in segnali:
        s["c2_ztl_completo"] = s["c2_ztl"]
        if s["zona_imq"] in completate and zone_istat.get(s["zona_imq"], {}).get("c2_completo") is not None:
            s["c2_ztl_completo"] = round(zone_istat[s["zona_imq"]]["c2_completo"]
                                         + (s["c3"] or 0.0), 1)
        s["b_giorno"] = nodi.get(s["id_luogo"], {}).get("b_giorno_corse_ora")
        s["c2_ztl_scenari"] = s["c2_ztl_completo"]

    chiavi = {"S1": ["a1", "b1", "c1"],
              "S2": ["a1", "a2", "b1", "b2", "c1", "c2_ztl_scenari", "d", "e"],
              "S3": ["a2", "b2", "c2_ztl_scenari", "d", "e"]}
    nomi_segnali = {"c2_ztl_scenari": "c2_ztl"}

    print("calcolo i tre scenari...")
    risultati = {}
    for nome, ss in chiavi.items():
        r = valuta_scenario(luoghi, segnali, ss)
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
    alberi = {}
    for k, v in insiemi.items():
        if v:
            xy = np.array([proietta(p["lon"], p["lat"]) for p in v])
            alberi[k] = cKDTree(xy)
    posizioni = {l["id_luogo"]: (l["lat"], l["lon"]) for l in segnali}

    copertura = {}
    for nome, r in risultati.items():
        copertura[nome] = {}
        for insieme in ("U", "F", "P"):
            copertura[nome][insieme] = {}
            for raggio in RAGGI:
                n = 0
                for idl in r["critici"]:
                    lat, lon = posizioni[idl]
                    xy = proietta(lon, lat)
                    if insieme in alberi and len(alberi[insieme].query_ball_point(xy, raggio)) > 0:
                        n += 1
                copertura[nome][insieme][raggio] = n
    print("  coperti a 200 m:", {n: {k: copertura[n][k][200] for k in ("U", "F", "P")}
                                 for n in risultati})

    # --- confronto fra scenari ---
    def insieme(nome):
        return set(risultati[nome]["critici"])

    comune = {f"{a}∩{b}": len(insieme(a) & insieme(b))
              for a, b in (("S1", "S2"), ("S1", "S3"), ("S2", "S3"))}
    dettaglio = {l["id_luogo"]: l for l in segnali}
    sostituzioni = {l["id_luogo"]: l["nome"] for l in luoghi}

    def elenco(ids_entrano, ids_escono, base):
        def riga(idl):
            d = dettaglio[idl]
            seg = " ".join(f"{k}={d.get(k)}" for k in ("a1", "a2", "b1", "b2", "c1", "c2_ztl"))
            return {"id_luogo": idl, "nome": d["nome"], "zona_imq": d["zona_imq"],
                    "punteggio": base[idl], "segnali": seg}
        return ([riga(i) for i in ids_entrano], [riga(i) for i in ids_escono])

    confronti = {}
    for altra in ("S2", "S3"):
        entrano = sorted(insieme(altra) - insieme("S1"),
                         key=lambda i: -risultati[altra]["punteggi"][i]["punteggio"])[:15]
        escono = sorted(insieme("S1") - insieme(altra),
                        key=lambda i: -risultati["S1"]["punteggi"][i]["punteggio"])[:15]
        e, u = elenco(entrano, escono, {**{i: risultati[altra]["punteggi"][i]["punteggio"] for i in entrano},
                                       **{i: risultati["S1"]["punteggi"][i]["punteggio"] for i in escono}})
        confronti[altra] = {"entrano": e, "escono": u,
                            "n_entrano": len(insieme(altra) - insieme("S1")),
                            "n_escono": len(insieme("S1") - insieme(altra))}

    # --- sensibilita' ---
    print("sensibilita' ai singoli segnali nuovi...")
    base = chiavi["S2"]
    varianti = {
        "senza_a2": [s for s in base if s != "a2"],
        "senza_b2": [s for s in base if s != "b2"],
        "senza_c2_ztl": [s for s in base if s != "c2_ztl_scenari"],
        "senza_d": [s for s in base if s != "d"],
        "senza_e": [s for s in base if s != "e"],
        "c2_invece_di_c2_ztl": [s if s != "c2_ztl_scenari" else "c2" for s in base],
        "b_giorno_invece_di_b2": [s if s != "b2" else "b_giorno" for s in base],
    }
    sensibilita = {}
    for nome, ss in varianti.items():
        r = valuta_scenario(luoghi, segnali, ss)
        nuovo = set(r["critici"])
        vecchio = insieme("S2")
        sensibilita[nome] = {
            "segnali": ss, "critici": len(nuovo),
            "entrano": len(nuovo - vecchio), "escono": len(vecchio - nuovo),
            "cambiano": len(nuovo ^ vecchio),
            "in_comune": len(nuovo & vecchio),
        }

    # --- output ---
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "controllo_riproducibilita": controllo,
        "parametri": {"percentile_critiche": PERCENTILE_CRITICHE, "zona_esclusa": ZONA_ESCLUSA,
                      "raggi": list(RAGGI), "posti_minimi_p": POSTI_MINIMI_P},
        "scenari": {n: {"titolo": SCENARI[n]["titolo"], "segnali": [nomi_segnali.get(s, s) for s in r["segnali"]],
                        "soglia": r["soglia"], "n_critici": len(r["critici"]),
                        "critici": [{"id_luogo": i, **r["punteggi"][i]} for i in r["critici"]],
                        "mancanti": r["mancanti"],
                        "copertura": copertura[n]}
                    for n, r in risultati.items()},
        "confronti": comune,
        "entrano_escono": confronti,
        "sensibilita": sensibilita,
        "insiemi_parcheggi": {k: len(v) for k, v in insiemi.items()},
    }, ensure_ascii=False), encoding="utf-8")

    # --- rapporto ---
    righe = []
    righe.append("RAPPORTO RISULTATO 6 v2 — LUOGHI CRITICI E COPERTURA (Passo 8)")
    righe.append("Le fermate vicine sono unite in LUOGHI (fermate entro 40 m). "
                 "Un luogo e' critico se sta nel 10% dei punteggi piu' alti ed e' fuori dal centro (Q001).")
    righe.append("Le distanze sono in linea d'aria, non a piedi.")
    righe.append("")
    righe.append("CONTROLLO DI RIPRODUCIBILITA' (v1, fermata per fermata): "
                 f"{controllo['critiche']} critiche, {controllo['coperte']} coperte, "
                 f"{controllo['scoperte']} scoperte — come la v1 (611 / 17 / 594): OK")
    righe.append("")
    righe.append("== Quadro d'insieme ==")
    righe.append("  scenario | luoghi critici | coperti U 200 m | coperti F 200 m | coperti P 200 m")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n} {SCENARI[n]['titolo']:20s} {len(risultati[n]['critici']):5d}   "
                     f"{copertura[n]['U'][200]:4d}   {copertura[n]['F'][200]:4d}   {copertura[n]['P'][200]:4d}")
    righe.append("")
    righe.append("  U = i 5 interscambi ufficiali")
    righe.append(f"  F = parcheggi 'interscambio_di_fatto' + 'potenziale' ({len(insiemi['F'])})")
    righe.append(f"  P = parcheggi aperti con almeno {POSTI_MINIMI_P} posti ({len(insiemi['P'])})")
    righe.append("")
    righe.append("== Copertura completa per scenario, insieme e raggio ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n} ({len(risultati[n]['critici'])} critici):")
        for insieme_nome in ("U", "F", "P"):
            righe.append(f"     {insieme_nome}: " + "  ".join(
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
    righe.append("== Sensibilita': cosa cambia togliendo o sostituendo un segnale di S2 ==")
    righe.append(f"  S2 completo: {len(risultati['S2']['critici'])} luoghi critici")
    for nome, s in sensibilita.items():
        righe.append(f"  {nome:24s} critici {s['critici']:4d}  entrano {s['entrano']:3d}  "
                     f"escono {s['escono']:3d}  cambiano {s['cambiano']:3d}")
    righe.append("")
    righe.append("== Segnali mancanti per scenario ==")
    for n in ("S1", "S2", "S3"):
        righe.append(f"  {n}: " + ", ".join(f"{nomi_segnali.get(k, k)} {v}"
                                            for k, v in risultati[n]["mancanti"].items()))
    righe.append("")
    righe.append("== Limiti da tenere presenti ==")
    for testo in (
        "Riempimento dei parcheggi: pochi giorni [DATI SCARSI]; 4 parcheggi non trasmettono; "
        "le soglie delle firme sono provvisorie.",
        "Parcheggi OpenStreetMap: elenco incompleto; posti stimati dalla superficie (~25 m2 a posto) "
        "[STIMATO]; tariffa spesso ignota; nessun riempimento per i parcheggi gratuiti (es. attorno a Fermi).",
        "Pendolari IMQ: indagine campionaria, solo residenti 11-84 anni; le zone con poche interviste "
        "sono state completate con le proporzioni ISTAT 2011 (solo proporzioni, mai numeri del 2011).",
        "Velocita': solo dove c'e' un sensore 5T (97 sensori usabili).",
        "Distanze in linea d'aria, non a piedi.",
        "Corse da orario programmato [PROGRAMMATO], non da dati reali.",
        "Treni: le stazioni vengono da OpenStreetMap; le frequenze dei treni non sono nei dati "
        "(il GTFS GTT non ha i treni).",
    ):
        righe.append(f"  - {testo}")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT}")
    print(f"Scritto: {RAPPORTO}")
    for n in ("S1", "S2", "S3"):
        print(f"  {n}: {len(risultati[n]['critici'])} critici, coperti U/F/P a 200 m: "
              f"{copertura[n]['U'][200]}/{copertura[n]['F'][200]}/{copertura[n]['P'][200]}")


if __name__ == "__main__":
    sys.exit(main())
