# -*- coding: utf-8 -*-
"""Carica su GitHub (repo PRIVATO 'multiple-agents') una COPIA di Ufficio + progetti (05/10/2026).
Gli originali non vengono toccati: si copia tutto in C:\\GITHUB_UFFICIO\\multiple-agents e si carica da li'.
Si puo' rilanciare quando vuoi: aggiorna la copia e carica solo le differenze.
Esclusi: cartelle .git e __pycache__, file sopra 50 MB, file che contengono chiavi API (elencati in NON_CARICATI.md).
"""
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

UTENTE = "campeseleonardo-tech"
NOME_REPO = "multiple-agents"
UFF = Path(os.environ.get("BK_UFFICIO") or Path(__file__).resolve().parent.parent)
COPIA = Path(os.environ.get("GH_COPIA") or r"C:\GITHUB_UFFICIO") / NOME_REPO
REMOTO = os.environ.get("GH_REMOTO") or f"https://github.com/{UTENTE}/{NOME_REPO}.git"
MAX_MB = 50
SALTA_DIR = {".git", "__pycache__", "node_modules", ".venv", "venv", ".ipynb_checkpoints"}
SALTA_FILE = {"chiavi.json"}
# forme tipiche delle chiavi API (OpenRouter, Anthropic, Groq, Google, Cerebras, GitHub, OpenAI)
CHIAVE = re.compile(r"(sk-or-v1-[0-9a-f]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{30,}|"
                    r"csk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-proj-[A-Za-z0-9_-]{20,})")
TESTO = {".py", ".js", ".json", ".jsonl", ".txt", ".md", ".bat", ".ps1", ".vbs", ".html", ".css", ".csv", ".log", ".env",
         ".ini", ".cfg", ".toml", ".yaml", ".yml", ".ts", ""}

esclusi = []


def say(*a):
    print(*a, flush=True)


def git(*a, cwd=None, mostra=False):
    p = subprocess.run(["git", *a], cwd=str(cwd or COPIA), capture_output=not mostra, text=True,
                       encoding="utf-8", errors="replace")
    return (p.stdout or "").strip(), (p.stderr or "").strip(), p.returncode


def ha_chiave(p):
    if p.suffix.lower() not in TESTO or p.stat().st_size > 5 * 1024 * 1024:
        return False
    try:
        return bool(CHIAVE.search(p.read_text(encoding="utf-8", errors="ignore")))
    except Exception:
        return False


def copia_albero(src, dst):
    n = 0
    for r, ds, fs in os.walk(src):
        ds[:] = [d for d in ds if d not in SALTA_DIR]
        rel = Path(r).relative_to(src)
        for f in fs:
            p = Path(r) / f
            q = rel / f
            try:
                mb = p.stat().st_size / 1024 ** 2
                if f in SALTA_FILE:
                    esclusi.append((dst.name, q, "file delle chiavi"))
                    continue
                if f.endswith((".pyc", "-wal", "-shm", "-journal")):
                    continue
                if mb > MAX_MB:
                    esclusi.append((dst.name, q, f"{mb:.0f} MB (oltre {MAX_MB} MB)"))
                    continue
                if ha_chiave(p):
                    esclusi.append((dst.name, q, "contiene una chiave API"))
                    continue
                (dst / rel).mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst / q)
                n += 1
            except Exception as e:
                esclusi.append((dst.name, q, f"non leggibile: {type(e).__name__}"))
    return n


def progetti():
    out, visti = [], set()
    for f in sorted((UFF / "progetti").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        c = Path(d.get("cartella") or "")
        if not str(c) or not c.exists():
            continue
        try:
            c.resolve().relative_to(UFF.resolve())
            continue                                   # gia' dentro la cartella dell'Ufficio
        except ValueError:
            pass
        k = str(c.resolve()).lower()
        if k not in visti:
            visti.add(k)
            out.append((d.get("id") or f.stem, d.get("nome") or f.stem, c))
    return out


def main():
    say("=" * 70)
    say(f" CARICAMENTO SU GITHUB (privato): {UTENTE}/{NOME_REPO}")
    say("=" * 70)
    say(f" Copia di lavoro: {COPIA}   (gli originali non vengono toccati)")
    if not (UFF / "motori.py").exists():
        say("ERRORE: lo script deve stare in Multiple Agents\\pulizia.")
        return 1
    _, _, rc = git("--version", cwd=UFF)
    if rc:
        say("ERRORE: git non trovato.")
        return 1

    # 1) svuota la copia (tranne .git) e ricopia tutto
    COPIA.mkdir(parents=True, exist_ok=True)
    for x in COPIA.iterdir():
        if x.name != ".git":
            shutil.rmtree(x) if x.is_dir() else x.unlink()
    say("\n[1/4] Copio l'Ufficio...")
    say(f"      {copia_albero(UFF, COPIA / 'ufficio')} file")
    pj = progetti()
    righe_rami = [f"# Stato git dei progetti al {datetime.now():%d/%m/%Y %H:%M}", "",
                  "Qui c'e' solo la copia dei file del ramo attivo. Storia e rami completi: repo locali sul PC e backup (.bundle).", ""]
    say(f"\n[2/4] Copio i progetti ({len(pj)})...")
    for pid, nome, c in pj:
        n = copia_albero(c, COPIA / "progetti" / pid)
        say(f"      {nome}: {n} file")
        righe_rami.append(f"## {nome} (`progetti/{pid}`, originale `{c}`)")
        if (c / ".git").exists():
            cur, _, _ = git("rev-parse", "--abbrev-ref", "HEAD", cwd=c)
            st, _, _ = git("status", "--porcelain", cwd=c)
            br, _, _ = git("for-each-ref", "--sort=-committerdate",
                           "--format=- `%(refname:short)` %(committerdate:short) %(subject)", "refs/heads", cwd=c)
            righe_rami += [f"Ramo copiato: `{cur}` - modifiche non salvate incluse: {len(st.splitlines())}", "", br, ""]
        else:
            righe_rami += ["Non e' un repo git.", ""]
    (COPIA / "RAMI_PROGETTI.md").write_text("\n".join(righe_rami) + "\n", encoding="utf-8")
    nc = ["# File NON caricati su GitHub", "", f"Restano sul PC e nel backup (C:\\BACKUP_UFFICIO). Aggiornato {datetime.now():%d/%m/%Y %H:%M}.", "",
          "| dove | file | motivo |", "|---|---|---|"] + [f"| {a} | `{b}` | {m} |" for a, b, m in esclusi]
    (COPIA / "NON_CARICATI.md").write_text("\n".join(nc) + "\n", encoding="utf-8")
    (COPIA / "LEGGIMI.md").write_text(f"""# multiple-agents (copia privata)

COPIA dell'Ufficio multi-agente di Leo e dei suoi progetti, aggiornata con `ufficio/pulizia/CARICA_SU_GITHUB.bat`.
I file VERI stanno sul PC di Leo: le modifiche fatte qui NON tornano da sole sul PC.

- `ufficio/` = cartella `{UFF}` (pannello, motori, task, log)
- `progetti/<id>/` = stato attuale di ogni progetto (solo il ramo attivo, vedi `RAMI_PROGETTI.md`)
- `NON_CARICATI.md` = file esclusi (troppo grandi o con chiavi API)
- Chiavi API: mai qui. Stanno in `%USERPROFILE%\\.ufficio\\chiavi.json` sul PC.
""", encoding="utf-8")
    say(f"      esclusi: {len(esclusi)} file (vedi NON_CARICATI.md)")
    for a, b, m in esclusi:
        say(f"        - {a}/{b}: {m}")

    # 2) commit
    say("\n[3/4] Salvo la versione (commit)...")
    if not (COPIA / ".git").exists():
        git("init")
        git("checkout", "-b", "main")
        git("remote", "add", "origin", REMOTO)
    if not git("config", "user.email")[0]:
        git("config", "user.name", "Leo")
        git("config", "user.email", "campese.leonardo@gmail.com")
    git("config", "core.autocrlf", "false")
    git("config", "core.quotepath", "false")
    git("add", "-A")
    st, _, _ = git("status", "--porcelain")
    if st:
        _, err, rc = git("commit", "-q", "-m", f"Copia Ufficio + progetti {datetime.now():%Y-%m-%d %H:%M}")
        if rc:
            say("ERRORE nel commit: " + err[:300])
            return 1
        say(f"      {len(st.splitlines())} file nuovi o cambiati")
    else:
        say("      nessuna differenza dall'ultima volta")

    # 3) push
    say("\n[4/4] Carico su GitHub...")
    _, err, rc = git("ls-remote", "origin")
    if rc:
        say("\n  Non trovo il repo su GitHub (o non hai ancora fatto l'accesso).")
        say("  1. Vai su https://github.com/new")
        say(f"  2. Nome: {NOME_REPO}  -  scegli PRIVATE  -  NON aggiungere README, .gitignore o licenza")
        say("  3. Premi 'Create repository' e poi rilancia questo file.")
        say("  (Se il repo esiste gia': si aprira' una finestra di accesso a GitHub, accedi e rilancia.)")
        say("  Dettaglio: " + err[:200])
        return 2
    _, err, rc = git("push", "-u", "origin", "main", mostra=True)
    if rc:
        say("ERRORE nel caricamento. Copia questo messaggio a Claude.")
        return 1
    say("")
    say("=" * 70)
    say(f" FATTO: https://github.com/{UTENTE}/{NOME_REPO}")
    say("=" * 70)
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say(f"\nERRORE inatteso: {e}. Gli originali non sono stati toccati.")
        rc = 1
    sys.exit(rc)
