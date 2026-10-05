id: T20-esegui-b
title: Realizzazione (modello b)
project: langue
tier: small
priority: 4
repo: C:\Users\campe\Desktop\Langue
branch: T20-esegui-b
base_branch: T19-scelta
allowed: [web/index.html, web/app.js, web/style.css]
motore: gratis
modello: @gratis2
approved: yes
checks: [node_check:web/app.js, html_js_check:web/index.html, git_unchanged:contenuti;schema;words_db.json;archivio;web/data.js]
checks_warn: [contains_all:agenti/T20-esegui-b/RAPPORTO.md;T20-esegui-b, min_chars:agenti/T20-esegui-b/RAPPORTO.md;300]
---
Context: Langue is a static website (plain HTML/CSS/JS in web/) for Italians learning German (A1-A2), with 3 games; it was built by agents and NEVER tested by running it. Read PROGETTO.md, SCHEMA.md, web/index.html, web/app.js, web/style.css. You cannot run it: reason carefully about the code.

Implement the improvement chosen in agenti/T19-scelta/SCELTA.md (read it first: the brief is binding). Edit ONLY web/index.html, web/app.js, web/style.css, with EDIT blocks (small local changes; never rewrite whole files). Do not touch web/data.js or any content/data file. Keep every existing feature working; mark new or changed code with a comment [agente T20-esegui-b].
Write agenti/T20-esegui-b/RAPPORTO.md in Italian: what you changed and exactly what Leo should click to test it.
