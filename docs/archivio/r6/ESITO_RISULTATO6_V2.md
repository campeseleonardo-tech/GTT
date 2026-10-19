# Esito — Risultato 6, versione 2 (parcheggi di interscambio)

Piano di riferimento: `docs/PIANO_RISULTATO6_V2.md`.
Ramo git: **`prova`**. Nessun commit (decide Leo).
Inizio lavori: 18/10/2026 ore 23:51. Fine: 19/10/2026 ore 00:05.

## Passi

| Passo | Stato |
|---|---|
| 0 — Controlli iniziali | **OK** |
| 1 — Luoghi di fermata | **OK** |
| 2 — Inventario parcheggi | **OK** |
| 3 — Riempimento (anteprima) | **OK** (con 2 scostamenti, sotto) |
| 4 — Nodi di trasporto | **OK** |
| 5 — Funzione dei parcheggi | **OK** |
| 6 — Segnali di criticità | **OK** |
| 7 — ISTAT 2011 proporzioni | **OK** |
| 8 — Tre scenari e copertura | **OK** |
| 9 — Verifiche indipendenti | **OK** |
| 10 — Esito | **OK** |

## PASSO 0 — controlli iniziali

- Ramo git verificato: `prova`.
- Cartella `data/processed/risultato6_v2/` creata.
- Tutti i 18 file di input richiesti esistono (controllati uno per uno).
- Database `data/storico_backup.sqlite` (aperto in sola lettura): ultima riga di
  `occupazione_pk` con `generato_utc` = **2026-10-18T17:47:52Z** (atteso almeno 18/10: OK).
  Righe totali: 48.544; parcheggi distinti: 41.
- Nessuna parte della versione 1 è stata rilanciata: solo letta.

## PASSO 1 — luoghi di fermata

- 7.045 fermate → **5.087 luoghi** (atteso 5.080, tolleranza ±1%: dentro).
- Luoghi con almeno una fermata critica v1: **462** (atteso 461 ±2%: dentro).
- Luoghi con almeno una fermata coperta v1: **12** (atteso 10-15: dentro).
- Fermate per luogo: 1 → 3.266, 2 → 1.725, 3 → 67, 4 o più → 29.
- "611 fermate critiche della versione 1 = **462** luoghi". Il luogo con più fermate è
  CAIO MARIO (11 fermate).
- 24 luoghi hanno il punto medio fuori da tutte le zone IMQ: usata la zona della prima
  fermata, come prevede il piano.

## PASSO 2 — inventario dei parcheggi

- 5T senza camper: **40** (atteso 40). Comune: **39** (atteso 39). OSM: **5.176**
  (atteso ~5.176), di cui **25 park&ride** e 586 con `capacity` numerica (atteso 586).
- I 5 interscambi ufficiali ci sono tutti: Stura, Caio Mario, Sofia, Venchi Unica, Fermi.
- Conversione delle coordinate del Comune (Gauss-Boaga EPSG:3003 → lat/lon): distanza dal
  punto 5T omonimo Stura 54 m, Caio Mario 21 m, Sofia 61 m, Venchi Unica 36 m (limite 300 m: OK).
- OSM abbinati a un parcheggio 5T/Comune (così non si contano due volte): 30.
- Elenco finale: **5.205 parcheggi**. Per tipo: interscambio_ufficiale 5, garage_5t 54,
  park_ride_osm 19, osm_pubblico 3.353, lungo_strada 1.048, clienti 385, privato 341.
- Controllo Fermi (45,0766; 7,5903) entro 500 m: parcheggi aperti (conteggiati nei posti)
  **75.103 m²**; aggiungendo la sosta lungo strada (3.473) e i parcheggi per clienti (6.266)
  si arriva a **84.842 m²**, cioè il valore atteso "~85.000": il numero del piano
  comprendeva anche quelle due categorie. Il sotterraneo grande c'è: **30.650 m² a 178 m**
  (atteso ~30.000 m² a ~180 m). Tariffa dei parcheggi aperti vicino a Fermi: 9 gratuiti,
  9 ignoti, 2 a pagamento.
- Scelte fatte (il piano lasciava spazio):
  - `posti_stimati` calcolato solo dove i posti si contano (`park_ride_osm`, `osm_pubblico`);
    per `lungo_strada`, `clienti`, `privato` resta vuoto, perché il piano dice che quei
    posti non si contano.
  - Se due record 5T/Comune vicini pescano lo stesso poligono OSM, il poligono va al più
    vicino: così una superficie non viene contata due volte.

## PASSO 3 — anteprima del riempimento

- **ANTEPRIMA [DATI SCARSI]**: **2 giorni feriali validi** (15 e 16/10), più sabato 17/10.
  Il 14/10 la raccolta è partita alle 15:10 e non arriva alle 230 letture minime; la
  domenica 18/10 è incompleta (la copia del database è delle 17:47 UTC). Il piano parlava
  di "3 feriali 14-16/10": sono 2 per la regola delle 230 letture.
- Firme (41 parcheggi 5T): pendolare 16, destinazione 10, misto 8, residenziale 2,
  dato_bloccato 1, nessun_dato 4.
- Controlli attesi, uno per uno:
  - Fermi, Racconigi, Unione Sovietica, V Padiglione = `nessun_dato` **OK**.
  - Sofia = `residenziale` con notte 55% e giorno 32% **OK**.
  - Porta Susa FS: notte 36%, giorno 78% → `destinazione`. Ciclo giorno/notte chiaro **OK**
    (il giorno è 78% invece di 80-88%: stesso andamento).
  - Caio Mario: occupazione 1,5% (1-2%) → firma `dato_bloccato` (perché l'ampiezza è
    0,006, sotto la soglia 0,05) **con il contrassegno `vuoto`**, come chiedeva il piano.
  - Stura: notte 79%, giorno 90% → `misto`, non `pendolare`. Il piano diceva che con
    queste soglie va bene così. **OK**
  - Venchi Unica: profilo quasi piatto (48-52%), ma l'ampiezza è **0,0552**, appena sopra
    la soglia 0,05 → risulta `misto` e non `dato_bloccato`. Con soglia 0,06 sarebbe
    `dato_bloccato`. Soglie provvisorie: decide Leo.

## PASSO 4 — nodi di trasporto

- **346 nodi forti** su 5.087 luoghi: 23 con la metropolitana, 114 con una stazione dei
  treni entro 300 m, 69 capolinea, 140 solo perché hanno almeno 20 corse/ora.
- Stazioni dei treni trovate in OSM: **36**. Ci sono tutte quelle attese (Porta Nuova,
  Porta Susa, Lingotto, Stura, Rebaudengo).
- Metropolitana: **23 luoghi**, esattamente le 23 stazioni da Fermi a Bengasi.
- 91 assi di ingresso (assi con tratte sia a Torino sia in un altro comune) su 31.639 assi.
- 13.683 corse attive il 12/10/2026 (126 servizi).

## PASSO 5 — quanto ogni parcheggio fa da interscambio

- Parcheggi considerati (esclusi privati, clienti e sosta lunga): **3.431**.
- Classi: **interscambio_di_fatto 9** (3.264 posti), **solo_sulla_carta 4** (1.716),
  **potenziale 725** (53.131), **non_interscambio 2.693** (159.768).
- Controlli attesi: Venchi Unica e Sofia `solo_sulla_carta` **OK**; Fermi `potenziale` **OK**;
  i grandi parcheggi gratuiti OSM vicino a Fermi `potenziale` **OK** (es. 1.226 posti a
  174 m dal metro, 773 posti, 651 posti).
- In più risultano `solo_sulla_carta` anche Caio Mario (firma dato_bloccato + vuoto) e
  Stura (firma misto): è quello che dicono le regole del piano.
- Su un asse di ingresso: 42 parcheggi; 8 non hanno nessuna strada entro 150 m.

## PASSO 6 — segnali di criticità

- Luoghi con un valore per segnale: a1 5.087 · a2 **3.261** (manca in 1.826) · b1 5.087 ·
  b2 5.087 · c1 5.058 · c2 4.464 · c2_ztl 4.464 · d **96** (manca in 4.991) · e 5.087
  (metro o treno in **137** luoghi).
- c2 (auto in entrata al mattino, IMQ 2022): **95.297 spostamenti, 1.139 interviste**
  (atteso ~95.300 e 1.139: OK).
- c3 (ZTL centrale, arrivo 07:30-10:30): 16.722 spostamenti, 203 interviste. L'unica zona
  IMQ con almeno il 10% della superficie dentro la ZTL centrale è **Q001 (68,3%)**.
- 2.943 luoghi stanno in zone con meno di 30 interviste (c2 "scarso").
- d: 97 sensori 5T usabili (su 109); calo massimo 0,65 (Corso Trieste), mediana 0,21.
  Un sensore (SS31 Del Monferrato) ha un valore anomalo (notte 15 km/h, punta 43 km/h,
  calo −1,89): lo segnalo come dato da guardare, non è stato escluso.
- f (auto che già oggi passano al mezzo pubblico, solo informazione): **24.459 spostamenti,
  299 interviste** (atteso ~24.500 e 299: OK). Per secondo mezzo: codice 12 → 13.583,
  codice 19 → 3.958 (il "~4.000 verso la metro" del piano corrisponde al codice 19),
  codice 06 → 2.281, gli altri meno. Zona del cambio non indicata nel 60% dei casi.

## PASSO 7 — ISTAT 2011 (solo proporzioni)

- 4.876.242 righe lette; 20.122 spostamenti cintura → Torino usati; 311 comuni di
  residenza; 77 zone IMQ collegate; 5 comuni senza zona IMQ.
- Controllo dei codici: per chi va a Torino **per lavoro** il mezzo più frequente è il
  codice 07 (auto come conducente, 85.720 persone) contro 9.068 del treno: **OK**.
- Zone con poche interviste completate con la quota auto 2011: **54** (tutte C… e E…,
  nessun quartiere Q…).
- La quota auto IMQ 2022 è quasi sempre più alta di quella ISTAT 2011 (fino a +30 punti
  nelle zone di cintura). Motivo probabile: l'IMQ qui guarda solo chi si sposta **al
  mattino verso Torino**, che usa l'auto più della media di tutti gli spostamenti.

## PASSO 8 — tre scenari e copertura

Controllo di riproducibilità (obbligatorio): rifacendo S1 fermata per fermata escono
**611 critiche, 17 coperte, 594 scoperte**, come la versione 1: **OK**.

| Scenario | Luoghi critici | Coperti U 200 m | Coperti F 200 m | Coperti P 200 m |
|---|---|---|---|---|
| S1 "come la v1, per luoghi" | 438 | 13 | 171 | 156 |
| S2 "integrato" | 436 | 13 | 186 | 162 |
| S3 "solo nuovi" | 438 | 14 | 193 | 172 |

- U = 5 interscambi ufficiali · F = 734 parcheggi di fatto/potenziali · P = 1.147 parcheggi
  aperti con almeno 50 posti.
- Copertura a 100 / 200 / 400 m:
  - S1: U 4 / 13 / 25 · F 78 / 171 / 290 · P 61 / 156 / 311
  - S2: U 3 / 13 / 23 · F 82 / 186 / 301 · P 61 / 162 / 327
  - S3: U 4 / 14 / 23 · F 87 / 193 / 307 · P 64 / 172 / 341
- Confronto: S1∩S2 = 370 (entrano 66, escono 68); S1∩S3 = 327 (entrano 111, escono 111);
  S2∩S3 = 392.
- Sensibilità (S2 completo = 436 critici; quanti luoghi cambiano togliendo un segnale):
  senza a2 → 148; senza c2_ztl → 120; senza b2 → 118; senza e → 90; senza d → 12;
  c2 al posto di c2_ztl → 20; b_giorno al posto di b2 → 6. Il segnale che pesa di più è
  **a2** (importanza della strada); `d` quasi non pesa perché esiste solo vicino a 97 sensori.
- 438 luoghi critici in S1, non 462: 462 sono i luoghi che **contengono** almeno una
  fermata critica della v1; qui il punteggio è calcolato sul luogo intero, quindi qualcuno
  scende sotto la soglia.

## PASSO 9 — verifiche indipendenti

Tutte superate (`docs/RAPPORTO_R6V2_VERIFICHE.txt`):

1. Numero di luoghi rifatto con cKDTree + componenti connesse: **5.087 = 5.087**.
2. b2 e c2 di 5 luoghi a caso (seme 20261018): **identici**.
3. Firma di Porta Susa FS e Venchi Unica rifatta con pandas: **identica**.
4. Superficie di 3 parcheggi OSM vicino a Fermi rifatta con shapely in EPSG:32632:
   differenza **0,51%** (limite 2%).
5. Copertura U a 200 m sulle fermate: **17**, come la v1.
6. git: **0 file esistenti modificati**, nessun commit. File nuovi: 8 script, 9 rapporti
   in `docs/`, 7 file in `data/processed/risultato6_v2/` (questi ultimi non tracciati da
   git perché `data/` non è in git).

## Anomalie e differenze dagli "attesi" del piano

1. Luoghi: 5.087 invece di 5.080 (dentro la tolleranza; il controllo indipendente
   conferma 5.087, quindi il numero del piano veniva da una misura leggermente diversa).
2. Giorni feriali validi: 2 invece di 3 (il 14/10 è incompleto).
3. Venchi Unica `misto` invece di `dato_bloccato` (ampiezza 0,0552 contro soglia 0,05).
4. Caio Mario: firma `dato_bloccato` con contrassegno `vuoto` (il piano si aspettava "vuoto").
5. Fermi: 75.103 m² di parcheggi aperti invece di ~85.000; la differenza è la sosta lungo
   strada e i parcheggi per clienti, che il piano aveva incluso.
6. Caio Mario e Stura risultano `solo_sulla_carta`: conseguenza delle regole, non previsto
   dal piano nella lista degli attesi.
7. Un sensore velocità ha un calo negativo anomalo (−1,89).

## File creati

Script (nuovi, nessuno esistente modificato):
`scripts/68_luoghi_fermate.py`, `69_parcheggi_inventario.py`, `71_parcheggi_riempimento.py`,
`72_nodi_tp.py`, `73_segnali_criticita.py`, `74_istat2011_auto_orari.py`,
`75_risultato6_v2.py`, `76_verifiche_r6v2.py`.

Dati (`data/processed/risultato6_v2/`): `luoghi.json`, `parcheggi.json`,
`riempimento.json`, `nodi.json`, `parcheggi_funzione.json`, `segnali.json`,
`istat2011_proporzioni.json`, `scenari.json`.

Rapporti (`docs/`): `RAPPORTO_R6V2_LUOGHI.txt`, `RAPPORTO_R6V2_PARCHEGGI.txt`,
`RAPPORTO_R6V2_RIEMPIMENTO.txt`, `RAPPORTO_R6V2_NODI.txt`, `RAPPORTO_R6V2_FUNZIONE.txt`,
`RAPPORTO_R6V2_SEGNALI.txt`, `RAPPORTO_R6V2_ISTAT2011.txt`, `RAPPORTO_RISULTATO6_V2.txt`,
`RAPPORTO_R6V2_VERIFICHE.txt`, e questo esito.

## Cosa resta (lo fa Claude con Leo)

1. Scegliere lo scenario (S1, S2 o S3) e fissare le soglie delle firme di riempimento.
2. Preparare la scheda del Risultato 6 v2 e aggiornare la memoria del progetto.
   (Il piano vieta di toccare memoria, schede e mappa: non sono state toccate.)
3. Nessun commit è stato fatto: decide Leo.
