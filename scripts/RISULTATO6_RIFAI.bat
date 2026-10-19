@echo off
rem RISULTATO6_RIFAI.bat - rifa tutta la catena del Risultato 6 corretto (20/10/2026), in ordine.
rem Doppio clic. Si ferma al primo errore. Log in logs\risultato6_rifai.log
rem Ordine: 71 riempimento, 72 nodi e zone dei parcheggi, 73 segnali, 81 auto che passano, 82 parcheggi adatti,
rem 83 fermate importanti, 84 risultato, 79 dati per la mappa, 85 verifiche indipendenti, 04 mappa,
rem schede_risultati (simulazione.html), prova_pagine_r6 (errori nelle pagine).
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\risultato6_rifai.log"
echo === %date% %time% === > "%LOG%"
for %%S in (71_parcheggi_riempimento 72_nodi_tp 73_segnali_criticita 81_auto_di_passaggio 82_parcheggi_adatti 83_fermate_importanti 84_risultato6_parcheggi 79_dati_mappa_r6 85_verifiche_correzioni 04_genera_mappa schede_risultati prova_pagine_r6) do (
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
