# Piano e storia — Risultato 2 "metro di notte"

> ## IN PAUSA (Leo, 20/10/2026)
>
> **Perché.** La domanda vera di Leo era: «uscendo la sera, con la metro aperta, sarebbe più facile tornare a casa?».
> Il risultato invece conta i **servizi raggiungibili** di notte: è normale che con la metro aperta tanta gente ne
> raggiunga di più, ma di notte dorme e molti servizi (soprattutto i negozi) sono chiusi. Il numero non risponde
> alla domanda.
>
> **Decisione.** Scheda **nascosta** da `simulazione.html` e dal README finché non lo riprendiamo; dati e script
> (28, 29, `RISULTATO2_*.bat`) restano. Da fare (piccolo): togliere R2 dall'elenco delle schede in
> `schede_risultati.py` con un interruttore, non cancellandolo.
>
> **Come riprenderlo (ordine scelto da Leo).**
> 1. **Il popolo della notte** con l'IMQ 2022: spostamenti con partenza 00:00-05:00 (da dove, verso dove, con quale
>    mezzo, per quale scopo). Attenzione: pochi casi (indagine campionaria, residenti 11-84 anni, nessun turista o
>    visitatore). Controllo: quante interviste ci sono davvero in quelle ore, prima di fare qualsiasi calcolo.
> 2. **Tornare a casa**: da 3-4 zone della vita notturna (da scegliere con Leo, es. San Salvario, Vanchiglia, Quadrilatero,
>    Murazzi) il tempo per tornare a casa in ogni quartiere, con e senza la metro di notte (motore di accessibilità
>    già pronto, scenari `notte15`/`notte30` già calcolati). Risponde alla domanda di Leo.
> 3. **Solo idea**: incidenti di notte evitabili. Dati trovati: incidenti di aperTO 2011-2017, senza l'informazione
>    sull'alcol; troppo vecchi e senza la variabile che serve. Non si fa senza una fonte nuova.

Stato: **chiuso (v2) il 16/10/2026.** Numeri ufficiali in `docs/RAPPORTO_RISULTATO2_METRO_NOTTE.txt`,
scheda in `simulazione.html` (da `scripts/schede_risultati.py`). Dal 20/10 la scheda mostra anche il numero più severo
(almeno +25% di servizi: 334.085 residenti con la metro ogni 15 minuti, 153.062 ogni 30).
Qui stanno i dettagli; `MEMORIA_PROGETTO.md` ne tiene solo il riassunto.

## Domanda

Quanti residenti guadagnano servizi raggiungibili in più, di notte, se la metro M1 facesse corse anche
nel buco notturno reale?

## Il "buco vero" (verificato sul GTFS reale, giorno feriale di riferimento 12/10/2026)

- Metro vera (`route_id METROU`): servizio 05:22 → 22:02.
- Bus sostitutivo `M1SU` (route_type 3): 21:35 → ~00:50.
- **Finestra senza metro né sostitutivo: 00:50 → 05:22.** Non tutta la notte.
- File GTFS usato: `data/raw/gtt_gtfs_20261003_224530.zip` (lo stesso di `18_accessibilita.py`).

## Scenari (script 28)

`scripts/28_scenario_metro_notte.py` copia il GTFS e aggiunge corse finte della metro solo nella
finestra, valide solo il 12/10/2026 (`calendar_dates`, `calendar.txt` intatto):

- Stampino: l'ultima corsa vera di ciascuna direzione (stesse fermate, stessi offset di tempo).
- Prima partenza 00:50, poi ogni 15' o 30', ultima prima delle 05:22.
- Risultato: `data/scenari/gtt_gtfs_notte15.zip` (19 corse/direzione, 00:50→05:20) e
  `gtt_gtfs_notte30.zip` (10 corse/direzione). Identici all'originale tranne `trips`, `stop_times`,
  `calendar_dates`. Verificato file per file.

## Calcolo accessibilità (script 18, giro R5)

- `18_accessibilita.py` ha ora `--gtfs` e `--out` (patch minima; senza le due opzioni nulla cambia).
- Lanciato da `RISULTATO2_METRO_NOTTE.bat`: ore 01-04, giorno 2026-10-12, con `--salva-tappe`. ~1 ora
  per ora simulata, ~4 ore per scenario. Fuori da opencode, RAM controllata (PC 8 GB).
- **Bug trovato e aggirato (nel .bat, script 18 non toccato):** la "firma" dei parziali
  (`firma_run`) non contiene il percorso del GTFS e lo script non pulisce mai
  `data/processed/accessibilita_parziale/`. Senza pulizia, il secondo scenario avrebbe riusato i parziali
  del primo, dando numeri identici e sbagliati. Il .bat cancella la cartella prima di ogni lancio.

## Metrica: da v1 a v2

- **v1 (fallita):** "sezioni che passano da zero servizi a >0 nelle ore 01-04" → 0 / 0. Controllando i
  dati veri: nessuna delle 8.317 sezioni è mai a zero di notte (minimo 2 servizi), perché i bus
  notturni esistenti coprono già tutto. La metrica non può mai cambiare a Torino.
- **v2 (decisione di Leo, 16/10):** per ogni sezione, delta = servizi raggiungibili con la metro di notte
  − baseline, sommato sulle 4 ore. **"Migliorata" = qualsiasi aumento, anche di 1; nessuna soglia al
  calcolo.** Delta per sezione e per ora salvato in `risultato2_metro_notte.json` (`dettaglio`), così si
  può filtrare per rilevanza dopo senza ricalcolare.

## Numeri finali (v2, verificati: stesso risultato nel sandbox di Claude e sul PC di Leo)

| | Ogni 15' | Ogni 30' |
|---|---|---|
| Sezioni migliorate | 3.689 | 3.155 |
| Residenti con accesso migliorato | 773.307 | 652.891 |
| Delta totale servizi raggiungibili (città) | +51.935.040 | +27.215.916 |
| Delta mediano tra le migliorate (90° perc.) | 9.179 (33.289) | 3.436 (26.088) |
| Attesa media teorica | 7,5 min | 15 min |

3 sezioni mostrano un delta minimo negativo (~-1): rumore di R5 al margine del cutoff di 45 min.

## Limiti

- Orario programmato [PROGRAMMATO]/[STIMATO]: nessun traffico, ritardo, capienza, domanda reale.
- "Servizi raggiungibili" è un conteggio di destinazioni entro 45 min, non una stima di passeggeri.
- Corse finte con semplificazioni volute: nessun tempo di sosta alle fermate intermedie.
- Non risponde a "quanti veicoli in meno": serve una metodologia a parte (direzione futura trasversale).

## File

Script 28 e 29 (v2), patch a 18, `RISULTATO2_METRO_NOTTE.bat` (giro completo),
`RISULTATO2_RICALCOLA_NUMERI.bat` (solo script 29, pochi secondi), `risultato2_riepilogo_mappa.json`.

## Rimandato (non prioritario)

Elemento molto grafico (mappa) dentro `simulazione.html`, o fusione mappa+simulazione; ulteriori valori
nella scheda; filtro per rilevanza sul delta; stima dei veicoli in meno.
