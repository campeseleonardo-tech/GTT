# ESITO C1 — riorganizzazione e prova delle pagine (cloud, 22/10/2026)

Piano 1 (passi 4-7) e piano 5 (passi 1 e 9). Ramo della sessione `claude/ecstatic-faraday-nuy8hv`; un commit per punto.
Prima di cominciare: `git fetch --unshallow` e `scripts/controlla_rami.py`: nessun ramo con lavoro fuori da `origin/prova`
(il ramo della sessione era indietro di 7 commit e l'ho portato avanti con un fast-forward).

## Cosa è stato fatto
1. **`sviluppo/`** (piano 1, passo 4): con `git mv` dentro `sviluppo/` ci sono `MEMORIA_PROGETTO.md`, `piani/` (compreso `PROMPT_LAVORI.md`),
   `TESI_E_PROGETTO.md` e `AGENTS.md` completo. In radice `AGENTS.md` è di 7 righe e rimanda a `sviluppo/AGENTS.md` e `sviluppo/MEMORIA_PROGETTO.md`.
   Percorsi vecchi aggiornati con `git grep` in documenti, script (08, 13, 14, 67, 95) e prompt. Restano i vecchi nomi solo in `docs/rapporti/RAPPORTO_FASE5_VERIFICHE.txt`
   (testo scritto dallo script 67: si aggiorna al prossimo lancio) e nella storia dei piani.
2. **Dati di accesso al Pi fuori da git** (passo 5): `scripts/config_locale.esempio.json` (valori finti) e `scripts/config_locale.py` (legge `config_locale.json`
   nella radice, già in `.gitignore`; se manca si ferma con un messaggio che dice come crearlo). IP, utente e percorso della chiave non compaiono più in nessun file in git
   (`git grep` su `192.168`, `leopi@`, `id_gtt`, `/home/leopi` = vuoto). **File che leggono il config:**
   - `scripts/config_locale.py` (modulo e riga di comando: `pi`, `utente`, `indirizzo`, `chiave`, `dir_remota`)
   - `scripts/backup_da_leopi.py` (copia dello storico)
   - `scripts/controlla_leopi.py` (controllo della raccolta)
   - `scripts/RACCOLTA_GIORNALIERA.bat` (chiama `config_locale.py`; poi lancia i due script sopra)
   - `scripts/AGGIORNA_RACCOLTA_LEOPI.bat` (chiama `config_locale.py`)
   - indirettamente `CONTROLLA_LEOPI.bat` e `FETCH_LEOPI_E_VELOCITA_5T.bat` (lanciano gli script sopra).
   `controlla_raccolta_5t.py` e `controlla_raccolta_pk.py` girano sul Pi: usano `~/GTT/data/...` invece di `/home/leopi/...`.
   Nei documenti ora c'è «il Raspberry Pi di casa». Il nome «leopi» resta solo come nome del Pi e dei `.bat`.
3. **Testi puliti** (passo 6): bottone `◎` della mappa con titolo «Tutta l'area»; nella mappa «IMQ 2022» → «indagine sugli spostamenti 2022» (legende, schede zona, guida,
   badge «indagine 2022», nota dell'ora); testi delle schede (`schede_risultati.py`): «IMQ» e «Q001-Q009» sostituiti («i quartieri centrali»), «Fase B», «Versione N», «Prima versione»,
   «Una prima versione» tolti; commenti con «Leo», «Giro 5», «Fase 5» ripuliti. `index.html` e `risultati.html` non avevano niente da togliere. Stessi cambiamenti
   applicati a mano anche a `mappa_torino.html` (22 righe, come nel template). Nessun numero e nessun calcolo toccati. **Non toccato:** gli indirizzi dei codici zona (`Q001`…) dentro i dati
   della mappa (sono identificativi, visibili solo come nomi di zona), le date dei dati misurati («pochi giorni di ottobre», «mercoledì 14/10» nel metodo), le intestazioni
   «(Claude, 20/10/2026)» in testa a molti script (rumore solo nei commenti, tocca farlo quando si apre ogni script).
4. **Script 86** (passo 7): ora `86_controlla_file_pagine.py` (rinominato). Non scrive più `README.md`, non crea `pubblica/`. Legge `index.html`, `risultati.html`,
   `mappa_torino.html`, elenca ogni file caricato (script src, fetch, `ricarica(...)`, gruppi di `data/catalogo/`, pagine collegate) e per ognuno dice «esiste/MANCA» e
   «in git/NON in git» (AVVISO se no). Nel cloud: 9 AVVISO, tutti file di `data/` (oggi `data/` non è in git: lo porta il piano 2). `RIFAI_MAPPA_E_SCHEDE.bat` aggiornato.
5. **`prova_pagine.py`** (piano 5, passo 1; ex `prova_pagine_r6.py`): su Windows Edge/Chrome come prima; altrimenti (o con `--playwright`) Playwright con Chromium
   (anche da `/opt/pw-browsers/chromium-*/chrome-linux/chrome`). Stesse prove: tutti i temi, errori JavaScript, pannello `#jsoff`, titolo della legenda, identificatori R6;
   in più schede `#r10` e screenshot 1440x900 e 390x844 di ingresso, risultati, mappa e viste dei parcheggi in `immagini/`. I file di `data/` mancanti sono «file assente», non errori.
   `requirements.txt`: aggiunto `playwright` (solo per questa prova).
6. **`#p3`/`#r6` senza ricaricare** (piano 5, passo 9): in `risultati.html` evento `hashchange` che richiama la stessa funzione dell'avvio. Provato nel browser: prima non apriva
   niente, ora apre la scheda giusta per `#p3`, `#r6`, `#p5`, `#p1`. La prova è dentro `prova_pagine.py` (solo con Playwright e con `data/schede_risultati.js`).

## Prove (cloud, senza `data/`)
- `python -m py_compile` su tutti i 93 script (`scripts/` e `scripts/prove/`): 0 errori.
- `python scripts/prova_pagine.py` senza `data/`: 19 pagine, 0 errori JavaScript, unici avvisi «file assente»: `data/schede_risultati.js`, `data/processed/orari_fermate.js`,
  `data/catalogo/istruzione.js`. Screenshot fatti.
- Con le schede costruite da `scripts/prove/dati_da_mappa_95.py` + `95_case_fragilita_servizi.py` + `prove/prova_scheda_case.py` (schede 1, 4, 6, 8 **finte**, scheda 5 con
  numeri indicativi): prova pagine 19 pagine, 0 errori, cambio di indirizzo OK.
- Screenshot prima/dopo (1440x900) di `index`, `risultati`, scheda 3, scheda 5, `mappa`, `mappa#tema=imq`, `mappa#tema=interscambio&vista=parcheggi`: ingresso, risultati, schede e mappa
  iniziale identici pixel per pixel; nella mappa cambiano solo i testi voluti (legenda e guida di «Spostamenti», fonti dei parcheggi).

## Cosa deve fare Leo sul PC (giro P1)
1. Unire il ramo in `prova` (comandi nella chiusura del messaggio) e fare `git pull`.
2. Creare `config_locale.json` nella radice copiando `scripts\config_locale.esempio.json` con i valori veri (indirizzo, utente, chiave del Pi). Non finisce in git.
3. Provare `scripts\CONTROLLA_LEOPI.bat` (deve dare lo stesso esito di prima) e, alla prossima occasione, `RACCOLTA_GIORNALIERA.bat` (anche l'attività pianificata la usa).
4. Lanciare `scripts\RIFAI_MAPPA_E_SCHEDE.bat`: rigenera `mappa_torino.html` e le schede, lo script 86 elenca i file e **non** tocca `README.md`; poi `python scripts\prova_pagine.py` = 0 errori.
5. Aprire `index.html` e `risultati.html`: numeri uguali a prima, nessuna sigla (IMQ, Q001…); nella mappa, tema «Spostamenti»: «indagine sugli spostamenti 2022»; passando sul bottone `◎` compare «Tutta l'area».
