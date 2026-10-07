# Prompt: migrate the "maps" domain (Google Maps Timeline / location history)

Use this as the opening message of a **new, dedicated session** on the Timelive_full
project (same pattern already used for chess.com, Spotify, money, instagram — one domain
per effort). Paste it as-is, or trim the parts that no longer apply once you've re-read the
project's current state.

---

## Task

Migrate the **maps** domain straight into the new single-SQLite (`vault.db`) architecture
used by `ingest_engine.py` — this domain was never on the old PRIMARY/FULL JSON system in
any real form, so there is no legacy `maps_ingest.py` to port, only a real export file that
has never been touched. Follow the same process already used for
`chessdotcom_ingest.py`/`spotify_ingest.py`/`money_ingest.py`/`instagram_ingest.py`.

## 0. Read before touching anything

In this order:
1. `timelive.md` — architecture, domain contract (§3), decision rules (§7 — data-first, no
   schema before real data), current migration state (§8).
2. `EVOLUTION_LOG.md` — specifically its **"Ordine dei prossimi domini deciso
   (2026-09-17)"** section (why Maps was picked first: already-exported, simplest of the
   remaining candidates) and its **"PayPal migrato in money_ingest.py"** section (most
   recent real-data-inspection discipline example — same rigor expected here: verify column
   names/fill rates/duplicate ids against the real file, don't assume).
3. `ingest_engine.py` — current engine (`ColumnSpec`/`TableSpec`, `upsert_rows`,
   `create_schema_for_table`'s automatic FK-child indexing, `ColumnSpec.sensitive`,
   `truncate_text()`).
4. `instagram_ingest.py` and `money_ingest.py` — reference implementations for style,
   `TableSpec` shape, `run_ingest(conn, dry_run, verbose)` entrypoint, module-docstring
   documentation of real-data findings (both are good examples of "REAL-DATA FINDING"-style
   inline documentation to match).

## 1. Real data — what's already known, verify the rest

The file is `Input/Maps/Timeline.json` (Google Maps Timeline / location history export,
~2.2MB as of 2026-09-17, 2,994 entries at last count — re-check both numbers, the user may
export again before you run this). Already confirmed by inspection (re-verify, don't just
trust this prompt):

- Top-level structure: a JSON **array** of entries, each with `startTime`/`endTime`
  (ISO 8601 with offset, e.g. `"2025-05-18T09:13:18.000+02:00"`) plus exactly one of three
  keys seen so far:
  - `"visit"`: a place the user stayed at — `hierarchyLevel`, `topCandidate`
    (`probability`, `semanticType` e.g. `"Unknown"`, `placeID`, `placeLocation` as a
    `"geo:<lat>,<lon>"` string), and a top-level `probability`.
  - `"activity"`: a movement segment — `probability`, `start`/`end` as `"geo:<lat>,<lon>"`
    strings, `topCandidate` (`type` e.g. `"walking"`, `probability`), `distanceMeters`.
  - `"timelinePath"`: seen in the key listing but **never actually sampled this session** —
    inspect its real shape before assuming it's a list of raw GPS breadcrumbs (likely, but
    unverified).
- **No native per-entry id anywhere in the sample** — dedup key will need to be composed
  (e.g. `startTime + endTime + entry-type + a hash of the type-specific payload`), the same
  kind of problem money_ingest.py solved for meinElba (no native id) with a composite
  dedup_key. Check for real collisions before picking the composite (same discipline as
  Spotify's 701-collision check, PayPal's 16-collision check).
- **IMPORTANT — the user has explicitly said this export is NOT a complete history**: his
  real location data only goes back roughly one year. Missing older history is an export
  limitation, not a parsing bug — don't go looking for a "missing file" that doesn't exist,
  and don't flag data-completeness gaps before ~1 year ago as a problem to solve.
- `placeID`/`semanticType` suggest Google's own place-recognition data is present but weakly
  resolved (`"Unknown"` in the one sample checked) — verify how often `semanticType` is
  actually meaningful vs. always `"Unknown"` before deciding whether it's worth a column at
  all (same "don't invent, don't guess" standard as everywhere else in this project).

## 2. Design questions to raise with the user before finalizing the schema

- **One table vs. several.** `visit`/`activity`/`timelinePath` look like genuinely different
  shapes (a place-visit vs. a movement segment vs. a raw path) — same kind of split decision
  Trade Republic needed (3 tables) rather than forcing one flat table. Propose a concrete
  split once you've seen real counts/shapes of all three entry kinds, and confirm it with the
  user.
- **Privacy.** Location history is a step up in sensitivity from anything except maybe
  Instagram DMs/PayPal's `messaggio` — home address, workplace, and travel patterns are all
  directly derivable from this data. Surface this explicitly and ask whether any handling
  beyond the existing `ColumnSpec.sensitive` marker is wanted (e.g. should raw
  lat/lon ever be rounded/generalized? Precedent so far in this project is "keep native,
  mark sensitive" — not silent lossy transformation — but ask rather than assume for this
  domain specifically, since it's more re-identifying than most).
- **Re-export behavior.** Does a fresh Google Takeout / Timeline export always cover the
  full retained history from scratch (making dedup-by-composite-key sufficient on re-ingest),
  or could it be a rolling/incremental export where re-running loses entries no longer in the
  latest file? Ask the user how they expect to refresh this domain's data over time before
  assuming full-history re-ingest is always safe.
- **`geo:` string parsing.** Decide whether to store latitude/longitude as two REAL columns
  (queryable, matches how the rest of this project prefers structured columns over embedded
  strings) or keep the native `"geo:<lat>,<lon>"` string as-is with parsed REAL columns
  alongside it (native-value-preservation precedent, e.g. PayPal's `category_raw` kept
  alongside derived fields) — this is a real, worth-asking design choice, not a detail to
  decide alone.

## 3. Explicitly OUT of scope for this session

The user has a separate, **already-parked** idea about a shared cross-domain "places /
locations" layer (something like the already-planned people/contacts layer, but for
locations) that multiple domains could reference via FK instead of each domain keeping its
own isolated raw coordinates. **Do not build this as part of the Maps migration** — it was
explicitly deferred as a separate task in the 2026-09-17 session that produced this prompt.
If Maps' natural table design happens to make a later shared-locations layer easier to bolt
on, that's a fine side effect, but it is not a goal to design toward now — avoid premature
complexity, same standard as everywhere else in this project. Do not modify `timelive.md`
to introduce this pattern in this session; that's part of the separate, not-yet-scheduled
task.

## 4. Build and test (same discipline as every prior migration)

- Write `maps_ingest.py` mirroring `instagram_ingest.py`'s/`money_ingest.py`'s structure:
  module docstring documenting every real-data finding and design decision, `TableSpec`(s)
  with `dedup_key_column`, `canonical_timestamp_column`, `foreign_keys` set correctly if
  more than one table.
- Register the domain in `ingest_engine.py`'s `DOMAIN_REGISTRY` and remove `"maps"` from
  `_PLANNED_DOMAINS`'s "not yet migrated" list once it's real.
- Build a sandbox test harness (stage the real file, point a test `config.py` at it and a
  scratch in-memory `vault.db`) and actually run the ingest — don't just write it.
- **Run it twice in a row** to confirm idempotency (second run: 0 new rows, no errors, no
  hangs), `PRAGMA integrity_check` = ok, zero FK violations if multiple tables are linked.
- Sanity-check the LLM bridge against the populated test `vault.db` (list_tables,
  describe_table, a few run_sql queries) before handing anything to the user for a real Pi
  test.
- **Re-measure `build_system_prompt()`'s token cost** after adding maps' table(s) — the
  2026-09-17 session measured ~2,317 tokens for the current 16-table/4-domain compact index;
  note the new total after maps is added (useful real data point for the still-open Task 3
  scalability question, even though solving that question is not this session's job).

## 5. What NOT to do

- Don't touch `chessdotcom_ingest.py`/`spotify_ingest.py`/`money_ingest.py`/
  `instagram_ingest.py` unless a genuinely shared bug or improvement is found — and if you
  do, say so explicitly and explain why it's shared rather than maps-specific.
- Don't mark `timelive.md` §8 as done for maps until the user has validated it on the real
  Pi.
- Don't build the shared places/locations layer (see §3 above) — separately parked, not this
  session's scope.
- Don't assume `Timeline.json`'s current 2,994-entry/2.2MB shape is still accurate — re-check
  both numbers against the live file, the user may have re-exported since this prompt was
  written.

## 6. Communication style

Be critical, not assertive. Ask as many questions as needed before finalizing any decision
that's genuinely debatable (table split, privacy handling, geo-string parsing, dedup-key
composition) — don't guess and present it as settled. Work incrementally and surface
intermediate real-data findings before writing the full schema, same as every prior
migration in this project.

---

**After Maps**: the agreed next domain is **WhatsApp** (`Input/Whatsapp/`, 11 real chat
exports, already inspected at a high level in the 2026-09-17 session — see
EVOLUTION_LOG.md's "Ordine dei prossimi domini deciso" section). Don't start it in this
session; just don't be surprised it's next.
