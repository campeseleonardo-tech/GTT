id: TL07-bridge-v2
title: Bridge v2: un solo progetto chiaro (da A e B)
project: timelive
tier: small
priority: 3
repo: C:\Users\campe\Desktop\timelive_repo
branch: TL07-bridge-v2
base_branch: TL01-progetto-b
allowed: [docs/BRIDGE_V2.md]
motore: gratis
modello: @forte
approved: yes
checks: [files_exist:docs/BRIDGE_V2.md]
checks_warn: [min_chars:docs/BRIDGE_V2.md;3000, contains_all:docs/BRIDGE_V2.md;## In breve;## Ordine di lavoro;## Domande per Leo]
---
Context: Timelive is Leo's personal data archive (SQLite vault.db) with an LLM bridge (code/llm_bridge.py) that lets a model answer questions by calling tools (describe_table, run_sql ...). Read docs/todo_table_routing_test.md: it contains the pending directions to implement. NEVER read, print or invent real personal data: use only synthetic example data. Python standard library only unless the existing code already uses something else.

Two models wrote two independent designs of llm_bridge v2: docs/BRIDGE_V2_a.md and docs/BRIDGE_V2_b.md. Read both, plus code/llm_bridge.py (only the parts you need) and docs/todo_table_routing_test.md.
Write docs/BRIDGE_V2.md IN ITALIAN: ONE design that keeps the best of A and B and starts from the simplest thing that could work. Leo is not a programmer: explain in plain words, short sentences, no jargon without a one-line explanation.
Sections (exact titles): ## In breve (5 lines max: what v2 changes for Leo in practice) | ## Come funziona oggi | ## Cosa cambia in v2 | ## Dove A e B non sono d'accordo (and what you chose and why) | ## Ordine di lavoro (small steps, each one a possible separate agent task with the files it touches) | ## Rischi | ## Domande per Leo.
IMPORTANT: Leo answered earlier questions about B without understanding them; ignore any previous answers. In "## Domande per Leo" and in DOMANDE.md ask at most 5 questions, each with the context needed to understand it (perche) and what each option changes in practice (cambia). Mark "da verificare" anything you did not see in the code. Do not write code files.

NOTA DI LEO (2026-10-05): ha provato solo gemini finora, provare altri modelli
