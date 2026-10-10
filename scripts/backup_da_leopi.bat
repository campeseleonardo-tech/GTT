@echo off
cd /d "%~dp0.."
python scripts\backup_da_leopi.py >> logs\backup_da_leopi.log 2>&1
exit /b %ERRORLEVEL%
