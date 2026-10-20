@echo off
rem INSTALLA_RACCOLTA_GIORNALIERA.bat - doppio clic, UNA volta sola (20/10/2026).
rem Dice a Windows (Utilita' di pianificazione) di lanciare scripts\RACCOLTA_GIORNALIERA.bat ogni giorno alle 07:30.
rem Se a quell'ora il PC e' spento, parte appena lo accendi ed entri con il tuo utente.
rem Gira con il tuo utente (serve la chiave SSH in %USERPROFILE%\.ssh): parte solo se hai fatto l'accesso a Windows.
rem Per toglierla: DISINSTALLA in fondo a questo file, oppure Utilita' di pianificazione -> "GTT raccolta giornaliera" -> Elimina.

cd /d "%~dp0.."
set "BAT=%CD%\scripts\RACCOLTA_GIORNALIERA.bat"

powershell -NoProfile -Command ^
  "$a = New-ScheduledTaskAction -Execute '%BAT%';" ^
  "$t = New-ScheduledTaskTrigger -Daily -At 07:30;" ^
  "$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2);" ^
  "Register-ScheduledTask -TaskName 'GTT raccolta giornaliera' -Action $a -Trigger $t -Settings $s -Description 'Copia dal Raspberry Pi tutti i dati GTT e controlla la raccolta' -Force | Out-Null;" ^
  "Get-ScheduledTask -TaskName 'GTT raccolta giornaliera' | Select-Object TaskName, State | Format-List;" ^
  "(Get-ScheduledTaskInfo -TaskName 'GTT raccolta giornaliera').NextRunTime"
if errorlevel 1 goto errore

echo.
echo FATTO. Qui sopra devi vedere:
echo   TaskName : GTT raccolta giornaliera
echo   State    : Ready
echo   e la data/ora della prossima esecuzione (domani alle 07:30).
echo Per provarla subito: doppio clic su scripts\RACCOLTA_GIORNALIERA.bat
echo (oppure Utilita' di pianificazione -^> GTT raccolta giornaliera -^> Esegui).
pause
exit /b 0

:errore
echo.
echo ERRORE: Windows non ha accettato l'attivita'. Copia questa finestra e mandala a Claude.
pause
exit /b 1

rem DISINSTALLA (da scrivere in una finestra cmd):
rem   powershell -NoProfile -Command "Unregister-ScheduledTask -TaskName 'GTT raccolta giornaliera' -Confirm:$false"
