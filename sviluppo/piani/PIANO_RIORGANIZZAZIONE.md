# Piano 1 — Riorganizzazione del repository e pubblicazione

Obiettivo: chi apre GitHub o il sito capisce in 2 minuti cosa è il progetto, chi l'ha fatto e da dove partire.
Gli appunti di lavoro restano in git, ma fuori dalla vista.

Decisioni di Leo (22/10):
- ramo **`main`** = versione pubblicata e ramo di default; `prova` resta per lavorare;
- appunti di lavoro in **`sviluppo/`**;
- repository rinominato da Leo in **`Turin-mobility`** (22/10); titolo del sito «Torino Mobilità» (in inglese «Turin Mobility»); indirizzo `campeseleonardo-tech.github.io/Turin-mobility/`;
- **«Chi sono»**: Leonardo Campese, LinkedIn https://www.linkedin.com/in/leocampese/, email campese.leonardo@gmail.com;
- sfondi Esri consentiti (progetto non commerciale; se diventa commerciale si cambiano);
- licenza del codice **MIT** (`LICENSE` fatto il 22/10; i dati restano con la licenza della fonte).

Dove si lavora: [CLOUD] sessione cloud · [PC] PC di Leo · [GITHUB] impostazioni sul sito di GitHub, a mano (Leo).

## Come sarà alla fine

```
README.md            presentazione IT + EN: cosa è, link al sito, 5 risultati con un'immagine, fonti, come rifare
LICENSE              MIT per il codice; i dati con la licenza della fonte
index.html           ingresso del sito
risultati.html       le schede
progetto.html        perché questo progetto: la storia (piano 4, G)
mappa_torino.html    la mappa (resta in git: è la pagina che il sito pubblica)
404.html             pagina «non trovata» con i link alle altre
assets/              stile comune, font, icona, immagini di anteprima, script delle animazioni
data/                solo i file che servono a pagine e calcoli (piano 2)
docs/                METODO, FONTI_DATI, DATI, un documento per risultato, rapporti/
scripts/             script numerati, comuni.py, .bat; scripts/prove/
sviluppo/            AGENTS completo, MEMORIA_PROGETTO, piani/, TESI_E_PROGETTO
AGENTS.md            corto: rimanda a sviluppo/AGENTS.md
```

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | **FATTO (22/10)**: memoria allineata, `ESITO_*.md` e piani vecchi cancellati, rami controllati (nessun lavoro perso) | CLOUD | — |
| 2 | **`main`**: creato da `prova` e repository rinominato `Turin-mobility` (**FATTO**, Leo 22/10). `main` è ramo di default e il PC punta al nuovo indirizzo (**FATTO**, Leo 22/10). In `main` si entra solo con un blocco finito e provato | GITHUB (Leo) | piccolo |
| 3 | **Rami vecchi** cancellati da Leo il 22/10 (**FATTO**); `vibrant-planck-cztsh9` e `sharp-maxwell-mpqd8z` dopo l'unione in `prova` | GITHUB (Leo) | piccolo |
| 4 | **FATTO (C1)**: `sviluppo/`: spostare `MEMORIA_PROGETTO.md`, `docs/piani/`, `docs/TESI_E_PROGETTO.md`; `AGENTS.md` in radice ridotto a poche righe (`docs/ANALISI_STATO.md` già cancellato il 22/10); aggiornare i percorsi citati (`git grep`) | CLOUD | piccolo |
| 5 | **FATTO (C1, file locale da creare sul PC: giro P1)**: dati di accesso fuori dai testi pubblici: IP del Pi, utente SSH, percorso della chiave → file locale `config_locale.json` (in `.gitignore`) letto da script e `.bat` | CLOUD (codice) + PC (file) | piccolo |
| 6 | **FATTO (C1)**: testi puliti: niente «Leo», «giro», «fase», date di sviluppo nelle pagine e nei commenti (`simulazione.html` già cancellata il 22/10) | CLOUD | medio |
| 7 | **FATTO (C1)**: script 86: oggi **riscrive `README.md`** a ogni `RIFAI_MAPPA_E_SCHEDE.bat` (cancellerebbe il README nuovo). Diventa solo un controllo «ogni file caricato dalle pagine esiste ed è in git»; niente più cartella `pubblica/` | CLOUD | piccolo |
| 8 | **GitHub Pages da `main`** (cartella radice), con i dati delle pagine in git (piano 2) | GITHUB (Leo) | piccolo |
| 9 | **FATTO (C12)**: **README nuovo** (alla fine, dopo piani 2-4): cosa è, link al sito, 5 risultati con una riga e un'immagine, fonti e licenze, come rifare i calcoli in 3 comandi, «Chi sono» | CLOUD | piccolo |
| 10 | **Descrizione del repository**: una riga, link al sito, argomenti (`torino`, `public-transport`, `open-data`, `gtfs`, `raspberry-pi`, `data-visualization`), immagine di anteprima del repository | GITHUB (Leo) | piccolo |

Favicon, anteprima dei link e «Chi sono» nelle pagine stanno nel piano 4 (H), perché dipendono dallo stile scelto.
I commit «descrizione di cosa hai fatto» restano nella storia; da qui messaggi chiari anche dal PC.

## Controllo dei rami (regola fissa)
Prima di ogni lavoro: `scripts\CONTROLLA_RAMI.bat` sul PC, o lo stesso controllo nel cloud (`git fetch --prune` e, per ogni
ramo, commit non presenti in `prova`). Se un ramo ha commit non uniti, si dice a Leo prima di iniziare.
Attenzione nel cloud: la copia di partenza può avere la storia tagliata; prima del confronto `git fetch --unshallow`
(il 22/10 senza questo passo sembravano mancare 200 commit, che invece c'erano).
