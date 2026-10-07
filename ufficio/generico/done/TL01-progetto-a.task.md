id: TL01-progetto-a
title: Progetto bridge v2 (versione A)
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL01-progetto-a
allowed: [docs/BRIDGE_V2_a.md]
motore: gratis
modello: @gratis1
approved: yes
checks: [files_exist:docs/BRIDGE_V2_a.md]
checks_warn: [min_chars:docs/BRIDGE_V2_a.md;3000, contains_all:docs/BRIDGE_V2_a.md;## Cosa cambia in v2;## Dubbi aperti per Leo]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Write docs/BRIDGE_V2_a.md IN ITALIAN: the design of llm_bridge v2 based on the directions of docs/todo_table_routing_test.md and on how code/llm_bridge.py works today (read it).
Sections (exact titles): ## Come funziona oggi (max 15 lines, only what you saw in the code) | ## Cosa cambia in v2 | ## Interfaccia del router di tabelle (Python signatures, backends A/B/C swappable) | ## Politica online/offline (L0/L1/L2, where the config lives, how sensitive=True columns are redacted) | ## Metriche e come misurarle | ## Ordine di lavoro (small steps) | ## Dubbi aperti per Leo.
Do not write code files. Mark as "da verificare" anything you did not see in the code.
