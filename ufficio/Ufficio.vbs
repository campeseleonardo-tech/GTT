' Apre l'Ufficio senza finestra nera (creato da INSTALLA_UFFICIO). Se e' gia' acceso apre solo il browser.
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "C:\Users\campe\Desktop\Multiple Agents\pannello"
sh.Run """C:\Users\campe\AppData\Local\Microsoft\WindowsApps\pythonw.exe"" ""C:\Users\campe\Desktop\Multiple Agents\pannello\pannello_server.py""", 0, False
