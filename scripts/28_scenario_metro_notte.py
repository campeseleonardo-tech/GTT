#!/usr/bin/env python3
"""Risultato 2 - scenario "metro anche nel buco notturno".

Genera due copie modificate del GTFS vero (data/raw/gtt_gtfs_20261003_224530.zip)
con corse FINte della metro M1 (route_id METROU) aggiunte solo nel buco
notturno reale del 12/10/2026 (feriale): tra le 00:50:00 e le 05:22:00.
Verificato sul GTFS vero: il bus sostitutivo M1SU arriva fino alle 00:50, la
prima corsa vera della metro (METROU) parte alle 05:22.

Per ciascun intervallo (15 e 30 minuti) scrive uno zip identico all'originale
tranne trips.txt, stop_times.txt e calendar_dates.txt, che contengono le righe
originali PIU' le righe nuove. Il servizio finto esiste solo il 12/10/2026
(riga in calendar_dates.txt, calendar.txt non viene toccato).

Output:
  data/scenari/gtt_gtfs_notte15.zip
  data/scenari/gtt_gtfs_notte30.zip

La logica dei service_id attivi e' copiata da scripts/calcola_simulazione.py
(funzione servizi_attivi), come richiesto.
"""
import csv
import io
import sys
import zipfile
from datetime import date
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
GTFS = RADICE / "data/raw/gtt_gtfs_20261003_224530.zip"
SCENARI = RADICE / "data/scenari"

GIORNO = date(2026, 10, 12)          # feriale di riferimento (lunedi')
PRIMA_PARTENZA = "00:50:00"          # ultima corsa del bus sostitutivo M1SU
FINE_BUCO = "05:22:00"               # prima corsa vera della metro (METROU)
INTERVALLI = [15, 30]                # minuti tra una corsa finta e la successiva


def log(msg):
    print(msg, flush=True)


# --- logica dei service_id attivi: copiata da scripts/calcola_simulazione.py ---
def data_gtfs(s):
    return date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def servizi_attivi(cal, eccezioni, d):
    giorni = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    attivi = set()
    for r in cal:
        if data_gtfs(r["start_date"]) <= d <= data_gtfs(r["end_date"]) and r[giorni[d.weekday()]] == "1":
            attivi.add(r["service_id"])
    for r in eccezioni:
        if data_gtfs(r["date"]) == d:
            if r["exception_type"] == "1":
                attivi.add(r["service_id"])
            elif r["exception_type"] == "2":
                attivi.discard(r["service_id"])
    return attivi


def secondi(hhmmss):
    """HH:MM:SS -> secondi dalla mezzanotte (accetta anche ore >= 24)."""
    h, m, s = hhmmss.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def orario(sec):
    """Secondi dalla mezzanotte -> HH:MM:SS su 24h."""
    return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"


def testo_righe(righe):
    """Righe CSV (senza intestazione) nello stesso stile del GTFS (tutti i campi
    tra virgolette, a capo LF)."""
    buf = io.StringIO()
    w = csv.writer(buf, quoting=csv.QUOTE_ALL, lineterminator="\n")
    for r in righe:
        w.writerow(r)
    return buf.getvalue()


def aggiungi_righe(raw, testo_nuovo):
    """Aggiunge le righe nuove in coda al file originale, senza toccare i byte
    originali (a parte un eventuale a capo finale mancante)."""
    out = raw
    if out and not out.endswith(b"\n"):
        out += b"\n"
    return out + testo_nuovo.encode("utf-8")


def leggi_stop_times_metro(z, metro_ids):
    """Una passata riga per riga su stop_times.txt: solo le sequenze delle corse
    metro (dict trip_id -> lista di righe)."""
    rd = z.open("stop_times.txt")
    lettore = csv.reader(io.TextIOWrapper(rd, encoding="utf-8-sig"))
    intest = next(lettore)
    i_tid = intest.index("trip_id")
    i_seq = intest.index("stop_sequence")
    i_arr = intest.index("arrival_time")
    i_dep = intest.index("departure_time")
    per_trip = {}
    for row in lettore:
        tid = row[i_tid]
        if tid in metro_ids:
            per_trip.setdefault(tid, []).append(row)
    return per_trip, intest, i_tid, i_seq, i_arr, i_dep


def main():
    if not GTFS.exists():
        sys.exit(f"GTFS non trovato: {GTFS}")

    z = zipfile.ZipFile(GTFS)
    nomi = z.namelist()

    cal = list(csv.DictReader(io.StringIO(z.read("calendar.txt").decode("utf-8-sig"))))
    ecc = list(csv.DictReader(io.StringIO(z.read("calendar_dates.txt").decode("utf-8-sig"))))
    attivi = servizi_attivi(cal, ecc, GIORNO)
    log(f"Giorno {GIORNO} (feriale): {len(attivi)} service_id attivi")

    # trips.txt: tengo solo le corse METROU attive il 12/10
    trips_txt = z.read("trips.txt").decode("utf-8-sig")
    tr_lettore = csv.reader(io.StringIO(trips_txt))
    tr_head = next(tr_lettore)
    tr_rows = list(tr_lettore)
    i_route = tr_head.index("route_id")
    i_serv = tr_head.index("service_id")
    i_trid = tr_head.index("trip_id")
    i_dir = tr_head.index("direction_id")
    metro = [r for r in tr_rows if r[i_route] == "METROU" and r[i_serv] in attivi]
    log(f"Corse METROU attive il {GIORNO}: {len(metro)}")
    if not metro:
        sys.exit("ERRORE: nessuna corsa METROU attiva: fermo qui (dati diversi da quelli descritti)")

    metro_ids = {r[i_trid] for r in metro}
    per_trip, st_head, i_st_tid, i_st_seq, i_st_arr, i_st_dep = leggi_stop_times_metro(z, metro_ids)
    log(f"Corse metro con stop_times: {len(per_trip)}")

    # corse-stampino: per ciascuna direzione l'ultima corsa reale del giorno
    # (departure_time piu' tardo dalla prima fermata)
    def partenza_dalla_prima(tid):
        righe = per_trip[tid]
        prima = min(righe, key=lambda x: int(x[i_st_seq]))
        return secondi(prima[i_st_dep])

    stampini = {}
    for direzione in ("0", "1"):
        candidati = [r[i_trid] for r in metro if r[i_dir] == direzione]
        if not candidati:
            sys.exit(f"ERRORE: nessuna corsa METROU per direction_id {direzione}")
        tid_ultimo = max(candidati, key=partenza_dalla_prima)
        righe = sorted(per_trip[tid_ultimo], key=lambda x: int(x[i_st_seq]))
        stampini[direzione] = {
            "trip_row": next(r for r in metro if r[i_trid] == tid_ultimo),
            "righe": righe,
        }
        log(f"  stampino direzione {direzione}: trip {tid_ultimo}, "
            f"{len(righe)} fermate, prima partenza {righe[0][i_st_dep]}")

    fine = secondi(FINE_BUCO)
    prima = secondi(PRIMA_PARTENZA)
    esiti = {}

    for intervallo in INTERVALLI:
        nuove_trips = []
        nuove_st = []
        per_dir = {}
        for direzione in ("0", "1"):
            st = stampini[direzione]
            base = secondi(st["righe"][0][i_st_dep])
            offsets = [secondi(r[i_st_dep]) - base for r in st["righe"]]
            part = prima
            n = 0
            partenze = []
            while part < fine:  # si ferma PRIMA di raggiungere o superare 05:22
                trip_id = f"NOTTE{intervallo}_D{direzione}_{n}"
                service_id = f"NOTTE{intervallo}_FER"
                riga_trip = list(st["trip_row"])
                riga_trip[i_trid] = trip_id
                riga_trip[i_serv] = service_id
                nuove_trips.append(riga_trip)
                for riga, off in zip(st["righe"], offsets):
                    nuova = list(riga)
                    nuova[i_st_tid] = trip_id
                    t = orario(part + off)
                    nuova[i_st_arr] = t
                    nuova[i_st_dep] = t
                    nuove_st.append(nuova)
                partenze.append(part)
                n += 1
                part += intervallo * 60
            per_dir[direzione] = partenze

        testo_trips = testo_righe(nuove_trips)
        testo_st = testo_righe(nuove_st)
        testo_cd = testo_righe([[f"NOTTE{intervallo}_FER", "20261012", "1"]])

        SCENARI.mkdir(parents=True, exist_ok=True)
        out_path = SCENARI / f"gtt_gtfs_notte{intervallo}.zip"
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zo:
            for nome in nomi:
                if nome == "trips.txt":
                    dati = aggiungi_righe(z.read(nome), testo_trips)
                elif nome == "stop_times.txt":
                    dati = aggiungi_righe(z.read(nome), testo_st)
                elif nome == "calendar_dates.txt":
                    dati = aggiungi_righe(z.read(nome), testo_cd)
                else:
                    dati = z.read(nome)
                zo.writestr(nome, dati)
        esiti[intervallo] = {"path": out_path, "per_dir": per_dir,
                             "n_trips": len(nuove_trips), "n_st": len(nuove_st)}
        log(f"Scritto {out_path} ({out_path.stat().st_size/1e6:.1f} MB)")

    # ---- controlli meccanici ----
    ok = True
    for intervallo in INTERVALLI:
        e = esiti[intervallo]
        log(f"=== CONTROLLO scenario {intervallo} minuti ({e['path'].name}) ===")
        totale = 0
        for direzione in ("0", "1"):
            p = e["per_dir"][direzione]
            totale += len(p)
            primo, ultimo = p[0], p[-1]
            passo_ok = (ultimo - primo) // (intervallo * 60) == len(p) - 1
            finestra_ok = primo >= prima and ultimo < fine
            log(f"  direzione {direzione}: {len(p)} corse nuove, "
                f"prima {orario(primo)}, ultima {orario(ultimo)}")
            log(f"    (ultima-00:50)/{intervallo} = {(ultimo-primo)//(intervallo*60)}  "
                f"atteso = {len(p)-1}  -> {'OK' if passo_ok else 'ERRORE'}")
            log(f"    prima >= 00:50 e ultima < 05:22: {'OK' if finestra_ok else 'ERRORE'}")
            if not (passo_ok and finestra_ok):
                ok = False
        log(f"  corse nuove totali (due direzioni): {totale} "
            f"({e['n_trips']} righe trips, {e['n_st']} righe stop_times)")

    if not ok:
        sys.exit("ERRORE: un controllo meccanico non passa, fermo qui")
    log("Tutti i controlli meccanici passano.")


if __name__ == "__main__":
    main()
