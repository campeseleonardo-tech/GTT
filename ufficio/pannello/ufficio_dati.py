r"""
ufficio_dati.py - dati e azioni della pagina nuova "Ufficio" (ufficio.html), 04/10/2026.
Legge: progetti\*.json, la coda dei task generici, lo stato delle candidature, diario.jsonl, comune.py.
Il pannello vecchio (pannello.html) continua a funzionare con le sue API: questo file aggiunge solo cose nuove.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import comune  # noqa: E402
import motori  # noqa: E402  log unico del consumo logs\uso.csv (v0.5)
import scheda  # noqa: E402

PROG = ROOT / "progetti"
GEN = ROOT / "generico"
CV = ROOT / "candidature"
DIARIO = ROOT / "diario.jsonl"
ROT = ROOT / "rotazione.json"
CARTELLE_GEN = {"queue": "in_coda", "done": "fatto", "failed": "fallito", "incomplete": "incompleto",
                "blocked": "bloccato", "sospesi": "sospeso", "scartate": "scartata"}
GRANDEZZA = {"piccolo": "small", "medio": "medium", "grande": "large"}
DOMANDE = ROOT / "domande.jsonl"
USO_DEFAULT = {"small": 5, "medium": 12, "large": 30}
H = {}          # funzioni del server (cv_mod, cv_collect, file_info, gen_task_detail, sources, log): le passa init()


def init(**kw):
    H.update(kw)


def _disp():
    import importlib.util
    spec = importlib.util.spec_from_file_location("ufficio_dispatcher", ROOT / "dispatcher.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def jload(p, default):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except Exception:
        return default


def jsave(p, data):
    p = Path(p)
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def slug(s, n=30):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower().replace("à", "a").replace("è", "e").replace("é", "e")
               .replace("ì", "i").replace("ò", "o").replace("ù", "u")).strip("-")
    return s[:n].strip("-") or "x"


def pct_of(cost):
    try:
        return round(100 * comune.token_pesati(float(cost or 0)) / comune.token_100())
    except Exception:
        return None


# ------------------------------------------------------------------ progetti
def progetti():
    out = []
    for f in sorted(PROG.glob("*.json")) if PROG.exists() else []:
        p = jload(f, None)
        if p and p.get("id"):
            out.append(p)
    order = {"alta": 0, "media": 1, "bassa": 2}
    out.sort(key=lambda p: (p.get("stato") == "archiviato", order.get(p.get("priorita"), 1), p.get("nome", "")))
    return out


def progetto(pid):
    return jload(PROG / f"{pid}.json", None)


# ------------------------------------------------------------------ task generici
def parse_task(path):
    text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    head, _, body = text.partition("\n---")
    meta = {}
    for raw in head.splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#") and ":" in raw:
            k, v = raw.split(":", 1)
            k, v = k.strip().lower(), v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            meta[k] = v
    meta["body"] = body.lstrip("-").strip()
    meta["_path"] = Path(path)
    meta.setdefault("id", Path(path).name.replace(".task.md", ""))
    return meta


def _usage_gen():
    """Per ogni task generico: costo totale, token, turni, esito (dal log unico logs\\uso.csv, motori.py)."""
    try:
        return motori.per_task("generico")
    except Exception:
        return {}


def _listify(v):
    if not v:
        return []
    return v if isinstance(v, list) else [v]


def gen_tasks():
    """Tutti i task generici: [{id, progetto, titolo, stato, nota, pct, quando, approvare, ...}]"""
    use = _usage_gen()
    done_ids = {p.name.replace(".task.md", "") for p in (GEN / "done").glob("*.task.md")} if (GEN / "done").exists() else set()
    att = jload(ROOT / "agente_attuale.json", {})
    out, seen = [], set()
    piu_recente = {}                     # se lo stesso task e' in due cartelle (es. failed vecchio + done nuovo) vale la copia piu' recente
    for cart in ("queue", "blocked", "incomplete", "failed", "done", "sospesi", "scartate"):
        for f in (GEN / cart).glob("*.task.md") if (GEN / cart).exists() else []:
            k = f.name
            if k not in piu_recente or (cart == "queue") or (f.stat().st_mtime > piu_recente[k][0] and piu_recente[k][1] != "queue"):
                piu_recente[k] = (f.stat().st_mtime, cart)
    for cart in ("queue", "blocked", "incomplete", "failed", "done", "sospesi", "scartate"):
        d = GEN / cart
        for p in sorted(d.glob("*.task.md")) if d.exists() else []:
            if piu_recente.get(p.name, (0, cart))[1] != cart:
                continue
            try:
                t = parse_task(p)
            except Exception:
                continue
            tid = t["id"]
            if tid in seen:
                continue
            seen.add(tid)
            u = use.get(tid, {})
            stato = CARTELLE_GEN[cart]
            nota, approvare = "", None
            if cart == "queue":
                if t.get("approval_before", "").lower() == "leo" and t.get("approved", "no").lower() != "yes":
                    nota, approvare = "aspetta il tuo OK prima di partire", "prima"
                else:
                    for dep in _listify(t.get("depends_on")):
                        if not any(i.startswith(dep) for i in done_ids):
                            nota = f"aspetta che finisca {dep}"
                            break
                    else:
                        nota = "pronto"
                if att.get("id") == tid:
                    stato, nota = "in_corso", "un agente ci sta lavorando adesso"
            elif cart == "done" and t.get("approval_after", "").lower() == "leo" and t.get("approved", "no").lower() != "yes":
                nota, approvare = "fatto: aspetta il tuo controllo", "dopo"
            elif cart == "blocked":
                nota = "ha delle domande per te"
            elif cart == "failed":
                nota = "non ha passato i controlli"
            elif cart == "sospesi":
                nota = "spento: parte solo se lo attivi"
            out.append({"id": tid, "progetto": (t.get("project") or "altro").lower(), "titolo": t.get("title") or tid,
                        "stato": stato, "nota": nota, "approvare": approvare, "tier": t.get("tier", "small"),
                        "pct": pct_of(u.get("costo_tot")) if u else None, "quando": (u.get("timestamp") or "")[:16].replace("T", " "),
                        "mtime": p.stat().st_mtime, "repo": t.get("repo", ""), "cartella": cart,
                        "proposta": bool(t.get("proposta")), "tipo": t.get("tipo", "")})
    return out


# ------------------------------------------------------------------ candidature
def cv_dati():
    """Offerte, domande, direzioni e conteggi delle candidature."""
    src = next((s for s in H["sources"]() if s.get("tipo") == "cv_runner"), None)
    if not src:
        return None
    S = H["cv_mod"](src)
    s = S.load()
    r = H["cv_collect"](src)
    offerte = []
    for o in s["offerte"]:
        stato, nota, fase = S.offer_view(s, o)
        if o["stato"] == "scartata":
            stato = "scartata"
        offerte.append({"id": o["id"], "titolo": S.label(o), "stato": stato, "stato_raw": o["stato"], "nota": nota,
                        "url": o.get("url") or "", "azienda": o.get("azienda") or "", "ruolo": o.get("ruolo") or "",
                        "sede": o.get("sede") or "", "perche": o.get("perche") or "", "gap": o.get("gap") or "",
                        "pubblicata": o.get("pubblicata") or "", "creata": o.get("creata") or "", "cartella": str(S.OUT / o["tag"]) if o.get("tag") else ""})
    n = lambda st: sum(1 for o in s["offerte"] if o["stato"] == st)
    cont = {"Mappa": len(s["mappa"]), "Trovate": len(s["offerte"]), "Scartate": n("scartata"),
            "Da approvare": sum(1 for o in offerte if o["stato"] == "da_approvare"),
            "Lettere": n("pronta")}
    lavori = [{"id": j["id"], "tipo": j["tipo"], "stato": j["stato"], "esito": j.get("esito") or "",
               "quando": (j.get("fine") or j.get("inizio") or j.get("creato") or "")[:16].replace("T", " ")} for j in s["coda"][-12:]]
    return {"sorgente": src["id"], "offerte": offerte, "domande": r["domande"], "hint": s["hint"], "conteggi": cont,
            "imp": {k: s["impostazioni"].get(k) for k in ("effort", "letter_effort", "scout_effort", "scout_picks", "scout_companies")},
            "pausa": S.STOP_FILE.exists(), "lavori": lavori, "registro_n": sum(1 for x in s["registro"] if x["stato"] == "attivo")}


# ------------------------------------------------------------------ diario
def diario(n=60):
    if not (ROOT / ".diario_ricostruito").exists():
        _backfill()
    rows = []
    try:
        for line in DIARIO.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    except OSError:
        pass
    return list(reversed(rows[-n:]))


def _backfill():
    """Prima apertura: ricostruisce il diario dai log gia' esistenti (generico + candidature), 0 token."""
    rows = []
    try:
        for r in _usage_gen().values():
            tid = r.get("task_id")
            summ = GEN / "results" / tid / "summary.txt"
            txt = summ.read_text(encoding="utf-8", errors="replace") if summ.exists() else ""
            first = next((l.strip() for l in txt.splitlines() if l.strip()), "")
            if first.upper().startswith("ESITO:"):
                first = first[6:].strip()
            first = re.split(r"(?<=[.!?])\s", first)[0][:220] if first else ""
            st = r.get("status") or ""
            rows.append({"quando": (r.get("timestamp") or "")[:16].replace("T", " "), "progetto": (r.get("project") or "").lower(),
                         "task": tid, "titolo": tid, "esito": st,
                         "frase": first or {"done": "completato", "failed": "non ha passato i controlli", "limit": "fermato dal limite di Claude"}.get(st, st),
                         "pct": pct_of(r.get("cost_usd")) if r.get("cost_usd") else 0, "secondi": None,
                         "dettagli": f"turni {r['num_turns']}" if r.get("num_turns") else "", "rapporto": "", "riassunto": txt[:1500]})
    except OSError:
        pass
    try:
        s = jload(CV / "stato" / "stato.json", {})
        uso = motori.righe_candidature()
        for j in s.get("coda", []):
            if j.get("stato") not in ("fatto", "errore"):
                continue
            ini, fin = (j.get("inizio") or "").replace("T", " "), (j.get("fine") or "").replace("T", " ")
            cost = sum(float(x.get("cost_usd_listprice") or 0) for x in uso if ini <= (x.get("started") or "") <= fin)
            rows.append({"quando": fin[:16], "progetto": "candidature", "task": j["id"],
                         "titolo": {"scout": "Scout", "cv": "Analisi + CV", "letter": "Lettera"}.get(j["tipo"], j["tipo"]),
                         "esito": "done" if j["stato"] == "fatto" else "failed", "frase": j.get("esito") or "", "pct": pct_of(cost),
                         "secondi": None, "dettagli": "", "rapporto": "", "riassunto": ""})
    except Exception:
        pass
    try:                                   # righe gia' scritte dal dispatcher: si tengono
        for line in DIARIO.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    except OSError:
        pass
    rows.sort(key=lambda x: x.get("quando") or "")
    with open(DIARIO, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (ROOT / ".diario_ricostruito").write_text(datetime.now().isoformat(), encoding="utf-8")


# ------------------------------------------------------------------ vista completa
def _piano(p, tasks_by_id):
    out = []
    for i, tp in enumerate(p.get("piano") or []):
        ids = tp.get("task") or []
        st = tp.get("stato")
        if not st:
            sts = [tasks_by_id[i_]["stato"] for i_ in ids if i_ in tasks_by_id]
            if ids and sts and all(x == "fatto" for x in sts) and len(sts) == len(ids):
                st = "fatto"
            elif any(x in ("fatto", "in_corso") for x in sts):
                st = "in_corso"
            else:
                st = "da_fare"
        out.append({"i": i, "testo": tp.get("testo", ""), "stato": st, "task": ids, "manuale": bool(tp.get("stato"))})
    return out


def stato_ufficio(cfg):
    D = _disp()
    gts = gen_tasks()
    by_id = {t["id"]: t for t in gts}
    cv = None
    try:
        cv = cv_dati()
    except Exception as e:
        H["log"](f"(candidature non leggibili: {e})")
    di = diario()
    prj = progetti()
    rot = jload(ROT, {})
    try:
        cands = D.candidati()
        ordine = D.ordine_simulato(cands, rot, {p["id"]: p for p in prj}, n=15)
    except Exception:
        ordine = []
    in_cima = set(rot.get("in_cima", []))
    coda = [{"progetto": c["progetto"], "id": c["id"], "titolo": c["titolo"], "nota": "pronto", "pronto": True,
             "in_cima": c["id"] in in_cima} for c in ordine]
    for t in gts:
        if t["cartella"] == "queue" and t["id"] not in {c["id"] for c in coda}:
            coda.append({"progetto": t["progetto"], "id": t["id"], "titolo": t["titolo"], "nota": t["nota"], "pronto": False,
                         "in_cima": t["id"] in in_cima})
    serve = []
    if cv:
        for o in cv["offerte"]:
            if o["stato"] == "da_approvare":
                serve.append({"progetto": "candidature", "tipo": "offerta", "id": o["id"], "titolo": o["titolo"],
                              "nota": o["nota"], "gap": o["gap"], "url": o["url"]})
        for q in cv["domande"]:
            serve.append({"progetto": "candidature", "tipo": "domanda", "id": q["id"], "titolo": q.get("azienda") or "",
                          "nota": q["testo"], "opzioni": q.get("opzioni") or []})
    for t in gts:
        if t["approvare"]:
            serve.append({"progetto": t["progetto"], "tipo": "approva_task", "id": t["id"], "titolo": t["titolo"], "nota": t["nota"],
                          "quando": t["approvare"]})
        elif t["cartella"] == "blocked":
            dec = GEN / "decisions" / f"{t['id']}.md"
            serve.append({"progetto": t["progetto"], "tipo": "decisione", "id": t["id"], "titolo": t["titolo"],
                          "nota": "l'agente ha delle domande", "testo": dec.read_text(encoding="utf-8", errors="replace")[:4000] if dec.exists() else ""})
        elif t["cartella"] == "failed" and time.time() - t["mtime"] < 3 * 86400:
            serve.append({"progetto": t["progetto"], "tipo": "fallito", "id": t["id"], "titolo": t["titolo"], "nota": t["nota"]})
    approva = []
    if cv:
        for o in cv["offerte"]:
            if o["stato"] == "da_approvare":
                approva.append({"tipo": "offerta", "id": o["id"], "progetto": "candidature", "titolo": o["titolo"],
                                "per_te": "CV e analisi per questa offerta" if o["stato_raw"] == "trovata" else "Lettera per questa offerta"})
    approva += approvazioni()
    domande = []
    if cv:
        for q in cv["domande"]:
            domande.append({"tipo": "cv", "id": q["id"], "progetto": "candidature", "domanda": q["testo"],
                            "opzioni": [o[1] for o in (q.get("opzioni") or [])], "scelta": "", "ferma": True, "titolo": q.get("azienda") or ""})
    for t in gts:
        if t["cartella"] == "blocked":
            dec = GEN / "decisions" / f"{t['id']}.md"
            domande.append({"tipo": "decisione", "id": t["id"], "progetto": t["progetto"], "domanda": f"{t['titolo']}: l'agente si e' fermato e ti chiede una decisione",
                            "opzioni": [], "scelta": "", "ferma": True, "testo": dec.read_text(encoding="utf-8", errors="replace")[:4000] if dec.exists() else ""})
    by_t = {t["id"]: t for t in gts}
    for d in domande_aperte():
        domande.append({"tipo": "agente", "id": d["id"], "progetto": d.get("progetto"), "domanda": d["domanda"], "opzioni": d.get("opzioni") or [],
                        "scelta": d.get("scelta") or "", "ferma": False, "task": d.get("task"), "dove": d.get("dove"),
                        "perche": d.get("perche") or d.get("contesto") or d.get("motivo") or "", "cambia": d.get("cambia") or "", "quando": d.get("quando") or "",
                        "task_titolo": by_t.get(d.get("task"), {}).get("titolo", ""), "task_stato": by_t.get(d.get("task"), {}).get("stato", "")})
    for p_ in prj:
        for i_, x_ in enumerate(p_.get("da_rivedere") or []):
            if not x_.get("fatto"):
                domande.append({"tipo": "scheda", "id": f"{p_['id']}#{i_}", "i": i_, "progetto": p_["id"], "domanda": "Scheda: " + x_.get("testo", ""),
                                "opzioni": [], "scelta": "", "ferma": False, "path": str(scheda.percorso(p_) or "")})
    falliti = [{"id": t["id"], "progetto": t["progetto"], "titolo": t["titolo"]} for t in gts
               if t["cartella"] == "failed" and time.time() - t["mtime"] < 3 * 86400]
    att = jload(ROOT / "agente_attuale.json", None)
    if att:
        try:
            att["da_s"] = int(time.time() - datetime.fromisoformat(att["inizio"]).timestamp())
        except Exception:
            att["da_s"] = None
    plist = []
    for p in prj:
        pid = p["id"]
        mine = [t for t in gts if t["progetto"] == pid]
        d = dict(p)
        d["piano"] = _piano(p, by_id)
        if p.get("tipo") == "candidature" and cv:
            d["conteggi"] = cv["conteggi"]
            d["cv"] = cv
        else:
            c = lambda st: sum(1 for t in mine if t["stato"] == st)
            d["conteggi"] = {"Fatti": c("fatto"), "In coda": c("in_coda") + c("in_corso"), "Da approvare": sum(1 for t in mine if t["approvare"]),
                             "Bloccati": c("bloccato"), "Falliti": c("fallito")}
        d["tasks"] = sorted(mine, key=lambda t: (t["cartella"] != "queue", -t["mtime"]))
        d["serve"] = sum(1 for x in approva + domande if x.get("progetto") == pid)
        last = next((x for x in di if x.get("progetto") == pid), None)
        d["ultimo"] = last
        nxt = next((x for x in coda if x["progetto"] == pid), None)
        d["prossimo"] = nxt
        d["git"] = bool(p.get("cartella")) and (Path(p["cartella"]) / ".git").exists()
        sf = scheda.percorso(p)
        d["scheda_path"] = str(sf) if sf else ""
        d["scheda_esiste"] = bool(sf and sf.exists())
        d["speciali"] = {k: any(t.get("tipo") == k and t["cartella"] == "queue" for t in mine) for k in ("consigli", "revisione")}
        aperte = [q for q in domande if q.get("progetto") == pid and q.get("tipo") == "agente"]
        d["domande_n"] = len(aperte)
        d["domande_chiuse"] = sum(1 for q in aperte if len(q.get("opzioni") or []) >= 2)
        d["in_corso"] = bool(att and att.get("progetto") == pid)
        plist.append(d)
    lim = comune.limite_fino()
    perche = comune.perche_non_parte("dispatcher") if not att else ""
    try:
        suc = succede(gts, cv, coda, approva, domande, att, di, prj, lim)
    except Exception as e:
        H.get("log", print)(f"(cosa succede non calcolato: {e})")
        suc = None
    try:
        cons = motori.consumo()
    except Exception:
        cons = None
    try:
        import consumo_dettaglio
        breve = consumo_dettaglio.riassunto()
    except Exception as e:
        H.get("log", print)(f"(riassunto consumo non calcolato: {e})")
        breve = None
    return {"succede": suc, "consumo": cons, "consumo_breve": breve, "motori": {"lista": motori.MOTORI, "chiave_openrouter": bool(motori.chiave("openrouter")),
                       "fornitori": [{"id": k, "nome": v["nome"], "chiave": bool(motori.chiave(k))} for k, v in motori.FORNITORI.items()], "predefinito": motori.predefinito()},
            "adesso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "contatore": comune.contatore(), "agente": att,
            "limite": comune.quando(lim) if lim else None, "perche_fermo": perche, "serve_te": serve, "coda": coda,
            "approva": approva, "domande": domande, "falliti": falliti,
            "diario": di[:40], "progetti": plist, "pausa": {"agenti": (GEN / "STOP").exists(), "candidature": bool(cv and cv["pausa"])},
            "dispatcher_attivo": _disp_attivo()}


def _disp_attivo():
    try:
        return time.time() - (ROOT / "dispatcher.lock").stat().st_mtime < 300
    except OSError:
        return False


def task_dettaglio(tid):
    t = None
    for cart in CARTELLE_GEN:
        f = GEN / cart / f"{tid}.task.md"
        if f.exists():
            t = parse_task(f)
            t["_cart"] = cart
            break
    if not t:
        return {"ok": False, "msg": "Task non trovato."}
    res = GEN / "results" / tid
    rd = lambda p: p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
    righe = []
    try:
        for line in rd(GEN / "logs" / "runner.log").splitlines():
            if f" {tid}:" in line or f" {tid} " in line:
                righe.append(line[:300])
    except Exception:
        pass
    u = _usage_gen().get(tid, {})
    repo = Path(t["repo"]) if t.get("repo") else None
    files = []
    if repo:
        for n in ("RAPPORTO.md", "RUNNER.md", "VALIDATORE.md", "DECISIONS.md"):
            f = repo / "agenti" / tid / n
            if f.exists():
                files.append({"nome": n, "path": str(f)})
        for a in _listify(t.get("allowed")):
            f = repo / a
            if f.exists():
                files.append({"nome": a, "path": str(f)})
    for f in sorted(res.glob("*")) if res.exists() else []:
        if f.is_file():
            files.append({"nome": "risultati/" + f.name, "path": str(f)})
        elif f.is_dir():
            for g in sorted(f.rglob("*"))[:20]:
                if g.is_file():
                    files.append({"nome": "risultati/" + str(g.relative_to(res)), "path": str(g)})
    files.append({"nome": "file del task (istruzioni)", "path": str(t["_path"])})
    di = [x for x in diario(400) if x.get("task") == tid]
    return {"ok": True, "id": tid, "titolo": t.get("title") or tid, "progetto": (t.get("project") or "").lower(), "scheda": scheda_corta(t),
            "motore": _motore_task(t), "modello": t.get("modello") or "",
            "stato": CARTELLE_GEN[t["_cart"]], "tier": t.get("tier", "small"), "cosa": t["body"][:3000],
            "permessi": _listify(t.get("allowed")), "repo": t.get("repo", ""), "ramo": t.get("branch") or (tid if repo else ""),
            "riassunto": rd(res / "summary.txt")[:3000], "validatore": rd(res / "VALIDATORE.log")[:3000],
            "timeline": righe[-40:], "diario": di[:10], "pct": pct_of(u.get("costo_tot")) if u else None,
            "turni": u.get("num_turns"), "files": files, "approvare": t.get("approval_before", "") or t.get("approval_after", ""),
            "proposta": bool(t.get("proposta")),
            "approvato": t.get("approved", "no"), **_dal_vivo(t, tid, res),
            "problema": problema(tid, t["_cart"], righe, t.get("repo"))}


# ------------------------------------------------------------------ problemi spiegati (piano v5, pezzo D)
_SPIEGA = [
    (r"would be overwritten by checkout|local changes", "git non ha potuto cambiare ramo: c'erano modifiche non salvate nella cartella del progetto"),
    (r"ramo .*esiste gia", "il ramo della task esisteva gia' e non si e' potuto riusare"),
    (r"repo non valido", "la cartella del progetto non e' un repository git valido"),
    (r"sarei su main|master", "per sicurezza mi sono fermato: sarei finito sul ramo principale (main)"),
    (r"file non tracciati", "nella cartella ci sono troppi file non tracciati da git (manca un .gitignore?)"),
    (r"fuori ambito|fuori dai percorsi|out of scope|non permess", "ha toccato file che non poteva toccare"),
    (r"NESSUNA MODIFICA APPLICATA|tutto o niente", "le modifiche proposte dal modello non combaciavano con i file: non e' stato scritto niente"),
    (r"tempo massimo|timeout|troppo lento", "il modello non ha risposto entro il tempo massimo"),
    (r"429|sovraccaric|rate limit", "i modelli gratis erano sovraccarichi"),
    (r"non ha prodotto nulla di valido", "il modello gratis non ha prodotto una risposta utilizzabile"),
    (r"controlli falliti|non ha passato i controlli", "il lavoro e' stato fatto ma non ha passato i controlli finali"),
    (r"turni|incomplete", "e' finito il tempo o il numero di passi a disposizione"),
    (r"limite di Claude|limit", "si e' fermato per il limite di Claude"),
]


def problema(tid, cartella, righe_log, repo=None):
    """Cosa e' andato storto, in parole semplici, + controlli falliti con i file collegati."""
    if cartella not in ("failed", "incomplete", "blocked"):
        return None
    res = GEN / "results" / tid
    out = {"spiegazione": "", "tecnico": "", "controlli": [], "stop": None}
    stp = res / "STOP.json"
    if stp.exists() and cartella == "failed":
        st = jload(stp, {})
        out["stop"] = st
        out["spiegazione"] = "L'hai fermata tu" + (f": {st.get('motivo')}" if st.get("motivo") else " (senza motivo)")
    ult = ""
    for l in reversed(righe_log or []):
        if re.search(r": (failed|blocked|incomplete)\b|errore|ERRORE|NESSUNA MODIFICA", l):
            ult = l[20:].replace(tid + ": ", "")
            break
    out["tecnico"] = ult[:400]
    if not out["spiegazione"]:
        if cartella == "blocked":
            out["spiegazione"] = "L'agente si e' fermato perche' ha delle domande per te"
        else:
            testo = re.sub(r"timeout \d+s|max turni \d+", "", ult + " " + " ".join(righe_log[-6:] if righe_log else []))
            for pat, frase in _SPIEGA:
                if re.search(pat, testo, re.I):
                    out["spiegazione"] = frase[0].upper() + frase[1:]
                    break
            if not out["spiegazione"]:
                out["spiegazione"] = "Non ha finito: vedi il dettaglio tecnico qui sotto"
    v = res / "VALIDATORE.log"
    if v.exists():
        txt = v.read_text(encoding="utf-8", errors="replace")
        blocco = txt.split("## Giro")[-1]
        cur = None
        for l in blocco.splitlines():
            m = re.match(r"- (ERRORE|AVVISO)\s+(.*)", l)
            if m:
                spec = m.group(2).strip()
                files = []
                for tok in re.findall(r"[\w./\\-]+\.[A-Za-z0-9]{1,6}", spec):
                    if repo and (Path(repo) / tok).exists():
                        files.append({"nome": tok, "path": str(Path(repo) / tok)})
                cur = {"tipo": m.group(1).lower(), "controllo": spec[:200], "dettagli": [], "file": files}
                out["controlli"].append(cur)
            elif cur and l.strip().startswith("- "):
                cur["dettagli"].append(l.strip()[2:][:200])
        out["controlli"] = out["controlli"][:15]
        out["validatore"] = str(v)
        err = [c for c in out["controlli"] if c["tipo"] == "errore"]
        if err and cartella == "failed" and not out["stop"] and not re.search(r"git:|repo non valido|main", ult):
            fuori = any(re.search(r"scope|ambito|allowed", c["controllo"] + " ".join(c["dettagli"]), re.I) for c in err)
            out["spiegazione"] = (f"Il lavoro e' stato fatto ma {len(err)} controll{"o non e' passato" if len(err) == 1 else "i non sono passati"}" +
                                  (": ha toccato file che non poteva toccare" if fuori else ""))
    return out


def _dal_vivo(t, tid, res):
    """Per la vista task (piano v5, pezzo C): e' in corso? con quale modello? quali file sta toccando? motivo dello Stop."""
    out = {"in_corso": jload(ROOT / "agente_attuale.json", {}).get("id") == tid, "ora": [], "toccati": [], "stop": None}
    stp = res / "STOP.json"
    if stp.exists():
        out["stop"] = jload(stp, None)
    if out["in_corso"]:
        try:
            out["inizio"] = jload(ROOT / "agente_attuale.json", {}).get("inizio")
            for c in motori.in_corso():
                if c.get("task") == tid:
                    out["ora"].append({"modello": (c.get("modello") or "").replace(":free", "").split("/")[-1], "motore": c.get("motore") or "",
                                       "fase": c.get("fase") or "", "da": c.get("modello_da") or c.get("inizio") or "", "inizio": c.get("inizio") or ""})
        except Exception:
            pass
        repo = Path(t["repo"]) if t.get("repo") else None
        if repo and (repo / ".git").exists():
            try:
                p = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=20, creationflags=0x08000000 if os.name == "nt" else 0)
                for l in (p.stdout or "").splitlines()[:30]:
                    if l.strip():
                        out["toccati"].append({"stato": {"M": "modificato", "A": "nuovo", "D": "cancellato", "??": "nuovo"}.get(l[:2].strip(), l[:2].strip()),
                                               "file": l[3:].strip().strip('"')})
            except Exception:
                pass
    return out


# ------------------------------------------------------------------ azioni
def _set_header(path, key, value):
    text = Path(path).read_text(encoding="utf-8-sig")
    head, sep, body = text.partition("\n---")
    lines = head.splitlines()
    for i, l in enumerate(lines):
        if l.strip().lower().startswith(key + ":"):
            lines[i] = f"{key}: {value}"
            break
    else:
        lines.append(f"{key}: {value}")
    Path(path).write_text("\n".join(lines) + sep + body, encoding="utf-8")


def _trova(tid, cartelle=("queue", "done", "blocked", "sospesi", "failed", "incomplete")):
    for c in cartelle:
        f = GEN / c / f"{tid}.task.md"
        if f.exists():
            return f
    return None


def _prossimo_id(p):
    pref = p.get("prefisso") or (p.get("sigla") or p["id"][:2]).upper()
    mx = 0
    for c in CARTELLE_GEN:
        for f in (GEN / c).glob("*.task.md") if (GEN / c).exists() else []:
            m = re.match(re.escape(pref) + r"(\d+)", f.name)
            if m:
                mx = max(mx, int(m.group(1)))
    return f"{pref}{mx + 1:02d}"


def task_nuova(body):
    p = progetto(str(body.get("progetto", "")))
    if not p:
        return {"ok": False, "msg": "Progetto non trovato."}
    if p.get("tipo") == "candidature":
        return {"ok": False, "msg": "Per le candidature usa Cerca offerte / Aggiungi offerta."}
    cosa = (body.get("cosa") or "").strip()
    if len(cosa) < 10:
        return {"ok": False, "msg": "Scrivi cosa deve fare (almeno una frase)."}
    titolo = (body.get("titolo") or "").strip() or cosa.split("\n")[0][:70]
    tier = GRANDEZZA.get(body.get("grandezza", "medio"), "medium")
    files = [x.strip().replace("\\", "/") for x in re.split(r"[,\n]", body.get("file") or "") if x.strip()]
    tid = _prossimo_id(p) + "-" + slug(titolo, 24)
    cart = Path(p.get("cartella") or "")
    lines = [f"id: {tid}", f"title: {titolo}", f"project: {p['id']}", f"tier: {tier}", "priority: 2",
             f"data_level: {p.get('livello_dati', 0)}", f"origine: {body.get('origine') or 'pannello'} {datetime.now():%Y-%m-%d %H:%M}",
             "per_te: " + " ".join(str(body.get("per_te") or titolo).split())[:200]]
    if body.get("motore") in motori.MOTORI:
        lines.append(f"motore: {body['motore']}")
    if (body.get("modello") or "").strip():
        lines.append("modello: " + re.sub(r"[^\w./:\-]", "", body["modello"].strip())[:80])
    if p.get("profilo") and (GEN / p["profilo"]).exists():
        lines.append(f"profile: {p['profilo']}")
    if (cart / ".git").exists():
        lines += [f"repo: {cart}", f"branch: {tid}"]
        if files:
            lines.append("allowed: [" + ", ".join(files) + "]")
            fl = [f for f in files if "." in Path(f).name]
            if fl:
                lines.append("checks: [files_exist:" + ";".join(fl) + "]")
        modo = "sui file veri del progetto (ramo git del task)"
    else:
        ins = [str(cart / f) for f in files if (cart / f).is_file()]
        if ins:
            lines.append("inputs: [" + ", ".join(ins) + "]")
        modo = "su una copia dei file indicati (la cartella del progetto non e' un repository git): il risultato va in generico\\results"
    if tier == "large":
        lines += ["approval_before: leo", "approved: no"]
    dest = GEN / ("sospesi" if body.get("sospesa") else "queue")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{tid}.task.md").write_text("\n".join(lines) + "\n---\n" + cosa + "\n", encoding="utf-8")
    if body.get("tappa") not in (None, "", -1, "-1"):
        try:
            i = int(body["tappa"])
            pj = progetto(p["id"])
            pj["piano"][i].setdefault("task", []).append(tid)
            jsave(PROG / f"{p['id']}.json", pj)
        except Exception:
            pass
    if body.get("in_cima"):
        rot = jload(ROT, {})
        rot.setdefault("in_cima", []).append(tid)
        jsave(ROT, rot)
    return {"ok": True, "id": tid, "msg": f"Task {tid} creata {('(serve il tuo OK: e grande) ' if tier == 'large' else '')}e messa "
            f"{'tra i sospesi' if body.get('sospesa') else 'in coda'}. Lavora {modo}."}


def task_approva(body):
    f = _trova(str(body.get("id", "")), ("queue", "done", "blocked"))
    if not f:
        return {"ok": False, "msg": "Task non trovato."}
    _set_header(f, "approved", "yes")
    return {"ok": True, "msg": "Approvato."}


def task_attiva(body):
    tid = str(body.get("id", ""))
    f = GEN / "sospesi" / f"{tid}.task.md"
    if not f.exists():
        return {"ok": False, "msg": "Non e' tra i sospesi."}
    (GEN / "queue").mkdir(exist_ok=True)
    shutil.move(str(f), str(GEN / "queue" / f.name))
    return {"ok": True, "msg": "Attivato: e' in coda."}


def task_sospendi(body):
    tid = str(body.get("id", ""))
    f = GEN / "queue" / f"{tid}.task.md"
    if not f.exists():
        return {"ok": False, "msg": "Si possono sospendere solo i task in coda."}
    if jload(ROOT / "agente_attuale.json", {}).get("id") == tid:
        return {"ok": False, "msg": "Ci sta lavorando un agente adesso."}
    (GEN / "sospesi").mkdir(exist_ok=True)
    shutil.move(str(f), str(GEN / "sospesi" / f.name))
    return {"ok": True, "msg": "Sospeso: non parte finche' non lo riattivi."}


def task_rifai(body):
    """Un task fallito/incompleto torna in coda (con una nota tua per l'agente, se la scrivi)."""
    tid = str(body.get("id", ""))
    f = _trova(tid, ("failed", "incomplete", "done"))
    if not f:
        return {"ok": False, "msg": "Task non trovato tra fatti/falliti."}
    nota = (body.get("nota") or "").strip()
    if nota:
        text = f.read_text(encoding="utf-8")
        f.write_text(text.rstrip() + f"\n\nNOTA DI LEO ({datetime.now():%Y-%m-%d}): {nota}\n", encoding="utf-8")
    shutil.move(str(f), str(GEN / "queue" / f.name))
    return {"ok": True, "msg": "Rimesso in coda."}


def in_cima(body):
    rot = jload(ROT, {})
    lst = [x for x in rot.get("in_cima", []) if x != body.get("id")]
    rot["in_cima"] = [str(body.get("id"))] + lst
    jsave(ROT, rot)
    return {"ok": True, "msg": "Messo in cima: parte per primo appena possibile."}


def decisione_rispondi(body):
    tid = str(body.get("id", ""))
    risp = (body.get("risposta") or "").strip()
    if not risp:
        return {"ok": False, "msg": "Scrivi la risposta."}
    dec = GEN / "decisions" / f"{tid}.md"
    blk = GEN / "blocked" / f"{tid}.task.md"
    if not dec.exists() or not blk.exists():
        return {"ok": False, "msg": "Domanda non trovata."}
    dec.write_text(dec.read_text(encoding="utf-8").rstrip() + "\n" + risp + "\n", encoding="utf-8")
    shutil.move(str(blk), str(GEN / "queue" / blk.name))
    return {"ok": True, "msg": "Risposta salvata: il task e' tornato in coda."}


def progetto_salva(body):
    nome = (body.get("nome") or "").strip()[:60]
    if not nome:
        return {"ok": False, "msg": "Manca il nome."}
    pid = body.get("id") or slug(nome, 20)
    f = PROG / f"{pid}.json"
    p = jload(f, {}) if body.get("id") else {}
    if not body.get("id") and f.exists():
        return {"ok": False, "msg": "Esiste gia' un progetto con questo nome."}
    p.update({"id": pid, "nome": nome})
    for k in ("obiettivo", "cartella", "frase"):
        if k in body:
            p[k] = str(body[k]).strip()[:400]
    if body.get("priorita") in ("alta", "media", "bassa"):
        p["priorita"] = body["priorita"]
    if body.get("motore") in motori.MOTORI:
        p["motore"] = body["motore"]
    elif "motore" in body and not body.get("motore"):
        p.pop("motore", None)          # "come l'Ufficio"
    if "livello_dati" in body:
        try:
            p["livello_dati"] = max(0, min(2, int(body["livello_dati"])))
        except ValueError:
            pass
    if "piano" in body and isinstance(body["piano"], str):
        old = {x.get("testo"): x for x in p.get("piano") or []}
        p["piano"] = [old.get(l.strip(), {"testo": l.strip(), "task": []}) for l in body["piano"].splitlines() if l.strip()]
    p.setdefault("sigla", re.sub(r"[^A-Z]", "", nome.upper())[:2] or "PR")
    p.setdefault("prefisso", p["sigla"])
    p.setdefault("colore", body.get("colore") or "#5fa8a0")
    p.setdefault("tipo", "generico")
    p.setdefault("stato", "attivo")
    p.setdefault("piano", [])
    PROG.mkdir(exist_ok=True)
    jsave(f, p)
    return {"ok": True, "id": pid, "msg": "Progetto salvato."}


def progetto_archivia(body):
    p = progetto(str(body.get("id", "")))
    if not p:
        return {"ok": False, "msg": "Progetto non trovato."}
    if body.get("riattiva"):
        p["stato"] = "attivo"
    else:
        p["stato"] = "archiviato"
        p["motivo_archivio"] = (body.get("motivo") or p.get("motivo_archivio") or "").strip()[:600]
        p["frase"] = f"Archiviato il {datetime.now():%d/%m/%Y}"
    jsave(PROG / f"{p['id']}.json", p)
    return {"ok": True, "msg": "Fatto."}


def tappa_stato(body):
    p = progetto(str(body.get("progetto", "")))
    try:
        i = int(body.get("i"))
        tp = p["piano"][i]
    except Exception:
        return {"ok": False, "msg": "Tappa non trovata."}
    st = body.get("stato")
    if st in ("da_fare", "in_corso", "fatto"):
        tp["stato"] = st
    else:
        tp.pop("stato", None)        # torna automatico (dai task)
    jsave(PROG / f"{p['id']}.json", p)
    return {"ok": True, "msg": "Tappa aggiornata."}


def avvia_dispatcher():
    """Fa partire il dispatcher (invisibile) se non sta gia' lavorando."""
    if _disp_attivo():
        return {"ok": True, "msg": "Gli agenti stanno gia' lavorando."}
    exe = Path(sys.executable)
    if os.name == "nt" and exe.name.lower() == "python.exe" and (exe.parent / "pythonw.exe").exists():
        exe = exe.parent / "pythonw.exe"
    kw = {"creationflags": 0x08000000} if os.name == "nt" else {}
    subprocess.Popen([str(exe), str(ROOT / "dispatcher.py")], cwd=str(ROOT), stdin=subprocess.DEVNULL,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kw)
    return {"ok": True, "msg": "Avviato."}



# ------------------------------------------------------------------ scheda corta per approvare
def _uso_medio(tier):
    use = _usage_gen()
    vals = []
    for tid, r in use.items():
        if (r.get("tier") or "") == tier and r.get("status") == "done" and float(r.get("costo_tot") or 0) > 0:
            vals.append(pct_of(r["costo_tot"]))
    return round(sum(vals) / len(vals)) if len(vals) >= 2 else USO_DEFAULT.get(tier, 12)


def scheda_corta(t):
    """Per approvare: cosa fa, cosa tocca, uso stimato, rischio. Niente testo per l'agente."""
    repo = Path(t["repo"]) if t.get("repo") else None
    allowed = _listify(t.get("allowed"))
    nuovi, modif = [], []
    for a in allowed:
        (modif if (repo and (repo / a).exists()) else nuovi).append(a)
    agente = bool(t.get("body", "").strip()) and t.get("agent", "auto").lower() != "no" and (not t.get("script") or t.get("agent", "auto").lower() == "yes")
    uso = _uso_medio(t.get("tier", "small")) if agente else 0
    tocca = []
    if nuovi:
        tocca.append(("crea " if repo else "") + ", ".join(nuovi))
    if modif:
        tocca.append("modifica " + ", ".join(modif))
    if t.get("script"):
        tocca.insert(0, "uno script del runner (" + t["script"] + ")")
    rischio = t.get("rischio") or ("basso" if (allowed and not modif and t.get("tier") != "large") else "medio")
    return {"per_te": t.get("per_te") or t.get("title") or t["id"],
            "tocca": "; ".join(tocca) or "non indicato",
            "uso": uso, "rischio": rischio, "agente": agente}


def approvazioni():
    out = []
    for cart in ("queue", "done"):
        for f in sorted((GEN / cart).glob("*.task.md")) if (GEN / cart).exists() else []:
            try:
                t = parse_task(f)
            except Exception:
                continue
            prima = cart == "queue" and t.get("approval_before", "").lower() == "leo"
            dopo = cart == "done" and t.get("approval_after", "").lower() == "leo"
            if (prima or dopo) and t.get("approved", "no").lower() != "yes":
                out.append({"tipo": "task", "id": t["id"], "progetto": (t.get("project") or "altro").lower(), "proposta": bool(t.get("proposta")),
                            "titolo": t.get("title") or t["id"], "quando": "prima" if prima else "dopo", **scheda_corta(t)})
    return out


# ------------------------------------------------------------------ domande non bloccanti
def _domande_tutte():
    rows = []
    try:
        for line in DOMANDE.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    except OSError:
        pass
    return rows


def domande_aperte():
    return [d for d in _domande_tutte() if d.get("stato") == "aperta"]


def _norm(x):
    return re.sub(r"\W+", " ", (x or "").lower()).strip()


def domanda_rispondi(body):
    did, risp = str(body.get("id", "")), (body.get("risposta") or "").strip()
    if not risp:
        return {"ok": False, "msg": "Scegli o scrivi una risposta."}
    rows = _domande_tutte()
    d = next((x for x in rows if x.get("id") == did and x.get("stato") == "aperta"), None) or \
        next((x for x in rows if x.get("id") == did), None)      # 05/10: con id doppi si risponde a quella ancora aperta
    if not d or d.get("stato") != "aperta":
        return {"ok": False, "msg": "Domanda non trovata o gia' risposta."}
    d.update(stato="risposta", risposta=risp, risposta_quando=datetime.now().strftime("%Y-%m-%d %H:%M"))
    tmp = Path(str(DOMANDE) + ".tmp")
    tmp.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
    tmp.replace(DOMANDE)
    p = progetto(d.get("progetto"))
    if p:
        p.setdefault("decisioni", []).append({"quando": d["risposta_quando"], "task": d.get("task"), "domanda": d["domanda"], "risposta": risp})
        p["decisioni"] = p["decisioni"][-60:]
        jsave(PROG / f"{p['id']}.json", p)
    _scheda_refresh(d.get("progetto"))
    if _norm(risp) == _norm(d.get("scelta")):
        return {"ok": True, "msg": "Confermata. Vale anche per le prossime task."}
    f0 = _trova(d.get("task", ""), tuple(CARTELLE_GEN))
    if f0 and parse_task(f0).get("tipo") in ("consigli", "revisione"):
        return {"ok": True, "msg": "Salvata: vale per le prossime task del progetto."}
    r = _task_correzione(d, risp)
    return {"ok": True, "msg": "Salvata. " + (r.get("msg") or "")}


def _task_correzione(d, risp):
    """La risposta e' diversa dalla scelta provvisoria: parte da sola una piccola task che corregge solo quel punto."""
    f = _trova(d.get("task", ""), ("done", "failed", "incomplete", "queue", "blocked"))
    if not f:
        return {"ok": False, "msg": "Task originale non trovata: la risposta vale solo per il futuro."}
    t = parse_task(f)
    base = t["id"].split("-")[0]
    n = 1
    while _trova(f"{base}-risposta{n}", tuple(CARTELLE_GEN)):
        n += 1
    tid = f"{base}-risposta{n}"
    lines = [f"id: {tid}", f"title: correzione di {base} dopo la tua risposta", f"project: {t.get('project', '')}", "tier: small", "priority: 1",
             f"per_te: Applica la tua risposta (\"{risp[:60]}\") al lavoro di {base}, solo dove serve.",
             f"origine: risposta di Leo {datetime.now():%Y-%m-%d %H:%M}"]
    for k in ("data_level", "profile", "repo", "motore", "modello"):     # 05/10: stesso motore e modello della task originale
        if t.get(k):
            lines.append(f"{k}: {t[k]}")
    if t.get("repo"):
        lines.append(f"branch: {tid}")
    for k in ("allowed", "checks", "inputs"):
        if t.get(k):
            lines.append(f"{k}: [" + ", ".join(_listify(t[k])) + "]")
    body = (f"Leo answered a question asked during task {t['id']} ({t.get('title', '')}).\n"
            f"Question: {d['domanda']}\nYour provisional choice was: {d.get('scelta')}\nLeo's answer: {risp}\n"
            f"Where it applies: {d.get('dove') or 'see the report of ' + t['id']}\n"
            "Update ONLY what this answer changes, keep everything else exactly as it is, keep 'origine' and 'stato' fields unchanged. "
            "Do not ask new questions unless really needed.")
    (GEN / "queue").mkdir(exist_ok=True)
    (GEN / "queue" / f"{tid}.task.md").write_text("\n".join(lines) + "\n---\n" + body + "\n", encoding="utf-8")
    return {"ok": True, "msg": f"Parte da sola la correzione {tid} (piccola)."}


# ------------------------------------------------------------------ pulizia pannello vecchio
def vecchio_elenco():
    P = HERE
    da_cancellare = [P / "pannello.html", P / "AVVIA_PANNELLO.bat", P / "_backup" / "pannello.html",
                     P / "_backup" / "pannello_server.py", P / "_backup" / "_info.json", GEN / "runner_v0_backup.py"]
    da_spostare = [P / "8b051b56-4707-4802-916e-05839ea64edb.png"] + sorted((P / "immagini").glob("Y5Lrdu*.png")) + \
        [P / "immagini" / "8b051b56-4707-4802-916e-05839ea64edb.png"]
    return [str(x) for x in da_cancellare if x.exists()], [str(x) for x in da_spostare if x.exists()]


def vecchio_elimina():
    canc, spost = vecchio_elenco()
    dest = HERE / "immagini" / "originali"
    for x in canc:
        Path(x).unlink(missing_ok=True)
    for x in spost:
        dest.mkdir(parents=True, exist_ok=True)
        tgt = dest / Path(x).name
        if tgt.exists():
            tgt = dest / ("root_" + Path(x).name)
        shutil.move(x, str(tgt))
    return {"ok": True, "msg": f"Pannello vecchio tolto: {len(canc)} file cancellati, {len(spost)} immagini originali spostate in immagini\\originali."}



# ------------------------------------------------------------------ scheda progetto, consigli, revisione
def _scheda_refresh(pid):
    """Aggiorna la parte automatica della scheda, ma non mentre un agente lavora su quel progetto."""
    try:
        if jload(ROOT / "agente_attuale.json", {}).get("progetto") != pid:
            scheda.aggiorna(pid)
    except Exception:
        pass


def consigli(body):
    return scheda.crea_speciale(str(body.get("progetto", "")), "consigli")


def revisione(body):
    return scheda.crea_speciale(str(body.get("progetto", "")), "revisione")


def task_scarta(body):
    tid = str(body.get("id", ""))
    f = _trova(tid, ("queue", "sospesi"))
    if not f:
        return {"ok": False, "msg": "Si possono scartare solo task non ancora partite."}
    (GEN / "scartate").mkdir(exist_ok=True)
    shutil.move(str(f), str(GEN / "scartate" / f.name))
    return {"ok": True, "msg": "Scartata (resta in generico\\scartate)."}


def scheda_fatto(body):
    p = progetto(str(body.get("progetto", "")))
    try:
        p["da_rivedere"][int(body.get("i"))]["fatto"] = True
    except Exception:
        return {"ok": False, "msg": "Voce non trovata."}
    jsave(PROG / f"{p['id']}.json", p)
    _scheda_refresh(p["id"])
    return {"ok": True, "msg": "Segnato come fatto."}


def scheda_crea(body):
    p = progetto(str(body.get("progetto", "")))
    f = scheda.crea_se_manca(p) if p else None
    if not f or not f.exists():
        return {"ok": False, "msg": "Il progetto non ha una cartella valida."}
    _scheda_refresh(p["id"])
    return {"ok": True, "path": str(f), "msg": "Scheda pronta."}



# ------------------------------------------------------------------ "Cosa succede" (riga in alto e pannello) - 05/10
FASI = {"agente": "lavora", "fix1": "corregge gli errori (1 di 2)", "fix2": "corregge gli errori (2 di 2)",
        "cv": "scrive analisi e CV", "letter": "scrive la lettera", "fix": "corregge CV o lettera",
        "scout": "cerca offerte sui siti", "nuove_aziende": "cerca nuove aziende", "modifica": "modifica il pannello"}
TIER_IT = {"small": "piccola", "medium": "media", "large": "grande"}


_LOGR = {"t": 0, "righe": []}


def _log_runner():
    """Righe del log del runner (lette al massimo ogni 5 s)."""
    if time.time() - _LOGR["t"] > 5:
        try:
            _LOGR["righe"] = (GEN / "logs" / "runner.log").read_text(encoding="utf-8", errors="replace").splitlines()[-3000:]
        except OSError:
            _LOGR["righe"] = []
        _LOGR["t"] = time.time()
    return _LOGR["righe"]


def _da(ts):
    """Secondi trascorsi da un timestamp (float) o da una data ISO; None se non si sa."""
    try:
        if isinstance(ts, (int, float)):
            return max(0, int(time.time() - ts))
        if ts:
            return max(0, int(time.time() - datetime.fromisoformat(str(ts).replace(" ", "T")[:19]).timestamp()))
    except Exception:
        pass
    return None


def _mtime(p):
    try:
        return p.stat().st_mtime
    except OSError:
        return None


def succede(gts, cv, coda, approva, domande, att, di, prj, lim):
    nomi = {p["id"]: p.get("nome") or p["id"] for p in prj}
    by_id = {t["id"]: t for t in gts}
    out = {"lavoro": [], "serve": [], "sistemare": [], "coda": [], "pausa": [], "limite": None, "ultimo": None}
    # --- al lavoro: il task del dispatcher + le chiamate in corso (fase precisa)
    vivi = motori.in_corso()
    if att:
        ch = next((c for c in vivi if c.get("task") in (att.get("id"), "") or c.get("progetto") == att.get("progetto")), None)
        if att.get("tipo") == "cv":
            fase = FASI.get((ch or {}).get("fase"), "prepara il lavoro") if ch else "prepara o controlla"
            solito = motori.durata_solita("candidature", fase=(ch or {}).get("fase") or "cv")
        else:
            t = by_id.get(att.get("id"), {})
            fase = FASI.get((ch or {}).get("fase"), "lavora") if ch else "controlla il risultato"
            solito = motori.durata_solita("generico", progetto=att.get("progetto", ""), livello=t.get("tier", ""))
        out["lavoro"].append({"progetto": att.get("progetto"), "id": att.get("id"), "titolo": att.get("titolo"),
                              "fase": fase, "da_s": _da(att.get("inizio")), "solito_s": solito, "motore": (ch or {}).get("motore") or "Claude"})
    for c in vivi:          # chiamate partite fuori dal dispatcher (es. dal pannello o a mano), tranne la chat
        if c.get("chi") == "pannello" or (att and (c.get("task") == att.get("id") or c.get("progetto") == att.get("progetto"))):
            continue
        out["lavoro"].append({"progetto": c.get("progetto"), "id": c.get("task"), "titolo": c.get("task"),
                              "fase": FASI.get(c.get("fase"), c.get("fase")), "da_s": _da(c.get("inizio")), "solito_s": None, "motore": c.get("motore") or "Claude"})
    # --- serve te
    for a in approva:
        if a.get("tipo") == "offerta":
            o = next((x for x in (cv or {}).get("offerte", []) if x["id"] == a["id"]), {})
            out["serve"].append({"progetto": "candidature", "id": a["id"], "titolo": a["titolo"], "tipo": "offerta",
                                 "dettaglio": "da approvare · " + a.get("per_te", "").lower(), "da_s": _da(o.get("creata") or o.get("quando"))})
        else:
            t = by_id.get(a["id"], {})
            nf = len(_listify(_task_campo(a["id"], "allowed")))
            det = ("da approvare" if a.get("quando") == "prima" else "fatta: da controllare") + \
                  (" · " + TIER_IT.get(t.get("tier"), "") if t.get("tier") else "") + (f" · tocca {nf} file" if nf else "")
            out["serve"].append({"progetto": a["progetto"], "id": a["id"], "titolo": a["titolo"], "tipo": "approva",
                                 "dettaglio": det[:140], "da_s": _da(t.get("mtime"))})
    gruppi = {}
    for q in domande:
        if q["tipo"] == "decisione":
            out["serve"].append({"progetto": q["progetto"], "id": q["id"], "titolo": by_id.get(q["id"], {}).get("titolo", q["id"]),
                                 "tipo": "decisione", "dettaglio": "si è fermato: ti chiede una decisione",
                                 "da_s": _da(by_id.get(q["id"], {}).get("mtime"))})
        elif q["tipo"] in ("agente", "cv"):
            k = (q["progetto"], q.get("task") or ("candidature" if q["tipo"] == "cv" else ""))
            g = gruppi.setdefault(k, {"n": 0, "ferma": False, "da": None})
            g["n"] += 1
            g["ferma"] = g["ferma"] or q.get("ferma")
            d = _da(next((x.get("quando") for x in _domande_tutte() if x.get("id") == q["id"]), None))
            g["da"] = max(g["da"] or 0, d or 0) or g["da"]
        elif q["tipo"] == "scheda":
            out["serve"].append({"progetto": q["progetto"], "id": q["id"], "titolo": "Scheda progetto", "tipo": "scheda",
                                 "dettaglio": q["domanda"].replace("Scheda: ", "da completare: ")[:140], "da_s": None})
    for (pid, tid), g in gruppi.items():
        tit = by_id.get(tid, {}).get("titolo") or ("Candidature" if pid == "candidature" else tid or "Domande")
        out["serve"].append({"progetto": pid, "id": tid, "titolo": tit, "tipo": "domande", "n": g["n"],
                             "dettaglio": f"{g['n']} domand{'a' if g['n'] == 1 else 'e'}" +
                                          ("" if g["ferma"] else " · il lavoro va avanti con risposte provvisorie"),
                             "da_s": g["da"]})
    out["serve"].sort(key=lambda x: -(x.get("da_s") or 0))
    # --- da sistemare: task falliti o interrotti (ultimi 7 giorni), lavori delle candidature finiti in errore (ultime 24 ore)
    for t in gts:
        if t["cartella"] in ("failed", "incomplete") and time.time() - t["mtime"] < 7 * 86400:
            det = "non ha passato i controlli" if t["cartella"] == "failed" else "interrotto: turni o tempo finiti"
            v = (GEN / "results" / t["id"] / "VALIDATORE.log")
            sm = GEN / "results" / t["id"] / "summary.txt"
            if t["cartella"] == "failed" and not v.exists() and sm.exists():
                prima = next((x.strip() for x in sm.read_text(encoding="utf-8", errors="replace").splitlines() if x.strip()), "")
                if prima and not prima.upper().startswith("ESITO"):
                    det = _corto(prima)
            if t["cartella"] == "failed" and v.exists():
                n_fix = v.read_text(encoding="utf-8", errors="replace").count("-> correzione")
                det += f" dopo {n_fix} correzion{'e' if n_fix == 1 else 'i'}" if n_fix else ""
            try:
                _rl = [l for l in _log_runner() if f" {t['id']}:" in l]
                _pb = problema(t["id"], t["cartella"], _rl[-40:])
                if _pb and _pb.get("spiegazione") and not _pb["spiegazione"].startswith("Non ha finito"):
                    det = _pb["spiegazione"][0].lower() + _pb["spiegazione"][1:]
            except Exception:
                pass
            stp = GEN / "results" / t["id"] / "STOP.json"
            if t["cartella"] == "failed" and stp.exists() and stp.stat().st_mtime >= t["mtime"] - 10:
                m = jload(stp, {}).get("motivo") or ""
                det = "fermata da te" + (f": {_corto(m)}" if m else " (nessun motivo)")
            out["sistemare"].append({"progetto": t["progetto"], "id": t["id"], "titolo": t["titolo"], "dettaglio": det, "da_s": _da(t["mtime"])})
    if cv:
        for j in cv.get("lavori", []):
            if j["stato"] == "errore" and (_da(j["quando"]) or 1e9) < 86400 and "limite" not in (j.get("esito") or "").lower():
                out["sistemare"].append({"progetto": "candidature", "id": j["id"], "titolo": {"scout": "Cerca offerte", "cv": "Analisi e CV",
                                         "letter": "Lettera"}.get(j["tipo"], j["tipo"]), "dettaglio": _corto(j.get("esito") or "errore"),
                                         "da_s": _da(j["quando"]), "cv": True})
    # --- in coda (solo i pronti, in ordine)
    pronti = [c for c in coda if c.get("pronto") and not (att and c["id"] == att.get("id"))]
    for i, c in enumerate(pronti):
        out["coda"].append({"progetto": c["progetto"], "id": c["id"], "titolo": c["titolo"],
                            "dettaglio": "parte appena si libera un posto" if i == 0 else "dopo " + (pronti[i - 1]["titolo"] or "")[:50],
                            "cima": c["progetto"] != "candidature"})
    # --- in pausa
    if (GEN / "STOP").exists():
        out["pausa"].append({"nome": "Task dei progetti", "sorgente": "agents", "da_s": _da(_mtime(GEN / "STOP"))})
    if cv and cv.get("pausa"):
        out["pausa"].append({"nome": "Candidature", "sorgente": "cv", "da_s": _da(_mtime(CV / "stato" / "STOP"))})
    if lim:
        out["limite"] = comune.quando(lim)
    if di:
        out["ultimo"] = {"titolo": di[0].get("titolo"), "progetto": di[0].get("progetto"), "da_s": _da(di[0].get("quando")),
                         "esito": di[0].get("esito")}
    ds = jload(ROOT / "logs" / "dispatcher_stato.json", {})
    out["controllo"] = {"da_s": _da(ds.get("quando")), "esito": ds.get("esito"), "perche": ds.get("perche")}
    # --- riga in alto
    if out["lavoro"]:
        out["fermo_da_s"] = None
    else:
        fine = [x for x in (out["ultimo"] or {}, ) if x]
        out["fermo_da_s"] = fine[0].get("da_s") if fine else None
    out["nomi"] = nomi
    return out


def _corto(t, n=90):
    t = " ".join(str(t).split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"


def _task_campo(tid, campo):
    for cart in ("queue", "done"):
        f = GEN / cart / f"{tid}.task.md"
        if f.exists():
            try:
                return parse_task(f).get(campo)
            except Exception:
                return None
    return None


def annota_claude(body):
    def num(v):
        try:
            v = float(str(v).replace("%", "").replace(",", ".").strip())
            return v if 0 < v <= 100 else None
        except (TypeError, ValueError):
            return None
    a, b = num(body.get("pct5h")), num(body.get("pct7g"))
    if a is None and b is None:
        return {"ok": False, "msg": "Scrivi almeno un numero tra 1 e 100."}
    motori.annota_claude(a, b)
    c = motori.calibrazione()
    return {"ok": True, "msg": f"Annotato ({c['n']} in tutto)." + ("" if c["cento_5h"] or c["cento_7g"] else " La stima parte da 3 annotazioni.")}



# ------------------------------------------------------------------ motori (fase B)
def _motore_task(t):
    m = (t.get("motore") or "").strip().lower()
    if m in motori.MOTORI:
        return m
    p = progetto((t.get("project") or "").lower()) or {}
    return p.get("motore") if p.get("motore") in motori.MOTORI else motori.predefinito()


def chiave_salva(body):
    nome = str(body.get("nome") or "openrouter")
    if nome != "openrouter" and nome not in motori.FORNITORI:
        return {"ok": False, "msg": "Motore sconosciuto."}
    v = (body.get("valore") or "").strip()
    if nome == "openrouter" and v and not v.startswith("sk-or-"):
        return {"ok": False, "msg": "Non sembra una chiave di OpenRouter (inizia con sk-or-)."}
    on = motori.salva_chiave(nome, v)
    return {"ok": True, "msg": "Chiave salvata (fuori dalle cartelle che la chat può leggere)." if on else "Chiave tolta."}


def prova_motore(body):
    return motori.prova(str(body.get("motore") or "openrouter"))
