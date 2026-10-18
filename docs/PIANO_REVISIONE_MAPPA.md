# Revisione della mappa (`mappa_torino.html`) — 18/10/2026

Revisione fatta da Claude su richiesta di Leo. **Nessuna modifica fatta**: qui ci sono solo i problemi trovati
e le correzioni proposte. Si corregge un punto alla volta, dopo l'ok di Leo.

Scelte di Leo per questa revisione: pubblico = **chi vede il portfolio** (testi brevi, niente sigle, dettagli
a richiesta); si possono proporre temi da togliere o accorpare; i Risultati (R4, R6, R9) restano fuori dalla
mappa per ora.

Come è stata controllata: lettura di `scripts/04_genera_mappa.py` e `scripts/mappa_template.html`; mappa aperta
nel browser integrato (server locale `pagine-gtt`, porta 8765) provando tutti i 10 temi e tutte le opzioni,
anche a misura di telefono; numeri ricalcolati dai dati incorporati nella mappa e dallo storico (sola lettura)
con uno script a parte.

Stato del file: mappa generata il **15/10 16:36**; il modello è stato ritoccato il 18/10 (3 frasi della guida),
quindi la mappa non è allineata al modello. Orari GTT versione 20261002 (validi fino al 31/01/2027).

---

## Gravità ALTA — la mappa mostra una cosa sbagliata

**A1. "Criticità" non funziona e ha i colori al contrario.** (Servizio e abitanti → Criticità)
- La legenda dice "Dati ISTAT non disponibili", ma i dati ci sono. Causa: le soglie della criticità si calcolano
  *prima* che esistano le soglie dell'offerta per abitante, da cui dipendono, quindi restano vuote.
- Senza soglie, quasi tutte le sezioni escono verdi; in **rosso** finiscono le sezioni con *più* offerta (indice 0),
  per esempio zone industriali con pochi abitanti vicino a linee forti. Cioè il rosso dice il contrario del vero.
- Anche con le soglie giuste la tavolozza è rovesciata: indice alto = più critico, ma la classe alta è verde.
- In più l'indice è solo l'"offerta per abitante" rimessa su una scala da 0 a 100: è un **doppione**.
- **Proposta:** togliere la voce "Criticità" (e la riga "Indice di criticità" da schede e pendolari). In alternativa:
  correggere ordine di calcolo e tavolozza.

**A2. "Dove mancano i servizi" e "Accessibilità" mescolano Torino e cintura.**
- In cintura i servizi vengono da OSM (molto più poveri del catalogo comunale). Esempio, scuole a piedi in 15':
  valore tipico **29 a Torino, 3 in cintura**; cibo: 1.212 contro 8.
- Le soglie dei colori sono calcolate su tutta l'area insieme, quindi la cintura esce quasi tutta rossa o gialla.
  In "Dove mancano i servizi" le sezioni segnalate per almeno un gruppo sono 4.950: **4.238 (86%) sono in cintura**,
  cioè il 99% delle sezioni della cintura (4.238 su 4.273). A colpo d'occhio la mappa dice
  "manca tutto fuori Torino", che è soprattutto mancanza di dati. L'avviso c'è, ma solo in una frase della legenda.
- Il Risultato 1 ufficiale (10.919 residenti senza servizi) è **solo Torino**: la mappa non lo rispecchia.
- **Proposta:** per scuole, salute e cibo colorare **solo Torino** e mostrare la cintura in grigio "dato non
  confrontabile"; soglie calcolate solo su Torino. Per fermate e verde (stessa fonte ovunque) si può tenere tutto.

**A3. "Quota pubblico" (IMQ) è tutta dello stesso colore.**
- Le classi sono fisse a 20/40/60/80%, ma la quota del pubblico va da 0 a 21%: tutte le 101 zone cadono nella
  prima classe (azzurro chiarissimo). Il tema dichiara una cosa che non si vede.
- **Proposta:** classi adatte ai valori (es. 0-5-10-15-20%) con i numeri scritti in legenda; per "quota privato"
  lo stesso controllo.

**A4. "Adesso" e "tempo reale" non sono veri, e per chi guarda il portfolio non lo saranno mai.**
- La copia dei dati dal Raspberry è settimanale: i "mezzi adesso" e i "sensori degli ultimi 5 minuti" sono dati
  vecchi di giorni. Oggi (18/10) i mezzi sono **1** (feed GTT fermo dalle 09:05).
- Chi apre la mappa da fuori non ha la raccolta: "Segnalazioni adesso", "più lento del solito" e il pallino verde
  "dati live" non hanno senso per lui.
- Senza la cartella `data/` accanto (live.js, stat.js, replay, catalogo, orari) quelle parti spariscono in silenzio.
- **Proposta:** togliere la parola "adesso" e il tema "Tempo reale e flotta"; tenere il **Replay** come "Una giornata
  registrata" (mezzi veri che si muovono, con la data scritta). Sensori 5T: mostrare il **traffico tipico per ora**
  (già calcolato) invece dell'ultima lettura.

---

## Gravità MEDIA — si capisce male o si legge male

**M1. Velocità commerciale: dicitura impossibile e testo superato.**
- La legenda dice "Storico usato: **26.996,5 ore** (4 ott → **1 nov 2029**)". Causa nei dati: un mezzo (2897U, linea
  16CDU) ha l'orologio avanti di ~3 anni: **2.100 righe** su 3,1 milioni. Effetto sui numeri trascurabile (0,07%,
  e la data sbagliata può spostarle di giorno), ma l'etichetta è assurda.
- "Non c'è il codice della corsa: nessun ritardo" (legenda, scheda linea, scheda mezzo) non è più vero: dal 10/10
  i ritardi ci sono (Risultato 4).
- **Proposta:** nello script 04 scartare le letture con `ts_feed` lontano da `letto_utc`; frase nuova e corta.

**M2. Testi superati sull'accessibilità con i mezzi pubblici.** La scheda della sezione dice ancora "una delle
4 fasce orarie (08/14/23/02) … entro 1 ora"; la legenda dice "fascia 15:00, calcolata sulla fascia 15:00 (entro 1
ora)". Dal 15/10 le fasce sono 24. **Proposta:** "nell'ora scelta (orario programmato)".

**M3. Vulnerabilità: legenda e descrizione non corrispondono.**
- Legenda "0 … 100" senza classi; le componenti sono percentili 0-1, colorate per quintili.
- La descrizione dice "+ accessibilità a servizi e verde", ma quelle componenti sono state tolte.
- Etichetta "STIMATO/SIMULATO": è un calcolo sul censimento, non una simulazione.
- **Proposta:** "Più vulnerabile ↔ meno vulnerabile (5 gruppi di uguale numero di sezioni)"; descrizione corretta;
  etichetta "CENSIMENTO · calcolo".

**M4. OMI: stesse classi in €/m² per tutte le 14 tipologie.** Le classi (1.000-3.500 €/m²) vanno bene per le
abitazioni, ma capannoni (315-390) e magazzini (300-575) escono tutti di un colore; i box quasi tutti nella prima
classe. **Proposta:** classi per tipologia; e ridurre le tipologie a 4-5 (abitazioni, negozi, uffici, box,
capannoni).

**M5. Colori rosso-verde.** Offerta per abitante, accessibilità, vulnerabilità, criticità usano scale rosso→verde,
illeggibili per chi non distingue rosso e verde (circa 1 uomo su 12). **Proposta:** scale a una tinta (chiaro→scuro)
o divergenti accessibili (es. viola–arancio).

**M6. Sfondo satellite e griglia accesi all'apertura.** Per le mappe a colori per area la buona pratica è uno sfondo
chiaro e neutro; il satellite cambia i colori e copre le differenze. **Proposta:** partenza con "Mappa chiara",
griglia spenta.

**M7. Legende con pochi numeri e in formato inglese.** Scale da 5 colori con solo 2 soglie scritte ("7.5", "22.4"),
punto decimale all'inglese; IMQ "basso/alto" senza numeri e con la frase falsa "quantili della vista" (le soglie sono
su tutte le zone). **Proposta:** 4 soglie scritte, virgola decimale, unità di misura, frase "5 gruppi con lo stesso
numero di sezioni".

**M8. Codici al posto dei nomi.** Schede e tooltip dicono "Comune 001272", "Comune 001156": per chi non conosce
i codici ISTAT non vuol dire niente. **Proposta:** aggiungere i nomi dei comuni (tabella ISTAT, una volta sola).

**M9. Telefono.** Pannello e legenda coprono ~70% dello schermo; i pulsanti dello zoom coprono il tasto per chiudere
il pannello; la barra della scala finisce sotto la legenda. **Proposta:** legenda chiusa di partenza sotto 640 px,
pulsanti zoom spostati in basso.

**M10. Titolo e frase iniziale non dicono a cosa serve la mappa.** "Offerta GTT programmata, traffico 5T e mezzi
GTT all'ultimo aggiornamento" descrive 2 temi su 10. **Proposta:** "Come si muove Torino: dove vive la gente, dove
passa il trasporto pubblico, dove mancano i servizi." + una riga "Dati: orari GTT, censimento 2021, indagine IMQ".

**M11. "Offerta per abitante" senza avviso sulla cintura nella legenda.** Fuori Torino mancano treni SFM e altri
operatori; l'avviso c'è solo nella guida in fondo. **Proposta:** una riga in legenda.

**M12. Avvisi GTT del 9/10 senza data.** 115 avvisi "ancora attivi" alla generazione; oggi 5 sono già scaduti e
nessuna scritta dice che è una fotografia del 9/10. **Proposta:** "Avvisi GTT al 9/10" oppure toglierli dalla
versione portfolio.

---

## Gravità BASSA — rifiniture

- **B1.** Tendina "Visualizzazione" di Servizio: le voci del profilo residenti compaiono **prima** di quella
  predefinita (ordine del codice).
- **B2.** Codice morto: "Zone statistiche" (94 zone del 2011) non è più usato da nessun tema, ma la guida lo
  descrive ancora.
- **B3.** Testi troppo tecnici per il portfolio: "celle pesate di ~50 m", "Accuratezza: 1", "il valore 5T è già in
  veicoli/ora", "EPSG:3003", "Fermata n. 1234", "rilancia gli script 01 e 04", nomi di file `.bat` e `.py` nei
  messaggi. Vanno in un "approfondisci" o tolti.
- **B4.** Descrizioni dei temi lunghe (IMQ ~300 caratteri, OMI ~200): tenerle sotto ~120 caratteri.
- **B5.** La mappa non è rigenerata dopo il ritocco del modello del 18/10 (3 frasi della guida).
- **B6.** Peso del file 28,8 MB, più i file in `data/`: lento da aprire su telefono.
- **B7.** Sfondi Esri usati senza chiave: per una pubblicazione va controllato che le condizioni d'uso lo
  permettano (in alternativa sfondi OpenStreetMap/CARTO con attribuzione).

---

## Doppioni e temi da togliere o accorpare (proposte)

| Oggi | Proposta | Perché |
|---|---|---|
| Servizio → Criticità | **togliere** | doppione rotto di "Offerta per abitante" (A1) |
| Servizio → Profilo residenti (occupati, 5-14, 65+) | **spostare** in Vulnerabilità come "Chi abita qui" | occupati e anziani sono già componenti della vulnerabilità |
| Accessibilità → Fermate a piedi | **togliere** (resta Servizio → Solo offerta) | due modi di dire "quante fermate ho vicino" |
| Tempo reale e flotta + Replay + Segnalazioni adesso | **un solo tema** "Una giornata registrata" | il "tempo reale" non esiste per chi guarda (A4) |
| Catalogo dei dati (6 gruppi, ~170.000 oggetti, di cui 132.000 alberate) | **togliere dalla versione portfolio** (o spostare nella guida) | è un inventario di dati, non risponde a una domanda; gli unici dati che servono sono già in Accessibilità |
| OMI (14 tipologie) | tenere, **ridotto** a 4-5 tipologie | contesto utile (dove costa vivere) ma fuori tema "mobilità" |
| Pendolarismo ISTAT e IMQ | tenere entrambi, **spiegare la differenza** in una riga | ISTAT = lavoro/studio comune→Torino; IMQ = tutti gli spostamenti per zona |

Con queste scelte i temi passano da 10 a 7: Servizio e abitanti · Dove mancano i servizi · Accessibilità ·
Vulnerabilità e residenti · Chi va dove (IMQ + pendolari) · Una giornata registrata (+ traffico tipico) ·
Valore immobiliare.

---

## Città e area metropolitana: cosa copre ogni tema

| Tema | Copertura | Nota |
|---|---|---|
| Sezioni (servizio, accessibilità, vulnerabilità, dove mancano) | Torino + 68 comuni (8.317 sezioni, 1.557.493 abitanti; Torino 4.044 / 848.748) | servizi in cintura da OSM: non confrontabili (A2) |
| Pendolari | stessi 68 comuni + Torino | + 1.681 comuni fuori area solo in legenda |
| IMQ | 101 zone di tutta la Città metropolitana | area più grande delle altre: il pulsante "cintura" non la mostra tutta |
| OMI | 68 comuni | |
| Velocità commerciale, sensori 5T | rete GTT e 112 sensori (quasi tutti a Torino) | |
| Zone statistiche (non usate) | solo Torino, confini 2011 | B2 |

---

## Dati ricontrollati (numeri coerenti con la memoria)

8.317 sezioni, 1.557.493 abitanti (Torino 848.748) ✓ · 7.036 fermate con passaggi su 7.045 ✓ · 215 linee (204 bus,
9 tram, 1 metro, 1 funicolare) ✓ · accessibilità con 24 fasce TP per sezione ✓, nessuna sezione mancante ✓ ·
pendolari lavoro 138.605 entrano / 71.297 escono / 212.249 interni ✓ (uguali ai valori attesi) · vulnerabilità: 50
sezioni senza indice · velocità: 133 linee, 4.449 celle, km/h tipici 12-19 ✓ (problema date in M1) · 25 fermate
senza passaggi nel feriale (normale: servizi festivi o sospesi).

---

## Ordine di lavoro proposto (dopo l'ok di Leo)

1. ✅ **Fatto il 18/10** (mappa rigenerata e provata nel browser): A1 Criticità tolta (menu, legenda, schede,
   pendolari); A3 quote IMQ con classi 5-10-15-20% (pubblico) e 50-60-70-80% (privato) e numeri in legenda, le altre
   misure IMQ con le soglie scritte; M1 script 04 scarta le letture con ora della posizione lontana oltre 1 h dalla
   lettura (3.312 righe), legenda "dal 4 ott al 18 ott", testi sui ritardi → Risultato 4; M2 testi accessibilità
   "partenza alle HH:00 di un giorno feriale". Nuovo problema visto durante la prova (**B8**): la scheda di Torino in
   Pendolarismo scrive "Flusso interno: 332.397 (lavoro)" ma il numero è lavoro + studio.
2. A2 Torino/cintura in Accessibilità e Dove mancano — decisione di Leo sulla resa della cintura.
3. Accorpamento dei temi (tabella sopra) e A4 tempo reale → giornata registrata.
4. Testi per il portfolio (M3, M7, M8, M10, B3, B4) e colori (M5, M6).
5. Telefono e peso (M9, B6), sfondi (B7).
6. Rigenerare la mappa e ricontrollare nel browser tema per tema.
