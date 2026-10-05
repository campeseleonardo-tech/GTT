id: TL01-progetto-b
title: Progetto bridge v2 (versione B)
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL01-progetto-b
base_branch: TL01-progetto-a
allowed: [docs/BRIDGE_V2_b.md]
motore: gratis
modello: @gratis2
approved: yes
checks: [files_exist:docs/BRIDGE_V2_b.md]
checks_warn: [min_chars:docs/BRIDGE_V2_b.md;3000, contains_all:docs/BRIDGE_V2_b.md;## Cosa cambia in v2;## Dubbi aperti per Leo]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Write docs/BRIDGE_V2_b.md IN ITALIAN: an independent design of llm_bridge v2 (another model writes a parallel version; do your own). Focus on RISKS and on the simplest thing that could work first.
Sections (exact titles): ## Come funziona oggi | ## Cosa cambia in v2 | ## Interfaccia del router di tabelle | ## Politica online/offline | ## Metriche e come misurarle | ## Ordine di lavoro | ## Dubbi aperti per Leo.
Do not write code files. Mark as "da verificare" anything you did not see in the code.
