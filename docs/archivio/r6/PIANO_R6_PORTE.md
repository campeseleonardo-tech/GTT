# Piano meccanico — Risultato 6 (versione finale): le «porte» della città e i posti per lasciare l'auto

Scritto da Claude il 19/10/2026 con Leo, per un altro modello (agente). **Sostituisce** `PIANO_INTEGRAZIONE_R6.md` per tutto ciò che riguarda tema della mappa, scheda ed eventi
(i colori verde→rosso / blu→arancione e i tipi di grafico `profilo`, `immagini`, `tono` già fatti **restano**).
Esegui **tutte le fasi di seguito, senza fermarti a chiedere**. Dopo ogni fase scrivi in `docs/ESITO_R6_PORTE.md` `FASE n: OK` o `FASE n: FERMO – motivo`.
Se un controllo numerico non torna: correggi se la causa è tua e chiara; altrimenti **non inventare**, scrivi cosa hai visto, salta quella parte e continua (le fasi che ne dipendono: «NON ESEGUITA – dipende da…»).
Claude controlla tutto nel browser alla fine.

## 0. Regole

1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (se no, FERMATI). **Nessun commit.** Python del PATH (3.14), non Anaconda. Nessuna libreria nuova. Dati e database in sola lettura.
2. **Puoi modificare:** `scripts/79_dati_mappa_r6.py`, `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`, `simulazione.html` (solo dove indicato). **Nuovi:** `scripts/80_porte_interscambio.py`, `docs/RAPPORTO_R6_PORTE.txt`, `docs/ESITO_R6_PORTE.md`. Non toccare: `MEMORIA_PROGETTO.md`, script 68-78, `data/processed/risultato6_v2/{luoghi,parcheggi,segnali,riempimento,scenari,nodi,parcheggi_funzione}.json`, `data/ref/*`.
3. `mappa_torino.html` e `data/schede_risultati.js` si **rigenerano** (`python scripts\04_genera_mappa.py`, `python scripts\schede_risultati.py`), mai a mano.
4. Dopo ogni modifica al template: estrai gli `<script>` di `mappa_torino.html` in un file in `%TEMP%` e `node --check`; anche per `simulazione.html` e `data\schede_risultati.js`. Non basta: gli errori di resa li vede Claude.
5. Distanze: haversine in metri. Italiano semplice, numeri con virgola decimale e punto delle migliaia. Etichette: [MISURATO] [PROGRAMMATO] [STIMATO] [OSSERVAZIONE di Leo] [DATI SCARSI].
6. **Versione finale, senza storia**: nei testi di mappa e scheda **mai** «v1», «v2», «versione», «scenario S1/S2/S3», «giro», né confronti con risultati precedenti. Eventi, classi dei parcheggi («di fatto», «solo sulla carta», «potenziale», «non interscambio»), zona centrale, insiemi di parcheggi, raggi 100/400 m: **non compaiono** né in mappa né in scheda.

## 1. Decisioni di Leo (19/10) — fisse

- **Domanda**: «Dove mancano posti per lasciare l'auto vicino ai punti dove si entra in città o nel trasporto pubblico?» Serve a capire **dove sarebbe più importante mettere un parcheggio o ingrandirne uno che c'è**.
- **Porta** = **zona IMQ** (cintura, resto della Città metropolitana, quartieri di Torino) che contiene almeno un «luogo critico». Si aggiunge, in modo uniforme per tutte le porte, l'informazione sulle **strade d'ingresso** (idea «asse d'ingresso»).
- Si contano **tutti i parcheggi aperti** (5T, Comune, OpenStreetMap), centro compreso, **posti nominali** (dichiarati, o stimati a 25 m² per posto); distanza fissa **200 m** dal luogo critico.
- **Riempimento**: dove misurato (5T) si usa; dove manca (es. Fermi, che si sa pieno) c'è una nota a mano; in più un **indice di pressione** (auto che potrebbero lasciare l'auto ÷ posti utili) uguale per tutte le porte.
- Luoghi critici = quelli di sempre (10% più alto del punteggio, centro Q001 escluso): nel testo pubblico si chiamano **«fermate importanti per chi arriva in auto»**.
- Colori: scala bene/male verde→rosso, categorie con colore proprio (già nel progetto).

## 2. Definizioni (da implementare esattamente così)

- **Luoghi critici**: i 378 di `data/processed/risultato6_v2/mappa_r6.json` → `luoghi_critici` (campi `id_luogo, nome, lat, lon, zona_imq, punteggio, segnali`). Non cambiare l'elenco.
- **Parcheggi considerati**: `data/processed/risultato6_v2/parcheggi.json`, tipi `interscambio_ufficiale`, `garage_5t`, `park_ride_osm`, `osm_pubblico` (3.431). `posti` = `posti_dichiarati` se c'è, altrimenti `posti_stimati`, altrimenti 0.
  `posti_origine` = «dichiarati» / «stimati (25 m² a posto, ±30%)» / «nessuno».
- **Stato di riempimento** di ogni parcheggio (primo che vale):
  1. **[OSSERVAZIONE di Leo]**: il parcheggio è entro `raggio_m` da un punto di `data/ref/parcheggi_osservazioni.json` → `stato = "pieno"`, `fonte` = quella del file;
  2. **[MISURATO]**: ha `id_5t` e in `riempimento.json` (lista `parcheggi`, chiave `id_5t`) c'è `G_giorno_feriale` (media feriale 10-16, 0-1) e giorni validi ≥ 2 → `stato`: `pieno` se G ≥ 0,85, `libero` se G < 0,50, altrimenti `a_meta`; `riempimento_giorno = G`;
  3. altrimenti `stato = "non_misurato"`.
- **Posti utili** = per `pieno` da osservazione: 0; per misurato: `posti × (1 − G)`; per `non_misurato`: `posti` (nominali). Arrotonda a intero solo alla fine.
- **Luogo critico → posti vicini**: parcheggi considerati entro **200 m** (nominali) e posti utili. **Assegna ogni parcheggio a un solo luogo critico: il più vicino entro 200 m** quando si somma per porta (niente doppi conteggi); per il singolo luogo si mostrano comunque tutti i parcheggi entro 200 m.
  Categoria del luogo (3 classi, nell'ordine): **«Nessun parcheggio vicino»** (0 posti nominali entro 200 m, rosso) · **«Pochi posti»** (1-49 posti nominali, arancione) · **«50 posti o più»** (verde).
- **Porta** = zona IMQ con almeno un luogo critico (esclusa nessuna). Per ogni porta:
  - `auto_in_entrata` = `c2` della zona **completato** come fa lo script 75 (cerca `c2_completo`/`istat2011` per le zone con meno di 30 interviste; per le altre il `c2` di `segnali.json`), `interviste`, `dati_scarsi` (< 30 interviste). Fonte [STIMATO] IMQ 2022. Nota nel testo: per i comuni di cintura sono le auto che **partono** verso Torino al mattino, per i quartieri di Torino quelle che **arrivano** dalla cintura;
  - `quota_interscambio` = `f.totale / c2_totale` di `segnali.json` (atteso ≈ 0,257: auto che oggi già cambiano con un mezzo pubblico; 299 interviste [DATI SCARSI]), **uguale per tutte le porte**, opzione `--quota-interscambio`;
  - `domanda` = `auto_in_entrata × quota_interscambio` (auto che potrebbero lasciare l'auto lì) [STIMATO];
  - `posti_nominali`, `posti_utili` (somma sui parcheggi assegnati alla porta), `posti_pieni_osservati_o_misurati`, `quota_posti_misurati` (quanti posti hanno stato misurato o osservato, in %);
  - `copertura` = `posti_utili ÷ domanda` e `mancano` = max(0, `domanda` − `posti_utili`) (auto);
  - **categoria** (4 classi): **«Bastano»** (copertura ≥ 1, verde) · **«Quasi»** (0,5-0,99, giallo) · **«Pochi»** (0,2-0,49, arancione) · **«Mancano»** (< 0,2, rosso);
  - `n_luoghi_critici`, `n_luoghi_senza_parcheggio`;
  - `dove_intervenire`: i 5 luoghi critici della porta **senza parcheggio vicino** (o con meno posti) con punteggio più alto (nome, punteggio, posti vicini) e i 5 parcheggi della porta **pieni** (osservazione o misura) con più posti (nome, posti, stato, fonte);
  - `strade_ingresso`: per ogni luogo critico della porta chiama `trova_strada(lat, lon)` del modulo `scripts/77_strade_comuni.py` (caricalo con `importlib`); tieni le strade con `asse_ingresso` vero; per ognuna, prendi dalla tratta il `veic_giorno` (`data/processed/traffico_d/tratte_traffico.json`, stima ±38%, due sensi); raggruppa per asse (campo `asse`) e riporta le **3 con più veicoli**: `nome` (solo per leggere), `classe`, `veic_giorno`. È solo informazione ([STIMATO]), non entra nell'indice. Se una porta non tocca nessun asse d'ingresso: lista vuota.
  - `poligoni`: contorni della zona da `data/processed/imq_zone_geo.json` (punti `[lat, lon]`), semplificati con `shapely.simplify(0.0002)` e arrotondati a 5 decimali; `nome` da `imq_zone.json` (campo `denom`, togli i prefissi numerici «01 Torino-»).
- **Classifica**: porte ordinate per `mancano` decrescente.

---

## FASE 1 — Script `80_porte_interscambio.py`

1. Leggi gli input della sezione 2. Scrivi `data/processed/risultato6_v2/porte.json` (porte, luoghi critici con posti vicini e categoria, parcheggi con stato e posti utili, riepilogo) e `docs/RAPPORTO_R6_PORTE.txt` (tabella di tutte le porte in ordine di `mancano`: nome, auto in entrata, domanda, posti nominali, posti utili, copertura, categoria, quota posti misurati, strade d'ingresso; poi i totali; poi i limiti).
2. **Controlli numerici** (scrivili nell'esito; se non tornano FERMO):
   - luoghi critici 378; parcheggi considerati 3.431; ogni parcheggio assegnato a **al più un** luogo critico nelle somme per porta;
   - `quota_interscambio` tra 0,25 e 0,27; nessun valore negativo; somma di `domanda` ≤ `c2_totale` × quota (± zone senza luoghi critici);
   - luoghi critici senza parcheggio entro 200 m (0 posti nominali): **147**; con 1-49: **59**; con ≥ 50: **172** (100 + 44 + 28). Se i numeri differiscono, riporta quelli trovati e **FERMO su questa fase**;
   - **Fermi** (zona **C003 Collegno**): scrivi `posti_nominali` e `posti_utili` della porta con e senza l'osservazione di Leo (lancia una volta con `--senza-osservazioni`) e la categoria nei due casi: con l'osservazione la copertura deve **scendere**;
   - Stura, Caio Mario, Porta Susa FS: `stato` misurato con `riempimento_giorno` come in `riempimento.json`.
3. Test del metodo (non è un errore se non torna, ma scrivilo): «Fermi risulta in categoria Pochi o Mancano?» e la lista delle 10 porte con più `mancano`.

## FASE 2 — Riscrivere `79_dati_mappa_r6.py` (file per mappa e scheda)

Il file `data/processed/risultato6_v2/mappa_r6.json` ora contiene **solo**:
- `porte` (tutti i campi della Fase 1, con `poligoni`);
- `luoghi` (378): `id, nome, lat, lon, zona_imq, punteggio, categoria, posti_nominali_200, parcheggi:[{id, nome, dist_m, posti, stato}]` (ordinati per distanza, max 6), `porta` (codice zona);
- `parcheggi` (solo quelli entro 200 m da almeno un luogo critico, e i garage 5T): `id, nome, lat, lon, posti, posti_origine, a_pagamento, stato, riempimento_giorno, fonte_stato, profilo_feriale[24] (da riempimento.json, arrotondato a 2 decimali, null se manca)`;
- `riepilogo` (per la scheda): numeri chiave (luoghi critici, senza parcheggio, pochi posti, 50+; auto in entrata totali; domanda totale; posti nominali e utili totali; mancano totali), porte per categoria (conteggi), top 10 porte per `mancano`, top 10 luoghi senza parcheggio per punteggio, parcheggi pieni (misurati/osservati) con più posti, quota posti misurati, `giorni_feriali_validi`, profili 24 ore di 4-5 parcheggi grandi e misurati (Stura, Porta Susa FS, Sofia, Venchi Unica, Caio Mario) con `stato`;
- `etichette`, `fonti`, `generato`.
**Via**: `eventi`, `ufficiali`, `zona_centrale`, `classe`, `motivo`, `forza`, `punti_a_favore`, `coperto_*`, `scenario`, ogni riferimento a S1/S2/S3. Peso del file < 1,5 MB (scrivilo). Controlli: il file si carica con `json.load`; 378 luoghi; i conteggi per categoria coincidono con la Fase 1.

## FASE 3 — Mappa: tema «Parcheggi di interscambio» (rifare il tema esistente)

In `scripts/mappa_template.html` il tema `interscambio` esiste già (con opzioni, classi, eventi, cerchi per insieme): **rimpiazzalo** (stesso id, stessa voce in `THEMES`, stesso link `#tema=interscambio`). Rimuovi: opzioni `r6Vista`, `r6Insieme`, `r6Raggio` (da `OPZIONI`, `OPT_VAL`, `HANDLERS`), `r6Coperto`, il disegno di zona centrale/eventi/classi e i testi relativi. Il tema **non ha opzioni** (`opzioni:[]`).
`scripts/04_genera_mappa.py` carica il nuovo `mappa_r6.json` (stessa chiave `r6`; adatta il messaggio a stampa: porte, luoghi, parcheggi). Proietta in `R6` (come ora): `porte[].poligoni`, `luoghi`, `parcheggi`.

**Descrizione del tema** (`desc`): «Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico. Ogni area è una zona dell'indagine IMQ.»

**Disegno** (dal basso):
1. **Porte**: poligoni riempiti per categoria — Bastano `#1a9850`, Quasi `#fee08b`, Pochi `#fc8d59`, Mancano `#d73027` (opacità `AREA_ALPHA`), bordo sottile; a zoom < 13 etichetta con il nome della porta (stile delle altre etichette; se non esiste, disegna il testo al baricentro con alone bianco, solo per le porte «Mancano» e «Pochi» se sono troppe). Le zone senza luoghi critici restano trasparenti.
2. **Luoghi critici**: cerchio piccolo (raggio 4-6 px), colore per categoria: «Nessun parcheggio vicino» rosso `#d73027`, «Pochi posti» arancione `#fc8d59`, «50 posti o più» verde `#1a9850`; bordo bianco. Visibili da zoom 11.
3. **Parcheggi**: puntino grigio `#6b7280`, raggio `2 + √posti/8` (max 10 px), solo da zoom 14; **contorno rosso spesso se `stato` = pieno** (misurato o osservato), tratteggiato se i posti sono stimati. Cerchio di **200 m** (come ora, in `disegnaR6Sopra`) attorno al luogo critico o al parcheggio selezionato.

**Tocco / passaggio del mouse** (stesso schema dell'attuale blocco «0ter»; ordine: parcheggi 10 px, luoghi 9 px, porte dentro il poligono): al passaggio `mostraTipBase(tipC(…))`, al clic `apriScheda(creaScheda({…}))`:
- **porta**: titolo = nome; valore = categoria in parole («Mancano posti: copertura 12%»); dettagli = auto in entrata al mattino [STIMATO] (con «[DATI SCARSI]» se < 30 interviste), «auto che potrebbero lasciare l'auto: N», posti nominali, posti utili, **mancano ~N auto**, luoghi critici e quanti senza parcheggio, quota posti misurati; sezione «Dove intervenire» con i 5 luoghi e i 5 parcheggi pieni; sezione «Strade d'ingresso principali» con le 3 strade e «traffico stimato N veicoli/giorno [STIMATO ±38%]»; una riga di spiegazione del metodo;
- **luogo critico**: nome, categoria, posti nominali entro 200 m, elenco dei parcheggi vicini (nome, distanza, posti, stato: «pieno di giorno [MISURATO]», «pieno [OSSERVAZIONE di Leo]», «a metà», «con posti liberi», «non misurato»), nome della porta;
- **parcheggio**: nome, posti (dichiarati o stimati [STIMATO]), tariffa, stato di riempimento con la fonte, mini-curva 24 ore (SVG, come ora) con «[DATI SCARSI: 2 giorni feriali]» se c'è.

**Legenda** (una sola, chiara): titolo «Posti per lasciare l'auto vicino a dove si entra in città»; blocco 1 «Aree (zone IMQ): posti utili rispetto alle auto che potrebbero lasciare l'auto» con i 4 colori e le soglie scritte («Bastano: almeno il 100%», «Quasi: 50-99%», «Pochi: 20-49%», «Mancano: meno del 20%») e il numero di porte per categoria; blocco 2 «Fermate importanti per chi arriva in auto (378)»: i 3 colori con conteggio; blocco 3 «Parcheggi: puntino grigio, grandezza = posti; contorno rosso = pieno di giorno; tratteggiato = posti stimati dalla superficie»; avvisi `[STIMATO]` `[MISURATO]` `[OSSERVAZIONE di Leo]` `[DATI SCARSI]`. Nessun cenno a versioni o scenari.
**Guida** (`<details id="infoDati">`): sostituisci il paragrafo del Risultato 6 con 4-5 frasi semplici: cosa sono le fermate importanti, come si contano i posti (tutti i parcheggi, nominali, 25 m² a posto), come si stimano le auto che potrebbero lasciare l'auto (quota già misurata), cosa significano le quattro categorie, limiti.
**Errore in console**: all'apertura compare «drawImage … canvas … width or height of 0»: apri `#tema=servizio` (un altro tema) e vedi se compare uguale; se sì è preesistente, scrivilo nell'esito e non toccare; se solo nel tema nuovo, correggilo.

## FASE 4 — Scheda in `simulazione.html` (`scripts/schede_risultati.py`)

1. **Cancella** la vecchia `scheda_r6` (prima versione) e **rinomina** `scheda_r6_v2` in `scheda_r6`; aggiorna `main()` (nome file `risultato6_riepilogo_mappa.json` invariato). Rimuovi i grafici/testi su classi, eventi, scenari, insiemi e raggi. Leggi **solo** `mappa_r6.json` (`riepilogo`, `porte`).
2. Campi: `risultato:"6"`, `titolo:"Parcheggi di interscambio"`, `stato:"Aggiornato al 19/10/2026"` (nessuna «versione»), `tag:"STIMATO / MISURATO (dati scarsi)"`.
3. **Impostazione a domande e risposte**: `domanda` = «Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico?»; `numero_chiave` = auto che potrebbero lasciare l'auto che **non trovano posto** (`mancano` totale), unità «auto», testo «al giorno, sommando le zone dove i posti non bastano».
   `risposta` (4 frasi, numeri veri da `riepilogo`): (1) quante auto entrano al mattino e quante potrebbero lasciarla [STIMATO]; (2) le 3 zone dove mancano più posti (nome, mancano ~N) e quante zone su totale in categoria «Mancano»/«Pochi»; (3) quante fermate importanti su 378 non hanno nessun parcheggio entro 200 m (147) e quante hanno meno di 50 posti (59); (4) quanti posti sono già pieni di giorno [MISURATO + OSSERVAZIONE di Leo] e che le informazioni sul riempimento coprono solo X% dei posti.
4. **Grafici** (solo questi, titoli chiari e brevi, `nota` dove serve):
   1. `barre` «Dove mancano più posti (auto al giorno)» — top 10 porte per `mancano`, `tono`: rosso se «Mancano», arancione se «Pochi», giallo se «Quasi»;
   2. `pila` «Le zone con fermate importanti: bastano o no?» — numero di porte per categoria (verde/giallo/arancione/rosso);
   3. `pila` «Fermate importanti e parcheggi a 200 m» — nessun parcheggio (rosso) / pochi posti (arancione) / 50 o più (verde);
   4. `barre` «Auto in entrata al mattino e posti utili» — per le 8 porte con più `domanda`: due voci (domanda, posti utili) con `prima`=domanda, `valore`=posti utili (la barra «prima» più chiara = quante servirebbero);
   5. `profilo` «Quanto si riempiono i parcheggi più grandi (giorno feriale)» — serie da `riepilogo.profili`, `nota`: «[MISURATO] media di 2 giorni feriali: dati ancora pochi»;
   6. `barre` «Parcheggi già pieni di giorno» — i 10 con più posti (misurati o osservati), voce con la fonte tra parentesi.
5. `immagini`: `[{"file":"immagini/r6_torino.png","didascalia":"Le zone: verde = posti sufficienti, rosso = mancano posti"},{"file":"immagini/r6_zoom.png","didascalia":"Zoom su una zona: fermate importanti e parcheggi con il cerchio di 200 m"}]` (gli screenshot li fa Leo; i file mancanti sono già gestiti: la sezione non appare).
6. `metodo` (5 frasi semplici, senza gergo): 1) fermate importanti = 10% più alto per importanza della strada, corse nelle ore dei pendolari, pendolari della zona, ZTL, calo di velocità, nodo treno/metro; 2) posti = tutti i parcheggi aperti entro 200 m (OpenStreetMap, Comune, 5T), posti dichiarati o stimati (25 m² a posto); 3) riempimento: misurato dove il 5T lo trasmette, osservazioni a mano dove si sa; 4) auto che potrebbero lasciare l'auto = auto in entrata al mattino (IMQ 2022) × 26% (quota di chi già oggi cambia con un mezzo pubblico); 5) categoria della zona = posti utili ÷ auto che potrebbero lasciare l'auto.
   `parametri`: soglia 10%, universo 4.425 luoghi (Città metropolitana), distanza 200 m, 25 m² a posto, quota 26%, giorni feriali di riempimento (date), zone esaminate (numero porte).
   `limiti`: dati di riempimento di soli 2 giorni feriali [DATI SCARSI] (da rifare con più giorni); posti stimati ±30% per i parcheggi senza dato; la domanda è per zona (indagine campionaria) e non sa delle auto che arrivano da più lontano; i quartieri di Torino contano chi ci arriva, i comuni chi parte; una nota a mano (Fermi) vale al posto di una misura che manca; distanze in linea d'aria; strade d'ingresso con traffico stimato (±38%).
   `mappa`: `{"id":"interscambio","tema":"Parcheggi di interscambio","nota":"Zone, fermate importanti e parcheggi su mappa."}`; `fonti`: `docs/RAPPORTO_R6_PORTE.txt`, `scripts/80_porte_interscambio.py`; `avviso`: tag dei dati. `scenari`: un solo blocco «Oggi» con 5-6 numeri (fermate importanti, senza parcheggio, auto in entrata, auto che potrebbero lasciare l'auto, posti utili, mancano), `prima:None`.
7. Rilancia `python scripts\schede_risultati.py`; `node --check data\schede_risultati.js`; controlla che il file contenga «Parcheggi di interscambio» e **non** contenga «versione 2», «S2», «scenario», «Allianz», «solo sulla carta», «potenziale».

## FASE 5 — Pulizia e rigenerazione

1. Rigenera la mappa; peso di `mappa_torino.html` prima/dopo nell'esito. Cerca in `mappa_template.html`, `schede_risultati.py` e nei dati i resti di: `eventi`, `ufficiali`, `zona_centrale`, `r6Insieme`, `r6Raggio`, `r6Vista`, «solo sulla carta», «scenario» riferito al R6: devono sparire (salvo commenti di storia che non finiscono in pagina).
2. Cancella dal repo solo i file generati inutili che hai creato in questo piano (nessuno dei dati dei giri precedenti). Non cancellare `data/processed/risultato6_v2/giro1/` né i rapporti `RAPPORTO_R6V2_*`.
3. Nell'esito: tabella delle porte (nome, categoria, mancano), controllo Fermi (con e senza osservazione), numeri della scheda, anomalie, file modificati, limiti aperti.

## Cosa NON fare
- Non cambiare i 378 luoghi critici, la soglia, i segnali, i dati di riempimento o i parametri (200 m, 25 m², quota calcolata, soglie delle categorie).
- Non scrivere dati a mano nel template o nella scheda: tutto da `mappa_r6.json`. Non pubblicare niente. Non fare commit. Nessuna libreria esterna.
- Non mostrare in pagina nulla di versioni precedenti, scenari, eventi, classi dei parcheggi.
