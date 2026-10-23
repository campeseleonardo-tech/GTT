# Esito del giro L11 (24/10/2026): mappa pulita

Scelte di Claude (Leo le ha lasciate a lui), applicate come nel blocco L11:

- **La mappa parte come prima** (satellite, nessun tema), con **3 viste consigliate** in cima al pannello, un clic ciascuna: «Fragili e con pochi servizi» (tema Fragilità sociale, vista Doppio svantaggio), «Ritardi delle linee alle 8» (tema Ritardi, ora 8), «Dove lasciare l'auto» (tema Parcheggi di scambio). Usano gli stessi indirizzi `#tema=…` delle schede. Se si sceglie un altro tema dal menu e poi si ricliccca la stessa vista, funziona lo stesso (l'indirizzo non cambia, la vista viene riapplicata). Sul telefono il clic richiude il foglio, così si vede la mappa.
- **«Chi abita qui» da 8 a 3 viste**: densità, anziani, persone sole. Tolte dal pannello e dal codice del template giovani, età media, laureati, occupati, persone per famiglia (valori, testi, nomi, scale di colore, totali di Torino, campi delle sezioni). Il profilo della zona ha ora 2 barre (anziani, persone sole). Nello script 04 non si esportano più le colonne `f, occ, p1564, p014, em, ist9, it` (nessun altro tema le usa); restano `sen, pf1, pf3` per anziani e persone sole.
- **Via «Copia il link di questa vista»**: tolti il pulsante, `costruisciLink` e il suo codice. `git grep copiaLink costruisciLink` fuori da `sviluppo/` non trova niente. Gli indirizzi si leggono ancora (tema, vista, linea, ora, giorno, anche zoom e centro dei vecchi link copiati).
- **«Vedi sulla mappa» anche nella scheda 4**: tema «Spostamenti» (nessun tema mostra l'area che si espande; nessun tema nuovo, come da regola). Nessun altro tema è stato tolto.

## Peso di `mappa_torino.html`
Prima 6.098.893 byte (circa 6,1 MB), dopo 5.906.557 byte (5,9 MB): non cresce, scende di circa 190 KB.

## Controlli
pyflakes zero; `schede_risultati.py` senza ATTENZIONE; `prova_pagine.py --playwright`: 0 errori su 20 pagine. Prova nuova in `prova_pagine.py` (`prova_link_mappa`): apre i 5 «Vedi sulla mappa» delle schede (scheda 4 compresa) e le 3 viste consigliate e legge nel DOM menu dei temi, vista (`vuln_doppio`, `parcheggi`/`mancano`) e ora (08:00); clicca le viste consigliate anche con indirizzo già uguale: 8 indirizzi, tutti OK. Non fatto: controllo grafico (lo fa Leo).
