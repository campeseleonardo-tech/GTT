# Piano — Pulizia completa del progetto e nuovo ordine dei prossimi passi (20/10/2026)

Scritto da Claude su richiesta di Leo, dopo le correzioni generali.

> **Stato (20/10, sera).** Risposte di Leo: superati **in archivio** (non cancellati); portfolio su **GitHub Pages**;
> campo **ridotto** (via bici, telefonia, logistica, eventi; uno solo fra R3 e R5). **Già fatto** da Claude: 2.1 tranne
> il R6 vecchio, 2.2, 2.3 tranne le voci «dopo l'esito», `immagini/` in `.gitignore`, testate dei piani, memoria
> (sezioni 5 e 6). **Da fare dopo l'esito**: R6 vecchio (74-78, 80) e documenti delle correzioni in archivio, 2.5
> (template e `simulazione.html`, che l'agente può aver toccato), memoria riscritta corta.

## 0. Cosa ho guardato e cosa no

- Ho letto memoria, `AGENTS.md`, i documenti in `docs/`, tutti gli script e i `.bat`, e ho ricostruito chi legge e
  chi scrive ogni file (catene del Risultato 6, mappa, schede, traffico, raccolta sul Pi).
- **Non ho l'esito delle correzioni**: `docs/ESITO_CORREZIONI_GENERALI.md` non è su GitHub (l'agente sul PC non
  doveva fare commit). Non so quindi se la catena nuova del Risultato 6 (81-85) ha girato bene sui dati veri.
  Per questo le parti che dipendono dall'esito sono segnate **[dopo l'esito]**.
- Non ho `data/` né il PC: in git c'è ancora la mappa **vecchia** (23,6 MB); quella nuova (~13 MB) è solo sul PC.

## 1. La situazione in breve

| | Quanti | Davvero usati oggi | Superati o usati una volta sola |
|---|---|---|---|
| Script Python | 95 | 80 | 15 |
| `.bat` / `.sh` / `.ps1` | 25 | 19 | 6 (5 superati + 2 quasi uguali da unire) |
| Documenti in `docs/` (fuori archivio) | 61 | 11 note + ~34 rapporti riscritti dagli script | ~16 |

Il problema principale non è il numero dei file ma che **le cose vive e quelle superate stanno mescolate**:
in `docs/` 16 documenti scritti a mano sono in mezzo a 44 rapporti generati; in `scripts/` gli script del
Risultato 6 «vecchio» (74-78, 80) stanno accanto a quelli nuovi (81-85) senza nessun segno che non servono più;
quattro piani dicono ancora «da fare» per lavori già finiti.

## 2. Proposta di pulizia (nessun numero cambia)

Default (come finora): **spostare in archivio, non cancellare**. Git tiene comunque tutta la storia.

### 2.1 Script superati → `scripts/archivio/`

| Script | Perché è superato | Controllato che nessuno lo usa? |
|---|---|---|
| 74 `istat2011_auto_orari`, 75 `risultato6_v2`, 76 `verifiche_r6v2`, 77 `strade_comuni`, 78 `eventi_parcheggi`, 80 `porte_interscambio` | Risultato 6 prima delle correzioni; sostituiti da 81-85 | Sì: la catena nuova (`RISULTATO6_RIFAI.bat`) non li lancia; 83 legge `scenari.json` del 75 **solo se c'è** (confronto) e l'84 riscrive `porte.json` al posto dell'80. **[dopo l'esito]** |
| `calcola_simulazione.py` + `scenario_esempio.json` | Simulatore generico, escluso il 9/10 | Sì: 28 ne ha solo copiato una funzione |
| 02 `ispeziona_dati`, 09 `analisi_dati_diurni` | Controlli dei primi giorni (3-10/10); con il 02 va in archivio anche `RAPPORTO_ISPEZIONE.txt` | Sì |
| 38 `verifica_provinciali`, 46 `verifica_5t_codici`, 47 `prova_raccolta_5t_su_copia`, 48 `verifiche_indipendenti`, 55 `verifiche_fase4`, `controllo_fase1_5t` | Verifiche fatte una volta durante le fasi del traffico | Sì: non sono nei `.bat` settimanali |

**Restano** (e perché, visto che sembrano vecchi): 25 (il Risultato 6 v1 produce `risultato6_interscambio.json`,
che 72 e 73 leggono ancora); 06 e `supervisore.py` (girano sul Pi); i passi delle fasi 3-4 del traffico (37, 43-45,
50b, 53-54: la Fase 5 legge le loro uscite) e 49-50, 62 (modelli V3 e V4 scartati, ma servono ai confronti
settimanali dello script 63). Il traffico non lo tocco.

### 2.2 `.bat` → `scripts/archivio/` o uniti

| Cosa | Proposta |
|---|---|
| `backup_da_leopi.bat` | Archivio: fa esattamente la prima metà di `FETCH_LEOPI_E_VELOCITA_5T.bat` (rischio di lanciare quello sbagliato) |
| `verifica_ritardi_diurna.bat` | Archivio: controllo di un giorno solo (11/10, data scritta dentro) |
| `V3_MODELLO.bat` | Archivio: modello V3 scartato, già calcolato |
| `RAPPORTO_PILOTA.bat`, `RAPPORTO_CONTROLLA.bat` | Archivio: servivano a mettere a punto l'estrazione del rapporto GTT, finita. `RAPPORTO_1/2/3` restano |
| `aggiorna_raccolta_leopi.bat` + `AGGIORNA_RACCOLTA_5T_CODICI.bat` | Quasi uguali (copiano il raccoglitore sul Pi e lo riavviano). Uno solo, `AGGIORNA_RACCOLTA_LEOPI.bat`, che fa la copia di sicurezza con la data nel nome e lancia entrambi i controlli |
| `sync_da_leopi.bat` | **Resta**: non è un doppione (copia `stat.js` e `replay_*.js` che la mappa usa) |

### 2.3 Documenti

**Restano in `docs/`** (le note vive): `FONTI_DATI.md`, `CONOSCENZA_TORINO_LEO.md`, `PIANO_ACCESSIBILITA.md`,
`PIANO_RISULTATO2.md`, `PIANO_RISULTATO4.md`, `PIANO_RISULTATO6.md`, `PIANO_RISULTATO9_ATTESA.md`,
`RIASSUNTO_TRAFFICO.md`, `RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`, `PIANO_COSTI.md`, questo piano.

**In archivio**:

| Cosa | Dove |
|---|---|
| `ANALISI_PROGETTO.md`, `ANALISI_RISULTATO6.md`, `PIANO_CORREZIONI_GENERALI.md`, `ESITO_CORREZIONI_GENERALI.md` **[dopo l'esito]** | `docs/archivio/correzioni_20ott/` |
| `RAPPORTO_RISULTATO6_V2.txt`, `RAPPORTO_R6V2_EVENTI/ISTAT2011/STRADE/VERIFICHE/MAPPA_DATI.txt` (scritti da 74-78, 80) | `docs/archivio/r6/` |
| `PIANO_REVISIONE_MAPPA.md` (fatta il 18/10), `PIANO_RAPPORTO_SOSTENIBILITA.md` (fatto), `RAPPORTO_COLORI.txt` (sostituzioni fatte il 19/10), `RAPPORTO_RISULTATO4_v1.txt`, `RAPPORTO_ISPEZIONE.txt` (script 02) | `docs/archivio/` |

`RAPPORTO_VELOCITA_5T_prima_fetch.txt` **resta**: lo riscrive `FETCH_LEOPI_E_VELOCITA_5T.bat` a ogni fetch (copia di
confronto della settimana prima).
| `richiesta_dati_telefonia.md` (bozza mai inviata) | `docs/archivio/idee/` (o la tieni tu fuori dal progetto) |

**Rapporti generati in una cartella loro** (facoltativo, vedi domanda 2): i ~34 `RAPPORTO_*.txt` che gli script
riscrivono a ogni giro in `docs/rapporti/`. Così `docs/` ha solo le ~11 note scritte a mano. Costo: cambiare
il percorso di uscita in ~40 script (una riga ciascuno, la stessa) e i rimandi nei documenti.

**Testate sbagliate da correggere** (dicono «da fare» per lavori finiti): `PIANO_ACCESSIBILITA.md` («prossimo
passo: fase 0»), `PIANO_RISULTATO9_ATTESA.md` («da approvare»), `PIANO_RISULTATO4.md` (scritto «per un agente»,
senza lo stato attuale in testa). Una riga «Stato al 20/10» in cima a ciascuno.

### 2.4 Git

| Cosa | Problema | Proposta |
|---|---|---|
| `immagini/` | **Non è in `.gitignore`**, anche se il piano diceva di sì: gli screenshot di `prova_pagine_r6.py` finirebbero nel prossimo commit | Aggiungerla a `.gitignore` (sicuro, lo farei subito) |
| `mappa_torino.html` | 23,6 MB rigenerati e salvati a ogni giro (10 volte) | Leo ha scelto GitHub Pages: le pagine pubblicate devono stare in git. Si decide la cartella al passo «Pubblicare» (per esempio `pubblica/` tolta da `.gitignore` e salvata solo quando si pubblica; la mappa di lavoro nella radice fuori da git) |
| `data/processed/vulnerabilita*.json` | 4 MB in git nonostante `data/` sia escluso | Toglierli da git **sul PC** con `git rm --cached data/processed/vulnerabilita*.json` e commit: se lo facessi io, al pull git li **cancellerebbe** dal PC |
| `requirements.txt` | Senza versioni | Le scrive il passo 0.5 delle correzioni **[dopo l'esito]** |

### 2.5 Codice (piccolo, sicuro)

- `mappa_template.html`: 57 commenti tipo `[agente GT05-pendolari]` (e 6 in `04_genera_mappa.py`): sono note di
  lavorazione, per chi legge il codice del portfolio sembrano disordine. Toglierli o ridurli a un commento normale.
- `simulazione.html`: c'è ancora la zona «trascina qui i file JSON» e il codice del vecchio formato «scenario»
  di `calcola_simulazione.py`. Toglierli; poi `prova_pagine_r6.py` per vedere che la pagina funziona.
- `66_pubblicazione_incrocio.py`: due commenti con accenti rovinati («piÃ¹»). Solo testo.
- Funzioni copiate (distanze in 22 script, `trova_radice` in 46): **non** rifare tutto adesso (rischio alto, nessun
  numero cambia). Regola: chi tocca uno script per altri motivi passa a `comuni.py`.
- Script del traffico settimanale con numeri attesi «di oggi» (35: 17 esclusi / 92 usabili; 36; 38b: 112 voci):
  oggi stampano «NON TORNANO» ma non fermano la catena. Lasciati: si guardano nel log.

### 2.6 Memoria **[dopo l'esito]**

`MEMORIA_PROGETTO.md` va riscritta corta: la sezione 5 (correzioni in corso) diventa una riga in FATTO con i
numeri nuovi del Risultato 6; il lungo elenco «Trovati da Claude» della sezione 7 va in archivio con le analisi
(resta solo quello che è ancora un limite vero); le «piccole pulizie» (file `3)`, `*.bak_18ott`) si chiudono;
l'elenco degli script nella sezione 3 segue la nuova divisione.

## 3. Come la eseguirei (un passo alla volta)

1. **[dopo l'esito]** Leggo `docs/ESITO_CORREZIONI_GENERALI.md`, ricontrollo i numeri, aggiorno il Risultato 6 nella
   memoria e in `PIANO_RISULTATO6.md`.
2. Spostamenti (2.1-2.3) con `git mv`, così la storia di ogni file resta collegata. Controllo con una ricerca che
   nessuno script, `.bat` o pagina citi più un file spostato.
3. `.gitignore` e git (2.4), solo per le voci che approvi.
4. Codice (2.5). Prova: `python -m py_compile` su tutti gli script; tu lanci `scripts\RISULTATO6_RIFAI.bat` sul PC
   (deve finire con `FATTO` e 0 errori nelle pagine).
5. Memoria riscritta (2.6), commit sul ramo di lavoro quando dici tu.

## 4. Prossimi passi, nuovo ordine (dal più rilevante)

Criterio: prima quello che **scade** o **blocca**, poi quello che rende il portfolio **visibile**, poi quello che lo
rende **più forte**, poi il nuovo.

| # | Cosa | Perché ora | Quanto |
|---|---|---|---|
| 1 | **Chiudere le correzioni**: esito, ricontrollo, memoria | Blocca tutto il resto del Risultato 6 | 1 sessione |
| 2 | **Ora legale del 25/10** (domenica): controllo a mano dello script 26 dopo il fetch del 1/11 | Scade questa settimana; altrimenti un'ora di dati 5T fuori posto per sempre | 15 min |
| 3 | **Pulizia** (questo piano) | Il progetto è difficile da leggere, anche per gli agenti | 1 sessione |
| 4 | **Controllo automatico di leopi ogni mattina** (`schtasks`, già scritto) | Il 18/10 la raccolta si è fermata e ce ne siamo accorti dopo | 5 min (tu) |
| 5 | **Pubblicare il portfolio**: dove (domanda 3), condizioni d'uso degli sfondi Esri, README, prova di `pubblica/` | Senza questo nessuno vede il lavoro | 1-2 sessioni |
| 6 | **2-3 risultati di punta + «come sappiamo che è vero»** per ciascuno, con i dati che ci sono già (rapporto GTT 2025, sensori 5T, parcheggi 5T, la tua conoscenza) | È la cosa che oggi manca di più per la credibilità | 1 sessione a risultato |
| 7 | **Rilanciare R4 e R9 con un mese di dati** (metà novembre) e R6 con ≥ 5 feriali di parcheggi (inizio novembre); poi R4 in mappa | Oggi sono su 1-2 settimane | `.bat` già pronti |
| 8 | **Tempi TP contro auto per coppie di zone** | Base comune per «auto in meno» e costi del viaggio | 2-3 sessioni |
| 9 | **Costi del viaggio** (`PIANO_COSTI.md`) | Dopo il punto 8 | da stimare |
| 10 | Più avanti: treni SFM (GTFS regionale: servono a R6 e alla cintura), lista dei luoghi «speciali», effetto ZTL, Corso Moncalieri, mappa del traffico | Utili ma non urgenti | — |

**Da togliere o congelare** (proposta, domanda 4): Risultato 7 bici (nessun dato), richiesta dati telefonia,
logistica, eventi (stadi/palazzetti). Dei due scenari rimasti (3 «più passaggi su una linea», 5 «linea nuova») ne
terrei **uno**, dopo i punti 1-7: l'obiettivo dice «pochi scenari», e il Risultato 2 ne è già uno.

## 5. Cose da sapere

- Lavoro su un ramo mio (`claude/zen-newton-brrak9`), uguale a `prova` all'inizio. Non tocco `prova`.
- `.claude/launch.json` (citato nella memoria) non è in git: esiste solo sul PC.

## 6. Domande per Leo

1. Mi mandi l'esito? (commit e push di `docs/ESITO_CORREZIONI_GENERALI.md` su `prova`, o incollalo in chat)
2. File superati: **archivio** (come finora) o **cancellazione** (git li tiene nella storia)? E i rapporti
   generati in `docs/rapporti/`?
3. Dove vuoi pubblicare il portfolio (cambia cosa tenere in git)?
4. Va bene togliere bici, telefonia, logistica ed eventi, e tenere un solo scenario fra 3 e 5?
