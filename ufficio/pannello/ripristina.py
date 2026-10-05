"""ripristina.py - rimette il pannello come era prima dell'ultima modifica fatta dalla chat.
Non ha bisogno che il pannello funzioni: si lancia con RIPRISTINA.bat (doppio clic)."""
import json, shutil, sys
from pathlib import Path
H = Path(__file__).resolve().parent
B = H / "_backup"
try:
    info = json.loads((B / "_info.json").read_text(encoding="utf-8"))
except Exception:
    sys.exit("Non c'e' nessuna copia di sicurezza (_backup). Niente da ripristinare.")
for n in info["files"]:
    if (B / n).exists():
        shutil.copy2(B / n, H / n)
        print("Ripristinato:", n)
print("Fatto: il pannello e' com'era prima di:", info.get("testo", "")[:100])
print("Ora chiudi la finestra nera (se aperta) e riapri run.bat.")
