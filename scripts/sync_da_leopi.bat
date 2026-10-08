@echo off
rem sync_da_leopi.bat - riporta al PC i file generati sul Pi per la mappa.
rem
rem Usa la chiave SSH (vedi setup chiave in MEMORIA_PROGETTO); nessuna password.
rem Da pianificare in Windows (Attività pianificate), per es. ogni 5 minuti:
rem   schtasks /create /tn "GTT sync da leopi" /tr "C:\projects\Progetti\GTT\scripts\sync_da_leopi.bat" /sc minute /mo 5 /f
rem
rem Se il nome utente sul Pi e' diverso da "leopi", cambialo sotto (es. pi@...).

set PI=leopi@192.168.8.200
set SRC=/home/leopi/GTT/data
set DEST=C:\projects\Progetti\GTT\data

rem File vivi della mappa (fallisce in silenzio se manca qualcosa: la mappa resta com'e')
scp -q -o BatchMode=yes -o ConnectTimeout=10 "%PI%:%SRC%/live.js" "%PI%:%SRC%/stat.js" "%PI%:%SRC%/agg_cache.json" "%DEST%\" 2>nul
scp -q -o BatchMode=yes -o ConnectTimeout=10 "%PI%:%SRC%/replay_*.js" "%DEST%\" 2>nul

exit /b 0