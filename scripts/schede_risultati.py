"""Schede dei RISULTATI per simulazione.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_v2/mappa_r6.json   (Risultato 6, da 79 e 84) -> data/processed/risultato6_riepilogo_mappa.json
  data/processed/risultato8_riepilogo_mappa.json   (Risultato 8, dalla Fase 5 del traffico, script 56-67)
  data/schede_risultati.js   (tutte le schede, R2 compreso, caricate da sole da simulazione.html)

Il riepilogo base del Risultato 2 lo scrive 29_risultato2_metro_notte.py: qui si legge e si arricchisce
solo nel .js (il file JSON di R2 non viene riscritto).

Formato della scheda (base, compatibile col caricamento a mano):
  {risultato, titolo, domanda, scenari:[{nome, numeri:[{label,prima,dopo,unita}], nota}], avviso}
  Un numero senza "prima/dopo" (fotografia di oggi) ha prima = null.
Campi in piu' per la finestra di dettaglio (tutti facoltativi):
  tag, stato, in_breve, numero_chiave {valore, unita, testo}, racconto, risposta [frasi],
  grafici [{tipo: "barre"|"pila"|"orario", titolo, unita, nota, voci|righe}],
  metodo [frasi], parametri [[nome, valore]], limiti [frasi], mappa {tema, nota} | null, fonti [file].
Nessun calcolo nuovo sui dati grezzi: solo numeri gia' presenti nei file prodotti dagli script
(ricontrollati da Claude il 18/10/2026) e semplici somme/conteggi su di essi.
"""
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
PROC = RADICE / "data" / "processed"
DOCS = RADICE / "docs"
OUT_JS = RADICE / "data" / "schede_risultati.js"


def leggi(nome):
    return json.loads((PROC / nome).read_text(encoding="utf-8"))


def num(label, dopo, unita, prima=None):
    return {"label": label, "prima": prima, "dopo": dopo, "unita": unita}


def voce(label, valore, prima=None, tono=None):
    v = {"label": label, "valore": valore}
    if prima is not None:
        v["prima"] = prima
    if tono is not None:   # [R6] "verde"/"rosso" = bene/male; senza tono = blu neutro (quantità)
        v["tono"] = tono
    return v


def migliaia(n):
    return f"{n:,}".replace(",", ".")


def virgola(x):
    testo = f"{x:.1f}".replace(".", ",")
    return testo[:-2] if testo.endswith(",0") else testo


def il(x):
    """articolo davanti a una percentuale: 'il 4,2%', ma 'l'8,3%' e 'l'11%'."""
    testo = virgola(x)
    return ("l'" if testo[0] == "8" or testo.split(",")[0] in ("11", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89") else "il ") + testo


def ora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def minuti(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


# ---------------------------------------------------------------- Risultato 1

GRUPPI_EN = {"scuole": "schools", "salute": "health", "cibo": "shops and commercial activities",
             "fermate": "public transport stops",
             "verde": "green space"}   # nomi dei gruppi del risultato 1 in inglese (solo per la traduzione)
NOMI_R1 = {"cibo": "negozi e attività commerciali"}   # il gruppo "cibo" contiene tutte le attività commerciali (20/10/2026)


def nome_r1(g):
    return NOMI_R1.get(g, g)


def scheda_r1():
    vuoti = leggi("risultato1_vuoti.json")
    cand = leggi("risultato1_candidati.json")["gruppi"]
    testa = vuoti["numeri_di_testa"]
    gruppi = vuoti["gruppi"]
    v2 = vuoti["v2"]    # versione 2 (20/10/2026): serve aver rilanciato 21_risultato1_vuoti.py
    t2 = v2["titolo"]
    SOGLIA_TITOLO_R1 = v2["soglia_titolo_n_mancanti"]   # dal JSON, non scritta qui
    rif = str(v2["soglia_poco_abitata_ab_km2"])
    r2 = v2["torino"][rif]
    abitate = r2["per_n_mancanti"]["abitate"]
    titolo_n = t2["residenti_abitati_con_3_o_piu_mancanti"]
    titolo_pct = 100.0 * titolo_n / t2["residenti_torino"]
    poco = t2["residenti_poco_abitate"]
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
            num("Residenti senza almeno un servizio essenziale", senza, "residenti"),
            num("Quota dei residenti di Torino senza almeno un servizio", testa["quota_residenti_torino"], "%")]
    oggi += [num(f"Senza {nome_r1(g)} entro 15 min", gruppi[g]["torino"]["zero"]["residenti"], "residenti")
             for g in ordine]
    dopo, barre_dopo = [], []
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
        "stato": "Fatto (12-14/10/2026)",
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
            "Fase B: per ogni gruppo si cercano fino a 5 punti (raggruppando le zone scoperte entro 400 m) che "
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
            f"Up to 5 new services per group, placed where they help most, would bring {salvati:,} of these cases "
            "within 15 minutes, counted group by group.",
            "Limits: only the City of Turin is covered; outside it the service catalogue is missing, so a zero there "
            "often means missing data.",
        ],
        "mappa": {"id": "faseb", "tema": "Dove mancano i servizi",
                  "nota": "Nella mappa, menu dei temi: \"Dove mancano i servizi\" (zone scoperte e punti nuovi) "
                          "oppure \"Accessibilità ai servizi\"."},
        "fonti": ["docs/RAPPORTO_RISULTATO1.txt", "docs/RAPPORTO_RISULTATO1_CANDIDATI.txt",
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


# ---------------------------------------------------------------- Risultato 2

def arricchisci_r2(s):
    r2 = leggi("risultato2_metro_notte.json")
    da, a = r2["finestra"].split("-")
    totale_res = sum(x["res"] for x in r2["notte15"]["dettaglio"])
    n15, n30 = r2["notte15"], r2["notte30"]
    # testi dello script 29 scritti senza accenti: solo per la pagina, il JSON di R2 resta com'e'
    accenti = lambda x: x.replace("piu'", "più").replace(" li'", " lì") if isinstance(x, str) else x
    s["domanda"] = accenti(s["domanda"])
    for sc in s["scenari"]:
        sc["nota"] = accenti(sc.get("nota"))
        for n in sc["numeri"]:
            n["label"] = accenti(n["label"])
    s.update({
        "tag": "PROGRAMMATO / STIMATO",
        "stato": "Chiuso (16/10/2026)",
        "in_breve": f"La metro M1 non passa dalle {da} alle {a}: in quelle ore restano solo i bus notturni.",
        # numero in grande: quello severo (almeno +soglia_quota di servizi), scelta di Leo del 20/10
        "numero_chiave": ({"valore": n15["residenti_migliorati_quota"], "unita": "residenti",
                           "testo": f"raggiungerebbero almeno il {round(100 * n15['soglia_quota'])}% di servizi in più "
                                    "di notte con una metro ogni 15 minuti"}
                          if "residenti_migliorati_quota" in n15 else
                          {"valore": n15["residenti_migliorati"], "unita": "residenti",
                           "testo": "raggiungerebbero più servizi di notte con una metro ogni 15 minuti"}),
        "racconto": "Uno dei problemi notati all'inizio del progetto: la metro chiude la sera. Dopo l'ultima corsa "
                    f"arriva un bus sostitutivo, poi dalle {da} alle {a} non c'è più niente sulla linea.",
        "risposta": [
            f"Con una metro ogni 15 minuti nel buco notturno, {migliaia(n15['residenti_migliorati'])} residenti "
            f"di Torino e cintura (su {migliaia(totale_res)}) raggiungerebbero più servizi entro 45 minuti.",
            f"Con una corsa ogni 30 minuti sarebbero {migliaia(n30['residenti_migliorati'])}: metà delle corse, "
            f"ma {il(round(100 * n30['residenti_migliorati'] / n15['residenti_migliorati']))}% dei residenti che ci guadagnano.",
            f"L'attesa media teorica alla fermata sarebbe di {virgola(n15['attesa_media_minuti'])} minuti nel primo "
            f"caso e {virgola(n30['attesa_media_minuti'])} nel secondo.",
        ] + ([f"Contando solo chi ha un miglioramento netto (almeno il {round(100 * n15['soglia_quota'])}% di servizi "
              f"raggiungibili in più di notte): {migliaia(n15['residenti_migliorati_quota'])} residenti con la metro ogni "
              f"15 minuti, {migliaia(n30['residenti_migliorati_quota'])} ogni 30."]
             if "residenti_migliorati_quota" in n15 else []),
        "grafici": [
            {"tipo": "orario", "titolo": "La metro M1 nelle 24 ore (giorno feriale)",
             "nota": "Il buco senza metro né bus sostitutivo è quello che lo scenario riempie con corse finte.",
             "righe": [
                 {"label": "Metro M1", "tono": "pieno", "tratti": [[minuti("05:22"), minuti("22:02")]]},
                 {"label": "Bus sostitutivo", "tono": "medio",
                  "tratti": [[minuti("21:35"), 1440], [0, minuti(da)]]},
                 {"label": "Nessun servizio sulla linea", "tono": "vuoto", "tratti": [[minuti(da), minuti(a)]]},
             ]},
            {"tipo": "barre", "titolo": "Residenti che raggiungono più servizi di notte",
             "unita": "residenti",
             "voci": [voce("una corsa ogni 15 minuti", n15["residenti_migliorati"]),
                      voce("una corsa ogni 30 minuti", n30["residenti_migliorati"])]
                     + ([voce(f"ogni 15 minuti, almeno +{round(100 * n15['soglia_quota'])}%", n15["residenti_migliorati_quota"]),
                         voce(f"ogni 30 minuti, almeno +{round(100 * n15['soglia_quota'])}%", n30["residenti_migliorati_quota"])]
                        if "residenti_migliorati_quota" in n15 else [])},
            {"tipo": "barre", "titolo": "Sezioni di censimento migliorate", "unita": "sezioni",
             "nota": f"Su {migliaia(len(n15['dettaglio']))} sezioni di Torino e cintura.",
             "voci": [voce("una corsa ogni 15 minuti", n15["sezioni_migliorate"]),
                      voce("una corsa ogni 30 minuti", n30["sezioni_migliorate"])]},
        ],
        "metodo": [
            f"Dal GTFS ufficiale GTT (giorno feriale del {r2['giorno']}) si trova il buco reale: metro "
            f"05:22-22:02, bus sostitutivo fino alle 00:50, poi niente fino alle 05:22.",
            "Si costruiscono due orari finti, uguali a quello vero più corse della metro nel buco: una ogni 15 "
            "minuti oppure una ogni 30, copiando i tempi dell'ultima corsa vera.",
            "Per ogni sezione di censimento di Torino e cintura si contano i servizi raggiungibili in 45 minuti "
            "(a piedi + trasporto pubblico) alle ore 01, 02, 03 e 04, con e senza le corse finte (motore R5).",
            "Una sezione è \"migliorata\" se il numero di servizi raggiungibili aumenta anche di poco: a Torino "
            "nessuna zona è mai del tutto scoperta di notte, perché ci sono già i bus notturni.",
        ],
        "parametri": [["Finestra", f"{da} - {a}"], ["Ore calcolate", "01, 02, 03, 04"],
                      ["Tempo massimo di viaggio", "45 minuti"],
                      ["Sezioni migliorate (15')", migliaia(n15["sezioni_migliorate"])],
                      ["Sezioni migliorate (30')", migliaia(n30["sezioni_migliorate"])]],
        "limiti": [
            "Orario programmato: niente traffico, ritardi, capienza dei mezzi o passeggeri reali.",
            "\"Servizi raggiungibili\" è un conteggio di destinazioni, non una stima di quante persone "
            "userebbero la metro di notte.",
            "Le corse finte non hanno tempi di sosta alle fermate e non tengono conto di costi e manutenzione notturna.",
            "Non dice quante auto in meno ci sarebbero: serve un metodo a parte.",
        ],
        "in_english": [
            f"Question: if the metro ran through the night gap between {da} and {a} (simulated extra runs), how many residents "
            "would reach more services?",
            f"With a metro every 15 minutes in the gap, {n15['residenti_migliorati']:,} residents of Turin and the belt "
            f"(out of {totale_res:,}) would reach more services within 45 minutes. With a run every 30 minutes, "
            f"{n30['residenti_migliorati']:,} would."
            + (f" Counting only a clear gain (at least {round(100 * n15['soglia_quota'])}% more reachable services at "
               f"night): {n15['residenti_migliorati_quota']:,} and {n30['residenti_migliorati_quota']:,} residents."
               if "residenti_migliorati_quota" in n15 else ""),
            f"The average theoretical wait at the stop would be {n15['attesa_media_minuti']:.1f} minutes in the first "
            f"case and {n30['attesa_media_minuti']:.1f} in the second.",
            "Limits: scheduled timetable only, with no traffic, delays, vehicle capacity or real passengers; the count is "
            "of reachable destinations, not of people using the metro.",
        ],
        "mappa": {"id": "accessibilita", "tema": "Accessibilità ai servizi",
                  "nota": "La mappa mostra la situazione di oggi ora per ora (tema \"Accessibilità ai servizi\", "
                          "cursore dell'ora sulla notte); lo scenario con la metro non è ancora in mappa."},
        "fonti": ["docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt", "docs/PIANO_RISULTATO2.md",
                  "scripts/28_scenario_metro_notte.py", "scripts/29_risultato2_metro_notte.py"],
    })
    return s


# ---------------------------------------------------------------- Risultato 4

def fasce_r4():
    """Tabella 'fasce orarie (feriale)' del rapporto dello script 27 (non e' nel JSON)."""
    testo = (DOCS / "RAPPORTO_RISULTATO4.txt").read_text(encoding="utf-8")
    blocco = testo.split("fasce orarie (feriale")[1].split("\n\n")[0]
    righe = []
    for riga in blocco.splitlines():
        m = re.match(r"\s*([a-z_]+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)", riga)
        if m:
            righe.append((m.group(1), int(m.group(2)), float(m.group(5))))
    return righe


# copertura verificata da Claude il 18/10/2026 su trip_update_gtt (ore 06-24 con almeno 50 minuti letti)
GIORNI_PARZIALI_R4 = ("sabato 10 dalle 15, lunedì 12 dalle 12, martedì 13 con buchi il pomeriggio e la sera, "
                      "domenica 18 fino alle 9:30 (poi guasto del feed GTT)")


def scheda_r4():
    r = leggi("risultato4_regolarita.json")
    c = r["citta"]
    par = r["parametri"]
    nomi = {"0": "Feriale", "1": "Sabato", "2": "Domenica"}
    scenari = []
    for k in ("0", "1", "2"):
        x = c[k]
        scenari.append({
            "nome": f"{nomi[k]} ({r['giorni'][k]} {'giorno' if r['giorni'][k] == 1 else 'giorni'}, "
                    f"{migliaia(x['passaggi'])} passaggi)",
            "numeri": [
                num("Passaggi in ritardo oltre 5 min", x["ritardo"], "%"),
                num("Coppie di bus a grappolo o con un buco (linee frequenti)",
                    round(x["grappolo"] + x["buco"], 1), "%"),
                num("Ritardo mediano", x["mediana"], "min"),
                num("Passaggi in anticipo oltre 1 min", x["anticipo"], "%"),
            ],
        })
    scenari[0]["nota"] = ("Molti passaggi risultano in anticipo perché l'orario ufficiale ha margini; "
                          "un ritardo mediano negativo vuol dire 'di solito un po' prima'.")
    s = r["scarti"]
    tot = s["usati"] + s["fuori_gtfs"] + s["lettura_lontana"]
    fer = c["0"]
    linee = [(nome, v["0"]) for nome, v in r["linee"].items() if "0" in v]
    peggio_rit = sorted((x for x in linee if x[1]["passaggi"] >= par.get("min_passaggi_classifica", 2000) and str(x[0]).isdigit()),
                        key=lambda x: -x[1]["ritardo"])[:10]
    peggio_irr = sorted((x for x in linee if (x[1].get("coppie") or 0) >= par["min_coppie"] and str(x[0]).isdigit()),
                        key=lambda x: -(x[1]["grappolo"] + x[1]["buco"]))[:10]
    nomi_fasce = {"punta_mattina": "punta del mattino (7-9)", "giorno": "giorno (9-16)",
                  "punta_sera": "punta della sera (16-19)", "sera": "sera (19-24)", "notte": "notte e primo mattino (fino alle 7, dati parziali)"}
    scheda = {
        "risultato": "4",
        "titolo": "Bus in ritardo e bus irregolari",
        "tag": "MISURATO",
        "stato": f"Versione 2 ({r['periodo']['da'][8:10]}-{r['periodo']['a'][8:10]}/10/2026)",
        "in_breve": "L'orario alla fermata promette un passaggio ogni tot minuti. Quanto spesso i mezzi GTT "
                    "arrivano davvero in ritardo, o a coppie lasciando un buco?",
        "domanda": "Quanto spesso i mezzi GTT arrivano in ritardo, e quanto spesso sulle linee frequenti "
                   "arrivano a grappolo o lasciano buchi?",
        "numero_chiave": {"valore": fer["ritardo"], "unita": "%",
                          "testo": "dei passaggi nei giorni feriali arriva con più di 5 minuti di ritardo"},
        "racconto": "Una delle direzioni del progetto: confrontare l'orario promesso con quello reale, usando "
                    "le posizioni e i ritardi dei mezzi che il Raspberry Pi del progetto raccoglie ogni minuto.",
        "risposta": [
            f"Nei giorni feriali {il(fer['ritardo'])}% dei passaggi arriva con più di 5 minuti di "
            f"ritardo; il sabato {il(c['1']['ritardo'])}%.",
            f"Sulle linee frequenti {il(fer['grappolo'] + fer['buco'])}% delle coppie di mezzi "
            "consecutivi arriva a grappolo o lascia un buco.",
            f"Il problema più comune è l'anticipo: {il(fer['anticipo'])}% dei passaggi feriali arriva "
            "più di un minuto prima dell'orario.",
        ],
        "grafici": [
            {"tipo": "pila", "titolo": "Come arrivano i mezzi nei giorni feriali", "unita": "%",
             "voci": [voce("in anticipo (oltre 1 min)", fer["anticipo"]),
                      voce("puntuali (da -1 a +5 min)", fer["puntuale"], tono="verde"),
                      voce("in ritardo (oltre 5 min)", fer["ritardo"], tono="rosso")]},
            {"tipo": "barre", "titolo": "Passaggi in ritardo oltre 5 minuti, per fascia oraria (feriale)",
             "unita": "%", "voci": [voce(nomi_fasce.get(f, f), v, tono="rosso") for f, _, v in fasce_r4()]},
            {"tipo": "barre", "titolo": "Passaggi in ritardo oltre 5 minuti, per tipo di giorno",
             "unita": "%", "voci": [voce(nomi[k].lower(), c[k]["ritardo"], tono="rosso") for k in ("0", "1", "2")]},
            {"tipo": "barre", "titolo": "Le 10 linee più in ritardo (feriale)", "unita": "%",
             "nota": f"Solo linee ordinarie (nome di sole cifre) con almeno {par.get('min_passaggi_classifica', 2000)} passaggi osservati.",
             "voci": [voce(f"linea {n}", x["ritardo"], tono="rosso") for n, x in peggio_rit]},
            {"tipo": "barre", "titolo": "Le 10 linee più irregolari (feriale): grappolo + buco", "unita": "%",
             "nota": f"Solo linee frequenti (un mezzo ogni {int(par['freq_max_min'])} minuti o meno) con almeno "
                     f"{par['min_coppie']} coppie osservate.",
             "voci": [voce(f"linea {n}", round(x["grappolo"] + x["buco"], 1)) for n, x in peggio_irr]},
        ],
        "metodo": [
            "Il Raspberry Pi legge ogni minuto il feed in tempo reale di GTT: per ogni corsa, il ritardo "
            "previsto alle fermate successive.",
            "Per ogni corsa e fermata si tiene l'ultima lettura prima del passaggio, la più vicina all'arrivo "
            "vero, e la si confronta con l'orario ufficiale (GTFS).",
            "Classi: in anticipo sotto -1 minuto, puntuale da -1 a +5, in ritardo oltre +5.",
            "Regolarità: per due mezzi consecutivi della stessa linea alla stessa fermata, \"grappolo\" se "
            "l'intervallo vero è meno della metà di quello previsto, \"buco\" se è più del doppio. Solo linee "
            "con un mezzo ogni 15 minuti o meno.",
        ],
        "parametri": [["Periodo", f"{r['periodo']['da']} - {r['periodo']['a']}"],
                      ["Passaggi usati", f"{migliaia(s['usati'])} ({round(100 * s['usati'] / tot)}%)"],
                      ["Soglia ritardo", f"{virgola(par['soglia_ritardo_min'])} min"],
                      ["Soglia anticipo", f"{virgola(par['soglia_anticipo_min'])} min"],
                      ["Lettura troppo lontana", f"oltre {int(par['max_lettura_lontana_min'])} min, scartata"]],
        "limiti": [
            f"Pochi giorni ({r['giorni']['0']} feriali, {r['giorni']['1']} sabati, {r['giorni']['2']} domeniche), "
            f"e non tutti interi: {GIORNI_PARZIALI_R4}. Ogni giorno conta con le ore che hanno dati.",
            "La raccolta si ferma a mezzanotte e riparte verso le 5: la notte non è misurata.",
            "Il feed copre solo le linee urbane (circa 90): le extraurbane non ci sono mai. Anche sulle linee "
            "coperte manca circa 1 corsa su 5 (il 15/10: 80% delle corse programmate presenti): se alcune erano "
            "saltate davvero, la puntualità reale è peggiore e i buchi sono più di quelli contati.",
            "Il ritardo è quello dichiarato dal feed di GTT a ridosso della fermata, non osservato sul posto.",
            f"Scartato il {round(100 * (tot - s['usati']) / tot)}% dei passaggi (corse non nell'orario ufficiale "
            "o lette troppo lontano dall'arrivo).",
            "Dice quanto spesso c'è ritardo, non quante persone aspettano né quanto erano pieni i mezzi.",
        ],
        "in_english": [
            "Question: how often do GTT vehicles arrive late, and how often do frequent lines bunch together or leave "
            "gaps?",
            f"On weekdays {fer['ritardo']:.1f}% of departures arrive more than 5 minutes late; on Saturdays "
            f"{c['1']['ritardo']:.1f}%. On frequent lines {fer['grappolo'] + fer['buco']:.1f}% of consecutive pairs of "
            "vehicles bunch together or leave a gap.",
            f"The most common problem is early arrival: {fer['anticipo']:.1f}% of weekday departures arrive more than one "
            "minute before the timetable.",
            f"Limits: only {r['giorni']['0']} weekdays, {r['giorni']['1']} Saturdays and {r['giorni']['2']} Sundays of data, "
            "some of them partial; the night is not measured.",
        ],
        "mappa": None,
        "fonti": ["docs/RAPPORTO_RISULTATO4.txt", "docs/PIANO_RISULTATO4.md", "scripts/27_risultato4_regolarita.py"],
        "generato": ora(),
        "avviso": [
            "Dati [MISURATO] — pochi giorni",
            f"Arrivi reali dal feed GTT raccolto dal Raspberry Pi, {r['periodo']['da']} - {r['periodo']['a']}: "
            f"usato il {round(100 * s['usati'] / tot)}% dei passaggi letti (scartati quelli fuori orario ufficiale "
            "o con lettura lontana). Giorni non tutti interi e solo linee urbane presenti nel feed: vedi i limiti."
        ],
        "scenari": scenari,
    }
    r9 = scheda_r9()
    scheda["titolo"] = "Puntualità e attese"
    scheda["domanda"] = scheda["domanda"] + " E quanto si aspetta davvero alla fermata, rispetto a quello che promette l'orario?"
    scheda["risposta"] = scheda["risposta"] + ["Attesa: " + r9["risposta"][0]] + r9["risposta"][1:]
    for chiave in ("grafici", "scenari", "limiti"):
        scheda[chiave] = scheda.get(chiave, []) + r9.get(chiave, [])
    scheda["in_english"] = scheda.get("in_english", []) + r9.get("in_english", [])[1:]
    scheda["fonti"] = [f.replace("PIANO_RISULTATO9_ATTESA.md", "PIANO_RISULTATO4.md")
                       for f in scheda.get("fonti", []) + r9.get("fonti", [])]
    return scheda


# ---------------------------------------------------------------- Risultato 6

R6_FILE = PROC / "risultato6_v2" / "mappa_r6.json"    # file unico della mappa (script 79, dati dello script 84)


def nome_pulito(n):
    """'RIVALTA DI TORINO' -> 'Rivalta di Torino', 'PORTA SUSA FS' -> 'Porta Susa FS'; gli altri nomi restano uguali."""
    if not n.isupper():
        return n
    return n.title().replace(" Di ", " di ").replace(" Fs", " FS")


R6_TONO_AREA = {"Critica": "rosso", "Scarsa": "arancio", "Buona": "verde"}


def date_it(iso_list):
    """['2026-10-15', '2026-10-16'] -> '15/10 e 16/10'"""
    giorni = [d[8:10] + "/" + d[5:7] for d in iso_list]
    if not giorni:
        return "—"
    return giorni[0] if len(giorni) == 1 else ", ".join(giorni[:-1]) + " e " + giorni[-1]


def scheda_r6():
    """Risultato 6 corretto (20/10/2026): legge mappa_r6.json (script 79 <- 84). Prima la scoperta misurata
    sugli interscambi del Comune, poi dove mancano posti prima di entrare in città, poi la verifica."""
    r = json.loads(R6_FILE.read_text(encoding="utf-8"))
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
            f"Ogni mattina entrano a Torino circa {migliaia(int(round(rie['M_cint'], -2)))} auto [STIMATO, IMQ 2022]; "
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
            "Fermate importanti: il 10% più alto di un punteggio fra i luoghi di fermata della Città metropolitana fuori "
            "dal centro (quartieri Q001-Q009): importanza della strada, corse nelle ore dei pendolari, auto in entrata che "
            "passano accanto, metro o stazione vicina, con pesi uguali.",
            "Auto in entrata che passano accanto: le auto che entrano a Torino al mattino (indagine IMQ 2022) fatte "
            "«guidare» sul percorso più veloce della rete stradale; si legge la strada più trafficata entro 100 m.",
            f"Auto da fermare = auto che passano × {quota_txt}% (chi già oggi lascia l'auto per un mezzo pubblico).",
            f"Posti adatti: parcheggi aperti fuori dal centro, con almeno 20 posti, non di ospedali, università o centri "
            f"commerciali, entro {raggio} m a piedi (linea d'aria × 1,3); posti dichiarati o stimati con 25 m² a posto.",
            "Punti prioritari (fino a 20, almeno 50 posti mancanti, uno per asse d'ingresso, oltre 3 km dal centro): fermate senza posti bastanti raggruppate entro 1 km, in "
            "ordine di posti che mancano.",
        ],
        "parametri": [["Centro escluso", "quartieri Q001-Q009 (fermate e parcheggi)"],
                      ["Fermate importanti", f"10% più alto ({migliaia(n_fermate)} su {migliaia(rie['n_eleggibili'])})"],
                      ["Distanza", f"{raggio} m a piedi (linea d'aria × 1,3)"],
                      ["Auto da fermare", f"auto che passano × {quota_txt}%"],
                      ["Posti stimati", "25 m² a posto (±30%)"],
                      ["Giorni feriali di riempimento", giorni]],
        "limiti": [
            "Auto che passano: modello del traffico (percorso più veloce, senza code), stima debole: solo ordine di grandezza. "
            "Le stesse auto passano davanti a più fermate dello stesso corso.",
            f"Riempimento misurato su soli {len(rie['giorni_feriali_validi'])} giorni feriali e solo dove il 5T lo trasmette "
            "[DATI SCARSI]: Fermi e i parcheggi gratuiti non sono misurati.",
            "Quota di chi lascia l'auto: indagine IMQ 2022, poche interviste.",
            "Parcheggi da OpenStreetMap incompleti; posti spesso stimati dalla superficie (±30%).",
            "Distanza a piedi stimata (linea d'aria × 1,3). Treni non considerati.",
        ],
        "criteri": r.get("criteri", []),
        "mappa": {"id": "interscambio", "tema": "Parcheggi per lasciare l'auto",
                  "nota": "Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."},
        "fonti": ["docs/RAPPORTO_R6_PARCHEGGI.txt", "docs/RAPPORTO_R6_AUTO_PASSAGGIO.txt",
                  "docs/RAPPORTO_R6_FERMATE_IMPORTANTI.txt", "docs/RAPPORTO_R6_PARCHEGGI_ADATTI.txt",
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
            "Limits: car flows come from a simple traffic model (order of magnitude only); occupancy is measured on "
            "few days and only where the city's 5T system reports it; trains are not included.",
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
    sens = leggi("traffico_d/v0/sensori.json")["sensori"]
    u, c, tar = r["universo_torino"], r["conteggi"], r["taratura"]
    km_poco = round(u["km"] - u["km_coperti_tp"], 1)
    err = v["varianti"]["v0"]
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
    fascia50, fascia90 = round(tar["fascia_50"] * 100), round(tar["fascia_90"] * 100)
    return {
        "risultato": "8",
        "titolo": "Traffico sulle strade e trasporto pubblico",
        "tag": "STIMATO / MISURATO / PROGRAMMATO",
        "stato": "Versione 1 (18/10/2026)",
        "in_breve": "Quante auto passano sulle strade grandi di Torino? E dove c'è tanto traffico ma nessun bus, "
                    "tram o metro comodo, così che l'auto resta l'unica scelta?",
        "domanda": "Sulle strade grandi di Torino, dove c'è molto traffico e poco trasporto pubblico vicino?",
        "numero_chiave": {"valore": round(u["quota_km_coperta_tp"] * 100, 1), "unita": "%",
                          "testo": f"dei km di strade grandi di Torino hanno fermate frequenti a pochi passi "
                                   f"({virgola(u['km_coperti_tp'])} km su {virgola(u['km'])})"},
        "racconto": "Una prima versione trovava 23 strade \"con molto traffico e poco trasporto pubblico\". "
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
            "entro 300 m). In più un tratto di Corso Moncalieri, coperto solo per un quarto della lunghezza.",
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
            {"tipo": "barre", "titolo": "Prova del modello sui 20 sensori: misurato e stimato",
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
            "Domanda: gli spostamenti in auto dell'indagine IMQ 2022 (residenti, giorno feriale), assegnati alla "
            "strada più veloce sulla rete di OpenStreetMap.",
            f"Taratura su {err['n']} punti di misura dei sensori 5T: un solo fattore per tutta la città, provato "
            "togliendo un sensore alla volta e stimandolo con gli altri.",
            "Strade come assi: un corso che cambia nome o comune resta la stessa strada, tagliata in tratte da "
            "300 m a 1,5 km. Strade grandi = Torino, importanza alta o strade principali, almeno 300 m, senza "
            "tangenziale e raccordi.",
            "Trasporto pubblico per posizione delle fermate, mai per nome: una tratta è servita dove c'è una "
            "fermata con almeno 4 passaggi all'ora entro 300 m (orario ufficiale, mercoledì 14/10), o la metro "
            "entro 600 m. Poco trasporto pubblico = servita per metà della lunghezza o meno.",
            "Molto traffico = il terzo più alto delle tratte. Un modello più ricco (attrazioni, code, ZTL) è stato "
            "provato una volta e non ha migliorato l'ordine delle strade: si tiene quello semplice.",
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
            "Solo i residenti tra 11 e 84 anni (indagine IMQ): mancano merci, turisti e chi viene da fuori. Il "
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
        "fonti": ["docs/PIANO_RISULTATO8.md", "docs/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt",
                  "docs/archivio/traffico/ESITO_FASE5_TRAFFICO.md", "data/processed/risultato8_traffico_tp_v2.json"],
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


# ---------------------------------------------------------------- Risultato 9

MIN_INTERVALLI_R9 = 2000   # sotto questa soglia un tipo di giorno non entra nella scheda (la domenica ne ha ~600)


def scheda_r9():
    r = leggi("risultato9_attesa.json")
    par = r["parametri"]
    nomi_tipo = {"0": "Feriale", "1": "Sabato", "2": "Domenica"}
    nomi_fasce = {"punta_mattina": "punta del mattino (7-9)", "giorno": "giorno (9-16)",
                  "punta_sera": "punta della sera (16-19)", "sera": "sera (19-24)",
                  "notte": "primo mattino (fino alle 7)"}
    fer = r["citta"]["0"]
    gps = r["controllo_gps"] or {}
    linee = sorted(((v["in_piu_min_bassa"], k, v) for k, v in r["linee"].get("0", {}).items()
                    if v["intervalli_osservati"] >= par["min_intervalli_classifica"]), reverse=True)[:10]
    scenari = []
    for t in ("0", "1", "2"):
        c = r["citta"].get(t)
        if not c or c["intervalli_osservati"] < MIN_INTERVALLI_R9:  # domenica: poche linee frequenti
            continue
        scenari.append({"nome": f"{nomi_tipo[t]} ({r['giorni'][t]} {'giorno' if r['giorni'][t] == 1 else 'giorni'})",
                        "numeri": [num("Attesa media alla fermata, stima bassa", c["reale_min_bassa"], "min",
                                       prima=c["promessa_min"]),
                                   num("Attesa media alla fermata, stima alta", c["reale_min_alta"], "min",
                                       prima=c["promessa_min"]),
                                   num("Corse programmate assenti dal feed", c["corse_assenti_feed_pct"], "%")]})
    scenari[0]["nota"] = "Prima = attesa promessa dall'orario, dopo = attesa reale stimata dai passaggi."
    sens = r["sensibilita_freq"]
    return {
        "risultato": "9",
        "titolo": "Quanto si aspetta davvero alla fermata",
        "tag": "MISURATO",
        "stato": f"Versione 1 ({r['periodo']['da'][8:10]}-{r['periodo']['a'][8:10]}/10/2026)",
        "in_breve": "L'orario promette un bus ogni pochi minuti. Se però i bus arrivano a coppie e poi lasciano un "
                    "buco, alla fermata si aspetta di più, anche se in un'ora ne passano tanti quanti promessi.",
        "domanda": "Sulle linee frequenti, quanti minuti in più aspetta in media chi arriva alla fermata senza "
                   "guardare l'orario, rispetto a quanto promette l'orario?",
        "numero_chiave": {"valore": fer["in_piu_min_bassa"], "unita": "min",
                          "testo": f"in più di attesa alla fermata nei giorni feriali (fino a "
                                   f"{virgola(fer['in_piu_min_alta'])}), su {virgola(fer['promessa_min'])} promessi"},
        "racconto": "Il risultato 4 contava quante coppie di bus arrivano a grappolo o lasciano un buco. Questo "
                    "risultato traduce quei numeri in minuti persi alla fermata, con la misura che usano le grandi "
                    "aziende di trasporto (Londra la pubblica come \"attesa in eccesso\").",
        "risposta": [
            f"Nei giorni feriali, sulle linee frequenti, l'orario promette un'attesa media di "
            f"{virgola(fer['promessa_min'])} minuti; quella reale è tra {virgola(fer['reale_min_bassa'])} e "
            f"{virgola(fer['reale_min_alta'])} minuti.",
            f"Sono da {virgola(fer['in_piu_min_bassa'])} a {virgola(fer['in_piu_min_alta'])} minuti in più a ogni "
            f"attesa: almeno {il(round(fer['in_piu_pct_bassa']))}% oltre la promessa.",
            f"La linea con più attesa in più è la {linee[0][1]} ({virgola(linee[0][0])} minuti in più, stima bassa)."
            if linee else "",
        ],
        "grafici": [
            {"tipo": "barre", "titolo": "Attesa media alla fermata per fascia oraria (feriale)", "unita": "min",
             "nota": "Barra chiara = attesa promessa, barra scura = attesa reale (stima bassa).",
             "voci": [voce(nomi_fasce[f], r["citta_fascia"]["0"][f]["reale_min_bassa"],
                           prima=r["citta_fascia"]["0"][f]["promessa_min"])
                      for f in ("punta_mattina", "giorno", "punta_sera", "sera") if r["citta_fascia"]["0"].get(f)]},
            {"tipo": "barre", "titolo": "Minuti in più di attesa, per fascia oraria (feriale)", "unita": "min",
             "forbice": True,
             "nota": "Barra chiara = stima bassa, barra scura = stima alta.",
             "voci": [voce(nomi_fasce[f], r["citta_fascia"]["0"][f]["in_piu_min_alta"],
                           prima=r["citta_fascia"]["0"][f]["in_piu_min_bassa"])
                      for f in ("punta_mattina", "giorno", "punta_sera", "sera") if r["citta_fascia"]["0"].get(f)]},
            {"tipo": "barre", "titolo": "Le 10 linee con più attesa in più (feriale, stima bassa)", "unita": "min",
             "nota": f"Solo linee con almeno {par['min_intervalli_classifica']} intervalli osservati.",
             "voci": [voce(f"linea {k}", round(v, 1)) for v, k, _ in linee]},
        ],
        "metodo": [
            "Per chi arriva alla fermata a caso, l'attesa media dipende da quanto sono regolari i passaggi: con gli "
            "intervalli h1, h2, ... è (h1² + h2² + ...) / (2 × (h1 + h2 + ...)). Bus ogni 10 minuti esatti: 5 minuti. "
            "Stessi due bus all'ora ma con intervalli di 2 e 18 minuti: 8,2 minuti.",
            "Attesa promessa = la formula sugli orari ufficiali (GTFS). Attesa reale = la formula sugli arrivi stimati "
            "dal feed GTT a ridosso della fermata (stessa lettura del risultato 4).",
            f"Solo linee frequenti: intervallo programmato medio di {int(par['freq_max_min'])} minuti o meno, per "
            "fermata, linea, verso e fascia oraria. Solo nelle ore in cui il Raspberry Pi stava raccogliendo.",
            "Corse che non compaiono nel feed: non si sa se sono saltate o solo non trasmesse, quindi due stime. "
            "Bassa: si usano solo i tratti senza corse mancanti. Alta: una corsa assente sia dal feed sia dal GPS "
            "conta come saltata.",
            "Media della città pesata sul numero di intervalli programmati (non ci sono dati sui passeggeri).",
        ],
        "parametri": [["Periodo", f"{r['periodo']['da']} - {r['periodo']['a']}"],
                      ["Linea frequente", f"intervallo medio ≤ {int(par['freq_max_min'])} min"],
                      ["Intervalli osservati (feriale)", migliaia(fer["intervalli_osservati"])],
                      ["Esclusi per dati scarsi", f"linea-fascia con più del {int(par['max_mancanti'] * 100)}% di corse assenti"],
                      ["Controllo col GPS", f"{gps.get('passaggi_confrontati', '-')} passaggi delle linee "
                                            f"{', '.join(gps.get('linee', []))}: differenza tipica "
                                            f"{virgola(gps.get('differenza_assoluta_mediana_min') or 0)} min"],
                      ["Soglia 10 / 15 min", f"in più {virgola(sens['10']['in_piu_min_bassa'])} / "
                                             f"{virgola(sens['15']['in_piu_min_bassa'])} min (stima bassa)"]],
        "limiti": [
            "Arrivi stimati dal feed GTT a ridosso della fermata, non visti sul posto; il controllo col GPS dei mezzi "
            f"dà una differenza tipica di {virgola(gps.get('differenza_assoluta_mediana_min') or 0)} minuti.",
            "Solo le linee urbane presenti nel feed; niente extraurbane e niente notte.",
            "Le corse mancanti rendono il risultato una forbice, non un numero solo.",
            "Vale per chi arriva alla fermata senza guardare orario o app: è il caso tipico delle linee frequenti, "
            "non di quelle rare (per quelle conta la puntualità, risultato 4).",
            "Pochi giorni (gli stessi del risultato 4, non tutti interi): va rifatto con più settimane di dati. "
            "La domenica le linee frequenti sono poche: troppo pochi dati per dare un numero.",
        ],
        "in_english": [
            "Question: on frequent lines, how many more minutes does a passenger who arrives at the stop without checking "
            "the timetable wait on average, compared with what the timetable promises?",
            f"On weekdays the timetable promises an average wait of {fer['promessa_min']:.1f} minutes; the real one is "
            f"between {fer['reale_min_bassa']:.1f} and {fer['reale_min_alta']:.1f} minutes. That is "
            f"{fer['in_piu_min_bassa']:.1f} to {fer['in_piu_min_alta']:.1f} minutes more per wait, at least "
            f"{round(fer['in_piu_pct_bassa']):,}% above the promise.",
            f"Limits: only {r['giorni']['0']} weekdays of data so far; real arrivals are estimated from the GTT feed, not "
            "seen at the stop; the night is not included.",
        ],
        "mappa": None,
        "fonti": ["docs/RAPPORTO_RISULTATO9_ATTESA.txt", "docs/PIANO_RISULTATO9_ATTESA.md",
                  "scripts/70_risultato9_attesa.py"],
        "generato": ora(),
        "avviso": [
            "Dati [MISURATO] — forbice per le corse mancanti",
            "Arrivi stimati dal feed GTT raccolto dal Raspberry Pi, solo linee urbane frequenti e ore con raccolta "
            "attiva. Stima bassa = solo tratti senza corse mancanti; stima alta = corse assenti da feed e GPS "
            "contate come saltate."
        ],
        "scenari": scenari,
    }


NASCOSTE = {"risultato2"}   # in pausa (Leo, 20/10/2026): docs/PIANO_RISULTATO2.md


def main():
    schede = []
    for nome, fabbrica in (("risultato1", scheda_r1), ("risultato2", None),
                           ("risultato4", scheda_r4), ("risultato6", scheda_r6),
                           ("risultato8", scheda_r8)):
        if nome in NASCOSTE:
            continue
        file = f"{nome}_riepilogo_mappa.json"
        if fabbrica is None:
            s = arricchisci_r2(leggi(file))  # il JSON di R2 resta quello dello script 29
        else:
            s = fabbrica()
            (PROC / file).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        s["_nome"] = file
        schede.append(s)
        print(f"{file}: {s['titolo']} - {sum(len(sc['numeri']) for sc in s['scenari'])} numeri, "
              f"{len(s.get('grafici', []))} grafici")
    OUT_JS.write_text("// generato da scripts/schede_risultati.py - non modificare a mano\n"
                      "window.SCHEDE_RISULTATI = " + json.dumps(schede, ensure_ascii=False, indent=1) + ";\n",
                      encoding="utf-8")
    print(f"scritto {OUT_JS.relative_to(RADICE)} con {len(schede)} schede")


if __name__ == "__main__":
    main()
