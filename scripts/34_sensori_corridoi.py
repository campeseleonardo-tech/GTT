#!/usr/bin/env python3
"""34_sensori_corridoi.py

Mette in tabella, senza decidere niente: quale corridoio stradale di
data/processed/importanza_vie.json cade sotto ogni sensore 5T con almeno una
cella ok (flusso misurato) di data/processed/flusso_5t_sensori.json.

Regola IDENTICA allo script 24 (stesso abbinamento, non una regola nuova):
- il nome della via del sensore si normalizza con la funzione `normalizza` dello
  script 24 (toglie via/corso/strada, accenti, apostrofi, il suffisso "(TO)");
- si guardano i corridoi con lo stesso nome normalizzato;
- il sensore si dice "abbinato" se la distanza minima fra il sensore e un punto
  qualsiasi della geometria del corridoio (tutti i tratti e tutti i punti, non
  solo gli estremi) e' <= 60 m.

Il risultato non assegna flussi e non stima niente: dice solo chi sta su cosa.
Lo script 24 importa le sue funzioni (il nome del file inizia con un numero,
quindi si carica con importlib).

Output:
- data/processed/sensori_corridoi.json
- docs/rapporti/RAPPORTO_SENSORI_CORRIDOI.txt

Solo libreria standard. Nessuna scrittura sul database.
"""

import importlib.util
import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
IN_SENSORI = RADICE / "data" / "processed" / "flusso_5t_sensori.json"
IN_CORRIDOI = RADICE / "data" / "processed" / "importanza_vie.json"
OUT = RADICE / "data" / "processed" / "sensori_corridoi.json"
RAPPORTO = RADICE / "docs" / "rapporti" / "RAPPORTO_SENSORI_CORRIDOI.txt"
RAPPORTO.parent.mkdir(parents=True, exist_ok=True)

SOGLIA_M = 60   # come lo script 24
RIGHE = []


def scrivi(msg=""):
    RIGHE.append(str(msg))


def carica_script_24():
    """Carica 24_importanza_vie.py come modulo (il nome inizia con un numero)."""
    percorso = RADICE / "scripts" / "24_importanza_vie.py"
    if not percorso.is_file():
        raise SystemExit(f"Script 24 non trovato: {percorso}")
    spec = importlib.util.spec_from_file_location("m24_importanza_vie", percorso)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def distanza_minima(lat, lon, geometria, haversine_m):
    """Distanza minima (m) fra il punto e tutti i punti della geometria."""
    migliore = None
    for tratto in geometria:
        for punto in tratto:
            d = haversine_m(lat, lon, punto[0], punto[1])
            if migliore is None or d < migliore:
                migliore = d
    return migliore


def main():
    m24 = carica_script_24()

    for p in (IN_SENSORI, IN_CORRIDOI):
        if not p.is_file():
            raise SystemExit(f"File non trovato: {p}")
    sensori_dati = json.loads(IN_SENSORI.read_text(encoding="utf-8"))["sensori"]
    corridoi = json.loads(IN_CORRIDOI.read_text(encoding="utf-8"))["corridoi"]

    per_chiave = {}
    for c in corridoi:
        per_chiave.setdefault(c["chiave_normalizzata"], []).append(c)

    # solo i sensori con almeno una cella ok (flusso misurato)
    sensori = {k: s for k, s in sensori_dati.items() if s["tipo"]}

    risultato = {}
    for lcd1, s in sorted(sensori.items(), key=lambda kv: str(kv[0])):
        chiave = m24.normalizza(s["via"])
        candidati = per_chiave.get(chiave, [])
        best, best_d = None, None
        for c in candidati:
            d = distanza_minima(s["lat"], s["lon"], c["geometria"], m24.haversine_m)
            if d is not None and (best_d is None or d < best_d):
                best, best_d = c, d
        abbinato = best_d is not None and best_d <= SOGLIA_M
        risultato[str(lcd1)] = dict(
            lcd1=s.get("lcd1", lcd1), via=s["via"], dir=s["dir"],
            lat=s["lat"], lon=s["lon"], urbano=s["urbano"],
            chiave_normalizzata=chiave,
            abbinato=abbinato,
            distanza_m=None if best_d is None else round(best_d, 1),
            corridoio=(None if best is None else
                       dict(nome=best["nome"], punteggio=best["punteggio"],
                            lunghezza_km=best["lunghezza_km"])),
            n_corridoi_omonimi=len(candidati),
        )

    # ---------- conteggi per il rapporto ----------
    tutti = list(risultato.values())
    abb = [r for r in tutti if r["abbinato"]]
    non = [r for r in tutti if not r["abbinato"]]
    abb_urb = [r for r in abb if r["urbano"]]
    non_urb = [r for r in non if r["urbano"]]
    dist_punt = {}
    for r in abb:
        dist_punt[r["corridoio"]["punteggio"]] = dist_punt.get(r["corridoio"]["punteggio"], 0) + 1
    senza_omonimo = [r for r in non if r["n_corridoi_omonimi"] == 0]
    oltre_soglia = [r for r in non if r["n_corridoi_omonimi"] > 0]

    payload = {
        "fonte": {
            "sensori": "data/processed/flusso_5t_sensori.json",
            "corridoi": "data/processed/importanza_vie.json",
            "regola": "stessa dello script 24: nome normalizzato uguale e distanza <= 60 m",
        },
        "tag": "MISURATO (posizione) - nessun flusso assegnato o stimato qui",
        "soglia_m": SOGLIA_M,
        "sensori": risultato,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

    # ---------- rapporto ----------
    scrivi("SENSORI 5T E CORRIDOI STRADALI (abbinamento, nessuna stima)")
    scrivi("=" * 78)
    scrivi(f"sensori considerati (con almeno una cella ok): {len(tutti)}")
    scrivi(f"corridoi in importanza_vie.json: {len(corridoi)}")
    scrivi(f"regola: nome normalizzato uguale (idea dello script 24) e distanza minima <= {SOGLIA_M} m "
           "da un punto qualsiasi del corridoio")
    scrivi("")
    scrivi("(1) Conteggi")
    scrivi(f"  abbinati: {len(abb)}   [attesi vicini a 15, come lo script 24]")
    scrivi(f"    di cui urbani (nome con '(TO)'): {len(abb_urb)}")
    scrivi(f"  NON abbinati: {len(non)}")
    scrivi(f"    di cui urbani: {len(non_urb)}")
    scrivi(f"    - nessun corridoio con lo stesso nome: {len(senza_omonimo)}")
    scrivi(f"    - corridoio omonimo trovato ma oltre {SOGLIA_M} m: {len(oltre_soglia)}")
    scrivi("")
    scrivi("(2) Distribuzione degli abbinati per punteggio del corridoio (1-5)")
    for p in (1, 2, 3, 4, 5):
        scrivi(f"  punteggio {p}: {dist_punt.get(p, 0)}")

    scrivi("")
    scrivi("(3) Sensori abbinati")
    scrivi(f"  {'lcd1':>6}  {'via':32s} {'dir':9s} {'corridoio':30s} {'p':>2} "
           f"{'km':>7} {'dist_m':>7}  urbano")
    for r in sorted(abb, key=lambda r: str(r["lcd1"])):
        c = r["corridoio"]
        scrivi(f"  {r['lcd1']:>6}  {r['via'][:32]:32s} {r['dir'][:9]:9s} "
               f"{c['nome'][:30]:30s} {c['punteggio']:>2} {c['lunghezza_km']:>7.1f} "
               f"{r['distanza_m']:>7.1f}  {'si' if r['urbano'] else 'no'}")

    scrivi("")
    scrivi("(4) Sensori NON abbinati (per capire perche' manca il corridoio)")
    scrivi("    'piu vicino' = corridoio con lo stesso nome piu' vicino (anche oltre la soglia)")
    scrivi(f"  {'lcd1':>6}  {'via':32s} {'dir':9s} {'piu vicino':30s} {'p':>2} {'dist_m':>8}  note")
    for r in sorted(non, key=lambda r: str(r["lcd1"])):
        c = r["corridoio"]
        nome = c["nome"][:30] if c else "-"
        pun = f"{c['punteggio']:>2}" if c else "-"
        dist = f"{r['distanza_m']:>8.1f}" if r["distanza_m"] is not None else "       -"
        nota = "nessun corridoio con questo nome" if r["n_corridoi_omonimi"] == 0 else ""
        scrivi(f"  {r['lcd1']:>6}  {r['via'][:32]:32s} {r['dir'][:9]:9s} "
               f"{nome:30s} {pun} {dist}  {nota}")

    testo = "\n".join(RIGHE)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.write(testo + "\n")
    RAPPORTO.write_text(testo + "\n", encoding="utf-8")
    print(f"\nRapporto salvato: {RAPPORTO}")
    print(f"JSON salvato: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
