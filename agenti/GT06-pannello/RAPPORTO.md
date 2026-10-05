# Rapporto GT06-pannello

Modificato solo `scripts/mappa_template.html`. Non ho potuto eseguire nulla: i controlli li fa il runner.

## Cosa ho fatto
Ordine del pannello, dall'alto: titolo, **Quando**, **Tema** (con descrizione), Sovrapposizioni, Sfondo e filtro, Segnalazioni (solo dove visibili), "Cosa stai guardando e limiti", **Info sui dati** (chiuso), **Legenda**.

1. **Quando**: l'h2 ora è "Quando". Riga 1: Feriale/Sabato/Domenica + Adesso. Riga 2: play/pausa, cursore dell'ora, orario, velocità (1×, 10×, 60×, 240×). Sotto c'è la frase "La mappa mostra il servizio di un giorno feriale/un sabato/una domenica alle HH:MM". Si aggiorna con il cursore, con i bottoni, con Adesso, durante la simulazione e con il replay. Tutti gli id sono invariati (`#giorno`, `#ora`, `#oraTxt`, `#adesso`, `#play`, `#vel`, `#nAtt`).
2. **Tema**: un solo `<select id="temi">` costruito da THEMES. Un tema nuovo compare aggiungendo una riga alla tabella. Il tema di partenza è Offerta. `#temaDesc` resta sotto il menu. Le scelte di Pendolari (`#boxPend`) sono subito sotto.
3. **Legenda**: `#legenda` è dentro il pannello, ultimo blocco, con h2 "Legenda". Ho tolto la posizione flottante e la regola che la nascondeva sotto 640 px. `aggiornaLegenda()` è invariata, tranne che nasconde anche il titolo quando non c'è nulla da mostrare.
4. **Tag PROGRAMMATO**: tolto dove era l'unico tag (Offerta, Zone, Linee, Fermate). Restano:
   - MISURATO e STIMATO/SIMULATO;
   - CENSIMENTO;
   - "dati scarsi";
   - PROGRAMMATO nei blocchi misti ("Poca offerta per abitante" = PROGRAMMATO + CENSIMENTO, "Linee: mezzi reali rispetto al previsto" = MISURATO + PROGRAMMATO).
5. **Info sui dati**: `<details id="infoDati">`, chiuso all'avvio, con dentro `#stato` e `#statoLive`. `#boxSegn` è rimasto com'era, con la sua logica per tema.

## Scelte
- "Cosa stai guardando e limiti" resta sopra "Info sui dati", per lasciare la legenda come ultimo blocco.
- Il blocco "Sfondo e filtro" è sceso sotto "Sovrapposizioni", come da ordine richiesto.
- Il sottotitolo sotto "Mobilità Torino" non è stato toccato.
- Sul telefono (< 640 px) la legenda ora si vede, dentro il pannello. Prima era nascosta.

## Da provare (Leo)
1. Apri `mappa_torino.html`, dopo che il runner l'ha rigenerata.
2. Menu Tema: scegli uno dopo l'altro Nessuno, Offerta, Domanda, Poca offerta per abitante, Zone statistiche, Traffico, Tempo reale, **Velocità**, **Pendolari**. Per ognuno controlla che cambino la mappa, la descrizione e la legenda in fondo al pannello. Con Pendolari devono comparire i tre menu Lavoro/Direzione/Colore. Con Traffico e Tempo reale deve comparire "Segnalazioni adesso".
3. Clicca Feriale, Sabato, Domenica, muovi il cursore e premi Adesso, play e pausa, cambia la velocità. La frase sotto "Quando" deve cambiare di conseguenza.
4. Clicca "Info sui dati": deve aprirsi e mostrare Aggiornamento e Dati raccolti, poi richiudersi.
5. Accendi e spegni le sovrapposizioni: la legenda in fondo si aggiorna.
6. Restringi la finestra: non deve esserci nessun riquadro sovrapposto. Il pannello scorre al suo interno.

## Domande per Leo
Nessuna bloccante.
