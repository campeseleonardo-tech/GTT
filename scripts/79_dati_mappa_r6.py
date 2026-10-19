#!/usr/bin/env python3
"""
79_dati_mappa_r6.py  -  Risultato 6: il file piccolo che leggono la mappa e la scheda.

Cosa fa
-------
Prende quello che ha calcolato lo script 80 e lo mette in un unico file JSON compatto, pronto
per essere disegnato sulla mappa e raccontato nella scheda. Non fa calcoli nuovi.

Il file contiene:
  - aree (celle esagonali di circa 2 km²): centro, poligono, fermate, categoria, parcheggi pieni;
  - punti_prioritari (20): dove servirebbe di più un parcheggio, con i candidati ad ampliarsi;
  - fermate (378): fermate importanti, classe (nessun parcheggio / pochi posti / 50 posti o più);
  - parcheggi (mostrati): almeno 100 posti entro 400 m da una fermata importante o da un nodo di trasporto importante,
    più i garage 5T con dati di riempimento;
  - profili (garage 5T con dati) e profili_medi (per firma);
  - riepilogo, criteri, etichette, fonti, generato.
Le direzioni d'ingresso NON vanno in mappa: restano nel riepilogo (riferimento_direzioni) per la scheda.

Cosa legge
----------
  data/processed/risultato6_v2/porte.json   (prodotto dallo script 80)

Cosa scrive
-----------
  data/processed/risultato6_v2/mappa_r6.json

Come si lancia
--------------
  python scripts\\79_dati_mappa_r6.py
"""
import json
import sys
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
P = RADICE / "data" / "processed" / "risultato6_v2"
PORTE = P / "porte.json"
OUT = P / "mappa_r6.json"
LIMITE_BYTE = 1_500_000

CLASSI = ("Nessun parcheggio", "Pochi posti", "50 posti o più")

ETICHETTE = {
    "aree": "celle esagonali di circa 2 km² con almeno una fermata importante; colore = quota di fermate "
            "senza 50 posti entro 200 m (Critica ≥ 60%, Scarsa 30-59%, Buona < 30%); bordo tratteggiato = meno di 3 fermate",
    "classe": "posti nominali entro 200 m: nessun parcheggio (0), pochi posti (1-49), 50 posti o più",
    "posti": "posti dichiarati dove ci sono, altrimenti stimati dalla superficie (25 m² a posto, ±30%)",
    "stato": "riempimento di giorno: pieno ≥ 85%, a metà, con posti liberi < 50%, non misurato",
    "riempimento": "misura 5T, media feriale 10-16 [DATI SCARSI]",
    "profilo_feriale": "occupazione media ora per ora, giorno feriale [DATI SCARSI]",
    "profilo_weekend": "occupazione media ora per ora, weekend [DATI SCARSI]",
    "nodo_vicino": "nodo di trasporto importante entro 400 m: metro, treno, capolinea o molte corse (almeno 20 corse all'ora) oppure nessuno",
}


def main():
    if not PORTE.exists():
        sys.exit(f"Manca: {PORTE} (lancia prima scripts\\80_porte_interscambio.py)")

    d = json.loads(PORTE.read_text(encoding="utf-8"))

    fermate = [{"id": f["id"], "nome": f["nome"], "lat": f["lat"], "lon": f["lon"],
                "zona_nome": f["zona_nome"], "punteggio": f["punteggio"], "classe": f["classe"],
                "posti_nominali_200": f["posti_nominali_200"],
                "parcheggi": [{"id": p["id"], "nome": p["nome"], "dist_m": p["dist_m"],
                               "posti": p["posti"], "stato": p["stato"]} for p in f["parcheggi"]]}
               for f in d["fermate"]]

    parcheggi = [{"id": p["id"], "nome": p["nome"], "lat": p["lat"], "lon": p["lon"], "posti": p["posti"],
                  "posti_origine": p["posti_origine"], "a_pagamento": p["a_pagamento"], "stato": p["stato"],
                  "riempimento_giorno": p["riempimento_giorno"],
                  "dist_fermata_importante_m": p["dist_fermata_importante_m"], "nodo_vicino": p["nodo_vicino"],
                  "profilo_feriale": p["profilo_feriale"], "profilo_weekend": p["profilo_weekend"],
                  "descrizione": p["descrizione"]}
                 for p in d["parcheggi"]]

    aree = [{"id": a["id"], "centro": a["centro"], "poligono": a["poligono"], "n_fermate": a["n_fermate"],
             "nessun": a["nessun"], "pochi": a["pochi"], "ok": a["ok"], "quota_senza": a["quota_senza"],
             "categoria": a["categoria"], "indicativo": a["indicativo"],
             "zone_principali": a["zone_principali"], "etichetta": a["etichetta"],
             "mostra_etichetta": a["mostra_etichetta"], "posti_nominali_200": a["posti_nominali_200"],
             "parcheggi_pieni": a["parcheggi_pieni"], "fermate_senza": a["fermate_senza"]}
            for a in d["aree"]]

    mappa = {
        "generato": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "fonti": ["data/processed/risultato6_v2/porte.json", "scripts/80_porte_interscambio.py"],
        "etichette": ETICHETTE,
        "soglia_aree": d["soglia_aree"],
        "aree": aree,
        "punti_prioritari": d["punti_prioritari"],
        "fermate": fermate,
        "parcheggi": parcheggi,
        "profili": d["profili"],
        "criteri": d["criteri"],
        "riepilogo": d["riepilogo"],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(mappa, ensure_ascii=False), encoding="utf-8")
    dim = OUT.stat().st_size
    if dim > LIMITE_BYTE:
        sys.exit(f"mappa_r6.json pesa {dim} byte (limite 1,5 MB): togli i campi piu' pesanti")

    conta = {c: sum(1 for f in fermate if f["classe"] == c) for c in CLASSI}
    somma_aree = sum(a["n_fermate"] for a in aree)
    atteso = (len(fermate), conta[CLASSI[0]], conta[CLASSI[1]], conta[CLASSI[2]]) == (378, 147, 59, 172) and \
        somma_aree == 378 and len(punti := mappa["punti_prioritari"]) == 20 and \
        "direzioni" not in mappa and 190 <= len(parcheggi) <= 240
    print(f"mappa_r6.json: {dim} byte ({dim/1024:.0f} KB)")
    print(f"  aree {len(aree)}, punti prioritari {len(punti)}, fermate {len(fermate)} "
          f"(nessun parcheggio {conta[CLASSI[0]]} / pochi {conta[CLASSI[1]]} / 50+ {conta[CLASSI[2]]}), "
          f"parcheggi mostrati {len(parcheggi)}, profili {len(mappa['profili'])}")
    print(f"  chiavi: {list(mappa.keys())}; controlli {'OK' if atteso else 'NO'}")
    if not atteso:
        sys.exit("Controlli non tornano: fermarsi")
    print(f"Scritto: {OUT}")


if __name__ == "__main__":
    sys.exit(main())
