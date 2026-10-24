# Esito del giro L9b (24/10/2026): numeri stabili prima della grafica

Risposte di Leo usate: periodo a giorni interi = sì; partenza al capolinea corretta = sì; scheda 5 col grafico fragilità-servizi = sì.
La risposta sulla «domanda della scheda 5» è arrivata come segnaposto («tieni / solo la seconda parte»): non so quale delle due, quindi la domanda è rimasta com'era (tieni). Leo può dire se vuole solo la seconda parte.

## Cosa è stato fatto

1. **Periodo a giorni interi.** `comuni.PERIODO`: GPS 10/10-22/10 (prima fino al 23/10, giorno a metà), sensori 5T 09/10-22/10 e parcheggi 15/10-22/10 (invariati). Regola scritta in `comuni.py`: il periodo non contiene mai il giorno della copia dello storico; `comuni.controlla_copia_storico` stampa un AVVISO se succede (lo script 27 lo chiama). Il periodo ora lo leggono anche `04_genera_mappa.py` (velocità delle linee), `24_importanza_vie.py` e `69_parcheggi_inventario.py`. Gli altri script che aprono lo storico non fanno risultati: 35 ha già date fisse (09-16/10), 38b è una verifica dei codici dei sensori, 12 e 06 sono la raccolta.
2. **Partenza al capolinea** (script 27, funzione `cerca_vincolata(..., partenza=True)`): per la sola prima fermata di ogni corsa il passaggio è l'ultimo istante del gruppo di posizioni vicine alla fermata, cioè quando il bus se ne va. Le altre fermate non cambiano. Lo script 70 usa la stessa funzione (passa da `costruisci_passaggi_gps`), quindi vale anche per le attese. Prova con una corsa finta (bus fermo 4 minuti, poi parte): `scripts/prove/prova_capolinea.py`, aggiunta ai controlli su GitHub.
3. **Scheda 5.** Grafico principale: zone con fragilità (x) e servizi (y), grandezza = abitanti, retta di tendenza (calcolata dallo script 95, nuova chiave `retta_fragilita_servizi`); nella nota la correlazione a parità di distanza (−0,48, da −0,66 a −0,23, regge). Prezzo-servizi è ora fra gli «altri grafici», con la nota che a parità di distanza il legame quasi sparisce (0,21).
4. **Rilancio completo** `rifai_tutto.py --da traffico` (42 minuti, exit 0) e `04_genera_mappa.py`. Seconda esecuzione di `schede_risultati.py`: nessuna differenza fuori da «generato» e «Aggiornato al». I numeri ora si riproducono.
5. **Release** `dati-2026-11` rifatta (script 98): `dati-grezzi-istat-2026-11.zip` 280,7 MB (139 file), `dati-grezzi-altri-2026-11.zip` 27,1 MB (52 file), `dati-calcolati-2026-11.zip` 96,8 MB (29 file), più `SHA256SUMS.txt`, in `C:\projects\Progetti\GTT_release`. Gli zip hanno sostituito quelli di L8; Leo la carica.

## Prima e dopo (feriale, salvo dove scritto)

| Numero | Prima | Dopo |
|---|---|---|
| Giorni feriali / passaggi GPS | 8 / 1.344.165 | 7 / 1.250.433 |
| Copertura GPS | 79,5% | 79,8% |
| R4 oltre 5 minuti | 15,6% | 16,0% |
| R4 oltre 10 minuti | 6,19% | 6,41% |
| Anticipo a ogni fermata (a) | 36,2% | 35,4% |
| Anticipo alla prima fermata (b) | 56,1% | 29,0% (sotto il 30%: nessun AVVISO) |
| Anticipo a metà corsa (c) / fuori punta (d) | 36,0% (misura di L9) / — | 35,9% / 35,7% |
| Oltre 10 min, settimana: a ogni fermata / prima fermata / metà corsa / fuori punta | 6,02 / 4,29 / 5,72 / 5,63% | 6,18 / 5,28 / 5,86 / 5,79% |
| Ritardo alla partenza (oltre 10, prima fermata) contro GTT 2,3% | 4,29% | 5,28% |
| Feed GTT, oltre 5 minuti | 6,0% | 6,2% |
| Tram / bus oltre 5 minuti | 15,0% / 15,8% | 15,4% / 16,2% |
| Grappolo + buco | 21,6% | 21,6% |
| Attesa promessa / reale (stima bassa–alta) | 4,7 / 6,3–6,5 min | 4,8 / 6,4–6,5 min |
| Attesa in più | 1,5–1,7 min (+32%) | 1,6–1,7 min (+33%) |
| Linee peggiori per ritardo | 17, 6, 19, 68, 66 | 17, 6, 19, 68, 66 (stesso ordine) |
| R6 fermate senza posti, classi dei 12 punti, pareggio | — | invariati (sensori e parcheggi: stesso periodo) |
| R8 rapporto mediano, quota delle auto, modello del traffico | — | invariati |
| R1 residenti esposti | — | invariati |
| R10 (scheda 5) numeri | — | invariati (cambiano solo i grafici) |

Nota sui numeri della colonna «Prima» di R4: sono quelli pubblicati fino a L9 (copia dello storico del 23/10 mattina). La differenza di 6,19 → 6,41 è in parte il giorno a metà tolto, in parte il passaggio più tardi alla prima fermata.

## Documenti aggiornati
`docs/R4_puntualita.md` (periodo, numeri, definizione della partenza al capolinea), memoria, README e pagine `r/N.html` (dai numeri delle schede). `docs/R1`, `R6`, `R8`: numeri invariati.

## Controlli
pyflakes zero; nessuna ATTENZIONE delle schede; `prova_pagine.py --playwright` 0 errori su 20 pagine; avvisi del rilancio: solo quelli attesi (pochi sabati e domeniche, 21:00 non più veloce delle 8, dati scarsi delle zone della cintura).

## Da fare a mano (Leo)
Caricare la Release (GitHub → Releases → Draft a new release → tag `dati-2026-11` → trascinare i 3 zip e `SHA256SUMS.txt` → Publish). Guardare le schede 4 e 5 e la mappa (tema Puntualità).
