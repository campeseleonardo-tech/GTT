r"""
comune.py - regole condivise da TUTTI i runner e dal pannello (Multiple Agents).
Aggiunto dalla chat di controllo il 04/10/2026.

1) UN SOLO AGENTE ALLA VOLTA tra progetti diversi (candidature + generico/Langue + futuri).
2) LIMITE DI CLAUDE condiviso: se un runner prende il limite, si fermano tutti fino all'orario di reset
   letto dal messaggio di Claude ("resets 5am"), poi ripartono da soli. Niente piu' STOP automatici.
3) CONTATORE D'USO stimato: token pesati delle ultime 5 ore (costo di listino convertito in token
   di input Sonnet: 1 M token pesati ~ 3 USD). 100% = 1.000.000 (stima di Leo, si cambia in
   pannello_config.json con "contatore_token_100"). A 80% avviso nel log, a 100% i nuovi lavori
   non partono finche' la finestra non scende. La chat del pannello non viene bloccata.
   La chat Cowork NON e' contata (non lascia log sul PC).
"""
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent                    # ...\Multiple Agents
import sys  # noqa: E402
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
LIMITE_FILE = ROOT / "LIMITE_CLAUDE.txt"                  # "fino a" ISO + motivo
CV_LOCK = ROOT / "candidature" / "stato" / "attivo.lock"  # heartbeat ogni 20 s
GEN_LOCK = ROOT / "generico" / "runner.lock"
CONFIG = ROOT / "pannello" / "pannello_config.json"

PREZZO_TOKEN = 3.0 / 1_000_000      # USD per token di input Sonnet (listino)
FINESTRA_ORE = 5
AVVISO_PCT, PAUSA_PCT = 80, 100

# Il consumo si legge dal log unico logs\uso.csv, scritto da motori.py (piano v0.5, fase A).


def _cfg():
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def token_100():
    try:
        return int(_cfg().get("contatore_token_100") or 1_000_000)
    except (TypeError, ValueError):
        return 1_000_000


def _when(v):
    v = (v or "").strip().replace("T", " ")[:19]
    for fmt, n in (("%Y-%m-%d %H:%M:%S", 19), ("%Y-%m-%d %H:%M", 16)):
        try:
            return datetime.strptime(v[:n], fmt)
        except ValueError:
            pass
    return None


def contatore(ora=None):
    """{'pct', 'token', 'per_fonte': {...}, 'avviso', 'pausa'} sulle ultime 5 ore (dal log unico di motori.py)."""
    import motori
    c = motori.costo_ultime_ore(FINESTRA_ORE, ora)
    tok = int(c["totale"] / PREZZO_TOKEN)
    pct = round(100 * tok / token_100())
    return {"pct": pct, "token": tok, "per_fonte": {k: int(v / PREZZO_TOKEN) for k, v in c["per_fonte"].items()},
            "avviso": pct >= AVVISO_PCT, "pausa": pct >= PAUSA_PCT, "token_100": token_100()}


def token_pesati(cost_usd):
    try:
        return int(float(cost_usd or 0) / PREZZO_TOKEN)
    except (TypeError, ValueError):
        return 0


# ---------------------------------------------------------------- limite di Claude
_RESET = re.compile(r"resets?\s+(?:at\s+)?(?:([A-Za-z]{3,9})\s+(\d{1,2}),?\s+(?:at\s+)?)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)", re.I)
_MESI = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def orario_reset(testo, ora=None):
    """Legge 'resets 5am' / 'resets Oct 6, 9:30pm' dal messaggio di Claude. None se non c'e'."""
    ora = ora or datetime.now()
    m = _RESET.search(testo or "")
    if not m:
        return None
    mese, giorno, h, mi, ap = m.groups()
    h = int(h) % 12 + (12 if ap.lower() == "pm" else 0)
    t = ora.replace(hour=h, minute=int(mi or 0), second=0, microsecond=0)
    if mese and mese[:3].lower() in _MESI:
        try:
            t = t.replace(month=_MESI[mese[:3].lower()], day=int(giorno))
        except ValueError:
            pass
        if t < ora - timedelta(days=1):
            t = t.replace(year=t.year + 1)
    elif t <= ora:
        t += timedelta(days=1)
    return t + timedelta(minutes=2)


def imposta_limite(testo, chi, ora=None):
    """Registra il limite per TUTTI i runner. Torna l'orario fino a cui si aspetta."""
    ora = ora or datetime.now()
    fino = orario_reset(testo, ora) or ora + timedelta(minutes=60)
    stima = "" if orario_reset(testo, ora) else " (orario di reset non letto: stima 60 min)"
    LIMITE_FILE.write_text(f"{fino.isoformat(timespec='seconds')}\n{chi} {ora:%Y-%m-%d %H:%M}{stima}\n", encoding="utf-8")
    return fino


def limite_fino():
    try:
        fino = datetime.fromisoformat(LIMITE_FILE.read_text(encoding="utf-8").splitlines()[0].strip())
    except Exception:
        return None
    if datetime.now() >= fino:
        try:
            LIMITE_FILE.unlink()
        except OSError:
            pass
        return None
    return fino


def pulizia_avvio():
    """Approvata da Leo il 04/10 ('si', con correzioni):
    - toglie gli STOP AUTOMATICI per limite (sistema vecchio: restavano e bloccavano tutto per ore);
    - toglie lo STOP del 04/10 02:31 messo durante il limite (Leo ha chiesto di ripartire);
    - toglie il doppione failed/T02-schema.task.md (T02 e' in done/).
    Gli STOP che metti tu dal pannello da ora in poi NON vengono toccati."""
    fatto = []
    for stop in (ROOT / "candidature" / "stato" / "STOP", ROOT / "generico" / "STOP"):
        try:
            t = stop.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if t.startswith("STOP automatico: limite") or t == "STOP creato dal pannello il 2026-10-04T02:31:15":
            stop.unlink()
            fatto.append(f"tolto {stop.relative_to(ROOT)} ({t[:40]}...)")
    f2 = ROOT / "generico" / "failed" / "T02-schema.task.md"
    if f2.exists() and (ROOT / "generico" / "done" / "T02-schema.task.md").exists():
        f2.unlink()
        fatto.append("tolto il doppione generico/failed/T02-schema.task.md")
    return fatto


# ---------------------------------------------------------------- un agente alla volta
def _eta(p):
    try:
        return time.time() - p.stat().st_mtime
    except OSError:
        return None


def altro_al_lavoro(chi):
    """chi = 'candidature' o 'generico'. Torna il nome dell'altro runner attivo, o None."""
    if chi != "candidature":
        a = _eta(CV_LOCK)
        if a is not None and a < 90:
            return "candidature"
    if chi != "generico":
        a = _eta(GEN_LOCK)
        if a is not None and a < 3 * 3600:
            return "generico (Langue e altri task)"
    return None


def quando(dt):
    return f"{dt:%H:%M}" if dt.date() == datetime.now().date() else f"{dt:%d/%m %H:%M}"


def perche_non_parte(chi):
    """Motivo per cui un nuovo lavoro NON deve partire adesso, oppure '' se puo' partire."""
    f = limite_fino()
    if f:
        return f"limite di Claude: riparto da solo dopo le {quando(f)}"
    c = contatore()
    if c["pausa"]:
        return f"contatore d'uso al {c['pct']}% (ultime 5 ore): aspetto che scenda sotto il 100%"
    o = altro_al_lavoro(chi)
    if o:
        return f"sta lavorando un altro agente ({o}): un solo agente alla volta"
    return ""
