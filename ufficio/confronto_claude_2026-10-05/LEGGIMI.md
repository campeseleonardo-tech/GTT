# Confronto qualita': modelli gratis (Ufficio) vs Claude Sonnet vs Claude Opus - notte 05/10/2026

Per ogni caso trovi tre cartelle: `gratis` (cio' che ha prodotto l'Ufficio), `sonnet`, `opus`.

| Caso | Cosa e' | Note |
|---|---|---|
| T18-idee | Langue: idee di miglioramento fatte da soli | Gratis = 3 modelli diversi (a=nemotron 120b, b=nemotron 550b, c=qwen 27b), Claude = 1 risposta per modello. Il file c gratis e' stato poi corretto dalla tua risposta alla domanda |
| T19-scelta | Langue: scelta dell'idea da realizzare | Input = le 3 IDEE gratis (stesso input per tutti) |
| GT09-qualita | GTT: analisi della qualita' dei dati | Input = STATISTICHE.md prodotto dallo script |
| TL01-progetto | Timelive: progetto bridge v2 (versione A) | Input = llm_bridge.py + file todo |
| T20-esegui | Langue: realizzazione dell'idea scelta | Input = SCELTA.md gratis, file `web/` originali (ricostruiti annullando il diff gratis). Confronta i `DIFF.patch` e i `RAPPORTO.md` |

## Come e' stato reso equo
- Stesso identico testo del task, stessi file nel messaggio, stesse regole di risposta "a colpo singolo" (nessun accesso ai file, nessuno strumento). Il testo esatto e' in `prompt_usati/`.
- Differenza non eliminabile: la scheda progetto inserita nel testo e' quella al momento della ricostruzione (puo' differire di poche righe da quella vista dai gratis).
- Per T20, le modifiche di Claude sono state applicate con lo stesso meccanismo del motore (blocchi EDIT): tutte applicate senza errori e `node --check` su `app.js` e' passato per entrambi. Non sono state aperte in un browser: nessuno dei tre (gratis, Sonnet, Opus) e' provato.

## Misure oggettive (non dicono quale e' migliore)
Tutti e tre rispettano i titoli di sezione richiesti in tutti i casi. Lunghezza in caratteri (gratis -> sonnet -> opus): T19 6.8k -> 15.3k -> 12.9k; GT09 4.2k -> 9.5k -> 9.9k; TL01 8.0k -> 15.9k -> 15.5k; T18 6.1k/10.5k/10.4k (gratis a/b/c) -> 15.7k -> 12.3k.
T20, righe di diff aggiunte/rimosse: gratis 654/3, sonnet 213/17, opus 253/16 (il gratis ha aggiunto molto piu' codice: da guardare se e' utile o ridondante).

## Cosa guardare tu (la qualita' la giudichi tu)
Esattezza dei numeri (GT09: confronta con STATISTICHE.md), cose inventate (TL01: funzioni del codice citate che non esistono?), originalita' vs ovvieta' delle idee (T18), se il brief di T19 e' davvero eseguibile, se il codice di T20 funziona nel browser.
