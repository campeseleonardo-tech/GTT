@echo off
rem Carica una COPIA di Ufficio + progetti nel repo privato GitHub multiple-agents (gli originali non vengono toccati)
cd /d "%~dp0"
python pubblica_github.py
echo.
pause
