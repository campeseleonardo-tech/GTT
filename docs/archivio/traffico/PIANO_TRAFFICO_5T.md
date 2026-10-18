# Piano — Traffico veicolare dai sensori 5T (flusso, non solo velocità)

Scritto il 16/10/2026 (sera) da Claude con Leo. **Stato: PIANO, NIENTE DA COSTRUIRE FINO ALLE DECISIONI
APERTE (sezione 6).** Dal 16/10 sera è il **Risultato 8 — Traffico veicolare**, prossimo risultato prioritario. Sostituisce il vecchio punto "Velocità 5T in mappa" di `MEMORIA_PROGETTO.md`.
Il vecchio `docs/PIANO_VELOCITA_5T.md` resta come storia dello script 26 (già fatto).

## 1. Cosa vuole Leo (decisioni del 16/10)

- Lo slider dell'ora e il selettore "Adesso" vanno bene come sono.
- La baseline dei bus resta quella simulata/programmata (GTFS), come oggi. I 5T invece NON sono
  simulati: il "Tipico" è la media di quanto misurato da leopi (a regime sostituirà la baseline
  anche altrove, vedi "direzione futura" in MEMORIA).
- **Gli interessa il traffico veicolare (quanti veicoli passano), molto più della velocità.** Anche nelle
  viuzze dove non si va veloci: vuole sapere quanti passano.
- Mostrare tutti i dati dove ci sono; **dedurre il più possibile dove mancano i sensori**.
- I risultati sono **prima di tutto analisi**; la visualizzazione viene dopo o se serve (a volte gli serve
  per capire cosa si sta facendo).
- Resta valido: dati grezzi senza filtri (tutti i sensori), si decide dopo cosa scartare.
- **Deciso 16/10 sera:** questo diventa il prossimo risultato prioritario (numerato 8: scelta di Claude, modificabile), **senza
  abbandonare gli altri** (Risultato 6 v2 in novembre, 4, ecc. restano in coda).
- **Deciso 16/10 sera:** area intera (Torino + cintura ~18 km), senza restringerla per la RAM. Leo lascia il PC libero
  (nessun altro programma aperto) durante i calcoli pesanti. Claude propone comunque una prova su un'area piccola
  prima del giro intero (regola del progetto: prima il campione) e chiede un test di memoria, perché con 8 GB il
  crash dell'11/10 è già successo anche con la sola accessibilità.
- Direzione trasversale già annotata: "quanti veicoli in meno potrebbero circolare" come metrica
  (da progettare, vedi sezione 5).

## 2. Stato dei dati (verificato sui file veri; aggiornato dopo il fetch del 17/10 00:50)

| Cosa | Stato |
|---|---|
| Copia sul PC `data/storico_backup.sqlite` | **fetch del 17/10 00:50**: 1,6 GB, snapshot verificato. `flussi_5t` fino a **2026-10-16T22:36Z** (= 00:36 del 17/10), 365.477 righe; `accuratezza_5t` 243.179; `mezzi_gtt` 4.059.000; `trip_update_gtt` 1.893.353; **`parcheggi_5t` 41, `occupazione_pk` 27.921 (dal 14/10 13:10Z), `ztl_5t` 1** (ora copiati). Il sync è settimanale (domenica); prossimo fetch lunedì 19/10. |
| Letture con accuratezza | solo dall'8/10 21:30 UTC. Giorni interi utili: **6 feriali (9, 12, 13, 14, 15, 16/10), 1 sabato (10), 1 domenica (11)**. Controllo aritmetico: 193.925 usate + 49.254 scartate (13,5%) = 243.179 con accuratezza; + 122.298 senza riga = 365.477 flussi. Tornano. |
| `data/processed/velocita_5t.json` | rigenerato il 17/10: 109 sensori, 6.745 celle, **2.346 valide: feriale 2.252/2.266, sabato 94, domenica 0**. Contiene `f` = flusso tipico in veicoli/ora. **Le 94 celle "valide" del sabato sono un artefatto**: tutte ora 0, perché il sabato 17/10 conta come "giorno" con soli 36 minuti di dati (7 letture) e arriva a 2 giorni con il sabato 10. Correzione: Fase 1, passo 2 (v2: esclusione dei giorni parziali ai bordi; la soglia "6 letture" della v1 era sbagliata). |
| Anomalia ora locale 01:00 | nelle celle feriali dell'ora 1 (23:00-24:00 UTC) solo **31 sensori su 109 hanno letture affidabili** (28 valide) contro 95-97 delle ore vicine. Quindi solo **28 sensori (18 urbani) hanno tutte e 24 le ore valide** e quindi un totale giornaliero. Diagnosi Fase 1 passo 1 (17/10): non è un buco di raccolta (le righe ci sono) ma **accuratezza 0 su ~75% delle letture** in quell'ora, con salita graduale dalle 21 UTC e discesa fino alle 04 UTC. Possibile legame con il poco traffico notturno: da testare nel passo 2bis. |
| Sensori | 109 totali (63 "positive", 46 "negative"); 31 urbani (nome con "(TO)"), 78 fuori città (tangenziali, provinciali, statali). 12 senza nessuna cella valida, di cui **3 urbani** (2× Corso Regina Margherita, 1× Corso Moncalieri). |
| Flusso | già in veicoli/ora (multipli di 12). Picchi osservati: Corso Unità d'Italia ~3.265 veic/h; somma su 24 h fino a ~44.600 veic/giorno su un solo sensore. |
| Copertura rete | `importanza_vie.json`: 10.743 corridoi stradali (~6.800 km); **solo 10 corridoi (~141 km) hanno ≥1 sensore abbinato**; 15 sensori abbinati in tutto. Le vie piccole (punteggio 1-2, ~5.000 km) non hanno nessun sensore. |
| Weekend | sabato 17 e domenica 18/10 saranno interi dal **19/10**: fetch lunedì (stesso doppio clic) e si avranno 2 sabati e 2 domeniche. |

Da verificare (Claude, sulla documentazione 5T): se il flusso di un sensore è per tutta la carreggiata
(tutte le corsie di quella direzione) o per una sola corsia. Cambia il significato dei numeri. **Finché non è chiarito, i sensori non si sommano tra loro** (due sensori sulla stessa via e nella stessa direzione, es. Corso Francia 40021 e 40022, sono punti diversi, non corsie: sommarli conterebbe due volte gli stessi veicoli).

Nota: il "Tipico" oggi in mappa viene da `stat.js` (calcolato sul Pi, **non scarta** le letture con
accuratezza 0); `velocita_5t.json` le scarta. Passando al nuovo file il "Tipico" cambia: va detto.

## 3. Cosa può dare l'IMQ 2022 (discussione del 16/10)

L'IMQ finora è usato poco (Risultato 6 per i pendolari, tema "Mobilità IMQ" in mappa). Ha però quello che
serve per **scalare** i dati misurati, perché è l'unica fonte di *domanda* sul traffico privato:
- 95.608 spostamenti intervistati, pesati a 8.217.863 spostamenti/giorno feriale medio (torna col report).
- Per ogni spostamento: zona di partenza e arrivo (212 zone: 23 quartieri di Torino + comuni), **ora di
  partenza e arrivo al minuto**, scopo, mezzi usati, **numero di passeggeri in auto** (`PAX_AUTO`) e se si
  guida (mezzo 03 = conducente). Quindi si possono contare i **veicoli** (conducenti), non le persone.
- Controllo fatto il 16/10 sul file `spostamenti.csv`: spostamenti con auto come conducente ≈ **4,18
  milioni/giorno (50,9%)**, di cui ≈ 0,97 milioni con almeno un estremo in un quartiere di Torino;
  partenze con picchi 7-8 (≈19%) e 16-18 (≈26%). [STIMATO, da campione]
- Usi possibili: (a) **totali di controllo**: confrontare i veicoli stimati dall'IMQ con quelli misurati
  dai 5T ai punti d'ingresso; (b) **forma oraria**: confrontare il profilo orario IMQ con quello 5T;
  (c) **domanda per la stima C** (sezione 4); (d) **base del "quanti veicoli in meno"** (sezione 5).

Limiti dell'IMQ (da dichiarare sempre, vedi `docs/RAPPORTO_IMQ.txt`):
1. Indagine telefonica a campione: a livello di singola coppia di zone le celle sono quasi sempre sotto 30
   interviste (privato: solo il 4,7% delle celle ≥30). Si legge per aggregati (zona, macroarea, ora).
2. Solo residenti 11-84 anni, giorno feriale medio: **mancano turisti, pendolari esterni, merci, taxi
   commerciali, furgoni**. I 5T misurano tutto → la differenza IMQ-5T non è un errore puro, in parte è
   proprio il traffico che l'IMQ non vede (logistica!). Non va letta come "errore del modello".
3. Quartieri di Torino con confini del 1984: 7 su 23 non coincidono con le zone di campionamento.
4. Anno 2022 (post-pandemia); zone di Torino grandi (23) per la rete stradale di una città.

## 4. Metodi per le strade senza sensore

- **A. Per tipo di strada**: a ogni via la media dei sensori della stessa classe (punteggio 1-5 di
  `importanza_vie.json`). Semplice, molto grezzo; poche vie urbane con sensori.
- **B. Lungo la stessa via**: estendere il flusso dal sensore più vicino sullo stesso corridoio. Affidabile
  dove funziona, copre ~141 km su ~6.800.
- **C. Assegnazione dalla domanda IMQ**: veicoli IMQ tra le 212 zone per ora → fatti passare sulla rete
  stradale (percorso più breve) → calibrati sui sensori. È il metodo "vero", ma pesante: serve una rete
  stradale per auto (r5py supporta le auto, da verificare sulla tua area), il PC ha 8 GB di RAM (già un
  crash), molte ipotesi (zone grandi, nessuna merce, nessun non residente).
- **Segnali indiretti** possibili: velocità reale dei bus (rallenta col traffico, solo sulle vie dei
  bus), occupazione parcheggi, ZTL. Sono indizi, non flussi.

**Proposta di Claude (da confermare):** A+B subito (poco costo), poi **collaudo "un sensore alla volta
nascosto"**: si nasconde un sensore, si stima il suo flusso con gli altri, si confronta col valore vero.
Si passa a C solo se il collaudo va male. Con ~28 sensori urbani validi il collaudo è comunque debole:
va dichiarato. Tutto ciò che è dedotto porta il tag [STIMATO], mai [MISURATO].

## 5. Collegamento con "quanti veicoli in meno" (non progettato)

Idea di base: dove l'accessibilità in trasporto pubblico migliora (es. Risultato 2, linea nuova, più
frequenza), una parte degli spostamenti IMQ in auto (conducente) tra quelle zone potrebbe passare al
mezzo pubblico. Servono: quota di spostamenti auto per coppia di zone (IMQ), differenza di tempo auto
contro trasporto pubblico (R5), un'ipotesi di sostituzione. Serve una discussione a parte prima di
costruire; qui si annota solo che l'IMQ è il punto di partenza.

## 6. Decisioni (16/10 sera: Leo ha risposto a tutte)

1. "Trafficata" = veicoli/ora per ogni ora tipica + totale giornaliero a due direzioni: **sì**.
2. Cosa serve prima: **traffico stimato su tutta la rete**; poi, incrociandolo con l'offerta di trasporto
   pubblico, **le vie con molto traffico e poco trasporto pubblico**. ("Veicoli in meno" dopo, dalla
   direzione trasversale della sezione 5.) Per l'incrocio serve una misura dell'offerta TP per via
   (es. corse/ora dei bus sulle vie, già disponibile dal GTFS): da definire quando si arriva lì.
3. Metodo: **A+B + collaudo, poi C**; si fa tutto (area intera, vedi sezione 1): **sì**.
4. Velocità reale dei bus come indizio di traffico: **no** (Leo: "ci possono essere molti bus e poco
   traffico", cioè i due segnali non vanno confusi).
5. Sensori fuori città: **sì**, usati come ingressi/uscite (restano anche nei dati grezzi).
6. Weekend: si parte coi feriali (dati scarsi dichiarati) e il weekend si aggiunge dopo il fetch del 19/10.
   **I dati freschi vanno presi da leopi** (vedi sezione 7, passo 2).
7. Mappa: **dopo** l'analisi.
8. Ruolo dell'IMQ come base della stima del traffico e dei "veicoli in meno": **sì**.
9. Area del metodo C: **intera**.

10. **Da decidere dopo il Passo 2bis:** regola per le letture con accuratezza 0 di notte (oggi scartate: se significano
    "pochi veicoli" il flusso notturno è sovrastimato) e come trattare l'ora 01:00 nel totale giornaliero (proposta:
    non interpolare nei dati misurati; eventuale imputazione solo come [STIMATO] separato).

Superate dalla nuova priorità: scala colori della velocità, velocità libera, scala comune con i bus.

## 7. Passi (in ordine)

*(I passi 2 e 3 sono in gran parte eseguiti dalla Fase 1 meccanica della sezione 9, affidabile a un altro agente.)*

1. Claude verifica sulla documentazione 5T cosa misura un sensore (corsie, direzione).
2. **Dati freschi da leopi** (fetch fatto la notte del 16->17/10, poi di nuovo lunedì 19/10 per sabato e
   domenica completi). Claude (questa chat, nel cloud) NON può collegarsi a leopi: `192.168.8.200` è un
   indirizzo della rete di casa e da qui non si raggiunge; la chiave SSH sta sul PC di Leo (`~/.ssh/id_gtt_leopi`).
   Come si fa: **doppio clic su `scripts\FETCH_LEOPI_E_VELOCITA_5T.bat`** (PC sulla stessa rete di leopi, PC libero,
   alcuni minuti). Fa: copia dello storico (snapshot SQLite verificato, sola lettura sul Pi) → copia dei
   risultati 5T precedenti (`*_prima_fetch.*`) → rilancio dello script 26. Se non parte, l'agente opencode (che
   ha l'SSH in sola lettura) può eseguire `python scripts\backup_da_leopi.py` e `python scripts\26_velocita_5t.py`.
   Controlli dopo il fetch (li fa Claude leggendo i log e i file): ultimo `flussi_5t` ≥ fine giornata attesa;
   `accuratezza_5t` parte da 2026-10-08T21:30; feriali, sabato, domenica contati giusti nel rapporto; tabelle
   parcheggi/ZTL presenti nel log del backup.
   **Correzione trovata il 17/10:** `backup_da_leopi.py` copiava solo 7 tabelle e NON `parcheggi_5t`,
   `occupazione_pk`, `ztl_5t` (raccolte su leopi dal 14/10): senza di esse il Risultato 6 v2 di novembre non avrebbe
   avuto dati sul PC. Aggiunte le 3 tabelle (e l'intervallo di `occupazione_pk` nel log); provato su un DB finto.
   Spazio disco: serve circa il doppio della dimensione dello storico (~1 GB oggi) liberi durante la copia.
3. Nuovo script (numero libero: **33**; 30-32 sono del rapporto di sostenibilità — controllare MEMORIA sezione 3) che legge `velocita_5t.json` e produce flusso per sensore, ora, giorno;
   scheda con 3 numeri e limiti.
4. Metodi A+B sulla rete di `importanza_vie.json`; collaudo con un sensore alla volta; rapporto in `docs/`.
5. Metodo C: IMQ (conducenti, ora al minuto) → rete stradale → calibrazione sui sensori. Prima prova su
   un'area piccola con misura della RAM; poi area intera, PC libero.
6. Incrocio con l'offerta TP: vie con molto traffico e poco trasporto pubblico.
7. Solo dopo: mappa / `simulazione.html` (scheda risultato generica).

## 8. Regole che restano

- Ramo `prova`, niente commit di Claude (decide Leo). Dati grezzi e storico in sola lettura.
- Prima su una copia o un campione, poi il giro vero. Calcoli lunghi in una finestra `.bat` propria.
- Tag: [MISURATO] sensori; [STIMATO] ogni valore dedotto; [DATI SCARSI] finché ci sono pochi giorni.
- Un solo file di memoria (`MEMORIA_PROGETTO.md`) con il riassunto; i dettagli stanno qui.

## 9. Fase 1 — piano meccanico per un altro agente (scritto il 17/10)

Obiettivo: preparare tutto ciò che serve per il collaudo e per i metodi A+B senza prendere decisioni di
progetto. L'agente esegue i passi **nell'ordine**, ne verifica il risultato, scrive l'esito in
`docs/ESITO_FASE1_TRAFFICO_5T.md` e **si ferma** a ogni controllo che non torna (non corregge a caso).

### Regole per l'agente (valgono per tutti i passi)
- Ramo git `prova` (altrimenti fermarsi). **Nessun commit.** Non toccare: `data/raw/`, `data/storico_backup.sqlite`
  (solo sola lettura: `sqlite3.connect("file:...?mode=ro", uri=True)`), `mappa_torino.html`,
  `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/18_*`, `scripts/24_*`, `MEMORIA_PROGETTO.md`.
- Niente R5/Java. Solo libreria standard di Python (comando `python`, quello del PATH; NON Anaconda).
- Il PC deve essere libero (nessun altro programma pesante). Tutti i passi sono leggeri, tranne la lettura del
  database (1,6 GB, sola lettura).
- Ore locali: Europe/Rome = UTC+2 fino al 24/10/2026 incluso (poi UTC+1). I dati dei passi coprono 8-17/10.
- Tipo di giorno: 0 feriale (lun-ven), 1 sabato, 2 domenica. Numero libero per i nuovi script: **33** e **34**
  (controllare prima `scripts/`: se 33 o 34 esistono già, usare i primi due liberi e scriverlo nell'esito).
- Ogni passo termina con una riga nell'esito: `PASSO n: OK` oppure `PASSO n: FERMO – motivo`.

### Passo 0 – Pre-controlli
1. `git branch --show-current` deve dire `prova`. Annotare `git status --short` (non toccare nulla).
2. Esistono: `data/storico_backup.sqlite` (≈1,6 GB), `data/processed/velocita_5t.json`,
   `data/processed/velocita_5t_prima_fetch.json`, `data/processed/importanza_vie.json`, `scripts/26_velocita_5t.py`.
3. Annotare data e ora di inizio.

### Passo 1 – Controllo del database e diagnosi dell'ora 01:00 (sola lettura)
Scrivere `scripts/controllo_fase1_5t.py` (resta nella cartella come strumento) che stampa e salva in
`docs/ESITO_FASE1_TRAFFICO_5T.md`:
- a) Conteggi: `flussi_5t` **365477**, `accuratezza_5t` **243179**, `parcheggi_5t` **41**, `occupazione_pk` **27921**
  (può essere più alto solo se il file è stato riscaricato), `ztl_5t` **1**, `trip_update_gtt` **1893353**,
  `mezzi_gtt` **4059000**. Ultimo `generato_utc` di `flussi_5t`: **2026-10-16T22:36:17.111Z**.
- b) Righe di `flussi_5t` senza riga in `accuratezza_5t` (join su `generato_utc` e `lcd1`): **122298**; con
  `accuratezza = 0`: **49254**; con `accuratezza > 0` e `flusso` non nullo: **193925**.
- c) **Diagnosi ora 1**: per ogni ora UTC (0-23) sul periodo 2026-10-09 → 2026-10-16: (i) numero di righe di
  `flussi_5t`, (ii) quota di righe con `accuratezza = 0`, (iii) numero di sensori distinti con almeno una riga con
  `accuratezza > 0`. Scrivere la tabella. In particolare confrontare le ore UTC 21, 22, **23**, 00, 01.
  Non interpretare: riportare solo i numeri e dire in una frase se l'ora UTC 23 (= 01:00 locale) si distingue.
- Se un conteggio a) o b) non coincide: FERMARSI.

### Passo 2 – Correzione dello script 26 (v2, 17/10 01:30): esclusione dei giorni parziali ai bordi
Storia: la prima versione del passo (soglia "almeno 6 letture per giorno e cella") era sbagliata: i 36 minuti del
sabato 17/10 danno 7 letture (≥6) e il giorno contava lo stesso; e la soglia faceva perdere 127 celle feriali
buone. L'agente si è fermato correttamente. **Nuova regola:** non si guarda il numero di letture di una cella, ma si
**escludono il primo e l'ultimo giorno locale dei dati se non coprono tutta la giornata** (primo giorno: prima
lettura dopo le 00:30; ultimo giorno: ultima lettura prima delle 23:30). Qui: l'8/10 (dati dalle 23:30) e il 17/10
(dati fino alle 00:36).
Cosa fare, in ordine:
1. **Ripartire dalla copia di sicurezza:** copiare `scripts/26_velocita_5t.py.bak_17ott` sopra
   `scripts/26_velocita_5t.py` (annullando le 5 modifiche del passo 2 v1). Se la copia non esiste: fermarsi.
2. In `main()`, **subito prima** del commento `# --- accumulo per (sensore, tipo, ora) ---` (cioè dopo il blocco
   `if args.prova:`), inserire:
```
    # --- giorni parziali ai bordi del periodo: si escludono (regola 17/10) ---
    # Il primo e l'ultimo giorno locale dei dati contano solo se coprono tutta la
    # giornata (primo giorno: prima lettura entro le 00:30; ultimo: ultima dopo le 23:30).
    copertura = {}      # giorno locale -> (minuti della prima lettura, minuti dell'ultima)
    for g, *_ in letture:
        loc = a_roma(parsa_utc(g))
        m = loc.hour * 60 + loc.minute
        lo, hi = copertura.get(loc.date(), (m, m))
        copertura[loc.date()] = (min(lo, m), max(hi, m))
    giorni_esclusi = set()
    if copertura:
        primo_g, ultimo_g = min(copertura), max(copertura)
        if copertura[primo_g][0] > 30:
            giorni_esclusi.add(primo_g)
        if copertura[ultimo_g][1] < 23 * 60 + 30:
            giorni_esclusi.add(ultimo_g)
        letture = [r for r in letture
                   if a_roma(parsa_utc(r[0])).date() not in giorni_esclusi]
```
3. Nel rapporto, subito dopo la riga `scrivi(f"periodo (giorni locali): {primo} -> {ultimo}")`, aggiungere:
   `if giorni_esclusi: scrivi("giorni parziali esclusi (bordo del periodo): " + ", ".join(str(d) for d in sorted(giorni_esclusi)))`
4. Nei `parametri` del JSON **non** aggiungere altro. Nessuna altra modifica (il resto resta com'era).
5. `python scripts\26_velocita_5t.py --prova`, poi `python scripts\26_velocita_5t.py`.
Controlli attesi (devono coincidere, altrimenti FERMARSI):
- `giorni parziali esclusi`: **2026-10-08 e 2026-10-17**; periodo **2026-10-09 → 2026-10-16**;
  giorni per tipo: **feriale 6, sabato 1, domenica 1**.
- celle ok: **sabato 0, domenica 0, feriale tra 2245 e 2260** (prima di qualsiasi correzione erano 2252).
- letture affidabili usate = **193925 − (letture affidabili dei giorni locali 8/10 e 17/10)**: calcolare questi due
  numeri con una query SQL (sola lettura, UTC+2) e verificare l'uguaglianza esatta; scrivere i due numeri nell'esito.

### Passo 2bis – Test: "accuratezza = 0" significa sensore rotto o poco traffico? (solo SQL, sola lettura)
Motivo (17/10): la quota di letture con accuratezza 0 non è costante: 12-13% di giorno, ma sale a 13,6% (ore UTC 21),
53,4% (22), **74,9% (23)**, 45,2% (00), 38,6% (01), 30,5% (02), 16,6% (03) e torna al 12% dalle 04. Il 12% di giorno
corrisponde ai ~12 sensori sempre senza dati; l'aumento serale/notturno potrebbe invece voler dire "pochi veicoli
contati". Se così fosse, scartare le letture con accuratezza 0 gonfia i flussi notturni (restano solo i momenti più
carichi e le strade più trafficate). **Ipotesi da verificare, non da dare per vera.**
Per ogni ora locale 0-23 (giorni locali 2026-10-09 → 2026-10-16, UTC+2), solo sui sensori che hanno almeno una lettura
con accuratezza > 0 nel periodo (i "vivi"; contare anche i sensori "morti" = sempre accuratezza 0, attesi **12**):
(i) letture totali; (ii) quota con accuratezza 0; (iii) tra le letture con accuratezza 0, quota con flusso = 0;
(iv) tra le letture con accuratezza > 0, quota con flusso = 0; (v) flusso medio delle letture con accuratezza > 0.
Scrivere la tabella nell'esito e **una sola frase** di sintesi senza interpretare (es. "alle ore 1 locali il 9x% delle
letture con accuratezza 0 ha flusso 0, contro il y% di quelle con accuratezza > 0"). Non cambiare nessuno script.

### Passo 3 – Ricalcolo indipendente di 6 celle (dal database, non dallo script 26)
Per ciascuna coppia (sensore, ora locale): lcd1 **40040** ore 8 e 3; lcd1 **40095** ore 8 e 13; lcd1 **40174** ore 8 e 18.
Leggere da `flussi_5t` + `accuratezza_5t` (join su `generato_utc` e `lcd1`) le righe con `accuratezza > 0` e `flusso`
non nullo, convertire l'orario in locale (UTC+2), tenere solo giorni lun-ven tra 2026-10-08 e 2026-10-16 e
l'ora locale indicata. Calcolare: `n` = numero di righe; `f` = media del flusso (zeri compresi, arrotondata
all'intero); `v` = Σ(velocità×flusso)/Σflusso solo sulle righe con flusso > 0 (arrotondata a 0,1). Confrontare con
`velocita_5t.json` (`sensori[lcd1].celle["0"][ora]`: campi `n`, `f`, `v`). Tolleranza: `n` uguale, `f` ±1, `v` ±0,1.
Se anche una sola cella non coincide: FERMARSI e riportare i due valori.

### Passo 4 – Script 33: flusso per sensore, ora e giorno
Nuovo `scripts/33_flusso_sensori.py` (stile degli altri script: docstring in italiano, solo libreria standard).
Legge `data/processed/velocita_5t.json` e scrive `data/processed/flusso_5t_sensori.json` e
`docs/RAPPORTO_FLUSSO_5T_SENSORI.txt`. Per **ogni** sensore (anche senza dati) e per ogni tipo di giorno con almeno
una cella ok:
`{"lcd1","via","dir","lat","lon","urbano","tipo":{"0":{"f_ora":[24 valori o null],"n_ore_ok":..,"totale_giorno":..,"f_punta":..,"ora_punta":..}}}`
- `f_ora[h]` = campo `f` della cella **solo se `ok` è vero**, altrimenti `null`.
- `totale_giorno` = somma dei 24 `f_ora` **solo se `n_ore_ok` = 24**, altrimenti `null` (non interpolare!);
  `totale_parziale` = somma delle ore ok (sempre scritto).
- `f_punta`/`ora_punta` = massimo tra le ore ok.
- I sensori **non si sommano tra loro**.
Nel rapporto: (1) quanti sensori hanno `totale_giorno` (attesi circa **28**, di cui urbani circa **18**) e quanti hanno 23
ore ok; (2) i 15 sensori urbani con più veicoli/giorno (via, direzione, totale, ora di punta); (3) il profilo
orario completo dei primi 3; (4) sensori senza nessuna cella ok (attesi circa 12, di cui circa 3 urbani); (5) controllo: nessun
`f_ora` negativo, nessun `f_ora` > 6000 (se c'è, elencare), massimo atteso ≈ 3202.
Prima `--prova` su 5 sensori (stampa a console senza scrivere), poi giro completo.

### Passo 5 – Script 34: quale sensore cade su quale corridoio (solo tabella, senza decidere)
Nuovo `scripts/34_sensori_corridoi.py`. Importare da `scripts/24_importanza_vie.py` (con `importlib`, il nome inizia
con un numero) le funzioni `normalizza` e `haversine_m`. Per ogni sensore di `flusso_5t_sensori.json` con almeno una
cella ok, cercare in `data/processed/importanza_vie.json` (chiave `corridoi`) i corridoi con
`chiave_normalizzata == normalizza(via)` e calcolare la distanza minima del sensore dai punti della geometria
(`geometria` = lista di tratti, ogni tratto lista di `[lat, lon]`). Regola identica allo script 24: abbinato se la
distanza minima ≤ 60 m. Scrivere `data/processed/sensori_corridoi.json` e `docs/RAPPORTO_SENSORI_CORRIDOI.txt`
con: per ogni sensore il corridoio abbinato (nome, punteggio, km) oppure `nessuno` + il corridoio omonimo più
vicino con la sua distanza (anche oltre 60 m) per capire perché manca; conteggi: sensori abbinati / non abbinati,
separati urbani e non; distribuzione dei sensori abbinati per punteggio 1-5. **Non** assegnare né stimare niente.
Controllo atteso: sensori abbinati **vicini a 15** (script 24 ne abbinava 15; scarti spiegati nel rapporto).

### Passo 6 – Chiusura
Scrivere in `docs/ESITO_FASE1_TRAFFICO_5T.md`: esito di ogni passo, file creati/modificati, numeri chiave (celle ok
per tipo, sensori con totale giornaliero, abbinati ai corridoi), la risposta alla diagnosi dell'ora 1, eventuali
anomalie, tabella del Passo 2bis. **Non** aggiornare `MEMORIA_PROGETTO.md` (lo fa Claude/Leo). Dire a Leo in parole semplici cosa è stato
fatto e, in caso di FERMO, cosa serve.

### Non fare (Fase 2, decisioni da prendere insieme a Leo)
Metodi A, B e C; collaudo del sensore nascosto; qualsiasi stima fuori dai sensori; mappa/`simulazione.html`;
somma tra sensori; interpolazione di ore mancanti; commit.

### Prompt da dare all'agente
```
Sei un agente con accesso al terminale sul PC di Leo. Lavori nella cartella C:\projects\Progetti\GTT.
Leo non è un programmatore: spiegagli tutto in italiano, con parole semplici, senza gergo.

1) Leggi per intero, nell'ordine: AGENTS.md, MEMORIA_PROGETTO.md, docs/PIANO_TRAFFICO_5T.md.
2) Poi esegui la sezione "9. Fase 1 — piano meccanico per un altro agente" del piano, passo per passo,
   nell'ordine, senza saltare nulla e senza aggiungere iniziative.
3) Regole non negoziabili: ramo git `prova` (se non sei lì, fermati e dillo); nessun commit; il database
   data/storico_backup.sqlite si apre solo in sola lettura; non toccare i file elencati nella sezione "Regole per
   l'agente"; solo libreria standard di Python; PC libero (nessun altro programma pesante).
4) Dopo ogni passo scrivi in docs/ESITO_FASE1_TRAFFICO_5T.md "PASSO n: OK" oppure "PASSO n: FERMO – motivo".
   Se un controllo non torna FERMATI subito, scrivi i due valori a confronto e aspetta Leo: non correggere,
   non inventare, non andare avanti.
5) Quando hai finito, rispondi a Leo con: cosa è stato fatto (5 righe al massimo), i numeri chiave, le anomalie,
   e i file creati o modificati. Niente altro.
```
