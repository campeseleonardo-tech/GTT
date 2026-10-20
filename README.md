# Mobilità a Torino — come si muove la città

Progetto personale di analisi dei dati (Leo, 2026): chi va dove, dove mancano servizi, dove sono le criticità
del trasporto pubblico a Torino e nella Città metropolitana, e pochi scenari «cosa succede se».
Due pagine: **`mappa_torino.html`** (mappa con i temi) e **`simulazione.html`** (le schede dei risultati: domanda,
risposta, grafici, criteri, limiti).

Ogni numero porta un'etichetta: [MISURATO] = misura vera (sensori 5T, mezzi GTT registrati ogni minuto da un
Raspberry Pi dal 3/10/2026); [PROGRAMMATO] = orario ufficiale GTT; [STIMATO] = calcolo nostro su dati veri;
[DATI SCARSI] = pochi dati. Le simulazioni usano l'orario programmato: non tengono conto di traffico, ritardi,
capienza e domanda reale.

## I risultati
### Risultato 1 — Dove mancano i servizi a piedi
*Quanti residenti di Torino non hanno almeno un servizio essenziale (scuole, salute, cibo, fermate, verde) entro 15 minuti a piedi, e quanti ne recupererebbe qualche servizio nuovo?*

**10.919 residenti** senza almeno un servizio essenziale a 15 minuti a piedi (1,3% dei torinesi)

10.919 residenti su 848.748 (1,3%) non hanno almeno uno dei 5 servizi entro 15 minuti a piedi.

### Risultato 2 — Metro di notte
*Quanti residenti guadagnano servizi raggiungibili in più nel buco notturno reale (00:50-05:22) se la metro M1 facesse corse finte anche lì?*

**334.085 residenti** raggiungerebbero almeno il 25% di servizi in più di notte con una metro ogni 15 minuti

Con una metro ogni 15 minuti nel buco notturno, 773.307 residenti di Torino e cintura (su 1.557.493) raggiungerebbero più servizi entro 45 minuti.

### Risultato 4 — Bus in ritardo e bus irregolari
*Quanto spesso i mezzi GTT arrivano in ritardo, e quanto spesso sulle linee frequenti arrivano a grappolo o lasciano buchi?*

**5,3 %** dei passaggi nei giorni feriali arriva con più di 5 minuti di ritardo

Nei giorni feriali il 5,3% dei passaggi arriva con più di 5 minuti di ritardo; il sabato il 7%.

### Risultato 6 — Parcheggi per lasciare l'auto
*Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, per le auto che ogni mattina entrano a Torino?*

**253 fermate** su 391 fermate importanti fuori dal centro non hanno abbastanza posti adatti entro 400 m a piedi per le auto in entrata che passano accanto

Gli interscambi che ci sono: nei giorni misurati Stura: sempre quasi pieno: 80% di notte, 90% di giorno; Caio Mario: il valore non cambia (2%): forse il contatore è fermo; Sofia: è più pieno di notte che di giorno: 55% di notte, 32% di giorno; Venchi Unica: sempre intorno al 51%; Fermi non trasmette il riempimento [MISURATO, DATI SCARSI]. Pieni di giorno: 1 su 5.

### Risultato 8 — Traffico sulle strade e trasporto pubblico
*Sulle strade grandi di Torino, dove c'è molto traffico e poco trasporto pubblico vicino?*

**95,3 %** dei km di strade grandi di Torino hanno fermate frequenti a pochi passi (327,3 km su 343,3)

Sulle 540 tratte di strade grandi di Torino (343,3 km), il 95,3% della lunghezza ha una fermata con almeno 4 passaggi all'ora entro 300 m, o la metro entro 600 m.

### Risultato 9 — Quanto si aspetta davvero alla fermata
*Sulle linee frequenti, quanti minuti in più aspetta in media chi arriva alla fermata senza guardare l'orario, rispetto a quanto promette l'orario?*

**0,6 min** in più di attesa alla fermata nei giorni feriali (fino a 1,5), su 4,8 promessi

Nei giorni feriali, sulle linee frequenti, l'orario promette un'attesa media di 4,8 minuti; quella reale è tra 5,4 e 6,2 minuti.

## Fonti e licenze
- GTT: orari (GTFS) e dati in tempo reale (GTFS-RT), dati aperti.
- 5T (sistema dei trasporti della Città di Torino): flussi di traffico, parcheggi, ZTL, dati aperti.
- ISTAT: censimento 2021 (sezioni), pendolarismo 2011 e 2021.
- Agenzia della Mobilità Piemontese: indagine IMQ 2022 (dati aperti).
- Agenzia delle Entrate — OMI: quotazioni immobiliari.
- Comune di Torino (aperTO): catalogo dei servizi, parcheggi.
- © contributori di OpenStreetMap (ODbL).
- Sfondi della mappa: **condizioni d'uso da verificare prima di pubblicare**.

## Limiti generali
Orario programmato per accessibilità e scenari; raccolta dei dati misurati iniziata il 3/10/2026 (parcheggi dal
14/10): le serie sono ancora brevi. Limiti di ogni risultato nella sua scheda.

## Come rifare i calcoli
Python 3 con le librerie di `requirements.txt`. Gli script sono in `scripts/`, numerati; i `.bat` lanciano le
catene (es. `scripts/RISULTATO6_RIFAI.bat`). I dati grezzi non sono nel repository (vedi `docs/FONTI_DATI.md`).

---

# Mobility in Turin — how the city moves (English)

Personal data-analysis project (Leo, 2026) on public transport and mobility in Turin, Italy: who travels where,
where services are missing, where the problems are, and a few "what if" scenarios. Two pages:
**`mappa_torino.html`** (interactive map) and **`simulazione.html`** (one card per result). The pages are in Italian;
every card has a short summary in English. Tags: [MISURATO] measured, [PROGRAMMATO] scheduled timetable,
[STIMATO] estimated, [DATI SCARSI] little data.

## Results
### Result 1
Question: how many Turin residents lack at least one essential service (schools, health, food, stops, green space) within 15 minutes on foot, and how many would gain one with a few new services? 10,919 residents out of 848,748 (1.3%) lack at least one of the 5 services within 15 minutes on foot. The most often missing one is health, with 9,104 residents without a nearby service of that kind. Up to 5 new services per group, placed where they help most, would bring 9,670 of these cases within 15 minutes, counted group by group. Limits: only the City of Turin is covered; outside it the service catalogue is missing, so a zero there often means missing data.

### Result 2
Question: if the metro ran through the night gap between 00:50 and 05:22 (simulated extra runs), how many residents would reach more services? With a metro every 15 minutes in the gap, 773,307 residents of Turin and the belt (out of 1,557,493) would reach more services within 45 minutes. With a run every 30 minutes, 652,891 would. Counting only a clear gain (at least 25% more reachable services at night): 334,085 and 153,062 residents. The average theoretical wait at the stop would be 7.5 minutes in the first case and 15.0 in the second. Limits: scheduled timetable only, with no traffic, delays, vehicle capacity or real passengers; the count is of reachable destinations, not of people using the metro.

### Result 4
Question: how often do GTT vehicles arrive late, and how often do frequent lines bunch together or leave gaps? On weekdays 5.3% of departures arrive more than 5 minutes late; on Saturdays 7.0%. On frequent lines 10.5% of consecutive pairs of vehicles bunch together or leave a gap. The most common problem is early arrival: 39.9% of weekday departures arrive more than one minute before the timetable. Limits: only 5 weekdays, 2 Saturdays and 2 Sundays of data, some of them partial; the night is not measured.

### Result 6
Question: where are park-and-ride spaces missing for the cars that enter Turin every morning, next to an important public transport stop outside the city centre? Existing park-and-ride car parks of the City: 4 of 5 report their occupancy; full during the day: 1 (measured, only a few days of data). About 87,200 cars enter Turin every morning (2022 travel survey) and 5.8% of these drivers already continue by public transport. 253 of 391 important stops outside the centre lack enough suitable parking within 400 m on foot for the cars passing by. Limits: car flows come from a simple traffic model (order of magnitude only); occupancy is measured on few days and only where the city's 5T system reports it; trains are not included.

### Result 8
Question: on Turin's major roads, where is there a lot of traffic and little public transport nearby? Of 540 road sections (343.3 km), 95.3% of the length has a frequent stop (at least 4 departures an hour) within 300 m, or the metro within 600 m. Heavy-traffic sections (over 11,720 vehicles a day): 180; of these, 5 also have little public transport. In practice this is one main case: Corso Regina Margherita westbound, a fast road with no frequent stop within 300 m, plus one stretch of Corso Moncalieri covered for only a quarter of its length. Limits: traffic figures are estimates with a typical error of ±38%; use them to rank the roads, not to count vehicles.

### Result 9
Question: on frequent lines, how many more minutes does a passenger who arrives at the stop without checking the timetable wait on average, compared with what the timetable promises? On weekdays the timetable promises an average wait of 4.8 minutes; the real one is between 5.4 and 6.2 minutes. That is 0.6 to 1.5 minutes more per wait, at least 13% above the promise. Limits: only 5 weekdays of data so far; real arrivals are estimated from the GTT feed, not seen at the stop; the night is not included.
