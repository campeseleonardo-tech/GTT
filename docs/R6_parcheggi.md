# Risultato 6 — Parcheggi per lasciare l'auto

**Domanda.** Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, così
da togliere auto dal centro?

**Tag dati:** [STIMATO] (indagine IMQ 2022 + modello del traffico + inventario dei parcheggi); riempimento [MISURATO]
solo per pochi garage.

## Messaggio

**I parcheggi di scambio convengono solo se in centro si perdono abbastanza minuti a parcheggiare.** Misura principale (script 94): i **minuti di pareggio**, cioè quanti minuti per parcheggiare in centro rendono il tempo in auto uguale al tempo coi mezzi da quel punto a Piazza Castello alle 8 (minuti = tempo coi mezzi − flusso libero × fattore di punta). Dal 24/10 la stima principale dell'auto è TomTom (per percorso) e i sensori 5T restano come stima più favorevole all'auto: vengono due valori per punto, non un minimo e un massimo; il titolo della scheda usa la mediana dei 12 punti. Non c'è nessuna soglia scelta da noi: la classe con 1,5 volte e la sensibilità a 5/10/15 minuti restano sotto, solo per confronto. I numeri si leggono in `docs/rapporti/RAPPORTO_R6_BUS_CONTRO_AUTO.txt` (sezione «MINUTI DI PAREGGIO»).

Numeri (calcolo sul PC, 24/10, TomTom per percorso): mediana dei 12 punti **16-28 minuti** (TomTom - sensori; con TomTom a fattore unico 17-28; con Google 21-28); i più promettenti sono vicini alla metro (Metro Massaua 3-15, Regina Margherita 8-24, e fra gli interscambi Fermi 0-17 e Venchi Unica 4-17); i più lontani 29-43 (Ponte Cavalieri Templari, Marsè). Stura è pieno anche se servono 14-27 minuti: chi lo usa sceglie per altri motivi (costo, ZTL, stress del traffico), che il calcolo dei tempi non vede.

Confronto con la letteratura (da verificare sulla fonte originale, vedi `sviluppo/TESI_E_PROGETTO.md`): in media servono circa 7,8 minuti per trovare parcheggio, meno dei 16 minuti di pareggio con TomTom (28 con i sensori).

Perché questa misura: con la classe «1,5 volte» e la sola stima TomTom il risultato passa da 8 punti su 12 «il bus conviene» (5 minuti di parcheggio) a 10 (10 minuti) e a 12 (15 minuti). Il risultato vero è quindi la soglia stessa, ed è la conclusione classica sui parcheggi di scambio: funzionano se parcheggiare in centro è scomodo o caro.

- Interscambi esistenti (con TomTom): pieno e con bus che conviene, Stura; poco usati: Caio Mario con bus che conviene (ha il contatore fermo), Sofia senza (rapporto oltre 1,5).
- Fermate importanti senza posti bastanti: 179 su 274.
- Limiti: tempi coi mezzi solo GTT, senza treni; parcheggio in centro fissato a 5 minuti; costo del parcheggio non considerato.

### Sensibilità ai minuti per parcheggiare in centro

| Minuti | Punti: conviene / non conviene | Interscambi: conviene / non conviene |
|---|---|---|
| 5 | 8 / 4 | 4 / 1 |
| 10 | 10 / 2 | 5 / 0 |
| 15 | 12 / 0 | 5 / 0 |

### Punti prioritari (rapporto = tempo coi mezzi / tempo in auto)

| Luogo | Posti che mancano | Mezzi (min) | Auto (min, sensori - TomTom) | Rapporto (TomTom - sensori) | Classe (5 min) | Classe con 5 / 10 / 15 min |
|---|---|---|---|---|---|---|
| Santa Rita | 450 | 36 | 14-27 | 1,3-2,6 | il bus conviene | conviene / conviene / conviene |
| Metro Massaua | 350 | 25 | 15-27 | 0,9-1,7 | il bus conviene | conviene / conviene / conviene |
| Ponte Cavalieri Templari | 350 | 51 | 18-27 | 1,9-2,8 | il bus non conviene | non conviene / non conviene / conviene |
| Regina Margherita | 350 | 31 | 12-28 | 1,1-2,7 | il bus conviene | conviene / conviene / conviene |
| Pasini | 250 | 28 | 12-20 | 1,4-2,3 | il bus conviene | conviene / conviene / conviene |
| Leonardo Da Vinci | 200 | 59 | 20-38 | 1,5-3,0 | il bus non conviene | non conviene / conviene / conviene |
| Drosso Cap | 200 | 43 | 17-31 | 1,4-2,5 | il bus conviene | conviene / conviene / conviene |
| Stura Lazio | 200 | 37 | 14-27 | 1,4-2,6 | il bus conviene | conviene / conviene / conviene |
| Marsè | 150 | 61 | 23-34 | 1,8-2,6 | il bus non conviene | non conviene / non conviene / conviene |
| Derna Est | 100 | 34 | 14-24 | 1,4-2,5 | il bus conviene | conviene / conviene / conviene |
| Ferrara | 80 | 49 | 20-35 | 1,4-2,5 | il bus conviene | conviene / conviene / conviene |
| Zara | 60 | 33 | 12-19 | 1,8-2,8 | il bus non conviene | non conviene / conviene / conviene |

### Interscambi esistenti

| Luogo | Riempimento | Mezzi (min) | Auto (min, sensori - TomTom) | Rapporto (TomTom - sensori) | Classe (5 min) | Classe con 5 / 10 / 15 min |
|---|---|---|---|---|---|---|
| Stura | pieno | 39 | 17-30 | 1,3-2,2 | il bus conviene | conviene / conviene / conviene |
| Venchi Unica | a meta | 28 | 16-29 | 1,0-1,8 | il bus conviene | conviene / conviene / conviene |
| Caio Mario | libero | 38 | 16-30 | 1,3-2,4 | il bus conviene | conviene / conviene / conviene |
| Fermi | non misurato | 31 | 19-37 | 0,8-1,7 | il bus conviene | conviene / conviene / conviene |
| Sofia | libero | 33 | 13-22 | 1,5-2,5 | il bus non conviene | non conviene / conviene / conviene |

## Come si calcola

| Criterio | Valore |
|---|---|
| Auto in entrata al mattino | IMQ 2022, partenza 06-10, conducente + car sharing: 87.162 dalla cintura e da fuori; più i torinesi dei quartieri periferici diretti alle zone Q001-Q009 (29.988, il 34%, soglia 25%) |
| Chi già oggi lascia l'auto | 5,8% (5.067 auto; **64 interviste**) |
| Auto che passano accanto a una fermata | instradamento sul modello del traffico (R8, stima debole ±38%) |
| **Fermata importante** | fuori dal centro (Q001-Q009), **metro/stazione/capolinea oppure almeno 10 corse all'ora** nelle ore dei pendolari, **e almeno 1.000 auto in entrata** che passano accanto: **274** |
| Parcheggio adatto | aperto, fuori dal centro, almeno 20 posti, non di ospedali/università/centri commerciali: 1.874 (157.103 posti) |
| Fermata coperta | posti adatti entro 400 m a piedi ≥ auto che passano × 5,8% |
| Punto prioritario | uno per asse d'ingresso, almeno 3 km da Piazza Castello, almeno 50 posti che mancano; stesso asse = meno di 2 km, o stessa strada entro 5 km |
| Posti che mancano | arrotondati (decine sotto 100, cinquantine sotto 1.000, centinaia sopra); il calcolo resta in `mancano_stima` |
| Linee utili | le 54 che toccano più zone fra le 20 più popolari per arrivi/km² (IMQ senza ritorni a casa, script 87); mostrate nel pannello del parcheggio |

## Numeri (`docs/rapporti/RAPPORTO_R6_*.txt`)

- **274 fermate importanti, 179 senza posti bastanti**: 68 senza nessun parcheggio adatto, 111 con posti
  insufficienti, 95 sufficienti.
- **12 punti prioritari**: Santa Rita (circa 450), Metro Massaua, Ponte Cavalieri Templari, Regina Margherita (circa
  350), Pasini, Leonardo da Vinci, Drosso Cap, Stura Lazio, Marsè, Derna Est, Ferrara, Zara.
- La somma dei posti che mancano nei punti resta sotto le 5.067 auto che si possono fermare (un punto per asse: le
  stesse auto non si contano due volte; controllo dello script 85).
- Zone più popolari per arrivi/km²: Centro (44.404), San Paolo, Cenisia, San Donato, Nizza Millefonti.
- 1.264 parcheggi adatti su 1.874 non hanno una linea utile entro 400 m a piedi.
- In mappa anche 80 parcheggi del centro (in viola); verifiche automatiche dello script 85: 0 non superate.

### Prove di controllo

- **Sensori 5T** (script 88): ordine delle auto in entrata del mattino, modello contro sensori entro 25 km da Torino:
  ρ 0,83 per sensore, **0,60 per luogo (debole)**, 0,52 senza i sensori fuori rete. Il modello sottostima le
  provinciali (SP1, SP8, SP2) e sopravvaluta corso Giulio Cesare, Unione Sovietica, Allamano, Sebastopoli.
- **Interscambi del Comune** (5): solo Stura dice qualcosa (pieno, su strada con molte auto: coerente); Caio Mario ha il
  contatore fermo, Fermi non trasmette, Venchi Unica è a metà, Sofia è poco usato con molte auto accanto. Le
  osservazioni personali sui parcheggi servono solo come controllo a posteriori (`data/ref/parcheggi_osservazioni.json`)
  e non entrano nei dati.
- **Sensibilità della regola** (misurata una volta, lo script è stato tolto): N 10-30 corse/ora e M 500-3.000 auto danno da 25 a 347 fermate; più la
  regola è severa, meno dei punti prioritari restano coperti.

### Bus contro auto verso Piazza Castello (script 94)

**Dal giro L8 (24/10/2026, decisione di Leo) la stima dell'auto è una, quella di TomTom, col fattore del percorso stesso** (percorso «luogo → Piazza Castello» alle 8, script 101; tutti i 17 luoghi hanno il proprio fattore: da 1,88 a 4,1, mediana 2,59). Auto = flusso libero × fattore + 5 minuti di parcheggio (sensibilità 10 e 15). Rapporto = mezzi / auto. Classi, **solo con la stima TomTom e con la soglia di prima (1,5)**: **il bus conviene** se il rapporto è ≤ 1,5, **non conviene** se è oltre; la classe «dipende dal traffico» non c'è più. La stima dei sensori 5T (fattore 1,2, la più favorevole all'auto: non conta semafori e incroci) resta come sensibilità nel JSON (`rapporto_alto`, `pareggio_alto_min`) e nel testo.

**Numeri (alle 8, 5 minuti di parcheggio):** punti «il bus conviene / non conviene» **8 / 4** su 12; interscambi **4 / 1** su 5; minuti di pareggio (mediana dei 12 punti) **16** con TomTom e 28 con i sensori. Prima (L6bis, fattore unico d'entrata 2,59, tre classi): 0 / 7 «dipende» / 5 e interscambi 0 / 5 / 0; pareggio 17-28. Cambia la classe di alcuni punti perché ognuno ha il proprio fattore, non la mediana.

Correzione del 24/10 (L6bis) e motivi: vedi `docs/R8_traffico.md` (sezioni «L8» e «Noi contro Google Maps»). TomTom è un tempo previsto su traffico tipico (partenze di martedì 10/11/2026; mercoledì 11 per i percorsi di L6), non misurato; un solo servizio. Dati di traffico: TomTom (`docs/FONTI_DATI.md`).

### Bus contro auto a 4 ore del giorno (script 100; dal giro L8 con TomTom per percorso e per ora)

Gli stessi 12 punti e 5 interscambi verso Piazza Castello alle 8:00, 13:00, 17:30 e 21:00 (scelte e ipotesi in `docs/R8_traffico.md`, sezione «Non solo all'ora di punta»).

| Ora | Mezzi dai punti prioritari (mediana) | Minuti di pareggio, punti (stima TomTom - stima sensori) | Punti: conviene / non conviene | Interscambi: conviene / non conviene |
|---|---|---|---|---|
| 8:00 | 36,5 min | 16-28 (16,00 - 27,50) | 8 / 4 | 4 / 1 |
| 13:00 | 35,0 min | 18-27 (17,85 - 26,75) | 6 / 6 | 5 / 0 |
| 17:30 | 37,5 min | 17-28 (16,75 - 28,50) | 9 / 3 | 5 / 0 |
| 21:00 | 34,5 min | 21-28 (21,10 - 28,00) | 2 / 10 | 3 / 2 |

Il messaggio: con TomTom per percorso i punti dove il bus conviene (rapporto ≤ 1,5) sono 8 su 12 alle 8, 6 alle 13, 9 alle 17:30 e 2 la sera. Resta vero che il bus batte l'auto solo se in centro si perdono parecchi minuti a parcheggiare (16 con TomTom, 28 con i sensori alle 8). I mezzi dai punti prioritari la sera non impiegano di più che alle 8 (AVVISO del controllo: l'orario programmato non ha traffico).

## Mappa e scheda

Tema «Parcheggi per lasciare l'auto»: fermate importanti, parcheggi adatti, punti prioritari, pannello con linee
utili; il pannello dei punti prioritari e degli interscambi mostra anche i tempi verso Piazza Castello e la classe (script 94). Scheda `scheda_r6` in `scripts/schede_risultati.py`. In pagina niente versioni, scenari, eventi o classi dei
parcheggi.

## Limiti

- I «posti che mancano» sono ordini di grandezza (quota da 64 interviste × traffico ±38%).
- Il modello del traffico non ha le code e preferisce le strade veloci.
- Riempimento misurato solo per pochi garage 5T; occupazione disponibile dal 14/10.
- Il controllo con i sensori è debole (ρ 0,52–0,60).
- Una fermata a 560-650 m dalla metro non conta come fermata della metro.

## Script e come rifarlo

| Script | Cosa fa |
|---|---|
| 68-69 | inventari dei parcheggi e dei luoghi |
| 71-73, 77 | riempimento, nodi, segnali, modulo delle strade |
| 81 | auto che passano accanto a ogni fermata |
| 82 | parcheggi adatti |
| 83 | fermate importanti (regola N, M) |
| 84 | risultato: coperture, punti prioritari |
| 94 | bus contro auto verso Piazza Castello: classe dei punti prioritari e degli interscambi (serve il 93) |
| 79 | dati della mappa |
| 80 | funzioni usate da 84-85 |
| 85 | verifiche automatiche |
| 87 · 88 | popolarità delle zone e linee utili · confronto con i sensori 5T |

Catena completa (circa 4 minuti), da lanciare dopo ogni rifacimento dei dati:

```
scripts\RISULTATO6_RIFAI.bat
```

Poi `python scripts\schede_risultati.py` e `python scripts\prova_pagine.py --senza-screenshot`. Si rifà con più
giorni feriali di parcheggi raccolti (serve almeno una settimana).
