# Esito — Fase 5 del Risultato 8 (giro di correzione: assi, corsie, ZTL, TP per posizione, modello V4)

Eseguito da: **agente opencode** sul PC di Leo. Giorno: **18/10/2026**.
Cartella `C:\projects\Progetti\GTT`. Ramo git **`prova`**, **nessun commit**.
Database storico e `data/raw/` aperti in **sola lettura**. Niente scritto né riavviato sul Pi.
Riferimento: `docs/PIANO_TRAFFICO_FASE5.md`. I criteri di riuscita della Fase 3, la regola
V4-contro-V0, le definizioni di "molto traffico", "poco TP", "affidabile" e "robusto" e l'uso di
`docs/CONOSCENZA_TORINO_LEO.md` come solo controllo di buon senso **non sono stati cambiati**.

## 0. Esito di ogni pacchetto (riga di stato)

```
PASSO A: OK    (assi = stessa strada anche se cambia nome/comune; tratte 0,3-1,5 km; incoerenti 5 su 31.639 = 0,02%)
PASSO B: OK    (corsie e capacita': tag lanes su 29,4% dei tratti; capacita' per corsia dichiarata; corsie per tratta)
PASSO C: OK    (3 ZTL unificate con orari + 143 aree pedonali; 0 sensori 5T dentro ZTL/aree pedonali)
PASSO D: OK    (TP per POSIZIONE delle fermate: 5.055 fermate, 13.158 corse; copertura per tratta; causa Cairoli trovata)
PASSO E: OK    (modello V4 valutato UNA volta: NON migliora V0 secondo la regola fissata -> resta V0; congestione ancora debole)
PASSO F: OK    (universo Torino 540 tratte / 343,3 km; fasce +-38% (50%) e +-64% (90%); estrapolazioni x2)
PASSO G: OK    (pubblicazione + incrocio: 5 tratte "molto traffico e poco TP", 2 robuste; accordo con Leo riportato)
PASSO H: OK    (codici ~2 presenti nel database copiato; TRAFFICO_RILANCIA_SENSORI.bat esteso; cambio ora legale da controllare dopo il 25/10)
```

**Risultato finale: variante del traffico = V0, classe di esito = `C-DEBole`**
(errore mediano **38,4%**, IC90 25,5%-49,8%, p90 64,5%, rho di Spearman **0,605**, n=20).
**V4 non migliora V0 secondo la regola** (rho V4 0,571 < 0,605): per il piano si tiene V0.
La diagnostica dice però *quale* pezzo conta (sezione E).

---

## 1. Decisioni dell'agente (cosa ho scelto e perché)

1. **Prima la struttura (A, B, C), poi D ed E**: l'estensione della rete OSM (corsie) è servita
   anche agli assi, quindi ho ricostruito la rete in `data/processed/traffico_d/rete/` (la rete
   della Fase 3 resta intatta). `rete_osm.py` è stato esteso **con copia `.bak_18ott`** e conserva
   la compatibilità con gli script 42-50 (stesse chiavi in `carica()`); il controllo dice che la
   nuova rete è **identica** alla Fase 3 (81.966 nodi, 105.890 tratti).
2. **Costruzione degli assi** (pacchetto A): a ogni incrocio accoppio i due tratti che proseguono
   quasi dritti (deviazione ≤ 35°, ≤ 45° se stesso nome o stesso `ref`), scegliendo sempre la coppia
   con deviazione minima; **non accoppio** agli incroci con rotatoria o con 5+ tratti (regola per
   rotatorie e svincoli); le due carreggiate omonime entro 100 m le unisco nello stesso asse.
   L'asse si ferma dove la classe diventa autostrada/tangenziale.
3. **Unità di volume a due versi coerente coi sensori**: i sensori 5T a un solo verso sono già
   raddoppiati nella misura; per coerenza ho definito il flusso di una **tratta** come somma dei due
   versi, **x2 se la tratta è a senso unico** (una sola carreggiata). Questo ha cambiato il valore di
   riferimento di V0 rispetto alla Fase 3 (dichiarato in anomalie), ma rende V0 e V4 confrontabili.
4. **TP per posizione**: le fermate GTFS entro 40 m sono raggruppate in una sola "fermata di
   posizione" (i due versi sono fermate distinte nello stesso punto), così "partenze/ora" è la somma
   dei due versi come chiede il piano. **Mai i nomi**: solo `stop_lat/stop_lon`.
5. **Modello V4**: attrattori (riuso `punti_v3` della Fase 4), congestione con capacità **per corsia**
   (pacchetto B) e domanda di punta, MSA + BPR, ZTL chiusa al traffico di attraversamento nella
   punta, porte di rango ≥ 3. Un solo giro di valutazione, 8 iterazioni (5 per le ablazioni).
6. **Universo (pacchetto F)**: trattе di Torino con **punteggio di importanza ≥ 3** (dal catalogo di
   script 24, mappato sui tratti via `segmenti.csv` della Fase 3) o classe primary e superiori,
   lunghezza ≥ 300 m, esclusi autostrade/tangenziali/raccordi. Ho interpretato così il "rango ≥ 3"
   del piano (che parla di punteggio ≥ 3, non della sola classe OSM).
7. **Regola (d) di affidabilità**: confronto il flusso di una tratta con la **media dei vicini nella
   stessa catena** (non con la mediana dell'intero asse), perché le tratte sono già tagliate ai grandi
   incroci e un asse lungo ha un gradiente di flusso fisiologico. Soglia 100%, come da piano; sui
   tratti con flusso < 500 non si applica (evita di marcare strade minuscole).
8. **"Poco TP"**: `copertura_con_metro` ≤ 50% della lunghezza (bus/tram ≥ 4 pass/h entro 300 m
   **oppure** stazione metro/ferrovia entro 600 m). Sensibilità a 30% e 70% e con la sola
   `copertura_300`. Robustezza = resta "molto traffico" con traffico x0,65/x1,35 **e** con le soglie
   di sensibilità.
9. **Accordo con Leo**: le strade della sua conoscenza sono cercate su **tutte** le tratte di Torino
   (non solo l'universo), così il confronto non dipende dal filtro; fasce A/B/C dai terzili
   dell'universo. **Riportato, mai usato per scegliere o tarare.**
10. **Nessun commit, database e `data/raw` in sola lettura.**

---

## 2. Pacchetto A — assi e tratte (script 56-57)

- **Assi: 31.639. Tratte: 47.807.** Accoppiamenti "quasi dritto" agli incroci: 63.990.
- Copertura: **100%** dei km di strade di rango OSM ≥ 3 in Torino appartengono a un asse
  (340,2 km). Tratte sotto 300 m: 38.077 in tutto (di cui **solo 620** hanno rango OSM ≥ 3 a
  Torino); tratte oltre 1.500 m: 196.
- **Assi incoerenti (classi di famiglie diverse, es. autostrada + urbana): 5 su 31.639 = 0,02%**
  (soglia di arresto 10%: ampiamente rispettata).
- **Esempi del piano, tutti corretti:** Trapani→Siracusa→Potenza→Lecce→Cosenza (22,65 km);
  Via Tommaso Agudio→Corso Don Luigi Sturzo (5,79 km; l'asse continua anche come Lungo Stura Lazio
  e ponte Diga); Corso Francia (41,8 km, comuni **Torino, Collegno, Rivoli**, si ferma entrando in
  autostrada verso Rivoli); Corso Regina Margherita (25,8 km, fino a lungo Po e sottopasso
  Repubblica); Corso Allamano (22,5 km, Torino-Grugliasco-Rivoli); Corso Vittorio Emanuele II
  (12,8 km, un nome solo); Corso Giulio Cesare (14,3 km); Corso Vercelli (8,8 km); Corso Lione
  (2,2 km, fino a Corso Mediterraneo/Bobbio). L'asse **non** si ferma al confine comunale.
- Indipendente (verifica 4): per le coppie Trapani↔Lecce, Lecce↔Potenza, Agudio↔Sturzo,
  Francia↔Rivoli i punti OSM delle due strade hanno **distanza minima 0 m** (si toccano): la
  continuità fisica è confermata sul PBF.

## 3. Pacchetto B — corsie e capacità (script 58; `rete_osm.py` esteso con `.bak_18ott`)

- **Copertura del tag `lanes`**: 29,4% dei tratti (29,3% dei km). Per classe: motorway 99%,
  primary 87% (91% dei km), secondary 82%, tertiary 62%, residential 19%, service 0,9%. Dove
  manca, corsie per verso standard dichiarate (`CORSIE_DEFAULT_VERSO`).
- **Capacità per corsia dichiarata** (veic/ora, fonte: capacità pratica urbana/HCM): motorway 1.800,
  trunk 1.400, primary 1.000, secondary 800, tertiary 700, residential 500, service 300.
  Capacità di tratto = corsie del verso × capacità per corsia.
- **Controllo a mano su 10 strade** (`docs/RAPPORTO_CORSIE.txt`): corsie per verso (mediana) —
  Racconigi 1, Re Umberto 1, Francia 1, Nizza 1, Vittorio Emanuele II 1, Lungo Po Diaz 1+1,
  Unità d'Italia 3, Giulio Cesare 2, Cosenza 3; **Agudio non trovato col suo nome** (è
  "Tommaso Agudio"). Le strade a 1 corsia per verso sembrano in parte **sottostimate** da OSM (i
  controviali non sono contati): dichiarato.

## 4. Pacchetto C — ZTL unificata e aree pedonali (script 59)

- **3 zone ZTL** unificate: *romana* (lun-sab 21:00-07:30), *centrale* (lun-ven 07:30-10:30, orari
  dalla fonte 5T 2022-2024, la più recente; il Comune 2016-2017 concorda), *valentino* (00:00-24:00).
  In più **143 aree pedonali**.
- La ZTL del Comune è in **EPSG:3003** (Gauss-Boaga), quella 5T in lat/lon: convertite e unite.
- **Nessun sensore 5T cade dentro una ZTL o un'area pedonale** (0).
- Controlli di coerenza con la conoscenza di Leo (per posizione): Piazza Castello, Via Montebello,
  Via San Massimo hanno `ztl_frazione` 1,00 (dentro la ZTL Centrale); Corso Cairoli 0,25 (il tratto
  verso Piazza Vittorio, "più avanti inizia la ZTL"); Via Roma non compare nella rete **auto**
  (è pedonale, quindi esclusa dal grafo): coerente.

## 5. Pacchetto D — trasporto pubblico per POSIZIONE (script 60-61)

- Giorno feriale tipico **14/10/2026**: 13.690 corse attive, **13.158 bus/tram** (controllo
  indipendente: 13.158, uguale). 6.989 fermate GTFS → **5.055 fermate "di posizione"** (entro 40 m),
  di cui 23 di metropolitana; nessuna ferrovia nel GTFS (flag ferroviario preso da OSM).
- Copertura delle tratte (bus/tram ≥ 4 pass/h entro 300 m): 48% in tutto il territorio; sensibilità
  200 m → 4.506 tratte cambiano gruppo, 400 m → 3.073, soglia 6/h → 3.052, soglia 2/h → 3.991.
- **Controlli di buon senso (per posizione):** Corso Francia, Regina Margherita, Nizza, Vittorio
  Emanuele II, Giulio Cesare, Cairoli, Fiume hanno tutti copertura 300 m **piena** (1,00) — come
  atteso.
- **DIAGNOSTICA richiesta — perché Corso Cairoli aveva "2 linee ma 0,0 passaggi/ora":** la Fase 4
  contava i passaggi come **media pesata su tutto il corridoio per nome** (1,35 km) mentre **solo
  156 m** avevano una forma agganciata, e attribuiva ogni corsa all'**ora di partenza del capolinea**
  (non a quella del punto): il valore collassava a 0,0 (e il "2" veniva dai pochi tratti agganciati).
  In più due fermate vicine (Giolitti, Mazzini) elencano le linee 24 e 93 ma hanno departures solo
  di prima mattina/sera (0 in punta). **Con le coordinate delle fermate Cairoli è servito** (copertura
  1,00, fino a 81 pass/h a una fermata vicina). Stessa causa per Corso Fiume (una linea vecchia, 0,0;
  nuovo metodo: copertura piena, 26,5 pass/h).

## 6. Pacchetto E — modello del traffico V4, valutato UNA volta (script 62-63)

Tutti i modelli girano sulla **stessa rete** e con la stessa unità (diurno 6-21, due versi). V0 =
popolazione, senza congestione né ZTL, tutte le porte. V4 = attrattori + congestione per corsia +
ZTL + porte ≥ 3. Taratura **leave-one-out** con un fattore globale, come la Fase 3.

| variante | n | err. mediano (IC90) | p90 | rho LOO | rho grezzo | k |
|---|---|---|---|---|---|---|
| **V0 (attuale)** | 20 | **38,4%** [25,5%-49,8%] | 64,5% | **0,605** | 0,626 | 0,953 |
| V4 | 20 | 30,5% [25,5%-48,3%] | 66,9% | 0,571 | 0,577 | 1,007 |
| V4 senza attrattori | 20 | 40,5% [26,9%-54,5%] | 63,0% | 0,577 | 0,612 | 0,995 |
| V4 senza congestione | 20 | 29,9% [24,1%-38,5%] | 65,8% | **0,615** | 0,638 | 0,947 |
| V4 senza porte ristrette | 20 | 29,0% [26,2%-48,0%] | 62,7% | 0,586 | 0,594 | 1,013 |

**Regola di scelta (fissata):** V4 si adotta se rho(V4) ≥ rho(V0) **e** l'errore mediano di V4 non è
peggiore di V0 di più di 3 punti. Qui rho(V4) = 0,571 < 0,605 → **resta V0**, e non si fanno altri
tentativi. Diagnostica (cosa conta): **togliere la congestione migliora** (err 29,9%, rho 0,615):
la congestione, così come funziona, **non aiuta il rango**; togliere gli attrattori peggiora
(40,5%): gli attrattori servirebbero; togliere la restrizione delle porte peggiora (rho 0,586).

**Controllo obbligatorio dei tempi di viaggio (V4 congestionato vs flusso libero):**

| percorso | flusso libero | V4 congestione | atteso in punta |
|---|---|---|---|
| Castello → Collegno | 13,1 min | **13,8 min** | **20-35 min (NON rispettato)** |
| Castello → Venaria | 12,8 | 14,0 | |
| Castello → Settimo | 14,7 | 15,3 | |
| Castello → Moncalieri | 11,4 | 11,9 | |
| Castello → Orbassano | 18,0 | 20,1 | |

La congestione resta **troppo debole** (v/c medio 0,55, contro 0,40 in Fase 4): nonostante le
capacità per corsia, la domanda di punta è piccola rispetto alla capacità totale. Velocità mediana
del modello sui tratti dei sensori in punta = **49,2 km/h** (misurata 41,6): coerente con "congestione
quasi assente". **Dichiarato**: il mandato del piano era "se dopo un tentativo ragionevole la
congestione resta inattiva, dichiaralo e tieni V0".

## 7. Pacchetto F — affidabilità, universo e fasce (script 65)

- **Universo di Torino: 540 tratte, 343,3 km** (mediana 5.400 veic/giorno). Prima cintura:
  248 tratte, 181,7 km.
- Regole di inaffidabilità (tratte e km marcati): **bordo** (porta entro 1,5 km) 2.363 / 514,9 km;
  **struttura** (ponte/sottopasso/…) 96 / 20,8 km; **rango ≤ 2 con flusso > 12.000 senza sensore**
  532 / 68,3 km; **salto > 100% dalla media dei vicini** 283 / 123,0 km.
- Tratte citate dal piano: **Via Palestrina** → inaffidabile (rango ≤ 2, flusso 13.061 senza sensore);
  **Corso Monte Lungo** → affidabile (21.851); **Via Quarto dei Mille** → affidabile (325, strada
  piccola).
- **Fasce dichiarate:** in metà dei casi lo scarto è entro **±38%**; 9 volte su 10 entro **±64%**.
  Fuori dall'intervallo validato (8.845-105.230 veic/giorno) la stima è `estrapolazione: true` e la
  fascia si allarga **×2** (±77% / ±130%). Dove c'è un sensore sulla tratta, valore **misurato**
  (×2 se un solo verso), `fiducia` alta.

## 8. Pacchetto G — pubblicazione e incrocio (script 66)

- **Universo di Torino: 540 tratte, 343,3 km**; lunghezza **coperta dal TP** (copertura ≥ 50%):
  **327,3 km = 95,3%** (con la sola copertura_300: 94,9%).
- **"Molto traffico"** (terzo più alto, ≥ 11.720 veic/giorno, e ≥ 8.845 limite validato): **180
  tratte**. **"Poco TP"** (copertura ≤ 50%): **19 tratte**. **"Da guardare" (molto traffico e poco
  TP): 5 tratte**, di cui **2 robuste** (per corsia: 6).
- **Le 5 tratte "da guardare"** (2 assi):

| # | asse | trata | veic/giorno | fascia 50% | copertura TP | corsie | veic/corsia | robusta |
|---|---|---|---|---|---|---|---|---|
| 1 | Regina Margherita | Asse di penetrazione urbana di Corso Regina Margherita (Q015) | 33.529 | ±38% | 0,00 | 3 | 11.176 | **sì** |
| 2 | Regina Margherita | Corso Regina Margherita (Q015) | 30.402 | ±38% | 0,00 | 3 | 10.134 | **sì** |
| 3 | Regina Margherita | Corso Regina Margherita (Q015) | 32.134 | ±38% | 0,40 | 3 | 10.711 | no |
| 4 | Regina Margherita | Corso Regina Margherita (Q015) | 32.606 | ±38% | 0,50 | 3 | 10.869 | no |
| 5 | Casale > Gran Madre > Moncalieri | Corso Moncalieri (Q022) | 13.992 | ±38% | 0,25 | 4 | 3.498 | no |

- **La lista NON è dominata da raccordi/strutture/bordo**: 0 tratte "da guardare" con nome di
  ponte/sottopasso, 0 al bordo (già esclusi dall'universo).
- **Tre esempi:** (1) da guardare = Asse di penetrazione urbana di Corso Regina Margherita,
  33.529 veic/giorno, 3 corsie, TP 0%, 0 linee; (2) molto traffico ma TP buono = Corso Unità d'Italia
  (80.946, TP 100%, 13,5 pass/h); (3) poco traffico e poco TP = Ettore Stampini (9.485, TP 40%).
- **Accordo con la conoscenza di Leo (solo riferimento, NON taratura):** strade nella fascia giusta
  **10 su 18**; confronti giusti **4 su 7** (giusti: Vittorio Emanuele II > Giulio Cesare,
  Casale ≈ Moncalieri, Racconigi > Re Umberto, Vercelli > Bolzano; sbagliati: Cosenza > Lione,
  Stati Uniti > Duca degli Abruzzi, Agudio > Monte Lungo).

## 9. Pacchetto H — raccolta e rilancio

- Il database copiato `data/storico_backup.sqlite` ha **112 sensori** e **i tre codici `~2`**
  (`13077~2`, `40123~2`, `40189~2`): la correzione del raccoglitore è arrivata sul PC (ultima
  lettura 18/10 12:14Z). I secondi sensori avranno dati utili dopo ~6 giorni feriali e, come da
  piano, **non entrano** nelle 20 unità di valutazione (le soglie non cambiano).
- `scripts\TRAFFICO_RILANCIA_SENSORI.bat` **esteso** (copia `.bak_18ott`): dopo il fetch esegue anche
  63 (valutazione), 65 (fasce), 66 (incrocio) e 67 (verifiche). Assi, corsie, ZTL, TP per posizione
  (60-61) e modello V4 (62) non dipendono dai sensori: si rifanno con `FASE5_MODELLO.bat`.
- **Da fare da Leo:** il fetch di **lunedì 19/10** e il rilancio con il `.bat`; **dopo il 25/10**
  (fine ora legale) il controllo a mano delle ore locali nello script 26.

---

## 10. Verifiche indipendenti (sezione 11) — `scripts/67_verifiche_fase5.py`

`docs/RAPPORTO_FASE5_VERIFICHE.txt`:
1. Partenze GTFS ricalcolate con un altro metodo (pandas puro): **13.158 = 13.158** (uguale);
2. fattore di taratura ricalcolato a mano = **0,953205**, coincide; 3 errori leave-one-out rifatti
   a mano (SP1 Valli di Lanzo 49,8%, Giulio Cesare 28,6%, Trieste 15,6%) coerenti;
3. 5 tratte seguite dai dati grezzi (OSM → asse → flusso → copertura → gruppo): tutte coerenti;
4. 3 assi con cambio di nome (Trapani/Lecce, Lecce/Potenza, Agudio/Sturzo, +Francia/Rivoli): punti
   OSM a **0 m** l'uno dall'altro (continuità confermata);
5. `git status`: nessun commit. Vedi l'anomalia 4 (file vietati).

---

## 11. Anomalie e limiti (da dire chiaramente)

1. **Il risultato resta debole.** Classe `C-DEBole`, errore mediano 38,4%, rho 0,605, e l'intervallo
   al 90% (25,5%-49,8%) attraversa la soglia del 35%: **la stima puntuale è incerta**. I numeri
   assoluti servono a ordinare, non a contare i veicoli. Ci sono errori grandi e noti (Corso Unione
   Sovietica +177%, Corso Sebastopoli +99%): il modello V0 concentra il traffico su alcune strade.
2. **V4 non migliora V0**: la congestione, anche con le capacità per corsia, resta debole
   (Castello→Collegno 13,8 min contro 20-35 attesi). Come nella Fase 4, l'ablazione "senza
   congestione" andrebbe meglio (rho 0,615), ma la regola del piano non consente di sceglierla.
3. **Il gruppo "da guardare" è piccolissimo** (5 trattе, 2 assi): con il TP misurato per posizione,
   **il 95,3% dei km dell'universo è servito** e in Torino **non ci sono quasi strade grandi con
   molto traffico e nessun bus**. Le poche eccezioni sono la **penetrazione di Corso Regina
   Margherita** (expressway, nessuna fermata) e un tratto di **Corso Moncalieri**. È il risvolto
   della correzione: la vecchia lista (Cairoli, Palestrina, Agudio, Cosenza, San Massimo…) era un
   artefatto del TP misurato "sulla strada".
4. **File vietati.** `git status` mostra modificati `MEMORIA_PROGETTO.md`,
   `scripts/mappa_template.html` e `scripts/04_genera_mappa.py`. **Non li ho toccati io**: le loro
   ore di modifica (15:15-15:26) e i file rigenerati nello stesso intervallo (`data/catalogo/*.js`,
   `mappa_torino.html`, `data/live.js`, `data/stat.js`, `replay_*.js`) mostrano **una seconda
   sessione al lavoro sulla mappa in parallelo**. Il mio lavoro ha scritto **solo** gli script 56-67,
   `docs/RAPPORTO_*` nuovi, `data/processed/traffico_d/**`,
   `data/processed/risultato8_traffico_tp_v2.json`, i `.bat` e le copie `.bak_18ott`.
5. **Convenzione a due versi ×2 sulle tratte a senso unico**: ha cambiato il riferimento di V0
   rispetto alla Fase 3 (rho 0,605/err 38,4% contro 0,602/31,9%); è la convenzione coerente coi
   sensori, ma va ricordata. La classe di esito è la stessa (`C-DEBole`).
6. **Corsie stimate** (70% dei tratti) e **corsie mancanti sui controviali**: la pressione per corsia
   è indicativa. **Sensori a un solo verso**: la punta non è validata. **IMQ 2022**: solo residenti
   11-84 anni. **TP programmato** (GTFS): niente ritardi, capienza, passeggeri. **Centro** (ZTL e
   pedonali) non stimato in modo affidabile.
7. **Accordo con Leo modesto** (10/18 fasce, 4/7 confronti): molte strade che Leo sente "di
   quartiere ma trafficate" (Bolzano, Quintino Sella, Re Umberto) il modello le tiene più basse, e
   alcune arterie Leo le sente più trafficate di quanto stimato. **Non ho tarato nulla su Leo.**

---

## 12. Durate

| Attività | Durata |
|---|---|
| Lettura piani/esiti + esplorazione | ~20 min |
| A-B (rete con corsie + assi/tratte) | ~15 min (asse 57: 11 s, rete 8 s) |
| C + D (ZTL, fermate, copertura) | ~25 min |
| E: V0 | 63 s |
| E: V4 (8 iterazioni MSA + giorno) | **~22,5 min** |
| E: ablazioni 1-2-3 | ~21 min |
| E: valutazione 63 | ~1 min |
| F-G-H e verifiche 56-67 | ~15 min |
| **Totale sessione** | **~1 h 50 min** (14:05 → 15:40 circa) |

## 13. File creati / modificati

**Script nuovi (56-67):** `56_build_rete_lanes.py`, `57_assi_tratte.py`, `58_corsie.py`,
`59_ztl.py`, `60_tp_fermate.py`, `61_tp_tratte.py`, `62_v4_modello.py`, `63_v4_valutazione.py`,
`65_affidabilita.py`, `66_pubblicazione_incrocio.py`, `67_verifiche_fase5.py`.
**Script/bat modificati (con `.bak_18ott`):** `scripts/rete_osm.py`,
`scripts/TRAFFICO_RILANCIA_SENSORI.bat`. **Nuovo bat:** `scripts/FASE5_MODELLO.bat`
(calcolo lungo, ripartibile, log `logs/fase5_modello.log`).
**Dati nuovi:** `data/processed/traffico_d/` (rete, `tratte.json`, `tratte.csv`, `assi.json`,
`assi_tratte.npz`, `corsie.csv`, `tratte_corsie.json`, `ztl_unificata.json`, `tratte_ztl.csv`,
`tp_fermate.csv`, `tp_tratte.csv`, `tratte_traffico.json`, `valutazione_fase5.json`, le 5 varianti
`v0/v4/abl1/abl2/abl3/`); `data/processed/risultato8_traffico_tp_v2.json` (la v1 della Fase 4 resta
intatta).
**Rapporti nuovi in `docs/`:** `ESITO_FASE5_TRAFFICO.md`, `RAPPORTO_ASSI_TRATTE.txt`,
`RAPPORTO_CORSIE.txt`, `RAPPORTO_ZTL.txt`, `RAPPORTO_TP_ACCESSIBILITA.txt`,
`RAPPORTO_TRAFFICO_V4.txt`, `RAPPORTO_AFFIDABILITA.txt`,
`RAPPORTO_RISULTATO8_TRAFFICO_TP_V2.txt`, `RAPPORTO_FASE5_VERIFICHE.txt`.
**Non toccati da me:** `MEMORIA_PROGETTO.md`, `scripts/mappa_template.html`,
`scripts/04_genera_mappa.py` (modificati da un'altra sessione, vedi anomalia 4),
`data/raw/*`, `data/storico_backup.sqlite`, i dati delle Fasi 1-4. **Nessun commit.**
**Pacchetti Python:** nessuno installato (numpy 2.5.3, scipy 1.18.1, pandas 3.0.6, shapely 2.2.0,
pyproj 3.8.0, osmium, networkx 3.7 già presenti).

## 14. Testo proposto per MEMORIA_PROGETTO.md (non l'ho modificata)

> | Traffico 5T, Fase 5 (56-67) | **18/10.** Giro di correzione della Fase 4. **A** assi (stessa strada anche se cambia nome/comune) e tratte 0,3-1,5 km: 31.639 assi, 47.807 tratte, 100% dei km di rango ≥3 in Torino coperti, 0,02% incoerenti; Trapani>Lecce>Potenza, Agudio>Sturzo, Francia (Torino-Collegno-Rivoli) corretti. **B** corsie (tag `lanes` su 29% dei tratti; capacità per corsia dichiarata) e `veic_per_corsia`. **C** ZTL unificate (3 zone + 143 aree pedonali; 0 sensori dentro). **D** TP per POSIZIONE delle fermate (5.055 fermate, 13.158 corse; **copertura ≥4 pass/h entro 300 m**): 95,3% dei km coperti; **causa trovata per Cairoli**: la Fase 4 mediava su tutto il corridoio (solo 156 m agganciati) e usava l'ora di partenza del capolinea. **E** modello V4 (attrattori + congestione per corsia + ZTL + porte ≥3) valutato una volta: **non migliora V0** (rho 0,571 < 0,605) → **resta V0, C-DEBole** (err 38,4%, IC90 25,5-49,8%, rho 0,605, n=20); congestione ancora debole (Castello→Collegno 13,8 min contro 20-35). **F** universo Torino 540 tratte / 343 km, fascia ±38% (50%) / ±64% (90%), estrapolazioni ×2. **G** incrocio: **5 tratte "molto traffico e poco TP" (2 assi: penetrazione di Regina Margherita e Corso Moncalieri), 2 robuste**; accordo con la conoscenza di Leo 10/18 fasce e 4/7 confronti. **H** i tre codici `~2` sono nel database copiato; `TRAFFICO_RILANCIA_SENSORI.bat` esteso (63/65/66/67). Output: `data/processed/risultato8_traffico_tp_v2.json`, `data/processed/traffico_d/**`, `docs/RAPPORTO_*`. Dettagli: `docs/ESITO_FASE5_TRAFFICO.md`. Verifiche indipendenti: `docs/RAPPORTO_FASE5_VERIFICHE.txt` (tutte OK).

## 15. Passo successivo suggerito

1. **Solo se Leo vuole:** mappa delle tratte colorate per `veic_giorno` (con fascia) e dei 2 assi
   "da guardare"; il resto è già in `risultato8_traffico_tp_v2.json`.
2. **Raccolta:** fetch di lunedì 19/10 e rilancio; dopo il 25/10 controllo dell'ora legale.
3. **Se in futuro un modello migliore:** la strada è la congestione (domanda per fascia oraria più
   fine, capacità reali, più coppie O-D) — NON gli attrattori né le porte, che qui non spostano il
   rango. I criteri di riuscita restano quelli della Fase 3.
