# Piano traffico veicolare — Fase 3-bis (modello più realistico) e Fase 4 (traffico × trasporto pubblico)

Scritto il 17/10/2026, dopo l'esito della Fase 3 (`docs/ESITO_FASE3_TRAFFICO.md`: classe **C-DEBOLE**, errore mediano 31,9%,
Spearman 0,602, n=20). Piani precedenti: `docs/PIANO_TRAFFICO_5T.md` (decisioni di fondo), `docs/PIANO_TRAFFICO_FASE2.md`
(Fasi 1-2 e idea della Fase 4), `docs/PIANO_TRAFFICO_FASE3.md` (criteri di riuscita, che restano validi).

## 0. Obiettivo, in parole semplici

Trovare le strade di Torino con **molto traffico e poco trasporto pubblico** (bus/tram). Servono quindi due cose per ogni strada: quanto traffico
di auto c'è (stima, con la sua accuratezza) e quanti passaggi di bus/tram ci sono (dagli orari). Poi si incrociano.

## 1. Decisioni di Leo (17/10)

1. **Modello più realistico "quanto basta"**: un solo pacchetto di miglioramenti scelto prima di vedere i risultati (sezione 3), valutato una volta.
   Se non migliora, si tiene il modello attuale (V0) e si va avanti senza altri tentativi.
2. **Il risultato finale deve avere sia numeri assoluti (con l'accuratezza che riusciamo ad ottenere), sia valori relativi, sia una graduatoria.** Questo
   cambia SOLO la regola di pubblicazione: la classe di esito (C-ASSOLUTO / C-INDICE / C-DEBOLE / C-NO) resta quella calcolata con i criteri fissati
   nella Fase 3 e va scritta accanto a ogni numero. I numeri assoluti si pubblicano sempre con la fascia di errore (sezione 5).
3. Il raccoglitore corretto sul Pi è già stato avviato da Leo (17/10). Verifica del suo esito: sezione 7.
4. Fase 4 parte con l'offerta di trasporto pubblico (non dipende dal modello del traffico) e si incrocia dopo.
5. Prima l'analisi, la mappa dopo (e solo se Leo la chiede).

## 2. Regole per l'agente (valgono per tutti i pacchetti)

Le stesse del piano della Fase 3 (sezione 2), in breve: cartella `C:\projects\Progetti\GTT`; leggi `AGENTS.md` e `MEMORIA_PROGETTO.md`; ramo `prova`
(se no, fermati); **nessun commit**; database storico e `data/raw` in sola lettura; non scrivere né riavviare nulla sul Pi; non modificare `MEMORIA_PROGETTO.md`,
`scripts/mappa_template.html`, `scripts/04_genera_mappa.py`; copia `.bak_17ott` prima di cambiare un file esistente; Python del PATH (no Anaconda); `pip --user` per
pacchetti comuni (da annotare); nessun servizio esterno; PC con 8 GB di RAM; calcoli lunghi in un `.bat` a parte, ripartibili, con log. Script numerati da **49** in poi.
Esito in `docs/ESITO_FASE4_TRAFFICO.md`, con una riga `PASSO <lettera>: OK` oppure `PASSO <lettera>: FERMO - motivo` per ogni pacchetto, e una sezione
"Decisioni dell'agente". Il tuo giudizio è libero sulle scelte di realizzazione; i criteri di riuscita e le regole di pubblicazione di questo piano non si cambiano.

**Ti devi fermare e scrivere a Leo solo se:** (1) l'offerta TP non si riesce a collegare alla rete stradale per più del 25% dei passaggi (dopo averci provato in due modi);
(2) controlli di coerenza che differiscono di oltre il 5% senza spiegazione; (3) serve qualcosa vietato; (4) disco o RAM esauriti. Altrimenti vai avanti col default
ragionevole e annotalo. Non cercare di far uscire un bel risultato: se è debole, scrivilo.

## 3. Pacchetto A — Fase 3-bis: modello più realistico (script 49-50)

**Cosa non va nel modello attuale (V0), dall'esito della Fase 3:** (a) nessuna congestione: i viaggi corrono tutti sulle strade più veloci e le concentrano
(Piazza Castello→Collegno 11,7 min invece di 20-35; "Lungo Po Diaz" 85.826 veic/giorno); (b) le destinazioni sono pesate sulla popolazione, quindi il centro (uffici, negozi,
scuole) è sottostimato; (c) il traffico da fuori area entra da 206 "porte", di cui 132 strade minori: valori assurdi (fino a 250.000 veic/giorno) sui bordi.

**Pacchetto di miglioramenti V3 (fissato ora; si valuta UNA volta):**
1. **Destinazioni per attrattori.** Estremi "a casa" → popolazione (sezioni); altri estremi → pesi di attrattori coerenti con lo scopo del viaggio: lavoro → uffici/sedi/attività
   commerciali/servizi; scuola/università → scuole e università; acquisti → attività commerciali; cure → ospedali e consultori; altro → mix. Dati: catalogo comunale
   (`data/processed/catalogo`), `servizi_osm_cintura.json`, e gli zip in `data/raw` (anagrafe scuole, attività commerciali, sedi amministrative, ospedali, università). L'origine di un
   viaggio non domestico si deduce dallo scopo del viaggio precedente della stessa persona (righe consecutive di `spostamenti.csv`, `PROGR_SPOST`); se non è ricostruibile, usa la popolazione.
2. **Congestione.** Assegnazione ripetuta con tempi che dipendono dal flusso (metodo delle medie successive, funzione ritardo di tipo BPR; capacità per classe di strada e numero di corsie
   da OSM, con valori standard dove mancano; 10-20 iterazioni; ora di punta del mattino come caso principale e il giorno intero come somma delle fasce). Obbligatorio il controllo
   sul tempo di viaggio: Piazza Castello→Collegno e altri 5 percorsi noti devono avvicinarsi ai tempi di punta reali (20-35 min il primo). Secondo controllo indipendente: le **velocità** che il modello dà
   ai tratti dei sensori si confrontano con le velocità misurate dai sensori in quelle ore (`velocita_5t.json`).
3. **Porte.** Solo strade di rango ≥ 3 (almeno "primary"/statali importanti), con quote fra le porte proporzionali alla capacità e alla direzione; dove ci sono sensori 5T su quelle strade
   entro ~5 km dal bordo, usali per verificare (o orientare) le quote d'ingresso. Conta e scrivi quanti sensori esterni sono utilizzabili. Se i valori sui tratti di bordo restano assurdi (> 80.000 veic/giorno
   su strade di rango ≤ 2), marcali `affidabile: false` e non usarli nelle graduatorie.

**Come si valuta:** esattamente come in Fase 3 (stesse unità-sensore, taratura *leave-one-out*, stesse metriche con intervalli, stessa tabella di classificazione). Si eseguono V3 e,
solo come diagnostica descrittiva, fino a 3 ablazioni (V3 senza il punto 1, senza il 2, senza il 3) per dire quale miglioramento conta; **la variante finale è V3 oppure V0 e basta**,
non si sceglie fra le ablazioni.
**Regola di scelta (fissata ora):** si adotta V3 se ρ(V3) ≥ ρ(V0) e l'errore mediano di V3 non è peggiore di V0 di più di 3 punti. Altrimenti resta V0, si scrive "V3 non migliora" e si smette.
**Tempo massimo:** circa 3 ore di lavoro; l'assegnazione completa dura meno di 15 minuti anche con 20 iterazioni (V0: 44 secondi).
Se i nuovi sensori `40123~2`, `40189~2`, `13077~2` hanno già celle valide (probabilmente no prima di fine mese) aggiungili alle unità solo se non cambiano le soglie.
Output: `data/processed/traffico_c/v3/…`, `docs/RAPPORTO_TRAFFICO_C_V3.txt` con tabella V0 vs V3 vs ablazioni (n, errori, ρ, intervalli) e il tempo di viaggio dei percorsi noti.

## 4. Pacchetto B — Offerta di trasporto pubblico per strada (script 51-52) [PROGRAMMATO]

Obiettivo: per ogni tratto di rete (gli stessi 105.890 della Fase 3) e poi per ogni corridoio: quanti **passaggi di bus e tram all'ora** ci sono in un giorno feriale tipico.
- Dati: `data/raw/gtt_gtfs_20261003_224530.zip` (ha `shapes.txt`, `trips.txt` con `shape_id`, `stop_times.txt`, `calendar.txt`, `calendar_dates.txt`, `routes.txt` con `route_type`). Giorno feriale tipico:
  un mercoledì in periodo scolastico incluso nella validità del feed e senza eccezioni (per esempio 14/10/2026; controllalo in `calendar`/`calendar_dates` e scrivilo). Fai anche sabato e domenica tipici se è facile
  (il traffico resta feriale, ma l'offerta weekend serve dopo).
- Si considerano bus e tram (route_type 0 e 3, più eventuali tipi urbani); la **metropolitana** e la **ferrovia** non scorrono sulle strade: non entrano nei passaggi per strada, ma si registra un flag
  `metro_vicina` / `ferrovia_vicina` (linea o stazione entro 300 m dal corridoio) per non scambiare per "scoperta" una strada che ha la metro a fianco.
- Metodo: per ogni corsa del giorno tipico, la sua forma (`shape_id`) viene riportata sui tratti OSM (map matching: i punti della forma si agganciano ai tratti stradali vicini ≤ 20-25 m, con verso e
  continuità; i tram, che possono stare su binari non presenti nella rete auto, si agganciano alla strada più vicina). Conta le corse per tratto e per fascia: mattina 7-9, sera 17-19, giorno 6-21, e la
  frequenza media in punta (passaggi/ora). Conta anche le **linee diverse** per tratto.
- Controlli: (1) corse totali del giorno tipico uguali a quelle di `trips`+`calendar` ricalcolate in un altro modo (tolleranza 0); (2) quota di corse bus/tram la cui forma si aggancia alla rete ≥ 75% (altrimenti fermati);
  (3) tre fermate a caso ricalcolate a mano dal GTFS grezzo; (4) buon senso: Corso Francia, Corso Vittorio Emanuele II, via Nizza, Corso Giulio Cesare con tanti passaggi in punta; strade residenziali di
  periferia con zero; (5) corridoi di Torino con passaggi ma nessuna fermata nei dintorni → da guardare.
- Output: `data/processed/traffico_c/tp_tratti.csv` (o json), `data/processed/tp_corridoi.json` (per corridoio: passaggi/ora in punta mattina e sera, giorno, linee, lunghezza coperta, metro/ferrovia vicina, tag
  `[PROGRAMMATO]`) e `docs/RAPPORTO_TP_PER_STRADA.txt`.

## 5. Pacchetto C — Pubblicazione del traffico (script 53)

Dopo il pacchetto A (variante finale V0 o V3) produci `data/processed/traffico_stimato_finale_v2.json` (non sovrascrivere il file della Fase 3: tienine una copia) con, per ogni corridoio:
- `veic_giorno` (6-21, due versi), con `stimato: true` ovunque non c'è un sensore sullo stesso corridoio (dove c'è, il valore misurato ×2 se un solo verso, con `misurato: true`);
- **accuratezza dichiarata:** `fascia_50` e `fascia_90`, ricavate dagli errori *leave-one-out* della variante finale (esempio: errore mediano 32% → "nella metà dei casi lo scarto è entro ±32%"; 90° percentile → "9 volte su 10 entro ±X%").
  Le fasce si costruiscono con un'unica regola, documentata, e valgono per tutti i corridoi dove il modello è validato (cioè con flusso modello nell'intervallo dei sensori); fuori da quell'intervallo (strade con
  flusso molto basso, estrapolazione) il campo `estrapolazione: true` e la fascia si allarga a un valore dichiarato;
- **relativi:** `indice_1_5` (quintili) e `rapporto_su_mediana_torino` (flusso diviso la mediana dei corridoi dell'universo di Torino, definito sotto);
- **graduatoria:** `posizione_torino` (1 = più traffico) fra i corridoi dell'universo di Torino, e `posizione_cintura` per la prima cintura;
- `classe_esito` della Fase 3 accanto a ogni numero (C-DEBOLE o quello che risulta), `affidabile` (false per i tratti di bordo e le porte), `fiducia` (alta: sensore sullo stesso corridoio; media: modello
  nell'intervallo validato e strada di rango ≥ 3; bassa: altro).
**Universo di Torino:** corridoi con "(Torino)" nel nome, lunghezza ≥ 300 m, escluse autostrade/tangenziali/raccordi (classe a parte, perché il trasporto pubblico su gomma non le serve), strade
a flusso modello nullo e quelle con `affidabile: false`. **Prima cintura:** i comuni confinanti, stessa regola. Scrivi in rapporto quanti corridoi e quanti km ci sono nell'universo.
Le soglie "alto/medio/basso" si ricalcolano **dentro l'universo di Torino** (quartili o terzili: dichiara quali), non su tutti i 10.122 corridoi (dove "alto" partiva da soli 1.520 veic/giorno).

## 6. Pacchetto D — Incrocio traffico × trasporto pubblico (script 54)

Per ogni corridoio dell'universo di Torino (e, separatamente, della prima cintura):
- coppia (traffico, passaggi TP in punta mattina e sera);
- **definizione fissata ora:** "molto traffico" = nel quarto più alto per `veic_giorno` nell'universo; "poco TP" = nel quarto più basso per passaggi/ora in punta (compresi gli zeri) **e** senza `metro_vicina`
  o `ferrovia_vicina`. Una strada con molto traffico e poco TP è quindi nel gruppo "da guardare". Sensibilità: ripeti con terzili e con la sola punta del mattino, riportando quali corridoi restano;
- **robustezza all'incertezza del traffico:** un corridoio è `robusto` se resta "molto traffico" anche quando il suo traffico è moltiplicato per 0,65 e per 1,35 (circa la fascia al 50%);
- graduatoria per "divario" = percentile del traffico − percentile dell'offerta TP, a parità di condizioni; lista dei primi 30 con nome, quartiere, lunghezza, traffico (valore + fascia), passaggi TP/h, linee, flag;
- **raggruppamento:** corridoi consecutivi o omonimi del gruppo "da guardare" si riportano insieme in un elenco di assi (per leggibilità), senza perdere i dati per corridoio;
- tre esempi spiegati in chiaro (una strada nel gruppo, una con molto traffico ma TP buono, una con poco traffico e poco TP) per sanity check;
- controlli: la lista non deve essere dominata da strade di bordo, ponti/sottopassi corti o strade con meno di 300 m; se lo è, scrivilo e spiega come hai filtrato. Controllo di buon senso a campione:
  confronta 10 corridoi della lista con la conoscenza della città (per esempio linee note come Corso Giulio Cesare o Corso Orbassano) e annota dove la lista sembra strana.
- Output: `data/processed/risultato8_traffico_tp.json`, `docs/RAPPORTO_RISULTATO8_TRAFFICO_TP.txt`. Nessuna mappa in questa fase.
- Aggiungi in coda al rapporto i limiti da dichiarare ovunque: stime di traffico deboli (C-DEBOLE), sensori a un verso, IMQ solo residenti 11-84 anni, offerta TP da orario programmato (non tiene conto di
  ritardi, capienza, affollamento), nessuna misura dei passeggeri.

## 7. Verifica del raccoglitore corretto (Leo l'ha già avviato) — pacchetto E

Dopo l'avvio, nel log `logs\aggiorna_raccolta_5t_codici.log` Leo deve aver letto `active`, `sensori nell'ultimo istante: 112` e `codici ~2 con dati: 3/3`. Verificalo (Leo ti incollerà le ultime righe del log). Con il
prossimo fetch da leopi (lunedì 19/10) controlla nel database copiato che compaiano i tre codici `~2` e che 26/33/35-37 non cambino sui dati storici. Dopo il 24/10 verifica anche le ore locali (il 25/10 cambia l'ora).

## 8. Rilancio e consegne

- `scripts/TRAFFICO_RILANCIA_SENSORI.bat` (della Fase 3) va esteso con i nuovi script (traffico finale v2, TP, incrocio) dove dipendono dai sensori; l'offerta TP e il modello non cambiano con il fetch.
- Consegne: `docs/ESITO_FASE4_TRAFFICO.md` (esito per pacchetto, decisioni, numeri chiave, anomalie, pacchetti installati, durate, file creati/modificati, testo proposto per l'aggiornamento di `MEMORIA_PROGETTO.md`,
  che non va modificata). Verifiche indipendenti obbligatorie: totali delle corse TP (pacchetto B), fattore di taratura e 3 errori *leave-one-out* della variante finale ricalcolati con un altro metodo,
  5 corridoi seguiti dai dati grezzi al valore finale, `git status` senza file vietati toccati.

## 9. Prompt per l'agente (da incollare tutto, una volta sola)

```
Sei l'agente che esegue la Fase 3-bis e la Fase 4 del Risultato 8 (traffico veicolare) del progetto GTT di Leo, sul PC di Leo, cartella C:\projects\Progetti\GTT.

Leggi per primi: AGENTS.md, MEMORIA_PROGETTO.md, docs/PIANO_TRAFFICO_5T.md, docs/PIANO_TRAFFICO_FASE2.md, docs/PIANO_TRAFFICO_FASE3.md, docs/ESITO_FASE3_TRAFFICO.md e soprattutto
docs/PIANO_TRAFFICO_FASE4.md (il tuo piano). Controlla di essere sul ramo "prova"; se no, fermati.

Obiettivo: trovare le strade di Torino con molto traffico e poco trasporto pubblico. Esegui i pacchetti A, B, C, D, E del piano (A = modello del traffico piu' realistico V3, valutato una volta con i criteri
gia' fissati; B = offerta di bus e tram per strada dal GTFS; C = pubblicazione del traffico con numeri assoluti e fascia di errore, valori relativi e graduatoria; D = incrocio traffico x trasporto pubblico;
E = verifica del raccoglitore). Puoi fare B prima di A, ma C e D vengono dopo A e B. Hai liberta' sulle scelte di realizzazione; i criteri di riuscita, la regola di scelta fra V0 e V3 e le regole di pubblicazione non si cambiano.

Paletti: nessun commit; database e data/raw in sola lettura; non scrivere ne' riavviare nulla sul Pi; non modificare MEMORIA_PROGETTO.md, scripts/mappa_template.html, scripts/04_genera_mappa.py; copia .bak_17ott prima di
cambiare un file esistente; calcoli lunghi in un .bat a parte, ripartibili, con log; PC con 8 GB di RAM; pip --user solo per pacchetti comuni (da annotare); niente servizi esterni.

Fermati e scrivi a Leo SOLO se: meno del 75% delle corse bus/tram si aggancia alla rete stradale (dopo due tentativi diversi); un controllo di coerenza differisce di oltre il 5% e non lo sai spiegare; serve
qualcosa che il piano vieta; disco o RAM esauriti. Altrimenti vai avanti col default piu' ragionevole e annotalo. Se V3 non migliora V0 secondo la regola del piano, tieni V0, scrivilo e vai avanti: non fare altri tentativi.

Scrivi in docs/ESITO_FASE4_TRAFFICO.md una riga "PASSO <lettera>: OK" o "PASSO <lettera>: FERMO - motivo" per pacchetto, le "Decisioni dell'agente" e le verifiche indipendenti della sezione 8. Non cercare di far uscire
un bel risultato: se e' debole, scrivilo con i numeri.

Risposta finale a Leo (massimo 12 righe): variante finale (V0 o V3) con errore mediano, rho di Spearman, n e intervalli, e la classe di esito; accuratezza dichiarata dei numeri assoluti (fascia 50% e 90%); quanti corridoi e quanti km
nell'universo di Torino; quota di corse TP agganciate alla rete; i 10 assi di Torino con piu' traffico e meno TP (nome, traffico con fascia, passaggi/ora); quanti robusti; anomalie; durata; file principali creati o modificati.
```
