#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""90 - Verifica della regola D3 dello script 27 con le posizioni GPS dei mezzi (Risultato 4, Giro 3).

SOLO LETTURA: database aperto in sola lettura; scrive solo docs/RAPPORTO_R4_VERIFICA_GPS.txt. NON cambia D3 ne' nessun'altra
regola D1-D9: serve a decidere con Leo.

Domanda: la regola D3 scarta i passaggi la cui ultima lettura e' a piu' di 10 minuti dall'arrivo stimato. Gli scartati hanno
ritardi lunghi (nei feriali 34.929 su 49.818 oltre 10 minuti): se si scartano, i ritardi lunghi non entrano nei conti. Qui si
controlla con un dato indipendente, il GPS (tabella mezzi_gtt), quanto sono davvero in ritardo.

Gruppi (2 giorni feriali interi, 15 e 16 ottobre):
  A  usati con ritardo del feed fino a 5 minuti
  B  usati con ritardo del feed oltre 5 e fino a 10 minuti (se esistessero usati oltre 10, vanno qui e sono contati a parte)
  C  scartati per lettura lontana (D3)
Per ogni gruppo si prende a passo fisso (uno ogni k, niente caso) al massimo MAX_PER_GRUPPO passaggi in tutto (meta' per giorno).
Passaggio GPS valido: il mezzo (stessa corsa) passa a meno di 60 m dalla fermata (stessa logica di controllo_gps() dello
script 70: tempo interpolato sul segmento fra due posizioni consecutive piu' vicino alla fermata, segmenti di non piu' di 180 s).
Ritardo vero = istante del passaggio GPS - orario programmato. Se |ritardo vero| supera MAX_RITARDO_VERO_MIN il passaggio GPS
si considera una corrispondenza sbagliata (es. linee ad anello) e non e' valido.
"""
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comuni  # noqa: E402

RADICE = comuni.RADICE
RAPPORTO = RADICE / "docs" / "RAPPORTO_R4_VERIFICA_GPS.txt"
GIORNI = ("20261015", "20261016")      # 2 feriali interi (valore predefinito di Claude, 21/10)
MAX_PER_GRUPPO = 3000                  # in tutto, per gruppo
DIST_GPS_M = 60.0                      # come lo script 70
SEGMENTO_MAX_S = 180
MAX_RITARDO_VERO_MIN = 60.0
MIN_GPS_GRUPPO_C = 300
GRUPPI = {"A": "usati, ritardo del feed fino a 5 min", "B": "usati, ritardo del feed oltre 5 min",
          "C": "scartati per lettura lontana (D3)"}
PERC = (10, 25, 50, 75, 90)

m27 = comuni.carica_script("27_risultato4_regolarita.py")
m70 = comuni.carica_script("70_risultato9_attesa.py")


def passaggi_con_scartati(ultimo, giorno, trip_info, nome_linea, prog):
    """Come m27.costruisci_passaggi (D2-D5) ma tiene anche gli scartati per lettura lontana (D3).
    Ritorna lista di dict e il conteggio dei fuori GTFS."""
    data = datetime.strptime(giorno, "%Y%m%d").date()
    off = m27.offset_data_locale(data)
    mezzanotte = datetime(data.year, data.month, data.day, tzinfo=timezone.utc) - timedelta(hours=off)
    out, fuori = [], 0
    for (tid, seq), (letto, arr) in ultimo.items():
        info = trip_info.get(tid)
        p = prog.get((tid, seq))
        if info is None or p is None:
            fuori += 1
            continue
        secondi, stop_id = p
        sched = mezzanotte + timedelta(seconds=secondi)
        if not isinstance(arr, dict):
            continue
        if arr.get("delay") is not None:
            rit = arr["delay"] / 60.0
        elif arr.get("time") is not None:
            rit = (arr["time"] - sched.timestamp()) / 60.0
        else:
            continue
        est = sched + timedelta(minutes=rit)
        letto_dt = datetime.fromisoformat(letto)
        scartato = abs((est - letto_dt).total_seconds()) > m27.MAX_LETTURA
        gruppo = "C" if scartato else ("A" if rit <= m27.SOGLIA_RITARDO else "B")
        out.append({"linea": nome_linea.get(info[0], info[0]), "tid": tid, "seq": seq, "stop": stop_id,
                    "sched": sched.timestamp(), "est": est.timestamp(), "rit": rit,
                    "letto": letto_dt.timestamp(), "g": gruppo})
    return out, fuori


def passo_fisso(lista, massimo):
    """Uno ogni k (k = ceil(n / massimo)), niente caso; ordine fisso per (stop, trip, seq)."""
    lista = sorted(lista, key=lambda x: (x["tid"], x["seq"]))
    if len(lista) <= massimo:
        return lista
    k = -(-len(lista) // massimo)
    return lista[::k]


def ora_gps_vicino(punti, flat, flon):
    """Istante (epoch s) in cui il mezzo passa piu' vicino alla fermata, se entro DIST_GPS_M; altrimenti None.
    Stessa logica di controllo_gps() dello script 70, per un passaggio alla volta."""
    migliore = None
    for (t0, la0, lo0), (t1, la1, lo1) in zip(punti, punti[1:]):
        if t1 - t0 > SEGMENTO_MAX_S or t1 <= t0:
            continue
        x0, y0 = m70.metri(flat, flon, la0, lo0)
        x1, y1 = m70.metri(flat, flon, la1, lo1)
        dx, dy = x1 - x0, y1 - y0
        l2 = dx * dx + dy * dy
        f = 0.0 if l2 == 0 else max(0.0, min(1.0, -(x0 * dx + y0 * dy) / l2))
        dist = (((x0 + f * dx) ** 2) + ((y0 + f * dy) ** 2)) ** 0.5
        if migliore is None or dist < migliore[0]:
            migliore = (dist, t0 + f * (t1 - t0))
    return migliore[1] if migliore and migliore[0] <= DIST_GPS_M else None


def perc(v, p):
    s = sorted(v)
    return s[int(round(p / 100.0 * (len(s) - 1)))] if s else None


def quote(rv):
    """% del ritardo vero: fino a 5, da 5 a 10, oltre 10 minuti."""
    n = len(rv)
    if not n:
        return None
    return (100.0 * sum(x <= 5 for x in rv) / n, 100.0 * sum(5 < x <= 10 for x in rv) / n, 100.0 * sum(x > 10 for x in rv) / n)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    c = comuni.Controlli()
    trip_info, nome_linea, prog, modo_linea, _us, _km = m27.carica_gtfs()
    _s, _c, _e, fermate = m70.carica_calendario()
    con = sqlite3.connect(f"file:{m27.DB}?mode=ro", uri=True, timeout=60)

    tot = {g: 0 for g in GRUPPI}                       # passaggi per gruppo, 2 giorni
    tot_modo = {(g, m): 0 for g in GRUPPI for m in ("tram", "bus")}
    campione = {g: [] for g in GRUPPI}                 # passaggi del campione (con ritardo vero se valido)
    usati_m27 = 0
    usati_miei = 0
    oggi = {m: [0, 0, 0] for m in ("tutti", "tram", "bus")}      # passaggi usati, oltre 5 min, oltre 10 min (feed)
    righe_giorno = {}
    for giorno in GIORNI:
        n_righe = con.execute("SELECT COUNT(*) FROM trip_update_gtt WHERE start_date = ?", (giorno,)).fetchone()[0]
        data = datetime.strptime(giorno, "%Y%m%d").date()
        c(f"{giorno} e' un giorno feriale", m27.tipo_giorno_data(data) == 0, bloccante=True)
        righe_giorno[giorno] = n_righe
        print(f"giorno {giorno}: {n_righe} righe di trip_update", file=sys.stderr)
        ultimo = m27.leggi_giorno(con, giorno)
        passaggi, fuori = passaggi_con_scartati(ultimo, giorno, trip_info, nome_linea, prog)
        # controllo: i miei A + B uguali ai passaggi usati dallo script 27
        p27, sc27, _t, _es = m27.costruisci_passaggi(ultimo, giorno, trip_info, nome_linea, prog)
        usati_m27 += len(p27)
        usati_miei += sum(1 for p in passaggi if p["g"] != "C")
        del ultimo, p27
        per_g = defaultdict(list)
        for p in passaggi:
            per_g[p["g"]].append(p)
            tot[p["g"]] += 1
            m = modo_linea.get(p["linea"], "bus")
            if p["g"] != "C":
                for k in ("tutti", m):
                    if k in oggi:
                        oggi[k][0] += 1
                        oggi[k][1] += p["rit"] > m27.SOGLIA_RITARDO
                        oggi[k][2] += p["rit"] > m27.SOGLIA_RITARDO_10
            if m in ("tram", "bus"):
                tot_modo[(p["g"], m)] += 1
        scelti = []
        for g, lista in per_g.items():
            for p in passo_fisso(lista, MAX_PER_GRUPPO // len(GIORNI)):
                scelti.append(p)
        # posizioni GPS delle corse scelte
        corse = {p["tid"] for p in scelti}
        mezz = m70.mezzanotte_utc(giorno)
        da, a = mezz.isoformat(), (mezz + timedelta(hours=26)).isoformat()
        pos = defaultdict(set)
        for corsa, ts, lat, lng in con.execute(
                "SELECT corsa, ts_feed, lat, lng FROM mezzi_gtt WHERE letto_utc BETWEEN ? AND ?", (da, a)):
            if corsa in corse and ts and lat and lng:
                pos[corsa].add((ts, lat, lng))
        punti_corsa = {k: sorted(v) for k, v in pos.items()}
        for p in scelti:
            p["modo"] = modo_linea.get(p["linea"], "bus")
            p["gps"] = None
            info = fermate.get(p["stop"])
            punti = punti_corsa.get(p["tid"])
            if info and punti and len(punti) >= 2:
                t = ora_gps_vicino(punti, info[1], info[2])
                if t is not None:
                    rv = (t - p["sched"]) / 60.0
                    if abs(rv) <= MAX_RITARDO_VERO_MIN:
                        p["gps"] = t
                        p["rv"] = rv
            campione[p["g"]].append(p)
        del passaggi, scelti, pos, punti_corsa
    con.close()

    c("passaggi usati (A + B) uguali a quelli dello script 27 nei 2 giorni", usati_m27 == usati_miei,
      dettaglio=f"{usati_miei} contro {usati_m27}")
    c("i due giorni hanno righe di trip_update simili (almeno 70% del maggiore)",
      min(righe_giorno.values()) >= 0.7 * max(righe_giorno.values()),
      dettaglio=", ".join(f"{g}: {n}" for g, n in righe_giorno.items()))

    R = ["RAPPORTO R4 - VERIFICA DELLA REGOLA D3 CON IL GPS (script 90, solo lettura)", "=" * 70,
         f"Giorni feriali: {', '.join(GIORNI)}. Gruppi: " + "; ".join(f"{g} = {d}" for g, d in GRUPPI.items()) + ".",
         f"Campione a passo fisso: al massimo {MAX_PER_GRUPPO} passaggi per gruppo in tutto ({MAX_PER_GRUPPO // len(GIORNI)} per giorno).",
         f"GPS valido: stessa corsa a meno di {DIST_GPS_M:.0f} m dalla fermata, segmenti di non piu' di {SEGMENTO_MAX_S} s; "
         f"ritardo vero = passaggio GPS - orario programmato; scartato se oltre {MAX_RITARDO_VERO_MIN:.0f} min in valore assoluto.", ""]
    R.append("PER GRUPPO")
    R.append("gruppo | passaggi (2 giorni) | nel campione | con GPS valido | ritardo vero: <=5 min | 5-10 min | >10 min "
             "| mediana (min) | stima feed - GPS, mediana (min)")
    risultati = {}
    for g in GRUPPI:
        camp = campione[g]
        valid = [p for p in camp if p["gps"] is not None]
        rv = [p["rv"] for p in valid]
        q = quote(rv)
        diff = sorted((p["est"] - p["gps"]) / 60.0 for p in valid)
        risultati[g] = {"n": tot[g], "campione": len(camp), "valid": len(valid), "q": q}
        if q:
            R.append(f"{g:6} | {tot[g]:19} | {len(camp):12} | {len(valid):14} | {q[0]:21.1f}% | {q[1]:8.1f}% | {q[2]:7.1f}% "
                     f"| {perc(rv, 50):13.1f} | {perc(diff, 50):.1f}")
        else:
            R.append(f"{g:6} | {tot[g]:19} | {len(camp):12} | {0:14} | nessun GPS valido")
    R.append("")
    R.append("PER MODO (gruppo C e confronto)")
    R.append("gruppo modo | passaggi | con GPS valido | ritardo vero: <=5 | 5-10 | >10")
    for g in GRUPPI:
        for m in ("tram", "bus"):
            valid = [p for p in campione[g] if p["gps"] is not None and p["modo"] == m]
            q = quote([p["rv"] for p in valid])
            if q:
                R.append(f"{g:6} {m:4} | {tot_modo[(g, m)]:8} | {len(valid):14} | {q[0]:16.1f}% | {q[1]:4.1f}% | {q[2]:4.1f}%")
            else:
                R.append(f"{g:6} {m:4} | {tot_modo[(g, m)]:8} | {0:14} | nessun GPS valido")
    R.append("")
    # gruppo C: quando smette la lettura
    cv = [p for p in campione["C"] if p["gps"] is not None]
    dist_c = [(p["letto"] - p["sched"]) / 60.0 for p in campione["C"]]
    R.append("GRUPPO C - ultima lettura meno orario programmato (minuti; negativo = lettura prima dell'orario)")
    R.append("  tutto il campione C: " + ", ".join(f"p{x} {perc(dist_c, x):.1f}" for x in PERC) if dist_c else "  (vuoto)")
    if cv:
        R.append("  solo C con GPS valido: " + ", ".join(f"p{x} {perc([(p['letto'] - p['sched']) / 60.0 for p in cv], x):.1f}" for x in PERC))
        dl = [(p["letto"] - p["gps"]) / 60.0 for p in cv]
        R.append("  ultima lettura meno passaggio GPS (C con GPS): " + ", ".join(f"p{x} {perc(dl, x):.1f}" for x in PERC))
        R.append("  ritardo del feed (C con GPS): " + ", ".join(f"p{x} {perc([p['rit'] for p in cv], x):.1f}" for x in PERC))
        R.append("  ritardo vero (C con GPS): " + ", ".join(f"p{x} {perc([p['rv'] for p in cv], x):.1f}" for x in PERC))
    R.append("")

    # stima corretta: usati come oggi (ritardo del feed) + scartati con il ritardo vero del GPS, pesati per il numero di scartati
    def stima(m):
        n_u, o5, o10 = oggi[m]
        n_c = tot["C"] if m == "tutti" else tot_modo[("C", m)]
        valid = [p for p in campione["C"] if p["gps"] is not None and (m == "tutti" or p["modo"] == m)]
        if not n_u or not valid:
            return None
        f5 = sum(p["rv"] > m27.SOGLIA_RITARDO for p in valid) / len(valid)
        f10 = sum(p["rv"] > m27.SOGLIA_RITARDO_10 for p in valid) / len(valid)
        tutti = n_u + n_c
        return {"oggi5": 100.0 * o5 / n_u, "oggi10": 100.0 * o10 / n_u,
                "cor5": 100.0 * (o5 + n_c * f5) / tutti, "cor10": 100.0 * (o10 + n_c * f10) / tutti,
                "n_usati": n_u, "n_scartati": n_c, "n_valid": len(valid)}
    R.append("STIMA CORRETTA (2 giorni feriali, % dei passaggi in ritardo)")
    R.append("  corretta = passaggi usati come oggi (ritardo del feed) + scartati per lettura lontana con il ritardo vero del GPS "
             "(frazione misurata sul campione con GPS valido, pesata per tutti gli scartati)")
    R.append("modo  | usati | scartati | GPS validi (C) | oggi: oltre 5 | oggi: oltre 10 | corretta: oltre 5 | corretta: oltre 10")
    stime = {}
    for m in ("tutti", "tram", "bus"):
        st = stima(m)
        stime[m] = st
        if st:
            R.append(f"{m:5} | {st['n_usati']:5} | {st['n_scartati']:8} | {st['n_valid']:14} | {st['oggi5']:12.2f}% | {st['oggi10']:12.2f}% "
                     f"| {st['cor5']:16.2f}% | {st['cor10']:16.2f}%")
        else:
            R.append(f"{m:5} | nessuna stima (GPS validi insufficienti)")
    n_c = tot["C"]
    usati = tot["A"] + tot["B"]
    R.append(f"  scartati per lettura lontana: {n_c} su {usati + n_c} passaggi con orario nel GTFS ({100.0 * n_c / (usati + n_c):.1f}%)")
    n_valid_c = len([p for p in campione["C"] if p["gps"] is not None])
    c("almeno %d passaggi con GPS valido nel gruppo C" % MIN_GPS_GRUPPO_C, n_valid_c >= MIN_GPS_GRUPPO_C,
      dettaglio=f"{n_valid_c} su {len(campione['C'])} del campione")
    for m in ("tram", "bus"):
        nv = len([p for p in campione["C"] if p["gps"] is not None and p["modo"] == m])
        c(f"gruppo C con GPS valido, {m}: almeno 30", nv >= 30, dettaglio=f"{nv}")
    R += ["", "Letture: la stima corretta e' un controllo con un dato indipendente, non cambia la regola D3 ne' i risultati; "
          "la decisione e' di Leo.", "", "CONTROLLI"] + ["  " + x for x in c.righe]
    testo = chr(10).join(R) + chr(10)
    RAPPORTO.write_text(testo, encoding="utf-8")
    print(testo)
    print(f"Scritto {RAPPORTO.relative_to(RADICE)}; avvisi: {len(c.avvisi())}")


if __name__ == "__main__":
    main()
