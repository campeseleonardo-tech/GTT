# Piano meccanico — Risultato 6 v2 in mappa e in `simulazione.html`, con colori uniformi

Scritto da Claude il 19/10/2026 con Leo, per un altro modello (agente). Sostituisce le Fasi C e D di `PIANO_RISULTATO6_FINALE.md`.
Le decisioni di Leo sono **fisse**. Fai **una fase alla volta, nell'ordine**. Dopo ogni fase scrivi in `docs/ESITO_INTEGRAZIONE_R6.md`
`FASE n: OK` o `FASE n: FERMO – motivo`, poi **FERMATI**: Claude controlla la pagina nel browser (tu non la vedi) e ti dà il via per la fase dopo.
Se un controllo non torna: fermati, scrivi cosa hai visto, non inventare correzioni.

## 0. Regole

1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (`git branch --show-current`; se no, FERMATI). **Nessun commit.** Python del PATH (3.14), non Anaconda. Non installare librerie.
2. Dati in sola lettura. **Non modificare** `mappa_torino.html` a mano (si rigenera), né `simulazione.html` fuori dai punti indicati, né altri script.
   File che puoi modificare: `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`, `simulazione.html` (solo le parti della Fase 4). File nuovi: `docs/ESITO_INTEGRAZIONE_R6.md`, `docs/RAPPORTO_COLORI.txt`.
3. Rigenera la mappa con `python scripts\04_genera_mappa.py` e le schede con `python scripts\schede_risultati.py`. Prima di rigenerare tieni una copia: `copy mappa_torino.html mappa_torino_prima_R6.html` (solo la prima volta; Claude la toglie a fine lavoro).
4. Controllo di sintassi dopo ogni modifica al template: estrai il contenuto dei `<script>` di `mappa_torino.html` in un file temporaneo nella cartella `%TEMP%` e lancia `node --check` su di esso (se non c'è `node`, scrivilo). **Non basta**: gli errori di resa li vede Claude nel browser.
5. Standard del progetto: un campo nuovo in `D.sezioni[i]` va anche nella proiezione `sez` (qui non serve); chi cambia l'ora chiama `aggiornaLegenda()`; numeri in italiano (virgola decimale); italiano semplice, niente gergo; etichette dei dati sempre visibili ([MISURATO] [PROGRAMMATO] [STIMATO] [DATI SCARSI]).
6. Commenti nel codice nello stile esistente (`// [R6] …`). Non rinominare o spostare funzioni esistenti.

## 1. Decisioni di Leo (19/10) — fisse

- **Colori**: in tutta la mappa e in tutte le schede **le scale sono due, sempre le stesse**:
  - **Scala «bene/male»**: da **verde (bene) a rosso (male)**, per tutto ciò che ha un giudizio chiaro.
  - **Scala «neutra»** (nessun giudizio: quantità come abitanti, spostamenti, pendolari, prezzi): **blu → arancione, non troppo forti**.
  Le **categorie** (un colore per gruppo, es. catalogo, tipi di linea) non sono gradienti e restano come sono. (Più avanti le quantità neutre potrebbero avere un'altra rappresentazione: non ora.)
- Dettaglio dei colori nella tabella della Fase 1. Ogni legenda continua a **scrivere i numeri delle soglie** e le parole agli estremi (non solo il colore): serve anche a chi non distingue rosso e verde.
- Il link «Apri la mappa» di **ogni scheda** apre la mappa **già sul tema giusto**.
- Gli **screenshot** per la scheda li fa Leo (cartella `immagini/`, vedi Fase 4); se mancano, la sezione non appare.
- Scenario **S2**, eventi: Olimpico Grande Torino, Inalpi Arena, Oval (Allianz rimandato).

## 2. Dati disponibili (tutti già prodotti e ricontrollati)

`data/processed/risultato6_v2/mappa_r6.json` (529 KB), chiavi: `scenario`, `luoghi_critici` (378: `id, nome, lat, lon, zona_imq, n_fermate, punteggio, segnali, parcheggio_f{id,nome,dist_m}, parcheggio_u{…}, coperto_f200, coperto_u200, coperto_p200`),
`parcheggi` (813: `id, nome, tipo, classe, motivo, lat, lon, zona_imq, zona_centrale, posti, posti_origine, a_pagamento, forza, punti_a_favore, su_asse_ingresso, firma, profilo_feriale[24], fragile`),
`ufficiali` (5), `zona_centrale{zone_centrali, poligoni[{cod, denom, anelli}]}` (anelli `[lat, lon]`), `eventi` (3: `id, nome, tipo, lat, lon, capienza, auto_stimate, posti_500, posti_1000, mancano, fermate_500, corse_ora_sera_*`),
`riepilogo` (`copertura_per_raggio`, `parcheggi_per_classe`, `parcheggi_per_motivo`, `firme_riempimento`, `giorni_feriali_validi`, `zone_scoperte_top10`, `piu_scoperti_top10`, `solo_sulla_carta`, …), `etichette`, `fonti`.
Numeri da ritrovare: critici 378; coperti a 200 m: F (di fatto+potenziali) 140, U (ufficiali) 11, F+S 144 (P = tutti i parcheggi ≥ 50 posti: 147, solo in scheda); classi parcheggi: di fatto 0, solo sulla carta 4, potenziale 758.

---

## FASE 1 — Due scale di colore in tutta la mappa (`scripts/mappa_template.html`)

**1.1 Nuove costanti** (mettile al posto delle vecchie, vicino a riga ~609-619, e cambia i commenti «arancio→viola»):

```js
const PAL_VR   = ["#1a9850","#91cf60","#fee08b","#fc8d59","#d73027"];  // verde (bene) -> rosso (male)
const PAL_RV   = [...PAL_VR].reverse();                                  // rosso (male) -> verde (bene)
const PAL_NEU  = ["#6a98c4","#b4cbe0","#ece9e2","#f1c58f","#e08a38"];  // neutra: blu (poco) -> arancione (tanto), colori smorzati
```

**1.2 Tabella delle sostituzioni** (cerca ogni nome con `grep -n` e cambia **solo** quello; controlla che l'ordine «indice 0 = valore più basso» sia rispettato):

| Dove | Oggi | Nuovo | Significato |
|---|---|---|---|
| `PAL_POCO_MALE` (≈610) | arancio→viola, basso = male | **`PAL_RV`** (indice 0 = rosso) | valore basso = peggio (offerta, accessibilità) |
| `PAL_ALTO_MALE` (≈611) | inverso | **`PAL_VR`** (indice 0 = verde) | valore alto = peggio (vulnerabilità) |
| `PAL_RAPP` (≈612) | = POCO_MALE | `PAL_RV` | offerta rispetto agli abitanti |
| `PAL_BASE` (≈613) | verde acqua | **`PAL_NEU`** | quantità neutre |
| `PAL_PEND` (≈614) | viola | **`PAL_NEU`** | pendolari (neutro) |
| `PAL_SEZ` (≈615) | `dens, occ, sc, sen` → BASE | `PAL_NEU` | abitanti, occupati, bambini, anziani: neutri |
| `PAL_SEZ.serv` | BASE | **`PAL_RV`** | «solo offerta»: più passaggi = meglio |
| `PAL_SEZ.acc` (≈618) | `PAL_POCO_MALE` | `PAL_RV` | più servizi raggiungibili = meglio; aggiorna il commento |
| `PAL_SEZ.fb` (≈619) | `["#ecebf2","#f1a340","#b35806"]` | `["#e3f0df","#fc8d59","#d73027"]` | 0 = ok (verde chiarissimo), 1 = pochissimo, 2 = zero |
| `OMI_PAL` (≈284) | giallo→arancio | **`PAL_NEU`** | prezzi (neutro) |
| `IMQ_PAL` (≈302) | azzurri | **`PAL_NEU`** | spostamenti IMQ (neutro) |
| `VEL_PAL` (≈1062) | 4 colori arancio→viola | `["#d73027","#fc8d59","#91cf60","#1a9850"]` | indice 0 = lento (rosso) … 3 = veloce (verde) |
| testo riga ≈1815 | «Arancio = poca offerta.» | «Rosso = poca offerta.» | |

Dopo le sostituzioni cerca tutte le altre occorrenze di quei nomi e dei vecchi esadecimali (`#b35806 #f1a340 #fee0b6 #b2abd2 #542788 #998ec3 #fff7bc #fee391 #fec44f #fe9929 #cc4c02 #dbe9f6 #a9cbe8 #6fa8d0 #3a7cb5 #123f6d #e3f1ef #b5dcd6 #7cc0b8 #3f9a95 #1b6f73 #efe9f6 #cdb9e3 #a98acd #7d55b0 #51287f`)
in `mappa_template.html` **e** in `04_genera_mappa.py`: devono sparire tutte, salvo nella frase «arancio…» di commenti vecchi (aggiornali). Scrivi in `docs/RAPPORTO_COLORI.txt` l'elenco di ogni sostituzione (riga, vecchio → nuovo) e di ogni colore categorico lasciato (catalogo, `COL.*` delle linee, sfondi).
**Sensori di traffico** (≈1055): usano `VEL_PAL` (velocità media) → ok. Le **linee delle corse/mezzi** sono categoriche (tipo di mezzo): non toccarle.

**1.3 Legende**: le funzioni `scalaSoglie` e `scalaHtml` usano le palette passate: non vanno toccate. Controlla (leggendo il codice) che le parole agli estremi siano coerenti col nuovo verso:
- `rapp`/`acc`/`serv`: sinistra = rosso = «poca offerta / pochi / meno», destra = verde. ✔ (indice 0 è a sinistra);
- `vuln*`: sinistra = verde = «meno vulnerabile», destra = rosso ✔;
- `dens/occ/sc/sen/pend/omi/imq`: sinistra = blu = «meno», destra = arancione = «più» ✔;
- `fb`: legenda a puntini (≈564): aggiorna le tre tinte e i testi se citano colori;
- velocità: le classi `&lt;12 / 12–16 / 16–… ` vanno già dal più lento al più veloce ✔.
Se una legenda cita un nome di colore a parole, cambialo (cerca «arancio», «viola», «azzurr», «verde acqua»).

**1.4 Guida** (`<details id="infoDati">` ≈205): aggiungi un paragrafo «Colori: verde = bene, rosso = male; blu→arancione = poco→tanto, senza giudizio. Le legende scrivono sempre i numeri.»

**1.5 Rigenera** `mappa_torino.html`, `node --check`, scrivi `RAPPORTO_COLORI.txt` ed esito. **FERMATI**: Claude apre ogni tema (servizio, accessibilità, dove mancano, vulnerabilità, IMQ, pendolari, bus e traffico misurati, valore immobiliare, catalogo) e controlla aree, legende e tocco; poi ti dà il via.

---

## FASE 2 — Dati del Risultato 6 nella mappa

**2.1 `scripts/04_genera_mappa.py`**: dopo il blocco `fb_candidati` (≈riga 891-898) aggiungi

```python
    r6 = None
    f_r6 = RADICE / "data" / "processed" / "risultato6_v2" / "mappa_r6.json"
    if f_r6.is_file():
        r6 = json.loads(f_r6.read_text(encoding="utf-8"))
        print(f"  risultato6 v2: {len(r6['luoghi_critici'])} luoghi critici, {len(r6['parcheggi'])} parcheggi, {len(r6['eventi'])} eventi")
```
e nel dizionario `dati` (≈riga 957, dopo `"fb_candidati": fb_candidati,`) aggiungi `"r6": r6,`.

**2.2 `mappa_template.html`**, subito dopo il blocco `fbCandidati` (≈riga 701), proietta le coordinate:

```js
// [R6] Risultato 6 v2: parcheggi di interscambio (null se il file dati manca)
const R6 = D.r6 ? (()=>{ const r=D.r6, pj=a=>a.map(o=>({...o,x:px(o.lon),y:py(o.lat)}));
  return { scenario:r.scenario, luoghi:pj(r.luoghi_critici), parcheggi:pj(r.parcheggi), eventi:pj(r.eventi), ufficiali:pj(r.ufficiali),
           centro:(r.zona_centrale.poligoni||[]).map(p=>p.anelli.map(an=>an.map(([la,lo])=>[px(lo),py(la)]))), riepilogo:r.riepilogo, etichette:r.etichette, fonti:r.fonti }; })() : null;
```
(Ordine delle coordinate dei poligoni: `[lat, lon]`.) **Controllo**: nessuna modifica al comportamento dei temi esistenti.

---

## FASE 3 — Tema «Parcheggi di interscambio»

Tutto in `mappa_template.html`. Il tema compare solo se `R6` non è null.

**3.1 Opzioni** — in `OPT_VAL` (≈2012) aggiungi `r6Vista:"tutto", r6Insieme:"F", r6Raggio:"200"`. In `OPZIONI` (≈1990) aggiungi:

```js
  r6Vista:{etichetta:"Cosa vedere", voci:[["tutto","Luoghi critici e parcheggi"],["luoghi","Solo luoghi critici"],["parcheggi","Solo parcheggi"],["eventi","Luoghi di eventi"]]},
  r6Insieme:{etichetta:"Quali parcheggi contano", voci:[["F","Potenziali e di fatto (consigliato)"],["U","Solo i 5 interscambi ufficiali"],["FS","Potenziali + ufficiali poco usati"]]},
  r6Raggio:{etichetta:"Distanza dal parcheggio", voci:[["100","100 m"],["200","200 m"],["400","400 m"]]},
```
Gli handler: `HANDLERS.r6Vista = HANDLERS.r6Insieme = HANDLERS.r6Raggio = ()=>{ baseVer++; chiede(); aggiornaLegenda(); };` (guarda come sono fatti gli altri in `HANDLERS` ≈2013 e copia lo stile).

**3.2 Copertura calcolata al volo**: funzione `r6Coperto(l)` che, per il luogo `l`, dato insieme (F/U/FS/P) e raggio (100/200/400), restituisce vero/falso con la distanza dal parcheggio più vicino dell'insieme.
Insiemi: **F** = classe `interscambio_di_fatto` o `potenziale`; **U** = tipo `interscambio_ufficiale`; **FS** = F più la classe `solo_sulla_carta`. L'insieme P (tutti i parcheggi aperti con almeno 50 posti) **non** è nel file della mappa (ci sono solo 813 parcheggi): resta solo nella scheda, dal `riepilogo`. Distanza haversine in metri sulle coordinate `lat/lon`.
**Controllo obbligatorio** (scrivilo nell'esito, eseguito con `node` o con una pagina di prova): a 200 m i coperti sono **F 140, U 11, FS 144** Se non tornano: FERMO.

**3.3 Disegno** — funzione `disegnaR6(ws,ox,oy)` chiamata da `disegnaBase` subito prima della riga `if(tema.id==="catalogo") …` (≈1007): `if(tema.id==="interscambio" && R6) disegnaR6(ws,ox,oy);`. Ordine di disegno, dal basso:
1. **Zona centrale** Q001-Q009: poligoni `R6.centro` pieni grigio chiaro (`rgba(120,125,135,.18)`) con bordo tratteggiato; etichetta «zona centrale (qui un parcheggio non conta come interscambio)» nella legenda.
2. **Cerchi di copertura**: attorno ai 5 ufficiali e al parcheggio selezionato (se c'è `schedaSel`), raggio in metri convertito in pixel con la funzione dei metri per pixel già presente (cerca `metriPerPixel` / la scala in basso, riga ≈861), colore del bordo come la classe, riempimento al 10%.
3. **Parcheggi** (solo se `r6Vista` ∈ tutto/parcheggi): cerchio, raggio px = `3 + √posti/6` limitato a 3-14; **colore per classe, tavolozza categorica diversa da verde/rosso**: potenziale = turchese `#2a9d9d`, solo sulla carta = viola `#7b5ea7`, di fatto = blu scuro `#1f4e8c`, garage 5T non interscambio = grigio `#8a8f9a`, ufficiali = bordo nero spesso. Contorno **tratteggiato** se `posti_origine==="stimati"`; senza posti = cerchio vuoto. Sotto zoom 12 disegna solo ufficiali, solo sulla carta e i 100 potenziali con più posti.
4. **Luoghi critici** (solo se `r6Vista` ∈ tutto/luoghi): cerchio, raggio px 4-9 in base al punteggio; **verde `#1a9850` se coperto, rosso `#d73027` se scoperto** (secondo `r6Coperto`), bordo bianco 1 px.
5. **Eventi** (solo se `r6Vista` = eventi, o tutto a zoom ≥ 13): stella a 5 punte nera con bordo bianco; anelli tratteggiati a 500 m e 1.000 m.
Usa `AREA_ALPHA`, `AREA_STROKE` e le abitudini delle altre funzioni di disegno (`cx`, `dentroVista`). Niente animazioni.

**3.4 Tocco / passaggio del mouse** — in `cercaTip` (≈1530), dopo il blocco «0bis. Candidati Fase B», aggiungi un blocco «0ter» per `tema.id==="interscambio"` con la funzione `vicino(arr, raggio_px)` esistente, in quest'ordine: eventi (raggio 14 px), parcheggi (10 px), luoghi (9 px). Al passaggio: `mostraTipBase(tipC(nome, valore, extra), sx, sy)`; al clic: `apriScheda(html, null)` con la funzione `creaScheda` (stessa struttura delle altre schede al clic, ≈1163):
- luogo: titolo = nome; valore = «coperto da <parcheggio> a N m» oppure «nessun parcheggio entro N m»; dettagli = zona IMQ, n. fermate, punteggio S2 e 3-4 segnali principali (a2 strada, b2 corse dei pendolari, c1 pendolari), parcheggio più vicino dell'insieme scelto e distanza;
- parcheggio: tipo e classe in parole («interscambio ufficiale», «segnato come interscambio ma usato in altro modo», «potenziale: ben posizionato, nessun dato d'uso», «non interscambio: zona centrale / nessun punto a favore»), posti con [STIMATO] se stimati, tariffa, punti a favore (testo), firma del riempimento con «[DATI SCARSI: 2 giorni feriali]»; se `profilo_feriale` non è nullo, aggiungi una **mini-curva SVG a 24 ore** (viewBox 0 0 240 60, asse 0-24, linea `#1f4e8c`);
- evento: capienza, auto stimate [STIMATO], posti entro 500 m e 1 km, «mancano ~N» (se > 0), fermate entro 500 m, corse all'ora la sera (feriale/sabato/domenica) [PROGRAMMATO], frase «ordini di grandezza, non previsioni».
Testi sempre in italiano semplice.

**3.5 Tema e legenda** — aggiungi in `THEMES` (dopo «faseb», ≈1953), costruendo l'oggetto solo se `R6`:

```js
  ...(R6 ? [{id:"interscambio", label:"Parcheggi di interscambio",
   desc:"Le fermate più importanti per chi arriva in auto: ce n'è una vicino a un parcheggio che potrebbe fare da interscambio? Verde = coperta, rosso = scoperta.",
   area:null, over:{...NESSUNA}, opzioni:["r6Vista","r6Insieme","r6Raggio"], legenda:legendaR6}] : []),
```
`legendaR6()` (stile di `legendaFb`, ≈557): titolo con scenario («Scenario S2: 378 luoghi critici su 4.425»), conteggio **calcolato** dei coperti con insieme e raggio scelti (usa `r6Coperto`), puntini verde/rosso per i luoghi, punti per classe di parcheggio con i posti totali per classe (da `riepilogo.parcheggi_per_classe`), «contorno tratteggiato = posti stimati dalla superficie [STIMATO]», «grigio = zona centrale», stella = evento, avviso `[DATI SCARSI]` con `riepilogo.giorni_feriali_validi`, e la riga «Fonti: orari GTT [PROGRAMMATO], parcheggi 5T/Comune/OpenStreetMap, indagine IMQ 2022 [STIMATO]».

**3.6 Link con il tema** — leggi l'indirizzo all'apertura: sostituisci in fondo (≈2099) `sicuro(()=>applicaTema("servizio"))` con

```js
const temaDaUrl = ()=>{ const m=/[#&?]tema=([a-z0-9_]+)/i.exec(location.hash||""); return m && THEMES.some(t=>t.id===m[1]) ? m[1] : "servizio"; };
… sicuro(()=>applicaTema(temaDaUrl()));
addEventListener("hashchange",()=>applicaTema(temaDaUrl()));
```
(`applicaTema` esiste, ≈2053, e imposta già il menu `#temi`.)

**3.7 Guida**: nella «Guida e fonti dei dati» aggiungi un paragrafo su cosa sono luogo critico, parcheggio potenziale / solo sulla carta / di fatto, scenario S2, eventi, 25 m² a posto (±30%).

**3.8** Rigenera, `node --check`, scrivi l'esito (peso di `mappa_torino.html` prima/dopo) e **FERMATI**: Claude apre il tema (`mappa_torino.html#tema=interscambio`), prova livelli, insiemi e raggi, tocco su un luogo, un parcheggio, un evento, schermo stretto, console, e riguarda 2-3 altri temi.

---

## FASE 4 — `simulazione.html`: colori, nuovi grafici, immagini, link (solo queste parti)

**4.1 Colori** — nel `:root` (≈riga 9) aggiungi `--vr-verde:#1a9850; --vr-giallo:#fee08b; --vr-rosso:#d73027; --neu-blu:#6a98c4; --neu-blu-chiaro:#b4cbe0; --neu-arancio:#e08a38;`.
- `graficoBarre`: la barra usa `v.tono` se c'è: `"verde"`→`var(--vr-verde)`, `"rosso"`→`var(--vr-rosso)`, `"giallo"`, `"blu"`, `"arancio"`; altrimenti **`var(--neu-blu)`** (prima: `--accent`); la barra «prima» resta più chiara (`--neu-blu-chiaro`).
- `PALETTE_PILA` → `["var(--neu-blu)","var(--neu-arancio)","#9aa3b2","#c9b27a","#8d7bb0"]`; in `graficoPila` se la voce ha `tono` usa quello al posto della palette (legenda compresa).
- `TONI` (grafico orario): `pieno:"var(--neu-blu)"`, `medio:"var(--neu-blu-chiaro)"`, `vuoto:"var(--vr-rosso)"` se «vuoto» indica un problema; **controllalo** leggendo come lo usa `scheda_r2`.
- In `schede_risultati.py` assegna `tono` solo dove il significato è chiaro (regola: voci con «senza», «scoperte», «in ritardo», «critiche» → `"rosso"`; «coperte», «serviti», «in orario» → `"verde"`; il resto niente). **Elenca in `ESITO_INTEGRAZIONE_R6.md` tutte le voci a cui hai messo un tono**, una riga ciascuna (scheda, grafico, voce, tono): Claude le rivede.

**4.2 Nuovo grafico `profilo`** (curva a 24 ore) — in `grafico(g)` aggiungi il ramo `g.tipo==="profilo"` → `graficoProfilo(g)`: dati `{tipo:"profilo", titolo, unita:"%", serie:[{label, valori:[24 numeri 0-1 o null], tono, tratteggio}], nota}`. SVG inline `viewBox="0 0 480 170"`, asse x 0-24 con tacche ogni 3 ore (stesso stile di `graficoOrario`), asse y 0-100% con linee guida a 0/50/100, una `polyline` per serie (colori: `--neu-blu`, `--neu-arancio`, `#9aa3b2`, `--vr-rosso`; tratteggiata se `tratteggio`), legenda sotto con le etichette, nota sotto. I `null` interrompono la linea. Aggiungi la classe `largo`.

**4.3 Immagini** — in `apri(i)` aggiungi la sezione «Com'è fatta in mappa» se `s.immagini` è un array non vuoto: `<figure><img src="${file}" alt="${didascalia}" loading="lazy" onerror="this.closest('figure').remove()"><figcaption>${didascalia}</figcaption></figure>` per ogni elemento `{file, didascalia}`; stili: larghezza 100%, bordo e raggio come le altre carte. Se tutte falliscono, la sezione resta vuota e va rimossa (controlla che `sezione()` non mostri un titolo vuoto).

**4.4 Link con il tema** — in `apri()` il bottone «Apri la mappa» usa `mappa_torino.html#tema=${s.mappa.id}` se `s.mappa.id` c'è, altrimenti `mappa_torino.html`.
In `schede_risultati.py` aggiungi il campo `id` dove la scheda ha già `mappa`: R1 `"id": "faseb"` (riga ≈153), R2 `"id": "accessibilita"` (≈244). Le schede con `"mappa": None` restano così.

**4.5** Rilancia `python scripts\schede_risultati.py`, `node --check data\schede_risultati.js`; scrivi l'esito. **FERMATI**: Claude apre tutte le schede e controlla che grafici, colori e link siano a posto.

---

## FASE 5 — Scheda Risultato 6 v2 (`scripts/schede_risultati.py`)

**5.1** Aggiungi `scheda_r6_v2()` **senza cancellare** `scheda_r6`; in `main()` sostituisci `scheda_r6` con `scheda_r6_v2` (resta il nome file `risultato6_riepilogo_mappa.json`). Leggi **solo** `data/processed/risultato6_v2/mappa_r6.json` (campi `scenario`, `riepilogo`, `eventi`, `parcheggi`): nessun calcolo nuovo, solo somme e conteggi.
Numeri con il punto delle migliaia e la virgola decimale (usa `migliaia`, `virgola`, `il`).

**5.2 Contenuto della scheda:**
- `risultato:"6"`, `titolo:"Parcheggi di interscambio"`, `stato:"Versione 2 (19/10/2026)"`, `tag:"STIMATO / PROGRAMMATO / MISURATO (dati scarsi)"`.
- `domanda`: «Chi arriva in auto dalla cintura trova un parcheggio vicino alle fermate più importanti? E i parcheggi che si chiamano di interscambio lo sono davvero?»
- `in_breve`, `racconto`: come nella v1 (Fermi, Collegno) aggiornati con una riga sul nuovo metodo.
- `numero_chiave`: valore = luoghi critici **scoperti** a 200 m dall'insieme F (378 − 140 = **238**), unità «luoghi», testo «su 378 luoghi critici non hanno un parcheggio potenziale o di fatto entro 200 m».
- `risposta` (4 frasi, con i numeri veri del file): 1) critici/coperti F (140) e coperti dagli ufficiali (11); 2) «nessun parcheggio fuori dal centro ha il profilo di chi lascia l'auto per andare al lavoro» (di fatto = 0) e i **4** interscambi del Comune risultano «solo sulla carta» (nomi, firme); 3) 758 parcheggi potenziali con X posti, senza dati d'uso; 4) zone con più scoperti (prime 3 con nome e numero) e una frase sugli eventi (auto stimate e posti mancanti per l'Olimpico, ordine di grandezza).
- `grafici` (nell'ordine; titolo chiaro, `nota` dove serve):
  1. `pila` «Luoghi critici: coperti e scoperti (200 m, parcheggi potenziali e di fatto)» — voci coperti (`tono:"verde"`) e scoperti (`tono:"rosso"`);
  2. `barre` «Quanti luoghi critici sono coperti, per distanza e per insieme di parcheggi» — 3 insiemi × 3 raggi (da `copertura_per_raggio`), senza tono;
  3. `barre` «Parcheggi per classe» con voci «(N parcheggi, M posti)» e come valore i **posti** (di fatto / solo sulla carta / potenziali / non interscambio);
  4. `barre` «Perché un parcheggio non è considerato interscambio» (`parcheggi_per_motivo`);
  5. `barre` «Quartieri e comuni con più luoghi critici scoperti» (top 10, `zone_scoperte_top10`, nomi);
  6. `barre` «Profili del riempimento» (`firme_riempimento`) con nota [DATI SCARSI: 2 giorni feriali];
  7. `profilo` «Quanto si riempiono: i 4 interscambi del Comune» — serie Stura, Sofia, Caio Mario, Venchi Unica (da `solo_sulla_carta` / `parcheggi[].profilo_feriale`, ore 0-23, valori 0-1) più Porta Susa FS come esempio di ciclo pulito; nota «feriale, media di 2 giorni»;
  8. `barre` «Eventi: auto stimate, posti entro 1 km, posti che mancano» per i 3 luoghi (3 grafici piccoli o voci con etichetta «Olimpico – auto stimate», ecc.), nota «[STIMATO] capienze da fonti web, 50% in auto, 2,5 persone per auto».
- `immagini`: `[{"file":"immagini/r6_torino.png","didascalia":"Tutta Torino: luoghi critici coperti (verde) e scoperti (rosso)"},{"file":"immagini/r6_zoom.png","didascalia":"Zoom su un quartiere: parcheggi e cerchi di 200 m"},{"file":"immagini/r6_evento.png","didascalia":"Il Lingotto e i luoghi di eventi"}]` (i file li crea Leo).
- `metodo` (4-6 frasi semplici): luoghi = fermate entro 40 m; i 7 segnali di S2 in parole; soglia = 10% più alto sul 4.425 luoghi della Città metropolitana; parcheggi = 5T + Comune + OpenStreetMap; classi e punti a favore; zona centrale Q001-Q009; copertura = parcheggio entro 200 m in linea d'aria.
- `parametri`: scenario, soglia 63,97, universo 4.425, raggi 100/200/400 m, zona centrale Q001-Q009, posti stimati 25 m² a posto (±30%), giorni di riempimento (date), auto per evento.
- `limiti` (sempre): riempimento pochi giorni [DATI SCARSI] e data prevista di aggiornamento (dopo il 25/10); parcheggi OSM incompleti, posti stimati; zona centrale scelta provvisoria; pendolari IMQ campionari; linea d'aria; corse programmate; nessuna stima del traffico di eventi reale; Allianz Stadium non incluso; fermate fuori Città metropolitana escluse; 23 luoghi senza zona IMQ fuori.
- `mappa`: `{"id":"interscambio","tema":"Parcheggi di interscambio","nota":"Luoghi critici e parcheggi su mappa, con cerchi di copertura e luoghi di eventi."}`.
- `fonti`: `docs/PIANO_RISULTATO6_FINALE.md`, `docs/ESITO_RISULTATO6_V2_GIRO2.md`, `docs/RAPPORTO_RISULTATO6_V2.txt`, `docs/RAPPORTO_R6V2_EVENTI.txt`, `scripts/68…79`. `avviso`: `["Dati [STIMATO] / [PROGRAMMATO] / [MISURATO – dati scarsi]", "…"]`. `scenari`: un solo blocco «Scenario S2» con 5-6 numeri (critici, coperti F 200 m, coperti ufficiali, parcheggi potenziali, posti potenziali, interscambi solo sulla carta), `prima: None`.

**5.3** Rilancia `python scripts\schede_risultati.py` e `node --check data\schede_risultati.js`; controlla nello stdout la riga di R6 (numeri e grafici = 8); controlla che `data/schede_risultati.js` contenga «Parcheggi di interscambio», «238» e «Versione 2». Scrivi l'esito e **FERMATI**: Claude apre `simulazione.html` e la scheda nel browser.

---

## FASE 6 — Chiusura (Claude)

Verifica visiva finale di mappa e scheda (anche schermo stretto), aggiornamento di `MEMORIA_PROGETTO.md`, rimozione di `mappa_torino_prima_R6.html`, commit su richiesta di Leo. Poi, dopo il fetch di **domenica 25/10** (≥ 5 feriali): rifare 71→72→73→75→76→78→79, `04_genera_mappa.py`, `schede_risultati.py`.

## Cosa NON fare

- Non cambiare scenario, parametri degli eventi, zona centrale, né i numeri dei file di dati. Non toccare gli altri risultati se non per i colori della Fase 1 e 4.
- Non scrivere dati a mano nel template: tutto da `D.r6`.
- Non usare librerie esterne (la pagina deve funzionare offline). Non pubblicare niente.
- Non cancellare `scheda_r6` né la copia `mappa_torino_prima_R6.html`.
