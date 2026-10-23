#!/usr/bin/env python3
"""
comuni.py  -  funzioni e costanti usate da piu' script (preparato da Claude il 20/10/2026).

Cosa c'e'
---------
  trova_radice()          cartella del progetto (quella che si chiama GTT)
  haversine_m()           distanza in metri fra due punti (lat, lon)
  proietta(lat, lon)      coordinate in metri (piano locale centrato su 45,07 gradi), per distanze veloci
  ora_locale(dt_utc)      ora italiana da un datetime UTC (ora legale: ultima domenica di marzo e di ottobre)
  percentile_rank(dict)   percentile 0-100, valori uguali -> stesso percentile (copia di quella dello script 75)
  soglia_quantile(lista, percentile)  valore alla posizione del percentile (stessa regola dello script 75)
  carica_script(nome)     carica uno script che inizia con un numero (es. "42_instradamento.py") come modulo
  Controlli               raccoglie i controlli: bloccanti (errori di struttura) o avvisi (numeri da guardare)
Costanti: ZONE_CENTRALI (Q001-Q009), MACRO_UNIVERSO, CENTRO_LAT/LON (Piazza Castello), FATTORE_PIEDI,
MODI_AUTO, MEZZI_PUBBLICI, MATTINO_MINUTI.

Come si prova
-------------
  python scripts\\comuni.py      (stampa 4 controlli: devono essere tutti OK)
"""
import importlib.util
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# zona centrale: per fermate E parcheggi (vedi docs/R6_parcheggi.md)
ZONE_CENTRALI = tuple(f"Q{n:03d}" for n in range(1, 10))
MACRO_UNIVERSO = ("01 Torino", "02 Cintura", "03 Resto CMTO")
CENTRO_LAT, CENTRO_LON = 45.0711, 7.6857          # Piazza Castello
LAT_RIF = 45.07
M_GRADO = 111000.0
FATTORE_PIEDI = 1.3                                # distanza a piedi = linea d'aria x 1,3
MODI_AUTO = ("03", "21")                           # auto da conducente, car sharing (04 = passeggero: persone, non auto)
MODI_AUTO_PERSONE = ("03", "04", "21")
MEZZI_PUBBLICI = ("06", "07", "08", "09", "12", "13", "19", "22")   # come lo script 73
MATTINO_MINUTI = (360, 599)                        # partenza 06:00-09:59


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def proietta(lat, lon):
    """(x, y) in metri; stessa formula degli script 80 e 69."""
    return (lon * M_GRADO * math.cos(math.radians(LAT_RIF)), lat * M_GRADO)


def _ultima_domenica(anno, mese):
    d = date(anno, mese, 31)
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


def ora_locale(dt_utc):
    a = dt_utc.year
    inizio = datetime(a, 3, _ultima_domenica(a, 3).day, 1, tzinfo=timezone.utc)
    fine = datetime(a, 10, _ultima_domenica(a, 10).day, 1, tzinfo=timezone.utc)
    return dt_utc + timedelta(hours=2 if inizio <= dt_utc < fine else 1)


def percentile_rank(valori):
    """Percentile 0-100, valori uguali -> stesso percentile (copia della funzione dello script 75)."""
    chiavi = list(valori.keys())
    ordinati = sorted(chiavi, key=lambda k: valori[k])
    n = len(ordinati)
    if n <= 1:
        return {k: 100.0 for k in chiavi}
    rank = {}
    i = 0
    while i < n:
        j = i
        while j + 1 < n and valori[ordinati[j + 1]] == valori[ordinati[i]]:
            j += 1
        for k in ordinati[i:j + 1]:
            rank[k] = (i + j) / 2
        i = j + 1
    return {k: 100.0 * rank[k] / (n - 1) for k in chiavi}


def soglia_quantile(valori, percentile):
    """Stessa regola di soglia_90 dello script 75, per un percentile qualsiasi (90 = il 10% piu' alto)."""
    v = sorted(valori)
    if not v:
        return None
    idx = max(0, min(len(v) - 1, round(percentile / 100 * (len(v) - 1))))
    return v[idx]


TEMPI_TRAFFICO = RADICE / "data" / "processed" / "tempi_traffico.json"


def fattore_servizio(gruppo, ora="08:00"):
    """Fattore_rete mediano del servizio di percorsi (TomTom, script 101) per gruppo («entrata», «coppie») e ora, o None se il file
    manca o e' di prova. fattore_rete = tempo col traffico / nostro flusso libero: la stessa grandezza del 2,1 di Google (L6bis)."""
    if not TEMPI_TRAFFICO.exists():
        return None
    d = json.loads(TEMPI_TRAFFICO.read_text(encoding="utf-8"))
    if d.get("prova") or d.get("solo_controllo") or d.get("stop"):
        return None
    try:
        return d["gruppi"][gruppo][ora]["fattore_rete"]["mediana"]
    except KeyError:
        return None


def imposta_java(jdk=None):
    """Java per r5py (serve 21 o piu'): JAVA_HOME gia' impostato non si tocca; altrimenti la cartella data/otp/jdk-... se esiste
    (setdefault), altrimenti il Java del sistema (PATH). Se non c'e' nessuno dei due, si ferma con un messaggio chiaro."""
    import os
    import shutil
    if jdk is not None:
        cartelle = [Path(jdk), *sorted(Path(jdk).parent.glob("jdk-*"))]
        trovata = next((c for c in cartelle if c.is_dir()), None)
        if trovata:
            os.environ.setdefault("JAVA_HOME", str(trovata))
    if not os.environ.get("JAVA_HOME") and not shutil.which("java"):
        sys.exit("ERRORE: Java non trovato. r5py ha bisogno di Java 21 o piu': installalo (es. Temurin 21) oppure metti un JRE in data/otp/ "
                 "e imposta JAVA_HOME.")


def carica_script(nome_file):
    """Carica scripts/<nome_file> come modulo (serve per i nomi che iniziano con un numero)."""
    percorso = AQUI / nome_file
    if str(AQUI) not in sys.path:
        sys.path.insert(0, str(AQUI))
    spec = importlib.util.spec_from_file_location(Path(nome_file).stem.replace("-", "_"), percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class Controlli:
    """Controlli di uno script. bloccante=True solo per errori di struttura (file vuoti, somme che non
    tornano, valori negativi): allora lo script si ferma. Tutto il resto e' un AVVISO: si stampa, si
    scrive nel rapporto e lo script continua."""

    def __init__(self):
        self.righe = []

    def __call__(self, nome, ok, bloccante=False, dettaglio=""):
        stato = "OK" if ok else ("ERRORE" if bloccante else "AVVISO")
        riga = f"{stato:6s} {nome}" + (f" — {dettaglio}" if dettaglio else "")
        self.righe.append(riga)
        print("  " + riga)
        if not ok and bloccante:
            sys.exit(f"ERRORE BLOCCANTE: {nome} {dettaglio}")
        return ok

    def avvisi(self):
        return [r for r in self.righe if r.startswith("AVVISO")]


if __name__ == "__main__":
    c = Controlli()
    d = haversine_m(45.06120, 7.67780, 45.07158, 7.66586)
    c("haversine Porta Nuova - Porta Susa circa 1.487 m", abs(d - 1487) < 5, dettaglio=f"{d:.0f} m")
    t1 = ora_locale(datetime(2026, 10, 25, 0, 30, tzinfo=timezone.utc))
    t2 = ora_locale(datetime(2026, 10, 25, 1, 30, tzinfo=timezone.utc))
    c("ora legale: 25/10 00:30 UTC e 01:30 UTC = 02:30 italiane", t1.strftime("%H:%M") == t2.strftime("%H:%M") == "02:30")
    p = percentile_rank({"a": 1, "b": 2, "c": 2, "d": 3})
    c("percentile di [1,2,2,3] = 0, 50, 50, 100", [round(p[k]) for k in "abcd"] == [0, 50, 50, 100])
    c("zone centrali Q001-Q009", ZONE_CENTRALI[0] == "Q001" and ZONE_CENTRALI[-1] == "Q009" and len(ZONE_CENTRALI) == 9)
    print("avvisi:", len(c.avvisi()))
