#!/usr/bin/env python3
"""
runner.py - il motore delle candidature. UN solo programma, UN solo nome (mai runner_v9).

Come funziona (a gate, un agente alla volta):
  scout   cerca offerte vere nelle aziende a priorita' A         -> le offerte restano "trovate" e aspettano il tuo OK
  cv      analisi + CV_description (+ una correzione se serve)   -> si ferma: "CV pronto", aspetta il tuo OK
  letter  lettera (+ una correzione se serve)                    -> "pronta"
Domande e dubbi dell'agente vanno nel pannello (non in chat). Quando rispondi, il lavoro riparte da solo.

Dove sta cosa (tutto dentro la cartella CV):
  Job search framework.md, CV_description_baseline.txt, cover letter baseline.md   i 3 documenti, MAI copiati
  runner\\        questo programma
  stato\\         stato.json (la memoria), coda.md (rapporto leggibile), log.txt (consumo: ..\\..\\logs\\uso.csv), lavoro\\ (si svuota a ogni lavoro)
  output\\<Azienda>_<lingua>\\   solo CV e lettera, si sovrascrivono ai rifacimenti

Uso da prompt dei comandi (nella cartella runner):
  python runner.py coda                    mostra offerte, domande e coda
  python runner.py scout                   cerca offerte (poi si ferma e aspetta il tuo OK)
  python runner.py aggiungi <link>         aggiunge un'offerta e prepara analisi + CV
  python runner.py avanti <id|tutte>       approva il passo successivo (CV, poi lettera) e lavora
  python runner.py rifai <id> cv|lettera   rifa' una fase
  python runner.py lavora                  svuota la coda, un lavoro alla volta, poi si ferma
Il pannello fa le stesse cose con i pulsanti (parte con run.bat). Se non lavora nessuno, nessun token.
"""
import argparse, json, os, re, shutil, stat, subprocess, sys, threading, unicodedata
from datetime import datetime
from pathlib import Path

import state as st
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import motori  # l'unico punto da cui passano le chiamate ai modelli + log unico logs\uso.csv (v0.5)
import comune  # regole condivise: un agente alla volta tra progetti, limite di Claude, contatore d'uso (04/10)
import checks
import fetcher

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

log = st.log
CV_TOOLS = "Read,Write,Edit,Glob,Grep"


class JobError(Exception):
    pass


class LimitReached(JobError):
    pass


# ----------------------------------------------------------------- utilita'
def fmt_s(s):
    s = int(round(s))
    return f"{s // 60}m{s % 60:02d}s"


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


def slugify(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:40] or "offer"


def find_claude():
    p = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if not p:
        raise JobError("comando 'claude' non trovato nel PATH")
    return p


def clean_env():
    env = dict(os.environ)
    if env.pop("ANTHROPIC_API_KEY", None):
        log("ATTENZIONE: ANTHROPIC_API_KEY era impostata, la ignoro per usare l'abbonamento.")
    return env


def preflight(claude, env):
    """Controlla quali opzioni esistono nella versione di claude installata (nessun token usato)."""
    r = subprocess.run([claude, "--help"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, stdin=subprocess.DEVNULL, timeout=60)
    h = r.stdout + r.stderr
    v = subprocess.run([claude, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=env, stdin=subprocess.DEVNULL, timeout=60)
    log(f"claude versione: {v.stdout.strip() or '?'}")
    missing = [f for f in ("--output-format", "--model", "--allowedTools") if f not in h]
    if missing:
        raise JobError(f"opzioni non trovate in 'claude --help': {missing}")
    caps = set()
    for flag, name in (("--effort", "effort"), ("--restricted", "restricted"), ("--permission-prompts", "permission-prompts"),
                       ("--add-dir", "add-dir")):
        if flag in h:
            caps.add(name)
    return caps


def parse_json(stdout):
    s = stdout.strip()
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


def session_log_tokens(session_id):
    if not session_id:
        return {}
    try:
        files = list((Path.home() / ".claude" / "projects").glob(f"*/{session_id}.jsonl"))
        if not files:
            return {}
        msgs = {}
        for line in files[0].read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except Exception:
                continue
            m = o.get("message") or {}
            u = m.get("usage")
            if o.get("type") == "assistant" and u:
                msgs[m.get("id") or o.get("uuid")] = u
        tot = {"input": 0, "cache_creation": 0, "cache_read": 0, "output": 0}
        for u in msgs.values():
            tot["input"] += u.get("input_tokens", 0) or 0
            tot["cache_creation"] += u.get("cache_creation_input_tokens", 0) or 0
            tot["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
            tot["output"] += u.get("output_tokens", 0) or 0
        return tot
    except Exception:
        return {}


def keep_awake(on):
    if os.name != "nt":
        return
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | (0x00000001 if on else 0))
    except Exception:
        pass


def _rm_ro(func, path, exc):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass


# ------------------------------------------------------------ contesto agenti
class Ctx:
    """Come l'agente raggiunge i 3 documenti: 'adddir' = li legge dove stanno (nessuna copia);
    'copy' = piano B, copia di sola lettura DENTRO la cartella di lavoro (che si svuota a ogni lavoro)."""

    def __init__(self, a, S):
        self.a, self.S = a, S
        self.claude = None
        self.env = None
        self.caps = set()
        self.mode = "copy"
        self.paths = {n: st.doc_path(n) for n in st.DOCS}

    def setup(self):
        if self.a.dry_run and not os.environ.get("CLAUDE_BIN") and not shutil.which("claude"):
            self.claude, self.env, self.caps = "claude", dict(os.environ), {"add-dir"}
        else:
            self.claude = find_claude()
            self.env = clean_env()
            self.caps = preflight(self.claude, self.env)
        want = self.a.context
        self.mode = "adddir" if (want in ("auto", "adddir") and "add-dir" in self.caps) else "copy"
        log(f"documenti base: {'letti dove stanno (--add-dir)' if self.mode == 'adddir' else 'copia temporanea nella cartella di lavoro'}")
        checks.BASELINE_PATH = str(self.paths["CV_description_baseline.txt"])
        for n, p in self.paths.items():
            if not p.exists():
                raise JobError(f"manca il documento base: {p}")

    def ref(self, name):
        return str(self.paths[name]) if self.mode == "adddir" else f"context/{name}"

    def add_dirs(self):
        return sorted({str(p.parent) for p in self.paths.values()})

    def prepare(self, wd):
        if self.mode == "copy":
            (wd / "context").mkdir(parents=True, exist_ok=True)
            for n, p in self.paths.items():
                dst = wd / "context" / n
                shutil.copyfile(p, dst)
                os.chmod(dst, stat.S_IREAD)

    def snapshot(self):
        """Foto di cio' che l'agente NON deve cambiare: i 3 documenti, lo storico (Archivio) e il codice del runner."""
        snap = {p: p.read_bytes() for p in self.paths.values()}
        extra = []
        if st.ARCHIVIO.exists():
            extra += [f for f in st.ARCHIVIO.rglob("*") if f.is_file()][:600]
        extra += [f for f in st.HERE.glob("*") if f.is_file() and f.suffix in (".py", ".md", ".json")]
        for f in extra:
            try:
                if f.stat().st_size <= 3_000_000:
                    snap[f] = f.read_bytes()
            except OSError:
                pass
        return snap

    def guard(self, snap):
        """Se un agente ha toccato un documento base, lo rimette com'era. Nella baseline la sezione AUTO
        (scritta dal pannello con le tue risposte) non conta: si controlla e ripristina solo la parte normale."""
        for p, data in snap.items():
            try:
                cur = p.read_bytes()
                if cur == data:
                    continue
                if p.name == st.BASELINE_NAME:
                    bom = cur.startswith(b"\xef\xbb\xbf")
                    m_cur, a_cur = st.auto_split(cur.decode("utf-8-sig"))
                    m_old, _ = st.auto_split(data.decode("utf-8-sig"))
                    if m_cur == m_old:
                        continue
                    p.write_bytes((b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b"") + (m_old + a_cur).encode("utf-8"))
                else:
                    p.write_bytes(data)
                log(f"ATTENZIONE: un agente aveva modificato {p.name}: ripristinato com'era.")
            except FileNotFoundError:
                try:
                    p.write_bytes(data)
                    log(f"ATTENZIONE: {p.name} era sparito durante il lavoro: ripristinato.")
                except Exception as e:
                    log(f"(ripristino di {p.name} non riuscito: {e})")
            except Exception as e:
                log(f"(controllo di {p.name} non riuscito: {e})")
        if st.ARCHIVIO.exists():                         # file nuovi nello storico: li ha creati l'agente, non devono esserci
            for f in st.ARCHIVIO.rglob("*"):
                if f.is_file() and f not in snap:
                    try:
                        f.unlink()
                        log(f"ATTENZIONE: l'agente aveva creato {f.name} nell'Archivio: tolto.")
                    except OSError:
                        pass

    def fill(self, text):
        arc = str(st.ARCHIVIO) if (self.mode == "adddir" and st.ARCHIVIO.exists()) else "(not available this run)"
        outd = str(st.OUT) if (self.mode == "adddir" and st.OUT.exists()) else "(not available this run)"
        return (text.replace("{{ARC}}", arc).replace("{{OUTD}}", outd)
                .replace("{{FW}}", self.ref("Job search framework.md"))
                .replace("{{CVB}}", self.ref("CV_description_baseline.txt"))
                .replace("{{LB}}", self.ref("cover letter baseline.md")))


def _opzioni(ctx, turns, effort, tools, use_restricted):
    return dict(modello=ctx.S["model"], turni=turns, effort=effort if "effort" in ctx.caps else None, strumenti=tools,
                cartelle_extra=ctx.add_dirs() if ctx.mode == "adddir" else (), ristretto=use_restricted and "restricted" in ctx.caps,
                sessione=True, stdin=False)


def build_cmd(ctx, prompt, turns, effort, tools, use_restricted=True):
    return motori.comando(prompt, claude=ctx.claude, **_opzioni(ctx, turns, effort, tools, use_restricted))


def run_claude(ctx, cwd, prompt, turns, phase, effort, tools=CV_TOOLS, use_restricted=True):
    if ctx.a.dry_run:
        cmd = build_cmd(ctx, prompt, turns, effort, tools, use_restricted)
        log("DRY-RUN, comando che verrebbe eseguito:\n    " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
        return {"dry": True, "phase": phase, "started": datetime.now(), "ended": datetime.now(), "wall": 0.0,
                "status": "DRY"}
    r = motori.chiama(prompt, cwd, chi="candidature", progetto="candidature", task=getattr(ctx, "job_id", "") or phase,
                      fase=phase, timeout=ctx.S["timeout_min"] * 60, **_opzioni(ctx, turns, effort, tools, use_restricted))
    status = "TIMEOUT" if r.timeout else "ok"
    stderr, rc = r.stderr, r.returncode
    j = r.dati or {}
    u = j.get("usage") or {}
    res = {"phase": phase, "started": r.inizio, "ended": r.fine, "wall": r.secondi,
           "api_s": (j.get("duration_api_ms") or 0) / 1000, "turns": j.get("num_turns"),
           "models": r.modelli, "input": u.get("input_tokens"),
           "cache_creation": u.get("cache_creation_input_tokens"), "cache_read": u.get("cache_read_input_tokens"),
           "output": u.get("output_tokens"), "cost": j.get("total_cost_usd"), "subtype": j.get("subtype", ""),
           "is_error": j.get("is_error"), "result": str(j.get("result", ""))[:300], "session_id": j.get("session_id"),
           "rc": rc, "stderr": stderr[-400:], "status": status, "effort": effort}
    if status == "ok":
        txt = (res["result"] + " " + stderr).lower()
        if rc != 0 or res["is_error"]:
            res["status"] = "LIMIT" if re.search(r"limit|quota|usage|rate", txt) else "ERROR"
            if res["subtype"] == "error_max_turns":
                res["status"] = "INCOMPLETE"
    res["log"] = session_log_tokens(res["session_id"])
    return res


def tok_total(res):
    return sum((res.get(k) or 0) for k in ("input", "cache_creation", "cache_read", "output"))


def write_csv(oid, res, ctx, issues):
    """(v0.5) Il consumo di ogni chiamata lo scrive gia' motori.chiama nel log unico logs\\uso.csv: qui non serve piu' nulla."""
    return None


def upd_offer(oid, fn):
    def go(s):
        o = st.find_offer(s, oid)
        if o is not None:
            fn(s, o)
    st.update(go)


def record_phase(oid, name, res, ctx, issues=0):
    write_csv(oid, res, ctx, issues)
    if res.get("dry"):
        return

    def go(s, o):
        e = {"nome": name, "inizio": res["started"].strftime("%Y-%m-%dT%H:%M:%S"),
             "fine": res["ended"].strftime("%Y-%m-%dT%H:%M:%S"), "stato": res["status"], "turni": res.get("turns"),
             "secondi": round(res["wall"]), "costo": res.get("cost") or 0, "token": tok_total(res)}
        o["fasi"] = [x for x in o.get("fasi", []) if x.get("nome") != name] + [e]
    upd_offer(oid, go)


def stop_for_limit(res):
    # 04/10: niente piu' STOP automatico (restava li' e bloccava tutto per ore). Si registra l'orario di reset di Claude
    # per TUTTI i runner; il lavoro torna in coda e riparte da solo dopo il reset.
    fino = comune.imposta_limite(f"{res.get('result') or ''} {res.get('stderr') or ''}", "candidature")
    raise LimitReached(f"limite di Claude: il lavoro torna in coda e riparte da solo dopo le {comune.quando(fino)}")


def check_status(res, what):
    if res.get("dry"):
        return
    if res["status"] == "LIMIT":
        stop_for_limit(res)
    if res["status"] in ("ERROR", "TIMEOUT"):
        raise JobError(f"{what}: {res['status']} {res.get('result') or res.get('stderr')}"[:300])


def fresh_lavoro():
    wd = st.LAVORO
    if wd.exists():
        assert wd.resolve().name == "lavoro" and wd.resolve().parent.name == "stato"
        shutil.rmtree(wd, onerror=_rm_ro)
    wd.mkdir(parents=True, exist_ok=True)
    return wd


# ------------------------------------------------------------ testo offerta
def issues_text(issues):
    return "\n".join(f"- [{f}] {k} (riga {ln}): {msg}" if ln else f"- [{f}] {k}: {msg}" for f, k, ln, msg in issues)


def questions_from_text(text):
    return [m.strip() for m in re.findall(r"\[\[\s*(?:CONFIRM:?)?\s*(.*?)\]\]", text, flags=re.S) if m.strip()]


def user_blocks(s, oid, fase):
    """Direzioni e risposte di Leonardo da passare all'agente."""
    out = []
    hs = st.hints_for(s, oid, fase)
    if hs:
        out.append("\n## HINTS FROM LEONARDO (standing directions: follow them; they come from him)\n"
                   + "\n".join(f"- {h['testo']}" for h in hs))
    ans = [q for q in s["domande"] if q["offerta"] == oid and q.get("risposta") and q.get("tipo") != "testo_offerta"]
    if ans:
        out.append("\n## ANSWERS FROM LEONARDO TO YOUR EARLIER QUESTIONS (facts told by Leonardo himself: they count as "
                   "baseline facts for this offer; do not ask these questions again)\n"
                   + "\n".join(f"- Q: {q['testo']}\n  A: {q['risposta']}" for q in ans))
    return "\n".join(out) + ("\n" if out else "")


def get_offer_text(oid):
    """Testo dell'offerta: quello salvato; se manca lo legge dal link. Ritorna (testo, ok)."""
    s = st.load()
    o = st.find_offer(s, oid)
    if o.get("testo"):
        text = o["testo"]
        if o.get("ctx") is None and o.get("url"):
            try:
                ctx, used = fetcher.fetch_company_context(o["url"], [], "")
                log("    pagine azienda lette: " + (", ".join(used) if used else "nessuna (NOT AVAILABLE)"))
            except Exception as e:
                log(f"    (pagina azienda non letta: {e})")
                ctx = ""
            upd_offer(oid, lambda s_, o_: o_.__setitem__("ctx", ctx))
        return text, True
    url = o.get("url")
    if not url:
        return "", False
    log(f"leggo il link: {url}")
    fo = fetcher.fetch_offer(url)
    if not fo["ok"]:
        log(f"    NON LEGGIBILE: {fo['error']}")

        def go(s_, o_):
            st.add_question(s_, oid, f"Offerta non leggibile dal link ({fo['error'][:80]}). Incolla qui il testo dell'annuncio.",
                            tipo="testo_offerta")
            st.offer_log(o_, "link non leggibile: serve il testo")
        upd_offer(oid, go)
        return "", False
    host = re.sub(r"^www\.", "", re.sub(r"^https?://", "", url).split("/")[0])
    ctx, used = fetcher.fetch_company_context(url, fo["links"], fo["org_url"])
    log(f"    offerta letta: {len(fo['text'])} caratteri; pagine azienda: " + (", ".join(used) if used else "nessuna"))
    text = f"SOURCE LINK: {url}\n\n" + fo["text"]

    def go(s_, o_):
        o_["testo"] = text[:40000]
        o_["ctx"] = ctx[:15000]
        if not o_.get("azienda"):
            o_["azienda"] = host
        if not o_.get("ruolo"):
            o_["ruolo"] = (fo.get("title") or "")[:80]
    upd_offer(oid, go)
    return text, True


def cv_header(o, meta):
    link = f"OFFER LINK: {o['url']}\n" if o.get("url") else "OFFER: testo incollato\n"
    return link + f"OFFER: {meta.get('role', '')} | {meta.get('company', '')} | {meta.get('location', '')}\n" + "-" * 60 + "\n\n"


def strip_header(text):
    lines = text.split("\n")
    for i, ln in enumerate(lines[:6]):
        if re.fullmatch(r"-{20,}", ln.strip()):
            return "\n".join(lines[i + 1:]).lstrip("\n")
    return text


def _part(x, n):
    x = unicodedata.normalize("NFKD", str(x or "")).encode("ascii", "ignore").decode()
    x = re.sub(r"\((?:m|w|d|f|x|/|\s|\*)+\)", " ", x, flags=re.I)         # (m/w/d), (m/f/x)
    words = re.findall(r"[A-Za-z0-9]+", x)
    return "".join(w[:1].upper() + w[1:] for w in words)[:n]


def make_tag(s_, o_, meta, lang):
    """Nome cartella: Azienda_Ruolo_LINGUA. Unico tra le offerte (se esiste gia' si aggiunge l'id)."""
    az = _part(meta.get("company") or o_.get("azienda"), 24) or "Azienda"
    ru = _part(meta.get("role") or o_.get("ruolo"), 32) or "Ruolo"
    tag = "_".join(x for x in (az, ru, lang) if x)
    used = {x.get("tag") for x in s_["offerte"] if x.get("tag") and x["id"] != o_["id"]}
    return tag if tag not in used else f"{tag}_{o_['id']}"


def write_pair(wd_dir, name, text):
    wd_dir.mkdir(parents=True, exist_ok=True)
    p = wd_dir / name
    p.write_text(text, encoding="utf-8")
    return p


# ------------------------------------------------------------------- fase CV
def do_cv(job, ctx):
    oid = job["offerta"]
    s = st.load()
    o = st.find_offer(s, oid)
    log(f"=== CV: {st.label(o)}")
    text, ok = get_offer_text(oid)
    if not ok:
        return "serve il testo dell'offerta (domanda nel pannello)"
    s = st.load()
    o = st.find_offer(s, oid)
    wd = fresh_lavoro()
    for d in ("out/cv", "out/analysis", "out/letter"):
        (wd / d).mkdir(parents=True, exist_ok=True)
    ctx.prepare(wd)
    (wd / "offer.txt").write_text(text, encoding="utf-8")
    (wd / "company_context.txt").write_text(o.get("ctx") or "NOT AVAILABLE (no company page read)", encoding="utf-8")
    task = ctx.fill((st.HERE / "TASK_template.md").read_text(encoding="utf-8")) + user_blocks(s, oid, "cv")
    (wd / "TASK.md").write_text(task, encoding="utf-8")
    snap = ctx.snapshot()
    try:
        log("fase 1: analisi + CV")
        r1 = run_claude(ctx, wd, "Read TASK.md in the current folder and carry it out completely.",
                        ctx.S["turns"], "generate", ctx.S["effort"])
        if r1.get("dry"):
            return "DRY"
        if ctx.mode == "adddir" and not (wd / "out/cv/CV_description.txt").exists() and r1["status"] in ("ok", "ERROR", "INCOMPLETE"):
            log("nessun file prodotto leggendo i documenti dove stanno: riprovo una volta con la copia temporanea")
            ctx.mode = "copy"
            ctx.prepare(wd)
            (wd / "TASK.md").write_text(ctx.fill((st.HERE / "TASK_template.md").read_text(encoding="utf-8")) + user_blocks(s, oid, "cv"),
                                        encoding="utf-8")
            record_phase(oid, "Analisi e CV", r1, ctx)
            r1 = run_claude(ctx, wd, "Read TASK.md in the current folder and carry it out completely.",
                            ctx.S["turns"], "generate", ctx.S["effort"])
        record_phase(oid, "Analisi e CV", r1, ctx)
        log(f"fine fase 1: {fmt_s(r1['wall'])}, turni {r1.get('turns')}, stato {r1['status']}, costo listino ${r1.get('cost') or 0:.3f}")
        check_status(r1, "fase 1")
        cvp, anp, mp = wd / "out/cv/CV_description.txt", wd / "out/analysis/Analysis.md", wd / "out/meta.json"
        missing = [p.name for p in (cvp, anp, mp) if not p.exists()]
        if missing:
            raise JobError(f"l'agente non ha scritto: {missing}")
        meta = {}
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            log("meta.json non valido")
        lang = re.sub(r"[^A-Za-z]+", "", meta.get("lang", "")).upper()
        issues, warns = checks.check_cv(cvp, text, lang)
        hard = [("CV_description.txt",) + x for x in issues if x[0] != "PLACEHOLDER"]
        if hard and not ctx.a.no_retry:
            log(f"controlli: {len(hard)} errori, parte la correzione")
            for _f, _k, _ln, _m in hard:
                log(f"    - {_k}" + (f" (riga {_ln})" if _ln else "") + f": {str(_m)[:160]}")
            n_first = len(hard)
            (wd / "FIX.md").write_text(ctx.fill((st.HERE / "FIX_template.md").read_text(encoding="utf-8"))
                                       .replace("{{ISSUES}}", issues_text(hard)), encoding="utf-8")
            r2 = run_claude(ctx, wd, "Read FIX.md in the current folder and carry it out completely.", 12, "fix", ctx.S["effort"])
            record_phase(oid, "Correzione", r2, ctx, issues=n_first)
            log(f"fine correzione: {fmt_s(r2['wall'])}, stato {r2['status']}")
            check_status(r2, "correzione")
            issues, warns = checks.check_cv(cvp, text, lang)
            hard = [("CV_description.txt",) + x for x in issues if x[0] != "PLACEHOLDER"]
        cv_text = cvp.read_text(encoding="utf-8-sig")
        analysis = anp.read_text(encoding="utf-8-sig")
        qs = [q for q in (meta.get("questions") or []) if isinstance(q, str)]
        qs += ["Dato mancante: " + x for x in questions_from_text(cv_text)]
        esito = "DA RIVEDERE (errori residui)" if hard else "OK"
        ctrl = ((issues_text([("CV_description.txt",) + x for x in issues]) + "\n") if issues else "") + (
            "\n".join(f"- avviso [{k}] {msg}" for k, ln, msg in warns) or "- nessun avviso")

        def go(s_, o_):
            tag = o_.get("tag") or make_tag(s_, o_, meta, lang)    # fissato al primo giro: i rifacimenti sovrascrivono
            o_["tag"] = tag
            o_["lingua"] = lang or o_.get("lingua", "")
            o_["azienda"] = meta.get("company") or o_.get("azienda", "")
            o_["ruolo"] = meta.get("role") or o_.get("ruolo", "")
            o_["sede"] = meta.get("location") or o_.get("sede", "")
            o_["analisi"], o_["controlli"], o_["esito"] = analysis, ctrl, esito
            if not o_.get("mappa_id"):                      # collega l'offerta alla mappa (o la aggiunge come nuova, annullabile)
                c = st.find_company(s_, o_.get("azienda"))
                if c is None and o_.get("azienda"):
                    c = st.map_add(s_, {"name": o_["azienda"], "city": o_.get("sede", ""), "url": "", "roles": o_.get("ruolo", ""),
                                        "priority": "B"}, "agente", f"offerta {o_['id']} di un'azienda non in mappa")
                if c is not None:
                    o_["mappa_id"] = c["id"]
            o_["giri"] = o_.get("giri", 0) + 1
            n = 0
            for q in qs:
                if st.add_question(s_, oid, q):
                    n += 1
            o_["stato"] = "cv_pronto"
            st.offer_log(o_, f"CV pronto ({esito})" + (f", {n} domande nuove" if n else ""))
            folder = st.OUT / tag
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"CV_description_{tag}.txt").write_text(cv_header(o_, meta) + cv_text, encoding="utf-8")
        upd_offer(oid, go)
        return f"CV pronto ({esito})"
    finally:
        ctx.guard(snap)


# ------------------------------------------------------------------- lettera
def do_letter(job, ctx):
    oid = job["offerta"]
    s = st.load()
    o = st.find_offer(s, oid)
    log(f"=== LETTERA: {st.label(o)}")
    tag = o.get("tag")
    cvf = st.OUT / tag / f"CV_description_{tag}.txt" if tag else None
    if not cvf or not cvf.exists() or not o.get("analisi"):
        raise JobError("manca il CV di questa offerta: prima fai la fase CV")
    text, ok = get_offer_text(oid)
    if not ok:
        return "serve il testo dell'offerta (domanda nel pannello)"
    s = st.load()
    o = st.find_offer(s, oid)
    wd = fresh_lavoro()
    for d in ("out/cv", "out/analysis", "out/letter"):
        (wd / d).mkdir(parents=True, exist_ok=True)
    ctx.prepare(wd)
    (wd / "offer.txt").write_text(text, encoding="utf-8")
    (wd / "company_context.txt").write_text(o.get("ctx") or "NOT AVAILABLE (no company page read)", encoding="utf-8")
    (wd / "out/analysis/Analysis.md").write_text(o["analisi"], encoding="utf-8")
    (wd / "out/cv/CV_description.txt").write_text(strip_header(cvf.read_text(encoding="utf-8-sig")), encoding="utf-8")
    (wd / "LETTER.md").write_text(ctx.fill((st.HERE / "LETTER_template.md").read_text(encoding="utf-8")) + user_blocks(s, oid, "lettera"),
                                  encoding="utf-8")
    snap = ctx.snapshot()
    try:
        log(f"fase lettera (effort {ctx.S['letter_effort']})")
        r = run_claude(ctx, wd, "Read LETTER.md in the current folder and carry it out completely.", 12, "letter",
                       ctx.S["letter_effort"])
        if r.get("dry"):
            return "DRY"
        record_phase(oid, "Lettera", r, ctx)
        log(f"fine lettera: {fmt_s(r['wall'])}, turni {r.get('turns')}, stato {r['status']}, costo listino ${r.get('cost') or 0:.3f}")
        check_status(r, "lettera")
        lp = wd / "out/letter/CoverLetter.txt"
        if not lp.exists():
            raise JobError("l'agente non ha scritto la lettera")
        lang = (o.get("lingua") or "").upper()
        issues, warns = checks.check_letter(lp, text, lang)
        hard = [("CoverLetter.txt",) + x for x in issues if x[0] != "PLACEHOLDER"]
        if hard and not ctx.a.no_retry:
            log(f"controlli lettera: {len(hard)} errori, parte la correzione")
            for _f, _k, _ln, _m in hard:
                log(f"    - {_k}" + (f" (riga {_ln})" if _ln else "") + f": {str(_m)[:160]}")
            n_first = len(hard)
            (wd / "FIX.md").write_text(ctx.fill((st.HERE / "FIX_template.md").read_text(encoding="utf-8"))
                                       .replace("{{ISSUES}}", issues_text(hard)), encoding="utf-8")
            r2 = run_claude(ctx, wd, "Read FIX.md in the current folder and carry it out completely.", 12, "fix", ctx.S["effort"])
            record_phase(oid, "Correzione lettera", r2, ctx, issues=n_first)
            check_status(r2, "correzione lettera")
            issues, warns = checks.check_letter(lp, text, lang)
            hard = [("CoverLetter.txt",) + x for x in issues if x[0] != "PLACEHOLDER"]
        letter = lp.read_text(encoding="utf-8-sig")
        qs = ["Dato mancante: " + x for x in questions_from_text(letter)]
        esito = "DA RIVEDERE (errori residui)" if hard else "OK"
        ctrl_l = ((issues_text([("CoverLetter.txt",) + x for x in issues]) + "\n") if issues else "") + (
            "\n".join(f"- avviso [{k}] {msg}" for k, ln, msg in warns) or "- nessun avviso")

        def go(s_, o_):
            o_["controlli"] = (o_.get("controlli") or "").split("\nLettera:")[0] + "\nLettera:\n" + ctrl_l
            n = sum(1 for q in qs if st.add_question(s_, oid, q))
            o_["esito"] = esito if esito != "OK" else ("OK" if not (o_.get("esito") or "").startswith("DA RIVEDERE") else o_["esito"])
            o_["stato"] = "lettera" if st.open_questions(s_, oid) else "pronta"
            st.offer_log(o_, f"lettera fatta ({esito})" + (f", {n} domande nuove" if n else ""))
            folder = st.OUT / tag
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"CoverLetter_{tag}.txt").write_text(letter, encoding="utf-8")
        upd_offer(oid, go)
        return f"lettera fatta ({esito})"
    finally:
        ctx.guard(snap)


# ----------------------------------------------------------------- lavori
def make_ctx(a):
    s = st.load()
    S = dict(s["impostazioni"])
    for k in ("model", "effort", "letter_effort", "turns", "timeout_min"):
        v = getattr(a, k, None)
        if v is not None:
            S[k] = v
    ctx = Ctx(a, S)
    ctx.setup()
    return ctx


def run_job(job_id, a):
    """Esegue UN lavoro della coda. Un solo agente alla volta: se un altro e' attivo, esce."""
    if not a.dry_run:
        why = comune.perche_non_parte("candidature")
        if why:
            print(f"Non parto: {why}.")
            return "occupato"
    if not a.dry_run and not st.acquire_run(job_id):
        print("Un altro lavoro e' gia' in corso: aspetto il mio turno (un solo agente alla volta).")
        return "occupato"
    stop_hb = threading.Event()

    def hb():
        while not stop_hb.wait(20):
            st.heartbeat()
    threading.Thread(target=hb, daemon=True).start()
    keep_awake(True)
    esito, errore, rimetti = "", False, False
    try:
        s = st.load()
        job = next((j for j in s["coda"] if j["id"] == job_id), None)
        if not job:
            return "sconosciuto"
        if not a.dry_run:
            def start(s_):
                j = next(x for x in s_["coda"] if x["id"] == job_id)
                j["stato"], j["inizio"] = "in_corso", st.now_iso()
                if j["tipo"] == "scout":
                    s_["scout"]["ultimo"] = None
            st.update(start)
        ctx = None if job["tipo"] == "manutenzione" else make_ctx(a)
        if ctx is not None:
            ctx.job_id = job_id          # per il log unico: a quale lavoro appartiene ogni chiamata
        try:
            if job["tipo"] == "manutenzione":
                import mappa
                esito = mappa.do_manutenzione(job)
            elif job["tipo"] == "nuove_aziende":
                import mappa
                esito = mappa.do_nuove_aziende(job, ctx)
            elif job["tipo"] == "scout":
                import scout
                esito = scout.do_scout(job, ctx)
            elif job["tipo"] == "cv":
                esito = do_cv(job, ctx)
            elif job["tipo"] == "letter":
                esito = do_letter(job, ctx)
            else:
                raise JobError(f"tipo di lavoro sconosciuto: {job['tipo']}")
        except LimitReached as e:
            esito, errore, rimetti = str(e), True, True
        except JobError as e:
            esito, errore = str(e), True
        except Exception as e:
            if type(e).__name__ == "LimitReached":   # scout.py la solleva come runner.LimitReached (modulo diverso da __main__)
                esito, errore, rimetti = str(e), True, True
            else:
                import traceback
                esito, errore = f"errore imprevisto: {e}", True
                log(traceback.format_exc())
        log(f"=== FINE lavoro {job['tipo']} {job.get('offerta') or ''}: {esito}")
    except Exception as e:
        import traceback
        esito, errore = f"errore imprevisto: {e}", True
        log(traceback.format_exc())
    finally:
        stop_hb.set()
        keep_awake(False)
        if not a.dry_run:
            def end(s_):
                j = next((x for x in s_["coda"] if x["id"] == job_id), None)
                if j and rimetti:
                    j["stato"], j["inizio"], j["esito"] = "in_attesa", None, esito   # riparte da solo dopo il reset
                elif j:
                    j["stato"] = "errore" if errore else "fatto"
                    j["fine"], j["esito"] = st.now_iso(), esito
                    o = st.find_offer(s_, j.get("offerta")) if j.get("offerta") else None
                    if o is not None and errore:
                        st.offer_log(o, "ERRORE: " + esito)
            st.update(end)
            st.release_run()
    return "errore" if errore else "fatto"


def work_queue(a):
    """Svuota la coda un lavoro alla volta, poi si ferma (nessuna attesa, nessun token a vuoto)."""
    n = 0
    while True:
        if st.STOP_FILE.exists():
            log("file STOP presente: coda in pausa.")
            break
        why = "" if a.dry_run else comune.perche_non_parte("candidature")
        if why:
            print(f"In pausa: {why}.")
            break
        s = st.load()
        job = st.next_job(s)
        if not job:
            break
        r = run_job(job["id"], a)
        n += 1
        if r == "occupato":
            break
        if st.STOP_FILE.exists():
            break
    if n == 0:
        print("Niente da fare in coda.")


def resolve_offer(s, key):
    key = str(key)
    for o in s["offerte"]:
        if o["id"] == key:
            return o
    hits = [o for o in s["offerte"] if key.lower() in st.label(o).lower() or key in (o.get("url") or "")]
    return hits[0] if len(hits) == 1 else None


def cmd_coda(a):
    s = st.load()
    print(f"Pausa (STOP): {'si' if st.STOP_FILE.exists() else 'no'}   Agente al lavoro: {'si' if st.runner_busy() else 'no'}")
    for o in s["offerte"]:
        if o["stato"] == "scartata":
            continue
        stato, nota, _ = st.offer_view(s, o)
        print(f"  {o['id']:<5} {stato:<13} {st.label(o)[:60]}   {nota}")
    qs = st.open_questions(s)
    print(f"Domande aperte: {len(qs)}")
    for q in qs:
        print(f"  {q['id']}: {q['testo']}")
    print("Direzioni attive: " + (str(len(s['hint'])) if s["hint"] else "nessuna"))
    print(f"Lavori in attesa: {len([j for j in s['coda'] if j['stato'] == 'in_attesa'])}   rapporto: {st.CODA_MD}")


def main():
    ap = argparse.ArgumentParser(description="Runner candidature (un agente alla volta, a gate).")
    ap.add_argument("comando", choices=["coda", "scout", "aggiungi", "avanti", "rifai", "lavora", "job", "manutenzione", "nuove_aziende", "mappa"])
    ap.add_argument("arg", nargs="*")
    ap.add_argument("--dry-run", action="store_true", help="prepara tutto e mostra il comando, senza chiamare Claude")
    ap.add_argument("--no-retry", action="store_true", help="niente correzione automatica")
    ap.add_argument("--context", default="auto", choices=["auto", "adddir", "copy"])
    ap.add_argument("--model", default=None)
    ap.add_argument("--effort", default=None)
    ap.add_argument("--letter-effort", dest="letter_effort", default=None)
    ap.add_argument("--turns", type=int, default=None)
    ap.add_argument("--timeout-min", dest="timeout_min", type=int, default=None)
    a = ap.parse_args()
    st.STATO.mkdir(parents=True, exist_ok=True)

    if a.comando == "coda":
        return cmd_coda(a)
    if a.comando == "job":
        run_job(a.arg[0], a)
        return
    if a.comando == "mappa":
        s = st.load()
        ms = list(s["mappa"].values())
        print(f"Mappa: {len(ms)} aziende (A {sum(1 for c in ms if c.get('priority') == 'A')}, B {sum(1 for c in ms if c.get('priority') == 'B')}, "
              f"C {sum(1 for c in ms if c.get('priority') == 'C')}); modifiche degli agenti da rivedere: "
              f"{sum(1 for r in s['registro'] if r['stato'] == 'attivo')}")
        return
    if a.comando in ("manutenzione", "nuove_aziende"):
        st.update(lambda s: st.enqueue(s, a.comando))
    elif a.comando == "scout":
        st.update(lambda s: st.enqueue(s, "scout"))
    elif a.comando == "aggiungi":
        if not a.arg:
            sys.exit("Uso: python runner.py aggiungi <link>")

        def go(s):
            o, new = st.add_offer(s, url=a.arg[0], stato="approvata")
            st.enqueue(s, "cv", o["id"])
        st.update(go)
    elif a.comando in ("avanti", "rifai"):
        if not a.arg:
            sys.exit(f"Uso: python runner.py {a.comando} <id|tutte>")

        def go(s):
            targets = [o for o in s["offerte"] if o["stato"] in ("trovata", "cv_pronto")] if a.arg[0] == "tutte" else [resolve_offer(s, a.arg[0])]
            for o in targets:
                if o is None:
                    print("Offerta non trovata (guarda gli id con: python runner.py coda).")
                    continue
                if st.open_questions(s, o["id"]):
                    print(f"{o['id']}: ha domande aperte, rispondi prima (pannello).")
                    continue
                if a.comando == "rifai":
                    st.redo(s, o, (a.arg[1] if len(a.arg) > 1 else "cv").lower())
                else:
                    st.advance(s, o)
        st.update(go)
    work_queue(a)


if __name__ == "__main__":
    main()
