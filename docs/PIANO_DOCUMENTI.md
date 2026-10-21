# Piano — pulizia dei documenti e del repository

Obiettivo: chi apre il repository capisce in 2 minuti cosa c'è e da dove partire. Niente storia dello sviluppo in
vista (resta in git). Decisione di Leo (21/10): i documenti superati si **cancellano**, non si archiviano.

## Come sarà alla fine

```
README.md                  presentazione (italiano + inglese), link a mappa e schede
AGENTS.md                  regole per gli agenti (resta, è di lavoro)
MEMORIA_PROGETTO.md        memoria (resta, accorciata: solo stato e decisioni vive)
mappa_torino.html, simulazione.html
docs/
  METODO.md                dati, area, etichette, motore di accessibilità, colori: una pagina
  FONTI_DATI.md            fonti e licenze (ripulita dalle note di lavoro)
  R1_servizi.md            uno per risultato: domanda, metodo, criteri, numeri, limiti, come rifarlo
  R4_puntualita.md
  R6_parcheggi.md
  R8_traffico.md
  R2_metro_notte.md        in pausa: tenuto corto
  piani/                   piani di lavoro aperti (questo, mappa, risultati, schede, costi)
  rapporti/                i RAPPORTO_*.txt che gli script di oggi riscrivono
scripts/                   solo gli script della catena attuale + comuni.py; .bat ridotti
```

## Passi (in ordine)

| # | Passo | Dettagli | Quanto |
|---|---|---|---|
| 1 | **Cancellare `docs/archivio/`** (75 file) | Tutta la cartella. È solo storia. | piccolo |
| 2 | **Cancellare gli esiti** `docs/ESITO_*.md` (13 file) | Prima: controllare che ogni numero ancora usato sia nel documento del risultato (passo 4). | piccolo |
| 3 | **Cancellare i piani chiusi**: `PIANO_GIRO1_RITOCCHI.md`, `PIANO_PULIZIA.md` | Il contenuto vivo è nella memoria. | piccolo |
| 4 | **Un documento per risultato** (`docs/R1_servizi.md` …) dai `PIANO_RISULTATO*.md` | Si tiene solo lo stato finale: domanda, criteri (tabella), numeri, limiti, script e comando per rifarlo. Via commenti, «giri», prompt, storia. Massimo ~2 pagine. Poi si cancellano i `PIANO_RISULTATO*.md`. | medio |
| 5 | **`docs/METODO.md`** da `PIANO_ACCESSIBILITA.md`, standard tecnici della memoria e parti comuni | Una pagina; `PIANO_ACCESSIBILITA.md` poi si cancella (aggiornare il rimando nello script 18). | piccolo |
| 6 | **Rapporti in `docs/rapporti/`** | Spostare solo i rapporti scritti da script ancora in uso; nei ~40 script cambiare il percorso di uscita (`docs/RAPPORTO_` → `docs/rapporti/RAPPORTO_`). Cancellare quelli senza script vivo: `RAPPORTO_ACCESSIBILITA_NOTTE15/30.txt` (R2, si rigenerano), `RAPPORTO_IMQ.txt`, `RAPPORTO_VELOCITA_5T_prima_fetch.txt`, i rapporti delle versioni superate del traffico (`TRAFFICO_AB`, `TRAFFICO_C`, `_V2`, `_V3`, `_SEGMENTI`, `_VALIDAZIONE`, `RISULTATO8_TRAFFICO_TP.txt` v1), i rapporti di prova del R4 (`R4_GPS_PROVA`, `R4_VERIFICA_GPS`) e `R6_PROPOSTA_FERMATE`. | medio |
| 7 | **Documenti personali**: `CONOSCENZA_TORINO_LEO.md` → dentro `R8_traffico.md` come «controllo di buon senso» (anonimo); `RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md` → `docs/rapporti/` (lo citano 27 e 32) | | piccolo |
| 8 | **Script superati**: cancellare `scripts/archivio/`; spostare le prove chiuse (90, 91 se il R4 non le chiama, 89, 37, 49-50b, 62-63 del modello V3/V4 che non ha migliorato) **solo dopo** aver controllato con `grep` che nessuno script vivo le importi o ne legga le uscite (la memoria avvisa: 77 e 80 servono, le uscite delle fasi 3-4 sono lette dalla Fase 5). Rinumerare **no**: i numeri compaiono nei documenti. | medio |
| 9 | **`.bat`**: tenerne pochi con nomi chiari (`RACCOLTA_GIORNALIERA`, `INSTALLA_…`, `CONTROLLA_LEOPI`, `RIFAI_R1/R4/R6/R8`, `RIFAI_MAPPA_E_SCHEDE`); gli altri si cancellano o finiscono dentro questi. | piccolo |
| 10 | **Rumore nel codice visibile**: commenti `[R6]`, `[pulizia]`, `[revisione 18/10]`, date nei testi delle pagine (12 date nel template della mappa). Nel codice i commenti utili restano, senza date e senza «Leo». | piccolo |
| 11 | **README**: riscritto alla fine (dopo `PIANO_SCHEDE.md`): cosa è, due link, 4 risultati con una riga e un'immagine ciascuno, fonti, licenze, come rifare. Senza date di sviluppo e senza nomi. | piccolo |
| 12 | **Memoria**: accorciata (stato attuale, decisioni vive, prossimi passi); i dettagli vanno nei documenti dei risultati. | piccolo |
| 13 | **`mappa_torino.html` in git (13,6 MB a ogni giro)**: con la pubblicazione su GitHub Pages si toglie dal ramo principale (va solo in `gh-pages`), si aggiunge a `.gitignore`. | piccolo |

## Regole
- Si lavora nel cloud o sul PC indifferentemente (sono solo file di testo e percorsi). Dopo il passo 6 e 8 sul PC:
  rilanciare le catene (`RIFAI_*`) e `prova_pagine_r6.py` per essere sicuri che nessun percorso sia rotto.
- Ogni passo un commit. Prima di cancellare un documento: `grep -r "<nome file>" scripts docs *.md` per trovare chi
  lo cita.
