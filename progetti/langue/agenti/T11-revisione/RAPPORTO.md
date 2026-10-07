# Rapporto T11-revisione

Seconda lettura indipendente di 100 parole, 50 frasi, 30 errori. Non ho eseguito programmi: la validazione la fa il runner. Nessun record è stato impostato a "verificato", nessun id/origine/ordine cambiato.

## contenuti/parole_nuove.json (100 record)

| id | cosa ho cambiato | perche' |
|---|---|---|
| art-0286 (Ärger) | stato → da_verificare, riga in note | "Rabbia" è dubbio: Ärger è più "fastidio/irritazione"; la rabbia forte è "Wut". Non sono certo che sia sbagliato (alcuni dizionari lo danno), quindi decide Leo |

Articoli controllati tutti: nessuno sbagliato. Casi a rischio verificati: das Gleis, die Bank (stesso articolo per banca e panchina, cambia solo il plurale Banken/Bänke: la nota è corretta), das Gepäck, der Euro, die E-Mail, das Passwort, das Formular, die Party, der Spaß, der Husten, das Fieber.
Lasciati invariati: 99 su 100. I livelli A1/A2 non li ho toccati (opinabili, non errori).

## contenuti/frasi.json (50 record)

Tutte le frasi sono grammaticali e naturali, traduzioni ok. Ho solo aggiunto alternative corrette mancanti:

| id | cosa ho cambiato | perche' |
|---|---|---|
| fra-0002 | + "Im Garten spielen die Kinder Fußball." | inversione con luogo in prima posizione, neutra |
| fra-0003 | + "In der Stadt haben wir eine kleine Wohnung." | idem |
| fra-0012 | + "Unter dem Tisch sitzt die Katze." | idem |
| fra-0014 | + "Mein Bruder spielt Gitarre sehr gut." | "sehr gut" può seguire l'oggetto |
| fra-0020 | + "Am Wochenende besucht uns mein Onkel." | con pronome oggetto, "uns" prima del soggetto pieno è anzi l'ordine più naturale; l'originale resta corretto ma meno comune |
| fra-0033 | + "Hier kannst du nicht parken." | inversione |
| fra-0036 | + "Sie kann Deutsch sehr gut sprechen." | ordine alternativo corretto |
| fra-0043 | + "Oft ruft mich mein Freund an." | inversione con avverbio |

Non aggiunti (corretti ma enfatici/marcati, es. oggetto in prima posizione): 0001, 0007, 0010, 0028 ("Trinkst du Kaffee gern mit Milch?" è possibile ma sposta l'enfasi), 0031, 0037. Lasciati invariati: 42 su 50 (nessun campo toccato oltre alle alternative sopra).

## contenuti/errori.json (30 record)

| id | cosa ho cambiato | perche' |
|---|---|---|
| err-0013 | spiegazione corretta, note | la spiegazione diceva "sei/tuo" ma la frase è in prima persona ("sono / il mio corpo") |
| err-0020 | spiegazione corretta, stato → da_verificare, note | la spiegazione attribuiva la confusione a un "suono simile a diventare": falso. Bekommen/become è un falso amico con l'INGLESE; per un italiano l'errore è meno tipico. Decide Leo se tenere il record |

Frasi sbagliate con un solo errore e frasi corrette: tutte ok. Osservazioni lasciate senza modifiche:
- err-0021 (Gift), err-0023 (also): errori tipici soprattutto via inglese, spiegazione vera.
- err-0022 (Gymnasium) e err-0025 (brav): la frase sbagliata è grammaticale, sbagliata solo di senso/contesto; accettabile come "falso amico".
- err-0029: cambiano due elementi (haben→sein, + alt) ma è un'unica costruzione, ok.
- err-0011: l'esempio "das System" ha come equivalente italiano "sistema" (in -ma): ok, ma l'ordine potrebbe confondere.
Lasciati invariati: 28 su 30 (di cui 0013 e 0020 modificati sopra).

## Scelte
- Per Ärger ho scelto "da_verificare" invece di cambiare la traduzione (non certezza).
- Note in italiano, brevi, con prefisso "T11:".
