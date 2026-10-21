# Piano — mappa più semplice e gradevole

Obiettivo: si entra e si vede Torino dal satellite, pulita; si sceglie un tema e si vede **solo** quello, con una
legenda corta. Tutto il resto è nascosto. File: `scripts/mappa_template.html` (pagina), `scripts/04_genera_mappa.py`
(dati). Dopo ogni giro: `python scripts\04_genera_mappa.py` e `python scripts\prova_pagine_r6.py --senza-screenshot`
(0 errori), poi guardare la pagina in Chromium.

Decisioni di Leo (21/10): partenza vuota su satellite; nomi chiari e corti; «Tutti i servizi» in accessibilità;
«Chi abita qui» più completo; dei due «Chi va dove» resta solo l'IMQ; «Velocità e traffico» = media per tipo di giorno
su tutti i giorni raccolti, niente giornate singole.

## 1. Temi: nomi e ordine (proposta, valori predefiniti di Claude)

Menu con due gruppi (`<optgroup>`) e una prima voce vuota.

| Gruppo | Nome nuovo | Era | Viste (menu «Cosa vedere») |
|---|---|---|---|
| — | **Scegli un tema…** | — | (nessuna: mappa vuota) |
| Chi abita e cosa trova | **Chi abita qui** | Vulnerabilità e residenti (parte) + «Solo abitanti» | vedi sezione 3 |
| | **Fragilità sociale** | Vulnerabilità e residenti (indice) | Indice (0-100) · Senza lavoro · Poca istruzione · Case affollate · Anziani |
| | **Servizi a portata** | Accessibilità ai servizi | **Tutti i servizi** (nuova, predefinita) · Scuole · Salute · Negozi · Verde; a piedi 15' / coi mezzi 45' |
| | **Servizi mancanti** | Dove mancano i servizi (R1) | come oggi; cambia col nuovo R1 (`PIANO_RISULTATI.md`, A) |
| | **Prezzo delle case** | Valore immobiliare | Abitazioni (predefinita) · Negozi · Uffici; via box e magazzini |
| Come ci si muove | **Mezzi pubblici sotto casa** | Servizio e abitanti | Passaggi all'ora per abitante · Passaggi all'ora |
| | **Spostamenti** | Chi va dove: tutti gli spostamenti (IMQ) | come oggi; via «Residenti 11-84» (sta in «Chi abita qui») |
| | **Velocità e traffico** | Bus e traffico misurati | sezione 4 |
| | **Ritardi delle linee** | Puntualità delle linee (R4) | come oggi |
| | **Parcheggi di scambio** | Parcheggi per lasciare l'auto (R6) | Dove ci sono · Dove servirebbero |
| | **Luoghi della città** | Catalogo dei dati (inventario) | sezione 6 |

Tolto: **Chi va dove: pendolari** (tema, legenda, `costruisci_pendolari` nel 04, `D.pend`).
Gli indirizzi vecchi (`#tema=interscambio`, `#tema=puntualita` …) restano validi: gli id non cambiano, cambiano solo
le etichette (le schede usano quei link).

## 2. Partenza, sfondo, pannello

| Cosa | Oggi | Nuovo |
|---|---|---|
| Tema di partenza | «Servizio e abitanti» | **nessuno**: niente aree, niente linee, legenda chiusa; nel pannello solo titolo, una riga e il menu dei temi |
| Sfondo di partenza | Mappa chiara | **Satellite**; con un tema acceso l'intensità dello sfondo scende da sola al 60% (le aree si leggono meglio) |
| Sfondi | chiara, satellite, stradale, nessuno + cursore intensità + griglia | **Satellite · Chiara · Nessuno**; cursore dentro «Altre opzioni» chiuso; griglia tolta |
| Scatola «Quando» | sempre visibile; play, velocità 1×-240×, «Adesso» | visibile **solo** nei temi che cambiano con l'ora (Spostamenti, Velocità e traffico, Ritardi, Mezzi sotto casa, Servizi a portata coi mezzi): **Feriale/Sabato/Domenica + ora a scatti di un'ora**; via play, velocità, «Adesso», minuti |
| Sovrapposizioni | 6 caselle + tendina giornate | dentro «Altre opzioni» chiuso: **Linee** (con «solo una linea») e **Fermate**; tolti: corse simulate in movimento, sensori (stanno nel loro tema), mezzi di una giornata |
| Legenda | riquadro sempre presente | appare solo con un tema; massimo 6 righe di colore + 1 riga di fonte |
| Box «Simulazione» | bottone «Apri pagina simulazione» | link «**I risultati →**» in fondo al pannello |
| Guida e fonti | lunga, con testo del R6 | 5 righe (come leggere i colori, le etichette, l'area) + fonti; il dettaglio dei temi sta nella descrizione del tema |
| Avvisi GTT | fotografia del 9/10 nel pannello delle fermate | **tolti** (dato vecchio; 0,12 MB) |
| Mezzi «live», `stat.js` per la tendina giornate | caricati | tolti dalla pagina pubblica (restano sul Pi per la raccolta) |

Pannello: larghezza fissa, sezioni che si aprono a fisarmonica; su telefono il pannello parte chiuso con un
bottone «Temi».

## 3. «Chi abita qui» più completo

Oggi in mappa ci sono solo abitanti, famiglie, occupati, ragazzi 5-14, anziani. Lo script 05 legge già dal censimento
2021 anche età per classi (P14-P29) e titolo di studio in 5 livelli (P83-P90), ma solo alcuni campi arrivano alla mappa.
Regola fissa del progetto: **mai nazionalità**.

Viste (ognuna una percentuale della sezione, colori blu→arancione perché non sono un giudizio):

| Vista | Calcolo | Campi |
|---|---|---|
| Abitanti per km² (predefinita) | p / a | già in mappa |
| Bambini e ragazzi (0-14) | quota | P14-P16 (aggiungere P14 se c'è) |
| Anziani (65+) e grandi anziani (80+) | quota | P27-P29 (80+ = P29 se la classe è quella: controllare il tracciato) |
| Età media (stima) | media pesata dei centri delle classi | P14-P29 |
| Laureati | it / ist9 | già letti dal 05, da portare in mappa |
| Occupati (15-64) | occ / p1564 | già in mappa |
| Persone per famiglia | p / f | già in mappa |

**Scheda della zona** (clic su una sezione): un piccolo profilo con 5 barre orizzontali (giovani, anziani,
laureati, occupati, persone per famiglia) e accanto il valore di Torino come tacca, così si vede subito in cosa la zona
è diversa dalla media. Una riga: «Censimento 2021, sezione di N abitanti». Sotto 50 abitanti: «troppo pochi
abitanti per le percentuali».

Da controllare prima sul file ISTAT (tracciato R01 2021): quali classi d'età esatte sono P14-P29 e se ci sono le
famiglie per numero di componenti (persone che vivono sole: buon indicatore di fragilità degli anziani). Se c'è,
aggiungere «Persone sole» alla Fragilità sociale.

Lavoro: 05 (campi), 04 (proiezione `sez` nel template: **ricordarsi di aggiungerli anche lì**), template (viste,
legenda, profilo).

## 4. «Velocità e traffico»: solo medie

- Velocità dei bus: già una media degli ultimi 28 giorni per linea × tipo di giorno × ora (`calcola_velocita` nel 04).
  Cambiare `VEL_GIORNI = 28` in **tutti i giorni raccolti** (con avviso se un tipo di giorno ha meno di 3 giorni).
- Traffico ai sensori: oggi dal «tipico» di `stat.js` (Pi, nessuna lettura scartata). Passare a
  `data/processed/velocita_5t.json` (script 26: solo letture affidabili, già per tipo di giorno × ora), **dentro** la
  mappa come gli altri dati: niente file esterno.
- Togliere la tendina «Rivedi i mezzi di una giornata», `caricaReplay`, `disegnaReplay`, i file `replay_*.js` dalla
  pubblicazione (script 86) e la casella `Lreplay`.
- Legenda: «Media di N giorni feriali (dal … al …)», senza elenco di date.

## 5. Accessibilità: «Tutti i servizi»

Sommare i servizi non funziona (i negozi sono migliaia, le scuole decine: la somma sarebbe «quanti negozi»).
Proposta: **punteggio 0-100** = media dei percentili dei 5 gruppi (scuole, salute, negozi, fermate, verde) della
sezione, calcolata a parte per «a piedi» e «coi mezzi». 100 = fra le sezioni meglio servite per ogni tipo.
Si calcola nel 04 dai valori già in `acc`; legenda verde→rosso a 5 classi; clic sulla sezione = i 5 numeri.
Fuori Torino: stessa nota di oggi (servizi da OpenStreetMap, meno completi).

## 6. «Luoghi della città» al posto del catalogo grezzo

Oggi: 7 gruppi, 40 tabelle, metadati tecnici (licenza, CRS, campi mancanti). Nuovo: 6 caselle — Scuole e nidi ·
Ospedali e salute · Mercati · Cultura (musei, biblioteche, cinema) · Sport · Mobilità (ciclabili, bike sharing,
ricarica, parcheggi in struttura) — con il punto e il nome al clic. Il resto del catalogo esce dalla mappa (resta
nei dati per i calcoli). Peso: oggi il catalogo si carica a parte; controllare che resti così.

## 7. Peso della pagina (13,6 MB → obiettivo sotto 7 MB)

| Parte | Oggi | Azione |
|---|---|---|
| Sezioni (forme + valori) | 9,3 MB | coordinate a 4 decimali (~10 m) e semplificazione delle forme (Douglas-Peucker 5 m) nel 04; `acc` per 24 ore × 5 gruppi solo dove serve (le ore TP si possono ridurre a 6 fasce) |
| Fermate | 1,7 MB | togliere i campi non usati dopo la pulizia (avvisi) |
| Corse simulate | 0,6 MB | **tolte** (niente più corse in movimento) |
| IMQ, linee, OMI, R6 | 1,7 MB | invariati |
| Pendolari, avvisi, replay | — | tolti |

## 8. Altre criticità trovate

- **Clic sulle aree**: ogni tema ha una sua scheda; renderle uguali (titolo = nome del posto, 3-5 righe, fonte in
  piccolo). Il pannello del R6 è stato corretto il 20/10: ricontrollare le etichette lunghe anche negli altri temi.
- **Colori sul satellite**: le aree piene al 100% coprono tutto; opacità 0,65 e bordi bianchi sottili solo da zoom 14.
- **Zoom**: il bottone «◎ Cintura» è poco chiaro: diventa «Tutta l'area».
- **Testi con date e sigle** (12 date nel template, «[revisione 18/10]», «Q001-Q009», «IMQ», «5T»): sigle spiegate una
  volta nella guida; nei temi parole semplici («indagine sugli spostamenti 2022»).
- **Sfondi Esri**: condizioni d'uso da controllare prima di pubblicare; attribuzione sempre visibile.
- **Accessibilità della pagina**: le legende scrivono già i numeri (bene per i daltonici); controllare il contrasto dei
  testi grigi sul satellite (pannello bianco: ok).

## 9. Ordine dei giri

1. Pulizia (sezione 2) + nomi e gruppi (sezione 1) + tolti pendolari, replay, corse simulate, avvisi, griglia.
2. Velocità e traffico solo medie (4) + «Tutti i servizi» (5).
3. «Chi abita qui» e «Fragilità sociale» (3).
4. Luoghi della città (6) + peso (7) + criticità (8).
Ogni giro: rigenerare, provare le pagine, guardare la mappa; Leo apre `mappa_torino.html` e controlla: all'apertura
satellite e nessun colore; il menu ha i due gruppi; ogni tema mostra solo il suo.
