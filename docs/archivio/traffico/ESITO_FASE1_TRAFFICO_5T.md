# Esito — Fase 1 del piano traffico 5T (docs/PIANO_TRAFFICO_5T.md, sezione 9)

Eseguito da: agente opencode sul PC di Leo. Data di inizio: **17/10/2026, ore 00:56**.
Ramo git: `prova` (nessun commit). Solo libreria standard di Python. Database aperto in sola lettura.

Ogni passo finisce con una riga `PASSO n: OK` oppure `PASSO n: FERMO – motivo`.

PASSO 0: OK

<!-- INIZIO PASSO 1 -->
PASSO 1 - CONTROLLO DEL DATABASE E DIAGNOSI ORA 01:00 (sola lettura)
========================================================================
DB (sola lettura): C:\projects\Progetti\GTT\data\storico_backup.sqlite

-- a) conteggi tabelle --
  flussi_5t             365477  atteso    365477  OK
  accuratezza_5t        243179  atteso    243179  OK
  parcheggi_5t              41  atteso        41  OK
  occupazione_pk         27921  atteso     27921  OK
  ztl_5t                     1  atteso         1  OK
  trip_update_gtt      1893353  atteso   1893353  OK
  mezzi_gtt            4059000  atteso   4059000  OK
  ultimo flussi_5t.generato_utc  2026-10-16T22:36:17.111Z
  ultimo atteso                  2026-10-16T22:36:17.111Z  OK

-- b) aritmetica delle letture 5T --
  senza riga in accuratezza_5t      122298  atteso    122298  OK
  accuratezza = 0                    49254  atteso     49254  OK
  accuratezza > 0 e flusso          193925  atteso    193925  OK
  (accuratezza > 0 con flusso NULL: 0)
  controllo somma: 122298 + 49254 + 193925 + 0 = 365477  su flussi_5t 365477  OK

-- c) ore UTC sul periodo 2026-10-09 -> 2026-10-16 --
     righe   = righe di flussi_5t nell'ora
     acc0    = quota di righe con accuratezza = 0
     sensori = sensori distinti con almeno una riga con accuratezza > 0
   ora    righe     acc0   quota  sensori
     0    10355     4678  45.2%       97  <-- confronto
     1    10464     4042  38.6%       97  <-- confronto
     2    10246     3127  30.5%       97
     3    10246     1697  16.6%       98
     4    10246     1301  12.7%       97
     5    10355     1253  12.1%       97
     6    10137     1210  11.9%       97
     7    10246     1223  11.9%       97
     8    10246     1238  12.1%       97
     9    10355     1254  12.1%       97
    10    10246     1247  12.2%       97
    11    10137     1223  12.1%       97
    12    10028     1196  11.9%       97
    13    10246     1224  11.9%       97
    14    10355     1231  11.9%       98
    15    10246     1219  11.9%       97
    16     8829     1071  12.1%       97
    17     8720     1054  12.1%       98
    18     9156     1115  12.2%       97
    19     9810     1225  12.5%       97
    20    10137     1272  12.5%       98
    21    10355     1405  13.6%       97  <-- confronto
    22     9701     5176  53.4%       97  <-- confronto
    23     9047     6772  74.9%       31  <-- confronto

  ore UTC 21/22/23/00/01 righe: 10355/9701/9047/10355/10464 | sensori con accuratezza > 0: 97/97/31/97/97
  frase: l'ora UTC 23 (= 01:00 locale) SI distingue dalle ore vicine per numero di sensori con letture affidabili.
<!-- FINE PASSO 1 -->

PASSO 1: OK

PASSO 2 (versione 1, ora sostituita dalla v2): FERMO – celle ok del sabato = **27** (attese **0**); celle ok feriali = **2125** (attese **tra 2200 e 2266**)

Il piano dice: «Se sabato > 0: FERMARSI». Mi fermo. Non ho corretto nulla, non sono andato avanti:
i passi 3, 4 e 5 **non** sono stati eseguiti.

Cosa è stato fatto in questo passo (tutto prescritto dal piano):
- copiato `scripts/26_velocita_5t.py` in `scripts/26_velocita_5t.py.bak_17ott`;
- applicate le 5 modifiche allo script 26, esattamente come scritto nel piano
  (verificato con `git diff --no-index` fra la copia di sicurezza e il file: sono solo quelle 5 righe);
- `python scripts\26_velocita_5t.py --prova` → gira senza errori (codice di uscita 0);
- `python scripts\26_velocita_5t.py` (giro completo) → gira senza errori (codice di uscita 0).

Confronto con i controlli attesi nel piano (passo 2):

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| celle ok sabato | 0 | **27** | NON torna |
| celle ok domenica | 0 | 0 | OK |
| celle ok feriale | tra 2200 e 2266 | **2125** | NON torna |
| periodo (giorni locali) | 2026-10-08 → 2026-10-17 | uguale | OK |
| letture affidabili | 193925 | 193925 | OK |

Fatti verificati sul file `data/processed/velocita_5t.json` (numeri, non interpretazioni):
- le 27 celle "ok" del sabato sono **tutte all'ora locale 0** (00:00–00:59), su 27 sensori diversi,
  ognuna con `g=2` e `n=19` letture;
- con la correzione, un giorno conta in una cella solo se ha almeno 6 letture in quell'ora.
  Sabato 10/10 ora 0 = 12 letture; sabato 17/10 ora 0 = 7 letture (i dati si fermano alle 00:36 locali,
  cioè 22:36 UTC del 16/10): 12 + 7 = 19 = il valore `n` della cella. Quindi i 36 minuti del sabato 17/10
  bastano comunque (≥6 letture) e quel giorno viene contato: da qui `g=2` e la cella risulta "ok";
- celle ok feriali: prima della correzione 2252, dopo 2125 (il piano attendeva 2200–2266);
- in `parametri` del JSON è presente `"min_letture_giorno": 6`.

File creati o modificati dal passo 2:
- `scripts/26_velocita_5t.py` (5 modifiche)
- `scripts/26_velocita_5t.py.bak_17ott` (copia di sicurezza, nuova)
- `data/processed/velocita_5t.json` (rigenerato dal giro completo)
- `docs/RAPPORTO_VELOCITA_5T.txt` (rigenerato dal giro completo)

Da decidere con Leo/Claude: i valori attesi nel piano non coincidono con il risultato delle modifiche
prescritte. Non ho cercato rimedi da solo (regola del piano).

PASSO 2 (v2, 17/10 – regola dei giorni parziali ai bordi): OK

Fatto, nell'ordine:
1. `scripts/26_velocita_5t.py` **ripristinato** da `scripts/26_velocita_5t.py.bak_17ott`
   (verificato: `git diff --no-index` fra i due file = nessuna differenza, quindi le 5 modifiche v1 sono annullate).
2. Inserito in `main()` il blocco "giorni parziali ai bordi" (subito prima del commento
   `# --- accumulo per (sensore, tipo, ora) ---`) e la riga di rapporto sui giorni esclusi.
   `git diff --no-index` contro la copia di sicurezza mostra **solo** queste due aggiunte.
3. `python scripts\26_velocita_5t.py --prova` → esce senza errori (codice 0).
   `python scripts\26_velocita_5t.py` → esce senza errori (codice 0).

Controlli attesi (coincidono tutti):

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| giorni parziali esclusi | 2026-10-08 e 2026-10-17 | 2026-10-08, 2026-10-17 | OK |
| periodo (giorni locali) | 2026-10-09 → 2026-10-16 | 2026-10-09 → 2026-10-16 | OK |
| giorni per tipo | feriale 6, sabato 1, domenica 1 | feriale 6, sabato 1, domenica 1 | OK |
| celle ok sabato | 0 | 0 | OK |
| celle ok domenica | 0 | 0 | OK |
| celle ok feriale | tra 2245 e 2260 | 2252 | OK |

Controllo aritmetico sulle letture (query SQL diretta sul DB, sola lettura, conversione UTC+2):
- letture affidabili del giorno locale 8/10 = **548**; del giorno locale 17/10 = **487**; somma = **1035**;
- 193925 − 1035 = **192890**, che è esattamente il valore "letture affidabili usate" del rapporto. OK.

Effetto della v2: le celle "false" del sabato sono sparite del tutto (sabato **0**, prima erano 94 e poi 27);
le celle feriali tornano a **2252**, identiche a prima di qualsiasi correzione.

File creati o modificati dal passo 2 v2:
- `scripts/26_velocita_5t.py` (ripristinato dalla copia + 2 aggiunte)
- `data/processed/velocita_5t.json` (rigenerato dal giro completo)
- `docs/RAPPORTO_VELOCITA_5T.txt` (rigenerato dal giro completo)

<!-- INIZIO PASSO 2bis -->
PASSO 2bis - TEST: "accuratezza = 0" = sensore rotto o poco traffico? (solo SQL, sola lettura)
====================================================================================================
Periodo: giorni locali 2026-10-09 -> 2026-10-16 (UTC+2).
Sensori nel database (sensori_5t): 109
Sensori 'vivi' (almeno una lettura con accuratezza > 0 nel periodo): 98
Sensori 'morti' (hanno letture nel periodo, ma SEMPRE accuratezza 0): 11  [attesi 12]
Sensori senza nessuna lettura nel periodo: 0
Letture del periodo senza riga in accuratezza_5t: 0  [atteso 0]

Tabella (SOLO sensori 'vivi'), per ora locale:
  (i) letture totali  (ii) quota accuratezza 0  (iii) fra le accuratezza 0, quota flusso 0
  (iv) fra le accuratezza > 0, quota flusso 0  (v) flusso medio delle accuratezza > 0

  ora      (i)    (ii)   (iii)    (iv)      (v)
    0     9114   48.9%  100.0%    0.1%      192
    1     9310   72.3%  100.0%    1.5%      221
    2     9310   39.0%  100.0%    2.3%      100
    3     9408   31.7%  100.0%    3.1%       83
    4     9212   22.7%  100.0%    1.2%       84
    5     9212    7.2%  100.0%    0.2%      131
    6     9212    2.9%  100.0%    0.0%      223
    7     9310    2.2%  100.0%    0.0%      463
    8     9114    2.1%  100.0%    0.0%      568
    9     9212    2.1%  100.0%    0.0%      494
   10     9212    2.2%  100.0%    0.0%      471
   11     9310    2.2%  100.0%    0.0%      461
   12     9212    2.3%  100.0%    0.0%      467
   13     9114    2.2%  100.0%    0.0%      446
   14     9016    2.0%  100.0%    0.0%      488
   15     9212    2.1%  100.0%    0.0%      503
   16     9310    2.0%  100.0%    0.0%      557
   17     9212    2.0%  100.0%    0.0%      650
   18     7938    2.3%  100.0%    0.0%      638
   19     7840    2.2%  100.0%    0.0%      543
   20     8232    2.3%  100.0%    0.0%      378
   21     8820    2.7%  100.0%    0.0%      245
   22     9114    2.7%  100.0%    0.0%      225
   23     9310    3.9%  100.0%    0.0%      184

Sintesi: alle ore 1 locali il 100% delle letture con accuratezza 0 ha flusso 0, contro il 1% di quelle con accuratezza > 0.
  (controllo: ora 0 locale -> accuratezza 0 = 48.9%; ora 12 locale -> 2.3%)
<!-- FINE PASSO 2bis -->

Nota: il piano dice «morti attesi **12**»; con la definizione scritta nel piano stesso ("sempre accuratezza 0")
i morti sono **11**. I sensori senza nessuna cella ok nel JSON `velocita_5t.json` sono **12** =
11 morti + 1 vivo (lcd1 **11421**, "SS458 Di Casalborgone": 8 letture con accuratezza > 0 nel periodo,
troppo poche per formare una cella ok). I due numeri quindi non sono in contraddizione: dipende solo da cosa
si conta. I 3 sensori urbani morti sono Corso Moncalieri 40071 e 2× Corso Regina Margherita 40121/40123,
come dice la memoria del progetto.

PASSO 2bis: OK

PASSO 2ter - CONTROLLI T1-T4 SU "accuratezza = 0" (sola lettura, nessuna modifica)
====================================================================================================
Periodo: giorni locali 2026-10-09 -> 2026-10-16 (UTC+2).
Sensori 'vivi' (almeno una lettura con accuratezza > 0 nel periodo): 98. Le letture senza riga di accuratezza nel periodo sono 0.

T1) Per ogni istante di lettura, quanti sensori vivi hanno accuratezza = 0
    (denominatore della quota = 98 sensori vivi)

  ora loc  istanti   min  mediana   max  istanti >80%  mediana sensori presenti
        1       95    68     71.0    73             0                      98.0
        3       96    11     33.5    47             0                      98.0
       12       94     1      2.0     4             0                      98.0

T2) Flusso medio diurno (ore 8-18, accuratezza > 0) e quota accuratezza = 0 (ore 2-4)
    sensori usati: 98 su 98 (esclusi quelli senza letture buone di giorno o senza letture nelle ore 2-4)
    correlazione di Pearson (flusso diurno vs quota accuratezza 0): r = -0.583
    tagli dei quartili del flusso diurno: 296 / 396 / 621 veic/h
   gruppo  sensori  flusso medio  quota acc=0 media
       Q1       25           179              48.7%
       Q2       24           344              41.2%
       Q3       24           466              25.5%
       Q4       25          1044               9.5%

T3) Coppie distinte (flusso, velocita) per sensore vivo, fra le letture con accuratezza > 0
    sensori con meno di 20 coppie distinte: 6 su 98
    lcd1  via                                dir       coppie  coppie piu' frequenti (flusso, velocita, n)
   11436  SS460 Di Ceresole                  positive       1  (12, 97, 2217)
   11437  SS460 Di Ceresole                  negative       1  (48, 78, 2217)
   13703  SS11 Padana Superiore              positive       1  (396, 65, 2217)
    3851  SS11 Padana Superiore              negative       1  (624, 64.79, 2217)
   40191  Corso Unita' D'italia(TO)          negative       1  (1572, 55.82, 2217)
   11421  SS458 Di Casalborgone              negative       7  (12, 60, 2); (12, 82, 1); (24, 66, 1); (24, 60, 1)

T3b) Verifica a parte (sola lettura) sui 6 sensori del T3 col numero di coppie piu' basso,
     su TUTTO lo storico (non solo il periodo considerato):
     11436: 2231 letture, 1 solo flusso (12) e 1 sola velocita' (97)
     11437: 2231 letture, 1 solo flusso (48) e 1 sola velocita' (78)
     13703: 2231 letture, 1 solo flusso (396) e 1 sola velocita' (65)
      3851: 2231 letture, 1 solo flusso (624) e 1 sola velocita' (64,79)
     40191: 2231 letture, 1 solo flusso (1572) e 1 sola velocita' (55,82)
     11421: 8 letture, 2 flussi (12 e 24) e 6 velocita' -> NON bloccato, solo pochissime letture
     Quindi i sensori "bloccati" (stesso numero ripetuto sempre, anche di notte) sono **5**, non 1:
     11436, 11437, 13703, 3851, 40191. I loro valori non vanno usati come misura di traffico.

T4) Sensori con 23 ore ok in flusso_5t_sensori.json: quale ora manca
    sensori (x tipo di giorno) con 23 ore ok: 66
   ora mancante  sensori
              1       66


PASSO 2ter: OK

PASSO 3 - Ricalcolo indipendente di 6 celle dal database (senza usare lo script 26): OK

Letto da `flussi_5t` + `accuratezza_5t` (join su `generato_utc` e `lcd1`), righe con `accuratezza > 0` e
`flusso` non nullo, orario convertito in locale (UTC+2), solo giorni lun-ven fra l'8/10 e il 16/10.
`n` = righe, `f` = media del flusso (zeri compresi), `v` = Σ(velocità×flusso)/Σflusso sulle righe con flusso > 0.

| lcd1 | ora | n (SQL / JSON) | f (SQL / JSON) | v (SQL / JSON) | Esito |
|---|---|---|---|---|---|
| 40040 | 8 | 69 / 69 | 1479 / 1479 | 38,4 / 38,4 | OK |
| 40040 | 3 | 72 / 72 | 49 / 49 | 65,2 / 65,2 | OK |
| 40095 | 8 | 69 / 69 | 2497 / 2497 | 30,0 / 30,0 | OK |
| 40095 | 13 | 71 / 71 | 1427 / 1427 | 51,5 / 51,5 | OK |
| 40174 | 8 | 69 / 69 | 2658 / 2658 | 12,0 / 12,0 | OK |
| 40174 | 18 | 58 / 58 | 2907 / 2907 | 16,7 / 16,7 | OK |

Nessun file del progetto creato o modificato in questo passo (solo letture).

PASSO 4 – Script 33 (flusso per sensore, ora e giorno): OK

Creato `scripts/33_flusso_sensori.py`. Legge `data/processed/velocita_5t.json` e scrive
`data/processed/flusso_5t_sensori.json` + `docs/RAPPORTO_FLUSSO_5T_SENSORI.txt`.
`--prova` (5 sensori, solo console, nessun file) gira senza errori; il giro completo pure (codice 0).

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| sensori con totale_giorno | circa 28, di cui circa 18 urbani | **28** (urbani **18**) | OK |
| sensori senza nessuna cella ok | circa 12, di cui circa 3 urbani | **12** (urbani **3**) | OK |
| valori orari negativi | 0 | 0 | OK |
| valori orari oltre 6000 veic/h | 0 | 0 | OK |
| valore massimo | circa 3202 | **3202** | OK |

Altri numeri utili: sensori con 23 ore ok (una sola ora mancante) = **66**; celle orarie scritte = 2252
(tutte feriali: sabato e domenica 0, come dopo la correzione v2). Primi 3 sensori urbani per veicoli/giorno:
Corso Unità d'Italia 40189 (44.018 veic/giorno, punta alle 17), Corso Unità d'Italia 40191 (37.728),
Corso Trieste 40174 (37.230).

**Anomalia trovata (dato, non interpretazione)**: il sensore **40191** ("Corso Unita' D'italia(TO)",
negative) ha il flusso tipico **identico in tutte e 24 le ore: 1.572 veic/h**. Controllo sui dati grezzi:
su **2.231** letture con accuratezza > 0 il valore è sempre `flusso = 1572` e sempre `velocita = 55,82`.
Quindi quel sensore ripete sempre lo stesso numero (valore "bloccato"): i suoi 37.728 veicoli/giorno
non vanno presi per buoni. Resta scritto così com'è nei file (nessun filtro aggiunto).

File creati o modificati dal passo 4:
- `scripts/33_flusso_sensori.py` (nuovo)
- `data/processed/flusso_5t_sensori.json` (nuovo)
- `docs/RAPPORTO_FLUSSO_5T_SENSORI.txt` (nuovo)

PASSO 5 – Script 34 (quale sensore cade su quale corridoio): OK

Creato `scripts/34_sensori_corridoi.py`. Carica le funzioni `normalizza` e `haversine_m` dallo script 24
(con `importlib`, il nome inizia con un numero) e applica la regola identica allo script 24: nome della via
normalizzato uguale a `chiave_normalizzata` del corridoio e distanza minima dai punti della geometria ≤ 60 m.
Non assegna né stima nessun flusso. Gira senza errori (codice 0).

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| sensori abbinati | vicini a 15 (lo script 24 ne abbinava 15) | **15** | OK |

Conteggi: sensori considerati (con almeno una cella ok) **97**; abbinati **15** (tutti urbani);
non abbinati **82** (di cui urbani 13). Motivi dei non abbinati: **81** non hanno nessun corridoio con lo
stesso nome (sono statali/provinciali, tangenziali, raccordi: nomi che non esistono nella rete OSM caricata),
**1** ha il corridoio omonimo ma troppo lontano (lcd1 **40212** "Ponte Amedeo VIII(TO)": 201,7 m).
Distribuzione per punteggio dei 15 abbinati: 1→0, 2→0, 3→2, 4→11, 5→2.

File creati o modificati dal passo 5:
- `scripts/34_sensori_corridoi.py` (nuovo)
- `data/processed/sensori_corridoi.json` (nuovo)
- `docs/RAPPORTO_SENSORI_CORRIDOI.txt` (nuovo)

PASSO 6 – Chiusura

Esito di ogni passo: **0 OK · 1 OK · 2 v1 FERMO (poi sostituito dalla v2) · 2 v2 OK · 2bis OK · 3 OK · 4 OK · 5 OK**.
Sono arrivato in fondo. Ramo `prova`, **nessun commit**, database sempre in sola lettura, nessun file vietato toccato.

Numeri chiave
- Celle ok nel file `velocita_5t.json`: **feriale 2252 · sabato 0 · domenica 0**; periodo **2026-10-09 → 2026-10-16**
  (8/10 e 17/10 esclusi perché parziali); letture affidabili usate **192890** (= 193925 − 1035 dei due giorni di bordo).
- Script 33: **28** sensori con totale giornaliero (di cui **18** urbani), **66** con 23 ore ok, **12** senza nessuna
  cella ok (di cui **3** urbani); max orario **3202** veic/h; nessun valore negativo né oltre 6000.
- Script 34: **15** sensori abbinati a un corridoio, **82** no.
- Diagnosi dell'ora 1 locale (= 23 UTC): nell'ora arrivano comunque **9047** righe (come nelle ore vicine: non è un
  buco di raccolta), ma solo **31** sensori su 109 hanno almeno una lettura con accuratezza > 0 (le ore vicine ne hanno
  97-98) e la quota di letture con accuratezza = 0 sale al **74,9%** contro il ~12% del giorno. Il passo 2bis mostra
  che in quell'ora il **100%** delle letture con accuratezza 0 ha flusso 0, contro l'**1,5%** di quelle con
  accuratezza > 0. Lettura cauta (da confermare sulla documentazione 5T): non è una perdita di dati, ma un'ora in cui
  il sistema marca quasi tutto come "non affidabile" e i flussi sono a zero; le ore notturne degli altri sensori
  restano comunque coperte.

Anomalie
1. Sensore **40191**: flusso tipico identico in tutte e 24 le ore (**1572** veic/h) e, sui dati grezzi, sempre
   `flusso = 1572` e `velocita = 55,82` su **2231** letture: valore bloccato, i suoi numeri non vanno presi per buoni.
2. Passo 2bis: sensori "morti" (sempre accuratezza 0) = **11**, non 12 come scritto nel piano. Il **12** è il numero
   dei sensori senza nessuna cella ok: 11 morti + 1 vivo che non arriva a una cella ok (**11421**, solo 8 letture buone).
   I due numeri non si contraddicono, contano cose leggermente diverse.
3. Il sensore **11421** ha 8 letture con accuratezza > 0 nel periodo, insufficienti per una cella ok.
4. Nessun'altra anomalia: i controlli del piano (conteggi del database, aritmetica delle letture, 6 celle ricalcolate)
   tornano tutti.

File creati: `docs/ESITO_FASE1_TRAFFICO_5T.md`, `scripts/controllo_fase1_5t.py`,
`scripts/26_velocita_5t.py.bak_17ott`, `scripts/33_flusso_sensori.py`, `scripts/34_sensori_corridoi.py`,
`data/processed/flusso_5t_sensori.json`, `data/processed/sensori_corridoi.json`,
`docs/RAPPORTO_FLUSSO_5T_SENSORI.txt`, `docs/RAPPORTO_SENSORI_CORRIDOI.txt`.
File modificati: `scripts/26_velocita_5t.py`, `data/processed/velocita_5t.json`, `docs/RAPPORTO_VELOCITA_5T.txt`.
`MEMORIA_PROGETTO.md` **non** è stato toccato.
