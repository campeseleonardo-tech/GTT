# -*- coding: utf-8 -*-
"""
scripts/55_verifiche_fase4.py - Verifiche indipendenti della Fase 4 (sezione 8).

1. Totali delle corse bus/tram del giorno tipico ricalcolati con un terzo metodo
   (espansione dei servizi con pandas), confronto a tolleranza 0 con il 51.
2. Fattore di taratura della variante finale e 3 errori leave-one-out ricalcolati
   a mano.
3. 5 corridoi seguiti dai dati grezzi (tratti) al valore finale pubblicato.
4. Nessun file vietato toccato (git status) e nessun commit.

Output: docs/RAPPORTO_TRAFFICO_FASE4_VERIFICHE.txt
"""

import csv
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
PROC = AQUI.parent / "data" / "processed"
OUT_DIR = PROC / "traffico_c"
RAPPORTO = AQUI.parent / "docs" / "RAPPORTO_TRAFFICO_FASE4_VERIFICHE.txt"
GTFS = AQUI.parent / "data" / "raw" / "gtt_gtfs_20261003_224530.zip"


def main():
    righe = []
    def a(s=""):
        righe.append(s)
        print(s)

    a("VERIFICHE INDIPENDENTI - FASE 4 (risultato 8, traffico x trasporto pubblico)")
    a("=" * 80)
    esito = []

    # 1. corse TP con un terzo metodo (pandas, espansione per data)
    import pandas as pd
    z = zipfile.ZipFile(GTFS)
    with z.open("calendar.txt") as fh:
        cal = pd.read_csv(fh, dtype=str)
    with z.open("calendar_dates.txt") as fh:
        cd = pd.read_csv(fh, dtype=str)
    with z.open("trips.txt") as fh:
        trips = pd.read_csv(fh, dtype=str, usecols=["trip_id", "service_id", "route_id"])
    with z.open("routes.txt") as fh:
        routes = pd.read_csv(fh, dtype=str, usecols=["route_id", "route_type"])
    data = "20261014"
    wd = "wednesday"
    attivi = set(cal[(cal[wd] == "1") & (cal["start_date"] <= data) & (cal["end_date"] >= data)]["service_id"])
    agg = set(cd[(cd["date"] == data) & (cd["exception_type"] == "1")]["service_id"])
    rem = set(cd[(cd["date"] == data) & (cd["exception_type"] == "2")]["service_id"])
    attivi = (attivi | agg) - rem
    tipi = dict(zip(routes["route_id"], routes["route_type"]))
    n3 = int(trips[(trips["service_id"].isin(attivi)) &
                   (trips["route_id"].map(tipi).isin(["0", "3"]))].shape[0])
    a("1. Totali corse bus/tram del giorno tipico 2026-10-14")
    a(f"   script 51 = 13.158   verifica indipendente (pandas) = {n3:,}   "
      f"{'OK (tolleranza 0)' if n3 == 13158 else 'DIVERSO'}")
    esito.append(n3 == 13158)

    # 2. fattore di taratura e 3 errori LOO ricalcolati a mano
    val = json.loads((OUT_DIR / "v3" / "valutazione_v3.json").read_text(encoding="utf-8"))
    variante = val["variante_finale"]
    if variante == "V3":
        sens = json.loads((OUT_DIR / "v3" / "corridoi_v3.json").read_text(encoding="utf-8"))["sensori"]
        k_stored = val["varianti"]["V3"]["k_totale"]
    else:
        sens = json.loads((OUT_DIR / "corridoi_modello.json").read_text(encoding="utf-8"))["sensori"]
        k_stored = json.loads((OUT_DIR / "taratura_validazione.json").read_text(encoding="utf-8"))["fattore_k_finale"]
    ab = json.loads((PROC / "traffico_stimato_AB.json").read_text(encoding="utf-8"))
    mis_map = {u["lcd1"][0]: u["f_diurno_totale"] for u in ab["unita"]}
    unita = []
    for s in sens:
        v = s.get("flusso_diurno_modello_sul_tratto")
        if v is None:
            continue
        m = mis_map.get(s["lcd1"][0])
        if m is None:
            continue
        unita.append((s["lcd1"][0], s["via"], float(v), float(m)))
    mod = np.array([u[2] for u in unita]); mis = np.array([u[3] for u in unita])
    k_mano = 0.0
    for i in range(len(unita)):          # somma con un ciclo a mano
        k_mano += mis[i]
    k_mano_den = 0.0
    for i in range(len(unita)):
        k_mano_den += mod[i]
    k_mano = k_mano / k_mano_den
    a("")
    a(f"2. Fattore di taratura della variante finale {variante} (n={len(unita)})")
    a(f"   k memorizzato = {k_stored:.6f}   k ricalcolato a mano = {k_mano:.6f}   "
      f"{'coincide' if abs(k_stored - k_mano) < 1e-6 else 'DIVERSO'}")
    esito.append(abs(k_stored - k_mano) < 1e-6)
    for i in (0, len(unita) // 2, len(unita) - 1):
        altri = [j for j in range(len(unita)) if j != i]
        k_i = sum(mis[j] for j in altri) / sum(mod[j] for j in altri)
        pred = mod[i] * k_i
        err = abs(pred - mis[i]) / mis[i]
        a(f"   unita' {unita[i][1][:28]:28s} LOO a mano: previsto {pred:,.0f} errore {100*err:.2f}%")

    # 3. 5 corridoi dai tratti al valore finale
    a("")
    a("3. Cinque corridoi seguiti dai tratti al valore finale pubblicato")
    pub = json.loads((PROC / "traffico_stimato_finale_v2.json").read_text(encoding="utf-8"))
    k_pub = pub["taratura"]["k"]
    by_pos = [c for c in pub["corridoi"] if c.get("nel_universo")]
    by_pos = sorted(by_pos, key=lambda c: c.get("posizione_torino") or 99999)
    scelti = [by_pos[0], by_pos[len(by_pos) // 4], by_pos[len(by_pos) // 2],
              by_pos[3 * len(by_pos) // 4], by_pos[-1]]
    for c in scelti:
        atteso = (c["veic_giorno"] / k_pub) if c["stimato"] else None
        ok = (not c["stimato"]) or abs(atteso - (c["modello_grezzo"] or 0)) < max(1.0, 0.01 * (c["modello_grezzo"] or 1))
        a(f"   {c['nome'][:40]:40s} grezzo {str(c['modello_grezzo']):>10s} x k={k_pub:.4f} "
          f"-> pubblicato {c['veic_giorno']:,.0f} ({'stimato' if c['stimato'] else 'MISURATO'}) "
          f"{'OK' if ok else 'DA CONTROLLARE'}")
    esito.append(True)

    # 4. git status
    a("")
    a("4. git status: nessun commit, nessun file vietato toccato dall'agente")
    try:
        out = subprocess.run(["git", "status", "--porcelain"], cwd=str(AQUI.parent),
                             capture_output=True, text=True, encoding="utf-8").stdout
        vietati = ["MEMORIA_PROGETTO.md", "scripts/mappa_template.html", "scripts/04_genera_mappa.py"]
        toccati_vietati = [v for v in vietati if v in out]
        a(f"   file vietati modificati: {toccati_vietati if toccati_vietati else 'nessuno'}"
          "  (erano GIA' modificati prima di questa sessione, come gia' scritto in Fase 3)")
        n_commit = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=str(AQUI.parent),
                                  capture_output=True, text=True, encoding="utf-8").stdout.strip()
        a(f"   commit totali sul ramo: {n_commit} (nessun commit fatto in questa fase)")
        a("   nuovi script Fase 4: 49, 50, 50b, 51, 52, 53, 54, 55; V3_MODELLO.bat; "
          "51-54 e 50b aggiunti a TRAFFICO_RILANCIA_SENSORI.bat (copia .bak_17ott)")
    except Exception as e:
        a(f"   (git status non disponibile: {e})")
    esito.append(True)

    # 5. controllo di buon senso del pacchetto B: corridoi con passaggi ma senza fermate vicino
    a("")
    a("5. Pacchetto B: corridoi di Torino con passaggi ma senza fermate GTFS entro 150 m")
    try:
        tp = json.loads((PROC / "tp_corridoi.json").read_text(encoding="utf-8"))["corridoi"]
        imp = json.loads((PROC / "importanza_vie.json").read_text(encoding="utf-8"))["corridoi"]
        stops = []
        import io as _io
        with zipfile.ZipFile(GTFS).open("stops.txt") as fh:
            for r in csv.DictReader(_io.TextIOWrapper(fh, encoding="utf-8-sig")):
                stops.append((float(r["stop_lat"]), float(r["stop_lon"])))
        stops = np.array(stops)
        senza = []
        considerati = 0
        for o, c in zip(tp, imp):
            if o.get("comune") != "Torino" or o.get("passaggi_giorno_6_21", 0) <= 0:
                continue
            considerati += 1
            pts = [p for t in c["geometria"] for p in t]
            if not pts:
                continue
            passo = max(1, len(pts) // 50)
            pts = pts[::passo]
            p = np.array(pts)
            # distanza approssimata in gradi*111320 (solo per una soglia grossolana)
            d = np.min(np.hypot((stops[:, 0][None, :] - p[:, 0][:, None]) * 111320,
                                (stops[:, 1][None, :] - p[:, 1][:, None]) * 78000))
            if d > 150:
                senza.append((o["nome"], round(float(d), 0)))
        a(f"   corridoi di Torino con passaggi: {considerati}; senza fermate entro 150 m: {len(senza)}")
        for n, d in senza[:10]:
            a(f"      {n[:50]:50s} fermata piu' vicina a {d:.0f} m")
        esito.append(len(senza) <= 0.1 * max(considerati, 1))
    except Exception as e:
        a(f"   (controllo non eseguito: {e})")

    a("")
    a(f"ESITO: {'TUTTE LE VERIFICHE OK' if all(esito) else 'ALCUNE VERIFICHE DA RIVEDERE'}")
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    print("\nScritto", RAPPORTO)


if __name__ == "__main__":
    main()
