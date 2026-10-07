@echo off
rem Rimette il pannello come era prima dell ultima modifica fatta dalla chat.
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (python ripristina.py) else (py ripristina.py)
echo.
pause
