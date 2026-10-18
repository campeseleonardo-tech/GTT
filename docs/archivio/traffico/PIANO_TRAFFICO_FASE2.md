# Piano traffico veicolare — dalla Fase 2 in poi (scritto il 17/10/2026)

Seguito di `docs/PIANO_TRAFFICO_5T.md` (decisioni, metodi) e `docs/ESITO_FASE1_TRAFFICO_5T.md` (esito Fase 1).
Obiettivo (decisione di Leo): **traffico veicolare stimato su tutta la rete**, poi **incrocio con l'offerta di
trasporto pubblico** -> "vie con molto traffico e poco trasporto pubblico". Prima l'analisi, la mappa dopo.
Ogni valore non misurato porta l'etichetta [STIMATO].

## 0. Cosa ci hanno insegnato i test della Fase 1 (fatti, non interpretazioni)

- Dati utili: 6 giorni feriali (9 e 12-16/10). Sabato e domenica: celle "ok" = 0 (serve il fetch di lunedi' 19/10).
- Accuratezza 0 => flusso 0 **sempre, a tutte le ore** (colonna iii del Passo 2bis = 100%). Quindi "accuratezza 0"
  e "flusso 0" sono la stessa cosa nel dato: il test non separa "sensore rotto" da "nessun veicolo".
- Ora locale 1 (23 UTC): a ogni istante 68-73 sensori su 98 sono a zero (mai sotto il 69%, mai sopra il 75%) e solo
  31 sensori hanno letture affidabili in quell'ora. E' sempre lo stesso gruppo di ~67 sensori, ogni notte:
  e' un fenomeno del sistema, **non traffico**. Regola: ora 1 = DATO MANCANTE (non zero).
- Ore 2-4: la quota di zeri dipende dal traffico (correlazione -0,58; sensori poco trafficati 49% di zeri, molto
  trafficati 9,5%). Ma anche una strada da ~1000 veic/h di giorno ha il 9,5% di zeri di notte, e li' un vero zero in
  5 minuti e' improbabile. Quindi di notte gli zeri sono **un misto** di traffico basso e dati mancanti.
  Conseguenza: i flussi notturni calcolati scartando gli zeri sono probabilmente SOVRASTIMATI. Di giorno (6-22)
  gli zeri sono ~2%: li' il dato e' buono.
- Sensori da escludere: 11 "morti" (sempre accuratezza 0), 5 "bloccati" (stesso valore in tutte le 2231 letture:
  11436, 11437, 13703, 3851, 40191), 1 con troppe poche letture (11421). Totale 17, restano 92 usabili.
- **Scoperta del 17/10 (file XML grezzo del 3/10 e script 03):** i sensori fisici sono 112, ma il codice `lcd1` e' unico solo per 109: tre codici sono condivisi da due sensori diversi (40189: due punti di Corso Unita' d'Italia a ~800 m; 40123: uno morto e uno VIVO in Corso Regina Margherita; 13077: due punti di SS662). Il raccoglitore (script 03) salva flussi e accuratezza con `INSERT OR IGNORE` (vince il PRIMO della lista) e la posizione con `INSERT OR REPLACE` (vince l'ULTIMO): quindi per questi tre codici il flusso e la posizione possono venire da sensori diversi, e un sensore per codice (compreso un sensore vivo in Corso Regina Margherita) non viene mai registrato. Correzione del raccoglitore: decisione di Leo, vedi sezione 9.
- **Verso:** `positive`/`negative` e' il verso lungo la strada. Fuori Torino i sensori sono in coppia (stesso punto, due versi). A Torino quasi tutti sono `positive` e da soli: i 14 SICURO sono tutti un solo verso e nessuno ha il compagno. Quindi i flussi urbani sono **per un verso**, non per la strada intera.
- Solo 15 sensori (10 corridoi) sono abbinati a un corridoio per nome+posizione; 28 sensori hanno tutte le 24 ore;
  66 hanno 23 ore (manca sempre l'ora 1).

## 1. Decisioni prese (default dichiarati; Leo puo' cambiarli)

1. **Misure principali = di giorno.** (a) flusso in ora di punta (max sulle ore 7-9 e 16-19), (b) totale "diurno"
   = somma delle ore locali 6-21 (16 ore). Sono le misure dove il dato e' affidabile.
2. **Totale su 24 ore = stimato**: totale diurno diviso la quota diurna mediana misurata sui sensori con 24 ore ok
   (si riporta anche minimo-massimo della quota). Sempre [STIMATO].
3. Ora 1 = mancante; ore 0, 2-5 usate solo se la lettura e' affidabile e segnate "notte: probabile sovrastima".
4. Sensori esclusi: i 17 sopra, in un file (`data/processed/sensori_esclusi.json`) con il motivo.
5. Due versi della stessa strada: se ci sono due sensori (stesso nome, versi opposti, <= 200 m) si sommano e si scrive "due versi". Se c'e' un solo sensore (il caso di quasi tutta Torino) il valore resta "un verso"; per la **stima a due versi** si usa un sensore x 2, ma solo per il totale diurno (che e' circa simmetrico), mai per l'ora di punta (di mattina un verso e' piu' carico dell'altro). Sempre [STIMATO], con il flag `un_verso`.
6. Metodo B (estendere lungo la stessa strada): al massimo **1 km** dal sensore, finche' non abbiamo modo di
   validare meglio (quasi tutti i corridoi hanno un solo sensore, quindi la prova "nascondi un sensore" non
   puo' verificare B).
7. Criterio di riuscita del metodo C (IMQ): errore relativo mediano <= 35% nella prova "nascondi un sensore" **e**
   meglio del metodo A. Se non ci riesce: i numeri del C si presentano solo come **indice relativo**
   (alto/medio/basso), non come veicoli/ora.
8. Fino a nuovo ordine il traffico dei weekend non si stima (mancano i dati): solo feriale.

## 2. Regole per l'agente (valgono per tutti i passi)

- Cartella `C:\projects\Progetti\GTT`. Leggi AGENTS.md e MEMORIA_PROGETTO.md. Ramo `prova` (se non sei su `prova`, fermati).
- Nessun commit. Database in sola lettura. Non toccare `data/raw`, `data/storico_backup.sqlite`, `MEMORIA_PROGETTO.md`,
  `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`.
- Fase 2: solo libreria standard di Python. Fase 3: solo pacchetti gia' installati (r5py, geopandas, pandas, shapely, osmium);
  nessuna installazione senza chiedere a Leo.
- Dopo ogni passo scrivi in `docs/ESITO_FASE2_TRAFFICO.md` una riga `PASSO n: OK` oppure `PASSO n: FERMO - motivo`
  con i numeri attesi e trovati. Se un controllo non torna: fermati, scrivi i due valori, non cercare rimedi.
- Numeri nuovi nei file di dati: mai arrotondare senza dirlo; i valori stimati portano `"stimato": true`.
- Prima di ogni script lungo: PC libero da altri programmi (8 GB di RAM).

## 3. FASE 2 — metodi A e B con prova "nascondi un sensore" (script 35-37)

**Passo 7 — esclusioni e nuove misure.**
a) `scripts/35_sensori_esclusi.py` -> `data/processed/sensori_esclusi.json` (lista `{lcd1, nome, motivo}`) + `docs/RAPPORTO_SENSORI_ESCLUSI.txt`.
   Regole: "morto" = nel periodo 9-16/10 ha letture ma tutte con accuratezza 0; "bloccato" = fra le letture con accuratezza > 0 ha meno di
   20 coppie distinte (flusso, velocita') e almeno 500 letture; "pochi dati" = ha letture con accuratezza > 0 ma nessuna cella ok in `velocita_5t.json`.
   Controllo: morti 11 (urbani 3), bloccati 5 (i cinque nominati sopra), pochi dati 1 (11421): totale 17; sensori usabili 109 - 17 = 92.
b) Copia `scripts/33_flusso_sensori.py` in `scripts/33_flusso_sensori.py.bak_17ott` e modificalo (v2): legge `sensori_esclusi.json`,
   i sensori esclusi restano nel file con `"escluso": "<motivo>"` e NESSUN valore; per gli altri aggiungi `f_diurno` (somma ore locali 6-21,
   solo se tutte e 16 le ore sono ok, altrimenti null), `n_ore_diurne_ok`, `f_punta_am` (max ore 7-9), `f_punta_pm` (max ore 16-19),
   `quota_diurna` (f_diurno / totale_giorno, solo dove esiste totale_giorno). Nel rapporto: mediana, minimo, massimo di `quota_diurna`;
   `totale_giorno_stimato` = f_diurno / mediana(quota_diurna) con `"stimato": true`. L'ora 1 resta null.
   Controlli: (1) per i sensori non esclusi i valori orari sono identici a prima (confronta con la copia: nessuna differenza);
   (2) esclusi = 17; (3) nessun valore negativo; (4) scrivi quanti sensori hanno f_diurno (atteso: la maggior parte dei 92; se < 60 scrivilo come anomalia ma prosegui).
c) `--prova` prima del giro completo.

**Passo 8 — abbinamento sensore -> corridoio per posizione (script 36).**
`scripts/36_abbinamento_posizione.py` (riusa `normalizza` e `haversine_m` dallo script 24 via importlib, come lo script 34).
Per ognuno dei 92 sensori usabili: i 3 corridoi piu' vicini entro 60 m (nome, punteggio, distanza, `stesso_nome` si'/no).
Classe: SICURO (stesso nome, <= 60 m: la regola di prima), DA_VEDERE (nome diverso, <= 40 m), NESSUNO.
In piu': coppie di versi (sensori con stesso nome normalizzato, segno opposto, <= 200 m) e quali sensori restano senza compagno.
Output: `data/processed/sensori_corridoi_v2.json` + `docs/RAPPORTO_ABBINAMENTO_POSIZIONE.txt` con la tabella DA_VEDERE completa.
Controlli: SICURO circa 14-15 (erano 15, meno quelli esclusi); il totale delle tre classi = 92.
**Revisione di Claude (17/10, fatta):** `data/processed/abbinamenti_confermati.json` esiste. Confermati: 40212, 39977, 2375, 39983 (distanza <= 5 m, stessa strada con nome scritto in altro modo). In attesa di verifica: 35478, 35479, 36066, 36067, 35824 (distanza 21-27 m, nome diverso, strade provinciali). Nessun giudizio a occhio: lo decide il Passo 8b.

**Passo 8b — verifica con i dati OSM delle strade provinciali (script 38_verifica_provinciali.py, sola lettura).**
Per i 5 sensori in attesa piu' i 5 sensori `urbano` ma NESSUNO (35518, 35519, 35559, 35560, 35823): con pyosmium sul file `data/otp/rete/torino_cintura.osm.pbf` elenca le strade (tag `highway`) entro 60 m dalla posizione del sensore (da `sensori_5t`): nome, `ref`, tipo `highway`, distanza. Regola: un sensore `SPn(...)` e' CONFERMATO se una strada entro 60 m ha `ref` uguale a `SPn` (si ignorano spazi e maiuscole) **e** appartiene al corridoio proposto; altrimenti resta DUBBIO. Per i sensori NESSUNO con `ref` uguale ma senza corridoio: scrivi "strada senza nome nei corridoi" (nessun abbinamento). Output: `docs/RAPPORTO_VERIFICA_PROVINCIALI.txt` e aggiunta di un campo `verifica_osm` ai sensori nel file `data/processed/abbinamenti_confermati.json` (crea un nuovo file `abbinamenti_confermati_v2.json`, non sovrascrivere il vecchio). Se la coppia di versi ha esiti diversi, tieni il piu' prudente per entrambi.

**Passo 8c — codici sensore condivisi (sola lettura).**
(i) Leggi `data/raw/5t_flussi_20261003_224539.xml`: atteso 112 voci, 109 `lcd1` distinti, e questi tre codici doppi: 40123, 40189, 13077 (stampa le due voci di ciascuno: verso, offset, lat, lng, accuratezza). (ii) Nel database: per i tre codici stampa la riga di `sensori_5t` (nome, offset, lat, lng) e il numero di righe in `flussi_5t` per ogni `generato_utc` (atteso 1 per tutte). (iii) Segna nel file `sensori_corridoi_v2.json` e nei file del Passo 9 i tre codici con `"codice_condiviso": true`; 40189 resta usabile ma NON per il metodo B (la sua posizione non e' sicura), 40123 e 13077 restano esclusi se lo erano. NON modificare script 03 ne' il database. Se i numeri attesi non tornano, FERMATI.

**Passo 9 — metodi A e B e prova (script 37), dopo la revisione.**
`scripts/37_traffico_AB.py`. Grandezze: `f_punta_am`, `f_punta_pm`, `f_diurno`.
- Quantita' a due versi: `f_diurno_totale` = somma dei due versi se la coppia esiste; altrimenti `f_diurno` x 2 con `un_verso: true, stimato: true` (decisione 5). L'ora di punta si lascia per verso, senza moltiplicare.
- Unita' di calcolo: sensore (o coppia di versi sommata, decisione 5) abbinato a un corridoio SICURO o confermato.
- Metodo A: per gruppo (punteggio 3/4/5) x (dentro Torino / fuori Torino) = mediana, 10o e 90o percentile. Gruppo con meno di 3 sensori: "non stimabile".
- Metodo B: sul corridoio del sensore, i tratti entro 1 km (lungo la strada) prendono il valore del sensore, `"metodo": "B"`, `"stimato": true`.
- Prova "nascondi un sensore" per A: per ogni sensore, predizione = mediana del suo gruppo SENZA di lui; errore relativo = |pred - misurato| / misurato.
  Riporta per gruppo e in totale: n, errore relativo mediano, 90o percentile, distorsione media (segno).
- Prova per B: solo sui corridoi con almeno 2 sensori; tabella distanza fra i due sensori -> errore. Se i casi sono < 5, scrivi "non valutabile".
- Output: `data/processed/traffico_stimato_AB.json` (per corridoio: valori, metodo, gruppo, stimato) + `docs/RAPPORTO_TRAFFICO_AB.txt`.
- In piu': elenca le coppie di sensori sullo STESSO corridoio e stesso verso (es. Corso Francia 40021/40022, Corso Giulio Cesare 40040/40041, Corso Orbassano 40095/40097/40098): distanza fra i due e rapporto fra i loro `f_diurno`. E' l'unico modo per capire quanto cambia il traffico lungo una stessa strada (serve a decidere il limite di 1 km del metodo B).
Controlli: nessun sensore usato per predire se' stesso; nessun valore senza etichetta di metodo; tutti i corridoi senza stima elencati con il motivo.
Aspettativa onesta (da NON "correggere"): A sara' probabilmente impreciso (strade della stessa classe hanno traffici molto diversi).
Questo e' un risultato, non un errore: e' il motivo per cui serve il metodo C.

**Passo 10 — chiusura Fase 2.** Riepilogo in `docs/ESITO_FASE2_TRAFFICO.md` (numeri chiave, anomalie, file creati/modificati). Non aggiornare MEMORIA_PROGETTO.md.

## 4. FASE 3 — metodo C: la domanda IMQ assegnata alla rete (script 39 in poi)

Si fa **solo dopo** aver letto l'esito della Fase 2. Ci sono gia' gli strumenti: r5py, Java, `data/otp/rete/torino_cintura.osm.pbf`
(Torino + ~18 km), `imq_zone_geo.json`, `sezioni_torino.json` (6.916 sezioni con popolazione), `spostamenti.csv`.
Idea semplice: prendiamo i viaggi in auto (conducente) del campione IMQ, li facciamo "guidare" sul percorso piu' veloce,
contiamo quanti passano su ogni strada, e poi correggiamo la scala con i sensori.

- **3.0 Prova piccola** (nessun risultato): r5py in modalita' auto sulla rete tagliata; 200 coppie origine-destinazione tra zone;
  misura tempo e memoria (heap Java 3 GB); verifica che il percorso restituisca la geometria; scrivi se e' fattibile.
  **Cancello:** se non gira entro limiti ragionevoli (< 1 ora per l'insieme completo stimato, nessun crash), ci fermiamo e ne parliamo.
- **3.1 Domanda**: da `spostamenti.csv` i viaggi con "autoveicolo conducente" (codice 03), pesati con PESO, per fascia oraria di partenza
  (ore 7-8, 8-9, 17-18, 18-19 e il giorno). Controlli: totale auto-conducente ~4,18 milioni/giorno, ~0,97 milioni con un estremo a Torino
  (come nel rapporto IMQ). Conta anche quanti viaggi hanno un estremo **fuori dal taglio OSM**: da questo numero dipende la decisione sui "cancelli"
  di ingresso (autostrade e statali principali al bordo del taglio), da prendere con Leo.
- **3.2 Zone -> punti**: ogni zona rappresentata da piu' punti pesati con la popolazione (default 5 punti per quartiere di Torino,
  da sezioni; 1 punto per comune della cintura); i viaggi interni a una zona sono instradati fra punti diversi della stessa zona.
  Limite noto: 7 quartieri su 23 hanno confini del 1984 che non coincidono con la zonizzazione IMQ.
- **3.3 Instradamento e conteggio**: percorso piu' veloce per ogni coppia di punti (nessuna congestione, nessuna scelta di percorsi alternativi:
  limite dichiarato); i viaggi si sommano sui tratti di strada, poi si riportano ai corridoi (vicinanza <= 25 m). Output: veicoli/ora modello per corridoio.
- **3.4 Calibrazione**: confronto modello vs sensori (ora di punta e diurno) con un fattore di scala per classe di strada; la domanda IMQ non include
  merci, turisti, pendolari da fuori area: il fattore ne tiene conto in media, non strada per strada. Prova "nascondi un sensore" e confronto con il metodo A.
  Si applica il criterio di riuscita (decisione 7).
- **3.5 Esito**: `data/processed/traffico_stimato_C.json`, `docs/RAPPORTO_TRAFFICO_C.txt`, `docs/ESITO_FASE3_TRAFFICO.md`. Dove il sensore esiste vale il sensore
  (misurato); altrove il modello calibrato [STIMATO]; ogni tratto porta anche un livello di fiducia (alta: sensore sullo stesso corridoio; media: modello calibrato
  su strada simile; bassa: modello senza sensori simili).

## 5. FASE 4 — traffico x trasporto pubblico

- **4.0 Offerta TP per corridoio**: guardare prima se esiste gia' (passaggi di linee per via nei dati della mappa/accessibilita'); altrimenti calcolarla dal GTFS
  (`gtt_gtfs_*.zip`: tracciati delle linee bus e tram sui corridoi, passaggi per ora in un giorno feriale tipo). Metro e ferrovia a parte (non scorrono sulle strade).
- **4.1 Incrocio**: per ogni corridoio di Torino con stima di fiducia media o alta: coppia (veicoli/ora in punta, passaggi TP/ora in punta). Classi con soglie da
  decidere con Leo guardando la distribuzione (default: traffico >= 75o percentile e TP <= 25o percentile = "molto traffico e poco TP").
- **4.2 Controlli di buon senso**: la lista delle vie trovate va letta a occhio da Leo (ci sono parallele alla metro? sono tangenziali?). Le tangenziali e le autostrade
  si trattano in una classe a parte (il TP su gomma non le serve).
- **4.3 Esito** in un rapporto e in `data/processed/risultato8_traffico_tp.json`.

## 6. FASE 5 — dopo (non adesso)

- Mappa: strato "traffico" con etichetta [STIMATO] e fiducia (solo se richiesto da Leo).
- "Veicoli in meno" con IMQ come base (se si sposta una quota dei viaggi su altri mezzi).
- Weekend: dopo il fetch di lunedi' 19/10 le celle sabato/domenica avranno g=2 (10 e 17/10; 11 e 18/10).

## 7. Aggiornamento dei dati (ogni volta)

1. Doppio clic su `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat` (fa backup da leopi + rilancia lo script 26).
2. Poi in ordine: `python scripts\33_flusso_sensori.py`, `python scripts\35_sensori_esclusi.py`, `python scripts\36_abbinamento_posizione.py`,
   `python scripts\37_traffico_AB.py` (e dalla Fase 3 gli script del C).
3. **Dopo il 25/10 (fine ora legale)**: controllare a mano che le ore locali restino corrette (prova: una lettura delle 01:30 UTC del 26/10 deve cadere all'ora locale 2 o 1
   secondo la regola; scrivere il risultato). Il periodo prima del 25/10 e' UTC+2, dopo UTC+1.
4. Lunedi' 19/10 e' il primo fetch utile per sabato e domenica.

## 8. Decisioni aperte per Leo

1. **Correggere il raccoglitore** (script 03, anche sul Pi leopi) perche' registri i 112 sensori e non 109: la chiave diventerebbe `lcd1` + offset quando il codice e' condiviso (per i dati vecchi: 40189 -> primo punto, 40123 -> quello morto, 13077 -> primo). Guadagno: 2 sensori urbani vivi in piu' (40123 verso positivo, secondo punto di 40189). Rischio: si tocca la raccolta in corso; da provare prima su una copia. Consiglio: si', ma dopo l'esito della Fase 2.
2. Soglie di riuscita del metodo C (sezione 1, punto 7): con soli ~20 sensori utili l'errore stimato sara' molto incerto: i numeri vanno sempre letti insieme a "n".

## 9. Prompt per l'agente (Passi 8b, 8c, 9, 10)

```
Leggi AGENTS.md, MEMORIA_PROGETTO.md, docs/PIANO_TRAFFICO_5T.md, docs/ESITO_FASE1_TRAFFICO_5T.md, docs/PIANO_TRAFFICO_FASE2.md e docs/ESITO_FASE2_TRAFFICO.md.
I Passi 7 e 8 sono gia' fatti e rivisti da Claude (esiste data/processed/abbinamenti_confermati.json): non rifarli.
Esegui in ordine i Passi 8b, 8c, 9 e 10 della sezione 3 del piano docs/PIANO_TRAFFICO_FASE2.md, rispettando le regole della sezione 2.
Aggiungi l'esito in coda a docs/ESITO_FASE2_TRAFFICO.md con "PASSO n: OK" o "PASSO n: FERMO - motivo".
Se un controllo non torna (in particolare nel Passo 8c: 112 voci, 109 codici distinti, tre codici doppi), FERMATI e scrivi i due valori a confronto.
Nel Passo 9 non "migliorare" i risultati dei metodi A e B: se gli errori sono grandi, scrivili cosi' come sono.
Alla fine rispondi a Leo in massimo 8 righe: numeri chiave (sensori usati, errori della prova per A, coppie sullo stesso corridoio), anomalie, file creati o modificati.
```
