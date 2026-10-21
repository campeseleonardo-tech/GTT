# Esito — R1: copertura a 5/10/15 minuti (A1) ed esposizione al traffico (A3) (21/10/2026)

Piano: `PIANO_RISULTATI.md`, parte A. Fatto in una **sessione cloud** (ramo `claude/keen-faraday-73k145`): non ci sono `data/`, il Pi,
R5 né Windows. Il codice è scritto e provato su dati finti; **i numeri veri si calcolano sul PC di Leo** (passi in fondo).
Le tabelle sono state compilate sul PC il 21/10 dopo i passi 2-7.

Stato: **OK** = fatto e provato; **DA PROVARE SUL PC** = scritto, mai girato sui dati veri.

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| 18 `--solo-piedi` | OK (21/10, PC) | Salta il mezzo pubblico, `--ore` si ignora (prima `--ore ""` si rompeva). Con `--out` ora vale anche un percorso (`data/processed/accessibilita_piedi10.json`): la parte `.json` e le cartelle si tolgono, il rapporto va in `RAPPORTO_ACCESSIBILITA_PIEDI10.txt`. `accessibilita.json` non si tocca. Non provato: serve R5. |
| 18 via Chieti | OK (codice) | Le sezioni `12720005328` e `12720000972` sono in `SEZIONI_FUORI_RETE` (valgono dal prossimo calcolo). |
| `R1_PIEDI_5_10.bat` | OK (21/10, PC: prova 200, 10 e 5 minuti; rapporti con «sezioni: 8317») | Passo 0: prova su 200 sezioni; poi 10 minuti; poi 5 minuti. Prima di ogni lancio cancella `accessibilita_parziale/`. Se un lancio cade, riparte dopo 60 s (10 volte). Log in `logs\R1_piedi_5_10.log`. |
| 21 sezione «v3» | OK (dati veri, 21/10: tutti i controlli OK) | JSON: `v3`; rapporto: «VERSIONE 3». Niente tolto. Controlli: somma dei residenti a ogni soglia = zone abitate; copertura 5 ≤ 10 ≤ 15; sezioni che peggiorano con più minuti. Un errore di somma o di ordine fa uscire lo script con errore (dopo aver scritto il rapporto). Se manca un file dei 5 o 10 minuti la soglia è saltata e scritto nel rapporto. |
| 21 per circoscrizione | Saltato | `sezioni_torino.json` non ha il campo (cerco `circoscrizione`, `circ`, `cir`). Lo scrive il rapporto. Il codice per circoscrizione c'è e funziona se il campo compare (provato su dati finti). |
| 92 esposizione al traffico | OK (dati veri, 21/10: girato senza modifiche, i campi c'erano; 180 tratte molto trafficate = R8) | Nuovo, sola lettura. Tratte come nel R8 (Torino, punteggio ≥ 3, ≥ 300 m, affidabili, niente autostrade, rango < 5) con almeno 11.720 veicoli/giorno. **Nel file `tratte_traffico.json` non c'è la geometria**: viene da `traffico_d/tratte.csv`. I nomi dei campi li ho presi dagli script 65-66; non ho potuto aprire il file vero. Se un campo non c'è, lo script si ferma e stampa i campi presenti. Scrive `esposizione_traffico.json` e `RAPPORTO_ESPOSIZIONE_TRAFFICO.txt` («stima debole: il modello del traffico sbaglia del ±38%», il 38 è letto dal file). Controllo: stesso numero di tratte del R8 (AVVISO se diverso). Per circoscrizione: stesso campo mancante, saltato. |
| Scheda R1 | OK (dati veri, 21/10: titolo, 3 barre, 3 punti chiave, aperta in Chromium senza errori) | `forma_r1` legge solo i JSON (21 v3, 92). Titolo, numero grande, barre al 100% (una per soglia), 3 punti chiave, altri 2 grafici, limiti di oggi + frase sul traffico, inglese invariato. 0 avvisi sui testi. Aprendo `risultati.html` con una scheda finta: 0 errori, grafico e parti chiuse a posto. |
| `.gitattributes` | OK | `*.bat text eol=crlf`; `git add --renormalize .` ha cambiato solo `scripts/CONTROLLA_LEOPI.bat` (era in CRLF nell'indice, ora LF nell'indice e CRLF sul PC). |
| Mappa: zona grigia | OK | Un clic su una zona grigia (sotto 1.000 ab/km², tranne nel tema «Abitanti per km²») chiude la scheda e mostra solo «zona con pochi abitanti». Provato in Chromium sulla mappa di oggi con il template nuovo: grigia → riga piccola, scheda chiusa; zona abitata → scheda aperta; 0 errori JavaScript. |
| `ESITO_SCHEDE.md` | OK | Cancellato (non lo cita nessuno). |
| Memoria | OK | Prossimo numero libero 93; voce in «In corso»; nota sullo script 18. `docs/R1_servizi.md` aggiornato. |

## Cosa NON è stato provato (nel cloud non si può)

- `18_accessibilita.py` con la prova `--campione 200` e i due lanci veri.
- `04_genera_mappa.py`, `prova_pagine_r6.py` (serve Edge o Chrome con PowerShell) e `schede_risultati.py` completo (leggono `data/`).
  `schede_risultati.py` è stato provato solo per R1, con i JSON finti; `04` solo compilato. Il template della mappa è stato provato
  in Chromium inserendo i dati della mappa di oggi.
- Il confronto «a 15 minuti vicino a quanto c'è oggi» e gli altri controlli di buon senso sui numeri veri.

## Tabella 1 — copertura a piedi, Torino, zone abitate (compilata)

| Tempo a piedi | Tutti e 5 i servizi | 4 servizi | 3 o meno | Residenti zone abitate |
|---|---|---|---|---|
| 5 minuti | 574.422 (68,25%) | 187.168 (22,24%) | 80.001 (9,51%) | 841.591 |
| 10 minuti | 814.527 (96,78%) | 20.600 (2,45%) | 6.464 (0,77%) | 841.591 |
| 15 minuti | 834.963 (99,21%) | 5.302 (0,63%) | 1.326 (0,16%) | 841.591 |

Cosa deve venire: a 15 minuti vicino a oggi (quasi tutti: nel rapporto di oggi 6.768 sono in zone poco abitate e 362 senza 3 o più servizi);
a 5 minuti molto meno; 5 ≤ 10 ≤ 15. Se a 15 minuti viene lontano da oggi, fermarsi e dirlo a Claude.

## Tabella 2 — esposizione al traffico (compilata; totale 841.980 residenti in 3.545 sezioni)

| Classe | Distanza dalla strada molto trafficata | Residenti | % |
|---|---|---|---|
| Esposta | meno di 100 m | 190.255 | 22,6% |
| Vicina | 100-250 m | 259.977 | 30,9% |
| Lontana | oltre 250 m | 391.748 | 46,5% |

Cosa deve venire: una minoranza di esposti (il controllo avvisa se oltre il 50%) e 180 tratte molto trafficate come nel R8.
Stima debole: il modello del traffico sbaglia del ±38%.

## Passi sul PC (Leo)

1. Aprire il ramo con le modifiche (in `prova` dopo l'unione) e fare doppio clic su `scripts\R1_PIEDI_5_10.bat`. **Il calcolo è lungo (ore)**:
   la finestra va lasciata aperta. Prima fa la prova su 200 sezioni e si ferma: deve scrivere `RAPPORTO_ACCESSIBILITA_PROVA200.txt` con
   circa 200 sezioni, «TP: non calcolato» e mediane a piedi sensate; poi un tasto lancia 10 minuti e poi 5 minuti.
2. A fine corsa devono esserci `data\processed\accessibilita_piedi10.json` e `accessibilita_piedi5.json` (rapporti con «sezioni: 8317»).
3. `python scripts\21_risultato1_vuoti.py` → in fondo a `RAPPORTO_RISULTATO1.txt`, «VERSIONE 3», tutti i controlli OK.
4. `python scripts\92_esposizione_traffico.py` → `RAPPORTO_ESPOSIZIONE_TRAFFICO.txt`. Se si ferma per un campo mancante, mandare il messaggio a Claude.
5. `python scripts\schede_risultati.py`, `python scripts\04_genera_mappa.py`, `python scripts\prova_pagine_r6.py` (deve dare 0 errori).
6. Aprire `risultati.html`, scheda del Risultato 1: titolo «A 15 minuti quasi tutti hanno i servizi; a 5 minuti molti meno», tre barre,
   punto sul traffico, punto sulla collina. Aprire `mappa_torino.html`: clic su una zona grigia = una riga, nessuna scheda.
7. Compilare qui le due tabelle.


## Esito sul PC (21/10/2026)

- Passo 1 verificato: `accessibilita_piedi5.json` e `accessibilita_piedi10.json` esistono; i rapporti dicono «sezioni: 8317 (Torino 4044, cintura 4273)».
- 21: v3 tutti i controlli OK. Somme uguali a 841.591 a ogni soglia; copertura 5 ≤ 10 ≤ 15; nessuna sezione peggiora con più minuti.
  **A 15 minuti il numero coincide con oggi**: 834.963 con tutti e 5 i servizi (gli stessi «0 mancanti» della scheda precedente) e 362 con 3 mancanti; nessuna correzione necessaria.
- 92: **180 tratte molto trafficate, come nel R8** (139,9 km). Esposti 22,6%, sotto il 50%. Nessun campo mancante, nessuna modifica allo script.
- AVVISO (spiegato): i residenti del 92 (841.980, 3.545 sezioni) sono 389 più di quelli del 21 v3 (841.591, 3.543 sezioni): il 92 include le zone «da verificare», il 21 le lascia fuori.
- AVVISO: per circoscrizione saltato in 21 e 92 (`sezioni_torino.json` non ha il campo), come previsto.
- Prove: 21, 92, `schede_risultati.py`, `04_genera_mappa.py` (mappa 13,54 MB), `prova_pagine_r6.py`: **0 errori su 18 pagine**.
- Non rifatto da me: il clic su una zona grigia nella mappa (provato nel cloud sul template; qui solo 0 errori a runtime).
