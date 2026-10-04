@echo off
REM Avvia la raccolta continua (lascia questa finestra aperta; Ctrl+C per fermare).
REM Doppio clic per partire. Il PC deve restare acceso e NON andare in stop.
cd /d "%~dp0scripts"
:giro
python 03_raccolta_continua.py
echo Raccolta interrotta, riparto tra 30 secondi (chiudi la finestra per fermarla)...
timeout /t 30 >nul
goto giro
