"""Applica a DATI (estratto dalla mappa di oggi) le trasformazioni del 04 e scrive i DATI nuovi."""
import importlib.util, json, sys, time, copy
spec = importlib.util.spec_from_file_location("g04", "scripts/04_genera_mappa.py")
g04 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g04)
J = lambda v: len(json.dumps(v, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/"))
if __name__ == "__main__":
    S, out = sys.argv[1], sys.argv[2]
    d = json.load(open(S))
    t0 = time.time()
    d["sezioni"] = g04.compatta_sezioni(d["sezioni"])
    d["fermate"] = g04.compatta_fermate(d["fermate"])
    # catalogo: in questo file l'indice e' gia' quello pieno
    d["catalogo"] = g04.catalogo_ridotto(d["catalogo"])
    print("trasformazione", round(time.time() - t0, 1), "s")
    json.dump(d, open(out, "w"), separators=(",", ":"), ensure_ascii=False)
    print({k: J(v) for k, v in d.items() if J(v) > 5000})
    print({k: J(v) for k, v in d["sezioni"].items()})
