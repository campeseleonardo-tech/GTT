# ESITO C5 — stile «Torino», numeri che contano, omini (cloud, 22/10/2026)

Piano 4 passi 2 e 3, piano 3 punto 3. Stile scelto da Leo il 22/10: **Torino** (blu e oro, verde acqua per il bene, granata per il male; Barlow Condensed + Barlow).
Si è lavorato con i dati veri: `data/` ora è in git, quindi `data/schede_risultati.js` è stato rifatto qui con `python scripts/schede_risultati.py` (prima del cambio era identico al file in git).

## Cosa è stato fatto
1. **`assets/stile.css`**: l'unico posto dei colori del sito (variabili in `:root`, modo scuro con `prefers-color-scheme`), font in `assets/font/` (4 file `.woff2`, 90 KB), barra in alto, piè di pagina, riquadri, finestra, grafici, omini. `index.html` e `risultati.html` non scrivono più colori.
   Nuovi: `assets/sito.js` (numeri in italiano, numeri che salgono, «dati aggiornati al …»), `assets/icona.svg` + `icona-32.png` + `icona-180.png`, `assets/anteprima.png` (1200x630, con la mappa e tre numeri veri; rifatta da `python scripts/costruisci_asset_sito.py`).
2. **Anteprima dei link** su `index.html`, `risultati.html` (e `progetto.html`): `description`, Open Graph e Twitter con titolo, descrizione e immagine (indirizzo `https://campeseleonardo-tech.github.io/Turin-mobility/...`).
3. **Barra in alto** (Home · Risultati · Mappa · Il progetto) e **piè di pagina** («Chi sono»: Leonardo Campese, LinkedIn, email, GitHub, licenza MIT, «Dati aggiornati al 22/10/2026» letto dalle schede). Il bottone IT/EN arriva in C6.
   `progetto.html` esiste come **segnaposto** (titolo e due bottoni) per non avere un link rotto: lo sostituisce C11.
4. **Mappa** (`scripts/mappa_template.html` e `mappa_torino.html`, stesse modifiche a mano nei due file, come in C1): variabili e font del sito nel pannello (modo scuro compreso, font da `assets/font/`), titolo «Torino Mobilità», link a Home e Il progetto,
   scale dei dati ripensate: `PAL_VR` verde acqua → corallo/granata, `PAL_NEU` blu → oro, doppio svantaggio, servizi mancanti, aree e stato dei parcheggi, velocità. Restano un file unico; il 04 non cambia.
5. **Numeri che contano**: solo nei 5 riquadri della home e nel numero grande della scheda aperta, da 0 al valore in circa 1 secondo, una volta, in formato italiano; con «riduci movimento» il numero è subito quello finale (provato). Dissolvenza all'apertura della finestra.
6. **Omini e quadratini** (nuovo campo `unita` nella forma delle schede, scritto da `schede_risultati.py`): scheda 5 = 10 omini con 1 colorato (9,5%); scheda 2 = 100 quadratini con 14 colorati (14,1% oltre 5 minuti); scheda 3 = 12 pallini, uno per punto prioritario (0 verde, 1 giallo, 11 rossi). Sempre con la didascalia scritta.
7. **Scheda 5, grafico della metro**: ora barre delle differenze (con metro meno senza metro) per fascia di distanza, con il numero di zone scritto sotto ogni barra: +73 (6 con, 8 senza), +219 (3 con, 16 senza), +52 (2 con, 10 senza), «non confrontabile» per 6-8 km (0 con, 1 senza).
8. Correzioni al `.gitignore`/inventario: i file `data/catalogo/*.js` sono caricati dalla mappa e vanno in git (prima `reti.js` era escluso); regola nello script 96.

## Prove (cloud, dati veri)
- `python scripts/prova_pagine.py`: 19 pagine, **0 errori**, prova del cambio di indirizzo OK; pesi in git 154 MB, 0 errori.
- `python scripts/prove/screenshot_sito.py`: 25 immagini in `sviluppo/c5_screenshot/` (computer 1440x900 e telefono 390x844, chiaro e scuro, e «riduci movimento»): nessun errore JavaScript, nessuna richiesta esterna, nessuno scorrimento orizzontale.
  Home, risultati, schede 2, 3 e 5, mappa (tema Fragilità sociale), progetto; file `<pagina>_<computer|telefono>_<chiaro|scuro>[_riduci_movimento].jpg`.
- Peso: `index.html` + `assets/` = 0,6 MB (sotto 1 MB); la mappa resta circa 6 MB (+ i 3 font, caricati a parte).
- `scripts/86_controlla_file_pagine.py`: dopo il commit dei file nuovi tutto «in git» (prima li segnalava perché non ancora salvati).

## Da fare sul PC (giro P5 arriverà dopo C9; per ora)
1. Unire il ramo; `git status` deve mostrare anche `data/catalogo/reti.js` (ora non più escluso) e `data/schede_risultati.js`.
2. `scripts\RIFAI_MAPPA_E_SCHEDE.bat`: rigenera `mappa_torino.html` dal template e le schede dai dati veri; poi `python scripts\prova_pagine.py` = 0 errori.
3. Aprire `index.html`, `risultati.html` (scheda 5: omini e barre della metro; scheda 2: quadratini; scheda 3: pallini) e `mappa_torino.html` (tema «Fragilità sociale» e «Servizi mancanti»: verde acqua → granata, legende con i numeri).
