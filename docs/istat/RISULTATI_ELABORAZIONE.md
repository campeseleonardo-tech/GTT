# Risultati elaborazione matrici pendolarismo ISTAT

## Sintesi
Elaborazione completata dallo script `scripts/07_elabora_matrici_pendolarismo.py` 
in data del [inserire data].

## Fonti elaborate
- Matrice pendolarismo 2011 a livello di sezione di censimento (file ZIP in `docs/`)
- Matrici pendolarismo 2021 (lavoro e studio) a livello di comune (file ZIP in `docs/`)

## Filtro applicato
Sono stati mantenuti solo i record dove l'origine **o** la destinazione appartengono:
- Alla sezione di censimento di Torino o cintura (area entro 18 km dal centro)
  per i dati 2011 (fonte: `data/processed/sezioni_torino.json`)
- Al comune di Torino o cintura (derivato dalle sezioni sopra) per i dati 2021

## Volumi trovati
| Anno | Tipo        | Record totali | Record filtrati | Note |
|------|-------------|---------------|-----------------|------|
| 2011 | Sezione     | [da_verificare] | [da_verificare] | Valori da inserire dopo lo script |
| 2021 | Lavoro      | [da_verificare] | [da_verificare] | Valori da inserire dopo lo script |
| 2021 | Studio      | [da_verificare] | [da_verificare] | Valori da inserire dopo lo script |

## File prodotto
- `data/processed/pendolarismo_torino_cintura.json`: contiene i record filtrati in formato JSON
  con struttura:
  ```json
  {
    "2011": [ { ... record origine/destinazione sezione ... }, ... ],
    "2021": [ { ... record origine/destinazione comune, tipo: lavoro/studio ... }, ... ]
  }
  ```

## Prossimi passi
1. Verificare i volumi prodotti dallo script (sostituire [da_verificare] con i valori reali)
2. Utilizzare questi dati per popolare il livello "Domanda" nella mappa interattiva
3. Aggiornare lo script di generazione mappa (`scripts/04_genera_mappa.py`) per leggere questo file

## Note
- Gli orari/motivi presenti nella matrice 2011 sono mantenuti nei record filtrati.
- Per la matrice 2021, è stato aggiunto il campo "tipo" (lavoro/studio) e "numero_persone".
