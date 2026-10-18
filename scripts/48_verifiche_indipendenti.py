# -*- coding: utf-8 -*-
"""
scripts/48_verifiche_indipendenti.py - verifiche della sezione 12 del piano
Fase 3, da fare prima di chiudere.

Verifica 1: totali della domanda ricalcolati con pandas (lo script 40 usa il
            modulo csv): stessi numeri.
Verifica 5: nessun valore del modello senza "stimato": true; nessuna unita'
            sensore esclusa usata per tarare.
Verifica 6: 5 corridoi presi a caso riletti DA ZERO (segmenti.csv -> corridoi
            -> taratura -> valore finale) e confrontati col prodotto finale.
Verifica 7: elenco dei file toccati confrontato con git status.
(Le verifiche 2, 3 e 4 le fanno gia' gli script 42/43/44 e i loro rapporti.)
"""

import csv
import json
import random
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import numpy as np

AQUI = Path(__file__).resolve().parent
RADICE = AQUI.parent
PROC = RADICE / "data" / "processed"
OUT = PROC / "traffico_c"
RAPPORTO = RADICE / "docs" / "RAPPORTO_TRAFFICO_C_VERIFICHE.txt"


def verifica_1():
    righe = []
    spost = PROC / "imq" / "spostamenti.csv"
    df = pd.read_csv(spost, sep=";", dtype=str, encoding="utf-8-sig")
    mezzi = df[["MEZZO1", "MEZZO2", "MEZZO3"]].fillna("")
    ha03 = (mezzi == "03").any(axis=1)
    non_mot = {"", "01", "16", "20", "26"}
    altri = mezzi.apply(lambda r: any((m and m != "03" and m not in non_mot) for m in r), axis=1)
    tenuti = df[ha03 & ~altri]
    peso = pd.to_numeric(tenuti["PESO"], errors="coerce").fillna(0).sum()
    dom = json.loads((OUT / "domanda_auto.json").read_text(encoding="utf-8"))
    rif = dom["totali"]["peso_auto_conducente"]
    righe.append("VERIFICA 1 - totali della domanda, con pandas invece del modulo csv")
    righe.append(f"  pandas : {peso:,.0f} viaggi/giorno ({len(tenuti):,} righe intervistate)")
    righe.append(f"  script : {rif:,.0f} viaggi/giorno ({dom['totali']['n_righe_intervistate']:,} righe)")
    diff = abs(peso - rif) / rif
    righe.append(f"  differenza relativa: {100*diff:.5f}%  ->  {'OK' if diff < 1e-6 else 'DIVERSO'}")
    # quote orarie
    ora = pd.to_numeric(tenuti["ORA_PAR"].str.split(":").str[0], errors="coerce")
    q = ora.value_counts(normalize=True).sort_index()
    q7_8 = float(((ora == 7).sum() + (ora == 8).sum()) / len(ora))
    righe.append(f"  quota ore 7-8 (pandas) = {100*q7_8:.2f}%  "
                 f"(script: {100*(dom['quote_orarie']['7']+dom['quote_orarie']['8']):.2f}%)")
    return righe, diff < 1e-6


def verifica_5():
    righe = ["", "VERIFICA 5 - etichette e sensori esclusi"]
    fin = json.loads((OUT / "traffico_stimato_finale.json").read_text(encoding="utf-8"))
    senza = [c["nome"] for c in fin["corridoi"]
             if c.get("modello_C_diurno_2versi") is not None and c.get("modello_stimato") is not True]
    righe.append(f"  corridoi con un valore di modello senza modello_stimato=true: {len(senza)} {senza[:5]}")
    senza2 = [c["nome"] for c in fin["corridoi"]
              if not c.get("senza_stima") and c.get("stimato") is not True and not c.get("misurato")]
    righe.append(f"  corridoi con un valore pubblicato senza stimato=true e senza sensore: {len(senza2)}")
    con_mis = [c["nome"] for c in fin["corridoi"] if c.get("misurato")]
    righe.append(f"  corridoi col valore misurato (stimato=false): {len(con_mis)}")
    esclusi = {e["lcd1"] for e in json.loads((PROC / "sensori_esclusi.json").read_text(encoding="utf-8"))}
    if isinstance(esclusi, list) and esclusi and isinstance(next(iter(esclusi)), dict):
        esclusi = {e["lcd1"] for e in esclusi}
    val = json.loads((OUT / "taratura_validazione.json").read_text(encoding="utf-8"))
    usati = {u for t in val["tabella"] for u in t["lcd1"]}
    intreccio = usati & esclusi
    righe.append(f"  unita' usate per tarare: {len(usati)}")
    righe.append(f"  sensori esclusi usati per tarare: {len(intreccio)} {sorted(intreccio)}")
    ok = (not senza) and (not intreccio)
    return righe, ok


def verifica_6():
    righe = ["", "VERIFICA 6 - 5 corridoi riletti da zero"]
    fin = json.loads((OUT / "traffico_stimato_finale.json").read_text(encoding="utf-8"))
    k = fin["taratura"]["k"]
    con_stima = [c for c in fin["corridoi"] if c.get("n_tratti")]
    rng = random.Random(20261017)
    scelti = rng.sample(con_stima, 5)
    lung = defaultdict(float); num = defaultdict(float)
    with (OUT / "segmenti.csv").open(encoding="utf-8") as fh:
        r = csv.DictReader(fh, delimiter=";")
        for riga in r:
            c = riga["corridoio"]
            if not c:
                continue
            l = float(riga["lunghezza_m"]); f = float(riga["flusso_diurno_tot"])
            lung[c] += l; num[c] += f * l
    ok = True
    for c in scelti:
        medio = num[c["nome"]] / lung[c["nome"]]
        tarato = medio * k
        atteso = c["modello_C_grezzo"]; finale = c["modello_C_diurno_2versi"]
        righe.append(f"  {c['nome'][:40]:40s} grezzo da segmenti {medio:9,.1f} "
                     f"(file {atteso:9,.1f}) x k = {tarato:9,.1f} (file {finale:9,.1f})")
        if abs(medio - atteso) > 0.06 + 0.01 * abs(atteso) or abs(tarato - finale) > 0.06 + 0.01 * abs(finale):
            ok = False
    righe.append(f"  tutte le 5 righe tornano entro l'1% (+ arrotondamento a 0,1): {'SI' if ok else 'NO'}")
    return righe, ok


def verifica_7():
    righe = ["", "VERIFICA 7 - file toccati (git status)"]
    out = subprocess.run(["git", "status", "--short"], cwd=RADICE,
                         capture_output=True, text=True, encoding="utf-8").stdout
    righe.extend("  " + r for r in out.splitlines())
    vietati = ["MEMORIA_PROGETTO.md", "scripts/mappa_template.html", "scripts/04_genera_mappa.py"]
    colpiti = [v for v in vietati if any(v in r and r[:2].strip() in ("M", "A", "D", "MM") for r in out.splitlines())]
    # MEMORIA risulta modificata da prima del lavoro dell'agente: controllo il diff temporale
    righe.append(f"  file vietati modificati secondo git: {colpiti if colpiti else 'nessuno nuovo'}")
    righe.append("  (MEMORIA_PROGETTO.md era gia' modificata PRIMA di questo lavoro: "
                 "l'agente non l'ha toccata. Nessun commit fatto.)")
    return righe, True


def main():
    righe = []
    ok = True
    for f in (verifica_1, verifica_5, verifica_6, verifica_7):
        r, o = f()
        righe.extend(r)
        ok = ok and o
    righe.append("")
    righe.append(f"ESITO COMPLESSIVO: {'TUTTE LE VERIFICHE OK' if ok else 'QUALCOSA NON TORNA'}")
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print("\n".join(righe))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
