"""Dati di progetto.html (data/progetto.js): contatore della raccolta, zone di Torino con le 5 in doppio svantaggio, confronto feed-GPS dei ritardi.

Tutto viene da file gia' prodotti: data/storico_riassunti (contatore, come la home), data/processed/velocita_5t.json (numero di sensori),
case_fragilita_servizi.json (script 95) e omi_zone.json (poligoni delle zone OMI), risultato4_regolarita.json (script 27), assets/torino_contorno.json.
I numeri dei risultati (2-3 volte, minuti di pareggio, ...) la pagina li legge dalle schede (data/schede_risultati.js): qui non si copiano.
Nessun numero e' scritto a mano."""
import json

from schede.comune import PROC, RADICE, leggi
from schede.home import contatore
from schede.r10 import nome_zona

OUT = RADICE / "data" / "progetto.js"


def _rdp(pts, tol):
    """Douglas-Peucker su una lista di (x, y); tiene il primo e l'ultimo punto."""
    if len(pts) < 3:
        return pts
    (x0, y0), (x1, y1) = pts[0], pts[-1]
    dx, dy = x1 - x0, y1 - y0
    n = (dx * dx + dy * dy) ** 0.5 or 1e-9
    dmax, k = 0.0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x1 * y0 - y1 * x0) / n
        if d > dmax:
            dmax, k = d, i
    if dmax <= tol:
        return [pts[0], pts[-1]]
    return _rdp(pts[:k + 1], tol)[:-1] + _rdp(pts[k:], tol)


def _percorso(anelli, c, tol=1.1):
    """Anelli [[lat, lon], ...] -> percorso SVG relativo (interi) nel disegno del contorno di Torino (stesse coordinate di assets/torino_contorno.json)."""
    out = ""
    for anello in anelli:
        pts = [((lon - c["lon_min"]) * c["k"] * c["scala"], (c["lat_max"] - lat) * c["scala"]) for lat, lon in anello]
        m = len(pts) // 2                                    # anello chiuso: primo e ultimo punto coincidono, si semplificano le due meta'
        pts = _rdp(pts[:m + 1], tol)[:-1] + _rdp(pts[m:], tol)
        if len(pts) < 3:
            continue
        x, y = round(pts[0][0]), round(pts[0][1])
        out += f"M{x} {y}"
        for px, py in pts[1:]:
            nx, ny = round(px), round(py)
            out += f"l{nx - x} {ny - y}"
            x, y = nx, ny
        out += "z"
    return out


def scrivi_progetto():
    c = json.loads((RADICE / "assets" / "torino_contorno.json").read_text(encoding="utf-8"))
    cf = leggi("case_fragilita_servizi.json")
    e2 = cf["e2_doppio_svantaggio"]
    doppie = {z["zona"].split(" ", 1)[0]: z for z in e2["zone"]}
    omi = next(x for x in json.loads((PROC / "omi_zone.json").read_text(encoding="utf-8")) if x["c"] == 1272)["zone"]
    zone = []
    for z in omi:
        d = _percorso(z["g"], c)
        if not d:
            continue
        voce = {"cod": z["z"], "d": d}
        if z["z"] in doppie:
            voce.update({"nome": nome_zona(doppie[z["z"]]["zona"]), "abitanti": doppie[z["z"]]["abitanti"], "doppio": 1})
        zone.append(voce)
    mancanti = set(doppie) - {z["cod"] for z in zone}
    if mancanti:
        raise SystemExit(f"ERRORE: zone in doppio svantaggio senza poligono in omi_zone.json: {sorted(mancanti)}")
    r4 = leggi("risultato4_regolarita.json")
    gps, feed = r4["citta"]["0"]["ritardo"], r4["confronto_feed"]["citta"]["0"]["ritardo"]
    se = e2["sezioni"]
    dati = {
        "contatore": contatore(),
        "sensori_5t": len(leggi("velocita_5t.json")["sensori"]),
        "contorno": {"larghezza": c["larghezza"], "altezza": c["altezza"], "d": c["d"]},
        "zone": zone,
        "doppio": {"residenti": se["residenti_doppio_svantaggio"], "quota": round(100 * se["quota_residenti_di_riferimento"], 1),
                   "n_su": round(10 / max(1, round(10 * se["quota_residenti_di_riferimento"]))), "n_zone": len(doppie), "abitanti_zone": e2["residenti_zone_doppio_svantaggio"]},
        "ritardi": {"gps_pct": gps, "feed_pct": feed, "rapporto": round(gps / feed, 1) if feed else None,
                    "copertura_gps_pct": r4["copertura_gps"]["totale"]["copertura_pct"], "soglia_min": r4["parametri"]["soglia_ritardo_min"]},
    }
    OUT.write_text("// generato da scripts/schede_risultati.py - non modificare a mano\nwindow.PROGETTO = " + json.dumps(dati, ensure_ascii=False, separators=(",", ":")) + ";\n",
                   encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"progetto.js: {len(zone)} zone di Torino ({len(doppie)} in doppio svantaggio), contatore {dati['contatore']}, "
          f"ritardi oltre {dati['ritardi']['soglia_min']:g} min: GPS {gps}% contro feed {feed}%, {kb:.0f} KB")
    if kb > 200:
        print(f"AVVISO: data/progetto.js pesa {kb:.0f} KB (limite scelto: 200 KB)")
