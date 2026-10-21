@echo off
rem R1_PIEDI_5_10.bat - accessibilita' a PIEDI a 10 e a 5 minuti (solo piedi, niente mezzi pubblici), tutte le sezioni.
rem Doppio clic. Gira in questa finestra: NON chiuderla. Non tocca accessibilita.json (uscite separate).
rem Passi: 0) prova su 200 sezioni  1) 10 minuti  2) 5 minuti.
rem Prima di ogni lancio cancella data\processed\accessibilita_parziale (i parziali di un lancio non servono all'altro).
rem Se un lancio si interrompe con un errore, riparte da solo dopo 60 secondi (max 10 volte) dai lotti salvati.
rem Log: logs\R1_piedi_5_10.log

setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\R1_piedi_5_10.log"

echo.
echo === PASSO 0: prova su 200 sezioni (10 minuti) - %date% %time% ===
echo === PASSO 0: prova su 200 sezioni - %date% %time% === >> "%LOG%"
if exist data\processed\accessibilita_parziale rmdir /s /q data\processed\accessibilita_parziale
powershell -NoProfile -Command "python -u scripts\18_accessibilita.py --solo-piedi --cutoff-piedi 10 --campione 200 --out accessibilita_prova200 2>&1 | Tee-Object -FilePath '%LOG%' -Append; exit $LASTEXITCODE"
if errorlevel 1 goto errore
echo.
echo Prova fatta. Apri docs\rapporti\RAPPORTO_ACCESSIBILITA_PROVA200.txt: deve dire "sezioni: 200" (circa),
echo "TP: non calcolato" e mediane a piedi sensate (scuole, salute, negozi, fermate, verde sotto quelle a 15 minuti).
echo Se va bene premi un tasto per lanciare il calcolo vero (10 minuti poi 5 minuti); se no chiudi la finestra.
pause

set "PASSO=10"
call :lancia 10
if errorlevel 1 goto errore
call :lancia 5
if errorlevel 1 goto errore

echo.
echo FATTO. Devono esserci data\processed\accessibilita_piedi10.json e accessibilita_piedi5.json
echo e i rapporti docs\rapporti\RAPPORTO_ACCESSIBILITA_PIEDI10.txt e _PIEDI5.txt (sezioni: 8317, "TP: non calcolato").
echo Poi avvisa Claude: si lancia python scripts\21_risultato1_vuoti.py.
pause
exit /b 0

:lancia
rem %1 = minuti a piedi
set /a TENTATIVO=0
if exist data\processed\accessibilita_parziale rmdir /s /q data\processed\accessibilita_parziale
:giro
set /a TENTATIVO+=1
echo.
echo === A piedi %1 minuti, tentativo %TENTATIVO% - %date% %time% ===
echo === A piedi %1 minuti, tentativo %TENTATIVO% - %date% %time% === >> "%LOG%"
powershell -NoProfile -Command "python -u scripts\18_accessibilita.py --solo-piedi --cutoff-piedi %1 --out data/processed/accessibilita_piedi%1.json --salva-tappe 2>&1 | Tee-Object -FilePath '%LOG%' -Append; exit $LASTEXITCODE"
if not errorlevel 1 exit /b 0
if %TENTATIVO% GEQ 10 exit /b 1
echo Interrotto con codice %errorlevel%, riparto tra 60 secondi... (chiudi la finestra per fermare)
timeout /t 60 /nobreak > nul
goto giro

:errore
echo.
echo ERRORE: il calcolo si e' fermato. Manda a Claude il file %LOG%.
pause
exit /b 1
