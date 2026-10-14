# Piano Risultato 6 — Parcheggi di interscambio

Deciso con Leo il 14/10/2026.

**Stato (14/10 sera)**: passi 0-5 fatti (versione 1, rapporto in `docs/RAPPORTO_RISULTATO6.txt`).
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
