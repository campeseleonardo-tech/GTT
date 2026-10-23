# -*- coding: utf-8 -*-
"""
scripts/101_tempi_traffico.py - fattore di rallentamento dell'auto misurato da un servizio di percorsi (TomTom Routing API), L6.

Perche': il fattore di Google Maps (2,1) viene da 6 percorsi IN USCITA dal centro presi a mano alle 8; l'unico in entrata dava 3,6.
Qui il servizio da' per ogni percorso e ora di partenza (giorno futuro) il tempo col traffico tipico (travelTimeInSeconds) e quello senza
(noTrafficTravelTimeInSeconds): fattore di un percorso = col traffico / senza traffico. Per gruppo e ora: mediana, 25° e 75° percentile.

Regole fissate prima di vedere i numeri (blocco L6 di sviluppo/piani/PROMPT_LAVORI.md, non cambiarle dopo):
  - percorsi: (A) i 12 punti prioritari del R6 e i 5 interscambi verso Piazza Castello (gruppo «entrata») e il ritorno («uscita»);
              (B) gli 8 percorsi di controllo dello script 93, nei due sensi; (C) le 100 coppie di zone con piu' auto del mattino
              (ore_del_giorno.json), nel senso del viaggio, dal punto di maggior peso di ogni zona («coppie»);
  - partenze: martedi' 10/11/2026 e mercoledi' 11/11/2026 alle 8:00, 13:00, 17:30 e 21:00 (ora italiana, +01:00); per ogni percorso e ora
    la media dei due giorni; circa 1.200 richieste;
  - controllo: sui 6 percorsi da Piazza Castello (uscita) alle 8 il fattore mediano si confronta col 2,1 di Google; oltre 0,5 di differenza:
    AVVISO e STOP (codice di uscita 4: gli script 93, 94 e 100 NON cambiano finche' Leo non decide).
Chiave: in config_locale.json («tomtom_chiave», fuori da git). Non viene mai stampata ne' scritta: ogni messaggio d'errore la toglie.
Risposte grezze: NON si salvano (SALVA_GREZZI = False finche' Leo non ha letto le condizioni d'uso di TomTom). In git e nei rapporti solo
statistiche per gruppo e ora e, per i percorsi di controllo, il fattore a una cifra. Il file parziale (per riprendere) tiene solo il
rapporto di ogni richiesta, non i tempi, ed e' fuori da git.

Come si lancia
--------------
  python scripts\\101_tempi_traffico.py --prova              (risposte finte, nessuna chiamata, uscite in una cartella temporanea)
  python scripts\\101_tempi_traffico.py --solo-controllo     (solo i percorsi B, un giorno: circa 64 richieste; scrive il confronto)
  python scripts\\101_tempi_traffico.py                      (tutto; riprende da data\\processed\\tempi_traffico_parziale.json)
Codici di uscita: 0 = fatto; 4 = STOP del controllo; 3 = il servizio rifiuta la chiave o il limite di richieste (si salva il parziale).

Uscite: data/processed/tempi_traffico.json, docs/rapporti/RAPPORTO_TEMPI_TRAFFICO.txt
"""
import argparse
import datetime as dt
import json
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import comuni  # noqa: E402
import config_locale  # noqa: E402

RADICE = comuni.RADICE
PROC = RADICE / "data" / "processed"
OUT_JSON = PROC / "tempi_traffico.json"
RAPPORTO = RADICE / "docs" / "rapporti" / "RAPPORTO_TEMPI_TRAFFICO.txt"
PARZIALE = PROC / "tempi_traffico_parziale.json"
R6_BUS = PROC / "r6_bus_contro_auto.json"
ORE_GIORNO = PROC / "ore_del_giorno.json"

URL = "https://api.tomtom.com/routing/1/calculateRoute/{a}:{b}/json"
GIORNI = (dt.date(2026, 11, 10), dt.date(2026, 11, 11))          # martedi' e mercoledi', senza feste
ORE = ("08:00", "13:00", "17:30", "21:00")
FUSO = "+01:00"                                                  # ora solare italiana dal 25/10/2026
N_COPPIE = 100
PAUSA_S = 0.3                                                    # il piano gratuito ammette 5 richieste al secondo
FATTORE_GOOGLE_USCITA = 2.1                                      # controllo: mediana dei 6 percorsi da Piazza Castello alle 8
SOGLIA_STOP = 0.5
FATTORE_MIN, FATTORE_MAX = 1.0, 5.0                              # fuori: AVVISO
SALVA_GREZZI = False                                             # finche' Leo non ha letto le condizioni d'uso di TomTom
GRUPPI = ("entrata", "uscita", "controllo_uscita", "controllo_altri", "coppie")


class StopServizio(Exception):
    """Il servizio rifiuta la chiave o ha finito le richieste: si ferma e si salva il parziale."""


def chiave():
    k = json.loads(config_locale.FILE.read_text(encoding="utf-8")).get("tomtom_chiave", "").strip()
    if not k:
        sys.exit("ERRORE: manca \"tomtom_chiave\" in config_locale.json (chiedila a Leo).")
    return k


def senza_chiave(testo, k):
    """Toglie la chiave da qualunque testo (messaggi d'errore compresi)."""
    return str(testo).replace(k, "***").replace(urllib.parse.quote(k), "***") if k else str(testo)


def richiesta(k, da, a, giorno, ora):
    """Un percorso: ritorna (tempo col traffico, tempo senza traffico) in secondi. Mai stampa ne' registra l'indirizzo con la chiave."""
    q = urllib.parse.urlencode({"key": k, "departAt": f"{giorno}T{ora}:00{FUSO}", "traffic": "true", "travelMode": "car",
                                "routeType": "fastest", "computeTravelTimeFor": "all"})
    url = URL.format(a=f"{da[0]:.5f},{da[1]:.5f}", b=f"{a[0]:.5f},{a[1]:.5f}") + "?" + q
    for tentativo in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "GTT-progetto-personale/0.1"}), timeout=60) as r:
                s = json.loads(r.read().decode("utf-8"))["routes"][0]["summary"]
            return float(s["travelTimeInSeconds"]), float(s["noTrafficTravelTimeInSeconds"])
        except urllib.error.HTTPError as e:
            if e.code == 429 and tentativo < 5:
                time.sleep(2 + 3 * tentativo)
                continue
            if e.code in (401, 403, 429):
                raise StopServizio(f"il servizio risponde {e.code}: chiave rifiutata o limite di richieste raggiunto") from None
            raise RuntimeError(f"il servizio risponde {e.code}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if tentativo < 5:
                time.sleep(3 + 3 * tentativo)
                continue
            raise RuntimeError(senza_chiave(f"rete: {e}", k)) from None
    raise RuntimeError("troppi tentativi")


def percorsi(m93, solo_controllo):
    """Elenco di (id, gruppo, nome, (lat, lon) partenza, (lat, lon) arrivo)."""
    out = []
    # B: gli 8 percorsi noti dello script 93, nei due sensi
    for i, (nome, p, q) in enumerate(m93.NOTI):
        da_castello = p == m93.CASTELLO and i < m93.N_NOTI_TARATURA
        out.append((f"B{i}a", "controllo_uscita" if da_castello else "controllo_altri", nome, p, q))
        out.append((f"B{i}r", "controllo_altri", f"{nome.split(' → ')[1]} → {nome.split(' → ')[0]}", q, p))
    if solo_controllo:
        return out
    # A: punti prioritari e interscambi, verso Piazza Castello e ritorno
    r94 = json.loads(R6_BUS.read_text(encoding="utf-8"))
    for i, l in enumerate(r94["luoghi"]):
        p = (l["lat"], l["lon"])
        out.append((f"A{i}e", "entrata", f"{l['nome']} → Piazza Castello", p, m93.CASTELLO))
        out.append((f"A{i}u", "uscita", f"Piazza Castello → {l['nome']}", m93.CASTELLO, p))
    # C: le coppie con piu' auto del mattino, dal punto di maggior peso di ogni zona
    zone = m93.carica_zone(False)
    ore = json.loads(ORE_GIORNO.read_text(encoding="utf-8"))["ore"][0]["coppie"]
    ore = sorted(ore, key=lambda x: -x["auto"])[:N_COPPIE]
    for i, cp in enumerate(ore):
        pa, pb = zone[cp["da"]]["punti"][0], zone[cp["a"]]["punti"][0]
        out.append((f"C{i}", "coppie", f"{zone[cp['da']]['nome']} → {zone[cp['a']]['nome']}", (pa["lat"], pa["lon"]), (pb["lat"], pb["lon"])))
    return out


def dati_finti(elenco):
    """Prova: rapporti inventati e deterministici (nessuna chiamata)."""
    rng = np.random.default_rng(1)
    base = {"08:00": 1.9, "13:00": 1.4, "17:30": 1.8, "21:00": 1.1}
    return {(p[0], str(g), ora): round(float(max(1.0, base[ora] + rng.normal(0, .2))), 3) for p in elenco for g in GIORNI for ora in base}


def stat(v):
    v = np.array(v, dtype=float)
    return {"mediana": round(float(np.median(v)), 2), "q1": round(float(np.percentile(v, 25)), 2), "q3": round(float(np.percentile(v, 75)), 2), "n": len(v)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", action="store_true")
    ap.add_argument("--solo-controllo", action="store_true", help="solo i percorsi B, un giorno (circa 64 richieste)")
    args = ap.parse_args()
    c = comuni.Controlli()
    m93 = comuni.carica_script("93_tp_contro_auto.py")
    if args.prova:
        cartella = Path(tempfile.mkdtemp(prefix="tempi_traffico_prova_"))
        out_json, rapporto, parziale = cartella / OUT_JSON.name, cartella / RAPPORTO.name, cartella / PARZIALE.name
        print(f"PROVA con risposte finte: uscite in {cartella}")
        elenco = [(i, g, n, (45.0 + .001 * k, 7.6), (45.07, 7.68)) for k, (i, g, n) in enumerate(
            [(f"B{k}", "controllo_uscita", f"p{k}") for k in range(6)] + [(f"A{k}", "entrata", f"a{k}") for k in range(5)]
            + [(f"U{k}", "uscita", f"u{k}") for k in range(5)] + [(f"C{k}", "coppie", f"c{k}") for k in range(10)])]
    else:
        suff = "_controllo" if args.solo_controllo else ""
        out_json, rapporto = OUT_JSON.with_name(OUT_JSON.stem + suff + ".json"), RAPPORTO.with_name(RAPPORTO.stem + suff + ".txt")
        parziale = PARZIALE.with_name(PARZIALE.stem + suff + ".json")
        elenco = percorsi(m93, args.solo_controllo)
    giorni = GIORNI[:1] if args.solo_controllo else GIORNI
    c("percorsi per gruppo", True, dettaglio=", ".join(f"{g} {sum(1 for p in elenco if p[1] == g)}" for g in GRUPPI))
    totale = len(elenco) * len(giorni) * len(ORE)
    print(f"richieste previste: {totale}")

    risposte = {}
    if parziale.exists() and not args.prova:
        risposte = json.loads(parziale.read_text(encoding="utf-8"))
        print(f"ripresa dal parziale: {len(risposte)} richieste gia' fatte")
    finti = dati_finti(elenco) if args.prova else None
    k = None if args.prova else chiave()
    fatte = 0
    interrotto = None
    try:
        for p in elenco:
            for g in giorni:
                for ora in ORE:
                    chiave_r = f"{p[0]}|{g}|{ora}"
                    if chiave_r in risposte:
                        continue
                    if args.prova:
                        risposte[chiave_r] = finti[(p[0], str(g), ora)]
                        continue
                    tt, nt = richiesta(k, p[3], p[4], g, ora)
                    if tt <= 0 or nt <= 0:
                        c("tempi della risposta maggiori di zero", False, bloccante=True, dettaglio=p[0])
                    risposte[chiave_r] = round(tt / nt, 3)
                    fatte += 1
                    if fatte % 25 == 0:
                        parziale.write_text(json.dumps(risposte), encoding="utf-8")
                        print(f"  {len(risposte)}/{totale}", flush=True)
                    time.sleep(PAUSA_S)
    except StopServizio as e:
        interrotto = senza_chiave(e, k)
    except RuntimeError as e:
        interrotto = senza_chiave(e, k)
    finally:
        if not args.prova:
            parziale.write_text(json.dumps(risposte), encoding="utf-8")
    if interrotto:
        print(f"STOP: {interrotto}. Salvate {len(risposte)} richieste su {totale} in {parziale.name}: rilancia per riprendere.")
        return 3

    # fattore di ogni percorso e ora = media dei giorni; poi statistiche per gruppo e ora
    per_perc = {p[0]: {ora: float(np.mean([risposte[f"{p[0]}|{g}|{ora}"] for g in giorni])) for ora in ORE} for p in elenco}
    stats = {g: {ora: stat([per_perc[p[0]][ora] for p in elenco if p[1] == g]) for ora in ORE} for g in GRUPPI if any(p[1] == g for p in elenco)}
    tutti = [v for d in per_perc.values() for v in d.values()]
    c(f"fattori fra {FATTORE_MIN:g} e {FATTORE_MAX:g}", all(FATTORE_MIN <= v <= FATTORE_MAX for v in tutti),
      dettaglio=f"da {min(tutti):.2f} a {max(tutti):.2f}; fuori: {sum(1 for v in tutti if not FATTORE_MIN <= v <= FATTORE_MAX)} su {len(tutti)}")
    controllo = stats["controllo_uscita"]["08:00"]["mediana"]
    stop = abs(controllo - FATTORE_GOOGLE_USCITA) > SOGLIA_STOP
    c(f"6 percorsi in uscita alle 8: fattore del servizio vicino al 2,1 di Google (entro {SOGLIA_STOP:g})", not stop,
      dettaglio=f"mediana {controllo:.2f} contro {FATTORE_GOOGLE_USCITA:g}" + (" -> STOP: decide Leo" if stop else ""))

    nomi = {p[0]: p for p in elenco}
    controllo_b = [{"percorso": nomi[i][2], "gruppo": nomi[i][1], "fattori": {ora: round(v, 1) for ora, v in d.items()}}
                   for i, d in per_perc.items() if i.startswith("B")]
    out = {"fonte": "TomTom Routing API (tempo col traffico tipico / tempo senza traffico, partenza in un giorno futuro)", "prova": bool(args.prova),
           "solo_controllo": bool(args.solo_controllo), "giorni": [str(g) for g in giorni], "ore": list(ORE), "richieste": len(risposte),
           "grezzi_salvati": SALVA_GREZZI, "stop": stop, "gruppi": stats, "controllo_B": controllo_b, "controlli": list(c.righe)}
    out_json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    r = ["RAPPORTO TEMPI TRAFFICO (TomTom Routing API)" + (" - PROVA CON DATI FINTI" if args.prova else "") + (" - SOLO CONTROLLO" if args.solo_controllo else ""),
         f"generato: {dt.datetime.now().isoformat(timespec='seconds')}", "",
         f"Giorni di partenza: {', '.join(str(g) for g in giorni)}; ore: {', '.join(ORE)} (ora italiana); richieste: {len(risposte)}.",
         "Fattore = tempo col traffico tipico / tempo senza traffico, media dei giorni. Le risposte grezze non sono salvate.", "",
         "FATTORE PER GRUPPO E ORA: mediana (25° - 75° percentile), numero di percorsi"]
    for g, d in stats.items():
        r.append(f"  {g}: " + " | ".join(f"{ora} {s['mediana']:.2f} ({s['q1']:.2f}-{s['q3']:.2f}), n {s['n']}" for ora, s in d.items()))
    r += ["", "PERCORSI DI CONTROLLO (fattore a una cifra)"]
    r += [f"  {b['percorso']} [{b['gruppo']}]: " + " | ".join(f"{ora} {f:g}" for ora, f in b["fattori"].items()) for b in controllo_b]
    r += ["", "CONTROLLI"] + [f"  {x}" for x in c.righe]
    rapporto.write_text("\n".join(r) + "\n", encoding="utf-8")
    print(f"scritti {out_json.name} e {rapporto.name}")
    return 4 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
