# Esito — mappa, giro 1 (21/10/2026)

Piano: `PIANO_MAPPA.md`, sezione 9, giro 1 (sezioni 1 e 2). File toccati: `scripts/mappa_template.html`,
`scripts/04_genera_mappa.py`, `scripts/86_prepara_pubblicazione.py`.

**Peso di `mappa_torino.html`: prima 13.783.876 byte (13,8 MB) → dopo 13.061.568 byte (13,1 MB), −0,7 MB.**
(Il grosso resta nelle sezioni, 9,3 MB: è il giro 4.)

Righe cambiate (git, +aggiunte / −tolte): template +113 / −403; script 04 +3 / −197; script 86 +1 / −5.

## Per punto

| Punto | Esito | Note |
|---|---|---|
| Partenza senza tema | OK | `tema = NESSUN_TEMA`; legenda nascosta, nessuna area né linea; pannello: titolo, riga, menu. |
| Partenza su satellite | OK | `baseCorrente="sat"`. Le mattonelle Esri si vedono con internet. |
| Intensità sfondo 60% con un tema | OK | Scende al 60% a ogni cambio tema e torna 100% senza tema; il cursore (in «Altre opzioni») si può ancora spostare a mano. |
| Solo Satellite, Chiara, Nessuno | OK | Tolto «Mappa stradale». |
| Scatola «Quando» | OK | Solo giorno (Feriale/Sabato/Domenica) e ora a scatti di un'ora. Visibile in: Mezzi pubblici sotto casa, Spostamenti, Velocità e traffico, Ritardi delle linee, Servizi a portata (solo con «Mezzi pubblici»). Via play, velocità, «Adesso», minuti. Il giorno e l'ora iniziali sono quelli di adesso. |
| Sovrapposizioni | OK | Solo Linee (con «solo una linea») e Fermate, dentro «Altre opzioni» chiuso. I sensori restano accesi dal tema «Velocità e traffico» (casella interna, non nel pannello). |
| Link «I risultati →» | OK | Porta a `simulazione.html` (stessa pagina del vecchio bottone). |
| Guida corta | OK | 4 righe + fonti e date. Tolto il testo lungo del Risultato 6 (sta nella scheda). |
| Nomi nuovi e due gruppi | OK | Menu «Scegli un tema…» + «Chi abita e cosa trova» (Chi abita qui, Fragilità sociale, Servizi a portata, Servizi mancanti, Prezzo delle case) + «Come ci si muove» (Mezzi pubblici sotto casa, Spostamenti, Velocità e traffico, Ritardi delle linee, Parcheggi di scambio, Luoghi della città). |
| Id dei temi invariati | OK | `#tema=interscambio` e `#tema=puntualita&linea=17` provati e funzionanti. Nuovo id solo per «Chi abita qui»: `residenti` (prima era dentro `servizio`); `#tema=domanda` porta lì. |
| «Chi abita qui» | OK | Solo viste già esistenti: abitanti per km², bambini 5-14, anziani 65+, occupati. «Fragilità sociale» tiene le 5 viste dell'indice. «Mezzi pubblici sotto casa» ha «Passaggi all'ora per abitante» / «Passaggi all'ora». |
| Tolto il tema pendolari | OK | Tema, legenda, scheda comune, tooltip, opzioni; nello script 04 `costruisci_pendolari` e `D.pend`. Il vecchio `#tema=pendolari` apre la mappa senza tema. |
| Tolte corse simulate | OK | Casella, disegno, `D.corse` (script 04), contatore. |
| Tolti avvisi GTT | OK | `D.avvisi`, badge nelle schede fermata/linea, riga nelle fonti, `meta.avvisi_data`. |
| Tolta griglia | OK | Casella, disegno, testo nella scala. |
| Tolta tendina giornate registrate | OK | Tendina, `caricaReplay`, `disegnaReplay`, animazione. |
| Tolti i `replay_*.js` dalla pubblicazione | OK | Script 86: tolto il ciclo di copia e il commento. I file restano in `data/` (non toccati). |

## Prove

- `python scripts\04_genera_mappa.py`: OK, 13,1 MB, nessun errore (risultato 1 torna: 362).
- `python scripts\prova_pagine_r6.py --senza-screenshot`: **0 errori** su 13 pagine (tutti i temi).
- `node --check` sullo script della pagina: OK.
- In Chromium (pannello del browser): all'apertura satellite, nessun colore, legenda nascosta; menu con i due gruppi;
  per ogni tema acceso solo il suo (area, linee, sensori, «Quando» e legenda controllati uno per uno); «Chi abita qui»
  cambia vista (4); `#tema=interscambio` (vista parcheggi), `#tema=puntualita&linea=17` (filtro 17, Linee accese).

## Avvisi / da decidere

- **AVVISO** — «Sfondo» (Satellite/Chiara/Nessuno) resta visibile nel pannello, anche all'apertura; nel piano si legge «solo titolo, una riga e menu». Il cursore dell'intensità è invece in «Altre opzioni». Se si vuole il pannello ancora più vuoto, si sposta anche lo sfondo in «Altre opzioni».
- **AVVISO** — Senza tema la legenda non appare nemmeno se si accendono a mano Linee o Fermate (come da piano: legenda solo con un tema).
- **AVVISO** — «Spostamenti» tiene ancora la vista «Residenti 11-84 anni» (il piano la sposta in «Chi abita qui», sezione 3: giro 3).
- **AVVISO** — `stat.js` è ancora caricato: serve al traffico tipico dei sensori; esce nel giro 2 (sezione 4).
- **AVVISO** — il peso cala solo di 0,7 MB: l'obiettivo sotto 7 MB è del giro 4.
- Non fatte, come richiesto: sezioni 3-8 (viste nuove di «Chi abita qui», «Tutti i servizi», «Luoghi della città», peso, criticità).
