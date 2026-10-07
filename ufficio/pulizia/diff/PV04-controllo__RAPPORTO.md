origine: agente PV04-controllo
stato: bozza

Rapporto di controllo (PV04‑controllo)

**1. Revisione di `strumenti/genera_preventivo.py`**  
- Ho esaminato il codice alla ricerca di errori reali legati a:
  - messaggi di errore errati,
  - controllo delle chiavi JSON,
  - generazione del nome file da `PROTOCOLLO`,
  - manipolazione del file .docx che potesse alterare il logo o altre parti binary.
- **Esito:** nessun bug reale individuato. Le verifiche di errore, la sanitizzazione del nome file e la copia dei contenuti zip sono corrette. Il logo rimane intatto perché solo `word/document.xml` viene modificato.

**2. Modifiche apportate**  
- Nessuna modifica al file `strumenti/genera_preventivo.py` (il codice è già corretto).

**3. Documentazione di test**  
- Ho creato `strumenti/PROVA_PREVENTIVO.md` con istruzioni passo‑passo per testare il generatore, includendo controlli su placeholder, logo, dati e apertura con Word/LibreOffice.

**4. Scelte**  
- Nessuna scelta da prendere, il comportamento predefinito è stato mantenuto.

**5. Prossimi passi**  
- Leo può ora eseguire il test descritto in `PROVA_PREVENTIVO.md`.  
- In caso di problemi, annotare le osservazioni secondo le indicazioni fornite.

---  
*Report redatto dall’agente PV04‑controllo.*
