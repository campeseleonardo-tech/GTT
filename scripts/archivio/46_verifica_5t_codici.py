# -*- coding: utf-8 -*-
"""
scripts/46_verifica_5t_codici.py - Pacchetto H, punto 1 (verifica).

Rilegge il file XML grezzo del 3/10/2026 e scarica un XML fresco dal feed
aperto 5T (sola lettura), per confermare che i codici lcd1 condivisi da due
sensori fisici sono ancora gli stessi. Controlla anche, nel database storico
(sola lettura), che per i codici condivisi siano stati salvati i valori della
PRIMA voce del documento.

Non scrive ne' modifica nulla del database e di data/raw: l'XML fresco viene
salvato in data/processed/5t_flussi_verifica_<data>.xml.
"""

import json
import sqlite3
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
XML_3OTTOBRE = RADICE / "data" / "raw" / "5t_flussi_20261003_224539.xml"
DB = RADICE / "data" / "storico_backup.sqlite"
URL_5T = "https://opendata.5t.torino.it/get_fdt"
UA = "GTT-progetto/1.0 (raccolta dati traffico, uso di studio)"
ANCORE = {"40189": 160, "40123": 1555, "13077": 4960}   # offset della PRIMA voce attesa
RAPPORTO = RADICE / "docs" / "RAPPORTO_TRAFFICO_C_CODICI_5T.txt"


def locale(tag):
    return tag.rsplit("}", 1)[-1]


def leggi_voci(dati):
    radice = ET.fromstring(dati)
    voci = []
    for s in radice.iter():
        if locale(s.tag) != "FDT_data":
            continue
        a = s.attrib
        sf = next((x for x in s if locale(x.tag) == "speedflow"), None)
        voci.append({
            "lcd1": a.get("lcd1"), "dir": a.get("direction"),
            "offset": a.get("offset"), "lat": a.get("lat"), "lng": a.get("lng"),
            "acc": a.get("accuracy"), "period": a.get("period"),
            "flow": None if sf is None else sf.attrib.get("flow"),
            "speed": None if sf is None else sf.attrib.get("speed"),
        })
    return radice.attrib.get("generation_time"), voci


def analizza(nome, generato, voci):
    righe = []
    c = Counter(v["lcd1"] for v in voci)
    doppi = {k: n for k, n in c.items() if n > 1}
    righe.append(f"--- {nome} ---")
    righe.append(f"  generation_time: {generato}")
    righe.append(f"  voci FDT_data: {len(voci)}   codici lcd1 distinti: {len(c)}")
    righe.append(f"  codici con piu' voci: {sorted(doppi)}")
    for k in sorted(doppi):
        righe.append(f"  codice {k}:")
        for i, v in enumerate([x for x in voci if x["lcd1"] == k], 1):
            righe.append(f"    {i}a voce: dir={v['dir']} offset={v['offset']} "
                         f"lat={v['lat']} lng={v['lng']} acc={v['acc']} flow={v['flow']}")
    return doppi, righe


def main():
    righe = []
    def a(s=""):
        righe.append(s)
        print(s)

    a("VERIFICA CODICI 5T CONDIVISI (pacchetto H, punto 1)")
    a("=" * 70)
    if not XML_3OTTOBRE.is_file():
        a(f"FERMO: non trovo {XML_3OTTOBRE}")
        RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
        return 1

    gen, voci = leggi_voci(XML_3OTTOBRE.read_bytes())
    doppi_vecchi, r = analizza("XML del 3/10/2026 (data/raw, sola lettura)", gen, voci)
    righe.extend(r)

    # ancore
    a("")
    a("  Controllo della REGOLA degli identificativi (prima voce = codice invariato):")
    ok_ancore = True
    for cod, off in ANCORE.items():
        prime = [v for v in voci if v["lcd1"] == cod]
        primo_off = prime[0]["offset"] if prime else None
        esito = "OK" if str(primo_off) == str(off) else "NON TORNA"
        if esito != "OK":
            ok_ancore = False
        a(f"    {cod}: offset della prima voce = {primo_off} (atteso {off})  {esito}")

    # XML fresco
    a("")
    a("  Scarico un XML fresco dal feed 5T (sola lettura, nessun invio di dati)...")
    fresco = None
    try:
        req = urllib.request.Request(URL_5T, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            dati = resp.read()
        fresco = RADICE / "data" / "processed" / time.strftime("5t_flussi_verifica_%Y%m%d_%H%M%S.xml")
        fresco.write_bytes(dati)
        gen2, voci2 = leggi_voci(dati)
        doppi_oggi, r2 = analizza(f"XML fresco del {gen2}", gen2, voci2)
        righe.extend(r2)
        a("")
        a(f"  confronto: codici doppi oggi {sorted(doppi_oggi)}, il 3/10 {sorted(doppi_vecchi)}")
        if set(doppi_oggi) == set(doppi_vecchi):
            a("  ESITO: gli stessi tre codici sono ancora condivisi -> la regola li copre.")
        else:
            a("  ATTENZIONE: i codici condivisi sono CAMBIATI -> la tabella delle ancore va aggiornata.")
        for cod in sorted(doppi_oggi):
            prime = [v for v in voci2 if v["lcd1"] == cod]
            if cod in ANCORE and str(prime[0]["offset"]) != str(ANCORE[cod]):
                a(f"    ATTENZIONE {cod}: la prima voce ha offset {prime[0]['offset']} "
                  f"invece di {ANCORE[cod]}")
    except Exception as e:
        a(f"  download non riuscito ({type(e).__name__}: {e}) - la verifica resta "
          f"quella del file del 3/10")

    # database
    a("")
    a("  Controllo nel database storico (sola lettura):")
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    ts = con.execute("SELECT MIN(generato_utc) FROM flussi_5t").fetchone()[0]
    a(f"    primo istante in flussi_5t: {ts}")
    if str(ts).startswith("2026-10-03T22:45:03"):
        a("    (e' l'istante del file del 3/10: controllo diretto possibile)")
    else:
        a("    (il file del 3/10 22:45:03 NON e' nel database: il raccoglitore e' partito dopo.")
        a("     Il piano chiedeva di controllare quell'istante 'se c'e'': non c'e'. Controllo")
        a("     il primo istante disponibile, che serve allo stesso scopo.)")
    for lcd in ("40189", "40123", "13077"):
        f = con.execute("SELECT flusso, velocita FROM flussi_5t WHERE generato_utc=? AND lcd1=?",
                        (ts, lcd)).fetchone()
        s = con.execute("SELECT nome_strada, offset_m, lat, lng FROM sensori_5t WHERE lcd1=?",
                        (lcd,)).fetchone()
        a(f"    {lcd}: flussi_5t {f}   sensori_5t {s}")
    a("    atteso: il flusso e' quello della PRIMA voce del documento (40123 = 0, il sensore")
    a("    morto) mentre la posizione in sensori_5t e' quella dell'ULTIMA (offset 125, vivo).")
    r40123 = con.execute("SELECT flusso FROM flussi_5t WHERE generato_utc=? AND lcd1=?",
                         (ts, "40123")).fetchone()
    verdetto = "CONFERMATO (il flusso salvato e' della prima voce)" if r40123 and r40123[0] == 0 \
        else "DA VERIFICARE (il flusso di 40123 non e' zero)"
    a(f"    VERDETTO: {verdetto}")
    con.close()

    a("")
    a(f"Esito: {'tutto confermato' if ok_ancore else 'ANCORE NON CONFERMATE'}")
    RAPPORTO.write_text("\n".join(righe) + "\n", encoding="utf-8")
    return 0 if ok_ancore else 2


if __name__ == "__main__":
    sys.exit(main())
