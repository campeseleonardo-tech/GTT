"""Risultato 10 (pubblico 5): case, servizi e fragilita'."""
import re
from schede.comune import forma_base, leggi, migliaia, num, ora, pct2, virgola




# ---------------------------------------------------------------- Risultato 10 (pubblico: 5) «Case, servizi e fragilita'»
# Tutti i numeri vengono da data/processed/case_fragilita_servizi.json (script 95); qui niente e' scritto a mano.

def nome_zona(n):
    """«D6 MIRAFIORI SUD» -> «Mirafiori Sud»: via il codice OMI davanti, maiuscole normali."""
    parole = n.split(" ", 1)
    resto = parole[1] if len(parole) == 2 and re.fullmatch(r"[A-Z]\d+", parole[0]) else n
    return " ".join(w.capitalize() for w in resto.split())




def scheda_r10():
    j = leggi("case_fragilita_servizi.json")
    e1, e2 = j["e1_si_paga_per_i_servizi"], j["e2_doppio_svantaggio"]
    se = e2["sezioni"]
    quota = se["quota_residenti_di_riferimento"]
    # stessa approssimazione degli omini (decimi): 9,5% -> «circa 1 su 10», cosi' titolo e testo coincidono
    decimi = round(10 * quota)
    n_su = round(10 / decimi) if decimi else 0
    return {
        "risultato": "10",
        "titolo": "Case, servizi e fragilità",
        "tag": "STIMATO / CENSIMENTO",
        "stato": "Fatto",
        "in_breve": "Le case costano di più dove ci sono più servizi? E dove la fragilità sociale è alta e i servizi sono pochi?",
        "domanda": "Si paga per i servizi? E chi vive dove la fragilità è alta e i servizi sono pochi?",
        "numero_chiave": {"valore": se["residenti_doppio_svantaggio"], "unita": "",
                          "testo": f"residenti in sezioni con fragilità alta e pochi servizi ({virgola(100 * quota)}% dei residenti)"},
        "racconto": "", "risposta": [], "grafici": [], "metodo": [], "limiti": [], "parametri": [],
        "mappa": {"id": "vulnerabilita", "vista": "doppio", "nota": "Vista «Doppio svantaggio» nel tema Fragilità sociale."},
        "fonti": ["docs/rapporti/RAPPORTO_CASE_FRAGILITA_SERVIZI.txt", "data/processed/case_fragilita_servizi.json"],
        "generato": ora(),
        "avviso": ["Dati [STIMATO] (servizi, indice) / [CENSIMENTO] (abitanti). Differenza fra zone, non effetto causale."],
        "in_english": [],
        "scenari": [{
            "nome": "Oggi",
            "numeri": [
                num("Residenti in sezioni con fragilità alta e pochi servizi", se["residenti_doppio_svantaggio"], "residenti"),
                num("Quota dei residenti di Torino", round(100 * quota, 1), "%"),
                num("Zone in doppio svantaggio", len(e2["zone"]), "zone"),
                num("Correlazione prezzo-servizi (Spearman)", e1["spearman"], ""),
            ],
            "nota": "Zone OMI di Torino; le sezioni si sommano nella zona, pesate per abitanti.",
        }],
        "_n_su": n_su,
    }




def forma_r10(s):
    j = leggi("case_fragilita_servizi.json")
    e1, e2, e3 = j["e1_si_paga_per_i_servizi"], j["e2_doppio_svantaggio"], j["e3_valore_metro"]
    cn, se = j["conteggi"], e2["sezioni"]
    retta = e1["retta"]
    ic = e1["spearman_ic95"]
    soglie = e2["soglie_fissate"]
    n_su = s["_n_su"]
    # grafico principale: una zona = un punto (servizi, prezzo, abitanti, nome) e la retta di tendenza
    zone = j["zone"]
    principale = {"tipo": "dispersione", "titolo": f"Prezzo delle case e servizi a piedi, una zona OMI per punto ({len(zone)} zone)",
                  "xlabel": "punteggio «Tutti i servizi» a piedi, 0-100", "ylabel": "prezzo delle case, euro al m²",
                  "passo_x": 20, "passo_y": 500, "xnome": "servizi", "ynome": "euro al m²",
                  "punti": [[z["servizi"], z["prezzo"], z["abitanti"], nome_zona(z["zona"])] for z in zone],
                  "retta": {"a": retta["intercetta_eur_m2"], "b": retta["pendenza_eur_m2_per_punto_servizi"], "label": "tendenza"},
                  "nota": f"Ogni punto è una zona, grande quanto i suoi abitanti. La linea è la tendenza: ogni 10 punti di servizi in più, "
                          f"{migliaia(round(10 * retta['pendenza_eur_m2_per_punto_servizi']))} euro al m² in più."}
    zd = e2["zone"]
    nomi_zd = ", ".join(nome_zona(z["zona"]) for z in zd[:5]) + (" e altre" if len(zd) > 5 else "")
    # metro: media delle differenze nelle fasce dove si hanno sia zone con metro sia senza
    fasce = [f for f in e3["fasce"] if f["differenza"] is not None]
    diff_media = round(sum(f["differenza"] for f in fasce) / len(fasce)) if fasce else None
    senza_media = round(sum(f["senza_metro"]["prezzo_medio"] for f in fasce) / len(fasce)) if fasce else None
    if diff_media is None:
        kp_metro = "Vicino alla metro non si può confrontare il prezzo: mancano zone con e senza metro a pari distanza dal centro."
    else:
        entita = "poco di più" if 0 < diff_media < 0.15 * senza_media else "di più" if diff_media > 0 else "non di più"
        kp_metro = (f"Vicino alla metro le case costano {entita} ({'+' if diff_media > 0 else ''}{migliaia(diff_media)} euro al m² in media, a pari distanza dal centro). "
                    "Differenza fra zone, non effetto causale.")
    classi = se["classi"]
    nomi_classi = [("tutte_e_due", "fragilità alta e servizi bassi", "rosso"), ("solo_fragilita", "solo fragilità alta", "arancio"),
                   ("solo_servizi", "solo servizi bassi", "blu"), ("nessuna", "nessuna delle due", "verde")]
    graf_classi = {"tipo": "barre", "titolo": "Residenti delle sezioni di Torino per condizione", "unita": "residenti",
                   "nota": f"Sezioni abitate di Torino, senza le zone quasi disabitate. Fragilità alta = indice sopra {virgola(se['soglia_fragilita_sopra'])} su 100 (il 20% più alto); "
                           f"servizi bassi = punteggio fino a {virgola(se['soglia_servizi_fino_a'])} su 100 (il 20% più basso).",
                   "voci": [{"label": n, "valore": classi[k]["residenti"], "tono": tn, "testo": f"{migliaia(classi[k]['residenti'])} ({migliaia(classi[k]['sezioni'])} sezioni)"}
                            for k, n, tn in nomi_classi]}
    graf_metro = {"tipo": "barre_diff", "titolo": "Quanto più costano le case vicino alla metro (con metro meno senza metro)", "unita": "€/m²",
                  "nota": "Per fascia di distanza da Piazza Castello (2 km): prezzo medio delle zone con una fermata M1 entro 600 m meno quello delle zone senza, "
                          "alla stessa distanza dal centro. Su ogni barra il numero di zone. Differenza fra zone, non effetto della metro.",
                  "voci": [{"label": f"{f['fascia_km']} km dal centro", "valore": f["differenza"],
                            "testo": f"({f['con_metro']['zone']} zone con metro, {f['senza_metro']['zone']} senza)"}
                           for f in e3["fasce"]]}
    nz_usate = cn["zone_usate"]
    return forma_base(
        s,
        f"Circa 1 torinese su {n_su} vive in una zona con più difficoltà sociali e pochi servizi",
        "Si paga per i servizi? E chi vive dove i servizi sono pochi e la fragilità è alta?",
        {"valore": se["residenti_doppio_svantaggio"], "unita": "",
         "testo": f"residenti in zone con più difficoltà sociali e servizi bassi: il {virgola(100 * se['quota_residenti_di_riferimento'])}% dei residenti delle zone abitate"},
        principale,
        [f"Prezzo e servizi vanno insieme: correlazione di Spearman {pct2(e1['spearman'])} su {e1['n_zone']} zone (da {pct2(ic[0])} a {pct2(ic[1])}).",
         f"{len(zd)} zone sono in doppio svantaggio: {nomi_zd}. Ci abitano {migliaia(e2['residenti_zone_doppio_svantaggio'])} persone.",
         kp_metro],
        [graf_classi, graf_metro],
        [f"Unità: le {nz_usate} zone OMI di Torino con almeno 500 abitanti. Le sezioni si sommano nella zona, pesate per abitanti.",
         "Servizi: punteggio «Tutti i servizi» a piedi in 15 minuti. Fragilità: indice del censimento 2021 (lavoro, istruzione, case, anziani).",
         "Prezzo: centro della forbice OMI per le abitazioni civili. Tendenza: retta dei minimi quadrati.",
         f"Doppio svantaggio = fragilità nel 20% più alto e servizi nel 20% più basso. Soglie fissate prima dei numeri: {virgola(soglie['fragilita_sopra'])} e {virgola(soglie['servizi_fino_a'])}.",
         "Metro: zone con una fermata M1 entro 600 m dal centro, contro le altre alla stessa distanza da Piazza Castello."],
        [["Zone", f"{nz_usate} zone OMI di Torino, almeno 500 abitanti"],
         ["Fragilità alta", f"indice sopra {virgola(se['soglia_fragilita_sopra'])} su 100 (sezioni) / {virgola(soglie['fragilita_sopra'])} (zone)"],
         ["Servizi bassi", f"punteggio fino a {virgola(se['soglia_servizi_fino_a'])} su 100 (sezioni) / {virgola(soglie['servizi_fino_a'])} (zone)"],
         ["Metro vicina", "fermata M1 entro 600 m dal centro della zona"],
         ["Fasce", "2 km da Piazza Castello"]],
        ["I prezzi sono quotazioni OMI, non compravendite.",
         "C'è un solo semestre di quotazioni (2025/2).",
         "Le zone OMI sono grandi: dentro una zona i prezzi e i servizi cambiano molto.",
         "L'indice di fragilità non è il reddito: misura lavoro, istruzione, affollamento e anziani."],
        ["Question: do homes cost more where services are plentiful, and who lives where fragility is high and services are few?",
         f"Answer: 1 Turin resident in {n_su} ({migliaia(se['residenti_doppio_svantaggio'])} people, {100 * se['quota_residenti_di_riferimento']:.1f}%) lives where fragility is high and services are few. "
         f"Price and services go together (Spearman {e1['spearman']:.2f} over {e1['n_zone']} zones).",
         "Limit: price quotes, not sales; one semester; large zones. The metro price gap is between zones, not a causal effect."],
        anima={"tipo": "omini", "totale": 10, "colorati": round(10 * se["quota_residenti_di_riferimento"]),
               "didascalia": f"Circa {round(10 * se['quota_residenti_di_riferimento'])} torinese su 10 vive dove l'indice di fragilità sociale è alto e i servizi sono pochi "
                             f"({virgola(100 * se['quota_residenti_di_riferimento'])}% dei residenti delle zone abitate)."},
        )
