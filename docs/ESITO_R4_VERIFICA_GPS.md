# Esito R4 - verifica della regola D3 con il GPS (Giro 3, 21/10/2026)

Partenza: ramo `prova`, pulito, `git pull` ok. D3 e le altre regole D1-D9 **non cambiate**; database aperto in sola lettura; `MEMORIA_PROGETTO.md` non toccata.
Nota: la sezione «Ricontrollo del Giro 2» e il Giro 3 erano già in `prova`.

## Riepilogo
| Passo | Esito |
|---|---|
| 1. Script 90 (verifica col GPS) | OK, nessun AVVISO; **risultato importante, vedi sotto** |
| 2. Classifica «ritardo a fine corsa» per minuti di ritardo | OK |
| 3. Link `&ora=8` e `ora=` nell'indirizzo della mappa | OK, provato nel browser |
| 4. Lanci 90 → 27 → 70 → 04 → schede → prova pagine | OK, 0 errori su 13 pagine |

## Risultato della verifica (2 feriali: 15 e 16/10; 455.118 passaggi con orario nel GTFS)
Il feed GTT **smette di elencare la fermata all'orario programmato** (gruppo C: ultima lettura meno orario programmato, mediana −0,6 min).
Per un mezzo in ritardo l'ultima lettura è quindi lontana dall'arrivo vero e D3 la scarta: i ritardi lunghi non entrano mai nei conti.

| Gruppo | Passaggi | Nel campione | Con GPS | Ritardo vero ≤5 | 5-10 | >10 |
|---|---|---|---|---|---|---|
| A usati, feed fino a 5 min | 406.631 | 2.991 | 2.426 | 91,7% | 6,8% | 1,6% |
| B usati, feed oltre 5 min | 25.790 | 2.879 | 2.000 | 6,7% | 37,2% | 56,0% |
| C scartati (D3) | 22.697 | 2.865 | 1.618 | 30,6% | 3,2% | 66,2% |

Ritardo vero mediano: A −0,2 min, B +10,7, C +16,6. Differenza mediana stima del feed − GPS: A −0,4 min, B −4,0, C −5,1 (il feed **sottostima** i ritardi
anche fra gli usati). Per modo, gruppo C: tram 385 con GPS (71,9% oltre 10 min), bus 1.233 (64,4%).

| Stima, % dei passaggi in ritardo | oggi (solo usati) oltre 5 | oggi oltre 10 | corretta oltre 5 | corretta oltre 10 |
|---|---|---|---|---|
| Tutti | 5,96% | 0,00% | **9,13%** | **3,30%** |
| Tram | 5,97% | 0,00% | 11,12% | 5,40% |
| Bus | 5,96% | 0,00% | 8,68% | 2,82% |

«Corretta» = usati come oggi + scartati con il ritardo vero del GPS (frazione misurata sul campione con GPS valido, pesata per tutti gli scartati).
L'oltre 10 minuti corretto (3,3%) è dello stesso ordine del 2,3% di GTT 2025. Il 5,96% «oggi» è sui 2 giorni (il titolo su 7 feriali è 5,2%).
Limiti: campione a passo fisso di 3.000 per gruppo (1.500 per giorno); GPS valido = a meno di 60 m dalla fermata; scartati i passaggi GPS con ritardo
oltre 60 minuti in valore assoluto (corrispondenze sbagliate, regola aggiunta da me e dichiarata nello script); la correzione non copre il gruppo B (anche lì il feed sottostima).
Da decidere con Leo: se e come cambiare D3 (per esempio usare l'ultima lettura anche se lontana quando il ritardo è già grande, o integrare il GPS).

## Passo 1 - scripts/90_verifica_ritardi_gps.py (nuovo, sola lettura)
Carica 27 e 70 con `comuni.carica_script`; usa `carica_gtfs()` (6 valori), `leggi_giorno()`, `costruisci_passaggi()` (per il controllo), `carica_calendario()` e
`mezzanotte_utc()`/`metri()` del 70. La logica di `controllo_gps()` (passaggio più vicino a una fermata, segmenti ≤ 180 s, 60 m) è copiata in
`ora_gps_vicino()`, che lavora su un passaggio alla volta. `passaggi_con_scartati()` rifà D2-D5 tenendo gli scartati. Tabella `mezzi_gtt`: colonne
`letto_utc, ts_feed, veicolo, linea, corsa, lat, lng` (come nel piano; la corsa è presente per quasi tutte le righe del 15 e 16/10). Controlli: A + B
uguali ai passaggi usati dello script 27 (432.421 contro 432.421) OK; 2 giorni feriali di dimensione simile OK; gruppo C con GPS valido 1.618 (≥ 300) OK;
tram 385 e bus 1.233 (≥ 30) OK. Rapporto: `docs/RAPPORTO_R4_VERIFICA_GPS.txt`. Durata ≈ 46 s.

## Passo 2 - classifica del ritardo a fine corsa
- `27_risultato4_regolarita.py`, rapporto: ordinata per `ritardo_mediana` (minuti) invece che per minuti ogni 10 km; colonne: ritardo, km corsa, min ogni 10 km, passaggi.
- `schede_risultati.py`: grafico «Ritardo a fine corsa (feriale)», valore = ritardo mediano; i minuti ogni 10 km nell'etichetta di ogni barra e nella nota; frase inglese adattata.
- Prima (per km): 6, 19, 60. Dopo (per minuti): **6 (1,2 min), 17 (1,2), 19 (1,1)**, poi 60, 132, 33, 74, 76, 72, 61. La 17 (corsa 17,4 km) entra al secondo posto.

## Passo 3 - link alla mappa alle 8
- Template, `applicaLineaDaUrl()`: legge `ora=<0-23>`; se c'è, preme il pulsante feriale e porta lo slider a quell'ora (`S.m = ora*60; aggiornaOra()`), poi ridisegna e aggiorna la legenda.
  (Il piano diceva solo di impostare l'ora; ho aggiunto il pulsante feriale perché la mappa potrebbe aprirsi su sabato/domenica.)
- `link_linea()`: aggiunge `&ora=8`; nota del grafico: «la mappa si apre alle 8 di un feriale».
- Provato: `#tema=puntualita&linea=17&ora=8` → tema Puntualità, campo linea «17», feriale, 08:00, legenda «punta del mattino (7-9)».

## Passo 4 - lanci
90 → 27 → 70 → 04 → schede → `prova_pagine_r6.py --senza-screenshot`: tutti con uscita 0; **0 errori su 13 pagine** (nessun identificatore non definito).
Il rapporto R4 nuovo inizia con il testo di prima identico (aggiunte solo in coda). `mappa_torino.html` 13.783.398 byte.

## Uscita completa dello script 90
```
  OK     20261015 e' un giorno feriale
  OK     20261016 e' un giorno feriale
  OK     passaggi usati (A + B) uguali a quelli dello script 27 nei 2 giorni — 432421 contro 432421
  OK     i due giorni hanno righe di trip_update simili (almeno 70% del maggiore) — 20261015: 379307, 20261016: 376418
  OK     almeno 300 passaggi con GPS valido nel gruppo C — 1618 su 2865 del campione
  OK     gruppo C con GPS valido, tram: almeno 30 — 385
  OK     gruppo C con GPS valido, bus: almeno 30 — 1233
RAPPORTO R4 - VERIFICA DELLA REGOLA D3 CON IL GPS (script 90, solo lettura)
======================================================================
Giorni feriali: 20261015, 20261016. Gruppi: A = usati, ritardo del feed fino a 5 min; B = usati, ritardo del feed oltre 5 min; C = scartati per lettura lontana (D3).
Campione a passo fisso: al massimo 3000 passaggi per gruppo in tutto (1500 per giorno).
GPS valido: stessa corsa a meno di 60 m dalla fermata, segmenti di non piu' di 180 s; ritardo vero = passaggio GPS - orario programmato; scartato se oltre 60 min in valore assoluto.

PER GRUPPO
gruppo | passaggi (2 giorni) | nel campione | con GPS valido | ritardo vero: <=5 min | 5-10 min | >10 min | mediana (min) | stima feed - GPS, mediana (min)
A      |              406631 |         2991 |           2426 |                  91.7% |      6.8% |     1.6% |          -0.2 | -0.4
B      |               25790 |         2879 |           2000 |                   6.7% |     37.2% |    56.0% |          10.7 | -4.0
C      |               22697 |         2865 |           1618 |                  30.6% |      3.2% |    66.2% |          16.6 | -5.1

PER MODO (gruppo C e confronto)
gruppo modo | passaggi | con GPS valido | ritardo vero: <=5 | 5-10 | >10
A      tram |    76263 |            481 |             91.1% |  7.3% |  1.7%
A      bus  |   330368 |           1945 |             91.8% |  6.6% |  1.5%
B      tram |     4839 |            335 |              6.0% | 24.5% | 69.6%
B      bus  |    20951 |           1665 |              6.8% | 39.8% | 53.3%
C      tram |     6586 |            385 |             25.5% |  2.6% | 71.9%
C      bus  |    16111 |           1233 |             32.2% |  3.4% | 64.4%

GRUPPO C - ultima lettura meno orario programmato (minuti; negativo = lettura prima dell'orario)
  tutto il campione C: p10 -1.1, p25 -0.9, p50 -0.6, p75 -0.3, p90 -0.1
  solo C con GPS valido: p10 -1.1, p25 -0.9, p50 -0.6, p75 -0.3, p90 -0.1
  ultima lettura meno passaggio GPS (C con GPS): p10 -32.0, p25 -23.4, p50 -17.2, p75 -0.3, p90 11.6
  ritardo del feed (C con GPS): p10 -12.5, p25 9.6, p50 11.4, p75 14.4, p90 19.5
  ritardo vero (C con GPS): p10 -12.3, p25 -0.8, p50 16.6, p75 22.8, p90 31.7

STIMA CORRETTA (2 giorni feriali, % dei passaggi in ritardo)
  corretta = passaggi usati come oggi (ritardo del feed) + scartati per lettura lontana con il ritardo vero del GPS (frazione misurata sul campione con GPS valido, pesata per tutti gli scartati)
modo  | usati | scartati | GPS validi (C) | oggi: oltre 5 | oggi: oltre 10 | corretta: oltre 5 | corretta: oltre 10
tutti | 432421 |    22697 |           1618 |         5.96% |         0.00% |             9.13% |             3.30%
tram  | 81102 |     6586 |            385 |         5.97% |         0.00% |            11.12% |             5.40%
bus   | 351319 |    16111 |           1233 |         5.96% |         0.00% |             8.68% |             2.82%
  scartati per lettura lontana: 22697 su 455118 passaggi con orario nel GTFS (5.0%)

Letture: la stima corretta e' un controllo con un dato indipendente, non cambia la regola D3 ne' i risultati; la decisione e' di Leo.

CONTROLLI
  OK     20261015 e' un giorno feriale
  OK     20261016 e' un giorno feriale
  OK     passaggi usati (A + B) uguali a quelli dello script 27 nei 2 giorni — 432421 contro 432421
  OK     i due giorni hanno righe di trip_update simili (almeno 70% del maggiore) — 20261015: 379307, 20261016: 376418
  OK     almeno 300 passaggi con GPS valido nel gruppo C — 1618 su 2865 del campione
  OK     gruppo C con GPS valido, tram: almeno 30 — 385
  OK     gruppo C con GPS valido, bus: almeno 30 — 1233

Scritto docs\RAPPORTO_R4_VERIFICA_GPS.txt; avvisi: 0
```
