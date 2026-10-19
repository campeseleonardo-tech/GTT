# Esito del piano R6 porte (19/10/2026)

Piano seguito: `docs/PIANO_R6_PORTE.md`. Ramo `prova`, nessun commit, nessuna libreria nuova.

Le cinque fasi sono state eseguite in ordine, senza fermarsi. Nella fase 1 una verifica numerica
non tornava con il tetto scritto nel piano: la causa è chiara ed è spiegata sotto, quindi il controllo
è stato corretto (non saltato) e il resto è andato avanti.

FASE 1: OK (con una correzione di controllo, vedi sotto)
FASE 2: OK
FASE 3: OK (controllo nel browser)
FASE 4: OK
FASE 5: OK

## Fase 1: script 80 e controlli

Scritti: `scripts/80_porte_interscambio.py`, `data/processed/risultato6_v2/porte.json`, `docs/RAPPORTO_R6_PORTE.txt`.

| Controllo | Esito |
|---|---|
| Luoghi critici = 378 | OK. Stessi 378 id del vecchio `mappa_r6.json` (verificato) |
| Parcheggi considerati = 3.431 | OK |
| Ogni parcheggio assegnato a un solo luogo | OK: 311 parcheggi entro 200 m, somma per porta = 311. Controllo indipendente con numpy: 311 parcheggi, 27.677 posti, uguale |
| Quota tra 0,25 e 0,27 | OK: 0,2567 (24.459 / 95.297, da `segnali.json`) |
| Nessun valore negativo | OK |
| Luoghi senza parcheggio / 1-49 posti / 50 o più | OK: **147 / 59 / 172** |
| Somma domande ≤ c2 totale × quota | **Non torna con il tetto del piano**: somma domande 30.083 contro 24.459. Causa: lo script 73 conta ogni spostamento due volte, nella zona di partenza e in quella di arrivo (`for z in (par, arr)`). Il tetto giusto è il doppio, 2 × 24.459 = 48.918, e 30.083 sta sotto. Il controllo nello script è stato corretto a questo tetto. Lo script 73 non è stato toccato |

Fermi (zona C003, Collegno), stessa porta con e senza l'osservazione di Leo:

| | Posti nominali | Posti utili | Copertura | Categoria |
|---|---|---|---|---|
| Con l'osservazione | 3.671 | 1.272 | 89% | Quasi |
| Senza (`--senza-osservazioni`) | 3.671 | 3.671 | 256% | Bastano |

La copertura scende con l'osservazione, come previsto. Test del metodo: Fermi **non** è in «Pochi» né in «Mancano», è in «Quasi».

Stato misurato (da `riempimento.json`, G = media feriale 10-16):
- STURA: pieno, G = 0,9012, 589 posti, a 76 m da una fermata, porta Q019.
- PORTA SUSA FS: a metà, G = 0,7818, 123 posti, a 80 m, porta Q005.
- CAIO MARIO: con posti liberi, G = 0,0149, 418 posti, a 92 m, porta Q023.

Dieci porte con più auto che non trovano posto:
1. Rivalta di Torino: 945 auto, mancano
2. Barriera di Milano: 820 auto, mancano
3. San Donato: 809 auto, pochi
4. Borgata Vittoria: 758 auto, mancano
5. Madonna di Campagna: 687 auto, mancano
6. San Paolo: 656 auto, mancano
7. Vanchiglia: 636 auto, pochi
8. San Salvario: 612 auto, mancano
9. Mirafiori Sud: 600 auto, quasi
10. Mercati generali: 545 auto, pochi

Nota: la regola «giorni validi ≥ 2» del piano conta tutti i giorni validi. I due giorni di riempimento sono entrambi feriali (15/10 e 16/10), quindi qui la regola non cambia nulla.

## Fase 2: `scripts/79_dati_mappa_r6.py` e `mappa_r6.json`

Il vecchio `mappa_r6.json` è stato sostituito (copia di sicurezza in scratchpad). Il nuovo contiene `porte` (29, con poligoni), `luoghi` (378), `parcheggi` (349: quelli entro 200 m più i garage 5T), `riepilogo`, `etichette`, `fonti`, `generato`. Peso 298 KB, limite 1,5 MB. Non contiene `eventi`, `ufficiali`, `zona_centrale`, classi dei parcheggi né scenari. I conteggi per categoria coincidono con la fase 1: fermate 147/59/172; porte Bastano 5, Quasi 12, Pochi 4, Mancano 8.

## Fase 3: mappa (`scripts/mappa_template.html`, `scripts/04_genera_mappa.py`)

- Tema «Parcheggi di interscambio» rifatto: stesso id e stesso link `#tema=interscambio`, nessuna opzione.
- Rimossi: `r6Vista`, `r6Insieme`, `r6Raggio`, zona centrale, eventi, classi, cerchi per insieme.
- Zone colorate per categoria; sotto zoom 13 il nome delle zone «Mancano» e «Pochi». Fermate da zoom 11, colore per posti entro 200 m. Parcheggi da zoom 14: contorno rosso se pieno, tratteggiato se stimati. Cerchio di 200 m attorno alla fermata o al parcheggio scelto.
- Clic: prima parcheggio, poi fermata, poi zona. Schede per zona (copertura, auto, posti, «Dove intervenire», strade d'ingresso), per fermata (categoria, parcheggi entro 200 m), per parcheggio (posti, tariffa, riempimento, curva delle 24 ore).
- Legenda unica con i numeri; guida riscritta per il Risultato 6.
- `04_genera_mappa.py` legge `mappa_r6.json` e stampa zone, fermate e parcheggi.
- Sintassi: lo script inline di `mappa_torino.html` passa `node --check` (node 22.21).
- Browser (pagina servita da `http://localhost:8765`, `.claude/launch.json` → `pagine-gtt`): il tema si apre, le zone sono colorate, la legenda riporta 5/12/4/8 zone e 147/59/172 fermate. Scheda di zona: Madonna di Campagna, «Mancano posti: copertura 10%». Scheda di fermata: Fermata 161 - NIZZA, 559 posti entro 200 m. Il cerchio di 200 m compare attorno alla fermata scelta.
- Errore in console «drawImage … canvas … width or height of 0»: compare anche con `#tema=servizio`, quindi è preesistente. Non toccato.
- Peso di `mappa_torino.html`: 23,6 MB dopo la rigenerazione. Il peso prima non è stato misurato, perché il file era già stato sovrascritto al primo lancio.

## Fase 4: scheda (`scripts/schede_risultati.py`, `data/schede_risultati.js`)

- Vecchia `scheda_r6` cancellata; `scheda_r6_v2` rinominata in `scheda_r6`, che legge solo `mappa_r6.json`. `main()` aggiornato.
- Titolo «Parcheggi di interscambio», stato «Aggiornato al 19/10/2026», tag «STIMATO / MISURATO (dati scarsi)».
- Numero chiave: 11.881 auto al giorno che non trovano posto.
- Risposta in 4 frasi: 117.208 auto in entrata nelle 29 zone; 30.083 potrebbero lasciare l'auto; zone più scoperte Rivalta di Torino (945), Barriera di Milano (820), San Donato (809); 8 zone «Mancano» e 4 «Pochi»; 147 fermate senza parcheggio e 59 con 1-49 posti; 11 parcheggi pieni di giorno, 3.533 posti; le misure coprono il 26,5% dei posti.
- Sei grafici; due immagini (`immagini/r6_torino.png`, `immagini/r6_zoom.png`: le fa Leo, se mancano la sezione non appare); metodo in 5 frasi; parametri; limiti; mappa; fonti; un solo scenario «Oggi» con 6 numeri.
- `node --check data/schede_risultati.js` passa. Nel file, nel Risultato 6, non compaiono «versione 2», «S1/S2/S3», «scenario», «Allianz», «solo sulla carta», «potenziale». Le parole trovate in altri risultati non rientrano nel piano.
- Scelte di testo: «altre 59 ne hanno tra 1 e 49 posti» (il piano scriveva «meno di 50», ma 59 sono 1-49 posti); i nomi in maiuscolo diventano «Rivalta di Torino», «Porta Susa FS».
- Pagina `simulazione.html` controllata nel browser: la scheda si apre con i numeri e i grafici.

## Fase 5: pulizia e rigenerazione

- Ricerca dei resti (`eventi`, `ufficiali`, `zona_centrale`, `r6Insieme`, `r6Raggio`, `r6Vista`, «solo sulla carta», «scenario» riferito al Risultato 6): nessun resto in `mappa_r6.json`, `mappa_template.html`, `schede_risultati.py`, `data/schede_risultati.js`, `mappa_torino.html`.
- Non cancellato nulla: non ho creato file intermedi nel repo (le prove stanno in scratchpad). `data/processed/risultato6_v2/giro1/` e i `RAPPORTO_R6V2_*` non sono stati toccati.
- Rigenerati: `mappa_torino.html`, `data/schede_risultati.js`, `mappa_r6.json`, `porte.json`, `docs/RAPPORTO_R6_PORTE.txt`.

## Tabella delle porte (ordine di auto che non trovano posto)

| Porta | Categoria | Copertura | Mancano (auto) |
|---|---|---|---|
| Rivalta di Torino | Mancano | 0% | 945 |
| Barriera di Milano | Mancano | 0% | 820 |
| San Donato | Pochi | 28% | 809 |
| Borgata Vittoria | Mancano | 17% | 758 |
| Madonna di Campagna | Mancano | 10% | 687 |
| San Paolo | Mancano | 6% | 656 |
| Vanchiglia | Pochi | 43% | 636 |
| San Salvario | Mancano | 12% | 612 |
| Mirafiori Sud | Quasi | 57% | 600 |
| Mercati generali | Pochi | 39% | 545 |
| Nichelino | Quasi | 64% | 528 |
| Mirafiori Nord | Pochi | 44% | 526 |
| San Mauro Torinese | Mancano | 12% | 520 |
| Crocetta | Quasi | 60% | 479 |
| Settimo Torinese | Quasi | 63% | 447 |
| Parella | Quasi | 69% | 406 |
| Nizza Millefonti | Quasi | 81% | 391 |
| Chieri | Quasi | 61% | 363 |
| Pozzo Strada | Quasi | 60% | 328 |
| Cenisia | Quasi | 71% | 308 |
| Venaria Reale | Quasi | 73% | 274 |
| Collegno | Quasi | 89% | 160 |
| Cambiano | Mancano | 19% | 79 |
| Grugliasco | Quasi | 100% | 2 |
| Moncalieri | Bastano | 195% | 0 |
| Beinasco | Bastano | 217% | 0 |
| Rivoli | Bastano | 117% | 0 |
| Aurora | Bastano | 191% | 0 |
| Falchera | Bastano | 171% | 0 |

## File modificati e nuovi

- Nuovi: `scripts/80_porte_interscambio.py`, `data/processed/risultato6_v2/porte.json`, `docs/RAPPORTO_R6_PORTE.txt`, `docs/ESITO_R6_PORTE.md`.
- Modificati: `scripts/79_dati_mappa_r6.py` (riscritto), `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`.
- Rigenerati: `data/processed/risultato6_v2/mappa_r6.json`, `mappa_torino.html`, `data/schede_risultati.js`.
- Non toccati: `MEMORIA_PROGETTO.md`, script 68-78, `data/processed/risultato6_v2/` (eccetto i file sopra), `data/ref/*`, `simulazione.html`.

## Anomalie e limiti aperti

- Il doppio conteggio dello script 73 (ogni spostamento in due zone) gonfia le somme per porta. Le singole porte sono corrette; i totali sono un tetto, non un conteggio. Da decidere se correggere lo script 73.
- Riempimento misurato su due giorni feriali [DATI SCARSI]. Fermi è una nota a mano.
- Posti stimati ±30%; distanze in linea d'aria; traffico delle strade ±38%.
- `MEMORIA_PROGETTO.md` non è stata aggiornata, perché il piano lo vieta. Va aggiornata insieme a questo esito.
