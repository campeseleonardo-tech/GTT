#!/usr/bin/env python3
"""89 - Proposta di regola fissa per le "fermate importanti" (lavoro 5). SOLO LETTURA.

Non cambia lo script 83 ne' i risultati: scrive solo docs/RAPPORTO_R6_PROPOSTA_FERMATE.txt. Sceglie Leo N e M.

Universo: gli stessi luoghi eleggibili dello script 83 (Citta' metropolitana fuori da Q001-Q009).
Segnali, come li legge lo script 83: b2 (corse/ora, media ore 6-10 e 16-20 di un feriale) da segnali.json;
c4 (auto in entrata che passano accanto) da auto_passaggio.json. Metro / stazione (ferro) / capolinea da nodi.json
(il capolinea vale gia' solo con almeno 4 corse/ora fra le 6 e le 9, script 72).
Regola: (metro o stazione o capolinea, OPPURE b2 >= N) E c4 >= M.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comuni  # noqa: E402

RADICE = comuni.RADICE
P = RADICE / "data" / "processed" / "risultato6_v2"
LUOGHI, SEGNALI, PASSAGGIO = P / "luoghi.json", P / "segnali.json", P / "auto_passaggio.json"
NODI, IMPORTANTI, MAPPA = P / "nodi.json", P / "fermate_importanti.json", P / "mappa_r6.json"
ZONE = RADICE / "data" / "processed" / "imq_zone.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6_PROPOSTA_FERMATE.txt"
GRIGLIA_N = (10, 15, 20, 30)
GRIGLIA_M = (500, 1000, 2000, 3000)
PERC = (10, 25, 50, 75, 90, 95, 99)
RAGGIO_PUNTO_M = 3000.0   # le fermate di un punto prioritario sono indicate per nome: si collegano ai luoghi cosi'
CENTRO_LAT, CENTRO_LON = 45.0703, 7.6869   # piazza Castello (nord-ovest = lat > e lon <)


def pr(v):
    return "  ".join(f"p{p}={np.percentile(v, p):.1f}" for p in PERC) + f"  max={max(v):.1f}"


def main():
    c = comuni.Controlli()
    for f in (LUOGHI, SEGNALI, PASSAGGIO, NODI, IMPORTANTI, MAPPA, ZONE):
        c(f"esiste {f.name}", f.exists(), bloccante=True)

    def rd(f):
        return json.loads(f.read_text(encoding="utf-8"))
    luoghi = {l["id_luogo"]: l for l in rd(LUOGHI)["luoghi"]}
    seg = {s["id_luogo"]: s for s in rd(SEGNALI)["luoghi"]}
    pas = rd(PASSAGGIO)["luoghi"]
    nodi = {n["id_luogo"]: n for n in rd(NODI)["luoghi"]}
    macro = {z["cod"]: z["macro"] for z in rd(ZONE)}
    oggi = rd(IMPORTANTI)
    imp_oggi = {x["id_luogo"] for x in oggi["importanti"]}
    punti = rd(MAPPA)["punti_prioritari"]

    eleg = [i for i, l in luoghi.items() if l.get("zona_imq") and macro.get(l["zona_imq"]) in comuni.MACRO_UNIVERSO
            and l["zona_imq"] not in comuni.ZONE_CENTRALI]
    c("eleggibili = quelli dello script 83", len(eleg) == oggi["n_eleggibili"], bloccante=True,
      dettaglio=f"{len(eleg)} vs {oggi['n_eleggibili']}")
    c("le importanti di oggi sono tutte fra gli eleggibili", imp_oggi <= set(eleg), bloccante=True)
    c("nodi.json copre tutti gli eleggibili", all(i in nodi for i in eleg),
      dettaglio=f"{sum(i not in nodi for i in eleg)} mancanti")

    b2 = {i: (seg.get(i, {}).get("b2") or 0.0) for i in eleg}
    c4 = {i: (pas.get(i) or {}).get("c4", 0) or 0 for i in eleg}
    c("nessun valore negativo", min(b2.values()) >= 0 and min(c4.values()) >= 0, bloccante=True)
    metro = {i: bool(nodi.get(i, {}).get("metro")) for i in eleg}
    ferro = {i: bool(nodi.get(i, {}).get("ferro")) for i in eleg}
    capo = {i: bool(nodi.get(i, {}).get("capolinea")) for i in eleg}
    nodo = {i: metro[i] or ferro[i] or capo[i] for i in eleg}
    nome_gruppo = {"01 Torino": "Torino", "02 Cintura": "cintura", "03 Resto CMTO": "resto CMTO"}
    gr = {i: nome_gruppo[macro[luoghi[i]["zona_imq"]]] for i in eleg}
    cg = Counter(gr.values())

    def nord_ovest(i):
        return luoghi[i]["lat"] > CENTRO_LAT and luoghi[i]["lon"] < CENTRO_LON

    r = ["RAPPORTO R6 - PROPOSTA PER LE FERMATE IMPORTANTI CON REGOLA FISSA (script 89, solo lettura)", "",
         f"Eleggibili {len(eleg)} (Torino fuori da Q001-Q009 {cg['Torino']}, cintura {cg['cintura']}, "
         f"resto CMTO {cg['resto CMTO']}).",
         f"Fermate importanti oggi (script 83, punteggio, 10%): {len(imp_oggi)}. Punti prioritari oggi: {len(punti)}.",
         "Regola proposta: (metro o stazione o capolinea, oppure corse/ora b2 >= N) e auto che passano c4 >= M.", "",
         "== Distribuzioni sugli eleggibili ==",
         "corse/ora pendolari b2 (media ore 6-10 e 16-20 feriale):", "  tutti:    " + pr(list(b2.values())),
         f"  solo > 0: " + pr([v for v in b2.values() if v > 0]) + f"  ({sum(v > 0 for v in b2.values())} fermate)",
         "auto in entrata che passano accanto c4:", "  tutti:    " + pr(list(c4.values())),
         "  solo > 0: " + pr([v for v in c4.values() if v > 0]) + f"  ({sum(v > 0 for v in c4.values())} fermate)",
         f"metro: {sum(metro.values())}; stazione (ferro entro 300 m): {sum(ferro.values())}; "
         f"capolinea: {sum(capo.values())}; almeno uno dei tre: {sum(nodo.values())} "
         f"(fra le importanti di oggi: {sum(nodo[i] for i in imp_oggi)} su {len(imp_oggi)})",
         "Importanti di oggi:", "  b2: " + pr([b2[i] for i in imp_oggi]), "  c4: " + pr([c4[i] for i in imp_oggi]), ""]

    def nome_corto(n):   # come lo script 84 (via 80): "Fermata 6181 - PESSIONE CAP" -> "PESSIONE CAP"
        return re.sub(r"^Fermata \d+\s*-\s*", "", n or "").strip()

    # i punti prioritari indicano le fermate per nome: si collegano ai luoghi vicini al loro centro
    def luoghi_del_punto(pt):
        nomi = {f["nome"] for f in pt["fermate"]}
        la, lo = pt["centro"]
        return {i for i in eleg if nome_corto(luoghi[i]["nome"]) in nomi
                and comuni.haversine_m(la, lo, luoghi[i]["lat"], luoghi[i]["lon"]) <= RAGGIO_PUNTO_M}
    coll = [luoghi_del_punto(pt) for pt in punti]
    ok_oggi = sum(1 for s in coll if s & imp_oggi)
    c("ogni punto prioritario di oggi ha una fermata fra le importanti di oggi (il collegamento per nome funziona)",
      ok_oggi == len(punti), dettaglio=f"{ok_oggi} su {len(punti)}")

    nw_oggi = sum(nord_ovest(i) for i in imp_oggi)
    r += ["== Griglia N (corse/ora) x M (auto che passano) ==",
          f"Importanti di oggi a nord-ovest (lat > 45,0703 e lon < 7,6869): {nw_oggi} su {len(imp_oggi)}", "",
          f"{'N':>3} {'M':>5} | {'tot':>5} {'Torino':>6} {'cint.':>5} {'resto':>5} | {'restano':>7} {'nuove':>5} "
          f"{'nuove NO':>8} {'tot NO':>6} | punti prioritari con >=1 fermata"]
    for N in GRIGLIA_N:
        for M in GRIGLIA_M:
            nuova = {i for i in eleg if (nodo[i] or b2[i] >= N) and c4[i] >= M}
            cnt = Counter(gr[i] for i in nuova)
            nuove = nuova - imp_oggi
            r.append(f"{N:>3} {M:>5} | {len(nuova):>5} {cnt['Torino']:>6} {cnt['cintura']:>5} {cnt['resto CMTO']:>5} | "
                     f"{len(nuova & imp_oggi):>7} {len(nuove):>5} {sum(nord_ovest(i) for i in nuove):>8} "
                     f"{sum(nord_ovest(i) for i in nuova):>6} | {sum(1 for s in coll if s & nuova):>2} su {len(punti)}")
        r.append("")
    r += ["Colonne: tot = fermate importanti con la regola (Torino / cintura / resto della Citta' metropolitana);",
          "restano = delle importanti di oggi, quante ci sono ancora; nuove = non erano importanti oggi;",
          "nuove NO = fra le nuove, quelle a nord-ovest di piazza Castello; tot NO = tutte quelle a nord-ovest;",
          "punti prioritari = quelli di oggi (mappa_r6.json) con almeno una loro fermata nella lista.",
          f"Un punto prioritario e' collegato alle fermate per nome, a meno di {RAGGIO_PUNTO_M / 1000:.0f} km dal suo centro.",
          "", "== Controlli ==", *("  " + x for x in c.righe)]
    RAPPORTO.write_text("\n".join(r) + "\n", encoding="utf-8")
    print("\n".join(r))
    print(f"\nScritto {RAPPORTO.relative_to(RADICE)}; avvisi: {len(c.avvisi())}")


if __name__ == "__main__":
    main()
