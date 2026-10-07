id: T20-risposta1
title: correzione di T20 dopo la tua risposta
project: langue
tier: small
priority: 1
per_te: Applica la tua risposta ("B: sottomenu 3 giochi") al lavoro di T20, solo dove serve.
origine: risposta di Leo 2026-10-05 12:24
repo: C:\Users\campe\Desktop\Langue
branch: T20-risposta1
allowed: [web/index.html, web/app.js, web/style.css]
checks: [node_check:web/app.js, html_js_check:web/index.html, git_unchanged:contenuti;schema;words_db.json;archivio;web/data.js]
---
Leo answered a question asked during task T20-esegui-b (Realizzazione (modello b)).
Question: Il bottone "Ripasso" in home deve avviare il ripasso per un gioco specifico (qual'è?) o aprire un sottomenu per scegliere?
Your provisional choice was: A
Leo's answer: B: sottomenu 3 giochi
Where it applies: web/app.js (avviaRipasso), web/index.html (listener)
Update ONLY what this answer changes, keep everything else exactly as it is, keep 'origine' and 'stato' fields unchanged. Do not ask new questions unless really needed.
