# Risultato 5 (script 95) — Case, servizi e fragilità

Solo Torino; unità = zona OMI (46 zone con almeno 500 abitanti e prezzo); le sezioni di censimento si sommano nella zona, pesate per abitanti. Rapporto completo: `docs/rapporti/RAPPORTO_CASE_FRAGILITA_SERVIZI.txt`; numeri: `data/processed/case_fragilita_servizi.json`.

## Legami a parità di distanza dal centro (giro L9, 24/10/2026)

Regole fissate prima dei numeri: correlazione **parziale sui ranghi** a parità di distanza dal centro della zona a Piazza Castello; intervallo al 95% per ricampionamento delle zone (2.000 volte, seme 95); **«regge» solo se l'intervallo non contiene lo 0**.

| Legame | Spearman (intervallo 95%) | A parità di distanza (intervallo 95%) | Regge |
|---|---|---|---|
| prezzo-servizi | +0,61 (+0,39 / +0,79) | +0,21 (−0,12 / +0,52) | no |
| fragilita-servizi | −0,74 (−0,83 / −0,59) | −0,48 (−0,66 / −0,23) | sì |
| prezzo-fragilita | −0,83 (−0,91 / −0,68) | −0,69 (−0,85 / −0,37) | sì |

Il punto chiave sul prezzo dice quindi: a parità di distanza dal centro il legame prezzo-servizi quasi sparisce (la correlazione semplice, +0,61, era in gran parte l'effetto del centro); reggono fragilità-servizi e prezzo-fragilità.

## Doppio svantaggio contro il caso

Sezioni di Torino con almeno 1.000 abitanti per km². Fragilità alta (20% più alto) per il 26.4% dei residenti, servizi bassi (20% più basso) per il 21.5%: se le due condizioni fossero indipendenti, le avrebbe entrambe il 5.67%; le ha il **9.48%**, cioè **1,67 volte quanto ci si aspetterebbe per caso**. Residenti: 79,598.

## Altro

Il grafico «metro/prezzi» non è più nella scheda; il confronto fra zone con e senza metro a pari distanza resta nel rapporto (E3: differenza fra zone, non effetto causale). Limiti: quotazioni OMI e non compravendite, un solo semestre, zone grandi, l'indice di fragilità non è il reddito.
