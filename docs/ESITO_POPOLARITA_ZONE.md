# Esito popolarità delle zone e linee utili (script 87, 20/10/2026)

Script: scripts/87_popolarita_zone.py (solo lettura dei dati). Scrive data/processed/popolarita_zone.json e
docs/RAPPORTO_POPOLARITA_ZONE.txt. Non ho toccato altri script né i risultati.

## Scelte e differenze dal piano (da guardare)
- File e colonne come nel piano (spostamenti.csv `;`, COD_ARR, SCOPO, PESO; imq_zone_geo.json; parcheggi_adatti.json).
  Il file dei parcheggi adatti non ha le coordinate: le prendo da parcheggi.json (stesso id). Zone e fermate: punto in
  poligono con le funzioni dello script 72.
- **La classifica delle zone è solo sulla Città metropolitana** (macro Torino, Cintura, Resto CMTO, come nel resto del
  Risultato 6). La prima versione metteva in cima Novara, Alessandria, Asti, Biella, Vercelli (fuori dalla rete GTT):
  restano nel file con `in_universo = false`, ma non entrano nelle 20 zone «più popolari».
- Popolarità = totale degli arrivi (senza ritorni a casa). Servizi ed esercizi sono mostrati a parte e **non sommati**:
  dentro Torino vengono dal catalogo comunale, fuori da OpenStreetMap (scuole, salute, cibo: incompleto), non sono
  confrontabili. «Servizi» = istruzione, salute, servizi comunali, impianti sportivi, mercati tematici, luoghi, musei,
  biblioteche, cinema; «esercizi» = attività commerciali (sono 31.271 e peserebbero da sole più di tutto il resto).
- Linea = route_short_name; «linea più lunga» = più fermate distinte. Linee utili = 25% con (a) più alto, a pari (a)
  conta (b); la soglia di (a) cade su un gruppo di linee a pari valore e (b) decide chi entra (vedi controlli).
- 165 punti del catalogo comunale cadono in zone della cintura (soprattutto Moncalieri e Grugliasco): sono contati lì,
  e lì si sommano anche ai punti OSM (possibile doppio conteggio, piccolo).
- Il piano dice «dalle 20 zone più popolari»: per «tocca» conta la fermata dentro la zona (30 fermate su 7.043 non
  stanno in nessuna zona IMQ e non contano).

## Uscita completa

```
  OK     esiste spostamenti.csv
  OK     esiste imq_zone.json
  OK     esiste servizi_osm_cintura.json
  OK     esiste gtt_gtfs_20261003_224530.zip
  OK     esiste parcheggi_adatti.json
  OK     esiste parcheggi.json
  OK     esiste istruzione.json
  OK     nessuna zona senza nome
  OK     poligoni per tutte le zone — 212 poligoni, 212 zone
1. arrivi dell'IMQ per zona di arrivo e scopo...
  OK     arrivi + ritorni a casa esclusi = totale spostamenti IMQ (stesso peso) — arrivi 4,444,360 + ritorni 3,714,050 + senza zona 59,452 + zona non nell'elenco 0 + scopo non classificato 0 = 8,217,863
  OK     spostamenti senza zona di arrivo, zona sconosciuta o scopo non classificato sotto l'1% — senza zona 59,452, zona sconosciuta 0, scopo non classificato 0
  OK     ritorni a casa esclusi sono una parte rilevante degli spostamenti — 45%
   servizi per zona (catalogo comunale dentro Torino, OSM fuori)...
  OK     punti del catalogo fuori da ogni zona IMQ — servizi 0, esercizi 0
  AVVISO punti OSM della cintura fuori da ogni zona IMQ — 1
  AVVISO punti del catalogo comunale in zone fuori Torino (atteso 0: il catalogo e' di Torino) — 165 punti in C002 (50), C003 (2), C004 (1), C007 (13), C009 (96), C011 (1), C066 (2)
  OK     somma degli arrivi per zona = arrivi contati
  OK     zone senza nessun arrivo nell'IMQ — 0 su 212
   zone 212; arrivi 4,444,360; ritorni esclusi 3,714,050
2. linee GTT (GTFS): zone toccate...
   fermate 7045; linee (route_short_name) 215
  OK     linee nel GTFS > 50 — 215
  AVVISO fermate usate dalle linee fuori da ogni zona IMQ — 30 su 7043 (non contano per nessuna zona)
   linee utili 54 (25% di 215); punteggio (a) di soglia 4
  OK     (a) non e' uguale per tutte le linee
  OK     linee con (a) uguale a quello di soglia (decide (b)) — 25 linee con (a) = 4, di cui 22 utili
  OK     le 10 linee piu' lunghe (per fermate) NON sono tutte fra le prime 15 per (a) — 0 su 10 sono fra le prime 15 (lunghe: 3107, 3006, 2014, 2172, 4512, 5137, 1510, 3106, 4108, 90)
3. parcheggi adatti: linee utili entro 400 m a piedi...
  OK     tutti i parcheggi adatti hanno coordinate — 1874 adatti
  AVVISO parcheggi adatti senza nessuna linea entro 400 m a piedi — 495 su 1874
  AVVISO parcheggi adatti senza nessuna linea utile entro 400 m a piedi — 1123 su 1874
RAPPORTO - POPOLARITA' DELLE ZONE E LINEE GTT UTILI (script 87)

Popolarita' = spostamenti IMQ che ARRIVANO nella zona, ritorni a casa (scopi 08, 11) esclusi: 4,444,360 su 8,217,863 (peso IMQ); ritorni esclusi 3,714,050.
Gruppi: lavoro/studio (01,02,03); acquisti/cure/svago (04,06,07); altro (05,09,10,12,13,14,15,16).
Servizi ed esercizi sono mostrati a parte e non sommati agli arrivi: dentro Torino vengono dal catalogo comunale, fuori da OpenStreetMap (dato meno completo): non sono confrontabili fra dentro e fuori Torino.
Linee GTT: 215 (route_short_name, tutte le corse, due direzioni insieme); fermate nel GTFS 7045.
Linea utile = 25% piu' alto per (a) = quante delle 20 zone piu' popolari tocca; a pari (a) conta (b) = somma della popolarita' delle zone toccate. Utili: 54; (a) di soglia 4.
Parcheggio adatto: linee utili con una fermata entro 400 m a piedi (linea d'aria x 1.3).

== Le 15 zone piu' popolari della Citta' metropolitana (Torino, cintura, resto CMTO) ==
  1. Q001 01 Torino-Centro             arrivi    168,734 (lavoro/studio 77,984; acquisti/svago 68,901; altro 21,849) servizi 285 esercizi 5139 [catalogo comunale]
  2. Q009 01 Torino-Nizza millefonti   arrivi     63,817 (lavoro/studio 23,335; acquisti/svago 30,447; altro 10,036) servizi 88 esercizi 1102 [catalogo comunale]
  3. C009 MONCALIERI                   arrivi     60,326 (lavoro/studio 19,204; acquisti/svago 30,096; altro 11,027) servizi 68 esercizi 281 [OpenStreetMap (incompleto)]
  4. C016 RIVOLI                       arrivi     59,518 (lavoro/studio 20,726; acquisti/svago 27,265; altro 11,527) servizi 70 esercizi 334 [OpenStreetMap (incompleto)]
  5. Q014 01 Torino- Parella           arrivi     59,433 (lavoro/studio 17,300; acquisti/svago 32,374; altro 9,759) servizi 117 esercizi 1177 [catalogo comunale]
  6. Q006 01 Torino-San Donato         arrivi     56,687 (lavoro/studio 20,423; acquisti/svago 24,320; altro 11,944) servizi 85 esercizi 1547 [catalogo comunale]
  7. C003 COLLEGNO                     arrivi     55,702 (lavoro/studio 17,496; acquisti/svago 26,697; altro 11,510) servizi 38 esercizi 168 [OpenStreetMap (incompleto)]
  8. C011 NICHELINO                    arrivi     50,092 (lavoro/studio 14,762; acquisti/svago 26,459; altro 8,872) servizi 38 esercizi 87 [OpenStreetMap (incompleto)]
  9. C006 SETTIMO TORINESE             arrivi     49,042 (lavoro/studio 16,868; acquisti/svago 23,697; altro 8,477) servizi 39 esercizi 128 [OpenStreetMap (incompleto)]
 10. Q012 01 Torino- Mirafiori Nord    arrivi     48,717 (lavoro/studio 18,288; acquisti/svago 22,125; altro 8,304) servizi 153 esercizi 777 [catalogo comunale]
 11. Q017 01 Torino- Borgata Vittoria  arrivi     48,159 (lavoro/studio 15,006; acquisti/svago 25,474; altro 7,679) servizi 61 esercizi 1234 [catalogo comunale]
 12. Q004 01 Torino-San Paolo          arrivi     46,945 (lavoro/studio 12,602; acquisti/svago 25,504; altro 8,839) servizi 72 esercizi 1094 [catalogo comunale]
 13. C002 GRUGLIASCO                   arrivi     46,470 (lavoro/studio 17,168; acquisti/svago 19,812; altro 9,490) servizi 32 esercizi 189 [OpenStreetMap (incompleto)]
 14. Q003 01 Torino-Crocetta           arrivi     45,767 (lavoro/studio 19,887; acquisti/svago 18,594; altro 7,286) servizi 76 esercizi 1555 [catalogo comunale]
 15. Q008 01 Torino-Vanchiglia         arrivi     45,512 (lavoro/studio 15,840; acquisti/svago 20,127; altro 9,545) servizi 77 esercizi 1103 [catalogo comunale]

Fuori dalla Citta' metropolitana (non entrano nella classifica, le linee GTT non ci arrivano): NOVARA (153,274); ALESSANDRIA (119,693); ASTI (118,846); BIELLA (89,576); VERCELLI (76,084) ...

== Le 5 zone piu' popolari per gruppo di scopo ==
  lavoro/studio: 01 Torino-Centro (77,984); 01 Torino-Nizza millefonti (23,335); RIVOLI (20,726); 01 Torino-San Donato (20,423); 01 Torino-Crocetta (19,887)
  acquisti/cure/svago: 01 Torino-Centro (68,901); 01 Torino- Parella (32,374); 01 Torino-Nizza millefonti (30,447); MONCALIERI (30,096); RIVOLI (27,265)
  altro: 01 Torino-Centro (21,849); 01 Torino-San Donato (11,944); RIVOLI (11,527); COLLEGNO (11,510); MONCALIERI (11,027)

== Le 15 linee piu' utili ==
  pos. linea   (a) zone top toccate   (b) popolarita' zone toccate   zone toccate   fermate   [b: lavoro | svago | altro]
    1. 2        (a)= 8  (b)=   610,462  zone  15  fermate  103  [201,508 | 298,571 | 110,383]
    2. 1085     (a)= 7  (b)=   757,926  zone  17  fermate  141  [281,397 | 345,924 | 130,606]
    3. 56       (a)= 7  (b)=   500,512  zone   9  fermate   94  [194,773 | 216,487 | 89,252]
    4. 1442     (a)= 7  (b)=   473,236  zone  11  fermate   36  [149,375 | 237,472 | 86,389]
    5. 93/      (a)= 6  (b)=   576,558  zone  12  fermate  114  [228,833 | 250,319 | 97,406]
    6. 91       (a)= 6  (b)=   507,358  zone   9  fermate   88  [195,400 | 229,521 | 82,437]
    7. M1       (a)= 6  (b)=   491,880  zone   7  fermate   23  [187,127 | 225,064 | 79,689]
    8. 35       (a)= 6  (b)=   490,583  zone   8  fermate   75  [194,396 | 218,929 | 77,258]
    9. M1S      (a)= 6  (b)=   477,322  zone   7  fermate   46  [187,811 | 213,562 | 75,949]
   10. 33       (a)= 6  (b)=   441,137  zone   7  fermate  101  [173,320 | 193,655 | 74,162]
   11. 12       (a)= 6  (b)=   436,688  zone   7  fermate   65  [173,499 | 193,530 | 69,659]
   12. 55       (a)= 6  (b)=   436,433  zone   7  fermate   88  [169,452 | 195,063 | 71,918]
   13. 15       (a)= 6  (b)=   417,872  zone   7  fermate   75  [167,235 | 179,543 | 71,094]
   14. 62       (a)= 6  (b)=   415,484  zone  11  fermate  125  [143,769 | 196,103 | 75,611]
   15. 22       (a)= 6  (b)=   414,004  zone  10  fermate   84  [135,475 | 202,248 | 76,281]

== I 15 parcheggi adatti con piu' linee utili (a pari linee: piu' posti) ==
    1. OSM way 1071023818                 osm_pubblico           Q010  posti 27  linee utili 20 (linee totali 30): 10, 1085, 1435, 1442, 1510, 18, 2, 2014, 3106, 3329, 38, 4
    2. OSM way 1509522235                 osm_pubblico           Q023  posti 23  linee utili 20 (linee totali 30): 10, 1085, 1435, 1442, 1510, 18, 2, 2014, 3106, 3329, 38, 4
    3. OSM way 540986061                  osm_pubblico           Q023  posti 76  linee utili 19 (linee totali 28): 10, 1085, 1435, 1442, 1510, 18, 2014, 3106, 3329, 38, 4, 62
    4. OSM way 612685927                  osm_pubblico           Q012  posti 200  linee utili 18 (linee totali 23): 10, 1085, 1435, 1510, 18, 2, 3106, 3329, 4, 62, 90, 91
    5. OSM way 652761156                  osm_pubblico           Q012  posti 80  linee utili 18 (linee totali 23): 12, 1435, 2014, 3106, 3329, 5, 5/, 62, 71, 74, 90, 91
    6. CAIO MARIO                         interscambio_ufficiale Q023  posti 418  linee utili 17 (linee totali 22): 10, 1085, 1510, 18, 2, 3106, 3329, 4, 62, 90, 91, 92
    7. OSM way 333542192                  osm_pubblico           Q012  posti 30  linee utili 16 (linee totali 21): 10, 1085, 1510, 18, 2, 3106, 3329, 4, 62, 90, 92, 93/
    8. OSM way 243506577                  osm_pubblico           Q012  posti 67  linee utili 14 (linee totali 18): 12, 1435, 2, 2014, 3106, 3329, 62, 90, 91, 92, 93/, 94
    9. OSM way 335813435                  osm_pubblico           Q010  posti 20  linee utili 14 (linee totali 21): 10, 1085, 1442, 1510, 18, 2014, 3106, 38, 4, 62, 91, 92
   10. OSM way 249741900                  osm_pubblico           Q012  posti 181  linee utili 13 (linee totali 17): 12, 2, 2014, 3106, 3329, 62, 90, 91, 92, 93/, 94, 97
   11. OSM way 249741901                  osm_pubblico           Q012  posti 86  linee utili 13 (linee totali 17): 12, 2, 2014, 3106, 3329, 62, 90, 91, 92, 93/, 94, 97
   12. OSM way 105712907                  osm_pubblico           Q012  posti 57  linee utili 12 (linee totali 14): 1085, 12, 44, 5, 5/, 58, 62, 71, 74, 90, 94, S05
   13. OSM way 106565241                  osm_pubblico           Q012  posti 30  linee utili 12 (linee totali 12): 1085, 12, 2, 5, 5/, 58, 62, 71, 74, 90, 94, S05
   14. OSM way 862941755                  osm_pubblico           Q011  posti 27  linee utili 12 (linee totali 12): 1085, 12, 1442, 17, 17/, 5, 5/, 58, 58/, 62, 94, S05
   15. PALAZZO NUOTO                      garage_5t              Q011  posti 190  linee utili 9 (linee totali 10): 10, 1442, 1510, 17, 17/, 4, 91, 92, S04

== Controlli ==
  OK     esiste spostamenti.csv
  OK     esiste imq_zone.json
  OK     esiste servizi_osm_cintura.json
  OK     esiste gtt_gtfs_20261003_224530.zip
  OK     esiste parcheggi_adatti.json
  OK     esiste parcheggi.json
  OK     esiste istruzione.json
  OK     nessuna zona senza nome
  OK     poligoni per tutte le zone — 212 poligoni, 212 zone
  OK     arrivi + ritorni a casa esclusi = totale spostamenti IMQ (stesso peso) — arrivi 4,444,360 + ritorni 3,714,050 + senza zona 59,452 + zona non nell'elenco 0 + scopo non classificato 0 = 8,217,863
  OK     spostamenti senza zona di arrivo, zona sconosciuta o scopo non classificato sotto l'1% — senza zona 59,452, zona sconosciuta 0, scopo non classificato 0
  OK     ritorni a casa esclusi sono una parte rilevante degli spostamenti — 45%
  OK     punti del catalogo fuori da ogni zona IMQ — servizi 0, esercizi 0
  AVVISO punti OSM della cintura fuori da ogni zona IMQ — 1
  AVVISO punti del catalogo comunale in zone fuori Torino (atteso 0: il catalogo e' di Torino) — 165 punti in C002 (50), C003 (2), C004 (1), C007 (13), C009 (96), C011 (1), C066 (2)
  OK     somma degli arrivi per zona = arrivi contati
  OK     zone senza nessun arrivo nell'IMQ — 0 su 212
  OK     linee nel GTFS > 50 — 215
  AVVISO fermate usate dalle linee fuori da ogni zona IMQ — 30 su 7043 (non contano per nessuna zona)
  OK     (a) non e' uguale per tutte le linee
  OK     linee con (a) uguale a quello di soglia (decide (b)) — 25 linee con (a) = 4, di cui 22 utili
  OK     le 10 linee piu' lunghe (per fermate) NON sono tutte fra le prime 15 per (a) — 0 su 10 sono fra le prime 15 (lunghe: 3107, 3006, 2014, 2172, 4512, 5137, 1510, 3106, 4108, 90)
  OK     tutti i parcheggi adatti hanno coordinate — 1874 adatti
  AVVISO parcheggi adatti senza nessuna linea entro 400 m a piedi — 495 su 1874
  AVVISO parcheggi adatti senza nessuna linea utile entro 400 m a piedi — 1123 su 1874

Scritti: data\processed\popolarita_zone.json, docs\RAPPORTO_POPOLARITA_ZONE.txt; avvisi: 5
```
