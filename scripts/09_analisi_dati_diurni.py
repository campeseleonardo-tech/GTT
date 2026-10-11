#!/usr/bin/env python3
"""09_analisi_dati_diurni.py

Analisi in SOLA LETTURA di data/storico.sqlite (non scrive mai sul database):

1. Controlli di base: schema, intervallo temporale, snapshot, duplicati, NULL.
2. Flussi 5T: copertura per giorno/tipo di giorno/ora locale, quota di
   flusso=0 / >0 / NULL e velocita' NULL, distribuzioni senza mescolare i
   dati mancanti con gli zeri reali, copertura per sensore e per strada+direzione.
   L'accuratezza non e' salvata con le misure (solo l'ultimo stato per sensore
   in sensori_5t): NON viene usata per classificare il passato.
3. Mezzi GTT: veicoli DISTINTI per snapshot, ora locale, tipo di giorno e
   linea; buchi temporali; snapshot ripetuti; ore di punta osservate.
   Il conteggio misura i mezzi localizzati, non necessariamente l'intera flotta.

Output:
- console;
- docs/RAPPORTO_ANALISI_5T.txt  (rapporto sintetico, valori dell'ultima esecuzione);
- data/processed/analisi_5t.json (aggregati riutilizzabili).

Solo libreria standard. Ore locali Europe/Rome calcolate a mano (niente zoneinfo
su Windows): CET = UTC+1, CEST = UTC+2; DST dall'ultima domenica di marzo
01:00 UTC all'ultima domenica di ottobre 01:00 UTC (regola UE).

A differenza delle vecchie versioni 09/10: qui non si cerca accuracy su
flussi_5t (colonna inesistente) e non si uniscono i flussi passati
all'accuratezza attuale del sensore (sarebbe fuorviante).
"""

import argparse
import json
import sqlite3
import statistics
import sys
from calendar import monthrange
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RAD = Path(__file__).resolve().parents[1]
# sul PC si legge la copia settimanale dal Pi; se manca, il vecchio storico locale
DB = RAD / "data" / "storico_backup.sqlite"
if not DB.is_file():
    DB = RAD / "data" / "storico.sqlite"
RAPPORTO = RAD / "docs" / "RAPPORTO_ANALISI_5T.txt"
JSON_OUT = RAD / "data" / "processed" / "analisi_5t.json"

PERIODO_5T_MIN = 5       # i feed 5T sono aggiornati ogni 5 minuti
SNAPSHOT_ATTESI_GIORNO = 24 * 60 // PERIODO_5T_MIN   # 288
SNAPSHOT_ATTESI_ORA = 60 // PERIODO_5T_MIN           # 12
GAP_5T_MIN = 6           # buco "anomalo" nei 5T: > 6 minuti
GAP_MEZZI_SEC = 90       # buco "anomalo" nei mezzi: > 90 secondi

RIGHE = []  # testo del rapporto, riusato per console e file


def scrivi(msg=""):
    RIGHE.append(str(msg))


def stampa_rapporto():
    testo = "\n".join(RIGHE) + "\n"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.write(testo)
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text(testo, encoding="utf-8")
    print(f"\nRapporto salvato: {RAPPORTO}")


# ---------- ora locale Europe/Rome (senza zoneinfo) ----------

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


def parsa_utc(s):
    """Timestamp ISO (con Z o +00:00, con o senza millisecondi) -> datetime UTC."""
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def tipo_giorno(d):
    return {5: "sabato", 6: "domenica"}.get(d.weekday(), "feriale")


# ---------- database ----------

def apri_db(percorso):
    if not percorso.is_file():
        raise SystemExit(f"DB non trovato: {percorso}")
    con = sqlite3.connect(f"file:{percorso}?mode=ro", uri=True, timeout=60)
    con.execute("PRAGMA busy_timeout=60000")
    return con


def controllo_conteggi(cur, tabella, righe_script):
    """Conteggio grezzo SQL vs. conteggio dello script: devono coincidere."""
    n_sql = cur.execute(f"SELECT COUNT(*) FROM {tabella}").fetchone()[0]
    n_script = len(righe_script)
    esito = "OK" if n_sql == n_script else "DIVERSO!"
    scrivi(f"  controllo conteggio {tabella}: SQL={n_sql}  script={n_script}  {esito}")
    return n_sql


# ---------- analisi 5T ----------

def analizza_5t(cur):
    scrivi("\n" + "=" * 72)
    scrivi("FLUSSI 5T  (storico non riscritto; accuratezza storica NON disponibile)")
    scrivi("=" * 72)

    cols5 = {c[1] for c in cur.execute("PRAGMA table_info(flussi_5t)")}
    if "accuratezza" in cols5 or "accuracy" in cols5:
        scrivi("  !! colonna di accuratezza presente in flussi_5t: non prevista dallo schema")

    righe = cur.execute("""
        SELECT f.generato_utc, f.lcd1, f.flusso, f.velocita, f.periodo_min,
               s.nome_strada, s.direzione
        FROM flussi_5t f LEFT JOIN sensori_5t s ON s.lcd1 = f.lcd1
        ORDER BY f.generato_utc, f.lcd1
    """).fetchall()
    n_tot = controllo_conteggi(cur, "flussi_5t", righe)
    if not n_tot:
        scrivi("  (nessun dato)")
        return {}

    # --- carica in memoria con timestamp UTC e locale ---
    dati = []   # (utc, locale, lcd1, flusso, velocita, strada, direzione)
    for generato, lcd1, flusso, vel, per, strada, dir_ in righe:
        utc = parsa_utc(generato)
        dati.append((utc, a_roma(utc), lcd1, flusso, vel,
                     strada or "(sconosciuta)", dir_ or "?"))

    # snapshot distinti: tag = generato_utc al secondo
    snap_tag = {}
    for utc, loc, *_ in dati:
        snap_tag.setdefault(utc.isoformat(timespec="seconds"), (utc, loc))
    n_snap = len(snap_tag)
    nsens = len({r[2] for r in dati})

    loc_min = min(r[1] for r in dati)
    loc_max = max(r[1] for r in dati)
    scrivi(f"  righe totali: {n_tot}")
    scrivi(f"  snapshot distinti (generato_utc): {n_snap}")
    scrivi(f"  sensori distinti: {nsens}")
    scrivi(f"  intervallo UTC:  {min(r[0] for r in dati).isoformat()} -> {max(r[0] for r in dati).isoformat()}")
    scrivi(f"  intervallo ora locale: {loc_min.isoformat()} -> {loc_max.isoformat()}")
    dup = n_tot - len({(r[0].isoformat(timespec="seconds"), r[2]) for r in dati})
    scrivi(f"  duplicati (generato_utc,lcd1): {dup}")
    scrivi(f"  periodo_min valori: {sorted({r[4] for r in righe})}")

    # --- copertura per giorno locale ---
    scrivi("\n-- Copertura per giorno locale (atteso nella finestra = 1 snapshot ogni 5 min) --")
    per_giorno_snap = {}
    for tag, (utc, loc) in snap_tag.items():
        per_giorno_snap.setdefault(loc.date(), []).append((utc, loc))
    tab_giorni = []
    for d in sorted(per_giorno_snap):
        lista = sorted(per_giorno_snap[d])
        primo, ultimo = lista[0][1], lista[-1][1]
        finestra = int((ultimo - primo).total_seconds() // 300) + 1
        obs = len(lista)
        buchi = []
        prev = None
        for _, loc in lista:
            if prev is not None:
                gm = (loc - prev).total_seconds() / 60
                if gm > GAP_5T_MIN:
                    buchi.append(round(gm, 1))
            prev = loc
        tipo = tipo_giorno(d)
        tab_giorni.append(dict(giorno=d.isoformat(), tipo=tipo, snapshot=obs,
                               attesi_finestra=finestra, buchi_gt6=buchi))
        scrivi(f"  {d} ({tipo:9s}) snapshot {obs:4d}/{finestra:3d} "
               f"({obs / finestra:5.1%})  buchi>6': {len(buchi)} "
               f"{buchi[:5]}{'...' if len(buchi) > 5 else ''}")

    # --- per tipo di giorno e ora locale ---
    per_ho = {}   # (tipo, ora) -> contatori con snapshot distinti
    for utc, loc, lcd1, flusso, vel, strada, dir_ in dati:
        k = (tipo_giorno(loc.date()), loc.hour)
        d = per_ho.setdefault(k, dict(snap=set(), n=0, f0=0, fp=0, vnull=0,
                                      flussi=[], vels=[]))
        d["snap"].add(utc.isoformat(timespec="seconds"))
        d["n"] += 1
        if flusso == 0:
            d["f0"] += 1
        elif flusso is not None and flusso > 0:
            d["fp"] += 1
        if flusso is None:
            d["vnull"] += 1
        if flusso is not None and flusso > 0:
            d["flussi"].append(flusso)
        if vel is not None:
            d["vels"].append(vel)

    giorni_tipo = {}
    for t in tab_giorni:
        giorni_tipo[t["tipo"]] = giorni_tipo.get(t["tipo"], 0) + 1

    scrivi("\n-- Per tipo di giorno e ora locale --")
    scrivi("   (coper. = snapshot osservati su 12 all'ora per ogni giorno presente del tipo;")
    scrivi("    giorni parziali o buchi della raccolta abbassano la copertura)")
    tab_ho = []
    for tipo in ("feriale", "sabato", "domenica"):
        if tipo not in giorni_tipo:
            scrivi(f"  -- {tipo}: nessun giorno --")
            continue
        nd = giorni_tipo[tipo]
        attesi_h = SNAPSHOT_ATTESI_ORA * nd
        scrivi(f"  -- {tipo} ({nd} giorno/i) --")
        for h in range(24):
            d = per_ho.get((tipo, h))
            if not d:
                scrivi(f"    {h:02d}:00  nessun dato")
                continue
            snap_osservati = len(d["snap"])
            med = statistics.median(d["flussi"]) if d["flussi"] else None
            fl_ord = sorted(d["flussi"])
            p95 = fl_ord[int(len(fl_ord) * 0.95)] if fl_ord else None
            medv = statistics.median(d["vels"]) if d["vels"] else None
            tab_ho.append(dict(tipo=tipo, ora=h, n=d["n"], snap=snap_osservati,
                               attesi=attesi_h, flusso0=d["f0"], flusso_pos=d["fp"],
                               mediana_flusso=med, p95_flusso=p95, vel_null=d["vnull"],
                               mediana_vel=medv))
            scrivi(f"    {h:02d}:00  misure {d['n']:5d}  snap {snap_osservati:3d}/{attesi_h:3d} "
                   f"({snap_osservati / attesi_h:5.1%})  zero {d['f0'] / d['n']:5.1%}  "
                   f">0 {d['fp'] / d['n']:5.1%}  med>0 {med or 0:6.1f}  p95>0 {p95 or 0:6.1f}  "
                   f"velNULL {d['vnull'] / d['n']:5.1%}  med_vel {medv or 0:5.1f}")

    # --- distribuzione globale (zeri reali separati da NULL; NULL assenti in 5T) ---
    n0 = sum(1 for r in dati if r[3] == 0)
    np = sum(1 for r in dati if r[3] is not None and r[3] > 0)
    nnull = sum(1 for r in dati if r[3] is None)
    flussi_pos = [r[3] for r in dati if r[3] is not None and r[3] > 0]
    vels = [r[4] for r in dati if r[4] is not None]
    vnull = n_tot - len(vels)
    scrivi("\n-- Distribuzione globale (denominatori espliciti) --")
    scrivi(f"  flusso=0:        {n0:7d} / {n_tot} ({n0 / n_tot:6.2%})")
    scrivi(f"  flusso>0:        {np:7d} / {n_tot} ({np / n_tot:6.2%})")
    scrivi(f"  flusso NULL:     {nnull:7d} / {n_tot} ({nnull / n_tot:6.2%})")
    scrivi(f"  velocita NULL:   {vnull:7d} / {n_tot} ({vnull / n_tot:6.2%})")
    if flussi_pos:
        q = statistics.quantiles(flussi_pos, n=4)
        scrivi(f"  flusso>0: mediana {statistics.median(flussi_pos):.1f}  "
               f"quartili [{q[1]:.1f}, {q[2]:.1f}]  max {max(flussi_pos):.1f}")
    if vels:
        scrivi(f"  velocita (non NULL): mediana {statistics.median(vels):.1f}  "
               f"media {statistics.mean(vels):.1f}  max {max(vels):.1f}")

    # --- copertura per sensore ---
    scrivi("\n-- Per sensore (copertura = snapshot in cui il sensore compare su tutti quelli osservati) --")
    per_sens = {}
    for _, loc, lcd1, flusso, vel, strada, dir_ in dati:
        d = per_sens.setdefault(lcd1, dict(strada=strada, dir=dir_, n=0, f0=0,
                                           fp=0, flussi=[], vels=[]))
        d["n"] += 1
        if flusso == 0:
            d["f0"] += 1
        elif flusso is not None and flusso > 0:
            d["fp"] += 1
        if flusso is not None and flusso > 0:
            d["flussi"].append(flusso)
        if vel is not None:
            d["vels"].append(vel)
    tab_sens = []
    sotto = 0
    for lcd1 in sorted(per_sens):
        d = per_sens[lcd1]
        cop = d["n"] / n_snap
        med = statistics.median(d["flussi"]) if d["flussi"] else None
        medv = statistics.median(d["vels"]) if d["vels"] else None
        tab_sens.append(dict(lcd1=lcd1, strada=d["strada"], direzione=d["dir"], n=d["n"],
                             copertura=round(cop, 4), flusso0=d["f0"], flusso_pos=d["fp"],
                             mediana_flusso=med, mediana_vel=medv))
        if cop < 1.0:
            sotto += 1
            scrivi(f"    {lcd1:>6} {d['strada'][:38]:38s} {d['dir']:8s} "
                   f"{d['n']:4d}/{n_snap} ({cop:5.1%})  zero {d['f0'] / d['n']:5.1%}")
    scrivi(f"  sensori sotto copertura: {sotto} su {len(per_sens)}")

    # --- sintesi per strada+direzione ---
    scrivi("\n-- Sintesi per strada + direzione (media (>0) tra sensori dello stesso tratto) --")
    per_strada = {}
    for d in per_sens.values():
        per_strada.setdefault((d["strada"], d["dir"]), []).append(d)
    tab_strada = []
    for (strada, dir_), lista in sorted(per_strada.items(), key=lambda kv: -len(kv[1])):
        medie = [statistics.mean(d["flussi"]) for d in lista if d["flussi"]]
        media = statistics.mean(medie) if medie else None
        tab_strada.append(dict(strada=strada, direzione=dir_, sensori=len(lista),
                               flusso_medio=media))
        if media is not None:
            scrivi(f"    {strada[:44]:44s} {dir_:8s} sensori {len(lista):2d}  "
                   f"flusso medio (>0) {media:.1f}")
        else:
            scrivi(f"    {strada[:44]:44s} {dir_:8s} sensori {len(lista):2d}  (sempre 0 o NULL)")

    return dict(n_tot=n_tot, n_snap=n_snap, sensori_distinti=nsens, giorni=tab_giorni,
                per_ora=tab_ho, sensori=tab_sens, stradadirezione=tab_strada)


# ---------- analisi mezzi GTT ----------

def analizza_mezzi(cur):
    scrivi("\n" + "=" * 72)
    scrivi("MEZZI GTT  (vehicle_position; conta veicoli DISTINTI, non righe)")
    scrivi("=" * 72)

    righe = cur.execute("""
        SELECT letto_utc, veicolo, linea FROM mezzi_gtt ORDER BY letto_utc
    """).fetchall()
    n_tot = controllo_conteggi(cur, "mezzi_gtt", righe)
    if not n_tot:
        scrivi("  (nessun dato)")
        return {}

    duplicati = n_tot - len({(r[0], r[1]) for r in righe})
    vuoti = sum(1 for r in righe if not r[1] or not r[2])
    scrivi(f"  righe: {n_tot}   duplicati (letto_utc,veicolo): {duplicati}   "
           f"righe con veicolo/linea vuoti: {vuoti}")

    # per snapshot: righe, veicoli distinti, linee, ora locale
    snap = {}   # tag -> dict(righe=0, veicoli=set, linee=set, loc)
    for letto, veicolo, linea in righe:
        utc = parsa_utc(letto)
        tag = utc.isoformat(timespec="seconds")
        d = snap.setdefault(tag, dict(righe=0, veicoli=set(), linee=set(), loc=a_roma(utc)))
        d["righe"] += 1
        d["veicoli"].add(veicolo)
        d["linee"].add(linea)

    n_snap = len(snap)
    vpersnap = [len(d["veicoli"]) for d in snap.values()]
    media_occup = sum(vpersnap) / n_snap
    scrivi(f"  snapshot distinti (letto_utc): {n_snap}")
    scrivi(f"  veicoli distinti per snapshot: minimo {min(vpersnap)}  "
           f"mediana {statistics.median(vpersnap)}  media {media_occup:.1f}  "
           f"massimo {max(vpersnap)}")
    scrivi(f"  NOTA: ~{media_occup:.0f} mezzi localizzati per snapshot e' il volume del FEED,"
           "\n        non necessariamente l'intera flotta in servizio.")

    lista = sorted(snap.items())
    buchi = []
    for (_, d1), (_, d2) in zip(lista, lista[1:]):
        sec = (d2["loc"] - d1["loc"]).total_seconds()
        if sec > GAP_MEZZI_SEC:
            buchi.append((d1["loc"], d2["loc"], round(sec / 60, 1)))
    scrivi(f"  buchi > {GAP_MEZZI_SEC} s: {len(buchi)}")
    for p, c, m in buchi[:12]:
        scrivi(f"    {p.isoformat(timespec='minutes')} -> {c.isoformat(timespec='minutes')}  {m} min")
    if len(buchi) > 12:
        scrivi(f"    ... altre {len(buchi) - 12}")

    povere = {k: len(d["veicoli"]) for k, d in snap.items() if len(d["veicoli"]) < 50}
    scrivi(f"  snapshot con < 50 veicoli distinti: {len(povere)} su {n_snap}")
    for k, nv in sorted(povere.items(), key=lambda kv: kv[1])[:10]:
        scrivi(f"    {k}  veicoli distinti {nv}")

    # per tipo di giorno + ora: media dei veicoli distinti per snapshot
    per_ho = {}   # (tipo, ora) -> [somma veicoli distinti, n snapshot, righe, union veicoli, union linee]
    for tag, d in snap.items():
        loc = d["loc"]
        k = (tipo_giorno(loc.date()), loc.hour)
        a = per_ho.setdefault(k, [0, 0, 0, set(), set()])
        a[0] += len(d["veicoli"])
        a[1] += 1
        a[2] += d["righe"]
        a[3] |= d["veicoli"]
        a[4] |= d["linee"]

    giorni_tipo = {}
    for d in snap.values():
        t = tipo_giorno(d["loc"].date())
        giorni_tipo.setdefault(t, set()).add(d["loc"].date())
    giorni_tipo = {k: len(v) for k, v in giorni_tipo.items()}

    scrivi("\n-- Per tipo di giorno e ora locale (media dei veicoli distinti per snapshot) --")
    tab_ho = []
    punte = {}
    for tipo in ("feriale", "sabato", "domenica"):
        if tipo not in giorni_tipo:
            scrivi(f"  -- {tipo}: nessun giorno --")
            continue
        scrivi(f"  -- {tipo} ({giorni_tipo[tipo]} giorno/i) --")
        best = None
        for h in range(24):
            a = per_ho.get((tipo, h))
            if not a:
                continue
            somma, ns, righe_h, vuni, luni = a
            media = somma / ns if ns else 0
            tab_ho.append(dict(tipo=tipo, ora=h, righe=righe_h, snapshot=ns,
                               veicoli_union=len(vuni),
                               media_veicoli_snapshot=round(media, 1),
                               linee_distinte=len(luni)))
            scrivi(f"    {h:02d}:00  righe {righe_h:6d}  snap {ns:4d}  "
                   f"media veicoli/snap {media:6.1f}  veicoli union {len(vuni):3d}  "
                   f"linee {len(luni):3d}")
            if best is None or media > best[0]:
                best = (media, h)
        if best:
            punte[tipo] = best[1]
            scrivi(f"    -> punta osservata {tipo}: ora {best[1]:02d}:00 "
                   f"({best[0]:.1f} mezzi/snapshot)")

    # per linea: media dei veicoli distinti per snapshot nei momenti in cui compare
    per_linea_snap = {}   # (tag, linea) -> set(veicoli)
    for letto, veicolo, linea in righe:
        tag = parsa_utc(letto).isoformat(timespec="seconds")
        per_linea_snap.setdefault((tag, linea), set()).add(veicolo)
    per_linea = {}
    for (tag, linea), veicoli in per_linea_snap.items():
        d = per_linea.setdefault(linea, dict(n_snap=0, somma=0, veicoli=set()))
        d["n_snap"] += 1
        d["somma"] += len(veicoli)
        d["veicoli"] |= veicoli
    scrivi("\n-- Per linea (top 25 per media veicoli/snapshot nei momenti in cui compare) --")
    tab_linee = []
    for linea, d in sorted(per_linea.items(),
                           key=lambda kv: -(kv[1]["somma"] / kv[1]["n_snap"]))[:25]:
        media = d["somma"] / d["n_snap"]
        tab_linee.append(dict(linea=linea, snapshot_presente=d["n_snap"],
                              veicoli_distinti=len(d["veicoli"]),
                              media_snapshot=round(media, 2)))
        scrivi(f"    {linea:>4}  media {media:5.2f}/snap  n_snap {d['n_snap']:4d}  "
               f"veicoli dist. {len(d['veicoli']):3d}")

    scrivi("\n  NOTA: il conteggio misura i MEZZI LOCALIZZATI dal feed, non necessariamente")
    scrivi("        l'intera flotta in servizio (il feed non contiene il trip_id).")

    return dict(n_tot=n_tot, n_snap=n_snap, media_veicoli_snapshot=round(media_occup, 1),
                per_ora=tab_ho, linee=tab_linee, punte=punte,
                buchi=[(p.isoformat(), c.isoformat(), m) for p, c, m in buchi])


def main():
    ap = argparse.ArgumentParser(description="Analisi in sola lettura di storico.sqlite")
    ap.add_argument("--no-scritture", action="store_true",
                    help="non scrivere il rapporto e il JSON (solo console)")
    ap.add_argument("--db", default=None, help="percorso alternativo del database (per prove)")
    args = ap.parse_args()
    global DB, RAPPORTO, JSON_OUT
    if args.db:
        DB = Path(args.db)
        RAPPORTO = DB.parent / f"{DB.stem}_rapporto_5t.txt"
        JSON_OUT = DB.parent / f"{DB.stem}_analisi.json"

    con = apri_db(DB)
    cur = con.cursor()
    risultato = {}
    try:
        scrivi("DB (sola lettura): " + str(DB) + f"  ({DB.stat().st_size / 1e6:.1f} MB)")
        tabs = [r[0] for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY 1")]
        scrivi("Tabelle: " + ", ".join(tabs))
        if "flussi_5t" in tabs:
            risultato["5t"] = analizza_5t(cur)
        if "mezzi_gtt" in tabs:
            risultato["mezzi"] = analizza_mezzi(cur)
        if "sensori_5t" in tabs:
            n_sens = cur.execute("SELECT COUNT(*) FROM sensori_5t").fetchone()[0]
            n_acc0 = cur.execute(
                "SELECT COUNT(*) FROM sensori_5t WHERE accuratezza=0").fetchone()[0]
            scrivi("\n-- Fotografia attuale dei sensori (NON storica, NON usata per i flussi) --")
            scrivi(f"  sensori_5t: {n_sens} righe, accuratezza=0: {n_acc0} "
                   f"({n_acc0 / n_sens:5.1%})")
            risultato["sensori_attuali"] = dict(n=n_sens, accuratezza0=n_acc0)
        trip = [t for t in tabs
                if any(k in t.lower() for k in ("trip", "rit", "update"))]
        scrivi("\n-- Feed trip_update (ritardi): solo controllo di presenza, non analisi --")
        scrivi(f"  tabelle trip/ritardi/update: {trip if trip else '(nessuna: il feed non è raccolto)'}")
        risultato["trip_update_presente"] = bool(trip)
    finally:
        con.close()

    if not args.no_scritture:
        JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
        JSON_OUT.write_text(json.dumps(risultato, ensure_ascii=False, indent=1,
                                       default=str), encoding="utf-8")
        print(f"Aggregati salvati: {JSON_OUT}")
    stampa_rapporto()
    return 0


if __name__ == "__main__":
    sys.exit(main())