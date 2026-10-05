id: T23-prova-guidata
title: Lista di prova del sito per Leo (10 minuti)
project: langue
tier: small
priority: 4
repo: C:\Users\campe\Desktop\Langue
branch: T23-prova-guidata
base_branch: T22-ripasso-fix
allowed: [docs/PROVA_SITO.md]
motore: gratis
modello: @forte
approved: yes
checks: [files_exist:docs/PROVA_SITO.md, git_unchanged:web;contenuti;schema;words_db.json;archivio]
checks_warn: [min_chars:docs/PROVA_SITO.md;1200]
---
Context: Langue is a static website (plain HTML/CSS/JS in web/) for Italians learning German (A1-A2), with 3 games (articoli, frasi, errori) and a new "Ripasso degli sbagli". It was built by agents and NEVER tested by running it. Read PROGETTO.md (rules and Leo's decisions), web/index.html, web/app.js, web/style.css. You cannot run it: reason carefully about the code.

Write docs/PROVA_SITO.md IN ITALIAN: a checklist Leo can follow in about 10 minutes, opening web/index.html in Chrome, to test everything: home, the 3 games, wrong answers, the Ripasso (submenu, a wrong answer that later disappears when answered right), reload of the page (progress kept), daily goal. For each step: what to click, what he should see, and a checkbox "[ ] ok / [ ] non va" with space for a note. At the end: how to open the browser console (F12) and copy any red error to send to the agents. Do not modify any other file.
