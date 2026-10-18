# Memoria del progetto GTT

Ultimo aggiornamento: **19/10/2026**. File unico di memoria: leggerlo all'inizio, aggiornarlo alla fine.
Solo lo stato attuale, **conciso ma completo**: i dettagli di un passo stanno nel suo piano in `docs/`
(qui una riga e il rimando). La storia sta in git. Sezioni fisse: 1 Obiettivo · 2 Regole · 3 Cartelle e dati ·
4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI · 7 MANCA · 8 Standard tecnici. Non aggiungerne altre.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove sono le
criticità) + pochi scenari "cosa succede se". Prodotti: la mappa `mappa_torino.html` e i RISULTATI, uno alla
volta (domanda → pochi numeri → grafici → limiti), presentati come schede in `simulazione.html`. Mappa e schede
sono due filoni separati. Interesse in crescita: traffico, parcheggi, logistica, costi. Nel tempo i dati
MISURATI (raccolta su leopi, sempre attiva) devono calibrare quelli simulati.

Risultati: **1** servizi (fatto) · **2** metro di notte (chiuso) · **3** più passaggi su una linea · **4** bus in
ritardo e irregolari (v2) · **5** linea nuova · **6** parcheggi di interscambio (v1) · **7** bici · **8** traffico
(v1) · **9** attesa promessa contro reale (v1). Scenari in `data/scenari/<nome>.json`, avviso standard:
"SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale."

## 2. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente** di ogni fatto importante sui file veri prima di darlo a Leo.
- Git: ramo `prova`; Claude committa solo quando Leo lo chiede.
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

## 3. Cartelle e dati

Radice: `mappa_torino.html`, `simulazione.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: piani, rapporti,
`RIASSUNTO_TRAFFICO.md`; vecchi documenti in `docs/archivio/`. `data/` (non in git): `raw/` (non toccare),
`processed/`, `otp/` (R5), `scenari/`.
Script: 01-20 dati · 21-22 R1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 R6 · 26 velocità 5T · 27 R4 ·
28-29 R2 · 30-32 rapporto sostenibilità · 33-67 + `rete_osm.py` traffico (R8, vedi `docs/RIASSUNTO_TRAFFICO.md`)
· 70 R9 · `schede_risultati.py` schede. **Prossimo numero libero: 80** (68, 69, 71-79 = Risultato 6 v2).

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
| Mappa | **Revisione completa fatta il 18/10** (`docs/PIANO_REVISIONE_MAPPA.md`): 9 temi, niente dati "live", colori leggibili, nomi dei comuni, guida con fonti e date; pubblico = portfolio. Aperto: condizioni d'uso degli sfondi Esri prima di pubblicare. |
| Accessibilità (18) | 24 fasce orarie (15/10); piedi 15 min (80 m/min), TP 45 min. `docs/PIANO_ACCESSIBILITA.md`. |
| Risultato 1 | 10.919 residenti a Torino senza servizi essenziali a 15' (1,3%), peggiore la salute; candidati per nuovi servizi in mappa. |
| Risultato 2 (28-29) | Chiuso il 16/10: metro ogni 15' di notte → 773.307 residenti con accesso migliore (ogni 30': 652.891). `docs/PIANO_RISULTATO2.md`. |
| Risultato 4 v2 (27) | 18/10: feriale 5,3% in ritardo > 5 min, 10,5% grappolo+buco. `docs/PIANO_RISULTATO4.md`. |
| Risultato 6 v1 (24-25) | 611 fermate critiche fuori dal centro (= 462 luoghi, fermate entro 40 m unite), 594 senza interscambio entro 200 m. `docs/PIANO_RISULTATO6.md`. |
| Risultato 6 v2, giro 2 (68-69, 71-77) | 19/10, agente + Claude, numeri ricontrollati; commit 7387285. 5.087 luoghi (fermate entro 40 m), universo dei percentili = 4.425 luoghi della Città metropolitana. Strade corrette (modulo 77: primarie ≥ 4, secondarie ≥ 3, scelta del tratto importante entro 50 m). Parcheggi (3.431 considerati): **0 "di fatto"** (i 19 con firma pendolare stanno in Q001-Q009: ospedali, tribunale, centro), 4 "solo sulla carta" (Stura, Caio Mario, Sofia, Venchi Unica), 758 "potenziali" (zona non centrale + punti a favore: nodo, asse d'ingresso). Scenari: S1 riferimento v1 374 luoghi critici, S2 integrato 378, S3 solo nuovi 385 (coperti da parcheggi di fatto/potenziali a 200 m: 117/140/147). Piano `docs/PIANO_RISULTATO6_V2_GIRO2.md`, esito `docs/ESITO_RISULTATO6_V2_GIRO2.md`. Riempimento: solo 2 feriali validi [DATI SCARSI]. |
| Risultato 8 v1 (33-67) | 18/10, Fase 5 di opencode ricontrollata: 95,3% dei km di strade grandi di Torino serviti dal TP; "molto traffico e poco TP" quasi solo Corso Regina Margherita ovest. Stima C-DEBOLE (errore ±38%). `docs/RIASSUNTO_TRAFFICO.md`. |
| Risultato 9 v1 (70) | 18/10: sulle linee frequenti 0,6-1,5 min in più di attesa rispetto ai 4,8 promessi. `docs/PIANO_RISULTATO9_ATTESA.md`. |
| Rapporto sostenibilità GTT 2025 | 980 fatti verificati, `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`. |
| Schede risultato | `simulazione.html`: R1, R2, R4, R6, R8, R9 da `scripts/schede_risultati.py` → `data/schede_risultati.js`. Rieseguire lo script dopo ogni rilancio di un risultato. Scelte di Leo: due livelli, grafici + link mappa, solo risultati finiti. |

## 5. IN CORSO

- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 v2.
- Piccole pulizie: togliere il file `3)` nella radice (creato per errore da un `.bat`) e le copie
  `scripts/*.bak_18ott` (decide Leo).

## 6. PROSSIMI PASSI (in ordine)

1. **Traffico, routine**: fetch di lunedì 19/10 (sabato/domenica), poi ogni domenica, + `TRAFFICO_RILANCIA_SENSORI.bat`;
   dopo il 25/10 controllare a mano l'ora legale nello script 26. Da fare: controllo a mano di Corso Moncalieri,
   collegare la mappa a `velocita_5t.json` (oggi usa il "tipico" non pulito di `stat.js`), decidere se togliere
   dal bat i passi delle fasi 3-4. Mappa del traffico solo se Leo vuole. (`docs/RIASSUNTO_TRAFFICO.md`, sezione 6.)
2. **Tempi TP contro auto** per coppie di zone IMQ, poi **costi del viaggio** (TP, auto, taxi) e costo di
   potenziare una linea: `docs/PIANO_COSTI.md` (bozza; primo passo: cercare le fonti sul web).
3. **Risultato 6 v2** (dati pronti, resta l'integrazione): scelte di Leo: scenario **S2**; parcheggi centrali = Q001-Q009; 25 m²/posto confermati (mediana 25,4); nodo TP = punto a favore; b2 al posto di b1; universo = Città metropolitana. Eventi (script 78, capienze da web in `data/ref/eventi_luoghi.json`): fatti Olimpico Grande Torino, Inalpi Arena, Oval; **Allianz Stadium rimandato** (in OSM è senza nome, way 119509840) al tema eventi futuro. File unico per mappa e scheda: `data/processed/risultato6_v2/mappa_r6.json` (script 79), ricontrollato da Claude. **Da fare**: integrazione in mappa (nuovo tema) e in `simulazione.html` con grafici + regola colori verde→rosso: `docs/PIANO_INTEGRAZIONE_R6.md`. Dopo il fetch del 25/10 (≥ 5 feriali) rifare 71→72→73→75→76→78→79. Aperto: 23 luoghi senza zona IMQ (fuori universo).
4. **Risultati 4 e 9**: rilanciare con più settimane di dati (27, poi 70, poi `schede_risultati.py`); R4 in mappa
   (linee colorate per ritardo con lo slider dell'ora).
5. Più avanti: effetto ZTL sulle strade attorno; Risultati 3, 5, 7; accessibilità con i tempi reali raccolti;
   logistica come mappa di contesto (`docs/PIANO_COSTI.md`).

Metrica trasversale (Leo, 16/10, da progettare): "quanti veicoli in meno potrebbero girare" da un miglioramento
dell'accessibilità TP, con IMQ per modo come base.
Idea trasversale (Leo, 19/10): una lista di luoghi "speciali" (stadi, palasport, fiere, ospedali, tribunale…) da trattare in modo standard con parametri fissi in tutti i risultati, invece di eccezioni caso per caso: da progettare più avanti.
Idee secondarie: picchi orari per strada/linea; riempimento dei garage del centro come segnale delle auto in
entrata; IMQ in mappa (7 misure); avvisi GTT da aggiornare.

## 7. MANCA (limiti noti)

- Dati: passeggeri/affollamento, bici, costi del servizio, merci, taxi, treni SFM e bus extraurbani di altre
  aziende (fonte possibile: GTFS regionale Piemonte). Occupazione parcheggi solo dal 14/10.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità e scenari su orario programmato: ottimisti per definizione. Di notte nessuna sezione di Torino è
  mai a zero TP (bus notturni): guardare sempre il miglioramento, non la soglia zero.
- Cintura: servizi OSM incompleti, non confrontabili con Torino.
- Traffico: 20 punti di misura, stima debole (±38%), solo residenti 11-84 anni; limiti completi in
  `docs/RIASSUNTO_TRAFFICO.md`. Velocità 5T: "urbano" = nome con "(TO)", include alcune provinciali.

## 8. Standard tecnici

- **Bug di resa**: `node --check` trova solo errori di sintassi; colori, legende e dati non disegnati si
  controllano aprendo la pagina nel browser ed esercitando l'interfaccia.
- **Fermate e strade**: mai abbinare per nome, solo per coordinate. Un corso che cambia nome o comune è un solo
  asse; l'unità del traffico è la tratta d'asse.
- **Mappa**: un campo nuovo in `D.sezioni[i]` va aggiunto anche nella proiezione `sez` di `mappa_template.html`;
  chi cambia l'ora (`#ora`) deve richiamare `aggiornaLegenda()`. Numeri in italiano (virgola decimale).
- **Script 24**: corridoio = stesso nome + tratti collegati o entro ~100-200 m; togliere "(TO)" dai nomi 5T.
- **Script 18**: la firma della run non contiene il percorso del GTFS: tra due lanci con GTFS diversi pulire
  `data/processed/accessibilita_parziale/` (il `.bat` del Risultato 2 lo fa già).
- **Bridge** (chat senza terminale): `device_commit_files` a volte non scrive i file grossi; rileggere dopo.
- **Colori dei gradienti** (Leo, 19/10): in tutta la mappa e nelle schede ogni scala con gradiente va da **verde (bene) a rosso (male/critico)**, mai altre scale; verificare anche i temi esistenti.
