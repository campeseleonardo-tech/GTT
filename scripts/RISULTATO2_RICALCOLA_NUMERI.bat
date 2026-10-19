@echo off
rem RISULTATO2_RICALCOLA_NUMERI.bat - ricalcola SOLO i numeri finali del Risultato 2
rem (script 29 v2), senza rifare i giri R5 (quelli di oggi restano validi).
rem Dura pochi secondi: nessun avviso RAM da seguire, va bene lanciarla anche dentro opencode.
setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs

echo Ricalcolo i numeri del Risultato 2 (metrica v2: qualsiasi aumento, nessuna soglia)...
python scripts\29_risultato2_metro_notte.py > logs\29_risultato2_metro_notte.log 2>&1
if errorlevel 1 goto errore

echo.
echo FATTO. Controlla:
echo   data\processed\risultato2_metro_notte.json
echo   data\processed\risultato2_riepilogo_mappa.json
echo   docs\RAPPORTO_RISULTATO2_METRO_NOTTE.txt
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause > nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude il log dentro logs\.
pause
exit /b 1
