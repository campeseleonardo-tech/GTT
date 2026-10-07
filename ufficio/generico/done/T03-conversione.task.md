id: T03-conversione
title: conversione dei 200 sostantivi nello schema (contenuti/parole.json)
project: langue
tier: small
priority: 1
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T03-conversione
depends_on: [T02]
script: T03_converti.py
allowed: [contenuti/parole.json]
checks: [files_exist:contenuti/parole.json, count_equals:contenuti/parole.json;200, schema_validate:schema/contenuto.schema.json;contenuti/parole.json, unique_ids:contenuti/parole.json, no_duplicates:parola;contenuti/parole.json, git_unchanged:words_db.json]
---
(Nessun agente: script del runner scripts/T03_converti.py.) Legge words_db.json (sezione articles_game/de, 200 voci) e scrive contenuti/parole.json con i campi dello schema; livello A1 di default per tutti, stato "verificato", origine "importato". Non modifica words_db.json.
