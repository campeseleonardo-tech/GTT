# Risultato 2 — Metro di notte (in pausa)

**Domanda.** Quanti residenti guadagnano servizi raggiungibili in più, di notte, se la metro M1 facesse corse anche nel
buco notturno reale?

**Stato: in pausa.** Il numero conta i *servizi raggiungibili* di notte, non risponde alla domanda «uscendo la sera,
con la metro aperta, sarebbe più facile tornare a casa?»: di notte molti servizi (soprattutto i negozi) sono chiusi.
La scheda è nascosta da `risultati.html`; dati e script restano. **Tag:** [STIMATO] su orario programmato.

## Il buco notturno (GTFS reale, feriale di riferimento 12/10/2026)

- Metro (`METROU`): 05:22 → 22:02. Bus sostitutivo `M1SU`: 21:35 → circa 00:50.
- **Finestra senza metro né sostitutivo: 00:50 → 05:22.**

## Scenari e calcolo

- Script 28 copia il GTFS e aggiunge corse finte della metro solo nella finestra (stampino dell'ultima corsa vera di
  ogni direzione), valide solo il 12/10/2026: ogni 15 minuti (19 corse per direzione) o ogni 30 (10 corse). Uscite:
  `data/scenari/gtt_gtfs_notte15.zip` e `gtt_gtfs_notte30.zip`.
- `18_accessibilita.py` con `--gtfs` e `--out`: ore 01-04, circa 1 ora per ora simulata, circa 4 ore per scenario.
  `RISULTATO2_METRO_NOTTE.bat` cancella prima `data/processed/accessibilita_parziale/` (la firma dei parziali non
  contiene il percorso del GTFS e riuserebbe i numeri dello scenario precedente).
- **Metrica:** per ogni sezione, servizi raggiungibili con la metro di notte − servizi di base, sommato sulle 4 ore;
  «migliorata» = qualsiasi aumento. (Contare le sezioni che passano da zero servizi a più di zero non funziona:
  nessuna delle 8.317 sezioni è mai a zero di notte, minimo 2 servizi, per i bus notturni.)

## Numeri (`docs/rapporti/RAPPORTO_RISULTATO2_METRO_NOTTE.txt`)

| | Ogni 15' | Ogni 30' |
|---|---|---|
| Sezioni migliorate | 3.689 | 3.155 |
| Residenti con accesso migliorato | 773.307 | 652.891 |
| Con almeno +25% di servizi (numero in grande della scheda) | **334.085** | 153.062 |
| Delta totale servizi raggiungibili (città) | +51.935.040 | +27.215.916 |
| Delta mediano fra le migliorate (90° perc.) | 9.179 (33.289) | 3.436 (26.088) |
| Attesa media teorica | 7,5 min | 15 min |

3 sezioni mostrano un delta minimo negativo (circa −1): rumore del motore al margine del cutoff di 45 minuti.

## Limiti

- Orario programmato: nessun traffico, ritardo, capienza, domanda reale.
- «Servizi raggiungibili» è un conteggio di destinazioni entro 45 minuti, non una stima di passeggeri.
- Corse finte senza tempo di sosta alle fermate intermedie.
- Non dice quanti veicoli in meno girerebbero.

## Come riprenderlo

1. **Il popolo della notte** (IMQ 2022): spostamenti con partenza 00:00-05:00 (da dove, verso dove, con quale mezzo,
   per quale scopo). Pochi casi (indagine campionaria, residenti 11-84 anni, niente turisti): prima contare le
   interviste in quelle ore.
2. **Tornare a casa:** da 3-4 zone della vita notturna, tempo per tornare in ogni quartiere con e senza metro di notte
   (scenari `notte15`/`notte30` già calcolati).
3. Idea: incidenti di notte evitabili — i dati trovati (aperTO 2011-2017) sono vecchi e senza l'informazione sull'alcol.

## Script

`28_scenario_metro_notte.py`, `29_*` (numeri), `scripts\RISULTATO2_METRO_NOTTE.bat` (giro completo, molte ore),
`scripts\RISULTATO2_RICALCOLA_NUMERI.bat` (solo lo script 29, pochi secondi); riepilogo per la scheda in
`data/processed/risultato2_riepilogo_mappa.json`.
