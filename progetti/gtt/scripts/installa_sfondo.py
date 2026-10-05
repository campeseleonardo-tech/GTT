#!/usr/bin/env python3
"""
installa_sfondo.py - fa partire la raccolta in automatico e senza finestra, ad ogni accesso a Windows.

    python installa_sfondo.py installa     (crea l'avvio automatico e parte subito)
    python installa_sfondo.py rimuovi      (toglie l'avvio automatico e ferma il supervisore)
    python installa_sfondo.py stato        (dice se sta girando e mostra le ultime righe del log)

Non servono permessi di amministratore: mette un piccolo file nella cartella "Esecuzione automatica" di Windows.
"""
import os
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SUP = AQUI / "supervisore.py"
RADICE = next((c for c in [AQUI, *AQUI.parents] if c.name.lower() == "gtt"), AQUI.parent)
STOP = RADICE / "data" / "STOP_RACCOLTA.txt"


def cartella_avvio():
    base = os.environ.get("APPDATA")
    if not base:
        sys.exit("Questo script e' per Windows (manca la cartella APPDATA).")
    return Path(base) / "Microsoft/Windows/Start Menu/Programs/Startup"


def pythonw():
    p = Path(sys.executable)
    w = p.with_name("pythonw.exe")
    if not w.is_file():
        sys.exit(f"pythonw.exe non trovato accanto a {p}")
    return w


def in_esecuzione():
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", 47813))
        return False
    except OSError:
        return True
    finally:
        s.close()


def installa():
    vbs = cartella_avvio() / "GTT raccolta.vbs"
    w = pythonw()
    vbs.write_text(f'CreateObject("WScript.Shell").Run """{w}"" ""{SUP}""", 0, False\r\n', encoding="utf-8")
    if STOP.exists():
        STOP.unlink()
    print(f"Avvio automatico creato: {vbs}")
    if in_esecuzione():
        print("Il supervisore sta gia' girando.")
    else:
        subprocess.Popen([str(w), str(SUP)], creationflags=0x08000000 | 0x00000008, close_fds=True)
        print("Raccolta avviata in background (nessuna finestra).")
    print("Log: GTT\\logs\\raccolta_" + datetime.now().strftime("%Y-%m") + ".log")
    print("IMPORTANTE: se avevi ancora aperta la finestra nera del raccoglitore, chiudila (Ctrl+C), altrimenti i dati sono doppi.")


def rimuovi():
    vbs = cartella_avvio() / "GTT raccolta.vbs"
    if vbs.exists():
        vbs.unlink(); print("Avvio automatico rimosso.")
    STOP.parent.mkdir(parents=True, exist_ok=True)
    STOP.write_text("Fermata con installa_sfondo.py rimuovi.\n", encoding="utf-8")
    print("Messo il file STOP: il supervisore, se sta girando, si ferma alla prossima ripartenza del raccoglitore.")
    print("Per fermarlo subito: Gestione attivita' (Ctrl+Maiusc+Esc) -> chiudi i processi 'pythonw.exe' e 'python.exe'.")


def stato():
    print("Supervisore:", "IN ESECUZIONE" if in_esecuzione() else "non in esecuzione")
    print("Avvio automatico:", "presente" if (cartella_avvio() / "GTT raccolta.vbs").exists() else "assente")
    print("File STOP:", "presente (la raccolta non riparte)" if STOP.exists() else "assente")
    log = RADICE / "logs" / f"raccolta_{datetime.now():%Y-%m}.log"
    if log.is_file():
        print("\nUltime righe del log:")
        print("".join(log.read_text(encoding="utf-8", errors="replace").splitlines(True)[-8:]))


if __name__ == "__main__":
    az = sys.argv[1] if len(sys.argv) > 1 else "stato"
    {"installa": installa, "rimuovi": rimuovi, "stato": stato}.get(az, stato)()
