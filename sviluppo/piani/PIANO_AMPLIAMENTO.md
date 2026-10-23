# Piano (da discutere) — Ampliare il progetto: dati che abbiamo, dati che mancano, risultati nuovi

Scritto il 23/10/2026 sera, dopo L2 (`prova` 36e9372), mentre L3 è aperto. **Solo proposte**: niente è deciso. Le idee che toccano le schede 3 e 4
aspettano la fine di L3. Le prove (file, numeri, comandi) sono accanto a ogni voce; i calcoli «prova grezza» sono fatti nel cloud sui file in git
e vanno rifatti per bene. Regola di sempre: **soglie e regole di ogni risultato nuovo si fissano prima di vedere i numeri.**

## 1. Cosa abbiamo, e quanto lo usiamo

| Dato | Usato in | Poco usato o mai usato |
|---|---|---|
| **GPS dei mezzi** (storico + riassunti `passaggi_2026-10.zip` in git: per ogni passaggio corsa, fermata, istante) | R4, home | **tempi fra due fermate** (dove i bus si fermano), velocità vera ora per ora (12,7 km/h alle 8, dati già nella mappa), variabilità dei tempi di viaggio, anticipi (38% dei passaggi oltre 1 minuto prima), corse programmate mai viste |
| Feed dei ritardi GTT (`trip_update_gtt`) | solo il confronto col GPS | pesa ~190 MB al giorno per un confronto già fatto (`PIANO_RACCOLTA.md`, passo 5) |
| Avvisi GTT (`avvisi_gtt`) | **mai** | deviazioni, scioperi, lavori: servirebbero a spiegare i giorni anomali del R4. Il 23/10 sera l'indirizzo del feed dava errore |
| Sensori 5T, ogni 5 minuti (velocità e flusso) | R8 (valori tipici), R6 | giorno per giorno: pioggia, scioperi, ora legale, «quando comincia l'ora di punta» |
| Parcheggi 5T | R6 (riempimento) | curva di riempimento per ora; pochi garage |
| GTFS GTT | accessibilità, R4, R6, R8 | **offerta per quartiere** (corse per abitante), chilometri per bus/tram/metro, la sera (quando la frequenza crolla), struttura della rete (radiale o di traverso) |
| Censimento 2021 per sezione | fragilità, residenti | — |
| IMQ 2022 (indagine sugli spostamenti) | domanda del traffico, R6, popolarità delle zone | **scelta del mezzo** (chi prende l'auto e perché), scopi, età, ore; nessuna scheda «chi va dove» |
| **ISTAT pendolarismo 2011** (Comune per Comune, **con mezzo, ora di uscita e durata**) e **2021** (Comune per Comune) | **mai** (scaricati, in `data/raw/istat`, nella Release) | conteggi completi, non un campione: quota di auto di chi entra a Torino per lavoro, comune per comune (oggi il R6 usa 64 interviste); cambiamento 2011 → 2021 |
| Redditi IRPEF 2024 per comune (`data/raw/Redditi_…_2024`) | **mai** | reddito dei comuni della cintura (Torino è un solo valore) |
| Rapporto di sostenibilità GTT 2025 (980 fatti) | confronto del R4 (2,3%) | **passeggeri per tipo di mezzo**: bus urbani 183,7 milioni, tram 52,7, metro 48,3; vetture-km 55,0 milioni; 305 viaggi per abitante all'anno contro 257,7 nel Nord-Ovest (`docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`, righe 9-37) |
| OMI 2025/2 | scheda 5 | un solo semestre (E4 tolto da Leo) |

## 2. Cosa manca, verificato oggi

| Dato | Stato | Cosa si può fare al suo posto |
|---|---|---|
| **Passeggeri per linea / affollamento** | **Non c'è.** Il feed GTT dal vivo (23/10, 364 mezzi) non ha i campi dell'affollamento; nessun dato aperto per linea trovato sul web (GTT e Fondazione Links parlano di migliorare il conteggio dei passeggeri; la Regione ha fatto campagne di conteggio su 4, 15, 16, 11, 56 ma non sono pubbliche) | (a) totali per tipo di mezzo dal rapporto GTT; (b) **stima del carico per linea**: i viaggi coi mezzi dell'IMQ messi sulla rete (stesso motore r5py) e riportati ai totali del rapporto: [STIMATO]; (c) chiedere a GTT o all'Agenzia le validazioni BIP per linea (Leo ha già scritto all'Agenzia per altro); (d) passeggeri per abitante delle città italiane (ISTAT, «Dati ambientali nelle città») per un confronto |
| **Treni (SFM) e bus di altre aziende** | **Nessun GTFS aperto trovato** per il Piemonte; il Punto di Accesso Nazionale (cciss.it) ha gli orari Trenitalia in formato NeTEx, da verificare licenza e copertura | (a) NeTEx convertito in GTFS (lavoro grande, licenza da verificare); (b) un orario a mano delle 8 linee SFM per un feriale di riferimento (medio); (c) solo una **prova di quanto pesa**: sui corridoi coi treni (Moncalieri, Chieri, Settimo, Pinerolo) quanto cambierebbero R6 e R8 (Google: Moncalieri → Lingotto 19-23 minuti col treno contro 33 solo GTT) |
| Qualità dell'aria oraria | sul Comune solo medie annuali 2007-2015; **ARPA Piemonte** dà i dati orari di ogni stazione degli ultimi due anni in CSV (secondo i documenti ARPA; licenza da verificare) | NO2 contro traffico 5T ora per ora (stazioni Rebaudengo, Lingotto, Rubino…) |
| Meteo | archivio orario gratuito (Open-Meteo, CC BY 4.0; raggiungibile) e ARPA | pioggia contro ritardi e traffico |
| Incidenti | geolocalizzati su aperTO solo fino al 2017; ISTAT ha i dati 2024 georeferenziati al 99,8% (documento ISTAT, non verificato per Torino) | da cercare meglio; utile con il modello del traffico |
| Scioperi | calendario pubblico del Ministero dei trasporti | esperimenti naturali (traffico in un giorno senza mezzi) |
| Bici, telefonia, logistica, eventi | **congelati da Leo (20/10)** | — |
| Costi del servizio | `PIANO_COSTI.md` | vedi 3.3 |

## 3. Risultati nuovi (in ordine di valore rispetto al lavoro)

Per ognuno: domanda · dati già pronti · regola da fissare prima · lavoro · perché interessa · rischio.

### 3.1 «Dove si fermano i bus» (tempi fra due fermate) — il risultato più «da smart city»
- **Domanda.** Su quali tratti di strada i bus e i tram perdono più tempo all'ora di punta rispetto alla notte, e quanti minuti al giorno si perdono lì?
- **Dati pronti.** Riassunti `passaggi_*.zip` (in git) + GTFS della Release: per ogni coppia di fermate consecutive, tempo misurato alle 8 e alle 3-5 (o alle 21). Nessun dato nuovo.
- **Regola prima.** Tratti con almeno 200 passaggi in ogni fascia; «minuti persi» = (mediana alle 8 − mediana di notte) × passaggi alle 8; classifica dei 20 tratti peggiori; solo linee urbane.
- **Lavoro.** Medio (uno script nuovo + un tema della mappa «Dove si fermano i bus»).
- **Perché.** È il dato che solo questo progetto ha (GPS raccolto ogni minuto); dice dove servirebbero corsie preferenziali o semafori con priorità: un risultato **utile a qualcuno**. E dà un **fattore di punta misurato strada per strada e nelle due direzioni** (bus in mezzo al traffico), che aiuta a riparare il problema del fattore di Google misurato solo in uscita (`ANALISI_CRITICA.md` §1.1).
- **Rischio.** Il tempo fra due fermate comprende la salita dei passeggeri (più gente alle 8): va detto nei limiti.

### 3.2 «Dove il mezzo pubblico è lento, si prende l'auto» (scelta del mezzo)
- **Domanda.** Le coppie di zone dove i mezzi impiegano molto più dell'auto hanno meno persone che usano i mezzi?
- **Dati pronti.** `imq_od.json` (viaggi per modo) + `tp_contro_auto.json` (rapporto dei tempi), entrambi in git.
- **Prova grezza (cloud, 23/10)**: coppie con almeno 30 interviste: **Torino-cintura, 21 coppie, Spearman −0,79 (p < 0,001)**: dove il rapporto è più alto la quota dei mezzi crolla. Dentro Torino (114 coppie) −0,13, non significativo. Quota dei mezzi per fascia (Torino e cintura insieme): rapporto sotto 1,5 → 38%; 1,5-2,5 → 21%.
- **Regola prima.** Solo celle con almeno 30 interviste (`SOGLIA_N` dello script 14); Spearman con intervallo al 95% (ricampionamento); gruppi separati; un risultato «regge» solo se l'intervallo non contiene lo 0.
- **Lavoro.** Piccolo. **Perché.** Trasforma la scheda 4 da descrizione («2-3 volte») a comportamento («e infatti chi viene dalla cintura prende l'auto»); prepara la metrica di Leo «quanti veicoli in meno».
- **Rischio.** È una relazione, non una causa (chi abita lontano ha anche più auto); dentro Torino non regge: va detto.

### 3.3 «Quanto lavora un chilometro di tram, di bus, di metro» (il livello «business» della tesi)
- **Domanda.** Quanti passeggeri porta ogni chilometro percorso da un tram, un bus, la metro?
- **Dati pronti.** Passeggeri per tipo di mezzo (rapporto GTT 2025) + vetture-km per tipo dal GTFS.
- **Prova grezza (cloud, dai dati della mappa, metodo rozzo)**: vetture-km annue stimate 72 milioni contro i 55,0 del rapporto (+31%: il metodo grezzo conta troppo); tram ~5,6 passeggeri per vettura-km, bus ~3,2 (rapporto circa 1,7). Da rifare sul GTFS vero.
- **Regola prima.** Il totale delle vetture-km dal GTFS deve stare entro ±15% dei 55,0 milioni del rapporto, altrimenti ci si ferma; metro a parte (vetture diverse).
- **Lavoro.** Piccolo. **Perché.** È la domanda «tram contro bus» già nella memoria (sezione 6, punto 4) e chiude il cerchio con la tesi di Management; un numero semplice per un post.
- **Rischio.** Bus urbani ed extraurbani nello stesso conto del GTFS: separarli per linea.

### 3.4 «Quanto ci si può fidare dei dati aperti» (sesto risultato)
Già in `ANALISI_CRITICA.md` §2.4: feed contro GPS (dopo L2: 6,0% contro 15,6%), sensori 5T esclusi, contatori fermi, orologio sbagliato, feed degli avvisi in errore. **Piccolo**; il più vendibile per un portfolio di analisi dati.

### 3.5 «Chi entra a Torino in auto, comune per comune» (pendolari ISTAT)
- **Dati pronti.** ISTAT pendolarismo 2011 con mezzo (dati completi del censimento) e 2021 (volumi), in `data/raw/istat` (Release).
- **Cosa dà.** Quota di auto per comune di partenza verso Torino con migliaia di persone invece di 64 interviste; confronto 2011 → 2021 dei volumi; ora di uscita (picco). Rafforza il R6 (quanti lascerebbero l'auto) e la scheda 4.
- **Da verificare prima.** Cosa contiene esattamente il file 2021 (se ha il mezzo). **Lavoro.** Medio. **Rischio.** Il 2011 è vecchio: si usa per le proporzioni, non per i numeri assoluti.

### 3.6 «Offerta e fragilità»: le zone fragili hanno meno mezzi pubblici?
- **Dati pronti.** GTFS (corse per fermata e ora, anche in `data/processed/orari_fermate.js`), sezioni con fragilità e residenti.
- **Regola prima.** Corse all'ora fra le 7 e le 9 alle fermate entro 400 m dal centro della sezione, per abitante, per quintile di fragilità; Torino sola.
- **Lavoro.** Piccolo-medio. **Perché.** Unisce le due anime del progetto (sociale e trasporti) e rafforza la scheda 5 («anche meno servizio?» oppure «no: il mezzo pubblico c'è, mancano gli altri servizi»: tutte e due sono una notizia).

### 3.7 «La sera Torino si spegne?»
- **Dati pronti.** GTFS (frequenze per ora) + attese misurate per fascia (R4: la sera l'attesa media supera i 9 minuti).
- **Lavoro.** Piccolo. **Perché.** È la domanda giusta del R2 in pausa («tornare a casa la sera») senza calcoli lunghi; il R2 completo (r5py dai luoghi della notte con gli scenari della metro già costruiti) può venire dopo.

### 3.8 Pioggia, scioperi, ora legale (esperimenti naturali)
- **Dati pronti.** Storico (GPS, 5T) + meteo orario scaricabile dopo (Open-Meteo) + calendario degli scioperi.
- **Regola prima.** «Giorno di pioggia» = almeno 5 mm fra le 7 e le 9 a Torino; confronto con i feriali asciutti della stessa settimana; ritardo oltre 5' e velocità 5T. Ora legale: due settimane prima e dopo il 25/10, stesse ore.
- **Lavoro.** Piccolo per ognuno, **ma serve un mese di dati** (metà novembre, con P8). **Perché.** Risultati facili da raccontare («quando piove i ritardi salgono del X%»).

### 3.9 Aria e traffico
- **Dati.** NO2 orario ARPA (da scaricare, licenza da verificare) + flussi 5T vicini alle stazioni.
- **Lavoro.** Medio. **Perché.** Dà sostanza all'«esposizione al traffico» della scheda 1, oggi solo distanza da una strada stimata.

### 3.10 Carico stimato per linea (il dato dei passeggeri che manca)
- **Come.** Viaggi coi mezzi dell'IMQ (per zona e ora) messi sulla rete GTT con r5py (percorso più veloce), sommati per linea e tratta; totale riportato ai passeggeri del rapporto GTT per tipo di mezzo.
- **Lavoro.** Grande. **Perché.** È il pezzo che chi lavora nei trasporti cerca per primo (dove i mezzi sono pieni). [STIMATO], da confrontare con le campagne della Regione se diventano pubbliche.

### 3.11 Cose più grandi, più avanti
- Treni nel calcolo (2, riga «Treni»). Confronto con un'altra città (Milano o Bologna) con lo stesso metodo di accessibilità. Per circoscrizione (confini aperTO): piccolo-medio, già in `ANALISI_CRITICA.md` §2.7.

## 4. Come metterli insieme (proposta di racconto)

Oggi i risultati sono 5 schede indipendenti. Con 3.1-3.4 il sito può raccontare tre storie:
1. **La città misurata** (quello che solo questo progetto ha): dove si fermano i bus (3.1), puntualità (scheda 2), quanto ci si può fidare dei dati (3.4).
2. **Perché si prende l'auto**: tempi (scheda 4) → scelta del mezzo (3.2) → parcheggi di scambio (scheda 3) → pendolari ISTAT (3.5).
3. **Chi resta indietro**: servizi (scheda 1) → doppio svantaggio (scheda 5) → offerta e fragilità (3.6), la sera (3.7).
Più il «conto» (3.3) come ponte verso `PIANO_COSTI.md`.

## 5. Ordine proposto (da discutere)

| Quando | Cosa | Dove |
|---|---|---|
| subito (non tocca L3) | raccolta del Pi: `PIANO_RACCOLTA.md` passi 1, 2a, 3 | CLOUD → Leo |
| dopo L3 | problemi gravi delle schede 3-4 (`ANALISI_CRITICA.md` §1.1-1.3; giro G1 con i tempi Google in entrata) | Leo a mano + PC |
| dopo L3 | 3.2, 3.3, 3.4 (piccoli, dati già in git o nella Release) | CLOUD (script) → PC |
| dopo | 3.1 (medio, il più forte) e 3.6 | CLOUD → PC |
| metà novembre, con P8 | 3.8 (un mese di dati) | PC |
| più avanti | 3.5, 3.9, 3.10, 3.11 | — |

## 6. Domande per Leo
1. Quale delle tre storie del punto 4 ti interessa di più per il portfolio?
2. 3.1 «Dove si fermano i bus» è il risultato più originale: lo mettiamo come sesto risultato (o al posto di uno dei cinque)?
3. Vuoi chiedere a GTT o all'Agenzia i dati delle validazioni per linea? Se sì, preparo il testo della richiesta.
4. Treni: provare prima solo a misurare quanto pesano (prova piccola su 2-3 corridoi) o lasciarli fra i limiti?
