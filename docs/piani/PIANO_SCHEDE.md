# Piano — schede dei risultati chiare e presentabili

Oggi ogni scheda (`risultati.html`, testi da `scripts/schede_risultati.py`) ha fino a **15 sezioni**: problema,
domanda, risposta (6 frasi lunghe), grafici, immagini, prima/dopo, criteri a 4 colonne, verifica, affidabilità,
metodo, limiti, mappa, file del progetto, inglese, avviso. In testa «Fatto (12-14/10/2026)». Troppo testo, e parla
dello sviluppo («fase B», «giro», nomi di file).

## Forma nuova (uguale per tutti i risultati)

```
[etichetta MISURATO/STIMATO]                      Risultato N
TITOLO = la risposta in una frase                 (es. «Quasi tutti i torinesi hanno i servizi a 15 minuti»)
DOMANDA in una riga
NUMERO GRANDE + 1 riga di spiegazione
GRAFICO PRINCIPALE (uno, quello giusto)           + bottone «Vedi sulla mappa»
3 PUNTI CHIAVE (una riga ciascuno, con un numero)
▸ Altri grafici (al massimo 2, chiusi)
▸ Come l'abbiamo calcolato (5 righe + tabella dei criteri a 2 colonne: criterio, valore)
▸ Limiti (al massimo 4 righe)
▸ In English (3 righe)
```

Tolti dalla pagina: «Il problema» (va nella domanda), «Prima e dopo, numero per numero» (diventa un grafico se
serve), «Cosa cambia se lo cambiamo» (va nel documento del metodo), «File del progetto», stato con le date, avvisi
di sviluppo. Le date restano solo dove sono un dato («giorni misurati: ottobre 2026»).

Pagina indice: 4 riquadri (R1, R4, R6, R8) con titolo-risposta, numero grande e una piccola immagine della mappa;
il R2 resta nascosto.

## Il grafico giusto per ogni risultato

| Risultato | Grafico principale | Altri (chiusi) |
|---|---|---|
| **R1** servizi | **barre impilate** per soglia a piedi (5 / 10 / 15 minuti): quota di residenti con 5, 4, 3 o meno servizi. Mostra in un colpo «a 15' tutti, a 5' no» | quintili dei servizi contesi per circoscrizione; residenti esposti al traffico (una barra per classe) |
| **R4** puntualità | **barra a 100%** «come arrivano i mezzi» (anticipo / puntuale / ritardo 5-10 / oltre 10) per feriale, sabato, domenica | ritardo per fascia oraria (linea, non barre: è un andamento); «noi e GTT» (barre per definizione); 10 linee peggiori con link alla mappa |
| **R6** parcheggi | **mappa statica** dei 12 punti con il colore della classe (alto/medio/basso), oppure barre orizzontali dei punti per classe | riempimento degli interscambi esistenti (5 barre, giorno/notte); tempo TP contro auto per punto (dispersione) |
| **R8** traffico/TP | **dispersione** tempo auto (x) contro tempo coi mezzi (y) per le coppie di zone, dimensione = auto; linea «il doppio» | prova del modello sui sensori (misurato contro stimato, con l'errore %) |
| **R4 attese** (parte 2) | **barre affiancate** attesa promessa / attesa vera per fascia oraria | 10 linee con più attesa in più |

Regole dei colori di sempre: verde→rosso per bene/male, blu→arancione per quantità neutre, numeri sempre scritti.
Prima di disegnare i grafici nuovi seguire le indicazioni della skill di visualizzazione (`dataviz`): niente
torte, assi da zero per le barre, etichette dirette invece di legende.

## Testi

- Titolo = la risposta, non l'argomento («I ritardi gravi sono il 5% dei passaggi», non «Bus in ritardo e bus irregolari»).
- Frasi di massimo 20 parole; un numero per frase; niente sigle senza spiegazione (IMQ → «indagine sugli
  spostamenti 2022»; Q001-Q009 → «il centro»).
- Niente «Leo», «fase», «giro», «versione», nomi di script o di file nelle pagine.
- Inglese: 3 righe (domanda, risposta, limite principale).

## Passi

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Struttura nuova della scheda (sezioni sopra) e pagina indice | `risultati.html` | medio |
| 2 | Schema dei dati della scheda: campi nuovi `punti_chiave` (3), `grafico_principale`, `altri_grafici` (≤ 2), `criteri` a 2 colonne; via `stato`, `fonti`, `numeri` prima/dopo dalla pagina | `schede_risultati.py` | medio |
| 3 | Tipi di grafico che mancano: barre a 100% impilate, linea per andamento orario, dispersione | `risultati.html` | medio |
| 4 | Riscrivere i testi di R4 e R6 subito (i risultati non cambiano molto); R1 e R8 dopo `PIANO_RISULTATI.md` A e D | `schede_risultati.py` | medio |
| 5 | Immagini della mappa per l'indice (screenshot automatici di `prova_pagine_r6.py`, già nella cartella `immagini/`) | — | piccolo |
| 6 | README allineato alle schede (stessi titoli e numeri, letti dal JSON) | 86 | piccolo |

Prova: `python scripts\schede_risultati.py` e `python scripts\prova_pagine_r6.py`; Leo apre `risultati.html` e
controlla che ogni scheda stia in una schermata e mezza senza aprire le parti chiuse.
