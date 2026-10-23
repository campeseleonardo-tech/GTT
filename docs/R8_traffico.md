# Risultato 8 — Traffico sulle strade e trasporto pubblico

**Domanda.** Quanti veicoli passano sulle strade di Torino, e dove c'è molto traffico ma poco trasporto pubblico (TP),
così che l'auto resta l'unica scelta?

**Tag dati:** [STIMATO] (modello della domanda IMQ 2022 sulla rete OSM, tarato su 22 punti di misura dei sensori 5T) + [PROGRAMMATO] per il
TP (orario GTFS).

## Risposta

- Sulle **611 tratte di strade grandi di Torino (372,7 km)** il **95,6% della lunghezza** ha una fermata con almeno 4
  passaggi all'ora entro 300 m oppure la metro entro 600 m. La frase giusta è: *lungo le strade grandi di Torino c'è
  quasi sempre una fermata frequente a meno di 300 m*; non vale per tutte le strade.
- **204 tratte** hanno molto traffico (≥ 10.677 veicoli/giorno, 6-21, due versi: il terzo più alto delle tratte); **5** hanno anche poco TP: in pratica
  **corso Regina Margherita ovest** (scorrimento veloce, circa 32.000 veicoli/giorno, nessuna fermata frequente
  entro 300 m) e **un tratto di corso Casale** (coperto per un quarto; da controllare a mano).
- Una lista precedente di 23 strade era un artefatto: il TP era misurato lungo la strada per nome. Con le fermate
  cercate per posizione è sparita.

## Qualità della stima: classe C-DEBOLE

Errore mediano **28,3%** (intervallo 90%: 24,2-37,9%), correlazione di Spearman **0,639**, 22 punti di misura, fattore
di taratura k = 0,980. Fasce pubblicate: metà dei casi entro ±28%, 9 su 10 entro ±62%; fuori da 8.974-106.543
veicoli/giorno è un'estrapolazione e la fascia raddoppia. **Serve a ordinare le strade, non a contare i veicoli.**

| Classe di esito | Condizione | Cosa si pubblica |
|---|---|---|
| C-ASSOLUTO | errore ≤ 35%, meglio del metodo A, ρ ≥ 0,7 | veicoli/giorno con fascia |
| C-INDICE | ρ ≥ 0,7 ma errore > 35% | solo indice relativo |
| C-DEBOLE | 0,5 ≤ ρ < 0,7 | classi alto/medio/basso, marcate «debole»; numeri assoluti con fascia |
| C-NO | ρ < 0,5 | niente |

## Come si calcola

- **Sensori 5T:** 112 sensori che danno già veicoli/ora; esclusi 17 (11 morti, 5 bloccati, 1 con pochi dati) → 92
  usabili; abbinamento sensori-corridoi per posizione → 22 unità di confronto. Velocità e flusso
  tipici per sensore × tipo di giorno × ora: `data/processed/velocita_5t.json` (solo letture affidabili).
- **Modello adottato: V4** (script 62-63). Domanda auto IMQ (4,15 milioni di viaggi/giorno) assegnata sulla rete
  OSM (81.966 nodi, 105.890 tratti, porte sul bordo di rango ≥ 3) con destinazioni per attrattori, congestione con capacità
  per corsia (funzione BPR, punta del mattino) e ZTL/aree pedonali chiuse. La scelta fra il modello semplice (V0) e V4 la fa
  una regola fissata prima di vedere i numeri (script 63): con i 20 sensori di metà ottobre vinceva V0 (errore 38,4%, ρ 0,605
  contro ρ 0,571); con 22 sensori (altri giorni di dati) vince V4 (errore 28,3%, ρ 0,639) e **cambia il modello pubblicato**.
  La congestione resta debole: Piazza Castello → Collegno 13,8 minuti nel modello contro 20-35 attesi in punta.
- **Strade:** solo strade grandi; fermate e strade solo per coordinate, mai per nome; un corso che cambia nome o comune
  è un solo asse; l'unità è la tratta d'asse (0,3-1,5 km). ZTL unificata (3 zone + 143 aree pedonali); corsie da OSM
  `lanes` (29% dei tratti).
- **TP per posizione:** 5.055 fermate, 13.158 corse di un feriale del GTFS; «poco TP» = accessibilità (fermate vicine
  con buon servizio), non bus che passano sulla strada.

## Controllo di buon senso

Un giudizio qualitativo di una persona che conosce la città (strade A = molto trafficate, B = medie, C = tranquille) è
usato solo come controllo, mai per tarare il modello: 11 strade su 18 nella fascia giusta, 5 confronti su 7. Regole
che ne vengono: un corso cambia nome lungo il percorso (Trapani → Lecce → Potenza; Agudio → Sturzo), l'asse non si
ferma al confine comunale; a parità di traffico una strada a due corsie sente meno pressione di una a una corsia; il
centro-centro non è prioritario. Il modello **sottovaluta** il semicentro (Bolzano, Quintino Sella, Lombardia, Re
Umberto, Vittorio Emanuele II) e **sopravvaluta** raccordi e strade corte (Palestrina, Monte Lungo, Quarto dei Mille);
ai sensori corso Unione Sovietica è +177% e corso Sebastopoli +99%.

## L8 (24/10/2026): TomTom è la stima principale

**Decisione di Leo, presa dopo aver visto i numeri di L6bis:** i tempi in auto si prendono da TomTom; la stima dei sensori 5T resta come «stima più favorevole all'auto» (non conta semafori e incroci). La scelta è motivata dal **difetto di metodo provato** (la nostra rete va ai limiti di velocità, senza semafori), non dai risultati. Le regole sono state fissate prima dei numeri nuovi (blocco L8 di `sviluppo/piani/PROMPT_LAVORI.md`) e non sono state cambiate dopo averli visti.

- **Auto** = nostro flusso libero × `fattore_rete` TomTom + 5 minuti. Il fattore è quello **del percorso stesso** quando è stato chiesto a TomTom; per le coppie di zone non chieste, la **mediana delle coppie TomTom della stessa ora e della stessa fascia di flusso libero** (terzili del nostro flusso libero fra le coppie TomTom di quell'ora). Area che si espande: fattore della zona (Piazza Castello → punto di maggior peso della zona, alle 8). Sensori: stessa formula col fattore 5T, solo come sensibilità.
- **Richieste** (`scripts/101_tempi_traffico.py --estendi`, martedì 10/11/2026, ore italiane): C1 coppie 101-600 alle 8:00 (500), C2 coppie 101-300 alle 13:00, 17:30 e 21:00 (600), D Piazza Castello → ognuna delle **71 zone con punti** (il blocco ne diceva 101: le altre zone sono rappresentate solo da «porte» e non hanno un punto di calcolo). In tutto **1.171 richieste nuove** (tetto bloccante 2.000), nessun rifiuto di TomTom; con le 1.200 di L6bis sono 2.371. Si salvano solo rapporti a 2 decimali per percorso, mai i minuti né le risposte.
- **Quante auto hanno il fattore del proprio percorso:** alle 8, 600 coppie su 2.061 (**83,2% delle auto**); alle altre ore 300 coppie (circa 60% delle auto). Tutti i 17 luoghi del R6 e tutte le 23 zone di Torino dell'area hanno il proprio fattore.
- **Controllo di coerenza** (100 coppie di L6bis, solo martedì contro media dei due giorni): differenza mediana 08:00 0,009, 13:00 0,007, 17:30 0,007, 21:00 0,003, tutte sotto 0,05: nessun AVVISO.
- Mediana di `fattore_rete` TomTom: coppie 101-600 alle 8 **2,14** (le prime 100: 2,45); zone da Piazza Castello **1,88**; punti in entrata 2,59.
- Numeri (alle 8): rapporto mediano coi mezzi pubblici **1,85** con TomTom (2,94 con i sensori), pesato per le 220.307 auto; auto con rapporto oltre 2: **35,4%** con TomTom, 97,0% con i sensori. Titolo della scheda: «Al mattino, coi mezzi pubblici si impiega 1,9 volte il tempo dell'auto» (la regola ±0,3 delle 4 ore, applicata alla sola stima TomTom, non scatta: alle 21:00 il rapporto è 2,30, 0,45 sopra quello delle 8).
- Area che si espande (Piazza Castello, 30 minuti): mezzi 42,2% dei torinesi, auto 90,1% con TomTom (100,0% con i sensori).
- Limite scritto nelle schede: «Tempi in auto previsti da TomTom su traffico tipico di un feriale di novembre, non misurati in un giorno preciso.» Un solo servizio.

## Noi contro Google Maps

**Due stime, non un minimo e un massimo.** Il tempo in auto non conta semafori e incroci, quindi il fattore di punta è incerto. Il risultato è **dato con due stime**:
la **stima con il rallentamento dei sensori** usa il fattore dei sensori 5T (1,2: mediana di velocità 2-5 / velocità alle 8 su 97 sensori);
la **stima con il rallentamento di TomTom** (dal 24/10; prima era quella di Google) usa il fattore del servizio di percorsi TomTom (2,45: mediana dei 100 viaggi con più auto del mattino, alle 8; script 101):
tempo previsto da TomTom col traffico tipico / **nostro** tempo a flusso libero dello stesso percorso. Stessa grandezza del 2,1 di Google (che era (tempo Google − 5) / nostro flusso libero, mediana di 6 percorsi controllati a mano il 20/10).
**Cosa misura ognuna.** Il nostro flusso libero viene dalla rete OSM ai limiti di velocità, **senza semafori e incroci**: è troppo veloce (Corso Racconigi → Piazza Castello: 6,4 minuti; Google alle 8: 29). Il fattore di TomTom e quello di Google correggono insieme la rete troppo veloce **e** il traffico. Il fattore dei sensori 5T (1,2) è solo il traffico: non conta semafori e incroci ed è la stima più favorevole all'auto.
TomTom è un tempo previsto su traffico tipico (partenze del 10 e 11/11/2026, media dei due giorni), **non misurato**; un solo servizio. Dati di traffico: TomTom. I minuti e le risposte grezze non sono salvati: solo i rapporti per gruppo e ora (`data/processed/tempi_traffico.json`).
Le due stime non sono un minimo e un massimo: **il valore vero può stare anche fuori**.

**Correzione del 24/10, decisa dopo aver visto lo STOP del primo controllo.** La regola di L6 diceva: fattore di TomTom = tempo col traffico / tempo TomTom senza traffico (la «congestione»). Sui 6 percorsi in uscita alle 8 dava **1,26** contro il 2,1 di Google e il controllo si è fermato (soglia 0,5). Non era un disaccordo fra le fonti ma un errore della regola: la congestione è solo traffico, il 2,1 comprende anche la rete troppo veloce. Si è confrontata la stessa grandezza (tempo TomTom / nostro flusso libero): **1,98** contro 2,1 (entro la soglia di 0,5, regole e soglie invariate). La congestione di TomTom resta nel file, da confrontare coi sensori 5T (1,26 alle 8 contro 1,2).

Controllo con TomTom, alle 8:00 (media del 10 e 11/11/2026), contro il 2,1 di Google (per percorso: (tempo Google − 5) / nostro flusso libero):

| Percorso | TomTom, tempo / nostro flusso libero | TomTom, congestione (con / senza traffico) | Google (a mano, 20/10) |
|---|---|---|---|
| Piazza Castello → Collegno | 2,40 | 1,37 | 1,1 |
| Piazza Castello → Venaria Reale | 2,07 | 1,26 | 2,0 |
| Piazza Castello → Settimo Torinese | 1,95 | 1,27 | 2,3 |
| Piazza Castello → Moncalieri | 1,87 | 1,21 | 2,5 |
| Piazza Castello → Orbassano | 1,97 | 1,17 | 2,2 |
| Piazza Castello → Rivoli | 1,98 | 1,51 | 1,8 |
| Corso Racconigi → Piazza Castello | 3,00 | 1,28 | (29 minuti: 3,6 con la stessa formula) |
| **mediana dei 6 in uscita** | **1,98** | 1,26 (sensori: 1,2) | **2,1** |

TomTom è più uniforme di Google fra i percorsi (1,87-2,40 contro 1,1-2,5): Google a mano è un solo giorno e un solo tentativo per percorso. In entrata (17 percorsi dai punti del R6) la mediana è **2,59** (25°-75° percentile 2,42-2,73), più alta che in uscita (1,26 di congestione in uscita contro 1,39 in entrata).

Controllo a mano, **martedì 20/10/2026 alle 8:00**. I primi 6 percorsi partono da Piazza Castello; gli ultimi 2 sono di controllo. Tempi in minuti.

| Percorso | Mezzi pubblici, nostri | Mezzi pubblici, Google | Auto, nostra (stima sensori, fattore 1,2) | Auto, nostra (fattore Google 2,1) | Auto, Google |
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
- **Auto**: con la stima dei sensori (fattore 1,2) siamo sotto Google di 11,4 minuti in media (sui 6 percorsi); con il fattore di Google (2,1) di 1,7 (differenza media, nostro meno Google); con quello di TomTom (2,45) l'auto è più lenta ancora. Sono due stime: il valore vero può stare anche fuori.
- Rapporto mediano coi mezzi pubblici (Torino-Torino e Torino-cintura): **1,85** con TomTom per percorso (L8; con TomTom a fattore unico, L6bis: 1,75; con Google: 1,96) e 2,94 con i sensori.

### Stima TomTom e stima dei sensori: rapporto mediano e fasce (Torino-Torino e Torino-cintura, 220.307 auto)

Fasce fisse del rapporto (tempo coi mezzi / tempo in auto). Il metodo è cambiato 4 volte il 21/10 dopo le prime prove; le fasce sono state scelte dopo. Celle: auto (% delle auto).

| Stima | Fattore | Rapporto mediano | Oltre 2 | sotto 1,5 | 1,5-2 | 2-3 | oltre 3 |
|---|---|---|---|---|---|---|---|
| **Stima TomTom (fattore: mediana dei fattori applicati)** | 2,23 | **1,85** | 35,4% | 28.510 (12,9%) | 113.791 (51,7%) | 73.728 (33,5%) | 4.278 (1,9%) |
| **Stima più favorevole all'auto (sensori 5T)** | 1,20 | **2,94** | 97,0% | 0 (0,0%) | 6.661 (3,0%) | 115.033 (52,2%) | 98.612 (44,8%) |

Per gruppo (mediano e quota oltre 2: stima TomTom | stima dei sensori). Cintura-cintura è a parte: mancano treni e altre aziende.

| Gruppo | Mediano basso | Mediano alto | Oltre 2 basso | Oltre 2 alto |
|---|---|---|---|---|
| (a) Torino-Torino | 1,69 | 2,78 | 14,5% | 93,5% |
| (b) Torino-cintura (e cintura-Torino) | 2,03 | 3,07 | 53,8% | 100,0% |
| (ab) principale: Torino-Torino e Torino-cintura | 1,85 | 2,94 | 35,4% | 97,0% |
| (c) cintura-cintura | 2,22 | 3,49 | 62,9% | 100,0% |

### Non solo all'ora di punta: 4 ore del giorno (script 100, 23/10)

Stesso confronto alle 8:00, 13:00, 17:30 e 21:00 di un feriale (partenza 7:45, 12:45, 17:15, 20:45, finestra di 30 minuti, mediana). Auto = flusso libero × fattore dell'ora + 5 minuti.
Stima dei sensori = rallentamento misurato dai sensori 5T (mediana di velocità 2-5 / velocità all'ora); stima di TomTom = fattore_rete mediano di TomTom per ogni ora (gruppo «coppie» per le coppie di zone del R8, «entrata» per i punti del R6): non c'è più nessuna ipotesi di scala. (Fino al 23/10 la stima era quella di Google, noto solo alle 8 e **scalato** nello stesso rapporto dei sensori con `1 + 1,1 × (f(h) − 1) / 0,2`, mai sotto 1: un'ipotesi, ora sostituita.) Regola del titolo fissata prima (blocco L3): «a ogni ora» solo se il rapporto mediano resta entro ±0,3 da quello delle 8 con tutte e due le stime (dal giro L8 si applica alla sola stima TomTom; non è il caso: alle 21:00 la differenza dalle 8 è oltre 0,3).

| Ora | Fattore sensori | Fattore TomTom, mediana applicata (punti del R6) | Rapporto mediano (stima TomTom - stima sensori) | Auto con rapporto oltre 2 | Auto senza collegamento |
|---|---|---|---|---|---|
| 8:00 | 1,2 | 2,23 (punti: 2,59) | 1,85 - 2,94 | 35% - 97% | 5.616 |
| 13:00 | 1,1 | 1,89 (punti: 2,27) | 2,10 - 3,10 | 58% - 98% | 4.810 |
| 17:30 | 1,2 | 2,15 (punti: 2,66) | 1,92 - 3,02 | 41% - 97% | 6.095 |
| 21:00 | 1,0 | 1,71 (punti: 1,88) | 2,30 - 3,32 | 74% - 100% | 9.511 |

Di giorno e di sera l'auto è più veloce (meno traffico) e i mezzi restano lenti: il rapporto sale. Alle 8 i numeri coincidono con quelli degli script 93 e 94 (controllo dello script 100).
Rifare: `python scripts/100_ore_del_giorno.py` (circa 3-4 minuti dopo 93 e 94; `--campione 10` e `--prova` per provare); è nella fase «r6» di `rifai_tutto.py`.

## Limiti

- Stima debole; senza un sensore sull'asse la classifica mette in cima strade poco credibili (corso Dogliotti circa
  58.500): nella scheda si mostrano solo strade con un sensore sull'asse.
- 22 punti di misura, tutti fra circa 9.000 e 106.500 veicoli/giorno; a Torino sensori a un solo verso (×2 per i due
  versi); la notte è inaffidabile e l'ora di punta non è validata.
- Domanda IMQ 2022: solo residenti 11-84 anni, feriale medio; mancano merci, turisti, pendolari da fuori.
- TP programmato: niente ritardi né affollamento. Il centro (ZTL, pedonali) non è stimato bene.
- Il rallentamento dei sensori è misurato; quello di TomTom è un tempo previsto su traffico tipico (due giorni feriali di novembre, un solo servizio), non misurato. La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto. Un solo giorno di GTFS (12/10).
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
| 101 | fattori di rallentamento dell'auto da TomTom (rete e congestione, per gruppo e ora) → `tempi_traffico.json`; **non è in `rifai_tutto.py`**: usa la chiave in `config_locale.json`, ~1.200 richieste, e il file è in git; si rilancia a mano (`python scripts\101_tempi_traffico.py`) |
| 100 | lo stesso confronto a 4 ore del giorno (8, 13, 17:30, 21) → `ore_del_giorno.json` |
| 93 | tempo coi mezzi contro auto fra zone IMQ: due stime con due fattori di punta → `tp_contro_auto.json` (si rifà in circa 1 minuto) |
| 99 | «area che si espande» (scheda 4): da Piazza Castello a ogni sezione di Torino, coi mezzi (r5py) e in auto (rete del modello, gli stessi due fattori del 93); zona-zona di Torino ricopiata dal 93 → `area_tempi.json` → `data/area_tempi.js` (`scripts\AREA_TEMPI.bat`; `--finto` per provare la pagina senza dati) |

Risultato: `data/processed/risultato8_traffico_tp_v2.json` (universo, assi da guardare, tratte); dettaglio per tratta in
`data/processed/traffico_d/tratte_traffico.json`; valutazione in `traffico_d/valutazione_fase5.json`.

```
scripts\FETCH_LEOPI_E_VELOCITA_5T.bat      (dopo ogni raccolta dal Pi)
scripts\TRAFFICO_RILANCIA_SENSORI.bat      (riscrive anche i rapporti)
python scripts\62_v4_modello.py --variante v4 --iter 8 --outdir v4     (solo se cambiano rete o GTFS; lungo, circa 1 ora)
python scripts\63_v4_valutazione.py
```
Le varianti di confronto (`--variante v0`, `abl1`, `abl2`, `abl3`, con `--outdir` uguale al nome) si rifanno allo stesso modo prima del 63;
lo stato `msa_stato.npz` di una variante si cancella (cartella `data\processed\traffico_d\<variante>`) per rifare da capo.

```
python scripts\schede_risultati.py
```

Da fare: controllo a mano della copertura TP di corso Moncalieri; `velocita_5t.json` al posto del «tipico» di
`data/stat.js` nella mappa (quello calcolato sul Pi non scarta le letture inaffidabili); aggiungere unità di confronto
dopo alcuni feriali con i codici sensore corretti; cambio dell'ora legale del 25/10 da controllare nello script 26.
