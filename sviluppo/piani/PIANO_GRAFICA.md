# Piano 4 — Grafica, animazioni e racconto

Obiettivo: il sito colpisce nei primi 5 secondi e fa capire i risultati anche a chi non legge i testi.

Decisioni di Leo (22/10):
- i colori verde→rosso e blu→arancione erano una **direzione**, non una regola: si passa a **verde acqua → corallo**
  (non prioritario);
- **un file di stile** comune a tutte le pagine;
- **numeri che contano** solo nei numeri grandi e molto visibili, non in tutti (altrimenti dà fastidio);
- **omini e quadratini**, **gara bus contro auto** e **area che si espande** dentro le **schede**;
- **ore che scorrono** nella mappa; **mezzi in movimento** in home;
- il racconto «perché questo progetto» in una **pagina a sé**: `progetto.html`;
- sito in italiano con bottone **IT/EN** su home, risultati e progetto (la mappa resta in italiano).

Regole che restano: **numeri sempre scritti** accanto ai colori; animazioni spente per chi ha attivato «riduci movimento»
nel sistema; pagine che funzionano anche senza le animazioni.

## Dove va ogni elemento

| Elemento | Cos'è | Dove |
|---|---|---|
| **A. Mezzi in movimento** | sfondo scuro con la forma di Torino; i puntini di bus e tram veri (GPS del Pi) si muovono durante un'ora tipica, accelerata in circa 20 secondi, con l'orologio che scorre | **home**, in alto dietro il titolo |
| **B. Numeri che contano** | il numero sale da 0 al valore in circa 1 secondo quando appare | **solo**: il numero di ognuno dei 5 riquadri della home, il numero grande della scheda aperta, il contatore della raccolta (J). Nessun altro numero |
| **C. Omini e quadratini** | il numero grande disegnato: 10 omini con 1 colorato (scheda 5, «quasi 1 su 10»); 100 quadratini con 13 corallo (scheda 2, passaggi oltre 5 minuti); 12 pallini, uno per punto (scheda 3) | **scheda aperta**, sotto il numero grande |
| **D. Gara bus contro auto** | bus e auto partono insieme da uno dei 12 punti verso Piazza Castello; l'auto arriva prima, il bus dopo; tendina per scegliere il punto; i minuti scritti all'arrivo | **scheda 3** (parcheggi di scambio), grafico principale. Dati già pronti (script 94) |
| **E. Area che si espande** | due aree che crescono minuto per minuto: dove arrivi in 10, 20, 30, 45 minuti **coi mezzi** e **in auto**, alle 8. Si parte da **Piazza Castello**, con una tendina per scegliere **qualsiasi altra zona** (Leo, 22/10) | **scheda 4** (traffico e mezzi). Piazza Castello in dettaglio (per sezione: calcolo nuovo sul PC); le altre zone con i tempi zona-zona già calcolati dallo script 93 (controllare che il JSON abbia tutte le coppie, altrimenti il 93 salva la tabella completa) |
| **F. Ore che scorrono** | bottone ▶ che fa scorrere le ore dalle 6 alle 24 con passaggi morbidi di colore | **mappa**, nei temi che cambiano con l'ora |
| **G. Perché questo progetto** | pagina a scorrimento: testo a sinistra, disegno a destra che cambia a ogni paragrafo; traccia sotto | **`progetto.html`**, link dalla barra in alto e in fondo a `risultati.html` |
| **H. Stile** | `assets/stile.css` comune; font salvati in `assets/`; verde acqua → corallo; modo scuro; icona del sito; anteprima per i link condivisi (immagine 1200×630, titolo, descrizione) | **tutte le pagine**; il pannello della mappa lo segue |

### Aggiunte proposte nell'analisi del 22/10

| Elemento | Cos'è | Dove |
|---|---|---|
| **I. Barra e piè di pagina comuni** | in alto: Home · Risultati · Mappa · Il progetto · IT/EN. In basso: «Chi sono» (nome, LinkedIn, email, GitHub), licenza, **«dati aggiornati al …»** | home, risultati, progetto (la mappa ha il suo pannello: lì solo il link «Il progetto») |
| **J. Contatore della raccolta** | «Il Raspberry Pi legge Torino da N giorni: X milioni di posizioni dei mezzi» (numeri scritti dallo script delle schede) | **home**, sotto il titolo |
| **K. Miniature nei riquadri** | ~~immagine fissa del grafico~~ → dal 23/10 (Leo) l'animazione della scheda in piccolo; le immagini `assets/miniature/` si tolgono in L2 | home |
| **L. Caricamento della mappa** | mentre arrivano i 6 MB: il contorno di Torino che si disegna e una barra; la finestra delle schede si apre con una dissolvenza | mappa, risultati |
| **M. Mappa più comoda** | su telefono il pannello sale dal basso; schede dei temi uniformi (titolo = nome del posto, 3-5 righe, fonte in piccolo); «◎ Cintura» diventa «Tutta l'area»; ultime date e sigle tolte dal testo; bottone «copia il link di questa vista» | mappa |
| **N. Come funziona** | schema animato: sensori e GPS → Raspberry Pi → storico → script → pagine (i livelli dell'IoT della tesi) | `progetto.html` |
| **O. Pagina «non trovata»** | `404.html` nello stile del sito con i link alle pagine | radice |
| **P. Pagine dei singoli risultati** | `r/1.html` … `r/5.html`: pagine minime, scritte dallo script delle schede, con titolo, descrizione e immagine del risultato, che portano subito a `risultati.html#pN`. Un post su LinkedIn mostra la scheda giusta. Poco lavoro (Leo: sì, se resta poco) | radice, cartella `r/` |

### Traccia di `progetto.html`
1. **La promessa** (tesi del 2020): «sensori e dati cambieranno le città».
2. **Il sistema**: un Raspberry Pi che legge Torino ogni minuto (N, schema animato).
3. **Chi abita dove**: fragilità, poi servizi; le 5 zone in doppio svantaggio si accendono.
4. **Muoversi**: bus contro auto, in breve, con il link alle schede 3 e 4.
5. **Quanto ci si può fidare dei dati**: il feed dei ritardi che sbagliava di 2-3 volte, il bus con l'orologio 3 anni avanti.
6. **Cosa manca** (costi, passeggeri, treni) e **Chi sono**.

## Passi (in ordine)

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **FATTO (C4, Leo sceglie)**: 3 prove di stile su una pagina (`sviluppo/prove_stile.html`: «Notte», «Carta», «Torino»), con lo stesso riquadro, grafico e mappa piccola → Leo sceglie | CLOUD | piccolo |
| 2 | **FATTO (C5)**: H + I: `assets/stile.css`, font, icona, modo scuro, barra e piè di pagina, anteprima dei link; home e risultati nello stile nuovo; colori di mappa e schede ripensati insieme (verde acqua → corallo) | CLOUD | medio |
| 3 | **FATTO (C5)**: B + C + L (parte schede): numeri grandi che contano, omini e quadratini, dissolvenza della finestra | CLOUD | piccolo |
| 4 | **D** gara bus contro auto nella scheda 3 | CLOUD | medio |
| 5 | **FATTO (C6, Leo rilegge)**: testi IT/EN: dopo la divisione di `schede_risultati.py` (piano 5, passo 4), inglese completo delle schede; Leo rilegge | CLOUD | medio |
| 6 | **A + J + K** home: animazione dei mezzi (serve l'ora tipica: piano 2, passo 4, sul PC), contatore, miniature | CLOUD → PC → CLOUD | medio |
| 7 | **F + L + M** mappa: ore che scorrono, caricamento, pannello su telefono, schede dei temi, link della vista | CLOUD | medio |
| 8 | **FATTO nel cloud (C10), da calcolare sul PC (P6: `AREA_TEMPI.bat`)**: **E** area che si espande nella scheda 4: script 99, da Piazza Castello e da ogni zona di Torino | CLOUD (script) → PC (calcolo) → CLOUD | medio |
| 9 | **FATTO (C11, Leo rilegge i testi)**: **G + N** `progetto.html` | CLOUD | grande |
| 10 | **FATTO (C12)**: **O**, **P**; screenshot per il README (piano 1) | CLOUD | piccolo |

Prova di ogni passo: le pagine aperte in un browser senza schermo (0 errori, screenshot a misura di computer e telefono, anche
con «riduci movimento»); Leo guarda gli screenshot e poi le pagine vere sul PC.
Peso: home sotto 1 MB con l'animazione; mappa non oltre i 6 MB di oggi.

## Revisione di Leo (23/10) e come la applichiamo

Leo ha guardato home, schede e mappa dopo C7-C9. Gli piacciono il caricamento della mappa (la città che si disegna) e i mezzi in movimento in home.
Le sue modifiche, con le scelte di Claude dove Leo ha lasciato decidere (valori predefiniti, si cambiano con una riga):

**Home**
- «Torino Mobilità» in **oro**; sotto: «Un progetto per capire come si muove la città».
- Frase della raccolta, più generale: «Da **N** giorni raccogliamo, minuto per minuto, dove sono bus e tram e quanto traffico c'è sulle strade. E continuiamo.» + «Per capire chi va dove, e come ci va.»
  N = giorni dal primo giorno della raccolta (3/10/2026) a **oggi**, contati nella pagina: «e continuiamo» resta vero finché il Raspberry Pi raccoglie (la raccolta è sempre attiva).
- I 5 riquadri mostrano **la stessa animazione della loro scheda**, in piccolo, al posto delle miniature fisse (componente unico `assets/animazioni.js`, usato da home e schede).

**Numeri che salgono** (home e schede): più lenti (circa 2,5 secondi), partenza e arrivo morbidi; durante la corsa solo numeri interi, **senza virgola né %**:
la parte decimale e il % compaiono solo alla fine. Cifre a larghezza fissa e spazio riservato, così il testo intorno non si muove. Anche le forbici («21–28», «2–3») salgono.

**Schede**
- Via la parte «In English» (l'inglese resta col bottone IT/EN).
- Meno parti chiuse: domanda → numero grande con la sua animazione → grafico principale → 3 punti chiave → «Vedi sulla mappa» → **tutti gli altri grafici aperti**
  (anche quelli che prima stavano in una parte chiusa: attese, interscambi, strade grandi) → **una sola** parte chiusa «Come l'abbiamo calcolato e limiti» (calcolo, criteri, confronto, limiti).
- Titoli nuovi (Leo ha proposto, Claude ha ritoccato):

| Scheda | Titolo | Perché il ritocco |
|---|---|---|
| 1 servizi | «Torino, città dei 15 minuti: quasi tutti hanno i servizi a 15 minuti a piedi» | l'idea dei 15 minuti si chiama «città dei 15 minuti»; «smart city» è un'altra cosa (sensori e dati: è il racconto della pagina «Il progetto») |
| 2 puntualità | «Circa il 5% dei passaggi arriva con più di 10 minuti di ritardo» | «in ritardo» da solo è ambiguo: oltre 5 minuti sono il 14% |
| 3 parcheggi | «2 fermate importanti su 3 non hanno dove lasciare l'auto» | il risultato vero è quanto è facile lasciare l'auto e proseguire coi mezzi (Leo); i minuti di parcheggio diventano un punto chiave |
| 4 traffico | resta «Al mattino, coi mezzi pubblici si impiega da 2 a 3 volte il tempo dell'auto» finché non c'è il giorno intero (L3) | |
| 5 case | «Circa 1 torinese su 10 vive in una zona con più difficoltà sociali e pochi servizi» | «fragile» detto di persone suona male; «difficoltà sociali» descrive l'indice senza etichettare chi ci vive |

- **Animazioni** (tutte con «riduci movimento»: figura ferma e numeri scritti):
  1. **Servizi**: tre cerchi intorno a una casa, 5 → 10 → 15 minuti a piedi; ogni cerchio si apre col suo % (68 → 97 → 99).
  2. **Puntualità**: 100 quadratini che si accendono (ritardo oltre 5 minuti chiaro, oltre 10 scuro), poi **il giorno che scorre**: le 4 fasce orarie (punta del mattino, giorno, punta della sera, sera) cambiano i quadratini, con l'orologio. I dati per fascia ci sono già.
  3. **Parcheggi**: la forma di Torino, le 274 fermate importanti che compaiono e si colorano (posti bastanti / pochi / nessuno), poi i 12 punti prioritari che si accendono.
     La scheda cambia centro: numero grande = fermate senza posti bastanti (179 su 274), grafico principale = i 12 punti per bisogno; i minuti di parcheggio passano fra i punti chiave e gli altri grafici.
     La **gara bus contro auto** resta come secondo grafico e **gira da sola** da un punto all'altro (finita una corsa parte la successiva, col nome del punto); la tendina resta, piccola, per chi vuole scegliere.
  4. **Traffico**: l'area che si espande (C10, fatta) è l'animazione principale, anche in home; la gara sui viaggi tipici fra zone (le coppie con più auto del mattino), da sola, va negli altri grafici.
  5. **Case**: 10 omini che compaiono uno alla volta, poi uno si accende.

Come si fa: giro **L2** (agente in locale) in `PROMPT_LAVORI.md`, con la bozza di codice `C14_bozza.patch`. **Controlli grafici solo di Leo** (23/10).

**Non solo all'ora di punta** (schede 3 e 4, richiesta di Leo): oggi i tempi coi mezzi sono calcolati solo alle 8. Per l'auto abbiamo già il tempo a strada libera e le velocità
dei sensori 5T per ora; per i mezzi serve il calcolo a più ore (stesso motore degli script 93 e 94) → giro **L3** (agente in locale: script 100 e calcolo). Poi la gara
mostra le 4 ore una dopo l'altra (8, 13, 17:30, 21; scelte e regola del titolo nel blocco L3 di `PROMPT_LAVORI.md`) e la scheda 4 ha la linea «quante volte il tempo dell'auto, ora per ora». L'ora di punta resta il numero principale.
