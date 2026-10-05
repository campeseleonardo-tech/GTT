# GT08 – griglia in metri e barra della scala

Modificato solo `scripts/mappa_template.html` (blocchi marcati `[agente GT08-griglia-scala]`). Non testato: non posso eseguire programmi.

## Cosa ho fatto
- **Griglia quadrata in metri**, disegnata in `disegnaBase`, subito dopo lo sfondo e prima di zone/sezioni/linee/fermate. Sta nel livello in cache: nessun lavoro in più mentre si trascina senza cambiare vista.
- **Barra della scala** (HTML, `#scala`) in basso a sinistra, con lunghezza tonda e testo, più "griglia: X" accanto.
- **Casella "Griglia in metri"** in "Sfondo e filtro", accesa di default. La barra è sempre visibile.

## Come si calcolano i metri
`metri per pixel = 40.075.016,7 × cos(latitudine) / (256 × 2^zoom)`.
- Barra: usa la latitudine del centro della vista.
- Griglia: usa fissa la latitudine di Torino (45,0703°) e parte dal centro di Torino. Così la griglia non "scivola" quando si trascina; l'errore rispetto alla barra è < 0,5% entro 18 km.

## Misure per zoom
Si sceglie il passo più piccolo con cella ≥ 40 px (quindi 40–100 px). Circa, a Torino:
| zoom | m/px | passo |
|---|---|---|
| 9 | 216 | 10 km (46 px) |
| 10 | 108 | 5 km (46 px) |
| 11 | 54 | 5 km (92 px) |
| 12 | 27 | 2 km (74 px) |
| 13 | 13,5 | 1 km (74 px) |
| 14 | 6,8 | 500 m (74 px) |
| 15 | 3,4 | 250 m (74 px) |
| 16 | 1,7 | 100 m (59 px) |
| 17 | 0,84 | 100 m (119 px) |
| 18 | 0,42 | 50 m (119 px) |

Barra: lunghezza tonda più grande (10 m … 50 km) che non supera 140 px.

## Colori
Due linee affiancate da 1 px: scura `rgba(70,70,70,.22)` e chiara `rgba(255,255,255,.28)` (spostata di 1 px). Così si legge sia sul satellite scuro sia su "Mappa chiara". Il solo grigio `rgba(150,150,150,.25)` sarebbe quasi invisibile sul satellite, quindi ho cambiato. Non ho potuto vederlo: da giudicare a occhio.

## Scelte
- Oltre i passi richiesti ho aggiunto 10, 25 e 50 m per gli zoom alti (altrimenti a zoom 17-18 le celle superano 120 px).
- Barra: a sinistra (12 px); se il pannello copre l'angolo in basso a sinistra, va a destra del pannello, o in basso al centro se non c'è spazio.
- La posizione della barra si aggiorna a ogni ridisegno, non quando si apre/chiude il pannello (basta muovere o zoomare).

## Da provare (clic)
1. Zoom con + / − o rotella: la dimensione delle celle e la barra cambiano; il testo "griglia: …" segue.
2. Togli la spunta "Griglia in metri": le linee spariscono, la barra resta (senza "griglia: …").
3. Cambia sfondo (Satellite, Mappa chiara, Stradale, Nessuno): controlla che le linee si vedano.
4. Misura Piazza Castello – Porta Nuova (≈ 1,2 km) con la barra o contando le celle da 500 m / 250 m.
5. Apri/chiudi il pannello (×, poi riapri): la barra non deve restare sotto il pannello.
6. Attiva zone/sezioni: la griglia deve restare sotto i colori.
