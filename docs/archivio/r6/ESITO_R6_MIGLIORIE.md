# Esito R6 migliorie (piano `PIANO_R6_MIGLIORIE.md`)

Eseguito il 19/10/2026 sul ramo `prova`. Nessun commit. `MEMORIA_PROGETTO.md` non toccata (il piano lo vieta).

## Esito per fase

- **FASE 1: OK.** `80_porte_interscambio.py` riscritto: classi solo sui posti nominali (nessuno / 1-49 / 50+), niente più «utile»; celle esagonali di circa 2 km² (lato 900 m); 20 punti prioritari; parcheggi mostrati (almeno 100 posti entro 400 m da una fermata importante o da un nodo forte, più i garage 5T con dati); profili feriali e weekend. `79_dati_mappa_r6.py` riscritto: `mappa_r6.json` (290 KB) con aree, punti prioritari, fermate, parcheggi, profili, riepilogo. Tutti i controlli OK.
- **FASE 2: OK (solo controlli di codice).** Mappa rigenerata (`mappa_torino.html`, 23,6 MB). Tre viste, ognuna con la domanda nel menu: «Dove ci sono parcheggi?», «In quali aree mancano parcheggi?», «Dove servirebbe di più un parcheggio?». Legenda aperta quando si apre il tema, guida riscritta, tema rinominato «Parcheggi per lasciare l'auto». I blocchi di script superano `node --check`. **Non verificata nel browser**: il browser integrato non apre né `localhost` né il file (vedi Anomalie).
- **FASE 3: OK.** Scheda R6 riscritta: numero chiave 206 su 378; risposta a 4 frasi; grafici (aree, pila, fermate, 20 punti, profili medi, sei profili singoli, parcheggi pieni, riferimento); criteri; metodo; limiti. Nuova sezione «Quanto sono affidabili i dati» in `simulazione.html`. `data/schede_risultati.js` rigenerato, `node --check` OK.
- **FASE 4: OK.** Nella scheda R6 e nella mappa non compaiono «utile», «osservazione», «versione», «scenario», «S2», «Allianz», «doppio». Restano «osservazion» solo nello script 80 (controllo a posteriori) e nel nome «OSSERVATORIO» di una fermata.

## Numeri chiave (dal file, ricontrollati)

- Fermate importanti: **378**. Nessun parcheggio entro 200 m **147**; pochi posti (1-49) **59**; 50 posti o più **172**. Senza 50 posti: **206**.
- Parcheggi trovati **5.205**; esclusi **1.774** (lungo strada 1.048, solo clienti 385, privati 341); considerati **3.431**; con almeno 50 posti **1,147** (175,356 posti).
- Parcheggi mostrati in mappa: **212** (58,833 posti), incluso il Palavela.
- Posti dichiarati / stimati: 374 / 2902.
- Parcheggi da 50+ posti entro 200 m da una fermata importante: 124 (23,819 posti). Da fermata o nodo forte: 194 (38,146 posti, circa il 22%).
- Nodi forti (metro, treno, capolinea, frequente): 346.
- Aree: 73 (Critica 37, Scarsa 12, Buona 24); di queste 26 hanno meno di 3 fermate (dato indicativo).
- Riempimento misurato: 9 parcheggi pieni di giorno tra quelli mostrati (3,041 posti). Quota dei posti mostrati con misura: 25.2%. Garage 5T con dato di riempimento: 32. Giorni feriali: 2026-10-15, 2026-10-16.
- Validazione dei 25 m²: mediana 24.4 m² per posto; 25°-75° percentile [14.2, 32.7]; 172 parcheggi OSM con posti dichiarati.
- Palavela (OSM 104393338): 568 posti stimati, a 200 m dalla fermata importante più vicina. Il sito turistico dice «fino a 600»: è una verifica a mano, non un dato.

## Sensibilità

- Distanza, fermate senza 50 posti: a 100 m 315; a 200 m 206; a 400 m 66. È il criterio che pesa di più.
- Posti per fermata coperta, fermate sotto la soglia: con 30 posti 170; con 50 206; con 100 258.
- Soglia delle fermate (script 75): 5% → 177 fermate; 10% → 378; 15% → 580.
- Soglie delle aree: 60/30 (scelta) → Critica 37; 50/25 → {'Critica': 45, 'Scarsa': 10, 'Buona': 18}; 66/33 → {'Critica': 37, 'Scarsa': 12, 'Buona': 24}.

## Tabella delle aree

| Area (id) | Zone principali | Fermate | Nessuno / pochi / 50+ | Quota senza 50 posti | Categoria |
|---|---|---:|---|---:|---|
| c-1463_3700 | Moncalieri | 6 | 4 / 2 / 0 | 100% | Critica |
| c-1468_3702 | Mirafiori Sud | 6 | 6 / 0 / 0 | 100% | Critica |
| c-1469_3707 | Parella | 6 | 5 / 1 / 0 | 100% | Critica |
| c-1467_3701 | Mirafiori Sud | 5 | 4 / 1 / 0 | 100% | Critica |
| c-1461_3699 | Moncalieri | 4 | 3 / 1 / 0 | 100% | Critica |
| c-1468_3704 | Mirafiori Nord | 4 | 4 / 0 / 0 | 100% | Critica |
| c-1471_3704 | Grugliasco | 3 | 3 / 0 / 0 | 100% | Critica |
| c-1471_3701 | Rivalta di Torino | 2 | 2 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1470_3702 | Beinasco | 2 | 0 / 2 / 0 | 100% | Critica (dato indicativo) |
| c-1469_3703 | Mirafiori Sud | 2 | 2 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1468_3709 | Borgata Vittoria | 2 | 2 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1461_3697 | Moncalieri | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1458_3697 | Cambiano | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1462_3699 | Moncalieri | 1 | 1 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1457_3700 | Chieri | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1467_3703 | Mirafiori Nord | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1465_3703 | Nizza millefonti | 1 | 1 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1464_3707 | San Mauro Torinese | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1473_3708 | Collegno | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1464_3708 | San Mauro Torinese | 1 | 0 / 1 / 0 | 100% | Critica (dato indicativo) |
| c-1471_3711 | Venaria Reale | 1 | 1 / 0 / 0 | 100% | Critica (dato indicativo) |
| c-1468_3706 | Cenisia - San Donato | 13 | 11 / 1 / 1 | 92% | Critica |
| c-1467_3705 | Crocetta - Cenisia | 14 | 12 / 0 / 2 | 86% | Critica |
| c-1468_3707 | San Donato | 13 | 8 / 3 / 2 | 85% | Critica |
| c-1462_3700 | Moncalieri | 5 | 2 / 2 / 1 | 80% | Critica |
| c-1466_3704 | San Salvario - Crocetta | 4 | 1 / 2 / 1 | 75% | Critica |
| c-1466_3705 | Crocetta - San Salvario | 4 | 3 / 0 / 1 | 75% | Critica |
| c-1468_3703 | Mirafiori Nord | 7 | 2 / 3 / 2 | 71% | Critica |
| c-1466_3703 | Nizza millefonti - San Salvario | 17 | 9 / 3 / 5 | 71% | Critica |
| c-1473_3706 | Collegno - Rivoli | 9 | 5 / 1 / 3 | 67% | Critica |
| c-1464_3701 | Moncalieri | 6 | 4 / 0 / 2 | 67% | Critica |
| c-1469_3704 | Grugliasco - Mirafiori Nord | 6 | 3 / 1 / 2 | 67% | Critica |
| c-1470_3704 | Grugliasco | 6 | 4 / 0 / 2 | 67% | Critica |
| c-1470_3706 | Parella | 6 | 2 / 2 / 2 | 67% | Critica |
| c-1466_3706 | Aurora | 3 | 1 / 1 / 1 | 67% | Critica |
| c-1467_3708 | Borgata Vittoria - Barriera di Milano | 3 | 1 / 1 / 1 | 67% | Critica |
| c-1472_3711 | Venaria Reale | 3 | 0 / 2 / 1 | 67% | Critica |
| c-1467_3702 | Mirafiori Sud - Mirafiori Nord | 22 | 7 / 4 / 11 | 50% | Scarsa |
| c-1470_3707 | Parella | 12 | 2 / 4 / 6 | 50% | Scarsa |
| c-1472_3706 | Collegno - Grugliasco | 10 | 4 / 1 / 5 | 50% | Scarsa |
| c-1466_3702 | Nizza millefonti - Mercati generali | 8 | 4 / 0 / 4 | 50% | Scarsa |
| c-1469_3706 | Parella - Pozzo Strada | 8 | 4 / 0 / 4 | 50% | Scarsa |
| c-1467_3704 | Crocetta - San Paolo | 6 | 1 / 2 / 3 | 50% | Scarsa |
| c-1470_3705 | Grugliasco - Pozzo Strada | 2 | 1 / 0 / 1 | 50% | Scarsa (dato indicativo) |
| c-1467_3707 | Aurora | 2 | 0 / 1 / 1 | 50% | Scarsa (dato indicativo) |
| c-1468_3705 | Cenisia - Pozzo Strada | 7 | 3 / 0 / 4 | 43% | Scarsa |
| c-1465_3699 | Nichelino | 5 | 1 / 1 / 3 | 40% | Scarsa |
| c-1465_3702 | Nizza millefonti - Moncalieri | 8 | 3 / 0 / 5 | 38% | Scarsa |
| c-1469_3702 | Beinasco | 6 | 2 / 0 / 4 | 33% | Scarsa |
| c-1465_3701 | Moncalieri - Nizza millefonti | 26 | 1 / 6 / 19 | 27% | Buona |
| c-1471_3706 | Collegno - Grugliasco | 8 | 1 / 1 / 6 | 25% | Buona |
| c-1469_3705 | Pozzo Strada - Grugliasco | 4 | 1 / 0 / 3 | 25% | Buona |
| c-1467_3706 | Cenisia - Aurora | 4 | 1 / 0 / 3 | 25% | Buona |
| c-1469_3709 | Madonna di Campagna | 4 | 1 / 0 / 3 | 25% | Buona |
| c-1470_3710 | Venaria Reale | 4 | 1 / 0 / 3 | 25% | Buona |
| c-1464_3700 | Moncalieri | 18 | 1 / 3 / 14 | 22% | Buona |
| c-1475_3706 | Rivoli | 6 | 1 / 0 / 5 | 17% | Buona |
| c-1474_3706 | Rivoli | 7 | 1 / 0 / 6 | 14% | Buona |
| c-1467_3710 | Falchera | 5 | 0 / 0 / 5 | 0% | Buona |
| c-1457_3701 | Chieri | 4 | 0 / 0 / 4 | 0% | Buona |
| c-1473_3707 | Collegno | 3 | 0 / 0 / 3 | 0% | Buona |
| c-1471_3707 | Parella | 3 | 0 / 0 / 3 | 0% | Buona |
| c-1465_3711 | Settimo Torinese | 3 | 0 / 0 / 3 | 0% | Buona |
| c-1466_3700 | Nichelino | 2 | 0 / 0 / 2 | 0% | Buona (dato indicativo) |
| c-1467_3709 | Falchera | 2 | 0 / 0 / 2 | 0% | Buona (dato indicativo) |
| c-1454_3697 | Chieri | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1467_3700 | Nichelino | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1465_3700 | Nichelino | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1465_3706 | Vanchiglia | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1472_3707 | Collegno | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1468_3708 | Borgata Vittoria | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1471_3710 | Venaria Reale | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |
| c-1465_3712 | Settimo Torinese | 1 | 0 / 0 / 1 | 0% | Buona (dato indicativo) |

## I 20 punti prioritari

1. **SETTEMBRINI** (Mirafiori Sud): 9 fermate, punteggio 618.9, posti entro 200 m 0. Candidati: nessuno entro 600 m.
2. **PAVESE** (Mirafiori Sud): 8 fermate, punteggio 569.0, posti entro 200 m 0. Candidati: nessuno entro 600 m.
3. **INDUSTRIA** (San Donato): 8 fermate, punteggio 534.8, posti entro 200 m 28. Candidati: OSM way 310919719 (465 m, 136 posti, non_misurato); FORTINO (498 m, 125 posti, non_misurato).
4. **METRO SPEZIA** (Nizza millefonti): 7 fermate, punteggio 525.5, posti entro 200 m 16. Candidati: BACIGALUPO (205 m, 326 posti, a_meta); VENTIMIGLIA (247 m, 303 posti, pieno); C.T.O. (254 m, 162 posti, non_misurato).
5. **PROVANA** (Collegno): 7 fermate, punteggio 522.9, posti entro 200 m 12. Candidati: nessuno entro 600 m.
6. **METRO LINGOTTO** (Nizza millefonti): 6 fermate, punteggio 428.3, posti entro 200 m 36. Candidati: OSM way 122239101 (430 m, 114 posti, non_misurato); LINGOTTO (440 m, 3100 posti, libero); Parcheggio L (487 m, 1738 posti, non_misurato).
7. **POLITECNICO** (Crocetta): 6 fermate, punteggio 398.8, posti entro 200 m 0. Candidati: OSM way 106366574 (511 m, 420 posti, non_misurato); Parcheggio Stati Uniti (558 m, 520 posti, non_misurato).
8. **STATI UNITI** (Crocetta): 5 fermate, punteggio 396.5, posti entro 200 m 0. Candidati: PORTA NUOVA FS (422 m, 242 posti, pieno).
9. **METRO PRINCIPI ACAJA** (San Donato): 5 fermate, punteggio 375.1, posti entro 200 m 0. Candidati: BOLZANO (236 m, 858 posti, a_meta); PORTA SUSA FS (256 m, 123 posti, a_meta); PALAGIUSTIZIA (388 m, 616 posti, libero).
10. **TRAIANO** (Mirafiori Sud): 5 fermate, punteggio 360.7, posti entro 200 m 78. Candidati: CAIO MARIO (206 m, 418 posti, libero); OSM way 612685927 (326 m, 200 posti, non_misurato).
11. **MARSÈ** (Moncalieri): 5 fermate, punteggio 358.4, posti entro 200 m 21. Candidati: OSM way 375014428 (394 m, 135 posti, non_misurato).
12. **METRO BERNINI** (San Donato): 5 fermate, punteggio 351.0, posti entro 200 m 38. Candidati: BIXIO (556 m, 255 posti, libero).
13. **METRO NIZZA** (San Salvario): 5 fermate, punteggio 350.0, posti entro 200 m 46. Candidati: nessuno entro 600 m.
14. **SAN MATTEO** (Moncalieri): 5 fermate, punteggio 346.4, posti entro 200 m 96. Candidati: Piazza Bengasi (470 m, 463 posti, non_misurato); OSM way 1115777654 (573 m, 109 posti, non_misurato).
15. **AVELLINO** (San Donato): 5 fermate, punteggio 334.9, posti entro 200 m 40. Candidati: RICHELMY (61 m, 115 posti, a_meta).
16. **METRO ITALIA61** (Nizza millefonti): 4 fermate, punteggio 300.1, posti entro 200 m 0. Candidati: OSM way 104393338 (558 m, 568 posti, non_misurato).
17. **XXIV MAGGIO** (Collegno): 4 fermate, punteggio 299.2, posti entro 200 m 12. Candidati: OSM way 211478725 (27 m, 105 posti, non_misurato); OSM way 192975576 (579 m, 141 posti, non_misurato).
18. **DROSSO CAP** (Mirafiori Sud): 4 fermate, punteggio 294.9, posti entro 200 m 24. Candidati: UNIONE SOVIETICA (311 m, 150 posti, non_misurato).
19. **MACEDONIA** (Collegno): 4 fermate, punteggio 287.9, posti entro 200 m 48. Candidati: nessuno entro 600 m.
20. **LEONARDO DA VINCI** (Grugliasco): 4 fermate, punteggio 279.3, posti entro 200 m 0. Candidati: OSM way 1120098134 (95 m, 525 posti, non_misurato).

## Controlli

Script 80, tutti OK: 378 fermate; classi 147 / 59 / 172; ogni fermata in una sola area (somma 378); 73 aree (tra 55 e 110); auto in entrata 95.297 (±1) e domanda 24.459 (±5); nessun valore negativo; soglia 10% riproduce le 378 fermate di S2; Palavela tra i parcheggi mostrati con almeno 500 posti; tutti i garage 5T con dati sono mostrati; 212 parcheggi mostrati (tra 190 e 240).
Script 79, tutti OK: 378 fermate (147 / 59 / 172), 73 aree, 20 punti, 212 parcheggi, 41 profili.

## Verifica a posteriori (non entra nei dati)

Fermi (raggio 500 m): 20 parcheggi considerati nel raggio, nessuno misurato dal 5T. Il metodo **non può confermare** l'osservazione «sempre pieno»: il riempimento misurato non c'è per questi parcheggi.

## Scostamenti dal piano

1. **Garage 5T con dato di riempimento**: il piano scrive 36. Nel file ce ne sono 41 con un profilo, di cui **32 con la media feriale** e 37 con almeno 2 giorni validi. Ho usato i 32 come «garage con dati»; i 41 profili compaiono nella scheda.
2. **Parcheggi da 50+ entro 200 m da una fermata importante**: 124 (23.819 posti) contro 122 (23.566) del piano. Il dato da fermate o nodi forti (194; 38.146 posti; circa il 22%) coincide con il piano.
3. **Validazione dei 25 m²**: mediana 24.4 su 172 parcheggi, contro 25,4 su 152 del piano. La fascia è larga (14.2-32.7), quindi il dato resta un'indicazione, non una taratura.
4. **Parcheggi mostrati**: 212 (il piano diceva circa 209 più i garage: il numero compreso nei garage).
5. **Quota dei posti misurati**: 25.2% dei posti mostrati. Il dato precedente (36,3%) si riferiva a un altro insieme di parcheggi.
6. **Direzioni**: il riferimento usa ora i posti nominali, non più i «posti utili», perché il termine è stato tolto.

## File modificati o creati

Modificati: `scripts/80_porte_interscambio.py` (riscritto), `scripts/79_dati_mappa_r6.py` (riscritto), `scripts/mappa_template.html`, `scripts/04_genera_mappa.py`, `scripts/schede_risultati.py`, `simulazione.html`.
Generati: `data/processed/risultato6_v2/porte.json`, `data/processed/risultato6_v2/mappa_r6.json`, `docs/RAPPORTO_R6_PORTE.txt`, `mappa_torino.html`, `data/schede_risultati.js`, `data/processed/risultato6_riepilogo_mappa.json`.
Non toccati: `MEMORIA_PROGETTO.md`, `data/ref/*`, `data/raw`, lo storico.

## Anomalie e cose da sapere

1. **Mappa non verificata nel browser.** Il browser integrato non apre `localhost` né il file locale. Ho controllato la sintassi JavaScript e i dati. Va aperta a mano: `mappa_torino.html`, tema «Parcheggi per lasciare l'auto», menu «Cosa vedere».
2. **Molte aree piccole.** 26 delle 73 aree hanno meno di 3 fermate (bordo tratteggiato, dato indicativo): sono i bordi della nuvola di fermate. Il piano fissa il lato a 900 m.
3. **Aree a 0% o 100%.** Le celle con 1-2 fermate hanno quote estreme per caso; vanno lette con cautela.
4. I profili singoli sono sei nella scheda e tutti hanno pochi giorni di misura [DATI SCARSI].
5. Restano aperti: 23 luoghi senza zona IMQ (fuori dalle 378), la lista di altri parcheggi «sempre pieni» da Leo (solo per verifica), e il fetch del 25/10 con la catena 71 → 72 → 73 → 75 → 76 → 80 → 79.
