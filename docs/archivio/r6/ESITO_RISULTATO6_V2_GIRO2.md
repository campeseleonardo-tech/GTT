# Esito — Risultato 6 v2, GIRO 2 (correzioni, nuovo giro, scheda)

Piano di riferimento: `docs/PIANO_RISULTATO6_V2_GIRO2.md`.
Ramo git: **`prova`**. Nessun commit (decide Leo).
Inizio lavori: 19/10/2026 ore 00:38. Fine: 19/10/2026 ore 00:55.

## Passi

| Passo | Stato | Durata |
|---|---|---|
| G0 — Controlli e copia del giro 1 | **OK** | ~3 minuti (00:38–00:41) |
| G1 — Modulo condiviso delle strade (`77`) | **OK** | ~5 s |
| G2 — Segnali (`73`) | **OK** | prova 4 s, completo 5 s |
| G3 — Funzione dei parcheggi (`72`) | **OK** | prova 24 s, completo 25 s |
| G4 — Soglie delle firme (`71`) | **OK** | ~1 s |
| G5 — Scenari e universo (`75`) | **OK** | ~2 s |
| G6 — Rilancio in ordine | **OK** | incluso sopra |
| G7 — Verifiche indipendenti (`76`) | **OK** | ~1 min 20 s |
| G8 — Esito (questo file) | **OK** | ~10 min |
| G9 — Scheda (`schede_risultati.py`) | **NON ESEGUITO** | G9.0 (`SCENARIO SCELTO`) è vuoto |

Ordine di rilancio seguito come chiede G6: 77 → 71 → 72 → 73 → (74 solo controllato) → 75 → 76.

## PASSO G0 — controlli e copia del giro 1 (OK)

- Ramo verificato: `prova`.
- Copia di sicurezza del giro 1:
  - `data/processed/risultato6_v2/giro1/` con 8 file JSON;
  - `docs/archivio/r6v2_giro1/` con i 9 rapporti.
- Database (sola lettura): al controllo delle 00:38 l'ultima lettura di `occupazione_pk` era
  **2026-10-18T17:47:52Z**, con **2 giorni feriali validi** (15 e 16/10) e 1 di fine settimana
  (17/10). Non è meno di 2 → si continua, ma è **[DATI SCARSI]**.
  I 4 parcheggi che non trasmettono: FERMI, RACCONIGI, UNIONE SOVIETICA, V PADIGLIONE.
- **Il database è stato aggiornato durante il lavoro** (file riscritto alle 00:40:24, probabile
  fetch automatico): ora l'ultima lettura è **2026-10-18T22:28:14Z** e le righe sono 50.799
  (erano 48.544). Con il file nuovo la **domenica 18/10 è completa** e conta come secondo giorno
  di fine settimana; i feriali validi restano 2. Tutti i passi di questo giro usano il file nuovo.
- Tutti i file di input richiesti ci sono (compreso `imq_zone.json`, che serve a G5).
- `luoghi.json` ha **5.087** luoghi: lo script 68 non è stato rilanciato.

## PASSO G1 — modulo delle strade (`scripts/77_strade_comuni.py`) (OK)

- Indice di 653.455 punti (vertici veri + punti finti ogni 25 m lungo i tratti lunghi: con i soli
  vertici i tratti più lunghi di 50 m non si troverebbero).
- **Punteggi corretti**: 4.443 tratte cambiano (**557 km**). Autostrada/tangenziale 5; primarie mai
  sotto 4 (184 alzate); secondarie mai sotto 3 (529 alzate); residenziali/di servizio/zone pedonali
  mai sopra 2 se `motivi` è vuoto (3.729 ridotte); le altre classi invariate. Il valore del giro 1
  resta in `punteggio_orig`.
- Controlli: primarie < 4 → **0**; secondarie < 3 → **0**.
- **GENOVA N.212** → strada **"genova" (primary, punteggio 4) a 6,2 m**, esito `ok` (nel giro 1 era
  un tratto di servizio).
- **Fermi** → strada **"edmondo de amicis" (tertiary, punteggio 2) a 46 m**; **asse d'ingresso = no**
  (l'asse ha il solo comune di Collegno). **Corso Francia in questa rete dista 313 m**, quindi resta
  fuori dai 50 m del primo passo della regola. Il piano prevedeva questa risposta e chiede di
  scriverla: fatto (non è un motivo di stop).
- **Venchi Unica** → strada **"francia" (primary, punteggio 5) a 24,8 m**, **asse d'ingresso = sì**
  (comuni Collegno, Rivoli, Torino).
- **Assi d'ingresso: 80** (il giro 1 ne contava 91: gli 11 di differenza hanno come unico "altro
  comune" un valore vuoto, che il piano dice di ignorare).
- **Via Torino a Venaria Reale**: nei dati del traffico **non esiste** nessuna tratta con nome o
  elenco nomi contenente "torino" nel comune di Venaria Reale → controllo non applicabile (scritto
  nel rapporto). La regola generale è comunque verificata.
- Esito della ricerca sui 5.087 luoghi: **ok 2.791 · strada_lontana 269 · solo_minore 205 ·
  nessuna 1.822**.

## PASSO G2 — segnali (`73_segnali_criticita.py`) (OK)

- a2 con il modulo 77: il valore è `min(5, punteggio_corr + 1 se asse d'ingresso)`; si salvano
  `a2_esito`, `a2_classe`, `a2_strada`, `a2_distanza_m` e il segnale `a2_incerto` quando la strada
  trovata è una stradina (esito `solo_minore`).
- Sensori del calo `d`: scartati quelli con calo negativo o sopra 0,9 o con velocità notturna sotto
  20 km/h → **97 usati, 12 scartati con il motivo** (fra cui SS31 Del Monferrato, calo −1,89).
- Controlli: **c2 = 95.297 spostamenti (1.139 interviste)** e **f = 24.459 (299 interviste)**:
  identici al giro 1. **GENOVA N.212: a2 = 4** (OK, prima era 1).
- **Luoghi con a2: 3.265** (giro 1: 3.261) → **senza a2: 1.822** (erano 1.826). Per esito: ok 2.791,
  strada_lontana 269, solo_minore 205 (di cui 205 marcati `a2_incerto`).
- **Confronto con il giro 1**: a2 cambia in **552 luoghi** (7 nuovi, 3 persi, 2.706 uguali).
  Differenza: −3 → 7, −2 → 17, −1 → 37, 0 → 2.706, +1 → 194, +2 → 188, +3 → 77, +4 → 32.
  I cambiamenti più grandi (da 1 a 5) sono luoghi dove prima si prendeva una stradina di servizio e
  ora un corso importante: Unione Sovietica, Park Stura Cap (tangenziale), Allamano, Casale,
  Brighenti/Al Traforo di Pino, Di Settimo, Francia (Collegno).

## PASSO G3 — funzione dei parcheggi (`72_nodi_tp.py`) (OK)

- Passo 4 (corse, nodi, stazioni) **invariato**: **346 nodi forti** come nel giro 1 (controllo OK).
- Classi (3.431 parcheggi considerati):

| Classe | Giro 1 | Giro 2 | Posti giro 2 |
|---|---|---|---|
| interscambio_di_fatto | 9 | **0** | 0 |
| solo_sulla_carta | 4 | 4 | 1.716 |
| potenziale | 725 | **758** | 56.566 |
| non_interscambio | 2.693 | 2.669 | 159.597 |

- Motivi: `nessun_punto` 2.445, `punti_a_favore` 758, `zona_centrale` 223,
  `dichiarato_non_usato` 4, `firma_non_pendolare` 1.
- Punti a favore (forza): 0 → 2.489 parcheggi, 1 → 370, 2 → 529, 3 → 43.
- **Sensibilità della zona centrale**: Q001 → 11 di fatto / 4 / 866 / 2.550 (56 in centro);
  Q001-Q005 → 7 / 4 / 820 / 2.600 (126); **Q001-Q009 (predefinito) → 0** / 4 / 758 / 2.669 (223);
  Q001-Q012 → 0 / 4 / 709 / 2.718 (317).
- Controlli richiesti, tutti **OK**: Molinette, CTO, Palagiustizia, Nizza, Stati Uniti, Ancona,
  Bacigalupo, Fontanesi, Ventimiglia = `non_interscambio / zona_centrale`; **Fermi = potenziale con
  forza 2**; i grandi parcheggi gratuiti OSM vicino a Fermi (1.226 posti a 178 m, 453 a 230 m, 281 a
  137 m) = potenziale; Stura, Caio Mario, Sofia, Venchi Unica = `solo_sulla_carta`.
- **Quanti "di fatto" restano: zero.** Non è un errore e le regole non sono state allargate: tutti i
  19 parcheggi con firma "pendolare" stanno dentro Q001-Q009 (ospedali, tribunale, garage del centro).

## PASSO G4 — soglie delle firme (`71_parcheggi_riempimento.py`) (OK)

- Soglie in cima allo script e da riga di comando: bloccato **0,06** (era 0,05), pendolare 0,20 (con
  fine settimana 0,10), residenziale 0,10, pieno 0,85, vuoto 0,15.
- Firme con i dati aggiornati: **pendolare 19, destinazione 7, misto 6, residenziale 2,
  dato_bloccato 3, nessun_dato 4**.
- Controlli: Fermi/Racconigi/Unione Sovietica/V Padiglione `nessun_dato` OK; Sofia `residenziale` OK;
  **Venchi Unica `dato_bloccato`** OK; **Caio Mario `dato_bloccato` + `vuoto`** OK; Porta Susa FS
  ciclo giorno/notte chiaro (notte 36,5%, giorno 78,2%) OK. Stura resta `misto` (79% notte, 90%
  giorno).
- Nuova **tabella di sensibilità** (bloccato 0,04/0,06/0,08 × pendolare 0,15/0,20/0,25) e parcheggi
  "fragili" (**7**: Bixio, Emanuele Filiberto, Lingotto, Madama Cristina, Palazzo Nuoto, Porta
  Palazzo, Venchi Unica).

## PASSO G5 — universo e scenari (`75_risultato6_v2.py`) (OK)

- **Universo = 4.425 luoghi** (macro-aree "01 Torino" 1.673, "02 Cintura" 1.259, "03 Resto CMTO"
  1.493), esattamente l'atteso. Fuori: 403 (10 Cuneo), 153 (08 Asti), 75 (09 Alessandria), 8 (04
  Vercelli) e **23 luoghi senza zona IMQ** (elencati con nome e coordinate nel rapporto: decide Leo).
- Controllo di riproducibilità della v1 sulle 7.045 fermate: **611 / 17 / 594** → **OK**.

| Scenario | Segnali | Luoghi critici | Coperti U | F | P | F+S (200 m) |
|---|---|---|---|---|---|---|
| S1 riferimento v1 | a1, b1, c1 | 374 | 13 | 117 | 135 | 122 |
| S2 integrato | a1, a2, b2, c1, c2_ztl, d, e | 378 | 11 | 140 | 147 | 144 |
| S3 solo nuovi | a2, b2, c2_ztl, d, e | 385 | 12 | 147 | 160 | 152 |

- A 100 m e 400 m (F): S1 56/210 · S2 69/229 · S3 78/229. Tabelle complete nel rapporto.
- Confronto fra scenari: **S1∩S2 = 279 (entrano 99, escono 95)**; **S1∩S3 = 253 (entrano 132,
  escono 121)**; **S2∩S3 = 309**.
- Confronto con il giro 1: S1 438 → 374 (restano 374, entrano 0, escono 64);
  S2 436 → 378 (restano 327, entrano 51, escono 109); S3 438 → 385 (restano 335, entrano 50, escono 103).
- Sensibilità su S2 (378 critici): senza a1 125 cambiano, senza a2 131, senza b2 146, senza c1 132,
  senza c2_ztl 145, senza d 10, senza e 95; c2 al posto di c2_ztl 16; b_giorno al posto di b2 6;
  **b1 al posto di b2 41**; universo "tutto" 63 (tutti in più, 0 in meno).
- Salvati in `scenari.json` anche `per_zona` (critici e coperti F a 200 m per zona IMQ) e
  `piu_scoperti` (i 25 più gravi senza U né F a 400 m, per ogni scenario).

## PASSO G7 — verifiche indipendenti (`76_verifiche_r6v2.py`) (OK)

Tutte superate (`docs/RAPPORTO_R6V2_VERIFICHE.txt`):

1. Luoghi con cKDTree 41 m + filtro haversine + componenti connesse: **5.087 = 5.087**.
2. b2 e c2 di 5 luoghi a caso (seme 20261018): **identici**.
3. Firma di Porta Susa FS e Venchi Unica rifatta con pandas: **identica**.
4. Superficie di 3 parcheggi OSM vicino a Fermi con shapely in EPSG:32632: **0,51%** (limite 2%).
5. Copertura U a 200 m sulle fermate v1: **17**, come la v1.
6. [nuovo] **a2 di 8 luoghi** rifatto con shapely/STRtree in EPSG:32632: nome strada, valore e esito
   **tutti uguali**.
7. [nuovo] **Universo** rifatto con pandas: **4.425 = 4.425**.
8. [nuovo] **zona centrale, forza e classe di 5 parcheggi** (3 del 5T + 2 OSM) rifatti a mano:
   **tutti uguali**.
9. [nuovo] **Soglia del 90° di S2** rifatta con numpy e `rankdata`: 63,97 contro 63,97
   (differenza 0,002 → uguale). Alla prima prova era diversa di 0,02 perché la verifica usava
   `c2_ztl` invece di `c2_ztl` completato con l'ISTAT: corretto e ora coincide.
10. git: **nessun commit**. Vedi la sezione "File" per i file modificati.

## Risposte ai 4 problemi posti da Leo

**1) a2 e asse d'ingresso.**
- GENOVA N.212 (Moncalieri): ora la strada è **Strada Genova** (primary) a 6,2 m, **a2 = 4** (prima
  era un tratto di servizio con a2 = 1).
- Via Torino a Venaria Reale: **nei dati non esiste** una strada con questo nome nel comune di
  Venaria Reale (cercato sia `nome` sia `nomi`): controllo non applicabile. La regola generale
  funziona (0 secondarie sotto 3).
- Fermi: strada trovata "edmondo de amicis" (tertiary, 2) a 46 m, **non** su un asse d'ingresso;
  Corso Francia in questa rete è a **313 m** (fuori dai 50 m della regola). Venchi Unica: "francia"
  (primary, 5) a 24,8 m, **su un asse d'ingresso** (Collegno, Rivoli, Torino).
- Parcheggi su un asse d'ingresso: **210** su 3.431 (nel giro 1 erano 42: con la regola nuova si
  trova più spesso un corso importante invece di una stradina). 13 parcheggi non hanno nessuna
  strada entro 150 m; 622 hanno solo una stradina entro 50 m.
- Effetto complessivo: a2 cambia in **552 luoghi** (194 volte +1, 188 +2, 77 +3, 32 +4; solo 61
  luoghi scendono). Nei test di sensibilità a2 è fra i segnali che spostano più luoghi (131).

**2) "Di fatto".** Restano **zero** con la zona centrale Q001-Q009. Con la sola Q001 sarebbero **11**,
  con Q001-Q005 sarebbero **7**. I 19 parcheggi con firma "pendolare" stanno tutti in Q001-Q009:
  sono garage di ospedali, tribunale e centro (Molinette, CTO, Palagiustizia, Nizza…), non
  interscambi di periferia. Le regole non sono state allargate per farne uscire qualcuno.

**3) Universo.** 4.425 luoghi (Torino 1.673, cintura 1.259, resto della Città metropolitana 1.493).
  Fuori 639 luoghi in altre province e **23 senza zona IMQ** (elencati nel rapporto): su questi 23
  decide Leo.

**4) b1 → b2.** Negli scenari nuovi b1 non c'è più; al suo posto b2 (corse/ora nelle ore dei
  pendolari). Mettendo b1 al posto di b2 in S2 cambiano 41 luoghi (21 entrano, 20 escono); usando la
  media di tutta la giornata (`b_giorno`) cambiano solo 6. Quindi la sostituzione conta, ma molto
  meno di a1, a2, c1 e c2_ztl.

## Tabella per Leo (per scegliere lo scenario — nessuna raccomandazione)

| | S1 "riferimento v1" | S2 "integrato" | S3 "solo nuovi" |
|---|---|---|---|
| Cosa misura | solo i segnali del giro 1 (corridoio, corse di punta, pendolari) portati sui luoghi | vecchi + nuovi insieme (corridoio, strada, corse dei pendolari, pendolari, ZTL, calo di velocità, nodi) | solo i segnali nuovi |
| Luoghi critici | 374 | 378 | 385 |
| Coperti a 200 m (U / F / P) | 13 / 117 / 135 | 11 / 140 / 147 | 12 / 147 / 160 |
| Coperti a 200 m aggiungendo i "solo sulla carta" (F+S) | 122 | 144 | 152 |
| Esempi che ENTRANO rispetto a S1 | (nessuno: S1 è il riferimento) | Ponte Po (C009), Duchessa Jolanda EST (Q005), metrò Pozzo Strada (Q014) | metrò Pozzo Strada (Q014), Goito cap (C009), Torino-Stazione (C011) |
| Esempi che ESCONO rispetto a S1 | (nessuno) | Pinerolo (C015), Fermata 12 - Pozzo Strada (Q014), Cattaneo (Q012) | Don Borio (C002), Massaua Ovest (Q014), Antica di Grugliasco (C002) |
| Cosa NON dice | niente su strade, ZTL, velocità, nodi | mescola vecchi e nuovi, quindi non si sa "quanto aggiunge" ciascuno | butta via il corridoio e i pendolari della v1 |

Dettaglio completo di chi entra e chi esce (15 per volta) nei tre scenari: nel rapporto del Passo G5.

## Anomalie, differenze dagli attesi e limiti

1. **Il database è cambiato a metà lavoro** (00:40): la domenica 18/10 è diventata un giorno di
   fine settimana valido. Le firme del riempimento non sono quindi confrontabili 1:1 con il giro 1.
2. **Assi d'ingresso: 80** invece dei "circa 91" attesi; la differenza è spiegata dalla regola
   "ignora comune = None" chiesta dal piano (11 assi).
3. **Fermi non è su Corso Francia** in questa rete stradale (313 m): scritto, non è un motivo di stop.
4. **Via Torino a Venaria Reale** non esiste nei dati: controllo non applicabile.
5. **"Interscambio di fatto": zero** (con Q001-Q009); con la sola Q001 sarebbero 11.
6. **Nel working tree risultano modificati anche `MEMORIA_PROGETTO.md` e
   `docs/RAPPORTO_VELOCITA_5T.txt`**: NON li ha toccati questo giro (sono della sessione di Claude
   delle 00:36–00:41, insieme all'aggiornamento del database). Li lascio come sono.
7. Un sensore velocità (SS31 Del Monferrato) aveva calo −1,89: ora viene scartato.
8. Alla prima esecuzione la verifica n. 7 (soglia del 90°) segnalava una differenza di 0,02: era un
   errore **della verifica** (usava c2_ztl senza il completamento ISTAT), corretto e ora coincidono.
9. Limiti da tenere presenti (dal piano, sezione 4): riempimento con pochi giorni [DATI SCARSI];
   parcheggi OSM incompleti e posti stimati [STIMATO]; zona centrale Q001-Q009 provvisoria;
   pendolari IMQ campionari; l'importanza della strada viene da una stima debole (±38%); calo di
   velocità solo vicino a 97 sensori; distanze in linea d'aria; corse programmate; universo solo
   Città metropolitana; frequenze dei treni non disponibili.

## File

**Modificati da questo giro** (come previsto dalla regola 0.2 del piano):
`scripts/71_parcheggi_riempimento.py`, `scripts/72_nodi_tp.py`, `scripts/73_segnali_criticita.py`,
`scripts/75_risultato6_v2.py`, `scripts/76_verifiche_r6v2.py`; più i rapporti rigenerati dai lanci
(`docs/RAPPORTO_R6V2_RIEMPIMENTO.txt`, `RAPPORTO_R6V2_FUNZIONE.txt`, `RAPPORTO_R6V2_SEGNALI.txt`,
`RAPPORTO_RISULTATO6_V2.txt`, `RAPPORTO_R6V2_VERIFICHE.txt`).

**Nuovi**: `scripts/77_strade_comuni.py`, `docs/RAPPORTO_R6V2_STRADE.txt`,
`docs/ESITO_RISULTATO6_V2_GIRO2.md`, `data/processed/risultato6_v2/giro1/` (copia),
`docs/archivio/r6v2_giro1/` (copia).

**Dati rigenerati** in `data/processed/risultato6_v2/`: `riempimento.json`, `nodi.json`,
`parcheggi_funzione.json`, `segnali.json`, `scenari.json`. Non toccati (e non rilanciati):
`luoghi.json`, `parcheggi.json`, `istat2011_proporzioni.json`.

## Cosa resta

1. **Leo sceglie lo scenario** (S1, S2 o S3) e, se vuole, cambia le soglie delle firme e la zona
   centrale dei parcheggi: sono tutti parametri da riga di comando.
2. Se compare la riga `SCENARIO SCELTO:` in `docs/PIANO_RISULTATO6_V2_GIRO2.md` (punto G9.0), si può
   fare il Passo G9 (scheda in `simulazione.html`): **non fatto** perché quella riga è vuota.
3. Il giro va rifatto quando ci saranno **almeno 5 giorni feriali** di riempimento.
4. Nessun commit è stato fatto: decide Leo.
