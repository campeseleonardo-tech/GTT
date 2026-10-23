# Esito C10 — area che si espande (23/10/2026, cloud)

## Fatto
1. **Script 93: nessuna modifica.** Il suo `tp_contro_auto.json` ha già la tabella zona × zona completa: `coppie` (con collegamento: `tp_min`, `auto_punta_min` col fattore dei sensori, `auto_punta_basso_min` col fattore di Google) più `senza_collegamento` (solo auto a flusso libero); 2.719 + 2.251 = 71 × 70 coppie. Fra le 23 zone di Torino (gruppo «a») tutte le 506 coppie hanno i tempi.
2. **`scripts/99_area_tempi.py`** (numero 99 nuovo; prossimo libero **100**). Da Piazza Castello a ogni sezione di Torino con residenti (4.044, centroidi da `accessibilita_piedi5.json`):
   mezzi con r5py (come 93: 12/10, 7:45, finestra 30 minuti, mediana, cammino 4,8 km/h, massimo 120 minuti) e auto sulla rete del modello (flusso libero × fattore + 5 minuti) **con i due fattori del 93**, letti da `tp_contro_auto.json`.
   Ricopia dal 93 la tabella zona-zona di Torino e assegna ogni sezione alla sua zona (punto nel poligono di `imq_zone_geo.json`; 11 sezioni su 4.044 cadono fuori dai poligoni e vanno alla zona più vicina).
   Uscita `data/processed/area_tempi.json` (~100 KB, minuti interi) e `docs/rapporti/RAPPORTO_AREA_TEMPI.txt`. Opzioni: `--prova N`, `--finto` (tempi finti dalla distanza, scrive `area_tempi_finto.json`, solo per provare la pagina).
   Scelta mia: **solo sezioni di Torino** (le percentuali sono «torinesi raggiunti»; la cintura peserebbe di più e ha i mezzi incompleti).
3. **`assets/area.js`** (componente come `gara.js`) + grafico «area che si espande» nella scheda 4, subito sotto il grafico principale: due mappe di quadratini (mezzi / auto), cursore 0-60 minuti e ▶ (9 secondi), tendina della partenza («Piazza Castello» in dettaglio per sezione + 23 zone di Torino, per zona), tendina del traffico in auto (scorrevole ×1,2 / pesante ×2,1; scelta mia: parte da «scorrevole»),
   quota di torinesi raggiunti sotto ogni mappa e tabella con le soglie 10, 20, 30, 45 (l'auto sempre come forbice fra i due fattori). Con «riduci movimento»: niente cursore, 4 soglie affiancate e ferme. IT/EN (testo in `testi.json`).
   I dati stanno in `data/area_tempi.js` (~100 KB, scritto da `scripts/schede/r8.py`, caricato dalla pagina solo quando si apre il grafico); senza `area_tempi.json` la scheda esce **senza** il grafico (con un AVVISO) e il resto non cambia.
4. `scripts/AREA_TEMPI.bat`: prova su 200 sezioni, calcolo vero, schede, prova delle pagine. `.gitignore`: `data/area_tempi.js` tenuto, prove escluse.

## Prove (cloud, dati finti nello stesso formato)
- `99 --finto`: 4.044 sezioni, 23 zone, controlli OK (tempi non negativi, tutte le sezioni in una zona, tabella completa, soglie crescenti).
- Pagina vera `risultati.html#p4` aperta in Chromium a 1440, 390 e 1100 px (con «riduci movimento»): 0 errori, ▶ che scorre, cambio di partenza (Cenisia), tabella delle soglie. Prova rifatta poi cancellata: i file di test (`area_tempi.json`, `data/area_tempi.js`) **non** sono in git.
- Il rilancio di `schede_risultati.py` con i dati finti non dà frasi senza traduzione.

## Da fare sul PC (giro P6)
1. `scripts\AREA_TEMPI.bat` (la parte lenta è avviare r5py; poi pochi minuti). Controlli di buon senso scritti dallo script: Piazza Castello → Porta Nuova coi mezzi sotto 15 minuti, auto in centro sotto 10 minuti a flusso libero, nessun tempo negativo; guardare nel rapporto quante sezioni sono senza collegamento entro 120 minuti.
2. Aprire `risultati.html`, scheda 4: il grafico deve mostrare l'area dei mezzi più piccola di quella dell'auto; a 30 minuti i numeri sono nel rapporto `RAPPORTO_AREA_TEMPI.txt`.
3. Il 93 non è stato toccato: niente da rilanciare.
