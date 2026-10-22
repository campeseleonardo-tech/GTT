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
rem Dati di accesso al Pi: da config_locale.json (vedi scripts\config_locale.esempio.json)
set "PI="
for /f "delims=" %%a in ('python scripts\config_locale.py pi') do set "PI=%%a"
for /f "delims=" %%a in ('python scripts\config_locale.py chiave') do set "CHIAVE=%%a"
for /f "delims=" %%a in ('python scripts\config_locale.py dir_remota') do set "DIRPI=%%a"
if not defined PI (
  echo.
  echo Manca o non e' valido config_locale.json: copia scripts\config_locale.esempio.json in config_locale.json
  echo nella cartella del progetto e scrivi i valori veri. Poi rilancia.
  pause
  exit /b 1
)
set "SRC=%DIRPI%/data"
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
