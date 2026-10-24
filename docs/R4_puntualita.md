# Risultato 4 — Puntualità e attese

**Domande.**
1. Quanti passaggi dei mezzi GTT alle fermate arrivano con più di 5 minuti di ritardo? Su quali linee, a che ora?
2. Sulle linee frequenti, quanto spesso i mezzi arrivano a grappolo (due attaccati) o lasciano un buco?
3. Quanti minuti in più aspetta, alla fermata, chi arriva a caso rispetto a quanto promette l'orario?

**Tag dati:** [MISURATO] con il GPS dei mezzi; pochi giorni di ottobre 2026; solo linee urbane (circa 90).

## Come si misura

- **Fonte degli arrivi: il GPS dei mezzi** (tabella `mezzi_gtt`, una posizione al minuto circa, raccolta dal Raspberry
  Pi). Il feed dei ritardi GTT non si usa più per i numeri: smette di elencare la fermata all'orario programmato,
  quindi per i mezzi in ritardo la sua stima resta troppo bassa. Resta solo come confronto.
- **Passaggio valido:** stessa corsa, a meno di 60 m dalla fermata, segmento fra due posizioni lungo al massimo 180 s
  (istante interpolato sul segmento più vicino), fermate cercate in ordine di `stop_sequence` e ogni passaggio dopo
  quello della fermata precedente, |ritardo| ≤ 60 minuti. Finestra: dalle 02:00 locali di ogni giorno (la fascia
  «notte» è parziale).
- **Ritardo** = istante GPS − orario programmato (GTFS), in minuti.
- **Giorni:** un giorno entra solo se le corse viste dal GPS sono almeno metà della mediana dei giorni dello stesso
  tipo; gli esclusi sono scritti nel rapporto e nel JSON (`giorni_esclusi_gps`).

| Regola | Valore |
|---|---|
| Classi | anticipo sotto −1 min · puntuale da −1 a +5 · in ritardo oltre +5 (e oltre 10) |
| Fasce orarie (ora locale dell'arrivo programmato) | punta mattina 7-9 · giorno 9-16 · punta sera 16-19 · sera 19-24 · notte 0-7 |
| Regolarità | coppie di passaggi consecutivi, stessa fermata e linea, intervallo programmato ≤ 15 min; **grappolo** se osservato < 0,5 × programmato, **buco** se > 2 × |
| Classifiche | linee ordinarie (nome di sole cifre) con almeno 2.000 passaggi (puntualità) o 100 coppie (regolarità) |
| Fine corsa | passaggi alle ultime 3 fermate della corsa, almeno 100 per entrare in classifica |
| Linee utili | le 54 linee che toccano più zone molto frequentate (script 87) |

## Numeri (feriale; `docs/rapporti/RAPPORTO_RISULTATO4.txt`)

Periodo fisso a giorni interi (`comuni.PERIODO["gps"]`, giro L9b): dal 10 al 22 ottobre 2026, mai il giorno della copia dello storico.
Giorni usati: 7 feriali, 2 sabati, 1 domenica (esclusi 14, 18 e 19/10 per poco GPS). Copertura GPS:
**79,8%** dei passaggi programmati delle corse viste (1.606.548 su 2.013.755); le corse mai viste dal GPS non si contano.
Un rilancio con lo stesso periodo dà gli stessi numeri (prova del giro L9b).

| | GPS | Feed (confronto) |
|---|---|---|
| In ritardo oltre 5 minuti | **16,0%** | 6,2% |
| In ritardo oltre 10 minuti | **6,41%** | 0,0% (la regola del feed scarta i ritardi lunghi) |
| Grappolo + buco | **21,6%** (16,4% + 5,2%) | 10,3% |
| Ritardo mediano | 0,1 min | |
| Tram: oltre 5 · oltre 10 · grappolo+buco | 15,4% · 6,20% · 26,8% | 5,4% · 0,0% · 13,4% |
| Bus: oltre 5 · oltre 10 · grappolo+buco | 16,2% · 6,47% · 18,3% | 6,4% · 0,0% · 8,4% |

- Sabato 16,9% oltre 5 minuti; domenica 12,1% (un solo giorno: [DATI SCARSI]).
- Fasce (feriale, oltre 5 minuti): punta mattina 15,5% · giorno 16,3% · punta sera 20,4% · sera 18,2% · notte 5,9%.
- Anticipo (oltre 1 minuto prima), feriale: 35,4% a ogni fermata, 29,0% alla prima fermata (dopo la correzione della partenza), 35,9% a metà corsa, 35,7% fuori punta: l'orario ufficiale ha margini.
- **Linee peggiori per ritardo:** 17 (41,4%), 6 (39,6%), 19 (36,7%), 68, 66, 33, 4, 72, 61, 52.
- **Più irregolari:** 14, 4, 45, 43, 17.
- **Ritardo a fine corsa** (mediana alle ultime 3 fermate): in testa 19, 17 e 4 (tram), da 3,4 a 4,1 minuti.
- **Linee utili** contro le altre: 17,5% contro 13,2% in ritardo oltre 5 minuti; grappolo+buco 22,9% contro 17,2%.
- **GTT dichiara 2,3% oltre 10 minuti per il 2025**: il suo metodo non è pubblicato; qui si misura a ogni fermata con il
  GPS, su pochi giorni di ottobre. Confronto solo come ordine di grandezza.

### Confronto con GTT (oltre 10 minuti, feriale · settimana 5/1/1)

GTT 2,3%. Noi: a ogni fermata 6,41% · 6,18%; solo alla prima fermata 5,48% · 5,28%; a metà corsa 6,15% · 5,86%; fuori dalle ore di punta 5,96% · 5,79%.
**Partenza al capolinea (giro L9b).** Prima, alla prima fermata di una corsa il passaggio era il punto GPS più vicino alla fermata: ma al capolinea il bus aspetta fermo lì vicino, e il punto più vicino cadeva spesso durante l'attesa, prima della partenza vera. Risultato: alla prima fermata sembrava in anticipo il 56,1% dei passaggi (36,0% a ogni fermata) e il ritardo alla partenza era sottostimato (4,29%). Ora, per la sola prima fermata di ogni corsa, il passaggio è l'ultimo istante del gruppo di posizioni vicine alla fermata, cioè quando il bus se ne va (`cerca_vincolata(..., partenza=True)` nello script 27, che vale anche per lo script 70: usa le stesse funzioni); per le altre fermate niente cambia. Dopo la correzione l'anticipo alla prima fermata è il 29,0% (sotto il 30% fissato), il ritardo alla partenza 5,28% (prima 4,29%). La prova con una corsa finta (bus fermo 4 minuti, poi parte) è `scripts/prove/prova_capolinea.py`.
Incertezza: ±1 minuto sui passaggi = 5,5-7,6% (feriale); corse senza GPS tutte puntuali o come i giorni peggiori = 5,16-6,93%. Dettaglio nella sezione «CONFRONTO CON GTT» del rapporto; JSON `confronto_gtt`.

### Attese (alla fermata, linee frequenti)

Per chi arriva a caso, con intervalli h1…hn l'attesa media è `Σh² / (2·Σh)`. Linea frequente = intervallo programmato
medio ≤ 12 minuti per fermata-linea-verso-fascia (almeno 6 intervalli); media pesata sugli intervalli programmati;
solo ore con raccolta attiva. Le corse assenti dal GPS fanno due stime: **bassa** (solo tratti senza corse mancanti)
e **alta** (una corsa assente dal GPS conta come saltata); chiavi con più del 20% di corse assenti = dati scarsi.

| Feriale | Promessa | In più (bassa – alta) | Intervalli osservati |
|---|---|---|---|
| Città | 4,8 min | **1,6 – 1,7 min** (+33% sulla promessa, stima bassa) | 92.004 |
| Tram | 4,5 min | 1,7 – 1,7 min | 73.550 |
| Bus | 5,7 min | 1,1 – 2,0 min | 18.454 |

Per fascia l'attesa in più (stima bassa) va da 0,8 min (notte) a 2,1 min (punta sera).

## Mappa e scheda

Tema «Puntualità delle linee» (linee colorate per % di ritardo oltre 5 minuti nell'ora scelta: sotto 10% · 10-15 ·
15-20 · 20-30 · oltre 30%), link dalla scheda con `#tema=puntualita&linea=17&ora=8`. Scheda `scheda_r4` (con la parte
attese `scheda_r9`) in `scripts/schede_risultati.py`.

## Limiti

- Pochi giorni (non tutti interi), solo linee urbane viste dal GPS; niente extraurbane.
- Il GPS c'è per circa tre passaggi su quattro delle corse viste; se corse mai viste erano saltate, la puntualità vera
  è peggiore.
- Distanza di 60 m dalla fermata: un mezzo fermo poco prima conta come arrivato poco dopo.
- Dice quanto spesso c'è ritardo, non quante persone aspettano né quanto erano pieni i mezzi.
- Attese: stima a forbice; i bus hanno molti meno dati dei tram.

## Script e come rifarlo

| Script | Cosa fa |
|---|---|
| `27_risultato4_regolarita.py` | puntualità, regolarità, fine corsa, linee utili, confronto col feed (opzione `--fonte feed` per il calcolo col feed) |
| `70_risultato9_attesa.py` | attesa promessa contro reale, per linea, fermata, modo |
| `87_popolarita_zone.py` | popolarità delle zone e linee utili (input) |

```
python scripts\27_risultato4_regolarita.py
python scripts\70_risultato9_attesa.py
python scripts\04_genera_mappa.py
python scripts\schede_risultati.py
python scripts\prova_pagine.py --senza-screenshot
```

Dati: `data/storico_backup.sqlite` (copia dal Pi, sola lettura), GTFS in `data/raw/`. Fonte del 2,3%:
`docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`.
