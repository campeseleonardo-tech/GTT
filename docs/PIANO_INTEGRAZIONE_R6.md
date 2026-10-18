# Piano di integrazione — Risultato 6 v2 in mappa e in `simulazione.html` (+ colori verde→rosso ovunque)

Scritto da Claude il 19/10/2026 con Leo. Dati pronti e ricontrollati: `data/processed/risultato6_v2/mappa_r6.json` (script 79, scenario S2).
Numeri chiave: 378 luoghi critici su 4.425; coperti da parcheggi di fatto/potenziali a 200 m: 140 (ufficiali 11, tutti i parcheggi aperti 147);
parcheggi per classe: di fatto 0, solo sulla carta 4, potenziali 758. Eventi: Olimpico Grande Torino, Inalpi Arena, Oval (Allianz rimandato).
Riferimenti: `PIANO_RISULTATO6_FINALE.md` (fasi C e D, qui sostituite da questo piano), `ESITO_RISULTATO6_EVENTI_DATI.md`.

## Regole

- Ramo `prova`; commit solo quando Leo lo chiede. Python del PATH (3.14). Database e `data/raw` in sola lettura.
- La mappa si rigenera da `scripts/04_genera_mappa.py` + `scripts/mappa_template.html` → `mappa_torino.html`; **non** si modifica `mappa_torino.html` a mano.
- La scheda si rigenera con `python scripts\schede_risultati.py` → `data/schede_risultati.js`; `simulazione.html` la carica da sola.
- Standard del progetto: un campo nuovo in `D.sezioni[i]` va anche nella proiezione `sez`; chi cambia l'ora richiama `aggiornaLegenda()`; numeri in italiano (virgola);
  `node --check` non basta: ogni modifica si prova aprendo la pagina (`pagine-gtt`, porta 8765) ed esercitando l'interfaccia.
- Etichette dei dati sempre visibili: [MISURATO] [PROGRAMMATO] [STIMATO] [DATI SCARSI].
- Ogni fase finisce con una riga di esito in `docs/ESITO_INTEGRAZIONE_R6.md`: `FASE n: OK` / `FERMO – motivo`.

## Decisione nuova di Leo (19/10): colori

**In tutta la mappa, ogni scala con gradiente va da verde a rosso** (una sola scala, facile da capire). Vale anche per le schede.
Stato oggi (letto nel codice): le scale sono diverse per tema — `PAL_POCO_MALE`/`PAL_ALTO_MALE` (arancio→viola), `PAL_BASE` (verde acqua), `PAL_PEND` (viola),
`OMI_PAL` (giallo→arancio), `IMQ_PAL` (azzurri), `PAL_SEZ.fb`, `VEL_PAL` (arancio→viola). Quindi è una modifica trasversale, da fare **prima** del nuovo tema.

## FASE 1 — Una sola scala verde→rosso (tutta la mappa)

1. **Inventario**: cercare nel template tutte le palette e i colori calcolati a gradiente (`PAL_*`, `*_PAL`, `scalaHtml`, `scalaSoglie`, interpolazioni nel disegno dei confini,
   degli archi dei pendolari, dei punti dei sensori, delle linee). Elenco in un rapporto breve con riga del codice e tema.
2. **Scala unica**: definire in un solo punto `SCALA_VR` (5 passi, verde→giallo→rosso) e le due funzioni `verdeRosso(valore01)` (colore continuo) e `PAL_VR` (5 classi).
   Scegliere i colori con la skill `dataviz` (validatore: leggibilità, contrasto e **daltonismo rosso/verde**). Contro il daltonismo: i passi differiscono anche per luminosità
   e **ogni legenda scrive i numeri delle soglie** (già fanno così `scalaSoglie`), mai solo il colore.
3. **Direzione** (da decidere con Leo, vedi Domande): dove c'è "bene/male" chiaro il verde è bene e il rosso è male; per le quantità neutre il verde è "poco" e il rosso è "tanto".
   Ogni legenda scrive le parole agli estremi (es. «poca offerta» → «molta», «meno vulnerabile» → «più vulnerabile»).
4. Sostituire la scala in **tutti** i temi: servizio, accessibilità, dove mancano i servizi, vulnerabilità e residenti, IMQ, pendolari, bus e traffico misurati, valore immobiliare.
   Il catalogo usa colori **categorici** (un colore per gruppo): non è un gradiente, resta com'è.
5. Verifica per ogni tema (browser, `pagine-gtt`): legenda coerente con l'area colorata, valori letti col tocco, zoom alto e basso, schermo stretto; screenshot prima/dopo per Leo.
6. Stessa regola nelle schede (fase 5.3).

## FASE 2 — Dati nella mappa (`04_genera_mappa.py`)

1. Leggere `data/processed/risultato6_v2/mappa_r6.json` e metterlo in `D.r6` (come per `fb_candidati`); se manca il file, il tema non appare e il resto funziona.
   Peso: 0,5 MB in più nel `mappa_torino.html` (controllare il peso finale).
2. Convertire le coordinate in proiezione schermo all'avvio, come per `fbCandidati` (`px/py`).
3. Usare la zona centrale (`D.r6.zona_centrale.poligoni`, ordine `[lat, lon]`) come area grigia di contesto.

## FASE 3 — Nuovo tema "Parcheggi di interscambio" (`mappa_template.html`)

Nuova voce in `THEMES` (id `interscambio`), stesso modo degli altri temi (`area`, `over`, `opzioni`, `legenda`), descrizione in italiano semplice, senza gergo:
«Dove sono le fermate più importanti per chi arriva in auto, e se c'è un parcheggio vicino che potrebbe fare da interscambio».

**Livelli** (casella per ognuno, tutti accesi tranne il dettaglio):
- **Luoghi critici** (378): cerchio; colore = coperto da un parcheggio entro il raggio (verde) o scoperto (rosso) — sono le due uniche tinte, niente gradiente; dimensione = punteggio.
- **Parcheggi**: forma/colore per classe (ufficiale, solo sulla carta, potenziale, garage 5T non interscambio) con una **tavolozza categorica** distinta dal verde/rosso (per non confondersi);
  dimensione = posti (radice quadrata); contorno tratteggiato se i posti sono **stimati** (25 m²/posto, ±30%).
- **Cerchio di copertura** (100/200/400 m) attorno ai parcheggi toccati e ai 5 ufficiali.
- **Zona centrale** Q001-Q009 in grigio (contesto: qui un parcheggio non conta come interscambio).
- **Eventi** (3): simbolo a stella, anelli a 500 m e 1 km; solo nella vista del tema, spenti di default.

**Opzioni del tema** (poche): insieme dei parcheggi che coprono (potenziali+di fatto / solo ufficiali / + solo sulla carta); raggio 100/200/400 m.
Lo scenario è fisso (S2) e scritto in legenda.

**Tocco / passaggio del mouse** (stesso meccanismo `vicino(...)` del tema `faseb`, riga ~1547):
- luogo critico → nome, zona IMQ, punteggio, i segnali principali, parcheggio più vicino e distanza, «coperto sì/no»;
- parcheggio → tipo, classe e motivo, posti (dichiarati o stimati), tariffa, punti a favore, firma del riempimento e **mini-profilo 24 ore** (solo se c'è) con «[DATI SCARSI: 2 giorni feriali]»;
- evento → capienza, auto stimate, posti entro 500 m / 1 km, quanti mancano, fermate e corse serali.

**Legenda** (come `legendaFb`/`legendaPendolari`): tinte con le parole, spiegazione delle forme, avvisi [STIMATO]/[DATI SCARSI], scenario e data dei dati.
**Link dalla scheda**: leggere `#tema=interscambio` all'apertura (oggi la scheda apre la mappa senza dire il tema), in modo che «Apri la mappa» porti direttamente qui. Valido per tutte le schede (altri temi: `servizio`, `accessibilita`, `faseb`, ecc.).

**Verifica** (browser): console senza errori; accendere/spegnere ogni livello; toccare un luogo, un parcheggio, un evento; cambiare insieme e raggio (la copertura sul cerchio e i conteggi in legenda
cambiano come in `scenari.json`: 140 / 11 / 147 / 144 a 200 m); schermo stretto; aprire altri 2-3 temi per controllare che non sia cambiato nulla; screenshot a Leo.

## FASE 4 — Scheda in `simulazione.html`: nuovi tipi di grafico

Oggi i grafici sono solo HTML/CSS (nessuna libreria, funziona offline): `barre`, `pila`, `orario` (intervalli di tempo). Servono due aggiunte, nello stesso stile:
1. **`barre` con tono per voce**: campo facoltativo `tono` (`"verde"|"rosso"|"neutro"|…`) per colorare coperte/scoperte; di default invariato (nessun'altra scheda cambia).
2. **`profilo`** (nuovo): curva a 24 ore del riempimento (valori 0-1), più linee sovrapposte (feriale / fine settimana, o 3-4 parcheggi), asse 0-24 come `graficoOrario`, tratteggio per «[DATI SCARSI]».
   Disegnato in SVG inline (poche righe), niente librerie.
3. **`immagini`** (nuovo, facoltativo): immagini statiche (screenshot della mappa) in una cartella `immagini/` accanto a `simulazione.html`, con didascalia; sezione «Com'è fatta in mappa».
   Se mancano i file, la sezione non appare.
4. La `pila` usa già verde/rosso nelle tinte? No: `PALETTE_PILA` è blu/verde acqua/rosso. Per coperte/scoperte usare gli stessi toni di (1).
Verifica: aprire le altre schede (R1, R2, R4, R8, R9) e controllare che non siano cambiate.

## FASE 5 — Scheda Risultato 6 v2 (`schede_risultati.py`)

1. Nuova `scheda_r6_v2()` (la `scheda_r6` resta nel file ma non è più usata nel `main()`). Legge **solo** `mappa_r6.json` (campo `riepilogo`) + `eventi`; nessun calcolo nuovo.
2. Contenuto (italiano semplice; numeri con la virgola e il punto delle migliaia):
   - **Domanda**: «Chi arriva in auto dalla cintura trova un parcheggio vicino alle fermate più importanti? E i parcheggi che si chiamano di interscambio lo sono davvero?»
   - **Numero chiave**: luoghi critici scoperti = 378 − 140 = **238** su 378.
   - **Risposta** (3-4 frasi): critici/coperti; «nessun parcheggio con profilo da pendolare fuori dal centro» (0 di fatto; i 4 interscambi del Comune sono «solo sulla carta»); 758 potenziali ma senza dati d'uso;
     zone con più scoperti; eventi: ordine di grandezza di auto e posti mancanti.
   - **Grafici**:
     1. pila «Luoghi critici: coperti / scoperti» (`tono` verde/rosso) a 200 m;
     2. barre «Copertura a 100 / 200 / 400 m» per insieme (ufficiali, di fatto+potenziali, tutti ≥ 50 posti);
     3. barre «Parcheggi per classe» con posti (di fatto / solo sulla carta / potenziale / non interscambio), tonalità distinte dalla scala verde-rosso;
     4. barre «Perché un parcheggio non è interscambio» (`parcheggi_per_motivo`: zona centrale, nessun punto a favore, …);
     5. barre «Zone con più luoghi critici scoperti» (top 10, `zone_scoperte_top10`, nomi dei quartieri/comuni);
     6. barre «Firme del riempimento» [DATI SCARSI];
     7. **profilo** a 24 ore dei 4 «solo sulla carta» (Stura, Sofia, Caio Mario, Venchi Unica) più Porta Susa FS come esempio di ciclo pulito;
     8. barre per i 3 eventi: auto stimate / posti entro 1 km / mancano.
   - **Immagini** (screenshot di Leo, vedi Domande): 3 viste del tema in mappa.
   - **Metodo / parametri / limiti** da `PIANO_RISULTATO6_V2_GIRO2.md` §4 e dal rapporto: luoghi = fermate entro 40 m; segnali di S2 in parole semplici; universo; zona centrale; 25 m² a posto (±30%);
     2 giorni feriali di riempimento; eventi con capienze da fonti web e auto = 50% ÷ 2,5 ipotizzate; linea d'aria; Allianz non incluso.
   - `mappa: {tema: "interscambio", nota: …}`; `fonti`: i rapporti e gli script 68-79; `avviso` con i tag.
3. **Colori** secondo la Fase 1 (anche `TONI`, `PALETTE_PILA` e le barre di R6; per le altre schede solo se Leo vuole: vedi Domande).
4. Rilanciare lo script, `node --check data\schede_risultati.js`, aprire `simulazione.html` nel browser: tutti i grafici disegnati, il profilo con le linee giuste, link «Apri la mappa» → tema giusto, console pulita, schermo stretto.

## FASE 6 — Chiusura

1. Aggiornare `MEMORIA_PROGETTO.md` (riga FATTO R6 v2, sezione 6, standard colori). Commit su richiesta di Leo.
2. Sul PC di Leo: pagina pubblica? **No**: le condizioni d'uso degli sfondi Esri restano da verificare prima di pubblicare.
3. **Dopo il fetch del 25/10** (≥ 5 feriali): rilanciare 71→72→73→75→76→78→79, poi `04_genera_mappa.py` e `schede_risultati.py`; ricontrollare i numeri in scheda e in memoria.

## Chi fa cosa

| Fase | Chi | Perché |
|---|---|---|
| 1 colori (tutta la mappa) | Claude | tocca ogni tema, serve giudizio e verifica visiva |
| 2-3 tema nuovo | Claude (o agente con piano meccanico dopo la Fase 1) | codice della mappa delicato |
| 4 tipi di grafico | Claude | piccola modifica a `simulazione.html` |
| 5 scheda | Claude | |
| Screenshot | Leo | solo se vuole le immagini |
| 6 | Claude con Leo | |

Ordine consigliato: 1 → 2 → 3 → 4 → 5 → 6 (la Fase 1 prima, perché cambia le palette di tutti i temi e quelle nuove la usano).

## Domande per Leo

1. **Direzione dei colori per le quantità neutre** (abitanti, spostamenti IMQ, pendolari, prezzi): verde = poco, rosso = tanto? (Per il resto: verde = bene, rosso = male.)
2. **Screenshot** per la scheda: li fai tu? Servirebbero 3 viste del tema (tutta Torino coi luoghi critici; zoom su una zona con parcheggi e cerchi; una zona evento). Altrimenti la scheda ha solo i grafici.
3. **Colori nelle altre schede** (R1, R2, R4, R8, R9): le uniformo anch'io (barre e pile coperte/scoperte, ecc.) o per ora solo la R6?
4. **Link dalla scheda alla mappa con il tema già aperto**: ok per tutte le schede?
