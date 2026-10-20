# Piano — Risultato 4: puntualità e attese dei mezzi GTT [MISURATO] (con dentro l'ex Risultato 9)

Piano unico del risultato. In testa stato, decisioni e lavori; sotto la storia del Risultato 4 (parte A) e il
piano dell'ex Risultato 9 (parte B, prima `docs/PIANO_RISULTATO9_ATTESA.md`). Aggiornato da Claude il 20/10/2026
dopo l'analisi di Leo. **Nessuna modifica fatta al risultato**: è un piano.

## Stato attuale

- **Ritardi e irregolarità** (v2, 18/10, script 27): feriale 5,3% dei passaggi in ritardo oltre 5 minuti, 10,5% di
  coppie a grappolo o con buco sulle linee frequenti; dati 10-18/10. Rapporto `docs/RAPPORTO_RISULTATO4.txt`.
- **Attesa reale** (ex R9, v1, 18/10, script 70 che riusa il 27): sulle linee frequenti l'attesa promessa è 4,8
  minuti, quella reale 5,4-6,2 (0,6-1,5 in più). Rapporto `docs/RAPPORTO_RISULTATO9_ATTESA.txt`.
- Oggi sono due schede separate (R4 e R9) in `simulazione.html`.
- Problema trovato il 20/10: in cima alle «10 linee peggiori per ritardo» ci sono servizi speciali con poche
  corse (RV2 2.226 passaggi, VEX 276, LS1 333, 68+ 1.612) davanti a linee vere come la 17 (21.483 passaggi).

## Commenti di Leo (20/10) e fattibilità

| Commento | Cosa c'è già | Lavoro |
|---|---|---|
| R4 è semplice e pulito | — | — |
| **Pulsante** dalle linee peggiori alla **mappa con quella linea selezionata** (per vedere che giro fa) | La mappa ha già il campo «Mostra solo una linea» (`#filtroLinea`) e si apre già da indirizzo per tema (`#tema=…`) | Piccolo: leggere `#linea=17` dall'indirizzo e riempire il filtro; nella scheda un link per ogni linea della classifica |
| **Ritardo per km** della linea (se la tratta è lunghissima) | Lunghezza delle linee calcolabile dal GTFS (percorsi `shapes` o somma delle distanze fra fermate) | Piccolo-medio: una colonna nella classifica; attenzione, il ritardo cresce lungo la corsa, quindi meglio «ritardo a fine corsa / km» o «ritardo medio per fermata» |
| Linee che passano da **zone affollate** | Abitanti per sezione e spostamenti per zona IMQ già pronti | Medio: si appoggia alla «popolarità» delle zone (misura comune, vedi `docs/PIANO_RISULTATO6.md`) |
| **Bus contro tram** (ritardi, irregolarità) | Il GTFS distingue tram e bus (tipo di linea); i dati del 27 sono per linea | Piccolo: due righe in più (tram / bus) in tutte le tabelle |
| Bus contro tram: **efficienza, efficacia, costo** (solo idea) | Dal rapporto GTT 2025: passeggeri per modo (bus urbani 183,7 M, tram 52,7 M), flotta (819 bus, 180 tram), vetture-km totali (non per modo). Costi per modo: **non ci sono** | Solo idea: passeggeri per vettura sì; costi no senza una fonte nuova (si lega a `docs/PIANO_COSTI.md`) |
| **Accorpare R9 a R4** | Stessi dati, il 70 riusa il 27 | Piccolo: una scheda con due parti |

## Decisioni di Leo (20/10)

1. **Una sola scheda «Puntualità e attese»** (numero 4) con due parti: ritardi e irregolarità; attesa reale contro
   promessa. R9 smette di esistere come numero a sé (gli script 27 e 70 restano).
2. Nelle classifiche **solo linee ordinarie con almeno 2.000 passaggi** (default); i servizi speciali in una riga a
   parte.
3. Tutte le aggiunte qui sopra vanno nel piano come lavori, nell'ordine della tabella che segue.

**Come eseguirli**: i lavori 1-2 sono nel **Giro 1** (`docs/PIANO_GIRO1_RITOCCHI.md`), con il prompt pronto.
Gli altri si preparano dopo, uno per volta, con un prompt nello stesso stile.

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Classifiche: solo linee ordinarie (≥ 2.000 passaggi; regola per riconoscere le speciali da fissare guardando l'elenco: lettere nel nome, poche corse) | 27, 70 | piccolo |
| 2 | Una scheda con due parti; toglierne una dall'elenco; testo inglese unico; nelle fonti della scheda il piano diventa `docs/PIANO_RISULTATO4.md` (oggi cita ancora `PIANO_RISULTATO9_ATTESA.md`, spostato in archivio) | `schede_risultati.py` | piccolo |
| 3 | Tram contro bus in ogni tabella | 27, 70 | piccolo |
| 4 | Link linea → mappa (`#linea=`) | `mappa_template.html`, scheda | piccolo |
| 5 | Ritardo per km (o a fine corsa) | 27 | piccolo-medio |
| 6 | Rilancio con un mese di dati (metà novembre): 27, poi 70, poi schede | `.bat` | — |
| 7 | R4 in mappa: linee colorate per ritardo, con lo slider dell'ora | 04, template | medio |
| 8 | Linee e zone affollate (dopo la «popolarità» delle zone) | — | medio |
| 9 | Controllo con la realtà: il rapporto GTT 2025 dichiara il 2,3% di passaggi bus/tram in ritardo oltre 10 minuti; noi misuriamo oltre 5 minuti: calcolare anche oltre 10 e confrontare | 27 | piccolo |
| — | Solo idea: efficienza e costo bus contro tram | — | serve una fonte sui costi |

## Giro 2 del Risultato 4 — tutti i lavori fattibili con i dati di oggi (piano del 20/10 sera)

Lavori dentro: **3** tram contro bus, **4** link linea → mappa, **5** ritardo per km, **7** R4 in mappa, **8** linee
utili (zone affollate), **9** oltre 10 minuti contro GTT. Fuori: **6** (rilancio con un mese di dati, metà novembre:
basterà rilanciare 27, 70, 04 e schede) e l'idea dei costi (manca la fonte).

### Scelte (valori predefiniti di Claude, dichiarati)
- **Modo della linea** dal GTFS (`route_type` di `routes.txt`): `0` tram, `1` metro, altro bus. La metro di solito non
  è nel feed: se ha dati, terza riga.
- **Oltre 10 minuti**: stessa misura del rapporto GTT 2025 (2,3% dei passaggi bus e tram in ritardo oltre 10 minuti,
  tutto l'anno; `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`, riga 40). Il 2,3% è l'unico numero scritto a mano: una
  costante con la fonte nel commento. Il confronto si scrive come «ordine di grandezza» (anno intero contro pochi
  giorni di ottobre; tutte le linee contro le ~90 urbane del feed).
- **Ritardo per km**: il ritardo cresce lungo la corsa, quindi si usa il **ritardo a fine corsa** (passaggi alle ultime
  3 fermate della corsa) diviso la **lunghezza della corsa** (somma delle distanze in linea d'aria fra fermate
  consecutive del GTFS). Misura: minuti di ritardo ogni 10 km (mediana). Classifica solo linee ordinarie con almeno
  100 passaggi di fine corsa.
- **Linee utili** = le 54 dello script 87 (`data/processed/popolarita_zone.json`): una riga «linee utili contro
  altre» per % in ritardo e grappolo+buco (feriale), pesata per passaggi.
- **R4 in mappa**: tema nuovo «Puntualità delle linee»: ogni linea colorata per % di passaggi in ritardo oltre 5 minuti
  nella fascia dell'ora scelta con lo slider e nel tipo di giorno; classi fisse verde→rosso: sotto 2,5% · 2,5-5 ·
  5-7,5 · 7,5-10 · oltre 10%; grigio sottile = linea senza dati (extraurbane, notte, meno di 200 passaggi). La notte
  (0-7) non è misurata: tutto grigio con una riga in legenda.
- **Link**: dalla scheda, ogni linea delle classifiche apre `mappa_torino.html#tema=puntualita&linea=<nome>`.

### Passi meccanici (per il modello minore, sul PC)
Regole come nel Giro 1 (`docs/PIANO_GIRO1_RITOCCHI.md`, sezione 0). Esito in `docs/ESITO_R4_GIRO2.md`: per ogni passo
OK / AVVISO / FERMO e le righe cambiate (file, prima, dopo). Aggiungi, non togliere: le uscite di oggi restano.
Database in sola lettura (`file:...?mode=ro`).

**Passo 1 — `scripts/27_risultato4_regolarita.py`.**
1. `carica_gtfs()`: leggi anche `route_type` (→ `modo_linea[route_short_name]` = "tram"/"metro"/"bus") e `stops.txt`
   (coordinate). Dopo `stop_times`, per ogni corsa calcola `ultima_seq[trip]` e `km_corsa[trip]` (somma delle distanze
   fra fermate consecutive in ordine di `stop_sequence`; usa `comuni.haversine_m`, importando `comuni` come gli altri
   script). Ritorna i nuovi dizionari; adatta la chiamata in `main()`.
2. **Oltre 10 minuti**: costante `SOGLIA_RITARDO_10 = 10.0`; in `stat_punt` aggiungi `"ritardo10"` = % dei ritardi > 10
   (dall'array dei ritardi che `stat_punt` riceve già). Vale per città, linee, fasce e modi.
3. **Tram contro bus**: nel ciclo sui passaggi aggiungi gli aggregati `punt_modo[(tipo, modo)]` e, nella regolarità,
   `reg_modo[(tipo, modo)]` (stessa logica di quelli per linea; se `regolarita()` ritorna i totali per nome linea,
   somma per modo da lì con `modo_linea`). JSON: `"modi": {"tram": {"0": {...}}, "bus": {...}}` e `"modo_linea"`.
4. **Ritardo a fine corsa**: per ogni passaggio con `seq >= ultima_seq[trip] - 2` aggiungi a `fine[(tipo, linea)]` la
   coppia (ritardo, km_corsa). Nel blocco di ogni linea: `"fine_corsa": {"passaggi": n, "ritardo_mediana": …,
   "km_mediana": …, "min_per_10km": mediana di (ritardo / km × 10)}` (solo se n > 0). Controllo: quota delle corse
   osservate con almeno un passaggio di fine corsa (OK sopra 30%, se no AVVISO).
5. **Linee utili**: se c'è `data/processed/popolarita_zone.json`, leggi l'elenco delle linee utili (guarda la chiave
   vera nel file) e scrivi `"linee_utili": {"0": {"utili": {...}, "altre": {...}}}` con passaggi, % ritardo, %
   ritardo10, % grappolo+buco (somme dei contatori, non medie di percentuali). Se il file manca: AVVISO e niente blocco.
6. Rapporto (in coda, il testo di oggi resta uguale): «OLTRE 10 MINUTI» (città per tipo di giorno, tram, bus, e la riga
   «GTT dichiara 2,3% nel 2025 (anno intero, tutte le linee): confronto solo come ordine di grandezza»); «TRAM CONTRO
   BUS» (feriale: passaggi, % in ritardo, % oltre 10, ritardo mediano, % grappolo+buco); «RITARDO A FINE CORSA» (10
   linee ordinarie con più minuti ogni 10 km, con almeno 100 passaggi di fine corsa: linea, modo, km, ritardo a fine
   corsa, minuti/10 km); «LINEE UTILI CONTRO ALTRE».
7. Costante del confronto: `RIF_GTT_RITARDO10_PCT = 2.3   # rapporto di sostenibilità GTT 2025: passaggi bus/tram in
   ritardo > 10', anno 2025 (docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md)`, scritta anche nei `parametri` del JSON.

**Passo 2 — `scripts/70_risultato9_attesa.py`: attesa per modo.** Leggi `modo_linea` da
`data/processed/risultato4_regolarita.json` (scritto dal passo 1; se manca: AVVISO e niente blocco). In `aggrega()`
aggiungi `"modi": {tipo: {modo: media_pesata([chiavi buone di quel tipo e di quel modo], acc)}}`; nel rapporto, in
coda, «ATTESA PER MODO (feriale)»: promessa, in più (bassa-alta), intervalli, per tram e bus.

**Passo 3 — `scripts/04_genera_mappa.py`: dati per il tema della puntualità.** Se c'è `risultato4_regolarita.json`,
aggiungi ai dati della mappa `"r4": {nome_linea_minuscolo: {tipo: {fascia: pct_ritardo, ...}, "n": {tipo: passaggi}}}`
solo per linee e fasce con almeno `min_passaggi` del JSON (oggi 200) e `"r4_meta": {"periodo": …, "soglia_min": 5,
"fasce": …}`. Stampa quante linee hanno dati. Dimensione attesa: pochi KB.

**Passo 4 — `scripts/mappa_template.html`.**
1. **Link dall'indirizzo**: funzione `applicaLineaDaUrl()` che legge `linea=<nome>` da `location.hash` (stessa forma di
   `applicaVistaDaUrl`), scrive il nome in `#filtroLinea`, accende `Llinee` se il tema lo prevede e richiama il
   ridisegno (`baseVer++; chiede();`). Chiamala accanto a `applicaVistaDaUrl()` all'avvio e in `hashchange`.
2. **Tema nuovo** in `THEMES`, dopo il tema della velocità: `{id:"puntualita", label:"Puntualità delle linee",
   desc:"Quanti passaggi arrivano con più di 5 minuti di ritardo, linea per linea, nell'ora scelta con il cursore.
   Misurato dal feed GTT.", area:null, over:{...NESSUNA,Llinee:1}, puntualita:true, legenda:()=>legendaR4()}`.
3. Disegno delle linee (cerca `if(tema.id==="velocita" || tema.velocita){`): prima di quel ramo, un ramo `if(tema.puntualita){ … continue; }`
   come quello della velocità: valore = `D.r4[l.nome]?.[String(S.dt)]?.[fasciaR4(S.h)]`; colore
   `PAL_VR[classe]` con le soglie `[2.5, 5, 7.5, 10]`, spessore 3,2; senza valore grigio `#9aa0ad`, alpha .5, spessore
   1,4. `fasciaR4(h)`: 0-6 notte, 7-8 punta_mattina, 9-15 giorno, 16-18 punta_sera, 19-23 sera (D9 del piano).
4. `legendaR4()`: titolo «Passaggi in ritardo oltre 5 minuti · fascia <nome della fascia> · <tipo di giorno>
   [MISURATO]», 5 riquadri con le classi scritte in numeri («sotto 2,5%», «2,5-5%», «5-7,5%», «7,5-10%», «oltre 10%»),
   un riquadro grigio «nessun dato (extraurbane, poche corse osservate)», una riga con il periodo da `D.r4_meta`; di
   notte la riga «La notte non è misurata (la raccolta riparte verso le 5)». Chi cambia l'ora deve già richiamare
   `aggiornaLegenda()` (standard della memoria): controlla che valga anche qui.
5. Legenda generica delle linee (cerca `if(vis("Llinee") && !tema.velocita && tema.id!=="velocita"){`): aggiungi
   `&& !tema.puntualita`.
6. Tooltip delle linee, se esiste un tooltip al passaggio sulle linee: nel tema puntualità mostra «linea N · X% in
   ritardo oltre 5 min (fascia)»; se il tooltip delle linee non esiste, non crearlo e scrivilo nell'esito.

**Passo 5 — `simulazione.html`: link nelle barre.** In `function graficoBarre(g)`, se la voce ha `v.link`, l'etichetta
diventa `<a href="${esc(v.link)}" class="barra-link">…</a>` (stesso testo, `title` uguale); stile minimo: colore del
link della pagina, niente sottolineatura finché non ci passi sopra.

**Passo 6 — `scripts/schede_risultati.py`.**
1. `voce(...)`: parametro facoltativo `link=None` (se dato, `v["link"] = link`).
2. Scheda R4: nelle due classifiche delle linee (cerca `"Le 10 linee più in ritardo (feriale)"` e `"Le 10 linee più
   irregolari"`) ogni voce ha `link=f"mappa_torino.html#tema=puntualita&linea={n}"`; nella nota «Clicca una linea per
   vederla nella mappa.».
3. Grafici nuovi (dopo quelli di oggi): «Tram contro bus (feriale)» (barre: % in ritardo oltre 5 min e % oltre 10 min
   per tram e bus); «Ritardo a fine corsa: minuti ogni 10 km (feriale)» (10 linee, con link); «Linee utili contro
   altre (feriale)» (% in ritardo). Fra i numeri «Oggi»: «In ritardo oltre 10 minuti (feriale)» e una riga nella
   risposta: «Oltre 10 minuti: X% nei feriali (GTT dichiara 2,3% per il 2025, su tutto l'anno e tutte le linee: solo
   ordine di grandezza).»
4. Parte «attese» (ex R9): una riga per tram e bus dall'attesa per modo (passo 2), se c'è.
5. `"mappa"` della scheda R4: `{"id": "puntualita", "tema": "Puntualità delle linee", "nota": "Nella mappa, tema
   «Puntualità delle linee»: ogni linea colorata per ritardo nell'ora scelta con il cursore."}`.
6. `in_english` con gli stessi numeri nuovi (tram/bus, oltre 10, per km). Niente numeri scritti a mano tranne il 2,3
   (dalla costante del JSON).

**Passo 7 — Lanci.** `python scripts\27_risultato4_regolarita.py` → `python scripts\70_risultato9_attesa.py` →
`python scripts\04_genera_mappa.py` → `python scripts\schede_risultati.py` → `python scripts\prova_pagine_r6.py
--senza-screenshot` (0 errori; il tema `puntualita` deve comparire fra i temi provati). Nell'esito: oltre 10 minuti
(città feriale, tram, bus), tram contro bus, le 10 linee per minuti/10 km, linee utili contro altre, attesa per modo,
quante linee hanno dati in mappa, dimensione di `mappa_torino.html`, `git status`. Buon senso (non nel codice): oltre 10
minuti intorno all'1-3%; feriale in ritardo oltre 5 minuti resta circa 5,2%.

### Controlli di Claude dopo il giro
Codice; numeri del rapporto (somme tram + bus = città; oltre 10 ≤ oltre 5); mappa in Chromium (tema nuovo con lo slider
dell'ora, legenda, linea da indirizzo `#tema=puntualita&linea=17`), link della scheda.

### Prompt da incollare (per Leo, sul PC)

> Sei un agente che lavora sul progetto GTT in `C:\projects\Progetti\GTT`, ramo git `prova`. Prima:
> `git branch --show-current` (deve dire `prova`, altrimenti fermati e dimmelo), `git status` (se ci sono modifiche
> fermati e dimmelo), `git pull origin prova`. Leggi `AGENTS.md` e in `docs/PIANO_RISULTATO4.md` la sezione «Giro 2
> del Risultato 4», poi esegui i 7 passi meccanici, uno alla volta, nell'ordine. Aggiungi, non togliere: le uscite di
> oggi restano. Cambia solo quello che i passi dicono; niente numeri scritti a mano nei testi, salvo il 2,3 di GTT
> (costante con la fonte). Database in sola lettura. Se una riga da cercare non c'è o un nome è diverso, guarda il
> file vero, adatta e scrivilo. Scrivi tutto in `docs/ESITO_R4_GIRO2.md` (OK / AVVISO / FERMO per passo, righe
> cambiate prima/dopo, uscite dei controlli). Non modificare `MEMORIA_PROGETTO.md`. Python: `python` del PATH, mai
> Anaconda. Alla fine fai commit e push come dice `AGENTS.md` (sezione «Commit») e scrivi un riassunto di 10 righe in
> italiano semplice con: oltre 10 minuti (e il confronto con GTT), tram contro bus, le 3 linee con più ritardo per km,
> linee utili contro altre, e gli errori della prova delle pagine.

## Ricontrollo del Giro 2 (Claude, 21/10) e problema trovato

Codice e numeri del Giro 2 a posto (tram + bus = città, fine corsa su 88,5% delle corse, 90 linee in mappa; mappa in
Chromium: `#tema=puntualita&linea=17` apre il tema con la 17 filtrata, legenda giusta, nessun errore). Numeri feriali:
oltre 5 minuti tram 4,6%, bus 5,4%; grappolo+buco tram 13,8%, bus 8,4%; attesa in più tram 0,6-1,1 min, bus
0,6-2,3; linee utili 5,6% in ritardo contro 4,4% delle altre.

**Problema (trovato dall'agente, confermato da Claude sul codice):** fra i passaggi usati nessun ritardo supera 10
minuti (massimo 9,98). La regola D3 scarta un passaggio se l'ultima lettura è a più di 10 minuti dall'arrivo stimato;
nei feriali ne scarta 49.818, e **34.929 di questi hanno un ritardo oltre 10 minuti**. Spiegazione probabile: il feed
GTT smette di elencare la fermata verso l'orario programmato, quindi per un mezzo molto in ritardo l'ultima lettura è
lontana dall'arrivo e D3 la butta. Conseguenza: **i ritardi lunghi non entrano mai nei conti**, e anche il titolo
«5,2% in ritardo oltre 5 minuti» è sottostimato. Rimettendo dentro gli scartati con ritardo oltre 10 minuti il titolo
salirebbe verso l'8% (ordine di grandezza, da verificare). Va controllato con un dato indipendente prima di cambiare
la regola: le **posizioni GPS dei mezzi** (tabella `mezzi_gtt`), già usate dallo script 70 per il «controllo col GPS».

## Giro 3 del Risultato 4 — verifica della regola D3 con il GPS (solo lettura) + due ritocchi

Valori predefiniti di Claude: 2 giorni feriali interi (15/10 e 16/10; se uno è incompleto, il feriale intero più
vicino); al massimo 3.000 passaggi per gruppo, presi a passo fisso (uno ogni k, niente caso); passaggio GPS valido se
il mezzo passa a meno di 60 m dalla fermata (come lo script 70).

**Passo 1 — nuovo `scripts/90_verifica_ritardi_gps.py` (sola lettura, scrive solo il suo rapporto).**
1. Carica lo script 27 con `comuni.carica_script("27_risultato4_regolarita.py")` e usane `carica_gtfs()`,
   `leggi_giorno()` e le funzioni dell'ora; dallo script 70 (stesso modo) usa la logica di `controllo_gps()` per trovare
   l'istante in cui il mezzo passa vicino alla fermata (copiala in una funzione che lavora su un passaggio alla volta, se
   non si può riusare così com'è).
2. Per ogni giorno ricostruisci i passaggi come `costruisci_passaggi()` dello script 27 ma **tenendo anche gli
   scartati per lettura lontana**, con: linea, trip, seq, stop, orario programmato, ritardo del feed, arrivo stimato,
   istante dell'ultima lettura.
3. Gruppi: (A) usati con ritardo del feed fino a 5 min; (B) usati con ritardo 5-10; (C) scartati per lettura lontana.
   Per ognuno, sui passaggi con GPS valido: ritardo vero = passaggio GPS − orario programmato.
4. Rapporto `docs/RAPPORTO_R4_VERIFICA_GPS.txt`: per gruppo, quanti passaggi e quanti con GPS valido; distribuzione del
   ritardo vero (% sotto 5, 5-10, oltre 10); differenza mediana fra arrivo stimato dal feed e GPS; per il gruppo C anche
   la distribuzione di (ultima lettura − orario programmato) in minuti (serve a capire quando il feed smette di elencare
   la fermata). In fondo la **stima corretta** per i 2 giorni: % in ritardo oltre 5 e oltre 10 minuti, contando i
   passaggi usati come oggi più gli scartati con il ritardo vero del GPS (pesati per quanti sono gli scartati in
   tutto), accanto a quella di oggi.
5. Controlli: almeno 300 passaggi con GPS valido nel gruppo C (se no AVVISO); tram + bus nel rapporto.

**Passo 2 — ritocco: classifica del ritardo a fine corsa.** In `27_risultato4_regolarita.py` (rapporto) e nella scheda
R4 la classifica «ritardo a fine corsa» si ordina per **ritardo a fine corsa (mediana, minuti)**, non per minuti ogni
10 km (che premiava le linee corte: in testa la 6 con 4,3 km e 1,2 minuti); i minuti ogni 10 km restano come colonna e
nella nota. Titolo del grafico: «Ritardo a fine corsa (feriale)».

**Passo 3 — ritocco: i link aprono la mappa alle 8.** Template: `applicaLineaDaUrl()` legge anche `ora=<0-23>`
dall'indirizzo e, se c'è, porta lo slider a quell'ora (`S.m = ora*60`, poi `aggiornaOra(); aggiornaLegenda();`). Scheda
R4: `link_linea()` aggiunge `&ora=8`; la nota del grafico dice «la mappa si apre alle 8 di un feriale».

**Passo 4 — lanci.** `python scripts\90_verifica_ritardi_gps.py` → `python scripts\27_risultato4_regolarita.py` →
`python scripts\70_risultato9_attesa.py` → `python scripts\04_genera_mappa.py` → `python scripts\schede_risultati.py`
→ `python scripts\prova_pagine_r6.py --senza-screenshot`. Esito in `docs/ESITO_R4_VERIFICA_GPS.md` con l'uscita
completa dello script 90. **Non** cambiare la regola D3: si decide con Leo dopo aver visto la verifica.

### Prompt da incollare (per Leo, sul PC)

> Sei un agente che lavora sul progetto GTT in `C:\projects\Progetti\GTT`, ramo git `prova`. Prima:
> `git branch --show-current` (deve dire `prova`, altrimenti fermati e dimmelo), `git status` (se ci sono modifiche
> fermati e dimmelo), `git pull origin prova`. Leggi `AGENTS.md` e in `docs/PIANO_RISULTATO4.md` le sezioni
> «Ricontrollo del Giro 2» e «Giro 3 del Risultato 4», poi esegui i 4 passi, uno alla volta, nell'ordine. Database in
> sola lettura (`file:...?mode=ro`). Non cambiare la regola D3 né altre regole D1-D9. Niente numeri scritti a mano nei
> testi. Se un nome di tabella, colonna o funzione è diverso dal piano, guarda il file vero, adatta e scrivilo. Esito in
> `docs/ESITO_R4_VERIFICA_GPS.md` (OK / AVVISO / FERMO per passo, righe cambiate prima/dopo, uscita completa dello
> script 90). Non modificare `MEMORIA_PROGETTO.md`. Python: `python` del PATH, mai Anaconda. Alla fine fai commit e
> push come dice `AGENTS.md` (sezione «Commit») e scrivi un riassunto di 10 righe in italiano semplice: per i tre gruppi
> quanti passaggi hanno il GPS e che ritardo vero hanno, e la stima corretta di «oltre 5» e «oltre 10» minuti accanto a
> quella di oggi.

---

# PARTE A — storia del Risultato 4


Scritto il 14/10/2026 per un agente. Esegui i passi **nell'ordine**, uno alla volta. Ogni passo ha un
controllo: se non torna, **FERMATI** e scrivi a Leo cosa hai visto. Non inventare correzioni.

## La domanda

1. **Puntualità**: quanti passaggi dei mezzi GTT alle fermate arrivano con **più di 5 minuti di
   ritardo**? Su quali linee e a che ora va peggio?
2. **Regolarità**: sulle linee frequenti, quante volte i mezzi arrivano **a grappolo** (due attaccati)
   o lasciano un **buco** (attesa molto più lunga del previsto)?

## Regole (valgono sempre)

- Ramo git `prova` (se non ci sei, fermati). **Non fare commit**: decide Leo.
- `python` del PATH (3.14), niente Anaconda. Solo libreria standard (niente pandas).
- `data/storico_backup.sqlite` **solo in lettura**: `sqlite3.connect("file:data/storico_backup.sqlite?mode=ro", uri=True)`.
- Non toccare `data/raw/`, la mappa (`mappa_torino.html`, `scripts/mappa_template.html`) e
  `scripts/04_genera_mappa.py`. Non lanciare `04_genera_mappa.py`.
- Non lanciare nulla che usi R5/Java: il PC sta facendo un altro calcolo lungo.
- Scrivi solo questi file: `scripts/27_risultato4_regolarita.py`,
  `data/processed/risultato4_regolarita.json`, `docs/RAPPORTO_RISULTATO4.txt`, e alla fine due righe
  in `MEMORIA_PROGETTO.md` (passo 7).

## Come sono fatti i dati (già verificato, non serve ricontrollarlo)

- **Ritardi**: tabella `trip_update_gtt` in `data/storico_backup.sqlite`, una lettura circa ogni minuto
  dal 10/10. Colonne: `letto_utc`, `trip_id`, `start_date` (AAAAMMGG, data locale della corsa),
  `start_time`, `payload` (JSON). Esempio di `payload`:
  ```json
  {"trip":{"trip_id":"28373194U","start_time":"10:39:00","start_date":"20261014","rel":0},
   "stu":[{"seq":55,"arr":{"delay":249},"rel":0}],"ts":1791971630,"id":"28373194U"}
  ```
  Ogni elemento di `stu` è una fermata della corsa (`seq` = `stop_sequence` del GTFS). Dentro `arr`
  c'è **o** `delay` (ritardo in secondi, ~70% dei casi) **o** `time` (orario previsto di arrivo, in
  secondi epoch UTC, ~30%). La stessa corsa compare in molte letture di fila: il bus avanza e le
  `seq` crescono.
- **Orario programmato**: `data/raw/gtt_gtfs_20261003_224530.zip`, file `trips.txt` (`trip_id`,
  `route_id`, `direction_id`), `routes.txt` (`route_id`, `route_short_name`), `stop_times.txt`
  (`trip_id`, `stop_sequence`, `arrival_time`, `stop_id`). `arrival_time` è `HH:MM:SS` in ora locale e
  può superare 24:00 (corse dopo mezzanotte).
- **Ora locale**: dal 10/10 al 24/10 l'Italia è a UTC+2. Per sicurezza copia le funzioni
  `ultima_domenica`, `offset_roma`, `a_roma` da `scripts/09_analisi_dati_diurni.py`.
- Tipo di giorno: 0 = feriale (lun-ven), 1 = sabato, 2 = domenica.

## Decisioni già prese (non cambiarle)

| # | Regola | Valore |
|---|---|---|
| D1 | Passaggio osservato | per ogni (`trip_id`, `start_date`, `seq`) si tiene **solo l'ultima lettura** (la `letto_utc` più recente) in cui quella `seq` compare: è la più vicina all'arrivo vero |
| D2 | Ritardo del passaggio | se c'è `arr.delay`: `delay/60` minuti. Se c'è `arr.time`: `(time - orario_programmato)/60`, con orario programmato = mezzanotte locale di `start_date` + `arrival_time` del GTFS, convertito in UTC |
| D3 | Lettura affidabile | si scarta il passaggio se l'ultima lettura è lontana dall'arrivo stimato più di **10 minuti** (cioè \|arrivo stimato − letto_utc\| > 10 min) o se la corsa/seq non è nel GTFS. Conta e riporta quanti scarti |
| D4 | Classi di puntualità | **anticipo** se ritardo < −1 min; **puntuale** se −1 … +5 min; **in ritardo** se > +5 min |
| D5 | Arrivo stimato | orario programmato + ritardo (serve per la regolarità e per D3) |
| D6 | Linee frequenti | per la regolarità si considerano solo coppie con intervallo **programmato ≤ 15 minuti** |
| D7 | Classi di regolarità | per due passaggi consecutivi alla stessa fermata (stessa linea, stessa direzione, stesso giorno): **grappolo** se intervallo osservato < 0,5 × programmato; **buco** se > 2 × programmato; altrimenti **regolare** |
| D8 | Dati sufficienti | una linea entra nelle classifiche solo con **≥ 200 passaggi** osservati nel tipo di giorno (puntualità) e **≥ 100 coppie** (regolarità) |
| D9 | Fasce orarie | punta mattina 7-9, giorno 9-16, punta sera 16-19, sera 19-24, notte 0-7 (ora locale dell'arrivo programmato) |

## Passo 1 — Controllo di partenza

Lancia:
```
python -c "import sqlite3;c=sqlite3.connect('file:data/storico_backup.sqlite?mode=ro',uri=True);print(c.execute('select count(*),min(letto_utc),max(letto_utc),count(distinct start_date) from trip_update_gtt').fetchone())"
```
Atteso: circa 1 milione di righe, dal `2026-10-10` al `2026-10-14`. Annota il risultato.

## Passo 2 — Scrivere `scripts/27_risultato4_regolarita.py`

Struttura dello script (docstring in italiano che riassume domanda, decisioni D1-D9, input e output):

1. **Carica il GTFS** (una volta sola, dal file zip):
   - `trips.txt` → `trip_info[trip_id] = (route_id, direction_id)`;
   - `routes.txt` → `nome_linea[route_id] = route_short_name`;
   - `stop_times.txt` → `prog[(trip_id, stop_sequence)] = (secondi_da_mezzanotte, stop_id)`, dove
     `secondi = h*3600 + m*60 + s` (h può essere ≥ 24).
2. **Un giorno alla volta** (il PC ha poca memoria libera: NON caricare tutti i giorni insieme).
   Prendi l'elenco dei giorni con `SELECT DISTINCT start_date FROM trip_update_gtt ORDER BY 1` e, per
   ogni giorno, leggi solo le sue righe (`SELECT letto_utc, trip_id, payload FROM trip_update_gtt
   WHERE start_date = ? ORDER BY letto_utc`). Per ogni elemento di `stu` aggiorna un dizionario
   `ultimo[(trip_id, seq)] = (letto_utc, arr)`. Siccome le righe sono in ordine di tempo, alla fine
   resta l'ultima lettura (D1). Fai i punti 3 e 5 per quel giorno, conserva solo i numeri che servono
   ai totali (ritardi in minuti in liste per chiave, conteggi delle coppie), poi **svuota** `ultimo`
   e i passaggi del giorno prima di passare al successivo.
3. **Costruisce i passaggi** del giorno: per ogni chiave di `ultimo`:
   - se `(trip_id, seq)` non è in `prog` o `trip_id` non è in `trip_info` → scarto "fuori GTFS";
   - orario programmato UTC = mezzanotte locale di `start_date` + secondi, meno l'offset (UTC+2);
   - ritardo in minuti come D2; arrivo stimato come D5;
   - se \|arrivo stimato − letto_utc\| > 10 min → scarto "lettura lontana" (D3);
   - altrimenti salva il passaggio: linea (nome), direzione, stop_id, trip_id, start_date, tipo di
     giorno, fascia oraria (D9), orario programmato, arrivo stimato, ritardo, classe (D4).
4. **Puntualità**: per città e per (linea × tipo di giorno) e per (linea × tipo di giorno × fascia):
   numero di passaggi, % anticipo, % puntuale, % in ritardo, ritardo mediano e 90° percentile.
5. **Regolarità**: raggruppa i passaggi per (linea, direzione, stop_id, start_date). In ogni gruppo
   ordina per **orario programmato**; per ogni coppia di passaggi consecutivi calcola intervallo
   programmato e intervallo osservato (differenza degli arrivi stimati, in minuti). Tieni solo le
   coppie con programmato ≤ 15 min (D6) e classificale (D7). Per città e per (linea × tipo di
   giorno): numero di coppie, % grappolo, % buco, % regolare.
6. **Output JSON** `data/processed/risultato4_regolarita.json` (compatto, `ensure_ascii=False`):
   ```json
   {"generato":"...","tag":"MISURATO","periodo":{"da":"...","a":"..."},
    "giorni":{"0":3,"1":1,"2":1},"parametri":{"soglia_ritardo_min":5,"soglia_anticipo_min":-1,
    "max_lettura_lontana_min":10,"freq_max_min":15,"min_passaggi":200,"min_coppie":100},
    "scarti":{"fuori_gtfs":0,"lettura_lontana":0,"usati":0},
    "citta":{"0":{"passaggi":0,"anticipo":0.0,"puntuale":0.0,"ritardo":0.0,"mediana":0.0,"p90":0.0,
                  "coppie":0,"grappolo":0.0,"buco":0.0,"regolare":0.0}},
    "linee":{"<nome>":{"0":{...stessi campi...,"fasce":{"punta_mattina":{...}}}}}}
   ```
   Percentuali con una cifra decimale. I tipi di giorno senza dati non si scrivono.
7. **Rapporto** `docs/RAPPORTO_RISULTATO4.txt`, in quest'ordine:
   - periodo, giorni per tipo, passaggi usati e scarti (numeri e %);
   - **I 3 NUMERI** (feriale): % passaggi in ritardo > 5 min; % coppie a grappolo + % a buco sulle
     linee frequenti; ritardo mediano;
   - puntualità città per tipo di giorno e per fascia oraria (feriale);
   - **10 linee peggiori per % in ritardo** (feriale, solo con ≥ 200 passaggi);
   - **10 linee peggiori per % grappolo + buco** (feriale, solo con ≥ 100 coppie);
   - avviso finale: "[MISURATO] dal feed GTFS-Realtime GTT; il ritardo è quello stimato dal sistema
     GTT alla fermata nell'ultima lettura prima dell'arrivo; sabato e domenica con 1 solo giorno:
     [DATI SCARSI]."
8. Opzione `--prova`: usa solo `start_date = 20261013` e scrive il rapporto **solo a schermo** (non
   scrive i file).

## Passo 3 — Prova

`python scripts\27_risultato4_regolarita.py --prova`

Controlli (scrivi l'esito di ognuno). Riferimento: Claude ha provato le regole su 13/10 dalle 7 alle
10 e ha ottenuto ~9% fuori GTFS, ~3% letture lontane, mediana −0,4 min, 90° percentile 3,6 min,
5,5% in ritardo > 5 min. Sul giorno intero i numeri saranno simili, non identici.
- gira senza errori in pochi minuti;
- scarti "fuori GTFS" sotto il 25% (il GTFS è del 3/10, qualche corsa può mancare);
- ritardo mediano della città tra −1 e +3 minuti;
- % in ritardo > 5 min tra l'1% e il 30%;
- se uno di questi non torna: **FERMATI** e scrivi a Leo.

## Passo 4 — Giro completo

1. Controlla la memoria libera:
   `powershell -NoProfile -Command "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1KB)"`
   (numero in MB). Se è **sotto 800**, non lanciare il giro: fermati e scrivi a Leo che conviene
   aspettare la fine del calcolo di accessibilità (domattina).
2. `python scripts\27_risultato4_regolarita.py` (senza `--prova`). Controlla che abbia scritto i due
   file e annota quanto tempo ci ha messo.

## Passo 5 — Controlli indipendenti (obbligatori)

1. **Due passaggi a mano**: prendi 2 passaggi dal JSON/rapporto (uno con `arr.delay`, uno con
   `arr.time`). Per ciascuno, con una query SQL diretta trova l'ultima riga di `trip_update_gtt` di
   quella corsa e data in cui compare quella `seq`, leggi `arr` e ricalcola il ritardo a mano con
   l'orario del GTFS. Deve coincidere.
2. **Le due fonti si somigliano**: calcola il ritardo mediano separatamente per i passaggi con
   `delay` e per quelli con `time`. Devono essere simili (differenza sotto i 2 minuti); se no, dillo.
3. **Il ritardo cresce lungo la corsa**: ritardo mediano dei passaggi con `seq` ≤ 5 contro `seq` ≥ 30.
   Di solito il secondo è più alto.
4. **Le ore di punta vanno peggio**: % in ritardo feriale in punta (7-9, 16-19) contro notte (0-7).
5. **Una coppia a grappolo a mano**: prendi una coppia classificata "grappolo", riporta i due
   orari programmati e i due arrivi stimati e verifica la regola D7.
6. Somme: per la città, anticipo + puntuale + ritardo = 100% (±0,1); grappolo + buco + regolare = 100%.

## Passo 6 — Consegna a Leo (poi Claude ricontrolla)

Scrivi a Leo, in parole semplici e corte:
- i **3 numeri** (feriale);
- le 5 linee peggiori per ritardo e le 5 peggiori per irregolarità;
- l'esito di ognuno dei controlli del passo 5;
- scarti e limiti (giorni pochi, sabato/domenica scarsi);
- i file creati.

## Passo 7 — Memoria

In `MEMORIA_PROGETTO.md`: nella tabella della **sezione 4 (FATTO)** aggiungi una riga "Risultato 4
v1 (27)" con i 3 numeri; nella **sezione 6** aggiorna il punto del Risultato 4 con "fatto, da
controllare da Claude; resta la mappa". Non aggiungere sezioni, non toccare il resto.

## Dopo (NON in questo giro)

Mappa (colorare le linee per % in ritardo / irregolarità con lo slider dell'ora, come la velocità
commerciale già presente) e pagina in `simulazione.html`: piano a parte, dopo la rigenerazione della
mappa. Rilanciare lo script quando ci saranno più sabati e domeniche.

## Stato al 18/10/2026 (spostato qui dalla memoria)

- **Versione 2** [MISURATO], 10-18/10 (5 feriali, 2 sabati, 2 domeniche; giorni parziali 10, 12, 13, 18/10
  contati con le ore che hanno dati — scelta di Leo), 1.280.961 passaggi.
  **Feriale: 5,3% in ritardo > 5 min · 10,5% grappolo+buco · ritardo mediano −0,4 min · 39,9% in anticipo.**
  Sale rispetto alla v1 (4,2%) perché giovedì 15 e venerdì 16 sono andati peggio (ricontrollo indipendente
  giorno per giorno: stessa tendenza). La v1 aveva giorni a metà (il 12/10 solo pomeriggio); è conservata in
  `data/processed/risultato4_regolarita_v1.json` e `docs/archivio/RAPPORTO_RISULTATO4_v1.txt`. Scheda in `simulazione.html`.
- **Copertura del feed ritardi** (`trip_update_gtt`, dal 10/10, una lettura al minuto; verificata 18/10):
  `delay` di corsa mai presente; per ogni fermata `stop_time_update.arr` ha `delay` in secondi (~70%) o l'arrivo
  previsto `time` (~30%, da confrontare con l'orario GTFS). Raccolta 05-24 locali (niente notte); solo ~90 linee
  urbane, 108 linee mai presenti (extraurbane a 4 cifre, alcune notturne; 3.540 corse/giorno); sulle linee coperte
  c'è ~80% delle corse programmate (GPS `mezzi_gtt` 77%, almeno uno dei due 82%). Corse mancanti = saltate o non
  trasmesse, non distinguibili: il risultato misura solo le corse presenti nel feed.
- Il 18/10 il feed GTT (`percorsieorari.gtt.to.it`) non ha risposto dalle ~09:05: buco nei dati di quel giorno.


---

# PARTE B — ex Risultato 9: attesa promessa contro attesa reale [MISURATO]

> **Stato (20/10/2026): versione 1 fatta il 18/10, scheda in `simulazione.html`** (numeri nella sezione 9).
> Prossimo: rilancio con un mese di dati (metà novembre).

Scritto da Claude il 18/10/2026, da approvare con Leo prima di costruire (sezione 6: decisioni aperte).
Riparte dai dati e dallo script del Risultato 4 (`scripts/27_risultato4_regolarita.py`, `docs/PIANO_RISULTATO4.md`).

### 1. La domanda (in parole semplici)

Alla fermata l'orario promette, per esempio, un bus ogni 8 minuti: chi arriva a caso aspetta in media 4 minuti.
Se però i bus arrivano a coppie (grappolo) e poi lasciano un buco, l'attesa vera è più lunga, anche se il numero
di bus nell'ora è lo stesso. **Quanti minuti in più aspetta, in media, chi prende un bus o tram frequente a Torino?
Su quali linee, fermate e ore va peggio?**

Perché è rilevante: è la misura che usano le grandi aziende di trasporto per la regolarità delle linee frequenti
(Londra la pubblica come "Excess Wait Time"). Traduce il risultato 4 (percentuali di grappoli e buchi) in una cosa
che tutti capiscono: minuti persi alla fermata. Si calcola con dati che solo questo progetto raccoglie (feed GTT
salvato ogni minuto sul Raspberry Pi).

### 2. La formula (una sola, spiegata)

Per una fermata, una linea, un verso e una fascia oraria, con gli intervalli fra un passaggio e il successivo
h1, h2, ..., hn (in minuti):

- **attesa media** di chi arriva a caso = (h1² + h2² + ... + hn²) / (2 × (h1 + h2 + ... + hn))
- **attesa promessa** = la stessa formula con gli intervalli dell'orario ufficiale (GTFS)
- **attesa reale** = la stessa formula con gli intervalli osservati (arrivi stimati dal feed, come nel risultato 4)
- **attesa in più** = attesa reale − attesa promessa

Esempio: bus esattamente ogni 10 minuti → (10²+10²)/(2×20) = 5 minuti. Stessi 2 bus all'ora ma a coppie, con
intervalli 2 e 18 → (4+324)/(2×20) = 8,2 minuti. Stessa offerta, 3,2 minuti in più di attesa.

La formula vale per le linee **frequenti** (chi va alla fermata non guarda l'orario). Per le linee rare conta la
puntualità, che è già nel risultato 4.

### 3. Cosa sappiamo già dei dati (verificato da Claude il 18/10 sul backup del 18/10)

1. **Feed dei ritardi** (`trip_update_gtt`): dal 10/10, una lettura al minuto. Le giornate complete (06-24) sono
   11, 14, 15, 16 e 17/10; il 10, 12, 13 e 18/10 sono parziali (il 18 per un guasto del feed GTT dalle ~09:05).
   La raccolta si ferma ogni notte a mezzanotte locale e riparte verso le 5: la notte non è misurabile.
2. **Il feed copre solo le linee urbane.** Il 15/10: 90 linee con dati, **108 linee mai presenti** (3.540 corse
   al giorno: numeri a 4 cifre, cioè extraurbane, e alcune notturne). Il risultato vale solo per le linee coperte.
3. **Anche sulle linee coperte manca circa 1 corsa su 5.** Il 15/10, su 9.624 corse programmate delle 90 linee:
   80,1% nel feed dei ritardi, 77,1% nelle posizioni GPS (`mezzi_gtt`), 82,2% in almeno uno dei due. Le linee
   frequenti sono coperte meglio (linea 4: 369 su 380; linea 10: 251 su 260), ma per esempio la linea 2 ha 194 su 243.
   **Una corsa che manca può essere saltata davvero oppure non trasmessa: dai dati non si distingue.** Questo è il
   punto più delicato del metodo (sezione 4, punto 3, e decisione D1).
4. L'arrivo "osservato" è l'arrivo **stimato dal feed** nell'ultima lettura entro 10 minuti dal passaggio (regola
   D1-D5 del risultato 4), non un arrivo visto sul posto.

### 4. Metodo proposto (passi, ognuno con un controllo)

**Passo 1 — Linee e fasce.** Linee frequenti = intervallo programmato ≤ 12 minuti (almeno 5 passaggi all'ora) in
quella fascia, fermata e verso (D2). Fasce come nel risultato 4 (punta mattina 7-9, giorno 9-16, punta sera 16-19,
sera 19-24), più tipo di giorno. Solo le ore in cui la raccolta era attiva (almeno 50 minuti letti nell'ora).
*Controllo:* elenco delle linee frequenti con numero di fermate e passaggi programmati; confronto con le linee
frequenti già usate nel risultato 4.

**Passo 2 — Intervalli promessi e osservati.** Per ogni fermata-linea-verso-giorno si mettono in fila le corse
programmate e i loro arrivi stimati (dallo script 27, stessa lettura dei dati). *Controllo:* per 3 fermate
scelte a mano (una della linea 4, una della 15, una della 68) stampare la fila di orari promessi e stimati e rifare a
mano l'attesa promessa e reale.

**Passo 3 — Corse mancanti: una forbice, non un numero solo (D1).**
- *Stima bassa:* una corsa assente nel feed è considerata "non vista": l'intervallo si calcola solo tra corse
  consecutive entrambe osservate (si scartano i pezzi con buchi). Sottostima l'attesa se le corse mancanti erano
  saltate davvero.
- *Stima alta:* una corsa assente sia dal feed dei ritardi sia dal GPS mentre la raccolta era attiva è considerata
  **non effettuata**: l'intervallo reale salta da un bus all'altro. Sovrastima l'attesa se la corsa c'era ma non
  trasmetteva.
- Si pubblicano entrambe, con il numero principale = la stima bassa (prudente) e la forbice accanto.
*Controllo:* quota di corse mancanti per linea e fascia; se una linea ne ha più del 20% in una fascia, quella
fascia va in tabella "dati scarsi" e non entra nei numeri di testa.

**Passo 4 — Prova con il GPS (controllo indipendente del feed).** Su 2 linee frequenti (4 e 15) e circa 20
fermate, confrontare l'arrivo stimato dal feed con il momento in cui il GPS del mezzo (`mezzi_gtt`, posizione ogni
minuto) passa più vicino alla fermata. Se la differenza mediana supera 1 minuto, fermarsi e decidere con Leo.

**Passo 5 — Numeri.** Per linea-verso-fascia-tipo di giorno: attesa promessa, attesa reale (bassa e alta),
attesa in più in minuti e in %, numero di intervalli. Città: media pesata sul numero di passaggi programmati (non
abbiamo i passeggeri; D3). Classifiche: le 10 linee e le 20 fermate con più attesa in più (con almeno 30 intervalli).

**Passo 6 — Scheda in `simulazione.html`** (stesso formato delle altre, `scripts/schede_risultati.py`): numero
chiave, grafico per fascia oraria, classifica delle linee, prima/dopo "attesa promessa → attesa reale".
La mappa per fermate solo se Leo la vuole, dopo.

### 5. Uscite

`scripts/<numero libero>_risultato9_attesa.py` (il numero si sceglie quando l'agente della Fase 5 ha finito, per
non scontrarsi con i suoi 56+), `data/processed/risultato9_attesa.json`, `docs/RAPPORTO_RISULTATO9_ATTESA.txt`,
scheda nella pagina dei risultati. Calcolo leggero (come lo script 27: ~500 MB di memoria, pochi minuti).

### 6. Decisioni aperte (da chiedere a Leo, con il default proposto)

| # | Domanda | Default proposto |
|---|---|---|
| D1 | Corse mancanti | Forbice bassa/alta, numero principale = stima bassa |
| D2 | Cosa vuol dire "frequente" | ≤ 12 minuti di intervallo programmato (sensibilità: 10 e 15) |
| D3 | Peso per la media della città | Passaggi programmati (niente dati sui passeggeri) |
| D4 | Numero del risultato | Risultato 9 |
| D5 | Chi lo esegue | Claude, in questa cartella, dopo l'approvazione del piano |

### 7. Limiti da dichiarare già ora

- Arrivi stimati dal feed GTT, non osservati sul posto (verificati a campione col GPS, passo 4).
- Solo linee urbane presenti nel feed; niente extraurbane, niente notte.
- Corse mancanti: risultato dato come forbice.
- Chi arriva alla fermata "a caso": vero per le linee frequenti, non per chi guarda l'orario o l'app.
- Pochi giorni (vedi sezione 3): il risultato va rifatto quando ci sono più settimane di dati.

### 8. Effetto sul risultato 4 (scoperto preparando questo piano)

Anche il risultato 4 misura solo le corse presenti nel feed: se le corse mancanti sono in parte saltate davvero, la
puntualità reale è peggiore di quella misurata e i "buchi" sono sottostimati (una corsa saltata non crea un buco
nel conteggio, perché la coppia si calcola fra corse osservate). Va scritto fra i limiti del risultato 4.

### 9. Stato al 18/10/2026 (spostato qui dalla memoria)

**Versione 1** [MISURATO], 10-18/10, linee urbane frequenti (≤ 12 min), ore con raccolta attiva.
Feriale: attesa promessa 4,8 min, reale 5,4-6,2 → **0,6-1,5 min in più** (+13% stima bassa); sabato +0,8-1,4;
domenica troppo pochi dati. Peggiori: linea 68 (+1,3-3,0), 3, 56, 46, 62; fermate della 18 (Caio Mario,
Lingotto) e della 62. Controlli: GPS linee 4 e 15 (343 passaggi, scarto tipico 0,45 min, 70% entro 1 min); una
chiave rifatta da zero coincide (2,555 / 3,668 min). Lo script 70 riusa il 27 senza modificarlo. Scheda in
`simulazione.html`. Da rilanciare con più settimane di dati (27, poi 70, poi `schede_risultati.py`).
