# Analisi dello stato del progetto (ottobre 2026)

Scritta da Claude dopo aver letto tutto il repository (memoria, README, mappa, schede, piani, script).
Le domande di Leo hanno una risposta qui; i lavori stanno nei piani:

| Piano | Cosa |
|---|---|
| `docs/piani/PIANO_DOCUMENTI.md` | pulizia di documenti e script, un documento per risultato |
| `docs/piani/PIANO_MAPPA.md` | mappa più semplice: temi, nomi, partenza vuota su satellite, peso |
| `docs/piani/PIANO_RISULTATI.md` | R1, R4 (confronto con GTT), R6, R8 e le analisi nuove (case, servizi, criticità) |
| `docs/piani/PIANO_SCHEDE.md` | schede dei risultati più corte, grafici giusti, niente rumore di sviluppo |

Decisioni di Leo (21/10, alle domande di Claude): il «R2» della domanda su GTT è il **Risultato 4**; di «Chi va dove»
resta **solo l'IMQ**; «Velocità e traffico» = **media per tipo di giorno** (feriale, sabato, domenica) su tutti i
giorni raccolti; i documenti superati si **cancellano** (restano nella storia di git).

---

## 1. Il quadro in una pagina

**Cosa funziona.** La raccolta su leopi è stabile; i dati sono tanti e buoni (GTFS, GPS dei mezzi, 5T, censimento,
IMQ, OMI, catalogo). I risultati hanno controlli, etichette ([MISURATO], [STIMATO]…) e limiti scritti. Il lavoro è
serio e onesto: molti numeri sono stati corretti quando i controlli hanno trovato errori (es. il R4 rifatto sul GPS).

**Cosa non funziona per un portfolio.**
1. **Troppo rumore di sviluppo.** 72 file in `docs/` più 75 in `docs/archivio/` (piani, esiti di ogni «giro»,
   rapporti di versioni superate); date, «giri», «Leo ha scelto» dentro pagine e testi; 19 `.bat`.
   Chi arriva non capisce da dove partire.
2. **La mappa fa troppe cose.** 10 temi, una scatola «Quando» con play e velocità (resto del vecchio simulatore),
   6 sovrapposizioni, 4 sfondi, griglia in metri, giornate registrate, catalogo grezzo. Pesa 13,6 MB (9,3 MB sono le
   sezioni di censimento).
3. **Due risultati dicono «va quasi tutto bene»** (R1: 362 persone; R8: 95,3% delle strade grandi coperte). Non è
   un errore: è il segnale che il **criterio è troppo largo** (basta *un* servizio, basta *una* fermata vicina). La
   letteratura dice la stessa cosa (sezione 3).
4. **Le schede sono lunghe.** Racconto, risposta, criteri, sensibilità, limiti, inglese: molto testo per numeri che
   si capirebbero con un grafico.

**Direzione proposta.** Meno temi e più chiari; ogni risultato = una domanda, un numero, una mappa, un grafico,
tre limiti. Per R1 e R8 cambiare la domanda (o il metro) invece di aggiungere dettagli.

---

## 2. Mappa (riassunto; dettagli in `PIANO_MAPPA.md`)

| Oggi | Proposta |
|---|---|
| Si apre sul tema «Servizio e abitanti», sfondo chiaro | Si apre **vuota su satellite**: solo il menu dei temi |
| 10 temi in una lista sola | 8 temi in 2 gruppi («Chi abita e cosa trova», «Come ci si muove»), nomi corti |
| Accessibilità: 4 servizi uno per volta | Aggiunta la voce **«Tutti i servizi»** |
| «Chi abita qui»: 3 voci (occupati, ragazzi, anziani) | Tema a sé con età, istruzione, lavoro, famiglie, densità + scheda della zona con un piccolo profilo |
| Due «Chi va dove» | Uno solo: **«Spostamenti»** (IMQ); pendolari ISTAT tolti |
| «Bus e traffico misurati» con giornata singola | **Media per feriale/sabato/domenica**, giornate singole tolte |
| Scatola «Quando» sempre visibile, con play e velocità | Solo giorno e ora, e solo nei temi che cambiano con l'ora |
| Corse simulate in movimento, avvisi GTT del 9/10, griglia, sfondo stradale | Tolti |
| Catalogo grezzo (40 tabelle) | «Luoghi della città»: pochi gruppi utili, senza metadati tecnici |

---

## 3. Risposte alle domande sui dati

### 3.1 Valore immobiliare incrociato con vulnerabilità e servizi: sì, ha senso

Tre domande che si possono fare con i dati che abbiamo (OMI per zona, sezioni per indice e servizi):
1. **Dove si paga per i servizi?** Prezzo delle case contro servizi raggiungibili (a piedi e coi mezzi). Ci si
   aspetta: più servizi, prezzo più alto. Le zone **fuori dalla regola** sono le interessanti: molti servizi e prezzo
   basso (zone «convenienti», spesso con un problema non misurato: rumore, degrado, percezione); pochi servizi e
   prezzo alto (collina: si paga il verde e la quiete, non i servizi).
2. **Doppio svantaggio**: zone con indice di vulnerabilità alto **e** pochi servizi. Il prezzo basso spiega perché
   chi è fragile abita lì. È la mappa più «politica» e più utile del progetto.
3. **Il valore della metro**: prezzo entro 600 m da una fermata della M1 contro zone simili lontane. Tema molto
   attuale (linea 2 in progetto). Limite: OMI ha un solo semestre e zone grandi: si parla di **differenze fra
   zone**, non di effetto causale.

Lavoro: medio, uno script nuovo (prossimo numero libero 92). Unità = **zona OMI** (le sezioni si aggregano nella
zona, pesate per abitanti). Facoltativo e utile: scaricare 4-6 semestri OMI passati per vedere dove i prezzi
**salgono** (rischio di espulsione dei residenti fragili). Piano in `PIANO_RISULTATI.md`, parte E.

### 3.2 Quanta gente frequenta i servizi del catalogo: no, non c'è

Il catalogo comunale non ha frequentatori. Ha solo qualche **capienza**: posti dei nidi, sale dei cinema, posti
auto, stalli disabili. Per scuole e ospedali niente.
Fonti esterne aperte che li hanno:
- **Scuole**: il Ministero dell'Istruzione pubblica gli **alunni per scuola** (Portale Unico dei Dati della Scuola,
  codice meccanografico). Lavoro medio: abbinare i codici alle sedi del catalogo (per indirizzo o coordinate).
- **Ospedali**: il Ministero della Salute pubblica i **posti letto per struttura**. Lavoro piccolo-medio.
- Negozi, sport, verde: niente di affidabile.

Vale la pena **solo per scuole e salute**, perché serve a una cosa precisa: pesare i servizi del R1 per la loro
capienza (un ospedale grande e un ambulatorio oggi contano uguale), e fare un calcolo «posti per abitante» (vedi 3.3).
Per gli altri calcoli non serve. Da fare dopo il nuovo R1, non prima.

### 3.3 «Dove mancano i servizi»: 5 punti in collina. Serve un metodo diverso

Il metodo di oggi chiede «c'è **almeno un** servizio a 15 minuti?». A Torino la risposta è quasi sempre sì: la
città è densa. Per questo escono solo 5 sezioni in collina. Non è un metodo sbagliato: è un metodo che **non
distingue** fra chi ha 1 farmacia e chi ne ha 20.

Proposta: tre misure, in ordine di costo, tutte già note in letteratura.
1. **Soglie più strette (10 e 5 minuti)**. È esattamente lo studio di Staricco (Politecnico di Torino, 2022,
   «15-, 10- or 5-minute city? A focus on accessibility to services in Turin», *Journal of Urban Mobility*; titolo da
   ricontrollare): a 15 minuti Torino è quasi tutta coperta, a 10 e 5 minuti emergono le differenze fra quartieri.
   Possiamo confrontarci con un lavoro pubblicato sulla stessa città: ottimo per il portfolio. Costo: rifare il
   calcolo a piedi dello script 18 con 5 e 10 minuti (solo a piedi, poche ore).
2. **Quanti servizi per abitante, non «almeno uno»** (metodo dei bacini a due passi, «2SFCA»: per ogni servizio si
   contano gli abitanti che lo raggiungono; poi per ogni casa si sommano i servizi raggiungibili divisi per la loro
   «folla»). Fa emergere le zone dense dove il servizio c'è ma è **conteso**: periferie popolose, non la collina.
   Per scuole e salute meglio con la capienza (3.2), ma si può partire con «1 servizio = 1».
3. **Cintura**: invece di contare i comuni come città dei 15 minuti, chiedere «quanto tempo coi mezzi pubblici per
   il servizio più vicino» (già calcolato alle 8). Lì emergono i punti critici veri fuori Torino. Limite: servizi
   OSM incompleti fuori Torino, da dichiarare.

Il risultato diventa: «dove i servizi ci sono ma sono pochi per la gente che ci abita» (città) + «dove servono più
di X minuti di bus» (cintura). Punti critici veri, in posti abitati.

### 3.4 R1: 362 abitanti. Diciamo «Torino è ottima» o critichiamo il criterio?

Tutte e due, in quest'ordine. È la scelta più forte e più onesta.
1. **Il risultato è vero e va detto chiaro**: con il criterio classico (Moreno, «città dei 15 minuti») Torino è
   quasi tutta coperta. Il titolo: «A Torino quasi tutti hanno i servizi essenziali a 15 minuti a piedi».
2. **Poi la critica, con la letteratura**: la città dei 15 minuti misura la **vicinanza**, non la **qualità di
   vita**. Le critiche note: (a) «almeno uno» non dice se basta (capienza, affollamento → 3.3 punto 2); (b) la soglia
   di 15 minuti è larga per anziani e bambini (velocità a piedi più bassa → 3.3 punto 1); (c) la vicinanza non dice
   nulla dell'**ambiente**: traffico, rumore, aria, caldo, verde fruibile.
3. **Un indicatore di qualità di vita che possiamo calcolare davvero**: **residenti esposti al traffico** = abitanti
   delle sezioni a meno di 100 m da una tratta con molto traffico (dal modello del R8, che è debole ma va bene per
   le classi alto/medio/basso). Traffico è il miglior sostituto che abbiamo di rumore e smog: i dati ARPA aperti
   sono solo medie annuali per centralina, troppo pochi punti per una mappa. Si aggiunge al R1 come seconda parte:
   «I servizi ci sono; ma 1 torinese su N vive su una strada molto trafficata».
   Facoltativo: **pendenza** (la collina è vicina in linea d'aria ma in salita) dal modello del terreno: lavoro
   medio, utile soprattutto per anziani.

Così il R1 passa da «362 persone» a tre numeri che dicono qualcosa di vero: copertura a 15', differenze a 10'/5' e
servizi contesi, esposizione al traffico.

### 3.5 R4: perché il nostro numero è diverso da quello di GTT

GTT (rapporto di sostenibilità 2025, p. 128) dichiara **2,3%** di passaggi bus e tram **in ritardo oltre 10 minuti**
(2,6% nel 2024, 2,5% nel 2023). Noi misuriamo col GPS **5,4%** (feriali di ottobre; 14,1% oltre 5 minuti).
Risposta da saper dare in 30 secondi:

> «Non sono la stessa misura. GTT fa la media dell'**anno intero**, estate e sere comprese, su **tutte le linee**, con
> un metodo che non pubblica. Noi misuriamo **solo ottobre** (scuole aperte, pioggia, cantieri), **solo le ~90 linee
> urbane**, dalle 5 a mezzanotte, a **ogni fermata** della corsa, con la posizione GPS dei mezzi. Il ritardo cresce
> lungo la corsa: chi lo misura alla partenza o a metà corsa trova numeri più bassi. Tutti e due dicono la stessa
> cosa: i ritardi gravi sono una piccola parte dei passaggi, fra il 2 e il 6%.»

Cosa possiamo fare per renderla solida (piano in `PIANO_RISULTATI.md`, parte B):
- **Tabella delle definizioni**: il nostro numero calcolato in 4 modi (a ogni fermata; solo alla partenza; solo a
  metà corsa; ore di punta escluse). Se «alla partenza» viene vicino al 2%, la differenza è spiegata con i fatti.
- **Stagione**: dire che ottobre non è un mese medio; rifare il numero a gennaio e in estate (la raccolta continua)
  per avere un confronto sull'anno.
- **Nostri errori possibili**, dichiarati: il passaggio alla fermata è stimato fra due posizioni GPS (circa 1
  minuto di incertezza); il 22% delle corse non ha GPS (se mancano quelle peggiori o le migliori il numero si sposta).
- In scheda: una riga e un piccolo grafico «noi contro GTT» con le barre delle 4 definizioni.

### 3.6 R6: obiettivo, metodo, risultati. Siamo soddisfatti?

**In parte.** L'obiettivo è chiaro e utile (dove servono parcheggi di scambio per togliere auto dal centro).
Il metodo è ragionato e ogni passo è controllato. Ma:
1. **Catena di stime troppo lunga**: auto in entrata (IMQ) × quota di chi lascia l'auto (**64 interviste**) × auto
   che passano (modello del traffico, ρ 0,52 contro i sensori) × regola delle fermate (N, M scelti) × parcheggi adatti.
   Ogni anello è debole; il «posti che mancano» è un ordine di grandezza, e lo diciamo.
2. **Contraddizione non spiegata**: gli interscambi che esistono sono **poco pieni** (Sofia 32% di giorno, Venchi
   Unica 52%, Caio Mario fermo). Se quelli esistenti non si riempiono, «mancano posti» è la risposta giusta? La
   letteratura sul park-and-ride dice che funziona solo se il mezzo pubblico dal parcheggio è **più veloce o più
   comodo dell'auto** e se parcheggiare in centro **costa**. Non lo misuriamo.
3. **Troppi criteri in pagina** (fermate importanti, parcheggi adatti, assi, 3 km, 50 posti…): difficile da
   spiegare in un minuto.

Proposta (piano in `PIANO_RISULTATI.md`, parte C): (a) presentare i 12 punti come **classifica di assi in 3 classi**
(alto, medio, basso), non con i posti; (b) aggiungere il test che manca: **tempo coi mezzi dal parcheggio al
centro contro tempo in auto** (si appoggia al lavoro «tempi TP contro auto» già nei prossimi passi); un punto entra
solo se il mezzo pubblico è competitivo; (c) spiegare in scheda perché gli interscambi esistenti sono vuoti (stesso
test applicato a loro); (d) rilancio a inizio novembre con più giorni di parcheggi, come previsto.

### 3.7 R8: obiettivo, metodo, risultati. Siamo soddisfatti?

**Del metodo sì, della domanda no.** Il modello del traffico è debole (errore ±38%, ρ 0,6, 20 sensori) ma usato
nel modo giusto (classifica, non conteggi). La domanda «dove c'è molto traffico e nessuna fermata vicina» però ha
quasi sempre risposta «da nessuna parte» (95,3%; in pratica solo Corso Regina Margherita ovest): stesso problema
del R1, il criterio «una fermata a 300 m» è troppo largo. Una fermata vicina non vuol dire che il bus sia
un'alternativa all'auto.

Proposta (piano in `PIANO_RISULTATI.md`, parte D): cambiare la domanda in **«dove il mezzo pubblico non conviene
rispetto all'auto»**: per coppie di zone IMQ, tempo coi mezzi (motore dello script 18, alle 8) diviso tempo in auto
(rete del modello del traffico); pesato per le auto che fanno quel viaggio. È la misura classica di
«competitività» del trasporto pubblico. Risultato atteso: un elenco di relazioni (es. cintura ovest → zona
industriale nord) dove il TP impiega più del doppio. Unisce R8 e il passo «tempi TP contro auto»; serve anche al
R6 (punto b). Il 95,3% resta come riga («quasi tutte le strade grandi hanno una fermata vicina»).

---

## 4. Rischi e cose aperte

- **Sfondi Esri**: condizioni d'uso da verificare prima di pubblicare (già noto). Alternativa sicura: sfondo OSM o
  CARTO con attribuzione; per il satellite, Esri World Imagery chiede attribuzione e uso non commerciale ragionevole.
- **Storico**: 2,1 GB, +190 MB al giorno; servirà una copia solo dei dati nuovi.
- **R2 in pausa**: resta fuori dalla presentazione finché non si rifà con la domanda giusta.
- **R3/R5** (scenario di linea): mai fatti; per il portfolio bastano R1, R4, R6, R8 fatti bene.
- **Repository pubblico**: niente dati personali; il nome «Leo» nei documenti di lavoro va tolto da ciò che si
  pubblica (README, pagine).

---

## 5. Revisione finale (dopo pulizia dei documenti, mappa giri 1-2 e confronto R4 con GTT)

Controllato da Claude su `prova`: esiti letti, mappa aperta in Chromium su tutti gli 11 temi (computer e telefono),
codice e testi cercati. **Nessun errore JavaScript.** I tre giri sono fatti bene e i numeri tornano (es. «Tutti i
servizi»: Piazza Castello 92, Mirafiori Sud 46, Venaria 38; confronto con GTT: 3,9% alla partenza, 5,5% a ogni fermata,
forbice 4,3-5,7% per le corse senza GPS: la differenza con il 2,3% di GTT **non** si spiega solo con la definizione, e va
detto così).

### 5.1 Da correggere subito (problemi veri)

| # | Problema | Perché conta | Lavoro |
|---|---|---|---|
| 1 | **Dato personale nel repository pubblico**: il nome della cartella OMI scaricata contiene un codice personale (in `docs/FONTI_DATI.md` e `scripts/08_prepara_omi.py`); l'email personale è nell'intestazione delle richieste di 3 script (01, 03, 12) | il repository è pubblico | piccolo: rinominare la cartella sul PC (es. `data/raw/omi_2025_2/`), percorso nel 08, togliere la riga dai documenti; email → una casella dedicata al progetto o niente contatto. **Il codice resta nella storia di git**: per toglierlo davvero serve riscrivere la storia (decisione di Leo) |
| 2 | **README vecchio** (10.919 residenti, 5,2%, 253 fermate, «Leo, 2026»): è la prima cosa che si vede su GitHub | numeri sbagliati in vetrina | piccolo: rigenerarlo (script 86) dopo le schede; nel frattempo togliere i numeri |
| 3 | **Pubblicazione rotta per «Luoghi della città»**: la mappa carica `data/catalogo/<gruppo>.js`, ma lo script 86 non copia quei file in `pubblica/` | il tema sarebbe vuoto online | piccolo: aggiungerli a `FILE_FISSI` nel 86 e provare con `prova_pagine_r6.py --cartella pubblica` |
| 4 | **«Tutti i servizi» mescola due fonti**: il percentile è calcolato su tutta l'area, ma fuori Torino scuole, salute e negozi vengono da OpenStreetMap (più povero): la cintura viene tutta rossa anche per mancanza di dati | messaggio falsato | piccolo: percentili **separati** Torino / cintura (o cintura in grigio per i gruppi OSM), detto in legenda |
| 5 | **Le zone grandi e vuote dominano la vista**: colline, campi e parchi sono sezioni enormi con pochi abitanti; nei temi delle sezioni l'occhio vede la superficie, non le persone | mappa che inganna | piccolo-medio: come nei «Servizi mancanti», grigio chiaro per le sezioni sotto 1.000 ab/km² in **tutti** i temi delle sezioni (o opacità proporzionale agli abitanti) |
| 6 | **Periodi diversi fra temi e schede**: bus 4-21/10 (13 feriali), sensori 9-18/10 (6), R4 10-20/10 (6), parcheggi 3 giorni | confuso e difficile da difendere | piccolo: per la versione da presentare, **un periodo unico congelato** (es. 4 settimane), tutti gli script rilanciati sulla stessa finestra, scritto una volta in testa alle pagine |

### 5.2 Da migliorare (mappa)

- **Ancora da fare dal piano**: «Chi abita qui» completo con il profilo della zona (sezione 3), «Luoghi della città»
  ridotto a 6 caselle (oggi è ancora il catalogo grezzo con i nomi tecnici, es. «Reti e accessibilita'»), peso (13,1 MB,
  sezione 7), schede uniformi (sezione 8).
- **Testi di legenda troppo lunghi** in quasi tutti i temi (R6: 9 righe di testo; «Velocità e traffico»: date al minuto,
  «GPS dal 4 ott, 01:43»). Regola: titolo, colori con numeri, **una** riga di fonte; il resto nella guida.
- **Parcheggi di scambio**: i parcheggi del centro (viola, pieni) sono la cosa più visibile, ma non sono l'oggetto del
  tema. Viola chiaro e più piccoli, o accesi solo da «Altre opzioni».
- **Prezzo delle case**: togliere box e magazzini (piano, sezione 1); le classi 1.125-1.675 €/m² sono strette: con 5
  classi a quantili va bene, ma scrivere in legenda anche minimo e massimo.
- **«Spostamenti»**: c'è ancora «Residenti 11-84 anni» (va in «Chi abita qui»).
- **Telefono**: il pannello occupa metà dello schermo e resta aperto all'avvio; partire chiuso con un bottone «Temi».
- **Nome della pagina dei risultati** (fatto 21/10): era `simulazione.html`, ora `risultati.html`
  (il vecchio nome porta alla nuova pagina); aggiunta la **pagina d'ingresso** `index.html` (titolo, 3 righe, due bottoni:
  Mappa, Risultati): serve anche per GitHub Pages.
- **Sfondo**: condizioni d'uso di Esri ancora da controllare; con il satellite come partenza è più importante di prima.

### 5.3 Da migliorare (risultati e schede)

- **Le schede non sono ancora state toccate** (`PIANO_SCHEDE.md`): oggi sono il punto più debole della presentazione. È il
  lavoro con più resa.
- **R4**: aggiungere alla scheda la frase onesta che esce dal confronto: «anche contando come GTT alla partenza, noi
  troviamo 3,9%; il resto della differenza è stagione e metodo». La stagione (B3) si chiude solo a gennaio.
- **R1, R6, R8**: i lavori grossi del piano (A, C, D) sono ancora da fare; R6 aspetta i parcheggi di inizio novembre.
- **R2 e R3/R5**: per il portfolio meglio non mostrarli finché non sono rifatti. Va bene presentare **4 risultati**.

### 5.4 Da togliere

- ~~Script e `.bat` superati~~: fatto (passi 8-9 di `PIANO_DOCUMENTI.md`).
- `docs/piani/ESITO_*.md` dopo ogni ricontrollo (la regola c'è già nella memoria).
- ~~La memoria è cresciuta~~: riscritta in meno di 120 righe (passo 12).
- `mappa_torino.html` dal ramo principale quando si pubblica (13 MB a ogni giro nella storia di git).

### 5.5 Da aggiungere (idee che valgono il lavoro)

1. **Pagina d'ingresso** con i 4 risultati in una riga ciascuno (vedi 5.2): la prima impressione del portfolio.
2. **Una mappa statica per scheda** (immagine del tema giusto, già prodotta da `prova_pagine_r6.py`): chi legge la
   scheda capisce senza aprire la mappa.
3. **«Doppio svantaggio»** (fragilità alta e pochi servizi, parte E del piano): è la mappa più significativa che si
   può fare con i dati già pronti, e lega tre temi che oggi sono separati.
4. **Sezione «Come è fatto»** breve nel README (raccolta su Raspberry Pi ogni minuto, 20 giorni di GPS, motore R5): per
   un portfolio la parte tecnica è un pregio, oggi è nascosta nei documenti.

### 5.6 Ordine consigliato da qui

1. Correzioni 5.1 (1-4): un giro piccolo, subito.
2. Mappa giro 3 («Chi abita qui», zone vuote in grigio, legende corte, parcheggi del centro, telefono).
3. Schede (`PIANO_SCHEDE.md`) per R4 e R6, poi pagina d'ingresso e README.
4. R1 nuovo (parte A), R8 nuovo (parte D), poi R6 con i dati di novembre (parte C).
5. Periodo congelato, mappa giro 4 (peso, luoghi), pulizia di script e `.bat`, pubblicazione.
