# Diagnosi GT30: problema con il modulo `json`

Data: 8 ottobre 2026. Diagnosi in sola lettura: nessun file di sistema è stato modificato.

## Causa trovata

Il modulo `json` di Anaconda è **corrotto in un punto** e va in errore su ogni lettura.

File: `C:\Users\campe\anaconda3\lib\json\decoder.py`, riga 353

```python
# riga 353, come si trova ora sul disco (SBAGLIATO)
obj, end = self.scan_once(s, idx),

# come dovrebbe essere (UGUALE al Python 3.14 di riferimento)
obj, end = self.scan_once(s, idx)
```

C'è una **virgola finale** dopo `self.scan_once(s, idx)`. In Python una virgola finale trasforma
l'espressione in una tupla: `obj, end = self.scan_once(s, idx),` equivale a
`obj, end = (self.scan_once(s, idx),)`, cioè una tupla con un solo elemento. Lo
smistamento in due variabili fallisce sempre.

Errore che ne consegue, identico a ogni chiamata:

```
ValueError: not enough values to unpack (expected 2, got 1)
```

Il resto del package `json` è intatto: `__init__.py`, `scanner.py`, `encoder.py` caricano
normally e i metodi `dump`/`dumps` (scrittura) funzionano. Si rompe solo la **lettura**.

## Percorso effettivo del modulo json caricato

| Interprete | Percorso di `json` | Stato |
|---|---|---|
| Anaconda 3.8.8 | `C:\Users\campe\anaconda3\lib\json\__init__.py` | **ROTTO** (`decoder.py` riga 353) |
| Python 3.14 (nel PATH) | `C:\Users\campe\AppData\Local\Python\pythoncore-3.14-64\Lib\json\__init__.py` | funziona |

## Scoperte collaterali importanti

**1. Il `python` nel PATH non è Anaconda.**

```
python -> C:\Users\campe\AppData\Local\Microsoft\WindowsApps\python.exe
          (appareggia a C:\Users\campe\AppData\Local\Python\pythoncore-3.14-64\python.exe, versione 3.14.8)
```

Anaconda esiste in `C:\Users\campe\anaconda3` ma **non è nel PATH** (`conda` non è
riconosciuto come comando). Quindi i comandi `python ...` usati finora hanno girato sul
Python 3.14, non su Anaconda. I due interpreti hanno versioni diverse (3.14.8 contro
3.8.8) e librerie diverse: gli script del progetto devono dichiarare quale usano.

**2. Questo non spiega l'errore "Formato non valido" della pagina HTML.**

Quell'errore viene da `simulazione.html` ed è un'altra cosa: la pagina rifiuta
`scenario_esempio.json` perché quel file è un **input** (le modifiche da applicare), mentre la
pagina accetta solo l'**output** dello script (i numeri del confronto). Python e json non
c'entrano. Vedi `MEMORIA_PROGETTO.md`, sezione "Costruzione delle simulazioni".

**3. Il progetto usa `json.load` in modo incidenteale.**

`calcola_simulazione.py` e `07_elabora_scenario.py` leggono gli scenari con
`json.load`. Lanciati con Anaconda falliscono subito:

```
C:\Users\campe\anaconda3\lib\json\__init__.py", line 357, in loads
C:\Users\campe\anaconda3\lib\json\decoder.py", line 353, in raw_decode
ValueError: not enough values to unpack (expected 2, got 1)
```

## Cosa è stato escluso

- `PYTHONPATH` **vuoto** (`echo %PYTHONPATH%` non stampa nulla).
- Nessun file o cartella `json.py` / `json/` nel repository.
- Nessun `sitecustomize.py` né `usercustomize.py` installati.
- `scripts/__pycache__/` contiene solo `04_genera_mappa`, `06_dati_live`,
  `calcola_simulazione`: nessun `json*`.
- `importlib.util.find_spec('json')` in Anaconda punta alla stdlib, non a un file locale.
- Nessuna corruzione di `json` nel Python 3.14: stessa riga senza virgola.

## Come è stata confermata la causa

1. Letto il sorgente di `decoder.py` riga 353 e confrontato con la riga 361 (identica) del
   Python 3.14: differenza di una virgola.
2. Riprodotto l'errore con Anaconda, sia con `json.loads` sia con `json.load` su uno scenario
   reale del progetto.
3. Ricaricato `decoder.py` **in memoria** (senza scrivere sul disco) togliendo la virgola:
   `JSONDecoder().decode('{"a":1}')` restituisce `{'a': 1}` e
   `decode('[1, 2, {"b": true}]')` restituisce `[1, 2, {'b': True}]`. Il caricamento
  dell'istanza `_default_decoder` già in memoria continua a usare il codice vecchio, quindi
   il test finale sul modulo `json` resta rosso: atteso, non è un problema della diagnosi.
4. Con Python 3.14 le stesse chiamate funzionano.

## Come sistemare (non ancora fatto)

Il file di sistema è corrotto: due strade, entrambe da decidere con Leo.

1. **Correggere la riga** di `decoder.py` togliendo la virgola. Modifica minima, ma tocca
   un file della libreria standard: si perde a ogni reinstallazione di Anaconda.
   Nota: `lib/json/` è la stdlib *impacchettata* in conda, quindi una reinstallazione o un
   `conda install --force-reinstall json` (o il pacchetto python) rimette il file giusto.
2. **Non usare Anaconda per gli script** e dichiararlo in `AGENTS.md`: gli script del progetto
   girano con il Python 3.14 già nel PATH. Bisogna però controllare che non servano librerie
   presenti solo in Anaconda (i dati ISTAT e SQLite si leggono con la stdlib, quindi
   probabilmente va bene).

La via 2 è la più pulita, ma va verificata prima: controllare quali librerie non standard
usano davvero gli script.

## Verifica

Criterio richiesto: il file esiste e indica il percorso effettivo del modulo json caricato.
Entrambe le condizioni sono soddisfatte: il file è `docs/diagnosi_json.md` e la tabella
della sezione "Percorso effettivo del modulo json caricato" riporta i due percorsi reali
(letti a runtime, non indovinati).