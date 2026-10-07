id: TL03-policy
title: Politica online/offline (nuovo file)
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL03-policy
base_branch: TL02-router
allowed: [code/privacy_policy.py]
motore: gratis
modello: @gratis2
approved: yes
checks: [py_compile:code/privacy_policy.py, run_py:code/privacy_policy.py]
checks_warn: [contains_all:code/privacy_policy.py;class Policy;def redact_rows;def load_policy]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Create the NEW file code/privacy_policy.py (do not edit existing files): the online/offline policy.
- Levels: L0 nothing leaves the machine; L1 only the question and the table descriptions may leave; L2 query results may leave too, with columns marked sensitive=True redacted (replaced by "[omesso]").
- API: class Policy(level, per_domain_overrides=None) with allows(kind) where kind in {"question","table_descriptions","query_results"}; redact_rows(columns, rows) where columns are dicts {name, sensitive}; load_policy(config_dict) reading a "privacy" section (document the JSON shape in the docstring, default = L0 when missing: safest).
- Self-test under __main__ with synthetic data only; print PASS/FAIL lines and exit with code 1 if any fails.
Italian comments. Write agenti/TL03-policy/RAPPORTO.md in Italian.
