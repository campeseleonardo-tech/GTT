# Esito del giro L20 (25/10/2026, sul PC di Leo)

Un solo esito per tutti i punti. Ogni numero viene dai file prodotti dagli script. Niente controlli grafici, niente telefono, niente scritture sul Pi.

## Prima

`git pull`, unione del ramo `claude/epic-clarke-6zdofk` (solo `PIANO_GRAFICA.md`, avanzamento rapido), push, `controlla_rami.py`: tutto allineato, nessun ramo con lavoro fuori da `prova`.

## 1. L13, scelta del mezzo (script 102): **non valutabile con la regola fissata**

- Regola (fissata prima dei numeri): viaggi dell'indagine IMQ in partenza dalle 6 alle 10 di un feriale, quota dei mezzi = mezzi / (mezzi + auto conducente + auto passeggero), coppie con almeno 30 interviste (viaggi che entrano nella quota), rapporto dei tempi TomTom alle 8, Spearman con intervallo al 95%.
- Coppie di zone diverse che raggiungono 30 interviste nella fascia: Torino-Torino **1**, Torino-cintura **0**, cintura-cintura **0** (su 2.719 coppie dello script 93). Con una coppia non si calcolano né la correlazione né l'intervallo. Risultato: né «regge» né «non regge»: **non valutabile**.
- Non ho cambiato la regola dopo aver visto il numero. La **variante a giornata intera** (non è la regola; solo informazione, nel JSON e nel rapporto): Torino-Torino: 57 coppie, Spearman -0,10, intervallo -0,36 / 0,17, non regge; Torino-cintura (e cintura-Torino): 15 coppie, Spearman -0,57, intervallo -0,91 / -0,06, regge; cintura-cintura: 17 coppie, Spearman -0,53, intervallo -0,81 / -0,01, regge. Per usarla in pagina serve una regola nuova, decisa da Leo, non scelta guardando questi numeri.
- Scheda 4: nessun punto chiave e nessun grafico nuovi (non c'è un risultato da dire). Una riga fra i limiti dice che la prova non ha esito; per fare posto ho tolto il limite «la stima dei sensori non conta semafori e incroci» (già nella riga del calcolo sui sensori). `docs/R8_traffico.md`: sezione nuova. Script aggiunto a `rifai_tutto.py` dopo il 93; `comuni._come_rifare` riconosce i file di `data/processed/imq/`.

## 2. L14, scheda 6 «Quanto costa muoversi» (script 103)

- Dati (`data/ref/costi.json`, con fonte, indirizzo e data): carburante self a Torino (media di 107 impianti entro 5 km da Piazza Castello, 24/10/2026) benzina 2,004, gasolio 2,249 euro al litro; Golf VIII 115 CV, consumo in città 7,2 (benzina) e 6,2 (gasolio) litri ogni 100 km, costo ACI 2026 0,5568 e 0,5047 euro al km; GTT biglietto 2,00, abbonamento mensile 38, annuale 310; sosta ZTL centrale 2,80, ordinaria 1,70, ridotta 1,50, smart 1,20 euro l'ora.
- **Fonte del carburante, deviazione dalla regola**: la regola chiedeva la media delle ultime 4 settimane; il sito dei CSV del Ministero (mimit.gov.it) non risponde da questo PC (connessione rifiutata), l'interrogazione di zona dà solo il prezzo del giorno. Si usa il prezzo del 24/10 e si scrive nei limiti; le medie nazionali del Ministero (6-21/10) sono stabili entro 0,02 euro. Il servizio non dà il comune: il cerchio di 5 km sostituisce «impianti della Città di Torino».
- Numero grande: **269 euro in più al mese** in auto per andare al lavoro in centro (mediana dei 12 punti del risultato 6): auto che si sente 307, mezzi 38; costo pieno 404 (differenza 366). Titolo: «Per andare al lavoro in centro l'auto costa circa 270 euro al mese più dei mezzi pubblici».
- Il parcheggio pesa più del carburante: 13,60 euro al giorno di sosta contro circa 1,76 di carburante. Tempo contro soldi: 11 minuti in più coi mezzi (mediana). Commissione di 2 ore: auto 5,16 euro (piena 10,00), mezzi 4,00.
- Coppie Torino-Torino (506), senza parcheggio, lavoro al mese per fascia di distanza: 52 coppie, auto 14 (piena 53); 191 coppie, auto 25 (piena 94); 207 coppie, auto 44 (piena 164); 56 coppie, auto 64 (piena 241), mezzi 38.
- **AVVISO, controllo con TomTom**: 11 dei 17 percorsi hanno una lunghezza oltre il ±10% da quella di TomTom (la nostra rete è spesso più corta, fino a −40% su Regina Margherita). Pesa poco sul risultato (il parcheggio vale quasi tutto il costo); scritto nei limiti della scheda e in `docs/R12_costi.md`. Sono 17 richieste TomTom di sola lunghezza.
- Cintura: tariffe a zone non assegnate alle zone dell'indagine, la scheda resta su Torino e sui punti del risultato 6 (AVVISO, come previsto dal blocco).
- Scheda: forma completa (domanda, numero grande con `breve`, `chiave`, 3 punti chiave di al massimo 25 parole, grafico principale a barre affiancate con il costo pieno come barra chiara, 3 altri grafici, calcolo, limiti, inglese in `testi.json`); animazione nuova «contatori» (due costi in euro che salgono insieme mese per mese, senza comandi, con «riduci movimento» finale subito); `r/6.html`, anteprima `r6.jpg`, README (sei risultati), home a 6 riquadri (3 + 3 dallo stile esistente). Prova nuova `design_l20` in `prova_pagine.py`.
- `docs/R12_costi.md`; script 103 in `rifai_tutto.py` (fase r6, dopo 94 e 100); i prezzi si rifanno a mano. `docs/FONTI_DATI.md`: nuova sezione delle fonti dei costi.

## 3. Scheda 5

La domanda è solo la seconda parte: «Chi vive dove i servizi sono pochi e le difficoltà sociali sono alte?» (inglese in `testi.json`; anche nel README e in `r/5.html`).

## 4. E4, velocità dei bus (script 104)

- Regole come da piano: stesso calcolo del livello «Velocità» della mappa (riuso di `calcola_velocita`), feriali del periodo fisso (2026-10-10 / 2026-10-22, 9 feriali), media pesata sui rilevamenti, ora per ora 5-24, bus e tram. Bus e tram si riconoscono dal tipo di linea del GTFS usando il codice della linea del feed (= `route_id`; 3 codici senza tipo contati come bus). Controlli: velocità 5-40 km/h e almeno 1.000 rilevamenti per ora: tutti OK, 0 avvisi.
- **Alle 8 un bus va in media a 13,0 km/h** (tram 11,1, insieme 12,6). Più lenti: ore di punta (17: 12,8); più veloci: le prime ore (5: 18,8).
- Scheda 2: punto chiave «Alle 8 di un feriale un bus va in media a ~13 km/h, fermate e semafori compresi.» **al posto di** «Guardando solo la partenza dal capolinea, i passaggi con oltre 10 minuti di ritardo sono ~5%»: era il più debole per chi legge (una variante di calcolo, già nelle righe del confronto e del calcolo); grafico a linea ora per ora fra gli «altri grafici»; riga nel calcolo. `docs/R4_puntualita.md`: sezione nuova.

## 5. Rilancio e prove

- `04_genera_mappa.py` (mappa 5.960.871 byte, entro il limite), `schede_risultati.py` (nessuna ATTENZIONE), `86_controlla_file_pagine.py` (0 avvisi), immagini del README e anteprime `r/N.html` rifatte da `prova_pagine.py --playwright`.
- `python -m pyflakes scripts`: zero. `node --check assets\*.js`: zero errori. `prova_pagine.py --playwright`: 0 errori su 20 pagine; prove L15 (ora schede 1-6, IT e EN), L16, L17, L18 e la nuova L20 tutte OK; link «Vedi sulla mappa» OK.
- Non fatti: `RIFAI_MAPPA_E_SCHEDE.bat` come file (ho lanciato gli stessi quattro passi uno per uno); non ho rilanciato i risultati lunghi (nessun dato di base è cambiato).

## 6. Prova da zero con la Release: **saltata**

La Release `dati-2026-11` non è pubblicata: l'indirizzo del tag risponde 404 e su GitHub è pubblicata solo `dati-2026-10` (la bozza non si vede). `scarica_dati.py` prende ancora la vecchia. Da fare dopo la pubblicazione (clone in una cartella temporanea, `scarica_dati.py`, `rifai_tutto.py --solo schede`).

## 7. Pulizie

Il file «3)» e `scripts\*.bak_18ott` non ci sono. `git status` pulito prima dei commit (niente `data\` fuori dalle regole, niente `.bak`, niente chiavi). `data/fonti_costi/` (ACI, risposte del servizio carburanti) è fuori da git. L'inventario `docs/DATI.md` e `.gitignore` sono stati rifatti dallo script 96.

## 8. Memoria e commit

Memoria aggiornata (120 righe). Un commit per passo, `git push origin prova` dopo ognuno.

## 9. Unione in `main`: **NON fatta**

Tutte le prove tecniche sono verdi, ma prima di unire ho letto le condizioni d'uso di TomTom (https://docs.tomtom.com/legal/terms-and-conditions), che la memoria e `docs/FONTI_DATI.md` indicavano come condizione per `main`. Le clausole rilevanti:
- **11.4**: il salvataggio (caching/storing) dei «Results» è vietato, salvo cache nel client e per il tempo indicato dalle intestazioni di controllo;
- **11.6.1**: è vietato estrarre o riusare i dati per creare un database secondario o derivato.
Il progetto salva e pubblica statistiche derivate dalle risposte TomTom (rapporti per gruppo e ora, fattori per percorso a due decimali, rapporti dei tempi nelle schede 3 e 4 e nella mappa). Non è un parere legale, ma la lettura più semplice è che c'è un conflitto, e `main` pubblica il sito su GitHub Pages. Per questo **non ho unito**: la decisione è di Leo (scrivere a TomTom per un permesso, oppure togliere da git e dal sito i numeri derivati da TomTom e ripiegare sui sensori 5T). Lo stesso vale per i 17 confronti di lunghezza di questo giro.

## Da guardare (Leo, computer)

Home a 6 riquadri (3 + 3); scheda 6 (animazione dei contatori, grafico principale, «Tempo contro soldi», parte chiusa); scheda 4 con la riga nuova fra i limiti; scheda 2 (punto chiave dei bus e grafico delle velocità); scheda 5 con la domanda nuova; mappa (peso 5,96 MB); `r/6.html` e le anteprime.
