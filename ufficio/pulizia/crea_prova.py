# -*- coding: utf-8 -*-
"""Crea (o ricrea) in ogni progetto un ramo 'prova' = main + il lavoro buono degli agenti, per provarlo.
- main NON viene toccato; i rami delle task NON vengono toccati; 'prova' si puo' ricreare quando si vuole.
- Se due lavori litigano sulle stesse righe (conflitto), quel ramo viene saltato e scritto nel rapporto.
- Alla fine il progetto resta sul ramo 'prova' (cosi' Leo apre i file e prova). La prossima task degli agenti
  torna da sola sul proprio ramo.
- Le modifiche non salvate della scheda progetto vengono messe da parte (git stash), non cancellate.
Rapporto: PROVA_RAMI.txt accanto a questo file."""
import subprocess
from datetime import datetime
from pathlib import Path

DESK = Path.home() / "Desktop"
# ordine = priorita': in caso di conflitto vince il primo
RAMI = {
    "Langue": (DESK / "Langue", ["T22-ripasso-fix", "T23-risposta1", "T23-risposta2"]),
    "GTT": (DESK / "GTT", ["GT14-verifica-passaggi", "GT13-altre-citta", "GT05-risposta2", "GT04-risposta1"]),
    "Timelive": (DESK / "timelive_repo", ["TL06-risposta1", "TL06-log-ollama", "TL07-risposta1", "TL07-bridge-v2"]),
    "Preventivi": (DESK / "Projects" / "Preventivi_Gigi", ["PV04-controllo", "PV03-istruzioni"]),
}
SERVIZIO = {"PROGETTO.md", "MEMORIA_PROGETTO.md", "agenti/LOG.md", "agenti/ULTIMO_SCRIPT.txt"}
ID = ["-c", "user.name=Ufficio", "-c", "user.email=ufficio@locale"]
out = [f"Ramo 'prova' - {datetime.now():%Y-%m-%d %H:%M}", ""]


def git(repo, *a):
    p = subprocess.run(["git", *ID, "-C", str(repo), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


for nome, (repo, rami) in RAMI.items():
    out.append(f"=== {nome}")
    if not (repo / ".git").exists():
        out.append("  non e' un repo git: salto"); continue
    rc, st, _ = git(repo, "status", "--porcelain")
    sporchi = [l for l in st.splitlines() if l.strip() and not l.startswith("??")]
    if sporchi:
        rc, o, e = git(repo, "stash", "push", "-m", "prima di crea_prova")
        out.append(f"  messe da parte {len(sporchi)} modifiche non salvate (git stash): " + ", ".join(l.split(maxsplit=1)[-1] for l in sporchi))
        if rc:
            out.append(f"  ERRORE stash ({e[:150]}): salto il progetto"); continue
    rc, _, e = git(repo, "checkout", "-B", "prova", "main")
    if rc:
        out.append(f"  ERRORE: non riesco a creare 'prova' da main ({e[:150]})"); continue
    for r in rami:
        rc, _, _ = git(repo, "rev-parse", "--verify", "--quiet", r)
        if rc:
            out.append(f"  - {r}: ramo non trovato"); continue
        rc, o, e = git(repo, "merge", "--no-edit", "--no-ff", r)
        if rc:
            _, conf, _ = git(repo, "diff", "--name-only", "--diff-filter=U")
            files = [f for f in conf.splitlines() if f.strip()]
            # file di servizio dell'Ufficio (scheda progetto, registri degli agenti): non sono lavoro, tengo la versione di 'prova'
            servizio = [f for f in files if f in SERVIZIO]
            if files and len(servizio) == len(files):
                for f in files:
                    git(repo, "checkout", "--ours", "--", f)
                    git(repo, "add", "--", f)
                rc2, _, e2 = git(repo, "commit", "--no-edit")
                if rc2 == 0:
                    out.append(f"  - {r}: unito (conflitti solo su file di servizio, tenuta la versione di 'prova': {', '.join(files)})")
                    continue
            git(repo, "merge", "--abort")
            out.append(f"  - {r}: SALTATO per conflitto su: {', '.join(files) or e[:120]}")
        else:
            out.append(f"  - {r}: unito")
    _, log, _ = git(repo, "log", "--oneline", "-1")
    out.append(f"  ora il progetto e' sul ramo 'prova' ({log[:80]})")
    out.append("")
dest = Path(__file__).with_name("PROVA_RAMI.txt")
dest.write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
