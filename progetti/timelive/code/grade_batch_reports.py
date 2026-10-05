# grade_batch_reports.py
# =============================================================================
# AUTOMATED CORRECTNESS GRADING — for batch_test_llm_bridge.py reports
# (2026-09-15, added alongside the overnight cross-domain comparison batch)
# =============================================================================
#
# WHY THIS EXISTS
# -----------------------------------------------------------------------
# batch_test_llm_bridge.py's own "success" field has only ever meant "the
# agentic loop didn't crash and produced SOME final answer" — never "the
# answer was factually correct". That gap was fine when a human read
# through 9-12 answers by eye (as happened for every report so far this
# project), but it stops working once an overnight run produces answers
# across ~59 questions x 3 backends (llama3.2:3b, a mid-size Together AI
# model, Claude) — nobody is going to carefully fact-check ~180 answers
# by hand. Concretely: in the instagram mini-test
# (batch_report_llama_instagram_mini.json, 2026-09-15), 8/9 questions were
# marked "success": true, but on inspection at least 3 of those 8 answers
# were wrong or built on broken logic (instagram_02 picked an arbitrary
# thread instead of the one with the most messages; instagram_03's
# "is_group" heuristic matched a literal string that never appears in the
# real data, then generalized from a truncated 200-row scan; instagram_05
# queried the wrong table entirely for a question about "likes"). This
# script is the fix the project owner asked for: an automated grading
# pass, not a replacement for eyeballing everything by hand.
#
# HOW IT WORKS — Claude-as-judge against a REFERENCE run's real retrieved
# data, not a hand-authored answer key
# -----------------------------------------------------------------------
# Writing exact numeric ground truth for every question by hand (~59
# questions across 4 domains) is its own large, error-prone undertaking,
# and this project's discipline throughout has been "measure the real
# data, don't guess at it" — so this script does NOT invent a static
# answer key. Instead it takes one already-run REFERENCE report (in
# practice: a `--backend claude` run over the same question set, since
# the 2026-09-15 money-domain comparison already showed claude-sonnet-5
# getting 12/12 right against real vault.db data — see timelive.md) and,
# for each question, pulls out every run_sql call's ACTUAL query and
# ACTUAL retrieved rows from that reference run. That raw retrieved data
# — not the reference model's prose answer, which is one more thing that
# could be misread — is what a TARGET report's answer is graded against.
# This makes the reference report itself the single most important input
# here: if it wasn't run against the real vault.db (or was run before a
# schema/data change), the grades below it are worthless. It is still not
# infallible ground truth (a reference query can itself be subtly wrong),
# so a verdict of "correct" here means "consistent with what a generally
# reliable reference run actually retrieved", not "independently verified
# against the raw source files" — a distinction worth remembering before
# treating this script's output as beyond question.
#
# For each question present in BOTH the reference and a target report,
# this script sends Claude (a single plain grading call, no tools — this
# is NOT going through llm_bridge.run_query()) the question text, the
# reference's retrieved SQL rows, and the target's final answer, and asks
# for a verdict: correct / partially_correct / incorrect / unverifiable,
# plus a one-line reason. "unverifiable" is used deliberately whenever
# the reference itself has no usable run_sql data for that question (it
# failed, hit_max_iterations with nothing useful, or never called
# run_sql at all) — this script never fabricates a verdict from nothing.
#
# REQUIRES: `pip install anthropic --break-system-packages` and an
# ANTHROPIC_API_KEY environment variable (same convention as
# llm_bridge.ClaudeAPIClient — never hardcoded here or passed as a CLI
# argument).
#
# HOW TO RUN
# -----------------------------------------------------------------------
#   python3 grade_batch_reports.py \
#       --reference batch_report_claude_20260916T010000Z.json \
#       --target batch_report_llama3.2_3b_overnight.json \
#       --target batch_report_together_overnight.json \
#       --output grading_report.json
#
# Prints a per-model/per-domain accuracy summary to stdout and writes the
# full per-question verdicts (with reasons) to --output.
# =============================================================================

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


GRADING_MODEL = "claude-sonnet-5"

GRADING_SYSTEM_PROMPT = (
    "You are grading whether an AI assistant's answer to a question about the "
    "user's personal data is factually consistent with a reliable reference "
    "dataset. You will be given: the question, the ACTUAL SQL queries and rows "
    "retrieved by a trusted reference run against the real database, and the "
    "candidate answer to grade. Judge ONLY factual/numeric consistency with the "
    "reference data — not style, phrasing, or completeness beyond what the "
    "reference data itself supports. If the reference data does not actually "
    "contain enough information to check the candidate answer, say so honestly "
    "with verdict 'unverifiable' rather than guessing.\n\n"
    "Respond with ONLY a JSON object, no other text, no markdown fences:\n"
    '{"verdict": "correct" | "partially_correct" | "incorrect" | "unverifiable", '
    '"reason": "one concise sentence explaining the verdict"}'
)


def _index_by_id(report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {r["id"]: r for r in report.get("results", []) if r.get("id")}


def _reference_evidence(entry: Dict[str, Any]) -> Optional[str]:
    """
    Extracts the actual run_sql queries + retrieved rows from one
    reference report entry, compactly. Returns None if there is nothing
    usable (the reference itself failed, or made no run_sql calls) — the
    caller must treat that as "unverifiable", never grade against
    nothing.
    """
    if not entry.get("success"):
        return None
    sql_calls = [
        c for c in entry.get("tool_calls_made", [])
        if c.get("tool") == "run_sql" and isinstance(c.get("result"), dict) and "error" not in c["result"]
    ]
    if not sql_calls:
        return None
    pieces = []
    for c in sql_calls:
        result = c["result"]
        rows = result.get("rows", [])
        pieces.append(
            f"Query: {c.get('arguments', {}).get('query', '')}\n"
            f"Rows returned ({result.get('row_count', len(rows))}"
            f"{', TRUNCATED' if result.get('truncated') else ''}): "
            f"{json.dumps(rows, ensure_ascii=False, default=str)}"
        )
    return "\n\n".join(pieces)


def grade_one(
    client: Any,
    question: str,
    reference_evidence: str,
    candidate_answer: str,
) -> Dict[str, str]:
    user_content = (
        f"QUESTION:\n{question}\n\n"
        f"REFERENCE DATA (actual SQL + rows retrieved by a trusted run):\n{reference_evidence}\n\n"
        f"CANDIDATE ANSWER TO GRADE:\n{candidate_answer}\n"
    )
    for attempt in range(3):
        try:
            response = client.messages.create(
                model=GRADING_MODEL,
                max_tokens=300,
                system=GRADING_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_content}],
            )
            text = "".join(block.text for block in response.content if block.type == "text").strip()
            # Strip accidental markdown fences before parsing, same
            # defensive habit as llm_bridge's malformed-tool-call handling.
            if text.startswith("```"):
                text = text.strip("`").lstrip("json").strip()
            parsed = json.loads(text)
            verdict = parsed.get("verdict")
            if verdict not in ("correct", "partially_correct", "incorrect", "unverifiable"):
                raise ValueError(f"unexpected verdict value: {verdict!r}")
            return {"verdict": verdict, "reason": str(parsed.get("reason", ""))}
        except Exception as exc:
            if attempt == 2:
                return {"verdict": "unverifiable", "reason": f"grading call failed after 3 attempts: {exc}"}
            time.sleep(2 * (attempt + 1))
    return {"verdict": "unverifiable", "reason": "unreachable"}


def grade_report_pair(
    client: Any,
    reference: Dict[str, Any],
    target: Dict[str, Any],
    target_label: str,
) -> List[Dict[str, Any]]:
    ref_by_id = _index_by_id(reference)
    target_by_id = _index_by_id(target)
    graded: List[Dict[str, Any]] = []

    shared_ids = [qid for qid in target_by_id if qid in ref_by_id]
    print(f"[{target_label}] grading {len(shared_ids)} question(s) shared with the reference report...")

    for i, qid in enumerate(shared_ids, start=1):
        ref_entry = ref_by_id[qid]
        target_entry = target_by_id[qid]
        question = target_entry.get("question", ref_entry.get("question", ""))
        domains = target_entry.get("domains_tagged", [])

        evidence = _reference_evidence(ref_entry)
        if evidence is None:
            graded.append({
                "id": qid, "model": target_label, "domains": domains, "question": question,
                "verdict": "unverifiable",
                "reason": "reference run had no usable run_sql data for this question (it failed or never queried).",
            })
            print(f"  [{i}/{len(shared_ids)}] {qid}: unverifiable (no reference data)")
            continue

        if not target_entry.get("success"):
            graded.append({
                "id": qid, "model": target_label, "domains": domains, "question": question,
                "verdict": "incorrect",
                "reason": f"target run itself failed: {target_entry.get('error', '(no error captured)')}",
            })
            print(f"  [{i}/{len(shared_ids)}] {qid}: incorrect (target run failed)")
            continue

        candidate_answer = target_entry.get("answer", "")
        verdict = grade_one(client, question, evidence, candidate_answer)
        graded.append({
            "id": qid, "model": target_label, "domains": domains, "question": question,
            "verdict": verdict["verdict"], "reason": verdict["reason"],
        })
        print(f"  [{i}/{len(shared_ids)}] {qid}: {verdict['verdict']} — {verdict['reason'][:100]}")

    return graded


def summarize_grades(all_graded: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_model: Dict[str, Dict[str, int]] = {}
    by_model_domain: Dict[str, Dict[str, Dict[str, int]]] = {}

    for g in all_graded:
        model = g["model"]
        verdict = g["verdict"]
        by_model.setdefault(model, {}).setdefault(verdict, 0)
        by_model[model][verdict] += 1
        for domain in (g["domains"] or ["(untagged)"]):
            by_model_domain.setdefault(model, {}).setdefault(domain, {}).setdefault(verdict, 0)
            by_model_domain[model][domain][verdict] += 1

    accuracy: Dict[str, Optional[float]] = {}
    for model, counts in by_model.items():
        gradable = sum(v for k, v in counts.items() if k != "unverifiable")
        correct = counts.get("correct", 0)
        accuracy[model] = round(100 * correct / gradable, 1) if gradable else None

    return {
        "counts_by_model": by_model,
        "accuracy_pct_by_model_excluding_unverifiable": accuracy,
        "counts_by_model_and_domain": by_model_domain,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade batch_test_llm_bridge.py target report(s) against a reference report's actual retrieved data, using Claude as judge.")
    parser.add_argument("--reference", required=True, help="Path to the reference report JSON (in practice: a --backend claude run over the same questions).")
    parser.add_argument("--target", action="append", required=True, help="Path to a target report JSON to grade (e.g. the llama3.2:3b or Together AI run). Repeat --target for multiple reports in one grading pass.")
    parser.add_argument("--output", default="grading_report.json", help="Output JSON path for the full per-question verdicts + summary (default: grading_report.json).")
    args = parser.parse_args()

    try:
        import anthropic
    except ImportError:
        print("ERROR: the `anthropic` package is required — pip install anthropic --break-system-packages", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment

    with open(args.reference, "r", encoding="utf-8") as f:
        reference = json.load(f)
    print(f"Reference: {args.reference} (backend={reference.get('backend')}, model={reference.get('model')})")

    all_graded: List[Dict[str, Any]] = []
    for target_path in args.target:
        with open(target_path, "r", encoding="utf-8") as f:
            target = json.load(f)
        target_label = f"{target.get('backend', '?')}:{target.get('model', Path(target_path).stem)}"
        all_graded.extend(grade_report_pair(client, reference, target, target_label))

    summary = summarize_grades(all_graded)

    report = {
        "reference_path": args.reference,
        "reference_backend": reference.get("backend"),
        "reference_model": reference.get("model"),
        "grading_model": GRADING_MODEL,
        "summary": summary,
        "graded": all_graded,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n{'=' * 70}\nRIEPILOGO GRADING\n{'=' * 70}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nReport completo scritto in: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
