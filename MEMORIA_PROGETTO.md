# Memoria del progetto GTT

Ultimo aggiornamento: **14/10/2026 sera (19:30)**. File unico di memoria: leggerlo all'inizio, aggiornarlo
alla fine, tenerlo corto (~15 KB). Solo lo stato attuale (la storia sta in git).
Sezioni fisse: 1 Obiettivo · 2 Regole · 3 Cartelle e dati · 4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI ·
7 MANCA · 8 Standard tecnici. Non aggiungerne altre.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove
sono le criticità) + pochi scenari "cosa succede se". Prodotti: la mappa interattiva
`mappa_torino.html` (pronta, non si rifà) + i RISULTATI, uno alla volta: domanda → 3 numeri →
mappa/grafici → limiti dichiarati; a risultato finito, presentato anche in `simulazione.html`.
Interesse in crescita: traffico auto, parcheggi, logistica. Nel tempo i dati MISURATI (raccolta su
leopi, che continua sempre) devono calibrare quelli simulati.

Risultati: **1** servizi (fatto) · **2** metro di notte · **3** più passaggi su una linea · **4** bus
in ritardo e irregolari [MISURATO] (v1 fatta) · **5** linea nuova inventata · **6** parcheggi di interscambio (v1 fatta)
· **7** bici. Scenari in `data/scenari/<nome>.json`, avviso standard: "SIMULAZIONE SU ORARIO
PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale."

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

## 3. Cartelle e dati

Radice: `mappa_torino.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: piani `PIANO_*.md`, rapporti
`RAPPORTO_*.txt`. `data/` (non in git): `raw/` (non toccare), `processed/`, `otp/` (R5), `scenari/`.
Script: 01-20 dati · 21-22 Risultato 1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 Risultato 6
· 26 velocità 5T. **Prossimo numero libero: 27.**

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate |
| Storico leopi | copia sul PC `data/storico_backup.sqlite` (aggiornata 14/10). Mezzi GTT, ritardi, 5T traffico (109 sensori, 31 col nome "(TO)"), parcheggi 5T e ZTL dal 14/10 |
| 5T traffico | il flusso è **già in veicoli/ora** (conteggio 5' × 12: tutti i valori sono multipli di 12). Accuratezza per lettura solo dall'8/10 21:30 UTC (`accuratezza_5t`) |
| Ritardi GTT | tabella `trip_update_gtt` (dal 10/10, una lettura al minuto). `delay` di corsa mai presente; per ogni fermata `stop_time_update.arr` ha il ritardo in secondi (`delay`, ~70%) o l'arrivo previsto (`time`, ~30%, da confrontare con l'orario GTFS). Campione: mediana 0, p95 +5 min. Usato dal Risultato 4 |
| Censimento 2021 | 8.317 sezioni, 1.557.493 abitanti (Torino 848.748) |
| IMQ 2022 + zone MTM | spostamenti ora × modo × scopo × O/D, tutto arrivato |
| Servizi | catalogo comunale (Torino) + OSM (cintura, più povero). OMI 2025/2. Avvisi GTT (snapshot 9/10) |
| Feed 5T aperti | solo 3: traffico, parcheggi, ZTL (ferma al 2024). Copie in `data/raw/5t_*_20261014.xml` |
| Mai usati (`data/raw/`) | zona blu, parcheggi disabili, aree pedonali, ciclabili, bike/car sharing, colonnine |

## 4. FATTO

| Cosa | Stato |
|---|---|
| Raccolta leopi | Attiva dal 3/10 (`gtt-raccolta`, `gtt-ritardi`). **Parcheggi 5T + ZTL dal 14/10 15:10** (`aggiorna_raccolta_leopi.bat`; controllo `controlla_raccolta_pk.py`). Spegnimento il 13/10 sera (alimentazione), ripartita. |
| Mappa | Temi trasporto, vulnerabilità, accessibilità (piedi e TP), avvisi GTT, "Dove mancano i servizi". |
| Accessibilità (18) | Completa a 4 fasce (12/10). La versione a 24 ore è in corso (sez. 5). |
| Risultato 1 | Fase A: 10.919 residenti a Torino senza servizi essenziali a 15' (1,3%), peggiore la salute. Fase B: candidati per tutti e 5 i gruppi, in mappa. |
| Risultato 6 v1 (24, 25) | 611 fermate critiche fuori dal centro, **17 coperte** da un interscambio entro 200 m, 594 scoperte. Assi peggiori: metro/corso Francia verso Collegno, via Nizza, Moncalieri. Piano e rapporto in `docs/`. |
| Velocità 5T tipica (26) | `data/processed/velocita_5t.json` [MISURATO]: sensore × tipo di giorno × ora, solo letture affidabili (8-14/10). 2.237 celle valide, **solo feriali** (sabato/domenica: 1 giorno ciascuno). 97/109 sensori. Controllato da Claude: 6 celle ricalcolate in SQL identiche, velocità coerenti con `stat.js`, notte più veloce del mattino in 24/28 sensori urbani. |
| Risultato 4 v1 (27) | [MISURATO] 10-14/10 (3 feriali, 1 sabato, 1 domenica), 596.534 passaggi usati. **Feriale: 4,2% in ritardo > 5 min · 10,3% coppie a grappolo+buco (linee frequenti) · ritardo mediano -0,6 min.** Scarti: 9,3% fuori GTFS, 3,6% letture lontane. `docs/RAPPORTO_RISULTATO4.txt` + `data/processed/risultato4_regolarita.json`. Controllato da Claude il 14/10: 3 passaggi ricalcolati dai dati grezzi identici, fonti `delay`/`time` coerenti (mediane −0,5/−0,3). Il ~43% di passaggi "in anticipo" (< −1 min) è reale: i mezzi guadagnano tempo lungo la corsa (mediana −0,1 alle prime fermate, −0,8 dopo la 30ª) → orari con margine. |

## 5. IN CORSO

- **Accessibilità a 24 fasce orarie** (`ACCESSIBILITA_24ORE.bat`, avviato da Leo il 14/10 alle 15:55).
  Ritmo ~1 h di calcolo per ogni ora del giorno: il 14/10 alle 19:30 era all'ora 3 → fine prevista
  15/10 metà pomeriggio [STIMATO]. Per seguirlo guardare i file in `data/processed/accessibilita_parziale/`
  (il log può restare indietro: PowerShell lo scrive a blocchi). Se si interrompe riparte da solo (60 s, max 20 volte)
  dai lotti salvati. Log: `logs/accessibilita_24ore.log`.
  ⚠ `data/processed/accessibilita.json` oggi è la PROVA a 30 sezioni; il completo a 4 fasce è in
  `accessibilita.json.bak_pre24ore`. **Non rigenerare la mappa finché il calcolo non è finito.**
- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 v2.

## 6. PROSSIMI PASSI (in ordine)

1. **A calcolo accessibilità finito**: controllare il rapporto (8.317 sezioni, 24 ore), rigenerare la
   mappa, cancellare i due `.bak_pre24ore`.
2. **Correzione flusso ×12**: sul Pi è attiva dal 14/10 16:13 (riga corretta a mano in
   `06_dati_live.py`, servizio riavviato; `stat.js` verificato: Corso Orbassano h8 2.492 veic/h).
   Resta la scheda sensore in `mappa_template.html`, che entra con la rigenerazione del punto 1.
3. **Risultato 2 "metro di notte"**: sfrutta subito l'accessibilità a 24 ore.
4. **Velocità 5T in mappa**: `velocita_5t.json` → `D.vel5t` in `04_genera_mappa.py`, selettore
   "Adesso / Tipico all'ora scelta" nel tema Traffico. Piano a parte, dopo il punto 1. Rilanciare lo
   script 26 quando ci sono almeno 2 sabati e 2 domeniche con accuratezza (dal 19/10).
5. **Risultato 6 v2 — inizio novembre**: riempimento dei parcheggi di interscambio per ora e giorno
   [MISURATO], poi mappa e `simulazione.html`. Variante da ricordare (Leo, 14/10: per ora no):
   escludere anche le zone semicentrali (`--escludi-zone Q001,Q00x`).
6. **Risultato 4 — mappa e presentazione** (dopo il punto 1): colorare le linee per % in ritardo /
   irregolarità con lo slider dell'ora, pagina in `simulazione.html`. Rilanciare lo script 27
   quando ci saranno più sabati e domeniche (prima: nuovo `backup_da_leopi.bat`).
7. Più avanti: effetto ZTL sulle strade attorno; Risultati 3, 5, 7.

Idee secondarie: frequenze "promesse vs osservate"; picchi orari per strada/linea; curva di
riempimento dei garage del centro come segnale delle auto in entrata. Scartata: "zone cieche" dei
sensori 5T pesate sui residenti.

Da chiarire con Leo: IMQ in mappa (7 metriche dietro un menu, rimandato); avvisi GTT da
aggiornare periodicamente (oggi uno snapshot del 9/10).

## 7. MANCA (limiti noti)

- Dati: passeggeri/affollamento, bici, costi del servizio, treni SFM e bus extraurbani (fonte
  possibile: GTFS regionale Piemonte). Occupazione parcheggi solo dal 14/10.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità e scenari su orario programmato: ottimisti per definizione.
- Cintura: servizi OSM incompleti, non confrontabili con Torino.
- Risultato 6: 200 m in linea d'aria; pendolari [STIMATO] per zona; l'etichetta comune dei corridoi
  lunghi è quella del punto centrale.
- Velocità 5T: "urbano" = nome con "(TO)", include anche alcune provinciali (es. SP8 di Druento).

## 8. Standard tecnici

- **Bug di resa**: `node --check` trova solo errori di sintassi; per dati non disegnati, colori o
  legenda sbagliati aprire la pagina in un browser ed esercitare l'interfaccia.
- **Bridge** (chat senza terminale): `device_commit_files` a volte non scrive davvero sui file
  grossi; ri-leggere e confrontare dopo ogni scrittura.
- **Mappa**: un campo nuovo in `D.sezioni[i]` va aggiunto anche nella proiezione `sez` di
  `mappa_template.html`; chi cambia l'ora (`#ora`) deve richiamare anche `aggiornaLegenda()`.
- **Script 24**: corridoio = stesso nome + tratti collegati o entro ~100-200 m; togliere il suffisso
  "(TO)" dai nomi dei sensori 5T prima del confronto.
- **Script 18**: con `--salva-tappe` ogni file parziale contiene tutti i lotti del gruppo (campo
  `lotti`); la firma della run (parametri) deve restare identica per riusare i parziali.
