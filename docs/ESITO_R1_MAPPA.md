# Esito Risultato 1, fase B (mappa 0-5) — 20/10/2026

Ramo `prova`, `git status` pulito e `git pull` già aggiornato all'inizio. Python del PATH.

## PASSO 1 — `scripts/21_risultato1_vuoti.py`: OK
- `n_mancanti_sezione`: ora ritorna `(n_v2, n_piedi, tp_ok, m)`. Prima: `n_v2 = n_piedi = 0` e `return n_v2, n_piedi, tp is not None`;
  dopo: `n_v2 = n_piedi = m = 0`, ciclo con `enumerate(GRUPPI)`, `m |= int(manca) << i`, `return n_v2, n_piedi, tp is not None, m`.
- `calcola_v2`: chiamata adattata (`n2, n_piedi, tp_ok, m = ...`); `per_sez.append` ora ha `"m": m` e `"poco"`.
- `v2` ha `"ordine_bit": GRUPPI` e `"sezioni_critiche_torino"` (id, res, densita, n_mancanti, mancano), ordinate per residenti decrescenti.
- `righe_rapporto_v2`: in coda la sezione «SEZIONI CRITICHE DI TORINO (abitate, 3+ mancanti)» e «da guardare a mano con Leo (lavoro 7)».
- Controlli stampati: OK bit accesi = n_mancanti (0 sezioni diverse); OK somma residenti sezioni critiche 751 = titolo 751 (7 sezioni).

## PASSO 2 — `scripts/04_genera_mappa.py`: OK
- Dopo la lettura di `fb_data`: costruiti `r1` e `r1_meta` dalla sezione `v2` (se manca: `r1 = {}`, `r1_meta = None`, riga AVVISO).
- In `sez`: aggiunto `"r1": r1.get(x.get("id",""))`. Nel dizionario dati: `"r1_meta": r1_meta,`.
- Nota: le sezioni di `sez` non hanno l'`id`, quindi il controllo (somma di `p` con id `1272…`, `r1` presente, `poco == 0`, `n >= 3`) rilegge `sezioni_torino.json`.
- Uscita: `OK: titolo risultato 1: 751 residenti di Torino abitati con 3+ servizi mancanti (script 21: 751); sezioni con r1: 8317`.

## PASSO 3 — `scripts/mappa_template.html`: OK
1. Proiezione sezioni: `fb:z.fb||{},` → `fb:z.fb||{}, r1:z.r1||null,`.
2. `PAL_SEZ.r1` (6 colori) e `r1Manca(z,g)` aggiunti dopo `PAL_SEZ.fb` (senza dati v2 ricade sullo «zero» della v1). Commento di `PAL_SEZ.fb`: «2=zero» → «2=manca».
3. Menu: prima voce `["tutti","Quanti servizi mancano (0-5)"]`; `OPT_VAL` `subFbGruppo:"salute"` → `"tutti"`.
4. Disegno: `pal` ora scelta dopo `fbGruppo` (`PAL_SEZ.r1` per `tutti`); `nulla` per `fbGruppo`: `tutti` → grigio se `!z.r1` o `z.r1[2]===1`, gruppi → grigio se poco abitata; colore `tutti` = `z.r1[0]`, gruppi = `r1Manca ? 2 : pochissimo ? 1 : 0`.
5. `legendaFb`: ramo `tutti` (titolo, 6 riquadri 0…«5 (tutti)», riquadro grigio con soglia da `D.r1_meta.soglia`, riga su Torino/cintura); gruppi: «nessuno a 15 min a piedi» → «manca» + riquadro grigio.
6. `schedaSezione` ramo `fb`: `tutti` → «N servizi mancanti su 5» / «Zona poco abitata: fuori dal conteggio», stato = nomi dei servizi o «nessuno»; gruppi → «Manca» / «Pochissimi» / «Presente». Dettagli «Abitanti per km²» e «Regola» aggiunti per `fam === "fb"`. Testo di approfondimento sostituito come da piano (soglia da `D.r1_meta`).
7. Tooltip: `tutti` → «N mancanti» / «poco abitata»; gruppi → «Poco abitata» / «Manca» / «Pochissimo» / «Ok».
8. Righe con `$("subFbGruppo")?.value||"salute"` controllate: disegno (~1152), `legendaFb`, scheda gruppo (`schedaSezione`), `gOsm` (~1658), candidati al passaggio (~1793), tooltip (~1910). Con `tutti`: `fbCandidati["tutti"]` e `NOTA_OSM["tutti"]` non esistono → nessun candidato né nota OSM. OK.
9. Descrizione del tema `faseb` sostituita con la frase del piano.
10. Altre frasi su `pochissim` / `Dove mancano i servizi`: riga 1049 «Dove mancano più posti» è di un altro tema (non toccata); le altre erano già coperte dai punti 5-7. Nessuna ulteriore modifica.

## PASSO 4 — `scripts/schede_risultati.py`: OK (codice) / vedi AVVISO passo 5
- `"mappa"."nota"` sostituita come da piano.
- `in_english`: «Limits: only the City of Turin is covered…» riscritta (cintura valutata con a piedi 15 min o mezzo pubblico 45 min alle 8; dato OSM meno completo). Nessun numero scritto a mano.

## PASSO 5 — Lanci
1. `21_risultato1_vuoti.py`: OK, tutti i controlli `v2 OK` (vedi sopra; somme per ambito e soglia uguali ai residenti, densità negative 0, sezioni senza superficie 0, cintura senza TP 0). Scritti `risultato1_vuoti.json` (1094 KB) e `docs/RAPPORTO_RISULTATO1.txt` con la nuova sezione «SEZIONI CRITICHE» (7 sezioni: 12720005328, 12720000972, 12720003044, 12720003783, 12720003836, 12720006938, 12720005880).
2. `04_genera_mappa.py`: OK. `mappa_torino.html` 13.692.378 → 13.802.275 byte (+0,11 MB, nell'atteso). Contiene `r1_meta` con soglia 1000.
3. `schede_risultati.py`: **AVVISO / FERMO** — `KeyError: 'cibo'` in `scheda_r1` (riga 124, `c = cand[g]`). Il file dei candidati ha solo `salute` e `scuole`, ma `scheda_r1` scorre tutti e 5 i gruppi. Il problema c'era già prima delle mie modifiche (verificato con `git stash`: stesso errore). Non l'ho risolto perché non è nei passi; probabile causa: i candidati per cibo/fermate/verde non sono ancora stati calcolati (script 22). Le schede quindi **non sono state rigenerate** (restano quelle di prima, con il testo vecchio della nota/Limits).
4. `prova_pagine_r6.py --senza-screenshot`: OK, 0 errori su 12 pagine (incluso il tema `faseb`).

## git status prima del commit
Modificati: `docs/RAPPORTO_RISULTATO1.txt`, `mappa_torino.html`, `scripts/04_genera_mappa.py`, `scripts/21_risultato1_vuoti.py`, `scripts/mappa_template.html`, `scripts/schede_risultati.py` (+ questo esito). Nessun file in `data/`, `.bak` o chiavi.
