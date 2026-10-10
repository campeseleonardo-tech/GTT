#!/usr/bin/env python3
"""Copia settimanalmente lo storico SQLite dal Pi al PC in modo consistente."""
import base64
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path


def trova_radice():
    qui = Path(__file__).resolve().parent
    return next((p for p in [qui, *qui.parents] if p.name.lower() == "gtt"), qui.parent)


RAD = trova_radice()
DATA = RAD / "data"
PI = "leopi@192.168.8.200"
REMOTE_DB = "/home/leopi/GTT/data/storico.sqlite"
SSH_KEY = Path.home() / ".ssh" / "id_gtt_leopi"
DEST = DATA / "storico_backup.sqlite"
TABELLE = ("sensori_5t", "flussi_5t", "accuratezza_5t", "mezzi_gtt", "errori",
           "trip_update_gtt", "avvisi_gtt")


def esegui(comando):
    r = subprocess.run(comando, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode:
        raise RuntimeError(f"Comando fallito ({r.returncode}): {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip()


def comando_ssh(testo):
    codice = base64.b64encode(testo.encode("utf-8")).decode("ascii")
    remoto = f"python3 -c \"import base64;exec(base64.b64decode('{codice}').decode())\""
    return [shutil.which("ssh") or "ssh", "-i", str(SSH_KEY), "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=30", PI, remoto]


def riepilogo_locale(percorso):
    uri = percorso.resolve().as_uri() + "?mode=ro"
    con = sqlite3.connect(uri, uri=True, timeout=30)
    integro = con.execute("PRAGMA integrity_check").fetchone()[0]
    if integro != "ok":
        con.close()
        raise RuntimeError(f"integrity_check locale: {integro}")
    presenti = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conteggi = {t: con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                for t in TABELLE if t in presenti}
    ultimi = {}
    for tabella, colonna in (("mezzi_gtt", "letto_utc"), ("flussi_5t", "generato_utc"),
                             ("trip_update_gtt", "letto_utc")):
        if tabella in presenti:
            ultimi[tabella] = con.execute(
                f'SELECT MIN("{colonna}"),MAX("{colonna}") FROM "{tabella}"').fetchone()
    con.close()
    return {"integrity_check": integro, "conteggi": conteggi, "intervalli": ultimi}


def main():
    if not SSH_KEY.is_file():
        raise RuntimeError(f"Chiave SSH non trovata: {SSH_KEY}")
    if not DATA.is_dir():
        raise RuntimeError(f"Cartella dati non trovata: {DATA}")
    ssh = shutil.which("ssh")
    scp = shutil.which("scp")
    if not ssh or not scp:
        raise RuntimeError("ssh e scp devono essere disponibili nel PATH di Windows")

    identificatore = uuid.uuid4().hex
    remoto_tmp = f"/tmp/gtt_storico_{identificatore}.sqlite"
    py_remoto = f'''import json, sqlite3
src=sqlite3.connect("file:{REMOTE_DB}?mode=ro", uri=True, timeout=60)
dst=sqlite3.connect("{remoto_tmp}", timeout=60)
src.backup(dst, pages=256, sleep=0.1)
check=dst.execute("PRAGMA integrity_check").fetchone()[0]
tables={{r[0] for r in dst.execute("SELECT name FROM sqlite_master WHERE type='table'")}}
names={TABELLE!r}
counts={{t: dst.execute('SELECT COUNT(*) FROM "'+t+'"').fetchone()[0] for t in names if t in tables}}
ranges={{}}
for t,col in (("mezzi_gtt","letto_utc"),("flussi_5t","generato_utc"),("trip_update_gtt","letto_utc")):
    if t in tables: ranges[t]=dst.execute('SELECT MIN("'+col+'"),MAX("'+col+'") FROM "'+t+'"').fetchone()
dst.close(); src.close()
print(json.dumps({{"integrity_check":check,"conteggi":counts,"intervalli":ranges}}))
'''
    local_tmp = DATA / f"storico_backup_{identificatore}.part"
    try:
        print("Creo uno snapshot SQLite consistente sul Pi...")
        remoto = json.loads(esegui(comando_ssh(py_remoto)))
        if remoto.get("integrity_check") != "ok":
            raise RuntimeError(f"integrity_check remoto: {remoto.get('integrity_check')}")
        print("Copio lo snapshot sul PC...")
        esegui([scp, "-q", "-i", str(SSH_KEY), "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=30", f"{PI}:{remoto_tmp}", str(local_tmp)])
        locale = riepilogo_locale(local_tmp)
        if locale["conteggi"] != remoto["conteggi"]:
            raise RuntimeError(f"conteggi diversi: Pi={remoto['conteggi']} PC={locale['conteggi']}")
        if locale["intervalli"] != {k: tuple(v) for k, v in remoto["intervalli"].items()}:
            raise RuntimeError("intervalli temporali diversi tra snapshot del Pi e copia PC")
        os.replace(local_tmp, DEST)
        print(f"Backup verificato: {DEST}")
        print(f"Dimensione: {DEST.stat().st_size:,} byte")
        print(f"Tabelle: {remoto['conteggi']}")
        print(f"Intervalli: {remoto['intervalli']}")
    finally:
        if local_tmp.exists():
            local_tmp.unlink()
        # Elimina esclusivamente lo snapshot temporaneo creato in questa esecuzione.
        pulisci = f"import pathlib; p=pathlib.Path({remoto_tmp!r}); p.unlink(missing_ok=True)"
        try:
            esegui(comando_ssh(pulisci))
        except Exception as e:
            print(f"Avviso: non ho potuto rimuovere lo snapshot temporaneo sul Pi: {e}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERRORE backup: {e}", file=sys.stderr)
        sys.exit(1)
