# Piano meccanico — Giro 1: ritocchi che si vedono in pagina (dopo l'analisi di Leo del 20/10/2026)

Scritto da Claude per un **modello minore** che lavora sul PC di Leo. Raccoglie i lavori piccoli decisi da Leo il
20/10 nei piani dei risultati (`docs/PIANO_RISULTATO2/4/6/8.md`). Nessun calcolo nuovo: si cambiano testi, schede e
mappa, poi si rigenera tutto **una volta sola** alla fine. Esito in `docs/ESITO_GIRO1_RITOCCHI.md`.

## 0. Regole (valgono per tutto il giro)

1. Cartella `C:\projects\Progetti\GTT`, ramo `prova` (`git branch --show-current`; se è un altro: FERMATI e dillo a
   Leo). Prima di tutto: `git status` (deve essere pulito) e `git pull origin prova`. **Nessun commit**: lo fa Leo.
2. Python del PATH (`python`), mai Anaconda. Sola lettura su `data/raw/`, `data/storico_backup.sqlite`, sul Pi.
3. Un passo alla volta, nell'ordine. Dopo ogni passo scrivi nell'esito: `PASSO x: OK` / `AVVISO` / `FERMO – motivo`,
   e **ogni riga di codice cambiata** (file, prima, dopo).
4. Cambia **solo** quello che il passo dice. Niente numeri scritti a mano nei testi: vengono dai file. Niente nuove
   soglie oltre a quelle scritte qui. Non toccare gli script 33-67, 81-83, 85, il database, il Pi.
5. Se un comando dà errore e la causa non è evidente in una riga: FERMO su quel passo, scrivi l'errore esatto e
   passa al passo successivo che non dipende da quello.

## Passo 1 — Pannello del parcheggio (R6, mappa)

File `scripts/mappa_template.html`.
1. Cerca la riga `.sc-det-k{color:var(--muted);flex:none}` e sostituiscila con
   `.sc-det-k{color:var(--muted);flex:0 1 auto;max-width:60%}`.
2. Cerca la riga `.sc-det-v{color:var(--ink);text-align:right;word-break:break-word}` e sostituiscila con
   `.sc-det-v{color:var(--ink);text-align:right;word-break:break-word;flex:1 1 auto;min-width:0}`.
3. In `function r6SchedaParcheggio(p)` cerca `titolo: esc(p.nome), badge:"stimato",` e sostituisci con
   `titolo: esc(p.nome), badge: stim ? "stimato" : null,` (il bollino solo se i posti sono stimati).
Controllo: le tre stringhe nuove compaiono una volta ciascuna (`findstr /n "max-width:60%" scripts\mappa_template.html`).

## Passo 2 — Togliere la vista «aree» (R6, mappa e scheda)

File `scripts/mappa_template.html`:
1. In `const OPZIONI = {` togli la riga `["aree","In quali aree mancano parcheggi?"],`.
2. In `const R6_DESC = {` togli la riga che inizia con `  aree: "In quali aree mancano posti?`.
3. Nella funzione che legge la vista dall'indirizzo (cerca `["parcheggi","aree","mancano"].includes(m[1])`) togli
   `"aree",`.
4. Nel testo della guida (cerca `<b>In quali aree mancano posti?</b>`) togli la frase da `<b>In quali aree mancano
   posti?</b>` fino al punto prima di `<b>Dove servirebbe di più un parcheggio?</b>`, e cambia «Tre domande» in «Due
   domande».
5. Nel commento sopra `const R6_VISTA` togli la riga `2. «aree»: …`. Le funzioni `disegnaR6Aree` e i rami
   `if(v==="aree")` **restano** (non fanno danni: la vista non si può più scegliere).
File `scripts/schede_risultati.py`, funzione `scheda_r6`:
6. Togli il grafico con `"titolo": "Le aree: critiche, scarse, buone"` (tutto il dizionario `{...}` fino alla sua
   chiusura e la virgola).
7. Nella frase della risposta che contiene `le aree più scoperte: {tre_critiche}` togli `; le aree più scoperte:
   {tre_critiche}` (il punto finale resta).
8. Nella lista dei numeri togli `num("Aree in categoria Critica", apc["Critica"], "aree"),`.
9. Nel testo con `"Tre domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi, in quali aree mancano
   posti, dove servirebbe di più u…` cambia in «Due domande … dove ci sono parcheggi e dove servirebbe di più un
   parcheggio» (il resto della frase uguale).
10. Nel metodo, la frase che inizia `"Aree: celle esagonali di circa 2 km²; punti prioritari` diventa `"Punti
   prioritari` (togli solo «Aree: celle esagonali di circa 2 km²; » e metti la P maiuscola); nei parametri togli
   la riga `["Aree", "celle di circa 2 km²; almeno 5 fermate valutate"],`.
11. Se dopo i tagli le variabili `tre_critiche`, `con_cat` o `apc` non sono più usate, lasciale (non fanno danni).
File `scripts/prova_pagine_r6.py`:
12. In `TITOLI_VISTA` togli la voce `"aree": …`; nella riga `for vista in (() if args.senza_screenshot else
   ("parcheggi", "aree", "mancano")):` togli `"aree", `.
Controllo: `python -m py_compile scripts\schede_risultati.py scripts\prova_pagine_r6.py` senza errori;
`findstr /c:"In quali aree" scripts\mappa_template.html scripts\schede_risultati.py` non trova niente.

## Passo 3 — Parcheggi del centro in mappa (R6)

File `scripts/84_risultato6_parcheggi.py`, sezione `# ---- parcheggi in mappa ----`.
1. Dopo la riga `grande_vicino = …` (due righe) aggiungi:
   ```python
        in_centro = info_ad.get(p["id"], {}).get("zona_imq") in comuni.ZONE_CENTRALI and \
            (posti_rec(p) >= MIN_POSTI_MOSTRATO or p["tipo"] == "garage_5t")
   ```
   (stessa indentazione di `grande_vicino`).
2. Cambia `if not (ufficiale or grande_vicino):` in `if not (ufficiale or grande_vicino or in_centro):`.
3. Nel dizionario `da_mostrare.append({…})` aggiungi la chiave `"in_centro": bool(in_centro),`.
4. I conteggi del risultato **non cambiano**: i parcheggi del centro non sono «adatti» e non entrano in nessuna
   classe. Verifica: nel rapporto `docs/RAPPORTO_R6_PARCHEGGI.txt` le righe «Fermate importanti» e «Punti
   prioritari» restano identiche a prima (confronta con `git diff docs\RAPPORTO_R6_PARCHEGGI.txt` dopo il passo 7).
File `scripts/mappa_template.html`, funzione `disegnaR6Parcheggi`:
5. Dopo `const r=r6RaggioPx(p), stim=r6Stimato(p);` la riga che imposta il colore diventa:
   `cx.beginPath(); cx.arc(X,Y,r,0,6.2832); cx.fillStyle=p.in_centro?"#6a51a3":(R6_COL_STATO[p.stato]||"#9aa3b2");`
6. In `function r6SchedaParcheggio(p)`, nella lista `dettagli`, come **prima** voce aggiungi
   `...(p.in_centro ? [{k:"In centro", v:"non serve a lasciare l'auto prima di entrare in città"}] : []),`.
7. In `function legendaR6()`, ramo `if(v==="parcheggi")`, subito **dopo** la riga
   ``+`<span><i style="background:#fff;border:2.5px solid #1d2430"></i>interscambio del Comune</span>` ``
   aggiungi la riga (viola = categoria a parte, diverso dal grigio «non misurato»)
   ``+`<span><i style="background:#6a51a3"></i>in centro (non per lasciare l'auto)</span>` ``.

## Passo 4 — Risultato 2 nascosto

File `scripts/schede_risultati.py`, funzione `main()`.
1. Sopra `def main():` aggiungi: `NASCOSTE = {"risultato2"}   # in pausa (Leo, 20/10/2026): docs/PIANO_RISULTATO2.md`
2. Dentro il `for nome, fabbrica in (…):`, come prima riga del corpo, aggiungi:
   `        if nome in NASCOSTE:` / `            continue` (due righe, indentazione del corpo del for).
Controllo: dopo il passo 7, `data\schede_risultati.js` non contiene `"risultato": "2"`.

## Passo 5 — Risultati 4 e 9 in una scheda, classifiche solo con linee ordinarie

A. File `scripts/27_risultato4_regolarita.py` (classifiche del rapporto):
1. Sotto `MIN_COPPIE = 100` aggiungi:
   ```python
   MIN_PASSAGGI_CLASSIFICA = 2000   # classifica delle linee peggiori: solo linee ordinarie (Leo, 20/10/2026)


   def linea_ordinaria(nome):
       """Linee ordinarie: nome fatto solo di cifre (es. 4, 17, 68). Speciali e varianti (RV2, VEX, LS1, 68+, 17/) no."""
       return str(nome).isdigit()
   ```
2. Nella classifica per ritardo (blocco `class_p = sorted(((v["ritardo"], k) for k, v in`) la riga
   `if v["passaggi"] >= MIN_PASSAGGI), reverse=True)` diventa
   `if v["passaggi"] >= MIN_PASSAGGI_CLASSIFICA and linea_ordinaria(k)), reverse=True)`; la riga sotto
   `R.append(f"10 LINEE PEGGIORI PER % IN RITARDO (feriale, >= {MIN_PASSAGGI} passaggi)")` diventa
   `R.append(f"10 LINEE PEGGIORI PER % IN RITARDO (feriale, linee ordinarie, >= {MIN_PASSAGGI_CLASSIFICA} passaggi)")`.
3. Nella classifica per irregolarità (blocco `class_r = …`) la riga `if v["coppie"] >= MIN_COPPIE), reverse=True)`
   diventa `if v["coppie"] >= MIN_COPPIE and linea_ordinaria(k)), reverse=True)`; nel titolo sotto aggiungi
   «linee ordinarie, ».
4. Nel dizionario dei parametri (riga con `"min_passaggi": MIN_PASSAGGI, "min_coppie": MIN_COPPIE}`) aggiungi
   `"min_passaggi_classifica": MIN_PASSAGGI_CLASSIFICA,` prima di `"min_coppie"`.
B. File `scripts/schede_risultati.py`, funzione `scheda_r4()` (la scheda calcola le sue classifiche):
5. La riga `peggio_rit = sorted((x for x in linee if x[1]["passaggi"] >= par["min_passaggi"]),` diventa
   `peggio_rit = sorted((x for x in linee if x[1]["passaggi"] >= par.get("min_passaggi_classifica", 2000) and str(x[0]).isdigit()),`
   e la riga `peggio_irr = sorted((x for x in linee if (x[1].get("coppie") or 0) >= par["min_coppie"]),` diventa
   `peggio_irr = sorted((x for x in linee if (x[1].get("coppie") or 0) >= par["min_coppie"] and str(x[0]).isdigit()),`.
   La nota del grafico `"Solo linee con almeno {par['min_passaggi']} passaggi osservati."` diventa
   `f"Solo linee ordinarie (nome di sole cifre) con almeno {par.get('min_passaggi_classifica', 2000)} passaggi osservati."`.
6. In `main()` togli `("risultato9", scheda_r9)` dalla tupla (la funzione `scheda_r9` resta).
7. In `scheda_r4()` la riga `    return {` (quella dopo `nomi_fasce = {…}`) diventa `    scheda = {`. Alla fine
   del dizionario (la `}` che lo chiude, con 4 spazi davanti) aggiungi sotto:
   ```python
    r9 = scheda_r9()
    scheda["titolo"] = "Puntualità e attese"
    scheda["domanda"] = scheda["domanda"] + " E quanto si aspetta davvero alla fermata, rispetto a quello che promette l'orario?"
    scheda["risposta"] = scheda["risposta"] + ["Attesa: " + r9["risposta"][0]] + r9["risposta"][1:]
    for chiave in ("grafici", "scenari", "limiti"):
        scheda[chiave] = scheda.get(chiave, []) + r9.get(chiave, [])
    scheda["in_english"] = scheda.get("in_english", []) + r9.get("in_english", [])[1:]
    scheda["fonti"] = [f.replace("PIANO_RISULTATO9_ATTESA.md", "PIANO_RISULTATO4.md")
                       for f in scheda.get("fonti", []) + r9.get("fonti", [])]
    return scheda
   ```
   (Attenzione: in questa funzione la variabile `s` è già usata per gli scarti: non usare `s`.)
Controllo dopo il passo 7: `data\schede_risultati.js` ha 4 schede (R1, R4, R6, R8); la scheda R4 si intitola
«Puntualità e attese» e contiene i grafici dell'attesa; nella classifica non ci sono RV2, VEX, LS1, 68+, 17/.

## Passo 6 — Risultato 8: frase corretta ed errore in %

File `scripts/schede_risultati.py`, funzione `scheda_r8`:
1. Nelle frasi di `"risposta"` e in `"in_english"` dove si dice la quota di km coperti, aggiungi che si tratta delle
   **strade grandi di Torino** se non c'è già scritto (cerca `quota_km_coperta_tp`). Nella scheda **non** deve
   comparire una frase che dica che nessuna zona è senza fermate.
2. Nel grafico `"Prova del modello sui 20 sensori: misurato e stimato"` lascia le barre; **dopo** quel grafico
   aggiungi un grafico nuovo:
   ```python
            {"tipo": "barre", "titolo": "Errore della stima su ogni sensore (%)", "unita": "%",
             "nota": "Errore = |stimato − misurato| / misurato. Metà dei sensori sotto il valore tipico, gli altri sopra.",
             "voci": [voce(s["via"].replace("(TO)", "").replace("Unita' D'italia", "Unità d'Italia").strip(),
                           round(100 * abs(st - s["misurato"]) / s["misurato"]), tono="rosso")
                      for s, st in sorted(loo, key=lambda x: abs(x[1] - x[0]["misurato"]) / x[0]["misurato"])]},
   ```
3. Nelle `"fonti"` della scheda sostituisci `"docs/RIASSUNTO_TRAFFICO.md"` con `"docs/PIANO_RISULTATO8.md"`.
Controllo: `python -m py_compile scripts\schede_risultati.py`.

## Passo 7 — Rigenerare tutto e provare le pagine

1. Doppio clic su `scripts\RISULTATO6_RIFAI.bat` (rifà R6, mappa, schede, prova delle pagine). Deve finire con
   `FATTO`; nel log `logs\risultato6_rifai.log` «Verifiche non superate: 0» e «nessun errore a runtime».
2. `python scripts\27_risultato4_regolarita.py`, poi `python scripts\70_risultato9_attesa.py`, poi
   `python scripts\schede_risultati.py`, poi `python scripts\prova_pagine_r6.py` (0 errori).
3. `python scripts\86_prepara_pubblicazione.py` (README: 4 risultati, R2 assente).
4. Nell'esito: elenco delle schede prodotte (titoli), le 10 linee peggiori nuove e quelle uscite, quanti parcheggi
   in mappa ora (prima 142) e quanti `in_centro`, le righe «Fermate importanti» e «Punti prioritari» del rapporto R6
   (devono essere uguali a prima), il risultato di `git status`.

## Prompt da incollare (per Leo)

> Sei un agente che lavora sul progetto GTT nella cartella `C:\projects\Progetti\GTT`, ramo git `prova`.
> Prima: `git branch --show-current` (deve dire `prova`, se no fermati e dimmelo), `git status` (se ci sono file
> modificati fermati e dimmelo), poi `git pull origin prova`. Leggi `AGENTS.md`, poi esegui il piano
> `docs/PIANO_GIRO1_RITOCCHI.md` dall'inizio alla fine, un passo alla volta, nell'ordine, seguendo le regole della
> sezione 0. Cambia solo quello che ogni passo dice, con le righe esatte indicate; se una riga da cercare non c'è,
> scrivilo e passa avanti. Scrivi tutto in `docs/ESITO_GIRO1_RITOCCHI.md`: per ogni passo OK / AVVISO / FERMO e ogni
> riga di codice cambiata. Non fare commit, non modificare `MEMORIA_PROGETTO.md`, non toccare il Pi né il database.
> Python: `python` del PATH, mai Anaconda. Alla fine scrivimi un riassunto di 10 righe in italiano semplice.

Dopo: Leo fa commit e push (`git add -A`, `git commit -m "Giro 1 ritocchi"`, `git push origin prova`); Claude
ricontrolla esito, pagine e numeri.
