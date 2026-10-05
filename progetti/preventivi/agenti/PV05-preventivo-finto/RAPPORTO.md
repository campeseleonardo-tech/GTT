# Rapporto Agente PV05-preventivo-finto

## Cosa è stato fatto
1. **Creato il file di dati finti realistico** `strumenti/esempi/finto_01.json`:
   - Rappresenta il preventivo verosimile di un elettricista per la ristrutturazione completa dell'impianto elettrico di un bilocale civile abitazione (rimozione vecchio impianto, nuovo centralino 24 moduli con differenziali, 22 prese cucina/forza motrice, 14 punti luce, messa a terra, collaudo e Di.Co. D.M. 37/08).
   - Utilizza esattamente le stesse 11 chiavi previste dal modello e da `dati_esempio.json`.
   - Il cliente è chiaramente inventato con la dicitura richiesta `"CLIENTE DI PROVA - Arch. Luca Moretti"`.
   - Gli importi delle 6 voci (400€ + 650€ + 1.100€ + 700€ + 300€ + 250€) sommano esattamente al TOTALE di `3.400,00` €.

2. **Creato lo script di verifica automatica** `strumenti/prova_finta.py`:
   - Utilizza esclusivamente la libreria standard di Python (`json`, `re`, `subprocess`, `tempfile`, `zipfile`, `decimal`, `pathlib`).
   - È eseguibile senza argomenti sia dalla radice del progetto sia dalla cartella `strumenti/`.
   - Genera il file Word in una cartella temporanea creata con `tempfile` (mai dentro il repository).
   - Esegue ed espone 5 controlli automatici rigorosi.

## Significato dei 5 controlli eseguiti
- **(a) Apertura zip e integrità (.docx)**: verifica che il file generato sia un archivio zip valido e non corrotto (`testzip()`).
- **(b) Nessun segnaposto rimasto**: controlla che in `word/document.xml` non sia rimasta alcuna parentesi quadra doppia `[[` o segnaposto non compilato.
- **(c) Presenza di tutti i valori del JSON**: verifica che ogni singolo testo del JSON (data, protocollo, intestatario, cantiere, formula di apertura, condizioni, totale e ogni singola voce) sia presente nel corpo del documento.
- **(d) Immagini dell'intestazione byte-identiche**: confronta byte per byte i file in `word/media/*` tra il modello Word originale e il file generato, assicurando che il logo non sia stato alterato o riscalato.
- **(e) Corrispondenza matematica della somma delle voci col TOTALE**: estrae gli importi monetari da ciascuna voce e verifica con precisione decimale che la loro somma equivalga al valore del campo `TOTALE`.

## Come provarlo
Dalla radice del progetto:
```bash
python strumenti/prova_finta.py
```

Oppure entrando nella cartella `strumenti/`:
```bash
cd strumenti
python prova_finta.py
```

Se si desidera testare un altro file JSON (ad esempio quello di esempio iniziale):
```bash
python strumenti/prova_finta.py strumenti/dati_esempio.json
```

## Scelte
- Per la somma aritmetica delle voci e del totale è stato usato il modulo standard `decimal.Decimal` per evitare imperfezioni di arrotondamento tipiche dei numeri in virgola mobile (`float`).
- In `finto_01.json` sono state mantenute esattamente e unicamente le 11 chiavi del modello per garantire la massima compatibilità e pulizia.
- Il file `.docx` viene prodotto nella cartella temporanea di sistema e rimosso automaticamente al termine del test senza lasciare file orfani nel repository.
