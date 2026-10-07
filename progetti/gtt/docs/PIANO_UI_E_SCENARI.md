# Piano di riordino interfaccia e architettura scenari

## In breve
La mappa attuale offre un patrimonio informativo ricco ma soffre di dispersione visiva tra nove temi eterogenei, troppi selettori e schede informative disomogenee.
Il piano condensa l'interfaccia in quattro temi funzionali e introduce un modello standard per tutte le schede al clic.
I dati di traffico (sensori 5T e velocità dei mezzi pubblici) vengono uniti in una sola vista coerente, mantenendo la distinzione tra misurato e programmato.
Viene impostata l'architettura per scenari alternativi tramite file di varianti leggeri, senza duplicare né alterare i dati ufficiali di partenza.
Il lavoro è suddiviso in cinque interventi autonomi e progressivi, capaci di valutare fin da subito la popolazione servita e la variazione delle frequenze.

## UI oggi
### Livelli e sovrapposizioni (8 voci)
- Linee GTT: tracciati vettoriali con spessore proporzionale alle corse/ora o colorati per rapporto mezzi reali/programmati.
- Fermate GTT: cerchietti azzurri visibili da zoom 14 con dimensione proporzionale ai passaggi orari.
- Corse simulate: puntini animati che scorrono lungo i tracciati a velocità costante stimata dagli orari.
- Mezzi reali GTT: posizioni GPS dei veicoli all'ultimo aggiornamento (senza legame alla singola corsa programmata).
- Sensori di traffico 5T: cerchi colorati per velocità media negli ultimi 5 minuti con indicatore di scostamento dal valore tipico.
- Replay storico: riproduzione temporale delle posizioni registrate in una giornata passata.
- Griglia metrica: reticolo di riferimento a terra con passo variabile (da 10 metri a 10 chilometri) e barra di scala.
- Aree territoriali: poligoni delle sezioni di censimento ISTAT 2021 o delle zone statistiche comunali (gestiti dal tema attivo).

### Temi attuali nel menu a tendina (9 voci)
- Nessuno: visualizza solo la mappa di sfondo senza colorazioni di zona o sovrapposizioni automatiche.
- Offerta: colora le sezioni di censimento in base ai passaggi/ora entro 400 metri programmati da orario.
- Domanda: colora le sezioni di censimento per densità di residenti (abitanti per km² da censimento 2021).
- Poca offerta per abitante: colora le sezioni evidenziando in rosso il basso rapporto tra passaggi orari e residenti.
- Zone statistiche: colora le 94 zone comunali storiche per passaggi/ora per km² (dati geometrici del 2011).
- Traffico: evidenzia i sensori 5T ingranditi e apre il riquadro delle segnalazioni di rallentamento.
- Tempo reale: attiva contemporaneamente le posizioni reali dei mezzi e le corse simulate da orario.
- Velocità: colora le linee del trasporto pubblico in base alla velocità commerciale misurata dai dati GPS storici.
- Pendolari: colora i comuni della cintura per flusso verso Torino e traccia le 30 linee di scambio principali.

### Controlli utente nel pannello e sulla mappa (16 voci)
- Pulsante di chiusura/apertura laterale: icona "-" per comprimere il pannello e pulsante galleggiante per riaprirlo.
- Selettore giorno tipico: tre pulsanti a segmenti per alternare feriale, sabato e domenica.
- Pulsante "Adesso": sincronizza automaticamente giorno e orario con l'orologio reale di sistema.
- Cursore orario e riproduzione: cursore da 0 a 24 ore, orologio numerico e pulsante play/pausa per l'avanzamento automatico.
- Selettore velocità animazione: menu con opzioni 1x, 10x, 60x e 240x.
- Sintesi temporale: riga descrittiva del contesto visualizzato e contatore dei veicoli teoricamente in movimento.
- Menu selezione tema: tendina principale con i 9 temi e testo esplicativo dinamico.
- Filtri pendolarismo: tre tendine aggiuntive (motivo lavoro/studio, direzione entrata/uscita, valore assoluto o relativo).
- Caselle sovrapposizioni: sei caselle per accendere o spegnere manualmente linee, fermate, corse, mezzi, sensori e replay.
- Selettore giornata replay: tendina con l'elenco delle date registrate disponibili nello storico.
- Selettore mappa base: tendina tra satellite Esri, mappa chiara Esri, stradale Esri o nessuno sfondo.
- Cursore intensità sfondo: regolazione trasparenza dal 0% al 100% per migliorare la leggibilità dei dati.
- Casella griglia metrica: interruttore per mostrare o nascondere le linee di coordinate e misura.
- Filtro per linea: casella di testo con completamento automatico per isolare un singolo percorso.
- Criterio colore linee: scelta tra spessore per corse programmate oppure colore per efficienza del servizio reale.
- Riquadro segnalazioni critiche: elenco dinamico dei sensori più lenti del solito e delle linee con minor numero di mezzi.

### Schede al clic e finestre informative (6 voci)
- Scheda fermata: nome, codice, elenco linee servite, passaggi nell'ora, passaggi giornalieri e prossimi transiti programmati.
- Scheda linea: nome linea, percorso esteso, velocità commerciale media nell'ora, numero di campioni e ore con rilevazioni.
- Scheda sensore 5T: toponimo, direzione di marcia, codice sensore, flusso veicolare, velocità media e confronto con lo storico.
- Scheda mezzo in tempo reale: numero di linea, capolinea, identificativo veicolo e orario dell'ultima localizzazione registrata.
- Scheda sezione censuaria: numero residenti, densità abitativa, offerta entro 400 metri, rapporto offerta/abitanti e dati comunali.
- Scheda zona statistica: denominazione, codice circoscrizionale, numero di fermate interne, estensione e densità passaggi.

## UI proposta
### Cosa eliminare e cosa accorpare
- Eliminare il tema "Zone statistiche 2011": era un surrogato temporaneo; oggi le sezioni di censimento 2021 forniscono un dettaglio territoriale molto più accurato e aggiornato.
- Accorpare "Offerta", "Domanda" e "Poca offerta per abitante" in un unico tema organico ("Servizio e abitanti"): una semplice scelta interna permette di guardare la copertura, i soli residenti o il loro rapporto.
- Accorpare "Traffico" (sensori 5T) e "Velocità" (mezzi pubblici) nel tema unificato "Traffico e velocità": la circolazione privata e il trasporto pubblico si influenzano a vicenda e vanno letti nello stesso quadro.
- Riorganizzare i controlli temporali: raggruppare i comandi dell'orologio in un unico blocco ergonomico ed eliminare i selettori ridondanti sul colore delle linee, assorbendoli nel tema specifico.

### I 4 temi proposti (massimo 4)
1. **Servizio e abitanti (Offerta e domanda):** analizza dove vivono le persone e quanto trasporto pubblico hanno vicino a casa (entro 400 metri). Un selettore interno consente di mostrare: "Indice di servizio" (rosso per chi ha pochi passaggi), "Solo offerta" o "Solo residenti".
2. **Traffico e velocità:** fotografa lo scorrimento della viabilità torinese. Mette a confronto diretto le velocità registrate dai sensori stradali 5T con la velocità commerciale delle linee GTT calcolata dai tracciati GPS reali.
3. **Tempo reale e flotta:** mostra i veicoli effettivamente monitorati sulle strade insieme all'avanzamento programmato, evidenziando subito linee con carenza di corse o rallentamenti improvvisi.
4. **Pendolarismo intercomunale:** visualizza le relazioni di viaggio quotidiane (lavoro e studio) tra Torino e i comuni dell'area metropolitana basate sui dati censuari ISTAT.

### Struttura unica per tutte le schede informative al clic
Tutte le schede informative condivideranno lo stesso schema fisso a quattro sezioni, evitando testi sparsi e disorientanti:
1. **Intestazione:** Nome dell'elemento (es. "Fermata Vittorio Emanuele", "Linea 4", "Sensore Corso Francia") e distintivo chiaro sull'origine del dato (`[MISURATO]`, `[PROGRAMMATO]`, `[CENSIMENTO]`).
2. **Dato principale in evidenza:** Il valore più significativo mostrato a caratteri grandi con il suo stato (es. "18 passaggi/ora - Servizio frequente", "11.2 km/h - Più lento del solito").
3. **Metriche di dettaglio:** Massimo 3 o 4 righe pulite con valori quantitativi (es. linee attive, residenti serviti, veicoli/ora).
4. **Approfondimento a richiesta:** Sezione espandibile o tabella ordinata (es. prossimi arrivi da orario per le fermate, storico orario per le linee).

### Schema visivo testuale della scheda unica
```text
+-------------------------------------------------------------+
| [ICONA] NOME ELEMENTO                   [BOLLINO FONTE DATO]|
| Sottotitolo descrittivo o codice identificativo             |
+-------------------------------------------------------------+
| VALORE PRINCIPALE (es. 14 passaggi/ora oppure 12 km/h)      |
| Stato sintetico: [Normale / Rallentato / Servizio scarso]   |
+-------------------------------------------------------------+
| DETTAGLI:                                                   |
| • Parametro A: Valore con unità di misura                   |
| • Parametro B: Valore con unità di misura                   |
| • Confronto:   Rispetto alla media o alla fascia oraria     |
+-------------------------------------------------------------+
| [SEZIONE APPROFONDIMENTO]                                   |
| Tabella orari prossimi / storico campioni / elenco linee    |
+-------------------------------------------------------------+
```

## Dati di traffico
### Dati già raccolti nel progetto
- **Sensori 5T (112 postazioni):** il raccoglitore salva ogni 5 minuti flusso di veicoli, velocità media rilevata, livello di accuratezza e toponimo stradale.
- **Posizioni dei mezzi GTT (GTFS-RT):** localizzazione ogni 60 secondi di ciascun veicolo circolante con coordinate GPS, identificativo vettura e linea assegnata.
- **Velocità commerciale calcolata:** stima chilometrica tra punti GPS consecutivi per determinare la velocità media per linea, giorno tipico e ora (includendo soste e semafori).
- **Profilo storico "di solito":** aggregazione statistica nello storico locale SQLite per stabilire le medie orarie tipiche di ciascun sensore e ciascuna linea.

### Cosa è affidabile e cosa non lo è
- **Affidabile:** le posizioni GPS valide dei mezzi GTT; i sensori 5T con accuratezza diversa da zero (circa 30-40 sensori urbani pienamente attivi); la velocità commerciale media calcolata su linee con più di 20 campioni registrati.
- **Non affidabile o lacunoso:** i sensori 5T con accuratezza pari a 0 e flusso 0 (non si distingue con certezza tra guasto e assenza di traffico); i ritardi delle singole corse (il feed GTT non fornisce il codice della corsa programmata `trip_id`, impedendo il legame diretto veicolo-orario); le serie storiche con meno di 72 ore di dati registrati.

### Come presentare il traffico senza confondere misurato e stimato
- **Identificazione visiva netta:** utilizzare linee piene e marcatori solidi per i dati `[MISURATO]` (sensori 5T attivi, velocità commerciale reale dei bus, veicoli GPS); utilizzare contorni tratteggiati o semitrasparenti per le stime `[PROGRAMMATO]` o `[STIMATO]` (posizioni teoriche delle corse da orario).
- **Trattamento dei sensori muti:** i sensori con accuratezza zero non devono apparire come "strada libera", ma in grigio chiaro con bordo a trattini e dicitura esplicita "Dato non disponibile".
- **Etichette sempre visibili:** ogni scheda o voce di legenda deve mostrare il bollino standardizzato (`[MISURATO]`, `[PROGRAMMATO]`, `[STIMATO]`, `[DATI SCARSI]`), evitando che l'utente scambi un orario teorico per un transito certo.

## Base per gli scenari
### Rappresentazione di uno scenario senza toccare i dati reali
- I dati ufficiali in `data/raw/` e il database di raccolta `data/storico.sqlite` restano rigorosamente protetti e invariati in sola lettura.
- Uno scenario viene definito come un file leggero di varianti in formato leggibile (JSON o dizionario Python) memorizzato nella cartella `data/scenari/<nome_scenario>.json`.
- Il file di scenario descrive solo i cambiamenti rispetto alla rete base:
  - Linee modificate: frequenza aumentata o ridotta (es. corse ogni 6 minuti invece di 10), variazione del percorso o estensione di capolinea.
  - Linee nuove: sequenza di fermate servite e numero di corse per ora.
  - Linee soppresse o deviate temporaneamente.

### Calcolo e confronto degli indicatori (Base vs Scenario)
- Il motore calcola la situazione di partenza ("Baseline") leggendo il GTFS ufficiale.
- Applicando le modifiche dello scenario, genera una tabella parallela di passaggi orari alle fermate e nelle sezioni territoriali.
- Il confronto produce mappe differenziali:
  - **Verde:** aumento di passaggi o riduzione dei tempi di attesa.
  - **Rosso:** calo di passaggi o peggioramento del servizio.
  - **Grigio neutro:** nessuna variazione.

### Indicatori semplici calcolabili subito con i dati disponibili
1. **Passaggi orari per sezione e per fermata:** variazione netta del numero di corse nell'ora di punta (es. +4 passaggi/ora su una direttrice).
2. **Tempo medio teorico di attesa (Headway / 2):** stima dell'intervallo tra due passaggi consecutivi (es. attesa media ridotta da 12 a 6 minuti).
3. **Popolazione servita da servizio frequente:** residenti ISTAT entro 400 metri da fermate che raggiungono almeno una soglia minima di corse (es. almeno 6 o 10 passaggi/ora).
4. **Volume chilometrico stimato:** stima chilometri-vettura per valutare l'impegno di mezzi aggiuntivi richiesti dalla modifica.

### Cosa manca per valutazioni più avanzate
- **Matrice Origine-Destinazione oraria per sezione:** disponiamo solo dei flussi comunali aggregati 2021 e dei residenti notturni; non conosciamo gli spostamenti precisi isolato per isolato nelle diverse ore della giornata.
- **Affollamento reale a bordo:** mancano i dati dei tornelli o dei sensori passeggeri a bordo bus; non è possibile determinare se un mezzo viaggia vuoto o saturo.
- **Motore di calcolo percorsi con trasbordo:** manca un algoritmo di itinerario pedonale integrato con cambi linea per stimare il tempo porta a porta degli utenti.

## Ordine di lavoro
Il piano è articolato in passi piccoli e autosufficienti, ciascuno realizzabile come compito autonomo:

1. **GT16 - Semplificazione temi e pannello principale:**
   - Riduzione del menu da 9 a 4 temi in `scripts/mappa_template.html`.
   - Rimozione delle opzioni superflue e riorganizzazione del blocco temporale ("Quando").
   - File coinvolti: `scripts/mappa_template.html`.

2. **GT17 - Uniformazione delle schede al clic:**
   - Ristrutturazione di tutte le schede (fermata, linea, sensore, sezione) secondo il modello fisso a 4 sezioni.
   - Uniformazione di caratteri, contrasti e distintivi di origine dato.
   - File coinvolti: `scripts/mappa_template.html`.

3. **GT18 - Integrazione unificata traffico e velocità:**
   - Fusione visiva dei sensori 5T e delle velocità commerciali delle linee nel tema unico "Traffico e velocità".
   - Aggiornamento della legenda e del riquadro segnalazioni critiche.
   - File coinvolti: `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`.

4. **GT19 - Motore base per scenari alternativi:**
   - Creazione dello script standalone `scripts/07_elabora_scenario.py` che legge il GTFS e applica un file di scenario in `data/scenari/`.
   - Calcolo del delta passaggi orari per fermata e variazione dei residenti serviti entro 400 metri.
   - Creazione di uno scenario dimostrativo (es. incremento corse linea 4 o prolungamento linea 15).
   - File coinvolti: `scripts/07_elabora_scenario.py`, `data/scenari/scenario_esempio.json`.

5. **GT20 - Visualizzazione e confronto scenari a schermo:**
   - Aggiunta nel pannello della funzione di caricamento scenario e visualizzazione differenziale (aree e linee verde/rosso).
   - Scheda riepilogativa con il guadagno di residenti coperti e variazione corse.
   - File coinvolti: `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`.

## Rischi e limiti
- **Prestazioni del browser locale:** l'aggiunta di scenari alternativi non deve raddoppiare in memoria le migliaia di punti e coordinate geografiche; la variante deve contenere solo le differenze rispetto alla base.
- **Complessità nella stesura degli scenari:** Leo non è un programmatore e non deve compilare file GTFS completi; il sistema deve accettare istruzioni intuitive (es. "linea: 15, intervallo: 8 minuti, nuova_fermata: nome_o_coord").
- **Assenza di domanda passeggeri puntuale:** non potendo prevedere quanti passeggeri reali saliranno a bordo, le valutazioni dello scenario devono dichiarare onestamente di misurare l'"Offerta potenziale di servizio" e i "Residenti raggiunti", mai i passeggeri trasportati effettivi.
- **Equivoco tra orario teorico e regolarità:** migliorare un orario sulla carta non garantisce che i bus non restino bloccati nel traffico; i risultati degli scenari devono sempre riportare l'avviso che si tratta di simulazioni basate su orari programmati.
