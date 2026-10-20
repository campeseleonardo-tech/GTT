#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""91 - Risultato 4 calcolato sul GPS: prova su 2 giorni feriali (Giro 4).

SOLO LETTURA: database aperto in sola lettura; scrive solo data/processed/risultato4_gps_prova.json e
docs/RAPPORTO_R4_GPS_PROVA.txt. Non cambia lo script 27, i suoi risultati ne' le pagine.

Idea (decisione di Leo, 21/10): il feed GTT smette di elencare la fermata all'orario programmato, quindi per i mezzi in
ritardo la stima del feed e' troppo bassa (script 90). Qui il ritardo di un passaggio e' preso dal GPS:
  ritardo = istante in cui il mezzo (stessa corsa) passa a meno di 60 m dalla fermata - orario programmato.
Il feed resta come confronto.

Regole del passaggio GPS (come gli script 70 e 90): segmenti fra due posizioni consecutive lunghi al massimo 180 s, tempo
interpolato sul segmento piu' vicino alla fermata, distanza <= 60 m, |ritardo| <= 60 min. In piu': le fermate di una corsa si
cercano in ordine di stop_sequence e il passaggio di una fermata puo' venire solo dopo quello della fermata prima (i tempi
non tornano indietro: evita errori sulle linee che ripassano vicino alla stessa fermata).
Classi, fasce e regolarita' (D4, D6, D7, D9) sono quelle dello script 27, con l'arrivo del GPS al posto di quello del feed.

Insiemi di passaggi confrontati:
  feed oggi     passaggi usati dallo script 27 (D3 applicata), ritardo del feed
  GPS tutti     tutti i passaggi con GPS valido
  stessi        passaggi con GPS valido E usati dal feed: stesso insieme, ritardo del feed contro ritardo del GPS
"""
import json
import math
import sqlite3
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comuni  # noqa: E402

RADICE = comuni.RADICE
OUT_JSON = RADICE / "data" / "processed" / "risultato4_gps_prova.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R4_GPS_PROVA.txt"
GIORNI = ("20261015", "20261016")      # come lo script 90
DIST_GPS_M = 60.0
SEGMENTO_MAX_S = 180
MAX_RITARDO_VERO_MIN = 60.0
COPERTURA_MIN_PCT = 60.0               # (a)
LETTURA_VICINA_S = 120.0               # (b) ultima lettura del feed a meno di 2 minuti dall'arrivo stimato
MAX_DIFF_FEED_GPS_MIN = 1.0            # (b)
MIN_CRESCENTI_PCT = 99.0               # (c)
CAMPIONE_CRESCENTI = 25                # (c) una corsa ogni 25 con la ricerca libera
PRIMA_FERMATA_MIN = (-2.0, 3.0)        # (d)
MAX_SCARTO_GIORNI = 0.20               # (e) differenza fra i due giorni al massimo 20%
MIN_PASSAGGI_PROG_COPERTURA = 200      # linee in classifica copertura: almeno 200 passaggi programmati
MIN_PASSAGGI_CLASSIFICA_RIF = 2000     # soglia dello script 27, pensata per tutti i giorni feriali del feed
MIN_COPPIE_CLASSIFICA = 30             # per la regolarita' per linea nei 2 giorni (solo in JSON)
MODI = ("tram", "bus")

m27 = comuni.carica_script("27_risultato4_regolarita.py")
m70 = comuni.carica_script("70_risultato9_attesa.py")
m90 = comuni.carica_script("90_verifica_ritardi_gps.py")

P_LINEA, P_DIR, P_STOP, P_SCHED, P_EST, P_RIT, P_FASCIA, P_SEQ, P_FONTE, P_TRIP = range(10)
FASCE = m27.FASCE


# ---------- ricerca del passaggio GPS ----------

def _segmento(punti, i, flat, flon, kx):
    """(dist, istante) del punto del segmento i piu' vicino alla fermata; None se il segmento non e' usabile.
    Stessa geometria di controllo_gps() dello script 70, con il rifiuto veloce per i segmenti lontani."""
    t0, la0, lo0 = punti[i]
    t1, la1, lo1 = punti[i + 1]
    if t1 <= t0 or t1 - t0 > SEGMENTO_MAX_S:
        return None
    x0, y0 = (lo0 - flon) * kx, (la0 - flat) * 110540.0
    x1, y1 = (lo1 - flon) * kx, (la1 - flat) * 110540.0
    r = DIST_GPS_M
    if (x0 > r and x1 > r) or (x0 < -r and x1 < -r) or (y0 > r and y1 > r) or (y0 < -r and y1 < -r):
        return (1e9, t0)
    dx, dy = x1 - x0, y1 - y0
    l2 = dx * dx + dy * dy
    f = 0.0 if l2 == 0 else max(0.0, min(1.0, -(x0 * dx + y0 * dy) / l2))
    return (math.hypot(x0 + f * dx, y0 + f * dy), t0 + f * (t1 - t0))


def cerca_vincolata(punti, flat, flon, kx, t_prec, i0):
    """Primo gruppo di segmenti vicini alla fermata con istante >= t_prec, a partire dal segmento i0.
    Ritorna (istante, indice del segmento) del piu' vicino del gruppo, oppure None."""
    migliore = None
    for i in range(i0, len(punti) - 1):
        s = _segmento(punti, i, flat, flon, kx)
        vicino = s is not None and s[0] <= DIST_GPS_M and s[1] >= t_prec
        if vicino:
            if migliore is None or s[0] < migliore[0]:
                migliore = (s[0], s[1], i)
        elif migliore is not None and s is not None:
            break
    return (migliore[1], migliore[2]) if migliore else None


def cerca_libera(punti, flat, flon, kx):
    """Come lo script 90: il segmento piu' vicino in tutta la corsa, entro 60 m."""
    migliore = None
    for i in range(len(punti) - 1):
        s = _segmento(punti, i, flat, flon, kx)
        if s is not None and (migliore is None or s[0] < migliore[0]):
            migliore = s
    return migliore[1] if migliore and migliore[0] <= DIST_GPS_M else None


def passaggi_corsa(punti, fermate_corsa, sched_base, fermate, libera=False):
    """Per ogni fermata della corsa (ordinata per stop_sequence) il passaggio GPS valido: {seq: istante}."""
    out = {}
    t_prec, i0 = -1e18, 0
    for seq, sec, stop in fermate_corsa:
        info = fermate.get(stop)
        if not info:
            continue
        flat, flon = info[1], info[2]
        kx = 111320.0 * math.cos(math.radians(flat))
        sched = sched_base + sec
        if libera:
            t = cerca_libera(punti, flat, flon, kx)
            idx = None
        else:
            r = cerca_vincolata(punti, flat, flon, kx, t_prec, i0)
            t, idx = r if r else (None, None)
        if t is None or abs(t - sched) / 60.0 > MAX_RITARDO_VERO_MIN:
            continue
        out[seq] = t
        if not libera:
            t_prec, i0 = t, idx
    return out


# ---------- aggregati ----------

class Acc:
    """Puntualita' (citta', modo, linea, fascia) e regolarita' (citta', linea) di un insieme di passaggi."""

    def __init__(self):
        self.citta = m27.agg_punt()
        self.modo = defaultdict(m27.agg_punt)
        self.linea = defaultdict(m27.agg_punt)
        self.fascia = defaultdict(m27.agg_punt)
        self.reg_citta = m27.agg_reg()
        self.reg_linea = defaultdict(m27.agg_reg)

    def aggiungi(self, passaggi, modo_linea):
        for pg in passaggi:
            rit = pg[P_RIT]
            m27.conta_punt(self.citta, rit)
            m27.conta_punt(self.modo[modo_linea.get(pg[P_LINEA], "bus")], rit)
            m27.conta_punt(self.linea[pg[P_LINEA]], rit)
            m27.conta_punt(self.fascia[pg[P_FASCIA]], rit)
        coppie, per_linea, _es = m27.regolarita(passaggi, "0")
        for i in range(4):
            self.reg_citta[i] += coppie[i]
        for (_t, linea), a in per_linea.items():
            for i in range(4):
                self.reg_linea[linea][i] += a[i]

    def reg_modo(self, modo_linea):
        out = defaultdict(m27.agg_reg)
        for linea, a in self.reg_linea.items():
            for i in range(4):
                out[modo_linea.get(linea, "bus")][i] += a[i]
        return out

    def punt(self, modo=None):
        return self.citta if modo is None else self.modo.get(modo, m27.agg_punt())

    def reg(self, modo_linea, modo=None):
        return self.reg_citta if modo is None else self.reg_modo(modo_linea).get(modo, m27.agg_reg())


def riga_punt(nome, a, r):
    s = m27.stat_punt(a)
    g = m27.stat_reg(r)
    return (f"{nome:24} | {s['passaggi']:8} | {s['anticipo']:6.1f} | {s['ritardo']:6.1f} | {s['ritardo10']:6.2f} | "
            f"{s['mediana']:7} | {g['coppie']:7} | {g['grappolo']:6.1f} | {g['buco']:5.1f} | {round(g['grappolo'] + g['buco'], 1):6}")


INTEST = ("insieme                  | passaggi | %antic | %>5min | %>10min | mediana | coppie  | %grapp | %buco | grap+buco"
          .replace("%>10min |", "%>10 |"))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    c = comuni.Controlli()
    trip_info, nome_linea, prog, modo_linea, ultima_seq, _km = m27.carica_gtfs()
    servizio, cal, eccezioni, fermate = m70.carica_calendario()
    con = sqlite3.connect(f"file:{m27.DB}?mode=ro", uri=True, timeout=60)

    n_feriali = sum(1 for (g,) in con.execute("SELECT DISTINCT start_date FROM trip_update_gtt")
                    if m27.tipo_giorno_data(datetime.strptime(g, "%Y%m%d").date()) == 0)
    soglia_classifica = max(1, round(MIN_PASSAGGI_CLASSIFICA_RIF * len(GIORNI) / n_feriali))

    acc = {k: Acc() for k in ("feed_oggi", "gps_tutti", "feed_stessi", "gps_stessi")}
    cop_linea = defaultdict(lambda: [0, 0])          # linea -> [passaggi programmati delle corse viste, con GPS valido]
    corse_linea = defaultdict(lambda: [0, 0])        # linea -> [corse programmate attive, viste nel GPS]
    prima_fermata = []
    diff_feed_gps = []                               # (b): feed - GPS, minuti, ultima lettura vicina all'arrivo
    diff_stessi = []                                 # feed - GPS su tutti gli stessi passaggi
    crescenti = [0, 0]                               # coppie di fermate consecutive: [non decrescenti, totali]
    accordo = [0, 0]                                 # ricerca vincolata = libera: [uguali entro 1 s, confrontati]
    stato_feed = {"usato": 0, "scartato D3": 0, "assente": 0}
    stato_feed_modo = {m: {"usato": 0, "scartato D3": 0, "assente": 0} for m in MODI}
    per_giorno = {}

    for giorno in GIORNI:
        t_inizio = time.perf_counter()
        data = datetime.strptime(giorno, "%Y%m%d").date()
        c(f"{giorno} e' un giorno feriale", m27.tipo_giorno_data(data) == 0, bloccante=True)
        mezz = m70.mezzanotte_utc(giorno)
        base = mezz.timestamp()
        finestra = (base + 2 * 3600, base + 26 * 3600)
        print(f"giorno {giorno}: feed...", file=sys.stderr)
        ultimo = m27.leggi_giorno(con, giorno)
        feed, fuori = m90.passaggi_con_scartati(ultimo, giorno, trip_info, nome_linea, prog)
        del ultimo
        feed_chiave = {(p["tid"], p["seq"]): p for p in feed}
        del feed

        print(f"giorno {giorno}: GPS...", file=sys.stderr)
        pos = defaultdict(list)
        righe = 0
        da, a = mezz + timedelta(hours=2), mezz + timedelta(hours=26)
        for corsa, ts, lat, lng in con.execute(
                "SELECT corsa, ts_feed, lat, lng FROM mezzi_gtt WHERE letto_utc BETWEEN ? AND ?",
                (da.isoformat(), a.isoformat())):
            righe += 1
            if corsa and ts and lat and lng:
                pos[corsa].append((ts, lat, lng))
        corse_gps = [t for t in pos if t in trip_info]
        corse_set = set(corse_gps)
        fuori_gtfs_gps = len(pos) - len(corse_gps)
        stops_corsa = defaultdict(list)
        for (tid, seq), (sec, stop) in prog.items():
            if tid in corse_set:
                stops_corsa[tid].append((seq, sec, stop))

        attivi = m70.servizi_attivi(giorno, cal, eccezioni)
        for tid, (route, _d) in trip_info.items():
            if servizio.get(tid) in attivi:
                cl = corse_linea[nome_linea.get(route, route)]
                cl[0] += 1
                cl[1] += tid in corse_set and len(pos[tid]) >= 2

        gps_p, feed_oggi_p, gps_st_p, feed_st_p = [], [], [], []
        fascia_cache = {}
        n_prog = n_valid = 0
        for k, tid in enumerate(corse_gps):
            punti = sorted(set(pos[tid]))
            if len(punti) < 2:
                continue
            fermate_c = sorted(stops_corsa[tid])
            route, direzione = trip_info[tid]
            linea = nome_linea.get(route, route)
            modo = modo_linea.get(linea, "bus")
            trovati = passaggi_corsa(punti, fermate_c, base, fermate)
            for seq, sec, stop in fermate_c:
                if finestra[0] <= base + sec <= finestra[1]:
                    n_prog += 1
                    cop_linea[linea][0] += 1
                    cop_linea[linea][1] += seq in trovati
            if k % CAMPIONE_CRESCENTI == 0:
                libera = passaggi_corsa(punti, fermate_c, base, fermate, libera=True)
                tempi = [libera[s] for s, _sec, _st in fermate_c if s in libera]
                crescenti[0] += sum(1 for x, y in zip(tempi, tempi[1:]) if y >= x)
                crescenti[1] += max(0, len(tempi) - 1)
                for s, t in trovati.items():
                    if s in libera:
                        accordo[1] += 1
                        accordo[0] += abs(libera[s] - t) <= 1.0
            if trovati and fermate_c[0][0] in trovati:
                prima_fermata.append((trovati[fermate_c[0][0]] - (base + fermate_c[0][1])) / 60.0)
            for seq, sec, stop in fermate_c:
                if seq not in trovati:
                    continue
                n_valid += 1
                sched = base + sec
                t = trovati[seq]
                rit = (t - sched) / 60.0
                h = int(sched) // 3600
                if h not in fascia_cache:
                    fascia_cache[h] = m27.fascia_oraria(m27.a_roma(datetime.fromtimestamp(sched, timezone.utc)).hour)
                tup = (linea, direzione, stop, sched, t, rit, fascia_cache[h], seq, "gps", tid)
                gps_p.append(tup)
                f = feed_chiave.get((tid, seq))
                if f is None:
                    stato = "assente"
                elif f["g"] == "C":
                    stato = "scartato D3"
                else:
                    stato = "usato"
                stato_feed[stato] += 1
                if modo in stato_feed_modo:
                    stato_feed_modo[modo][stato] += 1
                if stato == "usato":
                    gps_st_p.append(tup)
                    feed_st_p.append((linea, direzione, stop, sched, f["est"], f["rit"], fascia_cache[h], seq, "feed", tid))
                    diff_stessi.append((f["est"] - t) / 60.0)
                    if abs(f["letto"] - f["est"]) <= LETTURA_VICINA_S:
                        diff_feed_gps.append((f["est"] - t) / 60.0)
        del pos, stops_corsa
        # feed oggi: tutti i passaggi usati dallo script 27 (non solo quelli con GPS)
        for p in feed_chiave.values():
            if p["g"] != "C":
                s = p["sched"]
                h = int(s) // 3600
                if h not in fascia_cache:
                    fascia_cache[h] = m27.fascia_oraria(m27.a_roma(datetime.fromtimestamp(s, timezone.utc)).hour)
                feed_oggi_p.append((p["linea"], trip_info[p["tid"]][1], p["stop"], s, p["est"], p["rit"], fascia_cache[h], p["seq"], "feed", p["tid"]))
        del feed_chiave

        acc["gps_tutti"].aggiungi(gps_p, modo_linea)
        acc["feed_oggi"].aggiungi(feed_oggi_p, modo_linea)
        acc["gps_stessi"].aggiungi(gps_st_p, modo_linea)
        acc["feed_stessi"].aggiungi(feed_st_p, modo_linea)
        per_giorno[giorno] = {"righe_gps": righe, "corse_gps": len(corse_gps), "corse_gps_fuori_gtfs": fuori_gtfs_gps,
                              "passaggi_programmati": n_prog, "passaggi_gps": n_valid,
                              "passaggi_feed_usati": len(feed_oggi_p), "secondi": round(time.perf_counter() - t_inizio, 1)}
        print(f"giorno {giorno}: {n_valid} passaggi GPS su {n_prog} programmati, "
              f"{per_giorno[giorno]['secondi']} s", file=sys.stderr)
        del gps_p, feed_oggi_p, gps_st_p, feed_st_p
    con.close()

    # ---------- controlli ----------
    print("CONTROLLI")
    n_prog_tot = sum(d["passaggi_programmati"] for d in per_giorno.values())
    n_gps_tot = sum(d["passaggi_gps"] for d in per_giorno.values())
    c("ci sono passaggi GPS in entrambi i giorni", all(d["passaggi_gps"] > 0 for d in per_giorno.values()), bloccante=True)
    cop = 100.0 * n_gps_tot / n_prog_tot if n_prog_tot else 0.0
    c(f"(a) copertura GPS sopra {COPERTURA_MIN_PCT:.0f}% dei passaggi programmati delle corse viste", cop > COPERTURA_MIN_PCT,
      dettaglio=f"{cop:.1f}% ({n_gps_tot} su {n_prog_tot}); " + ", ".join(
          f"{g}: {100.0 * d['passaggi_gps'] / d['passaggi_programmati']:.1f}%" for g, d in per_giorno.items()))
    med_b = m27.mediana(diff_feed_gps)
    c(f"(b) differenza mediana feed - GPS entro +-{MAX_DIFF_FEED_GPS_MIN:g} min (ultima lettura a meno di 2 min dall'arrivo)",
      bool(diff_feed_gps) and abs(med_b) <= MAX_DIFF_FEED_GPS_MIN,
      dettaglio=f"{med_b} min su {len(diff_feed_gps)} passaggi; sugli stessi passaggi senza il filtro delle letture vicine: "
                f"{m27.mediana(diff_stessi)} min su {len(diff_stessi)}")
    pc = 100.0 * crescenti[0] / crescenti[1] if crescenti[1] else 0.0
    c(f"(c) tempi GPS non decrescenti lungo la corsa per oltre {MIN_CRESCENTI_PCT:g}% delle coppie di fermate "
      f"(ricerca libera, 1 corsa ogni {CAMPIONE_CRESCENTI})", pc > MIN_CRESCENTI_PCT,
      dettaglio=f"{pc:.2f}% ({crescenti[0]} su {crescenti[1]}); la ricerca ordinata li rende non decrescenti per costruzione; "
                f"ricerca ordinata = libera (entro 1 s) nel {100.0 * accordo[0] / accordo[1]:.1f}% dei {accordo[1]} passaggi confrontati"
                if accordo[1] else "")
    mp = m27.mediana(prima_fermata)
    c(f"(d) ritardo alla prima fermata della corsa: mediana fra {PRIMA_FERMATA_MIN[0]:g} e +{PRIMA_FERMATA_MIN[1]:g} min",
      bool(prima_fermata) and PRIMA_FERMATA_MIN[0] <= mp <= PRIMA_FERMATA_MIN[1],
      dettaglio=f"{mp} min su {len(prima_fermata)} corse")
    ng = [d["passaggi_gps"] for d in per_giorno.values()]
    c(f"(e) passaggi GPS dei due giorni simili (differenza entro {MAX_SCARTO_GIORNI * 100:.0f}% del maggiore)",
      min(ng) >= (1 - MAX_SCARTO_GIORNI) * max(ng), dettaglio=", ".join(f"{g}: {d['passaggi_gps']}" for g, d in per_giorno.items()))
    c("passaggi nel confronto 'stessi' uguali per feed e GPS",
      acc["feed_stessi"].citta[0] == acc["gps_stessi"].citta[0], bloccante=True,
      dettaglio=f"{acc['feed_stessi'].citta[0]}")
    for k, a in acc.items():
        n = a.citta[0]
        somma = a.modo["tram"][0] + a.modo["bus"][0] + a.modo.get("metro", [0])[0]
        c(f"{k}: passaggi tram + bus + metro = citta'", somma == n, bloccante=True, dettaglio=f"{somma} contro {n}")
        c(f"{k}: oltre 10 minuti <= oltre 5 minuti", a.citta[5] <= a.citta[3], bloccante=True)
        s = m27.stat_punt(a.citta)
        c(f"{k}: mediana plausibile fra -5 e +10 min", -5 <= s["mediana"] <= 10, dettaglio=f"{s['mediana']} min")

    # ---------- rapporto ----------
    R = ["RAPPORTO R4 - PROVA DEL CALCOLO SUL GPS (script 91, solo lettura)", "=" * 70,
         f"Giorni feriali: {', '.join(GIORNI)}. GPS valido: stessa corsa a meno di {DIST_GPS_M:.0f} m dalla fermata, segmenti di "
         f"non piu' di {SEGMENTO_MAX_S} s, fermate in ordine di stop_sequence con passaggio dopo quello della fermata prima, "
         f"|ritardo| <= {MAX_RITARDO_VERO_MIN:.0f} min. Finestra GPS come lo script 70 (dalle 02:00 locali di ogni giorno a 26 ore).",
         f"Soglia classifiche: {soglia_classifica} passaggi nei 2 giorni (= {MIN_PASSAGGI_CLASSIFICA_RIF} dello script 27 "
         f"x 2 giorni / {n_feriali} giorni feriali nel feed). Coppie di regolarita': stesse regole D6-D7 dello script 27.", ""]
    R.append("COPERTURA DEL GPS")
    R.append("giorno | righe GPS | corse GPS | corse fuori GTFS | passaggi programmati | con GPS valido | copertura | feed usati | secondi")
    for g, d in per_giorno.items():
        R.append(f"{g} | {d['righe_gps']:9} | {d['corse_gps']:9} | {d['corse_gps_fuori_gtfs']:16} | {d['passaggi_programmati']:20} "
                 f"| {d['passaggi_gps']:14} | {100.0 * d['passaggi_gps'] / d['passaggi_programmati']:8.1f}% | {d['passaggi_feed_usati']:10} | {d['secondi']}")
    R.append(f"totale: {n_gps_tot} passaggi GPS su {n_prog_tot} programmati delle corse viste ({cop:.1f}%)")
    R.append("")
    R.append("Dei passaggi con GPS valido, il feed (D3) ha: " + "; ".join(
        f"{k} {v} ({100.0 * v / max(1, n_gps_tot):.1f}%)" for k, v in stato_feed.items()))
    for m in MODI:
        tot = sum(stato_feed_modo[m].values())
        R.append(f"  {m}: " + "; ".join(f"{k} {v} ({100.0 * v / max(1, tot):.1f}%)" for k, v in stato_feed_modo[m].items()))
    R.append("")
    R.append("FEED CONTRO GPS (feriale, 2 giorni)")
    R.append("feed oggi = passaggi usati dallo script 27; stessi = solo passaggi che hanno sia GPS valido sia feed usato; "
             "GPS tutti = tutti i passaggi con GPS valido (anche scartati o assenti nel feed)")
    for titolo, modo in (("CITTA'", None), ("TRAM", "tram"), ("BUS", "bus")):
        R.append(titolo)
        R.append(INTEST)
        for k, nome in (("feed_oggi", "feed oggi (tutti usati)"), ("feed_stessi", "feed, stessi passaggi"),
                        ("gps_stessi", "GPS, stessi passaggi"), ("gps_tutti", "GPS, tutti")):
            R.append(riga_punt(nome, acc[k].punt(modo), acc[k].reg(modo_linea, modo)))
        R.append("")
    R.append("FASCE ORARIE (feriale): % oltre 5 minuti, feed oggi contro GPS tutti")
    R.append("fascia         | feed: passaggi | feed %>5 | feed mediana | GPS: passaggi | GPS %>5 | GPS %>10 | GPS mediana")
    for f in FASCE:
        a, b = acc["feed_oggi"].fascia.get(f), acc["gps_tutti"].fascia.get(f)
        if a and b and a[0] and b[0]:
            sa, sb = m27.stat_punt(a), m27.stat_punt(b)
            R.append(f"{f:14} | {sa['passaggi']:14} | {sa['ritardo']:8} | {sa['mediana']:12} | {sb['passaggi']:13} | {sb['ritardo']:7} "
                     f"| {sb['ritardo10']:8} | {sb['mediana']}")
    R.append("")

    # classifica linee peggiori col GPS, con la posizione col feed
    ordinarie = lambda a: {l: v for l, v in a.items() if m27.linea_ordinaria(l) and v[0] >= soglia_classifica}
    gl, fl = ordinarie(acc["gps_tutti"].linea), ordinarie(acc["feed_oggi"].linea)
    ord_gps = sorted(gl, key=lambda l: (-m27.pct(gl[l][3], gl[l][0]), l))
    ord_feed = sorted(fl, key=lambda l: (-m27.pct(fl[l][3], fl[l][0]), l))
    pos_feed = {l: i + 1 for i, l in enumerate(ord_feed)}
    R.append(f"10 LINEE PEGGIORI PER % IN RITARDO OLTRE 5 MINUTI COL GPS (feriale, linee ordinarie, >= {soglia_classifica} passaggi nei 2 giorni)")
    R.append("pos | linea | modo | GPS %>5 | GPS %>10 | GPS mediana | passaggi GPS | feed %>5 | passaggi feed | posizione col feed")
    for i, l in enumerate(ord_gps[:10], 1):
        s = m27.stat_punt(gl[l])
        f = fl.get(l)
        sf = m27.stat_punt(f) if f else None
        R.append(f"{i:3} | {l:5} | {modo_linea.get(l, 'bus'):4} | {s['ritardo']:7} | {s['ritardo10']:8} | {s['mediana']:11} | {s['passaggi']:12} "
                 f"| {sf['ritardo'] if sf else '-':>8} | {sf['passaggi'] if sf else '-':>13} | {pos_feed.get(l, '-')} su {len(ord_feed)}")
    R.append("")

    # copertura per linea
    cl = [(100.0 * v[1] / v[0], l, v) for l, v in cop_linea.items() if v[0] >= MIN_PASSAGGI_PROG_COPERTURA and m27.linea_ordinaria(l)]
    cl.sort()
    R.append(f"10 LINEE CON LA COPERTURA GPS PIU' BASSA (linee ordinarie, >= {MIN_PASSAGGI_PROG_COPERTURA} passaggi programmati delle corse viste)")
    R.append("linea | modo | copertura | passaggi programmati | con GPS | corse programmate (2 giorni) | corse viste nel GPS")
    for pct_, l, v in cl[:10]:
        k = corse_linea.get(l, [0, 0])
        R.append(f"{l:5} | {modo_linea.get(l, 'bus'):4} | {pct_:8.1f}% | {v[0]:20} | {v[1]:7} | {k[0]:28} | {k[1]}")
    quote_cop = [p for p, _l, _v in cl]
    if quote_cop:
        R.append(f"copertura per linea ordinaria: mediana {m27.mediana(quote_cop)}%, minima {min(quote_cop):.1f}%, "
                 f"{sum(q < COPERTURA_MIN_PCT for q in quote_cop)} linee su {len(quote_cop)} sotto {COPERTURA_MIN_PCT:.0f}%")
    tot_cp = sum(v[0] for v in corse_linea.values())
    tot_cv = sum(v[1] for v in corse_linea.values())
    R.append(f"corse programmate attive nei 2 giorni: {tot_cp}; viste nel GPS con almeno 2 posizioni: {tot_cv} ({100.0 * tot_cv / max(1, tot_cp):.1f}%)")
    R.append("")
    R += ["CONTROLLI"] + ["  " + x for x in c.righe]
    R += ["", "Letture: prova su 2 giorni, solo ordine di grandezza; il feed oggi e' quello dello script 27 (non cambia). "
          "Il giro completo su tutti i giorni (Giro 5) si scrive dopo la lettura di questa prova.", ""]
    testo = "\n".join(R) + "\n"
    RAPPORTO.write_text(testo, encoding="utf-8")

    def js(a, r_):
        return {"punt": m27.stat_punt(a), "reg": m27.stat_reg(r_)}
    out = {"generato": datetime.now().astimezone().isoformat(timespec="seconds"), "tag": "MISURATO-PROVA", "giorni": list(GIORNI),
           "parametri": {"dist_gps_m": DIST_GPS_M, "segmento_max_s": SEGMENTO_MAX_S, "max_ritardo_vero_min": MAX_RITARDO_VERO_MIN,
                         "soglia_classifica": soglia_classifica},
           "per_giorno": per_giorno, "copertura_pct": round(cop, 1), "stato_feed": stato_feed,
           "confronto": {k: {"citta": js(a.citta, a.reg_citta),
                             **{m: js(a.punt(m), a.reg(modo_linea, m)) for m in MODI}} for k, a in acc.items()},
           "controlli": c.righe}
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(testo)
    print(f"Scritti {OUT_JSON.relative_to(RADICE)} e {RAPPORTO.relative_to(RADICE)}; avvisi: {len(c.avvisi())}")


if __name__ == "__main__":
    main()
