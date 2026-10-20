# Esito R4 - Giro 2 (21/10/2026)

Partenza: ramo `prova`, working tree pulito, `git pull` ok. `MEMORIA_PROGETTO.md` non toccata. Le uscite di oggi restano: il rapporto
`RAPPORTO_RISULTATO4.txt` nuovo **inizia con il testo di prima identico** (verificato: il vecchio è un prefisso del nuovo; stessi numeri,
feriale 5,2% su 1.150.666 passaggi, periodo 10-20/10, 7 feriali, 2 sabati, 2 domeniche); le aggiunte stanno in coda. Nel rapporto R9
l'unica differenza oltre alla coda nuova è l'ordine di due righe di «dati scarsi» a pari valore (ordine non fissato già prima).
Per scrivere gli script con le parti lunghe ho usato file di appoggio nello scratchpad (il guscio rifiutava i blocchi con apostrofi): nessun file del
progetto in più.

## Riepilogo
| Passo | Esito |
|---|---|
| 1. Script 27 (modo, oltre 10 min, tram/bus, fine corsa, linee utili) | OK, con **un AVVISO importante sull'oltre 10 minuti** (sotto) |
| 2. Script 70 (attesa per modo) | OK |
| 3. Script 04 (dati `r4` per la mappa) | OK: 90 linee con dati |
| 4. Template della mappa (link `#linea=`, tema «Puntualità delle linee», legenda, tooltip) | OK, provato nel browser |
| 5. `simulazione.html`: link nelle barre | OK |
| 6. `schede_risultati.py`: link, grafici, numeri, inglese, mappa | OK |
| 7. Lanci e prova delle pagine | OK: 0 errori su 13 pagine (il tema `puntualita` c'è) |

## AVVISO principale: «oltre 10 minuti» misurato = 0
La regola D3 dello script 27 scarta i passaggi la cui ultima lettura è più lontana di 10 minuti dall'arrivo stimato. Controllato su un giorno
(15/10): tra i passaggi **usati** il ritardo massimo è 9,98 minuti, quindi la misura «oltre 10 minuti» esce **esattamente 0** (0 passaggi su
1.150.666) in ogni tipo di giorno, per tram e bus e per linee utili e altre. Non è «nessuno è in ritardo di 10 minuti»: i ritardi lunghi sono
quelli scartati da D3 (ultima lettura lontana dall'arrivo). Non ho cambiato D3 (D1-D9 «non modificabili»). Ho aggiunto, solo
informativo, il conteggio degli scartati: **feriale, 49.818 scartati per lettura lontana, di cui 34.929 con ritardo oltre 10 minuti**.
Includendoli (stima alta, letture non definitive) l'oltre 10 minuti feriale sarebbe **2,91%**, dello stesso ordine del **2,3%** di GTT per il 2025.
Il rapporto, il JSON (`lettura_lontana_per_tipo`) e la scheda lo dicono («0,00% tra i misurati, 2,91% includendo gli scartati: stima alta»).
Da decidere con Leo: se per l'oltre 10 minuti serve una regola diversa (per esempio tenere le letture lontane quando il ritardo è già grande).

## Passo 1 - scripts/27_risultato4_regolarita.py (aggiunte)
- `carica_gtfs()` ritorna ora 6 valori (prima 3): `trip_info, nome_linea, prog, modo_linea, ultima_seq, km_corsa`. `modo_linea` da `route_type`
  (0 tram, 1 metro, altro bus; nel feed: 204 bus tipo 3, 9 tram, 1 metro, 1 tipo 7 = funicolare, contata come bus; nessun nome con due tipi).
  `stops.txt` per le coordinate, `comuni.haversine_m` per i km della corsa. `import comuni` aggiunto.
- Costanti: `SOGLIA_RITARDO_10 = 10.0`, `RIF_GTT_RITARDO10_PCT = 2.3` (con fonte nel commento e nei `parametri` del JSON), `FINE_CORSA_ULTIME = 3`,
  `MIN_FINE_CORSA = 100`, `MODI`.
- `agg_punt()` ha un sesto elemento (contatore oltre 10 minuti); `stat_punt` aggiunge `ritardo10` (due decimali; il piano non dice quanti) e `ritardo10_n`.
- JSON: `modi` (tram/bus per tipo di giorno, con regolarità sommata dalle linee del modo), `modo_linea`, `fine_corsa` per linea
  (`passaggi, ritardo_mediana, km_mediana, min_per_10km`), `linee_utili` (somme dei contatori, non medie), `n_linee_utili`, `corse_fine`,
  `lettura_lontana_per_tipo`. La chiave delle linee utili in `popolarita_zone.json` è `linee[].utile` (booleano) con `linea`.
- Rapporto in coda: «OLTRE 10 MINUTI», «TRAM CONTRO BUS (feriale)», «RITARDO A FINE CORSA», «LINEE UTILI CONTRO ALTRE».
- Controlli (a schermo): tram + metro + bus = città in ogni tipo di giorno **OK**; oltre 10 ≤ oltre 5 **OK**; corse con almeno un passaggio di
  fine corsa **88,5% (49.171 su 55.538) OK** (soglia 30%); linee utili 54 **OK**.

### Numeri (feriale)
- Oltre 5 minuti: 5,2% città; **tram 4,6%, bus 5,4%**. Mediana ritardo: tram -0,6, bus -0,4 min. Grappolo+buco: tram 13,8%, bus 8,4%.
- Sabato 7,0%, domenica 5,4% (oltre 5 min).
- **Fine corsa**, 3 linee con più minuti ogni 10 km: **6 (2,7 min/10 km; corsa 4,3 km, ritardo a fine corsa 1,2 min), 19 (1,9; 5,9 km), 60 (0,9; 6,0 km)**;
  seguono 17, 132, 33, 74, 76, 72, 61. Le prime sono linee corte: il rapporto minuti/km le favorisce (vedi il rapporto per l'elenco intero).
- **Linee utili contro altre**: in ritardo oltre 5 min 5,6% contro 4,4%; grappolo+buco 11,1% contro 8,1%.

## Passo 2 - scripts/70_risultato9_attesa.py
`carica_gtfs()` adattato ai 6 valori; legge `modo_linea` da `risultato4_regolarita.json` (se manca: AVVISO su stderr e niente blocco);
`aggrega(..., modo_linea=None)` aggiunge `"modi"`; rapporto in coda «ATTESA PER MODO (feriale)»: **tram** promessa 4,3 min, in più 0,6-1,1;
**bus** promessa 5,4 min, in più 0,6-2,3; metro: nessuna linea frequente con dati.

## Passo 3 - scripts/04_genera_mappa.py
Nuova `leggi_r4()` + `R4_FILE`; chiavi `r4` e `r4_meta` nei dati della mappa; stampa «puntualita': 90 linee con dati (almeno 200 passaggi per fascia)».
`"n"` è per tipo di giorno (totale passaggi), come da piano. Mappa 13.783.398 byte.

## Passo 4 - scripts/mappa_template.html
- `applicaLineaDaUrl()` (legge `linea=` dall'indirizzo, riempie `#filtroLinea`, accende Llinee, ridisegna), chiamata all'avvio e in `hashchange`.
- Tema `puntualita` dopo «Bus e traffico misurati» (inserito solo se ci sono i dati `D.r4_meta`), ramo di disegno prima di quello della velocità,
  `fasciaR4`, `r4Classe`, `legendaR4()`; legenda generica delle linee esclusa col tema; l'ora dello slider e il tipo di giorno aggiornano già la legenda.
- **Tooltip delle linee: esiste** (`velTipLinea`), l'ho esteso: «Linea N · X% in ritardo oltre 5 min (fascia)».
- Provato nel browser: `#tema=puntualita&linea=17` apre il tema, il campo linea vale «17», la legenda è corretta e cambia con l'ora (notte → riga
  «non misurata»; alle 8:00 la linea 17 è rossa, valore dei dati 10,6%).

## Passo 5 - simulazione.html
`graficoBarre`: se la voce ha `v.link` l'etichetta è un `<a class="barra-link">` (colore `--accent`, sottolineato solo al passaggio).

## Passo 6 - scripts/schede_risultati.py
`voce(..., link=None)`; `link_linea()`; classifiche con link e nota «Clicca una linea per vederla nella mappa.»; tre grafici nuovi (tram contro bus,
ritardo a fine corsa con link, linee utili contro altre); numero «Passaggi in ritardo oltre 10 min» nel feriale; righe nella risposta (oltre 10 minuti
con il 2,3 dalla costante del JSON e l'avvertenza di cui sopra, tram e bus, linee utili, attesa per modo); `"mappa"` della scheda; `in_english`
con gli stessi numeri. Scheda: 21 numeri, 11 grafici.

## Passo 7 - lanci
27 (≈ 2,5 min) → 70 → 04 → schede → `prova_pagine_r6.py --senza-screenshot`: **0 errori su 13 pagine**, `puntualita` provato, nessun identificatore non definito.
`mappa_torino.html` 13.783.398 byte (prima 13.763.259). Feriale in ritardo oltre 5 minuti: 5,2% (atteso circa 5,2%); oltre 10 minuti: vedi l'AVVISO.

`git status` prima del commit: modificati script 04, 27, 70, template, `schede_risultati.py`, `simulazione.html`, rapporti R4 e R9, `mappa_torino.html`;
nessun file di `data/` né `.bak`.
