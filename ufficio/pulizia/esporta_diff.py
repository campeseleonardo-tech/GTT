# -*- coding: utf-8 -*-
"""SOLO LETTURA: copia in pulizia\\diff\\ il DIFF.patch e il RAPPORTO.md delle task delle ultime 24 ore,
leggendoli dai loro rami (senza cambiare ramo). Serve a Claude per controllare il lavoro degli agenti."""
import subprocess, time
from pathlib import Path
DESK = Path.home() / "Desktop"
REPO = [DESK / "Langue", DESK / "GTT", DESK / "timelive_repo", DESK / "Projects" / "Preventivi_Gigi"]
OUT = Path(__file__).with_name("diff"); OUT.mkdir(exist_ok=True)
def git(r, *a):
    p = subprocess.run(["git", "-C", str(r), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout if p.returncode == 0 else None
n = 0
for r in REPO:
    refs = git(r, "for-each-ref", "--format=%(refname:short) %(committerdate:unix)", "refs/heads") or ""
    for riga in refs.splitlines():
        ramo, t = riga.rsplit(" ", 1)
        if time.time() - int(t) > 86400 or "risposta" in ramo or ramo in ("main", "master"):
            continue
        for nome in ("DIFF.patch", "RAPPORTO.md"):
            txt = git(r, "show", f"{ramo}:agenti/{ramo}/{nome}")
            if txt:
                (OUT / f"{ramo}__{nome}").write_text(txt, encoding="utf-8"); n += 1
print(f"Fatto: {n} file in {OUT}")
