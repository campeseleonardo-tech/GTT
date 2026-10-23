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
| P1 | PC | `config_locale.json`, rilancio mappa e schede, prova delle pagine | 1 (5) |
| C2 (FATTO 22/10) | CLOUD | inventario dei dati (script 96) e licenze delle fonti | 2 (1, 2) |
| P2 (FATTO 22/10) | PC | lancio dello script 96 🛑 Leo e Claude decidono dove va ogni dato | 2 (1, 3) |
| C3 (FATTO 22/10) | CLOUD | riassunti dello storico + ora tipica (97), `.gitignore`, Release (98), `scarica_dati.py` | 2 (4-7) |
| P3 | PC | lancio 97 e 98, caricamento della Release, commit dei dati | 2 (4-6) |
| C4 (FATTO 22/10, aspetta la scelta di Leo) | CLOUD | 3 prove di stile 🛑 Leo sceglie | 4 (1) |
| C5 (FATTO 22/10) | CLOUD | stile comune, barra, piè di pagina, anteprima dei link; numeri che contano, omini e quadratini; grafico della metro (scheda 5) | 4 (2, 3), 3 (3) |
| C6 (FATTO 22/10) | CLOUD | divisione di `schede_risultati.py` e testi IT/EN | 5 (4), 4 (5) |
| P4 (FATTO 22/10) | PC | rilancio schede: stessi numeri di prima; Leo rilegge l'inglese 🛑 | 5 (4) |
| C7 (FATTO 22/10) | CLOUD | gara bus contro auto (scheda 3) | 4 (4) |
| C8 (FATTO 22/10, unito in prova il 23/10) | CLOUD | home: mezzi in movimento, contatore, miniature | 4 (6) |
| C9 (FATTO 22/10, unito in prova il 23/10) | CLOUD | mappa: ore che scorrono, caricamento, telefono, schede dei temi, link della vista | 4 (7) |
| C14 | CLOUD | revisione di Leo (23/10): home, numeri che salgono, schede con meno parti chiuse, titoli nuovi, animazioni delle 5 schede anche in home | 4 (revisione 23/10) |
| P5 | PC | prima `97 --solo ora --rifai` (ESITO_C8), poi rilancio mappa e schede, controllo a occhio di home, schede e mappa 🛑 → main | — |
| C15 | CLOUD | script 99: tempi coi mezzi e in auto a più ore del giorno (punti del R6, coppie di zone del R8); gara e scheda 4 con le ore | 4 (revisione 23/10) |
| P10 | PC | calcolo dello script 99 (lungo), rilancio schede 🛑 | — |
| C10 | CLOUD | area che si espande: script dei tempi e grafico (scheda 4) | 4 (8) |
| P6 | PC | calcolo dei tempi da Piazza Castello, rilancio schede | 4 (8) |
| C11 | CLOUD | `progetto.html` | 4 (9) |
| C12 | CLOUD | 404, pagine dei singoli risultati, README, controllo automatico su GitHub, `rifai_tutto.py` | 4 (10), 1 (9), 5 (2, 3) |
| P7 | PC | prova «da zero» e rilancio completo 🛑 → main; Leo accende GitHub Pages e scrive la descrizione del repository | 1 (8, 10), 5 (3) |
| C13 | CLOUD | pulizia del codice (funzioni comuni, codice morto, prove dei numeri), a pezzi | 5 (5-8) |
| P8 | PC | metà novembre: R4 con un mese di dati, rilancio | 3 (4) |

---

## Regole comuni (sono già dentro ogni prompt: non serve copiarle)

Ogni prompt dice al modello di: leggere `sviluppo/AGENTS.md` e la memoria; controllare i rami prima di iniziare; seguire il piano; provare davvero
(script lanciati, pagine aperte nel browser); scrivere un esito `ESITO_<giro>.md` accanto ai piani; aggiornare la memoria; fare commit e push.
I numeri dei risultati non si scrivono mai a mano: si leggono dai file prodotti dagli script.
**Controlli grafici (Leo, 23/10): li fa solo Leo.** Il modello controlla che il codice giri (script, 0 errori JavaScript con `prova_pagine.py`,
numeri nei JSON) e scrive a Leo una lista di cosa guardare; non guarda e non giudica schermate, colori o misure. Questo vale anche per i prompt
più sotto scritti prima del 23/10 che parlano di screenshot «da guardare».

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

## C14 — CLOUD: revisione di Leo del 23/10 (home, numeri, schede, animazioni)

Prima di lanciarlo: C8 e C9 devono essere in `prova` (lo sono dal 23/10, unione nel ramo `claude/vigilant-volta-l13do5`).
Cosa vuole Leo e perché: `PIANO_GRAFICA.md`, sezione «Revisione di Leo (23/10)». Esiste una **bozza di codice** scritta da Claude, `sviluppo/piani/C14_bozza.patch`
(si applica pulita su `prova` del 23/10; **non provata a occhio**, solo «0 errori» della prova delle pagine). Il giro serve a portarla a termine, non a riscriverla.

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md e sviluppo/piani/PIANO_GRAFICA.md (sezione «Revisione di Leo (23/10)»). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py; fermati se ci sono rami con lavoro non unito.
REGOLA DI LEO: niente controlli grafici (niente schermate da guardare, niente giudizi su colori o misure): li fa Leo. Tu controlli solo che il codice giri: script senza errori, prova delle pagine con 0 errori JavaScript, numeri giusti nei JSON.

0. git apply sviluppo/piani/C14_bozza.patch. Se non si applica, fermati e dillo a Leo (vuol dire che i file sono cambiati dopo il 23/10). Leggi TUTTO il diff prima di andare avanti: sotto c'è l'elenco di cosa fa e di cosa manca.

1. NUMERI CHE SALGONO (assets/sito.js, funzione contaSu). Controlla nel codice che: durano circa 2,6 secondi con partenza e arrivo morbidi; durante la corsa scrivono solo interi (Math.floor), senza virgola né %; il testo finale (con decimali e %) torna solo alla fine; la larghezza dell'elemento è fissata a quella del testo finale (min-width) prima di partire; data-forbice="21,28" fa salire due numeri insieme («21–28»). Cerca con git grep "data-suffisso" e togli ogni uso rimasto (non serve più).

2. HOME (index.html, assets/mezzi.js, assets/stile.css, scripts/schede/home.py).
   a. «Torino Mobilità» in oro (#e3bf55, lo stesso oro della barra), sottotitolo «Un progetto per capire come si muove la città.» con l'inglese in data-en.
   b. Contatore: «Da N giorni raccogliamo, minuto per minuto, i dati di bus, tram e traffico di Torino, e continuiamo: per capire chi va dove, e come ci va.» N = giorni da INIZIO_RACCOLTA (home.py, "2026-10-03") a oggi, calcolati nel browser (giorni di calendario, ora locale). Il numero sale (data-valore). Controlla che la frase inglese ci sia.
   c. I 5 riquadri mostrano l'animazione della loro scheda in piccolo (Anima.html(f.anima, {compatto: true})) al posto delle immagini. Le miniature non servono più: togli da scripts/prova_pagine.py la parte che le rifà (fai_miniature, MINIATURE, punto 4 della descrizione in testa al file) e cancella la cartella assets/miniature/ (prima git grep "miniature" per trovare chi la cita, anche nei documenti e nei piani; aggiorna i rimandi).
   d. Il riquadro è un link <a>: dentro non ci devono essere pulsanti né tendine. La gara in versione mini (opzione mini di assets/gara.js) non disegna i comandi: controllalo nel codice.

3. SCHEDE: STRUTTURA (risultati.html).
   Ordine dentro la scheda aperta: domanda → numero grande (sale) → animazione (f.anima; se manca, la figura vecchia f.unita) → 3 punti chiave → grafico principale → «Vedi sulla mappa» → «Altri grafici» APERTI (sottotitolo, non <details>) → la parte f.extra aperta, se c'è → UNA sola parte chiusa «Come l'abbiamo calcolato e limiti» (calcolo, confronto, criteri, poi «Limiti»).
   Via la parte «In English» dalla pagina e la chiave «english» dalle schede (scripts/schede/comune.py: forma_base non la salva più, controlla_forma non la conta più; l'argomento resta per non toccare tutte le chiamate). L'inglese resta col bottone IT/EN.
   Controlla con git grep "english" che non resti altro da togliere (traduci.py la salta già).

4. SCHEDE: TITOLI E TESTI (scripts/schede/r1.py, r4.py, r6.py, r10.py). I titoli sono quelli della tabella in PIANO_GRAFICA.md. Attenzione:
   - i numeri nei titoli e nei testi si calcolano dai dati, mai scritti a mano (es. «2 su 3» della scheda 3 viene da frazione(n_senza / n_fermate); «Circa il 5%» da round del ritardo oltre 10 minuti);
   - scheda 5: il 9,5% è la quota dei residenti delle «zone abitate» (sezioni fuori dalle zone quasi disabitate), NON di tutti i torinesi (79.598 / 848.748 = 9,4%): il testo deve dire «dei residenti delle zone abitate»;
   - scheda 3 riorganizzata (Leo: il risultato è quanto è facile lasciare l'auto, i minuti di parcheggio sono una postilla): numero grande = fermate importanti senza posti bastanti (179 su 274); grafico principale = i 12 punti per bisogno; altri grafici = gara (gira da sola), minuti di pareggio, parcheggi di scambio esistenti con lo stato (pieno, a metà, libero, non misurato); punti chiave = nessun parcheggio / pochi posti, il primo punto d'ingresso, il pareggio;
   - in r6.py alcune righe sono IDENTICHE in scheda_r6() e in forma_r6() (es. «val = rie.get(...)»): se cambi qualcosa a mano, cercala dentro la funzione giusta, non con la prima occorrenza del file.

5. ANIMAZIONI (assets/animazioni.js nuovo, assets/gara.js). Un componente unico usato da home e schede; ogni scheda porta in f.anima la sua descrizione, scritta dai moduli Python con i numeri dei dati:
   - scheda 1 «cerchi»: tre cerchi intorno a una casa, 5 → 10 → 15 minuti; ognuno si apre col suo % (dati: risultato1_vuoti.json, soglie 5/10/15, quota con tutti e 5 i servizi);
   - scheda 2 «quadratini»: 100 quadratini, si accendono uno alla volta quelli oltre 5 minuti, poi diventano scuri quelli oltre 10; poi il giorno che scorre: le 4 fasce orarie feriali (punta del mattino, giorno, punta della sera, sera) con il loro numero oltre 5 minuti (dati: fasce di risultato4_regolarita.json, le stesse del grafico a linea), poi di nuovo tutto il giorno, in giro;
   - scheda 3 «fermate»: forma di Torino (assets/torino_contorno.json, stessa proiezione della home: x = (lon − lon_min)·k·scala, y = (lat_max − lat)·scala) e le 274 fermate importanti di mappa_r6.json che compaiono dal centro verso fuori, colorate per classe (posti bastanti / pochi / nessuno), con i conteggi della legenda che salgono; poi i cerchi sui 12 punti prioritari. Molte fermate sono FUORI dal confine di Torino (cintura): il riquadro del disegno (vb) si calcola su fermate + contorno, non sul solo contorno;
   - scheda 4 «gara» su viaggi tipici: le 6 coppie di zone con più auto del mattino, una per zona di partenza (tp_contro_auto.json, gruppi a e b; nomi delle zone da per_zona e peggiori, senza «Torino, »); arrivo = zona di arrivo (campo «arrivo» nuovo nella gara);
   - scheda 5 «omini»: 10 omini che compaiono uno alla volta, poi quelli «colorati» si accendono.
   Gara (assets/gara.js): opzione giro (finita una corsa, dopo 2,2 secondi parte quella del luogo dopo; solo mentre si vede; scegliere dalla tendina ferma il giro), nome della partenza scritto sopra la corsa, opzione mini (niente comandi, per la home). Nella mappa la gara piccola del pannello R6 deve restare come prima (compatto SENZA mini): controllalo in scripts/mappa_template.html (r6Gara).
   Tutte le animazioni: con «riduci movimento» la figura finale ferma con i numeri scritti; partono quando entrano nella finestra (IntersectionObserver); nessun errore se un dato manca (la scheda si vede senza animazione).

6. INGLESE. Ogni frase nuova deve avere la traduzione in scripts/schede/testi.json («esatte» o «modelli» con {n0}, {s0}, {t0}). In scripts/schede/traduci.py la chiave «contorno» è in SALTA (è un disegno, non un testo). Lancia python scripts/schede_risultati.py: NESSUNA riga «ATTENZIONE» (né traduzioni mancanti né frasi oltre 20 parole: attenzione che la regola che divide le frasi non taglia dopo una cifra, «alle 8. L'auto» resta una frase sola).

7. PROVE (solo funzionamento):
   - python -m pyflakes sui file Python toccati: nessun avviso NUOVO (quelli che c'erano prima restano: confronta con git stash);
   - node --check su assets/*.js;
   - python scripts/schede_risultati.py: 5 schede, nessuna ATTENZIONE; controlla nei JSON che ogni forma abbia anima e che i numeri dell'animazione coincidano con quelli dei rapporti (es. scheda 3: 95 + 111 + 68 = 274; scheda 1: 68,3 / 96,8 / 99,2);
   - python scripts/prova_pagine.py (Chromium in /opt/pw-browsers/chromium): 0 errori su tutte le pagine. Non guardare le schermate: le guarda Leo.
8. Cancella sviluppo/piani/C14_bozza.patch. Esito in sviluppo/piani/ESITO_C14.md: cosa hai cambiato rispetto alla bozza e perché, e la LISTA PER LEO di cosa guardare (sotto, giro P5). Memoria; commit e push sul ramo della sessione.
```

Cosa NON fa la bozza (lo fa il giro, punto per punto sopra): togliere le miniature da `prova_pagine.py` e `assets/miniature/`; i rimandi nei documenti; il controllo della gara nella mappa.
Limiti noti da dire a Leo: la scheda 4 resta «al mattino» finché non c'è C15; i tempi a più ore della gara della scheda 3 arrivano con C15.

## P5 — PC: rilancio, poi Leo guarda 🛑 → main

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, ESITO_C8, ESITO_C9 e ESITO_C14. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
REGOLA DI LEO: i controlli grafici li fa Leo; tu fai girare gli script e prepari la pagina.
1. python scripts\97_riassunti_storico.py --solo ora --rifai (ora tipica della home sul giorno con più GPS: l'AVVISO «il GPS copre solo 21 minuti» deve sparire o dire quanti minuti copre il giorno migliore).
2. scripts\RIFAI_MAPPA_E_SCHEDE.bat, poi python scripts\prova_pagine.py: 0 errori. Peso di mappa_torino.html non oltre 6,2 MB.
3. Avvia python -m http.server 8765 nella cartella e dai a Leo questa lista da guardare (computer e telefono, chiaro e scuro):
   home: titolo in oro, frase dei giorni, mezzi in movimento, 5 riquadri con la loro animazione; numeri che salgono piano, senza virgola né % durante la corsa;
   schede: nessun «In English»; una sola parte chiusa; animazioni delle 5 schede (cerchi, quadratini col giorno, fermate su Torino, gara che gira da sola, omini); titoli nuovi;
   mappa: ▶ delle ore, caricamento, pannello sul telefono, copia link, gara piccola nel pannello dei parcheggi.
   Scrivi le sue osservazioni, parola per parola, in sviluppo/piani/ESITO_P5.md.
4. Commit e push su prova. Solo se Leo dice che va bene: git checkout main, git pull origin main, git merge --no-edit prova, git push origin main, git checkout prova; python scripts\controlla_rami.py: main uguale a prova.
```

## C15 — CLOUD: il giorno intero, non solo l'ora di punta (schede 3 e 4)

Richiesta di Leo (23/10): i confronti bus/auto non solo alle 8. Oggi i tempi coi mezzi esistono solo alle 7:45-8:15 (script 93 per le coppie di zone, 94 per i punti del R6).
Scelte di Claude (valori predefiniti, Leo può cambiarle prima del lancio):
- **4 ore**, le stesse fasce della scheda 2: 8:00 punta del mattino (c'è già), 13:00 giorno, 17:30 punta della sera, 21:00 sera. Feriale 2026-10-12, finestra di 30 minuti, mediana (come 93/94).
- **Auto a un'ora h** = tempo a flusso libero × fattore(h) + 5 minuti di parcheggio. fattore(h) dai sensori 5T (`data/processed/velocita_5t.json`, feriali): mediana sui sensori urbani di velocità di notte (3-5) / velocità all'ora h; deve valere 1,2 (± 0,1) alle 8 come oggi, altrimenti AVVISO e ci si ferma. Il fattore di Google (2,1) c'è solo alle 8: alle altre ore si scala nello stesso rapporto, fattore_basso(h) = 1 + (2,1 − 1) × (fattore(h) − 1) / (fattore(8) − 1). È un'ipotesi: va scritta nei limiti.
- **Regola fissata prima dei numeri** per il titolo della scheda 4: se il rapporto mediano delle 4 ore resta dentro ±0,3 da quello delle 8 con tutti e due i fattori → titolo «A ogni ora del giorno, coi mezzi pubblici si impiega da X a Y volte il tempo dell'auto»; altrimenti il titolo resta «Al mattino…» e un punto chiave dice da quanto a quanto cambia nel giorno. Scheda 3: il titolo resta sui parcheggi (Leo).

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, docs/R6_parcheggi.md, docs/R8_traffico.md, sviluppo/piani/PIANO_GRAFICA.md (revisione 23/10, «Non solo all'ora di punta») e il blocco C15 di sviluppo/piani/PROMPT_LAVORI.md (scelte e regola del titolo). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
REGOLA DI LEO: niente controlli grafici, li fa Leo.
1. Leggi gli script 93 e 94 e capisci come calcolano i tempi coi mezzi (r5py) e in auto. NON copiarne il codice: riusa le funzioni con comuni.carica_script come fa il 94.
2. Scrivi scripts/99_ore_del_giorno.py (99 è il prossimo numero libero: controllalo nella memoria). Sola lettura sui dati. Per le 4 ore (costante ORE in testa): tempi coi mezzi dai 12 punti prioritari e dai 5 interscambi a Piazza Castello (come il 94) e per le coppie di zone del 93 (gruppi a e b; se il calcolo di tutte le coppie a 4 ore è troppo lungo, le 600 coppie con più auto, e scrivilo nel rapporto). Auto con fattore(h) e fattore_basso(h) come nel blocco C15. Uscite: data/processed/ore_del_giorno.json (per ora: luoghi R6 con tp, auto_alto, auto_basso; coppie con tp, auto, auto_basso; rapporto mediano pesato per le auto del mattino, con tutti e due i fattori) e docs/rapporti/RAPPORTO_ORE_DEL_GIORNO.txt.
   Opzioni: --prova (dati finti piccoli, cartella temporanea) e --campione N (solo N zone, per la prova sul PC). Controlli: fattore alle 8 = quello di oggi (bloccante oltre ±0,1); alle 8 i tempi coi mezzi uguali a quelli di r6_bus_contro_auto.json e tp_contro_auto.json entro 1 minuto (AVVISO); nessun tempo nullo, negativo o infinito (bloccante); sera senza collegamento entro 120 minuti = conta a parte, non errore.
3. Schede (scripts/schede/r6.py e r8.py), solo se ore_del_giorno.json c'è (se manca, le schede restano come dopo C14):
   - gara della scheda 3: ogni luogo corre alle 4 ore una dopo l'altra (orologio scritto sopra la corsa: «8:00», «13:00», …), poi il luogo dopo; in home (mini) solo le 8;
   - gara della scheda 4: stessa cosa per i 6 viaggi tipici;
   - scheda 4: grafico a linea nuovo «Quante volte il tempo dell'auto, ora per ora» (due serie: fattore alto e basso) in «Altri grafici»; titolo secondo la regola del blocco C15 (fissata prima dei numeri: non cambiarla dopo averli visti);
   - assets/gara.js: campo facoltativo «ora» per ogni corsa, scritto nel disegno e nella frase per il lettore di schermo; italiano e inglese; traduzioni nuove in testi.json.
4. Limiti nuovi nelle schede 3 e 4: «Il rallentamento dell'auto alle altre ore viene dai sensori; quello di Google si conosce solo alle 8 ed è stato scalato.»
5. Prove nel cloud: --prova; python scripts/schede_risultati.py con un ore_del_giorno.json finto nello stesso formato (nessuna ATTENZIONE); prova_pagine.py 0 errori. Esito in sviluppo/piani/ESITO_C15.md con i comandi esatti per il PC (giro P10) e la durata stimata; memoria (prossimo numero libero 100); commit e push.
```

## P10 — PC: calcolo delle ore del giorno 🛑

```
Sei sul PC di Leo (C:\projects\Progetti\GTT, ramo prova). Leggi sviluppo/AGENTS.md, la memoria e sviluppo/piani/ESITO_C15.md. Prima: git pull --no-rebase origin prova, python scripts\controlla_rami.py.
1. python scripts\99_ore_del_giorno.py --campione 10: controlli OK, durata. Stima la durata del calcolo intero e dilla a Leo; se supera 2 ore, prepara un .bat (cd /d "%~dp0..", log in logs\, stop al primo errore) che Leo lancia con doppio clic.
2. Calcolo intero. Controlla che i numeri abbiano senso: alle 8 uguali a oggi (rapporti 93 e 94); di sera e a mezzogiorno l'auto più veloce che alle 8; i mezzi di sera più lenti o uguali. Scrivi una tabella ora per ora (rapporto mediano, auto oltre 2 volte) nell'esito.
3. scripts\RIFAI_MAPPA_E_SCHEDE.bat e python scripts\prova_pagine.py: 0 errori. Scrivi a Leo quale titolo è uscito per la scheda 4 e perché (regola del blocco C15).
4. Esito in fondo a ESITO_C15.md, memoria, commit e push su prova. Leo guarda le schede 3 e 4.
```

## C10 — CLOUD: area che si espande

```
Sessione cloud sul repository Turin-mobility. Leggi sviluppo/AGENTS.md, sviluppo/MEMORIA_PROGETTO.md, docs/R8_traffico.md e sviluppo/piani/PIANO_GRAFICA.md (elemento E, passo 8). Prima: git fetch --unshallow origin (se serve), python scripts/controlla_rami.py.
1. Controlla nello script 93 se data/processed/tp_contro_auto.json contiene i tempi coi mezzi e in auto per TUTTE le coppie di zone (campo «coppie»), o solo quelle con viaggi in auto. Se non tutte, modifica il 93 perché salvi anche la tabella completa zona × zona (tempi coi mezzi, auto con i due fattori) senza cambiare nient'altro del risultato.
2. Scrivi lo script nuovo (prossimo numero libero dalla memoria) che calcola, da Piazza Castello, il tempo coi mezzi (r5py come lo script 18: 2026-10-12, partenza 7:45, finestra 30 minuti, mediana) e in auto (rete del modello del traffico come lo script 93, flusso libero × i due fattori + 5 minuti di parcheggio) verso il centro di ogni sezione di censimento abitata; uscita compatta in data/processed/area_tempi.json (tempi in minuti interi). Opzione --prova con 200 sezioni.
3. Nella scheda 4 un grafico «area che si espande»: mappa semplice (sezioni come quadratini o forme semplificate, sfondo dello stile) con due colonne «coi mezzi» e «in auto»; un cursore e un ▶ fanno crescere le aree minuto per minuto fino a 60 minuti, con le soglie 10, 20, 30, 45 scritte e la percentuale di torinesi raggiunti a ogni soglia. Tendina della partenza: «Piazza Castello» (dettaglio per sezione) e tutte le zone di Torino dalla tabella zona × zona (dettaglio per zona). Dati portati nella scheda dallo script delle schede, peso aggiuntivo sotto 400 KB. Con «riduci movimento»: le 4 soglie affiancate e ferme.
Nota (23/10): l'area è solo alle 8; le altre ore di C15 si aggiungono solo se Leo lo chiede dopo P10 (il calcolo per sezione a 4 ore è lungo).
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
