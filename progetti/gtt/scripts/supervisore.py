#!/usr/bin/env python3
"""
supervisore.py - tiene sempre acceso il raccoglitore (03_raccolta_continua.py), senza finestra.

Cosa fa:
  - avvia il raccoglitore e lo riavvia se si ferma (dopo 30 s);
  - scrive tutto in GTT/logs/raccolta_AAAA-MM.log (un file al mese, mai cancellato);
  - impedisce a Windows di andare in stop mentre gira (lo schermo puo' spegnersi);
  - una volta a settimana (domenica sera) mostra una finestra: "Vuoi continuare?"
        Si' / nessuna risposta entro 1 ora -> continua;   No -> si ferma e non riparte da solo;
  - avvisa (finestra, una volta) se l'archivio supera i 10 GB;
  - ogni minuto prepara i file data/live.js, stat.js, replay_*.js che la mappa rilegge da sola (06_dati_live.py).
Si avvia da solo all'accesso a Windows (vedi installa_sfondo.py). Solo libreria standard.

Opzioni di prova:
  --promemoria-ora   mostra subito la finestra settimanale (per provarla)
"""
import json
import os
import socket
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for c in [AQUI, *AQUI.parents]:
        if c.name.lower() == "gtt":
            return c
    d = Path.home() / "Desktop" / "GTT"
    return d if d.is_dir() else AQUI.parent


RADICE = trova_radice()
DB = RADICE / "data" / "storico.sqlite"
LOGDIR = RADICE / "logs"
STATO = RADICE / "data" / "supervisore_stato.json"
STOP = RADICE / "data" / "STOP_RACCOLTA.txt"
RACCOGLITORE = AQUI / "03_raccolta_continua.py"
LIMITE_GB = 10
ATTESA_RIAVVIO = 30
ATTESA_RISPOSTA_MS = 3600 * 1000
WIN = os.name == "nt"
PORTA_BLOCCO = 47813  # impedisce di avere due supervisori insieme


def log(msg):
    LOGDIR.mkdir(parents=True, exist_ok=True)
    riga = f"{datetime.now().astimezone().isoformat(timespec='seconds')}  [supervisore] {msg}"
    with open(LOGDIR / f"raccolta_{datetime.now():%Y-%m}.log", "a", encoding="utf-8") as f:
        f.write(riga + "\n")


def scrivi_riga_raccoglitore(riga):
    with open(LOGDIR / f"raccolta_{datetime.now():%Y-%m}.log", "a", encoding="utf-8") as f:
        f.write(riga.rstrip("\n") + "\n")


def leggi_stato():
    try:
        return json.loads(STATO.read_text(encoding="utf-8"))
    except Exception:
        return {}


def salva_stato(d):
    STATO.parent.mkdir(parents=True, exist_ok=True)
    STATO.write_text(json.dumps(d, indent=1), encoding="utf-8")


def finestra(titolo, testo, domanda=False):
    """Mostra una finestra di Windows. Se domanda=True: Si'/No con scadenza (nessuna risposta = 'si')."""
    if not WIN:
        print(f"[FINESTRA] {titolo}\n{testo}")
        return os.environ.get("GTT_PROVA_RISPOSTA", "si") != "no"
    import ctypes
    MB_YESNO, MB_OK, MB_ICON, MB_TOPMOST = 0x4, 0x0, 0x20, 0x40000
    flags = (MB_YESNO if domanda else MB_OK) | MB_ICON | MB_TOPMOST
    try:
        r = ctypes.windll.user32.MessageBoxTimeoutW(0, testo, titolo, flags, 0, ATTESA_RISPOSTA_MS if domanda else 0x7FFFFFFF)
    except Exception:
        r = ctypes.windll.user32.MessageBoxW(0, testo, titolo, flags)
    return r != 7  # 7 = "No"; 32000 = scaduto -> continua


def riepilogo():
    righe, ultimo, errori = "?", "?", "?"
    try:
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=10)
        righe = con.execute("SELECT COALESCE(MAX(rowid),0) FROM mezzi_gtt").fetchone()[0]
        ultimo = con.execute("SELECT MAX(letto_utc) FROM mezzi_gtt").fetchone()[0]
        sett = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(timespec="seconds")
        errori = con.execute("SELECT COUNT(*) FROM errori WHERE quando_utc > ?", (sett,)).fetchone()[0]
        con.close()
    except Exception as e:
        log(f"riepilogo non riuscito: {e}")
    peso = sum(p.stat().st_size for p in DB.parent.glob("storico.sqlite*") if p.is_file()) / 1e9 if DB.parent.is_dir() else 0
    return righe, ultimo, errori, peso


def controllo_settimanale(forza=False):
    st = leggi_stato()
    ora = datetime.now()
    ultimo = datetime.fromisoformat(st["ultimo_promemoria"]) if st.get("ultimo_promemoria") else None
    if ultimo is None and not forza:
        st["ultimo_promemoria"] = ora.isoformat(); salva_stato(st)   # il primo arriva alla prossima domenica
        return None
    ultimo = ultimo or ora
    dovuto = forza or (ora.weekday() == 6 and ora.hour >= 20 and (ora - ultimo) > timedelta(days=2)) or (ora - ultimo) > timedelta(days=9)
    if not dovuto:
        return None
    righe, ult, err, peso = riepilogo()
    avviso = f"\n\nATTENZIONE: l'archivio ha superato i {LIMITE_GB} GB." if peso > LIMITE_GB else ""
    testo = (f"La raccolta dati GTT sta girando.\n\nPosizioni di mezzi salvate: {righe if isinstance(righe, str) else format(righe, ',')}\nUltimo dato: {ult}\n"
             f"Errori negli ultimi 7 giorni: {err}\nPeso archivio: {peso:.2f} GB (avviso oltre {LIMITE_GB} GB){avviso}\n\n"
             f"Vuoi continuare la raccolta?\nSi' = continua. No = si ferma e non riparte da sola.\n"
             f"(Se non rispondi entro un'ora, continua.)")
    continua = finestra("Raccolta dati GTT - continuiamo?", testo, domanda=True)
    st["ultimo_promemoria"] = datetime.now().isoformat(); salva_stato(st)
    log(f"promemoria settimanale: risposta = {'continua' if continua else 'STOP'}; righe={righe}, peso={peso:.2f} GB, errori7g={err}")
    return continua


def controllo_spazio():
    _, _, _, peso = riepilogo()
    st = leggi_stato()
    if peso > LIMITE_GB and not st.get("avviso_spazio"):
        st["avviso_spazio"] = True; salva_stato(st)
        log(f"ATTENZIONE: archivio {peso:.2f} GB, oltre {LIMITE_GB} GB")
        finestra("Raccolta dati GTT - spazio", f"L'archivio dati pesa {peso:.2f} GB, oltre il limite di {LIMITE_GB} GB.\nLa raccolta continua; dimmi se vuoi ridurre i dati.")


def resta_sveglio():
    if WIN:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)  # continuo + sistema acceso


def un_solo_supervisore():
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", PORTA_BLOCCO))
    except OSError:
        return None
    return s


def lancia():
    py = sys.executable
    if WIN and py.lower().endswith("pythonw.exe"):
        py = py[:-11] + "python.exe"
    kw = {"creationflags": 0x08000000} if WIN else {}   # CREATE_NO_WINDOW
    return subprocess.Popen([py, "-u", str(RACCOGLITORE)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, encoding="utf-8", errors="replace", **kw)


def main():
    blocco = un_solo_supervisore()
    if blocco is None:
        return  # ce n'e' gia' uno attivo
    forza = "--promemoria-ora" in sys.argv
    if STOP.exists() and not forza:
        log("Trovato STOP_RACCOLTA.txt: non avvio la raccolta (cancella il file o usa riavvia_raccolta.bat).")
        return
    resta_sveglio()
    log("supervisore avviato")
    stato = {"stop": False}

    def ciclo_controlli():
        primo = True
        while not stato["stop"]:
            try:
                r = controllo_settimanale(forza=forza and primo)
                primo = False
                if r is False:
                    STOP.write_text("Fermata su tua richiesta il " + datetime.now().isoformat() + ".\nCancella questo file (o lancia riavvia_raccolta.bat) per ripartire.\n", encoding="utf-8")
                    log("fermata su richiesta dell'utente")
                    stato["stop"] = True
                    if stato.get("proc"):
                        stato["proc"].terminate()
                    return
                controllo_spazio()
            except Exception as e:
                log(f"errore nei controlli: {e}")
            for _ in range(60):          # ricontrolla ogni ora; ogni minuto guarda se e' comparso il file STOP
                if stato["stop"]:
                    return
                if STOP.exists():
                    log("trovato STOP_RACCOLTA.txt: mi fermo")
                    stato["stop"] = True
                    if stato.get("proc"):
                        stato["proc"].terminate()
                    return
                time.sleep(60 if not forza else 1)
    threading.Thread(target=ciclo_controlli, daemon=True).start()

    def ciclo_live():
        """Ogni minuto aggiorna data/live.js; ogni 15 minuti statistiche e replay (per la mappa)."""
        import importlib.util
        try:
            sp = importlib.util.spec_from_file_location("dati_live", AQUI / "06_dati_live.py")
            dl = importlib.util.module_from_spec(sp); sp.loader.exec_module(dl)
        except Exception as e:
            log(f"impossibile caricare 06_dati_live.py: {e}"); return
        ultimo_stat, ultimo_errore, primo_giro = 0, "", True
        while not stato["stop"]:
            try:
                if DB.is_file():
                    dl.live()
                    if time.time() - ultimo_stat > 900:
                        dl.stat(); dl.replay(solo_oggi=not primo_giro); primo_giro = False
                        ultimo_stat = time.time()
                ultimo_errore = ""
            except Exception as e:
                if str(e) != ultimo_errore:
                    log(f"aggiornamento dati per la mappa non riuscito: {e}"); ultimo_errore = str(e)
            for _ in range(60):
                if stato["stop"]:
                    return
                time.sleep(1)
    threading.Thread(target=ciclo_live, daemon=True).start()

    while not stato["stop"]:
        try:
            p = lancia(); stato["proc"] = p
            log(f"raccoglitore avviato (pid {p.pid})")
            for riga in p.stdout:
                scrivi_riga_raccoglitore(riga)
            p.wait()
            log(f"raccoglitore terminato (codice {p.returncode})")
        except Exception as e:
            log(f"errore nell'avvio del raccoglitore: {e}")
        if stato["stop"]:
            break
        time.sleep(ATTESA_RIAVVIO)
    log("supervisore fermo")


if __name__ == "__main__":
    main()
