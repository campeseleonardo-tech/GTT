# Esito — Risultato 1, versione 2, fase A (passi meccanici)

Sessione cloud, ramo `claude/practical-lamport-5laaug` (AGENTS.md: nel cloud si resta sul ramo della sessione). Prima di cominciare ho portato il ramo allo stesso punto di `origin/prova` (`git merge --ff-only`, nessun conflitto, nessuna modifica locale). Python 3.13 del cloud, non Anaconda.
**Nel cloud non ci sono `data/`, il Pi, r5py né geopandas**: fatte solo le modifiche al codice; i passi che lanciano gli script sui dati (5) sono **DA FARE da Leo sul PC**. `MEMORIA_PROGETTO.md` non toccata.

Prova fatta qui: gli script 21 e `scheda_r1` girano su **dati finti** costruiti con la stessa struttura di `accessibilita.json` e `sezioni_torino.json` (in una cartella di prova fuori dal progetto): somme corrette, nessun errore. I numeri di quella prova non hanno alcun significato e non sono riportati qui.

| Passo | Esito |
|---|---|
| 1 Ramo / git | OK (vedi nota sopra) |
| 2 Script 21: sezione `v2` e «VERSIONE 2» | OK (provato su dati finti) |
| 3 Script 22: solo sezioni abitate | OK (provato fino al calcolo R5, che qui non gira) |
| 4 `scheda_r1` | OK (provato su dati finti) |
| 5 Lanciare gli script | **DA FARE da Leo sul PC** |
| 6 Esito, righe, git status | OK per le righe; numeri veri da aggiungere dopo il passo 5 |

## Campi controllati sul codice vero (piano e file combaciano)
- `accessibilita.json`: sezioni con `id`, `res`, `piedi["15"][gruppo]`, `tp["08"][gruppo]` (conteggi per gruppo, da `18_accessibilita.py`): **uguale al piano**, nessuna lista rinominata.
- `sezioni_torino.json`: lista di sezioni con `id` e `a` = superficie in **km²** (da `05_prepara_sezioni.py`): uguale al piano.
- Sezione senza `tp["08"]`: non prevista dal piano; il codice usa solo il piedi per quella sezione e la conta nel controllo («sezioni di cintura senza mezzo pubblico»).

## PASSO 2 — `scripts/21_risultato1_vuoti.py`: OK (solo aggiunte)
Le uscite di oggi non cambiano: nel JSON si aggiunge la chiave `"v2"` (le altre restano), nel rapporto si aggiunge in coda la sezione «VERSIONE 2» (il testo di prima è identico).
Aggiunto:
- docstring: paragrafo «VERSIONE 2»; costanti `SEZIONI_GEO`, `SOGLIA_POCO_ABITATA = 1000`, `SENSIBILITA_SOGLIA = (500, 2000)`, `SOGLIA_TITOLO = 3`, `ORA_TP = "08"`, `GRUPPI_TP_CINTURA = {scuole, salute, cibo}`, `MAX_SENZA_SUPERFICIE = 10`.
- funzioni nuove: `carica_superfici()`, `densita()`, `n_mancanti_sezione()`, `riepilogo_ambito()`, `calcola_v2()`, `righe_rapporto_v2()`.
- `main()`: dopo `esito = {…}` → `esito["v2"] = …` e stampa dei controlli; prima di scrivere il rapporto → `righe += righe_rapporto_v2(...)`.
Regole (come da piano): `n_mancanti` = gruppi a zero a piedi in 15 min; cintura: scuole/salute/cibo mancano solo se zero a piedi **e** zero col mezzo pubblico entro 45 min alle 08; fermate e verde come Torino; Torino = id che inizia per `1272`; densità = residenti / `a`; titolo = residenti abitati di Torino con `n_mancanti >= 3`; riga «tutti e 5»; zone poco abitate a parte; sensibilità 500 / 1.000 / 2.000.
Scelte mie (valori predefiniti dichiarati):
- Sezione senza superficie: conta come **abitata** (e si conta nel controllo; AVVISO se più di 10).
- In più, per confronto, la cintura con la regola di oggi (solo a piedi): serve per la tabella «fuori Torino 3+ mancanti» del piano.
- `v2.sezioni`: per ogni sezione `n_mancanti` e `densita`, pronte per la mappa (fase B).
- `v2.soglia_titolo_n_mancanti`: la soglia 3 viene dal JSON, così la scheda non la scrive a mano.
Controlli stampati (OK/AVVISO): somma dei residenti per `n_mancanti` = residenti dell'ambito (per Torino e cintura, a ogni soglia); densità negative; sezioni senza superficie; sezioni di cintura senza TP.

## PASSO 3 — `scripts/22_risultato1_candidati.py`: OK
- Importa da `21` la soglia e le funzioni di densità (un solo posto dove cambiarle).
- Nuovo `--soglia-densita` (default = `SOGLIA_POCO_ABITATA`). Le sezioni a zero sotto soglia non fanno candidati e non contano nei «residenti a zero» (`zero_ids_g`). Le origini dei calcoli R5 restano tutte le sezioni di Torino.
- Il JSON ha `filtro_abitate` per gruppo; il rapporto una riga per gruppo «sezioni a zero A → B, residenti a zero A → B, zone candidate A → B» (**serve per dire quanti candidati cambiano: i numeri veri arrivano dal passo 5**). In `parametri` aggiunta `soglia_densita_ab_km2`.

## PASSO 4 — `scripts/schede_risultati.py`, `scheda_r1`: OK
- Il numero in grande = residenti abitati con 3+ mancanti, letto da `risultato1_vuoti.json → v2` (nessun numero scritto a mano; anche la soglia 3 e la soglia 1.000 vengono dal JSON). Serve aver rilanciato prima lo script 21: altrimenti `KeyError: 'v2'` (voluto, meglio che un numero vecchio).
- «cibo» → «negozi e attività commerciali» in titolo, etichette, metodo, limiti e inglese (costante `NOMI_R1`, `GRUPPI_EN["cibo"]` = «shops and commercial activities»).
- Nuovo grafico a barre «Residenti per numero di servizi mancanti (0-5), zone abitate» (primo della lista); nuove righe nei numeri «Oggi»: residenti zone poco abitate, tutti e 5 mancanti; la risposta ha le frasi nuove (titolo, tutti e 5, zone poco abitate) e **resta** la frase vecchia «almeno uno dei 5» (aggiungo, non tolgo).
- Nuovo campo `criteri` (la pagina lo mostra già): zona poco abitata con la sensibilità 500/1.000/2.000, titolo, cintura a parte. In `parametri` la riga «Zona poco abitata».
- Limiti: aggiunti «capienza di ospedali, presidi e scuole non nota» e «orario programmato / sezioni senza superficie».
- `in_english`: domanda, titolo e sensibilità aggiornati con gli stessi numeri.
Non toccato: `mappa_torino` (fase B, lavoro 4), `MEMORIA_PROGETTO.md`.

## PASSO 5 — fatto da Leo sul PC il 20/10 (commit «Risultato 1 v2: calcoli sul PC»); numeri nella sezione «VERSIONE 2» di `docs/RAPPORTO_RISULTATO1.txt`, ricontrollati da Claude
(sotto, le istruzioni di allora)
In ordine:
1. `python scripts\21_risultato1_vuoti.py` (guardare i «v2 OK/AVVISO» e la sezione «VERSIONE 2» di `docs\RAPPORTO_RISULTATO1.txt`; buon senso dal piano: Torino, soglia 1.000, abitati con 3+ mancanti dell'ordine di 700-800; zone poco abitate circa 6.800).
2. `python scripts\22_risultato1_candidati.py --gruppi salute,scuole` (nel rapporto: quanti candidati cambiano).
3. `python scripts\schede_risultati.py` (la scheda R1 deve avere il titolo nuovo e 4 schede in tutto).
4. `python scripts\prova_pagine_r6.py --senza-screenshot` (0 errori).
Poi riportare qui i numeri veri (sezione «VERSIONE 2», candidati prima/dopo).

## Righe cambiate
`git diff --stat` (3 file di codice + questo esito): `21_risultato1_vuoti.py` +165, `22_risultato1_candidati.py` +46 −, `schede_risultati.py` +111 −.
