# Esito giro 4 della mappa: peso e «Luoghi della città» (21/10/2026, sessione cloud)

Fatto nel cloud (niente `data/`, Pi, Windows): codice in `scripts/04_genera_mappa.py` e `scripts/mappa_template.html`,
provato sui dati già dentro `mappa_torino.html`. **La `mappa_torino.html` del repo NON è stata rigenerata**: resta quella
di prima (13,5 MB) finché Leo non lancia il 04 sul PC.

## 1. Peso: 13,5 MB → circa 6,1 MB

Misure sui dati veri (estratti da `const DATI`, byte del JSON compatto):

| Voce | Prima | Dopo | Risparmio | Come |
|---|---|---|---|---|
| `acc` (piedi + 24 ore × 5 gruppi) | 4,59 MB | 1,63 MB | **2,96 MB** | testo: per ogni sezione 125 numeri come differenza dall'ora prima, 1 simbolo per i valori piccoli |
| Forme `g` | 2,84 MB | 0,34 MB | **2,50 MB** | vedi sotto |
| `vcomp` | 0,41 MB | 0,09 MB | 0,32 MB | 4 numeri in testo (millesimi); tolti `serv` e `verde`, che il template non legge (1 sezione) |
| `fb` | 0,35 MB | 0,02 MB | 0,33 MB | un intero in base 3 per sezione |
| Nomi dei campi ripetuti 8.300 volte, campo `ab` | ~1,5 MB | 0 | ~1,5 MB | `D.sezioni` a colonne (un elenco per campo); `ab` (abitazioni) non era letto da nessuno e sparisce |
| Fermate (campo `d`, 72 passaggi/ora) | 1,74 MB | 1,23 MB | **0,52 MB** | 72 numeri in testo (1 simbolo l'uno) |
| Indice del catalogo | 0,03 MB | 0,004 MB | 0,03 MB | restano id, nome, tipo, numero (niente licenza, CRS, campi mancanti, anomalie) |
| **Sezioni (totale)** | **9,66 MB** | **2,74 MB** | **6,92 MB** | |
| **File** | **13,54 MB** | **6,08 MB** | **7,46 MB** | file di prova costruito come lo farebbe il 04 |

Dettaglio forme (misurato a passi):
- solo 4 decimali: 2,84 → 2,54 MB (−0,30);
- + Douglas-Peucker 5 m: → 2,33 MB (−0,22). Punti da 149.517 a 136.559 (−9%): le forme delle sezioni sono già
  essenziali, la semplificazione toglie poco. Nessun anello tolto, nessuno sotto i 4 punti (8.959 anelli, tutti ≥ 4);
  distanza massima fra i punti vecchi e la nuova linea 11,6 m (5,5 m del solo arrotondamento + 5 m di semplificazione);
- + scrittura a testo con differenze fra punti: → 0,34 MB (−2,0). **È questo il passo che pesa.** Non era nella
  richiesta: serviva per stare sotto i 7 MB.

`acc`: togliere solo le ore uguali alla precedente (ipotesi provata) darebbe 4,59 → 3,92 MB (le ore uguali sono solo il
21%), troppo poco; la codifica a differenze fa 1,63 MB.

Campi controllati uno per uno nel template, **non tolti** perché usati: tutti quelli delle fermate (`id`, `n`, `la`, `lo`,
`r`, `d`) e degli altri blocchi (OMI, IMQ, linee, R6 restano invariati: 1,7 MB). Tolti: `ab`, `serv`/`verde` di `vcomp`,
campi tecnici del catalogo. Avvisi, corse simulate e pendolari erano già usciti nei giri 1-3.

Cosa cambia nel codice:
- 04: `cod_nn`/`cod_int` (alfabeto di 89 simboli senza `/`, `<`, `\`), `compatta_acc_testo`, `compatta_vcomp`, `compatta_fb`,
  `semplifica_anello`, `compatta_forma`, `compatta_riquadro`, `compatta_fermate`, `compatta_sezioni`, `catalogo_ridotto`,
  agganciate prima di scrivere il file. Se un valore non rientra nel formato (non intero, 3 decimali, gruppo nuovo) il campo
  resta nella forma vecchia e il template lo legge lo stesso.
- Template: blocco `DECODIFICA` (lettori) e proiezione `sez` riscritta per le colonne. **Il centro di ogni sezione si
  calcola dal riquadro delle forme ORIGINALI** (5 decimali, salvato a parte, 0,14 MB): così le fermate entro 400 m e tutti i
  valori derivati restano identici anche se i bordi si spostano di qualche metro.
- Regola da ricordare (messa in memoria): un campo nuovo di sezione va in `COLONNE_SEZ` del 04 **e** nella proiezione `sez`.

## 2. «Luoghi della città»: 6 caselle (PIANO_MAPPA sezione 6)

Al posto di gruppo/tabelle/scheda tecnica ci sono 6 caselle con colore e numero di luoghi, spuntabili insieme. Al clic
(o al passaggio) su un punto: nome e indirizzo, niente licenze, codici o coordinate. Linee e aree (ciclabili, mercati)
mostrano il nome. Il catalogo si carica come prima da `data/catalogo/<gruppo>.js`, solo quando si spunta una casella che
usa quel gruppo; se il file manca la casella scrive «(dati non disponibili)» e la mappa non si rompe.

Abbinamento (id veri letti in `D.catalogo`), **scelte di Claude con valori predefiniti**:

| Casella | Gruppo → dati |
|---|---|
| Scuole e nidi | istruzione → `scuole`, `infanzia_nidi_comunali`, `infanzia_nidi_convenzionati`, `infanzia_nidi_aziendali`, `infanzia_micronidi`, `infanzia_primavera` |
| Ospedali e salute | salute → `ospedali`, `consultori`, `farmacie` |
| Mercati | commercio → `mercati` (aree), `mercati_tematici` |
| Cultura | commercio → `musei`, `biblioteche`, `cinema` |
| Sport | sicurezza_sport → `impianti_sportivi` |
| Mobilità | reti → `ciclabili`, `bike_sharing`, `ricarica_elettrica`, `parcheggi_strutture` |

Esclusi (restano nei dati, non in mappa): università, ludoteche, centri per bambini, baby parking, strutture
socio-assistenziali, locali storici, tutte le attività commerciali (31.271), forze dell'ordine, uffici, car sharing,
Loges, parcheggi disabili e zona blu, ZTL, alberate. Se Leo vuole aggiungerne uno, si cambia la tabella `LUOGHI` nel template.
Spunta all'avvio: solo «Scuole e nidi».

**Attenzione (da decidere):** «Mercati» e «Cultura» stanno nel file `commercio.js`, che contiene anche le 31.271 attività
commerciali: spuntarle carica tutto il file (probabilmente alcuni MB, non misurabile nel cloud). Il codice scarta le
attività subito dopo il caricamento. Se pesa troppo si può far scrivere al 04 un file più piccolo; non l'ho fatto perché
chiedevi di caricare «come oggi».

## 3. Controllo dei valori

`scripts/prove/controllo_valori_giro4.js` (Node; fa leggere gli stessi dati dal lettore del template di oggi e da quello
nuovo e confronta). Risultato:

- **tutte le 8.317 sezioni** (200 di campione, seme fisso, comprese): 1.039.625 valori di accessibilità (5 gruppi × [a
  piedi + 24 ore]) **identici**; campione di 200 × 5 × 25 = 25.000 identici;
- insieme: 1.253.947 confronti, **0 differenze**: dizionario `acc` completo, `vcomp` (occ, ist, aff, anz), `fb`, `r1`,
  13 campi numerici (abitanti, famiglie, ecc.), riquadro/centro uguale a quello delle forme originali, numero di anelli e anelli chiusi ≥ 4 punti,
  passaggi per ora e dati di tutte le 7.036 fermate;
- il controllo è stato provato anche sbagliando di proposito un simbolo: trova le differenze (20 su una sezione).

Dati usati: `scripts/prove/estrai_dati_giro4.py` estrae DATI dal file, `trasforma_dati_giro4.py` applica le funzioni del 04.

## 4. Prova nel browser (Playwright + Chromium, 0 errori JavaScript)

- 12 temi (11 + nessun tema) × schermo largo 1440×900 e stretto 390×844, sia mappa di prima che nuova: **0 errori** JS,
  pannello `#jsoff` mai visibile.
- «Chi abita qui» e «Servizi a portata», prima e dopo, largo e stretto: a occhio **uguali**; differenza media per pixel
  0,4/255, nessun pixel con scarto > 40/255 (solo antialiasing dei bordi spostati di qualche decimo di pixel).
- «Luoghi della città» con 6 file finti nello stesso formato (`data/catalogo/<gruppo>.js`, ids veri): le 6 caselle si
  caricano, legenda con i numeri, tooltip e scheda con nome e indirizzo, area dei mercati e linee delle ciclabili disegnate,
  file mancante gestito; 0 errori a 1440 e a 390 px.

## 5. Da lanciare sul PC (Leo)

1. `python scripts\04_genera_mappa.py`. Atteso: nessun AVVISO nuovo; riga finale «Mappa creata: … (≈ 6,1 MB)» (accettabile
   fra 5,5 e 6,8; se 13 MB il template non è stato letto). Scrive anche `data/catalogo/*.js` come prima.
2. Aprire `mappa_torino.html` e guardare: «Chi abita qui» e «Servizi a portata» come prima; «Luoghi della città» con le 6
   caselle: spuntare ognuna, controllare che il numero e i punti compaiano e che il clic dia nome e indirizzo (per punti
   senza nome ci sarà la categoria). Provare «Mercati» e «Cultura» e annotare quanto tarda (vedi sopra).
3. `python scripts\prova_pagine_r6.py`. Atteso: 0 errori su tutte le pagine (mappa, tutti i temi, schede).
4. Facoltativo (serve Node): il controllo dei valori sta in `scripts/prove/controllo_valori_giro4.js`; serve il JSON dei dati vecchi, che dopo la rigenerazione non c'è più: non è indispensabile.

Non provato (non si può nel cloud): il 04 completo sui dati veri, `prova_pagine_r6.py` su Windows, il catalogo vero.
