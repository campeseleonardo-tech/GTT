# Esito — Risultato 6: direzioni d'ingresso, tre sottotemi, criteri spiegati

Piano eseguito: `docs/PIANO_R6_DIREZIONI.md`. Ramo `prova`, **nessun commit**, nessuna libreria nuova.
Dati e database in sola lettura. Lavoro del **19/10/2026** (ore 16:07-16:30 circa).

L'esito precedente (`docs/ESITO_R6_PORTE.md`, «porte = zone IMQ») è **superato**: il piano nuovo
sostituisce la domanda, le categorie, il tema della mappa e la scheda. Restano valide le parti
richiamate dal piano: parcheggi considerati, posti nominali, stato di riempimento, osservazioni a mano,
tipi di grafico, colori, regole di lavoro.

- **FASE 1: OK**
- **FASE 2: OK**
- **FASE 3: OK** (verifica nel browser)
- **FASE 4: OK**
- **FASE 5: OK**

## FASE 1 — `scripts/80_porte_interscambio.py` (riscritto)

Le «porte» sono ora **8 direzioni d'ingresso** (settori di 45° attorno a Piazza Castello, 0 = Nord in
senso orario). Ogni fermata, parcheggio e zona cade in una sola direzione (niente doppi conteggi).
Le auto in entrata per direzione vengono dai microdati IMQ 2022 con la funzione `zone_c2_c3()` dello
script 73 (in auto al mattino, zona di origine non «Q», arrivo «Q»); la direzione di una zona è quella
del baricentro del suo contorno (`imq_zone_geo.json`). **Decisione:** le 378 fermate importanti le leggo
da `scenari.json` (`scenari.S2.critici`) unito a `luoghi.json`, non da `mappa_r6.json`: quel file viene
riscritto dalla FASE 2, quindi leggerlo qui sarebbe circolare (i 378 id sono gli stessi).

Scritti: `data/processed/risultato6_v2/porte.json`, `docs/RAPPORTO_R6_PORTE.txt`.

**Controlli (tutti OK):** 378 fermate importanti; fermate senza/pochi/50+ = **147/59/172**; somma
`auto_in_entrata` = **95.298** (95.297 ±1); somma `domanda` = **24.459**; ogni parcheggio della mappa in
una sola direzione; somma `posti_utili` delle direzioni = somma dei parcheggi; nessun valore negativo.

**Tabella delle direzioni** (ordine di auto che non trovano posto):

| Direzione | Auto in entrata | Domanda | Posti nominali | Posti utili | Copertura | Categoria | Senza | Pochi | 50+ | Mancano |
|---|---|---|---|---|---|---|---|---|---|---|
| Nord-est | 15.247 | 3.913 | 1.654 | 1.544 | 40% | Pochi | 1 | 3 | 6 | 2.369 |
| Sud-est | 9.146 | 2.347 | 1.065 | 762 | 32% | Pochi | 0 | 2 | 5 | 1.586 |
| Nord-ovest | 8.984 | 2.306 | 2.308 | 1.855 | 80% | Quasi | 16 | 5 | 11 | 451 |
| Est | 3.002 | 771 | 727 | 474 | 62% | Quasi | 0 | 0 | 1 | 297 |
| Nord | 7.927 | 2.035 | 3.162 | 2.316 | 114% | Bastano | 4 | 2 | 9 | 0 |
| Sud | 12.527 | 3.215 | 11.830 | 9.283 | 289% | Bastano | 34 | 21 | 53 | 0 |
| Sud-ovest | 14.102 | 3.620 | 7.429 | 6.162 | 170% | Bastano | 46 | 14 | 30 | 0 |
| Ovest | 24.362 | 6.253 | 11.889 | 7.458 | 119% | Bastano | 46 | 12 | 57 | 0 |

Direzioni per categoria: Bastano 4, Quasi 2, Pochi 2, Mancano 0. Auto che non trovano posto: **4.703**.
Quota dei posti con riempimento misurato o osservato: **42,3%**. Parcheggi sulla mappa: **349**.

**Fermi (45,0766; 7,5903) è nella direzione Ovest.** Con l'osservazione a mano la copertura è **119%**;
senza (`--senza-osservazioni`) è **158%**: la copertura **sale** togliendo l'osservazione, come chiede il
controllo. Fermi non è in «Pochi» né in «Mancano».

**Sensibilità** (categorie delle direzioni), calcolata dallo script:

| Variante | Bastano | Quasi | Pochi | Mancano |
|---|---|---|---|---|
| quota 15% | 6 | 2 | 0 | 0 |
| quota 26% (usata) | 4 | 2 | 2 | 0 |
| quota 40% | 2 | 3 | 3 | 0 |
| distanza 100 m | 2 | 3 | 1 | 2 |
| distanza 200 m (usata) | 4 | 2 | 2 | 0 |
| distanza 400 m | 6 | 2 | 0 | 0 |
| 20 m² a posto | 4 | 2 | 2 | 0 |
| 25 m² a posto (usato) | 4 | 2 | 2 | 0 |
| 33 m² a posto | 3 | 3 | 2 | 0 |
| 6 settori | 3 | 1 | 2 | 0 |
| 8 settori (usati) | 4 | 2 | 2 | 0 |
| 12 settori | 4 | 4 | 2 | 2 |
| soglia fermate 5/10/15% | **non calcolata**: non ci sono i punteggi di tutti i luoghi (`scenari.S2.punteggi` assente) | | | |

## FASE 2 — `scripts/79_dati_mappa_r6.py` (riscritto)

Legge `porte.json` e scrive `mappa_r6.json` con: `generato`, `fonti`, `etichette`, `direzioni` (8),
`fermate` (378), `parcheggi` (349), `criteri` (10), `riepilogo`. Rimossi `porte`, `poligoni`, `luoghi`,
`eventi`, `ufficiali`, `zona_centrale`, classi e scenari.

Peso: **278.038 byte (272 KB)**, sotto il limite di 1,5 MB. Controlli: si carica con `json.load`;
8 direzioni, 378 fermate (147/59/172), 349 parcheggi, 10 criteri.

## FASE 3 — Mappa (`scripts/mappa_template.html`, `scripts/04_genera_mappa.py`)

Tema `interscambio` rifatto (stesso id e stesso link `#tema=interscambio`), con **tre sottotemi** nel
menu «Cosa vedere» (opzione `r6Vista`, rimessa in `OPZIONI`/`OPT_VAL`/`HANDLERS`):

- **parcheggi** «I parcheggi che ci sono»: solo i parcheggi con ≥50 posti (più quelli pieni), cerchio
  `3+√posti/6` (max 14 px), colore = riempimento di giorno (verde `#1a9850`, ambra `#fee08b`, rosso
  `#d73027`, grigio `#9aa3b2` = non misurato), bordo bianco, **tratteggiato** se i posti sono stimati.
- **non_bastano** «Dove i parcheggi non bastano»: gli **8 spicchi** (raggio 22 km) attorno a Piazza
  Castello, con **una sola scala sequenziale** (Bastano `#f3efe6`, Quasi `#f6d9a8`, Pochi `#ee9f5b`,
  Mancano `#c0562b`); etichetta nome+categoria **sempre visibile**; sopra, solo i **parcheggi pieni**
  (puntino nero).
- **mancano** «Dove non ci sono parcheggi»: solo le fermate con **0 posti** (viola scuro `#7b2d8e`,
  6 px) o **1-49 posti** (viola chiaro `#d99ac9`, 4 px); le 15 più importanti hanno il **numero 1-15**
  dentro il cerchio, elencate nella legenda.

La descrizione del tema e la legenda cambiano con la vista (una sola scala di colori per vista, con i
numeri sempre scritti). Il clic apre la scheda della **direzione** (dentro lo spicchio), della **fermata**
o del **parcheggio**, solo per gli elementi della vista attiva; il cerchio di 200 m compare attorno
all'elemento scelto (resta in `disegnaR6Sopra`, così il clic non ricalcola lo sfondo). Guida riscritta
(cosa sono le fermate importanti, come si contano i posti, come si stimano le auto, le categorie, il
rimando alla scheda).

**Decisione** (per rispettare «etichetta sempre visibile»): il nome del settore è messo al 60% del
raggio, ma se quel punto cade fuori dallo schermo viene **agganciato al bordo** invece di sparire.

**Banner d'errore** («drawImage … width or height of 0»): in `disegna()` ora si esce senza disegnare se
il canvas (destinazione o sorgente) ha misura zero, richiamando `chiede()` (così ridisegna al prossimo
`ridimensiona`). Verificato nel **browser integrato** (pagina servita da `http://localhost:8765`):
`mappa_torino.html#tema=interscambio` e `#tema=servizio` si aprono **senza banner** (`#jsoff` resta
`none`) e con **console vuota** (nessun errore). Le tre viste cambiano descrizione e legenda; il clic
apre le schede di direzione (es. «Sud-ovest — Nichelino, Orbassano, Beinasco»), fermata (es. «Fermata
1985 - COSSA OVEST») e parcheggio (es. «FORTINO, 125 posti»). Ho anche fatto uno screenshot della vista
«non bastano» (spicchi + legenda): ok.

`04_genera_mappa.py`: messaggio a stampa aggiornato («8 direzioni, 378 fermate importanti, 349
parcheggi»). Rigenerata **mappa_torino.html: 23.630.086 byte (23,6 MB)**. `node --check` su tutti i
blocchi `<script>` di `mappa_torino.html` e `simulazione.html`: **OK**.

## FASE 4 — Scheda (`scripts/schede_risultati.py`, `simulazione.html`)

`scheda_r6` riscritta sul nuovo file: **domanda**, **risposta in 4 frasi** (95.298 auto in entrata,
24.459 che potrebbero lasciarla; le direzioni più scoperte Nord-est 2.369 / Sud-est 1.586 / Nord-ovest
451; su 8 direzioni 2 «Pochi» e 0 «Mancano»; 147 fermate senza parcheggio e 59 con meno di 50; 17
parcheggi pieni, 5.440 posti, misure sul 42,3% dei posti), **numero chiave** = **4.703 auto**,
**6 grafici** (mancano più posti; auto che potrebbero lasciare l'auto e posti utili; fermate e parcheggi
a 200 m; fermate senza parcheggio per zona; profilo 24 ore; parcheggi già pieni), **2 immagini** (le fa
Leo), **metodo** (6 frasi), **parametri**, **limiti**, **mappa**, **fonti**, un blocco «Oggi» con 6
numeri.

**Nuova sezione «I criteri, uno per uno»** in `simulazione.html` (`apri()`): se `s.criteri` è un array
non vuoto, compare una **tabella a 4 colonne** (Criterio · Valore usato · Perché · Cosa cambia se lo
cambiamo) dopo «Prima e dopo, numero per numero» e prima de «Il metodo»; su schermo stretto le righe
diventano blocchi. `criteri` vengono da `porte.json` (script 80).

Controlli: `python scripts\schede_risultati.py` OK; `node --check data\schede_risultati.js` **OK**. La
scheda R6 **non** contiene «versione», «scenario», «S2», «potenziale», «solo sulla carta», «Allianz»,
«doppio» (verificato sul JSON e sul testo reso). Nel browser integrato la scheda si apre, la sezione
criteri ha le 4 intestazioni e 10 righe, e ci sono i 6 grafici.

**Decisione:** nei testi pubblici non compare mai «ufficiali» come classe (i 5 interscambi sono contati
nella voce «Parcheggi contati» come «interscambi 5»).

## FASE 5 — Pulizia

- Nessun resto di `porte`/`poligoni`/`r6Insieme`/`r6Raggio`/`r6Coperto` nel tema R6 (le occorrenze di
  «poligoni» nel template sono dei temi Catalogo e altri, non del R6). In `mappa_r6.json` non esistono
  campi `porte`/`poligoni`: «porte» compare solo nel nome file `porte.json` dentro `fonti`.
- «Barriera di Milano» compare solo come **nome di zona IMQ** (Q018), non come vecchia «porta».
- In `mappa_torino.html` e `data/schede_risultati.js` i termini «versione»/«scenario» compaiono solo
  nelle schede **di altri risultati** (R4, R8, R9), non nel Risultato 6.
- Non ho cancellato nulla dei giri precedenti (`data/processed/risultato6_v2/giro1/`, `RAPPORTO_R6V2_*`,
  gli esiti precedenti restano). Non ho creato file inutili nel repo: le prove stanno in `%TEMP%`.

## File modificati, rigenerati, nuovi

- **Modificati:** `scripts/80_porte_interscambio.py` (riscritto), `scripts/79_dati_mappa_r6.py`
  (riscritto), `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`,
  `simulazione.html`.
- **Rigenerati:** `data/processed/risultato6_v2/porte.json` (292.780 byte),
  `data/processed/risultato6_v2/mappa_r6.json` (278.038 byte),
  `data/processed/risultato6_riepilogo_mappa.json`, `mappa_torino.html`, `data/schede_risultati.js`.
- **Nuovi:** `docs/RAPPORTO_R6_PORTE.txt` (rifatto), `docs/ESITO_R6_DIREZIONI.md` (questo file).
- **Non toccati:** `MEMORIA_PROGETTO.md`, `data/ref/*`, i dati dei giri precedenti.

## Anomalie e limiti aperti

1. Con 8 settori le direzioni sono grandi: **nessuna è in «Mancano»** e le auto che non trovano posto
   scendono a **4.703** (con 12 settori comparirebbero 2 direzioni «Mancano»; con la distanza a 100 m,
   2). Non è un errore: è l'effetto del raggruppamento, ed è scritto nei criteri della scheda.
2. La soglia delle fermate importanti (5%/10%/15%) **non è calcolabile**: in `scenari.json` manca la
   chiave `scenari.S2.punteggi` (i punteggi di tutti i 4.425 luoghi). Nel criterio è scritto «non
   calcolato».
3. `Fermi` resta in «Bastano» anche con l'osservazione a mano: il controllo richiesto (copertura che
   sale senza l'osservazione) è soddisfatto (119% → 158%), ma non cambia la categoria.
4. Il banner d'errore è stato verificato nel browser (nessun banner, console vuota) su
   `#tema=interscambio` e `#tema=servizio`; dopo l'ultima rigenerazione non ho potuto rifare gli
   screenshot (la finestra del browser era nascosta), ma il controllo `#jsoff` e la console restano puliti.
5. La memoria del progetto **non è aggiornata**: il piano lo vieta (lo fa Claude a fine giro).
