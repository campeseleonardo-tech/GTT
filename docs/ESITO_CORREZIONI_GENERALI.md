# Esito correzioni generali (Risultato 6 e progetto)

- Piano eseguito: `docs/PIANO_CORREZIONI_GENERALI.md`
- Inizio: 20/10/2026, ore 01:45
- Ramo: `prova`; pull fast-forward da `83c577c` a `cbb144f` (nessun errore, nessun conflitto)

## Passo 0 — Preparazione

PASSO 0.0: OK — `git checkout prova`, `git fetch`, `git pull --ff-only origin prova` senza errori. Il log contiene i commit «Correzioni generali» (`87bb049`) e «Memoria: … piano e prompt» (`cbb144f`). Esistono `scripts\81_auto_di_passaggio.py`, `scripts\84_risultato6_parcheggi.py`, `scripts\comuni.py`, `scripts\RISULTATO6_RIFAI.bat` e `docs\archivio\r6\`.
- Avviso: `git status` prima del pull mostrava solo file non tracciati (non modifiche a file tracciati): `.claude/`, `immagini/`, `scripts/TRAFFICO_RILANCIA_SENSORI.bat.bak_18ott`, `scripts/rete_osm.py.bak_18ott`. Il pull è andato a buon fine comunque; i due `.bak` restano dove sono.

PASSO 0.1: OK — branch `prova`. Modifiche prima di iniziare: nessuna su file tracciati (vedi avviso sopra).

PASSO 0.2: OK — questo file creato.

PASSO 0.3: OK — copie di sicurezza in `data/backup/`:
- `risultato6_v2_prima_correzioni/` (19 MB)
- `mappa_torino_prima_correzioni.html` (23 MB)
- `schede_risultati_prima_correzioni.js` (64 KB)

PASSO 0.4: OK — numeri di partenza (`data/processed/risultato6_v2/mappa_r6.json`):
- fermate: 378 — 50 posti o più: 172; Pochi posti: 59; Nessun parcheggio: 147
- aree: Critica 37, Scarsa 12, Buona 24
- punti prioritari (20): SETTEMBRINI, PAVESE, INDUSTRIA, METRO SPEZIA, PROVANA, METRO LINGOTTO, POLITECNICO, STATI UNITI, METRO PRINCIPI ACAJA, TRAIANO, MARSÈ, METRO BERNINI, METRO NIZZA, SAN MATTEO, AVELLINO, METRO ITALIA61, XXIV MAGGIO, DROSSO CAP, MACEDONIA, LEONARDO DA VINCI
- parcheggi: 212
- mappa_torino.html prima: 23,6 MB

PASSO 0.5: OK — `import numpy, scipy, pandas, shapely, pyproj, osmium` stampa `ok`. Python 3.14.3. Versioni installate: numpy 2.5.3, scipy 1.18.1, pandas 3.0.6, shapely 2.2.0, pyproj 3.8.0, osmium 4.3.1, networkx 3.7, pypdf 6.20.0, matplotlib 3.11.2.

PASSO 0.6: OK — `python scripts\comuni.py`: 4 righe OK, avvisi 0.

## Fase 1 — Risultato 6: catena nuova

PASSO 1.1: OK — 71, 72, 73 eseguiti senza errori.
- 71: 41 parcheggi 5T nel database; 50.799 righe di occupazione; 4.956 letture scartate. Firme: destinazione 7, pendolare 19, misto 6, nessun dato 4, dato bloccato 3, residenziale 2.
- 72: 36 stazioni treno, 23 fermate metro; 5.087 luoghi, 346 nodi forti; parcheggi: solo sulla carta 4, potenziali 758, non interscambio 2.669.
- 73: 95.297 spostamenti; sensori 5T usabili 89, scartati 23; a2 disponibile in 3.265 luoghi; giro 1: 552 luoghi cambiano a2.
- Nota: 73 non ha stampato l'AVVISO «c2 diverso».

PASSO 1.2: OK — prova veloce 81: arrivata a fine, nessun ERRORE. Nel rapporto: «Metodo per c4: instradamento». Nessun ripiego.

PASSO 1.3: OK — giro completo 81 (53 s di instradamento, 648 origini, durata totale circa 55 s).
- Domanda del mattino: M_cint 87.162 auto (1.039 interviste; persone in auto 95.297, passeggeri esclusi) — minore di 95.297 e maggiore di 50.000 ✓
- M_tor 29.988 auto = 34% di M_cint → **torinesi nella domanda: SI** (soglia 25%)
- f_mattino 5.067 (64 interviste) → quota_mattino 5,8% (fra 5% e 40%) ✓
- Perdita della domanda: 0,0% (soglia 15%) ✓
- Fra i 15 luoghi in cima: 7 su 15 sono strade d'ingresso note (Francia, Unione Sovietica, Genova…) — controllo OK. Osservazione: la lista in cima è dominata da Strada Trieste, Strada Orbassano, Strada Regina Margherita e Potenza; Corso Francia non compare fra i primi 15 (il controllo è passato con 7 su 15).
- 15 luoghi in cima (auto che passano, stimate): Maroncelli (13.119), Maroncelli (11.972), Bosso (11.731), Sangone (11.731 ×2), Lecce (10.838), Regina Margherita (10.838), Ponte Cavalieri Templari (8.904), Trieste Ovest (8.904 ×2), Santa Rita (8.630), Orbassano (8.536 ×2), Settembrini (8.385), Cattaneo Sud (8.024).
- Avviso permanente del modello: traffico V0, stima debole (±38%), solo ordine di grandezza.

PASSO 1.4: OK — 82 eseguito, 6 secondi, nessun ERRORE.
- Catena: trovati 5.205 → aperti 3.431 → fuori dal centro 3.208 → con almeno 20 posti 2.006 → **adatti 1.874** (157.103 posti).
- Aree di destinazione trovate: 328 (retail 213, mall 55, hospital 39, university 17, college 4) ✓ (>50).
- Esclusi per destinazione: retail 81, hospital 31, mall 18, university 2. I 20 più grandi esclusi includono Piazza Paradiso, Il Gialdo, IRCCS Candiolo, Ospedale San Luigi Gonzaga, Ospedale di Rivoli, Millecity, Area 12, Le Fornaci, 45° Nord.
- I 5 interscambi ufficiali fuori centro risultano adatti (controllo OK).
- Nessun parcheggio adatto in zona centrale ✓.

PASSO 1.5: OK — 83 eseguito, nessun ERRORE.
- Luoghi 5.087; eleggibili 3.898 (in zona centrale 527); soglia 63,50; **fermate importanti 391**.
- 391 / 3.898 = 10,0% (atteso circa 10%) ✓. Nessuna fermata importante in Q001-Q009 ✓. c4 presente per tutti gli eleggibili ✓.
- Confronto con S2 (19/10): S2 378, nuove 391, restano 171, entrano 220, escono 207.
- Le prime 30: in cima Metro Marche, Metro Massaua, Metro Paradiso, Stazione Stura, Metro Pozzo Strada, Metro Monte Grappa (tutte Q014/Q019/C003).
- Per zona: Q011 42, Q012 29, C009 27, Q023 27, Q019 26 (le più alte).

PASSO 1.6: OK con AVVISO — 84 eseguito, 1 secondo.
- Fermate importanti per classe (somma 391 ✓): Nessun parcheggio 99 + Posti insufficienti 154 + Posti sufficienti 116 + Poche auto da fermare 22 = 391 ✓.
- Aree: Critica 20, Scarsa 5, Buona 5, Pochi dati 46 (76 aree).
- **20 punti prioritari** (km dal centro; auto che passano; da fermare; posti; mancano): Maroncelli (Moncalieri, 6,3 km; ~13.100; 762; 135; 627), Bosso (Moncalieri, 6,8; ~11.700; 682; 142; 540), Pellerina (Le Vallette, 3,5; ~7.300; 426; 0; 426), Santa Rita (4,0; ~8.600; 501; 117; 384), Ponte Cavalieri Templari (Moncalieri, 7,9; ~8.900; 517; 167; 350), Barbera (Mirafiori Sud, 7,2; ~6.000; 349; 0; 349), Settembrini (Mirafiori Sud, 7,1; ~8.400; 487; 151; 336), Pianezza (Le Vallette, 3,6; ~5.700; 330; 0; 330), Cattaneo (Mirafiori Nord, 6,1; ~8.000; 466; 137; 329), Metro Massaua (Parella, 4,7; ~7.000; 408; 105; 303), Pianezza (Pianezza, 9,6; ~4.700; 271; 0; 271), Villa Luigina (Pino Torinese, 5,5; ~4.600; 266; 0; 266), Svincolo Mirafiori (Mirafiori Sud, 7,8; ~6.900; 402; 151; 251), Gioanetti (Borgo Po e Cavoretto, 1,4; ~4.900; 285; 38; 247), Pasini (Madonna del Pilone, 3,5; ~4.200; 241; 0; 241), Toscana (Le Vallette, 3,7; ~4.100; 238; 0; 238), Rieti Nord (Parella, 6,3; ~7.100; 413; 178; 235), Leonardo da Vinci (Grugliasco, 8,4; ~3.900; 225; 0; 225), Traforo (Pino Torinese, 8,6; ~3.500; 205; 0; 205), Vigliani (Mirafiori Sud, 6,5; ~6.000; 349; 146; 203).
- **AVVISO**: nessun punto prioritario in zona centrale (nessuno a meno di 1,5 km da Piazza Castello). Il controllo è stato scritto così, è un avviso e non un errore; il punto più vicino è Gioanetti a 1,4 km.
- Validazione (5 righe, un esito ciascuna): Caio Mario — il contatore sembra fermo (valore fisso al 2%); Fermi — non trasmette il riempimento; Sofia — poco usato nonostante molte auto in entrata (da capire); Stura — coerente: sempre pieno (80% di notte, 90% di giorno); Venchi Unica — a metà (51%), non si può dire.
- Controllo a posteriori Fermi: nessun parcheggio adatto nel raggio trasmette il riempimento → non può confermare.
- Sensibilità: raggio 300/400/500 m; quota ×0,5/×1/×2; soglia fermate 5% → 197, 15% → 586.

PASSO 1.7: OK — 79 eseguito. `mappa_r6.json` = 334.608 byte (327 KB), sotto 1,5 MB. Aree 76, punti 20, fermate 391, parcheggi 142, profili 5. Avvisi 0.

PASSO 1.8: OK — 85 eseguito. **Verifiche non superate: 0.** Tutte le verifiche OK (M_cint, M_tor, f_mattino rifatti con pandas; instradamento 2 origini uguale a networkx, differenza 0,000; 8 c4 rifatti a mano; 8 punteggi rifatti; 391 fermate dalla soglia; 8 classi rifatte a mano; 8 regole «adatto»; nessuna fermata importante né parcheggio adatto in Q001-Q009; ogni fermata in una sola area). Rapporto: `docs/RAPPORTO_R6_VERIFICHE_CORREZIONI.txt`.
- Punti prioritari vicini al centro (solo informazione): a meno di 2,5 km da Piazza Castello c'è 1 solo punto (Gioanetti). Prima erano 7.

## Fase 2 — Mappa, schede, prova delle pagine

PASSO 2.1: OK — `04_genera_mappa.py` eseguito (circa 67 s), nessun AVVISO.
- `mappa_torino.html`: **13,6 MB** (prima 23,6 MB; atteso circa 13 MB) ✓.
- Date di riferimento nel file: 2026-11-10 (martedì), 2026-11-14 (sabato), 2026-11-15 (domenica) ✓.
- Dati caricati: 8.317 sezioni di censimento abitate (1.557.493 abitanti); velocità 137 linee; GTFS: 13.683 corse feriali; 112 sensori 5T; avvisi GTT attivi 110/134; nomi comuni 69 su 69.
- Risultato 6 nel riepilogo: 76 aree, 20 punti prioritari, 391 fermate importanti, 142 parcheggi.

PASSO 2.2: OK — `schede_risultati.py` eseguito senza errori. Scritto `data\schede_risultati.js` con 6 schede (R1, R2, R4, R6, R8, R9), 59 KB.
- R6: «Parcheggi per lasciare l'auto» — 4 numeri, 7 grafici.

PASSO 2.3: OK — `prova_pagine_r6.py` finito con **«OK: nessun errore a runtime sulle 13 pagine»**. Browser: Microsoft Edge. Mappa in 11 temi/viste: 0 righe di errore ciascuna (DOM circa 13,6 milioni di caratteri). Scheda: 0 errori (DOM 38.786 caratteri). Identificatori r6/R6 non definiti: nessuno. Etichette della vista aree: 18, nessun nome ripetuto.
- Screenshot creati: `immagini\r6_parcheggi.png` (478 KB), `immagini\r6_aree.png` (498 KB), `immagini\r6_mancano.png` (463 KB) — tutti sopra 20 KB.

PASSO 2.4: OK — controllo testi pubblici R6 in `data\schede_risultati.js`: risultato `[]` (nessuna parola vietata: utile, osservazione, versione, scenario, S2, S4, nodo forte, fonte_stato, sempre pieno).

## Fase 3 — Piccole cose rimaste

PASSO 3.1: OK — in `data\ref\parcheggi_osservazioni.json` aggiunto il campo `"nota"` alla voce di Fermi (nessuna coordinata, raggio o stato cambiati; JSON valido). Poi rilanciati 84 e 79 (79: `mappa_r6.json` 327 KB, avvisi 0).
- Riga «Controllo a posteriori»: Fermi — nessun parcheggio adatto nel raggio trasmette il riempimento → **non può confermare**. Adatti nel raggio 500 m: 11 (1.520 posti); gratuiti 7 (1.112 posti).
- La nota non entra in mappa né nelle schede: resta solo come controllo, come chiesto.

PASSO 3.2: OK — `RISULTATO2_RICALCOLA_NUMERI.bat` eseguito (pochi secondi; log in `logs\29_risultato2_metro_notte.log`), poi `schede_risultati.py` senza errori.
- `notte15`: residenti migliorati 773.307; con quota minima (+25%) 334.085.
- `notte30`: residenti migliorati 652.891; con quota minima 153.062.
- Il secondo (30 min) è minore del primo in entrambi i casi.

PASSO 3.3: OK — aggiunta la chiave `"in_english"` (4 frasi: domanda, due o tre frasi di risposta con gli stessi numeri, «Limits: …») a R1 (`scheda_r1`), R2 (`arricchisci_r2`), R4 (`scheda_r4`), R8 (`scheda_r8`), R9 (`scheda_r9`). R6 la aveva già. Rilanciati `schede_risultati.py` e `prova_pagine_r6.py --senza-screenshot` (OK, nessun errore).
- Esempio R1 (prodotto): «10,919 residents out of 848,748 (1.3%) lack at least one of the 5 services within 15 minutes on foot. The most often missing one is health, with 9,104 residents without a nearby service of that kind.»
- Righe cambiate in `scripts\schede_risultati.py`: aggiunto il dizionario `GRUPPI_EN` (5 nomi di gruppo in inglese, solo per la frase R1); aggiunto `"in_english"` nei dizionari di R1, R2, R4, R8, R9.

PASSO 3.4: OK — `86_prepara_pubblicazione.py` eseguito, avvisi 0; cartella `pubblica\` 90 MB, 20 file (mappa, simulazione, dati; nessun file mancante). `prova_pagine_r6.py --cartella pubblica --senza-screenshot`: OK, nessun errore.
- Creato `README.md` nella radice del progetto (file non tracciato; **non pubblicato**). Osservazione per Leo: nel README i numeri in grassetto non hanno il punto delle migliaia («10919 residenti», «773307 residenti») mentre nel testo sotto sì («10.919», «773.307»). Cosmetico; non cambiato.

PASSO 3.5: **ALLARME** (la raccolta su leopi risponde, ma un flusso è fermo) — `CONTROLLA_LEOPI.bat` eseguito alle 01:56. Pi raggiungibile. Uscita:
- `mezzi_gtt`: ultima lettura 20/10 01:55 (da 1 min)
- `trip_update_gtt`: ultima lettura 19/10 23:59 (da 117 min)
- `flussi_5t`: ultima lettura 20/10 01:50 (da 6 min)
- `occupazione_pk`: ultima lettura 20/10 01:54 (da 2 min)
- `ztl_5t`: ultima lettura **14/10 15:11** (da 7.845 min) — **FERMA**
- Comando per farlo girare ogni mattina (NON eseguito; lo lancia Leo):

```bash
schtasks /create /tn "GTT controlla leopi" /tr "C:\projects\Progetti\GTT\scripts\CONTROLLA_LEOPI.bat" /sc daily /st 08:00
```

PASSO 3.6: OK — `RISULTATO6_RIFAI.bat` eseguito dalla prima all'ultima fase, senza ERRORE. Durata circa **4 minuti** (01:56:31 → 02:00:38). Log in `logs\risultato6_rifai.log`. Unico AVVISO: «nessun punto prioritario in zona centrale» (vedi 1.6). Prova delle pagine: «OK: nessun errore a runtime sulle 13 pagine». Verifiche 85: «Verifiche non superate: 0».
- Il `.bat` finisce con `pause`: lanciato senza tastiera, si è chiuso da solo.

## Fase 4 — Esito

### 4.1 Prima / dopo

| Cosa | Prima (passo 0.4) | Dopo (esecuzione di oggi) |
|---|---|---|
| Fermate importanti (fuori centro) | 378 — «50 posti o più» 172, «Pochi posti» 59, «Nessun parcheggio» 147 (classi vecchie) | **391** — posti sufficienti 116, posti insufficienti 154, nessun parcheggio 99, poche auto da fermare 22 |
| Aree | Critica 37, Scarsa 12, Buona 24 (73) | Critica 20, Scarsa 5, Buona 5, **Pochi dati 46** (76) |
| Punti prioritari | 20 (lista vecchia) | 20 (lista nuova, sotto): in comune solo Settembrini e Leonardo da Vinci |
| Parcheggi in mappa | 212 | 142 |
| `mappa_torino.html` | 23,6 MB | **13,6 MB** |
| `mappa_r6.json` | non misurato | 327 KB |

Le classi vecchie e nuove non coincidono nei nomi: il confronto è indicativo.

**I 20 punti nuovi** (zona IMQ; km dal centro; auto che passano; da fermare; posti; posti che mancano):
1. Maroncelli — Moncalieri; 6,3 km; ~13.100; 762; 135; 627
2. Bosso — Moncalieri; 6,8 km; ~11.700; 682; 142; 540
3. Pellerina — Le Vallette; 3,5 km; ~7.300; 426; 0; 426
4. Santa Rita — 4,0 km; ~8.600; 501; 117; 384
5. Ponte Cavalieri Templari — Moncalieri; 7,9 km; ~8.900; 517; 167; 350
6. Barbera — Mirafiori Sud; 7,2 km; ~6.000; 349; 0; 349
7. Settembrini — Mirafiori Sud; 7,1 km; ~8.400; 487; 151; 336
8. Pianezza — Le Vallette; 3,6 km; ~5.700; 330; 0; 330
9. Cattaneo — Mirafiori Nord; 6,1 km; ~8.000; 466; 137; 329
10. Metro Massaua — Parella; 4,7 km; ~7.000; 408; 105; 303
11. Pianezza — Pianezza; 9,6 km; ~4.700; 271; 0; 271
12. Villa Luigina — Pino Torinese; 5,5 km; ~4.600; 266; 0; 266
13. Svincolo Mirafiori — Mirafiori Sud; 7,8 km; ~6.900; 402; 151; 251
14. Gioanetti — Borgo Po e Cavoretto; 1,4 km; ~4.900; 285; 38; 247
15. Pasini — Madonna del Pilone; 3,5 km; ~4.200; 241; 0; 241
16. Toscana — Le Vallette; 3,7 km; ~4.100; 238; 0; 238
17. Rieti Nord — Parella; 6,3 km; ~7.100; 413; 178; 235
18. Leonardo da Vinci — Grugliasco; 8,4 km; ~3.900; 225; 0; 225
19. Traforo — Pino Torinese; 8,6 km; ~3.500; 205; 0; 205
20. Vigliani — Mirafiori Sud; 6,5 km; ~6.000; 349; 146; 203

**Punti vicini al centro:** a meno di 2,5 km da Piazza Castello ce n'è **1** (Gioanetti, 1,4 km). Prima erano **7**. Nessun punto a meno di 1,5 km: è l'AVVISO del passo 1.6, previsto dal controllo.

**Torinesi nella domanda: SI.** Auto dai quartieri periferici di Torino verso Q001-Q009: 29.988 = **34%** delle auto che entrano (87.162). Soglia 25%. La decisione è automatica (script 81).

**Tabella di validazione** (5 interscambi del Comune):

| Interscambio | Posti | Stato misurato | Esito |
|---|---|---|---|
| Caio Mario | 418 | libero, valore fisso (2%) | non si può dire: il contatore sembra fermo |
| Fermi | 300 | non trasmette | non si può dire |
| Sofia | 272 | libero (55% di notte, 32% di giorno) | da capire: molte auto accanto, poco usato |
| Stura | 589 | pieno (80% di notte, 90% di giorno) | coerente: pieno su strada trafficata |
| Venchi Unica | 437 | a metà (51%) | non si può dire |

**Sensibilità** (script 84, nel rapporto): raggio 300/400/500 m; quota ×0,5 / ×1 / ×2; soglia fermate 5% → 197, 15% → 586 fermate.

**Da leggere con cautela:**
- Il modello del traffico è una stima (±38%): le auto sono ordini di grandezza.
- Nei 15 luoghi con più auto in entrata (passo 1.3) in cima ci sono soprattutto Strada Trieste, Strada Orbassano e Regina Margherita; Corso Francia non è fra i primi 15 (il controllo passa lo stesso: 7 su 15).
- 46 aree su 76 sono «Pochi dati».

### 4.2 Testo per la memoria (NON applicato: lo aggiorna Claude dopo il controllo)

Sezione 4, riga del Risultato 6:
> **Risultato 6 — Parcheggi per lasciare l'auto (corretto 20/10/2026).** 391 fermate importanti fuori dal centro (10% più alto fra 3.898 luoghi eleggibili); 253 senza posti bastanti entro 400 m a piedi per le auto in entrata che passano accanto. 20 punti prioritari (solo 1 a meno di 2,5 km dal centro). Torinesi nella domanda: sì (34% delle auto in entrata). Quota di chi lascia l'auto: 5,8% (IMQ 2022). Verifiche indipendenti (script 85): 0 non superate. Stime del traffico con errore tipico ±38%. Riempimento misurato su pochi giorni e solo dove il 5T lo trasmette.

Sezione 3, «prossimo numero libero»: **87**.

### 4.3 `git status`

```
 M docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt
 M mappa_torino.html
 M requirements.txt
 M scripts/schede_risultati.py
?? README.md                      (creato dal passo 3.4, non pubblicato)
?? docs/ESITO_CORREZIONI_GENERALI.md
?? docs/RAPPORTO_R6_AUTO_PASSAGGIO.txt
?? docs/RAPPORTO_R6_FERMATE_IMPORTANTI.txt
?? docs/RAPPORTO_R6_PARCHEGGI.txt
?? docs/RAPPORTO_R6_PARCHEGGI_ADATTI.txt
?? docs/RAPPORTO_R6_VERIFICHE_CORREZIONI.txt
?? .claude/, immagini/, scripts/*.bak_18ott   (presenti già prima di iniziare)
```
Nessun commit.

### 4.4 File cambiati a mano (riga per riga)

- `requirements.txt`: aggiunte le versioni esatte (`==`) a numpy, scipy, pandas, shapely, pyproj, osmium, pypdf, networkx, matplotlib.
- `data/ref/parcheggi_osservazioni.json`: aggiunto il campo `"nota"` alla voce di Fermi (passo 3.1). Nient'altro.
- `scripts/schede_risultati.py`: aggiunto `GRUPPI_EN` (5 nomi di gruppo in inglese) e il campo `"in_english"` in R1, R2, R4, R8, R9 (passo 3.3). Nessuna soglia, nessun testo italiano cambiato.
- Nessun errore piccolo da correggere: tutti gli script sono girati così come sono.

I file generati (`mappa_torino.html`, `data/schede_risultati.js`, `data/processed/...`, `docs/RAPPORTO_*`, `logs/`, `immagini/r6_*.png`, `pubblica/`, `README.md`) non sono stati modificati a mano. Copie di sicurezza in `data/backup/` (passo 0.3).

### Fine

Esecuzione completa dalle 01:45 alle 02:01 circa.
