#!/usr/bin/env python3
"""Rapporto di sostenibilita' GTT 2025 - passo 2: estrazione dei fatti con il modello.

Legge data/processed/rapporto_gtt/pagine.json (prodotto dallo script 30), raggruppa le
pagine in blocchi da 4 con 1 pagina di sovrapposizione (le tabelle spesso passano la
pagina) e chiede al modello DeepSeek di estrarre i dati utili al progetto come JSON.

Per OGNI blocco:
- chiama il modello (PROMPT DI ESTRAZIONE come messaggio di sistema);
- salva subito il risultato in data/processed/rapporto_gtt/cache/blocco_NNNN.json, cosi'
  se lo script si ferma riparte da dove era (i blocchi gia' fatti non si richiamano);
- controllo LOCALE (0 token): il campo "valore" deve comparire nel testo del blocco in
  forma normalizzata (numeri italiani: 183.675.867 / 5.665 / 15,1 / 4,2%); deve anche
  essere una pagina del blocco. I fatti che non passano vengono scartati e contati.

Alla fine unisce i doppioni (stesso tema+dato+valore+anno), ordina per tema e scrive
data/processed/rapporto_gtt/fatti.json.

Uso:
  python scripts/31_rapporto_fatti.py                # giro completo
  python scripts/31_rapporto_fatti.py --pagine 29-32 # solo quelle pagine PDF (pilota)
  python scripts/31_rapporto_fatti.py --casuali 10   # 10 pagine a caso

La chiave API si legge da chiave_deepseek.txt nella radice (una riga). Non finisce mai
nei log, nei JSON o nel codice.
"""
import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
PAGINE_JSON = RADICE / "data/processed/rapporto_gtt/pagine.json"
DEST_DIR = RADICE / "data/processed/rapporto_gtt"
CACHE_DIR = DEST_DIR / "cache"
FATTI_JSON = DEST_DIR / "fatti.json"
CHIAVE_FILE = RADICE / "chiave_deepseek.txt"

URL_API = "https://api.deepseek.com/chat/completions"
MODELLI = ["deepseek-flash", "deepseek-v4-flash"]  # il secondo e' il vecchio nome, ancora accettato
TEMPERATURA = 0
TIMEOUT_S = 120
TENTATIVI = 3
PAUSA_BASE_S = 5          # pausa crescente tra i tentativi: 5 s, 10 s, 15 s

DIM_BLOCCO = 4
SOVRAPPOSIZIONE = 1

# Tetti di sicurezza: lo script si ferma con un messaggio chiaro se li supera.
LIMITE_CHIAMATE = 80
LIMITE_TOKEN_TOTALI = 600000
MAX_TOKENS_USCITA = 12000

TEMA_ORDINE = ["spostamenti", "offerta", "qualita", "ambiente", "parcheggi",
               "economia", "accessibilita_sicurezza", "progetti"]

# Valori che il PILOTA (pagine PDF 29-32) DEVE far comparire. Servono a fermarsi in
# fretta se l'estrazione sbaglia. Formato: (valore, anno_o_None, descrizione).
ATTESI_PILOTA = [
    ("183.675.867", "2025", "passeggeri bus urbano 2025"),
    ("173.127.186", "2024", "passeggeri bus urbano 2024"),
    ("174.328.209", "2023", "passeggeri bus urbano 2023"),
    ("15.761.419", "2025", "passeggeri bus extraurbano 2025"),
    ("14.854.857", "2024", "passeggeri bus extraurbano 2024"),
    ("14.256.387", "2023", "passeggeri bus extraurbano 2023"),
    ("52.681.447", "2025", "passeggeri tram 2025"),
    ("53.482.515", "2024", "passeggeri tram 2024"),
    ("48.240.408", "2023", "passeggeri tram 2023"),
    ("48.250.804", "2025", "passeggeri metro 2025"),
    ("44.925.515", "2024", "passeggeri metro 2024"),
    ("36.503.720", "2023", "passeggeri metro 2023"),
    ("5.665", None, "area servita km2"),
    ("187", None, "tram: km di binari"),
    ("8", None, "tram: numero di linee"),
    ("180", None, "tram: numero mezzi"),
    ("23", None, "metro: fermate"),
    ("15,1", None, "metro: km tracciato"),
    ("58", None, "metro: convogli"),
    ("30", None, "parcheggi gestiti da GTT"),
]


def verifica_attesi(fatti):
    """Controlla che i valori attesi del pilota siano nei fatti. Ritorna (esiti, mancanti)."""
    solo_valore = {normalizza_numero(str(f.get("valore", ""))) for f in fatti}
    con_anno = {(normalizza_numero(str(f.get("valore", ""))), str(f.get("anno", "")).strip())
                for f in fatti}
    esiti, mancanti = [], []
    for valore, anno, desc in ATTESI_PILOTA:
        n = normalizza_numero(valore)
        trovato = (n in solo_valore) if anno is None else ((n, anno) in con_anno)
        esiti.append((trovato, desc, valore, anno))
        if not trovato:
            mancanti.append(f"{desc} = {valore}" + (f" (anno {anno})" if anno else ""))
    return esiti, mancanti

PROMPT_ESTRAZIONE = """Sei un assistente che estrae dati da un rapporto di sostenibilita' dell'azienda di trasporto pubblico GTT (Torino), anno 2025. Ti do un blocco di pagine in italiano, ogni pagina e' marcata "=== PAGINA PDF n / STAMPATA m ===".

CONTESTO. Servono i dati per un progetto personale di analisi della mobilita' di Torino e cintura (circa 18 km): mappa interattiva, scenari "cosa succede se" sull'accessibilita' al trasporto pubblico, stima del traffico auto, parcheggi di interscambio, taratura di dati simulati con dati reali. In particolare interessa: come si spostano le persone, quanti veicoli in meno potrebbero circolare, dove e quanto e' usato il servizio.

COSA CERCARE (in ordine di utilita'):
1. spostamenti: passeggeri trasportati per mezzo (bus urbano, bus extraurbano, tram, metro, altro) e per anno; ripartizione modale; passeggeri-km; indagini sulla mobilita'; usi per fascia oraria, giorno, area;
2. offerta: km di rete e di binari, numero di linee, fermate, flotta (numero, tipo, alimentazione, eta'), vetture-km, corse, area servita, frequenze;
3. qualita': puntualita', regolarita', affollamento/capienza, soddisfazione clienti, reclami;
4. auto e ambiente: emissioni, auto evitate o CO2 risparmiata, quota mezzi elettrici/ibridi, piani di transizione;
5. parcheggi e sosta: posti, parcheggi di interscambio/Park & Ride, ricavi della sosta, ZTL;
6. economia: ricavi da biglietti e abbonamenti, costi, contributi, tariffe, numero abbonati;
7. accessibilita' e sicurezza: mezzi accessibili, incidenti, aggressioni, vandalismi;
8. progetti: prolungamenti metro, nuove linee, investimenti con importi e date.

REGOLE (tutte obbligatorie):
- Estrai SOLO cio' che e' scritto nel testo. Non dedurre, non calcolare, non arrotondare, non completare dalla tua conoscenza.
- Preferisci numeri e dati misurabili. Ignora frasi generiche, impegni, slogan, descrizioni senza numeri.
- Se una tabella ha piu' anni (2025, 2024, 2023), crea un fatto per ogni anno, con l'anno giusto: controlla con cura a quale colonna appartiene il numero. Se non sei sicuro dell'anno, non estrarre il dato.
- "valore" deve essere copiato identico dal testo, come scritto (es. "183.675.867", "15,1", "4,2%"). L'unita' sta nel campo "unita".
- "frase_originale" e' un pezzo letterale del testo, al massimo 15 parole, che contiene il valore.
- Ignora cio' che e' visibile solo come immagine o grafico: se non c'e' nel testo, non esiste.
- Se nel blocco non c'e' nulla di utile, restituisci {"fatti": []}.
- Rispondi SOLO con JSON valido, senza altro testo.

FORMATO:
{"fatti":[{"tema":"spostamenti|offerta|qualita|ambiente|parcheggi|economia|accessibilita_sicurezza|progetti","dato":"descrizione breve di cosa misura (es. 'Passeggeri trasportati - tram, area urbana')","valore":"...","unita":"...","anno":"2025","pagina_pdf":30,"pagina_stampata":28,"frase_originale":"...","utilita":"alta|media"}]}

"utilita" = alta se serve direttamente a: passeggeri per mezzo, ripartizione modale, rete/flotta/offerta, qualita' misurata, auto evitate/emissioni, parcheggi/Park&Ride; media per tutto il resto."""


# ---------------------------------------------------------------- numeri ------

def normalizza_numero(s):
    """Forma canonica di un numero scritto all'italiana.

    '183.675.867' -> '183675867' · '5.665' -> '5665' · '15,1' -> '15.1' · '4,2%' -> '4.2'
    """
    t = re.sub(r"[^\d.,]", "", s or "")
    if not t:
        return ""
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
        return t.rstrip("0").rstrip(".") if "." in t else t
    parti = t.split(".")
    if len(parti) > 1 and all(len(p) == 3 for p in parti[1:]):
        return "".join(parti)          # punti = separatori delle migliaia
    if "." in t:
        return t.rstrip("0").rstrip(".") or "0"
    return t


def numeri_nel_testo(testo):
    return {normalizza_numero(x) for x in re.findall(r"\d[\d.,]*", testo or "")}


# ------------------------------------------------------------------- API ------

def leggi_chiave():
    if not CHIAVE_FILE.exists():
        raise SystemExit(
            "ERRORE: manca il file chiave_deepseek.txt nella radice del progetto.\n"
            "Crealo con dentro una sola riga: la tua chiave API DeepSeek.\n"
            "Poi rilancia questo script."
        )
    chiave = CHIAVE_FILE.read_text(encoding="utf-8").strip().splitlines()
    chiave = chiave[0].strip() if chiave else ""
    if not chiave:
        raise SystemExit("ERRORE: chiave_deepseek.txt esiste ma e' vuoto.")
    return chiave


def _posta(corpo, chiave):
    dati = json.dumps(corpo).encode("utf-8")
    req = urllib.request.Request(
        URL_API, data=dati, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {chiave}",
                 "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
        return json.loads(r.read().decode("utf-8"))


def chiama_api(system, user, chiave):
    """Una chiamata al modello. Prova i nomi dei modelli in ordine e ritenta con pausa
    crescente su errori temporanei. Ritorna (dati_json, usage, modello_usato)."""
    ultimo_errore = None
    for modello in MODELLI:
        corpo = {
            "model": modello,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": TEMPERATURA,
            "response_format": {"type": "json_object"},
            "thinking": {"type": "disabled"},
            "max_tokens": MAX_TOKENS_USCITA,
            "stream": False,
        }
        tentativo = 0
        while tentativo < TENTATIVI:
            tentativo += 1
            try:
                risposta = _posta(corpo, chiave)
                testo = (risposta.get("choices") or [{}])[0].get("message", {}).get("content") or ""
                usage = risposta.get("usage") or {}
                if not testo.strip():
                    raise ValueError("risposta vuota dal modello")
                return json.loads(testo), usage, modello
            except urllib.error.HTTPError as e:
                dettaglio = e.read().decode("utf-8", "replace")
                ultimo_errore = f"HTTP {e.code}: {dettaglio[:400]}"
                basso = dettaglio.lower()
                if e.code in (400, 404) and "model" in basso and "thinking" not in basso:
                    print(f"  ! modello '{modello}' non accettato, provo il prossimo.")
                    break  # passa al modello successivo, senza ritentare questo
                if e.code == 400 and "thinking" in basso and "thinking" in corpo:
                    print("  ! il parametro 'thinking' e' stato rifiutato: riprovo senza.")
                    corpo.pop("thinking", None)
                    continue
            except (urllib.error.URLError, TimeoutError, OSError, ValueError,
                    json.JSONDecodeError) as e:
                ultimo_errore = f"{type(e).__name__}: {e}"
            if tentativo < TENTATIVI:
                pausa = PAUSA_BASE_S * tentativo
                print(f"  ! tentativo {tentativo} fallito ({ultimo_errore}); riprovo tra {pausa} s")
                time.sleep(pausa)
    raise RuntimeError(f"chiamata al modello non riuscita dopo {TENTATIVI} tentativi "
                       f"per ogni modello. Ultimo errore: {ultimo_errore}")


# --------------------------------------------------------------- blocchi ------

def costruisci_blocchi(pagine):
    """Blocchi da DIM_BLOCCO pagine con SOVRAPPOSIZIONE pagine condivise."""
    passo = DIM_BLOCCO - SOVRAPPOSIZIONE
    blocchi = []
    i = 0
    n = len(pagine)
    while i < n:
        blocchi.append(pagine[i:i + DIM_BLOCCO])
        if i + DIM_BLOCCO >= n:
            break
        i += passo
    return blocchi


def testo_blocco(blocco):
    pezzi = []
    for p in blocco:
        pezzi.append(f"=== PAGINA PDF {p['pagina_pdf']} / STAMPATA {p['pagina_stampata']} ===")
        pezzi.append(p["testo"])
    return "\n\n".join(pezzi)


def parse_intervallo(spec):
    """'29-32' oppure '29,30,31' -> set di interi."""
    pagine = set()
    for parte in spec.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            a, b = parte.split("-", 1)
            pagine.update(range(int(a), int(b) + 1))
        else:
            pagine.add(int(parte))
    return pagine


# ------------------------------------------------------- controllo locale ------

def valida_fatti(fatti, blocco):
    """Tiene solo i fatti il cui 'valore' compare davvero nel testo del blocco."""
    pagine_del_blocco = {p["pagina_pdf"] for p in blocco}
    numeri = numeri_nel_testo(testo_blocco(blocco))
    validi, scartati = [], []
    for f in fatti:
        motivo = None
        valore = str(f.get("valore", ""))
        norm = normalizza_numero(valore)
        if not norm:
            motivo = "valore vuoto o senza cifre"
        elif norm not in numeri:
            motivo = f"valore '{valore}' non trovato nel testo del blocco"
        else:
            try:
                pdf_n = int(f.get("pagina_pdf"))
            except (TypeError, ValueError):
                pdf_n = None
            if pdf_n not in pagine_del_blocco:
                motivo = f"pagina_pdf {f.get('pagina_pdf')} non e' nel blocco"
        if motivo:
            scartati.append({"motivo": motivo, "fatto": f})
        else:
            validi.append(f)
    return validi, scartati


# ------------------------------------------------------------------ main ------

def nome_cache(blocco):
    """Nome del file di cache basato sulle pagine del blocco (non sull'indice), cosi'
    il pilota e il giro completo non si scambiano i risultati."""
    da = blocco[0]["pagina_pdf"]
    a = blocco[-1]["pagina_pdf"]
    return CACHE_DIR / f"blocco_{da:04d}_{a:04d}.json"


def carica_cache(blocco):
    f = nome_cache(blocco)
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    return None


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="Estrae i fatti dal rapporto GTT con DeepSeek.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--pagine", help="solo queste pagine PDF, es. 29-32 (pilota)")
    g.add_argument("--casuali", type=int, help="N pagine PDF scelte a caso")
    ap.add_argument("--verifica-attesi", action="store_true",
                    help="controlla i valori che il pilota (pag 29-32) deve far comparire")
    args = ap.parse_args()

    if not PAGINE_JSON.exists():
        raise SystemExit(f"ERRORE: manca {PAGINE_JSON}. Lancia prima lo script 30.")
    pagine = json.loads(PAGINE_JSON.read_text(encoding="utf-8"))
    if not pagine:
        raise SystemExit("ERRORE: pagine.json e' vuoto.")
    per_pdf = {p["pagina_pdf"]: p for p in pagine}

    if args.pagine:
        richieste = parse_intervallo(args.pagine)
        mancanti = sorted(richieste - set(per_pdf))
        if mancanti:
            print(f"Nota: pagine richieste assenti/scartate: {mancanti}")
        selezione = [per_pdf[n] for n in sorted(richieste & set(per_pdf))]
        nome_run = f"pagine {args.pagine}"
    elif args.casuali:
        n = min(args.casuali, len(pagine))
        selezione = sorted(random.sample(pagine, n), key=lambda p: p["pagina_pdf"])
        nome_run = f"{n} pagine a caso"
    else:
        selezione = pagine
        nome_run = "giro completo"

    if not selezione:
        raise SystemExit("ERRORE: nessuna pagina da elaborare.")

    blocchi = costruisci_blocchi(selezione)
    chiave = leggi_chiave()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Run: {nome_run} - {len(selezione)} pagine in {len(blocchi)} blocchi "
          f"(max {LIMITE_CHIAMATE} chiamate, max {LIMITE_TOKEN_TOTALI} token).")

    chiamate = 0
    token_prompt = token_completion = 0
    tutti_fatti = []
    tutti_scartati = []
    da_modello = 0

    for indice, blocco in enumerate(blocchi, start=1):
        salvato = carica_cache(blocco)
        if salvato is not None:
            print(f"[blocco {indice}/{len(blocchi)}] gia' in cache "
                  f"(pag {blocco[0]['pagina_pdf']}-{blocco[-1]['pagina_pdf']}, "
                  f"{len(salvato.get('fatti', []))} fatti, {len(salvato.get('scartati', []))} scartati).")
            tutti_fatti.extend(salvato.get("fatti", []))
            tutti_scartati.extend(salvato.get("scartati", []))
            token_prompt += salvato.get("usage", {}).get("prompt_tokens", 0)
            token_completion += salvato.get("usage", {}).get("completion_tokens", 0)
            continue

        if chiamate >= LIMITE_CHIAMATE:
            print(f"STOP: raggiunto il tetto di {LIMITE_CHIAMATE} chiamate.")
            break
        if token_prompt + token_completion >= LIMITE_TOKEN_TOTALI:
            print(f"STOP: raggiunto il tetto di {LIMITE_TOKEN_TOTALI} token.")
            break

        da_pdf = blocco[0]["pagina_pdf"]
        a_pdf = blocco[-1]["pagina_pdf"]
        print(f"[blocco {indice}/{len(blocchi)}] pag PDF {da_pdf}-{a_pdf}: chiamo il modello...")
        dati, usage, modello = chiama_api(PROMPT_ESTRAZIONE, testo_blocco(blocco), chiave)
        chiamate += 1
        da_modello += 1
        token_prompt += usage.get("prompt_tokens", 0)
        token_completion += usage.get("completion_tokens", 0)

        fatti = dati.get("fatti", []) if isinstance(dati, dict) else []
        if not isinstance(fatti, list):
            fatti = []
        validi, scartati = valida_fatti(fatti, blocco)
        print(f"  modello '{modello}': {len(fatti)} fatti, tenuti {len(validi)}, scartati {len(scartati)}")

        nome_cache(blocco).write_text(json.dumps({
            "blocco": indice,
            "da_pdf": da_pdf,
            "a_pdf": a_pdf,
            "pagine_pdf": [p["pagina_pdf"] for p in blocco],
            "modello": modello,
            "usage": usage,
            "fatti": validi,
            "scartati": scartati,
        }, ensure_ascii=False, indent=1), encoding="utf-8")

        tutti_fatti.extend(validi)
        tutti_scartati.extend(scartati)

    # unisci i doppioni (stesso tema+dato+valore+anno), ordina per tema
    unici = {}
    for f in tutti_fatti:
        chiave_f = (str(f.get("tema", "")).strip().lower(),
                    str(f.get("dato", "")).strip().lower(),
                    normalizza_numero(str(f.get("valore", ""))),
                    str(f.get("anno", "")).strip())
        if chiave_f not in unici:
            unici[chiave_f] = f
        elif str(f.get("utilita", "")).lower() == "alta":
            unici[chiave_f]["utilita"] = "alta"   # se un doppione e' "alta", vince

    def ordine_tema(f):
        t = str(f.get("tema", "")).strip().lower()
        return (TEMA_ORDINE.index(t) if t in TEMA_ORDINE else len(TEMA_ORDINE), t)

    fatti_finali = sorted(unici.values(), key=lambda f: (ordine_tema(f), str(f.get("dato", "")).lower()))

    esito = {
        "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pdf": "data/rapporto_di_sostenibilita_2025.pdf",
        "run": nome_run,
        "pagine": len(selezione),
        "blocchi": len(blocchi),
        "blocchi_chiamati": da_modello,
        "chiamate_api": chiamate,
        "token": {"prompt": token_prompt, "completion": token_completion,
                  "totali": token_prompt + token_completion},
        "fatti": fatti_finali,
        "fatti_scartati": len(tutti_scartati),
    }
    FATTI_JSON.write_text(json.dumps(esito, ensure_ascii=False, indent=1), encoding="utf-8")

    print("-" * 70)
    print(f"Fatti verificati (unici): {len(fatti_finali)}")
    print(f"Fatti scartati dal controllo locale: {len(tutti_scartati)}")
    print(f"Chiamate fatte in questa run: {chiamate}")
    print(f"Token: prompt {token_prompt}, completion {token_completion}, "
          f"totali {token_prompt + token_completion}")
    print(f"Scritto {FATTI_JSON}")

    if tutti_scartati:
        print("Esempi di fatti scartati (gli ultimi 5):")
        for s in tutti_scartati[-5:]:
            print(f"  - {s['motivo']} -> {s['fatto'].get('dato')} = {s['fatto'].get('valore')}")

    if args.verifica_attesi:
        print("=" * 70)
        print("VERIFICA ATTESI DEL PILOTA")
        esiti, mancanti = verifica_attesi(fatti_finali)
        for trovato, desc, valore, anno in esiti:
            print(f"  [{'OK ' if trovato else 'NO '}] {desc}: {valore}"
                  + (f" (anno {anno})" if anno else ""))
        if mancanti:
            print(f"PILOTA FALLITO: mancano {len(mancanti)} valori:")
            for m_ in mancanti:
                print(f"  - {m_}")
        else:
            print("PILOTA SUPERATO: tutti i valori attesi sono presenti con anno e pagina.")


if __name__ == "__main__":
    main()
