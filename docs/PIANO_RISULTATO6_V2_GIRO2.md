# Piano per un agente — Risultato 6 v2, GIRO 2 (correzioni, nuovo giro, scheda)

Scritto da Claude il 19/10/2026 per un altro modello (agente), dopo la discussione con Leo.
Le decisioni di Leo sono **fisse**. Fai **un passo alla volta, nell'ordine**. Ogni passo finisce con una riga nel
file di esito: `PASSO Gn: OK` oppure `PASSO Gn: FERMO – motivo`. Se un controllo non torna: **fermati**, scrivi
cosa hai visto, non inventare correzioni. Contesto: `docs/PIANO_RISULTATO6.md` (sezioni "Versione 2" e "Giro
dell'agente del 19/10"), `docs/PIANO_RISULTATO6_V2.md` (piano del primo giro: le sue regole 0.1-0.12 valgono
ancora, salvo le eccezioni qui sotto), `docs/ESITO_RISULTATO6_V2.md` (esito del primo giro).

---

## 0. Regole

1. Valgono le regole 1-12 di `PIANO_RISULTATO6_V2.md` (ramo `prova`, nessun commit, Python del PATH, database
   e `data/raw/` in sola lettura, ora UTC→italiana con la regola dell'ora legale, distanze haversine, mai per
   nome, tag dei dati, italiano semplice).
2. **Eccezione sui file**: questo giro **modifica sul posto** gli script del Risultato 6 v2:
   `scripts/71_parcheggi_riempimento.py`, `72_nodi_tp.py`, `73_segnali_criticita.py`, `75_risultato6_v2.py`,
   `76_verifiche_r6v2.py`. Nuovo script: **`scripts/77_strade_comuni.py`** (modulo condiviso). Gli script 68, 69, 74
   non si toccano. **Nessun altro file esistente** va modificato, **tranne** (solo al Passo G9, se autorizzato)
   `scripts/schede_risultati.py` e i file che lo script rigenera. Mai toccare: `MEMORIA_PROGETTO.md`,
   `mappa_torino.html`, `scripts/04_genera_mappa.py`, `scripts/mappa_template.html`, `scripts/24…`, `25…`,
   `data/processed/risultato6_interscambio.json`, `data/processed/traffico_d/*`.
3. Esito: `docs/ESITO_RISULTATO6_V2_GIRO2.md` (crealo a G0, aggiornalo a ogni passo). Rapporti nuovi o rigenerati in
   `docs/`, dati in `data/processed/risultato6_v2/`.
4. Prima di ogni script lungo: `--prova` (se lo script ce l'ha), poi completo. Scrivi nell'esito i tempi.
5. In ogni script modificato aggiorna la docstring in cima (cosa è cambiato nel giro 2, in italiano semplice).
6. Tutto ciò che qui è "default dichiarato" è una **scelta provvisoria**: rendila un'opzione da riga di comando o
   una costante in cima allo script, e scrivila nel rapporto.

## 1. Decisioni di Leo (19/10/2026, fisse)

1. **Strade (a2, asse d'ingresso)**: correggere la scelta del tratto (non più "il più vicino" ma "il più
   importante entro poca distanza, escluse le stradine") **e** correggere il punteggio delle tratte della Fase 5
   (primarie/secondarie non possono avere 1).
2. **Parcheggi "di fatto"**: primo filtro = il parcheggio deve stare **fuori dalla zona centrale**. La vicinanza
   a un nodo (metro/treno/capolinea/frequente) **non è più un via libera/stop**: è **un punto a favore**
   dell'importanza del nodo. Lo stesso vale per "su un asse d'ingresso".
3. **Universo delle fermate**: solo Città metropolitana di Torino (Torino + cintura + resto della Città
   metropolitana). Le fermate del resto del Piemonte escono dai percentili.
4. **b1 si sostituisce con b2** (corse nelle ore dei pendolari, feriale 6-10 e 16-20) negli scenari nuovi. La v1
   resta riproducibile (S1) solo come riferimento.
5. **Soglie delle firme del riempimento**: si fissano ora con i dati che ci sono (sono pochi: dichiararlo) e si
   **rifà il giro** quando ci saranno più giorni feriali.
6. Poi si sceglie lo scenario (lo sceglie Leo) e si prepara la scheda in `simulazione.html`.

**Default dichiarati (cambiabili da riga di comando):**
- "Zona centrale" per i **parcheggi** = zone IMQ **Q001-Q009** (Centro, San Salvario, Crocetta, San Paolo,
  Cenisia, San Donato, Aurora, Vanchiglia, Nizza Millefonti): opzione `--zone-centrali Q001,…,Q009`. Motivo: il
  primo giro ha messo "interscambio di fatto" ospedali e tribunale (Molinette, CTO, Palagiustizia, Nizza…) che
  stanno tutti in Q003-Q009. Per le **fermate critiche** il centro resta solo **Q001** (decisione del 14/10).
- Raggio di ricerca della strada: **50 m** (stretto), **150 m** (largo).
- Raggio nodo forte per i punti a favore: **400 m**.

---

## 2. Passi

### PASSO G0 — Controlli e copia del giro 1

1. Ramo `prova` (altrimenti FERMO). Crea `docs/ESITO_RISULTATO6_V2_GIRO2.md` (titolo, data, ora).
2. **Copia di sicurezza del giro 1** (serve per il confronto): copia i file di `data/processed/risultato6_v2/*.json`
   in `data/processed/risultato6_v2/giro1/` (crea la cartella; **non** sovrascrivere se esiste già) e i rapporti
   `docs/RAPPORTO_R6V2_*.txt`, `docs/RAPPORTO_RISULTATO6_V2.txt` in `docs/archivio/r6v2_giro1/` (crea la cartella).
3. Database (sola lettura): scrivi nell'esito la data più recente di `occupazione_pk.generato_utc` e quanti
   **giorni feriali validi** (≥230 letture) ci sono per ogni parcheggio 5T con dati. Se i feriali validi sono
   meno di 2: FERMO. Se sono pochi (2-4): continua, è [DATI SCARSI].
4. Controlla che esistano tutti i file elencati al Passo 0.2 di `PIANO_RISULTATO6_V2.md` e i file del giro 1.
   Se ne manca uno: FERMO.
5. `python scripts\68_luoghi_fermate.py` NON va rilanciato: controlla solo che `luoghi.json` abbia 5.087 luoghi.

### PASSO G1 — Modulo condiviso delle strade (`scripts/77_strade_comuni.py`)

Scopo: un solo modo, usato da 72 e 73, di trovare "la strada di un punto" e di correggere i punteggi.
Si importa con `importlib` (i nomi dei file iniziano con un numero). Niente `if __name__` pesante: una funzione di
prova che stampa i controlli sotto.

1. **Carica** (come fa già `73_segnali_criticita.py`, funzione `carica_strade`): `traffico_d/rete/rete_auto.npz`
   (`edge_pts`, `edge_off`), `traffico_d/assi_tratte.npz` (`edge_tratta`), `traffico_d/tratte_traffico.json`
   (`tratte[]`: `id, asse, comune, nome, classe, punteggio, motivi, veic_giorno, lunghezza_m`).
   Attenzione: `comune` può essere `None`.
2. **Punteggio corretto della tratta** (`punteggio_corr`), applicato a tutte le 47.807 tratte:
   - `primary` → almeno **4**; `secondary` → almeno **3**; `motorway`/`trunk` → 5 (già così);
   - `residential`, `service`, `living_street` → al massimo **2**, **ma solo se `motivi` è vuoto** (se `motivi`
     non è vuoto, cioè c'è un elenco a mano o un sensore 5T, il punteggio resta com'è);
   - tutte le altre classi (`tertiary`, `unclassified`, i `*_link`) invariate.
   Salva anche `punteggio_orig`. Scrivi il rapporto `docs/RAPPORTO_R6V2_STRADE.txt` con: quante tratte e quanti km
   cambiano, tabella classe × punteggio prima/dopo, i 20 tratti più lunghi ridotti (con `motivi`) e i 20 più
   lunghi alzati (nome, comune, classe, prima→dopo, `veic_giorno`).
3. **Classi "minori"** (escluse dalla scelta, salvo ultima spiaggia): `service`, `residential`, `living_street`.
4. **Asse d'ingresso**: come nel giro 1 (asse con tratte di comune "Torino" **e** di un altro comune; ignora
   `comune` = None). Riporta quanti assi (atteso circa 91) e **i 30 più lunghi** con nome e comuni toccati.
5. **Funzione `trova_strada(lat, lon)`** → dizionario `{tratta, asse, nome, comune, classe, punteggio_corr,
   asse_ingresso, distanza_m, esito}`; regola, nell'ordine:
   1. candidati = tratti (non tratte) entro **50 m** con classe **non minore**: scegli quello con
      `punteggio_corr` più alto; a parità il più vicino. `esito = "ok"`;
   2. altrimenti il tratto non minore **più vicino** entro **150 m**: `esito = "strada_lontana"`;
   3. altrimenti il tratto minore più vicino entro **50 m**: `esito = "solo_minore"`;
   4. altrimenti `None` (`esito = "nessuna"`).
   Un tratto con `edge_tratta` = −1 si ignora.
6. **Controlli (scrivili nel rapporto; se uno non torna: FERMO):**
   - dopo la correzione tutte le tratte `primary` hanno `punteggio_corr` ≥ 4 e tutte le `secondary` ≥ 3. Conta
     le eccezioni: deve essere 0;
   - le tratte di "Via Torino" a **Venaria Reale** (cerca `nome` o `nomi` che contengono "torino" con comune
     "Venaria Reale"): scrivi classe e punteggio prima/dopo (atteso: secondary → almeno 3);
   - la fermata **GENOVA N.212** (Moncalieri): cerca nei luoghi un nome che contenga "GENOVA N.212"; `trova_strada`
     deve restituire una strada **non minore** (atteso "Strada Genova", punteggio_corr ≥ 4), non un tratto di
     servizio; scrivi il risultato;
   - i parcheggi **Fermi** (45,0766; 7,5903) e **Venchi Unica**: scrivi la strada trovata e `asse_ingresso`
     (atteso: Corso Francia; se `asse_ingresso` resta falso, non è un motivo di stop: scrivilo, con i comuni
     dell'asse trovato).
7. Rapporto: conteggio degli `esito` sui 5.087 luoghi (ok / strada_lontana / solo_minore / nessuna).

### PASSO G2 — Segnali (`73_segnali_criticita.py`)

1. **a2** e `asse_ingresso`: sostituisci `strada_piu_vicina` con `trova_strada` del modulo 77.
   `a2 = min(5, punteggio_corr + (1 se asse_ingresso))`. Salva anche `a2_esito`, `a2_strada` (nome),
   `a2_distanza_m`. Se `esito = "solo_minore"` il valore è usato ma segnato `a2_incerto = true`.
2. **d**: escludi dai sensori usati quelli con calo < 0 oppure > 0,9, o con `v_notte` < 20 km/h (sono valori
   anomali, es. SS31 Del Monferrato calo −1,89). Elencali nel rapporto come "sensori scartati" con il motivo.
   Il resto di `d` non cambia.
3. **b1** resta calcolato (serve per la v1/S1 e per la sensibilità), ma non entra più negli scenari nuovi.
4. Tutto il resto (a1, b2, c1, c2, c3, c2_ztl, e, f) **invariato**. Rilancia con `--prova`, poi completo.
5. **Controlli:**
   - c2 = 95.297 spostamenti (±2%), 1.139 interviste; f = 24.459 e 299 interviste (uguali al giro 1);
   - luoghi con `a2`: deve salire da 3.261 (nel giro 1 mancava in 1.826 luoghi: scrivi il nuovo numero e, dei
     luoghi che ora hanno `a2`, quanti per `esito`);
   - nel rapporto: confronto con il giro 1 (`giro1/segnali.json`): quanti luoghi cambiano `a2`, di quanto
     (distribuzione della differenza: −4…+4), e i 20 cambiamenti più grandi con nome e zona;
   - **GENOVA N.212**: `a2` ≥ 4 (come sopra).

### PASSO G3 — Funzione dei parcheggi (`72_nodi_tp.py`, seconda parte)

Cambia **solo** la parte "Passo 5" (classi dei parcheggi) e il calcolo di `su_asse_ingresso` (usa `trova_strada`
del modulo 77, raggio stretto/largo come sopra; salva `strada` e `asse_ingresso_nome`). Corse, nodi, stazioni
(Passo 4) **non cambiano**: `nodi.json` deve avere gli stessi 346 nodi forti (controllo).

1. Per ogni parcheggio non `privato`/`clienti`/`lungo_strada` (3.431):
   - `zona_centrale` = zona IMQ in {Q001…Q009} (opzione `--zone-centrali`);
   - **punti a favore** (somma, 0-3), mai bloccanti:
     - +1 `nodo_vicino`: nodo forte entro 400 m (`dist_nodo_forte_m` ≤ 400);
     - +1 `nodo_ferro_metro`: nodo di tipo metro/ferro/capolinea entro 400 m (non solo "frequente");
     - +1 `su_asse_ingresso`;
     - `forza` = somma dei punti. Salva anche l'elenco leggibile dei punti ("nodo: metro Fermi 120 m", ecc.).
2. **Classe** (prima regola che vale):
   1. `zona_centrale` → `non_interscambio` con `motivo = "zona_centrale"`;
   2. tipo `interscambio_ufficiale` o `park_ride_osm` e firma in {residenziale, destinazione, vuoto,
      dato_bloccato, misto} → `solo_sulla_carta` (con la firma accanto);
   3. firma `pendolare` → `interscambio_di_fatto` (con `forza`: se `forza` = 0 scrivilo come "di fatto, senza nodo
      né asse vicino");
   4. firma sconosciuta/`nessun_dato`/`dati_insufficienti` e `forza` ≥ 1 → `potenziale`;
   5. altrimenti → `non_interscambio` (`motivo = "nessun_punto"` o `"firma_non_pendolare"`).
3. Rapporto `docs/RAPPORTO_R6V2_FUNZIONE.txt`: conteggi e posti per classe **e per motivo**; tabella dei 5
   ufficiali e dei garage 5T (zona, centrale sì/no, firma, forza, tariffa, classe); i 20 `potenziale` con più
   posti; **tabella di sensibilità** della zona centrale: ripeti i conteggi con zone centrali = {Q001},
   {Q001-Q005}, {Q001-Q009} (default), {Q001-Q012}.
4. **Controlli (non sono motivo di stop, ma scrivili uno per uno):** Molinette, CTO, Palagiustizia, Nizza,
   Stati Uniti, Ancona, Bacigalupo, Fontanesi, Ventimiglia (tutti in Q003-Q009) devono risultare
   `non_interscambio / zona_centrale`; Fermi `potenziale` con `forza` ≥ 2; i grandi parcheggi gratuiti OSM vicino
   a Fermi `potenziale`; Stura, Caio Mario, Sofia, Venchi Unica `solo_sulla_carta`. Scrivi quanti `interscambio_di_fatto`
   restano (può essere **zero o pochissimi**: è un risultato, non un errore; non allargare le regole per
   riempirlo).

### PASSO G4 — Soglie delle firme del riempimento (`71_parcheggi_riempimento.py`)

I dati restano pochi (vedi G0.3): le soglie si fissano ora e si rifà il giro quando i giorni feriali saranno ≥ 5.

1. Costanti in cima allo script (e opzioni da riga di comando). **Default dichiarati:**
   - `dato_bloccato`: ampiezza < **0,06** (era 0,05: Venchi Unica fermo al 51% ha 0,055 e deve risultare bloccato);
   - `pendolare`: G − N ≥ **0,20** e (W assente o G − W ≥ **0,10**) — invariato;
   - `residenziale`: N − G ≥ **0,10** — invariato;
   - `destinazione`: G − N ≥ 0,20 e W presente e G − W < 0,10 — invariato;
   - `pieno`: G ≥ 0,85; `vuoto`: G < 0,15 — invariato.
2. Nel rapporto, oltre alla tabella del primo giro, **tabella di sensibilità**: per ogni parcheggio con dati, la
   firma ottenuta con una griglia di soglie (bloccato 0,04 / 0,06 / 0,08 × pendolare G−N 0,15 / 0,20 / 0,25), e
   l'elenco dei parcheggi la cui firma **cambia** al variare delle soglie (sono quelli "fragili").
3. In testa al rapporto: "ANTEPRIMA [DATI SCARSI]: N giorni feriali validi (date), N weekend".
4. Controlli: Fermi, Racconigi, Unione Sovietica, V Padiglione = `nessun_dato`; Sofia `residenziale`;
   Venchi Unica `dato_bloccato`; Caio Mario `dato_bloccato`+`vuoto`; Porta Susa FS con ciclo giorno/notte chiaro
   (notte 36%, giorno ~78-88%). Se Porta Susa FS non ha un ciclo chiaro: FERMO (ore sbagliate).

### PASSO G5 — Scenari e universo (`75_risultato6_v2.py`)

1. **Universo**: costruisci la mappa zona IMQ → macro-area da `data/processed/imq_zone.json` (campo `macro`).
   Un luogo è **nell'universo** se la sua zona ha macro `01 Torino`, `02 Cintura` o `03 Resto CMTO`. I luoghi
   senza zona IMQ (23 nel giro 1) e quelli di altre macro-aree restano fuori da percentili e soglie. Opzione
   `--universo cmto` (default) / `--universo tutto` (per confrontare). Scrivi nel rapporto: luoghi nell'universo
   (atteso **4.425**), fuori per macro-area, e i 23 senza zona con nome e coordinate (decide Leo che farne).
2. I percentili e la soglia del 90° si calcolano **solo sui luoghi dell'universo**. Critico = punteggio ≥ soglia,
   non in Q001 (per i luoghi/fermate il centro resta Q001), nell'universo.
3. **Controllo di riproducibilità della v1** (obbligatorio, **per fermata**, con l'universo di sempre = tutte le
   7.045 fermate): 611 critiche, 17 coperte, 594 scoperte. Se no: FERMO. Questo controllo **non** usa l'universo
   nuovo, serve solo a provare che il codice base non si è rotto.
4. **Scenari** (massimo 3, stesso formato del giro 1):
   - **S1 "riferimento v1, per luoghi"**: a1, b1, c1 (il vecchio, solo per confronto);
   - **S2 "integrato"**: a1, a2, **b2**, c1, c2_ztl, d, e (b1 tolto, b2 al suo posto);
   - **S3 "solo nuovi"**: a2, b2, c2_ztl, d, e.
   `c2_ztl` usa `c2_completo` (ISTAT 2011) dove le interviste sono poche, come nel giro 1.
5. **Copertura** come nel giro 1: insiemi **U** (5 ufficiali), **F** (`interscambio_di_fatto` + `potenziale`),
   **P** (parcheggi aperti ≥ 50 posti), raggi 100/200/400 m. In più un insieme **F+S** = F più i parcheggi
   `solo_sulla_carta` (per vedere quanto cambia se si contano anche quelli ufficiali poco usati).
6. **Confronti**: luoghi critici per scenario; S1∩S2, S1∩S3, S2∩S3; i 15 che entrano e i 15 che escono (S1→S2,
   S1→S3) con nome, zona, segnali; **confronto con il giro 1** (`giro1/scenari.json`): per ogni scenario quanti
   luoghi critici restano, entrano, escono, e i 15 più cambiati.
7. **Sensibilità** (su S2): togliere un segnale alla volta (a1, a2, b2, c1, c2_ztl, d, e); c2 al posto di c2_ztl;
   b_giorno al posto di b2; **b1 al posto di b2** (per mostrare l'effetto della sostituzione); universo `tutto`
   al posto di `cmto`. Per ognuno: quanti luoghi critici cambiano.
8. **I più scoperti**: per ogni scenario i 25 luoghi critici più gravi senza copertura U né F a 400 m (nome, zona,
   punteggio, segnali, parcheggio più vicino e distanza).
9. **Per zona**: per ogni scenario, quanti luoghi critici per quartiere/zona IMQ e quanti coperti (F, 200 m): serve
   al grafico della scheda. Salva in `scenari.json` sotto `per_zona`.
10. Scrivi `data/processed/risultato6_v2/scenari.json` (struttura del giro 1 + `universo`, `confronto_giro1`,
    `piu_scoperti`, `per_zona`) e `docs/RAPPORTO_RISULTATO6_V2.txt` (in testa tabella breve: scenario → luoghi
    critici → coperti U/F/P/F+S a 200 m; poi confronti, sensibilità, limiti).
11. **Non scrivere che uno scenario è "migliore"**: li presenti, decide Leo.

### PASSO G6 — Rilancio in ordine

Ordine obbligato (ogni passo dopo il precedente): G1 → 71 (G4) → 72 (G3, usa 77 e il riempimento) → 73 (G2) → 74
(non va rilanciato: usa i file esistenti, controlla solo che `istat2011_proporzioni.json` ci sia) → 75 (G5) → 76 (G7).
Prima con `--prova` dove c'è, poi completo. Scrivi nell'esito il tempo di ognuno.

### PASSO G7 — Verifiche indipendenti (`76_verifiche_r6v2.py`)

Tieni i controlli del giro 1 (luoghi, b2/c2 di 5 luoghi a caso seme 20261018, firma di Porta Susa FS e Venchi Unica,
superficie di 3 parcheggi OSM, copertura U = 17 per fermata) e **aggiungi**:
1. **a2 rifatto a mano** per 8 luoghi (seme 20261019): ricostruisci i tratti entro 50 m con una via diversa
   (per es. `cKDTree` sui punti + distanza punto-segmento con shapely in EPSG:32632), applica la regola G1.5 e
   confronta nome strada e `a2` con `segnali.json`: devono essere uguali.
2. **Universo**: conteggio dei luoghi nell'universo rifatto con un metodo diverso (per es. dalle zone con pandas)
   = quello di G5.
3. **Parcheggi**: per 5 parcheggi (3 5T + 2 OSM, seme 20261019) rifai a mano `zona_centrale`, `forza` e classe →
   uguali a `parcheggi_funzione.json`.
4. **Soglia del 90°** di S2 rifatta con numpy sui soli luoghi dell'universo → uguale (±0,01).
5. `git status`: nessun commit; elenca i file **modificati** (devono essere solo quelli del punto 0.2) e i **nuovi**.

### PASSO G8 — Esito (`docs/ESITO_RISULTATO6_V2_GIRO2.md`)

1. Righe di stato `PASSO G0…G7: OK/FERMO`.
2. Le decisioni che hai preso tu dove il piano lasciava una scelta, e perché.
3. **Numeri chiave** (tabella): luoghi nell'universo; tratte corrette (n, km); luoghi con `a2` (prima/dopo); parcheggi
   per classe e posti (prima/dopo); firme; per scenario luoghi critici e coperti U/F/P/F+S a 100/200/400 m;
   confronto con il giro 1; sensibilità; i 25 più scoperti di ogni scenario.
4. **Risposte ai 4 problemi**, uno per uno: (1) a2 e asse d'ingresso — GENOVA N.212, Via Torino a Venaria, Fermi e
   Venchi Unica su un asse d'ingresso sì/no, quanti parcheggi su un asse; (2) "di fatto" — quanti restano e
   quali; (3) universo; (4) b1 → b2.
5. Anomalie, differenze dagli attesi, limiti (sezione 4), file creati, durate.
6. **Una tabella per Leo** per scegliere lo scenario: per S1/S2/S3 una riga con "cosa misura", luoghi critici, quanti
   coperti, due esempi di luoghi che entrano e due che escono. Nessuna raccomandazione.
7. **Fermati qui.** Non fare G9 se non c'è la riga `SCENARIO SCELTO` nel punto G9.0.

### PASSO G9 — Scheda in `simulazione.html` (SOLO dopo la scelta di Leo)

0. **SCENARIO SCELTO: S2** (Leo, 19/10/2026). G9 va però eseguito dentro `PIANO_RISULTATO6_FINALE.md` (Fase D), dopo mappa ed eventi.
1. Obiettivo: sostituire la scheda del Risultato 6 (versione 1) con la **versione 2**, nello stesso formato delle
   altre schede (vedi la docstring di `scripts/schede_risultati.py`: due livelli, grafici + link mappa, solo
   risultati finiti). In `schede_risultati.py` aggiungi `scheda_r6_v2()` e usala al posto di `scheda_r6` nella lista
   di `main()`; **lascia `scheda_r6` nel file** (non cancellarla). Scrive ancora `risultato6_riepilogo_mappa.json`.
   Nessun calcolo nuovo sui dati grezzi: solo numeri già in `scenari.json`, `parcheggi_funzione.json`,
   `riempimento.json`, con somme e conteggi semplici.
2. Contenuto (italiano semplice, numeri con la virgola e il punto delle migliaia come nelle altre schede):
   - `titolo` "Parcheggi di interscambio", `stato` "Versione 2 (data)", tag `STIMATO / PROGRAMMATO / MISURATO (dati scarsi)`;
   - `numero_chiave`: luoghi critici (scenario scelto) senza un parcheggio (F, 200 m) su quanti;
   - `risposta` (3-4 frasi): quanti luoghi critici, quanti coperti dai parcheggi di fatto/potenziali, quanti dagli
     ufficiali; quanti parcheggi fanno davvero da interscambio (di fatto, solo sulla carta, potenziale) con i posti;
     i quartieri/zone con più luoghi critici scoperti;
   - `grafici`: (a) pila luoghi critici coperti/scoperti; (b) barre classi dei parcheggi con i posti
     (di fatto / solo sulla carta / potenziale / non interscambio); (c) barre delle firme del riempimento; (d) barre
     dei quartieri con più luoghi critici scoperti (`per_zona`); (e) se i dati bastano, `tipo: "orario"` con il
     profilo feriale di 3-4 parcheggi significativi (Stura, Sofia, Porta Susa FS, Venchi Unica) — guarda come lo
     usa `scheda_r4` per il formato;
   - `metodo`: luoghi (fermate entro 40 m = un luogo), i segnali dello scenario scelto in parole semplici, la firma
     del riempimento, i punti a favore del nodo;
   - `parametri`: universo, soglia 90°, raggi, zone centrali dei parcheggi, giorni feriali di riempimento;
   - `limiti`: dal paragrafo 4 di questo piano, **sempre** con "[DATI SCARSI] pochi giorni di riempimento" e la data
     di aggiornamento prevista; `mappa`: `None`; `fonti`: i rapporti e gli script.
   - `avviso` standard del progetto con l'indicazione del tag dei dati.
3. Rilancia `python scripts\schede_risultati.py`. Controlli: lo script stampa la riga di R6 con numeri e grafici;
   `node --check data\schede_risultati.js`; il file contiene "Parcheggi di interscambio" e il numero chiave atteso.
   Se c'è `.claude/launch.json` → `pagine-gtt` (porta 8765), apri `simulazione.html`, apri la scheda R6 e controlla
   che i grafici si vedano (legge la pagina con `read_page`); se non puoi aprire il browser, scrivi nell'esito
   esattamente quale file Leo deve aprire e cosa deve vedere.
4. Non toccare `mappa_torino.html` né la memoria: lo fa Claude con Leo.

---

## 3. Cosa NON fare

- Non scegliere lo scenario e non dire che uno è migliore.
- Non allargare le regole per far uscire più "interscambi di fatto": se sono pochi o zero, scrivilo.
- Non toccare `MEMORIA_PROGETTO.md`, la mappa, gli script 24/25, né i dati in `data/raw`, `traffico_d`, né il database.
- Non usare numeri assoluti ISTAT 2011. Non abbinare per nome (eccezione: 5T↔Comune, nome **e** distanza < 150 m).
- Non scaricare niente da internet; non installare librerie; non fare commit.

## 4. Limiti da scrivere nei rapporti

- Riempimento: pochi giorni feriali [DATI SCARSI]; 4 parcheggi non trasmettono; soglie provvisorie; da rifare con ≥ 5 feriali.
- Parcheggi OSM: elenco incompleto; posti stimati dalla superficie (~25 m² a posto) [STIMATO]; tariffa spesso ignota;
  nessun riempimento per i parcheggi gratuiti (es. attorno a Fermi).
- "Zona centrale" dei parcheggi = Q001-Q009 è una scelta provvisoria; lo dice la tabella di sensibilità.
- Pendolari IMQ: indagine campionaria, residenti 11-84 anni; la zona IMQ dà lo stesso valore a tutti i luoghi della
  zona; zone con poche interviste completate con proporzioni ISTAT 2011.
- Importanza della strada (a2): punteggi della Fase 5 corretti per classe (primarie ≥ 4, secondarie ≥ 3) — la stima
  del traffico della Fase 5 è debole (±38%) e qui conta solo come ordine.
- Calo di velocità (d): solo vicino a un sensore 5T (pochi luoghi).
- Distanze in linea d'aria, non a piedi. Corse da orario programmato [PROGRAMMATO].
- Universo: solo Città metropolitana di Torino; le fermate del resto del Piemonte non sono valutate.
- Treni: le stazioni vengono da OSM; le frequenze dei treni non sono nei dati (il GTFS GTT non ha i treni).
