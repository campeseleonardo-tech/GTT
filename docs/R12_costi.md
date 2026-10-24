# Risultato 12 (scheda 6): quanto costa muoversi

Domanda: quanto costa andare in centro (e fra le zone di Torino) in auto e coi mezzi pubblici, oggi? Due livelli per l'auto: costo **che si sente** (carburante e parcheggio) e costo **pieno** (anche manutenzione, assicurazione, pneumatici, ammortamento: tabelle ACI). Collegato alle schede 3 e 4 (tempi) e al risultato 6 (punti prioritari).

## Risposta (prezzi consultati il 2026-10-24)

- Lavoro in centro, al mese, mediana dei 12 punti prioritari (percorso mediano 6,2 km): auto che si sente **307 euro**, auto piena 404 euro, mezzi pubblici 38 euro. **Numero grande: 269 euro in più al mese in auto** (con il costo pieno 366).
- Il parcheggio pesa più del carburante: 13,60 euro al giorno di sosta (8 ore) contro circa 1,76 euro di carburante.
- Tempo contro soldi: coi mezzi 11 minuti in più (mediana, stima TomTom alle 8, scheda 4) e 269 euro risparmiati al mese.
- Una commissione in centro (2 ore): auto che si sente 5,16 euro, auto piena 10,00, mezzi 4,00 (2 biglietti).
- Fra due zone di Torino, senza parcheggio (lavoro al mese, mediana per fascia di distanza):
  - 0-3 km: 52 coppie, auto che si sente 14 euro, auto piena 53, mezzi 38.
  - 3-6 km: 191 coppie, auto che si sente 25 euro, auto piena 94, mezzi 38.
  - 6-10 km: 207 coppie, auto che si sente 44 euro, auto piena 164, mezzi 38.
  - oltre 10 km: 56 coppie, auto che si sente 64 euro, auto piena 241, mezzi 38.
  Senza parcheggio l'auto che si sente costa meno dell'abbonamento nelle fasce più brevi (vedi i numeri sopra): il peso dell'auto in città è soprattutto la sosta.

## Fonti (tutte in `data/ref/costi.json`, con indirizzo e data)

- Carburante: Osservatorio prezzi carburanti del Ministero (interrogazione di zona, 107 impianti entro 5 km da Piazza Castello): benzina self 2,004, gasolio self 2,249 euro al litro. La regola chiedeva la media di 4 settimane: i file con lo storico non rispondono da questo PC, resta il prezzo del giorno (le medie nazionali del Ministero sono stabili entro 0,02 euro in due settimane).
- Auto di riferimento: la stessa Volkswagen Golf VIII da 115 CV, a benzina (7,2 litri ogni 100 km in città, scheda WLTP a bassa velocità) e a gasolio (6,2). Costo pieno ACI 2026 (Gazzetta Ufficiale n. 297 del 23/12/2025, supplemento ordinario n. 40, 15.000 km l'anno): benzina 0,5568, gasolio 0,5047 euro al km.
- Mezzi pubblici (GTT, pagine ufficiali): biglietto urbano 2,00 euro (digitale 1,90), giornaliero 4,50, abbonamento mensile urbano 38, annuale 310.
- Sosta (GTT, strisce blu, lunedì-sabato 8:00-19:30): ZTL centrale 2,80, ordinaria 1,70, ridotta 1,50, smart 1,20 euro l'ora. Durata massima e biglietto giornaliero non sono sulla pagina: la giornata è 8 ore alla tariffa oraria.
- Licenze: per gli usi di questo risultato si copiano solo prezzi e due medie (nessuna riproduzione di tabelle o file); il servizio carburanti è dato aperto del Ministero.

## Regole (fissate prima dei numeri, 24/10/2026)

Auto che si sente = km × consumo × prezzo, andata e ritorno, più il parcheggio; auto piena = km × costo ACI, più il parcheggio; il costo è la media delle due auto. Lavoro = 20 giorni al mese con 8 ore di sosta alla tariffa ordinaria (la ZTL non è nel calcolo); commissione = 2 ore di sosta. Mezzi = abbonamento mensile (= 38 euro / 40 viaggi) per il lavoro, 2 biglietti per la commissione. Confronti: i 12 punti prioritari del risultato 6 e i 5 interscambi verso Piazza Castello; le coppie di zone di Torino (script 93, gruppo Torino-Torino) senza parcheggio, in fasce fisse di distanza (sotto 3 km, 3-6, 6-10, oltre 10). Chilometri = percorso più veloce sulla rete del modello del traffico.

## Limiti

- Prezzi di un periodo preciso (24/10/2026); consumo di una Golf e non della propria auto; abbonamenti ridotti e agevolazioni non considerati; ZTL e abbonamenti alla sosta fuori dal calcolo.
- Controllo delle distanze con TomTom (17 percorsi, solo la lunghezza): **11 fuori dal ±10%** (AVVISO): sui percorsi più brevi la nostra rete trova spesso un percorso più corto (anche in zona ZTL). L'effetto sul risultato è piccolo perché il parcheggio vale la maggior parte del costo.
- Cintura: le tariffe a zone del sistema integrato non sono assegnate alle zone dell'indagine; la scheda resta su Torino e sui punti del risultato 6 (AVVISO nel rapporto).

## Come si rifà

I prezzi si rifanno **a mano** quando cambiano: si aggiorna `data/ref/costi.json` (valori, indirizzi, data) e si rilancia. Poi:

```
python scripts\103_costo_del_viaggio.py          (rete OSM, r6_bus_contro_auto.json, tp_contro_auto.json; controllo TomTom se c'è la chiave)
python scripts\103_costo_del_viaggio.py --prova   (dati finti)
python scripts\schede_risultati.py
```

Uscite: `data/processed/costo_del_viaggio.json`, `docs/rapporti/RAPPORTO_COSTO_DEL_VIAGGIO.txt`. Lo script è nella fase `r6` di `rifai_tutto.py` (dopo 94 e 100).
