id: T07-parole
title: 100 nuovi sostantivi A1-A2 con articolo e traduzione
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T07-parole
depends_on: [T02, T03]
profile: profiles/langue.md
allowed: [contenuti/parole_nuove.json]
checks: [files_exist:contenuti/parole_nuove.json, count_equals:contenuti/parole_nuove.json;100, schema_validate:schema/contenuto.schema.json;contenuti/parole_nuove.json, unique_ids:contenuti/parole.json;contenuti/parole_nuove.json, no_duplicates:parola;contenuti/parole.json;contenuti/parole_nuove.json, field_equals_all:contenuti/parole_nuove.json;stato;bozza, field_equals_all:contenuti/parole_nuove.json;origine;agente T07-parole]
---
Read SCHEMA.md and schema/contenuto.schema.json first, then read contenuti/parole.json (the 200 existing nouns).
Create contenuti/parole_nuove.json: a JSON array of exactly 100 NEW German nouns (tipo "articolo"), none of them already in contenuti/parole.json (compare case-insensitively; also avoid near-duplicates such as plural/singular of an existing word).
- Level A1 or A2 vocabulary useful to an Italian beginner. Cover themes NOT already covered by the existing list (which has animals, food and drink, body, nature/weather, house and rooms, city and transport, family, time, school/work objects and jobs). Good new themes: clothing, shopping and money, restaurant, hotel and travel, health and pharmacy, sport and hobbies, technology, post/bank/office, feelings and character nouns, festivities. Spread roughly evenly.
- Singular nouns only, standard German. Skip nouns whose article is uncertain, regional or variable (e.g. variants like der/das Joghurt). Prefer a clear, single Italian translation (add a short note only when the translation needs it).
- ids: "art-0201" to "art-0300", in order. livello "A1" or "A2" (your best judgement), stato "bozza", origine "agente T07-parole", fonte "conoscenza del modello: articolo da verificare".
- Check yourself before writing: article correct? translation correct? not already in the 200? Then write the file and the report. In the report list the 5 words you are least sure about.
