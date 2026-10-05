# Rapporto PV03-istruzioni

## Cosa ho fatto
- Creato `strumenti/ISTRUZIONI_CHAT.md` con le quattro sezioni richieste: "Come funziona", "Cosa chiedere alla chat", "Come generare il Word", "Se qualcosa non va".
- Il file è scritto in italiano per una persona non tecnica (il papà di Leo), con un testo pronto da incollare nella chat Claude che raccoglie i campi uno a uno e restituisce solo JSON valido.
- Usati solo dati di esempio inventati (Mario Rossi, Via Prova, ecc.), mai dati reali.
- Il comando di generazione usa i nomi file reali (`genera_preventivo.py`, `dati.json`, `MOD_PREVENTIVO_v4_1.docx`).

## Cosa ho controllato
- La lista campi in `dati_esempio.json` corrisponde ai segnaposto estratti in `ISPEZIONE.md` (tranne `VOCI` che è gestito a parte dallo script).
- Lo script `genera_preventivo.py` accetta 3 argomenti: `json_path`, `output_path` (file o cartella), `modello` opzionale (default `Preventivo Automatico/MOD_PREVENTIVO_v4_1.docx`).
- Il logo è un'immagine nei file `header1.xml`/`header2.xml` e lo script non lo tocca (preserva byte per byte tutto lo zip tranne `word/document.xml`).

## Scelte (default reversibili)
- Ho messo due opzioni di comando (output file fisso vs cartella con nome da PROTOCOLLO) perché lo script supporta entrambe.
- Nella tabella "Se qualcosa non va" ho coperto i casi più probabili per un utente non tecnico: logo, campi vuoti, entità XML, chiavi mancanti, JSON invalido, voci, file corrotto.
- Il testo "Istruzioni per la chat" è lungo ma completo: chiede un campo alla volta, vieta invenzioni, richiede output solo JSON.

## Per Leo (da decidere/rivedere)
- La cartella di default per l'output: ora l'esempio usa `./output/`. Vuoi un'altra cartella (es. `Preventivi/`) o va bene così?
- Il testo "Istruzioni per la chat" potrebbe essere abbreviato se lo ritieni troppo lungo; io l'ho tenuto esplicito per evitare ambiguità.
- Vuoi che aggiunga un esempio di sessione chat (dialogo utente ↔ chat) per mostrare come funziona "un campo alla volta"?
