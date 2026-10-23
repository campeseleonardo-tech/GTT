# Torino Mobilità

[![Controllo automatico](https://github.com/campeseleonardo-tech/Turin-mobility/actions/workflows/controllo.yml/badge.svg)](https://github.com/campeseleonardo-tech/Turin-mobility/actions/workflows/controllo.yml)
[![Licenza MIT](https://img.shields.io/badge/licenza-MIT-blue.svg)](LICENSE)

*Italiano · [English below](#turin-mobility-english)*

**Come si muove Torino, letto dai dati veri.** Un progetto personale di analisi dei dati: chi va dove, dove mancano servizi, dove il trasporto pubblico fa fatica.
Un Raspberry Pi di casa raccoglie ogni minuto la posizione di bus e tram e i sensori del traffico; una mappa e cinque risultati raccontano cosa ne esce.

**Il sito: <https://campeseleonardo-tech.github.io/Turin-mobility/>**

| Home | Un risultato | La mappa |
|---|---|---|
| ![Home](assets/readme/home.jpg) | ![Un risultato](assets/readme/scheda.jpg) | ![La mappa](assets/readme/mappa.jpg) |

## I cinque risultati

<!-- RISULTATI-IT:INIZIO -->
1. **A 15 minuti quasi tutti hanno i servizi; a 5 minuti molti meno**  
   Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata? → **99,2%** dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi. [Apri](https://campeseleonardo-tech.github.io/Turin-mobility/r/1.html)
2. **I ritardi gravi sono circa il 6% dei passaggi**  
   Quanto spesso i mezzi GTT arrivano in ritardo o a coppie? → **6,19%** dei passaggi feriali arriva con oltre 10 minuti di ritardo. [Apri](https://campeseleonardo-tech.github.io/Turin-mobility/r/2.html)
3. **Dai parcheggi di scambio il bus vale l'auto solo se in centro si perdono 21–28 minuti a parcheggiare**  
   Dove mancano posti per lasciare l'auto, e quando il bus da lì verso il centro è veloce quanto l'auto? → **21–28 minuti** persi in centro per parcheggiare: sotto questa soglia l'auto batte il bus (mediana dei 12 punti). [Apri](https://campeseleonardo-tech.github.io/Turin-mobility/r/3.html)
4. **Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto**  
   Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno? → **2–3 volte** il tempo dell'auto: rapporto mediano, pesato per le auto del mattino (220.307 auto). [Apri](https://campeseleonardo-tech.github.io/Turin-mobility/r/4.html)
5. **Circa 1 torinese su 10 vive dove la fragilità è alta e i servizi sono pochi**  
   Si paga per i servizi? E chi vive dove i servizi sono pochi e la fragilità è alta? → **79.598** residenti in sezioni con fragilità alta e servizi bassi: il 9,5% dei torinesi. [Apri](https://campeseleonardo-tech.github.io/Turin-mobility/r/5.html)
<!-- RISULTATI-IT:FINE -->

Ogni numero porta la sua etichetta: **misurato** (sensori, GPS dei mezzi), **programmato** (orario ufficiale), **stimato** (calcolo mio su dati veri), **censimento**.
Ogni risultato dichiara i suoi limiti nella sua scheda.

## Come è fatto

- **Raccolta**: un Raspberry Pi (Python, SQLite) legge ogni minuto la posizione dei mezzi GTT, i ritardi e i sensori 5T del traffico e dei parcheggi.
- **Calcoli**: script Python numerati in `scripts/` (numpy, scipy, pandas, r5py per i percorsi in trasporto pubblico). Per ogni risultato c'è un documento in `docs/` (domanda, criteri, numeri, limiti).
- **Pagine**: HTML e JavaScript senza librerie; i dati arrivano da file `.js` scritti dagli script. La mappa e le schede stanno in `mappa_torino.html` e `risultati.html`.
- **Appunti di lavoro** (piani, memoria, prove): in `sviluppo/`.

## Fonti e licenze

Solo dati aperti. Il codice ha licenza [MIT](LICENSE); i dati mantengono la licenza della loro fonte (tabella completa in [`docs/FONTI_DATI.md`](docs/FONTI_DATI.md)).

- GTT: orari (GTFS) e tempo reale (GTFS-RT), CC BY, via aperTO.
- 5T (Muoversi a Torino): flussi di traffico, parcheggi, ZTL; IODL 2.0.
- ISTAT: censimento 2021 e basi territoriali, CC BY 4.0.
- Comune di Torino (aperTO): catalogo dei servizi, zone, fermate della metro, CC BY 4.0.
- Agenzia della mobilità piemontese: indagine sugli spostamenti IMQ 2022; Agenzia delle Entrate: quotazioni OMI. Licenza non chiara: **non ripubblicati**, si scaricano dalla fonte.
- © contributori di OpenStreetMap (ODbL). Sfondi della mappa: Esri, Maxar, Earthstar Geographics.

## Come rifare i calcoli

```
pip install -r requirements.txt
python scripts/scarica_dati.py      # dati grandi dalla Release di GitHub (IMQ e OMI a mano: vedi docs/DATI.md)
python scripts/rifai_tutto.py       # tutto, nell'ordine giusto; si ferma e riprende con --riprendi (--elenco mostra le fasi)
```

Solo le pagine: `python scripts/rifai_tutto.py --solo schede,mappa`. Controllo delle pagine: `python scripts/prova_pagine.py`.

## Chi sono

Leonardo Campese. Nel 2020 la mia tesi triennale (*The effects and applications of Industry 4.0 on Smart Cities*) prometteva che sensori e dati avrebbero cambiato le città;
questo progetto è la verifica, sui dati veri di Torino.
[LinkedIn](https://www.linkedin.com/in/leocampese/) · [campese.leonardo@gmail.com](mailto:campese.leonardo@gmail.com)

---

# Turin Mobility (English)

*[Italiano sopra](#torino-mobilità)*

**How Turin moves, read from real data.** A personal data-analysis project: who travels where, where services are missing, where public transport struggles.
A Raspberry Pi at home collects the position of buses and trams and the traffic sensors every minute; a map and five results show what comes out of it.
The site is in Italian and English (button IT/EN); the map is in Italian.

**The site: <https://campeseleonardo-tech.github.io/Turin-mobility/>**

## The five results

<!-- RISULTATI-EN:INIZIO -->
1. **Within 15 minutes almost everyone has the services; within 5 minutes far fewer do**  
   How many people in Turin have the services within 5, 10 and 15 minutes on foot, and how many live on a busy road? → **99.2%** of residents of inhabited areas have all 5 services within a 15-minute walk. [Open](https://campeseleonardo-tech.github.io/Turin-mobility/r/1.html)
2. **Serious delays are about 6% of stop arrivals**  
   How often are GTT vehicles late or bunched together? → **6.19%** of weekday arrivals are more than 10 minutes late. [Open](https://campeseleonardo-tech.github.io/Turin-mobility/r/2.html)
3. **From park-and-ride lots the bus matches the car only if 21–28 minutes are lost parking downtown**  
   Where is there too little room to leave the car, and when is the bus from there to the centre as fast as the car? → **21–28 minutes** lost downtown looking for parking: below this threshold the car beats the bus (median of the 12 points). [Open](https://campeseleonardo-tech.github.io/Turin-mobility/r/3.html)
4. **In the morning, public transport takes 2 to 3 times as long as the car**  
   For which trips is the car much faster than public transport, and how many cars make them? → **2–3 times** the car's travel time: median ratio, weighted by morning cars (220,307 cars). [Open](https://campeseleonardo-tech.github.io/Turin-mobility/r/4.html)
5. **About 1 Turin resident in 10 lives where fragility is high and services are few**  
   Do people pay for services? And who lives where services are few and fragility is high? → **79,598** residents in sections with high fragility and low services: 9.5% of Turin residents. [Open](https://campeseleonardo-tech.github.io/Turin-mobility/r/5.html)
<!-- RISULTATI-EN:FINE -->

Every number carries a label: **measured** (sensors, vehicle GPS), **scheduled** (official timetable), **estimated** (my calculation on real data), **census**.
Each result states its limits on its own card.

## How it is built

- **Collection**: a Raspberry Pi (Python, SQLite) reads the position of GTT vehicles, delays and the 5T traffic and parking sensors every minute.
- **Calculations**: numbered Python scripts in `scripts/` (numpy, scipy, pandas, r5py for public-transport routing). Each result has a document in `docs/` (question, criteria, numbers, limits).
- **Pages**: plain HTML and JavaScript, no libraries; data come from `.js` files written by the scripts.
- **Working notes** (plans, memory, tests): in `sviluppo/` (Italian).

## Sources and licences

Open data only. The code is under the [MIT licence](LICENSE); the data keep the licence of their source (full table in [`docs/FONTI_DATI.md`](docs/FONTI_DATI.md), Italian).

- GTT: timetables (GTFS) and real time (GTFS-RT), CC BY, via aperTO.
- 5T (Muoversi a Torino): traffic flows, parking, restricted traffic zones; IODL 2.0.
- ISTAT: 2021 census and territorial bases, CC BY 4.0.
- City of Turin (aperTO): service catalogue, zones, metro stops, CC BY 4.0.
- Piedmont Mobility Agency: 2022 travel survey (IMQ); Revenue Agency: OMI price quotes. Licence unclear: **not republished**, download them from the source.
- © OpenStreetMap contributors (ODbL). Map backgrounds: Esri, Maxar, Earthstar Geographics.

## Rebuild the calculations

```
pip install -r requirements.txt
python scripts/scarica_dati.py      # large data from the GitHub Release (IMQ and OMI by hand: see docs/DATI.md)
python scripts/rifai_tutto.py       # everything, in the right order; stops and resumes with --riprendi (--elenco lists the steps)
```

Pages only: `python scripts/rifai_tutto.py --solo schede,mappa`. Page checks: `python scripts/prova_pagine.py`.

## About me

Leonardo Campese. In 2020 my bachelor's thesis (*The effects and applications of Industry 4.0 on Smart Cities*) promised that sensors and data would change cities;
this project is the check, on real data from Turin.
[LinkedIn](https://www.linkedin.com/in/leocampese/) · [campese.leonardo@gmail.com](mailto:campese.leonardo@gmail.com)
