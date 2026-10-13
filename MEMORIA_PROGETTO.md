# Memoria del progetto GTT

Ultimo aggiornamento: 13/10/2026. File unico di memoria: leggerlo all'inizio, aggiornarlo
alla fine, tenerlo CORTO (~15 KB max, solo lo stato attuale — la storia sta in git).

## 1. Obiettivo

Portfolio di Leo su Torino: mappa interattiva (`mappa_torino.html`, pronta, piace, non si rifà)
+ RISULTATI, uno alla volta. Ogni risultato: domanda → 3 numeri → mappa/grafici → limiti
dichiarati. Interesse principale per il futuro: traffico auto, parcheggi, logistica.

## 2. Risultati (in ordine, uno chiuso prima del successivo)

| # | Risultato | Stato |
|---|---|---|
| 1 | Zone con pochi servizi + "aggiungo un servizio qui" | **In corso** — vedi sez. 4 e punti aperti 1-2 |
| 2 | Metro di notte | Da iniziare |
| 3 | Più passaggi su una linea | Da iniziare |
| 4 | Bus lenti e regolarità (MISURATO) | Da iniziare |
| 5 | Linea nuova inventata | Da iniziare |
| 6 | Parcheggi di interscambio (indicatori) | Da iniziare |
| 7 | Bici (potenziale) | Da iniziare |

Ogni risultato: candidati proposti dall'analisi, Leo sceglie cosa simulare. Scenari (2,3,5,"+1
servizio") in `data/scenari/<nome>.json`, separando "cosa succede" da "se è meglio". Avviso
standard sugli scenari: "SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico,
ritardi, capienza, domanda reale. [PROGRAMMATO]/[STIMATO], non [MISURATO]."

## 3. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente**: ogni "fatto" importante va controllato sui file veri (non fidarsi
  del proprio output) prima di darlo a Leo. Già servita 2 volte a trovare bug prima di riportarli.
- Git branch `prova`, un commit per modifica. Script provati su campione prima del giro vero.
- Claude non ha terminale diretto sul PC: le modifiche a script/memoria si scrivono via bridge,
  ma NON diventano un commit git da sole — verificare con Leo come/quando committarle (il
  12/10 un aggiornamento scritto su disco è andato perso, probabile reset git non coordinato).
- `.bat` a doppio clic per Leo (`cd /d "%~dp0.."`); quelli nuovi salvano un log in `logs/` per
  poter diagnosticare un errore da remoto senza farselo ricopiare a mano.
- Python del PATH (3.14) sul PC, non Anaconda. Tag dati sempre: [MISURATO]/[PROGRAMMATO]/
  [STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali nei prodotti. Vulnerabilità sociale
  solo con l'indice dedicato, mai nazionalità. Catalogo dati congelato (nuovo dataset solo se un
  risultato lo richiede).

## 4. Stato attuale

| Componente | Stato |
|---|---|
| Raccolta dati (Pi "leopi", 192.168.8.200) | Attiva dal 3/10, systemd `gtt-raccolta`/`gtt-ritardi` |
| Mappa (`04_genera_mappa.py`) | Pronta, 7 temi |
| Accessibilità (script 18, 8.317 sezioni, R5/r5py) | **Fatta e controllata** (giro completo 12/10) |
| Vulnerabilità (script 19) | Pronta; in mappa da sola e incrociata col Risultato 1 (vuoto di servizio × deboli). Il 13/10: legenda combinata con `PAL_SEZ.vuln_combo` e tag SIMULATO; fix finale incrocio (04 legge `gruppi` da vulnerabilita_mappa.json, `modoSez` segue subVuln, colori combo da `PAL_VULN_COMBO`). |
| Risultato 1, fase A — dove mancano i servizi (script 21) | **Fatta.** 10.919 residenti a Torino senza nessun servizio essenziale a 15' a piedi (1,3% su 848.748); gruppo peggiore: **salute** (9.104 res./138 sez.); ranking: salute>scuole>cibo>fermate>verde |
| Risultato 1, fase B — dove aggiungere un servizio (script 22) | **Fatta per salute, scuole, cibo**: criteri relativi (coprire l'X% dei residenti a zero per gruppo, max candidati per tipologia). Cibo ora incluso, verde e fermate rinviati a un prossimo risultato. |


## 5. Cartelle e script

Radice: `mappa_torino.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: rapporti `RAPPORTO_*.txt`.
`data/` (non in git): `raw/` (non toccare), `processed/` (prodotti), `otp/` (R5/Java), `scenari/`.
Script numerati 01→20 = raccolta e preparazione dati (chiusa). 21 = risultato1 fase A, 22 = fase B.
Prossimo numero libero: 23.

## 6. Dati disponibili (essenziale)

- GTFS GTT (215 linee, 7.045 fermate) + storico mezzi/5T/ritardi da raccolta propria.
- Censimento 2021 per sezione: 8.317 sezioni, 1.557.493 abitanti (Torino 848.748).
- IMQ 2022 (101 zone, spostamenti per ora×modo×scopo×origine-destinazione); zone correggiate (tab_zone_camp) incrociate col Risultato 1 in mappa.
- Catalogo comunale servizi (Torino, 44 dataset) + OSM (cintura, più povero).
- OMI 2025/2 (valori immobiliari per zona). Accessibilità e risultato 1 fase A/B: vedi sez. 4.

## 7. Mancanze e limiti

- Mancano: passeggeri/affollamento, occupazione parcheggi, bici, costi servizio, orari treni SFM.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione.
- Accessibilità/scenari su orario programmato: ottimisti per definizione.
- Cintura: servizi da OSM incompleti (soprattutto commercio); scuole/salute/cibo in cintura NON
  comparabili con Torino (manca il catalogo, non necessariamente il servizio).

## 8. Punti aperti

1. Risultato 1 fase B: valutare se i parametri (celle 400 m, max 5 candidati, guadagno minimo 20)
   vanno tarati diversamente prima di considerarli definitivi.
2. Risultato 1: decidere se fare fase B anche per cibo/fermate/verde, poi fase C (scheda finale:
   3 numeri, mappa, grafici, limiti).
3. Verificare con Leo il flusso dei commit git per script/memoria (vedi sez. 3), per evitare che
   un aggiornamento scritto su disco si perda di nuovo.
4. Ritardi: `12_ritardi_gtt.py` non legge gli `stop_time_update` (ci sono nel 100% delle corse
   attive) — da fare prima del risultato 4.
5. Refuso nel rapporto accessibilità: "720 m" deve essere "1.200 m" (solo testo).
6. Leo deve riguardare a video la mappa dopo la pulizia del 9/10.
7. Risposta MTM attesa.
8. Capire la pausa di ~2h46 nel giro accessibilità dell'11→12/10 (nessun danno, ma da controllare
   prima di un prossimo giro lungo).
