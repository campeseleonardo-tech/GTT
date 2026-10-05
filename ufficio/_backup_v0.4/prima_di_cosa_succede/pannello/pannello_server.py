#!/usr/bin/env python3
"""
pannello_server.py - il pannello unico degli agenti (tutti i progetti).

Cosa fa:
  - legge lo stato dei progetti e lo passa alla pagina ufficio.html (il Mondo: mondo.html)
  - esegue i comandi dalla pagina: scout, approvazioni, risposte alle domande, direzioni (hint), pausa, aggiunta offerte
  - lancia i lavori degli agenti UNO ALLA VOLTA (dispatcher): quando non c'e' nulla in coda non fa nulla e non usa token
  - il pannello stesso NON chiama Claude: lo fa solo il runner, quando c'e' un lavoro da fare.

Si avvia con run.bat (un solo comando). Si ferma chiudendo la finestra nera.
Ascolta solo su questo PC (127.0.0.1) e le richieste devono portare un codice segreto,
cosi' un sito qualsiasi aperto nel browser non puo' lanciare agenti o aprire file al posto tuo.
Solo libreria standard di Python, niente da installare.
"""
import hashlib, json, mimetypes, os, re, secrets, subprocess, sys, threading, time, webbrowser
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import ufficio_extra as UX
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import motori  # noqa: E402  log unico del consumo (v0.5)
import comune  # un agente alla volta tra progetti, limite di Claude condiviso, contatore d'uso (04/10)
import ufficio_dati as UD  # pagina nuova "Ufficio" (ufficio.html): progetti, centro, diario, task (04/10)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
CONFIG_FILE = HERE / "pannello_config.json"
TOKEN = secrets.token_urlsafe(16)
NAMES = ["Marta", "Elio", "Bice", "Ugo", "Nina", "Tullio", "Greta", "Osvaldo", "Pina", "Remo", "Dora", "Ivo",
         "Lia", "Gino", "Rita", "Aldo", "Zita", "Milo", "Enea", "Vera", "Otto", "Sara", "Nico", "Ada"]
PHASE_NAMES = {1: "Analisi e CV", 2: "Lettera", 3: "Correzione"}
PHASE_CSV = {"generate": 1, "letter": 2, "fix": 3}
PHASE_TXT = {1: "Leggo l'offerta e scrivo analisi e CV", 2: "Scrivo la lettera", 3: "Correggo gli errori dei controlli"}
TEXT_EXT = {".txt", ".md", ".json", ".log", ".csv", ".py", ".yaml", ".yml", ".html"}


# ----------------------------------------------------------------- utilita'
def load_config():
    cfg = {"porta": 8765, "soglia_stop_pct": 60, "sorgenti": []}
    try:
        cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig")))
    except Exception as e:
        print(f"(config non leggibile, uso i valori base: {e})")
    for s in cfg["sorgenti"]:
        r = Path(os.path.expanduser(os.path.expandvars(s.get("radice") or "..")))
        s["_base"] = (r if r.is_absolute() else (HERE / r)).resolve()
    return cfg


def read_text_any(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16").replace("\r\n", "\n")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc).replace("\r\n", "\n")
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace").replace("\r\n", "\n")


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None


def parse_dt(s):
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(str(s).strip(), f)
        except Exception:
            pass
    return None


def num(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default


def agent_name(key):
    return NAMES[int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16) % len(NAMES)]


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def short(s, n=52):
    s = s.strip()
    return s if len(s) <= n else s[:n - 1] + "…"


def fmt_secs(s):
    s = int(round(s))
    return f"{s // 60}m{s % 60:02d}s"


def file_info(p, nome=None):
    p = Path(p)
    try:
        st = p.stat()
        return {"p": str(p), "nome": nome or p.name, "dir": p.is_dir(), "size": None if p.is_dir() else st.st_size,
                "mtime": iso(datetime.fromtimestamp(st.st_mtime))}
    except Exception:
        return {"p": str(p), "nome": nome or p.name, "dir": False, "size": None, "mtime": None, "manca": True}


def walk_files(root, depth=3, limit=60):
    out = []
    root = Path(root)
    if not root.exists():
        return out
    base = len(root.parts)
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d != "__pycache__"]
        if len(Path(dp).parts) - base >= depth:
            dn[:] = []
        for f in sorted(fn):
            out.append(Path(dp) / f)
            if len(out) >= limit:
                return out
    return out


# ------------------------------------------------------ adattatore: candidature
# Lo stato e' UNO solo (CV\stato\stato.json) e lo definisce CV\runner\state.py: il pannello usa lo stesso codice del runner.
_state_mods = {}


def cv_mod(src):
    key = str(src["_base"])
    if key not in _state_mods:
        import importlib.util
        p = src["_base"] / "runner" / "state.py"
        spec = importlib.util.spec_from_file_location("cv_state_" + hashlib.md5(key.encode()).hexdigest()[:6], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        _state_mods[key] = m
    return _state_mods[key]


def read_uso(S):
    """Chiamate delle candidature dal log unico logs\\uso.csv (motori.py, v0.5), con i nomi dei campi di prima."""
    try:
        return motori.righe_candidature()
    except Exception as e:
        print(f"(log unico non leggibile: {e})")
        return []


def cv_collect(src):
    S = cv_mod(src)
    sid = src["id"]
    s = S.load()
    tasks, domande = S.panel_view(s)
    for n, t in enumerate(tasks, 1):
        t.update(id=t["oid"], sid=f"C{n}", sorgente=sid, dip=sid, nome=agent_name(t["oid"]))
        t.pop("oid", None)
    for q in domande:
        q.update(sorgente=sid, task=q.pop("oid"), linea=None)
    busy = S.runner_busy()
    # quota (costo di listino dal registro uso.csv)
    now = datetime.now()
    c5 = t5 = cw = tw = 0.0
    per_day = {}
    for x in read_uso(S):
        e = parse_dt(x.get("ended"))
        if not e:
            continue
        cost = num(x.get("cost_usd_listprice"))
        tok = num(x.get("input_tokens")) + num(x.get("cache_creation")) + num(x.get("cache_read")) + num(x.get("output_tokens"))
        if now - e <= timedelta(hours=5):
            c5 += cost
            t5 += tok
        if now - e <= timedelta(days=7):
            cw += cost
            tw += tok
        per_day[e.strftime("%Y-%m-%d")] = per_day.get(e.strftime("%Y-%m-%d"), 0.0) + cost
    days = []
    for i in range(6, -1, -1):
        d = now - timedelta(days=i)
        days.append([["lun", "mar", "mer", "gio", "ven", "sab", "dom"][d.weekday()], round(per_day.get(d.strftime("%Y-%m-%d"), 0.0), 3)])
    quota = {"costo5h": round(c5, 3), "token5h": int(t5), "costo7g": round(cw, 3), "token7g": int(tw),
             "stimata_pct": None, "calibrata": False, "giorni": days}
    n_appr = len([t for t in tasks if t["stato"] == "da_approvare"])
    n_coda = len([j for j in s["coda"] if j["stato"] == "in_attesa"])
    paused = S.STOP_FILE.exists()
    controlli = [
        {"t": "Coda in pausa (STOP)", "d": "si: nessun nuovo lavoro parte" if paused else "no: i lavori partono da soli, uno alla volta", "ok": not paused},
        {"t": "Agente", "d": "al lavoro" if busy else "fermo, non consuma token", "ok": True},
        {"t": "Lavori in coda", "d": f"{n_coda} in attesa", "ok": True},
        {"t": "Da approvare", "d": f"{n_appr} offerte/CV aspettano il tuo OK", "ok": n_appr == 0},
        {"t": "Domande aperte", "d": f"{len(domande)} per te", "ok": len(domande) == 0}]
    return {"tasks": tasks, "domande": domande, "quota": quota, "controlli": controlli,
            "stop": {"presente": paused, "percorso": str(S.STOP_FILE)}, "runner_attivo": busy,
            "extra": {"hint": s["hint"], "scout": s["scout"].get("ultimo"),
                      "scout_b": bool(s["impostazioni"].get("scout_b")),
                      "imp": {k: s["impostazioni"].get(k) for k in ("effort", "letter_effort", "scout_effort")},
                      "mappa_n": len(s["mappa"]), "registro_n": sum(1 for r in s["registro"] if r["stato"] == "attivo"),
                      "offerte": [
                {"id": o["id"], "titolo": S.label(o), "stato": o["stato"]} for o in s["offerte"] if o["stato"] != "scartata"]}}


def cv_task_detail(src, task_id):
    S = cv_mod(src)
    s = S.load()
    groups = {"input": [], "lavoro": [], "output": []}
    cartelle, log_lines, seen = [], [], set()

    def add(g, p, nome=None):
        p = Path(p)
        if str(p) in seen or not p.exists():
            return
        seen.add(str(p))
        groups[g].append(file_info(p, nome))
    for n in S.DOCS:
        add("input", S.doc_path(n), f"{n}  (letto da qui, mai copiato)")
    if task_id in ("scout", "manutenzione", "nuove_aziende"):
        try:
            log_lines = S.LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()[-60:]
        except Exception:
            pass
    else:
        o = S.find_offer(s, task_id)
        if o:
            log_lines = o.get("log", [])
            if o.get("tag"):
                folder = S.OUT / o["tag"]
                for f in sorted(folder.glob("*")) if folder.exists() else []:
                    add("output", f)
                cartelle.append(str(folder))
            job = S.last_job(s, task_id)
            if job and job["stato"] == "in_corso":
                for f in walk_files(S.LAVORO, depth=3, limit=40):
                    add("lavoro", f, str(f.relative_to(S.LAVORO)))
    add("output", S.CODA_MD, "coda.md  (rapporto di tutto, si aggiorna da solo)")
    cartelle.append(str(S.STATO))
    link = {}
    if task_id not in ("scout", "manutenzione", "nuove_aziende"):
        o = S.find_offer(s, task_id)
        if o:
            link = {"url": o.get("url") or "", "azienda": o.get("azienda") or "", "ruolo": o.get("ruolo") or "", "sede": o.get("sede") or ""}
    return {"gruppi": groups, "cartelle": list(dict.fromkeys(cartelle)), "log": log_lines[-120:], "offerta": link}


def cv_recent(src, limit=10):
    S = cv_mod(src)
    cand = [f for f in walk_files(S.OUT, depth=3, limit=300) if f.is_file()] if S.OUT.exists() else []
    cand.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return [file_info(c) for c in cand[:limit]]


# ------------------------------------------- dispatcher: un agente alla volta
_procs = {}


def dispatch_once(cfg):
    for src in sources(cfg):
        if src.get("tipo") != "cv_runner":
            continue
        S = cv_mod(src)
        key = src["id"]
        p = _procs.get(key)
        if p is not None and p.poll() is None:
            continue
        s = S.load()
        if not S.runner_busy():
            orfani = [j for j in s["coda"] if j["stato"] == "in_corso"]
            if orfani:
                def fix(s_):
                    for j in s_["coda"]:
                        if j["stato"] == "in_corso":
                            j["stato"], j["fine"], j["esito"] = "errore", S.now_iso(), "interrotto (il programma si e' fermato a meta')"
                S.update(fix)
                continue
        if S.STOP_FILE.exists() or S.runner_busy():
            continue
        if comune.perche_non_parte("candidature"):
            continue
        job = S.next_job(s)
        if not job:
            continue
        runner_py = src["_base"] / "runner" / "runner.py"
        if not runner_py.exists():
            continue
        try:
            S.STATO.mkdir(parents=True, exist_ok=True)
            errf = open(S.LOG_FILE, "ab")
            _procs[key] = subprocess.Popen([sys.executable, str(runner_py), "job", job["id"]], cwd=str(runner_py.parent),
                                           stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=errf,
                                           creationflags=0x08000000 if os.name == "nt" else 0)
        except Exception as e:
            print(f"(non riesco a lanciare il lavoro {job['id']}: {e})")


def dispatch_loop(cfg):
    """04/10: i lavori di TUTTI i progetti li fa partire dispatcher.py (uno alla volta, rotazione 3-2-1).
    Il pannello lo sveglia ogni minuto e subito dopo ogni azione; a pannello chiuso ci pensa l'attivita' di Windows."""
    try:
        for x in comune.pulizia_avvio():
            UX.log(f"- PULIZIA {datetime.now():%Y-%m-%d %H:%M} · {x}")
    except Exception:
        pass
    while True:
        try:
            UD.avvia_dispatcher()
        except Exception:
            import traceback
            traceback.print_exc()
        time.sleep(60)


def generico_loop(cfg):
    """Se acceso in Impostazioni ("generico_auto"), avvia runner.py della cartella generico quando in coda cambia qualcosa
    (e comunque al massimo una volta all'ora), cosi' i task di Langue ecc. girano senza Task Scheduler. Il runner ha il suo blocco:
    non partono due esecuzioni insieme."""
    last_sig, last_t = None, 0.0
    while True:
        time.sleep(60)
        try:
            if not cfg.get("generico_auto"):
                continue
            s = next((x for x in cfg["sorgenti"] if x.get("tipo") == "generico" and x["_base"].exists()), None)
            rn = s["_base"] / "runner.py" if s else None
            if not rn or not rn.exists() or (s["_base"] / "STOP").exists():
                continue
            if comune.perche_non_parte("generico"):
                continue
            q = s["_base"] / "queue"
            files = sorted(q.glob("*.task.md")) if q.exists() else []
            if not files:
                continue
            sig = tuple((f.name, int(f.stat().st_mtime)) for f in files) + tuple(sorted(p.name for p in (s["_base"] / "done").glob("*.task.md")))
            if sig == last_sig and time.time() - last_t < 3600:
                continue
            last_sig, last_t = sig, time.time()
            kw = {"creationflags": 0x08000000} if os.name == "nt" else {}
            subprocess.Popen([sys.executable, str(rn)], cwd=str(s["_base"]), stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)
            UX.log(f"- AZIONE automatica {datetime.now():%Y-%m-%d %H:%M} · avviato il runner generico ({len(files)} task in coda)")
        except Exception:
            import traceback
            traceback.print_exc()


# ------------------------------------------------- adattatore: generico (C:\Agents)
def _md_task(path):
    """Legge un file *.task.md del runner generico: intestazione 'chiave: valore' fino alla riga ---."""
    text = read_text_any(path)
    head, _, body = text.partition("\n---")
    meta = {}
    for raw in head.splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#") and ":" in raw:
            k, v = raw.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    meta["_body"] = body.lstrip("-").strip()
    return meta


def _gen_usage(base):
    """Riassunto per task generico (token e costo di listino) dal log unico logs\\uso.csv (motori.py, v0.5)."""
    try:
        return motori.per_task("generico")
    except Exception:
        return {}


def _gen_nota(t, base, done_ids):
    """Perche' un task in coda non parte ancora (in parole semplici)."""
    if t.get("approval_before", "").lower() == "leo" and t.get("approved", "no").lower() != "yes":
        return "aspetta il tuo OK (scrivi 'approved: yes' nel file del task)"
    for dep in [x.strip() for x in t.get("depends_on", "").strip("[]").split(",") if x.strip()]:
        if not any(i.startswith(dep) for i in done_ids):
            return "aspetta che finisca " + dep
    return "pronto: parte al prossimo giro del runner"


def gen_collect(src):
    base = src["_base"]
    tasks, domande = [], []
    use = _gen_usage(base)
    cartelle = {"queue": "in_coda", "done": "completato", "failed": "fallito", "incomplete": "incompleto", "blocked": "bloccato"}
    running = None
    lock = base / "runner.lock"
    if lock.exists():
        try:
            if time.time() - lock.stat().st_mtime < 4 * 3600:
                parts = read_text_any(lock).split()
                running = parts[-1] if len(parts) >= 3 else ""
        except Exception:
            pass
    done_ids = [p.name.replace(".task.md", "") for p in (base / "done").glob("*.task.md")] if (base / "done").exists() else []
    n_done = 0
    seen = set()
    for cart, stato in cartelle.items():
        d = base / cart
        if not d.exists():
            continue
        files = sorted(d.glob("*.task.md"), key=lambda p: p.stat().st_mtime, reverse=(cart != "queue"))
        for p in files:
            if cart == "done":
                n_done += 1
                if n_done > 15:
                    break
            try:
                t = _md_task(p)
            except Exception:
                continue
            tid = t.get("id") or p.name.replace(".task.md", "")
            if tid in seen:          # stessa id in piu' cartelle (es. fallito e poi rifatto): vale la versione piu' recente (coda > fatto > resto)
                continue
            seen.add(tid)
            u = use.get(tid) or {}
            st = stato
            nota = ""
            if cart == "queue":
                nota = _gen_nota(t, base, done_ids)
                if running and tid == running:
                    st, nota = "in_corso", "il runner ci sta lavorando adesso"
            elif cart == "done":
                nota = "completato" + (" · aspetta il tuo controllo" if t.get("approval_after", "").lower() == "leo" and t.get("approved", "no").lower() != "yes" else "")
            elif cart == "failed":
                nota = "non ha passato i controlli: vedi RUNNER.md nel progetto (agenti\\" + tid + ")"
            tok = sum(int(float(u.get(k) or 0)) for k in ("input_tokens", "cache_creation", "cache_read", "output_tokens"))
            costo = u.get("cost_usd")
            tasks.append({"id": tid, "sid": tid, "sorgente": src["id"], "dip": t.get("project") or src["id"],
                          "nome": agent_name(tid), "titolo": t.get("title") or tid,
                          "etichetta": t.get("tier", ""), "stato": st, "fase": None,
                          "inizio": None, "fine": (u.get("timestamp") or None) if st not in ("in_coda", "in_corso") else None,
                          "turni": int(u["num_turns"]) if (u.get("num_turns") or "").isdigit() else None,
                          "token": tok or None, "costo": float(costo) if costo else None, "nota": nota, "fasi": [],
                          "esito": None, "_cartella": str(p)})
    stop = base / "STOP"
    return {"tasks": tasks, "domande": domande, "quota": None,
            "controlli": [{"t": "File STOP", "d": "presente" if stop.exists() else "assente", "ok": not stop.exists()}],
            "stop": {"presente": stop.exists(), "percorso": str(stop)}, "runner_attivo": bool(running)}


def gen_task_detail(src, task_id):
    base = src["_base"]
    groups = {"input": [], "lavoro": [], "output": []}
    cartelle = []
    for cart in ("queue", "done", "failed", "incomplete", "blocked"):
        for p in (base / cart).glob("*.task.md") if (base / cart).exists() else []:
            try:
                t = _md_task(p)
            except Exception:
                continue
            if (t.get("id") or p.name.replace(".task.md", "")) != task_id:
                continue
            groups["input"].append(file_info(p, "Il task (istruzioni)"))
            prof = t.get("profile")
            if prof and (base / prof).exists():
                groups["input"].append(file_info(base / prof, "Profilo del progetto"))
            res = base / "results" / task_id
            for f in walk_files(res, depth=2) if res.exists() else []:
                groups["lavoro"].append(file_info(f, str(f.relative_to(res))))
            repo = Path(t["repo"]) if t.get("repo") else None
            if repo and repo.exists():
                cartelle.append(str(repo))
                for n in ("RAPPORTO.md", "RUNNER.md", "DECISIONS.md"):
                    f = repo / "agenti" / task_id / n
                    if f.exists():
                        groups["output"].append(file_info(f, n))
                al = [x.strip() for x in t.get("allowed", "").strip("[]").split(",") if x.strip()]
                for a in al:
                    f = repo / a
                    if f.exists() and not f.is_dir():
                        groups["output"].append(file_info(f, a))
            cartelle.append(str(res))
            return {"gruppi": groups, "cartelle": cartelle, "log": []}
    return {"gruppi": groups, "cartelle": [], "log": []}


# ------------------------------------------------------------------- stato
_cache = {"t": 0, "v": None}
_lock = threading.Lock()


def sources(cfg):
    return [s for s in cfg["sorgenti"] if s.get("attivo", True) and s["_base"].exists()]


def build_state(cfg):
    with _lock:
        if time.time() - _cache["t"] < 2 and _cache["v"]:
            return _cache["v"]
        out = {"adesso": iso(datetime.now()), "nome": cfg.get("nome", "Ufficio"), "soglia_stop_pct": cfg.get("soglia_stop_pct", 60), "dipartimenti": [],
               "task": [], "domande": [], "controlli": [], "quota": None, "recenti": [], "sorgenti": [], "errori": []}
        for s in sources(cfg):
            try:
                r = cv_collect(s) if s.get("tipo") == "cv_runner" else gen_collect(s)
                if s.get("tipo") == "cv_runner":
                    out["recenti"] += cv_recent(s)
            except Exception as e:
                import traceback
                traceback.print_exc()
                out["errori"].append(f"{s['id']}: {e}")
                continue
            dips = {t["dip"] for t in r["tasks"]} or {s["id"]}
            for d in sorted(dips):
                out["dipartimenti"].append({"id": d, "nome": s["nome"] if d == s["id"] else d, "sub": s.get("sub", ""),
                                            "colore": s.get("colore", "#7FA8FF"), "sorgente": s["id"]})
            out["task"] += r["tasks"]
            out["domande"] += r["domande"]
            out["controlli"] += r["controlli"]
            if r["quota"] and not out["quota"]:
                out["quota"] = r["quota"]
            out["sorgenti"].append({"id": s["id"], "nome": s["nome"], "tipo": s.get("tipo"), "stop": r["stop"],
                                    "runner_attivo": r["runner_attivo"], "radice": str(s["_base"]), "extra": r.get("extra")})
        for t in out["task"]:
            for k in [k for k in t if k.startswith("_")]:
                t.pop(k)
        out["recenti"].sort(key=lambda x: x.get("mtime") or "", reverse=True)
        out["recenti"] = out["recenti"][:12]
        _cache.update(t=time.time(), v=out)
        return out


def allowed(cfg, path):
    try:
        p = Path(path).resolve()
    except Exception:
        return None
    for s in sources(cfg):
        b = s["_base"]
        if p == b or b in p.parents:
            return p
    for b in [HERE.parent] + [Path(x["cartella"]) for x in UD.progetti() if x.get("cartella")]:
        try:
            b = b.resolve()
        except Exception:
            continue
        if p == b or b in p.parents:
            return p
    return UX.under(cfg, p)       # cartelle consultabili in piu' (solo vedere/aprire)


def reload_cfg(cfg):
    """Rilegge pannello_config.json e lo rende attivo subito, senza riavviare."""
    new = load_config()
    cfg.clear()
    cfg.update(new)
    _cache["t"] = 0


def chat_context(cfg):
    """Stato in breve per la chat: lavori, domande, pausa e il rapporto leggibile della coda."""
    out = []
    try:
        st = build_state(cfg)
        for t in st["task"][-25:]:
            out.append("TASK " + json.dumps({k: t.get(k) for k in ("id", "titolo", "stato", "fase", "sorgente", "nota") if t.get(k)}, ensure_ascii=False))
        for q in st["domande"][:15]:
            out.append("DOMANDA " + json.dumps({k: q.get(k) for k in ("id", "task", "sorgente", "testo", "domanda", "titolo") if q.get(k)}, ensure_ascii=False)[:500])
        for s in st["sorgenti"]:
            out.append(f"SORGENTE {s['id']} ({s['nome']}): agente {'al lavoro' if s['runner_attivo'] else 'fermo'}, pausa {'si' if (s.get('stop') or {}).get('presente') else 'no'}")
    except Exception as e:
        out.append(f"(stato non leggibile: {e})")
    try:
        for pj in UD.progetti():
            out.append("PROGETTO " + json.dumps({k: pj.get(k) for k in ("id", "nome", "priorita", "stato", "cartella", "frase")}, ensure_ascii=False)
                       + " piano: " + " | ".join(t.get("testo", "") for t in pj.get("piano") or []))
        for t in UD.gen_tasks()[:40]:
            out.append("TASK_GEN " + json.dumps({k: t.get(k) for k in ("id", "progetto", "titolo", "stato", "nota", "pct")}, ensure_ascii=False))
        c = comune.contatore()
        out.append(f"CONTATORE uso 5 ore: {c['pct']}% (100% = {c['token_100']} token pesati)")
    except Exception as e:
        out.append(f"(progetti non leggibili: {e})")
    for s in sources(cfg):
        if is_cv(s):
            try:
                S = cv_mod(s)
                for o in S.load()["offerte"][-30:]:
                    out.append("OFFERTA " + json.dumps({"id": o.get("id"), "titolo": S.label(o), "stato": o.get("stato"), "sede": o.get("sede"),
                                                      "link": o.get("url") or "(testo incollato)"}, ensure_ascii=False))
            except Exception:
                pass
            try:
                out.append("RAPPORTO:\n" + cv_mod(s).CODA_MD.read_text(encoding="utf-8")[:2500])
            except Exception:
                pass
            break
    return "\n".join(out)


def get_salute(cfg):
    """Salute degli agenti: durata, giri, rifacimenti, fermo. Solo avvisi, non ferma niente."""
    out = {"avvisi": [], "in_corso": None, "fasi": [], "ultimi": [], "rifacimenti": []}
    now = datetime.now()
    for src in sources(cfg):
        if not is_cv(src):
            continue
        S = cv_mod(src)
        st_ = S.load()
        imp = st_["impostazioni"]
        maxt = int(imp.get("turns") or 25)
        rows = read_uso(S)
        byph = {}
        for r in rows:
            byph.setdefault(r.get("phase") or "?", []).append(r)
        media = {}
        for ph, lst in byph.items():
            w = [num(x.get("wall_s")) for x in lst[-15:] if num(x.get("wall_s")) > 0]
            media[ph] = sum(w) / len(w) if w else 0
            out["fasi"].append({"fase": ph, "n": len(lst), "media_s": round(media[ph]),
                                "turni_medi": round(sum(num(x.get("turns")) for x in lst[-15:]) / max(1, len(lst[-15:])), 1)})
        for r in rows[-12:][::-1]:
            ph, w, tu = r.get("phase") or "?", num(r.get("wall_s")), num(r.get("turns"))
            flags = []
            if len(byph.get(ph, [])) >= 4 and media.get(ph) and w > 2 * media[ph] and w > 60:
                flags.append("lento")
            if tu >= 0.8 * maxt:
                flags.append("molti giri")
            if (r.get("status") or "ok") not in ("ok", "OK", ""):
                flags.append(str(r.get("status")))
            out["ultimi"].append({"quando": r.get("ended"), "fase": ph, "offerta": r.get("offer"), "durata_s": round(w), "turni": int(tu),
                                  "max_turni": maxt, "costo": round(num(r.get("cost_usd_listprice")), 3), "flags": flags})
        for x in out["ultimi"][:5]:
            if x["flags"]:
                out["avvisi"].append({"liv": "medio", "testo": f"{x['fase']} su {x['offerta']}: {', '.join(x['flags'])} ({x['durata_s']} s, {x['turni']}/{x['max_turni']} giri)"})
        for o in st_["offerte"]:
            if (o.get("giri") or 0) >= 2 and o.get("stato") != "scartata":
                out["rifacimenti"].append({"offerta": S.label(o), "giri": o.get("giri"), "stato": o.get("stato")})
                if (o.get("giri") or 0) >= 3:
                    out["avvisi"].append({"liv": "medio", "testo": f"{S.label(o)} rifatta {o.get('giri')} volte"})
        age = S.lock_age()
        if age is not None and age < 90:
            try:
                la = now.timestamp() - S.LOG_FILE.stat().st_mtime
            except Exception:
                la = None
            job = None
            try:
                parts = S.RUN_LOCK.read_text(encoding="utf-8").split()
                job = parts[1] if len(parts) > 1 else None
            except Exception:
                pass
            out["in_corso"] = {"job": job, "ultimo_segnale_s": round(la) if la is not None else None}
            if la is not None and la > 15 * 60:
                out["avvisi"].append({"liv": "alto", "testo": f"L'agente e' fermo da {round(la / 60)} minuti senza scrivere nel log"})
    out["feedback"] = UX.feedback_list()
    return out


def default_src(cfg):
    return next((s["id"] for s in sources(cfg) if is_cv(s)), "")


def edit_flow(cfg, testo):
    r = UX.edit_prepare(cfg, testo)
    if r.get("ok") and r.get("auto") and r.get("id"):
        a = UX.edit_apply(cfg, r["id"], lambda: reload_cfg(cfg))
        r["applicata"] = a
    return r


def exec_chat_action(cfg, a):
    """Esegue un'azione confermata usando le stesse funzioni dei pulsanti del pannello."""
    p = dict(a.get("parametri") or {})
    p["sorgente"] = a.get("sorgente") if find_src(cfg, a.get("sorgente")) else default_src(cfg)   # id sbagliato scritto dalla chat -> progetto candidature
    n = a["azione"]
    if n == "richiesta_pannello":
        t = str(p.get("testo") or "").strip()
        if not t:
            return {"ok": False, "msg": "Manca il testo della richiesta."}
        f = HERE / "richieste_pannello.md"
        new = not f.exists()
        with f.open("a", encoding="utf-8") as fh:
            if new:
                fh.write("# Richieste di modifica al pannello\n\nScritte dalla chat con la tua conferma. Si applicano dalla chat di Cowork.\n")
            fh.write(f"\n- [{datetime.now():%Y-%m-%d %H:%M}] DA FARE: {t}\n")
        return {"ok": True, "msg": "Richiesta registrata in richieste_pannello.md: la applico dalla chat di Cowork."}
    if n == "pausa":
        return act_stop(cfg, {**p, "attiva": True})
    if n == "riprendi":
        return act_stop(cfg, {**p, "attiva": False})
    if n == "direzione":
        p["ambito"] = p.get("ambito") or "tutti"
    if n == "aggiungi":
        p["url"] = p.get("url") or ""
        p["nota"] = p.get("nota") or ""
    if n == "nuova_task":
        return UD.task_nuova({**p, "origine": "chat pannello"})
    if n == "approva_task":
        return UD.task_approva(p)
    if n == "attiva_task":
        return UD.task_attiva(p)
    if n == "in_cima":
        return UD.in_cima(p)
    if n == "rispondi_agente":
        return UD.decisione_rispondi(p)
    if n == "consigli":
        return UD.consigli(p)
    if n == "revisione":
        return UD.revisione(p)
    fn = {"scout": act_scout, "aggiungi": act_add, "approva": act_approve, "approva_tutte": act_approve_all,
          "scarta": act_discard, "rifai": act_redo, "direzione": act_hint, "manutenzione": act_manutenzione,
          "nuove_aziende": act_nuove_aziende, "rispondi": act_answer}.get(n)
    if not fn:
        return {"ok": False, "msg": "Azione non permessa."}
    return fn(cfg, p)


# ------------------------------------------------------------------ azioni
def act_open(cfg, body):
    p = allowed(cfg, body.get("path", ""))
    if not p or not p.exists():
        return {"ok": False, "msg": "Percorso non trovato o fuori dalle cartelle degli agenti."}
    modo = body.get("modo", "apri")
    try:
        if os.name == "nt":
            if modo == "mostra" and p.is_file():
                subprocess.Popen(f'explorer /select,"{p}"')
            elif modo == "cartella" and p.is_file():
                os.startfile(str(p.parent))
            else:
                os.startfile(str(p))
        else:
            target = p.parent if (modo != "apri" and p.is_file()) else p
            subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", str(target)])
        return {"ok": True, "msg": "Aperto."}
    except Exception as e:
        return {"ok": False, "msg": f"Non riesco ad aprirlo: {e}"}


def find_src(cfg, sid):
    return next((s for s in sources(cfg) if s["id"] == sid), None)


def is_cv(s):
    return bool(s) and s.get("tipo") == "cv_runner"


def act_stop(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not s:
        return {"ok": False, "msg": "Sorgente sconosciuta."}
    stop = cv_mod(s).STOP_FILE if is_cv(s) else s["_base"] / "STOP"
    try:
        if body.get("attiva", True):
            stop.parent.mkdir(parents=True, exist_ok=True)
            stop.write_text("STOP creato dal pannello il " + iso(datetime.now()) + "\n", encoding="utf-8")
            return {"ok": True, "msg": "Coda in pausa: il lavoro in corso finisce, poi non parte altro."}
        if stop.exists():
            stop.unlink()
        return {"ok": True, "msg": "Pausa tolta: la coda riparte."}
    except Exception as e:
        return {"ok": False, "msg": f"Errore: {e}"}


def act_answer(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    risposta = (body.get("risposta") or "").strip()
    if not s or not risposta:
        return {"ok": False, "msg": "Manca la risposta."}
    if is_cv(s):
        S = cv_mod(s)
        res = {}

        def go(st_):
            q = S.answer_question(st_, str(body.get("domanda")), risposta)
            if not q:
                return
            o = S.find_offer(st_, q["offerta"])
            res["ok"] = True
            if o is None or S.open_questions(st_, o["id"]):
                return
            res["ultima"] = True
            if o["stato"] in ("approvata", "cv_pronto", "lettera"):
                if o.get("giri", 0) >= 4 and o["stato"] != "lettera":
                    res["limite"] = True
                    return
                S.redo(st_, o, "letter" if o["stato"] == "lettera" else "cv")
                res["riparte"] = True
        try:
            S.update(go)
        except Exception as e:
            return {"ok": False, "msg": f"Errore: {e}"}
        if not res.get("ok"):
            return {"ok": False, "msg": "Domanda non trovata: ricarica il pannello."}
        if res.get("riparte"):
            return {"ok": True, "msg": "Risposta salvata. Era l'ultima domanda: il lavoro riparte da solo (se la coda non e' in pausa)."}
        if res.get("limite"):
            return {"ok": True, "msg": "Risposta salvata. Ho gia' rifatto questa offerta 4 volte: non riparto da solo, usa Rifai se vuoi."}
        return {"ok": True, "msg": "Risposta salvata."}
    d = s["_base"] / "queue" / str(body.get("task"))
    try:
        rp = d / "risposte.json"
        cur = json.loads(rp.read_text(encoding="utf-8")) if rp.exists() else {}
        cur[str(body.get("domanda"))] = {"risposta": risposta, "quando": iso(datetime.now())}
        rp.write_text(json.dumps(cur, indent=1, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "msg": "Risposta salvata in risposte.json del task."}
    except Exception as e:
        return {"ok": False, "msg": f"Errore: {e}"}


def act_add(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not s:
        return {"ok": False, "msg": "Sorgente sconosciuta."}
    try:
        if is_cv(s):
            S = cv_mod(s)
            url, testo = (body.get("url") or "").strip(), (body.get("testo") or "").strip()
            if not url and not testo:
                return {"ok": False, "msg": "Metti un link oppure il testo dell'offerta."}
            if url and not url.lower().startswith("http"):
                return {"ok": False, "msg": "Il link deve iniziare con http."}
            nome = (body.get("nome") or body.get("nota") or "").strip()
            out = {}

            def go(st_):
                o, new = S.add_offer(st_, url=url, testo=testo if not url else "", nome=nome, nota=nome, stato="approvata", origine="manuale")
                if url and testo:
                    o["testo"] = testo
                out["new"] = new
                if new or o["stato"] in ("trovata", "approvata"):
                    S.advance(st_, o) if o["stato"] == "trovata" else S.enqueue(st_, "cv", o["id"])
            S.update(go)
            return {"ok": True, "msg": "Offerta aggiunta: analisi e CV partono da soli, un lavoro alla volta." if out.get("new")
                    else "Era gia' in lista: l'ho rimessa in coda per il CV."}
        tid = re.sub(r"[^A-Za-z0-9_-]+", "-", (body.get("id") or datetime.now().strftime("T-%Y%m%d-%H%M%S")))
        d = s["_base"] / "queue" / tid
        d.mkdir(parents=True, exist_ok=True)
        task = {"id": tid, "progetto": body.get("progetto") or s["id"], "titolo": body.get("titolo") or tid,
                "tier": body.get("tier", "small"), "stato": "da_approvare" if body.get("tier") == "large" else "in_coda",
                "istruzioni": body.get("istruzioni", ""), "input": body.get("input", [])}
        (d / "task.json").write_text(json.dumps(task, indent=1, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "msg": f"Task {tid} creato."}
    except Exception as e:
        return {"ok": False, "msg": f"Errore: {e}"}


def act_approve(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not s:
        return {"ok": False, "msg": "Sorgente sconosciuta."}
    if is_cv(s):
        S = cv_mod(s)
        res = {}

        def go(st_):
            o = S.find_offer(st_, str(body.get("id")))
            if o is None:
                return
            if S.open_questions(st_, o["id"]):
                res["domande"] = True
                return
            res["fase"] = S.advance(st_, o)
        S.update(go)
        if res.get("domande"):
            return {"ok": False, "msg": "Prima rispondi alle domande di questa offerta."}
        if not res.get("fase"):
            return {"ok": False, "msg": "Niente da approvare per questa voce."}
        return {"ok": True, "msg": ("Approvato: analisi e CV partono da sole," if res["fase"] == "cv" else "Approvato: la lettera parte da sola,") + " un lavoro alla volta."}
    tj = s["_base"] / "queue" / str(body.get("id")) / "task.json"
    try:
        j = json.loads(read_text_any(tj))
        j["stato"], j["approvato"] = "in_coda", iso(datetime.now())
        tj.write_text(json.dumps(j, indent=1, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "msg": "Approvato."}
    except Exception as e:
        return {"ok": False, "msg": f"Errore: {e}"}


def act_approve_all(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    n = [0]

    def go(st_):
        for o in st_["offerte"]:
            if o["stato"] in ("trovata", "cv_pronto") and not S.open_questions(st_, o["id"]):
                if S.last_job(st_, o["id"]) and S.last_job(st_, o["id"])["stato"] in ("in_attesa", "in_corso"):
                    continue
                if S.advance(st_, o):
                    n[0] += 1
    S.update(go)
    return {"ok": True, "msg": f"Approvate {n[0]} voci." if n[0] else "Niente da approvare (o hanno domande aperte)."}


def act_discard(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)

    def go(st_):
        o = S.find_offer(st_, str(body.get("id")))
        if o is not None:
            o["stato"] = "scartata"
            S.offer_log(o, "scartata da Leonardo")
            for j in st_["coda"]:
                if j.get("offerta") == o["id"] and j["stato"] == "in_attesa":
                    j["stato"], j["esito"] = "errore", "scartata"
    S.update(go)
    return {"ok": True, "msg": "Offerta scartata (i file gia' consegnati restano in output)."}


def act_scout(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    S.update(lambda st_: S.enqueue(st_, "scout"))
    return {"ok": True, "msg": "Scout in coda: cerca offerte vere, poi si ferma e aspetta il tuo OK."}


def act_redo(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    res = {}

    def go(st_):
        o = S.find_offer(st_, str(body.get("id")))
        if o is None:
            return
        if (body.get("fase") or "cv").startswith("l") and not o.get("tag"):
            res["manca"] = True
            return
        S.redo(st_, o, body.get("fase") or "cv")
        res["ok"] = True
    S.update(go)
    if res.get("manca"):
        return {"ok": False, "msg": "La lettera si puo' rifare solo dopo il CV."}
    return {"ok": bool(res.get("ok")), "msg": "Rifacimento in coda: sovrascrive gli stessi file." if res.get("ok") else "Offerta non trovata."}


def act_hint(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    testo = (body.get("testo") or "").strip()
    if not is_cv(s):
        return {"ok": False, "msg": "Direzione NON salvata: progetto non trovato (le direzioni valgono solo per le candidature)."}
    if not testo:
        return {"ok": False, "msg": "Scrivi la direzione."}
    S = cv_mod(s)

    def go(st_):
        amb = body.get("ambito") or ""
        if amb not in S.HINT_AMBITI and S.find_offer(st_, amb) is None:
            return {"ok": False, "msg": "Scegli dove vale la direzione (scout, CV, lettera, tutte le fasi o una offerta)."}
        st_["hint"].append({"id": S.nid(st_, "h"), "ambito": amb, "testo": testo, "data": S.now_iso()})
    r = S.update(go)
    if r:
        return r
    return {"ok": True, "msg": "Direzione salvata: vale solo dove l'hai indicato."}


def act_hint_remove(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    S.update(lambda st_: st_.__setitem__("hint", [h for h in st_["hint"] if h["id"] != body.get("id")]))
    return {"ok": True, "msg": "Direzione tolta."}


# ------------------------------------------- mappa, registro, percorsi, manutenzione
def act_enqueue_aux(cfg, body, tipo, msg):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    S.update(lambda st_: S.enqueue(st_, tipo))
    return {"ok": True, "msg": msg}


def act_manutenzione(cfg, body):
    return act_enqueue_aux(cfg, body, "manutenzione", "Manutenzione in coda: controlla link e coerenza, senza usare token.")


def act_nuove_aziende(cfg, body):
    return act_enqueue_aux(cfg, body, "nuove_aziende", "Ricerca di nuove aziende in coda: un agente le propone, tu le rivedi nella Mappa.")


def act_impostazione(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    k = body.get("chiave")
    if k in ("effort", "letter_effort", "scout_effort"):
        v = str(body.get("valore"))
        if v not in ("low", "medium", "high"):
            return {"ok": False, "msg": "Livello non valido (low, medium o high)."}
        S.update(lambda st_: st_["impostazioni"].__setitem__(k, v))
        return {"ok": True, "msg": "Livello di sforzo cambiato: vale dal prossimo lavoro."}
    if k != "scout_b":
        return {"ok": False, "msg": "Impostazione sconosciuta."}
    S.update(lambda st_: st_["impostazioni"].__setitem__("scout_b", bool(body.get("valore"))))
    return {"ok": True, "msg": "Fatto: lo scout " + ("controlla anche le aziende B." if body.get("valore") else "controlla solo le aziende A.")}


def act_mappa_set(cfg, body):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    campo, valore = body.get("campo"), body.get("valore")
    if campo not in ("status", "priority", "notes"):
        return {"ok": False, "msg": "Campo non modificabile."}
    if campo == "status" and valore not in ("Da esplorare", "Monitorando", "Candidato", "Colloquio", "Offerta", "Scartato"):
        return {"ok": False, "msg": "Stato non valido."}
    if campo == "priority" and valore not in ("A", "B", "C"):
        return {"ok": False, "msg": "Priorita' non valida."}
    res = {}

    def go(st_):
        c = st_["mappa"].get(str(body.get("id")))
        if c is None:
            return
        res["ok"] = True
        S.map_set(st_, c["id"], campo, valore, "lui", "modificato nel pannello")
        c["nuova"] = False
    S.update(go)
    auto_conferma_mappa(S)
    return {"ok": bool(res.get("ok")), "msg": "Salvato." if res.get("ok") else "Azienda non trovata."}


def auto_conferma_mappa(S):
    # le modifiche alla mappa si applicano da sole: restano nel registro, ma non aspettano la conferma
    def go(st_):
        for r in st_["registro"]:
            if r["stato"] == "attivo" and r["tipo"] in ("mappa", "mappa_nuova"):
                r["stato"] = "ok"
                if r["tipo"] == "mappa_nuova" and r["oggetto"] in st_["mappa"]:
                    st_["mappa"][r["oggetto"]]["nuova"] = False
    if any(r["stato"] == "attivo" and r["tipo"] in ("mappa", "mappa_nuova") for r in S.load()["registro"]):
        S.update(go)


def act_registro(cfg, body, cosa):
    s = find_src(cfg, body.get("sorgente"))
    if not is_cv(s):
        return {"ok": False, "msg": "Solo per le candidature."}
    S = cv_mod(s)
    res = {}

    def go(st_):
        if cosa == "annulla":
            res["ok"], res["msg"] = S.reg_undo(st_, str(body.get("id")))
        else:
            r = next((x for x in st_["registro"] if x["id"] == str(body.get("id"))), None)
            if r and r["stato"] == "attivo":
                r["stato"] = "ok"
                if r["tipo"] == "mappa_nuova" and r["oggetto"] in st_["mappa"]:
                    st_["mappa"][r["oggetto"]]["nuova"] = False
                res["ok"], res["msg"] = True, "Confermata."
            else:
                res["ok"], res["msg"] = False, "Modifica non trovata o gia' gestita."
    S.update(go)
    return res


def act_annulla(cfg, body):
    return act_registro(cfg, body, "annulla")


def act_conferma(cfg, body):
    return act_registro(cfg, body, "conferma")


def get_mappa(cfg):
    for s in sources(cfg):
        if is_cv(s):
            S = cv_mod(s)
            auto_conferma_mappa(S)
            st_ = S.load()
            return {"sorgente": s["id"], "aziende": S.map_view(st_), "scout_b": bool(st_["impostazioni"].get("scout_b"))}
    return {"aziende": []}


def spiega_reg(r, nome):
    # spiegazione semplice di una voce del registro; se la voce ne ha gia' una scritta, vale quella
    if r.get("spiegazione"):
        return str(r["spiegazione"])

    def corto(v):
        v = " ".join(str(v).split())
        return v if len(v) <= 80 else v[:77] + "..."
    chi = "da te" if r.get("chi") == "lui" else "da un agente o dal programma"
    if r["tipo"] == "mappa_nuova":
        return ("Aggiunta l'azienda %s alla Mappa aziende, proposta %s: serve ad allargare l'elenco delle aziende dove cercare lavoro."
                % (nome, chi))
    if r["tipo"] == "mappa":
        campi = {"status": "lo stato", "priority": "la priorità", "notes": "le note"}
        campo = campi.get(r.get("campo"), "«%s»" % r.get("campo"))
        prima = "vuoto" if r.get("prima") is None else corto(r["prima"])
        return ("Cambiato %s dell'azienda %s nella Mappa aziende, %s: da «%s» a «%s». Serve a tenere aggiornato a che punto sei con questa azienda."
                % (campo, nome, chi, prima, corto(r.get("dopo", ""))))
    if r["tipo"] == "baseline":
        return ("Aggiunta una riga nella sezione AUTO della tua scheda di base del CV, scritta %s: serve a far usare questo dato nelle candidature."
                % chi)
    return "Modifica a %s fatta %s%s." % (nome, chi, (": " + corto(r["motivo"])) if r.get("motivo") else "")


def get_registro(cfg):
    for s in sources(cfg):
        if is_cv(s):
            S = cv_mod(s)
            auto_conferma_mappa(S)
            st_ = S.load()
            names = {c["id"]: c.get("name") for c in st_["mappa"].values()}
            rows = []
            for r in reversed(st_["registro"][-200:]):
                d = dict(r)
                if r["tipo"] in ("mappa", "mappa_nuova"):
                    d["oggetto_nome"] = names.get(r["oggetto"], r["oggetto"])
                else:
                    o = S.find_offer(st_, r["oggetto"])
                    d["oggetto_nome"] = S.label(o) if o else r["oggetto"]
                d["spiegazione"] = spiega_reg(r, d["oggetto_nome"])
                rows.append(d)
            return {"sorgente": s["id"], "righe": rows}
    return {"righe": []}


def get_percorsi(cfg):
    out = []
    for s in sources(cfg):
        if not is_cv(s):
            continue
        S = cv_mod(s)
        b = s["_base"]

        def add(nome, p, desc, kind="file"):
            p = Path(p)
            out.append({"nome": nome, "p": str(p), "desc": desc, "esiste": p.exists(), "dir": p.is_dir() or kind == "dir"})
        add("Baseline CV (fatti)", S.doc_path("CV_description_baseline.txt"), "L'unica baseline. In fondo, sezione AUTO: le righe scritte da pannello e agenti, riconoscibili dall'etichetta [AUTO].")
        add("Baseline lettere", S.doc_path("cover letter baseline.md"), "Stile ed esempi delle lettere.")
        add("Framework", S.doc_path("Job search framework.md"), "Processo, regole e formato. Solo tu lo modifichi.")
        add("Stato (tutto in un file)", S.STATE_FILE, "Offerte, domande, direzioni, coda, mappa aziende, registro modifiche.")
        add("Rapporto leggibile", S.CODA_MD, "Si rigenera da solo: da fare, offerte, mappa, registro.")
        add("Log", S.LOG_FILE, "Cosa e' successo, riga per riga.")
        add("Consumo (log unico)", motori.LOG, "Una riga per ogni chiamata a un modello, di tutti i progetti.")
        add("Consegne (CV e lettere)", S.OUT, "Una cartella per offerta: Azienda_Ruolo_LINGUA.", "dir")
        add("Archivio (storico)", S.ARCHIVIO, "Vecchi output e materiale storico. Gli agenti possono solo leggerlo.", "dir")
        add("Programma (runner)", b / "runner", "Il codice. Un solo runner, mai una versione nuova.", "dir")
        add("Documenti personali", getattr(S, "DOCS_HOME", b) / "certifications_documents", "Certificati e diplomi.", "dir")
    return {"voci": out}


# -------------------------------------------------------------------- HTTP

# ---------------- meteo (Open-Meteo, gratuito, senza chiave) ----------------
CITTA_DEFAULT = {
    "Jaca": (42.57, -0.55), "Salisburgo": (47.81, 13.04), "Torino": (45.07, 7.69),
}
_meteo_cache = {}


def wmo_cat(code):
    if code in (0, 1): return "sereno"
    if code in (2, 3): return "nuvoloso"
    if code in (45, 48): return "nebbia"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82): return "pioggia"
    if code in (71, 73, 75, 77, 85, 86): return "neve"
    if code in (95, 96, 99): return "temporale"
    return "nuvoloso"


def meteo_for(cfg, citta):
    cities = dict(CITTA_DEFAULT)
    for c in (cfg.get("meteo", {}) or {}).get("citta", []):
        try: cities[c["nome"]] = (float(c["lat"]), float(c["lon"]))
        except Exception: pass
    if citta not in cities:
        return {"ok": False, "msg": "Citta sconosciuta", "citta": citta, "citta_elenco": sorted(cities)}
    now = time.time()
    hit = _meteo_cache.get(citta)
    if hit and now - hit[0] < 900:
        return hit[1]
    lat, lon = cities[citta]
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&current=temperature_2m,weather_code,"
           "wind_speed_10m,is_day&timezone=auto" % (lat, lon))
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=6) as r:
            d = json.loads(r.read().decode("utf-8"))
        cur = d["current"]
        hh, mm = cur["time"][11:16].split(":")
        out = {"ok": True, "citta": citta, "cat": wmo_cat(cur["weather_code"]), "temp": cur["temperature_2m"],
               "vento": cur.get("wind_speed_10m"), "hour": int(hh) + int(mm) / 60, "giorno": bool(cur.get("is_day")),
               "citta_elenco": sorted(cities)}
    except Exception as e:
        if hit: return hit[1]
        return {"ok": False, "msg": "Meteo non raggiungibile: %s" % e, "citta": citta, "citta_elenco": sorted(cities)}
    _meteo_cache[citta] = (now, out)
    return out


class Handler(BaseHTTPRequestHandler):
    cfg = None
    port = 0

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8", extra=None):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _host_ok(self):
        return (self.headers.get("Host") or "").split(":")[0] in ("127.0.0.1", "localhost")

    def _token_ok(self, q):
        got = self.headers.get("X-Token") or (q.get("t") or [""])[0]
        return secrets.compare_digest(got.encode("utf-8", "replace"), TOKEN.encode("utf-8"))

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if not self._host_ok():
            return self._send(403, {"ok": False})
        if u.path == "/ping":
            return self._send(200, b"ufficio", "text/plain; charset=utf-8")
        if u.path in ("/", "/index.html", "/mondo"):
            nome = {"/mondo": "mondo.html"}.get(u.path, "ufficio.html")
            try:
                html = (HERE / nome).read_text(encoding="utf-8").replace("__TOKEN__", TOKEN)
            except Exception as e:
                return self._send(500, f"Manca {nome}: {e}".encode(), "text/plain; charset=utf-8")
            return self._send(200, html.encode("utf-8"), "text/html; charset=utf-8")
        if u.path in ("/mondo.js",) or (u.path.startswith("/tema_") and u.path.endswith(".js")):
            f = HERE / u.path.lstrip("/")
            if f.parent == HERE and f.is_file():
                return self._send(200, f.read_bytes(), "application/javascript; charset=utf-8")
            return self._send(404, {"ok": False})
        if u.path.startswith("/immagini/"):
            base = (HERE / "immagini").resolve()
            f = (HERE / u.path.lstrip("/")).resolve()
            ct = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(f.suffix.lower())
            if ct and base in f.parents and f.is_file():
                return self._send(200, f.read_bytes(), ct)
            return self._send(404, {"ok": False})
        if not self._token_ok(q):
            return self._send(403, {"ok": False, "msg": "Codice non valido: riapri il pannello dal file .bat."})
        try:
            if u.path == "/api/meteo":
                return self._send(200, meteo_for(self.cfg, (q.get("citta") or [""])[0]))
            if u.path == "/api/stato":
                return self._send(200, build_state(self.cfg))
            if u.path == "/api/ufficio":
                return self._send(200, UD.stato_ufficio(self.cfg))
            if u.path == "/api/vecchio":
                c, m = UD.vecchio_elenco()
                return self._send(200, {"cancella": c, "sposta": m})
            if u.path == "/api/task2":
                return self._send(200, UD.task_dettaglio((q.get("id") or [""])[0]))
            if u.path == "/api/mappa":
                return self._send(200, get_mappa(self.cfg))
            if u.path == "/api/registro":
                return self._send(200, get_registro(self.cfg))
            if u.path == "/api/modifica_diff":
                return self._send(200, UX.edit_diff((q.get("id") or [""])[0]))
            if u.path == "/api/salute":
                return self._send(200, get_salute(self.cfg))
            if u.path == "/api/config":
                return self._send(200, UX.public_config(self.cfg))
            if u.path == "/api/chat":
                return self._send(200, UX.chat_status(self.cfg))
            if u.path == "/api/percorsi":
                return self._send(200, get_percorsi(self.cfg))
            if u.path == "/api/task":
                tid = (q.get("id") or [""])[0]
                for s in sorted(sources(self.cfg), key=lambda x: x.get("tipo") == "cv_runner"):   # prima i task generici: quello delle candidature risponde sempre qualcosa
                    if s.get("tipo") == "cv_runner":
                        det = cv_task_detail(s, tid)
                        if any(det["gruppi"].values()) or det["log"]:
                            return self._send(200, det)
                    elif s.get("tipo") != "cv_runner":
                        det = gen_task_detail(s, tid)
                        if any(det["gruppi"].values()):
                            return self._send(200, det)
                return self._send(200, {"gruppi": {"input": [], "lavoro": [], "output": []}, "cartelle": [], "log": []})
            if u.path == "/api/dir":
                p = allowed(self.cfg, (q.get("p") or [""])[0])
                if not p or not p.is_dir():
                    return self._send(404, {"ok": False})
                items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))[:200]
                return self._send(200, {"p": str(p), "su": str(p.parent) if allowed(self.cfg, p.parent) else None,
                                        "voci": [file_info(i) for i in items]})
            if u.path == "/api/testo":
                p = allowed(self.cfg, (q.get("p") or [""])[0])
                if not p or not p.is_file():
                    return self._send(404, {"ok": False})
                if p.stat().st_size > 400_000:
                    return self._send(200, {"testo": "(file troppo grande per l'anteprima: usa Apri)", "troncato": True})
                return self._send(200, {"testo": read_text_any(p)})
            if u.path == "/api/file":
                p = allowed(self.cfg, (q.get("p") or [""])[0])
                if not p or not p.is_file():
                    return self._send(404, {"ok": False})
                ct = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
                return self._send(200, p.read_bytes(), ct, {"Content-Disposition": "inline"})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._send(500, {"ok": False, "msg": str(e)})
        self._send(404, {"ok": False})

    def do_POST(self):
        u = urlparse(self.path)
        if not self._host_ok() or not self._token_ok({}):
            return self._send(403, {"ok": False, "msg": "Codice non valido."})
        origin = self.headers.get("Origin")
        if origin and urlparse(origin).netloc.split(":")[0] not in ("127.0.0.1", "localhost"):
            return self._send(403, {"ok": False})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except Exception:
            return self._send(400, {"ok": False, "msg": "Richiesta non valida."})
        fn = {"/api/apri": act_open, "/api/stop": act_stop, "/api/rispondi": act_answer,
              "/api/aggiungi": act_add, "/api/approva": act_approve, "/api/approva_tutte": act_approve_all,
              "/api/scarta": act_discard, "/api/scout": act_scout, "/api/rifai": act_redo,
              "/api/hint": act_hint, "/api/hint_togli": act_hint_remove,
              "/api/manutenzione": act_manutenzione, "/api/nuove_aziende": act_nuove_aziende,
              "/api/impostazione": act_impostazione, "/api/mappa_set": act_mappa_set,
              "/api/annulla": act_annulla, "/api/conferma": act_conferma,
              "/api/config_set": lambda c, b: UX.set_config(c, b, lambda: reload_cfg(c)),
              "/api/chat_invia": lambda c, b: UX.chat_send(c, b.get("testo", ""), chat_context(c), str(b.get("vista", ""))[:200], default_src(c)),
              "/api/chat_azione": lambda c, b: UX.chat_azione(c, b, lambda a: exec_chat_action(c, a)),
              "/api/chat_sblocca": lambda c, b: UX.chat_sblocca(c),
              "/api/chat_modifica": lambda c, b: edit_flow(c, str(b.get("testo", ""))),
              "/api/modifica_applica": lambda c, b: UX.edit_apply(c, str(b.get("id", "")), lambda: reload_cfg(c)),
              "/api/modifica_scarta": lambda c, b: UX.edit_discard(c, str(b.get("id", ""))),
              "/api/ripristina": lambda c, b: UX.restore_backup(lambda: reload_cfg(c)),
              "/api/pulizia": lambda c, b: UX.pulizia(),
              "/api/task_nuova": lambda c, b: UD.task_nuova(b), "/api/task_approva": lambda c, b: UD.task_approva(b),
              "/api/task_attiva": lambda c, b: UD.task_attiva(b), "/api/task_sospendi": lambda c, b: UD.task_sospendi(b),
              "/api/task_rifai": lambda c, b: UD.task_rifai(b), "/api/in_cima": lambda c, b: UD.in_cima(b),
              "/api/decisione": lambda c, b: UD.decisione_rispondi(b), "/api/progetto_salva": lambda c, b: UD.progetto_salva(b),
              "/api/progetto_archivia": lambda c, b: UD.progetto_archivia(b), "/api/tappa": lambda c, b: UD.tappa_stato(b),
              "/api/avvia_agenti": lambda c, b: UD.avvia_dispatcher(), "/api/spegni": lambda c, b: spegni(), "/api/riavvia": lambda c, b: riavvia(),
              "/api/domanda": lambda c, b: UD.domanda_rispondi(b),
              "/api/consigli": lambda c, b: UD.consigli(b), "/api/revisione": lambda c, b: UD.revisione(b),
              "/api/task_scarta": lambda c, b: UD.task_scarta(b), "/api/scheda_fatto": lambda c, b: UD.scheda_fatto(b),
              "/api/scheda_crea": lambda c, b: UD.scheda_crea(b), "/api/vecchio_elimina": lambda c, b: UD.vecchio_elimina()}.get(u.path)
        if not fn:
            return self._send(404, {"ok": False})
        try:
            res = fn(self.cfg, body)
        except Exception as e:
            res = {"ok": False, "msg": f"Errore: {e}"}
        _cache["t"] = 0
        if res.get("ok") and u.path in ("/api/task_nuova", "/api/task_approva", "/api/task_attiva", "/api/task_rifai", "/api/in_cima",
                                        "/api/decisione", "/api/approva", "/api/approva_tutte", "/api/scout", "/api/rifai", "/api/aggiungi",
                                        "/api/rispondi", "/api/stop", "/api/manutenzione", "/api/nuove_aziende", "/api/domanda",
                                        "/api/consigli", "/api/revisione"):
            try:
                UD.avvia_dispatcher()
            except Exception:
                pass
        if u.path in ("/api/scarta", "/api/rifai") and res.get("ok") and (body.get("motivo") or body.get("tag")):
            try:
                fase = str(body.get("fase") or "")
                amb = "scout" if u.path == "/api/scarta" else ("lettera" if fase.startswith("l") else "cv")
                regola = bool(body.get("regola")) and bool(str(body.get("motivo") or "").strip())
                e = {"quando": f"{datetime.now():%Y-%m-%d %H:%M}", "azione": "scarta" if u.path == "/api/scarta" else "rifai " + (fase or "cv"),
                     "id": str(body.get("id", "")), "titolo": str(body.get("titolo", ""))[:120], "tag": [str(t)[:60] for t in (body.get("tag") or [])][:6],
                     "motivo": str(body.get("motivo") or "")[:600], "regola": False}
                if regola:
                    h = act_hint(self.cfg, {"sorgente": body.get("sorgente"), "ambito": amb,
                                             "testo": f"[AUTO {datetime.now():%Y-%m-%d} | feedback di Leonardo dopo un rifiuto di '{e['titolo']}'] {e['motivo']}"})
                    e["regola"] = bool(h.get("ok"))
                UX.feedback_add(e)
            except Exception:
                pass
        if u.path not in ("/api/spegni", "/api/riavvia", "/api/chat_invia", "/api/chat_azione", "/api/chat_sblocca", "/api/config_set", "/api/apri", "/api/chat_modifica", "/api/modifica_applica", "/api/modifica_scarta", "/api/ripristina", "/api/pulizia"):
            try:
                UX.log(f"- AZIONE dal pannello {datetime.now():%Y-%m-%d %H:%M} · {u.path} {json.dumps({k: v for k, v in body.items() if k in ('sorgente', 'id', 'url', 'fase', 'attiva', 'ambito', 'chiave', 'valore')}, ensure_ascii=False)} -> {'ok' if res.get('ok') else 'NO'}: {str(res.get('msg', ''))[:160]}")
            except Exception:
                pass
        self._send(200, res)


def spegni():
    UX.log(f"- UFFICIO spento dal pannello {datetime.now():%Y-%m-%d %H:%M} (gli agenti continuano con l'attivita' di Windows)")
    threading.Timer(0.6, lambda: os._exit(0)).start()
    return {"ok": True, "msg": "Ufficio spento. Gli agenti continuano a lavorare da soli; per rivederli usa l'icona sul desktop."}


def riavvia():
    """Riavvia il server (serve dopo una modifica ai file .py): ne lancia uno nuovo invisibile e chiude questo."""
    exe = Path(sys.executable)
    if os.name == "nt" and exe.name.lower() == "python.exe" and (exe.parent / "pythonw.exe").exists():
        exe = exe.parent / "pythonw.exe"
    kw = {"creationflags": 0x08000000} if os.name == "nt" else {}
    subprocess.Popen([str(exe), str(HERE / "pannello_server.py"), "--riavvio", "--no-browser"], cwd=str(HERE),
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)
    UX.log(f"- UFFICIO riavviato dal pannello {datetime.now():%Y-%m-%d %H:%M}")
    threading.Timer(0.6, lambda: os._exit(0)).start()
    return {"ok": True, "msg": "Riavvio in corso: la pagina si ricarica da sola."}


def gia_aperto(port):
    """Se l'Ufficio e' gia' acceso, apre solo il browser e non ne avvia un secondo."""
    import urllib.request
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/ping", timeout=2) as r:
            return r.read() == b"ufficio"
    except Exception:
        return False


def main():
    if sys.stdout is None:            # avviato senza finestra (pythonw): i messaggi vanno in server.log
        sys.stdout = sys.stderr = open(HERE / "server.log", "a", encoding="utf-8", buffering=1)
        print(f"\n=== avvio {datetime.now():%Y-%m-%d %H:%M:%S} ===")
    if "--riavvio" in sys.argv:
        time.sleep(2.5)               # aspetta che il server vecchio liberi la porta
    cfg = load_config()
    if gia_aperto(int(cfg.get("porta", 8765))):
        if "--no-browser" not in sys.argv:
            webbrowser.open(f"http://127.0.0.1:{int(cfg.get('porta', 8765))}/")
        return
    srv = None
    port = int(cfg.get("porta", 8765))
    for p in range(port, port + 10):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if not srv:
        sys.exit("ERRORE: nessuna porta libera tra %d e %d." % (port, port + 9))
    Handler.cfg, Handler.port = cfg, port
    UD.init(sources=lambda: sources(cfg), cv_mod=cv_mod, cv_collect=cv_collect, log=print)
    try:
        UX.pulizia()
    except Exception:
        pass
    threading.Thread(target=dispatch_loop, args=(cfg,), daemon=True).start()
    act = sources(cfg)
    print("=" * 60)
    print(" Ufficio - pannello pronto (un agente alla volta)")
    print(f" Indirizzo: http://127.0.0.1:{port}/")
    print(" Cartelle lette: " + (", ".join(f"{s['nome']} ({s['_base']})" for s in act) or "NESSUNA (controlla pannello_config.json)"))
    print(" Lascia questa finestra aperta. Per chiudere il pannello chiudila.")
    print("=" * 60)
    if "--no-browser" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(f"http://127.0.0.1:{port}/")).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
