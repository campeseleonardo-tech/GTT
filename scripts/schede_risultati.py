"""Schede dei RISULTATI per simulazione.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_riepilogo_mappa.json   (Risultato 6, da 25)
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


def voce(label, valore, prima=None):
    v = {"label": label, "valore": valore}
    if prima is not None:
        v["prima"] = prima
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

def scheda_r1():
    vuoti = leggi("risultato1_vuoti.json")
    cand = leggi("risultato1_candidati.json")["gruppi"]
    testa = vuoti["numeri_di_testa"]
    gruppi = vuoti["gruppi"]
    ordine = sorted(gruppi, key=lambda g: -gruppi[g]["torino"]["zero"]["residenti"])
    senza = testa["residenti_torino_senza_almeno_un_servizio_essenziale_a_zero"]
    oggi = [num("Residenti senza almeno un servizio essenziale", senza, "residenti"),
            num("Quota dei residenti di Torino", testa["quota_residenti_torino"], "%")]
    oggi += [num(f"Senza {g} entro 15 min", gruppi[g]["torino"]["zero"]["residenti"], "residenti")
             for g in ordine]
    dopo, barre_dopo = [], []
    for g in ordine:
        c = cand[g]
        n_punti = len(c["candidati_scelti"])
        etichetta = f"{n_punti} {'punto nuovo' if n_punti == 1 else 'punti nuovi'}"
        dopo.append(num(f"Senza {g} ({etichetta})", c["residenti_restano_a_zero"], "residenti",
                        prima=c["residenti_a_zero_totali"]))
        barre_dopo.append(voce(f"{g} ({etichetta})", c["residenti_restano_a_zero"],
                               prima=c["residenti_a_zero_totali"]))
    salvati = sum(cand[g]["residenti_guadagnati_totali"] for g in ordine)
    return {
        "risultato": "1",
        "titolo": "Dove mancano i servizi a piedi",
        "tag": "STIMATO",
        "stato": "Fatto (12-14/10/2026)",
        "in_breve": "Torino è una città compatta, ma non tutti hanno scuola, medico, negozi di alimentari, "
                    "una fermata e un po' di verde a un quarto d'ora a piedi da casa.",
        "domanda": "Quanti residenti di Torino non hanno almeno un servizio essenziale (scuole, salute, cibo, "
                   "fermate, verde) entro 15 minuti a piedi, e quanti ne recupererebbe qualche servizio nuovo?",
        "numero_chiave": {"valore": senza, "unita": "residenti",
                          "testo": f"senza almeno un servizio essenziale a 15 minuti a piedi "
                                   f"({virgola(testa['quota_residenti_torino'])}% dei torinesi)"},
        "racconto": "Una delle domande da cui è partito il progetto: dove mancano i servizi? L'idea di "
                    "riferimento è la \"città dei 15 minuti\", in cui le cose di tutti i giorni si raggiungono "
                    "a piedi.",
        "risposta": [
            f"{migliaia(senza)} residenti su {migliaia(testa['residenti_torino'])} "
            f"({virgola(testa['quota_residenti_torino'])}%) non hanno almeno uno dei 5 servizi entro 15 minuti a piedi.",
            f"Il servizio che manca più spesso è la {testa['gruppo_piu_carente_a_torino']}: "
            f"{migliaia(gruppi[testa['gruppo_piu_carente_a_torino']]['torino']['zero']['residenti'])} residenti senza un servizio di questo tipo vicino.",
            f"Pochi servizi nuovi messi nei punti giusti (al massimo 5 per gruppo) riporterebbero "
            f"entro i 15 minuti {migliaia(salvati)} di questi casi, contati gruppo per gruppo.",
        ],
        "grafici": [
            {"tipo": "barre", "titolo": "Residenti di Torino senza il servizio entro 15 minuti a piedi",
             "unita": "residenti",
             "voci": [voce(g, gruppi[g]["torino"]["zero"]["residenti"]) for g in ordine]},
            {"tipo": "barre", "titolo": "Residenti con pochissimi servizi di quel tipo vicini",
             "unita": "residenti",
             "nota": "\"Pochissimi\" = sotto il livello che ha il 10% dei residenti meno servito (soglia per gruppo).",
             "voci": [voce(g, gruppi[g]["torino"]["pochissimo"]["residenti"]) for g in ordine]},
            {"tipo": "barre", "titolo": "Residenti senza il servizio: oggi e con i punti nuovi",
             "unita": "residenti", "nota": "Barra chiara = oggi, barra scura = con i punti nuovi.",
             "voci": barre_dopo},
        ],
        "metodo": [
            "Per ognuna delle 4.044 sezioni di censimento di Torino (centinaia di persone ciascuna) si contano "
            "i servizi raggiungibili camminando 15 minuti sulla rete stradale reale (OpenStreetMap), con il "
            "motore di percorsi R5.",
            "Cinque gruppi trattati separatamente, senza un indice unico: scuole, salute, cibo (attività "
            "commerciali del catalogo comunale), fermate del trasporto pubblico, verde.",
            "\"Senza\" = zero servizi di quel gruppo entro 15 minuti. I residenti vengono dal censimento ISTAT 2021.",
            "Fase B: per ogni gruppo si cercano fino a 5 punti (raggruppando le zone scoperte entro 400 m) che "
            "riportano dentro i 15 minuti più residenti possibile, uno dopo l'altro.",
        ],
        "parametri": [["Tempo a piedi", "15 minuti"], ["Velocità a piedi", "80 m al minuto (4,8 km/h)"],
                      ["Sezioni di Torino", "4.044"], ["Residenti", migliaia(testa["residenti_torino"])],
                      ["Punti nuovi per gruppo", "fino a 5"]],
        "limiti": [
            "Solo Torino: in cintura il catalogo dei servizi non c'è, quindi lì \"zero\" vuol dire spesso "
            "\"manca il dato\", non \"manca il servizio\".",
            "Il gruppo \"cibo\" usa tutte le attività commerciali del catalogo, senza distinguere la categoria.",
            "Si conta se un servizio c'è, non quanto è grande o se ha posto (una scuola piena conta come una vuota).",
            "I punti nuovi sono posizioni ipotetiche: non tengono conto di costi, spazi liberi o permessi, e "
            "non si sommano tra gruppi.",
        ],
        "mappa": {"tema": "Dove mancano i servizi",
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
             "nota": f"Il gruppo con più residenti scoperti è {testa['gruppo_piu_carente_a_torino']}."},
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
        "numero_chiave": {"valore": n15["residenti_migliorati"], "unita": "residenti",
                          "testo": "raggiungerebbero più servizi di notte con una metro ogni 15 minuti"},
        "racconto": "Uno dei problemi notati all'inizio del progetto: la metro chiude la sera. Dopo l'ultima corsa "
                    f"arriva un bus sostitutivo, poi dalle {da} alle {a} non c'è più niente sulla linea.",
        "risposta": [
            f"Con una metro ogni 15 minuti nel buco notturno, {migliaia(n15['residenti_migliorati'])} residenti "
            f"di Torino e cintura (su {migliaia(totale_res)}) raggiungerebbero più servizi entro 45 minuti.",
            f"Con una corsa ogni 30 minuti sarebbero {migliaia(n30['residenti_migliorati'])}: metà delle corse, "
            f"ma {il(round(100 * n30['residenti_migliorati'] / n15['residenti_migliorati']))}% dei residenti che ci guadagnano.",
            f"L'attesa media teorica alla fermata sarebbe di {virgola(n15['attesa_media_minuti'])} minuti nel primo "
            f"caso e {virgola(n30['attesa_media_minuti'])} nel secondo.",
        ],
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
                      voce("una corsa ogni 30 minuti", n30["residenti_migliorati"])]},
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
        "mappa": {"tema": "Accessibilità ai servizi",
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
    peggio_rit = sorted((x for x in linee if x[1]["passaggi"] >= par["min_passaggi"]),
                        key=lambda x: -x[1]["ritardo"])[:10]
    peggio_irr = sorted((x for x in linee if (x[1].get("coppie") or 0) >= par["min_coppie"]),
                        key=lambda x: -(x[1]["grappolo"] + x[1]["buco"]))[:10]
    nomi_fasce = {"punta_mattina": "punta del mattino (7-9)", "giorno": "giorno (9-16)",
                  "punta_sera": "punta della sera (16-19)", "sera": "sera (19-24)", "notte": "notte e primo mattino (fino alle 7, dati parziali)"}
    return {
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
                      voce("puntuali (da -1 a +5 min)", fer["puntuale"]),
                      voce("in ritardo (oltre 5 min)", fer["ritardo"])]},
            {"tipo": "barre", "titolo": "Passaggi in ritardo oltre 5 minuti, per fascia oraria (feriale)",
             "unita": "%", "voci": [voce(nomi_fasce.get(f, f), v) for f, _, v in fasce_r4()]},
            {"tipo": "barre", "titolo": "Passaggi in ritardo oltre 5 minuti, per tipo di giorno",
             "unita": "%", "voci": [voce(nomi[k].lower(), c[k]["ritardo"]) for k in ("0", "1", "2")]},
            {"tipo": "barre", "titolo": "Le 10 linee più in ritardo (feriale)", "unita": "%",
             "nota": f"Solo linee con almeno {par['min_passaggi']} passaggi osservati.",
             "voci": [voce(f"linea {n}", x["ritardo"]) for n, x in peggio_rit]},
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


# ---------------------------------------------------------------- Risultato 6

def scheda_r6():
    r = leggi("risultato6_interscambio.json")
    crit = [f for f in r["fermate"] if f["fermata_critica"]]
    coperte = sum(1 for f in crit if f["coperta"])
    scoperte = len(crit) - coperte
    inter = sorted((p for p in r["parcheggi"] if p["interscambio"]), key=lambda p: -p["critiche_entro_raggio"])
    raggio = round(r["raggio_copertura_m"])
    per_strada = Counter(f["corridoio"] for f in crit if not f["coperta"]).most_common(10)
    prime3 = "; ".join(f"{n}: {k}" for n, k in per_strada[:3])
    return {
        "risultato": "6",
        "titolo": "Parcheggi di interscambio",
        "tag": "STIMATO / PROGRAMMATO",
        "stato": "Versione 1 (14/10/2026)",
        "in_breve": "Chi arriva in auto dalla cintura dovrebbe poterla lasciare vicino a una fermata ben "
                    "servita. Le fermate più importanti hanno un parcheggio di interscambio a due passi?",
        "domanda": "Le fermate dove arriva più gente dalla cintura hanno un parcheggio di interscambio vicino?",
        "numero_chiave": {"valore": scoperte, "unita": "fermate",
                          "testo": f"critiche su {len(crit)} senza un parcheggio di interscambio entro {raggio} m"},
        "racconto": "Uno dei problemi notati all'inizio del progetto: al capolinea Fermi della metro, a Collegno, i "
                    "posti per lasciare l'auto sono pochi. Da lì la domanda si è allargata a tutta la città.",
        "risposta": [
            f"Fuori dal centro ci sono {len(crit)} fermate \"critiche\": solo {coperte} hanno un parcheggio di "
            f"interscambio entro {raggio} m, le altre {scoperte} no.",
            f"I parcheggi di interscambio sono {len(inter)}, con {migliaia(sum(p['posti'] for p in inter))} "
            "posti in tutto.",
            f"Le strade con più fermate critiche scoperte: {prime3}.",
        ],
        "grafici": [
            {"tipo": "pila", "titolo": f"Fermate critiche fuori dal centro: coperte e scoperte", "unita": "fermate",
             "voci": [voce(f"coperte (parcheggio entro {raggio} m)", coperte), voce("scoperte", scoperte)]},
            {"tipo": "barre", "titolo": f"I {len(inter)} parcheggi di interscambio: fermate critiche entro {raggio} m",
             "unita": "fermate",
             "voci": [voce(f"{p['nome'].title()} ({migliaia(p['posti'])} posti)", p["critiche_entro_raggio"])
                      for p in inter]},
            {"tipo": "barre", "titolo": "Strade con più fermate critiche scoperte", "unita": "fermate",
             "nota": "Strade raggruppate per nome (metodo della versione 1).",
             "voci": [voce(n, k) for n, k in per_strada]},
        ],
        "metodo": [
            "Ogni fermata GTT riceve un punteggio da 0 a 100: media di tre graduatorie, cioè quanto è "
            "importante la strada, quante corse passano nell'ora di punta (orario ufficiale) e quanti "
            "pendolari tra Torino e cintura ha la zona (indagine IMQ 2022).",
            "Critica = nel 10% più alto del punteggio. Le fermate del centro (zona IMQ Torino-Centro) non "
            "contano: un interscambio serve all'ingresso in città, non in centro.",
            f"Coperta = un parcheggio di interscambio entro {raggio} m in linea d'aria. Elenco dei parcheggi dal "
            "feed 5T, con l'etichetta \"interscambio\" presa dal Comune.",
        ],
        "parametri": [["Fermate analizzate", migliaia(len(r["fermate"]))], ["Soglia critica", "10% più alto"],
                      ["Raggio di copertura", f"{raggio} m in linea d'aria"],
                      ["Zone escluse", ", ".join(r["zone_escluse"]) + " (centro)"],
                      ["Giorno dell'orario", r["giorno_tipo"]]],
        "limiti": [
            f"{raggio} m in linea d'aria, non a piedi lungo le strade.",
            "I pendolari sono stimati per zona (indagine IMQ), non contati alla fermata.",
            "Le strade sono raggruppate per nome: è un metodo che il lavoro sul traffico ha mostrato debole "
            "(una strada che cambia nome si spezza).",
            "Non dice ancora quanto si riempiono i parcheggi: la raccolta dei posti liberi è partita il 14/10 "
            "e servirà per la versione 2.",
        ],
        "mappa": None,
        "fonti": ["docs/RAPPORTO_RISULTATO6.txt", "docs/PIANO_RISULTATO6.md", "scripts/25_risultato6_interscambio.py"],
        "generato": ora(),
        "avviso": [
            "Dati [STIMATO] / [PROGRAMMATO] — versione 1",
            f"Fermata 'critica' = nel 10% più alto per strada importante, corse in punta e pendolari stimati "
            f"della zona (IMQ); centro escluso. Copertura = parcheggio entro {raggio} m in linea d'aria. "
            "Quanto si riempiono i parcheggi non è ancora misurato (versione 2, con i dati raccolti dal 14/10)."
        ],
        "scenari": [{
            "nome": "Oggi",
            "numeri": [
                num("Fermate critiche fuori dal centro", len(crit), "fermate"),
                num(f"Coperte da un interscambio entro {raggio} m", coperte, "fermate"),
                num("Scoperte", scoperte, "fermate"),
                num("Parcheggi di interscambio", len(inter), "parcheggi"),
                num("Posti negli interscambi", sum(p["posti"] for p in inter), "posti"),
            ],
            "nota": f"Strade con più fermate critiche scoperte: {prime3}.",
        }],
    }


def main():
    schede = []
    for nome, fabbrica in (("risultato1", scheda_r1), ("risultato2", None),
                           ("risultato4", scheda_r4), ("risultato6", scheda_r6)):
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
