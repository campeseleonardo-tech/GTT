# Piano meccanico — Risultato 6: correzioni di ciò che non funziona (19/10/2026)

Scritto da Claude con Leo, per un altro modello (agente). **Solo correzioni**: nessuna nuova funzione, nessun cambio di criteri o di numeri. Riepilogo del risultato: `docs/PIANO_RISULTATO6.md` (in testa). Ciò che non è citato qui **resta com'è**.
Esegui **tutte le fasi di seguito, senza fermarti a chiedere**. Dopo ogni fase scrivi in `docs/ESITO_R6_CORREZIONI.md` `FASE n: OK` o `FASE n: FERMO – motivo`. Se un controllo non torna: correggi se la causa è tua e chiara; altrimenti **non inventare**, scrivi cosa hai visto e continua. Claude controlla tutto nel browser alla fine.

## 0. Regole
1. Cartella `C:\projects\Progetti\GTT`, ramo **`prova`** (se no, FERMATI). **Nessun commit.** Python del PATH (3.14). Dati e database in sola lettura. Nessuna libreria nuova.
2. **Puoi modificare**: `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/80_porte_interscambio.py`, `scripts/79_dati_mappa_r6.py`, `scripts/schede_risultati.py`, `simulazione.html`. **Nuovi**: `scripts/prova_pagine_r6.py`, `docs/ESITO_R6_CORREZIONI.md`, `immagini/` (screenshot). Non toccare `MEMORIA_PROGETTO.md`, `data/ref/*`, script 68-78.
3. `mappa_torino.html`, `data/schede_risultati.js`, `mappa_r6.json`, `porte.json` si **rigenerano** (`python scripts\80_porte_interscambio.py`, `python scripts\79_dati_mappa_r6.py`, `python scripts\04_genera_mappa.py`, `python scripts\schede_risultati.py`), mai a mano.
4. **Perché questo piano**: il giro precedente è stato verificato solo con `node --check` e **non ha visto un errore a runtime** (`r6Data is not defined`) che appare in pagina. Da ora ogni fase si chiude con la **prova automatica a runtime** della Fase 1 (non basta la sintassi).

## FASE 1 — Prova automatica delle pagine (script nuovo)
Scrivi `scripts/prova_pagine_r6.py`:
1. Avvia `python -m http.server <porta libera> --bind 127.0.0.1` in un processo figlio dalla cartella del progetto (porta ≠ 8765, es. 8799) e lo ferma alla fine.
2. Per ognuno di questi indirizzi lancia **Edge headless** (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`; in alternativa `C:\Program Files\Google\Chrome\Application\chrome.exe`) con `--headless=new --disable-gpu --window-size=1400,900 --enable-logging=stderr --v=0 --virtual-time-budget=15000 --dump-dom <url>` e **cattura stderr**:
   `mappa_torino.html#tema=interscambio&vista=parcheggi`, `…&vista=aree`, `…&vista=mancano`, `mappa_torino.html#tema=servizio`, `simulazione.html`.
   Segnala come **ERRORE** ogni riga di stderr che contiene `Uncaught`, `ReferenceError`, `TypeError`, `SyntaxError` o `Failed to execute`, e controlla nel DOM stampato che `#jsoff` **non** sia `display: block` e (per la mappa) che la legenda contenga il titolo atteso della vista («Dove ci sono parcheggi?», «In quali aree mancano parcheggi?», «Dove servirebbe di più un parcheggio?»).
3. Fai gli **screenshot**: per ciascuna delle tre viste `--screenshot=immagini\r6_<vista>.png` (1400×900, `--virtual-time-budget=15000`); per `simulazione.html` non serve. Scrivi nel rapporto la dimensione di ogni file (se un file ha meno di 20 KB, probabile pagina vuota: segnala).
4. Esito stampato: «OK» o l'elenco degli errori con l'indirizzo. Lo script si lancia con `python scripts\prova_pagine_r6.py` e restituisce codice 1 in caso di errori.
5. **Per poter aprire direttamente una vista**, in `mappa_template.html` estendi `temaDaUrl` (≈ riga 2352): oltre a `#tema=interscambio` leggi `&vista=parcheggi|aree|mancano` e, dopo `applicaTema`, imposta `OPT_VAL.r6Vista` e il menu `#r6Vista` e richiama `impostaR6Vista()` (come fa il gestore del menu); valore non valido → `parcheggi`. Vale anche con `hashchange`.
6. Lancia lo script **ora** (prima delle altre correzioni): deve **trovare** l'errore `r6Data` (scrivilo nell'esito come prova che il test funziona). Se Edge non parte o non stampa errori, scrivilo e usa Chrome; se nessuno dei due funziona, scrivi «prova automatica non possibile: …» e procedi usando una funzione di prova in pagina (`window.__prova()`), solo se riesci a eseguirla davvero.

## FASE 2 — Errore `r6Data` e robustezza della legenda
1. In `mappa_template.html` `r6RigheFonti` (≈ riga 1080) usa `r6Data`, che **non esiste**: definiscila accanto agli altri helper `r6…` (≈ riga 937): `const r6Data = iso => { const p=String(iso||"").slice(0,10).split("-"); return p.length===3 ? `${p[2]}/${p[1]}` : String(iso||"—"); };` (da `2026-10-15` a `15/10`).
2. Cerca **tutti** gli identificatori `r6…`/`R6…` usati ma non definiti (controllo statico con una regex nel tuo script di prova) e correggili: oggi risulta solo `r6Data`.
3. **Legenda robusta**: in `aggiornaLegenda()` avvolgi `tema.legenda()` in `try/catch`: in caso di errore mostra «Legenda non disponibile» invece di lasciare la legenda del tema precedente (che oggi resta sullo schermo: «Passaggi all'ora ogni 1000 abitanti» sul tema dei parcheggi) e scrivi l'errore in `console.error`.
4. Rilancia `python scripts\04_genera_mappa.py` e `python scripts\prova_pagine_r6.py`: **zero errori** sulle 5 pagine. Scrivi l'esito.

## FASE 3 — Etichette ripetute nella vista «aree»
Nella vista «aree» il nome compare più volte per lo stesso comune/quartiere (es. «Venaria Reale» ×2, «Parella» ×2, «Mirafiori Sud» ×3, «Moncalieri» ×4). Correggi:
1. In `80_porte_interscambio.py` ogni area ha già `zone_principali`; aggiungi per ogni area il campo `etichetta` = la prima zona principale, e un campo `mostra_etichetta` = vero **solo per un'area per etichetta** (quella con più fermate importanti; a parità la più a nord), falso per le altre. Le aree con meno di 3 fermate (indicative) non hanno etichetta.
2. In `mappa_template.html` disegna l'etichetta solo se `mostra_etichetta` e a zoom < 13 (a zoom ≥ 13 nessuna etichetta, restano i colori e il clic); font come ora, alone bianco.
3. Il titolo della scheda al clic resta «Area di <zone principali>».
4. Rigenera 80 → 79 → 04. Controllo: nell'elenco delle etichette disegnate (esponi `window.__etichetteAree` solo per la prova, o contale nello script a partire dal JSON) nessun nome compare due volte. Esito: numero di etichette prima/dopo.

## FASE 4 — Profili di riempimento con descrizioni vere
Oggi i titoli dei profili dicono cose generiche («ha un andamento misto» per Stura, che di fatto è piena sia di notte sia di giorno).
1. In `80_porte_interscambio.py` calcola per ogni garage con dati: `notte` (N, media feriale 2-5), `giorno` (G, 10-16), `mattina` (M, 7-9), `weekend` (W, 10-16, se c'è), tutti in %.
2. **Descrizione in parole** (prima regola che vale; sostituisce quella per `firma`):
   - `G − N ≥ 20` punti e (W assente o G − W ≥ 10): «si riempie nei giorni feriali: N% di notte, G% di giorno»;
   - `G − N ≥ 20` e W presente e G − W < 10: «si riempie di giorno anche nel weekend: N% di notte, G% di giorno»;
   - `N − G ≥ 10`: «è più pieno di notte che di giorno: N% di notte, G% di giorno»;
   - ampiezza (max − min delle medie orarie) < 6 punti: «il valore non cambia (G%): forse il contatore è fermo» se G < 15% o G > 85%, altrimenti «sempre intorno al G%»;
   - `G ≥ 85` e `N ≥ 70`: «sempre quasi pieno: N% di notte, G% di giorno»;
   - altrimenti «andamento irregolare: N% di notte, G% di giorno».
   Applica la stessa descrizione ai nomi dei comportamenti medi (`profili_medi`: una riga per gruppo di garage con la stessa descrizione-tipo; se il gruppo ha meno di 2 garage non fare la curva media).
3. In `79`/`schede_risultati.py` usa queste descrizioni nei titoli dei grafici `profilo` e nelle legende; nella mappa nel clic del parcheggio. Titolo del tipo «Stura (589 posti): sempre quasi pieno: 79% di notte, 90% di giorno».
4. Controllo: Stura e Lingotto non risultano più «andamento misto»; Caio Mario «il valore non cambia (1%): forse il contatore è fermo»; Sofia «più pieno di notte che di giorno». Scrivi le 6 descrizioni nell'esito.

## FASE 5 — Nomi e coerenza dei testi
1. Il tema in mappa e la scheda si chiamano ora «**Parcheggi per lasciare l'auto**»: tieni questo nome **ovunque** (menu del tema, scheda, guida, avviso, `fonti`, titolo del grafico, memoria non toccare). Cerca «Parcheggi di interscambio» in `mappa_template.html`, `schede_risultati.py`, `simulazione.html`, `04_genera_mappa.py` e sostituisci dove è un nome pubblico (non nei nomi dei file né negli id `interscambio`/`risultato6`).
2. Nella vista «mancano» la legenda cita «circa 20 punti»: controlla che i numeri nella legenda coincidano con `punti_prioritari` (20) e con le fermate (206 senza 50 posti).
3. **Frasi pubbliche**: nella scheda e nella mappa cerca e rimuovi ogni espressione da addetti ai lavori: «fonte_stato», «nodo forte» (scrivi «nodo di trasporto importante: metro, treno, capolinea o molte corse»), «IMQ» senza spiegazione (la prima volta «indagine IMQ 2022 sugli spostamenti»), «5T» senza spiegazione (la prima volta «5T, il sistema dei trasporti della Città di Torino»), «[STIMATO]» senza la legenda dei tag (c'è già nella guida: controlla che la scheda abbia la riga «Come leggere i tag: [MISURATO]… »). Aggiungi quella riga se manca (campo `avviso` della scheda).
4. Controllo: la scheda R6 non contiene «utile», «osservazion», «versione», «scenario», «S2», «Allianz», «doppio», «nodo forte», «fonte_stato».

## FASE 6 — Prova finale e screenshot
1. Rigenera tutto nell'ordine 80 → 79 → 04 → `schede_risultati.py`; `node --check` su `data\schede_risultati.js` e sugli `<script>` di `mappa_torino.html` e `simulazione.html`.
2. Lancia `python scripts\prova_pagine_r6.py`: deve dare **zero errori** e generare `immagini\r6_parcheggi.png`, `immagini\r6_aree.png`, `immagini\r6_mancano.png`. Non rinominarli: Leo/Claude sceglieranno quali usare per la scheda.
3. Nell'esito: tabella degli errori trovati prima/dopo, numero di etichette prima/dopo, le 6 descrizioni dei profili, dimensioni dei PNG, file modificati, anomalie.

## Cosa NON fare
- Non cambiare criteri, soglie, numeri, parametri, né i 378 luoghi o i 212 parcheggi. Non usare le osservazioni di Leo nei dati. Niente nuove viste o funzioni. Nessun commit. Non pubblicare.
