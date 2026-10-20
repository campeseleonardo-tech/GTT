# Esito R6 - proposta fermate importanti con regola fissa (20/10/2026)

Script: scripts/89_proposta_fermate_importanti.py (solo lettura; non cambia lo script 83 né i risultati).
Rapporto: docs/RAPPORTO_R6_PROPOSTA_FERMATE.txt. Nota: nel piano non c'è una sezione «Esito del prompt A»; ho
usato l'esito di docs/ESITO_R6_SENSORI.md e le «Decisioni di Leo».

Scelte dichiarate: universo = i 3.898 eleggibili dello script 83; b2 da segnali.json e c4 da auto_passaggio.json
(come nello script 83); metro/stazione/capolinea da nodi.json; i punti prioritari (mappa_r6.json) citano le fermate
per nome (senza «Fermata N -»): le ho collegate ai luoghi per nome entro 3 km dal loro centro. Controllo: con la lista
di oggi tutti i 15 punti risultano collegati (15 su 15).

## Uscita completa

```
  OK     esiste luoghi.json
  OK     esiste segnali.json
  OK     esiste auto_passaggio.json
  OK     esiste nodi.json
  OK     esiste fermate_importanti.json
  OK     esiste mappa_r6.json
  OK     esiste imq_zone.json
  OK     eleggibili = quelli dello script 83 — 3898 vs 3898
  OK     le importanti di oggi sono tutte fra gli eleggibili
  OK     nodi.json copre tutti gli eleggibili — 0 mancanti
  OK     nessun valore negativo
  OK     ogni punto prioritario di oggi ha una fermata fra le importanti di oggi (il collegamento per nome funziona) — 15 su 15
RAPPORTO R6 - PROPOSTA PER LE FERMATE IMPORTANTI CON REGOLA FISSA (script 89, solo lettura)

Eleggibili 3898 (Torino fuori da Q001-Q009 1146, cintura 1259, resto CMTO 1493).
Fermate importanti oggi (script 83, punteggio, 10%): 391. Punti prioritari oggi: 15.
Regola proposta: (metro o stazione o capolinea, oppure corse/ora b2 >= N) e auto che passano c4 >= M.

== Distribuzioni sugli eleggibili ==
corse/ora pendolari b2 (media ore 6-10 e 16-20 feriale):
  tutti:    p10=0.4  p25=0.9  p50=2.6  p75=6.2  p90=10.8  p95=14.6  p99=24.8  max=89.8
  solo > 0: p10=0.4  p25=1.0  p50=2.8  p75=6.4  p90=10.8  p95=14.8  p99=25.0  max=89.8  (3834 fermate)
auto in entrata che passano accanto c4:
  tutti:    p10=0.0  p25=0.0  p50=48.0  p75=684.0  p90=2616.6  p95=3933.7  p99=7267.2  max=13119.0
  solo > 0: p10=50.8  p25=181.0  p50=574.0  p75=1765.0  p90=3840.4  p95=4944.9  p99=7830.0  max=13119.0  (2159 fermate)
metro: 7; stazione (ferro entro 300 m): 88; capolinea: 54; almeno uno dei tre: 142 (fra le importanti di oggi: 75 su 391)
Importanti di oggi:
  b2: p10=5.4  p25=8.0  p50=10.6  p75=15.8  p90=23.0  p95=28.9  p99=42.4  max=89.8
  c4: p10=846.0  p25=1905.0  p50=3006.0  p75=4447.0  p90=6920.0  p95=7408.0  p99=11731.0  max=13119.0

== Griglia N (corse/ora) x M (auto che passano) ==
Importanti di oggi a nord-ovest (lat > 45,0703 e lon < 7,6869): 93 su 391

  N     M |   tot Torino cint. resto | restano nuove nuove NO tot NO | punti prioritari con >=1 fermata
 10   500 |   347    249    97     1 |     233   114       31     92 | 12 su 15
 10  1000 |   274    205    68     1 |     211    63       22     78 | 12 su 15
 10  2000 |   201    170    31     0 |     177    24        8     51 | 10 su 15
 10  3000 |   127    116    11     0 |     123     4        2     34 |  9 su 15

 15   500 |   180    136    43     1 |     138    42       13     44 |  9 su 15
 15  1000 |   136    110    25     1 |     118    18        8     34 |  9 su 15
 15  2000 |   108     97    11     0 |     100     8        2     21 |  8 su 15
 15  3000 |    75     68     7     0 |      73     2        1     17 |  6 su 15

 20   500 |   114     79    34     1 |      92    22        6     28 |  5 su 15
 20  1000 |    83     65    17     1 |      74     9        4     21 |  5 su 15
 20  2000 |    64     57     7     0 |      59     5        0     11 |  4 su 15
 20  3000 |    46     41     5     0 |      45     1        0      9 |  3 su 15

 30   500 |    70     41    28     1 |      58    12        3     23 |  3 su 15
 30  1000 |    48     34    13     1 |      42     6        2     17 |  3 su 15
 30  2000 |    34     29     5     0 |      30     4        0      9 |  2 su 15
 30  3000 |    25     21     4     0 |      24     1        0      8 |  1 su 15

Colonne: tot = fermate importanti con la regola (Torino / cintura / resto della Citta' metropolitana);
restano = delle importanti di oggi, quante ci sono ancora; nuove = non erano importanti oggi;
nuove NO = fra le nuove, quelle a nord-ovest di piazza Castello; tot NO = tutte quelle a nord-ovest;
punti prioritari = quelli di oggi (mappa_r6.json) con almeno una loro fermata nella lista.
Un punto prioritario e' collegato alle fermate per nome, a meno di 3 km dal suo centro.

== Controlli ==
  OK     esiste luoghi.json
  OK     esiste segnali.json
  OK     esiste auto_passaggio.json
  OK     esiste nodi.json
  OK     esiste fermate_importanti.json
  OK     esiste mappa_r6.json
  OK     esiste imq_zone.json
  OK     eleggibili = quelli dello script 83 — 3898 vs 3898
  OK     le importanti di oggi sono tutte fra gli eleggibili
  OK     nodi.json copre tutti gli eleggibili — 0 mancanti
  OK     nessun valore negativo
  OK     ogni punto prioritario di oggi ha una fermata fra le importanti di oggi (il collegamento per nome funziona) — 15 su 15

Scritto docs\RAPPORTO_R6_PROPOSTA_FERMATE.txt; avvisi: 0
```
