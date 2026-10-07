#!/usr/bin/env python3
r"""
Runner notturno minimo, v1. Solo libreria standard di Python.

Novita' v1 (progetti con repository git, es. Langue): campo `repo:` nel task. Il runner crea un
ramo di lavoro (mai main), salva lo stato prima, lascia lavorare l'agente DIRETTAMENTE sui file veri,
controlla che abbia toccato solo i file permessi, esegue i controlli in Python, e committa
"[agente T0X]". Campi in piu': depends_on, approval_before, approval_after, script, allowed, checks,
gitignore, profile, title, branch. Vedi repo_tools.py.

Uso (PowerShell, nella cartella di questo file, es. C:\Agents):
  python runner.py --dry-run --ignore-window      mostra i comandi, non esegue nulla
  python runner.py --ignore-window --max-tasks 1  prova a mano con un task
  python runner.py                                 lavora sempre, un task alla volta, finche' non c'e' piu' nulla di pronto

Cartelle (create al primo avvio):
  queue/       task da fare (*.task.md)        done/        task completati
  blocked/     task che aspettano una tua risposta o approvazione
  incomplete/  fermati per limite di turni o di tempo
  failed/      errori                          work/        cartella di lavoro di ogni task
  results/     output, riassunti, JSON grezzi  decisions/   domande degli agenti
  logs/        usage.csv e runner.log
Per fermare tutto subito: crea un file vuoto chiamato STOP in questa cartella.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import repo_tools as rt

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
import scheda  # scheda progetto: documento centrale di ogni progetto (04/10)
import comune  # regole condivise: un agente alla volta, limite di Claude, contatore d'uso (04/10)
LAST_LIMIT_TEXT = ""
D = {n: BASE / n for n in ("queue", "done", "blocked", "incomplete", "failed",
                           "work", "results", "decisions", "logs", "samples")}

# Valori iniziali: da ritarare sui log dopo qualche notte.
TIERS = {
    "small":  dict(timeout=600,  max_turns=15,  model="sonnet", effort="low"),
    "medium": dict(timeout=1800, max_turns=40,  model="sonnet", effort="medium"),
    "large":  dict(timeout=5400, max_turns=100, model="sonnet", effort="high", needs_approval=True),
}
# v1.1: il runner lavora SEMPRE, un task alla volta, finche' la coda non ha piu' nulla di pronto.
# Nessuna finestra oraria e nessun tetto di default (si possono rimettere con --window 1-9, --max-tasks N, --cost-cap USD).
LIMIT_COOLDOWN_MIN = 60    # dopo un errore di limite d'uso aspetta questi minuti prima di riprovare
LOCK_STALE_H = 3           # un lock piu' vecchio di cosi' e' considerato rimasto da un'esecuzione interrotta
LIMIT_HINTS = ("usage limit", "rate limit", "limit reached", "limit will reset", "too many requests")

CSV_FIELDS = ["timestamp", "task_id", "project", "tier", "model", "status", "subtype", "is_error",
              "num_turns", "cost_usd", "input_tokens", "cache_creation", "cache_read",
              "output_tokens", "duration_s", "permission_denials"]

WRAPPER = """You are working unattended in an isolated folder. You can only read and write files in the current folder.
Inputs are in ./inputs/ . Write every deliverable to ./outputs/ .

Rules:
- Never invent facts. If something is not in the inputs, say it is unknown. "unknown" beats an invented answer.
- For small, reversible choices, pick a sensible default and log it as one line in ./DEFAULTS_LOG.md .
- If you need a decision you cannot safely default (irreversible, costly, affects other projects or shared files, changes data or schemas, or depends on the user's personal preference), do NOT guess: write the question with 2-3 options and your recommendation in ./DECISIONS.md, whose FIRST line must be exactly `STATUS: OPEN`. Finish whatever is not blocked, and stop.
- If ./ANSWERS.md exists, the user already answered: apply it and do NOT create ./DECISIONS.md again, unless a NEW question remains (then use `STATUS: OPEN`). To record how you applied an answer, use ./DEFAULTS_LOG.md.
- ASK QUESTIONS freely (Leo wants them: they are the best way to steer the project), but WITHOUT stopping: when a choice depends on Leo's taste, knowledge or plans, pick a sensible provisional choice, use it, keep working, and add one line per question to ./DOMANDE.md in exactly this format (Italian, max 15 words per question, max 8 questions; CLOSED questions with 2-4 options whenever possible, open only if impossible):
  - domanda breve? | opzioni: A / B / C | scelta: B | dove: file o record toccati
  Use DECISIONS.md (which STOPS the task) only when you truly cannot continue without Leo doing something.
- Do not try to access anything outside this folder.
- Finish with a summary in Italian of at most 5 lines: what you did, files produced, defaults chosen, open questions. Its FIRST line must be exactly: `ESITO: <one plain sentence with the concrete result, with numbers>`.
@@ANSWERS@@
TASK:
@@BODY@@
"""


REPO_WRAPPER = """You are working unattended, directly on the REAL project files in the current folder (a git repository, already on your own task branch). The runner commits your work afterwards: do not use git.
Write deliverables only to the paths listed under ALLOWED PATHS. Do not touch any other file. Ignore the folders .venv, .git, __pycache__ and archivio.

Rules:
- Never invent facts. If something is not verifiable, say so or mark it "da_verificare". "unknown" beats an invented answer.
- Everything you create must be recognizable as agent work: new content records carry "origine": "agente @@ID@@" and "stato": "bozza" (unless the task says otherwise).
- Never edit the project sheet (PROGETTO.md, MEMORIA_PROGETTO.md or the sheet named below): it belongs to Leo. Suggest changes to it in your report.
- Write a short report in Italian to ./agenti/@@ID@@/RAPPORTO.md : what you did, what you checked, small choices you made (defaults), anything Leo must decide or review.
- For small, reversible choices pick a sensible default and list it in the report under "Scelte". If you need a decision you cannot safely default (irreversible, costly, changes the schema or existing data, depends on Leo's taste), do NOT guess: write the question with 2-3 options and your recommendation in ./agenti/@@ID@@/DECISIONS.md, whose FIRST line must be exactly `STATUS: OPEN`. Finish whatever is not blocked, and stop.
- If ./agenti/@@ID@@/ANSWERS.md exists, Leo already answered: apply it and do NOT create DECISIONS.md again unless a NEW question remains.
- ASK QUESTIONS freely (Leo wants them: they are the best way to steer the project), but WITHOUT stopping: when a choice depends on Leo's taste, knowledge or plans, pick a sensible provisional choice, use it, keep working, and add one line per question to ./agenti/@@ID@@/DOMANDE.md in exactly this format (Italian, max 15 words per question, max 8 questions; CLOSED questions with 2-4 options whenever possible, open only if impossible):
  - domanda breve? | opzioni: A / B / C | scelta: B | dove: file o record toccati
  Use DECISIONS.md (which STOPS the task) only when you truly cannot continue without Leo doing something.
- You cannot run programs. After you finish, the RUNNER runs the project's validator (the task's checks) and logs the result. If it finds errors, you get up to two more short turns with the exact error list: fix only those. Never claim that you validated something yourself.
- Finish with a summary in Italian of at most 5 lines. Its FIRST line must be exactly: `ESITO: <one plain sentence with the concrete result, with numbers>` (it goes in Leo's diary).

ALLOWED PATHS: @@ALLOWED@@
@@PROFILE@@
@@ANSWERS@@
TASK:
@@BODY@@
"""


FIX_WRAPPER = """You are working unattended on the REAL project files in the current folder (a git repository, on your own task branch). Do not use git.
The runner validated your previous work and found the errors listed below. Fix ONLY these errors, editing only the ALLOWED PATHS. Do not rewrite things that are fine. Keep every record's "origine" and "stato" as they are.
Then finish with at most 3 lines: what you fixed. If an error cannot be fixed safely, say so in ./agenti/@@ID@@/RAPPORTO.md (append a short section "Validatore") instead of guessing.

ALLOWED PATHS: @@ALLOWED@@
VALIDATOR ERRORS (round @@ROUND@@):
@@ERRORS@@

TASK (for context, shortened):
@@BODY@@
"""
MAX_FIX_ROUNDS = 2


def listify(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def ready(t):
    """Il task puo' partire? (approvazione richiesta prima, dipendenze completate e approvate)"""
    if t.get("approval_before", "").lower() == "leo" and t.get("approved", "no").lower() != "yes":
        return False, "aspetta il tuo OK (Ufficio: Da approvare)"
    for dep in listify(t.get("depends_on")):
        files = sorted(D["done"].glob(dep + "*.task.md"))
        if not files:
            return False, f"dipende da {dep}, non ancora completato"
        m = parse_task(files[0])
        if m.get("approval_after", "").lower() == "leo" and m.get("approved", "no").lower() != "yes":
            return False, f"{dep} e' fatto ma aspetta il tuo OK (Ufficio: Da approvare)"
    return True, ""


def decisioni_progetto(t):
    """Risposte di Leo alle domande degli agenti di questo progetto (progetti/<id>.json, campo decisioni): valgono per ogni task."""
    try:
        p = json.loads((BASE.parent / "progetti" / f"{(t.get('project') or '').lower()}.json").read_text(encoding="utf-8-sig"))
    except Exception:
        return ""
    ds = (p.get("decisioni") or [])[-30:]
    if not ds:
        return ""
    return "\nLEO'S DECISIONS FOR THIS PROJECT (always follow them):\n" + "\n".join(f"- {d.get('domanda')} -> {d.get('risposta')}" for d in ds) + "\n"


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    print(line)
    with open(D["logs"] / "runner.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    (D["logs"] / "ultimo_stato.txt").unlink(missing_ok=True)


def log_once(msg):
    """Per i messaggi di attesa (STOP, limite, contatore): li scrive una volta sola finche' non cambiano,
    cosi' il log non si riempie di righe uguali ogni 15 minuti."""
    f = D["logs"] / "ultimo_stato.txt"
    try:
        if f.read_text(encoding="utf-8") == msg:
            print(msg)
            return
    except OSError:
        pass
    log(msg)
    f.write_text(msg, encoding="utf-8")


def to_int(v, default):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def parse_task(path):
    text = path.read_text(encoding="utf-8-sig")
    head, sep, body = text.partition("\n---")
    if not sep:
        raise ValueError("manca la riga --- tra intestazione e istruzioni")
    meta = {}
    for raw in head.splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#") or ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        k, v = k.strip().lower(), v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        meta[k] = v
    meta["body"] = body.lstrip("-").strip()
    meta["_path"] = path
    meta.setdefault("id", path.name.replace(".task.md", ""))
    return meta


def find_claude():
    exe = shutil.which("claude")
    if exe:
        return exe
    alt = Path.home() / ".local" / "bin" / "claude.exe"
    return str(alt) if alt.exists() else None


def move(path, folder):
    dest = D[folder] / path.name
    if dest.exists():
        dest.unlink()
    shutil.move(str(path), str(dest))


def write_usage(row):
    f = D["logs"] / "usage.csv"
    new = not f.exists()
    with open(f, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in CSV_FIELDS})


def parse_output(stdout):
    stdout = stdout.strip()
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        for line in reversed(stdout.splitlines()):
            if line.strip().startswith("{"):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    pass
    return None


def run_repo_task(t, claude, dry_run, cfg, model, max_turns, timeout, row):
    """Task su un repository git: l'agente lavora sui file veri, su un ramo del task."""
    tid = t["id"]
    repo = Path(t["repo"])
    title = t.get("title", tid)
    branch = t.get("branch") or tid
    allowed = listify(t.get("allowed"))
    ctl = repo / "agenti" / tid

    def finish(status, why=""):
        row["status"] = status
        write_usage(row)
        move(t["_path"], status)
        log(f"{tid}: {status} {why}")
        return status, float(row.get("cost_usd") or 0.0)

    if dry_run:
        log(f"[dry-run] {tid}: repo={repo} ramo={branch} script={t.get('script','-')} "
            f"agente={'si' if (t['body'].strip() and t.get('agent','auto').lower()!='no' and (not t.get('script') or t.get('agent','auto').lower()=='yes')) else 'no'} allowed={allowed} checks={listify(t.get('checks'))}")
        return "dry", 0.0
    if not rt.is_repo(repo):
        return finish("failed", f"(repo non valido: {repo})")
    try:
        how = rt.prepare_branch(repo, branch)
        if rt.current_branch(repo) in rt.PROTECTED_BRANCHES:
            return finish("failed", "(sarei su main/master: mi fermo)")
        added = rt.ensure_gitignore(repo, listify(t.get("gitignore")))
        n_untracked = rt.untracked_count(repo)
        if n_untracked > rt.MAX_UNTRACKED:
            return finish("failed", f"({n_untracked} file non tracciati: manca un .gitignore? non committo nulla)")
        base = rt.snapshot(repo, tid)
    except Exception as e:
        return finish("failed", f"(git: {e})")
    log(f"{tid}: ramo {branch} {how}; base {base[:8]}; .gitignore +{len(added)}")
    ctl.mkdir(parents=True, exist_ok=True)
    notes = []

    # 1) script del runner (parte meccanica)
    script = t.get("script")
    if script:
        sp = BASE / "scripts" / script
        r = subprocess.run([sys.executable, str(sp), str(repo)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=600)
        (ctl / "SCRIPT_LOG.txt").write_text(r.stdout + "\n--- STDERR ---\n" + r.stderr, encoding="utf-8")
        notes.append(f"script {script}: exit {r.returncode}")
        if r.returncode != 0:
            return _repo_close(t, repo, ctl, base, "failed", ["lo script e' fallito (vedi SCRIPT_LOG.txt)"], notes, row, tid, title, allowed)

    # 2) agente (parte di contenuto); con `agent: no` il runner rifa' solo i controlli
    status, errs, cost = "done", [], 0.0
    if t.get("agent", "auto").lower() == "no":
        notes.append("agente NON rieseguito: ricontrollo del lavoro gia' presente")
    agent_on = t.get("agent", "auto").lower()
    # Lavoro gia' completo da un tentativo interrotto (es. limite d'uso sull'ultimo messaggio): ramo riusato,
    # rapporto dell'agente presente e tutti i controlli OK -> si adotta senza richiamare l'agente (niente token sprecati).
    if (how == "riusato" and agent_on != "no" and (ctl / "RAPPORTO.md").exists() and listify(t.get("checks"))
            and t["body"].strip() and (not script or agent_on == "yes")):
        pre = rt.run_checks(repo, base, listify(t.get("checks")))
        if pre and not any(e for _, e in pre):
            notes.append("lavoro gia' completo dal tentativo interrotto (rapporto presente, controlli OK): agente NON richiamato")
            log(f"{tid}: lavoro gia' completo dal tentativo precedente: lo adotto senza richiamare l'agente")
            agent_on = "no"
    if t["body"].strip() and agent_on != "no" and (not script or agent_on == "yes"):
        for name in ("DECISIONS.md", "ANSWERS.md"):
            (ctl / name).unlink(missing_ok=True)
        answers = ""
        dec_file = D["decisions"] / f"{tid}.md"
        if dec_file.exists():
            txt = dec_file.read_text(encoding="utf-8")
            if "RISPOSTA:" in txt and txt.rsplit("RISPOSTA:", 1)[1].strip():
                (ctl / "ANSWERS.md").write_text(txt.rsplit("RISPOSTA:", 1)[1].strip(), encoding="utf-8")
                answers = f"Leo answered your earlier questions in ./agenti/{tid}/ANSWERS.md. Read it first."
        profile = ""
        try:
            pj = scheda.progetto((t.get("project") or "").lower())
            profile = scheda.regole_per_agenti(pj) if pj else ""
        except Exception:
            profile = ""
        if not profile and t.get("profile"):
            pp = BASE / t["profile"]
            if pp.exists():
                profile = "PROJECT PROFILE:\n" + pp.read_text(encoding="utf-8")
        profile += decisioni_progetto(t)
        prompt = (REPO_WRAPPER.replace("@@ID@@", tid).replace("@@ALLOWED@@", ", ".join(allowed) or "(see task)")
                  .replace("@@PROFILE@@", profile).replace("@@ANSWERS@@", answers).replace("@@BODY@@", t["body"]))
        cmd = [claude, "-p", "--output-format", "json", "--no-session-persistence",
               "--model", model, "--effort", t.get("effort") or cfg["effort"], "--max-turns", str(max_turns),
               "--restricted", "--permission-mode", "acceptEdits", "--permission-prompts", "none"]
        log(f"{tid}: avvio agente (tier {t.get('tier','small')}, modello {model}, max turni {max_turns}, timeout {timeout}s)")
        t0 = datetime.now()
        res_dir = D["results"] / tid
        res_dir.mkdir(parents=True, exist_ok=True)
        try:
            p = subprocess.run(cmd, input=prompt, cwd=repo, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            row.update(subtype="timeout", duration_s=timeout)
            return _repo_close(t, repo, ctl, base, "incomplete", [f"timeout dopo {timeout}s"], notes, row, tid, title, allowed)
        (res_dir / f"raw_{t0:%Y%m%d_%H%M%S}.txt").write_text(p.stdout + "\n--- STDERR ---\n" + p.stderr, encoding="utf-8")
        data = parse_output(p.stdout)
        row["duration_s"] = round((datetime.now() - t0).total_seconds(), 1)
        if data is None or data.get("is_error") or p.returncode != 0:
            blob = (p.stdout + " " + p.stderr).lower()
            if any(h in blob for h in LIMIT_HINTS) or (data or {}).get("api_error_status") == 429:
                global LAST_LIMIT_TEXT
                LAST_LIMIT_TEXT = p.stdout + " " + p.stderr
                c_lim = float((data or {}).get("total_cost_usd") or 0.0)
                row.update(status="limit", cost_usd=round(c_lim, 4), num_turns=(data or {}).get("num_turns", ""))
                log(f"{tid}: limite d'uso rilevato; il task resta in coda. Se l'agente aveva gia' finito (rapporto scritto e controlli OK), "
                    "al prossimo giro il lavoro viene adottato senza richiamarlo.")
                write_usage(row)
                return "limit", c_lim
        if data:
            u = data.get("usage", {})
            cost = float(data.get("total_cost_usd") or 0.0)
            row.update(subtype=data.get("subtype", ""), is_error=data.get("is_error", ""),
                       num_turns=data.get("num_turns", ""), cost_usd=round(cost, 4),
                       input_tokens=u.get("input_tokens", ""), cache_creation=u.get("cache_creation_input_tokens", ""),
                       cache_read=u.get("cache_read_input_tokens", ""), output_tokens=u.get("output_tokens", ""),
                       permission_denials=len(data.get("permission_denials", [])))
            (res_dir / "summary.txt").write_text(str(data.get("result") or "\n".join(data.get("errors", []))), encoding="utf-8")
        dec_out = ctl / "DECISIONS.md"
        dec_txt = dec_out.read_text(encoding="utf-8").strip() if dec_out.exists() else ""
        dec_open = bool(dec_txt) and not ("STATUS: RESOLVED" in dec_txt.upper() and "STATUS: OPEN" not in dec_txt.upper())
        if data is None or data.get("is_error"):
            status, errs = "failed", ["errore dell'agente (vedi results/%s)" % tid]
        elif data.get("subtype") == "error_max_turns":
            status, errs = "incomplete", ["limite di turni raggiunto"]
        elif dec_open:
            status = "blocked"
            D["decisions"].mkdir(exist_ok=True)
            dec_file.write_text(f"# Decisione richiesta: {tid}\n(Scrivi la tua risposta in fondo, dopo l'ultima riga 'RISPOSTA:'. "
                                "Poi sposta il file task da blocked/ a queue/.)\n\n" + dec_txt + "\n\nRISPOSTA:\n", encoding="utf-8")
    if status == "done" and agent_on != "no" and t["body"].strip() and (not script or agent_on == "yes") and listify(t.get("checks")):
        cost += _validate_loop(t, repo, ctl, base, claude, model, cfg, tid, allowed, row, timeout, max_turns)
    return _repo_close(t, repo, ctl, base, status, errs, notes, row, tid, title, allowed)


def _validate_loop(t, repo, ctl, base, claude, model, cfg, tid, allowed, row, timeout, max_turns):
    """Il runner esegue il validatore (i checks del task); se trova errori richiama l'agente con l'elenco, al massimo MAX_FIX_ROUNDS volte.
    Tutto finisce in results/<id>/VALIDATORE.log (e agenti/<id>/VALIDATORE.md nel progetto), cosi' si puo' controllare cosa e' stato trovato e corretto."""
    vlog = [f"# Validatore - {tid} - {datetime.now():%Y-%m-%d %H:%M}"]
    extra_cost = 0.0
    summary = "nessun controllo"
    for rnd in range(MAX_FIX_ROUNDS + 1):
        res = rt.run_checks(repo, base, listify(t.get("checks")))
        bad = [(sp, e) for sp, e in res if e]
        summary = "tutti i controlli OK" if not bad else f"{len(bad)} controlli falliti"
        vlog.append(f"\n## Giro {rnd}: {summary}")
        for sp, e in res:
            vlog.append(f"- {'OK    ' if not e else 'ERRORE'} {sp}")
            vlog += [f"    - {x}" for x in e[:15]]
        if not bad or rnd == MAX_FIX_ROUNDS:
            break
        errtxt = "\n".join(f"- {sp}\n" + "\n".join(f"    {x}" for x in e[:15]) for sp, e in bad)
        prompt = (FIX_WRAPPER.replace("@@ID@@", tid).replace("@@ALLOWED@@", ", ".join(allowed) or "(see task)")
                  .replace("@@ROUND@@", str(rnd + 1)).replace("@@ERRORS@@", errtxt).replace("@@BODY@@", t["body"][:1500]))
        cmd = [claude, "-p", "--output-format", "json", "--no-session-persistence", "--model", model, "--effort", t.get("effort") or cfg["effort"],
               "--max-turns", str(min(max_turns, 20)), "--restricted", "--permission-mode", "acceptEdits", "--permission-prompts", "none"]
        t0 = datetime.now()
        try:
            p = subprocess.run(cmd, input=prompt, cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=min(timeout, 900))
        except subprocess.TimeoutExpired:
            vlog.append(f"  -> correzione {rnd + 1}: timeout, mi fermo")
            break
        (D["results"] / tid).mkdir(parents=True, exist_ok=True)
        (D["results"] / tid / f"fix{rnd + 1}_{t0:%Y%m%d_%H%M%S}.txt").write_text(p.stdout + "\n--- STDERR ---\n" + p.stderr, encoding="utf-8")
        data = parse_output(p.stdout)
        c = float((data or {}).get("total_cost_usd") or 0.0)
        extra_cost += c
        vlog.append(f"  -> correzione {rnd + 1}: agente richiamato ({(data or {}).get('num_turns', '?')} turni, costo listino {c:.3f} USD)")
        blob = (p.stdout + " " + p.stderr).lower()
        if any(h in blob for h in LIMIT_HINTS) or (data or {}).get("api_error_status") == 429:
            vlog.append("  -> limite d'uso: mi fermo qui")
            break
    (D["results"] / tid).mkdir(parents=True, exist_ok=True)
    (D["results"] / tid / "VALIDATORE.log").write_text("\n".join(vlog) + "\n", encoding="utf-8")
    ctl.mkdir(parents=True, exist_ok=True)
    (ctl / "VALIDATORE.md").write_text("\n".join(vlog) + "\n", encoding="utf-8")
    log(f"{tid}: validatore: {summary}" + (f" (agente richiamato {sum(1 for x in vlog if x.startswith('  -> correzione'))} volte)" if extra_cost else ""))
    try:
        row["cost_usd"] = round(float(row.get("cost_usd") or 0.0) + extra_cost, 4)
    except Exception:
        pass
    return extra_cost


def _repo_close(t, repo, ctl, base, status, errs, notes, row, tid, title, allowed):
    """Guardia di ambito + controlli + RUNNER.md + LOG.md + commit + spostamento del file task."""
    lines = [f"# {tid} - esito del runner ({datetime.now():%Y-%m-%d %H:%M})", "", f"Stato dell'agente: {status}"]
    try:
        files = rt.changed_files(repo, base)
    except Exception as e:
        files, errs = [], errs + [f"git: {e}"]
    bad = rt.out_of_scope(files, allowed) if allowed else []
    notes_extra = []
    if bad:
        errs.append("file fuori dall'ambito permesso: " + ", ".join(bad))
        try:
            rt.restore_paths(repo, base, bad)
            notes_extra.append("file fuori ambito RIPRISTINATI allo stato di prima: " + ", ".join(bad))
            files = [f for f in files if f not in bad]
        except Exception as e:
            notes_extra.append(f"ripristino dei file fuori ambito NON riuscito: {e}")
    check_results = rt.run_checks(repo, base, listify(t.get("checks"))) if status in ("done", "incomplete") else []
    lines += ["", "## Controlli"]
    for spec, e in check_results:
        lines.append(f"- {'OK ' if not e else 'ERRORE'} {spec}")
        for x in e[:15]:
            lines.append(f"    - {x}")
        if e:
            errs.append(f"controllo fallito: {spec}")
    if not check_results:
        lines.append("- (nessun controllo eseguito)")
    lines += ["", "## File cambiati"] + [f"- {f}" for f in files] + ["", "## Note"] + [f"- {n}" for n in notes + notes_extra]
    if errs:
        lines += ["", "## Problemi"] + [f"- {x}" for x in errs]
        if status == "done":
            status = "failed"
    lines[2] = f"Esito finale: {status}"
    ctl.mkdir(parents=True, exist_ok=True)
    (ctl / "RUNNER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    logf = repo / "agenti" / "LOG.md"
    with open(logf, "a", encoding="utf-8") as fh:
        fh.write(f"- {datetime.now():%Y-%m-%d %H:%M} | {tid} | {status} | ramo {rt.current_branch(repo)} | "
                 f"{len(files)} file | costo listino {float(row.get('cost_usd') or 0):.3f} USD | {title}\n")
    tag = f"[agente {tid}]" if status == "done" else f"[agente {tid} {status.upper()}]"
    try:
        sha = rt.commit_all(repo, f"{tag} {title}")
    except Exception as e:
        sha = ""
        log(f"{tid}: commit non riuscito: {e}")
    row["status"] = status
    write_usage(row)
    move(t["_path"], status)
    log(f"{tid}: {status}, commit {sha[:8]} (turni {row.get('num_turns')}, costo listino {float(row.get('cost_usd') or 0):.3f} USD)")
    return status, float(row.get("cost_usd") or 0.0)


def run_task(t, claude, dry_run):
    tid = t["id"]
    tier_name = t.get("tier", "small")
    cfg = dict(TIERS.get(tier_name, TIERS["small"]))
    model = t.get("model", cfg["model"])
    max_turns = to_int(t.get("max_turns"), cfg["max_turns"])
    timeout = to_int(t.get("timeout"), cfg["timeout"])
    row = dict(timestamp=datetime.now().isoformat(timespec="seconds"), task_id=tid,
               project=t.get("project", ""), tier=tier_name, model=model)

    if cfg.get("needs_approval") and t.get("approved", "no").lower() != "yes":
        log(f"{tid}: tier large senza 'approved: yes' -> blocked")
        row["status"] = "blocked"
        write_usage(row)
        move(t["_path"], "blocked")
        return "blocked", 0.0
    if t.get("restricted", "yes").lower() != "yes":
        log(f"{tid}: modalita' non ristretta non abilitata in questa versione -> blocked")
        row["status"] = "blocked"
        write_usage(row)
        move(t["_path"], "blocked")
        return "blocked", 0.0

    if t.get("repo"):
        return run_repo_task(t, claude, dry_run, cfg, model, max_turns, timeout, row)

    work = D["work"] / tid
    (work / "inputs").mkdir(parents=True, exist_ok=True)
    (work / "outputs").mkdir(exist_ok=True)
    for name in ("DECISIONS.md", "ANSWERS.md"):
        (work / name).unlink(missing_ok=True)
    inputs = t.get("inputs", [])
    if isinstance(inputs, str):
        inputs = [inputs]
    for rel in inputs:
        src = Path(rel) if Path(rel).is_absolute() else BASE / rel
        if not src.exists():
            log(f"{tid}: input mancante: {src}")
            row["status"] = "failed"
            write_usage(row)
            move(t["_path"], "failed")
            return "failed", 0.0
        shutil.copy2(src, work / "inputs" / src.name)

    answers = ""
    dec_file = D["decisions"] / f"{tid}.md"
    if dec_file.exists():
        txt = dec_file.read_text(encoding="utf-8")
        if "RISPOSTA:" in txt:
            ans = txt.rsplit("RISPOSTA:", 1)[1].strip()
            if ans:
                (work / "ANSWERS.md").write_text(ans, encoding="utf-8")
                answers = ("The user answered your earlier questions in ./ANSWERS.md. "
                           "Read it first and continue the work accordingly. Do not recreate DECISIONS.md unless a new open question remains.")

    sheet = ""
    try:
        pj = scheda.progetto((t.get("project") or "").lower())
        sheet = scheda.regole_per_agenti(pj) if pj else ""
    except Exception:
        sheet = ""
    prompt = WRAPPER.replace("@@ANSWERS@@", answers + sheet + decisioni_progetto(t)).replace("@@BODY@@", t["body"])
    cmd = [claude, "-p", "--output-format", "json", "--no-session-persistence",
           "--model", model, "--effort", t.get("effort") or cfg["effort"], "--max-turns", str(max_turns),
           "--restricted", "--permission-mode", "acceptEdits", "--permission-prompts", "none"]

    if dry_run:
        log(f"[dry-run] {tid}: cwd={work}")
        log("[dry-run] " + " ".join(cmd))
        return "dry", 0.0

    log(f"{tid}: avvio (tier {tier_name}, modello {model}, max turni {max_turns}, timeout {timeout}s)")
    t0 = datetime.now()
    res_dir = D["results"] / tid
    res_dir.mkdir(parents=True, exist_ok=True)
    stamp = f"{t0:%Y%m%d_%H%M%S}"
    try:
        p = subprocess.run(cmd, input=prompt, cwd=work, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        log(f"{tid}: timeout dopo {timeout}s -> incomplete")
        row.update(status="incomplete", subtype="timeout", duration_s=timeout)
        write_usage(row)
        move(t["_path"], "incomplete")
        return "incomplete", 0.0

    (res_dir / f"raw_{stamp}.txt").write_text(p.stdout + "\n--- STDERR ---\n" + p.stderr, encoding="utf-8")
    data = parse_output(p.stdout)
    row["duration_s"] = round((datetime.now() - t0).total_seconds(), 1)

    if data is None or data.get("is_error") or p.returncode != 0:
        blob = (p.stdout + " " + p.stderr).lower()
        if any(h in blob for h in LIMIT_HINTS) or (data or {}).get("api_error_status") == 429:
            global LAST_LIMIT_TEXT
            LAST_LIMIT_TEXT = p.stdout + " " + p.stderr
            c_lim = float((data or {}).get("total_cost_usd") or 0.0)
            log(f"{tid}: limite d'uso rilevato; il task resta in coda")
            row.update(status="limit", cost_usd=round(c_lim, 4))
            write_usage(row)
            return "limit", c_lim

    cost = 0.0
    if data:
        u = data.get("usage", {})
        cost = float(data.get("total_cost_usd") or 0.0)
        row.update(subtype=data.get("subtype", ""), is_error=data.get("is_error", ""),
                   num_turns=data.get("num_turns", ""), cost_usd=round(cost, 4),
                   input_tokens=u.get("input_tokens", ""),
                   cache_creation=u.get("cache_creation_input_tokens", ""),
                   cache_read=u.get("cache_read_input_tokens", ""),
                   output_tokens=u.get("output_tokens", ""),
                   permission_denials=len(data.get("permission_denials", [])))
        (res_dir / "summary.txt").write_text(
            str(data.get("result") or "\n".join(data.get("errors", []))), encoding="utf-8")

    if work.joinpath("outputs").exists():
        shutil.copytree(work / "outputs", res_dir / "outputs", dirs_exist_ok=True)
    for name in ("DEFAULTS_LOG.md", "DOMANDE.md"):
        if (work / name).exists():
            shutil.copy2(work / name, res_dir / name)

    dec_out = work / "DECISIONS.md"
    dec_txt = dec_out.read_text(encoding="utf-8").strip() if dec_out.exists() else ""
    dec_open = bool(dec_txt) and not ("STATUS: RESOLVED" in dec_txt.upper() and "STATUS: OPEN" not in dec_txt.upper())
    if dec_txt:
        shutil.copy2(dec_out, res_dir / "DECISIONS.md")
    if data is None:
        status = "failed"
    elif data.get("subtype") == "error_max_turns":
        status = "incomplete"
    elif data.get("is_error"):
        status = "failed"
    elif dec_open:
        status = "blocked"
        D["decisions"].mkdir(exist_ok=True)
        dec_file.write_text(
            f"# Decisione richiesta: {tid}\n"
            "(Scrivi la tua risposta in fondo al file, dopo l'ultima riga di risposta. Poi sposta il file task da blocked/ a queue/.)\n\n"
            + dec_out.read_text(encoding="utf-8") + "\n\nRISPOSTA:\n", encoding="utf-8")
    else:
        status = "done"

    row["status"] = status
    write_usage(row)
    move(t["_path"], status)
    log(f"{tid}: {status} (turni {row.get('num_turns')}, costo listino {cost:.3f} USD)")
    return status, cost


def _lock_acquire():
    lock = BASE / "runner.lock"
    if lock.exists():
        age_h = (datetime.now().timestamp() - lock.stat().st_mtime) / 3600
        if age_h < LOCK_STALE_H:
            return None
        log("Lock vecchio: lo ignoro (esecuzione precedente interrotta).")
    lock.write_text(f"{os.getpid()} {datetime.now():%Y-%m-%d %H:%M:%S}", encoding="utf-8")
    return lock


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ignore-window", action="store_true", help="(non serve piu', accettato per compatibilita')")
    ap.add_argument("--window", default="", help="opzionale, es. 1-9: lavora solo in quelle ore")
    ap.add_argument("--max-tasks", type=int, default=0, help="0 = nessun limite")
    ap.add_argument("--cost-cap", type=float, default=0.0, help="USD di listino per esecuzione, 0 = nessun tetto")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--task", default="", help="esegue solo questo task (lo usa il dispatcher dell'Ufficio)")
    a = ap.parse_args()
    if a.task:
        a.max_tasks = 1

    for p in D.values():
        p.mkdir(exist_ok=True)
    if os.environ.get("ANTHROPIC_API_KEY"):
        log("ANTHROPIC_API_KEY impostata: mi fermo (userebbe l'API a pagamento).")
        return 1
    for x in comune.pulizia_avvio():
        log(f"Pulizia: {x}")
    if (BASE / "STOP").exists():
        log_once("File STOP presente (messo dal pannello): non parto. Toglilo con 'Riprendi' nel pannello.")
        return 0
    if a.window:
        lo, hi = [int(x) for x in a.window.split("-")]
        if not (lo <= datetime.now().hour < hi):
            log(f"Fuori dalla finestra {lo:02d}:00-{hi:02d}:00: non faccio nulla.")
            return 0
    (BASE / "logs" / "limit_until.txt").unlink(missing_ok=True)   # vecchio sistema (60 min fissi), sostituito da comune.py
    if not a.dry_run:
        why = comune.perche_non_parte("generico")
        if why:
            log_once(f"In pausa: {why}.")
            return 0
    claude = find_claude()
    if not claude:
        log("Programma 'claude' non trovato.")
        return 1
    lock = _lock_acquire()
    if lock is None:
        log("Un'altra esecuzione e' gia' in corso: esco.")
        return 0

    n, spent, tried = 0, 0.0, set()
    try:
        while True:
            if (BASE / "STOP").exists():
                log("File STOP presente: mi fermo.")
                break
            if not a.dry_run and n > 0:
                why = comune.perche_non_parte("generico")
                if why:
                    log(f"Mi fermo prima del prossimo task: {why}.")
                    break
                cnt = comune.contatore()
                if cnt["avviso"]:
                    log(f"Avviso: contatore d'uso al {cnt['pct']}% delle ultime 5 ore (a 100% i nuovi task aspettano).")
            if a.max_tasks and n >= a.max_tasks:
                break
            if a.cost_cap and spent >= a.cost_cap:
                log("Tetto di costo raggiunto: mi fermo.")
                break
            tasks = []
            for p in sorted(D["queue"].glob("*.task.md")):
                try:
                    tasks.append(parse_task(p))
                except Exception as e:
                    log(f"{p.name}: file non valido ({e}) -> failed")
                    move(p, "failed")
            tasks.sort(key=lambda t: (to_int(t.get("priority"), 2), t["_path"].name))
            pick, waiting = None, []
            for t in tasks:
                if t["id"] in tried or (a.task and t["id"] != a.task):
                    continue
                ok, why = ready(t)
                if ok:
                    pick = t
                    break
                waiting.append(f"{t['id']}: {why}")
            if pick is None:
                for w in waiting:
                    log(f"in attesa - {w}")
                break
            tried.add(pick["id"])
            lock.write_text(f"{os.getpid()} {datetime.now():%Y-%m-%d %H:%M:%S} {pick['id']}", encoding="utf-8")
            status, cost = run_task(pick, claude, a.dry_run)
            n += 1
            spent += cost
            if status == "limit":
                fino = comune.imposta_limite(LAST_LIMIT_TEXT, "generico")
                log(f"Fermo tutto (anche le candidature): limite di Claude. Riparto da solo dopo le {comune.quando(fino)}.")
                break
    finally:
        lock.unlink(missing_ok=True)
    log(f"Fine. Task avviati: {n}, costo stimato di listino: {spent:.3f} USD")
    return 0


if __name__ == "__main__":
    sys.exit(main())
