# Piano traffico veicolare — Fase 3: metodo C (domanda IMQ → rete) + correzione del raccoglitore

Scritto il 17/10/2026. Seguito di `docs/PIANO_TRAFFICO_5T.md` (decisioni di fondo), `docs/PIANO_TRAFFICO_FASE2.md`
(Fasi 1-2 e Fase 4) e degli esiti `docs/ESITO_FASE1_TRAFFICO_5T.md`, `docs/ESITO_FASE2_TRAFFICO.md`.
Questa fase va fatta **per intero** da un solo agente (con terminale sul PC di Leo). Il piano dice COSA ottenere, COME controllare
che sia giusto e quali sono i paletti; le scelte di realizzazione sono dell'agente, purché le documenti.

## 0. Perché serve il metodo C, e cosa abbiamo già

- I sensori 5T misurano bene, ma solo in pochi punti: 20 "unità" (sensore o coppia di versi) su 15 corridoi, su 10.743 corridoi.
- Metodo A (mediana per classe di strada): errore mediano 36,9% (n=16, 90° percentile 69%, peggiore 132%). Metodo B (estendere lungo la stessa strada):
  tra sensori sulla stessa strada l'errore va dal 7% all'84% (n=6) e non cala con la distanza. Quindi A e B non bastano: fuori dai punti misurati vanno
  stimati con un modello della **domanda**.
- Il modello: i viaggi in auto (conducente) dell'indagine IMQ 2022 vengono fatti "guidare" sul percorso più veloce della rete stradale; si contano i
  passaggi su ogni strada; i sensori servono per **tarare la scala** e per **controllare** quanto il modello ci azzecca.
- Limiti noti dell'IMQ da dichiarare in ogni uso: solo residenti 11-84 anni (niente merci, turisti, pendolari da fuori area), indagine telefonica a campione
  (le celle origine-destinazione fra due singole zone hanno quasi sempre meno di 30 interviste: i risultati regolari vengono dalla SOMMA di molte coppie),
  giorno feriale medio, anno 2022, confini dei quartieri di Torino del 1984 (7 su 23 non coincidono con la zonizzazione IMQ).
- Ingredienti già sul PC: `data/otp/rete/torino_cintura.osm.pbf` (OSM Torino + ~18 km, lon 7.45-7.93, lat 44.90-45.24), Java in `data/otp/jdk-25.0.4.1+1-jre`,
  r5py/geopandas/pandas/shapely/osmium (usati dallo script 18, che mostra come impostare R5 con heap 3 GB), `data/processed/imq/*.csv` (spostamenti, interviste,
  zone, comuni), `imq_zone_geo.json` (212 zone), `imq_zone.json` (zone → comuni ISTAT), `sezioni_torino.json` (sezioni di censimento con popolazione),
  `importanza_vie.json` (10.743 corridoi con `componenti`, `geometria`, `punteggio`), catalogo servizi (`data/processed/catalogo`, `servizi_osm_cintura.json`),
  scuole, attività commerciali, sedi amministrative, ospedali, università in `data/raw/*.zip` (zip da leggere senza estrarre nei raw),
  `traffico_stimato_AB.json`, `flusso_5t_sensori.json`, `sensori_corridoi_v2.json`, `abbinamenti_confermati_v2.json`.
- Colonne di `data/processed/imq/spostamenti.csv` (separatore `;`): LOTTO, SESSO, ATTIVITA, COD_CAMP, COD_DIM, PROGR_USC, PROGR_SPOST, SCOPO, COD_PAR, ORA_PAR (HH:MM),
  COD_ARR, ORA_ARR, USO_MEZZ, MEZZO1-3 (codice 03 = auto come conducente), PAX_AUTO, NUM_LIN_URB, COD_ALTROURB, ORA_2MEZZO, COD_2M, ORA_3MEZZO, COD_3M, PESO.
  Non c'è un identificativo di intervista (tolto per privacy): le righe consecutive con PROGR_SPOST crescente sono gli spostamenti della stessa persona.
  Tabella dei mezzi e degli scopi: `docs/RAPPORTO_IMQ.txt` e `scripts/14_prepara_imq.py`. Zone: Q001-Q023 (quartieri di Torino), altre C/E/R = comuni.

## 1. Criteri di riuscita (FISSATI PRIMA di vedere i risultati; non si cambiano dopo)

**Confronto.** Grandezza: totale diurno 6-21 a due versi (sensore a un solo verso ×2, coppia di versi = somma), stessa grandezza usata dal metodo A.
Unità: le 20 unità-sensore di `traffico_stimato_AB.json`, più quelle nuove se si sbloccano. La taratura (fattore o fattori di scala) si fa SENZA l'unità da
valutare ("nascondi un sensore", *leave-one-out*) e si predice l'unità tenuta fuori.

**Metriche (si riportano sempre con n e con un intervallo al 90% ottenuto per ricampionamento):**
1. errore relativo mediano e 90° percentile, `|previsto − misurato| / misurato`;
2. correlazione dei ranghi di Spearman ρ fra modello e misurato (sia sul modello grezzo, prima della taratura, sia sulle previsioni *leave-one-out*);
3. confronto con il metodo A sulle stesse unità (A: errore mediano 36,9%).

**Esito (per stima puntuale; se l'intervallo al 90% attraversa una soglia si scrive "incerto"):**
| Classe | Condizione | Cosa si pubblica |
|---|---|---|
| C-ASSOLUTO | errore mediano ≤ 35% **e** migliore di A **e** ρ ≥ 0,7 | veicoli/giorno e veicoli/ora [STIMATO] con fascia di errore (quantili dell'errore *leave-one-out*) |
| C-INDICE | ρ ≥ 0,7 ma errore > 35% o non migliore di A | solo un indice relativo (quintili 1-5) e rapporti fra strade, **niente veicoli/ora** |
| C-DEBOLE | 0,5 ≤ ρ < 0,7 | solo 3 classi (alto/medio/basso), marcate "debole"; Leo decide se tenerle |
| C-NO | ρ < 0,5 | nessuna stima pubblicata; si consegna il rapporto con la diagnosi e ci si ferma |

**Controlli di buon senso (non bloccanti, si riportano):** (a) l'ordine medio per classe di strada deve essere autostrada/tangenziale > arteria > strada locale;
(b) somma dei flussi del modello sulle strade che attraversano il confine di Torino confrontata con i sensori d'ingresso disponibili (rapporto atteso < 1,
perché l'IMQ non contiene merci e non residenti: se è > 1,3 c'è un errore da capire); (c) veicoli·km del modello contro viaggi·km attesi dalla domanda.

**Regole contro l'autoinganno:** (1) si esegue sempre la variante di base V0 (descritta ai pacchetti D-F) e se ne riportano i risultati; (2) si possono provare
altre varianti, ma al massimo 4 in tutto, riportandole **tutte** (non solo la migliore); (3) la variante finale è la più semplice che sta entro 5 punti di errore
mediano dalla migliore; (4) la classe di esito (tabella) è quella della variante finale; (5) con n≈20 le conclusioni vanno scritte con la dovuta cautela.

## 2. Regole per l'agente

**Fisse.**
- Cartella `C:\projects\Progetti\GTT`. Leggi `AGENTS.md`, `MEMORIA_PROGETTO.md` e i piani/esiti elencati sopra. Ramo `prova` (se non ci sei, fermati e dillo). **Nessun commit.**
- Database `data/storico_backup.sqlite` e `data/raw/` in sola lettura. Non modificare né sovrascrivere: `MEMORIA_PROGETTO.md`, `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`,
  i file di dati e gli script delle fasi precedenti (a meno che un pacchetto dica di farlo, e allora tieni una copia `.bak_17ott` dell'originale).
- Il Pi (leopi) è raggiungibile solo in lettura: **non scrivere né riavviare nulla sul Pi**. Per il pacchetto H prepari tutto e Leo lo avvia con un doppio clic.
- Python del PATH (3.14); NON usare Anaconda. Puoi installare con `pip install --user` pacchetti comuni (numpy, scipy, networkx, python-igraph, shapely, pyproj, ecc.) se servono;
  elencali in `docs/ESITO_FASE3_TRAFFICO.md` con la versione. Niente servizi esterni a pagamento né invio di dati all'esterno.
- PC con 8 GB di RAM: Java max 3 GB (come lo script 18), niente altri programmi pesanti. I calcoli lunghi si lanciano in una finestra `.bat` propria (log in `logs\`),
  **ripartibili** (salvano i risultati parziali ogni tot coppie e li riusano al rilancio), e li controlli leggendo il log.
- Prova su un campione piccolo prima di ogni giro lungo. Numeri nuovi nei file: valori stimati con `"stimato": true`; niente arrotondamenti nascosti.
- Per ogni pacchetto: script numerati da 39 in poi (`scripts/39_...py`), rapporto `docs/RAPPORTO_TRAFFICO_C_<pacchetto>.txt` quando utile, e una riga `PASSO <pacchetto>: OK` oppure
  `PASSO <pacchetto>: FERMO - motivo` in `docs/ESITO_FASE3_TRAFFICO.md`.

**Libertà.** Scegli tu motore di instradamento (r5py in modalità auto, oppure un grafo tuo costruito dall'OSM con networkx/igraph/scipy se è più veloce o più controllabile),
modo di rappresentare le zone, numero di punti per zona, uso di percorsi alternativi, velocità e rallentamenti nelle ore di punta, forma della taratura, analisi extra. Se un'idea
del piano si rivela sbagliata o impraticabile, cambiala e spiega perché (in "Decisioni dell'agente" nell'esito).

**Ti devi fermare e scrivere a Leo solo se:** (1) la prova di fattibilità A fallisce (non gira, o la stima del giro completo supera 8 ore, anche dopo la riduzione dei punti); (2) l'esito è
C-NO; (3) un controllo di coerenza della domanda (pacchetto B) differisce di oltre 5% dai totali di riferimento e non sai spiegarlo; (4) servirebbe qualcosa che il piano vieta
(scrivere sul Pi, committare, modificare i raw); (5) finisce lo spazio su disco (< 5 GB liberi) o il PC va in blocco due volte per la memoria. In tutti gli altri casi vai avanti
con il default più ragionevole e annotalo.

## 3. Pacchetto A — Prova di fattibilità (gate)

1. Verifica Java, r5py/geopandas, spazio disco (`data/` + `logs/`), RAM libera.
2. Costruisci la rete stradale dal `torino_cintura.osm.pbf` e instrada 200 coppie fra punti sparsi (centro, quartieri, cintura, bordi) in modalità auto. Misura tempo per coppia, picco di memoria,
   se il risultato dà il **tracciato** (geometria) e come riportare il tracciato sui tratti OSM / sui corridoi.
3. Scegli il motore. Stima il tempo del giro completo (numero di coppie dei pacchetti B-C × tempo per coppia). Se > 8 ore: riduci i punti per zona, usa la matrice per nodi o un grafo tuo.
4. Controlli: 10 percorsi a campione confrontati a occhio sulle coordinate (inizio, fine, lunghezza plausibile, passaggio su strade note come tangenziale e Corso Francia);
   tempi di viaggio plausibili (es. centro → Collegno in auto 20-35 minuti).
Esito nel file: motore scelto, tempo stimato, memoria, rischi.

## 4. Pacchetto B — Domanda IMQ (script 39-40)

Obiettivo: tabella dei viaggi in auto per **coppia di zone × ora di partenza** (giorno feriale medio), in viaggi/giorno pesati.
- Viaggi "auto conducente": quelli in cui MEZZO1-3 contiene 03. Conta e documenta come tratti i viaggi misti (auto + treno/bus/altro): di default tieni solo quelli dove 03 è l'unico mezzo
  motorizzato e scrivi quanti viaggi e quanti pesi lasci fuori e perché (se > 8% valuta un trattamento diverso, ad esempio tenere il tratto auto fino alla stazione quando la stazione è nota).
- Peso `PESO` (somma = viaggi/giorno). Ora = ora di partenza (`ORA_PAR`), fascia oraria locale. Se un viaggio dura più di un'ora puoi distribuirlo sulle ore di passaggio (facoltativo).
- Origine/destinazione = zone `COD_PAR`/`COD_ARR`. Viaggi con un estremo fuori dalle 212 zone (campo vuoto) → "esterno non localizzato": conta e tratta come gli esterni del pacchetto C.
- Controlli (tolleranza 5%): somma pesata dei viaggi auto-conducente ≈ 4,18 milioni/giorno (50,9% di 8.217.863); con almeno un estremo in una zona di Torino ≈ 0,97 milioni; picchi
  7-8 e 16-18 come nel rapporto IMQ; totale per macroarea coerente con `imq_od.json`. Riporta anche quanti viaggi hanno OD in zone con meno di 30 interviste (per celle e per peso).
- Output: `data/processed/traffico_c/domanda_auto.json` (o csv) con n interviste non pesate, somma pesi, per coppia zona-zona × ora; `docs/RAPPORTO_TRAFFICO_C_DOMANDA.txt`.

## 5. Pacchetto C — Dalle zone ai punti, e le "porte" (script 41)

Il modello deve far partire e arrivare i viaggi da **punti** della rete, non da un unico centro per zona (altrimenti le strade locali non vengono mai usate e i viaggi interni a una zona sparirebbero).
- Origine e destinazione di un viaggio non hanno gli stessi pesi: **a casa** (ritorno a casa, partenza dalla propria abitazione) → pesi di popolazione (sezioni di censimento; per i comuni della
  cintura le sezioni disponibili, altrimenti centroide del comune/residenziale OSM); **a lavoro / scuola / acquisti / altro** → pesi di attrattori coerenti con lo scopo (attività commerciali, sedi e uffici,
  scuole, università, ospedali, servizi OSM della cintura; per "lavoro" in mancanza di meglio un mix di attività commerciali, uffici e servizi). Lo scopo è in `SCOPO`; l'origine di un viaggio non domestico si può
  ricostruire dallo scopo del viaggio precedente della stessa persona (righe consecutive, `PROGR_SPOST`). Variante di base V0: usa popolazione per gli estremi domestici e una miscela unica di attrattori per gli altri; le
  raffinature per scopo sono varianti (regola dei max 4).
- Rappresenta ogni zona con un numero limitato di punti pesati (per i quartieri di Torino di solito 5-15, 1-3 per i comuni piccoli; decidi in base al tempo stimato nel pacchetto A), agganciati al nodo stradale
  percorribile in auto più vicino (non una strada pedonale, non un nodo isolato; come fa lo script 18 con SEZIONI_FUORI_RETE). I viaggi interni a una zona vanno instradati fra punti **diversi** della stessa zona.
- **Zone fuori dal taglio OSM** (comuni lontani, altre province): i loro viaggi entrano ed escono dall'area attraverso una **porta**. Trova da OSM le strade di rango ≥ secondary che attraversano il bordo del taglio
  (autostrade e tangenziali comprese); assegna ogni zona esterna a una o più porte secondo la direzione (azimut) e il rango (preferenza alle autostrade per le distanze lunghe). Dove ci sono sensori 5T vicino alle porte
  usali per orientare le quote (facoltativo). Conta quanti viaggi sono interessati (se sono pochi, anche una regola semplice va bene).
- Limite da dichiarare: **traffico di attraversamento, merci e non residenti non sono nell'IMQ**: il modello sottostima soprattutto tangenziali, autostrade e radiali d'ingresso. La taratura per classe di strada lo
  corregge in media, non strada per strada.
- Sensibilità sui 7 quartieri con confini 1984 non allineati (Cenisia, Mirafiori Sud, Barriera di Milano, Falchera, Regio Parco, Centro, San Paolo): una prova dove i punti dei quartieri vicini sono scambiati/uniti, per
  vedere quanto cambia il risultato (variante facoltativa).
- Output: `data/processed/traffico_c/punti.json` (zona, punto, nodo, peso, tipo), `.../porte.json`, rapporto.

## 6. Pacchetto D — Instradamento (script 42)

- Per ogni coppia di punti con domanda: percorso più veloce in auto (tempo da velocità OSM `maxspeed`/classe; r5py o grafo proprio). Variante di base V0: **tutto o niente** (un solo percorso per coppia),
  senza rallentamenti da traffico, uno schema unico per tutte le ore (le ore si ottengono con le quote orarie della domanda).
- Possibili varianti (a tua scelta, nei limiti delle 4): percorsi stocastici (costi dei tratti perturbati del ±10-20% su più repliche e flussi mediati) per spargere il traffico su più itinerari;
  velocità ridotte in punta con il rapporto fra velocità 5T d'ora e di notte per classe di strada (`velocita_5t.json`); penalità per i semafori/incroci.
- Va a lotti, salva tutto in `data/processed/traffico_c/instradamenti/`, riparte da dove era arrivato. Alla fine controlla: ogni coppia con domanda ha un percorso o è nell'elenco dei non raggiungibili
  (con motivo e peso perso, atteso < 1%).
- Controlli indipendenti (obbligatori): ricalcola con un altro metodo (altro motore o `networkx` sullo stesso grafo) almeno 20 coppie scelte a caso e confronta lunghezza e tempo (tolleranza 2%); somma
  `viaggi × lunghezza percorso` = veicoli·km del modello (riportalo).

## 7. Pacchetto E — Dai percorsi alle strade (script 43)

- Somma i viaggi sui **tratti** (segmenti OSM fra due incroci), per verso e per ora (almeno: 6-21 diurno, 7-8, 8-9, 17-18, 18-19 e il giorno intero). Poi riporta ai **corridoi** di `importanza_vie.json`: il
  campo `componenti` di ogni corridoio dice di quali vie/tratti è fatto (rileggi lo script 24 per sapere come); usa quella corrispondenza, e solo se manca usa la vicinanza (≤ 25 m e stessa strada).
- Output: `data/processed/traffico_c/segmenti.*` (un record per tratto: id, corridoio, lunghezza, flusso modello verso A/B per ora, rango OSM) — il formato lo scegli tu, ma deve essere leggibile da Python senza
  librerie speciali (csv o json) — e `data/processed/traffico_c/corridoi_modello.json` (per corridoio: flusso modello medio pesato per lunghezza, minimo e massimo, flusso sul tratto più vicino al sensore).
- Controlli: conservazione del flusso (nei nodi interni, ingresso ≈ uscita; l'errore entro 1%); nessun flusso negativo; corridoi senza flusso elencati con il motivo (strade pedonali, senza collegamento in auto…).

## 8. Pacchetto F — Taratura e validazione (script 44)

- Unità di confronto come in sezione 1. Il tratto del modello da confrontare con un sensore è il tratto di corridoio più vicino al sensore (≤ 30 m dal suo punto; per i codici condivisi, la posizione del
  sensore "primo punto"); se il sensore è a un solo verso, confronta con lo stesso verso se riesci a stabilirlo (dalla geometria dell'offset del sensore e dal profilo mattina/sera rispetto al centro: radiale in
  entrata al mattino), altrimenti confronta il totale dei due versi del modello con sensore ×2 (per il totale diurno, che è circa simmetrico).
- Taratura V0: un solo fattore globale k = Σ misurato / Σ modello (regressione per l'origine sul totale diurno, con pesi uguali per unità). Varianti: k per classe (autostrada/tangenziale; arteria; locale), oppure
  `misurato = a · modello^b`. Con n≈20 non usare più di 2-3 parametri.
- Produci per ogni variante: tabella unità × (misurato, modello grezzo, previsto *leave-one-out*, errore), le metriche della sezione 1 con intervalli, il confronto con A. Analizza i residui: quali sensori sono più
  lontani e perché (corsie non coperte, sensore vicino a un incrocio, quartiere con confini disallineati, strada soggetta ad attraversamento).
- Ripeti l'analisi per l'ora di punta del mattino e della sera **solo se** riesci a stabilire il verso dei sensori; altrimenti scrivilo e basta.
- Applica la regola di classificazione della sezione 1 e scrivi la classe finale, ripetendo i criteri parola per parola nel rapporto.
- Controlli indipendenti: ricalcola a mano (con un altro script o in un foglio) il fattore k e l'errore leave-one-out di 3 unità e confrontali.

## 9. Pacchetto G — Prodotto finale e rapporto (script 45)

Per ogni corridoio (e per ogni tratto) un record con: valore misurato dove c'è un sensore (con `misurato: true`, `fonte: sensore`), valore del modello tarato altrove (`stimato: true`, `fonte: modello C`, classe di esito),
**livello di fiducia**: alta = sensore sullo stesso corridoio entro 300 m; media = modello tarato e la classe di esito è C-ASSOLUTO o C-INDICE e nel corridoio il flusso modello non è sotto il 5% del suo massimo (il
modello è sensibile); bassa = altro. Facoltativo (con test *leave-one-out*): correzione locale vicino ai sensori (fattore residuo che decade con la distanza, con tetto di 1 km come il metodo B) — adottala solo se
migliora le metriche.
- Campi per la pubblicazione, secondo la classe: C-ASSOLUTO → `veic_diurno_2versi`, `veic_ora_punta_am/pm` se disponibili, fascia di errore; C-INDICE → `indice` 1-5 e `rapporto_su_mediana_torino`; C-DEBOLE → `classe3`; C-NO → nulla.
- File: `data/processed/traffico_stimato_finale.json` e `docs/RAPPORTO_TRAFFICO_C.txt` con: criteri e risultato della prova, tabella delle unità, i 30 corridoi di Torino con più traffico, le 10 sorprese rispetto
  al senso comune (strade che il modello mette molto più alte o basse di quanto ci si aspetti) con una spiegazione plausibile o "da indagare", elenco dei limiti. Un'etichetta [STIMATO] su ogni valore del modello.
- Non produrre mappe in questa fase (Leo: l'analisi prima, la visualizzazione dopo). Un grafico semplice di controllo (misurato vs previsto) in `docs/` è invece benvenuto, se utile alla spiegazione.

## 10. Pacchetto H — Correzione del raccoglitore sul Pi (script 46)

**Problema (verificato sul file XML grezzo del 3/10 e su `scripts/03_raccolta_continua.py`):** i sensori fisici sono 112 ma tre codici `lcd1` sono condivisi da due sensori: 40123 (uno morto in Corso Regina Margherita,
uno vivo a 45.086797,7.653109), 40189 (due punti di Corso Unità d'Italia a circa 800 m), 13077 (due punti di SS662). Lo script 03 salva `flussi_5t` e `accuratezza_5t` con `INSERT OR IGNORE` (vince la PRIMA voce
del file) e `sensori_5t` con `INSERT OR REPLACE` (vince l'ULTIMA): i dati sono del primo sensore, la posizione è dell'ultimo, il secondo non esiste.

Cosa fare (l'agente prepara, Leo avvia):
1. **Verifica.** Rileggi il XML (`data/raw/5t_flussi_20261003_224539.xml`); scarica un XML fresco dal feed aperto 5T con lo stesso metodo dello script 03/01 (sola lettura) e conferma i duplicati di oggi (stessi
   tre? di più? stesso ordine?). Controlla nel database, per un istante già presente (quello del 3/10 22:45:03Z se c'è), che per 40189 e 40123 siano stati salvati i valori della **prima** voce (flusso 1212 / accuratezza 0)
   e non della seconda. Se non è così, fermati a descrivere cosa trovi.
2. **Regola degli identificativi.** Nuovo identificativo del sensore: la prima voce di un `lcd1` (in ordine di apparizione nel documento) mantiene `lcd1` identico (così i dati storici restano valide e continue); la seconda e le
   successive diventano `lcd1~2`, `lcd1~3`… (esempio: `40189~2`). Per i tre casi noti verifica che la regola assegni il "primo" al punto con offset 160 (40189), 1555 (40123), 4960 (13077); se l'ordine del feed cambiasse, la
   regola deve usare questa tabella come àncora, e segnalare nei log ogni duplicato non previsto. Non cambiare lo schema delle tabelle.
3. **Patch dello script 03** (copia di sicurezza `scripts/03_raccolta_continua.py.bak_17ott`): applica la regola in `salva_5t_da_bytes` per `sensori_5t`, `accuratezza_5t`, `flussi_5t`; log di una riga se trovi duplicati. Nessun altro
   comportamento cambia (parcheggi, ZTL, mezzi, accuratezza).
4. **Controllo di tutto ciò che legge i sensori** (`grep` su `scripts/`: 04, 06, 09, 26, 33-38b, backup_da_leopi, check_backup, supervisore): devono funzionare con identificativi del tipo `40189~2` (stringhe), senza cambiare i
   risultati sui dati storici. Prova prima/dopo: rilancia 26 e 33 sul database attuale e verifica che le uscite siano identiche (tolleranza zero). Se serve, adatta gli script tenendo `.bak_17ott`.
5. **Prova su una copia.** Crea un database vuoto con lo stesso schema (non usare il 1,6 GB) e applica la funzione patchata: al primo giro con il XML del 3/10 devono risultare 112 righe in `sensori_5t`, 112 in `flussi_5t`, 112 in
   `accuratezza_5t`, con i 3 identificativi `~2`; al secondo giro con lo stesso XML 0 righe nuove (idempotente); e un secondo XML (modificato a mano) con un duplicato in più deve produrre l'identificativo `~3` e il log.
6. **Consegne per Leo.** `scripts/AGGIORNA_RACCOLTA_5T_CODICI.bat` (doppio clic, modellato su `scripts/aggiorna_raccolta_leopi.bat`: copia di sicurezza sul Pi `.bak_pre_codici`, invio dello script, `py_compile`, riavvio di
   `gtt-raccolta`, attesa, controllo) e `scripts/controlla_raccolta_5t.py` (eseguito sul Pi via ssh: stampa quanti sensori ci sono nell'ultimo istante e se i tre `~2` hanno dati; "112 e 3/3" = giusto). Il `.bat` deve scrivere
   in chiaro cosa Leo deve vedere alla fine. Scrivi nell'esito la procedura in 3 righe e il modo di tornare indietro (ripristino del `.bak_pre_codici` sul Pi).
7. **Dopo l'avvio.** I nuovi sensori (`40123` vivo ora come `40123~2`, `40189~2`, `13077~2`) avranno dati utilizzabili dopo ~6 giorni feriali. Predisponi la pipeline (script 33-37, 44) perché li includa da sola quando ci sono
   (celle ok) e documenta in `docs/ESITO_FASE3_TRAFFICO.md` quando rilanciare. Prima dell'avvio la pipeline deve restare identica.

## 11. Pacchetto I — Rilancio ripetibile (script/bat)

- `scripts/TRAFFICO_RILANCIA_SENSORI.bat`: dopo ogni fetch dei dati da leopi esegue in ordine 26, 33, 35, 36, 38b, 37, 44, 45 (la taratura e il prodotto finale con i dati nuovi), senza ripetere il calcolo pesante dei percorsi (che
  non dipende dai sensori e resta in cache). Registra il log e stampa a Leo 5 righe di numeri chiave.
- `scripts/TRAFFICO_RICALCOLA_MODELLO.bat`: ripete i pacchetti B-E (solo se cambiano rete OSM, IMQ o regole). Avviso chiaro che dura ore.
- Promemoria nell'esito: dopo il **25/10** finisce l'ora legale (UTC+1): controlla a mano che le ore locali dello script 26 siano corrette per le letture dopo il cambio (prova su una lettura delle 01:30 UTC del 26/10).
  Il primo fetch utile per sabato e domenica è lunedì 19/10 (10 e 17/10 sabati, 11 e 18/10 domeniche): con due giorni per tipo le celle weekend diventano "ok"; i metodi in questa fase restano per il feriale e il weekend
  può essere aggiunto dopo con lo stesso schema.

## 12. Verifiche indipendenti da fare prima di chiudere

1. Totali della domanda (4,18 M; 0,97 M) e quote orarie ricalcolati con una lettura diretta del csv in un altro modo (es. awk/pandas vs csv) — stessi numeri.
2. 20 percorsi ricalcolati con un secondo metodo (sezione 6).
3. Conservazione del flusso, veicoli·km (sezione 7).
4. Fattore k e 3 errori *leave-one-out* ricalcolati a mano (sezione 8).
5. Nessun valore del modello senza `stimato: true`; nessuna unità-sensore esclusa (i 17 di `sensori_esclusi.json`) usata per tarare.
6. Il prodotto finale riletto da zero: 5 corridoi a caso, dai dati grezzi al valore finale, senza errori.
7. Elenco dei file toccati confrontato con `git status` (nessun file vietato modificato; nessun commit).

## 13. Consegne

`docs/ESITO_FASE3_TRAFFICO.md` con: esito di ogni pacchetto, "Decisioni dell'agente" (cosa è stato scelto e perché, alternative provate e loro effetto sui criteri), numeri chiave, anomalie, pacchetti
installati, durate, file creati/modificati, il **testo proposto** per l'aggiornamento di `MEMORIA_PROGETTO.md` (non modificarla tu), la procedura per Leo per l'avvio del raccoglitore (pacchetto H) e il
suggerimento del passo successivo (Fase 4: incrocio con il trasporto pubblico, `docs/PIANO_TRAFFICO_FASE2.md` sezione 5).
Rapporti: `RAPPORTO_TRAFFICO_C_DOMANDA.txt`, `RAPPORTO_TRAFFICO_C.txt` e quelli dei pacchetti.

## 14. Prompt per l'agente (da incollare tutto, una volta sola)

```
Sei l'agente che esegue la Fase 3 del Risultato 8 (traffico veicolare) del progetto GTT di Leo, sul PC di Leo, cartella C:\projects\Progetti\GTT.

Prima di tutto leggi: AGENTS.md, MEMORIA_PROGETTO.md, docs/PIANO_TRAFFICO_5T.md, docs/PIANO_TRAFFICO_FASE2.md, docs/ESITO_FASE1_TRAFFICO_5T.md,
docs/ESITO_FASE2_TRAFFICO.md e soprattutto docs/PIANO_TRAFFICO_FASE3.md (il tuo piano). Controlla di essere sul ramo "prova"; se no, fermati.

Obiettivo: stimare il traffico veicolare su tutta la rete stradale di Torino e cintura con il metodo C descritto nel piano (domanda auto IMQ 2022 instradata sulla rete OSM e
tarata sui sensori 5T), validarlo con i criteri FISSATI nella sezione 1 del piano (non cambiarli), preparare la correzione del raccoglitore dei sensori sul Raspberry Pi
(pacchetto H) e lasciare tutto rilanciabile (pacchetto I).

Esegui i pacchetti A, B, C, D, E, F, G, H, I del piano, in questo ordine. Hai libertà sulle scelte di realizzazione (motore di instradamento, punti per zona, varianti, taratura),
nei limiti dei paletti della sezione 2 e della regola "massimo 4 varianti, riportale tutte". Documenta ogni scelta in docs/ESITO_FASE3_TRAFFICO.md ("Decisioni dell'agente").

Paletti che valgono sempre: nessun commit; database storico e data/raw in sola lettura; non scrivere né riavviare nulla sul Pi (per il pacchetto H prepari script, .bat e controlli e Leo li avvia
con un doppio clic); non modificare MEMORIA_PROGETTO.md, scripts/mappa_template.html, scripts/04_genera_mappa.py; copia .bak_17ott prima di cambiare qualunque script o file esistente;
calcoli lunghi in una finestra .bat propria, ripartibili, con log; prova su campione piccolo prima del giro lungo; PC con 8 GB di RAM (Java max 3 GB). Puoi installare pacchetti Python comuni
con pip --user (annotali); niente servizi esterni.

Fermati e scrivi a Leo SOLO se: la prova di fattibilita' (pacchetto A) fallisce o il giro completo stimato supera 8 ore anche riducendo i punti; l'esito di validazione e' C-NO; un controllo di coerenza
della domanda differisce di oltre il 5% dai totali di riferimento e non lo sai spiegare; serve qualcosa che il piano vieta; finisce lo spazio su disco o il PC si blocca due volte. In ogni altro caso vai
avanti con il default piu' ragionevole e annotalo. Leo potrebbe non essere presente: non aspettare risposte per scelte che il piano ti lascia.

Scrivi per ogni pacchetto una riga "PASSO <lettera>: OK" oppure "PASSO <lettera>: FERMO - motivo" (con numeri attesi e trovati) in docs/ESITO_FASE3_TRAFFICO.md. Fai le verifiche indipendenti della sezione 12
prima di chiudere. Non cercare di "far uscire" un buon risultato: se il modello e' debole, scrivilo con i numeri.

Risposta finale a Leo (massimo 12 righe): classe di esito (C-ASSOLUTO / C-INDICE / C-DEBOLE / C-NO) con errore mediano, rho di Spearman, n e intervalli; confronto con il metodo A; numero di corridoi con stima e quanti
con fiducia alta/media/bassa; i 5 corridoi di Torino con piu' traffico stimato; stato del pacchetto H (cosa deve fare Leo con il .bat, e cosa deve vedere); anomalie; durata; file principali creati o modificati.
```
