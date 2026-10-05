id: TL02-router
title: Router di tabelle (nuovo file)
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL02-router
base_branch: TL01-progetto-b
allowed: [code/table_router.py]
motore: gratis
modello: @gratis1
approved: yes
checks: [py_compile:code/table_router.py, run_py:code/table_router.py]
checks_warn: [contains_all:code/table_router.py;def route;def evaluate;KeywordBackend]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Create the NEW file code/table_router.py (do not edit existing files): route(question, tables, backend=..., k=3) -> ranked list of (table_name, score).
- `tables`: list of dicts {name, description}. Backends are classes with the same method rank(question, tables); implement: KeywordBackend (pure Python word-overlap/TF-IDF on name+description, no libraries), and the stubs EmbeddingBackend and LocalLLMBackend that raise NotImplementedError with a clear Italian message (they need Ollama; leave the interface and docstrings ready).
- Evaluation helper: evaluate(backend, cases, tables, k) -> dict with top1, top3, recall_at_k, where cases = list of {question, needed_tables}; plus a function that shuffles the table order N times (fixed seed) and reports how much the metrics change.
- A tiny self-test under `if __name__ == "__main__":` using ONLY synthetic tables and questions invented by you (a dozen), printing the metrics.
Italian comments. Write agenti/TL02-router/RAPPORTO.md in Italian (how to run it, limits).
