# -*- coding: utf-8 -*-
"""
verifica_preventivo.py - controllo AUTOMATICO del generatore di preventivi (scritto dall'Ufficio, non dall'agente).
Uso (dalla cartella del progetto):  python strumenti/verifica_preventivo.py [strumenti/genera_preventivo.py]
Lancia il generatore con strumenti/dati_esempio.json, scrive strumenti/out/PROVA_preventivo.docx e controlla che:
 1 il generatore parta e scriva il file; il file sia uno zip valido con gli STESSI file del modello;
 2 logo (word/media), intestazioni, piè di pagina, stili, numerazione, impostazioni siano IDENTICI byte per byte al modello;
 3 word/document.xml sia XML valido e non resti nessun segnaposto [[...]] ne' il suggerimento del protocollo;
 4 ogni segnaposto del modello abbia il suo valore in dati_esempio.json (chiave = testo prima del " — "; per le voci la chiave VOCI) e ogni valore compaia nel testo;
 5 la formattazione dei paragrafi (le "runs") sia rimasta uguale ai paragrafi del modello (esclusi i punti elenco delle voci);
 6 se c'e' LibreOffice: il PDF del modello e quello della prova abbiano lo stesso numero di immagini (il logo).
Esce con codice 0 solo se tutto e' OK. NON puo' vedere l'aspetto: quello lo guarda Leo aprendo il .docx in Word e in LibreOffice.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RADICE = Path(__file__).resolve().parent.parent
MODELLO = RADICE / "Preventivo Automatico" / "MOD_PREVENTIVO_v4_1.docx"
DATI = RADICE / "strumenti" / "dati_esempio.json"
USCITA = RADICE / "strumenti" / "out" / "PROVA_preventivo.docx"
errori, ok = [], []


def esito(nome, cond, dettaglio=""):
    (ok if cond else errori).append(nome + (": " + dettaglio if dettaglio and not cond else ""))
    print(("OK      " if cond else "ERRORE  ") + nome + ("  -> " + dettaglio if dettaglio and not cond else ""))


def chiave(t):
    return t.split(" — ")[0].strip()


def par_testi(root):
    return ["".join(e.text or "" for e in p.iter(W + "t")) for p in root.iter(W + "p")]


def firma_par(p):
    """Firma della formattazione di un paragrafo: proprieta' del paragrafo e di ogni run."""
    pr = p.find(W + "pPr")
    out = [ET.tostring(pr) if pr is not None else b""]
    for r in p.findall(W + "r"):
        rp = r.find(W + "rPr")
        out.append(ET.tostring(rp) if rp is not None else b"")
    return out


def conta_immagini_pdf(pdf):
    d = Path(pdf).read_bytes()
    return len(re.findall(rb"/Subtype\s*/Image", d))


def main():
    gen = Path(sys.argv[1]) if len(sys.argv) > 1 else RADICE / "strumenti" / "genera_preventivo.py"
    if not MODELLO.is_file():
        sys.exit(f"modello mancante: {MODELLO}")
    USCITA.parent.mkdir(parents=True, exist_ok=True)
    USCITA.unlink(missing_ok=True)
    try:
        r = subprocess.run([sys.executable, str(gen), str(DATI), str(USCITA)], capture_output=True, text=True, timeout=300, cwd=str(RADICE))
    except Exception as e:
        sys.exit(f"ERRORE: impossibile lanciare {gen}: {e}")
    esito("1a il generatore parte (exit 0) e scrive il file", r.returncode == 0 and USCITA.is_file(), (r.stderr or r.stdout)[-400:])
    if not USCITA.is_file():
        sys.exit(1)
    try:
        zo, zm = zipfile.ZipFile(USCITA), zipfile.ZipFile(MODELLO)
        assert zo.testzip() is None
    except Exception as e:
        esito("1b il file e' uno zip valido", False, str(e))
        sys.exit(1)
    esito("1b stessi file del modello dentro lo zip", sorted(zo.namelist()) == sorted(zm.namelist()),
          f"mancano {sorted(set(zm.namelist()) - set(zo.namelist()))}, in piu' {sorted(set(zo.namelist()) - set(zm.namelist()))}")
    diversi = [n for n in zm.namelist() if n in zo.namelist() and zm.read(n) != zo.read(n)]
    ammessi = {"word/document.xml"}
    esito("2 logo, intestazioni, piè di pagina, stili: identici al modello", set(diversi) <= ammessi, "cambiati: " + ", ".join(sorted(set(diversi) - ammessi)))
    media = [n for n in zm.namelist() if n.startswith("word/media/")]
    esito("2b ci sono immagini (logo) nel modello e nella prova", bool(media) and all(n in zo.namelist() for n in media), "nessuna immagine")

    try:
        xo = ET.fromstring(zo.read("word/document.xml"))
        xm = ET.fromstring(zm.read("word/document.xml"))
        esito("3a document.xml e' XML valido", True)
    except ET.ParseError as e:
        esito("3a document.xml e' XML valido", False, str(e))
        sys.exit(1)
    to, tm = par_testi(xo), par_testi(xm)
    testo_o = "\n".join(to)
    esito("3b nessun segnaposto [[ ]] rimasto", "[[" not in testo_o and "]]" not in testo_o)
    esito("3c il suggerimento del protocollo non c'e' piu'", "iniziale nome" not in testo_o)

    try:
        dati = json.loads(DATI.read_text(encoding="utf-8"))
    except Exception as e:
        esito("4a dati_esempio.json leggibile", False, str(e))
        sys.exit(1)
    seg = []
    for t in tm:
        seg += re.findall(r"\[\[(.+?)\]\]", t)
    chiavi = sorted({chiave(s) for s in seg if not s.startswith("Voce ")})
    mancano = [k for k in chiavi if k not in dati or not str(dati[k]).strip()]
    esito("4a dati_esempio.json ha un valore per ogni segnaposto", not mancano, "mancano: " + "; ".join(mancano))
    esito("4b VOCI e' una lista con almeno 4 righe (prova di piu' voci del modello)", isinstance(dati.get("VOCI"), list) and len(dati["VOCI"]) >= 4)
    valori = [str(dati[k]) for k in chiavi if k in dati] + [str(v) for v in (dati.get("VOCI") or [])]
    assenti = [v[:40] for v in valori if v.strip() and v not in testo_o]
    esito("4c ogni valore dei dati compare nel documento", not assenti, "non trovati: " + "; ".join(assenti))

    po = [p for p in xo.iter(W + "p")]
    pm = [p for p in xm.iter(W + "p")]
    fo = [firma_par(p) for p, t in zip(po, to) if not t.startswith("•")]
    fm = [firma_par(p) for p, t in zip(pm, tm) if not t.startswith("•") and "[[Voce" not in t]
    esito("5 formattazione dei paragrafi uguale al modello (esclusi i punti elenco)", fo == fm, f"{len(fo)} paragrafi nella prova, {len(fm)} nel modello")

    so = shutil.which("soffice") or shutil.which("libreoffice")
    if so:
        try:
            with tempfile.TemporaryDirectory() as td:
                for src, nome in ((MODELLO, "modello"), (USCITA, "prova")):
                    d = Path(td) / nome
                    d.mkdir()
                    shutil.copy(src, d / "x.docx")
                    subprocess.run([so, "--headless", "--convert-to", "pdf", "--outdir", str(d), str(d / "x.docx")], capture_output=True, timeout=180)
                a, b = Path(td, "modello", "x.pdf"), Path(td, "prova", "x.pdf")
                if a.is_file() and b.is_file():
                    esito("6 LibreOffice: stesso numero di immagini (logo) nel PDF", conta_immagini_pdf(a) == conta_immagini_pdf(b), f"{conta_immagini_pdf(a)} contro {conta_immagini_pdf(b)}")
                else:
                    print("AVVISO  LibreOffice non ha prodotto il PDF: controllo 6 saltato")
        except Exception as e:
            print(f"AVVISO  controllo LibreOffice saltato: {e}")
    else:
        print("AVVISO  LibreOffice non trovato: controllo 6 (PDF) saltato; apri tu il .docx in Word/LibreOffice")
    print(f"\n{len(ok)} controlli OK, {len(errori)} ERRORI. File di prova: {USCITA}")
    sys.exit(1 if errori else 0)


if __name__ == "__main__":
    main()
