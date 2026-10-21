# Risultato 6 — Parcheggi per lasciare l'auto

**Domanda.** Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, così
da togliere auto dal centro?

**Tag dati:** [STIMATO] (indagine IMQ 2022 + modello del traffico + inventario dei parcheggi); riempimento [MISURATO]
solo per pochi garage.

## Messaggio

**I parcheggi di scambio convengono solo se in centro si perdono abbastanza minuti a parcheggiare.** Misura principale (script 94): i **minuti di pareggio**, cioè quanti minuti per parcheggiare in centro rendono il tempo in auto uguale al tempo coi mezzi da quel punto a Piazza Castello alle 8 (minuti = tempo coi mezzi − flusso libero × fattore di punta). Con i due fattori dell'auto (Google e sensori) viene una forbice per punto; il titolo della scheda usa la mediana dei 12 punti. Non c'è nessuna soglia scelta da noi: la classe con 1,5 volte e la sensibilità a 5/10/15 minuti restano sotto, solo per confronto. I numeri si leggono in `docs/rapporti/RAPPORTO_R6_BUS_CONTRO_AUTO.txt` (sezione «MINUTI DI PAREGGIO»).

Numeri (calcolo sul PC): mediana dei 12 punti **21-28 minuti**; i più promettenti sono vicini alla metro (Metro Massaua 7-15, e fra gli interscambi Fermi 7-17 e Venchi Unica 9-17); i più lontani 33-44 (Leonardo da Vinci). Stura è pieno anche se servono 17-27 minuti: chi lo usa sceglie per altri motivi (costo, ZTL, stress del traffico), che il calcolo dei tempi non vede.

Perché questa misura: con la classe «1,5 volte» il risultato passava da 1 punto su 12 (5 minuti di parcheggio) a 10 su 12 (10 minuti). Il risultato vero è quindi la soglia stessa, ed è la conclusione classica sui parcheggi di scambio: funzionano se parcheggiare in centro è scomodo o caro.

- Interscambi esistenti: pieno e con bus competitivo, Stura; poco usati e senza bus competitivo, Caio Mario e Sofia (Caio Mario ha il contatore fermo).
- Fermate importanti senza posti bastanti: 179 su 274.
- Limiti: tempi coi mezzi solo GTT, senza treni; parcheggio in centro fissato a 5 minuti; costo del parcheggio non considerato.

### Sensibilità ai minuti per parcheggiare in centro

| Minuti | Punti: conviene / dipende / non conviene | Interscambi: conviene / dipende / non conviene |
|---|---|---|
| 5 | 0 / 1 / 11 | 0 / 3 / 2 |
| 10 | 1 / 9 / 2 | 2 / 3 / 0 |
| 15 | 4 / 8 / 0 | 5 / 0 / 0 |

### Punti prioritari (rapporto = tempo coi mezzi / tempo in auto)

| Luogo | Posti che mancano | Mezzi (min) | Auto (min, fattore alto-basso) | Rapporto (basso-alto) | Classe (5 min) | Classe con 5 / 10 / 15 min |
|---|---|---|---|---|---|---|
| Santa Rita | 450 | 36 | 14-20 | 1,8-2,6 | il bus non conviene | non conviene / dipende / dipende |
| Metro Massaua | 350 | 25 | 15-23 | 1,1-1,7 | dipende dal traffico | dipende / conviene / conviene |
| Ponte Cavalieri Templari | 350 | 51 | 18-28 | 1,8-2,8 | il bus non conviene | non conviene / non conviene / dipende |
| Regina Margherita | 350 | 31 | 12-17 | 1,9-2,7 | il bus non conviene | non conviene / dipende / conviene |
| Pasini | 250 | 28 | 12-17 | 1,6-2,3 | il bus non conviene | non conviene / dipende / conviene |
| Leonardo Da Vinci | 200 | 59 | 20-31 | 1,9-3,0 | il bus non conviene | non conviene / non conviene / dipende |
| Drosso Cap | 200 | 43 | 17-27 | 1,6-2,5 | il bus non conviene | non conviene / dipende / dipende |
| Stura Lazio | 200 | 37 | 14-21 | 1,7-2,6 | il bus non conviene | non conviene / dipende / dipende |
| Marsè | 150 | 61 | 23-37 | 1,7-2,6 | il bus non conviene | non conviene / dipende / dipende |
| Derna Est | 100 | 34 | 14-20 | 1,7-2,5 | il bus non conviene | non conviene / dipende / conviene |
| Ferrara | 80 | 49 | 20-31 | 1,6-2,5 | il bus non conviene | non conviene / dipende / dipende |
| Zara | 60 | 33 | 12-17 | 1,9-2,8 | il bus non conviene | non conviene / dipende / dipende |

### Interscambi esistenti

| Luogo | Riempimento | Mezzi (min) | Auto (min, fattore alto-basso) | Rapporto (basso-alto) | Classe (5 min) | Classe con 5 / 10 / 15 min |
|---|---|---|---|---|---|---|
| Stura | pieno | 39 | 17-27 | 1,5-2,2 | dipende dal traffico | dipende / dipende / conviene |
| Venchi Unica | a meta | 28 | 16-24 | 1,2-1,8 | dipende dal traffico | dipende / conviene / conviene |
| Caio Mario | libero | 38 | 16-24 | 1,6-2,4 | il bus non conviene | non conviene / dipende / conviene |
| Fermi | non misurato | 31 | 19-29 | 1,1-1,7 | dipende dal traffico | dipende / conviene / conviene |
| Sofia | libero | 33 | 13-20 | 1,7-2,5 | il bus non conviene | non conviene / dipende / conviene |

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
- **Sensibilità della regola** (script 89): N 10-30 corse/ora e M 500-3.000 auto danno da 25 a 347 fermate; più la
  regola è severa, meno dei punti prioritari restano coperti.

### Bus contro auto verso Piazza Castello (script 94)

Regola fissata prima dei numeri, rapporto = mezzi / auto: **il bus conviene** se ≤ 1,5 con entrambi i fattori del R8 (1,2 sensori, 2,1 Google); **dipende dal traffico** se ≤ 1,5 solo col fattore basso; **non conviene** se oltre 1,5 con entrambi. Auto = flusso libero × fattore + minuti di parcheggio (5 ufficiale). Tabelle e sensibilità in testa al documento; dettagli in `docs/rapporti/RAPPORTO_R6_BUS_CONTRO_AUTO.txt`.

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
| 87 · 88 · 89 | popolarità delle zone e linee utili · confronto con i sensori 5T · proposta di sensibilità |

Catena completa (circa 4 minuti), da lanciare dopo ogni rifacimento dei dati:

```
scripts\RISULTATO6_RIFAI.bat
```

Poi `python scripts\schede_risultati.py` e `python scripts\prova_pagine_r6.py --senza-screenshot`. Si rifà con più
giorni feriali di parcheggi raccolti (serve almeno una settimana).
