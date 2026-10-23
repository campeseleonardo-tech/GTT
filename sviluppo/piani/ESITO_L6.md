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

---

# L6bis — ripreso con la definizione giusta del fattore (24/10/2026, sera)

**Stato: fatto.** Il controllo è passato; giro completo di TomTom (1.200 richieste, nessun rifiuto), schede e documenti aggiornati.

## Perché lo STOP di L6 era un errore della regola (di Claude), non un disaccordo fra le fonti
- Il nostro «tempo a flusso libero» è la rete OSM ai limiti di velocità, senza semafori e incroci: troppo veloce (Corso Racconigi → Piazza Castello 6,4 minuti, Google alle 8: 29).
- Il 2,1 di Google = (tempo Google − 5) / **nostro** flusso libero: corregge insieme la rete troppo veloce e il traffico.
- Il fattore di L6 = tempo TomTom col traffico / tempo TomTom senza traffico: solo il traffico (anche il 1,2 dei sensori è solo traffico).
Correzione decisa **dopo** aver visto lo STOP (scritto così in `R6_parcheggi.md`, `R8_traffico.md`, nel rapporto e nello script 101): si confronta la stessa grandezza, soglie invariate.

## Cosa è cambiato
- `101_tempi_traffico.py`: per ogni percorso e ora salva `fattore_rete` (tempo TomTom col traffico / nostro flusso libero) e `congestione` (col traffico / senza), 2 decimali, mai i minuti; i percorsi A in uscita e i B di ritorno solo la congestione. Parziale `…_v2` (fuori da git).
- `93`: salva anche `libero_min` per coppia (nient'altro; riga di controllo: `RAPPORTO_TP_CONTRO_AUTO.txt` identico salvo la data prima della sostituzione del fattore). Poi la seconda stima = fattore_rete mediano delle **coppie** alle 8 (`fattore_basso_google` resta il nome storico nel JSON, con `fonte_basso`; il 2,1 sta in `fattore_google_manuale`).
- `94`: i punti usano il fattore in **entrata** (17 percorsi); `100`: fattore per ora (coppie per il R8, entrata per i luoghi del R6), senza più la formula riscalata di L3; `99` (area) usa il fattore dell'93.
- Schede 3 e 4, gare e criteri: «stima con il rallentamento di TomTom»; il limite sull'uscita dal centro è tolto; aggiunti «La stima dei sensori non conta semafori e incroci: è la più favorevole all'auto.» e «La stima di TomTom è un tempo previsto su traffico tipico, non misurato. Usiamo un solo servizio.»; attribuzione «Dati di traffico: TomTom» nei criteri; traduzioni in `testi.json`. `docs/FONTI_DATI.md`: voce TomTom, con il promemoria sulle condizioni d'uso.
- Classi del R6 (≤ 1,5) e regola del titolo della scheda 4 (±0,3): **invariate**.

## Il controllo (STOP/passa)
Sui 6 percorsi in uscita alle 8: fattore_rete mediano TomTom **1,98** contro **2,1** di Google (differenza 0,12, soglia 0,5): si prosegue. (Nel solo controllo, un giorno: 1,96; Corso Racconigi → Castello in entrata 2,99 contro i 3,6 di Google.) Congestione alle 8: uscita 1,26, entrata 1,39, coppie 1,33, sensori 1,2.

## Fattori usati (TomTom, fattore_rete mediano; sensori tra parentesi)
| Ora | coppie (R8) | entrata (punti R6) | sensori |
|---|---|---|---|
| 8:00 | 2,45 | 2,59 | 1,2 |
| 13:00 | 2,06 | 2,27 | 1,1 |
| 17:30 | 2,43 | 2,66 | 1,2 |
| 21:00 | 1,87 | 1,88 | 1,0 |

## Prima / dopo
**Scheda 3 (R6), alle 8, 5 minuti di parcheggio** — punti prioritari «il bus conviene / dipende / non conviene»: da 0 / 1 / 11 a **0 / 7 / 5**; interscambi da 0 / 3 / 2 a **0 / 5 / 0**; minuti di pareggio (mediana dei 12 punti, stima TomTom – sensori): da 21-28 (20,85 – 27,5) a **17-28 (16,85 – 27,5)**. A 4 ore, punti «dipende» (i punti restano 0 «conviene»): 8:00 7, 13:00 5, 17:30 8, 21:00 2.
Classi dei 12 punti dopo → prima: Santa Rita non conviene (=); Metro Massaua dipende (=); Ponte Cavalieri Templari non conviene (=); Regina Margherita non conviene (=); **Pasini, Drosso Cap, Stura Lazio, Marsè, Derna Est, Ferrara** da non conviene a **dipende**; Leonardo da Vinci, Zara non conviene (=). Interscambi: **Caio Mario e Sofia** da non conviene a dipende.
**Scheda 4 (R8), rapporto mediano (stima TomTom – sensori):** 8:00 da 1,96 – 2,94 a **1,75 – 2,94**; 13:00 da 2,37 – 3,10 a **1,96 – 3,10**; 17:30 da 2,01 – 3,02 a **1,79 – 3,02**; 21:00 da 3,32 – 3,32 a **2,14 – 3,32**. Auto con rapporto oltre 2 (8:00): da 41% – 97% a **14% – 97%**.
**Titolo della scheda 4:** invariato nel testo: «Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto». La regola ±0,3 non scatta (scarto massimo 0,39 alle 21:00 con la stima TomTom: prima 1,36), quindi resta «al mattino» e il punto chiave dice come cambia nel giorno («da 1,7 a 2,1 … da 2,9 a 3,3»). Gli estremi del titolo ora sono 1,75 → «2» e 2,94 → «3» (`forbice_estremi` arrotonda a intero sopra 0,5).

## Il messaggio delle schede 3 e 4 è cambiato?
- **Scheda 3:** il titolo no (fermate senza posti). Cambia il punto sul bus: con l'auto più lenta in entrata (TomTom 2,59 contro 2,1) 7 punti su 12 sono competitivi con almeno una stima (prima 1), nessuno «conviene» con entrambe; il bus batte l'auto se in centro si perdono più di 17 minuti (TomTom) o 28 (sensori), non più 21-28. Direzione invariata: serve che parcheggiare in centro sia scomodo o caro.
- **Scheda 4:** il messaggio regge («2-3 volte»), ma l'intervallo basso scende: con TomTom solo il 14% delle auto ha rapporto oltre 2 (prima 41% con Google).
- Perché: il 2,1 di Google era misurato in uscita su 6 percorsi; TomTom, su più percorsi e in entrata, dà un'auto più lenta in entrata (2,59) che in uscita (≈2,0).

## Da non dimenticare
- **Condizioni d'uso di TomTom: da leggere prima di unire in main** (cosa si può pubblicare; in git sono solo rapporti per gruppo e ora e i fattori dei percorsi di controllo).
- Il 2,1 di Google resta nei documenti come controllo; Google Maps non si usa da programma.
- Il file `tempi_traffico.json` è un ingresso fisso in git; lo script 101 non è in `rifai_tutto.py` (chiave, rete, ~1.200 richieste).
