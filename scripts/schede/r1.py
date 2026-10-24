"""Risultato 1 (pubblico 1): dove mancano i servizi a piedi."""
from schede.comune import circa, circa_mila, forma_base, leggi, migliaia, num, numero_di, ora, virgola, voce




# ---------------------------------------------------------------- Risultato 1

GRUPPI_EN = {"scuole": "schools", "salute": "health", "cibo": "shops and commercial activities",
             "fermate": "public transport stops",
             "verde": "green space"}   # nomi dei gruppi del risultato 1 in inglese (solo per la traduzione)


GRUPPI_R1 = ["scuole", "salute", "cibo", "fermate", "verde"]   # ordine dei 5 gruppi (come GRUPPI dello script 21)


NOMI_R1 = {"cibo": "negozi e attività commerciali"}   # il gruppo "cibo" contiene tutte le attività commerciali




def nome_r1(g):
    return NOMI_R1.get(g, g)




def scheda_r1():
    vuoti = leggi("risultato1_vuoti.json")
    cand = leggi("risultato1_candidati.json")["gruppi"]
    testa = vuoti["numeri_di_testa"]
    gruppi = vuoti["gruppi"]
    v2 = vuoti["v2"]    # versione 2: serve aver rilanciato 21_risultato1_vuoti.py
    t2 = v2["titolo"]
    SOGLIA_TITOLO_R1 = v2["soglia_titolo_n_mancanti"]   # dal JSON, non scritta qui
    rif = str(v2["soglia_poco_abitata_ab_km2"])
    r2 = v2["torino"][rif]
    abitate = r2["per_n_mancanti"]["abitate"]
    titolo_n = t2["residenti_abitati_con_3_o_piu_mancanti"]
    titolo_pct = 100.0 * titolo_n / t2["residenti_torino"]
    poco = t2["residenti_poco_abitate"]
    verif = t2["residenti_da_verificare"]
    raggio_f = v2["raggio_fermata_sospetta_m"]
    tutti5 = t2["residenti_tutti_5_mancanti"]
    soglia_txt = migliaia(v2["soglia_poco_abitata_ab_km2"])
    sens = {x: v2["torino"][x] for x in sorted(v2["torino"], key=int)}
    sens_txt = "; ".join(f"con {migliaia(int(x))} ab/km² le zone poco abitate sono {migliaia(q['residenti_poco_abitate'])} "
                         f"residenti e quelli con {SOGLIA_TITOLO_R1} o più servizi mancanti {migliaia(q['abitate_con_3_o_piu_mancanti'])}"
                         for x, q in sens.items())
    sens_en = "; ".join(f"at {int(x):,} inhabitants/km² the sparsely populated zones hold {q['residenti_poco_abitate']:,} "
                        f"residents and those missing {SOGLIA_TITOLO_R1}+ services {q['abitate_con_3_o_piu_mancanti']:,}"
                        for x, q in sens.items())
    cint = v2["cintura"][rif]
    ordine = sorted(gruppi, key=lambda g: -gruppi[g]["torino"]["zero"]["residenti"])
    senza = testa["residenti_torino_senza_almeno_un_servizio_essenziale_a_zero"]
    oggi = [num(f"Residenti di zone abitate senza {SOGLIA_TITOLO_R1} o più servizi", titolo_n, "residenti"),
            num("Quota dei residenti di Torino", round(titolo_pct, 1), "%"),
            num("Tutti e 5 i servizi mancanti", tutti5, "residenti"),
            num("Residenti nelle zone poco abitate (a parte)", poco, "residenti"),
            num("Residenti in zone da verificare (a parte)", verif, "residenti"),
            num("Residenti senza almeno un servizio essenziale", senza, "residenti"),
            num("Quota dei residenti di Torino senza almeno un servizio", testa["quota_residenti_torino"], "%")]
    oggi += [num(f"Senza {nome_r1(g)} entro 15 min", gruppi[g]["torino"]["zero"]["residenti"], "residenti")
             for g in ordine]
    dopo, barre_dopo = [], []
    mancanti = [g for g in ordine if g not in cand]
    if mancanti:
        raise SystemExit(f"Risultato 1: mancano i candidati di {', '.join(mancanti)}: "
                         "lancia scripts\\RISULTATO1_CANDIDATI.bat")
    for g in ordine:
        c = cand[g]
        n_punti = len(c["candidati_scelti"])
        etichetta = f"{n_punti} {'punto nuovo' if n_punti == 1 else 'punti nuovi'}"
        dopo.append(num(f"Senza {nome_r1(g)} ({etichetta})", c["residenti_restano_a_zero"], "residenti",
                        prima=c["residenti_a_zero_totali"]))
        barre_dopo.append(voce(f"{nome_r1(g)} ({etichetta})", c["residenti_restano_a_zero"],
                               prima=c["residenti_a_zero_totali"], tono="rosso"))
    salvati = sum(cand[g]["residenti_guadagnati_totali"] for g in ordine)
    return {
        "risultato": "1",
        "titolo": "Dove mancano i servizi a piedi",
        "tag": "STIMATO",
        "stato": "Fatto",
        "in_breve": "Torino è una città compatta, ma non tutti hanno scuola, medico, negozi, "
                    "una fermata e un po' di verde a un quarto d'ora a piedi da casa.",
        "domanda": "Quanti residenti di Torino, nelle zone abitate, non hanno più servizi essenziali (scuole, salute, "
                   "negozi e attività commerciali, fermate, verde) entro 15 minuti a piedi, e quanti ne "
                   "recupererebbe qualche servizio nuovo?",
        "numero_chiave": {"valore": titolo_n, "unita": "residenti",
                          "testo": f"di zone abitate di Torino senza {SOGLIA_TITOLO_R1} o più dei 5 servizi essenziali "
                                   f"a 15 minuti a piedi ({virgola(titolo_pct)}% dei torinesi)"},
        "racconto": "Una delle domande da cui è partito il progetto: dove mancano i servizi? L'idea di "
                    "riferimento è la \"città dei 15 minuti\", in cui le cose di tutti i giorni si raggiungono "
                    "a piedi.",
        "risposta": [
            f"{migliaia(titolo_n)} residenti su {migliaia(t2['residenti_torino'])} ({virgola(titolo_pct)}%) vivono in "
            f"zone abitate (almeno {soglia_txt} abitanti per km²) e non hanno {SOGLIA_TITOLO_R1} o più dei 5 servizi entro 15 minuti a piedi. "
            f"Tutti e 5 mancano a {migliaia(tutti5)} residenti.",
            f"Altri {migliaia(poco)} residenti vivono in zone poco abitate (parchi, collina): sono contati a parte, "
            "fuori dal titolo.",
            f"Altri {migliaia(verif)} residenti sono in zone dove il calcolo non raggiunge una fermata che c'è: "
            "contati a parte, da verificare.",
            f"Contando anche le zone poco abitate, {migliaia(senza)} residenti su {migliaia(testa['residenti_torino'])} "
            f"({virgola(testa['quota_residenti_torino'])}%) non hanno almeno uno dei 5 servizi entro 15 minuti a piedi.",
            f"Il servizio che manca più spesso è {nome_r1(testa['gruppo_piu_carente_a_torino'])}: "
            f"{migliaia(gruppi[testa['gruppo_piu_carente_a_torino']]['torino']['zero']['residenti'])} residenti senza un servizio di questo tipo vicino.",
            f"Pochi servizi nuovi messi nei punti giusti (al massimo 5 per gruppo) riporterebbero "
            f"entro i 15 minuti {migliaia(salvati)} di questi casi, contati gruppo per gruppo.",
        ],
        "grafici": [
            {"tipo": "barre", "titolo": "Residenti per numero di servizi mancanti (0-5), zone abitate",
             "unita": "residenti",
             "nota": f"Zone abitate = almeno {soglia_txt} abitanti per km². Le zone poco abitate "
                     f"({migliaia(poco)} residenti) sono escluse. Servizi mancanti = zero entro 15 minuti a piedi.",
             "voci": [voce(f"{k} mancanti", abitate[str(k)], tono="rosso" if k >= SOGLIA_TITOLO_R1 else None)
                      for k in range(6)]},
            {"tipo": "barre", "titolo": "Residenti di Torino senza il servizio entro 15 minuti a piedi",
             "unita": "residenti",
             "voci": [voce(nome_r1(g), gruppi[g]["torino"]["zero"]["residenti"], tono="rosso") for g in ordine]},
            {"tipo": "barre", "titolo": "Residenti con pochissimi servizi di quel tipo vicini",
             "unita": "residenti",
             "nota": "\"Pochissimi\" = sotto il livello che ha il 10% dei residenti meno servito (soglia per gruppo).",
             "voci": [voce(nome_r1(g), gruppi[g]["torino"]["pochissimo"]["residenti"]) for g in ordine]},
            {"tipo": "barre", "titolo": "Residenti senza il servizio: oggi e con i punti nuovi",
             "unita": "residenti", "nota": "Barra chiara = oggi, barra scura = con i punti nuovi.",
             "voci": barre_dopo},
        ],
        "metodo": [
            "Per ognuna delle 4.044 sezioni di censimento di Torino (centinaia di persone ciascuna) si contano "
            "i servizi raggiungibili camminando 15 minuti sulla rete stradale reale (OpenStreetMap), con il "
            "motore di percorsi R5.",
            "Cinque gruppi trattati separatamente, senza un indice unico: scuole, salute, negozi e attività "
            "commerciali (catalogo comunale), fermate del trasporto pubblico, verde.",
            "\"Senza\" = zero servizi di quel gruppo entro 15 minuti. I residenti vengono dal censimento ISTAT 2021.",
            f"Per ogni sezione si contano quanti dei 5 gruppi mancano (0-5). Le sezioni con meno di {soglia_txt} "
            "abitanti per km² (superficie e residenti del censimento) sono \"poco abitate\": in grigio e fuori dal "
            f"titolo, che conta i residenti delle zone abitate con {SOGLIA_TITOLO_R1} o più servizi mancanti.",
            "Dove aggiungere un servizio: per ogni gruppo si cercano fino a 5 punti (raggruppando le zone scoperte entro 400 m) che "
            "riportano dentro i 15 minuti più residenti possibile, uno dopo l'altro.",
        ],
        "criteri": [
            {"nome": "Zona poco abitata", "valore": f"sotto {soglia_txt} abitanti per km²",
             "perche": "parchi, collina e zone poco abitabili sono vuoti per natura: contarli come carenza falserebbe il titolo",
             "effetto": "; ".join(f"{migliaia(int(x))} ab/km²: {migliaia(q['residenti_poco_abitate'])} residenti poco abitati, "
                                  f"{migliaia(q['abitate_con_3_o_piu_mancanti'])} abitati con {SOGLIA_TITOLO_R1} o più servizi mancanti, "
                                  f"{migliaia(q['abitate_con_1_o_piu_mancanti'])} abitati con almeno 1" for x, q in sens.items())},
            {"nome": "Titolo", "valore": f"residenti delle zone abitate con {SOGLIA_TITOLO_R1} o più dei 5 servizi mancanti",
             "perche": "guardare dove mancano più servizi insieme, non uno solo",
             "effetto": f"\"tutti e 5 mancanti\": {migliaia(tutti5)} residenti (non fa titolo)"},
            {"nome": "Cintura (a parte)", "valore": f"servizio raggiungibile a piedi in 15 minuti o col mezzo pubblico entro 45 minuti alle {v2['ora_tp_cintura']}:00 di un feriale (scuole, salute, negozi)",
             "perche": "fuori Torino si va in paese e non a piedi: la regola della città dei 15 minuti non vale",
             "effetto": f"{migliaia(cint['abitate_con_3_o_piu_mancanti'])} residenti di zone abitate con {SOGLIA_TITOLO_R1} o più servizi mancanti: "
                        "non confrontabile con Torino (catalogo diverso)"},
        ],
        "parametri": [["Tempo a piedi", "15 minuti"], ["Velocità a piedi", "80 m al minuto (4,8 km/h)"],
                      ["Zona poco abitata", f"sotto {soglia_txt} ab/km² (prove con "
                                            + " e ".join(migliaia(x) for x in v2["sensibilita_ab_km2"]) + ")"],
                      ["Sezioni di Torino", "4.044"], ["Residenti", migliaia(testa["residenti_torino"])],
                      ["Punti nuovi per gruppo", "fino a 5"]],
        "limiti": [
            f"Zona \"da verificare\": nessuna fermata entro 15 minuti a piedi nel calcolo, ma una fermata GTT entro "
            f"{raggio_f} m in linea d'aria (probabile errore del punto di partenza); esclusa dal titolo e dai punti nuovi.",
            "Solo Torino: in cintura il catalogo dei servizi non c'è, quindi lì \"zero\" vuol dire spesso "
            "\"manca il dato\", non \"manca il servizio\".",
            "Il gruppo \"negozi e attività commerciali\" usa tutte le attività commerciali del catalogo, senza distinguere la categoria.",
            "Si conta se un servizio c'è, non quanto è grande o se ha posto (una scuola piena conta come una vuota).",
            "Capienza di ospedali, presidi e scuole non nota: un ospedale grande e un ambulatorio contano uguale.",
            "Orario programmato: niente ritardi né affollamento. Le sezioni senza superficie contano come abitate.",
            "I punti nuovi sono posizioni ipotetiche: non tengono conto di costi, spazi liberi o permessi, e "
            "non si sommano tra gruppi.",
        ],
        "in_english": [
            f"Question: how many Turin residents in inhabited areas lack {SOGLIA_TITOLO_R1} or more essential services "
            "(schools, health, shops and commercial activities, stops, green space) within 15 minutes on foot, and "
            "how many would gain one with a few new services?",
            f"{titolo_n:,} residents out of {t2['residenti_torino']:,} ({titolo_pct:.1f}%) live in inhabited areas "
            f"(at least {v2['soglia_poco_abitata_ab_km2']:,} inhabitants per km²) and lack {SOGLIA_TITOLO_R1} or more of the 5 services "
            f"within 15 minutes on foot; all 5 are missing for {tutti5:,}. A further {poco:,} residents live in sparsely "
            f"populated areas (parks, hills), counted separately. Sensitivity of the threshold: {sens_en}.",
            f"Counting those areas too, {senza:,} residents out of {testa['residenti_torino']:,} ({testa['quota_residenti_torino']:.1f}%) lack at "
            f"least one of the 5 services within 15 minutes on foot. The most often missing one is "
            f"{GRUPPI_EN.get(testa['gruppo_piu_carente_a_torino'], testa['gruppo_piu_carente_a_torino'])}, with "
            f"{gruppi[testa['gruppo_piu_carente_a_torino']]['torino']['zero']['residenti']:,} "
            "residents without a nearby service of that kind.",
            f"A further {verif:,} residents live in areas where the calculation does not reach a stop that exists "
            "(counted separately, to be verified).",
            f"Up to 5 new services per group, placed where they help most, would bring {salvati:,} of these cases "
            "within 15 minutes, counted group by group.",
            f"Areas flagged for verification have no stop within 15 minutes on foot in the calculation but a stop within "
            f"{raggio_f} m as the crow flies; they are excluded from the headline figure and from the new-service points.",
            "Limits: the map covers Turin and its surrounding belt; in the belt a service counts as missing only if it "
            "is out of reach both on foot (15 minutes) and by public transport (45 minutes, 8 am on a weekday), and the "
            "service data there (schools, health, shops from OpenStreetMap) is less complete.",
        ],
        "mappa": {"id": "faseb", "tema": "Dove mancano i servizi",
                  "nota": "Nella mappa, tema \"Dove mancano i servizi\": all'apertura quanti servizi mancano in ogni "
                          "zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove "
                          "aggiungerne uno."},
        "fonti": ["docs/R1_servizi.md", "docs/rapporti/RAPPORTO_RISULTATO1.txt", "docs/rapporti/RAPPORTO_RISULTATO1_CANDIDATI.txt",
                  "scripts/21_risultato1_vuoti.py", "scripts/22_risultato1_candidati.py"],
        "generato": ora(),
        "avviso": [
            "Dati [STIMATO] — solo comune di Torino",
            f"Distanze a piedi sulla rete stradale (15 min a 80 m/min) su {migliaia(testa['residenti_torino'])} "
            "residenti (censimento 2021). Servizi dal catalogo comunale: la cintura non è confrontabile (manca "
            "il dato, non il servizio). I punti nuovi sono ipotesi di posizione, calcolate gruppo per gruppo: "
            "non si sommano tra gruppi e non tengono conto di costi o spazi disponibili."
        ],
        "scenari": [
            {"nome": "Oggi", "numeri": oggi,
             "nota": f"Il gruppo con più residenti scoperti è {nome_r1(testa['gruppo_piu_carente_a_torino'])}. Sensibilità della soglia: {sens_txt}."},
            {"nome": "Con pochi servizi nuovi nei punti migliori", "numeri": dopo,
             "nota": "Fino a 5 punti per gruppo, scelti dove recuperano più residenti (raggruppamento 400 m)."},
        ],
    }




def forma_r1(s):
    """Scheda R1 (Piano risultati A1 + A3): copertura a 5, 10 e 15 minuti (v3 di 21_risultato1_vuoti.py) ed esposizione
    al traffico (92_esposizione_traffico.py). Tutti i numeri vengono dai JSON."""
    v2 = leggi("risultato1_vuoti.json")["v2"]
    v3 = leggi("risultato1_vuoti.json").get("v3")
    esp = leggi("esposizione_traffico.json")
    if not v3 or any(m not in v3["minuti_a_piedi"] for m in (5, 10, 15)):
        raise SystemExit("Risultato 1: la copertura a 5 e 10 minuti non c'e' in risultato1_vuoti.json: lancia "
                         "scripts\\R1_PIEDI_5_10.bat e poi scripts\\21_risultato1_vuoti.py")
    quota_senza = numero_di(s, "Quota dei residenti di Torino senza almeno")
    senza = numero_di(s, "Residenti senza almeno un servizio")
    tre_o_piu = numero_di(s, "Residenti di zone abitate senza")
    n_critiche = len(v2["sezioni_critiche_torino"])
    par = dict(map(tuple, s["parametri"]))
    soglia = par["Zona poco abitata"].split(" ab")[0].replace("sotto ", "")
    pr = esp["parametri"]
    raggio, raggio_v = int(pr["raggio_esposta_m"]), int(pr["raggio_vicina_m"])
    classi = esp["classi"]
    sol = v3["soglie"]

    def quota(m, k):   # % dei residenti delle zone abitate con k servizi presenti a m minuti
        return 100.0 * sol[str(m)]["per_n_servizi"][str(k)] / sol[str(m)]["residenti"]

    righe = []
    for m in (5, 10, 15):
        cinque, quattro = round(quota(m, 5), 1), round(quota(m, 4), 1)
        righe.append({"label": f"{m} minuti", "voci": [
            voce("tutti e 5 i servizi", cinque, tono="verde"),
            voce("4 servizi", quattro, tono="giallo"),
            voce("3 o meno", round(100 - cinque - quattro, 1), tono="rosso")]})
    principale = {"tipo": "pila100", "titolo": "Residenti per servizi raggiunti a piedi", "unita": "%",
                  "nota": f"Ogni barra è un tempo a piedi: 100% dei residenti delle zone abitate (almeno {soglia} abitanti per km²).",
                  "righe": righe}
    grafico_traffico = {"tipo": "barre", "titolo": "Residenti per distanza da una strada molto trafficata", "unita": "residenti",
                        "nota": f"Distanza dal centro della sezione. Strada molto trafficata: almeno "
                                f"{migliaia(pr['soglia_molto_traffico_veic_giorno'])} veicoli al giorno.",
                        "voci": [voce(f"esposti (meno di {raggio} m)", classi["esposta"]["residenti"], tono="rosso"),
                                 voce(f"vicini ({raggio}-{raggio_v} m)", classi["vicina"]["residenti"], tono="giallo"),
                                 voce(f"lontani (oltre {raggio_v} m)", classi["lontana"]["residenti"], tono="verde")]}
    ordine = sorted(GRUPPI_R1, key=lambda g: -sol["15"]["senza_servizio"][g])
    grafico_senza = {"tipo": "barre", "titolo": "Residenti senza il servizio a 15 minuti a piedi", "unita": "residenti",
                     "nota": f"Solo zone abitate (almeno {soglia} abitanti per km²).",
                     "voci": [voce(nome_r1(g), sol["15"]["senza_servizio"][g], tono="rosso") for g in ordine]}
    calcolo = ["Per ogni sezione di censimento si contano i servizi raggiungibili a piedi in 5, 10 e 15 minuti.",
               "I tipi di servizio sono cinque, contati separatamente: scuole, salute, negozi, fermate, verde.",
               f"Si cammina sulla rete stradale reale (OpenStreetMap), a {par['Velocità a piedi'].split(' (')[0]}.",
               f"Residenti dal censimento ISTAT 2021; le zone con meno di {soglia} abitanti per km² sono grigie e contate a parte.",
               f"Si è esposti se il centro della sezione è a meno di {raggio} m da una strada molto trafficata.",
               f"Il traffico viene da un modello tarato sui sensori, che sbaglia del ±{pr['fascia_errore_pct']}% in metà dei casi."]
    parametri = [["Tempi a piedi", "5, 10 e 15 minuti"] if p[0] == "Tempo a piedi" else list(p) for p in s["parametri"]]
    parametri += [["Strada molto trafficata", f"almeno {migliaia(pr['soglia_molto_traffico_veic_giorno'])} veicoli al giorno"],
                  ["Esposto al traffico", f"a meno di {raggio} m dalla strada"]]
    anima = {"tipo": "cerchi",
             "voci": [{"min": m, "pct": round(quota(m, 5), 1), "testo": f"tutti e 5 i servizi a {m} minuti a piedi"} for m in (5, 10, 15)],
             "didascalia": "Residenti delle zone abitate che hanno scuole, salute, negozi, fermate e verde a 5, 10 e 15 minuti da casa a piedi."}
    return forma_base(
        s,
        "Torino, città dei 15 minuti: quasi tutti hanno i servizi a 15 minuti a piedi",
        "Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata?",
        {"valore": round(quota(15, 5), 1), "unita": "%",
         "testo": "dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi"},
        principale,
        [f"A 5 minuti solo {circa(quota(5, 5), '%')} dei residenti ha tutti e 5 i servizi; a 10 minuti {circa(quota(10, 5), '%')}.",
         f"{circa_mila(classi['esposta']['residenti'])} residenti ({circa(classi['esposta']['quota'], '%')}) vivono a meno di "
         f"{raggio} m da una strada molto trafficata.",
         f"I {migliaia(tre_o_piu)} residenti senza 3 o più servizi sono in {n_critiche} {'sezione' if n_critiche == 1 else 'sezioni'} di collina: dove manca davvero tutto."],
        [grafico_traffico, grafico_senza],
        calcolo,
        parametri,
        ["Solo Torino: in cintura il catalogo dei servizi manca, quindi «zero» spesso vuol dire dato mancante.",
         "Si conta se un servizio c'è, non quanto è grande né se ha posto. Le fermate usano l'orario programmato: niente ritardi né affollamento.",
         "I punti nuovi sono ipotesi: non tengono conto di costi, spazi liberi o permessi.",
         "Il traffico è un modello e sostituisce rumore e smog, che non sono misurati."],
        ["Question: how many Turin residents lack schools, health, shops, stops or green space within 15 minutes on foot?",
         f"Answer: {senza:,} residents ({quota_senza:.1f}%) lack at least one of the 5 services; {tre_o_piu:,} in inhabited areas lack three or more.",
         "Limit: only Turin is covered, because the service catalogue is missing for the surrounding towns."],
        anima=anima)
