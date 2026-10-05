# -*- coding: utf-8 -*-
"""Controllo SOLO LETTURA dei repo dell'Ufficio (05/10/2026). Non cambia niente: non fa checkout, non cancella, non committa.
Scrive il risultato in CONTROLLO_REPO.txt accanto a questo file."""
import subprocess
from datetime import datetime
from pathlib import Path

DESK = Path.home() / "Desktop"
REPO = {"Langue": DESK / "Langue", "GTT": DESK / "GTT", "Timelive": DESK / "timelive_repo",
        "Preventivi": DESK / "Projects" / "Preventivi_Gigi"}
# file da provare su un ramo preciso (senza cambiare ramo: si legge con git show)
PROVE = [("Timelive", "TL05-log-ollama", "code/llm_bridge.py"),
         ("Preventivi", "PV02-generatore", "strumenti/genera_preventivo.py")]
out = [f"Controllo repo - {datetime.now():%Y-%m-%d %H:%M}", ""]


def git(repo, *a):
    p = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (p.stdout or "").strip(), (p.stderr or "").strip(), p.returncode


for nome, r in REPO.items():
    out.append(f"=== {nome} ({r})")
    if not (r / ".git").exists():
        out.append("  non e' un repo git")
        continue
    cur, _, _ = git(r, "rev-parse", "--abbrev-ref", "HEAD")
    out.append(f"  ramo attivo: {cur}")
    st, _, _ = git(r, "status", "--porcelain")
    righe = [l for l in st.splitlines() if l.strip()]
    out.append(f"  modifiche non salvate: {len(righe)}")
    out += ["    " + l for l in righe[:20]]
    br, _, _ = git(r, "for-each-ref", "--sort=-committerdate", "--format=%(refname:short) | %(committerdate:short) | %(subject)", "refs/heads")
    out.append("  rami (piu' recenti prima):")
    out += ["    " + l[:150] for l in br.splitlines()[:40]]
    out.append("")
out.append("=== Prove di compilazione (lettura dal ramo, senza cambiare ramo)")
for nome, ramo, f in PROVE:
    src, err, rc = git(REPO[nome], "show", f"{ramo}:{f}")
    if rc:
        out.append(f"  {nome} {ramo}:{f} -> non trovato ({err[:120]})")
        continue
    try:
        compile(src, f, "exec")
        out.append(f"  {nome} {ramo}:{f} -> OK, si compila ({len(src.splitlines())} righe)")
    except SyntaxError as e:
        out.append(f"  {nome} {ramo}:{f} -> ERRORE alla riga {e.lineno}: {e.msg}")
    d, _, _ = git(REPO[nome], "diff", "--stat", f"{ramo}~1", ramo)
    out.append("    ultimo commit del ramo: " + " / ".join(d.splitlines()[-3:]))
dest = Path(__file__).with_name("CONTROLLO_REPO.txt")
dest.write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
print(f"\nScritto in {dest}")
