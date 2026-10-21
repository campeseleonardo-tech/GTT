# Esito: scheda «Case, servizi e fragilità» (Risultato 10 interno, 5 in pagina), sessione cloud

Scritto nel cloud, senza `data/`: **`schede_risultati.py` non è stato lanciato sui dati veri** (mancano anche i file dei risultati 1, 4, 6, 8). Provato con il `case_fragilita_servizi.json` ricavato dai dati dentro `mappa_torino.html`
(script 95 con `scripts/prove/dati_da_mappa_95.py`) e con uno finto (`95 --prova`), più schede finte minime per gli altri quattro risultati: `scripts/prove/prova_scheda_case.py`.

## Cosa c'è
- **Scheda** `scheda_r10()` + `forma_r10()` in `scripts/schede_risultati.py`, file `data/processed/risultato10_riepilogo_mappa.json` (nell'elenco di `main()`). Tutti i numeri sono letti da `case_fragilita_servizi.json`
  (campi `e1_si_paga_per_i_servizi`, `e2_doppio_svantaggio` con `sezioni.classi`, `e3_valore_metro.fasce`, `zone`, `conteggi`); niente scritto a mano.
- **Titolo-risposta**: «1 torinese su N vive dove la fragilità è alta e i servizi sono pochi», con N = 1 / quota dei residenti in sezioni con entrambe le condizioni, arrotondato. **Con i dati indicativi della mappa (9,5%) esce «1 su 11», non «1 su 10»**:
  con i dati veri dipende dal lancio (il titolo non si aggiusta a mano: se la quota fosse vicina al 10% uscirà 10).
- **Numero grande**: residenti in sezioni con entrambe le condizioni (79.598 nella prova) con la % dei torinesi nel testo.
- **Grafico principale**: dispersione delle zone OMI (servizi in x, prezzo in y, grandezza = abitanti) con la **retta di tendenza**. `risultati.html`: il tipo «dispersione» ora accetta `retta {a, b, label}`, passi degli assi `passo_x` / `passo_y` e
  il nome della zona nel suggerimento al passaggio del mouse (quarto valore di ogni punto).
- **Punti chiave**: Spearman prezzo-servizi (con l'intervallo); le zone in doppio svantaggio con i nomi (fino a 5) e i residenti; metro: «le case costano poco di più (+X euro al m², a pari distanza dal centro). Differenza fra zone, non effetto causale»
  (la parola «poco di più» dipende dal numero: sotto il 15% del prezzo senza metro; sopra «di più»; se negativo «non di più»).
- **Altri grafici**: le 4 classi delle sezioni (barre, residenti); prezzo con e senza metro per fascia di distanza (barre a gruppi). **Limiti**: quotazioni e non compravendite; un solo semestre; zone grandi; l'indice di fragilità non è il reddito. **Inglese**: 3 righe con gli stessi numeri.
- **«Vedi sulla mappa»**: `mappa_torino.html#tema=vulnerabilita&vista=doppio`. Il template prima non sceglieva la vista: `applicaVistaDaUrl` ora, con `vista=doppio`, seleziona «Doppio svantaggio» (provato: apre la vista con la sua legenda; gli altri indirizzi, anche `vista=mancano` del R6, non cambiano).
- **Numerazione pubblica**: campo `numero_pubblico` in ogni scheda (R1 → 1, R4 → 2, R6 → 3, R8 → 4, R10 → 5). La pagina scrive «Risultato N» col numero pubblico e ordina per quello. Restano validi i link `risultati.html#r1`, `#r4`, `#r6`, `#r8`
  (numeri interni) e i nomi dei file; nuovi indirizzi `risultati.html#p1`…`#p5` (anche la pagina li scrive quando si apre una scheda). Il testo del R4 che citava «Risultato 6» ora dice «Risultato 3».
- **`index.html`**: 5 riquadri («Cinque risultati»), ognuno con «Risultato N» e link `#pN`; `risultati.html`: «Cinque domande…».

## Prove (nel cloud)
- `python -m py_compile scripts/schede_risultati.py`: ok. `main()` con la scheda nuova e le altre finte: **nessuna riga ATTENZIONE** (frasi di al massimo 20 parole, 3 punti, 2 altri grafici, 4 limiti, 3 righe inglesi), anche con il JSON finto.
- Chromium (Playwright), `index.html` e `risultati.html`, 1440 e 390 px: **0 errori JavaScript**; 5 riquadri, 5 schede con numeri 1-5 nell'ordine giusto; scheda 5: 46 cerchi, retta di tendenza disegnata, 3 grafici (principale + 2), pulsante con `&vista=doppio`;
  `#r4` apre il Risultato 2, `#p4` il Risultato 4, `#r10` e `#p5` il Risultato 5, `#r1` il Risultato 1.
- Non verificato: le schede vere dei risultati 1, 4, 6, 8 (nel cloud ci sono solo schede finte).

## Da lanciare sul PC (Leo)
1. Se il JSON dell'script 95 non c'è: `python scripts\95_case_fragilita_servizi.py`.
2. `python scripts\schede_risultati.py`. Atteso: righe «forma» per i risultati 1, 4, 6, 8 e 10, **nessuna riga ATTENZIONE**, `scritto data\schede_risultati.js con 4 schede`… **con 5 schede**. Il titolo del risultato 10 dice «1 torinese su N» con N da 9 a 12 (circa 9-10% dei torinesi).
3. `python scripts\04_genera_mappa.py` (per `&vista=doppio`) e `python scripts\prova_pagine_r6.py`: 0 errori.
4. Aprire `index.html` (5 riquadri 1-5) e `risultati.html#p5`: grafico con la retta, pulsante «Vedi sulla mappa» che apre la vista «Doppio svantaggio». Controllare a occhio che le altre 4 schede siano come prima (cambia solo il numero in testa).
5. Se il README mostra «4 risultati» o i vecchi numeri: lo riscrive lo script 86 (da rivedere con Leo dopo questo giro).
