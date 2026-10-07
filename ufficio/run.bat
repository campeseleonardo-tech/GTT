@echo off
rem Apre l Ufficio senza finestra nera (dopo INSTALLA_UFFICIO). Se Ufficio.vbs non esiste ancora, usa il vecchio modo.
if exist "%~dp0Ufficio.vbs" (
  start "" wscript "%~dp0Ufficio.vbs"
  exit /b
)
cd /d "%~dp0pannello"
python pannello_server.py
pause
