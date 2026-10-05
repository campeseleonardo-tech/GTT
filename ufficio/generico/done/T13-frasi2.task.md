id: T13-frasi2
title: altre 50 frasi A1-A2 da riordinare (contenuti/frasi_2.json)
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T13-frasi2
depends_on: [T11]
profile: profiles/langue.md
allowed: [contenuti/frasi_2.json]
checks: [files_exist:contenuti/frasi_2.json, count_equals:contenuti/frasi_2.json;50, schema_validate:schema/contenuto.schema.json;contenuti/frasi_2.json, unique_ids:contenuti/frasi.json;contenuti/frasi_2.json, join_equals:contenuti/frasi_2.json;blocchi;testo_de, no_duplicates:testo_de;contenuti/frasi.json;contenuti/frasi_2.json, field_equals_all:contenuti/frasi_2.json;stato;bozza, field_equals_all:contenuti/frasi_2.json;origine;agente T13-frasi2]
---
Read SCHEMA.md and schema/contenuto.schema.json first, then contenuti/frasi.json (the first 50 sentences) and agenti/T08-frasi/RAPPORTO.md and agenti/T11-revisione/RAPPORTO.md if it exists (lessons about alternative orders).
Create contenuti/frasi_2.json: a JSON array of exactly 50 NEW simple German sentences (tipo "frase") for the sentence-ordering game, ids "fra-0051".."fra-0100", livello A1 or A2, stato "bozza", origine "agente T13-frasi2", fonte "conoscenza del modello"; same record rules as in the first file (blocks 4 to 9, joined with single spaces EXACTLY equal to testo_de, punctuation attached to the last block).
- Not duplicates of the first 50. Structures to cover (about 8 each): Perfekt with haben, Perfekt with sein, subordinate clause with weil, subordinate clause with dass or wenn, imperative and polite requests (Könnten Sie...), sentences with two objects (dative and accusative), negation with nicht/kein, plus a few free ones. Everyday topics.
- Ordering games break if several orders are correct: prefer sentences with one natural order; list every other fully correct order in "alternative" as complete sentences.
- Grammatically perfect standard German; if unsure, replace the sentence with a safer one.
Report (agenti/T13-frasi2/RAPPORTO.md, Italian): what you did and the 5 sentences you are least sure about.
