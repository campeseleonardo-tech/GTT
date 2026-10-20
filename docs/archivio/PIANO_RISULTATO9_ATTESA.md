# Piano — Risultato 9: attesa promessa contro attesa reale [MISURATO]

> **Stato (20/10/2026): versione 1 fatta il 18/10, scheda in `simulazione.html`** (numeri nella sezione 9).
> Prossimo: rilancio con un mese di dati (metà novembre).

Scritto da Claude il 18/10/2026, da approvare con Leo prima di costruire (sezione 6: decisioni aperte).
Riparte dai dati e dallo script del Risultato 4 (`scripts/27_risultato4_regolarita.py`, `docs/PIANO_RISULTATO4.md`).

## 1. La domanda (in parole semplici)

Alla fermata l'orario promette, per esempio, un bus ogni 8 minuti: chi arriva a caso aspetta in media 4 minuti.
Se però i bus arrivano a coppie (grappolo) e poi lasciano un buco, l'attesa vera è più lunga, anche se il numero
di bus nell'ora è lo stesso. **Quanti minuti in più aspetta, in media, chi prende un bus o tram frequente a Torino?
Su quali linee, fermate e ore va peggio?**

Perché è rilevante: è la misura che usano le grandi aziende di trasporto per la regolarità delle linee frequenti
(Londra la pubblica come "Excess Wait Time"). Traduce il risultato 4 (percentuali di grappoli e buchi) in una cosa
che tutti capiscono: minuti persi alla fermata. Si calcola con dati che solo questo progetto raccoglie (feed GTT
salvato ogni minuto sul Raspberry Pi).

## 2. La formula (una sola, spiegata)

Per una fermata, una linea, un verso e una fascia oraria, con gli intervalli fra un passaggio e il successivo
h1, h2, ..., hn (in minuti):

- **attesa media** di chi arriva a caso = (h1² + h2² + ... + hn²) / (2 × (h1 + h2 + ... + hn))
- **attesa promessa** = la stessa formula con gli intervalli dell'orario ufficiale (GTFS)
- **attesa reale** = la stessa formula con gli intervalli osservati (arrivi stimati dal feed, come nel risultato 4)
- **attesa in più** = attesa reale − attesa promessa

Esempio: bus esattamente ogni 10 minuti → (10²+10²)/(2×20) = 5 minuti. Stessi 2 bus all'ora ma a coppie, con
intervalli 2 e 18 → (4+324)/(2×20) = 8,2 minuti. Stessa offerta, 3,2 minuti in più di attesa.

La formula vale per le linee **frequenti** (chi va alla fermata non guarda l'orario). Per le linee rare conta la
puntualità, che è già nel risultato 4.

## 3. Cosa sappiamo già dei dati (verificato da Claude il 18/10 sul backup del 18/10)

1. **Feed dei ritardi** (`trip_update_gtt`): dal 10/10, una lettura al minuto. Le giornate complete (06-24) sono
   11, 14, 15, 16 e 17/10; il 10, 12, 13 e 18/10 sono parziali (il 18 per un guasto del feed GTT dalle ~09:05).
   La raccolta si ferma ogni notte a mezzanotte locale e riparte verso le 5: la notte non è misurabile.
2. **Il feed copre solo le linee urbane.** Il 15/10: 90 linee con dati, **108 linee mai presenti** (3.540 corse
   al giorno: numeri a 4 cifre, cioè extraurbane, e alcune notturne). Il risultato vale solo per le linee coperte.
3. **Anche sulle linee coperte manca circa 1 corsa su 5.** Il 15/10, su 9.624 corse programmate delle 90 linee:
   80,1% nel feed dei ritardi, 77,1% nelle posizioni GPS (`mezzi_gtt`), 82,2% in almeno uno dei due. Le linee
   frequenti sono coperte meglio (linea 4: 369 su 380; linea 10: 251 su 260), ma per esempio la linea 2 ha 194 su 243.
   **Una corsa che manca può essere saltata davvero oppure non trasmessa: dai dati non si distingue.** Questo è il
   punto più delicato del metodo (sezione 4, punto 3, e decisione D1).
4. L'arrivo "osservato" è l'arrivo **stimato dal feed** nell'ultima lettura entro 10 minuti dal passaggio (regola
   D1-D5 del risultato 4), non un arrivo visto sul posto.

## 4. Metodo proposto (passi, ognuno con un controllo)

**Passo 1 — Linee e fasce.** Linee frequenti = intervallo programmato ≤ 12 minuti (almeno 5 passaggi all'ora) in
quella fascia, fermata e verso (D2). Fasce come nel risultato 4 (punta mattina 7-9, giorno 9-16, punta sera 16-19,
sera 19-24), più tipo di giorno. Solo le ore in cui la raccolta era attiva (almeno 50 minuti letti nell'ora).
*Controllo:* elenco delle linee frequenti con numero di fermate e passaggi programmati; confronto con le linee
frequenti già usate nel risultato 4.

**Passo 2 — Intervalli promessi e osservati.** Per ogni fermata-linea-verso-giorno si mettono in fila le corse
programmate e i loro arrivi stimati (dallo script 27, stessa lettura dei dati). *Controllo:* per 3 fermate
scelte a mano (una della linea 4, una della 15, una della 68) stampare la fila di orari promessi e stimati e rifare a
mano l'attesa promessa e reale.

**Passo 3 — Corse mancanti: una forbice, non un numero solo (D1).**
- *Stima bassa:* una corsa assente nel feed è considerata "non vista": l'intervallo si calcola solo tra corse
  consecutive entrambe osservate (si scartano i pezzi con buchi). Sottostima l'attesa se le corse mancanti erano
  saltate davvero.
- *Stima alta:* una corsa assente sia dal feed dei ritardi sia dal GPS mentre la raccolta era attiva è considerata
  **non effettuata**: l'intervallo reale salta da un bus all'altro. Sovrastima l'attesa se la corsa c'era ma non
  trasmetteva.
- Si pubblicano entrambe, con il numero principale = la stima bassa (prudente) e la forbice accanto.
*Controllo:* quota di corse mancanti per linea e fascia; se una linea ne ha più del 20% in una fascia, quella
fascia va in tabella "dati scarsi" e non entra nei numeri di testa.

**Passo 4 — Prova con il GPS (controllo indipendente del feed).** Su 2 linee frequenti (4 e 15) e circa 20
fermate, confrontare l'arrivo stimato dal feed con il momento in cui il GPS del mezzo (`mezzi_gtt`, posizione ogni
minuto) passa più vicino alla fermata. Se la differenza mediana supera 1 minuto, fermarsi e decidere con Leo.

**Passo 5 — Numeri.** Per linea-verso-fascia-tipo di giorno: attesa promessa, attesa reale (bassa e alta),
attesa in più in minuti e in %, numero di intervalli. Città: media pesata sul numero di passaggi programmati (non
abbiamo i passeggeri; D3). Classifiche: le 10 linee e le 20 fermate con più attesa in più (con almeno 30 intervalli).

**Passo 6 — Scheda in `simulazione.html`** (stesso formato delle altre, `scripts/schede_risultati.py`): numero
chiave, grafico per fascia oraria, classifica delle linee, prima/dopo "attesa promessa → attesa reale".
La mappa per fermate solo se Leo la vuole, dopo.

## 5. Uscite

`scripts/<numero libero>_risultato9_attesa.py` (il numero si sceglie quando l'agente della Fase 5 ha finito, per
non scontrarsi con i suoi 56+), `data/processed/risultato9_attesa.json`, `docs/RAPPORTO_RISULTATO9_ATTESA.txt`,
scheda nella pagina dei risultati. Calcolo leggero (come lo script 27: ~500 MB di memoria, pochi minuti).

## 6. Decisioni aperte (da chiedere a Leo, con il default proposto)

| # | Domanda | Default proposto |
|---|---|---|
| D1 | Corse mancanti | Forbice bassa/alta, numero principale = stima bassa |
| D2 | Cosa vuol dire "frequente" | ≤ 12 minuti di intervallo programmato (sensibilità: 10 e 15) |
| D3 | Peso per la media della città | Passaggi programmati (niente dati sui passeggeri) |
| D4 | Numero del risultato | Risultato 9 |
| D5 | Chi lo esegue | Claude, in questa cartella, dopo l'approvazione del piano |

## 7. Limiti da dichiarare già ora

- Arrivi stimati dal feed GTT, non osservati sul posto (verificati a campione col GPS, passo 4).
- Solo linee urbane presenti nel feed; niente extraurbane, niente notte.
- Corse mancanti: risultato dato come forbice.
- Chi arriva alla fermata "a caso": vero per le linee frequenti, non per chi guarda l'orario o l'app.
- Pochi giorni (vedi sezione 3): il risultato va rifatto quando ci sono più settimane di dati.

## 8. Effetto sul risultato 4 (scoperto preparando questo piano)

Anche il risultato 4 misura solo le corse presenti nel feed: se le corse mancanti sono in parte saltate davvero, la
puntualità reale è peggiore di quella misurata e i "buchi" sono sottostimati (una corsa saltata non crea un buco
nel conteggio, perché la coppia si calcola fra corse osservate). Va scritto fra i limiti del risultato 4.

## 9. Stato al 18/10/2026 (spostato qui dalla memoria)

**Versione 1** [MISURATO], 10-18/10, linee urbane frequenti (≤ 12 min), ore con raccolta attiva.
Feriale: attesa promessa 4,8 min, reale 5,4-6,2 → **0,6-1,5 min in più** (+13% stima bassa); sabato +0,8-1,4;
domenica troppo pochi dati. Peggiori: linea 68 (+1,3-3,0), 3, 56, 46, 62; fermate della 18 (Caio Mario,
Lingotto) e della 62. Controlli: GPS linee 4 e 15 (343 passaggi, scarto tipico 0,45 min, 70% entro 1 min); una
chiave rifatta da zero coincide (2,555 / 3,668 min). Lo script 70 riusa il 27 senza modificarlo. Scheda in
`simulazione.html`. Da rilanciare con più settimane di dati (27, poi 70, poi `schede_risultati.py`).
