@echo off
rem PI_UN_SOLO_PROCESSO.bat - doppio clic, UNA volta sola (20/10/2026).
rem Sul Raspberry Pi tutta la raccolta passa sotto un solo servizio (gtt-raccolta): il supervisore tiene accesi
rem sia 03_raccolta_continua.py (mezzi, 5T, parcheggi, ZTL) sia 12_ritardi_gtt.py (ritardi e avvisi GTT).
rem Il vecchio servizio separato dei ritardi (gtt-ritardi) viene fermato e disattivato.
rem Se il Pi chiede la password di sudo, scrivila e premi Invio. Log in logs\pi_un_solo_processo.log
rem
rem Per tornare indietro (sul Pi):
rem   cp ~/GTT/scripts/supervisore.py.bak_<data> ~/GTT/scripts/supervisore.py   (il nome esatto e' nel log)
rem   sudo systemctl enable --now gtt-ritardi ; sudo systemctl restart gtt-raccolta

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\pi_un_solo_processo.log"
set "PI=leopi@192.168.8.200"
set "CHIAVE=%USERPROFILE%\.ssh\id_gtt_leopi"
set "OPZ=-i "%CHIAVE%" -o ConnectTimeout=10"
for /f %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmm"') do set "QUANDO=%%d"
set "COPIA=supervisore.py.bak_%QUANDO%"

echo === %date% %time% === > "%LOG%"

echo [1/6] Controllo che sul Pi ci sia lo script dei ritardi...
ssh %OPZ% %PI% "test -f ~/GTT/scripts/12_ritardi_gtt.py && echo 12_ritardi_gtt.py presente" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [2/6] Copia di sicurezza del supervisore sul Pi (%COPIA%)...
ssh %OPZ% %PI% "cp ~/GTT/scripts/supervisore.py ~/GTT/scripts/%COPIA% && echo copia fatta: %COPIA%" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [3/6] Invio del supervisore nuovo...
scp -q %OPZ% scripts\supervisore.py %PI%:GTT/scripts/supervisore.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
ssh %OPZ% %PI% "python3 -m py_compile ~/GTT/scripts/supervisore.py && echo supervisore ok" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [4/6] Fermo il vecchio servizio dei ritardi e riavvio la raccolta (puo' chiedere la password di sudo)...
ssh -t %OPZ% %PI% "sudo systemctl disable --now gtt-ritardi; sudo systemctl restart gtt-raccolta"
if errorlevel 1 goto errore

echo [5/6] Attendo 2 minuti e controllo i processi...
timeout /t 120 /nobreak > nul
ssh %OPZ% %PI% "echo raccolta: $(systemctl is-active gtt-raccolta); echo vecchio servizio ritardi: $(systemctl is-active gtt-ritardi) / $(systemctl is-enabled gtt-ritardi 2>/dev/null); echo processi 03: $(pgrep -fc '[0]3_raccolta_continua.py'); echo processi 12: $(pgrep -fc '[1]2_ritardi_gtt.py raccogli-db')" >> "%LOG%" 2>&1

echo [6/6] Controllo che arrivino i dati...
python scripts\controlla_leopi.py >> "%LOG%" 2>&1

type "%LOG%"
echo.
echo ============================================================
echo  FATTO. Cosa devi vedere nel log qui sopra:
echo    raccolta: active
echo    vecchio servizio ritardi: inactive / disabled
echo    processi 03: 1      processi 12: 1
echo    Raccolta su leopi ...: OK   (di notte, 00-06, i ritardi non contano)
echo  Se vedi "processi 12: 2" o un ALLARME, manda il log a Claude.
echo ============================================================
pause
exit /b 0

:errore
type "%LOG%"
echo.
echo ERRORE: qualcosa non e' andato. Il log e' in %LOG% - mandalo a Claude.
pause
exit /b 1
