# Risultato 8 — Traffico sulle strade e trasporto pubblico

**Domanda.** Quanti veicoli passano sulle strade di Torino, e dove c'è molto traffico ma poco trasporto pubblico (TP),
così che l'auto resta l'unica scelta?

**Tag dati:** [STIMATO] (modello della domanda IMQ 2022 sulla rete OSM, tarato su 20 sensori 5T) + [PROGRAMMATO] per il
TP (orario GTFS).

## Risposta

- Sulle **540 tratte di strade grandi di Torino (343,3 km)** il **95,3% della lunghezza** ha una fermata con almeno 4
  passaggi all'ora entro 300 m oppure la metro entro 600 m. La frase giusta è: *lungo le strade grandi di Torino c'è
  quasi sempre una fermata frequente a meno di 300 m*; non vale per tutte le strade.
- **180 tratte** hanno molto traffico (≥ 11.720 veicoli/giorno, 6-21, due versi); **5** hanno anche poco TP: in pratica
  **corso Regina Margherita ovest** (scorrimento veloce, circa 34.000 veicoli/giorno, nessuna fermata frequente
  entro 300 m) e **un tratto di corso Moncalieri** (coperto per un quarto; da controllare a mano).
- Una lista precedente di 23 strade era un artefatto: il TP era misurato lungo la strada per nome. Con le fermate
  cercate per posizione è sparita.

## Qualità della stima: classe C-DEBOLE

Errore mediano **38,4%** (intervallo 90%: 25,5-49,8%), correlazione di Spearman **0,605**, 20 punti di misura, fattore
di taratura k = 0,953. Fasce pubblicate: metà dei casi entro ±38%, 9 su 10 entro ±64%; fuori da 8.845-105.230
veicoli/giorno è un'estrapolazione e la fascia raddoppia. **Serve a ordinare le strade, non a contare i veicoli.**

| Classe di esito | Condizione | Cosa si pubblica |
|---|---|---|
| C-ASSOLUTO | errore ≤ 35%, meglio del metodo A, ρ ≥ 0,7 | veicoli/giorno con fascia |
| C-INDICE | ρ ≥ 0,7 ma errore > 35% | solo indice relativo |
| C-DEBOLE | 0,5 ≤ ρ < 0,7 | classi alto/medio/basso, marcate «debole»; numeri assoluti con fascia |
| C-NO | ρ < 0,5 | niente |

## Come si calcola

- **Sensori 5T:** 112 sensori che danno già veicoli/ora; esclusi 17 (11 morti, 5 bloccati, 1 con pochi dati) → 92
  usabili; abbinamento sensori-corridoi per posizione → 20 unità di confronto su 15 corridoi. Velocità e flusso
  tipici per sensore × tipo di giorno × ora: `data/processed/velocita_5t.json` (solo letture affidabili).
- **Metodo C (adottato):** domanda auto IMQ (4,15 milioni di viaggi/giorno) assegnata al percorso più veloce sulla rete
  OSM (81.966 nodi, 105.890 tratti, porte sul bordo). I modelli più ricchi (attrattori, code, corsie) non hanno
  migliorato la correlazione (ρ 0,573 e 0,571) e non si adottano: la congestione non funziona (Piazza Castello →
  Collegno 13,8 minuti nel modello contro 20-35 attesi in punta). Se si riprova, la strada è la congestione
  (domanda per fascia oraria, capacità reali).
- **Strade:** solo strade grandi; fermate e strade solo per coordinate, mai per nome; un corso che cambia nome o comune
  è un solo asse; l'unità è la tratta d'asse (0,3-1,5 km). ZTL unificata (3 zone + 143 aree pedonali); corsie da OSM
  `lanes` (29% dei tratti).
- **TP per posizione:** 5.055 fermate, 13.158 corse di un feriale del GTFS; «poco TP» = accessibilità (fermate vicine
  con buon servizio), non bus che passano sulla strada.

## Controllo di buon senso

Un giudizio qualitativo di una persona che conosce la città (strade A = molto trafficate, B = medie, C = tranquille) è
usato solo come controllo, mai per tarare il modello: 10 strade su 18 nella fascia giusta, 4 confronti su 7. Regole
che ne vengono: un corso cambia nome lungo il percorso (Trapani → Lecce → Potenza; Agudio → Sturzo), l'asse non si
ferma al confine comunale; a parità di traffico una strada a due corsie sente meno pressione di una a una corsia; il
centro-centro non è prioritario. Il modello **sottovaluta** il semicentro (Bolzano, Quintino Sella, Lombardia, Re
Umberto, Vittorio Emanuele II) e **sopravvaluta** raccordi e strade corte (Palestrina, Monte Lungo, Quarto dei Mille);
ai sensori corso Unione Sovietica è +177% e corso Sebastopoli +99%.

## Noi contro Google Maps

**Metodo della forbice.** Il tempo in auto non conta semafori e incroci, quindi ha un fattore di punta incerto. Il risultato è una **forbice con due fattori**:
il **limite alto** del rapporto coi mezzi pubblici usa il fattore dei sensori 5T (1,2: mediana di velocità 2-5 / velocità alle 8 su 97 sensori);
il **limite basso** usa il fattore di Google Maps (2,1: mediana di (tempo Google − 5) / flusso libero sui 6 percorsi da Piazza Castello). I due percorsi di controllo non entrano nel fattore.

Controllo a mano, **martedì 20/10/2026 alle 8:00**. I primi 6 percorsi partono da Piazza Castello; gli ultimi 2 sono di controllo. Tempi in minuti.

| Percorso | Mezzi pubblici, nostri | Mezzi pubblici, Google | Auto, nostra (fattore alto 1,2) | Auto, nostra (fattore basso 2,1) | Auto, Google |
|---|---|---|---|---|---|
| Piazza Castello → Collegno | 47 | non controllato | 21 | 33 | 19 |
| Piazza Castello → Venaria Reale | 64 | non controllato | 20 | 32 | 31 |
| Piazza Castello → Settimo Torinese | 62 | non controllato | 22 | 35 | 38 |
| Piazza Castello → Moncalieri | 48 | non controllato | 19 | 29 | 34 |
| Piazza Castello → Orbassano | 74 | non controllato | 27 | 43 | 44 |
| Piazza Castello → Rivoli | 66 | non controllato | 27 | 43 | 38 |
| Corso Racconigi → Piazza Castello (controllo) | 31 | 30-35 (mezzi pubblici) | 13 | 18 | 29 |
| Moncalieri → Lingotto (controllo) | 33 | 30-35 (solo GTT; col treno 19-23) | 13 | 19 | 14 |

- **Mezzi pubblici**: i nostri tempi sono in linea con Google sui due percorsi di controllo (31 contro 30-35, 33 contro 30-35 solo GTT). Col treno Google scende a 19-23 sul Moncalieri → Lingotto: i treni nei nostri dati non ci sono.
- **Auto**: col fattore alto siamo sotto Google di 11,4 minuti in media (sui 6 percorsi); col fattore basso di 1,7 (differenza media, nostro meno Google). La verità sta nella forbice.
- Rapporto mediano coi mezzi pubblici (Torino-Torino e Torino-cintura): **da 1,96 a 2,94**.

### Forbice: rapporto mediano e fasce (Torino-Torino e Torino-cintura, 220.307 auto)

Fasce fisse del rapporto (tempo coi mezzi / tempo in auto), fissate prima di vedere i numeri. Celle: auto (% delle auto).

| Limite | Fattore | Rapporto mediano | Oltre 2 | sotto 1,5 | 1,5-2 | 2-3 | oltre 3 |
|---|---|---|---|---|---|---|---|
| **Basso** (Google Maps) | 2,1 | **1,96** | 41,4% | 8.649 (3,9%) | 120.360 (54,6%) | 90.508 (41,1%) | 791 (0,4%) |
| **Alto** (sensori 5T) | 1,2 | **2,94** | 97,0% | 0 (0,0%) | 6.661 (3,0%) | 115.033 (52,2%) | 98.612 (44,8%) |

Per gruppo (basso | alto). Cintura-cintura è a parte: mancano treni e altre aziende.

| Gruppo | Mediano basso | Mediano alto | Oltre 2 basso | Oltre 2 alto |
|---|---|---|---|---|
| (a) Torino-Torino | 1,96 | 2,78 | 39,2% | 93,5% |
| (b) Torino-cintura (e cintura-Torino) | 1,97 | 3,07 | 43,4% | 100,0% |
| (ab) principale: Torino-Torino e Torino-cintura | 1,96 | 2,94 | 41,4% | 97,0% |
| (c) cintura-cintura | 2,23 | 3,49 | 78,8% | 100,0% |

## Limiti

- Stima debole; senza un sensore sull'asse la classifica mette in cima strade poco credibili (corso Dogliotti circa
  58.500): nella scheda si mostrano solo strade con un sensore sull'asse.
- 20 punti di misura, tutti fra circa 9.000 e 105.000 veicoli/giorno; a Torino sensori a un solo verso (×2 per i due
  versi); la notte è inaffidabile e l'ora di punta non è validata.
- Domanda IMQ 2022: solo residenti 11-84 anni, feriale medio; mancano merci, turisti, pendolari da fuori.
- TP programmato: niente ritardi né affollamento. Il centro (ZTL, pedonali) non è stimato bene.
- Convenzione a due versi: ogni tratto OSM a senso unico vale ×2, quindi il doppio del reale sulle vie a senso unico
  vere (al massimo 47 tratte, 24 km).
- `tratte_traffico.json` dice 539 tratte / 342,8 km, `risultato8_traffico_tp_v2.json` 540 / 343,3 (giri diversi dello
  script 65/66).

## Script e come rifarlo

| Script | Cosa fa |
|---|---|
| 26 | velocità e flusso 5T tipici → `velocita_5t.json` |
| 33-48, `rete_osm.py` | flusso per sensore, esclusioni, abbinamento, modello della domanda sulla rete |
| 56-67 | assi e tratte, corsie, ZTL, TP per posizione, valutazione finale |
| `schede_risultati.py` (`scheda_r8`) | scheda con errore % per sensore |
| 93 | tempo coi mezzi contro auto fra zone IMQ: forbice con due fattori di punta → `tp_contro_auto.json` (si rifà in circa 1 minuto) |

Risultato: `data/processed/risultato8_traffico_tp_v2.json` (universo, assi da guardare, tratte); dettaglio per tratta in
`data/processed/traffico_d/tratte_traffico.json`; valutazione in `traffico_d/valutazione_fase5.json`.

```
scripts\FETCH_LEOPI_E_VELOCITA_5T.bat      (dopo ogni raccolta dal Pi)
scripts\TRAFFICO_RILANCIA_SENSORI.bat      (riscrive anche i rapporti)
scripts\FASE5_MODELLO.bat                  (assi, corsie, ZTL, TP, modello; lungo, circa 1 ora)
python scripts\schede_risultati.py
```

Da fare: controllo a mano della copertura TP di corso Moncalieri; `velocita_5t.json` al posto del «tipico» di
`data/stat.js` nella mappa (quello calcolato sul Pi non scarta le letture inaffidabili); aggiungere unità di confronto
dopo alcuni feriali con i codici sensore corretti; cambio dell'ora legale del 25/10 da controllare nello script 26.
