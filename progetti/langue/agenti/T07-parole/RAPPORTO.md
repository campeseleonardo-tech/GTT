# Rapporto T07-parole

**Fatto:** creato `contenuti/parole_nuove.json` con 100 sostantivi nuovi (art-0201 … art-0300), tipo "articolo", stato "bozza", origine "agente T07-parole". Un record per riga, per rilettura rapida.

**Controlli:** ho confrontato a mano ogni parola con l'elenco delle 200 esistenti (nessuna uguale, nessun singolare/plurale duplicato) e non ci sono doppioni interni. Articoli e traduzioni riletti uno per uno. Il file contiene solo campi dello schema. **Non ho potuto eseguire script (Bash disabilitato)**, quindi non ho validato il JSON con un programma: conviene un controllo automatico.

**Temi (10 parole ciascuno):** abbigliamento, acquisti e denaro, ristorante, viaggio/hotel, salute, sport e tempo libero, tecnologia, posta/banca/ufficio, sentimenti, feste.

**Scelte:**
- Traduzioni con l'iniziale maiuscola, come nel file esistente.
- Livello A1/A2 a mio giudizio.
- `note` solo dove la traduzione ha un secondo significato o serve un chiarimento.
- Esclusi nomi senza articolo o ambigui (Weihnachten, Ostern, Silvester) e varianti regionali.

**Le 5 parole di cui sono meno sicuro** (articoli corretti per quanto so; i dubbi riguardano livello e traduzione):
1. Gleis (das) – "binario"; livello forse A2.
2. Fußball (der) – "calcio" (sport) vs "pallone", segnalato in nota.
3. Bank (die) – "banca"; la nota sul plurale/panchina serve a chiarire che sono due parole omografe (Banken / Bänke).
4. Glück (das) – "fortuna" / "felicità": ho scelto il primo significato.
5. Humor (der) – "umorismo"; in uso corrente soprattutto in "Sinn für Humor".
