@echo off
setlocal
REM Script 18: accessibilita' COMPLETA (tutte le sezioni, giro lungo ~9-10 ore)
REM Lancialo di notte, PC alla corrente, con opencode e programmi pesanti chiusi.
REM Se si interrompe: i file parziali restano, ma al rilancio ricalcola da capo
REM (la ripresa dal lotto salvato va ancora implementata: vedi MEMORIA_PROGETTO.md).
echo Avvio accessibilita' completa (tutte le sezioni)...
python scripts/18_accessibilita.py --lotto-piedi 100 --lotto-tp 20 --salva-tappe --velocita-piedi 80 --velocita-tp 4.8
echo Fatto. Controlli poi: docs/RAPPORTO_ACCESSIBILITA.txt e data/processed/accessibilita.json
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
PAUSE > nul
