# Piano: rifare l'accessibilità per sezione (attività 1)

Data: 11/10/2026. Stato: APPROVATO da Leo l'11/10 (decisioni in fondo). Prossimo passo: fase 0.
Script coinvolto: `scripts/18_accessibilita.py`. Uscite: `data/processed/accessibilita.json`,
`docs/RAPPORTO_ACCESSIBILITA.txt`.

## Cosa è successo

- Giro completo del 10/10 sera: fallito l'11/10 ~01:18 per memoria esaurita, all'ora 14:00 (lotto
  119 di 208). A piedi aveva richiesto 6 min, l'ora 08:00 4,5 h. Lo script salva solo alla fine:
  si sono perse ~5,5 h di calcolo.
- Cause: PC con 8 GB di RAM; Java (R5) tiene 3 GB; ogni lotto col trasporto pubblico crea una
  tabella di ~1,9 milioni di righe (40 sezioni x ~47.000 destinazioni); in più giravano due
  processi opencode.
- I numeri non hanno errori del motore (controllo dell'11/10): in Torino R5 a piedi trova il ~91%
  di quanto c'è in linea d'aria entro 720 m (mediane: negozi 686, scuole 16, salute 9). Le mediane
  basse del rapporto venivano dalle 101 sezioni di cintura su 200, dove scuole, salute e cibo
  valgono 0 perché i cataloghi coprono solo il Comune di Torino.

## Fasi

### Fase 0 — Prima di tutto (Leo)

- Aver lanciato `PULIZIA_GTT.bat` (salva in git lo stato dell'11/10).
- Ramo git `prova`. Nessun altro processo opencode pesante mentre si lavora su questo piano.

### Fase 0b — Servizi della cintura da OSM (Claude/agente, prima delle modifiche allo script)

- Fonte: il taglio `data/otp/rete/torino_cintura.osm.pbf` (nodi e way con tag; le relazioni NON ci
  sono: le scuole o gli ospedali disegnati come multipoligono mancano, da dichiarare). Primo controllo:
  verificare che il taglio contenga davvero i tag `amenity`/`shop`/`healthcare`.
- Regola di unione: dentro il Comune di Torino si usa il catalogo comunale; fuori Torino si usano i
  punti OSM. Il confine è quello delle sezioni di Torino (codice comune 1272) o dei confini ISTAT 2022.
- Tag OSM proposti (piccola scelta, modificabile):
  - scuole: `amenity` = school, kindergarten, childcare, college, university;
  - salute: `amenity` = pharmacy, hospital, clinic, doctors, dentist; più `healthcare=*`;
  - cibo: ATTENZIONE, in Torino il gruppo usa TUTTE le 31.405 attività commerciali, non solo il
    cibo. Per coerenza fuori Torino si prendono tutti i `shop=*` + `amenity=marketplace`, non solo
    i negozi alimentari (altrimenti la cintura sembrerebbe più povera per costruzione).
- Controllo di completezza: contare gli stessi tag OSM DENTRO Torino e confrontarli col catalogo
  (es. OSM trova X farmacie contro 243 del catalogo). Il rapporto OSM/catalogo dice quanto la
  cintura è sottostimata e va scritto nel rapporto e nella scheda in mappa.
- Uscita: `data/processed/servizi_osm_cintura.json` (script nuovo: `20_servizi_osm.py`), con
  bollino della fonte per ogni punto (CATALOGO o OSM).

### Fase 1 — Modifiche allo script 18 (Claude, ~1 sessione)

1. **Salvataggio a tappe.** Un file per fase in `data/processed/accessibilita_parziale/`
   (`piedi.json`, `tp_08.json`, ...), aggiornato ogni 10 lotti. Se il giro si interrompe, al
   rilancio riparte dall'ultimo lotto salvato. Il file finale si compone alla fine.
2. **Meno memoria.** Si contano i servizi subito, lotto per lotto, e la tabella del lotto si butta.
   Lotti col trasporto pubblico da 40 a 20 sezioni. Si libera la memoria tra un lotto e l'altro.
3. **Velocità a piedi esplicita** (D2), usata sia da R5 sia dal margine dello script (oggi i due
   valori non coincidono: 3,6 contro 4,8 km/h).
4. **Destinazioni accorpate** (solo se D3 = sì): i punti dello stesso gruppo che stanno nella stessa
   cella di ~50 m diventano un punto con un peso. Per i cataloghi: da 32.724 a ~10.300 punti.
5. **Cintura**: le destinazioni fuori Torino arrivano da `servizi_osm_cintura.json` (fase 0b).
6. **Il PC non va in sospensione mentre lo script gira** (lo chiede lo script stesso a Windows,
   solo durante il calcolo).
7. Nel log: tempo per lotto e stima del tempo che manca.
8. Due file a doppio clic: `ACCESSIBILITA_PROVA.bat` (campione di 200) e
   `ACCESSIBILITA_COMPLETA.bat` (tutte le sezioni; se rilanciato riprende da dove era).

### Fase 2 — Prova sul campione (~30–40 min; la lancia l'agente o Leo con il .bat)

- `ACCESSIBILITA_PROVA.bat` con il Task Manager aperto (scheda Prestazioni -> Memoria).
- Controlli (li fa Claude sul risultato):
  - la memoria del PC resta sotto ~85%;
  - le sezioni di Torino danno numeri vicini al campione vecchio (differenze solo per D2/D3);
  - il salvataggio a tappe funziona: si chiude la finestra a metà, si rilancia e riparte.
- Dal tempo per lotto si ricava la durata del giro completo.

### Fase 3 — Giro completo (Leo lancia, di notte)

- Prima di lanciare: chiudere opencode e i programmi pesanti, PC alla corrente.
- `ACCESSIBILITA_COMPLETA.bat`. Durata stimata oggi: 9–10 h (08:00 da sola 4,5 h); la stima
  aggiornata viene dalla fase 2. Se serve, si fa un'ora alla volta in più notti.

### Fase 4 — Controlli sul risultato (Claude)

- 8.317 sezioni presenti per ogni fase; nessun valore negativo o mancante.
- Mediane attese in ordine: 08 >= 14 > 23 > 02. Elenco delle sezioni a zero alle 02.
- Le 3 sezioni di Torino con R5 sotto il 20% della linea d'aria: capire se il centroide cade fuori
  dalla rete (cortile, parco) e se serve correggerlo.
- Rapporto `docs/RAPPORTO_ACCESSIBILITA.txt` con Torino e cintura SEPARATE (mai mediane miste).

### Fase 5 — Chiusura

- Memoria aggiornata, commit su "prova", poi si passa al tema "Criticità" (attività 2).

## Decisioni prese da Leo (11/10/2026)

- **D1 — Cintura:** riempire scuole, salute e commercio fuori Torino con OpenStreetMap (fase 0b).
  Dentro Torino resta il catalogo comunale. Confine città/cintura da dichiarare come cambio di fonte.
- **D2 — Velocità a piedi:** 4,8 km/h (80 m/min), dichiarata nel rapporto; vale sia per R5 sia
  per i margini dello script.
- **D3 — Destinazioni accorpate** in celle di ~50 m, con peso: sì.
- **D4 — Ore del TP:** 08, 14, 23, 02 di lunedì 12/10/2026. In futuro più granularità oraria
  (più ore o tutte le 24): grazie al salvataggio per fase basterà aggiungere ore senza rifare le
  altre.
