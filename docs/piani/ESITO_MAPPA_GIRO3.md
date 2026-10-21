# Esito — mappa, giro 3 (21/10/2026)

Piano: `PIANO_MAPPA.md` sezione 3 e `ANALISI_STATO.md` 5.1 punto 5 e 5.2. File: `scripts/05_prepara_sezioni.py`, `scripts/04_genera_mappa.py`, `scripts/mappa_template.html`.
**Peso della mappa: 13,14 MB (13.138.524 byte) prima → 13,54 MB (13.542.954 byte) dopo** (+0,4 MB per i campi nuovi delle sezioni e il confine; la riduzione è del giro 4).

## Tracciato del file ISTAT (`TRACCIATO FILE REGIONALI.xlsx`, letto da `05_prepara_sezioni.py`)

- **P14-P29 sono le classi d'età a 5 anni:** P14 meno di 5 · P15 5-9 · P16 10-14 · P17 15-19 · P18 20-24 · P19 25-29 · P20 30-34 · P21 35-39 · P22 40-44 · P23 45-49 · P24 50-54 · P25 55-59 · P26 60-64 · P27 65-69 · P28 70-74 · P29 **oltre 74 anni** (classe aperta).
- **Non esiste una classe 80+**: l'ultima è «oltre 74». La vista «Grandi anziani 80+» **non è stata fatta**, come da istruzione.
- **Famiglie per numero di componenti: sì.** PF1 totale, PF3 un componente, PF4 due, PF5 tre, PF6 quattro, PF7 cinque, PF8 sei e oltre. Usati PF1 e PF3 per «Persone sole».
- Titolo di studio: P83 (9+ anni), P86-P90 (P90 = titoli terziari). Nel file ci sono anche i campi sulla nazionalità (IT, ST): **non usati, mai**.
- Letti dal 05, in più di prima: P14, PF1, PF3. Campi nuovi in `sezioni_torino.json`: `p014` (0-14), `em` (età media stimata dai centri delle classi; per «oltre 74» si assume 80), `pf1`, `pf3`. Passati al 04 (`p014, em, ist9, it, pf1, pf3`) e alla proiezione `sez` del template (con `f`). Tolto `sc` (5-14, non più usato).

## Per punto

| Punto | Esito | Note |
|---|---|---|
| «Chi abita qui» completo | OK | Viste: Abitanti per km² (predefinita) · Bambini e ragazzi 0-14 · Anziani 65+ · **Età media (stima)** · Laureati · Occupati 15-64 · Persone per famiglia · Persone sole. **Grandi anziani 80+: non fatta** (classe non esistente). Blu→arancione, 5 classi a quantili (calcolati sulle sezioni non grigie), numeri in legenda. Sotto 50 abitanti le percentuali non si calcolano (grigio in mappa). |
| Profilo al clic | OK | 5 barre (giovani, anziani, laureati, occupati, persone per famiglia) con la tacca scura del valore di Torino; sotto 50 abitanti: «troppo pochi abitanti per le percentuali». Provato in Chromium. |
| «Persone sole» anche in «Fragilità sociale» | OK | Voce nuova (verde→rosso), fuori dall'indice composito. |
| Tolto «Residenti 11-84 anni» da «Spostamenti» | OK | |
| Zone quasi disabitate in grigio | OK | Sotto 1.000 ab/km² in tutti i temi per sezioni, tranne «Abitanti per km²»; riga di legenda «grigio = zona con pochi abitanti (sotto 1.000 per km²)». «Servizi mancanti» tiene la sua regola. |
| Confine di Torino | OK | Linea scura sottile in tutti i temi per sezioni; viene dai confini ISTAT 2022 (nuovo `confine_torino()` nel 04: 2 anelli, 130 punti), non dalle sezioni. |
| «Servizi a portata», legenda | OK | «Torino e cintura hanno colori calcolati a parte: non confrontarle fra loro» + «confronto con le zone di Torino / della cintura». |
| Legende corte | OK, con un limite | Titolo, colori con i numeri, una riga di fonte (+ riga del grigio dove serve). Date al minuto tolte: «media di 13 giorni feriali, ottobre 2026». Parcheggi di scambio: spiegazioni lunghe spostate nella guida (parcheggi, zone grigie). **AVVISO**: restano un po' più lunghe le legende di «Servizi mancanti» (2 righe di colori con spiegazione) e «Spostamenti»; la lista dei 12 punti di «Dove servirebbe un parcheggio» è contenuto, non testo. |
| Parcheggi di scambio: centro | OK | Viola chiaro (#cdbfe6) e circa la metà del raggio. |
| Prezzo delle case | OK | Solo Abitazioni, Negozi, Uffici; in legenda minimo e massimo (sostituiscono «meno caro / più caro»). |
| Telefono (< 600 px) | OK | Pannello chiuso all'avvio e bottone «Temi». Provato a 390 px: nessuno scroll orizzontale; apre il pannello (318 px). |

## Valori di 3 sezioni (più 2 di controllo)

Percentuali sui residenti della sezione (laureati sui 9+ anni, occupati sui 15-64, persone sole sulle famiglie). Tutti i valori sono fra 0 e 100 e le età medie fra 30 e 60.

| Sezione | Abitanti | per km² | 0-14 | 65+ | Età media | Laureati | Occupati | Pers./famiglia | Pers. sole |
|---|---|---|---|---|---|---|---|---|---|
| **Centro** — Torino, Piazza Castello (12720000081) | 221 | 21.925 | 7,2% | 21,3% | 47,3 | 42,7% | 68,4% | 1,71 | 59,7% |
| **Periferia** — Torino, Falchera (12720002764) | 558 | 6.120 | 10,2% | 27,6% | 48,4 | 6,9% | 66,3% | 2,01 | 43,0% |
| **Cintura** — Venaria Reale (12920000068) | 336 | 8.604 | 16,7% | 18,2% | 42,7 | 15,1% | 65,3% | 2,32 | 33,8% |
| Periferia — Torino, Mirafiori Sud (12720002788) | 1.888 | 46.218 | 10,8% | 26,0% | 47,9 | 9,1% | 62,3% | 2,32 | 36,3% |
| Cintura — Rivoli (12190000004) | 170 | 13.067 | 10,0% | 22,4% | 48,2 | 24,4% | 68,7% | 1,87 | 46,2% |

Totali di Torino: 0-14 anni 11,7%, 65+ 26,0%, età media stimata 47,1, famiglie di una persona 47,5%; coerenti con le statistiche note. Il centro ha più laureati e più persone sole, la cintura più giovani.

**AVVISO**: fra le 5.360 sezioni con almeno 50 abitanti, **43** hanno un'età media stimata fuori da 30-60 (da 18 a 80 anni): sono convivenze (residenze per anziani, studentati, caserme); i dati sono veri, la mappa le mostra agli estremi della scala.

## Prove

- `python scripts\05_prepara_sezioni.py`: OK (8.317/8.317 sezioni abitate agganciate). `python scripts\04_genera_mappa.py`: OK. `python scripts\prova_pagine_r6.py --senza-screenshot`: **0 errori** su 13 pagine.
- Chromium (1024 px e 390 px): tutte le 8 viste di «Chi abita qui» con legenda e nessun errore; profilo e messaggio sotto 50 abitanti; grigio e confine visibili; telefono con «Temi».

## Non fatto / da sapere

- «Grandi anziani 80+»: la classe non esiste (ultima = oltre 74).
- Il quantile delle viste nuove esclude le zone grigie; le viste di «Fragilità sociale» (indice, componenti) e «Servizi a portata» (singoli gruppi) mantengono i loro quantili su tutte le sezioni.
- Resta da fare dal piano: «Luoghi della città» a 6 caselle (sezione 6), peso (sezione 7), schede uniformi (sezione 8).
