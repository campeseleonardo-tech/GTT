"""Risultato 8 (pubblico 4): traffico e mezzi pubblici."""
import json
import re
from schede import comune
from schede.comune import forma_base, grafico_per_titolo, leggi, migliaia, nome_pulito, num, ora, virgola, voce




# ---------------------------------------------------------------- Risultato 8

def nome_strada(n):
    """'unita d italia' -> 'Unità d'Italia' (i nomi del modello sono senza maiuscole e accenti)."""
    if n.startswith("di "):
        n = "strada " + n   # es. "di settimo" -> Strada di Settimo
    t = " ".join(w.capitalize() for w in n.split())
    t = re.sub(r" D (?=[A-Z])", " d'", t)
    for a, b in (("Unita ", "Unità "), (" Di ", " di "), (" Del ", " del ")):
        t = t.replace(a, b)
    return t




def scheda_r8():
    r = leggi("risultato8_traffico_tp_v2.json")
    v = leggi("traffico_d/valutazione_fase5.json")
    var = r.get("variante_traffico", "v0")   # il modello scelto dalla regola fissata prima (script 63)
    sens = leggi(f"traffico_d/{var}/sensori.json")["sensori"]
    u, c, tar = r["universo_torino"], r["conteggi"], r["taratura"]
    km_poco = round(u["km"] - u["km_coperti_tp"], 1)
    err = v["varianti"][var]
    # strade con piu' traffico: per nome solo per mostrarle (il calcolo e' per asse e tratta)
    per_nome = {}
    for t in r["tratte"]:
        if not t["asse_con_sensore"]:   # solo strade con un sensore sull'asse: le altre classifiche sono poco credibili
            continue
        k = t["nome"]
        if k not in per_nome or t["veic_giorno"] > per_nome[k]["veic_giorno"]:
            per_nome[k] = t
    top = sorted(per_nome.values(), key=lambda t: -t["veic_giorno"])[:10]
    # stima leave-one-out per ogni sensore (stesso metodo della valutazione: fattore = somma misurati / somma modello degli altri)
    tot_mis, tot_mod = sum(s["misurato"] for s in sens), sum(s["modello_2v"] for s in sens)
    loo = [(s, s["modello_2v"] * (tot_mis - s["misurato"]) / (tot_mod - s["modello_2v"])) for s in sens]
    loo.sort(key=lambda x: -x[0]["misurato"])
    dg = {a["nome_principale"]: a for a in r["assi_da_guardare"]}
    rm = dg.get("regina margherita", {})
    acc = r["accordo_leo"]
    altri_assi = [a for a in r["assi_da_guardare"] if a["nome_principale"] != "regina margherita"]
    altro_tratto = (f" In più un tratto di {nome_strada(altri_assi[0]['nome_principale'])}, coperto solo per "
                    f"{round(100 * altri_assi[0]['copertura_tp_max'])}% della lunghezza.") if altri_assi else ""
    fascia50, fascia90 = round(tar["fascia_50"] * 100), round(tar["fascia_90"] * 100)
    return {
        "risultato": "8",
        "titolo": "Traffico sulle strade e trasporto pubblico",
        "tag": "STIMATO / MISURATO / PROGRAMMATO",
        "stato": "Fatto",
        "in_breve": "Quante auto passano sulle strade grandi di Torino? E dove c'è tanto traffico ma nessun bus, "
                    "tram o metro comodo, così che l'auto resta l'unica scelta?",
        "domanda": "Sulle strade grandi di Torino, dove c'è molto traffico e poco trasporto pubblico vicino?",
        "numero_chiave": {"valore": round(u["quota_km_coperta_tp"] * 100, 1), "unita": "%",
                          "testo": f"dei km di strade grandi di Torino hanno fermate frequenti a pochi passi "
                                   f"({virgola(u['km_coperti_tp'])} km su {virgola(u['km'])})"},
        "racconto": "Un primo calcolo trovava 23 strade \"con molto traffico e poco trasporto pubblico\". "
                    "Ricontrollando, quasi tutte erano un errore di misura: i bus si cercavano lungo la strada per "
                    "nome invece che per posizione delle fermate (Corso Cairoli risultava senza passaggi). Rifatto il "
                    "calcolo, la lista si è quasi svuotata: è questa la risposta.",
        "risposta": [
            f"Sulle {migliaia(u['n_tratte'])} tratte di strade grandi di Torino ({virgola(u['km'])} km), il "
            f"{virgola(u['quota_km_coperta_tp'] * 100)}% della lunghezza ha una fermata con almeno 4 passaggi "
            "all'ora entro 300 m, o la metro entro 600 m.",
            f"Le tratte con molto traffico (oltre {migliaia(round(u['soglie']['q66']))} veicoli al giorno) sono "
            f"{c['molto_traffico']}; quelle che hanno anche poco trasporto pubblico sono {c['da_guardare']}.",
            f"In pratica è un solo caso: Corso Regina Margherita verso ovest, il tratto a scorrimento veloce "
            f"(circa {migliaia(int(round(rm.get('veic_max', 0), -3)))} veicoli al giorno, nessuna fermata frequente "
            "entro 300 m)." + altro_tratto,
            f"I numeri di traffico sono stime: in metà dei casi l'errore è entro ±{fascia50}%. Servono a ordinare "
            "le strade, non a contare i veicoli.",
        ],
        "grafici": [
            {"tipo": "pila", "titolo": "Km di strade grandi di Torino: con o senza trasporto pubblico vicino",
             "unita": "km",
             "voci": [voce("con fermate frequenti vicine", round(u["km_coperti_tp"], 1), tono="verde"),
                      voce("con poco trasporto pubblico", km_poco, tono="rosso")]},
            {"tipo": "barre", "titolo": "Strade con un sensore: la tratta più carica (veicoli al giorno, 6-21)",
             "unita": "veicoli/giorno",
             "nota": "Solo strade con almeno un sensore sullo stesso asse: senza, il modello mette in cima anche strade "
                     "poco credibili. \"misurato\" = sensore sulla tratta; le altre sono stime. Corso Unione Sovietica è "
                     "probabilmente sovrastimato: dove c'è il sensore il modello dava quasi il triplo del misurato.",
             "voci": [voce(nome_strada(t["nome"]) + (" (misurato)" if t["misurato"] else ""), round(t["veic_giorno"]))
                      for t in top]},
            {"tipo": "barre", "titolo": f"Prova del modello sui {len(sens)} sensori: misurato e stimato",
             "unita": "veicoli/giorno",
             "nota": "Barra chiara = misurato dal sensore, barra scura = stima del modello senza usare quel sensore.",
             "voci": [voce(s["via"].replace("(TO)", "").replace("Unita' D'italia", "Unità d'Italia").strip(), round(st), prima=s["misurato"]) for s, st in loo]},
            {"tipo": "barre", "titolo": "Errore della stima su ogni sensore (%)", "unita": "%",
             "nota": "Errore = |stimato − misurato| / misurato. Metà dei sensori sotto il valore tipico, gli altri sopra.",
             "voci": [voce(s["via"].replace("(TO)", "").replace("Unita' D'italia", "Unità d'Italia").strip(),
                           round(100 * abs(st - s["misurato"]) / s["misurato"]), tono="rosso")
                      for s, st in sorted(loo, key=lambda x: abs(x[1] - x[0]["misurato"]) / x[0]["misurato"])]},
        ],
        "metodo": [
            "Domanda: gli spostamenti in auto dell'indagine sugli spostamenti 2022 (residenti, giorno feriale), assegnati alla "
            "strada più veloce sulla rete di OpenStreetMap.",
            f"Taratura su {err['n']} punti di misura dei sensori 5T: un solo fattore per tutta la città, provato "
            "togliendo un sensore alla volta e stimandolo con gli altri.",
            "Strade come assi: un corso che cambia nome o comune resta la stessa strada, tagliata in tratte da "
            "300 m a 1,5 km. Strade grandi = Torino, importanza alta o strade principali, almeno 300 m, senza "
            "tangenziale e raccordi.",
            "Trasporto pubblico per posizione delle fermate, mai per nome: una tratta è servita dove c'è una "
            "fermata con almeno 4 passaggi all'ora entro 300 m (orario ufficiale, mercoledì 14/10), o la metro "
            "entro 600 m. Poco trasporto pubblico = servita per metà della lunghezza o meno.",
            "Molto traffico = il terzo più alto delle tratte. " + (
                "Un modello più ricco (attrazioni, code, ZTL) è stato provato una volta e non ha migliorato l'ordine delle strade: si tiene quello semplice."
                if var == "v0" else
                f"Il modello è quello più ricco (attrazioni, code, ZTL): con i sensori di ottobre sbaglia meno di quello semplice "
                f"(errore tipico {round(100 * err['errore_mediano'])}% contro {round(100 * v['varianti']['v0']['errore_mediano'])}%), secondo una regola fissata prima."),
        ],
        "parametri": [["Strade grandi di Torino", f"{migliaia(u['n_tratte'])} tratte, {virgola(u['km'])} km"],
                      ["Errore tipico (metà dei casi)", f"±{fascia50}% (9 volte su 10 entro ±{fascia90}%)"],
                      ["Ordine giusto delle strade (Spearman)", f"{err['rho_loo']:.2f}".replace(".", ",")],
                      ["Validato tra", f"{migliaia(int(round(tar['intervallo_validato_measured'][0], -2)))} e "
                                       f"{migliaia(int(round(tar['intervallo_validato_measured'][1], -3)))} veicoli/giorno"],
                      ["Soglia 'molto traffico'", f"{migliaia(round(u['soglie']['q66']))} veicoli/giorno"],
                      ["Confronto con chi conosce la città", f"{acc['n_giuste_18']} strade su 18 nella fascia giusta, "
                                                             f"{acc['n_giusti_7']} confronti su 7 (solo controllo)"]],
        "limiti": [
            f"Stima debole: errore tipico ±{fascia50}% e intervallo d'incertezza largo (da {round(err['ic90'][0] * 100)}% "
            f"a {round(err['ic90'][1] * 100)}%). Alcune strade sono molto sbagliate (Corso Unione Sovietica, Corso "
            "Sebastopoli): buona per ordinare, non per contare.",
            f"Solo {err['n']} punti di misura, quasi tutti su corsi trafficati: sotto circa "
            f"{migliaia(int(round(tar['intervallo_validato_measured'][0], -3)))} veicoli al giorno la stima non è "
            "verificata.",
            "Solo i residenti tra 11 e 84 anni (indagine sugli spostamenti): mancano merci, turisti e chi viene da fuori. Il "
            "modello non sa fare le code: l'ora di punta non è verificata.",
            "Trasporto pubblico programmato: niente ritardi né affollamento. Il centro (ZTL, aree pedonali) non è "
            "stimato bene.",
            "Il valore è per i due versi: sulle poche vie a senso unico vero potrebbe essere il doppio del reale.",
            "Il tratto di Corso Moncalieri va controllato a mano: una fermata con 26 passaggi all'ora è a 40 m, "
            "ma copre solo un quarto della tratta.",
        ],
        "in_english": [
            "Question: on Turin's major roads, where is there a lot of traffic and little public transport nearby?",
            f"Of {u['n_tratte']:,} road sections on Turin's major roads ({u['km']:.1f} km), {u['quota_km_coperta_tp'] * 100:.1f}% of the length "
            "has a frequent stop (at least 4 departures an hour) within 300 m, or the metro within 600 m. Heavy-traffic "
            f"sections (over {round(u['soglie']['q66']):,} vehicles a day): {c['molto_traffico']}; of these, "
            f"{c['da_guardare']} also have little public transport.",
            "In practice this is one main case: Corso Regina Margherita westbound, a fast road with no frequent stop "
            "within 300 m, plus one stretch of Corso Moncalieri covered for only a quarter of its length.",
            f"Limits: traffic figures are estimates with a typical error of ±{fascia50}%; use them to rank the roads, not "
            "to count vehicles.",
        ],
        "mappa": None,
        "fonti": ["docs/R8_traffico.md", "docs/rapporti/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt",
                  "data/processed/risultato8_traffico_tp_v2.json"],
        "generato": ora(),
        "avviso": [
            "Dati [STIMATO] (traffico) / [MISURATO] (sensori 5T) / [PROGRAMMATO] (orari GTT)",
            f"Traffico stimato con un modello tarato su {err['n']} sensori: errore tipico ±{fascia50}%. "
            "Trasporto pubblico = fermate con almeno 4 passaggi all'ora entro 300 m o metro entro 600 m."
        ],
        "scenari": [{
            "nome": "Oggi",
            "numeri": [
                num("Km di strade grandi di Torino", round(u["km"], 1), "km"),
                num("Con fermate frequenti vicine", round(u["quota_km_coperta_tp"] * 100, 1), "%"),
                num("Tratte con molto traffico", c["molto_traffico"], "tratte"),
                num("Molto traffico e poco trasporto pubblico", c["da_guardare"], "tratte"),
                num("Errore tipico della stima", fascia50, "%"),
            ],
            "nota": "Le 5 tratte sono quasi tutte su Corso Regina Margherita ovest; una su Corso Moncalieri.",
        }],
    }




def area_tempi_js():
    """Scrive data/area_tempi.js (dati dell'«area che si espande», letti da assets/area.js) dal file dello script 99 e ritorna il grafico della scheda;
    None se il file dello script 99 non c'e' ancora (la scheda esce senza il grafico)."""
    f = comune.PROC / "area_tempi.json"
    if not f.is_file():
        print("AVVISO: data/processed/area_tempi.json non c'e' (script 99): la scheda 4 esce senza l'area che si espande")
        return None
    a = json.loads(f.read_text(encoding="utf-8"))
    if a.get("finto") or a["parametri"].get("prova"):
        print("AVVISO: area_tempi.json e' una prova o ha tempi finti: la scheda 4 esce senza l'area che si espande")
        return None
    p, s, z = a["parametri"], a["sezioni"], a["zone"]
    la0, lo0 = p["origine"]
    dati = {"f": [p["fattore_alto"], p["fattore_basso"]], "soglie": p["soglie"],
            "ox": round((p["punto_coord"][1] - lo0) * p["scala_coordinate"]), "oy": round((p["punto_coord"][0] - la0) * p["scala_coordinate"]),
            "x": s["x"], "y": s["y"], "r": s["res"], "z": s["zona"],
            "c": {"m": a["castello"]["mezzi"], "a": a["castello"]["auto_alto"], "b": a["castello"]["auto_basso"]},
            "zn": [n.replace("Torino, ", "") for n in z["nomi"]], "zm": z["mezzi"], "za": z["auto_alto"], "zb": z["auto_basso"]}
    (comune.RADICE / "data" / "area_tempi.js").write_text(
        "// generato da scripts/schede_risultati.py (dati: scripts/99_area_tempi.py) - non modificare a mano\nwindow.AREA_TEMPI = "
        + json.dumps(dati, separators=(",", ":")) + ";\n", encoding="utf-8")
    q = a["quote_residenti"]
    return {"tipo": "area", "titolo": "L'area che si espande: dove si arriva in 10, 20, 30 e 45 minuti",
            "nota": f"Alle 7:45 di un feriale, da Piazza Castello o da una zona di Torino. Per Piazza Castello ogni quadratino è una sezione di censimento. "
                    f"Da Piazza Castello in 30 minuti si raggiunge il {virgola(q['mezzi']['30'])}% dei torinesi coi mezzi pubblici e il {virgola(q['auto_basso']['30'])}% "
                    f"in auto con la stima di TomTom, parcheggio compreso ({virgola(q['auto_alto']['30'])}% con la stima più favorevole all'auto, dei sensori 5T)."}


def forma_r8(s):
    """Scheda R8: tempo coi mezzi pubblici contro tempo in auto (script 93), come forbice fra due fattori di punta; in coda la copertura delle strade."""
    t = json.loads((comune.PROC / "tp_contro_auto.json").read_text(encoding="utf-8"))
    r = leggi("risultato8_traffico_tp_v2.json")
    u = r["universo_torino"]
    quota_strade = round(u["quota_km_coperta_tp"] * 100, 1)
    par, ti = t["parametri"], t["titolo"]
    ab = t["gruppi"]["ab"]
    lo, hi = ab["limite_basso"], ab["limite_alto"]            # lo = stima TomTom (principale, rapporto piu' basso), hi = sensori 5T (la piu' favorevole all'auto)
    x = virgola(round(ti["mediano_basso"], 1))               # numero grande e titolo: rapporto mediano TomTom alle 8, una cifra decimale (blocco L8)
    f_lo, f_hi = virgola(lo["fattore"]), virgola(hi["fattore"])
    q_lo, q_hi = virgola(round(100 * ti["quota_oltre_2_basso"])), virgola(round(100 * ti["quota_oltre_2_alto"]))
    coppie_ab = [p for p in t["coppie"] if p["gruppo"] in ("a", "b")]
    ordinate = sorted(coppie_ab, key=lambda p: -p["auto"])[:600]
    quota_punti = 100 * sum(p["auto"] for p in ordinate) / max(1, sum(p["auto"] for p in coppie_ab))
    f1, f2, f3 = par["fasce"]
    nomi_fasce = [f"sotto {virgola(f1)}", f"{virgola(f1)}-{virgola(f2)}", f"{virgola(f2)}-{virgola(f3)}", f"oltre {virgola(f3)}"]
    toni = ["verde", "giallo", "arancio", "rosso"]
    principale = {"tipo": "barre_gruppi", "titolo": "Auto del mattino per rapporto fra tempo coi mezzi pubblici e tempo in auto", "unita": "%", "max": 100,
                  "nota": "Rapporto 2 = coi mezzi pubblici si impiega il doppio che in auto. Coppie Torino-Torino e Torino-cintura. "
                          "Stima principale: tempo in auto previsto da TomTom; accanto la stima più favorevole all'auto (sensori 5T).",
                  "gruppi": [{"label": n, "voci": [
                      {"label": "stima TomTom", "valore": round(a["pct"], 1), "tono": tn, "testo": f"{virgola(round(a['pct'], 1))}% ({migliaia(a['auto'])} auto)"},
                      {"label": "stima più favorevole all'auto (sensori 5T)", "valore": round(b["pct"], 1), "tono": tn, "testo": f"{virgola(round(b['pct'], 1))}% ({migliaia(b['auto'])} auto)"}]}
                      for n, a, b, tn in zip(nomi_fasce, lo["fasce"], hi["fasce"], toni)]}
    disp = {"tipo": "dispersione", "titolo": "Tempo in auto e tempo coi mezzi pubblici, una coppia di zone per punto",
            "xlabel": "minuti in auto (ora di punta, stima TomTom)", "ylabel": "minuti coi mezzi pubblici",
            "punti": [[p["auto_punta_basso_min"], p["tp_min"], p["auto"]] for p in ordinate],
            "linee": [{"k": f1, "label": f"{virgola(f1)} volte"}, {"k": f2, "label": "il doppio"}],
            "nota": f"Ogni punto è una coppia di zone, grande quanto le auto del mattino. Sono le {len(ordinate)} coppie con più auto "
                    f"({virgola(quota_punti)}% delle auto). Sopra una linea il mezzo pubblico impiega più di quel multiplo dell'auto."}
    peggiori = t["peggiori"]
    pare = {"tipo": "barre", "titolo": "Le 15 coppie con più auto dove i mezzi pubblici impiegano più del doppio", "unita": "auto",
            "nota": "Auto del mattino su quella coppia (dalle 6 alle 10, giorno feriale), con la stima di TomTom. A destra i minuti coi mezzi contro quelli in auto.",
            "voci": [{"label": f"{p['da_nome']} → {p['a_nome']}", "valore": p["auto"], "tono": "rosso",
                      "testo": f"{migliaia(p['auto'])} auto: {round(p['tp_min'])} contro {round(p['auto_punta_basso_min'])} min"} for p in peggiori]}
    p3 = peggiori[:3]
    conferme = [n for n in t["noti"] if n["google_mezzi_min"]]
    txt_conf = " e ".join(f"{round(n['tp_min'])} contro {n['google_mezzi_min'][0]}-{n['google_mezzi_min'][1]}" for n in conferme)
    strade = grafico_per_titolo(s, "Km di strade grandi")
    extra = {"titolo": "Strade grandi e fermate vicine",
             "punto": f"Il {virgola(quota_strade)}% dei km di strade grandi ha una fermata frequente vicina: la fermata c'è, ma non basta.",
             "grafico": strade}
    # gara (Leo, 23/10; 24/10: sempre alle 8, cambia solo il luogo): viaggi tipici del mattino fra zone, le coppie con più auto, una partenza diversa per corsa
    od = comune.ore_del_giorno()
    nomi_z = {z["zona"]: z["nome"] for z in t["per_zona"]}
    for p in t["peggiori"]:
        nomi_z.setdefault(p["da"], p["da_nome"]); nomi_z.setdefault(p["a"], p["a_nome"])
    corto = lambda c: nome_pulito(nomi_z.get(c, c).replace("Torino, ", ""))
    viste, viaggi = set(), []
    for p in sorted(coppie_ab, key=lambda p: -p["auto"]):
        if p["da"] in viste or p["da"] == p["a"] or p["da"] not in nomi_z or p["a"] not in nomi_z:
            continue
        viste.add(p["da"])
        v = {"nome": corto(p["da"]), "arrivo": corto(p["a"]), "bus": p["tp_min"],
             "auto_min": p["auto_punta_basso_min"], "auto_max": p["auto_punta_basso_min"],       # un'auto sola: TomTom
             "giudizio": f"coi mezzi {virgola(round(p['rapporto_basso'], 1))} volte il tempo dell'auto ({virgola(round(p['rapporto'], 1))} con la stima dei sensori)"}
        viaggi.append(v)
        if len(viaggi) == 6:
            break
    gara = {"tipo": "gara", "titolo": "I viaggi in auto più frequenti del mattino: bus contro auto", "luoghi": viaggi, "scelto": 0,
            "nota": f"I {len(viaggi)} viaggi in auto più frequenti, alle 8 di un feriale, partendo da zone diverse: bus e auto partono insieme."}
    # regola del titolo (fissata prima dei numeri, blocco L3): se a tutte le ore il rapporto mediano resta entro ±0,3 da quello delle 8, con tutti e due i fattori,
    # il titolo dice «a ogni ora del giorno»; altrimenti resta «al mattino» e un punto chiave dice come cambia durante il giorno
    ore_linea, tutto_il_giorno, punto_giorno = None, False, None
    if od:
        o8 = od["ore"][0]["ab"]
        scarto = max(abs(o["ab"]["limite_basso"]["mediano"] - o8["limite_basso"]["mediano"]) for o in od["ore"])      # L8: regola ±0,3 sulla sola stima TomTom
        tutto_il_giorno = scarto <= 0.3 + 1e-9
        bassi, alti = [o["ab"]["limite_basso"]["mediano"] for o in od["ore"]], [o["ab"]["limite_alto"]["mediano"] for o in od["ore"]]
        punto_giorno = (f"Nel giorno il rapporto mediano va da {virgola(round(min(bassi), 1))} a {virgola(round(max(bassi), 1))} (stima TomTom) "
                        f"e da {virgola(round(min(alti), 1))} a {virgola(round(max(alti), 1))} (stima più favorevole all'auto, sensori 5T).")
        ore_linea = {"tipo": "linea", "titolo": "Quante volte il tempo dell'auto, ora per ora", "unita": "volte",
                     "nota": "Rapporto mediano fra tempo coi mezzi e tempo in auto, pesato per le auto del mattino, alle 4 ore del giorno. "
                             "Due linee: stima TomTom (a ogni ora) e stima più favorevole all'auto (sensori 5T).",
                     "categorie": [o["label"] for o in od["ore"]],
                     "serie": [{"label": "stima TomTom", "valori": [round(v, 2) for v in bassi]}, {"label": "sensori 5T, la più favorevole all'auto", "valori": [round(v, 2) for v in alti]}]}
    area = area_tempi_js()
    anima = {"tipo": "area", "didascalia": area["nota"]} if area else None   # l'animazione principale della scheda (e della home): l'area che si espande
    senza_ab = ab["senza_collegamento"]
    par_crit = [["Zone", f"{par['n_zone']} zone dell'indagine sugli spostamenti ({par['n_zone_torino']} di Torino), fino a {par['punti_per_zona']} punti ciascuna"],
                ["Mezzi pubblici", f"partenza {par['partenza']}-8:15 di un feriale, mediana, cammino a {virgola(par['velocita_piedi_kmh'])} km/h, al massimo {par['tempo_max_min']} minuti"],
                ["Auto, stima TomTom", f"tempo a flusso libero × fattore TomTom della coppia (mediana {f_lo}) + {virgola(par['minuti_parcheggio'])} minuti"],
                ["Auto, stima più favorevole all'auto", f"tempo a flusso libero × {f_hi} (sensori 5T, non contano semafori e incroci) + {virgola(par['minuti_parcheggio'])} minuti"],
                ["Fasce del rapporto", f"sotto {virgola(f1)}, {virgola(f1)}-{virgola(f2)}, {virgola(f2)}-{virgola(f3)}, oltre {virgola(f3)}"]]
    return forma_base(
        s,
        (f"A ogni ora del giorno, coi mezzi pubblici si impiega {x} volte il tempo dell'auto" if tutto_il_giorno
         else f"Al mattino, coi mezzi pubblici si impiega {x} volte il tempo dell'auto"),
        "Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno?",
        {"valore": x, "unita": "volte",
         "testo": f"il tempo dell'auto: rapporto mediano con la stima TomTom, pesato per le auto del mattino ({migliaia(ti['auto_collegate'])} auto); con i sensori 5T, la stima più favorevole all'auto, {virgola(round(ti['mediano_alto'], 1))}"},
        principale,
        [f"Con la stima di TomTom il {q_lo}% delle auto ha rapporto oltre 2; con la stima più favorevole all'auto (sensori 5T) il {q_hi}%.",
         (punto_giorno if (punto_giorno and not tutto_il_giorno)
          else "Le 3 coppie peggiori: " + ", ".join(f"{p['da_nome']} → {p['a_nome']}" for p in p3) + "."),
         f"Google conferma i tempi coi mezzi pubblici sui percorsi di controllo: {txt_conf} minuti."],
        ([ore_linea] if ore_linea else []) + [gara, disp, pare],
        ["Le zone sono quelle dell'indagine sugli spostamenti 2022 con punti di calcolo; ognuna ha fino a 5 punti.",
         "Mezzi pubblici: a piedi, bus, tram e metro, con partenza fra le 7:45 e le 8:15. Si prende la mediana.",
         "Auto: tempo a flusso libero per il fattore TomTom della coppia (previsto su traffico tipico), più 5 minuti; le coppie non chieste a TomTom prendono la mediana della loro fascia. Dati di traffico: TomTom.",
         "Rapporto = tempo coi mezzi diviso tempo in auto. Le fasce sono fisse.",
         "Le auto di una coppia sono i viaggi in auto dell'indagine, in partenza dalle 6 alle 10 di un feriale."],
        par_crit,
        ["Fuori Torino mancano treni e altre aziende: le coppie fra comuni della cintura non sono nel numero. Senza i treni metropolitani, dove ci sono, i mezzi pubblici risultano più lenti del vero. L'orario è quello programmato.",
         "La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto.",
         "Tempi in auto previsti da TomTom su traffico tipico di un feriale di novembre, non misurati in un giorno preciso. Usiamo un solo servizio.",
         f"L'indagine è un campione. I viaggi dentro una zona e {migliaia(senza_ab['coppie'])} coppie senza collegamento ({migliaia(senza_ab['auto'])} auto) non sono nel confronto."],
        ["Question: for which trips is the car much faster than public transport, and how many cars make them?",
         f"Answer: in the morning public transport takes {ti['mediano_basso']:.1f} times as long as the car (weighted median, TomTom estimate; {ti['mediano_alto']:.1f} with the 5T sensors, the estimate most favourable to the car). "
         f"For {100 * ti['quota_oltre_2_basso']:.0f}% of cars it takes more than twice as long ({100 * ti['quota_oltre_2_alto']:.0f}% with the sensors).",
         "Limit: car times are forecast by TomTom for typical traffic on a November weekday, not measured on a specific day; we use a single service. "
         "Without metropolitan trains, public transport looks slower than it is."],
        mappa=False, extra=extra, **({"anima": anima} if anima else {}))
