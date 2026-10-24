"""Risultato 6 (pubblico 3): parcheggi per lasciare l'auto e bus contro auto."""
from datetime import datetime
import json
from collections import Counter
from schede import comune
from schede.comune import circa, date_it, forma_base, migliaia, nome_pulito, num, ora, periodo_it, virgola, voce




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
VICINO_SOGLIA = (1.35, 1.65)   # L9: «vicino alla soglia» = ±10% attorno a 1,5 (regola fissata prima dei numeri)


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
                  "nota": "Barra = minuti coi mezzi pubblici fino a Piazza Castello alle 8. A destra il tempo in auto, parcheggio compreso (TomTom), e quanto è pieno il parcheggio di giorno.",
                  "voci": [{"label": nome_pulito(l["nome"]), "valore": round(l["tp_min"]),
                            "testo": f"{round(l['tp_min'])} contro {round(l['auto_basso_min'])} in auto · {stati.get(l.get('stato'), 'non misurato')}"}
                           for l in inter]}
    # minuti di pareggio = minuti per parcheggiare in centro che rendono l'auto lenta quanto il bus (script 94): una frase del calcolo, non piu' un grafico
    pm = ba["pareggio"]["punti"]
    lo_m, hi_m = round(pm["mediana_basso_min"]), round(pm["mediana_alto_min"])
    n_conv_p = sum(1 for l in ba["luoghi"][:n_punti_ba] if l["classe"] == "conviene")
    # gara: un bus e un'auto da ogni punto prioritario e da ogni interscambio verso Piazza Castello, alle 8 (tempi dello script 94, auto TomTom)
    luoghi_gara = [{"nome": nome_pulito(l["nome"]), "gruppo": "Punti prioritari" if l["tipo"] == "punto_prioritario" else "Interscambi esistenti",
                    "bus": l["tp_min"], "auto_min": l["auto_basso_min"], "auto_max": l["auto_basso_min"], "giudizio": l["classe_testo"]}
                   for l in ba["luoghi"] if l.get("tp_min") is not None]
    gara_g = {"tipo": "gara", "titolo": "La gara: bus e auto verso Piazza Castello, alle 8 di un feriale",
              "nota": "Bus e auto partono insieme da ogni parcheggio, uno dopo l'altro. L'auto ha il tempo previsto da TomTom, parcheggio compreso.",
              "luoghi": luoghi_gara, "scelto": 0}
    # il messaggio (Leo, 23/10): quanto è facile lasciare l'auto vicino a una fermata importante e proseguire coi mezzi
    fermate = r["fermate"]
    conta = Counter(f["classe"] for f in fermate)
    n_nessun, n_pochi, n_ok = conta["Nessun parcheggio"], conta["Posti insufficienti"], conta["Posti sufficienti"]
    a, b = frazione(n_senza / n_fermate)
    primo = ordinati[0]
    # L9: dei punti dove il bus conviene (rapporto TomTom <= 1,5), quanti sono vicini alla soglia (fra 1,35 e 1,65)
    conv_punti = [l for l in ba["luoghi"][:n_punti_ba] if l["classe"] == "conviene"]
    vicini = [l for l in conv_punti if VICINO_SOGLIA[0] <= l["rapporto_basso"] <= VICINO_SOGLIA[1]]
    # L9: sensibilita' alla quota di chi lascia l'auto (porte.json, script 84): meta' e doppio
    sq = json.loads((comune.PROC / "risultato6_v2" / "porte.json").read_text(encoding="utf-8"))["sensibilita"]["quota"]
    senza_q = [sq[k]["nessun"] + sq[k]["insufficienti"] for k in ("x0.5", "x2")]
    return forma_base(
        s,
        f"{a} fermate importanti su {b} non hanno abbastanza posti per lasciare l'auto",
        "Chi arriva in auto da fuori trova dove lasciarla vicino a una fermata importante, per proseguire coi mezzi?",
        {"valore": n_senza, "unita": "",
         "testo": f"fermate importanti su {n_fermate} non hanno posti bastanti a {raggio} metri a piedi"},
        principale,
        [f"{n_nessun} fermate importanti non hanno nessun parcheggio vicino, {n_pochi} troppo pochi.",
         f"Il primo dei {n_assi} punti d'ingresso dove servono posti è {nome_pulito(primo['nome'])}: ne mancano {circa(primo['mancano'])}.",
         f"In {n_conv_p} punti su {n_punti_ba}, lasciata l'auto, il bus arriva in centro in al più {virgola(SOGLIA_BUS)} volte il tempo dell'auto."],
        [gara_g, graf_inter],
        [f"Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure {reg['n_corse']} corse all'ora.",
         "Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.",
         f"Auto da fermare: auto che passano per il {quota}% che già oggi lascia l'auto. Posti: parcheggi adatti entro {raggio} metri.",
         "Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.",
         "Bus contro auto: minuti coi mezzi verso Piazza Castello alle 8, contro l'auto. Auto: tempo a flusso libero per il fattore TomTom del percorso, più 5 minuti. Dati di traffico: TomTom.",
         f"Pareggio: con {lo_m} minuti persi a parcheggiare in centro, l'auto impiega quanto il bus (mediana dei {n_punti_ba} punti, TomTom).",
         f"Dei punti dove il bus conviene, {len(vicini)} su {len(conv_punti)} sono vicini alla soglia: un'auto il 10% più veloce cambia classe.",
         f"Con la stima dei sensori del traffico, più favorevole all'auto (fattore {f_ba_hi}), il pareggio sale a {hi_m} minuti."],
        [["Fermate importanti", f"{reg['n_corse']} corse all'ora o metro, e {migliaia(reg['m_auto'])} auto che passano"],
         ["Distanza a piedi", f"{raggio} metri"],
         ["Auto da fermare", f"auto che passano × {quota}%"],
         ["Periodo del riempimento dei parcheggi", periodo_it(min(rie["giorni_feriali_validi"]), max(rie["giorni_feriali_validi"]))],
         ["Bus contro auto", f"verso Piazza Castello alle 8; auto: fattore TomTom del percorso (mediana {f_ba_lo}) + 5 minuti; stima più favorevole all'auto: sensori 5T, fattore {f_ba_hi}"]],
        ["Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati: quelli che mancano sono un ordine di grandezza. "
         f"Con metà o doppio di chi lascia l'auto, le fermate senza posti bastanti vanno da {min(senza_q)} a {max(senza_q)} su {n_fermate}.",
         "I tempi coi mezzi sono solo GTT, senza treni. La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto.",
         "Tempi in auto previsti da TomTom su traffico tipico di un feriale di novembre, non misurati in un giorno preciso. Si usa un solo servizio.",
         "Il costo del parcheggio non è nel calcolo: pesa come minuti in più. Si guarda un solo punto per luogo e una sola destinazione."],
        anima=anima_fermate(fermate, punti, n_ok, n_pochi, n_nessun),
        pareggio={"tomtom": lo_m, "sensori": hi_m})   # minuti di pareggio mediani dei punti (la home li legge)

