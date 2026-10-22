#!/usr/bin/env python3
"""
controlla_rami.py  -  le versioni locale e su GitHub sono le stesse? Ci sono rami con lavoro non unito? (solo lettura)

Cosa fa
-------
  1. Scarica da GitHub lo stato dei rami (git fetch --prune; se la copia ha la storia tagliata, la completa).
  2. Dice su che ramo sei, se ci sono modifiche non salvate e se il ramo locale e' avanti o indietro rispetto a GitHub.
  3. Per ogni ramo (locale e su GitHub) elenca i commit che NON sono in origin/prova: sono lavori non ancora uniti.
Non cambia nessun file e nessun ramo.

Come si lancia
--------------
  python scripts\\controlla_rami.py            (oppure doppio clic su scripts\\CONTROLLA_RAMI.bat)
  Codice di uscita 0 = tutto allineato; 1 = c'e' qualcosa da guardare.
"""
import subprocess
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
RIFERIMENTO = "origin/prova"


def git(*args):
    r = subprocess.run(["git", *args], cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def main():
    da_guardare = 0
    git("fetch", "--prune", "origin")
    if git("rev-parse", "--is-shallow-repository") == "true":
        print("La copia aveva la storia tagliata: la completo (serve per confronti giusti).")
        git("fetch", "--unshallow", "origin")

    ramo = git("rev-parse", "--abbrev-ref", "HEAD")
    print(f"Ramo attuale: {ramo}")
    modifiche = git("status", "--porcelain")
    if modifiche:
        da_guardare += 1
        print(f"  ATTENZIONE: {len(modifiche.splitlines())} file modificati e non salvati (commit) su questo PC")
    if git("ls-remote", "--heads", "origin", ramo):
        avanti, indietro = git("rev-list", "--left-right", "--count", f"{ramo}...origin/{ramo}").split()
        if avanti == indietro == "0":
            print(f"  OK: {ramo} uguale a GitHub")
        else:
            da_guardare += 1
            print(f"  ATTENZIONE: {ramo} ha {avanti} commit non inviati a GitHub e {indietro} commit di GitHub non scaricati")
    else:
        da_guardare += 1
        print(f"  ATTENZIONE: il ramo {ramo} non esiste su GitHub")

    print(f"\nRami con lavoro non presente in {RIFERIMENTO}:")
    rami = [r for r in git("for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes/origin").splitlines()
            if r not in ("origin", "origin/HEAD", RIFERIMENTO)]
    trovati = 0
    for r in sorted(rami):
        commit = git("log", "--format=%h %ad %s", "--date=short", f"{RIFERIMENTO}..{r}")
        if not commit:
            continue
        trovati += 1
        righe = commit.splitlines()
        print(f"  {r}: {len(righe)} commit")
        for c in righe[:5]:
            print(f"      {c[:110]}")
        if len(righe) > 5:
            print(f"      ... e altri {len(righe) - 5}")
    if trovati:
        da_guardare += 1
        print("  -> controllare con Claude se vanno uniti o se sono superati")
    else:
        print("  nessuno: tutto il lavoro e' in prova")

    print("\nRISULTATO:", "tutto allineato" if da_guardare == 0 else f"{da_guardare} cose da guardare")
    return 0 if da_guardare == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
