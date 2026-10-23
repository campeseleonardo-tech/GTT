@echo off
rem AREA_TEMPI.bat - tempi da Piazza Castello per la scheda 4 («area che si espande»): prima una prova su 200 sezioni, poi il calcolo vero, poi schede e prova delle pagine.
rem Doppio clic. Si ferma al primo errore. Log in logs\area_tempi.log
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\area_tempi.log"
echo === %date% %time% === > "%LOG%"
echo --- 99 prova su 200 sezioni --- >> "%LOG%"
python scripts\99_area_tempi.py --prova 200 >> "%LOG%" 2>&1
if errorlevel 1 goto errore
echo --- 99 tutte le sezioni --- >> "%LOG%"
python scripts\99_area_tempi.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
echo --- schede_risultati --- >> "%LOG%"
python scripts\schede_risultati.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
echo --- prova_pagine --- >> "%LOG%"
python scripts\prova_pagine.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
echo.
echo FATTO. Gli AVVISI sono nel log: cerca la parola AVVISO in %LOG%
findstr /c:"AVVISO" "%LOG%"
pause
exit /b 0
:errore
echo ERRORE - mi fermo. Guarda la fine di %LOG%
pause
exit /b 1
