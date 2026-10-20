#!/usr/bin/env python3
"""38_verifica_provinciali.py

Passo 8b del piano docs/PIANO_TRAFFICO_FASE2.md: decide, con i dati OSM veri, se i
sensori delle strade provinciali che erano "in attesa" stanno davvero sulla strada
che il nome dice.

Sensori controllati:
- i 5 in attesa di verifica (35478, 35479, 36066, 36067, 35824);
- i 5 sensori con "(TO)" nel nome ma classificati NESSUNO dal Passo 8
  (35518, 35519, 35559, 35560, 35823).

Cosa fa: legge il file OSM `data/otp/rete/torino_cintura.osm.pbf` con pyosmium
(l'unico pacchetto non di serie usato in Fase 2: e' il passo che lo chiede; e' gia'
installato) e per ogni sensore elenca le strade (tag `highway`) entro 60 m, con
nome, `ref`, tipo e distanza.

Regola: un sensore del tipo `SPn(...)` e' CONFERMATO se una strada entro 60 m ha
`ref` uguale a `SPn` (spazi e maiuscole ignorati) E appartiene al corridoio
proposto (nome normalizzato uguale alla chiave del corridoio). Altrimenti resta
DUBBIO / senza abbinamento.

NON modifica lo script 03 ne' il database (sola lettura). Non sovrascrive
`abbinamenti_confermati.json`: scrive `abbinamenti_confermati_v2.json`.

Output:
- docs/RAPPORTO_VERIFICA_PROVINCIALI.txt
- data/processed/abbinamenti_confermati_v2.json
"""

import importlib.util
import json
import math
import re
import sqlite3
import sys
from pathlib import Path

import osmium

RADICE = Path(__file__).resolve().parents[1]
DB = RADICE / "data" / "storico_backup.sqlite"
PBF = RADICE / "data" / "otp" / "rete" / "torino_cintura.osm.pbf"
IN_V2 = RADICE / "data" / "processed" / "sensori_corridoi_v2.json"
IN_CONF = RADICE / "data" / "processed" / "abbinamenti_confermati.json"
OUT = RADICE / "data" / "processed" / "abbinamenti_confermati_v2.json"
RAPPORTO = RADICE / "docs" / "RAPPORTO_VERIFICA_PROVINCIALI.txt"

SOGLIA_M = 60
IN_ATTESA = ["35478", "35479", "36066", "36067", "35824"]
NESSUNO_URBANI = ["35518", "35519", "35559", "35560", "35823"]
RIGHE = []


def scrivi(msg=""):
    RIGHE.append(str(msg))


def carica_script_24():
    percorso = RADICE / "scripts" / "24_importanza_vie.py"
    spec = importlib.util.spec_from_file_location("m24_importanza_vie", percorso)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def hav(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def ref_norm(x):
    """'SP1' / 'sp 1' -> 'SP1'."""
    return re.sub(r"\s+", "", (x or "")).upper()


def ref_dal_nome(nome):
    """'SP1(TO) delle Valli di Lanzo' -> 'SP1'."""
    m = re.search(r"\bSP\s?(\d+)", (nome or "").upper())
    return f"SP{m.group(1)}" if m else None


def main():
    m24 = carica_script_24()

    for p in (DB, PBF, IN_V2, IN_CONF):
        if not p.is_file():
            raise SystemExit(f"File non trovato: {p}")

    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=60)
    sensori = {}
    for l, n, d, la, lo in con.execute(
            "SELECT lcd1, nome_strada, direzione, lat, lng FROM sensori_5t"):
        if str(l) in IN_ATTESA + NESSUNO_URBANI:
            sensori[str(l)] = dict(nome=n or "", dir=d or "?", lat=la, lon=lo)
    con.close()
    if len(sensori) != 10:
        raise SystemExit(f"Attesi 10 sensori da controllare, trovati {len(sensori)}")

    corridoi = json.loads(IN_V2.read_text(encoding="utf-8"))["sensori"]

    # --- passata 1: i nodi OSM vicini ai sensori ---
    box = [(s["lat"], s["lon"]) for s in sensori.values()]
    nodi = {}

    class Nodi(osmium.SimpleHandler):
        def node(self, n):
            la, lo = n.location.lat, n.location.lon
            for bla, blo in box:
                if abs(la - bla) < 0.003 and abs(lo - blo) < 0.003:
                    nodi[n.id] = (la, lo)
                    return

    Nodi().apply_file(str(PBF))

    # --- passata 2: le strade (highway) che hanno almeno un nodo vicino ---
    vie = []

    class Vie(osmium.SimpleHandler):
        def way(self, w):
            if "highway" not in w.tags:
                return
            punti = [nodi[nd.ref] for nd in w.nodes if nd.ref in nodi]
            if not punti:
                return
            vie.append(dict(id=w.id, highway=w.tags.get("highway"),
                            name=w.tags.get("name"), ref=w.tags.get("ref"),
                            punti=punti))

    Vie().apply_file(str(PBF))

    # --- analisi per sensore ---
    esiti = {}
    for lcd1 in IN_ATTESA + NESSUNO_URBANI:
        s = sensori[lcd1]
        ref_atteso = ref_dal_nome(s["nome"])
        prop = corridoi.get(lcd1, {})
        corr = prop.get("corridoio") or {}
        trovate = []
        for w in vie:
            dm = min(hav(s["lat"], s["lon"], p[0], p[1]) for p in w["punti"])
            if dm <= SOGLIA_M:
                trovate.append(dict(distanza_m=round(dm, 1), highway=w["highway"],
                                    name=w["name"], ref=w["ref"],
                                    ref_norm=ref_norm(w["ref"]),
                                    nome_norm=m24.normalizza(w["name"])))
        trovate.sort(key=lambda t: t["distanza_m"])

        con_ref = [t for t in trovate if ref_atteso and t["ref_norm"] == ref_atteso]
        appartiene = [t for t in con_ref
                      if corr and t["nome_norm"] == m24.normalizza(corr.get("nome"))]

        if appartiene:
            esito = "CONFERMATO"
            migliore = appartiene[0]
            motivo = (f"strada con ref {ref_atteso} a {migliore['distanza_m']} m "
                      f"({migliore['name']!r}) = corridoio proposto {corr.get('nome')!r}")
        elif con_ref:
            esito = "strada senza nome nei corridoi"
            migliore = con_ref[0]
            motivo = (f"strada con ref {ref_atteso} a {migliore['distanza_m']} m "
                      f"({migliore['name']!r}) ma non e' il corridoio proposto "
                      f"({(corr or {}).get('nome')!r})")
        else:
            esito = "senza abbinamento"
            migliore = trovate[0] if trovate else None
            motivo = (f"nessuna strada con ref {ref_atteso} entro {SOGLIA_M} m" +
                      (f" (la piu' vicina: {migliore['name']!r} "
                       f"{migliore['distanza_m']} m, ref {migliore['ref']!r})" if migliore else ""))
        esiti[lcd1] = dict(lcd1=lcd1, nome_sensore=s["nome"], dir=s["dir"],
                           lat=s["lat"], lon=s["lon"], ref_atteso=ref_atteso,
                           corridoio_proposto=(corr or None),
                           vie_entro_60m=trovate[:6], esito=esito, motivo=motivo)
        # se il compagno di verso ha un esito piu' prudente, vale per entrambi
    ordine = {"CONFERMATO": 0, "strada senza nome nei corridoi": 1, "senza abbinamento": 2}
    per_nome = {}
    for l, e in esiti.items():
        per_nome.setdefault(e["nome_sensore"], []).append(l)
    note_coppia = []
    for nome, lista in per_nome.items():
        if len(lista) < 2:
            continue
        peggiore = max(esiti[l]["esito"] for l in lista)
        if any(esiti[l]["esito"] != peggiore for l in lista):
            for l in lista:
                note_coppia.append((nome, l, esiti[l]["esito"], peggiore))
                esiti[l]["esito"] = peggiore
                esiti[l]["motivo"] += f" | esito allineato al compagno di verso ({peggiore})"

    # --- file v2 ---
    vecchio = json.loads(IN_CONF.read_text(encoding="utf-8"))
    nuovi_confermati = [l for l in IN_ATTESA if esiti[l]["esito"] == "CONFERMATO"]
    v2 = dict(vecchio)
    v2["autore"] = vecchio.get("autore", "") + " + Passo 8b (verifica OSM)"
    v2["confermati"] = list(vecchio.get("confermati", [])) + [
        dict(lcd1=l, motivo=esiti[l]["motivo"]) for l in nuovi_confermati]
    v2["in_attesa_verifica_osm"] = [l for l in IN_ATTESA if esiti[l]["esito"] != "CONFERMATO"]
    v2["senza_abbinamento"] = [l for l in NESSUNO_URBANI if esiti[l]["esito"] != "CONFERMATO"]
    v2["verifica_osm"] = {l: esiti[l] for l in esiti}
    v2["nota"] += (" Il Passo 8b ha verificato con OSM i 5 in attesa: "
                   f"{len(nuovi_confermati)} confermati, "
                   f"{len(v2['in_attesa_verifica_osm'])} no. "
                   "I 5 sensori '(TO)' erano e restano senza abbinamento.")
    OUT.write_text(json.dumps(v2, ensure_ascii=False, indent=1), encoding="utf-8")

    # --- rapporto ---
    scrivi("VERIFICA OSM DEI SENSORI DELLE PROVINCIALI (Passo 8b)")
    scrivi("=" * 84)
    scrivi(f"OSM: {PBF.name} (letto con pyosmium, sola lettura)")
    scrivi(f"strade con tag highway considerate: {len(vie)}; nodi vicini raccolti: {len(nodi)}")
    scrivi(f"regola: ref OSM uguale a 'SPn' del nome del sensore (spazi/maiuscole ignorati) "
           f"e nome della strada = corridoio proposto; distanza <= {SOGLIA_M} m.")
    scrivi("nota: la distanza e' calcolata dai NODI della strada, non dai segmenti "
           "(approssimazione dichiarata).")
    scrivi("")
    for lcd1 in IN_ATTESA + NESSUNO_URBANI:
        e = esiti[lcd1]
        scrivi(f"{lcd1}  {e['nome_sensore']}  ({e['dir']})   ESITO: {e['esito']}")
        scrivi(f"    corridoio proposto: {(e['corridoio_proposto'] or {}).get('nome')} "
               f"(p{(e['corridoio_proposto'] or {}).get('punteggio')})")
        scrivi(f"    {e['motivo']}")
        for v in e["vie_entro_60m"]:
            scrivi(f"      {v['distanza_m']:6.1f} m  {v['highway']:12s} ref={v['ref']!s:8s} "
                   f"name={v['name']!r}")
        scrivi("")
    if note_coppia:
        scrivi("Coppie con esito diverso, allineate al piu' prudente:")
        for nome, l, prima, dopo in note_coppia:
            scrivi(f"  {l} ({nome}): {prima} -> {dopo}")
        scrivi("")
    scrivi("Riepilogo: " + ", ".join(
        f"{k} {sum(1 for e in esiti.values() if e['esito'] == k)}"
        for k in ("CONFERMATO", "strada senza nome nei corridoi", "senza abbinamento")))

    testo = "\n".join(RIGHE)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.write(testo + "\n")
    RAPPORTO.write_text(testo + "\n", encoding="utf-8")
    print(f"Rapporto salvato: {RAPPORTO}")
    print(f"JSON salvato: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
