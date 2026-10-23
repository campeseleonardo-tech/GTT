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


# Periodo fisso dei dati (giri L9 e L9b, 24/10/2026): SOLO GIORNI INTERI. Regola: il PERIODO non contiene mai il giorno della copia dello storico
# (quel giorno e' a meta': i numeri non si riprodurrebbero). Gli script 24, 26, 27, 33, 69, 70, 71, 88 e 04_genera_mappa.py lo leggono: i dati
# arrivati dopo non entrano nei risultati finche' non si cambia qui a mano (lavoro P8). Estremi inclusi, giorni locali.
PERIODO = {
    "sensori": ("2026-10-09", "2026-10-22"),     # sensori 5T (velocita_5t.json): script 24, 26, e da li' 33 e 88
    "gps": ("2026-10-10", "2026-10-22"),         # passaggi dei mezzi (start_date dello storico): script 27, 70 e velocita' della mappa
    "parcheggi": ("2026-10-15", "2026-10-22"),   # riempimento dei parcheggi 5T: script 69 e 71
}


def _iso(giorno):
    """'2026-10-09', '20261009' o date -> 'AAAA-MM-GG'."""
    t = giorno.isoformat() if hasattr(giorno, "isoformat") else str(giorno)
    return t if "-" in t else f"{t[:4]}-{t[4:6]}-{t[6:8]}"


def nel_periodo(giorno, chiave):
    """True se il giorno sta nel periodo fisso PERIODO[chiave]."""
    da, a = PERIODO[chiave]
    return da <= _iso(giorno)[:10] <= a


def controlla_copia_storico(db):
    """AVVISO se il giorno (locale) dell'ultimo cambio della copia dello storico e' dentro un PERIODO: sarebbe un giorno a meta'."""
    import datetime as _dt
    giorno = _dt.datetime.fromtimestamp(Path(db).stat().st_mtime).date().isoformat()
    for k, (da, a) in PERIODO.items():
        if da <= giorno <= a:
            print(f"AVVISO: il giorno della copia dello storico ({giorno}) e' dentro il periodo fisso '{k}' ({da} - {a}): giorno a meta', ritira l'estremo")


def testo_periodo(chiave):
    """«dal 09/10/2026 al 22/10/2026», per le schede."""
    da, a = PERIODO[chiave]
    it = lambda t: f"{t[8:10]}/{t[5:7]}/{t[:4]}"
    return f"dal {it(da)} al {it(a)}"


def controlla_periodo(periodo_json, chiave):
    """AVVISO (stampato) se il periodo scritto in un JSON non e' quello fisso."""
    p = (periodo_json or {})
    if (p.get("da"), p.get("a")) != PERIODO[chiave]:
        print(f"AVVISO: il periodo dei dati ({p.get('da')} - {p.get('a')}) non e' quello fisso {PERIODO[chiave][0]} - {PERIODO[chiave][1]} (comuni.PERIODO): rilancia lo script che scrive il JSON")


class FattoriTomTom:
    """Fattore_rete di TomTom (script 101) per percorso, come stima principale dell'auto dal giro L8 (24/10/2026).
    Auto = nostro flusso libero x fattore_rete del percorso stesso + 5 minuti. Quando il percorso non e' stato chiesto a TomTom:
      - coppie di zone: la mediana delle coppie TomTom della stessa ora e della stessa fascia di flusso libero (terzili, calcolati dallo script 101);
      - luoghi del R6 e zone (area): la mediana dei percorsi dello stesso gruppo alla stessa ora."""

    def __init__(self, d):
        self.d = d
        pp = d["per_percorso"]
        self.entrata, self.coppie_t, self.zone_t = pp["entrata"], pp["coppie"], pp["zone_castello"]
        self.regola = d["regola_coppie"]
        self.controllo = {b["percorso"]: b["fattore_rete"] for b in d.get("controllo_B", [])}
        self.mediane = d["mediane_gruppo"]       # {"entrata": {ora: x}, "zone_castello": {ora: x}}

    @staticmethod
    def _fr(voce, ora):
        x = voce.get(ora) if voce else None
        return None if not x else x[0]

    def luogo(self, nome, ora="08:00"):
        """(fattore, vero): vero = chiesto a TomTom per quel luogo."""
        x = self._fr(self.entrata.get(nome), ora)
        return (x, True) if x else (self.mediane["entrata"][ora], False)

    def zona(self, cod, ora="08:00"):
        x = self._fr(self.zone_t.get(cod), ora)
        return (x, True) if x else (self.mediane["zone_castello"][ora], False)

    def coppia(self, da, a, libero_min, ora="08:00"):
        x = self._fr(self.coppie_t.get(f"{da}|{a}"), ora)
        if x:
            return x, True
        t1, t2 = self.regola["terzili"][ora]
        f = 0 if libero_min <= t1 else (1 if libero_min <= t2 else 2)
        return self.regola["mediana_fascia"][ora][f], False

    def percorso_controllo(self, nome, ora="08:00"):
        x = self.controllo.get(nome, {}).get(ora)
        return x if x else None


def fattori_tomtom():
    """FattoriTomTom, o None se il file dello script 101 manca, e' di prova, di solo controllo o fermato."""
    if not TEMPI_TRAFFICO.exists():
        return None
    d = json.loads(TEMPI_TRAFFICO.read_text(encoding="utf-8"))
    if d.get("prova") or d.get("solo_controllo") or d.get("stop") or "per_percorso" not in d:
        return None
    return FattoriTomTom(d)


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
