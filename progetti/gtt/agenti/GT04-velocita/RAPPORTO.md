# GT04-velocita — Rapporto

## Cosa ho fatto
- `scripts/04_genera_mappa.py`: nuova funzione `calcola_velocita()` (blocco `# [agente GT04-velocita]`), chiamata in `main()`. I dati vanno nella pagina come `vel` = `{linea: {tipo: {ora: [km/h, campioni, giorni]}}}` (tipo 0 feriale, 1 sabato, 2 domenica) e `vel_meta` (primo/ultimo timestamp, ore di storico, righe lette, salti GPS scartati).
- `scripts/mappa_template.html`: nuovo tema **Velocità** nella tabella THEMES, colori, legenda, descrizione al passaggio del mouse/tocco su una linea.
- Non ho toccato `06_dati_live.py` (la logica dell'ora legale è copiata in 04), né data/live.js, stat.js.

## Metodo
- Database aperto SOLO in lettura: `sqlite3.connect("file:...?mode=ro", uri=True, timeout=30)`. Query con `letto_utc >= (adesso − 28 giorni)` (usa l'indice), ordinata per veicolo e `ts_feed`. Un solo passaggio sulle righe, solo somme in memoria.
- Coppie di posizioni consecutive dello stesso veicolo sulla stessa linea, con 20 s ≤ dt ≤ 180 s (se dt < 20 s si aspetta una posizione più nuova; se dt > 180 s si riparte). Distanza = haversine.
- Scartati: tratti > 90 km/h (errore GPS); soste: tratti con spostamento < 20 m che, sommati di fila, superano 5 minuti (capolinea). Le soste brevi (fermate) restano → velocità commerciale.
- Aggregazione per linea × tipo giorno × ora locale italiana (ora legale calcolata a mano): velocità = metri totali / secondi totali; campioni = numero di tratti; giorni = giorni distinti.
- Se il database manca o è bloccato: messaggio, livello saltato, lo script termina normalmente (exit 0); il tema mostra «nessun dato».
- Uscita di 04: "velocità: N linee con dati, M celle linea/tipo/ora, X ore di storico (righe lette, salti GPS scartati)".

## Scelte (default, modificabili)
- Classi: < 12 rosso, 12–16 arancio, 16–20 giallo, > 20 km/h verde.
- Minimo per colorare: **20 campioni** nella cella (≈ 20 minuti-veicolo); sotto, grigio. Il valore c'è comunque nel dettaglio, segnato «troppo pochi campioni».
- «Dati scarsi» se lo storico è < 72 h oppure nessuna cella ha ≥ 3 giorni distinti.
- Soglie tecniche: fermo = spostamento < 20 m; capolinea = fermo > 300 s di fila.
- Il dettaglio compare al passaggio del mouse (come gli altri livelli); sul telefono al tocco. Le «ore con dati» elencano le ore con ≥ 20 campioni per il giorno tipo scelto.
- Nel tema Velocità sono visibili solo le linee (disegnate a spessore fisso); le altre sovrapposizioni si possono riaccendere a mano.

## Limiti
- Senza `trip_id` non c'è ritardo: solo velocità media della linea (entrambi i sensi e tutte le tratte insieme).
- Il feed può non contenere tutti i mezzi; la media è sui mezzi visibili. Con poca storia (iniziata il 4/10/2026) i numeri sono provvisori.
- La velocità si aggiorna solo rigenerando la mappa con 04. Non ho potuto eseguire nulla: i numeri reali li stampa il runner (agenti/ULTIMO_SCRIPT.txt).
- Una linea con più direzioni/varianti usa un solo colore.

## Da provare (clic)
1. Aprire `mappa_torino.html`, pulsante tema **Velocità**.
2. Cambiare giorno (Feriale/Sabato/Domenica) e ora: i colori delle linee cambiano; grigio = nessun dato.
3. Passare il mouse su una linea colorata: km/h, campioni, giorni, ore con dati.
4. Legenda in basso: etichetta MISURATO (+ «dati scarsi» finché lo storico è corto) e la riga sulla velocità commerciale.
5. Tornare agli altri temi: devono funzionare come prima.

## Domande per Leo
Nessuna bloccante.
