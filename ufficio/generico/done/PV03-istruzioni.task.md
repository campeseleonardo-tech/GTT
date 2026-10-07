id: PV03-istruzioni
title: Istruzioni per usare la chat senza rompere il Word
project: preventivi
tier: small
priority: 1
repo: C:\Users\campe\Desktop\Projects\Preventivi_Gigi
branch: PV03-istruzioni
base_branch: PV02-generatore
allowed: [strumenti/ISTRUZIONI_CHAT.md]
motore: gratis
modello: @gratis2
approved: yes
checks: [files_exist:strumenti/ISTRUZIONI_CHAT.md]
checks_warn: [min_chars:strumenti/ISTRUZIONI_CHAT.md;1200, contains_all:strumenti/ISTRUZIONI_CHAT.md;## Come funziona;## Come generare il Word;## Se qualcosa non va]
---
Write strumenti/ISTRUZIONI_CHAT.md, in Italian, for a non-technical person (Leo's father) who prepares quotes (preventivi) with a Claude chat.
Problem to solve: once a Claude chat rebuilt the Word file from scratch and the result was badly formatted: the logo became badly made text. The solution is NOT to let the chat rebuild the document: the chat only collects the data and fills a JSON file; a script fills the real template, so logo, header and layout are always the original.
Read strumenti/genera_preventivo.py, strumenti/dati_esempio.json and agenti/PV01-ispeziona/ISPEZIONE.md. Write:
- ## Come funziona (5 lines)
- ## Cosa chiedere alla chat (a ready-to-paste instruction text for the chat: collect the fields of dati_esempio.json one by one, never invent amounts, output ONLY the JSON)
- ## Come generare il Word (the exact command, with the file names)
- ## Se qualcosa non va (logo, campi vuoti, caratteri strani)
Use ONLY made-up example data. Never mention real customers.
