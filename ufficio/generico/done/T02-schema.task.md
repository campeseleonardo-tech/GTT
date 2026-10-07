id: T02-schema
title: schema unico dei contenuti, esempi e SCHEMA.md
project: langue
tier: medium
priority: 1
data_level: 0
repo: C:\Users\campe\Desktop\Langue
branch: T02-schema
depends_on: [T01]
profile: profiles/langue.md
allowed: [schema, SCHEMA.md]
checks: [files_exist:SCHEMA.md;schema/contenuto.schema.json;schema/esempi_validi.json;schema/esempi_errati.json, json_valid:schema/contenuto.schema.json;schema/esempi_validi.json;schema/esempi_errati.json, schema_selftest:schema/contenuto.schema.json;schema/esempi_validi.json;schema/esempi_errati.json]
agent: no
approval_after: leo
approved: yes
---
Create the single content schema for Langue, in the SIMPLE FORMAT below (it is validated by the runner's own validator, not by JSON Schema tools). Write:

1. schema/contenuto.schema.json  -  a JSON object {"versione": 1, "comuni": {...}, "tipi": {...}}.
   "comuni" = fields shared by every record; "tipi" = extra fields per type. Each field is described by a spec object:
   {"tipo": "testo" | "intero" | "elenco_testi", "obbligatorio": true/false (default true), "valori": [allowed values], "min": n, "max": n}
   (for "testo": min/max are the length in characters; for "elenco_testi": number of items; for "intero": the value).
   Records may contain ONLY fields declared for their type (shared + type-specific).

   REQUIRED CONTENT (use exactly these field names, they are used by other tasks):
   comuni: id (testo), tipo (testo, valori: articolo, frase, errore, consiglio), lingua (testo, valori: ["de"]), livello (testo, valori: A1, A2, B1, altro), stato (testo, valori: bozza, verificato, da_verificare), origine (testo, e.g. "importato" or "agente T07"), fonte (testo, obbligatorio false), note (testo, obbligatorio false).
   tipo "articolo": parola (testo), articolo (testo, valori: der, die, das), traduzione_it (testo).
   tipo "frase": testo_de (testo), traduzione_it (testo), blocchi (elenco_testi, min 4, max 9; the blocks in correct order; joined with single spaces they must equal testo_de exactly), alternative (elenco_testi, obbligatorio false: other fully correct orderings of the same sentence, as complete sentences).
   tipo "errore": frase_sbagliata (testo), frase_corretta (testo), categoria (testo, valori: articolo, ordine_verbo, genere, falsi_amici, preposizioni, altro), spiegazione_it (testo, min 20).
   tipo "consiglio": titolo (testo), genere (testo, valori: thriller_crime, commedia, fantasy_fantascienza, musica_pop_rock), supporto (testo, valori: film, serie, libro, brano), perche_adatto_it (testo), parole_utili (elenco_testi, min 3, max 5).
   Do not add anything else to the schema file: the validator only knows "versione", "comuni" and "tipi".

2. schema/esempi_validi.json  -  a JSON ARRAY with at least one valid, realistic example record per type (articolo, frase, errore, consiglio), all with stato "bozza" and origine "agente T02-schema" and ids like "esempio-articolo-1". German must be correct.
3. schema/esempi_errati.json  -  a JSON ARRAY of at least 8 records that MUST be rejected, each breaking exactly one rule (missing field, wrong enum value, too few blocks, unknown field, wrong type of field, etc.). Records may contain only the schema's fields (do not add comment fields), so give each wrong example an id that explains the problem, e.g. "errato-pochi-blocchi".
4. SCHEMA.md  -  in ITALIAN, for a non-programmer: what each type is, every field with an example, how to mark a record as verified, how new content is marked (origine/stato), and a short table of the rules. Max about 80 lines.

Do not touch any other file. Self-check mentally that every example validates (or fails) as intended, then write the report.
