# Esito pulizia dei documenti (passi 1-7, 10 e 12 di `PIANO_DOCUMENTI.md`)

Ramo `prova`, albero pulito all'inizio, pull già aggiornato. `data/` non toccata. Non fatti, come richiesto: passi 8
(script), 9 (`.bat`), 11 (README), 13 (mappa in git).

| Passo | Esito |
|---|---|
| 1 - cancellare `docs/archivio/` | OK |
| 2 - cancellare gli esiti | OK |
| 3 - cancellare i piani chiusi | OK |
| 4 - un documento per risultato | OK |
| 5 - `docs/METODO.md` | OK |
| 6 - rapporti in `docs/rapporti/` | OK, con un AVVISO (sotto) |
| 7 - documenti personali | OK |
| 10 - rumore nel codice visibile | OK, limitato ai file visibili (sotto) |
| 12 - memoria | OK |

Prove: `python -m py_compile` su tutti i 58 script `.py` modificati o aggiunti: 0 errori. `python scripts\schede_risultati.py`:
OK (4 schede). `python scripts\prova_pagine_r6.py --senza-screenshot`: **0 errori sulle 13 pagine**.

## Passo 1 - `docs/archivio/`
Cancellata tutta la cartella (75 file). `git grep` prima: i rimandi stavano in `FONTI_DATI.md`, `scripts/80_porte_interscambio.py`,
`scripts/schede_risultati.py` (fonti della scheda R8), `scripts/archivio/76_verifiche_r6v2.py` (script archiviato, non toccato:
passo 8) e nella memoria. Aggiornati i primi tre e la memoria.

## Passo 2 - esiti
Cancellati i 13 `docs/ESITO_*.md` (`GIRO1_RITOCCHI`, `POPOLARITA_ZONE`, `R1_MAPPA`, `R1_MAPPA_BIS`, `R4_GIRO2`, `R4_GIRO5`,
`R4_GIRO6`, `R4_GPS_PROVA`, `R4_VERIFICA_GPS`, `R6_GIRO2`, `R6_PROPOSTA_FERMATE`, `R6_SENSORI`, `RISULTATO1_V2`). I numeri ancora validi
(R1 v2, R4 col GPS e attese, R6 giro 2, controllo con i sensori, proposta fermate, popolarità) sono in `docs/R1_servizi.md`,
`R4_puntualita.md`, `R6_parcheggi.md`. Rimandi aggiornati: memoria (`ESITO_R6_*`, `ESITO_POPOLARITA_ZONE`).

## Passo 3 - piani chiusi
Cancellati `PIANO_GIRO1_RITOCCHI.md` e `PIANO_PULIZIA.md` (contenuto vivo già nella memoria).

## Passo 4 - un documento per risultato
Creati `docs/R1_servizi.md`, `R4_puntualita.md`, `R6_parcheggi.md`, `R8_traffico.md`, `R2_metro_notte.md`: domanda, criteri,
numeri, limiti, script e comando per rifare, ciascuno entro circa 2 pagine, senza storia, «giri», prompt o nomi. Numeri
presi dai rapporti attuali (R4 dopo l'esclusione dei giorni con poco GPS; R6 dopo il giro con la regola fissa) e dalla
memoria. Cancellati `PIANO_RISULTATO1/2/4/6/8.md`. Rimandi aggiornati: `scripts/18`, `21`, `25`, `26`, `35-38b`, `44`, `49`,
`50b`, `66`, `70`, `80`, `84`, `comuni.py`, `schede_risultati.py` (le «fonti» delle schede puntano ai nuovi documenti),
`AGENTS.md`, memoria.

Note: il piano del R4 (`PIANO_RISULTATO4.md`, 786 righe) conteneva anche la storia dei giri e le regole D1-D9 del feed: le
regole ancora valide per il GPS (classi, fasce, coppie, minimi) sono nel nuovo documento; quelle solo del feed (D1-D3) non
sono riportate, restano in git.

## Passo 5 - `docs/METODO.md`
Creato (dati e area, etichette, motore di accessibilità, standard tecnici, colori). Cancellati `PIANO_ACCESSIBILITA.md`
e il rimando nello script 18 (ora «vedi docs/METODO.md»).

## Passo 6 - rapporti
- Spostati in `docs/rapporti/` (con `git mv`) i 31 `RAPPORTO_*.txt` che hanno uno script vivo, il grafico
  `grafico_misurato_vs_previsto.png` (scritto dallo script 44) e il riassunto del rapporto di sostenibilità.
- Cancellati senza script vivo: `RAPPORTO_ACCESSIBILITA_NOTTE15/30`, `RAPPORTO_IMQ`, `RAPPORTO_VELOCITA_5T_prima_fetch`, `TRAFFICO_AB`,
  `TRAFFICO_C`, `TRAFFICO_C_V2`, `TRAFFICO_C_V3`, `TRAFFICO_C_SEGMENTI`, `TRAFFICO_C_VALIDAZIONE`, `RISULTATO8_TRAFFICO_TP` (v1),
  `R4_GPS_PROVA`, `R4_VERIFICA_GPS`, `R6_PROPOSTA_FERMATE` (14 file).
- Script modificati (solo il percorso di uscita `docs/RAPPORTO_` → `docs/rapporti/RAPPORTO_`, più una riga che crea la
  cartella se manca): 56 file `.py` in `scripts/` (esclusi quelli in `scripts/archivio/`; alcuni anche per i rimandi ai documenti) e 7 `.bat` (solo i messaggi e il
  `copy`/`Get-Content` del bat della velocità 5T). Esempio, `scripts/21_risultato1_vuoti.py`:
  `RAPPORTO = RADICE / "docs/RAPPORTO_RISULTATO1.txt"` → `RADICE / "docs/rapporti/RAPPORTO_RISULTATO1.txt"` + `RAPPORTO.parent.mkdir(parents=True, exist_ok=True)`.
- **AVVISO:** alcuni script delle fasi vecchie del traffico (37, 43, 44, 45, 50b, 53, 54) sono ancora nel `.bat` settimanale e
  riscriveranno i rapporti che ho cancellato, ora in `docs/rapporti/`. Lo script 83 legge (se esiste) il rapporto della
  proposta fermate per un controllo facoltativo: ora non c'è finché non si rilancia lo script 89. Ne parla il passo 8 (script superati).

## Passo 7 - documenti personali
`CONOSCENZA_TORINO_LEO.md` portato, anonimo, come «Controllo di buon senso» dentro `R8_traffico.md` e cancellato.
`RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md` → `docs/rapporti/`; aggiornati gli script 27 e 32 e il `.bat` del passo 3 del rapporto.

## Passo 10 - rumore nel codice visibile
Tolti i marcatori `[R6]`, `[R4]`, `[pulizia]`, `[revisione 18/10]`, `[correzioni 20/10]`, le date dei commenti e le menzioni
a persone in `scripts/mappa_template.html`, `simulazione.html`, `scripts/schede_risultati.py`, `scripts/04_genera_mappa.py`;
nelle schede le parole di stato non portano più date («Fatto», «Chiuso», «Versione 1», «Versione 2»). Nei testi visibili
delle pagine non c'erano altre date. Non rigenerata `mappa_torino.html` (cambiano solo commenti): al prossimo `04` si
aggiorna. Non toccati i commenti degli altri script (le menzioni a nomi e date negli script di calcolo restano).

## Passo 12 - memoria
`MEMORIA_PROGETTO.md`: sezione 3 (Cartelle) riscritta con i percorsi nuovi (`docs/R*.md`, `METODO.md`, `piani/`, `rapporti/`); tutti i
rimandi a documenti cancellati o spostati corretti; sezione 5 con lo stato della pulizia e i passi che restano (8, 9, 11, 13).
Nessuna decisione tolta. `AGENTS.md`: i piani vanno in `docs/piani/`.

## git status (prima del commit)
75 file cancellati in `docs/archivio/`, 36 altri documenti cancellati (13 esiti, 2 piani chiusi, 5 piani dei risultati, il piano
dell'accessibilità, il documento personale, 14 rapporti), 6 nuovi (`METODO.md`, `R1/R2/R4/R6/R8`), 5 piani, 33 file di `docs/rapporti/` e `ESITO_DOCUMENTI.md` spostati o aggiunti,
modifiche a `AGENTS.md`, `MEMORIA_PROGETTO.md`, `FONTI_DATI.md`, `ANALISI_STATO.md`, script, template e `simulazione.html`. Nessun file
in `data/`, nessun `.bak`.
