# Qualità dei dati raccolti finora

Documento scritto dall'agente GT09-qualita (bozza, da rivedere da Leo).
Fonte unica dei numeri: `agenti/GT09-qualita/STATISTICHE.md` (generato il 2026-10-05 alle 02:38).
Dove i numeri non dicono qualcosa, scrivo "non risulta". I pochi calcoli fatti da me (non presenti nel file) sono segnati come **(calcolo mio)**.

Nota sugli orari: le statistiche sono in ora UTC. Adesso (ora legale) Torino = UTC + 2 ore. Esempio: "16h UTC" = ore 18 a Torino.

Periodo coperto: dal 03/10 sera al 05/10 notte, cioè **circa 25 ore** (calcolo mio). Il 04/10/2026 era una **domenica**: quasi tutti i dati sono di un giorno festivo. Sotto le 72 ore la mappa deve continuare a mostrare l'etichetta **"dati scarsi"**.

---

## Cosa funziona

1. **La raccolta gira davvero, quasi senza interruzioni.**
   - Database `data/storico.sqlite` di 28.3 MB.
   - Mezzi GTT: 1409 letture dal 2026-10-03 23:43 al 2026-10-05 00:22, intervallo mediano **61 s** (cioè circa una lettura al minuto, come previsto).
   - Nella maggior parte delle ore ci sono **59 letture all'ora** (dalle 02h alle 20h UTC, e alle 22h; 60 alle 18h).
   - Le ore 00h (71) e 23h (72) hanno più di 60 letture perché il periodo le contiene due volte (due notti diverse), non per un errore.

2. **Le posizioni dei mezzi GTT arrivano in quantità sensata.**
   - 233399 righe di posizioni, **386 veicoli distinti, 82 linee distinte**.
   - Mezzi per lettura: mediana **201**, massimo **261**.
   - L'andamento orario è realistico: pochi mezzi di notte (01h UTC: 7 in media), crescita al mattino (04h: 141, 07h: 204), massimo nel pomeriggio (16h UTC: **256**, cioè le 18 a Torino), calo la sera (22h: 105, 23h: 44).

3. **I sensori 5T rispondono tutti, ogni volta.**
   - 287 letture dal 2026-10-03 23:41 al 2026-10-05 00:37, intervallo mediano **301 s** (atteso 300): il ritmo di 5 minuti è rispettato.
   - Sensori in anagrafica 109, visti nei dati **109 su 109**.
   - 31283 righe = 287 letture × 109 sensori **(calcolo mio)**: in ogni lettura sono arrivati tutti i sensori.
   - Nessun valore mancante (NULL): flusso NULL 0, velocità NULL 0.
   - 97 sensori su 109 hanno mostrato almeno una volta un flusso maggiore di 0.

4. **L'andamento del traffico 5T è coerente con quello dei mezzi GTT.**
   - Flusso medio (solo righe con flusso>0): minimo di notte (02h UTC: 80.4), massimo nel tardo pomeriggio (16h UTC: **589.6**), come il massimo dei mezzi GTT (16h UTC: 256).
   - Le velocità medie scendono quando il flusso sale (16h UTC: 60.9; 01h UTC: 71.0): comportamento atteso.

5. **Pochissimi errori registrati.** Tabella errori: 1 riga sola (GTT, «HTTP Error 503: Service Unavailable», il 2026-10-04 alle 21:30 UTC).

---

## Problemi trovati

### 1. Mezzi GTT: il campo "corsa" (trip) è sempre vuoto
- **Evidenza:** 233399 righe, con corsa vuota **233399 (100%)**. Il fatto noto è confermato.
- **Perché conta per la mappa:** senza la corsa non si può collegare un mezzo reale al suo orario programmato. Quindi non si può misurare il **ritardo**, né sapere con certezza in che direzione va il mezzo, né confrontare "previsto vs reale" sulla stessa corsa. Per ora le corse sulla mappa restano **stimate/simulate** dagli orari; i mezzi reali danno solo "dove si trova un veicolo di quella linea".

### 2. Mezzi GTT: la velocità non è mai misurata
- **Evidenza:** velocità NULL in **233399 righe su 233399 (100%)**. Il fatto noto è confermato.
- **Perché conta per la mappa:** non abbiamo una velocità misurata dei mezzi pubblici. Una velocità si potrebbe solo **calcolare** dalla distanza tra due posizioni successive dello stesso veicolo: sarebbe una **stima**, e sulla mappa va scritta come tale, non come misura.

### 3. Sensori 5T: quasi metà ha accuratezza 0
- **Evidenza:** accuratezza dichiarata (valore: numero sensori): 0.0: **49**, 80.0: 2, 95.0: 18, 100.0: 40. Quindi 49 sensori su 109 (circa il 45%, calcolo mio). Il fatto noto è confermato.
- Curiosità: i sensori con accuratezza 0 non sono "muti": hanno flusso>0 in 8997 righe su 14063 (circa 64%, calcolo mio). Per confronto: accuratezza 100 → 10290 su 11480 (circa 90%), 95 → 4826 su 5166 (circa 93%), 80 → 574 su 574 (100%).
- **Perché conta per la mappa:** quei 49 sensori mandano numeri, ma il gestore stesso dichiara accuratezza 0. Se la mappa li mostra uguali agli altri, Leo vedrebbe come "misurato" un dato di affidabilità sconosciuta. Vanno distinti (es. colore diverso o avviso).

### 4. Sensori 5T: lo 0 potrebbe voler dire "nessun dato" e non "strada vuota"
- **Evidenza:** flusso NULL 0 e velocità NULL 0, ma righe con flusso>0 = **24687** e righe con velocità>0 = **24687**: esattamente lo stesso numero (79% delle 31283). Inoltre **12 sensori** (109 − 97, calcolo mio) non hanno mai mostrato flusso>0 in circa 25 ore.
- **Perché conta per la mappa:** se lo 0 fosse "nessun veicolo passato", la velocità non sarebbe sempre 0 insieme al flusso in modo così preciso. È probabile (ma **da_verificare**) che 0/0 significhi "dato non disponibile". Se la mappa colora quei sensori come "traffico nullo", mostra un'informazione falsa. Le medie orarie nel file usano già solo le righe con flusso>0, ed è la scelta prudente.

### 5. Buchi nella raccolta GTT di notte, quasi senza errori registrati
- **Evidenza:** buchi più lunghi: **18.2 min** (04/10 00:55–01:13 UTC), **11.1 min** (04/10 01:16–01:27), **11.1 min** (04/10 21:35–21:46), 7.0 min (04/10 00:37–00:44), 6.0 min (03/10 23:49–23:55). Le ore toccate hanno meno letture: 01h UTC: **37** invece di circa 59, 21h UTC: **48**. In ora di Torino i buchi sono tra le 01:49 e le 03:27 di notte, e alle 23:35 circa.
- La tabella errori ha **1 sola riga** (503 alle 21:30 UTC), vicina al buco delle 21:35 ma non uguale. Per i buchi delle 00:37–01:27 UTC nella tabella errori **non risulta nulla**.
- **Perché conta per la mappa:** i buchi cadono di notte, quando i mezzi sono pochi (01h UTC: 7 in media), quindi l'impatto oggi è piccolo. Ma la raccolta non registra il motivo di ogni buco: se in futuro capitano di giorno, la mappa (e il replay) mostrerebbe "pochi mezzi" quando in realtà mancano le letture. I buchi andrebbero segnati, non scambiati per "nessun mezzo".

### 6. Mezzi per lettura: minimo 1
- **Evidenza:** mezzi per lettura: minimo **1**, mediana 201.
- **Perché conta per la mappa:** una lettura con 1 solo mezzo può essere una notte molto tranquilla oppure una risposta incompleta del servizio GTT. Dalle statistiche **non risulta** in che ora sia capitata. Se fosse una risposta incompleta, nel replay apparirebbe come un "crollo" del servizio che non è avvenuto.

### 7. Lettura 5T: qualche lettura in meno del previsto
- **Evidenza:** 287 letture in circa 24 ore e 56 minuti; a una ogni 5 minuti ne servirebbero circa 300 **(calcolo mio)**, quindi ne mancano circa 13. Le statistiche non danno i buchi del 5T: per quando mancano **non risulta**.
- **Perché conta per la mappa:** impatto piccolo (circa 4%), ma va tenuto presente quando si fanno medie orarie.

### 8. Storico molto breve e quasi tutto di domenica
- **Evidenza:** circa 25 ore di dati, 04/10/2026 = domenica.
- **Perché conta per la mappa:** le medie orarie (mezzi in servizio, flussi 5T) descrivono **una domenica**, non un giorno feriale. Non vanno usate come "giorno tipo". Resta valida l'etichetta "dati scarsi" (sotto 72 ore).

---

## Cosa non sappiamo ancora

- **Come è un giorno feriale:** non risulta, abbiamo quasi solo una domenica.
- **Se la raccolta regge giorni interi senza fermarsi:** abbiamo solo circa 25 ore.
- **Il motivo dei buchi notturni** (00:37–01:27 UTC del 04/10): nella tabella errori non risulta nulla. Possibili cause (non verificate): PC in sospensione, rete, servizio GTT. **Da_verificare** nei log.
- **Cosa significa esattamente lo 0 nei dati 5T** (strada vuota o dato assente): da_verificare nella documentazione 5T.
- **Cosa vuol dire "accuratezza 0" per 5T** (sensore guasto, dato stimato, valore non compilato?): non risulta.
- **Quali sono i 12 sensori sempre a zero** e che accuratezza hanno: non risulta dalle statistiche.
- **Unità di misura di flusso e velocità 5T:** non risulta nel file statistiche (probabilmente veicoli/ora e km/h, ma da_verificare). Le velocità medie di 58–71 sembrano alte per strade urbane: forse molti sensori sono su strade veloci, da_verificare.
- **Se i dati GTT "corsa" e "velocità" esistono alla fonte** ma non vengono salvati, oppure se GTT non li fornisce proprio: non risulta.
- **In che ora è capitata la lettura con 1 solo mezzo:** non risulta.
- **Buchi e letture per ora dei sensori 5T:** non risultano (le statistiche li danno solo per GTT).

---

## Prossimi passi consigliati

1. **Mostrare sulla mappa i sensori 5T con accuratezza 0 in modo diverso** (es. grigio chiaro con scritta "affidabilità non dichiarata") e trattare 0/0 come "nessun dato", non come "traffico nullo". — **MEDIO** (modifica al template della mappa e allo script che prepara i dati).
2. **Lasciar girare la raccolta almeno 7 giorni** (feriali compresi) e poi rifare queste statistiche, per avere un giorno feriale vero e superare le 72 ore. — **FACILE** (basta aspettare e rilanciare lo script).
3. **Controllare nei log e nelle impostazioni del PC il motivo dei buchi notturni** (sospensione, aggiornamenti, rete). — **FACILE**.
4. **Verificare alla fonte se GTT fornisce "corsa" e "velocità"**: se sì, va corretto il raccoglitore; se no, calcolare la velocità dalle posizioni e mostrarla come **stima**. — **DIFFICILE** (tocca il raccoglitore, che è un file protetto: serve l'ok di Leo e va fatto a raccolta ferma).
5. **Far registrare al raccoglitore ogni lettura fallita o vuota** (non solo gli errori HTTP), così i buchi sono visibili nel replay come "dati mancanti". — **MEDIO** (anche qui file protetto: serve decisione di Leo).
6. **Aggiungere alle statistiche i buchi del 5T, l'elenco dei 12 sensori sempre a zero e l'ora della lettura con 1 solo mezzo.** — **FACILE**.
