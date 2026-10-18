"""Schede dei RISULTATI per simulazione.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_riepilogo_mappa.json   (Risultato 6, da 25)
  data/schede_risultati.js   (tutte le schede, R2 compreso, caricate da sole da simulazione.html)

Il riepilogo del Risultato 2 lo scrive gia' 29_risultato2_metro_notte.py: qui si legge e basta.
Formato della scheda: {risultato, titolo, domanda, scenari:[{nome, numeri:[{label,prima,dopo,unita}], nota}], avviso}.
Un numero senza "prima/dopo" (fotografia di oggi) ha prima = null.
Nessun calcolo nuovo: solo numeri gia' presenti nei file (ricontrollati da Claude il 18/10/2026).
"""
import json
from datetime import datetime, timezone
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
PROC = RADICE / "data" / "processed"
OUT_JS = RADICE / "data" / "schede_risultati.js"


def leggi(nome):
    return json.loads((PROC / nome).read_text(encoding="utf-8"))


def num(label, dopo, unita, prima=None):
    return {"label": label, "prima": prima, "dopo": dopo, "unita": unita}


def migliaia(n):
    return f"{n:,}".replace(",", ".")


def ora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def scheda_r1():
    vuoti = leggi("risultato1_vuoti.json")
    cand = leggi("risultato1_candidati.json")["gruppi"]
    testa = vuoti["numeri_di_testa"]
    gruppi = vuoti["gruppi"]
    ordine = sorted(gruppi, key=lambda g: -gruppi[g]["torino"]["zero"]["residenti"])
    oggi = [num("Residenti senza almeno un servizio essenziale",
                testa["residenti_torino_senza_almeno_un_servizio_essenziale_a_zero"], "residenti"),
            num("Quota dei residenti di Torino", testa["quota_residenti_torino"], "%")]
    oggi += [num(f"Senza {g} entro 15 min", gruppi[g]["torino"]["zero"]["residenti"], "residenti")
             for g in ordine]
    dopo = []
    for g in ordine:
        c = cand[g]
        n_punti = len(c["candidati_scelti"])
        dopo.append(num(f"Senza {g} ({n_punti} {'punto nuovo' if n_punti == 1 else 'punti nuovi'})",
                        c["residenti_restano_a_zero"], "residenti", prima=c["residenti_a_zero_totali"]))
    return {
        "risultato": "1",
        "titolo": "Dove mancano i servizi a piedi",
        "domanda": "Quanti residenti di Torino non hanno almeno un servizio essenziale (scuole, salute, cibo, "
                   "fermate, verde) entro 15 minuti a piedi, e quanti ne recupererebbe qualche servizio nuovo?",
        "generato": ora(),
        "avviso": [
            "Dati [STIMATO] — solo comune di Torino",
            f"Distanze a piedi sulla rete stradale (15 min a 80 m/min) su {migliaia(testa['residenti_torino'])} "
            "residenti (censimento 2021). Servizi dal catalogo comunale: la cintura non e' confrontabile (manca "
            "il dato, non il servizio). I punti nuovi sono ipotesi di posizione, calcolate gruppo per gruppo: "
            "non si sommano tra gruppi e non tengono conto di costi o spazi disponibili."
        ],
        "scenari": [
            {"nome": "Oggi", "numeri": oggi,
             "nota": f"Il gruppo con piu' residenti scoperti e' {testa['gruppo_piu_carente_a_torino']}."},
            {"nome": "Con pochi servizi nuovi nei punti migliori", "numeri": dopo,
             "nota": "Fino a 5 punti per gruppo, scelti dove recuperano piu' residenti (raggruppamento 400 m)."},
        ],
    }


def scheda_r4():
    r = leggi("risultato4_regolarita.json")
    c = r["citta"]
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
    scenari[0]["nota"] = ("Molti passaggi risultano in anticipo perche' l'orario ufficiale ha margini; "
                          "un ritardo mediano negativo vuol dire 'di solito un po' prima'.")
    s = r["scarti"]
    tot = s["usati"] + s["fuori_gtfs"] + s["lettura_lontana"]
    return {
        "risultato": "4",
        "titolo": "Bus in ritardo e bus irregolari",
        "domanda": "Quanto spesso i mezzi GTT arrivano in ritardo, e quanto spesso sulle linee frequenti "
                   "arrivano a grappolo o lasciano buchi?",
        "generato": ora(),
        "avviso": [
            "Dati [MISURATO] — pochi giorni",
            f"Arrivi reali dal feed GTT raccolto dal Raspberry Pi, {r['periodo']['da']} - {r['periodo']['a']}: "
            f"usato l'{round(100 * s['usati'] / tot)}% dei passaggi letti (scartati quelli fuori orario ufficiale "
            "o con lettura lontana). Sabato e domenica sono un giorno ciascuno: numeri indicativi."
        ],
        "scenari": scenari,
    }


def scheda_r6():
    r = leggi("risultato6_interscambio.json")
    crit = [f for f in r["fermate"] if f["fermata_critica"]]
    coperte = sum(1 for f in crit if f["coperta"])
    inter = [p for p in r["parcheggi"] if p["interscambio"]]
    raggio = round(r["raggio_copertura_m"])
    return {
        "risultato": "6",
        "titolo": "Parcheggi di interscambio",
        "domanda": "Le fermate dove arriva piu' gente dalla cintura hanno un parcheggio di interscambio vicino?",
        "generato": ora(),
        "avviso": [
            "Dati [STIMATO] / [PROGRAMMATO] — versione 1",
            f"Fermata 'critica' = nel 10% piu' alto per strada importante, corse in punta e pendolari stimati "
            f"della zona (IMQ); centro escluso. Copertura = parcheggio entro {raggio} m in linea d'aria. "
            "Quanto si riempiono i parcheggi non e' ancora misurato (versione 2, con i dati raccolti dal 14/10)."
        ],
        "scenari": [{
            "nome": "Oggi",
            "numeri": [
                num("Fermate critiche fuori dal centro", len(crit), "fermate"),
                num(f"Coperte da un interscambio entro {raggio} m", coperte, "fermate"),
                num("Scoperte", len(crit) - coperte, "fermate"),
                num("Parcheggi di interscambio", len(inter), "parcheggi"),
                num("Posti negli interscambi", sum(p["posti"] for p in inter), "posti"),
            ],
            "nota": "Gli assi scoperti peggiori: metro e corso Francia verso Collegno, via Nizza, Moncalieri.",
        }],
    }


def main():
    schede = []
    for nome, fabbrica in (("risultato1", scheda_r1), ("risultato2", None),
                           ("risultato4", scheda_r4), ("risultato6", scheda_r6)):
        file = f"{nome}_riepilogo_mappa.json"
        if fabbrica is None:
            s = leggi(file)
        else:
            s = fabbrica()
            (PROC / file).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        s["_nome"] = file
        schede.append(s)
        print(f"{file}: {s['titolo']} - {sum(len(sc['numeri']) for sc in s['scenari'])} numeri")
    OUT_JS.write_text("// generato da scripts/schede_risultati.py - non modificare a mano\n"
                      "window.SCHEDE_RISULTATI = " + json.dumps(schede, ensure_ascii=False, indent=1) + ";\n",
                      encoding="utf-8")
    print(f"scritto {OUT_JS.relative_to(RADICE)} con {len(schede)} schede")


if __name__ == "__main__":
    main()
