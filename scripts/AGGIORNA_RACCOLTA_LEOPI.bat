@echo off
rem AGGIORNA_RACCOLTA_LEOPI.bat - porta sul Raspberry Pi la versione di scripts\03_raccolta_continua.py
rem che c'e' sul PC e riavvia la raccolta. Unisce i due .bat di prima (aggiorna_raccolta_leopi.bat del 14/10 e
rem AGGIORNA_RACCOLTA_5T_CODICI.bat del 17/10, ora in scripts\archivio).
rem Doppio clic. Se il Pi chiede la password di sudo, scrivila e premi Invio. Log in logs\aggiorna_raccolta_leopi.log
rem
rem Per tornare indietro: sul Pi, "cp ~/GTT/scripts/03_raccolta_continua.py.bak_<data> ~/GTT/scripts/03_raccolta_continua.py"
rem e "sudo systemctl restart gtt-raccolta" (il nome esatto della copia e' scritto nel log).

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\aggiorna_raccolta_leopi.log"
set "PI=leopi@192.168.8.200"
set "CHIAVE=%USERPROFILE%\.ssh\id_gtt_leopi"
set "OPZ=-i "%CHIAVE%" -o ConnectTimeout=10"
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmm"') do set "QUANDO=%%d"
set "COPIA=03_raccolta_continua.py.bak_%QUANDO%"

echo === %date% %time% === > "%LOG%"

echo [1/5] Copia di sicurezza dello script vecchio sul Pi (%COPIA%)...
ssh %OPZ% %PI% "cp ~/GTT/scripts/03_raccolta_continua.py ~/GTT/scripts/%COPIA% && echo copia fatta: %COPIA%" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [2/5] Invio dello script nuovo...
scp -q %OPZ% scripts\03_raccolta_continua.py %PI%:GTT/scripts/03_raccolta_continua.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
ssh %OPZ% %PI% "python3 -m py_compile ~/GTT/scripts/03_raccolta_continua.py && echo script ok" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [3/5] Riavvio della raccolta (puo' chiedere la password di sudo)...
ssh -t %OPZ% %PI% "sudo systemctl restart gtt-raccolta"
if errorlevel 1 goto errore

echo [4/5] Attendo 6 minuti (serve un giro completo del feed 5T, uno ogni 5 minuti)...
timeout /t 360 /nobreak > nul
ssh %OPZ% %PI% "systemctl is-active gtt-raccolta" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [5/5] Controllo che arrivino parcheggi, ZTL e sensori del traffico...
ssh %OPZ% %PI% "python3 -" < scripts\controlla_raccolta_pk.py >> "%LOG%" 2>&1
ssh %OPZ% %PI% "python3 -" < scripts\controlla_raccolta_5t.py >> "%LOG%" 2>&1

type "%LOG%"
echo.
echo ============================================================
echo  FATTO. Cosa devi vedere nel log:
echo    active
echo    parcheggi: 41 o piu   ztl: 1 o piu   (ultima lettura di pochi minuti fa)
echo    sensori nell'ultimo istante: 112   e   codici ~2 con dati: 3/3
echo  Se leggi "NON ancora 112": aspetta 10 minuti e rilancia questo .bat
echo  (non fa danni: rimanda lo stesso script).
echo ============================================================
pause
exit /b 0

:errore
type "%LOG%"
echo.
echo ERRORE: qualcosa non e' andato. Il log e' in %LOG% - mandalo a Claude.
pause
exit /b 1
