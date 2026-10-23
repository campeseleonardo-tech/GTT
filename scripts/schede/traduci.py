"""Versione inglese delle schede: ricava la «forma» inglese da quella italiana con i testi di scripts/schede/testi.json.

L'italiano non si tocca: le schede restano scritte dai moduli r1, r4, r6, r8, r10. Qui ogni frase italiana viene cercata fra le frasi fisse
(«esatte») o fra i modelli con segnaposto («modelli») e sostituita con la versione inglese; i numeri passano al formato inglese
(1.234,5 -> 1,234.5). Un nome proprio (zona, linea, fermata) resta com'e'. Le frasi senza traduzione si elencano (e restano in italiano)."""
import json
import re
from pathlib import Path

FILE = Path(__file__).resolve().parent / "testi.json"
NUM = r"\d+(?:[.,]\d+)*"
TIPI = {"n": NUM, "p": r"[+\-−]?" + NUM, "s": r".+?", "t": r".+?", "w": r".+?", "a": r"(?:il |l')"}
PAROLE = [("minuti", "minutes"), ("nessuno", "none"), (" contro ", " versus "), (" e altre", " and others"), (" e ", " and ")]
CONNETTORI = {"di", "del", "della", "dei", "da", "d'", "de", "al", "e", "→", "-", "–", "+", "(", ")", "/", "Da", "Del", "Di"}


def numero_en(s):
    """'1.234,5' -> '1,234.5'; '0,4' -> '0.4'; '4.044' -> '4,044' (il punto italiano separa le migliaia)."""
    segno = ""
    if s and s[0] in "+-−":
        segno, s = s[0], s[1:]
    intero, _, dec = s.partition(",")
    intero = intero.replace(".", "")
    if len(intero) > 3:
        intero = f"{int(intero):,}"
    return segno + intero + ("." + dec if dec else "")


def _carica():
    d = json.loads(FILE.read_text(encoding="utf-8"))
    modelli = []
    for mod in d["modelli"]:
        rx, pos = "", 0
        for mt in re.finditer(r"\{([nspwta])(\d)\}", mod["it"]):
            rx += re.escape(mod["it"][pos:mt.start()]) + f"(?P<{mt.group(1)}{mt.group(2)}>{TIPI[mt.group(1)]})"
            pos = mt.end()
        rx += re.escape(mod["it"][pos:])
        letterali = len(re.sub(r"\{[nspwta]\d\}", "", mod["it"]))
        modelli.append((letterali, re.compile(rx), mod["en"]))
    modelli.sort(key=lambda x: -x[0])      # prima i modelli piu' specifici
    return d["esatte"], modelli


ESATTE, MODELLI = _carica()


def sembra_nome(t):
    """Nome proprio (zona, linea, fermata, intervallo di numeri): parole con la maiuscola, cifre, connettori e punteggiatura."""
    if not t.strip():
        return True
    for tok in re.split(r"[\s,]+", t):
        if not tok:
            continue
        if tok in CONNETTORI or re.fullmatch(r"[\d.,:+\-–/→×%()±€]+", tok) or re.fullmatch(r"[A-Z0-9À-Ý][^\s]*", tok):
            continue
        return False
    return True


def traduci(testo, mancanti=None):
    """Traduce una frase italiana; se non la conosce la lascia com'e' e la registra in mancanti."""
    if not isinstance(testo, str):
        return testo
    if testo in ESATTE:
        return ESATTE[testo]
    for _lett, rx, en in MODELLI:
        mt = rx.fullmatch(testo)
        if not mt:
            continue
        valori = {}
        for nome, v in mt.groupdict().items():
            tipo = nome[0]
            if tipo in "np":
                valori[nome] = numero_en(v)
            elif tipo == "t":
                valori[nome] = traduci(v, mancanti)
            elif tipo == "w":
                for it, ing in PAROLE:
                    v = v.replace(it, ing)
                valori[nome] = v
            elif tipo == "a":
                valori[nome] = ""
            else:
                valori[nome] = v
        return re.sub(r"\{([nspwta]\d)\}", lambda x: valori[x.group(1)], en)
    if re.fullmatch(r"[\d.,:\s\-–+]+", testo):     # solo cifre e punteggiatura (es. «1,5-2», «21–28»): i decimali passano al formato inglese
        return re.sub(NUM, lambda x: numero_en(x.group()) if re.search(r"[.,]", x.group()) else x.group(), testo)
    if sembra_nome(testo):
        return testo
    if mancanti is not None:
        mancanti.append(testo)
    return testo


ETICHETTE = {"STIMATO": "ESTIMATED", "MISURATO": "MEASURED", "PROGRAMMATO": "SCHEDULED", "CENSIMENTO": "CENSUS", "dati scarsi": "little data"}
SALTA = {"tipo", "tono", "link", "id", "vista", "xnome", "ynome", "mappa", "contorno"}


def _grafico_o_valore(o, mancanti):
    if isinstance(o, str):
        return traduci(o, mancanti)
    if isinstance(o, list):
        return [_grafico_o_valore(x, mancanti) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in SALTA else _grafico_o_valore(v, mancanti)) for k, v in o.items()}
    return o


def traduci_forma(f, mancanti=None):
    """La forma inglese di una scheda (stessa struttura di quella italiana, senza il vecchio riquadro «english»)."""
    out = {}
    for k, v in f.items():
        if k == "english":
            continue
        if k == "etichetta":
            e = v
            for it, ing in ETICHETTE.items():
                e = e.replace(it, ing)
            out[k] = e
        elif k == "principale" and isinstance(v, dict) and v.get("tipo") == "dispersione":
            g = dict(v)
            g["punti"] = v["punti"]          # i nomi delle zone restano com'e'
            out[k] = {kk: (vv if kk in SALTA or kk == "punti" else _grafico_o_valore(vv, mancanti)) for kk, vv in v.items()}
        elif k in SALTA:
            out[k] = v
        else:
            out[k] = _grafico_o_valore(v, mancanti)
    return out
