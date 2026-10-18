# Piano finale — Risultato 6 v2 (parcheggi di interscambio): mappa, scheda, eventi

Scritto da Claude il 19/10/2026 con Leo. Prima di questo: `PIANO_RISULTATO6.md` (storia), `PIANO_RISULTATO6_V2.md` e
`PIANO_RISULTATO6_V2_GIRO2.md` (giri dell'agente), `ESITO_RISULTATO6_V2_GIRO2.md` (numeri). Memoria: riga "Risultato 6 v2"
in `MEMORIA_PROGETTO.md`. Regole di lavoro e per gli agenti: quelle dei piani precedenti (ramo `prova`, nessun commit
dell'agente, database in sola lettura, esito in un file `docs/ESITO_*.md`, Claude ricontrolla prima di dire a Leo).

## Decisioni di Leo (19/10) — fisse

- Parcheggi in "zona centrale" = Q001-Q009 (fiducia in Claude). 23 luoghi senza zona IMQ: restano fuori, elencati nel rapporto.
- 25 m² a posto per i posti stimati: **confermato** (mediana 25,4 m² su 152 parcheggi OSM con posti dichiarati; la
  fascia va da 17 a 33 m²: lo dichiariamo come incertezza ±30%).
- Si fa il **punto in mappa** per vedere di cosa si parla.
- **Eventi** (stadi, palasport, fiere: migliaia di auto in un'ora): entrano come "luoghi speciali" (Fase B).
- Il resto del giro 2 va bene com'è.

## Fase A — Scelta dello scenario (Leo, 5 minuti)

Claude spiega S1/S2/S3 in parole semplici; Leo sceglie. Poi Claude scrive la scelta qui sotto e in `PIANO_RISULTATO6_V2_GIRO2.md` (G9.0).
**SCENARIO SCELTO: S2 "integrato"** (Leo, 19/10): a1, a2, b2, c1, c2_ztl, d, e — 378 luoghi critici, 140 coperti da parcheggi di fatto/potenziali a 200 m.
Il valore su cui si basa tutto il resto (mappa e scheda): lo scenario scelto con copertura **F** (parcheggi "potenziali" + "di fatto") a 200 m.

## Fase B — Eventi e luoghi speciali (nuovo; dopo la Fase A, prima della mappa)

Domanda: dove vanno migliaia di auto in poche ore (partite, concerti, fiere) e c'è posto/TP vicino?

B1. **Claude** (con ricerca sul web, fonti scritte) compila `data/ref/eventi_luoghi.json` a mano: Allianz Stadium, Stadio Olimpico
    Grande Torino, Inalpi Arena, Palasport Olimpico, Lingotto Fiere/Oval, più quelli che Leo vuole aggiungere. Per ognuno: nome, lat/lon,
    capienza **con link alla fonte**, tipo di eventi, giorni/ore tipici. Etichetta [STIMATO]. Leo controlla l'elenco prima del passo B2.
B2. **Agente** (script `78_eventi_parcheggi.py`): per ogni luogo, con le stesse distanze in linea d'aria:
    - parcheggi aperti (OSM, 5T, Comune) entro 500 m / 1 km, con posti dichiarati o stimati (25 m²) e tariffa;
    - fermate TP entro 500 m, corse all'ora la sera e nel fine settimana (GTFS 12/10, sabato e domenica);
    - parcheggi di interscambio (classe `solo_sulla_carta`/`potenziale`/ufficiali) entro 3 km con una linea TP diretta (nodo forte);
    - **stima delle auto**: capienza × quota di chi viene in auto × 1/occupanti per auto (**parametri dichiarati**, default da scrivere nel
      rapporto, es. 50% in auto e 2,5 persone per auto; Leo li conferma) → "posti che mancano" = auto stimate − posti vicini.
    Output `data/processed/risultato6_v2/eventi.json` e `docs/RAPPORTO_R6V2_EVENTI.txt`. Non entrano nei punteggi dei luoghi critici.
B3. Controlli Claude: ricalcolo a mano per 2 luoghi; i numeri sono ordini di grandezza, non previsioni.

## Fase C — Mappa (`mappa_torino.html`)

Nuovo **tema** "Parcheggi di interscambio" (id `interscambio`), come gli altri temi (vedi lista a `mappa_template.html`, ~riga 1944).
Si modificano `scripts/04_genera_mappa.py` (carica i dati, come per `fb_candidati`) e `scripts/mappa_template.html`, poi si rigenera.
Prima di toccarli: leggi la memoria sez. 8 (standard) e come lavorano `faseb` e `catalogo`.

C1. **Dati per la mappa** (dentro `D`, piccoli): `D.r6 = {scenario, luoghi_critici:[{id,nome,lat,lon,zona,punteggio,segnali,
    coperto_f200,parcheggio_vicino,dist_m}], parcheggi:[{id,nome,tipo,classe,lat,lon,posti,posti_stimato(bool),tariffa,firma,profilo_feriale[24]}],
    eventi:[…], raggio:200}`. Solo parcheggi di classe ufficiale/solo_sulla_carta/potenziale + i garage 5T (circa 800-1.000 punti),
    non i 3.000 aperti. Tutto da file già prodotti.
C2. **Livelli** (si accendono singolarmente): luoghi critici (cerchio: colore = coperto/scoperto, dimensione = punteggio);
    parcheggi (forma/colore per classe, dimensione per posti; i posti stimati sono tratteggiati e "[STIMATO]");
    cerchio di 200 m attorno al parcheggio toccato/ai 5 ufficiali; luoghi speciali/eventi (stella) con raggio 500 m e 1 km;
    zona centrale Q001-Q009 come area grigia di contesto.
C3. **Tocco/passaggio del mouse**: luogo critico → nome, zona IMQ, punteggio e i segnali che l'hanno alzato, parcheggio più vicino e distanza;
    parcheggio → tipo, posti (dichiarati o stimati), tariffa, classe e perché, firma del riempimento e mini-profilo orario feriale
    (solo se c'è) con "[DATI SCARSI: 2 feriali]"; evento → capienza, parcheggi e fermate vicini, auto stimate vs posti.
C4. **Legenda e guida**: legenda del tema (stesso stile della legenda Pendolari); guida con fonti, date e tag
    [MISURATO]/[PROGRAMMATO]/[STIMATO]/[DATI SCARSI]; testo di descrizione del tema (`desc`) in italiano semplice, senza gergo.
C5. **Opzioni del tema** (poche): scenario fisso (non selezionabile, ma scritto), interruttore "conta anche i parcheggi solo sulla carta"
    (F+S), interruttore raggio 100/200/400 m. Niente interfaccia dinamica complessa (decisione del 18/10).
C6. **Verifica** (come da standard: `node --check` non basta): `preview_start` `pagine-gtt` (porta 8765), aprire il tema, esercitare
    i livelli, controllare console senza errori, legende e dati disegnati, tocco su un luogo/parcheggio/evento, schermo stretto (mobile)
    e tema scuro se esiste. Screenshot a Leo. Controllo che nessun altro tema sia cambiato (aprirne 2-3).
C7. Aggiornare `mappa_torino.html` rigenerato; **non** pubblicare (le condizioni d'uso degli sfondi Esri sono ancora aperte).

## Fase D — Scheda in `simulazione.html` (Passo G9 del giro 2, esteso)

D1. In `scripts/schede_risultati.py` aggiungere `scheda_r6_v2()` (non cancellare `scheda_r6`), usarla in `main()`. Formato e campi: docstring
    dello script; contenuto già definito al Passo G9 di `PIANO_RISULTATO6_V2_GIRO2.md`, con **in più**:
    - un blocco "Eventi": 3-4 numeri (auto stimate, posti vicini, posti che mancano) per i luoghi speciali, con la frase che sono ordini di grandezza;
    - `mappa: {tema: "interscambio", nota: "…"}` (link alla mappa: guarda come lo fanno le schede R1/R8);
    - nel testo: il risultato "**nessun parcheggio fa davvero da interscambio di fatto fuori dal centro**" spiegato in due frasi + i 4 "solo sulla carta".
D2. Rilanciare `python scripts\schede_risultati.py`; `node --check data\schede_risultati.js`; aprire `simulazione.html` col browser integrato:
    grafici visibili, link alla mappa funzionante, nessun errore in console.
D3. Aggiornare l'avviso: "dati [STIMATO] / [PROGRAMMATO]; riempimento [DATI SCARSI]".

## Fase E — Chiusura

E1. **Memoria**: aggiornare riga FATTO e sezione 6 (togliere "resta da fare"), ricordare di rifare il giro dopo il 25/10.
E2. **Commit** (Leo lo chiede). Ricordarsi i file `.bak_18ott`, `3)` (decide Leo).

## Fase F — Dopo il fetch di domenica 25/10 (≥ 5 giorni feriali)

F1. `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat`; poi `71 → 72 → 73 → 75 → 76` (~2 minuti); controllare quali firme sono cambiate (soprattutto i 7
    parcheggi "fragili") e se qualche parcheggio fuori da Q001-Q009 è diventato "di fatto".
F2. `python scripts\04_genera_mappa.py` e `python scripts\schede_risultati.py`; rifare C6 e D2; aggiornare numeri in memoria.

## Chi fa cosa

| Fase | Chi | Perché |
|---|---|---|
| A | Leo | decisione |
| B1 | Claude | ricerca web con fonti |
| B2, C1 | agente (piano meccanico, da scrivere dopo B1) | calcolo ripetitivo |
| C2-C5 | Claude o agente, verifica nel browser sempre Claude | codice della mappa delicato |
| D | Claude | piccola modifica a uno script |
| E, F | Claude con Leo | |

## Domande ancora aperte per Leo

1. Lo scenario (Fase A).
(chiuse il 19/10) Altri luoghi di eventi: per ora nessuno oltre a stadi, palasport e Lingotto. Parametri auto per evento: 50% in auto, 2,5 persone per auto, come punto di partenza. **Eventi = fase leggera, non focalizzarsi troppo.**
