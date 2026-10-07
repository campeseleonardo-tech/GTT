@echo off
REM Attiva git nella cartella GTT (una volta sola). Serve agli agenti dell Ufficio.
cd /d "%~dp0"
if exist ".git" (
  echo Git e' gia' attivo in questa cartella: niente da fare.
  pause
  exit /b
)
set ID=
git config user.name >nul 2>&1 || set ID=-c user.name=Leo -c user.email=leo@local
git init -b main
git add -A
git %ID% commit -q -m "Stato iniziale GTT (prima degli agenti)"
echo.
echo File salvati in git:
git ls-files
echo.
echo Fatto. Puoi chiudere questa finestra.
pause
