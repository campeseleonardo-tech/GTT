@echo off
rem AGGIORNA_RACCOLTA_5T_CODICI.bat - Pacchetto H del Risultato 8 (traffico).
rem Porta sul Raspberry Pi il raccoglitore corretto, che salva TUTTI i 112 sensori
rem fisici 5T (prima ne salvava 109: tre codici erano condivisi da due sensori e
rem il secondo veniva perso). Doppio clic. Se il Pi chiede la password di sudo,
rem scrivila e premi Invio. Log in logs\aggiorna_raccolta_5t_codici.log
rem
rem Per tornare indietro: sul Pi, "cp ~/GTT/scripts/03_raccolta_continua.py.bak_pre_codici
rem ~/GTT/scripts/03_raccolta_continua.py" e "sudo systemctl restart gtt-raccolta".

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\aggiorna_raccolta_5t_codici.log"
set "PI=leopi@192.168.8.200"
set "CHIAVE=%USERPROFILE%\.ssh\id_gtt_leopi"
set "OPZ=-i "%CHIAVE%" -o ConnectTimeout=10"

echo === %date% %time% === > "%LOG%"

echo [1/5] Copia di sicurezza dello script vecchio sul Pi...
ssh %OPZ% %PI% "cp ~/GTT/scripts/03_raccolta_continua.py ~/GTT/scripts/03_raccolta_continua.py.bak_pre_codici && echo copia fatta" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [2/5] Invio dello script nuovo (riconosce i 3 codici condivisi)...
scp -q %OPZ% scripts\03_raccolta_continua.py %PI%:GTT/scripts/03_raccolta_continua.py >> "%LOG%" 2>&1
if errorlevel 1 goto errore
ssh %OPZ% %PI% "python3 -m py_compile ~/GTT/scripts/03_raccolta_continua.py && echo script ok" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [3/5] Riavvio della raccolta (puo' chiedere la password di sudo)...
ssh -t %OPZ% %PI% "sudo systemctl restart gtt-raccolta"
if errorlevel 1 goto errore

echo [4/5] Attendo 6 minuti (serve un giro completo del feed, uno ogni 5 minuti)...
timeout /t 360 /nobreak > nul
ssh %OPZ% %PI% "systemctl is-active gtt-raccolta" >> "%LOG%" 2>&1
if errorlevel 1 goto errore

echo [5/5] Controllo quanti sensori arrivano nell'ultimo istante...
ssh %OPZ% %PI% "python3 -" < scripts\controlla_raccolta_5t.py >> "%LOG%" 2>&1

type "%LOG%"
echo.
echo ============================================================
echo  FATTO. Cosa devi vedere alla fine del log:
echo    active
echo    sensori nell'ultimo istante: 112   (prima erano 109)
echo    codici ~2 con dati: 3/3
echo  Se leggi "NON ancora 112": aspetta 10 minuti e rilancia solo
echo  questo .bat (non fa danni: rimanda lo stesso script).
echo  Per tornare indietro: sul Pi ripristina 03_raccolta_continua.py.bak_pre_codici
echo  e riavvia gtt-raccolta (istruzioni in cima a questo file).
echo ============================================================
pause
exit /b 0

:errore
type "%LOG%"
echo.
echo ERRORE: qualcosa non e' andato. Il log e' in %LOG% - mandalo a Leo/Claude.
pause
exit /b 1
