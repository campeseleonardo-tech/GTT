@echo off
cd /d "%~dp0.."
python scripts\backup_da_leopi.py >> logs\verifica_ritardi_diurna.log 2>&1
if errorlevel 1 exit /b %errorlevel%
python scripts\12_ritardi_gtt.py analizza --db data\storico_backup.sqlite --da-utc 2026-10-11T06:00:00+00:00 --a-utc 2026-10-11T18:00:00+00:00 >> logs\verifica_ritardi_diurna.log 2>&1
exit /b %errorlevel%
