#!/usr/bin/env python3
"""
prova_pagine.py  -  Prova automatica a runtime delle pagine (mappa, ingresso, schede).

Cosa fa
-------
  1. Avvia un piccolo server locale (python -m http.server) dalla cartella del progetto.
  2. Apre ogni pagina in un browser headless e cerca errori JavaScript (Uncaught, ReferenceError, TypeError,
     SyntaxError, Failed to execute) e richieste fallite. Pagine: ogni tema della mappa (letti dal template),
     le viste dei parcheggi, l'ingresso, le schede dei risultati.
  3. Controlla nel DOM che il pannello di errore (#jsoff) non sia visibile e che la legenda della vista mostri
     il titolo atteso.
  4. Fa gli screenshot di ingresso, risultati e mappa (e delle viste dei parcheggi) a 1440x900 e 390x844
     in immagini/ (cartella fuori da git).
  5. Controllo statico: cerca identificatori r6... / R6... usati nel template ma non definiti.

Browser
-------
  Su Windows usa Edge o Chrome già installati. Se non ci sono (o su Linux/Mac), usa Playwright:
  pip install playwright (il browser lo trova in PLAYWRIGHT_BROWSERS_PATH, oppure: python -m playwright install chromium).
  --playwright forza Playwright anche su Windows.

File di data/ mancanti
----------------------
  Senza la cartella data/ (per esempio nel cloud o in un clone nuovo) le pagine non trovano i loro dati: i file
  mancanti di data/ si elencano come «file assente» e NON sono errori. Gli errori veri (JavaScript, altri file
  mancanti) fanno uscire con codice 1. La lista dei file attesi e se sono in git la dà lo script 86.

Come si lancia
--------------
  python scripts/prova_pagine.py
  python scripts/prova_pagine.py --cartella CARTELLA --senza-screenshot
  Codice di uscita 0 = nessun errore; 1 = errori trovati.

Non modifica nessun dato: scrive solo gli screenshot in immagini/.
"""
import glob
import http.server
import json
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
RADICE = AQUI.parent
PORTA = 8799
BROWSER_WINDOWS = [
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
DESKTOP, TELEFONO = (1440, 900), (390, 844)


def pagine_da_provare():
    """Le viste del Risultato 6, ogni altro tema della mappa (id letti dal template), l'ingresso e le schede."""
    temi = re.findall(r'\{id:"([a-z_0-9]+)", label:', TEMPLATE.read_text(encoding="utf-8"))
    out = [(f"mappa {v}", f"mappa_torino.html#tema=interscambio&vista={v}") for v in TITOLI_VISTA]
    out += [(f"mappa tema {t}", f"mappa_torino.html#tema={t}") for t in dict.fromkeys(temi) if t != "interscambio"]
    out.append(("ingresso", "index.html"))
    out += [(f"scheda R{n}", f"risultati.html#r{n}") for n in (1, 4, 6, 8, 10)]
    out.append(("elenco schede", "risultati.html"))
    return out


def pagine_screenshot():
    """(nome del file, pagina): ingresso, risultati, mappa e le due viste dei parcheggi."""
    return [("ingresso", "index.html"), ("risultati", "risultati.html"), ("mappa", "mappa_torino.html"),
            ("mappa_parcheggi", "mappa_torino.html#tema=interscambio&vista=parcheggi"),
            ("mappa_mancano", "mappa_torino.html#tema=interscambio&vista=mancano")]


class Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def avvia_server(cartella):
    os.chdir(cartella)
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORTA), Silenzioso)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    time.sleep(0.5)
    return srv


def file_di_data(url):
    """'data/...' se l'indirizzo punta dentro data/ del server locale, altrimenti None."""
    m = re.search(rf"127\.0\.0\.1:{PORTA}/(data/[^\s?#\"')]*)", url)
    return m.group(1) if m else None


# ---------------------------------------------------------------- Edge / Chrome di Windows
class BrowserWindows:
    nome = "Edge/Chrome di Windows"

    def __init__(self, percorso):
        self.percorso = percorso

    def chiudi(self):
        pass

    def esegui(self, url, extra, tag, w, h):
        """Edge/Chrome headless lanciato con PowerShell e -Wait: da Python il browser esce subito senza scrivere nulla."""
        cartella = Path(tempfile.gettempdir()) / "prova_pagine"
        cartella.mkdir(exist_ok=True)
        out, err = cartella / f"{tag}_out.txt", cartella / f"{tag}_err.txt"
        args = ["--headless=new", "--disable-gpu", "--no-first-run", f"--user-data-dir={cartella / ('profilo_' + tag)}",
                f"--window-size={w},{h}", "--enable-logging=stderr", "--v=0", "--virtual-time-budget=15000", *extra, url]
        arr = ",".join("'" + a.replace("'", "''") + "'" for a in args)
        ps = (f"$p = Start-Process -FilePath '{self.percorso}' -ArgumentList @({arr}) -Wait -PassThru "
              f"-RedirectStandardOutput '{out}' -RedirectStandardError '{err}' -WindowStyle Hidden; exit $p.ExitCode")
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], timeout=180, capture_output=True)
        except subprocess.TimeoutExpired:
            return "", "TIMEOUT"
        leggi = lambda f: f.read_text(encoding="utf-8", errors="replace") if f.exists() else ""
        return leggi(out), leggi(err)

    def apri(self, url, tag, png=None, w=DESKTOP[0], h=DESKTOP[1]):
        """(dom, errori, file assenti)"""
        if png:
            self.esegui(url, [f"--screenshot={png}"], "shot_" + tag, w, h)
            return "", [], []
        dom, log = self.esegui(url, ["--dump-dom"], tag, w, h)
        errori, assenti = [], []
        for riga in log.splitlines():
            if not any(p in riga for p in PAROLE_ERRORE):
                continue
            if "Failed to load resource" in riga and "404" in riga and file_di_data(riga):
                assenti.append(file_di_data(riga))
            else:
                errori.append(riga.strip()[:300])
        if "TIMEOUT" in log:
            errori.append("il browser non ha risposto in tempo")
        return dom, errori, sorted(set(assenti))


# ---------------------------------------------------------------- Playwright
class BrowserPlaywright:
    nome = "Playwright (Chromium)"

    def __init__(self):
        from playwright.sync_api import sync_playwright   # pip install playwright
        self.pw = sync_playwright().start()
        try:
            self.br = self.pw.chromium.launch()
        except Exception:
            # il browser puo' stare in una cartella che Playwright non indovina (es. /opt/pw-browsers)
            base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
            cand = sorted(glob.glob(os.path.join(base, "chromium-*", "chrome-linux", "chrome")))
            if not cand:
                self.pw.stop()
                raise
            self.br = self.pw.chromium.launch(executable_path=cand[-1])

    def chiudi(self):
        self.br.close()
        self.pw.stop()

    def apri(self, url, tag, png=None, w=DESKTOP[0], h=DESKTOP[1]):
        """(dom, errori, file assenti)"""
        ctx = self.br.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        errori, assenti = [], []

        def console(msg):
            if msg.type == "error" and "Failed to load resource" not in msg.text:
                errori.append(f"console: {msg.text[:300]}")

        def risposta(r):
            if r.status >= 400:
                d = file_di_data(r.url)
                (assenti.append(d) if d else errori.append(f"HTTP {r.status}: {r.url}"))

        page.on("console", console)
        page.on("pageerror", lambda e: errori.append(f"Uncaught {str(e)[:300]}"))
        page.on("response", risposta)
        try:
            page.goto(url, wait_until="load", timeout=60000)
            page.wait_for_timeout(2500)   # i dati si caricano con script aggiunti dopo
            if png:
                page.screenshot(path=str(png))
            dom = page.content()
        except Exception as e:
            dom = ""
            errori.append(f"il browser non ha caricato la pagina: {str(e)[:200]}")
        ctx.close()
        return dom, errori, sorted(set(assenti))


def sceglie_browser(forza_playwright):
    if not forza_playwright and os.name == "nt":
        for p in BROWSER_WINDOWS:
            if os.path.exists(p):
                return BrowserWindows(p)
        print("non trovo Edge né Chrome: provo con Playwright")
    try:
        return BrowserPlaywright()
    except ImportError:
        print("manca Playwright: pip install playwright (poi, se serve, python -m playwright install chromium)")
    except Exception as e:
        print(f"Playwright non riesce ad aprire il browser: {str(e)[:200]}")
    return None


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
    ap.add_argument("--playwright", action="store_true", help="usa Playwright anche su Windows")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    cartella = (RADICE / args.cartella) if args.cartella else RADICE
    br = sceglie_browser(args.playwright)
    if not br:
        print("prova automatica non possibile: nessun browser utilizzabile")
        return 1
    print(f"browser: {br.nome}")
    errori, assenti_tot = [], {}
    srv = avvia_server(cartella)
    pagine = pagine_da_provare()
    try:
        for nome, pagina in pagine:
            dom, err, assenti = br.apri(f"http://127.0.0.1:{PORTA}/{pagina}", nome.replace(" ", "_"))
            errori += [f"{nome}: {e}" for e in err]
            for a in assenti:
                assenti_tot.setdefault(a, []).append(nome)
            m = re.search(r'<div[^>]*id="jsoff"[^>]*>', dom)
            if m and re.search(r"display:\s*block", m.group(0)):
                errori.append(f"{nome}: il pannello #jsoff è visibile (display: block)")
            if pagina.startswith("mappa"):
                vista = re.search(r"vista=(\w+)", pagina)
                if vista and vista.group(1) in TITOLI_VISTA:
                    atteso = TITOLI_VISTA[vista.group(1)]
                    if atteso not in dom:
                        errori.append(f"{nome}: nella pagina manca il titolo della legenda «{atteso}»")
            print(f"  {nome}: {len(err)} errori, {len(assenti)} file assenti, DOM {len(dom)} caratteri")
        if not args.senza_screenshot:
            IMMAGINI.mkdir(exist_ok=True)
            for nome, pagina in pagine_screenshot():
                for sigla, (w, h) in (("desktop", DESKTOP), ("telefono", TELEFONO)):
                    png = IMMAGINI / f"{nome}_{sigla}.png"
                    if png.exists():
                        png.unlink()
                    br.apri(f"http://127.0.0.1:{PORTA}/{pagina}", f"{nome}_{sigla}", png=png, w=w, h=h)
                    dim = png.stat().st_size if png.exists() else 0
                    print(f"  screenshot {png.name} ({w}x{h}): {dim} byte" + ("  (meno di 5 KB: probabile pagina vuota)" if dim < 5000 else ""))
                    if dim < 5000:
                        errori.append(f"screenshot {png.name}: file piccolo ({dim} byte): probabile pagina vuota")
    finally:
        srv.shutdown()
        srv.server_close()
        br.chiudi()
    mancanti = controllo_statico()
    print(f"  identificatori r6/R6 non definiti: {mancanti if mancanti else 'nessuno'}")
    for m_ in mancanti:
        errori.append(f"identificatore non definito: {m_}")
    # etichette della vista aree: una sola per nome di zona
    dati = cartella / "data" / "processed" / "risultato6_v2" / "mappa_r6.json"
    if dati.exists():
        aree = json.loads(dati.read_text(encoding="utf-8"))["aree"]
        nomi = [a["etichetta"] for a in aree if a.get("mostra_etichetta")]
        ripetuti = sorted({n for n in nomi if nomi.count(n) > 1})
        print(f"  etichette della vista aree: {len(nomi)} (con nome ripetuto: {ripetuti or 'nessuno'})")
        if ripetuti:
            errori.append(f"etichette ripetute nella vista aree: {ripetuti}")
    if assenti_tot:
        print("\nfile assente (non è un errore del codice; senza data/ è normale):")
        for f, dove in sorted(assenti_tot.items()):
            print(f"  - {f}  (cercato da: {', '.join(dict.fromkeys(dove))})")
    if errori:
        print("\nERRORI:")
        for e in errori:
            print("  - " + e)
        return 1
    print(f"\nOK: nessun errore a runtime sulle {len(pagine)} pagine")
    return 0


if __name__ == "__main__":
    sys.exit(main())
