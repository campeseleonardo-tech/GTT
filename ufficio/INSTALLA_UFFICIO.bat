@echo off
rem Si lancia UNA volta: crea l icona Ufficio sul desktop e l attivita di Windows UfficioAgenti.
rem Spiegazione riga per riga in INSTALLA_UFFICIO.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0INSTALLA_UFFICIO.ps1"
echo.
pause
