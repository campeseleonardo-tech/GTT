# Piano meccanico — Correzioni generali del progetto e del Risultato 6 (20/10/2026)

Scritto da Claude con Leo, per un altro modello (agente) che lavora sul PC di Leo. Il perché di ogni correzione è
in `docs/ANALISI_PROGETTO.md` e `docs/ANALISI_RISULTATO6.md` (non serve rileggerli per eseguire).

**Il codice è già scritto e provato da Claude** su dati finti (rete stradale a griglia, zone, fermate, parcheggi):
gli script girano, l'instradamento coincide con un calcolo indipendente (networkx), mappa e scheda si aprono senza
errori in un browser. **Il tuo compito è lanciarli sui dati veri, nell'ordine, controllare i numeri, correggere
solo errori evidenti, fare le poche cose rimaste e scrivere l'esito.** Non devi riprogettare niente.

## 0. Regole

1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (`git branch --show-current`; se no: FERMATI e dillo a
   Leo). **Nessun commit.** `python` del PATH (3.14), **mai Anaconda**.
2. Sola lettura su `data/raw/`, `data/storico_backup.sqlite` e sul Raspberry Pi. In `data/ref/` una sola modifica
   (passo 3.1).
3. Esegui i passi **nell'ordine, uno alla volta, senza fermarti a chiedere**. Dopo ogni passo scrivi in
   `docs/ESITO_CORREZIONI_GENERALI.md` una riga `PASSO x.y: OK` / `AVVISI` / `FERMO – motivo` e i numeri richiesti.
4. Gli script stampano `OK`, `AVVISO` o `ERRORE`. **AVVISO** = numero da guardare: scrivilo nell'esito e vai
   avanti. **ERRORE** (lo script si ferma) = guarda la sezione «Se qualcosa va storto»; se non è lì, scrivi cosa
   hai visto, segna FERMO e salta ai passi che non dipendono da quello.
5. **Correggi il codice solo se** l'errore è chiaro e la correzione è piccola (un nome di campo, un percorso,
   un import). Scrivi nell'esito ogni riga cambiata. **Non cambiare** valori, soglie, regole, testi pubblici.
6. Mai numeri scritti a mano in template, schede o README: vengono sempre dai file.

## 1. Valori decisi (già nel codice come costanti e opzioni; non cambiarli)

| Cosa | Valore | Dove |
|---|---|---|
| Zona centrale, per fermate **e** parcheggi | Q001-Q009 | `scripts/comuni.py` |
| Auto | conducente (03) + car sharing (21); i passeggeri (04) sono persone, non auto | 81 |
| Mattino | partenza 06:00-09:59 | 81 |
| Torinesi nella domanda | sì se le auto dai quartieri periferici verso Q001-Q009 sono ≥ 25% di quelle che entrano da fuori; se no solo cintura | 81 |
| Fermate importanti | 10% più alto fra i luoghi della Città metropolitana fuori da Q001-Q009; segnali a2, b2, c4, e con pesi uguali | 83 |
| Parcheggi adatti | aperti, fuori da Q001-Q009, ≥ 20 posti, non di ospedali/università/centri commerciali | 82 |
| Distanza | 400 m a piedi = linea d'aria × 1,3 | 84 |
| Fermata coperta | **niente soglia fissa di posti**: posti adatti ≥ auto da fermare (auto che passano × quota di chi già oggi lascia l'auto); sotto 20 auto da fermare = «poche auto da fermare» | 84 |
| Aree | esagoni lato 900 m; colorate solo con ≥ 5 fermate valutate, se no «Pochi dati» | 84 |
| Date tipiche della mappa | 10/11/2026 (martedì), 14/11 (sabato), 15/11 (domenica) | 04 |

## 2. Cosa ha già cambiato Claude (non rifarlo)

- **Nuovi**: `scripts/comuni.py`; `81_auto_di_passaggio.py` (auto in entrata che passano accanto a ogni luogo),
  `82_parcheggi_adatti.py`, `83_fermate_importanti.py`, `84_risultato6_parcheggi.py` (prende il posto dell'80),
  `85_verifiche_correzioni.py` (verifiche indipendenti), `86_prepara_pubblicazione.py` (cartella `pubblica/` e
  README); `controlla_leopi.py` + `CONTROLLA_LEOPI.bat`; `RISULTATO6_RIFAI.bat`; `requirements.txt` (senza versioni).
- **Modificati**: `79_dati_mappa_r6.py` (legge l'84; avvisi invece di arresti); `mappa_template.html` (tema R6
  coi campi nuovi; accessibilità in forma compatta riespansa all'avvio; «Negozi e attività commerciali» al posto di
  «Negozi di alimentari»); `04_genera_mappa.py` (date fisse, accessibilità compatta: mappa da ~23,6 a ~13 MB, niente
  posizioni dei mezzi del 3/10); `schede_risultati.py` (scheda R6 nuova con verifica e riassunto in inglese; R2 con
  un secondo numero più severo); `simulazione.html` (sezioni «Il metodo funziona?» e «In English»);
  `29_risultato2_metro_notte.py` (residenti con almeno il 25% di servizi in più); `73` e `75` (avvisi invece di
  arresti); `prova_pagine_r6.py` (tutti i temi, `--cartella`, `--senza-screenshot`).
- **Spostati** (nessuna cancellazione): piani ed esiti superati del R6 in `docs/archivio/r6/`; i `.bat` della radice
  in `scripts/` (ora fanno `cd /d "%~dp0.."`).

---

## FASE 0 — Preparazione

**0.0 Scaricare da GitHub tutto il lavoro di Claude** (prima di ogni altra cosa).
```
git checkout prova
git status
```
Se `git status` mostra file modificati o nuovi in `scripts/`, `docs/`, `simulazione.html`, `MEMORIA_PROGETTO.md`:
**FERMATI** e scrivi a Leo l'elenco (il pull potrebbe sovrascriverli o andare in conflitto). File solo in `data/`,
`logs/`, `immagini/` non contano (git li ignora). Se è pulito:
```
git fetch origin
git pull --ff-only origin prova
git log -3 --oneline
```
Controlli: il pull finisce senza errori né conflitti; nel log c'è il commit «Correzioni generali: codice del Risultato 6
corretto…»; esistono `scripts\81_auto_di_passaggio.py`, `scripts\84_risultato6_parcheggi.py`, `scripts\comuni.py`,
`scripts\RISULTATO6_RIFAI.bat` e `docs\archivio\r6\`. Se il pull fallisce (conflitto, «not possible to fast-forward»,
rete): **FERMATI**, non provare a risolvere, scrivi a Leo il messaggio esatto. **Solo se il pull è a posto si procede.**


**0.1** `git branch --show-current` → `prova`. `git status` → scrivi nell'esito i file modificati prima di iniziare.
**0.2** Crea `docs/ESITO_CORREZIONI_GENERALI.md` (titolo, data, ora di inizio).
**0.3** Copie di sicurezza (non sovrascrivere se esistono già):
```
mkdir data\backup
xcopy /E /I /Y data\processed\risultato6_v2 data\backup\risultato6_v2_prima_correzioni
copy mappa_torino.html data\backup\mappa_torino_prima_correzioni.html
copy data\schede_risultati.js data\backup\schede_risultati_prima_correzioni.js
```
**0.4** Numeri di partenza (per il confronto finale). Lancia e copia l'uscita nell'esito:
```
python -c "import json;d=json.load(open('data/processed/risultato6_v2/mappa_r6.json',encoding='utf-8'));from collections import Counter as C;print('fermate',len(d['fermate']),dict(C(f['classe'] for f in d['fermate'])));print('aree',dict(C(a['categoria'] for a in d['aree'])));print('punti',[p['nome'] for p in d['punti_prioritari']]);print('parcheggi',len(d['parcheggi']))"
```
**0.5** Librerie: `python -c "import numpy, scipy, pandas, shapely, pyproj, osmium; print('ok')"`. Deve stampare
`ok` (se manca una libreria: FERMO generale, dillo a Leo). Poi per ognuna `python -m pip show <nome>` e scrivi in
`requirements.txt` la versione accanto al nome (es. `numpy==2.1.3`); networkx, pypdf, matplotlib solo se installate.
**0.6** `python scripts\comuni.py` → 4 righe `OK`.

## FASE 1 — Risultato 6: la catena nuova, passo per passo

Ogni script scrive un rapporto in `docs/`. Dopo ogni passo copia nell'esito le righe indicate.

**1.1 Script già esistenti, da rilanciare** (servono dati aggiornati: riempimento, zone dei parcheggi, segnali):
```
python scripts\71_parcheggi_riempimento.py
python scripts\72_nodi_tp.py
python scripts\73_segnali_criticita.py
```
Controllo: nessun errore. Il 73 ora può stampare `AVVISO: c2 diverso...`: è normale, scrivilo.

**1.2 Auto che passano, prova veloce**: `python scripts\81_auto_di_passaggio.py --prova`
Controllo: arriva a `Scritto: ...auto_passaggio.json`; nessun `ERRORE`; la riga `metodo per c4` (nel rapporto
`docs/RAPPORTO_R6_AUTO_PASSAGGIO.txt`) dice `instradamento`. Se dice `ripiego`, leggi l'AVVISO
`instradamento riuscito` e vai a «Se qualcosa va storto».

**1.3 Auto che passano, giro completo**: `python scripts\81_auto_di_passaggio.py` (pochi minuti). Nell'esito copia
la sezione «Domanda del mattino» e i «15 luoghi» del rapporto, più la durata. Controlli (se non tornano: AVVISO
nell'esito, si va avanti):
- `M_cint` è **minore** di 95.297 (prima si contavano anche i passeggeri) e maggiore di 50.000;
- `quota_mattino` fra 5% e 40%;
- la riga «torinesi nella domanda» dice SI o NO con il rapporto in percentuale (è una decisione automatica);
- perdita della domanda sotto il 15%;
- fra i 15 luoghi in cima ci sono strade d'ingresso note (Corso Francia, Corso Unione Sovietica, Strada Genova,
  Corso Giulio Cesare/Torino-Milano, la tangenziale…).

**1.4 Parcheggi adatti**: `python scripts\82_parcheggi_adatti.py` (qualche minuto: legge il PBF).
Nell'esito: la «Catena dei conteggi», i «Motivi», i 20 esclusi perché di destinazione. Controlli: `aree trovate`
più di 50; adatti meno di 3.431; tutti e 5 gli interscambi ufficiali fuori centro risultano adatti; fra gli esclusi
per destinazione ci sono ospedali e centri commerciali veri (es. Le Gru, ospedali di periferia).

**1.5 Fermate importanti**: `python scripts\83_fermate_importanti.py`
Nell'esito: la riga con luoghi/eleggibili/soglia/fermate importanti, le 30 in cima, «per zona», sensibilità,
confronto con S2. Controlli: le fermate importanti sono circa il 10% degli eleggibili; **nessuna** in Q001-Q009
(lo script si ferma da solo se succede); `c4 presente per tutti`.

**1.6 Risultato**: `python scripts\84_risultato6_parcheggi.py`
Nell'esito copia dal rapporto `docs/RAPPORTO_R6_PARCHEGGI.txt`: «Fermate importanti», «Aree» (solo la riga del
conteggio), i «20 punti», la «Validazione», il «Controllo a posteriori», i «Controlli». Controlli:
- la somma delle 4 classi = numero di fermate importanti;
- 20 punti (se meno: AVVISO, non errore); per ognuno km dal centro, auto che passano, posti che mancano;
- la tabella di validazione ha 5 righe (Stura, Caio Mario, Sofia, Venchi Unica, Fermi) con un esito ciascuna.

**1.7 Dati per la mappa**: `python scripts\79_dati_mappa_r6.py` → `mappa_r6.json` sotto 1,5 MB, nessun ERRORE.

**1.8 Verifiche indipendenti**: `python scripts\85_verifiche_correzioni.py` → deve finire con
`Verifiche non superate: 0`. Copia nell'esito tutto `docs/RAPPORTO_R6_VERIFICHE_CORREZIONI.txt`. Se una verifica
non torna: guarda «Se qualcosa va storto»; se non capisci la causa, FERMO su questa fase (scrivi la riga) e
continua con la FASE 3.

## FASE 2 — Mappa, schede, prova delle pagine

**2.1** `python scripts\04_genera_mappa.py`. Nell'esito: peso di `mappa_torino.html` (atteso **circa 13 MB**, era
23,6), le date di riferimento stampate (devono essere 10/11, 14/11, 15/11, senza AVVISO), eventuali AVVISI.
**2.2** `python scripts\schede_risultati.py` → righe per R1, R2, R4, R6, R8, R9 senza errori.
**2.3** `python scripts\prova_pagine_r6.py` → deve finire con `OK: nessun errore a runtime sulle 13 pagine` e fare
gli screenshot `immagini\r6_parcheggi.png`, `r6_aree.png`, `r6_mancano.png` (sopra i 20 KB). Se trova errori:
copia le righe nell'esito; correggi solo se l'errore indica chiaramente una riga del template cambiata da Claude
(cerca il nome della funzione in `scripts\mappa_template.html`), poi ripeti 2.1-2.3.
**2.4** Controllo dei testi pubblici: in `data\schede_risultati.js`, nella scheda del Risultato 6, non devono
comparire «utile», «osservazion», «versione», «scenario», «S2», «S4», «nodo forte», «fonte_stato», «Fermi sempre
pieno». Comando (deve stampare `[]`):
```
python -c "import json,re;t=open('data/schede_risultati.js',encoding='utf-8').read();s=json.loads(t[t.index('['):t.rstrip().rstrip(';').rindex(']')+1]);r6=json.dumps([x for x in s if x.get('risultato')=='6'],ensure_ascii=False).lower();print(sorted(set(re.findall(r'\b(utile|osservazion\w*|versione|scenario|s2|s4|nodo forte|fonte_stato|sempre pieno)\b',r6))))"
```

## FASE 3 — Piccole cose rimaste

**3.1 Osservazione di Leo su Fermi** (solo controllo a posteriori). Apri `data\ref\parcheggi_osservazioni.json`;
nella voce di Fermi aggiungi (o, se esiste già, completa) il campo
`"nota": "sempre pieno; i parcheggi gratuiti intorno si riempiono soprattutto al mattino (Leo, 20/10/2026)"`.
Non cambiare coordinate né raggio. Poi `python scripts\84_risultato6_parcheggi.py` e
`python scripts\79_dati_mappa_r6.py`; nell'esito la riga «Controllo a posteriori» del rapporto.
**3.2 Risultato 2, numero più severo**: doppio clic su `scripts\RISULTATO2_RICALCOLA_NUMERI.bat` (pochi secondi),
poi `python scripts\schede_risultati.py`. Nell'esito: da `data\processed\risultato2_metro_notte.json` i valori
`residenti_migliorati` e `residenti_migliorati_quota` per `notte15` e `notte30` (il secondo deve essere minore del
primo).
**3.3 Riassunti in inglese** (`scripts\schede_risultati.py`). La scheda R6 ce l'ha già (`"in_english"` in
`scheda_r6`: usala come modello). Aggiungi la chiave `"in_english"` (lista di 3-4 frasi) a `scheda_r1`,
`scheda_r4`, `scheda_r8`, `scheda_r9` (nel dizionario che ritornano) e a `arricchisci_r2` (dentro `s.update({...})`):
- frase 1: «Question: …» = traduzione di `"domanda"`;
- frase 2-3: la risposta, **con gli stessi numeri e le stesse variabili** usate nelle frasi di `"risposta"` di quella
  funzione, formattati all'inglese (`f"{x:,}"`, punto decimale);
- ultima frase: «Limits: …» = il limite più importante della lista `"limiti"`.
Niente numeri scritti a mano. Poi `python scripts\schede_risultati.py` e `python scripts\prova_pagine_r6.py
--senza-screenshot`. Nell'esito incolla le frasi prodotte (da `data\schede_risultati.js`).
**3.4 Cartella da pubblicare e README**: `python scripts\86_prepara_pubblicazione.py`, poi
`python scripts\prova_pagine_r6.py --cartella pubblica --senza-screenshot` → 0 errori. Nell'esito: peso di
`pubblica\`, file mancanti (AVVISI), e le prime 40 righe di `README.md`. **Non pubblicare niente.**
**3.5 Raccolta su leopi**: doppio clic su `scripts\CONTROLLA_LEOPI.bat`. Nell'esito l'uscita (OK / ALLARME / Pi non
raggiungibile). Poi scrivi (senza eseguirlo) il comando con cui Leo può farlo girare ogni mattina:
`schtasks /create /tn "GTT controlla leopi" /tr "C:\projects\Progetti\GTT\scripts\CONTROLLA_LEOPI.bat" /sc daily /st 08:00`.
**3.6 Catena unica**: doppio clic su `scripts\RISULTATO6_RIFAI.bat` (rifà 71→…→prova delle pagine): deve finire con
`FATTO`. Scrivi la durata. Da ora, dopo ogni fetch di domenica, basta questo `.bat`.

## FASE 4 — Esito e proposta per la memoria

**4.1** In `docs/ESITO_CORREZIONI_GENERALI.md`, una tabella **prima / dopo** (numeri del passo 0.4 contro quelli
nuovi): fermate importanti e classi, aree per categoria, i 20 punti (nome, zona, km dal centro), parcheggi in mappa,
peso della mappa. Sotto: quanti dei 20 punti nuovi stanno a meno di 2,5 km da Piazza Castello (erano 7) e in quali
zone; la decisione sui torinesi con i due numeri; la tabella di validazione; i file che hai cambiato tu (riga per
riga).
**4.2** In fondo all'esito, il testo **pronto da incollare** in `MEMORIA_PROGETTO.md` (sezione 4, riga del Risultato
6; sezione 3, «prossimo numero libero: 87»). **Non** modificare la memoria: la aggiorna Claude dopo aver ricontrollato.
**4.3** `git status` nell'esito. **Nessun commit.**

---

## Se qualcosa va storto

| Dove | Cosa vedi | Cosa fare |
|---|---|---|
| 81 | `Manca ... rete_auto.npz` o `punti.json`, oppure `instradamento non riuscito` | Lo script usa da solo il **ripiego** (auto che partono dalla zona). Scrivi l'errore esatto. Se è un nome di campo o un percorso evidente, correggilo e rilancia; se no tieni il ripiego e vai avanti: tutto il resto funziona lo stesso. |
| 81 | `MemoryError` | Chiudi gli altri programmi (opencode, Java/R5) e rilancia. |
| 81 | nessuna strada d'ingresso nota fra i 15 in cima | AVVISO forte nell'esito con l'elenco dei 15; vai avanti. |
| 82 | `aree trovate: 0` o errore di osmium sulle aree | Lancia `python scripts\82_parcheggi_adatti.py --senza-destinazioni` e scrivi nell'esito che il filtro delle destinazioni non è stato applicato. |
| 82 | `module 'shapely' has no attribute 'transform'` | Shapely vecchio: lo script ha già un ripiego; se l'errore resta, scrivilo (FERMO su 82, poi `--senza-destinazioni`). |
| 83 | `eleggibili > 1000` AVVISO | Scrivi il numero. Se è sotto 500 qualcosa non va con le zone: FERMO su 83 e salta alla FASE 3. |
| 84 | `KeyError` su un campo di `riempimento.json` o `nodi.json` | Probabilmente il nome di un campo diverso dal previsto: guarda il file vero (`python -c "import json;print(json.load(open(...))['parcheggi'][0].keys())"`), correggi il nome nell'84 e scrivilo. |
| 85 | `2. instradamento di 2 origini` diverso | Può succedere con due percorsi di uguale durata: scrivi la differenza; se è sotto l'1% del flusso massimo va bene. |
| 85 | `5. classe ... rifatta a mano` diversa | Errore vero: FERMO, scrivi i due valori. |
| 04 | `AVVISO: data fissa ... non valida` | Il GTFS è cambiato: scrivilo (Claude sceglierà date nuove). |
| prova_pagine | `non trovo Edge né Chrome` | Scrivilo; la prova la farà Claude. |

## Cosa NON fare

- Non cambiare regole, soglie, valori della sezione 1, testi pubblici, colori.
- Non usare le osservazioni di Leo nei dati o nei testi pubblici (solo il controllo a posteriori del passo 3.1).
- Non toccare `42_instradamento.py`, `rete_osm.py`, gli script del traffico 33-67, `data/raw`, il database, il Pi
  (sul Pi solo la lettura del passo 3.5).
- Non cancellare file; non pubblicare niente; nessun commit; non modificare `MEMORIA_PROGETTO.md`.

---

## Prompt da incollare nella nuova chat (per Leo)

> Sei un agente che lavora sul progetto GTT nella cartella `C:\projects\Progetti\GTT`, sul ramo git `prova`.
> Per prima cosa scarica da GitHub l'ultima versione: `git checkout prova`, `git status` (se ci sono modifiche
> locali in `scripts/`, `docs/`, `simulazione.html` o `MEMORIA_PROGETTO.md` fermati e dimmelo), poi
> `git fetch origin` e `git pull --ff-only origin prova`. Se il pull dà errori o conflitti, fermati e scrivimi il
> messaggio esatto, senza provare a risolverli. Solo se il pull è a posto e il file `docs/PIANO_CORREZIONI_GENERALI.md`
> c'è, prosegui:
> leggi `AGENTS.md`, poi esegui il piano `docs/PIANO_CORREZIONI_GENERALI.md` (passo 0.0 già fatto) dall'inizio alla fine,
> nell'ordine, un passo alla volta, **senza fermarti a chiedere** e seguendo le sue regole (sezione 0).
> Il codice è già scritto: il tuo compito è lanciare gli script sui dati veri, controllare i numeri come dice il
> piano, correggere solo errori piccoli ed evidenti (scrivendo ogni riga cambiata) e fare i passi della FASE 3.
> Scrivi tutto in `docs/ESITO_CORREZIONI_GENERALI.md`: per ogni passo una riga OK / AVVISI / FERMO e i numeri
> richiesti. Se uno script si ferma con un errore, guarda la tabella «Se qualcosa va storto» del piano; se il caso
> non c'è, scrivi cosa hai visto e continua con i passi che non dipendono da quello.
> Non fare commit, non pubblicare niente, non modificare `MEMORIA_PROGETTO.md`, non cambiare soglie, regole o testi.
> Python: quello del PATH (`python`), mai Anaconda. Alla fine scrivi un riassunto di 10 righe per Leo, in italiano
> semplice: cosa è andato bene, cosa no, i numeri principali prima/dopo.

Dopo: Claude ricontrolla l'esito e le pagine nel browser, aggiorna la memoria e, se Leo vuole, fa il commit.
