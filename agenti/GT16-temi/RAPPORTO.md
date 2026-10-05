# Rapporto GT16 - Semplificazione temi e blocco temporale

## Cosa è stato fatto
In conformità con il piano approvato in `docs/PIANO_UI_E_SCENARI.md` (passo GT16), ho modificato `scripts/mappa_template.html` per razionalizzare l'interfaccia principale:
1. **Riduzione dei temi da 9 a 4 temi funzionali**:
   - **Servizio e abitanti**: unifica le precedenti viste "Poca offerta per abitante", "Offerta" e "Domanda". Include un selettore interno (`#subServizio`) visibile solo quando il tema è attivo, con tre opzioni:
     - *Indice di servizio (poca offerta in rosso)* [impostazione di partenza]: colorazione del rapporto tra passaggi orari e residenti con linee GTT a metà spessore;
     - *Solo offerta (passaggi/ora entro 400 m)*: passaggi programmati alle fermate e linee piene;
     - *Solo residenti (abitanti per km²)*: densità di popolazione da censimento ISTAT 2021.
   - **Traffico e velocità**: unifica i sensori 5T (velocità media del traffico stradale, con marcatori ingranditi) e la velocità commerciale misurata delle linee GTT (colorazione delle linee da verde a rosso per km/h). Include il riquadro delle segnalazioni critiche ("Traffico più lento del solito" e "Linee con meno mezzi del previsto") e le legende combinate di traffico e velocità.
   - **Tempo reale e flotta**: posizioni GPS reali dei mezzi GTT affiancate alle corse simulate da orario per confrontare presenza reale e teorica, con riquadro segnalazioni attivo.
   - **Pendolarismo**: flussi comunali ISTAT 2021 tra la cintura e Torino con selettori dedicati (lavoro/studio, entrata/uscita, relativo/assoluto) e tracciamento delle prime 30 direttrici.
2. **Rimozione del tema "Zone statistiche 2011" dal menu**:
   - Le zone statistiche del 2011 non compaiono più nel menu a tendina. Il codice di calcolo e visualizzazione geometrica sottostante è stato preservato per garantire che nulla si rompa internamente.
3. **Raggruppamento ergonomico del blocco "Quando"**:
   - Il controllo temporale è ora racchiuso in una scheda visiva unitaria (`#boxQuando`), con intestazione sintetica "QUANDO", pulsante "Adesso", selettore giorno feriale/sabato/domenica, cursore orario con play/pausa e velocità animazione, e frase di contesto orario.

## Scelte effettuate
- **Tema e sottotema di partenza**: "Servizio e abitanti" con la modalità "Indice di servizio" (poca offerta in rosso per 1000 abitanti). È l'analisi centrale del progetto ("punti critici: domanda alta contro offerta bassa").
- **Compatibilità all'indietro**: nella funzione `applicaTema(id)` è stato inserito un reindirizzamento protettivo per vecchi identificatori (`offerta` -> `servizio [serv]`, `domanda` -> `servizio [dens]`, `rapporto` -> `servizio [rapp]`, `traffico`/`velocita` -> `traffico_vel`), in modo che eventuali chiamate esterne o ripristini di stato continuino a funzionare.
- **Nessuna modifica a calcoli o schede**: dati, logiche di rendering, database e schede al clic non sono stati toccati (oggetto di GT17 e GT18).

## Cosa Leo deve verificare
- Verificare che il nuovo aspetto compatto del blocco "Quando" e la tendina con i 4 temi risultino comodi da usare sullo schermo del proprio browser.

## Come provarlo
1. Rigenerare la mappa (lo fa il runner oppure lanciando `python scripts/04_genera_mappa.py`).
2. Aprire `mappa_torino.html` nel browser (Chrome, Edge o Firefox).
3. Verificare nel pannello di sinistra:
   - Il blocco "Quando" in alto racchiuso in un unico riquadro chiaro.
   - Il menu a tendina "Tema" contenente esattamente 4 voci: *Servizio e abitanti*, *Traffico e velocità*, *Tempo reale e flotta*, *Pendolarismo*.
   - Selezionando *Servizio e abitanti*, compare la tendina interna con *Indice di servizio*, *Solo offerta*, *Solo residenti*: provando a passare dall'una all'altra, la mappa e la legenda si aggiornano subito.
   - Selezionando *Traffico e velocità*, si accendono insieme i sensori 5T e le linee colorate per velocità commerciale, con le relative legende e il riquadro delle segnalazioni.
