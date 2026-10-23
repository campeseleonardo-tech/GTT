# Esito L6 — tempi in auto col traffico da TomTom (24/10/2026) — FERMO ALLO STOP DEL CONTROLLO

**Stato: passo 1 e 2 fatti, passi 3-7 NON fatti. Decide Leo.** Nessun risultato, scheda o documento di R6/R8 è cambiato: gli script 93, 94, 99 e 100 e le schede leggono ancora il 2,1 di Google.

## Cosa c'è
- `scripts/101_tempi_traffico.py` (nuovo): chiama la TomTom Routing API (libreria standard), pausa di 0,3 s, ripresa da un parziale (solo il rapporto di ogni richiesta, non i tempi, fuori da git), chiave letta solo da `config_locale.json` e tolta da ogni messaggio d'errore. Risposte grezze non salvate (`SALVA_GREZZI = False`). Opzioni `--prova`, `--solo-controllo`. Codici di uscita: 0 fatto, 4 STOP del controllo, 3 chiave rifiutata o limite richieste.
- Regole fissate (non cambiate): percorsi A (17 luoghi del R6, entrata e uscita), B (8 percorsi di controllo, due sensi), C (100 coppie di zone); partenze 10 e 11/11/2026 alle 8, 13, 17:30, 21; fattore = tempo col traffico / tempo senza; controllo contro il 2,1 di Google sui 6 percorsi in uscita alle 8, STOP oltre 0,5.
- Prove: `--prova` (risposte finte) OK; pyflakes zero.
- Lancio `--solo-controllo`: 64 richieste (16 percorsi × 4 ore, solo martedì 10/11), nessun errore, nessun rifiuto del servizio.

## Il controllo: STOP
Sui 6 percorsi da Piazza Castello alle 8:00 il fattore mediano di TomTom è **1,26** (25°-75° percentile 1,22-1,32), contro **2,1** di Google: differenza 0,84, oltre la soglia di 0,5.

| Percorso (alle 8) | TomTom | Google (da 93: (tempo Google − 5) / flusso libero) | Sensori 5T |
|---|---|---|---|
| Piazza Castello → Collegno | 1,3 | 1,1 | 1,2 |
| Piazza Castello → Venaria Reale | 1,3 | 2,0 | 1,2 |
| Piazza Castello → Settimo Torinese | 1,3 | 2,3 | 1,2 |
| Piazza Castello → Moncalieri | 1,2 | 2,5 | 1,2 |
| Piazza Castello → Orbassano | 1,2 | 2,2 | 1,2 |
| Piazza Castello → Rivoli | 1,5 | 1,8 | 1,2 |
| **mediana dei 6** | **1,26** | **2,1** | **1,2** |

(I fattori Google per percorso sono nel JSON dello script 93, `fattori_google_per_percorso`; il fattore dei sensori è 1,2 per tutti.)
Altri risultati del controllo, fattore mediano per gruppo e ora (8 / 13 / 17:30 / 21): uscita 1,26 / 1,21 / 1,41 / 1,07; altri percorsi (soprattutto in entrata, 10) 1,38 / 1,17 / 1,39 / 1,07. Il percorso in entrata Corso Racconigi → Piazza Castello dà 1,3 alle 8 (Google a mano: 3,6 con la sua formula). Tabella completa in `docs/rapporti/RAPPORTO_TEMPI_TRAFFICO_controllo.txt` e `data/processed/tempi_traffico_controllo.json`.

Lettura (da confermare con Leo): TomTom vede un rallentamento tipico molto più basso di Google (1,2-1,5) e vicino ai sensori 5T (1,2). Con 1,3 al posto di 2,1 le due stime quasi coincidono, il messaggio della scheda 3 («il bus conviene solo dove è veloce») probabilmente si rafforza, e la scheda 4 passerebbe da «da 2 a 3 volte» a un intervallo stretto intorno a 2,9-3,0. Il dato Google a mano era l'unico di 6 punti, in un solo giorno.

## Decisioni che servono a Leo
1. **Come procedere**, tre strade:
   - (a) continuare con TomTom come da regola (la stima «Google» diventa «TomTom»; il 2,1 resta come controllo e va nei limiti), lanciando il giro completo (~1.200 richieste, un giorno di piano gratuito) e poi i passi 3-7;
   - (b) tenere i due fattori com'erano (sensori e Google) e usare TomTom solo come terza stima di controllo;
   - (c) prima rifare a mano alcuni percorsi su Google Maps (alle 8, anche in entrata) per capire quale dei due è più vicino al vero.
2. **Condizioni d'uso di TomTom**: finché Leo non le ha lette, in git vanno solo statistiche aggregate e il fattore a una cifra dei percorsi di controllo (già così).

Per riprendere dopo la decisione: `python scripts\101_tempi_traffico.py` (giro completo, riprende dal parziale).
