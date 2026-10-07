# whatsapp_ingest.py
# =============================================================================
# WHATSAPP INGEST — Personal Data Vault (Messaging domain)
# =============================================================================
#
# STANDARD COMPLIANCE (see timelive.md)
# -----------------------------------------------------------------------
# Fifth domain on top of the shared library in main.py (timelive.md, Part
# VI). Roadmap item 5 in §10's "candidate future domains" list, explicitly
# flagged there as needing a deliberate, up-front decision on message-
# content sensitivity before starting — see the PRIVACY DECISION note
# below, agreed with the project owner before any line of this file was
# written (timelive.md §10 v4.2 / §23: real data first, decide sensitivity
# before starting).
#
# INPUT FORMAT (inspected on two real exports — timelive.md §19/§23:
# inspect real data, don't assume)
# -----------------------------------------------------------------------
# WhatsApp's "Export chat" (without media) produces a `_chat.txt` file
# inside a folder named after the chat. The folder name is the only
# reliable human-readable identifier — the file itself is ALWAYS named
# `_chat.txt` regardless of which chat it is (confirmed against two real
# exports, one 1:1 and one group). Each line has the form:
#
#     [dd/mm/yyyy, hh:mm:ss] Sender Name: message text
#
# sometimes prefixed by U+200E (LEFT-TO-RIGHT MARK, invisible) — observed
# on almost every "system-like" line (media/call/system placeholders) and
# almost never on plain text lines. A message can span multiple physical
# lines: a continuation line does NOT match the header pattern above and
# must be re-attached to the previous message. The header regex is
# therefore intentionally strict (2-digit day/month, 4-digit year, exact
# HH:MM:SS) — a real message in the sample data contains a *pasted* chat
# excerpt whose embedded "header" (`[30/4 18:49] Name: ...`, no year, no
# seconds) would otherwise be mis-detected as a real message boundary.
#
# Real vocabulary observed and handled explicitly (extensible, not
# exhaustive — timelive.md §22: normalize what's understood, preserve the
# rest; an unrecognized system-like line simply falls through to
# message_type="text" with its raw text kept in FULL, nothing is lost):
#   * media placeholders: "image/video/audio/video note/sticker/GIF/
#     Contact card omitted"; documents additionally carry a filename and
#     page count before "document omitted".
#   * calls: "Video call. <Nmin|Nsec|No answer>", "Voice call. ...",
#     "Missed video/voice call. Tap to call back", "Call failed. Try
#     again", "Group call. N invited".
#   * deletion: "You deleted this message." (export owner deleted their
#     own message) vs "This message was deleted." (someone else's
#     deletion) — a NATIVE distinction WhatsApp itself encodes in the
#     text, not an inference.
#   * edits: original text is kept, with a trailing "<This message was
#     edited>" marker — WhatsApp exports only the final text, never edit
#     history, so this is just a boolean flag (was_edited), not lost data.
#   * location shares: "Location: https://maps.google.com/?q=lat,lon" —
#     structured GPS coordinates, a real cross-domain join key shared
#     with maps_ingest (timelive.md §4/§5).
#   * system/group events: "X created this group", "You were added",
#     "X left", "X removed Y", subject/icon/description changes, security
#     code changes, etc. For SOME of these lines the "sender" shown in the
#     header is not a real participant at all but the chat's own name
#     (observed on the real group export's opening encryption-notice and
#     "You were added" lines) — see build_chat_index below for how
#     `participants` filters this out.
#
# PRIVACY DECISION (agreed with the project owner before writing this
# file, resolving timelive.md §10's explicit "decide deliberately before
# starting" note for this domain)
# -----------------------------------------------------------------------
#   1. Message TEXT is kept in full ONLY in FULL (whatsapp_dataset_full.
#      json). PRIMARY (whatsapp_dataset.json) never contains free-text
#      message content — notable_messages exposes metadata only (sender,
#      timestamp, message_type, structural attributes) with full_ref
#      pointing into FULL for the actual text. This mirrors how FULL/
#      PRIMARY are already separated for every other domain, just drawn
#      more conservatively here because message content routinely
#      includes text WRITTEN BY THIRD PARTIES (the user's contacts) who
#      never consented to this ingest.
#   2. Location shares (structured lat/lon, not free text) are the one
#      exception: they ARE exposed in PRIMARY as `notable_locations`,
#      because they are structured data (not conversational content) and
#      a direct interoperability win with maps_ingest (same lat/lon
#      shape, timelive.md §4/§5) — explicitly decided as worth the extra
#      exposure versus message text.
#   3. Timestamps are kept NAIVE, exactly as exported, with no timezone
#      conversion — WhatsApp exports local device time with no explicit
#      offset, and (unlike a single-account domain) the "correct" zone can
#      genuinely change message to message while the phone travels. This
#      mirrors money_ingest's own documented naive-timestamp decision
#      rather than inventing a single assumed zone (timelive.md §18:
#      timezone handling must be explicit — "naive, undocumented
#      otherwise" is the explicit choice here, spelled out once here and
#      in _logic rather than silently assumed).
#
# SELF-IDENTIFICATION WITHOUT ASKING THE USER PER-CHAT
# -----------------------------------------------------------------------
# WhatsApp's own export text already distinguishes the export owner's
# actions natively: "You deleted this message.", "You were added", "You
# left", "You're now an admin", etc. only ever appear for the phone that
# produced the export — never for anyone else. detect_self_display_name
# harvests this native signal per chat (no configuration, no inference,
# no confidence_rate needed — it is as native as Apple Health's own
# category field, timelive.md §26 priority 1) and uses it to set
# `is_self` on every message in that chat. SELF_DISPLAY_NAMES below is
# only a manual override/fallback for a chat where no such native marker
# ever occurs (e.g. a very short chat with no deletions, no group
# events) — most chats need no configuration at all.
#
# OUTPUT FILES
# -----------------------------------------------------------------------
#     whatsapp_dataset.json        -> PRIMARY (LLM-oriented, budget-aware)
#     whatsapp_dataset_full.json   -> FULL    (analytical, normalized)
#
# One pair of files for the ENTIRE vault, aggregating every chat
# (timelive.md §11: exactly two outputs — not one pair per chat). Each
# chat is distinguished by `chat_id` throughout, and a small top-level
# `chats` index (present in full in both PRIMARY and FULL, small by
# construction) tells the LLM which conversations exist before it has to
# look at a single message — the messaging-domain analogue of maps'
# `trips` or spotify's `sessions` as a mid-level structure, but needed
# here specifically because, unlike every other domain, WhatsApp data is
# inherently many independent streams rather than one.
#
# GOAL
# -----------------------------------------------------------------------
#     RAW Input/WhatsApp/<chat folder>/_chat.txt (one folder per chat)
#         |
#         v
#     NORMALIZATION (header parsing, multi-line join, message classification)
#         |
#         v
#     DEDUPLICATION (shared mechanism, composite key — no native id)
#         |
#         v
#     CHAT INDEX (participants, is_group, self-detection) +
#     CONVERSATION BURST GROUPING + AGGREGATIONS + NOTABILITY SCORING
#         |
#         v
#     FULL  (all normalized messages + chats + bursts + aggregations)
#         |
#         v
#     PRIMARY (compact, budget-aware, privacy-light LLM-first view)
#
# HOW TO MODIFY ANY THRESHOLD/RULE
# -----------------------------------
# Every parameter is collected in the CONFIGURATION section below, exactly
# like the other four ingests.
# =============================================================================

from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------------------------------------------------------
# SHARED LIBRARY (main.py) — see timelive.md Part VI
# ----------------------------------------------------------------------------
from main import (
    write_json,
    estimate_json_size_bytes,
    check_full_size_warning,
    confidence_rate,
    CONFIDENCE_INFERRED_HIGH,
    compute_notability_scores as shared_compute_notability_scores,
    recency_weight,
    select_within_size_budget,
    deduplicate_records as shared_deduplicate_records,
    group_by_time_and_compatibility,
    build_metadata,
    build_schema,
    build_logic,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

# ----------------------------------------------------------------------------
# CONFIG — Paths (with fallback if a central config.py is not available)
# ----------------------------------------------------------------------------
try:
    from config import (
        WHATSAPP_INPUT_DIR,
        WHATSAPP_OUTPUT_DATASET_PATH,
        WHATSAPP_OUTPUT_FULL_DATASET_PATH,
    )
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    WHATSAPP_INPUT_DIR = BASE_DIR / "Input" / "WhatsApp"
    OUTPUT_DIR = BASE_DIR / "Output"
    WHATSAPP_OUTPUT_DATASET_PATH = OUTPUT_DIR / "whatsapp_dataset.json"
    WHATSAPP_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / "whatsapp_dataset_full.json"

WHATSAPP_INPUT_DIR = Path(WHATSAPP_INPUT_DIR)
WHATSAPP_OUTPUT_DATASET_PATH = Path(WHATSAPP_OUTPUT_DATASET_PATH)
WHATSAPP_OUTPUT_FULL_DATASET_PATH = Path(WHATSAPP_OUTPUT_FULL_DATASET_PATH)


# ----------------------------------------------------------------------------
# CONFIG — Dataset identity
# ----------------------------------------------------------------------------
SOURCE_PREFIX = "whatsapp"
DATASET_VERSION = "1.0"


# ----------------------------------------------------------------------------
# CONFIG — Input file detection
# ----------------------------------------------------------------------------
# Expected real layout: WHATSAPP_INPUT_DIR/<chat folder name>/_chat.txt —
# one subfolder per chat, named by WhatsApp's export flow, containing a
# chat export text file (always named "_chat.txt" in every real export
# inspected, but matched permissively below rather than by exact name, per
# timelive.md §22: don't hardcode a filename assumption tighter than what
# is actually needed).
#
# Fallback: a loose .txt file dropped directly in WHATSAPP_INPUT_DIR (not
# inside a chat subfolder) is still ingested — chat_id/display_name are
# then derived from the FILENAME instead of a folder name, and a warning
# is recorded, since the filename alone is a weaker identifier (WhatsApp
# itself names every chat file identically).
CHAT_FILE_PATTERN = re.compile(r".*\.txt$", re.IGNORECASE)


# ----------------------------------------------------------------------------
# CONFIG — Self-identification override (see module docstring — usually
# not needed, since detect_self_display_name derives this natively per
# chat from WhatsApp's own "You ..." phrasing)
# ----------------------------------------------------------------------------
# Populate with display name(s) known to be the export owner's own
# WhatsApp name, used ONLY as a fallback for a chat where no native
# self-referential marker ever appears. Matching is case-insensitive,
# exact (no partial/fuzzy match, to avoid false positives).
SELF_DISPLAY_NAMES: set = set()


# ----------------------------------------------------------------------------
# CONFIG — PRIVACY: message text visibility (see module docstring's
# PRIVACY DECISION — decided explicitly with the project owner, not a
# default that silently crept in)
# ----------------------------------------------------------------------------
PRIMARY_INCLUDE_MESSAGE_TEXT = False   # never expose free text in PRIMARY
PRIMARY_INCLUDE_LOCATIONS = True       # structured lat/lon IS exposed in PRIMARY


# ----------------------------------------------------------------------------
# CONFIG — PRUNING (same philosophy as the other four domains)
# ----------------------------------------------------------------------------
# none/light: also keep the original raw source line per message (useful
#             for debugging a misclassification) alongside the parsed
#             fields.
# medium (default): drop the raw line, keep only parsed/normalized fields.
# aggressive: like medium, and also drop source_file/record_index_in_source
#             bookkeeping fields for non-notable messages in FULL.
# Note: unlike every other domain's PRUNE_LEVEL, this NEVER controls
# whether message text itself survives in FULL — that is governed
# entirely by PRIMARY_INCLUDE_MESSAGE_TEXT above (a privacy decision, not
# a size/detail tradeoff) and message text is always present in FULL
# regardless of PRUNE_LEVEL.
# ----------------------------------------------------------------------------
PRUNE_LEVEL = "medium"
VALID_PRUNE_LEVELS = {"none", "light", "medium", "aggressive"}

FULL_WARNING_SIZE_GB = 0.5


# ----------------------------------------------------------------------------
# CONFIG — PRIMARY budget (target, not a hard limit)
# ----------------------------------------------------------------------------
PRIMARY_MAX_SIZE_MB = 20
PRIMARY_SOFT_OVERFLOW_RATIO = 0.20

PRIMARY_MIN_RECENT_DAYS_GUARANTEED = 14
PRIMARY_RECENT_GUARANTEE_BOOST = 1000.0

# Weights for the notability score of an individual message (feeding
# main.compute_notability_scores, timelive.md §16, §33):
#   - "type_richness": how much a message_type is worth surfacing on its
#     own vs. being represented only through aggregations (see
#     MESSAGE_TYPE_RICHNESS below).
#   - "recency": exponential decay via main.recency_weight.
#   - "long_call_bonus": flat bonus for calls lasting >= LONG_CALL_SECONDS.
NOTABILITY_WEIGHT_TYPE_RICHNESS = 0.5
NOTABILITY_WEIGHT_RECENCY = 0.4
NOTABILITY_WEIGHT_LONG_CALL_BONUS = 0.3
NOTABILITY_RECENCY_HALF_LIFE_DAYS = 60
LONG_CALL_SECONDS = 5 * 60

# A message_type's inherent "worth surfacing individually" score, used by
# the type_richness signal. Deliberately excludes any notion of message
# LENGTH (which would require reading text content — PRIMARY never does).
MESSAGE_TYPE_RICHNESS = {
    "location": 1.0,
    "call": 0.9,
    "document": 0.7,
    "contact_card": 0.6,
    "text": 0.5,
    "image": 0.4,
    "video": 0.4,
    "video_note": 0.4,
    "gif": 0.3,
    "sticker": 0.2,
    "deleted": 0.3,
    "system_event": 0.2,
    "empty": 0.0,
}


# ----------------------------------------------------------------------------
# CONFIG — Conversation burst grouping (timelive.md §29: time proximity
# alone still needs a documented threshold; unlike bank/health/maps, this
# domain has no separate semantic-compatibility axis to combine it with —
# within a single chat, ANY two messages close in time belong to the same
# active exchange regardless of type, so is_compatible is trivially True
# and the generic framework (main.group_by_time_and_compatibility) applies
# directly, called once per chat_id since a burst never spans two chats.)
# ----------------------------------------------------------------------------
BURST_MAX_GAP_SECONDS = 45 * 60  # 45 minutes of silence ends a burst
BURST_MIN_MESSAGES = 3           # fewer than this is just a stray exchange
BURST_GROUPING_CONFIDENCE = CONFIDENCE_INFERRED_HIGH


# ----------------------------------------------------------------------------
# CONFIG — Temporal aggregations
# ----------------------------------------------------------------------------
AGGREGATION_GRANULARITIES = ("daily", "weekly", "monthly")
AGGREGATION_TOP_N_SENDERS = 20


# ============================================================================
# UTILITY — normalization and parsing
# ============================================================================

_LRM = "‎"


def strip_lrm(text: str) -> str:
    return text.replace(_LRM, "")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


# Strict on purpose — see module docstring for the real false-positive
# this strictness avoids (a pasted chat excerpt embedded in a message's
# own text, which uses a looser d/m HH:MM format with no year/seconds).
_HEADER_RE = re.compile(
    r"^‎?\[(?P<date>\d{2}/\d{2}/\d{4}), (?P<time>\d{2}:\d{2}:\d{2})\] "
    r"(?P<sender>.*?): (?P<body>.*)$"
)


def parse_header_timestamp(date_str: str, time_str: str) -> Optional[datetime]:
    """
    dd/mm/yyyy + HH:MM:SS -> naive datetime. Never raises; returns None on
    an unparseable value rather than inventing a fallback (timelive.md
    §22). No timezone is attached or assumed — see the PRIVACY DECISION
    note in the module docstring for why this stays naive.
    """
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M:%S")
    except ValueError:
        return None


def to_naive_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat()


def sanitize_identifier(raw: str) -> str:
    """Turns a folder/file name into a stable, readable chat_id (timelive.md §19)."""
    normalized = re.sub(r"\s+", "_", raw.strip().lower())
    normalized = re.sub(r"[^a-z0-9_\-]", "", normalized)
    return normalized or "unknown_chat"


# ============================================================================
# INPUT FILE DISCOVERY
# ============================================================================

def collect_chat_sources(input_dir: Path) -> Tuple[List[Tuple[str, str, List[Path]]], List[str]]:
    """
    Returns (chat_sources, warnings) where chat_sources is a list of
    (chat_id, display_name, [chat text files]) — one entry per detected
    chat. Preferred layout: one subfolder per chat, containing one or more
    *.txt export files (merged and deduplicated, mirroring how
    spotify_ingest merges multiple per-year files for one source). Loose
    *.txt files directly in input_dir are also accepted as a fallback (see
    CHAT_FILE_PATTERN's comment) — identified by filename instead of
    folder name, with a warning.
    """
    warnings: List[str] = []
    chat_sources: List[Tuple[str, str, List[Path]]] = []

    if not input_dir.exists():
        return chat_sources, warnings

    for entry in sorted(input_dir.iterdir(), key=lambda p: p.name.lower()):
        if entry.is_dir():
            txt_files = sorted(
                (p for p in entry.iterdir() if p.is_file() and CHAT_FILE_PATTERN.match(p.name)),
                key=lambda p: p.name.lower(),
            )
            if not txt_files:
                continue
            display_name = entry.name.strip()
            chat_id = sanitize_identifier(display_name)
            chat_sources.append((chat_id, display_name, txt_files))

    # Fallback: loose .txt files directly in input_dir (not inside a chat
    # subfolder). Real WhatsApp exports always use a folder, so this path
    # is a convenience for a manually-copied single export, not the
    # expected common case — flagged with a warning accordingly.
    loose_files = sorted(
        (p for p in input_dir.iterdir() if p.is_file() and CHAT_FILE_PATTERN.match(p.name)),
        key=lambda p: p.name.lower(),
    )
    for loose_file in loose_files:
        display_name = loose_file.stem.strip()
        chat_id = sanitize_identifier(display_name)
        chat_sources.append((chat_id, display_name, [loose_file]))
        warnings.append(
            f"'{loose_file.name}' was found directly in {input_dir}, not inside a "
            f"per-chat subfolder. Identified as chat_id='{chat_id}' from its "
            f"filename instead of a folder name — less reliable, since real "
            f"WhatsApp exports always name the file itself '_chat.txt' "
            f"regardless of which chat it is. Prefer the folder-per-chat layout."
        )

    return chat_sources, warnings


def read_text_with_fallback_encoding(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except Exception:
            continue
    raise RuntimeError(f"Could not read {path} with any known encoding.")


# ============================================================================
# NORMALIZATION — header parsing + multi-line joining
# ============================================================================

def split_into_raw_messages(raw_text: str, source_file: Path) -> List[Dict[str, Any]]:
    """
    Splits one chat export's raw text into a list of raw message dicts
    (date_str, time_str, sender, body, record_index_in_source), joining
    continuation lines (lines that don't match _HEADER_RE) onto the
    previous message's body with a newline. See module docstring for why
    the header regex is deliberately strict.
    """
    text = normalize_newlines(raw_text)
    lines = text.split("\n")

    messages: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None
    index = 0

    for line in lines:
        match = _HEADER_RE.match(line)
        if match:
            if current is not None:
                messages.append(current)
            current = {
                "date_str": match.group("date"),
                "time_str": match.group("time"),
                "sender": strip_lrm(match.group("sender")).strip(),
                "body": strip_lrm(match.group("body")),
                "record_index_in_source": index,
                "source_file": source_file.name,
            }
            index += 1
        else:
            if current is None:
                # Leading junk before the first real header (rare) — not a
                # continuation of anything, safely ignored rather than
                # crashing (timelive.md §22 spirit: don't fail on the
                # unexpected, preserve what can be preserved).
                continue
            stripped_line = strip_lrm(line)
            if stripped_line == "" and current["body"] == "":
                continue
            current["body"] = (current["body"] + "\n" + stripped_line) if current["body"] else stripped_line

    if current is not None:
        messages.append(current)

    return messages


# ============================================================================
# CLASSIFICATION — message type + structural fields
# ============================================================================

_MEDIA_SUFFIX_TYPES = [
    ("video note omitted", "video_note"),
    ("image omitted", "image"),
    ("video omitted", "video"),
    ("audio omitted", "audio"),
    ("sticker omitted", "sticker"),
    ("GIF omitted", "gif"),
    ("Contact card omitted", "contact_card"),
]

_DOCUMENT_RE = re.compile(
    r"^(?P<filename>.+?)\s*•\s*(?P<pages>\d+)\s*pages?\s*document omitted$"
)

_CALL_RE = re.compile(
    r"^(?P<prefix>Missed video call|Missed voice call|Video call|Voice call|Call failed|Group call)\.\s*(?P<detail>.*)$"
)

_CALL_DURATION_RE = re.compile(r"^(?P<value>\d+)\s*(?P<unit>min|sec)$")

_LOCATION_RE = re.compile(
    r"^Location:\s*https://maps\.google\.com/\?q=(?P<lat>-?\d+(?:\.\d+)?),(?P<lon>-?\d+(?:\.\d+)?)"
)

_EDITED_SUFFIX_RE = re.compile(r"\s*<This message was edited>\s*$")

# Anchored, deliberately specific phrasings — false negatives (an
# unmatched system-like line falling back to message_type="text") are
# safe by design (full text is preserved in FULL regardless, timelive.md
# §22); this list is extensible, not exhaustive.
_SYSTEM_EVENT_PATTERNS = [
    (re.compile(r"^Messages and calls are end-to-end encrypted\b.*$"), "encryption_notice"),
    (re.compile(r"^(?:You|.+) created this group$"), "group_created"),
    (re.compile(r"^You were added$"), "participant_added"),
    (re.compile(r"^(?:You|.+) added .+$"), "participant_added"),
    (re.compile(r"^(?:You|.+) removed .+$"), "participant_removed"),
    (re.compile(r"^(?:You|.+) left$"), "participant_left"),
    (re.compile(r"^(?:You|.+) changed the subject to .+$"), "subject_changed"),
    (re.compile(r"^(?:You|.+) changed this group.s icon$"), "icon_changed"),
    (re.compile(r"^(?:You|.+) changed the group description$"), "description_changed"),
    (re.compile(r"^Your security code with .+ changed\.?$"), "security_code_changed"),
    (re.compile(r"^(?:You|.+) is now an admin$"), "admin_granted"),
    (re.compile(r"^You.re now an admin$"), "admin_granted"),
    (re.compile(r"^(?:You|.+) changed their phone number to a new number\b.*$"), "phone_number_changed"),
    (re.compile(r"^This chat is with a business account\b.*$"), "business_account_notice"),
]


def classify_message(sender: str, body: str) -> Dict[str, Any]:
    """
    Returns the structural, non-text fields describing a message's type.
    Order matters: deletion/edit/call/location/media/system are all
    checked via anchored patterns before falling back to plain text, so a
    genuine text message that happens to contain e.g. the word "added"
    mid-sentence is never misclassified (the patterns above match the
    ENTIRE body, not a substring).
    """
    was_edited = False
    working_body = body

    edited_match = _EDITED_SUFFIX_RE.search(working_body)
    if edited_match:
        was_edited = True
        working_body = working_body[: edited_match.start()]

    stripped = working_body.strip()

    if stripped in ("You deleted this message.", "You deleted this message"):
        return {"message_type": "deleted", "deleted_by_export_owner": True, "was_edited": was_edited}
    if stripped in ("This message was deleted.", "This message was deleted"):
        return {"message_type": "deleted", "deleted_by_export_owner": False, "was_edited": was_edited}

    call_match = _CALL_RE.match(stripped)
    if call_match:
        prefix = call_match.group("prefix")
        detail = call_match.group("detail").strip()
        call_type = "video" if "video" in prefix.lower() else ("voice" if "voice" in prefix.lower() else (
            "group" if prefix == "Group call" else "unknown"
        ))
        call_outcome = "answered"
        duration_seconds = None
        if prefix.startswith("Missed"):
            call_outcome = "missed"
        elif prefix == "Call failed":
            call_outcome = "failed"
        elif detail == "No answer":
            call_outcome = "no_answer"
        elif "invited" in detail:
            call_outcome = "group_invite"
        duration_match = _CALL_DURATION_RE.match(detail)
        if duration_match:
            value = int(duration_match.group("value"))
            duration_seconds = value * 60 if duration_match.group("unit") == "min" else value
        return {
            "message_type": "call",
            "call_type": call_type,
            "call_outcome": call_outcome,
            "duration_seconds": duration_seconds,
            "was_edited": was_edited,
        }

    location_match = _LOCATION_RE.match(stripped)
    if location_match:
        return {
            "message_type": "location",
            "latitude": float(location_match.group("lat")),
            "longitude": float(location_match.group("lon")),
            "was_edited": was_edited,
        }

    document_match = _DOCUMENT_RE.match(stripped)
    if document_match:
        return {
            "message_type": "document",
            "document_filename": document_match.group("filename").strip(),
            "document_pages": int(document_match.group("pages")),
            "was_edited": was_edited,
        }

    for suffix, media_type in _MEDIA_SUFFIX_TYPES:
        if stripped == suffix:
            return {"message_type": media_type, "was_edited": was_edited}

    for pattern, event_type in _SYSTEM_EVENT_PATTERNS:
        if pattern.match(stripped):
            return {
                "message_type": "system_event",
                "system_event_type": event_type,
                "is_self_action": stripped.startswith("You "),
                "was_edited": was_edited,
            }

    if not stripped:
        return {"message_type": "empty", "was_edited": was_edited}

    return {"message_type": "text", "text": working_body.strip("\n"), "was_edited": was_edited}


# ============================================================================
# SELF-IDENTIFICATION (native, per chat — see module docstring)
# ============================================================================

def detect_self_display_name(messages: List[Dict[str, Any]]) -> Optional[str]:
    """
    Harvests WhatsApp's own "You ..." phrasing (self-referential system
    events, own-message deletions) to find which sender name is the
    export owner in THIS chat. Returns the name if every such marker
    agrees, else None (ambiguous or no marker present at all — falls back
    to SELF_DISPLAY_NAMES, or stays unknown).
    """
    candidates: set = set()
    for message in messages:
        if message.get("message_type") == "deleted" and message.get("deleted_by_export_owner"):
            candidates.add(message["sender"])
        elif message.get("message_type") == "system_event" and message.get("is_self_action"):
            candidates.add(message["sender"])
    if len(candidates) == 1:
        return next(iter(candidates))
    return None


# ============================================================================
# DEDUPLICATION
# ============================================================================
# No native per-message id exists in the export, so deduplication always
# uses a composite key (same pattern as spotify/health/maps). Delegated to
# main.deduplicate_records (timelive.md §25, §37).
#
# WHATSAPP-SPECIFIC WRINKLE, found on real data (timelive.md §23/§46: real
# data volume surfaces bugs a small fixture never would): WhatsApp
# timestamps only have SECOND granularity, and media bursts routinely put
# many messages from the same sender, of the same type (e.g. "image
# omitted", no distinguishing text at all), in the very same second — the
# real group export has 21 "image omitted" messages from one sender at one
# identical timestamp. A naive (chat_id, timestamp, sender, type, text)
# key would treat 20 of those 21 real, distinct images as "duplicates" of
# the first and silently delete them — exactly the kind of false-positive
# §25 warns against ("do not remove records simply because they look
# similar"). _assign_occurrence_within_file adds a same-signature
# occurrence counter, computed per SOURCE FILE in original parse order,
# to the key: within one file this makes each of the 21 images distinct
# (occurrence 1, 2, 3, ...), while two DIFFERENT files that legitimately
# re-export the same overlapping period (the actual case deduplication
# exists to catch) still collide 1:1 on both signature AND occurrence
# number, and are still correctly deduplicated. Accepted tradeoff,
# documented per §25: if a re-export reorders same-signature messages
# relative to each other, occurrence numbers could mismatch and a true
# duplicate could slip through — safer than the alternative failure mode
# (silently destroying real messages).

def _assign_occurrence_within_file(records: List[Dict[str, Any]]) -> None:
    counters: Dict[Tuple, int] = defaultdict(int)
    for record in records:
        signature = (
            record.get("source_file", ""),
            record.get("chat_id", ""),
            record.get("begin_timestamp", ""),
            record.get("sender", ""),
            record.get("message_type", ""),
            (record.get("text") or "")[:120],
        )
        counters[signature] += 1
        record["_occurrence_in_file"] = counters[signature]


def _composite_dedup_key(record: Dict[str, Any]) -> Tuple:
    return (
        record.get("chat_id", ""),
        record.get("begin_timestamp", ""),
        record.get("sender", ""),
        record.get("message_type", ""),
        (record.get("text") or "")[:120],
        record.get("_occurrence_in_file", 0),
    )


def deduplicate_messages(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Must be called BEFORE any reordering (chronological sort, etc.) — the
    occurrence counter's meaning depends on original per-file parse order.
    """
    _assign_occurrence_within_file(records)
    deduped, removed = shared_deduplicate_records(
        records,
        native_id_field=None,
        composite_key_fn=_composite_dedup_key,
    )
    for record in deduped:
        record.pop("_occurrence_in_file", None)
    return deduped, removed


# ============================================================================
# CHAT INDEX — participants, is_group, self-detection
# ============================================================================

_GROUP_EVENT_TYPES = {
    "group_created", "participant_added", "participant_removed",
    "participant_left", "subject_changed", "icon_changed",
    "description_changed", "admin_granted",
}


def build_chat_index_entry(chat_id: str, display_name: str, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    One entry per detected chat, always kept in full in both PRIMARY and
    FULL (this domain's analogue of maps' trips / spotify's sessions as a
    small, always-useful mid-level structure — see module docstring for
    why WhatsApp specifically needs this and the other domains don't).

    `participants` intentionally excludes senders whose ONLY appearances
    are on system_event messages — on the real group export, the chat's
    own name is used as the "sender" of the opening encryption notice and
    an early "You were added" line, which is not a real participant.
    """
    non_system_senders = {
        m["sender"] for m in messages if m.get("message_type") != "system_event" and m.get("sender")
    }
    any_group_event = any(m.get("system_event_type") in _GROUP_EVENT_TYPES for m in messages)
    is_group = any_group_event or len(non_system_senders) > 2

    timestamps = [m["begin_timestamp"] for m in messages if m.get("begin_timestamp")]
    self_name = detect_self_display_name(messages)
    if self_name is None:
        matches = {name for name in non_system_senders if name.lower() in {s.lower() for s in SELF_DISPLAY_NAMES}}
        if len(matches) == 1:
            self_name = next(iter(matches))

    return {
        "chat_id": chat_id,
        "display_name": display_name,
        "is_group": is_group,
        "participants": sorted(non_system_senders),
        "self_display_name": self_name,
        "self_display_name_source": "native_you_marker" if detect_self_display_name(messages) else (
            "config_override" if self_name else None
        ),
        "message_count": len(messages),
        "timestamp_begin": min(timestamps) if timestamps else None,
        "timestamp_end": max(timestamps) if timestamps else None,
    }


def apply_is_self(messages: List[Dict[str, Any]], self_display_name: Optional[str]) -> None:
    for message in messages:
        if self_display_name is None:
            message["is_self"] = None
        else:
            message["is_self"] = message.get("sender", "").lower() == self_display_name.lower()


# ============================================================================
# CONVERSATION BURST GROUPING (timelive.md §29)
# ============================================================================

def detect_conversation_bursts(chat_id: str, messages: List[Dict[str, Any]], counter_start: int) -> List[Dict[str, Any]]:
    """
    `messages` must be one chat's messages, already sorted chronologically.
    See the BURST_* CONFIG comment for why is_compatible is trivially True
    here (unlike bank/health/maps, there is no second semantic axis to
    combine time proximity with within a single conversation).
    """
    groups = group_by_time_and_compatibility(
        messages,
        timestamp_begin_field="begin_timestamp",
        timestamp_end_field="end_timestamp",
        max_gap_seconds=BURST_MAX_GAP_SECONDS,
        is_compatible=lambda a, b: True,
    )

    bursts: List[Dict[str, Any]] = []
    counter = counter_start
    for group in groups:
        if len(group) < BURST_MIN_MESSAGES:
            continue
        counter += 1
        distinct_senders = sorted({m["sender"] for m in group if m.get("message_type") != "system_event"})
        by_type: Dict[str, int] = defaultdict(int)
        for m in group:
            by_type[m.get("message_type", "unknown")] += 1

        bursts.append({
            "burst_id": f"{SOURCE_PREFIX}_burst_{counter}",
            "chat_id": chat_id,
            "timestamp_begin": group[0].get("begin_timestamp"),
            "timestamp_end": group[-1].get("end_timestamp"),
            "message_count": len(group),
            "distinct_sender_count": len(distinct_senders),
            "senders": distinct_senders,
            "message_type_counts": dict(by_type),
            "message_refs": [m["event_number"] for m in group],
            "confidence_rate": confidence_rate(BURST_GROUPING_CONFIDENCE),
        })

    return bursts, counter


# ============================================================================
# AGGREGATION — temporal buckets, per chat
# ============================================================================

def compute_bucket_bounds(dt: datetime, granularity: str) -> Tuple[datetime, datetime]:
    """Same bucketing logic as the other three domains (timelive.md §18)."""
    if granularity == "daily":
        begin = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end = begin + timedelta(days=1) - timedelta(microseconds=1)
    elif granularity == "weekly":
        begin = (dt - timedelta(days=dt.isoweekday() - 1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end = begin + timedelta(days=7) - timedelta(microseconds=1)
    elif granularity == "monthly":
        begin = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = (
            begin.replace(year=begin.year + 1, month=1)
            if begin.month == 12
            else begin.replace(month=begin.month + 1)
        )
        end = next_month - timedelta(microseconds=1)
    else:
        raise ValueError(f"Unsupported granularity: {granularity}")
    return begin, end


def build_conversation_aggregations(records: List[Dict[str, Any]], rich: bool) -> Dict[str, Any]:
    """
    Buckets separated by chat_id (mixing message counts across
    conversations would blur what's being counted, same spirit as bank
    keeping currency/domain separate — timelive.md §21). `rich` controls
    whether by_sender breakdowns (with message_refs) are included — FULL
    only, mirroring every other domain's by_* treatment.
    """
    aggregations: Dict[str, Any] = {}

    for granularity in AGGREGATION_GRANULARITIES:
        buckets: Dict[Tuple[datetime, str], Dict[str, Any]] = {}

        for record in records:
            if not record.get("begin_timestamp"):
                continue
            dt = datetime.fromisoformat(record["begin_timestamp"])
            bucket_begin, bucket_end = compute_bucket_bounds(dt, granularity)

            bucket_key = (bucket_begin, record["chat_id"])
            bucket = buckets.setdefault(bucket_key, {
                "timestamp_begin": bucket_begin,
                "timestamp_end": bucket_end,
                "chat_id": record["chat_id"],
                "message_count": 0,
                "call_count": 0,
                "call_seconds_total": 0,
                "location_count": 0,
                "_by_type": defaultdict(int),
                "_by_sender_count": defaultdict(int),
                "_by_sender_refs": defaultdict(list),
            })

            bucket["message_count"] += 1
            bucket["_by_type"][record.get("message_type", "unknown")] += 1
            if record.get("message_type") == "call" and record.get("duration_seconds"):
                bucket["call_count"] += 1
                bucket["call_seconds_total"] += record["duration_seconds"]
            if record.get("message_type") == "location":
                bucket["location_count"] += 1
            if record.get("sender") and record.get("message_type") != "system_event":
                bucket["_by_sender_count"][record["sender"]] += 1
                bucket["_by_sender_refs"][record["sender"]].append(record["event_number"])

        finalized = []
        for bucket in sorted(buckets.values(), key=lambda b: (b["timestamp_begin"], b["chat_id"])):
            entry = {
                "timestamp_begin": to_naive_iso(bucket["timestamp_begin"]),
                "timestamp_end": to_naive_iso(bucket["timestamp_end"]),
                "chat_id": bucket["chat_id"],
                "message_count": bucket["message_count"],
                "call_count": bucket["call_count"],
                "call_seconds_total": bucket["call_seconds_total"],
                "location_count": bucket["location_count"],
                "by_message_type": dict(bucket["_by_type"]),
            }
            if rich:
                entry["by_sender"] = [
                    {
                        "sender": sender,
                        "message_count": count,
                        "message_refs": bucket["_by_sender_refs"][sender],
                    }
                    for sender, count in sorted(
                        bucket["_by_sender_count"].items(), key=lambda kv: kv[1], reverse=True
                    )[:AGGREGATION_TOP_N_SENDERS]
                ]
            finalized.append(entry)

        aggregations[granularity] = finalized

    return aggregations


# ============================================================================
# NOTABILITY SCORE — domain signals feeding the shared engine (main.py)
# ============================================================================

def _type_richness_signal(record: Dict[str, Any]) -> float:
    return MESSAGE_TYPE_RICHNESS.get(record.get("message_type"), 0.3)


def _long_call_signal(record: Dict[str, Any]) -> float:
    if record.get("message_type") == "call" and (record.get("duration_seconds") or 0) >= LONG_CALL_SECONDS:
        return 1.0
    return 0.0


def compute_message_notability_scores(records: List[Dict[str, Any]]) -> None:
    shared_compute_notability_scores(
        records,
        weight_functions={
            "type_richness": _type_richness_signal,
            "recency": lambda r: recency_weight(
                r.get("begin_timestamp"), half_life_days=NOTABILITY_RECENCY_HALF_LIFE_DAYS
            ),
            "long_call_bonus": _long_call_signal,
        },
        weights={
            "type_richness": NOTABILITY_WEIGHT_TYPE_RICHNESS,
            "recency": NOTABILITY_WEIGHT_RECENCY,
            "long_call_bonus": NOTABILITY_WEIGHT_LONG_CALL_BONUS,
        },
    )

    now = datetime.now()
    for record in records:
        begin_timestamp = record.get("begin_timestamp")
        if not begin_timestamp:
            continue
        dt = datetime.fromisoformat(begin_timestamp)
        age_days = (now - dt).days
        if 0 <= age_days <= PRIMARY_MIN_RECENT_DAYS_GUARANTEED:
            record["notability_score"] = round(
                record.get("notability_score", 0.0) + PRIMARY_RECENT_GUARANTEE_BOOST, 4
            )


# ============================================================================
# FULL — analytical dataset construction
# ============================================================================

def apply_full_pruning(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    PRUNE_LEVEL here only ever controls bookkeeping/debugging fields
    (raw_line, source_file, record_index_in_source) — it NEVER touches
    message text itself, which is governed entirely by
    PRIMARY_INCLUDE_MESSAGE_TEXT (a privacy decision, not a size
    tradeoff — see module docstring). FULL always has full text.
    """
    out = dict(record)

    if PRUNE_LEVEL in ("none", "light"):
        pass  # keep raw_line + bookkeeping fields as-is
    elif PRUNE_LEVEL == "medium":
        out.pop("raw_line", None)
    else:  # aggressive
        out.pop("raw_line", None)
        if out.get("notability_score", 0) <= 0.6:
            out.pop("source_file", None)
            out.pop("record_index_in_source", None)

    return out


def build_full_payload(
    records: List[Dict[str, Any]],
    chats: List[Dict[str, Any]],
    bursts: List[Dict[str, Any]],
    aggregations: Dict[str, Any],
    files_processed: int,
    duplicates_removed: int,
    errors: List[Dict[str, Any]],
    warnings: List[Dict[str, Any]],
) -> Dict[str, Any]:
    pruned_records = [apply_full_pruning(r) for r in records]
    timestamps = [r["begin_timestamp"] for r in records if r.get("begin_timestamp")]

    metadata = build_metadata(
        dataset_name="whatsapp_dataset_full",
        source="whatsapp_chat_export",
        version=DATASET_VERSION,
        purpose=(
            "Normalized, analytical representation of every WhatsApp "
            "conversation exported into Input/WhatsApp. Used when PRIMARY "
            "(whatsapp_dataset.json) does not contain enough detail to "
            "answer the question — in particular, this is the ONLY place "
            "message text lives (see _logic.interpretation_notes: "
            "message_text_policy)."
        ),
        extra={
            "prune_level": PRUNE_LEVEL,
            "records_total": len(pruned_records),
            "duplicates_removed": duplicates_removed,
            "chats_detected": len(chats),
            "conversation_bursts_detected": len(bursts),
            "min_date": min(timestamps) if timestamps else None,
            "max_date": max(timestamps) if timestamps else None,
            "chat_files_processed": files_processed,
            "errors": errors,
            "warnings": warnings,
        },
    )

    schema = build_schema(
        sections={
            "chats": (
                "One entry per detected conversation: chat_id, "
                "display_name (from the export folder name), is_group, "
                "participants (real senders only — see _logic), "
                "self_display_name (see message_text_policy note), "
                "message_count, timestamp_begin/timestamp_end."
            ),
            "messages": (
                "Every normalized message across every chat. Always has "
                "chat_id, event_number (full_ref target), "
                "begin_timestamp/end_timestamp, sender, message_type "
                "(text/image/video/video_note/audio/sticker/gif/document/"
                "contact_card/location/call/deleted/system_event/empty), "
                "was_edited, is_self (null if undetected). Type-specific "
                "fields (text, call_type/call_outcome/duration_seconds, "
                "document_filename/document_pages, latitude/longitude, "
                "system_event_type, deleted_by_export_owner) are present "
                "only when relevant to that message_type."
            ),
            "conversation_bursts": (
                "Runs of >= BURST_MIN_MESSAGES messages in the same chat "
                "within BURST_MAX_GAP_SECONDS of each other. "
                "message_refs points to 'messages'. Carries "
                "confidence_rate."
            ),
            "conversation_aggregations": (
                "Dict per granularity ('daily'/'weekly'/'monthly'), a "
                "list of buckets separated by chat_id (never mixed — "
                "timelive.md §21 spirit). by_sender includes, per sender, "
                "message_count and message_refs."
            ),
        },
        conventions=[
            "Timestamps are NAIVE local time, exactly as WhatsApp exported "
            "them — no timezone is attached or assumed (see "
            "message_text_policy / naive_timestamps in _logic).",
            "confidence_rate follows the fixed scale documented in "
            "timelive.md §27 (1.0 native / 0.8 high / 0.5 medium / 0.2 low "
            "/ absent = not applicable).",
        ],
    )

    logic = build_logic(
        normalization=(
            "Each chat export lives in its own Input/WhatsApp/<folder> "
            "directory (folder name -> chat_id/display_name); the file "
            "itself is always named _chat.txt regardless of which chat it "
            "is, so it is never used as an identifier (see "
            "collect_chat_sources). Lines are parsed with a deliberately "
            "strict header regex (2-digit day/month, 4-digit year, exact "
            "HH:MM:SS) so a message whose own text happens to contain a "
            "pasted, looser-format chat excerpt is never mistaken for a "
            "real message boundary — a real case found in the sample data "
            "(timelive.md §23/§46: real data surfaces edge cases synthetic "
            "fixtures would not)."
        ),
        deduplication=(
            "No native per-message id exists in the export, so "
            "deduplication always uses a composite key of (chat_id, "
            "begin_timestamp, sender, message_type, first 120 chars of "
            "text). Delegated to the shared mechanism in main.py."
        ),
        classification=(
            "message_type is assigned via a fixed priority of anchored, "
            "whole-body regex patterns (deletion > edit-flag stripped > "
            "call > location > document > other media > system event > "
            "plain text fallback), documented in classify_message. An "
            "unrecognized system-like line safely falls back to "
            "message_type='text' with its raw text preserved in FULL — "
            "nothing is silently dropped (timelive.md §22). This is a "
            "deterministic structural classification (native phrasing "
            "WhatsApp itself writes), not an uncertain inference, so "
            "message_type itself carries no confidence_rate."
        ),
        pruning=(
            "PRUNE_LEVEL here only controls debugging/bookkeeping fields "
            "(raw_line, source_file, record_index_in_source) — it never "
            "affects message text, which is governed entirely by the "
            "message_text_policy decision below."
        ),
        grouping=(
            f"A conversation_burst groups >= {BURST_MIN_MESSAGES} messages "
            f"in the same chat within {BURST_MAX_GAP_SECONDS}s of each "
            "other (timelive.md §29). Computed once per chat_id via "
            "main.group_by_time_and_compatibility with a trivially-true "
            "compatibility check, since — unlike bank/health/maps — there "
            "is no second semantic axis to combine time proximity with "
            "inside a single conversation. Carries "
            "confidence_rate=0.8: deterministic given the threshold, but "
            "still an assumption about what constitutes one real-world "
            "exchange."
        ),
        pattern_detection=None,
        interpretation_notes=[
            "message_text_policy: PRIMARY (whatsapp_dataset.json) NEVER "
            "contains free-text message content, by deliberate decision "
            "(timelive.md §10's own note that messaging content needs "
            "resolving before starting) — message text exists ONLY in "
            "this FULL file. Structured GPS coordinates from location "
            "shares are the one exception and ARE exposed in PRIMARY "
            "(notable_locations), since they are structured data, not "
            "conversational content, and a direct join key with "
            "maps_ingest.",
            "naive_timestamps: begin_timestamp/end_timestamp are naive "
            "local time exactly as exported, with no timezone conversion "
            "or attached offset (mirrors money_ingest's own documented "
            "naive-timestamp decision) — the correct zone can genuinely "
            "change message to message as the phone travels, so no "
            "single assumed zone was applied.",
            "self_identification: is_self / chats[].self_display_name are "
            "derived NATIVELY from WhatsApp's own 'You ...' phrasing "
            "(deletions of one's own message, self-referential system "
            "events) wherever that phrasing appears in a chat — not a "
            "user-supplied guess. Only falls back to the "
            "SELF_DISPLAY_NAMES config override for a chat where no such "
            "native marker ever occurs. Both is_self and "
            "self_display_name are left null rather than guessed when "
            "genuinely unknown (timelive.md §26: unknown is preferable to "
            "fabricated certainty).",
            "participants_vs_system_pseudo_sender: chats[].participants "
            "excludes any sender name that appears ONLY on system_event "
            "messages, because a chat's own name is sometimes used as the "
            "'sender' of boilerplate system lines (observed on the real "
            "group export's opening encryption notice) rather than a real "
            "participant.",
            "how_to_retrieve_detail_from_full: every 'full_ref' in "
            "PRIMARY corresponds to 'messages[i].event_number' in this "
            "FULL file.",
        ],
    )

    return {
        "_metadata": metadata,
        "_schema": schema,
        "_logic": logic,
        "chats": chats,
        "messages": pruned_records,
        "conversation_bursts": bursts,
        "conversation_aggregations": aggregations,
    }


# ============================================================================
# PRIMARY — LLM-oriented, privacy-light, budget-aware view
# ============================================================================

_TEXT_FREE_FIELDS = (
    "event_number", "chat_id", "begin_timestamp", "end_timestamp", "sender",
    "message_type", "was_edited", "is_self", "deleted_by_export_owner",
    "call_type", "call_outcome", "duration_seconds",
    "document_filename", "document_pages", "system_event_type",
)


def build_primary_message_view(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compact, PRIVACY-LIGHT view: deliberately never includes 'text', on
    any message_type, regardless of PRUNE_LEVEL or notability (see the
    module docstring's PRIVACY DECISION — this is the enforcement point).
    full_ref points to FULL for the actual text.
    """
    view: Dict[str, Any] = {"full_ref": f"messages/{record['event_number']}"}
    for field in _TEXT_FREE_FIELDS:
        if record.get(field) is not None:
            view[field] = record[field]
    return view


def build_primary_location_view(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Locations get their own view (still no 'text', but WITH lat/lon) per
    the explicit decision to expose structured coordinates in PRIMARY —
    see PRIMARY_INCLUDE_LOCATIONS / the module docstring.
    """
    view = build_primary_message_view(record)
    view["latitude"] = record.get("latitude")
    view["longitude"] = record.get("longitude")
    return view


def build_primary_dataset(
    records: List[Dict[str, Any]],
    chats: List[Dict[str, Any]],
    bursts: List[Dict[str, Any]],
    aggregations: Dict[str, Any],
) -> Dict[str, Any]:
    metadata = build_metadata(
        dataset_name="whatsapp_dataset",
        source="whatsapp_chat_export",
        version=DATASET_VERSION,
        purpose=(
            "Compact, privacy-light, LLM-oriented view of WhatsApp "
            "conversations. NEVER contains free-text message content "
            "(deliberate decision, see whatsapp_dataset_full.json's "
            "_logic.interpretation_notes.message_text_policy) — retrieve "
            "actual message text from whatsapp_dataset_full.json via the "
            "full_ref field when genuinely needed."
        ),
        extra={
            "prune_level": PRUNE_LEVEL,
            "primary_max_size_mb_target": PRIMARY_MAX_SIZE_MB,
            "primary_include_message_text": PRIMARY_INCLUDE_MESSAGE_TEXT,
            "primary_include_locations": PRIMARY_INCLUDE_LOCATIONS,
            "records_total_available": len(records),
        },
    )

    schema = build_schema(
        sections={
            "chats": "Same structure as FULL's chats section, always included in full here.",
            "conversation_aggregations": (
                "Same structure as FULL (buckets with timestamp_begin/"
                "timestamp_end, message_count, call/location counts, "
                "by_message_type), always included in full here. Does "
                "NOT include by_sender: PRIMARY prioritizes direct "
                "individual notable_messages instead."
            ),
            "conversation_bursts": "Detected conversation bursts, always included in full here (never contain message text).",
            "notable_locations": (
                "Budget-aware subset of location shares, WITH lat/lon "
                "(the one message-content exception, see PRIMARY's "
                "purpose note) — a direct join key with maps_ingest."
            ),
            "notable_messages": (
                "Budget-aware subset of the most relevant individual "
                "messages, METADATA ONLY (sender, timestamp, "
                "message_type, structural fields like call duration or "
                "document filename) — never message text. full_ref "
                "points to whatsapp_dataset_full.json for the actual "
                "content."
            ),
        },
    )

    logic = build_logic(
        normalization="See whatsapp_dataset_full.json's _logic for full detail; PRIMARY reuses the same normalized messages.",
        deduplication="Deduplication happens once, upstream of both PRIMARY and FULL — see whatsapp_dataset_full.json's _logic.",
        classification="See whatsapp_dataset_full.json's _logic for the message_type classification priority.",
        pruning=(
            f"notable_locations then notable_messages are each filled in "
            f"decreasing notability_score order until the CUMULATIVE size "
            f"(carried over from chats/aggregations/bursts, then across "
            f"the two sections themselves) stays under "
            f"{PRIMARY_MAX_SIZE_MB}MB (main.select_within_size_budget), "
            f"with {PRIMARY_SOFT_OVERFLOW_RATIO*100:.0f}% soft overflow "
            "tolerance. Messages from the last "
            f"{PRIMARY_MIN_RECENT_DAYS_GUARANTEED} days get a large "
            "notability_score boost beforehand, so recent activity is "
            "always well represented."
        ),
        grouping="See whatsapp_dataset_full.json's _logic for the conversation-burst criteria.",
        interpretation_notes=[
            "why_no_text_here: see this dataset's own 'purpose' field and "
            "whatsapp_dataset_full.json's message_text_policy note — this "
            "is a deliberate privacy decision (timelive.md §10), not an "
            "oversight or a size-budget side effect.",
            "why_chats_aggregations_bursts_come_first: the most common "
            "questions (how many chats exist, how active was a "
            "conversation this month, when was the last long exchange) "
            "are answerable from chats/conversation_aggregations/"
            "conversation_bursts alone, without individual messages — for "
            "this reason they get full priority in the budget regardless "
            "of their size (which stays small anyway).",
            "how_to_retrieve_detail: use full_ref to retrieve the full "
            "message (including its text, if type='text') from "
            "whatsapp_dataset_full.json.",
        ],
    )

    base_payload: Dict[str, Any] = {
        "_metadata": metadata,
        "_schema": schema,
        "_logic": logic,
        "chats": chats,
        "conversation_aggregations": aggregations,
        "conversation_bursts": bursts,
    }

    always_include_bytes = estimate_json_size_bytes(base_payload)
    target_bytes = int(PRIMARY_MAX_SIZE_MB * 1024 * 1024) if PRIMARY_MAX_SIZE_MB else None
    cumulative_size = always_include_bytes

    def fill_section(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        nonlocal cumulative_size
        chosen = select_within_size_budget(
            candidates,
            target_bytes=target_bytes,
            soft_overflow_ratio=PRIMARY_SOFT_OVERFLOW_RATIO,
            rank_field="notability_score",
            always_include_bytes=cumulative_size,
        )
        for item in chosen:
            item.pop("notability_score", None)
        cumulative_size += sum(estimate_json_size_bytes(i) for i in chosen)
        return chosen

    location_candidates = []
    if PRIMARY_INCLUDE_LOCATIONS:
        for r in records:
            if r.get("message_type") == "location":
                view = build_primary_location_view(r)
                view["notability_score"] = r.get("notability_score", 0.0)
                location_candidates.append(view)
    notable_locations = fill_section(location_candidates)

    message_candidates = []
    for r in records:
        if r.get("message_type") == "location":
            continue  # already represented in notable_locations
        view = build_primary_message_view(r)
        view["notability_score"] = r.get("notability_score", 0.0)
        message_candidates.append(view)
    notable_messages = fill_section(message_candidates)

    base_payload["notable_locations"] = notable_locations
    base_payload["notable_messages"] = notable_messages
    base_payload["_metadata"]["notable_locations_included"] = len(notable_locations)
    base_payload["_metadata"]["notable_messages_included"] = len(notable_messages)
    base_payload["_metadata"]["estimated_size_bytes"] = cumulative_size

    return base_payload


# ============================================================================
# RECORD BUILDING — raw parsed message -> normalized record
# ============================================================================

def build_message_record(raw_message: Dict[str, Any], chat_id: str) -> Optional[Dict[str, Any]]:
    dt = parse_header_timestamp(raw_message["date_str"], raw_message["time_str"])
    if dt is None:
        return None

    classified = classify_message(raw_message["sender"], raw_message["body"])
    begin_iso = to_naive_iso(dt)

    end_dt = dt
    if classified.get("message_type") == "call" and classified.get("duration_seconds"):
        end_dt = dt + timedelta(seconds=classified["duration_seconds"])
    end_iso = to_naive_iso(end_dt)

    record: Dict[str, Any] = {
        "chat_id": chat_id,
        "begin_timestamp": begin_iso,
        "end_timestamp": end_iso,
        "sender": raw_message["sender"],
        "source_file": raw_message["source_file"],
        "record_index_in_source": raw_message["record_index_in_source"],
        "event_number": "",  # assigned after global chronological sort
    }
    record.update(classified)
    return record


# ============================================================================
# MAIN ENTRYPOINT
# ============================================================================

def ingest_whatsapp_history(
    enabled: bool = True,
    prune_level_override: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main entry point. Flow:
      1. validate config (PRUNE_LEVEL)
      2. discover every chat (folder-per-chat, or loose-file fallback) in
         WHATSAPP_INPUT_DIR
      3. parse + classify every message in every chat file
      4. deduplicate globally, sort chronologically per chat, assign
         event_number
      5. detect each chat's self_display_name + is_self, build the chats
         index, detect conversation bursts, compute aggregations and
         notability scores
      6. build FULL and PRIMARY
      7. write ONLY whatsapp_dataset.json and whatsapp_dataset_full.json

    `enabled` / `prune_level_override` are explicit-parameter overrides
    for the orchestrator (timelive.md §38) — main.run_all_ingests() sets
    these instead of ever mutating this module's globals from outside.
    """
    if not enabled:
        return {"success": True, "status": "skipped", "reason": "disabled via enabled=False"}

    global PRUNE_LEVEL
    if prune_level_override is not None:
        PRUNE_LEVEL = prune_level_override
    if PRUNE_LEVEL not in VALID_PRUNE_LEVELS:
        raise ValueError(f"Invalid PRUNE_LEVEL: {PRUNE_LEVEL}. Allowed: {VALID_PRUNE_LEVELS}")

    chat_sources, discovery_warnings = collect_chat_sources(WHATSAPP_INPUT_DIR)
    warnings: List[Dict[str, Any]] = [
        {"warning_type": "loose_file_fallback_used", "message": w} for w in discovery_warnings
    ]
    errors: List[Dict[str, Any]] = []

    if not WHATSAPP_INPUT_DIR.exists():
        return {
            "success": False,
            "status": "missing_input_directory",
            "input_directory": str(WHATSAPP_INPUT_DIR),
            "chats_found": 0,
            "records_processed": 0,
            "outputs": {
                "primary": str(WHATSAPP_OUTPUT_DATASET_PATH),
                "full": str(WHATSAPP_OUTPUT_FULL_DATASET_PATH),
            },
        }

    all_records: List[Dict[str, Any]] = []
    files_processed = 0

    for chat_id, display_name, txt_files in chat_sources:
        chat_raw_messages: List[Dict[str, Any]] = []
        for txt_file in txt_files:
            try:
                raw_text = read_text_with_fallback_encoding(txt_file)
                chat_raw_messages.extend(split_into_raw_messages(raw_text, txt_file))
                files_processed += 1
            except Exception as exc:
                errors.append({
                    "chat_id": chat_id,
                    "file": txt_file.name,
                    "error_type": "file_load_error",
                    "message": str(exc),
                })

        for raw_message in chat_raw_messages:
            try:
                record = build_message_record(raw_message, chat_id)
                if record is None:
                    errors.append({
                        "chat_id": chat_id,
                        "file": raw_message.get("source_file"),
                        "error_type": "unparseable_timestamp",
                        "message": f"{raw_message.get('date_str')} {raw_message.get('time_str')}",
                    })
                    continue
                all_records.append(record)
            except Exception as exc:
                errors.append({
                    "chat_id": chat_id,
                    "file": raw_message.get("source_file"),
                    "error_type": "record_process_error",
                    "message": str(exc),
                })

    # --- Deduplication (global — composite key already includes chat_id) ---
    all_records, duplicates_removed = deduplicate_messages(all_records)

    # --- Chronological sort per chat, THEN assign event_number globally ---
    # (grouped-by-chat rather than a single global timeline — see
    # build_full_payload's normalization note: naive timestamps from
    # different real-world timezones are not safely interleaved across
    # different chats, so this avoids implying a false cross-chat
    # chronology).
    all_records.sort(
        key=lambda r: (
            r.get("chat_id", ""),
            r.get("begin_timestamp") or "",
            r.get("source_file", ""),
            r.get("record_index_in_source", 0),
        )
    )
    for counter, record in enumerate(all_records, start=1):
        record["event_number"] = f"{SOURCE_PREFIX}_{counter}"

    # --- Per-chat: self-detection, is_self, chat index, bursts ---
    records_by_chat: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in all_records:
        records_by_chat[record["chat_id"]].append(record)

    chats: List[Dict[str, Any]] = []
    all_bursts: List[Dict[str, Any]] = []
    burst_counter = 0
    display_names = {chat_id: display_name for chat_id, display_name, _ in chat_sources}

    for chat_id, chat_messages in records_by_chat.items():
        chat_entry = build_chat_index_entry(chat_id, display_names.get(chat_id, chat_id), chat_messages)
        apply_is_self(chat_messages, chat_entry["self_display_name"])
        chats.append(chat_entry)

        chat_bursts, burst_counter = detect_conversation_bursts(chat_id, chat_messages, burst_counter)
        all_bursts.extend(chat_bursts)

    chats.sort(key=lambda c: c["chat_id"])

    # --- Notability (needs is_self/classification already applied) ---
    compute_message_notability_scores(all_records)

    # --- Aggregations ---
    full_aggregations = build_conversation_aggregations(all_records, rich=True)
    primary_aggregations = build_conversation_aggregations(all_records, rich=False)

    # --- FULL ---
    full_payload = build_full_payload(
        records=all_records,
        chats=chats,
        bursts=all_bursts,
        aggregations=full_aggregations,
        files_processed=files_processed,
        duplicates_removed=duplicates_removed,
        errors=errors,
        warnings=warnings,
    )

    full_size_bytes = estimate_json_size_bytes(full_payload)
    full_size_warning = check_full_size_warning(full_size_bytes, warning_gb=FULL_WARNING_SIZE_GB)
    if full_size_warning:
        warnings.append({"warning_type": "full_dataset_large", "message": full_size_warning})
        full_payload["_metadata"]["warnings"] = warnings

    # --- PRIMARY ---
    primary_payload = build_primary_dataset(
        records=all_records,
        chats=chats,
        bursts=all_bursts,
        aggregations=primary_aggregations,
    )

    # --- Write: ONLY these two files (timelive.md §11) ---
    primary_size = write_json(WHATSAPP_OUTPUT_DATASET_PATH, primary_payload)
    full_size = write_json(WHATSAPP_OUTPUT_FULL_DATASET_PATH, full_payload)

    return {
        "success": True,
        "input_directory": str(WHATSAPP_INPUT_DIR),
        "chats_found": len(chat_sources),
        "chat_files_processed": files_processed,
        "records_processed": len(all_records),
        "duplicates_removed": duplicates_removed,
        "conversation_bursts_detected": len(all_bursts),
        "primary_size_bytes": primary_size,
        "full_size_bytes": full_size,
        "errors": errors,
        "warnings": warnings,
        "outputs": {
            "primary": str(WHATSAPP_OUTPUT_DATASET_PATH),
            "full": str(WHATSAPP_OUTPUT_FULL_DATASET_PATH),
        },
    }


if __name__ == "__main__":
    result = ingest_whatsapp_history()
    if result.get("chats_found", 0) == 0:
        print(f"No chat exports found in {WHATSAPP_INPUT_DIR}. Copy Input/WhatsApp/<chat folder>/_chat.txt there and retry.")
    else:
        print("Ingest completed." if result.get("success") else "Ingest failed.")
        print("Chats found:", result["chats_found"])
        print("Chat files processed:", result["chat_files_processed"])
        print("Messages processed:", result["records_processed"])
        print("Duplicates removed:", result["duplicates_removed"])
        print("Conversation bursts detected:", result["conversation_bursts_detected"])
        print("PRIMARY:", result["outputs"]["primary"])
        print("FULL:", result["outputs"]["full"])
        if result["errors"]:
            print("Errors:", len(result["errors"]))
        if result["warnings"]:
            print("Warnings:", len(result["warnings"]))