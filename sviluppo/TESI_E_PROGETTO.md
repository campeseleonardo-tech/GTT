# Da dove nasce il progetto: la tesi del 2020 e la verifica sui dati di Torino

Documento di racconto (per README, LinkedIn, presentazioni), non di metodo.

**Tesi:** *The effects and applications of Industry 4.0 on Smart Cities*, laurea triennale in Business and Management,
Università di Torino, anno accademico 2019/2020. Rassegna della letteratura, senza parte empirica.

## Il racconto in una riga

Nel 2020 la tesi raccontava come sensori e dati avrebbero cambiato le città. Sei anni dopo, con un po' di tempo
libero, il progetto ha costruito un piccolo sistema che raccoglie i dati di Torino ogni minuto, per metterli alla
prova: cosa dicono davvero, e dove l'IoT e la «smart city» mostrano i loro limiti.

**La tesi era la promessa, il progetto è la verifica.**

## Le cornici della tesi applicate al progetto

| Nella tesi | Nel progetto |
|---|---|
| IBM: città «instrumented, interconnected, intelligent» | strumentata = GPS dei bus e sensori 5T; interconnessa = feed raccolti dal Raspberry Pi ogni minuto; intelligente = analisi, mappa, schede |
| UE 2013: «collecting, communicating, crunching» | raccolta su Raspberry Pi → storico SQLite → script e mappa |
| IoT a 6 livelli | percezione = GPS GTT e spire 5T; rete = feed GTFS-RT e XML; middleware = Raspberry Pi e SQLite; applicazione = mappa e schede; **business = manca** |
| Big Data, le «3V» | velocità = una lettura al minuto; volume = oltre 2 GB, circa 190 MB al giorno; varietà = GPS, sensori, censimento, indagine sugli spostamenti, prezzi delle case |
| Smart governance: open data | il progetto usa **solo** dati aperti: mostra cosa permettono e cosa manca |

## Temi della tesi che il progetto ha messo alla prova

| Tema della tesi | Dove torna |
|---|---|
| Gestione del traffico, sensori e semafori | Risultato «traffico e mezzi pubblici»: coi mezzi si impiega da 2 a 3 volte l'auto |
| Trasporto pubblico e localizzazione automatica dei bus (AVLS) | Risultato «puntualità»: i ritardi misurati proprio col GPS dei mezzi |
| Gestione dei parcheggi e sensori dei posti liberi | Risultato «parcheggi di scambio»: riempimento dai sensori 5T, minuti di pareggio |
| Città sovraffollata e qualità della vita | Risultato «servizi a piedi»: 5, 10, 15 minuti; esposizione al traffico |
| Questione sociale: «i problemi urbani sono sociali» (critica alla smart city delle grandi aziende) | Risultato «case, servizi e fragilità»: doppio svantaggio |
| Sicurezza e privacy | regole del progetto: niente dati personali, mai la nazionalità |
| Merci, rifiuti, acqua, energia | fuori dal progetto |

## Cosa ha mostrato la verifica (i limiti dell'IoT e della smart city, con casi veri)

- **I dati ci sono, il problema è la qualità**: il feed dei ritardi GTT smette di aggiornare la fermata e sottostimava i
  ritardi di 2-3 volte (il progetto è passato al GPS); un contatore di parcheggio è fermo; un mezzo ha l'orologio tre
  anni avanti; il feed tempo reale si è fermato per una mattina.
- **Pochi dati aperti davvero utili**: 5T pubblica solo 3 feed (traffico, parcheggi, ZTL ferma al 2024); per l'aria solo
  medie annuali; nessun dato sui passeggeri; treni e bus di altre aziende assenti dai dati usati.
- **Pochi sensori, stime deboli**: 20 punti di confronto per il traffico, modello con errore di circa ±38%; i tempi in
  auto vanno chiusi in una forbice fra sensori e Google Maps.
- **Il risultato più forte non è tecnologico ma sociale**: dove fragilità e pochi servizi coincidono. È la conclusione
  critica della tesi, ritrovata nei dati.

## Cosa manca per chiudere il cerchio con la tesi di Management

Il livello «business» dell'IoT: costi del servizio, valore per i soldi spesi (es. costo per passeggero di tram contro
bus; costo di un parcheggio di scambio contro i minuti risparmiati). Piano: `sviluppo/piani/PIANO_COSTI.md`.

## Dati della letteratura citati nella tesi, utili come confronto (DA VERIFICARE sulla fonte originale prima di usarli)

- «In media servono 7,8 minuti per trovare parcheggio» (tesi p. 19): confronto per il risultato dei parcheggi di
  scambio, dove il bus pareggia l'auto solo con 21-28 minuti persi in centro.
- «Il 30% delle auto in centro cerca parcheggio» (dato classico di Shoup, discusso in letteratura): solo con cautela.
- Hansen: inquinamento, incidenti e spazio occupato costano più della congestione (giustifica l'esposizione al traffico).
- SURTRAC (Pittsburgh): semafori adattivi, flusso +25-40%, emissioni −20%.

Bibliografia utile: Caragliu, Del Bo, Nijkamp 2011 (*Smart Cities in Europe*); Hollands (critica alla smart city
delle aziende); Harvey 2012 (*Rebel Cities*); Mangiaracina, Perego, Salvadori, Tumino 2017 (sistemi di trasporto
intelligenti).

## Avvertenze sulla tesi

Da riprendere le idee e le cornici, non il testo: contiene errori (es. «2,5 quintilioni di byte = 10^30»: sono 10^18),
numerazione dei capitoli ripetuta, voci doppie in bibliografia, note non allineate, immagini di terzi. Nel portfolio va
citata come punto di partenza, non messa in primo piano.

## Frase pronta per il post

«Nel 2020 la mia tesi triennale raccontava come sensori e dati avrebbero cambiato le città. Sei anni dopo ho costruito
un piccolo sistema che raccoglie i dati di Torino ogni minuto, per vedere cosa dicono davvero.»
