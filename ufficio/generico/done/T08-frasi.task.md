id: T08-frasi
title: 50 frasi A1-A2 da riordinare, con traduzione e blocchi
project: langue
tier: medium
priority: 2
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T08-frasi
depends_on: [T02]
profile: profiles/langue.md
allowed: [contenuti/frasi.json]
checks: [files_exist:contenuti/frasi.json, count_equals:contenuti/frasi.json;50, schema_validate:schema/contenuto.schema.json;contenuti/frasi.json, unique_ids:contenuti/frasi.json, join_equals:contenuti/frasi.json;blocchi;testo_de, no_duplicates:testo_de;contenuti/frasi.json, field_equals_all:contenuti/frasi.json;stato;bozza, field_equals_all:contenuti/frasi.json;origine;agente T08-frasi]
---
Read SCHEMA.md and schema/contenuto.schema.json first.
Create contenuti/frasi.json: a JSON array of exactly 50 simple German sentences (tipo "frase") for a sentence-ordering game for Italian beginners (A1-A2).
- Each record: id "fra-0001".."fra-0050", livello A1 or A2, stato "bozza", origine "agente T08-frasi", fonte "conoscenza del modello", testo_de (complete sentence with its final punctuation attached to the last block), traduzione_it (natural Italian), blocchi (4 to 9 blocks in the correct order; joined with single spaces they MUST equal testo_de exactly; punctuation stays attached to the word it follows).
- Variety: about 15 main clauses with the verb in 2nd position, 8 with an inverted start (time/place first), 8 questions (W-Fragen and yes/no), 8 with a modal verb (verb at the end), 6 with a separable verb, 5 with a time-manner-place sequence. Use everyday topics (family, food, home, work, travel, hobbies).
- Ordering games break if several orders are correct. Prefer sentences with one natural order; where another order is also fully correct, list it in "alternative" as complete sentences.
- Every sentence must be grammatically perfect standard German. If unsure, replace it with a safer one.
In the report list the 5 sentences you are least sure about.
