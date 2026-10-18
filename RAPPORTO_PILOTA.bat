@echo off
rem RAPPORTO_PILOTA.bat - prova piccola e obbligatoria prima del giro completo.
rem Doppio clic dalla radice del progetto. Gira in QUESTA finestra: NON chiuderla.
rem Fa: passo 1 (estrazione testo) e passo 2 SOLO sulle pagine PDF 29-32, poi verifica
rem che i valori attesi del rapporto ci siano tutti, con anno e pagina giusti.
rem Se ne manca anche uno, NON lanciare il giro completo: manda il log a Claude.
chcp 65001 >nul
setlocal
cd /d "%~dp0"
if not exist logs mkdir logs

echo [1/2] Estraggo il testo dal PDF...
python scripts\30_rapporto_estrai.py > logs\30_rapporto_estrai.log 2>&1
if errorlevel 1 goto errore
echo     ok (vedi logs\30_rapporto_estrai.log)
echo.

echo [2/2] Pilota: estraggo i fatti SOLO dalle pagine PDF 29-32 con DeepSeek...
echo.
python scripts\31_rapporto_fatti.py --pagine 29-32 --verifica-attesi > logs\31_rapporto_fatti.log 2>&1
if errorlevel 1 goto errore

echo ------------------ RIEPILOGO DEL PILOTA ------------------
type logs\31_rapporto_fatti.log
echo ---------------------------------------------------------
echo.
echo Guarda la riga finale:
echo   "PILOTA SUPERATO: ..."  -> tutto bene, puoi lanciare RAPPORTO_2_FATTI.bat
echo   "PILOTA FALLITO: ..."   -> NON andare avanti, manda il log a Claude
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause >nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude i log dentro logs\.
echo (se dice "manca il file chiave_deepseek.txt", il problema e' solo la chiave).
echo.
pause
exit /b 1
