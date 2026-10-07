id: T11-revisione
title: seconda lettura indipendente di parole, frasi ed errori gia' scritti (T07, T08, T10)
project: langue
tier: medium
priority: 1
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T11-revisione
depends_on: [T07, T08, T10]
profile: profiles/langue.md
allowed: [contenuti/parole_nuove.json, contenuti/frasi.json, contenuti/errori.json]
checks: [count_equals:contenuti/parole_nuove.json;100, count_equals:contenuti/frasi.json;50, count_equals:contenuti/errori.json;30, schema_validate:schema/contenuto.schema.json;contenuti/parole_nuove.json, schema_validate:schema/contenuto.schema.json;contenuti/frasi.json, schema_validate:schema/contenuto.schema.json;contenuti/errori.json, unique_ids:contenuti/parole_nuove.json, unique_ids:contenuti/frasi.json, unique_ids:contenuti/errori.json, join_equals:contenuti/frasi.json;blocchi;testo_de, fields_differ:contenuti/errori.json;frase_sbagliata;frase_corretta]
---
Read SCHEMA.md, schema/contenuto.schema.json and the three reports agenti/T07-parole/RAPPORTO.md, agenti/T08-frasi/RAPPORTO.md, agenti/T10-errori/RAPPORTO.md (they list the items the first author was least sure about).
You are an INDEPENDENT second reader of the drafts in contenuti/parole_nuove.json (100 nouns), contenuti/frasi.json (50 sentences) and contenuti/errori.json (30 error records). Check every record as a strict native German teacher would: article (der/die/das) of each noun, plural/homograph traps (e.g. Bank, Gleis), translation, level A1/A2, grammar and natural word order of each sentence, whether the listed "alternative" orders are really all correct and whether other correct orders are missing, and for each error record: is the wrong sentence really wrong with exactly ONE mistake typical of Italians, is the corrected sentence perfect, is the Italian explanation true.
What you may change:
- A record that is certainly wrong: fix the wrong field and add to "note" a short line "T11: corretto (era: <old value>)".
- A record you are not sure about: set "stato" to "da_verificare" and write in "note" one short line saying exactly what the doubt is.
- Missing correct alternatives in a sentence: add them to "alternative".
Never set "stato" to "verificato" (only Leo does that), never change "id", "origine", the number of records or the order of records, never remove a record. Keep the JSON formatting (one record per line as it is now).
Write agenti/T11-revisione/RAPPORTO.md in Italian: for each of the three files a short table "id | cosa ho cambiato | perche'", plus how many records you left untouched. Be honest: "unknown beats an invented certainty".
