#!/usr/bin/env python3
"""
79_dati_mappa_r6.py  -  Risultato 6 v2: il file piccolo che leggono la mappa e la scheda.

Cosa fa
-------
Prende i risultati gia' prodotti del Risultato 6 v2 (scenario S2, quello scelto da Leo) e
li mette in un unico file JSON compatto, pronto per essere disegnato sulla mappa e raccontato
nella scheda. Non rifa calcoli sui dati grezzi: solo distanze in linea d'aria e conteggi.

Contiene:
  - scenario: nome, titolo, segnali usati, soglia, quanti luoghi critici, quanti nell'universo;
  - luoghi_critici: i 378 luoghi critici con il parcheggio piu' vicino (di fatto/potenziale,
    ufficiale) e se hanno un parcheggio entro 200 m;
  - parcheggi: i parcheggi che contano (di fatto, solo sulla carta, potenziali e i garage 5T)
    con firma del riempimento e profilo orario;
  - ufficiali: i 5 parcheggi di interscambio ufficiali (raggio 200 m);
  - zona_centrale: i confini delle zone IMQ Q001-Q009 (centro), semplificati;
  - eventi: i luoghi di evento (da eventi.json) con le auto stimate e i posti vicini;
  - riepilogo: i numeri gia' pronti per la scheda.

Cosa legge
----------
  data/processed/risultato6_v2/scenari.json            (scenario S2 e coperture)
  data/processed/risultato6_v2/luoghi.json             (coordinate dei luoghi)
  data/processed/risultato6_v2/parcheggi.json          (posti dichiarati o stimati)
  data/processed/risultato6_v2/parcheggi_funzione.json (classe, motivo, punti a favore)
  data/processed/risultato6_v2/riempimento.json        (firme e profili orari 5T)
  data/processed/risultato6_v2/eventi.json             (dallo script 78)
  data/processed/imq_zone_geo.json                     (poligoni delle zone, [lat, lon])
  data/processed/imq_zone.json                         (nomi delle zone)

Cosa scrive
-----------
  data/processed/risultato6_v2/mappa_r6.json
  docs/RAPPORTO_R6V2_MAPPA_DATI.txt

Come si lancia
--------------
  python scripts\\79_dati_mappa_r6.py
"""
import json
import math
import sys
from datetime import datetime
from pathlib import Path

from shapely.geometry import Polygon, MultiPolygon

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
P = RADICE / "data" / "processed" / "risultato6_v2"
SCENARI = P / "scenari.json"
LUOGHI = P / "luoghi.json"
PARCHEGGI = P / "parcheggi.json"
FUNZIONE = P / "parcheggi_funzione.json"
RIEMPIMENTO = P / "riempimento.json"
EVENTI = P / "eventi.json"
ZONE_GEO = RADICE / "data" / "processed" / "imq_zone_geo.json"
ZONE = RADICE / "data" / "processed" / "imq_zone.json"
OUT = P / "mappa_r6.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_MAPPA_DATI.txt"

SCENARIO = "S2"
ZONE_CENTRALI = [f"Q{i:03d}" for i in range(1, 10)]
RAGGIO_COPERTURA = 200.0
RAGGIO_F = 2000.0
POSTI_MINIMI_P = 50
LIMITE_BYTE = 1_500_000


def haversine_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def piu_vicino(lat, lon, lista):
    """Ritorna (elemento, distanza) del piu' vicino, o (None, None) se la lista e' vuota."""
    migliore, d_min = None, None
    for e in lista:
        d = haversine_m(lat, lon, e["lat"], e["lon"])
        if d_min is None or d < d_min:
            migliore, d_min = e, d
    return migliore, d_min


def poligoni_zona(anelli):
    """Da una lista di anelli [lat, lon] a un poligono shapely nel piano (x=lon, y=lat)."""
    shell = [(p[1], p[0]) for p in anelli[0]]
    buchi = [[(p[1], p[0]) for p in a] for a in anelli[1:]]
    try:
        return Polygon(shell, buchi)
    except Exception:
        return Polygon(shell)


def anelli_da_geometria(geom):
    """Da poligono/multipoligono semplificato a liste [[lat, lon], ...]."""
    pezzi = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    anelli = []
    for pol in pezzi:
        anelli.append([[round(y, 5), round(x, 5)] for x, y in pol.exterior.coords])
    return anelli


def carica_posti_origine(parcheggi):
    """{id: 'dichiarati'/'stimati'/'nessuno'} da parcheggi.json."""
    out = {}
    for p in parcheggi:
        if p.get("posti_dichiarati"):
            out[p["id"]] = "dichiarati"
        elif p.get("posti_stimati"):
            out[p["id"]] = "stimati"
        else:
            out[p["id"]] = "nessuno"
    return out


def carica_id_5t(parcheggi):
    """{id parcheggio: id_5t} da parcheggi.json (parcheggi_funzione.json non ha id_5t)."""
    return {p["id"]: p.get("id_5t") for p in parcheggi}


def profilo_feriale_24(r):
    if not r or not r.get("profilo_feriale"):
        return None
    prof = r["profilo_feriale"]
    return [round(float(prof.get(str(h), 0)), 2) for h in range(24)]


def main():
    for f in (SCENARI, LUOGHI, PARCHEGGI, FUNZIONE, RIEMPIMENTO, EVENTI, ZONE_GEO, ZONE):
        if not f.exists():
            sys.exit(f"Manca: {f}")

    sc = json.loads(SCENARI.read_text(encoding="utf-8"))
    luoghi = json.loads(LUOGHI.read_text(encoding="utf-8"))["luoghi"]
    parcheggi = json.loads(PARCHEGGI.read_text(encoding="utf-8"))["parcheggi"]
    funzione = json.loads(FUNZIONE.read_text(encoding="utf-8"))["parcheggi"]
    riemp = json.loads(RIEMPIMENTO.read_text(encoding="utf-8"))
    eventi = json.loads(EVENTI.read_text(encoding="utf-8"))
    geo = json.loads(ZONE_GEO.read_text(encoding="utf-8"))
    zone_nomi = {z["cod"]: z for z in json.loads(ZONE.read_text(encoding="utf-8"))}

    s2 = sc["scenari"][SCENARIO]
    by_id_luogo = {l["id_luogo"]: l for l in luoghi}
    posti_origine = carica_posti_origine(parcheggi)
    id_5t_per_id = carica_id_5t(parcheggi)
    riemp_per_5t = {r["id_5t"]: r for r in riemp["parcheggi"]}

    # --- insiemi di parcheggi (come in scenari.json) ---
    F = [p for p in funzione if p["classe"] in ("interscambio_di_fatto", "potenziale")]
    S = [p for p in funzione if p["classe"] == "solo_sulla_carta"]
    U = [p for p in funzione if p["tipo"] == "interscambio_ufficiale"]
    Pset = [p for p in funzione if (p["posti"] or 0) >= POSTI_MINIMI_P]
    print(f"insiemi: U={len(U)} F={len(F)} S={len(S)} P={len(Pset)}")

    # --- PASSO E3.1 scenario ---
    scenario = {
        "id": SCENARIO, "titolo": s2["titolo"], "segnali": s2["segnali"],
        "soglia": s2["soglia"], "n_critici": s2["n_critici"],
        "universo": sc["n_universo"],
    }

    # --- PASSO E3.2 luoghi critici ---
    luoghi_critici = []
    conta_f200 = conta_u200 = conta_p200 = conta_fs200 = 0
    for c in s2["critici"]:
        l = by_id_luogo[c["id_luogo"]]
        pf, df = piu_vicino(l["lat"], l["lon"], F)
        pu, du = piu_vicino(l["lat"], l["lon"], U)
        pp, dp = piu_vicino(l["lat"], l["lon"], Pset)
        ps, ds = piu_vicino(l["lat"], l["lon"], S)
        coperto_f = df is not None and df <= RAGGIO_COPERTURA
        coperto_u = du is not None and du <= RAGGIO_COPERTURA
        coperto_p = dp is not None and dp <= RAGGIO_COPERTURA
        coperto_fs = coperto_f or (ds is not None and ds <= RAGGIO_COPERTURA)
        conta_f200 += coperto_f
        conta_u200 += coperto_u
        conta_p200 += coperto_p
        conta_fs200 += coperto_fs
        luoghi_critici.append({
            "id_luogo": c["id_luogo"], "nome": l["nome"], "lat": l["lat"], "lon": l["lon"],
            "zona_imq": l["zona_imq"], "n_fermate": l.get("n_fermate"),
            "punteggio": c["punteggio"], "segnali": c["segnali"],
            "parcheggio_f": ({"id": pf["id"], "nome": pf["nome"],
                              "dist_m": round(df) if df <= RAGGIO_F else None}
                             if pf is not None else None),
            "parcheggio_u": ({"id": pu["id"], "nome": pu["nome"], "dist_m": round(du)}
                             if pu is not None else None),
            "coperto_f200": coperto_f, "coperto_u200": coperto_u,
            "coperto_p200": coperto_p,
        })

    controllo = (conta_f200, conta_u200, conta_p200, conta_fs200)
    if controllo != (140, 11, 147, 144):
        sys.exit(f"PASSO E3: FERMO - coperti U/F/P/F+S a 200 m = {controllo}, "
                 f"attesi (140, 11, 147, 144)")
    print(f"coperti a 200 m: F={conta_f200} U={conta_u200} P={conta_p200} F+S={conta_fs200}")

    # --- PASSO E3.3 parcheggi per la mappa ---
    scelti = [p for p in funzione
              if p["classe"] in ("interscambio_di_fatto", "solo_sulla_carta", "potenziale")
              or p["tipo"] == "garage_5t"]
    visti = set()
    parcheggi_mappa = []
    for p in scelti:
        if p["id"] in visti:
            continue
        visti.add(p["id"])
        r = riemp_per_5t.get(id_5t_per_id.get(p["id"])) if id_5t_per_id.get(p["id"]) else None
        parcheggi_mappa.append({
            "id": p["id"], "nome": p["nome"], "tipo": p["tipo"], "classe": p["classe"],
            "motivo": p["motivo"], "lat": round(p["lat"], 5), "lon": round(p["lon"], 5),
            "zona_imq": p["zona_imq"], "zona_centrale": p["zona_centrale"],
            "posti": p["posti"], "posti_origine": posti_origine.get(p["id"], "nessuno"),
            "a_pagamento": p["a_pagamento"], "forza": p["forza"],
            "punti_a_favore": p["punti_a_favore"], "su_asse_ingresso": p["su_asse_ingresso"],
            "firma": r["firma"] if r else None,
            "profilo_feriale": profilo_feriale_24(r),
            "fragile": r.get("fragile") if r else None,
        })

    # --- PASSO E3.4 ufficiali ---
    ufficiali = [{
        "id": p["id"], "nome": p["nome"], "lat": round(p["lat"], 5), "lon": round(p["lon"], 5),
        "posti": p["posti"], "a_pagamento": p["a_pagamento"], "zona_imq": p["zona_imq"],
        "classe": p["classe"], "raggio_m": 200,
    } for p in U]

    # --- PASSO E3.5 zona centrale ---
    geo_per_cod = {g["cod"]: g for g in geo}
    poligoni = []
    for cod in ZONE_CENTRALI:
        g = geo_per_cod[cod]
        geom = poligoni_zona(g["g"]).simplify(0.0002)
        poligoni.append({"cod": cod, "denom": g.get("denom"), "anelli": anelli_da_geometria(geom)})
    zona_centrale = {"zone_centrali": ZONE_CENTRALI, "poligoni": poligoni}

    # --- PASSO E3.6 eventi ---
    eventi_mappa = [{
        "id": e["id"], "nome": e["nome"], "tipo": e["tipo"], "lat": e["lat"], "lon": e["lon"],
        "capienza": e["capienza"], "auto_stimate": e["auto_stimate"],
        "posti_500": e["posti_500"], "posti_1000": e["posti_1000"], "mancano": e["mancano"],
        "fermate_500": e["fermate_500"],
        "corse_ora_sera_feriale": e["corse_ora_sera_feriale"],
        "corse_ora_sera_sabato": e["corse_ora_sera_sabato"],
        "corse_ora_sera_domenica": e["corse_ora_sera_domenica"],
    } for e in eventi["eventi"]]

    # --- PASSO E3.7 riepilogo ---
    from collections import Counter
    per_classe = {}
    for c in ("interscambio_di_fatto", "solo_sulla_carta", "potenziale", "non_interscambio"):
        sel = [p for p in funzione if p["classe"] == c]
        per_classe[c] = {"n": len(sel), "posti": sum(p["posti"] or 0 for p in sel)}
    per_motivo = {}
    for m in sorted({p["motivo"] for p in funzione}):
        sel = [p for p in funzione if p["motivo"] == m]
        per_motivo[m] = {"n": len(sel), "posti": sum(p["posti"] or 0 for p in sel)}
    firme = dict(Counter(r["firma"] for r in riemp["parcheggi"]))
    feriali = sorted({d for r in riemp["parcheggi"] for d in r.get("giorni_validi", [])
                      if datetime.strptime(d, "%Y-%m-%d").weekday() < 5})

    zone_scoperte = []
    for cod, v in sc["per_zona"][SCENARIO].items():
        scoperti = v["critici"] - v["coperti_f200"]
        zone_scoperte.append({
            "zona": cod, "nome": zone_nomi.get(cod, {}).get("denom"),
            "critici": v["critici"], "coperti_f200": v["coperti_f200"], "scoperti": scoperti,
        })
    zone_scoperte.sort(key=lambda z: -z["scoperti"])
    zone_scoperte = zone_scoperte[:10]

    piu_scoperti = [{
        "nome": x["nome"], "zona": x["zona_imq"], "punteggio": x["punteggio"],
        "parcheggio_vicino": x["parcheggio_vicino"],
        "distanza_parcheggio_m": x["distanza_parcheggio_m"],
    } for x in sc["piu_scoperti"][SCENARIO][:10]]

    s_sc = []
    for p in S:
        r = riemp_per_5t.get(id_5t_per_id.get(p["id"])) if id_5t_per_id.get(p["id"]) else None
        s_sc.append({
            "nome": p["nome"], "posti": p["posti"], "a_pagamento": p["a_pagamento"],
            "firma": r["firma"] if r else None,
            "G_giorno_feriale": r.get("G_giorno_feriale") if r else None,
            "N_notte_feriale": r.get("N_notte_feriale") if r else None,
        })

    riepilogo = {
        "scenario": SCENARIO,
        "n_luoghi_critici": s2["n_critici"],
        "copertura_per_raggio": s2["copertura"],
        "parcheggi_per_classe": per_classe,
        "parcheggi_per_motivo": per_motivo,
        "firme_riempimento": firme,
        "giorni_feriali_validi": feriali,
        "zone_scoperte_top10": zone_scoperte,
        "piu_scoperti_top10": piu_scoperti,
        "solo_sulla_carta": s_sc,
        "senza_zona_imq_fuori_universo": len(sc["senza_zona"]),
        "fermate_escluse_fuori_citta_metropolitana": sum(sc["n_fuori_universo"].values()),
    }

    mappa = {
        "generato": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fonti": [
            "data/processed/risultato6_v2/scenari.json",
            "data/processed/risultato6_v2/luoghi.json",
            "data/processed/risultato6_v2/parcheggi.json",
            "data/processed/risultato6_v2/parcheggi_funzione.json",
            "data/processed/risultato6_v2/riempimento.json",
            "data/processed/risultato6_v2/eventi.json",
            "data/processed/imq_zone_geo.json",
        ],
        "etichette": {
            "posti": "posti dichiarati dove ci sono, altrimenti stimati da OpenStreetMap (25 m2 a posto)",
            "firma_riempimento": "da misure 5T [DATI SCARSI] (solo 2 giorni feriali validi)",
            "profilo_feriale": "occupazione media ora per ora, giorno feriale, da 5T [DATI SCARSI]",
            "corse_ora_sera": "orari programmati del trasporto pubblico [PROGRAMMATO]",
            "auto_eventi": "auto stimate = capienza x 50% / 2,5 [STIMATO]",
            "copertura": "luoghi critici con un parcheggio entro 200 m",
        },
        "scenario": scenario,
        "luoghi_critici": luoghi_critici,
        "parcheggi": parcheggi_mappa,
        "ufficiali": ufficiali,
        "zona_centrale": zona_centrale,
        "eventi": eventi_mappa,
        "riepilogo": riepilogo,
    }

    testo = json.dumps(mappa, ensure_ascii=False)
    tolto_punti = False
    if len(testo.encode("utf-8")) > LIMITE_BYTE:
        for p in mappa["parcheggi"]:
            p.pop("punti_a_favore", None)
        testo = json.dumps(mappa, ensure_ascii=False)
        tolto_punti = True
    if len(testo.encode("utf-8")) > LIMITE_BYTE:
        for p in mappa["parcheggi"]:
            if p["profilo_feriale"]:
                p["profilo_feriale"] = [round(v, 1) for v in p["profilo_feriale"]]
        testo = json.dumps(mappa, ensure_ascii=False)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(testo, encoding="utf-8")
    dimensione = OUT.stat().st_size
    if dimensione > LIMITE_BYTE:
        sys.exit(f"PASSO E3: FERMO - mappa_r6.json pesa {dimensione} byte (limite 1,5 MB)")

    # --- rapporto ---
    righe = []
    righe.append("RAPPORTO R6 v2 - DATI PER LA MAPPA E LA SCHEDA (scenario S2)")
    righe.append(f"Generato il {mappa['generato']} da scripts/79_dati_mappa_r6.py.")
    righe.append("")
    righe.append("== Contenuto e quantita' per sezione ==")
    righe.append(f"  scenario: {scenario['id']} '{scenario['titolo']}', segnali {scenario['segnali']}, "
                 f"soglia {scenario['soglia']}, {scenario['n_critici']} luoghi critici, "
                 f"universo {scenario['universo']}")
    righe.append(f"  luoghi_critici: {len(luoghi_critici)}")
    righe.append(f"  parcheggi: {len(parcheggi_mappa)}")
    righe.append(f"  ufficiali: {len(ufficiali)}")
    righe.append(f"  zona_centrale: {len(poligoni)} zone ({', '.join(ZONE_CENTRALI)})")
    righe.append(f"  eventi: {len(eventi_mappa)}"
                 + (f" (manca {', '.join(eventi['mancanti'])})" if eventi.get("mancanti") else ""))
    righe.append("")
    righe.append("== Controlli di copertura a 200 m (devono tornare) ==")
    righe.append(f"  coperto_f200 = {conta_f200} (atteso 140)")
    righe.append(f"  coperto_u200 = {conta_u200} (atteso 11)")
    righe.append(f"  coperto_p200 = {conta_p200} (atteso 147)")
    righe.append(f"  coperto_f200 oppure solo_sulla_carta entro 200 m = {conta_fs200} (atteso 144)")
    righe.append("")
    righe.append("== Copertura per raggio (da scenari.json, gia' calcolata) ==")
    for insieme in ("U", "F", "P", "F+S"):
        v = s2["copertura"][insieme]
        righe.append(f"  {insieme:4s}: 100 m {v['100']:4d} | 200 m {v['200']:4d} | 400 m {v['400']:4d}")
    righe.append("")
    righe.append("== Parcheggi per classe e per motivo ==")
    for c, v in per_classe.items():
        righe.append(f"  {c:22s} {v['n']:5d} parcheggi  {v['posti']:7d} posti")
    for m, v in per_motivo.items():
        righe.append(f"    motivo {m:20s} {v['n']:5d} parcheggi  {v['posti']:7d} posti")
    righe.append("")
    righe.append("== Firme del riempimento 5T [DATI SCARSI] ==")
    for f, n in sorted(firme.items(), key=lambda kv: -kv[1]):
        righe.append(f"  {f:20s} {n:3d} parcheggi")
    righe.append(f"  giorni feriali validi: {', '.join(feriali)}")
    righe.append("")
    righe.append("== Le 10 zone con piu' luoghi critici scoperti (coperti F a 200 m) ==")
    for z in zone_scoperte:
        righe.append(f"  {z['zona']:5s} {str(z['nome']):24s} critici {z['critici']:4d} "
                     f"coperti {z['coperti_f200']:4d} scoperti {z['scoperti']:4d}")
    righe.append("")
    righe.append("== I 10 luoghi piu' scoperti ==")
    for x in piu_scoperti:
        righe.append(f"  {x['punteggio']:6.2f} {x['nome'][:38]:38s} zona {str(x['zona']):5s} "
                     f"piu' vicino: {str(x['parcheggio_vicino'])[:26]:26s} {x['distanza_parcheggio_m']} m")
    righe.append("")
    righe.append("== I 4 parcheggi 'solo sulla carta' ==")
    for x in s_sc:
        righe.append(f"  {x['nome'][:24]:24s} {x['posti']} posti, tariffa {x['a_pagamento']}, "
                     f"firma {x['firma']}, giorno {x['G_giorno_feriale']}, notte {x['N_notte_feriale']}")
    righe.append("")
    righe.append("== Fuori universo ==")
    righe.append(f"  luoghi senza zona IMQ (fuori universo): {riepilogo['senza_zona_imq_fuori_universo']}")
    righe.append(f"  fermate GTT escluse perche' fuori Citta' metropolitana: "
                 f"{riepilogo['fermate_escluse_fuori_citta_metropolitana']}")
    righe.append("")
    righe.append("== Dimensione del file ==")
    righe.append(f"  mappa_r6.json: {dimensione} byte ({dimensione/1024:.0f} KB), "
                 f"limite 1,5 MB; punti_a_favore tolti: {'si' if tolto_punti else 'no'}")
    righe.append("")
    righe.append("== Limiti ==")
    righe.append("- Le distanze sono in linea d'aria, non a piedi.")
    righe.append("- Il riempimento viene da pochi giorni [DATI SCARSI].")
    righe.append("- I posti stimati da OpenStreetMap hanno un errore di circa il 30%.")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT} ({dimensione} byte)")
    print(f"Scritto: {RAPPORTO}")
    print(f"luoghi_critici={len(luoghi_critici)} parcheggi={len(parcheggi_mappa)} "
          f"ufficiali={len(ufficiali)} eventi={len(eventi_mappa)}")


if __name__ == "__main__":
    sys.exit(main())
