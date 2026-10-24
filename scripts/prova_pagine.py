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
  4. (Con Playwright e Pillow) rifà le anteprime 1200x630 dei risultati
     in assets/anteprime/rN.jpg (per le pagine r/N.html, link condivisi sui social) e le 3 immagini del README in assets/readme/.
     Fa gli screenshot di ingresso, risultati e mappa (e delle viste dei parcheggi) a 1440x900 e 390x844
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
import shutil
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
sys.path.insert(0, str(AQUI))
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
    out.append(("progetto", "progetto.html"))
    out += [(f"scheda R{n}", f"risultati.html#r{n}") for n in (1, 4, 6, 8, 10, 12)]
    out.append(("elenco schede", "risultati.html"))
    return out


def pagine_screenshot():
    """(nome del file, pagina): ingresso, risultati, mappa e le due viste dei parcheggi."""
    return [("ingresso", "index.html"), ("risultati", "risultati.html"), ("progetto", "progetto.html"), ("mappa", "mappa_torino.html"),
            ("mappa_parcheggi", "mappa_torino.html#tema=interscambio&vista=parcheggi"),
            ("mappa_mancano", "mappa_torino.html#tema=interscambio&vista=mancano")]


class Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")   # il browser non deve riusare script vecchi (Edge tiene il profilo fra una prova e l'altra)
        super().end_headers()


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
        shutil.rmtree(cartella / ("profilo_" + tag), ignore_errors=True)   # profilo nuovo a ogni apertura: niente cache di file vecchi
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
            cand = sorted(glob.glob(os.path.join(base, "chromium-*", "chrome-linux", "chrome")) + glob.glob(os.path.join(base, "chromium-*", "chrome-linux64", "chrome")))
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


def prova_cambio_indirizzo(br, cartella):
    """risultati.html: se cambia #p3 / #r6 senza ricaricare la pagina, la scheda giusta si apre. Solo con Playwright
    e con data/schede_risultati.js presente. Ritorna un elenco di errori."""
    if not isinstance(br, BrowserPlaywright) or not (cartella / "data" / "schede_risultati.js").exists():
        print("  cambio di indirizzo (#p3, #r6): non provato (serve Playwright e data/schede_risultati.js)")
        return []
    page = br.br.new_page()
    errori = []
    try:
        page.goto(f"http://127.0.0.1:{PORTA}/risultati.html", wait_until="load", timeout=60000)
        page.wait_for_timeout(500)
        for h in ("#p3", "#r6", "#p1"):
            page.evaluate(f"location.hash = '{h}'")
            page.wait_for_timeout(300)
            aperta = page.evaluate("document.getElementById('finestra').open")
            if not aperta:
                errori.append(f"risultati.html: cambiando l'indirizzo in {h} la scheda non si apre")
    finally:
        page.close()
    print(f"  cambio di indirizzo (#p3, #r6, #p1): {'OK' if not errori else 'ERRORE'}")
    return errori


def prova_link_mappa(br, cartella):
    """Giro L11: ogni «Vedi sulla mappa» delle schede (data/schede_risultati.js) e le 3 viste consigliate della mappa aprono il tema e la vista scelti.
    Si apre l'indirizzo e si legge nel DOM: menu dei temi, vista scelta, ora. Solo con Playwright. Ritorna un elenco di errori."""
    js = cartella / "data" / "schede_risultati.js"
    if not isinstance(br, BrowserPlaywright) or not js.exists():
        print("  link «Vedi sulla mappa»: non provati (serve Playwright e data/schede_risultati.js)")
        return []
    testo = js.read_text(encoding="utf-8")
    schede = json.loads(testo[testo.index("["):].split(chr(10) + "window.SCHEDE_PERIODO")[0].rstrip().rstrip(";"))
    link = []
    for s in schede:
        m = (s.get("forma") or {}).get("mappa")
        if m:
            h = f"tema={m['id']}" + (f"&vista={m['vista']}" if m.get("vista") else "")
            link.append((f"scheda {s.get('numero_pubblico', s['risultato'])}", h))
    modello = (cartella / "mappa_torino.html").read_text(encoding="utf-8")
    cons = re.findall(r'<button[^>]*data-h="([^"]+)"', modello[modello.index('id="consigliate"'):])[:3]
    link += [("vista consigliata", h.replace("&amp;", "&")) for h in cons]
    errori = []
    for nome, h in link:
        tema = re.search(r"tema=(\w+)", h).group(1)
        vista = re.search(r"vista=(\w+)", h)
        ora = re.search(r"ora=(\d+)", h)
        page = br.br.new_page(viewport={"width": DESKTOP[0], "height": DESKTOP[1]})
        try:
            page.goto(f"http://127.0.0.1:{PORTA}/mappa_torino.html#{h}", wait_until="load", timeout=60000)
            page.wait_for_timeout(2500)
            letto = page.evaluate("""() => ({tema: document.getElementById('temi').value,
                subVuln: (document.getElementById('subVuln') || {}).value, r6: (document.getElementById('r6Vista') || {}).value,
                ora: (document.getElementById('oraTxt') || {}).textContent})""")
            if letto["tema"] != tema:
                errori.append(f"{nome} (#{h}): il menu dei temi mostra «{letto['tema']}», atteso «{tema}»")
            if vista and tema == "vulnerabilita" and letto["subVuln"] != "vuln_doppio":
                errori.append(f"{nome} (#{h}): la vista del tema Fragilità è «{letto['subVuln']}», attesa «vuln_doppio»")
            if vista and tema == "interscambio" and letto["r6"] != vista.group(1):
                errori.append(f"{nome} (#{h}): la vista dei parcheggi è «{letto['r6']}», attesa «{vista.group(1)}»")
            if ora and not (letto["ora"] or "").startswith(f"{int(ora.group(1)):02d}:"):
                errori.append(f"{nome} (#{h}): l'ora mostrata è «{letto['ora']}», attesa le {int(ora.group(1)):02d}")
        finally:
            page.close()
    # le viste consigliate si possono cliccare anche quando l'indirizzo e' gia' quello (hash uguale): si riapplicano
    page = br.br.new_page(viewport={"width": DESKTOP[0], "height": DESKTOP[1]})
    try:
        page.goto(f"http://127.0.0.1:{PORTA}/mappa_torino.html", wait_until="load", timeout=60000)
        page.wait_for_timeout(2000)
        for i, atteso in enumerate(("vulnerabilita", "puntualita", "interscambio", "vulnerabilita")):
            page.locator("#consigliate button").nth(min(i, 2) if i < 3 else 0).click()
            page.wait_for_timeout(1200)
            if i == 3:   # secondo clic sullo stesso pulsante dopo aver cambiato tema col menu: l'indirizzo non cambia, il tema deve tornare
                page.select_option("#temi", "omi")
                page.wait_for_timeout(500)
                page.locator("#consigliate button").nth(0).click()
                page.wait_for_timeout(1200)
            tema = page.evaluate("document.getElementById('temi').value")
            if tema != atteso:
                errori.append(f"vista consigliata {i + 1}: il tema è «{tema}», atteso «{atteso}»")
    finally:
        page.close()
    print(f"  link «Vedi sulla mappa» e viste consigliate ({len(link)} indirizzi): {'OK' if not errori else 'ERRORE'}")
    return errori


# ---------------------------------------------------------------- prova_design (giri L15-L18): controlli nel DOM, solo con Playwright
# le etichette (STIMATO, MISURATO, ...) si cercano solo in maiuscolo: «sezioni di censimento» e «misurato» in una frase sono parole normali
PESO_MAPPA_MAX = 5_906_557 + 54_637   # byte: peso di mappa_torino.html dopo L11 piu' il toro del caricamento (L18)
VIETATE_IT = (re.compile(r"STIMAT|MISURAT|PROGRAMMAT|CENSIMENTO"), re.compile(r"\bstim[ae]\b|\bstimat|sensor[ei]|più favorevole all'auto|\bpunta\b|\bnoi\b|\bnostr\w*|\babbiamo\b|Limite:", re.I))
VIETATE_EN = (re.compile(r"ESTIMATED|MEASURED|SCHEDULED|CENSUS"), re.compile(r"\bwe\b|\bour\b|peak|sensor|Limit:|\bestimate", re.I))


def _leggi_schede(cartella):
    js = cartella / "data" / "schede_risultati.js"
    testo = js.read_text(encoding="utf-8")
    return json.loads(testo[testo.index("["):].split(chr(10) + "window.SCHEDE_PERIODO")[0].rstrip().rstrip(";"))


def design_l15(br, cartella):
    """L15: ogni scheda in italiano e inglese: fuori dalla parte chiusa niente parole vietate (etichette, «stima», «sensori», «punta», «noi», «Limite:»),
    punti chiave di al massimo 25 parole, numero grande uguale a quello dei dati. Con «riduci movimento» (numeri subito finali)."""
    errori, schede = [], _leggi_schede(cartella)
    for lingua, vietate in (("it", VIETATE_IT), ("en", VIETATE_EN)):
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]}, reduced_motion="reduce")
        page = ctx.new_page()
        try:
            for s in schede:
                n = s.get("numero_pubblico")
                if n is None:
                    continue
                page.goto(f"http://127.0.0.1:{PORTA}/risultati.html?lang={lingua}#p{n}", wait_until="load", timeout=60000)
                page.wait_for_timeout(900)
                r = page.evaluate("""() => {
                  const c = document.getElementById('finCorpo').cloneNode(true);
                  c.querySelectorAll('details').forEach(d => d.remove());
                  const punti = [...c.querySelectorAll('ul.punti li')].map(li => li.textContent.trim());
                  const grande = (c.querySelector('.grande') || {textContent: ''}).textContent.replace(/\\s+/g, ' ').trim();
                  const val = (document.querySelector('#finCorpo .grande .val') || {textContent: ''}).textContent.trim();
                  return {visibile: document.getElementById('finMeta').textContent + ' ' + document.getElementById('finTitolo').textContent + ' ' + c.textContent.replace(/\\s+/g, ' '),
                          punti, val, aperta: document.getElementById('finestra').open,
                          chiusa: document.querySelectorAll('#finCorpo details.parte').length, tipo: !!document.querySelector('#finCorpo details.parte p')};
                }""")
                f = s["forma_en"] if lingua == "en" and s.get("forma_en") else s["forma"]
                nome = f"scheda {n} ({lingua})"
                if not r["aperta"]:
                    errori.append(f"{nome}: la scheda non si apre")
                    continue
                for rx in vietate:
                    for m in rx.finditer(r["visibile"]):
                        ctxt = r["visibile"][max(0, m.start() - 40):m.end() + 40]
                        errori.append(f"{nome}: parola vietata fuori dalla parte chiusa «{m.group(0)}» in «…{ctxt}…»")
                if len(r["punti"]) != 3:
                    errori.append(f"{nome}: {len(r['punti'])} punti chiave invece di 3")
                for p in r["punti"]:
                    if len(p.split()) > 25:
                        errori.append(f"{nome}: punto chiave di {len(p.split())} parole: «{p[:60]}…»")
                v = f["numero"]["valore"]
                atteso = page.evaluate("(v) => typeof v === 'number' ? Sito.formattaNumero(v) : String(v)", v)
                if r["val"].rstrip("%") != atteso:
                    errori.append(f"{nome}: il numero grande è «{r['val']}», nei dati «{atteso}»")
                if r["chiusa"] != 1:
                    errori.append(f"{nome}: {r['chiusa']} parti chiuse invece di una")
        finally:
            ctx.close()
    print(f"  L15 (schede 1-6, IT e EN: parole vietate, punti chiave, numero grande): {'OK' if not errori else 'ERRORE'}")
    return errori


def design_l16(br, cartella):
    """L16: gara e area da sole. Nessun comando dentro .gara e .area; ogni testo della gara dentro il disegno, testi e mezzi che non si toccano;
    il nome del luogo cambia fra due corse; i minuti dell'area cambiano da soli entro 3 secondi; con «riduci movimento» tutto fermo e i numeri scritti."""
    errori = []
    JS_GARA = """() => [...document.querySelectorAll('.gara svg')].map(svg => {
        const vb = svg.viewBox.baseVal, r = [];
        const testi = [...svg.querySelectorAll('text')].filter(t => !t.closest('text, tspan') || true);
        const box = e => { const b = e.getBBox(); return {x: b.x, y: b.y, w: b.width, h: b.height, t: (e.textContent || '').slice(0, 30)}; };
        const fuori = testi.map(box).filter(b => b.x < -1 || b.y < -1 || b.x + b.w > vb.width + 1 || b.y + b.h > vb.height + 1);
        const bb = [...svg.querySelectorAll('text.gara-da, text.gara-min, text.gara-esito')].map(e => { const q = e.getBoundingClientRect(); return {x: q.left, y: q.top, r: q.right, b: q.bottom, t: e.textContent.slice(0, 20)}; });
        const toc = [];
        for (let i = 0; i < bb.length; i++) for (let j = i + 1; j < bb.length; j++) {
          const a = bb[i], c = bb[j];
          if (a.x < c.r - 1 && c.x < a.r - 1 && a.y < c.b - 1 && c.y < a.b - 1) toc.push(a.t + ' / ' + c.t);
        }
        const veic = [...svg.querySelectorAll('g.gv')].map(g => { const q = g.getBoundingClientRect(); return {y: q.top, b: q.bottom}; });
        let corsie = false; if (veic.length === 2) corsie = veic[0].b > veic[1].y + 1 && veic[1].b > veic[0].y + 1;
        return {fuori, toc, corsie, nome: (svg.querySelector('text.gara-da') || {textContent: ''}).textContent};
      })"""
    for lingua in ("it", "en"):
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]})
        page = ctx.new_page()
        try:
            for n_, cosa in ((3, "gara"), (4, "gara"), (4, "area")):
                page.goto(f"http://127.0.0.1:{PORTA}/risultati.html?lang={lingua}#p{n_}", wait_until="load", timeout=60000)
                page.wait_for_timeout(800)
                nome = f"scheda {n_} {cosa} ({lingua})"
                comandi = page.evaluate("document.querySelectorAll('#finCorpo .gara select, #finCorpo .gara button, #finCorpo .gara input, #finCorpo .area select, #finCorpo .area button, #finCorpo .area input').length")
                if comandi:
                    errori.append(f"{nome}: {comandi} comandi (select, button, input) dentro la gara o l'area")
                if cosa == "gara":
                    el = page.locator("#finCorpo .gara").first
                    if el.count() == 0:
                        errori.append(f"{nome}: gara assente")
                        continue
                    el.scroll_into_view_if_needed()
                    page.wait_for_timeout(1500)
                    r = page.evaluate(JS_GARA)
                    for g in r:
                        if g["fuori"]:
                            errori.append(f"{nome}: testi fuori dal disegno: {g['fuori'][:3]}")
                        if g["toc"]:
                            errori.append(f"{nome}: testi che si toccano: {g['toc'][:3]}")
                        if g["corsie"]:
                            errori.append(f"{nome}: le corsie si toccano")
                    primo = r[0]["nome"] if r else ""
                    cambiato = False
                    for _ in range(40):          # fino a 40 s: una corsa dura al massimo una decina di secondi, piu' la pausa
                        page.wait_for_timeout(1000)
                        if page.evaluate("(document.querySelector('#finCorpo .gara svg text.gara-da') || {textContent: ''}).textContent") != primo:
                            cambiato = True
                            break
                    if not cambiato:
                        errori.append(f"{nome}: il nome del luogo non cambia fra due corse (resta «{primo}»)")
                else:
                    el = page.locator("#finCorpo .area").first
                    if el.count() == 0:
                        errori.append(f"{nome}: area assente")
                        continue
                    el.scroll_into_view_if_needed()
                    page.wait_for_timeout(600)
                    a = page.evaluate("document.querySelector('#finCorpo .area-minuti').textContent")
                    page.wait_for_timeout(2400)
                    b = page.evaluate("document.querySelector('#finCorpo .area-minuti').textContent")
                    if a == b:
                        errori.append(f"{nome}: i minuti dell'area non cambiano da soli in 3 secondi (restano «{a}»)")
        finally:
            ctx.close()
        # riduci movimento: tutto fermo, numeri scritti
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]}, reduced_motion="reduce")
        page = ctx.new_page()
        try:
            for n_, cosa in ((3, "gara"), (4, "gara"), (4, "area")):
                page.goto(f"http://127.0.0.1:{PORTA}/risultati.html?lang={lingua}#p{n_}", wait_until="load", timeout=60000)
                page.wait_for_timeout(1200)
                nome = f"scheda {n_} {cosa} ({lingua}, riduci movimento)"
                if cosa == "gara":
                    r = page.evaluate("""() => ({svg: document.querySelectorAll('#finCorpo .gara svg').length, mezzi: document.querySelectorAll('#finCorpo .gara g.gv').length,
                        min: [...document.querySelectorAll('#finCorpo .gara text.gara-min')].filter(t => getComputedStyle(t).opacity !== '1').length})""")
                    if r["svg"] < 2 or r["mezzi"] or r["min"]:
                        errori.append(f"{nome}: non è tutto fermo con i minuti scritti: {r}")
                else:
                    a = page.evaluate("document.querySelector('#finCorpo .area-minuti').textContent")
                    page.wait_for_timeout(2000)
                    b = page.evaluate("[document.querySelector('#finCorpo .area-minuti').textContent, document.querySelector('#finCorpo [data-q=m]').textContent, document.querySelector('#finCorpo [data-q=a]').textContent]")
                    if a != b[0] or not a.startswith("30") or "%" not in b[1] or "%" not in b[2]:
                        errori.append(f"{nome}: area non ferma a 30 minuti con le quote scritte: {a} / {b}")
        finally:
            ctx.close()
    print(f"  L16 (gara e area da sole, senza comandi, testi nel disegno, riduci movimento): {'OK' if not errori else 'ERRORE'}")
    return errori


def design_l20(br, cartella):
    """L20: scheda 6, contatori di euro che salgono da soli (nessun comando); con «riduci movimento» i numeri finali sono quelli dei dati."""
    errori = []
    for riduci in (False, True):
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]}, reduced_motion="reduce" if riduci else "no-preference")
        page = ctx.new_page()
        try:
            page.goto(f"http://127.0.0.1:{PORTA}/risultati.html#p6", wait_until="load", timeout=60000)
            page.wait_for_timeout(1200)
            nome = "scheda 6 contatori" + (" (riduci movimento)" if riduci else "")
            n_ctrl = page.evaluate("document.querySelectorAll('#finCorpo .anima button, #finCorpo .anima select, #finCorpo .anima input').length")
            if n_ctrl:
                errori.append(f"{nome}: {n_ctrl} comandi dentro l'animazione")
            def euro():
                return page.evaluate("[...document.querySelectorAll('#finCorpo .anima .an-eur')].map(e => e.textContent.trim())")
            prima = euro()
            if len(prima) != 2:
                errori.append(f"{nome}: {len(prima)} contatori invece di 2")
                continue
            if riduci:
                dati = page.evaluate("(window.SCHEDE_RISULTATI.find(s => s.numero_pubblico === 6).forma.anima.righe || []).map(r => Math.round(r.mese * 12))")
                scritti = [int("".join(ch for ch in t if ch.isdigit()) or 0) for t in prima]
                if scritti != dati:
                    errori.append(f"{nome}: contatori {scritti}, nei dati {dati}")
            else:
                page.wait_for_timeout(2500)
                dopo = euro()
                if dopo == prima or all(t.replace("€", "").strip() in ("", "0") for t in dopo):
                    errori.append(f"{nome}: i contatori non salgono da soli ({prima} -> {dopo})")
        finally:
            ctx.close()
    print(f"  L20 (scheda 6: contatori da soli, senza comandi, riduci movimento): {'OK' if not errori else 'ERRORE'}")
    return errori


def design_l17(br, cartella):
    """L17: home da scorrere. I 3 numeri chiave uguali ai dati; un riquadro per scheda con anteprima, titolo e numero (testo breve); #progetto con le 6 tappe;
    con «riduci movimento» nessuna animazione; 0 errori in index, risultati e progetto; peso della home sotto 1 MB (HTML + JS e CSS propri)."""
    errori, schede = [], _leggi_schede(cartella)
    per_numero = {s["numero_pubblico"]: s for s in schede if s.get("numero_pubblico") is not None}
    for lingua in ("it", "en"):
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]}, reduced_motion="reduce")
        page = ctx.new_page()
        brutti = []
        page.on("pageerror", lambda e: brutti.append(str(e)[:200]))
        page.on("console", lambda m: brutti.append(m.text[:200]) if m.type == "error" and "Failed to load resource" not in m.text else None)
        try:
            page.goto(f"http://127.0.0.1:{PORTA}/index.html?lang={lingua}", wait_until="load", timeout=60000)
            page.wait_for_timeout(1500)
            nome = f"home ({lingua})"
            r = page.evaluate("""() => ({
              chiavi: [...document.querySelectorAll('#numeriChiave .num-chiave')].map(a => ({href: a.getAttribute('href'), val: a.querySelector('.val').textContent.trim()})),
              riquadri: [...document.querySelectorAll('#riquadri .riquadro')].map(a => ({href: a.getAttribute('href'), anteprima: !!a.querySelector('.anteprima .anima'),
                 titolo: (a.querySelector('h3') || {textContent: ''}).textContent.trim(), val: (a.querySelector('.grande .val') || {textContent: ''}).textContent.trim(),
                 txt: (a.querySelector('.grande .txt') || {textContent: ''}).textContent.trim()})),
              tappe: document.querySelectorAll('#progetto .testi section').length, figure: document.querySelectorAll('#progetto figure').length,
              titoloProgetto: (document.querySelector('#progetto h2') || {textContent: ''}).textContent.trim(),
              navProgetto: [...document.querySelectorAll('.barra-alta nav a')].some(a => a.getAttribute('href') === '#progetto'),
              animazioni: document.getAnimations().length,
              intro: document.querySelectorAll('ul.intro, .bottoni').length})""")
            if len(r["chiavi"]) != 3:
                errori.append(f"{nome}: {len(r['chiavi'])} numeri chiave invece di 3")
            for c, n_ in zip(r["chiavi"], (4, 2, 5)):
                f = (per_numero[n_]["forma_en"] if lingua == "en" and per_numero[n_].get("forma_en") else per_numero[n_]["forma"])
                k = f.get("chiave") or {}
                atteso = str(page.evaluate("(v) => typeof v === 'number' ? Sito.formattaNumero(v) : String(v)", k.get("valore"))) + ("%" if k.get("unita") == "%" else "")
                if c["val"] != atteso or c["href"] != f"risultati.html#p{n_}":
                    errori.append(f"{nome}: numero chiave della scheda {n_} è «{c['val']}» ({c['href']}), nei dati «{atteso}»")
            if len(r["riquadri"]) != len(per_numero):
                errori.append(f"{nome}: {len(r['riquadri'])} riquadri per {len(per_numero)} schede")
            for q, n_ in zip(r["riquadri"], sorted(per_numero)):
                f = (per_numero[n_]["forma_en"] if lingua == "en" and per_numero[n_].get("forma_en") else per_numero[n_]["forma"])
                if not q["anteprima"] or q["titolo"] != f["titolo"] or not q["val"] or q["href"] != f"risultati.html#p{n_}":
                    errori.append(f"{nome}: riquadro {n_} incompleto (anteprima {q['anteprima']}, titolo «{q['titolo'][:30]}», numero «{q['val']}», link {q['href']})")
                breve = f["numero"].get("breve")
                if not breve or breve not in q["txt"] or len(breve.split()) > 8:
                    errori.append(f"{nome}: riquadro {n_}: testo breve mancante o oltre 8 parole («{breve}»)")
            if r["tappe"] != 6 or r["figure"] != 6:
                errori.append(f"{nome}: #progetto ha {r['tappe']} tappe e {r['figure']} disegni invece di 6 e 6")
            if r["titoloProgetto"].lower() not in ("il progetto", "the project") or not r["navProgetto"]:
                errori.append(f"{nome}: titolo «{r['titoloProgetto']}» o link «Il progetto» della barra verso #progetto mancanti")
            if r["animazioni"]:
                errori.append(f"{nome}: con «riduci movimento» ci sono {r['animazioni']} animazioni CSS in corso")
            if r["intro"]:
                errori.append(f"{nome}: restano la lista «intro» o i due bottoni vecchi")
            for pagina in ("risultati.html", "progetto.html"):
                page.goto(f"http://127.0.0.1:{PORTA}/{pagina}?lang={lingua}", wait_until="load", timeout=60000)
                page.wait_for_timeout(1200)
            if brutti:
                errori.append(f"{nome}: errori JavaScript in index, risultati o progetto: {brutti[:3]}")
        finally:
            ctx.close()
    # peso della home: index.html e i file propri che carica (script, stili); font e immagini non contano
    index = (cartella / "index.html").read_text(encoding="utf-8")
    file_home = ["index.html"] + re.findall(r'<script src="([^"]+)"', index) + re.findall(r'<link rel="stylesheet" href="([^"]+)"', index)
    peso = sum((cartella / f).stat().st_size for f in file_home if (cartella / f).is_file())
    print(f"  peso della home (HTML, script e stili propri): {peso / 1e6:.2f} MB su {len(file_home)} file")
    if peso >= 1_000_000:
        errori.append(f"la home pesa {peso / 1e6:.2f} MB (limite 1 MB, HTML + JS e CSS propri)")
    print(f"  L17 (home: numeri chiave, riquadri, tappe del progetto, riduci movimento): {'OK' if not errori else 'ERRORE'}")
    return errori


def design_l18(br, cartella):
    """L18: il toro nel caricamento della mappa. #caricamento ha i tracciati del toro e non il contorno di Torino; resta visibile almeno 2 secondi
    dall'apertura; con «riduci movimento» il toro e' fermo e intero e sparisce appena la mappa e' pronta; la mappa non pesa piu' del limite."""
    errori = []
    pagina = cartella / "mappa_torino.html"
    if not pagina.exists():
        print("  L18: non provata (manca mappa_torino.html)")
        return []
    peso = pagina.stat().st_size
    if peso > PESO_MAPPA_MAX:
        errori.append(f"mappa_torino.html pesa {peso:,} byte, oltre il limite {PESO_MAPPA_MAX:,} (5.906.557 di L11 più il toro): semplificare i tracciati")
    # gara del pannello (giro L19): un'auto sola (TomTom), nessun comando; stesso pezzo nel template e nella mappa
    for f in (pagina, cartella / "scripts" / "mappa_template.html"):
        testo = f.read_text(encoding="utf-8")
        riga = next((r for r in testo.splitlines() if "return Gara.html(" in r), "")
        if "giro:true" not in riga or "auto_alto_min" in riga or "compatto" in riga:
            errori.append(f"{f.name}: la gara del pannello non è «giro:true» con la sola auto TomTom ({riga.strip()[:80]})")
    JS_FINE = """() => { window.__fine = null; const guarda = () => { const c = document.getElementById('caricamento');
        if (!c) { if (window.__fine === null) window.__fine = performance.now(); return; }
        new MutationObserver(() => { if (c.classList.contains('fine') && window.__fine === null) window.__fine = performance.now(); }).observe(c, {attributes: true}); };
      new MutationObserver((m, o) => { if (document.getElementById('caricamento')) { o.disconnect(); guarda(); } }).observe(document, {childList: true, subtree: true}); }"""
    for ridotto in (False, True):
        ctx = br.br.new_context(viewport={"width": DESKTOP[0], "height": DESKTOP[1]}, reduced_motion="reduce" if ridotto else "no-preference")
        page = ctx.new_page()
        nome = "mappa, caricamento" + (" (riduci movimento)" if ridotto else "")
        try:
            page.add_init_script("(" + JS_FINE + ")()")
            page.goto(f"http://127.0.0.1:{PORTA}/mappa_torino.html", wait_until="commit", timeout=60000)
            page.wait_for_selector("#caricamento", state="attached", timeout=20000)
            r = page.evaluate("""() => { const c = document.getElementById('caricamento'), s = c.querySelector('svg'), p = c.querySelector('path');
                const st = getComputedStyle(p);
                return {paths: c.querySelectorAll('path').length, vb: s.getAttribute('viewBox'), testo: c.querySelector('.car-testo').textContent,
                        anim: st.animationName, giri: st.animationIterationCount, dir: st.animationDirection, dash: st.strokeDashoffset, riempi: st.fill}; }""")
            if r["paths"] < 20 or r["vb"] != "0 0 600 1001":
                errori.append(f"{nome}: non c'è il toro ({r['paths']} tracciati, viewBox {r['vb']})")
            if r["testo"] != "Caricamento della mappa…":
                errori.append(f"{nome}: testo «{r['testo']}»")
            if ridotto and (r["anim"] != "none" or float(r["dash"].replace("px", "")) != 0):
                errori.append(f"{nome}: il toro non è a linee fermo e intero (animazione {r['anim']}, tratteggio {r['dash']})")
            if not ridotto and (r["anim"] != "car-disegna" or r["giri"] != "infinite" or "alternate" not in r["dir"]):
                errori.append(f"{nome}: la linea non corre avanti e indietro all'infinito (animazione {r['anim']}, giri {r['giri']}, direzione {r['dir']})")
            m_ = re.match(r"rgba?\(([^)]*)\)", r["riempi"])
            if m_ and (len(m_.group(1).split(",")) < 4 or float(m_.group(1).split(",")[3]) > 0.3):
                errori.append(f"{nome}: il toro ha un riempimento pieno ({r['riempi']})")
            page.wait_for_timeout(5000)
            fine = page.evaluate("window.__fine")
            if fine is None:
                errori.append(f"{nome}: il caricamento non sparisce")
            elif not ridotto and fine < 1950:
                errori.append(f"{nome}: sparito dopo {fine:.0f} ms, meno dei 2 secondi dall'apertura")
            if "M879 130l-33" in page.content():
                errori.append(f"{nome}: c'è ancora il contorno di Torino")
        except Exception as e:
            errori.append(f"{nome}: {str(e)[:200]}")
        finally:
            ctx.close()
    print(f"  L18 (toro nel caricamento: tracciati, almeno 2 secondi, linea infinita senza oro pieno, gara del pannello, riduci movimento, peso {peso:,} byte): {'OK' if not errori else 'ERRORE'}")
    return errori


def prova_design(br, cartella):
    """Controlli di design dei giri L15-L18 (DOM). Solo con Playwright e con data/schede_risultati.js."""
    if not isinstance(br, BrowserPlaywright) or not (cartella / "data" / "schede_risultati.js").exists():
        print("  prova_design: non provata (serve Playwright e data/schede_risultati.js)")
        return []
    return design_l15(br, cartella) + design_l16(br, cartella) + design_l17(br, cartella) + design_l18(br, cartella) + design_l20(br, cartella)


ANTEPRIME = RADICE / "assets" / "anteprime"
IMMAGINI_README = RADICE / "assets" / "readme"

# immagine di anteprima 1200x630 di un risultato (per r/N.html: i link condivisi sui social): numero grande e titolo sullo stile del sito
JS_ANTEPRIMA = """(n) => {
  const s = window.SCHEDE_RISULTATI.find(x => x.numero_pubblico === n), f = s.forma, g = f.numero;
  const val = typeof g.valore === "number" ? Sito.formattaNumero(g.valore) : g.valore;
  const unita = g.unita === "%" ? "%" : (g.unita || "");
  const st = document.createElement("style");
  st.textContent = "html,body{margin:0;padding:0;background:var(--barra)}.og{width:1200px;height:630px;box-sizing:border-box;background:var(--barra);color:var(--su-barra);"
    + "border-bottom:14px solid var(--oro);padding:52px 72px 44px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}"
    + ".og .k{font:700 30px/1 var(--font-titoli);letter-spacing:.08em;text-transform:uppercase;color:var(--oro-su-barra)}"
    + ".og .n{font:700 170px/1 var(--font-titoli)}.og .n small{font-size:56px;margin-left:16px;font-weight:600;opacity:.9}"
    + ".og .t{font:600 44px/1.18 var(--font-testi);max-width:1040px}.og .f{font:400 24px/1 var(--font-testi);opacity:.8}";
  document.head.appendChild(st);
  document.body.className = "";
  document.body.innerHTML = '<div class="og"><div class="k">Torino Mobilità · ' + 'Risultato ' + n + '</div><div class="n">' + val + (unita === "%" ? "%" : "<small>" + unita + "</small>")
    + '</div><div class="t">' + Sito.esc(f.titolo) + '</div><div class="f">campeseleonardo-tech.github.io/Turin-mobility</div></div>';
}"""


def _jpg(png_bytes, percorso, larghezza=None, qualita=82, ritaglia_alt=None):
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    if ritaglia_alt:
        img = img.crop((0, 0, img.width, min(img.height, ritaglia_alt)))
    if larghezza and img.width > larghezza:
        img = img.resize((larghezza, round(img.height * larghezza / img.width)), Image.LANCZOS)
    percorso.parent.mkdir(parents=True, exist_ok=True)
    img.save(percorso, "JPEG", quality=qualita, optimize=True)
    return percorso.stat().st_size


def fai_immagini_condivisione(br, cartella):
    """Anteprime 1200x630 dei risultati (assets/anteprime/rN.jpg, per le pagine r/N.html) e le 3 immagini del README (assets/readme/: home, un risultato, mappa).
    Serve Playwright, Pillow e i dati delle schede; altrimenti salta senza errore. Ritorna un elenco di errori."""
    if not isinstance(br, BrowserPlaywright) or not (cartella / "data" / "schede_risultati.js").exists():
        print("  immagini di anteprima e README: non fatte (serve Playwright e data/schede_risultati.js)")
        return []
    try:
        __import__("PIL")  # solo per sapere se Pillow c'è
    except ImportError:
        print("  immagini di anteprima e README: non fatte (manca Pillow: pip install pillow)")
        return []
    errori = []
    base = f"http://127.0.0.1:{PORTA}/"
    ctx = br.br.new_context(viewport={"width": 1200, "height": 630}, reduced_motion="reduce", color_scheme="light", locale="it-IT")
    page = ctx.new_page()
    try:
        page.goto(base + "risultati.html", wait_until="load", timeout=60000)
        numeri = page.evaluate("(window.SCHEDE_RISULTATI || []).filter(s => s.forma && s.numero_pubblico != null).map(s => s.numero_pubblico)")
        for n in sorted(numeri):
            page.goto(base + "risultati.html", wait_until="load", timeout=60000)
            page.evaluate(JS_ANTEPRIMA, n)
            page.wait_for_timeout(400)
            dim = _jpg(page.screenshot(clip={"x": 0, "y": 0, "width": 1200, "height": 630}), ANTEPRIME / f"r{n}.jpg", qualita=85)
            print(f"  anteprima r{n}.jpg: 1200x630, {dim // 1024} KB")
            if dim > 300_000:
                errori.append(f"anteprima r{n}.jpg pesa {dim} byte (limite 300000)")
    except Exception as e:
        errori.append(f"anteprime: {str(e)[:200]}")
    finally:
        ctx.close()
    ctx = br.br.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce", color_scheme="light", locale="it-IT")
    page = ctx.new_page()
    try:
        for nome, indirizzo, attesa in (("home", "index.html", 1500), ("mappa", "mappa_torino.html#tema=vulnerabilita&vista=doppio", 4000)):
            page.goto(base + indirizzo, wait_until="load", timeout=60000)
            page.wait_for_timeout(attesa)
            dim = _jpg(page.screenshot(), IMMAGINI_README / f"{nome}.jpg", larghezza=900, qualita=80)
            print(f"  README {nome}.jpg: {dim // 1024} KB")
            if dim > 250_000:
                errori.append(f"assets/readme/{nome}.jpg pesa {dim} byte (limite 250000)")
        page.goto(base + "risultati.html#p3", wait_until="load", timeout=60000)
        page.wait_for_timeout(1200)
        dim = _jpg(page.locator("#finestra").screenshot(), IMMAGINI_README / "scheda.jpg", larghezza=900, qualita=80, ritaglia_alt=1000)
        print(f"  README scheda.jpg: {dim // 1024} KB")
    except Exception as e:
        errori.append(f"immagini README: {str(e)[:200]}")
    finally:
        ctx.close()
    return errori


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
    ap.add_argument("--solo-design", action="store_true", help="solo i controlli di design (prova_design), veloci: per lavorare sulle schede e sulla home")
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
    if args.solo_design:
        try:
            errori = prova_design(br, cartella)
        finally:
            srv.shutdown()
            srv.server_close()
            br.chiudi()
        print("\nERRORI:\n" + "\n".join("  - " + e for e in errori) if errori else "\nOK: controlli di design")
        return 1 if errori else 0
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
        errori += prova_cambio_indirizzo(br, cartella)
        errori += prova_link_mappa(br, cartella)
        errori += prova_design(br, cartella)
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
            errori += fai_immagini_condivisione(br, cartella)
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
    # pesi dei file in git (piano 2, passo 5): nessun file sopra 50 MB, totale sotto 300 MB
    try:
        import controlla_pesi_git
        err_pesi, avv_pesi, tot_pesi, n_pesi = controlla_pesi_git.controlla(RADICE)
        print(f"  pesi in git: {n_pesi} file, {tot_pesi / 1e6:.1f} MB, {len(avv_pesi)} avvisi, {len(err_pesi)} errori")
        errori += [f"pesi in git: {e}" for e in err_pesi]
    except Exception as e:     # git assente o cartella senza git: non e' un errore delle pagine
        print(f"  pesi in git: non controllati ({str(e)[:80]})")
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
