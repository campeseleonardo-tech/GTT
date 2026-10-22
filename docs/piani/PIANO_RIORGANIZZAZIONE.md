# Piano 1 — Riorganizzazione del repository e pubblicazione

Obiettivo: chi apre GitHub o il sito capisce in 2 minuti cosa è il progetto, chi l'ha fatto e da dove partire.
Gli appunti di lavoro restano in git, ma fuori dalla vista. Sostituisce `PIANO_DOCUMENTI.md` (passi 11 e 13 ripresi qui).

Decisioni di Leo (22/10): ramo **`main`** = versione pubblicata, ramo di default; `prova` resta per lavorare.
Appunti di lavoro in **`sviluppo/`**. Sfondi Esri: uso consentito (progetto non commerciale; se diventa commerciale si
cambiano). Licenza del codice: **MIT** (file `LICENSE` fatto il 22/10; i dati restano con la licenza della fonte).

Dove si lavora: [CLOUD] = sessione cloud, [PC] = sul PC di Leo, [GITHUB] = impostazioni sul sito di GitHub (a mano, Leo).

## Come sarà alla fine

```
README.md            presentazione IT + EN: cosa è, link al sito, 5 risultati con un'immagine, fonti, come rifare
LICENSE              MIT per il codice; i dati con la licenza della fonte
index.html           ingresso del sito
risultati.html       le schede
racconto.html        la storia (piano 4)
mappa_torino.html    la mappa (resta in git: è la pagina che il sito pubblica)
assets/              stile comune, font, icona, immagine di anteprima, piccoli script delle animazioni
data/                solo i file che servono a pagine e calcoli (piano 2)
docs/                METODO, FONTI_DATI, un documento per risultato, rapporti/
scripts/             script numerati, comuni.py, .bat; scripts/prove/
sviluppo/            AGENTS completo, MEMORIA_PROGETTO, piani/, ANALISI_STATO, TESI_E_PROGETTO
AGENTS.md            corto: «le regole stanno in sviluppo/AGENTS.md»
```

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **Allineare la memoria** allo stato vero (giro 4, R6 minuti di pareggio, R4 giro 6, script 95 sono FATTI sul PC) e cancellare i 5 `docs/piani/ESITO_*.md` e i piani assorbiti (`PIANO_DOCUMENTI`, `PIANO_SCHEDE`, `PIANO_MAPPA`) dopo che Leo ha confermato | CLOUD | piccolo |
| 2 | **Creare `main`** da `prova` e renderlo ramo di default; regola: in `main` si entra solo quando un blocco è finito e provato | GITHUB (Leo) + CLOUD | piccolo |
| 3 | **`sviluppo/`**: spostare `MEMORIA_PROGETTO.md`, `docs/piani/`, `docs/ANALISI_STATO.md`, `docs/TESI_E_PROGETTO.md`; `AGENTS.md` in radice ridotto a 5 righe che rimandano a `sviluppo/AGENTS.md`; aggiornare i percorsi citati negli script (`git grep`) | CLOUD | piccolo |
| 4 | **Dati sensibili fuori dai testi pubblici**: IP del Pi, nome utente SSH, percorso della chiave → in un file locale non salvato (`.env` o `config_locale.json`, in `.gitignore`), letto dagli script e dai `.bat` | CLOUD (codice) + PC (file locale) | piccolo |
| 5 | **Testi delle pagine e del codice puliti**: niente «Leo», «giro», «fase», date di sviluppo nelle pagine; commenti nel codice senza date (passo 10 del vecchio piano) | CLOUD | medio |
| 6 | **Pagine pronte per la condivisione**: favicon, `<meta name="description">`, Open Graph (titolo, descrizione, immagine 1200×630) su index, risultati, mappa, racconto | CLOUD | piccolo |
| 7 | **Sezione «Chi sono»** in home e nel README: nome, una riga, link a GitHub/LinkedIn, la storia del Raspberry Pi e della tesi (da `TESI_E_PROGETTO.md`) | CLOUD (testi da Leo) | piccolo |
| 8 | **GitHub Pages da `main`** (cartella radice): con i dati delle pagine in git (piano 2) non serve più il ramo `gh-pages` né la cartella `pubblica/`; lo script 86 diventa un controllo «tutti i file caricati dalle pagine esistono» | GITHUB (Leo) + CLOUD | piccolo |
| 9 | **README nuovo** (alla fine, dopo piani 2-4): cosa è, link al sito, 5 risultati con una riga e un'immagine, fonti e licenze, come rifare i calcoli in 3 comandi | CLOUD | piccolo |
| 10 | **Descrizione del repository su GitHub**: una riga, sito, argomenti (`torino`, `public-transport`, `open-data`, `gtfs`, `raspberry-pi`, `data-visualization`) | GITHUB (Leo) | piccolo |

I commit con messaggio «descrizione di cosa hai fatto» restano nella storia (riscriverla romperebbe i rami): da qui in
avanti messaggi chiari anche dal PC.

## Domande aperte per Leo
- Cosa mettere in «Chi sono»: solo nome e LinkedIn, o anche email?
- Indirizzo del sito: va bene `campeseleonardo-tech.github.io/gtt/` o vuoi un nome di repository diverso (es. `torino-mobilita`)?
