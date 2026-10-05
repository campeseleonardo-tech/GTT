# Validatore - T17-prova-gratis - 2026-10-04 23:54

## Giro 0: tutti i controlli OK
- OK     files_exist:contenuti/frasi_prova_gratis.json
- OK     count_equals:contenuti/frasi_prova_gratis.json;10
- OK     schema_validate:schema/contenuto.schema.json;contenuti/frasi_prova_gratis.json
- OK     unique_ids:contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json
- OK     join_equals:contenuti/frasi_prova_gratis.json;blocchi;testo_de
- OK     no_duplicates:testo_de;contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json
- OK     field_equals_all:contenuti/frasi_prova_gratis.json;stato;bozza
- OK     field_equals_all:contenuti/frasi_prova_gratis.json;origine;agente T17-prova-gratis
