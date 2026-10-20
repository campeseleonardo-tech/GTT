# Piano — Risultato 1: dove mancano i servizi a piedi

Piano unico del risultato: in testa lo stato e i lavori da fare, sotto la storia. Scritto da Claude il 20/10/2026
dopo l'analisi di Leo (stessa data). Fase A fatta e ricontrollata (20/10); fase B (mappa) pronta, sotto.

## Stato attuale (versione 1, 12/10)

- Script: `21_risultato1_vuoti.py` (vuoti), `22_risultato1_candidati.py` (dove aggiungere un servizio); dati da
  `18_accessibilita.py` (`data/processed/accessibilita.json`). Rapporti: `docs/RAPPORTO_RISULTATO1.txt`,
  `docs/RAPPORTO_RISULTATO1_CANDIDATI.txt`. Scheda da `schede_risultati.py` (`scheda_r1`).
- Cinque gruppi: scuole, salute, «cibo» (in realtà tutte le attività commerciali del catalogo), fermate, verde.
  Per sezione di censimento: «zero» (nessuna destinazione a 15 minuti a piedi) o «pochissimo» (10% più basso).
- Titolo: **10.919 torinesi (1,3%) senza almeno uno dei 5 servizi**; il più carente è la salute (9.104).
- Fuori Torino scuole, salute e cibo **non sono confrontabili** (catalogo comunale solo per Torino, fuori c'è
  OpenStreetMap, più povero): zero spesso = dato mancante.

## Commenti di Leo (20/10) e controllo sui dati

| Commento | Controllo (dati dentro `mappa_torino.html`, sezioni con abitanti, superficie e «zero» per gruppo) | Fattibile? |
|---|---|---|
| Guardare dove mancano **tutti** i servizi | A Torino solo **8 residenti** non hanno nessuno dei 5; con 3 o più mancanti 2.469; con almeno 1 mancante 10.919 | Sì, subito (i dati ci sono già) |
| Escludere le zone **poco abitate** (parchi, collina, zone poco abitabili) | Dei 10.919, **8.916 vivono in sezioni sotto 2.000 ab/km²**; la sezione tipica di Torino ne ha 21.087. Il titolo di oggi misura soprattutto collina e periferie vuote | Sì, subito |
| Valutare la **cintura** diversamente («paese, non città dei 15 minuti») | Oggi in cintura tutto sembra rosso, ma è soprattutto mancanza di dato | Sì, con un calcolo nuovo (accessibilità col mezzo pubblico già calcolata dallo script 18) |
| Salute e scuole: ospedali grandi contro presidi piccoli, scuole grandi contro piccole | Capienza e iscritti non li abbiamo | Solo come limite dichiarato |

## Decisioni di Leo (20/10)

1. **Criticità = quanti servizi mancano (0-5)** per sezione: mappa a gradini; titolo = residenti con **3 o più**
   servizi mancanti; «tutti mancanti» resta come riga (8 persone, non fa titolo).
2. **Zone poco abitate in grigio, fuori dal titolo**: soglia predefinita **1.000 ab/km²**, con sensibilità a 500 e
   2.000; i loro residenti si dicono a parte.
3. **Cintura con una regola diversa**: Torino = 15 minuti a piedi; cintura = servizio raggiungibile **a piedi in 15
   minuti o col mezzo pubblico**, sempre in tabelle separate. Nota di Claude (20/10): il calcolo esistente (script 18)
   ha il mezzo pubblico solo **entro 45 minuti**, ora per ora; default = **45 minuti alle 8 di un feriale** (già
   calcolato). Un limite più stretto (es. 20 minuti) richiede di rifare l'accessibilità (diverse ore): solo se Leo
   lo chiede.

## Prima stima (Claude, 20/10, dai dati in mappa; da rifare con lo script)

| Soglia «poco abitata» | Torino: residenti in zone poco abitate | Torino: 3+ mancanti (abitate) | Torino: 1+ mancante (abitate) | Fuori Torino: 3+ mancanti (abitate, regola di oggi) |
|---|---|---|---|---|
| 500 ab/km² | 2.875 | 1.821 | 9.566 | 28.297 |
| **1.000 ab/km²** | 6.768 | **751** | 7.017 | 23.318 |
| 2.000 ab/km² | 17.039 | 389 | 2.003 | 8.739 |

Quello che emerge: **Torino è quasi tutta una città dei 15 minuti**; le carenze vere sono poche centinaia di
residenti, e vanno guardate una a una (dove sono, quale servizio manca). È un risultato più forte e onesto di
«10.919 senza servizi». La cintura con la regola di oggi resta non confrontabile: per questo serve la decisione 3.

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Conteggio 0-5 per sezione, soglia di densità con sensibilità (500/1.000/2.000), «poco abitata» come stato a parte | `21_risultato1_vuoti.py` (nuove uscite, le vecchie restano) | piccolo |
| 2 | Cintura: per scuole, salute, cibo usare il tempo col mezzo pubblico (già in `accessibilita.json`) oltre ai piedi; tabelle sempre separate | 21 | medio (controllare prima che i tempi TP per gruppo ci siano davvero) |
| 3 | Rinominare «cibo» in «negozi e attività commerciali» anche nella scheda (in mappa già fatto il 20/10) | `schede_risultati.py` | piccolo |
| 4 | Mappa: tema servizi con i gradini 0-5 (verde→rosso) e il grigio per le zone poco abitate; legenda con i numeri | `04_genera_mappa.py`, `mappa_template.html` | medio |
| 5 | Scheda: titolo nuovo (residenti abitati con 3+ mancanti), «tutti mancanti» come riga, residenti delle zone poco abitate a parte, sensibilità della soglia, limiti (capienza di ospedali e scuole non nota) | `schede_risultati.py` | piccolo |
| 6 | Candidati per nuovi servizi (22): rifarli solo sulle sezioni abitate | 22 | piccolo |
| 7 | Controllo con la realtà: 5-10 sezioni «critiche» guardate a mano con Leo (sono davvero senza servizi?) | — | 1 sessione |

Limite da scrivere sempre: capienza di ospedali, presidi e scuole non nota (un ospedale grande e un ambulatorio
contano uguale); orario programmato; catalogo diverso fra Torino e cintura.

## Come eseguirlo (fase A: calcoli e scheda; fase B: mappa, dopo)

Fase A = lavori 1, 2, 3, 5, 6. Fase B = lavoro 4 (mappa), da fare dopo aver visto i numeri della fase A.
Esito in `docs/ESITO_RISULTATO1_V2.md`; poi Leo fa commit e push e Claude ricontrolla.

### Passi meccanici della fase A (per il modello minore)

1. Prima: ramo `prova`, `git status` pulito, `git pull origin prova`. Alla fine commit e push da solo (`AGENTS.md`). Python del PATH.
2. `scripts/21_risultato1_vuoti.py`: **non cambiare** le uscite di oggi; **aggiungi** nel JSON
   `data/processed/risultato1_vuoti.json` una sezione `"v2"` e nel rapporto una sezione «VERSIONE 2»:
   - per ogni sezione: `n_mancanti` = quanti dei 5 gruppi sono a «zero» (piedi 15 min);
   - densità = residenti / km²: la superficie è il campo `"a"` (km²) di `data/processed/sezioni_torino.json`,
     agganciata per `"id"`; costante `SOGLIA_POCO_ABITATA = 1000` (ab/km²) e sensibilità 500 e 2.000;
   - Torino (sezioni con id che inizia per `1272`): residenti per `n_mancanti` 0..5, separati in «abitate» e «poco
     abitate»; titolo = residenti **abitati** con `n_mancanti >= 3`; riga «tutti e 5 mancanti»;
   - cintura: per scuole, salute, cibo un gruppo manca solo se è a zero **sia** a piedi 15 min **sia** col mezzo
     pubblico entro 45 minuti all'ora `"08"` (campo `"tp"` di `accessibilita.json`: guarda le chiavi con
     `python -c "import json;d=json.load(open('data/processed/accessibilita.json',encoding='utf-8'));s=d['sezioni'][0] if 'sezioni' in d else d[0];print(s.keys(), s['tp'].keys())"`
     e adatta il nome della lista se è diverso); fermate e verde come Torino; tabelle sempre separate da Torino.
   - Controlli (stampa OK/AVVISO): somma dei residenti per `n_mancanti` = residenti totali dell'ambito; nessuna
     densità negativa; sezioni senza superficie contate e scritte (AVVISO se più di 10).
   - Numeri attesi solo come controllo di buon senso (non scriverli nel codice): Torino, soglia 1.000, abitati con 3+
     mancanti dell'ordine di 700-800; residenti in zone poco abitate circa 6.800.
3. `scripts/22_risultato1_candidati.py`: i candidati per nuovi servizi solo su sezioni abitate (densità ≥ soglia):
   aggiungi il filtro e scrivi nell'esito quanti candidati cambiano.
4. `scripts/schede_risultati.py`, `scheda_r1`: il numero in grande diventa i residenti abitati con 3+ mancanti
   (letti dal JSON, mai scritti a mano); «cibo» si chiama «negozi e attività commerciali»; aggiungi un grafico a
   barre «Residenti per numero di servizi mancanti (0-5), zone abitate» e una riga con i residenti delle zone poco
   abitate; sensibilità della soglia (500/1.000/2.000) nei criteri; limite «capienza di ospedali e scuole non nota».
   Aggiorna `in_english` con gli stessi numeri.
5. `python scripts\21_risultato1_vuoti.py`, `python scripts\22_risultato1_candidati.py --gruppi salute,scuole`,
   `python scripts\schede_risultati.py`, `python scripts\prova_pagine_r6.py --senza-screenshot` (0 errori).
6. Nell'esito: la sezione «VERSIONE 2» del rapporto, le righe cambiate, `git status`.

### Prompt da incollare (per Leo)

> Sei un agente che lavora sul progetto GTT in `C:\projects\Progetti\GTT`, ramo git `prova`. Prima:
> `git branch --show-current` (deve dire `prova`), `git status` (se ci sono modifiche fermati e dimmelo),
> `git pull origin prova`. Leggi `AGENTS.md` e `docs/PIANO_RISULTATO1.md`, poi esegui la sezione «Passi meccanici
> della fase A», un passo alla volta. Aggiungi, non togliere: le uscite di oggi dello script 21 restano uguali. Niente
> numeri scritti a mano nei testi. Se un nome di campo è diverso da quello del piano, guarda il file vero, adatta e
> scrivilo. Scrivi tutto in `docs/ESITO_RISULTATO1_V2.md` (OK / AVVISO / FERMO per passo, righe cambiate, numeri).
> Alla fine fai commit e push come dice `AGENTS.md` (sezione «Commit»); se lavori nel cloud (niente `data/`), fai
> solo le modifiche al codice, salta i passi che lanciano gli script e scrivilo nell'esito. Non modificare `MEMORIA_PROGETTO.md`. Python: `python` del PATH, mai Anaconda. Alla fine un
> riassunto di 10 righe in italiano semplice.

## Fase B — mappa a gradini 0-5 (piano del 20/10 sera)

Fase A fatta e ricontrollata (numeri nel rapporto, sezione «VERSIONE 2»: Torino 751 abitati con 3+ mancanti, 6.768
in zone poco abitate, 8 con tutti e 5; cintura con la regola v2 834). Nelle zone abitate di Torino nessuno ha 4 o 5
servizi mancanti: i gradini 4-5 a Torino compaiono solo nel grigio.

### Scelte (Leo, 20/10 sera: valori predefiniti accettati)
1. Tema «Dove mancano i servizi», menu «Servizio essenziale»: prima voce nuova **«Quanti servizi mancano (0-5)»**
   (vista di partenza); poi le 5 voci per gruppo, come oggi, con i cerchi dei candidati.
2. Torino e cintura nella stessa mappa, stessi gradini; la cintura con la sua regola (a piedi 15 min **o** mezzo
   pubblico 45 min alle 8), detta in legenda e nel pannello.
3. Soglia «poco abitata» fissa a 1.000 ab/km² in mappa (letta dal JSON); la sensibilità resta nella scheda.
4. Colori (bene/male): 0 `#e3f0df` (verde chiarissimo, come oggi l'«ok»), 1 `#fee08b`, 2 `#fdae61`, 3 `#f46d43`,
   4 `#d73027`, 5 `#a50026`; zone poco abitate grigio `#9aa0ad` trasparenza 0,35 (come «nessun dato»).
5. Nelle viste per gruppo il rosso «manca» segue la **regola v2** (in cintura conta anche il mezzo pubblico), non più
   il «zero» della v1; l'arancione «pochissimi» resta quello della v1; le zone poco abitate sono grigie.

### Migliorie aggiunte da Claude (ripensando il piano)
- Lo script 21 scrive anche **quali** servizi mancano (non solo quanti): serve al pannello e alle viste per gruppo.
- Lo script 21 scrive l'**elenco delle sezioni critiche** di Torino (abitate, 3+ mancanti): è la base del lavoro 7
  (controllo con la realtà con Leo), oggi senza dati pronti.
- Lo script 04 controlla che la mappa dia lo stesso titolo dello script 21 (751): AVVISO se diverso.

### Passi meccanici della fase B (per il modello minore, sul PC)

Regole: come nella fase A (ramo `prova`, `git status` pulito, `git pull origin prova`, Python del PATH, commit e push
da solo, niente numeri scritti a mano). Un passo alla volta; dopo ogni passo nell'esito `docs/ESITO_R1_MAPPA.md`:
`PASSO x: OK / AVVISO / FERMO – motivo` e le righe cambiate (file, prima, dopo). Non toccare altri temi della mappa.

**Passo 1 — `scripts/21_risultato1_vuoti.py` (solo aggiunte).**
1. In `n_mancanti_sezione` costruisci anche una maschera di bit `m`: il bit `i` è acceso se il gruppo `GRUPPI[i]` manca
   con la regola v2 (`scuole`=1, `salute`=2, `cibo`=4, `fermate`=8, `verde`=16). Ritorna `(n_v2, n_piedi, tp_ok, m)` e
   adatta l'unica chiamata in `calcola_v2`. Controllo nel codice: il numero di bit accesi = `n_v2` (OK/AVVISO stampato).
2. In `calcola_v2`, in `per_sez.append(...)` aggiungi `"m": m` e `"poco": d is not None and d < SOGLIA_POCO_ABITATA`.
3. In `v2` aggiungi `"ordine_bit": GRUPPI` e `"sezioni_critiche_torino"`: le sezioni di Torino abitate con
   `n_mancanti >= SOGLIA_TITOLO`, ordinate per residenti decrescenti, ognuna con `id`, `res`, `densita`, `n_mancanti` e
   `mancano` (nomi dei gruppi). Controllo: la somma dei loro `res` = `v2.titolo.residenti_abitati_con_3_o_piu_mancanti`
   (OK/AVVISO).
4. In `righe_rapporto_v2` aggiungi in coda «SEZIONI CRITICHE DI TORINO (abitate, 3+ mancanti)»: una riga per sezione
   (id, residenti, ab/km², servizi che mancano), poi «da guardare a mano con Leo (lavoro 7)».

**Passo 2 — `scripts/04_genera_mappa.py`.**
1. Nel blocco «risultato 1» (cerca `fb_zero = {}`), dopo la lettura di `fb_data`: se c'è `fb_data["v2"]`, costruisci
   `r1 = {x["id"]: [x["n_mancanti"], x["m"], 1 if x["poco"] else 0] for x in fb_data["v2"]["sezioni"]}` e
   `r1_meta = {"soglia": v2["soglia_poco_abitata_ab_km2"], "ora_tp": v2["ora_tp_cintura"], "ordine": v2["ordine_bit"],
   "titolo": v2["titolo"]["residenti_abitati_con_3_o_piu_mancanti"]}`. Se manca `v2`: `r1 = {}`, `r1_meta = None` e
   una riga «AVVISO: lancia prima 21_risultato1_vuoti.py».
2. Nella costruzione di `sez` (cerca `"fb": fb_zero.get(`) aggiungi `"r1": r1.get(x.get("id",""))`.
3. Nel dizionario dei dati della mappa (cerca `"fb_candidati": fb_candidati,`) aggiungi `"r1_meta": r1_meta,`.
4. Controllo stampato: somma di `p` delle sezioni con id che inizia per `1272`, `r1` presente, `poco == 0` e
   `n >= 3`; OK se uguale a `r1_meta["titolo"]`, altrimenti AVVISO con i due numeri. Stampa anche quante sezioni hanno
   `r1` (attese ~8.300 meno quelle senza abitanti).

**Passo 3 — `scripts/mappa_template.html`.**
1. Proiezione delle sezioni (cerca `fb:z.fb||{},` dentro `const sez = (D.sezioni||[]).map`): aggiungi `r1:z.r1||null,`.
2. Vicino a `PAL_SEZ.fb = [...]` aggiungi
   `PAL_SEZ.r1 = ["#e3f0df","#fee08b","#fdae61","#f46d43","#d73027","#a50026"];   // 0..5 servizi mancanti` e una
   funzione `r1Manca(z,g)` che ritorna `true` se il bit del gruppo `g` (posizione in `D.r1_meta.ordine`) è acceso.
3. Menu (cerca `subFbGruppo:{etichetta:"Servizio essenziale", voci:[`): prima voce `["tutti","Quanti servizi mancano (0-5)"],`.
   In `const OPT_VAL` cambia `subFbGruppo:"salute"` in `subFbGruppo:"tutti"`.
4. Disegno (cerca `const c=pc ? (pc.sogl?` e la riga con `fbGruppo ? (((z.fb||{})[fbGruppo]==="zero")`):
   - vista `tutti`: colore `PAL_SEZ.r1[z.r1[0]]`; se `z.r1` manca o `z.r1[2]===1` → grigio come `nulla`;
   - vista per gruppo: se `z.r1 && z.r1[2]===1` → grigio; altrimenti rosso se `r1Manca(z,g)`, arancione se
     `(z.fb||{})[g]==="pochissimo"`, verde chiarissimo negli altri casi (stessa `PAL_SEZ.fb`);
   - la palette usata per quella vista è `PAL_SEZ.r1` per `tutti`, `PAL_SEZ.fb` per i gruppi.
5. Legenda (`function legendaFb()`): per `tutti` titolo «Quanti servizi essenziali mancano · ${TAG.sim}», 6 riquadri
   etichettati «0», «1», … «5 (tutti)», un riquadro grigio «zona poco abitata (sotto N ab/km²), fuori dal conteggio»
   con N da `D.r1_meta.soglia` in formato italiano, e una riga: «Torino: a piedi in 15 minuti. Fuori Torino: a piedi
   in 15 minuti o con i mezzi pubblici in 45 (partenza alle 8 di un feriale); scuole, salute e negozi da
   OpenStreetMap, meno completi.» Per i gruppi: come oggi, ma «nessuno a 15 min a piedi» diventa «manca» e si aggiunge
   il riquadro grigio.
6. Pannello della sezione (`function schedaSezione`, ramo `modo === "fb"`): per `tutti` → `val` = «N servizi mancanti
   su 5» (o «Zona poco abitata: fuori dal conteggio»), `stato` = nomi dei servizi che mancano separati da virgola (o
   «nessuno»); per i gruppi `val` usa `r1Manca` («Manca» / «Pochissimi» / «Presente»). In entrambi i casi aggiungi ai
   dettagli «Abitanti per km²» (da `z.dens`, numero italiano senza decimali) e «Regola» («Torino: a piedi 15 min» o
   «Cintura: a piedi 15 min o mezzi pubblici 45 min»). Il testo di approfondimento del ramo `fam === "fb"` diventa:
   «Servizio mancante = nessuno raggiungibile (Torino: a piedi in 15 minuti; fuori Torino anche con i mezzi pubblici
   in 45). Zone sotto N ab/km² in grigio: parchi, collina, aree poco abitate.»
7. Tooltip al passaggio (cerca `nome="Dove manca un servizio"; extra="STIMATO";`): per `tutti` → «N mancanti» o «poco
   abitata»; per i gruppi «Manca» / «Pochissimo» / «Ok» con `r1Manca`.
8. Ovunque si legga `$("subFbGruppo")?.value||"salute"` con `tutti` non devono comparire candidati né `NOTA_OSM`
   (già vero: `fbCandidati["tutti"]` e `NOTA_OSM["tutti"]` non esistono); controllalo riga per riga e scrivi l'elenco
   delle righe nell'esito.
9. Descrizione del tema (cerca `{id:"faseb", label:"Dove mancano i servizi", desc:`): «Quanti servizi essenziali
   mancano vicino a casa (0-5), con le zone poco abitate in grigio; per ogni servizio, dove aggiungerne uno aiuterebbe
   più persone.»
10. Cerca nel template `pochissim` e `Dove mancano i servizi`: scrivi nell'esito ogni altra frase (guida, testi) che
    descrive il tema; cambia solo quelle che parlano di «zero/pochissimo» come unica vista.

**Passo 4 — `scripts/schede_risultati.py`, `scheda_r1`.**
1. `"mappa"`: `"nota"` diventa «Nella mappa, tema "Dove mancano i servizi": all'apertura quanti servizi mancano in
   ogni zona (0-5, zone poco abitate in grigio); nel menu un servizio alla volta, con i punti dove aggiungerne uno.»
2. Nell'`in_english` la frase «Limits: only the City of Turin is covered; outside it the service catalogue is missing…»
   va allineata alla v2 (cintura valutata con a piedi o mezzo pubblico, dato meno completo). Nessun numero scritto a mano.

**Passo 5 — Lanci (nell'ordine).**
`python scripts\21_risultato1_vuoti.py` → `python scripts\04_genera_mappa.py` → `python scripts\schede_risultati.py` →
`python scripts\prova_pagine_r6.py --senza-screenshot` (0 errori). Nell'esito: le righe OK/AVVISO di 21 e 04, la nuova
sezione «SEZIONI CRITICHE» del rapporto, la dimensione di `mappa_torino.html` prima e dopo (attesa +0,1/0,3 MB),
`git status`.

### Controlli di Claude dopo il giro
Mappa ricostruita in Chromium dal template con i dati di `mappa_torino.html`: vista di partenza 0-5, grigio, legenda,
pannello in Torino e in cintura, una vista per gruppo con i candidati, `#tema=faseb` dall'indirizzo, 0 errori in
console; titolo della mappa = 751; elenco delle sezioni critiche pronto per il lavoro 7.

### Prompt da incollare (per Leo, sul PC)

> Sei un agente che lavora sul progetto GTT in `C:\projects\Progetti\GTT`, ramo git `prova`. Prima:
> `git branch --show-current` (deve dire `prova`, altrimenti fermati e dimmelo), `git status` (se ci sono modifiche
> fermati e dimmelo), `git pull origin prova`. Leggi `AGENTS.md` e in `docs/PIANO_RISULTATO1.md` la sezione «Fase B»,
> poi esegui i «Passi meccanici della fase B», uno alla volta, nell'ordine. Cambia solo quello che i passi dicono;
> niente numeri scritti a mano nei testi; nessun altro tema della mappa. Se una riga da cercare non c'è o un nome è
> diverso, guarda il file vero, adatta e scrivilo. Scrivi tutto in `docs/ESITO_R1_MAPPA.md` (OK / AVVISO / FERMO per
> passo, righe cambiate prima/dopo, uscite dei controlli). Non modificare `MEMORIA_PROGETTO.md`. Python: `python` del
> PATH, mai Anaconda. Alla fine fai commit e push come dice `AGENTS.md` (sezione «Commit») e scrivi un riassunto di 10
> righe in italiano semplice, con il titolo che stampa lo script 04 e quanti errori ha trovato la prova delle pagine.

## Storia

- 11-12/10: piano dell'accessibilità (`docs/PIANO_ACCESSIBILITA.md`), giro completo il 12/10, fase A (vuoti) e
  fase B (candidati) con Leo. Bug corretto il 12/10: i gruppi erano confrontati su ambiti diversi (Torino contro
  Torino+cintura).
- 20/10: «Negozi di alimentari» rinominato in mappa (il gruppo usa tutte le 31.405 attività del catalogo).
