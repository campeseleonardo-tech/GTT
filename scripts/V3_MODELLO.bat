@echo off
REM Calcolo lungo del modello V3 (Fase 3-bis) e delle ablazioni diagnostiche.
REM Ripartibile: se si interrompe, rilanciandolo riprende dalle iterazioni MSA
REM gia' fatte (i file msa_stato.npz stanno in data\processed\traffico_c\<outdir>).
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
if not exist logs mkdir logs
set LOG=logs\v3_modello.log
echo ==== INIZIO %DATE% %TIME% ==== >> "%LOG%"

echo [1/4] V3 principale (10 iterazioni MSA) ...
python scripts\50_v3_assegnazione.py --iter 10 --outdir v3 >> "%LOG%" 2>&1
echo ---- V3 principale finito %TIME% ---- >> "%LOG%"

echo [2/4] Ablazione 2: V3 senza congestione (tempi a flusso libero) ...
python scripts\50_v3_assegnazione.py --abl 2 --outdir v3_abl2 >> "%LOG%" 2>&1
echo ---- ablazione 2 finita %TIME% ---- >> "%LOG%"

echo [3/4] Ablazione 1: V3 senza attrattori (popolazione) - 6 iterazioni diagnostiche ...
python scripts\50_v3_assegnazione.py --abl 1 --iter 6 --outdir v3_abl1 >> "%LOG%" 2>&1
echo ---- ablazione 1 finita %TIME% ---- >> "%LOG%"

echo [4/4] Ablazione 3: V3 senza restrizione delle porte - 6 iterazioni diagnostiche ...
python scripts\50_v3_assegnazione.py --abl 3 --iter 6 --outdir v3_abl3 >> "%LOG%" 2>&1
echo ---- ablazione 3 finita %TIME% ---- >> "%LOG%"

echo ==== FINE %DATE% %TIME% ==== >> "%LOG%"
echo.
echo Fatto. Il log e' in %LOG%
