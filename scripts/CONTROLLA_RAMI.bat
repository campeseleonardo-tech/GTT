@echo off
rem CONTROLLA_RAMI.bat - doppio clic: PC e GitHub hanno la stessa versione? Ci sono rami con lavoro non unito? (solo lettura)
rem Log in logs\controlla_rami.log
cd /d "%~dp0.."
if not exist logs mkdir logs
python scripts\controlla_rami.py > logs\controlla_rami.log 2>&1
type logs\controlla_rami.log
echo.
pause
