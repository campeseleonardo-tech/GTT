# Esito Risultato 1, fase B bis — 20/10/2026

Ramo `prova`, `git status` pulito, `git pull` già aggiornato all'inizio. Python del PATH.

## PASSO 1 — candidati con tutti e 5 i gruppi: OK
- `scripts/22_risultato1_candidati.py`: `--gruppi` default `"salute,scuole"` → `"scuole,salute,cibo,fermate,verde"`; esempio nella docstring aggiornato.
- `scripts/RISULTATO1_CANDIDATI.bat`: tolto `--gruppi salute,scuole` dalla riga `python`; commento e `echo` ora dicono «tutti e 5 i gruppi».
- `scheda_r1`: prima del ciclo `for g in ordine:` controllo dei gruppi mancanti in `cand` → `SystemExit("Risultato 1: mancano i candidati di …: lancia scripts\\RISULTATO1_CANDIDATI.bat")`.

## PASSO 2 — `scripts/21_risultato1_vuoti.py`, sezioni «da verificare»: OK
- Aggiunti: `RAGGIO_FERMATA_SOSPETTA_M = 300`, `GTFS` (stesso zip dello script 18, sola lettura), `fermate_gtfs()`, `fermata_piu_vicina_m(lat, lon)` (con `comuni.haversine_m`), `da_verificare(s)`. `s["lat"]`/`s["lon"]` esistono in `accessibilita.json`.
- Stati in ordine: poco abitata → da verificare → abitata. `riepilogo_ambito` ha la terza categoria `da_verificare` + `residenti_da_verificare` + `sezioni_da_verificare`; il controllo delle somme somma le tre categorie (tutti OK).
- `per_sez` ha `"verif"`; `v2.titolo.residenti_da_verificare`; `v2.sezioni_da_verificare` (con `ambito` e `fermata_m`); `v2.raggio_fermata_sospetta_m`; `sezioni_critiche_torino` esclude le da verificare.
- Rapporto: riga «zone da verificare (a parte)» e sezione «SEZIONI DA VERIFICARE».
- Uscite: titolo **362** residenti (prima 751); controllo OK «sezioni critiche di Torino: 5, somma residenti 362 (titolo 362)». Da verificare: **2 sezioni, 389 residenti**, entrambe a Torino (12720005328: 245 ab., fermata a 179 m; 12720000972: 144 ab., fermata a 75 m); in cintura nessuna. Come atteso dal piano. Sezioni critiche rimaste: 12720003044, 12720003783, 12720003836, 12720006938, 12720005880.

## PASSO 3 — `scripts/22_risultato1_candidati.py`: OK
- Aggiunte `verificare(s)` (usa `vuoti21.da_verificare`, nessuna copia) e `candidabile(s)`; usata nel filtro delle sezioni a zero e in `zero_ids_g`. La riga «solo sezioni abitate» del rapporto ora termina con «sezioni da verificare tolte: N».
- Lancio (tutti e 5 i gruppi, 36 s per la matrice R5): candidati scelti **scuole 5, salute 5, cibo 3, fermate 1, verde 0**. Il candidato «fermate» a 45,07306 7,71159 non c'è più (ora 45,02549 7,70009, 85 residenti). Da verificare tolte: scuole 2, salute 2, cibo 0, fermate 2, verde 0.

## PASSO 4 — `04_genera_mappa.py` e `mappa_template.html`: OK
1. 04: `r1 = [n_mancanti, m, poco, verif]`; controllo del titolo esclude `verif == 1`: «OK: titolo risultato 1: 362 … (script 21: 362); sezioni con r1: 8317».
2. Template: helper `r1Verif(z)`; sezioni da verificare (non poco abitate) in lilla `#b9a6d6` nella vista `tutti` e nelle viste per gruppo (stessa trasparenza delle altre aree); riquadro in legenda «dato da verificare (punto di partenza lontano dalle strade)».
3. Vista `tutti`: cerchio (raggio 9 px, contorno 2,5 px `#a50026`) al centro delle sezioni di Torino abitate, non da verificare, con `r1[0] >= 3`; voce di legenda «cerchio = zona abitata con 3 o piu' servizi mancanti».
4. Pannello: «Dato da verificare» / «C'è una fermata vicina, ma il calcolo a piedi non la raggiunge»; tooltip «da verificare» / «Da verificare». Tolta la riga «Abitanti per km²» (resta «Regola»); le due righe «Residenti sezione» usano `Math.round(z.dens).toLocaleString("it-IT")`.

## PASSO 5 — `schede_risultati.py`, `scheda_r1`: OK
Riga «Residenti in zone da verificare (a parte)» tra i numeri «Oggi»; frase «Altri N residenti sono in zone dove il calcolo non raggiunge una fermata che c'è: contati a parte, da verificare.»; regola (con raggio dal JSON) nei limiti; stesse cose in `in_english`. Nessun numero scritto a mano. Nota: il primo limite «Solo Torino: in cintura il catalogo dei servizi non c'è…» è rimasto com'era (vecchio, non nel piano).

## PASSO 6 — Lanci: OK
`21` → `22` → `04` → `schede_risultati.py` (finito senza errori, «scritto data\schede_risultati.js con 4 schede») → `prova_pagine_r6.py --senza-screenshot`: **0 errori su 12 pagine**. `mappa_torino.html` 13,8 MB.

## git status prima del commit
Modificati: `docs/RAPPORTO_RISULTATO1.txt`, `docs/RAPPORTO_RISULTATO1_CANDIDATI.txt`, `mappa_torino.html`, `scripts/04_genera_mappa.py`, `21_risultato1_vuoti.py`, `22_risultato1_candidati.py`, `RISULTATO1_CANDIDATI.bat`, `mappa_template.html`, `schede_risultati.py` (+ questo esito). Niente `data/`, `.bak` o chiavi.
