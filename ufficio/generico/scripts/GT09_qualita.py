# -*- coding: utf-8 -*-
"""
GT09_qualita.py - script del runner (0 token). Uso: python GT09_qualita.py <cartella GTT>
Legge (SOLO in lettura) data/storico.sqlite e scrive agenti/GT09-qualita/STATISTICHE.md: numeri sulla qualita' dei dati raccolti.
Non modifica la raccolta ne' il database. Se il database e' occupato riprova qualche volta.
"""
import sqlite3
import statistics
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path


def ts(s):
    s = (s or "").replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def lettura_gaps(tempi, soglia_fattore=4, quanti=8):
    """tempi: lista ordinata di datetime. Torna (intervallo mediano in s, lista dei buchi piu' lunghi)."""
    if len(tempi) < 3:
        return None, []
    d = [(b - a).total_seconds() for a, b in zip(tempi, tempi[1:])]
    med = statistics.median(d)
    grandi = sorted(((x, a, b) for x, a, b in zip(d, tempi, tempi[1:]) if x > max(soglia_fattore * med, 120)), reverse=True)[:quanti]
    return med, grandi


def h(x):
    return f"{x / 3600:.1f} h" if x >= 3600 else f"{x / 60:.1f} min"


def apri(db):
    for i in range(5):
        try:
            c = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True, timeout=30)
            c.execute("select 1 from sqlite_master limit 1")
            return c
        except sqlite3.OperationalError:
            time.sleep(3 * (i + 1))
    raise SystemExit("database occupato: riprova piu' tardi")


def main():
    repo = Path(sys.argv[1]).resolve()
    db = repo / "data" / "storico.sqlite"
    ctl = repo / "agenti" / "GT09-qualita"
    ctl.mkdir(parents=True, exist_ok=True)
    c = apri(db)
    out = [f"# GT09 - statistiche sui dati raccolti ({datetime.now():%Y-%m-%d %H:%M})", "",
           f"Database: data/storico.sqlite, {db.stat().st_size / 1e6:.1f} MB. Orari in UTC (Torino = UTC+2 d'estate, +1 d'inverno).", ""]
    for t in ("mezzi_gtt", "flussi_5t", "sensori_5t", "errori"):
        out.append(f"- tabella {t}: {c.execute(f'select count(*) from {t}').fetchone()[0]} righe")
    out.append("")

    out.append("## Mezzi GTT (posizioni)")
    letture = [ts(r[0]) for r in c.execute("select distinct letto_utc from mezzi_gtt order by 1")]
    letture = [x for x in letture if x]
    med, gaps = lettura_gaps(letture)
    out.append(f"- letture: {len(letture)}, dal {letture[0]:%Y-%m-%d %H:%M} al {letture[-1]:%Y-%m-%d %H:%M}; intervallo mediano {med:.0f} s" if letture and med else "- poche letture")
    if gaps:
        out.append("- buchi piu' lunghi (nessuna lettura): " + "; ".join(f"{h(x)} da {a:%d/%m %H:%M} a {b:%d/%m %H:%M}" for x, a, b in gaps))
    per_lettura = [r[0] for r in c.execute("select count(*) from mezzi_gtt group by letto_utc")]
    if per_lettura:
        out.append(f"- mezzi per lettura: minimo {min(per_lettura)}, mediana {statistics.median(per_lettura):.0f}, massimo {max(per_lettura)}")
    r = c.execute("select count(*), sum(corsa is null or corsa=''), sum(velocita is null), count(distinct veicolo), count(distinct linea) from mezzi_gtt").fetchone()
    out.append(f"- righe {r[0]}; con corsa (trip) vuota: {r[1]} ({100 * (r[1] or 0) / max(r[0], 1):.0f}%); con velocita' non misurata (NULL): {r[2]} ({100 * (r[2] or 0) / max(r[0], 1):.0f}%); veicoli distinti {r[3]}, linee distinte {r[4]}")
    ore = Counter()
    for (x,) in c.execute("select substr(letto_utc,12,2) from mezzi_gtt group by letto_utc"):
        ore[x] += 1
    out.append("- letture per ora UTC: " + ", ".join(f"{k}h:{ore[k]}" for k in sorted(ore)))
    mezzi_ora = {}
    for hh, n in c.execute("select substr(letto_utc,12,2), avg(n) from (select letto_utc, count(*) n from mezzi_gtt group by letto_utc) group by 1"):
        mezzi_ora[hh] = n
    out.append("- mezzi medi in servizio per ora UTC: " + ", ".join(f"{k}h:{mezzi_ora[k]:.0f}" for k in sorted(mezzi_ora)))
    out.append("")

    out.append("## Flussi 5T (sensori traffico)")
    snaps = [ts(r[0]) for r in c.execute("select distinct generato_utc from flussi_5t order by 1")]
    snaps = [x for x in snaps if x]
    med5, gaps5 = lettura_gaps(snaps)
    if snaps and med5:
        out.append(f"- letture: {len(snaps)}, dal {snaps[0]:%Y-%m-%d %H:%M} al {snaps[-1]:%Y-%m-%d %H:%M}; intervallo mediano {med5:.0f} s (atteso 300)")
    if gaps5:
        out.append("- buchi piu' lunghi: " + "; ".join(f"{h(x)} da {a:%d/%m %H:%M} a {b:%d/%m %H:%M}" for x, a, b in gaps5))
    n_sens = c.execute("select count(*) from sensori_5t").fetchone()[0]
    visti = c.execute("select count(distinct lcd1) from flussi_5t").fetchone()[0]
    out.append(f"- sensori in anagrafica {n_sens}, visti nei dati {visti}")
    acc = c.execute("select accuratezza, count(*) from sensori_5t group by 1 order by 1").fetchall()
    out.append("- accuratezza dichiarata (valore: n. sensori): " + ", ".join(f"{a}: {n}" for a, n in acc))
    q = c.execute("select count(*), sum(flusso>0), sum(velocita>0), sum(flusso is null), sum(velocita is null) from flussi_5t").fetchone()
    out.append(f"- righe {q[0]}; con flusso>0: {q[1]} ({100 * (q[1] or 0) / max(q[0], 1):.0f}%); con velocita'>0: {q[2]} ({100 * (q[2] or 0) / max(q[0], 1):.0f}%); flusso NULL {q[3]}; velocita' NULL {q[4]}")
    attivi = c.execute("select count(*) from (select lcd1 from flussi_5t group by lcd1 having max(flusso)>0)").fetchone()[0]
    out.append(f"- sensori che hanno mostrato flusso>0 almeno una volta: {attivi} su {visti}")
    perac = c.execute("""select s.accuratezza, count(distinct f.lcd1), sum(f.flusso>0), count(*)
                         from flussi_5t f join sensori_5t s on s.lcd1=f.lcd1 group by s.accuratezza order by 1""").fetchall()
    out.append("- per accuratezza (accuratezza: sensori, righe con flusso>0 / righe): " + "; ".join(f"{a}: {n}, {p or 0}/{t}" for a, n, p, t in perac))
    orf = c.execute("select substr(generato_utc,12,2), round(avg(flusso),1), round(avg(velocita),1) from flussi_5t where flusso>0 group by 1 order by 1").fetchall()
    out.append("- media per ora UTC (solo righe con flusso>0), formato ora: flusso/velocita': " + ", ".join(f"{a}h:{b}/{v}" for a, b, v in orf))
    out.append("")

    out.append("## Errori registrati dalla raccolta")
    errs = c.execute("select fonte, messaggio, count(*), min(quando_utc), max(quando_utc) from errori group by 1,2 order by 3 desc limit 15").fetchall()
    out += [f"- {f}: «{m[:120]}» x{n}, dal {a[:16]} al {b[:16]}" for f, m, n, a, b in errs] or ["- nessun errore registrato"]
    out.append("")
    (ctl / "STATISTICHE.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"scritto {ctl / 'STATISTICHE.md'}")


if __name__ == "__main__":
    main()
