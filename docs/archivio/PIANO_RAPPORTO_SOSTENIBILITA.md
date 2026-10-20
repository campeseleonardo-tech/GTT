# Piano — agente leggero per il Rapporto di sostenibilità GTT 2025

Stato: **solo piano, niente costruito** (16/10/2026). Si costruisce dopo l'OK di Leo.

## 1. Cosa deve fare
Leggere `data/rapporto_di_sostenibilita_2025.pdf`, trovare i dati utili al progetto (mappa, scenari, calibrazione, "veicoli in meno") e scriverli in un **riassunto molto corto** con la pagina di origine. Solo questo PDF, per ora.

## 2. Decisioni di Leo (16/10)
- Il contesto è il progetto GTT; i temi li sceglie Claude (sezione 5).
- Lunghezza e numeri di pagina: a discrezione di Claude → **1 pagina (~350 parole) + tabella dei numeri chiave; ogni dato con pagina stampata e pagina PDF** (scarto di 2: pagina stampata 28 = pagina PDF 30).
- Metodo: **script locale + modello DeepSeek V4 Flash**.
- Grafici-immagine: **saltati, senza segnalarli**.
- Solo questo PDF. Memoria: piano ora, dati chiave dopo l'estrazione.

## 3. Cosa ho verificato sul PDF
- 162 pagine, A4, con **testo vero** (niente OCR). Circa 790.000 caratteri ≈ 200.000 token.
- Pagina stampata 28: **tabelle in testo** (passeggeri 2023-2025: bus urbano 183,7 M, extraurbano 15,8 M, tram 52,7 M, metro 48,3 M; 187 km di binari tram, 8 linee, 180 tram; metro 23 fermate su 15,1 km, 58 convogli; area servita 5.665 km²). Quindi l'estrazione funziona.
- Pagina stampata 29: GTT gestisce la sosta su strada a Torino e 30 parcheggi (anche Park & Ride) → collegato al Risultato 6.
- Pagine vuote o quasi (copertina, separatori): da scartare in automatico.

## 4. Il PC (controllo)
Da qui **non posso lanciare comandi sul PC**, quindi non posso dire cosa è installato. Dai file del progetto risulta: Python 3.14 nel PATH (no Anaconda); gli script usano solo librerie standard + pandas/geopandas/r5py/osmium; **nessuno usa una libreria PDF**. Non so se esiste già una chiave API DeepSeek (opencode non è la stessa cosa).
→ Il passo 0 è un `.bat` che controlla e dice a Leo cosa vede (sezione 6).

## 5. Temi da cercare (scelti da Claude, in ordine di utilità)
1. **Come si spostano le persone**: passeggeri per mezzo (bus urbano/extraurbano, tram, metro), andamento 2023-25, ripartizione modale, passeggeri-km, indagini sulla mobilità.
2. **Offerta**: km di rete, linee, fermate, flotta (tipo, alimentazione, età), vetture-km, corse, area servita, frequenze.
3. **Qualità**: puntualità, regolarità, affollamento/capienza, soddisfazione dei clienti, reclami (serve a Risultato 4 e al "MANCA" passeggeri/affollamento).
4. **Auto e ambiente**: emissioni, auto evitate / CO₂ risparmiata, quota mezzi elettrici/ibridi, piani di transizione (serve alla metrica "veicoli in meno").
5. **Parcheggi e sosta**: posti, parcheggi di interscambio/Park & Ride, ricavi sosta, ZTL (Risultati 6 e 8).
6. **Economia**: ricavi da biglietti/abbonamenti, costi, contributi, tariffe, abbonati.
7. **Accessibilità e sicurezza**: mezzi accessibili, incidenti, aggressioni, vandalismi.
8. **Progetti futuri**: prolungamento metro, nuove linee, investimenti.
Regola: se un dato non è nel testo, non si scrive. Si preferiscono numeri a frasi generiche ("impegno per la sostenibilità" non serve).

## 6. Come funziona (4 passi, numero script libero: 30)

**Passo 0 — controllo PC** (`RAPPORTO_CONTROLLA.bat`, doppio clic): mostra versione Python, se c'è `pypdf` (libreria PDF pura Python, sicura su Python 3.14; `pymupdf` può non avere versioni per 3.14), se c'è la chiave DeepSeek. Se manca `pypdf` propone `pip install pypdf`. Nessun file toccato.

**Passo 1 — estrazione locale, 0 token** (`scripts/30_rapporto_estrai.py`): legge una **copia** del PDF, estrae il testo pagina per pagina, calcola la pagina stampata (PDF − 2, controllata sul numero scritto in fondo alla pagina), scarta pagine quasi vuote e indici/note legali. Scrive `data/processed/rapporto_gtt/pagine.json`.

**Passo 2 — estrazione con DeepSeek Flash** (`scripts/31_rapporto_fatti.py`):
- blocchi da 4 pagine con 1 di sovrapposizione (le tabelle spesso passano la pagina);
- per blocco: richiesta con contesto del progetto + temi + regole → risposta **in JSON**: `tema, dato, valore, unità, anno, pagina_stampata, pagina_pdf, frase_originale (≤15 parole)`; "nessun dato utile" ammesso;
- temperatura 0; **salva ogni blocco appena finito** (se si ferma, riparte da dove era); limite massimo di token e di chiamate scritto nello script.

**Passo 3 — controllo locale, 0 token** (stesso script): ogni numero restituito deve comparire **identico nel testo del blocco** (formato italiano 183.675.867 e simili); quelli che non compaiono vengono scartati e contati. Poi unisce i doppioni e ordina per tema. Scrive `data/processed/rapporto_gtt/fatti.json`.

**Passo 4 — riassunto** (`scripts/32_rapporto_riassunto.py`, 1 sola chiamata): riceve **solo i fatti verificati** e scrive il riassunto breve → `docs/RIASSUNTO_RAPPORTO_SOSTENIBILITA_2025.md`. Etichetta dati: **[DICHIARATO GTT]** (proposta, aggiunta ai tag esistenti), perché sono numeri dell'azienda, non misurati da noi.

Tutti con `.bat` a doppio clic e log in `logs/`, come gli altri.

## 7. Costo (stime, da verificare al primo giro)
DeepSeek V4 Flash (nome API `deepseek-flash`, il vecchio `deepseek-v4-flash` ancora accettato; fonte: documentazione DeepSeek): 0,15-0,30 $ per milione di token in ingresso, 0,60-1,20 $ in uscita (meno nelle ore non di punta). Il rapporto intero (≈200.000 token, qualche migliaio in più per le istruzioni ripetute e la sovrapposizione) + ≈30.000 di uscita → **circa 0,1 $ per il giro completo**. Quindi filtrare per parole chiave per risparmiare non conviene: rischia solo di perdere dati. Il filtro locale serve solo a togliere pagine inutili.

## 8. Prove (come da regole: prima su copia, originale intatto)
1. Copia del PDF in `data/processed/rapporto_gtt/`; l'originale non si tocca.
2. **Pilota su 4 pagine** (PDF 29-32, quelle con la ripartizione tra mezzi): Leo o Claude confronta i numeri con il PDF a mano. Se anche uno è sbagliato, si ferma e si corregge il prompt.
3. Poi 10 pagine a caso, poi il giro completo.
4. Controllo finale su 5 dati scelti a caso, confrontati col PDF.
Atteso: i 4 valori di passeggeri e 3 dati metro/tram di pagina 28 compaiono tutti, con pagina giusta.

## 9. Rischi onesti
- Le tabelle estratte come testo possono mescolare le colonne (2025/2024/2023): il controllo "numero presente nel testo" non basta a garantire l'anno giusto → il pilota guarda proprio questo.
- Saltando i grafici-immagine, il riassunto può **sottostimare** cosa dice il rapporto (non lo segnaleremo nel riassunto, come deciso, ma resta il limite).
- DeepSeek è un servizio esterno: al modello va solo il testo pubblico del rapporto, nessun dato personale.
- Un riassunto di 1 pagina taglia per forza: il dettaglio resta in `fatti.json`.

## 10. Da fare / aperto
- Leo: dà l'OK a questo piano e dice se ha già una chiave DeepSeek (se no, crearla sul sito DeepSeek; va in un file locale non versionato, mai nel codice né in git).
- Default se non dice altro: chiave letta da `chiave_deepseek.txt` nella radice (da aggiungere a `.gitignore`).
