# Qualità dei dati raccolti

origine: agente GT09-qualita | stato: bozza

Questo documento riassume i numeri di `agenti/GT09-qualita/STATISTICHE.md`, generato il 2026-10-05 alle 02:38 (il file non dice se l'ora è locale o UTC). Ogni numero citato qui viene da quel file. Quando il file non dice una cosa, qui trovi scritto "non risulta".

Gli orari del database sono in UTC. Torino è UTC+2 finché dura l'ora legale (+1 d'inverno). Un orario "16h" nelle tabelle vuol dire circa le 18 a Torino.

Periodo coperto:
- Mezzi GTT: dal 2026-10-03 23:43 al 2026-10-05 00:22 (UTC).
- Sensori 5T: dal 2026-10-03 23:41 al 2026-10-05 00:37 (UTC).
- In entrambi i casi è poco più di un giorno di dati. Sulla mappa resta quindi l'etichetta "dati scarsi" (meno di 72 ore non basta).

## Cosa funziona

- **La raccolta dei mezzi GTT è regolare.** Ci sono 1409 letture. L'intervallo mediano è 61 secondi, e il progetto prevede una lettura al minuto. Quasi tutte le ore hanno 59 letture (18h ne ha 60).
- **Ogni lettura contiene tanti mezzi.** Per lettura il minimo è 1, la mediana 201 e il massimo 261. In tutto il database ci sono 386 veicoli distinti su 82 linee.
- **L'andamento della giornata è credibile.** I mezzi medi in servizio sono pochi di notte (01h: 7) e crescono al mattino (03h: 75, 04h: 141). Il massimo è nel pomeriggio (16h: 256) e poi calano (23h: 44).
- **I sensori di traffico 5T arrivano completi.** Sono 109 in anagrafica e tutti e 109 compaiono nei dati. Le letture sono 287 e l'intervallo mediano è 301 secondi (atteso 300). Le righe sono 31283, cioè 109 sensori per 287 letture, quindi in ogni lettura c'erano tutti i sensori.
- **Nessun valore mancante nei 5T.** Flusso e velocità hanno 0 valori NULL.
- **Anche il traffico ha un andamento credibile.** Il flusso medio è basso di notte (02h: 80.4) e alto nel pomeriggio (16h: 589.6). La velocità media scende quando il flusso sale (16h: 60.9 contro 02h: 70.5). Il file non dice in quale unità sono flusso e velocità.
- **Gli errori registrati sono pochissimi.** La tabella errori ha una sola riga: «HTTP Error 503: Service Unavailable» del 2026-10-04 alle 21:30 (GTT).
- **I numeri sono coerenti tra loro.** I sensori per accuratezza sommano a 109 (49 + 2 + 18 + 40), e le righe per accuratezza sommano a 31283. Le righe con flusso>0 per accuratezza sommano a 24687, come il totale.
- **Il database è piccolo.** Pesa 28.3 MB.

## Problemi trovati

### 1. I campi "corsa" e "velocita'" dei mezzi GTT sono sempre vuoti
- **Evidenza.** La tabella `mezzi_gtt` ha 233399 righe. In 233399 (100%) la corsa (trip) è vuota. In 233399 (100%) la velocità non è misurata (NULL). Questo conferma quanto già sapevamo.
- **Perché conta per la mappa.**
  - Senza la corsa non si può collegare in modo sicuro un mezzo reale a una corsa dell'orario. Ritardi e confronto orario/reale non sono quindi misurabili con questi dati.
  - Senza la velocità, ogni velocità dei mezzi mostrata sulla mappa sarebbe una stima ricavata dalle posizioni. Non sarebbe una misura, e va etichettata così.
- **Cosa non risulta.** STATISTICHE.md non dice se la fonte GTT offre questi dati e non vengono letti, o se la fonte proprio non li dà.

### 2. Molti sensori 5T dichiarano accuratezza 0
- **Evidenza.** Accuratezza dichiarata (valore: n. sensori): 0.0: 49, 80.0: 2, 95.0: 18, 100.0: 40. Quindi 49 sensori su 109 (circa il 45%) hanno accuratezza 0.
- **Cosa fanno quei sensori.** Hanno 14063 righe, e in 8997 il flusso è maggiore di zero. Anche con accuratezza 0 producono quindi molti valori. Per confronto, i valori con flusso>0 sono:
  - 574 su 574 per i sensori con 80.0;
  - 4826 su 5166 per quelli con 95.0;
  - 10290 su 11480 per quelli con 100.0.
- **Perché conta per la mappa.** Non sappiamo se "0" significa "sensore poco affidabile" oppure "accuratezza non dichiarata". Se la mappa mostra questi sensori come misure normali, può dare un'impressione di precisione che non abbiamo verificato.
- **Cosa non risulta.** Il significato del valore 0 non è nei dati.

### 3. Buchi nelle letture dei mezzi GTT
- **Evidenza.** I buchi più lunghi, senza nessuna lettura, sono:
  - 18.2 min da 04/10 00:55 a 01:13;
  - 11.1 min da 04/10 21:35 a 21:46;
  - 11.1 min da 04/10 01:16 a 01:27;
  - 7.0 min da 04/10 00:37 a 00:44;
  - 6.0 min da 03/10 23:49 a 23:55.
- **Effetto sulle ore.** Le ore toccate dai buchi hanno meno letture delle altre: 01h ne ha 37 e 21h ne ha 48, contro 59 delle ore normali. I due fatti sembrano collegati, ma qui è una mia lettura dei numeri, non una cosa scritta nel file.
- **Lettura quasi vuota.** Il minimo di mezzi per lettura è 1. Non risulta quando è successo né perché (può essere un buco parziale della fonte).
- **Perché conta per la mappa.** Durante un buco i mezzi sulla mappa restano fermi all'ultima posizione nota, e il replay o le statistiche possono saltare dei minuti. Questo va detto chiaramente, senza riempire il vuoto con valori inventati.
- **Cause.** Nella tabella errori c'è un solo errore, un 503 alle 21:30 del 04/10. Il buco delle 21:35 inizia 5 minuti dopo. Non risulta se i due fatti siano collegati. Per gli altri buchi non risulta nessun errore registrato, quindi la causa non è nota.

### 4. Storia molto breve e poco varia
- **Evidenza.** I dati coprono poco più di 24 ore (dal 03/10 23:43 al 05/10 00:22 per i mezzi). Quasi ogni ora del giorno è rappresentata una volta sola (solo 23h e 00h compaiono due volte: 23h: 72 letture, 00h: 71).
- **Calendario.** Dal calendario, il 4 ottobre 2026 è una domenica. Quasi tutto il periodo è quindi un giorno festivo. STATISTICHE.md non lo dice: è una verifica mia, da controllare.
- **Perché conta per la mappa.** Le medie per ora (mezzi e flussi) valgono per un solo giorno, probabilmente festivo, e non per un giorno feriale tipico. Restano "dati scarsi" e vanno mostrate così.

### 5. Nei sensori 5T lo zero è ambiguo e alcuni sensori non mostrano mai traffico
- **Evidenza.**
  - Il 79% delle righe ha flusso>0 (24687 su 31283). Il restante 21% (6596 righe) ha flusso 0, perché i valori NULL sono 0.
  - Le righe con velocità>0 sono 24687, lo stesso numero di quelle con flusso>0.
  - 97 sensori su 109 hanno mostrato flusso>0 almeno una volta, quindi 12 non l'hanno mai mostrato.
- **Perché conta per la mappa.** Non possiamo distinguere "nessuna auto in quei 5 minuti" da "sensore spento o senza dati". Se le righe con zero vengono mostrate come "traffico zero", la mappa dà una misura che potrebbe non essere vera.
- **Medie per ora.** Nelle medie per ora di STATISTICHE.md sono contate solo le righe con flusso>0. Di notte sono quindi più alte di quelle reali, perché non includono gli zeri.
- **Cosa non risulta.** Quali sono i 12 sensori senza flusso (e che accuratezza hanno) e quali sono le unità di misura.
- **Buchi.** Dal periodo (circa 25 ore) e dall'intervallo atteso (300 s) mi aspetterei circa 300 letture. Ne risultano 287. È un mio calcolo approssimativo: STATISTICHE.md non elenca buchi nei 5T.

## Cosa non sappiamo ancora

- Cosa significhi davvero accuratezza 0 per i 49 sensori 5T (non misurabile da questi dati).
- Quali siano i 12 sensori 5T che non hanno mai mostrato flusso>0, e se siano guasti o solo in strade poco trafficate.
- Se flusso 0 voglia dire "nessun veicolo" oppure "dato non disponibile".
- Perché la fonte GTT non dà corsa e velocità, o se la raccolta le scarta: non risulta.
- La causa dei buchi GTT, tranne forse quello delle 21:35 (un solo errore 503 registrato, 5 minuti prima).
- Quanto dura e quando è avvenuta la lettura GTT con un solo mezzo.
- Se ci sono buchi nei dati 5T (non elencati nel file).
- Come si comportano i dati nei giorni feriali, nei weekend e nei periodi con maltempo o scioperi: la storia è troppo corta.
- Le unità di misura di flusso e velocità dei 5T: non risultano da STATISTICHE.md.
- Se l'orario del file (02:38) è locale o UTC. L'ultima lettura GTT è alle 00:22 e l'ultima 5T alle 00:37 (UTC), e non risulta se la raccolta fosse ancora attiva al momento del calcolo.

## Prossimi passi consigliati

1. **Controllare se la fonte GTT offre corsa e velocità** (FACILE). Si guarda `docs/FONTI_DATI.md` o la risposta grezza della fonte. È il passo di maggior valore perché da lì dipendono ritardi e velocità reali. Se non li offre, va scritto nel documento delle fonti.
2. **Lasciare girare la raccolta almeno 72 ore, meglio 2-3 settimane con giorni feriali** (FACILE). Basta non spegnere il PC. Poi rifare queste statistiche e togliere l'etichetta "dati scarsi" solo quando i numeri lo permettono.
3. **Stimare la velocità dei mezzi dalle posizioni successive** (MEDIO). Distanza diviso tempo tra due letture, sempre etichettata "stimata dalle posizioni" e mai presentata come misura. Va tenuto conto dei buchi per non calcolare velocità tra letture troppo lontane.
4. **Mostrare i sensori 5T con accuratezza 0 e i flussi a zero in modo prudente** (MEDIO). Ad esempio un simbolo o un'etichetta "affidabilità non dichiarata", senza nasconderli. Prima conviene confrontare alcuni di questi sensori con la loro storia, per capire se lo zero è un dato vero.
5. **Far registrare i buchi e gli errori dalla raccolta** (MEDIO). Oggi un solo errore spiega pochi minuti su tanti buchi. Richiede una modifica a uno script protetto (`scripts/03_raccolta_continua.py`): non è stata fatta, va decisa da Leo.
6. **Segnalare i buchi nei dati sulla mappa e nel replay** (MEDIO). Invece di far sembrare continuo un periodo senza letture, indicare "nessun dato" per quei minuti.
