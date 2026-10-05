# -*- coding: utf-8 -*-
"""
Stop di una task (05/10/2026, piano UI v5 pezzo C).
- Task in coda (non ancora partita): va in "Da sistemare" (cartella failed) con il motivo di Leo.
- Task in corso: prima la si toglie dalla coda (cosi' il dispatcher non la riprende), poi si ferma SUBITO il runner
  (taskkill dell'albero di processi), si cancellano il lock del runner e i segni "in corso", e sul ramo della task
  si scartano le modifiche non salvate (git reset --hard; mai su main/master). I file nuovi non tracciati restano.
Il dispatcher, che aspettava il runner, passa da solo alla task successiva.
Il motivo resta in generico\\results\\<id>\\STOP.json (lo mostra il pannello; "Rifai" lo puo' passare all'agente).
"""
import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GEN = ROOT / "generico"
NOWIN = 0x08000000 if os.name == "nt" else 0
PROTETTI = ("main", "master")


def _git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", creationflags=NOWIN, timeout=60)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def _uccidi(pid):
    if os.name == "nt":
        p = subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", creationflags=NOWIN)
        return p.returncode == 0, (p.stdout or p.stderr or "").strip()[:200]
    try:
        os.kill(pid, 9)
        return True, ""
    except OSError as e:
        return False, str(e)


def ferma(body, parse_task, esito_task=None, diario_add=None):
    tid = str(body.get("id", "")).strip()
    motivo = str(body.get("motivo", "") or "").strip()[:1000]
    q = GEN / "queue" / f"{tid}.task.md"
    if not tid or not q.exists():
        return {"ok": False, "msg": "La task non e' in coda ne' in corso: niente da fermare."}
    try:
        t = parse_task(q)
    except Exception:
        t = {}
    try:
        att = json.loads((ROOT / "agente_attuale.json").read_text(encoding="utf-8"))
    except Exception:
        att = {}
    in_corso = att.get("id") == tid
    note = []
    # 1) motivo salvato + task fuori dalla coda (prima di fermare il runner: il dispatcher non deve riprenderla)
    res = GEN / "results" / tid
    res.mkdir(parents=True, exist_ok=True)
    (res / "STOP.json").write_text(json.dumps({"quando": datetime.now().isoformat(timespec="seconds"), "motivo": motivo,
                                               "in_corso": in_corso}, ensure_ascii=False, indent=1), encoding="utf-8")
    dest = GEN / "failed" / q.name
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        dest.unlink()
    shutil.move(str(q), str(dest))
    # 2) runner fermato subito
    if in_corso:
        lock = GEN / "runner.lock"
        pid = 0
        try:
            pid = int(lock.read_text(encoding="utf-8").split()[0])
        except Exception:
            pass
        if pid and pid != os.getpid():
            ok, msg = _uccidi(pid)
            note.append("programma fermato" if ok else f"non sono riuscito a fermare il programma ({msg})")
            time.sleep(1.5)
            for f in (ROOT / "logs" / "in_corso").glob(f"{pid}_*.json"):
                f.unlink(missing_ok=True)
        lock.unlink(missing_ok=True)
        # 3) ramo pulito: solo se siamo sul ramo della task
        repo = Path(t["repo"]) if t.get("repo") else None
        ramo = t.get("branch") or tid
        if repo and (repo / ".git").exists():
            try:
                rc, cur, _ = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
                if rc == 0 and cur == ramo and cur not in PROTETTI:
                    rc, out, _ = _git(repo, "status", "--porcelain")
                    tracciati = [l for l in out.splitlines() if l and not l.startswith("??")]
                    if tracciati:
                        _git(repo, "reset", "--hard", "HEAD")
                        note.append(f"scartate {len(tracciati)} modifiche non salvate sul ramo {ramo}")
                    else:
                        note.append(f"ramo {ramo} gia' pulito")
                else:
                    note.append(f"ramo non toccato (attivo: {cur})")
            except Exception as e:
                note.append(f"git: {e}")
    if esito_task:
        try:
            esito_task(chi="generico", progetto=(t.get("project") or "").lower(), task=tid, esito="fermata", sottotipo="stop")
        except Exception:
            pass
    if diario_add and not in_corso:      # se era in corso la riga di diario la scrive il dispatcher
        try:
            diario_add({"progetto": (t.get("project") or "").lower(), "task": tid, "titolo": t.get("title") or tid, "esito": "failed",
                        "frase": "Fermata da te" + (f": {motivo}" if motivo else ""), "pct": None, "secondi": None,
                        "dettagli": "; ".join(note), "rapporto": "", "riassunto": ""})
        except Exception:
            pass
    return {"ok": True, "msg": "Task fermata e messa in Da sistemare" + (" (" + "; ".join(note) + ")" if note else "") +
            (". Il dispatcher passa alla prossima." if in_corso else ".")}


def diario_writer(path):
    """Scrive una riga nel diario dell'Ufficio (stesso formato del dispatcher)."""
    def add(e):
        e.setdefault("quando", datetime.now().strftime("%Y-%m-%d %H:%M"))
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return add
