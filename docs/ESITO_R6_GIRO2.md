# Esito R6 - Giro 2 (20/10/2026)

Partenza: ramo `prova`, working tree pulito, `git pull` ok. Il piano (sezioni «Esito del prompt C» e «Giro 2») stava solo sul ramo
cloud `claude/festive-noether-tjjecr`: Leo l'ha unito in `prova` prima di questo giro (commit 25b6228, 6422e5b).
`MEMORIA_PROGETTO.md` non toccata.

## Riepilogo
| Passo | Esito |
|---|---|
| 1. Script 87, arrivi per km² | OK (3 AVVISO attesi: zone con dati scarsi, ecc.) |
| 2. Script 88, confronto_sensori.json | OK |
| 3. Script 83, regola fissa N 10 / M 1.000 | OK: 274 fermate = riga N 10, M 1.000 della proposta |
| 4. Script 84, criterio «Fermate importanti» | OK |
| 5. Script 79 e template: linee utili nel pannello, testo della guida | OK |
| 6. schede_risultati.py: regola e riga dei sensori | OK |
| 7. Catena (.bat), controlli A e B dell'85, rilancio | OK, 0 verifiche non superate, 0 errori nelle pagine |

## Passo 1 - scripts/87_popolarita_zone.py
- Aggiunta `MIN_INTERVISTE = 50` e `superficie_km2(anelli)`. **Differenza dal piano:** nel file i poligoni sono liste di anelli
  senza distinguere buchi e parti separate, e il «sottrai gli anelli interni» per contenimento dava aree negative (R307). Uso la
  somma con segno della formula del poligono (gli anelli esterni hanno tutti lo stesso verso, i buchi il verso opposto): 9 zone
  hanno buchi, nessuna perde più di metà superficie. Controlli: nessuna superficie ≤ 0 OK; **zone di Torino (Q…) 129,3 km²**
  (fra 120 e 135) OK.
- `popolarita` = arrivi / km² (restano `arrivi`, `km2`); `dati_scarsi` se meno di 50 righe IMQ di arrivo (3 zone su 101 nella
  Città metropolitana: AVVISO). (a), (b) delle linee e linee utili dei parcheggi ricalcolati con la nuova popolarità; anche le
  5 zone per gruppo di scopo sono per km². Rapporto: colonne arrivi, km², arrivi/km², riga «dati scarsi».
- Prima → dopo: prime 5 zone Centro, Nizza Millefonti, Moncalieri, Rivoli, Parella → **Centro (44.404 arrivi/km²), San Paolo
  (21.346), Cenisia (19.477), San Donato (18.535), Nizza Millefonti (17.672)**. Moncalieri, Rivoli, Collegno non sono più in cima.
- Linee in testa per (a): 1085 (12), 2 (11), 93/ (10), 91 (9), 24 (8). Linee utili: 54 (come prima), soglia (a) = 4.
- Parcheggi adatti senza linea utile entro 400 m: 1.264 su 1.874 (prima 1.123; AVVISO).

## Passo 2 - scripts/88_confronto_auto_sensori.py
Aggiunti `OUT_JSON` (`data/processed/risultato6_v2/confronto_sensori.json`), `import time` e la scrittura finale. Contenuto:
`rho_a 0.833, rho_b 0.596, rho_b_senza_fuori_rete 0.517, n_a 33, n_b 27, n_b_senza_fuori_rete 23, generato`.

## Passo 3 - scripts/83_fermate_importanti.py
- Prima: `PERCENTUALE = 10.0`, `scelti` = 10% più alto. Dopo: `N_CORSE = 10`, `M_AUTO = 1000` (commento «Leo, 20/10: regola fissa al
  posto del 10% più alto»), funzione `regola(...)`, lettura di `nodi.json` (`metro`, `ferro`, `capolinea`).
- `--percentuale` default `None` (se data: vecchia regola, con il vecchio controllo). `alternative`: `N10_M500` (347), `N10_M2000`
  (201), `N15_M1000` (136). Sensibilità: `solo_nodi_e_corse` (531 fermate; 257 entrano, 0 escono), `senza_nodi` (261; 0 entrano, 13
  escono), `c4_ripiego`. `parametri.regola = {n_corse, m_auto}`; `soglia` = null con la regola. Rapporto: riga della regola.
- Controllo: fermate importanti = 274 = riga N 10, M 1.000 di `RAPPORTO_R6_PROPOSTA_FERMATE.txt` (letto dal file): OK.
- Controllo vecchio dell'85 («numero di fermate dalla soglia») non applicabile con la regola: lo ha sostituito il controllo A (vedi passo 7).

## Passo 4 - scripts/84_risultato6_parcheggi.py
- Criterio «Fermate importanti» (prima «il 10% più alto del punteggio… (N fermate)») → «fuori dal centro, con metro, stazione o
  capolinea oppure almeno 10 corse all'ora nelle ore dei pendolari, e almeno 1.000 auto in entrata che passano accanto (274
  fermate)», perché «un parcheggio per lasciare l'auto serve dove passa un mezzo frequente e passano molte auto in entrata»; effetto
  con le tre varianti. N, M, X letti dai dati. Aggiunto `regola_fermate` al riepilogo (vicino a `n_eleggibili`).

## Passo 5 - scripts/79_dati_mappa_r6.py e mappa_template.html
- 79: non esiste `CAMPI_PARCHEGGIO`; aggiungo `linee_utili` e `linee_utili_txt` (prime 8 linee) direttamente a ogni parcheggio adatto
  di `d["parcheggi"]` leggendo `popolarita_zone.json`; se manca il file, AVVISO e campi assenti. mappa_r6.json: 340 KB (< 1,5 MB).
- Template: riga «Linee utili a meno di 400 m» = `N (linee…)` in `r6SchedaParcheggio`, frase «Linea utile: tocca molte delle zone dove
  arriva più gente per km² (indagine IMQ 2022, esclusi i ritorni a casa).» nell'approfondimento, testo della guida sostituito
  (nella mappa generata: 0 occorrenze del vecchio «10% più alto per punteggio»).

## Passo 6 - scripts/schede_risultati.py (`scheda_r6`)
Metodo, parametri e `in_english` con la regola (N, M dal riepilogo); nei limiti, e in inglese, la riga dei sensori:
«ρ = 0,52 su 23 luoghi; sottostima gli ingressi da nord-ovest» (da `confronto_sensori.json`). Nessun «10% più alto» rimasto nella scheda.

## Passo 7 - catena e controlli
- `RISULTATO6_RIFAI.bat`: aggiunti `88_confronto_auto_sensori` dopo 81 e `87_popolarita_zone` dopo 82; commento dell'ordine aggiornato.
- 85: controllo A (ogni fermata importante rispetta la regola, ricalcolata da nodi/segnali/auto con N e M del file; nessuna mancante):
  **OK, 274 attese contro 274**. Controllo B (la guida contiene «almeno 10 corse» e «almeno 1.000 auto»): **OK**.
- Rilancio `scripts\RISULTATO6_RIFAI.bat`: nessun errore.

### Numeri dopo il rilancio (prima → dopo)
- Fermate importanti: 391 → **274** (attese 274).
- Senza posti bastanti: 253 su 391 → **179 su 274** (68 senza nessun parcheggio, 111 con posti insufficienti, 95 sufficienti).
- Punti prioritari: 15 → **12**: Santa Rita, Metro Massaua, Ponte Cavalieri Templari, Regina Margherita, Pasini, Leonardo da Vinci,
  Drosso Cap, Stura Lazio, Marsè, Derna Est, Ferrara, Zara.
- Verifiche dell'85: **0 non superate** (44 righe OK).
- Prova delle pagine: **0 errori su 12 pagine**, nessun identificatore non definito.
- `mappa_torino.html`: 13.763.259 byte (13,8 MB; prima 13.820.331).
- 5 zone più popolari (arrivi per km²): Torino-Centro, Torino-San Paolo, Torino-Cenisia, Torino-San Donato, Torino-Nizza Millefonti.

### AVVISI del log (esclusi i doppioni)
- AVVISO fermate usate dalle linee fuori da ogni zona IMQ — 30 su 7043 (non contano per nessuna zona)
- AVVISO parcheggi adatti senza nessuna linea entro 400 m a piedi — 495 su 1874
- AVVISO parcheggi adatti senza nessuna linea utile entro 400 m a piedi — 1264 su 1874
- AVVISO punti OSM della cintura fuori da ogni zona IMQ — 1
- AVVISO punti del catalogo comunale in zone fuori Torino (atteso 0: il catalogo e' di Torino) — 165 punti in C002 (50), C003 (2), C004 (1), C007 (13), C009 (96), C011 (1), C066 (2)
- AVVISO sensori senza strada della rete entro 50 m — 6: 3717 SS10 Padana Inferiore, 3718 SS10 Padana Inferiore, 35559 SP13 di Front, 35560 SP13 di Front, 11432 SS460 Di Ceresole, 11433 SS460 Di Ceresole
- AVVISO sensori su strada della rete ma modello = 0 — 2: 35518 SP122 di Chieri, 35519 SP122 di Chieri
- AVVISO zone della Citta' metropolitana con dati scarsi (meno di MIN_INTERVISTE righe di arrivo) — 3 su 101

Gli AVVISO sono gli stessi dei giri precedenti più due nuovi attesi dal Giro 2 (zone con dati scarsi; parcheggi senza linea utile).
`git status` prima del commit: modificati script 79, 83, 84, 85, 87, 88, `.bat`, template, `schede_risultati.py`, rapporti rigenerati
e `mappa_torino.html`; nessun file di `data/` o `.bak`.
