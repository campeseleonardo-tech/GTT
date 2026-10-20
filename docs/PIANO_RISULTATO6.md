# Risultato 6 — Parcheggi per lasciare l'auto: STATO ATTUALE (corretto il 20/10/2026)

Correzioni eseguite sul PC il 20/10 (esito: `docs/archivio/correzioni_20ott/ESITO_CORREZIONI_GENERALI.md`, analisi e
piano nella stessa cartella) e **ricontrollate da Claude** sui dati dentro `mappa_torino.html` (classi, aree, distanze
dei 20 punti dal centro: tutto coincide). Catena: `scripts\RISULTATO6_RIFAI.bat` (71, 72, 73, 81, 82, 83, 84, 79, 85,
04, schede, prova delle pagine; ~4 minuti). Rapporti: `docs/RAPPORTO_R6_*.txt`.

## Domanda
Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, così da togliere
auto dal centro?

## Criteri (valori decisi con Leo il 20/10)
| Criterio | Valore |
|---|---|
| Auto in entrata al mattino | IMQ 2022, partenza 06-10, conducente + car sharing: 87.162 dalla cintura e da fuori; torinesi dei quartieri periferici verso Q001-Q009 inclusi (29.988 = 34%, soglia 25%) |
| Chi già oggi lascia l'auto | 5,8% (5.067 auto, **64 interviste**) |
| Auto che passano accanto | instradamento sul modello del traffico V0 (stima debole ±38%) |
| Fermate importanti | 10% più alto fra 3.898 luoghi fuori da Q001-Q009: **391**; segnali a2, b2, c4, e a pesi uguali |
| Parcheggi adatti | aperti, fuori da Q001-Q009, ≥ 20 posti, non di ospedali/università/centri commerciali: 1.874 (157.103 posti) |
| Fermata coperta | posti adatti entro 400 m a piedi ≥ auto che passano × 5,8% |

## Risultati
- **253 fermate importanti su 391 senza posti bastanti** (99 senza nessun parcheggio adatto, 154 con posti
  insufficienti); 116 con posti sufficienti; 22 con poche auto da fermare.
- **76 aree**: 20 critiche, 5 scarse, 5 buone, **46 «Pochi dati»** (meno di 5 fermate).
- **20 punti prioritari**, quasi tutti fra 3,5 e 9,6 km dal centro (uno solo sotto 2,5 km: Gioanetti, 1,4 km; prima
  erano 7): in testa Maroncelli e Bosso (Moncalieri), Pellerina (Le Vallette), Santa Rita.
- **Validazione sui 5 interscambi del Comune**: solo Stura dice qualcosa (pieno, su strada con molte auto: coerente);
  Caio Mario contatore fermo, Fermi non trasmette, Venchi Unica a metà, Sofia poco usato con molte auto accanto.
- Mappa 13,6 MB (era 23,6); 142 parcheggi mostrati.

## Punti deboli trovati da Claude nel ricontrollo (20/10, sera) — da decidere con Leo
1. **Stesse auto contate in più punti.** Maroncelli, Bosso e Ponte Cavalieri Templari (stesso asse di Moncalieri,
   0,7-1,2 km uno dall'altro) mostrano 627 + 540 + 350 posti che mancano, ma sono in buona parte le stesse auto. La
   somma dei «posti che mancano» nei 20 punti è 6.356, più delle auto che in tutto si potrebbero fermare (5.067).
   Coppie a meno di 1 km anche a Mirafiori (Barbera-Vigliani, Settembrini-Svincolo Mirafiori-Cattaneo) e alle Vallette
   (Pellerina-Pianezza-Toscana). Il totale non è mostrato in pagina, ma il grafico dei 10 punti lo suggerisce.
   Proposta: un punto per asse d'ingresso (come la regola del traffico: l'unità è l'asse).
2. **Gioanetti a 1,4 km dal centro**: fermare lì un'auto fa risparmiare poca strada. Proposta: distanza minima dal
   centro (es. 3 km) o peso per i km risparmiati.
3. **Quota del 5,8% su 64 interviste** moltiplicata per una stima di traffico al ±38%: i «posti che mancano» sono
   ordini di grandezza; meglio mostrarli arrotondati (es. «circa 600») o in fasce.
4. **Il modello del traffico senza code** manda le auto sulle strade veloci: Corso Francia non è fra i 15 luoghi con
   più auto in entrata, Strada Trieste (Moncalieri) è in cima. Si può controllare con i sensori 5T al mattino in
   entrata (dati che ci sono già).
5. **Validazione quasi vuota** (1 interscambio su 5 informativo) e **46 aree su 76 senza colore**: la vista «aree»
   dice poco.

## Prossimi passi
Dopo ≥ 5 feriali di parcheggi (inizio novembre): `scripts\RISULTATO6_RIFAI.bat`. Screenshot di Leo. Decidere i punti
1-5 qui sopra. Eventi (stadi, palazzetti): congelati (Leo, 20/10).

---

# Riepilogo del 19/10 (PRIMA delle correzioni: superato, resta per la storia)

## Domanda
«Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico?» — per capire dove mettere un parcheggio nuovo o ampliarne uno, così da togliere auto dalla circolazione (si lascia l'auto e si prosegue con il trasporto pubblico). Tutta la città conta, tranne il centro (Q001) per le fermate; i parcheggi contano ovunque.

## Come funziona (criteri, uno per uno)
| Criterio | Valore | Perché |
|---|---|---|
| Fermate importanti | 378 luoghi (fermate entro 40 m = un luogo): il 10% più alto di un punteggio su 4.425 luoghi della Città metropolitana. Il punteggio mescola importanza della strada (strade della Fase 5 con punteggio corretto: primarie ≥ 4, secondarie ≥ 3), corse nelle ore dei pendolari, pendolari della zona, ZTL, calo di velocità ai sensori, nodo treno/metro | sono i punti dove passa più gente e più mezzi |
| Parcheggi | 5.205 trovati (5T, Comune, OpenStreetMap) → 1.774 esclusi (1.048 sosta lungo strada, 385 solo clienti, 341 privati) → **3.431 considerati** → 1.147 con almeno 50 posti (175.356 posti) | per chi lascia l'auto contano i parcheggi aperti dove si può stare tutto il giorno |
| Posti | dichiarati (374) o **stimati a 25 m² a posto** (2.902; mediana verificata 24,4-25,4 su 152-172 parcheggi con posti dichiarati, fascia 14-33 m²: incertezza ±30%) | spesso il numero di posti non c'è |
| Distanza | **200 m** in linea d'aria (a 100 m: 315 fermate senza 50 posti; a 400 m: 66) | è il criterio che pesa di più |
| Fermata coperta | almeno **50 posti nominali** entro 200 m: 147 senza nessun parcheggio, 59 con 1-49 posti, 172 con 50+ | |
| Riempimento | solo **misurato** (feed 5T, 32-36 garage, 2 giorni feriali, ore 10-16): pieno ≥ 85%, con posti liberi < 50%. Le osservazioni di Leo (es. Fermi sempre pieno) **non entrano nei dati**: controllo a posteriori nel rapporto (oggi «non confermabile»: nessun parcheggio vicino trasmette) | un parcheggio pieno non serve |
| Aree | celle esagonali di circa 2 km² (lato 900 m): Critica ≥ 60% delle fermate senza 50 posti, Scarsa 30-59%, Buona < 30%; sotto 3 fermate «dato indicativo» | le zone IMQ erano troppo grandi e diseguali |
| 20 punti | fermate senza 50 posti raggruppate entro 1 km, in ordine di punteggio; per ognuno i parcheggi da 100+ posti entro 600 m che potrebbero ampliarsi | risponde a «dove metterne uno o ingrandirlo» |
| Direzioni d'ingresso (solo riferimento in scheda) | 8 settori attorno a Piazza Castello; auto in entrata al mattino (IMQ 2022, 95.297) × 26% (chi già oggi cambia con un mezzo pubblico, 299 interviste) = 24.459 auto; confrontate con i posti | stima di riferimento, non guida la mappa |

## Risultati
- **206 fermate importanti su 378 non hanno vicino un parcheggio con almeno 50 posti** (147 non ne hanno nessuno).
- **73 aree**: 37 critiche, 12 scarse, 24 buone (26 con meno di 3 fermate: indicative). Le zone più scoperte sono Mirafiori (Nord e Sud), San Donato, Crocetta-Cenisia, Parella, parte di Moncalieri.
- **20 punti prioritari**: in testa Settembrini e Pavese (Mirafiori Sud), Industria (San Donato), Metro Spezia e Metro Lingotto (Nizza Millefonti), Provana (Collegno).
- **Parcheggi mostrati in mappa: 212** (58.833 posti): almeno 100 posti entro 400 m da una fermata importante o da un nodo forte (346 nodi: metro, treno, capolinea, frequenti) più i garage 5T con dati; include il Palavela (568 posti stimati, il sito turistico dice «fino a 600»).
- **Riempimento**: 9 parcheggi pieni di giorno (3.041 posti); i dati coprono solo il 25-36% dei posti mostrati. Il grafico più chiaro: le curve a 24 ore dei garage (tre comportamenti: si riempiono di giorno / sono più pieni di notte / dato fermo).
- I 4 interscambi del Comune (Stura, Caio Mario, Sofia, Venchi Unica) non si comportano da interscambio di periferia: Stura è piena di giorno (90%) ma anche di notte (79%), Sofia è residenziale, Caio Mario è quasi vuoto (1,5%, forse contatore fermo), Venchi Unica dato quasi fisso.

## Dove si vede
- **Mappa** (`mappa_torino.html#tema=interscambio`, tema «Parcheggi per lasciare l'auto», 3 viste): «Dove ci sono parcheggi?» (riempimento), «In quali aree mancano parcheggi?» (esagoni rosso/arancione/verde), «Dove servirebbe di più un parcheggio?» (20 punti numerati).
- **Scheda** (`simulazione.html`, Risultato 6): domanda, risposta in 4 frasi, 13 grafici (aree, fermate e parcheggi, 20 punti, profili medi e 6 profili singoli, parcheggi pieni, riferimento per direzione), tabella «I criteri, uno per uno» con sensibilità, sezione «Quanto sono affidabili i dati», metodo, limiti. Gli screenshot (`immagini/r6_torino.png`, `immagini/r6_zoom.png`) li fa Leo.
- Colori: bene/male verde→rosso, quantità neutre blu→arancione, categorie colore proprio; una sola scala per vista.

## Limiti
Riempimento su 2 giorni feriali [DATI SCARSI] e solo per i garage del 5T (Fermi e molti altri non trasmettono); posti stimati ±30% (85% dei parcheggi); OpenStreetMap incompleto; distanze in linea d'aria; indagine IMQ campionaria; i risultati dipendono molto dalla distanza di 200 m; eventi (stadi, palazzetti: Olimpico, Inalpi Arena, Oval) rimandati a un tema a parte (`data/ref/eventi_luoghi.json`).

## File
Script 68-79 (luoghi, parcheggi, riempimento, nodi, segnali, ISTAT 2011, strade 77, eventi 78, dati mappa 79), **80** (aree, 20 punti, direzioni, criteri). Dati in `data/processed/risultato6_v2/` (`porte.json`, `mappa_r6.json`). Rapporti `docs/RAPPORTO_R6V2_*`, `RAPPORTO_R6_PORTE.txt`. Piani e esiti dei passi: `PIANO_RISULTATO6_V2.md`, `…_GIRO2.md`, `PIANO_R6_PORTE/DIREZIONI/ZONE/MIGLIORIE.md` e relativi `ESITO_*`.

## Da sistemare / prossimi passi
Correzioni tecniche in `docs/archivio/r6/PIANO_R6_CORREZIONI.md` (errore `r6Data`, legenda, etichette ripetute, descrizioni dei profili…). Dopo il fetch di domenica 25/10 (≥ 5 feriali): rifare 71→72→73→75→76→80→79 e rigenerare mappa e scheda. Screenshot di Leo. Tema eventi separato (più avanti).

---

# STORIA (non descrive più lo stato attuale)

Deciso con Leo il 14/10/2026.

**Stato (14/10 sera)**: passi 0-5 fatti (versione 1, rapporto in `docs/archivio/r6/RAPPORTO_RISULTATO6.txt`).
Da fare a inizio novembre: punto 0.4 (riempimento parcheggi [MISURATO]) e passo 6 (mappa, `simulazione.html`).

## Domanda

I 4 parcheggi di interscambio esistenti (Stura, Caio Mario, Sofia, Venchi Unica) sono a due
passi dalle fermate più critiche per chi arriva in auto dalla cintura? Quali fermate critiche
restano senza parcheggio?

Non si propongono parcheggi nuovi: solo copertura di quelli esistenti.

## Regole decise

| Regola | Valore | Chi l'ha decisa |
|---|---|---|
| Punteggio di criticità | media dei 3 percentili: corridoio (script 24), corse/ora di punta (GTFS), pendolari Torino↔cintura (IMQ) | già concordato |
| Fermata critica | 10% più alto del punteggio (percentile 90) | già concordato |
| Centro escluso | le fermate del centro non contano (un interscambio serve all'ingresso in città, non in centro) | Leo, 14/10 (scelta A) |
| Copertura | fermata coperta se un parcheggio è **entro 200 m a piedi**. Oltre, non ha senso lasciare l'auto lì | Leo, 14/10 |

Valori predefiniti (cambiabili da riga di comando):
- **Centro** = zona IMQ `Q001 Torino-Centro`. Opzione `--escludi-zone Q001` (si possono aggiungerne altre).
- **200 m a piedi** = distanza in linea d'aria fra fermata e ingresso del parcheggio (coordinate
  del dataset comunale). Opzione `--raggio-copertura-m 200`. A 200 m la differenza fra linea
  d'aria e percorso a piedi è piccola; lo dichiariamo come limite.

Effetto atteso, da sapere prima: con soli 4 parcheggi e 200 m, le fermate coperte saranno
pochissime (solo quelle attaccate ai 4 parcheggi). È normale: il risultato utile è la
**classifica delle fermate critiche scoperte**.

## Passi (uno alla volta, ognuno chiuso prima del successivo)

### Passo 0 — Elenco dei parcheggi (aggiunto 14/10)
1. Fonte principale: `get_pk` di 5T (41 parcheggi in struttura con lat/lon, posti totali e
   posti liberi ogni 5', raccolti su leopi da metà ottobre). Copre anche **Fermi** (Collegno),
   che il file del Comune non ha.
2. Il file del Comune (`parcheggi_accesso_controllato`) serve solo per sapere quali sono
   ufficialmente di interscambio.
3. Etichette: "interscambio ufficiale" e "garage in struttura" tenuti separati.
4. Quando ci sono alcune settimane di raccolta: quanto si riempie ogni parcheggio per ora e
   giorno [MISURATO] — da aggiungere al rapporto.

### Passo 1 — Sistemare "Strada Torino" e simili (script 24)
1. Problema: lo script 24 unisce le vie per nome, quindi strade diverse in comuni diversi con lo
   stesso nome diventano un corridoio solo ("Strada Torino" = 100 km, punteggio 5).
2. Modifica (fatta): il corridoio diventa **stesso nome + tratti collegati o vicini (~100-200 m)**,
   così carreggiate e controviali restano insieme e le vie omonime lontane si separano; il comune
   è aggiunto al nome solo come etichetta.
3. Rilanciare `python scripts\24_importanza_vie.py`.
4. Controllo in `docs/RAPPORTO_IMPORTANZA_VIE.txt`:
   - nessun corridoio cittadino o di cintura sopra ~30 km, a parte autostrade e tangenziali;
   - "Strada Torino" spezzata per comune, ogni pezzo con punteggio proprio.

### Passo 2 — Escludere il centro (script 25)
1. Aggiungere l'opzione `--escludi-zone` (default `Q001`).
2. Le fermate di quelle zone restano nel calcolo dei percentili ma non possono essere "critiche".
   (Default dichiarato: così i punteggi delle altre fermate non cambiano per l'esclusione.)
3. Controllo: nessuna fermata critica con `zona_imq = Q001` nel rapporto.

### Passo 3 — Nuova regola di copertura (script 25)
1. Sostituire "stesso corridoio entro 3 km" con "parcheggio entro 200 m in linea d'aria".
2. Opzione `--raggio-copertura-m` (default 200). Togliere `--soglia-copertura-km`.
3. L'assegnazione dei parcheggi a un corridoio non serve più per la copertura: resta solo come
   informazione nel rapporto.
4. Nel rapporto, per ogni parcheggio: quante fermate (critiche e non) ha entro 200 m.

### Passo 4 — Giro di prova e verifica
1. `python scripts\25_risultato6_interscambio.py --prova`
2. Controlli indipendenti (non fidarsi del rapporto da solo):
   - ricalcolare a mano, per ognuno dei 4 parcheggi, le fermate entro 200 m e confrontarle col rapporto;
   - la fermata `1103 CAIO MARIO` deve risultare vicina al parcheggio Caio Mario (o spiegare perché no);
   - nessuna fermata critica in Q001;
   - numeri sensati: critiche ≈ 10% delle fermate analizzate, coperte ≤ critiche, nessun valore negativo.
3. Mostrare a Leo il riepilogo: critiche, coperte, scoperte, prime 10 scoperte più gravi.
4. **Il giro completo parte solo con il via libera di Leo.**

### Passo 5 — Giro completo
1. `python scripts\25_risultato6_interscambio.py`
2. Stessi controlli del passo 4 su tutte le fermate.
3. Riepilogo a Leo con i 3 numeri:
   - quante fermate critiche (fuori dal centro);
   - quante coperte da un parcheggio entro 200 m;
   - le scoperte più gravi (nome, zona, punteggio).

### Passo 6 — Presentazione
1. Mappa: nuovo livello con i 4 parcheggi, cerchio di 200 m attorno, fermate critiche colorate
   coperte/scoperte. Verifica nel browser come da standard (sez. 9 della memoria).
2. Pagina in `simulazione.html` con mappa, numeri e limiti.
3. Aggiornare `MEMORIA_PROGETTO.md`.

## Limiti da dichiarare
- Occupazione dei parcheggi: solo dalla data di avvio della raccolta 5T (metà ottobre 2026); Fermi e Unione Sovietica a volte non trasmettono.
- Pendolari stimati per zona IMQ, non per fermata [STIMATO].
- Importanza delle vie da OSM + 5T + elenco a mano; in cintura OSM è meno completo.
- 200 m in linea d'aria, non percorso a piedi reale.
- Corse/ora da orario programmato [PROGRAMMATO], non misurate.

---

# Versione 2 — proposta discussa con Leo il 18/10/2026 (da approvare passo per passo)

## Decisioni di Leo (18/10)

- **Si resta sulle fermate** come unità (niente "porte d'ingresso" al loro posto), ma si dichiara che le
  fermate vicine (due lati della via, più paline nello stesso punto) sono **un solo luogo**.
- Le fermate critiche di oggi vicino ad autostrade e statali (Paradiso, Massaua, Lingotto, Moncalieri…) sono
  sensate: lì, se ci sono tanti mezzi, si dovrebbe poter lasciare l'auto.
- **Niente interfaccia dinamica per ora**: né nella mappa né nella scheda. Se servirà, al massimo **3
  scenari** fissi nella scheda, senza che la scheda ripeta la mappa.
- **Anteprima del riempimento** dei parcheggi dopo il fetch del 19/10.
- **ISTAT 2011**: solo per ciò che cambia poco nel tempo e per completare dati e calcoli esistenti (sotto, da
  confermare cosa vuol dire).
- **Tutti i parcheggi**, ognuno con la sua precisazione sul tipo e sui dati disponibili.

## A. Nuova misura: quanto un parcheggio fa davvero da interscambio

Per ogni parcheggio, tre domande:
1. **Posizione** — è a pochi passi da un nodo di trasporto forte (metro, capolinea, stazione, fermata con
   molte corse nelle ore dei pendolari)? È su una strada d'ingresso, tra la porta della città e il centro?
2. **Uso** (solo dove c'è il riempimento 5T) — la "firma" oraria:
   - *pendolare*: si riempie al mattino feriale (7-9), resta pieno in orario di lavoro, si svuota la sera,
     vuoto di notte e nel weekend;
   - *residenziale*: più pieno di notte che di giorno (es. Sofia: 55% di notte, 32% di giorno);
   - *destinazione*: picco nel pomeriggio o il sabato (centro, ospedali, centri commerciali);
   - *dato bloccato*: variazione giornaliera quasi nulla (es. Venchi Unica fermo al 51%);
   - *nessun dato*: Fermi, Racconigi, Unione Sovietica, V Padiglione non trasmettono mai i posti liberi.
3. **Condizioni** — capienza, a pagamento o gratis (tag OSM `fee`).

Classi finali: **interscambio di fatto** (posizione buona + firma pendolare) · **interscambio solo sulla
carta** (segnato dal Comune ma usato in altro modo, o vuoto) · **potenziale** (posizione buona, nessun dato
d'uso) · **non interscambio**. Si applica a tutti i 41 parcheggi 5T, non solo ai 5 ufficiali (un garage come
Bolzano, vicino a Porta Susa, potrebbe fare da interscambio di fatto).

Primi indizi (3 feriali, 14-16/10): Stura pieno (~90% di giorno, 80% di notte); Caio Mario quasi vuoto (1-2%
sempre: vuoto davvero o contatore guasto?); Sofia residenziale; Venchi Unica bloccato; Porta Susa FS con un
ciclo pulito (36% di notte, 88% di giorno). A Fermi, entro 500 m, OSM ha ~85.000 m² di parcheggi aperti quasi
tutti **gratuiti** (uno sotterraneo da ~30.000 m² a 180 m), mentre il park&ride ufficiale è a pagamento: conferma
l'idea di Leo che i parcheggi gratuiti vicino ai capolinea siano quelli davvero usati (e non misurati). Lo stesso
a Caio Mario: ufficiale a pagamento e vuoto, uno gratuito da ~5.000 m² a 170 m.

## B. Parcheggi: tutti, con la loro precisazione

| Tipo | Quanti | Dati | Precisazione |
|---|---|---|---|
| Interscambio ufficiali (Comune + Fermi) | 5 | posti; riempimento tranne Fermi | |
| Garage 5T | 36 | posti e riempimento (3 senza dati) | |
| OSM park&ride | 25 | posti solo per alcuni | molti senza nome, in cintura vicino a stazioni |
| OSM a raso / multipiano / sotterranei | ~2.500 | posti dichiarati su pochi | posti stimati dalla superficie (~25 m² a posto, compresi i corselli) [STIMATO] |
| OSM lungo strada | ~1.000 | quasi mai i posti | esclusi dal conteggio dei posti, solo informazione |
| Privati / solo clienti | ~360 + clienti | — | esclusi (clienti: segnalati a parte, es. centri commerciali) |

## C. Fermate critiche: cosa cambia

- **Luoghi**: le fermate entro 40 m sono un solo luogo (stesso criterio della Fase 5 del traffico). Oggi:
  611 fermate critiche = **469 luoghi** (379 se si unisce entro 80 m); coperte 17 fermate = 13 luoghi.
- **(a) Importanza della via** — oggi (script 24) è per *corridoio con lo stesso nome*: punteggio 1-5 = il più
  alto fra classe OSM, elenco a mano di Leo (minimo 4) e sensore 5T con flusso alto (minimo 3). Proposta: dopo
  il lavoro sulle strade, usare gli **assi della Fase 5** (un corso che cambia nome resta uno solo) con la loro
  classe, un segno "**asse d'ingresso**" (attraversa il confine di Torino) e il traffico stimato **solo come
  ordine** (la stima è debole).
- **(b) Corse** — oggi: corse nell'ora di punta alla fermata. Proposta: **media nelle ore dei pendolari**
  (6-10 e 16-20, feriale) come misura principale; punta e intera giornata come prove di sensibilità.
- **(c) Pendolari** — invariato (somma delle due direzioni, tutti i mezzi, giornata intera, valore uguale per
  tutta la zona IMQ), dichiarato così. Variante più precisa al passo D2.
- **Distanza**: 200 m restano la base; nel rapporto anche 100 e 400 m. Più avanti: distanza a piedi sulle
  strade invece che in linea d'aria.

## D. Dati non ancora usati, a passi

1. **Anteprima riempimento** (dopo il fetch del 19/10): firma oraria e classi del punto A.
2. **IMQ nelle ore critiche**: i microdati (`data/processed/imq/spostamenti.csv`) hanno zona e ora di
   partenza, zona di arrivo e mezzi in sequenza. Uso: (c) diventa "auto che entrano a Torino al mattino
   (6-10) dalla cintura", per zona. Quanto apporta lo si misura: quanti luoghi cambiano classe rispetto a oggi.
   Bonus: si vede chi **fa già** auto → mezzo pubblico: ~24.500 spostamenti al giorno (299 interviste), 63% verso
   il treno, ~4.000 verso la metro; la zona del cambio manca nel 60% dei casi e per singola zona le interviste
   sono poche (Collegno 19) → solo numeri d'insieme [DATI SCARSI].
3. **ZTL** (centrale lun-ven 7:30-10:30): pesare di più chi va verso il centro nelle ore della ZTL, perché deve
   lasciare l'auto prima. Si fa insieme al passo 2.
4. **Velocità 5T**: per evitare l'effetto di limiti e semafori, non la velocità assoluta ma il **calo** di
   ciascun sensore fra notte e punta (stesso punto, stessi limiti). Solo dove c'è un sensore (pochi, sugli
   ingressi).
5. **ISTAT 2011 per sezione** (mezzo e ora): solo per le cose che cambiano poco (proposta da confermare):
   *quota di chi va in auto* per sezione e *distribuzione degli orari di partenza*, usate come proporzioni per
   ripartire i totali IMQ 2022 dalle zone alle sezioni; mai numeri assoluti del 2011.
6. **Più avanti, mobilità d'insieme**: bici e bike sharing, car sharing, taxi, stazioni dei treni (da OSM:
   il GTFS GTT non ha i treni).

## Decisioni successive (18/10)

- Definizione ISTAT 2011 del punto D5: **confermata** da Leo.
- **I segnali della versione 1 restano** (importanza della via, corse, pendolari): i nuovi si aggiungono o, se
  sono la loro versione migliorata, li sostituiscono; si confrontano in 3 scenari e decide Leo.
- Piano meccanico per un agente: **`docs/archivio/r6/PIANO_RISULTATO6_V2.md`** (script 68, 69, 71-76).
- Ancora aperto: le soglie della firma oraria si fissano dopo aver visto l'anteprima.

## Giro dell'agente del 19/10 (piano `PIANO_RISULTATO6_V2.md`) — esito ricontrollato da Claude

Esito: `docs/archivio/r6/ESITO_RISULTATO6_V2.md`, rapporti `docs/RAPPORTO_R6V2_*.txt` e `docs/RAPPORTO_RISULTATO6_V2.txt`, dati in
`data/processed/risultato6_v2/`, script 68, 69, 71-76. Tutti i passi OK.

**Numeri confermati da Claude** (ricalcolati a parte): v1 rifatta fermata per fermata = 611 / 17 / 594; scenari S1 438,
S2 436, S3 438 luoghi critici (S1∩S2 370); c2 = 95.297 spostamenti in auto in entrata al mattino (1.139 interviste);
auto → mezzo pubblico ~24.500/giorno (299 interviste). Luoghi: 5.087 (le 611 fermate critiche v1 = 462 luoghi).
Parcheggi censiti 5.205 (5T 40, Comune 39, OSM 5.176). Anteprima riempimento: solo 2 feriali validi (15-16/10).

**Problemi trovati da Claude (da correggere prima di scegliere lo scenario):**
1. **a2 e "asse d'ingresso" prendono il tratto più vicino, anche se è una stradina di servizio** (regola del piano,
   errore di Claude). Esempio: la fermata Genova N.212 (Moncalieri) prende un tratto di servizio a 2 m (punteggio 1)
   invece di Strada Genova a 6 m (punteggio 4). Per lo stesso motivo **nessun parcheggio risulta su un asse
   d'ingresso**, neanche Fermi e Venchi Unica su Corso Francia. In più alcune tratte importanti hanno punteggio 1
   (Via Torino a Venaria, secondaria): da controllare il punteggio delle tratte della Fase 5. a2 è il segnale che
   pesa di più in S2 (toglierlo cambia 148 luoghi), quindi va sistemato prima di confrontare gli scenari.
   Correzione proposta: entro ~30-50 m prendere il tratto di classe più alta, escludendo service/residential.
2. **"Interscambio di fatto" troppo largo**: la firma "pendolare" non distingue chi lascia l'auto per prendere un
   mezzo da chi la lascia vicino al posto di lavoro (risultano interscambio di fatto Molinette, Palagiustizia,
   Nizza, CTO), e "posizione buona" (nodo forte entro 400 m, fuori Q001) vale per quasi tutta la città (346 nodi
   forti). Serve una condizione in più (es. nodo metro/treno/capolinea, oppure fuori dalla zona semicentrale, oppure
   su un asse d'ingresso una volta corretto il punto 1).
3. **Fermate di tutto il Piemonte**: luoghi e percentili includono le fermate GTT extraurbane fuori dalla Città
   metropolitana (Mondovì, Fossano…), come già la v1. Decidere se limitare l'universo (es. Torino + cintura).
4. **La v1 sbagliava "l'ora di punta"**: b1 prendeva l'ora con più corse anche di notte (es. Pozzo Strada: 9 corse
   "in punta" ma solo corse notturne; b2 = 0 è giusto). Argomento per sostituire b1 con b2.
Altri limiti: soglie delle firme provvisorie (Venchi Unica ampiezza 0,055 → "misto" invece di "bloccato"); la ZTL
centrale copre solo la zona Q001 (c2_ztl cambia 20 luoghi); il calo di velocità esiste solo vicino a 96 luoghi (pesa
poco); la quota auto ISTAT 2011 è più bassa di quella IMQ del mattino (universi diversi), usata per 54 zone.
