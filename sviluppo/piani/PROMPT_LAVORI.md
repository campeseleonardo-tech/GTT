# Prompt per far fare i lavori pianificati a un modello

Un prompt = un giro di lavoro. **Un giro per volta, nell'ordine della tabella** (mai due insieme: toccano gli stessi file).
- **CLOUD** = sessione cloud di Claude Code sul repository `campeseleonardo-tech/Turin-mobility` (niente `data/`, niente Pi, niente Windows).
- **PC** = Claude Code (o un altro modello con terminale) sul PC di Leo, cartella `C:\projects\Progetti\GTT`, ramo `prova`.
- 🛑 = Leo deve decidere o guardare qualcosa prima del giro dopo.

Dopo ogni giro CLOUD, Leo unisce il ramo della sessione in `prova` sul PC:
```
git checkout prova
git pull --no-rebase origin prova
git fetch origin
git merge --no-edit origin/<ramo della sessione, es. claude/nome-abc123>
git push origin prova
```
poi doppio clic su `scripts\CONTROLLA_RAMI.bat` e, se il giro lo chiede, il giro PC che segue. Il ramo della sessione si cancella
da GitHub dopo l'unione. Un giro finito e provato entra in `main` solo nei punti segnati «→ main».

## Ordine

| Giro | Dove | Cosa | Piani |
|---|---|---|---|
| P0 | PC | R6 rifatto con più giorni di parcheggi; scheda 5 controllata | 3 (1, 2) |
| C1 (FATTO 22/10) | CLOUD | riorganizzazione: `sviluppo/`, dati di accesso fuori dai testi, testi puliti, script 86, prova delle pagine su ogni sistema, difetto `#p3` | 1 (4-7), 5 (1, 9) |
| P1 (FATTO 23/10) | PC | `config_locale.json`, rilancio mappa e schede, prova delle pagine | 1 (5) |
| C2 (FATTO 22/10) | CLOUD | inventario dei dati (script 96) e licenze delle fonti | 2 (1, 2) |
| P2 (FATTO 22/10) | PC | lancio dello script 96 🛑 Leo e Claude decidono dove va ogni dato | 2 (1, 3) |
| C3 (FATTO 22/10) | CLOUD | riassunti dello storico + ora tipica (97), `.gitignore`, Release (98), `scarica_dati.py` | 2 (4-7) |
| P3 (FATTO 22/10, Release dati-2026-10) | PC | lancio 97 e 98, caricamento della Release, commit dei dati | 2 (4-6) |
| C4 (FATTO 22/10, aspetta la scelta di Leo) | CLOUD | 3 prove di stile 🛑 Leo sceglie | 4 (1) |
| C5 (FATTO 22/10) | CLOUD | stile comune, barra, piè di pagina, anteprima dei link; numeri che contano, omini e quadratini; grafico della metro (scheda 5) | 4 (2, 3), 3 (3) |
| C6 (FATTO 22/10) | CLOUD | divisione di `schede_risultati.py` e testi IT/EN | 5 (4), 4 (5) |
| P4 (FATTO 22/10) | PC | rilancio schede: stessi numeri di prima; Leo rilegge l'inglese 🛑 | 5 (4) |
| C7 (FATTO 22/10) | CLOUD | gara bus contro auto (scheda 3) | 4 (4) |
| C8 (FATTO 22/10) | CLOUD | home: mezzi in movimento, contatore, miniature | 4 (6) |
| C9 (FATTO 22/10) | CLOUD | mappa: ore che scorrono, caricamento, telefono, schede dei temi, link della vista | 4 (7) |
| P5 (FATTO 23/10, Leo guarda a occhio) | PC | prima `97 --solo ora --rifai` (ESITO_C8), poi rilancio mappa e schede, controllo a occhio di home, schede e mappa 🛑 → main | — |
| C10 (FATTO 23/10) | CLOUD | area che si espande: script dei tempi e grafico (scheda 4) | 4 (8) |
| P6 (FATTO 23/10) | PC | `AREA_TEMPI.bat` (ESITO_C10): calcolo dei tempi da Piazza Castello, rilancio schede | 4 (8) |
| C11 (FATTO 23/10, Leo rilegge i testi) | CLOUD | `progetto.html` | 4 (9) |
| C12 (FATTO 23/10) | CLOUD | 404, pagine dei singoli risultati, README, controllo automatico su GitHub, `rifai_tutto.py` | 4 (10), 1 (9), 5 (2, 3) |
| P7 (FATTO 23/10, tranne le 19 ore di accessibilità; ESITO_P7) | PC | prova «da zero» e rilancio completo 🛑 → main; Leo accende GitHub Pages e scrive la descrizione del repository | 1 (8, 10), 5 (3) |
| C13 (FATTO 23/10: tutti i gruppi, pyflakes a zero) | CLOUD | pulizia del codice (funzioni comuni, codice morto, prove dei numeri), a pezzi | 5 (5-8) |
| L1 (FATTO 23/10, esito ESITO_P7 e ESITO_C13_*) | PC | P1, P3, P5, P6, P7 e C13 sui dati veri | — |
| **L2 (FATTO 23/10, Leo guarda)** | PC | revisione grafica di Leo del 23/10 (ex C14): home, numeri che salgono, schede con una sola parte chiusa, titoli nuovi, animazioni anche in home; prima Leo sceglie se rifare R4, R6, R8 con lo storico di oggi 🛑 | 4 (revisione 23/10) |
| **L3 (FATTO 23/10, Leo guarda)** | PC | bus contro auto a 4 ore del giorno (ex C15 + P10), script 100, schede 3 e 4 🛑 | 4 (revisione 23/10) |
| **L4 (FATTO 23/10)** | PC | raccolta del Pi: copia che non perde dati, archivio del GTFS, controllo con spazio e scadenze (PIANO_RACCOLTA passi 1, 2a, 3) 🛑 | raccolta FATTO |
| **L4b** (urgente: entro fine ottobre) | PC | snapshot della copia sul disco del Pi invece di /tmp (PIANO_RACCOLTA passo 4) | raccolta |
| **L5** | PC | scheda 1 (testo che esce), gara della scheda 4 sempre alle 8, testi onesti su «forbice» e «fasce fissate prima» (ANALISI_CRITICA 1.2, 1.3) | 3, 4 |
| **L6** | PC | tempi in auto col traffico da un servizio di percorsi (TomTom), in entrata e in uscita, a 4 ore; fattore al posto del 2,1 di Google (ANALISI_CRITICA 1.1, 1.14) 🛑 Leo: chiave e condizioni d'uso | 3 |
| L7 (da scrivere dopo L6) | PC | calcoli rifacibili da un estraneo (ANALISI_CRITICA 6.1) e PIANO_RACCOLTA passo 2b | 5 |
| main | Leo | unire prova in main, accendere GitHub Pages (la pubblicazione per ultima) | 1 (8, 10) |
| P8 | PC | metà novembre: R4 con un mese di dati, rilancio | 3 (4) |

---

## Regole comuni (sono già dentro ogni prompt: non serve copiarle)

Ogni prompt dice al modello di: leggere `sviluppo/AGENTS.md` e la memoria; controllare i rami prima di iniziare; seguire il piano; provare davvero
(script lanciati, pagine aperte nel browser); scrivere un esito `ESITO_<giro>.md` accanto ai piani; aggiornare la memoria; fare commit e push.
I numeri dei risultati non si scrivono mai a mano: si leggono dai file prodotti dagli script.
**Controlli grafici (Leo, 23/10): li fa solo Leo.** Il modello controlla che il codice giri (script, 0 errori JavaScript con `prova_pagine.py`,
numeri nei JSON) e scrive a Leo una lista di cosa guardare; non guarda e non giudica schermate, colori o misure (vale anche per i prompt scritti prima).

---

## P0 — PC: R6 con più giorni e controllo della scheda 5

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT. Leggi sviluppo/AGENTS.md e sviluppo/MEMORIA_PROGETTO.md  e segui le loro regole.
Prima di tutto: verifica di essere sul ramo prova, fai git pull --no-rebase origin prova, lancia python scripts\controlla_rami.py e, se segnala rami con lavoro non unito, fermati e dillo a Leo.

Lavoro (piano 3, punti 1 e 2, in sviluppo/piani/PIANO_RISULTATI.md):
1. Lancia scripts\RISULTATO6_RIFAI.bat (circa 4 minuti) e poi scripts\RIFAI_MAPPA_E_SCHEDE.bat. Leggi il log in logs\: nessun errore.
2. In docs\rapporti\RAPPORTO_R6V2_RIEMPIMENTO.txt controlla quanti giorni feriali validi usa ora il riempimento (prima erano 3, segnati [DATI SCARSI]); se sono almeno 5, verifica che l'etichetta [DATI SCARSI] sul riempimento sia sparita o spiega perché resta.
3. Confronta i numeri principali del R6 prima e dopo (punti prioritari, fermate senza posti bastanti, minuti di pareggio): scrivi una tabella prima/dopo. Differenze grandi (oltre il 20%) = AVVISO da spiegare.
4. Apri data\schede_risultati.js e controlla che contenga la scheda del risultato 10 (in pagina «Risultato 5», «Case, servizi e fragilità») con numeri veri (non 12% «di prova»): titolo, numero grande, 5 zone in doppio svantaggio. Scrivi i valori.
5. Lancia python scripts\prova_pagine.py: 0 errori.
6. Scrivi sviluppo\piani\ESITO_P0.md (tabella prima/dopo, valori della scheda 5, esito delle prove). Aggiorna sviluppo/MEMORIA_PROGETTO.md (sezioni 4 e 5) solo con quello che è cambiato.
7. git status (niente data\, .bak, chiavi), git add -A, git commit -m "R6 rifatto con N feriali di parcheggi; scheda 5 controllata", git pull --no-rebase origin prova, git push origin prova.
Alla fine di' a Leo in 5 righe cosa è cambiato e cosa deve guardare in risultati.html (schede 3 e 5).
```

## C1 — CLOUD: riorganizzazione e prova delle pagine

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e i piani sviluppo/piani/PIANO_RIORGANIZZAZIONE.md e PIANO_CODICE.md. Segui le regole di AGENTS.md per il cloud (resta sul ramo della sessione, niente data/).
Prima di tutto: git fetch --unshallow origin (se la copia è tagliata) e python scripts/controlla_rami.py; se ci sono rami con lavoro non presente in origin/prova, fermati e dillo a Leo.

Lavoro, un commit per punto:
1. Piano 1 passo 4: crea sviluppo/ e spostaci con git mv MEMORIA_PROGETTO.md, docs/piani/ (diventa sviluppo/piani/, compreso questo file PROMPT_LAVORI.md) e docs/TESI_E_PROGETTO.md. Sposta il contenuto di AGENTS.md in sviluppo/AGENTS.md e lascia in radice un AGENTS.md di 5-8 righe che dice: leggi sviluppo/AGENTS.md e sviluppo/MEMORIA_PROGETTO.md prima di tutto. Cerca con git grep ogni percorso vecchio (sviluppo/MEMORIA_PROGETTO.md, sviluppo/piani, TESI_E_PROGETTO) in script, .bat, documenti e pagine e aggiornalo.
2. Piano 1 passo 5: l'IP del Raspberry Pi, l'utente SSH e il percorso della chiave non devono più comparire nei file in git. Scrivi scripts/config_locale.esempio.json (valori finti) e fai leggere a script e .bat un config_locale.json nella radice (aggiungilo a .gitignore); se manca, lo script si ferma con un messaggio chiaro che dice come crearlo. Togli IP e utente anche dai documenti (scrivi «il Raspberry Pi di casa»). Elenca in ESITO quali file leggono il config.
3. Piano 1 passo 6: nelle pagine (index.html, risultati.html, scripts/mappa_template.html, testi delle schede in scripts/schede_risultati.py) togli «Leo», «giro», «fase», «versione», date di sviluppo, sigle non spiegate (Q001-Q009 → «il centro», IMQ → «indagine sugli spostamenti 2022»). Nei commenti del codice togli date e «Leo» solo dove sono rumore. Nella mappa: il bottone «◎» ha come titolo «Tutta l'area». Non cambiare nessun numero né nessun calcolo.
4. Piano 1 passo 7: lo script 86 non deve più scrivere README.md né creare pubblica/: diventa un controllo che elenca ogni file caricato da index.html, risultati.html e mappa_torino.html (script src, fetch, data/catalogo) e dice se esiste e se è in git (AVVISO se manca). Aggiorna RIFAI_MAPPA_E_SCHEDE.bat e la memoria.
5. Piano 5 passo 1: rinomina scripts/prova_pagine_r6.py in scripts/prova_pagine.py (aggiorna .bat e documenti). Deve trovare il browser su Windows (Edge/Chrome come oggi) e, se non c'è, usare Playwright (pip install playwright; nel cloud Chromium è in /opt/pw-browsers/chromium-1194/chrome-linux/chrome). Stesse prove di oggi (tutti i temi, errori JavaScript, legenda), più gli screenshot a 1440x900 e 390x844. Provalo nel cloud: senza data/ gli unici errori ammessi sono i file data/ mancanti, che devono comparire come «file assente», non come errore del codice.
6. Piano 5 passo 9: in risultati.html, se cambia l'indirizzo (#p3, #r6) senza ricaricare la pagina, la scheda giusta si apre (evento hashchange). Provalo nel browser.
7. Prova finale nel cloud: python -m py_compile su tutti gli script; prova_pagine.py; per vedere le schede senza data/ usa scripts/prove/dati_da_mappa_95.py e scripts/prove/prova_scheda_case.py (istruzioni in testa ai file). Screenshot prima/dopo di index, risultati e mappa: niente deve essere cambiato a parte i testi.
8. Scrivi sviluppo/piani/ESITO_C1.md (cosa hai fatto, file toccati, prove, cosa deve fare Leo sul PC). Segna come FATTI i passi nei piani. Aggiorna la memoria. Commit e push sul ramo della sessione.
Alla fine scrivi a Leo: i comandi per unire il ramo in prova e il giro P1.
```

## P1 — PC: file locale e rilancio

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT. Leggi sviluppo/AGENTS.md e sviluppo/MEMORIA_PROGETTO.md.
Prima: ramo prova, git pull --no-rebase origin prova, python scripts\controlla_rami.py (fermati se segnala rami non uniti).
1. Leggi sviluppo/piani/ESITO_C1.md. Crea config_locale.json nella radice copiando scripts\config_locale.esempio.json e mettendo i valori veri (indirizzo, utente e chiave del Raspberry Pi di casa: li conosce Leo). Controlla con git status che NON entri in git.
2. Lancia scripts\CONTROLLA_LEOPI.bat: deve funzionare come prima (legge il config).
3. Lancia scripts\RIFAI_MAPPA_E_SCHEDE.bat: nessun errore; lo script 86 non deve aver toccato README.md (git diff README.md vuoto).
4. Lancia python scripts\prova_pagine.py: 0 errori.
5. Scrivi l'esito in fondo a sviluppo/piani/ESITO_C1.md (sezione «Prova sul PC»), commit e push su prova (regole di AGENTS.md).
Di' a Leo quali file aprire e cosa deve vedere: index.html e risultati.html identici a prima nei numeri, testi senza date e sigle.
```

## C2 — CLOUD: inventario dei dati e licenze

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_DATI.md.
Prima: git fetch --unshallow origin (se serve) e python scripts/controlla_rami.py; fermati se ci sono rami con lavoro non unito.
1. Scrivi scripts/96_inventario_dati.py (sola lettura): elenca ogni file sotto data/ con peso; per ogni file cerca il nome (e il nome della cartella) nel codice di scripts/, nelle pagine e nei .bat e dice quali script lo leggono e quali lo scrivono; propone un posto: «git» (sotto 5 MB e letto da pagine o scritto da uno script dei risultati), «Release» (dati grezzi grandi in data/raw o letti dagli script dei dati), «riassunto» (lo storico). Scrive docs/DATI.md (tabella per cartella e per file, totali per posto) e stampa i totali. Opzione --prova che crea una cartella data/ finta per provarlo nel cloud. Prossimo numero libero: controllalo nella memoria.
2. Piano 2 passo 2: cerca sul web la licenza di ogni fonte (GTT GTFS e GTFS-RT, 5T, ISTAT censimento e basi territoriali, IMQ 2022 dell'Agenzia della Mobilità Piemontese, OMI dell'Agenzia delle Entrate, aperTO del Comune di Torino, OpenStreetMap). Per ognuna: nome della licenza, link alla pagina ufficiale, se permette di ripubblicare i file (sì / no / con condizioni), cosa scrivere come citazione. Se una pagina ufficiale non lo dice chiaramente scrivi «NON CHIARO» e non indovinare. Scrivi tutto in docs/FONTI_DATI.md (tabella nuova in testa) e togli le note di lavoro vecchie che non servono più.
3. Esito in sviluppo/piani/ESITO_C2.md; memoria; commit e push sul ramo della sessione. Scrivi a Leo i comandi per unire e il giro P2.
```

## P2 — PC: inventario sui dati veri

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md. Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py.
1. Lancia python scripts\96_inventario_dati.py. Controlla che i totali abbiano senso (lo storico è circa 2 GB e passa; data/raw è grande; i file delle pagine sono pochi MB).
2. Fai commit e push di docs/DATI.md (regole di AGENTS.md).
3. Riassumi a Leo, in una tabella corta: quanto andrebbe in git, quanto nella Release, quanto resta fuori, e per quali fonti docs/FONTI_DATI.md dice che la ripubblicazione è «no» o «NON CHIARO». Chiedi a Leo di decidere fonte per fonte (piano 2, passo 3) e scrivi le sue decisioni in docs/DATI.md (colonna «deciso»), commit e push.
```

## C3 — CLOUD: riassunti dello storico, Release, scaricamento

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, sviluppo/piani/PIANO_DATI.md e docs/DATI.md (con le decisioni di Leo). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. Piano 2 passo 4: scripts/97_riassunti_storico.py (sola lettura sullo storico SQLite data/storico_backup.sqlite; leggi gli script 27, 70, 26, 71 per capire quali tabelle e colonne usano). Scrive in data/storico_riassunti/ un file compresso per mese: (a) passaggi per corsa e fermata dal GPS, quello che serve allo script 27 e al 70; (b) medie dei sensori 5T per sensore, tipo di giorno e ora (script 26); (c) riempimento dei parcheggi per parcheggio e ora (script 71). Poi modifica 27, 70, 26 e 71 perché, se lo storico non c'è, leggano i riassunti e diano gli stessi numeri. Scrive anche data/storico_riassunti/ora_tipica.json: le posizioni di tutti i mezzi di un feriale tipico fra le 7:30 e le 8:30 (una posizione ogni 30 secondi per mezzo, coordinate arrotondate a 5 decimali, al massimo 300 KB). Opzione --prova con un piccolo storico finto per provarlo nel cloud; controlli: righe lette e scritte, nessun valore negativo, date dentro la raccolta.
2. Piano 2 passo 5: .gitignore nuovo secondo docs/DATI.md (data/raw/ e lo storico restano fuori). Aggiungi a prova_pagine.py (o script a parte) un controllo: nessun file in git sopra 50 MB, totale sotto 300 MB.
3. Piano 2 passo 6: scripts/98_prepara_release.py: crea in una cartella fuori da git gli zip decisi in docs/DATI.md, con dentro ELENCO.txt e un file SHA256SUMS; stampa nomi e pesi (ogni zip sotto 1,9 GB).
4. Piano 2 passo 7: scripts/scarica_dati.py: scarica gli zip dall'ultima Release di GitHub (indirizzo https://github.com/campeseleonardo-tech/Turin-mobility/releases/latest/download/<nome>) e le fonti pubbliche di docs/FONTI_DATI.md, controlla gli SHA256, mette i file nelle cartelle giuste, non sovrascrive file uguali.
5. Prova tutto nel cloud con i dati finti. Esito in sviluppo/piani/ESITO_C3.md con i comandi esatti per il PC; memoria; commit e push sul ramo della sessione. Scrivi a Leo i comandi per unire e il giro P3.
```

## P3 — PC: riassunti, Release, dati in git

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/ESITO_C3.md. Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py.
1. Lancia python scripts\97_riassunti_storico.py (prima su un mese con --mese se lo script lo prevede). Controlla i pesi.
2. Prova che i riassunti bastano: rinomina temporaneamente data\storico_backup.sqlite (NON cancellarlo), lancia 27, 70, 26 e 71 e confronta i rapporti con quelli di prima (docs\rapporti): stessi numeri, salvo la data. Rimetti il nome giusto allo storico. Se i numeri cambiano, fermati e dillo a Leo.
3. Lancia python scripts\98_prepara_release.py e di' a Leo i nomi e i pesi degli zip. Leo li carica a mano: GitHub → Releases → Draft a new release → tag dati-AAAA-MM → trascina gli zip → Publish.
4. git status: entrano solo le cartelle decise in docs\DATI.md; nessun file sopra 50 MB. Commit «Dati necessari ai calcoli in git (riassunti dello storico, file delle pagine)» e push su prova.
5. Prova lo scaricamento: in una cartella temporanea fuori dal progetto, git clone del repository e python scripts\scarica_dati.py: deve scaricare e controllare tutto. Scrivi l'esito in fondo a ESITO_C3.md, commit e push.
```

## C4 — CLOUD: prove di stile 🛑

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_GRAFICA.md. Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
Piano 4 passo 1. Crea sviluppo/prove_stile.html: una pagina con tre colonne (su telefono una sotto l'altra), una per stile: «Notte» (blu notte, verde acqua acceso, corallo), «Carta» (crema, nero, un colore forte), «Torino» (blu e oro, granata per gli allarmi). In ogni colonna, uguali per tutti: il titolo del sito «Torino Mobilità», un riquadro di risultato vero (prendi titolo e numero dalla scheda 5 in data/schede_risultati.js; nel cloud ricavala con scripts/prove/dati_da_mappa_95.py e prova_scheda_case.py), un grafico a barre, 10 omini con 1 colorato, un pezzo di mappa con le sezioni colorate (puoi usare uno screenshot della mappa vera), il piè di pagina con «Chi sono». Per ogni stile: due font (titoli e testi) da Google Fonts scaricati in sviluppo/prove_stile_font/ (niente link esterni), palette con i codici dei colori scritti sotto, versione chiara e scura. Il bene/male usa verde acqua → corallo. Controlla il contrasto dei testi (almeno 4,5:1) e scrivi i valori.
Fai gli screenshot (computer e telefono) con Playwright (Chromium in /opt/pw-browsers/chromium-1194/chrome-linux/chrome) e mettili in sviluppo/prove_stile_*.png. Esito corto in sviluppo/piani/ESITO_C4.md, commit e push sul ramo della sessione. Poi chiedi a Leo quale stile sceglie (o un misto) e fermati: il giro C5 parte solo dopo la sua scelta, scritta nella memoria.
```

## C5 — CLOUD: stile comune, numeri che contano, omini

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md (contiene lo stile scelto da Leo), sviluppo/piani/PIANO_GRAFICA.md e PIANO_RISULTATI.md. Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. Piano 4 passo 2 (H + I): assets/stile.css con lo stile scelto (variabili dei colori in :root, modo scuro con prefers-color-scheme, font salvati in assets/font/), icona del sito (assets/icona.svg + png), anteprima dei link su index.html e risultati.html (meta description, Open Graph e Twitter: titolo, descrizione, immagine assets/anteprima.png 1200x630 che crei tu con lo stile), barra in alto (Home · Risultati · Mappa · Il progetto; il bottone IT/EN arriva nel giro C6) e piè di pagina («Chi sono»: Leonardo Campese, https://www.linkedin.com/in/leocampese/, campese.leonardo@gmail.com, link al repository GitHub, licenza MIT, «dati aggiornati al …» letto dalle schede). index.html e risultati.html usano stile.css e non hanno più colori scritti dentro. Il pannello della mappa (scripts/mappa_template.html) usa gli stessi colori e font, ma resta un file unico (copia lo stile dentro al momento della generazione nel 04 o includi solo le variabili). Colori di mappa e schede ripensati insieme: bene/male verde acqua → corallo; le legende scrivono sempre i numeri.
2. Piano 4 passo 3 (B + C + L): i numeri che contano SOLO nei 5 riquadri della home, nel numero grande della scheda aperta (e nel contatore della home che arriva nel giro C8): salgono da 0 al valore in circa 1 secondo quando appaiono, una volta sola, formato italiano. Omini e quadratini nella scheda aperta, sotto il numero grande: nuovo tipo di grafico «unita» in scripts/schede_risultati.py e risultati.html (scheda 5: 10 omini, quanti colorati dal numero vero; scheda 2: 100 quadratini, colorati = % oltre 5 minuti; scheda 3: un pallino per punto prioritario, colorato secondo la classe del bus contro auto). La finestra della scheda si apre con una dissolvenza. Con «riduci movimento» attivo, niente animazioni (numeri subito finali).
3. Piano 3 punto 3: grafico della metro nella scheda 5 rifatto come barre delle differenze (con metro − senza metro) per fascia di distanza, con il numero di zone scritto su ogni barra.
4. Prove: prova_pagine.py (0 errori), schede viste con dati veri ricavati dalla mappa (scripts/prove/), screenshot computer e telefono, chiaro e scuro, con e senza «riduci movimento»; peso di index.html + assets sotto 1 MB. Esito in sviluppo/piani/ESITO_C5.md con gli screenshot elencati; memoria; commit e push sul ramo della sessione. Scrivi a Leo i comandi per unire e cosa guardare (sul PC serve RIFAI_MAPPA_E_SCHEDE.bat).
```

## C6 — CLOUD: schede divise e testi IT/EN

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, sviluppo/piani/PIANO_CODICE.md (passo 4) e PIANO_GRAFICA.md (passo 5). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. Dividi scripts/schede_risultati.py in un pacchetto scripts/schede/ (comune.py, r1.py, r4.py, r6.py, r8.py, r10.py, r2.py) e un file di testi scripts/schede/testi.json con, per ogni frase fissa, la versione "it" e "en"; le frasi con numeri sono modelli con segnaposto ({valore}). scripts/schede_risultati.py resta come punto di ingresso con lo stesso comando. Regola d'oro: con gli stessi dati il file data/schede_risultati.js in italiano deve uscire IDENTICO a prima. Nel cloud provalo con i dati ricavati dalla mappa (scripts/prove/) e confronta il file prima/dopo con diff.
2. Ogni scheda ha ora anche i testi inglesi completi (titolo, domanda, testo del numero, punti chiave, grafici, calcolo, limiti), non solo le 3 righe di oggi. Inglese semplice e corretto.
3. Bottone IT/EN nella barra di index.html e risultati.html: cambia lingua senza ricaricare, ricorda la scelta (localStorage, protetto da try/catch), parte in inglese se la lingua del browser non è l'italiano; anche l'indirizzo ?lang=en funziona. La mappa resta in italiano.
4. Prove come nei giri precedenti, in entrambe le lingue. Esito in sviluppo/piani/ESITO_C6.md, con la lista delle frasi inglesi da far rileggere a Leo; memoria; commit e push sul ramo della sessione. Scrivi a Leo i comandi per unire e il giro P4.
```

## P4 — PC: stessi numeri dopo la divisione delle schede 🛑

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/ESITO_C6.md. Prima del pull copia data\schede_risultati.js in data\schede_risultati_prima.js. Poi: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
1. Lancia python scripts\schede_risultati.py. Confronta la parte italiana di data\schede_risultati.js con data\schede_risultati_prima.js: numeri e testi italiani uguali (le differenze ammesse sono i testi inglesi nuovi e quello che ESITO_C5/C6 dice di aver cambiato). Se cambia un numero, fermati e dillo a Leo.
2. python scripts\prova_pagine.py: 0 errori. Cancella data\schede_risultati_prima.js.
3. Mostra a Leo la lista delle frasi inglesi di ESITO_C6 e chiedi se vanno bene; correggi quelle che lui indica in scripts\schede\testi.json, rilancia le schede, commit e push su prova.
```

## C7 — CLOUD: gara bus contro auto

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_GRAFICA.md (elemento D, passo 4). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
Nella scheda 3 (parcheggi di scambio) il grafico principale diventa la gara: un bus e un'auto (icone semplici in SVG, colori dello stile) partono insieme da un punto e corrono su due corsie verso «Piazza Castello»; la durata è proporzionale ai minuti veri (1 minuto vero = circa 0,15 secondi); all'arrivo compaiono i minuti scritti; per l'auto una forbice (fattore dei sensori e fattore di Google) mostrata come due auto chiare o un tratto sfumato. Tendina con i 12 punti prioritari e i 5 interscambi; bottone «Riparti». Dati letti da quello che lo script 94 già scrive (data/processed/r6_bus_contro_auto.json) e portati nella scheda da scripts/schede/ (nuovo tipo di grafico «gara»); nessun numero scritto a mano. Con «riduci movimento»: barre ferme con i minuti. Funziona con tastiera e lettore di schermo (testo alternativo con i minuti).
Fai lo stesso componente riusabile in assets/gara.js: nel pannello della mappa, cliccando un punto del tema «Parcheggi di scambio», compare la gara piccola dello stesso punto.
Nel cloud costruisci un r6_bus_contro_auto.json di prova leggendo la struttura dallo script 94 (oppure ricavalo da mappa_torino.html, che ha i tempi nel pannello). Prove, screenshot, esito in sviluppo/piani/ESITO_C7.md, memoria, commit e push. Scrivi a Leo i comandi per unire e di lanciare RIFAI_MAPPA_E_SCHEDE.bat.
```

## C8 — CLOUD: home con i mezzi in movimento

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_GRAFICA.md (elementi A, J, K, passo 6). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py. Serve data/storico_riassunti/ora_tipica.json (giro P3): se non è in git, fermati e dillo a Leo.
1. A: in alto nella home un riquadro scuro a tutta larghezza con la forma di Torino (confine comunale semplificato, puoi ricavarlo dai dati della mappa) e i puntini dei mezzi di ora_tipica.json che si muovono (canvas, interpolazione fra le posizioni, scia corta; colori diversi per bus, tram e metro); l'ora reale scorre da 7:30 a 8:30 in circa 20 secondi e poi ricomincia; sopra, il titolo e una riga. Si ferma quando la scheda del browser non è visibile. Con «riduci movimento»: un fotogramma fermo. Peso del file dei dati sotto 300 KB, home sotto 1 MB in tutto.
2. J: contatore sotto il titolo «Il Raspberry Pi legge Torino da N giorni: X milioni di posizioni dei mezzi», con N e X scritti dallo script delle schede leggendo i riassunti (nessun numero a mano); il numero conta da 0 una volta sola.
3. K: miniatura in ogni riquadro dei 5 risultati: immagine piccola (WebP, sotto 40 KB) creata da prova_pagine.py con uno screenshot del grafico principale della scheda o della vista della mappa collegata; salvata in assets/miniature/.
4. Prove su computer e telefono, chiaro e scuro, con e senza «riduci movimento»; controlla che l'animazione non scaldi il processore (fotogrammi limitati a 30 al secondo). Esito in sviluppo/piani/ESITO_C8.md, memoria, commit e push. Scrivi a Leo i comandi per unire.
```

## C9 — CLOUD: mappa

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md (sezione 8, regole della mappa: D.sezioni a colonne, COLONNE_SEZ, aggiornaLegenda) e sviluppo/piani/PIANO_GRAFICA.md (elementi F, L, M, passo 7). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
Lavora su scripts/mappa_template.html e, se serve, scripts/04_genera_mappa.py. Nel cloud la mappa si prova sui dati già dentro mappa_torino.html (scripts/prove/estrai_dati_giro4.py mostra come estrarli e reinserirli).
1. F: nei temi che cambiano con l'ora un bottone ▶ / ❚❚ accanto al cursore dell'ora: scorre dalle 6 alle 24, circa 1 secondo per ora, con passaggio morbido di colore fra un'ora e l'altra; la legenda si aggiorna; si ferma se l'utente tocca il cursore.
2. L: mentre la pagina si carica, il contorno di Torino che si disegna e una barra di avanzamento; sparisce quando la mappa è pronta.
3. M: su telefono (sotto 640 px) il pannello diventa un foglio che sale dal basso (chiuso mostra solo il tema scelto); schede che si aprono cliccando un'area tutte uguali (titolo = nome del posto, 3-5 righe, fonte in piccolo) in tutti i temi; bottone «Copia il link di questa vista» (tema, vista, ora, zoom e centro nell'indirizzo; all'apertura la mappa torna lì).
4. Peso della mappa non oltre i 6 MB di oggi. prova_pagine.py 0 errori in tutti i temi; screenshot di ogni tema su computer e telefono. Esito in sviluppo/piani/ESITO_C9.md, memoria, commit e push. Scrivi a Leo i comandi per unire e il giro P5.
```

## P5 — PC: rilancio e controllo a occhio 🛑 → main

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e gli esiti C5-C9. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
1. scripts\RIFAI_MAPPA_E_SCHEDE.bat, poi python scripts\prova_pagine.py: 0 errori. Controlla il peso di mappa_torino.html (non oltre 6 MB) e della home.
2. Avvia python -m http.server 8765 nella cartella e di' a Leo di aprire http://localhost:8765/ e controllare, uno per uno: home (animazione dei mezzi, contatore, 5 riquadri con miniatura, numeri che contano solo lì), risultati (barra, IT/EN, scheda 3 con la gara, schede 2, 3, 5 con omini/quadratini), mappa (▶ delle ore, caricamento, pannello su telefono con la vista «telefono» del browser, copia link). Raccogli le sue osservazioni in sviluppo/piani/ESITO_P5.md.
3. Commit e push su prova. Se Leo dice che va bene: git checkout main, git pull origin main, git merge --no-edit prova, git push origin main, git checkout prova. Poi python scripts\controlla_rami.py: main uguale a prova.
```

## C10 — CLOUD: area che si espande

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, docs/R8_traffico.md e sviluppo/piani/PIANO_GRAFICA.md (elemento E, passo 8). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. Controlla nello script 93 se data/processed/tp_contro_auto.json contiene i tempi coi mezzi e in auto per TUTTE le coppie di zone (campo «coppie»), o solo quelle con viaggi in auto. Se non tutte, modifica il 93 perché salvi anche la tabella completa zona × zona (tempi coi mezzi, auto con i due fattori) senza cambiare nient'altro del risultato.
2. Scrivi lo script nuovo (prossimo numero libero dalla memoria) che calcola, da Piazza Castello, il tempo coi mezzi (r5py come lo script 18: 2026-10-12, partenza 7:45, finestra 30 minuti, mediana) e in auto (rete del modello del traffico come lo script 93, flusso libero × i due fattori + 5 minuti di parcheggio) verso il centro di ogni sezione di censimento abitata; uscita compatta in data/processed/area_tempi.json (tempi in minuti interi). Opzione --prova con 200 sezioni.
3. Nella scheda 4 un grafico «area che si espande»: mappa semplice (sezioni come quadratini o forme semplificate, sfondo dello stile) con due colonne «coi mezzi» e «in auto»; un cursore e un ▶ fanno crescere le aree minuto per minuto fino a 60 minuti, con le soglie 10, 20, 30, 45 scritte e la percentuale di torinesi raggiunti a ogni soglia. Tendina della partenza: «Piazza Castello» (dettaglio per sezione) e tutte le zone di Torino dalla tabella zona × zona (dettaglio per zona). Dati portati nella scheda dallo script delle schede, peso aggiuntivo sotto 400 KB. Con «riduci movimento»: le 4 soglie affiancate e ferme.
4. Nel cloud prova con dati finti nello stesso formato. Esito in sviluppo/piani/ESITO_C10.md con i comandi per il PC; memoria; commit e push. Scrivi a Leo i comandi per unire e il giro P6.
```

## P6 — PC: tempi da Piazza Castello

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/ESITO_C10.md. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
1. Se ESITO_C10 dice che il 93 è stato modificato: rilancialo e controlla che il titolo del risultato e i numeri del rapporto RAPPORTO_TP_CONTRO_AUTO.txt siano identici a prima (salvo la data).
2. Lancia lo script nuovo prima con --prova, poi completo (in una finestra .bat a parte se dura più di 10 minuti). Controlli di buon senso: Piazza Castello → Porta Nuova coi mezzi sotto 15 minuti; in auto il centro sotto 10 minuti a flusso libero; nessun tempo negativo; quante sezioni senza collegamento entro 120 minuti.
3. scripts\RIFAI_MAPPA_E_SCHEDE.bat, python scripts\prova_pagine.py (0 errori). Esito in fondo a ESITO_C10.md, commit e push su prova. Di' a Leo di aprire risultati.html, scheda 4, e cosa deve vedere.
```

## C11 — CLOUD: la pagina «Il progetto»

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, sviluppo/TESI_E_PROGETTO.md (attenzione: i dati della letteratura segnati DA VERIFICARE non vanno usati) e sviluppo/piani/PIANO_GRAFICA.md (elementi G e N, traccia in 6 parti). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
Crea progetto.html con lo stile comune, la barra e IT/EN: pagina a scorrimento con il testo a sinistra e un disegno fisso a destra che cambia a ogni paragrafo (su telefono il disegno sta sopra il testo). Sei parti: la promessa (tesi 2020), il sistema (schema animato N: sensori e GPS → Raspberry Pi → storico → script → pagine, con i numeri veri della raccolta), chi abita dove (fragilità, servizi, le 5 zone in doppio svantaggio che si accendono: usa i dati già nella mappa o nelle schede), muoversi (rimando alle schede 3 e 4 con un'immagine), quanto ci si può fidare dei dati (feed dei ritardi che sbagliava di 2-3 volte, mezzo con l'orologio 3 anni avanti, feed fermo il 18/10), cosa manca e chi sono. Ogni numero letto dai file dei risultati (nessun numero a mano: se serve, lo script delle schede scrive un piccolo data/progetto.js). Testi brevi, in prima persona, semplici; inglese completo. Link dalla barra e in fondo a risultati.html («Perché questo progetto»). Con «riduci movimento»: niente animazioni. Peso sotto 1,5 MB.
Prove, screenshot, esito in sviluppo/piani/ESITO_C11.md con i testi da far rileggere a Leo, memoria, commit e push. Scrivi a Leo i comandi per unire.
```

## C12 — CLOUD: ultimi pezzi per la pubblicazione

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, sviluppo/piani/PIANO_RIORGANIZZAZIONE.md, PIANO_GRAFICA.md e PIANO_CODICE.md. Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. 404.html nello stile del sito, con i link alle pagine (GitHub Pages la usa da sola).
2. Pagine dei singoli risultati (elemento P): lo script delle schede scrive r/1.html … r/5.html, pagine minime con titolo, descrizione e immagine di anteprima del risultato (Open Graph; immagine 1200x630 creata da prova_pagine.py dalla scheda) che portano subito a ../risultati.html#pN. Il bottone «Condividi» nella scheda copia l'indirizzo r/N.html.
3. README.md nuovo (piano 1 passo 9), italiano e poi inglese: una riga su cosa è; link al sito https://campeseleonardo-tech.github.io/Turin-mobility/; screenshot di home, una scheda e la mappa (in assets/readme/); i 5 risultati con una riga e il numero letto dalle schede (lo scrive lo script delle schede fra due commenti segnaposto, così non invecchia); come è fatto (Raspberry Pi, Python, pagine senza librerie); fonti e licenze (da docs/FONTI_DATI.md); come rifare i calcoli in 3 comandi; «Chi sono» (Leonardo Campese, LinkedIn, email).
4. Piano 5 passo 2: .github/workflows/controllo.yml: a ogni push su prova e main compila gli script, lancia pyflakes (solo errori, non le variabili inutilizzate), prova_pagine.py con Playwright, il controllo dei pesi e dei link interni. Badge nel README.
5. Piano 5 passo 3: scripts/rifai_tutto.py: lancia nell'ordine giusto le catene (leggi i .bat e la memoria per l'ordine: dati, accessibilità, risultati 1-4-6-8-10, schede, mappa, prova); si ferma al primo errore, salva a che punto è arrivato e riparte da lì con --riprendi; --solo schede,mappa per lanciare solo una parte. Nel README: «scarica_dati.py, poi rifai_tutto.py».
6. Prove, esito in sviluppo/piani/ESITO_C12.md, memoria, commit e push. Scrivi a Leo i comandi per unire e il giro P7.
```

## P7 — PC: prova da zero e pubblicazione 🛑 → main

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/ESITO_C12.md. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
1. Rilancio completo: python scripts\rifai_tutto.py (anche più ore: lancialo in una finestra .bat a parte con il log in logs\). Alla fine: i rapporti in docs\rapporti hanno gli stessi numeri di prima (git diff: cambiano solo le date) e prova_pagine.py dà 0 errori.
2. Prova da zero: in una cartella temporanea fuori dal progetto, git clone, python scripts\scarica_dati.py, python scripts\rifai_tutto.py --solo schede,mappa (e, se il tempo lo permette, tutto): le schede escono con gli stessi numeri. Scrivi le differenze in sviluppo/piani/ESITO_P7.md.
3. Controlla che su GitHub il controllo automatico (Actions) sia verde sull'ultimo commit di prova.
4. Commit e push su prova. Se Leo dice che va bene: unisci prova in main (git checkout main, git pull origin main, git merge --no-edit prova, git push origin main, git checkout prova).
5. Di' a Leo i passi su GitHub, a mano: Settings → Pages → Source «Deploy from a branch», ramo main, cartella / (root) → Save; dopo un paio di minuti il sito è su https://campeseleonardo-tech.github.io/Turin-mobility/. Poi nella pagina principale del repository, rotella accanto ad «About»: descrizione in una riga, sito, argomenti (torino, public-transport, open-data, gtfs, raspberry-pi, data-visualization). Settings → General → Social preview: carica assets/anteprima.png.
6. Apri il sito pubblicato e controlla con Leo: tutte le pagine, i link r/1.html … condivisi su LinkedIn (strumento Post Inspector di LinkedIn) mostrano l'anteprima giusta.
```

## C13 — CLOUD: pulizia del codice (a pezzi)

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_CODICE.md (passi 5-8). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
Fai UN gruppo di script per sessione (es. 21-29, poi 33-50, poi 51-67, poi 68-95), non tutto insieme:
1. Le funzioni copiate (distanze, ora legale, lettura del GTFS, percentili) diventano chiamate a scripts/comuni.py; prima confronta le copie: se una è diversa (es. raggio della Terra o arrotondamento), tieni il comportamento dello script e scrivilo nell'esito.
2. Togli le variabili e gli import mai usati segnalati da pyflakes in quegli script.
3. Per ogni script dei risultati del gruppo, una prova su dati finti con il risultato atteso (molti hanno già --prova): aggiungila al controllo automatico.
4. Nessun numero dei risultati deve cambiare: scrivi nell'esito quali script Leo deve rilanciare sul PC e quali rapporti confrontare (devono essere uguali salvo la data).
Prove, esito in sviluppo/piani/ESITO_C13_<gruppo>.md, memoria, commit e push. Scrivi a Leo i comandi per unire e cosa rilanciare.
```

## P8 — PC, metà novembre: R4 con un mese di dati

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e docs/R4_puntualita.md. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
Rilancia il R4 (27 e 70, come scritto in docs/R4_puntualita.md) su tutti i giorni raccolti; se esiste, aggiorna prima i riassunti dello storico (97). Tabella prima/dopo dei numeri principali (% oltre 5 e oltre 10 minuti, attese, linee peggiori): differenze oltre il 20% = AVVISO da spiegare. Rilancia schede e mappa (RIFAI_MAPPA_E_SCHEDE.bat), prova_pagine.py 0 errori. Aggiorna docs/R4_puntualita.md e la memoria, esito in sviluppo/piani/ESITO_P8.md, commit e push su prova. Se Leo dice ok, unisci in main.
```

---

## L1 — PC: tutto quello che manca dei giri PC (P1, P3, P5, P6, P7), con C13 provato sui dati veri

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md e sviluppo/MEMORIA_PROGETTO.md (sezioni 5 e 6) e gli esiti ESITO_C10, C11, C12 e ESITO_C13_21-29 in sviluppo/piani/.
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py (fermati se segnala lavoro non unito). Un passo per volta; se un passo fallisce, fermati e dillo a Leo con l'errore.
1. P1: se manca config_locale.json crealo da scripts\config_locale.esempio.json chiedendo a Leo i valori (non finiscono in git); scripts\CONTROLLA_LEOPI.bat deve funzionare.
2. P3 (solo se non fatto: guarda ESITO_C3/ESITO_P3): scripts\RIASSUNTI_STORICO.bat (prima un mese con --mese 2026-10), python scripts\confronta_riassunti.py (avvisi: 0), python scripts\96_inventario_dati.py --gitignore, python scripts\98_prepara_release.py; di' a Leo nomi e pesi degli zip (li carica lui a mano nella Release).
3. python scripts\97_riassunti_storico.py --solo ora --rifai (l'ora tipica deve coprire quasi tutta l'ora).
4. P6: scripts\AREA_TEMPI.bat. Controlli di buon senso nel rapporto docs\rapporti\RAPPORTO_AREA_TEMPI.txt: Piazza Castello-Porta Nuova coi mezzi sotto 15 minuti, auto in centro sotto 10, nessun tempo negativo, quante sezioni senza collegamento. Se sono strani, fermati.
5. scripts\RIFAI_MAPPA_E_SCHEDE.bat; poi python scripts\prova_pagine.py (0 errori). Controlla che esistano data\area_tempi.js, data\progetto.js, r\1.html..5.html, assets\anteprime\r1..r5.jpg, assets\readme\*.jpg e che il README elenchi i 5 risultati con numeri veri.
6. C13 sui dati veri: per lo script 25 e 29 rilancia e confronta i rapporti con quelli di prima (uguali salvo la data). Poi, un gruppo per volta (33-50, 51-67, 68-95): togli le copie di funzioni comuni (comuni.py) e le segnalazioni pyflakes (python -m pyflakes scripts), rilancia gli script toccati, confronta i rapporti (git diff docs\rapporti: cambia solo la data), un commit per gruppo, scrivi sviluppo/piani/ESITO_C13_<gruppo>.md. Nessun numero dei risultati deve cambiare: se cambia, ripristina e dillo a Leo.
7. P7: python scripts\rifai_tutto.py --elenco, poi il rilancio completo in una finestra a parte (anche ore; log in logs\rifai_tutto.log). Se un comando e' fuori ordine, correggi la lista FASI in scripts\rifai_tutto.py e riparti con --riprendi. Alla fine i rapporti in docs\rapporti hanno gli stessi numeri di prima (cambiano le date) e prova_pagine.py da' 0 errori. Prova "da zero" in una cartella temporanea: git clone, python scripts\scarica_dati.py, python scripts\rifai_tutto.py --solo schede,mappa. Scrivi le differenze in sviluppo/piani/ESITO_P7.md.
8. Controlla su GitHub che il controllo automatico (Actions, controllo.yml) sia verde sull'ultimo commit; se e' rosso, correggi.
9. Aggiorna sviluppo/MEMORIA_PROGETTO.md (sezioni 4-6, massimo 120 righe) solo con quello che e' cambiato, poi git add -A, git status (niente data\ non voluti, .bak, chiavi), commit, git pull --no-rebase origin prova, git push origin prova.
Alla fine di' a Leo in 5 righe cosa e' cambiato, cosa deve guardare (index.html, risultati.html scheda 4, progetto.html, mappa) e i passi a mano su GitHub: unire prova in main, Settings > Pages (ramo main, cartella /), descrizione del repository, anteprima social, Post Inspector di LinkedIn sui link r/N.html. P8 (R4 con un mese di dati) resta a meta' novembre.
```

## L2 — PC: revisione grafica di Leo del 23/10 (home, numeri che salgono, schede, animazioni)

Cosa vuole Leo e perché: `PIANO_GRAFICA.md`, sezione «Revisione di Leo (23/10)» (titoli, animazioni, struttura delle schede). Era il giro cloud C14: lo fa l'agente
in locale perché sul PC ci sono i dati e può rilanciare tutto. **Bozza di codice** di Claude: `sviluppo/piani/C14_bozza.patch` (scritta sulla versione di `prova` del 23/10 mattina,
prima di C10-C13). Sulla `prova` delle 18:32 del 23/10 si applicano ancora 12 file su 16; **non** si applicano `risultati.html`, `scripts/schede/r6.py`, `scripts/schede/r8.py`
e `scripts/schede/testi.json` (cambiati da C10 e C12): questi si rifanno a mano, guardando la bozza come esempio.
**Prima di lanciarlo Leo sceglie** (scrivilo in cima al prompt): AGGIORNA_RISULTATI = sì / no (rilanciare R4, R6, R8 con lo storico di oggi: in P7 dava R4 oltre 5' 14,1% → 15,6%,
oltre 10' 5,44% → 6,19%, R8 errore ±38% → ±28%; i titoli si aggiornano da soli).

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_GRAFICA.md (sezione «Revisione di Leo (23/10)», tutta).
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py (fermati se segnala lavoro non unito). Un passo per volta; se un passo fallisce, fermati e dillo a Leo con l'errore.
REGOLA DI LEO: i controlli grafici li fa solo lui. Tu NON guardi schermate e NON giudichi colori, misure o impaginazione. Controlli che il codice giri: script senza errori, prova_pagine.py con 0 errori JavaScript, numeri giusti nei JSON. Alla fine gli dai una lista di cosa guardare.

0. Solo se in cima al prompt c'è AGGIORNA_RISULTATI = sì: python scripts\rifai_tutto.py --da traffico (49 minuti in P7). Scrivi una tabella prima/dopo dei numeri principali di R4, R6, R8 (docs\rapporti, git diff) e aggiorna i numeri in docs\R4_puntualita.md, docs\R6_parcheggi.md, docs\R8_traffico.md e nella memoria. Commit a parte «Risultati rifatti con lo storico al <data>».
1. Bozza: git apply --include="assets/*" --include=index.html --include="scripts/schede/comune.py" --include="scripts/schede/home.py" --include="scripts/schede/r1.py" --include="scripts/schede/r4.py" --include="scripts/schede/r10.py" --include="scripts/schede/traduci.py" sviluppo\piani\C14_bozza.patch
   Leggi TUTTO il diff applicato (git diff) e quello non applicato (le parti di risultati.html, r6.py, r8.py, testi.json nella patch): devi capire cosa fa prima di andare avanti.
2. NUMERI CHE SALGONO (assets/sito.js, contaSu, dalla bozza): circa 2,6 secondi, partenza e arrivo morbidi; durante la corsa solo interi, senza virgola né %; il testo finale (decimali, %) solo all'arrivo; larghezza fissata a quella del testo finale prima di partire; data-forbice="21,28" fa salire due numeri insieme. git grep data-suffisso: togli gli usi rimasti (anche in r/*.html se lo script delle schede li scrive).
3. HOME (dalla bozza: index.html, mezzi.js, stile.css, home.py). Titolo «Torino Mobilità» in oro; sottotitolo «Un progetto per capire come si muove la città.»; frase «Da N giorni raccogliamo, minuto per minuto, i dati di bus, tram e traffico di Torino, e continuiamo: per capire chi va dove, e come ci va.» con N = giorni da INIZIO_RACCOLTA (home.py) a oggi, contati nel browser. I 5 riquadri mostrano l'animazione della scheda in piccolo (Anima.html(f.anima, {compatto: true})).
   Le miniature in assets/miniature/ non servono più: togli da scripts/prova_pagine.py la parte che le rifà (fai_miniature, MINIATURE e la riga della descrizione), cancella la cartella, git grep miniature e aggiorna i rimandi. NON toccare assets/anteprime/ (immagini per i link condivisi, C12) né assets/readme/ (README).
   Il riquadro è un link <a>: dentro niente pulsanti né tendine (la gara mini non disegna i comandi: verificalo nel codice di gara.js).
4. SCHEDE: STRUTTURA (risultati.html, a mano: la bozza non si applica perché C10 ha aggiunto l'area e C12 altre cose; tieni tutto quello che c'è di nuovo).
   Ordine nella scheda aperta: domanda → numero grande (sale; attributi con una funzione attrConta come nella bozza) → animazione (f.anima; se manca la figura vecchia f.unita) → 3 punti chiave → grafico principale → «Vedi sulla mappa» → «Altri grafici» APERTI (sottotitolo, non <details>), compresa l'area della scheda 4 se non è l'animazione principale (vedi 6) → f.extra aperta → UNA sola parte chiusa «Come l'abbiamo calcolato e limiti» (calcolo, confronto, criteri, poi «Limiti»).
   Via la parte «In English» (la riga parte("In English", …)): l'inglese resta col bottone IT/EN. In comune.py (bozza) forma_base non salva più «english» e controlla_forma non la conta; controlla con git grep english che non resti nulla (anche le pagine r/N.html e il README scritti dallo script delle schede).
5. TITOLI E TESTI (r1.py, r4.py, r10.py dalla bozza; r6.py a mano, vedi sotto). Titoli della tabella di PIANO_GRAFICA.md. Regole:
   - i numeri nei titoli si calcolano dai dati, mai a mano («2 su 3» da frazione(n_senza / n_fermate); «Circa il 5%» da round del ritardo oltre 10 minuti: con AGGIORNA_RISULTATI = sì diventa «6%», va bene così);
   - scheda 5: il 9,5% è dei residenti delle «zone abitate», non di tutti i torinesi (79.598 / 848.748 = 9,4%): il testo dice «dei residenti delle zone abitate». Correggi anche README e r/5.html se lo riportano (li scrive lo script delle schede: controlla che dopo il rilancio sia giusto);
   - scheda 3 riorganizzata (Leo: il risultato è quanto è facile lasciare l'auto; i minuti di parcheggio sono una postilla): numero grande = fermate importanti senza posti bastanti; grafico principale = i 12 punti per bisogno; altri grafici = gara (gira da sola), minuti di pareggio, parcheggi di scambio esistenti con lo stato (pieno di giorno / a metà / con posti liberi / non misurato, campo «stato» in r6_bus_contro_auto.json); punti chiave = nessun parcheggio / pochi posti, il primo punto d'ingresso, il pareggio. Guarda la parte r6.py della bozza (funzioni frazione e anima_fermate e la fine di forma_r6) e riportala a mano;
   - ATTENZIONE in r6.py: alcune righe sono IDENTICHE in scheda_r6() e forma_r6() (es. «val = rie.get(...)»). Ogni modifica va cercata dentro la funzione giusta, mai con la prima occorrenza del file. Dopo, python -m pyflakes scripts: deve restare a zero (C13).
6. ANIMAZIONI (assets/animazioni.js dalla bozza, nuovo; gara.js dalla bozza). Una per scheda, in f.anima, scritta dai moduli Python con i numeri dei dati:
   scheda 1 «cerchi» (5/10/15 minuti col %); scheda 2 «quadratini» (oltre 5 e oltre 10 minuti, poi le 4 fasce orarie in giro); scheda 3 «fermate» (Torino e le 274 fermate che si colorano, poi i 12 punti; il riquadro del disegno si calcola su fermate + contorno perché molte fermate sono in cintura); scheda 5 «omini».
   Scheda 4: DIVERSO dalla bozza. Dopo C10 la scheda ha già «l'area che si espande» (f.area, assets/area.js), che è un'animazione: è lei l'animazione principale (mettila al posto di f.anima nella scheda e nella home: nella home una versione piccola, senza tendina, che parte da sola; se area.js non ha una versione piccola, aggiungila con un'opzione, senza cambiare quella grande). La gara sui 6 viaggi tipici (parte r8.py della bozza) va negli «Altri grafici» della scheda 4.
   Gara (gara.js dalla bozza): opzione giro (finita una corsa, dopo 2,2 secondi la successiva; solo mentre si vede; la tendina ferma il giro), nome della partenza sopra la corsa, campo «arrivo» per luogo, opzione mini (niente comandi). La gara piccola nel pannello R6 della mappa resta come prima (compatto SENZA mini): verificalo in scripts/mappa_template.html (r6Gara).
   Tutte: con «riduci movimento» la figura finale ferma con i numeri scritti; partono quando entrano nella finestra; se un dato manca la scheda si vede senza animazione e senza errori.
7. INGLESE: ogni frase nuova ha la traduzione in scripts/schede/testi.json («esatte» o «modelli» con {n0}, {s0}, {t0}); prendi quelle della parte testi.json della bozza e aggiungile a mano (il file è cambiato: non riscriverlo tutto, aggiungi solo le voci). «contorno» in SALTA di traduci.py (bozza). python scripts\schede_risultati.py: NESSUNA riga «ATTENZIONE» (traduzioni mancanti, frasi oltre 20 parole: la regola che divide le frasi non taglia dopo una cifra, «alle 8. L'auto» resta una frase sola).
8. PROVE (solo funzionamento): python -m pyflakes scripts (zero); node --check assets\*.js; python scripts\schede_risultati.py (5 schede, nessuna ATTENZIONE; ogni forma ha anima o area; numeri delle animazioni uguali ai rapporti: scheda 3 95+111+68 = 274, scheda 1 68,3 / 96,8 / 99,2 se i dati non sono cambiati); scripts\RIFAI_MAPPA_E_SCHEDE.bat; python scripts\prova_pagine.py: 0 errori su tutte le pagine; controllo automatico di GitHub verde dopo il push.
9. Cancella sviluppo\piani\C14_bozza.patch. Esito in sviluppo/piani/ESITO_L2.md: cosa hai preso dalla bozza, cosa hai rifatto a mano e perché, eventuali scelte tue (con il valore predefinito). Memoria (sezioni 4-6, massimo 120 righe). git add -A, git status, commit, git pull --no-rebase origin prova, git push origin prova.
Alla fine dai a Leo la LISTA DA GUARDARE (computer e telefono, chiaro e scuro): home (titolo oro, frase dei giorni, 5 riquadri animati, numeri che salgono piano senza virgola né % durante la corsa); schede (niente «In English», una sola parte chiusa, titoli nuovi, le 5 animazioni, gara della scheda 3 che gira da sola, area della scheda 4); mappa (gara piccola nel pannello dei parcheggi come prima).
```

## L3 — PC: bus contro auto a 4 ore del giorno (schede 3 e 4) 🛑

Richiesta di Leo (23/10): i confronti bus/auto non solo all'ora di punta. Era il giro C15 + P10; in locale si fa in un giro solo. Dopo L2, e dopo che Leo ha guardato L2.
Scelte di Claude (valori predefiniti; Leo può cambiarle prima del lancio):
- **4 ore**, le fasce della scheda 2: 8:00 (punta del mattino, c'è già), 13:00, 17:30, 21:00. Feriale 2026-10-12, finestra di 30 minuti, mediana, come gli script 93 e 94.
- **Auto all'ora h** = flusso libero × fattore(h) + 5 minuti di parcheggio. fattore(h) dai sensori 5T (`data/processed/velocita_5t.json`, feriali): mediana sui sensori urbani di (velocità di notte, 3-5) / (velocità all'ora h). Deve dare 1,2 ± 0,1 alle 8 come oggi, se no ci si ferma.
  Il fattore di Google (2,1) esiste solo alle 8: alle altre ore si scala nello stesso rapporto, fattore_basso(h) = 1 + (2,1 − 1) × (fattore(h) − 1) / (fattore(8) − 1). È un'ipotesi e va nei limiti delle schede.
- **Regola del titolo della scheda 4, fissata prima dei numeri**: se a tutte e 4 le ore il rapporto mediano resta entro ±0,3 da quello delle 8, con tutti e due i fattori → «A ogni ora del giorno, coi mezzi pubblici si impiega da X a Y volte il tempo dell'auto»;
  altrimenti il titolo resta «Al mattino…» e un punto chiave dice da quanto a quanto cambia durante il giorno. Scheda 3: il titolo resta sui parcheggi.
- L'area che si espande (script 99) resta alle 8: per sezione a 4 ore il calcolo è lungo; solo se Leo lo chiede dopo.

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, docs/R6_parcheggi.md, docs/R8_traffico.md, sviluppo/piani/ESITO_L2.md e il blocco L3 di sviluppo/piani/PROMPT_LAVORI.md (scelte e regola del titolo: non cambiarle dopo aver visto i numeri).
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py. Un passo per volta; se un passo fallisce, fermati e dillo a Leo.
REGOLA DI LEO: niente controlli grafici, li fa lui.
1. Leggi gli script 93 e 94: come calcolano i tempi coi mezzi (r5py) e in auto. Non copiarne il codice: riusa le funzioni con comuni.carica_script come fa il 94.
2. Scrivi scripts/100_ore_del_giorno.py (100 è il prossimo numero libero: controllalo nella memoria; aggiornalo a 101). Sola lettura sui dati. Costante ORE in testa. Per ogni ora: tempi coi mezzi dai 12 punti prioritari e dai 5 interscambi a Piazza Castello (come il 94) e per le coppie di zone del 93 (gruppi a e b; se tutte a 4 ore richiedono più di 2 ore di calcolo, le 600 coppie con più auto, scritto nel rapporto). Auto con fattore(h) e fattore_basso(h) del blocco L3.
   Uscite: data/processed/ore_del_giorno.json (per ora: luoghi del R6 con tp, auto_alto, auto_basso; coppie con tp, auto, auto_basso; rapporto mediano pesato per le auto del mattino con i due fattori; quota di auto con rapporto oltre 2) e docs/rapporti/RAPPORTO_ORE_DEL_GIORNO.txt.
   Opzioni: --prova (dati finti piccoli, cartella temporanea), --campione N (solo N zone). Controlli: fattore alle 8 = quello di oggi entro ±0,1 (bloccante); alle 8 tempi coi mezzi uguali a r6_bus_contro_auto.json e tp_contro_auto.json entro 1 minuto (AVVISO); nessun tempo nullo, negativo o infinito (bloccante); di sera i luoghi senza collegamento entro 120 minuti si contano a parte.
3. Prova: --prova, poi --campione 10 (durata). Stima la durata intera e dilla a Leo; se supera 2 ore prepara scripts\ORE_DEL_GIORNO.bat (cd /d "%~dp0..", log in logs\, stop al primo errore) e chiedi a Leo di lanciarlo in una finestra sua; aggiungi il comando a rifai_tutto.py dopo il 94 e il 93.
4. Calcolo intero. Buon senso: alle 8 uguale a oggi; a mezzogiorno e di sera l'auto più veloce che alle 8; i mezzi di sera più lenti o uguali. Tabella ora per ora (rapporto mediano, auto oltre 2 volte) nell'esito.
5. Schede (r6.py, r8.py, gara.js), solo se ore_del_giorno.json c'è; se manca, le schede restano come dopo L2:
   - gara della scheda 3 e gara dei viaggi tipici della scheda 4: ogni luogo corre alle 4 ore una dopo l'altra (ora scritta sopra la corsa e nella frase per il lettore di schermo: campo facoltativo «ora» per ogni corsa), poi il luogo dopo; nella home (mini) solo le 8;
   - scheda 4: grafico a linea «Quante volte il tempo dell'auto, ora per ora» (due serie, fattore alto e basso) negli «Altri grafici»; titolo secondo la regola del blocco L3;
   - limite nuovo nelle schede 3 e 4: «Il rallentamento dell'auto alle altre ore viene dai sensori; quello di Google si conosce solo alle 8 ed è stato scalato.»; traduzioni in testi.json.
6. Prove: python -m pyflakes scripts (zero); python scripts\schede_risultati.py (nessuna ATTENZIONE); scripts\RIFAI_MAPPA_E_SCHEDE.bat; python scripts\prova_pagine.py (0 errori); docs\R6_parcheggi.md e docs\R8_traffico.md con la tabella delle ore e il comando per rifarle.
7. Esito sviluppo/piani/ESITO_L3.md (durata, tabella, quale titolo è uscito per la scheda 4 e perché), memoria, commit, git pull --no-rebase origin prova, git push origin prova. Di' a Leo cosa guardare: schede 3 e 4 (gara con le ore, linea ora per ora).
```

## Dopo L3 (Leo, a mano)
Leo guarda tutto; se va bene: `git checkout main`, `git pull origin main`, `git merge --no-edit prova`, `git push origin main`, `git checkout prova`; Settings > Pages (ramo `main`, cartella `/`), descrizione e argomenti del repository,
anteprima social, Post Inspector di LinkedIn sui link `r/N.html`. P8 (R4 con un mese di dati) a metà novembre.

## L4 — PC: raccolta del Pi più sicura (PIANO_RACCOLTA.md, passi 1, 2a e 3) 🛑

Perché (prove in `PIANO_RACCOLTA.md` e `ANALISI_CRITICA.md`, sezione 5): la copia giornaliera può sostituire lo storico buono con uno vuoto ma «integro»; il GTFS non si archivia
(quando GTT pubblica l'orario nuovo, al più tardi entro il 31/01/2027, le corse dei giorni nuovi non si abbinano più); spazio e scadenze sul Pi non arrivano mai a Leo.
Non tocca i file di L3. Il passo 2b (script 27 e 70 col GTFS di ogni giorno) è un giro a parte, dopo.
**Regole fissate ora, prima di vedere i numeri** (in testa agli script, come costanti):
- copia accettata solo se, per ogni tabella di `TABELLE` già presente nella copia vecchia: righe nuove ≥ righe vecchie; e per `mezzi_gtt` e `flussi_5t`: primo istante uguale e ultimo istante ≥ quello vecchio. Altrimenti la copia vecchia resta, la nuova diventa `storico_backup_SOSPETTO.sqlite` e il `.bat` dà ALLARME;
- spazio libero sul Pi: ALLARME sotto 5 GB, AVVISO sotto 10 GB; storico: AVVISO oltre 8 GB; `/tmp` del Pi: AVVISO se ha meno di 1,5 volte il peso dello storico (lì si fa lo snapshot); GTFS: ALLARME a 14 giorni o meno dalla scadenza, AVVISO a 45; archivio GTFS senza versioni o ultimo scaricamento riuscito più vecchio di 3 giorni: AVVISO; feed degli avvisi GTT in errore per tutte le ultime 24 ore: AVVISO;
- ALLARME = codice di uscita diverso da 0 e finestra di Windows (come oggi); AVVISO = riga nel registro e nel testo stampato, senza finestra.

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, sviluppo/piani/PIANO_RACCOLTA.md e il blocco L4 di sviluppo/piani/PROMPT_LAVORI.md (regole e soglie: non cambiarle).
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py (fermati se segnala lavoro non unito). Un passo per volta; se un passo fallisce, fermati e dillo a Leo.
REGOLE: verso il Pi solo SSH in sola lettura; tutto quello che scrive o riavvia sul Pi lo fa Leo con un .bat a doppio clic. NON lanciare tu backup_da_leopi.py né RACCOLTA_GIORNALIERA.bat (scrivono data\storico_backup.sqlite): li lancia Leo. Non toccare data\raw né lo storico. Niente controlli grafici.

1. COPIA CHE NON PERDE DATI (scripts/backup_da_leopi.py, scripts/RACCOLTA_GIORNALIERA.bat).
   a. Separa la decisione in una funzione pura, provabile senza Pi: decidi(riepilogo_vecchio, riepilogo_nuovo) -> (accetta: bool, motivi: list[str]), con la regola del blocco L4. I riepiloghi sono quelli di riepilogo_locale() (conteggi e intervalli). Per la copia vecchia basta leggere conteggi e intervalli (niente integrity_check: è lento su file grandi).
   b. Prima di os.replace: se c'è già data\storico_backup.sqlite e decidi() dice no → la nuova va in data\storico_backup_SOSPETTO.sqlite (sostituisce una SOSPETTO precedente), stampa i motivi, esci con codice 3. Se dice sì → la vecchia diventa data\storico_backup_ieri.sqlite (os.replace), poi la nuova prende il suo posto. Se sul disco del PC lo spazio libero è meno di 1,2 volte la copia nuova, salta la copia «ieri» con un AVVISO (mai fermare la copia per questo).
   c. Correggi la descrizione in testa al file («settimanalmente» → ogni giorno) e aggiungi il motivo delle regole.
   d. RACCOLTA_GIORNALIERA.bat: codice 3 = «ALLARME: la copia nuova dello storico è più piccola o diversa: tenuta quella di prima; la nuova è in data\storico_backup_SOSPETTO.sqlite». Fine riga Windows.
   e. Opzione --prova (cartella temporanea, due SQLite finti con le stesse tabelle): casi (1) nuova più grande → sostituita, c'è «ieri»; (2) nuova con meno righe → tenuta la vecchia, SOSPETTO, codice 3; (3) nuova vuota → come 2; (4) primo istante diverso → come 2; (5) nessuna copia vecchia → sostituita. Ogni caso stampa OK o ERRORE.
   f. Controlla che storico_backup_ieri.sqlite e _SOSPETTO non finiscano in git (git check-ignore) e aggiungili a docs/DATI.md (una riga ciascuno: solo sul PC).

2. ARCHIVIO DEL GTFS SUL PI (scripts/03_raccolta_continua.py, sul modello di giro_ztl).
   a. giro_gtfs(con): una volta al giorno (SECONDI_GTFS = 86400, anche all'avvio) scarica https://www.gtt.to.it/open_data/gtt_gtfs.zip (indirizzo già nello script 01), con timeout. Controlla che sia uno zip valido con stops.txt, trips.txt, stop_times.txt e calendar.txt o calendar_dates.txt; se no, registra_errore(con, "GTFS", …) e basta.
   b. Calcola sha256; se è diverso dall'ultimo in una tabella nuova gtfs_versioni (scaricato_utc, file, sha256, byte, valido_da, valido_a), salva il file nella cartella del Pi data/gtfs/gtt_gtfs_<AAAAMMGG>.zip (data italiana del giorno; se esiste già, aggiungi _2) e inserisci la riga. Validità: da feed_info.txt (feed_start_date, feed_end_date) se c'è, altrimenti minimo start_date e massimo end_date di calendar.txt, allargati con le date di calendar_dates.txt. Il file NON va dentro SQLite (lo storico crescerebbe a ogni versione).
   c. Ogni giorno, anche se invariato, scrivi nel log del raccoglitore «GTFS: invariato» o «GTFS: versione nuova …», come per la ZTL. Un errore non deve mai fermare la raccolta (try/except come gli altri giri).
   d. scripts/backup_da_leopi.py: aggiungi gtfs_versioni a TABELLE (così la copia la verifica). RACCOLTA_GIORNALIERA.bat: un passo che copia sul PC, in data\gtfs_archivio\, solo i file di data/gtfs/ del Pi che sul PC mancano (scp, sola lettura sul Pi); cartella fuori da git (git check-ignore) e in docs/DATI.md.
   e. Prova senza Pi: scripts/prove/prova_gtfs_archivio.py con un database temporaneo e due zip finti (prima versione salvata, stessa versione ignorata, versione nuova salvata, zip rotto → errore registrato, nessuna eccezione). Importa le funzioni del 03 senza far partire la raccolta (se il 03 non lo permette, sposta solo le funzioni del GTFS in testa al file senza cambiare il resto).

3. CONTROLLO GIORNALIERO PIÙ COMPLETO (scripts/controlla_leopi.py), soglie del blocco L4 come costanti in testa.
   a. Nel codice mandato al Pi (CODICE_PI, sempre sola lettura) aggiungi: spazio libero del disco dello storico (os.statvfs sulla cartella di dir_remota), spazio libero di /tmp e se /tmp è in memoria (tipo del file system da /proc/mounts), peso di storico.sqlite, ultima riga di gtfs_versioni (se la tabella c'è), ultimo errore e numero di errori del GTFS e del feed degli avvisi nelle ultime 24 ore (il nome della fonte degli avvisi è quello usato in scripts/12_ritardi_gtt.py: cercalo).
   b. Stampa una riga per ognuno (spazio in GB, peso, crescita in MB al giorno rispetto al lancio precedente salvato in logs\controlla_leopi_stato.json, GTFS «versione del …, valido fino al …, mancano N giorni»). ALLARME e AVVISO con le soglie del blocco L4; il codice di uscita cambia solo con ALLARME.
   c. Il feed degli avvisi «in errore per tutte le ultime 24 ore»: c'è almeno un errore in ognuna delle ultime 24 ore e nessuna riga nuova in avvisi_gtt nelle ultime 24 ore. Se la regola non si può applicare coi dati che ci sono, scrivi perché nell'esito invece di inventarne un'altra.
   d. Lancialo davvero (è sola lettura): python scripts\controlla_leopi.py. Scrivi nell'esito tutte le righe stampate (spazio, /tmp, peso, GTFS). Prima di 2 il GTFS darà AVVISO «archivio non attivo»: è giusto.

4. PROVE (solo funzionamento): python -m pyflakes scripts (zero); python scripts\backup_da_leopi.py --prova (5 casi OK); python scripts\prove\prova_gtfs_archivio.py (OK); python -m py_compile scripts\03_raccolta_continua.py; python scripts\controlla_leopi.py (righe nuove stampate, nessuna eccezione). Il controllo automatico di GitHub deve restare verde.
5. Esito in sviluppo/piani/ESITO_L4.md: cosa è cambiato, le righe del controllo, e i passi per Leo in quest'ordine:
   (1) doppio clic su scripts\AGGIORNA_RACCOLTA_LEOPI.bat (porta il 03 nuovo sul Pi e riavvia; nel log deve comparire «script ok» e «active»);
   (2) dopo 5 minuti, doppio clic su scripts\CONTROLLA_LEOPI.bat: la riga GTFS deve dire «versione del <oggi>»;
   (3) doppio clic su scripts\RACCOLTA_GIORNALIERA.bat: esito OK, in data\ c'è storico_backup_ieri.sqlite, in data\gtfs_archivio\ c'è uno zip.
   Memoria: una riga in sezione 4 (raccolta: copia protetta, GTFS archiviato, controllo con spazio e scadenza) e togli dal punto (5) di sezione 7 le parti risolte. Commit, git pull --no-rebase origin prova, git push origin prova.
```

## L4b — PC: snapshot della copia fuori da /tmp (PIANO_RACCOLTA passo 4) — URGENTE

Perché (ESITO_L4, controllo del 23/10): `/tmp` del Pi è in memoria (tmpfs) con 3,9 GB liberi; lo storico pesa 2,7 GB e cresce ~190 MB al giorno: **fra circa 6 giorni lo snapshot non ci sta più**
e la copia giornaliera comincia a fallire (in modo pulito, ma senza copie nuove). Il disco del Pi ha 87 GB liberi.
Regole fissate ora: snapshot in `<dir_remota>/data/tmp_copia/` (sul disco); prima di farlo, controllo che lì ci sia spazio libero ≥ 1,5 volte lo storico (se no ERRORE, la copia di prima resta);
si cancellano solo file di quella cartella col nome `gtt_storico_*.sqlite` più vecchi di 24 ore (resti di copie interrotte). Il controllo giornaliero guarda la cartella nuova invece di `/tmp`: ALLARME sotto 1,5 volte lo storico.

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, la memoria, sviluppo/piani/ESITO_L4.md e il blocco L4b di sviluppo/piani/PROMPT_LAVORI.md (regole: non cambiarle).
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py. Verso il Pi solo SSH in sola lettura; non lanci tu backup_da_leopi.py né RACCOLTA_GIORNALIERA.bat. Niente controlli grafici.
0. Chiusura di L4: leggi logs\raccolta_giornaliera.log, logs\backup_da_leopi.log e lancia python scripts\controlla_leopi.py (sola lettura). Scrivi nell'esito se Leo ha già fatto i 3 doppi clic di ESITO_L4 (GTFS archiviato sul Pi? copia con «ieri»? zip in data\gtfs_archivio\?). Se no, ricordaglieli alla fine, prima dei passi di L4b.
1. scripts/backup_da_leopi.py: remoto_tmp nella cartella del blocco L4b (CFG["dir_remota"] + "/data/tmp_copia"); il codice remoto crea la cartella se manca, controlla lo spazio (os.statvfs) contro 1,5 × peso di storico.sqlite PRIMA del backup SQLite e, se basta, cancella i resti come da regola. Il messaggio di errore dice quanto spazio c'è e quanto ne serve. La pulizia finale (unlink dello snapshot) resta.
2. scripts/controlla_leopi.py: la riga e la soglia di /tmp passano alla cartella nuova (ALLARME sotto 1,5 volte lo storico); /tmp resta solo come riga informativa.
3. Prove: python -m pyflakes scripts (zero); python scripts\backup_da_leopi.py --prova (i 5 casi di L4 restano OK); se la parte remota è una stringa di codice, provala in locale su un SQLite finto in una cartella temporanea (copia, controllo dello spazio con una soglia finta, pulizia dei soli resti vecchi); python scripts\controlla_leopi.py.
4. Esito sviluppo/piani/ESITO_L4b.md, memoria (sezione 7 punto 5: togli /tmp se risolto), commit, git pull --no-rebase origin prova, git push origin prova. Passo per Leo: doppio clic su scripts\RACCOLTA_GIORNALIERA.bat; nel log di backup deve comparire la cartella tmp_copia ed esito OK.
```

## L5 — PC: ritocchi alle schede 1 e 4 e testi onesti sui tempi in auto (ANALISI_CRITICA 1.2, 1.3)

Richieste di Leo (24/10): nella scheda 1 il testo esce dalla scheda; nella scheda 4 la gara deve essere sempre alla stessa ora, cambiando luogo.
Causa della scheda 1 (trovata nel codice, `assets/animazioni.js`, funzione `cerchi`): le scritte stanno DENTRO il disegno SVG, partono da x = 300 su una larghezza di 480 e la frase
«tutti e 5 i servizi a 15 minuti a piedi» (font 15) è lunga circa 280: finisce verso 580; in più `.anima svg{overflow:visible}` la lascia uscire. Nella home (versione piccola) è peggio.
Scelte di Claude (valori predefiniti): scheda 4, gara sempre **alle 8** (l'ora del numero principale); le altre ore restano nella linea «ora per ora». Scheda 3: la gara con le 4 ore resta com'è (Leo non l'ha chiesta).

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, la memoria, il blocco L5 di sviluppo/piani/PROMPT_LAVORI.md e sviluppo/piani/ANALISI_CRITICA.md paragrafi 1.2 e 1.3.
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py. Niente controlli grafici: li fa Leo. Un passo per volta.
1. SCHEDA 1 (assets/animazioni.js, cerchi). Nel disegno SVG restano solo i cerchi e la casa; le tre righe (numero % e testo) diventano HTML accanto al disegno: un contenitore flex che va a capo sotto il disegno quando la scheda è stretta (flex-wrap; disegno al massimo 260 px di larghezza, testo con overflow-wrap). Numeri che salgono e righe che compaiono in sincronia coi cerchi come oggi (stessi tempi). Versione piccola (home, compatto): solo i cerchi e, accanto, «5′ 68%», «10′ 97%», «15′ 99%» su tre righe brevi, senza la frase lunga. «Riduci movimento»: tutto fermo e scritto.
   Poi CONTROLLA TUTTE le altre animazioni e la gara per lo stesso difetto, nel codice: ogni <text> dentro un SVG deve avere spazio per il testo più lungo che i dati possono dare (stima: caratteri × 0,6 × dimensione del font, contro lo spazio fino al bordo del viewBox). Elenca nell'esito ogni testo controllato con la stima. Dove non c'è spazio: testo in HTML, oppure abbreviato dallo script delle schede. Togli overflow:visible da .anima svg se non serve più (se serve a qualcosa, dillo nell'esito).
2. SCHEDA 4 (scripts/schede/r8.py intorno alle righe 260-280, gara dei 6 viaggi tipici): i luoghi NON hanno più «ore»: solo le 8, e la gara gira da un viaggio all'altro. Titolo e nota della gara: «alle 8 di un feriale», via la frase «Poi gli stessi viaggi alle 13, alle 17:30 e alle 21». La linea «ora per ora» resta. La gara della scheda 3 non cambia.
3. TESTI ONESTI (ANALISI_CRITICA 1.2 e 1.3), in scripts/schede/r8.py, r6.py, docs/R8_traffico.md, docs/R6_parcheggi.md:
   - la «forbice» non è un minimo e un massimo (il 2,1 di Google è una mediana: Google è fuori in 5 percorsi su 8): «limite basso / limite alto» → «stima con il rallentamento di Google / stima con il rallentamento dei sensori» (nelle schede, nei criteri, nei grafici a gruppi, nelle note); dove si dice «sta fra» / «stimati fra» → «due stime; il valore vero può stare anche fuori»; docs/R8_traffico.md:62-64 e la frase «La verità sta nella forbice» riscritti allo stesso modo;
   - via «decise prima di vedere i numeri» / «fissate prima dei numeri» dalla scheda 4 (r8.py righe 303 e 320) e da docs/R8_traffico.md:85; nel documento R8 una riga: «Il metodo è cambiato 4 volte il 21/10 dopo le prime prove; le fasce sono state scelte dopo.»;
   - nelle schede 3 e 4 un limite: «Il rallentamento di Google è stato misurato su 6 percorsi in uscita dal centro; in entrata l'auto può essere più lenta.» (vale finché non c'è L6);
   - i nomi interni dei campi JSON (limite_basso, limite_alto) NON si cambiano: cambiano solo i testi.
   Traduzioni in scripts/schede/testi.json per ogni frase nuova.
4. Prove: python -m pyflakes scripts (zero); node --check assets\*.js; python scripts\schede_risultati.py (nessuna ATTENZIONE); git grep -n "limite basso\|limite alto\|decise prima\|fissate prima\|sta fra" su scripts/schede e docs: nessun testo rimasto (i nomi dei campi JSON sì); scripts\RIFAI_MAPPA_E_SCHEDE.bat; python scripts\prova_pagine.py (0 errori).
5. Esito sviluppo/piani/ESITO_L5.md (con l'elenco dei testi SVG controllati), memoria (sezione 7: togli i punti 2 e 3 dei problemi gravi se risolti), commit, git pull --no-rebase origin prova, git push origin prova.
Da guardare per Leo: scheda 1 su computer e telefono (testo dentro la scheda, anche nella home); scheda 4 (gara alle 8 che cambia viaggio); testi delle schede 3 e 4 («due stime»).
```

## L6 — PC: tempi in auto con traffico da un servizio di percorsi (ANALISI_CRITICA 1.1 e 1.14) 🛑

Perché: il fattore di Google (2,1) viene da 6 percorsi **in uscita** dal centro, presi a mano; l'unico in entrata dà 3,6 e con quello cambia il messaggio della scheda 3 (12 punti su 12 «il bus conviene»).
Alle altre ore (L3) il fattore di Google è solo quello dei sensori riscalato. Leo (24/10): meglio che i tempi li raccolga l'agente invece che a mano.
**Scelta proposta da Claude: TomTom Routing API** (piano gratuito senza carta di credito, oggi circa 2.500 richieste al giorno: da verificare al momento dell'iscrizione). Per ogni percorso e ora di partenza
(`departAt` in un giorno futuro) dà il tempo previsto col traffico tipico (`travelTimeInSeconds`) e quello senza traffico (`noTrafficTravelTimeInSeconds`): il rapporto è un fattore di punta misurato, per direzione e per ora.
Alternative: HERE Routing (simile, condizioni da verificare); Google Routes API (la stessa fonte del 2,1, ma serve un conto con carta di credito). Raccogliere da Google Maps con programmi automatici è vietato dalle sue condizioni: non si fa.
**Prima del giro (Leo):** crea l'account e la chiave, legge le condizioni d'uso (in particolare se si possono salvare i tempi e pubblicare valori ricavati) e scrive la chiave in config_locale.json (`"tomtom_chiave"`, fuori da git).
Se le condizioni vietano di salvare i tempi: si salvano solo i fattori aggregati (mediane e quartili per gruppo e ora), mai le risposte.

**Regole fissate ora, prima di vedere i numeri:**
- percorsi: (A) i 12 punti prioritari e i 5 interscambi → Piazza Castello (in entrata) e il ritorno (in uscita); (B) gli 8 percorsi di controllo del 93 (i 6 da Castello verso la cintura, Racconigi → Castello, il controllo della Fase 5), nei due sensi; (C) le 100 coppie di zone con più auto del mattino (`ore_del_giorno.json`), nel senso del viaggio. Stessi punti di partenza e arrivo degli script 93 e 94.
- partenze: martedì 10/11/2026 e mercoledì 11/11/2026 (settimana senza feste), alle 8:00, 13:00, 17:30, 21:00 ora italiana; per ogni percorso e ora la media dei due giorni. Circa (34 + 16 + 100) × 4 × 2 = 1.200 richieste: un giorno di piano gratuito; pausa fra le richieste come chiede il servizio.
- fattore di un percorso = tempo col traffico / tempo senza traffico. Per gruppo (entrata, uscita, coppie) e ora: mediana, 25° e 75° percentile.
- uso nei risultati: la stima «con il rallentamento di Google» diventa la stima «con il rallentamento del servizio di percorsi», con il fattore mediano della direzione giusta (entrata per i punti del R6, coppie per il R8) e dell'ora giusta (sostituisce la formula riscalata di L3). La stima dei sensori 5T resta com'è. Le classi del R6 (≤ 1,5) e la regola del titolo della scheda 4 (±0,3) NON cambiano.
- controllo: sui 6 percorsi in uscita alle 8 il fattore del servizio si confronta col 2,1 di Google: se la mediana differisce di più di 0,5, AVVISO e ci si ferma prima di cambiare le schede (decide Leo). Facoltativo, Leo a mano: i tempi Google in entrata alle 8 su 6 dei 12 punti, come secondo controllo.

```
Sei sul PC di Leo, cartella C:\projects\Progetti\GTT, ramo prova. Leggi sviluppo/AGENTS.md, la memoria, docs/R6_parcheggi.md, docs/R8_traffico.md, sviluppo/piani/ANALISI_CRITICA.md (1.1, 1.2, 1.14), sviluppo/piani/ESITO_L3.md, sviluppo/piani/ESITO_L5.md e il blocco L6 di sviluppo/piani/PROMPT_LAVORI.md (regole: non cambiarle dopo aver visto i numeri).
Prima: git pull --no-rebase origin prova e python scripts\controlla_rami.py. Se config_locale.json non ha "tomtom_chiave", fermati e chiedila a Leo. Niente controlli grafici. Un passo per volta.
1. Script nuovo scripts/101_tempi_traffico.py (101 è il prossimo numero libero: controllalo nella memoria e aggiornalo). Legge i punti di partenza e arrivo dagli stessi file di 93, 94 e 100 (non copiarne le coordinate a mano). Chiama il servizio (libreria standard: urllib), con pausa fra le richieste, ripresa se si interrompe (parziale salvato), nessuna chiave stampata né scritta nei log o nei file. Risposte grezze solo in data\tempi_traffico_grezzi\ (fuori da git: git check-ignore) e solo se le condizioni lo permettono (Leo lo scrive in cima al prompt: SALVA_GREZZI = sì/no).
   Uscite in git: data/processed/tempi_traffico.json (per gruppo e ora: mediana, 25° e 75° percentile del fattore, numero di percorsi; per i percorsi B anche i minuti, da confrontare con Google) e docs/rapporti/RAPPORTO_TEMPI_TRAFFICO.txt. Opzioni: --prova (risposte finte, nessuna chiamata), --solo-controllo (solo i percorsi B: circa 64 richieste).
   Controlli: tutte le risposte con tempo > 0 (bloccante); fattore fra 1 e 5 (AVVISO fuori); il controllo dei 6 percorsi in uscita contro il 2,1 del blocco L6 (AVVISO e STOP oltre 0,5).
2. Lancia prima --prova, poi --solo-controllo e scrivi la tabella dei percorsi B (servizio contro Google contro i nostri sensori) a Leo. Se scatta lo STOP, fermati qui e aspetta Leo.
3. Lancio intero. Poi gli script 93, 94 e 100 leggono il fattore del servizio (se tempi_traffico.json c'è) al posto del 2,1 e della formula riscalata, per direzione e ora come nel blocco L6; se il file manca restano come oggi. Il 93 per le coppie usa il fattore del gruppo coppie; il 94 e il 100 per i punti del R6 quello in entrata.
4. Rilancio: python scripts\rifai_tutto.py --da r8 (o i comandi equivalenti: 93, 94, 100, schede, mappa). Tabella prima/dopo: classi dei 12 punti e dei 5 interscambi, minuti di pareggio, rapporto mediano del R8 a ogni ora, titolo della scheda 4 (regola ±0,3). docs/R6_parcheggi.md e docs/R8_traffico.md aggiornati (fonte nuova, regole, limiti: tempi previsti dal servizio su traffico tipico, non misurati; un solo servizio).
5. Testi delle schede 3 e 4: «stima con il rallentamento del servizio di percorsi (TomTom)» e il limite di L5 sull'uscita dal centro tolto. Attribuzione della fonte come chiedono le condizioni d'uso (nelle schede e in docs/FONTI_DATI.md). Traduzioni in testi.json.
6. Prove: pyflakes zero; python scripts\schede_risultati.py (nessuna ATTENZIONE); scripts\RIFAI_MAPPA_E_SCHEDE.bat; python scripts\prova_pagine.py (0 errori); git grep della chiave: zero risultati.
7. Esito sviluppo/piani/ESITO_L6.md (tabelle dei passi 2 e 4), memoria (sezione 7: punti 1 dei problemi gravi e la critica a L3), commit, git pull --no-rebase origin prova, git push origin prova. Di' a Leo in 5 righe se il messaggio della scheda 3 è cambiato e perché.
```
