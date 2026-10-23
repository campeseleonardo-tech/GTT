#!/usr/bin/env python3
"""Prova senza dati veri della partenza al capolinea (giro L9b): alla prima fermata di una corsa il passaggio e' l'ultimo istante vicino
alla fermata (il bus riparte), non il punto piu' vicino durante l'attesa; alle altre fermate niente cambia."""
import importlib.util
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RADICE / "scripts"))
spec = importlib.util.spec_from_file_location("r4", RADICE / "scripts" / "27_risultato4_regolarita.py")
r4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r4)

ERRORI = 0


def esito(nome, ok):
    global ERRORI
    print(("OK     " if ok else "ERRORE ") + nome)
    ERRORI += 0 if ok else 1


LAT0, LON0 = 45.07, 7.68
M_LAT = 1 / 110540.0          # gradi di latitudine per metro
# capolinea in (LAT0, LON0); il bus aspetta fermo a 20 m dalla fermata per 4 minuti (una posizione ogni 60 s), poi parte verso nord.
# Seconda fermata 1 km a nord. Tempi in secondi dal tempo 0.
punti = [(t, LAT0 + 20 * M_LAT, LON0) for t in range(0, 241, 60)]               # fermo 0..240 s
punti += [(300, LAT0 + 70 * M_LAT, LON0), (360, LAT0 + 400 * M_LAT, LON0), (420, LAT0 + 800 * M_LAT, LON0),
          (480, LAT0 + 1000 * M_LAT, LON0), (540, LAT0 + 1200 * M_LAT, LON0)]
fermate = {"A": (None, LAT0, LON0), "B": (None, LAT0 + 1000 * M_LAT, LON0)}
corsa = [(1, 0, "A"), (2, 480, "B")]
out = r4.passaggi_corsa(punti, corsa, 0, fermate)
esito("prima fermata: il passaggio e' quando il bus riparte (240-300 s), non durante l'attesa (0-240 s)", 240 <= out[1] <= 300)
esito("seconda fermata: invariata, vicino a 480 s", abs(out[2] - 480) <= 30)
kx = 111320.0 * 0.7
vecchio = r4.cerca_vincolata(punti, LAT0, LON0, kx, -1e18, 0)
esito("senza partenza=True il punto e' ancora quello dell'attesa (la prova coglie la differenza)", vecchio[0] < 240)
sys.exit(1 if ERRORI else 0)
