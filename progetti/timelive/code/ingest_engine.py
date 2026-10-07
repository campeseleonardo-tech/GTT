# ingest_engine.py
# =============================================================================
# PERSONAL DATA VAULT — SHARED INGEST ENGINE (replaces main.py)
# =============================================================================
#
# SCOPE OF THIS FILE (timelive.md §5)
# -----------------------------------------------------------------------
# This module owns everything that used to be duplicated per domain:
#   * SQLite schema creation from a domain's declarative TableSpec
#   * notability_score computation (generic weighted-sum + recency, same
#     algorithm as the old main.py, unchanged)
#   * deduplication with a STABLE primary key across re-ingests (see
#     upsert_rows() below — this is a deliberate behavioural change from
#     the old deduplicate_records(), not just a port; see its docstring)
#   * session/grouping helper (group_into_sessions) for domains that need
#     it, generalised to a per-pair gap function instead of one fixed
#     constant (chess.com's gap depends on the *next* game's time control;
#     spotify's does not — both fit this one function)
#   * table-description generation for the future bridge tool
#     describe_table() (timelive.md §6) — the DATA this needs (columns,
#     types, semantic notes) is produced here, from the schema itself;
#     wiring it into an actual bridge tool is task 4, not this file
#   * the CLI entrypoint: choose which domain(s) to ingest, verbose/debug
#     output, --dry-run
#
# WHAT STAYS OUT OF THIS FILE, ON PURPOSE (timelive.md §3)
# -----------------------------------------------------------------------
#   * parse_raw() — always domain code, lives in <domain>_ingest.py
#   * classification logic with real domain semantics (win_method,
#     category rules, ISIN extraction, ...) — domain code
#   * the READ-ONLY guardrails for querying vault.db (no INSERT/UPDATE/
#     DELETE/DROP, row limit, timeout) — that is llm_bridge.py's job
#     (timelive.md §6). This file only ever opens vault.db read-write,
#     because ingest is the one legitimate writer.
#
# STATUS (2026-09-15): chess.com was the pilot migration, spotify the
# second, money the third (bank + public-market investments + private
# markets), instagram the fourth (posts/comments/likes/follows/DMs/login
# activity — see instagram_ingest.py). All four are registered in
# DOMAIN_REGISTRY below. _PLANNED_DOMAINS still lists every domain in
# original roadmap order (including the already-migrated ones) — it is
# only consulted for domains NOT in DOMAIN_REGISTRY, to give an honest
# "not yet" error instead of a bare KeyError; see the bottom of this file
# for the remaining domains still on the old JSON system.
#
# CHANGE (2026-09-14, spotify migration): added TableSpec.extra_indexed_
# columns — see its docstring. Needed because spotify's ~358k rows is the
# first domain where an un-indexed filter (e.g. WHERE artist_name = ...)
# would mean a full table scan on every such query; chess.com's ~1.8k
# rows never made this visible. Purely additive: any existing TableSpec
# that doesn't set it keeps exactly its old indexing behaviour.
#
# money migration (2026-09-14, same session): no engine change was
# needed — money_ingest.py's 3-table design (transactions/
# security_events/private_market_legs, no FKs between them) fits the
# existing primitives (TableSpec/upsert_rows/compute_notability_scores)
# without modification. Only this registry (below) and _PLANNED_DOMAINS
# changed. "bank" in the old roadmap list is renamed to "money" here —
# the domain now covers more than banking (see money_ingest.py's module
# docstring for why: private markets turned out to live inside the
# Trade Republic export, not a separate source).
#
# instagram migration (2026-09-15, this session): two small additive
# changes, both cross-cutting requests from the project owner made while
# scoping instagram_ingest.py, not instagram-specific:
#   * ColumnSpec.sensitive — see its docstring. A marker, not an access
#     control: the project owner's own words were "readable is fine as
#     long as it's only mine; it only needs encrypting if an external
#     party ends up touching the data" — so this only records WHICH
#     columns would need that treatment later, no cifratura implemented
#     now. Not retrofitted onto chess.com/spotify/money's existing
#     TableSpecs (no real need yet, and those are validated/stable —
#     same "don't touch what's working without cause" reasoning as
#     everywhere else in this file's history).
#   * register_table_spec() now rejects a duplicate table name outright,
#     instead of silently overwriting. timelive.md §3 already flags that
#     small local models confuse table names across domains once several
#     share one schema (chess.com vs spotify, both directions) — this
#     doesn't fix that (it's a query-time model-capability issue, see
#     timelive.md §6), but it does turn an actual accidental name clash
#     between two domains' TableSpecs into a loud error at import time
#     instead of one domain's schema silently shadowing another's.
#   * truncate_text() — a generic helper, added because instagram_ingest
#     needed it for its direct-message sampling (full text for the 20
#     busiest threads, first N chars for the rest) and the project owner
#     asked to centralize it now rather than let it become
#     instagram-specific. The "pick the N busiest groups" selection logic
#     itself stays in instagram_ingest.py — no second domain needs it yet
#     (WhatsApp isn't migrated), so it isn't generalized here on
#     spec — same reasoning as extra_indexed_columns above: centralize
#     when a second real case shows up, not preemptively.
# =============================================================================

from __future__ import annotations

import argparse
import importlib
import logging
import math
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    from config import BASE_DIR, OUTPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    OUTPUT_DIR = BASE_DIR / "Output"

# Single shared database file for every domain (timelive.md §2). Not
# read from config.json today — adding VAULT_DB_PATH there is a small,
# separate change (config.py's own docstring says paths live in
# config.json; this follows the same try/except fallback pattern used
# everywhere else in this project so it doesn't hard-depend on that
# change happening first).
try:
    from config import VAULT_DB_PATH  # type: ignore
except Exception:
    VAULT_DB_PATH = OUTPUT_DIR / "vault.db"
VAULT_DB_PATH = Path(VAULT_DB_PATH)


logger = logging.getLogger("ingest_engine")


# =============================================================================
# CONFIDENCE RATE — unchanged from main.py (timelive.md §4's fixed scale)
# =============================================================================

CONFIDENCE_NATIVE = 1.0
CONFIDENCE_INFERRED_HIGH = 0.8
CONFIDENCE_INFERRED_MEDIUM = 0.5
CONFIDENCE_INFERRED_LOW = 0.2

_VALID_CONFIDENCE_VALUES = {
    CONFIDENCE_NATIVE,
    CONFIDENCE_INFERRED_HIGH,
    CONFIDENCE_INFERRED_MEDIUM,
    CONFIDENCE_INFERRED_LOW,
}


def confidence_rate(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    if value not in _VALID_CONFIDENCE_VALUES:
        raise ValueError(
            f"confidence_rate must be one of {sorted(_VALID_CONFIDENCE_VALUES)} "
            f"or None, got {value!r}. See timelive.md §4 for the standard scale."
        )
    return value


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


# =============================================================================
# TEXT HELPERS
# =============================================================================


def truncate_text(text: Optional[str], max_chars: int) -> Optional[str]:
    """
    Generic truncation helper (added 2026-09-15 for instagram_ingest.py's
    direct-message sampling — see the module docstring's "instagram
    migration" note for why this lives here and the per-group selection
    logic doesn't). None/empty input passes through unchanged. Adds a
    single trailing "…" only when text was actually cut, so a caller can
    tell a truncated value from a naturally short one without comparing
    lengths itself.
    """
    if not text:
        return text
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars] + "…"


# =============================================================================
# DECLARATIVE SCHEMA — ColumnSpec / TableSpec (timelive.md §3)
# =============================================================================


@dataclass
class ColumnSpec:
    """
    One column of a domain table. `name` and `sql_type` are what actually
    reaches SQLite; everything else is metadata the engine keeps around
    for describe_table() (timelive.md §3: "columns (name, type, semantic
    note when the name alone isn't enough)").
    """

    name: str
    sql_type: str  # "TEXT" | "INTEGER" | "REAL" — SQLite type affinity only
    semantic_note: Optional[str] = None
    # "person" | "location" | "category" | ... — only ever set when the
    # domain genuinely has this concept (timelive.md §3: never invented
    # to resemble another domain). None for most columns.
    entity_hint: Optional[str] = None
    not_null: bool = False
    # Marks a column as holding data the project owner considers
    # sensitive (added 2026-09-15, instagram migration — e.g. raw DM
    # text, a real contact's name). Purely a marker for a future access-
    # control/encryption layer that does not exist yet (timelive.md: the
    # vault is readable by design as long as only the project owner's own
    # tools touch it — see the "instagram migration" note above this
    # class). describe_table() surfaces it so a future bridge/consumer
    # can tell without re-deriving it from column names. Never used to
    # skip/alter ingest behaviour today — default False everywhere it
    # isn't explicitly set.
    sensitive: bool = False


@dataclass
class TableSpec:
    """
    A domain's declaration of one SQL table. A domain that needs more than
    one table (timelive.md §3) declares one TableSpec per table and links
    them the normal SQL way (a column that is a foreign key to another
    table's primary key) — there is no special "multi-table domain" case
    in this engine, it's just more than one TableSpec.
    """

    name: str
    columns: List[ColumnSpec]
    # Name of the INTEGER PRIMARY KEY column. Auto-increment, assigned by
    # SQLite. This is the id domain code gets back from upsert_rows() to
    # link child tables (e.g. game_moves.game_id -> games.game_id).
    primary_key_column: str
    # Column whose value must be unique for this table (timelive.md
    # discussion 2026-09-14: a single computed key, not a Python-side
    # composite-key function — see upsert_rows() docstring for why).
    # None means "no re-ingest stability for this table" (plain INSERT
    # every time) — only appropriate for child tables owned entirely by
    # a parent row, see upsert_rows().
    dedup_key_column: Optional[str] = None
    # The column read by the future bridge as this table's canonical
    # timestamp (timelive.md §4). None for tables with no time axis of
    # their own (e.g. a pure lookup table).
    canonical_timestamp_column: Optional[str] = None
    foreign_keys: Dict[str, str] = field(default_factory=dict)  # {column: "other_table(other_column)"}
    # Extra columns to index beyond canonical_timestamp_column and
    # entity_hint columns (both already auto-indexed — see
    # create_schema_for_table). Added 2026-09-14 for spotify: at ~358k
    # rows, a column that is neither a timestamp nor a cross-domain
    # entity_hint (artist_name, content_type, media_type, skipped) but
    # IS commonly filtered on still needs an index, or run_sql's own
    # SQL_TIMEOUT_SECONDS guardrail (llm_bridge.py) starts rejecting
    # ordinary questions on a full table scan. Not auto-inferred from
    # semantic_note or anything else — a domain lists exactly the
    # columns it knows are commonly filtered, same spirit as
    # entity_hint never being guessed.
    extra_indexed_columns: List[str] = field(default_factory=list)

    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]


@dataclass
class NotabilityConfig:
    """
    timelive.md §3: "the formula/weights for notability_score" is domain
    data; the engine only knows how to do a weighted sum. `weight_functions`
    values receive one record dict and must return a float, normally in
    [0, 1] (recency and any percentile-style signal are expected to already
    be pre-normalised by the domain — the engine does not clamp).
    """

    weight_functions: Dict[str, Callable[[Dict[str, Any]], float]]
    weights: Dict[str, float]
    score_field: str = "notability_score"


# =============================================================================
# NOTABILITY — unchanged algorithm from main.py's compute_notability_scores
# =============================================================================


def compute_notability_scores(
    records: Sequence[Dict[str, Any]],
    config: NotabilityConfig,
) -> None:
    """Mutates each record in place, adding config.score_field."""
    for record in records:
        score = 0.0
        for signal_name, weight in config.weights.items():
            fn = config.weight_functions.get(signal_name)
            if fn is None:
                continue
            try:
                score += weight * float(fn(record))
            except Exception:
                logger.debug(
                    "notability signal %r raised on a record, skipped (0 contribution)",
                    signal_name,
                )
                continue
        record[config.score_field] = round(score, 6)


def recency_weight(
    timestamp_iso: Optional[str],
    half_life_days: float,
    now: Optional[datetime] = None,
) -> float:
    """Unchanged from main.py. Exponential decay, 0.5 at half_life_days old."""
    ts = _parse_iso(timestamp_iso)
    if ts is None or half_life_days <= 0:
        return 0.0
    now = now or datetime.now(timezone.utc)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    age_days = max((now - ts).total_seconds() / 86400.0, 0.0)
    return 0.5 ** (age_days / half_life_days)


# =============================================================================
# SESSION / GROUPING HELPER
# =============================================================================
# Generalises main.py's group_by_time_and_compatibility: the old version
# took one fixed max_gap_seconds for the whole domain (fine for spotify's
# flat 20-minute rule, not for chess.com, whose allowed gap depends on the
# *next* game's own time control). This version takes a function instead
# of a constant; a domain that just wants a fixed gap passes
# `lambda prev, curr: FIXED_SECONDS`.


def group_into_sessions(
    events: Sequence[Dict[str, Any]],
    timestamp_begin_field: str,
    timestamp_end_field: str,
    gap_seconds_fn: Callable[[Dict[str, Any], Dict[str, Any]], float],
    is_compatible: Callable[[Dict[str, Any], Dict[str, Any]], bool] = lambda a, b: True,
) -> List[List[Dict[str, Any]]]:
    """
    `events` must already be in chronological order. Returns a list of
    groups (each a list of events); a session boundary is drawn whenever
    the gap since the previous event's end exceeds gap_seconds_fn(prev,
    curr), OR is_compatible(prev, curr) is False.
    """
    groups: List[List[Dict[str, Any]]] = []
    current_group: List[Dict[str, Any]] = []

    for event in events:
        if not current_group:
            current_group = [event]
            continue

        previous = current_group[-1]
        prev_end = _parse_iso(previous.get(timestamp_end_field) or previous.get(timestamp_begin_field))
        curr_begin = _parse_iso(event.get(timestamp_begin_field))
        gap_seconds = (
            (curr_begin - prev_end).total_seconds() if (prev_end and curr_begin) else math.inf
        )
        allowed_gap = gap_seconds_fn(previous, event)

        if gap_seconds <= allowed_gap and is_compatible(previous, event):
            current_group.append(event)
        else:
            groups.append(current_group)
            current_group = [event]

    if current_group:
        groups.append(current_group)

    return groups


# =============================================================================
# SCHEMA CREATION
# =============================================================================


def create_schema_for_table(conn: sqlite3.Connection, table: TableSpec) -> None:
    """
    CREATE TABLE IF NOT EXISTS from a TableSpec, plus indexes on the
    canonical timestamp column, every entity_hint column, and (2026-09-14,
    spotify migration) every column listed in extra_indexed_columns — see
    TableSpec.extra_indexed_columns docstring for why that last one was
    added. Original 2026-09-14 note on the first two: proposed to keep
    run_sql usable on large tables like spotify/whatsapp without a full
    table scan on every query — flagged to the project owner as not yet
    explicitly confirmed; easy to remove below if unwanted.
    """
    column_defs = []
    for col in table.columns:
        parts = [col.name, col.sql_type]
        if col.name == table.primary_key_column:
            parts.append("PRIMARY KEY AUTOINCREMENT" if col.sql_type == "INTEGER" else "PRIMARY KEY")
        if col.not_null:
            parts.append("NOT NULL")
        column_defs.append(" ".join(parts))

    if table.dedup_key_column and table.dedup_key_column != table.primary_key_column:
        column_defs.append(f"UNIQUE({table.dedup_key_column})")

    for col_name, reference in table.foreign_keys.items():
        column_defs.append(f"FOREIGN KEY({col_name}) REFERENCES {reference}")

    ddl = f"CREATE TABLE IF NOT EXISTS {table.name} (\n    " + ",\n    ".join(column_defs) + "\n)"
    logger.debug("creating schema for %s:\n%s", table.name, ddl)
    conn.execute(ddl)

    index_columns = set()
    if table.canonical_timestamp_column:
        index_columns.add(table.canonical_timestamp_column)
    for col in table.columns:
        if col.entity_hint:
            index_columns.add(col.name)
    for col_name in table.extra_indexed_columns:
        index_columns.add(col_name)
    # Every FK child column, always — found necessary 2026-09-14 by actually
    # running the spotify ingest twice in a row (not by inspection): with
    # foreign_keys=ON, deleting a parent row (e.g. DELETE FROM
    # listening_sessions, run every ingest to rebuild sessions — see
    # spotify_ingest.run_ingest()) makes SQLite verify no child row still
    # references it. Without an index on the child's FK column, that check
    # is a full table scan PER DELETED PARENT ROW — fine at chess.com's
    # scale (364 sessions x 1,785 games) but with spotify's real numbers
    # (17,445 sessions x 357,739 plays) it made a single re-ingest hang
    # well past two minutes where the first ingest (empty tables, nothing
    # to scan) had finished in seconds. This is a well-known, documented
    # SQLite recommendation (index your FK child columns) — applying it
    # unconditionally here fixes it for every current and future domain,
    # not just the one where the scale finally made it visible.
    for col_name in table.foreign_keys:
        index_columns.add(col_name)

    for col_name in index_columns:
        index_name = f"idx_{table.name}_{col_name}"
        conn.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table.name}({col_name})")


# =============================================================================
# DEDUPLICATION / UPSERT WITH STABLE IDS
# =============================================================================
# Deliberate change from the old JSON-era deduplicate_records(): that
# function ran in Python, before anything was written, and threw duplicates
# away silently. In a re-ingestable SQLite table this is the wrong shape —
# it can't tell "this record already exists, keep its old id" apart from
# "this record is new", which is exactly the bug the old system had
# (chessdotcom's event_number renumbering on every re-ingest, flagged as
# unresolved in the pre-2026-09-14 architecture). Here the domain computes
# ONE string value per record (table.dedup_key_column) however it wants —
# a native id copied as-is, or a composite string built from several
# fields, that part is still domain logic — and SQLite's own UNIQUE
# constraint + INSERT OR IGNORE enforces it. This also makes duplicates
# queryable for debugging (`SELECT dedup_key, COUNT(*) ... HAVING
# COUNT(*)>1`), which a Python set never was.


@dataclass
class UpsertOutcome:
    primary_key: int
    was_new: bool


def upsert_rows(
    conn: sqlite3.Connection,
    table: TableSpec,
    records: Sequence[Dict[str, Any]],
) -> List[UpsertOutcome]:
    """
    Inserts `records` into `table`. For each record, in the same order as
    the input, returns the resulting primary key and whether it was newly
    inserted or already present. Domain code uses `was_new` to decide
    whether to also (re)insert this row's children in another table —
    e.g. only insert a game's moves into game_moves when the game itself
    was new, so a re-ingest never duplicates move rows even though
    game_moves has no dedup_key_column of its own (see TableSpec docstring).

    If table.dedup_key_column is None, every record is inserted
    unconditionally (was_new is always True) — only appropriate for a
    table with no independent identity of its own (a pure child table).
    """
    columns = table.column_names()
    placeholders = ", ".join("?" for _ in columns)
    column_list = ", ".join(columns)
    # Columns that may legitimately change on a re-ingest (e.g. session_id,
    # notability_score) and must therefore be refreshed on an existing row —
    # everything except the identity columns themselves. Found necessary by
    # actually re-running an ingest twice: an earlier version only fetched
    # the existing primary key and left every other column at its
    # first-ever-inserted value forever, silently going stale.
    updatable_columns = [
        c for c in columns if c not in (table.primary_key_column, table.dedup_key_column)
    ]

    outcomes: List[UpsertOutcome] = []

    for record in records:
        values = [record.get(c) for c in columns]

        if table.dedup_key_column is None:
            cursor = conn.execute(
                f"INSERT INTO {table.name} ({column_list}) VALUES ({placeholders})",
                values,
            )
            outcomes.append(UpsertOutcome(primary_key=cursor.lastrowid, was_new=True))
            continue

        dedup_value = record.get(table.dedup_key_column)
        existing = conn.execute(
            f"SELECT {table.primary_key_column} FROM {table.name} WHERE {table.dedup_key_column} = ?",
            (dedup_value,),
        ).fetchone()

        if existing is None:
            cursor = conn.execute(
                f"INSERT INTO {table.name} ({column_list}) VALUES ({placeholders})",
                values,
            )
            outcomes.append(UpsertOutcome(primary_key=cursor.lastrowid, was_new=True))
        else:
            primary_key = existing[0]
            set_clause = ", ".join(f"{c} = ?" for c in updatable_columns)
            update_values = [record.get(c) for c in updatable_columns] + [primary_key]
            conn.execute(
                f"UPDATE {table.name} SET {set_clause} WHERE {table.primary_key_column} = ?",
                update_values,
            )
            outcomes.append(UpsertOutcome(primary_key=primary_key, was_new=False))

    return outcomes


# =============================================================================
# TABLE DESCRIPTION — data source for the future bridge describe_table()
# =============================================================================
# timelive.md §5: describe_table() must come from the schema itself, not
# a second hand-written declaration. This function is that data source;
# llm_bridge.py (task 4) will call it, not reimplement it.

_TABLE_SPEC_REGISTRY: Dict[str, TableSpec] = {}


def register_table_spec(table: TableSpec) -> None:
    """
    Domain modules call this once per TableSpec at import/setup time.

    Raises ValueError on a duplicate table name (added 2026-09-15,
    instagram migration — see the module docstring's "instagram
    migration" note). Before this change, a second domain registering the
    same table name would silently overwrite the first domain's spec in
    _TABLE_SPEC_REGISTRY, and describe_table()/the bridge would then
    describe the wrong domain's table under that name with no error at
    all — exactly the kind of silent cross-domain confusion timelive.md
    §3 already documents happening at query time with generic names. This
    doesn't replace picking distinctive names (still the first line of
    defence, see timelive.md §3), it just makes an actual collision loud
    instead of silent.
    """
    if table.name in _TABLE_SPEC_REGISTRY and _TABLE_SPEC_REGISTRY[table.name] is not table:
        raise ValueError(
            f"table name {table.name!r} is already registered — pick a distinctive "
            f"name per domain (timelive.md §3: avoid generic names once several "
            f"domains share one schema). Registered tables: {sorted(_TABLE_SPEC_REGISTRY)}"
        )
    _TABLE_SPEC_REGISTRY[table.name] = table


def describe_table(conn: sqlite3.Connection, table_name: str) -> Dict[str, Any]:
    if table_name not in _TABLE_SPEC_REGISTRY:
        raise KeyError(
            f"no TableSpec registered for {table_name!r} — was register_table_spec() "
            f"called for it? (registered: {sorted(_TABLE_SPEC_REGISTRY)})"
        )
    spec = _TABLE_SPEC_REGISTRY[table_name]

    pragma_rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    actual_columns = {row[1]: row[2] for row in pragma_rows}  # {name: sqlite type}

    columns_out = []
    for col in spec.columns:
        columns_out.append(
            {
                "name": col.name,
                "sql_type": actual_columns.get(col.name, col.sql_type),
                "semantic_note": col.semantic_note,
                "entity_hint": col.entity_hint,
                "is_primary_key": col.name == spec.primary_key_column,
                "sensitive": col.sensitive,
            }
        )

    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    return {
        "table": table_name,
        "columns": columns_out,
        "canonical_timestamp_column": spec.canonical_timestamp_column,
        "foreign_keys": spec.foreign_keys,
        "row_count": row_count,
    }


def list_tables() -> List[str]:
    """All tables any loaded domain module has registered a TableSpec for."""
    return sorted(_TABLE_SPEC_REGISTRY)


# =============================================================================
# DOMAIN REGISTRY + CONNECTION HANDLING
# =============================================================================


@dataclass
class DomainSpec:
    name: str
    module_name: str  # e.g. "chessdotcom_ingest", imported lazily


@dataclass
class IngestReport:
    domain: str
    tables_written: List[str]
    rows_inserted: int
    rows_already_present: int
    dry_run: bool


# Domains in original roadmap order (timelive.md §8). Consulted only for
# a domain NOT in DOMAIN_REGISTRY, to give an honest "not yet migrated"
# instead of a bare KeyError — NOT a live "still pending" list (it is not
# updated when a domain migrates; DOMAIN_REGISTRY is the source of truth
# for what's actually done).
_PLANNED_DOMAINS = [
    "chessdotcom",  # migrated — pilot
    "spotify",      # migrated — second domain
    "money",        # migrated — third domain (bank + investment + private markets); replaces "bank" in the old roadmap list
    "instagram",    # migrated — fourth domain (2026-09-15, Tier 1: posts/comments/likes/follows/DMs/login_activity)
    "maps",      # migrated — sixth domain (2026-09-17: maps_visits/maps_activities/maps_labeled_places)
    "whatsapp",
    "health",  # disabled even before the redesign (timelive.md §1 — data noise)
]

DOMAIN_REGISTRY: Dict[str, DomainSpec] = {
    "chessdotcom": DomainSpec(name="chessdotcom", module_name="chessdotcom_ingest"),
    "spotify": DomainSpec(name="spotify", module_name="spotify_ingest"),
    "money": DomainSpec(name="money", module_name="money_ingest"),
    "instagram": DomainSpec(name="instagram", module_name="instagram_ingest"),
    "maps": DomainSpec(name="maps", module_name="maps_ingest"),
}


def _open_connection(dry_run: bool) -> sqlite3.Connection:
    if dry_run:
        logger.info("dry-run: using an in-memory database, %s is not touched", VAULT_DB_PATH)
        conn = sqlite3.connect(":memory:")
    else:
        VAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(VAULT_DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def run_domain_ingest(domain: str, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    """
    Imports <module_name>_ingest's run_ingest(conn, dry_run, verbose)
    entry point and runs it inside one transaction, so a domain's update
    is all-or-nothing — a crash mid-ingest never leaves that domain's
    tables half-written. Every domain module must expose exactly this
    function signature; that's the one contract this engine assumes.

    Note on --dry-run: it runs against a fresh in-memory database, so it
    exercises parsing/classification/schema creation faithfully, but it
    can never test upsert-against-real-existing-data behaviour (there is
    no existing data in an empty in-memory db). It catches parsing and
    schema bugs, not re-ingest/dedup bugs against production data.
    """
    if domain not in DOMAIN_REGISTRY:
        if domain in _PLANNED_DOMAINS:
            raise NotImplementedError(
                f"{domain!r} is not migrated to ingest_engine.py yet — still on the "
                f"old PRIMARY/FULL JSON system (timelive.md §8). Planned, not built."
            )
        raise KeyError(f"unknown domain {domain!r}. Known/planned domains: {_PLANNED_DOMAINS}")

    spec = DOMAIN_REGISTRY[domain]
    module = importlib.import_module(spec.module_name)
    if not hasattr(module, "run_ingest"):
        raise AttributeError(f"{spec.module_name} has no run_ingest(conn, dry_run, verbose) entry point")

    conn = _open_connection(dry_run=dry_run)
    try:
        with conn:  # commits on clean exit, rolls back on exception
            result = module.run_ingest(conn, dry_run=dry_run, verbose=verbose)
        return result
    finally:
        conn.close()


# =============================================================================
# CLI
# =============================================================================


def _resolve_requested_domains(arg_value: str) -> List[str]:
    if arg_value == "all":
        return list(DOMAIN_REGISTRY)
    return [d.strip() for d in arg_value.split(",") if d.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Personal Data Vault — shared ingest engine (writes to vault.db).",
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Comma-separated domain names, or 'all'. Migrated: "
        f"{sorted(DOMAIN_REGISTRY) or '(none yet)'}. Planned: {_PLANNED_DOMAINS}.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and classify, write to an in-memory database instead of vault.db. "
        "Does not test dedup/upsert against real existing data — see run_domain_ingest() docstring.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Debug-level logging for the selected domain(s) only.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    domains = _resolve_requested_domains(args.domain)
    if not domains:
        parser.error("--domain resolved to an empty list")

    for domain in domains:
        logger.info("=== %s ===", domain)
        try:
            report = run_domain_ingest(domain, dry_run=args.dry_run, verbose=args.verbose)
        except Exception:
            logger.exception("ingest failed for domain %r", domain)
            continue
        logger.info(
            "%s: %d table(s), %d row(s) inserted, %d already present%s",
            report.domain,
            len(report.tables_written),
            report.rows_inserted,
            report.rows_already_present,
            " (dry-run, nothing written to vault.db)" if report.dry_run else "",
        )


if __name__ == "__main__":
    main()
