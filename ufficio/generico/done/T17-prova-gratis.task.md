id: T17-prova-gratis
title: prova modello gratuito: 10 frasi A1 da riordinare (contenuti/frasi_prova_gratis.json)
project: langue
tier: small
priority: 1
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T17-prova-gratis
profile: profiles/langue.md
motore: gratis
per_te: Prova del primo modello gratuito: 10 frasi nuove in un file di prova, su un ramo a parte (main non viene toccato)
origine: chat di controllo 2026-10-05
allowed: [contenuti/frasi_prova_gratis.json]
checks: [files_exist:contenuti/frasi_prova_gratis.json, count_equals:contenuti/frasi_prova_gratis.json;10, schema_validate:schema/contenuto.schema.json;contenuti/frasi_prova_gratis.json, unique_ids:contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json, join_equals:contenuti/frasi_prova_gratis.json;blocchi;testo_de, no_duplicates:testo_de;contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json, field_equals_all:contenuti/frasi_prova_gratis.json;stato;bozza, field_equals_all:contenuti/frasi_prova_gratis.json;origine;agente T17-prova-gratis]
---
Read SCHEMA.md and schema/contenuto.schema.json first, then contenuti/frasi.json and contenuti/frasi_2.json (the existing 100 sentences: copy their exact record format).
Create contenuti/frasi_prova_gratis.json: a JSON array of exactly 10 NEW simple German sentences (tipo "frase") for the sentence-ordering game, ids "fra-9001".."fra-9010", livello A1, stato "bozza", origine "agente T17-prova-gratis", fonte "conoscenza del modello"; same record rules as the existing files (blocks 4 to 9, joined with single spaces EXACTLY equal to testo_de, punctuation attached to the last block).
- Not duplicates of the existing sentences. Everyday topics, present tense, one natural word order each; list any other fully correct order in "alternative" as complete sentences.
- Grammatically perfect standard German; if unsure, replace the sentence with a safer one.
Report (agenti/T17-prova-gratis/RAPPORTO.md, Italian, max 10 lines): what you did and the 2 sentences you are least sure about.
