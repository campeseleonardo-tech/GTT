# Esito — R4, confronto con GTT (B1, B2, B4) — 21/10/2026

Piano: `PIANO_RISULTATI.md`, parte B. File: `scripts/27_risultato4_regolarita.py` (B1, B2), `scripts/schede_risultati.py` (B4).
Fonte degli arrivi: GPS (predefinita). Tutto è aggiunto in coda: le uscite di prima sono identiche (JSON: stesse chiavi e stessi valori,
nuova solo `confronto_gtt`; l'unica differenza è il percorso scritto in `parametri.rif_gtt_fonte`; rapporto: 25 righe in più, nessuna cambiata).

## B1 — quota di passaggi oltre 10 minuti, 4 definizioni

Giorni: 6 feriali, 2 sabati, 1 domenica (10-20 ottobre; domenica con un solo giorno: [DATI SCARSI]). Settimana = media pesata 5 / 1 / 1 delle tre percentuali.
GTT dichiara **2,3%** (anno 2025, tutte le linee, metodo non pubblicato).

| Definizione | Feriale | Sabato | Domenica | **Settimana 5/1/1** | Passaggi feriale |
|---|---|---|---|---|---|
| (a) a ogni fermata (come oggi) | 5,44% | 7,10% | 4,11% | **5,49%** | 944.276 |
| (b) solo alla prima fermata della corsa | 3,86% | 5,34% | 2,81% | **3,92%** | 21.374 |
| (c) solo alla fermata di mezzo della corsa | 5,29% | 6,92% | 3,34% | **5,24%** | 30.292 |
| (d) solo fuori dalle ore di punta (fuori da 7-9 e 16-19) | 5,27% | 6,75% | 3,98% | **5,30%** | 657.981 |

Lo stesso, oltre 5 minuti: (a) 14,12 / 16,81 / 12,03 → 14,21% · (b) 7,77 / 10,11 / 6,36 → 7,90% · (c) 14,00 / 16,32 / 11,45 → 13,97% · (d) 13,76 / 16,72 / 11,88 → 13,91%.

**Lettura.** L'atteso del piano («alla partenza» vicino al 2-3%) si avvera solo in parte: alla prima fermata il numero scende a 3,9% (sotto di un terzo rispetto
ad (a)), ma non arriva a 2,3%. A metà corsa e fuori punta il numero resta vicino ad (a). La differenza con GTT non si spiega solo con la definizione:
restano stagione, linee, metodo non pubblicato. **AVVISO**: (b) e (c) poggiano su pochi passaggi (21.000 e 30.000 nei feriali; il GPS vede la prima fermata
solo per una parte delle corse), quindi sono meno solide di (a).

## B2 — incertezza nostra

(i) Passaggi spostati di −1 e +1 minuto (oltre 10 | oltre 5):

| Spostamento | Feriale | Sabato | Domenica |
|---|---|---|---|
| −1 min | 4,61% \| 11,42% | 6,18% \| 13,83% | 3,44% \| 9,45% |
| 0 | 5,44% \| 14,12% | 7,10% \| 16,81% | 4,11% \| 12,03% |
| +1 min | 6,44% \| 17,72% | 8,19% \| 20,62% | 5,01% \| 15,64% |

Un minuto di errore sposta l'oltre 10 minuti di circa ±0,9-1 punto (feriale 4,6-6,4%), l'oltre 5 minuti di circa ±3 punti: il numero a 10 minuti è
robusto come ordine di grandezza, quello a 5 minuti molto meno.

(ii) Passaggi programmati delle corse viste ma senza GPS valido (feriale 256.258 contro 944.276 con GPS). «Peggiori» = quota del 10% dei giorni peggiori dello stesso tipo (almeno 1 giorno):

| Tipo | Misurato | Mancanti tutti puntuali | Mancanti come i peggiori | Quota peggiori |
|---|---|---|---|---|
| Feriale | 5,44% | 4,28% | 5,74% | 6,81% |
| Sabato | 7,10% | 5,59% | 7,29% | 8,00% |
| Domenica | 4,11% | 3,07% | 4,11% | 4,11% (un solo giorno: il peggiore è l'unico) |

Forbice sul feriale: **4,3% - 5,7%**: nessuno dei due casi porta il numero vicino al 2,3% di GTT. **AVVISO**: le corse mai viste dal GPS non sono nella forbice
(non si sa se hanno girato); se erano saltate, la puntualità vera è peggiore.

## B4 — scheda R4

Grafico a barre «Noi e GTT: passaggi in ritardo oltre 10 minuti» (GTT 2,3% e le 4 definizioni, media della settimana) e 3 righe in «risposta» (non la stessa
misura; dove cresce il ritardo con i numeri di (b), (c), (a), (d); «tra 2,3% e 5,5%»), più una riga in inglese. Numeri letti da `confronto_gtt` del JSON; il 2,3% è la costante
`GTT_RITARDO10_2025_PCT` con la fonte nel commento (rapporto di sostenibilità GTT 2025, p. 128).

## Controlli (stampati dallo script 27, tutti OK)

- per ogni definizione e tipo di giorno: oltre 10 ≤ oltre 5;
- (a) = totale della città (944.276 / 244.582 / 111.576); fuori punta + di punta = totale (657.981 + 286.295 = 944.276 nei feriali);
- spostamento 0 = (a); forbice: puntuali ≤ misurato ≤ come i peggiori.

## Lanci

`27` (2 min 30 s), `70`, `04` (mappa 13,1 MB), `schede_risultati.py`, `prova_pagine_r6.py --senza-screenshot`: **0 errori** su 13 pagine.

## Da sapere

- B3 (stagione) non fatto: richiede la raccolta di gennaio e luglio.
- Il confronto non è ancora nella mappa (solo scheda e rapporto, sezione «CONFRONTO CON GTT»).
