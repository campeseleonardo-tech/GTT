# Piano meccanico — Risultato 6 (finale, passo 3): direzioni d'ingresso, tre sottotemi, criteri spiegati

Scritto da Claude il 19/10/2026 con Leo, per un altro modello (agente). **Sostituisce** le parti di `PIANO_R6_PORTE.md` sulle «porte = zone IMQ» (la domanda, le categorie, il tema della mappa e la scheda);
resta valido tutto il resto (parcheggi considerati, posti nominali, stato di riempimento, osservazioni a mano, tipi di grafico, colori, regole di lavoro).
Esegui **tutte le fasi di seguito, senza fermarti a chiedere**. Dopo ogni fase scrivi in `docs/ESITO_R6_DIREZIONI.md` `FASE n: OK` o `FASE n: FERMO – motivo`.
Se un controllo numerico non torna: correggi se la causa è tua e chiara; altrimenti **non inventare**, scrivi cosa hai visto, salta quella parte e continua. Claude controlla tutto nel browser alla fine.

## 0. Cosa non andava (perché questo piano)

1. In scheda: «117.208 auto in entrata» (più delle 95.297 vere) e «11.881 auto che non trovano posto» erano **gonfiati**: ogni spostamento era contato due volte e i **quartieri di Torino** erano trattati come punti di partenza, mentre per loro l'indagine conta le auto che **arrivano**. Le prime posizioni (Barriera di Milano, San Donato, Borgata Vittoria…) erano quartieri di destinazione, non porte.
2. Leo (19/10): i quartieri di Torino fuori dal centro **non vanno esclusi**: l'obiettivo è **togliere auto dalla circolazione** facendole lasciare a un interscambio per proseguire con il trasporto pubblico.
3. Nella mappa: troppi pallini, e la stessa scala rosso-giallo-verde usata per cose diverse nella stessa legenda. Il verde→rosso era una direzione, non una regola ferrea.
4. Nella scheda i **criteri di scelta** devono essere tutti sotto gli occhi, per giudicare se vanno bene.
5. Alla prima apertura della mappa compare un banner rosso «Errore nella pagina… drawImage… canvas… width or height of 0» (preesistente): non è presentabile.

## 1. Decisioni di Leo e di Claude (fisse)

- **Domanda**: «Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico?» — per capire dove mettere un parcheggio nuovo o ingrandirne uno.
- **Una «porta» è una direzione d'ingresso**: la città è divisa in **8 settori** attorno a Piazza Castello (45,0711; 7,6857), da nord in senso orario (N, NE, E, SE, S, SW, W, NW, ognuno largo 45°, centrato sulla direzione).
  Un settore comprende **comuni e quartieri di Torino** (fuori dal centro Q001 per le fermate; i parcheggi contano ovunque). **Ogni auto, ogni parcheggio e ogni fermata cade in un solo settore**: niente doppi conteggi, i totali tornano.
  Motivo: ogni spostamento ha una direzione d'arrivo; così si trattano nello stesso modo comuni e quartieri e l'idea di «asse d'ingresso» è uniforme (ogni direzione elenca le sue strade d'ingresso).
- **Domanda di interscambio** (auto che potrebbero lasciare l'auto) = auto che entrano in Torino al mattino (IMQ 2022) × **quota** 26% (= 24.459 ÷ 95.297, auto che già oggi cambiano con un mezzo pubblico; 299 interviste [DATI SCARSI]) → **24.459 auto in tutto** (controllo: la somma sui settori deve dare questo numero).
- **Posti utili** (offerta) = posti dei parcheggi entro 200 m da una fermata importante, ridotti dal riempimento (regole già in `PIANO_R6_PORTE.md`: misurato, osservazione a mano, nominale).
- **Categoria della direzione** = posti utili ÷ domanda: **Bastano** ≥ 100% · **Quasi** 50-99% · **Pochi** 20-49% · **Mancano** < 20% (come prima).
- **Tre sottotemi** nella mappa, uno alla volta (menu «Cosa vedere»), ognuno con **una sola scala di colori** e la sua legenda.
- Nel testo pubblico mai: «v1/v2», «versione», «scenario», «S2», «classi» dei parcheggi, eventi, «doppio conteggio», confronti con risultati precedenti.

## 2. Definizioni (da implementare esattamente così)

- **Fermate importanti** (luoghi critici): i 378 attuali di `mappa_r6.json` (`luoghi`), non cambiare l'elenco.
- **Parcheggi considerati** e **stato di riempimento**: come in `PIANO_R6_PORTE.md` §2 (tipi aperti, `posti`, `posti_origine`, osservazioni da `data/ref/parcheggi_osservazioni.json`, misura da `riempimento.json` con G ≥ 0,85 pieno / < 0,50 libero / altrimenti a metà).
- **Parcheggi della mappa e dell'offerta**: quelli entro 200 m da almeno una fermata importante (349 oggi, 160 con ≥ 50 posti).
- **Settore** di un punto = direzione dal centro: `angolo = (atan2(Δx, Δy) in gradi + 360 + 22,5) mod 360`, `settore = floor(angolo / 45)` con `Δx = (lon − 7,6857)·cos(45,07°)`, `Δy = lat − 45,0711`; 0 = N, 1 = NE, … 7 = NW. Per una **zona IMQ** si usa il baricentro (media dei punti del contorno da `data/processed/imq_zone_geo.json`, ordine `[lat, lon]`).
- **Auto in entrata per settore**: dai microdati `data/processed/imq/spostamenti.csv` con **la stessa funzione e lo stesso filtro dello script 73** (carica `scripts/73_segnali_criticita.py` con `importlib` e usa `zone_c2_c3()`; auto in entrata al mattino = mezzo 03/04/21, origine non `Q…`, arrivo `Q…`, partenza 06:00-09:59, pesi `PESO`). Usa **solo le zone d'origine non `Q`** (le `Q` nel risultato sono arrivi): somma per settore del baricentro della zona d'origine. **Controllo**: somma sui settori = **95.297** (±1).
- **Offerta per settore**: somma dei `posti_utili` dei parcheggi della mappa, ognuno nel settore delle sue coordinate (un parcheggio una sola volta).
- **Fermate per settore**: 378 distribuite per le coordinate; `n_senza_parcheggio` (0 posti nominali entro 200 m), `n_pochi` (1-49), `n_50piu`.
- **Nome del settore**: «Nord», «Nord-est», … più i 3 comuni/zone d'origine con più auto in quel settore («Ovest — Collegno, Rivoli, Grugliasco»); i nomi dei comuni da `imq_zone.json` (`denom`, in forma normale: «Rivalta di Torino»).
- **Strade d'ingresso del settore** (informazione, [STIMATO ±38%]): con `trova_strada` del modulo `scripts/77_strade_comuni.py` (via `importlib`) per ogni fermata importante del settore, tieni le strade con `asse_ingresso` vero, raggruppa per asse e riporta le 3 con più `veic_giorno` (due sensi) di `tratte_traffico.json`: nome (solo per leggere), classe, veicoli/giorno.
- **Dove intervenire** (per settore): le 5 fermate **senza parcheggio** con punteggio più alto (nome, zona, punteggio) e i 5 **parcheggi pieni** (osservazione o misura) con più posti (nome, posti, fonte); in più la lista per zona IMQ delle fermate senza parcheggio (zona, quante).
- **Classifica** dei settori per `mancano` = max(0, domanda − posti utili).
- **Sensibilità** (calcolata dallo script, per la tabella dei criteri): ricalcola le categorie dei settori e i conteggi delle fermate con
  quota 15% / 26% / 40%; distanza 100 / 200 / 400 m; 20 / 25 / 33 m² a posto; 6 / 8 / 12 settori; soglia fermate importanti 5% / 10% / 15% (dai punteggi per luogo in `scenari.json`, chiave `scenari.S2.punteggi`; se non ci sono, salta questa riga e scrivilo).

---

## FASE 1 — Script `80_porte_interscambio.py` (rifarlo)

1. Riscrivi lo script secondo la sezione 2. Output: `data/processed/risultato6_v2/porte.json` (chiave `direzioni`: 8 settori con tutti i campi sotto; `fermate`; `parcheggi`; `sensibilita`; `criteri`; `riepilogo`) e `docs/RAPPORTO_R6_PORTE.txt` (tabella dei settori in ordine di `mancano`: nome, auto in entrata, domanda, posti nominali, posti utili, copertura, categoria, fermate senza parcheggio / pochi / 50+, strade d'ingresso; poi i totali, la sensibilità, i limiti).
2. Campi di ogni direzione: `codice` (0-7), `nome`, `angolo_da`, `angolo_a` (gradi), `comuni_principali`, `auto_in_entrata`, `interviste`, `domanda`, `posti_nominali`, `posti_utili`, `posti_pieni`, `quota_posti_misurati`, `copertura`, `mancano`, `categoria`, `n_fermate`, `n_senza_parcheggio`, `n_pochi`, `n_50piu`, `dove_intervenire`, `strade_ingresso`.
3. `criteri`: lista di righe `{nome, valore, perche, effetto}` con **numeri veri** calcolati dallo script (vedi sezione 4 per i testi). `riepilogo`: numeri chiave, conteggi per categoria, top direzioni per `mancano`, top 10 fermate senza parcheggio per punteggio, parcheggi pieni con più posti, profili 24 ore di 4-5 parcheggi grandi misurati (Stura, Porta Susa FS, Sofia, Venchi Unica, Caio Mario), `giorni_feriali_validi`, quota posti misurati.
4. **Controlli** (se non tornano: FERMO su questa fase): 378 fermate; 147 / 59 / 172 (nessuno / 1-49 / 50+); somma `auto_in_entrata` = 95.297 (±1) e somma `domanda` = 24.459 (±5); somma `posti_utili` dei settori = somma dei `posti_utili` dei parcheggi (nessun parcheggio doppio); ogni valore ≥ 0; con `--senza-osservazioni` la direzione che contiene Fermi (45,0766; 7,5903) ha copertura **maggiore**.
   Scrivi nell'esito la tabella dei settori e **quale settore contiene Fermi**; dì se risulta in «Pochi» o «Mancano» (non è un errore se no).

## FASE 2 — `79_dati_mappa_r6.py` (file per mappa e scheda)

`mappa_r6.json` contiene: `direzioni` (campi sopra, senza i `criteri`), `fermate` (378: `id, nome, lat, lon, zona, punteggio, categoria, posti_nominali_200, direzione, parcheggi:[{id,nome,dist_m,posti,stato}]` max 6), `parcheggi` (349: `id, nome, lat, lon, posti, posti_origine, a_pagamento, stato, riempimento_giorno, fonte_stato, direzione, profilo_feriale[24]|null`), `riepilogo`, `criteri`, `etichette`, `fonti`, `generato`.
Rimuovi ogni campo `porte`/`poligoni`. Peso < 1,5 MB. Controlli: carica con `json.load`; conteggi uguali alla Fase 1.

## FASE 3 — Mappa: tema «Parcheggi di interscambio» con tre sottotemi

`scripts/04_genera_mappa.py`: stessa chiave `r6`, messaggio a stampa con direzioni/fermate/parcheggi. In `scripts/mappa_template.html` **rifai** il tema `interscambio` (stesso id e link `#tema=interscambio`):

**3.1 Menu «Cosa vedere»** (unica opzione, `r6Vista`, rimessa in `OPZIONI`, `OPT_VAL` = `"parcheggi"`, `HANDLERS` come gli altri; `opzioni:["r6Vista"]`):
- `parcheggi` → «I parcheggi che ci sono»
- `non_bastano` → «Dove i parcheggi non bastano»
- `mancano` → «Dove non ci sono parcheggi»
La descrizione del tema cambia con la vista (`tema.desc`, come fa già `impostaSubServizio`): 
- parcheggi: «I parcheggi vicino alle fermate importanti: quanto sono grandi e quanto si riempiono di giorno.»
- non_bastano: «Per ogni direzione da cui si entra in città: i posti utili bastano per le auto che potrebbero lasciare l'auto?»
- mancano: «Le fermate importanti che non hanno nessun parcheggio vicino, in ordine di importanza.»

**3.2 Disegno** — `disegnaR6(ws,ox,oy)` disegna **solo** ciò che serve alla vista scelta:
1. **Vista «parcheggi»** — solo parcheggi con **≥ 50 posti** (≈ 160) più tutti quelli **pieni**; cerchio con raggio `3 + √posti/6` (max 14 px), **colore = riempimento di giorno** (una sola scala): libero `#1a9850`, a metà `#fee08b`, pieno `#d73027`, non misurato `#9aa3b2`; bordo bianco; **tratteggiato** se i posti sono stimati. Niente fermate, niente aree.
2. **Vista «non_bastano»** — gli 8 **settori** come spicchi di cerchio attorno a Piazza Castello (raggio 22 km, angoli `angolo_da`-`angolo_a`), riempiti con **una sola scala sequenziale di un solo colore** per la mancanza di posti: Bastano `#f3efe6` (quasi trasparente), Quasi `#f6d9a8`, Pochi `#ee9f5b`, Mancano `#c0562b`; bordo sottile; **etichetta** (nome del settore + categoria) al 60% del raggio, sempre visibile. Sopra, solo i **parcheggi pieni** (puntino nero con bordo bianco, raggio come sopra). Niente fermate.
3. **Vista «mancano»** — solo le **fermate importanti con 0 posti** (`#7b2d8e` viola scuro, raggio 6 px) e **con 1-49 posti** (`#d99ac9` viola chiaro, raggio 4 px); le altre non si disegnano. Le 15 con punteggio più alto hanno il numero (1-15) dentro il cerchio e la legenda elenca nome e zona. Niente parcheggi, niente aree. (Colori diversi dalle altre due viste: qui si guarda una sola cosa, «dove non c'è parcheggio».)
Cerchio di **200 m** (in `disegnaR6Sopra`) attorno alla fermata o al parcheggio selezionato. Da zoom < 11 nessun punto singolo se sono più di 300 visibili (mostra solo le etichette dei settori nella vista `non_bastano`).

**3.3 Tocco / passaggio del mouse** (blocco «0ter» di `cercaTip`, solo gli elementi della vista attiva):
- **settore** (clic dentro lo spicchio; vista `non_bastano`): titolo = nome; valore = categoria in parole («Mancano posti: copertura 12%»); dettagli = auto che entrano al mattino [STIMATO, IMQ 2022], auto che potrebbero lasciare l'auto, posti utili e nominali, **mancano ~N auto**, fermate importanti (senza parcheggio / pochi / 50+), quota di posti con riempimento misurato; «Dove intervenire» (5 fermate senza parcheggio + 5 parcheggi pieni); «Strade d'ingresso principali» con traffico stimato; una riga di metodo;
- **fermata importante** (vista `mancano`): nome, zona, punteggio, posti entro 200 m, elenco dei parcheggi vicini (nome, distanza, posti, stato), direzione;
- **parcheggio** (viste `parcheggi` e `non_bastano`): nome, posti (dichiarati o stimati [STIMATO]), tariffa, stato di riempimento con fonte («pieno di giorno [MISURATO]», «pieno [OSSERVAZIONE di Leo]», «a metà», «con posti liberi», «non misurato»), mini-curva SVG 24 ore con «[DATI SCARSI: 2 giorni feriali]» se c'è.

**3.4 Legenda** (una sola scala per vista, i numeri sempre scritti):
- parcheggi: «Riempimento di giorno (feriale)»: 4 colori con la soglia («pieno: almeno 85%», «a metà», «con posti liberi: meno del 50%», «non misurato»), grandezza = posti, tratteggiato = posti stimati dalla superficie [STIMATO], «Misurato su 2 giorni [DATI SCARSI]; Fermi segnato pieno a mano [OSSERVAZIONE di Leo]»;
- non_bastano: «Posti utili rispetto alle auto che potrebbero lasciare l'auto»: 4 passi con le soglie («Bastano: almeno il 100%», «Quasi: 50-99%», «Pochi: 20-49%», «Mancano: meno del 20%») e il numero di direzioni per categoria; puntino nero = parcheggio pieno;
- mancano: «Fermate importanti senza parcheggio»: viola scuro «nessun parcheggio entro 200 m (N)», viola chiaro «meno di 50 posti (N)»; elenco delle prime 15 con numero, nome, zona.
Ogni legenda scrive la riga delle fonti e dei tag. **Guida**: riscrivi il paragrafo del Risultato 6 (5-6 frasi) con i criteri in parole semplici (vedi sezione 4) e rimanda alla scheda per il dettaglio.

**3.5 Banner d'errore** — correggi la causa: in `disegna()` (riga ≈867, `drawImage` di un canvas con larghezza o altezza 0) aggiungi un controllo: se il canvas di destinazione/sorgente ha `width===0 || height===0` esci senza disegnare e richiama `chiede()` al prossimo `ridimensiona`; verifica che il banner non compaia più aprendo `mappa_torino.html`, `#tema=servizio` e `#tema=interscambio` (scrivilo nell'esito; se non riesci a riprodurre l'errore, descrivi il controllo aggiunto).

**3.6** Rigenera con `python scripts\04_genera_mappa.py`; `node --check` sugli `<script>`; nell'esito il peso di `mappa_torino.html`.

## FASE 4 — Scheda in `simulazione.html` (`scripts/schede_risultati.py`)

**4.1 Impostazione a domande e risposte**, nell'ordine: *Qual è la domanda? → La risposta in breve → I numeri → I criteri, uno per uno → Il metodo → I limiti*.
- `domanda`: «Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico?»
- `numero_chiave`: **auto che non trovano posto** = somma dei `mancano` dei settori (valore calcolato, ≤ 24.459), unità «auto», testo «al giorno: auto che potrebbero lasciare l'auto in un interscambio e non trovano posto, sommando le direzioni dove i posti non bastano».
- `risposta` (4 frasi, numeri veri, **senza** «doppio conteggio», **senza** «0 fermate…»): 1) ogni mattina entrano in Torino circa **95.300** auto [STIMATO IMQ 2022]; circa **24.500** potrebbero lasciarla e proseguire con i mezzi pubblici (la quota di chi già oggi lo fa); 2) le direzioni dove mancano più posti (le 2-3 prime: nome, mancano ~N) e quante su 8 sono in «Mancano»/«Pochi»; 3) delle 378 fermate importanti **147** non hanno nessun parcheggio a 200 m e **59** ne hanno meno di 50; 4) **N parcheggi sono già pieni di giorno** (X posti) [MISURATO + OSSERVAZIONE di Leo]; le misure coprono solo il Y% dei posti.

**4.2 Nuova sezione «I criteri, uno per uno»** — in `simulazione.html`, in `apri(i)`: se `s.criteri` è un array non vuoto, aggiungi la sezione (dopo «Grafici», prima di «Il metodo») con una **tabella a 4 colonne** (Criterio · Valore usato · Perché · Cosa cambia se lo cambiamo), righe da `s.criteri` (`{nome, valore, perche, effetto}`), stile come `table.param`, su schermo stretto le righe diventano blocchi. In `schede_risultati.py` `criteri` si legge da `porte.json` (`criteri`). Le righe, con questi testi di base (i numeri li inserisce lo script):
1. **Fermate importanti** — *10% più alto* del punteggio, su 4.425 luoghi della Città metropolitana (378) — *perché*: sono i punti dove passa più gente e più mezzi; il punteggio mescola 7 segnali: importanza della strada, corse nelle ore dei pendolari, pendolari della zona, ZTL, calo di velocità, nodo treno/metro — *effetto*: con 5% sarebbero N, con 15% M.
2. **Parcheggi contati** — *tutti i parcheggi aperti (5T, Comune, OpenStreetMap)*, con i numeri per fonte e quanti esclusi (privati, solo clienti, lungo strada) — *perché*: per ogni auto conta ogni posto dove può fermarsi tutto il giorno — *effetto*: i parcheggi di OpenStreetMap sono incompleti, il numero reale è maggiore.
3. **Posti** — *dichiarati, o stimati a 25 m² a posto* (N di M parcheggi stimati) — *perché*: spesso il numero di posti manca — *effetto*: con 20 m² i posti stimati salgono del 25%, con 33 m² scendono del 24%; la categoria di K direzioni cambia.
4. **Distanza** — *200 m in linea d'aria* — *perché*: oltre non si lascia l'auto per prendere il mezzo — *effetto*: a 100 m le fermate senza parcheggio passano da 147 a A, a 400 m a B.
5. **Riempimento** — *misurato dove il 5T lo trasmette (2 giorni feriali, 10-16); pieno ≥ 85%; nota a mano per Fermi* — *perché*: un parcheggio pieno non serve — *effetto*: senza la nota su Fermi la direzione X avrebbe copertura Y% invece di Z%; i dati coprono solo W% dei posti.
6. **Auto che entrano** — *indagine IMQ 2022, mattino 6-10, in auto, verso Torino*: 95.297 spostamenti da 1.139 interviste — *perché*: è la domanda di spostamento misurata — *effetto*: campione piccolo per zona; sommando le zone di una direzione l'errore cala.
7. **Quota che lascia l'auto** — *26%* (chi oggi già cambia con un mezzo pubblico, 299 interviste) — *perché*: è l'unico dato misurato — *effetto*: con 15% le direzioni «Mancano»/«Pochi» sarebbero A, con 40% B (mostra le tre colonne in una frase).
8. **Direzioni d'ingresso** — *8 settori da Piazza Castello* — *perché*: ogni auto, parcheggio e fermata finisce in una sola direzione, comuni e quartieri insieme — *effetto*: con 6 settori … con 12 … categorie.
9. **Categorie** — *Bastano ≥ 100%, Quasi 50-99%, Pochi 20-49%, Mancano < 20%* (posti utili ÷ auto che potrebbero lasciare l'auto) — *perché*: soglie semplici — *effetto*: la scelta delle soglie è convenzionale.
10. **Strade d'ingresso** — *solo informazione, traffico stimato ±38%* — non entrano nel calcolo.
I valori sono quelli reali dello script; se una sensibilità non è calcolabile scrivi «non calcolato» nella cella.

**4.3 Grafici** (solo questi; titoli brevi; `tono`/palette secondo le viste: una scala per grafico):
1. `barre` «Dove mancano più posti (auto al giorno)» — le 8 direzioni per `mancano` (`tono` secondo la categoria: Mancano rosso `#c0562b`… usa i `tono` esistenti `rosso/arancio/giallo/verde`);
2. `barre` «Auto che potrebbero lasciare l'auto e posti utili, per direzione» — due voci per direzione (`prima`=domanda, `valore`=posti utili);
3. `pila` «Fermate importanti e parcheggi a 200 m» — nessun parcheggio / pochi posti / 50 o più (3 toni);
4. `barre` «Fermate senza parcheggio per zona» — le 10 zone con più fermate senza parcheggio;
5. `profilo` «Quanto si riempiono i parcheggi più grandi» — serie dai profili 24 ore, nota [MISURATO], 2 giorni feriali;
6. `barre` «Parcheggi già pieni di giorno» — i 10 con più posti, con la fonte.
`immagini`: come prima (`r6_torino.png`, `r6_zoom.png`, le fa Leo).
**4.4** `metodo` (5-6 frasi, derivate dai criteri), `parametri` (sezione 2), `limiti`: riempimento su 2 giorni feriali [DATI SCARSI]; parcheggi OpenStreetMap incompleti e posti stimati ±30%; indagine IMQ campionaria; la direzione non sa del percorso reale delle auto; una nota a mano (Fermi) vale al posto di una misura; distanze in linea d'aria; traffico delle strade ±38%. **Mai** «doppio conteggio», «versione», «scenario».
**4.5** Rilancia `python scripts\schede_risultati.py`, `node --check data\schede_risultati.js`. Controlla che la scheda R6 **non** contenga «versione», «scenario», «S2», «potenziale», «solo sulla carta», «Allianz», «doppio» e che i numeri siano coerenti col file.

## FASE 5 — Pulizia

Cerca e rimuovi i resti di `porte`/`poligoni`, `porta` (campo dei luoghi), «Barriera di Milano» come porta, ecc. in template, script e schede; `grep` dei termini vietati in `mappa_torino.html` e `data/schede_risultati.js`. Non cancellare i dati dei giri precedenti. Nell'esito: tabella delle direzioni, controlli, file modificati, anomalie.

## Cosa NON fare
- Non cambiare i 378 luoghi, la soglia, i dati di riempimento, né i parametri (200 m, 25 m², quota 26%, 8 settori, soglie delle categorie). Non toccare `MEMORIA_PROGETTO.md`, né i dati in `data/ref`.
- Non scrivere dati a mano nel template o nella scheda. Niente librerie esterne. Nessun commit. Non pubblicare.
