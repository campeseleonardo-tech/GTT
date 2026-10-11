# Piano: rifare l'accessibilità per sezione (attività 1)

Data: 11/10/2026. Stato: BOZZA, da approvare con Leo (decisioni D1–D4 in fondo).
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
5. **Cintura** gestita come da D1.
6. **Il PC non va in sospensione mentre lo script gira** (lo chiede lo script stesso a Windows,
   solo durante il calcolo).
7. Nel log: tempo per lotto e stima del tempo che manca.
8. Due file a doppio clic: `ACCESSIBILITA_PROVA.bat` (campione di 200) e
   `ACCESSIBILITA_COMPLETA.bat` (tutte le sezioni; se rilanciato riprende da dove era).

### Fase 2 — Prova sul campione (Leo lancia, ~30–40 min)

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

## Decisioni per Leo

- **D1 — Cintura (scuole, salute, cibo fuori Torino).** I cataloghi esistono solo per il Comune.
  - a) *(proposta)* Quei tre gruppi valgono solo per Torino; in cintura "dato non disponibile" (in
    grigio, non zero). Fermate e verde valgono ovunque. Onesto e subito pronto.
  - b) Completare la cintura con OSM (scuole, farmacie, supermercati). Fonte uniforme ma meno
    completa e diversa dal catalogo; rompe il "catalogo congelato" (qui c'è una domanda che lo
    giustifica). Si può fare dopo, con l'attività 8.
  - c) Calcolare l'accessibilità solo per il Comune di Torino.
- **D2 — Velocità a piedi.** 3,6 km/h (predefinito R5, prudente, adatto ad anziani) oppure
  4,8 km/h (valore usuale per la "città dei 15 minuti"). Proposta: 4,8 km/h, dichiarato nel
  rapporto. Con 4,8 i servizi a piedi crescono (15 min = 1,2 km invece di 900 m).
- **D3 — Accorpare destinazioni vicine (celle di ~50 m).** Errore massimo ~35 m (meno di 30 s a
  piedi), memoria nettamente più bassa; il guadagno di tempo è incerto (il tempo dipende soprattutto
  dalla ricerca dei percorsi, non dalle destinazioni) e si misura nella fase 2. Proposta: sì.
- **D4 — Ore del trasporto pubblico.** Restano 08, 14, 23, 02 di lunedì 12/10/2026 (orario
  valido fino al 31/1/2027)? Proposta: sì; servono per lo scenario "metro di notte".
