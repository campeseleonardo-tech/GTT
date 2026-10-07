r"""
motori.py - l'UNICO punto da cui passano le chiamate ai modelli (piano v0.5, fase A, 04/10/2026).

Oggi c'e' un solo motore: Claude Code con l'abbonamento Pro ("claude -p").
Nella fase B qui si aggiungono i motori gratuiti (OpenRouter, OpenCode): i runner e il pannello non cambiano.

UN SOLO LOG DEL CONSUMO: logs\uso.csv
  - una riga per ogni chiamata a un modello (chi, progetto, task, fase, motore, modello, token, costo, secondi, esito);
  - una riga "esito" per ogni task generico finito (fase = esito, senza costo): serve al pannello e al diario.
  La prima volta copia dentro i 3 log vecchi (generico\logs\usage.csv, candidature\stato\uso.csv,
  pannello\chat_uso.csv); da quel momento quei file non vengono piu' letti ne' scritti.
Solo libreria standard di Python.
"""
import csv
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "logs" / "uso.csv"
IN_CORSO = ROOT / "logs" / "in_corso"     # un file per ogni chiamata in corso (chi, progetto, task, fase, inizio): lo legge il pannello
CALIBRA = ROOT / "logs" / "calibrazione.jsonl"   # i % che Leo legge in Claude, accanto ai token contati in quel momento
PREZZO_TOKEN = 3.0 / 1_000_000            # USD di listino per token di input Sonnet: costo -> "token pesati"
CAMPI = ["quando", "chi", "progetto", "task", "fase", "livello", "motore", "modello", "esito", "sottotipo",
         "turni", "token_input", "cache_scritti", "cache_letti", "token_output", "costo_listino_usd", "secondi"]
VECCHI = {
    "generico": ROOT / "generico" / "logs" / "usage.csv",
    "candidature": ROOT / "candidature" / "stato" / "uso.csv",
    "pannello": ROOT / "pannello" / "chat_uso.csv",
}
NOWIN = 0x08000000 if os.name == "nt" else 0          # nessuna finestra nera su Windows
SEGNI_LIMITE = ("usage limit", "rate limit", "limit reached", "limit will reset", "too many requests", "quota")


class Risposta:
    """Risultato di una chiamata. stdout/stderr/returncode hanno gli stessi nomi di subprocess, cosi' i runner non cambiano."""

    def __init__(self):
        self.stdout, self.stderr, self.returncode = "", "", 0
        self.dati = None          # JSON finale di claude (dict) o None
        self.timeout = False
        self.secondi = 0.0
        self.esito = ""           # ok | limite | turni_finiti | timeout | errore
        self.costo = 0.0
        self.turni = None
        self.testo = ""           # risposta finale del modello
        self.modelli = ""         # modelli che hanno lavorato davvero (es. claude-sonnet-5-5)
        self.inizio = None
        self.fine = None


# ------------------------------------------------------------------ Claude Code
def trova_claude():
    p = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if p:
        return p
    for c in (Path.home() / ".local" / "bin" / "claude.exe", Path.home() / ".local" / "bin" / "claude"):
        if c.exists():
            return str(c)
    return None


_CAPS = {}
_OPZIONI = ("--effort", "--restricted", "--permission-prompts", "--no-session-persistence", "--add-dir", "--allowedTools")


def capacita(claude):
    """Quali opzioni conosce il claude installato (legge --help, 0 token). Se --help non risponde le considera tutte presenti."""
    if claude not in _CAPS:
        h = ""
        try:
            r = subprocess.run([claude, "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                               stdin=subprocess.DEVNULL, timeout=60, creationflags=NOWIN)
            h = (r.stdout or "") + (r.stderr or "")
        except Exception:
            h = ""
        _CAPS[claude] = {o for o in _OPZIONI if o in h} if "--output-format" in h else set(_OPZIONI)
    return _CAPS[claude]


def env_pulito():
    """Senza ANTHROPIC_API_KEY: cosi' si usa sempre l'abbonamento, mai l'API a pagamento."""
    return {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}


def comando(prompt, *, claude=None, modello="sonnet", turni=10, effort=None, strumenti=None, modifica=False,
            cartelle_extra=(), ristretto=True, sessione=False, stdin=True):
    """Il comando claude -p che verrebbe eseguito (lista)."""
    claude = claude or trova_claude() or "claude"
    caps = capacita(claude) if claude != "claude" or shutil.which("claude") else set(_OPZIONI)
    cmd = [claude, "-p"] + ([] if stdin else [prompt])
    if "--add-dir" in caps:
        for d in cartelle_extra or ():
            cmd += ["--add-dir", str(d)]
    cmd += ["--output-format", "json", "--model", modello, "--max-turns", str(turni)]
    if strumenti:
        cmd += ["--allowedTools", strumenti]
    if effort and "--effort" in caps:
        cmd += ["--effort", effort]
    if ristretto and "--restricted" in caps:
        cmd += ["--restricted"]
    if modifica:
        cmd += ["--permission-mode", "acceptEdits"]
    if "--permission-prompts" in caps:
        cmd += ["--permission-prompts", "none"]
    if not sessione and "--no-session-persistence" in caps:
        cmd += ["--no-session-persistence"]
    return cmd


def _json(stdout):
    s = (stdout or "").strip()
    try:
        return json.loads(s)
    except Exception:
        pass
    for line in reversed(s.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except Exception:
                continue
    return None


def chiama(prompt, cartella, *, chi, progetto="", task="", fase="", livello="", modello="sonnet", turni=10,
           effort=None, strumenti=None, modifica=False, cartelle_extra=(), ristretto=True, sessione=False,
           stdin=True, timeout=600, motore="claude", leggi=(), scrivi=()):
    """Chiama un modello e registra la riga nel log unico. Non solleva eccezioni per timeout: Risposta.timeout = True.
    chi = chi chiama (generico | candidature | pannello); fase = agente, fix, cv, lettera, chat, ...
    stdin = True: il prompt passa dall'ingresso standard (task lunghi); False: come argomento."""
    if motore in ("auto", "gratis", "openrouter"):
        return _colpo_singolo(prompt, cartella, chi=chi, progetto=progetto, task=task, fase=fase, livello=livello,
                              motore=motore, modello=modello, leggi=leggi, scrivi=scrivi, timeout=timeout)
    if motore != "claude":
        raise ValueError(f"motore sconosciuto: {motore}")
    r = Risposta()
    claude = trova_claude()
    if not claude:
        r.esito, r.stderr, r.returncode = "errore", "programma 'claude' non trovato", 127
        return r
    cmd = comando(prompt, claude=claude, modello=modello, turni=turni, effort=effort, strumenti=strumenti,
                  modifica=modifica, cartelle_extra=cartelle_extra, ristretto=ristretto, sessione=sessione, stdin=stdin)
    r.inizio = datetime.now()
    t0 = time.time()
    segno = _in_corso_apri(chi, progetto, task, fase, timeout, "Claude", modello)
    try:
        p = subprocess.run(cmd, input=prompt if stdin else None, stdin=None if stdin else subprocess.DEVNULL,
                           cwd=str(cartella), capture_output=True, text=True, encoding="utf-8", errors="replace",
                           env=env_pulito(), timeout=timeout, creationflags=NOWIN)
        r.stdout, r.stderr, r.returncode = p.stdout or "", p.stderr or "", p.returncode
    except subprocess.TimeoutExpired as e:
        r.timeout = True
        out = e.stdout or ""
        r.stdout = out.decode("utf-8", "replace") if isinstance(out, bytes) else out
    finally:
        _in_corso_chiudi(segno)
    r.secondi = time.time() - t0
    r.fine = datetime.now()
    j = _json(r.stdout)
    r.dati = j
    j = j or {}
    r.costo = float(j.get("total_cost_usd") or 0.0)
    r.turni = j.get("num_turns")
    r.testo = str(j.get("result") or "")
    r.modelli = ",".join((j.get("modelUsage") or {}).keys())
    blob = (r.stdout + " " + r.stderr).lower()
    if r.timeout:
        r.esito = "timeout"
    elif j.get("subtype") == "error_max_turns":
        r.esito = "turni_finiti"
    elif not r.dati or j.get("is_error") or r.returncode != 0:
        r.esito = "limite" if (any(s in blob for s in SEGNI_LIMITE) or j.get("api_error_status") == 429) else "errore"
    else:
        r.esito = "ok"
    u = j.get("usage") or {}
    registra({"quando": r.fine.strftime("%Y-%m-%d %H:%M:%S"), "chi": chi, "progetto": progetto, "task": task, "fase": fase,
              "livello": livello, "motore": motore, "modello": r.modelli or modello, "esito": r.esito,
              "sottotipo": j.get("subtype", ""), "turni": r.turni if r.turni is not None else "",
              "token_input": u.get("input_tokens", ""), "cache_scritti": u.get("cache_creation_input_tokens", ""),
              "cache_letti": u.get("cache_read_input_tokens", ""), "token_output": u.get("output_tokens", ""),
              "costo_listino_usd": round(r.costo, 4) if r.dati else "", "secondi": round(r.secondi)})
    return r


_N = [0]


def _in_corso_apri(chi, progetto, task, fase, timeout, motore="Claude", modello=""):
    try:
        IN_CORSO.mkdir(parents=True, exist_ok=True)
        _N[0] += 1
        f = IN_CORSO / f"{os.getpid()}_{_N[0]}.json"
        f.write_text(json.dumps({"chi": chi, "progetto": progetto, "task": task, "fase": fase, "motore": motore, "modello": modello,
                                 "inizio": datetime.now().isoformat(timespec="seconds"),
                                 "fino": (datetime.now() + timedelta(seconds=timeout + 120)).isoformat(timespec="seconds")},
                                ensure_ascii=False), encoding="utf-8")
        return f
    except Exception:
        return None


def _in_corso_modello(f, modello):
    """Aggiorna il modello in uso nel segno 'in corso' (cambia quando un gratis e' occupato e si passa al successivo). Per il pannello."""
    try:
        if f and f.exists():
            d = json.loads(f.read_text(encoding="utf-8"))
            d["modello"] = modello
            d["modello_da"] = datetime.now().isoformat(timespec="seconds")
            f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _in_corso_chiudi(f):
    try:
        if f:
            f.unlink(missing_ok=True)
    except Exception:
        pass


def in_corso():
    """Chiamate ai modelli in corso adesso (anche piu' di una). Ignora i file rimasti da un programma interrotto."""
    out = []
    now = datetime.now()
    for f in sorted(IN_CORSO.glob("*.json")) if IN_CORSO.exists() else []:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            if datetime.fromisoformat(d["fino"]) < now:
                f.unlink(missing_ok=True)
                continue
            out.append(d)
        except Exception:
            continue
    return out


# ------------------------------------------------------------------ log unico
def registra(riga):
    try:
        _migra()
        LOG.parent.mkdir(parents=True, exist_ok=True)
        nuovo = not LOG.exists()
        with open(LOG, "a", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CAMPI)
            if nuovo:
                w.writeheader()
            w.writerow({k: riga.get(k, "") for k in CAMPI})
    except Exception:
        pass        # il log non deve mai fermare un lavoro


def esito_task(*, chi, progetto, task, livello="", esito="", sottotipo="", turni="", secondi=""):
    """Riga di ESITO di un task (fase = esito, senza costo: il consumo e' gia' nelle righe delle chiamate)."""
    registra({"quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "chi": chi, "progetto": progetto, "task": task,
              "fase": "esito", "livello": livello, "esito": esito, "sottotipo": sottotipo, "turni": turni, "secondi": secondi})


def _quando(v):
    v = (v or "").strip().replace("T", " ")[:19]
    for fmt, n in (("%Y-%m-%d %H:%M:%S", 19), ("%Y-%m-%d %H:%M", 16)):
        try:
            return datetime.strptime(v[:n], fmt)
        except ValueError:
            pass
    return None


def righe(dal=None, **filtri):
    """Righe del log unico (dict), dalla piu' vecchia. dal = datetime; filtri = campo=valore (es. progetto='candidature')."""
    _migra()
    out = []
    try:
        with open(LOG, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if any((r.get(k) or "") != v for k, v in filtri.items()):
                    continue
                if dal is not None:
                    t = _quando(r.get("quando"))
                    if not t or t < dal:
                        continue
                out.append(r)
    except OSError:
        pass
    return out


def costo(r):
    try:
        return float(r.get("costo_listino_usd") or 0)
    except (TypeError, ValueError):
        return 0.0


def token(r):
    tot = 0
    for k in ("token_input", "cache_scritti", "cache_letti", "token_output"):
        try:
            tot += int(float(r.get(k) or 0))
        except (TypeError, ValueError):
            pass
    return tot


def costo_ultime_ore(ore=5, ora=None):
    """{'totale': USD, 'per_fonte': {chi: USD}} delle ultime ore (per il contatore d'uso)."""
    ora = ora or datetime.now()
    per = {}
    for r in righe(dal=ora - timedelta(hours=ore)):
        c = costo(r) if (r.get("motore") or "claude") == "claude" else 0
        if c:
            nome = {"generico": "agenti generici", "candidature": "candidature", "pannello": "chat pannello"}.get(r.get("chi"), r.get("chi") or "?")
            per[nome] = per.get(nome, 0.0) + c
    return {"totale": sum(per.values()), "per_fonte": per}


def per_task(chi="generico"):
    """Riassunto per task, con i nomi dei campi del vecchio generico\\logs\\usage.csv (per pannello e diario):
    {task_id: {timestamp, task_id, project, tier, model, status, subtype, num_turns, cost_usd, costo_tot, input_tokens, ...}}"""
    out = {}
    for r in righe(chi=chi):
        tid = r.get("task") or ""
        if not tid:
            continue
        o = out.setdefault(tid, {"task_id": tid, "costo_tot": 0.0, "cost_usd": 0.0, "input_tokens": 0, "cache_creation": 0,
                                 "cache_read": 0, "output_tokens": 0, "num_turns": "", "status": "", "subtype": ""})
        o["timestamp"] = (r.get("quando") or "").replace(" ", "T")
        o["project"] = r.get("progetto") or o.get("project", "")
        if r.get("livello"):
            o["tier"] = r["livello"]
        if r.get("fase") == "esito":
            o["status"], o["subtype"] = r.get("esito") or "", r.get("sottotipo") or ""
            if r.get("turni"):
                o["num_turns"] = r["turni"]
            if r.get("secondi"):
                o["duration_s"] = r["secondi"]
            continue
        c = costo(r)
        o["costo_tot"] += c
        o["cost_usd"] = round(o["costo_tot"], 4)
        o["model"] = r.get("modello") or o.get("model", "")
        for k_new, k_old in (("token_input", "input_tokens"), ("cache_scritti", "cache_creation"),
                             ("cache_letti", "cache_read"), ("token_output", "output_tokens")):
            try:
                o[k_old] += int(float(r.get(k_new) or 0))
            except (TypeError, ValueError):
                pass
        if r.get("fase") == "agente" and r.get("turni"):
            o["num_turns"] = r["turni"]
    return out


def righe_candidature():
    """Righe delle candidature con i nomi dei campi del vecchio candidature\\stato\\uso.csv (per il pannello)."""
    out = []
    stato = {"ok": "ok", "limite": "LIMIT", "timeout": "TIMEOUT", "turni_finiti": "INCOMPLETE", "errore": "ERROR"}
    for r in righe(chi="candidature"):
        if r.get("fase") == "esito":
            continue
        fine = _quando(r.get("quando"))
        try:
            sec = float(r.get("secondi") or 0)
        except ValueError:
            sec = 0.0
        ini = (fine - timedelta(seconds=sec)) if fine else None
        out.append({"offer": r.get("task"), "phase": r.get("fase"), "started": ini.strftime("%Y-%m-%d %H:%M:%S") if ini else "",
                    "ended": r.get("quando"), "wall_s": r.get("secondi"), "turns": r.get("turni"), "model": r.get("modello"),
                    "input_tokens": r.get("token_input"), "cache_creation": r.get("cache_scritti"),
                    "cache_read": r.get("cache_letti"), "output_tokens": r.get("token_output"),
                    "cost_usd_listprice": r.get("costo_listino_usd"), "status": stato.get(r.get("esito"), r.get("esito")),
                    "subtype": r.get("sottotipo")})
    return out


# ------------------------------------------------------------------ migrazione dei 3 log vecchi (una volta sola)
def _migra():
    if LOG.exists():
        return
    rows = []
    f = VECCHI["generico"]
    try:
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                base = {"quando": (r.get("timestamp") or "").replace("T", " "), "chi": "generico", "progetto": r.get("project", ""),
                        "task": r.get("task_id", ""), "livello": r.get("tier", "")}
                if r.get("cost_usd") or r.get("num_turns"):
                    rows.append({**base, "fase": "agente", "motore": "claude", "modello": r.get("model", ""),
                                 "esito": "ok" if r.get("subtype") == "success" else (r.get("status") or ""),
                                 "sottotipo": r.get("subtype", ""), "turni": r.get("num_turns", ""),
                                 "token_input": r.get("input_tokens", ""), "cache_scritti": r.get("cache_creation", ""),
                                 "cache_letti": r.get("cache_read", ""), "token_output": r.get("output_tokens", ""),
                                 "costo_listino_usd": r.get("cost_usd", ""), "secondi": r.get("duration_s", "")})
                rows.append({**base, "fase": "esito", "esito": r.get("status", ""), "sottotipo": r.get("subtype", ""),
                             "turni": r.get("num_turns", ""), "secondi": r.get("duration_s", "")})
    except OSError:
        pass
    mappa_st = {"ok": "ok", "LIMIT": "limite", "TIMEOUT": "timeout", "INCOMPLETE": "turni_finiti", "ERROR": "errore"}
    try:
        with open(VECCHI["candidature"], encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                rows.append({"quando": r.get("ended", ""), "chi": "candidature", "progetto": "candidature", "task": r.get("offer", ""),
                             "fase": r.get("phase", ""), "motore": "claude", "modello": r.get("model", ""),
                             "esito": mappa_st.get(r.get("status"), r.get("status", "")), "sottotipo": r.get("subtype", ""),
                             "turni": r.get("turns", ""), "token_input": r.get("input_tokens", ""),
                             "cache_scritti": r.get("cache_creation", ""), "cache_letti": r.get("cache_read", ""),
                             "token_output": r.get("output_tokens", ""), "costo_listino_usd": r.get("cost_usd_listprice", ""),
                             "secondi": r.get("wall_s", "")})
    except OSError:
        pass
    try:
        with open(VECCHI["pannello"], encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                rows.append({"quando": r.get("ended", ""), "chi": "pannello", "task": "chat",
                             "fase": "modifica" if (r.get("subtype") or "") == "modifica" else "chat", "motore": "claude",
                             "modello": "sonnet", "esito": "ok", "turni": r.get("turns", ""), "token_input": r.get("tokens", ""),
                             "costo_listino_usd": r.get("cost_usd_listprice", ""), "secondi": r.get("wall_s", "")})
    except OSError:
        pass
    rows.sort(key=lambda x: x.get("quando") or "")
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        tmp = LOG.with_name(f"uso.{os.getpid()}.tmp")
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=CAMPI)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in CAMPI})
        if LOG.exists():           # un altro programma l'ha appena creato: vale il suo
            tmp.unlink()
        else:
            os.replace(tmp, LOG)
    except OSError:
        pass


# ------------------------------------------------------------------ consumo per il pannello (token pesati)
def pesati(r):
    """Token "pesati" di una riga: costo di listino convertito in token di input Sonnet.
    Le letture dalla cache costano poco e quindi pesano poco, come nei limiti di Claude."""
    return int(costo(r) / PREZZO_TOKEN)


def consumo(ora=None):
    """Token pesati per progetto e per motore in 3 periodi: 5 ore, oggi, 7 giorni."""
    ora = ora or datetime.now()
    inizi = {"5h": ora - timedelta(hours=5), "oggi": ora.replace(hour=0, minute=0, second=0, microsecond=0),
             "7g": ora - timedelta(days=7)}
    out = {k: {"totale": 0, "progetti": {}, "motori": {}} for k in inizi}
    pesante = None
    for r in righe(dal=min(inizi.values())):
        mot = r.get("motore") or "claude"
        if r.get("fase") == "esito":
            continue
        claude = mot == "claude"
        t = pesati(r) if claude else token(r)
        if not t:
            continue
        q = _quando(r.get("quando"))
        nome = "chat" if r.get("chi") == "pannello" else (r.get("progetto") or r.get("chi") or "altro")
        for k, da in inizi.items():
            if q and q >= da:
                o = out[k]
                o["motori"][mot] = o["motori"].get(mot, 0) + t
                if claude:
                    o["totale"] += t
                    o["progetti"][nome] = o["progetti"].get(nome, 0) + t
                else:
                    o.setdefault("gratis", {})
                    o["gratis"][nome] = o["gratis"].get(nome, 0) + t
    per_task = {}
    for r in righe(dal=inizi["7g"]):
        if r.get("task") and r.get("chi") != "pannello":
            k = (r.get("progetto") or r.get("chi"), r.get("task"))
            per_task[k] = per_task.get(k, 0) + pesati(r)
    if per_task:
        k = max(per_task, key=per_task.get)
        pesante = {"progetto": k[0], "task": k[1], "token": per_task[k]}
    out["pesante_7g"] = pesante
    out["calibrazione"] = calibrazione()
    return out


def annota_claude(pct5h=None, pct7g=None):
    """Salva i % letti in Claude accanto ai token contati adesso (per stimare quanti token valgono il 100%)."""
    c = consumo()
    riga = {"quando": datetime.now().isoformat(timespec="seconds"), "pct5h": pct5h, "pct7g": pct7g,
            "token5h": c["5h"]["totale"], "token7g": c["7g"]["totale"]}
    CALIBRA.parent.mkdir(parents=True, exist_ok=True)
    with open(CALIBRA, "a", encoding="utf-8") as f:
        f.write(json.dumps(riga) + "\n")
    return riga


def calibrazione():
    """Stima di quanti token pesati valgono il 100% (mediana delle annotazioni con almeno 5%)."""
    pts = []
    try:
        for line in CALIBRA.read_text(encoding="utf-8").splitlines():
            try:
                pts.append(json.loads(line))
            except Exception:
                pass
    except OSError:
        pass

    def stima(kp, kt):
        v = sorted(p[kt] * 100 / p[kp] for p in pts if (p.get(kp) or 0) >= 5 and p.get(kt))
        return int(v[len(v) // 2]) if len(v) >= 3 else None
    return {"n": len(pts), "cento_5h": stima("pct5h", "token5h"), "cento_7g": stima("pct7g", "token7g"),
            "ultima": pts[-1] if pts else None}


def durata_solita(chi, progetto="", fase="agente", livello=""):
    """Secondi che ci mette di solito una chiamata simile (media delle ultime 10), o None."""
    v = [float(r.get("secondi") or 0) for r in righe(chi=chi, fase=fase)
         if (not progetto or r.get("progetto") == progetto) and (not livello or r.get("livello") == livello)
         and r.get("esito") == "ok" and float(r.get("secondi") or 0) > 0]
    v = v[-10:]
    return int(sum(v) / len(v)) if len(v) >= 2 else None



# ================================================================== FASE B: OpenRouter "a colpo singolo" (05/10)
# motore = claude      -> solo Claude (come prima)
#          auto        -> prima un modello gratuito; se fallisce, il runner passa a Claude
#          gratis      -> solo modelli gratuiti; se fallisce si ferma (Da sistemare)
#          openrouter  -> il modello scelto nel task (campo modello:), anche a pagamento; se fallisce si ferma
MOTORI = {"claude": "Claude (Pro)", "auto": "Gratis, poi Claude", "gratis": "Solo gratis", "openrouter": "OpenRouter, modello scelto"}
MODELLO_GRATIS = "openrouter/free"          # OpenRouter sceglie da solo un modello gratuito e dice quale ha usato
CHIAVI = Path.home() / ".ufficio" / "chiavi.json"   # FUORI dalle cartelle che la chat del pannello puo' leggere
URL_OPENROUTER = os.environ.get("UFFICIO_OPENROUTER_URL") or "https://openrouter.ai/api/v1/chat/completions"
MAX_FILE = 150_000          # caratteri per file messo nel messaggio
MAX_TOT = 300_000           # caratteri in tutto


def predefinito():
    """Motore predefinito di tutto l'Ufficio (Impostazioni), usato se task e progetto non dicono niente."""
    try:
        m = json.loads((ROOT / "pannello" / "pannello_config.json").read_text(encoding="utf-8-sig")).get("motore_predefinito")
    except Exception:
        m = None
    return m if m in MOTORI else "claude"


def chiave(nome="openrouter"):
    v = os.environ.get(nome.upper() + "_API_KEY")
    if v:
        return v.strip()
    try:
        return (json.loads(CHIAVI.read_text(encoding="utf-8")).get(nome) or "").strip() or None
    except Exception:
        return None


def salva_chiave(nome, valore):
    try:
        d = json.loads(CHIAVI.read_text(encoding="utf-8"))
    except Exception:
        d = {}
    valore = (valore or "").strip()
    if valore:
        d[nome] = valore
    else:
        d.pop(nome, None)
    CHIAVI.parent.mkdir(parents=True, exist_ok=True)
    CHIAVI.write_text(json.dumps(d, indent=1), encoding="utf-8")
    return bool(valore)


def modello_per(motore, modello=None):
    m = (modello or "").strip()
    if m.lower().startswith("@gratis"):
        m = risolvi_slot(m)
    elif m.lower() == "@forte" or m.lower()[1:] in FORNITORI:
        m = risolvi_forte(m)
    # senza modello scelto NON si usa piu' "openrouter/free" (pesca a caso: anche modelli di sicurezza o minuscoli): si usa lo slot 1, il migliore provato
    fallback = risolvi_slot("@gratis1")
    if motore in ("auto", "gratis"):
        return m if (m.endswith(":free") or _prov(m)) else fallback
    return m if m and m not in ("sonnet", "opus", "haiku") else fallback


# ---- modelli gratuiti: elenco vivo (07/10) -------------------------------------------------------------------
MODELLO_FISSO = "nvidia/nemotron-3-super-120b-a12b:free"          # provato a mano (T17): resta sempre lo slot 1
URL_MODELLI = os.environ.get("UFFICIO_OPENROUTER_MODELS_URL") or "https://openrouter.ai/api/v1/models"
_NO_MODELLI = ("safety", "guard", "moderat", "embed", "vision", "image", "audio", "tts", "whisper", "ocr", "rerank", "-vl", "omni")


def modelli_gratis(forza=False):
    """Modelli ':free' di OpenRouter adatti a scrivere testo/codice, dal migliore al peggiore (grandezza stimata, poi contesto).
    L'elenco e' salvato 6 ore in logs\\modelli_gratis.json: se OpenRouter non risponde si usa quello vecchio."""
    cache = ROOT / "logs" / "modelli_gratis.json"
    try:
        c = json.loads(cache.read_text(encoding="utf-8"))
        if not forza and time.time() - c.get("t", 0) < 6 * 3600 and c.get("modelli"):
            return c["modelli"]
    except Exception:
        c = {}
    try:
        import re as _re
        import urllib.request
        with urllib.request.urlopen(urllib.request.Request(URL_MODELLI, headers={"User-Agent": "ufficio"}), timeout=30) as resp:
            dati = json.loads(resp.read().decode("utf-8", "replace")).get("data", [])
        out = []
        for m in dati:
            mid = str(m.get("id") or "")
            if not mid.endswith(":free") or any(x in mid.lower() for x in _NO_MODELLI):
                continue
            arch = m.get("architecture") or {}
            if "text" not in (arch.get("output_modalities") or ["text"]):
                continue
            ctx = int(m.get("context_length") or 0)
            if ctx < 32000:
                continue
            g = _re.search(r"(\d+(?:\.\d+)?)b", mid.lower())
            out.append((float(g.group(1)) if g else 0.0, ctx, mid))
        out.sort(key=lambda x: (-x[0], -x[1], x[2]))
        ids = [x[2] for x in out]
        if MODELLO_FISSO in ids:
            ids.remove(MODELLO_FISSO)
        ids.insert(0, MODELLO_FISSO)
        if len(ids) > 1:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps({"t": time.time(), "modelli": ids}, ensure_ascii=False), encoding="utf-8")
        return ids
    except Exception:
        return c.get("modelli") or [MODELLO_FISSO]


def risolvi_slot(m):
    """'@gratis1' = modello fisso provato; '@gratis2', '@gratis3'... = i successivi dell'elenco vivo (log: modello effettivo)."""
    import re as _re
    g = _re.match(r"@gratis(\d*)$", m.strip().lower())
    n = max(1, int(g.group(1) or 1)) if g else 1
    ids = modelli_gratis()
    return ids[(n - 1) % len(ids)] if ids else MODELLO_FISSO


# ---- fornitori "compatibili OpenAI": modelli grandi gratis con limiti (05/10, piano v5) ------------------------------------
# Nome nel log/task: "<fornitore>:<modello>" (es. "groq:openai/gpt-oss-120b"). Slot: "@groq", "@cerebras", "@mistral", "@gemini";
# "@forte" = il migliore disponibile tra tutti (ordine sotto), poi i gratis di OpenRouter se tutti sono occupati.
FORNITORI = {
    "gemini":   {"nome": "Google AI Studio", "url": "https://generativelanguage.googleapis.com/v1beta/openai",
                 "pref": [r"gemini-[\d.]+-flash$", r"gemini-flash-latest", r"gemini-pro-latest", r"gemini-[\d.]+-pro"]},   # 05/10: i Pro non sono nel piano gratuito (402/429 subito)
    "cerebras": {"nome": "Cerebras", "url": "https://api.cerebras.ai/v1",
                 "pref": [r"gpt-oss-120b", r"qwen-?3.*235b", r"glm", r"qwen", r"llama-?4", r"llama-3\.3-70b"]},
    "groq":     {"nome": "Groq", "url": "https://api.groq.com/openai/v1",
                 "pref": [r"gpt-oss-120b", r"kimi-k2", r"qwen-?3.*(235|32)b", r"llama-?4.*maverick", r"llama-3\.3-70b"]},
    "mistral":  {"nome": "Mistral", "url": "https://api.mistral.ai/v1",
                 "pref": [r"^mistral-large-latest$", r"^mistral-medium-latest$", r"^magistral-medium-latest$", r"^devstral-medium", r"large"]},
}
ORDINE_FORTI = ("gemini", "cerebras", "groq", "mistral")
_NO_FORN = ("tts", "image", "embed", "audio", "live", "vision", "guard", "whisper", "moderation", "ocr", "transcri", "veo", "imagen", "aqa", "learnlm")


def _prov(m):
    p = (m or "").split(":", 1)[0].lower()
    return p if ":" in (m or "") and p in FORNITORI else ""


def _get_json(url, k, timeout=30):
    import urllib.request
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + k, "User-Agent": "ufficio"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def modelli_fornitore(prov, forza=False):
    """Modelli del fornitore adatti a testo/codice, dal preferito in giu' (elenco vivo, salvato 6 ore in logs\\modelli_fornitori.json)."""
    import re as _re
    cache = ROOT / "logs" / "modelli_fornitori2.json"
    try:
        c = json.loads(cache.read_text(encoding="utf-8"))
    except Exception:
        c = {}
    v = c.get(prov) or {}
    if not forza and time.time() - v.get("t", 0) < 6 * 3600 and v.get("modelli"):
        return v["modelli"]
    k = chiave(prov)
    if not k:
        return []
    try:
        d = _get_json(FORNITORI[prov]["url"] + "/models", k)
        ids = [str(x.get("id") or "").replace("models/", "") for x in (d.get("data") or d.get("models") or [])]
        ids = [i for i in ids if i and not any(n in i.lower() for n in _NO_FORN)]
        def ver(i):
            g = _re.findall(r"\d+(?:\.\d+)?", i)
            return [float(x) for x in g[:2]] if g else [0.0]
        ord_ = []
        for pat in FORNITORI[prov]["pref"]:
            hit = sorted([i for i in ids if _re.search(pat, i, _re.I) and i not in ord_],
                         key=lambda i: ("preview" in i or "exp" in i, [-x for x in ver(i)]))
            ord_ += hit
        ord_ += [i for i in ids if i not in ord_]
        sc = (c.get(prov) or {}).get("scartati", {})
        ord_ = [i for i in ord_ if i not in sc]
        c[prov] = {"t": time.time(), "modelli": ord_, "scartati": sc}
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
        return ord_
    except Exception:
        return v.get("modelli") or []


def _scarta_modello(m, o):
    """Toglie dall'elenco salvato un modello che il fornitore rifiuta (es. 404): la prossima volta si usa il successivo."""
    p, mid = _prov(m), m.split(":", 1)[1]
    cache = ROOT / "logs" / "modelli_fornitori2.json"
    try:
        c = json.loads(cache.read_text(encoding="utf-8"))
        v = c.get(p) or {}
        v["modelli"] = [x for x in v.get("modelli", []) if x != mid]
        v.setdefault("scartati", {})[mid] = (str(o.get("codice")) + " " + str(o.get("dettaglio") or o.get("errore") or ""))[:200]
        c[p] = v
        cache.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    except Exception:
        pass


def fornitori_attivi():
    return [p for p in ORDINE_FORTI if chiave(p)]


def catena_forte():
    """'@forte': il modello preferito di ogni fornitore con chiave, nell'ordine ORDINE_FORTI."""
    out = []
    for p in fornitori_attivi():
        out += [f"{p}:{x}" for x in modelli_fornitore(p)[:2]]
    return out


def _compatibile(prov, prompt, modello, timeout):
    """Una chiamata a un fornitore compatibile OpenAI. Stesso risultato di _openrouter (testo, modello, entrata, uscita, costo, errore)."""
    import urllib.request
    import urllib.error
    F = FORNITORI[prov]
    k = chiave(prov)
    if not k:
        return {"errore": f"manca la chiave di {F['nome']} (Impostazioni del pannello)"}
    body = json.dumps({"model": modello, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request(F["url"] + "/chat/completions", data=body, method="POST",
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json", "User-Agent": "ufficio"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            d = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")[:300] if hasattr(e, "read") else ""
        motivo = {401: "chiave non valida", 402: "modello non incluso nel piano gratuito", 403: "accesso negato", 413: "richiesta troppo grande per il limite gratuito",
                  429: "limite gratuito raggiunto (troppe richieste o token)", 408: "ci ha messo troppo"}.get(e.code, f"errore {e.code}")
        return {"errore": f"{F['nome']}: {motivo}", "dettaglio": txt, "codice": 429 if e.code == 413 else e.code}
    except Exception as e:
        return {"errore": f"{F['nome']} non raggiungibile: {e}"}
    if isinstance(d, list):
        d = d[0] if d else {}
    if d.get("error"):
        return {"errore": f"{F['nome']}: " + str((d["error"] or {}).get("message") or d["error"])[:200]}
    try:
        testo = d["choices"][0]["message"]["content"] or ""
    except Exception:
        testo = ""
    u = d.get("usage") or {}
    entrata, uscita = u.get("prompt_tokens") or 0, u.get("completion_tokens") or 0
    stimato = False
    if not entrata and not uscita:
        entrata, uscita, stimato = max(1, len(prompt) // 4), max(1, len(testo) // 4), True
    return {"testo": testo, "modello": f"{prov}:{d.get('model') or modello}", "entrata": entrata, "uscita": uscita, "costo": 0.0, "stimato": stimato}


def _chiama_modello(prompt, m, timeout):
    p = _prov(m)
    return _compatibile(p, prompt, m.split(":", 1)[1], timeout) if p else _openrouter(prompt, m, timeout)


def motore_log(m):
    """Nome del 'motore' nel log uso.csv: il fornitore (groq, gemini...) o openrouter."""
    return _prov(m) or "openrouter"


def risolvi_forte(m):
    m = (m or "").strip().lower()
    if m == "@forte":
        c = catena_forte()
        return c[0] if c else risolvi_slot("@gratis1")
    p = m[1:]
    if p in FORNITORI:
        mm = modelli_fornitore(p)
        return f"{p}:{mm[0]}" if mm else risolvi_slot("@gratis1")
    return m


ATTESE_RIPROVA = tuple(int(x) for x in os.environ.get("UFFICIO_ATTESE", "30,60").split(",") if x.strip())   # solo DOPO aver provato tutti i modelli
_CODICI_RIPROVABILI = (408, 429, 500, 502, 503, 504)
TEMPO_TOTALE = int(os.environ.get("UFFICIO_TEMPO_TOTALE", "900"))        # secondi massimi per una "chiamata" (tutti i tentativi insieme)
TEMPO_TENTATIVO = int(os.environ.get("UFFICIO_TEMPO_TENTATIVO", "600"))   # secondi massimi per un singolo modello
N_ALTERNATIVE = int(os.environ.get("UFFICIO_ALTERNATIVE", "5"))           # quanti altri modelli gratis provare dopo un rifiuto


def _riprovabile(o):
    return o.get("codice") in _CODICI_RIPROVABILI or bool(o.get("errore") and "non raggiungibile" in o["errore"])


def _openrouter_paziente(prompt, modello, timeout, segno=None, tempo_totale=None, attese=None):
    """Come _openrouter, ma se un modello gratuito e' occupato (429, 5xx, rete, troppo lento) passa SUBITO al modello gratuito successivo
    (non aspetta). Solo se tutti sono occupati aspetta un poco e rifa' il giro. Tempo massimo totale: TEMPO_TOTALE.
    Il risultato ha 'cambi': l'elenco dei modelli saltati e perche' (per il rapporto)."""
    t0 = time.time()
    cand = [modello]
    if _prov(modello):                      # fornitore "forte": prima gli altri forti, poi i gratis di OpenRouter
        cand += [x for x in catena_forte() if x != modello]
        try:
            cand += modelli_gratis()[:N_ALTERNATIVE]
        except Exception:
            pass
    elif modello.endswith(":free"):
        try:
            cand += [m for m in modelli_gratis() if m != modello][:N_ALTERNATIVE]
        except Exception:
            pass
    cambi, o = [], {}
    tot = tempo_totale or TEMPO_TOTALE
    att = ATTESE_RIPROVA if attese is None else tuple(attese)
    for giro in range(len(att) + 1):
        for m in cand:
            residuo = tot - (time.time() - t0)
            if residuo < 45:
                o = dict(o) if o else {}
                o.setdefault("errore", "Modelli gratis: tempo massimo raggiunto (" + str(tot) + " s) senza una risposta valida")
                o["cambi"] = cambi
                return o
            _in_corso_modello(segno, m)
            o = _chiama_modello(prompt, m, min(timeout, TEMPO_TENTATIVO, residuo))
            if _prov(m) and o.get("errore") and o.get("codice") in (400, 402, 403, 404):
                _scarta_modello(m, o)          # modello non disponibile per questa chiave: non riproporlo e passa al successivo
                cambi.append(f"{m}: {o.get('errore', '?')[:70]}")
                continue
            if not _riprovabile(o):
                o["cambi"] = cambi
                return o
            cambi.append(f"{m.split('/')[-1]}: {o.get('errore', '?')[:70]}")
        if giro < len(att):
            time.sleep(att[giro])
    o["cambi"] = cambi
    return o


def _openrouter(prompt, modello, timeout):
    """Una chiamata a OpenRouter. Torna dict: testo, modello, entrata, uscita, costo, errore."""
    import urllib.request
    import urllib.error
    k = chiave("openrouter")
    if not k:
        return {"errore": "manca la chiave di OpenRouter (Impostazioni del pannello)"}
    body = json.dumps({"model": modello, "messages": [{"role": "user", "content": prompt}],
                       "usage": {"include": True}}).encode("utf-8")
    req = urllib.request.Request(URL_OPENROUTER, data=body, method="POST", headers={
        "Authorization": "Bearer " + k, "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost/ufficio", "X-Title": "Ufficio di Leo"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            d = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")[:300] if hasattr(e, "read") else ""
        motivo = {401: "chiave non valida", 402: "credito OpenRouter finito", 429: "troppe richieste ai modelli gratuiti, riprovare piu' tardi",
                  408: "OpenRouter ci ha messo troppo"}.get(e.code, f"errore {e.code}")
        return {"errore": f"OpenRouter: {motivo}", "dettaglio": txt, "codice": e.code}
    except Exception as e:
        return {"errore": f"OpenRouter non raggiungibile: {e}"}
    if d.get("error"):
        return {"errore": "OpenRouter: " + str((d["error"] or {}).get("message") or d["error"])[:200]}
    try:
        testo = d["choices"][0]["message"]["content"] or ""
    except Exception:
        testo = ""
    u = d.get("usage") or {}
    entrata, uscita = u.get("prompt_tokens") or 0, u.get("completion_tokens") or 0
    stimato = False
    if not entrata and not uscita:        # alcuni modelli gratuiti non dicono i token: stima (circa 4 caratteri = 1 token)
        entrata, uscita, stimato = max(1, len(prompt) // 4), max(1, len(testo) // 4), True
    return {"testo": testo, "modello": d.get("model") or modello, "entrata": entrata,
            "uscita": uscita, "costo": float(u.get("cost") or 0.0), "stimato": stimato}



def conversa(prompt, *, chi="pannello", progetto="", task="chat", fase="chat", modello="@forte", timeout=180):
    """Chat con i modelli gratis (05/10, chat v2): solo testo, niente istruzioni per scrivere file, niente nota [runner].
    Usa la catena '@forte' (Gemini, Cerebras, Groq... poi i gratis di OpenRouter). Al massimo 'timeout' secondi in tutto,
    senza le lunghe attese tra un giro e l'altro. Registra la riga nel log unico come ogni altra chiamata."""
    r = Risposta()
    mod = modello_per("gratis", modello)
    r.inizio = datetime.now()
    t0 = time.time()
    segno = _in_corso_apri(chi, progetto, task, fase, timeout, "Gratis")
    try:
        o = _openrouter_paziente(prompt, mod, timeout, segno, tempo_totale=timeout + 45, attese=())
    finally:
        _in_corso_chiudi(segno)
    r.secondi = time.time() - t0
    r.fine = datetime.now()
    if o.get("errore"):
        r.esito, r.testo, r.modelli = "errore", o["errore"], mod
        r.dati = {"is_error": True, "result": o["errore"], "usage": {}}
    else:
        r.esito, r.testo, r.modelli = "ok", (o.get("testo") or "").strip(), o.get("modello") or mod
        r.dati = {"is_error": False, "result": r.testo, "stimato": bool(o.get("stimato")),
                  "usage": {"input_tokens": o.get("entrata", 0), "output_tokens": o.get("uscita", 0)}}
    r.costo = float(o.get("costo") or 0.0)
    r.turni = 1
    r.stdout = json.dumps(r.dati, ensure_ascii=False)
    r.returncode = 0 if r.esito == "ok" else 1
    u = r.dati["usage"]
    registra({"quando": r.fine.strftime("%Y-%m-%d %H:%M:%S"), "chi": chi, "progetto": progetto, "task": task, "fase": fase,
              "livello": "", "motore": motore_log(r.modelli), "modello": r.modelli, "esito": r.esito, "sottotipo": "chat",
              "turni": 1, "token_input": u.get("input_tokens", ""), "token_output": u.get("output_tokens", ""),
              "costo_listino_usd": round(r.costo, 6), "secondi": round(r.secondi)})
    return r

def _sicuro(rel):
    rel = (rel or "").strip().strip("`\"' ").replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    if not rel or rel.startswith("/") or ":" in rel or ".." in rel.split("/"):
        return None
    return rel


def _puo_scrivere(rel, scrivi):
    for a in scrivi or ():
        a = (_sicuro(a) or "").rstrip("/")
        if a and (rel == a or rel.startswith(a + "/")):
            return True
    return False


ISTRUZIONI_SINGOLO = """

=== HOW TO ANSWER (this overrides anything above about tools, reading files or running programs) ===
You cannot use tools, read files or run programs. The files you need are included below, between <<<READ path>>> and <<<END>>>.
To create or change a file, write its COMPLETE new content (never a partial diff) in a block exactly like this:
<<<FILE relative/path.ext>>>
...complete file content...
<<<END>>>
You may write ONLY these paths: {scrivi}
Write nothing else outside the blocks except your final summary, which goes AFTER all the blocks.

For a BIG EXISTING file (more than ~150 lines) do NOT rewrite it whole: send only the changed parts as search/replace edits, exactly like this:
<<<EDIT relative/path.ext>>>
<<<<<<< SEARCH
exact lines copied from the file as shown above (enough lines to be unique)
=======
the new lines that replace them
>>>>>>> REPLACE
<<<END>>>
You can put several SEARCH/REPLACE pairs in one EDIT block; they are applied in order. The SEARCH text must match the file EXACTLY and exactly once.
Use <<<FILE ...>>> (complete content) only for new files or small files.
"""


_RE_BLOCCO = r"<<<\s*FILE\s+([^\n>]+?)\s*>{1,3}[ \t]*\r?\n(.*?)(?:\r?\n)?[ \t]*(?:<<<\s*END\s*>{0,3}|(?=<<<\s*FILE)|\Z)"


_RE_EDIT = r"<<<\s*EDIT\s+([^\n>]+?)\s*>{1,3}[ \t]*\r?\n(.*?)(?:\r?\n)?[ \t]*(?:<<<\s*END\s*>{0,3}|(?=<<<\s*(?:FILE|EDIT))|\Z)"
_RE_HUNK = r"<{5,9}\s*SEARCH[ \t]*\r?\n(.*?)\r?\n={5,9}[ \t]*\r?\n(.*?)(?:\r?\n)?>{5,9}\s*REPLACE"


def _edit_blocchi(testo):
    """Blocchi <<<EDIT path>>> con coppie SEARCH/REPLACE: [(percorso, [(cerca, metti), ...])]."""
    import re as _re
    out = []
    for m in _re.finditer(_RE_EDIT, testo or "", _re.S):
        out.append((m.group(1), [(h.group(1), h.group(2)) for h in _re.finditer(_RE_HUNK, m.group(2), _re.S)]))
    return out


def _applica_hunk(testo, cerca, metti):
    """Sostituisce `cerca` (esatto e unico) con `metti`. Torna (nuovo_testo, errore|None). Tollera spazi a fine riga."""
    if not cerca.strip():
        return testo, "SEARCH vuoto"
    n = testo.count(cerca)
    if n == 1:
        return testo.replace(cerca, metti, 1), None
    if n > 1:
        return testo, f"SEARCH compare {n} volte (non unico)"
    norm = lambda x: "\n".join(l.rstrip() for l in x.split("\n"))
    t2, c2 = norm(testo), norm(cerca)
    if t2.count(c2) == 1:
        return t2.replace(c2, metti, 1), None
    return testo, "SEARCH non trovato (deve essere copiato esatto dal file)"


def _applica_edit(base, rel, hunks, scrivi=True):
    """Applica gli hunk al file esistente rel (conserva a-capo e codifica). Torna (n_applicati, [errori]).
    TUTTO O NIENTE: se anche un solo hunk non si applica, il file NON viene toccato. scrivi=False = solo prova."""
    f = Path(base) / rel
    if not f.is_file():
        return 0, [f"{rel}: il file non esiste (per i file nuovi serve <<<FILE>>>)"]
    raw = f.read_bytes().decode("utf-8", "replace")
    crlf = "\r\n" in raw
    testo = raw.replace("\r\n", "\n")
    ok, errs = 0, []
    for i, (cerca, metti) in enumerate(hunks, 1):
        testo, e = _applica_hunk(testo, cerca.replace("\r\n", "\n"), metti.replace("\r\n", "\n"))
        if e:
            errs.append(f"{rel}, modifica {i}: {e}")
        else:
            ok += 1
    if ok and not errs and scrivi:
        f.write_bytes((testo.replace("\n", "\r\n") if crlf else testo).encode("utf-8"))
    return (0 if errs else ok), errs


def _blocchi(testo):
    """Blocchi <<<FILE ...>>> ... <<<END>>>, tollerando segni scritti male (>> invece di >>>, fine mancante)."""
    import re as _re
    return [(m.group(1), m.group(2)) for m in _re.finditer(_RE_BLOCCO, testo or "", _re.S)]


def _pulisci(rel, testo):
    """Per i .json tiene solo il JSON valido (toglie ``` e testo in piu' prima o dopo)."""
    t = testo.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    if rel.lower().endswith(".json"):
        i = min([x for x in (t.find("["), t.find("{")) if x >= 0] or [0])
        try:
            _obj, fine = json.JSONDecoder().raw_decode(t[i:])
            return t[i:i + fine] + "\n"
        except ValueError:
            pass
    return t + "\n"


def _adatto(o, scrivi):
    """Il modello pescato va bene? No se e' un modello 'di sicurezza' o se non scrive nessun file quando serve."""
    nome = (o.get("modello") or "").lower()
    if any(x in nome for x in ("safety", "guard", "moderat")):
        return False
    return not scrivi or bool(_blocchi(o.get("testo") or "")) or bool(_edit_blocchi(o.get("testo") or ""))


def _colpo_singolo(prompt, cartella, *, chi, progetto, task, fase, livello, motore, modello, leggi, scrivi, timeout):
    import re as _re
    r = Risposta()
    mod = modello_per(motore, modello)
    base = Path(cartella)
    pezzi, tot, saltati = [], 0, []
    for rel in leggi or ():
        rel = _sicuro(rel)
        f = base / rel if rel else None
        if not f or not f.is_file():
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if len(txt) > MAX_FILE or tot + len(txt) > MAX_TOT:
            saltati.append(rel)
            continue
        tot += len(txt)
        pezzi.append(f"<<<READ {rel}>>>\n{txt}\n<<<END>>>")
    testo = (prompt + ISTRUZIONI_SINGOLO.format(scrivi=", ".join(scrivi or ()) or "(none)") +
             ("\n\n=== FILES ===\n" + "\n\n".join(pezzi) if pezzi else "\n\n(no files included)") +
             (f"\n\n(Not included because too large: {', '.join(saltati)})" if saltati else ""))
    r.inizio = datetime.now()
    t0 = time.time()
    segno = _in_corso_apri(chi, progetto, task, fase, timeout, "OpenRouter")
    try:
        for _giro in range(3):          # openrouter/free sceglie a caso: se pesca un modello inadatto, si richiede
            o = _openrouter_paziente(testo, mod, timeout, segno)
            if o.get("errore") or _adatto(o, scrivi):
                break
            registra({"quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "chi": chi, "progetto": progetto, "task": task,
                      "fase": fase, "livello": livello, "motore": motore_log(o.get("modello")), "modello": o.get("modello"), "esito": "scartato",
                      "turni": 1, "token_input": o.get("entrata", ""), "token_output": o.get("uscita", ""),
                      "costo_listino_usd": o.get("costo", 0.0), "secondi": round(time.time() - t0)})
    finally:
        _in_corso_chiudi(segno)
    r.secondi = time.time() - t0
    r.fine = datetime.now()
    scritti, rifiutati = [], []
    if o.get("errore"):
        r.esito = "errore"
        r.testo = o["errore"]
        dati = {"type": "result", "subtype": "error", "is_error": True, "result": o["errore"], "num_turns": 1,
                "total_cost_usd": 0.0, "usage": {}, "modelUsage": {mod: {}}}
    else:
        corpo = o["testo"]
        # prima PROVA di tutte le modifiche (senza scrivere): se una sola non si applica, non si scrive niente (tutto o niente)
        errori_edit = []
        for rel0, hunks in _edit_blocchi(corpo):
            rel = _sicuro(rel0)
            if rel and _puo_scrivere(rel, scrivi):
                errori_edit += _applica_edit(base, rel, hunks, scrivi=False)[1]
        if not errori_edit:
            for rel0, contenuto in _blocchi(corpo):
                rel = _sicuro(rel0)
                if not rel or not _puo_scrivere(rel, scrivi):
                    rifiutati.append(rel0.strip())
                    continue
                dest = base / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(_pulisci(rel, contenuto), encoding="utf-8")
                scritti.append(rel)
            for rel0, hunks in _edit_blocchi(corpo):
                rel = _sicuro(rel0)
                if not rel or not _puo_scrivere(rel, scrivi):
                    rifiutati.append(rel0.strip())
                    continue
                n_ok, errs = _applica_edit(base, rel, hunks)
                errori_edit += errs
                if n_ok and rel not in scritti:
                    scritti.append(rel)
        riass = _re.sub(_RE_EDIT, "", _re.sub(_RE_BLOCCO, "", corpo, flags=_re.S), flags=_re.S).strip()
        nota = f"\n\n[runner] motore {FORNITORI.get(_prov(o['modello']), {}).get('nome', 'OpenRouter')}, modello {o['modello']}; file scritti: {', '.join(scritti) or 'nessuno'}" + \
               (f"; RIFIUTATI (fuori dai permessi): {', '.join(rifiutati)}" if rifiutati else "") + \
               (f"; NESSUNA MODIFICA APPLICATA (tutto o niente): {' | '.join(errori_edit)}" if errori_edit else "") + \
               (f"; cambio modello per sovraccarico: {' | '.join(o['cambi'])}" if o.get("cambi") else "") + \
               ("; token stimati (il modello non li ha dichiarati)" if o.get("stimato") else "")
        r.testo = (riass or "ESITO: (il modello non ha scritto un riassunto)") + nota
        r.esito = "ok" if ((scritti or not scrivi) and not errori_edit) else "errore"
        dati = {"type": "result", "subtype": "success", "is_error": r.esito != "ok", "result": r.testo, "num_turns": 1,
                "total_cost_usd": o.get("costo", 0.0), "modelUsage": {o["modello"]: {}},
                "usage": {"input_tokens": o.get("entrata", 0), "output_tokens": o.get("uscita", 0)}}
        if r.esito != "ok":
            dati["result"] = ("Le modifiche del modello non combaciavano col file: non ho cambiato niente. " if errori_edit else "Il modello non ha scritto nessun file valido. ") + r.testo
        mod = o["modello"]
    r.dati = dati
    r.stdout = json.dumps(dati, ensure_ascii=False)
    r.returncode = 0 if r.esito == "ok" else 1
    r.costo = float(dati.get("total_cost_usd") or 0.0)
    r.turni = 1
    r.modelli = mod
    u = dati.get("usage") or {}
    registra({"quando": r.fine.strftime("%Y-%m-%d %H:%M:%S"), "chi": chi, "progetto": progetto, "task": task, "fase": fase,
              "livello": livello, "motore": motore_log(mod), "modello": mod, "esito": r.esito, "sottotipo": dati.get("subtype", ""),
              "turni": 1, "token_input": u.get("input_tokens", ""), "token_output": u.get("output_tokens", ""),
              "costo_listino_usd": round(r.costo, 6), "secondi": round(r.secondi)})
    return r


def prova(motore="openrouter"):
    """Piccola prova dal pannello: risponde? quale modello? quanto ci mette?"""
    t0 = time.time()
    if motore in FORNITORI:
        mm = modelli_fornitore(motore, forza=True)
        if not chiave(motore):
            return {"ok": False, "msg": f"Manca la chiave di {FORNITORI[motore]['nome']}."}
        if not mm:
            return {"ok": False, "msg": f"{FORNITORI[motore]['nome']}: non riesco a leggere l'elenco dei modelli (chiave giusta?)."}
        for mid in mm[:5]:
            o = _compatibile(motore, "Rispondi solo con la parola: funziona", mid, 60)
            if o.get("codice") in (400, 402, 403, 404):
                _scarta_modello(f"{motore}:{mid}", o)
                continue
            break
    else:
        o = _openrouter("Rispondi solo con la parola: funziona", MODELLO_GRATIS, 60)
    sec = round(time.time() - t0, 1)
    nome = FORNITORI.get(motore, {}).get("nome", "OpenRouter")
    if o.get("errore"):
        return {"ok": False, "msg": o["errore"]}
    registra({"quando": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "chi": "pannello", "task": "prova", "fase": "prova",
              "motore": motore_log(o["modello"]), "modello": o["modello"], "esito": "ok", "turni": 1, "token_input": o.get("entrata", ""),
              "token_output": o.get("uscita", ""), "costo_listino_usd": o.get("costo", 0.0), "secondi": round(sec)})
    return {"ok": True, "msg": f"{nome} risponde: «{(o['testo'] or '').strip()[:40]}» · modello {o['modello']} · {sec} s"}