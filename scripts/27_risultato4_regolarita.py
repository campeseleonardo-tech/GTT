#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Risultato 4 — Bus in ritardo e bus irregolari [MISURATO].

Domanda
-------
1. Puntualità: quanti passaggi dei mezzi GTT alle fermate arrivano con **più di 5 minuti**
   di ritardo? Su quali linee e a che ora va peggio?
2. Regolarità: sulle linee frequenti, quante volte i mezzi arrivano **a grappolo** (due
   attaccati) o lasciano un **buco** (attesa molto più lunga del previsto)?

Decisioni (D1-D9, non modificabili)
-----------------------------------
D1 passaggio = per ogni (trip_id, start_date, seq) si tiene solo l'ultima lettura
   (la letto_utc più recente) in cui quella seq compare;
D2 ritardo = arr.delay/60 minuti; se arr ha "time": (time - orario_programmato)/60, con
   orario programmato = mezzanotte locale di start_date + arrival_time GTFS, in UTC;
D3 scarto se |arrivo stimato - letto_utc| > 10 min, o se corsa/seq non è nel GTFS;
D4 classi: anticipo se < -1 min; puntuale se -1..+5; in ritardo se > +5;
D5 arrivo stimato = orario programmato + ritardo;
D6 regolarità solo su coppie con intervallo programmato <= 15 minuti;
D7 grappolo se osservato < 0,5 x programmato; buco se > 2 x programmato; altrimenti
   regolare;
D8 linea in classifica solo con >= 200 passaggi (puntualità, nel tipo di giorno) o
   >= 100 coppie (regolarità);
D9 fasce: punta_mattina 7-9, giorno 9-16, punta_sera 16-19, sera 19-24, notte 0-7
   (ora locale dell'arrivo programmato).

Input (sola lettura)
--------------------
data/storico_backup.sqlite  -> tabella trip_update_gtt (letto_utc, trip_id, start_date,
                               payload JSON con stu[].arr.delay o stu[].arr.time);
data/raw/gtt_gtfs_20261003_224530.zip -> trips.txt, routes.txt, stop_times.txt.

Output
------
data/processed/risultato4_regolarita.json
docs/RAPPORTO_RISULTATO4.txt

Uso
---
python scripts/27_risultato4_regolarita.py [--prova]
--prova = solo start_date 20261013, rapporto a schermo, nessun file scritto.
"""

import csv
import io
import json
import sqlite3
import sys
import zipfile
from array import array
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
DB = RADICE / "data" / "storico_backup.sqlite"
GTFS = RADICE / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"
OUT_JSON = RADICE / "data" / "processed" / "risultato4_regolarita.json"
OUT_RAPPORTO = RADICE / "docs" / "RAPPORTO_RISULTATO4.txt"

TAG = "MISURATO"
GIORNO_PROVA = "20261013"

# D2/D3/D4/D6/D8
SOGLIA_RITARDO = 5.0
SOGLIA_ANTICIPO = -1.0
MAX_LETTURA = 600.0          # secondi (10 minuti)
FREQ_MAX = 15.0              # minuti
MIN_PASSAGGI = 200
MIN_COPPIE = 100

TIPI = ("0", "1", "2")                        # 0 feriale, 1 sabato, 2 domenica
FASCE = ("punta_mattina", "giorno", "punta_sera", "sera", "notte")   # D9

# posizioni nei tuple dei passaggi
P_LINEA, P_DIR, P_STOP, P_SCHED, P_EST, P_RIT, P_FASCIA, P_SEQ, P_FONTE, P_TRIP = range(10)


# ---------- ora locale Europe/Rome (copiate da 09_analisi_dati_diurni.py) ----------

def ultima_domenica(anno, mese):
    """Giorno dell'ultima domenica del mese (date.weekday: lun=0 ... dom=6)."""
    ultimo = monthrange(anno, mese)[1]
    gw = date(anno, mese, ultimo).weekday()
    return ultimo - ((gw - 6) % 7)


def offset_roma(utc):
    """Offset in ore di Europe/Rome per un datetime UTC. Regola UE."""
    y = utc.year
    inizio = datetime(y, 3, ultima_domenica(y, 3), 1, tzinfo=timezone.utc)
    fine = datetime(y, 10, ultima_domenica(y, 10), 1, tzinfo=timezone.utc)
    return 2 if inizio <= utc < fine else 1


def a_roma(utc):
    return utc + timedelta(hours=offset_roma(utc))


def offset_data_locale(d):
    """Offset in ore valevole alla mezzanotte locale del giorno d."""
    for off in (2, 1):
        candidato = datetime(d.year, d.month, d.day, tzinfo=timezone.utc) - timedelta(hours=off)
        if offset_roma(candidato) == off:
            return off
    return 2


def fascia_oraria(h):
    if 7 <= h < 9:
        return "punta_mattina"
    if 9 <= h < 16:
        return "giorno"
    if 16 <= h < 19:
        return "punta_sera"
    if 19 <= h < 24:
        return "sera"
    return "notte"


def tipo_giorno_data(d):
    return {5: 1, 6: 2}.get(d.weekday(), 0)


def da_gttfs(g):
    return f"{g[0:4]}-{g[4:6]}-{g[6:8]}"


# ---------- GTFS ----------

def carica_gtfs():
    trip_info = {}
    nome_linea = {}
    prog = {}
    with zipfile.ZipFile(GTFS) as z:
        with z.open("routes.txt") as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                nome_linea[r["route_id"]] = r["route_short_name"]
        with z.open("trips.txt") as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                trip_info[r["trip_id"]] = (r["route_id"], int(r["direction_id"] or 0))
        with z.open("stop_times.txt") as f:
            for r in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")):
                h, m, s = (int(x) for x in r["arrival_time"].split(":"))
                prog[(r["trip_id"], int(r["stop_sequence"]))] = (h * 3600 + m * 60 + s, r["stop_id"])
    return trip_info, nome_linea, prog


# ---------- aggregatori ----------

def agg_punt():
    return [0, 0, 0, 0, array("d")]


def agg_reg():
    return [0, 0, 0, 0]


def conta_punt(a, rit):
    a[0] += 1
    if rit < SOGLIA_ANTICIPO:
        a[1] += 1
    elif rit > SOGLIA_RITARDO:
        a[3] += 1
    else:
        a[2] += 1
    a[4].append(rit)


def mediana(vals):
    if not vals:
        return 0.0
    v = sorted(vals)
    n = len(v)
    return round(v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2.0, 1)


def p90(vals):
    if not vals:
        return 0.0
    v = sorted(vals)
    return round(v[int(round(0.9 * (len(v) - 1)))], 1)


def pct(x, n):
    return round(100.0 * x / n, 1) if n else 0.0


def stat_punt(a):
    n = a[0]
    return {"passaggi": n, "anticipo": pct(a[1], n), "puntuale": pct(a[2], n),
            "ritardo": pct(a[3], n), "mediana": mediana(a[4]), "p90": p90(a[4])}


def stat_reg(a):
    n = a[0]
    return {"coppie": n, "grappolo": pct(a[1], n), "buco": pct(a[2], n),
            "regolare": pct(a[3], n)}


# ---------- un giorno alla volta ----------

def leggi_giorno(con, giorno):
    """D1: ultima lettura per (trip_id, seq) del giorno."""
    ultimo = {}
    for letto, trip_id, payload in con.execute(
            "SELECT letto_utc, trip_id, payload FROM trip_update_gtt "
            "WHERE start_date = ? ORDER BY letto_utc", (giorno,)):
        try:
            p = json.loads(payload)
        except (ValueError, TypeError):
            continue
        tid = ((p.get("trip") or {}).get("trip_id")) or trip_id
        for e in (p.get("stu") or []):
            arr = e.get("arr")
            seq = e.get("seq")
            if not arr or seq is None:
                continue
            ultimo[(tid, seq)] = (letto, arr)
    return ultimo


def costruisci_passaggi(ultimo, giorno, trip_info, nome_linea, prog):
    """D2-D5: trasforma le ultime letture in passaggi validi."""
    data = datetime.strptime(giorno, "%Y%m%d").date()
    tipo = str(tipo_giorno_data(data))
    off = offset_data_locale(data)
    mezzanotte = datetime(data.year, data.month, data.day, tzinfo=timezone.utc) - timedelta(hours=off)
    passaggi = []
    scarti = [0, 0]          # fuori GTFS, lettura lontana
    esempi = {"delay": None, "time": None}
    for (tid, seq), (letto, arr) in ultimo.items():
        info = trip_info.get(tid)
        p = prog.get((tid, seq))
        if info is None or p is None:
            scarti[0] += 1
            continue
        secondi, stop_id = p
        route_id, direzione = info
        sched = mezzanotte + timedelta(seconds=secondi)
        if not isinstance(arr, dict):
            continue
        if arr.get("delay") is not None:
            rit = arr["delay"] / 60.0
            fonte = "delay"
        elif arr.get("time") is not None:
            rit = (arr["time"] - sched.timestamp()) / 60.0
            fonte = "time"
        else:
            continue                     # né delay né time: nessun ritardo utilizzabile
        est = sched + timedelta(minutes=rit)
        letto_dt = datetime.fromisoformat(letto)
        if abs((est - letto_dt).total_seconds()) > MAX_LETTURA:
            scarti[1] += 1
            continue
        if esempi[fonte] is None:
            esempi[fonte] = {
                "trip_id": tid, "seq": seq, "start_date": giorno, "letto": letto,
                "arr": dict(arr), "fonte": fonte,
                "orario_gtfs": f"{secondi // 3600:02d}:{secondi % 3600 // 60:02d}:{secondi % 60:02d}",
                "sched_utc": sched.isoformat(), "est_utc": est.isoformat(),
                "ritardo_min": round(rit, 2)}
        passaggi.append((nome_linea.get(route_id, route_id), direzione, stop_id,
                         sched.timestamp(), est.timestamp(), rit,
                         fascia_oraria(a_roma(sched).hour), seq, fonte, tid))
    return passaggi, scarti, tipo, esempi


def regolarita(passaggi, tipo):
    """D6-D7: coppie di passaggi consecutivi alla stessa fermata.

    Ritorna (totali città, totali per nome linea, esempio di grappolo).
    """
    gruppi = {}
    for pg in passaggi:
        gruppi.setdefault((pg[P_LINEA], pg[P_DIR], pg[P_STOP]), []).append(pg)
    coppie = agg_reg()
    per_linea = {}
    esempio = None
    for lista in gruppi.values():
        if len(lista) < 2:
            continue
        lista.sort(key=lambda x: x[P_SCHED])
        for i in range(len(lista) - 1):
            a, b = lista[i], lista[i + 1]
            prog_i = (b[P_SCHED] - a[P_SCHED]) / 60.0
            if not 0 < prog_i <= FREQ_MAX:      # D6
                continue
            obs_i = (b[P_EST] - a[P_EST]) / 60.0
            if obs_i < 0.5 * prog_i:
                classe = 1                      # grappolo
            elif obs_i > 2 * prog_i:
                classe = 2                      # buco
            else:
                classe = 3                      # regolare
            coppie[0] += 1
            coppie[classe] += 1
            t = per_linea.setdefault((tipo, a[P_LINEA]), agg_reg())
            t[0] += 1
            t[classe] += 1
            if classe == 1 and esempio is None:
                esempio = {"linea": a[P_LINEA], "direzione": a[P_DIR], "stop_id": a[P_STOP],
                           "sched_a": datetime.fromtimestamp(a[P_SCHED], timezone.utc).isoformat(),
                           "sched_b": datetime.fromtimestamp(b[P_SCHED], timezone.utc).isoformat(),
                           "est_a": datetime.fromtimestamp(a[P_EST], timezone.utc).isoformat(),
                           "est_b": datetime.fromtimestamp(b[P_EST], timezone.utc).isoformat(),
                           "prog_min": round(prog_i, 2), "obs_min": round(obs_i, 2),
                           "tipo": tipo}
    return coppie, per_linea, esempio


# ---------- main ----------

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    prova = "--prova" in sys.argv[1:]

    print("Carico il GTFS...", file=sys.stderr)
    trip_info, nome_linea, prog = carica_gtfs()
    print(f"GTFS: {len(trip_info)} corse, {len(prog)} fermate di corsa", file=sys.stderr)

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=60)
    giorni = [r[0] for r in con.execute(
        "SELECT DISTINCT start_date FROM trip_update_gtt ORDER BY 1")]
    if prova:
        giorni = [g for g in giorni if g == GIORNO_PROVA]
        if not giorni:
            raise SystemExit(f"Nessuna riga per {GIORNO_PROVA}")
    print(f"Giorni: {giorni}", file=sys.stderr)

    giorni_tipo = {"0": 0, "1": 0, "2": 0}
    punt_citta, punt_citta_fascia, punt_linea, punt_fascia = {}, {}, {}, {}
    reg_citta, reg_linea = {}, {}
    scarti = {"fuori_gtfs": 0, "lettura_lontana": 0, "usati": 0}
    letti_totali = 0
    # controlli indipendenti (passo 5)
    per_fonte = {"delay": array("d"), "time": array("d")}
    per_seq = {"seq 1-5": array("d"), "seq 6-15": array("d"),
               "seq 16-30": array("d"), "seq 31+": array("d")}
    esempi = {"delay": None, "time": None}
    es_grappolo = None

    for n, giorno in enumerate(giorni, 1):
        print(f"[{n}/{len(giorni)}] giorno {giorno}...", file=sys.stderr)
        ultimo = leggi_giorno(con, giorno)
        letti_totali += len(ultimo)
        passaggi, sc, tipo, es = costruisci_passaggi(ultimo, giorno, trip_info, nome_linea, prog)
        del ultimo
        scarti["fuori_gtfs"] += sc[0]
        scarti["lettura_lontana"] += sc[1]
        scarti["usati"] += len(passaggi)
        giorni_tipo[str(tipo)] += 1
        for k, v in es.items():
            if esempi[k] is None and v is not None:
                esempi[k] = v
        for pg in passaggi:
            conta_punt(punt_citta.setdefault(tipo, agg_punt()), pg[P_RIT])
            conta_punt(punt_citta_fascia.setdefault((tipo, pg[P_FASCIA]), agg_punt()), pg[P_RIT])
            conta_punt(punt_linea.setdefault((tipo, pg[P_LINEA]), agg_punt()), pg[P_RIT])
            conta_punt(punt_fascia.setdefault((tipo, pg[P_LINEA], pg[P_FASCIA]), agg_punt()), pg[P_RIT])
            per_fonte[pg[P_FONTE]].append(pg[P_RIT])
            if pg[P_SEQ] <= 5:
                per_seq["seq 1-5"].append(pg[P_RIT])
            elif pg[P_SEQ] <= 15:
                per_seq["seq 6-15"].append(pg[P_RIT])
            elif pg[P_SEQ] <= 30:
                per_seq["seq 16-30"].append(pg[P_RIT])
            else:
                per_seq["seq 31+"].append(pg[P_RIT])
        c, per_linea, es = regolarita(passaggi, tipo)
        if c[0]:
            r = reg_citta.setdefault(tipo, agg_reg())
            for i in range(4):
                r[i] += c[i]
        for k, t in per_linea.items():
            r = reg_linea.setdefault(k, agg_reg())
            for i in range(4):
                r[i] += t[i]
        if es_grappolo is None and es is not None:
            es_grappolo = es
        del passaggi
    con.close()

    # ---------- output JSON ----------
    per = {"da": da_gttfs(giorni[0]), "a": da_gttfs(giorni[-1])}
    parametri = {"soglia_ritardo_min": SOGLIA_RITARDO, "soglia_anticipo_min": SOGLIA_ANTICIPO,
                 "max_lettura_lontana_min": MAX_LETTURA / 60, "freq_max_min": FREQ_MAX,
                 "min_passaggi": MIN_PASSAGGI, "min_coppie": MIN_COPPIE}
    j_citta = {}
    for t, a in punt_citta.items():
        blocco = stat_punt(a)
        blocco.update(stat_reg(reg_citta.get(t, agg_reg())))
        j_citta[t] = blocco
    j_linee = {}
    for (t, linea), a in punt_linea.items():
        c = reg_linea.get((t, linea), agg_reg())
        if a[0] < MIN_PASSAGGI and c[0] < MIN_COPPIE:      # D8
            continue
        blocco = stat_punt(a)
        blocco.update(stat_reg(c))
        fas = {}
        for f in FASCE:
            b = punt_fascia.get((t, linea, f))
            if b and b[0]:
                fas[f] = stat_punt(b)
        blocco["fasce"] = fas
        j_linee.setdefault(linea, {})[t] = blocco

    json_out = {
        "generato": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tag": TAG, "periodo": per, "giorni": giorni_tipo, "parametri": parametri,
        "scarti": scarti, "citta": j_citta, "linee": j_linee}

    # ---------- rapporto ----------
    R = []
    R.append("RISULTATO 4 — Bus in ritardo e bus irregolari [MISURATO]")
    R.append("=" * 66)
    R.append(f"Periodo: {per['da']} -> {per['a']}   giorni: feriale {giorni_tipo['0']}, "
             f"sabato {giorni_tipo['1']}, domenica {giorni_tipo['2']}")
    tot_sc = scarti["fuori_gtfs"] + scarti["lettura_lontana"] + scarti["usati"]
    R.append(f"Passaggi osservati (ultime letture): {tot_sc}")
    R.append(f"  usati: {scarti['usati']} ({pct(scarti['usati'], tot_sc)}%)")
    R.append(f"  scartati fuori GTFS: {scarti['fuori_gtfs']} ({pct(scarti['fuori_gtfs'], tot_sc)}%)")
    R.append(f"  scartati lettura lontana (>10 min): {scarti['lettura_lontana']} "
             f"({pct(scarti['lettura_lontana'], tot_sc)}%)")
    R.append("")
    fer = j_citta.get("0", {})
    R.append("I 3 NUMERI (feriale)")
    R.append(f"1. passaggi in ritardo > 5 min: {fer.get('ritardo', 0.0)}%")
    R.append(f"2. coppie a grappolo {fer.get('grappolo', 0.0)}% + a buco {fer.get('buco', 0.0)}%"
             f" = {round(fer.get('grappolo', 0.0) + fer.get('buco', 0.0), 1)}% (linee frequenti)")
    R.append(f"3. ritardo mediano: {fer.get('mediana', 0.0)} min")
    R.append("")
    R.append("PUNTUALITA' CITTA' — per tipo di giorno")
    R.append("tipo giorno | passaggi | % anticipo | % puntuale | % ritardo>5 | mediana | p90")
    nomi = {"0": "feriale", "1": "sabato", "2": "domenica"}
    for t in TIPI:
        if t in j_citta:
            c = j_citta[t]
            R.append(f"{nomi[t]:11} | {c['passaggi']:8} | {c['anticipo']:10} | {c['puntuale']:10} "
                     f"| {c['ritardo']:11} | {c['mediana']:7} | {c['p90']}")
    R.append("")
    R.append("PUNTUALITA' CITTA' — fasce orarie (feriale, ora locale dell'arrivo programmato)")
    R.append("fascia        | passaggi | % anticipo | % puntuale | % ritardo>5 | mediana | p90")
    for f in FASCE:
        b = punt_citta_fascia.get(("0", f))
        if b and b[0]:
            c = stat_punt(b)
            R.append(f"{f:13} | {c['passaggi']:8} | {c['anticipo']:10} | {c['puntuale']:10} "
                     f"| {c['ritardo']:11} | {c['mediana']:7} | {c['p90']}")
    R.append("")

    class_p = sorted(((v["ritardo"], k) for k, v in
                      ((ln, j_linee[ln]["0"]) for ln in j_linee if "0" in j_linee[ln])
                      if v["passaggi"] >= MIN_PASSAGGI), reverse=True)
    R.append(f"10 LINEE PEGGIORI PER % IN RITARDO (feriale, >= {MIN_PASSAGGI} passaggi)")
    for i, (val, ln) in enumerate(class_p[:10], 1):
        c = j_linee[ln]["0"]
        R.append(f"{i:2}. linea {ln:<5} {val:5}% in ritardo | {c['passaggi']} passaggi "
                 f"| mediana {c['mediana']} min | p90 {c['p90']} min")
    R.append("")

    class_r = sorted(((round(v["grappolo"] + v["buco"], 1), k) for k, v in
                      ((ln, j_linee[ln]["0"]) for ln in j_linee if "0" in j_linee[ln])
                      if v["coppie"] >= MIN_COPPIE), reverse=True)
    R.append(f"10 LINEE PEGGIORI PER IRREGOLARITA' (feriale, >= {MIN_COPPIE} coppie)")
    for i, (val, ln) in enumerate(class_r[:10], 1):
        c = j_linee[ln]["0"]
        R.append(f"{i:2}. linea {ln:<5} {val:5}% grappolo+buco | {c['coppie']} coppie "
                 f"| grappolo {c['grappolo']}% | buco {c['buco']}%")
    R.append("")
    R.append("[MISURATO] dal feed GTFS-Realtime GTT; il ritardo è quello stimato dal sistema GTT "
             "alla fermata nell'ultima lettura prima dell'arrivo; sabato e domenica con 1 solo "
             "giorno: [DATI SCARSI].")
    testo = "\n".join(R) + "\n"

    # ---------- controlli (passo 5) a schermo ----------
    C = []
    C.append("CONTROLLI (passo 5)")
    C.append(f"  mediana con arr.delay  : {mediana(per_fonte['delay'])} min "
             f"({len(per_fonte['delay'])} passaggi)")
    C.append(f"  mediana con arr.time   : {mediana(per_fonte['time'])} min "
             f"({len(per_fonte['time'])} passaggi)")
    for k, v in per_seq.items():
        C.append(f"  mediana {k:12}: {mediana(v):6} min ({len(v)} passaggi)")
    for f in FASCE:
        b = punt_citta_fascia.get(("0", f))
        if b and b[0]:
            C.append(f"  feriale {f:13}: {pct(b[3], b[0])}% in ritardo>5 ({b[0]} passaggi)")
    fer_somma = round(fer.get("anticipo", 0) + fer.get("puntuale", 0) + fer.get("ritardo", 0), 1)
    fer_reg = round(fer.get("grappolo", 0) + fer.get("buco", 0) + fer.get("regolare", 0), 1)
    C.append(f"  somma classi puntualita' feriale: {fer_somma}%")
    C.append(f"  somma classi regolarita' feriale: {fer_reg}%")
    for k in ("delay", "time"):
        if esempi[k]:
            C.append(f"  esempio {k}: {json.dumps(esempi[k], ensure_ascii=False)}")
    if es_grappolo:
        C.append(f"  esempio grappolo: {json.dumps(es_grappolo, ensure_ascii=False)}")
    testo_c = "\n".join(C) + "\n"

    sys.stdout.write("\n" + testo)
    sys.stdout.write("\n" + testo_c)

    if not prova:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(json_out, ensure_ascii=False), encoding="utf-8")
        OUT_RAPPORTO.write_text(testo, encoding="utf-8")
        print(f"Scritto: {OUT_JSON}\nScritto: {OUT_RAPPORTO}")
    else:
        print("(--prova: nessun file scritto)")


if __name__ == "__main__":
    main()
