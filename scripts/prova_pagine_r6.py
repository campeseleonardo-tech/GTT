#!/usr/bin/env python3
"""
prova_pagine_r6.py  -  Prova automatica a runtime delle pagine del Risultato 6.

Cosa fa
-------
  1. Avvia un piccolo server locale (python -m http.server) dalla cartella del progetto.
  2. Apre le pagine con Edge headless (o Chrome) e cattura il log del browser: cerca errori
     JavaScript (Uncaught, ReferenceError, TypeError, SyntaxError, Failed to execute).
  3. Controlla nel DOM stampato che il pannello di errore (#jsoff) non sia visibile e che la
     legenda della vista mostri il titolo atteso.
  4. Fa gli screenshot delle tre viste della mappa in immagini\\r6_<vista>.png.
  5. Controllo statico: cerca identificatori r6… / R6… usati nel template ma non definiti.

Correzioni del 20/10/2026 (Claude): prova TUTTI i temi della mappa (letti dal template), non solo
interscambio e servizio; --cartella per provare una copia (es. la cartella pubblica/); --senza-screenshot;
titoli delle legende del Risultato 6 aggiornati.

Come si lancia
--------------
  python scripts\\prova_pagine_r6.py
  python scripts\\prova_pagine_r6.py --cartella pubblica --senza-screenshot
  Codice di uscita 0 = nessun errore; 1 = errori trovati.

Non modifica nessun dato: scrive solo gli screenshot in immagini\\.
"""
import http.server
import os
import re
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def trova_radice():
    for cartella in [AQUI, *AQUI.parents]:
        if cartella.name.lower() == "gtt":
            return cartella
    return AQUI.parent


RADICE = trova_radice()
PORTA = 8799
BROWSER_CANDIDATI = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
TEMPLATE = RADICE / "scripts" / "mappa_template.html"
IMMAGINI = RADICE / "immagini"
PAROLE_ERRORE = ("Uncaught", "ReferenceError", "TypeError", "SyntaxError", "Failed to execute", "ERROR:CONSOLE")
TITOLI_VISTA = {
    "parcheggi": "Dove ci sono parcheggi per lasciare l'auto?",
    "mancano": "Dove servirebbe di più un parcheggio?",
}


def pagine_da_provare():
    """Le tre viste del Risultato 6, ogni altro tema della mappa (id letti dal template) e la scheda."""
    temi = re.findall(r'\{id:"([a-z_]+)", label:', TEMPLATE.read_text(encoding="utf-8"))
    out = [(f"mappa {v}", f"mappa_torino.html#tema=interscambio&vista={v}") for v in TITOLI_VISTA]
    out += [(f"mappa tema {t}", f"mappa_torino.html#tema={t}") for t in dict.fromkeys(temi) if t != "interscambio"]
    out.append(("ingresso", "index.html"))
    out += [(f"scheda R{n}", f"risultati.html#r{n}") for n in (1, 4, 6, 8)]
    out.append(("elenco schede", "risultati.html"))
    return out


def browser():
    for p in BROWSER_CANDIDATI:
        if os.path.exists(p):
            return p
    return None


class Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def avvia_server(cartella=None):
    os.chdir(cartella or RADICE)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORTA), Silenzioso)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)
    return srv


def esegui(br, url, extra, tag):
    """Edge/Chrome in modalita' headless. Lanciato con PowerShell e -Wait: da Python, il browser
    esce subito senza scrivere nulla. Ritorna (stdout, stderr)."""
    cartella = Path(tempfile.gettempdir()) / "prova_r6"
    cartella.mkdir(exist_ok=True)
    out, err = cartella / f"{tag}_out.txt", cartella / f"{tag}_err.txt"
    args = ["--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={cartella / ('profilo_' + tag)}",
            "--window-size=1400,900", "--enable-logging=stderr", "--v=0", "--virtual-time-budget=15000", *extra, url]
    arr = ",".join("'" + a.replace("'", "''") + "'" for a in args)
    ps = (f"$p = Start-Process -FilePath '{br}' -ArgumentList @({arr}) -Wait -PassThru "
          f"-RedirectStandardOutput '{out}' -RedirectStandardError '{err}' -WindowStyle Hidden; exit $p.ExitCode")
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], timeout=180, capture_output=True)
    except subprocess.TimeoutExpired:
        return "", "TIMEOUT"
    leggi = lambda f: f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
    return leggi(out), leggi(err)


def controllo_statico():
    """Identificatori r6.../R6... usati come variabili e non definiti.
    Esclusi: chiavi di oggetto («nome:»), proprietà («.nome»), testi tra virgolette («"nome"»)."""
    testo = TEMPLATE.read_text(encoding="utf-8")
    # via il testo tra virgolette (stringhe e id) prima di cercare gli usi
    senza_stringhe = re.sub(r'"[^"\n]*"|\'[^\'\n]*\'|`[^`]*`', '""', testo)
    usati = set()
    for m in re.finditer(r"(?<![\w.])([rR]6[A-Za-z_]\w*)\b", senza_stringhe):
        dopo = senza_stringhe[m.end():m.end() + 3].lstrip(" ")
        if dopo.startswith(":") and not dopo.startswith("::"):
            continue   # chiave di oggetto
        usati.add(m.group(1))
    definiti = set(re.findall(r"\b(?:const|let|var|function)\s+([rR]6\w*)", testo))
    return sorted(usati - definiti)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cartella", default=None, help="cartella da servire (default: radice del progetto)")
    ap.add_argument("--senza-screenshot", action="store_true")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    cartella = (RADICE / args.cartella) if args.cartella else RADICE
    br = browser()
    if not br:
        print("prova automatica non possibile: non trovo Edge né Chrome")
        return 1
    print(f"browser: {br}")
    errori = []
    srv = avvia_server(cartella)
    pagine = pagine_da_provare()
    try:
        for nome, pagina in pagine:
            url = f"http://127.0.0.1:{PORTA}/{pagina}"
            dom, log = esegui(br, url, ["--dump-dom"], nome.replace(" ", "_"))
            righe_err = [l for l in log.splitlines() if any(p in l for p in PAROLE_ERRORE)]
            for l in righe_err[:20]:
                errori.append(f"{nome}: {l.strip()[:300]}")
            if "TIMEOUT" in log:
                errori.append(f"{nome}: il browser non ha risposto in tempo")
            m = re.search(r'<div[^>]*id="jsoff"[^>]*>', dom)
            if m and re.search(r"display:\s*block", m.group(0)):
                errori.append(f"{nome}: il pannello #jsoff è visibile (display: block)")
            if pagina.startswith("mappa"):
                vista = re.search(r"vista=(\w+)", pagina)
                if vista and vista.group(1) in TITOLI_VISTA:
                    atteso = TITOLI_VISTA[vista.group(1)]
                    if atteso not in dom:
                        errori.append(f"{nome}: nella pagina manca il titolo della legenda «{atteso}»")
            print(f"  {nome}: {len(righe_err)} righe di errore, DOM {len(dom)} caratteri")
        IMMAGINI.mkdir(exist_ok=True)
        for vista in (() if args.senza_screenshot else ("parcheggi", "mancano")):
            png = IMMAGINI / f"r6_{vista}.png"
            url = f"http://127.0.0.1:{PORTA}/mappa_torino.html#tema=interscambio&vista={vista}"
            esegui(br, url, [f"--screenshot={png}"], "shot_" + vista)
            dim = png.stat().st_size if png.exists() else 0
            print(f"  screenshot {png.name}: {dim} byte" + ("  (meno di 20 KB: probabile pagina vuota)" if dim < 20000 else ""))
            if dim < 20000:
                errori.append(f"screenshot {png.name}: file piccolo ({dim} byte): probabile pagina vuota")
    finally:
        srv.shutdown()
        srv.server_close()
    mancanti = controllo_statico()
    print(f"  identificatori r6/R6 non definiti: {mancanti if mancanti else 'nessuno'}")
    for m_ in mancanti:
        errori.append(f"identificatore non definito: {m_}")
    # etichette della vista aree: una sola per nome di zona
    dati = RADICE / "data" / "processed" / "risultato6_v2" / "mappa_r6.json"
    if dati.exists():
        import json
        aree = json.loads(dati.read_text(encoding="utf-8"))["aree"]
        nomi = [a["etichetta"] for a in aree if a.get("mostra_etichetta")]
        ripetuti = sorted({n for n in nomi if nomi.count(n) > 1})
        print(f"  etichette della vista aree: {len(nomi)} (con nome ripetuto: {ripetuti or 'nessuno'})")
        if ripetuti:
            errori.append(f"etichette ripetute nella vista aree: {ripetuti}")
    if errori:
        print("\nERRORI:")
        for e in errori:
            print("  - " + e)
        return 1
    print(f"\nOK: nessun errore a runtime sulle {len(pagine)} pagine")
    return 0


if __name__ == "__main__":
    sys.exit(main())
