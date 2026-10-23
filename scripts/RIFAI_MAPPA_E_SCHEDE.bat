@echo off
rem RIFAI_MAPPA_E_SCHEDE.bat - rigenera la mappa e le schede dai dati gia' calcolati, in ordine.
rem Doppio clic. Si ferma al primo errore. Log in logs\rifai_mappa_e_schede.log
rem Ordine: 04 mappa (mappa_torino.html), schede_risultati (data\schede_risultati.js), 86 controllo dei file caricati dalle pagine,
rem prova_pagine (errori JavaScript nelle pagine: atteso 0).
rem Non ricalcola nessun risultato: per quello, prima, la catena del risultato (es. RISULTATO6_RIFAI.bat).
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\rifai_mappa_e_schede.log"
echo === %date% %time% === > "%LOG%"
for %%S in (04_genera_mappa schede_risultati 86_controlla_file_pagine prova_pagine) do (
  echo --- %%S --- >> "%LOG%"
  echo [%time%] %%S
  python scripts\%%S.py >> "%LOG%" 2>&1
  if errorlevel 1 (
    echo ERRORE in %%S - mi fermo. Guarda la fine di %LOG%
    echo ERRORE in %%S >> "%LOG%"
    pause
    exit /b 1
  )
)
echo.
echo FATTO. Gli AVVISI sono nel log: cerca la parola AVVISO in %LOG%
findstr /c:"AVVISO" "%LOG%"
pause
exit /b 0
