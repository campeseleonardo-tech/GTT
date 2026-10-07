# -*- coding: utf-8 -*-
"""
Consumo dettagliato dell'Ufficio (nuovo, 05/10/2026). Legge SOLO il log unico logs\\uso.csv tramite motori.py.
Risponde a: quali modelli hanno fatto cosa, quante chiamate, quanti token, quanto tempo, quanti errori.
Non scrive niente e non chiama nessun modello.

Una "chiamata" = una riga del log con fase diversa da "esito" (le righe "esito" sono il risultato finale di un task, senza token).
Esiti di una chiamata: ok, errore, scartato (modello inadatto), limite (limite di Claude). Tutto il resto conta come errore.
"""
from datetime import datetime, timedelta

import motori

PERIODI = {"oggi": "Oggi", "24h": "Ultime 24 ore", "7g": "7 giorni", "tutto": "Tutto"}
_OK = ("ok",)


def _int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0


def _flt(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _dal(per):
    now = datetime.now()
    if per == "oggi":
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    if per == "24h":
        return now - timedelta(hours=24)
    if per == "7g":
        return now - timedelta(days=7)
    return None


def _nome_modello(r):
    m = (r.get("modello") or "").strip()
    if not m:
        return "(non registrato)"
    return m.replace(":free", "") if r.get("motore") == "openrouter" else m


def _gruppo(d, chiave, r):
    g = d.setdefault(chiave, {"chiamate": 0, "ok": 0, "errori": 0, "scartate": 0, "tok_in": 0, "tok_out": 0, "secondi": 0.0,
                              "senza_token": 0, "task": set(), "modelli": set()})
    esito = (r.get("esito") or "").lower()
    g["chiamate"] += 1
    if esito in _OK:
        g["ok"] += 1
    elif esito == "scartato":
        g["scartate"] += 1
    else:
        g["errori"] += 1
    ti = _int(r.get("token_input"))
    to = _int(r.get("token_output"))
    g["tok_in"] += ti
    g["tok_out"] += to
    if not ti and not to:
        g["senza_token"] += 1
    g["secondi"] += _flt(r.get("secondi"))
    if r.get("task"):
        g["task"].add(r["task"])
    g["modelli"].add(_nome_modello(r))
    return g


def _chiudi(g, **extra):
    d = dict(g)
    d["task"] = sorted(g["task"]) if isinstance(g.get("task"), set) else g.get("task")
    d["modelli"] = sorted(g["modelli"]) if isinstance(g.get("modelli"), set) else g.get("modelli")
    d["secondi"] = round(g["secondi"])
    d["secondi_medi"] = round(g["secondi"] / g["chiamate"]) if g["chiamate"] else 0
    d["n_task"] = len(g["task"])
    d.update(extra)
    return d


def dettaglio(per="oggi"):
    per = per if per in PERIODI else "oggi"
    righe = motori.righe(dal=_dal(per))
    chiamate = [r for r in righe if (r.get("fase") or "") != "esito"]
    esiti = {}
    for r in righe:
        if (r.get("fase") or "") == "esito" and r.get("task"):
            esiti[r["task"]] = (r.get("esito") or "", r.get("quando") or "")

    tot = {"chiamate": 0, "ok": 0, "errori": 0, "scartate": 0, "tok_in": 0, "tok_out": 0, "secondi": 0.0, "senza_token": 0,
           "task": set(), "modelli": set()}
    per_mod, per_task, per_prog = {}, {}, {}
    for r in chiamate:
        _gruppo({"t": tot}, "t", r)
        mot = (r.get("motore") or "claude")
        m = _gruppo(per_mod, (mot, _nome_modello(r)), r)
        _gruppo(per_prog, r.get("progetto") or ("chat" if r.get("chi") == "pannello" else "(nessuno)"), r)
        if r.get("task") and r.get("chi") != "pannello":
            t = _gruppo(per_task, r["task"], r)
            t.setdefault("progetto", r.get("progetto") or "")
            t.setdefault("passi", []).append({
                "quando": (r.get("quando") or "")[5:16], "fase": r.get("fase") or "", "modello": _nome_modello(r),
                "motore": mot, "esito": r.get("esito") or "", "tok_in": _int(r.get("token_input")),
                "tok_out": _int(r.get("token_output")), "secondi": round(_flt(r.get("secondi")))})

    out_mod = [_chiudi(g, motore=k[0], modello=k[1]) for k, g in per_mod.items()]
    out_mod.sort(key=lambda x: -x["chiamate"])
    out_task = [_chiudi(g, id=k, progetto=g.get("progetto", ""), esito_finale=esiti.get(k, ("", ""))[0],
                        ultimo=(g["passi"][-1]["quando"] if g.get("passi") else "")) for k, g in per_task.items()]
    out_task.sort(key=lambda x: x["ultimo"], reverse=True)
    out_prog = [_chiudi(g, id=k) for k, g in per_prog.items()]
    out_prog.sort(key=lambda x: -(x["tok_in"] + x["tok_out"]))
    totale = _chiudi(tot)
    totale["costo_listino_usd"] = round(sum(motori.costo(r) for r in chiamate if (r.get("motore") or "claude") == "claude"), 2)
    return {"periodo": per, "periodi": PERIODI, "totale": totale, "modelli": out_mod, "task": out_task[:80], "progetti": out_prog,
            "nota": "Token dei modelli gratis non dichiarati dal modello sono stimati (4 caratteri = 1 token) dal 05/10 in poi; "
                    "prima restano vuoti: contati come 'senza token'. Le righe 'esito' (risultato finale della task) non sono chiamate."}
