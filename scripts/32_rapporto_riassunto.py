#!/usr/bin/env python3
"""Rapporto di sostenibilita' GTT 2025 - passo 3: il riassunto (una sola chiamata).

Legge i fatti gia' verificati (data/processed/rapporto_gtt/fatti.json) e chiede al
modello un riassunto MOLTO corto in italiano. Scrive
docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md.

Controllo locale (0 token): ogni numero che compare nel riassunto deve esistere in
fatti.json (valori, anni, pagine). Se un numero non c'e', rifa' la chiamata una volta;
se resta, lo segnala a Leo.

Nota tecnica: l'API e' chiamata con response_format json_object (come da regole), quindi
al modello si chiede di restituire {"riassunto": "<markdown>"}. Il markdown va nel file.
"""
import importlib.util
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FATTI_JSON = RADICE / "data/processed/rapporto_gtt/fatti.json"
RIASSUNTO_MD = RADICE / "docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md"
RIASSUNTO_MD.parent.mkdir(parents=True, exist_ok=True)

PROMPT_RIASSUNTO = """Ti do un elenco di fatti gia' verificati, estratti dal Rapporto di sostenibilita' GTT 2025, in JSON. Scrivi in italiano, semplice e senza gergo, un riassunto MOLTO corto per un progetto di analisi della mobilita' di Torino.

REGOLE:
- Usa SOLO numeri presenti nei fatti. Non aggiungere, non calcolare, non stimare, non arrotondare.
- Lunghezza: circa 350 parole in totale, piu' una tabella dei numeri chiave.
- Struttura: (1) 3-4 righe di sintesi: cosa dice il rapporto di utile per capire come si spostano le persone a Torino; (2) "Numeri chiave": tabella con colonne Dato | 2025 | 2024 | 2023 | Pag. stampata (pag. PDF), solo i dati piu' utili (passeggeri per mezzo, rete, flotta, qualita', ambiente, parcheggi); (3) "Altro che puo' servire" in 4-6 punti brevi; (4) "Limiti": 2-3 righe su cosa il rapporto non dice (per esempio dati per zona o per ora, affollamento) SOLO se i fatti mostrano che manca.
- Ogni numero ha la pagina di origine (stampata, e tra parentesi quella del PDF).
- Etichetta tutti i dati come [DICHIARATO GTT]: sono numeri dichiarati dall'azienda, non misurati da noi.
- Non scrivere frasi di promozione o valutazioni tue.

Rispondi SOLO con JSON valido, nella forma {"riassunto": "<il riassunto completo in markdown>"}."""

_mod31 = None


def carica_modulo31():
    """Carica lo script 31 per riusarne chiave, chiamata API e normalizzazione numeri."""
    percorso = Path(__file__).resolve().parent / "31_rapporto_fatti.py"
    spec = importlib.util.spec_from_file_location("rapporto_fatti", percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def num(s):
    return _mod31.normalizza_numero(s)


def numeri_da_fatti(fatti):
    """Tutti i numeri che il riassunto ha il diritto di usare."""
    consentiti = set()
    for f in fatti:
        for campo in ("valore", "anno", "pagina_stampata", "pagina_pdf", "unita"):
            consentiti.add(num(str(f.get(campo, ""))))
    consentiti.discard("")
    # numeri strutturali innocui: anni, ordinali piccoli, note tipo "circa 350 parole"
    consentiti |= {str(y) for y in range(2000, 2036)}
    consentiti |= {str(i) for i in range(0, 13)}
    consentiti |= {"350", "100", "50"}
    return consentiti


def numeri_nel_riassunto(md):
    return {num(x) for x in re.findall(r"\d[\d.,]*", md or "")} - {""}


def chiama(system, user, chiave):
    dati, usage, modello = _mod31.chiama_api(system, user, chiave)
    testo = ""
    if isinstance(dati, dict):
        testo = dati.get("riassunto") or dati.get("markdown") or dati.get("testo") or ""
        if not testo and len(dati) == 1:
            testo = str(next(iter(dati.values())))
    return testo, usage, modello


def pulisci_fences(t):
    t = (t or "").strip()
    m = re.match(r"^```[a-zA-Z]*\s*\n(.*)\n```\s*$", t, re.S)
    return m.group(1).strip() if m else t


def main():
    global _mod31
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if not FATTI_JSON.exists():
        raise SystemExit(f"ERRORE: manca {FATTI_JSON}. Lancia prima lo script 31 (o RAPPORTO_2_FATTI.bat).")
    esito = json.loads(FATTI_JSON.read_text(encoding="utf-8"))
    fatti = esito.get("fatti", []) if isinstance(esito, dict) else esito
    if not fatti:
        raise SystemExit("ERRORE: fatti.json non contiene fatti.")

    _mod31 = carica_modulo31()
    chiave = _mod31.leggi_chiave()
    consentiti = numeri_da_fatti(fatti)
    user = "Ecco i fatti in JSON:\n" + json.dumps(fatti, ensure_ascii=False, indent=1)

    md = ""
    modello = ""
    usage = {}
    mancanti = []
    for tentativo in (1, 2):
        print(f"Chiamata al modello per il riassunto (tentativo {tentativo})...")
        testo, usage, modello = chiama(PROMPT_RIASSUNTO, user, chiave)
        md = pulisci_fences(testo)
        mancanti = sorted(numeri_nel_riassunto(md) - consentiti)
        print(f"  modello '{modello}': {len(md)} caratteri, "
              f"numeri fuori dai fatti: {mancanti or 'nessuno'}")
        if not mancanti:
            break
        if tentativo == 1:
            print("  Rifaccio la chiamata una volta (numeri non presenti nei fatti).")
            time.sleep(3)

    if not md:
        raise SystemExit("ERRORE: il modello non ha restituito il riassunto.")

    intestazione = (
        "# Rapporto di sostenibilita' GTT 2025 - riassunto dei dati utili\n\n"
        f"_Generato il {datetime.now().strftime('%d/%m/%Y %H:%M')} da fatti verificati "
        f"({len(fatti)} fatti, modello {modello}). Tutti i numeri sono **[DICHIARATO GTT]**, "
        f"cioe' dichiarati dall'azienda, non misurati da noi._\n\n"
    )
    RIASSUNTO_MD.parent.mkdir(parents=True, exist_ok=True)
    RIASSUNTO_MD.write_text(intestazione + md + "\n", encoding="utf-8")
    print(f"Scritto {RIASSUNTO_MD}")

    tok_p = usage.get("prompt_tokens", 0)
    tok_c = usage.get("completion_tokens", 0)
    print(f"Token di questa chiamata: prompt {tok_p}, completion {tok_c}, totali {tok_p + tok_c}")
    if mancanti:
        print("ATTENZIONE PER LEO: nel riassunto restano numeri che NON sono nei fatti: "
              f"{mancanti}. Controlla a mano quelle righe.")
    else:
        print("Controllo numeri superato: tutti i numeri del riassunto esistono nei fatti.")


if __name__ == "__main__":
    main()
