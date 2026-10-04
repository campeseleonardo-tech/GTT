# Rapporto GT05-pendolari

## Cosa ho fatto
- `scripts/04_genera_mappa.py` (blocchi `# [agente GT05-pendolari]`):
  - `leggi_matrice_pendolari`: apre lo zip (prende il file di testo più grande), prova utf-8 poi latin-1, riconosce il separatore (atteso tab), trova da sola la riga di intestazione e le colonne (per nome "PROV"/"COM"; altrimenti per posizione: prov.res, com.res, prov.dest, com.dest, numero). Codice = provincia*1000 + comune (se il comune è già ≥ 1000 lo usa com'è). Stampa intestazione, colonne usate, righe scartate, totale persone, flussi di Torino e valori attesi, con un ATTENZIONE se si scostano oltre il 5%.
  - `costruisci_pendolari`: per ogni comune presente nelle sezioni (`c`): abitanti, baricentro pesato con gli abitanti (centro del riquadro di ogni sezione, pesato per abitanti), entrano a Torino / escono, lavoro e studio. Flussi dei comuni fuori area sommati in "altri comuni" (con il numero di comuni). Torino a parte, con il flusso interno. Se mancano gli zip (o sono illeggibili) stampa un avviso e va avanti: la mappa si genera lo stesso, esce 0.
  - Le sezioni incorporate hanno ora anche `c` (PRO_COM).
- `scripts/mappa_template.html`: nuovo tema **Pendolari** (ultimo pulsante): sezioni colorate col valore del loro comune, linee dritte dal baricentro di ogni comune a Torino (spessore ∝ flusso, primi 30 comuni), tre selettori (Lavoro/Studio/Entrambi, Entrano/Escono, colore "ogni 1000 abitanti"/"numero di persone"), scheda del comune al passaggio del mouse o al tocco, legenda con tag CENSIMENTO, testo "ISTAT 2021, comune→comune, senza mezzo né orario; studio = stima", riepilogo (primi 30, altri comuni dell'area, fuori area) e flusso interno Torino→Torino come numero (nessuna linea).

## Cosa ho controllato
Non posso eseguire nulla: non ho verificato io i totali. Al lancio di 04 la console stampa i valori reali; attesi dalle note: lavoro entrano 138.605, escono 71.297, dentro 212.249; studio entrano 48.730, escono 6.373, dentro 120.148. Se lo scostamento è > 5% compare "ATTENZIONE": vorrebbe dire colonne lette male (es. residenza e destinazione scambiate).

## Scelte
- Colore di default: "ogni 1000 abitanti"; direzione di default: Entrano; Lavoro.
- Soglie colore = quintili sui comuni con flusso > 0 (ricalcolate a ogni cambio di scelta).
- Torino e comuni senza flusso: grigio. Nessuna freccia, solo colore: viola = entrano, arancio = escono.
- Nomi dei comuni: nel progetto non c'è la tabella ISTAT dei codici, quindi la scheda mostra "Comune 00XXXX" (codice PRO_COM a 6 cifre); solo Torino ha il nome.
- Il "click" è il tooltip già esistente (mouse: passaggio; touch: tocco).

## Limiti
- Gli abitanti del comune sono la somma delle sezioni incluse nella mappa (entro 18 km da Torino): per i comuni di confine dell'area possono essere parziali, quindi "ogni 1000 abitanti" può risultare gonfiato. Con "numero di persone" il problema non c'è.
- Il baricentro è il centro del riquadro di ogni sezione, pesato con gli abitanti: approssimato.
- Studio = stima da modello ISTAT; flussi comune→comune, niente mezzo né orario né zone dentro Torino.
- Non testato né eseguito da me.

## Da cliccare per provare
1. Rilancia `04_genera_mappa.py` e leggi nel log le righe "lavoro"/"studio" (colonne, totali, eventuale ATTENZIONE).
2. Apri `mappa_torino.html`, tema **Pendolari**: compaiono 3 menu sotto la descrizione.
3. Cambia Lavoro / Studio / Entrambi, Entrano / Escono, colore: aree, linee e legenda cambiano.
4. Passa il mouse su un comune: codice, residenti, entrano/escono. Su Torino: flusso interno.
5. Controlla che gli altri temi funzionino come prima (cambiando tema i menu spariscono).

## Suggerimenti per la scheda di progetto (Leo)
- Aggiungere il tema Pendolari alla sezione Mappa; scaricare la tabella ISTAT dei codici comune per avere i nomi.
