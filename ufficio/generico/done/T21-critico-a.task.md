id: T21-critico-a
title: Critica della realizzazione a
project: langue
tier: small
priority: 4
repo: C:\Users\campe\Desktop\Langue
branch: T21-critico-a
base_branch: T20-esegui-a
allowed: []
motore: gratis
modello: @gratis3
approved: yes
checks: [files_exist:agenti/T21-critico-a/CRITICA.md]
checks_warn: [min_chars:agenti/T21-critico-a/CRITICA.md;800, contains_all:agenti/T21-critico-a/CRITICA.md;## Errori probabili;## Voto]
---
Review the work of task T20-esegui-a. Read agenti/T20-esegui-a/DIFF.patch (the exact changes), agenti/T19-scelta/SCELTA.md (the brief) and web/app.js.
Write agenti/T21-critico-a/CRITICA.md IN ITALIAN: ## Fa quello che chiedeva il brief? | ## Errori probabili (each with function name and the line from the diff) | ## Cosa potrebbe rompersi | ## Voto da 1 a 5 e perche'. Be critical and specific; do not praise generically. Do not modify any other file.
