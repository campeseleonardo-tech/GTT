# Esito: case × fragilità × servizi (parte E di PIANO_RISULTATI), sessione cloud

Scritto nel cloud, senza `data/`: **lo script 95 non è stato lanciato sui dati veri**. Provato con dati finti (`--prova`) e con i dati dentro
`mappa_torino.html` (sezioni, indice di vulnerabilità, servizi a piedi, zone OMI, fermate M1 decodificati con le funzioni del 04), per vedere che i numeri abbiano senso.
Il ramo è stato unito con `origin/prova` (mappa rigenerata) e con `origin/claude/vibrant-planck-cztsh9`.

## Cosa c'è
- `scripts/95_case_fragilita_servizi.py` (sola lettura; prossimo numero libero **96**). Legge `sezioni_torino.json` (05: `id`, `c`, `p`, `a`, `g`), `vulnerabilita.json` (19: `sezioni[].v`, `tipo`, `c`),
  `accessibilita.json` (18: `piedi.15` per gruppo), `omi_zone.json` (08: zone di Torino `c` = 1272, prezzo = centro della forbice `v.ab[0..1]`) e le fermate con `route_type` 1 del GTFS più recente.
  Scrive `data/processed/case_fragilita_servizi.json` e `docs/rapporti/RAPPORTO_CASE_FRAGILITA_SERVIZI.txt`. Opzioni: `--prova` (dati finti, cartella temporanea), `--radice CARTELLA`.
- «Tutti i servizi» a piedi: come la mappa (percentile a posizione media per gruppo fra le sezioni di Torino abitate, valore mancante = 0, media dei 5 × 100).
- Sezione → zona OMI: centro del riquadro della sezione dentro un anello della zona (a parità, l'anello più piccolo). Valori di zona: media pesata per abitanti. Fuori le zone sotto 500 abitanti.
- **E1** Spearman (con intervallo al 95% per ricampionamento, seme fisso), retta prezzo-servizi, residui, 5 zone più care e 5 più convenienti. **E2** zone e sezioni con fragilità nel 20% più alto e servizi nel 20% più basso (soglie nel codice,
  fissate prima dei numeri; per le sezioni, quintili delle sezioni di Torino abitate fuori dalle zone grigie sotto 1.000 ab/km², come la mappa). **E3** zone con una fermata M1 entro 600 m dal centro della zona (centroide dell'anello più grande) contro le altre, fasce di 2 km da Piazza Castello; sempre scritto «differenza fra zone, non effetto causale».
- Controlli: abitanti che tornano (bloccante), nessun prezzo nullo (bloccante), sezioni senza zona OMI (AVVISO oltre l'1%), indice di vulnerabilità senza servizi (altrimenti il confronto è circolare), fermate M1 trovate (AVVISO sotto 15). Nessun dato sulla nazionalità.
- **Mappa**: nel tema «Fragilità sociale» la vista «Doppio svantaggio (fragili e con pochi servizi)». Calcolata nel browser da `v` e dal punteggio «Tutti i servizi» già in mappa: 4 colori (rosso scuro tutte e due, arancio solo fragilità alta, blu solo servizi bassi, verde chiaro nessuna), grigio per le zone poco abitate come le altre viste e per la cintura (i suoi servizi vengono da OpenStreetMap), legenda con le soglie scritte, tooltip e scheda con la classe.
- `scripts/prove/dati_da_mappa_95.py`: ricostruisce da `mappa_torino.html` i file nel formato vero, per provare il 95 senza `data/`.

## Prove (nel cloud)
- `python -m py_compile` sullo script e sul tool di prova: ok. `--prova`: 24 zone, 2 escluse (una sotto 500 abitanti, una senza prezzo), controlli come previsto.
- Dati della mappa (indicativi: forme semplificate a 4 decimali): 4.044 sezioni di Torino, **848.748 abitanti (torna con il censimento)**, 1 sezione senza zona (0,02%), 46 zone usate su 47 (esclusa B9 Stati Uniti, sotto 500 abitanti), 23 fermate M1.
  **E1** Spearman 0,61 su 46 zone (intervallo 95% 0,39-0,79); più convenienti dei servizi: Barriera di Milano, Rebaudengo - Regio Parco, Porta Palazzo, Campidoglio - Martinetto, Spina 4; più care: Roma, Crimea, Carlo Emanuele II, Villa della Regina, Valentino.
  **E2** 5 zone in doppio svantaggio (Mirafiori Sud, Lucento - Vallette, Rebaudengo, Corona Nord, Barca - Bertolla): 129.285 residenti (15,2%); per sezione **79.598 torinesi (9,5%)** in 216 sezioni.
  **E3** fasce 0-2 / 2-4 / 4-6 km: con metro +73 / +219 / +52 €/m² sulle zone senza (poche zone con metro: 6, 3, 2): differenza piccola, solo fra zone. Questi numeri valgono solo per la prova: i veri escono dal lancio sul PC.
- Mappa con il template nuovo in Playwright/Chromium: tutti i 12 temi, a 1440 px e a 390 px, **0 errori JavaScript**. La vista nuova ha le 4 classi con i 4 colori e la legenda con le soglie (indice sopra 57,7; servizi fino a 34,4 su 100); le classi contate nel browser
  (2.332 / 489 / 483 / 216 sezioni; 79.598 residenti in doppio svantaggio) sono **identiche** a quelle dello script 95 sugli stessi dati. Clic e passaggio del mouse sulla sezione: classe e valori.

## Da lanciare sul PC (Leo)
1. `python scripts\95_case_fragilita_servizi.py`. Atteso: controlli senza ERRORE; AVVISO solo se le sezioni senza zona OMI superano l'1% o se mancano zone con prezzo; circa 46 zone usate, 23 fermate M1, abitanti di Torino 848.748; rapporto in `docs/rapporti/RAPPORTO_CASE_FRAGILITA_SERVIZI.txt`.
   Ordini di grandezza (da confermare con le forme vere): Spearman fra 0,5 e 0,7; qualche migliaio fino a poche decine di migliaia di residenti per zona in doppio svantaggio; 70-90 mila torinesi in sezioni con entrambe le condizioni.
2. `python scripts\04_genera_mappa.py` (o `scripts\RIFAI_MAPPA_E_SCHEDE.bat`): nel tema «Fragilità sociale» scegliere «Doppio svantaggio»: 4 colori, la cintura in grigio.
3. `python scripts\prova_pagine_r6.py`: 0 errori.
4. Ricontrollo: i numeri della legenda (soglie 57,7 e 34,4 sui dati di oggi) devono coincidere con quelli del rapporto (`sezioni.soglia_fragilita_sopra`, `soglia_servizi_fino_a`).
Non fatto: scheda in `risultati.html` (il piano dice che il risultato esce solo se E1-E2 dicono qualcosa di chiaro: da decidere con Leo dopo il lancio vero).
