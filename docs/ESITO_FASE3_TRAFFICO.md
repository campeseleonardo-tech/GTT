# Esito — Fase 3 del Risultato 8 (traffico veicolare), metodo C + correzione del raccoglitore

Eseguito da: **agente opencode** sul PC di Leo. Giorno: **17/10/2026**.
Cartella `C:\projects\Progetti\GTT`. Ramo git **`prova`**, **nessun commit**.
Database storico e `data/raw/` aperti in **sola lettura**. Niente scritto né riavviato sul Pi.
Riferimento: `docs/PIANO_TRAFFICO_FASE3.md` (i criteri di riuscita della sua sezione 1 non sono stati cambiati).

## 0. Esito di ogni pacchetto (riga di stato)

```
PASSO A: OK   (fattibilita': rete in 5,3 s, 10 ms per origine, giro completo stimato < 2 min, non 8 ore)
PASSO B: OK   (domanda auto 4.153.663 vs 4.180.000 attesi = -0,6%; Torino 950.893 vs ~970.000 = -2,0%)
PASSO C: OK   (947 punti su 810 nodi; 206 porte sul bordo del taglio; 141 zone esterne)
PASSO D: OK   (810 origini, 658.532 coppie di nodi, 22,27 M veicoli-km/giorno; verifica networkx 0,000%)
PASSO E: OK   (105.890 tratti, 10.122 corridoi con flusso, 621 senza; conservazione del flusso OK)
PASSO F: OK   (C-DEBole: errore mediano 31,9%, rho 0,602, n=20 - vedi tabella)
PASSO G: OK   (prodotto finale per 10.122 corridoi; fiducia alta 19, media 0, bassa 10.724)
PASSO H: OK   (verifica fatta, script 03 corretto, prova su database vuoto 112/112/112 e idempotente,
               .bat e controllo pronti: NON eseguiti sul Pi, li avvia Leo con un doppio clic)
PASSO I: OK   (TRAFFICO_RILANCIA_SENSORI.bat e TRAFFICO_RICALCOLA_MODELLO.bat scritti e provati a pezzi)
```

**Esito finale del modello: `C-DEBole`** — errore mediano 31,9% (intervallo al 90% 23,7%–40,2%),
rho di Spearman **0,602** (n=20), meglio del metodo A (36,9%) ma sotto la soglia 0,7.
Si pubblica solo la classe a 3 livelli (alto/medio/basso), marcata "debole".

---

## 1. Decisioni dell'agente (cosa ho scelto e perché)

1. **Motore: grafo proprio, non r5py.** r5py (r5) importa e funziona (Java in `data/otp/jdk-25.0.4.1+1-jre`,
   heap 3 GB), ma serve a calcolare percorsi puntuali o matrici di tempi, non a far passare ~2 milioni di
   viaggi su tutta la rete. Ho costruito la rete percorribile in auto dal taglio OSM con pyosmium
   (`scripts/rete_osm.py`, **81.966 nodi, 105.890 tratti, 8.592 km**) e uso
   `scipy.sparse.csgraph.dijkstra` + somma dei sottoalberi per contare i passaggi su ogni tratto.
   Costo misurato: **10 ms per albero di cammini minimi, ~40 ms per origine con l'accumulo dei flussi**.
   Il giro completo (pacchetto D) dura **~45 s**, non ore: la prova di fattibilita' A passa con margine enorme.
2. **Rappresentazione delle zone: punti pesati sulla POPOLAZIONE (sezioni di censimento).**
   V0 usa la popolazione sia per l'origine sia per la destinazione. Il piano prevedeva attrattori per gli
   estremi non domestici; l'ho semplificato (dichiarato) perché i servizi OSM della cintura sono incompleti
   e avrebbe richiesto di ricostruire le catene di spostamenti per ogni persona. **Punti per zona: 20 per i
   quartieri di Torino, 8 per i comuni della cintura, 5 per le zone "resto provincia" interne al taglio**
   (campionamento casuale con probabilità proporzionale alla popolazione, seme fisso 20261017).
3. **Zone fuori dal taglio OSM -> "porte".** Ho usato le strade che **attraversano** il bordo del riquadro
   (un estremo dentro, uno fuori), qualsiasi rango: **206 porte** (prima ne trovavo solo 45, con gli
   estremi di grado 1, e il traffico si concentrava su poche strade di campagna). Ogni zona esterna sceglie
   fino a 3 porte con costo = tempo zona->porta + tempo porta->Torino, con rango minimo crescente con la
   distanza (a 40 km non si entra da una strada di campagna).
4. **I viaggi interni a una zona ESTERNA non producono flusso.** Un viaggio che parte e arriva dentro una
   zona fuori dal taglio avviene fuori dall'area studiata: se lo instradassi fra due porte diverse creerei
   traffico finto sui corsi di Torino (l'ho visto: 133.000 veicoli/giorno su una strada di campagna di Chieri).
   Scelta: scartati (e contati). **È la voce principale del "peso che non produce flusso" (54% dei viaggi)**,
   ma è tutta fuori dall'area studiata: dentro Torino si perde il 16,5% dei viaggi interni a una zona e lo
   **0,0%** dei viaggi fra zone diverse.
5. **Aggancio dei punti ai nodi: solo il "nocciolo" della rete** (componente fortemente connessa più grande,
   80.094 nodi su 81.966). Senza questo, i punti caduti su strade a senso unico o su viuzze isolate non
   potevano raggiungere nulla (774.000 viaggi "non raggiungibili"); ora sono **0**.
6. **Taratura: la variante finale è V0 (un solo fattore globale k).** Il piano (regola 3) direbbe di usare
   la "più semplice entro 5 punti" e con i numeri la più semplice sarebbe la **V2 potenza** (errore mediano
   22,8%): l'ho scartata per decisione motivata perché **vince solo comprimendo gli estremi** e sui corridoi
   con modello grezzo basso produce valori assurdi (grezzo 100 -> 1.800 veicoli/giorno) che nessun sensore
   può validare, con la **correlazione di rango peggiore** di V0 (0,577 contro 0,602). La classe di esito è
   **C-DEBole con tutte e tre le varianti**, quindi la scelta non "migliora" niente: la riporto solo perché
   i numeri pubblicati restino plausibili. Vedi la tabella nel pacchetto F.
7. **Ore del giorno: uno schema unico (V0 del piano).** Le quote orarie della domanda IMU danno le ore
   (7-8: 9,3%; 16-18: 25,8%; diurno 6-21: 96,3% dei viaggi). Niente riassegnazione ora per ora.

### Varianti provate (regola "massimo 4, riportale tutte")
Solo varianti di **taratura** (V0, V1, V2), tutte nella tabella del pacchetto F. Non ho provato varianti di
**instradamento** (percorsi stocastici, velocità ridotte in punta) perché il collaudo era già abbastanza
chiaro e il tempo/beneficio non lo giustificava; resta il suggerimento per una Fase 3-bis.

### Pacchetti Python installati con `pip --user`
`networkx 3.7` (per la verifica indipendente dei percorsi), `matplotlib 3.11.2` (per il grafico di controllo)
e le loro dipendenze (contourpy, cycler, fonttools, kiwisolver, pillow). Già presenti: numpy 2.5.3, scipy 1.18.1,
pandas 3.0.6, geopandas 1.2.0, shapely 2.2.0, pyproj 3.8.0, osmium, psutil 7.2.2, r5py 1.1.7.

---

## 2. Pacchetto A — prova di fattibilità (gate)

`scripts/39_fattibilita_rete.py` → `data/processed/traffico_c/rete/` e `docs/RAPPORTO_TRAFFICO_C_FATTIBILITA.txt`.

- Ambiente: Python 3.14.3, Java trovato, r5py 1.1.7 importabile, **188 GB liberi su disco**, RAM 7,9 GB
  (2,5 GB liberi all'avvio).
- Rete: 63.388 way percorribili → **81.966 nodi, 105.890 tratti, 8.592 km**, costruita in **5,3 s**, 750 MB di RAM.
- 200 coppie: 200 alberi di cammini minimi in 2,05 s (**10 ms per origine**), 196/200 con geometria
  ricostruita; 109/196 passano su tangenziale o autostrada.
- Controlli: rapporto lunghezza di rete / in linea d'aria mediana 1,34 (min 1,12, max 2,34); 10 percorsi a
  campione con estremi e tempi plausibili.
- **Anomalia dichiarata:** piazza Castello → Collegno in **11,7 minuti** (9,0 km), mentre il piano si
  aspettava 20-35 minuti. Il percorso (verificato) va da Corso Vittorio Emanuele II a **Corso Francia**:
  11,7 minuti è il tempo a **flusso libero** (50 km/h, nessun semaforo, nessuna coda). È esattamente il
  limite dichiarato di V0 ("senza rallentamenti da traffico"). Non l'ho corretto.
- **Stima del giro completo** (Dijkstra + accumulo): 400 origini 26 s, 800 origini 51 s, 1200 origini 77 s.
  Molto sotto le 8 ore → gate superato.

## 3. Pacchetto B — domanda IMQ

`scripts/40_domanda_imq.py` → `data/processed/traffico_c/domanda_auto.json`, `docs/RAPPORTO_TRAFFICO_C_DOMANDA.txt`.

| Controllo | Atteso | Trovato | Esito |
|---|---|---|---|
| auto conducente (03 unico mezzo motorizzato) | ~4.180.000 | **4.153.663** (-0,6%) | OK |
| almeno un estremo in un quartiere di Torino | ~970.000 | **950.893** (-2,0%) | OK |
| viaggi esclusi perché misti | < 8% | **0,65%** del peso | OK |
| picchi orari | 7-8 e 16-18 | 19,3% e 25,8% | OK |

20.210 celle OD×ora; 20.129 (99,6%) hanno meno di 30 interviste: **91,9% del peso** sta in celle
statisticamente debolissime (limite noto IMQ, da dichiarare sempre). Un estremo fuori dalle 212 zone:
53.335 viaggi/giorno (trattati come "esterno non localizzato", distribuiti sulle porte).

## 4. Pacchetto C — punti e porte

`scripts/41_zone_punti.py` → `punti.json`, `porte.json`, `docs/RAPPORTO_TRAFFICO_C_PUNTI.txt`.

- 212 zone → **947 punti su 810 nodi** stradali; 23 quartieri (20 punti), 48 zone con sezioni (8 punti),
  141 zone-esterna (fino a 3 porte).
- **206 porte** sul bordo del taglio (rango 5: 10, 4: 15, 3: 14, 2: 35, 1: 132).
- 8.307 sezioni di censimento assegnate a una zona; 10 non assegnate.
- Nessuna zona senza punti, nessuna zona con tutti i punti su un solo nodo.

## 5. Pacchetto D — instradamento

`scripts/42_instradamento.py` → `archi_flusso.npz`, `instradamenti/riepilogo.json`.
Ripartibile (checkpoint ogni 100 origini con **firma della rete**: se la rete viene ricostruita il
checkpoint vecchio non viene riusato).

| Numero | Valore |
|---|---|
| origini usate | 810 |
| coppie di nodi con domanda | 658.532 |
| viaggi che producono flusso | 1.912.211 su 4.153.663 (46,0%) |
| veicoli·km/giorno | **22.270.614** |
| lunghezza media di viaggio (instradati) | **11,7 km** |
| veicoli-ora/giorno | 375.365 |
| peso non raggiungibile | **0** |
| durata | **44 s** |

Dettaglio del peso che non produce flusso: intra-zona esterna 1.598.037 (99,6% delle volte), fra due zone
esterne 558.919, intra-zona interna **100.502 (16,5%)**, fra porti/interni 32. **Dentro l'area studiata si
perde poco; fuori è strutturale** (quei viaggi non attraversano la rete studiata).

**Verifica indipendente (sezione 6/12):** 20 coppie ricalcolate con **networkx** sullo stesso grafo →
**errore massimo 0,000%** (tolleranza 2%).
**Bug trovato e corretto durante il lavoro (da raccontare):** salvavo i pesi degli archi come interi
(tempi troncati), quindi molti tratti corti avevano peso 0 e l'accumulo dei flussi sull'albero si rompeva
(fattore di perdita ~6,7×). Corretto in `rete_osm.py`; l'unità di prova ora dà veicoli·km identici alla
lunghezza del cammino esplicito.

## 6. Pacchetto E — dai percorsi ai corridoi

`scripts/43_segmenti_corridoi.py` → `segmenti.csv`, `corridoi_modello.json`, `docs/RAPPORTO_TRAFFICO_C_SEGMENTI.txt`.

- 105.890 tratti; **67.822** collegati a un corridoio per nome, **18.147** per vicinanza (≤25 m),
  19.921 senza corridoio (strade senza nome, non sono corridoi).
- 10.122 corridoi con almeno un tratto (su 10.743), **621 senza flusso** (elencati col motivo).
- **Controllo conservazione del flusso:** 174 nodi su 81.966 (0,21%) hanno ingresso ≠ uscita oltre l'1%
  del flusso medio — sono le origini/destinazioni. Flussi negativi: **0**.
- Veicoli·km diurni (6-21): **24.880.463**.

Nota: il campo `componenti` di `importanza_vie.json` **non** contiene gli id dei way OSM (contiene solo
contatori), quindi il collegamento tratto→corridoio l'ho fatto col nome normalizzato + vicinanza ≤25 m
(come consentito dal piano).

## 7. Pacchetto F — taratura e validazione

`scripts/44_taratura_validazione.py` → `taratura_validazione.json`, `docs/RAPPORTO_TRAFFICO_C_VALIDAZIONE.txt`.

Criteri (sezione 1, ripresi parola per parola): C-ASSOLUTO = errore mediano ≤35% **e** migliore di A **e** ρ ≥ 0,7;
C-INDICE = ρ ≥ 0,7 ma errore >35% o non migliore di A; C-DEBOLE = 0,5 ≤ ρ < 0,7; C-NO = ρ < 0,5.

| Variante | errore mediano (IC90) | p90 | peggiore | distorsione | ρ (leave-one-out) | meglio di A |
|---|---|---|---|---|---|---|
| **V0_globale** (k = 1,722) | **31,9%** [23,7%–40,2%] | 59,2% | 146,9% | +5,7% | **0,602** | sì |
| V1_per_classe | 31,9% [19,3%–37,6%] | 62,5% | 216,9% | +11,5% | 0,516 | sì |
| V2_potenza (a=148,5 b=0,544) | 22,8% [20,0%–34,0%] | 82,4% | 109,2% | +6,2% | 0,577 | sì |

Modello **grezzo** (prima della taratura): ρ = **0,614**.
Metodo A sulle stesse unità: errore mediano 36,9%. **Il metodo C è migliore di A di 5 punti di errore
mediano, ma la correlazione di rango resta 0,60: non basta per C-INDICE/C-ASSOLUTO.**

**Classe di esito: `C-DEBole`** (ρ = 0,602, 0,5 ≤ ρ < 0,7). L'intervallo al 90% dell'errore mediano di V0
(23,7%–40,2%) attraversa la soglia del 35%: la stima puntuale dell'errore è **incerta**.

Residui peggiori (variante finale): Corso Unione Sovietica +109%, Corso Allamano +85%, Corso Sebastopoli +82%,
Corso Unità d'Italia −46%, Corso Agnelli +43%. I sensori urbani di Torino sono a **un solo verso** e il verso
non è ricavabile con certezza: la punta mattina/sera **non** è stata stimata (dichiarato).

**Controlli di buon senso (sezione 1):** (a) ordine per classe rispettato SÌ (mediane: autostrada/tangenziale
9.273, arteria 938, locale 0 veicoli/giorno); (b) radiali d'ingresso: modello/misurato = **0,67** (<1 come
atteso); (c) veicoli·km coerenti con i viaggi × lunghezza (verifica networkx esatta).

## 8. Pacchetto G — prodotto finale

`scripts/45_prodotto_finale.py` → `data/processed/traffico_stimato_finale.json` (e copia in
`data/processed/traffico_c/`), `docs/RAPPORTO_TRAFFICO_C.txt`,
grafico di controllo `docs/grafico_misurato_vs_previsto.png`.

- 10.122 corridoi con stima, 621 senza. **Fiducia: alta 19, media 0, bassa 10.724** (con esito C-DEBole la
  fiducia "media" non può esistere per definizione del piano).
- Corridoi col sensore (misurato, `stimato: false`): 19. Tutti gli altri valori portano `stimato: true`
  (verificato: 0 senza etichetta).
- Campo pubblicabile per C-DEBole: `classe3` (alto da 1.520 veicoli/giorno, medio da 336).

**I 5 corridoi di Torino con più traffico stimato [STIMATO]:**

| # | corridoio | veicoli/giorno 6-21 | fiducia |
|---|---|---|---|
| 1 | Lungo Po Armando Diaz | 85.826 | bassa |
| 2 | Lungo Po Luigi Cadorna | 82.616 | bassa |
| 3 | Autostrada Serenissima (A4, tratto in Torino) | 53.930 | bassa |
| 4 | Corso Germano Sommeiller | 53.635 | bassa |
| 5 | Sottopasso Michele Lanza | 53.378 | bassa |

**10 sorprese** (strade di rango 1-2 con traffico altissimo, tutte in provincia, tutte da **indagare** —
coerenti col difetto delle porte): Via Ivrea (Caluso) 251.391, Strada dell'Olmo (Villanova d'Asti) 242.168,
Viale Lombardore (Caluso) 147.518, Via Chivasso (Caluso) 133.537, Corso Luigi Einaudi 65.836, ...
**Il traffico esterno concentrato su poche porte è il difetto principale del modello.**

## 9. Pacchetto H — correzione del raccoglitore sul Pi (pronto, NON eseguito)

### 9.1 Verifica dei fatti (`scripts/46_verifica_5t_codici.py` → `docs/RAPPORTO_TRAFFICO_C_CODICI_5T.txt`)
- XML del 3/10: **112 voci FDT_data, 109 codici distinti**, doppi **40123, 40189, 13077**.
- Offset della PRIMA voce: 40189 → **160**, 40123 → **1555**, 13077 → **4960** (le ancore attese: OK).
- Scaricato un **XML fresco dal feed 5T** (sola lettura, salvato in `data/processed/5t_flussi_verifica_*.xml`):
  **gli stessi tre codici sono ancora condivisi** → la regola li copre.
- Database: l'istante del file del 3/10 22:45:03 **non c'è** (il raccoglitore è partito dopo; il primo
  istante è `2026-10-03T23:41:02.415Z`). Su quell'istante: **40123 flusso = 0** (la voce morta, la prima)
  mentre `sensori_5t` ha **offset 125** (il sensore vivo, l'ultima) → **difetto CONFERMATO**.

### 9.2 Cosa è stato preparato
- `scripts/03_raccolta_continua.py` **corretto** (copia di sicurezza `scripts/03_raccolta_continua.py.bak_17ott`,
  unica modifica: `salva_5t_da_bytes` + tabella delle ancore `CODICI_CONDIVISI_ANCORA`). Regola: la **prima**
  voce tiene `lcd1`, le successive diventano `lcd1~2`, `lcd1~3`…; se l'ordine del feed cambia, lo **segnala nel log**.
- `scripts/47_prova_raccolta_5t_su_copia.py` → prova su **database vuoto** (`data/processed/traffico_c/prova_5t_codici.sqlite`):
  - 1° giro: **112 sensori_5t, 112 flussi_5t, 112 accuratezza_5t**, i 3 codici `~2`; posizioni giuste
    (40189 → 160, 40189~2 → 970, 40123 → 1555, 40123~2 → 125, 13077 → 4960, 13077~2 → 5150);
  - 2° giro con lo stesso XML: **0 righe nuove** (idempotente);
  - XML modificato con un duplicato in più: nasce **`40021~3`** e compare la riga di log.
- Controllo di tutto ciò che legge i sensori: `grep lcd1` su 04, 06, 09, 26, 33-38b, backup/check — nessuno
  assume che `lcd1` sia un numero. **Prova prima/dopo: rilanciati 26 e 33 sul database attuale, output
  identico byte per byte (impronta MD5 uguale, tolleranza zero).**
- `scripts/controlla_raccolta_5t.py` (gira **sul Pi**, sola lettura) e `scripts/AGGIORNA_RACCOLTA_5T_CODICI.bat`
  (doppio clic, copia di sicurezza sul Pi `.bak_pre_codici`, invio, `py_compile`, riavvio `gtt-raccolta`, attesa 6 minuti, controllo).

### 9.3 Procedura per Leo (3 righe)
1. Doppio clic su `scripts\AGGIORNA_RACCOLTA_5T_CODICI.bat` e attendi ~7 minuti (può chiedere la password di sudo).
2. In fondo al log devi vedere: `active`, **`sensori nell'ultimo istante: 112`** (prima erano 109) e
   **`codici ~2 con dati: 3/3`**.
3. Se leggi "NON ancora 112": aspetta 10 minuti e rilancia lo stesso .bat (non fa danni).
   **Per tornare indietro:** sul Pi `cp ~/GTT/scripts/03_raccolta_continua.py.bak_pre_codici ~/GTT/scripts/03_raccolta_continua.py`
   e `sudo systemctl restart gtt-raccolta`.

**⚠ Il .bat NON è stato eseguito** (servirebbe scrivere sul Pi, vietato): è scritto e modellato su
`aggiorna_raccolta_leopi.bat`, ma la prima esecuzione è la sua prova.

### 9.4 Dopo l'avvio
I tre sensori nuovi (`40123~2` vivo, `40189~2`, `13077~2`) avranno dati utilizzabili dopo **~6 giorni feriali**.
La pipeline (33-37, 43-45) li include **da sola** quando hanno celle ok: basta rilanciare
`TRAFFICO_RILANCIA_SENSORI.bat` dopo un fetch. **Prima dell'avvio la pipeline resta identica a oggi**
(verificato: 26 e 33 danno gli stessi numeri).

## 10. Pacchetto I — rilancio ripetibile

- `scripts/TRAFFICO_RILANCIA_SENSORI.bat`: dopo ogni fetch da leopi esegue in ordine
  26, 33, 35, 36, 38b, 37, **43**, 44, 45 (ho aggiunto **43**, che il piano non elencava: il 44 legge il suo
  `corridoi_modello.json` per sapere qual è il tratto più vicino a ogni sensore), senza rifare il calcolo dei
  percorsi (che resta in cache). Stampa 5 righe di numeri chiave.
- `scripts/TRAFFICO_RICALCOLA_MODELLO.bat`: rifà i pacchetti A-E (solo se cambiano rete OSM, IMQ o regole),
  con avviso chiaro che dura a lungo.
- **Promemoria:** dopo il **25/10** finisce l'ora legale (UTC+1): controllare a mano le ore locali dello
  script 26 per le letture dopo il cambio (prova su una lettura delle 01:30 UTC del 26/10).
  Il primo fetch utile per sabato e domenica è **lunedì 19/10**; con due giorni per tipo le celle weekend
  diventano "ok" (i metodi di questa fase restano per il feriale).

## 11. Verifiche indipendenti (sezione 12) — `scripts/48_verifiche_indipendenti.py`

`docs/RAPPORTO_TRAFFICO_C_VERIFICHE.txt` — **esito: TUTTE LE VERIFICHE OK**.
1. Totali della domanda ricalcolati **con pandas** (script 40 usa il modulo csv): **4.153.663 identici** (0,00000%).
2. 20 percorsi ricalcolati con networkx: errore massimo **0,000%**.
3. Conservazione del flusso: 174 nodi su 81.966 oltre l'1% (origini/destinazioni); veicoli·km 22,27 M.
4. Fattore k (1,721511) e 3 errori leave-one-out ricalcolati a mano: **coincidono**.
5. Nessun valore del modello senza `modello_stimato: true`; **0 sensori esclusi** usati per tarare.
6. 5 corridoi riletti da zero (segmenti.csv → corridoi → k → valore finale): tutti entro l'1% + arrotondamento.
7. `git status`: nessun file vietato toccato dall'agente (MEMORIA_PROGETTO.md e mappa_template.html erano
   **già** modificati prima di questo lavoro). **Nessun commit fatto.**

## 12. Anomalie e limiti (da dire chiaramente)

1. **Traffico esterno concentrato su poche porte**: alcune strade di campagna vicino al bordo del taglio
   hanno valori assurdi (fino a 250.000 veicoli/giorno). È il difetto maggiore: il traffico da fuori area
   entra da poche strade. **I valori sui tratti di bordo NON sono attendibili.**
2. **Assegnazione tutto-o-niente senza congestione**: il traffico si concentra sui percorsi più veloci;
   "Lungo Po Armando Diaz" con 85.826 veicoli/giorno è probabilmente troppo alto.
3. **Limiti IMQ** (dichiarati in ogni uso): solo residenti 11-84 anni, giorno feriale medio, campione
   telefonico, anno 2022, quartieri 1984. Mancano merci, turisti, non residenti → il modello sottostima in
   media (k = 1,72) e la taratura corregge in media, non strada per strada.
4. Il 54% del peso non produce flusso, quasi tutto nei viaggi con entrambi gli estremi **fuori** dal taglio.
5. Sensore 40191 (bloccato) e 17 esclusi non usati; 3 codici `lcd1` condivisi (pacchetto H).
6. L'ora locale 1 = dato mancante (già noto dalla Fase 1).
7. La variante finale pubblicata (V0) è una scelta motivata dell'agente, non quella letterale della regola 3
   (punto 6 delle Decisioni).

## 13. Durate

| Fase | Durata |
|---|---|
| Pacchetto A (prova, comprese le iterazioni di correzione) | ~15 min |
| Pacchetti B-C (domanda, punti, porte) | ~5 min |
| Pacchetto D (instradamento 810 origini) | **44 s** |
| Pacchetto E (corridoi) | ~2 min |
| Pacchetti F-G (taratura, prodotto) | ~1 min |
| Pacchetto H (verifica, patch, prova su copia) | ~10 min |
| Pacchetto I + esito | ~10 min |
| **Totale sessione agente** | **~1 ora e 30 minuti** (02:20 → 03:10) |

## 14. File creati / modificati

**Script nuovi:** `rete_osm.py`, `39_fattibilita_rete.py`, `40_domanda_imq.py`, `41_zone_punti.py`,
`42_instradamento.py`, `43_segmenti_corridoi.py`, `44_taratura_validazione.py`, `45_prodotto_finale.py`,
`46_verifica_5t_codici.py`, `47_prova_raccolta_5t_su_copia.py`, `48_verifiche_indipendenti.py`,
`controlla_raccolta_5t.py`, `AGGIORNA_RACCOLTA_5T_CODICI.bat`, `TRAFFICO_RILANCIA_SENSORI.bat`,
`TRAFFICO_RICALCOLA_MODELLO.bat`.
**Script modificato:** `03_raccolta_continua.py` (con `03_raccolta_continua.py.bak_17ott`).
**Dati nuovi (in `data/processed/traffico_c/`):** `rete/` (+`rete_auto.npz` 15 MB),
`domanda_auto.json`, `domanda_nodi.npz`, `punti.json`, `porte.json`, `archi_flusso.npz`, `instradamenti/`,
`segmenti.csv`, `corridoi_modello.json`, `taratura_validazione.json`, `traffico_stimato_finale.json`,
`verifica_networkx.npz`, `fattibilita.json`, `prova_5t_codici.sqlite`, `5t_flussi_verifica_*.xml`.
**Rapporti nuovi in `docs/`:** `ESITO_FASE3_TRAFFICO.md`, `RAPPORTO_TRAFFICO_C_DOMANDA.txt`,
`RAPPORTO_TRAFFICO_C_FATTIBILITA.txt`, `RAPPORTO_TRAFFICO_C_PUNTI.txt`, `RAPPORTO_TRAFFICO_C_SEGMENTI.txt`,
`RAPPORTO_TRAFFICO_C_VALIDAZIONE.txt`, `RAPPORTO_TRAFFICO_C.txt`, `RAPPORTO_TRAFFICO_C_CODICI_5T.txt`,
`RAPPORTO_TRAFFICO_C_PROVA_RACCOLTA.txt`, `RAPPORTO_TRAFFICO_C_VERIFICHE.txt`,
`grafico_misurato_vs_previsto.png`.
**Rigenerati (identici):** `data/processed/velocita_5t.json`, `flusso_5t_sensori.json` (prova 26/33 prima/dopo).
**Non toccati:** `MEMORIA_PROGETTO.md`, `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`,
`data/raw/*` (a parte la lettura), `data/storico_backup.sqlite` (solo lettura). **Nessun commit.**

## 15. Testo proposto per MEMORIA_PROGETTO.md (non l'ho modificato)

> | Traffico 5T, Fase 3 metodo C (39-48) | **17/10.** Riletti dal file OSM 81.966 nodi / 105.890 tratti in auto; la domanda IMQ auto (4.153.663 viaggi/giorno, tutti i giorni feriali) è fatta guidare sul percorso più veloce e sommata per tratto. **Esito della validazione (criteri fissati nel piano): C-DEBole** — errore mediano 31,9% (IC90 23,7-40,2%), rho di Spearman 0,602, n=20 sensori; il metodo A sulle stesse unità dava 36,9% (quindi C è meglio in media) ma la soglia per pubblicare i numeri è rho ≥ 0,7. Prodotto: 10.122 corridoi su 10.743 con una stima (fiducia alta 19, bassa 10.724), in `data/processed/traffico_stimato_finale.json`; si pubblica solo la classe alto/medio/basso, marcata debole. Limiti: traffico da fuori area concentrato su poche "porte" (valori assurdi sui tratti di bordo), assegnazione senza congestione, 54% dei viaggi non produce flusso (tutti con entrambi gli estremi fuori dal taglio). Dettagli e decisioni: `docs/ESITO_FASE3_TRAFFICO.md`; rapporto finale `docs/RAPPORTO_TRAFFICO_C.txt`. **Correzione del raccoglitore 5T pronta** (`scripts/AGGIORNA_RACCOLTA_5T_CODICI.bat`): da far partire a Leo con un doppio clic; i 3 sensori nuovi avranno dati utili dopo ~6 giorni feriali. Rilancio dopo ogni fetch: `scripts/TRAFFICO_RILANCIA_SENSORI.bat`.

## 16. Passo successivo suggerito

1. **Prima cosa:** far partire a Leo `AGGIORNA_RACCOLTA_5T_CODICI.bat` (pacchetto H), così i 3 sensori in più
   iniziano a raccogliere. Poi fetch di lunedì 19/10 e `TRAFFICO_RILANCIA_SENSORI.bat`.
2. **Fase 4** (`docs/PIANO_TRAFFICO_FASE2.md`, sezione 5): incrocio traffico × offerta di trasporto pubblico
   per via (passaggi bus/tram per ora dal GTFS), per trovare "vie con molto traffico e poco TP".
   Con il modello attuale conviene **limitare l'analisi a Torino e prima cintura**, dove il modello è
   sensato (sui corridoi di bordo i valori non sono attendibili) e usare la classe a 3 livelli, non i numeri.
3. **Fase 3-bis (se Leo vuole più precisione):** percorsi stocastici (spargere il traffico su più itinerari)
   e attrattori per le destinazioni non domestiche; oppure aumentare i punti per zona. Costo basso
   (l'instradamento completo dura meno di un minuto), ma i criteri di riuscita restano quelli fissati qui.
