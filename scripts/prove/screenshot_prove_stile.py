#!/usr/bin/env python3
"""Screenshot di sviluppo/prove_stile.html con Playwright: computer (1440 px) e telefono (390 px), versione chiara e scura, pagina intera.
Scrive sviluppo/prove_stile_computer_chiaro.png, ..._computer_scuro.png, ..._telefono_chiaro.png, ..._telefono_scuro.png.
Controlla anche: nessun errore JavaScript, nessuna richiesta esterna, nessuno scorrimento orizzontale, font caricati."""
import glob
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

RADICE = Path(__file__).resolve().parent.parent.parent
PAGINA = RADICE / "sviluppo" / "prove_stile.html"


def main():
    cand = sorted(glob.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium-*", "chrome-linux", "chrome")))
    problemi = []
    with sync_playwright() as p:
        try:
            br = p.chromium.launch()
        except Exception:
            br = p.chromium.launch(executable_path=cand[-1])
        for nome, (w, h) in (("computer", (1440, 900)), ("telefono", (390, 844))):
            for tema in ("chiaro", "scuro"):
                ctx = br.new_context(viewport={"width": w, "height": h}, color_scheme="dark" if tema == "scuro" else "light")
                pg = ctx.new_page()
                esterne, errori = [], []
                pg.on("request", lambda r: esterne.append(r.url) if not r.url.startswith(("file:", "data:")) else None)
                pg.on("pageerror", lambda e: errori.append(str(e)))
                pg.goto(f"file://{PAGINA}#{tema}")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(600)
                larghezza = pg.evaluate("document.documentElement.scrollWidth")
                font = pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight)")
                png = RADICE / "sviluppo" / f"prove_stile_{nome}_{tema}.png"
                pg.screenshot(path=str(png), full_page=True)
                print(f"{png.name}: {png.stat().st_size // 1024} KB, larghezza pagina {larghezza}, font caricati: {len(font)}")
                if larghezza > w + 1:
                    problemi.append(f"{nome}/{tema}: scorrimento orizzontale ({larghezza} > {w})")
                if esterne:
                    problemi.append(f"{nome}/{tema}: richieste esterne {esterne[:2]}")
                if errori:
                    problemi.append(f"{nome}/{tema}: errori JS {errori[:2]}")
                if len(font) < 6:
                    problemi.append(f"{nome}/{tema}: pochi font caricati ({len(font)})")
                ctx.close()
        br.close()
    for x in problemi:
        print("PROBLEMA:", x)
    print("OK" if not problemi else "CI SONO PROBLEMI")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
