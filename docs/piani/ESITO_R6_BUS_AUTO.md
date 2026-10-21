# Esito R6 parte C: il bus contro l'auto verso Piazza Castello (21/10/2026)

Script nuovo `scripts/94_r6_bus_contro_auto.py` (sola lettura; riusa le funzioni dello script 93 con `comuni.carica_script`, non le copia; il prossimo numero libero è 95).
Uscite: `data/processed/r6_bus_contro_auto.json`, `docs/rapporti/RAPPORTO_R6_BUS_CONTRO_AUTO.txt`. Prove sul PC: 94, `79_dati_mappa_r6.py`, `schede_risultati.py`, `04_genera_mappa.py`, `prova_pagine_r6.py` (0 errori sulle 18 pagine).

## Metodo e regola (fissata prima dei numeri)

- Luoghi: i 12 punti prioritari del R6 (centro delle fermate del punto, da `porte.json` dello script 84) e i 5 interscambi esistenti del Comune. Destinazione: Piazza Castello.
- Mezzi pubblici: r5py come nello script 93, 2026-10-12, partenza 7:45 con finestra di 30 minuti, mediana, cammino a 4,8 km/h.
- Auto: flusso libero × fattore di punta + 5 minuti per parcheggiare. Fattori letti da `tp_contro_auto.json`: alto 1,2 (sensori 5T), basso 2,1 (Google Maps).
- Rapporto = tempo coi mezzi / tempo in auto. **Il bus conviene**: rapporto ≤ 1,5 con entrambi i fattori. **Dipende dal traffico**: ≤ 1,5 solo col fattore basso. **Il bus non conviene**: oltre 1,5 con entrambi (anche senza collegamento entro 120 minuti: qui nessun caso).

## Risultato

- Punti prioritari: **0 il bus conviene, 1 dipende dal traffico, 11 il bus non conviene** (su 12).
- Interscambi esistenti: 0 conviene, 3 dipende, 2 non conviene (su 5).
- Il solo punto che «dipende» è Metro Massaua (rapporto da 1,1 a 1,7): ha la metro vicina.
- Dai punti prioritari il bus è quasi sempre più lento dell'auto di oltre una volta e mezza: l'auto resta più comoda finché non c'è un collegamento diretto.

### Tabella completa: punti prioritari

Tempi in minuti. Auto: fattore alto-basso. Rapporto: limite basso-alto.

| Luogo | Posti che mancano | Mezzi | Auto | Rapporto | Classe |
|---|---|---|---|---|---|
| Santa Rita | 450 | 36 | 14-20 | 1,8-2,6 | il bus non conviene |
| Metro Massaua | 350 | 25 | 15-23 | 1,1-1,7 | dipende dal traffico |
| Ponte Cavalieri Templari | 350 | 51 | 18-28 | 1,8-2,8 | il bus non conviene |
| Regina Margherita | 350 | 31 | 12-17 | 1,9-2,7 | il bus non conviene |
| Pasini | 250 | 28 | 12-17 | 1,6-2,3 | il bus non conviene |
| Leonardo Da Vinci | 200 | 59 | 20-31 | 1,9-3,0 | il bus non conviene |
| Drosso Cap | 200 | 43 | 17-27 | 1,6-2,5 | il bus non conviene |
| Stura Lazio | 200 | 37 | 14-21 | 1,7-2,6 | il bus non conviene |
| Marsè | 150 | 61 | 23-37 | 1,7-2,6 | il bus non conviene |
| Derna Est | 100 | 34 | 14-20 | 1,7-2,5 | il bus non conviene |
| Ferrara | 80 | 49 | 20-31 | 1,6-2,5 | il bus non conviene |
| Zara | 60 | 33 | 12-17 | 1,9-2,8 | il bus non conviene |

### Tabella completa: interscambi esistenti

| Luogo | Riempimento di giorno | Mezzi | Auto | Rapporto | Classe |
|---|---|---|---|---|---|
| Stura | pieno | 39 | 17-27 | 1,5-2,2 | dipende dal traffico |
| Venchi Unica | a meta | 28 | 16-24 | 1,2-1,8 | dipende dal traffico |
| Caio Mario | libero | 38 | 16-24 | 1,6-2,4 | il bus non conviene |
| Fermi | non misurato | 31 | 19-29 | 1,1-1,7 | dipende dal traffico |
| Sofia | libero | 33 | 13-20 | 1,7-2,5 | il bus non conviene |

Interscambi esistenti del Comune, stesso test. STURA (pieno): 39 minuti coi mezzi contro 17-27 in auto (rapporto 1,5-2,2); dipende dal traffico. VENCHI UNICA (a meta): 28 minuti coi mezzi contro 16-24 in auto (rapporto 1,2-1,8); dipende dal traffico. CAIO MARIO (libero): 38 minuti coi mezzi contro 16-24 in auto (rapporto 1,6-2,4); il bus non conviene. FERMI (non misurato): 31 minuti coi mezzi contro 19-29 in auto (rapporto 1,1-1,7); dipende dal traffico. SOFIA (libero): 33 minuti coi mezzi contro 13-20 in auto (rapporto 1,7-2,5); il bus non conviene. Quelli poco pieni: da VENCHI UNICA dipende dal traffico; da SOFIA il bus non conviene.

## Collegamento al R6

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| Elenco dei punti | OK | Nessun punto tolto: lo script 79 aggiunge solo il campo `bus_auto` (tempi, rapporti, classe) ai 12 punti e ai 5 interscambi in `mappa_r6.json`. |
| Mappa | OK | Pannello del punto prioritario e dell'interscambio: tempo coi mezzi, tempo in auto (due fattori), classe. Controllato in Chromium sui punti 1 (Santa Rita, non conviene) e 2 (Metro Massaua, dipende dal traffico). |
| Scheda R6 | OK | Il limite «non misuriamo ancora…» è diventato punto chiave: da 0 punti su 12 il bus conviene, da 1 dipende dal traffico. Il punto sugli interscambi poco pieni è passato nella parte chiusa «Interscambi esistenti e bus verso il centro», con grafico dei minuti. Nuovo limite sui tempi (solo GTT, fattori). |
| Catena | OK | `RISULTATO6_RIFAI.bat`: 94 fra 84 e 79 (serve aver lanciato il 93 almeno una volta). |
| Documenti | OK | `docs/R8_traffico.md` ha ora anche la tabella «forbice» (fasce e gruppi) e la riga dello script 93; `ESITO_R8_TP_AUTO.md` cancellato. `docs/R6_parcheggi.md` e `MEMORIA_PROGETTO.md` aggiornati. |

## Da sapere

- I tempi coi mezzi sono solo GTT, senza treni: dai luoghi fuori Torino (Ponte Cavalieri Templari, Marsè, Leonardo da Vinci) il bus può risultare peggiore del vero.
- Un solo punto per luogo; per i punti prioritari è il centro delle fermate importanti, non una fermata precisa.
- Col fattore alto la soglia 1,5 non è mai rispettata; il limite basso dà la sola eccezione. L'esito dipende dalla soglia scelta prima dei numeri: non è stata cambiata.
- Lo script 94 riscrive `r6_bus_contro_auto_parziale.npz`, diverso dal file parziale del 93 (non si sovrascrivono).


## Messaggio nuovo e sensibilità (21/10/2026)

| Punto | Stato | Cosa è stato fatto |
|---|---|---|
| Sensibilità nello script 94 | OK | Classi ricalcolate con 5, 10 e 15 minuti di parcheggio in centro (`MINUTI_SENSIBILITA`). La classe ufficiale resta quella con 5 (controllo bloccante: la colonna 5 coincide). Nel JSON: `sensibilita_parcheggio` e `classi_sensibilita` per luogo; nel rapporto una tabella e le classi per luogo. |
| Scheda R6 | OK | Titolo «I parcheggi di scambio funzionano solo dove il mezzo pubblico è veloce: oggi su 1 punto su 12»; numero grande 1 su 12; grafico principale = rapporto dei 12 punti (barra scura = limite basso, chiara = alto, linea a 1,5, colore = classe; `soglia` nuovo in `risultati.html`); punti chiave: interscambi pieni/vuoti con i nomi, fermate senza posti, N10 = 10 e N15 = 12; altro grafico: punti per bisogno di posti; limiti con GTT senza treni, parcheggio a 5 minuti, costo non considerato; inglese con gli stessi numeri. Criteri ridotti a 4 righe e metodo a 5. |
| Documento | OK | `docs/R6_parcheggi.md`: messaggio in testa, tabella dei luoghi con classe a 5/10/15 minuti, sensibilità. |
| Prove | OK | 94, 79, `schede_risultati.py`, `04_genera_mappa.py`, `prova_pagine_r6.py`: 0 errori su 18 pagine; scheda controllata in Chromium. |

### Sensibilità (punti | interscambi: conviene / dipende / non conviene)

| Minuti | Punti | Interscambi | Punti competitivi |
|---|---|---|---|
| 5 | 0 / 1 / 11 | 0 / 3 / 2 | 1 su 12 |
| 10 | 1 / 9 / 2 | 2 / 3 / 0 | 10 su 12 |
| 15 | 4 / 8 / 0 | 5 / 0 / 0 | 12 su 12 |

### Da sapere

- Il messaggio è molto sensibile ai minuti di parcheggio: da 1 punto su 12 (5 minuti) a 10 (10 minuti) a 12 (15 minuti). Il numero ufficiale resta 1, ma va letto con questa forbice.
- «Competitivo» = conviene o dipende dal traffico. Col fattore alto dei sensori solo 1 punto su 12 conviene già con 10 minuti.
- Interscambi: Venchi Unica (a metà) e Fermi (non misurato) hanno il bus competitivo ma non sono né pieni né vuoti: restano fuori dal punto chiave.
