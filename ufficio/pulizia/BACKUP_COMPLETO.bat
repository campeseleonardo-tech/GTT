@echo off
rem Backup COMPLETO di Ufficio + progetti in C:\BACKUP_UFFICIO (non modifica e non cancella niente)
cd /d "%~dp0"
python backup_completo.py
echo.
pause
