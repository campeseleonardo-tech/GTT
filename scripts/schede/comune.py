"""Funzioni e costanti comuni delle schede dei risultati (percorsi, lettura dei JSON, formati dei numeri, forma base delle schede)."""
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import json
import re



RADICE = Path(__file__).resolve().parent.parent.parent


PROC = RADICE / "data" / "processed"


DOCS = RADICE / "docs"


OUT_JS = RADICE / "data" / "schede_risultati.js"




def leggi(nome):
    return json.loads((PROC / nome).read_text(encoding="utf-8"))




def num(label, dopo, unita, prima=None):
    return {"label": label, "prima": prima, "dopo": dopo, "unita": unita}




def voce(label, valore, prima=None, tono=None, link=None):
    v = {"label": label, "valore": valore}
    if link is not None:   # la barra e' un link (es. alla linea nella mappa)
        v["link"] = link
    if prima is not None:
        v["prima"] = prima
    if tono is not None:   # "verde"/"rosso" = bene/male; senza tono = blu neutro (quantità)
        v["tono"] = tono
    return v




def migliaia(n):
    return f"{n:,}".replace(",", ".")




def virgola(x):
    testo = f"{x:.1f}".replace(".", ",")
    return testo[:-2] if testo.endswith(",0") else testo




def pct2(x):
    """percentuale con due decimali e virgola (per valori piccoli, es. 'oltre 10 minuti')."""
    return f"{x:.2f}".replace(".", ",")




def link_linea(nome):
    """Link dalla scheda alla mappa con quella linea selezionata (tema «Puntualita' delle linee»)."""
    return "mappa_torino.html#tema=puntualita&linea=" + quote(str(nome), safe="") + "&ora=8"   # si apre alle 8 di un feriale




def il(x):
    """articolo davanti a una percentuale: 'il 4,2%', ma 'l'8,3%' e 'l'11%'."""
    testo = virgola(x)
    return ("l'" if testo[0] == "8" or testo.split(",")[0] in ("11", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89") else "il ") + testo




def ora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")




def minuti(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)




def nome_pulito(n):
    """'RIVALTA DI TORINO' -> 'Rivalta di Torino', 'PORTA SUSA FS' -> 'Porta Susa FS'; gli altri nomi restano uguali."""
    if not n.isupper():
        return n
    return n.title().replace(" Di ", " di ").replace(" Fs", " FS")




def date_it(iso_list):
    """['2026-10-15', '2026-10-16'] -> '15/10 e 16/10'"""
    giorni = [d[8:10] + "/" + d[5:7] for d in iso_list]
    if not giorni:
        return "—"
    return giorni[0] if len(giorni) == 1 else ", ".join(giorni[:-1]) + " e " + giorni[-1]




NASCOSTE = {"risultato2"}   # in pausa: docs/R2_metro_notte.md




# ---------------------------------------------------------------- Forma nuova delle schede
# Ogni scheda ha un campo "forma" con tutto quello che la pagina mostra: etichetta, titolo-risposta, domanda in una riga,
# numero grande, grafico principale, 3 punti chiave, e le parti chiuse (altri grafici, calcolo, limiti, inglese).
# I campi vecchi restano nel JSON ma la pagina non li usa. I numeri vengono sempre dai file dei risultati.

PAROLE_VIETATE = re.compile(r"\bLeo\b|\bgiro\b|\bfase\b|\bversione\b|\.py\b|\.json\b|\.md\b|\bIMQ\b|\bQ00\d|\b5T\b|\bGTFS\b", re.I)




def controlla_forma(nome, f):
    """Avvisi sui testi della forma: frasi di oltre 20 parole e parole che non vanno nelle pagine."""
    testi = [f["titolo"], f["domanda"], f["numero"]["testo"], *f["punti"], *f["calcolo"], *f.get("confronto", []),
             *f["limiti"], *f["english"], *(a for a in [f.get("extra", {}).get("punto")] if a)]
    for t in testi:
        if PAROLE_VIETATE.search(t):
            print(f"  ATTENZIONE {nome}: parola da togliere in «{t[:60]}»")
        for frase in re.split(r"(?<=[a-zA-ZàèéìòùÀ%)\]»])[.;:] +(?=[A-ZÈÀ])", t):
            if len(frase.split()) > 20:
                print(f"  ATTENZIONE {nome}: frase di {len(frase.split())} parole: «{frase[:70]}…»")
    if len(f["punti"]) != 3 or len(f["limiti"]) > 4 or len(f["altri"]) > 2 or len(f["english"]) != 3 or len(f["calcolo"]) > 5:
        print(f"  ATTENZIONE {nome}: numero di righe fuori misura")




def forma_base(s, titolo, domanda, numero, principale, punti, altri, calcolo, criteri, limiti, english, mappa=True, **extra):
    f = {"etichetta": s["tag"], "titolo": titolo, "domanda": domanda, "numero": numero, "principale": principale,
         "punti": punti, "altri": altri, "calcolo": calcolo, "criteri": criteri, "limiti": limiti, "english": english}
    if mappa and s.get("mappa"):
        f["mappa"] = {"id": s["mappa"]["id"], "nota": s["mappa"]["nota"]}
        if s["mappa"].get("vista"):   # es. #tema=vulnerabilita&vista=doppio
            f["mappa"]["vista"] = s["mappa"]["vista"]
    f.update(extra)
    return f




def grafico_per_titolo(s, inizio):
    return next(g for g in s["grafici"] if g["titolo"].startswith(inizio))




def numero_di(s, label_inizio, scenario=0):
    return next(n for n in s["scenari"][scenario]["numeri"] if n["label"].startswith(label_inizio))["dopo"]




def forbice_estremi(x, y):
    """Estremi della forbice per il titolo: interi se differiscono di almeno 0,5, altrimenti con un decimale."""
    if abs(y - x) >= 0.5:
        return str(round(x)), str(round(y))
    return virgola(round(x, 1)), virgola(round(y, 1))
