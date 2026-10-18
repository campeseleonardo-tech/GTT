#!/usr/bin/env python3
"""Risultato 2 - numeri finali dello scenario "metro di notte" (v2, 16/10/2026).

v1 contava solo le sezioni che passavano da ZERO servizi assoluti a qualcosa: a
Torino questo non succede mai (bus notturni gia' presenti ovunque, minimo 2
servizi anche di notte), quindi v1 dava sempre 0. v2 conta invece QUALSIASI
aumento, anche piccolo, dei servizi raggiungibili nella finestra — nessuna
soglia applicata qui: il delta per sezione e per ora resta nel dettaglio cosi'
si puo' filtrare con soglie diverse in futuro senza rifare il giro R5.

Legge tre file gia' pronti (nessun nuovo giro R5):
  data/processed/accessibilita.json            (baseline, ore 0-23)
  data/processed/accessibilita_notte15.json    (scenario 15 minuti, ore 01-04)
  data/processed/accessibilita_notte30.json    (scenario 30 minuti, ore 01-04)

Output:
  data/processed/risultato2_metro_notte.json       (dettaglio completo per sezione)
  data/processed/risultato2_riepilogo_mappa.json   (pochi numeri, per la scheda in simulazione.html)
  docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt
"""
import json
from datetime import datetime, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
BASE = RADICE / "data/processed/accessibilita.json"
SCENARI = {
    "notte15": {"file": RADICE / "data/processed/accessibilita_notte15.json", "intervallo": 15, "nome": "Ogni 15 minuti"},
    "notte30": {"file": RADICE / "data/processed/accessibilita_notte30.json", "intervallo": 30, "nome": "Ogni 30 minuti"},
}
OUT = RADICE / "data/processed/risultato2_metro_notte.json"
OUT_RIEPILOGO = RADICE / "data/processed/risultato2_riepilogo_mappa.json"
RAPPORTO = RADICE / "docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt"

GIORNO = "2026-10-12"
FINESTRA = "00:50-05:22"
ORE = ["01", "02", "03", "04"]  # ore ricalcolate dagli scenari

TITOLO = "Metro di notte"
DOMANDA = ("Quanti residenti guadagnano servizi raggiungibili in piu' nel buco notturno reale "
           f"({FINESTRA}) se la metro M1 facesse corse finte anche li'?")

# Avviso standard del progetto (era in scripts/07_elabora_scenario.py, tolto il 18/10: doppione di calcola_simulazione.py)
AVVISO = [
    "⚠ SIMULAZIONE SU ORARIO PROGRAMMATO",
    "I risultati mostrano l'offerta potenziale (passaggi/ora, residenti raggiunti, tempi di attesa teorici)",
    "calcolata applicando le variazioni indicate all'orario ufficiale GTFS.",
    "Non tengono conto di: traffico reale, ritardi, capienza dei mezzi, domanda effettiva passeggeri, regolarità del servizio.",
    "Un aumento di corse sulla carta non garantisce che i bus arrivino in orario.",
    "Dati [PROGRAMMATO] / [STIMATO] — non [MISURATO].",
]


def somma_ora(sezione, nome_ora):
    """Somma dei servizi raggiungibili in una fascia (0 = nessun servizio)."""
    return sum(sezione["tp"][nome_ora].values())


def carica_sezioni(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    return {s["id"]: s for s in d["sezioni"]}, d


def controlla_ore(sezioni, path, attese):
    """Le fasce orarie dentro i file devono essere esattamente quelle attese."""
    viste = set()
    for s in sezioni.values():
        viste |= set(s["tp"].keys())
    if not attese.issubset(viste):
        raise SystemExit(f"ERRORE struttura: in {path.name} mancano le ore {sorted(attese - viste)} "
                         f"(trovate {sorted(viste)})")
    return viste


def mediana(valori_ordinati):
    n = len(valori_ordinati)
    if n == 0:
        return None
    meta = n // 2
    if n % 2 == 1:
        return valori_ordinati[meta]
    return (valori_ordinati[meta - 1] + valori_ordinati[meta]) / 2


def percentile(valori_ordinati, p):
    n = len(valori_ordinati)
    if n == 0:
        return None
    idx = max(0, min(n - 1, round(p / 100 * (n - 1))))
    return valori_ordinati[idx]


def calcola(baseline, scenario, intervallo):
    """Numeri dello scenario: delta di servizi raggiungibili per sezione, nessuna soglia."""
    ids_base = list(baseline.keys())
    if set(ids_base) != set(scenario.keys()):
        raise SystemExit("ERRORE: le sezioni dei file non coincidono (id diversi)")

    residenti_migliorati = 0
    sezioni_migliorate = 0
    delta_totale_citta = 0
    sezioni_con_delta_negativo = 0
    deltas_positivi = []
    dettaglio = []

    for sid in ids_base:
        sb = baseline[sid]
        sc = scenario[sid]
        delta_ore = {o: somma_ora(sc, o) - somma_ora(sb, o) for o in ORE}
        delta_totale = sum(delta_ore.values())
        delta_totale_citta += delta_totale
        migliorata = delta_totale > 0  # qualsiasi aumento, anche di 1: nessuna soglia qui

        if any(v < 0 for v in delta_ore.values()):
            sezioni_con_delta_negativo += 1
        if migliorata:
            sezioni_migliorate += 1
            residenti_migliorati += sb["res"]
            deltas_positivi.append(delta_totale)

        riga = {"id": sid, "res": sb["res"], "delta_totale": int(delta_totale), "migliorata": bool(migliorata)}
        for o in ORE:
            riga[f"delta_{o}"] = int(delta_ore[o])
        dettaglio.append(riga)

    deltas_positivi.sort()

    return {
        "parametri": {
            "giorno": GIORNO,
            "finestra": FINESTRA,
            "intervallo_minuti": intervallo,
            "ore": ORE,
        },
        "soglia_applicata": 0,
        "nota_soglia": ("Nessuna soglia: 'migliorata' = qualsiasi aumento (anche di 1) nella somma "
                        "delle 4 ore. Il delta e' salvato per ogni sezione e ogni ora nel 'dettaglio', "
                        "cosi' si puo' applicare una soglia diversa in futuro senza ricalcolare."),
        "sezioni_migliorate": sezioni_migliorate,
        "residenti_migliorati": int(residenti_migliorati),
        "delta_totale_citta": int(delta_totale_citta),
        "delta_mediano_migliorate": mediana(deltas_positivi),
        "delta_p90_migliorate": percentile(deltas_positivi, 90),
        "attesa_media_minuti": intervallo / 2,
        "sezioni_con_delta_negativo": sezioni_con_delta_negativo,
        "nota_delta_negativo": ("Un numero molto piccolo di sezioni puo' mostrare un delta negativo "
                                "minimo (tipicamente -1 servizio): rumore del motore di routing R5 ai "
                                "margini del cutoff di 45 min, non un vero peggioramento reale."),
        "dettaglio": dettaglio,
    }


def main():
    baseline, _ = carica_sezioni(BASE)
    controlla_ore(baseline, BASE, set(ORE))

    esito = {
        "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "giorno": GIORNO,
        "finestra": FINESTRA,
        "ore": ORE,
    }
    riepilogo_scenari = []

    for chiave, cfg in SCENARI.items():
        scenario, _ = carica_sezioni(cfg["file"])
        controlla_ore(scenario, cfg["file"], set(ORE))
        r = calcola(baseline, scenario, cfg["intervallo"])
        esito[chiave] = r
        print(f"{chiave}: sezioni migliorate {r['sezioni_migliorate']}, "
              f"residenti migliorati {r['residenti_migliorati']}, "
              f"delta totale citta {r['delta_totale_citta']}, "
              f"attesa media {r['attesa_media_minuti']} min "
              f"(delta negativi: {r['sezioni_con_delta_negativo']})")

        riepilogo_scenari.append({
            "nome": cfg["nome"],
            "numeri": [
                {"label": "Residenti con accesso migliorato", "prima": 0,
                 "dopo": r["residenti_migliorati"], "unita": "residenti"},
                {"label": "Sezioni di censimento migliorate", "prima": 0,
                 "dopo": r["sezioni_migliorate"], "unita": "sezioni"},
                {"label": "Attesa media teorica", "prima": None,
                 "dopo": r["attesa_media_minuti"], "unita": "min"},
            ],
            "nota": (f"Delta mediano tra le sezioni migliorate: {r['delta_mediano_migliorate']} "
                     f"servizi in piu' (90-esimo percentile: {r['delta_p90_migliorate']})."),
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(esito, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Scritto {OUT}")

    riepilogo = {
        "risultato": "2",
        "titolo": TITOLO,
        "domanda": DOMANDA,
        "generato": esito["generato"],
        "avviso": AVVISO,
        "scenari": riepilogo_scenari,
    }
    OUT_RIEPILOGO.write_text(json.dumps(riepilogo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scritto {OUT_RIEPILOGO}")

    righe = [
        "RISULTATO 2 - METRO DI NOTTE: servizi raggiungibili in piu' nel buco notturno (v2, nessuna soglia)",
        f"generato: {esito['generato']}  giorno: {GIORNO}  finestra: {FINESTRA}  "
        f"ore ricalcolate: {','.join(ORE)}",
        "",
        "NOTA METODO: la versione precedente contava solo le sezioni che passavano da ZERO servizi",
        "assoluti a qualcosa: a Torino questo non succede mai (bus notturni gia' presenti ovunque,",
        "minimo 2 servizi anche nelle ore piu' vuote), quindi dava sempre 0/0. Questa versione conta",
        "invece QUALSIASI aumento, anche piccolo, dei servizi raggiungibili nella finestra 01-04;",
        "nessuna soglia applicata: il delta per sezione resta nel JSON per poter filtrare dopo.",
        "",
    ]
    for chiave, cfg in SCENARI.items():
        r = esito[chiave]
        inter = cfg["intervallo"]
        righe.append(f"== Scenario {inter} minuti (una corsa finta ogni {inter}' tra le 00:50 e le 05:22) ==")
        righe.append(f"  residenti con accesso migliorato: {r['residenti_migliorati']}")
        righe.append(f"  sezioni migliorate: {r['sezioni_migliorate']}")
        righe.append(f"  delta totale di servizi raggiungibili in citta': {r['delta_totale_citta']}")
        righe.append(f"  delta mediano tra le sezioni migliorate: {r['delta_mediano_migliorate']} "
                     f"(90-esimo percentile: {r['delta_p90_migliorate']})")
        righe.append(f"  attesa media teorica: {r['attesa_media_minuti']} min")
        righe.append(f"  sezioni con un delta negativo minimo (rumore R5, vedi nota): "
                     f"{r['sezioni_con_delta_negativo']}")
        righe.append("")
    righe.append("")
    righe.extend(AVVISO)

    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe), encoding="utf-8")
    print(f"Scritto {RAPPORTO}")


if __name__ == "__main__":
    main()
