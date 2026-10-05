# Rapporto T10-errori

## Cosa ho fatto
Creato `contenuti/errori.json`: 30 record tipo "errore" (err-0001..err-0030), tutti `stato: bozza`, `origine: agente T10-errori`, `fonte: conoscenza del modello`.

Distribuzione: articolo 6 (0001-0006), genere 6 (0007-0012), altro 3 (0013, 0029, 0030), ordine_verbo 6 (0014-0019), falsi_amici 6 (0020-0025), preposizioni 3 (0026-0028). Livelli misti A1/A2.
Gli id non sono raggruppati per categoria: 0013 è «altro» e si trova in mezzo.

## Controlli
- Ogni coppia sbagliata/corretta differisce solo per l'errore (negli errori di costruzione, come età/freddo, l'intera espressione cambia perché l'errore è la costruzione).
- Campi usati solo quelli dello schema. Non ho eseguito un validatore automatico (l'ho scritto a mano rispettando lunghezze e valori).

## Scelte
- «articolo» = forma dell'articolo sbagliata per caso/declinazione; «genere» = genere sbagliato per influenza dell'italiano.
- Evitati nomi con genere regionale (es. «der/die Butter»).
- Evitato «aktuell»: in tedesco significa anche «attuale», quindi non è un falso amico netto.

## Da rileggere: i 5 meno sicuri
1. err-0025 «brav» vs «gut»: «brav» è corretto in tedesco, ma è un falso amico meno noto; la frase sbagliata è comprensibile e di registro discutibile.
2. err-0028 «Angst von» vs «Angst vor»: errore plausibile, ma meno frequente di altri.
3. err-0009 «den Milch»: l'errore tipico è l'articolo maschile da «il latte»; la frase con «die Milch» + articolo è un po' innaturale (meglio «Milch» senza articolo).
4. err-0020 «bekommt Arzt»: l'errore tipico è più spesso «Ich bekomme müde»; la frase scelta è semplificata.
5. err-0022 «Gymnasium»: «ins Gymnasium gehen» è corretto in tedesco con altro senso; l'errore dipende dal contesto (qui «dreimal pro Woche» lo rende chiaro).
