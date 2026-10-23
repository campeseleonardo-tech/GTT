# Piano 4 — Grafica, animazioni e racconto

Obiettivo: il sito colpisce nei primi 5 secondi e fa capire i risultati anche a chi non legge i testi.

Decisioni di Leo (22/10):
- i colori verde→rosso e blu→arancione erano una **direzione**, non una regola: si passa a **verde acqua → corallo**
  (non prioritario);
- **un file di stile** comune a tutte le pagine;
- **numeri che contano** solo nei numeri grandi e molto visibili, non in tutti (altrimenti dà fastidio);
- **omini e quadratini**, **gara bus contro auto** e **area che si espande** dentro le **schede**;
- **ore che scorrono** nella mappa; **mezzi in movimento** in home;
- il racconto «perché questo progetto» in una **pagina a sé**: `progetto.html`;
- sito in italiano con bottone **IT/EN** su home, risultati e progetto (la mappa resta in italiano).

Regole che restano: **numeri sempre scritti** accanto ai colori; animazioni spente per chi ha attivato «riduci movimento»
nel sistema; pagine che funzionano anche senza le animazioni.

## Dove va ogni elemento

| Elemento | Cos'è | Dove |
|---|---|---|
| **A. Mezzi in movimento** | sfondo scuro con la forma di Torino; i puntini di bus e tram veri (GPS del Pi) si muovono durante un'ora tipica, accelerata in circa 20 secondi, con l'orologio che scorre | **home**, in alto dietro il titolo |
| **B. Numeri che contano** | il numero sale da 0 al valore in circa 1 secondo quando appare | **solo**: il numero di ognuno dei 5 riquadri della home, il numero grande della scheda aperta, il contatore della raccolta (J). Nessun altro numero |
| **C. Omini e quadratini** | il numero grande disegnato: 10 omini con 1 colorato (scheda 5, «quasi 1 su 10»); 100 quadratini con 13 corallo (scheda 2, passaggi oltre 5 minuti); 12 pallini, uno per punto (scheda 3) | **scheda aperta**, sotto il numero grande |
| **D. Gara bus contro auto** | bus e auto partono insieme da uno dei 12 punti verso Piazza Castello; l'auto arriva prima, il bus dopo; tendina per scegliere il punto; i minuti scritti all'arrivo | **scheda 3** (parcheggi di scambio), grafico principale. Dati già pronti (script 94) |
| **E. Area che si espande** | due aree che crescono minuto per minuto: dove arrivi in 10, 20, 30, 45 minuti **coi mezzi** e **in auto**, alle 8. Si parte da **Piazza Castello**, con una tendina per scegliere **qualsiasi altra zona** (Leo, 22/10) | **scheda 4** (traffico e mezzi). Piazza Castello in dettaglio (per sezione: calcolo nuovo sul PC); le altre zone con i tempi zona-zona già calcolati dallo script 93 (controllare che il JSON abbia tutte le coppie, altrimenti il 93 salva la tabella completa) |
| **F. Ore che scorrono** | bottone ▶ che fa scorrere le ore dalle 6 alle 24 con passaggi morbidi di colore | **mappa**, nei temi che cambiano con l'ora |
| **G. Perché questo progetto** | pagina a scorrimento: testo a sinistra, disegno a destra che cambia a ogni paragrafo; traccia sotto | **`progetto.html`**, link dalla barra in alto e in fondo a `risultati.html` |
| **H. Stile** | `assets/stile.css` comune; font salvati in `assets/`; verde acqua → corallo; modo scuro; icona del sito; anteprima per i link condivisi (immagine 1200×630, titolo, descrizione) | **tutte le pagine**; il pannello della mappa lo segue |

### Aggiunte proposte nell'analisi del 22/10

| Elemento | Cos'è | Dove |
|---|---|---|
| **I. Barra e piè di pagina comuni** | in alto: Home · Risultati · Mappa · Il progetto · IT/EN. In basso: «Chi sono» (nome, LinkedIn, email, GitHub), licenza, **«dati aggiornati al …»** | home, risultati, progetto (la mappa ha il suo pannello: lì solo il link «Il progetto») |
| **J. Contatore della raccolta** | «Il Raspberry Pi legge Torino da N giorni: X milioni di posizioni dei mezzi» (numeri scritti dallo script delle schede) | **home**, sotto il titolo |
| **K. Miniature nei riquadri** | ~~immagine fissa del grafico~~ → dal 23/10 (Leo) l'animazione della scheda in piccolo; le immagini `assets/miniature/` si tolgono in L2 | home |
| **L. Caricamento della mappa** | mentre arrivano i 6 MB: il contorno di Torino che si disegna e una barra; la finestra delle schede si apre con una dissolvenza | mappa, risultati |
| **M. Mappa più comoda** | su telefono il pannello sale dal basso; schede dei temi uniformi (titolo = nome del posto, 3-5 righe, fonte in piccolo); «◎ Cintura» diventa «Tutta l'area»; ultime date e sigle tolte dal testo; bottone «copia il link di questa vista» | mappa |
| **N. Come funziona** | schema animato: sensori e GPS → Raspberry Pi → storico → script → pagine (i livelli dell'IoT della tesi) | `progetto.html` |
| **O. Pagina «non trovata»** | `404.html` nello stile del sito con i link alle pagine | radice |
| **P. Pagine dei singoli risultati** | `r/1.html` … `r/5.html`: pagine minime, scritte dallo script delle schede, con titolo, descrizione e immagine del risultato, che portano subito a `risultati.html#pN`. Un post su LinkedIn mostra la scheda giusta. Poco lavoro (Leo: sì, se resta poco) | radice, cartella `r/` |

### Traccia di `progetto.html`
1. **La promessa** (tesi del 2020): «sensori e dati cambieranno le città».
2. **Il sistema**: un Raspberry Pi che legge Torino ogni minuto (N, schema animato).
3. **Chi abita dove**: fragilità, poi servizi; le 5 zone in doppio svantaggio si accendono.
4. **Muoversi**: bus contro auto, in breve, con il link alle schede 3 e 4.
5. **Quanto ci si può fidare dei dati**: il feed dei ritardi che sbagliava di 2-3 volte, il bus con l'orologio 3 anni avanti.
6. **Cosa manca** (costi, passeggeri, treni) e **Chi sono**.

## Passi (in ordine)

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **FATTO (C4, Leo sceglie)**: 3 prove di stile su una pagina (`sviluppo/prove_stile.html`: «Notte», «Carta», «Torino»), con lo stesso riquadro, grafico e mappa piccola → Leo sceglie | CLOUD | piccolo |
| 2 | **FATTO (C5)**: H + I: `assets/stile.css`, font, icona, modo scuro, barra e piè di pagina, anteprima dei link; home e risultati nello stile nuovo; colori di mappa e schede ripensati insieme (verde acqua → corallo) | CLOUD | medio |
| 3 | **FATTO (C5)**: B + C + L (parte schede): numeri grandi che contano, omini e quadratini, dissolvenza della finestra | CLOUD | piccolo |
| 4 | **D** gara bus contro auto nella scheda 3 | CLOUD | medio |
| 5 | **FATTO (C6, Leo rilegge)**: testi IT/EN: dopo la divisione di `schede_risultati.py` (piano 5, passo 4), inglese completo delle schede; Leo rilegge | CLOUD | medio |
| 6 | **A + J + K** home: animazione dei mezzi (serve l'ora tipica: piano 2, passo 4, sul PC), contatore, miniature | CLOUD → PC → CLOUD | medio |
| 7 | **F + L + M** mappa: ore che scorrono, caricamento, pannello su telefono, schede dei temi, link della vista | CLOUD | medio |
| 8 | **FATTO nel cloud (C10), da calcolare sul PC (P6: `AREA_TEMPI.bat`)**: **E** area che si espande nella scheda 4: script 99, da Piazza Castello e da ogni zona di Torino | CLOUD (script) → PC (calcolo) → CLOUD | medio |
| 9 | **FATTO (C11, Leo rilegge i testi)**: **G + N** `progetto.html` | CLOUD | grande |
| 10 | **FATTO (C12)**: **O**, **P**; screenshot per il README (piano 1) | CLOUD | piccolo |

Prova di ogni passo: le pagine aperte in un browser senza schermo (0 errori, screenshot a misura di computer e telefono, anche
con «riduci movimento»); Leo guarda gli screenshot e poi le pagine vere sul PC.
Peso: home sotto 1 MB con l'animazione; mappa non oltre i 6 MB di oggi.

## Revisione di Leo (23/10) e come la applichiamo

Leo ha guardato home, schede e mappa dopo C7-C9. Gli piacciono il caricamento della mappa (la città che si disegna) e i mezzi in movimento in home.
Le sue modifiche, con le scelte di Claude dove Leo ha lasciato decidere (valori predefiniti, si cambiano con una riga):

**Home**
- «Torino Mobilità» in **oro**; sotto: «Un progetto per capire come si muove la città».
- Frase della raccolta, più generale: «Da **N** giorni raccogliamo, minuto per minuto, dove sono bus e tram e quanto traffico c'è sulle strade. E continuiamo.» + «Per capire chi va dove, e come ci va.»
  N = giorni dal primo giorno della raccolta (3/10/2026) a **oggi**, contati nella pagina: «e continuiamo» resta vero finché il Raspberry Pi raccoglie (la raccolta è sempre attiva).
- I 5 riquadri mostrano **la stessa animazione della loro scheda**, in piccolo, al posto delle miniature fisse (componente unico `assets/animazioni.js`, usato da home e schede).

**Numeri che salgono** (home e schede): più lenti (circa 2,5 secondi), partenza e arrivo morbidi; durante la corsa solo numeri interi, **senza virgola né %**:
la parte decimale e il % compaiono solo alla fine. Cifre a larghezza fissa e spazio riservato, così il testo intorno non si muove. Anche le forbici («21–28», «2–3») salgono.

**Schede**
- Via la parte «In English» (l'inglese resta col bottone IT/EN).
- Meno parti chiuse: domanda → numero grande con la sua animazione → grafico principale → 3 punti chiave → «Vedi sulla mappa» → **tutti gli altri grafici aperti**
  (anche quelli che prima stavano in una parte chiusa: attese, interscambi, strade grandi) → **una sola** parte chiusa «Come l'abbiamo calcolato e limiti» (calcolo, criteri, confronto, limiti).
- Titoli nuovi (Leo ha proposto, Claude ha ritoccato):

| Scheda | Titolo | Perché il ritocco |
|---|---|---|
| 1 servizi | «Torino, città dei 15 minuti: quasi tutti hanno i servizi a 15 minuti a piedi» | l'idea dei 15 minuti si chiama «città dei 15 minuti»; «smart city» è un'altra cosa (sensori e dati: è il racconto della pagina «Il progetto») |
| 2 puntualità | «Circa il 5% dei passaggi arriva con più di 10 minuti di ritardo» | «in ritardo» da solo è ambiguo: oltre 5 minuti sono il 14% |
| 3 parcheggi | «2 fermate importanti su 3 non hanno dove lasciare l'auto» | il risultato vero è quanto è facile lasciare l'auto e proseguire coi mezzi (Leo); i minuti di parcheggio diventano un punto chiave |
| 4 traffico | resta «Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto» finché non c'è il giorno intero (L3) | |
| 5 case | «Circa 1 torinese su 10 vive in una zona con più difficoltà sociali e pochi servizi» | «fragile» detto di persone suona male; «difficoltà sociali» descrive l'indice senza etichettare chi ci vive |

- **Animazioni** (tutte con «riduci movimento»: figura ferma e numeri scritti):
  1. **Servizi**: tre cerchi intorno a una casa, 5 → 10 → 15 minuti a piedi; ogni cerchio si apre col suo % (68 → 97 → 99).
  2. **Puntualità**: 100 quadratini che si accendono (ritardo oltre 5 minuti chiaro, oltre 10 scuro), poi **il giorno che scorre**: le 4 fasce orarie (punta del mattino, giorno, punta della sera, sera) cambiano i quadratini, con l'orologio. I dati per fascia ci sono già.
  3. **Parcheggi**: la forma di Torino, le 274 fermate importanti che compaiono e si colorano (posti bastanti / pochi / nessuno), poi i 12 punti prioritari che si accendono.
     La scheda cambia centro: numero grande = fermate senza posti bastanti (179 su 274), grafico principale = i 12 punti per bisogno; i minuti di parcheggio passano fra i punti chiave e gli altri grafici.
     La **gara bus contro auto** resta come secondo grafico e **gira da sola** da un punto all'altro (finita una corsa parte la successiva, col nome del punto); la tendina resta, piccola, per chi vuole scegliere.
  4. **Traffico**: l'area che si espande (C10, fatta) è l'animazione principale, anche in home; la gara sui viaggi tipici fra zone (le coppie con più auto del mattino), da sola, va negli altri grafici.
  5. **Case**: 10 omini che compaiono uno alla volta, poi uno si accende.

Come si fa: giro **L2** (agente in locale) in `PROMPT_LAVORI.md`, con la bozza di codice `C14_bozza.patch`. **Controlli grafici solo di Leo** (23/10).

**Non solo all'ora di punta** (schede 3 e 4, richiesta di Leo): oggi i tempi coi mezzi sono calcolati solo alle 8. Per l'auto abbiamo già il tempo a strada libera e le velocità
dei sensori 5T per ora; per i mezzi serve il calcolo a più ore (stesso motore degli script 93 e 94) → giro **L3** (agente in locale: script 100 e calcolo). Poi la gara
mostra le 4 ore una dopo l'altra (8, 13, 17:30, 21; scelte e regola del titolo nel blocco L3 di `PROMPT_LAVORI.md`) e la scheda 4 ha la linea «quante volte il tempo dell'auto, ora per ora». L'ora di punta resta il numero principale.

---

## Discussione di design (dopo il 24/10/2026, sessione cloud `claude/epic-clarke-6zdofk`)

Fatta su `origin/prova` dopo L9; L9b-L12 in corso sul PC (prompt sul ramo `claude/vigilant-volta-l13do5`). Bozza: `sviluppo/prove_design/toro_caricamento.html`
(file del toro: `sviluppo/prove_design/toro.svg`, quello di Leo). Niente di questa sezione è già applicato al sito.

### Decisioni di Leo

**Mappa, caricamento.** «Quando si carica la mappa si deve vedere la forma del toro anziché il profilo della città; fai caricare la mappa per almeno 1-2 secondi
così che si veda bene l'animazione.» Disegno: lo SVG di Leo (28 tracciati pieni, 54 KB).

**Risultati, in generale.**
- Via le scritte STIMATO / PROGRAMMATO / MISURATO dalla grafica: «sono dati che devono stare nel "come lo abbiamo calcolato", non aggiunti in grafica rumorosa».
- Meno rumore, descrizioni più semplici: «meno dati di quello che è stato lo sviluppo, più dati che parlino per sé stessi, esplicativi e concisi».
- Tutto scritto in modo **impersonale**, senza io/noi.
- Via «Condividi» ovunque (lo fa già L10).
- «Punta del mattino» → **mattino**, «punta della sera» → **sera**.
- **Tilde «~»** per i numeri meno importanti: **solo i numeri secondari** (il numero grande resta preciso).

**Schede.**
- 1: i 5/10/15 minuti della scheda aperta (68,3 → 96,8 → 99,2%) senza virgole, con ~.
- 2: «attesa media alla fermata prima/dopo» non si capisce: semplificare il concetto.
- 3: via «(stima)»; gara: «dal parcheggio» resta schiacciata; via ore, tendina del punto e «Riparti»: una gara animata per ogni parcheggio, poi la successiva; spiegazione più facile; la storia del parcheggio «troppi dati, troppe scritte, troppo da capire».
- 4: via stimato/misurato/programmato; spiegazione più semplice; animazione dell'area senza tendina della partenza, senza scelta della stima, senza «Parti»: va da sola, un po' più lenta, sempre da Piazza Castello, auto con TomTom; descrizioni uniformi fra loro; gara tagliata, stesse modifiche della scheda 3 (qui non ci sono ore, va bene); «le 12 coppie» → qualcosa come «i tragitti dove i mezzi pubblici ci mettono molto più dell'auto».
- 5: va abbastanza bene; via «Condividi».

**Home (temi 1 e 2).** Una home sola da scorrere, in tre parti:
1. una spiegazione con qualche numero chiave;
2. i risultati in breve: per ognuno solo anteprima animata, titolo e numeri molto importanti;
3. «Il progetto» in fondo, «più riconoscibile».

`risultati.html` e `progetto.html` **restano intatte per ora**: «poi vedremo la differenza e decideremo se cancellarle o ripristinarle».

**Fuori dallo scopo.**
- **Telefono:** «cosa si vede dal telefono non mi interessa, è un ordine». Nessun lavoro e nessuna prova a misura di telefono in questi giri; le regole che ci sono già nel CSS restano come sono.
- **Gerarchia dei riquadri:** «decideremo dopo quali e come metterli»; per ora tutti alla pari.
- **Altri temi** (scheda aperta in generale, anteprime LinkedIn, tipografia, animazioni oltre a quelle qui sopra): in disparte.

**Quando.** I giri L15-L18 sono per un agente in cloud, da far partire **dopo L12** (Leo ne discute il modo con Claude prima di lanciarli).

### Valori predefiniti di Claude (piccole scelte; si cambiano con una riga)

| Voce | Valore predefinito | Perché |
|---|---|---|
| Durata minima del caricamento | 2 secondi dall'apertura della pagina; con «riduci movimento» nessuna attesa e toro fermo e intero | «almeno 1-2 secondi» |
| Forma del toro | variante **B** della bozza (linee d'oro che si disegnano, poi l'oro riempie i tratti come nell'immagine); Leo può scegliere A o C | è la più fedele all'immagine |
| Testo del caricamento | «Caricamento della mappa…» (impersonale) | oggi «Carico la mappa…» |
| Fasce orarie | mattino (7-9) · giorno (9-16) · sera (16-19) · **tarda sera (19-24)** | «sera» per 16-19 si scontra con la fascia 19-24 che si chiama già «sera» |
| Tilde | numero grande preciso; nei punti chiave, didascalie e animazioni percentuali, minuti e rapporti interi con ~ (~68%, ~2 volte, ~1 min e mezzo); conteggi piccoli esatti senza ~ (12 punti, 68 fermate, 5 zone); conteggi grandi arrotondati (~222 mila); nelle etichette delle barre interi senza ~; nel «come è stato calcolato» tutto preciso | «solo i numeri secondari» |
| Etichette | la pastiglia STIMATO/MISURATO sparisce da scheda, riquadri e anteprime; nel «come è stato calcolato» una riga «Tipo di dato: …» spiegata a parole | decisione di Leo |
| Stima più favorevole all'auto (sensori 5T) | sparisce da grafici, punti chiave, gara e area delle schede 3 e 4: resta solo TomTom; i sensori restano nel «come è stato calcolato» come prova di sensibilità (una frase con i due numeri) | «via la stima» e «meno dati»; TomTom è la stima principale dal 24/10 |
| Titolo della parte chiusa | «Come è stato calcolato, e limiti» | impersonale |
| «Chi sono» | resta in prima persona (nome, contatti): è l'unica eccezione all'impersonale | è una firma, non un testo del risultato |
| Riga di limite di L10 sotto il numero grande | resta, al massimo ~12 parole, senza le parole stima/misurato | serietà visibile (analisi 3.11) senza rumore |
| Area della scheda 4 | ~1,5 volte più lenta di oggi; gira da sola (fino a 45 minuti, pausa ~3 s, ricomincia); via il cursore, al suo posto «N minuti» scritto grande | «va da sola, un po' più lenta» |
| Gara (schede 3 e 4) | una corsa per luogo, alle 8, poi la successiva dopo una pausa; il nome del luogo sopra la corsa; il distacco scritto all'arrivo (L10); nessun comando | «una gara animata e poi quella dopo» |
| Scheda 2, attesa | grafico «Quanto si aspetta in più di quanto dice l'orario»: una barra per fascia = minuti in più; a destra «~6 min invece di ~5»; punto: «Sulle linee frequenti si aspetta ~1 minuto e mezzo in più di quanto promette l'orario.» | oggi «4,53 → 5,85» con barra chiara/scura non si capisce |
| Home, numeri chiave | 3 numeri letti dalle schede (non scritti a mano): scheda 4 (1,9 volte), scheda 2 (~6% oltre 10 minuti), scheda 5 (~1 su 10), più il contatore della raccolta (L10) | i tre più forti dopo L9; la scelta definitiva va con la gerarchia |
| Home, «Il progetto» | le 6 tappe di `progetto.html` dentro la home, stesso codice (spostato in `assets/progetto.js`, usato da tutte e due le pagine), in una fascia scura come l'eroe con bordo oro e titolo «Il progetto» | «più riconoscibile»; codice in comune, così se `progetto.html` sparisce non si perde niente |
| Clic su un riquadro della home | apre `risultati.html#pN` come oggi | le pagine restano intatte |

### Aperto (si decide dopo)
- Gerarchia dei riquadri (6 dopo L14): quali in testa e come.
- `risultati.html` e `progetto.html`: cancellare o tenere, dopo aver visto la home nuova.
- Variante del toro (A, B, C): Leo guarda la bozza.
- Nome della fascia 19-24 («tarda sera» predefinito).
- I temi lasciati in disparte (anteprime LinkedIn, tipografia, scheda aperta in generale).

### Per L13 e L14 (già scritti, da fare dopo L15-L18 o prima: decide Leo)
Se L13/L14 partono **dopo** L15-L18, devono seguire le regole qui sopra (impersonale, niente etichette, solo TomTom in vista, tilde sui numeri secondari, fasce senza «punta»).
Basta aggiungere in testa al loro prompt: «Segui anche le regole della "Discussione di design" in sviluppo/piani/PIANO_GRAFICA.md.» Se partono **prima**, L15 le applica anche alla scheda 6 e alla parte nuova della scheda 4.

### Regole comuni ai giri L15-L18 (cloud)
- Partono dal ramo `prova` **dopo L12** (meglio: dopo l'ultimo ESITO arrivato su `origin/prova`), su un ramo di sessione `claude/...`; commit e push lì, Leo unisce in `prova`.
- Nel cloud non ci sono lo storico, `data/raw`, il Pi e Windows. `data/processed/` è in git; se `scripts/schede_risultati.py` non gira per un file mancante (dopo L12 IMQ e OMI non sono in git), **non inventare dati**: cambia il codice, prova con `scripts/prove/` dove serve, e scrivi a Leo di lanciare `scripts\RIFAI_MAPPA_E_SCHEDE.bat`.
- **Controlli grafici solo di Leo.** Prove solo di funzionamento: `python -m pyflakes scripts` zero, `node --check assets/*.js`, `python scripts/prova_pagine.py --playwright` 0 errori JavaScript, controlli nel DOM scritti nei prompt. Solo misura computer (1440×900): **niente telefono**.
- Numeri mai a mano: si leggono dai JSON. Testi inglesi in `scripts/schede/testi.json` e negli attributi `data-en`.
- Stile «Torino» (colori solo in `assets/stile.css`), numeri scritti accanto ai colori, animazioni ferme con «riduci movimento», niente «condividi»/«copia il link», peso della mappa non oltre quello di dopo L11.
- Esito `sviluppo/piani/ESITO_L1x.md` con prima/dopo di ogni testo cambiato e la lista per Leo di cosa guardare; memoria aggiornata.

## L15 — CLOUD: schede con meno rumore (testi, etichette, tilde, fasce)

Perché: decisioni di Leo qui sopra («Risultati, in generale» e schede 1-5). File: `scripts/schede/comune.py`, `r1.py`, `r4.py` (scheda 2), `r6.py` (scheda 3), `r8.py` (scheda 4),
`r10.py` (scheda 5), `testi.json`, `traduci.py` se serve, `pagine_r.py` (anteprime), `risultati.html` (pastiglia dell'etichetta in `#finMeta`, titolo della parte chiusa),
`assets/animazioni.js` (percentuali dei cerchi con ~), `scripts/prova_pagine.py` (prove nuove), `data/schede_risultati.js` e `r/` se si possono rifare nel cloud.

Regole fissate:
- Funzione unica `circa(x, ...)` in `comune.py` per la tilde (regole della tabella); i numeri grandi restano come oggi.
- Nella parte visibile della scheda (domanda, numero grande, riga di limite, punti chiave, titoli e note dei grafici, didascalie) non compaiono più: STIMATO, MISURATO, PROGRAMMATO, CENSIMENTO, «stima», «(stima)», «stima debole», «stima bassa», «sensori 5T», «più favorevole all'auto», «noi», «nostro», «abbiamo», «punta». Tutto questo, se serve, va nel «come è stato calcolato» (calcolo, criteri, limiti), detto in modo impersonale.
- Punti chiave: al massimo ~25 parole ciascuno, un numero principale per punto; note dei grafici: al massimo 2 frasi.
- Scheda 2: grafico dell'attesa come nella tabella; «Noi e GTT» → «GPS e dato ufficiale GTT».
- Scheda 3: titolo senza «(stima)»; 3 punti chiave semplici. (1) Fermate senza posti: «68 non hanno nessun parcheggio vicino, 111 troppo pochi». (2) Il primo dei 12 punti d'ingresso, con i posti che mancano con la ~. (3) In quanti dei 12 punti il bus dal parcheggio arriva in centro quasi come l'auto: solo TomTom, senza soglie in minuti. Via dagli «Altri grafici» la barra «minuti per parcheggiare oltre i quali…»: la sua idea va in una frase del calcolo. Restano: i 12 punti (principale), la gara, i parcheggi di scambio che ci sono già (solo TomTom).
- Scheda 4: domanda e testo del numero grande in una frase ciascuno (la quota 47% e le coppie escluse vanno nel calcolo). Grafico principale: solo TomTom. Linea ora per ora: una sola linea (TomTom). Punto sulla verifica con Google: nel calcolo. «Le 12 coppie con più auto dove…» → «I tragitti dove coi mezzi pubblici si impiega più del doppio dell'auto». Dispersione delle 600 coppie: resta, con una nota di una frase.
- Scheda 1: cerchi e punto 1 con ~ (~68%, ~97%, ~99% nei cerchi; 99,2% resta nel numero grande).
- Fasce: mattino, giorno, sera, tarda sera (tabella) in r4.py (tutte e quattro le mappe di nomi) e nei testi inglesi (morning, daytime, evening, late evening).

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e, in sviluppo/piani/PIANO_GRAFICA.md, la sezione «Discussione di design» (decisioni di Leo, valori predefiniti, regole comuni) e il blocco L15.
Prima: git fetch origin; parti da origin/prova (git checkout -B <ramo della sessione> origin/prova se il ramo è vuoto); leggi gli ESITO_L9b..L12 (e L13/L14 se ci sono) per sapere cosa è già cambiato; python scripts/controlla_rami.py.
Niente controlli grafici (li fa Leo), niente telefono, niente dati inventati. Un commit per scheda più uno per le parti comuni.
1. Parti comuni: circa() in scripts/schede/comune.py; pastiglia dell'etichetta tolta da risultati.html (#finMeta), dalle anteprime (pagine_r.py / prova_pagine.py) e dai riquadri se c'è; nel «come è stato calcolato» una riga «Tipo di dato» a parole; titolo della parte chiusa «Come è stato calcolato, e limiti» (IT/EN).
2. Schede 1, 2, 3, 4, 5 come nel blocco L15, una alla volta; traduzioni in testi.json.
3. Controllo automatico nuovo in scripts/prova_pagine.py (o uno script di prova a parte): apre ogni scheda di risultati.html in IT e in EN e, nel testo visibile fuori dalla parte chiusa, cerca le parole vietate del blocco L15 (anche in inglese: ESTIMATED, MEASURED, SCHEDULED, "we ", "our ", "peak", "sensor"); 0 trovate. Conta le parole dei punti chiave (massimo ~25).
4. Prove: python -m pyflakes scripts (zero); node --check assets/*.js; python scripts/schede_risultati.py se gira nel cloud (nessuna ATTENZIONE; se manca un file, scrivilo e lascia a Leo RIFAI_MAPPA_E_SCHEDE.bat); python scripts/prova_pagine.py --playwright (0 errori).
5. Esito sviluppo/piani/ESITO_L15.md: tabella prima/dopo di ogni testo visibile cambiato, scheda per scheda; cosa è passato nel «come è stato calcolato»; lista per Leo di cosa guardare. Memoria; commit; git push -u origin <ramo della sessione>.
```

## L16 — CLOUD: gara e area che vanno da sole

Perché: schede 3 e 4 (decisioni di Leo). File: `assets/gara.js`, `assets/area.js`, `assets/animazioni.js` (anteprima della home), `scripts/schede/r6.py` e `r8.py` (dati della gara: un'ora sola, solo TomTom), `risultati.html` se passa opzioni, `scripts/prova_pagine.py`.

Regole fissate:
- **Gara:** nessun comando (via `select`, «Riparti», le «ore»: solo le 8); un'auto sola (TomTom, parcheggio compreso); le corse dei luoghi una dopo l'altra, con il nome del luogo sopra; il distacco all'arrivo (L10) resta. Scheda 3: i 12 punti d'ingresso, poi i 5 interscambi. Scheda 4: i 6 viaggi più frequenti. Con «riduci movimento»: tutte le corse ferme all'arrivo, una sotto l'altra, coi minuti scritti.
- **Gara tagliata o schiacciata:** nessun testo deve uscire dal disegno e nessuna corsia deve sovrapporsi a un'altra. Lo si controlla con una prova automatica: per ogni corsa, ogni `<text>` ha il riquadro (getBBox) dentro il `viewBox` e le corsie non si toccano. Se un nome è troppo lungo, va a capo o si accorcia con «…» e il nome intero resta nel `title`.
- **Area (scheda 4 e anteprima in home):** via la tendina della partenza, via la scelta della stima (solo TomTom), via «Parti/Ferma» e il cursore; parte da sola quando compare, ~1,5 volte più lenta di oggi, fino a 45 minuti, pausa ~3 s, ricomincia; sempre da Piazza Castello; «N minuti» scritto grande al posto del cursore; i % coi mezzi e in auto restano scritti accanto alle aree. I dati delle altre zone restano nel file (non si toccano gli script dei dati), la pagina non li usa più.
- Testi delle animazioni impersonali e con la tilde (blocco L15).

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, la memoria e, in sviluppo/piani/PIANO_GRAFICA.md, la «Discussione di design» e il blocco L16. Parti dal ramo con L15 fatto (o da origin/prova se L15 è già unito); leggi ESITO_L15.
Niente controlli grafici, niente telefono. Un commit per la gara, uno per l'area.
1. assets/gara.js e i dati della gara in scripts/schede/r6.py e r8.py come nel blocco L16. Prova automatica in prova_pagine.py: apri le schede 3 e 4, aspetta 2 corse, controlla che (a) non ci siano select né button dentro .gara, (b) ogni <text> stia dentro il viewBox, (c) le corsie non si sovrappongano, (d) cambi il nome del luogo fra una corsa e l'altra. Con riduci movimento (emulazione di Playwright): tutte le corse scritte, nessuna animazione.
2. assets/area.js come nel blocco L16 (scheda 4 e anteprima in home). Prova: nessun select/button/input dentro .area; dopo ~3 s il numero dei minuti è cambiato da solo; con riduci movimento figura ferma a 30 minuti e % scritti.
3. pyflakes zero; node --check assets/*.js; schede_risultati.py se gira nel cloud; prova_pagine.py --playwright (0 errori). Esito sviluppo/piani/ESITO_L16.md (durate vecchie e nuove, cosa è stato tolto), lista per Leo; memoria; commit; push sul ramo della sessione.
```

## L17 — CLOUD: home da scorrere (spiegazione, risultati in breve, il progetto)

Perché: temi 1 e 2 (decisione di Leo). File: `index.html`, `assets/stile.css`, `assets/progetto.js` (nuovo: il codice delle tappe preso da `progetto.html`), `progetto.html` (usa `assets/progetto.js`: **stesso aspetto e stessi testi di prima**), `scripts/schede/home.py` e/o `comune.py` (campo dei numeri chiave e del testo breve), `testi.json`, `scripts/prova_pagine.py`.
`risultati.html` non si tocca (salvo quanto fatto in L15-L16).

Regole fissate:
- **Parte 1, sotto l'eroe:** «In breve». 2-3 frasi impersonali su cosa si misura e come (Raspberry Pi, GPS, sensori, dati aperti), poi i 3 numeri chiave (tabella dei valori predefiniti), letti da un campo nuovo `chiave` delle schede scelte (`{valore, testo}`, scritto dagli script delle schede, IT/EN), ognuno col link alla sua scheda; il contatore della raccolta (L10) resta nell'eroe. Le due frasi di oggi («Chi va dove…», «Ogni numero viene da dati veri…») e i due bottoni sono sostituiti da questa parte; il link alla mappa resta come bottone sotto i numeri.
- **Parte 2, «I risultati»:** riquadri con solo anteprima animata, titolo e numero grande con una parola breve (campo nuovo `numero.breve`, al massimo ~6 parole, es. «volte il tempo dell'auto»); via il testo lungo del numero. Tutti alla pari (gerarchia rimandata). Clic → `risultati.html#pN`.
- **Parte 3, «Il progetto»:** le 6 tappe di `progetto.html` con lo stesso codice (`assets/progetto.js`), in una fascia scura come l'eroe, bordo oro e titolo grande «Il progetto»; un'àncora `#progetto`; il «Chi sono» resta nel piè di pagina (non due volte).
- Barra in alto invariata (Home · Risultati · Mappa · Il progetto); in home il link «Il progetto» porta a `#progetto`.
- Animazioni della home: ogni anteprima parte solo quando il suo riquadro entra nella finestra (analisi 3, critica a L2); con «riduci movimento» tutto fermo.
- Peso della home (HTML + JS propri, senza i dati delle schede) scritto nell'esito: sotto 1 MB.

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, la memoria e, in sviluppo/piani/PIANO_GRAFICA.md, la «Discussione di design» e il blocco L17. Parti dal ramo con L16 fatto; leggi ESITO_L15 e ESITO_L16.
Niente controlli grafici, niente telefono. Un commit per parte (codice comune del progetto, parte 1, parte 2, parte 3).
1. Sposta il codice delle tappe da progetto.html in assets/progetto.js (stile in assets/stile.css) senza cambiare progetto.html a vista: prova automatica che i testi visibili di progetto.html in IT e in EN siano identici prima e dopo (salvo L15).
2. Campi nuovi chiave e numero.breve negli script delle schede (IT/EN in testi.json), poi index.html con le tre parti del blocco L17.
3. Prove in prova_pagine.py su index.html (1440×900, IT ed EN): (a) i 3 numeri chiave uguali a quelli di data/schede_risultati.js; (b) un riquadro per scheda, ognuno con anteprima, titolo, numero; (c) #progetto esiste e contiene le 6 tappe; (d) nessun «Condividi»/«copia il link»; (e) con riduci movimento nessuna animazione in corso; 0 errori JavaScript in index, risultati, progetto.
4. pyflakes zero; node --check assets/*.js; schede_risultati.py se gira nel cloud; prova_pagine.py --playwright. Esito sviluppo/piani/ESITO_L17.md (peso della home, cosa è stato tolto dalla home vecchia), lista per Leo: cosa guardare scorrendo la home dall'alto in fondo e in cosa differisce da risultati.html e progetto.html (per decidere se tenerle); memoria; commit; push sul ramo della sessione.
```

## L18 — CLOUD: il toro nel caricamento della mappa

Perché: decisione di Leo. File: `scripts/mappa_template.html` (blocco `#caricamento`, righe ~149-161 e ~184-188, e la chiusura del caricamento a ~2511), `sviluppo/prove_design/toro.svg` (solo lettura), `mappa_torino.html` (solo il blocco `#caricamento`, vedi regole), `scripts/prova_pagine.py`.

Regole fissate:
- Il contorno di Torino del caricamento è sostituito dal toro di Leo, nella variante scelta in `sviluppo/prove_design/toro_caricamento.html` (predefinita **B**), in oro `#e3bf55` sul fondo scuro di oggi. Barra e testo restano; testo «Caricamento della mappa…».
- Il caricamento resta almeno **2 secondi** dall'apertura della pagina anche se la mappa è pronta prima; poi la dissolvenza di oggi. Con «riduci movimento»: toro fermo e intero, nessuna attesa in più.
- Peso: il toro va dentro la pagina come SVG; coordinate arrotondate a interi, nessun dato in più. Peso di `mappa_torino.html` non oltre quello dopo L11 (scritto in ESITO_L11): se lo supera, semplifica i tracciati (meno punti) finché rientra e scrivilo.
- Nel cloud `04_genera_mappa.py` non gira (mancano i dati): cambia il template e applica **lo stesso blocco** anche a `mappa_torino.html` con una sostituzione solo di quel pezzo, poi controlla che il blocco nei due file sia identico. Leo rigenera la mappa sul PC al prossimo `RIFAI_MAPPA_E_SCHEDE.bat`: il risultato deve essere lo stesso.

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, la memoria e, in sviluppo/piani/PIANO_GRAFICA.md, la «Discussione di design» e il blocco L18 (variante del toro: quella scritta da Leo nella discussione, altrimenti B). Parti dal ramo con L17 fatto.
Niente controlli grafici, niente telefono. Un commit.
1. scripts/mappa_template.html: toro, durata minima, testo, riduci movimento come nel blocco L18 (il codice della variante è in sviluppo/prove_design/toro_caricamento.html). Stesso blocco in mappa_torino.html; controllo che i due blocchi siano identici.
2. Prova in prova_pagine.py: apri mappa_torino.html; il #caricamento contiene i tracciati del toro e non il contorno di Torino; resta visibile almeno 2 s (misura il tempo fra apertura e classe "fine"); con riduci movimento sparisce appena la mappa è pronta; 0 errori JavaScript; tutti i temi come prima.
3. Peso di mappa_torino.html prima e dopo nell'esito sviluppo/piani/ESITO_L18.md; lista per Leo (aprire la mappa, guardare il toro e la durata; poi RIFAI_MAPPA_E_SCHEDE.bat sul PC e riguardare); memoria; commit; push sul ramo della sessione.
```

### Tutti e quattro di seguito (un prompt solo, per la sessione cloud)

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, la memoria e, in sviluppo/piani/PIANO_GRAFICA.md, la «Discussione di design» e i blocchi L15, L16, L17, L18.
Fai i quattro giri in quest'ordine sullo stesso ramo della sessione, partendo da origin/prova dopo L12, ognuno col suo esito e i suoi commit; push dopo ogni giro. Se un giro si ferma (prova che non passa, file che manca), scrivilo nel suo esito e passa al successivo solo se non dipende da quello. Alla fine scrivi a Leo il nome del ramo e, per ogni giro, cosa guardare.
```
