# GT01-sfondi – Rapporto

## Cosa ho fatto (solo scripts/mappa_template.html)
- Rimossi tutti gli URL tile.openstreetmap.org.
- Sfondi, tutti Esri senza chiave: Satellite (World_Imagery, zoom max 19), Mappa chiara (Canvas/World_Light_Gray_Base, max 16), Mappa stradale (World_Street_Map, max 19), Nessuno sfondo (grigio chiaro).
- Oltre lo zoom massimo viene ingrandita la mattonella dello zoom massimo (overzoom). Limiti della cache invariati (600/200).
- Sfondo predefinito: satellite.
- Cursore "Intensità sfondo" 0-100% (predefinito 70%): un solo rettangolo bianco semitrasparente per fotogramma.
- Crediti Esri corretti per ogni sfondo, più "dati GTT, 5T, ISTAT, Comune di Torino".
- Avviso "Sfondo non disponibile (connessione?)" se falliscono più di 20 mattonelle e nessuna è arrivata; non blocca i dati.

## Scelte
- Il cursore schiarisce verso il BIANCO (non scuro).
- Rimosso il filtro grigio sulla "chiara": Esri è già grigio chiaro.
- Il valore "osm" non esiste più; "stradale" lo sostituisce.
- I contatori di errore si azzerano al cambio sfondo.

## Non verificato
Non posso eseguire la pagina: i testi dei crediti Esri sono quelli abituali, da controllare sui termini Esri.

## Cosa cliccare per provare
1. Apri la mappa: deve partire sul satellite, cursore a 70%.
2. Menu sfondo: prova Satellite, Chiara, Stradale, Nessuno; guarda i crediti in basso a destra.
3. Su "Mappa chiara" zooma a 17-18: lo sfondo deve restare visibile (ingrandito, più sfocato), senza buchi.
4. Muovi il cursore da 0 a 100%: a 0% quasi bianco, a 100% sfondo pieno; i livelli dati restano leggibili.
5. (Facoltativo) Scollega la rete e cambia sfondo: deve comparire l'avviso.
