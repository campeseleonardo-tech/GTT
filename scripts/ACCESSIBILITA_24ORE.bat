@echo off
rem ACCESSIBILITA_24ORE.bat - accessibilita' a piedi + TP su 24 fasce orarie (0-23), tutte le sezioni.
rem Doppio clic. Gira in questa finestra (non dentro opencode): NON chiuderla.
rem Se il calcolo si interrompe con un errore, riparte da solo dopo 60 secondi (max 20 volte)
rem e riprende dai lotti gia' salvati in data\processed\accessibilita_parziale.
rem Stessi parametri della run avviata il 14/10: i lotti gia' salvati vengono riusati.
rem Log (in aggiunta): logs\accessibilita_24ore.log

setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\accessibilita_24ore.log"
set "ORE=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23"
set /a TENTATIVO=0

:giro
set /a TENTATIVO+=1
echo.
echo === Tentativo %TENTATIVO% - %date% %time% ===
echo === Tentativo %TENTATIVO% - %date% %time% === >> "%LOG%"
powershell -NoProfile -Command "python -u scripts\18_accessibilita.py --giorno 2026-10-12 --ore %ORE% --lotto-piedi 100 --lotto-tp 20 --salva-tappe --velocita-piedi 80 --velocita-tp 4.8 2>&1 | Tee-Object -FilePath '%LOG%' -Append; exit $LASTEXITCODE"
if not errorlevel 1 goto fatto

if %TENTATIVO% GEQ 20 goto arreso
echo.
echo Calcolo interrotto (codice %errorlevel%). Riparto tra 60 secondi... (chiudi la finestra per fermare)
echo Interrotto con codice %errorlevel%, riparto tra 60 s >> "%LOG%"
timeout /t 60 /nobreak > nul
goto giro

:fatto
echo.
echo FATTO. Controlla docs\RAPPORTO_ACCESSIBILITA.txt (deve dire "sezioni: 8317" e 24 ore)
echo e data\processed\accessibilita.json. Poi avvisa Claude.
pause
exit /b 0

:arreso
echo.
echo ERRORE: interrotto 20 volte di fila. Manda a Claude il file %LOG%.
pause
exit /b 1
