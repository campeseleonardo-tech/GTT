# Esito C8 — home con i mezzi in movimento (22/10/2026, cloud)

## Fatto
- **A. Mezzi in movimento** (`assets/mezzi.js`, riquadro `.eroe` in `index.html`, stile in `assets/stile.css`): riquadro scuro a tutta larghezza con il contorno di Torino (`assets/torino_contorno.json`, fatto da `scripts/costruisci_contorno_torino.py`
  dai confini della mappa) e i puntini dei mezzi dell'ora tipica: bus azzurri, tram oro, metro verde acqua (nei dati non ci sono metro: il GPS è solo sui mezzi di superficie). Scia corta, orologio che scorre, 20 secondi per giro.
  Computer: città a destra, testo a sinistra; telefono: città dietro il testo. Si ferma se la scheda del browser non si vede o se il riquadro è fuori schermo; 30 fotogrammi al secondo al massimo (misurati: 30,3);
  con «riduci movimento» un fotogramma fermo. Senza i dati la pagina resta valida (solo il testo).
- **Dati** (`scripts/schede/home.py`, chiamato da `schede_risultati.py`, scrive `data/home_mezzi.js`, 147 KB): ora tipica da `data/storico_riassunti/ora_tipica.json`, classe bus/tram dalla tabella di `risultato4_regolarita.json`, contorno e contatore.
  `home_mezzi.js` è entrato in git (`.gitignore`). Home intera: circa 0,7 MB con le miniature.
- **J. Contatore**: «Il Raspberry Pi legge Torino da 13 giorni: 1,6 milioni di passaggi di bus e tram alle fermate misurati col GPS» (IT e EN). **Scelta mia**: i riassunti non contengono le singole posizioni del GPS, ma i
  passaggi alle fermate misurati col GPS (un passaggio ogni 4 byte di `gps_trip.bin`), e sono quelli che conto; i giorni vanno dal primo all'ultimo giorno presente nei riassunti (10/10, non il 3/10 d'avvio della raccolta). I numeri salgono da 0 una volta sola.
- **K. Miniature**: `python scripts/prova_pagine.py` (con Playwright e Pillow) rifà `assets/miniature/p1…p5.webp` (480×270, 5-12 KB) dallo screenshot del grafico principale di ogni scheda (con «riduci movimento»); nei riquadri della home.
  Sono in modo chiaro anche quando la pagina è scura.

## Problema trovato nei dati (importante)
L'ora tipica fatta dal giro P3 (giorno 15/10) ha il GPS a ondate: il feed non si aggiorna per qualche minuto e tutti i mezzi spariscono insieme, e dopo i primi 22 minuti non ci sono più posizioni.
Cosa ho fatto: (1) `home.py` unisce i buchi fino a 6 minuti con una linea retta fra la fine di un tratto e l'inizio di un altro della **stessa linea** abbastanza vicino (871 unioni), (2) l'animazione gira solo sui passi che hanno dati (qui dalle 7:30 alle 7:52, 21 minuti)
e `home.py` scrive un AVVISO. (3) **Ho cambiato lo script 97**: ora sceglie il giorno feriale con la copertura migliore (passi da 30 secondi con almeno una posizione), non quello mediano per numero di corse.
**Non l'ho potuto provare sui dati veri**: sul PC lancia `python scripts\97_riassunti_storico.py --solo ora --rifai`, poi `RIFAI_MAPPA_E_SCHEDE.bat`. Se anche il giorno migliore ha buchi, l'AVVISO lo dice e ne parliamo.

## Prove
- Browser headless: home su computer chiaro e scuro, telefono, inglese, «riduci movimento»; 0 errori; schermate in `/tmp` (non in git).
- `prova_pagine.py`: vedi esito C9 (stesso lancio).
