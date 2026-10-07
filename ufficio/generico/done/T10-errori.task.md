id: T10-errori
title: 30 errori tipici di italiani che imparano il tedesco
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T10-errori
depends_on: [T02]
profile: profiles/langue.md
allowed: [contenuti/errori.json]
checks: [files_exist:contenuti/errori.json, count_equals:contenuti/errori.json;30, schema_validate:schema/contenuto.schema.json;contenuti/errori.json, unique_ids:contenuti/errori.json, fields_differ:contenuti/errori.json;frase_sbagliata;frase_corretta, field_equals_all:contenuti/errori.json;stato;bozza, field_equals_all:contenuti/errori.json;origine;agente T10-errori]
---
Read SCHEMA.md and schema/contenuto.schema.json first.
Create contenuti/errori.json: a JSON array of exactly 30 records (tipo "errore"), each a typical mistake that ITALIAN native speakers make when writing or speaking German at A1-A2, for a "find the error" game.
- Fields: id "err-0001".."err-0030", livello A1 or A2, stato "bozza", origine "agente T10-errori", fonte "conoscenza del modello", frase_sbagliata (natural-looking sentence containing exactly ONE mistake), frase_corretta (the same sentence, corrected, perfect standard German), categoria, spiegazione_it (clear Italian explanation of the rule, 1-3 sentences, mention the Italian habit that causes the mistake when relevant).
- Distribution: at least 6 each of articolo (wrong article for the noun), ordine_verbo (verb position: V2, verb at the end, separable verbs), genere (gender mistakes caused by Italian: e.g. nouns whose gender differs from Italian), falsi_amici (false friends such as bekommen/diventare, Gift/regalo, aktuell/attuale); the rest preposizioni or altro.
- The mistake must be one that really occurs for Italians (not a random typo). The only difference between wrong and corrected sentence should be the error itself. Real, verifiable facts only: for false friends use only well-known ones.
In the report list the 5 items you are least sure about.
