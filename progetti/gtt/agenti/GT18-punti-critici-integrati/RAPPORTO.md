# Rapporto GT18 – punti critici integrati

## Cosa ho fatto (solo `scripts/mappa_template.html`; `04_genera_mappa.py` non serviva toccarlo)
- **Indice di criticità 0–100** per ogni sezione di censimento e per ogni ora/giorno (funzione `critSez`). Si basa sul rapporto già usato dalla mappa: passaggi GTT programmati/ora entro 400 m ogni 1000 residenti entro 400 m.
  - 100 = nessun passaggio programmato (con residenti); 80 o più = il peggior quinto delle sezioni (soglie dei quintili già calcolate per le ore 7–20); 0 = tra le meglio servite.
  - Sezioni senza residenti: nessun indice.
- **Nei 4 temi, senza nuovi menu**: ogni tema ha un **contorno rosso** sulle sezioni con indice ≥ 80, che segue giorno e ora scelti. Nel tema «Servizio e abitanti» la voce «Indice di servizio» è rinominata «Criticità (poca offerta per abitante in rosso)» e la legenda dice «critico / ok».
- **Scheda unica (GT17)**: nella scheda sezione c'è la riga «Indice di criticità» (nel modo Criticità è anche il valore grande, «Criticità 87/100»), con spiegazione nell'approfondimento. Nel tema Pendolarismo la scheda del comune mostra la criticità della sezione cliccata.
- **Clic** nei temi Traffico e Tempo reale (dove non c'è area colorata): rispondono solo le sezioni col contorno rosso e aprono la scheda con il valore.
- Legenda: aggiunto blocco «Zone critiche» con etichette PROGRAMMATO + CENSIMENTO e la dicitura «stima».

## Scelte
- Indice relativo (quintili), non soglia assoluta: «80» significa «tra le peggiori dell'area», non «servizio insufficiente» in senso assoluto.
- Domanda = solo residenti ISTAT 2021 (non pendolari): scelta prudente, i pendolari 2021 sono solo comune→comune.
- Di notte (fuori 7–20) quasi tutte le sezioni risultano 100: è corretto (niente passaggi), ma il contorno rosso sarà quasi ovunque.
- Fuori Torino mancano altri operatori e treni: il rosso può essere mancanza di dati (già avvisato nelle note).

## Da provare (Leo)
1. Apri la mappa, tema «Servizio e abitanti» → contorni rossi sulle sezioni rosse. Cambia ora e giorno: i contorni cambiano.
2. Clicca una sezione: la scheda mostra «Criticità NN/100».
3. Passa a «Traffico e velocità», «Tempo reale e flotta», «Pendolarismo»: contorno rosso presente; nei primi due, clicca dentro un contorno rosso per la scheda.
4. Nelle altre scelte («Solo offerta», «Solo residenti») la scheda riporta comunque la riga criticità.

Nessuna verifica eseguita da me (non posso lanciare programmi): attendere il validatore.

## Per il foglio di progetto (suggerimento)
Aggiungere: «Indice di criticità 0–100 per sezione (poca offerta programmata per residenti), contorno rosso ≥ 80 in tutti i temi».
