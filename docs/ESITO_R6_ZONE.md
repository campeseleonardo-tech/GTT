# Esito R6 zone (piano `PIANO_R6_ZONE.md`)

Eseguito il 19/10/2026 sul ramo `prova`. Nessun commit. `MEMORIA_PROGETTO.md` non toccata (il piano lo vieta).

## Esito per fase

- **FASE 1: OK** — script `80_porte_interscambio.py` riscritto: osservazioni tolte da stato, posti utili, criteri e sensibilità; calcolo per zona; verifica a posteriori nel rapporto; sensibilità aggiornata; soglia fermate ricalcolata con lo script 75.
- **FASE 2: OK** — `79_dati_mappa_r6.py`: `mappa_r6.json` (281.925 byte) con zone (29), fermate (378), parcheggi (349), riepilogo, criteri. Via `direzioni`, `direzione`, `fonte_stato`, `fonte_testo`.
- **FASE 3: OK (solo controlli di codice)** — mappa rigenerata (`mappa_torino.html`, 23,6 MB). Tre viste: «I parcheggi che ci sono», «Disponibilità di parcheggio per zona» (nuova, sostituisce «Dove i parcheggi non bastano»), «Dove non ci sono parcheggi». I tre blocchi script superano `node --check`. **Non verificata nel browser**: il browser integrato non riesce ad aprire né `localhost` né il file (vedi Anomalie).
- **FASE 4: OK** — scheda R6 riscritta (numero chiave, risposta a 4 frasi, grafici, criteri, metodo, limiti). `data/schede_risultati.js` rigenerato, `node --check` OK. `simulazione.html` non richiedeva modifiche.
- **FASE 5: OK** — grep dei resti: nessun «osservazione», «non_bastano», «spicchio», «fonte_stato» né «direzione» nella mappa e nella scheda. Le sole occorrenze nel codice sono in `80` (controllo a posteriori e campo interno che `79` non copia). `data/ref/parcheggi_osservazioni.json` non modificato.

## Numeri chiave (dal file, ricontrollati)

- Fermate importanti: **378**
- Senza parcheggio utile (meno di 50 posti liberi a 200 m): **207**
  - nessun parcheggio: **147**
  - parcheggio piccolo o pieno (1-49 posti liberi): **60**
  - parcheggio utile (50 o più): **171**
- Zone IMQ con fermate importanti: **29** — Critica **10**, Scarsa **10**, Buona **9**
- Parcheggi pieni di giorno [MISURATO]: **9**, per **3.041** posti
- Quota dei posti con riempimento misurato: **36,3%**
- Auto in entrata al mattino (riferimento): **95.297** [STIMATO IMQ 2022]; domanda 24.459

## Tabella delle zone

Ordinate per quota di fermate senza parcheggio utile. «Indicativo» = meno di 3 fermate.

| Zona | Tipo | Fermate | Senza nessun parcheggio | Piccolo o pieno | Quota senza parcheggio utile | Categoria |
|---|---|---:|---:|---:|---:|---|
| Rivalta di Torino | comune | 2 | 2 | 0 | 100% | Critica (indicativo) |
| San Mauro Torinese | comune | 2 | 0 | 2 | 100% | Critica (indicativo) |
| Cambiano | comune | 1 | 0 | 1 | 100% | Critica (indicativo) |
| Barriera di Milano | quartiere di Torino | 1 | 1 | 0 | 100% | Critica (indicativo) |
| San Donato | quartiere di Torino | 19 | 13 | 3 | 84% | Critica |
| Crocetta | quartiere di Torino | 23 | 15 | 3 | 78% | Critica |
| San Salvario | quartiere di Torino | 4 | 1 | 2 | 75% | Critica |
| Mirafiori Nord | quartiere di Torino | 14 | 6 | 4 | 71% | Critica |
| Mirafiori Sud | quartiere di Torino | 34 | 19 | 5 | 71% | Critica |
| Cenisia | quartiere di Torino | 18 | 10 | 1 | 61% | Critica |
| Parella | quartiere di Torino | 31 | 11 | 7 | 58% | Scarsa |
| Grugliasco | comune | 21 | 11 | 1 | 57% | Scarsa |
| Pozzo Strada | quartiere di Torino | 7 | 4 | 0 | 57% | Scarsa |
| Aurora | quartiere di Torino | 7 | 2 | 2 | 57% | Scarsa |
| Nizza Millefonti | quartiere di Torino | 35 | 16 | 3 | 54% | Scarsa |
| Collegno | comune | 23 | 8 | 4 | 52% | Scarsa |
| Moncalieri | comune | 64 | 17 | 15 | 50% | Scarsa |
| Beinasco | comune | 8 | 2 | 2 | 50% | Scarsa |
| Borgata Vittoria | quartiere di Torino | 4 | 2 | 0 | 50% | Scarsa |
| Venaria Reale | comune | 9 | 2 | 2 | 44% | Scarsa |
| Madonna di Campagna | quartiere di Torino | 4 | 1 | 0 | 25% | Buona |
| Nichelino | comune | 9 | 1 | 1 | 22% | Buona |
| Rivoli | comune | 17 | 3 | 0 | 18% | Buona |
| Chieri | comune | 6 | 0 | 1 | 17% | Buona |
| Falchera | quartiere di Torino | 8 | 0 | 1 | 12% | Buona |
| Settimo Torinese | comune | 4 | 0 | 0 | 0% | Buona |
| Mercati Generali | quartiere di Torino | 1 | 0 | 0 | 0% | Buona (indicativo) |
| San Paolo | quartiere di Torino | 1 | 0 | 0 | 0% | Buona (indicativo) |
| Vanchiglia | quartiere di Torino | 1 | 0 | 0 | 0% | Buona (indicativo) |

Nota: la zona di Collegno (C003, dove si trova Fermi) ha quota 52%, Scarsa. Il nome «Moncalieri» con 32 fermate senza parcheggio utile è il più alto nella tabella dei grafici.

## Sensibilità delle zone e delle fermate

- Soglia delle fermate (script 75, verificata): **5%** → 177 fermate (91 senza parcheggio utile); **10%** → 378 (207), che coincide con S2 (controllo OK); **15%** → 580 (327).
- Soglia del parcheggio utile: 30 posti → 170 senza; 50 → 207; 100 → 263.
- Distanza: 100 m → 316 senza; 200 m → 207; 400 m → 69.
- Riempimento senza correzione: 206 senza (contro 207 con la correzione): il riempimento cambia pochissimo il risultato.
- Soglie delle zone: 60/30 → Critica 10, Scarsa 10, Buona 9 (scelta usata); 50/25 → 19, 2, 8; 66/33 → 9, 11, 9.

## Verifica a posteriori (non entra nei dati mostrati)

Osservazione di Leo: **Fermi (capolinea metro, Collegno)**, raggio 500 m, «sempre pieno».
- Parcheggi considerati entro 500 m: 20 (2.803 posti nominali).
- Parcheggi misurati dal 5T nel raggio: **nessuno**.
- Zona che contiene il punto: Collegno, quota senza parcheggio utile 52%, Scarsa.
- Direzione: Ovest (categoria Bastano, per il riferimento).
- Esito: **il metodo non può confermare**: nessun parcheggio entro il raggio trasmette il riempimento. Come previsto dal piano, questa osservazione non entra nei numeri.

## Controlli (script 80 e 79)

Tutti OK:
- 378 fermate importanti
- fermate per categoria nominale 147 / 59 / 172
- somma auto in entrata 95.297 (±1) e domanda 24.459 (±5)
- ogni parcheggio della mappa in una sola direzione
- posti utili direzioni = posti utili parcheggi
- nessun valore negativo
- 29 zone
- somma delle fermate delle zone = 378
- posti nominali delle zone = posti dei parcheggi della mappa (ogni parcheggio conta una volta)
- soglia del 10% riproduce le 378 fermate di S2 (stessi luoghi)
- `mappa_r6.json`: 378 fermate, 29 zone, 349 parcheggi; classi 147 / 60 / 171; nessuna chiave `direzioni`

## File modificati o creati

Modificati:
- `scripts/80_porte_interscambio.py` (riscritto)
- `scripts/79_dati_mappa_r6.py`
- `scripts/mappa_template.html` (testo introduttivo, dati R6, viste, schede, legenda, clic)
- `scripts/04_genera_mappa.py` (messaggio di stampa e commento)
- `scripts/schede_risultati.py` (scheda R6 e percorso del file)

Generati (rigenerati):
- `data/processed/risultato6_v2/porte.json`
- `data/processed/risultato6_v2/mappa_r6.json`
- `docs/RAPPORTO_R6_PORTE.txt`
- `mappa_torino.html`
- `data/schede_risultati.js`
- `data/processed/risultato6_riepilogo_mappa.json`

Non toccati: `MEMORIA_PROGETTO.md`, `data/ref/*`, `data/raw`, lo storico.

## Anomalie e cose da sapere

1. **Mappa non verificata nel browser.** Il browser integrato non apre né `localhost:8766` né il file locale (errore di navigazione). Ho controllato solo la sintassi JavaScript (`node --check`) e il contenuto dei dati. Va aperta a mano (vedi istruzioni nel messaggio).
2. Il tema nel menu si chiama ancora «Parcheggi di interscambio»; le viste e i testi parlano di «parcheggi per lasciare l'auto». Cambiare il nome del tema è una scelta di Leo.
3. La scheda R6 non mostra più le due figure `immagini/r6_torino.png` e `immagini/r6_zoom.png`: non esistono nella cartella `immagini/`.
4. Le direzioni d'ingresso restano solo come riferimento nella scheda (grafico «Riferimento»). In mappa non ci sono più.
5. Le schede R1, R2, R4, R8 e R9 non sono state toccate (le rigenera lo stesso script, con gli stessi contenuti).
6. Restano aperti (come nel piano precedente): 23 luoghi senza zona IMQ (fuori dalle 378) e la lista di altri parcheggi «sempre pieni» da Leo, solo per verifica.
