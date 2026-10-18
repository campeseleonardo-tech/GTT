# -*- coding: utf-8 -*-
"""
scripts/47_prova_raccolta_5t_su_copia.py - Pacchetto H, punto 5.

Prova la funzione patchata di scripts/03_raccolta_continua.py su un DATABASE
VUOTO con lo stesso schema (NON usa il database storico da 1,6 GB).

Controlli:
 1. primo giro con l'XML del 3/10: 112 righe in sensori_5t, 112 in flussi_5t,
    112 in accuratezza_5t, con i 3 codici '~2';
 2. secondo giro con lo stesso XML: 0 righe nuove (idempotente);
 3. un XML modificato a mano con un duplicato in piu': nasce '<codice>~3' e
    compare la riga di log.

Il database di prova viene creato in
data/processed/traffico_c/prova_5t_codici.sqlite (si puo' cancellare).
"""

import importlib.util
import io
import contextlib
import copy
import sqlite3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
XML = RADICE / "data" / "raw" / "5t_flussi_20261003_224539.xml"
DB_PROVA = RADICE / "data" / "processed" / "traffico_c" / "prova_5t_codici.sqlite"


def carica_modulo():
    spec = importlib.util.spec_from_file_location("raccolta03", AQUI / "03_raccolta_continua.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def conteggi(con):
    s = con.execute("SELECT COUNT(*) FROM sensori_5t").fetchone()[0]
    f = con.execute("SELECT COUNT(*) FROM flussi_5t").fetchone()[0]
    a = con.execute("SELECT COUNT(*) FROM accuratezza_5t").fetchone()[0]
    code2 = [r[0] for r in con.execute("SELECT lcd1 FROM sensori_5t WHERE lcd1 LIKE '%~%' ORDER BY lcd1")]
    return s, f, a, code2


def main():
    mod = carica_modulo()
    DB_PROVA.parent.mkdir(parents=True, exist_ok=True)
    if DB_PROVA.is_file():
        DB_PROVA.unlink()
    mod.DB = DB_PROVA
    con = mod.apri_db()
    dati = XML.read_bytes()

    righe = []
    def a(s=""):
        righe.append(s)
        print(s)

    a("PROVA DEL RACCOGLITORE PATCHATO SU UN DATABASE VUOTO (pacchetto H, punto 5)")
    a("=" * 74)
    a(f"database di prova: {DB_PROVA}")

    # --- giro 1 ---
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        n1 = mod.salva_5t_da_bytes(con, dati)
    log1 = buf.getvalue().strip().splitlines()
    s, f, a1, code2 = conteggi(con)
    a("")
    a("1) primo giro con l'XML del 3/10:")
    a(f"   misure salvate: {n1}   sensori_5t {s}   flussi_5t {f}   accuratezza_5t {a1}")
    a(f"   codici con '~': {code2}")
    a(f"   righe di log: {len(log1)}")
    for r in log1[:5]:
        a("     " + r)
    ok1 = (n1 == 112 and s == 112 and f == 112 and a1 == 112 and len(code2) == 3)

    # --- giro 2 (idempotente) ---
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        n2 = mod.salva_5t_da_bytes(con, dati)
    s2, f2, a2, code2b = conteggi(con)
    a("")
    a("2) secondo giro con lo stesso XML:")
    a(f"   misure nuove: {n2}   sensori_5t {s2}   flussi_5t {f2}   accuratezza_5t {a2}")
    ok2 = (n2 == 0 and s2 == 112 and f2 == 112 and a2 == 112)

    # --- giro 3: XML con un duplicato in piu' ---
    radice = ET.fromstring(dati)
    voci = [e for e in radice.iter() if e.tag.rsplit('}', 1)[-1] == 'FDT_data']
    normale = next(e for e in voci if e.attrib.get("lcd1") == "40021")
    for _ in range(2):
        radice.append(copy.deepcopy(normale))
    radice.attrib["generation_time"] = "2026-10-17T00:00:00.000Z"
    xml2 = ET.tostring(radice)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        n3 = mod.salva_5t_da_bytes(con, xml2)
    log3 = buf.getvalue().strip().splitlines()
    s3, f3, a3, code2c = conteggi(con)
    a("")
    a("3) XML modificato a mano (40021 ripetuto 3 volte):")
    a(f"   misure salvate: {n3}   sensori_5t {s3}   flussi_5t {f3}   accuratezza_5t {a3}")
    a(f"   codici con '~': {code2c}")
    for r in log3:
        a("     " + r)
    ok3 = ("40021~2" in code2c and "40021~3" in code2c and s3 == 114
           and any("40021" in r for r in log3))

    # --- controllo ancore: offset associati ---
    a("")
    a("4) posizione salvata per i codici condivisi (deve essere quella di OGNI voce):")
    for cod in ("40189", "40189~2", "40123", "40123~2", "13077", "13077~2"):
        r = con.execute("SELECT offset_m, lat, lng FROM sensori_5t WHERE lcd1=?", (cod,)).fetchone()
        a(f"   {cod:10s} {r}")
    ok4 = True
    att = {"40189": 160.0, "40189~2": 970.0, "40123": 1555.0, "40123~2": 125.0,
           "13077": 4960.0, "13077~2": 5150.0}
    for cod, off in att.items():
        r = con.execute("SELECT offset_m FROM sensori_5t WHERE lcd1=?", (cod,)).fetchone()
        if not r or float(r[0]) != off:
            ok4 = False
            a(f"   ATTESO {cod} offset {off}, trovato {None if not r else r[0]}")
    con.close()

    a("")
    a(f"ESITO: giro1 {'OK' if ok1 else 'NO'} · giro2 {'OK' if ok2 else 'NO'} · "
      f"giro3 {'OK' if ok3 else 'NO'} · ancore {'OK' if ok4 else 'NO'}")
    (RADICE / "docs" / "RAPPORTO_TRAFFICO_C_PROVA_RACCOLTA.txt").write_text(
        "\n".join(righe) + "\n", encoding="utf-8")
    return 0 if (ok1 and ok2 and ok3 and ok4) else 1


if __name__ == "__main__":
    sys.exit(main())
