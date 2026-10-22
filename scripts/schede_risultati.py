"""Schede dei RISULTATI per risultati.html.

Legge i file gia' prodotti dagli script dei risultati e scrive:
  data/processed/risultato1_riepilogo_mappa.json   (Risultato 1, da 21 e 22)
  data/processed/risultato4_riepilogo_mappa.json   (Risultato 4, da 27)
  data/processed/risultato6_v2/mappa_r6.json   (Risultato 6, da 79 e 84) -> data/processed/risultato6_riepilogo_mappa.json
  data/processed/risultato8_riepilogo_mappa.json   (Risultato 8, script 56-67)
  data/processed/risultato10_riepilogo_mappa.json  (Risultato 10 = «Case, servizi e fragilita'», da case_fragilita_servizi.json dello script 95)
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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))   # il pacchetto schede/ sta accanto a questo file
from schede import comune  # noqa: E402
from schede.comune import NASCOSTE, RADICE, controlla_forma, leggi  # noqa: E402
from schede.r1 import forma_r1, scheda_r1  # noqa: E402
from schede.r10 import forma_r10, scheda_r10  # noqa: E402
from schede.r2 import arricchisci_r2  # noqa: E402
from schede.r4 import forma_r4, scheda_r4  # noqa: E402
from schede.r6 import forma_r6, scheda_r6  # noqa: E402
from schede.r8 import forma_r8, scheda_r8  # noqa: E402




FORME = {"risultato1": forma_r1, "risultato4": forma_r4, "risultato6": forma_r6, "risultato8": forma_r8, "risultato10": forma_r10}



# numerazione pubblica: in pagina i risultati sono 1-5; i numeri interni e i link #rN restano validi
NUMERO_PUBBLICO = {"risultato1": 1, "risultato4": 2, "risultato6": 3, "risultato8": 4, "risultato10": 5}




def main():
    schede = []
    for nome, fabbrica in (("risultato1", scheda_r1), ("risultato2", None),
                           ("risultato4", scheda_r4), ("risultato6", scheda_r6),
                           ("risultato8", scheda_r8), ("risultato10", scheda_r10)):
        if nome in NASCOSTE:
            continue
        file = f"{nome}_riepilogo_mappa.json"
        if fabbrica is None:
            s = arricchisci_r2(leggi(file))  # il JSON di R2 resta quello dello script 29
        else:
            s = fabbrica()
            s["forma"] = FORME[nome](s)
            s["numero_pubblico"] = NUMERO_PUBBLICO[nome]
            s.pop("_n_su", None)
            print(f"{nome}: forma - «{s['forma']['titolo']}», numero grande {s['forma']['numero']['valore']} {s['forma']['numero']['unita']}")
            controlla_forma(nome, s["forma"])
            (comune.PROC / file).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
        s["_nome"] = file
        schede.append(s)
        print(f"{file}: {s['titolo']} - {sum(len(sc['numeri']) for sc in s['scenari'])} numeri, "
              f"{len(s.get('grafici', []))} grafici")
    comune.OUT_JS.write_text("// generato da scripts/schede_risultati.py - non modificare a mano\n"
                      "window.SCHEDE_RISULTATI = " + json.dumps(schede, ensure_ascii=False, indent=1) + ";\n",
                      encoding="utf-8")
    try:
        mostra = comune.OUT_JS.relative_to(RADICE)
    except ValueError:   # solo nelle prove, con un'altra cartella
        mostra = comune.OUT_JS
    print(f"scritto {mostra} con {len(schede)} schede")




if __name__ == "__main__":
    main()
