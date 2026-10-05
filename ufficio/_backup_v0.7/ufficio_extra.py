"""
ufficio_extra.py - parti aggiunte al pannello "Ufficio": cartelle consultabili, impostazioni modificabili dal pannello,
panoramica dei progetti e chat (sola lettura, con limite giornaliero). Solo libreria standard.
Importato da pannello_server.py. Non lancia mai Claude da solo: lo fa solo la chat, quando scrivi un messaggio.
"""
import difflib, json, os, re, shutil, threading, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys  # noqa: E402
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))
import motori  # noqa: E402  l'unico punto da cui passano le chiamate ai modelli + log unico logs\uso.csv (v0.5)
CONFIG_FILE = HERE / "pannello_config.json"
CHAT_FILE = HERE / "chat_stato.json"
CHAT_USO = HERE / "chat_uso.csv"      # vecchio log della chat: dal v0.5 il consumo va in logs\uso.csv (motori.py)
CHAT_LOG = HERE / "chat_log.md"          # tutto quello che si dice in chat e ogni azione/modifica: lo si puo' rileggere con Claude
AZIONI_OK = ("scout", "aggiungi", "approva", "approva_tutte", "scarta", "rifai", "direzione", "pausa", "riprendi",
             "manutenzione", "nuove_aziende", "rispondi", "richiesta_pannello", "modifica_pannello",
             "nuova_task", "approva_task", "attiva_task", "in_cima", "rispondi_agente", "consigli", "revisione")
AZIONI_PROGETTO = ("nuova_task", "approva_task", "attiva_task", "in_cima", "rispondi_agente", "consigli", "revisione", "pausa", "riprendi")
_chat_lock = threading.Lock()
_NOWIN = 0x08000000 if os.name == "nt" else 0   # niente finestre nere quando il pannello gira senza console (pythonw)


def log(txt):
    """Aggiunge una riga al log (sempre in coda, mai riscritto)."""
    try:
        new = not CHAT_LOG.exists()
        with CHAT_LOG.open("a", encoding="utf-8") as f:
            if new:
                f.write("# Log dell'Ufficio\n\nChat, azioni confermate, note e modifiche alle impostazioni. Si aggiunge solo in coda.\n")
            f.write(txt.rstrip() + "\n")
    except Exception:
        pass


def _stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _expand(p):
    return Path(os.path.expanduser(os.path.expandvars(str(p))))


def roots(cfg):
    """Cartelle in piu' che si possono consultare (solo vedere/aprire: nessun agente ci scrive)."""
    out = []
    for p in cfg.get("cartelle_consultabili") or []:
        try:
            out.append(_expand(p).resolve())
        except Exception:
            pass
    return out


def under(cfg, path):
    try:
        p = Path(path).resolve()
    except Exception:
        return None
    for b in roots(cfg):
        if p == b or b in p.parents:
            return p
    return None


# ------------------------------------------------------------------ impostazioni
def _int(v, lo, hi, default):
    try:
        return max(lo, min(hi, int(v)))
    except Exception:
        return default


def _lines(v):
    if isinstance(v, str):
        v = v.splitlines()
    out = []
    for x in v or []:
        x = str(x).strip().strip('"')
        if x and x not in out:
            out.append(x)
    return out[:40]


def public_config(cfg):
    return {"nome": cfg.get("nome", "Ufficio"), "soglia_stop_pct": cfg.get("soglia_stop_pct", 60),
            "contatore_token_100": cfg.get("contatore_token_100", 1000000),
            "chat_limite_giorno": cfg.get("chat_limite_giorno", 20),
            "cartelle_consultabili": cfg.get("cartelle_consultabili") or [],
            "chat_cartelle": cfg.get("chat_cartelle") or [], "modifiche_auto": bool(cfg.get("modifiche_auto")), "motore_predefinito": cfg.get("motore_predefinito") or "claude", "generico_auto": bool(cfg.get("generico_auto")),
            "progetti": cfg.get("progetti") or [],
            "sorgenti": [{"id": s["id"], "nome": s["nome"], "attivo": s.get("attivo", True),
                          "radice": str(s["_base"]), "esiste": s["_base"].exists()} for s in cfg.get("sorgenti", [])]}


def set_config(cfg, body, reload_fn):
    """Cambia solo le chiavi permesse nel file di configurazione e le rende attive subito (senza riavviare)."""
    raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig"))
    if "nome" in body:
        raw["nome"] = (str(body["nome"]).strip() or "Ufficio")[:40]
    if "soglia_stop_pct" in body:
        raw["soglia_stop_pct"] = _int(body["soglia_stop_pct"], 0, 100, 60)
    if "chat_limite_giorno" in body:
        raw["chat_limite_giorno"] = _int(body["chat_limite_giorno"], 1, 200, 20)
    if "contatore_token_100" in body:
        raw["contatore_token_100"] = _int(body["contatore_token_100"], 100000, 20000000, 1000000)
    for k in ("cartelle_consultabili", "chat_cartelle"):
        if k in body:
            raw[k] = _lines(body[k])
    if "progetti" in body:
        pr = []
        for p in (body["progetti"] or [])[:20]:
            nome = str(p.get("nome", "")).strip()[:60]
            if not nome:
                continue
            pr.append({"nome": nome, "cartella": str(p.get("cartella", "")).strip(), "stato": str(p.get("stato", "")).strip()[:80],
                       "idee": _lines(p.get("idee"))[:12]})
        raw["progetti"] = pr
    if "modifiche_auto" in body:
        raw["modifiche_auto"] = bool(body["modifiche_auto"])
    if body.get("motore_predefinito") in motori.MOTORI:
        raw["motore_predefinito"] = body["motore_predefinito"]
    if "generico_auto" in body:
        raw["generico_auto"] = bool(body["generico_auto"])
    if "sorgenti_attive" in body:
        att = body["sorgenti_attive"] or {}
        for s in raw.get("sorgenti", []):
            if s.get("id") in att:
                s["attivo"] = bool(att[s["id"]])
    tmp = CONFIG_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(CONFIG_FILE)
    reload_fn()
    log(f"\n### {_stamp()} · IMPOSTAZIONI modificate: " + ", ".join(sorted(k for k in body if k != "progetti") + (["progetti"] if "progetti" in body else [])))
    return {"ok": True, "msg": "Salvato e gia' attivo."}


# ------------------------------------------------------------------ chat
def _load_chat(cfg):
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        d = json.loads(CHAT_FILE.read_text(encoding="utf-8"))
    except Exception:
        d = {}
    if d.get("data") != today:
        d = {"data": today, "usati": 0, "sbloccati": 0, "storia": d.get("storia", [])[-12:],
             "progetti": {k: v[-12:] for k, v in (d.get("progetti") or {}).items()}}
    d.setdefault("progetti", {})
    return d


def _storia(d, progetto=""):
    """La cronologia della chat generale (progetto vuoto) o di un progetto."""
    if progetto:
        return d["progetti"].setdefault(progetto, [])
    return d["storia"]


def _save_chat(d):
    CHAT_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _limit(cfg, d):
    return int(cfg.get("chat_limite_giorno", 20)) * (1 + int(d.get("sbloccati", 0)))


def chat_status(cfg, progetto=""):
    d = _load_chat(cfg)
    lim = _limit(cfg, d)
    return {"usati": d["usati"], "limite": lim, "rimasti": max(0, lim - d["usati"]),
            "storia": (d["progetti"].get(progetto, []) if progetto else d["storia"])[-20:],
            "blocco": cfg.get("chat_limite_giorno", 20), "progetto": progetto or ""}


def chat_sblocca(cfg):
    d = _load_chat(cfg)
    d["sbloccati"] = d.get("sbloccati", 0) + 1
    _save_chat(d)
    return {"ok": True, "msg": f"Sbloccati altri {cfg.get('chat_limite_giorno', 20)} messaggi per oggi.", **chat_status(cfg)}


def _find_claude():
    p = shutil.which("claude")
    if p:
        return p
    for c in (Path.home() / ".local" / "bin" / "claude.exe", Path.home() / ".local" / "bin" / "claude"):
        if c.exists():
            return str(c)
    return None


def _prompt_progetto(pj, vista, contesto, cron, testo):
    """Prompt corto della chat di un progetto (niente azioni sulle candidature, niente modifica del pannello)."""
    az = pj.get("azioni") or ()
    if az:
        parte_az = (
            "Per far fare qualcosa al pannello PROPONI un'azione: Leonardo la conferma con un pulsante e solo allora parte. "
            "Alla fine della risposta scrivi, per ogni azione, UNA riga con JSON su una riga, ad esempio:\n"
            '@@AZIONE {"azione":"nuova_task","parametri":{"titolo":"...","cosa":"istruzioni chiare e complete per l\'agente (cosa fare, cosa NON toccare, quando e\' finita)",'
            '"file":"file o cartelle che puo\' toccare, separati da virgola, relativi alla cartella del progetto","grandezza":"piccolo|medio|grande",'
            '"tappa":"numero della tappa del piano o vuoto","per_te":"UNA frase breve su cosa fa la task"},"descrizione":"cosa succede, in una frase"}\n'
            "Azioni possibili: nuova_task{titolo,cosa,file,grandezza,tappa,per_te}, approva_task{id}, attiva_task{id}, in_cima{id}, "
            "rispondi_agente{id,risposta}, consigli{}, revisione{}, pausa{}, riprendi{}. Il progetto e' gia' questo: non serve scriverlo. "
            "Usa solo id che compaiono nello stato qui sotto. Non proporre azioni se Leonardo chiede solo informazioni. ")
    else:
        parte_az = "In questa chat non puoi proporre azioni: rispondi solo a voce e, se serve un'azione, dillo a Leonardo. "
    return (
        "Sei l'assistente del progetto «" + str(pj.get("nome") or "") + "» nell'Ufficio di Leonardo (un pannello con agenti che lavorano sui suoi progetti). "
        "Rispondi in italiano semplice, breve, senza gergo. Puoi LEGGERE file nella cartella del progetto (se hai gli strumenti), ma NON modificare "
        "file e NON eseguire comandi. " + parte_az +
        "Se Leonardo esprime una decisione, una preferenza o una regola da ricordare, aggiungi una riga '@@NOTA testo breve'. "
        "Non inventare: se non sai o non trovi, dillo.\n\n"
        "DOVE STA GUARDANDO LEONARDO ORA: " + (vista or "non noto") + "\n\n"
        "CONTESTO DEL PROGETTO:\n" + (contesto[:16000] or "(non disponibile)") +
        ("\n\nCONVERSAZIONE FINORA:\n" + cron if cron else "") + "\n\nMESSAGGIO DI LEONARDO:\n" + testo)


def chat_send(cfg, testo, contesto="", vista="", default_src="", motore="claude", progetto="", pj=None):
    testo = (testo or "").strip()
    if not testo:
        return {"ok": False, "msg": "Scrivi qualcosa."}
    if len(testo) > 4000:
        return {"ok": False, "msg": "Messaggio troppo lungo (max 4000 caratteri)."}
    if os.environ.get("ANTHROPIC_API_KEY"):
        return {"ok": False, "msg": "ANTHROPIC_API_KEY e' impostata: la chat si rifiuta di partire (userebbe l'API a pagamento)."}
    claude = _find_claude()
    if not claude:
        return {"ok": False, "msg": "Non trovo il programma claude sul PC."}
    if not _chat_lock.acquire(blocking=False):
        return {"ok": False, "msg": "Sto ancora rispondendo al messaggio precedente."}
    try:
        d = _load_chat(cfg)
        if d["usati"] >= _limit(cfg, d):
            return {"ok": False, "msg": "Limite di oggi raggiunto. Se vuoi continuare, premi «Sblocca altri messaggi».", **chat_status(cfg)}
        dirs = [str(_expand(p)) for p in (cfg.get("chat_cartelle") or []) if _expand(p).exists()]
        storia = _storia(d, progetto)
        if progetto and pj:      # chat di un progetto: cartella del progetto leggibile (solo Claude), prompt corto
            if pj.get("cartella") and Path(pj["cartella"]).exists():
                dirs.append(pj["cartella"])
        cron = "\n".join(("Leonardo: " if m["r"] == "u" else "Tu: ") + m["t"][:1200] for m in storia[-6:])
        if progetto and pj:
            prompt = _prompt_progetto(pj, vista, contesto, cron, testo)
        else:
          prompt = (
            "Sei l'assistente dell'Ufficio di Leonardo: un pannello con agenti che lavorano sui suoi progetti. "
            "Rispondi in italiano semplice, breve, senza gergo. Puoi LEGGERE file nelle cartelle permesse, ma NON modificare "
            "file e NON eseguire comandi. Per far fare qualcosa al pannello PROPONI un'azione: Leonardo la conferma con un "
            "pulsante e solo allora viene eseguita. Per ogni azione scrivi, alla fine della risposta, UNA riga cosi' (JSON su una riga):\n"
            '@@AZIONE {"azione":"scout","sorgente":"' + (default_src or "cv") + '","parametri":{},"descrizione":"cosa succede, in una frase"}\n'
            "Azioni possibili (parametri): scout{}, aggiungi{url,nota}, approva{id}, approva_tutte{}, scarta{id}, rifai{id,fase:cv|lettera}, "
            "direzione{testo,ambito:tutti|scout|cv|lettera}, pausa{}, riprendi{}, manutenzione{}, nuove_aziende{}, rispondi{domanda,risposta}, richiesta_pannello{testo}. "
            "Per i progetti diversi dalle candidature (Langue, Timelive, Preventivi...): nuova_task{progetto: id del PROGETTO, titolo, cosa: istruzioni chiare e complete per l'agente, "
            "file: file/cartelle che puo' toccare separati da virgola (relativi alla cartella del progetto), grandezza: piccolo|medio|grande, tappa: numero della tappa del piano o vuoto, "
            "per_te: UNA frase breve in italiano per Leonardo su cosa fa la task (la legge per approvarla)}, "
            "approva_task{id}, attiva_task{id}, in_cima{id}, rispondi_agente{id,risposta}, consigli{progetto}, revisione{progetto}. Quando Leonardo descrive una task, scrivila tu in modo preciso "
            "(cosa fare, cosa NON toccare, quando e' finita) e proponila con nuova_task: parte solo dopo la sua conferma. "
            "Puoi far modificare il pannello (pagina, pulsanti, server): se Leonardo chiede un cambio, rispondi in una frase cosa farai e scrivi UNA riga @@AZIONE con azione modifica_pannello e parametri {testo: la modifica precisa e completa}. "
            "Non serve la sua conferma per prepararla: viene fatta su una copia e lui la applica o la scarta dopo aver visto cosa cambia. Non dire che non puoi. "
            "Per le offerte hai nello stato id, titolo, sede e LINK: usali quando ti chiede il link. "
            "Usa solo id che compaiono nello stato qui sotto. Non proporre azioni se Leonardo chiede solo informazioni. "
            "Se Leonardo esprime una decisione, una preferenza o una regola da ricordare, aggiungi una riga '@@NOTA testo breve' "
            "(finisce nel log che rilegge con Claude). Non inventare: se non sai o non trovi, dillo. "
            "Non ripetere dati personali (telefono, indirizzo) se non servono.\n\n"
            "DOVE STA GUARDANDO LEONARDO ORA: " + (vista or "non noto") + "\n\n"
            "STATO ATTUALE:\n" + (contesto[:6000] or "(non disponibile)") +
            ("\n\nCONVERSAZIONE FINORA:\n" + cron if cron else "") + "\n\nMESSAGGIO DI LEONARDO:\n" + testo)
        if motore in ("auto", "gratis", "openrouter"):      # modelli via OpenRouter: non leggono file, rispondono con lo stato qui sopra
            r = motori.chiama(prompt, HERE.parent, chi="pannello", progetto=progetto or "", task="chat", fase="chat", motore=motore, timeout=240)
        else:
          r = motori.chiama(prompt, HERE.parent, chi="pannello", progetto=progetto or "", task="chat", fase="chat", modello="sonnet", turni=6, effort="low",
                          strumenti="Read,Glob,Grep", cartelle_extra=dirs, stdin=False, timeout=240)
        if r.timeout:
            return {"ok": False, "msg": "Claude ci ha messo troppo (4 minuti): messaggio non conteggiato."}
        out = (r.stdout or "").strip()
        try:
            j = json.loads(out)
        except Exception:
            low = (out + (r.stderr or "")).lower()
            if "limit" in low:
                return {"ok": False, "msg": "Sembra che il limite d'uso di Claude sia raggiunto. Riprova piu' tardi."}
            return {"ok": False, "msg": "Risposta non leggibile: " + ((r.stderr or out)[:300] or "nessun output")}
        ris = (j.get("result") or "").strip()
        if j.get("is_error") or not ris:
            low = json.dumps(j).lower()
            if "limit" in low:
                return {"ok": False, "msg": "Sembra che il limite d'uso di Claude sia raggiunto. Riprova piu' tardi."}
            ris = ris or "(nessuna risposta: " + str(j.get("subtype", "errore")) + ")"
        azioni, note = [], []
        for line in ris.splitlines():
            m = re.match(r"\s*@@AZIONE\s+(\{.*\})\s*$", line)
            n = re.match(r"\s*@@NOTA\s+(.+)$", line)
            if m:
                try:
                    a = json.loads(m.group(1))
                    ok_az = (pj.get("azioni") or ()) if (progetto and pj) else AZIONI_OK
                    if a.get("azione") in ok_az and len(azioni) < 4:
                        par = a.get("parametri") if isinstance(a.get("parametri"), dict) else {}
                        if progetto and a["azione"] in ("nuova_task", "consigli", "revisione"):
                            par["progetto"] = progetto          # nella chat di un progetto la task e' sempre di quel progetto
                        azioni.append({"id": "a%d%d" % (int(time.time()), len(azioni)), "azione": a["azione"],
                                       "sorgente": str(a.get("sorgente") or default_src),
                                       "parametri": par,
                                       "descrizione": str(a.get("descrizione") or a["azione"])[:300], "stato": "in attesa"})
                except Exception:
                    pass
            elif n:
                note.append(n.group(1).strip()[:400])
        avvia = None
        for a in list(azioni):
            if a["azione"] == "modifica_pannello":
                azioni.remove(a)
                avvia = str(a["parametri"].get("testo") or "").strip()[:2000] or None
        ris = "\n".join(l for l in ris.splitlines() if not re.match(r"\s*@@(AZIONE|NOTA)\b", l)).strip() or "(fatto)"
        d["usati"] += 1
        storia += [{"r": "u", "t": testo}, {"r": "a", "t": ris, "azioni": azioni}]
        storia[:] = storia[-24:]
        _save_chat(d)
        log(f"\n### {_stamp()} · {('chat progetto ' + progetto + ' · ') if progetto else ''}vista: {vista or '-'}\n**Leonardo:** {testo}\n\n**Ufficio:** {ris}")
        for a in azioni:
            log(f"- AZIONE proposta [{a['id']}] {a['azione']} {json.dumps(a['parametri'], ensure_ascii=False)}: {a['descrizione']}")
        for n in note:
            log(f"- NOTA: {n}")
        return {"ok": True, "risposta": ris, "avvia_modifica": avvia, **chat_status(cfg, progetto)}
    finally:
        _chat_lock.release()


def chat_azione(cfg, body, executor):
    """Conferma (o annulla) un'azione proposta dalla chat. Solo azioni dell'elenco, solo dopo il clic di Leonardo."""
    aid, ok = str(body.get("id", "")), bool(body.get("conferma"))
    with _chat_lock:
        d = _load_chat(cfg)
        pj = str(body.get("progetto") or "")
        for m in _storia(d, pj):
            for a in m.get("azioni") or []:
                if a["id"] != aid:
                    continue
                if a["stato"] != "in attesa":
                    return {"ok": False, "msg": "Azione gia' gestita."}
                if ok and any(b["stato"] == "non riuscita" for b in (m.get("azioni") or [])):
                    return {"ok": False, "msg": "Un'azione precedente di questo messaggio NON e' riuscita: non eseguo le altre. Chiedimi di riproporle."}
                if not ok:
                    a["stato"] = "annullata"
                    _save_chat(d)
                    log(f"- AZIONE [{aid}] ANNULLATA da Leonardo ({_stamp()})")
                    return {"ok": True, "msg": "Annullata.", **chat_status(cfg, pj)}
                if a["azione"] not in AZIONI_OK:
                    return {"ok": False, "msg": "Azione non permessa."}
                try:
                    res = executor(a)
                except Exception as e:
                    res = {"ok": False, "msg": f"Errore: {e}"}
                a["stato"] = "fatto" if res.get("ok") else "non riuscita"
                a["esito"] = str(res.get("msg", ""))[:300]
                _save_chat(d)
                log(f"- AZIONE [{aid}] CONFERMATA da Leonardo ({_stamp()}) -> {a['stato']}: {a['esito']}")
                return {"ok": bool(res.get("ok")), "msg": a["esito"], **chat_status(cfg, pj)}
    return {"ok": False, "msg": "Azione non trovata (e' passato troppo tempo?)."}


FEEDBACK = HERE / "feedback.json"


def feedback_list():
    try:
        return json.loads(FEEDBACK.read_text(encoding="utf-8"))[-30:][::-1]
    except Exception:
        return []


def feedback_add(e):
    """Motivi di rifiuto: restano qui e nel log. Se diventano regola, la regola e' marcata [AUTO ...] tra le direzioni."""
    try:
        lst = json.loads(FEEDBACK.read_text(encoding="utf-8"))
    except Exception:
        lst = []
    lst.append(e)
    FEEDBACK.write_text(json.dumps(lst[-200:], ensure_ascii=False, indent=1), encoding="utf-8")
    log(f"- RIFIUTO {e['quando']} · {e['azione']} · {e['titolo'] or e['id']} · motivi: {', '.join(e['tag']) or '-'} · note: {e['motivo'] or '-'}"
        + (" · diventato REGOLA [AUTO] tra le direzioni" if e.get("regola") else ""))


# ------------------------------------------------------------------ modifiche al pannello fatte dalla chat
BOZZA = HERE / "_bozza"
BACKUP = HERE / "_backup"            # UNA sola copia di sicurezza: lo stato prima dell'ultima modifica applicata
MODS = HERE / "modifiche_pannello.md"
EDIT_FILES = ["ufficio.html", "ufficio_dati.py", "mondo.html", "mondo.js", "pannello_server.py", "ufficio_extra.py", "pannello_config.json"]


def _read(p):
    try:
        return Path(p).read_bytes()
    except Exception:
        return None


def _changed(root):
    out = []
    for n in EDIT_FILES:
        a, b = _read(HERE / n), _read(Path(root) / n)
        if b is not None and a != b:
            out.append(n)
    return out


def _diff(root, files, limit=250):
    lines = []
    for n in files:
        a = (_read(HERE / n) or b"").decode("utf-8", "replace").splitlines()
        b = (_read(Path(root) / n) or b"").decode("utf-8", "replace").splitlines()
        lines += list(difflib.unified_diff(a, b, "prima/" + n, "dopo/" + n, lineterm="", n=2))
    plus = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
    return "\n".join(lines[:limit]) + ("\n... (diff accorciato)" if len(lines) > limit else ""), plus, minus


def _validate(root, files):
    """Controlli minimi prima di applicare. Non provano che la pagina funzioni: per quello c'e' il backup."""
    for n in files:
        raw = _read(Path(root) / n)
        if raw is None:
            return f"{n}: file mancante"
        txt = raw.decode("utf-8", "replace")
        if n.endswith(".py"):
            try:
                compile(txt, n, "exec")
            except SyntaxError as e:
                return f"{n}: errore di sintassi alla riga {e.lineno}: {e.msg}"
        elif n.endswith(".json"):
            try:
                json.loads(txt.lstrip("\ufeff"))
            except Exception as e:
                return f"{n}: JSON non valido ({e})"
        elif n.endswith(".html"):
            if "</html>" not in txt or txt.count("<script") != txt.count("</script>"):
                return f"{n}: struttura HTML incompleta"
        if len(raw) < 200:
            return f"{n}: file quasi vuoto"
    return None


def edit_prepare(cfg, testo, reload_fn=None):
    testo = (testo or "").strip()
    if not testo:
        return {"ok": False, "msg": "Manca il testo della modifica."}
    claude = _find_claude()
    if not claude or os.environ.get("ANTHROPIC_API_KEY"):
        return {"ok": False, "msg": "Claude non disponibile (o ANTHROPIC_API_KEY impostata)."}
    if not _chat_lock.acquire(blocking=False):
        return {"ok": False, "msg": "Sto ancora lavorando al messaggio precedente."}
    try:
        d = _load_chat(cfg)
        if d["usati"] >= _limit(cfg, d):
            return {"ok": False, "msg": "Limite di messaggi di oggi raggiunto.", **chat_status(cfg)}
        if BOZZA.exists():
            shutil.rmtree(BOZZA, ignore_errors=True)
        BOZZA.mkdir()
        for n in EDIT_FILES:
            if (HERE / n).exists():
                shutil.copy2(HERE / n, BOZZA / n)
        prompt = ("Sei lo sviluppatore del pannello 'Ufficio' di Leonardo (Python standard + HTML/JS in un file). "
                  "In questa cartella ci sono COPIE dei file del pannello: ufficio.html (la PAGINA PRINCIPALE nuova: quasi sempre e' questa da cambiare), "
                  "ufficio_dati.py (dati e azioni della pagina nuova), pannello_server.py (server), ufficio_extra.py (chat), pannello_config.json, "
                  "mondo.html + mondo.js (il Mondo: la mappa illustrata con gli edifici dei progetti, vista a parte). Leggi solo i file che servono. "
                  "Stile della pagina: poco testo, poche righe, niente pannelli o pulsanti in piu' se non servono. "
                  "Fai questa modifica, cambiando il minimo necessario e senza rompere il resto:\n\n" + testo +
                  "\n\nRegole: modifica solo i file che esistono qui, non creare file nuovi, mantieni lo stile del codice, niente dati personali. "
                  "Se cambi un .py controlla la sintassi leggendo con attenzione. Alla fine rispondi con 1-3 frasi in italiano semplice: cosa hai cambiato e dove lo vedra' Leonardo.")
        r = motori.chiama(prompt, BOZZA, chi="pannello", task="modifica", fase="modifica", modello="sonnet", turni=30, effort="medium",
                          strumenti="Read,Glob,Grep,Edit,Write", modifica=True, stdin=False, timeout=900)
        if r.timeout:
            shutil.rmtree(BOZZA, ignore_errors=True)
            return {"ok": False, "msg": "Troppo tempo (15 minuti): non ho cambiato niente."}
        try:
            j = json.loads((r.stdout or "").strip())
        except Exception:
            shutil.rmtree(BOZZA, ignore_errors=True)
            low = ((r.stdout or "") + (r.stderr or "")).lower()
            return {"ok": False, "msg": "Limite d'uso di Claude raggiunto, riprova piu' tardi." if "limit" in low else "Risposta non leggibile: " + (r.stderr or "")[:300]}
        riassunto = (j.get("result") or "").strip() or "(nessun commento)"
        files = _changed(BOZZA)
        d["usati"] += 1
        if not files:
            shutil.rmtree(BOZZA, ignore_errors=True)
            d["storia"] += [{"r": "a", "t": "Non ho cambiato nessun file. " + riassunto}]
            _save_chat(d)
            log(f"\n### {_stamp()} · MODIFICA PANNELLO richiesta ma nessun file cambiato: {testo}")
            return {"ok": True, "msg": "Nessuna modifica.", **chat_status(cfg)}
        errore = _validate(BOZZA, files)
        diff, plus, minus = _diff(BOZZA, files)
        mid = "m%d" % int(time.time())
        pend = {"id": mid, "testo": testo, "riassunto": riassunto, "files": files, "plus": plus, "minus": minus,
                "diff": diff, "errore": errore, "stato": "in attesa", "quando": _stamp()}
        (BOZZA / "_pending.json").write_text(json.dumps(pend, ensure_ascii=False), encoding="utf-8")
        mod = {k: pend[k] for k in ("id", "files", "plus", "minus", "errore", "stato")}
        d["storia"] += [{"r": "a", "t": riassunto, "modifica": mod}]
        d["storia"] = d["storia"][-24:]
        _save_chat(d)
        log(f"\n### {_stamp()} · MODIFICA PANNELLO preparata [{mid}]\n**Richiesta:** {testo}\n- file: {', '.join(files)} (+{plus} -{minus})" + (f"\n- NON applicabile: {errore}" if errore else ""))
        return {"ok": True, "msg": "Modifica pronta.", "id": mid, "auto": bool(cfg.get("modifiche_auto")) and not errore, **chat_status(cfg)}
    finally:
        _chat_lock.release()


def _pending(mid):
    try:
        p = json.loads((BOZZA / "_pending.json").read_text(encoding="utf-8"))
    except Exception:
        return None
    return p if p.get("id") == mid else None


def edit_diff(mid):
    p = _pending(mid)
    return {"diff": p["diff"], "files": p["files"], "riassunto": p["riassunto"], "errore": p.get("errore")} if p else {"diff": "(non piu' disponibile)", "files": []}


def _set_state(cfg, mid, stato):
    d = _load_chat(cfg)
    for m in d["storia"]:
        if (m.get("modifica") or {}).get("id") == mid:
            m["modifica"]["stato"] = stato
    _save_chat(d)


def edit_apply(cfg, mid, reload_fn=None):
    with _chat_lock:
        p = _pending(mid)
        if not p or p.get("stato") != "in attesa":
            return {"ok": False, "msg": "Modifica non piu' disponibile."}
        err = _validate(BOZZA, p["files"])
        if err:
            return {"ok": False, "msg": "Non applico: " + err}
        if BACKUP.exists():
            shutil.rmtree(BACKUP, ignore_errors=True)
        BACKUP.mkdir()
        for n in p["files"]:
            if (HERE / n).exists():
                shutil.copy2(HERE / n, BACKUP / n)
        (BACKUP / "_info.json").write_text(json.dumps({"quando": _stamp(), "id": mid, "testo": p["testo"], "files": p["files"]}, ensure_ascii=False), encoding="utf-8")
        for n in p["files"]:
            shutil.copy2(BOZZA / n, HERE / n)
        shutil.rmtree(BOZZA, ignore_errors=True)
        _set_state(cfg, mid, "applicata")
        try:
            new = not MODS.exists()
            with MODS.open("a", encoding="utf-8") as f:
                if new:
                    f.write("# Modifiche al pannello fatte dalla chat\n\nUna voce per modifica applicata: richiesta, file, differenze. Le piu' vecchie vengono potate da sole.\n")
                f.write(f"\n## {_stamp()} · [{mid}] {p['testo']}\n**Cosa e' stato fatto:** {p['riassunto']}\n**File:** {', '.join(p['files'])} (+{p['plus']} -{p['minus']})\n```diff\n{p['diff']}\n```\n")
        except Exception:
            pass
        log(f"- MODIFICA [{mid}] APPLICATA da Leonardo ({_stamp()}): {', '.join(p['files'])}; copia di sicurezza in _backup")
        if reload_fn and "pannello_config.json" in p["files"]:
            reload_fn()
        riavvio = any(n.endswith(".py") for n in p["files"])
        return {"ok": True, "riavvio": riavvio, "msg": ("Applicata. Hai cambiato file del programma: premi Menu > Riavvia Ufficio (si riapre da solo)." if riavvio else "Applicata. Premi F5 per vederla.")}


def edit_discard(cfg, mid):
    with _chat_lock:
        if _pending(mid):
            shutil.rmtree(BOZZA, ignore_errors=True)
        _set_state(cfg, mid, "scartata")
        log(f"- MODIFICA [{mid}] SCARTATA da Leonardo ({_stamp()})")
    return {"ok": True, "msg": "Scartata: non e' cambiato niente."}


def restore_backup(reload_fn=None):
    """Rimette i file com'erano prima dell'ultima modifica applicata."""
    try:
        info = json.loads((BACKUP / "_info.json").read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "msg": "Non c'e' nessuna copia di sicurezza."}
    for n in info["files"]:
        if (BACKUP / n).exists():
            shutil.copy2(BACKUP / n, HERE / n)
    log(f"- MODIFICA [{info['id']}] ANNULLATA: ripristinati {', '.join(info['files'])} ({_stamp()})")
    if reload_fn:
        reload_fn()
    return {"ok": True, "msg": "Ripristinato com'era prima di: " + info["testo"][:80] + (". Riapri run.bat se avevi cambiato il programma, poi F5." if any(n.endswith(".py") for n in info["files"]) else ". Premi F5.")}


def pulizia():
    """Toglie il vecchio: bozze rimaste, log molto lunghi, modifiche passate vecchie."""
    fatto = []
    try:
        if BOZZA.exists():
            shutil.rmtree(BOZZA, ignore_errors=True)
            fatto.append("bozza")
        for f, righe in ((CHAT_LOG, 1500), (CHAT_USO, 2000)):
            if f.exists():
                L = f.read_text(encoding="utf-8", errors="replace").splitlines()
                if len(L) > righe:
                    keep = (L[:1] if f == CHAT_USO else L[:3]) + L[-righe:]
                    f.write_text("\n".join(keep) + "\n", encoding="utf-8")
                    fatto.append(f.name)
        if MODS.exists():
            t = MODS.read_text(encoding="utf-8", errors="replace")
            parts = re.split(r"(?m)^(?=## )", t)
            if len(parts) > 26:
                MODS.write_text(parts[0] + "".join(parts[-25:]), encoding="utf-8")
                fatto.append(MODS.name)
    except Exception:
        pass
    return {"ok": True, "msg": "Pulito: " + (", ".join(fatto) if fatto else "niente da togliere.")}
