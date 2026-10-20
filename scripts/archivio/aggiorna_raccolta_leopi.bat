@echo off
rem aggiorna_raccolta_leopi.bat - porta sul Pi la nuova 03_raccolta_continua.py
rem (aggiunge parcheggi 5T ogni 5 minuti + ZTL una volta al giorno) e riavvia la raccolta.
rem Doppio clic. Se il Pi chiede la password di sudo, scrivila e premi Invio.
rem Log in logs\aggiorna_raccolta_leopi.log

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\aggiorna_raccolta_leopi.log"
set "PI=leopi@192.168.8.200"
set "CHIAVE=%USERPROFILE%\.ssh\id_gtt_leopi"
set "OPZ=-i "%CHIAVE%" -o ConnectTimeout=10"

echo === %date% %time% === > "%LOG%"

echo [1/4] Copia di sicurezza dello script vecchio sul Pi...
ssh %OPZ% %PI% "cp ~/GTT/scripts/03_raccolta_continua.py ~/GTT/scripts/03_raccolta_continua.py.bak_pre_pk && echo copia fatta" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [2/4] Invio dello script nuovo...
scp -q %OPZ% scripts\03_raccolta_continua.py %PI%:GTT/scripts/03_raccolta_continua.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
ssh %OPZ% %PI% "python3 -m py_compile ~/GTT/scripts/03_raccolta_continua.py && echo script ok" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [3/4] Riavvio della raccolta (puo' chiedere la password di sudo)...
ssh -t %OPZ% %PI% "sudo systemctl restart gtt-raccolta"
if errorlevel 1 goto errore

echo [4/4] Attendo 40 secondi e controllo che i parcheggi arrivino...
timeout /t 40 /nobreak > nul
ssh %OPZ% %PI% "systemctl is-active gtt-raccolta" >> "%LOG%" 2>&1
if errorlevel 1 goto errore
ssh %OPZ% %PI% "python3 -" < scripts\controlla_raccolta_pk.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore

type "%LOG%"
echo.
echo FATTO. Devi vedere: active  e  parcheggi: 41  letture: 41 o piu  ztl: 1
pause
exit /b 0

:errore
type "%LOG%"
echo.
echo ERRORE: qualcosa non e' andato. Il log e' in %LOG% - mandalo a Claude.
pause
exit /b 1
