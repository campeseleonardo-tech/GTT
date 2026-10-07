id: T14-errori2
title: altri 30 errori tipici di italiani (contenuti/errori_2.json)
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T14-errori2
depends_on: [T11]
profile: profiles/langue.md
allowed: [contenuti/errori_2.json]
checks: [files_exist:contenuti/errori_2.json, count_equals:contenuti/errori_2.json;30, schema_validate:schema/contenuto.schema.json;contenuti/errori_2.json, unique_ids:contenuti/errori.json;contenuti/errori_2.json, fields_differ:contenuti/errori_2.json;frase_sbagliata;frase_corretta, no_duplicates:frase_sbagliata;contenuti/errori.json;contenuti/errori_2.json, field_equals_all:contenuti/errori_2.json;stato;bozza, field_equals_all:contenuti/errori_2.json;origine;agente T14-errori2]
---
Read SCHEMA.md and schema/contenuto.schema.json first, then contenuti/errori.json (the first 30) and agenti/T10-errori/RAPPORTO.md and agenti/T11-revisione/RAPPORTO.md if it exists.
Create contenuti/errori_2.json: a JSON array of exactly 30 NEW records (tipo "errore"), ids "err-0031".."err-0060", livello A1 or A2, stato "bozza", origine "agente T14-errori2", fonte "conoscenza del modello"; same fields and rules as the first file (frase_sbagliata with exactly ONE mistake that Italians really make, frase_corretta perfect, categoria, spiegazione_it of 1-3 sentences mentioning the Italian habit when relevant).
- Do not repeat the mistakes of the first 30. Cover more: dative vs accusative (mir/mich), separable verbs, Perfekt (haben/sein and participle), subordinate clause word order (weil, dass), modal verbs, personal pronouns, plural forms, "man" vs "si", prepositions with fixed cases, and a few well-known false friends (only really well-known ones). Balanced across categories.
- Real, verifiable facts only. Report (agenti/T14-errori2/RAPPORTO.md, Italian): what you did and the 5 items you are least sure about.
