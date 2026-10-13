# Memoria del progetto GTT

Ultimo aggiornamento: 13/10/2026 sera. File unico di memoria: leggerlo
all'inizio, aggiornarlo alla fine, tenerlo CORTO (~15 KB max, solo lo stato attuale — la
storia sta in git).

## 1. Obiettivo

Portfolio di Leo su Torino: mappa interattiva (`mappa_torino.html`, pronta, piace, non si rifà)
+ RISULTATI, uno alla volta. Ogni risultato: domanda → 3 numeri → mappa/grafici → limiti
dichiarati. Interesse principale per il futuro: traffico auto, parcheggi, logistica.

## 2. Risultati (in ordine, uno chiuso prima del successivo)

| # | Risultato | Stato |
|---|---|---|
| 1 | Zone con pochi servizi + "aggiungo un servizio qui" | **In corso** — vedi sez. 4 |
| 2 | Dove l'auto è inevitabile (auto privata) | Da iniziare |
| 3 | Più passaggi su una linea | Da iniziare |
| 4 | Bus lenti e regolarità (MISURATO) | Da iniziare |
| 5 | Linea nuova inventata | Da iniziare |
| 6 | Parcheggi di interscambio (indicatori) | Da iniziare |
| 7 | Bici (potenziale) | Da iniziare |
| 8 | Parcheggi di interscambio (indicatori) — dove metto l'auto prima di prendere il tram? | Da iniziare |
| 9 | Dove l'auto è inevitabile — dove il TP non basta | Da iniziare |

Ogni risultato: candidati proposti dall'analisi, Leo sceglie cosa simulare. Scenari (2,3,5,"+1
servizio") in `data/scenari/<nome>.json`, separando "cosa succede" da "se è meglio". Avviso
standard sugli scenari: "SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico,
ritardi, capienza, domanda reale. [PROGRAMMATO]/[STIMATO], non [MISURATO]."

## 3. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente**: ogni "fatto" importante va controllato sui file veri (non fidarsi
  del proprio output) prima di darlo a Leo.
- Git branch `prova`, un commit per modifica. Script provati su campione prima del giro vero.
- Claude non ha terminale diretto sul PC: le modifiche a script/memoria si scrivono via bridge,
  ma NON diventano un commit git da sole. **Leo decide da solo quando e come committare**
  (messaggi proposti pronti in sez. 10): non è un punto aperto da chiedere.
- `.bat` a doppio clic per Leo (`cd /d "%~dp0.."`); quelli nuovi salvano un log in `logs/` per
  poter diagnosticare un errore da remoto senza farselo ricopiare a mano.
- Python del PATH (3.14) sul PC, non Anaconda. Tag dati sempre: [MISURATO]/[PROGRAMMATO]/
  [STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali nei prodotti. Vulnerabilità sociale
  solo con l'indice dedicato, mai nazionalità. Catalogo dati congelato (nuovo dataset solo se un
  risultato lo richiede).

## 4. Stato attuale

| Componente | Stato |
|---|---|
| Raccolta dati (Pi "leopi", 192.168.8.200) | Attiva dal 3/10, systemd `gtt-raccolta`/`gtt-ritardi`. **13/10 sera**: il Pi si è spento per sottoalimentazione (hardware, non software) — buco di alcune ore nei dati di oggi; riconnesso e raccolta ripartita, confermato (`replay_*.js` aggiornati in tempo reale). Da tenere d'occhio se si ripete. |
| Mappa (`04_genera_mappa.py`) | Pronta, 9 temi |
| Accessibilità (script 18, 8.317 sezioni, R5/r5py) | Fatta e controllata (giro completo 12/10) |
| Vulnerabilità (script 19) | Pronta; in mappa da sola e incrociata col Risultato 1. 2 bug di resa trovati e corretti il 13/10 (non ancora committati, vedi sez. 10). |
| Risultato 1, fase A — dove mancano i servizi (script 21) | **Fatta.** 10.919 residenti a Torino senza nessun servizio essenziale a 15' a piedi (1,3% su 848.748); gruppo peggiore: **salute** (9.104 res./138 sez.); ranking: salute>scuole>cibo>fermate>verde |
| Risultato 1, fase B — dove aggiungere un servizio (script 22) | **Fatta solo per salute e scuole** (celle 400 m, max 5 candidati, guadagno minimo 20). **Parametri confermati da Leo (13/10 sera): vanno bene per partire, non serve tararli ora** — si raffinano eventualmente più avanti. Cibo, verde e fermate restano da fare, volutamente rimandati. |

## 5. Cartelle e script

Radice: `mappa_torino.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: rapporti `RAPPORTO_*.txt`.
`data/` (non in git): `raw/` (non toccare), `processed/` (prodotti), `otp/` (R5/Java), `scenari/`.
Script numerati 01→20 = raccolta e preparazione dati (chiusa). 21 = risultato1 fase A, 22 = fase B.
Prossimo numero libero: 23.

## 6. Dati disponibili (essenziale)

- GTFS GTT (215 linee, 7.045 fermate) + storico mezzi/5T/ritardi da raccolta propria.
- Censimento 2021 per sezione: 8.317 sezioni, 1.557.493 abitanti (Torino 848.748).
- IMQ 2022 (101 zone, spostamenti per ora×modo×scopo×origine-destinazione); zone correggiate (tab_zone_camp) incrociate col Risultato 1 in mappa. **Zone di campionamento ricevute da MTM** (chiuso 13/10): `data/IMQ2022_opendata_web`, `data/IMQ2013-22_zone_camp_TO`, `data/IMQ2022_zone_camp_noTO` — tutto quanto serviva da MTM è arrivato.
- Catalogo comunale servizi (Torino, 44 dataset) + OSM (cintura, più povero).
- OMI 2025/2 (valori immobiliari per zona). Accessibilità e risultato 1 fase A/B: vedi sez. 4.
- Avvisi/disservizi GTT (snapshot, vedi sez. 8) e accessibilità anche via trasporto pubblico (vedi sez. 10).

## 7. Mancanze e limiti

- Mancano: passeggeri/affollamento, occupazione parcheggi, bici, costi servizio, orari treni SFM.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità/scenari su orario programmato: ottimisti per definizione.
- Cintura: servizi da OSM incompleti (soprattutto commercio); scuole/salute/cibo in cintura NON
  comparabili con Torino (manca il catalogo, non necessariamente il servizio).

## 8. Punti aperti — prossimi passi

1. **Da chiarire con Leo — `12_ritardi_gtt.py` e `stop_time_update`.** Controllato il 13/10
   sera su richiesta: il codice LEGGE già correttamente `stop_time_update` quando il feed lo
   manda (lo conta in `con_stu`/`n_stu`, non è un bug di lettura). Ma il docstring dello script
   stesso dice il contrario di quanto annotato qui in precedenza: "verificato sui campioni, il
   feed trip_update di GTT NON pubblica delay né stop_time_update". La vecchia nota diceva
   invece che `stop_time_update` è presente nel 100% delle corse attive. Non è stato possibile
   controllare i dati reali da qui (vivono solo in `storico.sqlite` su leopi, nessun terminale
   diretto). **Da chiedere a Leo**: la sua osservazione "100% delle corse" veniva da un
   controllo più recente/diverso da quello nel docstring? Se sì va aggiornato lo
   script/docstring; se no, il punto si chiude da solo (limite del feed GTT, non un bug nostro).
2. IMQ 2022: rimandato (deciso da Leo il 13/10 sera). Non è un bug di resa (colore già a
   gradiente per quintili) ma un problema di leggibilità: 7 metriche dietro un menu, nessuna
   vista d'insieme. Da riprendere in un round futuro.
3. Avvisi GTT in mappa (vedi sez. 10): lo snapshot usato oggi (`avvisi_20261009.json`) invecchia.
   Se Leo vuole gli avvisi sempre aggiornati, va programmato un giro periodico che rigenera
   quel file (non ancora fatto) — `04_genera_mappa.py` da solo prende sempre il file
   `avvisi_*.json` più recente per nome, ma qualcuno deve produrne uno nuovo di tanto in tanto.

## 9. Standard di lavoro consolidati

- **Verifica dei bug di resa (non di sintassi)**: `node --check` sui blocchi `<script>`
  estratti trova solo errori di sintassi. Per i bug di resa (dato non disegnato, colore
  sbagliato, pannello/legenda con contenuto vecchio) l'unico modo affidabile è aprire davvero
  la pagina in un browser headless (Playwright, Chromium a `/opt/pw-browsers/chromium-1194/
  chrome-linux/chrome` in questa sessione) ed esercitare l'interfaccia (cambio tema, click,
  hover, slider orario) leggendo poi il DOM/scheda/legenda risultante.
- **Scrittura file via bridge**: `device_commit_files` fallisce silenziosamente circa 1 volta
  su 2 su file grossi (riporta "written" ma il contenuto sul PC resta quello vecchio). Prassi
  fissa: dopo ogni scrittura, ri-`device_stage_files` lo stesso file e confrontarlo con la
  copia locale; se non combacia, riscrivere con `force:true` e riverificare. Ha sempre
  funzionato al secondo tentativo.
- **Un campo nuovo in `D.sezioni[i]` va aggiunto in DUE punti**: nei dati grezzi E nella
  proiezione leggera `sez` (`return {p:z.p, c:z.c, ...}` in `mappa_template.html`). Dimenticare
  il secondo punto non dà errori, semplicemente il dato non arriva mai al disegno.
- **Un elemento UI che cambia l'ora (`#ora`) deve richiamare anche `aggiornaLegenda()`**, non
  solo `aggiornaOra()`/il ridisegno della mappa — altrimenti la legenda mostra un dato non più
  aggiornato mentre il colore delle sezioni invece sì (bug trovato e corretto il 13/10 sera
  sulla fascia oraria TP: un pezzo di UI collegato solo a metà).

## 10. Round 13/10 — check generale + 5 blocchi di modifiche (fatto, approvato da Leo a video, da committare quando vuole)

Leo ha chiesto un check critico di tutta la mappa (fatto: zero errori console su tutti i temi
via Playwright) + un giro di miglioramenti. Tutti i 5 blocchi sotto sono stati scritti,
verificati (sintassi + render reale via Playwright, zero errori) e **approvati da Leo a video
il 13/10 sera** ("le modifiche vanno bene"). Restano da committare, quando e come decide Leo
(vedi sez. 3).

**Blocco 0 — Regia unica pannello/tooltip per tema.** Risolti 3 bug: tooltip che mostrava dati
di trasporto non pertinenti su Vulnerabilità/Accessibilità; pannello con campi fissi (Indice di
criticità, passaggi GTT) sempre presenti anche su temi non di trasporto; pannello che restava
visibile dopo un cambio tema senza nuovo click. Nuova funzione `famigliaModo()` classifica il
modo attivo (trasporto/demo/vuln/acc/fb) e decide quali campi di contesto mostrare;
`applicaTema()` ora chiude pannello e tooltip ad ogni cambio tema.

**Blocco 1 — Pulizia codice morto `vuln_serv`/`vuln_verde`.** Rimossi completamente.

**Blocco 2 — Accessibilità anche via trasporto pubblico.** Nuovo selettore "Modalità" (a piedi
15'/mezzi pubblici 45') nel tema Accessibilità, campo `tp` di `accessibilita.json` (4 fasce
orarie: 08/14/23/02). **Regola confermata da Leo il 13/10 sera**: la fascia va usata solo se
l'ora selezionata in mappa è esatta o entro 1 ora da una delle 4; altrimenti il dato è "non
disponibile" (non viene più scelta la fascia più vicina a prescindere dalla distanza). Corretto
in corsa anche un bug collegato: muovendo lo slider dell'ora la legenda non si aggiornava (vedi
sez. 9).

**Blocco 3 — Avvisi/disservizi GTT.** Nuovo campo `D.avvisi` (filtrato: solo avvisi ancora
attivi, 116/134 nello snapshot usato), mostrato come badge "⚠" nel pannello di linee e fermate
coinvolte. Link ai dettagli GTT quando disponibile. Vedi punto aperto 3 per l'aggiornamento nel
tempo.

**Blocco 4 — "Dove mancano i servizi" (fase A completa + candidati fase B).** Nuovo tema:
colora le sezioni per zero/pochissimo/ok rispetto al gruppo scelto (dato completo per tutti e 5
i gruppi, da `risultato1_vuoti.json`), e sopra disegna i pallini cliccabili dei candidati fase B
dove già calcolati (solo salute e scuole).

**File toccati in tutti i blocchi**: `scripts/mappa_template.html` (sorgente), `mappa_torino.html`
(già generato, stesso stato), `scripts/04_genera_mappa.py` (legge anche `avvisi_*.json` più
recente, `risultato1_vuoti.json`, `risultato1_candidati.json`, embedda `tp` oltre a `piedi`).

**Messaggi di commit proposti** (Leo decide se/quando usarli, un commit per blocco, nell'ordine):

1. `fix: pannello e tooltip mostrano solo i dati del tema attivo, chiusura automatica al cambio tema`
2. `chore: rimosso codice morto vuln_serv/vuln_verde (tolti dal menu in un turno precedente)`
3. `feat: accessibilità ai servizi anche via trasporto pubblico (45 min, 4 fasce orarie, match esatto o entro 1h)`
4. `feat: avvisi e disservizi GTT in corso, come badge su linee e fermate coinvolte`
5. `feat: nuovo tema "Dove mancano i servizi" (fase A completa) con candidati fase B dove disponibili`
6. `fix: 2 bug di resa sui temi vulnerabilità (crash su modoSez, soglie mancanti per vuln*)`
7. `feat: tema "Vulnerabilità × servizi" sostituito da "Accessibilità ai servizi"`
