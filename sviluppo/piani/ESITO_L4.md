# Esito L4 — raccolta del Pi più sicura (23/10/2026)

Fatti i passi 1, 2a e 3 di `PIANO_RACCOLTA.md`. Le soglie sono quelle del blocco L4, scritte come costanti in testa agli script (non cambiate).
Non ho lanciato `backup_da_leopi.py` né `RACCOLTA_GIORNALIERA.bat` (scrivono `data\storico_backup.sqlite`); verso il Pi ho fatto solo `controlla_leopi.py` (sola lettura).

## Cosa è cambiato

1. **Copia che non perde dati** (`scripts/backup_da_leopi.py`, `scripts/RACCOLTA_GIORNALIERA.bat`)
   - `decidi(riepilogo_vecchio, riepilogo_nuovo)` è una funzione pura: per ogni tabella già nella copia vecchia, righe nuove ≥ vecchie; per `mezzi_gtt` e `flussi_5t` anche primo istante uguale e ultimo ≥ vecchio.
   - Se la regola non passa: la vecchia resta, la nuova va in `data\storico_backup_SOSPETTO.sqlite`, il programma esce col codice 3 e il `.bat` scrive ALLARME (testo del blocco L4).
   - Se passa: la vecchia diventa `storico_backup_ieri.sqlite`. Con meno di 1,2 volte la copia nuova di spazio libero sul PC la copia «ieri» salta con un AVVISO (la copia non si ferma mai per questo).
   - `--prova`: 5 casi su due SQLite finti, tutti OK (nuova più grande, meno righe, vuota, primo istante diverso, nessuna copia vecchia).
   - Descrizione corretta («ogni giorno») e motivo delle regole in testa al file. `gtfs_versioni` aggiunta a `TABELLE`.
   - `_ieri` e `_SOSPETTO` sono fuori da git (`*.sqlite`), scritti in `docs/DATI.md`.
2. **Archivio del GTFS sul Pi** (`scripts/03_raccolta_continua.py`)
   - `giro_gtfs`: una volta al giorno (anche all'avvio) scarica `gtt_gtfs.zip`, controlla che sia uno zip con `stops.txt`, `trips.txt`, `stop_times.txt` e `calendar.txt` o `calendar_dates.txt`; se l'hash è nuovo salva `data/gtfs/gtt_gtfs_AAAAMMGG.zip` (`_2` se esiste) e una riga in `gtfs_versioni` (validità da `feed_info.txt`, altrimenti da `calendar` e `calendar_dates`). Errore → `registra_errore(con, "GTFS", …)`, la raccolta continua. Ogni giorno una riga nel log: «GTFS: invariato» o «versione nuova salvata».
   - `RACCOLTA_GIORNALIERA.bat` ha un passo nuovo (3/4): copia in `data\gtfs_archivio\` solo gli zip del Pi che sul PC mancano (ssh `ls` + scp, sola lettura). Cartella fuori da git, scritta in `docs/DATI.md`.
   - `scripts/prove/prova_gtfs_archivio.py`: 8 controlli OK (prima versione, validità, stessa versione ignorata, nuova versione, `feed_info`, due file, zip rotto, zip incompleto). È entrata anche nel controllo di GitHub, insieme a `backup_da_leopi.py --prova`.
3. **Controllo più completo** (`scripts/controlla_leopi.py`): spazio libero, `/tmp` (spazio e tipo), peso e crescita dello storico, GTFS con giorni alla scadenza, feed avvisi. ALLARME cambia il codice di uscita, AVVISO solo righe.

## Righe del controllo (lanciato davvero, 23/10 20:59)

```
Raccolta su leopi, 23/10/2026 20:59: OK (3 avvisi)
  spazio libero sul Pi: 87.1 GB
  /tmp del Pi: 3.9 GB liberi, tipo tmpfs
  storico sul Pi: 2.7 GB (crescita: serve un lancio di almeno 6 ore fa)
  GTFS: archivio senza versioni (tabella assente)
  feed avvisi GTT: ultima riga vista 21/10 12:40; ore con errore nelle ultime 24: 24
  AVVISO: /tmp ha 3.9 GB, meno di 1.5 volte lo storico (2.7 GB): lo snapshot della copia puo' fallire
  AVVISO: archivio GTFS non attivo o vuoto: il raccoglitore del Pi non l'ha ancora scaricato
  AVVISO: feed avvisi GTT in errore per tutte le ultime 24 ore (ultimo: HTTPError 500: Internal Server Error)
```

Cose scoperte:
- **`/tmp` del Pi è in memoria (tmpfs) con 3,9 GB liberi.** Oggi lo snapshot (2,7 GB) ci sta; con la crescita di ~190 MB al giorno non ci starà più fra circa 6 giorni. Serve il passo 4 di `PIANO_RACCOLTA.md` (snapshot in una cartella del disco, 87 GB liberi) **prima** di allora, altrimenti la copia comincia a fallire (fallisce in modo pulito: ERRORE, la copia di prima resta).
- Il feed degli avvisi GTT risponde 500 da giorni (ultima riga vista il 21/10): AVVISO giusto, e gli avvisi non servono a nessun risultato.
- Spazio sul Pi: 87 GB, nessun problema.

Due regole le ho dovute interpretare, dove i dati non bastavano:
- «Ultimo scaricamento riuscito più vecchio di 3 giorni»: la tabella `gtfs_versioni` registra solo le versioni *cambiate*, non i tentativi riusciti. Uso invece: errore GTFS in ognuno degli ultimi 3 giorni → AVVISO. Se il GTFS è invariato per mesi, non c'è falso avviso.
- Crescita in MB al giorno: si calcola solo se il lancio precedente salvato è di almeno 6 ore fa (altrimenti due lanci ravvicinati danno numeri senza senso); il primo lancio salva il peso e la crescita compare dal successivo.

## Prove (solo funzionamento)

- `python -m pyflakes scripts`: nessuna segnalazione.
- `python scripts\backup_da_leopi.py --prova`: 5 casi OK.
- `python scripts\prove\prova_gtfs_archivio.py`: OK.
- `python -m py_compile scripts\03_raccolta_continua.py`: OK.
- `python scripts\controlla_leopi.py`: righe nuove stampate, nessuna eccezione, codice 0.

## Passi per Leo, in quest'ordine

1. Doppio clic su `scripts\AGGIORNA_RACCOLTA_LEOPI.bat` (porta il 03 nuovo sul Pi e riavvia; nel log devono comparire «script ok» e «active»).
2. Dopo 5 minuti, doppio clic su `scripts\CONTROLLA_LEOPI.bat`: la riga GTFS deve dire «versione del 23/10/2026» (o la data di oggi).
3. Doppio clic su `scripts\RACCOLTA_GIORNALIERA.bat`: esito OK; in `data\` c'è `storico_backup_ieri.sqlite`, in `data\gtfs_archivio\` c'è uno zip.

Dopo: passo 4 del piano (snapshot fuori da `/tmp`) entro pochi giorni; passo 2b (script 27, 70, 97 col GTFS di ogni giorno) quando il Pi ha almeno due versioni.
