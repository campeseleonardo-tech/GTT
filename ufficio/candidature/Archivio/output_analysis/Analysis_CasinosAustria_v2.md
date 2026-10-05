# Analisi: Automatentechniker:in (all genders), Casinos Austria, Casino Salzburg

## Fit: medio-basso (raccomandazione: valutare, non priorità)
- Punti a favore: tecnico hands-on su banchi prova (manutenzione, messa in servizio, sicurezza, CAN, diagnosi guasti), elettricista PV/EV, eventi con ~1.000 ospiti, sede Salzburg, disponibilità immediata, tedesco C1, ruolo "Berufseinstieg".
- Ruolo lontano dal posizionamento core (Product/Project Management, ruolo strategico): è un lavoro di assistenza tecnica su slot machine con turni. Preferenze di ricerca: "physical product" sì, ma carriera/strategia no.

## Stipendio
- Offerta: da EUR 39.620 lordi/anno, full time. Richiesta abituale: EUR 50-55k (ultimo KTM ~60k). Il minimo è circa 20-28% sotto la richiesta abituale e circa 34% sotto l'ultimo stipendio. Rischio di sovraqualificazione (MSc) e di retention.

## Gap veri
- Nessuna riparazione di slot machine, Kartenmischmaschinen o apparecchi da gioco; nessuna esperienza in casinò.
- Spielerklärungen / Gästebetreuung al Floor: solo eventi (Croma) e danza, non servizio clienti in casinò.
- Netzwerke: baseline ha solo CAN, Raspberry, Arduino; nessun networking IT dichiarato, quindi non scritto.
- Turni, lavoro notturno e nel weekend: nessun impegno dichiarato, non affermato nella lettera.
- Datenanbindung / Abrechnung: analogia solo (acquisizione dati, CAN, database), non identità.

## Rischi ATS
- Keyword offerta presenti in CV solo dove supportate: Wartung, Fehlersuche, Funktionstests (come Testfälle/Versuche), Inbetriebnahme, Dokumentation, MS Office, CAN.
- Non presenti: Reparatur Spielautomaten, Netzwerke, Gästebetreuung nel senso casinò. Possibile filtro per "technische Ausbildung" (MSc Engineering lo copre, ma non è una Lehre/HTL).

## Scelte fatte
- Elettricista incluso come voce CV (offerta tecnica di installazione/messa in servizio, dominio lo richiede); non indicato come informale.
- Voce System Testing a 8 righe (centrale), Functional Development a 3, Intern 3, Event Manager con ospiti/budget.
- Lettera aperta con i 4 punti critici dell'offerta collegati a KTM; gap dichiarato in una frase; danza menzionata per il contatto con il pubblico.
- Nessun nome cliente; KTM sempre al passato; niente su orari, turni o stipendio.
- Archivio non aperto (azienda/settore non nell'indice).

## OPEN QUESTIONS
- Disponibilità a Schichtdienst con lavoro notturno e nel weekend (richiesta dall'offerta): non dichiarata, non affermata.
- Conoscenze di reti (TCP/IP, switch) oltre CAN: se esistono, aggiungere a TOOLS.
- Esperienza di assistenza clienti o servizio diretto con ospiti (es. pizzaiolo, danza) da confermare se rilevante.

## DA VERIFICARE
- "Testautomatisierung ... 50 Prozent" e "an Nachfolger übergeben" (baseline: sì, controllo cifra).
- "Wärmebildkamera betreut und gewartet" (lettera di referenza).
- Date elettricista 06/2014 - 09/2018, "Familienbetrieb" come nome azienda come in baseline.
- Tono della frase sul gap e della menzione del titolo di campione del mondo 2016.


## CONTROLLI AUTOMATICI (script)
- avviso [CV_description.txt] TOLLERATA: 91 car.: Testautomatisierung per Skript: Auswertezeit um 50 Prozent gesenkt, üb...
- avviso [CV_description.txt] VOCE_CORTA: University Collaboration - Business Development: 2 righe di descrizione (fatto mancante?)
- avviso [CV_description.txt] VOCE_CORTA: Bachelor of Science in Business & Management: 2 righe di descrizione (fatto mancante?)
Esito: OK
