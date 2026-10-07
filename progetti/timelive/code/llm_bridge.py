# llm_bridge.py
# =============================================================================
# PERSONAL DATA VAULT — LLM QUERY / BRIDGE LAYER (SQLite architecture,
# 2026-09-14 rebuild — see EVOLUTION_LOG.md and timelive.md §6)
# =============================================================================
#
# WHAT CHANGED FROM THE OLD (PRIMARY/FULL JSON) VERSION OF THIS FILE
# -----------------------------------------------------------------------
# The old file had 4 tools, all domain-specific: search(), resolve_full_ref(),
# get_aggregation(), plus list_domains() pre-injected into the system prompt.
# Every one of those, and the DOMAIN_REGISTRY/DomainConfig machinery behind
# them, is GONE. There are now exactly 3 tools, and none of them know
# anything about "chess.com" or "spotify" specifically — they only know
# about SQL tables:
#     list_tables()        — which tables exist right now in vault.db
#     describe_table(table) — that table's columns, types, meaning, row count
#     run_sql(query)        — the ONLY way to actually read data
#
# GUARDRAILS (timelive.md §6 — "same spirit as the old validation, adapted
# to SQL")
# -----------------------------------------------------------------------
#   * Read-only at the OS/driver level, not just by convention: vault.db is
#     opened with SQLite's own read-only URI mode. An INSERT/UPDATE/DELETE/
#     DROP fails with a real database error before touching any data —
#     this is enforced by SQLite itself, not by scanning the query text for
#     forbidden words (which is easy to get wrong/bypass).
#   * A row limit (SQL_ROW_LIMIT below) is applied by fetching at most that
#     many rows, however many the query would otherwise return — never by
#     rewriting the model's SQL to insert a LIMIT clause (fragile: the query
#     might already have one, use a JOIN, an ORDER BY, etc.).
#   * A wall-clock timeout (SQL_TIMEOUT_SECONDS below) using SQLite's
#     progress handler — the only real way to interrupt a slow query
#     mid-execution in SQLite; connection-level `timeout=` only controls how
#     long to wait for a lock, it does NOT limit query execution time.
#   * A single SQL statement per call — Python's sqlite3 module already
#     refuses to execute more than one statement via `execute()`, which
#     incidentally blocks the classic "hide a second statement after a
#     semicolon" trick too.
#
# BOTH SQL_ROW_LIMIT AND SQL_TIMEOUT_SECONDS ARE PLACEHOLDER VALUES
# -----------------------------------------------------------------------
# 2026-09-14 conversation: no domain is "typical" yet (chess.com is tiny
# compared to what spotify/health/whatsapp will be), so there is no real
# basis yet to tune these precisely. Kept as the two constants right below
# — change them in ONE place here, not per domain — and revisit once
# bigger domains are migrated and real queries have been seen.
#
# OLLAMA_NUM_CTX — NOT a placeholder, a real fix (2026-09-14, spotify
# migration testing)
# -----------------------------------------------------------------------
# The pre-injected schema in build_system_prompt() scales with how many
# domains are migrated: with chess.com alone it was small enough not to
# matter; with chess.com + spotify (5 tables, spotify's `plays` and
# chess.com's `games` each ~29-31 columns with semantic notes) it measures
# ~3,460 tokens on its own — verified by actually building it against the
# real vault.db, not estimated. Ollama's default context window for
# llama3.2:3b (2048 unless told otherwise) is SMALLER than that. Without
# num_ctx set explicitly, the system prompt gets silently truncated before
# the model ever sees the actual question — no error, just a model that
# looks confused about a schema it was never fully shown. Set here once,
# not per call site, so it always travels with OllamaClient regardless of
# who instantiates it. 8192 leaves headroom for schema growth (more
# domains still to migrate) plus a few tool-call/tool-result round trips;
# raise it further if a future domain's schema needs more room, but note
# a bigger context window costs more RAM and slower prefill on the Pi's
# CPU — it is not a free dial.
#
# 2026-09-15 UPDATE — schema injection made lazy (instagram migration,
# real batch failure on the Pi)
# -----------------------------------------------------------------------
# The OLLAMA_NUM_CTX note above turned out to be exactly right, and the
# growth it warned about actually happened: adding money (3 tables) and
# then instagram (8 tables) pushed the FULL pre-injected schema (every
# column's semantic_note/entity_hint/sensitive flag, for every table) from
# the ~3,460 tokens measured above to ~10,200 tokens — verified by
# actually rebuilding the real 16-table schema (chessdotcom+spotify+money+
# instagram) locally and measuring build_system_prompt()'s real output,
# not estimated. That is now BIGGER than OLLAMA_NUM_CTX (8192), so Ollama
# silently truncates the prompt before the model ever sees it — and,
# independent of truncation, prefilling ~10k tokens on the Pi's CPU is
# itself slow. Real-world confirmation: a real 9-question mini-batch
# (llama3.2:3b, --request-timeout 120) run on the Pi after the instagram
# migration failed 9/9 with an identical HTTP read-timeout on every single
# question, including the very first tool call of the very first
# question — a systemic prefill-cost problem, not a per-question model
# reasoning failure (those look different: partial success, occasional
# hit_max_iterations, not 100% identical timeouts).
#
# This does NOT get fixed by raising OLLAMA_NUM_CTX again — that only
# delays the same failure to the next domain (each one adds roughly
# 1,500-2,500 more tokens of full schema, forever, to EVERY question
# regardless of which domain it's actually about). The real fix, and the
# standard approach for text-to-SQL over a schema with many tables: stop
# dumping the full schema (every column's semantic_note/entity_hint/
# sensitive flag) into every prompt, and inject only a COMPACT index
# instead — table name, row_count, column NAMES and SQL types only, no
# semantic notes — then let the model call the already-existing
# describe_table tool for the 1-3 tables it actually needs before writing
# SQL. Measured effect on the same real 16-table schema: the compact index
# is ~19x smaller than the full manifest (about 2,000 characters instead
# of ~38,700), comfortably inside OLLAMA_NUM_CTX even with many more
# domains added later. See build_system_prompt()'s docstring below for the
# exact shape and _compact_schema_entry().
#
# Project owner's explicit decision (2026-09-15 chat): keep vault.db as
# ONE shared database (not one file per domain) — cross-domain queries
# (e.g. "who I message on Instagram vs. who I share a Spotify playlist
# with") are an explicit stated future goal, and splitting the database
# would work against that. A further two-level index (domain -> tables,
# for when table COUNT itself gets very large, e.g. hundreds of tables
# across ~30-50+ domains) was discussed and deliberately deferred — no
# `domain` field exists yet on TableSpec, and the flat compact index
# already comfortably outscales the near-term roadmap. Revisit if/when
# the flat compact index itself starts approaching a meaningful fraction
# of OLLAMA_NUM_CTX again.
#
# 2026-09-15 UPDATE 2 — the compact index fixed the timeout, but exposed
# a SEPARATE bug: describe_table is never actually called
# -----------------------------------------------------------------------
# The real 9-question instagram mini-test re-run after the fix above: 8/9
# succeeded (down from 9/9 timeouts), avg 79s/question (down from
# 120-237s). The context-overflow bug is fixed, confirmed on real
# hardware, not just by local measurement. BUT the report's
# tool_calls_by_tool showed {"run_sql": 12} and NOT ONE describe_table
# call across all 9 questions — despite the system prompt explicitly
# instructing the model to call describe_table before writing SQL against
# an uninspected table. llama3.2:3b just guesses column names from the
# compact index instead (e.g. "media_owner_username" on instagram_posts,
# "follower_count" on instagram_following, "type" on
# instagram_direct_message_threads — all real sql_errors from the actual
# run), then either recovers by trial and error, silently reads a value
# straight off the table index without querying, or gives a confidently
# wrong/incomplete answer. Prompt text alone isn't enough for this model.
#
# Fix: describe_table is no longer just RECOMMENDED, it's ENFORCED in
# code. run_query() now tracks which tables have had describe_table
# called on them THIS conversation; a run_sql call that references a
# table not yet described is intercepted before it ever reaches SQLite
# and bounced back with an error telling the model which table(s) to
# describe first — see _extract_referenced_tables() and the
# `described_tables` bookkeeping in run_query(). This costs one extra
# iteration per new table touched (describe_table, then the real query),
# which is why MAX_ITERATIONS was raised from 5 to 8 in the same change —
# a cross-domain question touching 3 tables one at a time could otherwise
# hit the old cap before ever getting a real answer. NOTE this table-name
# extraction is a narrow FROM/JOIN regex, not a real SQL parser (same
# philosophy as _try_parse_malformed_tool_call's regex fallback below) —
# it can miss a table referenced only via comma-join syntax or deep
# inside a subquery; it does not need to be perfect to be a large
# improvement over pure prompt instructions.
#
# 2026-09-17 UPDATE — EMPTY FINAL ANSWER despite "success": true
# (fresh-45 batch analysis, qwen3.5:4b, real Pi hardware)
# -----------------------------------------------------------------------
# A real 45-question batch (never-before-tested question set, 300s
# request timeout) found 4 questions where the agentic loop ended with
# turn.is_final=True, zero tool calls, AND an empty content string —
# recorded by run_query() as a normal, successful QueryResult with
# answer="" (see the `return QueryResult(answer=turn.content or "", ...)`
# branch above). 13.3% of that batch's "successful" answers were
# genuinely blank text, despite real (often correct) tool calls having
# already been made earlier in the same conversation — e.g. adversarial_04
# ran 6 well-targeted queries confirming no Tesla holdings, then wrote
# nothing as its final answer. This is NOT the already-known malformed-
# JSON-as-final-answer bug (that always produces some non-empty, wrong-
# shaped text) — here there is no text captured at all. Iteration counts
# at the empty turn varied (5, 6, 7, 8) — not tied to hitting
# MAX_ITERATIONS.
#
# Leading hypothesis, NOT YET CONFIRMED on real hardware (flagged
# explicitly rather than presented as settled — this needs verification
# on the Pi, not assumed from this analysis alone): qwen3.5 is a
# reasoning-capable model family with an extended "thinking" mode Ollama
# exposes as a message field separate from `content` (already flagged as
# a latency risk on 2026-09-14 in the harness section below, never
# actually checked until now). If a turn's entire generation budget goes
# into that separate `thinking` field with nothing left over for visible
# `content`, this bridge's old code (`content=message.get("content") or
# None`) silently discarded the thinking and returned an empty answer —
# exactly the observed symptom.
#
# Fix applied here, NOT yet validated against a real Ollama server (see
# OllamaClient.__init__'s `think` parameter and .chat()'s docstring
# comments): (1) `think: false` is now sent on every request by default,
# so a thinking-capable model is asked to answer directly instead of
# spending its budget on hidden reasoning — this bridge never surfaces
# chain-of-thought to the user anyway, so there is no upside being traded
# away; this may also help the (much larger) timeout problem, since
# thinking mode was already suspected of inflating latency on CPU. (2) As
# a defensive fallback in case `think: false` doesn't fully eliminate the
# issue (unsupported Ollama version, or a different root cause entirely):
# if a "final" turn comes back with no tool calls and no content,
# .chat() now checks the separate `thinking` field and, if present,
# returns it as an explicitly-labeled, explicitly-unverified partial
# answer instead of silent blank text — an honest partial beats a silent
# empty "success". Next real batch on the Pi should report whether (a)
# blank final answers still occur at all with think:false, and (b) the
# two 500 Internal Server Error failures seen the same batch
# (spotify_15, ambiguous_01 — a different failure mode, an actual Ollama
# server error rather than a well-formed empty response) also stop
# happening; those need the Pi's own Ollama server logs to root-cause and
# were NOT diagnosable from the batch report alone.
# =============================================================================

from __future__ import annotations

import importlib
import json
import re
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import ingest_engine

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# --- Orchestration ---
# 2026-09-15 UPDATE 2: raised from 5 to 8 — the new mandatory
# describe_table-before-run_sql gate (see module docstring) costs one
# extra iteration per NEW table a question touches (describe_table, then
# the real query), so a 3-table cross-domain question could exhaust the
# old cap of 5 before ever producing a real answer.
MAX_ITERATIONS = 8  # hard cap on tool-call round-trips per question; tune per model

# --- Generation temperature ---
TOOL_CALL_TEMPERATURE = 0.1
FINAL_ANSWER_TEMPERATURE = 0.4

# --- SQL guardrails (PLACEHOLDER VALUES — see module docstring) ---
SQL_ROW_LIMIT = 200
SQL_TIMEOUT_SECONDS = 10.0

# --- Ollama connection defaults (overridable per OllamaClient instance) ---
OLLAMA_DEFAULT_HOST = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3.2:3b"
OLLAMA_NUM_CTX = 8192  # see module docstring's OLLAMA_NUM_CTX note — not a placeholder


# ==============================================================================
# DOMAIN MODULE LOADING
# ==============================================================================
# Each domain module registers its own TableSpecs (columns, semantic notes,
# entity hints) as a side effect of being imported — see e.g.
# chessdotcom_ingest.py's module-level register_table_spec() calls. This
# bridge needs those specs to build describe_table()/the schema manifest,
# so every migrated domain is imported here, once, even though this file
# never calls any domain's run_ingest() itself (it only ever reads).

for _domain_spec in ingest_engine.DOMAIN_REGISTRY.values():
    importlib.import_module(_domain_spec.module_name)


class DatasetUnavailableError(Exception):
    """Raised when vault.db itself doesn't exist yet — nothing has been ingested."""


def _get_readonly_connection() -> sqlite3.Connection:
    if not ingest_engine.VAULT_DB_PATH.exists():
        raise DatasetUnavailableError(
            f"{ingest_engine.VAULT_DB_PATH} does not exist yet — no domain has been ingested."
        )
    # SQLite's own read-only mode, enforced by the database engine itself —
    # not a convention this file just happens to follow.
    conn = sqlite3.connect(f"file:{ingest_engine.VAULT_DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _install_timeout(conn: sqlite3.Connection, seconds: float) -> None:
    deadline = time.monotonic() + seconds

    def handler() -> int:
        return 1 if time.monotonic() > deadline else 0  # non-zero return aborts the query

    conn.set_progress_handler(handler, 1000)  # check every 1000 SQLite VM instructions


def _compact_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), default=str)


def _compact_schema_entry(full_entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    2026-09-15 addition (see module docstring's UPDATE note): strips one
    table's FULL describe_table() output down to just what's needed to
    decide WHETHER a table is relevant to a question — column NAMES and
    SQL types, row_count, foreign_keys, canonical_timestamp_column. Drops
    the expensive part: every column's semantic_note/entity_hint/sensitive
    flag, which is exactly what made the full manifest ~19x bigger than
    this. Those details aren't gone — describe_table(table) still returns
    them in full, on demand, for the 1-3 tables a given question actually
    needs (see the new system-prompt rule in build_system_prompt()).
    """
    return {
        "row_count": full_entry.get("row_count"),
        "columns": {c["name"]: c["sql_type"] for c in full_entry.get("columns", [])},
        "foreign_keys": full_entry.get("foreign_keys") or {},
        "canonical_timestamp_column": full_entry.get("canonical_timestamp_column"),
    }


_TABLE_REF_RE = re.compile(r'\b(?:FROM|JOIN)\s+["\[`]?([A-Za-z_][A-Za-z0-9_]*)', re.IGNORECASE)


def _extract_referenced_tables(query: str) -> List[str]:
    """
    2026-09-15 UPDATE 2 addition (see module docstring): best-effort scan
    for real table names referenced via FROM/JOIN in a run_sql query,
    used to enforce "describe_table before run_sql on a new table" in
    code rather than relying on the model reading a prompt instruction
    (see run_query()'s `described_tables` bookkeeping). Deliberately a
    narrow regex, not a real SQL parser — same philosophy as
    _try_parse_malformed_tool_call's regex fallback elsewhere in this
    file. Filtered against ingest_engine.list_tables() so a CTE name or a
    subquery alias is never mistaken for a real table needing
    describe_table. Known blind spot: a table referenced only via
    old-style comma-join syntax (`FROM a, b`) or nested two levels deep
    inside a subquery may be missed — acceptable, since the point is to
    catch the common case (a bare FROM/JOIN on a real table), not to
    replace real SQL validation.
    """
    known = set(ingest_engine.list_tables())
    found: List[str] = []
    for match in _TABLE_REF_RE.finditer(query):
        name = match.group(1)
        if name in known and name not in found:
            found.append(name)
    return found


# ==============================================================================
# THE 3 TOOLS
# ==============================================================================


def tool_list_tables() -> Dict[str, Any]:
    return {"tables": ingest_engine.list_tables()}


def tool_describe_table(table: str) -> Dict[str, Any]:
    conn = _get_readonly_connection()
    try:
        return ingest_engine.describe_table(conn, table)
    finally:
        conn.close()


def tool_run_sql(query: str) -> Dict[str, Any]:
    stripped = query.strip()
    conn = _get_readonly_connection()
    try:
        _install_timeout(conn, SQL_TIMEOUT_SECONDS)
        cursor = conn.execute(stripped)
        column_names = [d[0] for d in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(SQL_ROW_LIMIT + 1)
        truncated = len(rows) > SQL_ROW_LIMIT
        rows = rows[:SQL_ROW_LIMIT]
        result: Dict[str, Any] = {
            "columns": column_names,
            "rows": [dict(row) for row in rows],
            "row_count": len(rows),
        }
        if truncated:
            result["truncated"] = True
            result["note"] = (
                f"Result truncated to {SQL_ROW_LIMIT} rows. Add WHERE/GROUP BY/LIMIT/ORDER BY "
                f"to your query to get a smaller, more specific answer instead of relying on this cutoff."
            )
        return result
    except sqlite3.OperationalError as exc:
        message = str(exc)
        if "interrupted" in message.lower():
            return {
                "error": "timeout",
                "message": (
                    f"Query did not finish within {SQL_TIMEOUT_SECONDS}s and was stopped. "
                    f"Try a narrower or simpler query (add a WHERE clause, avoid scanning "
                    f"every row of a large table)."
                ),
            }
        return {"error": "sql_error", "message": message}
    except sqlite3.Error as exc:
        return {"error": "sql_error", "message": str(exc)}
    finally:
        conn.close()


TOOL_FUNCTIONS: Dict[str, Callable[..., Dict[str, Any]]] = {
    "list_tables": tool_list_tables,
    "describe_table": tool_describe_table,
    "run_sql": tool_run_sql,
}

TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_tables",
            "description": "List every table currently available in the vault database.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "describe_table",
            "description": (
                "Get one table's columns (name, SQL type, and what each one means when "
                "the name alone isn't obvious), its row count, and which other table(s) "
                "it links to. The compact index already in your system prompt only gives "
                "column names/types with no explanation. REQUIRED: run_sql will be "
                "REJECTED with an error if it references a table you have not called "
                "describe_table on yet this conversation — call this first for every new "
                "table, so you know what each column actually means instead of guessing "
                "from its name."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "table": {"type": "string", "description": "Exact table name, from list_tables."}
                },
                "required": ["table"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": (
                f"Run a single read-only SQL SELECT statement against the vault database "
                f"(standard SQLite syntax). This is the ONLY way to actually retrieve data. "
                f"Results are capped at {SQL_ROW_LIMIT} rows — use WHERE / GROUP BY / ORDER BY / "
                f"LIMIT to get exactly what the question needs instead of relying on that cutoff. "
                f"REQUIRED: call describe_table first on every table this query references that "
                f"you haven't already inspected this conversation — this call is REJECTED "
                f"otherwise, with an error naming which table(s) to describe."
            ),
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "A single SQL SELECT statement."}},
                "required": ["query"],
            },
        },
    },
]


# ==============================================================================
# TOOL-CALL VALIDATION
# ==============================================================================


class ToolValidationError(Exception):
    """Raised for anything wrong with a tool call before it ever touches vault.db."""


def validate_tool_call(name: str, arguments: Dict[str, Any]) -> None:
    if name not in TOOL_FUNCTIONS:
        raise ToolValidationError(f"Unknown tool {name!r}. Available tools: {sorted(TOOL_FUNCTIONS)}.")

    if name == "describe_table":
        table = arguments.get("table")
        known = ingest_engine.list_tables()
        if table not in known:
            raise ToolValidationError(f"Unknown table {table!r}. Known tables: {known}.")

    elif name == "run_sql":
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ToolValidationError("'query' must be a non-empty SQL string.")
        first_word = query.strip().split(None, 1)[0].upper()
        if first_word not in ("SELECT", "WITH"):
            raise ToolValidationError(
                f"run_sql only accepts a SELECT (or WITH ... SELECT) statement — got a query "
                f"starting with {first_word!r}. The database connection is read-only regardless, "
                f"but write-shaped queries are rejected here with a clearer message first."
            )


# ==============================================================================
# SYSTEM PROMPT
# ==============================================================================


def build_system_prompt() -> str:
    """
    2026-09-15 UPDATE (see module docstring): used to pre-inject the FULL
    schema of every table (every column's semantic_note/entity_hint/
    sensitive flag) — that's what grew to ~10,200 tokens once
    money+instagram were added, bigger than OLLAMA_NUM_CTX, and caused a
    100% timeout failure in a real batch run on the Pi. Now injects only a
    COMPACT index (table name -> row_count, column names/types,
    foreign_keys, canonical_timestamp_column — see _compact_schema_entry())
    and tells the model to call describe_table for the specific table(s)
    it actually needs. The model can still call list_tables/describe_table
    itself for anything not covered here, same as before.
    """
    conn = _get_readonly_connection()
    try:
        full_manifest = {name: ingest_engine.describe_table(conn, name) for name in ingest_engine.list_tables()}
    except DatasetUnavailableError:
        full_manifest = {}
    finally:
        if "conn" in locals():
            try:
                conn.close()
            except Exception:
                pass

    compact_manifest = {name: _compact_schema_entry(entry) for name, entry in full_manifest.items()}

    return (
        "You are a private data assistant for the user's Personal Data Vault. "
        "You answer questions using ONLY the run_sql tool against the tables described "
        "below — never from general knowledge, and never by inventing a number you did "
        "not retrieve with a real query.\n\n"
        "You have 3 tools: list_tables, describe_table, run_sql.\n\n"
        "Below is a COMPACT INDEX of every table currently available: row_count, column "
        "names and SQL types only — NO explanation of what a column means. Use it to "
        "figure out which table(s) are relevant to the question, then call describe_table "
        "on those specific table(s) BEFORE writing any SQL against them, to learn what "
        "each column actually means (native vs derived, units, which literal values are "
        "real, caveats) — do not guess a column's meaning from its name alone. This is "
        "ENFORCED, not optional: run_sql will be rejected with an error if it references "
        "a table you have not called describe_table on yet this conversation. Skip "
        "describe_table only for a table you have already called it on earlier in this "
        "same conversation.\n\n"
        f"TABLE INDEX:\n{_compact_json(compact_manifest)}\n\n"
        "Rules:\n"
        "- run_sql is the only way to retrieve data. Write standard SQLite SELECT statements.\n"
        "- Every run_sql result may be capped at a row limit — if a result says "
        "'truncated', narrow your query (WHERE / GROUP BY / LIMIT) instead of assuming "
        "the rows you got back are everything.\n"
        "- Never call run_sql with the exact same query twice in a row.\n"
        "- Columns ending in _id (e.g. game_id, session_id) are internal identifiers — "
        "useful for JOINs, not meaningful to show the user directly.\n"
        "- A NULL value in a column means the data genuinly is not known/not applicable "
        "— never fill in a guess for it.\n"
        "- Each table's row_count is already given to you above, in the table index — "
        "never call run_sql just to COUNT(*) an entire table, read it from the index instead.\n"
        "- run_sql takes a single 'query' string and nothing else — there is no parameter "
        "binding. Never use placeholders like ? or :name in your SQL; write every value "
        "directly as a literal in the query text.\n"
        "- A column's real stored values can differ from how you would naturally phrase "
        "the question (language, translation, exact native spelling/casing). Before "
        "filtering a text column on a specific value you are not certain is exact "
        "(a name, an institution, a security, a category), run a quick discovery query "
        "first, e.g. SELECT DISTINCT column FROM table WHERE column LIKE '%keyword%', "
        "instead of guessing the literal string and concluding 'no data' from zero rows.\n"
        "- If you already have enough information from a previous run_sql result, answer "
        "directly in plain text instead of calling another tool.\n"
    )


# ==============================================================================
# LLM CLIENT INTERFACE + IMPLEMENTATIONS
# ==============================================================================
# Unchanged from the old file — none of this is domain- or tool-specific,
# it only knows about the generic OpenAI-style tool-calling shape.


@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]


@dataclass
class AssistantTurn:
    """One model turn: either a final answer, or one or more tool calls."""
    content: Optional[str] = None
    tool_calls: List[ToolCall] = field(default_factory=list)
    # [agente TL06] per-call Ollama prompt-eval metrics — fields of the raw
    # /api/chat response, recorded to check whether Ollama's prompt-prefix
    # cache works (docs/todo_table_routing_test.md, "Altro spunto").
    # prompt_eval_count = tokens of the prompt the model evaluated;
    # prompt_eval_duration = nanoseconds spent on that prefill. None when the
    # backend is not Ollama (or the response lacks the fields) — see
    # OllamaClient.chat(); nothing downstream may fail on them.
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None

    @property
    def is_final(self) -> bool:
        return not self.tool_calls


class LLMClient:
    """Minimal interface the agentic loop needs from any model backend."""

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        temperature: float,
    ) -> AssistantTurn:
        raise NotImplementedError


class OllamaClient(LLMClient):
    """Real backend: Ollama's OpenAI-compatible tool-calling chat API."""

    def __init__(
        self,
        model: str = OLLAMA_DEFAULT_MODEL,
        host: str = OLLAMA_DEFAULT_HOST,
        timeout_seconds: float = 600.0,
        num_ctx: int = OLLAMA_NUM_CTX,
        think: bool = False,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.num_ctx = num_ctx
        # 2026-09-17 addition — see module docstring's "empty final answer"
        # note below. Default False: this bridge parses a strict tool-call/
        # plain-text-answer shape and never shows chain-of-thought to the
        # user, so a reasoning model's extended thinking buys nothing here
        # and, per the fresh-45 batch, may be actively costing correctness
        # (4/30 blank final answers) and latency (already flagged as a risk
        # on 2026-09-14, never verified until now). NOT yet validated
        # against a real Ollama server + qwen3.5:4b on the Pi — the request
        # field name/behavior ("think") matches Ollama's documented
        # thinking-model support as of this bridge's last verification, but
        # Ollama's API can change between versions; if the server rejects
        # or silently ignores this field, that itself is a useful signal
        # (check `ollama --version` and the release notes for "think" /
        # "reasoning" support before assuming this fix landed).
        self.think = think

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        temperature: float,
    ) -> AssistantTurn:
        import requests  # lazy import — so FakeLLM-only usage needs no network dependency

        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "tools": tools,
                "stream": False,
                # 2026-09-17: disable extended "thinking" for reasoning-capable
                # models (e.g. qwen3.5) — see self.think's docstring above and
                # the module docstring's "EMPTY FINAL ANSWER" note. Harmless
                # no-op on a model/Ollama version that doesn't support it.
                "think": self.think,
                # num_ctx set explicitly — see module docstring's OLLAMA_NUM_CTX note.
                # Ollama's own default (2048) is smaller than this bridge's system
                # prompt once more than one domain is migrated; left implicit, the
                # schema gets silently truncated with no error at all.
                "options": {"temperature": temperature, "num_ctx": self.num_ctx},
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        message = payload.get("message", {})
        # [agente TL06] capture the top-level prompt-eval metrics from the
        # Ollama response. .get() (never dict indexing): absent field =>
        # None, so an Ollama version that omits them cannot break the loop.
        prompt_eval_count = payload.get("prompt_eval_count")
        prompt_eval_duration = payload.get("prompt_eval_duration")

        raw_tool_calls = message.get("tool_calls") or []
        tool_calls = [
            ToolCall(
                name=(tc.get("function", {}) or {}).get("name", ""),
                arguments=_coerce_arguments((tc.get("function", {}) or {}).get("arguments", {})),
            )
            for tc in raw_tool_calls
        ]
        content = message.get("content") or None
        if content is None and not tool_calls:
            # 2026-09-17 diagnostic (see module docstring): this is exactly
            # the shape observed 4 times in the fresh-45 batch (money_15,
            # spotify_07, instagram_04, adversarial_04) — a "final" turn
            # with no tool calls AND no content, silently recorded as a
            # blank "success". Surface whatever Ollama put in the separate
            # `thinking` field (present on reasoning-model responses,
            # distinct from `content`) into the returned content instead of
            # discarding it — an explicit, visibly-partial answer is more
            # honest than a blank one, and the presence/absence of this
            # field is itself useful evidence for confirming the "thinking
            # ate the whole turn" hypothesis on the next real batch.
            thinking = message.get("thinking")
            if thinking:
                content = (
                    "[risposta finale mancante — riportato il ragionamento "
                    "grezzo del modello, non verificato: " + thinking.strip() + "]"
                )
        return AssistantTurn(
            content=content,
            tool_calls=tool_calls,
            # [agente TL06] per-call metrics for the prefix-cache check.
            prompt_eval_count=prompt_eval_count,
            prompt_eval_duration=prompt_eval_duration,
        )


def _coerce_arguments(arguments: Any) -> Dict[str, Any]:
    """Ollama can return tool-call arguments as a dict OR a JSON string, depending on version."""
    if isinstance(arguments, dict):
        return arguments
    if isinstance(arguments, str):
        try:
            return json.loads(arguments)
        except json.JSONDecodeError:
            return {}
    return {}


def _internal_messages_to_anthropic(
    messages: List[Dict[str, Any]],
) -> Tuple[Optional[str], List[Dict[str, Any]]]:
    """
    Converts the OpenAI-chat-completions-shaped message list run_query()
    builds into what the Anthropic Messages API expects. See run_query():
    every assistant message here has exactly one tool call, immediately
    followed by its one tool-result message, so ids can be derived
    deterministically from position in `messages` with no extra bookkeeping.
    """
    system_prompt: Optional[str] = None
    anthropic_messages: List[Dict[str, Any]] = []

    for index, msg in enumerate(messages):
        role = msg.get("role")

        if role == "system":
            system_prompt = msg.get("content")
        elif role == "user":
            anthropic_messages.append({"role": "user", "content": msg.get("content") or ""})
        elif role == "assistant":
            tool_use_id = f"toolu_{index}"
            content_blocks: List[Dict[str, Any]] = []
            if msg.get("content"):
                content_blocks.append({"type": "text", "text": msg["content"]})
            for call in msg.get("tool_calls", []):
                fn = call.get("function", {})
                content_blocks.append({
                    "type": "tool_use",
                    "id": tool_use_id,
                    "name": fn.get("name"),
                    "input": fn.get("arguments") or {},
                })
            anthropic_messages.append({"role": "assistant", "content": content_blocks})
        elif role == "tool":
            anthropic_messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": f"toolu_{index - 1}",
                    "content": msg.get("content") or "",
                }],
            })

    return system_prompt, anthropic_messages


def _openai_tools_to_anthropic(tool_schemas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    converted = []
    for schema in tool_schemas:
        fn = schema["function"]
        converted.append({
            "name": fn["name"],
            "description": fn.get("description", ""),
            "input_schema": fn["parameters"],
        })
    return converted


class ClaudeAPIClient(LLMClient):
    """
    Cloud backend: calls the real Anthropic Messages API instead of a local
    Ollama server. Requires `pip install anthropic --break-system-packages`
    and an ANTHROPIC_API_KEY environment variable set in the shell this
    runs in — never hardcoded here or passed as a plain CLI argument.
    """

    def __init__(self, model: str = "claude-sonnet-5", max_tokens: int = 1536) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        temperature: float,
    ) -> AssistantTurn:
        client = self._ensure_client()
        system_prompt, anthropic_messages = _internal_messages_to_anthropic(messages)

        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt or "",
            messages=anthropic_messages,
            tools=_openai_tools_to_anthropic(tools),
        )

        text_parts: List[str] = []
        tool_calls: List[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(name=block.name, arguments=dict(block.input or {})))

        return AssistantTurn(
            content="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
        )


def _internal_messages_to_openai(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    2026-09-15 UPDATE 2 addition: converts the internal message list this
    file builds (Ollama-shaped — tool-call arguments as a raw dict, only
    loosely tracking tool_call_id) into the STRICT OpenAI chat-completions
    format TogetherAIClient's real OpenAI-compatible endpoint expects:
    function.arguments JSON-encoded as a string (per spec — Ollama's own
    /api/chat is lenient and accepts a raw dict, which is why the internal
    format was never strict to begin with), and tool_call_id present on
    both the assistant's tool_calls entry and its matching tool-role
    result message (run_query() now always sets this — see the
    `tool_call_id` bookkeeping there). Same pattern as
    _internal_messages_to_anthropic() above: each backend owns its own
    wire-format conversion instead of forcing one strict shape on the
    shared internal representation.
    """
    converted: List[Dict[str, Any]] = []
    for msg in messages:
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            new_calls = []
            for i, tc in enumerate(msg["tool_calls"]):
                fn = tc.get("function", {})
                new_calls.append({
                    "id": tc.get("id") or f"call_{i}",
                    "type": "function",
                    "function": {
                        "name": fn.get("name"),
                        "arguments": _compact_json(fn.get("arguments") or {}),
                    },
                })
            converted.append({"role": "assistant", "content": msg.get("content"), "tool_calls": new_calls})
        elif msg.get("role") == "tool":
            converted.append({
                "role": "tool",
                "tool_call_id": msg.get("tool_call_id") or "call_0",
                "content": msg.get("content"),
            })
        else:
            converted.append(msg)
    return converted


class TogetherAIClient(LLMClient):
    """
    2026-09-15 UPDATE 2 addition. Cloud backend: Together AI's real,
    OpenAI-compatible chat-completions API, for comparing llama3.2:3b
    (local, Ollama, 3B) against a mid-size (8-16B class) open model
    without needing to run it on the Pi. Requires a TOGETHER_API_KEY
    environment variable — never hardcoded here or passed as a plain CLI
    argument (same convention as ANTHROPIC_API_KEY for ClaudeAPIClient
    above). Uses `requests` directly against Together's HTTP API — no
    extra package needed beyond what OllamaClient already requires.

    Project owner's choice (2026-09-15 chat): Together AI + a Qwen2.5
    14B/32B-class model for the overnight cross-domain comparison batch.

    NOT LIVE-TESTED IN THIS SESSION — unlike every other number in this
    session's work (schema sizes, the describe_table gate's effect,
    etc.), which were measured against real data before being reported,
    this client has never been run against a real Together endpoint (no
    API key, no egress to arbitrary hosts from this sandbox). The request/
    response shape follows Together's documented OpenAI-compatible spec,
    and _internal_messages_to_openai() exists specifically because the
    internal message format was never strict enough for this to work
    without it — but confirm the exact model slug (Together's serverless
    catalog changes; check https://docs.together.ai/docs/serverless-models
    or `together models list`) and run ONE cheap smoke-test question
    (`--backend together --ids manifest_01`) before committing to a full
    overnight run.
    """

    def __init__(
        self,
        model: str = "Qwen/Qwen2.5-14B-Instruct",
        host: str = "https://api.together.xyz/v1",
        max_tokens: int = 1536,
        timeout_seconds: float = 120.0,
    ) -> None:
        self.model = model
        self.host = host.rstrip("/")
        self.max_tokens = max_tokens
        self.timeout_seconds = timeout_seconds

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        temperature: float,
    ) -> AssistantTurn:
        import os
        import requests  # lazy import — same convention as OllamaClient

        api_key = os.environ.get("TOGETHER_API_KEY")
        if not api_key:
            raise RuntimeError(
                "TOGETHER_API_KEY is not set in the environment — required for "
                "TogetherAIClient. Never hardcode it here or pass it as a CLI argument "
                "(same convention as ANTHROPIC_API_KEY)."
            )

        response = requests.post(
            f"{self.host}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": self.model,
                "messages": _internal_messages_to_openai(messages),
                "tools": tools,
                "temperature": temperature,
                "max_tokens": self.max_tokens,
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        message = payload["choices"][0]["message"]

        raw_tool_calls = message.get("tool_calls") or []
        tool_calls = [
            ToolCall(
                name=(tc.get("function", {}) or {}).get("name", ""),
                arguments=_coerce_arguments((tc.get("function", {}) or {}).get("arguments", {})),
            )
            for tc in raw_tool_calls
        ]
        return AssistantTurn(content=message.get("content") or None, tool_calls=tool_calls)


class FakeLLM(LLMClient):
    """Deterministic, scripted stand-in for a real model — for testing the Python-side loop only."""

    def __init__(self, scripted_turns: List[AssistantTurn]) -> None:
        self._turns = list(scripted_turns)
        self._index = 0

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        temperature: float,
    ) -> AssistantTurn:
        if self._index >= len(self._turns):
            return AssistantTurn(content="(FakeLLM ran out of scripted turns)")
        turn = self._turns[self._index]
        self._index += 1
        return turn


# ==============================================================================
# THE AGENTIC LOOP
# ==============================================================================


@dataclass
class QueryResult:
    answer: str
    iterations_used: int
    tool_calls_made: List[Tuple[str, Dict[str, Any]]] = field(default_factory=list)
    # 2026-09-14 addition: the actual result returned by each call in
    # tool_calls_made, same order, same length. Added after a batch run
    # (spotify) where two questions' final answers were the model
    # apologizing and printing a malformed, never-executed tool-call-shaped
    # JSON blob as plain text — without the underlying tool result (row
    # counts, or a real sql_error) captured anywhere, there was no way to
    # tell from the report alone whether the PRECEDING call had actually
    # errored (prompting that malformed retry) or returned data the model
    # just ignored. Kept separate from tool_calls_made rather than folded
    # into it, so existing tuple-unpacking call sites (`for name, args in
    # tool_calls_made`) keep working unchanged.
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    hit_max_iterations: bool = False
    # 2026-09-14 addition: how many times _try_parse_malformed_tool_call()
    # salvaged a call the model wrote as plain apology-plus-JSON text
    # instead of a real tool call (see that function's docstring). Almost
    # always 0; a nonzero value is a real signal about how often a given
    # model/backend needs this crutch, worth watching per-model in batch
    # reports rather than silently absorbing it.
    malformed_tool_call_recoveries: int = 0
    # [agente TL06] one entry per llm.chat() call of this run, same order as
    # the iterations: {"iteration", "prompt_eval_count",
    # "prompt_eval_duration"} — taken from the Ollama response (see
    # OllamaClient.chat()). Values are None on non-Ollama backends or when
    # the response lacks the fields; this per-call list sits next to
    # tool_calls_made/tool_results, which report the per-tool-call info.
    # Lets Leo check the system-prompt prefix cache (todo_table_routing_test.md).
    llm_calls: List[Dict[str, Any]] = field(default_factory=list)


def _canonical_call(name: str, arguments: Dict[str, Any]) -> Tuple[str, str]:
    """Stable key for loop-breaking: same tool + same args, order-independent."""
    return name, _compact_json({k: arguments[k] for k in sorted(arguments)})


def _extract_first_json_object(text: str) -> Optional[str]:
    """Balanced-brace scan for the first top-level {...} in text (not a regex,
    to avoid pathological backtracking on arbitrary model output)."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


# 2026-09-15 addition — see _try_parse_malformed_tool_call's docstring below.
# Narrow, tool-specific fallback for the one shape that keeps defeating
# strict json.loads in practice: a run_sql call whose embedded SQL string
# uses raw/unescaped double quotes for SQL string literals (e.g.
# `"query":"...WHERE domain = "bank"..."`) instead of `\"bank\"`. Requires
# the surrounding {"name": ..., "parameters"/"arguments": {"query": "..."}}
# shape to be present — ordinary prose containing a brace still won't match.
_MALFORMED_RUNSQL_RE = re.compile(
    r'"name"\s*:\s*"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"'
    r'.*?"(?:parameters|arguments)"\s*:\s*\{'
    r'.*?"query"\s*:\s*"(?P<query>.*)"'
    r'\s*\}+\s*$',
    re.DOTALL,
)


def _try_parse_malformed_tool_call(content: str) -> Optional[ToolCall]:
    """
    2026-09-14, added after a real spotify batch run: some models (observed
    with llama3.2:3b, twice in an 11-question batch, both times right after
    a genuine sql_error from a prior call) don't retry via a proper
    structured tool call once they realize a call went wrong — instead they
    write an apology plus a tool-call-shaped JSON blob as plain assistant
    TEXT, e.g. "Mi scuso per l'errore. Ecco una nuova query:
    {\"name\": \"run_sql\", \"parameters\": {\"query\": \"...\"}}". Without
    this, run_query() takes that text as the FINAL answer (turn.tool_calls
    is empty, so turn.is_final is True) and silently discards a call the
    model clearly intended to make — this was confirmed by hand: the
    preceding query in both real cases really had errored
    ({'error': 'sql_error', ...} from a genuine SQLite syntax error), so the
    model's instinct to retry was correct, only its output format was not.
    This looks for exactly that shape and, if found, salvages it into a
    real ToolCall so the loop can actually execute it instead of ending.
    Deliberately narrow — must parse as a JSON object, must name one of the
    3 real registered tools, must carry a dict of arguments under
    "parameters" or "arguments" — so ordinary prose that happens to contain
    a brace (e.g. discussing a table's columns) is not misread as a call.

    2026-09-15 addition — see the overnight cross-domain batch
    (batch_report_llama3.2_3b_overnight.json): the SAME shape appeared on
    the model's very FIRST turn (zero prior tool calls, zero prior errors)
    in 8 of 58 questions, not just as an error-retry — a much larger share
    than the 2/11 this recovery was originally built for. In all 8 real
    cases, the blob failed strict json.loads because the model's own
    embedded SQL used unescaped double quotes for SQL string literals
    (e.g. `"query":"...WHERE domain = "bank"..."`), sometimes inconsistently
    within the same blob (money_04: `\"income\"` escaped, `"bank"` not).
    Rather than attempt a general JSON repair (risking false positives),
    this adds one narrow regex fallback — _MALFORMED_RUNSQL_RE above — that
    only fires after strict parsing fails, only recognizes the exact
    {"name": ..., "parameters"/"arguments": {"query": "..."}} shape, and
    only extracts the tool name + raw query text (never attempts to
    interpret the rest of the blob as JSON). SQLite itself tolerates
    double-quoted string literals when they don't match a real column/table
    name, so the extracted query usually runs as-is; any accidentally
    doubly-escaped quotes (\\") are normalized back to a plain quote before
    being handed to run_sql.
    """
    if not content or "{" not in content:
        return None
    blob = _extract_first_json_object(content)
    if blob is None:
        return None
    try:
        parsed = json.loads(blob)
    except json.JSONDecodeError:
        match = _MALFORMED_RUNSQL_RE.search(blob)
        if match is None:
            return None
        name = match.group("name")
        if name not in TOOL_FUNCTIONS:
            return None
        # Normalize any run of backslashes immediately before a quote back to
        # a plain quote (observed inconsistently escaped within the SAME
        # blob — see money_04/money_12 in the docstring above, one escaped
        # correctly, one with a doubled backslash) and drop literal \n/\t
        # sequences a model sometimes writes instead of real whitespace.
        query_text = re.sub(r"\\+\"", '"', match.group("query"))
        query_text = query_text.replace("\\n", " ").replace("\\t", " ")
        if not query_text.strip():
            return None
        return ToolCall(name=name, arguments={"query": query_text})
    if not isinstance(parsed, dict):
        return None
    name = parsed.get("name")
    if not isinstance(name, str) or name not in TOOL_FUNCTIONS:
        return None
    arguments = parsed.get("parameters")
    if not isinstance(arguments, dict):
        arguments = parsed.get("arguments")
    if not isinstance(arguments, dict):
        arguments = {}
    return ToolCall(name=name, arguments=arguments)


def run_query(
    question: str,
    llm: LLMClient,
    max_iterations: int = MAX_ITERATIONS,
) -> QueryResult:
    """
    Runs the full agentic loop for one user question: the model either
    answers directly or calls run_sql (or, rarely, list_tables/
    describe_table); every tool call is validated before execution; an
    exact repeated call is short-circuited instead of re-executed; and if
    max_iterations is reached without a final answer, Python — never
    another model attempt — returns the last useful tool result with an
    explicit partial-answer caveat.
    """
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": question},
    ]

    tool_calls_made: List[Tuple[str, Dict[str, Any]]] = []
    tool_results: List[Dict[str, Any]] = []
    # [agente TL06] per llm.chat() call: iteration + Ollama prompt-eval
    # metrics (None-safe) — feeds QueryResult.llm_calls, used to check the
    # system-prompt prefix cache (see todo_table_routing_test.md).
    llm_calls: List[Dict[str, Any]] = []
    last_call_key: Optional[Tuple[str, str]] = None
    last_tool_result: Optional[Dict[str, Any]] = None
    malformed_recoveries = 0
    # 2026-09-15 UPDATE 2: which tables describe_table has actually been
    # called on (successfully) this conversation — see module docstring.
    # A run_sql call referencing a table not in this set is intercepted
    # below instead of being sent to SQLite.
    described_tables: set[str] = set()

    for iteration in range(1, max_iterations + 1):
        is_last_allowed_iteration = iteration == max_iterations
        turn = llm.chat(
            messages,
            tools=TOOL_SCHEMAS,
            temperature=FINAL_ANSWER_TEMPERATURE if not turn_expects_tool(messages) else TOOL_CALL_TEMPERATURE,
        )

        # [agente TL06] record this call's prompt-eval metrics. getattr with
        # a None default (instead of plain attribute access) keeps a
        # non-standard LLMClient subclass returning a leaner turn object
        # perfectly safe: missing field => None, never a crash.
        llm_calls.append({
            "iteration": iteration,
            "prompt_eval_count": getattr(turn, "prompt_eval_count", None),
            "prompt_eval_duration": getattr(turn, "prompt_eval_duration", None),
        })

        if turn.is_final:
            # See _try_parse_malformed_tool_call's docstring (2026-09-14):
            # some models write an intended retry as plain apology+JSON text
            # instead of a real tool call after seeing an error. Salvage
            # that into a real call before accepting this as the final
            # answer — only true prose (no parseable tool-call JSON inside)
            # ends the loop here.
            salvaged = _try_parse_malformed_tool_call(turn.content or "")
            if salvaged is None:
                return QueryResult(
                    answer=turn.content or "",
                    iterations_used=iteration,
                    tool_calls_made=tool_calls_made,
                    tool_results=tool_results,
                    malformed_tool_call_recoveries=malformed_recoveries,
                    llm_calls=llm_calls,  # [agente TL06]
                )
            malformed_recoveries += 1
            turn = AssistantTurn(content=turn.content, tool_calls=[salvaged])

        for call_index, call in enumerate(turn.tool_calls):
            # 2026-09-15 UPDATE 2: a stable id per call, threaded through
            # both the assistant's tool_calls entry and the matching
            # tool-role result message. Ollama's /api/chat never required
            # this (which is why it wasn't here before), but a real
            # OpenAI-compatible endpoint (TogetherAIClient) does expect
            # tool_call_id to line up — see _internal_messages_to_openai().
            tool_call_id = f"call_{iteration}_{call_index}"
            messages.append({
                "role": "assistant",
                "content": turn.content,
                "tool_calls": [{
                    "id": tool_call_id,
                    "type": "function",
                    "function": {"name": call.name, "arguments": call.arguments},
                }],
            })

            call_key = _canonical_call(call.name, call.arguments)
            if call_key == last_call_key:
                tool_result: Dict[str, Any] = {
                    "note": (
                        f"You already called {call.name} with these exact arguments and got the "
                        f"result above. Try different arguments, or answer with what you already have."
                    ),
                }
            elif call.name == "run_sql" and isinstance(call.arguments.get("query"), str) and (
                pending_tables := [
                    t for t in _extract_referenced_tables(call.arguments["query"])
                    if t not in described_tables
                ]
            ):
                # 2026-09-15 UPDATE 2 (see module docstring): mandatory
                # describe_table-before-run_sql gate — intercepted here,
                # before the query ever reaches SQLite, instead of relying
                # on the model reading the system-prompt instruction.
                tool_result = {
                    "error": "describe_table_required",
                    "message": (
                        f"This query references {', '.join(pending_tables)}, which you have "
                        f"not called describe_table on yet this conversation. Call "
                        f"describe_table for each of those tables first (to learn what the "
                        f"columns actually mean), then retry this exact query."
                    ),
                }
            else:
                try:
                    validate_tool_call(call.name, call.arguments)
                    tool_result = TOOL_FUNCTIONS[call.name](**call.arguments)
                    if call.name == "describe_table" and "error" not in tool_result:
                        described_tables.add(call.arguments.get("table"))
                except ToolValidationError as exc:
                    tool_result = {"error": "validation_error", "message": str(exc)}
                except DatasetUnavailableError as exc:
                    tool_result = {"error": "dataset_unavailable", "message": str(exc)}
                except Exception as exc:  # last-resort guard: one bad call must not crash the loop
                    tool_result = {"error": "tool_execution_error", "message": str(exc)}

            last_call_key = call_key
            last_tool_result = tool_result
            tool_calls_made.append((call.name, call.arguments))
            tool_results.append(tool_result)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": call.name,
                "content": _compact_json(tool_result),
            })

        if is_last_allowed_iteration:
            break

    fallback = (
        "I could not fully answer within the allotted number of tool calls. "
        "Here is the last relevant information I retrieved, which may be partial: "
        f"{_compact_json(last_tool_result) if last_tool_result else '(no tool result was obtained)'}"
    )
    return QueryResult(
        answer=fallback,
        iterations_used=max_iterations,
        tool_calls_made=tool_calls_made,
        tool_results=tool_results,
        hit_max_iterations=True,
        malformed_tool_call_recoveries=malformed_recoveries,
        llm_calls=llm_calls,  # [agente TL06]
    )


def turn_expects_tool(messages: List[Dict[str, Any]]) -> bool:
    """The first turn on a fresh question gets the low, structured-output temperature."""
    return not any(m.get("role") == "tool" for m in messages)


# ==============================================================================
# CLI — manual smoke-check against a real Ollama server, if one is running
# ==============================================================================

if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "What tables do you have data in, and how many rows does each have?"
    print(f"Q: {question}\n")
    result = run_query(question, llm=OllamaClient())
    print(f"A: {result.answer}\n")
    print(f"(iterations used: {result.iterations_used}, tool calls: {result.tool_calls_made})")
