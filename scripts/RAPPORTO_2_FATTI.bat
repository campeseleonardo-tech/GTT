@echo off
rem RAPPORTO_2_FATTI.bat - passo 2: estrae i fatti dal testo con DeepSeek (giro completo).
rem Doppio clic (sta in scripts\, lavora dalla radice del progetto). Gira in QUESTA finestra: NON chiuderla.
rem Legge la chiave da chiave_deepseek.txt. Salva ogni blocco appena finito: se si
rem interrompe, rilanciandolo riparte da dove era (le cache stanno in
rem data\processed\rapporto_gtt\cache).
rem Log: logs\31_rapporto_fatti.log
chcp 65001 >nul
setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs

echo Passo 2 (GIRO COMPLETO): estraggo i fatti da tutte le pagine con DeepSeek.
echo Sono circa 50 chiamate al modello: puo' durare alcuni minuti.
echo Se si interrompe, rilanciando questo file riparte da dove era.
echo.
python scripts\31_rapporto_fatti.py > logs\31_rapporto_fatti.log 2>&1
if errorlevel 1 goto errore

echo ------------------ RIEPILOGO ------------------
type logs\31_rapporto_fatti.log
echo ----------------------------------------------
echo.
echo FATTO. Controlla in fondo: "Fatti verificati (unici)" e i token usati.
echo Il file e' data\processed\rapporto_gtt\fatti.json
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause >nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude il file logs\31_rapporto_fatti.log
echo (se dice "manca il file chiave_deepseek.txt", il problema e' solo la chiave).
echo.
pause
exit /b 1
