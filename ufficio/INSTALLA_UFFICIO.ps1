# INSTALLA_UFFICIO.ps1 - si lancia UNA volta con doppio clic su INSTALLA_UFFICIO.bat (04/10/2026)
# 1) trova pythonw.exe (Python senza finestra nera)
# 2) scrive Ufficio.vbs, che apre l'Ufficio senza finestra nera
# 3) crea l'icona "Ufficio" sul desktop
# 4) crea l'attivita' di Windows "UfficioAgenti": ogni 5 minuti fa partire dispatcher.py (invisibile),
#    cosi' gli agenti lavorano anche a pannello chiuso; toglie la vecchia attivita' "AgentsNightly"
# 5) apre l'Ufficio
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Cartella: $root"

$pyw = $null
foreach ($c in @("pythonw.exe", "pyw.exe")) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd) { $pyw = $cmd.Source; break }
}
if (-not $pyw) {
  $py = Get-Command "python.exe" -ErrorAction SilentlyContinue
  if ($py) { $cand = Join-Path (Split-Path $py.Source) "pythonw.exe"; if (Test-Path $cand) { $pyw = $cand } }
}
if (-not $pyw) { Write-Host "ERRORE: non trovo pythonw.exe. Niente e' stato cambiato." -ForegroundColor Red; exit 1 }
Write-Host "Python senza finestra: $pyw"

$vbs = Join-Path $root "Ufficio.vbs"
$srv = Join-Path $root "pannello\pannello_server.py"
@"
' Apre l'Ufficio senza finestra nera (creato da INSTALLA_UFFICIO). Se e' gia' acceso apre solo il browser.
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "$root\pannello"
sh.Run """$pyw"" ""$srv""", 0, False
"@ | Set-Content -Path $vbs -Encoding ASCII
Write-Host "Scritto: $vbs"

$desk = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desk "Ufficio.lnk"
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut($lnk)
$s.TargetPath = "$env:WINDIR\System32\wscript.exe"
$s.Arguments = "`"$vbs`""
$s.WorkingDirectory = $root
$s.IconLocation = "$env:WINDIR\System32\imageres.dll,174"
$s.Description = "Ufficio degli agenti"
$s.Save()
Write-Host "Icona sul desktop: $lnk"

$disp = Join-Path $root "dispatcher.py"
$act = New-ScheduledTaskAction -Execute $pyw -Argument "`"$disp`"" -WorkingDirectory $root
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$set = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 0)
Register-ScheduledTask -TaskName "UfficioAgenti" -Action $act -Trigger $trg -Settings $set -Description "Fa lavorare gli agenti dell'Ufficio (uno alla volta), anche a pannello chiuso" -Force | Out-Null
Write-Host "Attivita' di Windows 'UfficioAgenti' creata (ogni 5 minuti, invisibile)"
if (Get-ScheduledTask -TaskName "AgentsNightly" -ErrorAction SilentlyContinue) {
  Unregister-ScheduledTask -TaskName "AgentsNightly" -Confirm:$false
  Write-Host "Tolta la vecchia attivita' 'AgentsNightly'"
}

Start-Process "$env:WINDIR\System32\wscript.exe" -ArgumentList "`"$vbs`""
Write-Host ""
Write-Host "FATTO. Da ora apri l'Ufficio con l'icona 'Ufficio' sul desktop." -ForegroundColor Green
