# Piano — Risultato 1: dove mancano i servizi a piedi

Piano unico del risultato: in testa lo stato e i lavori da fare, sotto la storia. Scritto da Claude il 20/10/2026
dopo l'analisi di Leo (stessa data). **Nessuna modifica fatta al risultato**: è un piano.

## Stato attuale (versione 1, 12/10)

- Script: `21_risultato1_vuoti.py` (vuoti), `22_risultato1_candidati.py` (dove aggiungere un servizio); dati da
  `18_accessibilita.py` (`data/processed/accessibilita.json`). Rapporti: `docs/RAPPORTO_RISULTATO1.txt`,
  `docs/RAPPORTO_RISULTATO1_CANDIDATI.txt`. Scheda da `schede_risultati.py` (`scheda_r1`).
- Cinque gruppi: scuole, salute, «cibo» (in realtà tutte le attività commerciali del catalogo), fermate, verde.
  Per sezione di censimento: «zero» (nessuna destinazione a 15 minuti a piedi) o «pochissimo» (10% più basso).
- Titolo: **10.919 torinesi (1,3%) senza almeno uno dei 5 servizi**; il più carente è la salute (9.104).
- Fuori Torino scuole, salute e cibo **non sono confrontabili** (catalogo comunale solo per Torino, fuori c'è
  OpenStreetMap, più povero): zero spesso = dato mancante.

## Commenti di Leo (20/10) e controllo sui dati

| Commento | Controllo (dati dentro `mappa_torino.html`, sezioni con abitanti, superficie e «zero» per gruppo) | Fattibile? |
|---|---|---|
| Guardare dove mancano **tutti** i servizi | A Torino solo **8 residenti** non hanno nessuno dei 5; con 3 o più mancanti 2.469; con almeno 1 mancante 10.919 | Sì, subito (i dati ci sono già) |
| Escludere le zone **poco abitate** (parchi, collina, zone poco abitabili) | Dei 10.919, **8.916 vivono in sezioni sotto 2.000 ab/km²**; la sezione tipica di Torino ne ha 21.087. Il titolo di oggi misura soprattutto collina e periferie vuote | Sì, subito |
| Valutare la **cintura** diversamente («paese, non città dei 15 minuti») | Oggi in cintura tutto sembra rosso, ma è soprattutto mancanza di dato | Sì, con un calcolo nuovo (accessibilità col mezzo pubblico già calcolata dallo script 18) |
| Salute e scuole: ospedali grandi contro presidi piccoli, scuole grandi contro piccole | Capienza e iscritti non li abbiamo | Solo come limite dichiarato |

## Decisioni di Leo (20/10)

1. **Criticità = quanti servizi mancano (0-5)** per sezione: mappa a gradini; titolo = residenti con **3 o più**
   servizi mancanti; «tutti mancanti» resta come riga (8 persone, non fa titolo).
2. **Zone poco abitate in grigio, fuori dal titolo**: soglia predefinita **1.000 ab/km²**, con sensibilità a 500 e
   2.000; i loro residenti si dicono a parte.
3. **Cintura con una regola diversa**: Torino = 15 minuti a piedi; cintura = servizio raggiungibile **a piedi in 15
   minuti o col mezzo pubblico**, sempre in tabelle separate. Nota di Claude (20/10): il calcolo esistente (script 18)
   ha il mezzo pubblico solo **entro 45 minuti**, ora per ora; default = **45 minuti alle 8 di un feriale** (già
   calcolato). Un limite più stretto (es. 20 minuti) richiede di rifare l'accessibilità (diverse ore): solo se Leo
   lo chiede.

## Prima stima (Claude, 20/10, dai dati in mappa; da rifare con lo script)

| Soglia «poco abitata» | Torino: residenti in zone poco abitate | Torino: 3+ mancanti (abitate) | Torino: 1+ mancante (abitate) | Fuori Torino: 3+ mancanti (abitate, regola di oggi) |
|---|---|---|---|---|
| 500 ab/km² | 2.875 | 1.821 | 9.566 | 28.297 |
| **1.000 ab/km²** | 6.768 | **751** | 7.017 | 23.318 |
| 2.000 ab/km² | 17.039 | 389 | 2.003 | 8.739 |

Quello che emerge: **Torino è quasi tutta una città dei 15 minuti**; le carenze vere sono poche centinaia di
residenti, e vanno guardate una a una (dove sono, quale servizio manca). È un risultato più forte e onesto di
«10.919 senza servizi». La cintura con la regola di oggi resta non confrontabile: per questo serve la decisione 3.

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Conteggio 0-5 per sezione, soglia di densità con sensibilità (500/1.000/2.000), «poco abitata» come stato a parte | `21_risultato1_vuoti.py` (nuove uscite, le vecchie restano) | piccolo |
| 2 | Cintura: per scuole, salute, cibo usare il tempo col mezzo pubblico (già in `accessibilita.json`) oltre ai piedi; tabelle sempre separate | 21 | medio (controllare prima che i tempi TP per gruppo ci siano davvero) |
| 3 | Rinominare «cibo» in «negozi e attività commerciali» anche nella scheda (in mappa già fatto il 20/10) | `schede_risultati.py` | piccolo |
| 4 | Mappa: tema servizi con i gradini 0-5 (verde→rosso) e il grigio per le zone poco abitate; legenda con i numeri | `04_genera_mappa.py`, `mappa_template.html` | medio |
| 5 | Scheda: titolo nuovo (residenti abitati con 3+ mancanti), «tutti mancanti» come riga, residenti delle zone poco abitate a parte, sensibilità della soglia, limiti (capienza di ospedali e scuole non nota) | `schede_risultati.py` | piccolo |
| 6 | Candidati per nuovi servizi (22): rifarli solo sulle sezioni abitate | 22 | piccolo |
| 7 | Controllo con la realtà: 5-10 sezioni «critiche» guardate a mano con Leo (sono davvero senza servizi?) | — | 1 sessione |

Limite da scrivere sempre: capienza di ospedali, presidi e scuole non nota (un ospedale grande e un ambulatorio
contano uguale); orario programmato; catalogo diverso fra Torino e cintura.

## Come eseguirlo (fase A: calcoli e scheda; fase B: mappa, dopo)

Fase A = lavori 1, 2, 3, 5, 6. Fase B = lavoro 4 (mappa), da fare dopo aver visto i numeri della fase A.
Esito in `docs/ESITO_RISULTATO1_V2.md`; poi Leo fa commit e push e Claude ricontrolla.

### Passi meccanici della fase A (per il modello minore)

1. Prima: ramo `prova`, `git status` pulito, `git pull origin prova`. Alla fine commit e push da solo (`AGENTS.md`). Python del PATH.
2. `scripts/21_risultato1_vuoti.py`: **non cambiare** le uscite di oggi; **aggiungi** nel JSON
   `data/processed/risultato1_vuoti.json` una sezione `"v2"` e nel rapporto una sezione «VERSIONE 2»:
   - per ogni sezione: `n_mancanti` = quanti dei 5 gruppi sono a «zero» (piedi 15 min);
   - densità = residenti / km²: la superficie è il campo `"a"` (km²) di `data/processed/sezioni_torino.json`,
     agganciata per `"id"`; costante `SOGLIA_POCO_ABITATA = 1000` (ab/km²) e sensibilità 500 e 2.000;
   - Torino (sezioni con id che inizia per `1272`): residenti per `n_mancanti` 0..5, separati in «abitate» e «poco
     abitate»; titolo = residenti **abitati** con `n_mancanti >= 3`; riga «tutti e 5 mancanti»;
   - cintura: per scuole, salute, cibo un gruppo manca solo se è a zero **sia** a piedi 15 min **sia** col mezzo
     pubblico entro 45 minuti all'ora `"08"` (campo `"tp"` di `accessibilita.json`: guarda le chiavi con
     `python -c "import json;d=json.load(open('data/processed/accessibilita.json',encoding='utf-8'));s=d['sezioni'][0] if 'sezioni' in d else d[0];print(s.keys(), s['tp'].keys())"`
     e adatta il nome della lista se è diverso); fermate e verde come Torino; tabelle sempre separate da Torino.
   - Controlli (stampa OK/AVVISO): somma dei residenti per `n_mancanti` = residenti totali dell'ambito; nessuna
     densità negativa; sezioni senza superficie contate e scritte (AVVISO se più di 10).
   - Numeri attesi solo come controllo di buon senso (non scriverli nel codice): Torino, soglia 1.000, abitati con 3+
     mancanti dell'ordine di 700-800; residenti in zone poco abitate circa 6.800.
3. `scripts/22_risultato1_candidati.py`: i candidati per nuovi servizi solo su sezioni abitate (densità ≥ soglia):
   aggiungi il filtro e scrivi nell'esito quanti candidati cambiano.
4. `scripts/schede_risultati.py`, `scheda_r1`: il numero in grande diventa i residenti abitati con 3+ mancanti
   (letti dal JSON, mai scritti a mano); «cibo» si chiama «negozi e attività commerciali»; aggiungi un grafico a
   barre «Residenti per numero di servizi mancanti (0-5), zone abitate» e una riga con i residenti delle zone poco
   abitate; sensibilità della soglia (500/1.000/2.000) nei criteri; limite «capienza di ospedali e scuole non nota».
   Aggiorna `in_english` con gli stessi numeri.
5. `python scripts\21_risultato1_vuoti.py`, `python scripts\22_risultato1_candidati.py --gruppi salute,scuole`,
   `python scripts\schede_risultati.py`, `python scripts\prova_pagine_r6.py --senza-screenshot` (0 errori).
6. Nell'esito: la sezione «VERSIONE 2» del rapporto, le righe cambiate, `git status`.

### Prompt da incollare (per Leo)

> Sei un agente che lavora sul progetto GTT in `C:\projects\Progetti\GTT`, ramo git `prova`. Prima:
> `git branch --show-current` (deve dire `prova`), `git status` (se ci sono modifiche fermati e dimmelo),
> `git pull origin prova`. Leggi `AGENTS.md` e `docs/PIANO_RISULTATO1.md`, poi esegui la sezione «Passi meccanici
> della fase A», un passo alla volta. Aggiungi, non togliere: le uscite di oggi dello script 21 restano uguali. Niente
> numeri scritti a mano nei testi. Se un nome di campo è diverso da quello del piano, guarda il file vero, adatta e
> scrivilo. Scrivi tutto in `docs/ESITO_RISULTATO1_V2.md` (OK / AVVISO / FERMO per passo, righe cambiate, numeri).
> Alla fine fai commit e push come dice `AGENTS.md` (sezione «Commit»); se lavori nel cloud (niente `data/`), fai
> solo le modifiche al codice, salta i passi che lanciano gli script e scrivilo nell'esito. Non modificare `MEMORIA_PROGETTO.md`. Python: `python` del PATH, mai Anaconda. Alla fine un
> riassunto di 10 righe in italiano semplice.

## Storia

- 11-12/10: piano dell'accessibilità (`docs/PIANO_ACCESSIBILITA.md`), giro completo il 12/10, fase A (vuoti) e
  fase B (candidati) con Leo. Bug corretto il 12/10: i gruppi erano confrontati su ambiti diversi (Torino contro
  Torino+cintura).
- 20/10: «Negozi di alimentari» rinominato in mappa (il gruppo usa tutte le 31.405 attività del catalogo).
