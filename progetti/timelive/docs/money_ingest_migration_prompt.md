# Prompt: migrate the "money" domain (bank + investments + private markets)

Use this as the opening message of a **new, dedicated session** on the Timelive_full
project (same pattern already used for chess.com and Spotify — one domain per effort).
Paste it as-is, or trim the parts that no longer apply once you've re-read the project's
current state.

---

## Task

Migrate the **money** domain from the old PRIMARY/FULL JSON architecture
(`money_ingest.py` + `main.py`) to the new single-SQLite (`vault.db`) architecture used by
`ingest_engine.py`, following the exact same process already used for `chessdotcom_ingest.py`
and `spotify_ingest.py`.

This domain is explicitly flagged by the user as more complex and higher-stakes than the
previous two: it covers **banking, investments, and private markets** — "tante cose" (lots
of stuff). Go slower and ask more questions than you did for Spotify, not fewer.

## 0. Read before touching anything

In this order:
1. `timelive.md` — architecture, domain contract, §7 decision rules (data-first, no schema
   before real data), §8 current migration state.
2. `EVOLUTION_LOG.md` — real bugs and decisions already made for chess.com and Spotify; don't
   rediscover them.
3. `ingest_engine.py` — current engine. Note it already has: `extra_indexed_columns` on
   `TableSpec`, and **automatic indexing of every `foreign_keys` child column** in
   `create_schema_for_table` (added after a real performance bug on Spotify — a domain with
   many rows and a session/grouping table WILL hit this if it's missing, so this is not
   optional to preserve).
4. `spotify_ingest.py` and `chessdotcom_ingest.py` — reference implementations for style,
   `TableSpec` shape, `run_ingest(conn, dry_run, verbose)` entrypoint, notability scoring
   pattern, module-docstring documentation of real-data findings.
5. `llm_bridge.py` — the 3-tool bridge (list_tables/describe_table/run_sql) that will query
   whatever you build. Note `OLLAMA_NUM_CTX = 8192` was just added because the system prompt
   (which embeds the full schema of every registered table) already measured ~3,460 tokens
   with only 2 domains migrated. Money will likely add several tables with many columns —
   **re-measure the system prompt size after migration** and raise `OLLAMA_NUM_CTX` further
   if needed, or consider whether `describe_table` should stay the only place full column
   lists live (i.e. keep semantic notes in the system prompt short).
6. `money_ingest.py` (old) — the current domain logic to migrate. As of this writing it
   recognizes exactly three sources (meinElba/Raiffeisen, Trade Republic, Banca Sella) plus a
   generic fallback parser, with a `domain="bank"` vs `domain="investment"` split, native-id
   priority dedup, a strict "never invent a category" classification policy, ISIN extraction,
   recurring-transaction/refund-pairing detection, and anomaly z-score flagging.

**Important:** the old `money_ingest.py` has no concept of "private markets" at all. The user
mentioned it explicitly — do not assume it's just another investment source shaped like Trade
Republic. Find the real files first (ask the user where they are if not obvious from
`config.py` / the input folder) and inspect them before assuming anything about their shape,
fields, or how they relate (or don't relate) to the existing bank/investment tables.

## 1. Real data first (timelive.md §7 — non-negotiable)

Before writing a single `TableSpec`:
- Locate and inspect the **real** export files for all three sub-areas (bank, public-market
  investments, private markets) — actual files from the user's input folder, not the old
  code's assumptions about them.
- For private markets specifically: ask the user what the source actually is (a broker
  export? a manually maintained file? PDF statements?) if it's not obvious, since nothing in
  the codebase currently handles it.
- Check real value distributions before picking any threshold (recurring-transaction
  matching windows, anomaly z-score cutoffs, session/grouping gaps if any grouping concept
  applies here) — don't reuse the old file's constants without re-validating them against
  real numbers, the same way Spotify's session gap was re-validated against real percentile
  data rather than assumed.

## 2. Design questions to raise with the user before finalizing the schema

Ask these explicitly (via AskUserQuestion or in plain text) rather than deciding alone —
this mirrors how ip_addr exclusion and the Spotify dedup-key semantics were decided:

- **Multiple TableSpecs vs one.** timelive.md §3 explicitly allows a domain to declare
  multiple tables when concepts differ in shape. Bank transactions, investment
  holdings/positions, and private-market positions are almost certainly different shapes
  (e.g. a transaction has amount+direction+counterparty; a position has quantity+instrument+
  valuation date). Propose a concrete table split once you've seen the real data, and confirm
  it with the user rather than forcing everything into one flat `transactions` table like the
  old system did.
- **Field-level privacy.** This domain is a step up in sensitivity from anything migrated so
  far (Spotify's only precedent was excluding `ip_addr`). Before including any of: IBANs /
  account numbers / account references, native transaction ids, running balances, exact
  amounts, counterparty names, or anything from private-market statements — surface the list
  of candidate fields to the user and ask which should be excluded, generalized (e.g. IBAN
  last-4 instead of full IBAN), or included as-is. Remember `vault.db` is directly queryable
  by a cloud LLM (`ClaudeAPIClient`) once the bridge is pointed at it — this is a real
  exposure surface, not a theoretical one.
- **Dedup key design.** Prefer native transaction ids per source when the source provides
  one (Trade Republic has `transaction_id`; Sella has "Codice identificativo"). For sources
  without a reliable native id (meinElba, generic fallback, and whatever private-markets
  turns out to be), check for dedup collisions against real data the same way Spotify's 701
  colliding records were found — and ask the user how to resolve any that turn up, rather
  than silently merging or silently splitting. Carry forward the general principle from
  Spotify: never silently drop or merge records that only "look like" duplicates.
- **Category policy.** The old file's "never invent a category absent a native signal" rule
  is worth keeping — confirm with the user if you find real data that seems to need it
  relaxed.

## 3. Build and test (same discipline as Spotify)

- Write `money_ingest.py` mirroring `spotify_ingest.py`'s structure: module docstring
  documenting every real-data finding and design decision, `TableSpec`(s) with
  `dedup_key_column`, `canonical_timestamp_column`, `foreign_keys` set correctly (so the
  engine's automatic FK-index fix applies), `run_ingest(conn, dry_run, verbose)`.
- Register the domain in `ingest_engine.py`'s `DOMAIN_REGISTRY`.
- Build a sandbox test harness (stage real files, point a test `config.py` at them and a
  scratch `vault.db`) and actually run the ingest — don't just write it.
- **Run it twice in a row.** This is how both chess.com bugs and Spotify's FK-index hang were
  found. Confirm idempotency (second run: 0 new rows for unchanged input, no errors, no
  hangs), `PRAGMA integrity_check` = ok, zero FK violations.
- Sanity-check the LLM bridge against the populated test `vault.db` (list_tables,
  describe_table, a few run_sql queries) before handing anything to the user for a real Pi
  test.

## 4. What NOT to do

- Don't touch `spotify_ingest.py` or `chessdotcom_ingest.py` unless a genuinely shared bug or
  improvement is found (as happened with the FK-index fix and `llm_bridge.py`'s `num_ctx`
  fix this session) — and if you do, say so explicitly and explain why it's shared rather than
  money-specific.
- Don't mark `timelive.md` §8 as done for money until the user has validated it on the real
  Pi, same as chess.com and Spotify.
- Don't finalize `SQL_ROW_LIMIT` / `SQL_TIMEOUT_SECONDS` in `llm_bridge.py` based on this
  domain alone — those are still explicitly waiting on real usage data across domains.
- Don't assume the three-source list (meinElba, Trade Republic, Sella) is complete, and don't
  assume private markets fits any existing pattern until you've actually seen the files.

## 5. Communication style

Be critical, not assertive. Ask as many questions as needed before finalizing any decision
that's genuinely debatable (schema shape, field inclusion/exclusion, dedup semantics,
thresholds) — don't guess and present it as settled. Work incrementally and surface
intermediate real-data findings (e.g. "found N files, here's what fields they actually
contain, here's what I'm proposing") before writing the full schema.
