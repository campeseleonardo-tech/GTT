# Rapporto GT13-altre-citta

## Cosa ho fatto
- Letto `MEMORIA_PROGETTO.md`, `docs/FONTI_DATI.md`, `scripts/04_genera_mappa.py` per identificare tutto ciò che è hardcoded per Torino.
- Scritto `docs/ALTRE_CITTA.md` con le 5 sezioni richieste: specificità Torino (tabella file/funzione), dati necessari per nuova città (tabella), proposta config JSON, piano 8 passi, rischi.

## Cosa ho controllato
- Costanti hardcoded in `04_genera_mappa.py`: URL, prefissi file, PRO_COM_TORINO=1272, PEND_ATTESI, soglie velocità, conversione Gauss-Boaga, parser 5T, fuso orario italiano.
- Riferimenti in `docs/FONTI_DATI.md` per URL e stato verifica.
- Struttura dati restituita da `elabora_gtfs()`, `leggi_zone()`, `calcola_velocita()`, `costruisci_pendolari()` per capire cosa serve replicare.

## Scelte (default reversibili)
- Config in `config/citta/<slug>.json` (cartella nuova, non esistente).
- Parser traffico pluggabile via `scripts/parsers/traffico/<nome>.py`.
- Zone statistiche: strategia per proiezione sorgente (EPSG + funzione conversione) nel config.
- Fuso orario: usare `zoneinfo` (stdlib Python 3.9+) invece di funzioni custom, parametrizzato nel config.
- Template HTML riceve config via `__DATI__` (già usato per passare tutto il JSON).

## Domande per Leo (da decidere)
- Nessuna domanda bloccante: il documento è uno studio, non richiede cambiamenti al codice ora. Le decisioni vere arrivano quando si implementa il passo 1-2.

## Note
- Non ho modificato nessun file esistente (solo creato `docs/ALTRE_CITTA.md` e questo rapporto).
- Il piano è ordinato per non rompere Torino: passi 1-2 sono solo rifattorizzazione interna.
