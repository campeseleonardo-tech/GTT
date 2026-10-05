# Multiple Agents: piano v0.5

*Scritto il 04/10/2026 dalla chat di controllo. Sostituisce `PIANO_multi_agent.md` (v0.4).*

## In una frase

Riordinare l'Ufficio perché ci siano **un solo punto da cui si chiamano i modelli e un solo log del consumo**. Poi far lavorare i task anche su **modelli gratuiti** al posto di Claude. Solo alla fine far girare **due task insieme**.
Regola guida: **semplice adesso**; il resto va nell'elenco "Dopo", in fondo.

---

## Dove siamo (04/10 sera)

- **Due runner** che fanno lo stesso mestiere: `candidature\runner\runner.py` e `generico\runner.py`. Li coordina `dispatcher.py`, che lavora un task alla volta ogni 5 minuti con la rotazione 3-2-1.
- **Due formati di task:** i job dentro `candidature\stato\stato.json` (190 KB) e i file `.task.md` in `generico\`.
- **Tre file di consumo separati:** `candidature\stato\uso.csv`, `generico\logs\usage.csv` e `pannello\chat_uso.csv`.
- **Ogni task usa Claude** (`claude -p`, sonnet, `--restricted`).
- **Agenti fermi:** il file STOP c'è dalle 17:51 del 04/10. In coda ci sono GT04 e GT05.

| Progetto | Priorità | Stato |
|---|---|---|
| Candidature | alta | scout in corso, fermo per limite alle 02:05; CV e lettere non ancora fatti nella nuova struttura |
| Langue | media | contenuti v1 e v2 e sito fatti; manca la prova con utenti |
| GTT | media | GT01 e GT02 fatti; GT04 e GT05 in coda; 3 domande aperte |
| Preventivi | bassa | resta il logo nel Word (gli agenti non possono modificare Word) |
| Timelive | bassa | solo idee, i test richiedono WSL2 |
| Mercatino | — | archiviato, M01 sospeso |

---

## Decisioni di Leo

- Il sistema deve poter usare **più modelli**. Non dipendere né da Claude né da un solo programma.
- Il Claude Pro resta per **costruire** (pannello e sistema) da queste chat. Gli agenti devono consumarlo il meno possibile.
- Va bene condividere i dati con i fornitori gratuiti; caso per caso se serve.
- **Controllo = log ben fatti e corti**, da cui si capisce se tutto è andato nella direzione giusta.
- **Tre fasi in sequenza**, ognuna provata prima della successiva.
- **Pannello: si ristruttura**, non si rifà. Resta l'interfaccia v2.
- **Le candidature diventano un progetto come gli altri.**
- **Raspberry Pi e LLM locale: dopo.** Resta come idea per un hardware dedicato ai task semplici e ripetitivi.
- **OpenRouter con 10 $ una tantum**, per imparare quali modelli funzionano e un giorno farne a meno.
- **Account:** OpenRouter, ChatGPT (già presente), gli altri solo se si entra con Google.
- **Restare semplici:** niente database, niente framework, niente 20 motori adesso.

---

## Fase A: unificare e pulire, FATTA il 04/10 (versione semplice scelta da Leo)

Dopo aver letto il codice, si è scelta una versione più semplice di quella prevista. Il dispatcher unificava già la scelta dei task e `comune.py` le regole comuni. Il vero doppione erano le **chiamate a Claude, sparse in 6 punti**, e i **3 file di consumo**.

**Fatto:**
1. **`motori.py`**: l'unico punto da cui passano tutte le chiamate ai modelli (task generici, correzioni del validatore, candidature, chat del pannello, modifiche del pannello). Oggi c'è solo Claude; nella fase B i motori gratuiti si aggiungono solo qui.
2. **Un solo log del consumo: `logs\uso.csv`.**
   - Contiene una riga per chiamata (chi, progetto, task, fase, motore, modello, token, costo, secondi, esito) e una riga "esito" per ogni task finito.
   - I 3 log vecchi vengono copiati dentro una volta sola, poi non sono più usati: si possono cancellare dopo una giornata di prova.
   - Il contatore d'uso, il diario, la Sala controllo e le schede dei task leggono da qui.
3. **Le candidature restano con la loro coda** in `stato.json`, perché il pannello è costruito attorno a quella. Cambia solo il modo in cui chiamano Claude.
4. **Pagina `/vecchio` tolta dal server.** I file della pulizia li hai eliminati tu.
5. **LEGGIMI aggiornati:** quello principale, quello di `generico` e quello di `pannello`.
6. **Backup** dei file cambiati in `_backup_v0.4\`: uno solo, da cancellare quando tutto funziona.

**Come è stata provata (sul cloud, con un Claude finto):**
- task con repository, validatore con 2 correzioni, task semplice;
- dispatcher con il diario;
- chat del pannello;
- chiamate delle candidature, anche con limite di Claude e prova a secco;
- dati del pannello identici alla versione precedente.

**Da provare tu sul PC:**
- Menu > Riavvia Ufficio;
- togli lo STOP;
- lasci girare GT04 e GT05;
- controlli che pannello, diario e contatore si vedano come prima;
- poi uno scout delle candidature.

**Prossimo:** la fase B.

---

## Fase B: motori gratuiti (pochi, semplici)

**Obiettivo:** i task girano prima sui modelli gratuiti; Claude solo dove serve.

1. **Due modi di eseguire un task.** Li sceglie il runner in base al tipo di task, non sei tu a deciderlo.
   - **Colpo singolo.** Python prepara il contesto, il modello risponde una volta, Python scrive i file e lancia i controlli. Serve per contenuti, analisi, riassunti ed estrazioni: ad esempio Langue parole, frasi ed errori, e l'analisi delle offerte.
   - **Agente.** Il modello legge e modifica più file. Serve per il codice: GTT e il sito di Langue.
2. **Solo tre motori all'inizio:**

   | Motore | Per cosa | Come |
   |---|---|---|
   | `openrouter` | colpo singolo | API di OpenRouter, modelli gratuiti; il log segna quale modello ha risposto |
   | `opencode` | agente | programma OpenCode collegato a OpenRouter |
   | `claude` | ultima spiaggia, o task marcati `motore: claude` | come oggi |

3. **Catena semplice, uguale per tutti:** si prova il gratuito; se i controlli falliscono si fanno 2 tentativi con l'errore spiegato; se fallisce ancora si passa a Claude. Le lettere delle candidature restano `motore: claude` fino a prova contraria.
4. **Cosa vedi nel pannello:**
   - su ogni task un'etichetta con motore e modello (ad esempio "OpenRouter · nemotron");
   - nel contatore d'uso, Claude e gratuiti separati.
5. **Log corto per ogni task**, una riga nel diario più un riassunto di massimo 10 righe nel risultato: motore, modello, token, tentativi, esito dei controlli, file toccati.

**Come si prova: una piccola gara su task già fatti da Claude.**
- **Colpo singolo:** rifare T12 (parole), su una copia dei file di Langue.
- **Agente:** rifare GT01 (sfondi), su un ramo git separato.
- **Criteri decisi prima:** i controlli passano, il numero di tentativi, il tempo, il tuo giudizio veloce ("va bene / no").

**Fatto quando:** almeno metà dei task nuovi di Langue e GTT finisce senza Claude, e i log ti bastano per capire cosa è successo.

**Da fare tu:** creare l'account OpenRouter, ricaricare 10 $ e incollare la chiave nelle Impostazioni del pannello (ti guido io al momento).

---

## Fase C: due alla volta

**Obiettivo:** più lavoro nello stesso tempo, senza rischi.

1. **Massimo 2 task insieme:** uno con Claude e uno con un motore gratuito, oppure due gratuiti.
2. **Mai due task dello stesso progetto insieme** (un "lucchetto" per progetto), così non si pestano i file.
3. La rotazione 3-2-1 resta: il secondo posto lo prende il prossimo progetto in rotazione che ha un task pronto.

**Come si prova:** una giornata con Langue e GTT in coda insieme, controllando nei log che non ci siano sovrapposizioni.

**Fatto quando:** due task di progetti diversi finiscono insieme senza errori, e il pannello mostra entrambi gli agenti al lavoro.

---

## Dopo (non ora, ma tenuto a mente)

| Idea | Quando ha senso |
|---|---|
| Più fornitori gratuiti (Groq, Cerebras, Mistral, Google AI Studio) | quando OpenRouter non basta o dà troppi "occupato" |
| Codex con il tuo ChatGPT gratuito | per avere una seconda quota agente gratuita |
| Gara tra programmi agente (OpenCode, Cline, Kilo, Goose) | se OpenCode delude o cambia condizioni |
| Classifica dei modelli dai log ("per X va bene Y") | dopo qualche settimana di dati |
| Collegarsi direttamente ai fornitori, senza OpenRouter | quando la classifica è chiara |
| Candidature come task `.task.md` con un solo runner (era nella fase A) | se il doppio runner dà problemi o serve il parallelo sulle candidature |
| Database SQLite al posto dei file JSON | se i file diventano lenti o si rompono con più agenti |
| Più di 2 task insieme | se 2 non bastano e la RAM regge |
| "Rifallo con un altro motore" (pulsante) | quando i motori sono più di 3 |
| Ritentativo automatico più tardi per i task falliti per limite | se capita spesso |
| WSL2 con sandbox (agenti che eseguono test e comandi) | per Timelive e per test veri su GTT |
| Hardware dedicato con LLM locale (Pi o altro) | per i task costanti e meccanici |
| Notifiche sul telefono | quando l'Ufficio lavora molto senza di te |
| Mondo (mappa gioco) | in parallelo, quando ti va |

---

## Rischi

- **Qualità dei gratuiti:** per tedesco, lettere e codice potrebbe essere peggiore. Per questo c'è la gara della fase B e Claude come ultima spiaggia.
- **I gratuiti cambiano:** modelli che spariscono e limiti che scendono. La catena di fallback e gli adattatori separati servono a non bloccarsi.
- **Fase A tocca le candidature:** per qualche giorno il flusso candidature va riprovato. Si fa quando non hai offerte urgenti.
- **Agenti senza comandi su Windows:** restano senza Bash finché non c'è WSL2. I controlli li fa il runner in Python.

## Ordine dei lavori

1. Tu: pulizia dei file e togli lo STOP quando vuoi che riprendano.
2. Fase A: fatta (04/10); tu la provi sul PC.
3. Tu: account OpenRouter e 10 $.
4. Fase B con la gara, poi la decisione.
5. Fase C.
