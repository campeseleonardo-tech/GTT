# Memoria del progetto GTT

Ultimo aggiornamento: **20/10/2026, sera** (pulizia completa). File unico di memoria: leggerlo all'inizio, aggiornarlo alla fine.
Solo lo stato attuale, **conciso ma completo**: i dettagli di un passo stanno nel suo piano in `docs/`
(qui una riga e il rimando). La storia sta in git. Sezioni fisse: 1 Obiettivo · 2 Regole · 3 Cartelle e dati ·
4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI · 7 MANCA · 8 Standard tecnici. Non aggiungerne altre.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove sono le
criticità) + pochi scenari "cosa succede se". Prodotti: la mappa `mappa_torino.html` e i RISULTATI, uno alla
volta (domanda → pochi numeri → grafici → limiti), presentati come schede in `simulazione.html`. Mappa e schede
sono due filoni separati. Interesse in crescita: traffico, parcheggi, costi. Nel tempo i dati
MISURATI (raccolta su leopi, sempre attiva) devono calibrare quelli simulati.

Risultati: **1** servizi (fatto) · **2** metro di notte (chiuso) · **3** più passaggi su una linea · **4** bus in
ritardo e irregolari (v2) · **5** linea nuova · **6** parcheggi per lasciare l'auto (corretto) · ~~**7** bici~~ (tolto il 20/10) · **8** traffico
(v1) · **9** attesa promessa contro reale (v1). Di 3 e 5 se ne farà **uno solo** (Leo, 20/10). Scenari in `data/scenari/<nome>.json`, avviso standard:
"SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale."

## 2. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente** di ogni fatto importante sui file veri prima di darlo a Leo.
- Git: ramo `prova`; Claude committa solo quando Leo lo chiede. Nelle sessioni cloud Claude lavora su un ramo
  `claude/...` che Leo unisce in `prova`. Il repository GitHub è **pubblico** dal 20/10 (sera): niente segreti né dati personali in git.
- Script provati su campione prima del giro vero. Python del PATH (3.14), non Anaconda.
- Accesso: terminale sul PC e SSH **in sola lettura** verso leopi (`leopi@192.168.8.200`, chiave
  `~/.ssh/id_gtt_leopi`). Scrivere/riavviare sul Pi → `.bat` a doppio clic per Leo (`cd /d "%~dp0.."`, log in
  `logs/`). Calcoli lunghi in una finestra `.bat` propria.
- Tag dati: [MISURATO]/[PROGRAMMATO]/[STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali;
  vulnerabilità solo con l'indice dedicato, mai nazionalità.
- Orari: il PC è in ora italiana (Git Bash mostra un'etichetta di fuso sbagliata).
- **Ogni fase ha il suo `docs/PIANO_*.md`** (storia, decisioni, passi, prompt); la memoria ha il riassunto.
- Agenti esterni (opencode): ramo `prova` senza commit, database in sola lettura, esito in `docs/ESITO_*.md`;
  Claude ricontrolla i numeri prima di darli a Leo.
- Prova delle pagine nel browser integrato: `.claude/launch.json` → `pagine-gtt` (porta 8765).
- Regole fisse di Leo per il R6: le sue osservazioni non entrano nei dati (solo controllo a posteriori,
  `data/ref/parcheggi_osservazioni.json`); in pagina niente versioni, scenari, eventi, classi dei parcheggi.

## 3. Cartelle e dati

Radice: `mappa_torino.html`, `simulazione.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: piani, rapporti,
`RIASSUNTO_TRAFFICO.md`, `PIANO_PULIZIA.md` (analisi e ordine dei passi del 20/10); vecchi documenti in `docs/archivio/`
(correzioni del 20/10 in `docs/archivio/correzioni_20ott/`). `data/` (non in git): `raw/` (non toccare),
`processed/`, `otp/` (R5), `scenari/`.
Script: 01-20 dati · 21-22 R1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 R6 · 26 velocità 5T · 27 R4 ·
28-29 R2 · 30-32 rapporto sostenibilità · 33-67 + `rete_osm.py` traffico (R8, vedi `docs/RIASSUNTO_TRAFFICO.md`)
· 70 R9 · R6: 68-69 inventari, 71-73 riempimento/nodi/segnali, 77 modulo delle strade, 79 dati mappa, 80 solo funzioni usate da 84-85, 81 auto che passano, 82 parcheggi adatti, 83 fermate importanti, 84 risultato, 85 verifiche · 86 cartella `pubblica/` e README · `comuni.py` funzioni comuni · `controlla_leopi.py` · `schede_risultati.py` schede. Catena R6: `scripts/RISULTATO6_RIFAI.bat`. Superati in `scripts/archivio/` (elenco in `LEGGIMI.txt`). **Prossimo numero libero: 87**.

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate (versione 20261002, valida fino al 31/01/2027) |
| Storico leopi | copia `data/storico_backup.sqlite`, aggiornata **la domenica** con `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat`. Mezzi GTT, ritardi (dal 10/10), 5T traffico, parcheggi 5T e ZTL (dal 14/10). Il mezzo 2897U ha l'orologio ~3 anni avanti (lo script 04 scarta le letture lontane oltre 1 h) |
| Ritardi GTT | solo ~90 linee urbane, 05-24, ~80% delle corse programmate presenti: dettagli in `docs/PIANO_RISULTATO4.md` |
| 5T traffico | già veicoli/ora; 112 sensori (3 codici doppi, corretti sul Pi il 17/10); dettagli in `docs/RIASSUNTO_TRAFFICO.md` |
| Censimento 2021 | 8.317 sezioni, 1.557.493 abitanti (Torino 848.748), 69 comuni |
| IMQ 2022 + zone MTM | spostamenti ora × modo × scopo × O/D (101 zone della Città metropolitana) |
| Servizi | catalogo comunale (Torino) + OSM (cintura, più povero). OMI 2025/2. Avvisi GTT (fotografia del 9/10) |
| Feed 5T aperti | solo 3: traffico, parcheggi, ZTL (ferma al 2024). Copie in `data/raw/5t_*_20261014.xml` |
| Fonti e indirizzi | `docs/FONTI_DATI.md` |

## 4. FATTO

| Cosa | Stato |
|---|---|
| Raccolta leopi | Attiva dal 3/10; parcheggi 5T + ZTL dal 14/10. 18/10: backup notturno fallito, rifatto da Claude (verificato); feed tempo reale GTT fermo dalle ~09:05 (guasto esterno, buco nei dati di quel giorno). |
| Mappa | **Revisione completa fatta il 18/10** (`docs/archivio/PIANO_REVISIONE_MAPPA.md`): 9 temi, niente dati "live", colori leggibili, nomi dei comuni, guida con fonti e date; pubblico = portfolio. Aperto: condizioni d'uso degli sfondi Esri prima di pubblicare. |
| Accessibilità (18) | 24 fasce orarie (15/10); piedi 15 min (80 m/min), TP 45 min. `docs/PIANO_ACCESSIBILITA.md`. |
| Risultato 1 | 10.919 residenti a Torino senza servizi essenziali a 15' (1,3%), peggiore la salute; candidati per nuovi servizi in mappa. |
| Risultato 2 (28-29) | Chiuso il 16/10: metro ogni 15' di notte → **334.085 residenti con almeno +25% di servizi** (ogni 30': 153.062; numero in grande da 20/10); con qualsiasi miglioramento 773.307 (652.891). `docs/PIANO_RISULTATO2.md`. |
| Risultato 4 v2 (27) | 18/10: feriale 5,3% in ritardo > 5 min, 10,5% grappolo+buco. `docs/PIANO_RISULTATO4.md`. |
| Risultato 6 (24-25, 68-73, 77, 79-85) | **Corretto il 20/10** (esito ricontrollato da Claude): 391 fermate importanti fuori dal centro, **253 senza posti bastanti** entro 400 m a piedi (99 senza nessun parcheggio adatto); 76 aree (20 critiche, 46 «Pochi dati»); 20 punti prioritari (1 solo sotto 2,5 km dal centro, prima 7); auto in entrata 87.162, chi già lascia l'auto 5,8% (64 interviste); torinesi inclusi (34%). Validazione: solo Stura informativo. Mappa 13,6 MB. Punti deboli da decidere (stesse auto in più punti, Gioanetti a 1,4 km): `docs/PIANO_RISULTATO6.md`. Catena `scripts\RISULTATO6_RIFAI.bat` (~4 min). |
| Risultato 8 v1 (33-67) | 18/10, Fase 5 di opencode ricontrollata: 95,3% dei km di strade grandi di Torino serviti dal TP; "molto traffico e poco TP" quasi solo Corso Regina Margherita ovest. Stima C-DEBOLE (errore ±38%). `docs/RIASSUNTO_TRAFFICO.md`. |
| Risultato 9 v1 (70) | 18/10: sulle linee frequenti 0,6-1,5 min in più di attesa rispetto ai 4,8 promessi. `docs/PIANO_RISULTATO9_ATTESA.md`. |
| Rapporto sostenibilità GTT 2025 | 980 fatti verificati, `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`. |
| Schede risultato | `simulazione.html`: R1, R2, R4, R6, R8, R9 da `scripts/schede_risultati.py` → `data/schede_risultati.js`, con riassunto in inglese. Rieseguire lo script dopo ogni rilancio di un risultato. Scelte di Leo: due livelli, grafici + link mappa, solo risultati finiti. |
| Pulizia (20/10) | 21 file superati in `scripts/archivio/` (`LEGGIMI.txt`), documenti finiti in `docs/archivio/`, un solo `scripts\AGGIORNA_RACCOLTA_LEOPI.bat`, commenti `[agente]` tolti, niente più «carica file» in `simulazione.html`. `docs/PIANO_PULIZIA.md`. |
| Controllo leopi | `scripts\CONTROLLA_LEOPI.bat` (20/10; tolto il falso allarme sulla ZTL, che si salva solo se cambia). |

## 5. IN CORSO

- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 (più giorni feriali di riempimento).
- **Risultato 6, punti per asse** (Leo, 20/10 sera): un punto per asse d'ingresso, almeno 3 km dal centro, posti che
  mancano arrotondati: eseguito sul PC il 20/10 (19 punti, verifiche 0 non superate, ricontrollato da Claude).
  Poi regola «almeno 50 posti mancanti»: giro del 20/10 12:11, **16 punti**, verifiche 0 non superate. Chiuso. Risultato 2: numero in grande = 334.085 (severo), in `schede_risultati.py`.
- Sul PC (Leo): cancellare il file `3)` e `scripts/*.bak_18ott`; salvare in git `README.md` dopo aver rilanciato lo 86.

## 6. PROSSIMI PASSI (in ordine: dettagli in `docs/PIANO_PULIZIA.md` sezione 4)

1. (fatto il 20/10: ramo di Claude unito in `prova`, Risultato 6 rifatto, README in git.)
2. `schtasks` con `scripts\CONTROLLA_LEOPI.bat` ogni mattina (comando in `docs/archivio/correzioni_20ott/ESITO_CORREZIONI_GENERALI.md`, 3.5).
3. Ora legale del 25/10: controllo a mano dello script 26 dopo il fetch del 1/11 (+ `TRAFFICO_RILANCIA_SENSORI.bat`).
4. Risultato 6: confronto delle auto in entrata con i sensori 5T del mattino.
5. Pubblicare su GitHub Pages (proposta: ramo `gh-pages` con solo `pubblica/`), cartella leggera (oggi 90 MB), sfondi Esri.
6. 2-3 risultati di punta, ognuno con «come sappiamo che è vero».
7. Rilanci: R6 dopo ≥ 5 feriali di parcheggi (inizio novembre); R4 e R9 con un mese (metà novembre); R4 in mappa.
   Screenshot di Leo per la scheda R6.
8. Tempi TP contro auto per coppie di zone IMQ, poi costi del viaggio (`docs/PIANO_COSTI.md`).
9. Più avanti: treni SFM, uno scenario fra R3 e R5, luoghi «speciali», effetto ZTL, Corso Moncalieri, `velocita_5t.json` in mappa.

Metrica trasversale (Leo, 16/10, da progettare): "quanti veicoli in meno potrebbero girare" da un miglioramento
dell'accessibilità TP, con IMQ per modo come base.
Idea trasversale (Leo, 19/10): una lista di luoghi "speciali" (stadi, palasport, fiere, ospedali, tribunale…) da trattare in modo standard con parametri fissi in tutti i risultati, invece di eccezioni caso per caso: da progettare più avanti.
Idee secondarie: picchi orari per strada/linea; riempimento dei garage del centro come segnale delle auto in
entrata; IMQ in mappa (7 misure); avvisi GTT da aggiornare. Congelate (Leo, 20/10): bici, dati da telefonia,
logistica, eventi (stadi, palazzetti).

## 7. MANCA (limiti noti)

- Dati: passeggeri/affollamento, bici, costi del servizio, merci, taxi, treni SFM e bus extraurbani di altre
  aziende (fonte possibile: GTFS regionale Piemonte). Occupazione parcheggi solo dal 14/10.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità e scenari su orario programmato: ottimisti per definizione. Di notte nessuna sezione di Torino è
  mai a zero TP (bus notturni): guardare sempre il miglioramento, non la soglia zero.
- Cintura: servizi OSM incompleti, non confrontabili con Torino.
- Traffico: 20 punti di misura, stima debole (±38%), solo residenti 11-84 anni; limiti completi in
  `docs/RIASSUNTO_TRAFFICO.md`. Velocità 5T: "urbano" = nome con "(TO)", include alcune provinciali.

- Risultato 6: i «posti che mancano» sono ordini di grandezza (quota da 64 interviste × traffico ±38%); il modello del
  traffico senza code preferisce le strade veloci; riempimento misurato solo per pochi garage 5T.
- Script 80 e 77 sembrano superati ma servono (funzioni per 84-85, modulo per 72-73). `supervisore.py` e `06_dati_live.py`
  girano sul Pi. I passi delle fasi 3-4 nel `.bat` del traffico hanno uscite lette dalla Fase 5: lasciati.
- Codice copiato (distanze, radice del progetto, ora legale) in molti script: si passa a `comuni.py` quando si tocca uno script.
- `mappa_torino.html` (13,6 MB) è ancora salvata in git a ogni giro: si decide con la pubblicazione.

## 8. Standard tecnici

- **Bug di resa**: `node --check` trova solo errori di sintassi (il giro R6 ha lasciato una funzione non definita, trovata solo a runtime); colori, legende e dati non disegnati si
  controllano aprendo la pagina nel browser ed esercitando l'interfaccia. Prova automatica: `python scripts\prova_pagine_r6.py` (errori a runtime su mappa e scheda).
- **Fermate e strade**: mai abbinare per nome, solo per coordinate. Un corso che cambia nome o comune è un solo
  asse; l'unità del traffico è la tratta d'asse.
- **Mappa**: un campo nuovo in `D.sezioni[i]` va aggiunto anche nella proiezione `sez` di `mappa_template.html`;
  chi cambia l'ora (`#ora`) deve richiamare `aggiornaLegenda()`. Numeri in italiano (virgola decimale).
- **Script 24**: corridoio = stesso nome + tratti collegati o entro ~100-200 m; togliere "(TO)" dai nomi 5T.
- **Script 18**: la firma della run non contiene il percorso del GTFS: tra due lanci con GTFS diversi pulire
  `data/processed/accessibilita_parziale/` (il `.bat` del Risultato 2 lo fa già).
- **Bridge** (chat senza terminale): `device_commit_files` a volte non scrive i file grossi; rileggere dopo.
- **Controlli negli script** (20/10): si fermano solo per errori di struttura (file mancante, somme che non tornano,
  valori negativi); un numero diverso da quello di oggi è un AVVISO. Funzioni comuni (distanze, ora legale, percentili,
  zona centrale Q001-Q009) in `scripts/comuni.py`. Ogni risultato deve avere una verifica su fatti noti.
- **Colori** (Leo, 19/10), uguali in mappa e schede: gradiente «bene/male» = **verde→rosso**; quantità neutre (abitanti, spostamenti, pendolari, prezzi) = **blu→arancione smorzati**; categorie = un colore per gruppo. Le legende scrivono sempre i numeri (daltonismo). Piano: `docs/archivio/r6/PIANO_INTEGRAZIONE_R6.md`; elenco delle sostituzioni: `docs/archivio/RAPPORTO_COLORI.txt`.
