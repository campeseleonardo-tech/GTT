@echo off
setlocal
cd /d "%~dp0.."
REM Script 21, fase A: dove mancano i servizi essenziali (nessun calcolo R5, solo lettura
REM di data/processed/accessibilita.json). Veloce: pochi secondi.
echo Avvio risultato 1, fase A (vuoti di servizio)...
python scripts/21_risultato1_vuoti.py
echo Fatto. Controlla: docs\RAPPORTO_RISULTATO1.txt e data\processed\risultato1_vuoti.json
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
PAUSE > nul
