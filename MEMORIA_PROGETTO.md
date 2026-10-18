# Memoria del progetto GTT

Ultimo aggiornamento: **17/10/2026**. File unico di memoria: leggerlo all'inizio, aggiornarlo
alla fine, tenerlo corto (~15 KB). Solo lo stato attuale (la storia sta in git).
Sezioni fisse: 1 Obiettivo · 2 Regole · 3 Cartelle e dati · 4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI ·
7 MANCA · 8 Standard tecnici. Non aggiungerne altre.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove
sono le criticità) + pochi scenari "cosa succede se". Prodotti: la mappa interattiva
`mappa_torino.html` (pronta, non si rifà) + i RISULTATI, uno alla volta: domanda → 3 numeri →
mappa/grafici → limiti dichiarati; a risultato finito, presentato anche in `simulazione.html`.
**Dal 16/10: lavoro sulla mappa e lavoro su `simulazione.html` sono due filoni separati.**
`simulazione.html` avrà un formato "scheda risultato" generico e semplice (prima/dopo, pochi numeri
chiave, un grafico semplice), pensato per ospitare tutti i risultati futuri allo stesso modo — sforzo
grafico minimo per ora, si raffina più avanti.
Interesse in crescita: traffico auto, parcheggi, logistica. Nel tempo i dati MISURATI (raccolta su
leopi, che continua sempre) devono calibrare quelli simulati.

Risultati: **9** attesa promessa contro reale [MISURATO] (v1 fatta) · **1** servizi (fatto) · **2** metro di notte (chiuso) · **3** più passaggi su una linea · **4** bus in ritardo e
irregolari [MISURATO] (v1 fatta) · **5** linea nuova inventata · **6** parcheggi di interscambio (v1 fatta) · **7** bici ·
**8** traffico veicolare [MISURATO+STIMATO] (**priorità dal 16/10**; il resto resta in coda). Scenari in `data/scenari/<nome>.json`,
avviso standard: "SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale."

## 2. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente** di ogni fatto importante sui file veri prima di darlo a Leo.
- Git: ramo `prova`, un commit per modifica; Claude committa solo quando Leo lo chiede.
- Script provati su campione prima del giro vero. Python del PATH (3.14), non Anaconda.
- Accesso: Claude Code ha terminale sul PC e SSH **in sola lettura** verso leopi (`leopi@192.168.8.200`,
  chiave `~/.ssh/id_gtt_leopi`). Scrivere/riavviare sul Pi è bloccato → `.bat` a doppio clic per Leo
  (`cd /d "%~dp0.."`, log in `logs/`). Calcoli lunghi: in una finestra `.bat` propria, non in opencode.
- Tag dati: [MISURATO]/[PROGRAMMATO]/[STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali;
  vulnerabilità solo con l'indice dedicato, mai nazionalità.
- Orari: il PC è in ora italiana (la shell Git Bash mostra un'etichetta di fuso sbagliata).
- **Ogni fase ha il suo `docs/PIANO_*.md`** (storia, decisioni, passi, prompt per l'agente); qui solo il riassunto.
- Agenti esterni (opencode): lavorano sul ramo `prova` senza commit, database in sola lettura, scrivono l'esito in `docs/ESITO_*.md`; Claude ricontrolla i numeri prima di darli a Leo.

## 3. Cartelle e dati

Radice: `mappa_torino.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: piani `PIANO_*.md`, rapporti
`RAPPORTO_*.txt`. `data/` (non in git): `raw/` (non toccare), `processed/`, `otp/` (R5), `scenari/`.
Script: 01-20 dati · 21-22 Risultato 1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 Risultato 6
· 26 velocità 5T · 27 Risultato 4 · 28-29 Risultato 2 (metro notte) · 30-32 rapporto sostenibilità · 33-38b traffico 5T (flusso per sensore, esclusioni, abbinamento ai corridoi, metodi A+B, verifiche) · 39-48 + `rete_osm.py` metodo C (rete OSM, assegnazione IMQ, validazione) · 49-55 Fase 3-bis e 4 (modello V3, TP per strada, pubblicazione, incrocio). **Prossimo numero libero: 56** (56-67 in uso dalla Fase 5; 70 = Risultato 9). Pulizia 18/10: tolti 07 (doppione di `calcola_simulazione.py`), i `.bat` e `installa_sfondo.py` della vecchia raccolta sul PC, file di prova e `ACCESSIBILITA_COMPLETA/PROVA.bat` (restano in git).

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate |
| Storico leopi | copia sul PC `data/storico_backup.sqlite`; sync da leopi **una volta a settimana** (domenica) con `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat` (anche fetch manuale). Mezzi GTT, ritardi, 5T traffico, parcheggi 5T e ZTL (dal 14/10) |
| 5T traffico | flusso **già in veicoli/ora** (multipli di 12). **112 sensori fisici ma `lcd1` unico solo per 109** (3 codici doppi: 40123, 40189, 13077). **Raccoglitore corretto sul Pi il 17/10 11:24** (`AGGIORNA_RACCOLTA_5T_CODICI.bat`): verificato, 112 sensori e 3/3 codici `~2` con dati; i secondi sensori hanno dati utili dopo ~6 giorni feriali. Il codice `~2` non esiste nei dati storici prima del 17/10. Accuratezza per lettura dal 8/10 21:30 UTC. Esito delle prime analisi: `docs/ESITO_FASE1_TRAFFICO_5T.md`, `docs/ESITO_FASE2_TRAFFICO.md` |
| Ritardi GTT | tabella `trip_update_gtt` (dal 10/10, una lettura al minuto), usata dal Risultato 4. `delay` di corsa mai presente; per ogni fermata `stop_time_update.arr` ha `delay` in secondi (~70%) o l'arrivo previsto `time` (~30%, da confrontare con l'orario GTFS). **Copertura (verificata 18/10):** raccolta 05-24 locali (niente notte); solo ~90 linee urbane, 108 linee mai presenti (extraurbane 4 cifre, alcune notturne; 3.540 corse/giorno); sulle linee coperte presenti ~80% delle corse programmate (GPS `mezzi_gtt` 77%, almeno uno dei due 82%): corse mancanti = saltate o non trasmesse, non distinguibili |
| Censimento 2021 | 8.317 sezioni, 1.557.493 abitanti (Torino 848.748) |
| IMQ 2022 + zone MTM | spostamenti ora × modo × scopo × O/D, tutto arrivato |
| Servizi | catalogo comunale (Torino) + OSM (cintura, più povero). OMI 2025/2. Avvisi GTT (snapshot 9/10) |
| Feed 5T aperti | solo 3: traffico, parcheggi, ZTL (ferma al 2024). Copie in `data/raw/5t_*_20261014.xml` |
| Mai usati (`data/raw/`) | zona blu, parcheggi disabili, aree pedonali, ciclabili, bike/car sharing, colonnine |

## 4. FATTO

| Cosa | Stato |
|---|---|
| Raccolta leopi | Attiva dal 3/10 (`gtt-raccolta`, `gtt-ritardi`). **Parcheggi 5T + ZTL dal 14/10 15:10** (`aggiorna_raccolta_leopi.bat`; controllo `controlla_raccolta_pk.py`). Spegnimento il 13/10 sera (alimentazione), ripartita. Sync verso il PC ora settimanale (vedi sezione 3). **18/10:** backup pianificato delle 03:00 fallito (scp interrotto); rifatto da Claude alle 14:18 (`backup_da_leopi.py`, 1,83 GB, verificato, dati al 18/10, 112 sensori). Lo stesso giorno il feed tempo reale GTT (`percorsieorari.gtt.to.it`) non risponde dalle ~09:05 (né dal Pi né dal PC; 5T regolare): buco nei dati mezzi/ritardi, guasto esterno. |
| Mappa | Temi trasporto, vulnerabilità, accessibilità (piedi e TP), avvisi GTT, "Dove mancano i servizi". |
| Accessibilità (18) | Completa a 24 fasce orarie (15/10), mappa rigenerata e verificata a ore 0/12/19/23. Cutoff: piedi 15 min (80 m/min), TP 45 min. Opzioni `--gtfs`/`--out` (per Risultato 2). |
| Risultato 1 | Fase A: 10.919 residenti a Torino senza servizi essenziali a 15' (1,3%), peggiore la salute. Fase B: candidati per tutti e 5 i gruppi, in mappa. |
| Risultato 6 v1 (24, 25) | 611 fermate critiche fuori dal centro, **17 coperte** da un interscambio entro 200 m, 594 scoperte. Assi peggiori: metro/corso Francia verso Collegno, via Nizza, Moncalieri. Piano e rapporto in `docs/`. |
| Traffico 5T, Fasi 1-2 (26, 33-38b) | **17/10.** `velocita_5t.json` rigenerato (9-16/10, giorni parziali ai bordi esclusi; 2.252 celle feriali, sabato/domenica 0 finché non c'è il fetch del 19/10). 17 sensori esclusi (11 morti, 5 bloccati, 1 pochi dati) → 92 usabili; misure principali = ora di punta e totale diurno 6-21 (ora 1 locale = dato mancante, notte inaffidabile). Metodo A: errore mediano 37% (n=16); metodo B ≈ A. Solo 20 unità-sensore su 15 corridoi (su 10.743). Dettagli e decisioni: `docs/PIANO_TRAFFICO_5T.md`, `docs/PIANO_TRAFFICO_FASE2.md`. |
| Traffico 5T, Fase 3 metodo C (39-48) | **17/10.** Domanda IMQ auto (4,15 M viaggi/giorno) assegnata ai percorsi più veloci su rete OSM (81.966 nodi, 105.890 tratti), tarata sui sensori (k = 1,72). **Esito secondo i criteri fissati: C-DEBOLE** — errore mediano 31,9% (IC90 23,7-40,2%), p90 59%, Spearman 0,60, n=20 unità-sensore (il metodo A dava 36,9% su n=16: differenza non distinguibile). 10.122 corridoi su 10.743 con stima, fiducia alta solo 19. Limiti: nessuna congestione, destinazioni pesate sulla popolazione, "porte" di bordo con valori assurdi (fino a 250.000 veic/giorno), soglie alto/medio/basso calcolate su tutti i corridoi (da rifare dentro Torino). Rapporto `docs/RAPPORTO_TRAFFICO_C.txt`, dettagli `docs/ESITO_FASE3_TRAFFICO.md`, output `data/processed/traffico_stimato_finale.json`. Rilancio dopo ogni fetch: `scripts\TRAFFICO_RILANCIA_SENSORI.bat`. |
| Traffico 5T, Fasi 3-bis e 4 (49-55) | **17/10.** Modello V3 (attrattori+congestione+porte) non adottato: rho 0,573 < 0,602 di V0 → si tiene **V0 (C-DEBOLE)**; la congestione non agiva (Castello→Collegno 13,1→13,3 min). Offerta bus/tram dal GTFS (mercoledì 14/10): 13.158 corse, 93,1% agganciate. Pubblicati numeri con fascia ±32% (50%) / ±59% (90%) e graduatoria; universo Torino 872 corridoi / 1.300 km. Incrocio: 23 corridoi "molto traffico, poco TP". **Verdetto di Claude (18/10): la lista non è affidabile** — TP misurato con aggancio forma→strada (incoerente: Cairoli 2 linee, 0 passaggi), corridoi per nome, nessuna corsia né ZTL, centro sottostimato, raccordi sopravvalutati. Confronto con la conoscenza di Leo (25 strade): Spearman ~0,48. Dettagli: `docs/ESITO_FASE4_TRAFFICO.md`. |
| Traffico 5T, Fase 5 (56-67, opencode) | **18/10, ricontrollata da Claude.** Assi (stessa strada anche se cambia nome/comune), corsie, ZTL unificata (3 zone + 143 aree pedonali), **TP per posizione delle fermate** (5.055 fermate, 13.158 corse; Cairoli ora servito: l'errore della Fase 4 era la media su tutto il corridoio). Modello V4 non migliora V0 (rho 0,571 < 0,605) → **V0, C-DEBOLE: err. mediano 38,4% (IC90 25,5-49,8%), rho 0,605, n=20** — ricalcolati da Claude, identici (k 0,953). Il riferimento cambia dalla Fase 3 (31,9%) per la nuova convenzione: sensore a un verso ×2 e tratto OSM a senso unico ×2 (giusto per i corsi a due carreggiate, doppio sulle vie a senso unico vere: al massimo 47 tratte / 24 km dell'universo, non separabili con certezza). Universo Torino 540 tratte / 343 km (il file `tratte_traffico.json` dice 539/342,8 e conteggi delle regole un po' diversi dall'ESITO: giro precedente, differenze piccole), fasce ±38% / ±64%. **Incrocio: 95,3% dei km serviti dal TP; "molto traffico e poco TP" = 5 tratte, in pratica solo Corso Regina Margherita ovest (penetrazione, nessuna fermata ≥4/h entro 300 m: ricontrollato) + 1 tratto di Corso Moncalieri (da verificare a mano)**; la vecchia lista di 23 era un artefatto. Lunghezze degli assi nell'ESITO = somma di carreggiate e controviali (es. Francia 41,8 km), non la lunghezza della strada. File: `data/processed/risultato8_traffico_tp_v2.json`, `traffico_d/`, `docs/ESITO_FASE5_TRAFFICO.md`. |
| Risultato 4 v2 (27) | **18/10**, [MISURATO] 10-18/10 (5 feriali, 2 sabati, 2 domeniche; giorni parziali 10, 12, 13, 18/10 contati con le ore che hanno dati — scelta di Leo), 1.280.961 passaggi. **Feriale: 5,3% in ritardo > 5 min · 10,5% grappolo+buco · ritardo mediano −0,4 min · 39,9% in anticipo.** Sale rispetto alla v1 (4,2%) perché gio 15 e ven 16 sono andati peggio (ricontrollo indipendente giorno per giorno: stessa tendenza). La v1 aveva giorni a metà (il 12/10 solo pomeriggio). v1 conservata in `risultato4_regolarita_v1.json` / `RAPPORTO_RISULTATO4_v1.txt`. Limite nuovo: misura solo le corse presenti nel feed (vedi sezione 3, Ritardi GTT). |
| Risultato 2 "metro di notte" (28, 29 v2) | **Chiuso il 16/10.** Buco senza metro 00:50-05:22. Metrica "qualsiasi aumento": **ogni 15': 3.689 sezioni / 773.307 residenti migliorati, attesa media 7,5 min · ogni 30': 3.155 / 652.891, 15 min.** Scheda in `simulazione.html` (`risultato2_riepilogo_mappa.json`). Dettagli e limiti: `docs/PIANO_RISULTATO2.md`, `docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt`. |
| Risultato 9 v1 (70) | **18/10**, [MISURATO] 10-18/10, linee urbane frequenti (≤ 12 min), ore con raccolta attiva. **Feriale: attesa promessa 4,8 min, reale 5,4-6,2 → 0,6-1,5 min in più (+13% stima bassa)**; sabato +0,8-1,4; domenica troppo pochi dati. Peggiori: linea 68 (+1,3-3,0), 3, 56, 46, 62; fermate della 18 (Caio Mario, Lingotto) e della 62. Forbice: bassa = solo tratti senza corse mancanti, alta = corse assenti da feed e GPS = saltate. Controlli: GPS linee 4 e 15 (343 passaggi, scarto tipico 0,45 min, 70% entro 1 min); una chiave rifatta da zero coincide (2,555 / 3,668 min). `docs/RAPPORTO_RISULTATO9_ATTESA.txt`, `data/processed/risultato9_attesa.json`, scheda in `simulazione.html`. Script 70 riusa il 27 senza modificarlo. |
| Rapporto sostenibilità GTT 2025 | **Fatto il 17/10 senza servizi esterni.** 980 fatti verificati (27 scartati), riassunto in `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`; dati in `data/processed/rapporto_gtt/`. Script 30-32 e `.bat` pronti per un eventuale giro via DeepSeek (serve `chiave_deepseek.txt`). |
| Schede risultato | **18/10:** `simulazione.html` = galleria di schede (problema, cosa cerchiamo, numero chiave) per R1, R2, R4, R6, R8 (18/10: numero chiave 95,3% dei km di strade grandi serviti dal TP; classifica solo strade con sensore sull'asse, perché senza il modello mette in cima strade poco credibili come Dogliotti e d'Azeglio), R9; clic → finestra con problema, domanda, risposta, grafici solo HTML/CSS (barre, pila, 24 ore), prima/dopo, metodo (chiuso, due livelli), limiti, link mappa, file. Contenuti e numeri in `scripts/schede_risultati.py` → `data/schede_risultati.js` (+ `risultato{1,4,6}_riepilogo_mappa.json`; R2 base dallo script 29). Numeri ricontrollati. Caricamento a mano dei JSON ancora possibile. Dopo un nuovo risultato o un rilancio (es. 27): rieseguire `schede_risultati.py`. Scelte di Leo: due livelli, grafici + link mappa, solo risultati finiti (R8 dopo la Fase 5), breve racconto dell'origine. |

## 5. IN CORSO

- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 v2.
- **Risultato 8, dopo la Fase 5** (finita e ricontrollata il 18/10, vedi FATTO): restano un solo riassunto dei ~35 documenti traffico (vecchi in `docs/archivio/`), accorciare questa memoria (~15 KB), togliere il file `3)` creato per errore dal `.bat`, commit dei file della Fase 5 (non ancora in git). L'"anomalia 4" dell'ESITO (file della mappa modificati in parallelo) era la sessione di revisione della mappa: normale.

## 6. PROSSIMI PASSI (in ordine)

1. **Risultato 8 — Traffico veicolare** (priorità; area Torino+cintura; PC libero per i calcoli). Obiettivo di Leo: quanti veicoli passano su ogni strada, poi "vie con molto traffico e poco TP"; analisi prima, mappa dopo.
   Fatte le Fasi 1-5 (vedi FATTO). **Decisioni di Leo 17-18/10:** risultato finale con numeri assoluti (fascia di errore dagli errori leave-one-out: 50% ≈ ±38%, 90% ≈ ±64% dopo la Fase 5), valori relativi e graduatoria, con la classe di esito accanto; **"poco TP" = accessibilità** (fermate vicine con buon servizio), non i bus sulla strada; solo strade grandi; il centro-centro non è prioritario; la ZTL si unisce in una mappa con gli orari e il traffico si stima per fascia; le corsie contano (traffico per corsia); un corso che cambia nome o comune è un solo asse; **le fermate si cercano per posizione, mai per nome**. La sua conoscenza della città (`docs/CONOSCENZA_TORINO_LEO.md`) è solo controllo di buon senso, mai taratura. Poi, solo se Leo vuole, mappa. Fetch lunedì 19/10 per sabato/domenica (`FETCH_LEOPI_E_VELOCITA_5T.bat` + `TRAFFICO_RILANCIA_SENSORI.bat`), poi ogni domenica. Dopo il 25/10 controllare a mano il cambio ora legale nello script 26.
1b. **Dopo la Fase 5: tempi TP contro auto** per coppie di zone IMQ (base per "veicoli in meno"). Risultati 4 e 9 da rilanciare quando ci sono più settimane di dati (`27`, poi `70`, poi `schede_risultati.py`).
2. **Risultato 6 v2 — inizio novembre**: riempimento dei parcheggi di interscambio per ora e giorno [MISURATO], poi mappa e `simulazione.html`. Variante (Leo, 14/10: per ora no): escludere anche le zone semicentrali (`--escludi-zone Q001,Q00x`).
3. **Risultato 4 — mappa e presentazione**: colorare le linee per % in ritardo/irregolarità con lo slider dell'ora; rilanciare lo script 27 con più sabati/domeniche.
4. Più avanti: effetto ZTL sulle strade attorno; Risultati 3, 5, 7; rilanciare l'accessibilità/mappa con baseline = media dei dati raccolti su leopi (non solo orario GTFS; Leo 16/10, ritardi da decidere).

**Metrica trasversale (Leo, 16/10, non ancora progettata)**: "quanti veicoli in meno potrebbero girare" a partire da un miglioramento di accessibilità TP, con IMQ per modo come base; da riprendere dopo il Risultato 8.

**Revisione della mappa (18/10): fatta** → `docs/PIANO_REVISIONE_MAPPA.md` (problemi per gravità + ordine di lavoro). **Correzioni tutte fatte il 18/10** (mappa rigenerata, 23,4 MB, 9 temi, niente più dati "live": `data/live.js` non si legge più; dettagli nel piano). Scelte di Leo: pubblico = portfolio; cintura con la stessa scala di Torino + nota breve su OSM solo dove serve; "Bus e traffico misurati" con giornata registrata al posto del tempo reale; Catalogo tenuto (inventario, in fondo); Risultati fuori dalla mappa per ora. Aperto: condizioni d'uso sfondi Esri prima di pubblicare. Prova nel browser: `.claude/launch.json` → `pagine-gtt` (porta 8765). Storico: il mezzo 2897U ha `ts_feed` ~3 anni avanti (2.100 righe).

**Idee nuove di Leo (discusse 18/10, piacciono; si riprendono dopo aver finito le correzioni della mappa).** Ordine proposto da Claude: (1) **costi del viaggio** TP/auto/taxi per coppia di zone IMQ, insieme ai "tempi TP contro auto" (punto 1b): tariffe GTT, costo auto al km (tabelle ACI) + parcheggio (zona blu già nel catalogo), tariffe taxi del Comune; due versioni per l'auto ("costo che senti" e "costo vero"). (2) **costo di potenziare una linea** come colonna del Risultato 3: km in più × costo per km (manca: bilancio GTT o contratto con l'Agenzia Mobilità Piemontese; il rapporto di sostenibilità ha solo i km, 55-57 M/anno) contro beneficio da accessibilità/attesa (R9). (3) **Taxi solo come tariffa** dentro (1): a Torino non ci sono dati aperti sulle corse. (4) **Logistica dopo, come mappa di contesto** (interporto SITO Orbassano, magazzini/aree industriali OSM, negozi da rifornire): niente dati merci (5T non distingue i veicoli, IMQ = solo residenti) → [DATI SCARSI], salvo trovare dati nei piani della mobilità (PUMS) o conteggi ZTL merci. Prossimo passo quando si riprende: cercare sul web le fonti (solo lettura), poi `docs/PIANO_COSTI.md`.

Idee secondarie: frequenze "promesse vs osservate"; picchi orari per strada/linea; curva di riempimento dei garage del centro come segnale delle auto in entrata. Da chiarire: IMQ in mappa (7 metriche dietro un menu); avvisi GTT da aggiornare (oggi snapshot del 9/10).

## 7. MANCA (limiti noti)

- Dati: passeggeri/affollamento, bici, costi del servizio, treni SFM e bus extraurbani (fonte
  possibile: GTFS regionale Piemonte). Occupazione parcheggi solo dal 14/10.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità e scenari su orario programmato: ottimisti per definizione. **Risultato 2 in particolare
  ha mostrato che a Torino nessuna sezione è mai a copertura TP zero di notte (bus notturni esistenti),
  quindi un confronto "isolata vs servita" non è mai informativo qui — va sempre guardato il delta, non
  la soglia zero.**
- Cintura: servizi OSM incompleti, non confrontabili con Torino.
- Risultato 6: 200 m in linea d'aria; pendolari [STIMATO] per zona; l'etichetta comune dei corridoi
  lunghi è quella del punto centrale.
- Velocità 5T: "urbano" = nome con "(TO)", include anche alcune provinciali (es. SP8 di Druento).
- Traffico: pochi sensori (20 unità utili, su poche strade), a Torino un solo verso; notte inaffidabile; IMQ = solo residenti 11-84 anni (niente merci, turisti, pendolari da fuori); stima modello debole (C-DEBOLE), probabilmente vicina al limite misurabile (due sensori sulla stessa strada differiscono ~36%); i 20 sensori stanno tutti su strade da ~12.000 a ~81.000 veicoli/giorno, quindi sotto ~9.000 il modello non è validato.

## 8. Standard tecnici

- **Bug di resa**: `node --check` trova solo errori di sintassi; per dati non disegnati, colori o
  legenda sbagliati aprire la pagina in un browser ed esercitare l'interfaccia.
- **Bridge** (chat senza terminale): `device_commit_files` a volte non scrive davvero sui file
  grossi; ri-leggere e confrontare dopo ogni scrittura.
- **Fermate e strade**: mai abbinare per nome (il nome di una fermata è spesso un incrocio); solo per coordinate. Un corso è un asse che può cambiare nome o comune: l'unità di analisi del traffico è la tratta d'asse, non il nome.
- **Mappa**: un campo nuovo in `D.sezioni[i]` va aggiunto anche nella proiezione `sez` di
  `mappa_template.html`; chi cambia l'ora (`#ora`) deve richiamare anche `aggiornaLegenda()`.
- **Script 24**: corridoio = stesso nome + tratti collegati o entro ~100-200 m; togliere il suffisso
  "(TO)" dai nomi dei sensori 5T prima del confronto.
- **Script 18**: con `--salva-tappe` ogni file parziale contiene tutti i lotti del gruppo (campo
  `lotti`); la firma della run (parametri) deve restare identica per riusare i parziali.
  La firma **non** contiene il percorso del GTFS: due run con GTFS diversi ma stessi parametri
  si scambiano i parziali se non si pulisce `data/processed/accessibilita_parziale/` tra un lancio
  e l'altro (bug reale trovato e aggirato da Claude il 16/10 nel `.bat` del Risultato 2, pulendo quella
  cartella prima di ogni lancio — lo script 18 in sé non è stato toccato).
