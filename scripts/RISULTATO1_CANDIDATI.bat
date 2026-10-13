@echo off
setlocal
cd /d "%~dp0.."
REM Script 22, fase B: dove aggiungere un servizio (salute e scuole, solo Torino).
REM Fa un giro R5 piccolo (pochi minuti, non ore): origini tutta Torino, destinazioni
REM solo le zone candidate.
if not exist logs mkdir logs
echo Avvio risultato 1, fase B (candidati salute + scuole)...
python scripts/22_risultato1_candidati.py --gruppi salute,scuole > logs\risultato1_candidati.log 2>&1
echo Codice di uscita: %errorlevel%
echo Fatto (o fallito: vedi sopra). Controlla sempre anche logs\risultato1_candidati.log
echo.
type logs\risultato1_candidati.log
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
PAUSE > nul
