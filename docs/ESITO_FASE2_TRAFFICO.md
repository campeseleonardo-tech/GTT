# Esito — Fase 2 del piano traffico 5T (docs/PIANO_TRAFFICO_FASE2.md, sezione 3)

Eseguito da: agente opencode sul PC di Leo. Data: **17/10/2026, ore 01:31 → 01:42**.
Ramo git: `prova` (nessun commit). Solo libreria standard di Python. Database aperto in sola lettura.
Sono stati eseguiti **solo i Passi 7 e 8**. Il **Passo 9 NON è stato fatto**: serve prima la revisione di
Claude sulla tabella DA_VEDERE e il file `data/processed/abbinamenti_confermati.json`.

---

## PASSO 7: OK

### 7a — Sensori da escludere

Creato `scripts/35_sensori_esclusi.py` → `data/processed/sensori_esclusi.json` (lista di
`{lcd1, nome, motivo}`) e `docs/RAPPORTO_SENSORI_ESCLUSI.txt`. Periodo: giorni locali 9→16/10 (UTC+2).

Regole applicate (una sola per sensore, in quest'ordine):

1. **morto** = nel periodo ha letture ma tutte con accuratezza 0;
2. **bloccato** = almeno 500 letture con accuratezza > 0 ma meno di 20 coppie distinte (flusso, velocità);
3. **pochi dati** = ha letture con accuratezza > 0 ma nessuna cella ok in `velocita_5t.json`.

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| morti | 11 (urbani 3) | **11** (urbani **3**) | OK |
| bloccati | 5 | **5** | OK |
| pochi dati | 1 (11421) | **1** (11421) | OK |
| esclusi in tutto | 17 | **17** | OK |
| sensori usabili | 109 − 17 = 92 | **92** | OK |

I 17 esclusi:

| lcd1 | nome | dir | urbano | motivo | letture | acc>0 | coppie |
|---|---|---|---|---|---|---|---|
| 11436 | SS460 Di Ceresole | positive | no | bloccato | 2217 | 2217 | 1 |
| 11437 | SS460 Di Ceresole | negative | no | bloccato | 2217 | 2217 | 1 |
| 13703 | SS11 Padana Superiore | positive | no | bloccato | 2217 | 2217 | 1 |
| 3851 | SS11 Padana Superiore | negative | no | bloccato | 2217 | 2217 | 1 |
| 40191 | Corso Unita' D'italia(TO) | negative | **si** | bloccato | 2217 | 2217 | 1 |
| 11787 | SS494 Vigevanese | positive | no | morto | 2217 | 0 | 0 |
| 11788 | SS494 Vigevanese | negative | no | morto | 2217 | 0 | 0 |
| 14789 | SP155(AL) | positive | no | morto | 2217 | 0 | 0 |
| 14790 | SP155(AL) | negative | no | morto | 2217 | 0 | 0 |
| 40071 | Corso Moncalieri(TO) | positive | **si** | morto | 2217 | 0 | 0 |
| 40121 | Corso Regina Margherita(TO) | positive | **si** | morto | 2217 | 0 | 0 |
| 40123 | Corso Regina Margherita(TO) | positive | **si** | morto | 2217 | 0 | 0 |
| 5057 | SS30 Di Val Bormida | positive | no | morto | 2217 | 0 | 0 |
| 5058 | SS30 Di Val Bormida | negative | no | morto | 2217 | 0 | 0 |
| 7934 | SS142 Biellese | positive | no | morto | 2217 | 0 | 0 |
| 7935 | SS142 Biellese | negative | no | morto | 2217 | 0 | 0 |
| 11421 | SS458 Di Casalborgone | negative | no | pochi dati | 2217 | 8 | 7 |

### 7b — Script 33 v2 (misure diurne + esclusi)

Copia di sicurezza fatta in `scripts/33_flusso_sensori.py.bak_17ott`, poi il file è diventato la **v2**.
`python scripts\33_flusso_sensori.py --prova` e il giro completo girano senza errori (codice 0).
Output rigenerati: `data/processed/flusso_5t_sensori.json` e `docs/RAPPORTO_FLUSSO_5T_SENSORI.txt`.

Cosa fa la v2: i 17 esclusi restano nel file con `"escluso": "<motivo>"` e **nessun valore**; per gli altri
aggiunge, per ogni tipo di giorno: `f_diurno` (somma ore locali 6-21, solo se tutte e 16 sono ok),
`n_ore_diurne_ok`, `f_punta_am` (max ore 7-9), `f_punta_pm` (max ore 16-19), `quota_diurna`
(`f_diurno / totale_giorno`, dove esiste) e `totale_giorno_stimato` = `f_diurno / mediana(quota_diurna)`,
scritto come `{"valore": ..., "stimato": true}`.

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| (1) valori orari identici a prima, sensori non esclusi | nessuna differenza | **0 differenze su 92 sensori** | OK |
| (2) esclusi | 17 | **17** | OK |
| (3) valori negativi / oltre 6000 / massimo | 0 / 0 / ~3202 | **0 / 0 / 3202** | OK |
| (4) sensori con `f_diurno` | maggior parte dei 92 (se < 60: anomalia) | **91** | OK |

Altri numeri: celle orarie scritte 2132 (= 2252 − 120 delle celle dei 5 bloccati); sensori usabili 92;
sensori con `quota_diurna` **23**; sensori con la stima **91**; `quota_diurna` mediana **0,9125**,
minimo **0,6716**, massimo **0,9407**.

Scelta dichiarata (default): **l'ora 1 locale non viene riempita**, come chiede il piano. Nota: non è stata
azzerata nemmeno dove la cella era ok, perché il controllo (1) impone che i valori orari restino identici
a prima, e perché senza l'ora 1 nessun sensore avrebbe tutte e 24 le ore ok (quindi `totale_giorno` e
`quota_diurna` non sarebbero calcolabili). L'ora 1 resta comunque esclusa dalle misure diurne e dalle stime.

Anomalia minore: **1** sensore usabile su 92 non ha `f_diurno` (non ha tutte e 16 le ore diurne ok).

**PASSO 7: OK**

---

## PASSO 8: OK

Creato `scripts/36_abbinamento_posizione.py` (usa `normalizza` e `haversine_m` dello script 24, caricate
con `importlib`, come lo script 34). Output: `data/processed/sensori_corridoi_v2.json` e
`docs/RAPPORTO_ABBINAMENTO_POSIZIONE.txt`. Gira senza errori (codice 0).

Per ognuno dei **92** sensori usabili: i 3 corridoi più vicini entro 60 m, poi la classe:
**SICURO** (stesso nome, ≤ 60 m), **DA_VEDERE** (nome diverso, ≤ 40 m), **NESSUNO**.

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| SICURO | circa 14-15 (erano 15, meno gli esclusi) | **14** | OK |
| totale delle tre classi | 92 | **92** | OK |

Classi: **SICURO 14** (tutti urbani) · **DA_VEDERE 9** (8 urbani + 1 fuori città) · **NESSUNO 69**
(64 fuori città + 5 con "(TO)" nel nome ma che sono provinciali fuori dal taglio della rete OSM).
Nessun sensore NESSUNO ha corridoi fra 40 e 60 m: per tutti vale "niente entro le soglie".

I 14 SICURO (corridoio, punteggio, distanza in m): Corso Francia 40021 e 40022 → *Corso Francia (Collegno)*
p5, 4,9 e 16,8; Corso Giulio Cesare 40040 e 40041 → *Corso Giulio Cesare (Torino)* p4, 19,9 e 2,9;
Corso Orbassano 40095, 40097, 40098 → *Corso Orbassano* p4, 10,2 · 23,2 · 9,3; Corso Regina Margherita 40122
→ *Corso Regina Margherita (Torino)* p4, 3,9; Corso Trieste 40174 → *Corso Trieste (Moncalieri)* p4, 27,0;
Corso Unione Sovietica 40182 → *Corso Unione Sovietica (Torino)* p4, 0,8; Corso Unità d'Italia 40189 →
*Corso Unità d'Italia (Torino)* p4, 1,2; Strada di Settimo 40253 → *Strada di Settimo (Torino)* p4, 11,3;
Corso Sebastopoli 40149 → *Corso Sebastopoli (Torino)* p3, 11,3; Corso Vercelli 40194 → *Corso Vercelli (Torino)*
p3, 8,7. I 15° di prima era 40191, ora escluso come "bloccato".

**Tabella DA_VEDERE completa** (da far vedere a Claude — nel rapporto c'è la stessa tabella con i corridoi
vicini nel dettaglio):

| lcd1 | via del sensore | dir | corridoio proposto (nome diverso) | punteggio | distanza m |
|---|---|---|---|---|---|
| 40212 | Ponte Amedeo VIII(TO) | positive | Strada di Settimo (Torino) | 4 | 1,2 |
| 39977 | Corso Agnelli(TO) | positive | Corso Giovanni Agnelli (Torino) | 4 | 3,0 |
| 2375 | R24 Raccordo Torino-Aeroporto Caselle | negative | Raccordo Autostradale Torino-Caselle | 5 | 3,7 |
| 39983 | Corso Allamano(TO) | positive | Corso Canonico Giuseppe Allamano (Torino) | 4 | 4,8 |
| 35478 | SP1(TO) delle Valli di Lanzo | positive | Via Lanzo (Lanzo Torinese e limiti) | 3 | 21,5 |
| 35479 | SP1(TO) delle Valli di Lanzo | negative | Via Lanzo (Lanzo Torinese e limiti) | 3 | 21,5 |
| 36066 | SP8(TO) di Druento | positive | Via Torino (Druento) | 2 | 26,2 |
| 36067 | SP8(TO) di Druento | negative | Via Torino (Druento) | 2 | 26,2 |
| 35824 | SP2(TO) Di Germagnano | negative | Via Torino (San Maurizio Canavese) | 4 | 26,6 |

Coppie di versi (stesso nome, segno opposto, ≤ 200 m): **35**; sensori usabili **senza compagno**: **22**
(la lista è nel rapporto). Le 35 coppie coinvolgono 70 sensori, ognuno con un solo compagno.

**PASSO 8: OK**

---

## Situazione e file

Numeri chiave: esclusi **17** su 109 → usabili **92**; sensori con `f_diurno` **91**;
`quota_diurna` mediana **0,9125**; classi **SICURO 14 · DA_VEDERE 9 · NESSUNO 69**.

Serve ora la revisione di **Claude** sulla tabella DA_VEDERE: sceglie quali abbinamenti accettare e scrive
`data/processed/abbinamenti_confermati.json`. **Senza quel file non si fa il Passo 9** (metodi A e B).

File creati: `docs/ESITO_FASE2_TRAFFICO.md`, `scripts/35_sensori_esclusi.py`, `scripts/36_abbinamento_posizione.py`,
`scripts/33_flusso_sensori.py.bak_17ott`, `data/processed/sensori_esclusi.json`,
`data/processed/sensori_corridoi_v2.json`, `docs/RAPPORTO_SENSORI_ESCLUSI.txt`,
`docs/RAPPORTO_ABBINAMENTO_POSIZIONE.txt`.
File modificati: `scripts/33_flusso_sensori.py` (v2), `data/processed/flusso_5t_sensori.json`,
`docs/RAPPORTO_FLUSSO_5T_SENSORI.txt`.
`MEMORIA_PROGETTO.md` **non** è stato toccato.

---

# Seconda parte — Passi 8b, 8c, 9, 10 (17/10/2026, ore 01:45 → 02:20)

Eseguiti dopo la revisione di Claude (che ha scritto `data/processed/abbinamenti_confermati.json`).
Ramo `prova`, **nessun commit**, database in sola lettura, nessun file vietato toccato.

## PASSO 8b: OK

Creato `scripts/38_verifica_provinciali.py` → `docs/RAPPORTO_VERIFICA_PROVINCIALI.txt` e
`data/processed/abbinamenti_confermati_v2.json` (nuovo file: il vecchio non è stato sovrascritto).

Controllati con OSM (pyosmium su `data/otp/rete/torino_cintura.osm.pbf`) i 10 sensori:
i 5 in attesa (35478, 35479, 36066, 36067, 35824) e i 5 con "(TO)" nel nome ma NESSUNO (35518, 35519,
35559, 35560, 35823). Regola: `ref` OSM uguale a `SPn` del nome del sensore (spazi e maiuscole ignorati)
**e** nome della strada uguale al corridoio proposto, entro 60 m.

| lcd1 | sensore | esito | perché |
|---|---|---|---|
| 35478 | SP1(TO) delle Valli di Lanzo | **CONFERMATO** | `ref=SP1`, "Via Lanzo", 21,5 m = corridoio proposto |
| 35479 | SP1(TO) delle Valli di Lanzo | **CONFERMATO** | idem (stesso punto, verso opposto) |
| 36066 | SP8(TO) di Druento | **CONFERMATO** | `ref=SP8`, "Via Torino", 26,2 m = corridoio proposto |
| 36067 | SP8(TO) di Druento | **CONFERMATO** | idem |
| 35824 | SP2(TO) Di Germagnano | senza abbinamento | avrebbe `ref=SP2` a 26,6 m su "Via Torino", ma vedi nota |
| 35823 | SP2(TO) Di Germagnano | senza abbinamento | nessuna strada entro 60 m (il punto è 470 m più a nord) |
| 35518/35519 | SP122(TO) di Chieri | senza abbinamento | nessuna strada (ref `SP122` o no) entro 60 m; la più vicina è a 58,6 m senza nome |
| 35559/35560 | SP13(TO) di Front | senza abbinamento | nessuna strada entro 60 m |
| — | — | "strada senza nome nei corridoi": **0** | — |

Nota dichiarata sulla decisione presa (la sceglie Claude/Leo): il piano dice «se la coppia di versi ha
esiti diversi, tieni il più prudente per entrambi». Ho applicato la regola ai due sensori con lo stesso
nome e verso opposto (35823 e 35824, che sono i due versi della stessa provinciale): 35824 **sarebbe**
CONFERMATO (ref SP2 a 26,6 m su "Via Torino", che è il corridoio proposto), ma il compagno 35823, 470 m
più a nord, non ha nessuna strada entro 60 m (probabile bordo del ritaglio OSM), quindi ho lasciato
entrambi senza abbinamento. Se Claude preferisce limitare la regola alle coppie entro 200 m (la
definizione della decisione 5), 35824 torna confermato.

`abbinamenti_confermati_v2.json` = il file di Claude + i 4 nuovi confermati + `verifica_osm` per tutti e
10 i sensori. Totale abbinamenti utilizzabili dal Passo 9: 14 SICURO + 4 di Claude + 4 dall'8b = **22**.

## PASSO 8c: OK

Creato `scripts/38b_codici_condivisi.py` → `docs/RAPPORTO_CODICI_CONDIVISI.txt` (il numero 39 è riservato
alla Fase 3, quindi ho usato 38b). Non ho toccato lo script 03 né il database.

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| voci `FDT_data` nell'XML del 3/10 | 112 | **112** | OK |
| codici `lcd1` distinti | 109 | **109** | OK |
| codici con più di una voce | 40123, 40189, 13077 | **13077, 40123, 40189** | OK |
| righe di `flussi_5t` per `generato_utc` (per i 3 codici) | 1 | **1** (3353 istanti, 3353 righe) | OK |

Le due voci di ciascun codice condiviso (dal file XML):

| codice | voce | verso | offset | lat / lng | accuratezza |
|---|---|---|---|---|---|
| 40123 | 1ª | negative | 1555 | 45,093256 / 7,63375 | 0 (morto) |
| 40123 | 2ª | positive | 125 | 45,086797 / 7,653109 | 95 (vivo) |
| 40189 | 1ª | positive | 160 | 45,01876 / 7,66932 | 95 |
| 40189 | 2ª | positive | 970 | 45,02586 / 7,671667 | 80 |
| 13077 | 1ª | positive | 4960 | 44,64808 / 7,59853 | 0 |
| 13077 | 2ª | negative | 5150 | 44,65592 / 7,71134 | 0 |

Nel database `sensori_5t` per tutti e tre i codici c'è **la posizione della seconda voce** (l'ultima
arrivata): 40123 → offset 125 (il punto vivo), 40189 → offset 970, 13077 → offset 5150. Per 40189 le due
voci sono a circa **800 m** di distanza e il flusso può venire dalla prima mentre la posizione è della
seconda: per questo la sua posizione non è sicura (il piano lo dice già).

Marcatura: i tre codici sono segnati con `"codice_condiviso": true` (e `"posizione_sicura": false`) in
`data/processed/sensori_corridoi_v2.json` e da lì nel file del Passo 9. 40123 era ed è escluso (morto);
40189 è usabile ma **non** come fonte del metodo B; 13077 non era escluso e resta fra i 92 (comunque non
ha nessun corridoio abbinato, quindi non entra nei conti del Passo 9).

## PASSO 9: OK

Creato `scripts/37_traffico_AB.py` → `data/processed/traffico_stimato_AB.json` e
`docs/RAPPORTO_TRAFFICO_AB.txt`. Unità di calcolo = sensore o coppia di versi sommata, abbinata a un
corridoio SICURO o confermato: **22 sensori → 20 unità** (2 coppie di versi sommate + 18 sensori di un
solo verso, per i quali il totale a due versi è `f_diurno × 2` con `un_verso: true, stimato: true`).
Corridoi con un valore: **15** (tutti misurati da un sensore). L'ora di punta resta per verso, non si
moltiplica.

**Metodo A** — gruppi (punteggio × dentro/fuori Torino), su `f_diurno_totale` (veicoli/giorno):

| gruppo | n | stimabile | mediana | p10 | p90 |
|---|---|---|---|---|---|
| p2_dentro | 1 | no | 20.889 | — | — |
| p3_dentro | 3 | sì | 17.342 | 16.177 | 24.464 |
| p4_dentro | 13 | sì | 28.846 | 17.324 | 65.348 |
| p5_dentro | 2 | no | 29.816 | 28.922 | 30.710 |
| p5_fuori | 1 | no | 40.092 | — | — |

**Prova "nascondi un sensore" (A)** — errore = |mediana del gruppo senza quel sensore − misurato| / misurato:

| gruppo | n | errore mediano | 90° | peggiore | distorsione media (segno) |
|---|---|---|---|---|---|
| p3_dentro | 3 | 36,7% | 37,1% | 37,2% | +7,3% |
| p4_dentro | 13 | 39,2% | 72,1% | 132,5% | +7,3% |
| **TOTALE** | **16** | **36,9%** | **69,3%** | **132,5%** | **+7,3%** |

4 unità su 20 non sono valutabili perché il loro gruppo ha meno di 3 unità (p2_dentro, p5_dentro,
p5_fuori). L'errore è grande, come il piano prevedeva: **non l'ho aggiustato**. Peggiore caso: 39983
(Corso Allamano, misurato 12.636 veic/giorno, previsione 29.381 → +132,5%).

**Metodo B** — due letture, entrambe riportate:
1. estensione dentro il corridoio del sensore: le parti entro 1 km dal sensore sono **70,9 km su 207,7 km**
   (34,1%) dei 15 corridoi con sensore (1 km in linea d'aria: approssimazione dichiarata);
2. estensione ad **altri** corridoi con lo stesso nome entro 1 km: **0 casi** (i 107 corridoi con lo stesso
   nome di una via con sensore sono tutti oltre 1 km: il limite di 1 km non copre niente).

**Prova per B** (corridoi con almeno 2 sensori, stesso verso): **6 casi** → valutabile.

| corridoio | a | b | distanza m | f_diurno a | f_diurno b | rapporto | errore |
|---|---|---|---|---|---|---|---|
| Corso Francia (Collegno) | 40021 | 40022 | 245,6 | 14.349 | 15.467 | 0,93 | 7,2% |
| Corso Orbassano | 40097 | 40098 | 411,3 | 20.673 | 13.631 | 1,52 | 51,7% |
| Strada di Settimo (Torino) | 40212 | 40253 | 956,2 | 14.958 | 8.444 | 1,77 | 77,1% |
| Corso Giulio Cesare (Torino) | 40040 | 40041 | 1230,4 | 16.964 | 14.423 | 1,18 | 17,6% |
| Corso Orbassano | 40095 | 40097 | 1288,5 | 25.102 | 20.673 | 1,21 | 21,4% |
| Corso Orbassano | 40095 | 40098 | 1696,8 | 25.102 | 13.631 | 1,84 | 84,2% |

Lettura (senza "migliorare" niente): due sensori sulla **stessa** strada e nello **stesso** verso, a
poche centinaia di metri, possono avere flussi che differiscono del 50-84%: il traffico **cambia molto
lungo la strada**, quindi estendere un valore per 1 km è già rischioso. Questo è un risultato.

Controlli: nessun sensore usato per predire sé stesso; nessun valore senza etichetta di metodo; tutti i
10429 corridoi senza stima sono elencati nel JSON con il motivo (10.314 "nessun sensore su questa strada",
107 "stessa strada di un corridoio con sensore ma oltre 1 km", 8 "nome uguale a una via con sensore ma
nessun corridoio abbinato").

## PASSO 10 — Chiusura

Numeri chiave della seconda parte: abbinamenti usabili **22 sensori / 20 unità**; corridoi con un valore
**15** (0 estesi da B da altri corridoi); prova A su **16** unità con errore mediano **36,9%** (p90 69,3%,
peggiore 132,5%, distorsione +7,3%); prova B **6 casi**, errori **7,2% → 84,2%**; corridoi senza stima
**10.429**.

Anomalie / cose da decidere:
1. 35824 "SP2(TO) Di Germagnano": vedi la nota del Passo 8b (compagno di verso senza strada OSM entro
   60 m; esito allineato per prudenza). Decisione di Claude/Leo.
2. Il limite di 1 km del metodo B non copre nessun corridoio (tutti gli omonimi sono oltre 1 km).
3. Il metodo A è impreciso (errore mediano 36,9%): atteso dal piano, è il motivo per cui serve il C.
4. 13077 (codice condiviso) resta fra i 92 usabili secondo il piano, ma non ha corridoio abbinato.
5. Eccezione dichiarata alla regola della sezione 2: il Passo 8b chiede pyosmium e l'ho usato (già
   installato); nessuna installazione è stata fatta.

File creati in questa seconda parte: `scripts/38_verifica_provinciali.py`,
`scripts/38b_codici_condivisi.py`, `scripts/37_traffico_AB.py`,
`data/processed/abbinamenti_confermati_v2.json`, `data/processed/traffico_stimato_AB.json`,
`docs/RAPPORTO_VERIFICA_PROVINCIALI.txt`, `docs/RAPPORTO_CODICI_CONDIVISI.txt`,
`docs/RAPPORTO_TRAFFICO_AB.txt`.
File modificati: `data/processed/sensori_corridoi_v2.json` (marcatura `codice_condiviso`),
`docs/ESITO_FASE2_TRAFFICO.md`.
