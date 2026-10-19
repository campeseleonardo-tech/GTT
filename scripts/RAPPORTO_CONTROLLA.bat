@echo off
rem RAPPORTO_CONTROLLA.bat - controllo del PC per il rapporto di sostenibilita' GTT 2025.
rem Doppio clic (sta in scripts\, lavora dalla radice del progetto). NON tocca nessun file: guarda e basta.
rem Controlla: Python, la libreria pypdf, la chiave DeepSeek, il PDF del rapporto.
chcp 65001 >nul
setlocal
cd /d "%~dp0.."
echo ============================================================
echo   CONTROLLO del PC - Rapporto di sostenibilita' GTT 2025
echo ============================================================
echo.

where python >nul 2>&1
if errorlevel 1 goto no_python
echo [OK] Python trovato. Versione:
python --version
echo.
goto check_pypdf

:no_python
echo [X] Python NON trovato nel PATH.
echo     Installa Python 3.14 e riprova. NON usare Anaconda.
goto salta_pypdf

:check_pypdf
python -c "import pypdf" >nul 2>&1
if not errorlevel 1 goto pypdf_ok
echo [X] La libreria pypdf NON e' installata (serve per leggere il PDF).
set /p RISPOSTA=Vuoi installarla adesso con "pip install pypdf"? (s/n) 
if /i not "%RISPOSTA%"=="s" goto pypdf_no
echo Installo pypdf...
python -m pip install pypdf
goto dopo_pypdf

:pypdf_no
echo Ok, non installo. Serve pypdf per andare avanti.
goto dopo_pypdf

:pypdf_ok
python -c "import pypdf; print('[OK] pypdf installato, versione', pypdf.__version__)"

:dopo_pypdf
:salta_pypdf
echo.

if exist chiave_deepseek.txt goto chiave_ok
echo [X] chiave_deepseek.txt NON trovato nella radice: serve la chiave API DeepSeek (una riga).
echo     Chiedi a Leo di crearlo (contiene la chiave, non va mai in git).
goto dopo_chiave

:chiave_ok
echo [OK] chiave_deepseek.txt trovato.

:dopo_chiave
echo.

if exist data\rapporto_di_sostenibilita_2025.pdf goto pdf_ok
echo [X] PDF NON trovato: data\rapporto_di_sostenibilita_2025.pdf
goto dopo_pdf

:pdf_ok
echo [OK] PDF del rapporto trovato: data\rapporto_di_sostenibilita_2025.pdf

:dopo_pdf
echo.
echo ------------------------------------------------------------
echo Cosa fare adesso:
echo   - se vedi tre [OK] (pypdf, chiave, PDF) puoi lanciare RAPPORTO_PILOTA.bat
echo   - se manca la chiave, chiedila a Leo
echo   - se manca pypdf, rispondi "s" quando te lo chiede
echo ------------------------------------------------------------
echo.
echo Per terminare, premi un tasto (o chiudi la finestra) ...
pause >nul
