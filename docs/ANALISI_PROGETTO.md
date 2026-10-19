# Analisi completa del progetto GTT — criticità, cosa manca, cosa è di troppo

Scritta da Claude il 19/10/2026 su richiesta di Leo. L'analisi del Risultato 6 (parcheggi) è in un documento a
parte: `docs/ANALISI_RISULTATO6.md`.

## Come ho lavorato (e cosa non ho potuto fare)

- Ho letto la memoria, i piani, gli esiti e i rapporti in `docs/`, il codice degli script e i dati che stanno
  **dentro** `mappa_torino.html` (lì ci sono, per esempio, le 378 fermate e i 212 parcheggi del Risultato 6).
- **Non avevo `data/`** (non è in git): non ho potuto rilanciare gli script né rileggere il database. Quando
  scrivo un numero, viene dai rapporti, dal codice o dai dati della mappa, e l'ho ricontato dove potevo.
- Ramo: lavoro su `claude/sweet-lovelace-hmqh81`, che all'inizio era identico a `prova` (stesso commit
  `83c577c`). Non ho toccato `prova`.

## In breve (le 7 cose più importanti)

1. **Tanto lavoro in poco tempo, poca profondità.** In 12 giorni (8-20/10) sono nati 9 risultati, 6 schede, 105
   script e 80 documenti. Molti risultati sono «versione 1» con un titolo debole o ovvio. Manca un filo che li
   tenga insieme.
2. **Il modo di lavorare (piano → agente → esito → correzione) produce molta carta e molti cambi di rotta.**
   Il Risultato 6 da solo ha 44 file e cambia domanda 6 volte in 5 giorni (dettagli nell'altra analisi).
3. **Pochi controlli con la realtà.** Quasi tutti i controlli verificano che il codice dia i numeri attesi
   (riproducibilità), quasi mai che il risultato sia vero (confronto con fatti noti).
4. **Indici fatti mescolando percentuali** con pesi non dichiarati e valori di zona dati a ogni fermata: il
   risultato dipende molto dalle scelte (R6 è il caso più evidente).
5. **Il repository da solo non funziona**: la mappa e le schede leggono file che non sono in git
   (`data/stat.js`, `data/processed/orari_fermate.js`, `data/schede_risultati.js`). Un visitatore del portfolio
   vedrebbe pagine rotte.
6. **Non c'è un modo unico per rifare tutto**: l'ordine degli script sta scritto nella memoria a parole
   (es. «71→72→73→75→76→80→79»), e alcuni script si fermano se i numeri non sono quelli di oggi.
7. **Per un portfolio mancano le cose di base**: una pagina di presentazione (README), una mappa leggera
   (oggi 23,6 MB), le condizioni d'uso degli sfondi, forse una versione in inglese.

---

## 1. Criticità

### 1.1 Obiettivo e focus

- **La direzione del 9/10** è chiara («capire come funziona la città» + pochi scenari). Nei fatti il lavoro si è
  allargato: traffico (R8, ~35 script), rapporto di sostenibilità GTT (980 fatti), eventi, costi, taxi,
  logistica. Ogni idea nuova diventa un piano; poche arrivano in fondo con un risultato forte.
- **I titoli dei risultati sono deboli o ovvi**, perché la metrica scelta li rende tali:
  - R2: «773.307 residenti con accesso migliore» = il 91% di Torino, perché conta **qualsiasi** miglioramento,
    anche di un solo servizio. Il rapporto riporta anche «51.935.040 servizi raggiungibili in più», un numero che
    non dice niente a chi legge.
  - R8: «95,3% dei km di strade grandi serviti dal TP»: dice che quasi tutto è coperto; la notizia vera (Corso
    Regina Margherita ovest) è una riga, con una stima di traffico debole (±38%).
  - R1: «1,3% senza servizi essenziali», ma il gruppo «cibo» usa tutte le 31.405 attività commerciali, non solo
    i negozi di alimentari: il numero è ottimista per costruzione.
  - R6: «206 fermate su 378 senza 50 posti a 200 m»: dipende quasi tutto dai parametri (vedi l'altra analisi).
- **Manca la storia che unisce i risultati.** Un portfolio regge meglio con 2-3 risultati forti e collegati
  (per esempio: «chi resta indietro» = accessibilità + vulnerabilità + attesa reale) che con 9 schede.

### 1.2 Modo di lavorare

- **Molti cambi di rotta in poco tempo.** Esempio R6 (19/10, un giorno solo): scenario S2 → porte = zone IMQ →
  direzioni d'ingresso → zone colorate → esagoni + 20 punti → correzioni. Ogni giro lascia piani, esiti,
  rapporti, campi nei JSON e funzioni nel codice.
- **I piani scrivono i numeri attesi prima del calcolo** («atteso 378», «147/59/172», «il Palavela deve
  comparire»). È utile per trovare errori, ma ha due effetti collaterali:
  - spinge a far tornare i conti (il Palavela era fuori «per un soffio» a 200 m → la regola dei parcheggi
    mostrati è cambiata e ora c'è un controllo che pretende il Palavela);
  - i numeri restano scritti nel codice: `79_dati_mappa_r6.py` si **ferma** se le fermate non sono esattamente
    378 / 147 / 59 / 172. Con il prossimo GTFS (quello di oggi vale fino al 31/01/2027) o un OSM nuovo, la
    catena si blocca anche se il calcolo è giusto.
- **Gli agenti non vedono le pagine.** La verifica nel browser è sempre mancata o è stata parziale (il giro R6
  ha lasciato una funzione non definita); `prova_pagine_r6.py` aiuta, ma funziona solo con Edge su Windows e
  non clicca.
- **Decisioni prese molto in fretta**, a volte «per fiducia in Claude» (es. zona centrale Q001-Q009). Va bene
  per le piccole scelte, meno per quelle che cambiano il risultato.

### 1.3 Metodo (problemi che tornano in più risultati)

- **Indici composti da percentili** (R6, in parte R1/R8): si mettono insieme cose diverse trasformandole in
  posizioni in classifica. Così si perde la grandezza (essere primi di poco o di tanto vale uguale), i pesi
  diventano impliciti e due versioni dello stesso segnale contano doppio.
- **Valori di zona dati a ogni punto**: le zone IMQ sono 101 e molto diverse (Moncalieri è una zona sola, un
  quartiere di Torino è molto più piccolo). Tutte le fermate di una zona prendono lo stesso valore: le zone
  grandi pesano di più per costruzione.
- **Soglie scelte a mano e risultati molto sensibili** (200 m, 50 posti, 10%, 60/30%): le sensibilità sono
  dichiarate (bene), ma il numero principale cambia del doppio o della metà.
- **Poca validazione esterna.** Il progetto ha già dei «fatti veri» che non usa per controllare i risultati:
  - il rapporto di sostenibilità GTT 2025 (passeggeri per modo, km, 30 parcheggi gestiti, park & ride);
  - le misure dei parcheggi 5T (Stura pieno, Caio Mario vuoto) per il Risultato 6;
  - la conoscenza della città di Leo (già usata per R8: 10 strade su 18 nella fascia giusta).
- **Orario programmato**: accessibilità e scenari sono ottimisti per definizione (dichiarato). Ora che c'è la
  raccolta dei ritardi, la cosa più originale del progetto sarebbe confrontare promesso e reale (R9 lo fa).

### 1.4 Dati

- **Serie brevi**: mezzi dal 3/10, ritardi dal 10/10, parcheggi dal 14/10. Il Risultato 6 usa **2 giorni
  feriali** (15-16/10) di riempimento. Serve tempo, non codice.
- **Raccolta fragile**: il 18/10 è fallito il backup notturno e il feed GTT si è fermato alle ~09:05. Non c'è un
  avviso automatico quando la raccolta si ferma (ce ne si accorge al fetch della domenica).
- **Buchi noti e importanti**: treni SFM (il GTFS GTT non li ha; per il Risultato 6 sono la parte principale:
  il 63% di chi oggi passa dall'auto al mezzo pubblico prende il treno), bus extraurbani di altre aziende,
  passeggeri per linea, bici. Il feed ritardi copre ~90 linee urbane e ~80% delle corse.
- **Date di riferimento della mappa** (`date_riferimento` in `04_genera_mappa.py`): sono «il prossimo martedì,
  sabato e domenica» rispetto al giorno in cui si rigenera. Oggi la domenica scelta è il **25/10**, giorno del
  cambio dell'ora; in futuro può cadere su un festivo (1/11, 8/12). Meglio fissare date «tipiche» a mano.

### 1.5 Tecnica e ordine dei file

- **Nessuna catena unica**: non c'è uno script «rifai tutto» né l'elenco delle librerie (`requirements.txt`).
  L'ordine giusto vive nella memoria e nei piani.
- **Codice copiato**: la distanza haversine è definita in 12 script, `trova_radice` in 46, l'ora legale in 8.
  Una correzione va fatta in tanti posti.
- **Script e passi superati che girano ancora**: il `.bat` settimanale del traffico rilancia le fasi 3-4
  (37, 43-45, 50b, 53-54), già superate dalla Fase 5.
- **File generati in git**: `mappa_torino.html` (23,6 MB) è stato salvato 10 volte; i `RAPPORTO_*.txt` che gli
  script riscrivono a ogni giro fanno rumore nella storia.
- **`data/processed/vulnerabilita.json` e `vulnerabilita_mappa.json` sono in git** anche se `data/` è escluso
  (aggiunti prima della regola). Non sono dati personali, ma è un'eccezione da decidere.
- **Le pagine dipendono da file fuori da git** (sopra, punto 5 del riassunto): chi scarica il repository non
  vede la storia dei sensori né le schede.

### 1.6 Presentazione (portfolio)

- **Mappa da 23,6 MB**: 22 MB sono le 8.317 sezioni con l'accessibilità per 24 ore. Su un telefono è lenta.
  Si può dividere (un file per tema, caricato quando serve) o ridurre (meno decimali, meno ore).
- **Sfondi Esri**: le condizioni d'uso sono ancora da chiarire prima di pubblicare (già in memoria).
- **Nessuna pagina di ingresso** per chi arriva da fuori: `AGENTS.md` e la memoria sono note di lavoro.
- **Scheda R6 troppo piena** (13 grafici, 6 profili, 9 criteri): per un visitatore è difficile capire la risposta.
- Tutto in italiano: va bene se il pubblico è italiano; se il portfolio serve anche fuori, basta un riassunto in
  inglese per scheda.

---

## 2. Cosa manca (in ordine di importanza)

1. **Una domanda guida e 2-3 risultati «di punta»**, scelti tra quelli già fatti, con una frase forte e
   verificata ciascuno.
2. **Un controllo con la realtà per ogni risultato** (una riga «come sappiamo che è vero?»), con i dati che ci
   sono già: rapporto GTT 2025, parcheggi 5T, conoscenza di Leo, sensori 5T.
3. **Un modo unico per rifare tutto**: un solo `.bat` (o script) per risultato che lancia gli script nell'ordine
   giusto, + `requirements.txt`. I controlli con i numeri di oggi diventano **avvisi**, non arresti.
4. **Un modulo comune** (es. `scripts/comuni.py`) con haversine, radice del progetto, ora legale, lettura GTFS.
5. **Pagine autosufficienti**: una versione «da pubblicare» di mappa e schede che contiene tutto ciò che serve
   (o una cartella `pubblica/` con i file necessari), più leggera, e un README.
6. **Treni (GTFS regionale Piemonte)**: servono al Risultato 6, all'accessibilità della cintura e al Risultato 5.
7. **Un avviso automatico se la raccolta su leopi si ferma** (es. un controllo giornaliero che scrive un file
   o manda un messaggio; da fare con un `.bat` per Leo, come da regole).
8. **La metrica trasversale «auto in meno»** (idea di Leo del 16/10): è l'unico numero che lega accessibilità,
   parcheggi e traffico. Oggi nessun risultato la calcola.

## 3. Cosa è di troppo

| Cosa | Perché | Proposta |
|---|---|---|
| Piani, esiti e rapporti superati (R6: 44 file, ~63% delle righe di `docs/`) | Ogni giro lascia un piano e un esito; i rapporti dei giri vecchi confondono | Tenere per ogni risultato **un piano** (stato attuale in testa, come già `PIANO_RISULTATO6.md`) e il rapporto finale; il resto in `docs/archivio/` |
| Script superati: `25` (R6 v1), `06_dati_live.py` e `supervisore.py` (raccolta su Windows, ora su leopi), `calcola_simulazione.py` + `scenario_esempio.json` (simulatore generico, escluso il 9/10), fasi 3-4 del traffico | Non servono al risultato attuale, ma si leggono e si mantengono | Spostarli in `scripts/archivio/` (nessuna cancellazione) |
| Parti del Risultato 6 che non entrano nel risultato finale: classi dei parcheggi «di fatto / solo sulla carta / potenziale» (72, seconda parte), eventi (78), direzioni d'ingresso | Lavoro fatto, ma oggi non cambia nessun numero mostrato | Decidere: o entrano (vedi l'altra analisi) o vanno in archivio |
| Tre modi di copiare dati da leopi (`sync_da_leopi.bat`, `backup_da_leopi.bat`, `FETCH_LEOPI_E_VELOCITA_5T.bat`) | Facile lanciare quello sbagliato | Tenerne uno |
| 7 `.bat` nella radice (rapporto di sostenibilità, R2) | La radice dovrebbe avere solo le pagine e le note | In `scripts/` |
| Dati «live» rimasti nella mappa (110 posizioni dei mezzi del 3/10, avvisi del 9/10) | La revisione del 18/10 ha tolto il «live» ma i dati sono ancora dentro | Toglierli da `D` se non servono |
| `mappa_torino.html` salvato in git a ogni giro | Fa crescere il repository di MB a ogni commit | Salvarlo solo quando si pubblica, o fuori da git |
| Numeri senza significato per il lettore (R2 «51.935.040 servizi in più», punteggi tipo «618,9» nei 20 punti) | Sembrano precisi ma non si capiscono | Sostituirli con grandezze leggibili (residenti, minuti, auto) |

## 4. Una proposta di ordine (da decidere con Leo, un passo alla volta)

1. **Fermarsi una settimana sulle cose nuove** e lasciare correre la raccolta (servono ≥ 5 feriali di parcheggi e
   più settimane di ritardi).
2. **Pulizia leggera**: archivio dei piani/esiti superati e degli script vecchi, un modulo comune, i controlli
   fissi trasformati in avvisi. Nessun numero cambia.
3. **Decidere il Risultato 6** (le due strade sono nell'altra analisi: correggerlo o rifarlo).
4. **Scegliere i 2-3 risultati di punta** e aggiungere a ognuno il controllo con la realtà.
5. **Versione da pubblicare**: README, mappa leggera, sfondi con licenza chiara, schede autosufficienti.

## 5. Domande per Leo

1. **Per chi è il portfolio?** (lavoro nei trasporti / analisi dati / pubblico generico; Italia o anche fuori?)
   Cambia quanto spazio dare al metodo e se serve l'inglese.
2. **Preferisci pochi risultati molto curati o tanti risultati «v1»?** Io consiglio i pochi.
3. **Posso proporti un piano di pulizia** (solo spostamenti in archivio e un modulo comune, nessun numero
   cambia)?
4. **La metrica «auto in meno»** è ancora un obiettivo? Se sì, la userei come filo comune di R6, R8 e degli
   scenari.
