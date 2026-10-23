# ESITO L9 (24/10/2026): chiusura delle schede 2-5

Regole del blocco L9 fissate prima dei numeri, non cambiate dopo.

## Scheda 3 (parcheggi) — commit «L9 scheda 3»
| | Prima | Dopo |
|---|---|---|
| Titolo | «2 fermate importanti su 3 non hanno abbastanza posti per lasciare l'auto» | «… per lasciare l'auto (stima)» |
| Punto chiave 3 | «… Con TomTom il bus conviene (fino a 1,5 volte l'auto) in 8 punti su 12 e 4 dei 5 interscambi.» | stessa frase + «Dei punti dove il bus conviene, 5 su 8 sono vicini alla soglia: un'auto il 10% più veloce cambia classe.» (vicino = rapporto TomTom fra 1,35 e 1,65) |
| Limiti | — | + «Con metà o doppio di chi lascia l'auto, le fermate senza posti bastanti vanno da 135 a 212 su 274.» (da `porte.json`, sensibilità quota) |
| Numero più solido | 68 senza nessun parcheggio | invariato |
Documento R6: tabella «Controllo a mano di Leo (24/10)» e sezione sulla soglia.

## Scheda 4 (traffico e mezzi) — commit «L9 scheda 4»
- Testo del numero grande: «…pesato per le auto del mattino (220.307 auto)» → «… Sono il **47%** delle auto del mattino (220.307): mancano i viaggi dentro una zona e fra comuni della cintura.»
- Coppie nominate solo con almeno 30 interviste. **Interpretazione da conoscere:** con le sole interviste dei conducenti in auto del mattino nessuna coppia supera 21; ho usato le interviste della coppia (tutti i mezzi, giorno intero, `imq_od.json` dello script 14: l'affidabilità di SOGLIA_N). Le coppie con rapporto oltre 2 e almeno 30 interviste sono **12** (non 15): il grafico dice «Le 12 coppie…». Nomi senza «Torino, »; elenco «A → B · C → D».
- Via «Strade grandi e fermate vicine» (95,3%) dalla scheda; resta nel documento R8, con la tabella del controllo a mano.
- Script 93: nuovo campo `interviste` per coppia; titolo e gruppi identici a prima (controllato).

## Scheda 5 (case, servizi, fragilità) — commit «L9 scheda 5»
Correlazione parziale sui ranghi a parità di distanza dal centro (46 zone), intervallo al 95% (2.000 ricampionamenti, seme 95); regge se l'intervallo non contiene lo 0:
| Legame | Spearman | A parità di distanza | Regge |
|---|---|---|---|
| prezzo-servizi | +0,61 (0,39 / 0,79) | **+0,21 (−0,12 / +0,52)** | **no** |
| fragilità-servizi | −0,74 (−0,83 / −0,59) | **−0,48 (−0,66 / −0,23)** | sì |
| prezzo-fragilità | −0,83 (−0,91 / −0,68) | **−0,69 (−0,85 / −0,37)** | sì |
Doppio svantaggio contro il caso: fragilità alta 26,4% × servizi bassi 21,5% = 5,67% atteso; osservato 9,48% → **1,67 volte il caso** («1,7 volte quanto ci si aspetterebbe per caso» nel numero grande).
| | Prima | Dopo |
|---|---|---|
| Punto 1 | «Prezzo e servizi vanno insieme: correlazione di Spearman 0,61 su 46 zone (da 0,39 a 0,79).» | «A parità di distanza dal centro il legame prezzo-servizi quasi sparisce: correlazione 0,21 su 46 zone (da −0,12 a 0,52).» |
| Punto 3 | «Vicino alla metro le case costano … (differenza fra zone)» | «A parità di distanza dal centro reggono fragilità-servizi (−0,48) e prezzo-fragilità (−0,69).» |
| Grafico | metro/prezzi | tolto (resta nel rapporto E3) |
Rilancio del 95: tutti gli altri numeri uguali (controllato JSON e rapporto). Nuovo documento `docs/R10_case_fragilita_servizi.md`.

## Scheda 2 (puntualità) — commit «L9 scheda 2»
Anticipo (oltre 1 minuto in anticipo, feriale) con le tre definizioni (script 27, campo `anticipo_pct` in `confronto_gtt`): **(a) a ogni fermata 36,0%; (b) alla sola prima fermata 56,1%; (c) alla sola fermata di mezzo 36,0%.** Alla prima fermata NON è sotto il 10% (anzi è molto più alto): la condizione per aggiungere il limite «Gran parte degli anticipi avviene lungo la corsa…» non scatta, quindi nessun testo e nessun numero della scheda cambia. (I tre valori vengono dal rilancio sui dati di oggi; vedi sotto.)

## Periodo fisso — 🛑 RILANCIO CON NUMERI DIVERSI
Codice fatto: `comuni.PERIODO` (sensori 09/10-22/10; GPS 10/10-23/10; parcheggi 15/10-22/10, le date dei JSON pubblicati), letto da 26, 27, 70, 71 (filtro dei giorni) e controllato da 33 e 88; le schede 2, 3, 4 scrivono «Periodo dei dati…» (parametri).
**Ma** rilanciando con quelle date i numeri NON sono identici: 26 e 88 sì; 27, 70, 71, 33 no. Motivo: lo storico di oggi ha più dati dentro le stesse date (il 23/10 e i bordi: passaggi 1.419.943 contro 1.344.165, anticipo (a) 36,0% contro 36,2%, oltre 10 minuti 6,29% contro 6,19%; 33: un sensore non più escluso; 71: più letture nei giorni del bordo). Il periodo per date non basta a riprodurre i numeri pubblicati, che vengono da una copia dello storico più vecchia. **Come da regola ho ripristinato tutti i JSON e i rapporti pubblicati** (git checkout), e **non** ho cambiato la regola. Il codice del PERIODO resta (non cambia nessun numero finché non si rilancia); decide Leo: (1) rilanciare tutto con le nuove cifre (R4 passa a 6,3% oltre 10 minuti) e aggiornare i testi, oppure (2) fissare il periodo a giorni interi più vecchi (per esempio GPS fino al 22/10).
Anche `04_genera_mappa.py`, rilanciato, cambia i dati della mappa (legge lo storico di oggi): ripristinato `mappa_torino.html`.

## Controllo su GitHub
Nuovo passo in `.github/workflows/controllo.yml`: dopo `schede_risultati.py`, `git diff --exit-code -I'generato' -I'Aggiornato al' -- data/schede_risultati.js r README.md` (provato in locale: vuoto dopo il rilancio).

## Prove
pyflakes zero; `schede_risultati.py` senza ATTENZIONE; traduzioni aggiunte in `testi.json`; passi della `RIFAI_MAPPA_E_SCHEDE.bat` fatti a mano (04, schede, 86, prova pagine: la .bat ha `pause`); `prova_pagine.py --playwright`: 0 errori su 20 pagine.

## Cosa guardare (Leo)
Schede 3, 4, 5 e 2 su computer e telefono: titolo scheda 3 con «(stima)», numero grande scheda 4 (47%), punti chiave scheda 5, assenza del grafico metro; la riga «Periodo dei dati» nei parametri; e decidere sul periodo fisso.
