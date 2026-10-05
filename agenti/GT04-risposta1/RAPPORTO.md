# Rapporto GT04-risposta1

## Cosa ho fatto
Applicata la risposta di Leo alla domanda del task GT04-velocita:
«Soglie colori velocità (12/16/20 km/h) vanno bene?» → **«A tenere»**.
La risposta conferma le soglie già presenti nel codice, quindi **non ho modificato nessun file** (né `scripts/mappa_template.html` né `scripts/04_genera_mappa.py`): «tenere» = lasciare intatto ciò che c'è.

## Cosa ho controllato
- `scripts/mappa_template.html`: `const velClasse = k => k<12?0 : k<16?1 : k<20?2 : 3;` → soglie 12 / 16 / 20 km/h, esattamente quelle citate nella domanda.
- `legendaVelocita()`: etichette `<12`, `12–16`, `16–20`, `>20 km/h` coerenti con i 4 colori di `VEL_PAL` (rosso, arancio, giallo, verde) + grigio per nessun dato o meno di `VEL_MIN_CAMP` (20) campioni.
- `scripts/04_genera_mappa.py` → `calcola_velocita()`: produce `D.vel[linea][tipo][ora]=[km/h, campioni, giorni]`; le soglie di colore stanno solo nel template, lo script non le usa → non va toccato.

## Scelte
- Nessuna scelta nuova: la risposta «A tenere» conferma le soglie 12/16/20 già implementate. Niente da decidere, niente domande.

## Da testare (per Leo)
- Niente di nuovo da provare: apri `mappa_torino.html`, scegli il tema «Velocità» in alto e passa il mouse su una linea; i colori restano <12 rosso, 12–16 arancio, 16–20 giallo, >20 verde.

## Per Leo
- Niente da rivedere: le soglie restano 12/16/20 km/h, come hai deciso. La decisione è già nella lista «Decisioni del progetto».
