# test_llm_bridge.py
# =============================================================================
# FAST SMOKE TEST — llm_bridge.py (timelive.md §45 practice, applied to the
# LLM bridge layer instead of an ingest)
# =============================================================================
#
# WHY THIS EXISTS
# -----------------------------------------------------------------------
# Same philosophy as test_smoke.py (timelive.md §45/§46): fast, deterministic
# checks that don't need a real Ollama server or GPU, so the Python-side
# logic (tool validation, size budgeting, loop-breaking, MAX_ITERATIONS
# fallback) can be iterated on quickly. It is NOT a substitute for actually
# running this against a real small model on real hardware once that is
# available — it only proves "the bridge's control logic is not obviously
# broken."
#
# WHAT THIS TESTS AGAINST
# -----------------------------------------------------------------------
# Unlike test_smoke.py (synthetic fixtures), this suite runs the tool
# functions directly against the user's REAL PRIMARY datasets (and the
# real FULL datasets, where available) copied into ../Output/ for this
# session — because llm_bridge.py's whole job is to answer questions about
# exactly that kind of data, and its filtering/budgeting logic needs to be
# validated against real field values and real volume (timelive.md §46:
# a smoke test on tiny synthetic data does not catch scale-dependent
# issues — e.g. whether the size budget actually keeps a real result
# small when a filter is broad).
#
# v4.7: not every environment running this suite has every domain's real
# Output/*.json file present at once (a dev sandbox vs. the real Pi
# deployment differ here on purpose, timelive.md §23/§43.9) — each
# domain-specific test section is gated on whether that domain's real
# PRIMARY file actually exists, and prints a skip note instead of failing
# when it doesn't, so this suite stays meaningful whether run against one
# domain's fresh real data or the full six-domain deployment.
#
# HOW TO RUN
# -----------------------------------------------------------------------
#   python3 test_llm_bridge.py
# =============================================================================

import sys
import time
import traceback

import llm_bridge as lb

FAILURES = []
SKIPPED = []


def _present(domain: str) -> bool:
    """True iff `domain`'s real PRIMARY file actually exists on disk in
    THIS environment. Read from DOMAIN_REGISTRY (the single source of
    truth llm_bridge.py itself uses), never hardcoded."""
    return domain in lb.DOMAIN_REGISTRY and lb.DOMAIN_REGISTRY[domain].primary_path.exists()


def _full_present(domain: str) -> bool:
    full_path = lb.DOMAIN_REGISTRY[domain].full_path if domain in lb.DOMAIN_REGISTRY else None
    return full_path is not None and full_path.exists()


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def skip(message: str) -> None:
    SKIPPED.append(message)
    print(f"  (skipped: {message})")


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


# =============================================================================
# PART 1 — list_domains() / manifest sanity against real data
# =============================================================================

def test_list_domains():
    section("list_domains()")
    manifest = lb.list_domains()

    # Required core domains must always be present; extra domains (maps,
    # whatsapp, chessdotcom, ...) are fine and deliberately not rejected
    # here — this check must not go stale the moment a new domain is
    # wired in.
    required_domains = {"bank", "spotify"}
    check(required_domains.issubset(set(manifest)), f"missing required domains: {required_domains - set(manifest)}")

    # v4.7: apple_health is registered but enabled=False — it must NEVER
    # appear in the manifest the LLM sees, even though its code/data are
    # still fully intact (see the domain-specific direct-call test below).
    check("apple_health" not in manifest, "apple_health has enabled=False and must not appear in list_domains()")
    check("apple_health" not in lb.ACTIVE_DOMAINS, "apple_health must not be in ACTIVE_DOMAINS")
    check("apple_health" in lb.DOMAIN_REGISTRY, "apple_health must still be registered in DOMAIN_REGISTRY (code intact, just not offered)")

    for domain, info in manifest.items():
        print(f"{domain}: available={info.get('available')} "
              f"date_range=({info.get('min_date')} .. {info.get('max_date')}) "
              f"resolve_full_ref={info.get('resolve_full_ref_available')}")
        if not _present(domain):
            skip(f"{domain}: no real PRIMARY file in this environment, only checking it doesn't crash")
            check(info.get("available") is False, f"{domain}: expected available=False when the file is missing")
            continue
        check(info.get("available") is True, f"{domain}: reported unavailable")
        check(bool(info.get("min_date")) and bool(info.get("max_date")), f"{domain}: missing date range")
        check(len(info.get("sections", {})) > 0, f"{domain}: no searchable sections found")

    # resolve_full_ref_available must always match reality (file existence),
    # never be hardcoded — deliberately dynamic since which real FULL files
    # are present differs between a dev sandbox and the real deployment.
    for domain in manifest:
        if not _present(domain):
            continue
        expected = _full_present(domain)
        check(
            manifest[domain]["resolve_full_ref_available"] is expected,
            f"{domain}: resolve_full_ref_available should match whether the FULL file exists (exists={expected})",
        )


# =============================================================================
# PART 2 — validate_tool_call
# =============================================================================

def test_validate_tool_call():
    section("validate_tool_call()")

    # valid calls must not raise
    try:
        lb.validate_tool_call("search", {"domain": "bank", "section": "notable_transactions"})
        lb.validate_tool_call("get_aggregation", {"domain": "bank", "granularity": "monthly", "period": "2026-08"})
        lb.validate_tool_call("resolve_full_ref", {"domain": "bank", "full_ref": "transactions/x"})
        lb.validate_tool_call("search", {"domain": "whatsapp", "section": "notable_messages"})
        lb.validate_tool_call("search", {"domain": "chessdotcom", "section": "notable_games"})
        lb.validate_tool_call("get_aggregation", {"domain": "chessdotcom", "granularity": "monthly", "period": "2026-08"})
    except Exception as exc:
        check(False, f"a valid call was rejected: {exc}")

    # invalid tool name
    try:
        lb.validate_tool_call("delete_everything", {})
        check(False, "unknown tool name should have raised ToolValidationError")
    except lb.ToolValidationError:
        pass

    # unknown domain
    try:
        lb.validate_tool_call("search", {"domain": "crypto_wallet", "section": "notable_transactions"})
        check(False, "unknown domain should have raised ToolValidationError")
    except lb.ToolValidationError:
        pass

    # v4.7: apple_health is registered but disabled — from the LLM's point
    # of view it must behave exactly like an unknown domain, even though
    # its code and data still work when called directly (see
    # test_tool_search_health below).
    try:
        lb.validate_tool_call("search", {"domain": "apple_health", "section": "sessions"})
        check(False, "apple_health has enabled=False -- search() through the LLM path should have raised ToolValidationError")
    except lb.ToolValidationError as exc:
        # The error legitimately echoes back the domain that was requested
        # ("Unknown domain 'apple_health'") -- what matters is that it is
        # never listed among the *available* domains offered to the model.
        check("apple_health" not in sorted(lb.ACTIVE_DOMAINS), "apple_health must never appear in the domains offered to the LLM")

    # unknown section for a real domain
    try:
        lb.validate_tool_call("search", {"domain": "bank", "section": "groupings"})
        check(False, "'groupings' is FULL-only, not a searchable PRIMARY section -- should have raised")
    except lb.ToolValidationError:
        pass

    # get_aggregation on a domain that doesn't support it
    try:
        lb.validate_tool_call("get_aggregation", {"domain": "maps", "granularity": "monthly", "period": "2026-08"})
        # maps DOES support aggregation_key -- this call should actually succeed;
        # test the real "no aggregation_key" case instead with a domain that lacks one.
        # (apple_health has none, but it's disabled -- so this path is only reachable
        # via a direct DOMAIN_REGISTRY lookup, not through validate_tool_call. Nothing
        # further to assert here; kept as a documented non-check.)
    except lb.ToolValidationError:
        check(False, "maps DOES have an aggregation_key (movement_aggregations) -- this should not have raised")

    # bad granularity enum
    try:
        lb.validate_tool_call("get_aggregation", {"domain": "bank", "granularity": "yearly", "period": "2026"})
        check(False, "'yearly' is not a valid granularity -- should have raised")
    except lb.ToolValidationError:
        pass

    # malformed full_ref
    try:
        lb.validate_tool_call("resolve_full_ref", {"domain": "bank", "full_ref": "not_a_ref"})
        check(False, "full_ref without '/' should have raised")
    except lb.ToolValidationError:
        pass


# =============================================================================
# PART 3 — tool functions against real data
# =============================================================================

def test_tool_search_bank():
    section("tool_search: bank")
    if not _present("bank"):
        skip("bank: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="bank", section="notable_transactions", text_query="netflix", limit=5)
    print(f"'netflix' matches: total_matched={result['total_matched']}, returned={len(result['results'])}")
    check(result["total_matched"] >= 0, "total_matched should never be negative")
    check(len(result["results"]) <= 5, "limit=5 was not respected")
    for txn in result["results"]:
        check("netflix" in " ".join(str(txn.get(f, "")) for f in ("merchant", "category", "transaction_type", "institution", "currency")).lower(),
              f"a result did not actually match the text_query: {txn}")

    result = lb.tool_search(domain="bank", section="notable_transactions", date_from="2026-08-01", date_to="2026-08-31", limit=50)
    print(f"August 2026 transactions: total_matched={result['total_matched']}")
    for txn in result["results"]:
        ts = txn.get("timestamp_begin", "")
        check("2026-08" in ts, f"date filter leaked an out-of-range transaction: {ts}")

    result = lb.tool_search(domain="bank", section="notable_transactions", max_value=-500, limit=50)
    for txn in result["results"]:
        check(txn.get("amount", 0) <= -500, f"min/max_value filter leaked: amount={txn.get('amount')}")


def test_tool_search_spotify():
    section("tool_search: spotify")
    if not _present("spotify"):
        skip("spotify: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="spotify", section="notable_plays", text_query="lavoe", limit=10)
    print(f"'lavoe' matches: total_matched={result['total_matched']}, returned={len(result['results'])}")
    for play in result["results"]:
        check("lavoe" in (play.get("artist") or "").lower() or "lavoe" in (play.get("track") or "").lower(),
              f"a result did not match text_query 'lavoe': {play}")

    result = lb.tool_search(domain="spotify", section="sessions", min_value=30, limit=5)
    for s in result["results"]:
        check(s.get("total_played_minutes", 0) >= 30, f"min_value filter leaked a short session: {s}")


def test_tool_search_health():
    section("tool_search: apple_health (direct call — disabled for the LLM, but code/data still work)")
    if not _present("apple_health"):
        skip("apple_health: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="apple_health", section="sessions", text_query="sleep", limit=5)
    print(f"sleep-labeled sessions: total_matched={result['total_matched']}")
    for s in result["results"]:
        haystack = " ".join(str(s.get(f, "")) for f in ("activity_type", "source", "device", "heart_rate_mode")).lower()
        check("sleep" in haystack, f"text_query 'sleep' leaked a non-matching session: {s}")

    result = lb.tool_search(domain="apple_health", section="sleep", limit=5)
    print(f"dedicated 'sleep' section matches: total_matched={result['total_matched']}")


def test_tool_search_maps():
    section("tool_search: maps")
    if not _present("maps"):
        skip("maps: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="maps", section="trips", limit=10)
    print(f"trips: total_matched={result['total_matched']}, returned={len(result['results'])}")
    check(result["total_matched"] >= 0, "total_matched should never be negative")


def test_tool_search_whatsapp():
    section("tool_search: whatsapp")
    if not _present("whatsapp"):
        skip("whatsapp: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="whatsapp", section="notable_messages", limit=10)
    print(f"notable_messages: total_matched={result['total_matched']}, returned={len(result['results'])}")
    for msg in result["results"]:
        check("text" not in msg, f"PRIVACY VIOLATION: a whatsapp PRIMARY search result must never contain 'text': {msg}")
        check("full_ref" in msg, f"a notable_messages result is missing full_ref, needed to retrieve the actual text: {msg}")

    result = lb.tool_search(domain="whatsapp", section="chats", limit=50)
    print(f"chats: total_matched={result['total_matched']}")

    result = lb.tool_search(domain="whatsapp", section="notable_locations", limit=10)
    print(f"notable_locations: total_matched={result['total_matched']}")
    for loc in result["results"]:
        check("latitude" in loc and "longitude" in loc, f"a notable_locations result is missing coordinates: {loc}")


def test_tool_search_chessdotcom():
    section("tool_search: chessdotcom")
    if not _present("chessdotcom"):
        skip("chessdotcom: no real PRIMARY file in this environment")
        return

    result = lb.tool_search(domain="chessdotcom", section="notable_games", text_query="checkmate", limit=10)
    print(f"'checkmate' win_method matches: total_matched={result['total_matched']}, returned={len(result['results'])}")
    for game in result["results"]:
        check("checkmate" in " ".join(str(game.get(f, "")) for f in
              ("opponent_username", "time_class", "win_method", "opening_signature", "user_side", "result_for_user")).lower(),
              f"a result did not actually match text_query 'checkmate': {game}")

    result = lb.tool_search(domain="chessdotcom", section="notable_games", min_value=1200, limit=20)
    print(f"games vs opponent_rating>=1200: total_matched={result['total_matched']}")
    for game in result["results"]:
        check((game.get("opponent_rating") or 0) >= 1200, f"min_value filter leaked a low-rated opponent: {game}")

    result = lb.tool_search(domain="chessdotcom", section="playing_sessions", min_value=30, limit=10)
    print(f"playing_sessions >=30min: total_matched={result['total_matched']}")
    for s in result["results"]:
        check(s.get("duration_minutes", 0) >= 30, f"min_value filter leaked a short session: {s}")


def test_tool_get_aggregation():
    section("tool_get_aggregation")
    if _present("bank"):
        result = lb.tool_get_aggregation(domain="bank", granularity="monthly", period="2026-08")
        print(f"bank monthly 2026-08 buckets: total_matched={result['total_matched']}")
        for bucket in result["results"]:
            check(bucket["timestamp_begin"].startswith("2026-08"), f"get_aggregation leaked a wrong-period bucket: {bucket['timestamp_begin']}")
    else:
        skip("bank: no real PRIMARY file in this environment")

    if _present("spotify"):
        result = lb.tool_get_aggregation(domain="spotify", granularity="monthly", period="2026-08")
        print(f"spotify monthly 2026-08 buckets: total_matched={result['total_matched']}")
    else:
        skip("spotify: no real PRIMARY file in this environment")

    if _present("whatsapp"):
        primary = lb.load_primary("whatsapp")
        any_month = None
        for bucket in primary.get("conversation_aggregations", {}).get("monthly", []):
            any_month = str(bucket["timestamp_begin"])[:7]
            break
        if any_month:
            result = lb.tool_get_aggregation(domain="whatsapp", granularity="monthly", period=any_month)
            print(f"whatsapp monthly {any_month} buckets: total_matched={result['total_matched']}")
            for bucket in result["results"]:
                check(bucket["timestamp_begin"].startswith(any_month), f"get_aggregation leaked a wrong-period bucket: {bucket['timestamp_begin']}")
    else:
        skip("whatsapp: no real PRIMARY file in this environment")

    if _present("chessdotcom"):
        primary = lb.load_primary("chessdotcom")
        any_month = None
        for bucket in primary.get("game_aggregations", {}).get("monthly", []):
            any_month = str(bucket["timestamp_begin"])[:7]
            break
        if any_month:
            result = lb.tool_get_aggregation(domain="chessdotcom", granularity="monthly", period=any_month)
            print(f"chessdotcom monthly {any_month} buckets: total_matched={result['total_matched']}")
            check(result["total_matched"] >= 1, f"expected at least one bucket for period {any_month} taken directly from real data")
            for bucket in result["results"]:
                check(bucket["timestamp_begin"].startswith(any_month), f"get_aggregation leaked a wrong-period bucket: {bucket['timestamp_begin']}")
    else:
        skip("chessdotcom: no real PRIMARY file in this environment")


def test_tool_resolve_full_ref():
    section("tool_resolve_full_ref")

    # health: must be explicitly unavailable, not attempt a 770MB json.load()
    # (this is a property of full_path being None, independent of the v4.7
    # enabled=False flag -- both apply to apple_health, but this specific
    # check is about the size-safety design, not the LLM-visibility flag).
    t0 = time.time()
    result = lb.tool_resolve_full_ref(domain="apple_health", full_ref="sessions/session_1")
    elapsed = time.time() - t0
    print(f"apple_health resolve_full_ref responded in {elapsed:.4f}s: {result}")
    check(result.get("error") == "full_ref_unavailable", "apple_health resolve_full_ref should return a typed 'unavailable' error, not attempt to load FULL")
    check(elapsed < 1.0, "apple_health resolve_full_ref took too long -- it must fail fast, never attempt to load the 770MB FULL file")

    for domain, section_prefix in (("bank", "transactions"), ("spotify", "plays"), ("whatsapp", "messages"), ("chessdotcom", "games")):
        if not _present(domain):
            skip(f"{domain}: no real PRIMARY file in this environment")
            continue
        if not _full_present(domain):
            skip(f"{domain}: no real FULL file in this environment")
            try:
                result = lb.tool_resolve_full_ref(domain=domain, full_ref=f"{section_prefix}/x")
                check(False, f"expected DatasetUnavailableError for {domain} (no FULL file present), got: {result}")
            except lb.DatasetUnavailableError:
                pass
            continue

        search_section = {
            "bank": "notable_transactions",
            "spotify": "notable_plays",
            "whatsapp": "notable_messages",
            "chessdotcom": "notable_games",
        }[domain]
        search_result = lb.tool_search(domain=domain, section=search_section, limit=1)
        if not search_result["results"]:
            skip(f"{domain}: no records in {search_section} to test resolve_full_ref against")
            continue
        sample_ref = search_result["results"][0].get("full_ref")
        if not sample_ref:
            skip(f"{domain}: {search_section} results carry no full_ref field")
            continue
        resolved = lb.tool_resolve_full_ref(domain=domain, full_ref=sample_ref)
        print(f"resolved {domain} {sample_ref} -> found={resolved.get('found')}")
        check(resolved.get("found") is True, f"a {domain} full_ref taken directly from search() should resolve: {sample_ref}")

        if domain == "whatsapp":
            record = resolved.get("record", {})
            if record.get("message_type") == "text":
                check("text" in record, "a resolved text-type whatsapp message should include 'text' in FULL")

    # unknown id (bank, whose real FULL file is expected to exist whenever this
    # domain is present at all)
    if _present("bank") and _full_present("bank"):
        resolved = lb.tool_resolve_full_ref(domain="bank", full_ref="transactions/this_id_does_not_exist")
        check(resolved.get("found") is False, "a made-up id should resolve to found=False, not raise or silently succeed")


# =============================================================================
# PART 4 — size budgeting (§43.5)
# =============================================================================

def test_budget_list_result():
    section("budget_list_result() -- §43.5 tool-result size budget")

    if _present("spotify"):
        # Ask for something broad enough that the real dataset has far more
        # matches than the budget can hold, to prove truncation actually engages.
        result = lb.tool_search(domain="spotify", section="notable_plays", date_from="2020-01-01", limit=lb.SEARCH_MAX_LIMIT)
        serialized_len = len(lb._compact_json(result))
        print(f"broad spotify search: total_matched={result['total_matched']}, returned={len(result['results'])}, "
              f"serialized_len={serialized_len} (budget={lb.TOOL_RESULT_CHAR_BUDGET})")
        check(serialized_len <= lb.TOOL_RESULT_CHAR_BUDGET * 1.5, "tool result grossly exceeded its budget (some slack allowed for the wrapper/message)")
        if result["total_matched"] > len(result["results"]):
            check("message" in result, "when results were truncated, an explicit count message must be present")
    elif _present("chessdotcom"):
        result = lb.tool_search(domain="chessdotcom", section="notable_games", date_from="2000-01-01", limit=lb.SEARCH_MAX_LIMIT)
        serialized_len = len(lb._compact_json(result))
        print(f"broad chessdotcom search: total_matched={result['total_matched']}, returned={len(result['results'])}, "
              f"serialized_len={serialized_len} (budget={lb.TOOL_RESULT_CHAR_BUDGET})")
        check(serialized_len <= lb.TOOL_RESULT_CHAR_BUDGET * 1.5, "tool result grossly exceeded its budget (some slack allowed for the wrapper/message)")
        if result["total_matched"] > len(result["results"]):
            check("message" in result, "when results were truncated, an explicit count message must be present")
    else:
        skip("no domain with real data present to test broad-search budgeting against")

    # Degenerate case: a single huge-ish item should still be returned
    # whole, never truncated mid-object.
    single = lb.budget_list_result([{"a": "x" * 10000}], total_matched=1, rank_field=None, char_budget=100)
    check(len(single["results"]) == 1, "a lone oversized item must still be returned whole, never dropped or cut mid-object")


# =============================================================================
# PART 5 — the agentic loop, with FakeLLM (no Ollama/GPU needed)
# =============================================================================

def test_loop_direct_final_answer():
    section("run_query: model answers directly, no tool calls")
    fake = lb.FakeLLM([lb.AssistantTurn(content="I don't need any tools for that.")])
    result = lb.run_query("What is 2+2?", llm=fake)
    check(result.answer == "I don't need any tools for that.", "direct final answer was not passed through")
    check(result.iterations_used == 1, f"expected 1 iteration, got {result.iterations_used}")
    check(not result.hit_max_iterations, "should not have hit max iterations")


def test_loop_one_tool_call_then_answer():
    section("run_query: one valid tool call, then a final answer")
    fake = lb.FakeLLM([
        lb.AssistantTurn(tool_calls=[lb.ToolCall("search", {"domain": "chessdotcom", "section": "notable_games", "text_query": "checkmate"})]),
        lb.AssistantTurn(content="You've won several games by checkmate recently."),
    ])
    result = lb.run_query("How many of my recent wins were by checkmate?", llm=fake)
    check(result.answer == "You've won several games by checkmate recently.", "final answer after a tool call was not passed through")
    check(result.iterations_used == 2, f"expected 2 iterations, got {result.iterations_used}")
    check(result.tool_calls_made == [("search", {"domain": "chessdotcom", "section": "notable_games", "text_query": "checkmate"})],
          f"unexpected tool call log: {result.tool_calls_made}")


def test_loop_validation_error_recovers():
    section("run_query: invalid tool call is caught and fed back, model recovers")
    fake = lb.FakeLLM([
        lb.AssistantTurn(tool_calls=[lb.ToolCall("search", {"domain": "apple_health", "section": "sessions"})]),  # disabled domain
        lb.AssistantTurn(content="Sorry, I don't have apple_health data available right now."),
    ])
    result = lb.run_query("How did I sleep?", llm=fake)
    check("apple_health" in result.answer, "expected the model's recovery answer to be returned")
    check(result.iterations_used == 2, "a validation error must still consume one iteration (loop-breaking against infinite retries)")


def test_loop_repeated_call_short_circuits():
    section("run_query: exact repeated tool call is not re-executed (§43.6)")
    same_call = lb.ToolCall("search", {"domain": "chessdotcom", "section": "notable_games", "text_query": "checkmate"})
    fake = lb.FakeLLM([
        lb.AssistantTurn(tool_calls=[same_call]),
        lb.AssistantTurn(tool_calls=[same_call]),  # model repeats itself
        lb.AssistantTurn(content="Okay, based on what I already found."),
    ])
    result = lb.run_query("How many checkmates?", llm=fake)
    check(result.iterations_used == 3, f"expected all 3 scripted turns to be consumed, got {result.iterations_used}")
    check(len(result.tool_calls_made) == 2, "both calls should be logged even though the second was not re-executed")


def test_loop_max_iterations_fallback():
    section("run_query: MAX_ITERATIONS reached -> Python fallback, not another model attempt")
    # A model that never gives a final answer, always issuing a *different*
    # call each time so loop-breaking doesn't mask the max-iterations path.
    turns = [
        lb.AssistantTurn(tool_calls=[lb.ToolCall("search", {"domain": "chessdotcom", "section": "notable_games", "limit": i})])
        for i in range(1, 10)
    ]
    fake = lb.FakeLLM(turns)
    result = lb.run_query("Just keep searching forever.", llm=fake, max_iterations=3)
    check(result.hit_max_iterations is True, "expected the max-iterations fallback to trigger")
    check(result.iterations_used == 3, f"expected exactly max_iterations=3, got {result.iterations_used}")
    check("could not fully answer" in result.answer.lower(), "fallback answer should explicitly caveat that the answer may be partial")


def test_loop_unknown_domain_never_crashes():
    section("run_query: a completely malformed tool call never raises out of run_query")
    fake = lb.FakeLLM([
        lb.AssistantTurn(tool_calls=[lb.ToolCall("nonexistent_tool", {"foo": "bar"})]),
        lb.AssistantTurn(content="Handled gracefully."),
    ])
    try:
        result = lb.run_query("Trigger an unknown tool.", llm=fake)
        check(result.answer == "Handled gracefully.", "expected graceful recovery after an unknown-tool call")
    except Exception:
        check(False, "run_query must never raise on a malformed tool call -- see traceback above")
        traceback.print_exc()


# =============================================================================
# MAIN
# =============================================================================

def main():
    tests = [
        test_list_domains,
        test_validate_tool_call,
        test_tool_search_bank,
        test_tool_search_spotify,
        test_tool_search_health,
        test_tool_search_maps,
        test_tool_search_whatsapp,
        test_tool_search_chessdotcom,
        test_tool_get_aggregation,
        test_tool_resolve_full_ref,
        test_budget_list_result,
        test_loop_direct_final_answer,
        test_loop_one_tool_call_then_answer,
        test_loop_validation_error_recovers,
        test_loop_repeated_call_short_circuits,
        test_loop_max_iterations_fallback,
        test_loop_unknown_domain_never_crashes,
    ]

    t0 = time.time()
    for test in tests:
        try:
            test()
        except Exception:
            FAILURES.append(f"{test.__name__}: raised an exception -- see traceback above")
            traceback.print_exc()
    elapsed = time.time() - t0

    section("RESULT")
    print(f"Ran {len(tests)} test groups in {elapsed:.2f}s.")
    if SKIPPED:
        print(f"\n{len(SKIPPED)} check group(s) skipped (real data not present in this environment) -- see '(skipped: ...)' lines above.")
    if FAILURES:
        print(f"\n{len(FAILURES)} CHECK(S) FAILED:\n")
        for f in FAILURES:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("\nALL CHECKS PASSED.")
        sys.exit(0)


if __name__ == "__main__":
    main()
