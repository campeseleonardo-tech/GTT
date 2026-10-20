# Memoria del progetto GTT

Ultimo aggiornamento: **20/10/2026, sera** (Risultato 1 v2 chiuso: fasi A, B, B bis ricontrollate). File unico di memoria: leggerlo all'inizio, aggiornarlo alla fine.
Solo lo stato attuale, **conciso ma completo**: i dettagli di un passo stanno nel suo piano in `docs/`
(qui una riga e il rimando). La storia sta in git. Sezioni fisse: 1 Obiettivo · 2 Regole · 3 Cartelle e dati ·
4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI · 7 MANCA · 8 Standard tecnici. Non aggiungerne altre.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove sono le
criticità) + pochi scenari "cosa succede se". Prodotti: la mappa `mappa_torino.html` e i RISULTATI, uno alla
volta (domanda → pochi numeri → grafici → limiti), presentati come schede in `simulazione.html`. Mappa e schede
sono due filoni separati. Interesse in crescita: traffico, parcheggi, costi. Nel tempo i dati
MISURATI (raccolta su leopi, sempre attiva) devono calibrare quelli simulati.

Risultati: **1** servizi · **2** metro di notte (**in pausa**, scheda nascosta) · **3** più passaggi su una linea · **4**
puntualità e attese (ritardi + ex **9** attesa reale, da unire in una scheda) · **5** linea nuova · **6** parcheggi per
lasciare l'auto · ~~**7** bici~~ (tolto) · **8** traffico. Di 3 e 5 se ne farà **uno solo** (Leo, 20/10).
**Un piano per risultato** (Leo, 20/10): `docs/PIANO_RISULTATO1/2/4/6/8.md`, in testa stato, commenti, decisioni e
lavori in ordine; sotto la storia. Scenari in `data/scenari/<nome>.json`, avviso standard:
"SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale."

## 2. Regole di lavoro

- Passo passo con Leo: decisioni importanti chieste prima; piccole scelte con default dichiarati.
- **Verifica indipendente** di ogni fatto importante sui file veri prima di darlo a Leo.
- Git: ramo `prova`; **commit e push sempre automatici** alla fine del lavoro (Leo, 20/10; regole in `AGENTS.md`). Nelle sessioni cloud Claude lavora su un ramo
  `claude/...` che Leo unisce in `prova`. Il repository GitHub è **pubblico** dal 20/10 (sera): niente segreti né dati personali in git.
- Script provati su campione prima del giro vero. Python del PATH (3.14), non Anaconda.
- Accesso: terminale sul PC e SSH **in sola lettura** verso leopi (`leopi@192.168.8.200`, chiave
  `~/.ssh/id_gtt_leopi`). Scrivere/riavviare sul Pi → `.bat` a doppio clic per Leo (`cd /d "%~dp0.."`, log in
  `logs/`). Calcoli lunghi in una finestra `.bat` propria.
- Tag dati: [MISURATO]/[PROGRAMMATO]/[STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali;
  vulnerabilità solo con l'indice dedicato, mai nazionalità.
- Orari: il PC è in ora italiana (Git Bash mostra un'etichetta di fuso sbagliata).
- **Ogni fase ha il suo `docs/PIANO_*.md`** (storia, decisioni, passi, prompt); la memoria ha il riassunto.
- Agenti esterni (modello minore, sul PC o nel cloud): fanno commit e push da soli (`AGENTS.md`), database in sola lettura, esito in `docs/ESITO_*.md`;
  Claude ricontrolla i numeri prima di darli a Leo.
- Prova delle pagine nel browser integrato: `.claude/launch.json` → `pagine-gtt` (porta 8765).
- Regole fisse di Leo per il R6: le sue osservazioni non entrano nei dati (solo controllo a posteriori,
  `data/ref/parcheggi_osservazioni.json`); in pagina niente versioni, scenari, eventi, classi dei parcheggi.

## 3. Cartelle e dati

Radice: `mappa_torino.html`, `simulazione.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: piani, rapporti,
`PIANO_RISULTATO8.md` (traffico), `PIANO_PULIZIA.md` (analisi e ordine dei passi del 20/10); vecchi documenti in `docs/archivio/`
(correzioni del 20/10 in `docs/archivio/correzioni_20ott/`). `data/` (non in git): `raw/` (non toccare),
`processed/`, `otp/` (R5), `scenari/`.
Script: 01-20 dati · 21-22 R1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 R6 · 26 velocità 5T · 27 R4 ·
28-29 R2 · 30-32 rapporto sostenibilità · 33-67 + `rete_osm.py` traffico (R8, vedi `docs/PIANO_RISULTATO8.md`)
· 70 R9 · R6: 68-69 inventari, 71-73 riempimento/nodi/segnali, 77 modulo delle strade, 79 dati mappa, 80 solo funzioni usate da 84-85, 81 auto che passano, 82 parcheggi adatti, 83 fermate importanti, 84 risultato, 85 verifiche · 86 cartella `pubblica/` e README · `comuni.py` funzioni comuni · `controlla_leopi.py` · `schede_risultati.py` schede. Catena R6: `scripts/RISULTATO6_RIFAI.bat`. Superati in `scripts/archivio/` (elenco in `LEGGIMI.txt`). **Prossimo numero libero: 87** (88 e 89 fatti; riservato: 87 popolarità).

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate (versione 20261002, valida fino al 31/01/2027) |
| Storico leopi | copia `data/storico_backup.sqlite`: dal 20/10 **ogni giorno alle 07:30** con `scripts\RACCOLTA_GIORNALIERA.bat` (attività di Windows «GTT raccolta giornaliera», installata con `INSTALLA_RACCOLTA_GIORNALIERA.bat`; copia anche `stat.js` e `replay_*.js` e controlla la raccolta). Sul Pi **un solo servizio** `gtt-raccolta` (supervisore → 03 + 12 ritardi; `gtt-ritardi` disattivato con `PI_UN_SOLO_PROCESSO.bat`). Le analisi (26, traffico, R6) si lanciano a mano. Mezzi GTT, ritardi (dal 10/10), 5T traffico, parcheggi 5T e ZTL (dal 14/10). Il mezzo 2897U ha l'orologio ~3 anni avanti (lo script 04 scarta le letture lontane oltre 1 h) |
| Ritardi GTT | solo ~90 linee urbane, 05-24, ~80% delle corse programmate presenti: dettagli in `docs/PIANO_RISULTATO4.md` |
| 5T traffico | già veicoli/ora; 112 sensori (3 codici doppi, corretti sul Pi il 17/10); dettagli in `docs/PIANO_RISULTATO8.md` |
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
| Risultato 1 (21-22) | **v2 del 20/10** (fasi A, B, B bis, ricontrollate da Claude anche in Chromium): **362 torinesi in zone abitate con 3+ servizi mancanti** (5 sezioni in collina: Lavazza, Mainero, Sant'Anna ×2, Maddalena); 6.768 in zone poco abitate (sotto 1.000 ab/km², grigio); 389 «da verificare» (2 sezioni di via Chieti: fermata a 75-179 m che il calcolo a piedi non raggiunge; da aggiungere a `SEZIONI_FUORI_RETE` dello script 18 al prossimo calcolo completo); cintura con a piedi o mezzo pubblico 45' alle 8. Mappa: tema «Dove mancano i servizi» a gradini 0-5, cerchi sulle zone critiche, viste per servizio con i candidati (5 gruppi: scuole 5, salute 5, cibo 3, fermate 1, verde 0). `docs/PIANO_RISULTATO1.md`. |
| Risultato 2 (28-29) | Chiuso il 16/10: metro ogni 15' di notte → **334.085 residenti con almeno +25% di servizi** (ogni 30': 153.062; numero in grande da 20/10); con qualsiasi miglioramento 773.307 (652.891). **In pausa** (Leo, 20/10): non risponde alla domanda «tornare a casa la sera»; scheda da nascondere; ripresa con il «popolo della notte» (IMQ 00-05). `docs/PIANO_RISULTATO2.md`. |
| Risultato 4 «Puntualità e attese» (27 + 70) | Giro 1 del 20/10: una scheda con l'ex R9; classifiche solo linee ordinarie (≥ 2.000 passaggi; in testa la 17). Dati 10-20/10 (7 feriali): feriale **5,2%** in ritardo > 5 min, 10,5% grappolo+buco; attesa promessa 4,8 min, reale 5,4-6,3 (+0,6-1,6). Idee: link linea→mappa, ritardo/km, tram contro bus. `docs/PIANO_RISULTATO4.md`. |
| Risultato 6 (24-25, 68-73, 77, 79-85) | **Corretto il 20/10** (esito ricontrollato da Claude): 391 fermate importanti fuori dal centro, **253 senza posti bastanti** entro 400 m a piedi (99 senza nessun parcheggio adatto); 15 punti prioritari (giro del 20/10 15:06; uno per asse, ≥ 3 km dal centro, ≥ 50 posti mancanti); in mappa anche 80 parcheggi del centro (viola), 2 viste; auto in entrata 87.162, chi già lascia l'auto 5,8% (64 interviste); torinesi inclusi (34%). Validazione: solo Stura informativo. Mappa 13,6 MB. Da fare (Leo, 20/10): pannello del parcheggio rotto (CSS), parcheggi del centro in mappa, via la vista «aree», fermate importanti con regola fissa, «popolarità» delle zone e linee utili (script 87). `docs/PIANO_RISULTATO6.md`. Catena `scripts\RISULTATO6_RIFAI.bat` (~4 min). |
| Risultato 8 v1 (33-67) | 18/10, Fase 5 di opencode ricontrollata: 95,3% dei km di strade grandi di Torino serviti dal TP; "molto traffico e poco TP" quasi solo Corso Regina Margherita ovest. Stima C-DEBOLE (errore ±38%). Da fare: errore % per sensore in scheda, frase corretta (il 95,3% vale solo per le strade grandi). `docs/PIANO_RISULTATO8.md`. |
| Rapporto sostenibilità GTT 2025 | 980 fatti verificati, `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`. |
| Schede risultato | `simulazione.html`: R1, R2, R4, R6, R8, R9 da `scripts/schede_risultati.py` → `data/schede_risultati.js`, con riassunto in inglese. Rieseguire lo script dopo ogni rilancio di un risultato. Scelte di Leo: due livelli, grafici + link mappa, solo risultati finiti. |
| Pulizia (20/10) | 21 file superati in `scripts/archivio/` (`LEGGIMI.txt`), documenti finiti in `docs/archivio/`, un solo `scripts\AGGIORNA_RACCOLTA_LEOPI.bat`, commenti `[agente]` tolti, niente più «carica file» in `simulazione.html`. `docs/PIANO_PULIZIA.md`. |
| Controllo leopi | `scripts\CONTROLLA_LEOPI.bat` (20/10; tolto il falso allarme sulla ZTL, che si salva solo se cambia); dentro la raccolta giornaliera. |
| Ora legale | Controllata da Claude il 20/10: tutte le conversioni UTC → ora italiana (04, 06, 12, 26, 27, 71, `comuni.py`) coincidono con il fuso ufficiale su 35.040 istanti del 2026-2027, cambio del 25/10 compreso. Niente controllo a mano. |

## 5. IN CORSO

- **Raccolta parcheggi** su leopi: serve fino a inizio novembre per il Risultato 6 (più giorni feriali di riempimento).
- **Risultato 6, punti per asse** (Leo, 20/10 sera): un punto per asse d'ingresso, almeno 3 km dal centro, posti che
  mancano arrotondati: eseguito sul PC il 20/10 (19 punti, verifiche 0 non superate, ricontrollato da Claude).
  Poi regola «almeno 50 posti mancanti»: giro del 20/10 12:11, **16 punti**, verifiche 0 non superate. Chiuso. Risultato 2: numero in grande = 334.085 (severo), in `schede_risultati.py`.
- **Analisi di Leo del 20/10** sui risultati: discussa, decisioni nei piani per risultato. Nessun risultato ancora modificato.
- Sul PC (Leo): cancellare il file `3)` e `scripts/*.bak_18ott`.

## 6. PROSSIMI PASSI (in ordine; i lavori di ogni risultato sono nel suo piano, con i prompt)

1. (fatto il 20/10 alle 14:45: raccolta automatica attiva, log controllati da Claude: un solo servizio sul Pi con 03
   e 12, copia giornaliera OK.) Da tenere d'occhio: lo storico pesa **2,1 GB** e cresce di circa 190 MB al giorno
   (soprattutto i ritardi): la copia intera richiede ~10 minuti oggi; verso i 6-8 GB servirà una copia solo dei
   dati nuovi o una pulizia (il supervisore avvisa oltre 10 GB).
2. (fatto il 20/10, ricontrollato: Giro 1, `docs/PIANO_GIRO1_RITOCCHI.md`.) Trovato nel ricontrollo: a pari punteggio
   l'ordine delle fermate importanti cambiava a ogni giro (insieme non ordinato nello script 83) e con lui il nome e
   la strada di un gruppo dell'84 (Chieri: 16 → 15 punti). Corretto con uno spareggio fisso: si vede al prossimo
   `RISULTATO6_RIFAI.bat`.
3. (fatto il 20/10, ricontrollato: Risultato 1 v2 fase A, 751 abitati con 3+ mancanti.) **Risultato 1 fase B** (mappa
   0-5, grigio sotto 1.000 ab/km², quali servizi mancano nel pannello, elenco delle sezioni critiche per il lavoro 7):
   e B bis fatte sul PC il 20/10 e ricontrollate da Claude (Chromium: 0 errori, titolo 362 in pagina, cerchi sulle 5
   zone critiche). Lavoro 7 fatto con Leo: le 5 zone critiche sono tutte in collina, **confermate**. **R1 v2 chiuso.** Al prossimo calcolo completo dell'accessibilità (18): le 2 sezioni da
   verificare in `SEZIONI_FUORI_RETE`. Corretto da Claude nel template «piu'» → «più» (si vede al prossimo 04).
4. **Risultato 6**: (prompt A fatto il 20/10 sera, ricontrollato: spareggio OK, 15 punti identici in due giri; confronto
   con i sensori 5T **debole**, ρ 0,52 su 23 luoghi, il modello sottostima gli ingressi da nord-ovest; riga nei limiti
   della scheda da aggiungere dopo B e C.) (Prompt B fatto, ricontrollato: **Leo sceglie N 10 corse/ora, M 1.000 auto**,
   274 fermate importanti al posto di 391; si applica nel giro di modifica dopo il C.) Poi B
   (proposta fermate importanti, script 89, Leo sceglie N e M), poi C (popolarità delle zone senza i ritorni a casa,
   script 87): `docs/PIANO_RISULTATO6.md` (prompt rivisti il 20/10 sera).
4bis. **Risultato 4, lavori piccoli sui dati di oggi** (non serve aspettare novembre): tram contro bus (3), oltre 10
   minuti contro il 2,3% di GTT (9), link linea → mappa (4), ritardo per km (5). Prompt da scrivere; dopo la fase B
   del R1 (toccano lo stesso template).
5. Pubblicare su GitHub Pages (ramo `gh-pages` con solo `pubblica/`), cartella leggera (oggi 90 MB), sfondi Esri.
6. Rilanci con più dati: R6 dopo ≥ 5 feriali di parcheggi (inizio novembre); R4 (con R9) con un mese (metà
   novembre); poi R4 in mappa. Screenshot di Leo per la scheda R6.
7. Tempi TP contro auto per coppie di zone IMQ, poi costi del viaggio (`docs/PIANO_COSTI.md`).
8. Più avanti: R2 ripreso (popolo della notte), treni SFM, uno scenario fra R3 e R5, luoghi «speciali», effetto ZTL,
   Corso Moncalieri, `velocita_5t.json` in mappa, tram contro bus (efficienza e costi).

Come si lavora con il modello minore: un giro per volta (mai due insieme: toccano gli stessi file); lui lavora sul
ramo `prova` (sul PC) o sul suo ramo (cloud), scrive `docs/ESITO_*.md` e fa commit e push da solo; se era nel cloud, Leo
unisce il ramo e lancia i passi sui dati; Claude ricontrolla prima del giro dopo. Merge sempre con `--no-edit`.

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
  `docs/PIANO_RISULTATO8.md`. Velocità 5T: "urbano" = nome con "(TO)", include alcune provinciali.

- Risultato 6: i «posti che mancano» sono ordini di grandezza (quota da 64 interviste × traffico ±38%); il modello del
  traffico senza code preferisce le strade veloci; riempimento misurato solo per pochi garage 5T.
- Risultato 6, controllo con i sensori 5T (script 88, 20/10): ordine delle auto in entrata del mattino, modello contro
  sensori entro 25 km da Torino: rho 0,83 per sensore, **0,60 per luogo (0,596: debole)**, 0,52 senza i sensori fuori rete.
  Il modello sottostima le provinciali (SP1, SP8, SP2) e sopravvaluta C.so Giulio Cesare, Unione Sovietica, Allamano,
  Sebastopoli. Dettagli: docs/ESITO_R6_SENSORI.md.
- Risultato 6, fermate importanti con regola fissa (script 89, solo proposta, 20/10): la regola «(metro/stazione/capolinea o
  N corse/ora) e M auto» dà da 25 a 347 fermate sulla griglia N 10-30, M 500-3000; Leo deve scegliere N e M. Più la regola è
  severa, meno punti prioritari di oggi restano coperti (da 12 su 15 a 2). Dettagli: docs/ESITO_R6_PROPOSTA_FERMATE.md.
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
