# T17-prova-gratis - esito del runner (2026-10-04 23:54)

Esito finale: done

## Controlli
- OK  files_exist:contenuti/frasi_prova_gratis.json
- OK  count_equals:contenuti/frasi_prova_gratis.json;10
- OK  schema_validate:schema/contenuto.schema.json;contenuti/frasi_prova_gratis.json
- OK  unique_ids:contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json
- OK  join_equals:contenuti/frasi_prova_gratis.json;blocchi;testo_de
- OK  no_duplicates:testo_de;contenuti/frasi.json;contenuti/frasi_2.json;contenuti/frasi_prova_gratis.json
- OK  field_equals_all:contenuti/frasi_prova_gratis.json;stato;bozza
- OK  field_equals_all:contenuti/frasi_prova_gratis.json;origine;agente T17-prova-gratis

## File cambiati
- agenti/T17-prova-gratis/RAPPORTO.md
- agenti/T17-prova-gratis/VALIDATORE.md
- contenuti/frasi_prova_gratis.json

## Note
