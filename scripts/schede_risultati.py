"""Schede dei RISULTATI per risultati.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_v2/mappa_r6.json   (Risultato 6, da 79 e 84) -> data/processed/risultato6_riepilogo_mappa.json
  data/processed/risultato8_riepilogo_mappa.json   (Risultato 8, dalla Fase 5 del traffico, script 56-67)
  data/schede_risultati.js   (tutte le schede, R2 compreso, caricate da sole da risultati.html)

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
e semplici somme/conteggi su di essi.
"""
import json
from urllib.parse import quote
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


def voce(label, valore, prima=None, tono=None, link=None):
    v = {"label": label, "valore": valore}
    if link is not None:   # la barra e' un link (es. alla linea nella mappa)
        v["link"] = link
    if prima is not None:
        v["prima"] = prima
    if tono is not None:   # "verde"/"rosso" = bene/male; senza tono = blu neutro (quantità)
        v["tono"] = tono
    return v


def migliaia(n):
    return f"{n:,}".replace(",", ".")


def virgola(x):
    testo = f"{x:.1f}".replace(".", ",")
    return testo[:-2] if testo.endswith(",0") else testo


def pct2(x):
    """percentuale con due decimali e virgola (per valori piccoli, es. 'oltre 10 minuti')."""
    return f"{x:.2f}".replace(".", ",")


def link_linea(nome):
    """Link dalla scheda alla mappa con quella linea selezionata (tema «Puntualita' delle linee»)."""
    return "mappa_torino.html#tema=puntualita&linea=" + quote(str(nome), safe="") + "&ora=8"   # si apre alle 8 di un feriale


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
        "stato": "Chiuso",
        "in_breve": f"La metro M1 non passa dalle {da} alle {a}: in quelle ore restano solo i bus notturni.",
        # numero in grande: quello severo (almeno +soglia_quota di servizi)
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
        "fonti": ["docs/R2_metro_notte.md", "docs/rapporti/RAPPORTO_RISULTATO2_METRO_NOTTE.txt",
                  "scripts/28_scenario_metro_notte.py", "scripts/29_risultato2_metro_notte.py"],
    })
    return s


# ---------------------------------------------------------------- Risultato 4

def fasce_r4():
    """Tabella 'fasce orarie (feriale)' del rapporto dello script 27 (non e' nel JSON)."""
    testo = (DOCS / "rapporti" / "RAPPORTO_RISULTATO4.txt").read_text(encoding="utf-8")
    blocco = testo.split("fasce orarie (feriale")[1].split("\n\n")[0]
    righe = []
    for riga in blocco.splitlines():
        m = re.match(r"\s*([a-z_]+)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)", riga)
        if m:
            righe.append((m.group(1), int(m.group(2)), float(m.group(5))))
    return righe


# GTT: passaggi bus e tram in ritardo oltre 10 minuti nel 2025, 2,3% (rapporto di sostenibilita' GTT 2025, p. 128;
# sintesi in docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md). Costante: non esce da nessun nostro calcolo.
GTT_RITARDO10_2025_PCT = 2.3
DEF_R4 = (("a", "a ogni fermata"), ("b", "solo alla prima fermata"), ("c", "solo a metà corsa"), ("d", "fuori dalle ore di punta"))


# copertura verificata su trip_update_gtt (ore 06-24 con almeno 50 minuti letti)
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
                *([num("Passaggi in ritardo oltre 10 min", x["ritardo10"], "%")] if "ritardo10" in x else []),
            ],
        })
    scenari[0]["nota"] = ("Molti passaggi risultano in anticipo perché l'orario ufficiale ha margini; "
                          "un ritardo mediano negativo vuol dire 'di solito un po' prima'.")
    s = r["scarti"]
    fer = c["0"]
    # dal Giro 5 gli arrivi sono del GPS; il feed resta solo come confronto (JSON: confronto_feed, copertura_gps, regole_gps)
    cf = r["confronto_feed"]
    cf_fer = cf["citta"]["0"]
    cop_gps = r["copertura_gps"]["totale"]
    dist_gps = int(r["regole_gps"]["dist_gps_m"])
    linee = [(nome, v["0"]) for nome, v in r["linee"].items() if "0" in v]
    peggio_rit = sorted((x for x in linee if x[1]["passaggi"] >= par.get("min_passaggi_classifica", 2000) and str(x[0]).isdigit()),
                        key=lambda x: -x[1]["ritardo"])[:10]
    peggio_irr = sorted((x for x in linee if (x[1].get("coppie") or 0) >= par["min_coppie"] and str(x[0]).isdigit()),
                        key=lambda x: -(x[1]["grappolo"] + x[1]["buco"]))[:10]
    nomi_fasce = {"punta_mattina": "punta del mattino (7-9)", "giorno": "giorno (9-16)",
                  "punta_sera": "punta della sera (16-19)", "sera": "sera (19-24)", "notte": "notte e primo mattino (fino alle 7, dati parziali)"}
    modi = r.get("modi") or {}
    tram_f, bus_f = (modi.get("tram") or {}).get("0"), (modi.get("bus") or {}).get("0")
    utili = (r.get("linee_utili") or {}).get("0")
    # classifica per ritardo a fine corsa (mediana, minuti); i minuti ogni 10 km restano nella nota
    fine_corsa = sorted(((x["fine_corsa"]["ritardo_mediana"], n, x) for n, x in linee
                         if x.get("fine_corsa") and x["fine_corsa"]["passaggi"] >= par.get("min_fine_corsa", 100)
                         and str(n).isdigit()), key=lambda t: (-t[0], -t[2]["fine_corsa"]["min_per_10km"]))[:10]
    rif10 = par.get("rif_gtt_ritardo10_pct")
    cg = r.get("confronto_gtt")      # B1: 4 definizioni di «oltre 10 minuti» (script 27), mai scritte a mano
    grafici_nuovi, righe_gtt, righe_gtt_en = [], [], []
    if cg:
        dd = cg["definizioni"]
        sett = {k: dd[k]["settimana"]["ritardo10_pct"] for k, _ in DEF_R4}
        fer10 = {k: dd[k]["per_tipo"]["0"]["ritardo10_pct"] for k, _ in DEF_R4}
        grafici_nuovi.append({
            "tipo": "barre", "titolo": "Noi e GTT: passaggi in ritardo oltre 10 minuti", "unita": "%",
            "nota": f"Barre = media della settimana (feriale 5 : sabato 1 : domenica 1). Nei feriali: a ogni fermata {pct2(fer10['a'])}%, "
                    f"alla prima fermata {pct2(fer10['b'])}%, a metà corsa {pct2(fer10['c'])}%, fuori punta {pct2(fer10['d'])}%. "
                    f"GTT: anno 2025, tutte le linee, metodo non pubblicato.",
            "voci": [voce("GTT (2025, anno intero)", GTT_RITARDO10_2025_PCT)]
                    + [voce(f"noi, {nome}", sett[k], tono="rosso") for k, nome in DEF_R4]})
        basso, alto = min([GTT_RITARDO10_2025_PCT] + list(sett.values())), max(sett.values())
        righe_gtt = [
            "Non è la stessa misura: GTT fa la media dell'anno intero, estate e sere comprese, su tutte le linee, con un metodo che non pubblica; "
            "noi misuriamo pochi giorni di ottobre, solo le linee urbane, dalle 5 a mezzanotte.",
            f"{'Il ritardo cresce lungo la corsa: ' if sett['b'] < sett['a'] else ''}alla prima fermata è {pct2(sett['b'])}%, "
            f"a metà corsa {pct2(sett['c'])}%, a ogni fermata {pct2(sett['a'])}%, fuori dalle ore di punta {pct2(sett['d'])}% (media della settimana).",
            f"Tutte e due le misure dicono che i ritardi gravi sono una piccola parte dei passaggi: tra {virgola(basso)}% e {virgola(alto)}%.",
        ]
        righe_gtt_en = [
            f"Why our number differs from GTT's {GTT_RITARDO10_2025_PCT}% (more than 10 minutes late, 2025): GTT averages the whole year on all lines with "
            f"an unpublished method; we measure a few October days on urban lines. At the first stop of the trip we get {sett['b']:.2f}%, "
            f"at every stop {sett['a']:.2f}% (weekly average)."]
    if tram_f and bus_f:
        grafici_nuovi.append({
            "tipo": "barre", "titolo": "Tram contro bus (feriale)", "unita": "%",
            "nota": f"Tram: {migliaia(tram_f['passaggi'])} passaggi; bus: {migliaia(bus_f['passaggi'])}.",
            "voci": [voce("tram: in ritardo oltre 5 min", tram_f["ritardo"], tono="rosso"),
                     voce("bus: in ritardo oltre 5 min", bus_f["ritardo"], tono="rosso"),
                     voce("tram: in ritardo oltre 10 min", tram_f["ritardo10"], tono="rosso"),
                     voce("bus: in ritardo oltre 10 min", bus_f["ritardo10"], tono="rosso"),
                     voce("tram: a grappolo o con un buco", round(tram_f["grappolo"] + tram_f["buco"], 1)),
                     voce("bus: a grappolo o con un buco", round(bus_f["grappolo"] + bus_f["buco"], 1))]})
    if fine_corsa:
        grafici_nuovi.append({
            "tipo": "barre", "titolo": "Ritardo a fine corsa (feriale)", "unita": "min",
            "nota": f"Ritardo mediano alle ultime {par.get('fine_corsa_ultime_fermate', 3)} fermate della corsa, in minuti. "
                    f"Solo linee ordinarie con almeno {par.get('min_fine_corsa', 100)} passaggi di fine corsa. "
                    "I minuti ogni 10 km (ritardo diviso la lunghezza della corsa) sono nel rapporto: per km le linee corte vengono premiate. "
                    "Clicca una linea per vederla nella mappa: la mappa si apre alle 8 di un feriale.",
            "voci": [voce(f"linea {n} ({virgola(x['fine_corsa']['min_per_10km'])} min ogni 10 km)", val, tono="rosso", link=link_linea(n))
                     for val, n, x in fine_corsa]})
    if utili:
        grafici_nuovi.append({
            "tipo": "barre", "titolo": "Linee utili contro altre (feriale)", "unita": "%",
            "nota": f"Linee utili = le {r.get('n_linee_utili')} che toccano più delle zone dove arriva più gente per km² "
                    f"(Risultato 6). Passaggi: {migliaia(utili['utili']['passaggi'])} sulle utili, {migliaia(utili['altre']['passaggi'])} sulle altre.",
            "voci": [voce("linee utili: in ritardo oltre 5 min", utili["utili"]["ritardo"], tono="rosso"),
                     voce("altre linee: in ritardo oltre 5 min", utili["altre"]["ritardo"], tono="rosso"),
                     voce("linee utili: a grappolo o con un buco", utili["utili"]["grappolo_buco"]),
                     voce("altre linee: a grappolo o con un buco", utili["altre"]["grappolo_buco"])]})
    scheda = {
        "risultato": "4",
        "titolo": "Bus in ritardo e bus irregolari",
        "tag": "MISURATO",
        "stato": "Versione 2",
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
            f"Il feed in tempo reale di GTT, che usavamo prima, dava il {virgola(cf_fer['ritardo'])}% in ritardo invece del "
            f"{virgola(fer['ritardo'])}%: smette di aggiornare la fermata all'orario previsto e così sottostima i ritardi.",
            *([f"Oltre 10 minuti: {pct2(fer['ritardo10'])}% nei feriali. GTT dichiara il {virgola(rif10)}% per il 2025: "
               "il suo metodo non è pubblicato; noi misuriamo a ogni fermata con il GPS, su pochi giorni."]
              if "ritardo10" in fer and rif10 is not None else []),
            *righe_gtt,
            *([f"Tram e bus: in ritardo oltre 5 minuti {il(tram_f['ritardo'])}% dei passaggi dei tram e {il(bus_f['ritardo'])}% "
               f"dei bus (feriale)."] if tram_f and bus_f else []),
            *([f"Linee utili (quelle che toccano più zone affollate): in ritardo oltre 5 minuti {il(utili['utili']['ritardo'])}% dei passaggi, "
               f"contro {il(utili['altre']['ritardo'])}% delle altre linee (feriale)."] if utili else []),
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
             "nota": f"Solo linee ordinarie (nome di sole cifre) con almeno {par.get('min_passaggi_classifica', 2000)} passaggi osservati. "
                     "Clicca una linea per vederla nella mappa.",
             "voci": [voce(f"linea {n}", x["ritardo"], tono="rosso", link=link_linea(n)) for n, x in peggio_rit]},
            {"tipo": "barre", "titolo": "Le 10 linee più irregolari (feriale): grappolo + buco", "unita": "%",
             "nota": f"Solo linee frequenti (un mezzo ogni {int(par['freq_max_min'])} minuti o meno) con almeno "
                     f"{par['min_coppie']} coppie osservate. Clicca una linea per vederla nella mappa.",
             "voci": [voce(f"linea {n}", round(x["grappolo"] + x["buco"], 1), link=link_linea(n)) for n, x in peggio_irr]},
            *grafici_nuovi,
        ],
        "metodo": [
            "Il Raspberry Pi registra ogni minuto le posizioni GPS dei mezzi GTT.",
            f"Per ogni corsa e fermata si prende l'istante in cui il GPS del mezzo passa a meno di {dist_gps} metri dalla "
            "fermata e lo si confronta con l'orario ufficiale (GTFS).",
            "Classi: in anticipo sotto -1 minuto, puntuale da -1 a +5, in ritardo oltre +5.",
            "Regolarità: per due mezzi consecutivi della stessa linea alla stessa fermata, \"grappolo\" se "
            "l'intervallo vero è meno della metà di quello previsto, \"buco\" se è più del doppio. Solo linee "
            "con un mezzo ogni 15 minuti o meno.",
        ],
        "parametri": [["Periodo", f"{r['periodo']['da']} - {r['periodo']['a']}"],
                      ["Passaggi con GPS valido", f"{migliaia(s['usati'])} ({virgola(cop_gps['copertura_pct'])}% di quelli programmati dalle corse viste)"],
                      ["Soglia ritardo", f"{virgola(par['soglia_ritardo_min'])} min"],
                      ["Soglia anticipo", f"{virgola(par['soglia_anticipo_min'])} min"],
                      ["Distanza dalla fermata", f"entro {dist_gps} m"]],
        "limiti": [
            f"Pochi giorni ({r['giorni']['0']} feriali, {r['giorni']['1']} sabati, {r['giorni']['2']} domeniche), "
            f"e non tutti interi: {GIORNI_PARZIALI_R4}. Ogni giorno conta con le ore che hanno dati.",
            "La raccolta si ferma a mezzanotte e riparte verso le 5: la notte non è misurata.",
            "Il GPS copre solo le linee urbane (circa 90): le extraurbane non ci sono mai. Anche sulle linee "
            "coperte alcune corse non sono mai viste dal GPS: se erano saltate davvero, la puntualità reale è peggiore "
            "e i buchi sono più di quelli contati.",
            f"Il GPS c'è per circa il {round(cop_gps['copertura_pct'])}% dei passaggi delle corse viste; "
            "le corse mai viste dal GPS non si contano.",
            f"Distanza di {dist_gps} metri dalla fermata: un mezzo fermo poco prima conta come arrivato poco dopo.",
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
            f"Arrivals are now measured with the vehicles' GPS; the GTT real-time feed we used before gave {cf_fer['ritardo']:.1f}% "
            f"late instead of {fer['ritardo']:.1f}% because it stops updating a stop at its scheduled time, so it underestimates delays.",
            *([f"More than 10 minutes late: {fer['ritardo10']:.2f}% of weekday departures. GTT reports {rif10}% for 2025: "
               "its method is not published; we measure at every stop with GPS, over a few days."]
              if "ritardo10" in fer and rif10 is not None else []),
            *righe_gtt_en,
            *([f"Trams vs buses (weekdays): {tram_f['ritardo']:.1f}% of tram departures and {bus_f['ritardo']:.1f}% of bus departures "
               "are more than 5 minutes late."] if tram_f and bus_f else []),
            *([f"Delay at the end of the trip (median, last stops): highest on line {fine_corsa[0][1]} ({fine_corsa[0][0]:.1f} minutes)."]
              if fine_corsa else []),
            *([f"Useful lines (touching the busiest zones per km2): {utili['utili']['ritardo']:.1f}% of departures more than 5 minutes late, "
               f"other lines {utili['altre']['ritardo']:.1f}% (weekdays)."] if utili else []),
        ],
        "mappa": {"id": "puntualita", "tema": "Puntualità delle linee",
                  "nota": "Nella mappa, tema «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."},
        "fonti": ["docs/R4_puntualita.md", "docs/rapporti/RAPPORTO_RISULTATO4.txt", "scripts/27_risultato4_regolarita.py"],
        "generato": ora(),
        "avviso": [
            "Dati [MISURATO] — pochi giorni",
            f"Arrivi misurati con il GPS dei mezzi GTT raccolto dal Raspberry Pi, {r['periodo']['da']} - {r['periodo']['a']}: "
            f"il GPS c'è per il {round(cop_gps['copertura_pct'])}% dei passaggi programmati delle corse viste (prima si usava il feed GTT, "
            "che sottostima i ritardi: confronto nella scheda). Giorni non tutti interi e solo linee urbane viste dal GPS: vedi i limiti."
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
    modi9 = (leggi("risultato9_attesa.json").get("modi") or {}).get("0") or {}
    if modi9.get("tram") and modi9.get("bus"):
        t9, b9 = modi9["tram"], modi9["bus"]
        scheda["risposta"] = scheda["risposta"] + [
            f"Attesa alla fermata sulle linee frequenti (feriale): tram, promessa {virgola(t9['promessa_min'])} min, in più "
            f"{virgola(t9['in_piu_min_bassa'])}-{virgola(t9['in_piu_min_alta'])} min; bus, promessa {virgola(b9['promessa_min'])} min, "
            f"in più {virgola(b9['in_piu_min_bassa'])}-{virgola(b9['in_piu_min_alta'])} min."]
        scheda["in_english"] = scheda["in_english"] + [
            f"Waiting time on frequent lines (weekdays): trams promise {t9['promessa_min']:.1f} min, {t9['in_piu_min_bassa']:.1f}-"
            f"{t9['in_piu_min_alta']:.1f} min more in reality; buses {b9['promessa_min']:.1f} min, {b9['in_piu_min_bassa']:.1f}-"
            f"{b9['in_piu_min_alta']:.1f} min more."]
    scheda["fonti"] = ["docs/R4_puntualita.md"] + [f for f in scheda.get("fonti", []) + r9.get("fonti", []) if f != "docs/R4_puntualita.md"]
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
    """Risultato 6 corretto: legge mappa_r6.json (script 79 <- 84). Prima la scoperta misurata
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
    reg = rie["regola_fermate"]                      # N e M dallo script 83, via 84
    n_corse, m_auto = reg["n_corse"], migliaia(reg["m_auto"])
    regola_txt = (f"fuori dal centro, con metro, stazione o capolinea oppure almeno {n_corse} corse all'ora nelle ore dei "
                  f"pendolari, e con almeno {m_auto} auto in entrata che passano accanto")
    sens_file = R6_FILE.parent / "confronto_sensori.json"
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
            f"Fermate importanti: fra i luoghi di fermata della Città metropolitana, quelle {regola_txt} "
            "(centro = quartieri Q001-Q009). Regola fissa; il punteggio (importanza della strada, corse, auto, metro o "
            "stazione, pesi uguali) serve solo per l'ordine.",
            "Auto in entrata che passano accanto: le auto che entrano a Torino al mattino (indagine IMQ 2022) fatte "
            "«guidare» sul percorso più veloce della rete stradale; si legge la strada più trafficata entro 100 m.",
            f"Auto da fermare = auto che passano × {quota_txt}% (chi già oggi lascia l'auto per un mezzo pubblico).",
            f"Posti adatti: parcheggi aperti fuori dal centro, con almeno 20 posti, non di ospedali, università o centri "
            f"commerciali, entro {raggio} m a piedi (linea d'aria × 1,3); posti dichiarati o stimati con 25 m² a posto.",
            "Punti prioritari (fino a 20, almeno 50 posti mancanti, uno per asse d'ingresso, oltre 3 km dal centro): fermate senza posti bastanti raggruppate entro 1 km, in "
            "ordine di posti che mancano.",
        ],
        "parametri": [["Centro escluso", "quartieri Q001-Q009 (fermate e parcheggi)"],
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
            "Quota di chi lascia l'auto: indagine IMQ 2022, poche interviste.",
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
        "stato": "Versione 1",
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
                                   num("Corse programmate assenti dal GPS", c["corse_assenti_feed_pct"], "%")]})
    scenari[0]["nota"] = "Prima = attesa promessa dall'orario, dopo = attesa reale stimata dai passaggi."
    sens = r["sensibilita_freq"]
    return {
        "risultato": "9",
        "titolo": "Quanto si aspetta davvero alla fermata",
        "tag": "MISURATO",
        "stato": "Versione 1",
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
            "Attesa promessa = la formula sugli orari ufficiali (GTFS). Attesa reale = la formula sugli arrivi misurati "
            "con il GPS dei mezzi (stessa misura del risultato 4).",
            f"Solo linee frequenti: intervallo programmato medio di {int(par['freq_max_min'])} minuti o meno, per "
            "fermata, linea, verso e fascia oraria. Solo nelle ore in cui il Raspberry Pi stava raccogliendo.",
            "Corse che non compaiono nel GPS: non si sa se sono saltate o solo non trasmesse, quindi due stime. "
            "Bassa: si usano solo i tratti senza corse mancanti. Alta: una corsa assente dal GPS "
            "conta come saltata.",
            "Media della città pesata sul numero di intervalli programmati (non ci sono dati sui passeggeri).",
        ],
        "parametri": [["Periodo", f"{r['periodo']['da']} - {r['periodo']['a']}"],
                      ["Linea frequente", f"intervallo medio ≤ {int(par['freq_max_min'])} min"],
                      ["Intervalli osservati (feriale)", migliaia(fer["intervalli_osservati"])],
                      ["Esclusi per dati scarsi", f"linea-fascia con più del {int(par['max_mancanti'] * 100)}% di corse assenti"],
                      ["Controllo del feed col GPS", f"{gps.get('passaggi_confrontati', '-')} passaggi delle linee "
                                            f"{', '.join(gps.get('linee', []))}: differenza tipica "
                                            f"{virgola(gps.get('differenza_assoluta_mediana_min') or 0)} min"],
                      ["Soglia 10 / 15 min", f"in più {virgola(sens['10']['in_piu_min_bassa'])} / "
                                             f"{virgola(sens['15']['in_piu_min_bassa'])} min (stima bassa)"]],
        "limiti": [
            "Arrivi misurati con il GPS dei mezzi (a meno di 60 metri dalla fermata); il vecchio feed GTT, controllato col GPS, "
            f"dava una differenza tipica di {virgola(gps.get('differenza_assoluta_mediana_min') or 0)} minuti.",
            "Solo le linee urbane viste dal GPS; niente extraurbane e niente notte.",
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
            f"Limits: only {r['giorni']['0']} weekdays of data so far; real arrivals are measured with the vehicles' GPS "
            "(within 60 metres of the stop); the night is not included.",
        ],
        "mappa": None,
        "fonti": ["docs/rapporti/RAPPORTO_RISULTATO9_ATTESA.txt", "docs/R4_puntualita.md",
                  "scripts/70_risultato9_attesa.py"],
        "generato": ora(),
        "avviso": [
            "Dati [MISURATO] — forbice per le corse mancanti",
            "Arrivi misurati con il GPS dei mezzi raccolto dal Raspberry Pi, solo linee urbane frequenti e ore con raccolta "
            "attiva. Stima bassa = solo tratti senza corse mancanti; stima alta = corse assenti dal GPS "
            "contate come saltate."
        ],
        "scenari": scenari,
    }


NASCOSTE = {"risultato2"}   # in pausa: docs/R2_metro_notte.md


# ---------------------------------------------------------------- Forma nuova delle schede (PIANO_SCHEDE.md)
# Ogni scheda ha un campo "forma" con tutto quello che la pagina mostra: etichetta, titolo-risposta, domanda in una riga,
# numero grande, grafico principale, 3 punti chiave, e le parti chiuse (altri grafici, calcolo, limiti, inglese).
# I campi vecchi restano nel JSON ma la pagina non li usa. I numeri vengono sempre dai file dei risultati.

PAROLE_VIETATE = re.compile(r"\bLeo\b|\bgiro\b|\bfase\b|\bversione\b|\.py\b|\.json\b|\.md\b|\bIMQ\b|\bQ00\d|\b5T\b|\bGTFS\b", re.I)


def controlla_forma(nome, f):
    """Avvisi sui testi della forma: frasi di oltre 20 parole e parole che non vanno nelle pagine."""
    testi = [f["titolo"], f["domanda"], f["numero"]["testo"], *f["punti"], *f["calcolo"], *f.get("confronto", []),
             *f["limiti"], *f["english"], *(a for a in [f.get("extra", {}).get("punto")] if a)]
    for t in testi:
        if PAROLE_VIETATE.search(t):
            print(f"  ATTENZIONE {nome}: parola da togliere in «{t[:60]}»")
        for frase in re.split(r"(?<=[a-zA-ZàèéìòùÀ%)\]»])[.;:] +(?=[A-ZÈÀ])", t):
            if len(frase.split()) > 20:
                print(f"  ATTENZIONE {nome}: frase di {len(frase.split())} parole: «{frase[:70]}…»")
    if len(f["punti"]) != 3 or len(f["limiti"]) > 4 or len(f["altri"]) > 2 or len(f["english"]) != 3 or len(f["calcolo"]) > 5:
        print(f"  ATTENZIONE {nome}: numero di righe fuori misura")


def forma_base(s, titolo, domanda, numero, principale, punti, altri, calcolo, criteri, limiti, english, mappa=True, **extra):
    f = {"etichetta": s["tag"], "titolo": titolo, "domanda": domanda, "numero": numero, "principale": principale,
         "punti": punti, "altri": altri, "calcolo": calcolo, "criteri": criteri, "limiti": limiti, "english": english}
    if mappa and s.get("mappa"):
        f["mappa"] = {"id": s["mappa"]["id"], "nota": s["mappa"]["nota"]}
    f.update(extra)
    return f


def grafico_per_titolo(s, inizio):
    return next(g for g in s["grafici"] if g["titolo"].startswith(inizio))


def numero_di(s, label_inizio, scenario=0):
    return next(n for n in s["scenari"][scenario]["numeri"] if n["label"].startswith(label_inizio))["dopo"]


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
                                f"{migliaia(pr['soglia_molto_traffico_veic_giorno'])} veicoli al giorno. "
                                f"Stima debole: il modello sbaglia del ±{pr['fascia_errore_pct']}% in metà dei casi.",
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
               f"Si è esposti se il centro della sezione è a meno di {raggio} m da una strada molto trafficata."]
    parametri = [["Tempi a piedi", "5, 10 e 15 minuti"] if p[0] == "Tempo a piedi" else list(p) for p in s["parametri"]]
    parametri += [["Strada molto trafficata", f"almeno {migliaia(pr['soglia_molto_traffico_veic_giorno'])} veicoli al giorno"],
                  ["Esposto al traffico", f"a meno di {raggio} m dalla strada"]]
    return forma_base(
        s,
        "A 15 minuti quasi tutti hanno i servizi; a 5 minuti molti meno",
        "Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata?",
        {"valore": round(quota(15, 5), 1), "unita": "%",
         "testo": "dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi"},
        principale,
        [f"A 5 minuti solo {il(quota(5, 5))}% dei residenti ha tutti e 5 i servizi; a 10 minuti {il(quota(10, 5))}%.",
         f"{migliaia(classi['esposta']['residenti'])} residenti ({virgola(classi['esposta']['quota'])}%) vivono a meno di "
         f"{raggio} m da una strada molto trafficata.",
         f"I {migliaia(tre_o_piu)} residenti senza 3 o più servizi sono in {n_critiche} {'sezione' if n_critiche == 1 else 'sezioni'} di collina: dove manca davvero tutto."],
        [grafico_traffico, grafico_senza],
        calcolo,
        parametri,
        ["Solo Torino: in cintura il catalogo dei servizi manca, quindi «zero» spesso vuol dire dato mancante.",
         "Si conta se un servizio c'è, non quanto è grande né se ha posto. Le fermate usano l'orario programmato: niente ritardi né affollamento.",
         "I punti nuovi sono ipotesi: non tengono conto di costi, spazi liberi o permessi.",
         "Il traffico è una stima e sostituisce rumore e smog, che non misuriamo."],
        ["Question: how many Turin residents lack schools, health, shops, stops or green space within 15 minutes on foot?",
         f"Answer: {senza:,} residents ({quota_senza:.1f}%) lack at least one of the 5 services; {tre_o_piu:,} in inhabited areas lack three or more.",
         "Limit: only Turin is covered, because the service catalogue is missing for the surrounding towns."])


def forma_r4(s):
    r = leggi("risultato4_regolarita.json")
    c, par = r["citta"], r["parametri"]
    fer = c["0"]
    dd = r["confronto_gtt"]["definizioni"]
    a_fer, b_fer = dd["a"]["per_tipo"]["0"]["ritardo10_pct"], dd["b"]["per_tipo"]["0"]["ritardo10_pct"]
    a_set, b_set = dd["a"]["settimana"]["ritardo10_pct"], dd["b"]["settimana"]["ritardo10_pct"]
    nomi = {"0": "feriale", "1": "sabato", "2": "domenica"}
    pila = {"tipo": "pila100", "titolo": "Come arrivano i mezzi", "unita": "%",
            "nota": "Ogni barra è un tipo di giorno: 100% dei passaggi.",
            "righe": [{"label": nomi[k], "voci": [
                voce("in anticipo (oltre 1 minuto)", c[k]["anticipo"], tono="blu"),
                voce("puntuali", c[k]["puntuale"], tono="verde"),
                voce("ritardo da 5 a 10 minuti", round(c[k]["ritardo"] - c[k]["ritardo10"], 2), tono="giallo"),
                voce("ritardo oltre 10 minuti", c[k]["ritardo10"], tono="rosso")]} for k in ("0", "1", "2")]}
    fasce = [(f, v) for f, _, v in fasce_r4() if f != "notte"]
    nomi_f = {"punta_mattina": "punta mattino (7-9)", "giorno": "giorno (9-16)", "punta_sera": "punta sera (16-19)", "sera": "sera (19-24)"}
    linea = {"tipo": "linea", "titolo": "Ritardo oltre 5 minuti, per fascia oraria (feriale)", "unita": "%",
             "categorie": [nomi_f[f] for f, _ in fasce], "serie": [{"label": "passaggi in ritardo", "valori": [v for _, v in fasce]}]}
    noi_gtt = next(g for g in s["grafici"] if g["titolo"].startswith("Noi e GTT"))
    linee = [(n, v["0"]) for n, v in r["linee"].items() if "0" in v]
    peggio = max((x for x in linee if x[1]["passaggi"] >= par.get("min_passaggi_classifica", 2000) and str(x[0]).isdigit()),
                 key=lambda x: x[1]["ritardo"])
    tram, bus = r["modi"]["tram"]["0"], r["modi"]["bus"]["0"]
    gb_tram, gb_bus = tram["grappolo"] + tram["buco"], bus["grappolo"] + bus["buco"]
    dist = int(r["regole_gps"]["dist_gps_m"])
    gg = r["giorni"]
    r9 = scheda_r9()
    f9 = r9["scenari"][0]["numeri"]
    attese = (f9[0], f9[1])
    extra = {"titolo": "Quanto si aspetta alla fermata",
             "punto": f"Sulle linee frequenti si aspettano da {virgola(attese[0]['dopo'] - attese[0]['prima'])} a "
                      f"{virgola(attese[1]['dopo'] - attese[1]['prima'])} minuti in più di quanto promette l'orario (feriale).",
             "grafico": dict(r9["grafici"][0], titolo="Attesa media alla fermata, per fascia oraria (feriale)")}
    return forma_base(
        s,
        f"I ritardi gravi sono circa il {round(fer['ritardo10'])}% dei passaggi",
        "Quanto spesso i mezzi GTT arrivano in ritardo o a coppie?",
        {"valore": a_fer, "unita": "%", "testo": "dei passaggi feriali arriva con oltre 10 minuti di ritardo"},
        pila,
        [f"Oltre 10 minuti di ritardo: {virgola(a_fer)}% dei passaggi a ogni fermata, {virgola(b_fer)}% se si guarda solo la partenza.",
         f"La linea più in ritardo è la {peggio[0]}: {virgola(peggio[1]['ritardo'])}% dei passaggi feriali oltre 5 minuti.",
         f"I tram arrivano più a grappolo dei bus: {virgola(gb_tram)}% delle coppie di mezzi contro {virgola(gb_bus)}% (feriale)."],
        [noi_gtt, linea],
        ["Il Raspberry Pi registra ogni minuto la posizione GPS dei mezzi GTT.",
         f"Il passaggio è l'istante in cui il GPS è a meno di {dist} metri dalla fermata.",
         "Il ritardo è quell'istante meno l'orario ufficiale.",
         f"In anticipo oltre {virgola(abs(par['soglia_anticipo_min']))} minuto; in ritardo oltre {virgola(par['soglia_ritardo_min'])} minuti.",
         "Grappolo: due mezzi attaccati. Buco: intervallo doppio del previsto. Solo linee frequenti."],
        [list(p) for p in s["parametri"]],
        [f"Pochi giorni: {gg['0']} feriali, {gg['1']} sabati e {gg['2']} {'domenica' if gg['2'] == 1 else 'domeniche'}, non tutti interi.",
         "Solo le linee urbane viste dal GPS, dalle 5 a mezzanotte.",
         f"Il GPS copre circa il {round(r['copertura_gps']['totale']['copertura_pct'])}% dei passaggi programmati; le corse mai viste non si contano.",
         "Contiamo quanto spesso c'è ritardo, non quante persone aspettano."],
        [f"Question: how often are GTT vehicles late or bunched? Answer: {fer['ritardo10']:.1f}% of weekday departures are more than 10 minutes late.",
         f"GTT reports {GTT_RITARDO10_2025_PCT}% for 2025. Counting only the first stop we get {b_set:.1f}%; the rest is season and method.",
         f"Limit: only {gg['0']} weekdays, {gg['1']} Saturdays and {gg['2']} Sunday of data, urban lines only, no night."],
        confronto=[f"GTT dichiara il {virgola(GTT_RITARDO10_2025_PCT)}% oltre 10 minuti nel 2025: media dell'anno, tutte le linee, metodo non pubblicato.",
                   f"Noi misuriamo pochi giorni di ottobre sulle linee urbane: {virgola(a_set)}% a ogni fermata, {virgola(b_set)}% alla partenza.",
                   f"Anche contando come GTT alla partenza troviamo il {virgola(b_set)}%; il resto della differenza è stagione e metodo."],
        extra=extra)


def forma_r6(s):
    r = json.loads(R6_FILE.read_text(encoding="utf-8"))
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
    ba = json.loads((PROC / "r6_bus_contro_auto.json").read_text(encoding="utf-8"))
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
    mi = lambda l: f"{round(l['pareggio_basso_min'])}–{round(l['pareggio_alto_min'])} minuti" if l["pareggio_basso_min"] is not None else "nessun collegamento"
    pieni_i = [l for l in inter if l["stato"] == "pieno"]
    vuoti_i = [l for l in inter if l["stato"] == "libero"]
    kp1 = ("Interscambi esistenti: pieni " + (", ".join(f"{nome_pulito(l['nome'])} ({mi(l)})" for l in pieni_i) or "nessuno")
           + "; poco usati " + (", ".join(f"{nome_pulito(l['nome'])} ({mi(l)})" for l in vuoti_i) or "nessuno") + ".")
    migliore = pb[0] if pb else None
    kp3 = (f"Il punto più promettente è {nome_pulito(migliore['nome'])}: bastano {mi(migliore)} perché il bus pareggi l'auto."
           if migliore else "Nessun punto ha un collegamento coi mezzi entro 120 minuti.")
    return forma_base(
        s,
        f"Dai parcheggi di scambio il bus vale l'auto solo se in centro si perdono {forbice_m} minuti a parcheggiare",
        "Dove mancano posti per lasciare l'auto, e quando il bus da lì verso il centro è veloce quanto l'auto?",
        {"valore": forbice_m, "unita": "minuti",
         "testo": f"persi in centro per parcheggiare: sotto questa soglia l'auto batte il bus (mediana dei {n_punti_ba} punti)"},
        pareggio_g,
        [kp1,
         f"{n_senza} fermate importanti su {n_fermate} non hanno posti bastanti a {raggio} metri a piedi.",
         kp3],
        [principale],
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
        extra=extra)


def forbice_estremi(x, y):
    """Estremi della forbice per il titolo: interi se differiscono di almeno 0,5, altrimenti con un decimale."""
    if abs(y - x) >= 0.5:
        return str(round(x)), str(round(y))
    return virgola(round(x, 1)), virgola(round(y, 1))


def forma_r8(s):
    """Scheda R8: tempo coi mezzi pubblici contro tempo in auto (script 93), come forbice fra due fattori di punta; in coda la copertura delle strade."""
    t = json.loads((PROC / "tp_contro_auto.json").read_text(encoding="utf-8"))
    r = leggi("risultato8_traffico_tp_v2.json")
    u = r["universo_torino"]
    quota_strade = round(u["quota_km_coperta_tp"] * 100, 1)
    par, ti = t["parametri"], t["titolo"]
    ab = t["gruppi"]["ab"]
    lo, hi = ab["limite_basso"], ab["limite_alto"]            # lo = fattore di Google (rapporto piu' basso), hi = fattore dei sensori (rapporto piu' alto)
    x, y = forbice_estremi(ti["mediano_basso"], ti["mediano_alto"])
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
                          f"Limite basso: auto lenta come su Google Maps (fattore {f_lo}); limite alto: auto veloce come misurano i sensori (fattore {f_hi}).",
                  "gruppi": [{"label": n, "voci": [
                      {"label": "limite basso", "valore": round(a["pct"], 1), "tono": tn, "testo": f"{virgola(round(a['pct'], 1))}% ({migliaia(a['auto'])} auto)"},
                      {"label": "limite alto", "valore": round(b["pct"], 1), "tono": tn, "testo": f"{virgola(round(b['pct'], 1))}% ({migliaia(b['auto'])} auto)"}]}
                      for n, a, b, tn in zip(nomi_fasce, lo["fasce"], hi["fasce"], toni)]}
    disp = {"tipo": "dispersione", "titolo": "Tempo in auto e tempo coi mezzi pubblici, una coppia di zone per punto",
            "xlabel": f"minuti in auto (ora di punta, fattore {f_lo})", "ylabel": "minuti coi mezzi pubblici",
            "punti": [[p["auto_punta_basso_min"], p["tp_min"], p["auto"]] for p in ordinate],
            "linee": [{"k": f1, "label": f"{virgola(f1)} volte"}, {"k": f2, "label": "il doppio"}],
            "nota": f"Ogni punto è una coppia di zone, grande quanto le auto del mattino. Sono le {len(ordinate)} coppie con più auto "
                    f"({virgola(quota_punti)}% delle auto). Sopra una linea il mezzo pubblico impiega più di quel multiplo dell'auto."}
    peggiori = t["peggiori"]
    pare = {"tipo": "barre", "titolo": "Le 15 coppie con più auto dove i mezzi pubblici impiegano più del doppio", "unita": "auto",
            "nota": f"Auto del mattino su quella coppia (dalle 6 alle 10, giorno feriale), con il fattore basso {f_lo}. A destra i minuti coi mezzi contro quelli in auto.",
            "voci": [{"label": f"{p['da_nome']} → {p['a_nome']}", "valore": p["auto"], "tono": "rosso",
                      "testo": f"{migliaia(p['auto'])} auto: {round(p['tp_min'])} contro {round(p['auto_punta_basso_min'])} min"} for p in peggiori]}
    p3 = peggiori[:3]
    conferme = [n for n in t["noti"] if n["google_mezzi_min"]]
    txt_conf = " e ".join(f"{round(n['tp_min'])} contro {n['google_mezzi_min'][0]}-{n['google_mezzi_min'][1]}" for n in conferme)
    strade = grafico_per_titolo(s, "Km di strade grandi")
    extra = {"titolo": "Strade grandi e fermate vicine",
             "punto": f"Il {virgola(quota_strade)}% dei km di strade grandi ha una fermata frequente vicina: la fermata c'è, ma non basta.",
             "grafico": strade}
    senza_ab = ab["senza_collegamento"]
    gg = t["google"]
    par_crit = [["Zone", f"{par['n_zone']} zone dell'indagine sugli spostamenti ({par['n_zone_torino']} di Torino), fino a {par['punti_per_zona']} punti ciascuna"],
                ["Mezzi pubblici", f"partenza {par['partenza']}-8:15 di un feriale, mediana, cammino a {virgola(par['velocita_piedi_kmh'])} km/h, al massimo {par['tempo_max_min']} minuti"],
                ["Auto, limite alto", f"tempo a flusso libero × {f_hi} (sensori 5T) + {virgola(par['minuti_parcheggio'])} minuti"],
                ["Auto, limite basso", f"tempo a flusso libero × {f_lo} (Google Maps, 6 percorsi) + {virgola(par['minuti_parcheggio'])} minuti"],
                ["Fasce del rapporto", f"sotto {virgola(f1)}, {virgola(f1)}-{virgola(f2)}, {virgola(f2)}-{virgola(f3)}, oltre {virgola(f3)} (fissate prima dei numeri)"]]
    return forma_base(
        s,
        f"Al mattino, coi mezzi pubblici si impiega da {x} a {y} volte il tempo dell'auto",
        "Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno?",
        {"valore": f"{x}–{y}", "unita": "volte",
         "testo": f"il tempo dell'auto: rapporto mediano, pesato per le auto del mattino ({migliaia(ti['auto_collegate'])} auto)"},
        principale,
        [f"Le auto con rapporto oltre 2 sono il {q_lo}% con il fattore basso e il {q_hi}% con il fattore alto.",
         "Le 3 coppie peggiori: " + ", ".join(f"{p['da_nome']} → {p['a_nome']}" for p in p3) + ".",
         f"Google conferma i tempi coi mezzi pubblici sui percorsi di controllo: {txt_conf} minuti."],
        [disp, pare],
        ["Le zone sono quelle dell'indagine sugli spostamenti 2022 con punti di calcolo; ognuna ha fino a 5 punti.",
         "Mezzi pubblici: a piedi, bus, tram e metro, con partenza fra le 7:45 e le 8:15. Si prende la mediana.",
         f"Auto: tempo a flusso libero per un fattore di punta, più 5 minuti. I fattori sono due: {f_lo} da Google Maps e {f_hi} dai sensori.",
         "Rapporto = tempo coi mezzi diviso tempo in auto. Le fasce sono fisse e decise prima di vedere i numeri.",
         "Le auto di una coppia sono i viaggi in auto dell'indagine, in partenza dalle 6 alle 10 di un feriale."],
        par_crit,
        ["Fuori Torino mancano treni e altre aziende: le coppie fra comuni della cintura non sono nel numero.",
         "La nostra rete stradale non conta semafori e incroci. I tempi in auto sono stimati fra il rallentamento misurato dai sensori e quello di Google Maps.",
         "Senza i treni metropolitani, dove ci sono, i mezzi pubblici risultano più lenti del vero. L'orario è quello programmato.",
         f"L'indagine è un campione. I viaggi dentro una zona e {migliaia(senza_ab['coppie'])} coppie senza collegamento ({migliaia(senza_ab['auto'])} auto) non sono nel confronto."],
        ["Question: for which trips is the car much faster than public transport, and how many cars make them?",
         f"Answer: in the morning public transport takes {ti['mediano_basso']:.1f} to {ti['mediano_alto']:.1f} times as long as the car (weighted median). "
         f"For {100 * ti['quota_oltre_2_basso']:.0f}% to {100 * ti['quota_oltre_2_alto']:.0f}% of cars it takes more than twice as long.",
         f"Limit: car times lie between the slowdown measured by sensors ({hi['fattore']:g}) and by Google Maps ({lo['fattore']:g}). "
         "Without metropolitan trains, public transport looks slower than it is."],
        mappa=False, extra=extra)


FORME = {"risultato1": forma_r1, "risultato4": forma_r4, "risultato6": forma_r6, "risultato8": forma_r8}


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
            s["forma"] = FORME[nome](s)
            print(f"{nome}: forma - «{s['forma']['titolo']}», numero grande {s['forma']['numero']['valore']} {s['forma']['numero']['unita']}")
            controlla_forma(nome, s["forma"])
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
