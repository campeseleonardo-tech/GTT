# Rapporto GT14-verifica-passaggi

Verificato che «Prossimi passaggi» (aggiunto da GT12) nella scheda della fermata funzioni davvero, e corretti solo i
bug reali. Ho lavorato solo sul codice: **non ho eseguito nulla, non ho aperto la pagina e non ho potuto leggere
`data/processed/orari_fermate.js`** (4,3 MB, non forniti): i controlli automatici sono del runner, la prova visiva è di Leo.
Unico file toccato: `scripts/mappa_template.html` (1 blocco EDIT, marcato `// [agente GT14]`).

## Punti richiesti dalla verifica
1. **Tag script con ripiego** — ok, nessun cambiamento: `data/processed/orari_fermate.js` si carica con `onerror="window.ORARI=null"` prima dello script della mappa. Se il file manca o è rotto, la scheda funziona senza la sezione passaggi e senza errore (guarda su `window.ORARI`).
2. **Tipo di giorno** — ok: all'avvio (e col tasto «Adesso») la pagina prende il giorno reale in fuso Europe/Rome (con ripiego sul fuso del PC): lun-ven→Feriale, sab→Sabato, dom→Domenica, e lo stesso indice (0/1/2) è usato sugli orari. L'ordine fer/sab/dom nel file orari è da confermare (punto "Da verificare" qui sotto), ma è molto probabile: è l'ordine che usa il resto della pagina (`TIPI_GIORNO`).
3. **Prossimi 4 passaggi per linea dall'ora** — ok: solo gli orari ≥ all'ora corrente, massimo 4 per linea.
4. **Prima corsa del giorno dopo** — ok: se ne restano meno di 4, si aggiunge la prima corsa del giorno dopo, marcat... 
   (aggiustato: no più duplicati se la linea ha corse "oltre la mezzanotte", vedi bug 4).
5. **Formato HH:MM + minuti da ora** — c'era un bug piccolo: con l'orologio in moto i minuti uscivano con i decimali (es. `59,38'`). Corretto (v. bug 2).
6. **Etichetta «Orario programmato (non è il tempo reale)»** — presente, testo identico; c'era un bug (usciva anche da sola, senza nessuna linea): corretto (v. bug 3).
7. **Niente mostrato e nessun errore se il dato manca** — ok: ORARI assente/null, fermata non nel file o linea senza orari → niente sezione, niente errore.
8. **Lavoro solo al clic** — c'era un bug: il calcolo (ricerca nome→id per ogni linea e formattazione) partiva anche al semplice passaggio del mouse. Corretto (v. bug 1).

## Bug trovati e corretti (nessun altro punto toccato)
1. **Calcolo anche in hover**: i passaggi venivano elaborati ad ogni mouse-mouse sopra la fermata. Ora solo al click.
2. **Minuti decimali**: `Math.round` sui "minuti da ora" (con il play l'ora era frazionaria).
3. **Etichetta orfanella**: la riga «Orario programmato…» veniva aggiunta anche se nessuna linea era leggibile. Ora appare solo con almeno una linea.
4. **Metà dei passaggi mancanti sulle linee a due direzioni**: una linea GTT ha due id di rotta (andata/ritorno) e GT12 si fermava al primo id trovato col nome — se il file orari è a id (caso più probabile), su molte fermate comparivano solo le corse di una direzione. Ora unisco le voci di entrambi i nomi.
5. Rafforzcini: se il file orari fosse a nome linea invece che a id, il codice lo legge ugualmente; ultimo nome oltre i 14 con "…" ritrovato; anti-duplicazione sulla corsa del giorno dopo.

## Da verificare (non lo posso sapere da qui — segnalo, non invento)
- **Struttura interna di `orari_fermate.js`**: chiavi a id di rotta (duplicato per direzione) oppure a nome linea. Il codice ora va bene nei due casi; la prova di Leo (punto 6) lo conferma.
- **Ordine fer/sab/dom** delle liste giornaliere: probabile, ma non dimostrabile solo col codice: la prova col tasto «Sabato» lo mostra.
- **Linee notturne "oltre la mezzanotte"** (orari tipo 25:30): ora vanno marcate come «(domani)»; se mai le si vede, da oc-

## Scelte (default ragionevoli, reversibili — dettagli in DOMANDE.md)
- I passaggi partono dall'ora e dal tipo di giorno **scelti** in alto (per default: l'ora reale col tasto «Adesso»), così si possono provare orari di un'altra ora o di sabato. Se li vuoi sempre quelli veri attuali, dimmelo.
- Tenuta la scelta di GT12: 4 passaggi + 1 di domani se serve.
- Tag `<script>`, `04_genera_mappa.py` e tutti gli altri file: invariati.

## Come provarlo
1. Da `GTT\scripts` lancia: `python 04_genera_mappa.py` (rigenera `mappa_torino.html`).
2. Apri `mappa_torino.html` con Chrome, Edge o Firefox (doppio clic, non da un'anteprima).
3. Premi «Adesso» in alto per mettere l'orologio sull'ora reale. Il tema di partenza «Offerta» ha già i puntini delle fermate.
4. Ingrandisci (botone + o rotella) su una zona con fermate finché compaiono i punti azzurri (zoom 14+).
5. **Clicca** su una fermata: a destra si apre la scheda con nome, linee, «Passaggi alle HH», «Nella giornata (…)» e, in fondo, **Prossimi passaggi:** con la riga in corsico *Orario programmato (non è il tempo reale)*; per ogni linea fino a 4 orari del tipo `12:35 (42')`.
6. Scegli una fermata di **tram o metro** (andata e ritorno): gli orari in lista devono essere in linea con il numero di «Passaggi alle HH» (somma di tutte le linee). **Se sono circa la metà**, rispondi alla domanda 2 di DOMANDE.md.
7. Sposta la levetta dell'ora di un'ora e clicca di nuovo: gli orari e i "minuti da ora" vanno cambiati; verso mezzanotte appare anche un orario «00:xx (domani)». Passa a «Sabato» e «Domenica»: i passaggi devono cambiare di conseguenza.
8. Accendi il play (▶) qualche secondo e clicca una fermata: i "minuti da ora" devono restare numeri interi.
9. **Test del dato mancante**: rinomina per un momento `data\processed\orari_fermate.js` (es. in `orari_fermate.js-pausa`), ricarica la pagina e clicca una fermata: la scheda funziona, senza «Prossimi passaggi» e senza errore o avviso rosso. Rimetti il file col nome giusto.

## Proposta per
