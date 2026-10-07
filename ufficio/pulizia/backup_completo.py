# -*- coding: utf-8 -*-
"""Backup COMPLETO dell'Ufficio e dei progetti (05/10/2026).
SOLO LETTURA sulle cartelle originali: non cambia ramo, non committa, non cancella niente.
Crea  C:\\BACKUP_UFFICIO\\<data_ora>\\  con:
  ufficio.zip                 tutta la cartella Multiple Agents (anche i vecchi _backup)
  progetti\\<id>.zip           la cartella di ogni progetto, con .git, dati e file non tracciati
  progetti\\<id>.bundle        storia git con TUTTI i rami e lo stash (per ripristinare anche solo i rami)
  chiavi_PRIVATE\\             le chiavi API (cartella .ufficio): NON caricare mai su GitHub
  INVENTARIO.md               cosa c'e' dentro, generato automaticamente
  COME_RIPRISTINARE.md        come rimettere tutto a posto
  CONTROLLO.txt               esito dei controlli (zip leggibili, bundle verificati, impronte sha256)
"""
import csv
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:
    pass

UFF = Path(os.environ.get("BK_UFFICIO") or Path(__file__).resolve().parent.parent)        # cartella Multiple Agents
RADICE = Path(os.environ.get("BK_DEST") or r"C:\BACKUP_UFFICIO")
CHIAVI = Path(os.environ.get("BK_CHIAVI") or (Path.home() / ".ufficio"))
DEST = RADICE / datetime.now().strftime("%Y-%m-%d_%H%M")
SALTA_DIR = {"__pycache__", "node_modules", ".venv", "venv"}
DB_EST = {".sqlite", ".sqlite3", ".db"}

saltati = []          # file non letti (bloccati ecc.)
controlli = []        # righe per CONTROLLO.txt
tutto_ok = True


def say(*a):
    print(*a, flush=True)


def umano(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024


def peso(cartella):
    tot = 0
    for r, ds, fs in os.walk(cartella):
        ds[:] = [d for d in ds if d not in SALTA_DIR]
        for f in fs:
            try:
                tot += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return tot


def git(repo, *a):
    p = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (p.stdout or "").strip(), (p.stderr or "").strip(), p.returncode


def copia_db(src):
    """Copia coerente di un database SQLite anche se e' in uso (es. raccolta GTT che scrive)."""
    tmp = Path(tempfile.mkdtemp()) / src.name
    s = sqlite3.connect(f"file:{src}?mode=ro", uri=True, timeout=30)
    d = sqlite3.connect(tmp)
    with d:
        s.backup(d)
    s.close()
    d.close()
    return tmp


def zippa(cartella, zip_path):
    n = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, allowZip64=True, compresslevel=6) as z:
        for r, ds, fs in os.walk(cartella):
            ds[:] = [d for d in ds if d not in SALTA_DIR]
            for f in fs:
                p = Path(r) / f
                arc = str(p.relative_to(cartella.parent))
                try:
                    if p.suffix.lower() in DB_EST and not p.name.endswith(("-wal", "-shm", "-journal")):
                        try:
                            t = copia_db(p)
                            z.write(t, arc)
                            shutil.rmtree(t.parent, ignore_errors=True)
                            n += 1
                            continue
                        except Exception:
                            pass            # non e' un SQLite valido: copia normale
                    z.write(p, arc)
                    n += 1
                except Exception as e:
                    saltati.append(f"{p} -> {type(e).__name__}: {e}")
    return n


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def prima_riga_doc(p):
    """Prima riga utile della descrizione di un file (docstring Python, rem dei .bat, titolo dei .md)."""
    try:
        t = p.read_text(encoding="utf-8", errors="replace")[:3000]
    except Exception:
        return ""
    if p.suffix == ".py":
        for q in ('"""', "'''"):
            i = t.find(q)
            if i != -1 and i < 400:
                j = t.find(q, i + 3)
                righe = [x.strip() for x in t[i + 3:j].splitlines() if x.strip()]
                return righe[0][:160] if righe else ""
        for x in t.splitlines():
            if x.startswith("#") and "coding" not in x:
                return x.lstrip("# ").strip()[:160]
    if p.suffix in (".bat", ".cmd"):
        for x in t.splitlines():
            s = x.strip()
            if s.lower().startswith(("rem ", "::")):
                return s[3:].strip()[:160] if s.lower().startswith("rem") else s[2:].strip()[:160]
        cmd = [x.strip() for x in t.splitlines() if x.strip() and not x.strip().startswith("@") and not x.lower().startswith(("cd ", "echo", "pause"))]
        return ("esegue: " + cmd[0])[:160] if cmd else ""
    if p.suffix in (".md", ".txt"):
        for x in t.splitlines():
            if x.strip():
                return x.strip().lstrip("# ")[:160]
    return ""


# ----------------------------------------------------------------------------------------------------------------
def progetti():
    out = []
    for f in sorted((UFF / "progetti").glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            out.append({"id": f.stem, "errore": str(e)})
            continue
        out.append({"id": d.get("id") or f.stem, "nome": d.get("nome", f.stem), "cartella": d.get("cartella", ""),
                    "motore": d.get("motore", ""), "stato": d.get("stato", ""), "obiettivo": d.get("obiettivo", ""),
                    "n_task": len(d.get("task") or []) if isinstance(d.get("task"), list) else ""})
    return out


def dentro(p, base):
    try:
        Path(p).resolve().relative_to(Path(base).resolve())
        return True
    except Exception:
        return False


def info_repo(r):
    if not (Path(r) / ".git").exists():
        return None
    cur, _, _ = git(r, "rev-parse", "--abbrev-ref", "HEAD")
    st, _, _ = git(r, "status", "--porcelain")
    br, _, _ = git(r, "for-each-ref", "--sort=-committerdate",
                   "--format=%(refname:short) | %(committerdate:short) | %(subject)", "refs/heads")
    sl, _, _ = git(r, "stash", "list")
    rem, _, _ = git(r, "remote", "-v")
    return {"ramo": cur, "modifiche": [x for x in st.splitlines() if x.strip()],
            "rami": [x for x in br.splitlines() if x.strip()], "stash": [x for x in sl.splitlines() if x.strip()],
            "remote": sorted({x.split()[1] for x in rem.splitlines() if x.split()[1:]})}


def file_grandi(cartella, n=8):
    v = []
    for r, ds, fs in os.walk(cartella):
        ds[:] = [d for d in ds if d not in SALTA_DIR and d != ".git"]
        for f in fs:
            p = Path(r) / f
            try:
                v.append((p.stat().st_size, p))
            except OSError:
                pass
    return sorted(v, reverse=True)[:n]


def albero(cartella, prof=2):
    """Cartelle fino a 'prof' livelli con numero di file e peso."""
    righe = []
    base = Path(cartella)
    for r, ds, fs in os.walk(base):
        ds[:] = sorted(d for d in ds if d not in SALTA_DIR and d != ".git")
        liv = len(Path(r).relative_to(base).parts)
        if liv >= prof:
            ds[:] = []
        if liv == 0:
            continue
        righe.append(f"{'  ' * (liv - 1)}- `{Path(r).name}/` ({umano(peso(r))})")
    return righe


def riassunto_uso():
    f = UFF / "logs" / "uso.csv"
    if not f.exists():
        return ["(logs/uso.csv non trovato)"]
    try:
        rr = list(csv.DictReader(open(f, encoding="utf-8", errors="replace")))
    except Exception as e:
        return [f"(uso.csv non leggibile: {e})"]
    d = defaultdict(lambda: [0, 0, 0, 0.0])
    for x in rr:
        if not x.get("modello"):
            continue
        k = (x.get("motore") or "?", x["modello"])
        d[k][0] += 1
        d[k][1] += 0 if x.get("esito") == "ok" else 1
        try:
            d[k][2] += int(float(x.get("token_input") or 0)) + int(float(x.get("token_output") or 0))
            d[k][3] += float(x.get("costo_listino_usd") or 0)
        except ValueError:
            pass
    out = [f"Righe totali: {len(rr)} (dal {rr[0]['quando'] if rr else '?'} al {rr[-1]['quando'] if rr else '?'})", "",
           "| motore | modello | chiamate | non ok | token | costo listino $ |", "|---|---|---|---|---|---|"]
    for (m, mod), (n, e, t, c) in sorted(d.items(), key=lambda a: -a[1][0]):
        out.append(f"| {m} | {mod} | {n} | {e} | {t:,} | {c:.2f} |")
    out.append("")
    out.append("Nota: per Gemini/Cerebras/Groq il costo e' scritto 0 dal codice anche se il fornitore fattura.")
    return out


def task_ufficio():
    out = []
    g = UFF / "generico"
    if not g.exists():
        return ["(cartella generico non trovata)"]
    for sub in sorted(p for p in g.iterdir() if p.is_dir()):
        voci = sorted(x.name for x in sub.iterdir())
        out.append(f"- `generico/{sub.name}/`: {len(voci)} elementi" + (f" - es. {', '.join(voci[:6])}" if voci else ""))
    return out


# ----------------------------------------------------------------------------------------------------------------
def main():
    global tutto_ok
    t0 = time.time()
    say("=" * 70)
    say(" BACKUP COMPLETO DELL'UFFICIO - non modifica e non cancella niente")
    say("=" * 70)
    say(f" Ufficio:      {UFF}")
    say(f" Destinazione: {DEST}")
    say(" Consiglio: chiudi l'Ufficio (Menu > Esci) prima, cosi' la copia e' coerente.")
    say("")
    if not (UFF / "motori.py").exists():
        say("ERRORE: non trovo motori.py nella cartella dell'Ufficio. Lo script deve stare in Multiple Agents\\pulizia.")
        return 1

    pj = progetti()
    repo_list = []          # (id, nome, cartella)
    visti = set()
    for p in pj:
        c = p.get("cartella")
        if not c:
            continue
        if dentro(c, UFF):
            p["nota"] = "dentro la cartella dell'Ufficio: e' gia' in ufficio.zip"
            continue
        if not Path(c).exists():
            p["nota"] = "CARTELLA NON TROVATA: non salvata"
            continue
        key = str(Path(c).resolve()).lower()
        if key in visti:
            p["nota"] = "stessa cartella di un altro progetto"
            continue
        visti.add(key)
        repo_list.append((p["id"], p["nome"], Path(c)))

    say("Calcolo spazio necessario...")
    pesi = {"ufficio": peso(UFF)}
    for pid, _, c in repo_list:
        pesi[pid] = peso(c)
    serve = sum(pesi.values())
    RADICE.mkdir(parents=True, exist_ok=True)
    libero = shutil.disk_usage(RADICE).free
    say(f"  da copiare: {umano(serve)} (prima della compressione) - libero su disco: {umano(libero)}")
    if libero < serve * 1.3 + 500 * 1024 ** 2:
        say("ERRORE: spazio libero insufficiente. Libera spazio o cambia destinazione (BK_DEST). Nessun file creato.")
        return 1
    DEST.mkdir(parents=True)
    (DEST / "progetti").mkdir()

    # 1) Ufficio
    say(f"\n[1/5] Ufficio -> ufficio.zip ({umano(pesi['ufficio'])})...")
    n = zippa(UFF, DEST / "ufficio.zip")
    say(f"      {n} file")

    # 2) progetti
    info = {}
    say(f"\n[2/5] Progetti ({len(repo_list)})...")
    for pid, nome, c in repo_list:
        say(f"  - {nome}: {c} ({umano(pesi[pid])})")
        n = zippa(c, DEST / "progetti" / f"{pid}.zip")
        say(f"      zip: {n} file")
        ir = info_repo(c)
        info[pid] = ir
        if ir:
            b = DEST / "progetti" / f"{pid}.bundle"
            _, err, rc = git(c, "bundle", "create", str(b), "--all")
            if rc:
                say(f"      ATTENZIONE bundle non creato: {err[:200]}")
                controlli.append(f"BUNDLE {pid}: NON CREATO ({err[:200]})")
                tutto_ok = False
            else:
                say(f"      bundle: {len(ir['rami'])} rami, {len(ir['stash'])} stash")
        else:
            say("      (non e' un repo git: solo zip)")

    # 3) chiavi
    say("\n[3/5] Chiavi API -> chiavi_PRIVATE\\ ...")
    if CHIAVI.exists():
        shutil.copytree(CHIAVI, DEST / "chiavi_PRIVATE" / CHIAVI.name)
        (DEST / "chiavi_PRIVATE" / "LEGGIMI.txt").write_text(
            "Qui ci sono le chiavi API dell'Ufficio (copia di %s).\n"
            "NON caricarle su GitHub, non mandarle a nessun modello, non condividerle.\n"
            "Per ripristinarle: copia la cartella .ufficio in %s\n" % (CHIAVI, CHIAVI.parent), encoding="utf-8")
        say(f"      copiate da {CHIAVI}")
    else:
        say(f"      cartella chiavi non trovata ({CHIAVI}): saltato")
        controlli.append(f"CHIAVI: cartella {CHIAVI} non trovata")

    # 4) controlli
    say("\n[4/5] Controllo che tutto sia leggibile...")
    for z in [DEST / "ufficio.zip", *sorted((DEST / "progetti").glob("*.zip"))]:
        try:
            with zipfile.ZipFile(z) as zz:
                bad = zz.testzip()
            ok = bad is None
        except Exception as e:
            ok, bad = False, str(e)
        controlli.append(f"ZIP {z.name}: {'OK' if ok else 'ROTTO -> ' + str(bad)}  ({umano(z.stat().st_size)})")
        tutto_ok &= ok
        say(f"      {z.name}: {'OK' if ok else 'ROTTO'}")
    for pid, _, c in repo_list:
        b = DEST / "progetti" / f"{pid}.bundle"
        if b.exists():
            _, err, rc = git(c, "bundle", "verify", str(b))
            controlli.append(f"BUNDLE {b.name}: {'OK' if rc == 0 else 'ERRORE ' + err[:200]}  ({umano(b.stat().st_size)})")
            tutto_ok &= rc == 0
            say(f"      {b.name}: {'OK' if rc == 0 else 'ERRORE'}")
    controlli.append("")
    controlli.append("Impronte sha256 (per controllare piu' avanti che i file non si siano rovinati, es. dopo la copia sul Pi):")
    for f in sorted(DEST.rglob("*")):
        if f.is_file() and f.suffix in (".zip", ".bundle"):
            controlli.append(f"  {sha256(f)}  {f.relative_to(DEST)}")
    if saltati:
        tutto_ok = False
        controlli.append("")
        controlli.append(f"FILE NON COPIATI ({len(saltati)}) - di solito perche' aperti da un altro programma:")
        controlli.extend("  " + s for s in saltati)

    # 5) inventario
    say("\n[5/5] Scrivo INVENTARIO.md e COME_RIPRISTINARE.md...")
    scrivi_inventario(pj, repo_list, info, pesi)
    scrivi_ripristino(repo_list)
    esito = "TUTTO OK" if tutto_ok else "CON PROBLEMI (vedi CONTROLLO.txt)"
    (DEST / "CONTROLLO.txt").write_text(f"Backup del {datetime.now():%Y-%m-%d %H:%M} - esito: {esito}\n\n" + "\n".join(controlli) + "\n",
                                        encoding="utf-8")
    tot = sum(f.stat().st_size for f in DEST.rglob("*") if f.is_file())
    say("")
    say("=" * 70)
    say(f" FINITO in {time.time() - t0:.0f} s - esito: {esito}")
    say(f" Cartella: {DEST}  ({umano(tot)})")
    say(" Puoi spostarla dove vuoi (es. sul Pi): e' completa da sola.")
    say("=" * 70)
    try:
        os.startfile(str(DEST))          # apre la cartella in Esplora risorse (solo Windows)
    except Exception:
        pass
    return 0 if tutto_ok else 2


def scrivi_inventario(pj, repo_list, info, pesi):
    L = [f"# Inventario backup Ufficio - {datetime.now():%d/%m/%Y %H:%M}", "",
         "Generato automaticamente da `pulizia/backup_completo.py`. Descrive COSA c'e'; la spiegazione di COME funziona "
         "va scritta a parte (passo successivo).", "",
         "## Contenuto del backup", "",
         f"- `ufficio.zip` - cartella `{UFF}` ({umano(pesi['ufficio'])} prima della compressione)"]
    for pid, nome, c in repo_list:
        L.append(f"- `progetti/{pid}.zip` + `progetti/{pid}.bundle` - {nome}: `{c}` ({umano(pesi[pid])})")
    L += ["- `chiavi_PRIVATE/` - chiavi API (mai su GitHub)", "- `CONTROLLO.txt` - esito controlli e impronte", ""]

    L += ["## Progetti registrati nell'Ufficio (progetti/*.json)", "", "| id | nome | cartella | motore | stato | nota |",
          "|---|---|---|---|---|---|"]
    for p in pj:
        L.append(f"| {p.get('id')} | {p.get('nome', '')} | `{p.get('cartella', '')}` | {p.get('motore', '')} | "
                 f"{p.get('stato', '')} | {p.get('nota', p.get('errore', ''))} |")
    L.append("")

    L += ["## Cartella dell'Ufficio", "", "### Cartelle", ""] + albero(UFF, 2) + [""]
    L += ["### File principali (primo livello e pannello)", "", "| file | peso | modificato | descrizione (dal file) |", "|---|---|---|---|"]
    for base in (UFF, UFF / "pannello", UFF / "pulizia"):
        if not base.exists():
            continue
        for f in sorted(x for x in base.iterdir() if x.is_file() and x.suffix in (".py", ".bat", ".vbs", ".ps1", ".md", ".txt", ".html", ".json", ".jsonl", ".log", ".csv")):
            st = f.stat()
            L.append(f"| `{f.relative_to(UFF)}` | {umano(st.st_size)} | {datetime.fromtimestamp(st.st_mtime):%d/%m %H:%M} | "
                     f"{prima_riga_doc(f).replace('|', '/')} |")
    L.append("")
    L += ["### Task dell'Ufficio (cartella generico)", ""] + task_ufficio() + [""]
    L += ["### Backup vecchi dentro l'Ufficio", ""]
    for b in sorted(UFF.glob("_backup*")):
        L.append(f"- `{b.name}/` ({umano(peso(b))})")
    L.append("")
    L += ["### Modelli conosciuti (logs)", ""]
    for f in sorted((UFF / "logs").glob("modelli*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            if "modelli" in d:
                L.append(f"- `{f.name}`: {len(d['modelli'])} modelli - {', '.join(d['modelli'][:8])}")
            else:
                for k, v in d.items():
                    if isinstance(v, dict):
                        L.append(f"- `{f.name}` / {k}: {len(v.get('modelli', []))} modelli, scartati: {len(v.get('scartati', {}))}")
        except Exception as e:
            L.append(f"- `{f.name}`: non leggibile ({e})")
    L.append("")
    L += ["### Consumi registrati (logs/uso.csv)", ""] + riassunto_uso() + [""]

    L += ["## Repo dei progetti", ""]
    for pid, nome, c in repo_list:
        ir = info.get(pid)
        L += [f"### {nome} (`{c}`)", ""]
        if not ir:
            L += ["Non e' un repo git.", ""]
        else:
            L += [f"- ramo attivo: `{ir['ramo']}`", f"- modifiche non salvate: {len(ir['modifiche'])}",
                  f"- remote: {', '.join(ir['remote']) or 'nessuno (non e su GitHub)'}",
                  f"- stash: {len(ir['stash'])}"] + [f"  - {s}" for s in ir["stash"]]
            L += [f"- rami: {len(ir['rami'])} (piu' recenti prima)", ""]
            L += ["| ramo | data | ultimo messaggio |", "|---|---|---|"]
            for r in ir["rami"]:
                a = (r.split(" | ", 2) + ["", ""])[:3]
                L.append(f"| `{a[0]}` | {a[1]} | {a[2][:100].replace('|', '/')} |")
            if ir["modifiche"]:
                L += ["", "Modifiche non salvate (prime 30):", ""] + [f"    {m}" for m in ir["modifiche"][:30]]
            L.append("")
        L += ["Cartelle:", ""] + albero(c, 2) + ["", "File piu' grandi (escluso .git):", ""]
        L += [f"- `{p.relative_to(c)}` ({umano(s)})" for s, p in file_grandi(c)] + [""]
    (DEST / "INVENTARIO.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def scrivi_ripristino(repo_list):
    righe = "\n".join(f"- {nome}: `{c}` <- `progetti/{pid}.zip`" for pid, nome, c in repo_list)
    t = f"""# Come ripristinare questo backup

Backup del {datetime.now():%d/%m/%Y %H:%M}. Ogni zip contiene la cartella intera (per i progetti anche `.git`,
cioe' tutta la storia, i rami, lo stash e i file non tracciati come i dati).

## Ripristinare tutto com'era
1. Chiudi l'Ufficio.
2. Rinomina le cartelle attuali (es. `Multiple Agents` -> `Multiple Agents_vecchia`), non cancellarle subito.
3. Estrai `ufficio.zip` dentro `{UFF.parent}` (si ricrea `{UFF.name}`).
4. Estrai ogni zip dei progetti nella cartella che lo contiene:
{righe}
5. Copia `chiavi_PRIVATE/{CHIAVI.name}` in `{CHIAVI.parent}`.
6. Apri l'Ufficio e controlla. Se va tutto bene, puoi cancellare le cartelle `_vecchia`.

## Recuperare solo un ramo cancellato (es. dopo la pulizia dei rami)
Il file `.bundle` e' la storia git completa. Da una finestra nella cartella del progetto:

    git fetch "<percorso>\\progetti\\<id>.bundle" "NOME-RAMO:NOME-RAMO"

Per vedere quali rami contiene: `git bundle list-heads "<percorso>\\progetti\\<id>.bundle"`.

## Controllare che il backup non si sia rovinato (es. dopo averlo spostato sul Pi)
In `CONTROLLO.txt` ci sono le impronte sha256 di ogni file. Su Windows: `certutil -hashfile ufficio.zip SHA256`;
sul Pi: `sha256sum ufficio.zip`. Devono essere uguali.
"""
    (DEST / "COME_RIPRISTINARE.md").write_text(t, encoding="utf-8")


if __name__ == "__main__":
    try:
        rc = main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        say(f"\nERRORE inatteso: {e}. Nessun file originale e' stato toccato.")
        rc = 1
    sys.exit(rc)
