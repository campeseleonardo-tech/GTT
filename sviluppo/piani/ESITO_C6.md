# ESITO C6 — schede divise e testi IT/EN (cloud, 22/10/2026)

Piano 5 passo 4 e piano 4 passo 5. Ramo della sessione `claude/ecstatic-faraday-nuy8hv`. Prima, correzioni di C5 chieste da Leo (tendine della mappa nere nel modo scuro, Risultati/Home/Il progetto come pulsanti nella mappa,
numeri che rallentano alla fine, niente etichette misurato/stimato nelle anteprime): fatte nel commit precedente.

## Cosa è stato fatto
1. **`scripts/schede_risultati.py` diviso** in `scripts/schede/`: `comune.py` (percorsi, lettura dei JSON, formati dei numeri, forma base), `r1.py`, `r2.py`, `r4.py` (comprende l'attesa, ex risultato 9), `r6.py`, `r8.py`, `r10.py`.
   `scripts/schede_risultati.py` resta il punto di ingresso con lo stesso comando. **Regola d'oro rispettata**: con gli stessi dati il file italiano esce **identico** a prima (confronto fra il vecchio script e il nuovo sui dati veri, tolti `generato` e il nuovo campo `forma_en`).
   I moduli leggono `comune.PROC` al momento dell'uso (le prove lo cambiano); `prove/prova_scheda_case.py` aggiornato.
2. **Inglese completo** di ogni scheda: `forma_en` accanto a `forma` (titolo, domanda, testo del numero, punti chiave, grafici con titoli, note, etichette e testi delle barre, calcolo, criteri, confronto, limiti, extra, omini/pallini, tag).
   I testi stanno in **`scripts/schede/testi.json`**: 146 frasi fisse e 100 modelli con segnaposto (`{n0}` numero, `{s0}` testo copiato, `{w0}` elenco con parole sostituite, `{t0}` testo tradotto, `{a0}` articolo italiano che sparisce).
   Funziona così: lo script scrive l'italiano come prima; `scripts/schede/traduci.py` cerca ogni frase italiana fra le frasi fisse o i modelli e ne ricava l'inglese, con i numeri nel formato inglese (1.234,5 → 1,234.5). I nomi propri (zone, linee, fermate) restano come sono.
   Una frase italiana senza traduzione resta in italiano e lo script scrive «ATTENZIONE … frase senza traduzione»: se cambi una frase in un modulo, devi cambiare anche `testi.json`.
3. **Bottone IT / EN** nella barra di home, risultati e progetto (la mappa resta in italiano): cambia lingua senza ricaricare (anche con la scheda aperta), ricorda la scelta (`localStorage` dentro `try/catch`), parte in inglese se la lingua del browser non è l'italiano, `?lang=en` e `?lang=it` forzano la lingua.
   Testi fissi delle pagine: `data-en` sull'elemento; testi dinamici: `Sito.T(italiano, inglese)`; i numeri seguono la lingua. Nuovi in `assets/sito.js` e `assets/stile.css`.

## Prove (cloud, dati veri)
- Italiano identico a prima (confronto con l'uscita del vecchio script): **sì**.
- `python scripts/prove/prova_traduzione.py`: 5 schede, **0 frasi senza traduzione**, nessun segnaposto rimasto, nessun numero in formato italiano, stessa struttura dell'italiano.
- `python scripts/prova_pagine.py`: 19 pagine, **0 errori**. `python scripts/prove/screenshot_sito.py`: 35 immagini, nessun errore JavaScript né scorrimento orizzontale, anche in inglese (home, risultati, schede 2, 3, 5; computer e telefono: copie in `sviluppo/c6_screenshot/`, file `*_EN.jpg`).
- Provati con il browser: cambio lingua dalla home (riquadri, bottoni, piè di pagina), lingua ricordata aprendo `risultati.html#p5`, scheda aperta che si ridisegna cambiando lingua, browser inglese → inglese, `?lang=it` → italiano.
- `python -m py_compile` su tutti gli script e `pyflakes` sui file nuovi: puliti.

## Da fare sul PC (giro P4: stessi numeri dopo la divisione)
1. Unire il ramo; `scripts\RIFAI_MAPPA_E_SCHEDE.bat` (o solo `python scripts\schede_risultati.py`): non devono comparire righe «ATTENZIONE … senza traduzione».
2. Prima di unire, copiare `data\schede_risultati.js` in un altro file; dopo, confrontare: i numeri dell'italiano devono essere gli stessi (cambiano solo `generato` e il nuovo campo `forma_en`).
3. Aprire `risultati.html` e premere EN: rileggere l'inglese (lista qui sotto, o direttamente `scripts/schede/testi.json`).

## Frasi inglesi da rileggere
Le frasi con numeri sono modelli: `{n0}` = numero. Formato: *italiano* → inglese.

### Frasi lunghe e modelli
- *negozi e attività commerciali*  
  → shops and commercial activities
- *bisogno medio*  
  → medium need
- *bisogno basso*  
  → low need
- *A 15 minuti quasi tutti hanno i servizi; a 5 minuti molti meno*  
  → Within 15 minutes almost everyone has the services; within 5 minutes far fewer do
- *Quanti torinesi hanno i servizi a 5, 10 e 15 minuti a piedi, e quanti vivono su una strada trafficata?*  
  → How many people in Turin have the services within 5, 10 and 15 minutes on foot, and how many live on a busy road?
- *dei residenti delle zone abitate ha tutti e 5 i servizi a 15 minuti a piedi*  
  → of residents of inhabited areas have all 5 services within a 15-minute walk
- *Residenti per servizi raggiunti a piedi*  
  → Residents by services reached on foot
- *tutti e 5 i servizi*  
  → all 5 services
- *Residenti per distanza da una strada molto trafficata*  
  → Residents by distance from a very busy road
- *Residenti senza il servizio a 15 minuti a piedi*  
  → Residents without the service within a 15-minute walk
- *Per ogni sezione di censimento si contano i servizi raggiungibili a piedi in 5, 10 e 15 minuti.*  
  → For each census section we count the services reachable on foot in 5, 10 and 15 minutes.
- *I tipi di servizio sono cinque, contati separatamente: scuole, salute, negozi, fermate, verde.*  
  → There are five types of service, counted separately: schools, health, shops, stops, green space.
- *Tempi a piedi*  
  → Walking times
- *5, 10 e 15 minuti*  
  → 5, 10 and 15 minutes
- *Velocità a piedi*  
  → Walking speed
- *Zona poco abitata*  
  → Sparsely inhabited area
- *Sezioni di Torino*  
  → Sections in Turin
- *Punti nuovi per gruppo*  
  → New points per group
- *Strada molto trafficata*  
  → Very busy road
- *Esposto al traffico*  
  → Exposed to traffic
- *Solo Torino: in cintura il catalogo dei servizi manca, quindi «zero» spesso vuol dire dato mancante.*  
  → Turin only: the service catalogue is missing for the surrounding towns, so “zero” often means missing data.
- *Si conta se un servizio c'è, non quanto è grande né se ha posto. Le fermate usano l'orario programmato: niente ritardi né affollamento.*  
  → We count whether a service exists, not how big it is or whether it has room. Stops use the scheduled timetable: no delays and no crowding.
- *I punti nuovi sono ipotesi: non tengono conto di costi, spazi liberi o permessi.*  
  → New points are hypotheses: they ignore costs, free space and permits.
- *Il traffico è una stima e sostituisce rumore e smog, che non misuriamo.*  
  → Traffic is an estimate standing in for noise and smog, which we do not measure.
- *Quanto spesso i mezzi GTT arrivano in ritardo o a coppie?*  
  → How often are GTT vehicles late or bunched together?
- *dei passaggi feriali arriva con oltre 10 minuti di ritardo*  
  → of weekday arrivals are more than 10 minutes late
- *Come arrivano i mezzi*  
  → How vehicles arrive
- *Ogni barra è un tipo di giorno: 100% dei passaggi.*  
  → Each bar is a type of day: 100% of arrivals.
- *in anticipo (oltre 1 minuto)*  
  → early (more than 1 minute)
- *ritardo da 5 a 10 minuti*  
  → 5 to 10 minutes late
- *ritardo oltre 10 minuti*  
  → more than 10 minutes late
- *Noi e GTT: passaggi in ritardo oltre 10 minuti*  
  → Us and GTT: arrivals more than 10 minutes late
- *GTT (2025, anno intero)*  
  → GTT (2025, whole year)
- *noi, a ogni fermata*  
  → us, at every stop
- *noi, solo alla prima fermata*  
  → us, first stop only
- *noi, solo a metà corsa*  
  → us, mid-trip only
- *noi, fuori dalle ore di punta*  
  → us, outside peak hours
- *Ritardo oltre 5 minuti, per fascia oraria (feriale)*  
  → Delay over 5 minutes, by time of day (weekday)
- *punta mattino (7-9)*  
  → morning peak (7-9)
- *giorno (9-16)*  
  → daytime (9-16)
- *punta sera (16-19)*  
  → evening peak (16-19)
- *passaggi in ritardo*  
  → late arrivals
- *Il Raspberry Pi registra ogni minuto la posizione GPS dei mezzi GTT.*  
  → A Raspberry Pi records the GPS position of GTT vehicles every minute.
- *Il ritardo è quell'istante meno l'orario ufficiale.*  
  → The delay is that moment minus the official timetable.
- *Grappolo: due mezzi attaccati. Buco: intervallo doppio del previsto. Solo linee frequenti.*  
  → Bunching: two vehicles right behind each other. Gap: an interval twice the planned one. Frequent lines only.
- *Passaggi con GPS valido*  
  → Arrivals with a valid GPS fix
- *Soglia ritardo*  
  → Delay threshold
- *Soglia anticipo*  
  → Earliness threshold
- *Distanza dalla fermata*  
  → Distance from the stop
- *Solo le linee urbane viste dal GPS, dalle 5 a mezzanotte.*  
  → Urban lines seen by the GPS only, from 5 a.m. to midnight.
- *Contiamo quanto spesso c'è ritardo, non quante persone aspettano.*  
  → We count how often there is a delay, not how many people are waiting.
- *Quanto si aspetta alla fermata*  
  → How long you wait at the stop
- *Attesa media alla fermata, per fascia oraria (feriale)*  
  → Average wait at the stop, by time of day (weekday)
- *Barra chiara = attesa promessa, barra scura = attesa reale (stima bassa).*  
  → Light bar = promised wait, dark bar = actual wait (low estimate).
- *punta del mattino (7-9)*  
  → morning peak (7-9)
- *punta della sera (16-19)*  
  → evening peak (16-19)
- *Dove mancano posti per lasciare l'auto, e quando il bus da lì verso il centro è veloce quanto l'auto?*  
  → Where is there too little room to leave the car, and when is the bus from there to the centre as fast as the car?
- *Minuti per parcheggiare in centro oltre i quali il bus dal punto è veloce quanto l'auto*  
  → Minutes spent parking downtown beyond which the bus from the point is as fast as the car
- *Verso Piazza Castello alle 8. Barra scura = auto lenta (fattore di Google), barra chiara = auto veloce (fattore dei sensori). Meno minuti = punto più promettente; 0 = il bus è già più veloce.*  
  → Towards Piazza Castello at 8 a.m. Dark bar = slow car (Google factor), light bar = fast car (sensor factor). Fewer minutes = more promising point; 0 = the bus is already faster.
- *Il bisogno è alto, medio o basso a terzi, in base ai posti che mancano. Le lunghezze sono un ordine di grandezza.*  
  → Need is high, medium or low by thirds, based on the missing spaces. Lengths are an order of magnitude.
- *Le auto in entrata vengono dall'indagine sugli spostamenti 2022, assegnate al percorso più veloce.*  
  → Cars entering come from the 2022 travel survey, assigned to the fastest route.
- *Punti prioritari: fermate senza posti bastanti raggruppate entro 1 km, uno per asse d'ingresso.*  
  → Priority points: stops without enough parking, grouped within 1 km, one per entry axis.
- *Minuti di pareggio: tempo coi mezzi verso Piazza Castello alle 8, meno il tempo in auto senza parcheggio.*  
  → Break-even minutes: travel time by public transport to Piazza Castello at 8 a.m., minus travel time by car without parking.
- *Fermate importanti*  
  → Important stops
- *Distanza a piedi*  
  → Walking distance
- *Auto da fermare*  
  → Cars to stop
- *Bus contro auto*  
  → Bus versus car
- *Il costo del parcheggio in centro non è nel calcolo: pesa come minuti in più.*  
  → The cost of parking downtown is not in the calculation: it counts as extra minutes.
- *Si guarda un solo punto per luogo e una sola destinazione, Piazza Castello.*  
  → We look at one point per place and a single destination, Piazza Castello.
- *Le auto che passano vengono da un modello del traffico. I posti sono spesso stimati, con ±30%.*  
  → Passing cars come from a traffic model. Spaces are often estimated, with ±30%.
- *Interscambi esistenti e bus verso il centro*  
  → Existing park-and-ride lots and buses to the centre
- *Dagli interscambi esistenti a Piazza Castello, minuti coi mezzi pubblici*  
  → From existing park-and-ride lots to Piazza Castello, minutes by public transport
- *Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno?*  
  → For which trips is the car much faster than public transport, and how many cars make them?
- *Auto del mattino per rapporto fra tempo coi mezzi pubblici e tempo in auto*  
  → Morning cars by ratio of public transport time to car time
- *Tempo in auto e tempo coi mezzi pubblici, una coppia di zone per punto*  
  → Car time and public transport time, one pair of zones per point
- *minuti coi mezzi pubblici*  
  → minutes by public transport
- *Mezzi pubblici: a piedi, bus, tram e metro, con partenza fra le 7:45 e le 8:15. Si prende la mediana.*  
  → Public transport: on foot, bus, tram and metro, departing between 7:45 and 8:15. We take the median.
- *Rapporto = tempo coi mezzi diviso tempo in auto. Le fasce sono fisse e decise prima di vedere i numeri.*  
  → Ratio = public transport time divided by car time. The bands are fixed and chosen before seeing the numbers.
- *Le auto di una coppia sono i viaggi in auto dell'indagine, in partenza dalle 6 alle 10 di un feriale.*  
  → The cars of a pair are the survey's car trips, departing between 6 and 10 a.m. on a weekday.
- *Mezzi pubblici*  
  → Public transport
- *Auto, limite alto*  
  → Car, high limit
- *Auto, limite basso*  
  → Car, low limit
- *Fasce del rapporto*  
  → Ratio bands
- *Fuori Torino mancano treni e altre aziende: le coppie fra comuni della cintura non sono nel numero.*  
  → Outside Turin, trains and other operators are missing: pairs between suburban towns are not in the number.
- *La nostra rete stradale non conta semafori e incroci. I tempi in auto sono stimati fra il rallentamento misurato dai sensori e quello di Google Maps.*  
  → Our road network ignores traffic lights and junctions. Car times are estimated between the slowdown measured by sensors and that of Google Maps.
- *Senza i treni metropolitani, dove ci sono, i mezzi pubblici risultano più lenti del vero. L'orario è quello programmato.*  
  → Without metropolitan trains, where they exist, public transport looks slower than it is. The timetable is the scheduled one.
- *Strade grandi e fermate vicine*  
  → Large roads and nearby stops
- *Km di strade grandi di Torino: con o senza trasporto pubblico vicino*  
  → Km of large roads in Turin: with or without public transport nearby
- *con fermate frequenti vicine*  
  → with frequent stops nearby
- *con poco trasporto pubblico*  
  → with little public transport
- *Si paga per i servizi? E chi vive dove i servizi sono pochi e la fragilità è alta?*  
  → Do people pay for services? And who lives where services are few and fragility is high?
- *punteggio «Tutti i servizi» a piedi, 0-100*  
  → “All services” score on foot, 0-100
- *prezzo delle case, euro al m²*  
  → house price, euro per m²
- *Residenti delle sezioni di Torino per condizione*  
  → Residents of Turin's census sections by condition
- *fragilità alta e servizi bassi*  
  → high fragility and low services
- *solo fragilità alta*  
  → high fragility only
- *solo servizi bassi*  
  → low services only
- *nessuna delle due*  
  → neither
- *Quanto più costano le case vicino alla metro (con metro meno senza metro)*  
  → How much more homes cost near the metro (with metro minus without)
- *Per fascia di distanza da Piazza Castello (2 km): prezzo medio delle zone con una fermata M1 entro 600 m meno quello delle zone senza, alla stessa distanza dal centro. Su ogni barra il numero di zone. Differenza fra zone, non effetto della metro.*  
  → By distance band from Piazza Castello (2 km): average price of zones with an M1 stop within 600 m minus that of zones without, at the same distance from the centre. The number of zones is shown on each bar. A difference between zones, not an effect of the metro.
- *Servizi: punteggio «Tutti i servizi» a piedi in 15 minuti. Fragilità: indice del censimento 2021 (lavoro, istruzione, case, anziani).*  
  → Services: “All services” score within a 15-minute walk. Fragility: 2021 census index (work, education, housing, older people).
- *Prezzo: centro della forbice OMI per le abitazioni civili. Tendenza: retta dei minimi quadrati.*  
  → Price: middle of the OMI range for residential homes. Trend: least-squares line.
- *Metro: zone con una fermata M1 entro 600 m dal centro, contro le altre alla stessa distanza da Piazza Castello.*  
  → Metro: zones with an M1 stop within 600 m of the centre, compared with the others at the same distance from Piazza Castello.
- *Fragilità alta*  
  → High fragility
- *Servizi bassi*  
  → Low services
- *I prezzi sono quotazioni OMI, non compravendite.*  
  → Prices are OMI quotations, not actual sales.
- *C'è un solo semestre di quotazioni (2025/2).*  
  → There is only one semester of quotations (2025/2).
- *Le zone OMI sono grandi: dentro una zona i prezzi e i servizi cambiano molto.*  
  → OMI zones are large: prices and services vary a lot within a zone.
- *L'indice di fragilità non è il reddito: misura lavoro, istruzione, affollamento e anziani.*  
  → The fragility index is not income: it measures work, education, crowding and older people.
- *Nessun punto ha un collegamento coi mezzi entro 120 minuti.*  
  → No point has a public transport connection within 120 minutes.
- *Vicino alla metro non si può confrontare il prezzo: mancano zone con e senza metro a pari distanza dal centro.*  
  → Near the metro prices cannot be compared: there are no zones with and without a metro at the same distance from the centre.
- *Ogni barra è un tempo a piedi: 100% dei residenti delle zone abitate (almeno {n0} abitanti per km²).*  
  → Each bar is a walking time: 100% of residents of inhabited areas (at least {n0} inhabitants per km²).
- *{n0} minuti*  
  → {n0} minutes
- *{n0} servizi*  
  → {n0} services
- *{n0} o meno*  
  → {n0} or fewer
- *Distanza dal centro della sezione. Strada molto trafficata: almeno {n0} veicoli al giorno. Stima debole: il modello sbaglia del ±{n1}% in metà dei casi.*  
  → Distance from the centre of the census section. Very busy road: at least {n0} vehicles a day. Weak estimate: the model is off by ±{n1}% in half of the cases.
- *esposti (meno di {n0} m)*  
  → exposed (less than {n0} m)
- *vicini ({s0} m)*  
  → close ({s0} m)
- *lontani (oltre {n0} m)*  
  → far (over {n0} m)
- *Solo zone abitate (almeno {n0} abitanti per km²).*  
  → Inhabited areas only (at least {n0} inhabitants per km²).
- *Si cammina sulla rete stradale reale (OpenStreetMap), a {n0} m al minuto.*  
  → Walking follows the real street network (OpenStreetMap), at {n0} m per minute.
- *Residenti dal censimento ISTAT 2021; le zone con meno di {n0} abitanti per km² sono grigie e contate a parte.*  
  → Residents come from the ISTAT 2021 census; areas with fewer than {n0} inhabitants per km² are shown in grey and counted separately.
- *Si è esposti se il centro della sezione è a meno di {n0} m da una strada molto trafficata.*  
  → A section is exposed if its centre is less than {n0} m from a very busy road.
- *{n0} m al minuto ({n1} km/h)*  
  → {n0} m per minute ({n1} km/h)
- *sotto {n0} ab/km² (prove con {n1} e {n2})*  
  → under {n0} inh/km² (tested with {n1} and {n2})
- *fino a {n0}*  
  → up to {n0}
- *almeno {n0} veicoli al giorno*  
  → at least {n0} vehicles a day
- *a meno di {n0} m dalla strada*  
  → less than {n0} m from the road
- *I ritardi gravi sono circa il {n0}% dei passaggi*  
  → Serious delays are about {n0}% of stop arrivals
- *Barre = media della settimana (feriale 5 : sabato 1 : domenica 1). Nei feriali: a ogni fermata {n0}%, alla prima fermata {n1}%, a metà corsa {n2}%, fuori punta {n3}%. GTT: anno 2025, tutte le linee, metodo non pubblicato.*  
  → Bars = weekly average (weekday 5 : Saturday 1 : Sunday 1). On weekdays: at every stop {n0}%, at the first stop {n1}%, mid-trip {n2}%, off-peak {n3}%. GTT: year 2025, all lines, method not published.
- *Il passaggio è l'istante in cui il GPS è a meno di {n0} metri dalla fermata.*  
  → An arrival is the moment the GPS is less than {n0} metres from the stop.
- *In anticipo oltre {n0} minuto; in ritardo oltre {n1} minuti.*  
  → Early: more than {n0} minute; late: more than {n1} minutes.
- *{n0} ({n1}% di quelli programmati dalle corse viste)*  
  → {n0} ({n1}% of those scheduled for the trips seen)
- *entro {n0} m*  
  → within {n0} m
- *Pochi giorni: {n0} feriali, {n1} sabati e {n2} {t3}, non tutti interi.*  
  → Few days: {n0} weekdays, {n1} Saturdays and {n2} {t3}, not all complete.
- *Il GPS copre circa il {n0}% dei passaggi programmati; le corse mai viste non si contano.*  
  → The GPS covers about {n0}% of scheduled arrivals; trips never seen are not counted.
- *Su 100 passaggi feriali, circa {n0} arrivano con più di 5 minuti di ritardo ({n1}%); con più di 10 minuti circa {n2}.*  
  → Out of 100 weekday arrivals, about {n0} are more than 5 minutes late ({n1}%); more than 10 minutes late, about {n2}.
- *GTT dichiara il {n0}% oltre 10 minuti nel 2025: media dell'anno, tutte le linee, metodo non pubblicato.*  
  → GTT reports {n0}% over 10 minutes in 2025: yearly average, all lines, method not published.
- *Noi misuriamo pochi giorni di ottobre sulle linee urbane: {n0}% a ogni fermata, {n1}% alla partenza.*  
  → We measure a few days in October on urban lines: {n0}% at every stop, {n1}% at departure.
- *Anche contando come GTT alla partenza troviamo il {n0}%; il resto della differenza è stagione e metodo.*  
  → Even counting at departure like GTT, we find {n0}%; the rest of the difference is season and method.
- *Sulle linee frequenti si aspettano da {n0} a {n1} minuti in più di quanto promette l'orario (feriale).*  
  → On frequent lines you wait {n0} to {n1} minutes more than the timetable promises (weekday).
- *Dai parcheggi di scambio il bus vale l'auto solo se in centro si perdono {s0} minuti a parcheggiare*  
  → From park-and-ride lots the bus matches the car only if {s0} minutes are lost parking downtown
- *persi in centro per parcheggiare: sotto questa soglia l'auto batte il bus (mediana dei {n0} punti)*  
  → lost downtown looking for parking: below this threshold the car beats the bus (median of the {n0} points)
- *I {n0} punti d'ingresso, per bisogno di parcheggio*  
  → The {n0} entry points, by need for parking
- *Fermate importanti: fuori dal centro, con metro, stazione o capolinea, oppure {n0} corse all'ora.*  
  → Important stops: outside the centre, with a metro, station or terminus, or {n0} trips an hour.
- *Auto da fermare: auto che passano per il {n0}% che già oggi lascia l'auto. Posti: parcheggi adatti entro {n1} metri.*  
  → Cars to stop: passing cars times the {n0}% who already leave the car today. Spaces: suitable car parks within {n1} metres.
- *{n0} corse all'ora o metro, e {n1} auto che passano*  
  → {n0} trips an hour or a metro, and {n1} passing cars
- *{n0} metri*  
  → {n0} metres
- *auto che passano × {n0}%*  
  → passing cars × {n0}%
- *verso Piazza Castello alle 8, auto con fattore {n0} (sensori) e {n1} (Google)*  
  → towards Piazza Castello at 8 a.m., car with factor {n0} (sensors) and {n1} (Google)
- *I tempi coi mezzi sono solo GTT, senza treni. L'auto è stimata fra due fattori di punta, {n0} e {n1}.*  
  → Public transport times are GTT only, without trains. The car is estimated between two peak factors, {n0} and {n1}.
- *Un pallino per punto prioritario: verde = il bus conviene ({n0}), giallo = dipende ({n1}), rosso = il bus non conviene ({n2}).*  
  → One dot per priority point: green = the bus pays off ({n0}), yellow = it depends ({n1}), red = the bus does not pay off ({n2}).
- *Gli interscambi esistenti sono poco pieni: di giorno solo {n0} su {n1} è pieno.*  
  → Existing park-and-ride lots are not very full: in the daytime only {n0} of {n1} is full.
- *Alle 8 di un feriale. A destra il tempo in auto, parcheggio compreso, fra i due fattori di punta ({n0} e {n1}).*  
  → At 8 a.m. on a weekday. On the right, car time including parking, between the two peak factors ({n0} and {n1}).
- *{n0} contro {s1} in auto*  
  → {n0} versus {s1} by car
- *Al mattino, coi mezzi pubblici si impiega da {n0} a {n1} volte il tempo dell'auto*  
  → In the morning, public transport takes {n0} to {n1} times as long as the car
- *il tempo dell'auto: rapporto mediano, pesato per le auto del mattino ({n0} auto)*  
  → the car's travel time: median ratio, weighted by morning cars ({n0} cars)
- *Rapporto 2 = coi mezzi pubblici si impiega il doppio che in auto. Coppie Torino-Torino e Torino-cintura. Limite basso: auto lenta come su Google Maps (fattore {n0}); limite alto: auto veloce come misurano i sensori (fattore {n1}).*  
  → Ratio 2 = public transport takes twice as long as the car. Turin–Turin and Turin–suburb pairs. Low limit: slow car as on Google Maps (factor {n0}); high limit: fast car as the sensors measure (factor {n1}).
- *sotto {n0}*  
  → under {n0}
- *oltre {n0}*  
  → over {n0}
- *{n0}% ({n1} auto)*  
  → {n0}% ({n1} cars)
- *minuti in auto (ora di punta, fattore {n0})*  
  → minutes by car (peak hour, factor {n0})
- *{n0} volte*  
  → {n0} times
- *Ogni punto è una coppia di zone, grande quanto le auto del mattino. Sono le {n0} coppie con più auto ({n1}% delle auto). Sopra una linea il mezzo pubblico impiega più di quel multiplo dell'auto.*  
  → Each point is a pair of zones, sized by morning cars. These are the {n0} pairs with the most cars ({n1}% of cars). Above a line, public transport takes more than that multiple of the car's time.
- *Le {n0} coppie con più auto dove i mezzi pubblici impiegano più del doppio*  
  → The {n0} pairs with the most cars where public transport takes more than twice as long
- *Auto del mattino su quella coppia (dalle 6 alle 10, giorno feriale), con il fattore basso {n0}. A destra i minuti coi mezzi contro quelli in auto.*  
  → Morning cars on that pair (6 a.m. to 10 a.m., weekday), with the low factor {n0}. On the right, minutes by public transport versus by car.
- *{n0} auto: {n1} contro {n2} min*  
  → {n0} cars: {n1} versus {n2} min
- *Le zone sono quelle dell'indagine sugli spostamenti 2022 con punti di calcolo; ognuna ha fino a {n0} punti.*  
  → Zones are those of the 2022 travel survey, with calculation points; each has up to {n0} points.
- *Auto: tempo a flusso libero per un fattore di punta, più {n0} minuti. I fattori sono due: {n1} da Google Maps e {n2} dai sensori.*  
  → Car: free-flow time times a peak factor, plus {n0} minutes. There are two factors: {n1} from Google Maps and {n2} from the sensors.
- *{n0} zone dell'indagine sugli spostamenti ({n1} di Torino), fino a {n2} punti ciascuna*  
  → {n0} travel-survey zones ({n1} in Turin), up to {n2} points each
- *partenza {s0} di un feriale, mediana, cammino a {n1} km/h, al massimo {n2} minuti*  
  → departure {s0} on a weekday, median, walking at {n1} km/h, at most {n2} minutes
- *tempo a flusso libero × {n0} (sensori 5T) + {n1} minuti*  
  → free-flow time × {n0} (5T sensors) + {n1} minutes
- *tempo a flusso libero × {n0} (Google Maps, {n1} percorsi) + {n2} minuti*  
  → free-flow time × {n0} (Google Maps, {n1} routes) + {n2} minutes
- *sotto {n0}, {n1}-{n2}, {n3}-{n4}, oltre {n5} (fissate prima dei numeri)*  
  → under {n0}, {n1}-{n2}, {n3}-{n4}, over {n5} (fixed before the numbers)
- *L'indagine è un campione. I viaggi dentro una zona e {n0} coppie senza collegamento ({n1} auto) non sono nel confronto.*  
  → The survey is a sample. Trips within a zone and {n0} pairs with no connection ({n1} cars) are not in the comparison.
- *Il {n0}% dei km di strade grandi ha una fermata frequente vicina: la fermata c'è, ma non basta.*  
  → {n0}% of the km of large roads have a frequent stop nearby: the stop is there, but it is not enough.
- *1 torinese su {n0} vive dove la fragilità è alta e i servizi sono pochi*  
  → 1 Turin resident in {n0} lives where fragility is high and services are few
- *residenti in sezioni con fragilità alta e servizi bassi: il {n0}% dei torinesi*  
  → residents in sections with high fragility and low services: {n0}% of Turin residents
- *Prezzo delle case e servizi a piedi, una zona OMI per punto ({n0} zone)*  
  → House prices and services on foot, one OMI zone per point ({n0} zones)
- *Ogni punto è una zona, grande quanto i suoi abitanti. La linea è la tendenza: ogni 10 punti di servizi in più, {n0} euro al m² in più.*  
  → Each point is a zone, sized by its inhabitants. The line is the trend: for every 10 extra service points, {n0} euro per m² more.
- *Sezioni abitate di Torino, senza le zone quasi disabitate. Fragilità alta = indice sopra {n0} su 100 (il 20% più alto); servizi bassi = punteggio fino a {n1} su 100 (il 20% più basso).*  
  → Inhabited sections of Turin, without the almost uninhabited areas. High fragility = index above {n0} out of 100 (the highest 20%); low services = score up to {n1} out of 100 (the lowest 20%).
- *{n0} ({n1} sezioni)*  
  → {n0} ({n1} sections)
- *{s0} km dal centro*  
  → {s0} km from the centre
- *({n0} zone con metro, {n1} senza)*  
  → ({n0} zones with metro, {n1} without)
- *Unità: le {n0} zone OMI di Torino con almeno {n1} abitanti. Le sezioni si sommano nella zona, pesate per abitanti.*  
  → Unit: the {n0} OMI zones of Turin with at least {n1} inhabitants. Sections are added up within the zone, weighted by inhabitants.
- *Doppio svantaggio = fragilità nel 20% più alto e servizi nel 20% più basso. Soglie fissate prima dei numeri: {n0} e {n1}.*  
  → Double disadvantage = fragility in the highest 20% and services in the lowest 20%. Thresholds fixed before the numbers: {n0} and {n1}.
- *{n0} zone OMI di Torino, almeno {n1} abitanti*  
  → {n0} OMI zones of Turin, at least {n1} inhabitants
- *indice sopra {n0} su 100 (sezioni) / {n1} (zone)*  
  → index above {n0} out of 100 (sections) / {n1} (zones)
- *punteggio fino a {n0} su 100 (sezioni) / {n1} (zone)*  
  → score up to {n0} out of 100 (sections) / {n1} (zones)
- *fermata M1 entro {n0} m dal centro della zona*  
  → M1 stop within {n0} m of the zone centre
- *{n0} km da Piazza Castello*  
  → {n0} km from Piazza Castello
- *Circa {n0} torinese su {n1} vive in sezioni con fragilità alta e servizi bassi ({n2}% dei residenti).*  
  → About {n0} in {n1} Turin residents live in sections with high fragility and low services ({n2}% of residents).
- *A 5 minuti solo {a0}{n0}% dei residenti ha tutti e 5 i servizi; a 10 minuti {a1}{n1}%.*  
  → Within 5 minutes only {n0}% of residents have all 5 services; within 10 minutes {n1}%.
- *{n0} residenti ({n1}%) vivono a meno di {n2} m da una strada molto trafficata.*  
  → {n0} residents ({n1}%) live less than {n2} m from a very busy road.
- *I {n0} residenti senza 3 o più servizi sono in {n1} {t2} di collina: dove manca davvero tutto.*  
  → The {n0} residents without 3 or more services live in {n1} hillside {t2}: where really everything is missing.
- *Oltre 10 minuti di ritardo: {n0}% dei passaggi a ogni fermata, {n1}% se si guarda solo la partenza.*  
  → More than 10 minutes late: {n0}% of arrivals at every stop, {n1}% if we look only at departure.
- *La linea più in ritardo è la {s0}: {n1}% dei passaggi feriali oltre 5 minuti.*  
  → The line with the most delays is line {s0}: {n1}% of weekday arrivals more than 5 minutes late.
- *I tram arrivano più a grappolo dei bus: {n0}% delle coppie di mezzi contro {n1}% (feriale).*  
  → Trams bunch more than buses: {n0}% of vehicle pairs versus {n1}% (weekday).
- *Interscambi esistenti: pieni {w0}; poco usati {w1}.*  
  → Existing park-and-ride lots: full {w0}; little used {w1}.
- *{n0} fermate importanti su {n1} non hanno posti bastanti a {n2} metri a piedi.*  
  → {n0} important stops out of {n1} do not have enough parking within {n2} metres on foot.
- *Il punto più promettente è {s0}: bastano {s1} minuti perché il bus pareggi l'auto.*  
  → The most promising point is {s0}: {s1} minutes are enough for the bus to match the car.
- *Le auto con rapporto oltre 2 sono il {n0}% con il fattore basso e il {n1}% con il fattore alto.*  
  → Cars with a ratio above 2 are {n0}% with the low factor and {n1}% with the high factor.
- *Le 3 coppie peggiori: {s0}.*  
  → The 3 worst pairs: {s0}.
- *Google conferma i tempi coi mezzi pubblici sui percorsi di controllo: {w0} minuti.*  
  → Google confirms the public transport times on the check routes: {w0} minutes.
- *Prezzo e servizi vanno insieme: correlazione di Spearman {n0} su {n1} zone (da {n2} a {n3}).*  
  → Price and services go together: Spearman correlation {n0} over {n1} zones (from {n2} to {n3}).
- *{n0} zone sono in doppio svantaggio: {w1}. Ci abitano {n2} persone.*  
  → {n0} zones are in double disadvantage: {w1}. {n2} people live there.
- *Vicino alla metro le case costano {t0} ({p1} euro al m² in media, a pari distanza dal centro). Differenza fra zone, non effetto causale.*  
  → Near the metro homes cost {t0} ({p1} euro per m² on average, at the same distance from the centre). A difference between zones, not a causal effect.

### Parole e frasi brevi

*residenti* → residents; *minuti* → minutes; *volte* → times; *posti* → spaces; *auto* → cars; *feriale* → weekday; *sabato* → Saturday; *domenica* → Sunday; *domeniche* → Sundays; *salute* → health; *scuole* → schools; *fermate* → public transport stops; *verde* → green space; *limite basso* → low limit; *limite alto* → high limit; *il doppio* → twice as long; *bisogno alto* → high need; *Zone* → Zones; *Residenti* → Residents; *Periodo* → Period; *Fasce* → Bands; *puntuali* → on time; *sera (19-24)* → evening (19-24); *tendenza* → trend; *Metro vicina* → Metro nearby; *sezione* → section; *sezioni* → sections; *poco di più* → a little more; *di più* → more; *non di più* → no more
