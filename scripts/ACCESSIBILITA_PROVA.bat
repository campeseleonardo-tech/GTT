@echo off
setlocal
cd /d "%~dp0.."
REM Script 18: accessibilita' PROVA (campione di 200 sezioni, ~15-30 min)
REM Parametri: --campione 200 --lotto-piedi 100 --lotto-tp 20 --salva-tappe
REM Serve Python 3.14 nel PATH. NON usare Anaconda.
REM Se si interrompe e si rilancia, i lotti gia' salvati non vengono ricalcolati.
echo Avvio prova accessibilita' (campione 200)...
python scripts/18_accessibilita.py --campione 200 --lotto-piedi 100 --lotto-tp 20 --salva-tappe --velocita-piedi 80 --velocita-tp 4.8
echo Fatto. Controlli poi: docs/RAPPORTO_ACCESSIBILITA.txt e data/processed/accessibilita.json
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
PAUSE > nul
