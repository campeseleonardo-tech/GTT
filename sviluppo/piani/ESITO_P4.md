# ESITO P4 — giro dopo la divisione delle schede (22/10/2026)

## Cosa è andato diverso dal prompt (leggere per primo)
Il prompt partiva da uno stato che sul PC non c'era più:
- `git status` pulito, `git stash list` vuoto, nessun `data\schede_risultati_PRIMA.js`.
- Il ramo `origin/claude/ecstatic-faraday-nuy8hv` **non esiste** su origin (`git fetch origin` non lo porta). I commit C6 (`b67d39b`, `52144a5`) sono **già** in `prova`.
- Esiste già il commit `04fd345 "P4: schede rigenerate dopo la divisione, inglese verificato"` (Leo, 22/10 16:27): ha già rigenerato mappa e schede. Cambia solo `generato` nelle schede, i 5 riepiloghi `risultato*_riepilogo_mappa.json`, `mappa_torino.html`, `data/catalogo/reti.js`.
- Quindi i passi 1, 2 e 5 NON rifatti da me (niente da unire; rigenerare di nuovo cambierebbe solo le date). La copia PRIMA non si può creare: `data\schede_risultati.js` ha già `forma_en`.

## Passi
1. Merge del cloud — **non fatto** (già unito prima; ramo cloud assente).
2. Rigenera — **non fatto** (già fatto in `04fd345`). Non ho il log con eventuali righe «ATTENZIONE … senza traduzione»; `logs\rifai_mappa_e_schede.log` è di Leo.
3. Stessi numeri — **fatto, con un'altra base**. Come PRIMA ho usato la versione in git prima di C6: `git show 377fa55:data/schede_risultati.js`. Confronto in Python togliendo `generato` e `forma_en`.
   Risultato: 5 schede su 5, **nessuna differenza** (né numeri né testi italiani, né chiavi aggiunte o tolte).
   Limite: la base è l'ultima versione in git prima di C6, non la copia fatta a mano da Leo.
4. Prova delle pagine — **fatto**: `python scripts\prova_pagine.py` → «OK: nessun errore a runtime sulle 19 pagine». Nulla da cancellare (niente PRIMA, niente stash).
5. Commit dei rigenerati — **non fatto** (già in `04fd345`).
6. Inglese — **fatto**. Mostrati 3 gruppi da 18 frasi (1-54); Leo: «nessuna» per tutti e ha detto che anche le successive vanno bene. `testi.json` non toccato.
7. Controllo a occhio — **fatto** (browser interno, `python -m http.server` da `.claude/launch.json`, finestra 800x600). Non corretto nulla.
8. Chiusura — **fatto**: `PROMPT_LAVORI.md` (P4 FATTO 22/10), `MEMORIA_PROGETTO.md` (ancora 120 righe).

## Frasi cambiate
Nessuna.

## Controllo a occhio: cosa si vede e difetti (non corretti)
Visto in inglese: scheda 2, 3 e 5 si aprono e sono leggibili (grafici, omini, pallini, barre); bottone IT sulla home → titolo e `lang` passano all'italiano.
Difetti:
1. **Stemma**: nel piè della home («About me», link, licenza) non c'è nessuno stemma; nel progetto non c'è nessun file o riferimento «stemma». Se doveva esserci, manca.
2. **Scheda 5, incoerenza**: titolo «1 Turin resident in 11» ma sotto «About 1 in 10» (9,5% dei residenti; gli omini sono 10).
3. Home: il numero della scheda 5 passa da «0» a 79,598 solo dopo qualche secondo (animazione; è normale se parte dallo scorrimento, ma in uno screenshot veloce si vede «0»).
4. Dopo il cambio lingua l'indirizzo resta `?lang=en` (la pagina è già in italiano): solo estetico.
5. Su `risultati.html` il clic su IT con la scheda aperta ha cambiato l'indirizzo (tolto `#p5` e `?lang`) ma lo screenshot subito dopo mostrava ancora la pagina in inglese: non verificato se è un ritardo del disegno o un difetto. Da riprovare a mano.
Non guardato: la mappa (resta in italiano), le altre schede, telefono.
