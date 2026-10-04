# GT02-temi — Rapporto

Modificato solo `scripts/mappa_template.html` (blocchi marcati `[agente GT02-temi]`). Non ho potuto eseguire nulla: il controllo lo fa il runner.

## Cosa ho fatto
- Il blocco «Livelli» è sostituito da **Tema** (8 pulsanti grandi, uno attivo) + **Sovrapposizioni** (6 caselle: Linee, Fermate, Corse simulate, Mezzi reali, Sensori 5T, Replay).
- Scegliere un tema imposta area colorata e sovrapposizioni al suo preset; poi le caselle si possono cambiare a mano.
- Sezioni e zone non possono essere accese insieme: le caselle interne `Lsez`/`Lzone`/`modoSez` sono nascoste e le decide solo il tema.
- Legenda: mostra solo il tema attivo e le sovrapposizioni accese, con etichette MISURATO / PROGRAMMATO / STIMATO/SIMULATO / CENSIMENTO e «dati scarsi» (storico < 72 h, stessa regola di «Dati raccolti») su sensori, replay e linee «reali/previsto».
- Riempimenti area a 0.5 di trasparenza (prima 0.62-0.66), contorni più sottili.
- Tema di partenza: Offerta.
- Prestazioni: cambiare tema non ricalcola nulla di pesante (soglie e griglie sono già pronte); si ridisegna soltanto la base.

## Tabella dei temi (`THEMES`, in fondo allo script, sopra `aggiornaLegenda`)
| id | Etichetta | Area colorata | Sovrapposizioni accese | Note |
|---|---|---|---|---|
| nessuno | Nessuno | — | nessuna | solo sfondo |
| offerta | Offerta | sezioni: passaggi/ora entro 400 m | Linee, Fermate | tema di partenza |
| domanda | Domanda | sezioni: abitanti per km² | nessuna | |
| rapporto | Poca offerta per abitante | sezioni: rapporto esistente | Linee (spessore dimezzato) | |
| zone | Zone statistiche | 94 zone: passaggi/ora per km² | nessuna | al posto delle sezioni |
| traffico | Traffico | — | Sensori 5T (marcatori ×1,5) | senza dati live: «Nessun dato live: riavvia la raccolta.» |
| tempo | Tempo reale | — | Mezzi reali, Corse simulate | mostra «Segnalazioni adesso» |

Per aggiungere «Velocità» o «Pendolari»: una riga in `THEMES` (id, label, desc, area, over, legenda). Se serve una nuova area colorata va aggiunta anche in `disegnaBase` (oggi gestisce `Lsez` e `Lzone`).

## Cosa si è spostato
- Replay: dalla sezione «Dati raccolti» a «Sovrapposizioni» (resta il menu della giornata).
- «Segnalazioni adesso»: visibile solo nei temi Traffico e Tempo reale (negli altri è nascosta, non rimossa).
- Menu «Poca offerta / Passaggi / Abitanti» (`modoSez`): ora lo sceglie il tema.
- Rimane in «Sfondo e filtro»: filtro linea e menu «Come colorare le linee» (freq / mezzi reali rispetto al previsto).

## Scelte
- «Segnalazioni adesso» visibile anche nel tema Traffico (parla di traffico lento).
- Tempo reale: Linee e Fermate spente, per far vedere i mezzi.
- «Nessun veicolo/dati scarsi»: «dati scarsi» compare anche quando lo storico manca del tutto.
- Dopo ogni aggiornamento live (30 s) la legenda si ricostruisce (serve per il messaggio «nessun dato live»).

## Da testare (clic)
1. Apri `mappa_torino.html`: deve partire il tema **Offerta** (sezioni semitrasparenti, linee, fermate da zoom 14), legenda con PROGRAMMATO.
2. Clic su **Nessuno**: solo sfondo, nessuna legenda. Poi spunta «Linee»: compare la sua legenda.
3. **Domanda**: sezioni per abitanti, legenda CENSIMENTO, nessuna linea.
4. **Poca offerta per abitante**: scala rosso→verde, linee più sottili, legenda PROGRAMMATO + CENSIMENTO.
5. **Zone statistiche**: le sezioni spariscono, appaiono le 94 zone (mai entrambe).
6. **Traffico**: solo sensori, più grandi; passa il mouse su uno per il tooltip; riquadro «Segnalazioni adesso» visibile. Con la raccolta ferma deve apparire «Nessun dato live: riavvia la raccolta.»
7. **Tempo reale**: puntini neri (mezzi reali) e puntini piccoli (corse simulate, STIMATO/SIMULATO); in legenda MISURATO per i primi.
8. Dopo un tema, spunta/togli a mano ogni casella (Linee, Fermate, Corse, Mezzi, Sensori) e controlla che legenda e mappa seguano.
9. **Replay**: scegli una giornata dal menu (si accende da solo) oppure spunta «Replay»; legenda MISURATO.
10. Cambia Feriale/Sabato/Domenica e lo slider ora: l'area deve aggiornarsi; cambia sfondo/intensità: nessuna regressione.
11. In «Sfondo e filtro», «Linee: mezzi reali rispetto al previsto» con Linee accese: legenda con «dati scarsi» se lo storico è < 72 h.
