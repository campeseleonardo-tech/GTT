# Esito P0 — R6 rifatto con 5 feriali, scheda 5 controllata (22/10/2026)

Piano 3, punti 1 e 2 di `PIANO_RISULTATI.md`. Eseguito sul PC, ramo `prova`.

## Catena lanciata

- `RISULTATO6_RIFAI.bat` replicato a mano nello stesso ordine (71 → 85), log `logs/risultato6_rifai.log`.
  Il bat usa `pause`, quindi è stato lanciato passo per passo con lo stesso ordine e lo stesso log.
- Al passo 85 la verifica B ha fallito: la guida in `scripts/mappa_template.html` non aveva più «almeno 10 corse» e «almeno 1.000 auto» (a baseline passava). Leo ha dato la frase da aggiungere nel paragrafo «Parcheggi di scambio»; aggiunta, poi 85 rilanciato: **0 verifiche non superate**.
- `RIFAI_MAPPA_E_SCHEDE.bat` replicato a mano (04, schede_risultati, 86, prova_pagine_r6), log `logs/rifai_mappa_e_schede.log`: **0 errori**; prova pagine: **nessun errore a runtime sulle 18 pagine**.
- Avvisi nel log: velocità e sensori 5T con solo 2 sabati e 2 domeniche nello storico (media provvisoria). Non riguardano R6.

## 1. Riempimento: giorni feriali validi

- Prima: 3 feriali (15, 16, 19/10), etichetta [DATI SCARSI].
- Ora: **5 feriali** (15, 16, 19, 20, 21/10) più 2 giorni di fine settimana (17, 18/10).
- L'etichetta **[DATI SCARSI] resta**. Causa: nello script `scripts/71_parcheggi_riempimento.py` il testo «ANTEPRIMA [DATI SCARSI]» è scritto fisso (righe 246 e 262), non dipende dal numero di giorni. Decisione per Leo: 5 feriali di una sola settimana restano pochi. Il giro P8 (più settimane) deciderà se togliere l'etichetta.
- Cambia la classe di un parcheggio: **LANCIA** da «misto» a «residenziale». Molte letture per parcheggio cambiano di pochi punti; nessun parcheggio cambia di oltre il 20%.

## 2. Tabella prima / dopo R6

| Numero R6 | Prima | Dopo | Variazione |
|---|---|---|---|
| Fermate importanti | 274 | 274 | 0% |
| Fermate senza parcheggio (68) + posti insufficienti (111) | 179 | 179 | 0% |
| Fermate con posti sufficienti | 95 | 95 | 0% |
| Punti prioritari: bus conviene / dipende / non conviene | 0 / 1 / 11 | 0 / 1 / 11 | 0% |
| Minuti di pareggio, mediana punti prioritari | 20,85 – 27,5 | 20,85 – 27,5 | 0% |

Nessuna differenza sopra il 20%: nessun AVVISO da spiegare.

## 3. Scheda 5 «Case, servizi e fragilità» (`data/schede_risultati.js`)

- Titolo-risposta: «1 torinese su 11 vive dove la fragilità è alta e i servizi sono pochi».
- Numero grande: **79.598** residenti (in sezioni con fragilità alta e servizi bassi).
- Zone in doppio svantaggio: **5**: Mirafiori Sud, Lucento - Vallette, Rebaudengo - Regio Parco, Corona Nord, Barca - Bertolla (129.285 persone).
- Il segnaposto «12% di prova» non c'è più.
- Da verificare: la scheda scrive **9,5%** dei torinesi, mentre 79.598 / 848.748 residenti fa 9,4%. Il denominatore della percentuale nel testo va controllato nello script 95 (`scripts/95_case_fragilita_servizi.py`) prima di pubblicare. Non ho cambiato niente.

## 4. Da fare dopo

- Scheda 3 e scheda 5 da guardare in `risultati.html` (Leo).
- Etichetta [DATI SCARSI] dello script 71: decidere con più settimane di dati (giro P8).
- Denominatore del 9,5% nella scheda 5 (vedi sopra).
- R4 con un mese di dati (giro P5 del piano).
