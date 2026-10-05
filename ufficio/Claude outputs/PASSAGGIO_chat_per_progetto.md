# Passaggio di consegne: "chat per progetto" nell'Ufficio (05/10/2026)

Documento per una chat nuova, che deve costruire questa parte senza rileggere tutta la storia.

## Contesto in breve

- **Cos'è l'Ufficio:** un pannello locale per agenti AI su più progetti. Gira sul PC Windows di Leo, nella cartella `C:\Users\campe\Desktop\Multiple Agents`. Python standard + un file HTML.
  - si apre dall'icona Ufficio (`run.bat` / `Ufficio.vbs`);
  - il server è `pannello\pannello_server.py`, sulla porta 8765.
- **Leo** non è un programmatore. Vuole spiegazioni semplici, piano e domande prima di costruire, pochi token, test prima di consegnare.
- **Candidature:** vanno trattate come un progetto qualsiasi. Niente lavoro speciale su di loro adesso.
- **Il piano generale** è in `PIANO_v0.5.md` (nella cartella e nel progetto Claude):
  - fase A fatta;
  - "Cosa succede" e "Consumo" fatti;
  - fase B1 (OpenRouter) fatta;
  - motore predefinito dell'Ufficio fatto;
  - mancano: **chat per progetto (questo documento)**, B2 (OpenCode), C (due lavori insieme).

## File che contano

| File | Cosa fa |
|---|---|
| `motori.py` | **Unico punto da cui passano le chiamate ai modelli.** `chiama(prompt, cartella, chi=..., motore=claude/auto/gratis/openrouter, leggi=[file relativi], scrivi=[...])`. Contiene anche: `_openrouter()`, `_colpo_singolo()` (file passati nel messaggio, risposta in blocchi `<<<FILE path>>> … <<<END>>>`), `MOTORI`, `predefinito()`, `chiave()`, `consumo()`, `in_corso()`. Ogni chiamata scrive una riga nel log unico `logs\uso.csv`. |
| `pannello\ufficio_extra.py` | **La chat attuale.** `chat_send(cfg, testo, contesto, vista, default_src, motore)`. Il prompt è in italiano. Le azioni sono righe `@@AZIONE {json}` (lista `AZIONI_OK`), le note `@@NOTA`. Lo stato della chat è in `chat_stato.json` (`storia`, `usati`, limite giornaliero), il log in `chat_log.md`. Con `motore == "gratis"` chiama `motori.chiama(..., motore="gratis")` senza file. Contiene anche la modifica del pannello (`edit_prepare`). |
| `pannello\pannello_server.py` | Route API. La chat usa `/api/chat`, `/api/chat_invia`, `/api/chat_azione`, `/api/chat_sblocca`. `chat_context(cfg)` costruisce il testo dello stato. **Non loggare mai** il body di `/api/chiave`. |
| `pannello\ufficio_dati.py` | Dati della pagina (`stato_ufficio`, `succede`, `gen_tasks`, `progetto()`, `scheda.percorso(p)`), `progetto_salva`, `task_nuova`. |
| `pannello\ufficio.html` | Pagina unica. La chat è nell'`<aside id="chat">`: `send()`, `drawChat()`, select `#chatMot` (Claude/Gratis). La pagina progetto è `openProj(id)`, in un cassetto largo (`drawer.wide`) a due colonne. Aiuti nei "?" tramite `HELP` + `hlp(k)`. |
| `progetti\<id>.json` | Un file per progetto: `cartella`, `motore`, `piano`, `scheda`… |
| `scheda.py` | Scheda progetto: `percorso(p)`, `regole_per_agenti(p)`. |

## Cosa ha deciso Leo

1. **Una chat per progetto, come i Progetti di Claude.**
   - Nella pagina di un progetto, la chat parla di quel progetto.
   - La chat generale dell'Ufficio resta nella pagina principale.
2. **Contesto di ogni chat di progetto:**
   - la Scheda progetto, **sempre**;
   - i **"file di riferimento"** fissati da Leo con un pulsante "fissa nella chat";
   - l'elenco dei file del progetto, le task e lo stato del progetto;
   - un riassunto breve dell'Ufficio.
3. **Cronologia separata** per progetto.
4. **Motore:** segue l'interruttore unico (task → progetto → Ufficio). Si può cambiare al volo con il select, come oggi.
   - il **gratuito** non può aprire file da solo: il pannello mette nel messaggio la Scheda più i file fissati (`motori.chiama(..., leggi=[...])`, `scrivi=[]`);
   - **Claude** in più può leggere la cartella del progetto (`--add-dir` della cartella, strumenti `Read,Glob,Grep`).
5. **Azioni:** le stesse `@@AZIONE` di oggi, con il progetto già impostato; ad esempio `nuova_task` usa il progetto corrente.

## Proposta di realizzazione (da confermare con Leo a piccoli passi)

1. **Dati:** in `chat_stato.json` una chiave per chat: `"chat": {"generale": {...}, "<id progetto>": {"storia": [...]}}`. Va migrato il formato attuale nella chiave "generale". Il limite giornaliero resta unico.
2. **File fissati:**
   - nel `progetti\<id>.json` un campo `chat_file: [percorsi relativi alla cartella]`;
   - endpoint `/api/chat_file` per aggiungere o togliere un file;
   - nella pagina progetto, una sezione "File della chat" con un pulsante "＋ fissa" che apre la cartella del progetto (riusare `/api/dir`).
3. **Backend:** `chat_send(..., progetto=None)`. Se c'è un progetto:
   - contesto = scheda (max ~9.000 caratteri) + stato del progetto + elenco dei file della cartella (max ~200 righe) + file fissati (limite caratteri come `MAX_FILE` / `MAX_TOT` in motori);
   - per Claude: `cartelle_extra=[cartella del progetto]`;
   - motore predefinito = quello del progetto, se il select non dice altro.
4. **Interfaccia:**
   - quando la pagina di un progetto è aperta, la chat a destra passa a quella del progetto: titolo "Chat · Langue", con la sua cronologia;
   - quando si chiude la pagina, torna alla chat generale;
   - le altre azioni restano uguali;
   - poco testo, spiegazioni nei "?".
5. **Test prima di consegnare:**
   - con un Claude finto e un OpenRouter finto;
   - `motori.URL_OPENROUTER` si cambia con la variabile d'ambiente `UFFICIO_OPENROUTER_URL`;
   - `CLAUDE_BIN` o `PATH` puntati a uno script finto;
   - screenshot con Playwright: Chromium è già installato.

## Come si consegna sul PC (importante)

- **Backup:** prima di sovrascrivere, una copia dei file in `_backup_v0.4\<nome passo>\`.
- **Commit:** `device_commit_files` con `stagedPath` in un percorso **nuovo e unico** sotto `/mnt/user-data/outputs/…`, e `expectedMtimeMs` preso da `device_stage_files` / `device_list_dir`.
- **Verifica:** rileggere con `device_stage_files` e confrontare con `cmp`. Su un percorso già usato, `stagedPath` può scrivere contenuto vecchio; in quel caso usare `SendUserFile`, poi `fileUuid` con `force`.
- **Riavvio:** dopo aver cambiato i `.py` del pannello, Leo deve fare Menu > Riavvia Ufficio.
- **Niente comandi sul PC:** non c'è `device_bash`, quindi non si possono cancellare o spostare file. Quando serve, lo si chiede a Leo.

## Dopo la chat per progetto

- **B2:** OpenCode per i task che toccano più file e per le modifiche del pannello con il gratuito. Bash e web vietati in `opencode.json`. Installazione con un `.bat` (`npm i -g opencode-ai` da verificare).
- **C:** due lavori insieme, mai dello stesso progetto (un lucchetto per progetto).
- **Task notturne** che Leo vuole preparare: Langue, Timelive (rifare l'LLM bridge), Preventivi papà.
