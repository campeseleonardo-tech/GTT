@echo off
rem RAPPORTO_1_ESTRAI.bat - passo 1: legge il PDF e ne estrae il testo (0 token, veloce).
rem Doppio clic dalla radice del progetto. Gira in QUESTA finestra: NON chiuderla.
rem Log: logs\30_rapporto_estrai.log
chcp 65001 >nul
setlocal
cd /d "%~dp0"
if not exist logs mkdir logs

echo Passo 1: estraggo il testo dal PDF del rapporto GTT 2025...
echo (nessuna chiamata al modello: e' veloce, pochi secondi)
echo.
python scripts\30_rapporto_estrai.py > logs\30_rapporto_estrai.log 2>&1
if errorlevel 1 goto errore

echo ------------------ RIEPILOGO ------------------
type logs\30_rapporto_estrai.log
echo ----------------------------------------------
echo.
echo FATTO. Controlla in alto: "Pagine tenute" (atteso circa 151) e
echo il testo della "pagina PDF 30 (stampata 28)" con i passeggeri per mezzo.
echo Il file e' data\processed\rapporto_gtt\pagine.json
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause >nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude il file logs\30_rapporto_estrai.log
echo.
pause
exit /b 1
