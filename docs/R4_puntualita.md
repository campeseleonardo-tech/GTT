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

Giorni usati: 6 feriali, 2 sabati, 1 domenica (10-20 ottobre 2026; esclusi 14, 18 e 21/10 per poco GPS). Copertura GPS:
**78,3%** dei passaggi programmati delle corse viste (1.300.434 su 1.660.225); le corse mai viste dal GPS non si contano.

| | GPS | Feed (confronto) |
|---|---|---|
| In ritardo oltre 5 minuti | **14,1%** | 5,4% |
| In ritardo oltre 10 minuti | **5,44%** | 0,0% (la regola del feed scarta i ritardi lunghi) |
| Grappolo + buco | **20,9%** (15,9% + 5,0%) | 10,5% |
| Ritardo mediano | −0,1 min | |
| Tram: oltre 5 · oltre 10 · grappolo+buco | 14,4% · 5,66% · 26,7% | 5,1% · 0,0% · 14,0% |
| Bus: oltre 5 · oltre 10 · grappolo+buco | 14,0% · 5,38% · 17,1% | 5,5% · 0,0% · 8,4% |

- Sabato 16,8% oltre 5 minuti; domenica 12,0% (un solo giorno: [DATI SCARSI]).
- Fasce (feriale, oltre 5 minuti): punta mattina 12,3% · giorno 15,2% · punta sera 16,8% · sera 15,6% · notte 5,7%.
- Anticipo (oltre 1 minuto prima): circa il 38% dei passaggi, perché l'orario ufficiale ha margini.
- **Linee peggiori per ritardo:** 17 (38,1%), 6 (36,7%), 19 (30,1%), 68, 33, 66, 61, 4, 72, 52.
- **Più irregolari:** 14, 30, 4, 45, 17.
- **Ritardo a fine corsa** (mediana alle ultime 3 fermate): in testa 19, 4 (tram) e 17, circa 3 minuti.
- **Linee utili** contro le altre: 15,5% contro 11,4% in ritardo oltre 5 minuti; grappolo+buco 21,9% contro 17,2%.
- **GTT dichiara 2,3% oltre 10 minuti per il 2025**: il suo metodo non è pubblicato; qui si misura a ogni fermata con il
  GPS, su pochi giorni di ottobre. Confronto solo come ordine di grandezza.

### Confronto con GTT (oltre 10 minuti, feriale · settimana 5/1/1)

GTT 2,3%. Noi: a ogni fermata 5,44% · 5,49%; solo alla prima fermata 3,86% · 3,92%; a metà corsa 5,29% · 5,24%; fuori dalle ore di punta 5,27% · 5,30%.
Incertezza: ±1 minuto sui passaggi = 4,6-6,4% (feriale); corse senza GPS tutte puntuali o come i giorni peggiori = 4,3-5,7%. Dettaglio nella sezione «CONFRONTO CON GTT» del rapporto; JSON `confronto_gtt`.

### Attese (alla fermata, linee frequenti)

Per chi arriva a caso, con intervalli h1…hn l'attesa media è `Σh² / (2·Σh)`. Linea frequente = intervallo programmato
medio ≤ 12 minuti per fermata-linea-verso-fascia (almeno 6 intervalli); media pesata sugli intervalli programmati;
solo ore con raccolta attiva. Le corse assenti dal GPS fanno due stime: **bassa** (solo tratti senza corse mancanti)
e **alta** (una corsa assente dal GPS conta come saltata); chiavi con più del 20% di corse assenti = dati scarsi.

| Feriale | Promessa | In più (bassa – alta) | Intervalli osservati |
|---|---|---|---|
| Città | 4,7 min | **1,6 – 2,4 min** (+34% sulla promessa, stima bassa) | 72.420 |
| Tram | 4,5 min | 1,8 – 2,4 min | 57.920 |
| Bus | 5,6 min | 1,1 – 2,4 min | 14.500 |

Per fascia l'attesa in più (stima bassa) va da 0,6 min (notte) a 2,1 min (punta sera).

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
python scripts\prova_pagine_r6.py --senza-screenshot
```

Dati: `data/storico_backup.sqlite` (copia dal Pi, sola lettura), GTFS in `data/raw/`. Fonte del 2,3%:
`docs/rapporti/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`.
