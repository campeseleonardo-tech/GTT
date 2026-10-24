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

## Discussione di design (24/10/2026, sessione cloud `claude/epic-clarke-6zdofk`)

Base: `origin/prova` dopo L12 (2112dc6), cioè con L9b, L10, L11 e L12 fatti. Bozza del toro: `sviluppo/prove_design/toro_caricamento.html`; disegno di Leo: `sviluppo/prove_design/toro.svg`.
Il sito non è stato toccato. Provato nel cloud il 24/10:
- `python scripts/schede_risultati.py` gira e rifà le schede identiche (cambia solo «generato»; avviso atteso: `data/progetto.js` non si riscrive senza `omi_zone.json`);
- `pip install playwright` + `python scripts/prova_pagine.py --playwright` dà 0 errori su 20 pagine, ma riscrive `assets/anteprime/*.jpg` e `assets/readme/*.jpg`.

### Decisioni di Leo
**Mappa:** «quando si carica la mappa si deve vedere la forma del toro anziché il profilo della città», per **almeno 2 secondi**. Variante **B**: le linee d'oro si disegnano, poi l'oro riempie i tratti.

**Schede, in generale:**
- Via STIMATO / PROGRAMMATO / MISURATO dalla grafica: stanno nel «come è stato calcolato».
- «Meno dati di quello che è stato lo sviluppo, più dati che parlino per sé stessi, esplicativi e concisi.»
- Testi **impersonali**, senza io/noi.
- «Punta del mattino» → **mattino**, «punta della sera» → **sera**.
- **Tilde «~» solo sui numeri secondari.**
- Via la riga «Limite: …» messa da L10 sotto il numero grande: i limiti tornano solo nella parte chiusa.
- Schede 3 e 4: in vista **solo TomTom**; la stima dei sensori 5T va nel calcolo, con una frase.

**Schede, una per una:**
- **Scheda 1:** i 5/10/15 minuti della scheda aperta con ~ e senza virgole.
- **Scheda 2:** «attesa media prima/dopo» non si capisce: semplificare.
- **Scheda 3:** via «(stima)»; storia del parcheggio più semplice («troppi dati, troppe scritte»); gara non schiacciata, senza ore, senza scelta del punto, senza «Riparti»: una gara per parcheggio, poi la successiva.
- **Scheda 4:** spiegazione più semplice e testi uniformi. Area senza tendina della partenza, senza scelta della stima, senza «Parti»: va da sola, un po' più lenta, da Piazza Castello, auto TomTom. Gara non tagliata, come nella scheda 3. «Le 12 coppie» diventa «i tragitti dove coi mezzi pubblici si impiega più del doppio dell'auto».
- **Scheda 5:** va bene («Condividi» l'ha già tolto L10).

**Home:** una sola pagina da scorrere, in tre parti:
1. spiegazione con alcuni numeri chiave;
2. i risultati in breve: anteprima animata, titolo e numero grande;
3. «Il progetto» in fondo, ben riconoscibile.

`risultati.html` e `progetto.html` **restano intatte**: si decide dopo se toglierle.

**Fuori dallo scopo:**
- il **telefono** («è un ordine»): nessun lavoro e nessuna prova a misura di telefono;
- la gerarchia dei riquadri (si decide dopo): per ora tutti alla pari;
- anteprime LinkedIn, tipografia, altre animazioni.

**Organizzazione:** una sessione cloud sola, con i giri L15-L18 in fila (prompt qui sotto). Poi L13 e L14 sul PC, con le regole nuove.

### Valori predefiniti di Claude (si cambiano con una riga)
- **Fasce:** mattino (7-9), giorno (9-16), sera (16-19), **tarda sera (19-24)**. Il nome «sera» per la 19-24 si sarebbe scontrato con la 16-19. In inglese: morning, daytime, evening, late evening.
- **Tilde:** funzione unica `circa()` in `scripts/schede/comune.py`.
  - Il numero grande resta preciso.
  - Nei punti chiave, nelle didascalie e nelle animazioni: percentuali, minuti e rapporti interi con ~ (~68%, ~2 volte); il mezzo minuto scritto a parole («~1 minuto e mezzo»).
  - Conteggi piccoli esatti (12 punti, 68 fermate); conteggi grandi arrotondati (~222 mila).
  - Valori delle barre: interi senza ~. Nel calcolo: tutto preciso.
- **Parole vietate fuori dalla parte chiusa**, IT ed EN: STIMATO/MISURATO/PROGRAMMATO/CENSIMENTO, «stima», «sensori», «più favorevole all'auto», «punta», noi/nostro/abbiamo, «Limite:». Nella parte chiusa una riga «Tipo di dato: …» a parole. Titolo della parte chiusa: «Come è stato calcolato, e limiti». Il «Chi sono» del piè di pagina resta in prima persona.
- **Misure dei testi:** punti chiave al massimo ~25 parole e un numero principale ciascuno; note dei grafici al massimo 2 frasi.
- **Scheda 2, attesa.**
  - Grafico «Quanto si aspetta in più di quanto dice l'orario»: una barra per fascia = minuti in più, a destra «~6 min invece di ~5».
  - Punto chiave: «Sulle linee frequenti si aspetta ~1 minuto e mezzo in più di quanto promette l'orario.»
  - «Noi e GTT» diventa «GPS e dato ufficiale GTT».
- **Scheda 3.**
  - Punti chiave: (1) «68 fermate importanti non hanno nessun parcheggio vicino, 111 troppo pochi»; (2) il primo dei 12 punti d'ingresso con i posti che mancano (~); (3) in quanti dei 12 punti, lasciata l'auto, il bus arriva in centro quasi come l'auto (TomTom, senza soglie in minuti).
  - Tolto il grafico «minuti per parcheggiare oltre i quali…»: diventa una frase del calcolo.
  - Restano: i 12 punti (grafico principale), la gara, gli interscambi che ci sono già.
- **Scheda 4.**
  - Domanda e testo del numero grande in una frase ciascuno: la quota del 47% e le coppie escluse vanno nel calcolo.
  - Grafico principale e linea ora per ora con una sola stima (TomTom).
  - La verifica con Google va nel calcolo.
  - La dispersione delle 600 coppie resta, con una nota di una frase.
- **Gara (schede 3 e 4).**
  - Nessun comando; solo le 8; un'auto sola (TomTom, parcheggio compreso).
  - Le corse vanno una dopo l'altra, col nome del luogo sopra. Scheda 3: i 12 punti, poi i 5 interscambi. Scheda 4: i 6 viaggi più frequenti.
  - Il distacco di L10 resta.
  - Con «riduci movimento»: tutte le corse ferme all'arrivo, una sotto l'altra.
  - Nomi lunghi: a capo o «…», col nome intero nel `title`.
- **Area (scheda 4 e anteprima in home).**
  - Senza tendine, senza «Parti/Ferma», senza cursore; da sola, ~1,5 volte più lenta di oggi, fino a 45 minuti, pausa ~3 s e ricomincia.
  - «N minuti» scritto grande; i % coi mezzi e in auto scritti accanto alle aree.
  - Con «riduci movimento»: ferma a 30 minuti.
  - I dati delle altre zone restano nel file e la pagina non li usa più.
- **Home.**
  - **Parte 1, «In breve»:** 2-3 frasi impersonali e 3 numeri chiave letti dal campo nuovo `chiave` delle schede 4, 2 e 5 (1,9 volte; ~6% oltre 10 minuti; ~1 su 10), ognuno col link alla sua scheda, più un bottone per la mappa. Sostituisce la lista «intro» e i due bottoni di oggi.
  - **Parte 2:** i riquadri hanno il numero grande con un campo nuovo `numero.breve` (al massimo ~6 parole) al posto del testo lungo; clic → `risultati.html#pN`.
  - **Parte 3:** le 6 tappe di `progetto.html` con lo stesso codice, spostato in `assets/progetto.js`, in una fascia scura come l'eroe, bordo oro, titolo «Il progetto», àncora `#progetto`. In home il link «Il progetto» della barra porta a `#progetto`.
  - Le anteprime partono solo quando il riquadro entra nella finestra.
- **Caricamento della mappa.**
  - Testo «Caricamento della mappa…».
  - Con «riduci movimento»: toro fermo e intero, nessuna attesa in più.
  - Coordinate del toro arrotondate a interi.
  - Peso di `mappa_torino.html` non oltre 5.906.557 byte (dopo L11) più il toro: se lo supera, semplificare i tracciati.

### Aperto (dopo i giri)
- La gerarchia dei riquadri (6 dopo L14).
- Tenere o togliere `risultati.html` e `progetto.html`.
- Il nome della fascia 19-24.
- I temi lasciati in disparte.
- La domanda della scheda 5: in L9b la risposta di Leo è arrivata come segnaposto, quindi la domanda è rimasta com'era. Se Leo vuole «solo la seconda parte», si cambia in L15 punto 2.

### Per L13 e L14 (sul PC, dopo questi giri)
In testa al loro prompt in `PROMPT_LAVORI.md`, Leo o Claude aggiungono:
«Segui anche le regole della "Discussione di design" in sviluppo/piani/PIANO_GRAFICA.md: testi impersonali, niente etichette né riga "Limite", in vista solo TomTom, tilde sui numeri secondari con circa(), fasce senza "punta", gara e area senza comandi, campi `chiave` e `numero.breve` nella scheda 6.»

### L15-L18 — CLOUD, una sessione: schede con meno rumore, animazioni da sole, home da scorrere, toro della mappa

**FATTO (24/10, `ESITO_L15-18.md`)**: L15, L16, L17 e L18 fatti nella stessa sessione, con `prova_design` in `prova_pagine.py` (`--solo-design`). Il testo qui sotto resta come riferimento.

Come risparmiare token (vale per tutto il giro):
- **Da leggere:** `sviluppo/AGENTS.md`, la memoria e questa sezione. Gli ESITO solo se serve un fatto preciso. Niente ANALISI_CRITICA, PROMPT_LAVORI, ESITO_C*.
- **File grandi:** `mappa_torino.html` (6 MB) non si apre mai: si cerca con grep il blocco `id="caricamento"`. `scripts/mappa_template.html` (~2.500 righe): solo i pezzi trovati con grep (`caricamento`, `car-testo`, `"fine"`). I file degli script delle schede e degli asset si leggono interi una sola volta.
- **Prove:**
  - `pip install playwright` una volta; `prova_pagine.py --playwright` solo alla fine di ogni giro, non a ogni modifica.
  - Le prove nuove vanno in una funzione sola di `prova_pagine.py` (`prova_design`), che fa i controlli nel DOM elencati qui sotto.
  - Dopo ogni prova: `git checkout -- assets/readme/`. Le anteprime `assets/anteprime/*.jpg` si tengono solo se il giro le cambia apposta (L15, etichetta tolta).
- **Esito e memoria:** un esito solo, `sviluppo/piani/ESITO_L15-18.md`, con una sezione per giro; memoria aggiornata una volta alla fine.

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e, in sviluppo/piani/PIANO_GRAFICA.md, solo la sezione «Discussione di design» (decisioni di Leo, valori predefiniti, come risparmiare token). Non leggere altri piani né esiti salvo un fatto preciso che ti serve.
Prima: git fetch origin; parti da origin/prova (git checkout -B <ramo della sessione> origin/prova se il ramo non ha commit suoi); python scripts/controlla_rami.py; pip install playwright.
Regole: niente controlli grafici (li fa Leo), niente telefono, numeri mai a mano (dai JSON con python scripts/schede_risultati.py, che nel cloud gira), testi inglesi in scripts/schede/testi.json e data-en, colori solo in assets/stile.css, animazioni ferme con «riduci movimento». Un commit per giro (o per scheda in L15), push dopo ogni giro: git push -u origin <ramo della sessione>. Se un giro si ferma, scrivilo nell'esito e vai avanti solo se il giro dopo non ne dipende.

L15 — schede con meno rumore. File: scripts/schede/comune.py (circa()), r1.py, r4.py (scheda 2), r6.py (scheda 3), r8.py (scheda 4), r10.py (scheda 5), testi.json, pagine_r.py; risultati.html (via la pastiglia di etichetta() in #finMeta, via limiteVisibile, titolo della parte chiusa); assets/animazioni.js (cerchi con ~).
 1. Parti comuni (circa(), etichetta, riga «Limite», «Tipo di dato» nel calcolo, titolo della parte chiusa, fasce in tutte le mappe di nomi di r4.py).
 2. Schede 1-5 come nei valori predefiniti, una per commit; nel calcolo finisce tutto ciò che si toglie dalla vista (sensori, 47%, verifica Google, soglie dei minuti), detto in modo impersonale.
 3. prova_design (parte L15): ogni scheda in IT e EN, testo visibile fuori dalla parte chiusa senza le parole vietate (anche ESTIMATED, MEASURED, SCHEDULED, "we ", "our ", "peak", "sensor", "Limit:"); punti chiave ≤ 25 parole; numero grande uguale a prima.
 4. schede_risultati.py (nessuna ATTENZIONE), pyflakes zero, node --check assets/*.js, prova_pagine.py --playwright 0 errori. Esito: prima/dopo di ogni testo visibile cambiato.

L16 — gara e area da sole. File: assets/gara.js, assets/area.js, assets/animazioni.js, scripts/schede/r6.py e r8.py (dati della gara: solo le 8, solo TomTom).
 1. Gara e area come nei valori predefiniti.
 2. prova_design (parte L16): nessun select/button/input dentro .gara e .area; ogni <text> della gara col getBBox dentro il viewBox e corsie che non si toccano; il nome del luogo cambia fra due corse; il numero dei minuti dell'area cambia da solo entro 3 s; con riduci movimento (emulazione Playwright) tutto fermo e numeri scritti.
 3. Prove come L15. Esito: durate vecchie e nuove, cosa è stato tolto.

L17 — home da scorrere. File: index.html, assets/stile.css, assets/progetto.js (nuovo, codice delle tappe preso da progetto.html), progetto.html (usa assets/progetto.js, testi e aspetto invariati), scripts/schede/ (campi chiave e numero.breve, IT/EN). risultati.html non si tocca.
 1. assets/progetto.js; prova che i testi visibili di progetto.html in IT e EN siano identici prima e dopo.
 2. Campi chiave e numero.breve; index.html con le tre parti dei valori predefiniti.
 3. prova_design (parte L17): i 3 numeri chiave uguali a data/schede_risultati.js; un riquadro per scheda con anteprima, titolo, numero; #progetto con le 6 tappe; con riduci movimento nessuna animazione; 0 errori in index, risultati, progetto. Peso della home (HTML + JS propri) nell'esito: sotto 1 MB.

L18 — toro nel caricamento della mappa. File: scripts/mappa_template.html (blocco #caricamento: stile, svg, testo, chiusura con classe "fine"), mappa_torino.html (solo lo stesso blocco), sviluppo/prove_design/toro_caricamento.html (variante B, solo lettura).
 1. Toro variante B al posto del contorno di Torino, durata minima 2 s dall'apertura, riduci movimento, testo, coordinate intere.
 2. 04_genera_mappa.py non gira nel cloud (mancano i dati): stesso blocco sostituito anche in mappa_torino.html con un piccolo script Python (solo quel pezzo); controlla che i due blocchi siano identici. Peso prima/dopo nell'esito (limite nei valori predefiniti).
 3. prova_design (parte L18): #caricamento con i tracciati del toro e senza il contorno di Torino; visibile almeno 2 s; con riduci movimento sparisce appena la mappa è pronta; 0 errori; prova_link_mappa di L11 ancora tutta OK.

Fine: esito sviluppo/piani/ESITO_L15-18.md (una sezione per giro, prove, cosa resta aperto), memoria (una volta), push. Messaggio a Leo: il nome del ramo e, per ogni giro, cosa guardare (schede 1-5, home dall'alto in fondo confrontata con risultati.html e progetto.html, mappa al caricamento); sul PC dopo l'unione: RIFAI_MAPPA_E_SCHEDE.bat (la mappa rigenerata deve avere lo stesso caricamento).
```

### Dopo L15-L18 (24/10/2026, Leo: «va tutto bene, a parte il toro»)
Stato verificato il 24/10:
- `main` = `prova` = ff6fbca;
- la Release `dati-2026-11` **non è caricata**: su GitHub c'è solo `dati-2026-10`;
- GitHub Pages **non è acceso**: `campeseleonardo-tech.github.io/Turin-mobility/` risponde 404;
- descrizione del repository «GTT project».

**Toro (Leo):** «volevo si caricasse come si caricava prima il profilo della città, con una linea che si crea sul contorno del toro». Quindi è lo stesso effetto del vecchio contorno: la linea d'oro corre sul contorno, va e torna in 2,4 s finché la mappa è pronta, il riempimento resta appena accennato, **niente oro pieno**. La durata minima di 2 s resta.

Ordine dei passi:

| # | Chi | Cosa |
|---|---|---|
| 1 | Leo, a mano | caricare la Release `dati-2026-11`; accendere Pages; scrivere descrizione e argomenti del repository |
| 2 | CLOUD | **L19**: toro come il vecchio contorno, gara del pannello della mappa con una sola auto e senza «Riparti», immagini del README dalla home nuova |
| 3 | PC | **L13** e **L14** (blocchi in `PROMPT_LAVORI.md`) con le regole della «Discussione di design» |
| 4 | Leo + Claude | decisioni rimaste: gerarchia dei 6 riquadri; tenere o togliere `risultati.html` e `progetto.html`; poi un giro cloud breve (L21) |
| 5 | PC | **L20**: pulizie finali, prova da zero con la Release, `main`, controllo delle anteprime per LinkedIn |
| 6 | Leo | post su LinkedIn (home, poi un post per risultato con `r/N.html`) |

**Valori predefiniti di Claude per L19:**
- Animazione del toro = quella del vecchio contorno: `stroke-dasharray:1` con `pathLength="1"`, `animation:car-disegna 2.4s ease-in-out infinite alternate`, riempimento `rgba(143,176,234,.10)`, linea oro `#e3bf55`.
- La linea è sottile, perché i tratti del toro sono doppi (contorno di una forma piena).
- Con «riduci movimento»: toro a linee fermo e intero.
- Gara del pannello della mappa: solo l'auto TomTom e nessun comando, come nelle schede.

### Controllo del 25/10 e sessione in locale L20 (circa 2 ore)
**Controllo fatto nel cloud** su `origin/prova` 19afecd (L19 compreso):
- `schede_risultati.py` rifà le schede identiche (cambia solo «generato»).
- `prova_pagine.py --playwright`: 0 errori su 20 pagine; prove L15-L18 e link della mappa tutte OK; peso della mappa 5.958.369 byte; 461 file e 146,3 MB in git.
- Nessun ramo `claude/*` ha commit fuori da `prova`.
- `main` è indietro: manca L19.
- La Release `dati-2026-11` esiste ma è una **bozza** (draft): non è pubblicata, quindi `scarica_dati.py` prende ancora `dati-2026-10`.
- GitHub Pages è spento (404).

**Risposte di Leo (25/10):**
- L13 e poi L14; L14 si ferma solo sul pezzo dei dati che mancano e il lavoro va avanti.
- Pages adesso; alla fine l'agente unisce `prova` in `main` se tutte le prove passano; LinkedIn dopo L14.
- Extra: velocità vera dei bus (E4) nella scheda 2.
- Scheda 5: domanda con la sola seconda parte.

**Prima del lancio, Leo a mano:**
1. Pubblicare la bozza della Release: Releases → `dati-2026-11` (Draft) → Edit → «Publish release».
2. Accendere Pages: Settings → Pages → Branch `main`, cartella `/` → Save.

**Regole di E4, fissate ora** (valori predefiniti di Claude):
- Velocità commerciale dei bus e dei tram dal GPS = distanza fra fermate / tempo fra i passaggi. È lo stesso calcolo del livello «Velocità» di `04_genera_mappa.py`, da riusare e non riscrivere.
- Feriali del `comuni.PERIODO`, media pesata sui passaggi, ora per ora dalle 5 alle 24, bus e tram separati e insieme.
- Script `104_velocita_bus.py`: scrive `data/processed/velocita_bus.json` e `docs/rapporti/RAPPORTO_VELOCITA_BUS.txt`.
- Controlli: velocità fra 5 e 40 km/h; AVVISO per le ore con meno di 1.000 passaggi.
- Scheda 2:
  - un punto chiave «Alle 8 un bus va in media a ~N km/h» (sostituisce il meno forte dei 3: scriverlo nell'esito);
  - un grafico a linea ora per ora negli «Altri grafici»;
  - nel calcolo come si misura, e che le fermate e i semafori sono compresi.
- Nessun numero scritto a mano.

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, la memoria e, in sviluppo/piani/PIANO_GRAFICA.md, la «Discussione di design» (valori predefiniti: valgono per ogni testo e scheda nuova) e «Controllo del 25/10 e sessione in locale L20». Non leggere altri piani né esiti salvo i blocchi citati qui.
Prima: git pull --no-rebase origin prova; python scripts\controlla_rami.py (se un ramo ha commit non in prova, fermati e dillo a Leo).
Lavoro di circa 2 ore, in quest'ordine di priorità. Un commit per passo e git push origin prova dopo ognuno, così niente si perde se il tempo finisce. Niente controlli grafici (li fa Leo), niente telefono, niente scritture sul Pi.
1. L13: esegui il blocco L13 di sviluppo/piani/PROMPT_LAVORI.md, con le regole di design (testi impersonali, niente etichette né riga «Limite», in vista solo TomTom, circa() sui numeri secondari, punti chiave ≤ 25 parole).
2. L14: esegui il blocco L14 di PROMPT_LAVORI.md, con le stesse regole e in più: campi chiave e numero.breve della scheda 6, gara e contatori senza comandi, home a 6 riquadri (3 + 3), r/6.html. Lo STOP vale solo per i dati: se mancano carburante, tariffe GTT o sosta, scrivi in ESITO_L14.md cosa manca e dove hai cercato, non fare la scheda e passa al punto 3.
3. Scheda 5: la domanda diventa solo la seconda parte («Chi vive dove i servizi sono pochi e le difficoltà sociali sono alte?», inglese in testi.json).
4. E4, velocità vera dei bus nella scheda 2: regole in «Controllo del 25/10 e sessione in locale L20».
5. Rilancio e prove: scripts\RIFAI_MAPPA_E_SCHEDE.bat; python -m pyflakes scripts (zero); node --check assets\*.js; python scripts\schede_risultati.py (nessuna ATTENZIONE); python scripts\prova_pagine.py --playwright (0 errori, prova_design compresa).
6. Prova da zero con la Release dati-2026-11 (se è ancora una bozza, scrivilo e salta): clone in una cartella temporanea, python scripts\scarica_dati.py, python scripts\rifai_tutto.py --solo schede; data\schede_risultati.js uguale a quello di prova (salvo «generato»). Poi cancella la cartella temporanea.
7. Pulizie: file «3)» nella radice e scripts\*.bak_18ott se ci sono; git status pulito (niente data\ fuori dalle regole, .bak, chiavi).
8. Esito unico sviluppo/piani/ESITO_L20.md (una sezione per punto, numeri nuovi, cosa è saltato e perché), memoria, commit, git pull --no-rebase origin prova, git push origin prova.
9. Solo se il punto 5 è tutto verde: git checkout main; git pull origin main; git merge --no-edit prova; git push origin main; git checkout prova. Se qualcosa non è verde, non unire e scrivilo.
Se il tempo finisce prima, fermati dopo l'ultimo punto chiuso, fai il punto 8 e scrivi a Leo da dove ripartire.
ALLA FINE a Leo: per ogni punto fatto/saltato; numero grande e titolo della scheda 6; il valore di E4; cosa guardare (scheda 4 con la parte nuova, scheda 6, scheda 2, home a 6 riquadri); se main è stato aggiornato.
```
