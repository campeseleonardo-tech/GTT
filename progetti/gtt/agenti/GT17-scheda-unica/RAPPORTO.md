# Rapporto di lavoro GT17 - Scheda unica per tutte le schede al clic

## Cosa è stato fatto
- È stata introdotta in `scripts/mappa_template.html` la funzione generatrice unica `creaScheda(...)` che implementa la struttura standard a quattro sezioni definita in `docs/PIANO_UI_E_SCENARI.md`:
  1. **Intestazione:** titolo, sottotitolo o codice, e distintivo chiaro dell'origine del dato (`[MISURATO]`, `[PROGRAMMATO]`, `[CENSIMENTO]`).
  2. **Valore principale:** numero o indicatore chiave in evidenza a caratteri grandi, corredato da uno stato sintetico chiaro.
  3. **Metriche di dettaglio:** elenco pulito di 3-4 righe chiave con allineamento etichetta / valore.
  4. **Approfondimento espandibile:** blocco `<details>` con `<summary>` espandibile o già aperto (es. tabella dei prossimi arrivi da orario per le fermate), contenente spiegazioni metodologiche o orari analitici.
- Tutte le schede informative al clic del progetto sono state riscritte adottando questa struttura comune senza perdere alcuna informazione:
  - **Fermata GTT:** codice, passaggi/ora all'ora scelta, stato del servizio, linee servite, totale giornaliero, tipo giorno e approfondimento con i prossimi passaggi programmati per linea.
  - **Linea GTT:** identificativo linea, percorso, velocità commerciale misurata (o frequenza programmata), campioni GPS, ore con dati registrati e spiegazione della velocità commerciale.
  - **Sensore 5T:** toponimo, direzione di marcia, velocità media e flusso veicolare, confronto con il profilo storico orario e dettaglio su accuratezza e finestra temporale.
  - **Mezzo reale GTT:** matricola veicolo, linea e tipologia, indicatore "In servizio", orario esatto di localizzazione GPS e nota sull'assenza del codice corsa.
  - **Sezione di censimento:** indicatore chiave (rapporto offerta/residenti, offerta o densità abitativa), residenti, popolazione e fermate entro 400 metri, passaggi orari e note demografiche ISTAT 2021.
  - **Comune (tema Pendolarismo):** flusso pendolari (in entrata/uscita, lavoro/studio), residenti censiti, ripartizione lavoro vs studio, spostamenti interni e dettagli sulla sezione cliccata.
  - **Zona statistica:** denominazione, passaggi orari per km², numero fermate interne, superficie e densità.
- Il comportamento al passaggio del mouse (hover) è stato separato da quello al clic: al passaggio del mouse compare solo un tooltip conciso a 2 righe (o cursore puntatore per le aree poligonali), mentre al clic si apre la scheda analitica fissa a destra con possibilità di chiusura via pulsante `×`, tasto `Esc` o clic su spazio vuoto.

## Come provarlo
Apri `mappa_torino.html` con Chrome, Edge o Firefox e verifica i seguenti elementi:

1. **Scheda Fermata:**
   - Ingrandisci la mappa (zoom 14 o superiore) fino a visualizzare i cerchietti azzurri delle fermate.
   - Fai clic su una fermata (es. fermata in Piazza Castello o Porta Nuova).
   - **Cosa mostra la scheda:**
     - Intestazione con nome della fermata e bollino blu `[PROGRAMMATO]`.
     - Valore principale in grande: es. "28 passaggi/ora" con stato ("Servizio molto frequente").
     - Dettagli: elenco linee servite, passaggi nell'intera giornata, giorno visualizzato.
     - Approfondimento espandibile "Prossimi passaggi programmati": orari delle prossime corse per ciascuna linea.

2. **Scheda Linea GTT:**
   - Seleziona il tema "Traffico e velocità" (oppure attiva la casella "Linee: corse/ora").
   - Fai clic su uno dei tracciati delle linee (es. linea 4 o metro).
   - **Cosa mostra la scheda:**
     - Intestazione con "Linea X", tipologia (tram/bus/metro) e bollino verde `[MISURATO]` (o blu `[PROGRAMMATO]`).
     - Valore principale in grande: velocità commerciale (es. "15.4 km/h") con stato relativo.
     - Dettagli: tipologia mezzo, frequenza corse/ora programmata, campioni GPS registrati nello storico.
     - Approfondimento: note su percorso e metodo di calcolo della velocità commerciale.

3. **Scheda Sensore 5T:**
   - Nel tema "Traffico e velocità" (o con la casella "Sensori traffico 5T" accesa), fai clic su uno dei cerchi dei sensori stradali.
   - **Cosa mostra la scheda:**
     - Intestazione con nome della via e bollino verde `[MISURATO]`.
     - Valore principale in grande: velocità media (es. "38 km/h") o "Dato assente", con indicazione se il traffico è più lento del solito.
     - Dettagli: flusso in 5 minuti (veicoli/h equivalenti), direzione, velocità tipica a quest'ora e timestamp.
     - Approfondimento: codice sensore, accuratezza e base storica del confronto.

4. **Scheda Sezione di censimento:**
   - Nel tema "Servizio e abitanti", fai clic su un poligono territoriale colorato.
   - **Cosa mostra la scheda:**
     - Intestazione "Sezione di censimento" con codice comune e bollino viola `[CENSIMENTO]`.
     - Valore principale in grande: indice di servizio (es. "42 passaggi / 1000 ab.") con stato qualitativo.
     - Dettagli: residenti della sezione, abitanti e fermate entro 400 metri, passaggi orari programmati.
     - Approfondimento: dettagli territoriali e note sulla popolazione del censimento ISTAT 2021.

5. **Scheda Comune (Pendolarismo):**
   - Seleziona il tema "Pendolarismo" e fai clic su uno dei comuni della cintura torinese (es. Moncalieri, Collegno, Venaria).
   - **Cosa mostra la scheda:**
     - Intestazione con il nome del comune o codice ISTAT e bollino viola `[CENSIMENTO]`.
     - Valore principale in grande: numero totale di pendolari o tasso per 1000 abitanti con la direzione.
     - Dettagli: residenti censiti, persone che entrano a Torino (lavoro/studio), persone che escono da Torino.
     - Approfondimento: note sulla matrice ISTAT 2021 e dati della sezione specifica cliccata.

6. **Scheda Mezzo reale GTT:**
   - Nel tema "Tempo reale e flotta", fai clic su uno dei veicoli in circolazione (puntini con bordo bianco).
   - **Cosa mostra la scheda:**
     - Intestazione con matricola e linea, bollino verde `[MISURATO]`.
     - Valore principale: "In servizio" con orario di localizzazione.
     - Dettagli e approfondimento sul feed GTFS-RT.

## Scelte
- **Larghezza della scheda:** la larghezza massima della scheda `#scheda` è stata impostata a `min(320px, calc(100vw - 24px))` per accogliere comodamente le metriche a due colonne senza sacrificare la visualizzazione della mappa.
- **Approfondimenti:** la sezione espandibile sfrutta l'elemento standard `<details><summary>` per garantire interattività immediata senza logiche complesse aggiuntive; per le fermate la sezione orari è pre-aperta (`open`) se vi sono prossimi passaggi calcolabili.
