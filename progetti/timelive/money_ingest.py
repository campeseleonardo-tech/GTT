"""
MONEY INGEST — Personal Data Vault (Banking + Investment domain)
==================================================================

NOTA SUL NOME FILE
-------------------
Questo file si chiama `money_ingest.py` (nome esplicitamente richiesto),
ma segue esattamente lo standard architetturale "bank_ingest" descritto
nella spec di progetto e già usato da applehealth_ingest.py e
spotify_ingest.py. I DUE file di output prodotti restano quindi:

    bank_dataset.json        -> PRIMARY (LLM-oriented, budget-aware)
    bank_dataset_full.json   -> FULL    (analytical, normalizzato)

Nessun terzo file (nessun summary separato) viene prodotto, anche se
applehealth_ingest.py di fatto ne produce uno: qui si segue la regola
esplicita concordata per questo ingest ("sempre solo due file").


OBIETTIVO
---------
Trasformare CSV bancari/finanziari eterogenei (conto corrente, carta,
broker) in:

    RAW CSV (una o più fonti, mescolate nella stessa cartella)
        |
        v
    RICONOSCIMENTO SORGENTE (euristico, su header/contenuto)
        |
        v
    NORMALIZZAZIONE (schema comune a tutte le fonti)
        |
        v
    DEDUPLICAZIONE
        |
        v
    CLASSIFICAZIONE SEMANTICA (transaction_type, category)
        |
        v
    AGGREGAZIONI TEMPORALI/FINANZIARIE + RECURRING DETECTION + GROUPING
        |
        v
    FULL  (tutto il normalizzato + aggregazioni + pattern)
        |
        v
    PRIMARY (vista compatta, budget-aware, LLM-first)


DOMINI SUPPORTATI ORA (risposta esplicita: "entrambi, in maniera ben
distinguibile")
----------------------------------------------------------------------
- domain = "bank"       -> conti correnti / carte (es. meinElba, Sella)
- domain = "investment" -> broker (es. Trade Republic)

La distinzione è portata da un campo esplicito `domain` su ogni
transazione (vedi sezione NORMALIZATION SCHEMA), NON dal campo
`source`, che invece identifica l'esportatore/file di provenienza
(vedi SEZIONE 8 della spec: source/device devono restare valori
singoli e non essere confusi tra loro).


FONTI RICONOSCIUTE ORA
-----------------------
1. meinElba / Raiffeisen (conto corrente austriaco)
   - CSV senza header, delimitatore ';', 6 colonne posizionali
   - Esempio reale fornito dall'utente (vedi RIC. SORGENTE più sotto)

2. Trade Republic (broker)
   - CSV con header a virgola, quotato, con colonne note:
     account_type, category, type, asset_class, name, symbol, shares,
     price, amount, fee, tax, currency, original_amount,
     original_currency, fx_rate, description, transaction_id,
     counterparty_name, counterparty_iban, payment_reference, mcc_code
   - NOTA: l'utente ha confermato che l'header reale potrebbe contenere
     colonne aggiuntive (es. timestamp) non presenti nella lista sopra.
     Per questo il timestamp NON viene letto per posizione fissa, ma
     cercato per NOME tra alias comuni (vedi TIMESTAMP_ALIAS_KEYS), in
     modo da restare corretto anche se l'header reale differisce
     leggermente da quello fornito come esempio.

3. Banca Sella (conto corrente italiano)
   - CSV con header a virgola, quotato, in italiano, con colonne note:
     Codice identificativo, Data operazione, Data valuta, Descrizione,
     Divisa, Importo, Categoria, Sottocategoria, Etichette, Note
   - Ha già categorie native (Categoria/Sottocategoria): vengono usate
     direttamente (mappate nella nostra tassonomia) invece di essere
     indovinate.

4. Fonte sconosciuta (generic_bank_csv_export)
   - Qualsiasi altro CSV bancario non riconosciuto viene comunque
     processato con un parser euristico generico ad alias di colonna
     (ripreso e adattato da money_ingest_Primordial_version.py), così
     che il sistema resti estendibile a nuovi formati (spec punto 24)
     senza dover modificare il codice ogni volta.


PRINCIPIO SULLE CATEGORIE (risposta esplicita dell'utente: "non fare
assunzioni, se non si sa la categoria distintamente")
----------------------------------------------------------------------
Le categorie semantiche vengono assegnate SOLO quando:
  a) la fonte fornisce una categoria nativa esplicita (Sella), oppure
  b) il tipo di operazione è esplicito e inequivocabile (es. Trade
     Republic "DIVIDEND", "INTEREST_PAYMENT"), oppure
  c) il merchant è stato normalizzato con alta confidenza (es. "Amazon")
     ma questo NON implica automaticamente una categoria di spesa.

In tutti gli altri casi (es. meinElba, che non ha alcuna colonna di
categoria) la categoria resta "unknown" piuttosto che essere inventata
da keyword generiche. Il campo `category_raw` conserva sempre il dato
nativo originale quando esiste, così nessuna informazione viene persa
(spec punto 24) e la mappatura è estendibile in futuro.


COME MODIFICARE OGNI SOGLIA/REGOLA
-----------------------------------
Tutti i parametri sono raccolti nella sezione CONFIGURATION qui sotto.
Non sono sparsi nel corpo delle funzioni. In futuro potranno essere
spostati in un config.py centrale (per ora restano qui, come richiesto).
"""

from __future__ import annotations

import csv
import io
import json
import re
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================
#
# Questa sezione raccoglie OGNI soglia/parametro modificabile dello script.
# Nessuna soglia è nascosta dentro le funzioni: se in futuro serve cambiare
# un comportamento, si parte sempre da qui.
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Percorsi (con fallback se un config.py centrale non è disponibile)
# ----------------------------------------------------------------------------
# Convenzione scelta: come health/spotify, path RELATIVI basati sulla
# posizione dello script, non path assoluti Windows hardcoded (deciso in
# risposta alla domanda su come gestire i percorsi: "come pensi sia meglio").
try:
    from config import (
        BANK_INPUT_DIR,
        BANK_OUTPUT_DATASET_PATH,
        BANK_OUTPUT_FULL_DATASET_PATH,
    )
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    BANK_INPUT_DIR = BASE_DIR / "Input" / "Bank"
    OUTPUT_DIR = BASE_DIR / "Output"
    BANK_OUTPUT_DATASET_PATH = OUTPUT_DIR / "bank_dataset.json"
    BANK_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / "bank_dataset_full.json"

BANK_INPUT_DIR = Path(BANK_INPUT_DIR)
BANK_OUTPUT_DATASET_PATH = Path(BANK_OUTPUT_DATASET_PATH)
BANK_OUTPUT_FULL_DATASET_PATH = Path(BANK_OUTPUT_FULL_DATASET_PATH)


# ----------------------------------------------------------------------------
# CONFIG — Identità dataset
# ----------------------------------------------------------------------------
SOURCE_PREFIX = "bank"
DATASET_VERSION = "1.0"


# ----------------------------------------------------------------------------
# CONFIG — PRUNING (stessa filosofia di health/spotify, adattata al dominio
# finanziario)
# ----------------------------------------------------------------------------
# Il PRUNE_LEVEL controlla quanto dettaglio per-transazione resta in FULL
# (non in PRIMARY, che è governato separatamente da PRIMARY_MAX_SIZE_MB).
#
# light:
#   - ogni transazione mantiene la descrizione completa originale
#   - eventuali campi non riconosciuti del CSV vengono preservati
#     integralmente sotto "extra_fields"
#
# medium (default):
#   - descrizione ripulita e troncata a DESCRIPTION_MAX_LENGTH_MEDIUM
#   - "extra_fields" preservati solo se non vuoti
#
# aggressive:
#   - per le transazioni "ordinarie" (non ricorrenti, non anomale, non di
#     importo rilevante) la descrizione viene ridotta al minimo indispensabile
#     (merchant/categoria), privilegiando aggregazioni e pattern
#   - le transazioni "notevoli" (anomale, importi grandi, operazioni di
#     investimento) mantengono comunque il dettaglio, perché rimuoverle
#     violerebbe la regola "non eliminare informazione importante solo per
#     ridurre la dimensione" (spec punto 5/16)
# ----------------------------------------------------------------------------
PRUNE_LEVEL = "light"

VALID_PRUNE_LEVELS = {"light", "medium", "aggressive"}

DESCRIPTION_MAX_LENGTH_LIGHT = 600
DESCRIPTION_MAX_LENGTH_MEDIUM = 220
DESCRIPTION_MAX_LENGTH_AGGRESSIVE_ORDINARY = 60  # per transazioni non notevoli


# ----------------------------------------------------------------------------
# CONFIG — PRIMARY budget (target, non hard limit)
# ----------------------------------------------------------------------------
# PRIMARY_MAX_SIZE_MB è un obiettivo di dimensione per bank_dataset.json.
#
# Come funziona la selezione (vedi build_primary_dataset per il dettaglio):
#   1. Le sezioni sempre incluse (metadata/schema/logic/aggregazioni/
#      recurring) vengono calcolate per prime: sono generalmente piccole e
#      ad altissimo valore informativo, quindi non sono soggette a budget.
#   2. Le transazioni individuali vengono ordinate per "notability score"
#      (vedi compute_notability_score) e aggiunte finché la dimensione
#      cumulata resta sotto il target.
#   3. Se la transazione successiva sfora il target ma resta entro
#      target * PRIMARY_SOFT_OVERFLOW_RATIO, viene comunque inclusa (soft
#      overflow) e poi la selezione si ferma. Questo evita di tagliare a
#      metà un elemento importante solo perché arrivato per ultimo.
#
# Aumentare PRIMARY_MAX_SIZE_MB => più transazioni individuali in PRIMARY.
# Diminuirlo => PRIMARY diventa quasi solo aggregazioni + recurring.
# ----------------------------------------------------------------------------
PRIMARY_MAX_SIZE_MB = 20
PRIMARY_SOFT_OVERFLOW_RATIO = 1.20  # tolleranza del 20% oltre il target

# Numero massimo di transazioni "notevoli" che PRIMARY prova comunque a
# includere per intero prima di applicare il criterio di budget (utile per
# garantire che gli ultimi N giorni siano sempre ben rappresentati anche
# se il budget è già saturo di aggregazioni).
PRIMARY_MIN_RECENT_DAYS_GUARANTEED = 14

# Pesi usati per calcolare il "notability score" di ogni transazione
# (usato sia per l'ordine di inclusione in PRIMARY, sia per decidere quali
# transazioni restano "ricche" di dettaglio anche a PRUNE_LEVEL aggressive).
NOTABILITY_WEIGHT_AMOUNT = 0.7
NOTABILITY_WEIGHT_RECENCY = 0.3
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60  # oltre questa età, il bonus recency dimezza


# ----------------------------------------------------------------------------
# CONFIG — Classificazione finanziaria (stessa filosofia di
# ACTIVITY_INFERENCE_LEVEL usata negli altri ingest, applicata al dominio
# bancario invece che a quello motorio/attività)
# ----------------------------------------------------------------------------
# conservative:
#   - usa SOLO segnali espliciti nativi (categoria nativa, tipo nativo,
#     segno dell'importo). Nessuna inferenza da keyword.
#
# balanced (default):
#   - come conservative, più un piccolo set di keyword ad altissima
#     confidenza SOLO per raffinare transaction_type (es. "stipendio" /
#     "salary" -> income, "bancomat"/"atm" -> cash_withdrawal). NON usa
#     keyword per inventare una category di spesa quando non c'è una
#     categoria nativa: la category resta "unknown" in quel caso.
#
# aggressive:
#   - come balanced, con un set di keyword più ampio per transaction_type
#     (ma MAI per category, che resta legata solo a dati nativi/merchant
#     esplicitamente mappato — vedi principio sulle categorie in testa
#     al file).
# ----------------------------------------------------------------------------
ACTIVITY_INFERENCE_LEVEL = "balanced"

VALID_ACTIVITY_INFERENCE_LEVELS = {"conservative", "balanced", "aggressive"}


# ----------------------------------------------------------------------------
# CONFIG — Aggregazioni temporali
# ----------------------------------------------------------------------------
# Granularità supportate. Il timestamp usato è sempre `timestamp_begin`
# (vedi sezione TIMESTAMP STANDARD nella spec). Non si applica alcuna
# conversione di timezone: le date sono trattate come "naive" così come
# fornite dagli export bancari (assunzione esplicita, documentata qui
# perché nessuna delle fonti attuali fornisce un fuso orario esplicito
# per le date di operazione).
AGGREGATION_GRANULARITIES = ("daily", "weekly", "monthly")


# ----------------------------------------------------------------------------
# CONFIG — Deduplicazione
# ----------------------------------------------------------------------------
# Se la fonte fornisce un ID nativo stabile (transaction_id di Trade
# Republic, "Codice identificativo" di Sella), viene usato quello come
# chiave primaria di dedup: è affidabile e non genera falsi positivi.
#
# Se non esiste un ID nativo (meinElba, fonti generiche), la chiave è
# composta da campi semanticamente significativi. Il rischio di falsi
# duplicati (es. due caffè identici lo stesso giorno) è stato segnalato
# esplicitamente e l'utente ha indicato che non è prioritario ora: la
# chiave composita include quindi anche il timestamp completo
# (data+ora, non solo la data) quando disponibile, per ridurre — ma non
# eliminare del tutto — questo rischio.
DEDUP_USE_NATIVE_ID_WHEN_AVAILABLE = True
DEDUP_DESCRIPTION_PREFIX_LEN = 80  # quanta descrizione entra nella chiave


# ----------------------------------------------------------------------------
# CONFIG — Recurring detection
# ----------------------------------------------------------------------------
# Una transazione ricorrente (subscription / regular_bill / recurring
# income) viene riconosciuta SOLO se sono soddisfatti insieme:
#   - almeno RECURRING_MIN_OCCURRENCES occorrenze con lo stesso merchant
#     normalizzato (o stessa firma di descrizione, se il merchant non è
#     disponibile) e stessa valuta
#   - importi simili tra loro entro RECURRING_AMOUNT_TOLERANCE_PCT
#   - intervallo tra occorrenze consecutive coerente entro
#     RECURRING_INTERVAL_TOLERANCE_DAYS rispetto alla mediana degli
#     intervalli osservati
#
# Questo evita di classificare come subscription una transazione solo
# perché compare due volte (spec punto 14).
RECURRING_MIN_OCCURRENCES = 3
RECURRING_AMOUNT_TOLERANCE_PCT = 0.15
RECURRING_INTERVAL_TOLERANCE_DAYS = 5


# ----------------------------------------------------------------------------
# CONFIG — Grouping (spec punto 15: non forzare "sessioni" artificiali)
# ----------------------------------------------------------------------------
# Unico grouping implementato ora: pairing acquisto+rimborso, quando due
# transazioni sullo stesso account hanno importo uguale e opposto (entro
# GROUPING_AMOUNT_TOLERANCE) ed entrambe nella stessa valuta, entro
# GROUPING_REFUND_WINDOW_DAYS giorni l'una dall'altra.
GROUPING_REFUND_WINDOW_DAYS = 0
GROUPING_AMOUNT_TOLERANCE = 0.01


# ----------------------------------------------------------------------------
# CONFIG — Anomaly detection (leggera, opzionale per costruzione)
# ----------------------------------------------------------------------------
# Una transazione è marcata come "is_unusual" se il suo importo assoluto si
# discosta di più di ANOMALY_ZSCORE_THRESHOLD deviazioni standard dalla
# media delle transazioni con stessa category+currency+domain. Richiede
# almeno ANOMALY_MIN_SAMPLES osservazioni comparabili, altrimenti non viene
# calcolato (per non produrre falsi positivi su categorie con pochi dati).
ANOMALY_ZSCORE_THRESHOLD = 2.5
ANOMALY_MIN_SAMPLES = 5


# ----------------------------------------------------------------------------
# CONFIG — Tassonomia delle categorie semantiche
# ----------------------------------------------------------------------------
# Lista di base (spec punto 12) più alcune categorie aggiuntive necessarie
# per rappresentare fedelmente i dati reali osservati (dividendi/interessi,
# commissioni finanziarie, entrate non altrimenti classificate, telecom).
# Estendibile: aggiungere qui nuove voci quando servono, non "inventarle"
# nel corpo delle funzioni.
CATEGORY_TAXONOMY = {
    "food", "restaurants", "transport", "shopping", "housing",
    "subscriptions", "health", "sports", "travel", "utilities",
    "salary", "investment", "dividends_interest", "financial_fees",
    "other_income", "telecom", "unknown",
}

# Mappatura NATIVA -> nostra tassonomia, per fonti che forniscono già una
# categoria esplicita (es. Banca Sella). Le chiavi sono confrontate in
# lowercase. Se una categoria nativa non è presente qui, category diventa
# "unknown" ma category_raw preserva comunque il valore originale: nessuna
# invenzione, nessuna perdita di informazione (spec punto 24).
CATEGORY_NATIVE_MAP_SELLA = {
    "tasse, servizi e commissioni": "financial_fees",
    "dividendi, cedole e interessi": "dividends_interest",
    "entrate varie": "other_income",
}

# Mappatura tipo nativo Trade Republic -> (transaction_type, category).
# "unknown" per tipi non ancora visti: da estendere qui quando si
# incontrano nuovi valori (es. "DEPOSIT", "WITHDRAWAL", "ROUNDUP", ...),
# senza inventare nel frattempo una classificazione non supportata.
TRADE_REPUBLIC_TYPE_MAP = {
    "buy": ("investment", "investment"),
    "sell": ("investment", "investment"),
    "dividend": ("income", "dividends_interest"),
    "interest_payment": ("interest", "dividends_interest"),
    "tax_optimization": ("tax", "financial_fees"),
}


# ----------------------------------------------------------------------------
# CONFIG — Normalizzazione merchant
# ----------------------------------------------------------------------------
# Regole regex -> nome canonico. Elenco volutamente piccolo e derivato solo
# da evidenza osservata nei campioni reali: NON è una lista esaustiva, va
# estesa quando si incontrano nuove varianti. Normalizzare il nome di un
# merchant non implica assegnargli una categoria di spesa (vedi principio
# sulle categorie in testa al file).
MERCHANT_NORMALIZATION_RULES: List[Tuple[str, str]] = [
    (r"amazon|amzn", "Amazon"),
    (r"paypal", "PayPal"),
    (r"hutchison\s*drei", "Hutchison Drei"),
    (r"\bspar\b", "Spar"),
]


# ----------------------------------------------------------------------------
# CONFIG — Alias di colonna per il parser generico / ricerca timestamp
# ----------------------------------------------------------------------------
# Ripresi e adattati da money_ingest_Primordial_version.py. Usati:
#  - come UNICO meccanismo di parsing per fonti non riconosciute
#    (generic_bank_csv_export), per restare estendibili a nuovi formati
#    senza modificare il codice (spec punto 24 / punto 26);
#  - come rete di sicurezza per trovare la colonna data/ora anche nelle
#    fonti "conosciute" (Trade Republic, Sella), nel caso l'header reale
#    contenga colonne diverse da quelle mostrate come esempio.
TIMESTAMP_ALIAS_KEYS = [
    "timestamp", "date", "datetime", "booking date", "booking_date",
    "transaction date", "data operazione", "data",
    "buchungstag", "time",
]

# Alias usati SOLO per la seconda data (timestamp_end), quando la fonte la
# distingue esplicitamente dalla data principale (es. data valuta/
# settlement date). Se nessuno di questi alias produce un valore
# parsabile, timestamp_end viene semplicemente impostato uguale a
# timestamp_begin (confermato esplicitamente: nessuna invenzione di una
# seconda data quando la fonte non la distingue).
TIMESTAMP_END_ALIAS_KEYS = [
    "value date", "value_date", "settlement date", "data valuta", "valuta",
]


# ----------------------------------------------------------------------------
# CONFIG — Etichetta leggibile dell'istituto/banca
# ----------------------------------------------------------------------------
# Affianca (non sostituisce) il campo tecnico `source`. `source` resta il
# valore usato per logica/dedup/riconoscimento; `institution` è pensato
# solo per essere leggibile da un umano o da un LLM senza dover conoscere
# la convenzione interna dei nomi sorgente.
INSTITUTION_LABELS = {
    "meinelba_csv_export": "meinElba (Raiffeisen)",
    "traderepublic_csv_export": "Trade Republic",
    "sella_csv_export": "Banca Sella",
}


# ----------------------------------------------------------------------------
# CONFIG — Riconoscimento titoli/strumenti finanziari dalla descrizione
# ----------------------------------------------------------------------------
# Pattern ISIN standard: 2 lettere (paese) + 9 alfanumerici + 1 cifra di
# controllo. Usato per recuperare un riferimento al titolo (isin/nome)
# quando non è disponibile in un campo strutturato ma compare comunque nel
# testo della descrizione (es. Banca Sella: "LU1953188833 - ETF-UBS FND
# SOL MSCI", oppure Trade Republic: "Cash Dividend for ISIN BRPETRACNOR9").
# Volutamente semplice (una sola regex + un pattern di nome opzionale):
# l'obiettivo è recuperare un riferimento quando è ovvio nel testo, non
# costruire un parser di descrizioni completo.
ISIN_PATTERN = re.compile(r"\b([A-Z]{2}[A-Z0-9]{9}[0-9])\b")

DESCRIPTION_ALIAS_KEYS = [
    "description", "descrizione", "details", "booking text", "reference",
    "note", "memo", "text", "causale", "narration", "title",
]

AMOUNT_ALIAS_KEYS = ["amount", "importo", "betrag", "value", "totale"]
CURRENCY_ALIAS_KEYS = ["currency", "divisa", "valuta", "ccy"]
CATEGORY_ALIAS_KEYS = ["category", "categoria", "tag", "classification"]
COUNTERPARTY_ALIAS_KEYS = [
    "counterparty", "counterparty_name", "beneficiary", "payee", "merchant",
    "recipient", "destinatario", "beneficiario",
]
ACCOUNT_ALIAS_KEYS = ["account", "iban", "conto", "account_ref", "account_type"]


# ----------------------------------------------------------------------------
# CONFIG — Tipi di transazione ammessi
# ----------------------------------------------------------------------------
# Lista minima richiesta dalla spec (punto 10), estesa con "tax" per
# distinguere ottimizzazioni/rimborsi fiscali (visti nei dati Trade
# Republic) da una generica "fee". Convenzione del segno: income positivo,
# expense negativo (confermata esplicitamente).
TRANSACTION_TYPES = {
    "income", "expense", "transfer", "refund", "fee", "interest",
    "investment", "cash_withdrawal", "cash_deposit", "tax", "unknown",
}


# ============================================================================
# NORMALIZATION — utility generiche
# ============================================================================

def normalize_string(value: Any) -> str:
    """Converte un valore in stringa pulita; None -> stringa vuota."""
    if value is None:
        return ""
    return str(value).strip()


def clean_whitespace(text: str) -> str:
    """Comprime spazi/newline multipli in uno spazio singolo."""
    return re.sub(r"\s+", " ", text or "").strip()


def safe_float_eu_or_us(value: Any) -> Optional[float]:
    """
    Converte una stringa numerica in float, gestendo sia il formato europeo
    (1.234,56 oppure -11,78) sia quello americano (1,234.56).

    Perché serve: meinElba/Sella usano la virgola come separatore
    decimale, mentre fonti future potrebbero usare il punto. Non si può
    assumere un solo formato (spec punto 28).
    """
    raw = normalize_string(value)
    if not raw:
        return None
    raw = raw.replace("€", "").replace("EUR", "").replace("eur", "").strip()
    raw = raw.replace(" ", "")

    if "." in raw and "," in raw:
        # L'ultimo separatore incontrato è quello decimale.
        if raw.rfind(",") > raw.rfind("."):
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", "")
    elif "," in raw:
        raw = raw.replace(".", "").replace(",", ".")

    raw = re.sub(r"[^0-9.\-+]", "", raw)
    if raw in ("", "-", "+", "."):
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# Formati data/ora noti, in ordine di probabilità decrescente per le fonti
# attualmente supportate. Elenco estendibile.
_DATETIME_FORMATS = [
    "%d.%m.%Y %H:%M:%S:%f",   # meinElba: 25.08.2026 00:55:40:612
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%Y-%m-%dT%H:%M:%S.%fZ",  # Trade Republic ISO con millisecondi
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
]


def parse_flexible_datetime(value: Any) -> Optional[datetime]:
    """
    Prova a interpretare una stringa data/ora con i formati noti.
    Gestisce anche il caso "25.08.2026 00:55:40:612" (meinElba usa i due
    punti anche prima dei millisecondi, che va normalizzato in un punto
    prima dello strptime).
    """
    raw = normalize_string(value)
    if not raw:
        return None

    # meinElba: "HH:MM:SS:mmm" -> "HH:MM:SS.mmm" (ultimo ':' diventa '.')
    fixed = raw
    match = re.match(r"^(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}):(\d+)$", raw)
    if match:
        fixed = f"{match.group(1)}.{match.group(2)}"

    for fmt in _DATETIME_FORMATS:
        try:
            return datetime.strptime(fixed, fmt)
        except ValueError:
            continue

    # Ultimo tentativo: fromisoformat gestisce molte varianti ISO.
    try:
        return datetime.fromisoformat(fixed.replace("Z", "+00:00"))
    except ValueError:
        return None


def to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def get_first_alias_value(row: Dict[str, str], alias_keys: List[str]) -> str:
    """
    Cerca il primo valore non vuoto tra una lista di possibili nomi di
    colonna (case-insensitive, con match sia esatto sia parziale).
    Ripreso da money_ingest_Primordial_version.py: è il meccanismo che
    rende il parser generico estendibile a colonne non ancora conosciute.
    """
    lower_row = {k.strip().lower(): v for k, v in row.items() if k}

    for key in alias_keys:
        k = key.strip().lower()
        if k in lower_row and normalize_string(lower_row[k]):
            return normalize_string(lower_row[k])

    for row_key, row_value in lower_row.items():
        for candidate in alias_keys:
            c = candidate.strip().lower()
            if c and c in row_key and normalize_string(row_value):
                return normalize_string(row_value)

    return ""


def normalize_merchant(raw_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Applica MERCHANT_NORMALIZATION_RULES al testo grezzo.
    Ritorna (merchant_normalizzato_o_None, merchant_raw_o_None).
    merchant_raw viene popolato SOLO se diverso in modo utile dal
    normalizzato, per evitare ridondanza (spec punto 22).
    """
    if not raw_text:
        return None, None
    lowered = raw_text.lower()
    for pattern, canonical in MERCHANT_NORMALIZATION_RULES:
        if re.search(pattern, lowered):
            raw_clean = clean_whitespace(raw_text)[:120]
            if raw_clean.lower() == canonical.lower():
                return canonical, None
            return canonical, raw_clean
    return None, None


def resolve_institution_label(source: str, file_name: str) -> str:
    """
    Etichetta leggibile dell'istituto finanziario, derivata dal `source`
    già rilevato euristicamente. Per fonti non riconosciute, include il
    nome del file come indizio utile per capire manualmente di quale banca
    si tratti, invece di un'etichetta generica non informativa.
    """
    return INSTITUTION_LABELS.get(source, f"Banca non riconosciuta (file: {file_name})")


def extract_instrument_reference(description: str) -> Dict[str, Optional[str]]:
    """
    Cerca un riferimento a un titolo/strumento finanziario dentro un testo
    libero (descrizione), quando non è già disponibile in un campo
    strutturato. Riconosce:
      - un codice ISIN (regex ISIN_PATTERN)
      - un nome leggibile, SOLO se compare nel pattern comune
        "<ISIN> - <nome>" (es. Banca Sella) o "ISIN <codice> <nome>"
        (es. Trade Republic "Sell trade US02079... ALPHABET INC...")

    Se non trova nulla, ritorna isin=None, name=None (nessuna invenzione).
    Volutamente semplice: copre i casi osservati nei dati reali, non tutti
    i formati testuali immaginabili.
    """
    if not description:
        return {"isin": None, "name": None}

    match = ISIN_PATTERN.search(description)
    if not match:
        return {"isin": None, "name": None}

    isin = match.group(1)
    name = None

    # Pattern "<ISIN> - <nome>" (Banca Sella)
    after_dash = re.match(r"\s*-\s*([^,;]{3,80})", description[match.end():])
    if after_dash:
        name = clean_whitespace(after_dash.group(1))

    # Pattern "<ISIN> <NOME IN MAIUSCOLO...>" (Trade Republic, es.
    # "Sell trade US02079K3059 ALPHABET INC.CL.A DL-,001, quantity: ...")
    if not name:
        after_space = re.match(r"\s+([A-Z][A-Z0-9 .,\-]{3,60})", description[match.end():])
        if after_space:
            name = clean_whitespace(after_space.group(1)).rstrip(",")

    return {"isin": isin, "name": name}


def backfill_instrument_reference(txn: Dict[str, Any]) -> None:
    """
    Applica extract_instrument_reference() in-place quando la transazione
    non ha già isin/name da un campo strutturato. Non sovrascrive dati già
    presenti (es. symbol/name di Trade Republic restano quelli nativi,
    più affidabili di qualsiasi estrazione testuale).

    Applicato a TUTTE le transazioni (non solo domain="investment"),
    perché anche un conto bancario "normale" (es. Sella) può contenere
    righe legate a un titolo (dividendi, ritenute) senza che l'account
    stesso sia un conto di investimento.
    """
    instrument = txn.get("instrument") or {}
    isin = instrument.get("isin")
    name = instrument.get("name")

    if not isin:
        extracted = extract_instrument_reference(txn.get("description_full") or "")
        isin = isin or extracted["isin"]
        name = name or extracted["name"]

    if isin or name:
        merged = dict(instrument)
        merged["isin"] = isin
        merged["name"] = name
        txn["instrument"] = merged
    # Se non c'è nulla da aggiungere e instrument era già None, resta None
    # (non si crea un dict vuoto senza motivo).


def make_transaction_id(*parts: Any) -> str:
    """
    Costruisce un id stabile e leggibile da un insieme di parti, quando la
    fonte non fornisce un id nativo. Non è un hash crittografico: è
    deterministico e sufficiente per dedup/full_ref, e resta leggibile per
    debug (a differenza di un hash puro).
    """
    safe_parts = [re.sub(r"\s+", "_", normalize_string(p))[:40] for p in parts if p is not None]
    return "__".join(safe_parts) if safe_parts else "unknown_txn"


# ============================================================================
# NORMALIZATION — riconoscimento sorgente
# ============================================================================
#
# Il riconoscimento è PURAMENTE euristico su header/contenuto (deciso
# esplicitamente: nessuna convenzione di sottocartelle/nome file usata come
# segnale primario). Ogni file CSV nella cartella di input viene ispezionato
# indipendentemente dagli altri.
# ============================================================================

def sniff_csv_dialect_and_header(raw_text: str) -> Tuple[str, List[str], bool]:
    """
    Ispeziona il testo grezzo di un CSV e determina:
      - il delimitatore più probabile
      - gli header (se la prima riga sembra un header)
      - se il file ha o meno un header (has_header)

    meinElba non ha header: la prima riga inizia direttamente con una data
    in formato dd.mm.yyyy seguita da ';'. Questo è il segnale usato per
    distinguere "niente header" da "c'è un header".
    """
    sample = raw_text[:4000]
    candidates = [";", ",", "\t", "|"]
    delimiter = max(candidates, key=lambda d: sample.count(d))

    first_line = raw_text.splitlines()[0] if raw_text.splitlines() else ""
    first_cell = first_line.split(delimiter)[0].strip().strip('"')

    looks_like_date = bool(re.match(r"^\d{2}\.\d{2}\.\d{4}$", first_cell)) or bool(
        re.match(r"^\d{4}-\d{2}-\d{2}", first_cell)
    )

    has_header = not looks_like_date

    header: List[str] = []
    if has_header:
        try:
            reader = csv.reader(io.StringIO(first_line), delimiter=delimiter, quotechar='"')
            header = [clean_whitespace(h) for h in next(reader)]
        except Exception:
            header = []

    return delimiter, header, has_header


def detect_source_type(header: List[str], has_header: bool) -> str:
    """
    Determina la fonte in base (solo) a header/contenuto strutturale.

    Ritorna una delle stringhe:
      - "bank_meinelba_export"
      - "broker_traderepublic_export"
      - "bank_sella_export"
      - "generic_bank_csv_export"
    """
    if not has_header:
        # Nessun header + delimitatore ';' + prima cella = data -> meinElba.
        return "bank_meinelba_export"

    lower_header = {h.strip().lower() for h in header}

    # Trade Republic: combinazione di colonne tipiche di un export broker.
    trade_republic_signature = {"shares", "fee", "tax", "transaction_id", "asset_class"}
    if len(trade_republic_signature & lower_header) >= 3:
        return "broker_traderepublic_export"

    # Banca Sella: colonne italiane tipiche di un export di conto corrente.
    sella_signature = {"divisa", "importo", "codice identificativo", "categoria"}
    if len(sella_signature & lower_header) >= 2:
        return "bank_sella_export"

    return "generic_bank_csv_export"


# ============================================================================
# NORMALIZATION — lettura file robusta (encoding/delimiter)
# ============================================================================

def read_text_with_fallback_encoding(path: Path) -> str:
    """Prova diversi encoding comuni negli export bancari europei."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    raise RuntimeError(f"Impossibile leggere {path} con gli encoding noti.")


# ============================================================================
# NORMALIZATION — parser per-sorgente
# ============================================================================
#
# Ogni parser produce una lista di "transazioni" nello schema comune
# descritto in build_transaction_record(). I parser NON applicano
# classificazione finale (transaction_type/category): quella è delegata a
# classify_transaction(), così la logica di classificazione resta in un
# unico posto (facile da modificare senza toccare il parsing).
# ============================================================================

def parse_meinelba_description(raw_desc: str) -> Dict[str, str]:
    """
    Estrae counterparty/iban/riferimento dal blob di testo lunghissimo che
    meinElba mette nella colonna descrizione. Se un pattern non è presente,
    il campo resta vuoto (nessuna invenzione).
    """
    result = {"counterparty_name": "", "counterparty_iban": "", "payment_reference": ""}

    for label in ("Payment recipient:", "Recipient:"):
        if label in raw_desc:
            after = raw_desc.split(label, 1)[1]
            result["counterparty_name"] = after.split(";", 1)[0].split(" IBAN:")[0].strip()
            break

    iban_match = re.search(r"IBAN:\s*([A-Z0-9]{10,34})", raw_desc)
    if iban_match:
        result["counterparty_iban"] = iban_match.group(1)

    for label in ("Purpose of use:", "Payment reference:"):
        if label in raw_desc:
            after = raw_desc.split(label, 1)[1]
            result["payment_reference"] = after.split(";", 1)[0].strip()
            break

    if not result["counterparty_name"] and "ONLINE BANKING" in raw_desc.upper():
        result["counterparty_name"] = clean_whitespace(raw_desc)[:80]

    return result


def parse_meinelba_file(raw_text: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Parser posizionale per meinElba (nessun header).

    Layout osservato (6 colonne, delimitatore ';', quote '"'):
      0: data operazione     (dd.mm.yyyy)
      1: descrizione         (blob di testo tra virgolette)
      2: data valuta         (dd.mm.yyyy)
      3: importo             (formato europeo, es. -11,78)
      4: valuta              (es. EUR)
      5: timestamp completo  (dd.mm.yyyy HH:MM:SS:mmm)

    Nota su un possibile artefatto di copia-incolla: due transazioni che
    sembrano concatenate senza newline sono state confermate come un
    probabile errore di copia-incolla dell'utente, non una caratteristica
    reale del file. csv.reader gestisce comunque correttamente i campi tra
    virgolette che contengono newline reali, quindi non serve una logica
    speciale per "riparare" righe concatenate: se il file reale ha newline
    corretti (anche dentro il campo quotato), il parsing è già robusto.
    """
    transactions: List[Dict[str, Any]] = []
    reader = csv.reader(io.StringIO(raw_text), delimiter=";", quotechar='"')

    for idx, row in enumerate(reader):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) < 6:
            continue

        raw_date, raw_desc, raw_value_date, raw_amount, raw_currency, raw_full_ts = row[:6]

        dt_full = parse_flexible_datetime(raw_full_ts) or parse_flexible_datetime(raw_date)
        # timestamp_end: meinElba distingue esplicitamente "data valuta"
        # (colonna 2) dalla data operazione. Se non è parsabile, resta
        # uguale a timestamp_begin (nessuna seconda data inventata).
        dt_value = parse_flexible_datetime(raw_value_date)
        amount = safe_float_eu_or_us(raw_amount)
        currency = normalize_string(raw_currency).upper() or "EUR"
        desc_clean = clean_whitespace(raw_desc)
        extracted = parse_meinelba_description(desc_clean)

        merchant, merchant_raw = normalize_merchant(
            extracted["counterparty_name"] or desc_clean
        )

        transactions.append({
            "source": "meinelba_csv_export",
            "domain": "bank",
            "account_ref": "meinelba_checking",
            "timestamp_begin": to_iso(dt_full),
            "timestamp_end": to_iso(dt_value) or to_iso(dt_full),
            "amount": amount,
            "currency": currency,
            "description_full": desc_clean,
            "counterparty_name": extracted["counterparty_name"] or None,
            "counterparty_iban": extracted["counterparty_iban"] or None,
            "payment_reference": extracted["payment_reference"] or None,
            "merchant": merchant,
            "merchant_raw": merchant_raw,
            "category_raw": None,   # meinElba non fornisce categorie native
            "native_type": None,
            "instrument": None,     # concetto non applicabile al dominio bancario
            "native_id": None,      # meinElba non fornisce un id nativo di riga
            "source_file": file_name,
            "record_index_in_source": idx,
        })

    return transactions


def parse_traderepublic_file(raw_text: str, delimiter: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Parser per Trade Republic. Usa DictReader con l'header REALE letto dal
    file (non posizioni fisse), perché l'utente ha confermato che
    l'ordine/elenco colonne di esempio potrebbe non coincidere esattamente
    col file vero. I nomi di colonna "di dominio" (symbol, shares, price,
    fee, tax, ecc.) sono invece usati per nome esatto perché quelli sono
    stati forniti come header reale e affidabile.
    """
    transactions: List[Dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')

    for idx, row in enumerate(reader):
        if not row or not any(normalize_string(v) for v in row.values()):
            continue

        # Nomi di colonna noti e affidabili (forniti esplicitamente).
        native_type = normalize_string(row.get("type")).lower()
        native_category = normalize_string(row.get("category"))  # es. TRADING/CASH
        native_account_type = normalize_string(row.get("account_type")) or "default"
        name = normalize_string(row.get("name"))
        symbol = normalize_string(row.get("symbol"))
        shares = safe_float_eu_or_us(row.get("shares"))
        price = safe_float_eu_or_us(row.get("price"))
        amount = safe_float_eu_or_us(row.get("amount"))
        fee = safe_float_eu_or_us(row.get("fee"))
        tax = safe_float_eu_or_us(row.get("tax"))
        currency = normalize_string(row.get("currency")).upper() or "EUR"
        original_amount = safe_float_eu_or_us(row.get("original_amount"))
        original_currency = normalize_string(row.get("original_currency")).upper() or None
        fx_rate = safe_float_eu_or_us(row.get("fx_rate"))
        description = clean_whitespace(normalize_string(row.get("description")))
        native_id = normalize_string(row.get("transaction_id")) or None
        counterparty_name = normalize_string(row.get("counterparty_name")) or None
        counterparty_iban = normalize_string(row.get("counterparty_iban")) or None
        payment_reference = normalize_string(row.get("payment_reference")) or None

        # Timestamp: NON assunto per posizione. Cercato per alias, perché
        # l'header fornito come esempio potrebbe non includere la vera
        # colonna data/ora del file reale (vedi nota in testa al file).
        dt = parse_flexible_datetime(get_first_alias_value(row, TIMESTAMP_ALIAS_KEYS))
        # timestamp_end: Trade Republic non ha mostrato finora una seconda
        # data distinta (es. settlement date) negli esempi visti; se
        # comparisse in futuro, TIMESTAMP_END_ALIAS_KEYS la intercetta
        # automaticamente. In assenza, resta uguale a timestamp_begin.
        dt_end = parse_flexible_datetime(get_first_alias_value(row, TIMESTAMP_END_ALIAS_KEYS)) or dt

        merchant, merchant_raw = normalize_merchant(name or description)

        transactions.append({
            "source": "traderepublic_csv_export",
            "domain": "investment",
            "account_ref": f"traderepublic_{native_account_type.lower()}",
            "timestamp_begin": to_iso(dt),
            "timestamp_end": to_iso(dt_end),
            "amount": amount,
            "currency": currency,
            "description_full": description,
            "counterparty_name": counterparty_name,
            "counterparty_iban": counterparty_iban,
            "payment_reference": payment_reference,
            "merchant": merchant,
            "merchant_raw": merchant_raw,
            "category_raw": native_category or None,
            "native_type": native_type or None,
            "instrument": {
                "isin": symbol or None,
                "name": name or None,
                "shares": shares,
                "unit_price": price,
                "fee": fee,
                "tax": tax,
                "original_amount": original_amount,
                "original_currency": original_currency,
                "fx_rate": fx_rate,
            },
            "native_id": native_id,
            "source_file": file_name,
            "record_index_in_source": idx,
        })

    return transactions


def parse_sella_file(raw_text: str, delimiter: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Parser per Banca Sella. Header reale in italiano, con categorie native
    (Categoria/Sottocategoria) che vengono usate direttamente invece di
    essere indovinate.
    """
    transactions: List[Dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')

    for idx, row in enumerate(reader):
        if not row or not any(normalize_string(v) for v in row.values()):
            continue

        native_id = normalize_string(row.get("Codice identificativo")) or None
        raw_date = normalize_string(row.get("Data operazione"))
        raw_value_date = normalize_string(row.get("Data valuta"))
        description = clean_whitespace(normalize_string(row.get("Descrizione")))
        currency = normalize_string(row.get("Divisa")).upper() or "EUR"
        amount = safe_float_eu_or_us(row.get("Importo"))
        native_category = normalize_string(row.get("Categoria"))
        native_subcategory = normalize_string(row.get("Sottocategoria"))

        dt = parse_flexible_datetime(raw_date) or parse_flexible_datetime(raw_value_date)
        # timestamp_end: Sella distingue esplicitamente "Data valuta" da
        # "Data operazione". Se non è parsabile, resta uguale a
        # timestamp_begin.
        dt_value = parse_flexible_datetime(raw_value_date)

        merchant, merchant_raw = normalize_merchant(description)

        category_raw_combined = " / ".join(
            [p for p in (native_category, native_subcategory) if p and p != "-"]
        ) or None

        transactions.append({
            "source": "sella_csv_export",
            "domain": "bank",
            "account_ref": "sella_conto",
            "timestamp_begin": to_iso(dt),
            "timestamp_end": to_iso(dt_value) or to_iso(dt),
            "amount": amount,
            "currency": currency,
            "description_full": description,
            "counterparty_name": None,
            "counterparty_iban": None,
            "payment_reference": None,
            "merchant": merchant,
            "merchant_raw": merchant_raw,
            "category_raw": category_raw_combined,
            "native_type": native_category or None,
            "instrument": None,
            "native_id": native_id,
            "source_file": file_name,
            "record_index_in_source": idx,
        })

    return transactions


def parse_generic_file(raw_text: str, delimiter: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Parser di fallback per CSV bancari non riconosciuti. Usa esclusivamente
    ricerca per alias di colonna (nessuna posizione fissa), così qualunque
    nuovo formato bancario può essere ingerito senza modificare il codice
    (spec punto 24: estendibilità a nuovi formati).
    """
    transactions: List[Dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')

    for idx, row in enumerate(reader):
        if not row or not any(normalize_string(v) for v in row.values()):
            continue

        dt = parse_flexible_datetime(get_first_alias_value(row, TIMESTAMP_ALIAS_KEYS))
        dt_end = parse_flexible_datetime(get_first_alias_value(row, TIMESTAMP_END_ALIAS_KEYS)) or dt
        amount = safe_float_eu_or_us(get_first_alias_value(row, AMOUNT_ALIAS_KEYS))
        currency = get_first_alias_value(row, CURRENCY_ALIAS_KEYS).upper() or "EUR"
        description = clean_whitespace(get_first_alias_value(row, DESCRIPTION_ALIAS_KEYS))
        category_raw = get_first_alias_value(row, CATEGORY_ALIAS_KEYS) or None
        counterparty = get_first_alias_value(row, COUNTERPARTY_ALIAS_KEYS) or None
        account_ref = get_first_alias_value(row, ACCOUNT_ALIAS_KEYS) or "generic_account"

        merchant, merchant_raw = normalize_merchant(counterparty or description)

        transactions.append({
            "source": "generic_bank_csv_export",
            "domain": "bank",
            "account_ref": account_ref,
            "timestamp_begin": to_iso(dt),
            "timestamp_end": to_iso(dt_end),
            "amount": amount,
            "currency": currency,
            "description_full": description,
            "counterparty_name": counterparty,
            "counterparty_iban": None,
            "payment_reference": None,
            "merchant": merchant,
            "merchant_raw": merchant_raw,
            "category_raw": category_raw,
            "native_type": None,
            "instrument": None,
            "native_id": None,
            "source_file": file_name,
            "record_index_in_source": idx,
            # Campi non riconosciuti dal parser generico vengono comunque
            # preservati integralmente, per non perdere informazione su
            # formati mai visti prima (spec punto 24).
            "extra_fields": {k: v for k, v in row.items() if normalize_string(v)},
        })

    return transactions


# ============================================================================
# CLASSIFICATION — transaction_type + category
# ============================================================================
#
# Priorità (spec punto 21, "balanced"):
#   1. Segnali nativi espliciti (native_type, category_raw mappato)
#   2. Segno dell'importo (income se positivo, expense se negativo) come
#      fallback quando non c'è alcun segnale nativo di tipo
#   3. Keyword ad alta confidenza SOLO per transaction_type (mai per
#      category), attivate solo a livello "balanced"/"aggressive"
#   4. "unknown" se nessuna evidenza sufficiente
# ============================================================================

_KEYWORDS_CASH_WITHDRAWAL = ("atm", "bancomat", "withdrawal", "cash withdrawal")
_KEYWORDS_TRANSFER = ("bonifico", "sepa", "transfer", "online banking")
_KEYWORDS_SALARY = ("stipendio", "salary", "salario")
_KEYWORDS_FEE = ("commission", "commissione", "spese", "fee")


def classify_transaction(txn: Dict[str, Any]) -> Tuple[str, str]:
    """
    Ritorna (transaction_type, category) per una transazione normalizzata,
    seguendo la priorità descritta sopra. Non modifica txn in place: la
    chiamata a questa funzione è esplicita e visibile dove viene usata.
    """
    domain = txn.get("domain")
    native_type = (txn.get("native_type") or "").lower()
    category_raw = txn.get("category_raw")
    amount = txn.get("amount")
    description = (txn.get("description_full") or "").lower()

    # 1. Segnali nativi espliciti più forti: Trade Republic.
    if domain == "investment" and native_type in TRADE_REPUBLIC_TYPE_MAP:
        return TRADE_REPUBLIC_TYPE_MAP[native_type]

    # 1b. Categoria nativa esplicita (Sella): mappata se conosciuta.
    if category_raw:
        mapped = CATEGORY_NATIVE_MAP_SELLA.get(category_raw.split(" / ")[0].lower())
        if mapped:
            # Il transaction_type resta comunque dedotto dal segno, perché
            # una "categoria" non implica univocamente entrata/uscita
            # (es. una commissione può comparire come importo negativo).
            base_type = "income" if (amount is not None and amount > 0) else "expense"
            if mapped == "financial_fees":
                base_type = "fee"
            if mapped == "dividends_interest":
                base_type = "income"
            return base_type, mapped

    # 2. Fallback sul segno, se non c'è nulla di nativo.
    if amount is None:
        base_type = "unknown"
    elif amount > 0:
        base_type = "income"
    elif amount < 0:
        base_type = "expense"
    else:
        base_type = "unknown"

    # 3. Raffinamento tramite keyword ad alta confidenza (solo
    #    transaction_type, mai category), attivo da "balanced" in su.
    if ACTIVITY_INFERENCE_LEVEL in ("balanced", "aggressive"):
        if any(k in description for k in _KEYWORDS_CASH_WITHDRAWAL):
            base_type = "cash_withdrawal"
        elif any(k in description for k in _KEYWORDS_SALARY):
            base_type = "income"
        elif any(k in description for k in _KEYWORDS_FEE):
            base_type = "fee"
        elif ACTIVITY_INFERENCE_LEVEL == "aggressive" and any(
            k in description for k in _KEYWORDS_TRANSFER
        ):
            base_type = "transfer"

    return base_type, "unknown"


# ============================================================================
# DEDUPLICATION
# ============================================================================

def make_dedup_key(txn: Dict[str, Any]) -> str:
    """
    Chiave di deduplicazione.

    - Se la fonte fornisce un id nativo stabile (native_id) e
      DEDUP_USE_NATIVE_ID_WHEN_AVAILABLE è True, la chiave è
      (source, native_id): affidabile, nessuna euristica necessaria.

    - Altrimenti, la chiave combina: source, account_ref, timestamp
      completo (non solo la data, per ridurre falsi positivi tra
      transazioni identiche nello stesso giorno), importo, valuta e un
      prefisso della descrizione. Non è perfetta (due transazioni
      realmente identiche allo stesso secondo verrebbero comunque
      considerate duplicate), ma è il compromesso indicato come
      accettabile per ora.
    """
    if DEDUP_USE_NATIVE_ID_WHEN_AVAILABLE and txn.get("native_id"):
        return f"{txn.get('source')}||native_id||{txn['native_id']}"

    desc_prefix = normalize_string(txn.get("description_full"))[:DEDUP_DESCRIPTION_PREFIX_LEN].lower()
    return "||".join([
        normalize_string(txn.get("source")),
        normalize_string(txn.get("account_ref")),
        normalize_string(txn.get("timestamp_begin")),
        normalize_string(txn.get("amount")),
        normalize_string(txn.get("currency")),
        desc_prefix,
    ])


def deduplicate_transactions(transactions: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """Rimuove duplicati mantenendo la prima occorrenza. Ritorna (record, n_rimossi)."""
    seen = set()
    result = []
    removed = 0
    for txn in transactions:
        key = make_dedup_key(txn)
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        result.append(txn)
    return result, removed


# ============================================================================
# AGGREGATION — bucket temporali
# ============================================================================

def compute_bucket_bounds(dt: datetime, granularity: str) -> Tuple[datetime, datetime]:
    """
    Calcola (timestamp_begin, timestamp_end) del bucket temporale che
    contiene `dt`, secondo la granularità. Usato al posto di un
    identificatore testuale di periodo (es. "2026-08"): il bucket viene
    quindi identificato/ordinato tramite i suoi stessi timestamp, coerente
    col resto del dataset dove si usano sempre timestamp_begin/end
    piuttosto che etichette di periodo.

    - daily:   dalle 00:00:00 alle 23:59:59.999999 dello stesso giorno
    - weekly:  dal lunedì 00:00:00 alla domenica 23:59:59.999999 (ISO)
    - monthly: dal primo all'ultimo istante del mese di calendario

    Nessuna conversione di timezone (vedi nota su aggregation_timestamp
    più sotto): le date sono trattate come naive, così come fornite dagli
    export bancari.
    """
    if granularity == "daily":
        begin = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end = begin + timedelta(days=1) - timedelta(microseconds=1)

    elif granularity == "weekly":
        begin = (dt - timedelta(days=dt.isoweekday() - 1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end = begin + timedelta(days=7) - timedelta(microseconds=1)

    elif granularity == "monthly":
        begin = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (
            begin.replace(year=begin.year + 1, month=1)
            if begin.month == 12
            else begin.replace(month=begin.month + 1)
        )
        end = next_month - timedelta(microseconds=1)

    else:
        raise ValueError(f"Granularità non supportata: {granularity}")

    return begin, end


def build_financial_aggregations(transactions: List[Dict[str, Any]], rich: bool) -> Dict[str, Any]:
    """
    Costruisce le aggregazioni finanziarie per ogni granularità configurata
    in AGGREGATION_GRANULARITIES, SEMPRE separate per currency (spec punto
    11: mai sommare valute diverse insieme) e per domain (bank/investment),
    perché mescolare cash flow bancario e flussi di investimento
    produrrebbe un "net cash flow" fuorviante.

    Ogni bucket contiene: timestamp_begin/timestamp_end (inizio e fine
    esatti del bucket), income_total, expense_total, net_total,
    by_category (dict categoria -> totale).

    Il parametro `rich` controlla se includere anche `by_merchant`: un
    dict per ogni merchant con il totale speso E la lista dei
    transaction_id collegati (utile in FULL per "vai a vedere tutte le
    transazioni di questo merchant"). In PRIMARY (rich=False) questo
    dettaglio viene omesso: non è stato ritenuto abbastanza utile da solo
    per giustificare lo spazio nel budget, a favore di più transazioni
    individuali dirette in `notable_transactions` (dove il merchant è già
    presente per singola transazione).
    """
    aggregations: Dict[str, Any] = {}

    for granularity in AGGREGATION_GRANULARITIES:
        buckets: Dict[Tuple[datetime, str, str], Dict[str, Any]] = {}

        for txn in transactions:
            if not txn.get("timestamp_begin") or txn.get("amount") is None:
                continue
            dt = datetime.fromisoformat(txn["timestamp_begin"])
            bucket_begin, bucket_end = compute_bucket_bounds(dt, granularity)

            bucket_key = (bucket_begin, txn["currency"], txn["domain"])
            bucket = buckets.setdefault(bucket_key, {
                "timestamp_begin": bucket_begin,
                "timestamp_end": bucket_end,
                "currency": txn["currency"],
                "domain": txn["domain"],
                "income_total": 0.0,
                "expense_total": 0.0,
                "net_total": 0.0,
                "transaction_count": 0,
                "_by_category": defaultdict(float),
                "_by_merchant_total": defaultdict(float),
                "_by_merchant_refs": defaultdict(list),
            })

            amount = txn["amount"]
            bucket["net_total"] += amount
            bucket["transaction_count"] += 1
            if amount > 0:
                bucket["income_total"] += amount
            elif amount < 0:
                bucket["expense_total"] += abs(amount)
                if txn.get("merchant"):
                    bucket["_by_merchant_total"][txn["merchant"]] += abs(amount)
                    bucket["_by_merchant_refs"][txn["merchant"]].append(txn["transaction_id"])

            bucket["_by_category"][txn.get("category", "unknown")] += amount

        # Finalizza: arrotonda e rimuove gli accumulatori privati "_by_*".
        finalized = []
        for bucket in sorted(buckets.values(), key=lambda b: b["timestamp_begin"]):
            entry = {
                "timestamp_begin": to_iso(bucket["timestamp_begin"]),
                "timestamp_end": to_iso(bucket["timestamp_end"]),
                "currency": bucket["currency"],
                "domain": bucket["domain"],
                "income_total": round(bucket["income_total"], 2),
                "expense_total": round(bucket["expense_total"], 2),
                "net_total": round(bucket["net_total"], 2),
                "transaction_count": bucket["transaction_count"],
                "by_category": {k: round(v, 2) for k, v in bucket["_by_category"].items()},
            }
            if rich:
                entry["by_merchant"] = [
                    {
                        "merchant": merchant,
                        "total": round(total, 2),
                        "transaction_refs": bucket["_by_merchant_refs"][merchant],
                    }
                    for merchant, total in sorted(
                        bucket["_by_merchant_total"].items(), key=lambda kv: kv[1], reverse=True
                    )
                ]
            finalized.append(entry)

        aggregations[granularity] = finalized

    return aggregations


# ============================================================================
# ANOMALY DETECTION (leggera)
# ============================================================================

def flag_unusual_transactions(transactions: List[Dict[str, Any]]) -> None:
    """
    Marca in-place ogni transazione con `is_unusual` (bool), calcolato per
    gruppo (category, currency, domain) tramite z-score sull'importo
    assoluto. Richiede almeno ANOMALY_MIN_SAMPLES transazioni comparabili
    nel gruppo, altrimenti non calcola nulla (is_unusual = False) per
    evitare falsi positivi su gruppi troppo piccoli.
    """
    groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for txn in transactions:
        if txn.get("amount") is None:
            continue
        key = (txn.get("category", "unknown"), txn.get("currency"), txn.get("domain"))
        groups[key].append(txn)

    for _, group_txns in groups.items():
        if len(group_txns) < ANOMALY_MIN_SAMPLES:
            for txn in group_txns:
                txn["is_unusual"] = False
            continue

        amounts = [abs(t["amount"]) for t in group_txns]
        mean = statistics.mean(amounts)
        stdev = statistics.pstdev(amounts)
        for txn in group_txns:
            if stdev == 0:
                txn["is_unusual"] = False
                continue
            z = (abs(txn["amount"]) - mean) / stdev
            txn["is_unusual"] = z > ANOMALY_ZSCORE_THRESHOLD


# ============================================================================
# RECURRING DETECTION
# ============================================================================

def detect_recurring_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Raggruppa le transazioni per (merchant o firma descrizione, currency,
    domain, segno dell'importo) e verifica i tre criteri di evidenza
    descritti in RECURRING_* (occorrenze, coerenza importo, coerenza
    intervallo). Ritorna una lista di pattern ricorrenti riconosciuti,
    ciascuno con i riferimenti (full_ref) alle transazioni che lo
    compongono.
    """
    groups: Dict[Tuple[str, str, str, str], List[Dict[str, Any]]] = defaultdict(list)

    for txn in transactions:
        if txn.get("amount") is None or not txn.get("timestamp_begin"):
            continue
        signature = txn.get("merchant") or normalize_string(txn.get("description_full"))[:40].lower()
        if not signature:
            continue
        sign = "positive" if txn["amount"] > 0 else "negative"
        key = (signature, txn["currency"], txn["domain"], sign)
        groups[key].append(txn)

    recurring: List[Dict[str, Any]] = []

    for (signature, currency, domain, sign), group_txns in groups.items():
        if len(group_txns) < RECURRING_MIN_OCCURRENCES:
            continue

        group_txns_sorted = sorted(group_txns, key=lambda t: t["timestamp_begin"])
        amounts = [abs(t["amount"]) for t in group_txns_sorted]
        mean_amount = statistics.mean(amounts)
        if mean_amount == 0:
            continue
        amount_ok = all(
            abs(a - mean_amount) / mean_amount <= RECURRING_AMOUNT_TOLERANCE_PCT
            for a in amounts
        )
        if not amount_ok:
            continue

        dates = [datetime.fromisoformat(t["timestamp_begin"]) for t in group_txns_sorted]
        intervals_days = [(b - a).days for a, b in zip(dates, dates[1:])]
        if not intervals_days:
            continue
        median_interval = statistics.median(intervals_days)
        interval_ok = all(
            abs(d - median_interval) <= RECURRING_INTERVAL_TOLERANCE_DAYS
            for d in intervals_days
        )
        if not interval_ok:
            continue

        pattern_type = "subscription" if (sign == "negative" and median_interval <= 40) else (
            "recurring_income" if sign == "positive" else "regular_bill"
        )

        recurring.append({
            "signature": signature,
            "pattern_type": pattern_type,
            "domain": domain,
            "currency": currency,
            "occurrences": len(group_txns_sorted),
            "average_amount": round(mean_amount * (1 if sign == "positive" else -1), 2),
            "median_interval_days": median_interval,
            "first_seen": to_iso(dates[0]),
            "last_seen": to_iso(dates[-1]),
            "transaction_refs": [t["transaction_id"] for t in group_txns_sorted],
        })

    return recurring


# ============================================================================
# GROUPING — pairing acquisto/rimborso
# ============================================================================

def detect_refund_groupings(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Individua coppie (spesa, rimborso) sullo stesso account_ref, stessa
    valuta, importo uguale e di segno opposto (entro
    GROUPING_AMOUNT_TOLERANCE), entro GROUPING_REFUND_WINDOW_DAYS giorni.
    Non raggruppa transazioni solo perché vicine nel tempo (spec punto 15):
    l'importo speculare è la condizione necessaria, il tempo è solo un
    vincolo di finestra.
    """
    by_account: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for txn in transactions:
        if txn.get("amount") is not None and txn.get("timestamp_begin"):
            by_account[txn["account_ref"]].append(txn)

    groupings: List[Dict[str, Any]] = []
    used_ids = set()

    for account_ref, txns in by_account.items():
        txns_sorted = sorted(txns, key=lambda t: t["timestamp_begin"])
        for i, txn_a in enumerate(txns_sorted):
            if txn_a["transaction_id"] in used_ids or txn_a["amount"] >= 0:
                continue
            date_a = datetime.fromisoformat(txn_a["timestamp_begin"])
            for txn_b in txns_sorted[i + 1:]:
                if txn_b["transaction_id"] in used_ids:
                    continue
                if txn_b["currency"] != txn_a["currency"]:
                    continue
                date_b = datetime.fromisoformat(txn_b["timestamp_begin"])
                if (date_b - date_a).days > GROUPING_REFUND_WINDOW_DAYS:
                    break
                if abs(txn_b["amount"] + txn_a["amount"]) <= GROUPING_AMOUNT_TOLERANCE and txn_b["amount"] > 0:
                    groupings.append({
                        "grouping_type": "purchase_refund",
                        "account_ref": account_ref,
                        "currency": txn_a["currency"],
                        "amount": abs(txn_a["amount"]),
                        "purchase_ref": txn_a["transaction_id"],
                        "refund_ref": txn_b["transaction_id"],
                        "days_between": (date_b - date_a).days,
                    })
                    used_ids.add(txn_a["transaction_id"])
                    used_ids.add(txn_b["transaction_id"])
                    break

    return groupings


# ============================================================================
# NOTABILITY SCORE (usato per ordinare la selezione in PRIMARY e per
# decidere quali transazioni restano "ricche" di dettaglio in FULL a
# PRUNE_LEVEL aggressive)
# ============================================================================

def compute_notability_scores(transactions: List[Dict[str, Any]]) -> None:
    """
    Calcola in-place `notability_score` per ogni transazione, combinando:
      - importo normalizzato (percentile all'interno di stessa
        currency+domain, così un investimento in USD non viene confrontato
        direttamente con una spesa al supermercato in EUR)
      - un bonus di recency che decade esponenzialmente con
        NOTABILITY_RECENCY_HALF_LIFE_DAYS

    I pesi sono in NOTABILITY_WEIGHT_AMOUNT / NOTABILITY_WEIGHT_RECENCY.
    """
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for txn in transactions:
        if txn.get("amount") is not None:
            groups[(txn["currency"], txn["domain"])].append(txn)

    now = datetime.utcnow()

    for _, group_txns in groups.items():
        amounts_sorted = sorted(abs(t["amount"]) for t in group_txns)
        n = len(amounts_sorted)

        for txn in group_txns:
            # Percentile rank approssimato (0..1) dell'importo assoluto.
            rank = amounts_sorted.index(abs(txn["amount"]))
            amount_score = rank / max(n - 1, 1)

            recency_score = 0.0
            if txn.get("timestamp_begin"):
                age_days = (now - datetime.fromisoformat(txn["timestamp_begin"])).days
                recency_score = 0.5 ** (max(age_days, 0) / NOTABILITY_RECENCY_HALF_LIFE_DAYS)

            score = (
                NOTABILITY_WEIGHT_AMOUNT * amount_score
                + NOTABILITY_WEIGHT_RECENCY * recency_score
            )
            if txn.get("is_unusual"):
                score += 0.25  # piccolo bonus esplicito, non moltiplicativo

            txn["notability_score"] = round(score, 4)


# ============================================================================
# FULL — costruzione del dataset analitico
# ============================================================================

def apply_full_pruning(txn: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applica PRUNE_LEVEL al livello di dettaglio testuale di una
    transazione dentro FULL (non tocca i campi numerici/di
    classificazione, che restano sempre presenti: quelli servono per le
    aggregazioni e non pesano molto).
    """
    out = dict(txn)
    extra_fields = out.pop("extra_fields", None)

    if PRUNE_LEVEL == "light":
        out["description"] = out.pop("description_full", "")[:DESCRIPTION_MAX_LENGTH_LIGHT]
        if extra_fields:
            out["extra_fields"] = extra_fields

    elif PRUNE_LEVEL == "medium":
        out["description"] = out.pop("description_full", "")[:DESCRIPTION_MAX_LENGTH_MEDIUM]
        if extra_fields:
            out["extra_fields"] = extra_fields  # solo se non vuoti

    else:  # aggressive
        is_notable = out.get("is_unusual") or out.get("domain") == "investment" or (
            out.get("notability_score", 0) > 0.6
        )
        max_len = DESCRIPTION_MAX_LENGTH_LIGHT if is_notable else DESCRIPTION_MAX_LENGTH_AGGRESSIVE_ORDINARY
        out["description"] = out.pop("description_full", "")[:max_len]
        # A livello aggressive gli extra_fields di record non notevoli non
        # vengono propagati in FULL: sono già stati preservati una tantum
        # nel _logic/_metadata a livello di file_reports, se necessario.
        if extra_fields and is_notable:
            out["extra_fields"] = extra_fields

    return out


def build_full_payload(
    transactions: List[Dict[str, Any]],
    aggregations: Dict[str, Any],
    recurring: List[Dict[str, Any]],
    groupings: List[Dict[str, Any]],
    file_reports: List[Dict[str, Any]],
    errors: List[Dict[str, Any]],
    warnings: List[Dict[str, Any]],
    dedup_removed: int,
) -> Dict[str, Any]:
    """Assembla il payload FULL con documentazione interna per l'LLM."""
    pruned_transactions = [apply_full_pruning(t) for t in transactions]

    timestamps = [t["timestamp_begin"] for t in transactions if t.get("timestamp_begin")]

    payload = {
        "_metadata": {
            "dataset": "bank_dataset_full",
            "source": "bank_export",
            "version": DATASET_VERSION,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "purpose": (
                "Rappresentazione normalizzata e analitica di tutte le "
                "transazioni bancarie e di investimento. Usato quando "
                "PRIMARY (bank_dataset.json) non contiene abbastanza "
                "dettaglio per rispondere alla domanda."
            ),
            "prune_level": PRUNE_LEVEL,
            "activity_inference_level": ACTIVITY_INFERENCE_LEVEL,
            "records_total": len(pruned_transactions),
            "duplicates_removed": dedup_removed,
            "min_date": min(timestamps) if timestamps else None,
            "max_date": max(timestamps) if timestamps else None,
            "files_processed": len(file_reports),
            "errors": errors,
            "warnings": warnings,
        },
        "_schema": {
            "transactions": (
                "Lista di transazioni normalizzate. Ogni transazione ha "
                "domain='bank'|'investment', source (identificatore tecnico "
                "dell'esportatore) + institution (etichetta leggibile, es. "
                "'Trade Republic', 'Banca Sella', 'meinElba (Raiffeisen)', "
                "o 'Banca non riconosciuta (file: ...)' per fonti nuove), "
                "transaction_type, category, amount con segno (positivo="
                "income, negativo=expense), currency esplicita (mai "
                "convertita automaticamente), timestamp_begin/timestamp_end "
                "(coincidono quando la fonte non distingue data operazione "
                "da data valuta), e — quando riconoscibile — isin/name "
                "dentro 'instrument' per collegare la transazione al "
                "titolo che l'ha generata (acquisto/vendita/dividendo/"
                "interesse)."
            ),
            "financial_aggregations": (
                "Dict per granularità ('daily'/'weekly'/'monthly'), lista "
                "di bucket sempre separati per currency e per domain: "
                "mescolare valute o bank/investment produrrebbe totali "
                "fuorvianti. Ogni bucket è identificato da timestamp_begin/"
                "timestamp_end (inizio e fine esatti del bucket), non da "
                "un'etichetta testuale di periodo. by_merchant include, "
                "per ogni merchant, sia il totale sia transaction_refs "
                "(lista di transaction_id) per risalire alle transazioni "
                "originali."
            ),
            "recurring_transactions": (
                "Pattern ricorrenti riconosciuti con evidenza (occorrenze, "
                "coerenza importo/intervallo). transaction_refs punta ai "
                "transaction_id delle transazioni in 'transactions'."
            ),
            "groupings": (
                "Coppie di transazioni collegate logicamente (es. "
                "acquisto+rimborso), non semplicemente vicine nel tempo."
            ),
        },
        "_logic": {
            "sign_convention": "income positivo, expense negativo (importi già firmati nel campo amount)",
            "transaction_id_purpose": (
                "Identificatore stabile usato SOLO per collegare le sezioni "
                "del dataset tra loro (full_ref da PRIMARY, transaction_refs "
                "in recurring/groupings/by_merchant, chiave di dedup). Non è "
                "pensato per essere 'leggibile' dall'utente finale."
            ),
            "timestamp_begin_vs_end": (
                "timestamp_begin = data operazione (o trade date per gli "
                "investimenti); timestamp_end = data valuta/settlement "
                "date quando la fonte la distingue esplicitamente (es. "
                "meinElba, Banca Sella). Se la fonte non distingue le due "
                "date (es. Trade Republic, finché non fornisce una colonna "
                "dedicata), timestamp_end è semplicemente uguale a "
                "timestamp_begin: nessuna seconda data viene inventata. "
                "Nota: timestamp_end può talvolta precedere timestamp_begin "
                "(una 'data valuta' retroattiva rispetto alla 'data "
                "operazione' è un comportamento reale delle fonti bancarie, "
                "non un errore di parsing)."
            ),
            "institution_field": (
                "source_type/source restano l'identificatore tecnico usato "
                "per riconoscimento/dedup; institution è la stessa "
                "informazione resa leggibile per un umano o un LLM."
            ),
            "instrument_reference": (
                "isin/name dentro 'instrument' provengono prima da campi "
                "strutturati nativi (es. colonne symbol/name di Trade "
                "Republic), e solo se assenti da un'estrazione testuale "
                "semplice dalla descrizione (pattern ISIN + nome vicino, "
                "vedi extract_instrument_reference). Applicato a qualunque "
                "transazione, non solo domain='investment', perché anche "
                "un conto bancario puo contenere righe legate a un titolo "
                "(es. dividendi Banca Sella)."
            ),
            "classification_priority": (
                "1) segnali nativi espliciti della fonte, 2) segno "
                "dell'importo, 3) keyword ad alta confidenza solo per "
                "transaction_type (mai per category) se ACTIVITY_INFERENCE_LEVEL "
                "!= 'conservative', 4) 'unknown' se nessuna evidenza"
            ),
            "category_policy": (
                "La category resta 'unknown' quando la fonte non fornisce "
                "un segnale nativo esplicito: non viene mai indovinata da "
                "keyword generiche. category_raw conserva sempre il dato "
                "nativo originale, se esiste."
            ),
            "deduplication": (
                "Priorità a un id nativo stabile quando disponibile "
                "(transaction_id/Codice identificativo); altrimenti chiave "
                "composita source+account_ref+timestamp completo+amount+"
                "currency+prefisso descrizione."
            ),
            "aggregation_timestamp": (
                "timestamp_begin è l'unico timestamp usato per assegnare "
                "una transazione a un bucket (daily/weekly/monthly); "
                "nessuna conversione timezone (date trattate come naive)."
            ),
            "recurring_detection": (
                f"Richiede >= {RECURRING_MIN_OCCURRENCES} occorrenze con "
                f"stesso merchant/firma, importo entro "
                f"{RECURRING_AMOUNT_TOLERANCE_PCT*100:.0f}% e intervallo "
                f"coerente entro {RECURRING_INTERVAL_TOLERANCE_DAYS} giorni "
                "dalla mediana."
            ),
            "how_to_retrieve_detail_from_full": (
                "Ogni riferimento 'full_ref' in PRIMARY corrisponde a "
                "'transactions[i].transaction_id' in questo file FULL."
            ),
        },
        "transactions": pruned_transactions,
        "financial_aggregations": aggregations,
        "recurring_transactions": recurring,
        "groupings": groupings,
        "file_reports": file_reports,
    }

    return payload


# ============================================================================
# PRIMARY — vista LLM-oriented, budget-aware
# ============================================================================

def estimate_json_size_bytes(obj: Any) -> int:
    return len(json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8"))


def build_primary_transaction_view(txn: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vista compatta di una transazione per PRIMARY: solo i campi utili a un
    LLM per rispondere a domande comuni, con full_ref verso FULL per il
    dettaglio completo (spec punto 17).

    isin/instrument_name vengono inclusi solo quando esiste un riferimento
    a un titolo (da campo nativo o da estrazione testuale — vedi
    backfill_instrument_reference), indipendentemente dal domain: una riga
    di dividendo su un conto bancario "normale" (es. Banca Sella) è utile
    quanto un BUY/SELL su un conto broker per rispondere a "quale titolo
    ha generato questo movimento".
    """
    instrument = txn.get("instrument") or {}

    view = {
        "transaction_id": txn["transaction_id"],
        "institution": txn.get("institution"),
        "timestamp_begin": txn.get("timestamp_begin"),
        "timestamp_end": txn.get("timestamp_end"),
        "amount": txn.get("amount"),
        "currency": txn.get("currency"),
        "domain": txn.get("domain"),
        "transaction_type": txn.get("transaction_type"),
        "category": txn.get("category"),
        "merchant": txn.get("merchant"),
        "is_unusual": txn.get("is_unusual", False),
        "full_ref": f"transactions/{txn['transaction_id']}",
    }

    if instrument.get("isin") or instrument.get("name"):
        view["isin"] = instrument.get("isin")
        view["instrument_name"] = instrument.get("name")
        if instrument.get("shares") is not None:
            view["shares"] = instrument.get("shares")

    return view


def build_primary_dataset(
    transactions: List[Dict[str, Any]],
    aggregations: Dict[str, Any],
    recurring: List[Dict[str, Any]],
    file_reports: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Costruisce PRIMARY selezionando le transazioni individuali in base al
    notability_score, entro il budget PRIMARY_MAX_SIZE_MB (con soft
    overflow), dopo aver garantito l'inclusione delle sezioni sempre utili
    (aggregazioni, recurring). Vedi CONFIG in testa al file per la logica
    di budget dettagliata.
    """
    base_payload = {
        "_metadata": {
            "dataset": "bank_dataset",
            "source": "bank_export",
            "version": DATASET_VERSION,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "purpose": (
                "Vista compatta e LLM-oriented delle transazioni bancarie "
                "e di investimento. Privilegia aggregazioni finanziarie, "
                "pattern ricorrenti e transazioni individuali rilevanti. "
                "Se l'informazione richiesta non è qui, recuperarla da "
                "bank_dataset_full.json tramite il campo full_ref."
            ),
            "prune_level": PRUNE_LEVEL,
            "primary_max_size_mb_target": PRIMARY_MAX_SIZE_MB,
            "records_total_available": len(transactions),
        },
        "_schema": {
            "financial_aggregations": (
                "Stessa struttura di bank_dataset_full.json (bucket con "
                "timestamp_begin/timestamp_end, income/expense/net_total, "
                "by_category), sempre incluso per intero qui. NON include "
                "'by_merchant': in PRIMARY si è scelto di dare priorità a "
                "più transazioni individuali dirette (vedi "
                "notable_transactions, dove ogni transazione ha già il "
                "proprio merchant) invece che a un riepilogo per merchant, "
                "ritenuto meno utile qui rispetto allo spazio che "
                "occuperebbe nel budget."
            ),
            "recurring_transactions": "Pattern ricorrenti, sempre incluso per intero qui",
            "notable_transactions": (
                "Sottoinsieme budget-aware delle transazioni individuali "
                "più rilevanti (importo, recency, anomalie). Ogni voce ha "
                "timestamp_begin/timestamp_end, institution (banca/broker "
                "leggibile), e — quando pertinente — isin/instrument_name "
                "per rispondere a 'quale titolo'. full_ref punta a "
                "bank_dataset_full.json per il dettaglio completo "
                "(descrizione integrale, controparte, IBAN, ecc.)."
            ),
        },
        "_logic": {
            "why_aggregations_come_first": (
                "Le domande più comuni (quanto ho speso questo mese, quali "
                "sono le mie categorie di spesa, quali entrate ho avuto) "
                "sono risolvibili dalle aggregazioni senza bisogno delle "
                "transazioni individuali: per questo occupano priorità "
                "piena nel budget, indipendentemente dalla loro dimensione "
                "(che resta comunque piccola)."
            ),
            "why_no_by_merchant_here": (
                "by_merchant con transaction_refs esiste solo in FULL: qui "
                "occuperebbe spazio nel budget senza aggiungere molto "
                "rispetto a scorrere le notable_transactions, che già "
                "riportano il merchant per ogni singola transazione."
            ),
            "budget_policy": (
                f"notable_transactions viene riempito in ordine di "
                f"notability_score decrescente finché la dimensione "
                f"cumulata resta sotto {PRIMARY_MAX_SIZE_MB}MB. Se il "
                f"prossimo elemento supera il target ma resta entro "
                f"{PRIMARY_SOFT_OVERFLOW_RATIO}x il target, viene incluso "
                "comunque (soft overflow) e la selezione si ferma dopo."
            ),
            "how_to_retrieve_detail": "usare full_ref per recuperare la transazione completa da bank_dataset_full.json",
        },
        "financial_aggregations": aggregations,
        "recurring_transactions": recurring,
    }

    base_size = estimate_json_size_bytes(base_payload)
    target_bytes = PRIMARY_MAX_SIZE_MB * 1024 * 1024
    soft_limit_bytes = target_bytes * PRIMARY_SOFT_OVERFLOW_RATIO

    # Le transazioni recenti (ultimi PRIMARY_MIN_RECENT_DAYS_GUARANTEED
    # giorni) vengono sempre valutate per prime, indipendentemente dal loro
    # notability_score, per garantire che il mese corrente sia sempre ben
    # rappresentato anche se il budget si esaurisce prima.
    now = datetime.utcnow()

    def is_recent(t: Dict[str, Any]) -> bool:
        if not t.get("timestamp_begin"):
            return False
        age_days = (now - datetime.fromisoformat(t["timestamp_begin"])).days
        return age_days <= PRIMARY_MIN_RECENT_DAYS_GUARANTEED

    candidates = sorted(
        transactions,
        key=lambda t: (not is_recent(t), -t.get("notability_score", 0)),
    )

    notable_transactions: List[Dict[str, Any]] = []
    cumulative_size = base_size

    for txn in candidates:
        view = build_primary_transaction_view(txn)
        view_size = estimate_json_size_bytes(view)

        if cumulative_size + view_size <= target_bytes:
            notable_transactions.append(view)
            cumulative_size += view_size
            continue

        # Sopra il target: consentito solo un soft overflow, poi ci si ferma.
        if cumulative_size + view_size <= soft_limit_bytes:
            notable_transactions.append(view)
            cumulative_size += view_size
        break

    base_payload["notable_transactions"] = notable_transactions
    base_payload["_metadata"]["notable_transactions_included"] = len(notable_transactions)
    base_payload["_metadata"]["estimated_size_bytes"] = cumulative_size

    return base_payload


# ============================================================================
# I/O — collezione file, scrittura output
# ============================================================================

def collect_input_files(input_dir: Path) -> List[Path]:
    if not input_dir.exists():
        return []
    return sorted(input_dir.rglob("*.csv"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)


# ============================================================================
# ENTRYPOINT PRINCIPALE
# ============================================================================

def ingest_bank_history() -> Dict[str, Any]:
    """
    Entry point principale. Flusso:
      1. valida config (PRUNE_LEVEL/ACTIVITY_INFERENCE_LEVEL)
      2. legge tutti i CSV in BANK_INPUT_DIR
      3. per ciascuno: rileva sorgente, applica il parser corretto
      4. normalizza timestamp/classificazione, deduplica
      5. calcola aggregazioni, recurring, groupings, anomaly flags, notability
      6. costruisce FULL e PRIMARY
      7. scrive SOLO bank_dataset.json e bank_dataset_full.json
    """
    if PRUNE_LEVEL not in VALID_PRUNE_LEVELS:
        raise ValueError(f"PRUNE_LEVEL non valido: {PRUNE_LEVEL}. Ammessi: {VALID_PRUNE_LEVELS}")
    if ACTIVITY_INFERENCE_LEVEL not in VALID_ACTIVITY_INFERENCE_LEVELS:
        raise ValueError(
            f"ACTIVITY_INFERENCE_LEVEL non valido: {ACTIVITY_INFERENCE_LEVEL}. "
            f"Ammessi: {VALID_ACTIVITY_INFERENCE_LEVELS}"
        )

    errors: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    file_reports: List[Dict[str, Any]] = []
    all_transactions: List[Dict[str, Any]] = []

    input_files = collect_input_files(BANK_INPUT_DIR)

    if not BANK_INPUT_DIR.exists():
        warnings.append({
            "warning_type": "missing_input_directory",
            "message": f"La directory {BANK_INPUT_DIR} non esiste.",
        })

    for file_path in input_files:
        try:
            raw_text = read_text_with_fallback_encoding(file_path)
            delimiter, header, has_header = sniff_csv_dialect_and_header(raw_text)
            source_type = detect_source_type(header, has_header)

            if source_type == "bank_meinelba_export":
                txns = parse_meinelba_file(raw_text, file_path.name)
            elif source_type == "broker_traderepublic_export":
                txns = parse_traderepublic_file(raw_text, delimiter, file_path.name)
            elif source_type == "bank_sella_export":
                txns = parse_sella_file(raw_text, delimiter, file_path.name)
            else:
                txns = parse_generic_file(raw_text, delimiter, file_path.name)

            for txn in txns:
                # transaction_id: usa native_id se presente, altrimenti
                # costruisce un id deterministico dai campi disponibili.
                # Serve SOLO a collegare tra loro le sezioni del dataset
                # (full_ref in PRIMARY, transaction_refs in recurring/
                # groupings, dedup): non è pensato per essere "leggibile".
                txn["transaction_id"] = txn.get("native_id") or make_transaction_id(
                    txn["source"], txn["source_file"], txn["record_index_in_source"],
                    txn.get("timestamp_begin"), txn.get("amount"),
                )

                # institution: etichetta leggibile della banca/broker,
                # affiancata al campo tecnico `source`.
                txn["institution"] = resolve_institution_label(txn["source"], txn["source_file"])

                # Arricchisce il riferimento al titolo (isin/nome) dalla
                # descrizione, quando non già disponibile in un campo
                # strutturato (vedi backfill_instrument_reference).
                backfill_instrument_reference(txn)

            all_transactions.extend(txns)
            file_reports.append({
                "file_name": file_path.name,
                "detected_source_type": source_type,
                "records_loaded": len(txns),
                "status": "processed",
            })

        except Exception as exc:
            errors.append({
                "file": file_path.name,
                "error_type": "file_processing_error",
                "message": str(exc),
            })
            file_reports.append({
                "file_name": file_path.name,
                "detected_source_type": None,
                "records_loaded": 0,
                "status": "failed",
            })

    # --- Controllo qualità: timestamp mancanti ---
    # Se una quota rilevante di transazioni di una fonte non ha
    # timestamp_begin, quelle transazioni SPARISCONO silenziosamente dalle
    # aggregazioni temporali e dalla recurring detection (entrambe
    # richiedono un timestamp valido). Questo va segnalato esplicitamente:
    # è spesso sintomo di un header reale diverso da quello atteso (es.
    # colonna data/timestamp non riconosciuta per una fonte nuova/mutata).
    by_source_missing_ts: Dict[str, List[int]] = defaultdict(list)
    for txn in all_transactions:
        if not txn.get("timestamp_begin"):
            by_source_missing_ts[txn["source"]].append(1)
    for source_name, missing_list in by_source_missing_ts.items():
        total_for_source = sum(1 for t in all_transactions if t["source"] == source_name)
        if len(missing_list) / total_for_source >= 0.5:
            warnings.append({
                "warning_type": "missing_timestamp_for_source",
                "source": source_name,
                "message": (
                    f"{len(missing_list)}/{total_for_source} transazioni di "
                    f"'{source_name}' non hanno un timestamp valido: sono "
                    "escluse dalle aggregazioni temporali e dalla recurring "
                    "detection. Verificare che l'header del CSV contenga "
                    "una colonna data/timestamp riconoscibile "
                    "(vedi TIMESTAMP_ALIAS_KEYS)."
                ),
            })

    # --- Classificazione (transaction_type, category) ---
    for txn in all_transactions:
        transaction_type, category = classify_transaction(txn)
        txn["transaction_type"] = transaction_type
        txn["category"] = category

    # --- Deduplicazione ---
    all_transactions, dedup_removed = deduplicate_transactions(all_transactions)

    # --- Anomaly flags (prima della notability, che usa is_unusual) ---
    flag_unusual_transactions(all_transactions)

    # --- Notability score (usato per ordinare la selezione PRIMARY) ---
    compute_notability_scores(all_transactions)

    # --- Aggregazioni, recurring, groupings ---
    # Due varianti: quella "rich" (con by_merchant + transaction_refs) va
    # in FULL, per permettere il collegamento verso le transazioni
    # originali; quella snella va in PRIMARY, dove si è scelto di dare
    # priorità a più transazioni individuali dirette invece che a un
    # riepilogo per merchant (vedi build_financial_aggregations).
    full_aggregations = build_financial_aggregations(all_transactions, rich=True)
    primary_aggregations = build_financial_aggregations(all_transactions, rich=False)
    recurring = detect_recurring_transactions(all_transactions)
    groupings = detect_refund_groupings(all_transactions)

    # --- FULL ---
    full_payload = build_full_payload(
        transactions=all_transactions,
        aggregations=full_aggregations,
        recurring=recurring,
        groupings=groupings,
        file_reports=file_reports,
        errors=errors,
        warnings=warnings,
        dedup_removed=dedup_removed,
    )

    full_size_bytes = estimate_json_size_bytes(full_payload)
    full_size_gb = full_size_bytes / (1024 ** 3)
    if full_size_gb > 0.5:
        warnings.append({
            "warning_type": "full_dataset_large",
            "message": (
                f"bank_dataset_full.json è circa {full_size_gb:.2f} GB. "
                f"Valutare PRUNE_LEVEL='aggressive' per aumentare la compressione."
            ),
        })

    # --- PRIMARY ---
    primary_payload = build_primary_dataset(
        transactions=all_transactions,
        aggregations=primary_aggregations,
        recurring=recurring,
        file_reports=file_reports,
    )

    # --- Scrittura: SOLO questi due file ---
    write_json(BANK_OUTPUT_DATASET_PATH, primary_payload)
    write_json(BANK_OUTPUT_FULL_DATASET_PATH, full_payload)

    return {
        "success": True,
        "input_directory": str(BANK_INPUT_DIR),
        "files_found": len(input_files),
        "files_processed": len(file_reports),
        "records_processed": len(all_transactions),
        "duplicates_removed": dedup_removed,
        "recurring_patterns_found": len(recurring),
        "groupings_found": len(groupings),
        "errors": errors,
        "warnings": warnings,
        "outputs": {
            "primary": str(BANK_OUTPUT_DATASET_PATH),
            "full": str(BANK_OUTPUT_FULL_DATASET_PATH),
        },
        "file_reports": file_reports,
    }


if __name__ == "__main__":
    result = ingest_bank_history()
    if result.get("files_found", 0) == 0:
        print(f"Nessun file CSV trovato in {BANK_INPUT_DIR}.")
    else:
        print("Bank ingestion completata.")
        print("File trovati:", result["files_found"])
        print("Transazioni processate:", result["records_processed"])
        print("Duplicati rimossi:", result["duplicates_removed"])
        print("Pattern ricorrenti trovati:", result["recurring_patterns_found"])
        print("PRIMARY:", result["outputs"]["primary"])
        print("FULL:", result["outputs"]["full"])
        if result["errors"]:
            print("Errori:", len(result["errors"]))
        if result["warnings"]:
            print("Warning:", len(result["warnings"]))