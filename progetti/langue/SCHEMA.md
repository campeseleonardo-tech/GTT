# SCHEMA – come è fatto un contenuto di Langue

Ogni contenuto (parola, frase, errore, consiglio) è un "record": un elenco di campi con nome e valore.
Le regole complete sono in `schema/contenuto.schema.json`; esempi giusti in `schema/esempi_validi.json`, esempi sbagliati (da rifiutare) in `schema/esempi_errati.json`.
In un record si possono usare **solo** i campi elencati qui sotto: un campo in più rende il record non valido.

## Campi comuni (tutti i tipi)

| Campo | Cosa è | Esempio |
|---|---|---|
| id | nome unico del record | `esempio-articolo-1` |
| tipo | `articolo`, `frase`, `errore`, `consiglio` | `articolo` |
| lingua | sempre `de` | `de` |
| livello | `A1`, `A2`, `B1`, `altro` | `A1` |
| stato | `bozza`, `verificato`, `da_verificare` | `bozza` |
| origine | chi ha creato il record | `importato`, `agente T07` |
| fonte (facoltativo) | da dove viene l'informazione | – |
| note (facoltativo) | appunto breve per chi rilegge | `articolo da controllare` |

## I quattro tipi

**articolo** – un nome con il suo der/die/das.
- `parola`: `Tisch` · `articolo`: `der` · `traduzione_it`: `tavolo`

**frase** – una frase tedesca da rimettere in ordine.
- `testo_de`: `Ich lerne heute Deutsch`
- `traduzione_it`: `Oggi studio tedesco`
- `blocchi`: da 4 a 9 pezzi nell'ordine giusto: `["Ich", "lerne", "heute", "Deutsch"]`. Uniti da uno spazio devono dare **esattamente** `testo_de`.
- `alternative` (facoltativo): altri ordini corretti, come frasi complete: `["Heute lerne ich Deutsch"]`

**errore** – un errore tipico di chi parla italiano.
- `frase_sbagliata`: `Ich habe ein Hund.` · `frase_corretta`: `Ich habe einen Hund.`
- `categoria`: `articolo`, `ordine_verbo`, `genere`, `falsi_amici`, `preposizioni`, `altro`
- `spiegazione_it`: spiegazione in italiano (almeno 20 caratteri)

**consiglio** – un consiglio di film, serie, libri o brani (più avanti).
- `titolo`: titolo reale dell'opera
- `genere`: `thriller_crime`, `commedia`, `fantasy_fantascienza`, `musica_pop_rock`
- `supporto`: `film`, `serie`, `libro`, `brano`
- `perche_adatto_it`: perché è adatto a chi impara
- `parole_utili`: da 3 a 5 parole tedesche: `["die Polizei", "der Mord", "die Leiche"]`

## Come si segna un contenuto

- Contenuto nuovo creato da un agente: `"origine": "agente T0X"` e `"stato": "bozza"`.
- Contenuto importato dai vecchi dati: `"origine": "importato"`.
- Dubbio su tedesco o traduzione: `"stato": "da_verificare"` e una riga in `note` che spiega il dubbio.
- **Per segnarlo come verificato**: dopo averlo riletto, cambia a mano `"stato": "bozza"` in `"stato": "verificato"`. Non cambiare altro.

## Riepilogo delle regole

| Regola | Valore |
|---|---|
| Campi obbligatori | tutti, tranne `fonte`, `note`, `alternative` |
| Campi ammessi | solo quelli del proprio tipo + comuni |
| `lingua` | solo `de` |
| `blocchi` (frase) | 4–9 elementi, uniti = `testo_de` |
| `spiegazione_it` (errore) | almeno 20 caratteri |
| `parole_utili` (consiglio) | 3–5 elementi |
| `alternative` (frase) | se presente, 1–5 elementi |
| Testi | non vuoti, con lunghezza massima |
