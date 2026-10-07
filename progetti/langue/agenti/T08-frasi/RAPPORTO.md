# Rapporto T08-frasi

## Cosa ho fatto
Creato `contenuti/frasi.json`: 50 frasi (`fra-0001`..`fra-0050`), tutte `stato: bozza`, `origine: agente T08-frasi`, `fonte: conoscenza del modello`. Livelli: A1 e A2.

Distribuzione: 15 principali V2 (0001–0015), 8 con inversione (0016–0023), 8 domande (0024–0031), 8 con modale (0032–0039), 6 con verbo separabile (0040–0045), 5 tempo-modo-luogo (0046–0050).

## Cosa ho controllato
- Campi e limiti secondo SCHEMA.md e `schema/contenuto.schema.json` (4–9 blocchi, punteggiatura attaccata all'ultimo blocco).
- `testo_de` scritto come i blocchi uniti da uno spazio, controllato a mano record per record.
- **Non ho potuto eseguire alcuno script** (Bash non disponibile): la validazione automatica (blocchi = testo, JSON valido) non è stata fatta. Conviene lanciare il validatore del progetto.

## Scelte
- Dove un altro ordine è corretto (di solito l'inversione con tempo/luogo in prima posizione) l'ho messo in `alternative`. Il gioco deve accettarlo.
- Le frasi 0016–0023 sono inversioni: la versione non invertita sta in `alternative`.
- Ho evitato i sostantivi con articolo incerto.
- Alcune traduzioni sono libere per naturalezza (es. 0020, 0022).

## Le 5 frasi di cui sono meno sicuro
1. **fra-0014** «Mein Bruder spielt sehr gut Gitarre.» – corretta, ma «Gitarre spielen» + «sehr gut» ammette anche «…spielt Gitarre sehr gut»; non l'ho elencata come alternativa.
2. **fra-0002** «Die Kinder spielen im Garten Fußball.» – l'ordine con luogo prima dell'oggetto è naturale, ma quello in alternativa suona forse più comune.
3. **fra-0028** «Trinkst du gern Kaffee mit Milch?» – «gern» prima dell'oggetto è giusto; altri ordini possibili non elencati.
4. **fra-0035** «Mein Sohn darf nicht so lange fernsehen.» – corretta; «nicht so lange» ammette qualche variante d'ordine.
5. **fra-0020** «Am Wochenende besucht mein Onkel uns.» – corretta (pronome dopo il soggetto pieno, ordine neutro), ma «…besucht uns mein Onkel» è anch'essa possibile e non elencata.

## Da rivedere (Leo)
Verificare soprattutto se vuoi più ordini alternativi per 0002, 0014, 0020, 0028 (il gioco potrebbe rifiutare ordini validi).
