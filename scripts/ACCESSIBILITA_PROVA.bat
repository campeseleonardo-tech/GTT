@echo off
setlocal
REM Script per l'accessibilità (prova - campione di 200)
REM Lancia script 18 con --campione 200, --lotto-piedi 100, --lotto-tp 20, --salva-tappe
REM \nREM Per riavviarlo dopo un blocco: eseguire questo stesso .bat di nuovo (l'ultimo lotto salvato riprenderà)
REM \nREM NOTA: il .bat si aspetta Python 3.14 nel PATH (o Miniconda). NON usare Anaconda.
\necho Avviando prova di accessibilità (campione 200)...
python scripts/18_accessibilita.py --campione 200 --lotto-piedi 100 --lotto-tp 20 --salva-tappe --velocita-piedi 80 --velocita-tp 4.8
\necho Fatto. Ricorda di aggiornare la memoria e fare il commit su "prova" dopo la verifica.\necho.\necho Per terminare, premi un tasto (o chiudi la finestra) ...\nPAUSE > nul