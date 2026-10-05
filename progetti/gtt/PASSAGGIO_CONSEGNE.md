# Mappa mobilità Torino - passaggio di consegne (aggiornato 4/10/2026)

Incolla questo file in una nuova chat. Contesto: Leo, italiano a Salisburgo, PC Windows, Python, non programmatore (spiegazioni semplici, poco gergo). Preferenze: essere critici ma non assertivi, tutte le domande prima di costruire, niente costruzioni senza piano, pochi token, dati locali, provare su copie. Cartella: `Desktop\GTT`. Memoria di progetto: `MEMORIA_PROGETTO.md` (più dettagliata di questo file).

## Obiettivo
Pagina HTML interattiva di Torino e cintura: offerta e domanda di trasporto, punti critici (poca offerta per gli abitanti, traffico lento, mezzi in ritardo), flussi simulati il più possibile vicini ai veri orari. Uso personale per ora, forse condivisione.

## Cosa esiste (tutto in GTT)
- `mappa_torino.html` (~6 MB, doppio clic in Chrome/Edge): mappa su canvas in JavaScript puro, dati incorporati. Si ricostruisce con `scripts/04_genera_mappa.py` dal modello `scripts/mappa_template.html`.
- Dati statici incorporati: orari GTT (GTFS, validi 1/10/2026-31/1/2027), tracciati linee, 7.036 fermate, 94 zone statistiche (2011), 8.317 sezioni di censimento abitate 2021 (1,56 milioni abitanti, Torino 848.748).
- Livelli: sezioni (3 colorazioni: poca offerta per abitante = passaggi/ora entro 400 m ogni 1000 abitanti entro 400 m; passaggi/ora; abitanti/km²; grigio = nessun passaggio), zone, linee, fermate (da zoom 14), sensori traffico 5T, mezzi GTT reali, corse simulate (13.683 feriali/10.747 sabato/6.981 domenica, velocità costante lungo il tracciato tra prima e ultima fermata: STIMA, non reale), replay di giornate registrate.
- Comandi: giorno tipo (feriale/sabato/domenica), slider al minuto, play/pausa, velocità 1x-240x, pannello zoom (+, -, Torino, cintura, tasti + e -), sfondi (chiara=OpenStreetMap schiarito, stradale, satellite Esri; CARTO NON usare: richiede chiave), filtro per linea, colore linee per corse/ora o per mezzi reali rispetto al previsto, riquadro "Segnalazioni adesso", riquadro "Dati raccolti".
- Dati reali nella pagina: ogni 30 s rilegge `data/live.js`, ogni 5 min `data/stat.js`; replay da `data/replay_AAAA-MM-GG.js` (ultimi 10 giorni).

## Raccolta dati (gira sul PC, in futuro forse su Raspberry Pi 192.168.8.200)
- `scripts/03_raccolta_continua.py`: SQLite `data/storico.sqlite` (tabelle sensori_5t, flussi_5t, mezzi_gtt, errori). 5T ogni 300 s, mezzi GTT ogni 60 s. Senza librerie esterne (decoder protobuf scritto a mano).
- `scripts/supervisore.py`: avvio nascosto all'accesso a Windows, riavvio dopo 30 s, log mensili in `logs/`, impedisce lo stop del PC, finestra domenicale dopo le 20:00 "continuiamo?" (nessuna risposta in 1 h = continua, No = ferma, file `data/STOP_RACCOLTA.txt`), avviso oltre 10 GB. Ogni minuto lancia `06_dati_live.py` (live), ogni 15 min statistiche e replay.
- Installazione: `installa_raccolta.bat` (installa e avvia), `stato_raccolta.bat`, `ferma_raccolta.bat`, `riavvia_raccolta.bat`. Il vecchio `raccolta_continua.bat` è solo manuale.
- `scripts/06_dati_live.py`: legge il database in sola lettura e scrive live.js, stat.js (traffico tipico per sensore/ora/tipo giorno, mezzi reali per linea/ora, cache `data/agg_cache.json`), replay.
- Altri script: `01_scarica_dati.py` (scarica GTFS, feed realtime, 5T, zone in `data/raw`), `02_ispeziona_dati.py` (rapporto), `05_prepara_sezioni.py` (confini sezioni da `R01_21.zip` -> `data/processed/sezioni_torino.json`).
- Ordine per rigenerare la mappa: 01 (dati nuovi) -> 04. Il 05 solo una volta.

## Fonti
GTFS e GTFS-realtime GTT (gtt.to.it, percorsieorari.gtt.to.it), 5T opendata (opendata.5t.torino.it/get_fdt, 112 sensori, molti con accuracy 0 = significato incerto), ISTAT censimento 2021 (indicatori per sezione `Dati_regionali_2021.zip`, confini `R01_21.zip`, matrici pendolarismo comune-comune 2021 già scaricate), zone statistiche del Comune di Torino (CSV in Gauss-Boaga, riproiettato). Dettagli in `docs/FONTI_DATI.md`.

## Limiti onesti
- Offerta = orari programmati. Residenti = popolazione "di notte", non chi si sposta a quell'ora: la DOMANDA PER ORA non c'è ancora.
- Fuori Torino mancano altri operatori e treni: il rosso in cintura può essere mancanza di dati.
- Il feed GTT delle posizioni non ha il trip_id: i ritardi non sono misurabili; trip_update vuoto di notte.
- Storico appena iniziato (4/10/2026): "rispetto al solito" è indicativo (etichetta "dati scarsi" sotto 72 ore).
- Veicoli localizzati nel feed potrebbero non essere tutti.
- Provato in browser di prova e su Linux; non provato su Windows: finestra settimanale, anti-stop, avvio automatico.
- Ambiente cloud senza accesso a gtt.to.it, 5T, ISTAT, npm, pip: i download li fa Leo sul PC; non aggirare i blocchi.
- Il cloud non può spostare/cancellare file sul PC di Leo: i file ISTAT sparsi in GTT vanno spostati da lui (`data\raw\istat\...`, `docs\istat\`).

## Prossimi passi (in ordine)
1. Verificare che la raccolta in background parta e che il riquadro "Dati raccolti" mostri dati live (dopo ferma + installa).
2. Livello domanda per ora: pendolari/lavoratori/studenti (matrici ISTAT 2021 comune-comune già presenti; matrice 2011 per sezione con mezzo e fascia oraria ancora da trovare, forse micro.zone@istat.it).
3. Indicatore combinato "punti critici" (poca offerta + traffico lento + scostamenti dai dati reali), con etichetta dati scarsi.
4. Dopo una-due settimane di dati: traffico tipico affidabile, simulazione dei flussi calibrata sui sensori 5T, capire accuracy 0.
5. Richieste dati rimandate: MTM per IMQ 2022, dati telefonia (bozze in `docs/`).
6. Eventuale passaggio sul Raspberry Pi (adattare supervisore: niente finestre Windows) e condivisione della mappa.
