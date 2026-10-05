# Come funziona l'Ufficio: spiegazione completa

Scritto il 05/10/2026 leggendo la copia su GitHub (`ufficio/` e `progetti/`). Nessun file esistente è stato modificato.

**Come leggere questo documento**
- **[visto]**: l'ho letto nel codice o nei file, con file e riga.
- **[ipotesi]**: è una mia deduzione e va controllata sul PC.
- I numeri di riga valgono per la copia del 05/10/2026 alle 16:41.
- Le parole tecniche sono spiegate la prima volta che compaiono.

**Limiti di questa lettura**
- Il PC non l'ho visto. Conosco solo la copia caricata su GitHub.
- Dei repository dei progetti ho solo il ramo attivo, senza la storia. Quello che dico sui rami viene da `RAMI_PROGETTI.md`, `CONTROLLO_REPO.txt` e `PROVA_RAMI.txt`.
- Le cartelle `_backup_v0.*`, `confronto_claude_*`, `pulizia/diff` e i file di dati grandi non li ho letti. So solo cosa sono.

---

## 1. In una pagina

**Cosa fa l'Ufficio.** È un programma che gira sul PC di Leo. Fa lavorare dei modelli di intelligenza artificiale ("agenti") su piccoli lavori ("task") dei suoi progetti. Lavora un solo agente alla volta, anche quando il pannello è chiuso.

**Il percorso di una task, dall'idea al risultato:**

1. **Chi la crea.** Ci sono 5 modi:
   - Leo dal pannello, con il pulsante Nuova task (`ufficio_dati.py:620` `task_nuova`);
   - la chat del pannello, che propone l'azione `nuova_task` e Leo la conferma (`ufficio_extra.py:236`);
   - un agente "Consigli", che propone task che poi Leo approva (`scheda.py:290`);
   - una risposta di Leo a una domanda: se è diversa dalla scelta provvisoria dell'agente, parte da sola una task di correzione `XX-rispostaN` (`ufficio_dati.py:923`);
   - a mano, scrivendo un file `.task.md`.
2. **Dove va in coda.** Ogni task è un file `generico/queue/<id>.task.md`. In alto ci sono i campi (progetto, ramo, file permessi, controlli...), poi una riga `---`, poi le istruzioni per l'agente. Le candidature invece hanno la loro coda dentro `candidature/stato/stato.json`.
3. **Chi decide quando parte.** Il **dispatcher** (`dispatcher.py`). È un programma che parte ogni 5 minuti da un'attività di Windows (`UfficioAgenti`). Lo fa partire anche il pannello, ogni minuto e dopo ogni azione (`pannello_server.py:309`).
   - Sceglie un lavoro alla volta, con la **rotazione 3-2-1**: priorità alta 3 turni, media 2, bassa 1 (`dispatcher.py:134`).
   - Si ferma se c'è il limite di Claude, se il contatore d'uso è al 100% o se un altro agente sta lavorando (`comune.py:173`).
4. **Chi la esegue.** Il dispatcher lancia `generico/runner.py --task <id>`, oppure `candidature/runner/runner.py job <id>`. Per un progetto con git, il runner (`runner.py:261`) fa questi passi:
   - passa al ramo git della task, o lo crea (`repo_tools.py:54`). Un **ramo** è una copia parallela del progetto, dove si lavora senza toccare la versione principale;
   - salva lo stato di partenza;
   - fa lavorare l'agente;
   - controlla che l'agente abbia toccato solo i file permessi;
   - esegue i **controlli** (piccoli test automatici scritti nella task). Se falliscono, richiama l'agente fino a 2-3 volte per correggere;
   - fa un commit (un salvataggio git) e sposta il file della task in `done/` (fatte), `failed/` (fallite), `blocked/` (domande) o `incomplete/` (interrotte).
5. **Con quale modello.** Lo decide `motore_di` (`runner.py:401`), in quest'ordine: il campo `motore:` della task, poi quello del progetto, poi il predefinito nelle Impostazioni (oggi `gratis`). Tutte le chiamate passano da `motori.py` (dettagli nella sezione 3).
6. **Dove finisce il risultato.**
   - **Nel progetto:** i file cambiati, più la cartella `agenti/<id>/`. Dentro ci sono RAPPORTO.md (scritto dall'agente), RUNNER.md, VALIDATORE.md, DIFF.patch e a volte DOMANDE.md e DECISIONS.md. In più si aggiunge una riga in `agenti/LOG.md`.
   - **Nell'Ufficio:** `generico/results/<id>/` (risposta grezza, riassunto, log del validatore), una riga in `logs/uso.csv` per ogni chiamata, una riga in `diario.jsonl` e le domande in `domande.jsonl`.
7. **Come la vede Leo.** Nel pannello (`http://127.0.0.1:8765`, pagina `ufficio.html`):
   - "Cosa succede", il diario, le domande e "Da sistemare";
   - il dettaglio della task (`/api/task2`);
   - la scheda del progetto, aggiornata dopo ogni task.
   Per provare il lavoro, Leo lancia `pulizia/CREA_PROVA.bat`: unisce i rami buoni in un ramo `prova` di ogni progetto.

**Schema:**
```
Leo / chat / Consigli / risposta a domanda
        │  crea file .task.md
        ▼
generico/queue/  ──(ogni 5 min)──►  dispatcher.py  ──►  generico/runner.py --task X
                                        │                    │ ramo git X nel progetto
                                        │                    │ motori.py → Claude o modelli gratis
                                        │                    │ controlli, commit, sposta il file task
                                        ▼                    ▼
                         diario.jsonl, domande.jsonl     progetto/agenti/X/*, logs/uso.csv
                                        │
                                        ▼
                         scheda progetto riscritta (parte "STATO DELL'UFFICIO")
                                        ▼
                                 pannello (ufficio.html)
```

---

## 2. Mappa dei file dell'Ufficio

Legenda: **VIVO** = usato oggi · **VECCHIO** = non più usato · **DOPPIONE** = la stessa cosa è fatta anche altrove · **DUBBIO** = forse usato, da decidere.

### Avvio e installazione
| File | A cosa serve | Chi lo usa | Stato |
|---|---|---|---|
| `INSTALLA_UFFICIO.bat` + `.ps1` | Crea l'icona sul desktop, `Ufficio.vbs` e l'attività di Windows "UfficioAgenti" (ogni 5 minuti) | Leo, una volta sola | VIVO |
| `Ufficio.vbs` | Apre il pannello senza la finestra nera | icona sul desktop, `run.bat` | VIVO. I percorsi sono scritti fissi (`C:\Users\campe\...`) |
| `run.bat` | Apre il pannello. Se `Ufficio.vbs` manca, usa il vecchio modo | Leo | VIVO |
| `LEGGIMI.txt` (e quelli in `generico/`, `pannello/`, `progetti/`) | Spiegazioni | Leo | VIVO, ma in parte superato. Esempio: dice che `motori.py` ha "oggi solo Claude" |
| `PIANO_v0.5.md` | Il piano delle fasi A, B e C | Leo | VECCHIO in parte. Prevede "il gratuito, poi Claude come ultima spiaggia": oggi Leo vuole il contrario |
| `Claude outputs/` (passaggio di consegne, prototipo html) | Documenti per altre chat | — | VECCHIO |

### Nucleo
| File | A cosa serve | Chi lo usa | Stato |
|---|---|---|---|
| `motori.py` | L'unico punto da cui passano le chiamate ai modelli. Tiene il log dei consumi `logs/uso.csv`, le chiavi, gli elenchi dei modelli gratis, i "fornitori" (Gemini, Cerebras, Groq, Mistral) e la scrittura dei file per i modelli "a colpo singolo" | runner, candidature, pannello | VIVO. Dentro ci sono parti vecchie: `MODELLO_GRATIS` (riga 535, usato solo dalla Prova OpenRouter, riga 1164), la migrazione `_migra` dei 3 log vecchi (riga 382, ormai inutile), il commento iniziale superato |
| `comune.py` | Regole comuni: un agente alla volta, limite di Claude, contatore delle ultime 5 ore | runner, dispatcher, pannello | VIVO. `pulizia_avvio` (riga 126) è una pulizia del 04/10 scritta fissa nel codice: VECCHIO |
| `dispatcher.py` | Sceglie e lancia i lavori, scrive diario e domande | attività di Windows, pannello | VIVO. Carica `runner.py` 3 volte per scrivere il diario (righe 243, 256, 79): spreco, non un errore |
| `scheda.py` | La scheda del progetto (PROGETTO.md / MEMORIA_PROGETTO.md / altro file). Crea le task Consigli e Revisione e legge i loro risultati | dispatcher, runner, pannello | VIVO |
| `rotazione.json` | La memoria della rotazione 3-2-1 e dei lavori messi "in cima" | dispatcher | VIVO |
| `diario.jsonl`, `domande.jsonl` | Vedi sezione 4 | — | VIVO |
| `.diario_ricostruito` | Segno che il diario è già stato ricostruito una volta | `ufficio_dati.diario` | VIVO, ma il codice che lo usa (`_backfill`, `ufficio_dati.py:225`) è VECCHIO |
| `dispatcher.log`, `dispatcher_ultimo_output.txt` | Log del dispatcher e output dell'ultimo lavoro | Leo, se serve | VIVO |
| `logs/uso.csv` | Il log unico dei consumi | tutti | VIVO |
| `logs/modelli_gratis.json`, `logs/modelli_fornitori2.json` | Elenchi dei modelli, aggiornati ogni 6 ore, con i modelli "scartati" | `motori.py` | VIVO |
| `logs/modelli_fornitori.json` | Elenco vecchio. Il codice usa il file "2" | nessuno | VECCHIO |
| `logs/dispatcher_stato.json`, `logs/in_corso/`, `logs/calibrazione.jsonl` | Ultima decisione del dispatcher, chiamate in corso, i % letti da Claude | pannello | VIVO |

### generico/ (task dei progetti)
| File o cartella | A cosa serve | Stato |
|---|---|---|
| `runner.py` | Esegue una task (sezione 1) | VIVO. Il commento iniziale parla di "runner notturno" e di finestre orarie: superato |
| `repo_tools.py` | Comandi git, guardia sui file permessi, 19 tipi di controllo | VIVO |
| `queue/ done/ failed/ blocked/ incomplete/ sospesi/ scartate/` | Lo stato di ogni task, cioè la cartella in cui si trova il suo file | VIVO. Oggi: 0 in coda, 71 fatte, 2 fallite, 3 sospese |
| `results/<id>/` | Risposte grezze, riassunto, log del validatore, STOP.json | VIVO (67 cartelle, non si svuota mai) |
| `decisions/` | Domande che fermano una task (DECISIONS.md) | VIVO (2 file rimasti: T20-esegui-b, TL01-progetto-b, ma nessuna task è bloccata: [ipotesi] sono avanzi) |
| `profiles/gtt.md`, `profiles/langue.md` | Regole per gli agenti dei progetti senza scheda | DOPPIONE. Le stesse regole stanno già nella scheda (Langue: `PROGETTO.md` "Regole per gli agenti") |
| `scripts/` (T01, T03, T15, GT09, GT11, `pv/`) | Script Python lanciati da alcune task (0 token) | DUBBIO. Servivano a task già fatte. `pv/genera_preventivo_RIFERIMENTO.py` è anche in `progetti/preventivi/strumenti/`: DOPPIONE |
| `logs/runner.log` | Cosa fa il runner, riga per riga | VIVO |
| `logs/usage.csv` | Log vecchio dei consumi | VECCHIO |
| `failed/T17-prova-gratis.task.md` | T17 è anche in `done/` | DOPPIONE (il pannello tiene la copia più recente) |
| `sospesi/GT14-verifica-passaggi.task.md` | GT14 è anche in `done/` ed è già unita in `prova` | DOPPIONE |

### pannello/
| File | A cosa serve | Stato |
|---|---|---|
| `pannello_server.py` (1557 righe) | Server web locale: risponde alla pagina, esegue le azioni, adattatore delle candidature, chat, meteo | VIVO, ma con molte parti morte (vedi sotto) |
| `ufficio_dati.py` (1239 righe) | Dati e azioni della pagina: task, diario, "Cosa succede", domande, progetti | VIVO |
| `ufficio_extra.py` (632 righe) | Impostazioni, chat, "modifica il pannello" (fatta da Claude su una copia), feedback | VIVO |
| `consumo_dettaglio.py` | Consumo per modello, progetto e periodo | VIVO |
| `task_stop.py` | Pulsante Stop di una task | VIVO |
| `ufficio.html` | La pagina principale | VIVO |
| `mondo.html` + `mondo.js` + `immagini/` (47 MB) | Il "Mondo", la mappa gioco | DUBBIO. Funziona, ma il meteo è spento (`mondo.js:109`) e le immagini pesano molto |
| `pannello_config.json` | Impostazioni | VIVO. Contiene campi morti: `soglia_stop_pct`; `chat_limite_giorno: 20`, che non vale (il codice usa almeno 200, `ufficio_extra.py:172`); `generico_auto`, che non fa niente; `progetti` (un elenco di progetti che DOPPIA `progetti/*.json`) |
| `chat_stato.json`, `chat_log.md`, `feedback.json`, `modifiche_pannello.md` | Memoria della chat e delle modifiche | VIVO |
| `chat_uso.csv` | Log vecchio della chat | VECCHIO (si accorcia ancora da solo, `ufficio_extra.py:617`) |
| `server.log` | Messaggi del server | VIVO |
| `_backup/` | Copia di sicurezza prima dell'ultima modifica fatta dalla chat | VIVO (serve a `RIPRISTINA.bat`) |
| `ripristina.py`, `RIPRISTINA.bat` | Rimettono il backup anche se il pannello non parte | VIVO |
| `8b051b56-...png` (nella cartella principale del pannello) e `immagini/Y5Lrdu*.png` | Immagini originali | VECCHIO (sono già nell'elenco "da spostare", `ufficio_dati.py:960`) |

**Parti morte dentro `pannello_server.py`** [visto]:
- `dispatch_once` (riga 270): nessuno la chiama.
- `generico_loop` (riga 326): nessuno la avvia, quindi l'impostazione `generico_auto` non fa niente.
- `act_add`, `act_approve` e `act_answer`, nella parte per i task "non candidature" (righe 877-885, 913-920, 947-954): scrivono un `task.json` dentro `queue/<id>/`. È un formato che il runner non legge più.
- `meteo_for` e `/api/meteo` (righe 1241-1284): la pagina non li chiama mai.
- `/api/percorsi`, `/api/file`, `/api/tappa`, `/api/avvia_agenti`: la pagina non li usa.
- `get_salute` (`/api/salute`, riga 677), che viene dalla vecchia "Sala controllo": la pagina la chiama ancora una volta (`ufficio.html:536`). Guarda solo le candidature: DUBBIO.
- `build_state`, `gen_collect` e `cv_collect` (`/api/stato`): la pagina non usa `/api/stato`, però la chat generale le usa per il contesto (`chat_context`, riga 561). Quindi VIVO, ma solo per la chat.

**Doppioni nel codice** [visto]:
- **Lettura dei file task:** 4 copie (`runner.parse_task`, `scheda._parse_task`, `ufficio_dati.parse_task`, `pannello_server._md_task`).
- **Ricerca del programma `claude`:** 3 copie (`motori.trova_claude`, `runner.find_claude`, `ufficio_extra._find_claude`).
- **`jload`/`jsave`** (leggere e scrivere file json): 3 copie.
- **Prossimo numero di task:** 3 modi diversi (`ufficio_dati._prossimo_id`, `scheda._nuova_proposta`, `scheda._prossimo`).
- **Riconoscere il limite di Claude:** `runner.LIMIT_HINTS` e `motori.SEGNI_LIMITE`.
- **Calcolo dei consumi:** `cv_collect` (quota delle candidature), `motori.consumo` e `consumo_dettaglio`.

### candidature/
| File | A cosa serve | Stato |
|---|---|---|
| `runner/runner.py`, `state.py`, `scout.py`, `mappa.py`, `checks.py`, `fetcher.py`, i template | Il programma delle candidature: scout → analisi + CV → lettera. Ha una sua coda in `stato/stato.json` | VIVO. Usa solo Claude (abbonamento) |
| `stato/stato.json` (190 KB), `coda.md`, `log.txt` | Memoria e rapporto delle candidature | VIVO |
| `stato/uso.csv` | Log vecchio | VECCHIO |
| `Archivio/` | Vecchi CV e analisi, solo da leggere | VIVO (archivio) |

### pulizia/ (strumenti del 05/10)
| File | A cosa serve | Stato |
|---|---|---|
| `backup_completo.py` + `.bat` | Zip e `.bundle` di tutto in `C:\BACKUP_UFFICIO`. Un `.bundle` è un file che contiene tutta la storia git, con tutti i rami | VIVO, importante |
| `pubblica_github.py` + `CARICA_SU_GITHUB.bat` | Carica questa copia su GitHub | VIVO |
| `controlla_repo.py` + `.bat`, `CONTROLLO_REPO.txt` | Controllo dei rami, solo lettura | VIVO |
| `crea_prova.py` + `.bat`, `PROVA_RAMI.txt` | Ricrea il ramo `prova` = main + i rami scritti nel codice | VIVO, ma rischioso (sezione 6) |
| `esporta_diff.py` + `.bat`, `diff/` | Copia i DIFF e i RAPPORTO delle ultime 24 ore | VIVO |
| `PROMPT_CLOUD_1_SPIEGAZIONE.md` | Questo compito | — |

### Backup e copie
`_backup_v0.4`, `_backup_v0.5b`, `_backup_v0.6`, `_backup_v0.7` e `confronto_claude_2026-10-05`: sono copie di file vecchi e prove. Nessun programma le legge: **VECCHIO**. Pesano circa 2,5 MB in tutto.

---

## 3. Motori e modelli

### I 4 "motori" di oggi (`motori.py:534`)
| Nome nel codice | Nel pannello | Cosa fa davvero |
|---|---|---|
| `claude` | "Claude (Pro)" | `claude -p` con l'abbonamento. Il programma toglie apposta la chiave API (`env_pulito`, riga 85), così non si paga mai a consumo |
| `auto` | "Gratis, poi Claude" | Prima un modello gratis. **Se fallisce, passa a Claude (abbonamento)** (`runner.py:433-440`). Anche la 2ª correzione dopo i controlli va **sempre** a Claude (`fase == "fix2"`) |
| `gratis` | "Solo gratis" | Solo modelli gratis. Se falliscono, la task finisce in "Da sistemare" |
| `openrouter` | "OpenRouter, modello scelto" | Il modello scritto nella task, anche a pagamento (credito OpenRouter) |

Nella chat del pannello `auto` e `openrouter` valgono come "Gratis" (`ufficio_extra.py:244`). Per la chat quindi il ripiego su Claude non esiste.

### Come si sceglie il modello gratis (`modello_per`, riga 576)
- **Campo `modello:` vuoto** → `@gratis1`, cioè il modello fisso `nvidia/nemotron-3-super-120b-a12b:free` (riga 590).
- **`@gratisN`** → l'N-esimo dell'elenco di OpenRouter. I modelli sono ordinati per grandezza stimata dal nome (riga 595).
- **`@forte`** → il modello preferito di ogni fornitore con chiave, in questo ordine: Gemini → Cerebras → Groq → Mistral (riga 658). Se finiscono, si passa ai gratis di OpenRouter.
- **`@gemini`, `@groq`...** → il primo modello di quel fornitore.
- Per Gemini l'ordine di preferenza mette ancora i **Pro** dopo i Flash (`gemini-pro-latest`, `gemini-[\d.]+-pro`, riga 650), anche se il commento dice che non sono gratuiti.

### Catene e ripieghi
- **Dentro una chiamata** (`_openrouter_paziente`, riga 808):
  - se un modello è occupato (codici 408, 429, 5xx o rete), si passa subito al successivo;
  - quando sono finiti tutti, si aspetta 30 s e poi 60 s e si rifà il giro;
  - un modello che risponde 400/402/403/404 viene tolto dall'elenco. Questo però vale **solo** per Gemini, Cerebras, Groq e Mistral (riga 838), non per i modelli di OpenRouter.
- **Risposta "inadatta"** (nessun file scritto quando serviva): si richiede fino a 3 volte (`_colpo_singolo`, riga 1075).
- **Nel runner:**
  - se il modello gratis "non ha prodotto nulla di valido", si riprova fino a 3 volte (`TENTATIVI_GRATIS`, `runner.py:127`, `_chiama_con_tentativi`);
  - dopo i controlli ci sono fino a 3 giri di correzione con i gratis (2 con Claude).

### Quando una task "gratis" finisce su Claude e consuma l'abbonamento [visto]
1. Il motore della task o del progetto è `auto`. **Oggi Langue ha `"motore": "auto"`** (`ufficio/progetti/langue.json`).
2. Il motore è `auto` e si arriva alla 2ª correzione (`fix2`): va sempre a Claude.
3. Il motore della task è `claude`, oppure è `claude` quello del progetto o il predefinito.
4. La revisione critica chiede `model: opus` (`scheda.py:230`), ma questo vale solo se il motore è Claude.
5. "Modifica il pannello" dalla chat usa **sempre** Claude Sonnet (`ufficio_extra.py:495`).
6. La chat con la scelta "Claude".
7. Le candidature: **sempre** Claude.

Nel log del 05/10 ci sono **4 ripieghi su Claude** [visto, `generico/logs/runner.log` righe 255, 274, 421, 575 e `logs/uso.csv`]:
- T18-risposta1 e T18-risposta2 (Langue, `auto`);
- TL01-risposta6 (Timelive);
- GT18-punti-critici-integrati (GTT, 0,42 $ di listino).

TL01 e GT18 non hanno `motore:` né nella task né nel progetto. [ipotesi] In quel momento il predefinito nelle Impostazioni era ancora `auto`; oggi è `gratis`.

### Tempi massimi [visto]
| Cosa | Valore | Dove |
|---|---|---|
| Un singolo modello gratis | **600 s** (`TEMPO_TENTATIVO`) | `motori.py:800` |
| Tutti i tentativi di una chiamata gratis | 900 s (`TEMPO_TOTALE`) | `motori.py:799` |
| Chiamata gratis dal runner | `min(timeout del livello, 600)` | `runner.py:435` |
| Claude, task piccola / media / grande | 600 / 1800 / 5400 s | `runner.py:58-62` |
| Chat: gratis / Claude | 180 s / 240 s | `ufficio_extra.py:289, 296` |
| Modifica del pannello | 900 s | `ufficio_extra.py:496` |

**Il caso peggiore per una task gratis:**
- 3 richieste per risposta inadatta × 900 s = 45 minuti per chiamata;
- × 3 tentativi del runner, poi i giri di correzione;
- in teoria **più di 2 ore**.

Il tempo della task (600/1800 s) non ferma niente: per i gratis `p.timeout` non diventa mai vero, quindi la strada "interrotta per tempo" (`runner.py:358`) non scatta mai. [visto, deduzione dal codice]

Nel log ci sono chiamate singole da 527 s e 616 s (`logs/uso.csv`). Il 05/10 GT20 è stata fermata da Leo dopo 9 minuti con il motivo "non sta trovando il modello" (`results/GT20.../STOP.json`).

### Dove si registrano i consumi
- **`logs/uso.csv`:** una riga per chiamata (chi, progetto, task, fase, motore, modello, esito, token, costo di listino, secondi) e una riga "esito" per ogni task finita.
- Il **contatore delle 5 ore** (`comune.contatore`) conta solo il costo di listino di Claude, convertito in "token pesati": 1 milione = 100%, una stima di Leo.
- Per i fornitori compatibili OpenAI (Gemini, Cerebras, Groq, Mistral) il costo è scritto sempre **0** (`motori.py:772`).
  - [ipotesi] Se su Gemini è attiva la fatturazione, le chiamate a pagamento (per esempio i Pro, se qualche volta rispondono) **non compaiono come costo** da nessuna parte.
  - Nel log c'è 1 chiamata a `gemini-pro-latest` andata a buon fine.

---

## 4. Dati e stato: i file che fanno da "memoria"

| File | Cosa contiene | Chi lo scrive | Chi lo legge |
|---|---|---|---|
| `logs/uso.csv` | Consumi: una riga per chiamata + gli esiti | `motori.registra` | pannello, dispatcher, contatore |
| `diario.jsonl` | Una riga per lavoro finito: frase, esito, %, secondi, rapporto | dispatcher (`diario_gen`, `diario_cv`), `task_stop` | pannello, scheda |
| `domande.jsonl` | Domande che non fermano il lavoro (aperta/risposta) | dispatcher (da DOMANDE.md), scheda (Consigli e Revisione), pannello quando Leo risponde | pannello, scheda |
| `generico/decisions/<id>.md` | Domande che fermano una task + la risposta di Leo dopo "RISPOSTA:" | runner, pannello | runner (diventa ANSWERS.md) |
| `progetti/<id>.json` | Scheda tecnica del progetto: cartella, priorità, motore, piano, **decisioni** (risposte di Leo, ultime 60), da_rivedere, revisione | pannello, scheda | tutti. Le ultime 30 decisioni vanno nel prompt di ogni task (`runner.py:159`) |
| Scheda progetto nel repo (`PROGETTO.md`, `MEMORIA_PROGETTO.md` per GTT, `Desktop\Timelive\timelive.md` per Timelive) | Sopra: la parte di Leo (obiettivo, regole). Sotto, tra due segni: lo "STATO DELL'UFFICIO", riscritto da `scheda.aggiorna` | Leo (sopra), Ufficio (sotto) | agenti (primi 9000 caratteri), chat |
| `<progetto>/agenti/LOG.md` | Una riga per task | runner (`runner.py:561`) | Consigli, Revisione |
| `<progetto>/agenti/ULTIMO_SCRIPT.txt` | Output dell'ultimo controllo `run_py` | `repo_tools.py:406` | Leo |
| `<progetto>/agenti/<id>/*` | RAPPORTO, RUNNER, VALIDATORE, DIFF, DOMANDE, DECISIONS | runner, agente | pannello, Leo |
| `generico/results/<id>/` | Risposte grezze, summary, VALIDATORE.log, STOP.json | runner, task_stop | pannello, dispatcher |
| `rotazione.json` | Turni della rotazione, lavori "in cima" | dispatcher, pannello | dispatcher |
| `agente_attuale.json` | Il lavoro in corso adesso | dispatcher | pannello, task_stop |
| `LIMITE_CLAUDE.txt` | Fino a quando c'è il limite di Claude | `comune.imposta_limite` | tutti |
| `generico/STOP`, `candidature/stato/STOP` | Pausa | pannello | runner, dispatcher |
| `candidature/stato/stato.json` | Tutto delle candidature: offerte, domande, direzioni, coda, mappa delle aziende, registro | runner delle candidature, pannello | gli stessi |
| `pannello/chat_stato.json` | Cronologia della chat (generale e per progetto) e messaggi usati oggi | `ufficio_extra` | pannello |
| `pannello/chat_log.md` | Tutto quello che si dice in chat e le azioni confermate | `ufficio_extra.log` | Leo |
| `pannello/feedback.json` | Motivi di rifiuto delle offerte | pannello | pannello |
| `logs/calibrazione.jsonl` | I % letti da Leo in Claude | pannello | contatore |
| `~/.ufficio/chiavi.json` | Chiavi API (fuori da tutte le cartelle) | pannello | motori |

**Osservazione critica.** La stessa informazione vive in più posti:
- le decisioni di Leo stanno in `progetti/<id>.json`, nella scheda dentro il repo e in `domande.jsonl`;
- le regole per gli agenti stanno nella scheda e in `generico/profiles`;
- l'elenco dei progetti sta in `progetti/*.json` e nel campo `progetti` di `pannello_config.json`.

---

## 5. Progetti

**GTT** (`progetti/gtt`, Desktop\GTT, git)
- **Cosa è:** una mappa interattiva del trasporto a Torino. Mette insieme dati GTFS, mezzi in tempo reale, sensori 5T e pendolarismo ISTAT.
- **Com'è organizzato:**
  - `scripts/01..07_*.py` scaricano e raccolgono i dati (la raccolta gira di continuo);
  - `04_genera_mappa.py` genera `mappa_torino.html` dal modello `scripts/mappa_template.html`;
  - `docs/` contiene fonti, qualità e piano;
  - `data/` contiene i dati (60 MB di SQLite, ignorati da git).
- **File di servizio dell'Ufficio:** `MEMORIA_PROGETTO.md` (la memoria di Leo, usata come scheda: l'Ufficio riscrive le righe 132-172), `agenti/` (18 cartelle task + LOG.md + ULTIMO_SCRIPT.txt), `generico/profiles/gtt.md`.
- **Attenzione:** `mappa_torino.html` è **ignorato da git** (`.gitignore`), ma GT20 lo aveva tra i file permessi. Vedi il problema 5.
- **Rami:** 23. Il ramo attivo è GT20, con `prova` sotto.

**Langue** (`progetti/langue`, Desktop\Langue, git)
- **Cosa è:** un sito statico per italiani che imparano il tedesco (A1-A2) con 3 giochi.
- **Com'è organizzato:**
  - `contenuti/*.json` (parole, frasi, errori), `schema/` e `SCHEMA.md` (regole dei contenuti);
  - `web/` (index.html, app.js, data.js, style.css);
  - `archivio/` (codice vecchio);
  - `words_db.json` (dati originali di Leo).
- **File di servizio:** `PROGETTO.md` (scheda: "Per chi e contesto" e "Note di Leo" sono ancora vuote), `agenti/` (20 cartelle), `generico/profiles/langue.md` (le stesse regole della scheda). Il motore del progetto è `auto`.
- **"Obiettivo giornaliero"** [visto]:
  - è l'idea n. 6 di `agenti/T18-idee-c/IDEE.md`;
  - Leo ha risposto "5" a una domanda;
  - la correzione T18-risposta2 ha cambiato solo **una riga di IDEE.md**;
  - T19-scelta ha poi scartato l'idea.
  - Quindi nel sito l'obiettivo giornaliero **non esiste**: la risposta di Leo è finita su un documento di idee.
- **Rami:** 31, il numero più alto.

**Preventivi papà** (`progetti/preventivi`, Desktop\Projects\Preventivi_Gigi, git dal 05/10)
- **Cosa è:** un generatore di preventivi in Word per il papà di Leo.
- **Com'è organizzato:**
  - `strumenti/genera_preventivo.py`, `verifica_preventivo.py`, `prova_finta.py`, `dati_esempio.json`, `out/`;
  - `Template/` (logo, PDF);
  - `Preventivo Automatico/` (modello Word v4.1);
  - un vecchio `.doc` nella cartella principale.
- **File di servizio:** `PROGETTO.md` (scheda quasi vuota: niente regole e niente contesto), `agenti/` (7 cartelle + LOG.md + ULTIMO_SCRIPT.txt).
- **Problema aperto:** il logo nel Word. Gli agenti non possono aprire Word.
- `genera_preventivo_RIFERIMENTO.py` c'è sia qui sia in `ufficio/generico/scripts/pv/`.
- **Rami:** 8. Il ramo attivo è `PV05-risposta1`, con 1 modifica non salvata.

**Timelive** (`progetti/timelive`, Desktop\timelive_repo, git)
- **Cosa è:** un archivio personale e locale dei dati di Leo (Spotify, soldi, salute, mappe, WhatsApp, chess), interrogabile da un modello (locale con Ollama o cloud) tramite `llm_bridge.py`.
- **Com'è organizzato:**
  - `code/` (file `*_ingest.py`, `ingest_engine.py`, `llm_bridge.py`, `table_router.py`, test);
  - `test/` (rapporti dei batch);
  - `docs/` (BRIDGE_V2_a/b);
  - file `*_ingest.py` anche nella cartella principale: [ipotesi] doppioni di quelli in `code/`, da controllare.
- **File di servizio:** `agenti/` (9 cartelle).
  - La scheda dell'Ufficio è **fuori dal repo**: `Desktop\Timelive\timelive.md` (`progetti/timelive.json`, campo `scheda`).
  - Nel repo però c'è un altro `timelive.md` (il documento di architettura). [ipotesi] Due file con lo stesso nome in due cartelle: rischio di confonderli.
- **Rami:** 18, di cui 6 sono `TL01-rispostaN` (sei correzioni in fila sulla stessa task).

**Mercatino Austria** (`progetti/mercatino`, Desktop\Mercatino, non è git)
- **Cosa è:** studio di fattibilità di un franchising. Archiviato il 04/10.
- **Com'è organizzato:** 4 documenti (dossier PDF e markdown, documento di lavoro).
- **File di servizio:** nessuno. La task M01 è in `generico/sospesi`.

**Candidature** (dentro l'Ufficio: `ufficio/candidature`)
- **Cosa è:** progetto a sé, con un suo runner e una sua coda.
- I documenti di base (framework, baseline del CV e della lettera) restano in `Desktop\CV` e non vengono mai copiati.
- Usa solo Claude.

---

## 6. Problemi trovati (dal più grave)

1. **I file di servizio dell'Ufficio stanno dentro i repo e creano conflitti a ogni unione.** [visto]
   - Dopo ogni task il dispatcher riscrive la scheda (`dispatcher.py:271-283` → `scheda.aggiorna`, `scheda.py:177`). Lo fa nel repo, mentre il progetto è ancora sul ramo della task appena finita.
   - La task dopo trova la cartella "sporca" e **salva in automatico quella modifica sul ramo vecchio** (`repo_tools.py:44-51`, commit "[runner] salvataggio automatico").
   - In `RAMI_PROGETTI.md` 19 rami su 80 finiscono proprio con quel commit.
   - In più ogni task aggiunge una riga a `agenti/LOG.md` (`runner.py:561`) e `run_py` riscrive `agenti/ULTIMO_SCRIPT.txt` (`repo_tools.py:406`).
   - Risultato: in `PROVA_RAMI.txt` 8 unioni su 13 sono saltate per conflitti **solo su questi file** (`PROGETTO.md`, `MEMORIA_PROGETTO.md`, `agenti/LOG.md`, `agenti/ULTIMO_SCRIPT.txt`).
   - [ipotesi] La versione attuale di `crea_prova.py` dovrebbe risolverli da sola (tiene la versione di `prova`), ma il rapporto dice "SALTATO". Forse il rapporto è stato fatto con una versione precedente dello script, oppure `checkout --ours` non riesce su un file cancellato da una delle due parti. Va provato sul PC.

2. **Ogni ramo di task parte dal ramo attivo in quel momento, non da `prova` né da `main`.** [visto]
   - `prepare_branch` crea il ramo da quello corrente (`repo_tools.py:65-73`). Le task create dal pannello non mettono mai `base_branch` (`ufficio_dati.py:643-649`, `scheda.py:308-309`).
   - Così i rami nascono uno dall'altro "a catena": ognuno contiene anche il lavoro (buono o cattivo) dei rami precedenti, e la scheda salvata in automatico.
   - Unire "un ramo buono" porta dentro anche cose non volute.
   - Le correzioni `XX-rispostaN` (`ufficio_dati.py:923`) partono dal ramo attivo, che può essere quello di un'altra task, non quello della task da correggere.

3. **"Rifai" riusa il ramo vecchio e a volte non richiama nemmeno l'agente.** [visto]
   - `task_rifai` rimette in coda lo stesso file, con lo stesso id e lo stesso ramo (`ufficio_dati.py:707-718`).
   - Il runner passa sul ramo vecchio, quindi riparte dal lavoro vecchio e non da quello nuovo fatto nel frattempo su `prova` (`repo_tools.py:61-64`).
   - Se il ramo era già quello attivo, c'è un RAPPORTO.md e i controlli passano, **il lavoro vecchio viene preso per buono senza chiamare l'agente** (`runner.py:322-328`). Con controlli deboli come `files_exist` questo succede facilmente.
   - Esempio: il 05/10 PV02 è stata rifatta sul ramo esistente ("gia' esistente: ci sono passato sopra", `runner.log`).

4. **Le task "gratis" possono finire sull'abbonamento Claude** (sezione 3).
   - Succede con il motore `auto` (Langue oggi), e la 2ª correzione con `auto` va sempre a Claude (`runner.py:433-440`).
   - 4 casi il 05/10.
   - È il contrario della regola di Leo ("mai ripiego sull'abbonamento").

5. **Un modello può bloccare per 10 minuti, una task gratis anche per ore, e il pannello non lo mostra bene.** [visto + deduzione]
   - I limiti sono `TEMPO_TENTATIVO` = 600 s, i 3 giri in `_colpo_singolo` e i 3 tentativi nel runner (sezione 3).
   - Il segno "in corso" scade dopo `timeout + 120` s (`motori.py:201`) e poi viene cancellato (`motori.py:235-237`): dopo circa 12 minuti il pannello non vede più la chiamata, anche se continua.
   - I modelli che falliscono sempre non vengono esclusi:
     - un 429 ("troppe richieste") viene trattato come "riprova", non come "scarta" (`motori.py:798, 838`);
     - nel log `gemini-2.5-pro` ha **15 errori su 15**, eppure è ancora tra i candidati;
     - per i modelli di OpenRouter non esiste nessuna esclusione automatica.

6. **I file permessi possono essere file ignorati da git.** [visto]
   - In GTT, `mappa_torino.html` è nel `.gitignore`, ma era tra i file permessi di GT20.
   - Le modifiche a un file ignorato non finiscono nel commit, nel DIFF o nel ramo. La guardia dei file permessi non le vede (`repo_tools.changed_files`).
   - In più la prossima volta che si lancia `04_genera_mappa.py` il file viene rigenerato e le modifiche si perdono.

7. **"Fatta" non vuol dire "fatta tutta".** [visto]
   - Molte task hanno solo `files_exist` come controllo (`ufficio_dati.py:647-649`): basta che il file esista.
   - PV02 e TL05 risultano "done" anche se, in quel momento, parte delle modifiche **non era stata applicata**. Il runner lo aveva scritto ("MODIFICHE NON APPLICATE: ... SEARCH non trovato", `results/TL05-log-ollama/summary.txt`).
   - La versione attuale di `motori.py` è "tutto o niente" per le modifiche a pezzi (riga 1095), quindi questo caso preciso oggi non dovrebbe ripetersi. Restano però dei buchi:
     - se il modello riscrive per intero un file grande, nessuno controlla che non abbia tolto delle parti [ipotesi];
     - se il modello scrive file fuori dai permessi, i blocchi vengono rifiutati, ma l'esito resta "ok" (riga 1127);
     - le task fatte prima della correzione restano "done".

8. **`crea_prova.py` ricrea `prova` da `main` ogni volta e lascia degli "stash".** [visto]
   - `git checkout -B prova main` butta via il `prova` di prima: se Leo ha fatto delle prove o correzioni a mano su `prova`, le perde.
   - Ogni lancio mette da parte la scheda con `git stash` (un cassetto dove git mette da parte le modifiche) e non la riprende mai: gli stash si accumulano.
   - L'elenco dei rami da unire è scritto nel codice (righe 16-21) e va cambiato a mano ogni volta.

9. **Il salvataggio automatico salva tutto, anche i file nuovi, prima del controllo dei file non tracciati.** [visto]
   - `_salva_albero_sporco` fa `git add -A` (`repo_tools.py:48`) prima del controllo "troppi file non tracciati" (`runner.py:294`).
   - Se manca un `.gitignore`, finiscono nel commit centinaia di file (dati, cache).
   - Salva anche le modifiche fatte a mano da Leo sul ramo attivo, mescolandole col lavoro degli agenti.

10. **Le domande degli agenti spesso non si capiscono.** [visto]
    - L'esempio nel prompt è letteralmente `opzioni: A / B / C` (`runner.py:79, 101`), e i modelli lo copiano.
    - In `domande.jsonl` ci sono domande con opzioni "A", "B", "C" e il significato solo nel campo `cambia`.
    - Non c'è mai l'opzione "non so / decidi tu".
    - Una risposta diversa dalla scelta provvisoria crea **sempre** una task di correzione, anche quando la domanda riguarda un documento di idee (il caso Langue). Così nascono catene come TL01-risposta1...6.

11. **Il costo di Gemini è sempre 0 nel log.** [visto: `motori.py:772`; ipotesi sul fatto che costi davvero]
    - Con la fatturazione attiva e i modelli Pro ancora in elenco (riga 650), Leo potrebbe pagare senza vederlo nel pannello.

12. **Il runner si ferma se `claude` non è installato, anche per le task gratis** (`runner.py:784-787`). [visto]
    - Oggi non è un problema perché Claude è installato. Lo diventa se un giorno si vuole un Ufficio senza Claude.

13. **Codice morto e doppioni** (sezione 2). Non rompono niente, ma rendono difficile capire cosa fa cosa. I principali:
    - le parti morte in `pannello_server.py`;
    - `comune.pulizia_avvio`;
    - `_migra` e `MODELLO_GRATIS` in `motori.py`;
    - 4 copie della lettura dei file task;
    - campi morti in `pannello_config.json`.

14. **Mistral è nel codice e nel pannello** (`motori.py:655-658`, `ufficio.html:755`) anche se non ha API gratis. È innocuo senza chiave, ma confonde.

15. **Codex CLI non esiste nel codice.** È solo un'idea in `PIANO_v0.5.md:131`. Non c'è niente da togliere: c'è solo da decidere se farlo.

16. **Il diario non sempre ha l'esito.** Dopo lo Stop di GT20 la riga dice esito "?" e frase "?" (ultima riga di `diario.jsonl`). [visto; la causa precisa è un'ipotesi: `diario_gen` cerca la riga di esito nel log, ma non la trova o non la riconosce]

17. **Mancano dei contesti nelle schede.**
    - "Per chi e contesto" è vuoto in Langue e in Preventivi; in Preventivi mancano anche le regole.
    - Gli agenti lavorano senza sapere per chi lavorano. [visto]
