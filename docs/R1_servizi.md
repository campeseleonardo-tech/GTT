# Risultato 1 — Dove mancano i servizi a piedi

**Domanda.** In quali zone di Torino abitate mancano, a 15 minuti a piedi, i servizi essenziali (scuole, salute,
negozi e attività commerciali, fermate del mezzo pubblico, verde), e dove aggiungerne uno aiuterebbe più persone?

**Tag dati:** [STIMATO] su orario programmato (nessun ritardo, capienza o domanda reale).

## Come si calcola

Per ogni sezione di censimento (8.317 in tutto; 848.748 residenti a Torino) l'accessibilità viene da
`scripts/18_accessibilita.py` (motore R5, a piedi 15 minuti a 80 m/min; mezzo pubblico fino a 45 minuti alle 8 di un
feriale; vedi `docs/METODO.md`). Un servizio **manca** quando non c'è nessuna destinazione del gruppo raggiungibile.

| Criterio | Valore |
|---|---|
| Gruppi | scuole · salute · negozi e attività commerciali (nel dato «cibo») · fermate · verde |
| Torino | servizio mancante = zero destinazioni a piedi in 15 minuti (catalogo comunale) |
| Cintura | mancante solo se zero a piedi in 15 minuti **e** zero col mezzo pubblico in 45 minuti alle 8; servizi da OpenStreetMap, più poveri: tabelle sempre separate da Torino |
| Criticità | numero di servizi che mancano (0-5) per sezione |
| Zone poco abitate | sotto 1.000 abitanti/km² (sensibilità 500 e 2.000): in grigio, fuori dal titolo |
| Zone da verificare | zero fermate a 15 minuti a piedi ma una fermata GTT entro 300 m in linea d'aria (il calcolo a piedi non la raggiunge): contate a parte |
| Titolo | residenti di Torino, in zone abitate, senza 3 o più dei 5 servizi |

## Numeri (rapporto `docs/rapporti/RAPPORTO_RISULTATO1.txt`)

- **362 residenti** di Torino in zone abitate senza 3 o più servizi: 5 sezioni, tutte in collina (zone confermate
  guardandole una a una).
- **8 residenti** senza nessuno dei 5 servizi (non fanno titolo); 6.768 vivono in zone poco abitate (a parte);
  389 in 2 sezioni da verificare (fermata a 75-179 m che il calcolo a piedi non raggiunge).
- Nelle zone abitate di Torino nessuno ha 4 o 5 servizi mancanti.
- Sensibilità della soglia di densità (poco abitate / abitate con 3+ mancanti): 500 ab/km² → 2.875 / 1.395;
  1.000 → 6.768 / 362; 2.000 → 17.039 / 0.
- Cintura con la regola piedi o mezzo pubblico: 834 residenti abitati con 3+ mancanti (con i soli piedi 23.318: il
  dato mancante pesa più del servizio mancante).
- Dove aggiungere un servizio (script 22, solo zone abitate): candidati scuole 5 (1.912 residenti guadagnati),
  salute 5 (3.846), negozi 3 (347), fermate 1 (85), verde 0.
- In Torino i servizi più carenti per residenti a zero sono la salute e le scuole.

## Mappa e scheda

Tema «Dove mancano i servizi» della mappa: gradini 0-5 (verde → rosso), grigio per le zone poco abitate, lilla per
le zone da verificare, cerchi sulle zone abitate con 3+ mancanti, viste per singolo servizio con i candidati.
La scheda è `scheda_r1` in `scripts/schede_risultati.py`.

## Copertura a 5, 10 e 15 minuti e traffico (v3, 21/10)

Sezione «v3» di `risultato1_vuoti.json` e «VERSIONE 3» del rapporto: per Torino, solo zone abitate (almeno 1.000 ab/km²),
residenti con tutti e 5 i servizi a 5, 10 e 15 minuti a piedi e residenti per numero di servizi presenti (0-5). I tempi a 5 e 10
minuti vengono dallo script 18 con `--solo-piedi` (`scripts\R1_PIEDI_5_10.bat`: `accessibilita_piedi5.json` e
`accessibilita_piedi10.json`, `accessibilita.json` non si tocca). Controlli: la somma dei residenti torna a ogni soglia; copertura a 5 ≤ 10 ≤ 15.
Per circoscrizione: saltato, le sezioni non hanno il campo. Esposizione al traffico: script 92, classi esposta (meno di 100 m) /
vicina (100-250 m) / lontana. Il traffico è una stima e sostituisce rumore e smog, che non misuriamo.

## Limiti

- Capienza di ospedali, presidi e scuole non nota: un ospedale e un ambulatorio contano uguale.
- Orario programmato: ottimista per definizione.
- Il gruppo «negozi» usa tutte le attività commerciali del catalogo, senza distinguere la categoria.
- Fuori Torino scuole, salute e negozi vengono da OpenStreetMap (senza relazioni/multipoligoni): Torino e cintura non
  sono confrontabili.
- I candidati sono zone indicative, non indirizzi verificati.
- Le 2 sezioni da verificare (via Chieti) sono già in `SEZIONI_FUORI_RETE` dello script 18: valgono dal prossimo calcolo. Finché l'accessibilità a 15 minuti non è rifatta restano fuori dalla copertura v3.

## Script e come rifarlo

| Script | Cosa fa |
|---|---|
| `18_accessibilita.py` | accessibilità per sezione (input; si rifà solo se cambia il GTFS: `scripts\ACCESSIBILITA_24ORE.bat`) |
| `21_risultato1_vuoti.py` | conteggio 0-5, zone poco abitate e da verificare, sezioni critiche |
| `22_risultato1_candidati.py` | dove aggiungere un servizio (tutti e 5 i gruppi) |
| `92_esposizione_traffico.py` | residenti a meno di 100 m da una strada molto trafficata (≥ 11.720 veicoli/giorno, come il R8): stima debole |
| `schede_risultati.py` | scheda (`data/schede_risultati.js`) |

```
python scripts\21_risultato1_vuoti.py
python scripts\22_risultato1_candidati.py
python scripts\04_genera_mappa.py
python scripts\schede_risultati.py
python scripts\prova_pagine_r6.py --senza-screenshot
```

I primi due si lanciano insieme con `scripts\RISULTATO1_VUOTI.bat` e `scripts\RISULTATO1_CANDIDATI.bat`.
