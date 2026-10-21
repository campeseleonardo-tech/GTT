@echo off
rem RAPPORTO_3_RIASSUNTO.bat - passo 3: scrive il riassunto corto (una sola chiamata).
rem Doppio clic (sta in scripts\, lavora dalla radice del progetto). Va lanciato DOPO RAPPORTO_2_FATTI.bat.
rem Log: logs\32_rapporto_riassunto.log
chcp 65001 >nul
setlocal
cd /d "%~dp0.."
if not exist logs mkdir logs

echo Passo 3: scrivo il riassunto corto dai fatti verificati (una sola chiamata).
echo.
python scripts\32_rapporto_riassunto.py > logs\32_rapporto_riassunto.log 2>&1
if errorlevel 1 goto errore

echo ------------------ RIEPILOGO ------------------
type logs\32_rapporto_riassunto.log
echo ----------------------------------------------
echo.
echo FATTO. Apri il riassunto con Blocco note o un editor:
echo   docs\rapporti\RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md
echo Devi vedere: una sintesi corta, la tabella "Numeri chiave" e la sezione "Limiti".
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause >nul
exit /b 0

:errore
echo.
echo ERRORE (codice %errorlevel%). Manda a Claude il file logs\32_rapporto_riassunto.log
echo.
pause
exit /b 1
