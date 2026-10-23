# ESITO L8 (24/10/2026): TomTom stima principale, più percorsi, Release nuova

Decisione di Leo, presa dopo aver visto i numeri di L6bis: i tempi in auto si prendono da TomTom; i sensori 5T restano come «stima più favorevole all'auto». Motivo: difetto di metodo provato (rete ai limiti di velocità, senza semafori), non i risultati. Regole del blocco L8 non cambiate dopo i numeri.

## Richieste TomTom
- Nuove: **1.171** (martedì 10/11/2026): C1 coppie 101-600 alle 8 (500), C2 coppie 101-300 alle 13, 17:30, 21 (600), D Piazza Castello → zone (**71**, non 101: le altre zone hanno solo «porte», senza punto di calcolo). Tetto 2.000 rispettato, nessun rifiuto. Totale con L6bis: 2.371.
- Si salvano solo rapporti a 2 decimali (`per_percorso`, `regola_coppie`, `mediane_gruppo` in `tempi_traffico.json`), mai minuti.
- **Coerenza** (100 coppie, martedì contro media): differenza mediana 0,009 / 0,007 / 0,007 / 0,003 alle 8 / 13 / 17:30 / 21: sotto 0,05, nessun AVVISO. Controllo contro Google: 1,98 contro 2,1 (passa).
- AVVISO: 6 valori su 1.671 di fattore_rete fuori da 1-5 (0,87-5,12).

## Tabella prima (L6bis) / dopo (L8), alle 8 salvo indicazione
| | Prima | Dopo |
|---|---|---|
| 12 punti: conviene / dipende / non conviene | 0 / 7 / 5 | 8 / - / 4 (due classi) |
| 5 interscambi | 0 / 5 / 0 | 4 / - / 1 (Sofia non conviene) |
| Minuti di pareggio, mediana punti (TomTom - sensori) | 17-28 | 16-28 |
| Rapporto mediano scheda 4, 8:00 (TomTom - sensori) | 1,75 - 2,94 | 1,85 - 2,94 |
| 13:00 | 1,96 - 3,10 | 2,10 - 3,10 |
| 17:30 | 1,79 - 3,02 | 1,92 - 3,02 |
| 21:00 | 2,14 - 3,32 | 2,30 - 3,32 |
| Auto oltre 2 (TomTom), 8:00 | 13,8% | 35,4% |
| Titolo / numero grande scheda 4 | «da 2 a 3 volte» | «Al mattino… 1,9 volte» (regola ±0,3: non scatta, 21:00 è +0,45) |
| Auto con fattore del proprio percorso (8:00) | 0 (mediana unica) | 83,2% delle auto (600 coppie su 2.061); alle altre ore circa 60% |
| Torinesi in auto da Piazza Castello, TomTom, 10/20/30/45 min | 1,3 / 43,3 / 93,9 / 100 % | 1,9 / 37,8 / 90,1 / 100 % |
| Punti dove il bus conviene 8/13/17:30/21 | - | 8 / 6 / 9 / 2 su 12 |

Fattori: luoghi in entrata da 1,88 a 4,10; coppie 101-600 mediana 2,14 alle 8; zone 1,88.

## Come cambia il messaggio
- Scheda 3: titolo invariato (fermate senza posti). Ora il bus «conviene» (≤ 1,5) da 8 punti su 12 con TomTom; batte l'auto solo se in centro si perdono più di 16 minuti (28 con i sensori).
- Scheda 4: regge ma il numero scende: 1,9 volte con TomTom (2,9 con i sensori); la quota oltre 2 sale al 35% perché il fattore è per percorso.
- Area: l'auto raggiunge il 90% dei torinesi in 30 minuti (94% col fattore unico).

## AVVISI da sapere
- Piazza Castello → Collegno con il fattore proprio: 36,5 minuti, fuori dalla fascia 20-35 del controllo (non bloccante).
- Script 100: «21:00 mezzi non più lenti che alle 8» (vecchio, noto). Script 99: Porta Nuova 16 minuti coi mezzi (vecchio).

## Altro
- Home: la figura «Muoversi» legge un solo numero; «minuti di pareggio» della home ora legge il pareggio TomTom (prima leggeva il numero di fermate per errore).
- Area: scelta di default TomTom; tabella TomTom (sensori).
- Nuova prova `scripts/prove/prova_fattori_tomtom.py` (in CI). pyflakes zero, `schede_risultati.py` senza ATTENZIONE, Playwright 0 errori su 20 pagine.
- `scarica_dati.py` scarica «l'ultima Release» (`latest`): dopo la pubblicazione di `dati-2026-11` prende quella, nessuna modifica necessaria.

## Release dati-2026-11 (cartella `C:\projects\Progetti\GTT_release`)
dati-grezzi-istat-2026-11.zip 280,7 MB · dati-grezzi-altri-2026-11.zip 27,1 MB · dati-calcolati-2026-11.zip 96,8 MB · SHA256SUMS.txt.
Passi (a mano): GitHub → Releases → Draft a new release → tag `dati-2026-11` → trascina i 3 zip e `SHA256SUMS.txt` → Publish. Poi: prova da zero con `scarica_dati.py`.

## Ancora da fare (Leo)
Leggere le condizioni d'uso di TomTom prima di unire in main; guardare schede 3 e 4, area, README; non unire in main finché non dice OK.
