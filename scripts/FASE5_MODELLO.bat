@echo off
REM Calcolo lungo del modello V4 (Fase 5) e delle ablazioni diagnostiche.
REM Ripartibile: lo stato MSA sta in data\processed\traffico_d\<variante>\msa_stato.npz.
REM ATTENZIONE: il modello non e' idempotente al rilancio se msa_stato.npz esiste;
REM per rifare da capo cancellare la sottocartella della variante.
cd /d "%~dp0.."
set PYTHONIOENCODING=utf-8
if not exist logs mkdir logs
set LOG=logs\fase5_modello.log
echo ==== INIZIO %DATE% %TIME% ==== >> "%LOG%"

echo [1/5] V0 di riferimento (popolazione, senza congestione/ZTL, tutte le porte) ...
python scripts\62_v4_modello.py --variante v0 --outdir v0 >> "%LOG%" 2>&1
echo ---- v0 finito %TIME% ---- >> "%LOG%"

echo [2/5] V4 principale (attrattori + congestione per corsia + ZTL + porte >=3), 8 iterazioni ...
python scripts\62_v4_modello.py --variante v4 --iter 8 --outdir v4 >> "%LOG%" 2>&1
echo ---- v4 finito %TIME% ---- >> "%LOG%"

echo [3/5] Ablazione 1: V4 senza attrattori (popolazione) - 5 iterazioni ...
python scripts\62_v4_modello.py --variante abl1 --iter 5 --outdir abl1 >> "%LOG%" 2>&1
echo ---- abl1 finito %TIME% ---- >> "%LOG%"

echo [4/5] Ablazione 2: V4 senza congestione (tempi a flusso libero) ...
python scripts\62_v4_modello.py --variante abl2 --outdir abl2 >> "%LOG%" 2>&1
echo ---- abl2 finito %TIME% ---- >> "%LOG%"

echo [5/5] Ablazione 3: V4 senza restrizione delle porte - 5 iterazioni ...
python scripts\62_v4_modello.py --variante abl3 --iter 5 --outdir abl3 >> "%LOG%" 2>&1
echo ---- abl3 finito %TIME% ---- >> "%LOG%"

python scripts\63_v4_valutazione.py >> "%LOG%" 2>&1
echo ---- valutazione 63 finita %TIME% ---- >> "%LOG%"
echo ==== FINE %DATE% %TIME% ==== >> "%LOG%"
echo.
echo Fatto. Il log e' in %LOG%
echo Valutazione: docs\rapporti\RAPPORTO_TRAFFICO_V4.txt
