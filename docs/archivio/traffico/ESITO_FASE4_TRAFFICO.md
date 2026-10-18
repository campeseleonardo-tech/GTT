# Esito — Fase 3-bis (modello V3) e Fase 4 (traffico × trasporto pubblico) del Risultato 8

Eseguito da: **agente opencode** sul PC di Leo. Giorno: **17/10/2026**.
Cartella `C:\projects\Progetti\GTT`. Ramo git **`prova`**, **nessun commit**.
Database storico e `data/raw/` aperti in **sola lettura**. Niente scritto né riavviato sul Pi.
Riferimento: `docs/PIANO_TRAFFICO_FASE4.md` (i criteri di riuscita, la regola V0/V3 e le regole
di pubblicazione **non** sono stati cambiati).

## 0. Esito di ogni pacchetto (riga di stato)

```
PASSO A: OK    (V3 costruito ed eseguito una volta; per la regola fissata NON migliora V0 -> resta V0)
PASSO B: OK    (13.158 corse bus/tram il 14/10/2026; 12.256 agganciate alla rete = 93,1% >= 75%)
PASSO C: OK    (universo di Torino 872 corridoi / 1.300,5 km; cintura 574 / 756,4 km; fascia 50%/90%)
PASSO D: OK    (23 corridoi "molto traffico e poco TP", 12 robusti; 4 sono ponti/sottopassi, esclusi)
PASSO E: FERMO - da verificare quando Leo incolla il log e dopo il fetch di lunedi' 19/10
```

**Risultato finale: variante del traffico = V0, classe di esito = `C-DEBole`**
(errore mediano 31,9%, IC90 23,7%-40,2%, rho di Spearman 0,602, n=20).
**V3 non migliora V0 secondo la regola** (rho V3 = 0,573 < 0,602): per il piano si tiene V0 e
non si fanno altri tentativi. La diagnostica dice però *quale* miglioramento conta (sezione 2).

---

## 1. Decisioni dell'agente (cosa ho scelto e perché)

1. **Pacchetto B prima di A** (era consentito): l'offerta di trasporto pubblico non dipende dal
   modello del traffico.
2. **Giorno feriale tipico = mercoledì 14/10/2026** (dentro la validità del feed 3/10, senza
   eccezioni rilevanti: 126 servizi aggiunti e 9 tolti dalle regole settimanali). Corse bus
   (`route_type`=3) e tram (0): **13.158**. Metropolitana (1) e funicolare (7) **fuori** dai
   passaggi per strada (solo flag `metro_vicina`).
3. **Map matching delle forme GTFS**: polilinea ricampionata ogni 25 m; ogni punto si aggancia al
   tratto stradale più vicino entro 25 m; una corsa è "agganciata" se ≥60% dei punti dentro il
   riquadro OSM si aggancia e tocca ≥5 tratti. **93,1% delle corse agganciate** (2 forme su 1.231
   no). Le corse non agganciate NON entrano nei conteggi (dichiarato). I campioni di forma fuori
   dal riquadro del taglio non sono valutabili e non contano.
4. **Altezza del corridoio per il TP = tratto più servito (massimo), non media.** Le vie lunghe
   hanno tratti senza bus; la media pesata per lunghezza le farebbe sembrare "scoperte" a torto
   (es. Corso Vittorio Emanuele II: 3,1 pass/h di media ma 40 pass/h sul tratto migliore). Il
   campo `passaggi_ora_punta_am` (media) resta nel file per trasparenza.
5. **Congestione V3 con metodo delle medie successive (MSA), 10 iterazioni, funzione BPR
   t = t0·(1+0,15·(v/c)⁴)**, capacità per classe di strada (standard: motorway 8.000, primary 3.600,
   secondary 2.600, residential 900 veic/h, ecc.) perché la rete non conserva il numero di corsie.
   Caso principale = ora di punta del mattino (media delle ore 7 e 8); il giorno intero (6-21) è
   assegnato sulla rete con i tempi di punta congestionati. **La congestione è risultata debole**
   (v/c medio 0,40): i tempi di punta restano quasi quelli a flusso libero (vedi sezione 4).
6. **Attrattori** (punto 1 di V3): destinazioni pesate sui servizi geolocalizzati (catalogo
   comunale di Torino + servizi OSM della cintura), per gruppo di scopo; origine "da casa" (popolazione)
   se il viaggio inizia un'uscita o segue un ritorno a casa, altrimenti con gli attrattori dello scopo
   del viaggio precedente (catene di spostamenti IMQ). Massimo **8 nodi per gruppo per zona**
   (contro i 20 punti della popolazione) per tenere il calcolo sotto controllo: le origini passano
   da 810 a **2.263**.
7. **Porte V3**: solo rango ≥3 (39 porte su 206), peso proporzionale alla capacità. I viaggi fra
   due zone **esterne diverse** NON producono flusso (avvengono fuori dall'area studiata:
   instradarli creerebbe traffico finto sui corsi di Torino — difetto già visto in Fase 3).
8. **Ablazioni diagnostiche con 6 iterazioni** (invece di 10) per contenere il tempo: servono solo
   a dire quale miglioramento conta, non a scegliere la variante.
9. **Fascia di errore allargata ×2 per le estrapolazioni** (corridoi con flusso modello fuori
   dall'intervallo dei sensori): valore dichiarato, non nascosto.
10. **Pacchetto D**: "poco TP" misurato sul tratto più servito; i **ponti/sottopassi/cavalcavia**
    sono tolti dalla presentazione (la lista era dominata da strutture corte: 4 casi) ma restano
    nei dati.

## 2. Pacchetto A — Fase 3-bis, modello V3 (script 49, 50, 50b; `scripts\V3_MODELLO.bat`)

Criteri identici alla Fase 3 (stesse 20 unità-sensore, taratura leave-one-out con un fattore
globale, stessa tabella di classificazione). Metodo A sulle stesse unità: 36,9%.

| variante | n | errore mediano (IC90) | p90 | rho LOO | rho grezzo |
|---|---|---|---|---|---|
| **V0 (attuale)** | 20 | **31,9%** [23,7%-40,2%] | 59,3% | **0,602** | 0,614 |
| **V3 (attrattori + congestione + porte)** | 20 | 29,0% [21,4%-37,7%] | 65,0% | **0,573** | 0,626 |
| V3 senza attrattori | 20 | 35,2% [24,6%-47,2%] | 83,3% | 0,559 | 0,608 |
| V3 senza congestione | 20 | 26,6% [19,4%-31,7%] | 66,2% | **0,617** | 0,639 |
| V3 senza porte ristrette | 20 | 27,4% [20,6%-38,1%] | 66,5% | 0,571 | 0,653 |

**Regola di scelta (fissata):** V3 si adotta se rho(V3) ≥ rho(V0) **e** l'errore mediano non è
peggiore di V0 di più di 3 punti. Qui rho(V3) = 0,573 < 0,602 → **resta V0**, e non si fanno altri
tentativi. **Diagnostica (cosa conta):** togliendo gli **attrattori** il modello peggiora
(35,2% e rho 0,559) → gli attrattori servirebbero; togliendo la **congestione** migliora
(26,6% e rho 0,617) → **la congestione così com'è non aiuta**; togliendo la restrizione delle
porte peggiora un po' (rho 0,571). Il difetto principale di V0 (concentrazione senza congestione)
**non è stato risolto**.

**Controllo obbligatorio dei tempi di viaggio (V3 congestionato vs flusso libero):**

| percorso | flusso libero | congestionato V3 | atteso in punta |
|---|---|---|---|
| Castello → Collegno | 13,1 min | **13,3 min** | **20-35 min (NON rispettato)** |
| Castello → Venaria | 12,8 | 13,4 | |
| Castello → Settimo | 14,7 | 15,1 | |
| Castello → Moncalieri | 11,4 | 11,7 | |
| Castello → Orbassano | 18,0 | 19,3 | |
| Castello → Rivoli | non raggiungibile (punto di riferimento caduto su un nodo isolato) | idem | |

Il controllo **non è soddisfatto**: con v/c medio 0,40 la congestione sposta i tempi di pochi
decimi di minuto. È il motivo per cui la congestione non migliora il modello. **Non l'ho corretta**
(il piano dice: se V3 non migliora, si tiene V0 e si smette).
Secondo controllo indipendente: velocità mediana del modello V3 sui tratti dei sensori in punta =
**49,5 km/h** (a flusso libero ~50 km/h: coerente con "congestione quasi assente").

## 3. Pacchetto B — offerta di bus e tram per strada (script 51, 52)

- Giorno feriale tipico: **14/10/2026** (mercoledì). Corse bus/tram **13.158**.
- **Corse agganciate alla rete stradale: 12.256 = 93,1%** (soglia di arresto 75%: superata).
- Tratti stradali con almeno un passaggio: **9.807** su 105.890 (9,3%). Corridoi con passaggi:
  **1.673** (di cui 551 a Torino). Corridoi di Torino con **zero** passaggi: 1.699 su 2.250.
- Controlli: (1) corse totali ricalcolate con un altro metodo = **13.158 identiche (tolleranza 0)**;
  (3) tre fermate ricalcolate dal GTFS grezzo (XVIII Dicembre 894 corse/giorno, Vittorio Veneto 712,
  XVIII Dicembre 627 — ordini di grandezza corretti); (4) buon senso OK su Corso Francia (20 pass/h
  punta sul tratto migliore), Corso Vittorio Emanuele II (40), Corso Giulio Cesare (32), via Nizza
  (13); (5) corridoi di Torino con passaggi ma **senza fermata entro 150 m: solo 5** (163-263 m:
  Piazza Muzio Scevola, Ponte Pietro Secondo, Viale Dogali, Corso Federico Sclopis, via Gramsci).
- `metro_vicina`: 337 corridoi; `ferrovia_vicina`: 2.136 (linee in galleria del passante escluse).

## 4. Pacchetto C — pubblicazione del traffico (script 53)

`data/processed/traffico_stimato_finale_v2.json` (**il file della Fase 3 non è stato toccato**).

- Variante **V0**; taratura k = 1,7215.
- **Accuratezza dichiarata dei numeri assoluti:** in metà dei casi lo scarto è entro **±32%**;
  9 volte su 10 entro **±59%**. Per i corridoi in estrapolazione (flusso modello fuori
  dall'intervallo dei sensori) la fascia è **allargata ×2: ±64% / ±119%** (valore dichiarato).
  In estrapolazione: 9.611 corridoi totali, di cui **752** nell'universo di Torino.
- **Universo di Torino:** 872 corridoi, **1.300,5 km**, mediana 1.029 veic/giorno.
  **Prima cintura:** 574 corridoi, 756,4 km.
- **Soglie "alto/medio/basso" ricalcolate dentro l'universo di Torino** (terzili): medio da 549,
  alto da 2.190 veicoli/giorno (non più da 1.520 come su tutti i 10.743 corridoi).
- Ogni corridoio ha: `veic_giorno` con `stimato/misurato`, `fascia_50`, `fascia_90`,
  `estrapolazione`, `affidabile`, `classe_esito`, `indice_1_5`, `rapporto_su_mediana_torino`,
  `posizione_torino`, `posizione_cintura`, `classe3`.
- I 10 corridoi di Torino con più traffico stimato: Corso Unità d'Italia 80.946 (MISURATO),
  Corso Germano Sommeiller 53.635, Sottopasso Michele Lanza 53.378, Corso Palermo 48.158,
  Sottopasso Repubblica 41.046, Ponte Umberto I 37.715, Via Valperga di Caluso 29.886,
  Corso San Maurizio 29.258, Corso Massimo d'Azeglio 29.158, Corso Giulio Cesare 28.846 (MISURATO).

## 5. Pacchetto D — incrocio traffico × trasporto pubblico (script 54)

`data/processed/risultato8_traffico_tp.json`, `docs/RAPPORTO_RISULTATO8_TRAFFICO_TP.txt`.

- Universo di Torino: **872 corridoi**. Molto traffico (quarto più alto, ≥3.148 veic/g):
  **218**. Poco TP (quarto più basso di passaggi/ora in punta, **= 0**, senza metro né ferrovia
  vicina): **319**. Gruppo **"da guardare" (molto traffico e poco TP): 23**.
- **Robusti** all'incertezza del traffico (±35%): **12** su 23. Stabili alle 3 definizioni
  (quartili, terzili, punta sera): **23** (il "poco TP" è 0 in tutti i casi, quindi non cambia).
- **Controllo del piano:** la lista non è dominata da strade di bordo (già escluse perché non
  affidabili), né da strade < 300 m (già escluse), **ma 4 dei 23 sono ponti/sottopassi**
  (Sottopasso Michele Lanza, Ponte Umberto I, Ponte Diga, Sottopasso Mina-Grosseto): **esclusi
  dalla presentazione e dichiarati**. Restano **19 corridoi** in 19 vie diverse.
- **I 10 assi di Torino con più traffico e meno TP (ponti/sottopassi esclusi):**

| # | asse | veic/giorno | fascia 50% | pass/h in punta | linee |
|---|---|---|---|---|---|
| 1 | Corso Cairoli | 28.554 | ±32% | 0,0 | 2 |
| 2 | Via Giovanni Pierluigi da Palestrina | 28.536 | ±32% | 0,0 | 0 |
| 3 | Via Tommaso Agudio | 14.366 | ±32% | 0,0 | 0 |
| 4 | Corso Cosenza | 13.492 | ±32% | 0,0 | 0 |
| 5 | Via San Massimo | 11.744 | ±32% | 0,0 | 0 |
| 6 | Via Pollenzo | 7.484 | ±32% | 0,0 | 0 |
| 7 | Via Pasquale Paoli | 6.387 | ±64% | 0,0 | 0 |
| 8 | Corso Don Luigi Sturzo | 5.417 | ±64% | 0,0 | 0 |
| 9 | Via Quarto dei Mille | 5.399 | ±64% | 0,0 | 0 |
| 10 | Via Rivalta | 5.077 | ±64% | 0,0 | 0 |

- **Prima cintura:** **28** corridoi "da guardare" (i primi: Via Leinì a Settimo 15.711, Via Luigi
  Tenco a Nichelino 10.950, Via Italia a San Mauro 10.480, Via Santhià a Nichelino 9.742,
  Via Assietta a Collegno 9.263).
- **Controllo di buon senso su strade note:** tutte le arterie note sono "molto traffico ma TP ok"
  (Corso Giulio Cesare 32 pass/h, Corso Regina Margherita 33, Corso Unione Sovietica 34,
  Corso Sebastopoli 22,5, Corso Casale 29,5, Corso Trapani 13, via Nizza 13, Corso Vittorio
  Emanuele II 40, Corso Lecce 11): la lista **non** contiene gli assi di forza del trasporto pubblico.
  Dove la lista sembra strana: "Corso Cairoli", "Via Giovanni Pierluigi da Palestrina" e altre vie
  del centro hanno 0 passaggi ma sono interne/cortissime; il valore di traffico alto è in parte
  l'effetto della concentrazione del modello V0 sul centro (limite noto). Da indagare a mano.

## 6. Pacchetto E — verifica del raccoglitore corretto

**FERMO.** Il piano prevede che Leo incolli le ultime righe di `logs\aggiorna_raccolta_5t_codici.log`
(`active`, `sensori nell'ultimo istante: 112`, `codici ~2 con dati: 3/3`) e poi il fetch di
**lunedì 19/10**. Controllo già possibile sul PC: il database copiato
`data/storico_backup.sqlite` ha ancora **109 sensori e 0 codici `~2`** → la correzione non è
ancora arrivata sul PC. Non ho toccato nulla sul Pi. Da rifare dopo il 19/10 (e dopo il 25/10
per le ore locali, fine dell'ora legale).

## 7. Verifiche indipendenti (sezione 8 del piano) — `scripts/55_verifiche_fase4.py`

`docs/RAPPORTO_TRAFFICO_FASE4_VERIFICHE.txt` — **esito: TUTTE LE VERIFICHE OK**.
1. Totali corse bus/tram: ricalcolati con pandas (metodo diverso dal 51) = **13.158 identici (0)**.
2. Fattore di taratura ricalcolato a mano: **1,721511 coincide**; 3 errori leave-one-out
   ricalcolati a mano coincidono con lo script.
3. 5 corridoi riletti dai tratti al valore finale pubblicato: tutti coerenti (k=1,7215).
4. `git status`: **nessun commit**; `MEMORIA_PROGETTO.md` e `scripts/mappa_template.html` erano
   **già** modificati prima di questa sessione (come scritto in Fase 3); `04_genera_mappa.py` intatto.
5. Pacchetto B: solo 5 corridoi di Torino con passaggi ma senza fermata entro 150 m.

## 8. Anomalie e limiti (da dire chiaramente)

1. **Il risultato è debole.** Classe `C-DEBole`, errore mediano 31,9%, rho 0,602, e l'intervallo
   al 90% dell'errore (23,7%-40,2%) attraversa la soglia del 35%: **la stima puntuale è incerta**.
   I numeri assoluti servono a ordinare, non a contare i veicoli.
2. **V3 non migliora V0**: la congestione è troppo debole (v/c medio 0,40) e il controllo sui tempi
   di viaggio (Castello→Collegno) non è rispettato (13,3 min contro 20-35 attesi).
   Migliorerebbe solo togliendo la congestione (rho 0,617), ma la regola del piano non consente di
   scegliere un'ablazione.
3. **Il gruppo "da guardare" è piccolo e in parte fragile**: 23 corridoi, di cui 4 strutture;
   solo 12 restano "molto traffico" con il traffico ridotto del 35%. Il "poco TP" è quasi sempre
   **zero passaggi**: strade senza nessun bus, non strade con pochi bus.
4. **Traffico concentrato sul centro** (difetto V0): alcuni valori alti del centro (Corso Cairoli
   ecc.) sono probabilmente gonfiati; i valori sui tratti di bordo restano non affidabili ed esclusi.
5. **TP = orario programmato** (GTFS): non tiene conto di ritardi, capienza, affollamento;
   nessuna misura dei passeggeri. Il map matching sbaglia su ~7% delle corse (non contate).
6. Sensori 5T a un solo verso (punta del traffico non stimata); restano i 3 codici `lcd1` condivisi
   (pacchetto H pronto, non ancora attivo); ora locale 1 = dato mancante.

## 9. Durate

| Attività | Durata |
|---|---|
| Pacchetto B (51, 52, correzioni e controlli) | ~35 min |
| Pacchetto A: 49 (attrattori/domanda) | 14 s |
| Pacchetto A: 50 V3 principale (10 iter. MSA + giorno + corridoi) | **~27 min** |
| Pacchetto A: ablazione 2 (senza congestione) | ~4 min |
| Pacchetto A: ablazione 1 (senza attrattori, 6 iter.) | ~7 min |
| Pacchetto A: ablazione 3 (senza porte ristrette, 6 iter.) | ~19 min |
| Pacchetto A: 50b valutazione | ~2 min |
| Pacchetti C, D, verifiche 55 | ~8 min |
| **Totale sessione** | **~1 h 50 min** (12:14 → 13:20 circa) |

## 10. File creati / modificati

**Script nuovi:** `49_v3_punti_domanda.py`, `50_v3_assegnazione.py`, `50b_v3_valutazione.py`,
`51_tp_gtfs_tratti.py`, `52_tp_corridoi.py`, `53_pubblicazione_traffico.py`,
`54_incrocio_traffico_tp.py`, `55_verifiche_fase4.py`.
**Script/bat modificato:** `TRAFFICO_RILANCIA_SENSORI.bat` (copia `.bak_17ott`; aggiunti 50b, 53, 54).
**Nuovo bat:** `V3_MODELLO.bat` (calcolo lungo, ripartibile, log in `logs\v3_modello.log`).
**Dati nuovi:** `data/processed/traffico_c/v3/` (`punti_v3.json`, `porte_v3.json`, `domanda_v3.json`,
`archi_flusso_v3.npz`, `corridoi_v3.json`, `riepilogo.json`, `msa_stato.npz`, `valutazione_v3.json`),
`v3_abl1/`, `v3_abl2/`, `v3_abl3/`, `data/processed/traffico_c/tp_conteggi.npz`, `tp_tratti.csv`,
`data/processed/tp_corridoi.json`, `data/processed/traffico_stimato_finale_v2.json`,
`data/processed/risultato8_traffico_tp.json`.
**Rapporti nuovi in `docs/`:** `ESITO_FASE4_TRAFFICO.md`, `RAPPORTO_TP_PER_STRADA.txt`,
`RAPPORTO_TRAFFICO_C_V3.txt`, `RAPPORTO_TRAFFICO_C_V2.txt`, `RAPPORTO_RISULTATO8_TRAFFICO_TP.txt`,
`RAPPORTO_TRAFFICO_FASE4_VERIFICHE.txt`.
**Non toccati:** `MEMORIA_PROGETTO.md`, `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`,
`data/raw/*`, `data/storico_backup.sqlite`, tutti i dati della Fase 3. **Nessun commit.**
**Pacchetti Python:** nessuno installato (già presenti numpy, scipy, pandas, shapely, networkx).

## 11. Testo proposto per MEMORIA_PROGETTO.md (non l'ho modificata)

> | Traffico 5T, Fase 3-bis + Fase 4 (49-55) | **17/10.** **Fase 3-bis (V3):** destinazioni per attrattori + congestione (MSA/BPR) + porte di rango ≥3. Valutato UNA volta con i criteri della Fase 3: rho 0,573 e errore mediano 29,0%, **peggio di V0 quanto a correlazione** (0,602) → **resta V0** (regola fissata). La diagnostica dice che contano gli attrattori (senza: rho 0,559) e NON la congestione (senza: rho 0,617). **Fase 4:** offerta bus/tram dal GTFS (giorno tipico 14/10/2026, 13.158 corse, **93,1% agganciate** alla rete) → `data/processed/tp_corridoi.json`; pubblicazione del traffico con numeri assoluti+fascia (±32% metà dei casi, ±59% 9 su 10; estrapolazioni ×2), relativi e graduatoria → `data/processed/traffico_stimato_finale_v2.json` (universo Torino: 872 corridoi / 1.300 km; cintura 574 / 756 km); **incrocio traffico × TP** → **23 corridoi "molto traffico e poco TP" (12 robusti; 4 ponti/sottopassi esclusi)** in `data/processed/risultato8_traffico_tp.json`. Controllo raccoglitore (112 sensori): **da fare dopo il fetch del 19/10**. Dettagli: `docs/ESITO_FASE4_TRAFFICO.md`, `docs/RAPPORTO_RISULTATO8_TRAFFICO_TP.txt`.

## 12. Passo successivo suggerito

1. **Raccolta:** far partire/verificare il raccoglitore corretto (pacchetto E) e dopo il fetch del
   **19/10** rilanciare `scripts\TRAFFICO_RILANCIA_SENSORI.bat` (ora esegue anche 50b, 53, 54).
2. **Mappa (solo se Leo la chiede):** colorare i corridoi per `veic_giorno` con fascia e segnare
   il gruppo "da guardare".
3. **Se in futuro si vuole un modello migliore:** la strada giusta è **rendere realistica la
   congestione** (capacità/corsie da OSM, domanda per ora con riassegnazione, più origine-destinazione),
   non gli attrattori (che pure aiutano). Ma i criteri di riuscita restano quelli fissati.
