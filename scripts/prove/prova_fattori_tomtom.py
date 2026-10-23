#!/usr/bin/env python3
"""Prova senza dati veri di comuni.FattoriTomTom (giro L8): il fattore del percorso stesso, e per i percorsi non chiesti la mediana della stessa ora
e della stessa fascia di flusso libero (terzili)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import comuni  # noqa: E402

ERRORI = 0


def esito(nome, ok):
    global ERRORI
    print(("OK     " if ok else "ERRORE ") + nome)
    ERRORI += 0 if ok else 1


d = {"per_percorso": {"entrata": {"Pasini": {"08:00": [2.5, 1.4], "13:00": [None, 1.2]}},
                      "coppie": {"Q1|Q2": {"08:00": [2.0, 1.3], "13:00": [1.5, 1.1]}},
                      "zone_castello": {"Q7": {"08:00": [2.2, 1.3]}}},
     "regola_coppie": {"terzili": {"08:00": [5.0, 10.0], "13:00": [5.0, 10.0]},
                       "mediana_fascia": {"08:00": [1.8, 2.4, 3.0], "13:00": [1.4, 1.6, 1.9]}},
     "mediane_gruppo": {"entrata": {"08:00": 2.6, "13:00": 2.0}, "zone_castello": {"08:00": 2.3}},
     "controllo_B": [{"percorso": "Piazza Castello → Collegno", "fattore_rete": {"08:00": 2.39}}]}
f = comuni.FattoriTomTom(d)
esito("luogo chiesto: il suo fattore", f.luogo("Pasini", "08:00") == (2.5, True))
esito("luogo non chiesto: la mediana dell'entrata", f.luogo("Altro", "08:00") == (2.6, False))
esito("luogo senza fattore_rete a quell'ora: la mediana", f.luogo("Pasini", "13:00") == (2.0, False))
esito("coppia chiesta: il suo fattore, a ogni ora", f.coppia("Q1", "Q2", 7.0, "08:00") == (2.0, True) and f.coppia("Q1", "Q2", 7.0, "13:00") == (1.5, True))
esito("coppia non chiesta: la mediana della fascia (bassa, media, alta, estremi compresi nella fascia di sotto)",
      [f.coppia("X", "Y", m, "08:00") for m in (3.0, 5.0, 7.0, 10.0, 12.0)] == [(1.8, False), (1.8, False), (2.4, False), (2.4, False), (3.0, False)])
esito("coppia non chiesta: ogni ora ha le sue mediane", f.coppia("X", "Y", 12.0, "13:00") == (1.9, False))
esito("zona chiesta e non chiesta", f.zona("Q7") == (2.2, True) and f.zona("Q9") == (2.3, False))
esito("percorso di controllo", f.percorso_controllo("Piazza Castello → Collegno") == 2.39 and f.percorso_controllo("altro") is None)
sys.exit(1 if ERRORI else 0)
