"""Risultato 6 (pubblico 3): parcheggi per lasciare l'auto e bus contro auto."""
from datetime import datetime
import json
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
    rie, aree, punti, profili = r["riepilogo"], r["aree"], r["punti_prioritari"], r.get("profili", [])
    par = r.get("parametri", {})
    giorni = date_it(rie["giorni_feriali_validi"])
    apc = rie["aree_per_categoria"]
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
    con_cat = [a for a in aree if not a.get("pochi_dati")]
    critiche = sorted([a for a in con_cat if a["categoria"] == "Critica"], key=lambda a: -(a["nessun"] + a["insufficienti"]))
    tre_critiche = "; ".join(" - ".join(a["zone_principali"]) or "area senza nome" for a in critiche[:3]) or "nessuna"

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




def forma_r6(s):
    r = json.loads(r6_file().read_text(encoding="utf-8"))
    rie, punti, par = r["riepilogo"], r["punti_prioritari"], r.get("parametri", {})
    n_assi, n_fermate, n_senza = len(punti), rie["fermate_importanti"], rie["fermate_senza_posti_bastanti"]
    raggio = int(par.get("raggio_piedi_m", 400))
    quota = virgola(100 * rie["quota_mattino"])
    reg = rie["regola_fermate"]
    val = rie.get("validazione", [])
    misurati = [v for v in val if v["stato"] != "non_misurato" and not v["esito"].startswith("non si può dire")]
    pieni = sum(1 for v in val if v["stato"] == "pieno")
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
    graf_inter = {"tipo": "barre", "titolo": "Dagli interscambi esistenti a Piazza Castello, minuti coi mezzi pubblici", "unita": "minuti",
                  "nota": f"Alle 8 di un feriale. A destra il tempo in auto, parcheggio compreso, fra i due fattori di punta ({f_ba_hi} e {f_ba_lo}).",
                  "voci": [{"label": nome_pulito(l["nome"]), "valore": round(l["tp_min"]), "testo": f"{round(l['tp_min'])} contro {round(l['auto_alto_min'])}-{round(l['auto_basso_min'])} in auto"}
                           for l in inter]}
    extra = {"titolo": "Interscambi esistenti e bus verso il centro",
             "punto": f"Gli interscambi esistenti sono poco pieni: di giorno solo {pieni} su {len(val)} è pieno.",
             "grafico": graf_inter}
    # messaggio: minuti di pareggio = minuti per parcheggiare in centro che rendono l'auto lenta quanto il bus (script 94, senza soglie scelte da noi)
    pm = ba["pareggio"]["punti"]
    lo_m, hi_m = round(pm["mediana_basso_min"]), round(pm["mediana_alto_min"])
    forbice_m = f"{lo_m}–{hi_m}" if hi_m != lo_m else f"{lo_m}"
    pb = sorted((l for l in ba["luoghi"][:n_punti_ba] if l["pareggio_basso_min"] is not None), key=lambda l: l["pareggio_basso_min"])
    pareggio_g = {"tipo": "barre", "titolo": "Minuti per parcheggiare in centro oltre i quali il bus dal punto è veloce quanto l'auto", "unita": "minuti",
                  "nota": "Verso Piazza Castello alle 8. Barra scura = auto lenta (fattore di Google), barra chiara = auto veloce (fattore dei sensori). "
                          "Meno minuti = punto più promettente; 0 = il bus è già più veloce.",
                  "voci": [{"label": nome_pulito(l["nome"]), "valore": round(l["pareggio_basso_min"]), "prima": round(l["pareggio_alto_min"]),
                            "testo": f"{round(l['pareggio_basso_min'])}–{round(l['pareggio_alto_min'])} min"} for l in pb]}
    # gara: un bus e un'auto da ogni punto prioritario e da ogni interscambio verso Piazza Castello (tempi dallo script 94)
    luoghi_gara = [{"nome": nome_pulito(l["nome"]), "gruppo": "Punti prioritari" if l["tipo"] == "punto_prioritario" else "Interscambi esistenti",
                    "bus": l["tp_min"], "auto_min": l["auto_alto_min"], "auto_max": l["auto_basso_min"], "giudizio": l["classe_testo"]}
                   for l in ba["luoghi"] if l.get("tp_min") is not None]
    scelto = next((i for i, l in enumerate(luoghi_gara) if l["giudizio"].startswith("dipende")), 0)
    gara_g = {"tipo": "gara", "titolo": "La gara: bus e auto da un punto a Piazza Castello, alle 8 di un feriale",
              "nota": f"Un minuto vero dura un attimo: più la corsa è lunga, più il mezzo arriva tardi. L'auto ha due tempi, parcheggio compreso: "
                      f"{f_ba_hi} (sensori, auto veloce) e {f_ba_lo} (Google, auto chiara e lenta).",
              "luoghi": luoghi_gara, "scelto": scelto}
    mi = lambda l: f"{round(l['pareggio_basso_min'])}–{round(l['pareggio_alto_min'])} minuti" if l["pareggio_basso_min"] is not None else "nessun collegamento"
    pieni_i = [l for l in inter if l["stato"] == "pieno"]
    vuoti_i = [l for l in inter if l["stato"] == "libero"]
    kp1 = ("Interscambi esistenti: pieni " + (", ".join(f"{nome_pulito(l['nome'])} ({mi(l)})" for l in pieni_i) or "nessuno")
           + "; poco usati " + (", ".join(f"{nome_pulito(l['nome'])} ({mi(l)})" for l in vuoti_i) or "nessuno") + ".")
    migliore = pb[0] if pb else None
    kp3 = (f"Il punto più promettente è {nome_pulito(migliore['nome'])}: bastano {mi(migliore)} perché il bus pareggi l'auto."
           if migliore else "Nessun punto ha un collegamento coi mezzi entro 120 minuti.")
    tono_classe = {"conviene": "verde", "dipende": "giallo", "non_conviene": "rosso"}
    pallini = [{"label": nome_pulito(l["nome"]), "tono": tono_classe.get(l["classe"], "grigio")} for l in ba["luoghi"][:n_punti_ba]]
    npc = ba["riepilogo"]["punti"]
    unita = {"tipo": "pallini", "pallini": pallini,
             "didascalia": f"Un pallino per punto prioritario: verde = il bus conviene ({npc['conviene']}), giallo = dipende ({npc['dipende']}), "
                           f"rosso = il bus non conviene ({npc['non_conviene']})."}
    return forma_base(
        s,
        f"Dai parcheggi di scambio il bus vale l'auto solo se in centro si perdono {forbice_m} minuti a parcheggiare",
        "Dove mancano posti per lasciare l'auto, e quando il bus da lì verso il centro è veloce quanto l'auto?",
        {"valore": forbice_m, "unita": "minuti",
         "testo": f"persi in centro per parcheggiare: sotto questa soglia l'auto batte il bus (mediana dei {n_punti_ba} punti)"},
        gara_g,
        [kp1,
         f"{n_senza} fermate importanti su {n_fermate} non hanno posti bastanti a {raggio} metri a piedi.",
         kp3],
        [pareggio_g, principale],
        [f"Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure {reg['n_corse']} corse all'ora.",
         "Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.",
         f"Auto da fermare: auto che passano per il {quota}% che già oggi lascia l'auto. Posti: parcheggi adatti entro {raggio} metri.",
         "Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.",
         "Minuti di pareggio: tempo coi mezzi verso Piazza Castello alle 8, meno il tempo in auto senza parcheggio."],
        [["Fermate importanti", f"{reg['n_corse']} corse all'ora o metro, e {migliaia(reg['m_auto'])} auto che passano"],
         ["Distanza a piedi", f"{raggio} metri"],
         ["Auto da fermare", f"auto che passano × {quota}%"],
         ["Bus contro auto", f"verso Piazza Castello alle 8, auto con fattore {f_ba_hi} (sensori) e {f_ba_lo} (Google)"]],
        [f"I tempi coi mezzi sono solo GTT, senza treni. L'auto è stimata fra due fattori di punta, {f_ba_hi} e {f_ba_lo}.",
         "Il costo del parcheggio in centro non è nel calcolo: pesa come minuti in più.",
         "Si guarda un solo punto per luogo e una sola destinazione, Piazza Castello.",
         "Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati, con ±30%."],
        ["Question: when is the bus from a park-and-ride as fast as the car to the centre?",
         f"Answer: park-and-ride pays off only if parking downtown costs at least {forbice_m} minutes (median of {n_punti_ba} priority points). "
         f"Also, {n_senza} of {n_fermate} important stops lack enough parking.",
         "Limit: bus times use GTT only, without trains; parking cost is not considered."],
        unita=unita, extra=extra)
