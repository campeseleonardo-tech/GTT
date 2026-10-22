@echo off
rem RISULTATO6_RIFAI.bat - rifa tutta la catena del Risultato 6 corretto (20/10/2026), in ordine.
rem Doppio clic. Si ferma al primo errore. Log in logs\risultato6_rifai.log
rem Ordine: 71 riempimento, 72 nodi e zone dei parcheggi, 73 segnali, 81 auto che passano, 88 confronto con i sensori 5T,
rem 82 parcheggi adatti, 87 popolarita delle zone e linee utili, 83 fermate importanti, 84 risultato, 94 bus contro auto (serve aver lanciato il 93 almeno una volta), 79 dati per la mappa, 85 verifiche indipendenti, 04 mappa,
rem schede_risultati (risultati.html), prova_pagine (errori nelle pagine).
cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\risultato6_rifai.log"
echo === %date% %time% === > "%LOG%"
for %%S in (71_parcheggi_riempimento 72_nodi_tp 73_segnali_criticita 81_auto_di_passaggio 88_confronto_auto_sensori 82_parcheggi_adatti 87_popolarita_zone 83_fermate_importanti 84_risultato6_parcheggi 94_r6_bus_contro_auto 79_dati_mappa_r6 85_verifiche_correzioni 04_genera_mappa schede_risultati prova_pagine) do (
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
