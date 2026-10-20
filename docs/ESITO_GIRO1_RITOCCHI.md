# Esito — Giro 1 ritocchi (passi 1-6)

Eseguito da una sessione cloud (non dal PC di Leo), ramo `claude/practical-lamport-5laaug` (scelto da Leo al posto di `prova`).
Cambiate rispetto al piano: commit e push sul ramo di sessione (richiesti da Leo); nessun dato in `data/`, quindi **nessuno script è stato eseguito** (solo controllo di sintassi).
Python della sessione: 3.13 (non Anaconda). Non toccati: `prova`, `MEMORIA_PROGETTO.md`, il Pi, il database, `data/`.

Controlli fatti dopo ogni file: `python -m py_compile` sugli script Python; `node --check` sui tre blocchi `<script>` di `scripts/mappa_template.html` (tutti e tre OK dopo ogni modifica).

## Riepilogo

| Passo | Esito |
|---|---|
| 1 Pannello parcheggio | OK |
| 2 Togliere vista «aree» | AVVISO (restano due testi con «aree», vedi sotto) |
| 3 Parcheggi del centro in mappa | OK (non eseguibile qui: va rigenerato al passo 7) |
| 4 Risultato 2 nascosto | OK |
| 5 R4 e R9 in una scheda, classifiche ordinarie | OK |
| 6 Risultato 8 | OK |
| 7 Rigenerare tutto e provare le pagine | **DA FARE da Leo sul PC** (qui non ci sono i dati) |

## PASSO 1: OK
`scripts/mappa_template.html`
- `.sc-det-k{color:var(--muted);flex:none}` → `.sc-det-k{color:var(--muted);flex:0 1 auto;max-width:60%}`
- `.sc-det-v{color:var(--ink);text-align:right;word-break:break-word}` → `.sc-det-v{color:var(--ink);text-align:right;word-break:break-word;flex:1 1 auto;min-width:0}`
- `r6SchedaParcheggio`: `titolo: esc(p.nome), badge:"stimato", sub:` → `titolo: esc(p.nome), badge: stim ? "stimato" : null, sub:` (`creaScheda` già gestisce `badge` nullo).
Controllo: ognuna delle tre stringhe nuove compare 1 volta.

## PASSO 2: AVVISO
`scripts/mappa_template.html`
- tolta la riga `["aree","In quali aree mancano parcheggi?"],` da `OPZIONI`.
- tolta la riga `  aree: "In quali aree mancano posti? …"` da `R6_DESC`.
- `["parcheggi","aree","mancano"].includes(m[1])` → `["parcheggi","mancano"].includes(m[1])`.
- guida: tolta la frase da `<b>In quali aree mancano posti?</b>` a prima di `<b>Dove servirebbe di più un parcheggio?</b>`; «Tre domande, nel menu» → «Due domande, nel menu».
- tolta la riga di commento `   2. «aree»: In quali aree mancano posti? …` sopra `R6_VISTA`.

`scripts/schede_risultati.py` (`scheda_r6`)
- tolto il grafico `"Le aree: critiche, scarse, buone"` (intero dizionario).
- `non ne hanno nessuno); le aree più scoperte: {tre_critiche}.",` → `non ne hanno nessuno).",`
- tolta `num("Aree in categoria Critica", apc["Critica"], "aree"),`
- `"Tre domande nella mappa, … dove ci sono parcheggi, in quali aree mancano posti, dove servirebbe di più un parcheggio."` → `"Due domande nella mappa, nel menu «Cosa vedere»: dove ci sono parcheggi e dove servirebbe di più un parcheggio."`
- metodo: `"Aree: celle esagonali di circa 2 km²; punti prioritari (fino a 20…` → `"Punti prioritari (fino a 20…`
- tolta la riga parametri `["Aree", "celle di circa 2 km²; almeno 5 fermate valutate"],`
- `tre_critiche`, `con_cat`, `apc` ora non usate: lasciate (come da piano).

`scripts/prova_pagine_r6.py`
- tolta la voce `"aree": "In quali aree mancano posti per lasciare l'auto?",` da `TITOLI_VISTA`.
- `("parcheggi", "aree", "mancano")` → `("parcheggi", "mancano")`.

Controllo: `py_compile` OK. Il controllo `findstr "In quali aree"` **non è «vuoto»**, per due motivi che il piano non prevedeva (non toccati, per la regola 4):
1. `scripts/mappa_template.html` riga ~1124: titolo della legenda dentro il ramo `if(v==="aree")` di `legendaR6` (ramo morto, che il piano dice di lasciare: «i rami `if(v==="aree")` restano»). Non visibile a Leo.
2. **Visibile:** `scripts/mappa_template.html` riga ~2228, descrizione del tema «Parcheggi per lasciare l'auto»: «Tre domande: dove ci sono parcheggi, in quali aree mancano posti, dove servirebbe di più un parcheggio.» Il piano non la nomina (non contiene «In quali aree» con la I maiuscola, quindi il controllo non la trova), ma dopo il passo 2 è sbagliata. **Da correggere in «Due domande: dove ci sono parcheggi, dove servirebbe di più un parcheggio.»** (decisione a Leo/Claude).
Anche il commento sopra `R6_VISTA` dice ancora «Tre viste» (il piano chiede di togliere solo la riga 2). Non toccato.

## PASSO 3: OK (da verificare al passo 7)
`scripts/84_risultato6_parcheggi.py`, sezione `# ---- parcheggi in mappa ----`
- aggiunte dopo `grande_vicino = …`:
  ```python
          in_centro = info_ad.get(p["id"], {}).get("zona_imq") in comuni.ZONE_CENTRALI and \
              (posti_rec(p) >= MIN_POSTI_MOSTRATO or p["tipo"] == "garage_5t")
  ```
- `if not (ufficiale or grande_vicino):` → `if not (ufficiale or grande_vicino or in_centro):`
- in `da_mostrare.append({…})` aggiunta la chiave `"in_centro": bool(in_centro),`.

`scripts/mappa_template.html`
- `disegnaR6Parcheggi`: `cx.fillStyle=R6_COL_STATO[p.stato]||"#9aa3b2";` → `cx.fillStyle=p.in_centro?"#6a51a3":(R6_COL_STATO[p.stato]||"#9aa3b2");`
- `r6SchedaParcheggio`, `dettagli`: nuova prima voce `...(p.in_centro ? [{k:"In centro", v:"non serve a lasciare l'auto prima di entrare in città"}] : []),`
- `legendaR6`, ramo `parcheggi`: dopo la riga «interscambio del Comune» aggiunta `+`<span><i style="background:#6a51a3"></i>in centro (non per lasciare l'auto)</span>``.

Nota per il passo 7: `da_mostrare` alimenta anche i profili 5T e `parcheggi_mostrati`/`quota_posti_misurati` del riepilogo: questi due numeri possono cambiare (atteso, entrano i parcheggi del centro). «Fermate importanti» e «Punti prioritari» dovrebbero restare uguali: da confrontare.

## PASSO 4: OK
`scripts/schede_risultati.py`
- sopra `def main():` aggiunto `NASCOSTE = {"risultato2"}   # in pausa (Leo, 20/10/2026): docs/PIANO_RISULTATO2.md`
- nel `for nome, fabbrica in (…):` come prima riga del corpo: `if nome in NASCOSTE:` / `continue`.
Controllo «`"risultato": "2"` assente da `data\schede_risultati.js`»: da fare al passo 7.

## PASSO 5: OK
A. `scripts/27_risultato4_regolarita.py`
- sotto `MIN_COPPIE = 100`: aggiunti `MIN_PASSAGGI_CLASSIFICA = 2000` (con commento) e la funzione `linea_ordinaria(nome)` (`str(nome).isdigit()`).
- classifica ritardo: `if v["passaggi"] >= MIN_PASSAGGI), reverse=True)` → `if v["passaggi"] >= MIN_PASSAGGI_CLASSIFICA and linea_ordinaria(k)), reverse=True)`; titolo → `"10 LINEE PEGGIORI PER % IN RITARDO (feriale, linee ordinarie, >= {MIN_PASSAGGI_CLASSIFICA} passaggi)"`.
- classifica irregolarità: `if v["coppie"] >= MIN_COPPIE), reverse=True)` → `if v["coppie"] >= MIN_COPPIE and linea_ordinaria(k)), reverse=True)`; titolo → `"10 LINEE PEGGIORI PER IRREGOLARITA' (feriale, linee ordinarie, >= {MIN_COPPIE} coppie)"`.
- parametri: aggiunto `"min_passaggi_classifica": MIN_PASSAGGI_CLASSIFICA,` prima di `"min_coppie"`.

B. `scripts/schede_risultati.py`
- `peggio_rit`: `if x[1]["passaggi"] >= par["min_passaggi"]` → `if x[1]["passaggi"] >= par.get("min_passaggi_classifica", 2000) and str(x[0]).isdigit()`.
- `peggio_irr`: aggiunto `and str(x[0]).isdigit()` alla condizione.
- nota del grafico: `f"Solo linee con almeno {par['min_passaggi']} passaggi osservati."` → `f"Solo linee ordinarie (nome di sole cifre) con almeno {par.get('min_passaggi_classifica', 2000)} passaggi osservati."`
- `main()`: tolto `("risultato9", scheda_r9)` dalla tupla (`("risultato8", scheda_r8)):`).
- `scheda_r4()`: `    return {` → `    scheda = {`; dopo la `}` finale aggiunto il blocco del piano (`r9 = scheda_r9()` … `return scheda`), identico al testo del piano.
Controllo (4 schede, titolo «Puntualità e attese», niente RV2/VEX/LS1/68+/17/): da fare al passo 7. Il parametro `min_passaggi_classifica` esiste nel JSON solo dopo aver rieseguito lo script 27; fino ad allora la scheda usa 2000 per default.

## PASSO 6: OK
`scripts/schede_risultati.py`, `scheda_r8`
1. «strade grandi di Torino»: la frase di `"risposta"` lo diceva già («Sulle … tratte di strade grandi di Torino … il …% della lunghezza»): nessun cambio. In `"in_english"`: `Of {n} road sections ({km} km),` → `Of {n} road sections on Turin's major roads ({km} km),`. Nella scheda non c'è nessuna frase «nessuna zona senza fermate» (quella a riga ~261 è della scheda R1, di notte: non toccata).
2. Dopo il grafico «Prova del modello sui 20 sensori» aggiunto il grafico «Errore della stima su ogni sensore (%)», identico al testo del piano.
3. `"docs/RIASSUNTO_TRAFFICO.md"` → `"docs/PIANO_RISULTATO8.md"` nelle `fonti`.
Controllo: `py_compile` OK.

## PASSO 7: DA FARE da Leo sul PC
Qui non ci sono i dati (`data/processed` assente) e nessuno script è stato eseguito. Da fare come scritto nel piano: `scripts\RISULTATO6_RIFAI.bat`, poi `27_risultato4_regolarita.py`, `70_risultato9_attesa.py`, `schede_risultati.py`, `prova_pagine_r6.py`, `86_prepara_pubblicazione.py`. Da annotare: titoli delle 4 schede, 10 linee peggiori nuove/uscite, parcheggi in mappa (prima 142) e quanti `in_centro`, righe «Fermate importanti» e «Punti prioritari» del rapporto R6 (uguali a prima), `git status`.
Prima di rigenerare conviene decidere il testo del punto 2 dell'AVVISO del passo 2 (descrizione del tema a riga ~2228).
