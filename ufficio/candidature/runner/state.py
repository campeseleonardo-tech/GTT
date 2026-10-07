#!/usr/bin/env python3
"""
state.py - lo STATO UNICO delle candidature.

Tutto quello che il runner e il pannello devono ricordarsi sta in UN file: stato\\stato.json
(offerte, domande e risposte, direzioni/hint, coda dei lavori, esito dello scout).
Il file leggibile stato\\coda.md viene RIGENERATO da qui a ogni cambiamento: non si modifica a mano.

Usato sia da runner.py sia dal pannello. Solo libreria standard di Python.
Regola di casa: niente file o cartelle nuovi a ogni giro. Si sovrascrive sempre lo stesso posto.
"""
import json, os, re, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent          # ...\Multiple Agents\candidature\runner
BASE = HERE.parent                              # ...\Multiple Agents\candidature
DOCS_HOME = Path(os.environ.get("CV_DOCS_HOME", r"C:\Users\campe\Desktop\CV"))   # i 3 documenti base restano qui
STATO = BASE / "stato"
STATE_FILE = STATO / "stato.json"
LOCK_FILE = STATO / "stato.lock"
RUN_LOCK = STATO / "attivo.lock"                # c'e' un solo agente alla volta
STOP_FILE = STATO / "STOP"
LAVORO = STATO / "lavoro"                       # UNICA cartella di lavoro, si svuota a ogni lavoro
CODA_MD = STATO / "coda.md"
LOG_FILE = STATO / "log.txt"
USO_CSV = STATO / "uso.csv"
OUT = BASE / "output"
ARCHIVIO = BASE / "Archivio"                     # storico (vecchi output e simili), mai letto dagli agenti se non per confronto
DOCS = ["Job search framework.md", "CV_description_baseline.txt", "cover letter baseline.md"]
DEFAULTS = {"model": "sonnet", "effort": "low", "letter_effort": "medium", "scout_effort": "medium",
            "turns": 25, "timeout_min": 30, "scout_picks": 3, "scout_companies": 6, "scout_b": False,
            "nuove_aziende": 4, "controllo_link": 20}
PHASE_NAMES = {"cv": "Analisi e CV", "letter": "Lettera", "fix": "Correzione", "scout": "Scout",
               "manutenzione": "Manutenzione", "nuove_aziende": "Nuove aziende"}


def doc_path(name):
    """I tre documenti base restano dove sono: prima candidature\\input, poi candidature, poi Desktop\\CV."""
    for d in (BASE / "input", BASE, DOCS_HOME):
        if (d / name).exists():
            return d / name
    return DOCS_HOME / name


def now_iso():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


# ------------------------------------------------------------ file + blocco
class _Lock:
    def __enter__(self):
        STATO.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        while True:
            try:
                fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return self
            except FileExistsError:
                try:
                    if time.time() - LOCK_FILE.stat().st_mtime > 20:     # blocco rimasto da un crash
                        LOCK_FILE.unlink()
                        continue
                except OSError:
                    pass
                if time.time() - t0 > 20:
                    raise TimeoutError("stato.json occupato da troppo tempo")
                time.sleep(0.05)

    def __exit__(self, *a):
        try:
            LOCK_FILE.unlink()
        except OSError:
            pass


def empty_state():
    return {"v": 1, "seq": 0, "offerte": [], "domande": [], "hint": [], "coda": [],
            "scout": {"last": {}, "proposed": [], "ultimo": None, "controllate": []},
            "mappa": {}, "registro": [], "manutenzione": {"ultimo": None, "nuove": None},
            "impostazioni": dict(DEFAULTS)}


def _read():
    for _ in range(5):
        try:
            s = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            break
        except FileNotFoundError:
            return empty_state()
        except Exception:
            time.sleep(0.1)
    else:
        return empty_state()
    base = empty_state()
    for k, v in base.items():
        s.setdefault(k, v)
    for k, v in base["scout"].items():
        s["scout"].setdefault(k, v)
    for k, v in base["manutenzione"].items():
        s["manutenzione"].setdefault(k, v)
    for k, v in DEFAULTS.items():
        s["impostazioni"].setdefault(k, v)
    return s


def load():
    return _read()


def _write(s):
    STATO.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(s, indent=1, ensure_ascii=False), encoding="utf-8")
    for i in range(8):
        try:
            os.replace(tmp, STATE_FILE)
            return
        except PermissionError:
            time.sleep(0.1)
    os.replace(tmp, STATE_FILE)


def update(fn):
    """Legge, applica fn(stato), riscrive, rigenera coda.md. Ritorna quello che ritorna fn."""
    with _Lock():
        s = _read()
        r = fn(s)
        _prune(s)
        _write(s)
        try:
            write_coda_md(s)
        except Exception as e:      # il rapporto e' comodo ma non deve rompere il lavoro
            log(f"(coda.md non scritto: {e})")
    return r


def _prune(s):
    if len(s["coda"]) > 60:
        s["coda"] = s["coda"][-60:]


def nid(s, prefix):
    s["seq"] += 1
    return f"{prefix}{s['seq']}"


# --------------------------------------------------------------------- log
def log(msg, to_console=True):
    line = f"[{datetime.now():%H:%M:%S}] {msg}"
    if to_console:
        try:
            print(line, flush=True)
        except Exception:
            pass
    try:
        STATO.mkdir(parents=True, exist_ok=True)
        if LOG_FILE.exists() and LOG_FILE.stat().st_size > 400_000:     # un solo log, si tiene la coda
            keep = LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()[-1500:]
            LOG_FILE.write_text("\n".join(keep) + "\n", encoding="utf-8")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d} {line}\n")
    except Exception:
        pass


def offer_log(offer, msg):
    """Riga di diario dentro l'offerta (ultime 120). Va chiamata dentro update()."""
    offer.setdefault("log", []).append(f"[{datetime.now():%H:%M:%S}] {msg}")
    offer["log"] = offer["log"][-120:]


# ----------------------------------------------------------------- offerte
def find_offer(s, oid):
    return next((o for o in s["offerte"] if o["id"] == oid), None)


def add_offer(s, url="", testo="", nome="", nota="", azienda="", ruolo="", sede="", perche="", gap="",
              pubblicata="", stato="trovata", origine="manuale"):
    url = (url or "").strip()
    if url:
        for o in s["offerte"]:
            if o.get("url", "").rstrip("/") == url.rstrip("/"):
                return o, False
    elif testo:
        for o in s["offerte"]:
            if o.get("testo", "").strip() == testo.strip():
                return o, False
    o = {"id": nid(s, "o"), "url": url, "azienda": azienda, "ruolo": ruolo or nome, "sede": sede, "lingua": "",
         "stato": stato, "origine": origine, "nota": nota, "perche": perche, "gap": gap, "pubblicata": pubblicata,
         "testo": (testo or "").strip(), "ctx": None, "tag": "", "analisi": "", "controlli": "", "esito": "",
         "giri": 0, "fasi": [], "log": [], "creata": now_iso()}
    s["offerte"].append(o)
    offer_log(o, f"offerta aggiunta ({origine})")
    return o, True


def label(o):
    a, r = o.get("azienda") or "", o.get("ruolo") or ""
    if a and r:
        return f"{a} - {r}"
    return a or r or (o.get("url") or "offerta")[:60]


# -------------------------------------------------------------------- coda
def enqueue(s, tipo, offerta=None):
    for j in s["coda"]:
        if j["tipo"] == tipo and j.get("offerta") == offerta and j["stato"] in ("in_attesa", "in_corso"):
            return j
    j = {"id": nid(s, "j"), "tipo": tipo, "offerta": offerta, "stato": "in_attesa", "creato": now_iso(),
         "inizio": None, "fine": None, "esito": ""}
    s["coda"].append(j)
    return j


def next_job(s):
    return next((j for j in s["coda"] if j["stato"] == "in_attesa"), None)


def last_job(s, oid):
    js = [j for j in s["coda"] if j.get("offerta") == oid]
    return js[-1] if js else None


def advance(s, o):
    """Passo successivo di un'offerta (e' quello che fa il pulsante Approva). Ritorna 'cv', 'letter' o None."""
    if o["stato"] in ("trovata", "approvata"):
        o["stato"] = "approvata"
        enqueue(s, "cv", o["id"])
        offer_log(o, "approvata: parte analisi + CV")
        return "cv"
    if o["stato"] in ("cv_pronto", "lettera"):
        o["stato"] = "lettera"
        enqueue(s, "letter", o["id"])
        offer_log(o, "approvato il CV: parte la lettera")
        return "letter"
    return None


def redo(s, o, fase):
    """Rifai una fase ('cv' o 'letter'): sovrascrive gli stessi file."""
    if fase.startswith("l"):
        o["stato"] = "lettera"
        enqueue(s, "letter", o["id"])
    else:
        o["stato"] = "approvata"
        enqueue(s, "cv", o["id"])
    offer_log(o, "rifacimento richiesto: " + fase)


# ----------------------------------------------------------------- domande
def open_questions(s, oid=None):
    return [q for q in s["domande"] if not q.get("risposta") and (oid is None or q["offerta"] == oid)]


def add_question(s, oid, testo, opzioni=None, tipo="info"):
    testo = " ".join((testo or "").split())
    if not testo:
        return None
    key = norm(testo)
    for q in s["domande"]:
        if q["offerta"] == oid and norm(q["testo"]) == key:
            return None            # gia' chiesta (anche se gia' risposta): non si richiede
    q = {"id": nid(s, "q"), "offerta": oid, "testo": testo, "opzioni": opzioni or [], "tipo": tipo,
         "data": datetime.now().strftime("%Y-%m-%d"), "risposta": "", "quando": None}
    s["domande"].append(q)
    return q


def answer_question(s, qid, risposta):
    q = next((x for x in s["domande"] if x["id"] == qid), None)
    if not q:
        return None
    q["risposta"] = risposta.strip()
    q["quando"] = now_iso()
    o = find_offer(s, q["offerta"])
    if o is not None:
        if q.get("tipo") == "testo_offerta":
            o["testo"] = q["risposta"]
        offer_log(o, "risposta salvata: " + q["testo"][:60])
    if q.get("tipo") != "testo_offerta" and q["risposta"]:
        az = (o.get("azienda") if o else "") or (label(o) if o else "")
        riga = f"- [AUTO {datetime.now():%Y-%m-%d} | {az}] Q: {' '.join(q['testo'].split())} | A: {' '.join(q['risposta'].split())}"
        try:
            if baseline_auto_add(riga):
                reg_add(s, "python", "baseline", q["offerta"], "", None, riga, "risposta data nel pannello")
        except Exception as e:
            log(f"(baseline non aggiornata con la risposta: {e})")
    return q


# -------------------------------------------------------------------- hint
HINT_AMBITI = ("scout", "cv", "lettera", "tutti")


def hints_for(s, oid=None, fase=None):
    """Direzioni valide per una fase ('scout','cv','lettera') o per una singola offerta (ambito = id offerta)."""
    out = []
    for h in s["hint"]:
        a = h.get("ambito")
        if a == "tutti" or (fase and a == fase) or (oid and a == oid):
            out.append(h)
    return out


def hint_label(s, amb):
    names = {"scout": "solo scout", "cv": "solo CV", "lettera": "solo lettera", "tutti": "tutte le fasi"}
    if amb in names:
        return names[amb]
    o = find_offer(s, amb)
    return label(o) if o else amb


# ===================================================== baseline: sezione AUTO
AUTO_TITLE = "10. AUTO-ADDED FACTS"
BASELINE_NAME = "CV_description_baseline.txt"


def auto_split(text):
    """(parte normale, sezione AUTO). La sezione AUTO e' l'unica che programmi e agenti possono scrivere."""
    i = text.find("\n" + AUTO_TITLE)
    if i < 0:
        return text, ""
    j = text.rfind("\n=====", 0, i)
    if j < 0:
        j = i
    return text[:j + 1], text[j + 1:]


def _bl_read():
    p = doc_path(BASELINE_NAME)
    raw = p.read_bytes()
    return p, raw.startswith(b"\xef\xbb\xbf"), raw.decode("utf-8-sig")


def _bl_write(p, bom, text):
    data = text.encode("utf-8")
    p.write_bytes((b"\xef\xbb\xbf" if bom else b"") + data)


def baseline_auto_add(riga):
    """Aggiunge UNA riga etichettata [AUTO ...] in fondo alla baseline. Ritorna False se c'era gia'."""
    p, bom, text = _bl_read()
    nl = "\r\n" if "\r\n" in text else "\n"
    main, auto = auto_split(text)
    core = norm(riga.split("]", 1)[-1])
    for ln in auto.splitlines():
        if ln.startswith("- [AUTO") and norm(ln.split("]", 1)[-1]) == core:
            return False
    if not auto:
        sep = "=" * 69
        main = main if main.endswith("\n") else main + nl
        auto = nl.join(["", sep, AUTO_TITLE + " (written by the panel/agents, always tagged [AUTO ...]; Leonardo reviews, corrects or",
                        "promotes them to the sections above. Treat them as facts told by Leonardo himself.)", sep, ""])
        auto = auto.lstrip("\r\n") if main.endswith("\n\n") else auto
    if not auto.endswith("\n"):
        auto += nl
    _bl_write(p, bom, main + auto + riga + nl)
    return True


def baseline_auto_remove(riga):
    p, bom, text = _bl_read()
    nl = "\r\n" if "\r\n" in text else "\n"
    main, auto = auto_split(text)
    lines = auto.splitlines()
    keep = [ln for ln in lines if ln.strip() != riga.strip()]
    if len(keep) == len(lines):
        return False
    if not any(ln.startswith("- [AUTO") for ln in keep):
        _bl_write(p, bom, main.rstrip("\r\n") + nl)
    else:
        _bl_write(p, bom, main + nl.join(keep) + nl)
    return True


# ================================================ mappa aziende + registro
def today():
    return datetime.now().strftime("%Y-%m-%d")


def reg_add(s, chi, tipo, oggetto, campo, prima, dopo, motivo):
    """Ogni modifica fatta da programma o agente lascia una riga qui: prima/dopo, e si puo' annullare."""
    r = {"id": nid(s, "r"), "quando": now_iso(), "chi": chi, "tipo": tipo, "oggetto": oggetto, "campo": campo,
         "prima": prima, "dopo": dopo, "motivo": motivo, "stato": "attivo" if chi != "lui" else "ok"}
    s["registro"].append(r)
    s["registro"] = s["registro"][-400:]
    return r


def find_company(s, nome):
    n = norm(nome)
    if not n:
        return None
    best, gap = None, 99
    for c in s["mappa"].values():
        cn = norm(c.get("name"))
        if cn == n:
            return c
        if cn and min(len(cn), len(n)) >= 4 and (cn in n or n in cn):
            g = abs(len(cn) - len(n))
            if g < gap:
                best, gap = c, g
    return best


def map_set(s, cid, campo, valore, chi, motivo, registra=True):
    c = s["mappa"].get(cid)
    if c is None:
        return False
    prima = c.get(campo)
    if prima == valore:
        return False
    c[campo] = valore
    c["aggiornata"] = today()
    if registra:
        reg_add(s, chi, "mappa", cid, campo, prima, valore, motivo)
    return True


def map_add(s, d, chi, motivo):
    base = re.sub(r"[^a-z0-9]+", "-", norm(d.get("name")).replace(" ", "-"))[:30].strip("-") or "azienda"
    cid, n = base, 2
    while cid in s["mappa"]:
        cid, n = f"{base}-{n}", n + 1
    c = {"id": cid, "name": d.get("name", ""), "city": d.get("city", ""), "country": d.get("country", ""),
         "sector": d.get("sector", ""), "url": d.get("url", ""), "roles": d.get("roles", ""), "bridge": d.get("bridge", ""),
         "desc": d.get("desc", ""), "priority": d.get("priority") or "B", "status": "Da esplorare", "notes": "",
         "entry": d.get("entry", ""), "travel": d.get("travel", ""), "weapons": bool(d.get("weapons")), "clearance": False,
         "origine": "agente" if chi != "lui" else "lui", "nuova": chi != "lui", "creata": today(), "aggiornata": today()}
    s["mappa"][cid] = c
    reg_add(s, chi, "mappa_nuova", cid, "", None, c["name"], motivo)
    return c


def reg_undo(s, rid):
    r = next((x for x in s["registro"] if x["id"] == rid), None)
    if r is None:
        return False, "Modifica non trovata."
    if r["stato"] != "attivo":
        return False, "Questa modifica e' gia' stata gestita."
    if r["tipo"] == "mappa":
        c = s["mappa"].get(r["oggetto"])
        if c is None:
            return False, "L'azienda non c'e' piu'."
        if r["prima"] is None:
            c.pop(r["campo"], None)
        else:
            c[r["campo"]] = r["prima"]
    elif r["tipo"] == "mappa_nuova":
        s["mappa"].pop(r["oggetto"], None)
    elif r["tipo"] == "baseline":
        if not baseline_auto_remove(r["dopo"]):
            return False, "La riga non e' piu' nella baseline (forse l'hai gia' tolta o corretta a mano)."
    r["stato"] = "annullato"
    return True, "Modifica annullata."


def company_jobs(s, c):
    """Offerte collegate a un'azienda (derivate: niente da tenere allineato a mano)."""
    out = []
    for o in s["offerte"]:
        if o["stato"] == "scartata":
            continue
        if o.get("mappa_id") == c["id"] or (not o.get("mappa_id") and find_company(s, o.get("azienda")) is c):
            stato, nota, _ = offer_view(s, o)
            out.append({"id": o["id"], "ruolo": o.get("ruolo") or "", "stato": stato, "tag": o.get("tag") or ""})
    return out


def map_view(s):
    rows = []
    for c in s["mappa"].values():
        d = dict(c)
        d["lavori"] = company_jobs(s, c)
        rows.append(d)
    rows.sort(key=lambda x: ((x.get("priority") or "C"), (x.get("name") or "").lower()))
    return rows


def applied_names():
    """Aziende gia' candidate: la riga 'Already applied' della baseline (e' lei la fonte, non il codice)."""
    try:
        text = _bl_read()[2]
    except Exception:
        return []
    m = re.search(r"Already applied[^:]*:(.*?)(?:\n\s*\n|\n={5,})", text, flags=re.S)
    if not m:
        return []
    body = re.sub(r"\([^)]*\)", " ", m.group(1))
    names = []
    for part in re.split(r"[,;\n]| and ", body):
        part = re.sub(r"[.]+$", "", " ".join(part.split()))
        if len(part) >= 3:
            names.append(part)
    return names


# ------------------------------------------------------- vista per il pannello
def _fasi_tot(o):
    f = o.get("fasi") or []
    return (sum((x.get("turni") or 0) for x in f), sum((x.get("token") or 0) for x in f),
            round(sum((x.get("costo") or 0) for x in f), 4))


def offer_view(s, o):
    """(stato del pannello, nota, fase in corso) per una offerta."""
    job = last_job(s, o["id"])
    nq = len(open_questions(s, o["id"]))
    stato = o["stato"]
    if job and job["stato"] == "in_corso":
        return "in_corso", "In corso: " + PHASE_NAMES.get(job["tipo"], job["tipo"]).lower() + ".", PHASE_NAMES.get(job["tipo"])
    if job and job["stato"] == "in_attesa":
        return "in_coda", "Aspetta il suo turno: " + PHASE_NAMES.get(job["tipo"], job["tipo"]).lower() + ".", None
    if job and job["stato"] == "errore" and stato in ("approvata", "lettera"):
        return "fallito", (job.get("esito") or "Il lavoro non e' riuscito.") + " Usa Rifai per riprovare.", None
    if nq:
        return "bloccato", f"{nq} {'domanda' if nq == 1 else 'domande'} per te: rispondi nel pannello e il lavoro riparte da solo.", None
    if stato == "trovata":
        return "da_approvare", "Offerta trovata dallo scout. Approva per preparare analisi e CV.", None
    if stato == "cv_pronto":
        e = o.get("esito") or ""
        nota = "CV pronto. Approva per far scrivere la lettera."
        if e.startswith("DA RIVEDERE"):
            nota = "CV pronto ma con errori residui dei controlli. Rivedi, poi approva per la lettera."
        return "da_approvare", nota, None
    if stato == "pronta":
        e = o.get("esito") or "OK"
        if e.startswith("DA RIVEDERE"):
            return "incompleto", "CV e lettera consegnati, ma restano errori dei controlli: da rivedere a mano.", None
        return "completato", "CV e lettera consegnati in output.", None
    if stato in ("approvata", "lettera"):
        return "in_coda", "In attesa di partire.", None
    return "in_coda", "", None


def panel_view(s):
    """Task e domande nella forma che il pannello gia' conosce."""
    tasks, domande = [], []
    for o in s["offerte"]:
        if o["stato"] == "scartata":
            continue
        stato, nota, fase = offer_view(s, o)
        fasi = [dict(x) for x in o.get("fasi", [])]
        turni, token, costo = _fasi_tot(o)
        inizio = fasi[0].get("inizio") if fasi else o.get("creata")
        fine = None
        if stato != "in_corso" and fasi:
            fine = max((x.get("fine") or "" for x in fasi), default=None) or None
        tasks.append({"oid": o["id"], "titolo": label(o), "stato": stato, "fase": fase, "inizio": inizio, "fine": fine,
                      "turni": turni or None, "token": token or None, "costo": costo or None, "nota": nota,
                      "fasi": fasi, "esito": o.get("esito") or None, "etichetta": s["impostazioni"]["model"] + " · " + s["impostazioni"]["effort"]})
        for q in open_questions(s, o["id"]):
            domande.append({"id": q["id"], "oid": o["id"], "data": q["data"], "azienda": o.get("azienda") or label(o),
                            "testo": q["testo"], "opzioni": [[chr(65 + i), t] for i, t in enumerate(q.get("opzioni") or [])],
                            "importanza": "alta" if q.get("tipo") == "testo_offerta" else "media"})
    sc = s["scout"].get("ultimo")
    jobs = [j for j in s["coda"] if j["tipo"] == "scout"]
    if jobs and jobs[-1]["stato"] in ("in_attesa", "in_corso"):
        j = jobs[-1]
        tasks.append({"oid": "scout", "titolo": "Scout: cerca offerte vere", "stato": "in_corso" if j["stato"] == "in_corso" else "in_coda",
                      "fase": "Cerco offerte" if j["stato"] == "in_corso" else None, "inizio": j.get("inizio") or j.get("creato"),
                      "fine": None, "turni": None, "token": None, "costo": None, "fasi": [], "esito": None,
                      "nota": "Cerco annunci aperti nelle aziende A." if j["stato"] == "in_corso" else "Aspetta il suo turno.",
                      "etichetta": s["impostazioni"]["model"] + " · " + s["impostazioni"]["scout_effort"]})
    elif sc:
        tasks.append({"oid": "scout", "titolo": "Scout: cerca offerte vere", "stato": sc.get("stato", "completato"), "fase": None,
                      "inizio": sc.get("inizio"), "fine": sc.get("fine"), "turni": sc.get("turni"), "token": None,
                      "costo": sc.get("costo"), "fasi": [], "esito": None, "nota": sc.get("nota", ""),
                      "etichetta": s["impostazioni"]["model"] + " · " + s["impostazioni"]["scout_effort"]})
    for tipo, oid, titolo, run_nota, key in (("manutenzione", "manutenzione", "Manutenzione mappa e controlli", "Controllo link e coerenza (senza token).", "ultimo"),
                                              ("nuove_aziende", "nuove_aziende", "Nuove aziende per la mappa", "Cerco aziende nuove adatte al profilo.", "nuove")):
        jobs = [j for j in s["coda"] if j["tipo"] == tipo]
        last = (s.get("manutenzione") or {}).get(key)
        et = s["impostazioni"]["model"] + " · " + (s["impostazioni"]["scout_effort"] if tipo == "nuove_aziende" else "senza agente")
        if jobs and jobs[-1]["stato"] in ("in_attesa", "in_corso"):
            j = jobs[-1]
            run = j["stato"] == "in_corso"
            tasks.append({"oid": oid, "titolo": titolo, "stato": "in_corso" if run else "in_coda", "fase": "In corso" if run else None,
                          "inizio": j.get("inizio") or j.get("creato"), "fine": None, "turni": None, "token": None, "costo": None,
                          "fasi": [], "esito": None, "nota": run_nota if run else "Aspetta il suo turno.", "etichetta": et})
        elif last:
            tasks.append({"oid": oid, "titolo": titolo, "stato": last.get("stato", "completato"), "fase": None,
                          "inizio": last.get("inizio"), "fine": last.get("fine"), "turni": last.get("turni"), "token": None,
                          "costo": last.get("costo"), "fasi": [], "esito": None, "nota": last.get("nota", ""), "etichetta": et})
    return tasks, domande


# -------------------------------------------------------------- coda.md
def write_coda_md(s):
    L = ["# Candidature: stato e offerte",
         "",
         f"File unico GENERATO dal programma (aggiornato {datetime.now():%Y-%m-%d %H:%M}). Non modificarlo a mano: "
         "le domande e le direzioni si gestiscono dal pannello.",
         ""]
    todo = []
    for q in open_questions(s):
        o = find_offer(s, q["offerta"])
        todo.append(f"- DOMANDA ({label(o) if o else q['offerta']}): {q['testo']}")
    for o in s["offerte"]:
        stato, nota, _ = offer_view(s, o)
        if stato == "da_approvare":
            todo.append(f"- DA APPROVARE ({label(o)}): {nota}")
    L += ["## Da fare per te", *(todo or ["- niente"]), ""]
    if s["hint"]:
        L += ["## Direzioni attive (valgono finche' non le togli, solo dove indicato)"]
        for h in s["hint"]:
            L.append(f"- [{hint_label(s, h['ambito'])}] {h['testo']}")
        L.append("")
    L += ["## Offerte", ""]
    if not s["offerte"]:
        L.append("(nessuna offerta)")
    for o in s["offerte"]:
        if o["stato"] == "scartata":
            continue
        stato, nota, _ = offer_view(s, o)
        L += [f"### {label(o)}  [{stato}]", f"Link: {o.get('url') or '(testo incollato)'}"]
        meta = " | ".join(x for x in (o.get("sede"), o.get("lingua"), ("pubblicata " + o["pubblicata"]) if o.get("pubblicata") else "") if x)
        if meta:
            L.append(meta)
        if o.get("perche"):
            L.append(f"Fit (scout): {o['perche']}")
        if o.get("gap"):
            L.append(f"Gap principale: {o['gap']}")
        L.append(f"Stato: {nota}")
        if o.get("tag"):
            L.append(f"Consegna: output\\{o['tag']}\\")
        if o.get("controlli"):
            L += ["Controlli automatici:", o["controlli"]]
        qs = [q for q in s["domande"] if q["offerta"] == o["id"]]
        if qs:
            L.append("Domande:")
            for q in qs:
                L.append(f"- [{'x' if q.get('risposta') else ' '}] {q['testo']}" + (f"  ->  {q['risposta']}" if q.get("risposta") else ""))
        if o.get("analisi"):
            L += ["", "Analisi:", o["analisi"].strip()]
        L.append("")
    sc = s["scout"]
    L += ["## Scout", ""]
    if sc.get("ultimo"):
        u = sc["ultimo"]
        L.append(f"Ultimo giro: {u.get('fine') or u.get('inizio')} - {u.get('nota', '')}")
    for c in sc.get("controllate", []):
        L.append(f"- {c.get('name')} | {c.get('result')} | {c.get('note', '')}")
    L += ["", "## Mappa aziende (master locale, nel pannello si modifica)", ""]
    ms = list(s["mappa"].values())
    L.append(f"{len(ms)} aziende: " + ", ".join(f"{p} {sum(1 for c in ms if (c.get('priority') or 'C') == p)}" for p in ("A", "B", "C")))
    for c in sorted(ms, key=lambda x: (x.get("priority") or "C", x.get("name") or "")):
        js = company_jobs(s, c)
        if js or c.get("nuova") or c.get("nota_agente"):
            L.append(f"- {c['name']} [{c.get('priority')}/{c.get('status')}]" + (" NUOVA (proposta da agente)" if c.get("nuova") else "")
                     + (" | lavori: " + "; ".join(f"{j['ruolo'] or j['id']} ({j['stato']})" for j in js) if js else "")
                     + (f" | {c['nota_agente']}" if c.get("nota_agente") else ""))
    L += ["", "## Registro modifiche degli agenti (ultime 40, da rivedere nel pannello)", ""]
    for r in reversed(s["registro"][-40:]):
        L.append(f"- {r['quando'][:16]} [{r['stato']}] {r['chi']}: {r['tipo']} {r['oggetto']} {r['campo']} | {str(r['prima'])[:50]} -> {str(r['dopo'])[:80]} | {r['motivo']}")
    CODA_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


# ----------------------------------------------------------------- run lock
def lock_age():
    try:
        return time.time() - RUN_LOCK.stat().st_mtime
    except OSError:
        return None


def runner_busy():
    a = lock_age()
    return a is not None and a < 90


def acquire_run(job_id):
    if runner_busy():
        return False
    STATO.mkdir(parents=True, exist_ok=True)
    RUN_LOCK.write_text(f"{os.getpid()} {job_id}\n", encoding="utf-8")
    return True


def heartbeat():
    try:
        os.utime(RUN_LOCK, None)
    except OSError:
        pass


def release_run():
    try:
        RUN_LOCK.unlink()
    except OSError:
        pass
