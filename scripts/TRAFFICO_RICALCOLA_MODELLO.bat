@echo off
rem TRAFFICO_RICALCOLA_MODELLO.bat - Risultato 8 (traffico), pacchetto I.
rem Rifa da zero il METODO C: dai viaggi IMQ ai percorsi sulla rete stradale e
rem ai corridoi. Da lanciare SOLO se cambiano la rete OSM, i dati IMQ o le regole:
rem per il normale aggiornamento dei sensori usa TRAFFICO_RILANCIA_SENSORI.bat.
rem
rem ATTENZIONE: e' il giro pesante. Sul PC di Leo dura molte decine di minuti
rem (la rete si costruisce e si instrada una volta per nodo di origine). Il PC
rem deve restare libero. Doppio clic. Log in logs\traffico_ricalcola_modello.log
rem
rem Passi: A (fattibilita' e rete) - B (domanda IMQ) - C (punti e porte) -
rem        D (instradamento) - E (corridoi). Poi, per la taratura e il prodotto,
rem        lancia TRAFFICO_RILANCIA_SENSORI.bat.

cd /d "%~dp0.."
if not exist logs mkdir logs
set "LOG=logs\traffico_ricalcola_modello.log"

echo === %date% %time% === > "%LOG%"
echo ATTENZIONE: questo giro ricalcola tutto il modello e dura a lungo. >> "%LOG%"

call :passo scripts\39_fattibilita_rete.py
call :passo scripts\40_domanda_imq.py
call :passo scripts\41_zone_punti.py
call :passo scripts\42_instradamento.py
call :passo scripts\43_segmenti_corridoi.py

type "%LOG%"
echo.
echo FATTO il modello. Ora lancia TRAFFICO_RILANCIA_SENSORI.bat per taratura e prodotto.
pause
exit /b 0

:passo
echo. >> "%LOG%"
echo --- %~1 --- >> "%LOG%"
python "%~1" >> "%LOG%" 2>&1
if errorlevel 1 (
  echo ERRORE in %~1 - mi fermo, vedi il log. >> "%LOG%"
  type "%LOG%"
  pause
  exit /b 1
)
exit /b 0
