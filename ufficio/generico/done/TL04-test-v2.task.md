id: TL04-test-v2
title: Test per router e policy
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL04-test-v2
base_branch: TL03-policy
allowed: [code/test_table_router_policy.py]
motore: gratis
modello: @gratis3
approved: yes
checks: [py_compile:code/test_table_router_policy.py]
checks_warn: [run_py:code/test_table_router_policy.py, contains_all:code/test_table_router_policy.py;unittest]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Create the NEW file code/test_table_router_policy.py (do not edit existing files): unit tests (unittest, no network, no Ollama, no database) for code/table_router.py and code/privacy_policy.py, both already written (read them). Cover: ranking returns k results; an obviously matching table ranks first on synthetic data; shuffling the table order does not crash; policy default is L0; L1 blocks query_results; L2 redacts sensitive columns; load_policy with a missing section gives L0.
If a test would need something the code does not offer, test only what exists. Write agenti/TL04-test-v2/RAPPORTO.md in Italian (how to run: python -m unittest code/test_table_router_policy.py).
