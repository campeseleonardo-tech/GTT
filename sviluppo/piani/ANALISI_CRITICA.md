# Analisi critica del progetto (revisore esterno, 23/10/2026)

Fatta su `origin/prova` al commit `f2439ab` (piani L2 e L3), in sola lettura, nel cloud: c'è `data/processed/` (in git), non lo storico
né `data/raw`. Ogni affermazione ha la sua prova (file e riga, numero letto da un JSON, comando). I calcoli rifatti a mano sono in Python
sui JSON di `data/processed/`; le schermate sono state fatte con Chromium senza schermo a 1440×900, chiaro e scuro (0 errori JavaScript su
20 pagine aperte). Quello che L2 e L3 faranno già non è riproposto: lo critico solo dove vedo un problema.

Due parole che uso spesso:
- **fattore di punta**: per quanto si moltiplica il tempo in auto a strada libera per avere il tempo vero all'ora di punta (1,2 dai sensori, 2,1 da Google).
- **correlazione parziale**: quanto due cose vanno insieme *a parità* di una terza (qui: la distanza dal centro).

## Riassunto in 10 righe

**I 5 problemi più gravi**
1. Il fattore di Google (2,1) è misurato su 6 percorsi **in uscita** da Piazza Castello alle 8 (contromano rispetto ai pendolari); l'unico percorso **in entrata** misurato dà 3,6. Con 3,6 tutti e 12 i punti del R6 diventano «il bus conviene»: la conclusione della scheda 3 si ribalta (§1.1).
2. La «forbice» 2,1-1,2 non contiene la verità: 2,1 è una mediana, quindi Google sta fuori dalla forbice in 5 percorsi su 8. La frase «la verità sta nella forbice» (`docs/R8_traffico.md:79`) è falsa (§1.2).
3. Le fasce della scheda 4 sono dette «fissate prima dei numeri», ma il metodo è cambiato 4 volte in un giorno dopo aver visto i risultati (§1.3).
4. Un estraneo non può rifare i calcoli: mancano `r5py` e `geopandas` in `requirements.txt` e Java è cercato in una cartella che non è né in git né nella Release (§6.1).
5. La raccolta sul Pi ha tre punti fragili non sorvegliati: GTFS mai archiviato (lo script 27 ne usa uno fisso), avvisi di spazio che sul Pi finiscono solo nel log, copia sul PC che sovrascrive senza controllare che lo storico sia cresciuto (§5).

**Le 5 migliorie più utili**
1. Un giro manuale di tempi Google **in entrata** (12 punti + 6 percorsi, 4 ore): ripara R6, R8 e L3 insieme (giro G1).
2. Scheda 5 più forte e più onesta: «a parità di distanza dal centro le case costano meno dove c'è fragilità (−0,68), non dove mancano servizi (0,21)» e «il doppio svantaggio è 1,7 volte quello che darebbe il caso» (§1.4-1.5).
3. Risultati nuovi già calcolati: velocità vera dei bus ora per ora (12,7 km/h alle 8), la linea 17 (un passaggio su 5 oltre 10 minuti), «quanto ci si può fidare dei dati aperti» come sesto risultato (§2).
4. In home e nelle schede, una riga di limite visibile accanto al numero grande e il periodo dei dati al posto di «aggiornato al 23/10» (§3).
5. Ripulire la vetrina del repository per chi seleziona: commit con messaggi veri, `sviluppo/` meno in vista, una frase onesta sull'uso di Claude Code (§7).

---

## 1. Solidità dei risultati

### 1.1 Il fattore di Google è misurato nella direzione sbagliata per il R6
- **Cosa non va.** I 6 percorsi che danno il fattore 2,1 partono tutti **da** Piazza Castello verso la cintura alle 8 (`docs/R8_traffico.md`, tabella «Noi contro Google Maps»): è la direzione scarica. Il R6 invece guarda solo viaggi **verso** Piazza Castello. L'unico percorso in entrata misurato, «Corso Racconigi → Piazza Castello», ha auto Google 29 minuti contro 13-18 nostri.
- **Prova** (rifatto a mano: flusso libero = (tempo col fattore 1,2 − 5) / 1,2; fattore Google = (Google − 5) / flusso libero):

  | Percorso | Fattore Google |
  |---|---|
  | Castello → Collegno | 1,05 |
  | Castello → Rivoli | 1,80 |
  | Castello → Venaria | 2,08 |
  | Castello → Orbassano | 2,13 |
  | Castello → Settimo | 2,33 |
  | Castello → Moncalieri | 2,49 |
  | **Racconigi → Castello (in entrata, controllo)** | **3,60** |

  (Calcolo approssimato: parte dai minuti interi della tabella.) Da `data/processed/r6_bus_contro_auto.json` (campi `libero_min`, `tp_min`): per essere «il bus conviene» (rapporto ≤ 1,5) i 12 punti chiedono un fattore fra 2,23 (Ferrara) e 2,93 (Zara). Con 3,6 il rapporto va da 0,71 (Metro Massaua) a 1,28 (Zara): **12 su 12 sotto 1,5**, contro «0 conviene, 1 dipende, 11 no» di oggi. Anche i minuti di pareggio crollano (Santa Rita: 36 − 7,2 × 3,6 = 10 minuti invece di 21-27), vicini ai 7,8 minuti della letteratura citata in `docs/R6_parcheggi.md`.
- **Gravità: alta** (titolo e messaggio della scheda 3, e tutta la «gara»). **Lavoro: piccolo** (tempi presi a mano) + piccolo (rilancio 93, 94).
- **Proposta.** Non correggere a occhio: un solo percorso non basta. Raccogliere i tempi Google in entrata dai 12 punti e dai 5 interscambi (giro G1, regole fissate prima), poi decidere se il fattore va separato per direzione. Fino ad allora, nella scheda 3: «il fattore di punta è stato misurato in uscita dal centro; in entrata l'auto può essere più lenta».

### 1.2 La «forbice» non è un intervallo
- **Cosa non va.** Il fattore basso 2,1 è la **mediana** dei 6 percorsi: per costruzione in metà dei percorsi Google è più lento della nostra «auto lenta». La frase «La verità sta nella forbice» (`docs/R8_traffico.md:79`) e la scheda 4 («i tempi in auto sono stimati fra il rallentamento dei sensori e quello di Google») fanno credere a un minimo-massimo.
- **Prova.** Dalla tabella di `docs/R8_traffico.md`: Google è sopra il nostro tempo lento a Settimo (38 contro 35), Moncalieri (34/29), Orbassano (44/43), Racconigi (29/18); sotto il tempo veloce a Collegno (19/21). Fuori in **5 su 8**.
- **Gravità: alta** (numero grande della scheda 4: «2-3 volte»). **Lavoro: piccolo.**
- **Proposta.** Chiamarli «due stime» e non «limiti»; scrivere che il rapporto vero può stare anche fuori. Con i dati del giro G1 usare per il limite basso un quantile (es. il 75° dei fattori Google) invece della mediana: allora è davvero un limite.

### 1.3 «Fasce fissate prima dei numeri»: non del tutto vero
- **Cosa non va.** `scripts/schede/r8.py:247` e `:262` scrivono «fasce fisse e decise prima di vedere i numeri». La storia di git dello script 93 dice che il 21/10 il metodo è cambiato 4 volte dopo aver visto i risultati.
- **Prova.** `git log -- scripts/93_tp_contro_auto.py`: `9f1015e` (prima versione), `f32c661` «soglie 2,5 e 3,5 (quelle di prima, 1,5 e 2, restano nel JSON)», `543bc13` «rapporto mediano e fasce fisse al posto delle soglie», `de8b05a` (fattore dei sensori), `ec584a3` (forbice). Il JSON conserva le versioni vecchie (`tp_contro_auto.json`, `precedenti`: con soglie 1,5/2 «non conviene» il 98,6%).
  Le fasce attuali possono essere sensate, ma sono state scelte dopo.
- **Gravità: alta** per la credibilità (è proprio l'errore che il progetto dice di evitare, `MEMORIA_PROGETTO.md` riga 69). **Lavoro: piccolo.**
- **Proposta.** Togliere «decise prima di vedere i numeri» dalla scheda 4; nel documento R8 una riga: «metodo cambiato 4 volte il 21/10; le fasce sono state scelte dopo le prime prove». Mostrare il risultato con almeno due fasce diverse (sensibilità) invece di una sola.

### 1.4 Scheda 5: «Si paga per i servizi?» è quasi tutto «si paga per il centro»
- **Cosa non va.** Il punto chiave dice «Prezzo e servizi vanno insieme: Spearman 0,61». Ma sia il prezzo sia i servizi calano allontanandosi dal centro.
- **Prova** (rifatto su `case_fragilita_servizi.json`, campo `zone`, 46 zone): prezzo-servizi 0,614 (uguale al JSON); prezzo-distanza −0,69; servizi-distanza −0,74. **A parità di distanza** (correlazione parziale sui ranghi) prezzo-servizi = **0,21, p = 0,16** (non distinguibile da zero). Invece prezzo-fragilità a parità di distanza = **−0,68** (p < 0,001) e fragilità-servizi a parità di distanza = **−0,48** (p < 0,001).
- **Gravità: media.** **Lavoro: piccolo** (tre righe nello script 95, un punto chiave nella scheda).
- **Proposta.** Cambiare la domanda in «Dove le case costano poco, ci sono anche meno servizi e più fragilità?» e il punto: «A parità di distanza dal centro, le case costano meno dove la fragilità è alta; i servizi contano poco». Il legame fragilità-servizi invece **regge**: è una prova in più per il titolo della scheda 5 e va scritta.

### 1.5 Scheda 5: «1 su 10» è in parte deciso dalle soglie
- **Cosa non va.** «Fragilità alta» e «servizi bassi» sono il 20% più alto e più basso delle sezioni: una parte di torinesi in doppio svantaggio esce anche per puro caso. Il titolo dice «1 su 10» senza dire quanto è sopra il caso.
- **Prova** (`case_fragilita_servizi.json`, `e2_doppio_svantaggio.sezioni.classi`): residenti con fragilità alta 222.004 su 839.657 (26,4%), con servizi bassi 180.198 (21,5%). Se le due cose fossero indipendenti: 26,4% × 21,5% = 5,7%, circa 47.600 persone. Osservati **79.598 = 1,67 volte**. Per sezioni: attese 140, osservate 216 = **1,54 volte**.
- **Gravità: media.** **Lavoro: piccolo.**
- **Proposta.** Un punto chiave: «Quasi il doppio di quanto darebbe il caso (1,7 volte)». È la frase che rende il risultato davvero un risultato. Anche il titolo di L2 («Circa 1 torinese su 10 vive in una zona con più difficoltà sociali e pochi servizi») va bene solo se sotto c'è questa riga: «pochi» è relativo (il 20% più basso di Torino), non assoluto.

### 1.6 Scheda 4: le «3 coppie peggiori» poggiano su poche interviste
- **Cosa non va.** Il punto chiave nomina tre coppie di zone. Lo script 14 stesso considera «affidabile» una cella dell'indagine solo con almeno 30 interviste (`scripts/14_prepara_imq.py:47`, `SOGLIA_N = 30`).
- **Prova** (`imq_od.json`, modo `pri`, giorno intero): Madonna del Pilone → Vanchiglia **15 interviste**, Parella → San Paolo 27, Madonna del Pilone → Centro 28: tutte sotto 30 e tutte segnate `false`. Fra le 6 del mattino e le 10 sono ancora meno. Su 6.818 celle, 5.920 hanno meno di 10 interviste.
- **Gravità: media.** **Lavoro: piccolo.**
- **Proposta.** Nella classifica delle coppie (punto chiave e grafico «15 coppie») tenere solo celle con almeno 30 interviste, oppure togliere i nomi e dire «le coppie con molte auto e mezzi lenti sono soprattutto fra quartieri vicini separati dal Po».

### 1.7 Scheda 4: il numero copre meno della metà delle auto
- **Prova** (`tp_contro_auto.json`): auto del mattino delle zone incluse 465.534; nel numero 220.307 (Torino-Torino e Torino-cintura) = **47%**; dentro la stessa zona 164.203 (35%) escluse; 19.216 senza collegamento.
- **Gravità: media.** **Lavoro: piccolo.** **Proposta.** Nel testo del numero: «sul 47% delle auto del mattino: i viaggi dentro un quartiere e fra comuni della cintura non sono contati».

### 1.8 Scheda 3: i numeri dipendono da 64 interviste (e il titolo di L2 esagera)
- **Prova.** `docs/rapporti/RAPPORTO_R6_PARCHEGGI.txt:151`: con la quota di chi lascia l'auto dimezzata o raddoppiata (5,8% viene da 64 interviste) le fermate senza posti bastanti vanno da 135 a 212 su 274 (da 49% a 77%). Le fermate **senza nessun** parcheggio adatto restano 68 (25%).
- **Critica a L2.** Il titolo nuovo «2 fermate importanti su 3 non hanno dove lasciare l'auto» è letteralmente vero solo per 68 su 274 (1 su 4); le altre 111 hanno posti, ma meno di una stima.
- **Gravità: media. Lavoro: piccolo.** **Proposta.** «2 fermate importanti su 3 non hanno abbastanza posti per lasciare l'auto (stima)»; punto chiave: «1 su 4 non ne ha nessuno». Questo numero non dipende dalle 64 interviste: è il più solido.

### 1.9 Scheda 1: il titolo racconta il dato meno interessante
- **Prova** (`risultato1_vuoti.json`, `v3`): 574.422 / 841.591 = 68,25% a 5 minuti, 834.963 / 841.591 = 99,21% a 15 (uguali alla scheda). «Servizio presente» = almeno **una** destinazione del gruppo, e «negozi» = tutte le attività commerciali: a 1,2 km a piedi in una città densa è quasi garantito. Il dato vivo è a 5 minuti: 172.371 residenti senza salute, 138.187 senza scuola.
- **Critica a L2.** «Torino, città dei 15 minuti» prende uno slogan (Moreno, Parigi) che significa più di «un servizio per tipo»: sembra un giudizio sulla città che la misura non regge.
- **Gravità: bassa-media. Lavoro: piccolo.** **Proposta.** Titolo: «A 15 minuti a piedi quasi tutti hanno i servizi essenziali; a 5 minuti solo 2 su 3». Punto chiave nuovo: «A 5 minuti 1 torinese su 5 non ha un servizio sanitario».

### 1.10 Scheda 1: «strada molto trafficata» è relativo e i denominatori non coincidono
- **Prova.** `docs/rapporti/RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt:7`: 11.720 veicoli/giorno = «terzo più alto» delle strade grandi del modello (±38%). Esposizione: base 841.980 residenti (`esposizione_traffico.json`), copertura: 841.591 (`risultato1_vuoti.json`): due definizioni di «zone abitate» (le 389 «da verificare»).
- **Gravità: bassa. Lavoro: piccolo.** **Proposta.** Nel criterio: «il terzo più trafficato delle strade grandi»; stessa base nei due numeri.

### 1.11 Puntualità: il 38% di passaggi in anticipo non è spiegato
- **Prova** (`risultato4_regolarita.json`, `citta.0.anticipo` = 37,9; per linea feriale con almeno 2.000 passaggi: 27 → 62,5%, 45 → 61,7%, 13 → 59,8%, 10 → 58,6%; mediana delle 49 linee 34%). Anche il feed dà 39,9% (`confronto_feed`), quindi non è solo il GPS.
- **Gravità: bassa-media** (può essere un risultato o un difetto di misura). **Lavoro: piccolo.** **Proposta.** Prima di pubblicarlo come risultato (§2.3), controllare l'anticipo alla prima fermata e sulle linee a orario fisso; se è vero, è una notizia: un bus in anticipo su una linea ogni 20 minuti fa perdere la corsa.

### 1.12 Numeri che cambiano a ogni rilancio
- **Prova.** `sviluppo/piani/ESITO_P7.md`: rilanciando con lo storico del 23/10, R4 oltre 5' 14,1% → 15,6%; R8 errore ±38% → ±28%; esposti 190.255 → 205.034. Gli script 26, 27, 33, 70, 71, 88 leggono lo storico vivo senza una data di fine.
- **Gravità: media** (chi rifà i conti non ritrova i numeri pubblicati). **Lavoro: piccolo.** **Proposta.** Una costante `PERIODO = ("2026-10-10", "2026-10-20")` in `comuni.py` letta dagli script dei risultati, scritta nei JSON e in pagina; si cambia a mano quando si decide di aggiornare (P8).

### 1.13 Cose minori
- Fattore dei sensori: la mediana vera è 1,159 (`tp_contro_auto.json`, `parametri.fattore_sensori.mediana`), usato 1,2. Piccolo, ma in L3 pesa (§1.14).
- Scheda 5, metro +115 €/m²: media di 3 differenze fatte su gruppi di 2, 3 e 6 zone con metro (`e3_valore_metro.fasce`), nessun intervallo. Gravità bassa; proposta: togliere il grafico o lasciarlo solo nella parte chiusa.
- `docs/METODO.md` (sezione «Colori») dice ancora verde → rosso e blu → arancione; lo stile scelto il 22/10 è verde acqua → granata.

### 1.14 Critiche a L3 (bus contro auto a 4 ore)
- La formula del fattore Google alle altre ore, `1 + 1,1 × (f(h) − 1) / (f(8) − 1)`, divide per un numero piccolo: f(8) − 1 vale 0,16 (mediana vera) o 0,2 (arrotondata). Un errore di 0,03 nel fattore dei sensori a un'ora diventa ±0,2 nel fattore Google. E cambia del 25% secondo se si usa 1,159 o 1,2.
- Il controllo bloccante «fattore alle 8 = 1,2 ± 0,1» passa anche se il calcolo è sbagliato di 0,09.
- Il fattore Google alle altre ore non è una misura indipendente: è il fattore dei sensori riscalato. Due serie che si muovono insieme per costruzione non sono una forbice.
- **Proposta.** Fare prima G1 (tempi Google veri a 4 ore, nelle due direzioni) e usare quelli; la regola del titolo di L3 (±0,3) resta valida.

---

## 2. Risultati che mancano ma sono a portata

| # | Domanda | Dati già pronti | Cosa manca | Lavoro | Perché interessa |
|---|---|---|---|---|---|
| 2.1 | **A che velocità va davvero un bus a Torino, ora per ora?** | `vel` dentro `mappa_torino.html` (dal GPS, 137 linee, 15 feriali). Calcolo veloce (media pesata sui conteggi, da rifare nello script): 12,7 km/h alle 8, 12,5 alle 17, 16-20 di notte | uno script che lo scriva in un JSON, una scheda o un punto chiave; spiegare come è calcolata la velocità | piccolo | un numero che tutti capiscono («poco più di una bici») e, bonus, un terzo fattore di punta **misurato** (20 / 12,7 ≈ 1,5) per controllare la forbice 1,2-2,1 |
| 2.2 | **La linea più in ritardo** | `risultato4_regolarita.json`: linea 17, 28.233 passaggi feriali, 38,1% oltre 5', **20,1% oltre 10'**; seguono 6 e 19; ritardo a fine corsa già calcolato | un grafico «ritardo lungo la corsa» della 17 (fermata per fermata) | piccolo | un caso concreto, riconoscibile da chi vive a Torino: «sulla 17, un passaggio su 5 arriva con più di 10 minuti di ritardo» |
| 2.3 | **Bus in anticipo: quante corse si perdono?** | anticipo per linea e fascia (`risultato4_regolarita.json`) | classe delle linee per frequenza (da GTFS, già letta dal 70) e controllo §1.11 | piccolo-medio | ribalta l'idea che il problema sia solo il ritardo |
| 2.4 | **Quanto ci si può fidare dei dati aperti?** (sesto risultato) | feed contro GPS 5,4% / 14,1% (2,6 volte), feed fermo il 18/10, mezzo con l'orologio 3 anni avanti, contatore Caio Mario fermo, 17 sensori 5T esclusi su 112 (`RAPPORTO_SENSORI_ESCLUSI.txt`), copertura GPS 78,3% | metterlo in una scheda con 3-4 numeri | piccolo | per un portfolio di analisi dati è il risultato più vendibile: mostra che si sa controllare una fonte. Oggi è solo un paragrafo di `progetto.html` |
| 2.5 | **Fragilità e prezzi a parità di distanza** | `case_fragilita_servizi.json` (§1.4) | tre righe nello script 95 | piccolo | rende la scheda 5 più solida e dice una cosa vera e nuova |
| 2.6 | **Doppio svantaggio anche sui mezzi?** Le 5 zone hanno anche linee più in ritardo e meno accessibilità coi mezzi in 45'? | `accessibilita.json` (TP 45'), `vulnerabilita.json`, ritardi per linea, `orari_fermate.js` | abbinare per posizione fermate e zone (regola fissa: fermate entro 400 m dal centro delle sezioni) | medio | unisce le due anime del progetto (sociale e trasporti) |
| 2.7 | **Per circoscrizione** (R1, R5, ritardi) | tutte le sezioni con coordinate | confini delle 8 circoscrizioni (aperTO, CC BY) e unione per posizione; oggi saltato (`risultato1_vuoti.json`, `nota_circoscrizioni`) | piccolo-medio | chi legge da Torino pensa per circoscrizione; un'ottima tabella per un post |
| 2.8 | **Tornare a casa di notte** (R2 ripreso) | scenari `gtt_gtfs_notte15.zip` / `notte30.zip` già costruiti dallo script 28 | r5py da 3-4 luoghi della notte (Vanchiglia, San Salvario, Valentino) verso ogni zona, con e senza metro | medio | la domanda giusta per il R2; risultato facile da raccontare |
| 2.9 | **Quando si riempiono i parcheggi** | riassunti mensili del riempimento (`data/storico_riassunti/`) | grafico per ora dei garage 5T | piccolo | ma pochi garage: solo come grafico secondario della scheda 3 |
| 2.10 | **Cambio dell'ora legale (25/10)** | raccolta continua | due settimane di dati prima e dopo; regole fissate prima | medio | esperimento naturale; utile solo se esce qualcosa: tenerlo come idea |

Non verificato da me: se nei giorni raccolti c'è uno sciopero GTT (sarebbe un altro esperimento naturale sul traffico).

---

## 3. Grafica e racconto

Schermate fatte: home, risultati, le 5 schede aperte (con scorrimento dentro la finestra), progetto, 404, `r/1.html` (porta subito a `risultati.html#p1`), mappa; chiaro e scuro. 0 errori JavaScript in tutte. Il browser senza schermo parte in inglese (lingua del browser), quindi alcune schermate sono in inglese.

**Cosa funziona già bene.** `progetto.html` è la pagina più chiara: testo a sinistra, disegno a destra (schema del sistema, mappa con le 5 zone in rosso). L'area che si espande della scheda 4 è il grafico più forte del sito (in 30 minuti coi mezzi 42% dei torinesi, in auto quasi 100%: si vede senza leggere). Lo stile Torino è coerente su tutte le pagine, anche in scuro.

| # | Cosa non va | Prova | Gravità | Lavoro | Proposta |
|---|---|---|---|---|---|
| 3.1 | In 5 secondi la home non dice **nessun risultato**: titolo, sottotitolo e contatore parlano del progetto, non di Torino | `home_light.png`: sopra la piega ci sono solo «Torino Mobilità», «un progetto per capire…», il contatore | alta | piccolo | sotto il titolo una riga con 2-3 numeri forti e verificati (es. «12,7 km/h: la velocità di un bus alle 8» · «1 passaggio su 5 della linea 17 oltre 10 minuti di ritardo» · «il doppio svantaggio è 1,7 volte il caso»). L2 cambia il sottotitolo ma non aggiunge numeri |
| 3.2 | Home e Risultati sono quasi la stessa pagina (stessi 5 riquadri) | `home_light_full.png` e `risultati_light_full.png` | media | medio | `risultati.html` come pagina da leggere scorrendo (le 5 schede una sotto l'altra, aperte), la finestra solo per chi arriva da un link `#pN`; oppure togliere i riquadri dalla home e mettere i 3 numeri |
| 3.3 | 5 riquadri su 2 colonne: il quinto resta solo | stesse schermate | bassa | piccolo | 3 + 2 centrati, o un sesto riquadro (mappa o «fidarsi dei dati», §2.4) |
| 3.4 | Scheda 4, grafico «auto per rapporto»: le barre della stessa misura hanno lunghezze diverse fra righe, perché la traccia grigia finisce dove comincia il testo del numero (962, 1000, 940, 974 px…) | `sc/s4_0.png` | media | piccolo | colonna dei numeri a larghezza fissa. E meglio ancora: 2 barre 100% impilate («auto veloce», «auto lenta») con le 4 fasce, come la scheda 1. «Limite basso/alto» è gergo: «se l'auto va come dicono i sensori / come dice Google» |
| 3.5 | Gara: alla fine tutti i mezzi sono fermi sulla stessa linea del traguardo; il distacco si legge solo nei numeri, e un'immagine ferma (anteprima, screenshot) non dice niente | `scheda3_light.png` | media | piccolo | all'arrivo lasciare una scia lunga quanto i minuti, o scrivere «+10 min» fra bus e auto. Vale anche per la gara che gira da sola (L2) e per le 4 ore (L3) |
| 3.6 | «Le 3 coppie peggiori: Torino, Madonna Del Pilone → Torino, Vanchiglia, Torino, Parella → …»: le virgole dei nomi e della lista si confondono | `sc/s4_2.png`; codice `scripts/schede/r8.py:256` | media | piccolo | togliere «Torino, » dentro Torino, separare con «;», «del» minuscolo (vedi anche §1.6) |
| 3.7 | Scheda 2: il numero grande è 5,4% (oltre 10') ma i quadratini rossi sono 14 (oltre 5') con lo stesso colore | `sc/s2_0.png` | media | — | L2 lo risolve (due toni): va bene così |
| 3.8 | Cursore dell'area che si espande: blu predefinito del browser, fuori dallo stile | `sc/s4_0.png`, `scheda4_dark.png` | bassa | piccolo | `accent-color: var(--oro)` in `stile.css` |
| 3.9 | «Dati aggiornati al 23/10/2026» nel piè di pagina: è la data in cui è stata fatta la pagina; i dati sono del 10-20/10 | `risultati_light_full.png`; `criteri` della scheda 2 «2026-10-10 - 2026-10-20» | media | piccolo | «Dati dal 10 al 20 ottobre 2026» (letto dai JSON) |
| 3.10 | Contatori incoerenti fra pagine: home e progetto dicono «13 giorni», la memoria dice raccolta dal 3/10, L2 metterà in home i giorni dal 3/10 contati nel browser; la scheda 2 usa 1.300.434 passaggi, la home «1,6 milioni» | `data/progetto.js` (contatore 13 giorni, dal 10/10), PROMPT_LAVORI L2 passo 3 | bassa | piccolo | stessa regola su tutte le pagine; e un numero che il browser fa crescere da solo («da N giorni… e continuiamo») diventa falso se il Pi si ferma: meglio «dal 3 ottobre; ultimo dato: <data dei riassunti>» |
| 3.11 | Limiti tutti in una parte chiusa (oggi 2-3 parti, con L2 una sola) | schermate delle schede | media | piccolo | una riga di limite **visibile** sotto il numero grande (es. scheda 4: «stima: l'auto è calcolata, non misurata»). Per un selezionatore è il segno di serietà; nascosto non lo vede |
| 3.12 | La mappa si apre su un satellite senza dati: nei primi 5 secondi non si vede niente del progetto | `mappa_light.png` | media | piccolo | partire su un tema (es. «Fragilità sociale», vista «Doppio svantaggio», o «Ritardi delle linee» alle 8). È una scelta di Leo (memoria, riga 111): vedi domande |
| 3.13 | Scheda 3 a 1440×900: i punti chiave cominciano sotto la piega, dopo pallini e gara | `scheda3_light.png` | bassa | — | L2 riordina la scheda: va bene |
| 3.14 | Tema scuro: le miniature restano immagini chiare, rettangoli bianchi su fondo blu | `home_dark.png` | bassa | — | L2 le toglie: va bene |

Critiche alle scelte di L2 (solo dove vedo un problema):
- **Numeri che salgono in 2,6 secondi**: in home ci saranno 5 animazioni + 5 numeri + i mezzi in movimento insieme. Rischio di rumore e di processore: farle partire una alla volta quando il riquadro entra nella finestra (L2 lo dice per le schede; va detto anche per la home).
- **Titoli**: vedi §1.5 (scheda 5), §1.8 (scheda 3), §1.9 (scheda 1).
- **Scheda 3 «gira da sola»**: giusto, ma con §1.1 aperto il messaggio della gara («l'auto vince») potrebbe essere sbagliato. Meglio fare G1 prima di rendere la gara il pezzo più visto.

---

## 4. Mappa

- **Peso.** 6,10 MB, **2,32 MB compressa** (gzip -9; GitHub Pages la manda compressa). In locale si carica in 2,3-2,5 s. Dentro: `sezioni` 2,74 MB (tutte le 8.317 sezioni della Città metropolitana), `fermate` 1,23 MB, `imq` 0,53, `linee` 0,48, `omi` 0,38, `r6` 0,31 (misurato estraendo `const DATI`). Non è un problema grave: su rete mobile lenta 2,3 MB sono alcuni secondi, e il caricamento animato (giro C9) li copre. **Gravità bassa.** Se serve: sezioni della cintura e `fermate` caricate solo quando si sceglie un tema che le usa (lavoro medio).
- **Temi utili** (`scripts/mappa_template.html:2244-2272`): «Fragilità sociale» (con «Doppio svantaggio»), «Servizi mancanti», «Ritardi delle linee», «Parcheggi di scambio», «Spostamenti»: legati ai risultati, da tenere.
- **Temi deboli.** «Chi abita qui» con 8 viste (densità, giovani, anziani, laureati, famiglie…) è un atlante del censimento, non mobilità: ridurlo a 2-3 viste. «Prezzo delle case» mostra anche negozi, uffici, box, magazzini: per il racconto basta l'abitazione. «Velocità e traffico» usa medie calcolate sul Pi senza scartare le letture inaffidabili (`docs/R8_traffico.md`, «Da fare»): o si sostituisce con `velocita_5t.json`, o si scrive in legenda. **Gravità media, lavoro piccolo.**
- **Manca.** La scheda 4 non ha «Vedi sulla mappa» (`forma.mappa` = null nel JSON): un tema «Coi mezzi o in auto» (area che si espande da ogni zona, già calcolata) la collegherebbe. Lavoro medio.
- **Undici temi in una tendina** è molto per chi arriva da LinkedIn; i due gruppi aiutano. Proposta: in cima 3 «viste consigliate» con un clic (una per risultato forte).

---

## 5. Dati e raccolta sul Raspberry Pi

| # | Cosa non va | Prova | Gravità | Lavoro | Proposta |
|---|---|---|---|---|---|
| 5.1 | **Il GTFS non si archivia.** Lo script 27 usa un file fisso; quando GTT pubblica un orario nuovo (di solito a dicembre, prima della scadenza del 31/01/2027) le corse dei giorni nuovi non si abbinano | `scripts/27_risultato4_regolarita.py:78` (`gtt_gtfs_20261003_224530.zip`); già oggi 3.614 corse «fuori GTFS» su 51.455 (`copertura_gps.totale`); nessuno script del Pi scarica il GTFS (grep in 03, supervisore, controlla_leopi) | **alta** (P8 e tutti i rilanci futuri) | piccolo | sul Pi, una volta al giorno: scaricare `gtt_gtfs.zip`, tenerlo solo se l'hash è nuovo, col nome della data; lo 27 e il 70 scelgono il GTFS valido per ogni giorno. Avviso nel controllo giornaliero quando ne arriva uno nuovo |
| 5.2 | Sul Pi gli avvisi (10 GB, promemoria settimanale) **non arrivano a nessuno**: fuori da Windows `finestra()` stampa e basta | `scripts/supervisore.py:86-90` | media | piccolo | spazio libero del disco e peso dello storico dentro `controlla_leopi.py` (che Leo vede ogni giorno), con soglie fisse (es. ALLARME sotto 5 GB liberi) |
| 5.3 | La copia giornaliera sovrascrive quella del giorno prima **senza controllare che lo storico sia cresciuto**: se sul Pi il file si azzera (scheda SD, errore umano), il PC copia un archivio vuoto ma «integro» e perde l'unica copia | `scripts/backup_da_leopi.py:110` (`os.replace` dopo il solo controllo di integrità e di uguaglianza Pi = PC) | **alta** | piccolo | prima di sostituire: righe di `mezzi_gtt` ≥ quelle della copia vecchia e data minima uguale; altrimenti tenere la vecchia e dare ALLARME. Meglio ancora 2 copie a rotazione |
| 5.4 | Crescita: 2,1 GB il 23/10, ~190 MB al giorno → circa 10 GB ai primi di dicembre, circa 21 GB a fine gennaio; copia intera ogni giorno (oggi ~10 min, allora ~1,5 ore) e uno snapshot completo in `/tmp` sul Pi | memoria, riga 89; `backup_da_leopi.py` (snapshot in `/tmp/gtt_storico_*.sqlite`) | media | medio | (a) da verificare sul Pi con `df -h /tmp`: se `/tmp` è in memoria (succede nelle versioni recenti di Debian, su cui gira Python 3.13) lo snapshot fallirà presto; spostarlo in una cartella sul disco; (b) un file per mese (i mesi chiusi si copiano una volta sola); (c) i ritardi del feed, che il R4 non usa più per i numeri, si possono riassumere e alleggerire |
| 5.5 | Se il PC resta spento (vacanze), nessuno si accorge che il Pi è fermo | il controllo parte da `RACCOLTA_GIORNALIERA.bat` sul PC | media | piccolo | un controllo che parte dal Pi stesso e manda un avviso al telefono (un servizio di «battito» gratuito come healthchecks.io, o una notifica): da decidere con Leo, è un servizio esterno |
| 5.6 | Un solo posto per lo storico grezzo (Pi + una copia nella stessa casa) | memoria, sezione 3 | media | piccolo | i riassunti mensili sono già in git (`data/storico_riassunti/`): bene. Aggiungere una copia del mese chiuso su un disco esterno o nella Release |
| 5.7 | **Licenze: il README dice IMQ e OMI «non ripubblicati», ma sono in git** come dati derivati | in git: `data/processed/imq_od.json` (matrice origine/destinazione con il numero di interviste per cella), `imq_zone*.json`, `imq_residenti.json`, `omi_zone.json` (perimetri e prezzi minimo-massimo per 4 tipi di immobile in 68 comuni, cioè quasi tutto il file OMI); e la mappa li contiene | media | piccolo | scegliere: o la frase del README diventa «ripubblichiamo solo dati aggregati derivati, citando la fonte», o i file escono da git. Decisione di Leo (domanda 4) |
| 5.8 | Il testo intero del rapporto di sostenibilità GTT 2025 è in git, in 104 file | `git ls-files data/processed/rapporto_gtt` = 104; es. `blocco_005.txt` è testo del PDF | bassa | piccolo | i fatti estratti sono utili (980 fatti verificati); il testo integrale di un documento di terzi non serve: lasciarlo fuori da git |
| 5.8b | Fonti con licenza «da riconfermare» (GTFS statico, testo della IODL 2.0) | `docs/FONTI_DATI.md`, tabella in testa | bassa | piccolo | riaprire le due pagine prima di accendere GitHub Pages |

---

## 6. Codice e riproducibilità

| # | Cosa non va | Prova | Gravità | Lavoro | Proposta |
|---|---|---|---|---|---|
| 6.1 | **Un estraneo non può rifare i risultati.** `r5py` e `geopandas` (usati da 18, 22, 39, 93, 99) non sono in `requirements.txt`; lo script 18 impone Java in `data/otp/jdk-25.0.4.1+1-jre`, cartella «fuori» (né git né Release). Il README promette «pip install -r requirements.txt, scarica_dati, rifai_tutto» | `requirements.txt`; `scripts/18_accessibilita.py:37` e `:300` (`os.environ["JAVA_HOME"] = …` sempre, anche se Java c'è già); `docs/DATI.md`: `data/otp/jdk-25…` 320 file «fuori»; P7 ha provato da zero solo `--solo schede,mappa` | **alta** | piccolo | aggiungere r5py e geopandas con versione; usare la cartella del JDK solo se esiste, altrimenti il Java del sistema (`setdefault`); nel README: «serve Java 21 o più». Prova da zero in un contenitore pulito di almeno le fasi r1, r8, r10 |
| 6.2 | Gli AVVISI non fermano niente e il controllo su GitHub non ricalcola: un numero cambiato passa inosservato | `rifai_tutto.py` stampa solo «cerca la parola AVVISO nel log»; `controllo.yml` lancia `schede_risultati.py` ma non guarda cosa cambia | media | piccolo | nel controllo su GitHub, dopo `schede_risultati.py`: `git diff --exit-code` su `data/schede_risultati.js`, `r/`, `README.md` ignorando il campo `generato`. L'ho provato su una copia: oggi l'unica differenza è proprio `generato` (10 righe), quindi il controllo sarebbe verde e scatterebbe se qualcuno toccasse a mano i file o dimenticasse di rilanciare |
| 6.3 | I numeri pubblicati dipendono dal giorno in cui si rilancia | §1.12 | media | piccolo | periodo fisso nei parametri, scritto nei JSON |
| 6.4 | `rifai_tutto.py` non registra le versioni (Python, librerie, hash del GTFS, periodo) | lettura del file | bassa | piccolo | all'inizio del log: `pip freeze`, hash dei file in `data/raw`, periodo |
| 6.5 | La prova delle pagine conta gli errori JavaScript, ma non controlla che i numeri disegnati siano quelli dei JSON | `prova_pagine.py`; il difetto §3.4 (barre di lunghezze diverse) non lo vede nessuna prova | bassa | medio | una prova che legge da pagina il numero grande di ogni scheda e lo confronta con `data/schede_risultati.js` |
| 6.6 | Buono: `rifai_tutto.py --prova-secca`, pyflakes a zero, controllo verde (ultimi 5 giri su `prova` riusciti, l'ultimo il 23/10 alle 17:18 UTC), schede rifatte identiche salvo la data | GitHub Actions; prova mia sulla copia | — | — | da mettere in vista nel README |

---

## 7. Portfolio: come lo vede un selezionatore

**Punti di forza da mettere più in vista**
1. **Raccolta vera e continua** (Raspberry Pi, ogni minuto, da settimane, 1,6 milioni di passaggi GPS). È raro in un portfolio: oggi è un contatore piccolo nella home.
2. **Aver scoperto che il dato ufficiale sbaglia** (feed dei ritardi 5,4% contro GPS 14,1%, 2,6 volte) e averlo corretto. È la competenza che un datore di lavoro cerca: va in un risultato a sé (§2.4), non in un paragrafo.
3. **Onestà sui limiti** (tag dei dati, classi C-DEBOLE, sensibilità). È un punto di forza solo se si vede (§3.11) e se è coerente (§1.3).
4. **Il legame tesi 2020 → verifica 2026** in `progetto.html`: racconto personale e credibile.

**Punti deboli che danneggiano**
1. **Metodo cambiato dopo aver visto i numeri, ma dichiarato «fissato prima»** (§1.3): un revisore attento lo trova nella storia di git, che è pubblica. Danno più grande di qualsiasi difetto grafico.
2. **Titoli più forti dei dati** su R6 e R8 (§1.1, §1.2): proprio i due risultati che chi legge di trasporti guarda per primi.
3. **Il lavoro sembra fatto quasi tutto da Claude**: 97 commit su 119 di `prova` hanno «Co-Authored-By: Claude» (`git log origin/prova --format=%b | grep -c "Co-Authored-By: Claude"`), e `sviluppo/` (8,4 MB) è pieno di prompt per agenti, esiti di giri ed «ESITO_C13_68-95.md». Non è un male usare un assistente, ma va detto bene: una riga nel README («costruito con Claude Code come assistente: domande, scelte di metodo e controlli sono miei») e `sviluppo/` fuori dalla vetrina (cartella spostata o in un ramo, o almeno un `sviluppo/README.md` che spiega cos'è).
4. **Commit con messaggi vuoti**: «descrizione di cosa hai fatto» (2 volte), «descrizione» (`git log --format=%s`). Pochi, ma visibili.
5. **Cinque risultati tutti con la stessa forza** apparente: nessuno spicca. Meglio 1-2 risultati forti in testa (la scheda 5 corretta, l'affidabilità dei dati) e gli altri dopo.
6. **Documenti di lavoro solo in italiano** e molto lunghi: per un selezionatore estero basta il README inglese (già fatto bene).

**Cosa togliere (o nascondere)**
- Il punto «95,3% dei km di strade grandi ha una fermata frequente vicina» (scheda 4, parte extra): vale solo per le strade grandi, dove le fermate ci sono per definizione; non dice niente di nuovo.
- Il grafico metro/prezzi della scheda 5 (§1.13).
- Le 8 viste di «Chi abita qui» ridotte a 2-3.
- Gli screenshot di lavoro in `sviluppo/c5_screenshot/`, `c6_screenshot/`, `prove_stile_*.png` (25 + immagini; non servono a chi visita).

---

## Tabella unica delle proposte (in ordine di valore rispetto al lavoro)

| Ordine | Proposta | § | Valore | Lavoro | Dove |
|---|---|---|---|---|---|
| 1 | Tempi Google in entrata e a 4 ore (G1) | 1.1, 1.2, 1.14 | molto alto | piccolo | Leo a mano + PC |
| 2 | Togliere «fissate prima dei numeri» dalla scheda 4 e dire la storia del metodo | 1.3 | alto | piccolo | cloud |
| 3 | Requisiti e Java per un estraneo; prova da zero di r1, r8, r10 | 6.1 | alto | piccolo | cloud + PC |
| 4 | Controllo della copia giornaliera (non sovrascrivere con uno storico più piccolo) | 5.3 | alto | piccolo | cloud + Leo |
| 5 | GTFS archiviato ogni giorno sul Pi, GTFS giusto per giorno nel 27 e nel 70 | 5.1 | alto | piccolo | cloud + Leo sul Pi |
| 6 | Scheda 5: parziali a parità di distanza e confronto col caso | 1.4, 1.5, 2.5 | alto | piccolo | cloud + PC |
| 7 | Sesto risultato «Quanto ci si può fidare dei dati aperti» | 2.4 | alto | piccolo | cloud |
| 8 | Velocità dei bus ora per ora (scheda o punto chiave + controllo della forbice) | 2.1 | alto | piccolo | PC |
| 9 | Periodo fisso nei risultati + controllo `git diff` delle schede su GitHub | 1.12, 6.2, 6.3 | medio-alto | piccolo | cloud |
| 10 | Vetrina del repository: riga sull'uso di Claude, `sviluppo/` spiegato, commit leggibili | 7 | medio-alto | piccolo | cloud + Leo |
| 11 | Home: 2-3 numeri sotto il titolo; limite visibile sotto ogni numero grande; «dati dal 10 al 20/10» | 3.1, 3.9, 3.11 | medio-alto | piccolo | cloud (dopo L2) |
| 12 | Linea 17 come caso concreto | 2.2 | medio | piccolo | PC |
| 13 | Scheda 4: coppie con almeno 30 interviste; «47% delle auto» nel testo | 1.6, 1.7 | medio | piccolo | PC |
| 14 | Titoli di L2 corretti (schede 1, 3, 5) | 1.5, 1.8, 1.9 | medio | piccolo | dentro L2 o subito dopo |
| 15 | Grafico «auto per rapporto» rifatto; gara con il distacco all'arrivo; testo delle coppie | 3.4, 3.5, 3.6 | medio | piccolo | cloud |
| 16 | Avvisi del Pi dentro `controlla_leopi.py` (spazio, peso, `/tmp`) | 5.2, 5.4 | medio | piccolo | cloud + Leo |
| 17 | Mappa: partire su un tema; 3 viste consigliate; «Chi abita qui» ridotto | 3.12, 4 | medio | piccolo | cloud |
| 18 | Licenze: frase del README coerente con i file IMQ/OMI in git; testo GTT fuori | 5.7, 5.8 | medio | piccolo | Leo decide, cloud |
| 19 | Anticipi dei bus (dopo il controllo §1.11) | 1.11, 2.3 | medio | piccolo-medio | PC |
| 20 | Per circoscrizione | 2.7 | medio | piccolo-medio | cloud + PC |
| 21 | Doppio svantaggio anche sui mezzi | 2.6 | medio | medio | PC |
| 22 | Risultati come pagina da scorrere | 3.2 | medio | medio | cloud |
| 23 | Tornare a casa di notte (R2) | 2.8 | medio | medio | PC |
| 24 | Avviso dal Pi al telefono se la raccolta si ferma | 5.5 | medio | piccolo | Leo decide |
| 25 | Copia dei mesi chiusi fuori casa; file per mese | 5.4, 5.6 | medio | medio | PC |
| 26 | Tema «Coi mezzi o in auto» in mappa | 4 | basso-medio | medio | cloud |
| 27 | Prova che i numeri disegnati = JSON; versioni nel log | 6.4, 6.5 | basso | piccolo-medio | cloud |
| 28 | Cose minori (METODO colori, accent-color, griglia 3+2, metro/prezzi) | 1.13, 3.3, 3.8 | basso | piccolo | cloud |

### Bozze di giro per le prime 10 (stile `PROMPT_LAVORI.md`)

Regole comuni come in `PROMPT_LAVORI.md` (leggere `sviluppo/AGENTS.md` e la memoria, controllare i rami, provare davvero, esito in
`sviluppo/piani/ESITO_<giro>.md`, memoria, commit e push). **Soglie e regole qui sotto sono fissate ora, prima di vedere i numeri:
non si cambiano dopo.** I giri vanno fatti dopo L2 e L3, oppure G1 prima di L3 (vedi domanda 1).

**G1 — Leo a mano + PC: tempi Google in entrata e a 4 ore** (proposte 1)
```
Dove: Leo a mano (circa 1 ora), poi PC.
Regole fissate prima:
- Percorsi: i 12 punti prioritari e i 5 interscambi del R6 → Piazza Castello (in entrata), e i 6 percorsi di oggi anche al contrario (cintura → Piazza Castello).
- Ore: martedì o mercoledì feriale, partenza 8:00, 13:00, 17:30, 21:00; Google Maps «Parti alle», tempo in auto tipico (il valore centrale se Google dà una forbice).
- Fattore per percorso = (tempo Google) / flusso libero del modello, SENZA togliere 5 minuti (Google non conta il parcheggio).
- Fattore in entrata alle 8 = mediana dei 17 percorsi in entrata; limite «auto lenta» = 75° percentile, «auto veloce» = 25° percentile (non più mediana).
- Se il fattore in entrata alle 8 differisce da 2,1 di più di 0,3: il R6 si rifà col fattore in entrata e il titolo segue la regola di oggi (classe con 1,5).
Passi:
1. Leo riempie data/ref/google_tempi.csv (colonne: da, a, direzione, ora, minuti_auto, data_della_ricerca).
2. PC: lo script 93 legge il CSV (se c'è) al posto delle costanti; ricalcola fattori e quantili; scrive i fattori nel JSON e nel rapporto. Poi 94 e 99.
3. Tabella prima/dopo nell'esito: fattore in entrata e in uscita, classi dei 12 punti, minuti di pareggio, rapporto mediano della scheda 4.
Prove: controlli già presenti in 93/94 (nessun tempo nullo, negativo o infinito); il fattore in uscita alle 8 deve tornare 2,1 ± 0,1 coi 6 percorsi di oggi (se no fermarsi); schede e prova_pagine.py 0 errori.
```

**C-A — CLOUD: onestà del metodo nella scheda 4** (proposta 2)
```
1. scripts/schede/r8.py:247 e :262: togliere «fissate prima dei numeri» / «decise prima di vedere i numeri»; scrivere «fasce scelte dopo le prime prove (vedi docs/R8_traffico.md)»; traduzioni in testi.json.
2. docs/R8_traffico.md: sezione «Storia del metodo» con i 5 commit del 21/10 (9f1015e, f32c661, 543bc13, de8b05a, ec584a3), una riga ciascuno; togliere «La verità sta nella forbice» e scrivere «due stime: il valore vero può stare fuori».
3. Nella scheda 4, fra gli altri grafici: le quote con le fasce di oggi e con le soglie 1,5/2 (dal JSON, campo precedenti), solo come sensibilità.
Prove: schede_risultati.py senza ATTENZIONE; prova_pagine.py 0 errori; git grep "prima dei numeri" scripts/schede/r8.py vuoto.
```

**C-B — CLOUD + PC: rifare i calcoli da zero** (proposta 3)
```
1. requirements.txt: r5py e geopandas con la versione installata sul PC (Leo: python -m pip show r5py geopandas). 
2. scripts/18_accessibilita.py, 93, 99, 22, 39: JAVA_HOME = cartella data/otp/jdk-* solo se esiste; altrimenti quello del sistema; messaggio chiaro se Java manca («serve Java 21 o più»).
3. README (IT e EN), «Come rifare i calcoli»: Java, r5py, quali fasi servono IMQ e OMI a mano.
4. PC: clone in una cartella temporanea, scarica_dati.py, IMQ e OMI a mano, rifai_tutto.py --solo r1,r8,r10,schede. Regola fissata prima: i numeri principali dei rapporti devono essere UGUALI (salvo data) a quelli in git; se no fermarsi e scrivere le differenze.
Prove: controllo GitHub verde; esito con i tempi e le differenze.
```

**C-C — CLOUD, poi Leo: copia giornaliera che non perde dati** (proposta 4)
```
1. scripts/backup_da_leopi.py: prima di os.replace, se esiste la copia vecchia, leggere righe di mezzi_gtt e flussi_5t e MIN(letto_utc). Regola fissata prima: si sostituisce solo se righe nuove >= righe vecchie e MIN uguale; altrimenti si tiene la vecchia, si salva la nuova come storico_backup_SOSPETTO.sqlite e si esce con codice 1 (finestra di avviso già esistente nel .bat).
2. Tenere anche storico_backup_ieri.sqlite (rotazione a 2).
3. Prova con --prova su due database finti (uno più piccolo): deve rifiutarlo.
Leo: lancia RACCOLTA_GIORNALIERA.bat a mano una volta e controlla il log.
```

**C-D — CLOUD, poi Leo sul Pi: archivio del GTFS** (proposta 5)
```
1. Nel raccoglitore (03) o nel supervisore: una volta al giorno scaricare https://www.gtt.to.it/open_data/gtt_gtfs.zip; se l'hash è nuovo, salvarlo come data/gtfs/gtt_gtfs_AAAAMMGG.zip e scrivere una riga in una tabella gtfs_versioni (data, hash, inizio e fine validità da feed_info o calendar).
2. scripts/27 e 70: per ogni giorno usare il GTFS la cui validità lo contiene (il più recente scaricato prima di quel giorno); se nessuno, AVVISO e giorno saltato. Con un solo GTFS i numeri devono restare identici (regola di prova).
3. controlla_leopi.py: riga «GTFS: ultima versione del …, valida fino al …»; ALLARME se la validità finisce entro 14 giorni.
4. AGGIORNA_RACCOLTA_LEOPI.bat per Leo.
Prove: --prova con due GTFS finti; 27 sui riassunti: stessi numeri di oggi.
```

**P-E — PC: scheda 5 più solida** (proposta 6)
```
Regole fissate prima: distanza = distanza_castello_m già nel JSON; correlazione parziale di Spearman (ranghi, residui di una retta sulla distanza); intervallo al 95% con 2.000 ricampionamenti delle zone; «regge» se l'intervallo non contiene lo 0.
1. scripts/95: aggiungere a e1 le parziali prezzo-servizi, prezzo-fragilità, fragilità-servizi a parità di distanza; a e2 il confronto col caso (quota attesa = quota fragilità alta × quota servizi bassi, per residenti e per sezioni) e il rapporto osservato/atteso.
2. Scheda 5: domanda «Dove le case costano poco ci sono anche meno servizi e più fragilità?»; punto chiave sul confronto col caso; punto sui prezzi che dice cosa regge e cosa no secondo la regola sopra (il testo sceglie la frase da solo).
Attesi dal controllo di oggi (solo per verifica, non per scegliere): prezzo-servizi 0,21, prezzo-fragilità −0,68, fragilità-servizi −0,48; osservato/atteso 1,67 (residenti).
Prove: schede senza ATTENZIONE, prova_pagine.py 0 errori.
```

**C-F — CLOUD: sesto risultato «Quanto ci si può fidare dei dati aperti»** (proposta 7)
```
1. scripts/schede/r_fiducia.py: legge solo file già in git (risultato4_regolarita.json: confronto_feed e copertura_gps; sensori_esclusi.json; tp_contro_auto.json; rapporti dei parcheggi per il contatore fermo). Nessun numero a mano.
2. Titolo dalla regola: «Il dato ufficiale dei ritardi conta X volte meno ritardi del GPS» con X = ritardo oltre 5' GPS / feed, arrotondato a 0,5.
3. Numero grande X; animazione semplice (due barre); punti: sensori esclusi su totale, copertura GPS, giorni esclusi; limiti: «il GPS ha i suoi errori (60 m dalla fermata)».
4. Numerazione pubblica 6; README e r/6.html dallo script.
Prove: come gli altri giri delle schede.
```

**P-G — PC: velocità dei bus ora per ora** (proposta 8)
```
Regole fissate prima: feriali del periodo fisso del R4; velocità = come oggi nella mappa (scrivere nel documento come è calcolata); media pesata per numero di letture; ore 5-23; fattore di punta dei bus = velocità alle 4-5 / velocità alle 8.
1. scripts/101 (numero libero dopo L3): legge i dati da cui il 04 costruisce «vel»; scrive data/processed/velocita_bus.json e un rapporto.
2. Scheda 2 o 4: grafico a linea ora per ora; punto chiave «alle 8 un bus va a N km/h».
3. Nel documento R8: il fattore dei bus accanto a 1,2 (sensori) e al fattore Google: solo confronto, non entra nel calcolo.
Prove: velocità fra 5 e 40 km/h, nessuna ora vuota fra 6 e 22 (se no AVVISO).
```

**C-H — CLOUD: risultati stabili e controllati** (proposta 9)
```
1. comuni.py: PERIODO_RISULTATI = ("2026-10-10", "2026-10-20"); 26, 27, 33, 70, 71, 88 leggono solo quei giorni (opzione --fino-al per cambiarlo) e lo scrivono nel JSON.
2. controllo.yml: dopo schede_risultati.py, controllo che data/schede_risultati.js, r/ e README.md non cambino se non nel campo «generato» (piccolo script controlla_schede_invariate.py).
3. Nelle schede: «Dati dal … al …» al posto di «aggiornati al».
Prove: sul PC, rilancio di 27 e 70 con lo storico vivo: stessi numeri pubblicati oggi (14,1%, 5,44%).
```

**C-I — CLOUD + Leo: vetrina del repository** (proposta 10)
```
1. README (IT e EN), sezione «Come è fatto»: una riga sull'uso di Claude Code, scritta da Leo.
2. sviluppo/README.md: «appunti di lavoro e piani per l'assistente; non serve per usare il sito».
3. Leo decide se spostare gli screenshot di lavoro (sviluppo/c5_screenshot, c6_screenshot, prove_stile_*) fuori dal ramo main.
4. Da ora: messaggi di commit che dicono cosa cambia (regola in AGENTS.md); i messaggi vecchi non si riscrivono (storia pubblica).
```

---

## Domande per Leo

1. **G1 prima di L3?** Il fattore di Google è misurato solo in uscita dal centro. Vuoi prendere a mano i tempi in entrata (circa 1 ora con Google Maps) **prima** di L3, così le 4 ore usano tempi veri invece del fattore riscalato? Se esce che l'auto in entrata è molto più lenta, la scheda 3 cambia messaggio («il parcheggio di scambio può convenire»).
2. **Titoli di L2.** Accetti le tre correzioni (scheda 1 senza «città dei 15 minuti»; scheda 3 «non hanno abbastanza posti» con «1 su 4 non ne ha nessuno»; scheda 5 con «quasi il doppio del caso»), o preferisci tenere quelli scelti il 23/10?
3. **Mappa all'apertura.** Oggi parte sul satellite senza tema (scelta tua). Per chi arriva da LinkedIn proporrei di partire su «Doppio svantaggio» o «Ritardi delle linee alle 8». Va bene cambiarla?
4. **IMQ e OMI in git.** I dati derivati (matrice degli spostamenti, prezzi OMI per zona) sono già in git e nella mappa. Li consideri pubblicabili come dati aggregati citando la fonte (e allora cambiamo la frase del README), o li togliamo?
5. **Claude nel portfolio.** Come vuoi presentare l'uso di Claude Code (97 commit su 119 lo citano)? Una riga nel README scritta da te, oppure niente e `sviluppo/` fuori dal ramo pubblicato?
