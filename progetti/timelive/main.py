# main.py
# -----------------------------------------------------------------------------
# Scopo del file
# -----------------------------------------------------------------------------
# Questo file è l'orchestratore minimale del MVP.
# Richiama le pipeline Spotify e, se presente, anche la pipeline bancaria.
# Mostra un riepilogo chiaro a terminale per entrambe le fonti di dati.

# Collegamento agli altri file
# - importa ingest_spotify_history() da spotify_ingest.py
# - importa ingest_bank_history() da bank_ingest.py (se presente)
# - usa indirettamente config.py attraverso spotify_ingest.py e bank_ingest.py

# Cosa può essere modificato
# - il formato di stampa del riepilogo
# - l'ordine delle informazioni mostrate
# - l'aggiunta futura di altre pipeline oltre Spotify/Bancarie

# Cosa deve rimanere stabile
# - semplicità estrema
# - nessuna CLI complessa
# - esecuzione pulita anche in caso di errori o assenza file

# Semplificazioni adottate
# - nessun argparse
# - nessuna configurazione runtime
# - un solo flusso principale esplicito

# Possibili estensioni future
# - aggiungere altre sorgenti dati locali
# - orchestrare pipeline multiple
# - stampare un report finale aggregato del vault
# -----------------------------------------------------------------------------

from spotify_ingest import ingest_spotify_history
# Import bank ingestion se disponibile
try:
    from bank_ingest import ingest_bank_history  # type: ignore
    BANK_INGEST_AVAILABLE = True
except Exception:
    BANK_INGEST_AVAILABLE = False

def run_spotify_pipeline():
    """
    Esegue la pipeline Spotify e restituisce il risultato strutturato.
    """
    return ingest_spotify_history()

def run_bank_pipeline():
    """
    Esegue la pipeline bancaria se disponibile e input presenti.
    Restituisce dict di stato o None se non disponibile.
    """
    if not BANK_INGEST_AVAILABLE:
        return {"status": "skipped", "reason": "bank_ingest.py non disponibile nel momento."}
    try:
        return ingest_bank_history()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def print_run_summary(result, title="Spotify Pipeline Summary"):
    """
    Stampa un riepilogo semplice e leggibile dell'esecuzione.
    """
    files_found = result.get("files_found", 0)
    files_processed = result.get("files_processed", 0)
    records_processed = result.get("records_processed", 0)
    outputs = result.get("outputs", {})
    errors = result.get("errors", [])
    warnings = result.get("warnings", [])
    ignored_files = result.get("ignored_files", [])
    print(f"=== {title} ===")
    print(f"File trovati: {files_found}")
    print(f"File processati: {files_processed}")
    print(f"Record processati: {records_processed}")
    if outputs:
        print("Output generati:")
        if outputs.get("dataset"):
            print(f"- Dataset: {outputs['dataset']}")
        if outputs.get("summary"):
            print(f"- Summary: {outputs['summary']}")
    if ignored_files:
        print("File ignorati:")
        for name in ignored_files:
            print(f"- {name}")
    if warnings:
        print("Warning:")
        for warning in warnings:
            file_name = warning.get("file", "")
            warning_type = warning.get("warning_type", "warning")
            message = warning.get("message", "")
            print(f"- [{warning_type}] {file_name}: {message}")
    if errors:
        print("Errori:")
        for error in errors:
            file_name = error.get("file", "")
            error_type = error.get("error_type", "error")
            message = error.get("message", "")
            print(f"- [{error_type}] {file_name}: {message}")
    else:
        print("Nessun errore bloccante.")

if __name__ == "__main__":
    result_spotify = run_spotify_pipeline()
    if result_spotify.get("files_found", 0) == 0:
        print("Nessun file Spotify valido trovato in Input/Spotify.")
        print("Copia i file Extended Streaming History nella cartella e riesegui.")
    else:
        print_run_summary(result_spotify, title="Spotify Pipeline Summary")

    # Esegui la pipeline bancaria se disponibile e input presenti
    if BANK_INGEST_AVAILABLE:
        result_bank = run_bank_pipeline()
        if result_bank and isinstance(result_bank, dict):
            if result_bank.get("status") == "ok" or result_bank.get("records") or result_bank.get("records_count"):
                print_run_summary(result_bank, title="Bank History Pipeline Summary")
            elif result_bank.get("status") == "skipped":
                print("Bank ingested non attiva: ", result_bank.get("reason", " non disponibile in questa sessione."))
            elif result_bank.get("status") == "error":
                print("Errore durante bank_ingest.py: ", result_bank.get("message", "Errore non specificato"))
        else:
            print("Bank ingestion ha restituito un risultato non previsto.")
    else:
        print("Bank ingestion non disponibile in questa configurazione (bank_ingest.py non importabile).")
