# Piano — Risultato 8: traffico sulle strade e trasporto pubblico (prima `RIASSUNTO_TRAFFICO.md`)

Piano unico del risultato: in testa i commenti di Leo del 20/10 e i lavori, sotto il riassunto del 18/10 (invariato).
**Nessuna modifica fatta al risultato**: è un piano.

## Commenti di Leo (20/10) e fattibilità

| Commento | Controllo | Fattibile? |
|---|---|---|
| R8 è pulito | — | — |
| **Misurato e stimato per strada anche in percentuale**, per vedere come si distribuisce l'errore | La scheda ha già il grafico «Prova del modello sui 20 sensori» (barre misurato/stimato), ma non l'errore in %. Gli errori ci sono già (`docs/RAPPORTO_TRAFFICO_V4.txt`): dallo 0,2% di Corso Orbassano (40097) al 177% di Corso Unione Sovietica; metà entro ±38%, 9 su 10 entro ±64% | Sì, piccolo: colonna o grafico «errore %» nella scheda, ordinato |
| **Si può ridurre l'errore?** | Leve, in ordine di costo: (1) **più punti di confronto**: oggi 20 unità-sensore; i 3 codici doppi salvati dal 17/10 e altri sensori abbinati per posizione possono aggiungerne qualcuno; (2) **domanda per fascia oraria e code** nel modello (la Fase 5 ha visto che senza code Piazza Castello → Collegno vale 13,8 min contro 20-35 reali); (3) pendolari da fuori Piemonte, merci, turisti (dati che non abbiamo). Il modello più ricco V4 non aveva migliorato la correlazione | (1) piccolo-medio, da provare dopo 6 feriali con i codici nuovi; (2) grande; (3) no |
| **«95,3%» = «non ci sono zone completamente prive di fermate»** | Non proprio: il 95,3% riguarda solo le **strade grandi di Torino** (343 km). La frase giusta è «**lungo le strade grandi di Torino c'è quasi sempre una fermata frequente a meno di 300 m**». Per le zone: dal Risultato 1, 1.204 torinesi non hanno una fermata a 15 minuti a piedi (soprattutto in zone poco abitate) | Sì, piccolo: correggere la frase nella scheda e nel README |
| **Incrociare con i parcheggi** (una fermata serve a poco se non posso lasciare l'auto) | È la domanda del Risultato 6 | Solo idea: il collegamento si fa nel R6 (parcheggi vicino a linee utili), non qui |

## Decisioni di Leo (20/10)

Primo lavoro: **tabella degli errori in % + frase corretta**. Migliorare il modello solo come idea, dopo.

**Come eseguirli**: i lavori 1-2 sono nel **Giro 1** (`docs/PIANO_GIRO1_RITOCCHI.md`), con il prompt pronto.
Gli altri si preparano dopo, uno per volta, con un prompt nello stesso stile.

## Lavori da fare (in ordine)

| # | Lavoro | Dove | Quanto |
|---|---|---|---|
| 1 | Errore in % per ognuno dei 20 sensori nella scheda (ordinato; colore verde→rosso per l'errore) | `schede_risultati.py` (`scheda_r8`) | piccolo |
| 2 | Frase corretta sul 95,3% (solo strade grandi di Torino) in scheda, inglese e README; nelle fonti della scheda il piano diventa `docs/PIANO_RISULTATO8.md` (oggi cita ancora `RIASSUNTO_TRAFFICO.md`) | `schede_risultati.py` | piccolo |
| 3 | Routine settimanale: fetch, `TRAFFICO_RILANCIA_SENSORI.bat`; ora legale del 25/10 da controllare a mano nello script 26 dopo il fetch del 1/11 | — | — |
| 4 | Dopo 6 feriali con i codici nuovi (dal 17/10): provare ad aggiungere unità di confronto | 33-44 | piccolo-medio |
| 5 | Corso Moncalieri: controllo a mano della copertura TP | — | piccolo |
| — | Idee: modello con le code; mappa del traffico (solo se Leo vuole); `velocita_5t.json` al posto del «tipico» di `stat.js` in mappa | — | — |

---

# Riassunto del 18/10 (invariato)

Scritto da Claude il 18/10/2026 a partire dai piani, dagli esiti e dai rapporti delle Fasi 1-5 (ora in
`docs/archivio/traffico/`). Qui c'è tutto quello che serve per capire e riprendere il lavoro; i documenti
originali restano per i dettagli.

## 1. Domanda e risposta

**Domanda di Leo:** quanti veicoli passano sulle strade di Torino, e dove c'è molto traffico ma poco
trasporto pubblico (TP), così che l'auto resta l'unica scelta?

**Risposta (versione 1, 18/10):**
- Sulle **540 tratte di strade grandi di Torino (343,3 km)** il **95,3% della lunghezza** ha una fermata con
  almeno 4 passaggi/ora entro 300 m o la metro entro 600 m (327,3 km).
- **180 tratte** hanno molto traffico (≥ 11.720 veicoli/giorno, 6-21, due versi); **5** hanno anche poco TP:
  in pratica **Corso Regina Margherita ovest** (tratto a scorrimento veloce, ~34.000 veic/giorno, nessuna
  fermata frequente entro 300 m: ricontrollato) e **un tratto di Corso Moncalieri** (coperto per un quarto;
  da controllare a mano).
- La lista di 23 strade della Fase 4 era un **artefatto**: il TP era misurato lungo la strada per nome
  (Corso Cairoli risultava con 2 linee e 0 passaggi). Con le fermate cercate per posizione è sparita.
- Scheda in `simulazione.html` (da `scripts/schede_risultati.py`, funzione `scheda_r8`).

**Qualità della stima: classe `C-DEBOLE`** — errore mediano **38,4%** (intervallo 90%: 25,5-49,8%), Spearman
**0,605**, 20 punti di misura, fattore di taratura k = 0,953. Ricalcolati da Claude, identici. Fasce
pubblicate: metà dei casi entro **±38%**, 9 su 10 entro **±64%**; fuori da 8.845-105.230 veic/giorno è
un'estrapolazione e la fascia raddoppia. **Serve a ordinare le strade, non a contare i veicoli.**

| Classe di esito (fissata in Fase 3) | Condizione | Cosa si pubblica |
|---|---|---|
| C-ASSOLUTO | errore ≤ 35%, meglio del metodo A, ρ ≥ 0,7 | veicoli/giorno con fascia |
| C-INDICE | ρ ≥ 0,7 ma errore > 35% | solo indice relativo |
| C-DEBOLE | 0,5 ≤ ρ < 0,7 | classi alto/medio/basso, marcate "debole" (Leo ha scelto di pubblicare anche numeri assoluti con fascia) |
| C-NO | ρ < 0,5 | niente |

## 2. Decisioni di Leo (17-18/10)

- Risultato con **numeri assoluti + fascia** dagli errori leave-one-out, valori relativi e graduatoria, con la
  classe di esito accanto.
- **"Poco TP" = accessibilità** (fermate vicine con buon servizio), non bus che passano sulla strada.
- **Fermate e strade solo per coordinate, mai per nome.** Un corso che cambia nome o comune è **un solo asse**;
  l'unità è la tratta d'asse (0,3-1,5 km sulle strade grandi).
- Solo strade grandi; il centro-centro non è prioritario; ZTL unita con gli orari; le corsie contano.
- La conoscenza della città di Leo (`docs/CONOSCENZA_TORINO_LEO.md`) è **solo controllo di buon senso, mai
  taratura**. Accordo attuale: 10 strade su 18 nella fascia giusta, 4 confronti su 7.

## 3. Come si è arrivati qui (fasi)

| Fase | Script | Cosa | Esito |
|---|---|---|---|
| Velocità 5T | 26 | velocità e flusso tipici per sensore × tipo di giorno × ora, solo letture affidabili → `velocita_5t.json` | 2.252 celle feriali (9-16/10) |
| 1 | 33, controllo | flusso per sensore; il 5T dà **già veicoli/ora** (multipli di 12); 112 sensori, `lcd1` unico per 109 (codici doppi 40123, 40189, 13077); accuratezza per lettura dall'8/10 21:30 UTC; ora 1 locale = dato mancante | raccoglitore corretto sul Pi il 17/10 11:24 (`AGGIORNA_RACCOLTA_5T_CODICI.bat`): codici `~2` presenti solo da allora, utili dopo ~6 giorni feriali; non entrano nelle 20 unità di valutazione |
| 2 | 34-38b | esclusi 17 sensori (11 morti, 5 bloccati, 1 pochi dati) → 92 usabili; abbinamento sensori-corridoi per posizione; **metodo A** (medie per tipo di strada) errore 36,9%, metodo B ≈ A | solo 20 unità-sensore su 15 corridoi |
| 3 | 39-48, `rete_osm.py` | **metodo C**: domanda auto IMQ (4,15 M viaggi/giorno) assegnata al percorso più veloce su rete OSM (81.966 nodi, 105.890 tratti), porte sul bordo | C-DEBOLE, 31,9% / ρ 0,602 |
| 3-bis, 4 | 49-55 | modello V3 (attrattori + code + porte): non migliora (ρ 0,573) → resta V0; TP per strada dal GTFS; incrocio 23 corridoi | lista **non affidabile** (verdetto di Claude) |
| 5 | 56-67 | assi e tratte, corsie (OSM `lanes` sul 29% dei tratti), ZTL unificata (3 zone + 143 aree pedonali), **TP per posizione delle fermate** (5.055 fermate, 13.158 corse del 14/10), modello V4: non migliora (ρ 0,571) → **V0** | risultato attuale (sezione 1) |

Perché V0 e non i modelli più ricchi: la regola fissata (V4 si adotta solo se ρ non peggiora) l'ha escluso.
La congestione non funziona: Piazza Castello → Collegno 13,8 min nel modello contro 20-35 attesi in punta.
Se un giorno si riprova, la strada è la congestione (domanda per fascia oraria, capacità reali), non
attrattori o porte.

## 4. Limiti (da dire sempre)

- Stima debole; alcune strade molto sbagliate (Corso Unione Sovietica +177%, Corso Sebastopoli +99% ai
  sensori). Senza un sensore sull'asse, la classifica mette in cima strade poco credibili (es. Corso
  Dogliotti ~58.500): nella scheda si mostrano solo strade con un sensore sull'asse.
- 20 punti di misura, tutti tra ~9.000 e ~105.000 veic/giorno; a Torino sensori a un solo verso (×2 per avere
  i due versi); la notte è inaffidabile e l'ora di punta non è validata.
- Domanda IMQ 2022: solo residenti 11-84 anni, feriale medio; mancano merci, turisti, pendolari da fuori.
- TP programmato (GTFS): niente ritardi né affollamento. Centro (ZTL, pedonali) non stimato bene.
- **Convenzione a due versi**: ogni tratto OSM a senso unico vale ×2. Giusto per i corsi a due carreggiate,
  **doppio del reale sulle vie a senso unico vere**: al massimo 47 tratte / 24 km dell'universo, non separabili
  con certezza (controllo di Claude).
- Piccole differenze tra file: `tratte_traffico.json` dice 539 tratte / 342,8 km, `risultato8_traffico_tp_v2.json`
  540 / 343,3 (giri diversi dello script 65/66). Le "lunghezze degli assi" nell'ESITO della Fase 5 sono la
  somma di carreggiate e controviali (Corso Francia 41,8 km), non la lunghezza della strada.

## 5. File e rilancio

- **Risultato:** `data/processed/risultato8_traffico_tp_v2.json` (universo, conteggi, assi da guardare,
  tratte); dettaglio per tratta in `data/processed/traffico_d/tratte_traffico.json`; valutazione in
  `traffico_d/valutazione_fase5.json`. Le versioni delle fasi 3-4 restano in `traffico_c/` e
  `risultato8_traffico_tp.json` (superate).
- **Dopo ogni fetch dal Pi** (domenica, `FETCH_LEOPI_E_VELOCITA_5T.bat`): `scripts\TRAFFICO_RILANCIA_SENSORI.bat`
  (riscrive anche i rapporti in `docs/` elencati sotto). Assi, corsie, ZTL, TP e modello V4:
  `scripts\FASE5_MODELLO.bat` (lungo, ~1 ora). Il bat settimanale rilancia ancora anche i passi delle fasi 3-4
  (37, 43-45, 50b, 53-54): si possono togliere se non servono più (da decidere).
- **Rapporti che il rilancio riscrive (restano in `docs/`):** `RAPPORTO_VELOCITA_5T`, `FLUSSO_5T_SENSORI`,
  `SENSORI_ESCLUSI`, `ABBINAMENTO_POSIZIONE`, `CODICI_CONDIVISI`, `TRAFFICO_AB`, `TRAFFICO_C_SEGMENTI`,
  `TRAFFICO_C_VALIDAZIONE` (+ `grafico_misurato_vs_previsto.png`), `TRAFFICO_C`, `TRAFFICO_C_V2`,
  `TRAFFICO_C_V3`, `RISULTATO8_TRAFFICO_TP`, `TRAFFICO_V4`, `AFFIDABILITA`, `RISULTATO8_TRAFFICO_TP_V2`,
  `FASE5_VERIFICHE`.
- **In archivio** (`docs/archivio/traffico/`): piani ed esiti delle Fasi 1-5, piano della velocità 5T, rapporti
  fatti una volta sola. Se uno script delle fasi passate viene rilanciato, riscrive il suo rapporto in `docs/`.

## 6. Da fare

1. Fetch del 19/10 per sabato e domenica, poi ogni domenica; dopo il 25/10 controllare a mano il cambio dell'ora
   legale nello script 26.
2. Corso Moncalieri: controllo a mano della copertura TP.
3. Mappa del traffico (tratte colorate con fascia, assi "da guardare"): solo se Leo vuole.
4. La mappa usa per i sensori il "tipico" di `data/stat.js` (calcolato sul Pi **senza scartare le letture
   inaffidabili**); quello pulito è `velocita_5t.json`: da collegare alla mappa.
5. Dopo il Risultato 8: tempi TP contro auto per coppie di zone IMQ, poi costi del viaggio (vedi memoria).
