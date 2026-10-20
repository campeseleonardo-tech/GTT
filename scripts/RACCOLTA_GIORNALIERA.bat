@echo off
rem RACCOLTA_GIORNALIERA.bat - porta sul PC TUTTI i dati raccolti dal Raspberry Pi (20/10/2026).
rem Lo lancia da solo Windows una volta al giorno (vedi INSTALLA_RACCOLTA_GIORNALIERA.bat); si puo' anche
rem lanciare a mano con doppio clic. Solo lettura sul Pi.
rem   1) copia verificata dello storico: data\storico_backup.sqlite (tutte le tabelle)
rem   2) file della mappa preparati dal Pi: data\stat.js, live.js, agg_cache.json, replay_*.js
rem   3) controllo che la raccolta stia funzionando; se no, una finestra di avviso
rem Le analisi (velocita' 5T, traffico, Risultato 6...) NON partono da sole: si lanciano a mano quando servono.
rem Log: logs\raccolta_giornaliera.log (una riga di esito per giorno) e logs\backup_da_leopi.log

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\raccolta_giornaliera.log"
set "PI=leopi@192.168.8.200"
set "SRC=/home/leopi/GTT/data"
set "CHIAVE=%USERPROFILE%\.ssh\id_gtt_leopi"
set "ESITO=OK"

echo [%date% %time%] inizio >> "%LOG%"

echo [1/3] Copio lo storico dal Pi (qualche minuto)...
python scripts\backup_da_leopi.py >> logs\backup_da_leopi.log 2>&1
if errorlevel 1 set "ESITO=ERRORE nella copia dello storico - vedi logs\backup_da_leopi.log"

echo [2/3] Copio i file della mappa...
scp -q -i "%CHIAVE%" -o BatchMode=yes -o ConnectTimeout=20 "%PI%:%SRC%/live.js" "%PI%:%SRC%/stat.js" "%PI%:%SRC%/agg_cache.json" "%PI%:%SRC%/replay_*.js" data\ >> "%LOG%" 2>&1
if errorlevel 1 if "%ESITO%"=="OK" set "ESITO=ERRORE nella copia dei file della mappa"

echo [3/3] Controllo la raccolta sul Pi...
python scripts\controlla_leopi.py >> "%LOG%" 2>&1
if errorlevel 1 if "%ESITO%"=="OK" set "ESITO=ALLARME: la raccolta sul Pi ha un problema - vedi logs\controlla_leopi.log"

echo [%date% %time%] esito: %ESITO% >> "%LOG%"
echo Esito: %ESITO%
if not "%ESITO%"=="OK" (
  powershell -NoProfile -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('%ESITO%. Guarda logs\raccolta_giornaliera.log e scrivi a Claude.','GTT - raccolta giornaliera') | Out-Null"
  exit /b 1
)
exit /b 0
