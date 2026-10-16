@echo off
rem RISULTATO2_METRO_NOTTE.bat - Risultato 2 "metro di notte".
rem Doppio clic dalla radice del progetto. Gira in QUESTA finestra: NON chiuderla.
rem Genera due GTFS finti (corse METROU nel buco 00:50-05:22, ogni 15 e ogni 30 minuti)
rem e calcola l'accessibilita' con R5 nelle ore 01-04, poi i numeri finali.
rem
rem ATTENZIONE (avviso obbligatorio, leggere prima):
rem   i passaggi 2 e 3 usano R5 (Java, ~3 GB di RAM) e sono LENTI: ricalcolano
rem   la camminata + 4 ore di trasporto pubblico su tutte le 8317 sezioni.
rem   Prima di lanciare, Leo controlla a occhio su Task Manager la RAM libera
rem   E che nessun altro processo opencode/Claude sia in corso in quel momento.
rem   Non lanciare questo .bat dentro opencode.
rem
rem FIX di Claude (16/10, verificato sul codice di 18_accessibilita.py):
rem   la "firma" di una run (funzione firma_run) NON contiene il percorso del GTFS,
rem   solo giorno/ore/cutoff/ecc. Siccome notte15 e notte30 usano la STESSA firma,
rem   senza pulire data\processed\accessibilita_parziale tra un lancio e l'altro il
rem   passaggio 3 (notte30) avrebbe RIUSATO i parziali gia' scritti dal passaggio 2
rem   (notte15), dando numeri IDENTICI (e sbagliati) per i due scenari. Lo script 18
rem   non la pulisce mai da solo (restano li' anche a run finita). Percio' sotto
rem   cancello quella cartella subito prima di ciascuno dei due passaggi R5.
rem
setlocal
cd /d "%~dp0"
if not exist logs mkdir logs

echo [1/4] Genero i due scenari GTFS notte15 e notte30...
python scripts\28_scenario_metro_notte.py > logs\28_scenario_metro_notte.log 2>&1
if errorlevel 1 goto errore

echo [2/4] Accessibilita' scenario 15 minuti (R5, lungo)...
if exist data\processed\accessibilita_parziale rmdir /s /q data\processed\accessibilita_parziale
python scripts\18_accessibilita.py --giorno 2026-10-12 --ore 1,2,3,4 --gtfs data\scenari\gtt_gtfs_notte15.zip --out accessibilita_notte15 --salva-tappe > logs\18_notte15.log 2>&1
if errorlevel 1 goto errore

echo [3/4] Accessibilita' scenario 30 minuti (R5, lungo)...
if exist data\processed\accessibilita_parziale rmdir /s /q data\processed\accessibilita_parziale
python scripts\18_accessibilita.py --giorno 2026-10-12 --ore 1,2,3,4 --gtfs data\scenari\gtt_gtfs_notte30.zip --out accessibilita_notte30 --salva-tappe > logs\18_notte30.log 2>&1
if errorlevel 1 goto errore

rem Pulizia finale: non lasciare parziali di questa run a confondere il prossimo
rem ricalcolo della accessibilita.json "vera" (baseline, senza --gtfs/--out).
if exist data\processed\accessibilita_parziale rmdir /s /q data\processed\accessibilita_parziale

echo [4/4] Calcolo i numeri finali...
python scripts\29_risultato2_metro_notte.py > logs\29_risultato2_metro_notte.log 2>&1
if errorlevel 1 goto errore

echo.
echo FATTO. Controlla:
echo   data\processed\risultato2_metro_notte.json
echo   docs\RAPPORTO_RISULTATO2_METRO_NOTTE.txt
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause > nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude il log dentro logs\.
pause
exit /b 1
