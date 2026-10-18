#!/usr/bin/env python3
"""
71_parcheggi_riempimento.py  -  Risultato 6 v2, PASSO 3: ANTEPRIMA del riempimento.

Cosa fa
-------
Legge dal database le letture di occupazione dei parcheggi 5T (quanti posti liberi,
ogni pochi minuti) e costruisce, per ogni parcheggio, il profilo orario medio del
riempimento separato fra giorni feriali e fine settimana. Da quel profilo ricava una
"firma": pendolare / residenziale / destinazione / misto / dato_bloccato / nessun_dato.
Attenzione: sono POCHI giorni di raccolta (dal 14/10), quindi e' un'ANTEPRIMA [DATI SCARSI]
e le soglie delle firme sono provvisorie.

Cosa legge
----------
  data/storico_backup.sqlite (sola lettura): tabelle parcheggi_5t e occupazione_pk

Cosa scrive
-----------
  data/processed/risultato6_v2/riempimento.json
  docs/RAPPORTO_R6V2_RIEMPIMENTO.txt

Come si lancia
--------------
  python scripts\\71_parcheggi_riempimento.py
"""
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
DB = RADICE / "data" / "storico_backup.sqlite"
OUT = RADICE / "data" / "processed" / "risultato6_v2" / "riempimento.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_R6V2_RIEMPIMENTO.txt"

LETTURE_MINIME_GIORNO = 230     # su ~288 possibili (una ogni 5 minuti)
ORE_NOTTE = (2, 3, 4)           # N
ORE_GIORNO = (10, 11, 12, 13, 14, 15)   # G
ORE_MATTINA = (7, 8)            # M


# [agente] ora legale italiana, stessa regola di scripts/04_genera_mappa.py (_locale)
def _ultima_domenica(anno, mese):
    d = datetime(anno, mese, 31).date()
    while d.weekday() != 6:
        d -= timedelta(days=1)
    return d


def ora_locale(dt_utc):
    a = dt_utc.year
    inizio = datetime(a, 3, _ultima_domenica(a, 3).day, 1, tzinfo=timezone.utc)
    fine = datetime(a, 10, _ultima_domenica(a, 10).day, 1, tzinfo=timezone.utc)
    return dt_utc + timedelta(hours=2 if inizio <= dt_utc < fine else 1)


def leggi_database():
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        parcheggi = c.execute("select id, nome, lat, lng, totale from parcheggi_5t").fetchall()
        letture = c.execute(
            "select generato_utc, id, stato, totale, liberi from occupazione_pk").fetchall()
    finally:
        c.close()
    return parcheggi, letture


def firma_da(N, G, M, W, ampiezza, ha_weekend, ha_letture, giorni_feriali_validi):
    """Regole del piano, soglie PROVVISORIE (le confermera' Leo)."""
    if not ha_letture:
        return "nessun_dato"
    if giorni_feriali_validi < 2:
        return "dati_insufficienti"
    if ampiezza < 0.05:
        return "dato_bloccato"
    if G - N >= 0.20 and (not ha_weekend or G - W >= 0.10):
        return "pendolare"
    if N - G >= 0.10:
        return "residenziale"
    if G - N >= 0.20 and ha_weekend and G - W < 0.10:
        return "destinazione"
    return "misto"


def stato_da(G):
    """In piu' rispetto alla firma: pieno / vuoto, in base al giorno feriale."""
    if G is None:
        return None
    if G >= 0.85:
        return "pieno"
    if G < 0.15:
        return "vuoto"
    return None


def main():
    if not DB.exists():
        sys.exit(f"Manca: {DB}")
    parcheggi, letture = leggi_database()
    print(f"parcheggi 5T nel database: {len(parcheggi)}; righe di occupazione: {len(letture)}")

    dati = {}
    for pid, nome, lat, lng, totale in parcheggi:
        dati[pid] = {"id_5t": pid, "nome": nome, "lat": lat, "lon": lng,
                     "totale_db": totale, "letture": [], "azioni": 0}
    scartate = 0
    for generato, pid, stato, totale, liberi in letture:
        if pid not in dati:
            continue
        if stato != 1 or liberi is None:
            scartate += 1
            continue
        tot = totale or dati[pid]["totale_db"]
        if not tot:
            scartate += 1
            continue
        dt = datetime.strptime(generato[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        loc = ora_locale(dt)
        occ = max(0.0, min(1.0, 1.0 - liberi / tot))
        dati[pid]["letture"].append((loc, occ))
    print(f"letture scartate (stato 0 o liberi nulli): {scartate}")

    risultati = []
    for pid, d in dati.items():
        letture_pk = d["letture"]
        per_giorno = {}
        for loc, occ in letture_pk:
            per_giorno.setdefault(loc.date(), []).append((loc.hour, occ))
        giorni_validi = sorted(g for g, v in per_giorno.items() if len(v) >= LETTURE_MINIME_GIORNO)

        def media_ore(ore, weekend):
            vals = [occ for g in giorni_validi
                    for h, occ in per_giorno[g]
                    if h in ore and ((g.weekday() >= 5) == weekend)]
            return sum(vals) / len(vals) if vals else None

        def profilo(weekend):
            prof = {}
            for h in range(24):
                vals = [occ for g in giorni_validi for hh, occ in per_giorno[g]
                        if hh == h and ((g.weekday() >= 5) == weekend)]
                if vals:
                    prof[h] = sum(vals) / len(vals)
            return prof

        prof_f = profilo(False)
        prof_w = profilo(True)
        N = media_ore(ORE_NOTTE, False)
        G = media_ore(ORE_GIORNO, False)
        M = media_ore(ORE_MATTINA, False)
        W = media_ore(ORE_GIORNO, True)
        feriali_validi = [g for g in giorni_validi if g.weekday() < 5]
        weekend_validi = [g for g in giorni_validi if g.weekday() >= 5]
        ampiezza = (max(prof_f.values()) - min(prof_f.values())) if len(prof_f) >= 2 else 0.0
        firma = firma_da(N, G, M, W, ampiezza, bool(weekend_validi),
                         bool(letture_pk), len(feriali_validi))
        stato = stato_da(G)
        risultati.append({
            "id_5t": pid, "nome": d["nome"], "lat": d["lat"], "lon": d["lon"],
            "totale_posti": d["totale_db"],
            "n_letture": len(letture_pk),
            "giorni_validi": [str(g) for g in giorni_validi],
            "profilo_feriale": {str(h): round(v, 4) for h, v in sorted(prof_f.items())},
            "profilo_weekend": {str(h): round(v, 4) for h, v in sorted(prof_w.items())},
            "N_notte_feriale": round(N, 4) if N is not None else None,
            "G_giorno_feriale": round(G, 4) if G is not None else None,
            "M_mattina_feriale": round(M, 4) if M is not None else None,
            "W_giorno_weekend": round(W, 4) if W is not None else None,
            "ampiezza": round(ampiezza, 4),
            "firma": firma, "stato": stato,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "anteprima": True,
        "etichetta": "ANTEPRIMA [DATI SCARSI]",
        "letture_minime_giorno": LETTURE_MINIME_GIORNO,
        "parcheggi": risultati,
    }, ensure_ascii=False), encoding="utf-8")

    # --- rapporto ---
    usati = [r for r in risultati if r["giorni_validi"]]
    giorni_tutti = sorted({g for r in risultati for g in r["giorni_validi"]})
    feriali = [g for g in giorni_tutti if datetime.strptime(g, "%Y-%m-%d").weekday() < 5]
    righe = []
    righe.append("RAPPORTO R6 v2 — RIEMPIMENTO DEI PARCHEGGI 5T (Passo 3)")
    righe.append(f"ANTEPRIMA [DATI SCARSI]: {len(feriali)} giorni feriali validi, "
                 f"dal {feriali[0] if feriali else '-'} al {feriali[-1] if feriali else '-'}")
    righe.append(f"giorni validi in tutto (feriali + fine settimana): {', '.join(giorni_tutti) or '-'}")
    righe.append("il 14/10/2026 la raccolta e' iniziata a meta' pomeriggio, quindi quel giorno "
                 "non raggiunge le letture minime e non conta; la domenica 18/10 e' anch'essa incompleta")
    righe.append(f"ogni parcheggio ha letture ogni ~5 minuti; un giorno conta se ha almeno "
                 f"{LETTURE_MINIME_GIORNO} letture")
    righe.append("Le soglie delle firme sono PROVVISORIE: le conferma Leo dopo questa anteprima.")
    righe.append("")
    righe.append("== Firma per parcheggio ==")
    righe.append("  formato: occupazione % ogni 2 ore (feriale), poi la firma")
    ordine = {"pendolare": 0, "residenziale": 1, "destinazione": 2, "misto": 3,
              "dato_bloccato": 4, "dati_insufficienti": 5, "nessun_dato": 6}
    for r in sorted(risultati, key=lambda r: (ordine.get(r["firma"], 9), r["nome"])):
        coppie = []
        for h in range(0, 24, 2):
            vals = [r["profilo_feriale"].get(str(hh)) for hh in (h, h + 1)]
            vals = [v for v in vals if v is not None]
            coppie.append(f"{round(100 * sum(vals) / len(vals)):3d}" if vals else "  -")
        stato = f" [{r['stato']}]" if r["stato"] else ""
        righe.append(f"  {r['nome'][:22]:22s} {' '.join(coppie)}  -> {r['firma']}{stato}")
    righe.append("")
    righe.append("== Valori chiave per parcheggio ==")
    righe.append("  N = notte feriale 02-05, G = giorno feriale 10-16, M = mattina feriale 07-09,"
                 " W = giorno weekend, amp = ampiezza della giornata feriale")
    for r in sorted(risultati, key=lambda r: r["nome"]):
        def pct(v):
            return f"{100 * v:5.1f}" if v is not None else "  n.d."
        righe.append(f"  {r['nome'][:22]:22s} N={pct(r['N_notte_feriale'])} G={pct(r['G_giorno_feriale'])} "
                     f"M={pct(r['M_mattina_feriale'])} W={pct(r['W_giorno_weekend'])} amp={r['ampiezza']:.2f} "
                     f"giorni={len(r['giorni_validi'])} -> {r['firma']}")
    RAPPORTO.parent.mkdir(parents=True, exist_ok=True)
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")

    print(f"Scritto: {OUT}")
    print(f"Scritto: {RAPPORTO}")
    from collections import Counter
    print("firme:", dict(Counter(r["firma"] for r in risultati)))
    for nome in ("FERMI", "RACCONIGI", "UNIONE SOVIETICA", "V PADIGLIONE", "VENCHI UNICA",
                 "SOFIA", "PORTA SUSA FS", "CAIO MARIO", "STURA"):
        r = next((x for x in risultati if x["nome"] == nome), None)
        if r:
            print(f"  {nome:20s} {r['firma']:18s} {r['stato']} N={r['N_notte_feriale']} G={r['G_giorno_feriale']}")


if __name__ == "__main__":
    sys.exit(main())
