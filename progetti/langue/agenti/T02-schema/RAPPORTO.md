# Rapporto T02-schema

## Fatto
- `schema/contenuto.schema.json` (versione 1, solo "versione", "comuni", "tipi").
- `schema/esempi_validi.json`: 4 record (articolo, frase, errore, consiglio), bozza, origine "agente T02-schema".
- `schema/esempi_errati.json`: 13 record, ciascuno con una sola violazione (campo mancante, enum errato, pochi/troppi blocchi, blocchi diversi da testo_de, campo sconosciuto, tipo di campo errato, spiegazione corta, categoria/lingua/stato non validi, troppe parole_utili, tipo sconosciuto).
- `SCHEMA.md` in italiano.

## Controlli
Verifica solo mentale (non ho eseguito il validatore): ogni esempio valido rispetta campi e limiti; i blocchi uniti da spazio coincidono con testo_de.

## Scelte
- Limiti di lunghezza massimi e min 1 sui testi (non richiesti): id 3–80, origine 3–60, fonte 300, note 500, spiegazione_it max 600, ecc.
- `alternative`: min 1, max 5 se presente.
- Nessun campo numerico: il tipo "intero" non è usato.
- Il record `errato-blocchi-diversi-dal-testo` presuppone che il validatore controlli l'uguaglianza blocchi/testo_de (regola indicata nel compito, non esprimibile nello schema).
- `errato-tipo-sconosciuto` ha solo campi comuni: va rifiutato per tipo non ammesso.

## Da rivedere (Leo)
- Esempio consiglio: "Tatort" è una serie poliziesca tedesca reale; la descrizione è generica e non verificata nei dettagli, marcata in `note`. Le parole (die Polizei, der Mord, die Leiche) sono corrette per me.
- Un file di esempio contiene un record "errato" con tipo "verbo": se il validatore non gestisce tipi sconosciuti, va controllato.
