"""Risultato 6 (pubblico 3): parcheggi per lasciare l'auto e bus contro auto."""
from datetime import datetime
import json
from collections import Counter
from schede import comune
from schede.comune import date_it, forma_base, migliaia, nome_pulito, num, ora, virgola, voce




# ---------------------------------------------------------------- Risultato 6

def r6_file():
    """File unico della mappa (script 79, dati dello script 84); si calcola ogni volta perche' le prove cambiano comune.PROC."""
    return comune.PROC / "risultato6_v2" / "mappa_r6.json"




R6_TONO_AREA = {"Critica": "rosso", "Scarsa": "arancio", "Buona": "verde"}




def scheda_r6():
    """Risultato 6 corretto: legge mappa_r6.json (script 79 <- 84). Prima la scoperta misurata
    sugli interscambi del Comune, poi dove mancano posti prima di entrare in città, poi la verifica."""
    r = json.loads(r6_file().read_text(encoding="utf-8"))
    rie, punti, profili = r["riepilogo"], r["punti_prioritari"], r.get("profili", [])
    par = r.get("parametri", {})
    giorni = date_it(rie["giorni_feriali_validi"])
    n_fermate = rie["fermate_importanti"]
    n_senza = rie["fermate_senza_posti_bastanti"]
    val = rie.get("validazione", [])
    uff = {v["nome"]: v for v in val}
    raggio = int(par.get("raggio_piedi_m", 400))
    quota_txt = virgola(100 * rie["quota_mattino"])
    reg = rie["regola_fermate"]                      # N e M dallo script 83, via 84
    n_corse, m_auto = reg["n_corse"], migliaia(reg["m_auto"])
    regola_txt = (f"fuori dal centro, con metro, stazione o capolinea oppure almeno {n_corse} corse all'ora nelle ore dei "
                  f"pendolari, e con almeno {m_auto} auto in entrata che passano accanto")
    sens_file = r6_file().parent / "confronto_sensori.json"
    sens5t = json.loads(sens_file.read_text(encoding="utf-8")) if sens_file.exists() else None
    tre_punti = ", ".join(f"{p['ordine']}. {nome_pulito(p['nome'])} ({p['zona_nome']})" for p in punti[:3])

    def frase_uff(nome):
        v = uff.get(nome)
        if not v:
            return None
        if v["stato"] == "non_misurato":
            return f"{nome_pulito(nome)} non trasmette il riempimento"
        return f"{nome_pulito(nome)}: {v['descrizione']}"

    scoperta = "; ".join(x for x in (frase_uff(n) for n in ("STURA", "CAIO MARIO", "SOFIA", "VENCHI UNICA", "FERMI")) if x)
    prof_uff = [p for p in profili if p.get("tipo") == "interscambio_ufficiale"]
    pieni = sum(1 for v in val if v["stato"] == "pieno")
    return {
        "risultato": "6",
        "titolo": "Parcheggi per lasciare l'auto",
        "tag": "STIMATO / MISURATO (dati scarsi)",
        "stato": "Aggiornato al " + datetime.now().strftime("%d/%m/%Y"),
        "in_breve": "Dove lasciare l'auto prima di entrare in città e proseguire con i mezzi pubblici: come funzionano "
                    "gli interscambi che ci sono, e dove mancano posti per le auto che entrano ogni mattina.",
        "domanda": "Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, "
                   "per le auto che ogni mattina entrano a Torino?",
        "numero_chiave": {"valore": n_senza, "unita": "fermate",
                          "testo": f"su {n_fermate} fermate importanti fuori dal centro non hanno abbastanza posti adatti "
                                   f"entro {raggio} m a piedi per le auto in entrata che passano accanto"},
        "risposta": [
            f"Gli interscambi che ci sono: nei giorni misurati {scoperta} [MISURATO, DATI SCARSI]. "
            f"Pieni di giorno: {pieni} su {len(val)}.",
            f"Ogni mattina entrano a Torino circa {migliaia(int(round(rie['M_cint'], -2)))} auto [STIMATO, indagine sugli spostamenti 2022]; "
            f"oggi il {quota_txt}% di chi arriva in auto prosegue con un mezzo pubblico.",
            f"Delle {migliaia(n_fermate)} fermate importanti fuori dal centro, {migliaia(n_senza)} non hanno abbastanza "
            f"posti adatti entro {raggio} m a piedi per le auto da fermare ({migliaia(rie['fermate_nessun_parcheggio'])} "
            f"non ne hanno nessuno).",
            f"I punti dove servirebbe di più un parcheggio (posti che mancano, ordine di grandezza): {tre_punti}.",
        ],
        "grafici": [
            {"tipo": "profilo",
             "titolo": f"{nome_pulito(p['nome'])} ({migliaia(p['posti'])} posti): {p['descrizione']}",
             "unita": "", "nota": f"[MISURATO] {p['giorni_validi']} giorni validi; linea piena feriale, tratteggiata weekend [DATI SCARSI].",
             "serie": [{"label": "giorno feriale", "valori": p["profilo_feriale"]}]
                      + ([{"label": "weekend", "valori": p["profilo_weekend"], "tratteggio": True}] if p.get("profilo_weekend") else [])}
            for p in prof_uff[:4]
        ] + [
            {"tipo": "pila", "titolo": "Fermate importanti e posti adatti", "unita": "fermate",
             "nota": f"Posti adatti entro {raggio} m a piedi confrontati con le auto da fermare (auto che passano × {quota_txt}%).",
             "voci": [voce("nessun parcheggio", rie["fermate_nessun_parcheggio"], tono="rosso"),
                      voce("posti insufficienti", rie["fermate_insufficienti"], tono="arancio"),
                      voce("posti sufficienti", rie["fermate_sufficienti"], tono="verde"),
                      voce("poche auto da fermare", rie["fermate_poche_auto"])]},
            {"tipo": "barre", "titolo": "I punti dove mancano più posti", "unita": "posti",
             "nota": "Posti che mancano = auto da fermare − posti adatti vicini [STIMATO, ordine di grandezza].",
             "voci": [voce(f"{p['ordine']}. {nome_pulito(p['nome'])}", p["mancano"], tono="rosso") for p in punti[:10]]},
        ],
        "verifica": [{"nome": nome_pulito(v["nome"]),
                      "fatto": (f"{v['descrizione']} [MISURATO]" if v["stato"] != "non_misurato" else "non trasmette il riempimento")
                               + f"; auto in entrata sulla strada accanto: circa {migliaia(v['auto_passaggio_txt'])} [STIMATO]",
                      "esito": v["esito"]} for v in val],
        "affidabilita": r.get("affidabilita", []),
        "immagini": [],
        "metodo": [
            f"Fermate importanti: fra i luoghi di fermata della Città metropolitana, quelle {regola_txt} "
            "(centro = i quartieri centrali). Regola fissa; il punteggio (importanza della strada, corse, auto, metro o "
            "stazione, pesi uguali) serve solo per l'ordine.",
            "Auto in entrata che passano accanto: le auto che entrano a Torino al mattino (indagine sugli spostamenti 2022) fatte "
            "«guidare» sul percorso più veloce della rete stradale; si legge la strada più trafficata entro 100 m.",
            f"Auto da fermare = auto che passano × {quota_txt}% (chi già oggi lascia l'auto per un mezzo pubblico).",
            f"Posti adatti: parcheggi aperti fuori dal centro, con almeno 20 posti, non di ospedali, università o centri "
            f"commerciali, entro {raggio} m a piedi (linea d'aria × 1,3); posti dichiarati o stimati con 25 m² a posto.",
            "Punti prioritari (fino a 20, almeno 50 posti mancanti, uno per asse d'ingresso, oltre 3 km dal centro): fermate senza posti bastanti raggruppate entro 1 km, in "
            "ordine di posti che mancano.",
        ],
        "parametri": [["Centro escluso", "i quartieri centrali (fermate e parcheggi)"],
                      ["Fermate importanti", f"metro, stazione o capolinea o almeno {n_corse} corse all'ora, e almeno {m_auto} auto che passano "
                                             f"({migliaia(n_fermate)} su {migliaia(rie['n_eleggibili'])})"],
                      ["Distanza", f"{raggio} m a piedi (linea d'aria × 1,3)"],
                      ["Auto da fermare", f"auto che passano × {quota_txt}%"],
                      ["Posti stimati", "25 m² a posto (±30%)"],
                      ["Giorni feriali di riempimento", giorni]],
        "limiti": [
            "Auto che passano: modello del traffico (percorso più veloce, senza code), stima debole: solo ordine di grandezza. "
            "Le stesse auto passano davanti a più fermate dello stesso corso.",
            f"Riempimento misurato su soli {len(rie['giorni_feriali_validi'])} giorni feriali e solo dove il 5T lo trasmette "
            "[DATI SCARSI]: Fermi e i parcheggi gratuiti non sono misurati.",
            "Quota di chi lascia l'auto: indagine sugli spostamenti 2022, poche interviste.",
            *([f"Controllo con i sensori 5T del mattino: il modello mette le strade d'ingresso in un ordine simile solo in parte "
               f"(ρ = {sens5t['rho_b_senza_fuori_rete']:.2f}".replace(".", ",") + f" su {sens5t['n_b_senza_fuori_rete']} luoghi); "
               "sottostima gli ingressi da nord-ovest."] if sens5t else []),
            "Parcheggi da OpenStreetMap incompleti; posti spesso stimati dalla superficie (±30%).",
            "Distanza a piedi stimata (linea d'aria × 1,3). Treni non considerati.",
        ],
        "criteri": r.get("criteri", []),
        "mappa": {"id": "interscambio", "tema": "Parcheggi per lasciare l'auto",
                  "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."},
        "fonti": ["docs/R6_parcheggi.md", "docs/rapporti/RAPPORTO_R6_PARCHEGGI.txt", "docs/rapporti/RAPPORTO_R6_AUTO_PASSAGGIO.txt",
                  "docs/rapporti/RAPPORTO_R6_FERMATE_IMPORTANTI.txt", "docs/rapporti/RAPPORTO_R6_PARCHEGGI_ADATTI.txt",
                  "scripts/81_auto_di_passaggio.py", "scripts/82_parcheggi_adatti.py", "scripts/83_fermate_importanti.py",
                  "scripts/84_risultato6_parcheggi.py", "data/processed/risultato6_v2/mappa_r6.json"],
        "generato": ora(),
        "avviso": [
            "Come leggere i tag. ",
            "[MISURATO] = misura vera, fatta dai sensori del sistema 5T. [STIMATO] = calcolo nostro su dati veri, non una misura diretta. "
            "[DATI SCARSI] = pochi dati, da prendere con cautela.",
        ],
        "in_english": [
            "Question: where are park-and-ride spaces missing for the cars that enter Turin every morning, next to an "
            "important public transport stop outside the city centre?",
            f"Existing park-and-ride car parks of the City: {sum(1 for v in val if v['stato'] != 'non_misurato')} of "
            f"{len(val)} report their occupancy; full during the day: {pieni} (measured, only a few days of data).",
            f"About {int(round(rie['M_cint'], -2)):,} cars enter Turin every morning (2022 travel survey) and "
            f"{100 * rie['quota_mattino']:.1f}% of these drivers already continue by public transport. "
            f"{n_senza:,} of {n_fermate:,} important stops outside the centre lack enough suitable parking within "
            f"{raggio} m on foot for the cars passing by.",
            f"Important stops: outside the centre, with a metro, train station or terminus or at least {n_corse} departures "
            f"per hour at commuting times, and at least {migliaia(reg['m_auto']).replace('.', ',')} cars entering the city passing by.",
            "Limits: car flows come from a simple traffic model (order of magnitude only); occupancy is measured on "
            "few days and only where the city's 5T system reports it; trains are not included.",
            *([f"Check against the 5T morning sensors: the model ranks the entry roads in a similar order only in part "
               f"(rho = {sens5t['rho_b_senza_fuori_rete']:.2f} over {sens5t['n_b_senza_fuori_rete']} places); "
               "it underestimates the entries from the north-west."] if sens5t else []),
        ],
        "scenari": [{
            "nome": "Oggi",
            "numeri": [
                num("Fermate importanti fuori dal centro", n_fermate, "fermate"),
                num("Senza posti bastanti", n_senza, "fermate"),
                num("Senza nessun parcheggio adatto", rie["fermate_nessun_parcheggio"], "fermate"),
            ],
            "nota": "Stime [STIMATO]: auto dal modello del traffico, posti da OpenStreetMap, Comune e 5T; riempimento da 5T [DATI SCARSI].",
        }],
    }




PIAZZA_CASTELLO = (45.0712, 7.6853)
SOGLIA_BUS = 1.5   # la stessa dello script 94: rapporto massimo perché il bus «convenga»


def giudizio_bus(r_basso, r_alto):
    """La classe dello script 94 (stessa regola) per il rapporto tempo coi mezzi / tempo in auto con i due fattori."""
    if r_alto is not None and r_alto <= SOGLIA_BUS:
        return "il bus conviene"
    if r_basso is not None and r_basso <= SOGLIA_BUS:
        return "dipende dal traffico"
    return "il bus non conviene"


def ore_luogo(od, nome):
    """Le ore del giorno di un luogo per la gara: [{ora, bus, auto_min, auto_max, giudizio}], None se i dati a più ore mancano."""
    if not od:
        return None
    ore = []
    for o in od["ore"]:
        l = next((x for x in o["luoghi"] if x["nome"] == nome), None)
        if l and l["tp_min"] is not None:
            ore.append({"ora": o["label"], "bus": l["tp_min"], "auto_min": l["auto_alto_min"], "auto_max": l["auto_basso_min"],
                        "giudizio": giudizio_bus(l["rapporto_basso"], l["rapporto_alto"])})
    return ore if len(ore) > 1 else None


def frazione(q, max_den=5):
    """La frazione semplice più vicina a q (es. 0,65 -> 2 su 3), con denominatore fino a max_den."""
    return min(((round(q * d), d) for d in range(2, max_den + 1) if round(q * d) > 0), key=lambda x: (abs(x[0] / x[1] - q), x[1]))


def anima_fermate(fermate, punti, n_ok, n_pochi, n_nessun):
    """Animazione della scheda 3: la forma di Torino (assets/torino_contorno.json, stessa proiezione della home) e le fermate importanti
    che compaiono dal centro verso fuori, colorate per posti (0 bastanti, 1 pochi, 2 nessuno); poi i punti prioritari."""
    c = json.loads((comune.RADICE / "assets" / "torino_contorno.json").read_text(encoding="utf-8"))
    xy = lambda lat, lon: (round((lon - c["lon_min"]) * c["k"] * c["scala"]), round((c["lat_max"] - lat) * c["scala"]))
    cx, cy = xy(*PIAZZA_CASTELLO)
    classe = {"Posti sufficienti": 0, "Posti insufficienti": 1, "Nessun parcheggio": 2}
    pts = []
    for f in fermate:
        x, y = xy(f["lat"], f["lon"])
        pts.append([x, y, classe[f["classe"]], round(((x - cx) ** 2 + (y - cy) ** 2) ** .5)])
    prio = [list(xy(*p["centro"])) for p in punti]
    tutti_x = [p[0] for p in pts] + [0, c["larghezza"]]
    tutti_y = [p[1] for p in pts] + [0, c["altezza"]]
    x0, y0 = min(tutti_x) - 40, min(tutti_y) - 40
    return {"tipo": "fermate", "contorno": {"d": c["d"], "vb": [x0, y0, max(tutti_x) + 40 - x0, max(tutti_y) + 40 - y0]},
            "punti": pts, "prioritari": prio,
            "legenda": [{"label": "posti bastanti", "n": n_ok, "tono": "verde"}, {"label": "pochi posti", "n": n_pochi, "tono": "giallo"},
                        {"label": "nessun parcheggio", "n": n_nessun, "tono": "rosso"}],
            "didascalia": "Ogni punto è una fermata importante, in Torino e in cintura; la linea è il confine di Torino. "
                          f"I cerchi neri sono i {len(prio)} punti dove servirebbero di più nuovi posti."}


def forma_r6(s):
    r = json.loads(r6_file().read_text(encoding="utf-8"))
    rie, punti, par = r["riepilogo"], r["punti_prioritari"], r.get("parametri", {})
    n_assi, n_fermate, n_senza = len(punti), rie["fermate_importanti"], rie["fermate_senza_posti_bastanti"]
    raggio = int(par.get("raggio_piedi_m", 400))
    quota = virgola(100 * rie["quota_mattino"])
    reg = rie["regola_fermate"]
    ordinati = sorted(punti, key=lambda p: -p["mancano"])
    terzo = max(1, round(len(ordinati) / 3))
    classi = [("alto", "rosso"), ("medio", "arancio"), ("basso", "giallo")]
    voci = []
    for i, p in enumerate(ordinati):
        nome_cl, tono = classi[min(i // terzo, 2)]
        voci.append({"label": nome_pulito(p["nome"]), "valore": p["mancano"], "tono": tono, "testo": f"bisogno {nome_cl}"})
    principale = {"tipo": "barre", "titolo": f"I {n_assi} punti d'ingresso, per bisogno di parcheggio", "unita": "posti",
                  "nota": "Il bisogno è alto, medio o basso a terzi, in base ai posti che mancano. Le lunghezze sono un ordine di grandezza.",
                  "voci": voci}
    ba = json.loads((comune.PROC / "r6_bus_contro_auto.json").read_text(encoding="utf-8"))
    n_punti_ba = ba["riepilogo"]["n_punti"]
    inter = [l for l in ba["luoghi"] if l["tipo"] == "interscambio"]
    f_ba_lo, f_ba_hi = virgola(ba["parametri"]["fattore_basso"]), virgola(ba["parametri"]["fattore_alto"])
    stati = {"pieno": "pieno di giorno", "a_meta": "a metà", "libero": "con posti liberi", "non_misurato": "non misurato"}
    graf_inter = {"tipo": "barre", "titolo": "I parcheggi di scambio che ci sono già: quanto sono pieni e quanto ci mette il bus al centro", "unita": "minuti",
                  "nota": f"Barra = minuti coi mezzi pubblici fino a Piazza Castello alle 8. A destra quanto è pieno il parcheggio di giorno e il tempo in auto, "
                          f"parcheggio compreso, con due stime del rallentamento ({f_ba_hi} e {f_ba_lo}): il valore vero può stare anche fuori.",
                  "voci": [{"label": nome_pulito(l["nome"]), "valore": round(l["tp_min"]),
                            "testo": f"{stati.get(l.get('stato'), 'non misurato')}; {round(l['tp_min'])} contro {round(l['auto_alto_min'])} o {round(l['auto_basso_min'])} in auto"}
                           for l in inter]}
    # messaggio: minuti di pareggio = minuti per parcheggiare in centro che rendono l'auto lenta quanto il bus (script 94, senza soglie scelte da noi)
    pm = ba["pareggio"]["punti"]
    lo_m, hi_m = round(pm["mediana_basso_min"]), round(pm["mediana_alto_min"])
    forbice_m = f"{lo_m} minuti (stima Google) o {hi_m} (stima sensori)" if hi_m != lo_m else f"{lo_m} minuti"
    pb = sorted((l for l in ba["luoghi"][:n_punti_ba] if l["pareggio_basso_min"] is not None), key=lambda l: l["pareggio_basso_min"])
    pareggio_g = {"tipo": "barre", "titolo": "Minuti per parcheggiare in centro oltre i quali il bus dal punto è veloce quanto l'auto", "unita": "minuti",
                  "nota": "Verso Piazza Castello alle 8. Barra scura = stima con il rallentamento di Google, barra chiara = stima con il rallentamento dei sensori. "
                          "Meno minuti = punto più promettente; 0 = il bus è già più veloce.",
                  "voci": [{"label": nome_pulito(l["nome"]), "valore": round(l["pareggio_basso_min"]), "prima": round(l["pareggio_alto_min"]),
                            "testo": f"{round(l['pareggio_basso_min'])}–{round(l['pareggio_alto_min'])} min"} for l in pb]}
    # gara: un bus e un'auto da ogni punto prioritario e da ogni interscambio verso Piazza Castello (tempi dallo script 94)
    od = comune.ore_del_giorno()   # script 100: gli stessi luoghi alle altre ore (se mancano, la gara resta alle 8)
    luoghi_gara = [{"nome": nome_pulito(l["nome"]), "gruppo": "Punti prioritari" if l["tipo"] == "punto_prioritario" else "Interscambi esistenti",
                    "bus": l["tp_min"], "auto_min": l["auto_alto_min"], "auto_max": l["auto_basso_min"], "giudizio": l["classe_testo"],
                    **({"ore": ore} if (ore := ore_luogo(od, l["nome"])) else {})}
                   for l in ba["luoghi"] if l.get("tp_min") is not None]
    scelto = next((i for i, l in enumerate(luoghi_gara) if l["giudizio"].startswith("dipende")), 0)
    gara_g = {"tipo": "gara", "titolo": ("La gara: bus e auto da un punto a Piazza Castello, alle 8, alle 13, alle 17:30 e alle 21 di un feriale" if od
                         else "La gara: bus e auto da un punto a Piazza Castello, alle 8 di un feriale"),
              "nota": f"Un minuto vero dura un attimo: più la corsa è lunga, più il mezzo arriva tardi. L'auto ha due tempi, parcheggio compreso: "
                      f"{f_ba_hi} (stima con il rallentamento dei sensori) e {f_ba_lo} (stima con quello di Google, auto chiara).",
              "luoghi": luoghi_gara, "scelto": scelto}
    mi = lambda l: f"{round(l['pareggio_basso_min'])} minuti (stima Google) o {round(l['pareggio_alto_min'])} (stima sensori)" if l["pareggio_basso_min"] is not None else "nessun collegamento"
    migliore = pb[0] if pb else None
    if migliore:
        gara_g["nota"] += f" Il punto più promettente è {nome_pulito(migliore['nome'])}: lì bastano {mi(migliore)} persi a parcheggiare in centro."
    # il messaggio (Leo, 23/10): quanto è facile lasciare l'auto vicino a una fermata importante e proseguire coi mezzi
    fermate = r["fermate"]
    conta = Counter(f["classe"] for f in fermate)
    n_nessun, n_pochi, n_ok = conta["Nessun parcheggio"], conta["Posti insufficienti"], conta["Posti sufficienti"]
    a, b = frazione(n_senza / n_fermate)
    primo = ordinati[0]
    return forma_base(
        s,
        f"{a} fermate importanti su {b} non hanno abbastanza posti per lasciare l'auto",
        "Chi arriva in auto da fuori trova dove lasciarla vicino a una fermata importante, per proseguire coi mezzi?",
        {"valore": n_senza, "unita": "",
         "testo": f"fermate importanti su {n_fermate} non hanno posti bastanti a {raggio} metri a piedi"},
        principale,
        [f"{n_nessun} fermate importanti non hanno nessun parcheggio adatto vicino; {n_pochi} ne hanno troppo pochi.",
         f"Servirebbero posti soprattutto in {n_assi} punti d'ingresso: il primo è {nome_pulito(primo['nome'])}, dove ne mancano circa {migliaia(primo['mancano'])}.",
         f"Dal parcheggio il bus batte l'auto solo se in centro si perdono minuti a parcheggiare. Servono più di {forbice_m}."],
        [gara_g, pareggio_g, graf_inter],
        [f"Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure {reg['n_corse']} corse all'ora.",
         "Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.",
         f"Auto da fermare: auto che passano per il {quota}% che già oggi lascia l'auto. Posti: parcheggi adatti entro {raggio} metri.",
         "Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.",
         f"Bus contro auto: minuti coi mezzi verso Piazza Castello alle 8, contro l'auto col parcheggio. Mediana dei {n_punti_ba} punti."],
        [["Fermate importanti", f"{reg['n_corse']} corse all'ora o metro, e {migliaia(reg['m_auto'])} auto che passano"],
         ["Distanza a piedi", f"{raggio} metri"],
         ["Auto da fermare", f"auto che passano × {quota}%"],
         ["Bus contro auto", f"verso Piazza Castello alle 8, auto con fattore {f_ba_hi} (sensori) e {f_ba_lo} (Google)"]],
        ["Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati: quelli che mancano sono un ordine di grandezza.",
         ("I tempi coi mezzi sono solo GTT, senza treni. Il rallentamento dell'auto alle altre ore viene dai sensori. Quello di Google si conosce solo alle 8 ed è stato scalato."
          if od else f"I tempi coi mezzi sono solo GTT, senza treni, e solo al mattino. L'auto ha due stime del rallentamento, {f_ba_hi} e {f_ba_lo}: il valore vero può stare anche fuori."),
         "Il rallentamento di Google è stato misurato su 6 percorsi in uscita dal centro. In entrata l'auto può essere più lenta.",
         "Il costo del parcheggio non è nel calcolo: pesa come minuti in più. Si guarda un solo punto per luogo e una sola destinazione."],
        anima=anima_fermate(fermate, punti, n_ok, n_pochi, n_nessun))

