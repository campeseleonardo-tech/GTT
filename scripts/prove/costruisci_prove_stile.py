#!/usr/bin/env python3
"""
costruisci_prove_stile.py  -  scrive sviluppo/prove_stile.html: tre prove di stile («Notte», «Carta», «Torino») sulla stessa pagina.

Piano 4, passo 1. Per ogni stile, uguali per tutti: titolo del sito, riquadro di risultato VERO (scheda 5 di data/schede_risultati.js),
grafico a barre (dati veri della stessa scheda), 10 omini con 1 colorato, una mappa di Torino con le sezioni colorate (fragilita' sociale,
dati veri dentro mappa_torino.html, 5 classi con i numeri scritti), piè di pagina «Chi sono»; palette con i codici, font, contrasti calcolati.
Ogni stile ha la versione chiara e quella scura (bottone in alto; di partenza segue il sistema).

Scarica i font da Google Fonts (solo la parte latina, woff2) in sviluppo/prove_stile_font/ se mancano: la pagina non ha link esterni.
Uso: python scripts/prove/costruisci_prove_stile.py        (poi: scripts/prove/screenshot_prove_stile.py)
"""
import importlib.util
import json
import re
import sys
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RADICE = AQUI.parent.parent
SVILUPPO = RADICE / "sviluppo"
FONT_DIR = SVILUPPO / "prove_stile_font"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# ------------------------------------------------------------------ stili
FONT = {
    "notte": {"titoli": ("Space Grotesk", "600;700"), "testi": ("DM Sans", "400;600")},
    "carta": {"titoli": ("Fraunces", "600;700"), "testi": ("Source Sans 3", "400;600")},
    "torino": {"titoli": ("Barlow Condensed", "600;700"), "testi": ("Barlow", "400;600")},
}
# ruoli: bg fondo, sup riquadri, txt testo, muted testo secondario, link link e numeri, fill colore pieno (bottoni, barre forti),
# on testo sopra fill, bene verde acqua, male corallo (granata in «Torino»), extra secondo colore (oro in «Torino»), bordo, mid grigio neutro della scala
PALETTE = {
    "notte": {
        "scuro": dict(bg="#0b1426", sup="#121e38", txt="#e9eefa", muted="#a3b3d1", link="#3ee0cc", fill="#19d3c5", on="#04201e",
                      bene="#19d3c5", male="#ff7a6b", extra="#19d3c5", bordo="#26375c", mid="#3a4a6e"),
        "chiaro": dict(bg="#f2f6fb", sup="#ffffff", txt="#0b1426", muted="#4b5d7d", link="#00796f", fill="#0fb5a6", on="#00221f",
                       bene="#0b9d90", male="#d6443a", extra="#00796f", bordo="#cfd9e8", mid="#dde4ef"),
    },
    "carta": {
        "scuro": dict(bg="#1a1712", sup="#241f18", txt="#f4ecd9", muted="#b9ae98", link="#ff7b5c", fill="#ff6a47", on="#1a1712",
                      bene="#3cc9b8", male="#ff6a47", extra="#ff6a47", bordo="#4a4234", mid="#4a4234"),
        "chiaro": dict(bg="#f5eddc", sup="#fffaf0", txt="#151515", muted="#5b5346", link="#b92f16", fill="#e8472f", on="#151515",
                       bene="#0d8076", male="#e8472f", extra="#b92f16", bordo="#151515", mid="#e2d8c2"),
    },
    "torino": {
        "scuro": dict(bg="#08142e", sup="#0f2147", txt="#f1f4fb", muted="#a8b5d1", link="#e3bf55", fill="#e0b84a", on="#08142e",
                      bene="#32cfc2", male="#ee6a80", extra="#e0b84a", bordo="#27407a", mid="#34507f"),
        "chiaro": dict(bg="#f3f5fa", sup="#ffffff", txt="#0b2559", muted="#4a5a7a", link="#0b3a8c", fill="#c9a227", on="#0b2559",
                       bene="#0b8f8a", male="#a61e33", extra="#8a6d00", bordo="#c9d2e4", mid="#dde3ef"),
    },
}
NOMI = {"notte": "Notte", "carta": "Carta", "torino": "Torino"}
DESCR = {
    "notte": "blu notte, verde acqua acceso, corallo. Moderno, da schermo; bordi morbidi.",
    "carta": "crema e nero, un solo colore forte. Da giornale: titoli con le grazie, filetti neri.",
    "torino": "blu e oro, granata per gli allarmi. Istituzionale e sabaudo; titoli stretti e maiuscoli.",
}


# ------------------------------------------------------------------ colori
def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminanza(h):
    r, g, b = (lin(x) for x in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrasto(a, b):
    la, lb = luminanza(a), luminanza(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def a_oklab(h):
    r, g, b = (lin(x) for x in rgb(h))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def da_oklab(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    def gam(c):
        c = max(0.0, min(1.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return "#" + "".join(f"{round(gam(x) * 255):02x}" for x in (r, g, bb))


def mescola(h1, h2, t):
    a, b = a_oklab(h1), a_oklab(h2)
    return da_oklab(*(x + (y - x) * t for x, y in zip(a, b)))


def scala(p):
    """5 classi dal verde acqua (bene) al corallo (male), passando dal grigio neutro: 0 = bene ... 4 = male."""
    return [p["bene"], mescola(p["bene"], p["mid"], 0.55), p["mid"], mescola(p["mid"], p["male"], 0.45), p["male"]]


def tabella_contrasti(p):
    righe = [("testo su fondo", p["txt"], p["bg"], 4.5), ("testo su riquadro", p["txt"], p["sup"], 4.5),
             ("testo secondario su fondo", p["muted"], p["bg"], 4.5), ("testo secondario su riquadro", p["muted"], p["sup"], 4.5),
             ("link e numeri su fondo", p["link"], p["bg"], 4.5), ("link e numeri su riquadro", p["link"], p["sup"], 4.5),
             ("testo sul colore pieno", p["on"], p["fill"], 4.5),
             ("verde acqua (grafici) su riquadro", p["bene"], p["sup"], 3.0), ("corallo/granata (grafici) su riquadro", p["male"], p["sup"], 3.0)]
    return [(n, a, b, round(contrasto(a, b), 2), soglia, contrasto(a, b) >= soglia) for n, a, b, soglia in righe]


# ------------------------------------------------------------------ font
def scarica_font():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    css_out, usati = [], {}
    for stile, fam in FONT.items():
        for ruolo, (nome, pesi) in fam.items():
            fn = nome.replace(" ", "")
            for peso in pesi.split(";"):
                file = FONT_DIR / f"{fn}-{peso}.woff2"
                if not file.exists():
                    q = f"https://fonts.googleapis.com/css2?family={nome.replace(' ', '+')}:wght@{pesi}&display=swap"
                    css = urllib.request.urlopen(urllib.request.Request(q, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8")
                    blocchi = re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S)
                    for sub, corpo in blocchi:
                        if sub != "latin":
                            continue
                        peso_b = re.search(r"font-weight:\s*(\d+)", corpo).group(1)
                        url = re.search(r"url\((https://[^)]+\.woff2)\)", corpo).group(1)
                        dest = FONT_DIR / f"{fn}-{peso_b}.woff2"
                        if not dest.exists():
                            dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read())
                    if not file.exists():
                        # famiglia a peso variabile: Google restituisce lo stesso file per piu' pesi
                        for altro in FONT_DIR.glob(f"{fn}-*.woff2"):
                            file.write_bytes(altro.read_bytes())
                            break
                css_out.append(f"@font-face{{font-family:'{nome}';font-style:normal;font-weight:{peso};font-display:swap;"
                               f"src:url(prove_stile_font/{fn}-{peso}.woff2) format('woff2')}}")
                usati[file.name] = file.stat().st_size
    return "\n".join(css_out), usati


# ------------------------------------------------------------------ dati veri
def carica_dati():
    t = (RADICE / "data" / "schede_risultati.js").read_text(encoding="utf-8")
    schede = json.loads(t[t.index("["):t.rindex("]") + 1])
    scheda = next(s for s in schede if s["risultato"] == "10")
    spec = importlib.util.spec_from_file_location("g04", RADICE / "scripts" / "04_genera_mappa.py")
    g04 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g04)
    riga = next(x for x in (RADICE / "mappa_torino.html").read_text(encoding="utf-8").split("\n") if x.startswith("const DATI = "))
    D = json.loads(riga[len("const DATI = "):].rstrip(";"))
    return scheda, D["sezioni"], g04


def mappa_svg(S, g04, soglie_out):
    """Sezioni di Torino colorate per classe di fragilita' (quintili); path relativi in interi. Ritorna (svg interno, larghezza, altezza)."""
    import math
    idx = [i for i in range(S["n"]) if S["c"][i] == 1272 and S["v"][i] is not None and S["p"][i] and S["g"][i]]
    valori = sorted(S["v"][i] for i in idx)
    soglie = [valori[int(len(valori) * q)] for q in (0.2, 0.4, 0.6, 0.8)]
    soglie_out.extend(soglie)
    anelli = {}
    lat_min = lon_min = 1e9
    lat_max = lon_max = -1e9
    for i in idx:
        poligoni = []
        for r in S["g"][i].split(" "):
            n = g04.decod_int(r)
            la = lo = 0
            pts = []
            for k in range(0, len(n), 2):
                la += n[k]
                lo += n[k + 1]
                pts.append((la / 1e4, lo / 1e4))
            poligoni.append(pts)
            for la_, lo_ in pts:
                lat_min, lat_max = min(lat_min, la_), max(lat_max, la_)
                lon_min, lon_max = min(lon_min, lo_), max(lon_max, lo_)
        anelli[i] = poligoni
    k = math.cos(math.radians((lat_min + lat_max) / 2))
    larg = 900
    scala_ = larg / ((lon_max - lon_min) * k)
    alt = round((lat_max - lat_min) * scala_)
    percorsi = [[] for _ in range(5)]
    for i in idx:
        c = sum(S["v"][i] > s for s in soglie)
        d = []
        for pts in anelli[i]:
            xy = [(round((lo - lon_min) * k * scala_), round((lat_max - la) * scala_)) for la, lo in pts]
            sempl = [xy[0]]
            for p in xy[1:]:
                if p != sempl[-1]:
                    sempl.append(p)
            if len(sempl) < 3:
                continue
            d.append("M" + str(sempl[0][0]) + " " + str(sempl[0][1]) + "".join(f"l{x - px} {y - py}" for (px, py), (x, y) in zip(sempl, sempl[1:])) + "z")
        percorsi[c].append("".join(d))
    svg = "".join(f'<path class="c{c}" d="{"".join(p)}"/>' for c, p in enumerate(percorsi))
    return svg, larg, alt


# ------------------------------------------------------------------ pagina
def css_stile(stile, font):
    t, x = FONT[stile]["titoli"][0], FONT[stile]["testi"][0]
    extra = {
        "notte": ".s-notte .riquadro{border-radius:16px;box-shadow:0 0 0 1px var(--bordo)} .s-notte h1,.s-notte h2{letter-spacing:-.01em} .s-notte .grande{font-weight:700}",
        "carta": ".s-carta .riquadro{border-radius:2px;border:2px solid var(--bordo);box-shadow:5px 5px 0 var(--bordo)} .s-carta h1{font-weight:700;letter-spacing:-.02em} .s-carta .grande{font-weight:700} .s-carta .filetto{border-top:3px double var(--bordo)}",
        "torino": ".s-torino .riquadro{border-radius:6px;border-top:5px solid var(--extra);box-shadow:0 0 0 1px var(--bordo)} .s-torino h1,.s-torino h2,.s-torino .grande{text-transform:uppercase;letter-spacing:.02em} .s-torino h1{font-size:2.6rem}",
    }[stile]
    return (f".s-{stile}{{font-family:'{x}',system-ui,sans-serif}} .s-{stile} h1,.s-{stile} h2,.s-{stile} h3,.s-{stile} .grande,.s-{stile} .titolo"
            f"{{font-family:'{t}',system-ui,sans-serif}} {extra}")


def variabili(stile, tema, p):
    sc = scala(p)
    v = "".join(f"--{k}:{val};" for k, val in p.items()) + "".join(f"--m{i}:{c};" for i, c in enumerate(sc)) + f"--neutro:{mescola(p['muted'], p['sup'], 0.55)};"
    return f'.s-{stile}[data-t="{tema}"]{{{v}}}'


def omini(p_male="var(--male)"):
    omino = '<svg viewBox="0 0 24 48" class="omino{c}" aria-hidden="true"><circle cx="12" cy="7" r="6"/><path d="M5 17h14a3 3 0 0 1 3 3v14h-4v14h-5V34h-2v14H6V34H2V20a3 3 0 0 1 3-3z"/></svg>'
    return "".join(omino.format(c=" evidenza" if i == 9 else "") for i in range(10))


def costruisci():
    font_css, usati = scarica_font()
    scheda, S, g04 = carica_dati()
    soglie = []
    svg_interno, W, H = mappa_svg(S, g04, soglie)
    f = scheda["forma"]
    num = f["numero"]
    valore = f"{num['valore']:,}".replace(",", ".") if isinstance(num["valore"], int) else str(num["valore"])
    voci = f["altri"][0]["voci"]
    tono_cl = {"rosso": "m4", "arancio": "m3", "blu": "neutro", "verde": "m0"}
    massimo = max(v["valore"] for v in voci)
    barre = "".join(
        f'<div class="barra"><span class="et">{v["label"]}</span><span class="pista"><i style="width:{100 * v["valore"] / massimo:.1f}%;background:var(--{tono_cl.get(v["tono"], "neutro")})"></i></span>'
        f'<span class="val">{v["testo"]}</span></div>' for v in voci)
    nomi_classe = ["molto bassa", "bassa", "media", "alta", "molto alta"]
    estremi = [f"fino a {soglie[0]:.0f}", f"{soglie[0]:.0f}–{soglie[1]:.0f}", f"{soglie[1]:.0f}–{soglie[2]:.0f}", f"{soglie[2]:.0f}–{soglie[3]:.0f}", f"oltre {soglie[3]:.0f}"]
    legenda = "".join(f'<li><i style="background:var(--m{i})"></i>{nomi_classe[i]} ({estremi[i]})</li>' for i in range(5))

    colonne, stili_css, var_css = [], [], []
    for stile in ("notte", "carta", "torino"):
        stili_css.append(css_stile(stile, FONT[stile]))
        pal_html = ""
        for tema in ("chiaro", "scuro"):
            p = PALETTE[stile][tema]
            var_css.append(variabili(stile, tema, p))
            sw = "".join(f'<li><i style="background:{p[k]}"></i><code>{p[k]}</code> {k}</li>' for k in ("bg", "sup", "txt", "muted", "link", "fill", "bene", "male", "extra", "bordo"))
            sw += "".join(f'<li><i style="background:{c}"></i><code>{c}</code> scala {i + 1}</li>' for i, c in enumerate(scala(p)))
            ct = "".join(f'<tr class="{"ok" if ok else "no"}"><td>{n}</td><td><code>{a}</code> su <code>{b}</code></td><td>{val}:1</td><td>{"≥" + str(s) if ok else "SOTTO " + str(s)}</td></tr>'
                         for n, a, b, val, s, ok in tabella_contrasti(p))
            pal_html += (f'<div class="tema-{tema}"><h3>Palette {tema}</h3><ul class="sw">{sw}</ul>'
                         f'<table class="contrasti"><caption>Contrasti (WCAG: testi ≥ 4,5, grafici ≥ 3)</caption>{ct}</table></div>')
        colonne.append(f'''<section class="s-{stile}" data-t="chiaro" aria-labelledby="t-{stile}">
  <p class="tag-stile">Stile {NOMI[stile]}</p><p class="descr">{DESCR[stile]}</p>
  <div class="pagina">
    <header class="sito"><h1 id="t-{stile}">Torino Mobilità</h1><p class="sotto">Come si muove la città, con i numeri veri.</p></header>
    <article class="riquadro">
      <p class="eti">Risultato 5</p>
      <h2>{f["titolo"]}</h2>
      <p class="grande">{valore}</p>
      <p class="testo-num">{num["testo"]}</p>
      <div class="omini" role="img" aria-label="10 persone, 1 evidenziata: circa 1 torinese su 10">{omini()}</div>
      <p class="didascalia">circa 1 torinese su 10 (il 9,5%)</p>
      <p class="apri"><a href="#">Apri la scheda →</a></p>
    </article>
    <article class="riquadro">
      <h3>{f["altri"][0]["titolo"]}</h3>
      <div class="barre">{barre}</div>
    </article>
    <article class="riquadro">
      <h3>Fragilità sociale per sezione di censimento (Torino)</h3>
      <svg viewBox="0 0 {W} {H}" class="mappa" role="img" aria-label="Mappa di Torino, sezioni colorate per fragilità sociale"><use href="#sez-torino"/></svg>
      <ul class="legenda">{legenda}</ul>
      <p class="didascalia">Indice di fragilità 0-100, cinque gruppi con lo stesso numero di sezioni. Dati: ISTAT 2021, elaborazione propria.</p>
    </article>
    <footer class="piede filetto"><h3>Chi sono</h3><p>Leonardo Campese · <a href="#">LinkedIn</a> · <a href="#">campese.leonardo@gmail.com</a> · <a href="#">GitHub</a></p>
    <p class="piccolo">Codice con licenza MIT. Dati aggiornati al 22/10/2026.</p></footer>
  </div>
  <details class="scheda-tecnica" open><summary>Palette, font e contrasti</summary>
    <p><b>Font:</b> titoli <code>{FONT[stile]["titoli"][0]}</code> ({FONT[stile]["titoli"][1].replace(";", ", ")}), testi <code>{FONT[stile]["testi"][0]}</code> ({FONT[stile]["testi"][1].replace(";", ", ")}).</p>
    {pal_html}
  </details>
</section>''')
    base_css = """
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#e9e9ee;color:#111;font:16px/1.5 system-ui,sans-serif}
body[data-t="scuro"]{background:#05070d}
.testata{padding:18px 16px 6px;max-width:1500px;margin:0 auto;font-family:system-ui,sans-serif}
body[data-t="scuro"] .testata{color:#eee}
.testata h1{font-size:1.5rem;margin:0 0 4px}
.testata p{margin:2px 0;max-width:70ch}
.bottoni{display:flex;gap:8px;margin:10px 0 0}
.bottoni button{font:600 14px system-ui;padding:8px 14px;border-radius:8px;border:1px solid #888;background:#fff;color:#111;cursor:pointer}
.bottoni button[aria-pressed="true"]{background:#111;color:#fff}
.colonne{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:12px 16px 40px;max-width:1500px;margin:0 auto}
@media (max-width:1000px){.colonne{grid-template-columns:1fr}}
.colonne>section{background:var(--bg);color:var(--txt);border-radius:14px;padding:14px;min-width:0}
.tag-stile{font:700 12px system-ui;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin:0}
.descr{color:var(--muted);margin:2px 0 12px;font-size:.9rem}
.sito h1{font-size:2.3rem;line-height:1.05;margin:6px 0 2px;color:var(--txt)}
.sito .sotto{margin:0 0 14px;color:var(--muted)}
.riquadro{background:var(--sup);padding:16px;margin:0 0 14px}
.riquadro h2{font-size:1.3rem;line-height:1.2;margin:2px 0 8px}
.riquadro h3{font-size:1.05rem;line-height:1.25;margin:0 0 10px}
.eti{margin:0;font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:600}
.grande{font-size:3.6rem;line-height:1;margin:6px 0;color:var(--link)}
.testo-num{margin:0 0 10px;color:var(--txt)}
.omini{display:flex;gap:4px;align-items:flex-end;margin:6px 0 2px}
.omini svg{width:22px;height:44px;fill:var(--neutro)}
.omini svg.evidenza{fill:var(--male)}
.didascalia{margin:2px 0 0;color:var(--muted);font-size:.85rem}
.apri{margin:10px 0 0}
a{color:var(--link);font-weight:600;text-underline-offset:3px}
.barra{display:grid;grid-template-columns:minmax(90px,34%) 1fr;gap:2px 10px;align-items:center;margin:0 0 10px}
.barra .et{font-size:.88rem}
.barra .pista{background:var(--bg);height:16px;border-radius:3px;display:block;overflow:hidden}
.barra .pista i{display:block;height:100%}
.barra .val{grid-column:2;font-size:.82rem;color:var(--muted)}
.mappa{width:100%;height:auto;display:block;background:var(--bg);border-radius:4px}
.legenda{list-style:none;margin:8px 0 0;padding:0;display:grid;gap:3px;font-size:.82rem}
.legenda i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-2px}
.piede{margin-top:8px;padding-top:12px}
.piede h3{margin:0 0 4px;font-size:1.05rem}
.piede p{margin:2px 0}
.piccolo{font-size:.8rem;color:var(--muted)}
.filetto{border-top:1px solid var(--bordo)}
.scheda-tecnica{margin-top:16px;font-size:.84rem;background:var(--sup);padding:10px 12px;border-radius:8px}
.scheda-tecnica summary{cursor:pointer;font-weight:700}
.scheda-tecnica code{font-size:.9em}
.sw{list-style:none;padding:0;margin:4px 0 10px;columns:2;font-size:.8rem}
.sw li{margin:0 0 3px;break-inside:avoid}
.sw i{display:inline-block;width:14px;height:14px;border-radius:3px;margin-right:6px;vertical-align:-3px;box-shadow:0 0 0 1px #8887}
.contrasti{border-collapse:collapse;width:100%;font-size:.76rem}
.contrasti caption{text-align:left;font-weight:600;margin-bottom:3px}
.contrasti td{border-top:1px solid var(--bordo);padding:3px 4px;vertical-align:top}
.contrasti tr.no td{color:var(--male);font-weight:700}
.s-notte[data-t="chiaro"] .tema-scuro,.s-notte[data-t="scuro"] .tema-chiaro,.s-carta[data-t="chiaro"] .tema-scuro,.s-carta[data-t="scuro"] .tema-chiaro,
.s-torino[data-t="chiaro"] .tema-scuro,.s-torino[data-t="scuro"] .tema-chiaro{display:none}
.c0{fill:var(--m0)}.c1{fill:var(--m1)}.c2{fill:var(--m2)}.c3{fill:var(--m3)}.c4{fill:var(--m4)}
@media (prefers-reduced-motion:no-preference){a{transition:color .15s}}
"""
    pagina = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prove di stile</title>
<style>
{font_css}
{base_css}
{chr(10).join(var_css)}
{chr(10).join(stili_css)}
</style>
</head>
<body data-t="chiaro">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><g id="sez-torino">{svg_interno}</g></defs></svg>
<div class="testata">
  <h1>Prove di stile — Torino Mobilità</h1>
  <p>Tre stili sulla stessa pagina: lo stesso risultato vero (scheda 5), lo stesso grafico, la stessa mappa di Torino. Cambiano colori, font e forme. In ogni stile il bene è verde acqua e il male è corallo (granata in «Torino»); i numeri sono sempre scritti. Sotto ogni colonna: palette con i codici e contrasti.</p>
  <div class="bottoni" role="group" aria-label="Versione">
    <button type="button" data-v="chiaro" aria-pressed="true">Chiaro</button>
    <button type="button" data-v="scuro" aria-pressed="false">Scuro</button>
  </div>
</div>
<main class="colonne">
{chr(10).join(colonne)}
</main>
<script>
(function(){{
  function applica(v){{
    document.body.setAttribute("data-t", v);
    document.querySelectorAll(".colonne>section").forEach(function(s){{ s.setAttribute("data-t", v); }});
    document.querySelectorAll(".bottoni button").forEach(function(b){{ b.setAttribute("aria-pressed", b.getAttribute("data-v") === v ? "true" : "false"); }});
  }}
  document.querySelectorAll(".bottoni button").forEach(function(b){{ b.addEventListener("click", function(){{ applica(b.getAttribute("data-v")); }}); }});
  var h = location.hash.replace("#", "");
  applica(h === "scuro" || h === "chiaro" ? h : (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "scuro" : "chiaro"));
}})();
</script>
</body>
</html>
"""
    (SVILUPPO / "prove_stile.html").write_text(pagina, encoding="utf-8")
    # contrasti per l'esito
    fuori = []
    for stile in PALETTE:
        for tema, p in PALETTE[stile].items():
            for n, a, b, val, s, ok in tabella_contrasti(p):
                if not ok:
                    fuori.append(f"{stile}/{tema}: {n} {a} su {b} = {val} (serve {s})")
    peso_font = sum(usati.values())
    print(f"scritto {SVILUPPO / 'prove_stile.html'} ({len(pagina) / 1e3:.0f} KB), font {len(usati)} file, {peso_font / 1e3:.0f} KB")
    print("contrasti sotto la soglia:" if fuori else "contrasti: tutti sopra la soglia")
    for x in fuori:
        print("  ", x)
    return 1 if fuori else 0


if __name__ == "__main__":
    sys.exit(costruisci())
