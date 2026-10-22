# Piano 3 — Risultati: cosa è finale e cosa no

Riscritto il 22/10 dopo un controllo su `origin/prova` (commit e rapporti in `docs/rapporti/`). Leo aveva ragione: quasi
tutto quello che la memoria dava «da lanciare sul PC» era già stato lanciato. Il dettaglio dei lavori chiusi sta nei
documenti dei risultati (`docs/R*.md`) e nella storia di git.
Regole di sempre: dati in sola lettura, prova su un campione, controlli negli script, numeri mai scritti a mano nei testi.
Numerazione in pagina: 1 servizi (R1) · 2 puntualità (R4) · 3 parcheggi di scambio (R6) · 4 traffico e mezzi (R8) · 5 case, servizi e fragilità (R10).

## Stato verificato (22/10)

| Lavoro | Stato | Prova |
|---|---|---|
| Mappa giro 4 (peso ~6 MB, «Luoghi della città») | **FATTO** | commit e933a8b; `mappa_torino.html` 5,9 MB |
| R6 parte C bus contro auto + minuti di pareggio (94) | **FATTO** | commit 0c967a1, `RAPPORTO_R6_BUS_CONTRO_AUTO.txt` |
| R4 giro 6 (giorni con poco GPS esclusi, attese) | **FATTO** | commit cda3b87, `RAPPORTO_RISULTATO9_ATTESA.txt` (esclusi 14, 18, 21/10) |
| R4 confronto con GTT (4 definizioni, incertezza) — B1, B2, B4 | **FATTO** | `docs/R4_puntualita.md` |
| R1 copertura 5/10/15 minuti ed esposizione al traffico — A1, A3, A4 | **FATTO** | `docs/R1_servizi.md`, script 92 |
| R8 tempi mezzi contro auto — D1, D2, D3, D5; errore per sensore in scheda | **FATTO** | script 93, `scheda_r8` |
| Case × fragilità × servizi (95) e vista «Doppio svantaggio» | **FATTO** | commit 948ebc1, `RAPPORTO_CASE_FRAGILITA_SERVIZI.txt`, mappa |
| Scheda 5 «Case, servizi e fragilità» sui dati veri | **DA CONTROLLARE** | `data/schede_risultati.js` non è in git: Leo apre `risultati.html` e guarda se la scheda 5 c'è e ha numeri veri |

## Cosa manca davvero

| # | Lavoro | Perché | Dove | Quanto |
|---|---|---|---|---|
| 1 | **R6 rifatto con più giorni di parcheggi** | il riempimento oggi è su 3 feriali [DATI SCARSI]; dal 14/10 i feriali interi sono già 5 (15, 16, 19, 20, 21; il 14 è parziale) e da lunedì 26 saranno di più | PC: `RISULTATO6_RIFAI.bat`, poi `RIFAI_MAPPA_E_SCHEDE.bat` | piccolo (~10 min) |
| 2 | **Scheda 5: controllo sui dati veri** (riga «DA CONTROLLARE» sopra); titolo «1 su 11» o «1 su 10» secondo il numero vero | il titolo arrotonda da solo | PC: guardare la pagina | piccolo |
| 3 | **Scheda 5: grafico della metro** | barre quasi uguali (differenze di 60-200 € su 1.300-2.500) e gruppi di 1-3 zone: mostra poco. Proposta: barre delle **differenze** (con metro − senza) per fascia, con il numero di zone scritto, oppure togliere il grafico e lasciare la frase | CLOUD (`schede_risultati.py`) | piccolo |
| 4 | **R4 con un mese di dati** (metà novembre) e poi stagione (gennaio, luglio) | più giorni = numeri più stabili | PC | piccolo, ricorrente |
| 5 | **Rilancio di tutto prima di unire in `main`**: catene dei risultati, schede, mappa, prova delle pagine (0 errori) | i numeri in pagina devono essere quelli dei rapporti | PC | piccolo |

## Lavori del vecchio piano non fatti: da decidere (valore predefinito: **non farli ora**)
- **A2 servizi contesi** (servizi per 1.000 abitanti, bacini a due passi) e **F capienze**: arricchiscono il R1, ma il
  messaggio non cambia. Si fanno solo se il R1 deve diventare il risultato principale.
- **D4 vista in mappa «Dove i mezzi non convengono»**: nel piano grafica diventa la «gara bus contro auto» (piano 4).
- **C4 classifica dei punti del R6 in 3 classi**: superata dai minuti di pareggio.
- **E4 prezzi nel tempo** (4-6 semestri OMI): facoltativo, richiede i file scaricati a mano da Leo.
- **R2 metro di notte**: resta in pausa e nascosto.

## Domande aperte per Leo
- Va bene lasciare A2, F, C4 ed E4 fuori dalla versione pubblicata?
