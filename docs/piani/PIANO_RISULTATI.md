# Piano — revisione dei risultati e analisi nuove

Le ragioni sono in `docs/ANALISI_STATO.md` (sezione 3). Qui solo i lavori. Prossimo numero libero di script: **92**.
Regole di sempre: dati in sola lettura, prova su un campione, controlli negli script, numeri mai scritti a mano nei
testi, Claude ricontrolla prima di dare i numeri a Leo.

Ordine proposto: **B** (R4, piccolo, chiude una domanda aperta) → **A** (R1) → **D** (R8, che serve anche al R6) →
**C** (R6, dopo i parcheggi di novembre) → **E** (case) → **F** (capienze, solo se A lo chiede).

---

## A. R1 — dalla «città dei 15 minuti» alla qualità della vicinanza

Domanda nuova: **«I torinesi hanno i servizi vicino a casa? E sono abbastanza per chi ci abita?»**
Tre parti, un numero ciascuna:

| Parte | Misura | Come | Quanto |
|---|---|---|---|
| A1 Copertura | residenti con tutti e 5 i servizi a 15 / 10 / 5 minuti a piedi | script 18 solo a piedi con soglie 5 e 10 minuti (opzione `--soglie-piedi 5,10,15`), poi 21 | medio (calcolo di qualche ora sul PC) |
| A2 Servizi contesi | per scuole, salute, negozi: servizi raggiungibili **per 1.000 abitanti che li condividono** (bacini a due passi, 2SFCA, a piedi 15') | script nuovo 92 sui tempi a piedi già calcolati; classi in 5 quintili; titolo = residenti nel quintile più basso in zone abitate | medio |
| A3 Esposizione al traffico | residenti in sezioni a meno di 100 m da una tratta «molto trafficata» del R8 (≥ 11.720 veicoli/giorno) | script 92 (o 93) con le tratte di `66_pubblicazione_incrocio`; classi alto/medio/basso, dichiarato «stima debole» | piccolo |
| A4 Cintura | tempo coi mezzi al servizio più vicino (alle 8) | dai dati dello script 18; tabella separata | piccolo |

Passi:
1. Leggere lo studio di Staricco (2022) su Torino e annotare metodo e numeri per il confronto (soglie, servizi,
   risultati per quartiere). Se i numeri sono simili ai nostri a 15': ottima verifica su un fatto noto.
2. A1 e A3 (danno subito il messaggio: «a 15' quasi tutti, a 5' no; e 1 su N vive su una strada trafficata»).
3. A2 (con «1 servizio = 1»; se i risultati sono dominati da ospedali grandi o scuole piccole → parte F).
4. Scheda R1 rifatta (vedi `PIANO_SCHEDE.md`); tema «Servizi mancanti» in mappa: vista predefinita = A2 (quintili),
   poi copertura a 5/10/15', poi esposizione al traffico.
5. I 5 punti in collina restano come riga («dove manca davvero tutto: 362 persone, in collina»).

Limiti da scrivere: capienza non nota (finché manca F), pendenza non considerata, traffico come sostituto di rumore e
smog (dati ARPA solo medie annuali per centralina).

---

## B. R4 — saper spiegare la differenza con GTT

Il numero di GTT: 2,3% dei passaggi bus/tram oltre 10 minuti (anno 2025). Il nostro: ~5,4% (feriali di ottobre, GPS).

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| B1 | **Tabella delle definizioni** «oltre 10 minuti» calcolata in 4 modi: (a) a ogni fermata, come oggi; (b) solo alla prima fermata (partenza); (c) a metà corsa; (d) tutto il giorno contro solo fuori dalle ore di punta. Più: per tipo di giorno (feriale, sabato, domenica) e media pesata su una settimana intera | script 27, nuova sezione del rapporto e del JSON | piccolo |
| B2 | **Incertezza nostra**: (i) passaggio stimato fra due posizioni GPS: rifare il conto spostando tutti i passaggi di ±1 minuto; (ii) corse senza GPS: il numero se le corse mancanti fossero tutte puntuali / tutte in ritardo (forbice) | 27 | piccolo |
| B3 | **Stagione**: nota fissa nella scheda; ripetere il calcolo a gennaio e a luglio (la raccolta continua) e mostrare i mesi affiancati | — | nel tempo |
| B4 | Scheda: un grafico «noi e GTT» (barre: GTT 2,3%; noi in 4 definizioni) e la risposta di 3 righe (testo in `ANALISI_STATO.md`, 3.5) | `schede_risultati.py` | piccolo |

Atteso: (b) «alla partenza» molto più basso di (a); se viene vicino al 2-3%, la differenza è spiegata con i dati.

---

## C. R6 — più semplice e con il test che manca

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| C1 | **Tempo dal parcheggio al centro**: per ogni punto prioritario e ogni interscambio esistente, tempo coi mezzi fino a Piazza Castello (motore dello script 18, alle 8) contro tempo in auto (rete del modello del traffico, tempi in ora di punta corretti con il fattore misurato in Fase 5) | script nuovo dopo D1 (riusa lo stesso calcolo) | medio |
| C2 | Un punto resta prioritario solo se il mezzo pubblico non è molto peggio dell'auto (tempo TP ≤ 1,5 × auto, valore da discutere con Leo) | 84 | piccolo |
| C3 | **Interscambi esistenti poco usati**: stesso test; se il TP da lì non conviene, è la spiegazione; scriverla nella scheda | 84, scheda | piccolo |
| C4 | Presentazione: i punti come **classifica di assi in 3 classi** (bisogno alto/medio/basso), niente «circa 650 posti» in grande (resta nel pannello come ordine di grandezza) | scheda, template | piccolo |
| C5 | Rilancio con i parcheggi fino a inizio novembre (`RISULTATO6_RIFAI.bat`), già previsto | — | — |

Criteri in scheda: da 7 righe a 4 (auto che entrano; fermate servite bene; parcheggi adatti; mezzo pubblico
competitivo), gli altri nel documento del metodo.

---

## D. R8 — dove il mezzo pubblico non conviene

Domanda nuova: **«Per quali spostamenti l'auto è molto più veloce dei mezzi pubblici, e quante auto li fanno?»**

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| D1 | Tempi coi mezzi fra centri delle zone IMQ (101 × 101, alle 8 di un feriale, motore R5 dello script 18 con origini e destinazioni = centri delle zone pesati sugli abitanti) | script nuovo | medio-grande (calcolo lungo sul PC: prova prima su 10 zone) |
| D2 | Tempi in auto sulla stessa coppia (rete OSM del modello del traffico, velocità del modello con il fattore di congestione misurato); controllo con 10 percorsi noti | stesso script | medio |
| D3 | Rapporto TP/auto per coppia; pesato per le auto IMQ della coppia (06-10). Titolo: «X auto al mattino fanno viaggi dove il bus impiega più del doppio» | stesso script | piccolo |
| D4 | Mappa: tema «Spostamenti», vista nuova «Dove i mezzi non convengono» (clic su una zona = le destinazioni colorate per rapporto TP/auto) | 04, template | medio |
| D5 | La copertura delle strade grandi (95,3%) resta come seconda riga della scheda; il resto del R8 di oggi nel documento del metodo | scheda | piccolo |

Limiti: tempi programmati per il TP (ottimisti), tempi auto senza ricerca del parcheggio (ottimisti anche loro: si
compensano in parte; dirlo), IMQ campionaria.

---

## E. Prezzo delle case × fragilità × servizi (analisi nuova)

Unità: **zona OMI** di Torino (le sezioni si sommano nella zona, pesate per abitanti). Script nuovo (92 o successivo).

| # | Domanda | Misura | Grafico |
|---|---|---|---|
| E1 | Si paga per i servizi? | prezzo medio abitazioni (€/m², centro della forbice OMI) contro punteggio «Tutti i servizi» (mappa, sezione 5) | dispersione, una bolla per zona, dimensione = abitanti; correlazione di Spearman; le zone lontane dalla tendenza con il nome |
| E2 | Doppio svantaggio | zone con fragilità nel 20% più alto **e** servizi nel 20% più basso (A2) | mappa a 4 colori (2 × 2) |
| E3 | Il valore della metro | prezzo nelle zone con una fermata M1 entro 600 m contro le altre, a pari distanza dal centro (fasce di 2 km) | barre affiancate per fascia |
| E4 (facoltativo) | Dove salgono i prezzi | 4-6 semestri OMI scaricati a mano da Leo; variazione % per zona contro fragilità | mappa della variazione |

Avvertenze in scheda: OMI = quotazioni (non compravendite), zone grandi, un semestre; correlazione, non causa.
Esce come **Risultato nuovo** («Case, servizi e fragilità») solo se E1-E2 dicono qualcosa di chiaro; altrimenti
resta una vista della mappa.

---

## F. Capienza dei servizi (solo se serve ad A2)

| # | Fonte | Uso | Quanto |
|---|---|---|---|
| F1 | Ministero dell'Istruzione, Portale Unico dei Dati della Scuola: alunni per scuola (codice meccanografico) | peso delle scuole nel 2SFCA | medio (abbinamento per indirizzo/coordinate) |
| F2 | Ministero della Salute: posti letto per struttura | peso degli ospedali | piccolo-medio |
| — | Negozi, sport, verde | niente fonte affidabile | — |

Leo scarica i file (sono aperti); lo script li abbina e scrive quante sedi non trovano corrispondenza (AVVISO oltre il
10%).
