# Esito L4b — snapshot della copia fuori da /tmp (23/10/2026)

## Chiusura di L4 (passo 0)
Letti `logs\raccolta_giornaliera.log`, `logs\backup_da_leopi.log`; lanciato `controlla_leopi.py` (sola lettura). Leo ha già fatto i 3 doppi clic di ESITO_L4:
- GTFS archiviato sul Pi: sì (`data/gtfs/gtt_gtfs_20261023.zip`, 20 MB; il controllo dice «versione del 23/10/2026, valido fino al 31/01/2027, mancano 100 giorni»);
- copia con «ieri»: sì (`data\storico_backup_ieri.sqlite`, 2,84 GB, accanto a `storico_backup.sqlite`, 2,95 GB);
- zip in `data\gtfs_archivio\`: **no, la cartella era vuota. Difetto mio nel `.bat`**: dentro `for /f ('…')` le `=` non fra virgolette di `-o BatchMode=yes` spezzano il comando e ssh rispondeva «no argument after keyword batchmode». Corretto con `-o "BatchMode=yes" -o "ConnectTimeout=20"` (provato con un `.bat` di prova: elenca `gtt_gtfs_20261023.zip`). Basta rilanciare `RACCOLTA_GIORNALIERA.bat`.

## Cosa è cambiato
- `scripts/backup_da_leopi.py`: lo snapshot sul Pi va in `<dir_remota>/data/tmp_copia/gtt_storico_<id>.sqlite`. Il codice remoto (ora la funzione `codice_remoto`) crea la cartella, controlla lo spazio libero contro 1,5 volte il peso di `storico.sqlite` **prima** del backup (se non basta: errore «poco spazio sul Pi … liberi X GB, ne servono Y GB», la copia di prima resta), poi cancella solo i `gtt_storico_*.sqlite` di quella cartella più vecchi di 24 ore. La pulizia finale dello snapshot resta.
- `scripts/controlla_leopi.py`: riga «spazio per lo snapshot (data/tmp_copia)» con ALLARME sotto 1,5 volte lo storico; `/tmp` resta solo come riga informativa; tolto l'AVVISO su `/tmp`.
- `scripts/RACCOLTA_GIORNALIERA.bat`: corretto il passo 3 (vedi sopra).

## Prove
- `python -m pyflakes scripts`: nessuna segnalazione.
- `python scripts\backup_da_leopi.py --prova`: 5 casi di L4 OK + 3 casi nuovi OK sulla parte remota con un SQLite finto (spazio insufficiente con soglia finta: segnalato, nessuno snapshot, nessuna pulizia; snapshot fatto e integro; cancellato solo il resto vecchio, restano il file recente, uno con altro nome e lo snapshot). La parte remota usa `shutil.disk_usage` (stessa cosa di `statvfs` su Linux, e gira anche su Windows per la prova).
- `python scripts\controlla_leopi.py`: «spazio per lo snapshot (data/tmp_copia): 87,4 GB liberi, ne servono 4,1 GB»; codice 0; resta solo l'AVVISO del feed avvisi (errore 500).

## Passo per Leo
Doppio clic su `scripts\RACCOLTA_GIORNALIERA.bat`. Nel log di backup (`logs\backup_da_leopi.log`) deve comparire «Backup verificato»; sul Pi la cartella `data/tmp_copia` esiste (vuota, lo snapshot viene cancellato); l'esito è OK; in `data\gtfs_archivio\` c'è uno zip.
