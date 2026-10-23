# Piano 5 — Qualità tecnica del codice

Obiettivo: chi apre il repository vede codice ordinato e può rifare i calcoli senza Windows e senza chiedere a Leo.
I passi 1-3 subito (servono alla pubblicazione); gli altri **a pezzi, quando si tocca uno script per altri motivi**.

Stato al 22/10 (controllo nel cloud): tutti gli script si compilano; nessun nome usato senza essere definito; 93
segnalazioni del controllo automatico, quasi tutte variabili calcolate e mai usate; la funzione delle distanze è copiata in
19 script; `schede_risultati.py` ha 1.600 righe; la prova delle pagine cerca Edge/Chrome solo nelle cartelle di Windows.

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **FATTO (C1)**: prova delle pagine su ogni sistema: `prova_pagine_r6.py` → `prova_pagine.py`, con Playwright o il Chrome trovato sul sistema; controlla anche che ogni file caricato dalle pagine esista (oggi lo fa lo script 86) | CLOUD | piccolo |
| 2 | **FATTO (C12; verde su GitHub, 23/10)**: **Controllo automatico su GitHub** (GitHub Actions), a ogni push: compila gli script, `pyflakes`, prova delle pagine, pesi dei file (piano 2, passo 5), link rotti; badge nel README | CLOUD | piccolo |
| 3 | **FATTO (C12; ordine provato in P7, 23/10)**: **Un comando per rifare tutto**: `scripts/rifai_tutto.py` (dati → accessibilità → risultati → schede → mappa → prova), si ferma e riprende; i `.bat` restano come scorciatoie per Windows. **Prova finale «da zero»**: clone + `scarica_dati.py` (piano 2) + `rifai_tutto.py` = stessi numeri delle schede | CLOUD (scritto) → PC (provato) | medio |
| 4 | **FATTO (C6)**: divisione di `schede_risultati.py`: una parte per risultato e i testi IT/EN in un file a parte (prima del passo 5 del piano 4) | CLOUD | medio |
| 5 | **FATTO (C13, 23/10: 21-29, 33-50, 51-67, 68-95)**: **Funzioni comuni** in `comuni.py` (distanze, ora legale, lettura del GTFS, percentili): i 19 script le importano, quando li si tocca | CLOUD | medio, a pezzi |
| 6 | **FATTO (23/10)**: **Codice morto**: pyflakes a 0 segnalazioni su tutto `scripts/`, controllo su GitHub senza esclusioni | CLOUD | piccolo |
| 7 | **Mappa**: `mappa_template.html` (2.350 righe) diviso in stile, codice e dati; il 04 li rimette insieme nel file unico | CLOUD | medio |
| 8 | **Prove dei numeri**: per ogni risultato una prova su dati finti con il risultato atteso (molti script hanno già `--prova`), dentro il controllo automatico | CLOUD | medio |
| 9 | **FATTO (C1)**: piccolo difetto: in `risultati.html` la scheda si apre anche quando cambia `#p3` senza ricaricare la pagina | CLOUD | piccolo |

Prova: dopo ogni passo che tocca uno script dei risultati, rilancio sul PC e rapporto uguale a prima (salvo la data).
