@echo off
rem FETCH_LEOPI_E_VELOCITA_5T.bat - doppio clic.
rem 1) copia lo storico da leopi sul PC (sola lettura sul Pi, copia verificata)
rem 2) tiene una copia dei risultati 5T precedenti
rem 3) ricalcola velocita'/flusso tipici dei sensori 5T (script 26)
rem Il PC deve essere sulla stessa rete di leopi. Lascia il PC libero: ci vogliono alcuni minuti.
rem Log: logs\backup_da_leopi.log e logs\26_velocita_5t.log

cd /d "%~dp0.."
if not exist logs mkdir logs

echo [1/3] Copio lo storico da leopi (alcuni minuti, non chiudere la finestra)...
python scripts\backup_da_leopi.py >> logs\backup_da_leopi.log 2>&1
if errorlevel 1 goto errore
echo      Ultime righe del log del backup:
powershell -NoProfile -Command "Get-Content 'logs\backup_da_leopi.log' -Tail 5"

echo [2/3] Salvo una copia dei risultati 5T precedenti...
if exist data\processed\velocita_5t.json copy /y data\processed\velocita_5t.json data\processed\velocita_5t_prima_fetch.json >nul
if exist docs\RAPPORTO_VELOCITA_5T.txt copy /y docs\RAPPORTO_VELOCITA_5T.txt docs\RAPPORTO_VELOCITA_5T_prima_fetch.txt >nul

echo [3/3] Ricalcolo velocita'/flusso 5T...
python scripts\26_velocita_5t.py > logs\26_velocita_5t.log 2>&1
if errorlevel 1 goto errore
echo      Prime righe del rapporto:
powershell -NoProfile -Command "Get-Content 'docs\RAPPORTO_VELOCITA_5T.txt' -TotalCount 12"

echo.
echo FATTO. Torna da Claude e scrivi "fetch fatto".
pause
exit /b 0

:errore
echo.
echo ERRORE: qualcosa non e' andato. Guarda gli ultime righe in logs\backup_da_leopi.log
echo oppure logs\26_velocita_5t.log e scrivi a Claude "fetch fallito".
pause
exit /b 1
