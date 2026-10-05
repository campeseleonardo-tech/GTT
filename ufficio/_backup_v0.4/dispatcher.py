r"""
dispatcher.py - fa lavorare gli agenti di TUTTI i progetti, uno alla volta, anche a pannello chiuso.
Lo avvia l'attivita' di Windows "UfficioAgenti" ogni 5 minuti (invisibile) e il pannello quando cambia qualcosa.

Ordine: priorita' del progetto (progetti\*.json: alta / media / bassa) con rotazione 3-2-1:
l'alta riceve 3 turni, la media 2, la bassa 1, alternati; un task messo "in cima" dal pannello parte per primo.
Prima di ogni lavoro controlla (comune.py): limite di Claude, contatore d'uso al 100%, altri agenti al lavoro.
Dopo ogni lavoro scrive una riga nel diario (diario.jsonl, 0 token) leggendo cio' che il runner ha lasciato.
Si ferma quando non c'e' piu' niente di pronto. Due dispatcher non partono mai insieme (dispatcher.lock).
"""
import csv
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import comune  # noqa: E402
import scheda  # noqa: E402  scheda progetto (documento centrale): consigli, revisione, stato automatico

PROG = ROOT / "progetti"
GEN = ROOT / "generico"
CV = ROOT / "candidature"
ROT = ROOT / "rotazione.json"
DIARIO = ROOT / "diario.jsonl"
LOCK = ROOT / "dispatcher.lock"
LOGF = ROOT / "dispatcher.log"
PESI = {"alta": 3, "media": 2, "bassa": 1}
NOWIN = 0x08000000 if os.name == "nt" else 0


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    try:
        with open(LOGF, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    if sys.stdout and sys.stdout.isatty():
        print(line)


def jload(p, default):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def jsave(p, data):
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def progetti():
    out = {}
    for f in sorted(PROG.glob("*.json")) if PROG.exists() else []:
        p = jload(f, None)
        if p and p.get("id"):
            out[p["id"]] = p
    return out


def diario_add(e):
    e.setdefault("quando", datetime.now().strftime("%Y-%m-%d %H:%M"))
    with open(DIARIO, "a", encoding="utf-8") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")


# ------------------------------------------------------------ chi e' pronto
def _gen_mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_runner", GEN / "runner.py")
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(GEN))
    spec.loader.exec_module(m)
    return m


def _cv_mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location("cv_state_disp", CV / "runner" / "state.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def candidati():
    """Lavori pronti adesso: [{progetto, tipo: cv|gen, id, titolo}] (in ordine dentro ogni progetto)."""
    out = []
    if (CV / "runner" / "state.py").exists() and not (CV / "stato" / "STOP").exists():
        try:
            S = _cv_mod()
            s = S.load()
            j = S.next_job(s)
            if j:
                o = S.find_offer(s, j.get("offerta")) if j.get("offerta") else None
                tit = {"scout": "Scout: cerca offerte", "cv": "Analisi + CV", "letter": "Lettera",
                       "manutenzione": "Manutenzione mappa", "nuove_aziende": "Nuove aziende"}.get(j["tipo"], j["tipo"])
                out.append({"progetto": "candidature", "tipo": "cv", "id": j["id"],
                            "titolo": tit + (" · " + S.label(o) if o else "")})
        except Exception as e:
            log(f"candidature non leggibili: {e}")
    if (GEN / "runner.py").exists() and not (GEN / "STOP").exists():
        try:
            R = _gen_mod()
            ts = []
            for p in sorted((GEN / "queue").glob("*.task.md")):
                try:
                    ts.append(R.parse_task(p))
                except Exception:
                    continue
            ts.sort(key=lambda t: (R.to_int(t.get("priority"), 2), t["_path"].name))
            for t in ts:
                ok, _why = R.ready(t)
                if ok:
                    out.append({"progetto": (t.get("project") or "altro").lower(), "tipo": "gen", "id": t["id"],
                                "titolo": t.get("title") or t["id"]})
        except Exception as e:
            log(f"task generici non leggibili: {e}")
    return out


def scegli(cands, rot, prj, simula=False):
    """Rotazione pesata 3-2-1 (alternata). 'in cima' vince. Torna il candidato scelto (e aggiorna rot)."""
    if not cands:
        return None
    for tid in list(rot.get("in_cima", [])):
        for c in cands:
            if c["id"] == tid:
                if not simula:
                    rot["in_cima"].remove(tid)
                return c
    first = {}
    for c in cands:
        first.setdefault(c["progetto"], c)
    peso = {p: PESI.get((prj.get(p) or {}).get("priorita", "media"), 2) for p in first}
    cw = rot.setdefault("cw", {})
    tot = sum(peso.values())
    for p in first:
        cw[p] = cw.get(p, 0) + peso[p]
    best = max(first, key=lambda p: (cw[p], peso[p], p))
    cw[best] -= tot
    return first[best]


def ordine_simulato(cands, rot, prj, n=12):
    """Per il pannello: in che ordine partirebbero i lavori pronti (senza toccare lo stato vero)."""
    import copy
    r = copy.deepcopy(rot)
    rest = list(cands)
    out = []
    while rest and len(out) < n:
        c = scegli(rest, r, prj, simula=False)
        out.append(c)
        rest.remove(c)
    return out


# ------------------------------------------------------------ esecuzione
def _python():
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe" and (exe.parent / "python.exe").exists():
        return str(exe.parent / "python.exe")
    return str(exe)


def esegui(c):
    if c["tipo"] == "cv":
        cmd, cwd = [_python(), str(CV / "runner" / "runner.py"), "job", c["id"]], CV / "runner"
    else:
        cmd, cwd = [_python(), str(GEN / "runner.py"), "--task", c["id"]], GEN
    t0 = time.time()
    with open(ROOT / "dispatcher_ultimo_output.txt", "w", encoding="utf-8") as out:
        p = subprocess.Popen(cmd, cwd=str(cwd), stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT,
                             creationflags=NOWIN)
        last = 0.0
        while p.poll() is None:
            if time.time() - last > 30:
                last = time.time()
                try:
                    os.utime(LOCK, None)
                except OSError:
                    pass
            time.sleep(2)
    return time.time() - t0


def _first_line_esito(txt):
    for line in (txt or "").splitlines():
        line = line.strip().strip("*").strip()
        if line.upper().startswith("ESITO:"):
            return line[6:].strip()
    for line in (txt or "").splitlines():
        line = line.strip()
        if line:
            return re.split(r"(?<=[.!?])\s", line)[0][:220]
    return ""


def diario_gen(tid, prj_id, titolo, secs, inizio_ts):
    """Riga di diario per un task generico, dai file lasciati dal runner."""
    row = {}
    try:
        with open(GEN / "logs" / "usage.csv", encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("task_id") == tid:
                    row = r
    except OSError:
        pass
    stato = row.get("status") or "?"
    cost = float(row.get("cost_usd") or 0)
    res = GEN / "results" / tid
    summary = ""
    if (res / "summary.txt").exists() and (res / "summary.txt").stat().st_mtime >= inizio_ts - 5:
        summary = (res / "summary.txt").read_text(encoding="utf-8", errors="replace")
    val = ""
    if (res / "VALIDATORE.log").exists() and (res / "VALIDATORE.log").stat().st_mtime >= inizio_ts - 5:
        v = (res / "VALIDATORE.log").read_text(encoding="utf-8", errors="replace")
        ok = v.count("- OK")
        bad = v.count("- ERRORE")
        giri = v.count("## Giro")
        val = f"validatore: {ok} controlli OK" + (f", {bad} errori" if bad else "") + (f", {giri - 1} correzioni dell'agente" if giri > 1 else "")
    frase = _first_line_esito(summary)
    if not frase:
        frase = {"done": "completato", "failed": "non ha passato i controlli", "blocked": "si e' fermato: ha delle domande per te",
                 "incomplete": "interrotto (turni o tempo finiti)", "limit": "fermato dal limite di Claude"}.get(stato, stato)
    rapporto = ""
    try:
        R = _gen_mod()
        for d in ("done", "failed", "blocked", "incomplete", "queue"):
            f = GEN / d / f"{tid}.task.md"
            if f.exists():
                t = R.parse_task(f)
                if t.get("repo"):
                    rp = Path(t["repo"]) / "agenti" / tid / "RAPPORTO.md"
                    rapporto = str(rp) if rp.exists() else ""
                break
    except Exception:
        pass
    repo = ""
    try:
        R2 = _gen_mod()
        for d in ("done", "failed", "blocked", "incomplete", "queue"):
            f2 = GEN / d / f"{tid}.task.md"
            if f2.exists():
                repo = R2.parse_task(f2).get("repo") or ""
                break
    except Exception:
        pass
    if not rapporto:
        for n_ in ("REVISIONE.md", "CONSIGLI.md"):
            f_ = scheda._output({"id": tid, "repo": repo}, n_)
            if f_:
                rapporto = str(f_)
                break
    nd = domande_raccogli(tid, prj_id, inizio_ts, repo)
    try:
        nota = scheda.dopo_task(tid)
    except Exception as e:
        nota = ""
        log(f"scheda non aggiornata: {e}")
    if nota:
        frase = nota
    diario_add({"progetto": prj_id, "task": tid, "titolo": titolo, "esito": stato, "frase": frase + (f" · {nd} domande per te" if nd else ""),
                "pct": round(100 * comune.token_pesati(cost) / comune.token_100()), "secondi": round(secs),
                "dettagli": "; ".join(x for x in (val, f"turni {row.get('num_turns')}" if row.get("num_turns") else "") if x),
                "rapporto": rapporto, "riassunto": summary.strip()[:1500]})
    try:
        scheda.aggiorna(prj_id)          # di nuovo, cosi' la scheda include anche questa riga del diario
    except Exception:
        pass


def diario_cv(jid, titolo, secs):
    try:
        S = _cv_mod()
        s = S.load()
        j = next((x for x in s["coda"] if x["id"] == jid), None)
    except Exception:
        j = None
    cost = 0.0
    try:
        with open(CV / "stato" / "uso.csv", encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                if j and (r.get("started") or "") >= (j.get("inizio") or "9").replace("T", " ")[:19]:
                    cost += float(r.get("cost_usd_listprice") or 0)
    except OSError:
        pass
    stato = (j or {}).get("stato", "?")
    diario_add({"progetto": "candidature", "task": jid, "titolo": titolo,
                "esito": {"fatto": "done", "errore": "failed", "in_attesa": "limit"}.get(stato, stato),
                "frase": (j or {}).get("esito") or stato, "pct": round(100 * comune.token_pesati(cost) / comune.token_100()),
                "secondi": round(secs), "dettagli": "", "rapporto": str(CV / "stato" / "coda.md"), "riassunto": ""})


DOMANDE = ROOT / "domande.jsonl"
_RIGA_D = re.compile(r"^\s*[-*]\s*(?P<q>[^|]+?)\s*\|\s*opzioni\s*:\s*(?P<o>[^|]*)\|\s*scelta\s*:\s*(?P<s>[^|]*?)\s*(?:\|\s*dove\s*:\s*(?P<d>.*))?$", re.I)


def domande_raccogli(tid, prj_id, inizio_ts, repo):
    """Domande NON bloccanti dell'agente (DOMANDE.md) -> domande.jsonl, che il pannello mostra in 'Domande'."""
    cand = [GEN / "results" / tid / "DOMANDE.md"]
    if repo:
        cand.insert(0, Path(repo) / "agenti" / tid / "DOMANDE.md")
    f = next((c for c in cand if c.exists() and c.stat().st_mtime >= inizio_ts - 5), None)
    if not f:
        return 0
    n = 0
    with open(DOMANDE, "a", encoding="utf-8") as out:
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines()):
            m = _RIGA_D.match(line)
            if not m:
                continue
            opz = [x.strip() for x in m.group("o").split("/") if x.strip()][:5]
            out.write(json.dumps({"id": f"{tid}#{i}", "progetto": prj_id, "task": tid, "domanda": m.group("q").strip()[:200],
                                  "opzioni": opz, "scelta": m.group("s").strip()[:120], "dove": (m.group("d") or "").strip()[:200],
                                  "quando": datetime.now().strftime("%Y-%m-%d %H:%M"), "stato": "aperta"}, ensure_ascii=False) + "\n")
            n += 1
            if n >= 8:
                break
    return n


def lock_preso():
    try:
        if time.time() - LOCK.stat().st_mtime < 300:
            return True
    except OSError:
        pass
    LOCK.write_text(f"{os.getpid()} {datetime.now():%Y-%m-%d %H:%M:%S}", encoding="utf-8")
    return False


def main():
    if sys.stdout is None:            # avviato con pythonw (nessuna finestra): niente stampe
        sys.stdout = sys.stderr = open(os.devnull, "w")
    if os.environ.get("ANTHROPIC_API_KEY"):
        log("ANTHROPIC_API_KEY impostata: non parto (userebbe l'API a pagamento).")
        return
    if lock_preso():
        return
    try:
        for x in comune.pulizia_avvio():
            log("Pulizia: " + x)
        limite_visto = comune.limite_fino()
        n = 0
        while n < 50:
            why = comune.perche_non_parte("dispatcher")
            if why:
                if n:
                    log("Mi fermo: " + why)
                f = comune.limite_fino()
                if f and f != limite_visto:
                    diario_add({"progetto": "", "task": "", "titolo": "Limite di Claude", "esito": "limit",
                                "frase": f"Limite di Claude raggiunto: tutto in pausa fino alle {comune.quando(f)}, poi riparte da solo",
                                "pct": None, "secondi": None, "dettagli": "", "rapporto": "", "riassunto": ""})
                break
            prj = progetti()
            rot = jload(ROT, {})
            c = scegli(candidati(), rot, prj)
            if not c:
                break
            jsave(ROT, rot)
            log(f"Parte: {c['progetto']} · {c['id']} · {c['titolo']}")
            jsave(ROOT / "agente_attuale.json", {**c, "inizio": datetime.now().isoformat(timespec="seconds")})
            t0 = time.time()
            try:
                secs = esegui(c)
            finally:
                (ROOT / "agente_attuale.json").unlink(missing_ok=True)
            try:
                if c["tipo"] == "gen":
                    diario_gen(c["id"], c["progetto"], c["titolo"], secs, t0)
                else:
                    diario_cv(c["id"], c["titolo"], secs)
            except Exception as e:
                log(f"diario non scritto: {e}")
            log(f"Finito: {c['id']} in {secs:.0f} s")
            n += 1
            limite_visto = None
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
