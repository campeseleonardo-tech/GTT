# -*- coding: utf-8 -*-
"""
Strumenti del runner per i progetti con repository git (es. Langue).
Solo libreria standard. Usati da runner.py quando un task ha il campo `repo:`.

- git: ramo del task (mai main/master), commit "[runner]" dello stato prima, commit "[agente ...]" dopo
- guardia di ambito: controlla che l'agente abbia toccato solo i file permessi
- controlli (checks) eseguiti dal runner in Python, NON dall'agente
- validatore dello schema dei contenuti (formato semplice, vedi SCHEMA nel task T02)
"""
import hashlib
import json
import os
import subprocess
from pathlib import Path

PROTECTED_BRANCHES = ("main", "master")
MAX_UNTRACKED = 300


# ---------------------------------------------------------------- git
def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {(p.stderr or p.stdout).strip()}")
    return p.stdout.strip()


def is_repo(repo):
    return Path(repo).exists() and git(repo, "rev-parse", "--is-inside-work-tree", check=False) == "true"


def current_branch(repo):
    return git(repo, "rev-parse", "--abbrev-ref", "HEAD")


def _ident(repo):
    if git(repo, "config", "user.name", check=False):
        return []
    return ["-c", "user.name=Agenti (runner)", "-c", "user.email=agenti@local"]


def _salva_albero_sporco(repo, motivo):
    """Se ci sono modifiche non committate (es. la scheda progetto riscritta dall'Ufficio), le salva in un
    commit '[runner]' sul ramo corrente, cosi' si puo' cambiare ramo senza perdere nulla."""
    if git(repo, "status", "--porcelain"):
        git(repo, "add", "-A")
        git(repo, *_ident(repo), "commit", "-q", "-m", f"[runner] salvataggio automatico: {motivo}")
        return True
    return False


def prepare_branch(repo, branch, base_branch=""):
    """Torna il nome del ramo di lavoro; lo crea a partire dal ramo corrente (o da base_branch, se indicato). Mai su main/master.
    Prima di cambiare ramo l'albero viene ripulito (commit automatico). Se il ramo esiste gia' ma non e' attivo, ci si passa sopra."""
    cur = current_branch(repo)
    if cur == branch:
        return "riusato"
    _salva_albero_sporco(repo, f"prima di passare a {branch}")
    exists = git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", check=False)
    if exists:
        git(repo, "checkout", branch)
        return f"gia' esistente: ci sono passato sopra (ero su {cur})"
    if base_branch:
        if not git(repo, "rev-parse", "--verify", "--quiet", f"refs/heads/{base_branch}", check=False):
            # tollerante: il task che crea la base e' fallito o non e' passato -> si parte dal ramo corrente e si prosegue
            git(repo, "checkout", "-b", branch)
            return f"creato (ramo di partenza {base_branch} mancante: partito da {cur})"
        git(repo, "checkout", "-b", branch, base_branch)
    else:
        git(repo, "checkout", "-b", branch)
    return "creato"


def init_repo(repo, gitignore_lines=()):
    """Per i progetti senza git (es. Preventivi): git init + commit iniziale. Equivalente di ATTIVA_GIT.bat."""
    repo = Path(repo)
    if gitignore_lines:
        f = repo / ".gitignore"
        have = f.read_text(encoding="utf-8").splitlines() if f.exists() else []
        add = [x for x in gitignore_lines if x not in have]
        if add:
            f.write_text("\n".join(have + add) + "\n", encoding="utf-8")
    git(repo, "init", "-b", "main")
    git(repo, "add", "-A")
    git(repo, *_ident(repo), "commit", "-q", "-m", "Stato iniziale (prima degli agenti)")


def diff_testo(repo, base, massimo=80000):
    """Le modifiche dell'agente rispetto alla base (senza la cartella agenti/), per rileggerle al mattino."""
    git(repo, "add", "-A")
    p = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--no-renames", "--unified=3", base, "--", ".", ":(exclude)agenti"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    t = p.stdout
    return t if len(t) <= massimo else t[:massimo] + f"\n... (diff troncato: {len(t)} caratteri in tutto)\n"


def ensure_gitignore(repo, lines):
    f = Path(repo) / ".gitignore"
    have = f.read_text(encoding="utf-8").splitlines() if f.exists() else []
    add = [x for x in lines if x not in have]
    if add:
        text = "\n".join(have + add) + "\n"
        f.write_text(text, encoding="utf-8")
    return add


def untracked_count(repo):
    out = git(repo, "ls-files", "--others", "--exclude-standard")
    return len([x for x in out.splitlines() if x.strip()])


def head(repo):
    return git(repo, "rev-parse", "HEAD")


def snapshot(repo, tid):
    """Se c'e' qualcosa di non committato, lo salva in un commit '[runner]'. Torna lo sha di base."""
    if git(repo, "status", "--porcelain"):
        git(repo, "add", "-A")
        git(repo, *_ident(repo), "commit", "-m", f"[runner] stato prima di {tid}")
    return head(repo)


def changed_files(repo, base):
    git(repo, "add", "-A")
    out = git(repo, "diff", "--cached", "--name-only", "--no-renames", base)
    return sorted(x for x in out.splitlines() if x.strip())


def out_of_scope(files, allowed):
    allowed = [a.replace("\\", "/").rstrip("/") for a in (allowed or [])]
    bad = []
    for f in files:
        if f.startswith("agenti/"):
            continue
        if not any(f == a or f.startswith(a + "/") for a in allowed):
            bad.append(f)
    return bad


def restore_paths(repo, base, files):
    """Rimette i file fuori ambito come erano alla base (o li toglie se sono nuovi)."""
    done = []
    for f in files:
        existed = git(repo, "cat-file", "-e", f"{base}:{f}", check=False, ) == "" and \
            subprocess.run(["git", "-C", str(repo), "cat-file", "-e", f"{base}:{f}"], capture_output=True).returncode == 0
        if existed:
            git(repo, "checkout", base, "--", f)
        else:
            p = Path(repo) / f
            if p.exists():
                p.unlink()
            git(repo, "rm", "--cached", "--quiet", "--ignore-unmatch", "--", f, check=False)
        done.append(f)
    git(repo, "add", "-A")
    return done


def commit_all(repo, msg):
    git(repo, "add", "-A")
    if not git(repo, "status", "--porcelain"):
        return head(repo)
    git(repo, *_ident(repo), "commit", "-m", msg)
    return head(repo)


# ---------------------------------------------------------------- schema
def validate_record(rec, schema):
    """Torna la lista degli errori (vuota = valido).
    Formato dello schema: {"comuni": {campo: spec}, "tipi": {tipo: {campo: spec}}}
    spec: {"tipo": "testo"|"intero"|"elenco_testi", "obbligatorio": true|false,
           "valori": [...], "min": n, "max": n}   (min/max: lunghezza, n. di elementi o valore)"""
    errs = []
    if not isinstance(rec, dict):
        return ["il record non e' un oggetto"]
    tipi = schema.get("tipi", {})
    t = rec.get("tipo")
    if t not in tipi:
        return [f"tipo '{t}' sconosciuto (ammessi: {', '.join(tipi)})"]
    fields = dict(schema.get("comuni", {}))
    fields.update(tipi[t])
    for name in rec:
        if name not in fields:
            errs.append(f"campo non previsto: {name}")
    for name, spec in fields.items():
        required = spec.get("obbligatorio", True)
        if name not in rec:
            if required:
                errs.append(f"campo mancante: {name}")
            continue
        v, kind = rec[name], spec.get("tipo", "testo")
        if kind == "testo":
            if not isinstance(v, str):
                errs.append(f"{name}: deve essere testo"); continue
            n = len(v.strip())
            if required and n == 0 and spec.get("min", 1) > 0:
                errs.append(f"{name}: vuoto")
            size = len(v)
        elif kind == "intero":
            if isinstance(v, bool) or not isinstance(v, int):
                errs.append(f"{name}: deve essere un intero"); continue
            size = v
        elif kind == "elenco_testi":
            if not isinstance(v, list) or not all(isinstance(x, str) and x.strip() for x in v):
                errs.append(f"{name}: deve essere un elenco di testi non vuoti"); continue
            size = len(v)
        else:
            errs.append(f"{name}: tipo di campo sconosciuto nello schema ({kind})"); continue
        if "valori" in spec and v not in spec["valori"]:
            errs.append(f"{name}: '{v}' non ammesso (ammessi: {', '.join(map(str, spec['valori']))})")
        if "min" in spec and size < spec["min"]:
            errs.append(f"{name}: troppo piccolo/corto (min {spec['min']})")
        if "max" in spec and size > spec["max"]:
            errs.append(f"{name}: troppo grande/lungo (max {spec['max']})")
    if t == "frase" and isinstance(rec.get("blocchi"), list) and isinstance(rec.get("testo_de"), str):
        if " ".join(rec["blocchi"]) != rec["testo_de"]:
            errs.append("blocchi: uniti con uno spazio non danno esattamente testo_de")
    return errs


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ---------------------------------------------------------------- controlli
def _records(repo, rel):
    data = load_json(Path(repo) / rel)
    if not isinstance(data, list):
        raise ValueError(f"{rel}: deve contenere un elenco di record")
    return data


def _check_files_exist(repo, base, args):
    return [f"manca il file {a}" for a in args if not (Path(repo) / a).exists()]


def _check_json_valid(repo, base, args):
    errs = []
    for a in args:
        try:
            load_json(Path(repo) / a)
        except Exception as e:
            errs.append(f"{a}: JSON non valido ({e})")
    return errs


def _check_schema_validate(repo, base, args):
    schema_path, files = args[0], args[1:]
    schema = load_json(Path(repo) / schema_path)
    errs = []
    for f in files:
        for i, rec in enumerate(_records(repo, f)):
            for e in validate_record(rec, schema):
                errs.append(f"{f} [{i}] {rec.get('id', '?') if isinstance(rec, dict) else '?'}: {e}")
    return errs


def _check_schema_selftest(repo, base, args):
    schema = load_json(Path(repo) / args[0])
    valid = _records(repo, args[1])
    wrong = _records(repo, args[2])
    errs = []
    if not valid:
        errs.append("nessun esempio valido")
    if not wrong:
        errs.append("nessun esempio sbagliato")
    seen = {r.get("tipo") for r in valid if isinstance(r, dict)}
    for t in schema.get("tipi", {}):
        if t not in seen:
            errs.append(f"manca un esempio valido per il tipo '{t}'")
    for i, r in enumerate(valid):
        for e in validate_record(r, schema):
            errs.append(f"esempio valido #{i} rifiutato: {e}")
    for i, r in enumerate(wrong):
        if not validate_record(r, schema):
            errs.append(f"esempio sbagliato #{i} accettato (dovrebbe essere rifiutato)")
    return errs


def _check_count_equals(repo, base, args):
    n = len(_records(repo, args[0]))
    return [] if n == int(args[1]) else [f"{args[0]}: {n} record invece di {args[1]}"]


def _check_count_between(repo, base, args):
    n = len(_records(repo, args[0]))
    lo, hi = int(args[1]), int(args[2])
    return [] if lo <= n <= hi else [f"{args[0]}: {n} record, attesi tra {lo} e {hi}"]


def _check_no_duplicates(repo, base, args):
    field, files = args[0], args[1:]
    seen, errs = {}, []
    for f in files:
        for r in _records(repo, f):
            key = str(r.get(field, "")).strip().lower()
            if key in seen:
                errs.append(f"duplicato '{key}' ({seen[key]} e {f})")
            seen.setdefault(key, f)
    return errs


def _check_unique_ids(repo, base, args):
    seen, errs = set(), []
    for f in args:
        for r in _records(repo, f):
            if r.get("id") in seen:
                errs.append(f"id duplicato: {r.get('id')}")
            seen.add(r.get("id"))
    return errs


def _check_join_equals(repo, base, args):
    f, list_field, text_field = args
    errs = []
    for r in _records(repo, f):
        if " ".join(r.get(list_field, [])) != r.get(text_field):
            errs.append(f"{r.get('id', '?')}: unendo '{list_field}' non si ottiene '{text_field}'")
    return errs


def _check_field_equals_all(repo, base, args):
    f, field, value = args
    return [f"{r.get('id', '?')}: {field} = '{r.get(field)}' invece di '{value}'"
            for r in _records(repo, f) if r.get(field) != value]


def _check_fields_differ(repo, base, args):
    f, a, b = args
    return [f"{r.get('id', '?')}: '{a}' e '{b}' sono uguali" for r in _records(repo, f) if r.get(a) == r.get(b)]


def _check_git_unchanged(repo, base, args):
    errs = []
    for a in args:
        if git(repo, "diff", "--cached", "--name-only", "--no-renames", base, "--", a):
            errs.append(f"{a} e' stato modificato (non doveva)")
    return errs


def _check_node(repo, base, args):
    """Sintassi JavaScript con `node --check` (non esegue il codice)."""
    errs = []
    for a in args:
        p = Path(repo) / a
        if not p.exists():
            errs.append(f"{a}: file mancante")
            continue
        try:
            r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        except Exception as e:
            errs.append(f"{a}: node non disponibile ({e})")
            continue
        if r.returncode != 0:
            errs.append(f"{a}: errore di sintassi: " + ((r.stderr or r.stdout).strip().splitlines() or ["?"])[0][:200])
    return errs


def _check_pycompile(repo, base, args):
    """Sintassi Python senza eseguire niente."""
    import ast
    errs = []
    for a in args:
        try:
            ast.parse((Path(repo) / a).read_text(encoding="utf-8"))
        except Exception as e:
            errs.append(f"{a}: {e}")
    return errs


NOWIN = 0x08000000 if os.name == "nt" else 0   # niente finestre nere su Windows


def _check_run_py(repo, base, args):
    """Lancia uno script Python del progetto (es. GTT: scripts/04_genera_mappa.py) dalla sua cartella.
    Errore se esce con codice diverso da 0. Uso: run_py:scripts/04_genera_mappa.py"""
    import sys
    errs = []
    py = sys.executable
    if py.lower().endswith("pythonw.exe"):
        cand = py[:-len("pythonw.exe")] + "python.exe"
        if Path(cand).exists():
            py = cand
    for a in args:
        sp = (Path(repo) / a).resolve()
        if not sp.exists():
            errs.append(f"{a}: script mancante")
            continue
        try:
            r = subprocess.run([py, str(sp)], cwd=str(sp.parent), capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=900, creationflags=NOWIN)
        except subprocess.TimeoutExpired:
            errs.append(f"{a}: non ha finito entro 15 minuti")
            continue
        except Exception as e:
            errs.append(f"{a}: impossibile lanciarlo ({e})")
            continue
        logdir = Path(repo) / "agenti"
        logdir.mkdir(exist_ok=True)
        (logdir / "ULTIMO_SCRIPT.txt").write_text(f"{a} -> exit {r.returncode}\n\n{r.stdout[-6000:]}\n--- STDERR ---\n{r.stderr[-6000:]}",
                                                  encoding="utf-8")
        if r.returncode != 0:
            tail = [x for x in (r.stderr or r.stdout).strip().splitlines() if x.strip()][-3:]
            errs.append(f"{a}: exit {r.returncode}: " + " | ".join(tail)[:400])
    return errs


def _check_html_js(repo, base, args):
    """Sintassi del JavaScript scritto dentro una pagina HTML (blocchi <script> senza src), con `node --check`.
    Non esegue niente. Uso: html_js_check:scripts/mappa_template.html"""
    import re
    import tempfile
    errs = []
    for a in args:
        p = Path(repo) / a
        if not p.exists():
            errs.append(f"{a}: file mancante")
            continue
        html = p.read_text(encoding="utf-8", errors="replace")
        for i, m in enumerate(re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S | re.I), 1):
            code = m.group(1)
            if not code.strip():
                continue
            riga0 = html.count("\n", 0, m.start(1))
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as fh:
                fh.write("\n" * riga0 + code)     # stessi numeri di riga della pagina
                tmp = fh.name
            try:
                r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=120, creationflags=NOWIN)
            except Exception as e:
                errs.append(f"{a}: node non disponibile ({e})")
                break
            finally:
                Path(tmp).unlink(missing_ok=True)
            if r.returncode != 0:
                out = (r.stderr or r.stdout).strip().splitlines()
                where = next((x for x in out if ".js:" in x), "")
                riga = where.rsplit(":", 1)[-1] if where else "?"
                msg = next((x for x in out if "Error" in x), out[-1] if out else "?")
                errs.append(f"{a}: blocco <script> n.{i}, riga {riga}: {msg[:200]}")
    return errs


def _check_min_chars(repo, base, args):
    """min_chars:file;N - il file esiste e ha almeno N caratteri (utile per rapporti e documenti)."""
    errs = []
    try:
        f, n = Path(repo) / args[0], int(args[1])
    except Exception:
        return ["min_chars: servono file;N"]
    if not f.is_file():
        return [f"{args[0]}: file mancante"]
    k = len(f.read_text(encoding="utf-8", errors="replace").strip())
    if k < n:
        errs.append(f"{args[0]}: troppo corto ({k} caratteri, ne servono almeno {n})")
    return errs


def _check_contains_all(repo, base, args):
    """contains_all:file;testo1;testo2 - il file contiene tutti i testi indicati (es. i titoli delle sezioni richieste)."""
    f = Path(repo) / args[0]
    if not f.is_file():
        return [f"{args[0]}: file mancante"]
    t = f.read_text(encoding="utf-8", errors="replace")
    return [f"{args[0]}: manca «{x}»" for x in args[1:] if x not in t]


def _check_not_contains(repo, base, args):
    """not_contains:file;testo1;testo2 - il file NON contiene i testi indicati (es. i vecchi nomi degli strumenti)."""
    f = Path(repo) / args[0]
    if not f.is_file():
        return [f"{args[0]}: file mancante"]
    t = f.read_text(encoding="utf-8", errors="replace")
    return [f"{args[0]}: contiene ancora «{x}»" for x in args[1:] if x in t]


CHECKS = {
    "min_chars": _check_min_chars, "contains_all": _check_contains_all, "not_contains": _check_not_contains,
    "files_exist": _check_files_exist, "json_valid": _check_json_valid, "node_check": _check_node, "py_compile": _check_pycompile,
    "schema_validate": _check_schema_validate, "schema_selftest": _check_schema_selftest,
    "count_equals": _check_count_equals, "count_between": _check_count_between,
    "no_duplicates": _check_no_duplicates, "unique_ids": _check_unique_ids,
    "join_equals": _check_join_equals, "field_equals_all": _check_field_equals_all,
    "git_unchanged": _check_git_unchanged, "fields_differ": _check_fields_differ,
    "run_py": _check_run_py, "html_js_check": _check_html_js,
}


def run_checks(repo, base, specs):
    """specs: lista di 'nome:arg1;arg2'. Torna lista di (spec, [errori])."""
    git(repo, "add", "-A")      # git_unchanged confronta l'area di staging con la base
    out = []
    for spec in specs or []:
        name, _, rest = spec.partition(":")
        args = [x.strip() for x in rest.split(";") if x.strip()]
        fn = CHECKS.get(name.strip())
        if not fn:
            out.append((spec, [f"controllo sconosciuto: {name}"]))
            continue
        try:
            out.append((spec, fn(repo, base, args)))
        except Exception as e:
            out.append((spec, [f"errore nel controllo: {e}"]))
    return out
