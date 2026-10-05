# -*- coding: utf-8 -*-
"""
genera_preventivo_RIFERIMENTO.py - generatore di riferimento (scritto e provato dall'Ufficio, solo libreria standard).
Parte dal modello Word ORIGINALE e cambia soltanto il testo dei segnaposto [[...]] in word/document.xml.
Intestazioni, piè di pagina, logo (immagini), stili e tutto il resto restano IDENTICI byte per byte: il logo non puo' piu' "rompersi".

Uso:  python genera_preventivo_RIFERIMENTO.py dati.json uscita.docx [modello.docx]
dati.json: oggetto con una chiave per segnaposto = testo prima del " — " (es. "DATA", "PROTOCOLLO", "TOTALE") e "VOCI" = lista di righe.
"""
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

MODELLO = Path(__file__).resolve().parent.parent / "Preventivo Automatico" / "MOD_PREVENTIVO_v4_1.docx"
RE_SEG = re.compile(r"\[\[(.+?)\]\]", re.S)
RE_P = re.compile(r"<w:p[ >].*?</w:p>", re.S)
RE_T = re.compile(r"(<w:t(?: [^>]*)?>)(.*?)(</w:t>)", re.S)


def chiave(testo):
    return testo.split(" — ")[0].strip()


def testo_par(p):
    return "".join(m.group(2) for m in RE_T.finditer(p))


def _un(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&")


RE_SUGG = re.compile(r"\s*\(iniziale nome[^)]*\)")      # suggerimento dopo il protocollo: non va nel documento finale


def _sost(testo, dati):
    return RE_SUGG.sub("", RE_SEG.sub(lambda m: str(dati.get(chiave(_un(m.group(1))), m.group(0))), testo))


def sostituisci_par(p, dati):
    """Sostituisce i segnaposto di un paragrafo. Se ogni segnaposto sta dentro un solo <w:t> si cambia solo quello (la formattazione di ogni
    pezzo resta); se un segnaposto e' spezzato tra piu' <w:t> il testo nuovo va nel primo e gli altri si svuotano."""
    ts = list(RE_T.finditer(p))
    if not ts:
        return p
    testi = [_un(m.group(2)) for m in ts]
    pieno = "".join(testi)
    if "[[" not in pieno:
        return p
    if all(t.count("[[") == t.count("]]") for t in testi):
        nuovi = [escape(_sost(t, dati)) for t in testi]
    else:
        nuovi = [escape(_sost(pieno, dati))] + [""] * (len(ts) - 1)
    res, pos = [], 0
    for m, nt in zip(ts, nuovi):
        res.append(p[pos:m.start()])
        res.append(m.group(1) + nt + m.group(3))
        pos = m.end()
    res.append(p[pos:])
    return "".join(res)


def prepara_voci(xml, voci):
    """Le righe '•<TAB>[[Voce N ...]]' del modello sono il prototipo: si replicano una per voce (le altre si tolgono)."""
    pars = list(RE_P.finditer(xml))
    idx = [m for m in pars if re.search(r"\[\[Voce \d+", testo_par(m.group(0)))]
    if not idx or not voci:
        return xml
    proto = idx[0].group(0)
    nuove = []
    for v in voci:
        q = re.sub(r"\[\[Voce \d+.*?\]\]", lambda _m: escape(str(v)).replace("\\", "\\\\"), proto, count=1, flags=re.S)
        if q == proto:           # segnaposto spezzato: ripiego sul metodo generale
            q = sostituisci_par(proto, {"Voce 1 - descrizione lavorazione - importo": v})
        nuove.append(q)
    primo, ultimo = idx[0].start(), idx[-1].end()
    return xml[:primo] + "".join(nuove) + xml[ultimo:]


def compila(modello, dati, uscita):
    with zipfile.ZipFile(modello) as zin:
        xml = zin.read("word/document.xml").decode("utf-8")
        xml = prepara_voci(xml, dati.get("VOCI") or [])
        xml = RE_P.sub(lambda m: sostituisci_par(m.group(0), dati), xml)
        with zipfile.ZipFile(uscita, "w", zipfile.ZIP_DEFLATED) as zout:
            for it in zin.infolist():
                data = zin.read(it.filename)
                if it.filename == "word/document.xml":
                    data = xml.encode("utf-8")
                zout.writestr(it, data)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    dati = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    modello = Path(sys.argv[3]) if len(sys.argv) > 3 else MODELLO
    compila(modello, dati, sys.argv[2])
    print("scritto", sys.argv[2])


if __name__ == "__main__":
    main()
