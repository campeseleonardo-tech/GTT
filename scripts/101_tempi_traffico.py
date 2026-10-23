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
CORREZIONE DEL 24/10/2026 (L6bis), decisa DOPO aver visto lo STOP di L6 (TomTom 1,26 contro Google 2,1): i due numeri misuravano cose diverse.
  - il nostro «tempo a flusso libero» viene dalla rete OSM ai limiti di velocita', senza semafori e incroci: e' troppo veloce;
  - il fattore di Google (2,1) = (tempo Google - 5) / NOSTRO flusso libero: corregge insieme la rete troppo veloce e il traffico;
  - il fattore di L6 = tempo TomTom col traffico / tempo TomTom senza traffico: e' solo il traffico (TomTom i semafori li conta gia').
  Ora per ogni percorso e ora si salvano DUE rapporti (2 decimali, mai i minuti):
    fattore_rete = tempo TomTom col traffico / nostro flusso libero dello stesso percorso (la stessa grandezza del 2,1 di Google, senza i 5 minuti);
    congestione  = tempo col traffico / tempo senza traffico (il solo traffico, confrontabile coi sensori 5T).
  Il nostro flusso libero c'e' solo nel senso in cui i nostri script lo calcolano: i percorsi A in uscita e i B di ritorno danno solo la congestione.
  Il controllo: mediana di fattore_rete alle 8 sui 6 percorsi B in uscita contro 2,1, soglia 0,5 (invariata).
Chiave: in config_locale.json («tomtom_chiave», fuori da git). Non viene mai stampata ne' scritta: ogni messaggio d'errore la toglie.
Risposte grezze: NON si salvano (SALVA_GREZZI = False finche' Leo non ha letto le condizioni d'uso di TomTom). In git e nei rapporti solo
statistiche per gruppo e ora e, per i percorsi di controllo, il fattore a una cifra. Il file parziale (per riprendere) tiene solo il
rapporto di ogni richiesta, non i tempi, ed e' fuori da git.

GIRO L8 (24/10/2026), regole fissate prima dei numeri nuovi (blocco L8 di sviluppo/piani/PROMPT_LAVORI.md): TomTom diventa la stima principale
dell'auto (decisione di Leo, dopo L6bis). Lo script salva anche i fattori PER PERCORSO (fattore_rete e congestione, 2 decimali, mai i minuti) e
chiede, con --estendi e solo martedi' 10/11/2026 (ore italiane), tre gruppi di percorsi in piu':
  (C1) le coppie dalla 101a alla 600a per auto del mattino, alle 8:00 (500 richieste);
  (C2) le coppie dalla 101a alla 300a alle 13:00, 17:30 e 21:00 (600);
  (D)  Piazza Castello -> punto di maggior peso di ognuna delle zone dell'indagine, alle 8:00 (una per zona; il nostro flusso libero e' quello dello script 99).
Tetto bloccante MAX_RICHIESTE = 2000 per le richieste NUOVE di un lancio (si stampa prima il numero; se lo supererebbe: codice di uscita 5).
Controllo di coerenza: sulle 100 coppie gia' fatte il fattore_rete del solo martedi' deve differire dalla media dei due giorni di meno di 0,05 in mediana
(altrimenti AVVISO nel rapporto, non si ferma). Per le coppie non chieste a TomTom: mediana delle coppie TomTom della stessa ora e della stessa fascia di
flusso libero (terzili del nostro flusso libero fra le coppie TomTom di quell'ora); la regola e' salvata nel JSON (regola_coppie) e applicata da
comuni.FattoriTomTom.

Come si lancia
--------------
  python scripts\\101_tempi_traffico.py --estendi            (L8: chiede solo C1, C2 e D, martedi' 10/11; riprende dal parziale)
  python scripts\\101_tempi_traffico.py --prova            (risposte finte, nessuna chiamata, uscite in una cartella temporanea)
  python scripts\\101_tempi_traffico.py --solo-controllo     (solo i percorsi B, un giorno: circa 64 richieste; scrive il confronto)
  python scripts\\101_tempi_traffico.py                      (tutto; riprende da data\\processed\\tempi_traffico_parziale.json)
Codici di uscita: 0 = fatto; 4 = STOP del controllo; 3 = il servizio rifiuta la chiave o il limite di richieste (si salva il parziale);
5 = le richieste nuove supererebbero MAX_RICHIESTE.

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
PARZIALE = PROC / "tempi_traffico_parziale_v2.json"       # v2: due rapporti per richiesta (il parziale di L6 aveva solo la congestione)
TP_AUTO = PROC / "tp_contro_auto.json"
R6_BUS = PROC / "r6_bus_contro_auto.json"
ORE_GIORNO = PROC / "ore_del_giorno.json"

URL = "https://api.tomtom.com/routing/1/calculateRoute/{a}:{b}/json"
GIORNI = (dt.date(2026, 11, 10), dt.date(2026, 11, 11))          # martedi' e mercoledi', senza feste
ORE = ("08:00", "13:00", "17:30", "21:00")
FUSO = "+01:00"                                                  # ora solare italiana dal 25/10/2026
N_COPPIE = 100
N_COPPIE_C1 = 600                                                # L8: coppie 101-600 alle 8:00
N_COPPIE_C2 = 300                                                # L8: coppie 101-300 alle altre tre ore
MAX_RICHIESTE = 2000                                             # L8: tetto bloccante per le richieste nuove di un lancio
ORE_ALTRE = ORE[1:]
PAUSA_S = 0.3                                                    # il piano gratuito ammette 5 richieste al secondo
FATTORE_GOOGLE_USCITA = 2.1                                      # controllo: mediana dei 6 percorsi da Piazza Castello alle 8
SOGLIA_STOP = 0.5
FATTORE_MIN, FATTORE_MAX = 1.0, 5.0                              # fuori: AVVISO
SALVA_GREZZI = False                                             # finche' Leo non ha letto le condizioni d'uso di TomTom
GRUPPI = ("entrata", "uscita", "controllo_uscita", "controllo_altri", "controllo_ritorno", "coppie", "coppie_estese", "zone_castello")


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
    """Elenco base di (id, gruppo, nome, (lat, lon) partenza, (lat, lon) arrivo, nostro flusso libero in minuti o None, ore, chiave).
    La chiave identifica il percorso per gli altri script: nome del luogo, «da|a» delle zone, codice zona."""
    out = []
    t93 = json.loads(TP_AUTO.read_text(encoding="utf-8"))
    libero_noti = {n["nome"]: n["auto_libero_min"] for n in t93["noti"]}
    # B: gli 8 percorsi noti dello script 93, nei due sensi
    for i, (nome, p, q) in enumerate(m93.NOTI):
        da_castello = p == m93.CASTELLO and i < m93.N_NOTI_TARATURA
        out.append((f"B{i}a", "controllo_uscita" if da_castello else "controllo_altri", nome, p, q, libero_noti[nome], ORE, nome))
        out.append((f"B{i}r", "controllo_ritorno", f"{nome.split(' → ')[1]} → {nome.split(' → ')[0]}", q, p, None, ORE, nome))
    if solo_controllo:
        return out
    # A: punti prioritari e interscambi, verso Piazza Castello e ritorno
    r94 = json.loads(R6_BUS.read_text(encoding="utf-8"))
    for i, l in enumerate(r94["luoghi"]):
        p = (l["lat"], l["lon"])
        out.append((f"A{i}e", "entrata", f"{l['nome']} → Piazza Castello", p, m93.CASTELLO, l["libero_min"], ORE, l["nome"]))
        out.append((f"A{i}u", "uscita", f"Piazza Castello → {l['nome']}", m93.CASTELLO, p, None, ORE, l["nome"]))
    # C: le coppie con piu' auto del mattino, dal punto di maggior peso di ogni zona (le prime 100: ordine di ore_del_giorno.json, come in L6)
    zone = m93.carica_zone(False)
    ore = json.loads(ORE_GIORNO.read_text(encoding="utf-8"))["ore"][0]["coppie"]
    ore = sorted(ore, key=lambda x: -x["auto"])[:N_COPPIE]
    libero_coppie = {(x["da"], x["a"]): x["libero_min"] for x in t93["coppie"]}
    for i, cp in enumerate(ore):
        out.append(percorso_coppia(i, "coppie", cp["da"], cp["a"], zone, libero_coppie, ORE))
    return out


def percorso_coppia(i, gruppo, da, a, zone, libero_coppie, ore):
    pa, pb = zone[da]["punti"][0], zone[a]["punti"][0]
    return (f"C{i}", gruppo, f"{zone[da]['nome']} → {zone[a]['nome']}", (pa["lat"], pa["lon"]), (pb["lat"], pb["lon"]),
            libero_coppie[(da, a)], ore, f"{da}|{a}")


def percorsi_estesi(m93, base):
    """L8: i percorsi C1 (coppie 101-600 alle 8), C2 (101-300 alle altre ore: stesse coppie di C1) e D (Castello -> ogni zona alle 8)."""
    t93 = json.loads(TP_AUTO.read_text(encoding="utf-8"))
    zone = m93.carica_zone(False)
    libero_coppie = {(x["da"], x["a"]): x["libero_min"] for x in t93["coppie"]}
    ab = sorted((x for x in t93["coppie"] if x["gruppo"] in ("a", "b")), key=lambda x: -x["auto"])
    primi = [p for p in base if p[1] == "coppie"]
    assert [p[7] for p in primi] == [f"{x['da']}|{x['a']}" for x in ab[:N_COPPIE]], "l'ordine delle coppie non coincide con quello di L6"
    out = []
    for i in range(N_COPPIE, N_COPPIE_C1):
        x = ab[i]
        out.append(percorso_coppia(i, "coppie_estese", x["da"], x["a"], zone, libero_coppie, ("08:00",) + (ORE_ALTRE if i < N_COPPIE_C2 else ())))
    cod = sorted(zone)
    m99 = comuni.carica_script("99_area_tempi.py")
    punti = [(zone[z]["punti"][0]["lat"], zone[z]["punti"][0]["lon"]) for z in cod]
    _, libero = m99.tempi_auto_liberi([], punti)       # minuti a flusso libero da Piazza Castello, come lo script 99
    for k, z in enumerate(cod):
        out.append((f"D{k}", "zone_castello", f"Piazza Castello → {zone[z]['nome']}", m93.CASTELLO, punti[k], float(libero[k]), ("08:00",), z))
    return out


def dati_finti(elenco):
    """Prova: rapporti inventati e deterministici (nessuna chiamata)."""
    rng = np.random.default_rng(1)
    base = {"08:00": 1.9, "13:00": 1.4, "17:30": 1.8, "21:00": 1.1}
    return {(p[0], str(g), ora): round(float(max(1.0, base[ora] + rng.normal(0, .2))), 3) for p in elenco for g in GIORNI for ora in base}


def dati_finti_elenco():
    """Prova: percorsi inventati, uno per tipo (base ed estesi)."""
    e = [(f"B{k}", "controllo_uscita", f"p{k}", (45.0 + .001 * k, 7.6), (45.07, 7.68), 8.0, ORE, f"p{k}") for k in range(6)]
    e += [(f"A{k}e", "entrata", f"a{k}", (45.0 + .001 * k, 7.6), (45.07, 7.68), 8.0, ORE, f"Luogo {k}") for k in range(5)]
    e += [(f"A{k}u", "uscita", f"u{k}", (45.07, 7.68), (45.0 + .001 * k, 7.6), None, ORE, f"Luogo {k}") for k in range(5)]
    e += [(f"C{k}", "coppie", f"c{k}", (45.0, 7.6), (45.07, 7.68), 4.0 + k, ORE, f"Q{k}|Q{k + 1}") for k in range(10)]
    e += [(f"C{k}", "coppie_estese", f"c{k}", (45.0, 7.6), (45.07, 7.68), 4.0 + k % 12, ("08:00",) + (ORE_ALTRE if k < 16 else ()), f"Q{k}|Q{k + 1}") for k in range(10, 25)]
    e += [(f"D{k}", "zone_castello", f"d{k}", (45.07, 7.68), (45.0 + .001 * k, 7.6), 6.0, ("08:00",), f"Q{k}") for k in range(6)]
    return e


def stat(v):
    v = np.array(v, dtype=float)
    return {"mediana": round(float(np.median(v)), 2), "q1": round(float(np.percentile(v, 25)), 2), "q3": round(float(np.percentile(v, 75)), 2), "n": len(v)}


def media_giorni(risposte, pid, ora, i, giorni):
    """Media dei giorni disponibili di un rapporto (i = 0 fattore_rete, 1 congestione); None se manca o se in un giorno non c'e'."""
    v = [risposte[k][i] for g in giorni if (k := f"{pid}|{g}|{ora}") in risposte]
    return None if not v or any(x is None for x in v) else float(np.mean(v))


def regola_coppie(elenco, per_perc):
    """Per ogni ora: terzili del nostro flusso libero fra le coppie TomTom di quell'ora e mediana di fattore_rete in ogni fascia (blocco L8)."""
    out = {"terzili": {}, "mediana_fascia": {}, "n_fascia": {}}
    for ora in ORE:
        v = [(p[5], per_perc[p[0]][ora]["fattore_rete"]) for p in elenco
             if p[1] in ("coppie", "coppie_estese") and p[0] in per_perc and ora in per_perc[p[0]] and per_perc[p[0]][ora]["fattore_rete"] is not None]
        if not v:
            continue
        lib = np.array([x[0] for x in v], dtype=float)
        fr = np.array([x[1] for x in v], dtype=float)
        t1, t2 = (float(x) for x in np.percentile(lib, [100 / 3, 200 / 3]))
        fasce = [fr[lib <= t1], fr[(lib > t1) & (lib <= t2)], fr[lib > t2]]
        tutti = float(np.median(fr))
        out["terzili"][ora] = [round(t1, 3), round(t2, 3)]
        out["mediana_fascia"][ora] = [round(float(np.median(f)) if len(f) else tutti, 3) for f in fasce]
        out["n_fascia"][ora] = [int(len(f)) for f in fasce]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prova", action="store_true")
    ap.add_argument("--solo-controllo", action="store_true", help="solo i percorsi B, un giorno (circa 64 richieste)")
    ap.add_argument("--estendi", action="store_true", help="L8: chiede solo C1, C2 e D (martedi' 10/11)")
    args = ap.parse_args()
    c = comuni.Controlli()
    m93 = comuni.carica_script("93_tp_contro_auto.py")
    if args.prova:
        cartella = Path(tempfile.mkdtemp(prefix="tempi_traffico_prova_"))
        out_json, rapporto, parziale = cartella / OUT_JSON.name, cartella / RAPPORTO.name, cartella / PARZIALE.name
        print(f"PROVA con risposte finte: uscite in {cartella}")
        elenco = dati_finti_elenco()
        base = [p for p in elenco if p[1] not in ("coppie_estese", "zone_castello")]
    else:
        suff = "_controllo" if args.solo_controllo else ""
        out_json, rapporto = OUT_JSON.with_name(OUT_JSON.stem + suff + ".json"), RAPPORTO.with_name(RAPPORTO.stem + suff + ".txt")
        parziale = PARZIALE.with_name(PARZIALE.stem + suff + ".json")
        base = percorsi(m93, args.solo_controllo)
        elenco = base if args.solo_controllo else base + percorsi_estesi(m93, base)
    giorni_base = GIORNI[:1] if args.solo_controllo else GIORNI
    giorni_esteso = (GIORNI[0],)                                       # C1, C2 e D: solo martedi' 10/11
    estesi_ids = {p[0] for p in elenco if p[1] in ("coppie_estese", "zone_castello")}
    giorni_di = lambda p: giorni_esteso if p[0] in estesi_ids else giorni_base
    c("percorsi per gruppo", True, dettaglio=", ".join(f"{g} {sum(1 for p in elenco if p[1] == g)}" for g in GRUPPI))

    risposte = {}
    if parziale.exists() and not args.prova:
        risposte = json.loads(parziale.read_text(encoding="utf-8"))
        print(f"ripresa dal parziale: {len(risposte)} richieste gia' fatte")
    # le richieste da fare in questo lancio: con --estendi solo i percorsi estesi, altrimenti solo i percorsi base (di solito sono gia' tutti nel parziale)
    da_fare = [(p, g, ora) for p in elenco if args.prova or (p[0] in estesi_ids) == bool(args.estendi) for g in giorni_di(p) for ora in p[6]
               if f"{p[0]}|{g}|{ora}" not in risposte]
    print(f"richieste previste in questo lancio: {len(da_fare)} (gia' nel parziale: {len(risposte)}; tetto {MAX_RICHIESTE})", flush=True)
    if len(da_fare) > MAX_RICHIESTE and not args.prova:
        print(f"STOP: le richieste nuove ({len(da_fare)}) supererebbero il tetto di {MAX_RICHIESTE}. Non si chiede niente.")
        return 5
    finti = dati_finti(elenco) if args.prova else None
    k = None if args.prova else (chiave() if da_fare else None)
    fatte = 0
    interrotto = None
    try:
        for p, g, ora in da_fare:
            chiave_r = f"{p[0]}|{g}|{ora}"
            if args.prova:
                cg = finti[(p[0], str(g), ora)]
                risposte[chiave_r] = [round(cg * 1.5, 3) if p[5] else None, cg]
                continue
            tt, nt = richiesta(k, p[3], p[4], g, ora)   # minuti: solo in memoria
            if tt <= 0 or nt <= 0:
                c("tempi della risposta maggiori di zero", False, bloccante=True, dettaglio=p[0])
            risposte[chiave_r] = [round(tt / (p[5] * 60), 3) if p[5] else None, round(tt / nt, 3)]
            fatte += 1
            if fatte % 25 == 0:
                parziale.write_text(json.dumps(risposte), encoding="utf-8")
                print(f"  {fatte}/{len(da_fare)}", flush=True)
            time.sleep(PAUSA_S)
    except StopServizio as e:
        interrotto = senza_chiave(e, k)
    except RuntimeError as e:
        interrotto = senza_chiave(e, k)
    finally:
        if not args.prova and (fatte or not parziale.exists()):
            parziale.write_text(json.dumps(risposte), encoding="utf-8")
    mancano = 0
    if interrotto:
        mancano = len(da_fare) - fatte
        print(f"STOP: {interrotto}. Fatte {fatte} richieste su {len(da_fare)} in questo lancio, ne mancano {mancano}; salvate in {parziale.name}: rilancia per riprendere. "
              "Il JSON si scrive lo stesso con quello che c'e' (i percorsi mancanti prendono la mediana, come da regola).")

    # per ogni percorso e ora: media dei giorni disponibili, per i due rapporti (fattore_rete solo dove c'e' il nostro flusso libero)
    per_perc = {}
    for p in elenco:
        d = {}
        for ora in p[6]:
            co = media_giorni(risposte, p[0], ora, 1, giorni_di(p))
            if co is None:
                continue
            d[ora] = {"fattore_rete": media_giorni(risposte, p[0], ora, 0, giorni_di(p)), "congestione": co}
        if d:
            per_perc[p[0]] = d
    stats = {}
    for g in GRUPPI:
        stats[g] = {}
        for ora in ORE:
            ps = [per_perc[p[0]][ora] for p in elenco if p[1] == g and p[0] in per_perc and ora in per_perc[p[0]]]
            if not ps:
                continue
            voce = {"congestione": stat([x["congestione"] for x in ps])}
            fr = [x["fattore_rete"] for x in ps if x["fattore_rete"] is not None]
            if fr:
                voce["fattore_rete"] = stat(fr)
            stats[g][ora] = voce
        if not stats[g]:
            del stats[g]
    cong = [x["congestione"] for d in per_perc.values() for x in d.values()]
    rete = [x["fattore_rete"] for d in per_perc.values() for x in d.values() if x["fattore_rete"] is not None]
    c(f"congestione fra {FATTORE_MIN:g} e {FATTORE_MAX:g}", all(FATTORE_MIN <= v <= FATTORE_MAX for v in cong),
      dettaglio=f"da {min(cong):.2f} a {max(cong):.2f}; fuori: {sum(1 for v in cong if not FATTORE_MIN <= v <= FATTORE_MAX)} su {len(cong)}")
    c(f"fattore_rete fra {FATTORE_MIN:g} e {FATTORE_MAX:g}", all(FATTORE_MIN <= v <= FATTORE_MAX for v in rete),
      dettaglio=f"da {min(rete):.2f} a {max(rete):.2f}; fuori: {sum(1 for v in rete if not FATTORE_MIN <= v <= FATTORE_MAX)} su {len(rete)}")
    controllo = stats["controllo_uscita"]["08:00"]["fattore_rete"]["mediana"]
    stop = abs(controllo - FATTORE_GOOGLE_USCITA) > SOGLIA_STOP
    c(f"6 percorsi in uscita alle 8: fattore_rete del servizio vicino al 2,1 di Google (entro {SOGLIA_STOP:g})", not stop,
      dettaglio=f"mediana {controllo:.2f} contro {FATTORE_GOOGLE_USCITA:g}" + (" -> STOP: decide Leo" if stop else ""))

    # controllo di coerenza (L8): sulle 100 coppie base il solo martedi' contro la media dei due giorni
    coerenza = {}
    if not args.solo_controllo:
        for ora in ORE:
            dif = []
            for p in elenco:
                if p[1] != "coppie":
                    continue
                a, b = risposte.get(f"{p[0]}|{GIORNI[0]}|{ora}"), risposte.get(f"{p[0]}|{GIORNI[1]}|{ora}")
                if a and b and a[0] is not None and b[0] is not None:
                    dif.append(abs(a[0] - (a[0] + b[0]) / 2))
            if dif:
                coerenza[ora] = round(float(np.median(dif)), 3)
        tutte = [x for x in coerenza.values()]
        if tutte:
            c("coerenza: fattore_rete del solo martedi' contro la media dei due giorni, differenza mediana sotto 0,05 (100 coppie, ogni ora)",
              max(tutte) < 0.05, dettaglio=", ".join(f"{o} {v:.3f}" for o, v in coerenza.items()))

    nomi = {p[0]: p for p in elenco}
    controllo_b = [{"percorso": nomi[i][2], "gruppo": nomi[i][1],
                    "fattore_rete": {ora: (None if v["fattore_rete"] is None else round(v["fattore_rete"], 2)) for ora, v in d.items()},
                    "congestione": {ora: round(v["congestione"], 2) for ora, v in d.items()}}
                   for i, d in per_perc.items() if i.startswith("B")]

    # fattori per percorso (L8): solo rapporti a 2 decimali, mai i minuti; la chiave e' quella degli altri script
    def per_chiave(gruppi):
        out_ = {}
        for p in elenco:
            if p[1] in gruppi and p[0] in per_perc:
                out_[p[7]] = {ora: [None if x["fattore_rete"] is None else round(x["fattore_rete"], 2), round(x["congestione"], 2)] for ora, x in per_perc[p[0]].items()}
        return out_
    per_percorso = {"entrata": per_chiave(("entrata",)), "uscita": per_chiave(("uscita",)),
                    "coppie": per_chiave(("coppie", "coppie_estese")), "zone_castello": per_chiave(("zone_castello",))}
    med_ent = {ora: stats["entrata"][ora]["fattore_rete"]["mediana"] for ora in ORE if "fattore_rete" in stats.get("entrata", {}).get(ora, {})}
    med_zone = {ora: stats["zone_castello"][ora]["fattore_rete"]["mediana"] for ora in ORE if "fattore_rete" in stats.get("zone_castello", {}).get(ora, {})}
    if "08:00" not in med_zone and "08:00" in med_ent:
        med_zone["08:00"] = med_ent["08:00"]                          # D non chiesto: la zona prende la mediana dell'entrata (dichiarato in «mediane_gruppo_nota»)
    mediane_gruppo = {"entrata": med_ent, "zone_castello": med_zone}
    n_estese = sum(1 for p in elenco if p[0] in estesi_ids)
    out = {"fonte": "TomTom Routing API (tempo col traffico tipico, partenza in un giorno futuro)",
           "definizioni": {"fattore_rete": "tempo TomTom col traffico / nostro flusso libero dello stesso percorso (come il 2,1 di Google, senza i 5 minuti)",
                           "congestione": "tempo TomTom col traffico / tempo TomTom senza traffico (solo il traffico)"},
           "correzione_24_10": "decisa dopo aver visto lo STOP di L6: il primo confronto (congestione 1,26 contro 2,1) metteva a confronto grandezze diverse", "prova": bool(args.prova),
           "solo_controllo": bool(args.solo_controllo), "giorni": [str(g) for g in giorni_base], "giorno_esteso": str(giorni_esteso[0]),
           "ore": list(ORE), "richieste": len(risposte), "richieste_mancanti_estese": mancano,
           "grezzi_salvati": SALVA_GREZZI, "stop": stop, "gruppi": stats, "controllo_B": controllo_b, "controlli": list(c.righe)}
    if not args.solo_controllo:
        out.update({"per_percorso": per_percorso, "mediane_gruppo": mediane_gruppo, "regola_coppie": regola_coppie(elenco, per_perc),
                    "coerenza_martedi": coerenza, "percorsi_estesi": n_estese,
                    "nota_percorsi": "base (L6): media di martedi' 10 e mercoledi' 11/11/2026; estesi (L8: coppie 101-600, zone): solo martedi' 10/11/2026. "
                                     "Le coppie non chieste prendono la mediana delle coppie TomTom della stessa ora e fascia di flusso libero (regola_coppie)."})
    out_json.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    r = ["RAPPORTO TEMPI TRAFFICO (TomTom Routing API)" + (" - PROVA CON DATI FINTI" if args.prova else "") + (" - SOLO CONTROLLO" if args.solo_controllo else ""),
         f"generato: {dt.datetime.now().isoformat(timespec='seconds')}", "",
         f"Giorni di partenza: {', '.join(str(g) for g in giorni_base)} (percorsi base); {giorni_esteso[0]} (percorsi estesi del giro L8: coppie 101-600 e zone); ore: {', '.join(ORE)} (ora italiana); richieste nel parziale: {len(risposte)}.",
         "Fattore = tempo col traffico tipico / tempo senza traffico, media dei giorni. Le risposte grezze non sono salvate.", "",
         "fattore_rete = tempo col traffico / nostro flusso libero (come il 2,1 di Google); congestione = tempo col traffico / tempo senza traffico (come i sensori).",
         "Correzione del 24/10, decisa dopo aver visto lo STOP di L6: il primo confronto metteva a confronto grandezze diverse.", "",
         "FATTORE PER GRUPPO E ORA: mediana (25° - 75° percentile), numero di percorsi"]
    for g, d in stats.items():
        for nome_f in ("fattore_rete", "congestione"):
            if any(nome_f in s for s in d.values()):
                r.append(f"  {g}, {nome_f}: " + " | ".join(f"{ora} {s[nome_f]['mediana']:.2f} ({s[nome_f]['q1']:.2f}-{s[nome_f]['q3']:.2f}), n {s[nome_f]['n']}"
                                                          for ora, s in d.items() if nome_f in s))
    if not args.solo_controllo:
        rc = out["regola_coppie"]
        r += ["", "REGOLA PER LE COPPIE NON CHIESTE A TOMTOM (blocco L8): mediana delle coppie TomTom della stessa ora e fascia di flusso libero",
              "  ora | terzili del flusso libero (minuti) | mediana per fascia (bassa, media, alta) | coppie per fascia"]
        for ora in rc["terzili"]:
            r.append(f"  {ora} | {rc['terzili'][ora][0]:.1f} - {rc['terzili'][ora][1]:.1f} | " + ", ".join(f"{x:.2f}" for x in rc["mediana_fascia"][ora]) + " | " + ", ".join(str(x) for x in rc["n_fascia"][ora]))
        r += ["", "COERENZA (differenza mediana fra il solo martedi' e la media dei due giorni, 100 coppie base; soglia 0,05): "
              + (", ".join(f"{o} {v:.3f}" for o, v in coerenza.items()) if coerenza else "non calcolabile")]
    r += ["", "PERCORSI DI CONTROLLO (2 decimali): fattore_rete / congestione"]
    r += [f"  {b['percorso']} [{b['gruppo']}]: " + " | ".join(
        f"{ora} {'-' if b['fattore_rete'][ora] is None else format(b['fattore_rete'][ora], '.2f')} / {b['congestione'][ora]:.2f}" for ora in ORE) for b in controllo_b]
    r += ["", "CONTROLLI"] + [f"  {x}" for x in c.righe]
    rapporto.write_text("\n".join(r) + "\n", encoding="utf-8")
    print(f"scritti {out_json.name} e {rapporto.name}")
    if args.prova and not args.solo_controllo:
        f = comuni.FattoriTomTom(json.loads(out_json.read_text(encoding="utf-8")))
        c("prova: il modello legge il JSON (luogo, coppia chiesta, coppia non chiesta, zona)",
          f.luogo("Luogo 0")[1] and f.coppia("Q10", "Q11", 5.0)[1] and not f.coppia("Q90", "Q91", 5.0)[1] and f.zona("Q0")[1] and not f.zona("Q99")[1])
        print([x for x in c.righe if x.startswith("prova")])
    if mancano:
        return 3
    return 4 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
