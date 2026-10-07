id: T12-parole2
title: altri 100 sostantivi A1-A2 (contenuti/parole_nuove_2.json)
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T12-parole2
depends_on: [T11]
profile: profiles/langue.md
allowed: [contenuti/parole_nuove_2.json]
checks: [files_exist:contenuti/parole_nuove_2.json, count_equals:contenuti/parole_nuove_2.json;100, schema_validate:schema/contenuto.schema.json;contenuti/parole_nuove_2.json, unique_ids:contenuti/parole.json;contenuti/parole_nuove.json;contenuti/parole_nuove_2.json, no_duplicates:parola;contenuti/parole.json;contenuti/parole_nuove.json;contenuti/parole_nuove_2.json, field_equals_all:contenuti/parole_nuove_2.json;stato;bozza, field_equals_all:contenuti/parole_nuove_2.json;origine;agente T12-parole2]
---
Read SCHEMA.md and schema/contenuto.schema.json first, then contenuti/parole.json (200 nouns) and contenuti/parole_nuove.json (100 nouns), and agenti/T07-parole/RAPPORTO.md (how the first batch was done).
Create contenuti/parole_nuove_2.json: a JSON array of exactly 100 NEW German nouns (tipo "articolo"), none already present in the other two files (compare case-insensitively; avoid singular/plural near-duplicates).
- Level A1 or A2 vocabulary useful to an Italian beginner. Themes NOT yet covered: music, cinema and books; kitchen and cooking items; furniture and small household objects; landscape and environment; office and workplace; traffic and public transport details; seasons and weather phenomena; school and university; abstract everyday nouns (Idee, Problem, Frage, Antwort...); hobbies and games. About 10 per theme.
- Singular nouns only, standard German; skip nouns with uncertain, regional or variable article. One clear Italian translation (a short note only when needed).
- ids "art-0301" to "art-0400" in order; livello "A1" or "A2"; stato "bozza"; origine "agente T12-parole2"; fonte "conoscenza del modello: articolo da verificare". One record per line, same format as contenuti/parole_nuove.json.
Report (agenti/T12-parole2/RAPPORTO.md, Italian): what you did, the 5 words you are least sure about and why.
