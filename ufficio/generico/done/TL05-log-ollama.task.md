id: TL05-log-ollama
title: Registrare prompt_eval in llm_bridge
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL05-log-ollama
base_branch: TL04-test-v2
allowed: [code/llm_bridge.py]
motore: gratis
modello: @gratis1
approved: yes
checks: [py_compile:code/llm_bridge.py]
checks_warn: [contains_all:code/llm_bridge.py;prompt_eval_count;prompt_eval_duration;[agente TL05]]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Edit ONLY code/llm_bridge.py with small EDIT blocks (the file is big: never rewrite it). Goal: for every call to Ollama, record prompt_eval_count and prompt_eval_duration (fields of the Ollama response) so Leo can check whether the system-prompt prefix cache works. Find where the Ollama response is parsed; keep the values in the same structure that already stores per-call info (e.g. tokens/timings) and, if there is a per-run report or log, include them there. If the response does not contain the fields, store None (never fail). Do not change behaviour otherwise. Mark each change with a comment # [agente TL05].
Write agenti/TL05-log-ollama/RAPPORTO.md in Italian: where exactly the values are stored and what Leo should look at.
