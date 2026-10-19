# Piano meccanico — Correzioni generali del progetto e del Risultato 6 (20/10/2026)

Scritto da Claude con Leo, per un altro modello (agente), a partire da `docs/ANALISI_PROGETTO.md` e
`docs/ANALISI_RISULTATO6.md` (leggile **prima** di iniziare: spiegano il perché di ogni correzione).
Leo ha scelto (20/10): **correggere tutti gli errori**; i torinesi entrano nella domanda **solo se tolgono tante
auto**, altrimenti ci si concentra sulla **cintura**; treni SFM **fuori da questo piano**; il portfolio è per un
pubblico **italiano e straniero**.

Esegui **tutte le fasi, nell'ordine, senza fermarti a chiedere**. Dopo ogni passo scrivi in
`docs/ESITO_CORREZIONI_GENERALI.md` una riga `PASSO n.m: OK` oppure `PASSO n.m: FERMO – motivo`, poi i numeri
richiesti. Se un passo è FERMO, i passi che dipendono da lui diventano `NON ESEGUITO – dipende da n.m` e si va
avanti con gli altri. Se un controllo non torna: correggi se la causa è tua e chiara; altrimenti **non inventare**,
scrivi cosa hai visto e continua.

---

## 0. Regole (valgono per tutto il piano)

1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (`git branch --show-current`; se no, FERMATI del tutto).
   **Nessun commit** (decide Leo). Python del PATH (3.14), comando `python`; **mai Anaconda**.
2. Sola lettura su `data/raw/`, su `data/storico_backup.sqlite` (`sqlite3.connect("file:data/storico_backup.sqlite?mode=ro", uri=True)`)
   e sul Raspberry Pi (SSH solo per leggere). Unica eccezione in `data/ref/`: il passo 2.9.
3. Librerie: solo quelle già installate (numpy, scipy, pandas, shapely, pyproj, osmium, networkx se c'è). Niente
   download da internet.
4. Prima di ogni script lungo: `--prova` (dove c'è), poi completo. Scrivi i tempi nell'esito.
5. Ogni script nuovo o modificato ha in cima la docstring in italiano semplice (cosa fa, cosa legge, cosa scrive,
   come si lancia, cosa è cambiato il 20/10).
6. **Ogni valore predefinito di questo piano** è una costante in cima allo script **e** un'opzione da riga di
   comando, ed è scritto nel rapporto.
7. **Niente numeri attesi scritti nel codice come condizione per andare avanti.** I controlli sono di due tipi:
   - **bloccanti** solo per errori di struttura: file mancante, lista vuota, valore negativo, somme che non
     tornano (es. ogni fermata in una sola area), coordinate fuori dalla Città metropolitana;
   - **avvisi** per tutto il resto (numeri diversi da prima, conteggi fuori da un intervallo atteso): si stampano
     con `AVVISO:` e si scrivono nel rapporto, ma lo script continua.
8. Distanze: haversine in metri. Ore: database in UTC, ora italiana con la regola dell'ultima domenica di marzo e
   ottobre (funzione del modulo comune, passo 1.1). Fermate, strade e parcheggi **mai per nome**, solo per
   coordinate.
9. Etichette: [MISURATO] [PROGRAMMATO] [STIMATO] [CENSIMENTO] [DATI SCARSI]. Italiano semplice, numeri con la
   virgola decimale e il punto delle migliaia.
10. Regole di Leo che **non cambiano**: le osservazioni di Leo non entrano mai nei dati né nei testi pubblici
    (solo controllo a posteriori nei rapporti); niente «posti utili» (tolti il 19/10); nei testi pubblici mai
    «v1/v2», «versione», «scenario», «S2», «giro»; colori verde→rosso per bene/male, blu→arancione per quantità
    neutre; le legende scrivono sempre i numeri.
11. Script nuovi: numeri **81, 82, 83** (più `comuni.py` e `controlla_leopi.py`). Il prossimo numero libero dopo
    questo piano è **84**.
12. Se una pagina va controllata: `python scripts\prova_pagine_r6.py` (passo 1.7 la estende a tutte le pagine) deve
    dare **0 errori**. Il controllo a occhio nel browser lo fa poi Claude con Leo.

## 1. Valori predefiniti (Leo può cambiarli in questa tabella prima di lanciare)

| Nome | Valore | Dove |
|---|---|---|
| Zona centrale (fermate **e** parcheggi) | Q001-Q009 | `comuni.ZONE_CENTRALI` |
| Auto = | conducenti (`MEZZO1` 03) + car sharing (21); i passeggeri (04) solo come informazione | 73, 81 |
| Mattino | partenza 06:00-09:59 | 73, 81 |
| Torinesi nella domanda se | auto dai quartieri periferici verso Q001-Q009 al mattino ≥ **25%** delle auto che entrano dalla cintura | 81 `--soglia-torinesi 0.25` |
| Segnali del punteggio | a2 (strada), b2 (corse nelle ore dei pendolari), c4 (auto in entrata che passano accanto), e (metro/stazione) — pesi uguali | 75 |
| Fermate importanti | 10% più alto fra i luoghi della Città metropolitana **fuori** dalla zona centrale | 75 |
| Parcheggi adatti all'interscambio | aperti, fuori dalla zona centrale, ≥ 20 posti l'uno, non «di destinazione» (ospedali, università, centri commerciali) | 82, 80 |
| Distanza a piedi | linea d'aria × **1,3**; raggio **400 m a piedi** (≈ 308 m in linea d'aria) | 80 |
| Fermata coperta | ≥ **50** posti (decisione di Leo, invariata) | 80 |
| Aree | esagoni lato 900 m; colorate solo con ≥ **5** fermate importanti | 80 |
| Date di riferimento della mappa | martedì 10/11/2026, sabato 14/11/2026, domenica 15/11/2026 | 04 |

---

## FASE 0 — Preparazione

**0.1** Ramo `prova` (regola 0.1). `git status`: scrivi nell'esito i file già modificati prima di iniziare.
**0.2** Crea `docs/ESITO_CORREZIONI_GENERALI.md` (titolo, data, ora di inizio).
**0.3** Copia di sicurezza (non sovrascrivere se esiste): `data/processed/risultato6_v2/*.json` →
`data/processed/risultato6_v2/prima_correzioni/`; `mappa_torino.html` → `data/backup/mappa_torino_prima_correzioni.html`;
`data/schede_risultati.js` → `data/backup/schede_risultati_prima_correzioni.js`.
**0.4** Numeri di partenza (dai file, non dal piano): scrivi nell'esito una tabella con: luoghi, fermate importanti
e classi (oggi 378: 147/59/172), aree per categoria, i 20 punti (nome e zona), parcheggi mostrati, parcheggi pieni.
Servono per il confronto alla fine.
**0.5** Controlla che esistano: `data/processed/imq/spostamenti.csv`, `data/processed/imq_zone.json`,
`data/processed/imq_zone_geo.json`, `data/processed/traffico_c/rete/` (rete di `rete_osm.py`),
`data/processed/traffico_c/punti.json`, `data/processed/traffico_d/` (tratte e assi), `data/otp/rete/torino_cintura.osm.pbf`,
`data/processed/sezioni_torino.json`, tutti i file di `data/processed/risultato6_v2/`. Se manca uno di quelli di
`traffico_c`: il passo 2.4 userà il ripiego (scritto lì), non è un FERMO generale.

## FASE 1 — Ordine e sicurezza del codice (nessun numero dei risultati cambia)

**1.1 Modulo comune `scripts/comuni.py`.** Funzioni: `trova_radice()`, `haversine_m()`, `ora_locale(dt_utc)`,
`percentile_rank(valori)` (copia identica di quella di `75_risultato6_v2.py`), `carica_script(nome_file)` (importlib
per gli script che iniziano con un numero), `controllo(nome, ok, bloccante=False, rapporto=None)` (stampa `OK`/`AVVISO`
e, se bloccante e falso, esce con codice 1), costanti `ZONE_CENTRALI`, `CENTRO_LAT/LON` (Piazza Castello 45,0711;
7,6857). In fondo una funzione di prova (`python scripts\comuni.py` stampa 3 controlli: haversine fra le stazioni Porta Nuova
(45,06120; 7,67780) e Porta Susa (45,07158; 7,66586) ≈ 1.487 m; ora locale del 25/10/2026 00:30 UTC = 02:30 e 01:30 UTC = 02:30; percentile di [1,2,2,3]).
**Usalo** in tutti gli script toccati da questo piano (68-83); **non** riscrivere gli altri script.

**1.2 Controlli → avvisi** (regola 0.7) in `73`, `75`, `76`, `79`, `80`. In particolare togli: le condizioni
378/147/59/172, «20 punti», «parcheggi mostrati tra 190 e 240», «Palavela tra i mostrati», «somma auto = 95.297»,
«somma domanda = 24.459», «c2 ±2% di 95.300». Restano **bloccanti** solo i controlli di struttura. Il controllo di
riproducibilità della v1 in 75 (611/17/594) diventa un avviso.

**1.3 `requirements.txt`** nella radice: cerca con `grep` gli `import` di librerie esterne in `scripts/` e scrivi le
versioni installate (`python -m pip show <nome>`). Nessuna installazione.

**1.4 Archivio (spostare, mai cancellare).**
- `docs/archivio/r6/`: `PIANO_RISULTATO6_V2.md`, `PIANO_RISULTATO6_V2_GIRO2.md`, `PIANO_RISULTATO6_FINALE.md`,
  `PIANO_INTEGRAZIONE_R6.md`, `PIANO_RISULTATO6_EVENTI_DATI.md`, `PIANO_R6_PORTE.md`, `PIANO_R6_DIREZIONI.md`,
  `PIANO_R6_ZONE.md`, `PIANO_R6_MIGLIORIE.md`, `PIANO_R6_CORREZIONI.md` e tutti gli `ESITO_*` del Risultato 6
  (`ESITO_RISULTATO6_V2*.md`, `ESITO_RISULTATO6_EVENTI_DATI.md`, `ESITO_INTEGRAZIONE_R6.md`, `ESITO_R6_*.md`).
  **Non** spostare i `RAPPORTO_*` (li riscrivono gli script). In `docs/PIANO_RISULTATO6.md` aggiorna i percorsi citati.
- `scripts/archivio/`: `calcola_simulazione.py` e `scenario_esempio.json` (prima controlla con `grep` che nessuno
  script li importi o li legga).
- `.bat` della radice (`RAPPORTO_*.bat`, `RISULTATO2_*.bat`) → `scripts/`, cambiando `cd /d "%~dp0"` in
  `cd /d "%~dp0.."`. Controlla con `grep` che nessun altro file li citi col vecchio percorso (aggiorna i citati).
- **Non toccare** `supervisore.py`, `06_dati_live.py`, `03_raccolta_continua.py`, `installa_*.sh`: girano sul Pi.
- `sync_da_leopi.bat`: **solo se** la mappa non legge più `live.js` né `replay_*.js` (cerca nel template); altrimenti
  lascialo e scrivilo.
- `TRAFFICO_RILANCIA_SENSORI.bat`: per ogni passo delle fasi 3-4 (37, 43-45, 50b, 53-54) controlla con `grep` se un
  suo file di uscita è letto dagli script della Fase 5 (57-67), da `04_genera_mappa.py` o da `schede_risultati.py`.
  Togli dal `.bat` (mettendo `rem` davanti, non cancellando) **solo** i passi che nessuno legge. Elenca nell'esito
  cosa hai tolto e cosa hai tenuto, con il motivo.

**1.5 Date di riferimento della mappa** (`date_riferimento` in `04_genera_mappa.py`): costanti `DATA_FER =
2026-11-10`, `DATA_SAB = 2026-11-14`, `DATA_DOM = 2026-11-15` (opzione `--date AAAA-MM-GG,AAAA-MM-GG,AAAA-MM-GG`). Se
una data è fuori dalla validità del GTFS o non ha servizi attivi: AVVISO e si torna alla regola vecchia per quella
data. Scrivi nell'esito le date usate e le corse del giorno feriale prima/dopo.

**1.6 Dati inutili nella mappa**: cerca nel template se `D.mezzi` (110 posizioni del 3/10) è usato; se no, non
scriverlo più in `04`. Gli avvisi (`D.avvisi`) restano. Scrivi il peso di `mappa_torino.html` prima/dopo.

**1.7 Prova automatica di tutte le pagine**: estendi `scripts/prova_pagine_r6.py` (tieni il nome, aggiungi
`--tutte`, predefinito sì): apre **ogni tema** della mappa (leggi l'elenco dei temi dal template), le tre viste del
Risultato 6 e `simulazione.html`; se Edge manca prova Chrome. Aggiungi `--cartella` per provare una copia (serve
alla fase 6). Lancia ora: scrivi nell'esito gli errori trovati **prima** di ogni altra correzione (se ce ne sono,
correggili solo se la causa è chiara e piccola; altrimenti elencali).

**1.8 Controllo della raccolta su leopi** (`scripts/controlla_leopi.py` + `scripts/CONTROLLA_LEOPI.bat`): via SSH
(chiave `%USERPROFILE%\.ssh\id_gtt_leopi`, utente `leopi@192.168.8.200`), **solo lettura**, lancia sul Pi un piccolo
`python3 -c` che apre il database in sola lettura e stampa per ogni tabella raccolta (mezzi, ritardi, 5T traffico,
parcheggi, ZTL: leggi i nomi in `03_raccolta_continua.py`) l'ultima lettura. Esito: `OK` se ogni tabella ha letture
negli ultimi 30 minuti (ZTL: ultime 26 ore; di notte, 00-05 ora italiana, i ritardi possono mancare), altrimenti
`ALLARME` con la tabella ferma. Log in `logs/controlla_leopi.log`. Se il PC non vede il Pi: scrivi «Pi non
raggiungibile» e passa oltre. Nell'esito il comando `schtasks` (non eseguirlo) con cui Leo può farlo girare ogni
mattina alle 8.

**1.9 Catena del Risultato 6 in un solo file**: `scripts/RISULTATO6_RIFAI.bat` che lancia nell'ordine
71 → 72 → 73 → 81 → 82 → 75 → 80 → 79 → 76 → 04 → `schede_risultati.py` → `prova_pagine_r6.py`, si ferma al primo
codice di errore e scrive il log in `logs/risultato6_rifai.log`. Va creato ora e usato dalla fase 3 in poi.

## FASE 2 — Risultato 6: i segnali corretti

**2.1 Auto, non persone** (`73_segnali_criticita.py`). Oggi `c2` conta `MEZZO1` 03, 04, 21: i passeggeri (04) sono
persone, non auto. Nuovo `c2` = 03 + 21; salva anche `c2_persone` (03 + 04 + 21). Stessa correzione per `f`: solo 03 e
21 (oggi include 04 e la moto 05). Scrivi nell'esito i totali prima/dopo (oggi 95.297 e 24.459).

**2.2 Zona centrale unica.** Per **fermate e parcheggi** la zona centrale è `comuni.ZONE_CENTRALI` (Q001-Q009). In 72
(`--zone-centrali`) e 75 (oggi `ZONA_ESCLUSA = "Q001"`) usa la costante comune.

**2.3 Torinesi sì o no** (in `81_auto_di_passaggio.py`, prima parte). Dai microdati IMQ (stessi filtri di 2.1, mattino):
- `M_cint` = auto con `COD_PAR` non `Q…` (e non vuoto) e `COD_ARR` `Q…`;
- `M_tor` = auto con `COD_PAR` `Q…` **fuori** dalla zona centrale e `COD_ARR` dentro la zona centrale.
Regola: se `M_tor ≥ 0,25 × M_cint` i torinesi entrano nella domanda (`torinesi = true`), altrimenti no. Scrivi nell'esito
i due numeri, le interviste e la decisione. (Con o senza torinesi, le fermate dei quartieri periferici di Torino
restano **luoghi possibili**: lì si fermano anche le auto che arrivano dalla cintura.)

**2.4 Nuovo segnale c4: auto in entrata che passano accanto al luogo** (`81_auto_di_passaggio.py`, seconda parte).
È la correzione del difetto principale (oggi c2 dà ai quartieri le auto che **arrivano**).
1. Domanda: le auto del mattino del passo 2.3 (`M_cint`, più `M_tor` se `torinesi`), come celle
   `[COD_PAR, COD_ARR, ora, PESO, 1]`, lo stesso formato di `traffico_c/domanda_auto.json`.
2. Instradamento sulla rete di `traffico_c/rete/` con lo **stesso metodo di `42_instradamento.py`** (percorso più
   veloce, tutto o niente, punti pesati delle zone da `traffico_c/punti.json`, zona `FUORI` come in 42). Carica 42 con
   `comuni.carica_script` e riusa `carica_domanda_nodi`; il ciclo di Dijkstra copialo in una funzione di 81 (non
   modificare 42). Salva in `data/processed/risultato6_v2/auto_passaggio.npz` il flusso per arco e in `auto_passaggio.json` il
   riepilogo, `M_cint`, `M_tor`, `torinesi` e `c4` per luogo (lo legge 75).
3. Per ogni luogo (tutti i 5.087): `c4` = il flusso più alto, sommando i due versi, fra gli archi entro **100 m** (distanza
   punto-tracciato di `rete_osm.distanza_punto_tracciato_m`). Nessun arco entro 100 m → `c4 = 0`.
4. Controlli (avvisi): somma dei pesi instradati ≈ domanda (scrivi quanto si perde e perché); 20 percorsi verificati
   con `verifica_networkx` di 42 (se networkx c'è); i 15 luoghi fuori dalla zona centrale con `c4` più alto (nome,
   zona, strada) — **ci si aspetta** che ci siano ingressi come Corso Francia, Corso Unione Sovietica, Strada Genova,
   Corso Giulio Cesare/Torino-Milano, la tangenziale: se nessuno di questi compare, AVVISO forte e descrivi.
5. **Ripiego** (solo se l'instradamento non si può fare: file mancanti o errore non risolvibile): `c4` = auto che
   **partono** dalla zona del luogo (solo zone non `Q…`; zone `Q…` = 0). Scrivi `c4_metodo = "ripiego"` ovunque.
6. Il flusso è una stima del modello del traffico (classe C-DEBOLE): nei testi pubblici si mostra **arrotondato alle
   centinaia** e con «[STIMATO, ordine di grandezza]».

**2.5 Punteggio corretto** (`75_risultato6_v2.py`, nuovo scenario `S4` «corretto»; S1-S3 restano per confronto).
- Segnali: **a2, b2, c4, e**, pesi uguali (opzione `--pesi a2=1,b2=1,c4=1,e=1`). a1 e c1 escono (erano doppioni di a2
  e c2); d esce dal punteggio (c'è in ~90 luoghi) e resta come informazione.
- Segnali mancanti: **non** si fa più la media sui soli disponibili. a2 mancante (nessuna strada entro 150 m) = 1
  (strada minima); c4 mancante = 0. Nessun luogo dell'universo resta senza punteggio.
- Percentili e soglia del 10% fra i luoghi **eleggibili**: universo Città metropolitana (come oggi) **meno** i luoghi
  della zona centrale. e resta 0/100.
- Salva in `scenari.json` → `scenari.S4` la stessa struttura degli altri, più `segnali_usati`, `pesi`, `torinesi`,
  `c4_metodo`. 80 legge `S4` (costante `SCENARIO`).
- Sensibilità di S4 (quante fermate importanti cambiano): senza a2, senza b2, senza c4, senza e; c4 col ripiego al
  posto dell'instradamento; soglia 5% e 15%; con i torinesi forzati sì/no.
- Confronto con S2 (oggi): quante restano, entrano, escono; quante fermate importanti per zona prima/dopo.

## FASE 3 — Risultato 6: parcheggi, copertura, aree, punti, validazione

**3.1 Parcheggi «di destinazione»** (`82_parcheggi_destinazione.py`). Dal PBF OSM (osmium, `apply_file(...,
locations=True)`, aree con `osmium.area`) prendi le aree con `amenity` in {hospital, university, college} o
`landuse=retail` o `shop=mall`. Un parcheggio OSM è «di destinazione» se il suo centro cade dentro una di queste aree
o a meno di 50 m dal bordo. Scrivi `data/processed/risultato6_v2/parcheggi_destinazione.json` (`id`, motivo, nome
dell'area) e nel rapporto i conteggi per motivo e i 20 più grandi esclusi. I parcheggi 5T/Comune non si toccano
(quelli centrali escono già per la zona).

**3.2 Insieme dei parcheggi adatti all'interscambio** (in `80_porte_interscambio.py`): tipi `interscambio_ufficiale`,
`garage_5t`, `park_ride_osm`, `osm_pubblico`; **fuori** dalla zona centrale; **≥ 20 posti** l'uno (dichiarati o stimati
a 25 m²); non «di destinazione». Gli altri parcheggi aperti restano nel file con `adatto = false` e il motivo.
Nel rapporto la catena dei conteggi: trovati → aperti → fuori centro → ≥ 20 posti → non di destinazione.

**3.3 Distanza a piedi**: `dist_piedi = linea d'aria × 1,3` (`--fattore-piedi`); copertura entro **400 m a piedi**
(`--raggio-piedi`). Classi della fermata sui posti dei parcheggi adatti entro il raggio: «Nessun parcheggio» (0),
«Pochi posti» (1-49), «50 posti o più». Sensibilità: 300/400/500 m a piedi; 30/50/100 posti; senza il filtro di
destinazione; senza la soglia dei 20 posti.

**3.4 Aree**: esagoni come oggi; categoria (Critica/Scarsa/Buona, soglie 60/30) **solo** con ≥ 5 fermate importanti
(`MIN_FERMATE_AREA = 5`); le altre hanno categoria «Pochi dati» (grigio, bordo tratteggiato) e **non** entrano nei
conteggi per categoria. Etichette come oggi (una per nome).

**3.5 I 20 punti**: raggruppamento come oggi (1 km di diametro) sulle fermate non coperte; ordine per somma dei
punteggi (come oggi). Per ogni punto aggiungi `auto_passaggio` = il `c4` più alto fra le sue fermate. «Parcheggi che
potrebbero ampliarsi» = solo parcheggi **adatti** con ≥ 100 posti entro 600 m **a piedi**, con lo stato di
riempimento; se uno è misurato pieno scrivi «già pieno».

**3.6 Parcheggi mostrati in mappa**: parcheggi **adatti** con ≥ 100 posti entro 400 m (linea d'aria) da una fermata
importante o da un nodo forte, **più** tutti gli interscambi ufficiali e i park & ride OSM (anche se piccoli o non
vicini). Togli la regola «tutti i garage 5T con dati» e ogni caso particolare (Palavela). I garage del centro **non**
si mostrano più in questo tema.

**3.7 Direzioni d'ingresso (solo riferimento), con una quota coerente**: `f_mattino` = spostamenti del mattino con
`MEZZO1` 03/21 e un mezzo pubblico dopo, `COD_PAR` non `Q…`, `COD_ARR` `Q…` (stesso universo di `M_cint`); quota =
`f_mattino ÷ M_cint`. Se le interviste di `f_mattino` sono meno di 30: quota e categorie segnate [DATI SCARSI]. Posti =
solo parcheggi adatti. Scrivi la quota vecchia (26%) e nuova.

**3.8 Validazione sugli interscambi esistenti** (rapporto e scheda). Per Stura, Caio Mario, Sofia, Venchi Unica, Fermi
scrivi: posti; riempimento misurato (G di giorno, N di notte, M al mattino, descrizione del profilo) o «non trasmette»;
adatto sì/no; distanza a piedi dalla fermata importante più vicina; `c4` della strada accanto e la sua posizione in
classifica fra i luoghi eleggibili; categoria dell'area. **Prima di guardare i risultati** scrivi nel rapporto cosa ci
si aspetta: un interscambio pieno dovrebbe stare su una strada con molte auto in entrata (c4 alto) e vicino a una
fermata importante. Poi l'esito per ognuno: «coerente», «non coerente» (perché), «non si può dire» (manca il dato).
In scheda vanno **solo i fatti misurati** (niente osservazioni di Leo).

**3.9 Controllo a posteriori con le osservazioni di Leo** (solo rapporto). Aggiungi a `data/ref/parcheggi_osservazioni.json`
(unica scrittura permessa in `data/ref/`) la voce: Fermi, «i parcheggi gratuiti intorno si riempiono soprattutto al
mattino» (Leo, 20/10/2026), stesso raggio della voce esistente. Nel rapporto: quanti parcheggi gratuiti (`fee=no`) adatti
ci sono entro il raggio, posti, e la frase «il metodo conferma / non conferma / non può confermare».

**3.10 Rilancio**: `scripts\RISULTATO6_RIFAI.bat`. Poi scrivi nell'esito la tabella prima/dopo (numeri del passo 0.4
contro i nuovi), le 20 posizioni nuove con zona e distanza da Piazza Castello, quante fermate importanti e quanti punti
cadono in Q002-Q009 (**devono essere 0**: se no, è un errore, correggilo) e quanti in quartieri periferici di Torino /
cintura / resto della Città metropolitana.

## FASE 4 — Risultato 6: mappa e scheda

**4.1 Dati per la mappa** (`79_dati_mappa_r6.py`): come oggi, più: `validazione` (passo 3.8), per le fermate `c4`
arrotondato e la strada, per i punti `auto_passaggio`, per le aree la categoria «Pochi dati». **Togli** dai dati
pubblici i punteggi grezzi (es. «618,9»): resta la posizione in classifica.

**4.2 Mappa** (`mappa_template.html`, `04_genera_mappa.py`): le tre viste restano. Aggiorna le legende con i valori
veri letti dai dati (400 m a piedi, ≥ 5 fermate per colorare un'area, grigio = «Pochi dati», parcheggi = solo adatti
all'interscambio). Nel clic della fermata e del punto: «auto in entrata che passano qui al mattino: circa N
[STIMATO, ordine di grandezza]». Nel clic di un interscambio ufficiale: la riga di validazione (solo fatti misurati).
Guida (`#infoDati`): riscrivi il paragrafo del Risultato 6 in 5-6 frasi con i criteri nuovi.

**4.3 Scheda** (`schede_risultati.py`, funzione `scheda_r6`; `simulazione.html` solo se serve una sezione nuova):
- **In testa** la scoperta misurata: «Gli interscambi che ci sono: solo Stura si riempie di giorno…» (con i numeri del
  file), e i profili a 24 ore dei 4 interscambi del Comune (grafico preferito di Leo).
- Poi la domanda «Dove mancano posti per lasciare l'auto prima di entrare in città?», il numero chiave (fermate
  importanti senza 50 posti adatti a 400 m a piedi, su quante), le aree, i 20 punti con le auto che passano.
- Sezione «Il metodo funziona?» con la tabella di validazione (3.8).
- Tabella dei criteri e «Quanto sono affidabili i dati» aggiornate (tutti i valori di sezione 1 con le sensibilità).
- **Togli**: il grafico «parcheggi già pieni di giorno» con i garage del centro (non sono interscambi); al massimo 8
  grafici in tutto.
- Limiti: aggiungi «auto in entrata dal modello del traffico (stima debole, solo ordine di grandezza)», «distanza a
  piedi stimata (linea d'aria × 1,3)», «treni non considerati».

**4.4 Prova**: `RISULTATO6_RIFAI.bat` completo → `prova_pagine_r6.py` **0 errori**; nella scheda R6 e nel tema della
mappa non devono comparire: «utile», «osservazion», «versione», «scenario», «S2», «S4», «nodo forte», «fonte_stato»,
punteggi con decimali.

## FASE 5 — Altri risultati: testi che ingannano (nessun ricalcolo)

**5.1 Risultato 2** (`schede_risultati.py`, parte R2): togli dai testi pubblici numeri come «servizi raggiungibili in
più in città» sommati su tutte le sezioni (es. 51.935.040). Se `risultato2_metro_notte.json` ha, per sezione, sia il
valore prima sia quello dopo, aggiungi un secondo numero: «residenti con almeno il 25% di servizi raggiungibili in più
di notte» (soglia dichiarata, `--soglia-r2 0.25`); se non li ha, scrivi nell'esito «non calcolabile» e lascia solo la
frase che il miglioramento conta anche se piccolo (c'è già).
**5.2 Risultato 1**: nei testi pubblici il gruppo «cibo» diventa «negozi e attività commerciali» (usa tutte le 31.405
attività del catalogo); nei file e nel codice il nome interno resta.
**5.3** Rilancia `schede_risultati.py` e la prova delle pagine.

## FASE 6 — Portfolio (pronto, **non** pubblicato)

**6.1 Mappa più leggera** (`04_genera_mappa.py`), solo se le fasi 1-4 sono OK. Oggi 22 MB su 23,6 sono le sezioni.
Prova, una alla volta, misurando il peso dopo ognuna: coordinate dei contorni a 5 decimali; numeri dell'accessibilità
senza decimali inutili (interi dove sono conteggi). Obiettivo: almeno −30%. Controllo: per 50 sezioni a caso i valori
mostrati (arrotondati come in pagina) sono identici a prima; prova delle pagine 0 errori. Se un passo cambia un valore
mostrato, annullalo.

**6.2 Cartella da pubblicare** (`83_prepara_pubblicazione.py` → `pubblica/`, da aggiungere a `.gitignore`): copia
`mappa_torino.html`, `simulazione.html`, i file che le pagine caricano (`data/stat.js`, `data/processed/orari_fermate.js`,
`data/schede_risultati.js`, `immagini/` se esiste; trova l'elenco completo cercando `src=` nelle pagine) con gli stessi
percorsi relativi, e `README.md`. Poi `prova_pagine_r6.py --cartella pubblica` → 0 errori. Scrivi il peso totale.

**6.3 `README.md` nella radice**, in due lingue (prima italiano, poi **English**), per chi non conosce il progetto:
cos'è; le domande; **un paragrafo per ogni risultato finito con il numero principale letto da `data/schede_risultati.js`**
(nessun numero scritto a mano); come aprire mappa e schede; fonti con licenze (GTFS GTT, 5T, ISTAT, IMQ 2022, OSM ©
contributori, OMI) e «sfondi della mappa: condizioni d'uso da verificare prima di pubblicare»; limiti generali (orario
programmato, raccolta dal 3/10/2026); come rifare i calcoli (`requirements.txt`, i `.bat`).

**6.4 Riassunto in inglese nelle schede**: in `schede_risultati.py` aggiungi a ogni scheda il campo `in_english` (3-4
frasi: domanda, risposta con i numeri del file, un limite); in `simulazione.html` mostralo in fondo alla scheda in un
blocco «In English» chiuso (`<details>`). Numeri all'inglese (punto decimale, virgola delle migliaia).

## FASE 7 — Verifiche indipendenti ed esito

**7.1** In `76_verifiche_r6v2.py` aggiungi e lancia:
1. `M_cint`, `M_tor` e `c2` (conducenti) ricalcolati con pandas → uguali;
2. `c4` di 8 luoghi a caso (seme 20261020) ricalcolato a mano dal file dei flussi → uguale;
3. classe di 8 fermate importanti rifatta a mano (parcheggi adatti, 400 m a piedi) → uguale;
4. per 5 parcheggi a caso (seme 20261020) `adatto` e motivo rifatti a mano → uguali;
5. nessuna fermata importante, nessun punto e nessun parcheggio mostrato in Q001-Q009;
6. `git status`: elenca file modificati, nuovi, spostati; nessun commit.

**7.2 Esito** (`docs/ESITO_CORREZIONI_GENERALI.md`): righe di stato di ogni passo; tabella prima/dopo; decisione sui
torinesi con i numeri; validazione degli interscambi; sensibilità; file modificati, nuovi, spostati; anomalie; tempi.

**7.3 Proposta per la memoria**: in fondo all'esito, il testo **pronto da incollare** per `MEMORIA_PROGETTO.md` (riga
del Risultato 6 in sezione 4; sezioni 5-6; script e prossimo numero libero in sezione 3). **Non** modificare la memoria:
lo fa Claude con Leo dopo aver ricontrollato.

---

## Cosa NON fare

- Non cambiare: la soglia dei 50 posti, i 25 m² a posto, il 10% delle fermate, le regole di Leo della regola 0.10.
- Non usare le osservazioni di Leo nei dati, nei testi pubblici o nelle scelte.
- Non aggiungere treni SFM, bici, taxi, eventi (fuori da questo piano). Lo script 78 (eventi) non si rilancia.
- Non modificare `42_instradamento.py`, `rete_osm.py`, gli script del traffico 33-67, `data/raw`, il database, il Pi.
- Non cancellare file (solo spostare in `archivio/`). Non pubblicare niente. Nessun commit.
- Non scrivere numeri a mano in template, schede o README: sempre letti dai file.

## Per Leo: come lanciarlo

1. Porta questo piano sul ramo `prova` del PC (vedi il messaggio di Claude).
2. Apri una chat nuova con l'agente nella cartella del progetto e incolla:

> Leggi `AGENTS.md`, `MEMORIA_PROGETTO.md`, `docs/ANALISI_PROGETTO.md`, `docs/ANALISI_RISULTATO6.md` e poi esegui
> `docs/PIANO_CORREZIONI_GENERALI.md` dall'inizio alla fine, nell'ordine, senza fermarti a chiedere, seguendo le sue
> regole. Scrivi tutto in `docs/ESITO_CORREZIONI_GENERALI.md`. Nessun commit.

3. Alla fine: Claude ricontrolla l'esito e le pagine nel browser, aggiorna la memoria e, se Leo vuole, fa il commit.
