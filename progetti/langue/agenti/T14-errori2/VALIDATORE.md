# Validatore - T14-errori2 - 2026-10-04 16:05

## Giro 0: tutti i controlli OK
- OK     files_exist:contenuti/errori_2.json
- OK     count_equals:contenuti/errori_2.json;30
- OK     schema_validate:schema/contenuto.schema.json;contenuti/errori_2.json
- OK     unique_ids:contenuti/errori.json;contenuti/errori_2.json
- OK     fields_differ:contenuti/errori_2.json;frase_sbagliata;frase_corretta
- OK     no_duplicates:frase_sbagliata;contenuti/errori.json;contenuti/errori_2.json
- OK     field_equals_all:contenuti/errori_2.json;stato;bozza
- OK     field_equals_all:contenuti/errori_2.json;origine;agente T14-errori2
