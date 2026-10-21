@echo off
rem CONTROLLA_LEOPI.bat - doppio clic: la raccolta sul Raspberry Pi sta funzionando? (solo lettura)
rem Log in logs\controlla_leopi.log
cd /d "%~dp0.."
if not exist logs mkdir logs
python scripts\controlla_leopi.py
echo.
pause
