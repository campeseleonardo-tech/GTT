# GT07-clic-fermate: rapporto

Modificato solo `scripts/mappa_template.html` (blocchi marcati `[agente GT07-clic-fermate]`). Non ho potuto eseguire nulla: non ho provato la pagina.

## Cosa ho fatto
- Sezioni di censimento e zone statistiche: niente più tooltip al passaggio del mouse, il cursore diventa una manina. Al clic si apre la scheda con le stesse informazioni del vecchio tooltip. Per le sezioni aggiunge il valore del tema attivo (rapporto/passaggi/densità). In Pendolari aggiunge anche la scheda del comune.
- Un clic vale solo se il rilascio è entro 5 px dal punto di pressione e non c'è un pizzico a due dita. Trascinare la mappa non apre nulla.
- La scheda resta aperta finché non si preme ×, Esc, o si clicca sulla mappa vuota. Cliccando un'altra sezione la scheda cambia. La sezione scelta ha un contorno nero sottile (1,5 px) finché la scheda è aperta.
- Fermate, mezzi, sensori 5T, linee in Velocità: il tooltip al passaggio è ridotto alle prime 2 righe. Il clic apre la scheda con il testo completo. Il vecchio tooltip del comune in Pendolari ora è nella scheda.
- Fermate: raggio circa il 60% di prima (max 3 px, prima 5), azzurro pieno `#4aa3df` semitrasparente con bordo blu scuro di 0,5 px, niente bianco. Aggiornati i due elementi della legenda. Il raggio di hit-test resta 8 px.

## Scelte
- Scheda: `position:fixed`, a destra, 190 px dall'alto (sotto i pulsanti di zoom), larghezza max 300 px (o larghezza finestra − 24 px), scorre se è lunga.
- Il testo della scheda è una fotografia al momento del clic: se cambi ora o giorno, non si aggiorna finché non clicchi di nuovo.
- Ho rinominato la funzione `mostraTip` in `mostraTipBase`. Era usata solo in `cercaTip`.
- Doppio clic = zoom, ma apre anche la scheda con il primo clic.

## Da provare
1. Passa il mouse su una sezione: non appare nulla, il cursore diventa una manina.
2. Clicca: si apre la scheda in alto a destra e la sezione ha il contorno. Clicca un'altra sezione: la scheda cambia.
3. Trascina la mappa: la scheda non si apre (se era già aperta, resta).
4. Premi Esc, ×, o clicca fuori da ogni sezione: la scheda si chiude e il contorno sparisce.
5. Attiva Fermate e porta lo zoom tra 14 e 17: punti azzurri più piccoli, senza bordo bianco. Passaggio del mouse = 2 righe, clic = scheda.
6. Tema Pendolari: clicca un comune o una sezione. Tema Velocità: clicca una linea.
7. Controlla anche mezzi e sensori 5T.
