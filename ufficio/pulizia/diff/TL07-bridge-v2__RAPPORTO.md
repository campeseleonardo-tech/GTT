# Rapporto - Agente TL07-bridge-v2

**origine**: agente TL07-bridge-v2
**stato**: finale

## Cosa ho fatto
Ho studiato le proposte dei due modelli (A e B), gli appunti del progetto (TODO) e il codice effettivo di `llm_bridge.py`. Ho redatto il documento di progetto unificato in `docs/BRIDGE_V2.md`. 
Ho scomposto il lavoro in passi realizzabili, isolato le divergenze e formulato 3 domande non bloccanti per stabilire le configurazioni operative.

## Cosa ho verificato
- Ho analizzato i commenti in `llm_bridge.py` e verificato che attualmente i client cloud non applicano alcuna restrizione sui dati utente estratti da SQLite.
- Ho confermato, dalla decisione passata nel progetto, che i log delle metriche di Ollama non devono essere stampati sul terminale, ma unicamente inseriti nei dati di risultato.

## Scelte
- **Filtro in uscita vs In-Tool**: Ho scelto il filtro in uscita (suggerito da B) per l'online/offline policy, perché è più sicuro oscurare i dati nell'ultimo miglio (il client di rete) piuttosto che nel motore SQL dove potremmo sfuggire a futuri aggiornamenti.
- **L0/L1/L2 Globale**: Ho optato per una configurazione di privacy globale anziché specifica per colonna o dominio (suggerito da A). È il punto di partenza più semplice e riduce il rischio di errate configurazioni.
- **Estrazione in modulo**: Per limitare la mole di `llm_bridge.py`, ho stabilito che il nuovo componente `Router` opererà in un file separato.

## Da decidere/rivedere
Nessuna delle decisioni mancanti (scelta del motore embedding, presenza effettiva del flag sensitive, e default privacy) blocca la stesura dell'architettura; le ho raggruppate in `DOMANDE.md` con i default consigliati pronti da usare.
