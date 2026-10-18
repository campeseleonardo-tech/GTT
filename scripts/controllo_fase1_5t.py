#!/usr/bin/env python3
"""controllo_fase1_5t.py

Strumento di controllo della Fase 1 del piano docs/PIANO_TRAFFICO_5T.md
(sezione 9, passo 1).

Fa tre cose, in SOLA LETTURA su data/storico_backup.sqlite:
- a) conta le righe delle tabelle principali e l'ultimo istante disponibile in
     flussi_5t, confrontandoli con i valori attesi nel piano;
- b) controlla l'aritmetica delle letture 5T: righe senza riga di accuratezza,
     righe con accuratezza = 0, righe con accuratezza > 0 e flusso non nullo;
- c) diagnostica dell'ora 01:00 locale (23:00 UTC): per ogni ora UTC del periodo
     2026-10-09 -> 2026-10-16 riporta il numero di righe di flussi_5t, la quota
     di righe con accuratezza = 0 e il numero di sensori distinti con almeno una
     riga con accuratezza > 0.

Non interpreta i dati: riporta i numeri. Il testo prodotto viene stampato a
console e inserito in docs/ESITO_FASE1_TRAFFICO_5T.md, fra due marcatori, cosi'
da poter rilanciare lo script senza duplicare il blocco.

Solo libreria standard. Nessuna scrittura sul database.
"""

import sqlite3
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
DB = RADICE / "data" / "storico_backup.sqlite"
ESITO = RADICE / "docs" / "ESITO_FASE1_TRAFFICO_5T.md"

INIZIO = "<!-- INIZIO PASSO 1 -->"
FINE = "<!-- FINE PASSO 1 -->"

# a) conteggi attesi (docs/PIANO_TRAFFICO_5T.md, sezione 9 passo 1)
ATTESI = {
    "flussi_5t": 365477,
    "accuratezza_5t": 243179,
    "parcheggi_5t": 41,
    "occupazione_pk": 27921,
    "ztl_5t": 1,
    "trip_update_gtt": 1893353,
    "mezzi_gtt": 4059000,
}
ULTIMO_ATTESO = "2026-10-16T22:36:17.111Z"

# b) attesi
B_SENZA_RIGA = 122298
B_ACC0 = 49254
B_ACC_POS = 193925

# c) periodo (date UTC) e ore da confrontare
C_DA, C_A = "2026-10-09", "2026-10-16"
ORE_DA_CONFRONTARE = (21, 22, 23, 0, 1)

RIGHE = []


def scrivi(msg=""):
    RIGHE.append(str(msg))


def apri_db(percorso):
    if not percorso.is_file():
        raise SystemExit(f"DB non trovato: {percorso}")
    con = sqlite3.connect(f"file:{percorso}?mode=ro", uri=True, timeout=60)
    con.execute("PRAGMA busy_timeout=60000")
    return con


def main():
    con = apri_db(DB)
    cur = con.cursor()

    scrivi("PASSO 1 - CONTROLLO DEL DATABASE E DIAGNOSI ORA 01:00 (sola lettura)")
    scrivi("=" * 72)
    scrivi(f"DB (sola lettura): {DB}")

    # ---------- a) conteggi ----------
    scrivi("\n-- a) conteggi tabelle --")
    esito_a = True
    for tab, atteso in ATTESI.items():
        n = cur.execute(f"SELECT COUNT(*) FROM {tab}").fetchone()[0]
        if tab == "occupazione_pk":
            # puo' essere piu' alto se il DB e' stato riscaricato
            ok = n >= atteso
            nota = "" if n == atteso else " (piu' alto: DB riscaricato)"
        else:
            ok = n == atteso
            nota = ""
        esito_a = esito_a and ok
        scrivi(f"  {tab:18s} {n:>9d}  atteso {atteso:>9d}  "
               f"{'OK' if ok else 'DIVERSO'}{nota}")

    ultimo = cur.execute("SELECT MAX(generato_utc) FROM flussi_5t").fetchone()[0]
    ok_ultimo = ultimo == ULTIMO_ATTESO
    esito_a = esito_a and ok_ultimo
    scrivi(f"  ultimo flussi_5t.generato_utc  {ultimo}")
    scrivi(f"  ultimo atteso                  {ULTIMO_ATTESO}  "
           f"{'OK' if ok_ultimo else 'DIVERSO'}")

    # ---------- b) aritmetica delle letture ----------
    scrivi("\n-- b) aritmetica delle letture 5T --")
    n_senza_riga = cur.execute("""
        SELECT COUNT(*) FROM flussi_5t f
        LEFT JOIN accuratezza_5t a
               ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
        WHERE a.generato_utc IS NULL
    """).fetchone()[0]
    n_acc0 = cur.execute("""
        SELECT COUNT(*) FROM flussi_5t f
        JOIN accuratezza_5t a
          ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
        WHERE a.accuratezza = 0
    """).fetchone()[0]
    n_acc_pos = cur.execute("""
        SELECT COUNT(*) FROM flussi_5t f
        JOIN accuratezza_5t a
          ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
        WHERE a.accuratezza > 0 AND f.flusso IS NOT NULL
    """).fetchone()[0]
    n_acc_pos_flusso_nullo = cur.execute("""
        SELECT COUNT(*) FROM flussi_5t f
        JOIN accuratezza_5t a
          ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
        WHERE a.accuratezza > 0 AND f.flusso IS NULL
    """).fetchone()[0]
    n_tot = cur.execute("SELECT COUNT(*) FROM flussi_5t").fetchone()[0]

    esito_b = (n_senza_riga == B_SENZA_RIGA and n_acc0 == B_ACC0
               and n_acc_pos == B_ACC_POS)
    scrivi(f"  senza riga in accuratezza_5t   {n_senza_riga:>9d}  "
           f"atteso {B_SENZA_RIGA:>9d}  "
           f"{'OK' if n_senza_riga == B_SENZA_RIGA else 'DIVERSO'}")
    scrivi(f"  accuratezza = 0                {n_acc0:>9d}  "
           f"atteso {B_ACC0:>9d}  {'OK' if n_acc0 == B_ACC0 else 'DIVERSO'}")
    scrivi(f"  accuratezza > 0 e flusso       {n_acc_pos:>9d}  "
           f"atteso {B_ACC_POS:>9d}  {'OK' if n_acc_pos == B_ACC_POS else 'DIVERSO'}")
    scrivi(f"  (accuratezza > 0 con flusso NULL: {n_acc_pos_flusso_nullo})")
    scrivi(f"  controllo somma: {n_senza_riga} + {n_acc0} + {n_acc_pos} + "
           f"{n_acc_pos_flusso_nullo} = "
           f"{n_senza_riga + n_acc0 + n_acc_pos + n_acc_pos_flusso_nullo}  "
           f"su flussi_5t {n_tot}  "
           f"{'OK' if n_senza_riga + n_acc0 + n_acc_pos + n_acc_pos_flusso_nullo == n_tot else 'DIVERSO'}")

    # ---------- c) diagnosi ora 1 locale (23 UTC) ----------
    scrivi(f"\n-- c) ore UTC sul periodo {C_DA} -> {C_A} --")
    scrivi("     righe   = righe di flussi_5t nell'ora")
    scrivi("     acc0    = quota di righe con accuratezza = 0")
    scrivi("     sensori = sensori distinti con almeno una riga con accuratezza > 0")
    scrivi(f"  {'ora':>4} {'righe':>8} {'acc0':>8} {'quota':>7} {'sensori':>8}")

    righe = cur.execute("""
        SELECT f.generato_utc, f.lcd1, a.accuratezza
        FROM flussi_5t f
        LEFT JOIN accuratezza_5t a
               ON a.generato_utc = f.generato_utc AND a.lcd1 = f.lcd1
        WHERE substr(f.generato_utc, 1, 10) BETWEEN ? AND ?
    """, (C_DA, C_A)).fetchall()

    per_ora = {h: dict(righe=0, acc0=0, sensori=set()) for h in range(24)}
    for g, lcd1, acc in righe:
        h = int(g[11:13])
        d = per_ora[h]
        d["righe"] += 1
        if acc == 0:
            d["acc0"] += 1
        if acc is not None and acc > 0:
            d["sensori"].add(lcd1)

    for h in range(24):
        d = per_ora[h]
        quota = (d["acc0"] / d["righe"]) if d["righe"] else 0.0
        marca = "  <-- confronto" if h in ORE_DA_CONFRONTARE else ""
        scrivi(f"  {h:>4} {d['righe']:>8} {d['acc0']:>8} {quota:>6.1%} "
               f"{len(d['sensori']):>8}{marca}")

    d23 = per_ora[23]
    d22 = per_ora[22]
    d00 = per_ora[0]
    d01 = per_ora[1]
    frase = (f"  ore UTC 21/22/23/00/01 righe: "
             f"{per_ora[21]['righe']}/{d22['righe']}/{d23['righe']}/"
             f"{d00['righe']}/{d01['righe']} | sensori con accuratezza > 0: "
             f"{len(per_ora[21]['sensori'])}/{len(d22['sensori'])}/"
             f"{len(d23['sensori'])}/{len(d00['sensori'])}/{len(d01['sensori'])}")
    distingue = len(d23["sensori"]) < 0.8 * max(
        len(per_ora[21]["sensori"]), len(d22["sensori"]),
        len(d00["sensori"]), len(d01["sensori"]))
    scrivi("\n" + frase)
    scrivi(f"  frase: l'ora UTC 23 (= 01:00 locale) "
           f"{'SI distingue' if distingue else 'NON si distingue'} dalle ore vicine "
           f"per numero di sensori con letture affidabili.")

    con.close()

    testo = "\n".join(RIGHE)

    # console
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(testo)
    print()
    print(f"a) conteggi: {'OK' if esito_a else 'DA VERIFICARE'}")
    print(f"b) aritmetica: {'OK' if esito_b else 'DA VERIFICARE'}")

    # inserimento nel file di esito, senza duplicare blocchi precedenti
    vecchio = ESITO.read_text(encoding="utf-8") if ESITO.is_file() else ""
    if INIZIO in vecchio and FINE in vecchio:
        prima, resto = vecchio.split(INIZIO, 1)
        _, dopo = resto.split(FINE, 1)
        vecchio = prima.rstrip("\n") + "\n" + dopo
    blocco = f"{INIZIO}\n{testo}\n{FINE}\n"
    ESITO.parent.mkdir(parents=True, exist_ok=True)
    ESITO.write_text(vecchio.rstrip("\n") + "\n\n" + blocco, encoding="utf-8")
    print(f"Blocco scritto in: {ESITO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
