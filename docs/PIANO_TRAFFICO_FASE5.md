# Piano traffico veicolare — Fase 5: giro di correzione (assi, corsie, ZTL, TP per posizione, modello)

Scritto il 18/10/2026 dopo l'esito della Fase 4 (`docs/ESITO_FASE4_TRAFFICO.md`) e il confronto con la conoscenza della città di Leo
(`docs/CONOSCENZA_TORINO_LEO.md`). Piani precedenti che restano validi per criteri e regole: `PIANO_TRAFFICO_FASE3.md` (criteri di riuscita,
classi C-ASSOLUTO / C-INDICE / C-DEBOLE / C-NO) e `PIANO_TRAFFICO_FASE4.md` (regola V3 contro V0, fasce di errore, definizioni di partenza).

## 0. Perché questa fase (in parole semplici)

La Fase 4 ha fatto girare tutta la catena (traffico → bus/tram → incrocio) ma la lista finale "molto traffico, poco trasporto pubblico" non è affidabile:

1. **Il trasporto pubblico è misurato male.** Si contano i bus che corrono *sulla* strada (con aggancio delle forme delle linee), e il risultato è incoerente (Corso Cairoli
   ha 2 linee ma 0,0 passaggi all'ora). Quello che interessa è se la strada è *servita*: ci sono fermate vicine con un buon servizio. Si misura con le **coordinate delle fermate**,
   non con i nomi (il nome di una fermata non dice dove sta; vedi sezione 1, regola 4).
2. **L'unità di analisi è sbagliata.** Oggi un "corridoio" è tutto ciò che ha lo stesso nome: Corso Vittorio Emanuele II è 13 km con un solo numero; Corso Francia sparisce
   dall'elenco di Torino perché prende l'etichetta di un altro comune; Via Agudio e Corso Sturzo sono la stessa strada ma hanno valori molto diversi. Serve l'**asse** (la strada
   come la vede chi la percorre, anche se cambia nome) diviso in **tratte** di lunghezza confrontabile.
3. **Il modello del traffico sbaglia in modo sistematico** (sottostima il semicentro, sopravvaluta raccordi e strade corte), non conosce le **corsie** né la **ZTL**, e la congestione
   non agisce (13,1 → 13,3 minuti in punta tra Piazza Castello e Collegno invece di 20-35).

Questa fase sistema questi quattro punti, poi ripubblica numeri, fasce di errore, graduatoria e incrocio. Il metodo di valutazione del modello (leave-one-out sui 20 sensori) e le
classi di esito **non cambiano**: una modifica che non migliora secondo le regole di questo piano non si adotta.

## 1. Decisioni e regole (da Leo, 17-18/10)

1. **Risultato finale** = numeri assoluti con fascia di errore dichiarata (50%: circa ±32%; 90%: circa ±59%, più larghe fuori dall'intervallo validato), valori relativi e
   graduatoria, con la classe di esito (oggi C-DEBOLE) accanto a ogni numero. Solo strade grandi (vedi 7), con meno nomi ma più solide.
2. **Trasporto pubblico = accessibilità (vicinanza di fermate con buon servizio)**, non i soli bus sulla strada. Definizione operativa al pacchetto D.
3. **La conoscenza di Leo** (`CONOSCENZA_TORINO_LEO.md`) è un **controllo di buon senso, non un dato di taratura**: si usa per verificare e riferire, mai per scegliere fra varianti
   né per tarare coefficienti. Il centro-centro (ZTL storica, Piazza Castello) non è prioritario.
4. **Le fermate si trovano per posizione, mai per nome** (nome di fermata ≠ nome della strada su cui sta). Nessun confronto fra nomi di fermata e nomi di strada, né nel codice né nei controlli.
5. **ZTL**: unire in un'unica mappa tutte le zone con i loro orari; il traffico si stima per fascia oraria.
6. **Corsie**: la pressione di una strada è anche il traffico *per corsia*. Il numero di corsie entra nel modello (capacità) e nell'output (`veic_per_corsia`).
7. **Assi**: i corsi che cambiano nome (Trapani → Lecce → Potenza; Agudio → Sturzo) o che escono dal comune o diventano autostrada (Regina Margherita, Francia, Allamano) vanno trattati come
   un unico asse fin dove sono la stessa strada; l'autostrada o la tangenziale è un'altra classe e l'asse finisce lì.
8. **Un solo giro di valutazione del modello** (pacchetto E), valutato con le regole fissate prima di vedere i risultati. Se non migliora, resta V0 e si dichiara.

## 2. Regole per l'agente

Come nelle fasi precedenti: cartella `C:\projects\Progetti\GTT`; leggi `AGENTS.md`, `MEMORIA_PROGETTO.md` e i piani sopra; ramo `prova`; **nessun commit**; database storico e `data/raw` in sola lettura;
non scrivere né riavviare nulla sul Pi; non modificare `MEMORIA_PROGETTO.md`, `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`; copia `.bak_18ott` prima di cambiare un file esistente; Python del PATH;
pc con 8 GB di RAM (calcoli lunghi in un `.bat` a parte, ripartibili, con log); niente servizi esterni; `pip --user` solo per pacchetti comuni, da annotare. Script numerati da **56** in poi.
Esito in `docs/ESITO_FASE5_TRAFFICO.md`: una riga `PASSO <lettera>: OK` oppure `PASSO <lettera>: FERMO - motivo` per ogni pacchetto, "Decisioni dell'agente", durate, file creati/modificati, anomalie,
e il testo proposto per `MEMORIA_PROGETTO.md` (che non va modificata).

**Ti fermi e scrivi a Leo solo se:** (1) la rete OSM non ha i dati per costruire gli assi in modo sensato (vedi controlli A); (2) un controllo indipendente differisce di oltre il 5% senza spiegazione;
(3) serve qualcosa di vietato; (4) disco o RAM esauriti. Per ogni altro dubbio scegli il default ragionevole, annotalo e vai avanti. Non cercare di far uscire un bel risultato: se è debole, scrivilo con i numeri.

## 3. Pacchetto A — Assi e tratte (script 56-57)

**Obiettivo:** passare da "corridoio = stesso nome" ad **asse = stessa strada** e dividerlo in **tratte** su cui calcolare traffico e trasporto pubblico.

**Costruzione dell'asse (grafo OSM già in `scripts/rete_osm.py`):** a ogni incrocio si collegano due tratti di strada della stessa classe (stesso `highway` o classi adiacenti) che proseguono quasi dritto
(deviazione ≤ 30-35°), scegliendo la coppia con deviazione minima; in presenza di `ref` o di nome uguale il legame è più forte. Gli incroci con rotatorie e svincoli si trattano con regola scritta. L'asse **si ferma** dove la
classe diventa autostrada/tangenziale/raccordo (`motorway`, `trunk` o simili): quello è un altro asse, di classe a parte. Sottopassi, ponti e viadotti (`bridge`, `tunnel`) **non sono assi indipendenti**: ereditano
il flusso dell'asse di cui fanno parte (se serve, restano come tratti con flag).
**Nomi:** ogni asse ha tutti i nomi che attraversa in ordine (es. "Corso Trapani → Corso Lecce → Corso Potenza") e un nome principale (il più lungo). Il comune di un tratto è quello del tratto, non dell'asse
(un asse può attraversare più comuni; in Torino Corso Francia deve comparire).
**Tratte:** ogni asse si divide in tratte fra grandi incroci (incroci con strade dello stesso rango o superiore) e, se serve, ogni 0,5-1,5 km, evitando tratte < 300 m (si uniscono alla vicina). Ogni tratta ha
quartiere (circoscrizione), comune, lunghezza, classe, numero di corsie (pacchetto B), flag ZTL (C).
**Controlli obbligatori:**
- Gli esempi di Leo devono venire giusti: Trapani → Lecce → Potenza, Agudio → Sturzo, Francia (da Torino verso Rivoli, fino all'ingresso in autostrada), Regina Margherita (fino all'autostrada), Allamano, Vittorio Emanuele II,
  Giulio Cesare, Vercelli, Lione (fino a Corso Venezia). Per ciascuno scrivi nome degli assi, lunghezza e dove si ferma.
- Nessun asse con salti di oltre 100 m fra due tratti consecutivi; nessun tratto in due assi; copertura: ≥ 95% dei km di strade di rango ≥ 3 in Torino appartengono a un asse.
- Se più del 10% degli assi risulta incoerente (cambiano classe di colpo o tornano indietro), fermati e scrivilo.
Output: `data/processed/traffico_d/assi.json`, `tratte.csv`, `docs/RAPPORTO_ASSI_TRATTE.txt` (con statistiche, esempi di Leo e i 20 assi più lunghi).

## 4. Pacchetto B — Corsie e capacità (script 58, estende `rete_osm.py`)

- Aggiungi alla lettura OSM i tag `lanes`, `lanes:forward`, `lanes:backward`, `oneway`, `maxspeed`, `width`, `cycleway`/`bus` (corsie riservate se presenti), `bridge`, `tunnel`, `junction`.
  Copia `.bak_18ott` di `rete_osm.py` e conserva compatibilità con gli script 42-50.
- **Copertura:** per classe di strada quanti tratti hanno `lanes`. Dove manca, valori standard dichiarati per classe e per senso unico/doppio senso (con flag `corsie_stimate: true`).
- **Capacità per corsia** (veicoli/ora): valori standard per classe in una tabella dichiarata (partire da motorway ~1.800, primary ~900-1.000, secondary/tertiary urbane ~700-800; l'agente può affinare con fonti pubbliche
  note, scrivendo la fonte). Capacità di tratto = corsie per verso × capacità per corsia.
- **Output per tratta:** `corsie_totali`, `corsie_per_verso`, `corsie_stimate`, `capacita_oraria`. Dopo il pacchetto E si aggiunge `veic_per_corsia` (veicoli/giorno 6-21 diviso corsie totali) e `rapporto_flusso_capacita` in punta.
- Controllo a mano: 10 tratte note (Corso Racconigi, Corso Re Umberto con controviale, Corso Francia, Via Nizza, Corso Vittorio, Lungo Po, Corso Unità d'Italia, Corso Giulio Cesare, Via Agudio, Corso Cosenza) confrontate con i
  tag OSM trovati; riporta quelle in cui le corsie ti sembrano sbagliate.
Output: `data/processed/traffico_d/corsie.csv`, `docs/RAPPORTO_CORSIE.txt`.

## 5. Pacchetto C — ZTL unificata e aree pedonali (script 59)

- **Sorgenti da unire:** `data/raw/ztl_csv.zip` (poligoni del Comune con `ORA_INIZIO`, `ORA_FINE`, `SOSPENS`, probabilmente aggiornati al 2016-2017), `data/raw/5t_access_control_20261014.xml` (ZTL del feed 5T, validità 2022-2024, poligoni in lat/lon),
  la tabella `ztl_5t` raccolta sul Pi (stato dichiarato, ferma al 2024), `data/raw/aree_pedonali_csv.zip` (poligoni delle aree pedonali). Apri ogni sorgente e scrivi quali campi ha (orari, giorni, sospensioni, validità).
- **Unione:** un unico file `data/processed/traffico_d/ztl_unificata.json` con, per ogni zona: poligono (lat/lon), nome, fonti che la contengono, orari e giorni di attività (fasce: per es. lun-ven 7:30-10:30; sabato...; se le
  fonti discordano elenca le discordanze e usa la più recente dichiarando la scelta), validità, stato (attiva/sospesa), flag `fonte_vecchia`. Poligoni sovrapposti si uniscono per fascia oraria.
- **Aree pedonali:** i tratti dentro una zona pedonale (es. Via Roma) non sono percorribili dalle auto: escluderli dall'instradamento e marcarli `pedonale: true`.
- **Uso:** per ogni tratta calcola `ztl_frazione` (quota di lunghezza dentro una ZTL) e `ztl_fasce` (le ore attive). Nel modello (E), fuori dalle ore ZTL il traffico si stima normalmente; **dentro le ore ZTL** i tratti ZTL non
  sono usati per il traffico di attraversamento (percorsi vietati salvo accessi locali). Non inventare una quota di autorizzati: se serve, lasciala come parametro dichiarato (default: nessuna stima, il tratto in ZTL non
  entra nelle graduatorie nelle ore attive e il totale diurno riporta `ztl_parziale: true`).
- **Controlli:** i sensori 5T che cadono dentro una ZTL o in un'area pedonale (se ce ne sono) vanno elencati e trattati a parte; Via Roma, Piazza Castello, Via Montebello, Via San Massimo, Corso Cairoli (tratto vicino alla ZTL) devono
  avere flag coerenti con quello che Leo sa (`CONOSCENZA_TORINO_LEO.md`); riporta eventuali incoerenze senza forzare i dati.
Output: `ztl_unificata.json`, `tratte_ztl.csv`, `docs/RAPPORTO_ZTL.txt` (mappa riassuntiva in testo: n. zone, orari, discordanze).

## 6. Pacchetto D — Trasporto pubblico per posizione (script 60-61)

**Principio:** una strada è "servita" se ci sono fermate con buon servizio vicine, indipendentemente dal nome. Si usano solo **coordinate** di fermate (`stops.txt` lat/lon) e di forme (`shapes.txt`).

1. **Frequenza per fermata** dal GTFS (`data/raw/gtt_gtfs_20261003_224530.zip`), giorno feriale tipico (mercoledì 14/10/2026, già usato nella Fase 4; ricontrolla il calendario e annota): partenze/ora
   nella punta del mattino (7-9) e della sera (17-19), numero di linee, distinguendo **bus/tram** (route_type 0 e 3 e simili urbani) da **metropolitana e ferrovia** (1 e 2). Le fermate che appartengono a stazioni (parent_station) si trattano come
   una sola. Controlla che le partenze contate siano uguali a quelle che ottieni da `trips`+`calendar` con un altro metodo.
2. **Copertura della tratta:** per ogni tratta, quota della lunghezza entro **300 m** (distanza in linea d'aria, default) da una fermata bus/tram con **almeno 4 partenze/ora in punta** (somma dei due versi; cioè un
   mezzo ogni 15 minuti). Campi: `copertura_300`, `freq_max_300` (massimo passaggi/ora di una fermata vicina), `n_linee_300`, `dist_mediana_fermata_m`, `n_fermate_300`.
   **Sensibilità obbligatoria:** 200 m, 300 m, 400 m e soglia 4/h, 6/h, 2/h (riporta in tabella quante tratte cambiano gruppo).
3. **Metropolitana e ferrovia** (solo stazioni, per posizione): una stazione entro **600 m** conta come servizio; campi separati `metro_600`, `ferrovia_600`, `copertura_con_metro` (bus/tram oppure stazione).
4. **Opzionale (se facile, altrimenti salta e scrivilo):** `residenti_300` (abitanti nelle sezioni di censimento entro 300 m, da `sezioni_torino.json`) e `acc_tp_media` (accessibilità TP già calcolata, `accessibilita.json`,
   media sulle sezioni vicine). Servono come colonne informative per leggere la graduatoria, non entrano nella definizione di "poco TP".
5. **Metrica vecchia (passaggi sulla strada, Fase 4):** non è più la misura principale. **Diagnostica richiesta:** spiega perché Corso Cairoli risulta con le linee 24 e 93 ma con 0,0 passaggi/ora, e perché Corso Fiume ha una linea e 0,0.
   Verifica a mano 5 tratte: quali fermate (per coordinate) ci sono entro 300 m, quanti passaggi/ora ha ciascuna, e se l'aggancio forma → strada ha sbagliato. Scrivi la causa trovata.
6. **Controlli di buon senso (per posizione, mai per nome):** Corso Francia, Corso Regina Margherita, Via Nizza, Corso Vittorio, Corso Giulio Cesare con copertura alta; 10 tratte con copertura 0 viste su una mappa mentale/descrizione
   (nome dell'asse, quartiere, distanza dalla fermata più vicina) e giudicate plausibili o sospette dall'agente.
Output: `data/processed/traffico_d/tp_fermate.csv`, `tp_tratte.csv`, `docs/RAPPORTO_TP_ACCESSIBILITA.txt`.

## 7. Pacchetto E — Modello del traffico V4 (script 62-64) [valutazione unica]

**Cosa cambia rispetto a V0** (V3 della Fase 4 non è stato adottato: ha migliorato l'errore ma non il rango; l'ablazione ha mostrato che gli attrattori servono, mentre la congestione non agiva davvero):
1. **Destinazioni per attrattori** come in V3 (pacchetto della Fase 4): riusa `49_v3_punti_domanda.py` e conferma i pesi (lavoro: uffici/sedi/attività; scuola/università: scuole e università; acquisti: attività; cure: ospedali e consultori).
2. **Congestione fatta funzionare.** La Fase 4 ha lasciato i tempi quasi invariati: capire e correggere il perché (scala dei flussi nelle formule, domanda per fascia oraria, capacità). Procedura: domanda IMQ per fasce orarie (da `ORA_PAR`),
   flusso di punta = quota della fascia 7-9 e 17-19; capacità da pacchetto B (corsie × capacità per corsia); funzione di ritardo BPR (α=0,15, β=4) o equivalente; metodo delle medie successive con 10-20 iterazioni;
   **un solo parametro di scala** (moltiplicatore delle capacità) tarato sul tempo di viaggio nelle ore di punta, **non** sui flussi dei sensori. Test obbligatori: Piazza Castello → Collegno in punta entro 20-35 minuti; altri 5 percorsi noti con
   tempi plausibili (scrivili); velocità del modello sui tratti dei sensori in punta confrontate con quelle misurate (`velocita_5t.json`) e riportate in tabella. Se dopo un tentativo ragionevole la congestione resta inattiva, dichiaralo e tieni V0+attrattori.
3. **Porte di bordo:** solo strade di rango ≥ 3; quote per capacità e direzione; sensori fuori Torino usati per verificare le quote di ingresso dove possibile (conta quanti).
4. **ZTL e aree pedonali** dal pacchetto C (tratti pedonali tolti dal grafo; tratti ZTL non usati per attraversamento nelle ore attive).
5. **Il flusso si calcola per tratta**, poi si aggrega per asse (media pesata per lunghezza) e per tratta di asse. Un asse deve avere flussi *coerenti* da una tratta all'altra senza salti > 40% fra tratte consecutive se non c'è un incrocio importante;
   i salti si segnalano (es. Agudio 14.400 → Sturzo 5.400 della Fase 4).

**Valutazione (regola fissata ora, valutata una volta):** stesse 20 unità-sensore e stessa taratura leave-one-out della Fase 3, stesse metriche (errore mediano con intervallo 90%, p90, Spearman ρ, n). Confronta V0 e V4.
- **Si adotta V4 se** ρ(V4) ≥ ρ(V0) **e** l'errore mediano di V4 non è peggiore di quello di V0 di più di 3 punti. Altrimenti si tiene V0 e si scrive "V4 non migliora"; in ogni caso gli assi, le tratte, le corsie, la ZTL e il TP
  (pacchetti A-D) si applicano al modello scelto.
- Fino a 3 ablazioni solo descrittive (V4 senza attrattori / senza congestione / senza porte), per dire cosa conta: **la variante finale è V4 oppure V0**, non si sceglie fra le ablazioni.
- **Riferisci, senza usarlo per scegliere,** l'accordo con `CONOSCENZA_TORINO_LEO.md`: quanti dei 7 confronti sono giusti, quante delle 18 strade giudicate da Leo cadono nella fascia giusta (A/B/C con soglie dichiarate), correlazione di rango sulle 25 strade, e dove V4 migliora o peggiora rispetto a V0.
- Tempo massimo indicativo: 3 ore di lavoro; l'assegnazione completa dura meno di 15 minuti anche con 20 iterazioni.
Output: `data/processed/traffico_d/e/…` (flussi per tratta, bande orarie), `docs/RAPPORTO_TRAFFICO_V4.txt` (tabelle V0/V4/ablazioni con n, errori, ρ, intervalli, tempi di viaggio, velocità vs sensori, accordo con Leo).

## 8. Pacchetto F — Affidabilità, unità di analisi e fasce (script 65)

**Regole fissate ora (prima di guardare i risultati):**
1. **Universo di analisi** = tratte di asse che stanno nel comune di Torino, di rango ≥ 3 (punteggio importanza ≥ 3 o classe `primary` e superiori), lunghezza ≥ 300 m, escluse autostrade/tangenziali/raccordi e ponti/sottopassi
   che sono parte di un asse (non indipendenti). Prima cintura (comuni confinanti): stessa regola, tabella separata.
2. **`affidabile: false`** se: (a) la tratta è entro 1,5 km da una "porta" del bordo; (b) rango ≤ 2 e flusso > 12.000 veic/giorno senza sensore; (c) la tratta è un ponte/sottopasso/svincolo indipendente (se non ereditato dall'asse);
   (d) il flusso si discosta di oltre il 100% dalla mediana delle tratte consecutive dello stesso asse senza un incrocio importante. Elenca per ogni regola quante tratte e km, e le prime 20 per flusso. Via Palestrina, Corso Monte Lungo e
   Via Quarto dei Mille devono essere esaminate esplicitamente: scrivi a quale regola (se una) cadono.
3. **Intervallo validato:** da 0,7 × (flusso minimo misurato dai sensori) a 1,3 × (massimo). Fuori da questo intervallo il valore è `estrapolazione: true` e la fascia al 90% si allarga di un fattore dichiarato (default ×2, come in Fase 4).
4. **Fasce di errore:** `fascia_50` e `fascia_90` dagli errori leave-one-out della variante finale (V4 o V0), con una sola regola scritta. Dove c'è un sensore sullo stesso asse: valore misurato (×2 se un solo verso) con `misurato: true`.
5. **`fiducia`:** alta (sensore sulla tratta), media (modello nell'intervallo validato, rango ≥ 3, `affidabile` vero), bassa (altro).

Output: `data/processed/traffico_d/tratte_traffico.json` (per tratta: veic_giorno, fasce, veic_per_corsia, punta mattina/sera se stimata, misurato/stimato/estrapolazione, affidabile+motivo, fiducia, classe di esito), `docs/RAPPORTO_AFFIDABILITA.txt`.

## 9. Pacchetto G — Pubblicazione e incrocio (script 66)

**Valori e graduatoria (Torino e prima cintura, tabelle separate):**
- `veic_giorno` con fascia 50% e 90%, `indice_1_5` (quintili nell'universo), `rapporto_su_mediana`, `posizione_torino` (1 = più traffico) e `posizione_per_corsia` (graduatoria per `veic_per_corsia`).
- `classe_esito` della Fase 3 (oggi C-DEBOLE) accanto a ogni numero, `affidabile` e motivo, `fiducia`.

**Incrocio traffico × trasporto pubblico (definizioni fissate ora):**
- **Molto traffico** = nel terzo più alto per `veic_giorno` fra le tratte dell'universo che hanno `affidabile: true`, **e** almeno pari al limite basso dell'intervallo validato (pacchetto F, punto 3).
  Versione "per corsia": stesso criterio su `veic_per_corsia`. Riporta entrambe.
- **Poco TP** = `copertura_con_metro` ≤ 50% della lunghezza della tratta. Sensibilità: 30% e 70%; e con la sola `copertura_300` (senza metro). Le tratte nella soglia vanno nella tabella "da guardare".
- **Robustezza:** una tratta è `robusta` se resta "molto traffico" con il traffico moltiplicato per 0,65 e per 1,35 (circa la fascia al 50%) e con le soglie di sensibilità del pacchetto D.
- **Divario** = percentile del traffico − percentile della copertura TP, a parità di condizioni. Elenca le prime 30 tratte con: asse (tutti i nomi), quartiere, lunghezza, traffico con fascia, corsie, veic/corsia, copertura TP, frequenza massima vicina, linee,
  metro/ferrovia vicina, robustezza, fiducia, motivi di affidabilità. Raggruppa le tratte consecutive dello stesso asse in "assi da guardare" per la leggibilità, senza perdere i dati per tratta.
- **Controlli:** la lista non deve essere dominata da raccordi, sottopassi o tratte di bordo; descrivi 3 esempi in chiaro (una tratta nel gruppo, una con molto traffico e buon TP, una con poco traffico e poco TP); confronta la lista con
  `CONOSCENZA_TORINO_LEO.md` (strade che Leo giudica molto trafficate e poco servite) e riporta dove la lista contraddice la sua conoscenza, **senza correggerla a mano**.
- Limiti da dichiarare ovunque: stime di traffico deboli (C-DEBOLE o la classe finale), sensori a un solo verso, IMQ solo residenti 11-84 anni (niente merci, turisti, non residenti), offerta TP da orario programmato (non tiene conto di
  ritardi, capienza, affollamento), centro (ZTL e aree pedonali) non stimato in modo affidabile.
Output: `data/processed/risultato8_traffico_tp_v2.json` (non sovrascrivere la v1), `docs/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt`. Nessuna mappa in questa fase.

## 10. Pacchetto H — Raccolta e rilancio

- **Lunedì 19/10:** fetch con `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat` poi `TRAFFICO_RILANCIA_SENSORI.bat` (estendilo con i nuovi script dove dipendono dai sensori; il modello, gli assi, la ZTL e il TP non cambiano con il fetch).
  Controlla nel database copiato che compaiano i tre codici `~2` (verificati sul Pi il 17/10) e che i dati storici dei sensori 26/33/35-37 non siano cambiati.
- **Dopo il 25/10 (cambio ora legale):** controllo manuale di `26_velocita_5t.py` sui giorni a cavallo.
- **I tre sensori nuovi** (`40123~2`, `40189~2`, `13077~2`) entrano nelle unità di valutazione solo quando hanno ≥ 6 giorni feriali validi e senza cambiare le soglie.

## 11. Consegne e verifiche indipendenti

`docs/ESITO_FASE5_TRAFFICO.md` (come in sezione 2) con: variante finale con n, errore mediano e IC90, ρ, classe; numero di assi e tratte e km nell'universo di Torino; copertura TP; i 10 assi con più traffico e meno TP (nome, traffico con fascia, copertura);
accordo con la conoscenza di Leo; anomalie. **Verifiche indipendenti obbligatorie:** (1) partenze GTFS ricalcolate con un altro metodo; (2) fattore di taratura e tre errori leave-one-out della variante finale rifatti a mano con la formula giusta;
(3) cinque tratte seguite dai dati grezzi al valore finale (OSM → asse → flusso → copertura TP → gruppo); (4) tre assi cambiati di nome controllati contro la mappa OSM; (5) `git status` senza file vietati toccati.

## 12. Prompt per l'agente (da incollare tutto, una volta sola)

```
Sei l'agente che esegue la Fase 5 del Risultato 8 (traffico veicolare) del progetto GTT di Leo, sul PC di Leo, cartella C:\projects\Progetti\GTT.

Leggi per primi: AGENTS.md, MEMORIA_PROGETTO.md, docs/PIANO_TRAFFICO_FASE3.md, docs/PIANO_TRAFFICO_FASE4.md, docs/ESITO_FASE4_TRAFFICO.md, docs/CONOSCENZA_TORINO_LEO.md e soprattutto
docs/PIANO_TRAFFICO_FASE5.md (il tuo piano). Controlla di essere sul ramo "prova"; se no, fermati.

Obiettivo: correggere la catena della Fase 4 perche' la lista "molto traffico, poco trasporto pubblico" diventi credibile. Esegui i pacchetti A-H del piano: A assi e tratte (stessa strada anche se cambia nome o comune,
tratte di 0,3-1,5 km), B corsie e capacita', C ZTL unificata con orari e aree pedonali, D trasporto pubblico misurato con le COORDINATE delle fermate (mai con i nomi: il nome di una fermata non dice dove sta), E modello V4 valutato una
sola volta con le regole del piano, F affidabilita' e fasce di errore, G pubblicazione e incrocio, H raccolta/rilancio. Ordine: A, B, C prima (struttura); poi D ed E (possono procedere in parallelo); poi F e G; H in coda.
Hai liberta' sulle scelte di realizzazione. Non si cambiano: i criteri di riuscita della Fase 3, la regola V4-contro-V0, le definizioni di "molto traffico", "poco TP", "affidabile" e "robusto", e il fatto che
docs/CONOSCENZA_TORINO_LEO.md e' un controllo di buon senso: non tarare e non scegliere varianti in base ad esso, riferisci soltanto l'accordo.

Paletti: nessun commit; database e data/raw in sola lettura; non scrivere ne' riavviare nulla sul Pi; non modificare MEMORIA_PROGETTO.md, scripts/mappa_template.html, scripts/04_genera_mappa.py; copia .bak_18ott prima di cambiare
un file esistente (in particolare scripts/rete_osm.py); calcoli lunghi in un .bat a parte, ripartibili, con log; PC con 8 GB di RAM; pip --user solo per pacchetti comuni (da annotare); niente servizi esterni; script numerati da 56.

Fermati e scrivi a Leo SOLO se: la rete OSM non permette di costruire assi sensati (piu' del 10% incoerenti); un controllo di coerenza differisce di oltre il 5% e non lo sai spiegare; serve qualcosa che il piano vieta;
disco o RAM esauriti. Altrimenti vai avanti col default piu' ragionevole e annotalo. Se V4 non migliora V0 secondo la regola del piano, tieni V0, scrivilo e vai avanti: nessun altro tentativo di modello.

Scrivi in docs/ESITO_FASE5_TRAFFICO.md una riga "PASSO <lettera>: OK" o "PASSO <lettera>: FERMO - motivo" per pacchetto, le "Decisioni dell'agente" e le verifiche indipendenti della sezione 11. Non cercare di far uscire
un bel risultato: se e' debole, scrivilo con i numeri.

Risposta finale a Leo (massimo 14 righe): variante finale (V0 o V4) con errore mediano, rho di Spearman, n e intervalli, e la classe di esito; accuratezza dichiarata dei numeri assoluti (fascia 50% e 90%); quanti assi e tratte e quanti km
nell'universo di Torino; quota di lunghezza coperta dal trasporto pubblico; i 10 assi di Torino con piu' traffico e meno TP (nomi, traffico con fascia, copertura, corsie); accordo con la conoscenza di Leo (confronti giusti su 7, strade nella fascia
giusta su 18); causa trovata per Cairoli (linee ma 0 passaggi); anomalie; durata; file principali creati o modificati.
```
