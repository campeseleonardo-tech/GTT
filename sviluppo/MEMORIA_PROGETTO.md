# Memoria del progetto GTT

Ultimo aggiornamento: **22/10/2026**. File unico di memoria: leggerlo all'inizio, aggiornarlo alla fine. Solo lo stato attuale, massimo 120 righe: i dettagli di un
risultato stanno nel suo documento in `docs/` (`R1_servizi.md` …), i piani aperti in `sviluppo/piani/`, la storia in git. Sezioni fisse (non aggiungerne): 1 Obiettivo · 2 Regole · 3 Cartelle e dati · 4 FATTO · 5 IN CORSO · 6 PROSSIMI PASSI · 7 MANCA · 8 Standard tecnici.

## 1. Obiettivo

Portfolio di Leo su Torino: capire come funziona la città (chi va dove, dove mancano servizi, dove sono le criticità) + pochi scenari «cosa succede se». Prodotti: la mappa
`mappa_torino.html` e i RISULTATI, uno alla volta (domanda → pochi numeri → grafici → limiti), come schede in `risultati.html`; mappa e schede sono due filoni separati.
Interesse in crescita: traffico, parcheggi, costi. I dati MISURATI (raccolta su leopi, sempre attiva) devono calibrare quelli simulati.
Risultati: **1** servizi · **2** metro di notte (**in pausa**, scheda nascosta) · **3** più passaggi su una linea e **5** linea nuova (ne farà **uno solo**, Leo 20/10) ·
**4** puntualità e attese (con l'ex 9) · **6** parcheggi per lasciare l'auto · ~~7 bici~~ (tolto) · **8** traffico. Un documento per risultato: `docs/R1_servizi.md`,
`R2_metro_notte.md`, `R4_puntualita.md`, `R6_parcheggi.md`, `R8_traffico.md` (domanda, criteri, numeri, limiti, comando per rifarlo). Scenari in `data/scenari/<nome>.json`,
avviso standard: «SIMULAZIONE SU ORARIO PROGRAMMATO — non tiene conto di traffico, ritardi, capienza, domanda reale.»
**Racconto per il portfolio** (Leo, 22/10): il progetto mette alla prova sui dati veri di Torino quello che la sua tesi triennale
(2020, Industry 4.0 e smart city, solo letteratura) prometteva: «la tesi era la promessa, il progetto è la verifica» (limiti dell'IoT e
della qualità dei dati). Cornici, temi in comune, dati da verificare e frase per il post in `sviluppo/TESI_E_PROGETTO.md`.

## 2. Regole di lavoro

- Con Leo: passo passo; decisioni importanti chieste prima, piccole scelte con default dichiarati; spiegazioni semplici, senza gergo.
- **Verifica indipendente** di ogni fatto importante sui file veri prima di darlo a Leo; Claude ricontrolla i numeri degli agenti esterni.
- Git: sul PC ramo `prova`; **commit e push sempre automatici** a fine lavoro (Leo, 20/10; dettagli in `AGENTS.md`). Nelle sessioni cloud ramo `claude/...`, che Leo unisce in `prova`
  (merge sempre con `--no-edit`). Repository **pubblico**: niente segreti né dati personali in git. Non modificare `data/raw` né lo storico: solo leggere.
- Script provati su campione prima del giro vero. Python del PATH (3.14), non Anaconda (json rotto); sul Pi Python 3.13. Orari: il PC è in ora italiana.
- Accesso: terminale sul PC e SSH **in sola lettura** verso il Raspberry Pi di casa (leopi; indirizzo, utente e chiave in `config_locale.json`, fuori da git, modello `scripts/config_locale.esempio.json`). Scrivere o riavviare sul Pi → `.bat` a doppio clic per Leo
  (`cd /d "%~dp0.."`, log in `logs/`, stop al primo errore); calcoli lunghi in una finestra `.bat` propria.
- Tag dati: [MISURATO]/[PROGRAMMATO]/[STIMATO]/[CENSIMENTO]/[DATI SCARSI]. Niente dati personali; vulnerabilità solo con l'indice dedicato, mai nazionalità.
- Piani aperti in `sviluppo/piani/PIANO_*.md`; a lavoro chiuso il contenuto vivo passa nel documento del risultato e qui, il piano si cancella. Documenti e script superati si **cancellano** (Leo 21/10).
- Agenti esterni (modello minore, PC o cloud): un giro per volta (mai due insieme), commit e push da soli, database in sola lettura, esito in `sviluppo/piani/ESITO_*.md` (cancellato dopo il ricontrollo).
- Le soglie e le regole di un risultato si fissano **prima** di vedere i numeri (R6, R8). Regole di Leo per il R6: le sue osservazioni non entrano nei dati (solo controllo a posteriori,
  `data/ref/parcheggi_osservazioni.json`); in pagina niente versioni, scenari, eventi, classi dei parcheggi.
- Prova delle pagine nel browser integrato: `.claude/launch.json` → `pagine-gtt` (porta 8765).

## 3. Cartelle e dati

Radice: `README.md`, `mappa_torino.html`, `risultati.html`, `index.html`, `MEMORIA_PROGETTO.md`, `AGENTS.md`. `docs/`: `METODO.md` (dati, area, accessibilità, etichette, colori), `FONTI_DATI.md`,
un documento per risultato, `piani/`, `rapporti/` (`RAPPORTO_*.txt` riscritti dagli script, grafico del traffico, `RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`).
`data/` (non in git): `raw/` (non toccare), `processed/`, `otp/` (R5), `scenari/`, `catalogo/`. `scripts/prove/`: strumenti di controllo del giro 4 della mappa (estrai/trasforma i dati, controllo dei valori).
Script: 01-20 dati · 21-22 R1 · 23 vulnerabilità × servizi · 24 importanza vie · 25 R6 v1 (le sue uscite le leggono 68, 72, 73) · 26 velocità 5T · 27 R4 · 28-29 R2 · 30-32 rapporto sostenibilità
(chiuso, si lanciano a mano) · 33-67 + `rete_osm.py` traffico R8 (35-38b abbinamento sensori, 37 metodi A/B, 49-50b modello V3 e 62-63 V4: le uscite sono lette dal 53, 65-67 e dalla scheda R8: **non cancellarli**) ·
70 attesa (R4) · R6: 68-69 inventari, 71-73 riempimento/nodi/segnali, 77 modulo strade, 79 dati mappa, 80 solo funzioni usate da 84-85, 81 auto che passano, 82 parcheggi adatti, 83 fermate importanti,
84 risultato, 85 verifiche, 94 bus contro auto · 86 controllo dei file caricati dalle pagine (esistono? sono in git?; non scrive più il README) · 87 popolarità zone e linee utili · 88 confronto auto/sensori 5T · 92 esposizione al traffico (R1) ·
93 tempi TP contro auto (R8) · 95 case × fragilità × servizi (parte E, solo Torino, zone OMI) · `comuni.py` funzioni comuni · `schede_risultati.py` schede · `controlla_leopi.py`, `supervisore.py`, `06_dati_live.py`, `03`, `12` girano/si installano sul Pi · `controlla_rami.py` rami e GitHub. **Prossimo numero libero: 96.**
Catene `.bat` (in `scripts/`): `RACCOLTA_GIORNALIERA` + `INSTALLA_RACCOLTA_GIORNALIERA`, `CONTROLLA_LEOPI`, `CONTROLLA_RAMI`, `AGGIORNA_RACCOLTA_LEOPI` (porta 03 sul Pi), `FETCH_LEOPI_E_VELOCITA_5T`,
`ACCESSIBILITA_24ORE`, `R1_PIEDI_5_10`, `RISULTATO1_VUOTI`, `RISULTATO1_CANDIDATI`, `RISULTATO6_RIFAI`, `TRAFFICO_RILANCIA_SENSORI`, `TRAFFICO_RICALCOLA_MODELLO`, **`RIFAI_MAPPA_E_SCHEDE`** (04, schede, 86, prova pagine).

| Dato | Note |
|---|---|
| GTFS GTT | 215 linee, 7.045 fermate (versione 20261002, valida fino al 31/01/2027) |
| Storico leopi | copia `data/storico_backup.sqlite` ogni giorno alle 07:30 (`RACCOLTA_GIORNALIERA.bat`, attività Windows «GTT raccolta giornaliera»; copia anche `stat.js`, `replay_*.js`, controlla la raccolta). Sul Pi **un solo servizio** `gtt-raccolta` (supervisore → 03 + 12 ritardi). Pesa **2,1 GB**, cresce ~190 MB/giorno (ritardi): la copia intera dura ~10 min; verso 6-8 GB servirà copia incrementale o pulizia (il supervisore avvisa oltre 10 GB). Mezzi GTT, ritardi dal 10/10, 5T traffico, parcheggi 5T e ZTL dal 14/10. Il mezzo 2897U ha l'orologio ~3 anni avanti (il 04 scarta le letture lontane oltre 1 h). Le analisi (26, traffico, R6) si lanciano a mano |
| Ritardi GTT | ~90 linee urbane, 05-24, ~80% delle corse programmate presenti (`docs/R4_puntualita.md`) |
| 5T traffico | già veicoli/ora; 112 sensori (3 codici doppi corretti sul Pi il 17/10); feed aperti solo 3: traffico, parcheggi, ZTL (ferma al 2024) |
| Censimento 2021 | 8.317 sezioni, 1.557.493 abitanti (Torino 848.748), 69 comuni. IMQ 2022: spostamenti ora × modo × scopo × O/D, 101 zone della Città metropolitana |
| Servizi | catalogo comunale (Torino) + OSM (cintura, più povero). OMI 2025/2 in `data/raw/omi_2025_2`. Fonti e indirizzi: `docs/FONTI_DATI.md` |

## 4. FATTO

- **Raccolta leopi**: attiva dal 3/10, copia giornaliera e controllo automatici; il feed tempo reale GTT è stato fermo il 18/10 dalle ~09:05 (guasto esterno, buco nei dati).
- **Accessibilità (18)**: 24 fasce orarie; piedi 15 min (80 m/min), TP 45 min; `--solo-piedi` per 5 e 10 minuti. **«Tutti i servizi»**: punteggio 0-100 calcolato nel browser, percentili separati Torino/cintura (non confrontabili). `docs/METODO.md`.
- **R1 servizi** (21-22, 92): a piedi copertura a 15 minuti 99,2%, a 10 96,8%, a 5 68,3%; **362 torinesi in zone abitate con 3+ servizi mancanti** (5 sezioni in collina, confermate), 6.768 in zone poco abitate
  (sotto 1.000 ab/km², grigio), 389 «da verificare»; esposti al traffico 22,6% (180 tratte molto trafficate come nel R8); cintura con piedi o TP 45' alle 8; candidati per gruppo (scuole 5, salute 5, cibo 3, fermate 1, verde 0). Manca il per circoscrizione (campo assente). `docs/R1_servizi.md`.
- **R2 metro di notte** (28-29, **in pausa**, Leo 20/10: non risponde a «tornare a casa la sera»; ripresa con il «popolo della notte» IMQ 00-05): ogni 15' → **334.085 residenti con almeno +25% di servizi** (ogni 30': 153.062); con qualsiasi miglioramento 773.307 (652.891). `docs/R2_metro_notte.md`.
- **R4 puntualità e attese** (27, 70), **tutto sul GPS dei mezzi** (il feed sottostimava i ritardi di 2-3 volte), 7 feriali, copertura GPS 77%: **13,3% oltre 5 minuti** (feed 5,2%), 5,05% oltre 10 (GTT dichiara 2,3% per il 2025, metodo non
  pubblicato), grappolo+buco 20,4%; tram 13,0%, bus 13,4%; peggiori 17, 6, 19, 66, 68. «Oltre 10 minuti» in 4 definizioni: a ogni fermata 5,49%, prima fermata 3,92%, metà corsa 5,24%, fuori punta 5,30% (la definizione spiega solo parte della differenza).
  Tema «Puntualità delle linee» in mappa. `docs/R4_puntualita.md`.
- **R6 parcheggi** (24-25, 68-73, 77, 79-85, 87, 88, 94): fermate importanti con regola fissa (≥ 10 corse/ora o metro/stazione/capolinea, e ≥ 1.000 auto in entrata, scelta di Leo): **274**, **179 senza posti bastanti** entro 400 m a piedi
  (68 senza alcun parcheggio adatto); **12 punti prioritari** (uno per asse, ≥ 3 km dal centro, ≥ 50 posti mancanti; Maroncelli e Chieri escono, Leo: lasciare così); auto in entrata 87.162, chi già lascia l'auto 5,8% (64 interviste), torinesi inclusi 34%;
  in mappa anche 80 parcheggi del centro (viola), 2 viste. **Parte C bus contro auto** (94): 0 conviene, 1 dipende (Metro Massaua), 11 no; interscambi 0/3/2; messaggio della scheda «funzionano solo dove il mezzo pubblico è veloce: oggi 1 punto su 12»;
  sensibilità ai minuti di parcheggio in centro 5 → 1, 10 → 10, 15 → 12 punti competitivi (classe ufficiale 5 minuti). `docs/R6_parcheggi.md`; catena `RISULTATO6_RIFAI.bat` (~4 min). **Rifatto 22/10 con 5 feriali** (15, 16, 19, 20, 21/10): numeri sopra invariati (274, 179, 12 punti, 0/1/11, pareggio 20,85–27,5); cambia solo la classe di LANCIA (misto → residenziale). `sviluppo/piani/ESITO_P0.md`.
- **R8 traffico** (33-67, 93): stima C-DEBOLE, errore mediano 38,4% (±38%), rho 0,605, 20 punti di misura; 95,3% dei km di strade grandi di Torino serviti dal TP (vale solo per le strade grandi); «molto traffico e poco TP» quasi solo Corso Regina Margherita ovest.
  **Parte D** (93): tempo coi mezzi contro auto, forbice con due fattori di punta (1,2 sensori 5T; 2,1 Google Maps): rapporto mediano **da 1,96 a 2,94** («da 2 a 3 volte il tempo dell'auto»), auto oltre 2 volte da 41% a 97%; cintura-cintura a parte. `docs/R8_traffico.md`.
- **Mappa** (giri 1-4 fatti): partenza senza tema su satellite, due gruppi di temi, «Chi abita qui» (8 viste), «Fragilità sociale», «Servizi a portata», «Servizi mancanti», «Prezzo delle case», «Mezzi pubblici sotto casa», «Spostamenti» (IMQ),
  «Velocità e traffico» (medie per tipo di giorno), «Ritardi delle linee», «Parcheggi di scambio», «Luoghi della città»; niente dati live, corse simulate, pendolari, avvisi. **Giro 4 fatto** (5,9 MB, «Luoghi della città» a 6 caselle).
- **Schede** (`schede_risultati.py` → `data/schede_risultati.js`): `index.html` (ingresso), `risultati.html` con schede R1, R4, R6, R8 e R10 «Case, servizi e fragilità» (da controllare sui dati veri: piano 3); numerazione in pagina 1-5 (`numero_pubblico`: R1→1, R4→2, R6→3, R8→4, R10→5; link `#rN` interni validi, nuovi `#pN`) (titolo-risposta, numero grande, grafico, 3 punti chiave, parti chiuse; R2 nascosto). Rieseguire lo script dopo ogni rilancio di un risultato.
- **Rapporto sostenibilità GTT 2025**: 980 fatti verificati (`docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`). **Ora legale** controllata (conversioni UTC → italiana coincidono con il fuso ufficiale su 35.040 istanti 2026-27).
- **Pulizia** (21/10): documenti, script e `.bat` superati cancellati; il resto (README, `sviluppo/`, `main`) nel piano 1. Giro 4 della mappa, R6 minuti di pareggio, R4 giro 6 e script 95 lanciati sul PC (21-22/10).

## 5. IN CORSO

- **Cinque piani** (22/10, rivisti dopo l'analisi: ripetizioni tolte, aggiunte) in `sviluppo/piani/`: **1** `PIANO_RIORGANIZZAZIONE` (`main` creato da Leo il 22/10, da rendere di default; repository
  rinominato **`Turin-mobility`** (fatto da Leo, sito «Torino Mobilità»), appunti in `sviluppo/`, script 86 che non riscrive più il README, Pages da `main`) · **2** `PIANO_DATI` (estratti in git + Release; dello storico
  solo i **riassunti**, Leo) · **3** `PIANO_RISULTATI` (R6 con 5 feriali e scheda 5 fatti 22/10, `ESITO_P0.md`; resta: R4 a un mese; etichetta [DATI SCARSI] dello script 71 da decidere con più settimane; A2, F, C4, E4 **fuori**, Leo) · **4** `PIANO_GRAFICA`
  (decisioni di Leo: mezzi in movimento in home; numeri che contano **solo** nei numeri grandi; omini, gara bus/auto (scheda 3) e area che si espande (scheda 4) nelle schede;
  ore che scorrono in mappa; `progetto.html`; un file di stile; verde acqua → corallo) · **5** `PIANO_CODICE`. `PIANO_COSTI` dopo la pubblicazione. **Prompt** per far fare tutto a un modello, giro per giro (CLOUD C1-C13, PC P0-P8, ordine e fermate per Leo): `sviluppo/piani/PROMPT_LAVORI.md`.
- **Rami** (22/10): nessun lavoro fuori da `prova`; i rami `claude/...` vecchi si cancellano (Leo). «Chi sono»: LinkedIn leocampese, email campese.leonardo@gmail.com. Niente contatore delle visite (Leo). Controllo fisso: `scripts\CONTROLLA_RAMI.bat` (`controlla_rami.py`).
- **Raccolta parcheggi** su leopi continua (R6 rifatto con 5 feriali il 22/10). `LICENSE` (MIT per il codice, dati con la licenza della fonte) creato il 22/10.
- Sul PC (Leo): cancellare il file `3)` e `scripts/*.bak_18ott`. Il vecchio nome della cartella OMI resta nella storia di git.

## 6. PROSSIMI PASSI

1. Piano 1: `main` è il ramo di default e i rami vecchi sono cancellati (Leo, 22/10); restano i passi 4-7 (cloud). Sul PC: `RISULTATO6_RIFAI.bat` e `RIFAI_MAPPA_E_SCHEDE.bat`, controllo della scheda 5.
2. Piano 2: inventario dei dati (script 96 sul PC) e licenze delle fonti; piano 4: prove di stile (cloud), Leo sceglie.
3. Rilanci con più dati: R4 con un mese (metà novembre), poi stagione. Screenshot di Leo per la scheda R6.
4. Più avanti: tempi TP contro auto per coppie di zone IMQ e costi (`PIANO_COSTI.md`); R2 ripreso (popolo della notte), treni SFM, scenario fra R3 e R5, effetto ZTL, tram contro bus.
- Metrica trasversale (Leo, 16/10): «quanti veicoli in meno potrebbero girare»; luoghi «speciali» (stadi, fiere, ospedali…) con parametri fissi. **Congelate** (Leo, 20/10): bici, telefonia, logistica, eventi.

## 7. MANCA (limiti noti)

- Dati: passeggeri/affollamento, bici, costi del servizio, merci, taxi, treni SFM e bus extraurbani di altre aziende (fonte possibile: GTFS regionale Piemonte). Occupazione parcheggi solo dal 14/10.
- Domanda = residenti + IMQ per zona, non persone in movimento per sezione. Cintura: servizi OSM incompleti, non confrontabili con Torino (nel catalogo comunale dentro Torino, OSM fuori).
- Accessibilità e scenari su orario programmato: ottimisti per definizione; di notte nessuna sezione di Torino è mai a zero TP (bus notturni): guardare sempre il miglioramento, non la soglia zero.
- Traffico: 20 punti di misura, stima debole (±38%), solo residenti 11-84 anni; velocità 5T: «urbano» = nome con «(TO)», include alcune provinciali (limiti completi in `docs/R8_traffico.md`).
- R4: GPS solo sulle linee urbane (~90), le extraurbane non ci sono; ritardi e attese di bus con meno dati dei tram; GTT non pubblica il metodo del suo 2,3%.
- R6: i «posti che mancano» sono ordini di grandezza (quota da 64 interviste × traffico ±38%); il modello del traffico senza code preferisce le strade veloci; riempimento misurato solo per pochi garage 5T. Controllo con i sensori 5T (88): rho 0,83 per sensore,
  **0,60 per luogo (debole)**, 0,52 senza i sensori fuori rete; il modello sottostima le provinciali (SP1, SP8, SP2) e sopravvaluta C.so Giulio Cesare, Unione Sovietica, Allamano, Sebastopoli. Tempi dei mezzi solo GTT, senza treni; costo del parcheggio non considerato.
  Popolarità delle zone = arrivi IMQ senza ritorni a casa, classifica solo nella Città metropolitana; linea utile = 25% con più zone fra le 20 più popolari; molti parcheggi adatti non hanno linee utili vicine.
- Script 80 e 77 sembrano superati ma servono (funzioni per 84-85, modulo per 72-73). Le uscite delle fasi 3-4 del traffico sono lette dalla Fase 5. Codice copiato (distanze, radice, ora legale) in molti script: si passa a `comuni.py` quando si tocca uno script.
- `mappa_torino.html` (5,9 MB) resta in git: GitHub Pages la pubblica da `main` (piano 1).

## 8. Standard tecnici

- **Bug di resa**: `node --check` trova solo errori di sintassi; colori, legende e dati non disegnati si controllano aprendo la pagina e usando l'interfaccia. Prova automatica: `python scripts\prova_pagine_r6.py` (errori a runtime su mappa e schede, tutti i temi).
- **Fermate e strade**: mai abbinare per nome, solo per coordinate. Un corso che cambia nome o comune è un solo asse; l'unità del traffico è la tratta d'asse. Script 24: corridoio = stesso nome + tratti collegati o entro ~100-200 m; togliere «(TO)» dai nomi 5T.
- **Mappa**: `D.sezioni` è a colonne e in forma compatta (`compatta_sezioni` nel 04; lettori nel blocco DECODIFICA del template: cambiarli insieme). Un campo nuovo di sezione va in `COLONNE_SEZ` (o in una colonna codificata) nel 04 **e** nella proiezione `sez` del template.
  Chi cambia l'ora (`#ora`) richiama `aggiornaLegenda()`. Numeri in italiano (virgola decimale). Il centro delle sezioni si calcola dal riquadro delle forme originali.
- **Script 18**: la firma dei parziali non contiene il percorso del GTFS né l'uscita: cancellare `data/processed/accessibilita_parziale/` prima di ogni lancio con GTFS o opzioni diverse (`--solo-piedi` salta il TP, `--ore` si ignora).
- **Controlli negli script**: si fermano solo per errori di struttura (file mancante, somme che non tornano, valori negativi); un numero diverso da quello di oggi è un AVVISO. Funzioni comuni (distanze, ora legale, percentili, zona centrale Q001-Q009) in `scripts/comuni.py`. Ogni risultato ha una verifica su fatti noti.
- **`.bat`**: terminazioni di riga Windows (`.gitattributes`: `*.bat text eol=crlf`); log in `logs/`, stop al primo errore. **Bridge** (chat senza terminale): `device_commit_files` a volte non scrive i file grossi; rileggere dopo.
- **Colori**: verde→rosso (bene/male) e blu→arancione (quantità) erano una **direzione, non una regola** (Leo, 22/10): si ripensano con lo stile nuovo (piano 4). Regola che resta: le legende scrivono sempre i numeri (daltonismo).
