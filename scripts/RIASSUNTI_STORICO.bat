@echo off
rem RIASSUNTI_STORICO.bat - riassume lo storico della raccolta (script 97). Doppio clic; solo lettura sullo storico.
rem Senza argomenti: tutti i mesi nuovi o incompleti. Per un mese solo: RIASSUNTI_STORICO.bat 2026-10
rem Log in logs\riassunti_storico.log. Poi: python scripts\confronta_riassunti.py (stessi numeri?).
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\riassunti_storico.log"
echo === %date% %time% === > "%LOG%"
if "%~1"=="" (
  python scripts\97_riassunti_storico.py >> "%LOG%" 2>&1
) else (
  python scripts\97_riassunti_storico.py --mese %~1 >> "%LOG%" 2>&1
)
if errorlevel 1 (
  echo ERRORE: guarda la fine di %LOG%
  pause
  exit /b 1
)
echo FATTO. Ultime righe del log:
powershell -NoProfile -Command "Get-Content '%LOG%' -Tail 15"
pause
exit /b 0
