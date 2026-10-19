#!/usr/bin/env python3
"""
controlla_leopi.py  -  la raccolta sul Raspberry Pi (leopi) sta funzionando? (Claude, 20/10/2026)

Cosa fa
-------
Si collega a leopi con SSH (chiave %USERPROFILE%\\.ssh\\id_gtt_leopi) SOLO PER LEGGERE: apre il database
/home/leopi/GTT/data/storico.sqlite in sola lettura e guarda l'ultima riga scritta in ogni tabella raccolta.
  OK       = ogni tabella ha una lettura recente (vedi LIMITI_MINUTI);
  ALLARME  = almeno una tabella e' ferma (scrive quale e da quando).
Di notte (00-05 ora italiana) il feed dei ritardi GTT e' spento: per quella tabella non c'e' allarme.
Scrive anche una riga in logs\\controlla_leopi.log. Non modifica niente sul Pi.

Come si lancia
--------------
  doppio clic su scripts\\CONTROLLA_LEOPI.bat     (oppure: python scripts\\controlla_leopi.py)
  Codice di uscita: 0 = OK, 1 = ALLARME, 2 = Pi non raggiungibile.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comuni  # noqa: E402

PI = "leopi@192.168.8.200"
CHIAVE = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".ssh" / "id_gtt_leopi"
DB_PI = "/home/leopi/GTT/data/storico.sqlite"
# tabella -> (colonna del tempo, minuti oltre i quali e' ferma)
LIMITI_MINUTI = {
    "mezzi_gtt": ("letto_utc", 30),
    "trip_update_gtt": ("letto_utc", 30),
    "flussi_5t": ("generato_utc", 30),
    "occupazione_pk": ("generato_utc", 30),
    "ztl_5t": ("scaricato_utc", 26 * 60),
}
LOG = comuni.RADICE / "logs" / "controlla_leopi.log"

CODICE_PI = (
    "import sqlite3,json;"
    f"c=sqlite3.connect('file:{DB_PI}?mode=ro',uri=True);r={{}}\n"
    f"for t,col in {json.dumps({k: v[0] for k, v in LIMITI_MINUTI.items()})}.items():\n"
    "  try:\n"
    "    x=c.execute(f'SELECT {col} FROM {t} ORDER BY rowid DESC LIMIT 1').fetchone();r[t]=x[0] if x else None\n"
    "  except Exception as e:\n"
    "    r[t]='errore: '+str(e)\n"
    "print(json.dumps(r))"
)


def leggi_dal_pi():
    cmd = ["ssh", "-i", str(CHIAVE), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", PI, "python3", "-"]
    p = subprocess.run(cmd, input=CODICE_PI, capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"ssh codice {p.returncode}")
    return json.loads(p.stdout.strip().splitlines()[-1])


def parsa(ts):
    """Tempo del database (UTC, con o senza 'Z') -> datetime UTC."""
    d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d.astimezone(timezone.utc)


def main():
    ora = datetime.now(timezone.utc)
    ora_it = comuni.ora_locale(ora)
    try:
        ultimi = leggi_dal_pi()
    except Exception as e:  # noqa: BLE001
        riga = f"{ora_it:%d/%m %H:%M} Pi non raggiungibile: {e}"
        print(riga)
        LOG.parent.mkdir(exist_ok=True)
        LOG.open("a", encoding="utf-8").write(riga + "\n")
        return 2
    allarmi, righe = [], []
    for t, (_, limite) in LIMITI_MINUTI.items():
        v = ultimi.get(t)
        if v is None or str(v).startswith("errore"):
            righe.append(f"  {t:16s} nessun dato ({v})")
            allarmi.append(t)
            continue
        minuti = (ora - parsa(v)).total_seconds() / 60
        notte = t == "trip_update_gtt" and 0 <= ora_it.hour < 5
        ferma = minuti > limite and not notte
        righe.append(f"  {t:16s} ultima lettura {comuni.ora_locale(parsa(v)):%d/%m %H:%M} (da {minuti:,.0f} min)"
                     + ("  <-- FERMA" if ferma else ""))
        if ferma:
            allarmi.append(t)
    esito = "OK" if not allarmi else "ALLARME: ferme " + ", ".join(allarmi)
    print(f"Raccolta su leopi, {ora_it:%d/%m/%Y %H:%M}: {esito}")
    print("\n".join(righe))
    LOG.parent.mkdir(exist_ok=True)
    LOG.open("a", encoding="utf-8").write(f"{ora_it:%d/%m %H:%M} {esito}\n")
    return 0 if not allarmi else 1


if __name__ == "__main__":
    sys.exit(main())
