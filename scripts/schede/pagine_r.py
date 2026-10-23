"""Pagine dei singoli risultati (r/1.html ... r/5.html) e riga dei risultati del README.

r/N.html e' una pagina minima: titolo, descrizione e immagine di anteprima del risultato (Open Graph, per i post su LinkedIn e simili) e un rimando
immediato a ../risultati.html#pN. L'immagine 1200x630 (assets/anteprime/rN.jpg) la fa scripts/prova_pagine.py dai dati della scheda.
Il README ha due elenchi (italiano e inglese) fra i segnaposto <!-- RISULTATI-IT:INIZIO --> ... <!-- RISULTATI-IT:FINE --> e lo stesso con EN:
li riscrive questo modulo, cosi' i numeri non invecchiano. Nessun numero e' scritto a mano."""
import html
import re

from schede.comune import RADICE

SITO = "https://campeseleonardo-tech.github.io/Turin-mobility/"
NOME_SITO = "Torino Mobilità"
CARTELLA = RADICE / "r"
README = RADICE / "README.md"

PAGINA = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo} — {sito}</title>
<meta name="description" content="{descrizione}">
<meta name="theme-color" content="#0b2559">
<link rel="icon" href="../assets/icona-32.png" sizes="32x32" type="image/png">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{sito}">
<meta property="og:locale" content="it_IT">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descrizione}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{immagine}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titolo}">
<meta name="twitter:description" content="{descrizione}">
<meta name="twitter:image" content="{immagine}">
<meta http-equiv="refresh" content="0; url=../risultati.html#p{n}">
<link rel="stylesheet" href="../assets/stile.css">
</head>
<body>
<main>
<p class="sub">{sito} · Risultato {n}</p>
<h1>{titolo}</h1>
<p class="sub">{descrizione}</p>
<p><a class="btn primario" href="../risultati.html#p{n}">Apri il risultato</a></p>
</main>
<script>location.replace("../risultati.html#p{n}");</script>
</body>
</html>
"""


def _grande(f, lingua):
    """Numero grande della scheda come testo: «99,2%», «2–3 volte», «79.598»."""
    n = f["numero"]
    v = n["valore"]
    if isinstance(v, int):
        v = f"{v:,}".replace(",", "," if lingua == "en" else ".")
    elif isinstance(v, float):
        v = f"{v:g}" if lingua == "en" else f"{v:g}".replace(".", ",")
    return f"{v}%" if n["unita"] == "%" else f"{v} {n['unita']}".strip()


def scrivi_pagine_r(schede):
    """Una pagina per ogni scheda con numero pubblico e forma. Ritorna quante ne ha scritte."""
    CARTELLA.mkdir(exist_ok=True)
    scritte = 0
    for s in schede:
        n = s.get("numero_pubblico")
        f = s.get("forma")
        if n is None or not f:
            continue
        testo = PAGINA.format(n=n, titolo=html.escape(f["titolo"], quote=True), descrizione=html.escape(f["domanda"], quote=True), sito=NOME_SITO,
                              url=f"{SITO}r/{n}.html", immagine=f"{SITO}assets/anteprime/r{n}.jpg")
        (CARTELLA / f"{n}.html").write_text(testo, encoding="utf-8")
        scritte += 1
    return scritte


def _elenco(schede, lingua):
    righe = []
    for s in sorted((x for x in schede if x.get("numero_pubblico") is not None and x.get("forma")), key=lambda x: x["numero_pubblico"]):
        f = s["forma_en"] if lingua == "en" and s.get("forma_en") else s["forma"]
        n = s["numero_pubblico"]
        grande = _grande(f, lingua)
        righe.append(f"{n}. **{f['titolo']}**  \n   {f['domanda']} → **{grande}** {f['numero']['testo']}. [{'Open' if lingua == 'en' else 'Apri'}]({SITO}r/{n}.html)")
    return "\n".join(righe)


def aggiorna_readme(schede):
    """Riscrive gli elenchi dei risultati del README fra i segnaposto. Ritorna True se il README e' cambiato."""
    if not README.is_file():
        return False
    testo = vecchio = README.read_text(encoding="utf-8")
    for lingua, sigla in (("it", "IT"), ("en", "EN")):
        rx = re.compile(rf"(<!-- RISULTATI-{sigla}:INIZIO -->)\n.*?(<!-- RISULTATI-{sigla}:FINE -->)", re.S)
        if not rx.search(testo):
            print(f"AVVISO: README.md senza i segnaposto RISULTATI-{sigla}")
            continue
        testo = rx.sub(lambda m: m.group(1) + "\n" + _elenco(schede, lingua) + "\n" + m.group(2), testo)
    if testo != vecchio:
        README.write_text(testo, encoding="utf-8")
    return testo != vecchio
