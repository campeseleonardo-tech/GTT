origine: agente PV02-generatore
stato: bozza

Rapporto delle modifiche effettuate a strumenti/genera_preventivo.py:

1. Controllo errori JSON:
   - Verifica che il file esista.
   - Verifica che il JSON sia sintatticamente valido.
   - Verifica che tutte le chiavi necessarie (presenti nei segnaposto [[...]] del modello) siano presenti nel dati, indicando quale manca.
   - Altri errori di lettura (es. permessi) danno un messaggio generico in italiano.
   Tutti i messaggi sono in italiano e senza traceback.

2. Supporto output come cartella:
   - Se il percorso di uscita indica una directory esistente, il file viene creato al suo interno.
   - Il nome del file deriva dal valore del campo "PROTOCOLLO" (se mancante o vuoto si usa "preventivo").
   - I caratteri non ammessi nei nomi file (<> : \" / \\ | ? * e caratteri di controllo) vengono sostituiti da underscore.
   - Viene aggiunta l'estensione .docx.
   - Aggiunta della funzione ausiliaria _nome_file_sicuro per sanitizzare il nome del file.

3. Commenti esplicativi:
   - Aggiunti brevi commenti in italiano sopra ogni funzione per spiegare lo scopo, per facilitarne la comprensione anche a chi non è programmatori.
   - Funzioni interessate: prepara_voci, compila, _required_keys_from_model, main.

Scelte predefinite adottate:
   - Quando PROTOCOLLO è mancante o vuoto, si usa "preventivo" come nome base.
   - I caratteri non ammessi vengono sostituiti con underscore anziché rimossi, per preservare la leggibilità.
   - In caso di errore di lettura JSON diverso da JSONDecodeError, si mostra il messaggio generico: "Errore imprevisto nella lettura del JSON.".

Nessuna decisione richiesta a Leo: il funzionamento è completo e sicuro.

Come eseguire:
    python strumenti/genera_preventivo.py dati.json uscita.docx
