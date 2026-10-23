#!/usr/bin/env python3
"""
costruisci_asset_sito.py  -  immagini del sito nello stile «Torino»: assets/anteprima.png (1200x630, per l'anteprima dei link). Le icone (logo.png, icona-32.png, icona-180.png) vengono dal logo di Leo e non si rifanno qui.

Usa i numeri veri di data/schede_risultati.js e le sezioni di Torino dentro mappa_torino.html (fragilita' sociale), il font Barlow Condensed
di assets/font/ e Playwright (Chromium). Uso: python scripts/costruisci_asset_sito.py
Scrive: assets/anteprima.png.
"""
import glob
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

AQUI = Path(__file__).resolve().parent
RADICE = AQUI.parent
sys.path.insert(0, str(AQUI / "prove"))
import costruisci_prove_stile as ps  # noqa: E402  (mappa di Torino e colori)


def numeri():
    t = (RADICE / "data" / "schede_risultati.js").read_text(encoding="utf-8")
    schede = json.loads(t[t.index("["):t.rindex("]") + 1])
    out = []
    for s in sorted(schede, key=lambda x: x.get("numero_pubblico") or 99):
        n = s["forma"]["numero"]
        v = n["valore"]
        txt = f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v).replace(".", ",")
        out.append((txt + ("%" if n["unita"] == "%" else (" " + n["unita"] if n["unita"] else "")), s["forma"]["titolo"]))
    return out


def pagina():
    scheda, S, g04 = ps.carica_dati()
    soglie = []
    svg, W, H = ps.mappa_svg(S, g04, soglie)
    p = ps.PALETTE["torino"]["scuro"]
    sc = ps.scala(p)
    css_sc = "".join(f".c{i}{{fill:{c}}}" for i, c in enumerate(sc))
    num = numeri()
    didascalie = ["dei residenti ha i servizi a 15 minuti a piedi", "il tempo dell'auto, coi mezzi pubblici", "residenti dove servizi pochi e fragilità alta"]
    scelti = [num[0], num[3], num[4]] if len(num) >= 5 else num[:3]
    righe = "".join(f'<div class="n"><b>{v}</b><span>{d}</span></div>' for (v, _t), d in zip(scelti, didascalie))
    font = (RADICE / "assets" / "font").as_uri()
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:BC;font-weight:700;src:url({font}/BarlowCondensed-700.woff2)}}
@font-face{{font-family:BC;font-weight:600;src:url({font}/BarlowCondensed-600.woff2)}}
@font-face{{font-family:B;font-weight:400;src:url({font}/Barlow-400.woff2)}}
@font-face{{font-family:B;font-weight:600;src:url({font}/Barlow-600.woff2)}}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;background:linear-gradient(135deg,#08142e 0%,#0b2559 100%);color:#f1f4fb;font:400 26px/1.3 B;position:relative;overflow:hidden}}
.oro{{position:absolute;left:0;right:0;top:0;height:10px;background:#e3bf55}}
.testo{{position:absolute;left:64px;top:84px;width:640px}}
h1{{font:700 118px/0.92 BC;text-transform:uppercase;letter-spacing:.01em}}
h1 em{{font-style:normal;color:#e3bf55}}
.sotto{{margin-top:22px;font-size:29px;color:#c8d2ea;white-space:nowrap}}
.nums{{position:absolute;left:64px;bottom:44px;display:flex;gap:34px}}
.n b{{display:block;font:700 54px/1 BC;color:#e3bf55}}
.n span{{display:block;font-size:17px;color:#a8b5d1;max-width:190px;line-height:1.25;margin-top:4px}}
.mappa{{position:absolute;right:40px;top:50px;width:470px;height:{round(470 * H / W)}px}}
{css_sc}
</style></head><body><div class="oro"></div>
<div class="testo"><h1>Torino<br><em>Mobilità</em></h1><div class="sotto">Come si muove la città, con i numeri veri.</div></div>
<svg class="mappa" viewBox="0 0 {W} {H}"><g>{svg}</g></svg>
<div class="nums">{righe}</div></body></html>"""


def main():
    cand = sorted(glob.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium-*", "chrome-linux", "chrome")))
    html = RADICE / "assets" / "_anteprima_tmp.html"
    html.write_text(pagina(), encoding="utf-8")
    try:
        with sync_playwright() as pw:
            try:
                br = pw.chromium.launch()
            except Exception:
                br = pw.chromium.launch(executable_path=cand[-1])
            pg = br.new_page(viewport={"width": 1200, "height": 630})
            pg.goto(html.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            pg.screenshot(path=str(RADICE / "assets" / "anteprima.png"))
            br.close()
    finally:
        html.unlink(missing_ok=True)
    for n in ("anteprima.png",):
        print(n, (RADICE / "assets" / n).stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
