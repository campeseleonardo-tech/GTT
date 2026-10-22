# Piano 4 — Grafica, animazioni e racconto

Obiettivo: il sito deve colpire nei primi 5 secondi e far capire i risultati anche a chi non legge i testi.
Assorbe le parti rimaste di `PIANO_MAPPA.md` (schede uniformi dei temi) e di `PIANO_SCHEDE.md` (immagini, README).

Decisioni di Leo (22/10):
- i colori verde→rosso e blu→arancione erano una **direzione**, non una regola: si ripensano;
- il racconto è una **pagina separata** (`racconto.html`);
- sito in italiano con un **bottone IT/EN** su home, risultati e racconto (la mappa resta in italiano).

Resta come regola: **i numeri sono sempre scritti** accanto ai colori (chi non distingue i colori legge il numero), e le
animazioni si spengono per chi le ha disattivate nelle impostazioni del sistema («riduci movimento»).

## Dove va ogni elemento

| Elemento | Cos'è | Dove | Perché lì |
|---|---|---|---|
| **A. Mezzi in movimento** | sfondo scuro con la forma di Torino; i puntini dei bus e dei tram veri (GPS del Pi) si muovono durante un'ora tipica, accelerata in circa 20 secondi, con l'orologio che scorre | **home** (`index.html`), in alto dietro il titolo | è la prima cosa che si vede e mostra la raccolta dati del Pi |
| **B. Numeri che contano** | il numero grande di ogni risultato (es. 79.598) parte da 0 e sale fino al valore in circa 1 secondo, quando appare sullo schermo; le barre dei grafici crescono da sinistra | **home** (i 5 riquadri) e **risultati** (riquadri e schede aperte) | effetto piccolo, dà vita alle pagine senza cambiare niente |
| **C. Omini e quadratini** | il numero grande disegnato: 10 omini con 1 colorato («quasi 1 su 10» in doppio svantaggio); 100 quadratini con 13 rossi (passaggi oltre 5 minuti di ritardo); 12 pallini = i 12 punti dei parcheggi, 1 giallo e 11 grigi | **risultati**, nella scheda aperta subito sotto il numero grande; gli stessi disegni nel **racconto** | rendono il numero «fisico»; costano poco |
| **D. Gara bus contro auto** | due barre (o un bus e un'auto) che partono insieme da un punto e corrono verso Piazza Castello; l'auto arriva prima, il bus arriva dopo 2-3 volte il tempo; si sceglie il punto da una tendina | **risultati**: grafico principale delle schede 3 (parcheggi) e 4 (traffico). **Mappa**: lo stesso disegno, piccolo, nel pannello che si apre cliccando un punto del tema «Parcheggi di scambio» | nella scheda la vedono tutti; nella mappa serve a chi esplora un punto preciso. Un solo pezzo di codice usato in due posti |
| **E. La città che si spegne** | nei temi che cambiano con l'ora («Servizi a portata», «Mezzi pubblici sotto casa») un bottone ▶ fa scorrere le ore dalle 6 alle 24 con passaggi morbidi di colore | **mappa** | i dati per ora ci sono già nella mappa: si aggiunge solo il movimento |
| **F. Area che si espande** | da un luogo (es. Piazza Castello, Mirafiori, Falchera) un'area che si allarga minuto per minuto: dove arrivi coi mezzi in 10, 20, 30, 45 minuti, alle 8 e alle 23 | **racconto** (2-3 luoghi scelti) e poi **mappa** (vista nuova nel tema «Mezzi pubblici sotto casa») | richiede un calcolo nuovo sul PC (tempi da pochi luoghi di partenza, motore dello script 18): si parte dal racconto con pochi luoghi |
| **G. Racconto a scorrimento** | pagina dove il testo scorre a sinistra e la mappa a destra cambia a ogni paragrafo (come gli articoli del New York Times o di The Pudding) | **`racconto.html`**, con link dalla home (terzo bottone «La storia») e in fondo a `risultati.html` («Leggi la storia») | pagina a sé perché ha bisogno di una mappa leggera e di un layout tutto suo; in `risultati.html` la renderebbe pesante |
| **H. Stile nuovo** | colori, font, icona, ombre, modo scuro | **ovunque**: un file `assets/stile.css` comune a home, risultati e racconto; il pannello della mappa lo segue | le pagine oggi hanno ognuna il proprio stile, simile ma copiato |

### Il racconto (G), traccia proposta
1. **La promessa** (tesi del 2020): «sensori e dati cambieranno le città». Animazione A in piccolo.
2. **Il sistema**: un Raspberry Pi che legge Torino ogni minuto (numeri: letture, giorni, GB).
3. **Chi abita dove**: la mappa si colora di fragilità, poi di servizi; le 5 zone in doppio svantaggio si accendono. Omini (C).
4. **Muoversi**: area che si espande (F) alle 8 e alle 23; gara bus contro auto (D).
5. **Quanto ci si può fidare dei dati**: il feed dei ritardi che sbagliava di 2-3 volte, il bus con l'orologio 3 anni avanti.
6. **Cosa manca**: costi, passeggeri, treni. Link ai risultati e alla mappa.

## Stile (H): proposta da scegliere
Si preparano **3 prove di stile** su una pagina sola (`sviluppo/prove_stile.html`), con lo stesso riquadro, lo stesso grafico
e la stessa mappa in piccolo, e Leo sceglie:
1. **Notte**: blu notte, verde acqua acceso, corallo per gli allarmi (adatto all'animazione A).
2. **Carta**: sfondo crema, nero e un solo colore forte (stile giornale).
3. **Torino**: blu e oro, con il granata come colore di allarme.

Al posto del verde→rosso per bene/male: **verde acqua → corallo** (o blu → arancione), più leggibili anche per chi
confonde rosso e verde. Font: uno per i titoli con carattere e uno per i testi, salvati in `assets/` (le pagine
funzionano senza internet tranne gli sfondi della mappa).

## Passi

| # | Passo | Dove | Quanto |
|---|---|---|---|
| 1 | Prove di stile (3 varianti) → Leo sceglie | CLOUD | piccolo |
| 2 | `assets/stile.css` comune, icona, modo scuro; home e risultati con lo stile scelto; colori di mappa e schede ripensati insieme | CLOUD | medio |
| 3 | B numeri che contano + barre che crescono | CLOUD | piccolo |
| 4 | C omini e quadratini nelle schede (nuovo tipo di grafico in `schede_risultati.py` e `risultati.html`) | CLOUD | piccolo |
| 5 | D gara bus contro auto: componente unico, schede 3 e 4, poi pannello della mappa (i tempi ci sono già: script 93 e 94) | CLOUD | medio |
| 6 | A mezzi in movimento: script che estrae **un'ora tipica** di posizioni dallo storico (≤ 300 KB, piano 2 passo 4) → animazione nella home | CLOUD (codice) → PC (estratto) → CLOUD | medio |
| 7 | E bottone ▶ delle ore nella mappa | CLOUD | piccolo |
| 8 | Bottone IT/EN su home, risultati, racconto: testi inglesi completi nelle schede (oggi solo 3 righe) | CLOUD (Leo rilegge l'inglese) | medio |
| 9 | F tempi da 2-3 luoghi (script nuovo) | CLOUD (script) → PC (calcolo) | medio |
| 10 | G `racconto.html` | CLOUD | grande |
| 11 | Mappa: schede dei temi uniformi (resto di `PIANO_MAPPA.md`) | CLOUD | medio |
| 12 | Immagine di anteprima e screenshot per README (piano 1) | CLOUD | piccolo |

Prova di ogni passo: le pagine si aprono in un browser senza schermo nel cloud (0 errori, screenshot a misura di computer e
di telefono); Leo guarda gli screenshot e poi le pagine vere sul PC. Peso: la home sotto 1 MB, la mappa non oltre i 6 MB di oggi.

## Domande aperte per Leo
- Racconto: va bene la traccia in 6 parti? Vuoi usare la tesi in apertura o tenerla solo nel README?
- Area che si espande: quali 2-3 luoghi di partenza (proposta: Piazza Castello, Mirafiori Sud, Falchera)?
