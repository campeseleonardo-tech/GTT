# batch_test_llm_bridge.py
# =============================================================================
# BATCH REAL-MODEL EVALUATION HARNESS — llm_bridge.py (timelive.md §45/§46,
# "real-model, real-hardware validation" tier, extended to a batch run)
# =============================================================================
#
# 2026-09-14 UPDATE — ported to the SQLite / 3-tool architecture
# -----------------------------------------------------------------------
# This harness predates the PRIMARY/FULL -> single-vault.db rebuild and
# had two things that no longer made sense with the new llm_bridge.py
# (list_tables/describe_table/run_sql, no more domain-scoped tools):
#   * `lb.ACTIVE_DOMAINS` doesn't exist anymore (hard AttributeError on
#     the "Domini attivi" print line) — replaced with
#     `sorted(ingest_engine.DOMAIN_REGISTRY.keys())`, the real live list
#     of migrated domains.
#   * The summary's `primary_vs_full_access` breakdown (search/
#     get_aggregation vs resolve_full_ref call counts) was a PRIMARY/FULL
#     concept that has no equivalent now — there is no PRIMARY/FULL split
#     anymore, just list_tables/describe_table/run_sql. Removed; the
#     `tool_calls_by_tool` breakdown (already computed) is the correct
#     replacement for "how did the model spend its tool calls".
#   * `domain_tool_calls` grouped by an `arguments["domain"]` key the old
#     tools always had — the new tools don't take a domain argument at
#     all (describe_table takes `table`, run_sql takes `query`), so this
#     always silently degenerated to `{"(none)": N}`. Removed rather than
#     left silently meaningless.
#
# Also: the SPOTIFY_QUESTIONS additions below (spotify_05..spotify_11)
# were added after a real manual smoke test on the Pi (2026-09-14) found
# a genuine model-reasoning bug, not an infra bug: asked "Quante canzoni
# ho ascoltato in totale su Spotify?", llama3.2:3b ran
# `SELECT COUNT(DISTINCT media_type) FROM plays` (counting how many
# distinct media_type VALUES exist, i.e. 2) instead of
# `SELECT COUNT(*) FROM plays WHERE content_type = 'track'` (the actual
# answer, 358005) — despite the injected schema's semantic_note already
# spelling out the media_type/content_type distinction in plain language.
# The new questions deliberately re-probe that exact confusion plus
# related native-field and "correctly say no data" cases, so the batch
# report gives more than one anecdote to judge the model's reasoning by.
#
# 2026-09-14 UPDATE 2 — money domain migrated, "bank" questions retagged
# -----------------------------------------------------------------------
# money_ingest.py replaced the old "bank" domain (bank_*/whatsapp_*/
# maps_* below were written before any domain but chess.com/spotify was
# migrated). Every question previously tagged domains=["bank"] is now
# tagged domains=["money"] (ids renamed bank_* -> money_* to match) since
# "bank" is no longer a registered domain name. A few new money_*
# questions were added to actually probe the parts "bank" never covered:
# Trade Republic investments, private-market legs, and security_events
# (dividends/corporate actions) — none of which existed in the old
# PRIMARY/FULL bank dataset. Kept deliberately SHORT (money_04..money_07,
# 4 new questions) rather than a big new battery, for a cheap --only
# money run.
#
# 2026-09-14 UPDATE 3 — overnight cross-domain batch: checkpointing,
# resume, richer per-call capture, new questions
# -----------------------------------------------------------------------
# Three real problems surfaced analyzing the first money batch reports
# (money_04/money_05, both models) that this update fixes:
#
# (a) NO CHECKPOINTING — a multi-hour unattended run wrote its report ONLY
#     at the very end. A crash, an SSH disconnect without nohup/tmux, a
#     Pi reboot, or an OOM kill at hour 3 of 6 lost EVERYTHING, not just
#     the in-flight question. Fixed: --output is now also a checkpoint
#     path, rewritten atomically (temp file + os.replace, never a
#     half-written JSON) after every single question, not just at the
#     end. See _write_report_atomically() and _checkpoint() in main().
#
# (b) NO RESUME — following from (a), even a report that survived a
#     crash couldn't be picked up; the only option was rerunning
#     everything, expensive when a single money question can take
#     4-7+ minutes. Fixed: `--resume <path>` loads a previous report,
#     keeps its completed entries verbatim, and only actually re-runs
#     what's missing — restarting after a crash is the same command plus
#     `--resume <same output path>`.
#
# (c) LOST tool_results/malformed_tool_call_recoveries — llm_bridge.py's
#     QueryResult has carried per-call tool_results and a
#     malformed_tool_call_recoveries count since the spotify bridge fix
#     (EVOLUTION_LOG.md), but THIS harness never read them back out —
#     confirmed by inspecting the real money_04/money_05 reports, whose
#     tool_calls_made entries had no "result" key at all. A pure
#     reporting gap (llm_bridge.py itself was already computing both
#     correctly), silently throwing away exactly the kind of detail this
#     harness exists to collect. Fixed: restored in run_batch()/
#     summarize(), same shape already proven correct on the spotify batch.
#
# Also added: --request-timeout (lower the per-HTTP-call timeout for an
# overnight run so one hung call fails fast instead of silently eating up
# to 600s x max_iterations on a single question), line-buffered stdout
# (so `tail -f` on a nohup'd log shows progress live, not in one big
# chunk at the end), and 6 new EXTENDED_QUESTIONS: money_10/money_11
# (direct probes of the just-fixed BUY/SELL category_raw distinction —
# see money_ingest.py's 2026-09-14 UPDATE), money_12 (adversarial: PayPal
# is a real data source found in Input/Money but deliberately NOT
# ingested yet — correct behavior is to say so, not fabricate a number),
# manifest_02 (explicit per-table row-count coverage — earlier batches
# almost never touched security_events/private_market_legs directly),
# cross_05 (a genuine 3-DOMAIN cross question — money+chessdotcom+spotify
# together, not just 2), and adversarial_05 (a harder money question
# requiring the model to pair a sale with its earlier purchase price,
# which nothing in the schema does for it).
#
# 2026-09-14 UPDATE 4 — questions grounded in the real raw input content
# -----------------------------------------------------------------------
# Per the project owner's explicit request, the question set was reviewed
# against the ACTUAL raw files in Input/Spotify, Input/Chessdotcom and
# Input/Money (read directly this session, not inferred from the schema),
# so the batch simulates a genuine conversation rather than generic
# templated questions. The 4B-model idea discussed earlier the same
# session was explicitly dropped ("lascia il modello 4B da parte") — this
# run is llama3.2:3b vs qwen2.5:3b only, same two models as money_04/05,
# for direct comparability with that existing baseline.
#
# Two existing questions were tightened (kept their ids, for continuity
# with the money_04/money_05 baseline already run): adversarial_01
# ("Netflix marzo 2019" -> "dicembre 2025", still a real 0-match no-data
# case but now inside meinElba's actual covered range, a harder
# fabrication trap) and spotify_11 ("dicembre 2030" -> "settembre 2026",
# one month past the real last day of data, 2026-08-20, instead of an
# obviously-absurd future date).
#
# 12 new EXTENDED_QUESTIONS were added, each anchored to a specific real
# fact confirmed by inspection: money_13/14 (real Trade Republic top
# holdings — NVIDIA, BYD, Steyr Motors, Alphabet, Opendoor...), money_15
# (the confirmed Banca Sella self-transfer nuance), money_16 (the
# confirmed mismatched real date ranges across meinElba/Sella/Trade
# Republic), spotify_12-15 (real top artists, real ~48% skip rate, real
# near-zero audiobook/podcast usage, real platforms/incognito_mode field),
# chess_09-11 (the real most-played opponent Kenpachi-97, the real
# 300s/600s-dominant time-control distribution, the real last game date),
# and cross_06 (a 3-domain question anchored to the real overlapping
# Trade Republic/chess/spotify date windows).
#
# 2026-09-15 UPDATE 5 — instagram migration, short first coherence check
# -----------------------------------------------------------------------
# instagram_ingest.py just added 8 new tables (see that module's
# docstring). Rather than write a full validation battery before the
# domain has even been run once at full real scale (~790 DM threads —
# the earlier test run only exercised 31 of them), this adds a
# deliberately SHORT set (instagram_01..08, --only instagram, ~8
# questions) meant purely as a first coherence smoke test — the same
# role the spotify_05..11 additions played after the media_type/
# content_type bug (see UPDATE above): catch an obvious schema/semantic
# problem early with a real model, not exhaustively validate every
# table. Each question deliberately targets a specific real design
# decision from instagram_ingest.py rather than being generic:
#   - instagram_02 probes the is_sampled/top-20-full-text-DM design
#     (only some threads have message-level text; the rest are
#     metadata-only) — a model that ignores is_sampled and averages
#     over ALL threads is answering a different, wrong question.
#   - instagram_03 re-probes the real is_group bug found and fixed
#     during this session's own testing (participants includes the
#     account owner, so the correct group-vs-1:1 test is
#     len(participants) > 2, not > 1).
#   - instagram_06 and instagram_07 are adversarial, mirroring the
#     PayPal no-data trap (money_12): instagram_login_activity
#     deliberately has NO IP Address column (same privacy choice as
#     spotify's ip_addr exclusion), and connections/contacts/
#     synced_contacts.json was deliberately never ingested at all. A
#     model that fabricates an IP or a contact list here is a real bug,
#     not a missing-data quirk — the schema/semantic_notes should be
#     enough for it to say "I don't have that."
#   - instagram_08 is a first cross-domain probe including the new
#     domain, matching the existing cross_* pattern.
# Not yet added: an --extended battery mirroring the spotify_12-15 /
# chess_09-11 depth (grounded in exact real top likes/followers/etc.) —
# deferred until the full ~790-thread ingest has actually run once and
# those real facts can be confirmed by inspection, the same discipline
# already applied to every other domain's grounded questions above.
#
# HOW TO RUN AN UNATTENDED OVERNIGHT BATCH (Raspberry Pi)
# -----------------------------------------------------------------------
#   # One-shot, both models sequentially, survives an SSH disconnect
#   # (nohup) and survives a crash mid-run (each --output is also a
#   # checkpoint — see UPDATE 3 above). See the end of this file / the
#   # chat for the exact ready-to-paste command.
#   # To manually restart a single model after a crash, resume from its
#   # own checkpoint file instead of rerunning everything:
#   nohup python3 batch_test_llm_bridge.py --model llama3.2:3b \
#       --only chessdotcom,spotify,money --extended \
#       --request-timeout 180 \
#       --resume batch_report_llama3.2_3b_overnight.json \
#       > run_llama_resume.log 2>&1 &
#
# WHY THIS EXISTS
# -----------------------------------------------------------------------
# test_llm_bridge.py proves the Python-side control logic is not obviously
# broken (FakeLLM tier) and that the tool functions behave correctly
# against real data (real-data-volume tier). Neither of those tiers
# involves an actual model deciding what to call and when — timelive.md
# §43.9/§45 already names that as a THIRD, distinct tier ("real-model,
# real-hardware validation"), first exercised manually in v4.2 with one
# or two ad hoc questions typed at llm_bridge.py's own CLI.
#
# This script is that tier, done properly and repeatably: it runs a
# curated batch of realistic questions (see QUESTIONS below) through the
# real agentic loop (run_query) against a REAL Ollama server — no
# FakeLLM — and logs everything needed to evaluate the model's behavior
# afterward: which tool(s) it chose, with what arguments, how many
# iterations it needed, how long each question took wall-clock, whether
# it ever hit MAX_ITERATIONS, and its final answer. This is the "raccogli
# tanti dati" mechanism agreed with the project owner (chat, 2026-09-11):
# run this once on the Raspberry Pi (where a real Ollama server and every
# domain's real data already live), then hand the resulting JSON report
# back for analysis — which ingest/domain caused the model to struggle,
# which caveats it ignored, which questions needed too many iterations,
# etc. That analysis feeds back into concrete ingest/bridge improvements,
# closing the loop this phase is explicitly meant to open.
#
# WHAT THIS DOES NOT DO
# -----------------------------------------------------------------------
# It does not judge answer CORRECTNESS automatically — there is no ground
# truth encoded here, and the whole point of this phase is to look at
# real behavior with human judgment, not to pre-decide what "right" looks
# like. It only captures behavior faithfully so that judgment can happen
# afterward, with the full trace in hand. (Known real numbers for spotify,
# to check answers against by eye: 358,440 plays total — 358,005 track,
# 435 episode, 0 audiobook — across 33 files, 17,445 listening sessions.
# For money (2026-09-14 sandbox run, real data): 3,202 transactions, 38
# security_events, 8 private_market_legs.)
#
# HOW TO RUN (on the machine with a real Ollama server + real Input/*.json)
# -----------------------------------------------------------------------
#   python3 batch_test_llm_bridge.py --only spotify
#       # this session's scope: spotify + untagged manifest/cross questions
#       # that mention spotify (cross_02). Excludes bank/whatsapp/maps
#       # questions, whose domains are not migrated to the new engine yet.
#   python3 batch_test_llm_bridge.py --only money
#       # small, cheap run: just the money_* questions (7 of them) +
#       # untagged manifest/cross questions.
#   python3 batch_test_llm_bridge.py --model llama3.2:3b --host http://localhost:11434 --only spotify
#   python3 batch_test_llm_bridge.py --output my_report.json --max-iterations 5 --only spotify
#   python3 batch_test_llm_bridge.py --backend claude --ids money_01,money_04,money_05
#       # smallest, cheapest run: a handful of exact ids against the real
#       # Anthropic API instead of Ollama (needs ANTHROPIC_API_KEY set +
#       # `pip install anthropic`) — good for a first low-token sanity
#       # check of the money domain specifically.
#   python3 batch_test_llm_bridge.py --model llama3.2:3b --only instagram --request-timeout 120 --output batch_report_llama_instagram_mini.json
#       # 2026-09-15: the new instagram mini coherence check (UPDATE 5
#       # above) — 8 questions, ~30 min wall-clock on llama3.2:3b at the
#       # avg pace seen in the previous llama batch (~125s/question).
#   python3 batch_test_llm_bridge.py --backend together --model "Qwen/Qwen2.5-14B-Instruct" --only chessdotcom,spotify,money,instagram --extended --output batch_report_together.json
#       # 2026-09-15 UPDATE 6: the new TogetherAIClient (see llm_bridge.py)
#       # for a mid-size (8-16B class) open-model comparison against
#       # llama3.2:3b, without running it on the Pi. Needs
#       # TOGETHER_API_KEY set + `pip install requests` (already a
#       # dependency). NOT LIVE-TESTED THIS SESSION — see
#       # TogetherAIClient's own docstring in llm_bridge.py — confirm the
#       # exact model slug on Together's current serverless catalog and
#       # run one cheap smoke question first:
#       #   python3 batch_test_llm_bridge.py --backend together --ids manifest_01
#
# 2026-09-15 UPDATE 6 — the overnight cross-domain comparison batch
# -----------------------------------------------------------------------
# Project owner's explicit decision: scope the overnight comparison batch
# to the 4 domains that actually have real ingested data right now
# (chessdotcom, spotify, money, instagram) — deliberately EXCLUDING
# whatsapp/maps questions in QUESTIONS/EXTENDED_QUESTIONS above, which
# are kept in this file for when those domains get migrated but are not
# registered in ingest_engine.DOMAIN_REGISTRY yet and would only produce
# "table does not exist" errors. Use:
#   --only chessdotcom,spotify,money,instagram --extended
# for each backend (ollama/llama3.2:3b, together/Qwen2.5-14B, claude) to
# run the exact same, comparable question set on all three. Also see
# grade_batch_reports.py (new, same date) for the automated
# correctness-grading pass requested alongside this batch — "success" in
# THIS harness only ever meant "the loop didn't crash and produced SOME
# answer", never "the answer was actually correct" (see this file's own
# WHAT THIS DOES NOT DO note below, still true) — a real overnight batch
# across 3 backends produces far more answers than can be eyeballed by
# hand, which is exactly the gap grade_batch_reports.py fills.
#
# The report is written to a timestamped JSON file by default
# (batch_report_<backend>_<UTC timestamp>.json) so repeated runs never
# overwrite each other — send the resulting file back for analysis.
# =============================================================================

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import ingest_engine
import llm_bridge as lb


# ==============================================================================
# QUESTION SET
# ==============================================================================
# Each entry: (id, domains, question). `domains` is a list of the
# domain(s) this question is primarily about — used only for the --only
# filter and for grouping in the summary, never enforced against what the
# model actually calls (the model is free to call whatever it decides,
# including domains not listed here — that mismatch is itself useful
# signal). Phrased in Italian, the way the project owner actually talks
# to this assistant, deliberately mixing exact dates (where real data is
# known to cover them, e.g. money/spotify's confirmed 2026-08 coverage)
# with relative/open phrasing (where the exact real date range is not
# assumed here) so the batch also surfaces how well the model — and SQL
# it writes — handles vaguer real-world phrasing.
#
# NOTE (2026-09-14): whatsapp_*/maps_* questions below are kept for when
# those domains get migrated to ingest_engine.py — right now they are not
# registered, so use --only chessdotcom,spotify,money to avoid running
# questions against domains that don't exist yet in this architecture.
QUESTIONS: List[Dict[str, Any]] = [
    {"id": "money_01", "domains": ["money"], "question": "Quanto ho speso in totale ad agosto 2026?"},
    {"id": "money_02", "domains": ["money"], "question": "Quali sono state le mie spese più alte su Amazon negli ultimi mesi?"},
    {"id": "money_03", "domains": ["money"], "question": "Ho degli abbonamenti ricorrenti? Quali sono quelli che mi costano di più?"},
    # --- added 2026-09-14, money migration: probe investment/private-market/security_events, non coperti dal vecchio dominio bank ---
    {"id": "money_04", "domains": ["money"], "question": "Quanto ho investito su Trade Republic in totale, tra acquisti e vendite?"},
    {"id": "money_05", "domains": ["money"], "question": "Cosa ho comprato nei mercati privati (private markets)?"},
    {"id": "money_06", "domains": ["money"], "question": "Ho ricevuto dividendi? Quanto ho pagato di tasse su questi dividendi?"},
    {"id": "money_07", "domains": ["money"], "question": "Ci sono state operazioni straordinarie sui miei titoli, tipo split o conversioni?"},
    {"id": "spotify_01", "domains": ["spotify"], "question": "Cosa ho ascoltato di più di recente su Spotify?"},
    {"id": "spotify_02", "domains": ["spotify"], "question": "Qual è stata la mia sessione di ascolto più lunga ad agosto 2026?"},
    # --- added 2026-09-14, after the manual smoke-test bug (see header) ---
    {"id": "spotify_05", "domains": ["spotify"], "question": "Quante canzoni ho ascoltato in totale su Spotify?"},
    {"id": "spotify_06", "domains": ["spotify"], "question": "Quanti episodi di podcast ho ascoltato rispetto alle canzoni vere e proprie?"},
    {"id": "spotify_07", "domains": ["spotify"], "question": "Ho mai ascoltato audiolibri su Spotify?"},
    {"id": "spotify_08", "domains": ["spotify"], "question": "Quante volte ho saltato un brano (skip) rispetto a quante l'ho ascoltato fino alla fine?"},
    {"id": "spotify_09", "domains": ["spotify"], "question": "Quanto ascolto è avvenuto offline rispetto a online?"},
    {"id": "spotify_10", "domains": ["spotify"], "question": "Qual è la sessione di ascolto con più brani in assoluto, e quanti brani conteneva?"},
    {"id": "spotify_11", "domains": ["spotify"], "question": "Quante ore ho ascoltato Spotify a settembre 2026?"},
    {"id": "whatsapp_01", "domains": ["whatsapp"], "question": "In quali delle mie chat WhatsApp sono stato più attivo ultimamente?"},
    {"id": "whatsapp_02", "domains": ["whatsapp"], "question": "Quante videochiamate ho fatto di recente e quanto sono durate in totale?"},
    {"id": "whatsapp_03", "domains": ["whatsapp"], "question": "Ho condiviso qualche posizione GPS su WhatsApp di recente? Con chi e dove?"},
    {"id": "whatsapp_04", "domains": ["whatsapp"], "question": "Cosa diceva esattamente l'ultimo messaggio di testo che ho ricevuto?"},
    {"id": "chess_01", "domains": ["chessdotcom"], "question": "Come sta andando il mio rating a scacchi in blitz negli ultimi mesi?"},
    {"id": "chess_02", "domains": ["chessdotcom"], "question": "Quali sono state le mie vittorie più sorprendenti a scacchi contro avversari molto più forti di me?"},
    {"id": "chess_03", "domains": ["chessdotcom"], "question": "Qual è stata la mia sessione di scacchi più lunga: quante partite ho giocato e con che risultato?"},
    {"id": "chess_04", "domains": ["chessdotcom"], "question": "Quante partite ho perso per scacco matto rispetto a quante per tempo scaduto?"},
    {"id": "chess_05", "domains": ["chessdotcom"], "question": "Raccontami nel dettaglio l'ultima partita di scacchi che ho giocato, comprese le mosse."},
    {"id": "maps_01", "domains": ["maps"], "question": "Dove sono stato più spesso nell'ultimo mese, a parte casa?"},
    {"id": "maps_02", "domains": ["maps"], "question": "Quanti viaggi ho fatto di recente e quanto sono durati in media?"},
    {"id": "manifest_01", "domains": [], "question": "Che tipo di dati hai su di me al momento, e per quale periodo di tempo?"},
    {"id": "cross_01", "domains": ["chessdotcom", "whatsapp"], "question": "Ho dati sia sugli scacchi che su WhatsApp — che periodo di tempo coprono entrambi?"},
    {"id": "cross_02", "domains": ["chessdotcom", "spotify"], "question": "Quante partite a scacchi ho giocato in totale nella mia storia, e quante canzoni ho ascoltato su Spotify? Dammi i due numeri separatamente."},
    # --- added 2026-09-15, instagram migration: short first coherence
    # check (UPDATE 5 above) — deliberately NOT a full validation
    # battery, just enough to catch an obvious schema/semantic bug early.
    {"id": "instagram_01", "domains": ["instagram"], "question": "Quanti post ho pubblicato in totale su Instagram?"},
    {"id": "instagram_02", "domains": ["instagram"], "question": "Con quale contatto ho scambiato più messaggi diretti su Instagram, considerando solo le chat di cui hai il testo completo dei messaggi?"},
    {"id": "instagram_03", "domains": ["instagram"], "question": "Ho delle chat di gruppo nei messaggi diretti di Instagram, o sono tutte conversazioni individuali?"},
    {"id": "instagram_04", "domains": ["instagram"], "question": "Quante persone mi seguono su Instagram rispetto a quante ne seguo io?"},
    {"id": "instagram_05", "domains": ["instagram"], "question": "Ho messo 'mi piace' più spesso a dei post o a dei commenti su Instagram?"},
    {"id": "instagram_06", "domains": ["instagram"], "question": "Hai registrato il mio indirizzo IP negli accessi (login) al mio account Instagram?"},
    {"id": "instagram_07", "domains": ["instagram"], "question": "Hai accesso ai contatti della mia rubrica del telefono sincronizzati con Instagram?"},
    {"id": "instagram_08", "domains": ["instagram", "spotify", "chessdotcom"], "question": "Nei giorni in cui ho pubblicato più contenuti su Instagram, il mio modo di ascoltare musica o giocare a scacchi è cambiato rispetto agli altri giorni?"},
]


# v4.10: extended battery for a deliberately larger, unattended run —
# not a repeat of the 19 above, but new question TYPES chosen to probe
# things the original 19 never tested: paraphrase-stability (same intent,
# different wording), multi-step comparison, harder date phrasing,
# genuinely ambiguous/subjective phrasing, and deliberately
# impossible/out-of-range questions (does the model correctly say "no
# data" or fabricate one?). Run with --extended.
EXTENDED_QUESTIONS: List[Dict[str, Any]] = [
    {"id": "money_02b", "domains": ["money"], "question": "Negli ultimi tre mesi, quali sono state le spese più alte fatte su Amazon?"},
    {"id": "money_08", "domains": ["money"], "question": "Ho speso di più a luglio o ad agosto 2026, e di quanto?"},
    {"id": "money_09", "domains": ["money"], "question": "Quali sono le mie cinque spese più alte in assoluto, considerando tutta la mia storia?"},
    {"id": "spotify_01b", "domains": ["spotify"], "question": "Quali sono i brani che ho ascoltato di più questo mese?"},
    {"id": "spotify_03", "domains": ["spotify"], "question": "Quante canzoni diverse ho ascoltato in totale nella mia vita, come numero di brani distinti (non conteggio di riproduzioni)?"},
    {"id": "spotify_04", "domains": ["spotify"], "question": "C'è un artista che ascolto più di tutti gli altri messi insieme?"},
    {"id": "whatsapp_05", "domains": ["whatsapp"], "question": "Con quale contatto ho scambiato più messaggi in assoluto, considerando tutta la cronologia?"},
    {"id": "whatsapp_06", "domains": ["whatsapp"], "question": "Quante chat di gruppo ho su WhatsApp, rispetto alle chat individuali?"},
    {"id": "chess_06", "domains": ["chessdotcom"], "question": "Chi è l'avversario più forte (per rating) che ho mai battuto?"},
    {"id": "chess_07", "domains": ["chessdotcom"], "question": "Quante partite ho giocato in modalità bullet rispetto a blitz, in tutta la mia storia?"},
    {"id": "chess_08", "domains": ["chessdotcom"], "question": "Qual è la mia percentuale di vittorie complessiva, considerando tutta la mia storia su chess.com?"},
    {"id": "maps_03", "domains": ["maps"], "question": "Quanti luoghi diversi ho visitato in totale, escludendo casa?"},
    {"id": "maps_04", "domains": ["maps"], "question": "Sono mai stato in un posto per più di una settimana consecutiva?"},
    {"id": "cross_03", "domains": ["chessdotcom", "spotify"], "question": "Nei giorni in cui ho giocato di più a scacchi, ho anche ascoltato più musica su Spotify?"},
    {"id": "cross_04", "domains": ["money", "chessdotcom", "whatsapp"], "question": "Il giorno con la mia spesa bancaria più alta coincide con qualche partita a scacchi o messaggio WhatsApp particolare?"},
    {"id": "adversarial_01", "domains": ["money"], "question": "Quanto ho speso su Netflix a dicembre 2025?"},
    {"id": "adversarial_02", "domains": ["chessdotcom"], "question": "Quante partite ho vinto contro me stesso a scacchi?"},
    {"id": "adversarial_03", "domains": ["whatsapp"], "question": "Dimmi tutti i messaggi WhatsApp che ho scambiato con il numero +39 000 000 000."},
    {"id": "adversarial_04", "domains": ["money"], "question": "Quante azioni Tesla ho comprato?"},
    {"id": "ambiguous_01", "domains": ["money"], "question": "Sto spendendo troppo?"},
    {"id": "ambiguous_02", "domains": [], "question": "Come sto messo in generale?"},
    # --- added 2026-09-14 UPDATE 3, overnight cross-domain batch: probe the
    # just-fixed BUY/SELL category_raw distinction, a genuine 3-domain
    # cross question (not just 2), an adversarial probe for a real data
    # source (PayPal) that is deliberately NOT ingested yet, and explicit
    # per-table schema coverage (previous batches almost never touched
    # security_events/private_market_legs directly via describe_table). ---
    {"id": "money_10", "domains": ["money"], "question": "Su Trade Republic, ho comprato più azioni di quante ne abbia vendute, o il contrario? Dammi i due conteggi separatamente."},
    {"id": "money_11", "domains": ["money"], "question": "Qual è il mio investimento netto su Trade Republic ad oggi, cioè quanto ho comprato meno quanto ho venduto?"},
    {"id": "money_12", "domains": ["money"], "question": "Hai dati sui miei pagamenti PayPal? Se sì, quanto ho speso o ricevuto?"},
    {"id": "manifest_02", "domains": [], "question": "Per ciascuna tabella che hai a disposizione, dimmi quante righe contiene."},
    {"id": "cross_05", "domains": ["money", "chessdotcom", "spotify"], "question": "Nei giorni in cui ho speso di più, ho anche giocato a scacchi o ascoltato musica in modo diverso dal solito?"},
    {"id": "adversarial_05", "domains": ["money"], "question": "Ho mai venduto un titolo su Trade Republic in perdita rispetto al prezzo a cui l'avevo comprato?"},
    # --- added 2026-09-14 UPDATE 4: grounded in the REAL raw content of
    # Input/Spotify, Input/Chessdotcom and Input/Money (inspected directly
    # this session, not inferred from the schema) so the batch simulates
    # an actual conversation with real entities the model has to look up,
    # not generic placeholder questions. Two existing questions were also
    # tightened above (not counted as "new" here): adversarial_01's
    # "Netflix marzo 2019" was an easy no-data trap (obviously before any
    # account existed) — moved to "dicembre 2025", still 0 real matches
    # (grep-confirmed) but now INSIDE meinElba's real covered range
    # (01.02.2024-31.12.2025), a much harder fabrication trap. spotify_11's
    # "dicembre 2030" was similarly easy (absurdly far future) — moved to
    # "settembre 2026", one month past the real data's last day
    # (2026-08-20), a near-boundary trap instead of an obvious one.
    #
    # money: grounded in the real Trade Republic top holdings (NVIDIA, BYD,
    # Steyr Motors, Alphabet, Opendoor...) and the confirmed Banca Sella
    # self-transfer nuance (biggest "income" rows there are transfers
    # between the user's own accounts, not real income) and the confirmed
    # mismatched real date ranges across the 3 money sources (meinElba
    # Feb2024-Dec2025, Sella Jun-Aug2024 only, Trade Republic Feb2025-Aug2026).
    {"id": "money_13", "domains": ["money"], "question": "Ho mai comprato azioni NVIDIA su Trade Republic? Quante volte e con quale spesa totale?"},
    {"id": "money_14", "domains": ["money"], "question": "Tra tutti i titoli che ho comprato su Trade Republic, quali sono i 5 su cui ho investito di più in totale?"},
    {"id": "money_15", "domains": ["money"], "question": "Le entrate più alte che vedi sul mio conto Sella sono davvero stipendio o guadagni, o potrebbero essere giroconti tra i miei stessi conti?"},
    {"id": "money_16", "domains": ["money"], "question": "Da quando hai dati sui miei movimenti bancari, e coprono lo stesso periodo per tutti i miei conti o ci sono dei buchi tra un conto e l'altro?"},
    # spotify: grounded in the real top artists/tracks (Marco Castello,
    # Buena Vista Social Club, LATIN MAFIA, Prince Royce...), the real
    # confirmed ~48% skip rate, the real near-zero audiobook/podcast usage
    # (0 audiobooks, 2 podcast episodes total), and the real platforms
    # (ios/windows/cast) and incognito_mode field.
    {"id": "spotify_12", "domains": ["spotify"], "question": "Chi sono i miei 5 artisti più ascoltati in assoluto, considerando tutta la mia storia?"},
    {"id": "spotify_13", "domains": ["spotify"], "question": "Ascolto più musica latina/reggaeton o italiana? Dammi qualche esempio concreto dai miei artisti più ascoltati."},
    {"id": "spotify_14", "domains": ["spotify"], "question": "Ascolto più da telefono, da computer o trasmettendo su TV (Chromecast)?"},
    {"id": "spotify_15", "domains": ["spotify"], "question": "Quante volte ho usato la modalità incognito su Spotify, e cosa ascoltavo in quei casi rispetto al solito?"},
    # chess: grounded in the real most-played opponent (Kenpachi-97, 5
    # games), the real time-control distribution (300s/600s dominant, both
    # correctly bucketed as "blitz" per chess.com's own thresholds; 60s/180s
    # as "bullet"), and the real full date range (2022-05-27 to 2026-09-11).
    {"id": "chess_09", "domains": ["chessdotcom"], "question": "Contro quale avversario ho giocato più partite in assoluto, e qual è il bilancio (vittorie/sconfitte/pareggi) tra noi due?"},
    {"id": "chess_10", "domains": ["chessdotcom"], "question": "Gioco più partite in bullet o in blitz? Dammi i due conteggi."},
    {"id": "chess_11", "domains": ["chessdotcom"], "question": "Qual è stata la mia ultima partita di scacchi in assoluto, e come è andata?"},
    # cross-domain: grounded in the real overlapping windows (Trade
    # Republic Feb2025-Aug2026 fully overlaps both chess's 2022-2026 range
    # and spotify's Oct2025-Aug2026 window).
    {"id": "cross_06", "domains": ["money", "chessdotcom", "spotify"], "question": "Nei mesi in cui ho investito di più su Trade Republic, il mio modo di giocare a scacchi o ascoltare musica è cambiato rispetto agli altri mesi?"},
]


# ==============================================================================
# HARNESS
# ==============================================================================

def run_batch(
    questions: List[Dict[str, Any]],
    llm: "lb.LLMClient",
    max_iterations: int,
    already_done: Optional[Dict[str, Dict[str, Any]]] = None,
    on_progress: Optional[Callable[[List[Dict[str, Any]]], None]] = None,
) -> List[Dict[str, Any]]:
    """
    2026-09-14 UPDATE 3 (overnight cross-domain batch): two changes.

    (1) Restored per-call `result` capture and `malformed_tool_call_recoveries`
    in each entry. QueryResult.tool_results/.malformed_tool_call_recoveries
    have existed on llm_bridge.py's return value since the spotify bridge
    fix (see EVOLUTION_LOG.md) — but THIS harness never actually read them
    back out. Confirmed by inspecting the real money_04/money_05 reports
    from the Pi (2026-09-14): tool_calls_made entries had no "result" key
    and there was no per-question malformed_tool_call_recoveries anywhere,
    even though llm_bridge.py was already computing both. A real reporting
    gap, not a data/ingest bug — silently throwing away exactly the kind
    of detail ("raccogliere quante più informazioni possibili") this whole
    harness exists for. Fixed by zipping tool_calls_made with tool_results,
    same pattern already proven correct elsewhere.

    (2) `already_done` (question id -> previous result entry) lets a
    resumed run skip questions a prior, interrupted run already completed
    — see --resume in main(). `on_progress`, called with the full results
    list after every question, is how main() checkpoints to disk without
    run_batch needing to know anything about file paths.
    """
    results: List[Dict[str, Any]] = []
    already_done = already_done or {}

    for i, item in enumerate(questions, start=1):
        if item["id"] in already_done:
            print(f"\n[{i}/{len(questions)}] ({item['id']}) SALTATA — già presente nel report da cui si riprende.")
            results.append(already_done[item["id"]])
            if on_progress:
                on_progress(results)
            continue

        print(f"\n[{i}/{len(questions)}] ({item['id']}) {item['question']}")
        t0 = time.time()
        entry: Dict[str, Any] = {
            "id": item["id"],
            "domains_tagged": item["domains"],
            "question": item["question"],
        }
        try:
            result = lb.run_query(item["question"], llm=llm, max_iterations=max_iterations)
            elapsed = time.time() - t0
            # zip(tool_calls_made, tool_results): same order, same length,
            # guaranteed by run_query() — each is appended once per real or
            # short-circuited call, in lockstep.
            entry.update({
                "success": True,
                "answer": result.answer,
                "iterations_used": result.iterations_used,
                "hit_max_iterations": result.hit_max_iterations,
                "malformed_tool_call_recoveries": result.malformed_tool_call_recoveries,
                "tool_calls_made": [
                    {"tool": name, "arguments": args, "result": res}
                    for (name, args), res in zip(result.tool_calls_made, result.tool_results)
                ],
                "elapsed_seconds": round(elapsed, 2),
            })
            print(f"  -> {result.iterations_used} iterazioni, {len(result.tool_calls_made)} tool call, "
                  f"{elapsed:.1f}s{' (MAX_ITERATIONS raggiunto)' if result.hit_max_iterations else ''}"
                  f"{f' ({result.malformed_tool_call_recoveries} tool-call malformata recuperata)' if result.malformed_tool_call_recoveries else ''}")
            print(f"  Risposta: {result.answer[:200]}{'...' if len(result.answer) > 200 else ''}")
        except Exception as exc:
            elapsed = time.time() - t0
            entry.update({
                "success": False,
                "error": str(exc),
                "elapsed_seconds": round(elapsed, 2),
            })
            print(f"  -> ERRORE dopo {elapsed:.1f}s: {exc}")

        results.append(entry)
        if on_progress:
            on_progress(results)

    return results


def summarize(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    2026-09-14: rebuilt for the 3-tool architecture. The old
    primary_vs_full_access breakdown (search/get_aggregation vs
    resolve_full_ref call counts) doesn't map to anything real anymore —
    there's no PRIMARY/FULL split, just list_tables/describe_table/
    run_sql. tool_calls_by_tool below is the direct replacement: how many
    times each of the 3 real tools was actually called across the batch.
    Also tracks every run_sql query text verbatim, alongside a compact
    view of what it actually returned (run_sql_queries) — row_count/
    truncated/error only, not the full row data (that's still in each
    question's own tool_calls_made -> result, in `results`, if needed) —
    since that's exactly the kind of detail needed to diagnose a case
    like the 2026-09-14 media_type/content_type mix-up, or tell apart a
    genuine sql_error from the model just misreading a clean result,
    without digging back through each result individually.
    """
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    hit_max = [r for r in successful if r.get("hit_max_iterations")]

    tool_call_counts: Dict[str, int] = {}
    run_sql_queries: List[Dict[str, Any]] = []
    for r in successful:
        for call in r.get("tool_calls_made", []):
            tool_name = call.get("tool", "(unknown)")
            tool_call_counts[tool_name] = tool_call_counts.get(tool_name, 0) + 1
            if tool_name == "run_sql":
                result_obj = call.get("result") or {}
                run_sql_queries.append({
                    "question_id": r["id"],
                    "query": call.get("arguments", {}).get("query", ""),
                    "error": result_obj.get("error"),
                    "row_count": result_obj.get("row_count"),
                    "truncated": result_obj.get("truncated", False),
                })

    recovered = [r for r in successful if r.get("malformed_tool_call_recoveries")]

    return {
        "total_questions": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "hit_max_iterations_count": len(hit_max),
        "hit_max_iterations_ids": [r["id"] for r in hit_max],
        "failed_ids": [r["id"] for r in failed],
        "malformed_tool_call_recoveries_count": sum(r.get("malformed_tool_call_recoveries", 0) for r in successful),
        "malformed_tool_call_recoveries_ids": [r["id"] for r in recovered],
        "avg_iterations": round(sum(r["iterations_used"] for r in successful) / len(successful), 2) if successful else None,
        "avg_elapsed_seconds": round(sum(r["elapsed_seconds"] for r in results) / len(results), 2) if results else None,
        "total_elapsed_seconds": round(sum(r["elapsed_seconds"] for r in results), 2),
        "tool_calls_by_tool": tool_call_counts,
        "run_sql_queries": run_sql_queries,
    }


def _write_report_atomically(report: Dict[str, Any], output_path: Path) -> None:
    """
    2026-09-14 UPDATE 3: writes go to a sibling .tmp file, then
    os.replace() to the real path — os.replace is atomic on both Linux
    (the Pi) and Windows, so a process killed mid-write (power loss, OOM
    kill, kill -9) leaves either the OLD complete report or nothing at
    the .tmp path, never a half-written/corrupt JSON at output_path
    itself. Called after every single question (see run_batch's
    on_progress), not just at the end — see module docstring's
    "checkpointing" section for why this exists.
    """
    tmp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    tmp_path.replace(output_path)


def main() -> None:
    # Line-buffered stdout: under `nohup ... > run.log 2>&1 &` (recommended
    # for an unattended overnight run — see module docstring), Python's
    # default full buffering on a redirected-to-file stdout means `tail -f
    # run.log` shows nothing for a long time, then a big chunk all at once.
    # Reconfiguring to line buffering makes progress visible in real time.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Batch real-model evaluation of llm_bridge.py against real data.")
    parser.add_argument("--model", default=lb.OLLAMA_DEFAULT_MODEL, help=f"Ollama model name (default: {lb.OLLAMA_DEFAULT_MODEL})")
    parser.add_argument("--host", default=lb.OLLAMA_DEFAULT_HOST, help=f"Ollama server host (default: {lb.OLLAMA_DEFAULT_HOST})")
    parser.add_argument("--max-iterations", type=int, default=lb.MAX_ITERATIONS, help=f"Per-question MAX_ITERATIONS override (default: {lb.MAX_ITERATIONS})")
    parser.add_argument("--request-timeout", type=float, default=None, help="Per-HTTP-call timeout in seconds for the Ollama backend (default: OllamaClient's own default, currently 600s). Lower this for an overnight batch so one hung call fails fast instead of eating up to 600s x max_iterations on a single question.")
    parser.add_argument("--output", default=None, help="Output JSON report path (default: batch_report_<backend>_<UTC timestamp>.json). Also the checkpoint path: written after EVERY question, not just at the end (see --resume).")
    parser.add_argument("--resume", default=None, help="Path to a previous (possibly partial/interrupted) report JSON. Questions whose id already has an entry there are skipped and their old entry is kept verbatim; everything else runs normally. If --output is not also given, checkpoints continue writing to this same --resume path, so a crashed overnight run restarts with the same command plus --resume <path> and picks up where it left off.")
    parser.add_argument("--only", default=None, help="Comma-separated domain names — run only questions tagged with at least one of these domains (manifest/cross-domain questions with no tag always run).")
    parser.add_argument("--extended", action="store_true", help="Also include EXTENDED_QUESTIONS (edge cases, adversarial/ambiguous phrasing, stress tests) on top of the standard set.")
    parser.add_argument("--ids", default=None, help="Comma-separated EXACT question ids to run (e.g. money_01,money_04,cross_02) — searches both QUESTIONS and EXTENDED_QUESTIONS regardless of --extended/--only, and overrides them when set. For small, targeted, low-token runs (e.g. a cloud-model comparison on one known-broken case).")
    parser.add_argument("--backend", choices=["ollama", "claude", "together"], default="ollama", help="Which LLMClient to run against: the local Ollama server (default), the real Anthropic API (--backend claude, needs ANTHROPIC_API_KEY set and `pip install anthropic`), or Together AI's OpenAI-compatible API (--backend together, needs TOGETHER_API_KEY set — see TogetherAIClient's docstring in llm_bridge.py, NOT live-tested as of 2026-09-15).")
    parser.add_argument("--think", action="store_true", help="Ollama backend only: allow the model's extended 'thinking' mode instead of the bridge's 2026-09-17 default of disabling it (OllamaClient now sends think:false unless this flag is set). See llm_bridge.py's module docstring, 'EMPTY FINAL ANSWER' section, for why the default changed — pass --think to A/B-compare against the old (thinking-enabled) behavior on a real batch.")
    args = parser.parse_args()

    all_known_questions = QUESTIONS + EXTENDED_QUESTIONS

    if args.ids:
        wanted_ids = [q.strip() for q in args.ids.split(",") if q.strip()]
        by_id = {q["id"]: q for q in all_known_questions}
        questions = [by_id[qid] for qid in wanted_ids if qid in by_id]
        missing = [qid for qid in wanted_ids if qid not in by_id]
        if missing:
            print(f"ATTENZIONE: id sconosciuti, ignorati: {missing}")
        print(f"Filtro --ids: {len(questions)} domande selezionate.")
    else:
        questions = QUESTIONS + EXTENDED_QUESTIONS if args.extended else list(QUESTIONS)
        if args.only:
            wanted = {d.strip() for d in args.only.split(",") if d.strip()}
            questions = [q for q in questions if not q["domains"] or wanted.intersection(q["domains"])]
            print(f"Filtro --only={sorted(wanted)}: {len(questions)}/{len(all_known_questions)} domande selezionate.")

    if args.backend == "claude":
        llm: lb.LLMClient = lb.ClaudeAPIClient(model=args.model if args.model != lb.OLLAMA_DEFAULT_MODEL else "claude-sonnet-5")
        model_label = llm.model
        host_label = "(Anthropic API, non Ollama)"
    elif args.backend == "together":
        together_kwargs: Dict[str, Any] = {}
        if args.request_timeout is not None:
            together_kwargs["timeout_seconds"] = args.request_timeout
        default_together_model = "Qwen/Qwen2.5-14B-Instruct"
        llm = lb.TogetherAIClient(model=args.model if args.model != lb.OLLAMA_DEFAULT_MODEL else default_together_model, **together_kwargs)
        model_label = llm.model
        host_label = "(Together AI API, non Ollama)"
    else:
        ollama_kwargs: Dict[str, Any] = {"think": args.think}
        if args.request_timeout is not None:
            ollama_kwargs["timeout_seconds"] = args.request_timeout
        llm = lb.OllamaClient(model=args.model, host=args.host, **ollama_kwargs)
        model_label = args.model
        host_label = args.host

    active_domains = sorted(ingest_engine.DOMAIN_REGISTRY.keys())

    # --- resume support (2026-09-14 UPDATE 3) ---------------------------
    # Load a previous (possibly partial) report, keep its already-completed
    # question entries verbatim, and default the checkpoint/output path to
    # the SAME file unless --output overrides it — so the natural recovery
    # command after a crash is just the original command plus
    # `--resume <same path>`.
    already_done: Dict[str, Dict[str, Any]] = {}
    if args.resume:
        resume_path = Path(args.resume)
        try:
            with resume_path.open("r", encoding="utf-8") as f:
                previous_report = json.load(f)
            for entry in previous_report.get("results", []):
                if entry.get("id"):
                    already_done[entry["id"]] = entry
            print(f"Ripresa da {resume_path}: {len(already_done)} domande già completate verranno saltate.")
        except Exception as exc:
            print(f"ATTENZIONE: impossibile leggere --resume {resume_path}: {exc}. Si riparte da zero.")

    output_path = Path(args.output) if args.output else (
        Path(args.resume) if args.resume else
        Path(f"batch_report_{args.backend}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
    )

    print(f"Backend: {args.backend}  Modello: {model_label}  Host: {host_label}  MAX_ITERATIONS: {args.max_iterations}")
    print(f"Domini registrati in questa architettura: {active_domains}")
    print(f"Esecuzione di {len(questions)} domande ({len(already_done)} già completate, {len(questions) - sum(1 for q in questions if q['id'] in already_done)} da eseguire davvero)...")
    print(f"Checkpoint/report scritto dopo OGNI domanda in: {output_path.resolve()}")

    def _checkpoint(partial_results: List[Dict[str, Any]], started_at: float, status: str) -> None:
        partial_summary = summarize(partial_results)
        partial_report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": status,  # "in_progress" until the batch finishes, then "completed"
            "backend": args.backend,
            "model": model_label,
            "host": host_label,
            "max_iterations": args.max_iterations,
            "registered_domains": active_domains,
            "batch_elapsed_seconds": round(time.time() - started_at, 2),
            "summary": partial_summary,
            "results": partial_results,
        }
        _write_report_atomically(partial_report, output_path)

    batch_start = time.time()
    results = run_batch(
        questions,
        llm=llm,
        max_iterations=args.max_iterations,
        already_done=already_done,
        on_progress=lambda partial: _checkpoint(partial, batch_start, "in_progress"),
    )
    batch_elapsed = time.time() - batch_start
    summary = summarize(results)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "backend": args.backend,
        "model": model_label,
        "host": host_label,
        "max_iterations": args.max_iterations,
        "registered_domains": active_domains,
        "batch_elapsed_seconds": round(batch_elapsed, 2),
        "summary": summary,
        "results": results,
    }
    _write_report_atomically(report, output_path)

    print(f"\n{'=' * 70}\nRIEPILOGO\n{'=' * 70}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nReport completo scritto in: {output_path.resolve()}")
    print("Manda questo file per l'analisi.")


if __name__ == "__main__":
    main()
