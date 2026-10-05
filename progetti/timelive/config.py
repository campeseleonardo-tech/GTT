# config.py
# -----------------------------------------------------------------------------
# Scopo del file
# -----------------------------------------------------------------------------
# Questa versione di config.py funge da singola fonte di configurazione per
# MVP "Personal Data Vault & AI Assistant".
# Contiene:
# - percorsi di base e input/output
# - nomi file di output
# - documentazione Spotify Schema (in forma Python)
# - linee guida di utilizzo da AI
# - supporto opzionale per leggere una patch JSON di configurazione (config.json)
#
# Collegamento agli altri file
# - spotify_ingest.py importa costanti/parametri da qui
# - main.py usa config.py indirettamente tramite spotify_ingest.py
#
# Cosa può essere modificato
# - percorsi, nomi file, e la sezione pruning (enabled/keep_fields)
# - la documentazione dello schema Spotify
#
# Cosa deve rimanere stabile
# - importabilità come modulo Python
# - struttura chiara e semplice
#
# Semplificazioni adottate
# - nessuna dipendenza esterna
# - niente configurazioni multiple: una sola fonte di verità
#
# Possibili estensioni future
# - supporto più provider (input/output separati)
# - versione hardware-specific (es. Raspberry Pi) anteposta
# -----------------------------------------------------------------------------

import json
from pathlib import Path

# -----------------------------------------------------------------------------
# Directory di progetto
# -----------------------------------------------------------------------------
# Il progetto vive logicamente in:
# C:\\Users\\campe\\Desktop\\Timelive
# I file Python stanno dentro "code/", ma l'input e l'output sono directory
# sorelle rispetto a "code/".
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = BASE_DIR / "code"
INPUT_DIR = BASE_DIR / "Input"
SPOTIFY_INPUT_DIR = INPUT_DIR / "Spotify"
OUTPUT_DIR = BASE_DIR / "Output"

# -----------------------------------------------------------------------------
# Nomi file di output
# -----------------------------------------------------------------------------

SPOTIFY_DATASET_FILENAME = "spotify_history_dataset.json"
SPOTIFY_SUMMARY_FILENAME = "spotify_history_summary.json"

SPOTIFY_DATASET_PATH = OUTPUT_DIR / SPOTIFY_DATASET_FILENAME
SPOTIFY_SUMMARY_PATH = OUTPUT_DIR / SPOTIFY_SUMMARY_FILENAME

# -----------------------------------------------------------------------------
# Metadati di progetto
# -----------------------------------------------------------------------------

PROJECT_NAME = "Personal Data Vault & AI Assistant"
PROJECT_MVP_NAME = "Spotify Ingestion MVP"
SCRIPT_FRIENDLY_NAME = "spotify_ingest.py"

# -----------------------------------------------------------------------------
# Spotify Schema Documentation (Python dict)
# -----------------------------------------------------------------------------
SPOTIFY_SCHEMA_DOCUMENTATION = {
    "common_fields": {
        "endTime": {
            "meaning": "Timestamp storico usato nei vecchi export Spotify. Indica il momento di fine riproduzione, spesso senza timezone esplicita.",
            "logical_type": "string datetime",
            "interpretation_notes": [
                "Presente soprattutto nei file storici più vecchi.",
                "Può avere formati diversi a seconda dell'export.",
                "Quando possibile viene convertito in timestamp ISO leggibile.",
            ],
        },
        "ts": {
            "meaning": "Timestamp della riproduzione nei formati export più recenti. È spesso il campo temporale più affidabile.",
            "logical_type": "string datetime",
            "interpretation_notes": [
                "Può comparire al posto di endTime.",
                "Spesso è in formato ISO 8601 con informazione di timezone.",
                "Il parser prova prima ts e poi endTime per costruire il tempo normalizzato.",
            ],
        },
        "artistName": {
            "meaning": "Nome artista nei file legacy.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può essere vuoto o mancante per alcuni contenuti particolari.",
                "Nei file più recenti può essere sostituito da master_metadata_album_artist_name.",
            ],
        },
        "trackName": {
            "meaning": "Titolo del brano nei file legacy.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può essere vuoto per alcuni stream tecnici o record incompleti.",
                "Nei file più recenti può essere sostituito da master_metadata_track_name.",
            ],
        },
        "msPlayed": {
            "meaning": "Millisecondi riprodotti nei file legacy.",
            "logical_type": "integer",
            "interpretation_notes": [
                "È la base per calcolare minuti ascoltati e skip-like behavior.",
                "Se manca, il parser prova campi equivalenti più recenti come ms_played.",
            ],
        },
        "ms_played": {
            "meaning": "Millisecondi riprodotti nei file recenti.",
            "logical_type": "integer",
            "interpretation_notes": [
                "È spesso il campo canonico dei nuovi export.",
                "Viene normalizzato nel campo derivato played_minutes.",
            ],
        },
        "master_metadata_track_name": {
            "meaning": "Titolo del brano nei file più recenti.",
            "logical_type": "string",
            "interpretation_notes": [
                "È spesso più affidabile di trackName nei nuovi export.",
                "Usato per derivare track_name normalizzato e track_identity.",
            ],
        },
        "master_metadata_album_artist_name": {
            "meaning": "Nome artista album nei file più recenti.",
            "logical_type": "string",
            "interpretation_notes": [
                "È il sostituto frequente di artistName nei file recenti.",
                "Usato per derivare artist_name normalizzato e track_identity.",
            ],
        },
        "master_metadata_album_album_name": {
            "meaning": "Nome album nei file più recenti.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può essere assente per podcast o contenuti non musicali.",
                "Viene preservato per interrogazioni future.",
            ],
        },
        "spotify_track_uri": {
            "meaning": "URI Spotify del brano quando disponibile.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può aiutare a identificare in modo più stabile una traccia.",
                "Non sempre è presente.",
            ],
        },
        "episode_name": {
            "meaning": "Nome episodio podcast o contenuto non musicale.",
            "logical_type": "string",
            "interpretation_notes": [
                "Importante per distinguere musica da podcast o contenuti affini.",
                "Viene preservato anche se il focus dell'MVP è la cronologia Spotify generale.",
            ],
        },
        "episode_show_name": {
            "meaning": "Nome del podcast o show associato all'episodio.",
            "logical_type": "string",
            "interpretation_notes": [
                "Utile per future analisi sui podcast.",
                "Non sempre presente.",
            ],
        },
        "reason_start": {
            "meaning": "Motivo di avvio della riproduzione secondo Spotify.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può indicare avvio manuale, autoplay o altri trigger interni.",
                "Campo utile per future analisi comportamentali.",
            ],
        },
        "reason_end": {
            "meaning": "Motivo di fine della riproduzione secondo Spotify.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può aiutare a interpretare skip, fine naturale o cambio traccia.",
                "Viene preservato senza inferenze forti.",
            ],
        },
        "shuffle": {
            "meaning": "Indica se la riproduzione era in modalità shuffle.",
            "logical_type": "boolean",
            "interpretation_notes": [
                "Non sempre disponibile nei file storici.",
                "Utile per analisi future sulle abitudini di ascolto.",
            ],
        },
        "skipped": {
            "meaning": "Indicatore esplicito di skip nei file che lo includono.",
            "logical_type": "boolean",
            "interpretation_notes": [
                "Se manca, il parser calcola anche un indicatore semplice chiamato is_skipped_like.",
                "Il valore esplicito Spotify viene preservato.",
            ],
        },
        "platform": {
            "meaning": "Piattaforma o client usato per lo stream.",
            "logical_type": "string",
            "interpretation_notes": [
                "Può distinguere mobile, desktop, web player o altri ambienti.",
                "Campo utile per future analisi di contesto.",
            ],
        },
        "conn_country": {
            "meaning": "Paese di connessione osservato da Spotify.",
            "logical_type": "string",
            "interpretation_notes": [
                "Non va interpretato automaticamente come posizione fisica certa.",
                "Può riflettere VPN, roaming o geolocalizzazione di rete.",
            ],
        },
        "ip_addr_decrypted": {
            "meaning": "IP o informazione di rete presente in alcuni export.",
            "logical_type": "string",
            "interpretation_notes": [
                "Dato sensibile: viene preservato ma non reinterpretato.",
                "Può essere utile per future funzioni di audit o arricchimento locale.",
            ],
        },
        "offline": {
            "meaning": "Indica se la riproduzione è avvenuta offline.",
            "logical_type": "boolean",
            "interpretation_notes": [
                "Utile per interpretare possibili ritardi temporali nella sincronizzazione.",
            ],
        },
        "incognito_mode": {
            "meaning": "Indica se la sessione era in una modalità privata/incognito supportata.",
            "logical_type": "boolean",
            "interpretation_notes": [
                "Campo raro ma utile da preservare.",
            ],
        },
    },
    "derived_fields": {
        "source_file": {
            "meaning": "Nome del file sorgente da cui arriva il record.",
            "logical_type": "string",
            "interpretation_notes": [
                "Serve per tracciabilità e debug.",
            ],
        },
        "source_year": {
            "meaning": "Anno estratto dal nome file quando presente.",
            "logical_type": "integer",
            "interpretation_notes": [
                "Derivato dal filename, non dal timestamp del record.",
                "Può essere 0 se l'anno non è rilevabile.",
            ],
        },
        "media_type": {
            "meaning": "Tipo media rilevato dal nome file: audio o video.",
            "logical_type": "string",
            "interpretation_notes": [
                "Derivato dal filename, non dal contenuto del singolo record.",
            ],
        },
        "record_index_in_source": {
            "meaning": "Indice sequenziale del record dentro il file sorgente.",
            "logical_type": "integer",
            "interpretation_notes": [
                "Parte da 0.",
                "Utile per audit e ricostruzione errori.",
            ],
        },
        "played_minutes": {
            "meaning": "Durata riprodotta convertita in minuti decimali.",
            "logical_type": "float",
            "interpretation_notes": [
                "Calcolato da msPlayed o ms_played.",
                "Arrotondato per leggibilità, non per precisione scientifica.",
            ],
        },
        "is_skipped_like": {
            "meaning": "Euristica semplice che marca riproduzioni molto brevi come simili a skip.",
            "logical_type": "boolean",
            "interpretation_notes": [
                "Non è una verità assoluta.",
                "Serve come segnale pratico per analisi semplici.",
                "L'MVP usa una soglia corta e leggibile, non un modello avanzato.",
            ],
        },
        "track_identity": {
            "meaning": "Identificatore leggibile costruito da artista e titolo, o da metadati equivalenti.",
            "logical_type": "string",
            "interpretation_notes": [
                "Serve per aggregazioni semplici e ispezione umana.",
                "Non garantisce unicità assoluta.",
            ],
        },
        "end_time_parsed": {
            "meaning": "Timestamp normalizzato in formato ISO quando la conversione riesce.",
            "logical_type": "string",
            "interpretation_notes": [
                "È il campo temporale consigliato per interrogazioni future.",
            ],
        },
        "artist_name": {
            "meaning": "Nome artista normalizzato prendendo il miglior campo disponibile.",
            "logical_type": "string",
            "interpretation_notes": [
                "Deriva da artistName o master_metadata_album_artist_name.",
            ],
        },
        "track_name": {
            "meaning": "Titolo brano normalizzato prendendo il miglior campo disponibile.",
            "logical_type": "string",
            "interpretation_notes": [
                "Deriva da trackName o master_metadata_track_name.",
            ],
        },
    },
    "neutral_value_policy": {
        "strings": "Quando un testo manca, si usa stringa vuota o valore leggibile neutro come 'Unknown Artist' solo per campi derivati orientati alla leggibilità.",
        "integers": "Quando un intero manca o non è valido, si usa 0.",
        "floats": "Quando non calcolabile, si usa 0.0.",
        "booleans": "Quando assente, si usa False solo per i campi derivati. I campi originali Spotify vengono preservati come sono.",
        "dates": "Quando non interpretabili, il valore normalizzato resta stringa vuota.",
    },
    "limitations": [
        "Il parser non usa Spotify API e non arricchisce dati esternamente.",
        "Il tipo media è dedotto dal nome file.",
        "I timestamp possono avere formati diversi a seconda della versione export.",
        "Le euristiche di skip sono volutamente semplici.",
        "Il dataset privilegia leggibilità e robustezza rispetto a una normalizzazione rigida.",
    ],
}

# -----------------------------------------------------------------------------
# How an AI should use these outputs
# -----------------------------------------------------------------------------
# Queste linee guida sono destinate all'integrazione nei metadati generati
AI_USAGE_GUIDELINES = [
    "Usa _metadata per capire origine, limiti e percorso del dataset.",
    "Usa _schema prima di interpretare i record: i campi derivati sono i più stabili per query semplici.",
    "Per domande temporali preferisci end_time_parsed, poi ts, poi endTime.",
    "Per aggregazioni su artisti usa artist_name.",
    "Per aggregazioni su tracce usa track_identity o track_name a seconda del livello di dettaglio richiesto.",
    "Per durata ascoltata usa played_minutes, non msPlayed grezzo, salvo necessità di precisione originale.",
    "Non assumere che tutti i record rappresentino musica: alcuni possono essere video, podcast o contenuti incompleti.",
    "Se un campo originale Spotify manca, controlla se esiste un campo derivato equivalente.",
    "Usa source_file e record_index_in_source per audit e tracciabilità.",
    "Tratta is_skipped_like come euristica e non come prova definitiva di skip."
]

# -----------------------------------------------------------------------------
# Pruning Config Patch - JSON driven (opzionale)
# -----------------------------------------------------------------------------
# Se si desidera utilizzare una patch esterna config.json per pruning, puoi
# leggere le impostazioni qui e sovrascrivere i default. Il codice di ingestione
# può usare PRUNE_ENABLED e PRUNE_KEEP_FIELDS come flag universale.
PRUNE_ENABLED = True
PRUNE_KEEP_FIELDS = [
    "source_file",
    "source_year",
    "media_type",
    "record_index_in_source",
    "artist_name",
    "track_name",
    "end_time_parsed",
    "played_minutes",
    "track_identity",
    "is_skipped_like",
]

# Patch opzionale da config.json (scelta operativa: puoi decommentare se usi JSON)
# Esempio di ripresa:
# {
#   "pruning": {
#     "enabled": true,
#     "keep_fields": [
#       "source_file","source_year","media_type","record_index_in_source",
#       "artist_name","track_name","end_time_parsed","played_minutes","track_identity","is_skipped_like"
#     ]
#   }
# }
#
# Se vuoi attivare questa lettura JSON, decommenta il blocco sotto:
# try:
#     _cfg_path = Path(__file__).with_name("config.json")
#     if _cfg_path.exists():
#         with _cfg_path.open("r", encoding="utf-8") as _f:
#             _cfg = json.load(_f)
#             _prune = _cfg.get("pruning", {})
#             PRUNE_ENABLED = bool(_prune.get("enabled", PRUNE_ENABLED))
#             _keep = _prune.get("keep_fields", None)
#             if isinstance(_keep, list) and _keep:
#                 PRUNE_KEEP_FIELDS = [str(x) for x in _keep]
# except Exception:
#     pass  # fall back to defaults

# -----------------------------------------------------------------------------
# End of config.py
# -----------------------------------------------------------------------------
