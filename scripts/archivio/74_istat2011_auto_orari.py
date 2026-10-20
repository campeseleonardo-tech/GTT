#!/usr/bin/env python3
"""
74_istat2011_auto_orari.py  -  Risultato 6 v2, PASSO 7: proporzioni ISTAT 2011.

Cosa fa
-------
Dal censimento ISTAT 2011 prende solo PROPORZIONI stabili: quanta parte di chi va a
Torino per lavoro o studio usa l'auto, e a che ora esce di casa. Servono per completare
l'indagine IMQ 2022 nelle zone dove ci sono poche interviste. Non si usano MAI i numeri
assoluti del 2011.

Cosa legge
----------
  data/raw/istat/2011_sezioni/nazionale/matrix_pendo2011_10112014.txt  (riga per riga, ~307 MB)
  data/processed/imq/comuni.csv              (comune ISTAT -> zona IMQ)
  data/processed/imq/spostamenti.csv         (microdati IMQ 2022)
  data/processed/risultato6_v2/segnali.json  (c2 e le zone con poche interviste)

Cosa scrive
-----------
  data/processed/risultato6_v2/istat2011_proporzioni.json
  docs/RAPPORTO_R6V2_ISTAT2011.txt

Come si lancia
--------------
  python scripts\\74_istat2011_auto_orari.py
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
ISTAT = RADICE / "data" / "raw" / "istat" / "2011_sezioni" / "nazionale" / "matrix_pendo2011_10112014.txt"
COMUNI = RADICE / "data" / "processed" / "imq" / "comuni.csv"
SPOSTAMENTI = RADICE / "data" / "processed" / "imq" / "spostamenti.csv"
SEGNALI = RADICE / "data" / "processed" / "risultato6_v2" / "segnali.json"
OUT = RADICE / "data" / "processed" / "risultato6_v2" / "istat2011_proporzioni.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_ISTAT2011.txt"

PROV_TORINO = "001"
COM_TORINO = "272"
MEZZI_AUTO = ("07", "08")
MIN_INTERVISTE = 30


def peso(x):
    v = (x.get("PESO") or "").replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return 0.0


def minuti(orario):
    if not orario:
        return None
    try:
        h, m = orario.strip().split(":")
        return int(h) * 60 + int(m)
    except ValueError:
        return None


def leggi_istat():
    """Ritorna (per_comune, per_mezzo_lavoro, righe_lette, righe_usate)."""
    per_comune = defaultdict(lambda: {"persone": 0.0, "auto": 0.0, "orari": [0.0, 0.0, 0.0, 0.0]})
    per_mezzo_lavoro = defaultdict(float)
    lette = 0
    usate = 0
    with ISTAT.open(encoding="latin-1") as f:
        for riga in f:
            lette += 1
            if lette % 1000000 == 0:
                print(f"  ... {lette} righe lette, {usate} usate")
            if not riga.startswith("L "):
                continue
            p = riga.split()
            if len(p) < 15:
                continue
            if p[2] != PROV_TORINO or p[7] != PROV_TORINO or p[8] != COM_TORINO:
                continue
            if p[3] == COM_TORINO:
                continue
            try:
                persone = float(p[13])
            except ValueError:
                continue
            if persone <= 0:
                continue
            usate += 1
            pro_com = int(p[2]) * 1000 + int(p[3])
            c = per_comune[pro_com]
            c["persone"] += persone
            if p[10] in MEZZI_AUTO:
                c["auto"] += persone
            if p[11] in ("1", "2", "3", "4"):
                c["orari"][int(p[11]) - 1] += persone
            if p[5] == "2":
                per_mezzo_lavoro[p[10]] += persone
    return per_comune, per_mezzo_lavoro, lette, usate


def imq_per_zona():
    """Quota auto IMQ 2022 per zona, sullo stesso universo di c2 (ore 6-10, verso Torino),
    e base di spostamenti tutti i mezzi per il completamento."""
    base = defaultdict(float)
    auto = defaultdict(float)
    interviste = defaultdict(int)
    with SPOSTAMENTI.open(encoding="utf-8-sig") as f:
        for x in csv.DictReader(f, delimiter=";"):
            par = x["COD_PAR"].strip()
            arr = x["COD_ARR"].strip()
            if not par or par.startswith("Q") or not arr.startswith("Q"):
                continue
            mp = minuti(x["ORA_PAR"])
            if mp is None or not (360 <= mp <= 599):
                continue
            p = peso(x)
            for z in (par, arr):
                base[z] += p
                interviste[z] += 1
                if x["MEZZO1"] in ("03", "04", "21"):
                    auto[z] += p
    return base, auto, interviste


def main():
    for p in (ISTAT, COMUNI, SPOSTAMENTI, SEGNALI):
        if not p.exists():
            sys.exit(f"Manca: {p}")

    print("leggo la matrice ISTAT 2011 (riga per riga)...")
    per_comune, per_mezzo_lavoro, lette, usate = leggi_istat()
    print(f"  righe lette: {lette}; righe usate (cintura -> Torino): {usate}")
    print(f"  comuni di residenza con dati: {len(per_comune)}")

    # controllo codici: chi va a Torino per lavoro deve usare soprattutto l'auto (07)
    primo = max(per_mezzo_lavoro.items(), key=lambda kv: kv[1])
    print("  mezzi per lavoro (persone):", {k: round(v) for k, v in
                                           sorted(per_mezzo_lavoro.items(), key=lambda kv: -kv[1])})
    if primo[0] != "07":
        sys.exit(f"Controllo codici FALLITO: il mezzo piu' usato per lavoro non e' 07 ma "
                 f"'{primo[0]}'. Probabili codici o colonne sbagliati — FERMO.")

    comuni = {}
    with COMUNI.open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            try:
                pro_com = int(r["COD1_ISTAT"])
            except ValueError:
                continue
            comuni[pro_com] = {"zona": r["COD2"], "nome": r["DESCRIZIONE"]}

    zone = defaultdict(lambda: {"persone": 0.0, "auto": 0.0, "orari": [0.0, 0.0, 0.0, 0.0],
                                "comuni": []})
    fuori = 0
    for pro_com, c in per_comune.items():
        info = comuni.get(pro_com)
        if not info:
            fuori += 1
            continue
        z = zone[info["zona"]]
        z["persone"] += c["persone"]
        z["auto"] += c["auto"]
        for i in range(4):
            z["orari"][i] += c["orari"][i]
        z["comuni"].append(info["nome"])
    print(f"  comuni senza zona IMQ (fuori dalla Citta' metropolitana nei dati IMQ): {fuori}")

    base_imq, auto_imq, interviste = imq_per_zona()
    segnali = json.loads(SEGNALI.read_text(encoding="utf-8"))
    per_zona_segnali = {}
    for s in segnali["luoghi"]:
        z = s["zona_imq"]
        if z:
            per_zona_segnali[z] = {"c2": s["c2"], "c2_ztl": s["c2_ztl"],
                                   "c2_scarso": s["c2_scarso"]}

    esito_zone = {}
    completate = []
    for z, v in zone.items():
        quota_auto = v["auto"] / v["persone"] if v["persone"] else None
        tot_orari = sum(v["orari"])
        quota_orari = {str(i + 1): (round(v["orari"][i] / tot_orari, 3) if tot_orari else None)
                       for i in range(4)}
        q_imq = (auto_imq[z] / base_imq[z]) if base_imq.get(z) else None
        info = per_zona_segnali.get(z, {})
        scarso = bool(info.get("c2_scarso"))
        c2_completo = None
        if scarso and quota_auto is not None and base_imq.get(z):
            c2_completo = base_imq[z] * quota_auto
            completate.append(z)
        esito_zone[z] = {
            "quota_auto_2011": round(quota_auto, 4) if quota_auto is not None else None,
            "quota_orari_2011": quota_orari,
            "persone_2011_stima": round(v["persone"]),
            "n_comuni": len(v["comuni"]),
            "quota_auto_imq_2022": round(q_imq, 4) if q_imq is not None else None,
            "interviste_imq_mattino": interviste.get(z, 0),
            "c2_scarso": scarso,
            "c2_attuale": info.get("c2"),
            "c2_completo": round(c2_completo, 1) if c2_completo is not None else None,
            "differenza": (round(quota_auto - q_imq, 4)
                           if quota_auto is not None and q_imq is not None else None),
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "nota": "Solo proporzioni. Nessun numero assoluto del 2011 e' usato nei punteggi.",
        "blocchi": "le persone 2011 sono solo pesi per fare le medie per zona",
        "zone": esito_zone,
        "zone_completate": sorted(completate),
    }, ensure_ascii=False), encoding="utf-8")

    righe = []
    righe.append("RAPPORTO R6 v2 — ISTAT 2011: PROPORZIONI PER COMPLETARE L'IMQ (Passo 7)")
    righe.append("Dal 2011 si usano solo proporzioni (quota di chi va in auto, orari), mai numeri.")
    righe.append("")
    righe.append(f"righe lette: {lette}; spostamenti cintura -> Torino usati: {usate}")
    righe.append(f"comuni di residenza: {len(per_comune)}; zone IMQ collegate: {len(zone)}")
    righe.append("CONTROLLO codici: fra chi va a Torino per lavoro il mezzo piu' frequente e' "
                 f"il codice {primo[0]} (auto come conducente) — OK")
    righe.append("")
    righe.append("== Per zona: quota auto 2011, quota auto IMQ 2022, differenza ==")
    righe.append("  zona | comuni | quota auto 2011 | quota auto IMQ 2022 | differenza | interviste mattino")
    for z in sorted(esito_zone):
        e = esito_zone[z]
        def pct(v):
            return f"{100 * v:5.1f}%" if v is not None else "  n.d."
        righe.append(f"  {z:6s} {e['n_comuni']:4d}   {pct(e['quota_auto_2011']):>7} "
                     f"{pct(e['quota_auto_imq_2022']):>9} {pct(e['differenza']):>9} "
                     f"{e['interviste_imq_mattino']:6d}")
    righe.append("")
    righe.append("== Zone con poche interviste, completate con le proporzioni 2011 ==")
    if completate:
        for z in sorted(completate):
            e = esito_zone[z]
            righe.append(f"  {z}: c2 attuale {e['c2_attuale']} -> c2 completo {e['c2_completo']} "
                         f"(quota auto 2011 {100 * e['quota_auto_2011']:.1f}%)")
    else:
        righe.append("  nessuna")
    righe.append("")
    righe.append("== Orari di uscita 2011 per zona (solo proporzioni) ==")
    righe.append("  1 = prima delle 7:15, 2 = 7:15-8:14, 3 = 8:15-9:14, 4 = dopo le 9:14")
    for z in sorted(esito_zone):
        o = esito_zone[z]["quota_orari_2011"]
        def p(v):
            return f"{100 * v:4.0f}" if v is not None else "   -"
        righe.append(f"  {z:6s} {p(o['1'])} {p(o['2'])} {p(o['3'])} {p(o['4'])}")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print(f"Scritto: {OUT}")
    print(f"Scritto: {RAPPORTO}")
    print(f"zone completate: {len(completate)}")


if __name__ == "__main__":
    sys.exit(main())
