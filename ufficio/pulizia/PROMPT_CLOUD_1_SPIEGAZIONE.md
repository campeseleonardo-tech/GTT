# Compito per la sessione Claude nel cloud n.1: spiegazione completa + proposta di struttura standard

Incolla nella sessione cloud: **"Leggi ufficio/pulizia/PROMPT_CLOUD_1_SPIEGAZIONE.md e fai quello che dice."**

## Chi e' Leo e come vuole le cose
- Leo non e' un programmatore: italiano semplice, frasi brevi, niente gergo (se serve un termine tecnico, spiegalo in mezza riga).
- Vuole un piano chiaro prima di costruire. In questa sessione **non si modifica nessun file esistente**: si scrivono solo due documenti nuovi.
- Sii critico: segnala doppioni, codice morto, rischi, cose fatte male. Distingui sempre "visto nel file" da "mia ipotesi".
- Risparmia: non leggere per intero file enormi se non serve (dati, log lunghi, backup vecchi `_backup_*`, `confronto_claude_*`, `pulizia/diff`). Di quelli basta sapere cosa sono.

## Cosa c'e' in questo repo
- `ufficio/` = l'"Ufficio": pannello locale (Python standard + `pannello/ufficio.html`, porta 8765) che fa lavorare agenti AI (Claude e modelli gratis) su task dei progetti. Punti chiave: `motori.py` (tutte le chiamate ai modelli), `dispatcher.py` (coda task), `generico/` (runner e task), `pannello/` (server, dati, chat), `scheda.py`, `progetti/*.json`, `logs/`.
- `progetti/<id>/` = copia dello stato attuale di ogni progetto (GTT, Langue, Preventivi, Timelive, Mercatino). Rami: `RAMI_PROGETTI.md`.
- `NON_CARICATI.md` = file esclusi.
- Il lavoro vero gira sul PC Windows di Leo: ogni task crea un ramo git nel repo del progetto e una cartella `agenti/<id>/` (RAPPORTO, DIFF...).

## Documento 1: `docs/SPIEGAZIONE_SISTEMA.md`
Una spiegazione esaustiva ma leggibile:
1. **In una pagina**: cosa fa l'Ufficio, il percorso di una task dall'idea al risultato (chi la crea, dove va in coda, chi la esegue, con quale modello, dove finisce il risultato, come la vede Leo).
2. **Mappa dei file**: per ogni file/cartella dell'Ufficio, a cosa serve, chi lo usa, se e' ancora usato. Segna: VIVO / VECCHIO (non piu' usato) / DOPPIONE (stessa cosa fatta altrove) / DUBBIO.
3. **Motori e modelli**: come si sceglie il modello, catene, ripieghi (in particolare: quando una task "gratis" finisce su Claude e consuma l'abbonamento), tempi massimi, dove si registrano consumi.
4. **Dati e stato**: tutti i file json/jsonl/csv/md che fanno da "memoria" (diario, domande, consumi, schede progetto, chat) e chi li scrive.
5. **Progetti**: per ognuno, in 5-10 righe, cosa e', com'e' organizzato, file di servizio dell'Ufficio dentro il repo (PROGETTO.md, MEMORIA_PROGETTO.md, agenti/...).
6. **Problemi trovati**, in ordine di gravita', con file e riga quando possibile.

## Documento 2: `docs/PROPOSTA_STRUTTURA_STANDARD.md`
Una proposta (da discutere con Leo, NON da applicare) per ripartire puliti:
1. **Struttura standard di un progetto** (uguale per tutti): cartelle, dove stanno i file di servizio dell'Ufficio (fuori dal repo o non tracciati, per non creare conflitti a ogni unione), scheda progetto, documenti, dati grandi.
2. **Struttura standard dell'Ufficio**: cosa tenere, accorpare (es. `ufficio_extra.py` / `ufficio_dati.py` / `pannello_server.py`), togliere.
3. **Strategia rami git**: Leo usa un ramo `prova` per progetto (main intatto); ci sono centinaia di rami task. Proponi come arrivare a una situazione pulita senza perdere lavoro (i rami sono anche nel backup .bundle).
4. **Regole per i motori** gia' decise da Leo (da rispettare nella proposta):
   - se Leo sceglie Gratis, **mai** ripiego sul suo abbonamento Claude; le alternative le sceglie lui ogni volta: Gratis / Claude API (a consumo) / credito cloud;
   - Gemini resta (ha fatturazione, il tetto lo mette Leo nella console Google);
   - Mistral da togliere (nessuna API gratis);
   - un singolo modello non deve bloccare per 10 minuti (oggi `TEMPO_TENTATIVO` = 600 s) e i modelli che falliscono sempre vanno esclusi da soli.
5. **Lista della pulizia** (sotto) ordinata in passi piccoli, ognuno provabile da solo, con cosa puo' rompersi.
6. **Domande per Leo**: solo le decisioni vere, ognuna con "cosa cambia se scegli A o B".

## Lista della pulizia gia' raccolta da Leo (05/10/2026)
- Motori: togliere Mistral; Gemini Pro non gratuiti (tenere i Flash); semplificare i motori vecchi del pannello ("Claude (Pro)", "Gratis, poi Claude", "OpenRouter, modello scelto", "Solo gratis", slot @gratisN, @forte) in poche scelte chiare; MODELLO_GRATIS "openrouter/free" e commenti vecchi; Codex CLI: collegare o togliere.
- Runner/rami: una task fallita e rifatta riusa il ramo vecchio e non riparte dal lavoro nuovo; centinaia di rami; file di servizio che creano conflitti (scheda progetto riscritta dopo ogni task, agenti/LOG.md, agenti/ULTIMO_SCRIPT.txt); stash lasciati da crea_prova.py; task vecchie in generico/failed; cartelle _backup_v0.x; campi tier/effort inutili per i gratis; una task con modifiche applicate solo in parte risulta "fatta" (PV02, TL05).
- Pannello: codice della vecchia Sala controllo (/api/salute, get_salute); variabile PER e contatore 5 ore; dati "piano"/"tappe" non piu' mostrati (/api/tappa, _piano); limite messaggi chat; Candidature: azioni automatiche dormienti; Mondo (mappa gioco) da rivedere; funzioni sovrapposte tra ufficio_extra.py / ufficio_dati.py / pannello_server.py; "modifica pannello" usa sempre Sonnet.
- Domande degli agenti poco chiare: aggiungere sempre "non so / decidi tu" e il contesto.
- Progetti: GTT mappa da snellire; Langue: obiettivo giornaliero citato ma non presente.

## Come consegnare
- Lavora su un ramo nuovo (non su `main`), scrivi solo i due documenti in `docs/`, fai commit e push di quel ramo.
- Alla fine scrivi in chat: quanti file hai letto, i 5 problemi piu' gravi in una riga ciascuno, e le domande per Leo.
