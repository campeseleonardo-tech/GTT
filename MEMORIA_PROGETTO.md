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

Risultati: **1** servizi (fatto) · **2** metro di notte (chiuso) · **3** più passaggi su una linea · **4** bus in ritardo e
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
· 26 velocità 5T · 27 Risultato 4 · 28-29 Risultato 2 (metro notte) · 30-32 rapporto sostenibilità · 33-38b traffico 5T (flusso per sensore, esclusioni, abbinamento ai corridoi, metodi A+B, verifiche) · 39-48 + `rete_osm.py` metodo C (rete OSM, assegnazione IMQ, validazione) · 49-55 Fase 3-bis e 4 (modello V3, TP per strada, pubblicazione, incrocio). **Prossimo numero libero: 56** (56+ in uso dalla Fase 5). Pulizia 18/10: tolti 07 (doppione di `calcola_simulazione.py`), i `.bat` e `installa_sfondo.py` della vecchia raccolta sul PC, file di prova e `ACCESSIBILITA_COMPLETA/PROVA.bat` (restano in git).

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate |
| Storico leopi | copia sul PC `data/storico_backup.sqlite`; sync da leopi **una volta a settimana** (domenica) con `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat` (anche fetch manuale). Mezzi GTT, ritardi, 5T traffico, parcheggi 5T e ZTL (dal 14/10) |
| 5T traffico | flusso **già in veicoli/ora** (multipli di 12). **112 sensori fisici ma `lcd1` unico solo per 109** (3 codici doppi: 40123, 40189, 13077). **Raccoglitore corretto sul Pi il 17/10 11:24** (`AGGIORNA_RACCOLTA_5T_CODICI.bat`): verificato, 112 sensori e 3/3 codici `~2` con dati; i secondi sensori hanno dati utili dopo ~6 giorni feriali. Il codice `~2` non esiste nei dati storici prima del 17/10. Accuratezza per lettura dal 8/10 21:30 UTC. Esito delle prime analisi: `docs/ESITO_FASE1_TRAFFICO_5T.md`, `docs/ESITO_FASE2_TRAFFICO.md` |
| Ritardi GTT | tabella `trip_update_gtt` (dal 10/10, una lettura al minuto), usata dal Risultato 4. `delay` di corsa mai presente; per ogni fermata `stop_time_update.arr` ha `delay` in secondi (~70%) o l'arrivo previsto `time` (~30%, da confrontare con l'orario GTFS) |
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
| Risultato 4 v1 (27) | [MISURATO] 10-14/10, 596.534 passaggi. **Feriale: 4,2% in ritardo > 5 min · 10,3% coppie a grappolo+buco (linee frequenti) · ritardo mediano −0,6 min.** ~43% passaggi "in anticipo" reale (orari con margine). `docs/RAPPORTO_RISULTATO4.txt`, `data/processed/risultato4_regolarita.json`; verificato da Claude il 14/10. |
| Risultato 2 "metro di notte" (28, 29 v2) | **Chiuso il 16/10.** Buco senza metro 00:50-05:22. Metrica "qualsiasi aumento": **ogni 15': 3.689 sezioni / 773.307 residenti migliorati, attesa media 7,5 min · ogni 30': 3.155 / 652.891, 15 min.** Scheda in `simulazione.html` (`risultato2_riepilogo_mappa.json`). Dettagli e limiti: `docs/PIANO_RISULTATO2.md`, `docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt`. |
| Rapporto sostenibilità GTT 2025 | **Fatto il 17/10 senza servizi esterni.** 980 fatti verificati (27 scartati), riassunto in `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`; dati in `data/processed/rapporto_gtt/`. Script 30-32 e `.bat` pronti per un eventuale giro via DeepSeek (serve `chiave_deepseek.txt`). |
| Schede risultato | **18/10:** `simulazione.html` = galleria di schede (problema, cosa cerchiamo, numero chiave) per R1, R2, R4, R6; clic → finestra con problema, domanda, risposta, grafici solo HTML/CSS (barre, pila, 24 ore), prima/dopo, metodo (chiuso, due livelli), limiti, link mappa, file. Contenuti e numeri in `scripts/schede_risultati.py` → `data/schede_risultati.js` (+ `risultato{1,4,6}_riepilogo_mappa.json`; R2 base dallo script 29). Numeri ricontrollati. Caricamento a mano dei JSON ancora possibile. Dopo un nuovo risultato o un rilancio (es. 27): rieseguire `schede_risultati.py`. Scelte di Leo: due livelli, grafici + link mappa, solo risultati finiti (R8 dopo la Fase 5), breve racconto dell'origine. |

## 5. IN CORSO

- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 v2.
- **Risultato 8, Fase 5 (giro di correzione)**: piano e prompt pronti in `docs/PIANO_TRAFFICO_FASE5.md` (18/10); da lanciare con l'agente. Pacchetti: A assi e tratte (stessa strada anche se cambia nome/comune), B corsie e capacità, C ZTL unificata con orari + aree pedonali, D TP per posizione delle fermate (copertura entro 300 m con ≥4 passaggi/ora; metro/ferrovia entro 600 m), E modello V4 (congestione funzionante, valutato una volta, regola V4-contro-V0), F affidabilità e fasce, G pubblicazione e incrocio, H rilancio. Script da 56.

## 6. PROSSIMI PASSI (in ordine)

1. **Risultato 8 — Traffico veicolare** (priorità; area Torino+cintura; PC libero per i calcoli). Obiettivo di Leo: quanti veicoli passano su ogni strada, poi "vie con molto traffico e poco TP"; analisi prima, mappa dopo.
   Fatte le Fasi 1-4 (vedi FATTO); ora Fase 5 (`docs/PIANO_TRAFFICO_FASE5.md`). **Decisioni di Leo 17-18/10:** risultato finale con numeri assoluti (fascia di errore dagli errori leave-one-out: 50% ≈ ±32%, 90% ≈ ±59%), valori relativi e graduatoria, con la classe di esito accanto; **"poco TP" = accessibilità** (fermate vicine con buon servizio), non i bus sulla strada; solo strade grandi; il centro-centro non è prioritario; la ZTL si unisce in una mappa con gli orari e il traffico si stima per fascia; le corsie contano (traffico per corsia); un corso che cambia nome o comune è un solo asse; **le fermate si cercano per posizione, mai per nome**. La sua conoscenza della città (`docs/CONOSCENZA_TORINO_LEO.md`) è solo controllo di buon senso, mai taratura. Poi, solo se Leo vuole, mappa. Fetch lunedì 19/10 per sabato/domenica (`FETCH_LEOPI_E_VELOCITA_5T.bat` + `TRAFFICO_RILANCIA_SENSORI.bat`), poi ogni domenica. Dopo il 25/10 controllare a mano il cambio ora legale nello script 26.
2. **Risultato 6 v2 — inizio novembre**: riempimento dei parcheggi di interscambio per ora e giorno [MISURATO], poi mappa e `simulazione.html`. Variante (Leo, 14/10: per ora no): escludere anche le zone semicentrali (`--escludi-zone Q001,Q00x`).
3. **Risultato 4 — mappa e presentazione**: colorare le linee per % in ritardo/irregolarità con lo slider dell'ora; rilanciare lo script 27 con più sabati/domeniche.
4. Più avanti: effetto ZTL sulle strade attorno; Risultati 3, 5, 7; rilanciare l'accessibilità/mappa con baseline = media dei dati raccolti su leopi (non solo orario GTFS; Leo 16/10, ritardi da decidere).

**Metrica trasversale (Leo, 16/10, non ancora progettata)**: "quanti veicoli in meno potrebbero girare" a partire da un miglioramento di accessibilità TP, con IMQ per modo come base; da riprendere dopo il Risultato 8.

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
