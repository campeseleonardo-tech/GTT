# Analisi completa del Risultato 6 — parcheggi di interscambio («Parcheggi per lasciare l'auto»)

Scritta da Claude il 19/10/2026 su richiesta di Leo. L'analisi generale del progetto è in
`docs/ANALISI_PROGETTO.md`. Fonti: `PIANO_RISULTATO6.md` e tutti i piani/esiti/rapporti R6, gli script 68-80, e i
dati del Risultato 6 dentro `mappa_torino.html` (378 fermate, 212 parcheggi, 73 aree, 20 punti), che ho ricontato.
Non avevo `data/` né il database: non ho rilanciato gli script.

## 0. In breve

- **Il lavoro sui dati è serio**: inventario di 5.205 parcheggi da tre fonti, verifiche indipendenti, v1 sempre
  riproducibile, sensibilità dichiarate, osservazioni di Leo tenute fuori dai dati, e il coraggio di scrivere
  «interscambi di fatto: zero».
- **Ma il risultato finale non risponde alla domanda che si è dato** («togliere auto dalla circolazione»):
  misura **dove ci sono parcheggi vicino alle fermate molto servite**, cioè soprattutto **quanto è densa la città**.
- **Tre prove**:
  1. **10 dei 20 punti prioritari** (e 108 delle 378 fermate importanti) stanno nei quartieri **Q002-Q009**, che lo
     stesso progetto considera «zona centrale» per i parcheggi; 7 punti su 20 sono a meno di 2,5 km da Piazza
     Castello. Un interscambio lì attira auto verso il centro invece di fermarle prima.
  2. Il segnale dei pendolari (c2) per i quartieri di Torino conta **le auto che ci arrivano**, non quelle che
     ne partono: premia i luoghi di **destinazione**.
  3. **Il metodo non riconosce i fatti noti**: Fermi (pieno, secondo Leo) sta in un'area «Buona»; Caio Mario,
     interscambio quasi vuoto, è accanto al punto prioritario n. 10 e a 1-2 km dai n. 1 e 2.
- **Il riempimento misurato non entra nel risultato**: il rilancio dopo il 25/10 cambierà colori e profili, non
  206/378, le aree o i 20 punti.
- **La cosa più solida e interessante** che il Risultato 6 ha trovato è un'altra: **dei 4 interscambi del
  Comune solo Stura si comporta da interscambio** (pieno di giorno); Caio Mario è quasi vuoto, Sofia è usato di
  notte (residenti), Venchi Unica ha il dato fermo. È un fatto misurato, ed è una buona storia.
- **Proposta**: ripartire dalle **auto che entrano in città** e dai **corridoi** che percorrono, e chiedersi dove
  potrebbero essere fermate prima, vicino a un mezzo veloce (sezione 6). In alternativa, 7 correzioni mirate
  (sezione 7).

---

## 1. L'obiettivo e come è cambiato

| Data | Domanda | Cosa si contava |
|---|---|---|
| 14/10 (v1) | I 4 interscambi ufficiali sono vicini alle fermate più critiche per chi arriva dalla cintura? Nessun parcheggio nuovo. | 611 fermate critiche (10% più alto di 3 percentili), 17 coperte entro 200 m |
| 18/10 (proposta v2) | + quanto ogni parcheggio fa **davvero** da interscambio (posizione, uso orario, prezzo) | luoghi = fermate entro 40 m; tutti i parcheggi; 7 segnali; 3 scenari |
| 19/10 giro 1-2 | come sopra, con strade corrette, universo Città metropolitana, b2 | S2: 378 luoghi critici, 140 coperti da parcheggi «di fatto/potenziali»; «di fatto» = 0 |
| 19/10 «porte» | Dove mancano posti **vicino a dove si entra in città o nel TP**? Per decidere **dove mettere o ingrandire** un parcheggio | porte = zone IMQ; posti utili; osservazioni di Leo |
| 19/10 «direzioni» | idem; **i quartieri di Torino non vanno esclusi** (obiettivo: togliere auto) | 8 settori; domanda = auto in entrata × 26% |
| 19/10 «zone» → «migliorie» (finale) | idem | aree esagonali, 20 punti, 212 parcheggi mostrati, «utile» tolto |

Due cose da notare:
- **La domanda è passata da «verifico l'esistente» a «dove costruire»**, ma il metodo è rimasto quello della v1
  (punteggio delle fermate + parcheggi entro 200 m). Una domanda di pianificazione ha bisogno di una stima della
  domanda di interscambio, che non c'è.
- **L'obiettivo dichiarato è togliere auto dalla circolazione**, ma nessun numero del risultato misura auto
  tolte.

## 2. Il metodo attuale, passo per passo

1. **Luoghi**: le 7.045 fermate GTT unite se entro 40 m → 5.087 luoghi; universo = Città metropolitana (4.425).
2. **Punteggio di ogni luogo** (scenario S2) = media dei percentili di 7 segnali:
   - a1 = importanza del corridoio (script 24, 1-5); a2 = importanza della strada dal lavoro sul traffico (1-5,
     +1 se asse d'ingresso);
   - b2 = corse/ora nelle ore dei pendolari (GTFS, feriale);
   - c1 = pendolari IMQ della zona (tutti i mezzi, due versi); c2_ztl = auto che entrano a Torino al mattino
     **che toccano la zona** (come origine o destinazione), + quelle dirette nella ZTL contate due volte;
   - d = calo di velocità ai sensori 5T vicini (solo 92 luoghi); e = 100 se metro o stazione entro 300 m, se no 0.
3. **Fermate importanti** = il 10% più alto, fuori dalla zona Q001 → **378**.
4. **Parcheggi**: 5.205 trovati → 3.431 aperti (esclusi lungo strada, solo clienti, privati); posti dichiarati
   (374) o stimati a 25 m² a posto (2.902).
5. **Copertura**: somma dei posti nominali entro **200 m** in linea d'aria: 0 = nessun parcheggio, 1-49 = pochi,
   50+ = coperta. Il riempimento non conta.
6. **Aree**: esagoni di ~2 km²; Critica se ≥ 60% delle fermate non ha 50 posti.
7. **20 punti**: fermate non coperte raggruppate entro 1 km, ordinate per **somma** dei punteggi; per ognuno i
   parcheggi ≥ 100 posti entro 600 m («potrebbero ampliarsi»).
8. **Riempimento** (solo colori e profili): 5T, media feriale 10-16 di 2 giorni.
9. **Direzioni** (solo riferimento): 8 settori; domanda = auto in entrata × 26%.

## 3. I risultati

- **206 fermate importanti su 378 senza 50 posti a 200 m** (147 senza nessun parcheggio).
- **73 aree**: 37 critiche, 12 scarse, 24 buone.
- **20 punti**: Settembrini, Pavese (Mirafiori Sud), Industria (San Donato), Metro Spezia, Provana (Collegno),
  Metro Lingotto, Politecnico, Stati Uniti, Metro Principi d'Acaja, Traiano…
- **9 parcheggi pieni di giorno** (3.041 posti); il riempimento copre il 25% dei posti mostrati.
- **I 4 interscambi del Comune**: Stura pieno di giorno (90%) e anche di notte (80%); Caio Mario 1,5% (forse
  contatore fermo); Sofia più pieno di notte (55%) che di giorno (32%); Venchi Unica fermo al 51%. Fermi non
  trasmette.

## 4. Cosa funziona

- **Inventario dei parcheggi** da 5T, Comune e OpenStreetMap, con tipo, tariffa, posti e nota su ogni dato.
- **Controlli indipendenti** (luoghi rifatti con un altro metodo, b2/c2 ricalcolati a mano, superfici con
  shapely) e **riproducibilità della v1** (611/17/594) a ogni giro.
- **Le strade** (giro 2): niente più «stradina di servizio a 2 m» al posto di Strada Genova.
- **La «firma» oraria dei parcheggi** (pendolare / residenziale / dato fermo): è l'idea più originale, e il
  profilo a 24 ore è il grafico più chiaro (lo ha detto anche Leo).
- **Onestà**: «interscambi di fatto: zero», sensibilità scritte in scheda, osservazioni di Leo fuori dai dati.

## 5. I problemi (dal più grave)

### P1. L'indicatore non misura l'obiettivo
«Fermata molto servita senza un parcheggio da 50 posti a 200 m» non vuol dire «qui si potrebbero togliere auto».
Nelle città dense quasi nessuna fermata ha un parcheggio a 200 m, ed è normale. Per togliere auto serve sapere
**quante auto passano da lì, dove vanno, e se a loro conviene lasciare l'auto**. Nessuno di questi tre elementi
è nel risultato finale (le direzioni ci provano, ma vedi P10).

### P2. Il risultato premia il centro e la densità
Ricontato sui dati della mappa:
- **108 delle 378 fermate importanti (29%) e 10 dei 20 punti prioritari** sono nei quartieri San Salvario,
  Crocetta, San Paolo, Cenisia, San Donato, Aurora, Vanchiglia, Nizza Millefonti (Q002-Q009). Per i **parcheggi**
  il progetto ha deciso (giro 2) che queste zone sono «centrali» e non possono essere interscambi; per le
  **fermate** il centro è solo Q001. Le due regole si contraddicono.
- **7 dei 20 punti sono a meno di 2,5 km da Piazza Castello** (Stati Uniti, Metro Principi d'Acaja, Industria,
  Metro Nizza, Politecnico, Metro Bernini, Avellino).
- Le fermate **senza** parcheggio stanno in media più vicine al centro (mediana 5,4 km) di quelle coperte
  (6,4 km): il risultato segue la densità della città, perché dove la città è fitta non c'è spazio per i
  parcheggi a raso.
Un interscambio nel semicentro ha l'effetto opposto a quello voluto: le auto fanno quasi tutto il percorso in
città e si fermano a 2 km dalla destinazione.

### P3. Il segnale dei pendolari premia le destinazioni
In `73_segnali_criticita.py` (`zone_c2_c3`) ogni auto che entra a Torino al mattino viene sommata **sia alla zona
di partenza sia a quella di arrivo** (`for z in (par, arr)`); lo stesso fa c1. Per un comune di cintura c2 sono
le auto che partono (giusto); per un quartiere di Torino sono **le auto che arrivano** (l'opposto di ciò che
serve a un interscambio). I residenti di Torino che vanno in centro in auto, a cui pensava Leo il 19/10, non
sono contati affatto (il filtro esclude le partenze dai quartieri `Q`).

### P4. Il punteggio pesa cose diverse in modo nascosto
- **Doppioni**: a1 e a2 misurano entrambe l'importanza della strada, c1 e c2_ztl entrambe i pendolari della
  zona. Su 6-7 segnali, strada e pendolari valgono due volte ciascuno.
- **e vale 0 o 100**, non è un percentile come gli altri: da solo sposta 95 fermate.
- **Segnali mancanti**: a2 manca in 1.822 luoghi su 5.087 (36%), c2 in 623, d quasi ovunque. Dove manca, la
  media si fa sugli altri: un luogo senza auto in entrata non prende 0, il segnale semplicemente sparisce.
- **c2 ha meno di 30 interviste** in 2.943 luoghi (58%), completati con proporzioni ISTAT 2011.
- **Valori uguali per tutta la zona**: Moncalieri, che nell'IMQ è una zona sola, ha **64 delle 378 fermate
  importanti (17%)**.
- **Ogni segnale principale da solo sposta un terzo del risultato** (togliendone uno cambiano 95-146 fermate su
  378; solo d, che c'è in pochi luoghi, ne sposta 10): la lista dipende più dalla ricetta che dai dati.

### P5. L'offerta di posti è incerta proprio dove decide
- **124 delle 172 fermate «coperte»** lo sono solo grazie a parcheggi di OpenStreetMap senza nome, con i posti
  stimati dalla superficie e uso sconosciuto (cortili di condomini, aziende, ospedali, supermercati senza tag).
- Solo **20 delle 172** hanno vicino almeno un parcheggio misurato.
- I 25 m² a posto: la mediana regge (24,4), ma metà dei parcheggi sta tra 14 e 33 m² (cioè ±40%, non ±30%).
- 26 fermate arrivano a 50 posti solo sommando parcheggi piccoli.

### P6. Il riempimento non pesa sul risultato
- Classi, aree e 20 punti usano **solo i posti nominali**: il fetch del 25/10 non li cambierà.
- I parcheggi misurati sono quasi tutti **garage del centro**: dei 9 «pieni di giorno», 8 sono garage di
  destinazione (Roma-San Carlo, Santo Stefano, Galileo Ferraris, Porta Nuova FS, D'Azeglio, Monti, Re Umberto,
  Ventimiglia). Solo Stura è un interscambio. Il grafico «parcheggi già pieni» dice quindi «il centro è pieno»,
  non «mancano interscambi».
- Le classi «di fatto / solo sulla carta / potenziale» (giri 1-2) **non sono più usate** nel risultato finale.

### P7. Nessun controllo con i fatti noti
I 5 interscambi ufficiali sono il banco di prova naturale, e il metodo non li riconosce:
- **Fermi** (pieno secondo Leo, capolinea della metro vicino a Corso Francia): area «Buona», nessun dato misurato vicino.
- **Caio Mario** (418 posti, quasi vuoto, accanto a una fermata con ~90 corse/ora nelle ore dei pendolari): a 207 m dal punto n. 10
  (Traiano) e a 1,1-1,9 km dai punti n. 1-2 (Pavese, Settembrini). Se un interscambio esistente è vuoto,
  costruirne un altro a 1 km è poco credibile senza capire **perché** è vuoto (prezzo? posizione? contatore?).
- **Sofia** è a 2 km dalla fermata importante più vicina: per il metodo quasi non esiste.

### P8. Parametri decisivi e risultati instabili
- Distanza: 100 m → 315 fermate scoperte, 200 m → 206, 400 m → 66. La pratica degli interscambi accetta di solito
  camminate di 300-400 m; 200 m in linea d'aria è severo.
- Posti: soglia 30 → 170, 50 → 206, 100 → 258. Fermate importanti: 5% → 177, 15% → 580.
- **Aree**: 14 delle 37 «critiche» si basano su 1-2 fermate; 18 aree hanno una fermata sola (quota 0% o 100% per
  forza).
- Il numero chiave «206 su 378» non ha un termine di paragone (altre città, un obiettivo, un minimo atteso).

### P9. I «parcheggi che potrebbero ampliarsi» non sono interscambi
Tra i candidati: garage del CTO e dell'ospedale, Porta Nuova FS (già pieno), Palagiustizia, il Lingotto (3.100
posti al 7%: il parcheggio della fiera). Sono parcheggi di destinazione, che lo stesso progetto ha classificato
«non interscambio / zona centrale».

### P10. Le direzioni d'ingresso hanno una domanda incoerente
La quota 26% = `f ÷ c2` (script 80, riga «quota = f / c2_totale»), ma:
- **f** = 24.459 spostamenti al giorno in cui si passa dall'auto (o dalla moto, codice 05) a un mezzo pubblico,
  **in tutta la giornata e su qualsiasi tragitto**, il 63% verso il treno;
- **c2** = 95.297 auto che **entrano a Torino al mattino**.
Sono due insiemi diversi: «95.297 × 26%» è di nuovo f, ridistribuito sulle direzioni. Le categorie «Bastano /
Mancano» confrontano poi questa domanda con posti di qualsiasi tipo. Bene averle tenute solo come riferimento.

### P11. Mancano i treni
Il 63% di chi oggi lascia l'auto per un mezzo pubblico prende il treno, ma il GTFS GTT non ha i treni: le
stazioni contano solo come «nodo» (e = 100), qualunque sia la frequenza (una stazione con un treno all'ora vale
come la metro).

### P12. Il modo in cui è nato
- 6 ridefinizioni in 5 giorni, 44 file di documentazione (~63% delle righe di `docs/`), 13 script (25, 68-69, 71-80).
- Regole adattate a casi singoli: il Palavela, fuori «per un soffio» a 200 m, è uno dei motivi per cui ora si
  mostrano i parcheggi fino a 400 m, e il codice controlla che ci sia.
- Numeri di oggi scritti nel codice come condizione per andare avanti (`79_dati_mappa_r6.py` si ferma se non
  trova esattamente 378 / 147 / 59 / 172 e 20 punti).

---

## 6. Ripensarlo da zero

### 6.1 La domanda
> **Ogni mattina entrano a Torino circa 95.000 auto. Quante si potrebbero fermare prima, in un parcheggio vicino
> a un mezzo veloce che le porta a destinazione senza perdere troppo tempo? Lungo quali strade d'ingresso, e dove
> i posti mancano o sono già pieni?**

Numero chiave: **auto che si potrebbero fermare** (e, se si vuole, km d'auto risparmiati), confrontate con i
**posti** degli interscambi di quel corridoio. È la metrica «auto in meno» che Leo voleva dal 16/10.

### 6.2 Le regole di buon senso degli interscambi
- **Al bordo**, prima del traffico e della città densa, non a 2 km dal centro.
- **Vicino a un mezzo veloce e frequente** (metro, treno, tram/bus con corsia propria), con un collegamento
  **diretto** verso le destinazioni di chi arriva da quel corridoio.
- **Il prezzo conta**: Caio Mario a pagamento è vuoto, i parcheggi gratuiti vicino a Fermi sono pieni (indizi del
  18/10). Conta anche il costo di parcheggiare a destinazione (zona blu, ZTL).
- Un interscambio in città rischia di togliere passeggeri ai bus (chi prima prendeva il bus sotto casa ora va in
  auto fino al parcheggio): va guardato.

### 6.3 Il metodo, in 6 passi (con pezzi che il progetto ha già)
1. **Domanda**: dai microdati IMQ 2022, le auto che entrano a Torino al mattino **con origine e destinazione**
   (non sommate per zona). Già calcolate nello script 73 (95.297, 1.139 interviste).
2. **Percorso**: assegnarle alla rete stradale OSM (`rete_osm.py` e il modello del traffico, R8) → per ogni auto,
   **da quale strada d'ingresso entra** (gli 80 assi d'ingresso dello script 77).
3. **Siti possibili**: gli interscambi ufficiali, i park & ride OSM, i parcheggi grandi e i nodi forti (capolinea
   della metro, stazioni SFM, capolinea di tram) **lungo ogni corridoio, fuori dalla zona densa**.
4. **Convenienza**: per ogni coppia origine-destinazione e ogni sito, tempo «tutta in auto» contro «auto fino al
   sito + trasporto pubblico» (R5, già usato per l'accessibilità). Regola semplice e dichiarata: l'interscambio
   conviene se fa perdere al massimo X minuti (es. 10), o se la destinazione è in ZTL o in zona blu. Si conta
   quante auto lo trovano conveniente per ogni sito.
5. **Offerta**: posti e riempimento misurati (5T) dove ci sono; gli altri parcheggi segnati come «non misurati».
6. **Validazione prima di tutto**: il modello deve dire che **Stura e Fermi** attirano molte auto e che **Caio Mario**
   ne attira poche (o spiegare perché è vuoto). Se non lo fa, si corregge il modello prima di mostrarlo.

### 6.4 Come si vedrebbe
- **Mappa**: le strade d'ingresso disegnate più o meno spesse secondo le auto che entrano; sugli interscambi un
  cerchio grande quanto i posti, colorato col riempimento misurato. Clic: «da qui entrano X auto al mattino; Y
  potrebbero lasciare l'auto a Fermi; Fermi ha 300 posti ed è pieno».
- **Scheda**: una tabella di 10-15 corridoi (auto in entrata, auto che potrebbero fermarsi, interscambio, posti,
  pieno sì/no) + i profili a 24 ore degli interscambi veri.

### 6.5 Dati da aggiungere
- **Treni SFM** (GTFS regionale Piemonte): senza, metà della storia manca.
- **Tariffe dei parcheggi** (i 30 gestiti da GTT, compresi i park & ride) e **zone blu** (già nel catalogo).
- **Più settimane di riempimento** (la raccolta continua) e, se possibile, il dato di Fermi (richiesta a GTT/5T).

### 6.6 Costo
È un lavoro di più passi (5-8 sessioni), ma riusa quasi tutto: microdati IMQ, rete stradale, R5, inventario dei
parcheggi, riempimento. Il pezzo nuovo è il passo 4.

## 7. Se non si vuole rifare tutto: correzioni mirate (dalla più utile)

1. **Una sola «zona centrale»** per fermate e parcheggi (Q001-Q009), oppure fermate importanti solo **sugli assi
   d'ingresso o ai nodi forti fuori dalla zona densa**. Effetto atteso: spariscono i punti nel semicentro.
2. **c2 solo dal lato della partenza** (cintura); togliere i doppioni (tenere a2 e c2, togliere a1 e c1); e come
   percentile o con un peso dichiarato.
3. **Offerta solo da parcheggi che possono fare da interscambio** (ufficiali, park & ride, pubblici ≥ 100 posti,
   esclusi ospedali, stazioni FS e garage del centro) e **distanza a piedi** sulla rete (300-400 m).
4. **Una riga di validazione in scheda**: come si comporta il metodo sui 5 interscambi ufficiali (oggi: Fermi non
   riconosciuto). È onesto e convincente.
5. **Aree solo con ≥ 5 fermate** (o togliere gli esagoni e tenere i punti).
6. **Candidati ad ampliarsi filtrati** come al punto 3.
7. **I controlli con i numeri di oggi diventano avvisi** (in 79 e 80), così il rilancio dopo il 25/10 e con il
   prossimo GTFS non si blocca.

E in ogni caso: **mettere in primo piano la scoperta sugli interscambi esistenti** (solo Stura funziona da
interscambio; Caio Mario vuoto; Sofia residenziale; Venchi Unica dato fermo), con i profili a 24 ore. Con ≥ 5
feriali diventa la parte più solida del risultato.

## 8. Cosa si può dire oggi, onestamente

- «Dei 4 interscambi del Comune, nei giorni misurati solo Stura è pieno di giorno; Caio Mario è quasi vuoto,
  Sofia è usato soprattutto di notte, Venchi Unica trasmette un valore fisso. Fermi non trasmette.» [MISURATO,
  DATI SCARSI]
- «I garage pieni di giorno sono quasi tutti in centro.» [MISURATO]
- «Molte fermate importanti non hanno un grande parcheggio vicino, soprattutto nei quartieri densi; questo da
  solo non dice dove servirebbe un interscambio.» [STIMATO]

## 9. Domande per Leo

1. **Quale delle due strade?** (a) correzioni mirate della sezione 7 (1-2 sessioni), (b) rifare con le auto in
   entrata e i corridoi (sezione 6, 5-8 sessioni), (c) fermarsi e mettere in primo piano solo la scoperta sugli
   interscambi esistenti.
2. **«Togliere auto» vuol dire anche i torinesi** che vanno in centro in auto da Mirafiori o Vallette? Se sì, è
   una seconda domanda (parcheggi di quartiere vicino alla metro/tram), da tenere separata.
3. **Fermi**: oltre a «sempre pieno», sai se si riempiono anche i parcheggi gratuiti intorno? A che ora? Mi serve
   solo come controllo a posteriori, come da tua regola.
4. **Caio Mario**: ti risulta davvero vuoto (o il contatore è fermo)? È il controllo più importante per un
   eventuale modello nuovo.
5. **Treni**: posso cercare il GTFS regionale del Piemonte (SFM) per aggiungere le stazioni con le frequenze?
