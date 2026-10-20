# Risultato 6 — Parcheggi per lasciare l'auto: STATO ATTUALE (corretto il 20/10/2026)

Correzioni eseguite sul PC il 20/10 (esito: `docs/archivio/correzioni_20ott/ESITO_CORREZIONI_GENERALI.md`, analisi e
piano nella stessa cartella) e **ricontrollate da Claude** sui dati dentro `mappa_torino.html` (classi, aree, distanze
dei 20 punti dal centro: tutto coincide). Catena: `scripts\RISULTATO6_RIFAI.bat` (71, 72, 73, 81, 82, 83, 84, 79, 85,
04, schede, prova delle pagine; ~4 minuti). Rapporti: `docs/RAPPORTO_R6_*.txt`.

## Domanda
Dove mancano posti per lasciare l'auto prima di entrare in città, vicino a una fermata importante, così da togliere
auto dal centro?

## Criteri (valori decisi con Leo il 20/10)
| Criterio | Valore |
|---|---|
| Auto in entrata al mattino | IMQ 2022, partenza 06-10, conducente + car sharing: 87.162 dalla cintura e da fuori; torinesi dei quartieri periferici verso Q001-Q009 inclusi (29.988 = 34%, soglia 25%) |
| Chi già oggi lascia l'auto | 5,8% (5.067 auto, **64 interviste**) |
| Auto che passano accanto | instradamento sul modello del traffico V0 (stima debole ±38%) |
| Fermate importanti | 10% più alto fra 3.898 luoghi fuori da Q001-Q009: **391**; segnali a2, b2, c4, e a pesi uguali |
| Parcheggi adatti | aperti, fuori da Q001-Q009, ≥ 20 posti, non di ospedali/università/centri commerciali: 1.874 (157.103 posti) |
| Fermata coperta | posti adatti entro 400 m a piedi ≥ auto che passano × 5,8% |

## Risultati
- **253 fermate importanti su 391 senza posti bastanti** (99 senza nessun parcheggio adatto, 154 con posti
  insufficienti); 116 con posti sufficienti; 22 con poche auto da fermare.
- **76 aree**: 20 critiche, 5 scarse, 5 buone, **46 «Pochi dati»** (meno di 5 fermate).
- **16 punti prioritari** (giro del 20/10 12:11: uno per asse d'ingresso, almeno 3 km dal centro, almeno 50 posti
  mancanti): in testa Maroncelli (Moncalieri, circa 650), Pellerina (circa 450), Santa Rita (circa 400), Barbera,
  Metro Massaua.
- **Validazione sui 5 interscambi del Comune**: solo Stura dice qualcosa (pieno, su strada con molte auto: coerente);
  Caio Mario contatore fermo, Fermi non trasmette, Venchi Unica a metà, Sofia poco usato con molte auto accanto.
- Mappa 13,6 MB (era 23,6); 142 parcheggi mostrati.

## Punti deboli trovati da Claude nel ricontrollo (20/10, sera) e decisioni di Leo
1. **Stesse auto contate in più punti** (Maroncelli, Bosso e Ponte Cavalieri Templari sullo stesso asse di
   Moncalieri; somma dei 20 punti 6.356 > 5.067 auto che si possono fermare). **Leo: un punto per asse.** Nello
   script 84: si tiene il gruppo con più posti mancanti e si scartano quelli a meno di 2 km, o sulla stessa strada a
   meno di 5 km (solo il nome non basta: «strada Torino» c'è a Pino e a Mirafiori). Sui 20 punti di oggi ne
   restano 11 su assi diversi; la lista si riempie fino a 20 con gli altri gruppi.
2. **Gioanetti a 1,4 km dal centro.** **Leo: niente punti a meno di 3 km** da Piazza Castello.
3. **«Posti che mancano» con precisione apparente** (quota da 64 interviste × traffico ±38%). **Leo: arrotondati**
   (decine sotto 100, cinquantine sotto 1.000, centinaia sopra); il calcolo resta in `mancano_stima`.
4. **Modello del traffico senza code** (Corso Francia fuori dai 15 luoghi con più auto, Strada Trieste in cima):
   da controllare con i sensori 5T del mattino in entrata. Da fare.
5. **Validazione quasi vuota** (1 interscambio su 5) e **46 aree su 76 senza colore**: più giorni di parcheggi
   (inizio novembre), poi si rivede.

Punti 1-3 fatti nel codice (84, controlli nell'85) ed **eseguiti sul PC il 20/10 alle 11:52**: 60 gruppi, 41
scartati (stesso asse o sotto 3 km), 19 punti; verifiche 0 non superate; somma dei posti che mancano 4.319 (sotto
le 5.067 auto da fermare: ora torna). In testa: Maroncelli (Moncalieri, circa 650), Pellerina (circa 450), Santa
Rita (circa 400), Barbera (circa 350), Metro Massaua (circa 300). Gli ultimi tre punti avevano 0-23 posti mancanti:
aggiunta la regola **almeno 50 posti mancanti** per entrare nella lista: giro del 20/10 12:11, **16 punti**, verifiche
0 non superate.

**Giro 1 (20/10, 15:06)**: pannello corretto, vista «aree» tolta, 80 parcheggi del centro in viola, **15 punti**
(il gruppo di Chieri, prima «Valle Ceppi», è uscito: a pari punteggio la fermata «capo» del gruppo cambiava a ogni
giro; corretto con uno spareggio fisso negli script 83 e 84, il numero definitivo esce al prossimo giro).

## Commenti di Leo (20/10) e fattibilità

| Commento | Controllo | Fattibile? |
|---|---|---|
| **Il pannello a destra cliccando un parcheggio è rotto** | Confermato da Claude in Chromium sulla mappa del 20/10: le etichette lunghe («Distanza a piedi dalla fermata importante più vicina») non vanno a capo e schiacciano i valori, che finiscono una lettera per riga fuori dal riquadro. Causa: una regola CSS (`.sc-det-k{flex:none}` in `mappa_template.html`). In più il bollino «STIMATO» compare anche sui parcheggi con posti dichiarati (Stura) | Sì, piccolo (CSS + bollino solo se i posti sono stimati). Riguarda tutte le schede con etichette lunghe, non solo il R6 |
| **«Dove ci sono parcheggi» anche per il centro** | I parcheggi del centro sono esclusi perché non servono a lasciare l'auto prima di entrare; ci sono nei dati (`parcheggi.json`, garage 5T con riempimento) | Sì, piccolo-medio: mostrati con un colore a parte («in centro: non per lasciare l'auto»), fuori dai conteggi |
| **«In quali aree manca parcheggio» con gli esagoni non dice nulla** | 46 aree su 76 sono «Pochi dati» | Sì: si toglie la vista |
| **L'unico sottotema pulito è «Dove servirebbe un parcheggio»** | Dopo il giro del 20/10 (16 punti per asse) | — |
| **«Fermate importanti» balla troppo** fra 5%, 10% e 15% (197 / 391 / 586) | È una classifica: la soglia decide quante sono | Sì, medio: regola fissa (sotto) |
| **Parcheggi esistenti e «linee utili»**: quante linee utili tocca ogni parcheggio; linea utile = tocca servizi e zone «popolari» | Servizi per sezione ci sono; spostamenti in arrivo per zona IMQ (101 zone, per scopo) ci sono; per sezione no | Sì, medio: «popolarità» per zona IMQ + servizi (sotto) |

## Decisioni di Leo (20/10)

1. **Pannello** corretto; **parcheggi del centro mostrati** con colore a parte; **vista «aree» tolta**: restano 2 viste
   («Dove ci sono parcheggi?», «Dove servirebbe di più un parcheggio?»). Lo script 84 può smettere di calcolare le
   aree, o tenerle solo nel rapporto.
2. **Fermate importanti con una regola fissa**, non una percentuale. Proposta di Claude da discutere: fermata
   importante = fuori da Q001-Q009 **e** (metro, stazione o capolinea **oppure** almeno N passaggi all'ora fra le 7 e
   le 9) **e** almeno M auto in entrata che passano accanto. N e M si scelgono guardando le distribuzioni (non per
   far tornare un numero), e si dichiara quante fermate ne escono.
3. **«Popolarità» delle zone come misura comune**: spostamenti che **arrivano** in ogni zona IMQ (per scopo:
   lavoro/studio, svago e acquisti, altro) + servizi del catalogo; **linea utile** = linea che tocca zone popolari e
   servizi. Serve a R6 (parcheggi che portano a linee utili), R4 (linee in zone affollate), costi. Va in uno script
   suo (numero libero 87).

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Pannello: etichette che vanno a capo; bollino «STIMATO» solo se i posti sono stimati | `mappa_template.html` | piccolo |
| 2 | Togliere la vista «aree» (mappa, scheda, testi); tenere le aree solo nel rapporto o toglierle | template, 84, `schede_risultati.py` | piccolo |
| 3 | Parcheggi del centro nella vista «Dove ci sono parcheggi?», colore a parte, fuori dai conteggi | 84, 79, template | piccolo-medio |
| 4 | Confronto auto in entrata (modello) con i sensori 5T del mattino in entrata: il controllo con la realtà che manca | nuovo controllo nell'85 o script a parte | medio |
| 5 | Fermate importanti con regola fissa (decisione 2): proposta con le distribuzioni, poi scelta di Leo | 83 | medio |
| 6 | Popolarità delle zone + linee utili (script 87); poi per ogni parcheggio adatto: quante linee utili tocca | 87, poi 84 | medio |
| 7 | Rilancio dopo ≥ 5 feriali di parcheggi (inizio novembre): `scripts\RISULTATO6_RIFAI.bat`; screenshot di Leo | — | — |
| — | Congelato: eventi (stadi, palazzetti) | — | — |

## Esito del prompt A (20/10 sera, ricontrollato da Claude)
- **Spareggio**: catena rifatta due volte, **15 punti prioritari identici** (nomi, ordine, zone). Chiuso.
- **Confronto con i sensori 5T** (script 88, `docs/RAPPORTO_R6_CONFRONTO_SENSORI.txt`; codice letto, corretto):
  33 sensori entro 25 km con flusso al mattino. ρ = 0,83 sensore per sensore, ma è gonfiato (i due versi dello stesso
  punto contano due volte e 8 sensori su strade fuori dalla rete del modello stanno tutti in fondo in entrambe le
  classifiche). **Numero onesto: ρ = 0,52 su 23 luoghi dentro la rete** (0,60 con tutti i 27): **debole**, come il
  modello del traffico del R8 (0,605).
- Dove sbaglia: **sottostima gli ingressi da nord-ovest** (SP8 Druento, SP1 Valli di Lanzo, SP2 Germagnano, Corso
  Vercelli, raccordo di Caselle: misurati 3.000-5.000, modello 500-1.100) e **sovrastima i corsi interni a ovest**
  (Sebastopoli, Allamano, Unione Sovietica). In parte non è un errore: i sensori lontani (14-16 km) contano anche
  il traffico locale, che non va a Torino. In cima l'ordine è giusto (Unità d'Italia, Trieste a Moncalieri, Orbassano).
- **Dubbio del punto debole 4 risolto**: Corso Francia non è sottostimato (modello 7°-10°, sensori 13°-14° su 27),
  Corso Trieste (Moncalieri) è 2° anche nei sensori. Il modello senza code non stravolge le strade d'ingresso
  principali.
- Effetto sul risultato: nessun numero cambia. I punti del nord (Pellerina, Potenza, Rebaudengo, Stura Lazio,
  Pianezza) potrebbero servire **più** di quanto dice il modello, non meno. **Valore predefinito di Claude**: una riga
  nei limiti della scheda R6 («confronto con i sensori 5T: ordine debole, ρ 0,52; il modello sottostima gli ingressi
  da nord-ovest»), letta dal rapporto, nel prossimo giro che tocca la scheda R6 (dopo i prompt B e C).

## Esito del prompt B e decisione di Leo (20/10 sera)
Script 89 ricontrollato (stessi 3.898 eleggibili dello script 83; `docs/RAPPORTO_R6_PROPOSTA_FERMATE.txt`). Unica
scorciatoia: i punti prioritari collegati alle fermate per nome entro 3 km (solo per la proposta; nello script 83 si
usano le coordinate). **Leo sceglie N = 10, M = 1.000**: fermata importante = fuori da Q001-Q009 **e** (metro, stazione
o capolinea, **oppure** almeno 10 corse/ora nelle ore dei pendolari) **e** almeno 1.000 auto in entrata che passano
accanto. Ne escono **274** (205 Torino, 68 cintura, 1 resto), 211 delle 391 di oggi restano, 63 nuove; 12 dei 15 punti
di oggi hanno ancora una fermata. Perché: 10 corse/ora = un mezzo ogni 6 minuti; 1.000 auto × 5,8% ≈ 58 posti,
coerente con «almeno 50 posti mancanti»; M basso perché il modello sottostima il nord-ovest.
**Si applica nel giro di modifica del R6**, dopo il prompt C, insieme alla riga dei sensori nei limiti e alle linee
utili per parcheggio: una sola rigenerazione. Il prompt di quel giro si scrive dopo il ricontrollo del C.

## Come eseguirli

- Lavori 1-3: dentro il **Giro 1** (`docs/PIANO_GIRO1_RITOCCHI.md`, passi 1-3).
- Lavori 4, 5, 6: **un prompt per volta**, nell'ordine, ognuno con il suo esito; Claude ricontrolla fra l'uno e
  l'altro. Nessuno cambia i numeri pubblicati: producono rapporti e proposte. Le modifiche al risultato si decidono
  dopo, con Leo.

Prompt rivisti da Claude il 20/10 sera: A comincia con il rilancio della catena (controllo dello spareggio fisso) e
confronta anche per luogo (i due versi insieme); B usa b2 com'è davvero (ore 6-10 e 16-20) e non scrive a mano i punti;
C esclude i ritorni a casa dalla popolarità e non premia le linee solo perché sono lunghe.

### Prompt A — controllo con i sensori 5T (lavoro 4, script 88)

> Sei un agente sul progetto GTT (`C:\projects\Progetti\GTT`, ramo `prova`; prima `git status` pulito e
> `git pull origin prova`; alla fine commit e push da solo come dice `AGENTS.md`; `python` del PATH, mai Anaconda;
> questi prompt leggono i dati: vanno eseguiti **sul PC**, non nel cloud). Leggi `AGENTS.md` e la sezione
> «Commenti di Leo» di `docs/PIANO_RISULTATO6.md`.
> 0. Prima di tutto lancia `scripts\RISULTATO6_RIFAI.bat` e scrivi nell'esito quanti punti prioritari escono e i loro
>    nomi (è il primo giro con lo spareggio fisso negli script 83 e 84; al giro del 20/10 15:06 erano 15). Lancialo
>    una seconda volta: nomi e numero devono essere **identici** (se no: AVVISO con le differenze).
> Poi scrivi **un solo script nuovo** `scripts/88_confronto_auto_sensori.py`
> (solo lettura) che confronta le auto in entrata del mattino stimate dal modello con i sensori 5T:
> 1. sensori: `data/processed/velocita_5t.json`: `sensori[lcd1]` ha `via`, `dir`, `lat`, `lon`, `urbano` e
>    `celle["0"][ora] = {v, f, n, g, ok}` ("0" = feriale, `f` = veicoli/ora); flusso misurato = somma di `f` delle
>    ore 6, 7, 8, 9 (ora locale), solo celle con `ok` vero;
> 2. modello: carica lo script 81 con `comuni.carica_script("81_auto_di_passaggio.py")`, la rete come fa lo script
>    81 nel suo `main()` e `data/processed/risultato6_v2/auto_passaggio.npz` (`flusso_archi`); per ogni sensore usa
>    la funzione `c4_per_punti(rete, flusso_archi, [(id, lat, lon)], 50)` del modulo 81;
> 3. tieni solo i sensori di Torino e cintura con flusso misurato > 0. Il sensore conta un verso solo, il modello le
>    auto vicino al punto: fai il confronto **due volte**, (a) sensore per sensore, (b) per luogo, sommando i sensori a
>    meno di 30 m fra loro (i due versi della stessa strada). Confronto per **ordine** (correlazione di
>    Spearman con `scipy.stats.spearmanr`), non per valore (il modello conta solo le auto in entrata del mattino, il
>    sensore tutte le auto): stampa ρ, numero di sensori o luoghi, e la tabella sensore / strada / misurato /
>    modello / posizione in classifica nei due elenchi;
> 4. scrivi `docs/RAPPORTO_R6_CONFRONTO_SENSORI.txt` con: ρ di (a) e (b), le 10 strade dove le due classifiche sono
>    più diverse, dove stanno Corso Francia e Strada Trieste nelle due classifiche, e una frase di lettura sul
>    confronto (b) (ρ ≥ 0,6 buono, 0,4-0,6 debole, < 0,4 il modello non segue le strade d'ingresso).
> Non toccare altri script né i risultati. Esito in `docs/ESITO_R6_SENSORI.md` con l'uscita completa. Alla fine un
> riassunto di 10 righe in italiano semplice.

### Prompt B — fermate importanti con regola fissa: solo la proposta (lavoro 5, script 89)

> Stesse regole del prompt A (senza il punto 0). Scrivi `scripts/89_proposta_fermate_importanti.py` (solo lettura)
> che, per i 3.898 luoghi eleggibili di `data/processed/risultato6_v2/fermate_importanti.json` (o dei file che lo
> script 83 legge: guarda il suo `main()`), stampa le **distribuzioni** (percentili 10/25/50/75/90/95/99) di: corse
> all'ora nelle ore dei pendolari (segnale b2: media delle ore 6-10 e 16-20 di un feriale, come lo usa lo script 83),
> auto in entrata che passano accanto (c4), presenza di metro/stazione/capolinea (dai nodi, `nodi.json`; il capolinea
> conta già solo con almeno 4 corse/ora fra le 6 e le 9, script 72). Poi conta quante fermate risultano importanti con
> la regola «(metro o stazione o capolinea, oppure almeno N corse/ora) **e** almeno M auto che passano» per una griglia
> di valori: N = 10, 15, 20, 30; M = 500, 1.000, 2.000, 3.000. Per ogni combinazione: quante fermate (Torino /
> cintura), quante delle fermate importanti di oggi restano, quanti dei punti prioritari di oggi (letti da
> `mappa_r6.json`, `punti_prioritari`: mai scritti a mano) hanno almeno una fermata nella nuova lista. Scrivi tutto in
> `docs/RAPPORTO_R6_PROPOSTA_FERMATE.txt`. **Non** cambiare lo script 83 né i risultati: Leo sceglie N e M dopo.
> Esito in `docs/ESITO_R6_PROPOSTA_FERMATE.md`.

### Prompt C — popolarità delle zone e linee utili (lavoro 6, script 87)

> Stesse regole del prompt A (senza il punto 0). Scrivi `scripts/87_popolarita_zone.py` (solo lettura dei dati,
> scrive solo i suoi file). 1) Popolarità di ogni zona IMQ (le zone di `data/processed/imq_zone.json`, geometria in
> `imq_zone_geo.json`: non scrivere il numero a mano): spostamenti che **arrivano** nella zona,
> dall'IMQ 2022 (`data/processed/imq/spostamenti.csv`, separatore `;`, colonne `COD_ARR`, `SCOPO` e peso come le legge
> lo script 81 nella funzione `leggi_domanda()`), **esclusi i ritorni a casa** (scopi `08` e `11`: altrimenti le zone
> popolari sarebbero solo quelle dove si abita), in tre gruppi: lavoro/studio (`01`, `02`, `03`), acquisti/cure/svago
> (`04`, `06`, `07`), altro (`05`, `09`, `10` e `12`-`16`, come fa lo script 14); più il numero di servizi del
> catalogo nella zona (Torino: `data/processed/catalogo` come lo legge lo script 18; fuori Torino
> `data/processed/servizi_osm_cintura.json`, dato meno completo: scrivilo). 2) Per ogni linea GTT (GTFS in
> `data/raw`, sola lettura): le zone che tocca (fermate dentro la zona, per coordinate, mai per nome) e due punteggi:
> (a) **quante delle 20 zone più popolari tocca** (punteggio principale: non premia una linea solo perché è lunga);
> (b) somma della popolarità delle zone toccate (solo confronto, anche divisa per scopo). «Linea utile» = 25% più alto
> per (a), a pari valore conta (b). 3) Per ogni parcheggio adatto (`data/processed/risultato6_v2/parcheggi_adatti.json`):
> quante linee utili passano a meno di 400 m a piedi (linea d'aria × 1,3). Uscite: `data/processed/popolarita_zone.json`
> e `docs/RAPPORTO_POPOLARITA_ZONE.txt` con le 15 zone più popolari, le 15 linee più utili, i 15 parcheggi adatti con
> più linee utili. Controlli: arrivi contati + ritorni a casa esclusi = totale spostamenti IMQ (stesso peso); nessuna
> zona senza nome; se le 10 linee più lunghe sono tutte fra le prime 15 per (a): AVVISO.
> Esito in `docs/ESITO_POPOLARITA_ZONE.md`.

---

# Riepilogo del 19/10 (PRIMA delle correzioni: superato, resta per la storia)

## Domanda
«Dove mancano posti per lasciare l'auto vicino a dove si entra in città o nel trasporto pubblico?» — per capire dove mettere un parcheggio nuovo o ampliarne uno, così da togliere auto dalla circolazione (si lascia l'auto e si prosegue con il trasporto pubblico). Tutta la città conta, tranne il centro (Q001) per le fermate; i parcheggi contano ovunque.

## Come funziona (criteri, uno per uno)
| Criterio | Valore | Perché |
|---|---|---|
| Fermate importanti | 378 luoghi (fermate entro 40 m = un luogo): il 10% più alto di un punteggio su 4.425 luoghi della Città metropolitana. Il punteggio mescola importanza della strada (strade della Fase 5 con punteggio corretto: primarie ≥ 4, secondarie ≥ 3), corse nelle ore dei pendolari, pendolari della zona, ZTL, calo di velocità ai sensori, nodo treno/metro | sono i punti dove passa più gente e più mezzi |
| Parcheggi | 5.205 trovati (5T, Comune, OpenStreetMap) → 1.774 esclusi (1.048 sosta lungo strada, 385 solo clienti, 341 privati) → **3.431 considerati** → 1.147 con almeno 50 posti (175.356 posti) | per chi lascia l'auto contano i parcheggi aperti dove si può stare tutto il giorno |
| Posti | dichiarati (374) o **stimati a 25 m² a posto** (2.902; mediana verificata 24,4-25,4 su 152-172 parcheggi con posti dichiarati, fascia 14-33 m²: incertezza ±30%) | spesso il numero di posti non c'è |
| Distanza | **200 m** in linea d'aria (a 100 m: 315 fermate senza 50 posti; a 400 m: 66) | è il criterio che pesa di più |
| Fermata coperta | almeno **50 posti nominali** entro 200 m: 147 senza nessun parcheggio, 59 con 1-49 posti, 172 con 50+ | |
| Riempimento | solo **misurato** (feed 5T, 32-36 garage, 2 giorni feriali, ore 10-16): pieno ≥ 85%, con posti liberi < 50%. Le osservazioni di Leo (es. Fermi sempre pieno) **non entrano nei dati**: controllo a posteriori nel rapporto (oggi «non confermabile»: nessun parcheggio vicino trasmette) | un parcheggio pieno non serve |
| Aree | celle esagonali di circa 2 km² (lato 900 m): Critica ≥ 60% delle fermate senza 50 posti, Scarsa 30-59%, Buona < 30%; sotto 3 fermate «dato indicativo» | le zone IMQ erano troppo grandi e diseguali |
| 20 punti | fermate senza 50 posti raggruppate entro 1 km, in ordine di punteggio; per ognuno i parcheggi da 100+ posti entro 600 m che potrebbero ampliarsi | risponde a «dove metterne uno o ingrandirlo» |
| Direzioni d'ingresso (solo riferimento in scheda) | 8 settori attorno a Piazza Castello; auto in entrata al mattino (IMQ 2022, 95.297) × 26% (chi già oggi cambia con un mezzo pubblico, 299 interviste) = 24.459 auto; confrontate con i posti | stima di riferimento, non guida la mappa |

## Risultati
- **206 fermate importanti su 378 non hanno vicino un parcheggio con almeno 50 posti** (147 non ne hanno nessuno).
- **73 aree**: 37 critiche, 12 scarse, 24 buone (26 con meno di 3 fermate: indicative). Le zone più scoperte sono Mirafiori (Nord e Sud), San Donato, Crocetta-Cenisia, Parella, parte di Moncalieri.
- **20 punti prioritari**: in testa Settembrini e Pavese (Mirafiori Sud), Industria (San Donato), Metro Spezia e Metro Lingotto (Nizza Millefonti), Provana (Collegno).
- **Parcheggi mostrati in mappa: 212** (58.833 posti): almeno 100 posti entro 400 m da una fermata importante o da un nodo forte (346 nodi: metro, treno, capolinea, frequenti) più i garage 5T con dati; include il Palavela (568 posti stimati, il sito turistico dice «fino a 600»).
- **Riempimento**: 9 parcheggi pieni di giorno (3.041 posti); i dati coprono solo il 25-36% dei posti mostrati. Il grafico più chiaro: le curve a 24 ore dei garage (tre comportamenti: si riempiono di giorno / sono più pieni di notte / dato fermo).
- I 4 interscambi del Comune (Stura, Caio Mario, Sofia, Venchi Unica) non si comportano da interscambio di periferia: Stura è piena di giorno (90%) ma anche di notte (79%), Sofia è residenziale, Caio Mario è quasi vuoto (1,5%, forse contatore fermo), Venchi Unica dato quasi fisso.

## Dove si vede
- **Mappa** (`mappa_torino.html#tema=interscambio`, tema «Parcheggi per lasciare l'auto», 3 viste): «Dove ci sono parcheggi?» (riempimento), «In quali aree mancano parcheggi?» (esagoni rosso/arancione/verde), «Dove servirebbe di più un parcheggio?» (20 punti numerati).
- **Scheda** (`simulazione.html`, Risultato 6): domanda, risposta in 4 frasi, 13 grafici (aree, fermate e parcheggi, 20 punti, profili medi e 6 profili singoli, parcheggi pieni, riferimento per direzione), tabella «I criteri, uno per uno» con sensibilità, sezione «Quanto sono affidabili i dati», metodo, limiti. Gli screenshot (`immagini/r6_torino.png`, `immagini/r6_zoom.png`) li fa Leo.
- Colori: bene/male verde→rosso, quantità neutre blu→arancione, categorie colore proprio; una sola scala per vista.

## Limiti
Riempimento su 2 giorni feriali [DATI SCARSI] e solo per i garage del 5T (Fermi e molti altri non trasmettono); posti stimati ±30% (85% dei parcheggi); OpenStreetMap incompleto; distanze in linea d'aria; indagine IMQ campionaria; i risultati dipendono molto dalla distanza di 200 m; eventi (stadi, palazzetti: Olimpico, Inalpi Arena, Oval) rimandati a un tema a parte (`data/ref/eventi_luoghi.json`).

## File
Script 68-79 (luoghi, parcheggi, riempimento, nodi, segnali, ISTAT 2011, strade 77, eventi 78, dati mappa 79), **80** (aree, 20 punti, direzioni, criteri). Dati in `data/processed/risultato6_v2/` (`porte.json`, `mappa_r6.json`). Rapporti `docs/RAPPORTO_R6V2_*`, `RAPPORTO_R6_PORTE.txt`. Piani e esiti dei passi: `PIANO_RISULTATO6_V2.md`, `…_GIRO2.md`, `PIANO_R6_PORTE/DIREZIONI/ZONE/MIGLIORIE.md` e relativi `ESITO_*`.

## Da sistemare / prossimi passi
Correzioni tecniche in `docs/archivio/r6/PIANO_R6_CORREZIONI.md` (errore `r6Data`, legenda, etichette ripetute, descrizioni dei profili…). Dopo il fetch di domenica 25/10 (≥ 5 feriali): rifare 71→72→73→75→76→80→79 e rigenerare mappa e scheda. Screenshot di Leo. Tema eventi separato (più avanti).

---

# STORIA (non descrive più lo stato attuale)

Deciso con Leo il 14/10/2026.

**Stato (14/10 sera)**: passi 0-5 fatti (versione 1, rapporto in `docs/archivio/r6/RAPPORTO_RISULTATO6.txt`).
Da fare a inizio novembre: punto 0.4 (riempimento parcheggi [MISURATO]) e passo 6 (mappa, `simulazione.html`).

## Domanda

I 4 parcheggi di interscambio esistenti (Stura, Caio Mario, Sofia, Venchi Unica) sono a due
passi dalle fermate più critiche per chi arriva in auto dalla cintura? Quali fermate critiche
restano senza parcheggio?

Non si propongono parcheggi nuovi: solo copertura di quelli esistenti.

## Regole decise

| Regola | Valore | Chi l'ha decisa |
|---|---|---|
| Punteggio di criticità | media dei 3 percentili: corridoio (script 24), corse/ora di punta (GTFS), pendolari Torino↔cintura (IMQ) | già concordato |
| Fermata critica | 10% più alto del punteggio (percentile 90) | già concordato |
| Centro escluso | le fermate del centro non contano (un interscambio serve all'ingresso in città, non in centro) | Leo, 14/10 (scelta A) |
| Copertura | fermata coperta se un parcheggio è **entro 200 m a piedi**. Oltre, non ha senso lasciare l'auto lì | Leo, 14/10 |

Valori predefiniti (cambiabili da riga di comando):
- **Centro** = zona IMQ `Q001 Torino-Centro`. Opzione `--escludi-zone Q001` (si possono aggiungerne altre).
- **200 m a piedi** = distanza in linea d'aria fra fermata e ingresso del parcheggio (coordinate
  del dataset comunale). Opzione `--raggio-copertura-m 200`. A 200 m la differenza fra linea
  d'aria e percorso a piedi è piccola; lo dichiariamo come limite.

Effetto atteso, da sapere prima: con soli 4 parcheggi e 200 m, le fermate coperte saranno
pochissime (solo quelle attaccate ai 4 parcheggi). È normale: il risultato utile è la
**classifica delle fermate critiche scoperte**.

## Passi (uno alla volta, ognuno chiuso prima del successivo)

### Passo 0 — Elenco dei parcheggi (aggiunto 14/10)
1. Fonte principale: `get_pk` di 5T (41 parcheggi in struttura con lat/lon, posti totali e
   posti liberi ogni 5', raccolti su leopi da metà ottobre). Copre anche **Fermi** (Collegno),
   che il file del Comune non ha.
2. Il file del Comune (`parcheggi_accesso_controllato`) serve solo per sapere quali sono
   ufficialmente di interscambio.
3. Etichette: "interscambio ufficiale" e "garage in struttura" tenuti separati.
4. Quando ci sono alcune settimane di raccolta: quanto si riempie ogni parcheggio per ora e
   giorno [MISURATO] — da aggiungere al rapporto.

### Passo 1 — Sistemare "Strada Torino" e simili (script 24)
1. Problema: lo script 24 unisce le vie per nome, quindi strade diverse in comuni diversi con lo
   stesso nome diventano un corridoio solo ("Strada Torino" = 100 km, punteggio 5).
2. Modifica (fatta): il corridoio diventa **stesso nome + tratti collegati o vicini (~100-200 m)**,
   così carreggiate e controviali restano insieme e le vie omonime lontane si separano; il comune
   è aggiunto al nome solo come etichetta.
3. Rilanciare `python scripts\24_importanza_vie.py`.
4. Controllo in `docs/RAPPORTO_IMPORTANZA_VIE.txt`:
   - nessun corridoio cittadino o di cintura sopra ~30 km, a parte autostrade e tangenziali;
   - "Strada Torino" spezzata per comune, ogni pezzo con punteggio proprio.

### Passo 2 — Escludere il centro (script 25)
1. Aggiungere l'opzione `--escludi-zone` (default `Q001`).
2. Le fermate di quelle zone restano nel calcolo dei percentili ma non possono essere "critiche".
   (Default dichiarato: così i punteggi delle altre fermate non cambiano per l'esclusione.)
3. Controllo: nessuna fermata critica con `zona_imq = Q001` nel rapporto.

### Passo 3 — Nuova regola di copertura (script 25)
1. Sostituire "stesso corridoio entro 3 km" con "parcheggio entro 200 m in linea d'aria".
2. Opzione `--raggio-copertura-m` (default 200). Togliere `--soglia-copertura-km`.
3. L'assegnazione dei parcheggi a un corridoio non serve più per la copertura: resta solo come
   informazione nel rapporto.
4. Nel rapporto, per ogni parcheggio: quante fermate (critiche e non) ha entro 200 m.

### Passo 4 — Giro di prova e verifica
1. `python scripts\25_risultato6_interscambio.py --prova`
2. Controlli indipendenti (non fidarsi del rapporto da solo):
   - ricalcolare a mano, per ognuno dei 4 parcheggi, le fermate entro 200 m e confrontarle col rapporto;
   - la fermata `1103 CAIO MARIO` deve risultare vicina al parcheggio Caio Mario (o spiegare perché no);
   - nessuna fermata critica in Q001;
   - numeri sensati: critiche ≈ 10% delle fermate analizzate, coperte ≤ critiche, nessun valore negativo.
3. Mostrare a Leo il riepilogo: critiche, coperte, scoperte, prime 10 scoperte più gravi.
4. **Il giro completo parte solo con il via libera di Leo.**

### Passo 5 — Giro completo
1. `python scripts\25_risultato6_interscambio.py`
2. Stessi controlli del passo 4 su tutte le fermate.
3. Riepilogo a Leo con i 3 numeri:
   - quante fermate critiche (fuori dal centro);
   - quante coperte da un parcheggio entro 200 m;
   - le scoperte più gravi (nome, zona, punteggio).

### Passo 6 — Presentazione
1. Mappa: nuovo livello con i 4 parcheggi, cerchio di 200 m attorno, fermate critiche colorate
   coperte/scoperte. Verifica nel browser come da standard (sez. 9 della memoria).
2. Pagina in `simulazione.html` con mappa, numeri e limiti.
3. Aggiornare `MEMORIA_PROGETTO.md`.

## Limiti da dichiarare
- Occupazione dei parcheggi: solo dalla data di avvio della raccolta 5T (metà ottobre 2026); Fermi e Unione Sovietica a volte non trasmettono.
- Pendolari stimati per zona IMQ, non per fermata [STIMATO].
- Importanza delle vie da OSM + 5T + elenco a mano; in cintura OSM è meno completo.
- 200 m in linea d'aria, non percorso a piedi reale.
- Corse/ora da orario programmato [PROGRAMMATO], non misurate.

---

# Versione 2 — proposta discussa con Leo il 18/10/2026 (da approvare passo per passo)

## Decisioni di Leo (18/10)

- **Si resta sulle fermate** come unità (niente "porte d'ingresso" al loro posto), ma si dichiara che le
  fermate vicine (due lati della via, più paline nello stesso punto) sono **un solo luogo**.
- Le fermate critiche di oggi vicino ad autostrade e statali (Paradiso, Massaua, Lingotto, Moncalieri…) sono
  sensate: lì, se ci sono tanti mezzi, si dovrebbe poter lasciare l'auto.
- **Niente interfaccia dinamica per ora**: né nella mappa né nella scheda. Se servirà, al massimo **3
  scenari** fissi nella scheda, senza che la scheda ripeta la mappa.
- **Anteprima del riempimento** dei parcheggi dopo il fetch del 19/10.
- **ISTAT 2011**: solo per ciò che cambia poco nel tempo e per completare dati e calcoli esistenti (sotto, da
  confermare cosa vuol dire).
- **Tutti i parcheggi**, ognuno con la sua precisazione sul tipo e sui dati disponibili.

## A. Nuova misura: quanto un parcheggio fa davvero da interscambio

Per ogni parcheggio, tre domande:
1. **Posizione** — è a pochi passi da un nodo di trasporto forte (metro, capolinea, stazione, fermata con
   molte corse nelle ore dei pendolari)? È su una strada d'ingresso, tra la porta della città e il centro?
2. **Uso** (solo dove c'è il riempimento 5T) — la "firma" oraria:
   - *pendolare*: si riempie al mattino feriale (7-9), resta pieno in orario di lavoro, si svuota la sera,
     vuoto di notte e nel weekend;
   - *residenziale*: più pieno di notte che di giorno (es. Sofia: 55% di notte, 32% di giorno);
   - *destinazione*: picco nel pomeriggio o il sabato (centro, ospedali, centri commerciali);
   - *dato bloccato*: variazione giornaliera quasi nulla (es. Venchi Unica fermo al 51%);
   - *nessun dato*: Fermi, Racconigi, Unione Sovietica, V Padiglione non trasmettono mai i posti liberi.
3. **Condizioni** — capienza, a pagamento o gratis (tag OSM `fee`).

Classi finali: **interscambio di fatto** (posizione buona + firma pendolare) · **interscambio solo sulla
carta** (segnato dal Comune ma usato in altro modo, o vuoto) · **potenziale** (posizione buona, nessun dato
d'uso) · **non interscambio**. Si applica a tutti i 41 parcheggi 5T, non solo ai 5 ufficiali (un garage come
Bolzano, vicino a Porta Susa, potrebbe fare da interscambio di fatto).

Primi indizi (3 feriali, 14-16/10): Stura pieno (~90% di giorno, 80% di notte); Caio Mario quasi vuoto (1-2%
sempre: vuoto davvero o contatore guasto?); Sofia residenziale; Venchi Unica bloccato; Porta Susa FS con un
ciclo pulito (36% di notte, 88% di giorno). A Fermi, entro 500 m, OSM ha ~85.000 m² di parcheggi aperti quasi
tutti **gratuiti** (uno sotterraneo da ~30.000 m² a 180 m), mentre il park&ride ufficiale è a pagamento: conferma
l'idea di Leo che i parcheggi gratuiti vicino ai capolinea siano quelli davvero usati (e non misurati). Lo stesso
a Caio Mario: ufficiale a pagamento e vuoto, uno gratuito da ~5.000 m² a 170 m.

## B. Parcheggi: tutti, con la loro precisazione

| Tipo | Quanti | Dati | Precisazione |
|---|---|---|---|
| Interscambio ufficiali (Comune + Fermi) | 5 | posti; riempimento tranne Fermi | |
| Garage 5T | 36 | posti e riempimento (3 senza dati) | |
| OSM park&ride | 25 | posti solo per alcuni | molti senza nome, in cintura vicino a stazioni |
| OSM a raso / multipiano / sotterranei | ~2.500 | posti dichiarati su pochi | posti stimati dalla superficie (~25 m² a posto, compresi i corselli) [STIMATO] |
| OSM lungo strada | ~1.000 | quasi mai i posti | esclusi dal conteggio dei posti, solo informazione |
| Privati / solo clienti | ~360 + clienti | — | esclusi (clienti: segnalati a parte, es. centri commerciali) |

## C. Fermate critiche: cosa cambia

- **Luoghi**: le fermate entro 40 m sono un solo luogo (stesso criterio della Fase 5 del traffico). Oggi:
  611 fermate critiche = **469 luoghi** (379 se si unisce entro 80 m); coperte 17 fermate = 13 luoghi.
- **(a) Importanza della via** — oggi (script 24) è per *corridoio con lo stesso nome*: punteggio 1-5 = il più
  alto fra classe OSM, elenco a mano di Leo (minimo 4) e sensore 5T con flusso alto (minimo 3). Proposta: dopo
  il lavoro sulle strade, usare gli **assi della Fase 5** (un corso che cambia nome resta uno solo) con la loro
  classe, un segno "**asse d'ingresso**" (attraversa il confine di Torino) e il traffico stimato **solo come
  ordine** (la stima è debole).
- **(b) Corse** — oggi: corse nell'ora di punta alla fermata. Proposta: **media nelle ore dei pendolari**
  (6-10 e 16-20, feriale) come misura principale; punta e intera giornata come prove di sensibilità.
- **(c) Pendolari** — invariato (somma delle due direzioni, tutti i mezzi, giornata intera, valore uguale per
  tutta la zona IMQ), dichiarato così. Variante più precisa al passo D2.
- **Distanza**: 200 m restano la base; nel rapporto anche 100 e 400 m. Più avanti: distanza a piedi sulle
  strade invece che in linea d'aria.

## D. Dati non ancora usati, a passi

1. **Anteprima riempimento** (dopo il fetch del 19/10): firma oraria e classi del punto A.
2. **IMQ nelle ore critiche**: i microdati (`data/processed/imq/spostamenti.csv`) hanno zona e ora di
   partenza, zona di arrivo e mezzi in sequenza. Uso: (c) diventa "auto che entrano a Torino al mattino
   (6-10) dalla cintura", per zona. Quanto apporta lo si misura: quanti luoghi cambiano classe rispetto a oggi.
   Bonus: si vede chi **fa già** auto → mezzo pubblico: ~24.500 spostamenti al giorno (299 interviste), 63% verso
   il treno, ~4.000 verso la metro; la zona del cambio manca nel 60% dei casi e per singola zona le interviste
   sono poche (Collegno 19) → solo numeri d'insieme [DATI SCARSI].
3. **ZTL** (centrale lun-ven 7:30-10:30): pesare di più chi va verso il centro nelle ore della ZTL, perché deve
   lasciare l'auto prima. Si fa insieme al passo 2.
4. **Velocità 5T**: per evitare l'effetto di limiti e semafori, non la velocità assoluta ma il **calo** di
   ciascun sensore fra notte e punta (stesso punto, stessi limiti). Solo dove c'è un sensore (pochi, sugli
   ingressi).
5. **ISTAT 2011 per sezione** (mezzo e ora): solo per le cose che cambiano poco (proposta da confermare):
   *quota di chi va in auto* per sezione e *distribuzione degli orari di partenza*, usate come proporzioni per
   ripartire i totali IMQ 2022 dalle zone alle sezioni; mai numeri assoluti del 2011.
6. **Più avanti, mobilità d'insieme**: bici e bike sharing, car sharing, taxi, stazioni dei treni (da OSM:
   il GTFS GTT non ha i treni).

## Decisioni successive (18/10)

- Definizione ISTAT 2011 del punto D5: **confermata** da Leo.
- **I segnali della versione 1 restano** (importanza della via, corse, pendolari): i nuovi si aggiungono o, se
  sono la loro versione migliorata, li sostituiscono; si confrontano in 3 scenari e decide Leo.
- Piano meccanico per un agente: **`docs/archivio/r6/PIANO_RISULTATO6_V2.md`** (script 68, 69, 71-76).
- Ancora aperto: le soglie della firma oraria si fissano dopo aver visto l'anteprima.

## Giro dell'agente del 19/10 (piano `PIANO_RISULTATO6_V2.md`) — esito ricontrollato da Claude

Esito: `docs/archivio/r6/ESITO_RISULTATO6_V2.md`, rapporti `docs/RAPPORTO_R6V2_*.txt` e `docs/RAPPORTO_RISULTATO6_V2.txt`, dati in
`data/processed/risultato6_v2/`, script 68, 69, 71-76. Tutti i passi OK.

**Numeri confermati da Claude** (ricalcolati a parte): v1 rifatta fermata per fermata = 611 / 17 / 594; scenari S1 438,
S2 436, S3 438 luoghi critici (S1∩S2 370); c2 = 95.297 spostamenti in auto in entrata al mattino (1.139 interviste);
auto → mezzo pubblico ~24.500/giorno (299 interviste). Luoghi: 5.087 (le 611 fermate critiche v1 = 462 luoghi).
Parcheggi censiti 5.205 (5T 40, Comune 39, OSM 5.176). Anteprima riempimento: solo 2 feriali validi (15-16/10).

**Problemi trovati da Claude (da correggere prima di scegliere lo scenario):**
1. **a2 e "asse d'ingresso" prendono il tratto più vicino, anche se è una stradina di servizio** (regola del piano,
   errore di Claude). Esempio: la fermata Genova N.212 (Moncalieri) prende un tratto di servizio a 2 m (punteggio 1)
   invece di Strada Genova a 6 m (punteggio 4). Per lo stesso motivo **nessun parcheggio risulta su un asse
   d'ingresso**, neanche Fermi e Venchi Unica su Corso Francia. In più alcune tratte importanti hanno punteggio 1
   (Via Torino a Venaria, secondaria): da controllare il punteggio delle tratte della Fase 5. a2 è il segnale che
   pesa di più in S2 (toglierlo cambia 148 luoghi), quindi va sistemato prima di confrontare gli scenari.
   Correzione proposta: entro ~30-50 m prendere il tratto di classe più alta, escludendo service/residential.
2. **"Interscambio di fatto" troppo largo**: la firma "pendolare" non distingue chi lascia l'auto per prendere un
   mezzo da chi la lascia vicino al posto di lavoro (risultano interscambio di fatto Molinette, Palagiustizia,
   Nizza, CTO), e "posizione buona" (nodo forte entro 400 m, fuori Q001) vale per quasi tutta la città (346 nodi
   forti). Serve una condizione in più (es. nodo metro/treno/capolinea, oppure fuori dalla zona semicentrale, oppure
   su un asse d'ingresso una volta corretto il punto 1).
3. **Fermate di tutto il Piemonte**: luoghi e percentili includono le fermate GTT extraurbane fuori dalla Città
   metropolitana (Mondovì, Fossano…), come già la v1. Decidere se limitare l'universo (es. Torino + cintura).
4. **La v1 sbagliava "l'ora di punta"**: b1 prendeva l'ora con più corse anche di notte (es. Pozzo Strada: 9 corse
   "in punta" ma solo corse notturne; b2 = 0 è giusto). Argomento per sostituire b1 con b2.
Altri limiti: soglie delle firme provvisorie (Venchi Unica ampiezza 0,055 → "misto" invece di "bloccato"); la ZTL
centrale copre solo la zona Q001 (c2_ztl cambia 20 luoghi); il calo di velocità esiste solo vicino a 96 luoghi (pesa
poco); la quota auto ISTAT 2011 è più bassa di quella IMQ del mattino (universi diversi), usata per 54 zone.
