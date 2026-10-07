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
           stdin=True, timeout=600, motore="claude"):
    """Chiama un modello e registra la riga nel log unico. Non solleva eccezioni per timeout: Risposta.timeout = True.
    chi = chi chiama (generico | candidature | pannello); fase = agente, fix, cv, lettera, chat, ...
    stdin = True: il prompt passa dall'ingresso standard (task lunghi); False: come argomento."""
    if motore != "claude":
        raise ValueError(f"motore sconosciuto: {motore} (in questa versione c'e' solo claude)")
    r = Risposta()
    claude = trova_claude()
    if not claude:
        r.esito, r.stderr, r.returncode = "errore", "programma 'claude' non trovato", 127
        return r
    cmd = comando(prompt, claude=claude, modello=modello, turni=turni, effort=effort, strumenti=strumenti,
                  modifica=modifica, cartelle_extra=cartelle_extra, ristretto=ristretto, sessione=sessione, stdin=stdin)
    r.inizio = datetime.now()
    t0 = time.time()
    segno = _in_corso_apri(chi, progetto, task, fase, timeout)
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


def _in_corso_apri(chi, progetto, task, fase, timeout):
    try:
        IN_CORSO.mkdir(parents=True, exist_ok=True)
        _N[0] += 1
        f = IN_CORSO / f"{os.getpid()}_{_N[0]}.json"
        f.write_text(json.dumps({"chi": chi, "progetto": progetto, "task": task, "fase": fase,
                                 "inizio": datetime.now().isoformat(timespec="seconds"),
                                 "fino": (datetime.now() + timedelta(seconds=timeout + 120)).isoformat(timespec="seconds")},
                                ensure_ascii=False), encoding="utf-8")
        return f
    except Exception:
        return None


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
        c = costo(r)
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
        t = pesati(r)
        if not t:
            continue
        q = _quando(r.get("quando"))
        nome = "chat" if r.get("chi") == "pannello" else (r.get("progetto") or r.get("chi") or "altro")
        mot = r.get("motore") or "claude"
        for k, da in inizi.items():
            if q and q >= da:
                o = out[k]
                o["totale"] += t
                o["progetti"][nome] = o["progetti"].get(nome, 0) + t
                o["motori"][mot] = o["motori"].get(mot, 0) + t
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
