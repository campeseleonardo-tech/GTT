#!/usr/bin/env python3
"""Rapporto di sostenibilita' GTT 2025 - passo 1: estrazione locale del testo (0 token).

Legge una COPIA del PDF (l'originale in data/ non si tocca mai), estrae il testo
pagina per pagina con pypdf e scrive data/processed/rapporto_gtt/pagine.json.

- Usa la modalita' "layout" di pypdf: rende le tabelle in colonne allineate, cosi'
  il modello vede meglio a quale anno (2025/2024/2023) appartiene un numero
  (confrontata con la modalita' normale su pagina PDF 30: la layout e' piu' chiara).
- Pagina stampata = numero scritto in fondo alla pagina. Se in fondo non c'e' un
  numero, si usa come ripiego (PDF - 2), scarto verificato su molte pagine.
- Scarta pagine quasi vuote (copertina, separatori, pagine di sole immagini):
  meno di MIN_CARATTERI caratteri dopo aver tolto spazi e a capo.

Output: data/processed/rapporto_gtt/pagine.json
  lista di {pagina_pdf, pagina_stampata, testo}
"""
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pypdf

RADICE = Path(__file__).resolve().parent.parent
PDF_ORIGINALE = RADICE / "data/rapporto_di_sostenibilita_2025.pdf"
DEST_DIR = RADICE / "data/processed/rapporto_gtt"
COPIA = DEST_DIR / "rapporto_gtt_2025.pdf"
OUT = DEST_DIR / "pagine.json"

SCARTO_RIPIEGO = 2          # pagina stampata = pagina PDF - 2 (verificato su molte pagine)
MIN_CARATTERI = 200         # sotto questa soglia la pagina e' quasi vuota -> scartata
PAGINA_CONTROLLO_PDF = 30   # pagina da mostrare a video per controllo (stampata 28)


def normalizza_spazi(t):
    return re.sub(r"\s+", " ", t).strip()


def estrai_testo(pagina):
    """Testo della pagina in modalita' layout; se non supportata, testo normale."""
    try:
        return pagina.extract_text(extraction_mode="layout")
    except TypeError:
        return pagina.extract_text()


def pagina_stampata_dal_testo(testo, pagina_pdf):
    """Numero scritto in fondo alla pagina; se manca, ripiego su PDF - 2."""
    righe = [r.strip() for r in testo.rstrip().splitlines() if r.strip()]
    if righe:
        ultima = righe[-1]
        m = re.fullmatch(r"\d{1,3}", ultima)
        if m:
            return int(ultima), True
    return pagina_pdf - SCARTO_RIPIEGO, False


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if not PDF_ORIGINALE.exists():
        raise SystemExit(f"ERRORE: PDF non trovato: {PDF_ORIGINALE}")

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Copia di lavoro: l'originale non si tocca mai.
    if not COPIA.exists() or COPIA.stat().st_size != PDF_ORIGINALE.stat().st_size:
        shutil.copy2(PDF_ORIGINALE, COPIA)
        print(f"Copiato il PDF in {COPIA}")
    else:
        print(f"Copia del PDF gia' presente e identica: {COPIA}")

    lettore = pypdf.PdfReader(str(COPIA))
    totale = len(lettore.pages)
    print(f"Pagine nel PDF: {totale}")

    pagine = []
    scartate = []
    senza_numero = 0
    scarto_diverso = []

    for i in range(totale):
        pdf_n = i + 1
        testo = estrai_testo(lettore.pages[i])
        stampata, dal_numero = pagina_stampata_dal_testo(testo, pdf_n)
        if not dal_numero:
            senza_numero += 1
        elif stampata != pdf_n - SCARTO_RIPIEGO:
            scarto_diverso.append((pdf_n, stampata))

        if len(normalizza_spazi(testo)) < MIN_CARATTERI:
            scartate.append(pdf_n)
            continue

        pagine.append({
            "pagina_pdf": pdf_n,
            "pagina_stampata": stampata,
            "testo": testo,
        })

    tenute = len(pagine)
    print(f"Pagine tenute: {tenute}")
    print(f"Pagine scartate (quasi vuote): {len(scartate)} -> {scartate}")
    print(f"Pagine senza numero stampato (usato il ripiego PDF-{SCARTO_RIPIEGO}): {senza_numero}")
    if scarto_diverso:
        print(f"ATTENZIONE: {len(scarto_diverso)} pagine con scarto diverso da {SCARTO_RIPIEGO}: "
              f"{scarto_diverso[:10]}")
    else:
        print(f"Scarto pagina stampata = pagina PDF - {SCARTO_RIPIEGO} confermato su tutte le pagine "
              f"che hanno un numero in fondo.")

    OUT.write_text(json.dumps(pagine, ensure_ascii=False), encoding="utf-8")
    print(f"Scritto {OUT} ({tenute} pagine)")

    # Controllo a video: testo della pagina PDF di riferimento.
    esempio = next((p for p in pagine if p["pagina_pdf"] == PAGINA_CONTROLLO_PDF), None)
    print("=" * 70)
    if esempio:
        print(f"CONTROLLO - testo pagina PDF {esempio['pagina_pdf']} "
              f"(stampata {esempio['pagina_stampata']}):")
        print(esempio["testo"])
    else:
        print(f"CONTROLLO: pagina PDF {PAGINA_CONTROLLO_PDF} non trovata tra quelle tenute.")
    print("=" * 70)


if __name__ == "__main__":
    main()
