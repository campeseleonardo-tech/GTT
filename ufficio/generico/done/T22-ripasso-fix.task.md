id: T22-ripasso-fix
title: Ripasso: trovare e correggere gli errori veri
project: langue
tier: small
priority: 4
repo: C:\Users\campe\Desktop\Langue
branch: T22-ripasso-fix
base_branch: T20-esegui-b
allowed: [web/index.html, web/app.js, web/style.css]
motore: gratis
modello: @forte
approved: yes
checks: [node_check:web/app.js, html_js_check:web/index.html, git_unchanged:contenuti;schema;words_db.json;archivio;web/data.js]
checks_warn: [contains_all:agenti/T22-ripasso-fix/RAPPORTO.md;Come provarlo, min_chars:agenti/T22-ripasso-fix/RAPPORTO.md;400]
---
Context: Langue is a static website (plain HTML/CSS/JS in web/) for Italians learning German (A1-A2), with 3 games (articoli, frasi, errori) and a new "Ripasso degli sbagli". It was built by agents and NEVER tested by running it. Read PROGETTO.md (rules and Leo's decisions), web/index.html, web/app.js, web/style.css. You cannot run it: reason carefully about the code.

Two earlier reviews of the "Ripasso degli sbagli" code found serious problems: functions using variables that exist only inside another function (e.g. local to avviaSito) -> ReferenceError; variables never defined; possible infinite recursion between display functions; ids used without checking they exist; listeners attached twice. Some were fixed later, some may remain.
Check web/app.js carefully, function by function, for errors that would break the page at runtime: undefined variables, wrong scope, infinite loops/recursion, missing elements, duplicated listeners, progress not saved in localStorage. Fix ONLY real bugs, with small EDIT blocks (copy SEARCH text exactly). Do not add features and do not restyle. Leo's decisions (see PROGETTO.md): the Ripasso button opens a small submenu with the 3 games; keep the simplest option.
Mark changes with // [agente T22]. Write agenti/T22-ripasso-fix/RAPPORTO.md in Italian: list of bugs found (function name, what would happen, fixed or not) and a section "## Come provarlo" with the exact clicks for Leo in the browser (open web/index.html).
