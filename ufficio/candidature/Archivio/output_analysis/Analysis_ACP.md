# Analisi ACP (cliente IQS) - Test Engineer für Testautomatisierung, Salzburg

## Fit: MEDIO-BASSO
Motivo: Leonardo ha vera esperienza di automazione test e report (KTM System Testing, -50% tempo di analisi, handover ai successori) e Scrum certificato, ma su banchi prova, non su software. Mancano i requisiti espliciti: certificati Tricentis Tosca / Playwright (richiesti), esperienza professionale come software tester, Jira (solo visto). Il ruolo è software, lontano dalla preferenza "physical product". Raccomandazione (solo informativa): valutare; candidatura possibile, ma probabile scarto ATS sui certificati.

## Stipendio
Offerta: da EUR 3.377,65 lordi/mese per 30 h/settimana (in Austria di norma 14 mensilità, circa EUR 47k/anno, da confermare). Richiesta abituale: EUR 50-55k (ultimo KTM ~60k). Leggermente sotto per 30 h; il rapporto con il tempo pieno non è chiaro.

## Gap veri
- Nessun certificato Tosca/Playwright (requisito "erforderlich").
- Nessun lavoro da software tester; esperienza su hardware (analogia, non identità).
- Jira solo visto; Scrum solo come certificazione universitaria, non in un team Scrum.
- Nessun Tosca/Playwright/Selenium nei tool: non si dichiara.

## Rischi ATS
Keyword Tosca, Playwright, JIRA, Testfälle, Testautomatisierung, Scrum: presenti solo Scrum, Testautomatisierung, Jira (nur gesehen). Requisito formale (Bachelor/Master facheinschlägig + 3 anni) probabilmente soddisfatto dal MSc, ma anni "als Software-Tester" no. Accesso al mercato del lavoro austriaco: non è un problema noto, ma non dichiarato.

## Scelte fatte
- Cornice: automazione test/report + comunicazione con stakeholder; PM resta sullo sfondo (IPMA D, Scrum).
- System Testing a 4 righe (centrale), Functional Development a 3. Virtual Prototype solo come workstream di ~2 anni.
- Lettera: gap dichiarato in una frase (nessun lavoro su software, nessun certificato Tosca/Playwright), analogia hardware/software esplicita. Nessuna ora, stipendio o preavviso. Saluto "Guten Tag Torun Tek" (genere non chiaro).
- AI non menzionata (non richiesta). Elettricista, danza, E+H/ANDRITZ non usati.
- Tools: Jira "nur gesehen" indicato in modo onesto.

## OPEN QUESTIONS
1. Intende acquisire una certificazione Tosca o Playwright? Se sì, quando (si potrebbe dichiararlo)?
2. 30 h/settimana: va bene come impegno? (non scritto nella lettera)
3. Ha già usato Playwright o Tosca in progetti personali (es. Timelive)? Non in baseline, quindi omesso.
4. Anno del certificato Scrum non noto (omesso).

## DA VERIFICARE
- "-50% tempo di analisi" e "Analysezeit/Auswertungszeit" (baseline: scripted analysis cut analysis time by 50%).
- "formalisiert und übergeben (Nutzung, Pakete, Erweiterung)" e rollout con meccanici e vendite: da baseline.
- Scrum "an der Universität": baseline dice "Scrum certification during university".
- Riga MSc "Studierte Methoden" (corsi reali in baseline, usati solo indirettamente a KTM).
- Riga BSc con tesi IoT/Smart Cities: confermata 10/2026.
- Sottotitoli tradotti (Strömungsdynamik, Thermomanagement, Aerodynamik): controllo terminologico.


## CONTROLLI AUTOMATICI (script)
- avviso [CV_description.txt] VOCE_CORTA: Bachelor of Science | Wirtschaft und Management: 2 righe di descrizione (fatto mancante?)
- avviso [CoverLetter.txt] REVISIONE: IMPEGNO su ore/turni/stipendio: e' in baseline?
Esito: OK
