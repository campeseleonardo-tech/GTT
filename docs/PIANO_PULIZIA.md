# Analisi completa, pulizia e prossimi passi (20/10/2026, sera)

Scritto da Claude su richiesta di Leo. Seconda versione: rifatta **dopo** l'esito delle correzioni generali
(`docs/archivio/correzioni_20ott/ESITO_CORREZIONI_GENERALI.md`). La prima versione (stessa giornata, prima
dell'esito) è nella storia di git.

Scelte di Leo (20/10): file superati **in archivio**, non cancellati; portfolio su **GitHub Pages**; campo
**ridotto** (via bici, telefonia, logistica, eventi; uno solo fra Risultato 3 e 5).

## 1. Ricontrollo dell'esito

L'agente ha eseguito tutto il piano: 0 errori, verifiche indipendenti 0 non superate, pagine senza errori, mappa da
23,6 a 13,6 MB. **Ho ricontrollato i numeri del Risultato 6 sui dati dentro la nuova `mappa_torino.html`**: 391
fermate (99 / 154 / 116 / 22), 253 senza posti bastanti, 76 aree (20 / 5 / 5 / 46 «Pochi dati»), distanze dei 20
punti da Piazza Castello rifatte da zero: **tutto coincide** con l'esito e con i rapporti.

Le correzioni hanno funzionato su quello che dovevano correggere: i punti vicini al centro passano da 7 a 1, le
auto sono solo conducenti, la quota (5,8%) e le auto in entrata sono dello stesso insieme (mattino, in entrata).

## 2. Cosa ho trovato (dal più importante)

| # | Cosa | Perché conta | Stato |
|---|---|---|---|
| 1 | **Stesse auto contate in più punti del Risultato 6.** Maroncelli, Bosso e Ponte Cavalieri Templari stanno sullo stesso asse di Moncalieri, a 0,7-1,2 km l'uno dall'altro: 627 + 540 + 350 «posti che mancano», ma sono in gran parte le stesse auto. La somma dei 20 punti (6.356) supera tutte le auto che si potrebbero fermare (5.067). Altre coppie a meno di 1 km a Mirafiori e alle Vallette | Il grafico «I punti dove mancano più posti» fa pensare a 1.500 posti mancanti a Moncalieri | **Da decidere** (domanda 2): un punto per asse d'ingresso |
| 2 | **Gioanetti a 1,4 km dal centro** è un punto prioritario | Fermare un'auto lì fa risparmiare poca strada | **Da decidere** (domanda 2): distanza minima, es. 3 km |
| 3 | **Il repository è privato.** GitHub Pages da un repository privato richiede un account a pagamento | Cambia come si pubblica | **Da decidere** (domanda 1) |
| 4 | **Falso allarme nel controllo di leopi**: la ZTL risultava «ferma dal 14/10», ma il raccoglitore la salva solo quando cambia (il dato è fermo dal 2024). Con il controllo ogni mattina l'allarme sarebbe suonato **tutti i giorni** e avresti imparato a ignorarlo | Un allarme sempre acceso non serve | **Corretto** in `controlla_leopi.py`: la ZTL non dà più allarme (si stampa la data dell'ultima versione); si stampano gli errori del raccoglitore delle ultime 24 ore; la «notte» del feed dei ritardi arriva alle 6. Provato su un database finto |
| 5 | **Cartella da pubblicare di 90 MB** | Per GitHub Pages è tanto (ogni pubblicazione aggiunge peso al repository) | Da guardare al passo «Pubblicare»: quali file pesano (probabilmente le giornate registrate `replay_*.js`) |
| 6 | **Risultato 2: il numero in grande è ancora quello debole** (773.307 = qualsiasi miglioramento, anche di un solo servizio). Quello severo (334.085, almeno +25% di servizi) è solo nel testo | È il titolo che legge chi passa | **Da decidere** (domanda 3) |
| 7 | **La quota del 5,8% viene da 64 interviste** e si moltiplica per una stima di traffico a ±38%: i «posti che mancano» (627, 540…) hanno tre cifre ma sono ordini di grandezza | Precisione apparente | Proposta insieme alla domanda 2: arrotondare (es. «circa 600») |
| 8 | **Il modello del traffico senza code** manda le auto sulle strade veloci: Corso Francia non è fra i 15 luoghi con più auto in entrata, Strada Trieste (Moncalieri) è in cima | I punti prioritari dipendono da questo | Proposta: confronto con i sensori 5T al mattino in entrata (dati che ci sono già) |
| 9 | **Validazione del Risultato 6 quasi vuota**: dei 5 interscambi del Comune solo Stura dice qualcosa (pieno, su strada trafficata). Caio Mario ha il contatore fermo, Fermi non trasmette, Sofia è poco usato pur con molte auto accanto | Il risultato non ha ancora un controllo con la realtà | Più giorni di parcheggi (inizio novembre) + punto 8 |
| 10 | **46 aree su 76 «Pochi dati»** | La vista «aree» della mappa è quasi tutta grigia | Da rivedere dopo i punti 1-2 |
| 11 | README generato senza il punto delle migliaia nei numeri in grassetto («10919») | È la prima pagina | **Corretto** in `86_prepara_pubblicazione.py` |
| 12 | Riassunto inglese del Risultato 2: mancava il numero severo, c'era «dummy runs» | Coerenza con il testo italiano | **Corretto** in `schede_risultati.py` |
| 13 | Lo script 80 sembra superato, ma **84 e 85 ne usano le funzioni**; il 77 è un modulo usato da 72 e 73 | Spostarli in archivio avrebbe rotto la catena | Lasciati in `scripts/` con una nota; da sistemare quando si tocca l'84 |

## 3. Pulizia fatta oggi (nessun numero cambia)

| Cosa | Dove ora |
|---|---|
| 21 file superati o usati una volta (Risultato 6 prima delle correzioni: 74, 75, 76, 78; simulatore generico; verifiche delle fasi 1-4 del traffico; `.bat` doppi o di un giorno solo) | `scripts/archivio/` (elenco e motivi in `LEGGIMI.txt`) |
| Due `.bat` quasi uguali per aggiornare il Pi | uno solo: `scripts\AGGIORNA_RACCOLTA_LEOPI.bat` (**non provato**: alla prima volta guarda il log) |
| Analisi, piano ed esito delle correzioni | `docs/archivio/correzioni_20ott/` |
| 6 rapporti del Risultato 6 prima delle correzioni; piani finiti (revisione mappa, rapporto GTT); rapporti di una volta; bozza telefonia | `docs/archivio/`, `docs/archivio/r6/`, `docs/archivio/idee/` |
| `immagini/` | esclusa da git |
| 63 commenti di lavorazione `[agente …]` (template della mappa, 04, 71) | tolti. Verificato: JavaScript, HTML e CSS del template sono **identici** a prima, commenti esclusi (confronto dell'albero del codice) |
| Riquadro «Carica altri risultati o scenari» in `simulazione.html` (trascina file JSON, vecchio formato del simulatore) | tolto. Provata in Chromium con schede di prova: stesse schede, finestra e inglese di prima, nessun errore |
| Stato in testa a `PIANO_RISULTATO2/4/6/9_*.md` e `PIANO_ACCESSIBILITA.md` | aggiornato (il Risultato 6 con i numeri corretti e i punti deboli) |
| Memoria | riscritta corta |

**Non fatto apposta**: cartella separata per i rapporti generati (hai scelto solo l'archivio); riunire i doppioni
di codice (distanze in 22 script): si passa a `comuni.py` solo quando si tocca uno script; script del traffico
(stampano «NON TORNANO» su numeri di oggi ma non fermano niente).

**Sul PC (Leo)**: cancellare il file `3)` nella radice e `scripts\*.bak_18ott`; il README nella radice va salvato
in git **dopo** aver rilanciato `python scripts\86_prepara_pubblicazione.py` (numeri ora con il punto).

## 4. Prossimi passi, in ordine

Criterio: prima ciò che **scade** o **sbaglia**, poi ciò che rende il portfolio **visibile**, poi ciò che lo
rende **più forte**, poi il nuovo.

| # | Cosa | Perché ora | Chi / quanto |
|---|---|---|---|
| 1 | **Unire il ramo di Claude in `prova`**, poi doppio clic su `scripts\RISULTATO6_RIFAI.bat` (rifà il Risultato 6 con i punti per asse, la mappa, le schede e prova le pagine) e `python scripts\86_prepara_pubblicazione.py` | Porta sul PC pulizia e correzioni, e le prova sui dati veri | Leo, 10 min |
| 2 | **Controllo di leopi ogni mattina** con `schtasks` (ora senza falso allarme) | Il 18/10 la raccolta si è fermata e ce ne siamo accorti dopo | Leo, 5 min |
| 3 | **Ora legale del 25/10**: controllo a mano dello script 26 dopo il fetch del 1/11 | Un'ora di dati 5T fuori posto per sempre, se sbagliata | Claude, 15 min |
| 4 | **Risultato 6**: Claude ricontrolla il nuovo giro (punti per asse); poi confronto delle auto in entrata con i sensori 5T del mattino | È il controllo con la realtà che manca | Claude, 1 sessione |
| 5 | **Pubblicare** su GitHub Pages (repository ora pubblico): ramo `gh-pages`, cartella leggera (oggi 90 MB), condizioni d'uso degli sfondi Esri, README | Senza questo nessuno vede il lavoro | 1-2 sessioni |
| 6 | **2-3 risultati di punta + «come sappiamo che è vero»** (rapporto GTT 2025, sensori e parcheggi 5T, la tua conoscenza). Candidati: Risultato 9 (attesa promessa contro reale: misurato, originale), Risultato 1 con la vulnerabilità («chi resta indietro»), Risultato 6 dopo il punto 4 | È la cosa che manca di più per la credibilità | 1 sessione a risultato |
| 7 | **Rilanci con più dati**: Risultato 6 dopo ≥ 5 feriali di parcheggi (inizio novembre, `RISULTATO6_RIFAI.bat`); Risultati 4 e 9 con un mese (metà novembre); poi Risultato 4 in mappa | Oggi 1-2 settimane di dati | `.bat` pronti |
| 8 | **Tempi del mezzo pubblico contro l'auto** per coppie di zone, poi **costi del viaggio** | Base comune per «auto in meno» e costi | 2-3 sessioni |
| 9 | Più avanti: treni SFM (GTFS regionale), uno scenario fra Risultato 3 e 5, lista dei luoghi «speciali», effetto ZTL, Corso Moncalieri, velocità 5T pulite in mappa | Utili, non urgenti | — |

## 5. Risposte di Leo (20/10, sera) e cosa ho fatto

1. **Pubblicazione**: Leo ha reso **pubblico** il repository `GTT`. Controllato: in git non ci sono chiavi o password
   (`chiave_deepseek.txt` è esclusa). Tutto il progetto (memoria, note, script) ora è visibile. Proposta per Pages:
   un ramo a parte (es. `gh-pages`) con solo il contenuto di `pubblica/`, rifatto a ogni pubblicazione, così la
   mappa da 13 MB non si accumula nella storia di `prova`. Da decidere al passo «Pubblicare».
2. **Risultato 6**: un punto per asse, almeno 3 km dal centro, posti arrotondati → **fatto nello script 84** (e
   controlli nell'85). Dettagli in `docs/PIANO_RISULTATO6.md`. Da eseguire sul PC.
3. **Risultato 2**: numero in grande = quello severo (334.085) → **fatto** in `schede_risultati.py`.
