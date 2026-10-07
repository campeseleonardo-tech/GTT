# GTT - Mappa interattiva della mobilità di Torino

Progetto personale di studio: una pagina web (HTML) con una mappa di tutta Torino che mostra
domanda e offerta di mezzi, i punti critici e i flussi (misurati dove possibile, simulati altrove),
il più vicino possibile agli orari reali.

Leggi prima `MEMORIA_PROGETTO.md` (decisioni, limiti, cose da fare).

## Cartelle

- `scripts/`  gli script Python (solo libreria standard, tranne dove indicato)
- `data/raw/`  i file scaricati (non vanno modificati a mano)
- `data/storico.sqlite`  l'archivio che si riempie con la raccolta continua (nasce da solo)
- `docs/`  fonti dati, bozze di richieste, rapporti

## Cosa fare ora, in ordine

1. **Scaricare i dati** (fatto una volta il 3/10/2026; da ripetere di giorno per avere un campione diurno; sul PC, da Spyder o dal prompt di Anaconda):
   `python scripts/01_scarica_dati.py`
2. **Controllare cosa contengono**:
   `python scripts/02_ispeziona_dati.py`
   (per i dati GTT in tempo reale serve una volta, nella console di Spyder: `%pip install gtfs-realtime-bindings`)
   Poi incolla qui in chat il contenuto di `docs/RAPPORTO_ISPEZIONE.txt`.
3. **Creare la mappa**: `python scripts/04_genera_mappa.py` e poi apri `mappa_torino.html` con doppio clic
   (ricrea il file con gli ultimi dati scaricati; serve internet solo per lo sfondo della cartina).
4. **Scaricare a mano i dati ISTAT** (vedi `docs/FONTI_DATI.md`, sezione "Da scaricare a mano").
5. **Avviare la raccolta sul Raspberry Pi** quando i punti 1-2 sono andati bene:
   copia la cartella `scripts/` sul Pi e lancia `python3 03_raccolta_continua.py`.
   Prova prima con `--una-volta`.

Nota: gli script individuano da soli la cartella GTT, quindi i dati finiscono sempre in `GTT\\data\\raw`.

## Stato dei test (onesto)

- `01_scarica_dati.py` ha girato sul tuo PC il 3/10/2026: tutti i file scaricati.
- `02_ispeziona_dati.py` ha girato sul tuo PC; la prima versione contava 0 sensori 5T per un errore (schema XML), ora corretto
  e provato sul tuo file vero. `03_raccolta_continua.py` ora salva correttamente i dati 5T del tuo file vero (109 misure);
  la parte dei mezzi GTT resta NON provata.
