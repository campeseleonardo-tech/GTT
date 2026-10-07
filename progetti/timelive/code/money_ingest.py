# money_ingest.py
# =============================================================================
# MONEY INGEST — Personal Data Vault (SQLite / ingest_engine.py, third
# domain migrated in the 2026-09-14 architecture rebuild — see
# EVOLUTION_LOG.md and timelive.md §8). Covers banking, public-market
# investments, and private markets.
# =============================================================================
#
# WHAT CHANGED FROM THE OLD (PRIMARY/FULL JSON) VERSION OF THIS FILE
# -----------------------------------------------------------------------
# * Output is now THREE tables in the single shared vault.db, not two JSON
#   files: transactions, security_events, private_market_legs. No more
#   PRIMARY/FULL, no more size budget/notability-driven selection — same
#   "fallo sparire del tutto" decision already applied to chess.com/spotify.
# * REAL-DATA FINDING (2026-09-14, inspecting the user's actual 3 export
#   files in Input/Money — meinElba 2,449 rows, Banca Sella 358 usable
#   rows, Trade Republic 441 rows): the old file's assumption that
#   "private markets" would be a separate source/file was WRONG. There is
#   no separate private-markets export anywhere. Private-market activity
#   is 8 rows embedded INSIDE the Trade Republic export, distinguished by
#   asset_class="PRIVATE_FUND" (types PRIVATE_MARKET_BUY and BUY). Each
#   private-market purchase splits into two rows with COMPLEMENTARY null
#   patterns: a "cash leg" (amount populated, shares/price empty) and a
#   "shares leg" (shares+price populated, amount empty), linked only by
#   matching symbol + same-day timestamps + an internal order UUID
#   mentioned in free text that does not match any transaction_id column
#   anywhere. Project owner's explicit decision (2026-09-14 chat): keep
#   both legs as separate rows, never try to pair them — a
#   private_market_legs table, not a private_market_positions table.
# * REAL-DATA FINDING: Trade Republic's export also contains rows that are
#   neither cash movements nor liquid trades — corporate actions
#   (WARRANT_EXERCISE, REVERSE_SPLIT, SPLIT, category=CORPORATE_ACTION)
#   and portfolio migrations (MIGRATION, category=DELIVERY). Both share
#   the same real shape: a signed shares_delta, an optional price, and
#   NO amount/currency at all (these are not cash events). Migrated into
#   their own security_events table rather than forced into transactions
#   as amount=NULL/currency=NULL rows.
# * REAL-DATA FINDING (Sella native id is NOT unique): Banca Sella's
#   "Codice identificativo" collides in exactly 6 real pairs — each pair
#   is one dividend row (positive amount, category "Dividendi, cedole e
#   interessi") and its withholding-tax row (negative amount, category
#   "Tasse, servizi e commissioni"), sharing one operation id because
#   they are two legs of the same underlying event. The old rule
#   ("native id present -> dedup key = source+native_id") would have
#   silently treated one leg of every dividend as a duplicate and
#   dropped it. Project owner's explicit decision: dedup key = source +
#   native_id + sign(amount). Verified against the real file: 0
#   collisions with this key (down from 6 with the naive native-id-only
#   key).
# * REAL-DATA FINDING (Sella has a non-transaction footer row): the raw
#   export's last populated line is a running-balance snapshot
#   ("Saldo al <timestamp>", "12.067,30"), not a transaction — 6 columns
#   instead of the header's 11. Filtered out structurally (row length !=
#   header length), not by content-sniffing, since a blank trailing line
#   has the same problem and the same fix covers both (found: 358 usable
#   rows out of 360 raw lines below the header).
# * REAL-DATA FINDING (Sella's own native categories were mostly being
#   discarded): the old file only ever mapped 3 of Sella's real native
#   Categoria values (financial_fees/dividends_interest/other_income);
#   the real export actually uses 13 distinct native categories. Per
#   timelive.md §3's own category policy ("assigned when the source
#   provides an explicit native category"), CATEGORY_NATIVE_MAP_SELLA
#   below now maps every one of them that has a reasonable fit in the
#   shared taxonomy. Two don't ("Trasferimenti", "Tempo libero" — no
#   clean equivalent exists without inventing a new taxonomy value) and
#   stay category="unknown" with category_raw preserving the original —
#   flagged here as a judgment call, not silently made.
# * REAL BUG FOUND AND FIXED (meinElba millisecond timestamp): the old
#   file's regex-based fix for meinElba's "HH:MM:SS:mmm" format converts
#   the trailing colon to a dot ("44:653" -> "44.653") but then tried to
#   parse the result against a format string that still expected a colon
#   before the milliseconds ("%H:%M:%S:%f") — which can never match a
#   dot. Verified by actually running it against all 2,449 real rows:
#   100% failure on the precise timestamp, silently falling back to the
#   date-only field every single time (the "or" fallback in the old
#   build_record masked this completely — no error, just silently
#   dropped to day-level precision on every single meinElba transaction).
#   Fixed here: the format string now says "%d.%m.%Y %H:%M:%S.%f" (dot).
#   Re-verified: 0 failures on all 2,449 real rows.
# * PRIVACY (2026-09-14 chat, explicit project-owner decision): the raw
#   exports contain the user's own IBAN (in the meinElba filename AND as
#   a structured counterparty_iban on a Trade Republic top-up row), a
#   running account balance (the Sella footer above), and third-party
#   IBANs embedded in meinElba's free-text description ("Recipient IBAN:
#   ..."). None of these are copied into vault.db: counterparty_iban is
#   simply never selected into any output column, and description_full
#   has any "IBAN: <value>" substring redacted (see redact_iban_labels)
#   — a targeted, label-anchored replacement, not a blanket IBAN-shaped
#   regex, because a blanket regex would also clobber ISIN codes that
#   legitimately appear in the same free text (e.g. Sella's
#   "LU1953188833 - ETF-UBS FND SOL MSCI", a 12-character string with
#   the same rough shape as an IBAN but meaningful financial data, not
#   PII). counterparty_name (e.g. a landlord's name on a recurring rent
#   transfer) is KEPT as-is per the same decision — only account/IBAN-
#   shaped identifiers and the balance figure were flagged as the real
#   exposure surface, not people's names.
# * SCOPE (2026-09-14 chat, explicit project-owner decision): recurring-
#   transaction detection and purchase/refund pairing from the old file
#   are DROPPED from this migration, not ported. An LLM with SQL access
#   can already answer "what looks like a subscription" by querying
#   transactions directly; re-adding this as a precomputed table is left
#   for a later pass, once thresholds can be validated against more
#   real usage the way chess.com's session gap was.
# =============================================================================
# 2026-09-14 UPDATE — first real LLM batch tests against this domain
# -----------------------------------------------------------------------
# Ran a short (2-question, max_iterations=2) batch against real vault
# data on the Raspberry Pi with two local models (llama3.2:3b,
# qwen2.5:3b), questions money_04 ("how much invested on Trade Republic,
# buys and sells combined") and money_05 ("what was bought in private
# markets"). Findings from analyzing both reports plus direct re-
# inspection of the real Input/Money files:
# * SCHEMA GAP FOUND AND FIXED (buy vs sell indistinguishable): both
#   models failed or produced wrong SQL on money_04. Root cause verified
#   against the real 441-row Trade Republic export: TRADE_REPUBLIC_TYPE_MAP
#   maps native type "buy" AND "sell" to the identical
#   (transaction_type, category) = ("investment", "investment") pair (199
#   real BUY rows + 105 real SELL rows, all indistinguishable this way),
#   and the native type string itself was being discarded entirely in
#   run_ingest()'s cleanup loop — there was no column left anywhere that
#   could tell a buy from a sell except by re-deriving it from raw
#   amount/shares sign, which no model tried. Fixed (this update):
#   category_raw for Trade Republic transaction rows is now
#   "NATIVE_CATEGORY / NATIVE_TYPE" (e.g. "TRADING / BUY" vs
#   "TRADING / SELL"), mirroring the pattern Sella's category_raw already
#   used. See collect_input_files/parse_traderepublic_file and the
#   category_raw/shares ColumnSpec semantic_notes for the exact signal.
# * REAL BUG FOUND AND FIXED (case-sensitive file discovery):
#   collect_input_files() used Path.rglob("*.csv"), case-sensitive on the
#   Pi's Linux filesystem. Discovered while inspecting
#   Input/Money/paypal/ (see next finding) — its 8 files are all
#   "*.CSV" (uppercase), so they were silently invisible to every ingest
#   run to date, with no warning logged at all. Fixed to match
#   case-insensitively; these files are now discovered and skipped with
#   an explicit logger.warning (no PayPal parser exists yet — see next
#   finding), which is at least honest about what's happening.
# * NOT A BUG (shallow but correct): money_05's "Private Equity" answer
#   for every private-market leg is not an ingest defect — Trade
#   Republic's own `name` field really is just "Private Equity" for
#   these two ISINs in the raw export; there is no richer instrument
#   name anywhere in the source data to surface instead.
# * KNOWN, NOT FIXED (model reasoning, deferred): llama3.2:3b's answer to
#   money_04 was itself a well-formed-looking JSON tool-call string
#   returned as the "final answer" instead of an actual tool call — the
#   same class of bug already tracked in EVOLUTION_LOG.md
#   (_try_parse_malformed_tool_call() in llm_bridge.py), and not
#   recoverable by that existing fix because the model's self-written
#   JSON was itself invalid (an unescaped quote inside the embedded SQL
#   string). No bridge change made this round — project owner's explicit
#   decision was to hold off on bridge/prompt changes ("worked examples")
#   until after tonight's longer cross-domain batch test.
# * NEW REAL DATA SOURCE FOUND, INTEGRATION DEFERRED (PayPal): while
#   investigating the case-sensitivity bug, found a previously-unknown
#   Input/Money/paypal/ folder with 8 real PayPal export CSVs (2 with
#   real rows: 112 + 151 = 263 transactions; 6 are empty/header-only).
#   Format: UTF-8 BOM, 79 quoted Italian-language columns, gross/fee/net
#   structure (Lordo/Tariffa/Netto) plus a running balance column
#   (Saldo — same privacy concern as Sella's footer balance). Two
#   concrete integration risks identified but not yet resolved: (1)
#   double-counting — 73 "Bonifico bancario sul conto PayPal" rows
#   conceptually overlap with outgoing bank transfers already captured
#   in meinElba/Sella; (2) pending status — 91 of ~264 real rows are
#   Stato="In sospeso" (pending), not yet a settled transaction. Project
#   owner's explicit decision (2026-09-14 chat): defer PayPal ingestion
#   to a separate future round rather than build it alongside this fix.
# =============================================================================
# 2026-09-15 UPDATE — overnight cross-domain batch (llama3.2:3b, 58
# questions), model-reasoning bugs traced to exact literal values
# -----------------------------------------------------------------------
# Analyzed the full overnight batch report against real data. No ingest
# bug found this round — every wrong answer traced to the MODEL guessing
# a plausible-but-wrong literal string for a text-filter column, then
# reading zero matching rows as "no data" instead of verifying the value
# first. Three real, reproducible cases, root-caused against the actual
# schema (not assumed):
#   - money_15 ("entrate più alte sul conto Sella"): model filtered
#     institution = "Sella" — the real stored value is "Banca Sella"
#     (see INSTITUTION_LABELS below). 0 rows, false "no data" answer.
#   - money_02b ("spese Amazon ultimi 3 mesi"): model filtered
#     domain = "Amazon" — domain only ever holds 'bank'/'investment';
#     Amazon is a merchant, not a domain. 0 rows, false "no data".
#   - money_13 ("azioni NVIDIA su Trade Republic"): model filtered
#     transaction_type = "buy" (never a real value — Trade Republic buys
#     AND sells both show transaction_type="investment", see
#     TRADE_REPUBLIC_TYPE_MAP) AND instrument_name = "azioni NVIDIA" (a
#     literal Italian phrase, not the real native instrument string).
#     0 rows, "you never bought NVIDIA" — CONFIRMED FALSE by the project
#     owner, who does hold NVIDIA on Trade Republic. The real
#     instrument_name/isin string for it was not re-verified this round
#     (out of scope for this fix — the fix here is making the exact
#     literal values discoverable, not looking up this one holding).
# FIX (this update): enriched 4 ColumnSpec semantic_notes below
# (institution, domain, instrument_name, transaction_type) with the
# exact real literal values / explicit "this is not X" callouts, so a
# model reading the pre-injected schema doesn't have to guess. Paired
# with a general system-prompt rule in llm_bridge.py ("run a discovery
# query before filtering on a value you're not certain is exact") for
# the same failure mode on columns/domains not covered by a specific
# semantic_note. Neither change touches ingest logic or vault.db's
# schema/data — both are metadata-only, model-facing.
# =============================================================================
# 2026-09-17 UPDATE — PayPal added as a 4th source (own table, same file)
# -----------------------------------------------------------------------
# Real-data inspection (Input/Money/paypal/, 2 non-empty files, 263 total
# transactions, 0 id overlap between the two files) found the export is
# richer and structurally different enough from meinElba/Sella/Trade
# Republic that it gets its own TableSpec (paypal_transactions) in this
# same file, rather than being forced into the shared `transactions`
# table — project owner's explicit decision, after discussing both
# options (2026-09-17 chat): "Bonifico bancario"/pending/native-currency
# rows are NOT specific enough to justify losing PayPal's own rich
# columns (Titolo oggetto, Messaggio, indirizzo di spedizione, Codice di
# riferimento bancario, ...), and forcing them into `transactions` would
# add a `stato` column that's NULL for every meinElba/Sella/Trade
# Republic row.
#
# REAL-DATA FINDING (79 columns claimed in EVOLUTION_LOG.md was wrong):
# the real header has 83 columns, not 79. One column name is a genuine
# DUPLICATE: "N° ordine commerciante" appears at both index 31 (79.8%
# filled, 210/263) and index 62 (1.5% filled, 4/263). Verified: 0 rows
# have conflicting values when both are filled, and index 62 is always a
# subset of index 31 (never filled alone) — so no information is lost by
# keeping only the first occurrence. REAL BUG AVOIDED: csv.DictReader
# would have silently kept whichever occurrence comes LAST when building
# its dict from duplicate fieldnames — i.e. index 62, the near-always-
# empty one, exactly backwards from what's wanted. parse_paypal_file()
# below reads by column index via header.index(name), which returns the
# FIRST match, specifically to avoid this trap — do not switch this
# parser to DictReader without re-solving that problem.
#
# 35 of the 83 columns are 0% filled across all 263 real rows (auction/
# loyalty-card/campaign/credit fields PayPal exposes but this account
# has never used) and 3 more are 100%/99.6% filled but CONSTANT across
# every real row ("Idoneità per la protezione" always "02",
# "Transazione di pagamento con Fastlane" always "N", "Punti premio"
# always "N") — both groups excluded from the schema below, project
# owner's explicit decision (same "avoid premature complexity" reasoning
# as elsewhere in this file), not a data-loss risk since neither group
# carries any real signal today.
#
# DEDUP: native_id = "Codice transazione", confirmed unique across the
# combined 263 real rows (0 collisions) — used directly, same pattern as
# Trade Republic's transaction_id.
#
# TIMEZONE: "Fuso orario" (e.g. "CET") is kept as its own native text
# column, NOT used to attach a UTC offset to timestamp_end — CET vs CEST
# is a real DST distinction PayPal's own column already encodes
# natively; converting it ourselves would require a Europe/Rome DST
# lookup this file doesn't otherwise need and risks getting it wrong
# silently. timestamp_end is naive local wall-clock time from Data+Orario,
# consistent with how meinElba/Sella timestamps are already stored.
#
# PRIVACY / "saldo" (running PayPal balance after each transaction):
# explicitly discussed against the existing Sella precedent, where the
# account balance (a single footer snapshot row) is excluded from the
# vault entirely for privacy. Project owner's decision this time: KEEP
# PayPal's saldo (marked ColumnSpec.sensitive=True, the same marker
# built for instagram_ingest.py's DM text — a record of what needs
# careful treatment later, not an access control today), and separately
# asked to retrofit the SAME treatment onto Sella/meinElba's balance
# data. Investigated before touching that already-stable, tested code
# (real files re-inspected, not assumed): meinElba's export has NO
# balance field anywhere (positional 6-column format: date, description,
# value date, amount, currency, full timestamp — confirmed against the
# real file, all 2,449 rows, same shape start to finish); Sella's export
# has exactly ONE balance figure total — the single "Saldo al <export
# timestamp>" footer line already filtered out by parse_sella_file() as
# not a transaction row, not a per-transaction series like PayPal's. So
# there is nothing to add for meinElba, and Sella has only one point-in-
# time value, not a queryable history — flagged back to the project
# owner rather than silently building a 1-row table or skipping the
# request; not yet implemented pending that discussion.
#
# REAL-DATA FINDING (functional test against the real files, not just
# inspection): of the 263 raw PayPal rows, 16 share their native_id
# ("Codice transazione") with exactly one other row — always an
# "Autorizzazione generica" (card/merchant authorization hold, always
# impatto_saldo='Promemoria', i.e. not a real cash movement on its own)
# first reported stato='In sospeso', then the SAME id reported again a
# few seconds to ~2.5 minutes later with its final outcome — stato=
# 'Completata' in 15/16 cases, stato='Stornata' (with tipo changing to
# 'Annullamento autorizzazione') in the 16th. Confirmed the raw export is
# chronologically ordered within each file, so dedup_key=native_id alone
# (via the standard upsert_rows() UPDATE-on-collision path) naturally
# converges to the FINAL state for all 16 — verified directly (both ids
# checked resolve to their real final stato). Net effect: 263 raw lines
# -> 247 distinct paypal_transactions rows, which is the correct count
# (one row per real authorization event, not one row per CSV line) —
# not a data-loss bug. Re-ingest idempotency re-verified (0 newly
# inserted, table stays at 247 rows on a second run against the same
# files).
# =============================================================================

from __future__ import annotations

import logging
import re
import statistics
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ingest_engine import (
    ColumnSpec,
    TableSpec,
    NotabilityConfig,
    UpsertOutcome,
    IngestReport,
    confidence_rate,
    CONFIDENCE_NATIVE,
    CONFIDENCE_INFERRED_HIGH,
    create_schema_for_table,
    upsert_rows,
    compute_notability_scores,
    recency_weight,
    register_table_spec,
)

logger = logging.getLogger("money_ingest")


# ============================================================================
# CONFIGURATION
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Paths (same fallback pattern as chessdotcom_ingest.py/spotify_ingest.py)
# ----------------------------------------------------------------------------
try:
    from config import MONEY_INPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    MONEY_INPUT_DIR = BASE_DIR / "Input" / "Money"
MONEY_INPUT_DIR = Path(MONEY_INPUT_DIR)

SOURCE_PREFIX = "money"

# ----------------------------------------------------------------------------
# CONFIG — notability_score weights, transactions. Same shape as the old
# file's weights (amount / recency / anomaly bonus) — NOT re-derived from
# real query patterns (none exist yet, same caveat chess.com's/spotify's
# session-notability weights carry). Flagged as an invented default here,
# not a validated one.
# ----------------------------------------------------------------------------
NOTABILITY_WEIGHT_AMOUNT = 0.7
NOTABILITY_WEIGHT_RECENCY = 0.3
NOTABILITY_WEIGHT_ANOMALY_BONUS = 0.25
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60

# ----------------------------------------------------------------------------
# CONFIG — Anomaly detection (unchanged formula from the old file: a
# z-score on absolute amount within (category, currency, domain) groups).
# Real-data check (2026-09-14): Sella's 13 native categories mostly have
# >=5 members (min group size needed for this to fire at all) — smallest
# real groups are Rimborsi (2) and Affitto (1), which correctly never get
# a z-score computed (ANOMALY_MIN_SAMPLES below), rather than a false
# "unusual" flag on a group too small to judge.
# ----------------------------------------------------------------------------
ANOMALY_ZSCORE_THRESHOLD = 2.5
ANOMALY_MIN_SAMPLES = 5

# ----------------------------------------------------------------------------
# CONFIG — Classification inference level (unchanged concept from the old
# file). "balanced": native signals + amount sign + a small high-confidence
# keyword set for transaction_type only, never for category.
# ----------------------------------------------------------------------------
ACTIVITY_INFERENCE_LEVEL = "balanced"

_KEYWORDS_CASH_WITHDRAWAL = ("atm", "bancomat", "withdrawal", "cash withdrawal")
_KEYWORDS_SALARY = ("stipendio", "salary", "salario")
_KEYWORDS_FEE = ("commission", "commissione", "spese", "fee")

# ----------------------------------------------------------------------------
# CONFIG — Category taxonomy shared across bank sources. Extended
# 2026-09-14 relative to the old file's version (added nothing new to the
# taxonomy itself — every value below already existed in the old file;
# what changed is CATEGORY_NATIVE_MAP_SELLA now actually uses more of
# them, see module docstring).
# ----------------------------------------------------------------------------
CATEGORY_TAXONOMY = {
    "food", "restaurants", "transport", "shopping", "housing",
    "subscriptions", "health", "sports", "travel", "utilities",
    "salary", "investment", "dividends_interest", "financial_fees",
    "other_income", "telecom", "unknown",
}

# Sella's real native Categoria values (top-level; Sottocategoria stays in
# category_raw for detail) -> our taxonomy. Covers every value actually
# observed in the real export (13 distinct values, 2026-09-14 inspection).
# "Trasferimenti" and "Tempo libero" have no clean fit in the existing
# taxonomy and are left unmapped on purpose (category stays "unknown",
# category_raw keeps the original) rather than inventing a new bucket.
CATEGORY_NATIVE_MAP_SELLA = {
    "bar e ristoranti": "restaurants",
    "casa e famiglia": "housing",
    "viaggi e trasporti": "travel",
    "altre spese": "unknown",
    "entrate varie": "other_income",
    "tasse, servizi e commissioni": "financial_fees",
    "shopping": "shopping",
    "dividendi, cedole e interessi": "dividends_interest",
    "salute e benessere": "health",
    "rimborsi": "other_income",
    "affitto": "housing",
}

# Native Trade Republic `type` -> (transaction_type, category), for rows
# that land in the transactions table (i.e. NOT asset_class=PRIVATE_FUND
# and NOT category in (CORPORATE_ACTION, DELIVERY) — those go to
# private_market_legs / security_events instead, see route_traderepublic_row).
TRADE_REPUBLIC_TYPE_MAP: Dict[str, Tuple[str, str]] = {
    "buy": ("investment", "investment"),
    "sell": ("investment", "investment"),
    "dividend": ("income", "dividends_interest"),
    "interest_payment": ("interest", "dividends_interest"),
    "tax_optimization": ("tax", "financial_fees"),
    "tilg": ("investment", "investment"),  # "Tilgung" = redemption/settlement cash leg
    "customer_inbound": ("transfer", "unknown"),  # top-up from the user's own linked bank account
    "customer_inpayment": ("cash_deposit", "unknown"),  # e.g. Apple Pay top-up
    "transfer_instant_inbound": ("transfer", "unknown"),
    "bonus": ("income", "other_income"),
    "earnings": ("income", "dividends_interest"),
}

# ----------------------------------------------------------------------------
# CONFIG — Merchant normalization (unchanged small curated list from the
# old file; real Sella/meinElba merchants beyond these stay unmatched —
# honest, not a loss, since category_raw/description_full still carry
# the original text).
# ----------------------------------------------------------------------------
MERCHANT_NORMALIZATION_RULES: List[Tuple[str, str]] = [
    (r"amazon|amzn", "Amazon"),
    (r"paypal", "PayPal"),
    (r"hutchison\s*drei", "Hutchison Drei"),
    (r"\bspar\b", "Spar"),
]

# ----------------------------------------------------------------------------
# CONFIG — Financial instrument recognition from free-text description
# (unchanged from the old file — a real ISIN pattern, deliberately simple).
# ----------------------------------------------------------------------------
ISIN_PATTERN = re.compile(r"\b([A-Z]{2}[A-Z0-9]{9}[0-9])\b")

# ----------------------------------------------------------------------------
# CONFIG — IBAN redaction, two patterns:
#   1) label-anchored ("IBAN: <value>", meinElba's format)
#   2) a general IBAN-shaped pattern, needed after a REAL-DATA FINDING
#      (2026-09-14, found by actually querying the test vault.db for the
#      user's own IBAN, not by inspection): Trade Republic embeds the
#      IBAN with NO label at all in some descriptions, e.g. "Incoming
#      transfer from Leonardo Campese (AT913200000013275029)". A blanket
#      IBAN-shaped regex would also match ISIN codes in the same kind of
#      free text — but real IBANs (>=15 chars total: 2-letter country +
#      2 check digits + >=11 more) and ISINs (ALWAYS exactly 12 chars:
#      2-letter country + 9 alnum + 1 check digit) are structurally
#      distinguishable by length, since ISIN's fixed format always yields
#      an 8-character tail after country+check-digits, never reaching the
#      11-character minimum this pattern requires. Verified against every
#      real ISIN seen in this data (US67066G1040, LU1953188833, etc. —
#      none match) and every real IBAN seen (AT913200000013275029,
#      LU89751000135104200E, AT821200050660059008 — all match).
# ----------------------------------------------------------------------------
# REAL BUG FOUND (2026-09-14, found by running this against the actual
# filename, not by inspection): a plain \b word-boundary regex does NOT
# match between "_" and a letter — both count as "word" characters in
# regex terms, so \b never fires at that position. This silently failed
# to match "meinElba_transactions_AT913200000013275029_search.csv"
# (underscore-adjacent), even though it matched fine in free-text
# sentences (space-adjacent). Fixed with explicit lookaround boundaries
# instead of \b. Re-verified against the filename, free-text embeddings,
# and every real ISIN in this data (still correctly excluded).
_IBAN_LABEL_RE = re.compile(r"IBAN:\s*[A-Z0-9]{10,34}")
_IBAN_GENERAL_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z]{2}\d{2}[A-Z0-9]{11,30}(?![A-Za-z0-9])")

# ----------------------------------------------------------------------------
# CONFIG — Institution labels (human-readable, alongside the technical
# `source` field — timelive.md §4 naming standard).
# ----------------------------------------------------------------------------
INSTITUTION_LABELS = {
    "meinelba_csv_export": "meinElba (Raiffeisen)",
    "traderepublic_csv_export": "Trade Republic",
    "sella_csv_export": "Banca Sella",
}


# ============================================================================
# TABLE DECLARATIONS (timelive.md §3 — the "contract" for this domain)
# ============================================================================

TRANSACTIONS_TABLE = TableSpec(
    name="transactions",
    primary_key_column="transaction_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    extra_indexed_columns=["transaction_type", "domain", "merchant", "source"],
    columns=[
        ColumnSpec("transaction_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                    semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("timestamp_begin", "TEXT",
                    semantic_note="operation/trade date; equals timestamp_end when the source doesn't distinguish it from the value/settlement date"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="canonical timestamp — value/settlement date when the source distinguishes it (meinElba, Sella), else equal to timestamp_begin. Can precede timestamp_begin: a retroactive value date is real bank behavior, not a parsing error."),
        ColumnSpec("domain", "TEXT", semantic_note="'bank' (meinElba, Sella) or 'investment' (Trade Republic cash+trades) — only ever these 2 values. This is NOT a merchant or company name: 'Amazon', 'PayPal', etc. never appear here, they are in the merchant column instead."),
        ColumnSpec("source", "TEXT", semantic_note="technical exporter id — meinelba_csv_export/sella_csv_export/traderepublic_csv_export/generic_bank_csv_export"),
        ColumnSpec("institution", "TEXT", semantic_note="human-readable institution name — exactly one of these 3 literal values: 'meinElba (Raiffeisen)', 'Banca Sella', 'Trade Republic'. Not 'Sella' alone, not 'Raiffeisen' alone — use the full string or LIKE '%Sella%' / LIKE '%Trade Republic%'."),
        ColumnSpec("account_ref", "TEXT"),
        ColumnSpec("amount", "REAL", semantic_note="signed: positive=income, negative=expense. Native currency, never auto-converted."),
        ColumnSpec("currency", "TEXT"),
        ColumnSpec("transaction_type", "TEXT",
                    semantic_note="income/expense/transfer/investment/interest/tax/cash_deposit/cash_withdrawal/fee/unknown. For Trade Republic, both BUY and SELL rows have transaction_type='investment' — 'buy'/'sell' are never values of this column. To tell a purchase from a sale, use category_raw (LIKE '%/ BUY' or '%/ SELL') or the sign of shares (positive=buy, negative=sell)."),
        ColumnSpec("category", "TEXT", entity_hint="category",
                    semantic_note="from our shared taxonomy — 'unknown' whenever the source gives no explicit native signal (never guessed from generic keywords)"),
        ColumnSpec("category_raw", "TEXT", semantic_note="original native category/type string, always preserved even when category is 'unknown'. For Trade Republic rows this is 'NATIVE_CATEGORY / NATIVE_TYPE' (e.g. 'TRADING / BUY' vs 'TRADING / SELL') — the only place a buy is distinguishable from a sell, since transaction_type and category both collapse to 'investment' for both (see TRADE_REPUBLIC_TYPE_MAP in money_ingest.py). To find purchases only: category_raw LIKE '%/ BUY' or shares > 0; sales: '%/ SELL' or shares < 0."),
        ColumnSpec("merchant", "TEXT", semantic_note="normalized merchant name from a small curated list — most real merchants stay unmatched (None) on purpose, see module docstring. Trade Republic is never a value here (it's an institution, not a merchant) — use the institution column for it."),
        ColumnSpec("counterparty_name", "TEXT", entity_hint="person"),
        ColumnSpec("description_full", "TEXT", semantic_note="free-text description; any 'IBAN: <value>' substring is redacted (see module docstring's privacy note) — ISIN codes in the same text are NOT touched"),
        ColumnSpec("isin", "TEXT", semantic_note="security identifier, when this transaction relates to one (native field for Trade Republic trades, extracted from free text for others when present)"),
        ColumnSpec("instrument_name", "TEXT", semantic_note="native Trade Republic instrument name string, exactly as the broker wrote it (e.g. a company's official listed name, not a translated or colloquial phrase like 'azioni NVIDIA'). Match it with LIKE '%keyword%' or run a discovery query (SELECT DISTINCT instrument_name FROM transactions WHERE instrument_name LIKE '%...%') first — never an exact string you guessed. isin is a more reliable filter when you already know the ISIN."),
        ColumnSpec("shares", "REAL", semantic_note="signed quantity, populated only for Trade Republic BUY/SELL rows. Sign is a reliable buy/sell signal in the real data: positive=buy, negative=sell (amount sign runs the other way: negative=buy/cash-out, positive=sell/cash-in) — see category_raw for the same distinction via the native type string"),
        ColumnSpec("unit_price", "REAL"),
        ColumnSpec("fee", "REAL"),
        ColumnSpec("tax", "REAL"),
        ColumnSpec("original_amount", "REAL", semantic_note="amount in original_currency before FX conversion, when the source reports one"),
        ColumnSpec("original_currency", "TEXT"),
        ColumnSpec("fx_rate", "REAL"),
        ColumnSpec("native_id", "TEXT", semantic_note="native transaction id when the source provides one (Trade Republic transaction_id, Sella Codice identificativo); None for meinElba/generic"),
        ColumnSpec("is_unusual", "INTEGER", semantic_note="native boolean, 0/1 — z-score flag within (category, currency, domain), see ANOMALY_* config; 0 when the group is too small to judge (< 5 comparable transactions)"),
        ColumnSpec("notability_score", "REAL"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

SECURITY_EVENTS_TABLE = TableSpec(
    name="security_events",
    primary_key_column="event_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    columns=[
        ColumnSpec("event_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True),
        ColumnSpec("timestamp_begin", "TEXT"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="canonical timestamp — these are instantaneous events, timestamp_begin always equals timestamp_end"),
        ColumnSpec("event_type", "TEXT", semantic_note="warrant_exercise/reverse_split/split/migration — native Trade Republic type, lowercased"),
        ColumnSpec("category_raw", "TEXT", semantic_note="native category: CORPORATE_ACTION or DELIVERY"),
        ColumnSpec("isin", "TEXT"),
        ColumnSpec("instrument_name", "TEXT"),
        ColumnSpec("shares_delta", "REAL", semantic_note="signed change in shares held; NOT a cash amount — these rows carry no currency at all (native, real data: no amount/currency field is ever populated for these row types)"),
        ColumnSpec("price", "REAL", semantic_note="only populated for MIGRATION rows in the real data; None for warrant exercises/splits"),
        ColumnSpec("native_id", "TEXT"),
        ColumnSpec("source", "TEXT"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

PRIVATE_MARKET_LEGS_TABLE = TableSpec(
    name="private_market_legs",
    primary_key_column="leg_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    columns=[
        ColumnSpec("leg_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True),
        ColumnSpec("timestamp_begin", "TEXT"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="canonical timestamp — instantaneous events, timestamp_begin always equals timestamp_end"),
        ColumnSpec("leg_type", "TEXT", semantic_note="'cash' (amount populated, no shares/price) or 'shares' (shares+price populated, no amount) — see module docstring: the two legs of one purchase are NOT paired/merged, kept as separate rows on purpose"),
        ColumnSpec("isin", "TEXT"),
        ColumnSpec("instrument_name", "TEXT"),
        ColumnSpec("amount", "REAL", semantic_note="only populated on leg_type='cash' rows"),
        ColumnSpec("currency", "TEXT"),
        ColumnSpec("shares", "REAL", semantic_note="only populated on leg_type='shares' rows"),
        ColumnSpec("price", "REAL"),
        ColumnSpec("fee", "REAL"),
        ColumnSpec("description_full", "TEXT"),
        ColumnSpec("native_id", "TEXT"),
        ColumnSpec("source", "TEXT"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

PAYPAL_TRANSACTIONS_TABLE = TableSpec(
    name="paypal_transactions",
    primary_key_column="paypal_transaction_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="timestamp_end",
    extra_indexed_columns=["tipo", "stato", "impatto_saldo", "codice_riferimento_bancario"],
    columns=[
        ColumnSpec("paypal_transaction_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True,
                    semantic_note="internal only, not meaningful to read directly"),
        ColumnSpec("timestamp_begin", "TEXT",
                    semantic_note="always equal to timestamp_end — PayPal's export has one Data+Orario per row, no separate operation/value date distinction"),
        ColumnSpec("timestamp_end", "TEXT", not_null=True,
                    semantic_note="naive local wall-clock time parsed from the native Data+Orario columns — see fuso_orario for PayPal's own timezone label, not folded into this value (see module docstring's 2026-09-17 UPDATE, TIMEZONE note)"),
        ColumnSpec("fuso_orario", "TEXT", semantic_note="native PayPal timezone abbreviation (e.g. 'CET', 'CEST'), preserved as-is, never converted to a UTC offset"),
        ColumnSpec("tipo", "TEXT", semantic_note="native PayPal transaction type string, Italian (e.g. 'Bonifico bancario sul conto PayPal', 'Pagamento Express Checkout', 'Pagamento preautorizzato utenza') — run a discovery query (SELECT DISTINCT tipo FROM paypal_transactions) before filtering on an exact value you're not certain of"),
        ColumnSpec("stato", "TEXT", not_null=True, semantic_note="native status — exactly one of 'Completata', 'In sospeso' (pending, not yet settled), 'Stornata' (reversed). Every row is included regardless of stato (project owner's explicit decision, 2026-09-17) — filter WHERE stato = 'Completata' for settled-only questions."),
        ColumnSpec("impatto_saldo", "TEXT", semantic_note="native direction-of-money-flow signal — exactly one of 'Addebito' (debit/outflow), 'Accredito' (credit/inflow), 'Promemoria' (a memo/reminder entry, not a real cash movement). This is PayPal's equivalent of money_ingest's amount-sign convention elsewhere in this file — use it instead of guessing from the sign of lordo alone."),
        ColumnSpec("valuta", "TEXT", not_null=True, semantic_note="native currency code — NOT always EUR (real data: EUR/PLN/GBP/USD all present), never auto-converted, same standard as the transactions table's currency column"),
        ColumnSpec("lordo", "REAL", semantic_note="gross amount, signed, native currency (valuta)"),
        ColumnSpec("tariffa", "REAL", semantic_note="PayPal fee, native currency"),
        ColumnSpec("netto", "REAL", semantic_note="net amount = lordo - tariffa, native currency"),
        ColumnSpec("saldo", "REAL", sensitive=True,
                    semantic_note="PayPal account running balance immediately after this transaction, native currency — see module docstring's 2026-09-17 PRIVACY note"),
        ColumnSpec("imposte_sulle_vendite", "REAL", semantic_note="sales tax charged on this transaction; 0.00 for all but 2 of the 263 real rows"),
        ColumnSpec("sconto", "REAL", semantic_note="discount amount applied, when this was a purchase with a merchant-applied discount"),
        ColumnSpec("importo_spedizione_e_imballaggio", "REAL", semantic_note="shipping and handling amount charged, when applicable"),
        ColumnSpec("quantita", "REAL", semantic_note="item quantity, populated for purchase-type rows only"),
        ColumnSpec("nome_controparte", "TEXT", entity_hint="person", semantic_note="counterparty's display name as PayPal recorded it"),
        ColumnSpec("email_mittente", "TEXT"),
        ColumnSpec("email_destinatario", "TEXT"),
        ColumnSpec("stato_controparte", "TEXT", semantic_note="native 'Stato della controparte' — the counterparty's own verification/account status, not this transaction's own stato"),
        ColumnSpec("codice_paese_acquirente", "TEXT", semantic_note="buyer's country code (native 'Codice Paese acquirente')"),
        ColumnSpec("titolo_oggetto", "TEXT", semantic_note="item title, when this transaction relates to a specific purchased item"),
        ColumnSpec("oggetto", "TEXT", semantic_note="free-text subject/description of the transaction"),
        ColumnSpec("messaggio", "TEXT", sensitive=True, semantic_note="free-text message attached to the transaction, when the sender/recipient wrote one — only ~9% of real rows have one"),
        ColumnSpec("indirizzo_spedizione", "TEXT"),
        ColumnSpec("indirizzo_spedizione_continua", "TEXT"),
        ColumnSpec("citta", "TEXT"),
        ColumnSpec("provincia", "TEXT"),
        ColumnSpec("cap", "TEXT", semantic_note="postal code, kept as TEXT (can have a leading zero or letters depending on country)"),
        ColumnSpec("paese", "TEXT"),
        ColumnSpec("telefono", "TEXT", sensitive=True),
        ColumnSpec("prefisso_internazionale", "TEXT"),
        ColumnSpec("metodo_di_pagamento", "TEXT", semantic_note="almost always 'PayPal' in the real data (262/263) — kept for the rare exception, not a useful filter on its own"),
        ColumnSpec("codice_evento_transazione", "TEXT", semantic_note="PayPal's own internal transaction-event code (e.g. 'T0300', 'T0003') — an internal classification, not meant to be human-readable; correlate with tipo instead of matching this directly"),
        ColumnSpec("codice_riferimento_bancario", "TEXT", semantic_note="bank reference number for PayPal<->bank-account transfers — only ~29% of rows have one, but this is the field to JOIN against meinElba/Sella transactions when checking whether a 'Bonifico bancario sul conto PayPal' row (see tipo) duplicates a transfer already captured there (see module docstring's 2026-09-17 UPDATE)"),
        ColumnSpec("stato_revisione_autorizzazione", "TEXT", semantic_note="native authorization-review status, when this transaction went through one"),
        ColumnSpec("codice_transazione_riferimento", "TEXT", semantic_note="native id of a RELATED transaction (e.g. a refund pointing back at the original payment) — not this row's own id, see native_id for that"),
        ColumnSpec("n_ordine_commerciante", "TEXT", semantic_note="merchant order number — see module docstring's 2026-09-17 UPDATE for why this is read from the FIRST of two same-named source columns, not the second"),
        ColumnSpec("numero_personalizzato", "TEXT", semantic_note="a custom reference number, when the sender/merchant set one"),
        ColumnSpec("n_fattura_proforma_originale", "TEXT"),
        ColumnSpec("native_id", "TEXT", not_null=True, semantic_note="native 'Codice transazione' — PayPal's own transaction id, confirmed unique across all real rows"),
        ColumnSpec("source", "TEXT", semantic_note="always 'paypal_csv_export'"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

# Registered at import time (not inside run_ingest()) — same reasoning as
# chessdotcom_ingest.py/spotify_ingest.py: importing this module is enough
# for the bridge to know these tables' columns/semantic notes without
# running an ingest first.
register_table_spec(TRANSACTIONS_TABLE)
register_table_spec(SECURITY_EVENTS_TABLE)
register_table_spec(PRIVATE_MARKET_LEGS_TABLE)
register_table_spec(PAYPAL_TRANSACTIONS_TABLE)


# ============================================================================
# NORMALIZATION — generic utilities
# ============================================================================

def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def safe_float_eu_or_us(value: Any) -> Optional[float]:
    """
    Handles both European (1.234,56 / -11,78) and US (1,234.56) decimal
    formats — meinElba/Sella use a comma as the decimal separator, Trade
    Republic uses a dot. Confirmed against all 3 real files (unchanged
    logic from the old file, still correct).
    """
    raw = normalize_string(value)
    if not raw:
        return None
    raw = raw.replace("€", "").replace("EUR", "").replace("eur", "").strip()
    raw = raw.replace(" ", "")

    if "." in raw and "," in raw:
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


# Known date/time formats. REAL BUG FIX (2026-09-14, see module docstring):
# the meinElba millisecond format is "%d.%m.%Y %H:%M:%S.%f" (dot before
# the fractional seconds) — the regex below normalizes the raw colon
# ("44:653") to a dot ("44.653") BEFORE this list is tried, so the format
# string must expect a dot too. The old file's format string still said
# ":%f", which can never match post-normalization text — verified this
# fix against all 2,449 real meinElba rows (0 failures, down from 2,449).
_DATETIME_FORMATS = [
    "%d.%m.%Y %H:%M:%S.%f",   # meinElba: 25.08.2026 00:55:40:612 -> normalized to a dot below
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%Y-%m-%dT%H:%M:%S.%fZ",  # Trade Republic ISO with microseconds
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
]

_MEINELBA_MS_COLON_RE = re.compile(r"^(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}):(\d+)$")


def parse_flexible_datetime(value: Any) -> Optional[datetime]:
    raw = normalize_string(value)
    if not raw:
        return None

    fixed = raw
    match = _MEINELBA_MS_COLON_RE.match(raw)
    if match:
        fixed = f"{match.group(1)}.{match.group(2)}"

    for fmt in _DATETIME_FORMATS:
        try:
            return datetime.strptime(fixed, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(fixed.replace("Z", "+00:00"))
    except ValueError:
        return None


def to_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def normalize_merchant(raw_text: str) -> Optional[str]:
    if not raw_text:
        return None
    lowered = raw_text.lower()
    for pattern, canonical in MERCHANT_NORMALIZATION_RULES:
        if re.search(pattern, lowered):
            return canonical
    return None


def redact_iban_labels(text: Optional[str]) -> Optional[str]:
    """See CONFIG — IBAN redaction above. Applies both the label-anchored
    and the general length-based pattern, in that order (the label-
    anchored one produces a more readable "IBAN: [redacted]" for the
    common labeled case; the general one is the safety net for
    unlabeled embeddings like Trade Republic's)."""
    if not text:
        return text
    text = _IBAN_LABEL_RE.sub("IBAN: [redacted]", text)
    text = _IBAN_GENERAL_RE.sub("[IBAN redacted]", text)
    return text


def extract_isin(description: str) -> Optional[str]:
    if not description:
        return None
    match = ISIN_PATTERN.search(description)
    return match.group(1) if match else None


def resolve_institution_label(source: str, file_name: str) -> str:
    return INSTITUTION_LABELS.get(source, f"Unrecognized bank (file: {file_name})")


def sanitize_source_file(file_name: str) -> str:
    """
    REAL-DATA FINDING (2026-09-14, found by auditing the test vault.db for
    the user's own IBAN, not by inspection): the meinElba export's own
    FILENAME embeds the account IBAN
    ("meinElba_transactions_AT913200000013275029_search.csv"), so storing
    source_file verbatim leaked it into all 2,449 transaction rows even
    though description_full/counterparty_iban were already handled. The
    general (unlabeled) IBAN pattern is safe to apply here specifically
    because a filename has none of the free-text merchant-reference-code
    false-positive risk that ruled it out for counterparty_name (see
    module docstring).
    """
    return redact_iban_labels(file_name) or file_name


# ============================================================================
# PARSING — file reading
# ============================================================================

def read_text_with_fallback_encoding(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    raise RuntimeError(f"Could not read {path} with any known encoding.")


def collect_input_files(input_dir: Path) -> List[Path]:
    # REAL-DATA FIX (2026-09-14): rglob("*.csv") is case-SENSITIVE on
    # Linux (the Raspberry Pi this actually runs on), so it silently
    # missed all 8 real PayPal export files found in Input/Money/paypal/
    # (they arrive as "Download.CSV", "Download (1).CSV", ... - uppercase
    # extension). Matched case-insensitively here instead. This does NOT
    # turn on PayPal ingestion (that integration is explicitly deferred,
    # see module docstring's 2026-09-14 UPDATE note below) -
    # detect_source_type() still returns "generic_bank_csv_export" for
    # PayPal's header and there is no parser for it yet, so these files
    # go from being invisible to being discovered-but-skipped-with-a-
    # warning, which is the honest state until PayPal is actually built.
    if not input_dir.exists():
        return []
    return sorted(
        p for p in input_dir.rglob("*")
        if p.is_file() and p.suffix.lower() == ".csv"
    )


def detect_source_type(header: List[str], has_header: bool) -> str:
    if not has_header:
        return "meinelba_csv_export"

    lower_header = {h.strip().lower() for h in header}

    trade_republic_signature = {"shares", "fee", "tax", "transaction_id", "asset_class"}
    if len(trade_republic_signature & lower_header) >= 3:
        return "traderepublic_csv_export"

    sella_signature = {"divisa", "importo", "codice identificativo", "categoria"}
    if len(sella_signature & lower_header) >= 2:
        return "sella_csv_export"

    # Added 2026-09-17, PayPal migration. Distinct Italian-language column
    # set, no overlap with the Sella/Trade Republic signatures above.
    paypal_signature = {"codice transazione", "lordo", "netto", "tariffa", "impatto sul saldo"}
    if len(paypal_signature & lower_header) >= 3:
        return "paypal_csv_export"

    return "generic_bank_csv_export"


def sniff_csv_dialect_and_header(raw_text: str) -> Tuple[str, List[str], bool]:
    import csv
    import io

    sample = raw_text[:4000]
    candidates = [";", ",", "\t", "|"]
    delimiter = max(candidates, key=lambda d: sample.count(d))

    first_line = raw_text.splitlines()[0] if raw_text.splitlines() else ""
    first_cell = first_line.split(delimiter)[0].strip().strip('"')

    looks_like_date = bool(re.match(r"^\d{2}\.\d{2}\.\d{4}$", first_cell))
    has_header = not looks_like_date

    header: List[str] = []
    if has_header:
        try:
            reader = csv.reader(io.StringIO(first_line), delimiter=delimiter, quotechar='"')
            header = [clean_whitespace(h) for h in next(reader)]
        except Exception:
            header = []

    return delimiter, header, has_header


# ============================================================================
# PARSING — meinElba (positional, no header)
# ============================================================================

def parse_meinelba_description(raw_desc: str) -> Dict[str, str]:
    result = {"counterparty_name": "", "counterparty_iban": "", "payment_reference": ""}

    for label in ("Payment recipient:", "Recipient:"):
        if label in raw_desc:
            after = raw_desc.split(label, 1)[1]
            result["counterparty_name"] = after.split(";", 1)[0].split(" IBAN:")[0].strip()
            break

    iban_match = re.search(r"IBAN:\s*([A-Z0-9]{10,34})", raw_desc)
    if iban_match:
        result["counterparty_iban"] = iban_match.group(1)  # extracted for parsing only — never stored, see module docstring

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
    Positional parser, headerless CSV, ';' delimiter, 6 columns:
    0 operation date, 1 description, 2 value date, 3 amount, 4 currency,
    5 full timestamp. Confirmed against all 2,449 real rows: consistent
    6-column shape throughout, no header, always EUR.
    """
    import csv
    import io

    transactions: List[Dict[str, Any]] = []
    reader = csv.reader(io.StringIO(raw_text), delimiter=";", quotechar='"')

    for idx, row in enumerate(reader):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) < 6:
            continue

        raw_date, raw_desc, raw_value_date, raw_amount, raw_currency, raw_full_ts = row[:6]

        dt_full = parse_flexible_datetime(raw_full_ts) or parse_flexible_datetime(raw_date)
        dt_value = parse_flexible_datetime(raw_value_date)
        amount = safe_float_eu_or_us(raw_amount)
        currency = normalize_string(raw_currency).upper() or "EUR"
        desc_clean = clean_whitespace(raw_desc)
        extracted = parse_meinelba_description(desc_clean)

        counterparty_name = extracted["counterparty_name"] or None
        merchant = normalize_merchant(counterparty_name or desc_clean)
        isin = extract_isin(desc_clean)

        transactions.append({
            "domain": "bank",
            "source": "meinelba_csv_export",
            "account_ref": "meinelba_checking",
            "timestamp_begin": to_iso(dt_full),
            "timestamp_end": to_iso(dt_value) or to_iso(dt_full),
            "amount": amount,
            "currency": currency,
            "description_full": redact_iban_labels(desc_clean),
            "counterparty_name": counterparty_name,
            "merchant": merchant,
            "category_raw": None,  # meinElba provides no native category
            "native_type": None,
            "isin": isin,
            "instrument_name": None,
            "shares": None, "unit_price": None, "fee": None, "tax": None,
            "original_amount": None, "original_currency": None, "fx_rate": None,
            "native_id": None,  # meinElba provides no native row id
            "source_file": file_name,
            "record_index_in_source": idx,
            "_dedup_composite": (to_iso(dt_full) or "", str(amount), desc_clean[:80].lower()),
        })

    return transactions


# ============================================================================
# PARSING — Banca Sella
# ============================================================================

def parse_sella_file(raw_text: str, delimiter: str, file_name: str) -> List[Dict[str, Any]]:
    """
    DictReader by real header. REAL-DATA FIX (2026-09-14): the raw export
    has a trailing running-balance footer row ("Saldo al ...", 6 columns
    instead of the header's 11) and can have a fully blank line. DictReader
    pads a short row with None for missing fieldnames rather than shrinking
    the key count, so filtering on len(row) doesn't work — instead this
    relies on a genuine transaction row always having BOTH a parseable
    amount AND a native id, which the footer row has neither of (its 6
    values land on the wrong fieldnames entirely — "Divisa" ends up holding
    the balance figure, "Importo" ends up empty). Verified: 358 usable rows
    out of 360 raw lines.
    """
    import csv
    import io

    transactions: List[Dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')

    for idx, row in enumerate(reader):
        if not row or not any(normalize_string(v) for v in row.values()):
            continue

        native_id = normalize_string(row.get("Codice identificativo")) or None
        raw_date = normalize_string(row.get("Data operazione"))
        raw_value_date = normalize_string(row.get("Data valuta"))
        description = clean_whitespace(normalize_string(row.get("Descrizione")))
        currency = normalize_string(row.get("Divisa")).upper()
        amount = safe_float_eu_or_us(row.get("Importo"))
        native_category = normalize_string(row.get("Categoria"))
        native_subcategory = normalize_string(row.get("Sottocategoria"))

        # A genuine transaction row always has a currency and a parseable
        # amount; the footer/blank lines don't — belt-and-braces on top
        # of the column-count filter above.
        if not currency or amount is None or not native_id:
            continue

        dt = parse_flexible_datetime(raw_date) or parse_flexible_datetime(raw_value_date)
        dt_value = parse_flexible_datetime(raw_value_date)

        isin = extract_isin(description)
        merchant = normalize_merchant(description)

        category_raw_combined = " / ".join(
            p for p in (native_category, native_subcategory) if p and p != "-"
        ) or None

        transactions.append({
            "domain": "bank",
            "source": "sella_csv_export",
            "account_ref": "sella_conto",
            "timestamp_begin": to_iso(dt),
            "timestamp_end": to_iso(dt_value) or to_iso(dt),
            "amount": amount,
            "currency": currency,
            "description_full": redact_iban_labels(description),
            "counterparty_name": None,  # Sella provides no structured counterparty field
            "merchant": merchant,
            "category_raw": category_raw_combined,
            "native_type": native_category or None,
            "isin": isin,
            "instrument_name": None,
            "shares": None, "unit_price": None, "fee": None, "tax": None,
            "original_amount": None, "original_currency": None, "fx_rate": None,
            "native_id": native_id,
            "source_file": file_name,
            "record_index_in_source": idx,
            "_dedup_native_sign": (native_id, "+" if amount >= 0 else "-"),
        })

    return transactions


# ============================================================================
# PARSING — Trade Republic (routes into 3 different tables)
# ============================================================================

def parse_traderepublic_file(raw_text: str, delimiter: str, file_name: str) -> Tuple[
    List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]
]:
    """
    Returns (transaction_rows, security_event_rows, private_market_leg_rows)
    — see route_traderepublic_row for the routing rule, derived from real
    data (asset_class/category, not a guess). transaction_id is native and
    confirmed unique across the ENTIRE real file (441/441), so it is used
    directly as the dedup key for all three destination tables.
    """
    import csv
    import io

    transaction_rows: List[Dict[str, Any]] = []
    security_event_rows: List[Dict[str, Any]] = []
    private_market_leg_rows: List[Dict[str, Any]] = []

    reader = csv.DictReader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')

    for idx, row in enumerate(reader):
        if not row or not any(normalize_string(v) for v in row.values()):
            continue

        native_type_original = normalize_string(row.get("type"))
        native_type = native_type_original.lower()
        native_category = normalize_string(row.get("category"))
        asset_class = normalize_string(row.get("asset_class"))
        name = normalize_string(row.get("name")) or None
        symbol = normalize_string(row.get("symbol")) or None
        shares = safe_float_eu_or_us(row.get("shares"))
        price = safe_float_eu_or_us(row.get("price"))
        amount = safe_float_eu_or_us(row.get("amount"))
        fee = safe_float_eu_or_us(row.get("fee"))
        tax = safe_float_eu_or_us(row.get("tax"))
        currency = normalize_string(row.get("currency")).upper() or None
        original_amount = safe_float_eu_or_us(row.get("original_amount"))
        original_currency = normalize_string(row.get("original_currency")).upper() or None
        fx_rate = safe_float_eu_or_us(row.get("fx_rate"))
        description = clean_whitespace(normalize_string(row.get("description")))
        native_id = normalize_string(row.get("transaction_id")) or None

        dt = parse_flexible_datetime(row.get("datetime")) or parse_flexible_datetime(row.get("date"))
        ts = to_iso(dt)

        route = route_traderepublic_row(native_category, asset_class)

        if route == "private_market_leg":
            leg_type = "shares" if native_category == "TRADING" else "cash"
            private_market_leg_rows.append({
                "timestamp_begin": ts,
                "timestamp_end": ts,
                "leg_type": leg_type,
                "isin": symbol,
                "instrument_name": name,
                "amount": amount,
                "currency": currency,
                "shares": shares,
                "price": price,
                "fee": fee,
                "description_full": redact_iban_labels(description),
                "native_id": native_id,
                "source": "traderepublic_csv_export",
                "source_file": file_name,
                "dedup_key": f"traderepublic_csv_export||{native_id}",
            })
            continue

        if route == "security_event":
            security_event_rows.append({
                "timestamp_begin": ts,
                "timestamp_end": ts,
                "event_type": native_type or "unknown",
                "category_raw": native_category or None,
                "isin": symbol,
                "instrument_name": name,
                "shares_delta": shares,
                "price": price,
                "native_id": native_id,
                "source": "traderepublic_csv_export",
                "source_file": file_name,
                "dedup_key": f"traderepublic_csv_export||{native_id}",
            })
            continue

        # route == "transaction"
        transaction_type, category = TRADE_REPUBLIC_TYPE_MAP.get(native_type, (None, None))
        merchant = normalize_merchant(name or description)

        # REAL-DATA FIX (2026-09-14): TRADE_REPUBLIC_TYPE_MAP maps both
        # "buy" and "sell" to the IDENTICAL (transaction_type, category)
        # pair -> ("investment", "investment") — so those two columns
        # alone can never distinguish a purchase from a sale (confirmed:
        # 199 real BUY rows + 105 real SELL rows, all landing as
        # transaction_type="investment"/category="investment"). The old
        # cleanup step in run_ingest() discarded the native type string
        # entirely once category was set. Fixed by folding the ORIGINAL-
        # CASE native type into category_raw here (native_category was
        # already being preserved alone; now it's "CATEGORY / TYPE", e.g.
        # "TRADING / BUY" vs "TRADING / SELL") — project owner's explicit
        # decision (2026-09-14 chat): preserve the native type in a
        # column rather than only documenting the sign-based workaround.
        # shares' sign (positive=buy, negative=sell) is also a reliable
        # real-data signal for the same distinction, kept as a secondary
        # hint in the shares ColumnSpec's semantic_note.
        category_raw_combined = " / ".join(
            p for p in (native_category, native_type_original) if p
        ) or None

        transaction_rows.append({
            "domain": "investment",
            "source": "traderepublic_csv_export",
            "account_ref": "traderepublic_default",
            "timestamp_begin": ts,
            "timestamp_end": ts,
            "amount": amount,
            "currency": currency or "EUR",
            "description_full": redact_iban_labels(description),
            "counterparty_name": normalize_string(row.get("counterparty_name")) or None,
            "merchant": merchant,
            "category_raw": category_raw_combined,
            "native_type": native_type or None,
            "_native_transaction_type": transaction_type,
            "_native_category": category,
            "isin": symbol,
            "instrument_name": name,
            "shares": shares, "unit_price": price, "fee": fee, "tax": tax,
            "original_amount": original_amount, "original_currency": original_currency, "fx_rate": fx_rate,
            "native_id": native_id,
            "source_file": file_name,
            "record_index_in_source": idx,
            "_dedup_native_id": native_id,
        })

    return transaction_rows, security_event_rows, private_market_leg_rows


# ============================================================================
# PARSING — PayPal (own table, see module docstring's 2026-09-17 UPDATE)
# ============================================================================

# Output field name -> exact source header name. Looked up via
# header.index(name), which returns the FIRST matching column — this is
# what makes "n_ordine_commerciante" safely resolve to index 31 rather
# than the near-empty duplicate at index 62 (see module docstring; do
# NOT rewrite this parser to use csv.DictReader, which would silently
# invert that choice).
_PAYPAL_FIELD_MAP: Dict[str, str] = {
    "data": "Data",
    "orario": "Orario",
    "fuso_orario": "Fuso orario",
    "nome_controparte": "Nome",
    "tipo": "Tipo",
    "stato": "Stato",
    "valuta": "Valuta",
    "lordo": "Lordo",
    "tariffa": "Tariffa",
    "netto": "Netto",
    "email_mittente": "Indirizzo email mittente",
    "email_destinatario": "Indirizzo email destinatario",
    "native_id": "Codice transazione",
    "stato_controparte": "Stato della controparte",
    "stato_indirizzo": "Stato dell'indirizzo",
    "titolo_oggetto": "Titolo oggetto",
    "importo_spedizione_e_imballaggio": "Importo spese di spedizione e imballaggio",
    "imposte_sulle_vendite": "Imposte sulle vendite",
    "codice_transazione_riferimento": "Codice transazione di riferimento",
    "n_ordine_commerciante": "N° ordine commerciante",
    "numero_personalizzato": "Numero personalizzato",
    "quantita": "Quantità",
    "saldo": "Saldo",
    "indirizzo_spedizione": "Indirizzo",
    "indirizzo_spedizione_continua": "Indirizzo (continua)",
    "citta": "Città",
    "provincia": "Provincia",
    "cap": "CAP/Codice postale",
    "paese": "Paese",
    "telefono": "Telefono",
    "oggetto": "Oggetto",
    "messaggio": "Messaggio",
    "metodo_di_pagamento": "Metodo di pagamento",
    "codice_evento_transazione": "Codice evento transazione",
    "codice_riferimento_bancario": "Codice di riferimento bancario",
    "codice_paese_acquirente": "Codice Paese acquirente",
    "stato_revisione_autorizzazione": "Stato revisione autorizzazione",
    "prefisso_internazionale": "Prefisso internazionale",
    "impatto_saldo": "Impatto sul saldo",
    "sconto": "Sconto",
    "n_fattura_proforma_originale": "N. fattura pro-forma originale",
}

_PAYPAL_TEXT_FIELDS = {
    k for k in _PAYPAL_FIELD_MAP
    if k not in (
        "lordo", "tariffa", "netto", "imposte_sulle_vendite", "quantita",
        "saldo", "sconto", "importo_spedizione_e_imballaggio",
    )
}


def parse_paypal_file(raw_text: str, delimiter: str, file_name: str) -> List[Dict[str, Any]]:
    """
    Reads by column INDEX (header.index(name)), not csv.DictReader — see
    module docstring's 2026-09-17 UPDATE for why (the duplicate "N° ordine
    commerciante" column). Header-only files (6 of the 8 real exports)
    naturally produce zero rows here, no special-casing needed. A genuine
    transaction row always has both a native_id and a stato; used as a
    belt-and-braces filter the same way Sella's parser checks for a
    native_id + amount before treating a row as real.
    """
    import csv
    import io

    reader = csv.reader(io.StringIO(raw_text), delimiter=delimiter, quotechar='"')
    rows = list(reader)
    if not rows:
        return []

    header = [clean_whitespace(h) for h in rows[0]]

    field_indices: Dict[str, Optional[int]] = {}
    for out_name, source_name in _PAYPAL_FIELD_MAP.items():
        try:
            field_indices[out_name] = header.index(source_name)
        except ValueError:
            field_indices[out_name] = None  # column not present in this export — honestly absent, not guessed

    def cell(row: List[str], out_name: str) -> str:
        idx = field_indices.get(out_name)
        if idx is None or idx >= len(row):
            return ""
        return normalize_string(row[idx])

    transactions: List[Dict[str, Any]] = []

    for row_idx, row in enumerate(rows[1:]):
        if not row or all(not c.strip() for c in row):
            continue

        native_id = cell(row, "native_id") or None
        stato = cell(row, "stato") or None
        if not native_id or not stato:
            continue  # not a genuine transaction row

        raw_date = cell(row, "data")
        raw_time = cell(row, "orario")
        dt = parse_flexible_datetime(f"{raw_date} {raw_time}".strip()) or parse_flexible_datetime(raw_date)
        ts = to_iso(dt)

        record: Dict[str, Any] = {
            "timestamp_begin": ts,
            "timestamp_end": ts,
            "native_id": native_id,
            "stato": stato,
            "dedup_key": f"paypal_csv_export||{native_id}",
            "source": "paypal_csv_export",
            "source_file": file_name,
        }

        for out_name in _PAYPAL_FIELD_MAP:
            if out_name in ("data", "orario", "native_id", "stato"):
                continue  # already consumed above
            raw_value = cell(row, out_name)
            if out_name in _PAYPAL_TEXT_FIELDS:
                record[out_name] = clean_whitespace(raw_value) or None
            else:
                record[out_name] = safe_float_eu_or_us(raw_value)

        transactions.append(record)

    return transactions


def route_traderepublic_row(native_category: str, asset_class: str) -> str:
    """
    Routing rule, derived from real data (2026-09-14 inspection), not
    assumed: asset_class="PRIVATE_FUND" -> private_market_leg (covers
    both the CASH/PRIVATE_MARKET_BUY cash leg and the TRADING/BUY shares
    leg); category in (CORPORATE_ACTION, DELIVERY) -> security_event
    (covers WARRANT_EXERCISE/REVERSE_SPLIT/SPLIT/MIGRATION); everything
    else -> transaction. Note: one real BONUS row's free text mentions
    "Private Markets" but its asset_class is blank — per the project
    owner's explicit decision, it is NOT routed here (stays a plain
    transaction) because there is no structural signal, only text.
    """
    if asset_class == "PRIVATE_FUND":
        return "private_market_leg"
    if native_category in ("CORPORATE_ACTION", "DELIVERY"):
        return "security_event"
    return "transaction"


# ============================================================================
# CLASSIFICATION — transaction_type + category (transactions table only)
# ============================================================================

def classify_transaction(txn: Dict[str, Any]) -> Tuple[str, str]:
    """
    Priority: 1) explicit native signal (Trade Republic type map, Sella
    native category), 2) amount sign, 3) high-confidence keywords for
    transaction_type only (never category), 4) unknown. category stays
    "unknown" whenever the source provides no explicit native signal —
    never guessed from generic keywords (timelive.md §3).
    """
    native_type_for_domain = txn.get("_native_transaction_type")
    native_category_for_domain = txn.get("_native_category")
    if native_type_for_domain is not None:
        return native_type_for_domain, native_category_for_domain or "unknown"

    category_raw = txn.get("category_raw")
    amount = txn.get("amount")
    description = (txn.get("description_full") or "").lower()

    if category_raw and txn.get("source") == "sella_csv_export":
        top_level = category_raw.split(" / ")[0].strip().lower()
        mapped = CATEGORY_NATIVE_MAP_SELLA.get(top_level)
        if mapped:
            if mapped == "financial_fees":
                base_type = "fee"
            elif mapped == "dividends_interest":
                base_type = "income"
            elif mapped == "other_income":
                base_type = "income"
            else:
                base_type = "income" if (amount is not None and amount > 0) else "expense"
            return base_type, mapped

    if amount is None:
        base_type = "unknown"
    elif amount > 0:
        base_type = "income"
    elif amount < 0:
        base_type = "expense"
    else:
        base_type = "unknown"

    if ACTIVITY_INFERENCE_LEVEL in ("balanced", "aggressive"):
        if any(k in description for k in _KEYWORDS_CASH_WITHDRAWAL):
            base_type = "cash_withdrawal"
        elif any(k in description for k in _KEYWORDS_SALARY):
            base_type = "income"
        elif any(k in description for k in _KEYWORDS_FEE):
            base_type = "fee"

    return base_type, "unknown"


# ============================================================================
# DEDUPLICATION — per-source key computation (see module docstring for
# the real-data findings behind each choice)
# ============================================================================

def compute_transaction_dedup_key(txn: Dict[str, Any]) -> str:
    source = txn["source"]
    if source == "meinelba_csv_export":
        ts, amount, desc_prefix = txn["_dedup_composite"]
        return "|".join(["meinelba", ts, amount, desc_prefix])
    if source == "sella_csv_export":
        native_id, sign = txn["_dedup_native_sign"]
        return f"sella||{native_id}||{sign}"
    if source == "traderepublic_csv_export":
        return f"traderepublic||{txn['_dedup_native_id']}"
    # generic fallback — composite of what's available
    return "|".join([
        source,
        normalize_string(txn.get("account_ref")),
        normalize_string(txn.get("timestamp_begin")),
        normalize_string(txn.get("amount")),
        normalize_string(txn.get("currency")),
        normalize_string(txn.get("description_full"))[:80].lower(),
    ])


# ============================================================================
# ANOMALY DETECTION (transactions table only, unchanged formula)
# ============================================================================

def flag_unusual_transactions(transactions: List[Dict[str, Any]]) -> None:
    groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for txn in transactions:
        if txn.get("amount") is None:
            continue
        key = (txn.get("category", "unknown"), txn.get("currency"), txn.get("domain"))
        groups[key].append(txn)

    for _, group_txns in groups.items():
        if len(group_txns) < ANOMALY_MIN_SAMPLES:
            for txn in group_txns:
                txn["is_unusual"] = 0
            continue

        amounts = [abs(t["amount"]) for t in group_txns]
        mean = statistics.mean(amounts)
        stdev = statistics.pstdev(amounts)
        for txn in group_txns:
            if stdev == 0:
                txn["is_unusual"] = 0
                continue
            z = (abs(txn["amount"]) - mean) / stdev
            txn["is_unusual"] = 1 if z > ANOMALY_ZSCORE_THRESHOLD else 0


# ============================================================================
# NOTABILITY — transactions table only
# ============================================================================

def _compute_amount_percentiles(transactions: List[Dict[str, Any]]) -> None:
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for txn in transactions:
        if txn.get("amount") is not None:
            groups[(txn["currency"], txn["domain"])].append(txn)

    for _, group_txns in groups.items():
        amounts_sorted = sorted(abs(t["amount"]) for t in group_txns)
        n = len(amounts_sorted)
        rank_of_amount: Dict[float, int] = {}
        for idx, amount in enumerate(amounts_sorted):
            if amount not in rank_of_amount:
                rank_of_amount[amount] = idx
        for txn in group_txns:
            rank = rank_of_amount[abs(txn["amount"])]
            txn["_amount_percentile"] = rank / max(n - 1, 1)


def apply_transaction_notability(transactions: List[Dict[str, Any]]) -> None:
    _compute_amount_percentiles(transactions)
    compute_notability_scores(
        transactions,
        NotabilityConfig(
            weight_functions={
                "amount": lambda t: t.get("_amount_percentile", 0.0),
                "recency": lambda t: recency_weight(t.get("timestamp_begin"), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS),
                "anomaly_bonus": lambda t: 1.0 if t.get("is_unusual") else 0.0,
            },
            weights={
                "amount": NOTABILITY_WEIGHT_AMOUNT,
                "recency": NOTABILITY_WEIGHT_RECENCY,
                "anomaly_bonus": NOTABILITY_WEIGHT_ANOMALY_BONUS,
            },
        ),
    )
    for txn in transactions:
        txn.pop("_amount_percentile", None)


# ============================================================================
# MAIN ENTRYPOINT — the contract ingest_engine.py's CLI expects
# ============================================================================

def run_ingest(conn, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    """
    1. create schema for all 3 tables (no FK relationships between them —
       see module docstring: the tables are independent, linked only by
       isin/timestamp proximity a query can join on if it wants to)
    2. read every *.csv in MONEY_INPUT_DIR, detect source, parse — Trade
       Republic's parser returns rows for all 3 destination tables at once
    3. classify transaction_type/category for the transactions table
    4. compute dedup keys, flag anomalies, compute notability
    5. upsert all 3 tables (stable ids across re-ingests)
    """
    create_schema_for_table(conn, TRANSACTIONS_TABLE)
    create_schema_for_table(conn, SECURITY_EVENTS_TABLE)
    create_schema_for_table(conn, PRIVATE_MARKET_LEGS_TABLE)
    create_schema_for_table(conn, PAYPAL_TRANSACTIONS_TABLE)

    input_files = collect_input_files(MONEY_INPUT_DIR)
    logger.info("found %d .csv file(s) in %s", len(input_files), MONEY_INPUT_DIR)

    all_transactions: List[Dict[str, Any]] = []
    all_security_events: List[Dict[str, Any]] = []
    all_private_market_legs: List[Dict[str, Any]] = []
    all_paypal_transactions: List[Dict[str, Any]] = []
    error_count = 0

    for file_path in input_files:
        try:
            raw_text = read_text_with_fallback_encoding(file_path)
            delimiter, header, has_header = sniff_csv_dialect_and_header(raw_text)
            source_type = detect_source_type(header, has_header)
            # See sanitize_source_file() docstring — the meinElba filename
            # itself embeds the account IBAN.
            safe_file_name = sanitize_source_file(file_path.name)

            if source_type == "meinelba_csv_export":
                txns = parse_meinelba_file(raw_text, safe_file_name)
                all_transactions.extend(txns)
            elif source_type == "sella_csv_export":
                txns = parse_sella_file(raw_text, delimiter, safe_file_name)
                all_transactions.extend(txns)
            elif source_type == "traderepublic_csv_export":
                txns, events, legs = parse_traderepublic_file(raw_text, delimiter, safe_file_name)
                all_transactions.extend(txns)
                all_security_events.extend(events)
                all_private_market_legs.extend(legs)
            elif source_type == "paypal_csv_export":
                all_paypal_transactions.extend(parse_paypal_file(raw_text, delimiter, safe_file_name))
            else:
                logger.warning("%s: unrecognized bank CSV format, skipped (no generic fallback parser wired up yet for this domain)", safe_file_name)

        except Exception as exc:
            error_count += 1
            logger.warning("%s: file read/parse error: %s", file_path.name, exc)

    if error_count:
        logger.warning("%d file(s) skipped due to errors — see warnings above", error_count)

    for txn in all_transactions:
        txn["institution"] = resolve_institution_label(txn["source"], txn["source_file"])
        transaction_type, category = classify_transaction(txn)
        txn["transaction_type"] = transaction_type
        txn["category"] = category
        txn["dedup_key"] = compute_transaction_dedup_key(txn)
        for internal_key in ("_dedup_composite", "_dedup_native_sign", "_dedup_native_id",
                              "_native_transaction_type", "_native_category", "native_type",
                              "record_index_in_source"):
            txn.pop(internal_key, None)

    all_transactions.sort(key=lambda t: (t.get("timestamp_end") or "", t.get("source_file") or ""))
    flag_unusual_transactions(all_transactions)
    apply_transaction_notability(all_transactions)

    logger.info(
        "%d transaction(s), %d security event(s), %d private-market leg(s), %d PayPal transaction(s) parsed",
        len(all_transactions), len(all_security_events), len(all_private_market_legs), len(all_paypal_transactions),
    )

    transaction_outcomes: List[UpsertOutcome] = upsert_rows(conn, TRANSACTIONS_TABLE, all_transactions)
    security_event_outcomes: List[UpsertOutcome] = upsert_rows(conn, SECURITY_EVENTS_TABLE, all_security_events)
    private_market_leg_outcomes: List[UpsertOutcome] = upsert_rows(conn, PRIVATE_MARKET_LEGS_TABLE, all_private_market_legs)
    paypal_outcomes: List[UpsertOutcome] = upsert_rows(conn, PAYPAL_TRANSACTIONS_TABLE, all_paypal_transactions)

    all_outcomes = transaction_outcomes + security_event_outcomes + private_market_leg_outcomes + paypal_outcomes
    rows_inserted = sum(1 for o in all_outcomes if o.was_new)
    rows_already_present = sum(1 for o in all_outcomes if not o.was_new)

    return IngestReport(
        domain="money",
        tables_written=["transactions", "security_events", "private_market_legs", "paypal_transactions"],
        rows_inserted=rows_inserted,
        rows_already_present=rows_already_present,
        dry_run=dry_run,
    )