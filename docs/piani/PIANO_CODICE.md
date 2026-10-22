# Piano 5 — Qualità tecnica del codice

Obiettivo: chi apre il repository vede codice ordinato e può rifare i calcoli senza Windows e senza chiedere a Leo.
Si fa **a pezzi, quando si tocca uno script per altri motivi**, tranne i passi 1-3 che vanno fatti subito.

Stato al 22/10 (controllo nel cloud): tutti gli script si compilano; nessun nome usato senza essere definito; 93
segnalazioni del controllo automatico, quasi tutte variabili calcolate e mai usate; la funzione delle distanze è copiata in
19 script; `schede_risultati.py` ha 1.600 righe; la prova delle pagine cerca Edge/Chrome solo nelle cartelle di Windows.

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **Prova delle pagine su ogni sistema**: `prova_pagine_r6.py` (nome nuovo `prova_pagine.py`) usa Playwright o il Chrome trovato sul sistema, non solo i percorsi di Windows | CLOUD | piccolo |
| 2 | **Controllo automatico su GitHub** (GitHub Actions): a ogni push, compila gli script, lancia `pyflakes`, apre le pagine e segnala errori; badge verde nel README | CLOUD | piccolo |
| 3 | **Un comando per rifare tutto**: `scripts/rifai_tutto.py` con l'ordine delle catene (dati → accessibilità → risultati → schede → mappa → prova), che si può fermare e riprendere; i `.bat` restano come scorciatoie per Windows | CLOUD (scritto) → PC (provato) | medio |
| 4 | **Funzioni comuni**: distanze, ora legale, lettura del GTFS, percentili in `comuni.py`; i 19 script le importano invece di copiarle (quando li si tocca) | CLOUD | medio, a pezzi |
| 5 | **Codice morto**: togliere le variabili mai usate (93 segnalazioni) | CLOUD | piccolo |
| 6 | **`schede_risultati.py` diviso**: una parte per risultato (`schede/r1.py` …) e i testi IT/EN in un file a parte (serve al bottone IT/EN del piano 4) | CLOUD | medio |
| 7 | **Mappa**: `mappa_template.html` (2.350 righe) diviso in stile, codice e dati; il 04 li rimette insieme nel file unico | CLOUD | medio |
| 8 | **Prove dei numeri**: per ogni risultato una piccola prova su dati finti con il risultato atteso (molti script hanno già `--prova`): diventano parte del controllo automatico | CLOUD | medio |
| 9 | **Piccolo difetto**: in `risultati.html` la scheda si apre anche quando cambia `#p3` senza ricaricare la pagina | CLOUD | piccolo |

Prova: dopo ogni passo che tocca uno script dei risultati, rilancio sul PC e numeri uguali a prima (il rapporto non deve
cambiare se non nella data).
