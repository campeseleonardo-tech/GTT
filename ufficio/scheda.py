r"""
scheda.py - la SCHEDA PROGETTO: un solo documento centrale per progetto (impostazioni, regole, stato). 04/10/2026.

- Dove sta: progetti\<id>.json -> "scheda" (es. Timelive: Desktop\Timelive\timelive.md, gia' esistente),
  altrimenti <cartella>\PROGETTO.md (creata la prima volta), oppure MEMORIA_PROGETTO.md se esiste gia'.
- La parte sopra la riga "STATO DELL'UFFICIO" e' di Leo (la leggono anche gli agenti) e non viene mai toccata.
- La parte tra i due segni <!-- STATO DELL'UFFICIO --> la riscrive l'Ufficio dopo ogni task (0 token):
  piano, fatto, decisioni di Leo, domande aperte, task consigliate, ultima revisione, cose da rivedere.
- Consigli (pulsante): un agente Sonnet legge la scheda e gli ultimi rapporti e propone task / domande / "rivedi la scheda".
- Revisione critica (pulsante): un agente Opus guarda tutto da capo, con occhi diversi.
"""
import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROG = ROOT / "progetti"
GEN = ROOT / "generico"
DIARIO = ROOT / "diario.jsonl"
DOMANDE = ROOT / "domande.jsonl"
MARK_A = "<!-- STATO DELL'UFFICIO: inizio. Questa parte la riscrive l'Ufficio dopo ogni task: non scrivere qui, scrivi sopra. -->"
MARK_B = "<!-- STATO DELL'UFFICIO: fine -->"
CARTELLE = ("queue", "blocked", "incomplete", "failed", "done", "sospesi", "scartate")


def jload(p, d):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))
    except Exception:
        return d


def jsave(p, data):
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(p)


def progetto(pid):
    return jload(PROG / f"{pid}.json", None)


def percorso(p):
    """Il file della scheda (anche se non esiste ancora). None per progetti senza cartella o con documenti propri (candidature)."""
    if not p or p.get("tipo") == "candidature":
        return None
    if p.get("scheda"):
        return Path(p["scheda"])
    if not p.get("cartella"):
        return None
    c = Path(p["cartella"])
    for n in ("PROGETTO.md", "MEMORIA_PROGETTO.md"):
        if (c / n).exists():
            return c / n
    return c / "PROGETTO.md"


def _parse_task(path):
    text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    head, _, body = text.partition("\n---")
    meta = {}
    for raw in head.splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#") and ":" in raw:
            k, v = raw.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    meta["body"] = body.lstrip("-").strip()
    meta.setdefault("id", Path(path).name.replace(".task.md", ""))
    return meta


def _tasks(pid):
    out = {}
    for c in CARTELLE:
        for f in sorted((GEN / c).glob("*.task.md")) if (GEN / c).exists() else []:
            try:
                t = _parse_task(f)
            except Exception:
                continue
            if (t.get("project") or "").lower() == pid and t["id"] not in out:
                out[t["id"]] = dict(t, _cart=c, _path=f)
    return out


def _righe(path):
    try:
        return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]
    except Exception:
        return []


def _profilo_testo(p):
    if p.get("profilo") and (GEN / p["profilo"]).exists():
        return (GEN / p["profilo"]).read_text(encoding="utf-8", errors="replace").strip()
    return ""


def crea_se_manca(p):
    f = percorso(p)
    if not f or f.exists() or not f.parent.exists():
        return f
    regole = _profilo_testo(p) or "(nessuna regola ancora: scrivile qui, le leggono tutti gli agenti del progetto)"
    f.write_text(
        f"# Scheda progetto: {p.get('nome', p['id'])}\n\n"
        "Documento centrale del progetto: impostazioni, regole e stato. Tutto quello che sta SOPRA la riga "
        "\"STATO DELL'UFFICIO\" e' tuo: lo leggono anche gli agenti a ogni task. La parte sotto la aggiorna l'Ufficio da solo.\n\n"
        f"## Obiettivo\n{p.get('obiettivo') or '(da scrivere)'}\n\n"
        "## Per chi e contesto\n(da scrivere: per chi e', cosa conta di piu', cosa evitare)\n\n"
        f"## Regole per gli agenti\n{regole}\n\n"
        "## Note e direzioni di Leo\n(da scrivere)\n\n" + MARK_A + "\n" + MARK_B + "\n", encoding="utf-8")
    return f


def regole_per_agenti(p):
    """Testo che il runner passa agli agenti: la scheda (parte di Leo + stato) e, se la scheda non ha regole, il profilo."""
    f = percorso(p)
    txt = ""
    if f and f.exists():
        txt = f.read_text(encoding="utf-8", errors="replace")
    out = ""
    if txt:
        out += "PROJECT SHEET (Leo's central document for this project; the part below STATO DELL'UFFICIO is generated):\n" + txt[:9000] + "\n"
    m = re.search(r"##\s*Regole per gli agenti\s*\n(.*?)(\n##\s|\Z|" + re.escape(MARK_A) + ")", txt, re.S)
    if not (m and len(m.group(1).strip()) > 40 and "nessuna regola ancora" not in m.group(1)):
        prof = _profilo_testo(p)
        if prof:
            out += "PROJECT PROFILE:\n" + prof + "\n"
    return out


# ------------------------------------------------------------------ blocco automatico
def _blocco(p):
    pid = p["id"]
    ts = _tasks(pid)
    L = [f"## Stato dell'Ufficio (aggiornato {datetime.now():%d/%m/%Y %H:%M})", ""]
    L.append("### Piano")
    for tp in p.get("piano") or []:
        ids = tp.get("task") or []
        st = tp.get("stato")
        if not st:
            sts = [ts[i]["_cart"] for i in ids if i in ts]
            st = "fatto" if ids and len(sts) == len(ids) and all(x == "done" for x in sts) else ("in corso" if any(x == "done" for x in sts) else "da fare")
        L.append(f"- [{'x' if st == 'fatto' else ' '}] {tp.get('testo', '')} ({st.replace('_', ' ')}){' - ' + ', '.join(ids) if ids else ''}")
    if not p.get("piano"):
        L.append("- (nessuna tappa: da decidere)")
    fatti = [x for x in _righe(DIARIO) if x.get("progetto") == pid][-12:]
    L += ["", "### Fatto di recente"]
    L += [f"- {x.get('quando', '')} · {x.get('task', '')}: {x.get('frase', '')}" for x in reversed(fatti)] or ["- (niente ancora)"]
    dec = (p.get("decisioni") or [])[-20:]
    L += ["", "### Decisioni di Leo (risposte alle domande)"]
    L += [f"- {d.get('domanda')} -> **{d.get('risposta')}**" for d in dec] or ["- (nessuna)"]
    conf = (p.get("decisioni_agenti_ok") or [])[-15:]
    if conf:
        L += ["", "### Scelte degli agenti che la revisione considera gia' a posto"]
        L += [f"- {d}" for d in conf]
    aperte = [d for d in _righe(DOMANDE) if d.get("progetto") == pid and d.get("stato") == "aperta"]
    chiuse = sum(1 for d in aperte if len(d.get("opzioni") or []) >= 2)
    L += ["", f"### Domande aperte: {len(aperte)} ({chiuse} a risposta chiusa)"]
    L += [f"- {d['domanda']} ({' / '.join(d.get('opzioni') or [])}; scelta provvisoria: {d.get('scelta') or '-'})" for d in aperte[:12]]
    da_riv = p.get("da_rivedere") or []
    if da_riv:
        L += ["", "### Da completare in questa scheda (segnalato dai consigli o dalla revisione)"]
        L += [f"- {x.get('testo')}" for x in da_riv if not x.get("fatto")]
    cons = [t for t in ts.values() if t.get("proposta")]
    if cons:
        L += ["", "### Task consigliate"]
        st_txt = {"queue": "da approvare/in coda", "done": "fatte", "scartate": "scartata", "sospesi": "spenta"}
        L += [f"- {t['id']}: {t.get('per_te') or t.get('title')} ({st_txt.get(t['_cart'], t['_cart'])})" for t in list(cons)[-8:]]
    rev = p.get("revisione")
    if rev:
        L += ["", f"### Ultima revisione critica: {rev.get('quando')} -> {rev.get('file')}"]
    return "\n".join(L)


def aggiorna(pid):
    p = progetto(pid)
    if not p or p.get("stato") == "archiviato":
        return None
    f = crea_se_manca(p)
    if not f or not f.exists():
        return None
    txt = f.read_text(encoding="utf-8", errors="replace")
    blocco = MARK_A + "\n" + _blocco(p) + "\n" + MARK_B
    if MARK_A in txt and MARK_B in txt:
        a, b = txt.index(MARK_A), txt.index(MARK_B) + len(MARK_B)
        old = txt[a:b]
        if re.sub(r"aggiornato [^)]*\)", "", old) == re.sub(r"aggiornato [^)]*\)", "", blocco):
            return f
        new = txt[:a] + blocco + txt[b:]
    else:
        new = txt.rstrip() + "\n\n" + blocco + "\n"
    f.write_text(new, encoding="utf-8")
    return f


# ------------------------------------------------------------------ consigli e revisione: creazione task
def _prossimo(pref, tipo):
    n = 1
    while any((GEN / c / f"{pref}-{tipo}{n}.task.md").exists() for c in CARTELLE):
        n += 1
    return f"{pref}-{tipo}{n}"


def _gia_in_coda(pid, tipo):
    return any(t.get("tipo") == tipo and t["_cart"] == "queue" for t in _tasks(pid).values())


def crea_speciale(pid, tipo):
    """tipo = 'consigli' o 'revisione'. Crea la task in cima alla coda (parte appena l'agente e' libero)."""
    p = progetto(pid)
    if not p:
        return {"ok": False, "msg": "Progetto non trovato."}
    if _gia_in_coda(pid, tipo):
        return {"ok": False, "msg": "Ce n'e' gia' una in coda per questo progetto."}
    f = crea_se_manca(p)
    pref = p.get("prefisso") or p.get("sigla") or pid[:2].upper()
    tid = _prossimo(pref, "consigli" if tipo == "consigli" else "revisione")
    cart = Path(p.get("cartella") or "")
    git = (cart / ".git").exists()
    out = f"agenti/{tid}/" if git else "./outputs/"
    nome_out = "CONSIGLI.md" if tipo == "consigli" else "REVISIONE.md"
    lines = [f"id: {tid}", f"title: {'consigli di task' if tipo == 'consigli' else 'revisione critica'} ({p.get('nome')})",
             f"project: {pid}", f"tipo: {tipo}", "tier: medium", "priority: 0", f"data_level: {p.get('livello_dati', 0)}",
             "per_te: " + ("Legge la scheda e gli ultimi lavori e propone le prossime task e domande" if tipo == "consigli"
                           else "Guarda tutto da capo con occhi diversi: punti critici, scelte degli agenti, contesto mancante"),
             f"origine: pulsante {datetime.now():%Y-%m-%d %H:%M}"]
    if tipo == "revisione":
        lines += ["model: opus", "effort: high", "max_turns: 60", "timeout: 2700"]
    else:
        lines += ["max_turns: 25"]
    if git:
        lines += [f"repo: {cart}", f"branch: {tid}", f"allowed: [agenti/{tid}/{nome_out}]", f"checks: [files_exist:agenti/{tid}/{nome_out}]"]
    else:
        ins = [str(f)] if f and f.exists() else []
        if ins:
            lines.append("inputs: [" + ", ".join(ins) + "]")
    scheda_txt = f"the project sheet {f.name if f else '(missing)'}" + ("" if git else " (copied in ./inputs/)")
    if tipo == "consigli":
        body = f"""You are the ADVISOR of this project. Read {scheda_txt} (goal, rules, Leo's decisions and directions, plan, what is done, open questions){', agenti/LOG.md and the RAPPORTO.md of the last 3 tasks in agenti/' if git else ''}. Read code or data files only if really needed and only small parts.
Write {out}{nome_out} in ITALIAN, with ONLY these blocks:

## TASK: <short title>
per_te: <one plain Italian sentence for Leo: what it does and why it matters for the goal>
grandezza: piccolo | medio | grande
file: <paths the agent may create or change, comma separated, relative to the project folder>
tappa: <the plan step it belongs to, or empty>
istruzioni:
<complete instructions for the agent who will do it: what to do, what NOT to touch, when it is finished>

## DOMANDA: <short question for Leo> | opzioni: A / B / C | consiglio: B

## RIVEDI SCHEDA: <what exactly is missing in the project sheet to decide well>

Rules: at most 5 TASK and 6 DOMANDA. Each task must move the project toward its goal, follow Leo's decisions and directions and the project rules (protected files!), must not repeat work already done, and must be small enough for one agent session. Prefer closed questions (2-4 options). If the context is not enough to propose good tasks, or everything useful has been done, write NO tasks and use RIVEDI SCHEDA lines (+ questions) saying concretely what is missing. Do not write DOMANDE.md. Do not change any other file."""
    else:
        body = f"""You are an INDEPENDENT CRITICAL REVIEWER of this project, with fresh eyes. Do NOT assume that the plan, the previous advice or the agents' choices were right: re-derive everything from the goal and from the actual files.
Read {scheda_txt}{', agenti/LOG.md, every agenti/*/RAPPORTO.md, RUNNER.md and VALIDATORE.md, and look at the files the tasks produced (small parts of large files)' if git else ''}.
Write {out}{nome_out} in ITALIAN, plain language for Leo (not a programmer), with these sections:
1. In due righe: a che punto siamo rispetto all'obiettivo.
2. Punti critici (errori, rischi, incoerenze tra file, lavoro che non serve all'obiettivo, qualita' dei contenuti). Concreti, con file o record.
3. Contesto mancante: cosa non sappiamo e limita la qualita' del lavoro.
4. Cosa farei diversamente da come si e' ragionato finora.
5. Le 3 prossime cose piu' utili.
Then, at the end, one line for EACH decision an agent took on its own (from reports, 'Scelte', provisional answers):
## DECISIONE AGENTE: <the decision> | task: <id> | serve leo: si/no | opzioni: A / B | scelta attuale: A
(serve leo = si only if Leo's input really matters; no if it is clearly fine or already implicitly confirmed.)
And one line per missing context item:
## CONTESTO MANCANTE: <what is missing in the project sheet>
Do not change any other file. Be honest: "unknown" beats an invented certainty."""
    (GEN / "queue").mkdir(exist_ok=True)
    (GEN / "queue" / f"{tid}.task.md").write_text("\n".join(lines) + "\n---\n" + body + "\n", encoding="utf-8")
    rot = jload(ROOT / "rotazione.json", {})
    rot["in_cima"] = [tid] + [x for x in rot.get("in_cima", []) if x != tid]
    jsave(ROOT / "rotazione.json", rot)
    return {"ok": True, "id": tid, "msg": ("Consigli" if tipo == "consigli" else "Revisione critica") + " in cima alla coda: parte appena l'agente e' libero."}


# ------------------------------------------------------------------ dopo la task: leggere i risultati
def _output(t, nome):
    tid = t["id"]
    cands = []
    if t.get("repo"):
        cands.append(Path(t["repo"]) / "agenti" / tid / nome)
    cands += [GEN / "results" / tid / "outputs" / nome, GEN / "results" / tid / nome]
    return next((c for c in cands if c.exists()), None)


def _nuova_proposta(p, titolo, per_te, gr, files, tappa, istr, origine):
    pref = p.get("prefisso") or p.get("sigla") or p["id"][:2].upper()
    mx = 0
    for c in CARTELLE:
        for f in (GEN / c).glob("*.task.md") if (GEN / c).exists() else []:
            m = re.match(re.escape(pref) + r"(\d+)", f.name)
            if m:
                mx = max(mx, int(m.group(1)))
    sl = re.sub(r"[^a-z0-9]+", "-", titolo.lower()).strip("-")[:24] or "task"
    tid = f"{pref}{mx + 1:02d}-{sl}"
    tier = {"piccolo": "small", "medio": "medium", "grande": "large"}.get(gr.strip().lower(), "medium")
    cart = Path(p.get("cartella") or "")
    files = [x.strip().replace("\\", "/") for x in files.split(",") if x.strip()]
    lines = [f"id: {tid}", f"title: {titolo[:90]}", f"project: {p['id']}", f"tier: {tier}", "priority: 2",
             f"data_level: {p.get('livello_dati', 0)}", f"per_te: {' '.join(per_te.split())[:220]}", f"proposta: {origine}",
             "approval_before: leo", "approved: no"]
    if p.get("profilo"):
        lines.append(f"profile: {p['profilo']}")
    if (cart / ".git").exists():
        lines += [f"repo: {cart}", f"branch: {tid}"]
        if files:
            lines.append("allowed: [" + ", ".join(files) + "]")
            fl = [f for f in files if "." in Path(f).name]
            if fl:
                lines.append("checks: [files_exist:" + ";".join(fl) + "]")
    else:
        ins = [str(cart / f) for f in files if (cart / f).is_file()]
        if ins:
            lines.append("inputs: [" + ", ".join(ins) + "]")
    (GEN / "queue" / f"{tid}.task.md").write_text("\n".join(lines) + "\n---\n" + istr.strip() + "\n", encoding="utf-8")
    if tappa.strip():
        for tp in p.get("piano") or []:
            if tp.get("testo", "").strip().lower() == tappa.strip().lower():
                tp.setdefault("task", []).append(tid)
    return tid


def _aggiungi_domanda(pid, tid, i, testo, opzioni, scelta, dove=""):
    with open(DOMANDE, "a", encoding="utf-8") as out:
        out.write(json.dumps({"id": f"{tid}#{i}", "progetto": pid, "task": tid, "domanda": testo.strip()[:200],
                              "opzioni": [o.strip() for o in opzioni.split("/") if o.strip()][:5], "scelta": scelta.strip()[:120],
                              "dove": dove[:200], "quando": datetime.now().strftime("%Y-%m-%d %H:%M"), "stato": "aperta"}, ensure_ascii=False) + "\n")


def dopo_task(tid):
    """Chiamata dal dispatcher dopo ogni task generica. Gestisce consigli/revisione e aggiorna la scheda. Torna un testo per il diario."""
    t = None
    for c in CARTELLE:
        f = GEN / c / f"{tid}.task.md"
        if f.exists():
            t = _parse_task(f)
            break
    if not t:
        return ""
    pid = (t.get("project") or "").lower()
    p = progetto(pid)
    if not p:
        return ""
    nota = ""
    if t.get("tipo") == "consigli":
        f = _output(t, "CONSIGLI.md")
        if f:
            txt = f.read_text(encoding="utf-8", errors="replace")
            nt = nd = 0
            for blk in re.split(r"\n(?=##\s)", "\n" + txt):
                blk = blk.strip()
                m = re.match(r"##\s*TASK:\s*(.+)", blk)
                if m and nt < 5:
                    g = lambda k: (re.search(rf"^{k}\s*:\s*(.*)$", blk, re.M | re.I) or [None, ""])[1]
                    istr = blk.split("istruzioni:", 1)[1] if "istruzioni:" in blk else blk
                    _nuova_proposta(p, m.group(1).strip(), g("per_te") or m.group(1), g("grandezza") or "medio", g("file"), g("tappa"), istr, tid)
                    nt += 1
                m = re.match(r"##\s*DOMANDA:\s*(.+?)\|\s*opzioni\s*:\s*(.*?)(?:\|\s*consiglio\s*:\s*(.*))?$", blk, re.I)
                if m and nd < 6:
                    _aggiungi_domanda(pid, tid, nd, m.group(1), m.group(2), m.group(3) or "")
                    nd += 1
                m = re.match(r"##\s*RIVEDI SCHEDA:\s*(.+)", blk, re.I)
                if m:
                    p.setdefault("da_rivedere", []).append({"testo": m.group(1).strip()[:300], "quando": datetime.now().strftime("%Y-%m-%d"), "da": tid})
            jsave(PROG / f"{pid}.json", p)
            nota = f"{nt} task consigliate (in Da approvare), {nd} domande" + (", la scheda va completata" if p.get("da_rivedere") else "")
    elif t.get("tipo") == "revisione":
        f = _output(t, "REVISIONE.md")
        if f:
            txt = f.read_text(encoding="utf-8", errors="replace")
            ns = nn = 0
            for i, line in enumerate(txt.splitlines()):
                m = re.match(r"\s*##\s*DECISIONE AGENTE:\s*(.+?)\|\s*task\s*:\s*(.*?)\|\s*serve leo\s*:\s*(si|sì|no)\s*(?:\|\s*opzioni\s*:\s*(.*?))?(?:\|\s*scelta attuale\s*:\s*(.*))?$", line, re.I)
                if m:
                    if m.group(3).lower().startswith("s") and m.group(4):
                        _aggiungi_domanda(pid, m.group(2).strip() or tid, f"{tid}-{i}", "Confermi? " + m.group(1).strip(), m.group(4), m.group(5) or "")
                        ns += 1
                    else:
                        p.setdefault("decisioni_agenti_ok", []).append(m.group(1).strip()[:200] + f" ({m.group(2).strip()})")
                        nn += 1
                m = re.match(r"\s*##\s*CONTESTO MANCANTE:\s*(.+)", line, re.I)
                if m:
                    p.setdefault("da_rivedere", []).append({"testo": m.group(1).strip()[:300], "quando": datetime.now().strftime("%Y-%m-%d"), "da": tid})
            p["revisione"] = {"quando": datetime.now().strftime("%d/%m/%Y %H:%M"), "file": str(f)}
            jsave(PROG / f"{pid}.json", p)
            nota = f"revisione pronta: {ns} scelte degli agenti da confermare, {nn} considerate a posto"
    try:
        aggiorna(pid)
    except Exception:
        pass
    return nota
