# ESITO C4 — tre prove di stile (cloud, 22/10/2026)

Piano 4, passo 1. **Leo deve scegliere lo stile** (o un misto): il giro C5 parte solo dopo la sua scelta, scritta nella memoria.

## Cosa c'è
- `sviluppo/prove_stile.html`: tre colonne (una sotto l'altra su telefono) — **Notte**, **Carta**, **Torino**. In ognuna, uguali per tutti: titolo «Torino Mobilità»; riquadro del **Risultato 5 vero** (titolo e numero 79.598 da `data/schede_risultati.js`);
  grafico a barre con i dati veri della stessa scheda; 10 omini con 1 colorato; **mappa di Torino** con le sezioni colorate per fragilità sociale (dati veri dentro `mappa_torino.html`, 5 gruppi con i numeri scritti nella legenda);
  piè di pagina «Chi sono». Bottone **Chiaro / Scuro** in alto (di partenza segue il sistema; `#scuro` nell'indirizzo lo forza). Sotto ogni colonna: palette con i codici, scala della mappa, font e contrasti.
- Bene/male: **verde acqua → corallo** in tutti (in «Torino» il corallo diventa granata `#a61e33` chiaro, `#ee6a80` scuro). Numeri sempre scritti.
- Font (Google Fonts, solo parte latina, salvati in `sviluppo/prove_stile_font/`, 339 KB; la pagina non ha nessun link esterno): **Notte** Space Grotesk + DM Sans · **Carta** Fraunces + Source Sans 3 · **Torino** Barlow Condensed + Barlow.
- Screenshot (pagina intera): `sviluppo/prove_stile_computer_chiaro.png`, `..._computer_scuro.png`, `..._telefono_chiaro.png`, `..._telefono_scuro.png`.
- Come rifarlo: `python scripts/prove/costruisci_prove_stile.py` poi `python scripts/prove/screenshot_prove_stile.py`.

## Palette (chiaro / scuro)
| | fondo | riquadro | testo | link e numeri | colore pieno | verde acqua | corallo / granata |
|---|---|---|---|---|---|---|---|
| Notte chiaro | #f2f6fb | #ffffff | #0b1426 | #00796f | #0fb5a6 | #0b9d90 | #d6443a |
| Notte scuro | #0b1426 | #121e38 | #e9eefa | #3ee0cc | #19d3c5 | #19d3c5 | #ff7a6b |
| Carta chiaro | #f5eddc | #fffaf0 | #151515 | #b92f16 | #e8472f | #0d8076 | #e8472f |
| Carta scuro | #1a1712 | #241f18 | #f4ecd9 | #ff7b5c | #ff6a47 | #3cc9b8 | #ff6a47 |
| Torino chiaro | #f3f5fa | #ffffff | #0b2559 | #0b3a8c | #c9a227 (oro) | #0b8f8a | #a61e33 (granata) |
| Torino scuro | #08142e | #0f2147 | #f1f4fb | #e3bf55 | #e0b84a (oro) | #32cfc2 | #ee6a80 |

Altri codici (testo secondario, bordi, scala di 5 colori della mappa) nella pagina, sotto ogni colonna.

## Contrasti (WCAG; testi ≥ 4,5, grafici ≥ 3), valore più basso per stile
| | testi | grafici (verde acqua e corallo su riquadro) |
|---|---|---|
| Notte chiaro | 4,88 | 3,37 |
| Notte scuro | 7,82 | 6,50 |
| Carta chiaro | 4,67 | 3,76 |
| Carta scuro | 6,30 | 5,77 |
| Torino chiaro | 6,10 | 3,95 |
| Torino scuro | 7,67 | 5,27 |
Tutti sopra la soglia (tabella completa di ogni coppia nella pagina). Verifiche: nessun errore JavaScript, nessuna richiesta esterna, nessuno scorrimento orizzontale a 390 px, font caricati.

## Note per scegliere
- **Notte**: il più «da schermo», il verde acqua è il colore dei numeri; di giorno è il più freddo e meno distinto.
- **Carta**: il più riconoscibile (titoli con le grazie, filetti neri, un solo colore forte che qui è il corallo): il bene (verde acqua) compare solo nei grafici.
- **Torino**: il più istituzionale; l'oro dà identità ma i numeri grandi diventano blu (chiaro) o oro (scuro) e il granata sostituisce il corallo, quindi la scala «bene → male» si allontana un po' dalla regola.
- Limite: la mappa mostra la fragilità sociale (una sola variabile) con la stessa scala per tutti; nel sito vero le scale cambiano per tema.
