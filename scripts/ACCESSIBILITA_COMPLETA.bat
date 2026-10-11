@echo off
setlocal
REM Script per l'accessibilità completa (tutte le sezioni)
REM Lancia script 18 senza --campione (tutte le sezioni), --lotto-piedi 100, --lotto-tp 20, --salva-tappe
REM \nREM Per riavviarlo dopo un blocco: eseguire questo stesso .bat di nuovo (l'ultimo lotto salvato riprenderà)
REM \nREM NOTA: il .bat si aspetta Python 3.14 nel PATH (o Miniconda). NON usare Anaconda.
\necho Avviando accessoibilità completa (tutte le sezioni)...
python scripts/18_accessibilita.py --lotto-piedi 100 --lotto-tp 20 --salva-tappe --velocita-piedi 80 --velocita-tp 4.8
\necho Fatto. Ricorda di aggiornare la memoria e fare il commit su "prova" dopo la verifica.\necho.\necho Per terminare, premi un tasto (o chiudi la finestra) ...\nPAUSE > nul