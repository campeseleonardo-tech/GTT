# -*- coding: utf-8 -*-
"""
scripts/21_risultato1_vuoti.py - Risultato 1, fase A: dove mancano i servizi essenziali
(sola lettura di data/processed/accessibilita.json, nessun nuovo calcolo R5)

Domanda: quanti residenti NON hanno un servizio essenziale raggiungibile in 15 min a
piedi, e dove. Cinque gruppi trattati separatamente (nessun indice unico inventato):
scuole, salute, cibo, fermate, verde.

Due livelli di carenza per sezione, scelti con Leo il 12/10:
  zero       = il gruppo conta 0 destinazioni entro 15 min a piedi
               (coerente con la "citta' dei 15 minuti": zero accesso)
  pochissimo = sopra zero ma sotto il 10 percento piu' basso (--percentile)
               della distribuzione, pesata per residenti

Torino e cintura sono SEMPRE riportate separatamente per ogni gruppo (stesso
principio del rapporto di accessibilita'): confrontare "quanti residenti a
Torino" fra gruppi diversi deve sempre usare lo stesso ambito, altrimenti il
confronto e' falso (bug trovato e corretto il 12/10: la prima versione
confrontava fermate/verde calcolati su Torino+cintura con scuole/salute/cibo
calcolati solo su Torino).

Scelta dichiarata sull'ambito del PERCENTILE "pochissimo" (riguarda solo dove
si fissa la soglia, non dove si contano i residenti sotto soglia): per
scuole/salute/cibo il catalogo esiste solo dentro Torino (comune 1272); la
soglia si calcola quindi solo sulle sezioni di Torino. Per fermate e verde
(stessa fonte ovunque: GTFS e OSM) la soglia si calcola su tutte le 8.317
sezioni. In cintura, scuole/salute/cibo restano inoltre segnalati come "dato
non comparabile" (il catalogo comunale non c'e': zero e' spesso mancanza di
dato, non vero vuoto di servizio).

Uscite:
  data/processed/risultato1_vuoti.json  (soglie, numeri per gruppo e ambito,
                                          sezioni peggiori a Torino, flag
                                          "manca" per sezione per uso in mappa)
  docs/RAPPORTO_RISULTATO1.txt          (i 3 numeri di testa + dettaglio)

Usage:
    python 21_risultato1_vuoti.py [--percentile 10]
"""

import argparse
import datetime as dt
import json
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
ACCESS = RADICE / "data/processed/accessibilita.json"
OUT = RADICE / "data/processed/risultato1_vuoti.json"
RAPPORTO = RADICE / "docs/RAPPORTO_RISULTATO1.txt"

GRUPPI = ["scuole", "salute", "cibo", "fermate", "verde"]
SOLO_TORINO_PERCENTILE = {"scuole", "salute", "cibo"}  # dove si fissa la soglia "pochissimo"
NON_COMPARABILE_CINTURA = {"scuole", "salute", "cibo"}  # catalogo assente in cintura
COMUNE_TORINO_PREFIX = "1272"


def e_torino(sid):
    return str(sid).startswith(COMUNE_TORINO_PREFIX)


def percentile_pesato(coppie, p):
    """Valore sotto cui sta il p-esimo percento dei residenti (coppie pesate).
    coppie = [(valore, residenti)]. Ritorna la soglia (valore massimo incluso
    nella fascia "pochissimo"), o None se non calcolabile."""
    coppie = sorted((v, w) for v, w in coppie if w and w > 0)
    tot = sum(w for _, w in coppie)
    if tot <= 0:
        return None
    cum = 0.0
    for v, w in coppie:
        cum += w
        if cum / tot * 100.0 >= p:
            return v
    return coppie[-1][0] if coppie else None


def conta(sottoinsieme, g, soglia):
    """Residenti/sezioni a 'zero' e a 'pochissimo' (0 < v <= soglia) in un sottoinsieme."""
    res_zero = sez_zero = res_poco = sez_poco = 0
    for s in sottoinsieme:
        v = s["piedi"]["15"].get(g, 0)
        if v == 0:
            res_zero += s["res"]; sez_zero += 1
        elif soglia is not None and v <= soglia:
            res_poco += s["res"]; sez_poco += 1
    tot = sum(s["res"] for s in sottoinsieme)
    pct = lambda r: round(100.0 * r / tot, 1) if tot else None
    return {
        "residenti_totali_ambito": tot,
        "zero": {"residenti": res_zero, "sezioni": sez_zero, "quota_residenti": pct(res_zero)},
        "pochissimo": {"residenti": res_poco, "sezioni": sez_poco, "quota_residenti": pct(res_poco)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--percentile", type=float, default=10.0,
                     help="soglia della fascia 'pochissimo', in percento di residenti (default 10)")
    args = ap.parse_args()
    p = args.percentile

    access = json.loads(ACCESS.read_text(encoding="utf-8"))
    sezioni = access["sezioni"]
    taglio = access["parametri"]["cutoff_piedi_min"]
    print(f"Sezioni: {len(sezioni)}  cutoff a piedi: {taglio} min")

    torino = [s for s in sezioni if e_torino(s["id"])]
    cintura = [s for s in sezioni if not e_torino(s["id"])]
    print(f"Torino: {len(torino)}  cintura: {len(cintura)}")

    gruppi_esito = {}
    per_sezione_manca = {s["id"]: {} for s in sezioni}

    for g in GRUPPI:
        ambito_soglia = torino if g in SOLO_TORINO_PERCENTILE else sezioni
        soglia = percentile_pesato(
            [(s["piedi"]["15"].get(g, 0), s["res"]) for s in ambito_soglia], p)

        # il flag per-sezione (per la mappa) usa sempre la stessa soglia, su tutte le sezioni
        for s in sezioni:
            v = s["piedi"]["15"].get(g, 0)
            if v == 0:
                per_sezione_manca[s["id"]][g] = "zero"
            elif soglia is not None and v <= soglia:
                per_sezione_manca[s["id"]][g] = "pochissimo"

        peggiori_torino = sorted(
            [s for s in torino if s["piedi"]["15"].get(g, 0) == 0],
            key=lambda s: -s["res"])[:15]

        gruppi_esito[g] = {
            "ambito_percentile": "torino" if g in SOLO_TORINO_PERCENTILE else "torino+cintura",
            "soglia_pochissimo": soglia,
            "torino": conta(torino, g, soglia),
            "cintura": conta(cintura, g, soglia),
            "cintura_comparabile": g not in NON_COMPARABILE_CINTURA,
            "sezioni_peggiori_zero_torino": [
                {"id": s["id"], "res": s["res"], "lat": s["lat"], "lon": s["lon"]}
                for s in peggiori_torino],
        }
        if g in NON_COMPARABILE_CINTURA:
            gruppi_esito[g]["nota_cintura"] = (
                "catalogo comunale solo per Torino: in cintura 'zero'/'pochissimo' e' quasi "
                "sempre mancanza di dato, non assenza di servizio. Numeri riportati ma NON "
                "comparabili con Torino.")

    # 3 numeri di testa: tutti calcolati SOLO su Torino, confrontabili tra loro.
    res_torino_tot = sum(s["res"] for s in torino)
    almeno_uno_zero_torino = sum(
        s["res"] for s in torino if any(s["piedi"]["15"].get(g, 0) == 0 for g in GRUPPI))
    gruppo_peggiore = max(GRUPPI, key=lambda g: gruppi_esito[g]["torino"]["zero"]["residenti"])

    esito = {
        "generato": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "fonte": "data/processed/accessibilita.json (giro completo 12/10/2026, [STIMATO])",
        "percentile_pochissimo": p,
        "nota_ambito_percentile": ("La SOGLIA 'pochissimo' per scuole/salute/cibo e' fissata solo "
                         "su Torino (catalogo comunale); per fermate/verde su Torino+cintura "
                         "(fonte uniforme). I CONTEGGI di residenti/sezioni sotto soglia sono "
                         "invece sempre riportati separati per Torino e cintura, per ogni gruppo."),
        "numeri_di_testa": {
            "residenti_torino": res_torino_tot,
            "residenti_torino_senza_almeno_un_servizio_essenziale_a_zero": almeno_uno_zero_torino,
            "quota_residenti_torino": round(100.0 * almeno_uno_zero_torino / res_torino_tot, 1) if res_torino_tot else None,
            "gruppo_piu_carente_a_torino": gruppo_peggiore,
        },
        "gruppi": gruppi_esito,
        "sezioni_manca": [
            {"id": sid, "manca": v} for sid, v in per_sezione_manca.items() if v],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(esito, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Scritto {OUT} ({OUT.stat().st_size/1e3:.0f} KB)")

    # ---- rapporto leggibile
    righe = [
        "RAPPORTO RISULTATO 1 - fase A: dove mancano i servizi essenziali (STIMATO, a piedi)",
        f"generato: {esito['generato']}",
        f"fonte: {esito['fonte']}",
        f"cutoff a piedi: {taglio} min   soglia 'pochissimo': sotto il {p:.0f}% dei residenti",
        "",
        "I 3 NUMERI (tutti su Torino, confrontabili tra loro):",
        f"  1) Residenti a Torino SENZA ALMENO UN servizio essenziale entro {taglio} min a piedi: "
        f"{almeno_uno_zero_torino:,} su {res_torino_tot:,} ({esito['numeri_di_testa']['quota_residenti_torino']}%)",
        f"  2) Gruppo piu' carente a Torino (piu' residenti a zero, a Torino): {gruppo_peggiore}",
        f"  3) Vedi dettaglio: la cintura ha percentuali di 'zero' molto piu' alte, ma per "
        f"scuole/salute/cibo NON sono comparabili con Torino (manca il catalogo, non il servizio)",
        "",
        "DETTAGLIO PER GRUPPO (Torino e cintura sempre separate):",
    ]
    for g in GRUPPI:
        d = gruppi_esito[g]
        righe.append(f"  {g}  (soglia 'pochissimo' = {d['soglia_pochissimo']}, "
                      f"fissata su: {d['ambito_percentile']}):")
        t = d["torino"]
        righe.append(f"    Torino:   zero {t['zero']['residenti']:,} res / {t['zero']['sezioni']} sez "
                      f"({t['zero']['quota_residenti']}%)   pochissimo {t['pochissimo']['residenti']:,} res / "
                      f"{t['pochissimo']['sezioni']} sez ({t['pochissimo']['quota_residenti']}%)")
        c = d["cintura"]
        etichetta = "cintura" if d["cintura_comparabile"] else "cintura (NON comparabile)"
        righe.append(f"    {etichetta}: zero {c['zero']['residenti']:,} res / {c['zero']['sezioni']} sez "
                      f"({c['zero']['quota_residenti']}%)   pochissimo {c['pochissimo']['residenti']:,} res / "
                      f"{c['pochissimo']['sezioni']} sez ({c['pochissimo']['quota_residenti']}%)")
        if "nota_cintura" in d:
            righe.append(f"      -> {d['nota_cintura']}")
    righe += [
        "",
        "LIMITI: ORARIO PROGRAMMATO [STIMATO] (nessun ritardo/capienza/domanda reale); "
        "il gruppo 'cibo' usa tutte le attivita' del catalogo senza distinguere categoria; "
        "cintura su scuole/salute/cibo non comparabile con Torino (fonte diversa); "
        "le soglie DM 1444/1968 non sono state applicate qui (sono standard di superficie per "
        "comune, non di raggiungibilita' a piedi per sezione): citate come riferimento nella "
        "scheda finale, non calcolate.",
    ]
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe), encoding="utf-8")
    print(f"Scritto {RAPPORTO}")


if __name__ == "__main__":
    main()
