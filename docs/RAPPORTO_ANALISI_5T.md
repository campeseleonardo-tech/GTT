# Rapporto: analisi dei dati diurni 5T e mezzi GTT

Data dell'analisi: 8 ottobre 2026 (dati fino al 8/10 ~23:20 ora locale).
Strumento: `scripts/09_analisi_dati_diurni.py` (sola lettura, mai scrive su `storico.sqlite`).
Numeri grezzi completi: `docs/RAPPORTO_ANALISI_5T.txt` (rigenerato a ogni esecuzione).
Aggregati machine-readable: `data/processed/analisi_5t.json`.

## Periodo coperto

Dal 4 ottobre (01:41 locali) al 8 ottobre 2026 (23:20 locali): **5 giorni**, di cui
4 feriali (5–8/10) e 1 domenica (4/10). **Sabato assente** (la raccolta è partita il
3/10 sera, ma i primi 4 snapshot cadono già di domenica in ora locale).
Tutti i timestamp sono registrati in UTC e aggregati in ora locale Europe/Rome
(regola UE; verificata ai confini del cambio d'ora, che i dati attuali non attraversano).

## 5T — traffico (122.189 misure, 1.121 snapshot, 109 sensori)

### Fatti misurati
- **Copertura**: ogni snapshot contiene esattamente 109 sensori (0 sensori sotto
  copertura). Copertura nella finestra osservata del giorno: dom 4/10 95,9%,
  lun 5/10 91,3%, mar 6/10 87,1%, mer 7/10 98,0%, gio 8/10 92,5% (giorno in corso).
- **Zero e positivi** (denominatore = tutte le 122.189 misure): flusso=0 il **19,7%**,
  flusso>0 l'**80,3%**, flusso NULL il 0%, velocità NULL il 0%.
- **Profilo orario feriale** (4 giorni): la quota di zeri scende dal 57% a mezzanotte
  al 12% dalle 06:00 in poi; massimo del flusso mediano (>0) 528 alle 08:00,
  p95 1.644. Di notte (02–04) la copertura della raccolta è più bassa (69–75%
  delle 12 misure/ora attese): ci sono buchi, non zeri del tracciato.
- **Domenica** (1 giorno): profilo simile ma più dolce (mediana>0 max 432 alle 18:00).
- **Velocità**: mai NULL; mediana 59,2, massimo 167.
- **Strade**: i tratti più carichi sono le direttrici radiali (Corso Orbassano 874,
  Corso Giulio Cesare 733, SS11 neg. 380…) e il Raccordo per l'Aeroporto (729).
  I flussi per strada sono **media dei valori >0**, gli zeri non sono mescolati.
- **Sensori** (fotografia corrente, NON storica): 109 sensori, 14 con `accuratezza=0`
  (12,8%) oggi.

### Dato mancante
- **L'accuratezza non è stata salvata con ogni misura**: `flussi_5t` non ha la colonna
  e `sensori_5t` tiene solo l'ultimo stato per sensore. Quindi il passato non può essere
  classificato per accuratezza: questa variabile è "non disponibile" per l'intero periodo
  qui analizzato. La raccolta ora (dal prossimo riavvio) la salverà in `accuratezza_5t`.
- **Sabato**: nessun dato.

### Anomalie da tenere d'occhio
- Buco di ~16,7 h il 6–7/10 (16:42 → 09:27 successiva): raccolta ferma (probabile PC spento).
- Buco di ~87 min l'8/10 e di ~119 min il 6/10.
- Rari valori di flusso molto alti (max 5.916 in 5 minuti ≈ 1.183 veicoli/minuto):
  numericamente implausibili per una strada; da verificare prima di usarli come norma
  (possibile artefatto del sensore o del periodo di conteggio).

### Interpretazioni NON fatte
- Non si afferma che `accuratezza=0` significhi "sensore spento": non c'è una prova
  tecnica e il passato non permette di verificarla. Si potrà studiare sui nuovi campioni
  (accuratezza salvata per misura) dopo almeno 7–14 giorni di raccolta, inclusi feriali
  e weekend; e anche lì una correlazione non sarà da sola una dimostrazione.

## Mezzi GTT (1.580.712 righe, 5.163 snapshot)

### Fatti misurati
- Controlli: 0 duplicati `(letto_utc, veicolo)`, 0 righe con veicolo/linea vuoti.
- **~306 veicoli localizzati per snapshot** (mediana 337, max 577). Attenzione: questo
  è il volume del **feed**, non necessariamente l'intera flotta in servizio
  (il feed non trasporta il trip_id).
- **Ore di punta osservate** (media di veicoli distinti per snapshot):
  - feriale: **08:00 (555,5/snapshot)**, alto anche 07:00 (534) e 09:00 (478);
  - domenica: **18:00 (255,7/snapshot)**.
- Di giorno (07–19 feriale) il feed ha 400–550 veicoli/snapshot; tra le 02:00 e le
  03:00 quasi nulla (2–5 veicoli/snapshot, minimo 1).
- Linee con più mezzi localizzati (media per snapshot in cui compaiono): 4U (17,5),
  2U (10,9), 15U (9,8), 62U (8,4), 56U (8,2).
- **Buchi del feed**: 31 buchi > 90 s; i più lunghi ~92 min e ~91 min la notte/sera del
  5/10. 400 snapshot su 5.163 hanno meno di 50 veicoli (soprattutto di notte).

### Limite
- Il conteggio è **per veicolo distinto** e misura i mezzi che il feed localizza,
  non la flotta totale in servizio.

## Limiti generali di questo rapporto

- Solo 5 giorni, sabato mancante: le medie orarie feriali e domenicali hanno
  denominatori espliciti (numero di snapshot e giorni che le sostengono) nel txt,
  e vanno lette come prime indicazioni, non come norma.
- La rete 5T copre strade statali e provinciali anche fuori Torino (es. SS494, SP155,
  SS30 risultano sempre flusso 0): non leggere quei valori come "strade deserte",
  sono sensori fuori area o fuori servizio da verificare.
- Nessun risultato qui attribuisce l'accuratezza corrente alle misure passate.

## Prossimo passo

Raccolta dei trip_update e analisi dei ritardi (attività 2 della memoria). Nel
frattempo, dal riavvio della raccolta, `accuratezza_5t` comincerà a raccogliere
l'accuratezza per misura: dopo 7–14 giorni si potrà analizzare l'associazione
accuratezza ↔ flusso ↔ ora.