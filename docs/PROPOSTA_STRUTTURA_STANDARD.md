# Proposta: una struttura standard per ripartire puliti

Scritto il 05/10/2026. **È una proposta da discutere con Leo, non da applicare.** Si basa su `docs/SPIEGAZIONE_SISTEMA.md` (citato come "Spiegazione, problema N").

**Idea di fondo, in tre frasi**
- Il lavoro degli agenti deve stare nel repo del progetto; tutto il resto deve stare fuori.
- Ogni task parte da un punto preciso (`prova`) e il suo ramo si cancella quando ha finito il suo scopo.
- Con i modelli gratis non si passa mai da soli a Claude: decide Leo, caso per caso.

---

## 0. Decisioni di Leo (05/10, sera)

**Priorità generali**
1. Usare tutti i modelli gratis possibili, sempre il più potente disponibile.
2. Tenere `C:` pulito e ordinato, e così anche ogni progetto.
3. Fare un backup periodico che si possa ripristinare.

| # | Domanda | Decisione | Cosa vuol dire in pratica |
|---|---|---|---|
| 1 | Dove mettere i file di servizio | "decidi tu" → **fuori dal repo**, in `Multiple Agents\progetti\<id>\` | Il progetto contiene solo il lavoro vero. È la soluzione più pulita (priorità 2) |
| 2 | Il RAPPORTO nella storia git | "se serve" → nel commit va **solo la riga ESITO**. Il rapporto intero resta nel fascicolo | Una riga costa niente e basta a capire cosa ha fatto un ramo. Il resto sarebbe solo rumore nel repo |
| 3 | Quando una task gratis fallisce | **si ferma e sceglie Leo**. Da ripensare quando ci saranno più motori | "Da sistemare" con i pulsanti delle alternative (sezione 4) |
| 4 | L'abbonamento Claude per le task | **solo come scelta esplicita** | Niente più ripieghi automatici. Il motore `auto` sparisce |
| 5 | "Credito cloud" | **non è una cosa sola**: credito AI Studio (Gemini a pagamento), l'uso extra di Claude con il Pro, altro | Le alternative diventano un elenco di "motori a pagamento", ognuno con il suo tetto (sezione 4) |
| 6 | I rami dopo l'unione | **si cancellano** | Restano solo nel backup `.bundle` |
| 7 | Il ramo `prova` | **la cosa più pulita**, c'è già il backup | `prova` cresce; i rami delle task si cancellano dopo l'unione. Risultato: in ogni repo restano `main`, `prova` e solo le task aperte |
| 8 | Le candidature | **diventano task come gli altri progetti** | È il lavoro più grande della lista: va fatto per ultimo (passo 16) |
| 9 | Il pannello | **Mondo sì** (sarà ampliato). **Contatore delle 5 ore e tetto dei messaggi: no** | Si tolgono il contatore, la calibrazione, la variabile `PER` e il limite della chat. Il limite vero di Claude (`LIMITE_CLAUDE.txt`) resta, perché Claude si può ancora scegliere |
| 10 | Codex | **se serve, collegarlo** | Vedi sezione 4 |
| 11 | La mappa di GTT | **fuori da git**, rigenerata in automatico dopo le task | Gli agenti modificano il modello (`scripts/mappa_template.html`). Il runner rigenera la mappa; il controllo `run_py:scripts/04_genera_mappa.py` lo fa già |
| 12 | Quale `timelive.md` vale per Timelive | **il più recente** | Da controllare sul PC: confrontare le date dei due file. Quello vecchio va in archivio |

---

## 1. Struttura standard di un progetto (uguale per tutti)

```
<Progetto>\                    (repo git: SOLO il lavoro vero)
  LEGGIMI.md                   cos'è il progetto, come si usa (per una persona)
  SCHEDA.md                    la parte di Leo: obiettivo, per chi, regole per gli agenti, decisioni importanti.
                               La scrive solo Leo. L'Ufficio NON la riscrive mai.
  src\ o web\ o scripts\       il codice (il nome dipende dal progetto)
  contenuti\                   dati piccoli scritti a mano o dagli agenti (json, csv)
  docs\                        documenti
  dati\                        dati grandi, scaricati o generati: IGNORATI da git (.gitignore)
  .gitignore                   comprende: dati\, file generati, .ufficio\

Multiple Agents\progetti\<id>\ (FUORI dal repo: il "fascicolo" del progetto per l'Ufficio)
  progetto.json                cartella, priorità, motore, decisioni (oggi progetti\<id>.json)
  stato.md                     oggi è la parte "STATO DELL'UFFICIO" della scheda: generata, mai nel repo
  log.md                       oggi è agenti\LOG.md
  task\<id>\                   RAPPORTO.md, RUNNER.md, VALIDATORE.md, DIFF.patch, DOMANDE.md, ULTIMO_SCRIPT.txt
```

**Perché così**
- Il problema 1 sparisce: niente nel repo cambia dopo una task, a parte i file che l'agente doveva cambiare.
- Cambiare ramo non salva più niente in automatico, perché la cartella resta pulita.
- Le unioni in `prova` hanno conflitti solo dove due task hanno toccato lo stesso codice. Quelli sono conflitti veri, che vanno guardati.

**Alternativa più leggera (B):** lasciare i file di servizio nel progetto, ma in una cartella `.ufficio\` ignorata da git.
- Git non tocca i file ignorati quando si cambia ramo, quindi anche questa soluzione elimina i conflitti.
- Pro: tutto resta vicino al progetto.
- Contro: l'agente vede quei file, e un `git clean` (il comando che cancella i file non salvati) li cancellerebbe.

**Il rapporto della task** può comunque entrare nel commit, come testo del messaggio (le prime 5 righe). Così chi guarda la storia git capisce cosa ha fatto ogni ramo anche senza il fascicolo.

**Regole che il runner dovrebbe controllare prima di partire** (oggi non le controlla):
- Nessun file permesso può essere ignorato da git. Il caso GTT `mappa_torino.html` va bloccato con un messaggio chiaro: "modifica `scripts/mappa_template.html`, la mappa si rigenera".
- La cartella deve essere pulita. Se non lo è, il runner **si ferma e lo dice**, invece di salvare tutto in automatico sul ramo attivo.

**Per ogni progetto, in concreto**
| Progetto | Cosa cambia |
|---|---|
| GTT | `MEMORIA_PROGETTO.md` resta il documento di Leo e diventa (o resta) la sua SCHEDA. La parte automatica (righe 132-172) esce dal repo. Gli agenti modificano il template, non la mappa generata |
| Langue | `PROGETTO.md` → `SCHEDA.md`, da completare ("per chi"). `generico/profiles/langue.md` si toglie perché è uguale alla scheda |
| Preventivi | Scheda da scrivere: oggi è vuota. Il `.doc` vecchio va in `docs\` o in archivio |
| Timelive | Decidere quale `timelive.md` vale: quello nel repo o quello in `Desktop\Timelive`. Oggi ce ne sono due |
| Mercatino | Niente: archiviato |
| Candidature | Restano a parte (vedi domanda 8) |

---

## 2. Struttura standard dell'Ufficio

**Cosa tenere così com'è:** `motori.py`, `comune.py`, `dispatcher.py`, `scheda.py`, `generico/runner.py`, `generico/repo_tools.py`, `task_stop.py`, `consumo_dettaglio.py`, la cartella `pulizia/` (backup, GitHub, controllo).

**Cosa accorpare**

| Oggi | Proposta | Perché |
|---|---|---|
| `pannello_server.py` (1557 righe: server + candidature + chat + meteo + azioni vecchie) | `pannello_server.py` = solo il server web (indirizzi → funzioni). Le funzioni delle candidature vanno in `pannello/candidature_pannello.py` | Oggi per trovare una funzione bisogna aprire 3 file |
| `ufficio_dati.py` (dati + azioni + "Cosa succede") | resta, ma solo per le **letture** (stato, task, diario, cosa succede) | — |
| le azioni sparse in `ufficio_dati.py` e `pannello_server.py` | `pannello/azioni.py`: nuova task, approva, rifai, stop, rispondi... | Un solo posto per "cosa succede quando premo un pulsante" |
| `ufficio_extra.py` (impostazioni + chat + modifica del pannello + feedback) | `pannello/chat.py` (chat e modifica del pannello) + `pannello/impostazioni.py` | Sono due cose diverse |
| 4 letture dei file task, 3 ricerche di `claude`, 3 `jload` | un piccolo `task_file.py` nel nucleo (leggere, scrivere, spostare un file task) e `trova_claude` solo in `motori.py` | Meno copie da tenere allineate |

**Cosa togliere** (ogni voce è nella Spiegazione, sezione 2):
- **in `pannello_server.py`:** `dispatch_once`, `generico_loop`, le parti `task.json` di `act_add`, `act_approve` e `act_answer`, il meteo, `/api/percorsi`, `/api/file`, `/api/tappa`, `/api/avvia_agenti`;
- **in `pannello_config.json`:** `soglia_stop_pct`, `generico_auto`, il vecchio `chat_limite_giorno` (o farlo valere davvero), l'elenco `progetti`;
- **in `comune.py`:** `pulizia_avvio`;
- **in `motori.py`:** `_migra` e `VECCHI`, `MODELLO_GRATIS`, Mistral, i modelli Gemini Pro;
- **in `ufficio_dati.py`:** `_backfill`, `tappa_stato`, `_piano` (se le tappe non tornano), `vecchio_elenco` e `vecchio_elimina` (dopo averli usati una volta);
- **file vecchi:** `generico/logs/usage.csv`, `candidature/stato/uso.csv`, `pannello/chat_uso.csv`, `logs/modelli_fornitori.json`, `Claude outputs/`;
- **cartelle `_backup_v0.4/5b/6/7` e `confronto_claude_*`:** spostarle in `C:\BACKUP_UFFICIO`, che è già il posto dei backup;
- **i doppioni in `generico/`:** `failed/T17-prova-gratis`, `sospesi/GT14-verifica-passaggi`, i 2 file rimasti in `decisions/`.
- `generico/results/`: tenere solo gli ultimi 30 giorni, o spostare il resto in archivio.

**Deciso il 05/10:**
- il Mondo resta;
- si tolgono il contatore delle 5 ore, la calibrazione, la variabile `PER`, il tetto dei messaggi della chat e `get_salute` (guarda solo le candidature, che diventano task).

**Struttura delle cartelle proposta** (cambia poco rispetto a oggi):
```
Multiple Agents\
  run.bat, Ufficio.vbs, INSTALLA_UFFICIO.*      avvio
  motori.py, comune.py, dispatcher.py, scheda.py, task_file.py
  generico\   runner.py, repo_tools.py, queue\ done\ failed\ blocked\ sospesi\ scartate\ results\
  progetti\   <id>\ (fascicolo, sezione 1)
  pannello\   server, letture, azioni, chat, impostazioni, ufficio.html, mondo\
  candidature\
  logs\       uso.csv, runner.log, dispatcher.log, cache dei modelli
  pulizia\    backup, GitHub, controlli
```

---

## 3. Strategia per i rami git

### Regola per il futuro (semplice)
1. **`main`** non si tocca: è la versione "buona" che Leo sceglie a mano.
2. **`prova`** cresce: ogni lavoro accettato si unisce lì. Non si ricrea più da `main` ogni volta.
3. **Ogni task parte da `prova`.** Il runner mette sempre `base_branch = prova`. Le correzioni `-rispostaN` partono dal ramo della task da correggere, oppure da `prova` se quella task è già stata unita.
4. **"Rifai" crea un ramo nuovo** (`GT20-r2`) da `prova` di oggi. Il lavoro vecchio non si prende mai per buono da solo.
5. **Il ramo di una task si cancella** quando è stato unito in `prova` o scartato da Leo. Resta comunque nel backup `.bundle`.
6. **Unire in `prova`** si fa dal pannello, con un pulsante "Accetta" nel dettaglio della task. Così l'elenco dei rami non va scritto nel codice di `crea_prova.py`.

### Come arrivare a una situazione pulita senza perdere lavoro
In `RAMI_PROGETTI.md` vedo **80 rami** in 4 repo (GTT 23, Langue 31, Preventivi 8, Timelive 18), non centinaia. [ipotesi] Sul PC potrebbero essercene altri: va controllato con `CONTROLLA_REPO.bat`.

| Passo | Cosa si fa | Cosa può rompersi |
|---|---|---|
| 0 | `BACKUP_COMPLETO.bat`, poi si controlla `CONTROLLO.txt`: i bundle devono essere "verificati" | niente: legge soltanto |
| 1 | Si spengono gli agenti (Pausa) finché i rami non sono a posto | niente |
| 2 | Per ogni progetto: in ogni ramo si toglie dal salvataggio la scheda e `agenti/LOG.md`. Meglio: si portano fuori dal repo una volta sola, su `prova` (sezione 1) e si aggiungono al `.gitignore` | se un ramo vecchio viene unito dopo, la scheda può "tornare": si risolve tenendo la versione di `prova` |
| 3 | Per ogni progetto, Leo guarda l'elenco dei rami **non ancora uniti** in `prova` e per ciascuno sceglie: unisci / scarta / non so. Si può preparare un elenco con il rapporto di 1 riga per ramo | unire rami "a catena" porta dentro anche il lavoro dei rami precedenti (Spiegazione, problema 2): va guardato il DIFF rispetto a `prova`, non rispetto al ramo da cui è nato |
| 4 | Si uniscono in `prova` quelli scelti. Ora i conflitti sono solo su codice vero | conflitti veri: vanno risolti a mano, o con una task "risolvi conflitto" |
| 5 | Si cancellano i rami uniti o scartati (sono nel bundle) | se il bundle non fosse valido si perderebbe lavoro: per questo il passo 0 è obbligatorio |
| 6 | Si guardano gli stash (`git stash list`). Se contengono solo la scheda, si cancellano | si potrebbe perdere una modifica a mano di Leo alla scheda: prima si guarda il contenuto |
| 7 | Quando Leo è contento di `prova`: `main` = `prova` | niente, se fatto a mano |

---

## 4. Regole per i motori (già decise da Leo)

**Scelte per una task: solo due, più le alternative in caso di fallimento**
- **Gratis**: OpenRouter gratis, Gemini Flash, Cerebras, Groq.
  - Se fallisce, la task va in "Da sistemare" con il motivo e con dei pulsanti: **Riprova gratis / Claude API (a consumo) / Credito cloud**.
  - **Mai** l'abbonamento Claude in automatico.
- **Claude (abbonamento)**: solo se Leo lo sceglie esplicitamente su quella task o su quel progetto (deciso).
- **Alternative a pagamento**, scelte da Leo una per una, ognuna con un tetto di spesa per task:
  - Gemini oltre il gratuito, con il credito di AI Studio;
  - l'uso extra di Claude con il Pro;
  - Claude API;
  - altre da aggiungere.

  [da verificare] Se e come l'"uso extra" del Pro si possa usare da `claude -p` dipende dalle condizioni di Anthropic: va controllato prima di costruirlo.

**"Il più potente possibile" (priorità 1)**
- Oggi l'ordine `@forte` è scritto fisso: Gemini → Cerebras → Groq → Mistral (`motori.py:658`). Per OpenRouter i modelli sono ordinati per grandezza indovinata dal nome (`motori.py:621`).
- **Proposta:** un'unica classifica di tutti i modelli gratis, di tutti i fornitori, ordinata così:
  1. per la percentuale di successi misurata nel log `uso.csv` sulle task vere, appena ci sono abbastanza dati;
  2. altrimenti per grandezza.
- Ogni task usa il primo della classifica che non è "in panchina".
- La classifica si vede in Impostazioni → Motori.
- **Fornitori gratis in più:** ne esistono altri compatibili con lo stesso sistema. [da verificare] I candidati vanno controllati uno per uno su limiti e condizioni (anche "i dati possono essere usati per addestrare?") prima di aggiungerli. Non li elenco come certi.

**Codex** (domanda 10). Cos'è: un programma di OpenAI simile a Claude Code. È un **agente**: apre i file, li legge e li modifica da solo, in più passi.
- **A cosa servirebbe:** oggi i modelli gratis lavorano "a colpo singolo". Ricevono i file nel messaggio e rispondono una volta sola, e così sbagliano spesso sui file grandi (GTT, il pannello: vedi PV02 e TL05). Un agente risolve proprio questo.
- [da verificare] Con un account ChatGPT gratuito Codex può avere limiti bassi o cambiare condizioni. Va provato con una task piccola prima di contarci.
- **Alternativa con lo stesso scopo:** un programma agente "aperto" (OpenCode, già nel piano v0.5) collegato ai modelli gratis della classifica. Così l'agente userebbe i modelli più potenti gratis, invece di dipendere da un solo account.
- **Proposta:** provare tutti e due sulla stessa task (come la "gara" del piano v0.5) e tenere quello che funziona.
- Spariscono `auto` ("Gratis, poi Claude") e `openrouter` ("OpenRouter, modello scelto"). Il modello preciso resta un campo facoltativo della task.
- **Nel codice:** `runner.py:433-440` non passa più a Claude. Il valore `auto` nei file vecchi (Langue) diventa `gratis`.

**Attenzione: Claude API ("a consumo") oggi è bloccato apposta.**
- Il runner e il dispatcher si rifiutano di partire se esiste `ANTHROPIC_API_KEY` (`runner.py:765`, `dispatcher.py:372`), e `motori.env_pulito` la toglie.
- Per avere l'opzione "Claude API" serve una strada separata: la chiave sta in `chiavi.json` e si passa **solo** a quella chiamata, con un tetto di spesa per task.
- È un cambiamento di sicurezza: va fatto con attenzione.

**Gemini**
- Restano solo i Flash. Si tolgono `gemini-pro-latest` e `gemini-[\d.]+-pro` dalle preferenze (`motori.py:650`).
- Il tetto di spesa lo mette Leo nella console Google.
- Nel log si scrive un **costo stimato** anche per Gemini, oggi sempre 0 (`motori.py:772`). Così, se qualcosa costa, si vede.

**Mistral:** si toglie da `FORNITORI`, da `ORDINE_FORTI` e dalla pagina.

**Tempi, ed esclusione automatica dei modelli che falliscono sempre**
| Cosa | Oggi | Proposta |
|---|---|---|
| Un singolo modello | 600 s | **120 s** (180 s per le task grandi) |
| Una chiamata, tutti i modelli insieme | 900 s × 3 giri | **600 s in tutto**, un solo giro |
| Tentativi del runner con i gratis | 3 | 2 |
| Il segno "in corso" nel pannello | sparisce dopo 12 minuti | resta finché la chiamata è viva |
| Modello che fallisce | escluso solo per 400-404 e solo per i fornitori | **escluso per 24 ore dopo 3 errori di fila** (di qualsiasi tipo, anche 429 e tempo scaduto). Escluso per sempre per quella chiave se risponde 402 ("non incluso nel piano gratuito"). Vale anche per OpenRouter |
| Dove si vede | da nessuna parte | Impostazioni → Motori: elenco dei modelli "in panchina", con il motivo e un pulsante "riammetti" |

**Altri punti**
- `MODELLO_GRATIS = "openrouter/free"`: si toglie. "Prova OpenRouter" usa `@gratis1`.
- **Codex CLI:** nel codice non c'è (Spiegazione, problema 15). Va solo deciso se farlo (domanda 10).
- **"Modifica il pannello"** oggi usa sempre Sonnet in abbonamento (`ufficio_extra.py:495`). Proposta: chiede il motore come la chat. Va detto però che i modelli gratis "a colpo singolo" lavorano male su file da 1500 righe.
- Il runner non deve fermarsi se `claude` manca e la task è gratis (`runner.py:784`).

---

## 5. Lista della pulizia, in passi piccoli

Ogni passo si può provare da solo e annullare, e si fa con gli agenti in Pausa. L'ordine conta: prima ciò che costa (abbonamento, tempo), poi ciò che sporca (rami), poi l'ordine nel codice.

| # | Passo | Come si prova | Cosa può rompersi |
|---|---|---|---|
| 0 | Backup completo + controllo dei bundle | `CONTROLLO.txt` tutto OK | niente |
| 1 | **Niente ripiego su Claude:** via `auto` e la regola `fix2`; Langue → `gratis`; scelta Riprova / API / Cloud in "Da sistemare" | una task gratis che fallisce finisce in "Da sistemare" e in `uso.csv` non compare nessuna riga `claude` | le task che prima "si salvavano" con Claude ora si fermano: più lavoro per Leo, all'inizio |
| 2 | **Tempi più corti + esclusione automatica** (sezione 4) | una task con un modello finto lento: deve passare al successivo dopo 120 s; dopo 3 errori il modello va "in panchina" | con tempi troppo corti i modelli grandi e lenti non finiscono mai: si alza il valore |
| 3 | **Via Mistral, Gemini Pro, `MODELLO_GRATIS`**, costo stimato per Gemini | Impostazioni → Motori: Mistral non c'è più; Prova OpenRouter funziona | se qualche task ha `modello: @mistral` scritto dentro, ricade su `@gratis1` |
| 4 | **Domande più chiare:** nel prompt l'esempio diventa con parole vere (`opzioni: tieni il rosso / togli il rosso / non so, decidi tu`); il pannello aggiunge sempre "Non so / decidi tu"; mostra `perche` e `cambia` vicino alla domanda | la prossima task con domande: opzioni leggibili | le domande già aperte restano con A/B/C |
| 5 | **Risposta ≠ scelta provvisoria → task di correzione solo se serve:** il pannello chiede "applico adesso / vale solo per il futuro" | rispondere a una domanda su un documento di idee non crea una task | niente di grave |
| 6 | **File di servizio fuori dal repo** (sezione 1), uno alla volta: prima `agenti/LOG.md` e `ULTIMO_SCRIPT.txt`, poi la parte automatica della scheda, poi `agenti/<id>/` | dopo una task `git status` nel progetto è pulito | Consigli e Revisione leggono `agenti/LOG.md` e i RAPPORTO nel repo (`scheda.py:241, 259`): vanno aggiornati insieme |
| 7 | **Il runner si ferma se la cartella è sporca**, invece di salvare in automatico; controlla i file permessi ignorati da git | modificare un file a mano e lanciare una task: si ferma con un messaggio chiaro | se Leo lavora a mano nei progetti, gli agenti si fermano finché non salva (è voluto) |
| 8 | **Le task partono sempre da `prova`; Rifai = ramo nuovo; le correzioni partono dal ramo giusto** | 2 task di fila: il secondo ramo non contiene il primo; Rifai crea `-r2` | un progetto senza `prova` (Mercatino, progetti nuovi): `prova` va creata da `main` |
| 9 | **`crea_prova.py` → pulsante "Accetta" (unisci in `prova`)**, senza ricreare `prova` e senza stash | accettare una task: il suo DIFF compare in `prova` | conflitti veri: il pulsante deve fermarsi e spiegare, mai unire a metà |
| 10 | **Pulizia dei rami** (sezione 3, passi 1-7) | `CONTROLLA_REPO.bat`: pochi rami, `prova` aggiornata | vedi la tabella della sezione 3 |
| 11 | **Codice morto via** (sezione 2, "Cosa togliere") | il pannello si apre, tutti i pulsanti funzionano, il diario si vede | una funzione creduta morta in realtà usata. Prima si cerca il nome in tutti i file |
| 12 | **Accorpare i file del pannello** (sezione 2) | stessa prova del passo 11 | il pulsante "modifica il pannello" della chat conosce i nomi dei file (`ufficio_extra.py:413`): va aggiornato |
| 13 | **Cartelle vecchie in backup**, `results/` più vecchi di 30 giorni in archivio, doppioni in `generico/` | il pannello mostra le stesse task | il dettaglio delle task vecchie perde le risposte grezze |
| 14 | **"Fatta" più seria:** l'esito non è "ok" se ci sono file rifiutati; le task create dal pannello propongono un controllo in più (per esempio `py_compile` per i `.py`, `node_check` per i `.js`); avviso se un file grande si accorcia di molto | una task che riscrive male un file grande finisce in "Da sistemare" | più task "fallite" all'inizio |
| 15 | **Progetti:** GTT (mappa: gli agenti modificano il template; la mappa si snellisce con una task sua); Langue (obiettivo giornaliero: decidere se farlo davvero, oggi esiste solo in IDEE.md); schede da completare | — | — |

**Passi aggiunti dopo le decisioni del 05/10 sera**

| # | Passo | Come si prova | Cosa può rompersi |
|---|---|---|---|
| 16 | **Via il contatore delle 5 ore, la calibrazione, `PER` e il tetto della chat.** Resta il limite vero di Claude | il pannello si apre senza contatore; la chat non ha più "Sblocca messaggi" | il dispatcher oggi si ferma anche con il "contatore al 100%" (`comune.py:180`): quel controllo va tolto insieme, non da solo |
| 17 | **Classifica unica dei modelli gratis** (sezione 4) | Impostazioni → Motori mostra la classifica; una task usa il primo disponibile | all'inizio la classifica ha pochi dati: si parte dalla grandezza |
| 18 | **Prova di un motore agente** (Codex e/o OpenCode) su una task piccola già fatta, su un ramo a parte | la task finisce, i controlli passano, nessuna riga `claude` nel log | account e limiti esterni: se non va, non si perde niente |
| 19 | **Backup periodico** (sezione 7) | dopo una settimana c'è un backup nuovo e il più vecchio è stato tolto | se il disco si riempie il backup fallisce: serve un avviso |
| 20 | **`C:` in ordine** (sezione 7), un progetto alla volta | il progetto spostato funziona dal pannello (una task di prova) | percorsi scritti fissi nel codice (sezione 7): vanno cambiati tutti insieme |
| 21 | **Candidature come task** (decisione 8): per ultimo, perché è il pezzo più grande | uno scout, un CV e una lettera vanno a buon fine dal nuovo sistema | per qualche giorno le candidature non sono disponibili: farlo quando non ci sono offerte urgenti |

---

## 6. Domande del 05/10

Hanno tutte una risposta: vedi la sezione 0.

---

## 7. `C:` in ordine e backup periodico

### Dove sono le cose oggi (dai percorsi scritti nel codice)
| Cosa | Dove |
|---|---|
| Ufficio | `C:\Users\campe\Desktop\Multiple Agents` |
| Progetti | `Desktop\GTT`, `Desktop\Langue`, `Desktop\timelive_repo`, `Desktop\Timelive` (scheda vecchia?), `Desktop\Projects\Preventivi_Gigi`, `Desktop\Mercatino` |
| Documenti delle candidature | `Desktop\CV` |
| Backup | `C:\BACKUP_UFFICIO` |
| Copia per GitHub | `C:\GITHUB_UFFICIO\multiple-agents` |
| Chiavi | `C:\Users\campe\.ufficio` |

Tutto è sparso tra Desktop, `Desktop\Projects` e la radice di `C:`.

### Proposta: una sola cartella madre
```
C:\Lavori\                    (il nome lo sceglie Leo)
  Ufficio\                    oggi "Multiple Agents"
  Progetti\
    GTT\  Langue\  Timelive\  Preventivi\  Candidature\  (CV e documenti)
  Archivio\                   progetti chiusi (Mercatino) e cartelle vecchie (Desktop\Timelive, _backup_v0.*)
  Backup\                     oggi C:\BACKUP_UFFICIO
  GitHub\                     oggi C:\GITHUB_UFFICIO
```
Sul Desktop resterebbe solo l'icona "Ufficio".

**Cosa può rompersi spostando le cartelle** [visto]. I percorsi sono scritti fissi in molti posti:
- `Ufficio.vbs`;
- `pannello_config.json` (sorgenti, cartelle della chat);
- `progetti/*.json` (cartella, scheda);
- **ogni file task**, nel campo `repo:`;
- `crea_prova.py`, `controlla_repo.py`, `esporta_diff.py` (`DESK / ...`);
- `candidature/runner/state.py` (`DOCS_HOME`);
- l'attività di Windows.

**Proposta:** prima di spostare, un solo file con i percorsi (`percorsi.json`) che tutti leggono. Poi lo spostamento diventa: sposto la cartella, cambio una riga, avvio una task di prova.

### Backup periodico
- `backup_completo.py` esiste già e fa zip + bundle + controllo.
- **Proposta:**
  - un'attività di Windows lo lancia **una volta alla settimana**, di notte, con gli agenti in pausa durante il backup;
  - si tengono gli **ultimi 4** backup;
  - il pannello mostra "ultimo backup: data, esito".
- **Critica:** un backup sullo stesso disco `C:` protegge da errori ed eliminazioni, **non** da un disco rotto o da un PC perso. Serve anche una copia fuori dal PC (disco esterno o cloud).
- La copia su GitHub non basta: non ha la storia dei rami e lascia fuori i file grandi.

### Come vedere i rami (oggi, senza comandi)
- `RAMI_PROGETTI.md` non sta nella cartella dell'Ufficio. Lo crea `CARICA_SU_GITHUB.bat` in `C:\GITHUB_UFFICIO\multiple-agents\RAMI_PROGETTI.md`.
- In alternativa: doppio clic su `Multiple Agents\pulizia\CONTROLLA_REPO.bat`, che scrive `CONTROLLO_REPO.txt` nella stessa cartella. È solo lettura: non cambia niente.
- **Proposta:** una pagina "Rami" nel pannello. Per ogni progetto mostra i rami, quali sono già uniti in `prova` e i pulsanti Accetta / Scarta.

---

## 8. Domande rimaste

1. **La cartella madre:** `C:\Lavori`, oppure un altro nome o posto? Il Desktop è sincronizzato con OneDrive?
   - **Cosa cambia:** se il Desktop è sincronizzato, git e OneDrive possono litigare sui file. Spostare fuori dal Desktop sarebbe un motivo in più.
2. **Backup fuori dal PC:** hai un disco esterno o un cloud dove copiarlo?
   - **Cosa cambia:** senza, il backup periodico protegge solo dagli errori, non dalla rottura del disco.
3. **Ogni quanto il backup:** una volta alla settimana va bene?
   - **Cosa cambia:** più spesso = meno lavoro perso, più spazio usato (oggi un backup pesa circa quanto tutte le cartelle, comprese le zip di GTT da centinaia di MB).
4. **Dati e addestramento:** alcuni fornitori gratis usano i messaggi per addestrare i loro modelli. Va bene per tutti i progetti?
   - **Cosa cambia:** se no, Timelive (dati personali) e Candidature (CV) andrebbero esclusi dai fornitori che lo fanno. Nel piano v0.5 hai scritto "caso per caso".
