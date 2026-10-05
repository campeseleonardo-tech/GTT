id: T16-sito
title: sito statico di Langue con i tre giochi (web/)
project: langue
tier: large
priority: 3
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T16-sito
depends_on: [T15]
profile: profiles/langue.md
allowed: [web/index.html, web/style.css, web/app.js]
checks: [files_exist:web/index.html;web/style.css;web/app.js;web/data.js, node_check:web/app.js, node_check:web/data.js, json_valid:schema/contenuto.schema.json]
approval_before: leo
approval_after: leo
approved: yes
---
Read SCHEMA.md and look at web/data.js (it defines window.LANGUE_DATA = {articoli: [...], frasi: [...], errori: [...]} with the records of contenuti/*.json; you may read it but do NOT modify it).
Build a small static website in web/ (plain HTML, CSS, JavaScript; NO external libraries, NO network access, works by opening web/index.html from disk). Write only web/index.html, web/style.css, web/app.js.
- Interface and all texts in ITALIAN, simple and friendly, mobile-first, readable colours, large touch targets, keyboard accessible. Home page with three games and a short progress summary.
- Game 1 "Der, die o das?": show a noun from articoli (one at a time, random), three buttons der/die/das, immediate feedback with the Italian translation, streak counter.
- Game 2 "Rimetti in ordine": take a frase, show its blocchi shuffled as buttons, the player taps blocks to build the sentence, a "Controlla" button accepts the correct order OR any order listed in "alternative" (compare complete sentences, ignore the case of the first letter), show traduzione_it as a hint.
- Game 3 "Trova l'errore": show frase_sbagliata and frase_corretta in random order as two options, the player picks the correct one, then show spiegazione_it.
- Use only records whose stato is not "da_verificare". Level filter A1/A2/tutti on the home page.
- Progress (counts of right/wrong per game, best streak) stored ONLY in the browser's localStorage under the key "langue_progress_v1", wrapped in try/catch; the site must work if localStorage is blocked. No accounts, no tracking, no cookies.
- Code: small, commented in Italian, no eval, no innerHTML with data (use textContent) so that content can never inject HTML. Game logic must be testable: put pure functions (shuffle, check order, pick random) at the top of app.js.
Report (agenti/T16-sito/RAPPORTO.md, Italian): what you built, how to open it, what is NOT done or not tested (you cannot run the code: say so honestly).
