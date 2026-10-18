"""Schede dei RISULTATI per simulazione.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_riepilogo_mappa.json   (Risultato 6, da 25)
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
             "voci": [voce("con fermate frequenti vicine", round(u["km_coperti_tp"], 1)),
                      voce("con poco trasporto pubblico", km_poco)]},
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
        "mappa": None,
        "fonti": ["docs/ESITO_FASE5_TRAFFICO.md", "docs/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt",
                  "docs/PIANO_TRAFFICO_FASE5.md", "data/processed/risultato8_traffico_tp_v2.json"],
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


def main():
    schede = []
    for nome, fabbrica in (("risultato1", scheda_r1), ("risultato2", None),
                           ("risultato4", scheda_r4), ("risultato6", scheda_r6),
                           ("risultato8", scheda_r8), ("risultato9", scheda_r9)):
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
