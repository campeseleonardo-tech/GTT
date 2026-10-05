# config.py
# =============================================================================
# PERSONAL DATA VAULT — CENTRAL CONFIGURATION
# =============================================================================
#
# STANDARD COMPLIANCE (see timelive.md §33)
# -----------------------------------------------------------------------
# This is the hybrid config described in timelive.md §33:
#
#   * config.json (next to this file) holds PURE DATA: relative
#     input/output paths and output filenames per domain. It has no
#     comments-as-code-documentation needs, so it is easy to hand-edit or
#     eventually generate from a settings UI.
#
#   * config.py (this file) LOADS config.json, resolves it into absolute,
#     environment-portable Path objects (works unmodified on the Windows
#     machine and on the Raspberry Pi copy of the repository, since every
#     path is computed relative to this file's location, never hardcoded),
#     and is where documentation/comments and any structure too rich for
#     plain JSON continue to live (e.g. SPOTIFY_RAW_FIELD_REFERENCE below).
#
# WHAT THIS FILE PROVIDES
# -----------------------------------------------------------------------
#   * BASE_DIR / INPUT_DIR / OUTPUT_DIR       — used by main.py
#   * SPOTIFY_INPUT_DIR / SPOTIFY_OUTPUT_*    — used by spotify_ingest.py
#   * HEALTH_INPUT_DIR / HEALTH_INPUT_FILE /
#     HEALTH_OUTPUT_*                         — used by health_ingest.py
#   * BANK_INPUT_DIR / BANK_OUTPUT_*          — used by the old money_ingest.py (pre-migration; kept for the domains not yet migrated off PRIMARY/FULL)
#   * MONEY_INPUT_DIR                         — used by money_ingest.py (SQLite/ingest_engine.py version, 2026-09-14 migration — no OUTPUT_* here, this domain no longer produces JSON files, see below)
#   * INSTAGRAM_INPUT_DIR                     — used by instagram_ingest.py (SQLite/ingest_engine.py version, 2026-09-15 migration — same "no OUTPUT_*" shape as money, see below)
#   * MAPS_INPUT_DIR / MAPS_OUTPUT_*          — used by maps_ingest.py (v4.1)
#   * WHATSAPP_INPUT_DIR / WHATSAPP_OUTPUT_*  — used by whatsapp_ingest.py (v4.4)
#   * CHESSDOTCOM_INPUT_DIR / CHESSDOTCOM_OUTPUT_* — used by
#     chessdotcom_ingest.py (v4.6)
#
# Every one of the ingests, and main.py itself, already falls back
# to sensible hardcoded relative defaults via `try: from config import
# ... except Exception: ...` if this file is missing or a name isn't
# found here — so this file is a convenience/override layer, not a hard
# dependency. When both exist, values from config.json (via this file)
# take priority because the `from config import ...` succeeds first.
#
# WHAT CAN BE MODIFIED
# -----------------------------------------------------------------------
#   * Everything in config.json: paths, output filenames.
#   * SPOTIFY_RAW_FIELD_REFERENCE / AI_USAGE_GUIDELINES below (documentation
#     content only — does not affect ingest behavior).
#
# WHAT MUST STAY STABLE
# -----------------------------------------------------------------------
#   * The exported name of every constant listed under "WHAT THIS FILE
#     PROVIDES" above — each ingest imports these by exact name.
#   * Importability as a plain Python module with no required arguments.
#
# NOT YET DONE (see timelive.md §33/§39 roadmap)
# -----------------------------------------------------------------------
# Domain-specific processing thresholds (prune_level, primary_max_size_mb,
# notability_weights, activity_inference_level, recurring/grouping
# tolerances, ...) still live inside each ingest script's own CONFIG
# section, not here. Migrating those into config.json is a separate,
# larger change (it requires editing every ingest again to read from
# here instead of their local constants) and was intentionally left out of
# this pass, which only had to produce config.py itself.
#
# KNOWN ISSUE — RESOLVED (2026-09-15, instagram migration): the real
# config.json on disk used to not be valid JSON (found 2026-09-14 while
# migrating money_ingest.py — it contained a stale copy of an early,
# Spotify-only config.py, not the {"base":..., "domains":...} structure
# this file's _load_config_data() expects). Every domain was silently
# falling back to _FALLBACK_CONFIG_DATA below as a result. The project
# owner deleted the stale file; config.json has now been rewritten from
# scratch as valid JSON mirroring _FALLBACK_CONFIG_DATA (including the
# new "instagram" entry), so _load_config_data() below now actually reads
# real, editable data instead of silently using the hardcoded fallback
# for every domain. The fallback dict itself is left in place, unchanged
# in spirit — it's still the safety net for a missing/corrupted
# config.json, just no longer the thing silently doing all the work.
# =============================================================================

import json
from pathlib import Path

# -----------------------------------------------------------------------------
# Project metadata
# -----------------------------------------------------------------------------
PROJECT_NAME = "Personal Data Vault & AI Assistant"
PROJECT_MVP_NAME = "Spotify + Apple Health + Banking + Maps Ingestion MVP"
CONFIG_VERSION = "2.5"  # bumped: added instagram domain (2026-09-15 SQLite migration) + config.json rewritten as valid JSON


# -----------------------------------------------------------------------------
# Project directory layout
# -----------------------------------------------------------------------------
# This file lives in "code/"; Input/ and Output/ are sibling directories of
# "code/". BASE_DIR is computed from this file's own location so the same
# repository works unmodified whether it sits under
# C:\Users\campe\Desktop\Timelive (Windows) or its Raspberry Pi copy
# (timelive.md §31: no hardcoded absolute paths).
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = BASE_DIR / "code"

_CONFIG_JSON_PATH = Path(__file__).resolve().with_name("config.json")

# -----------------------------------------------------------------------------
# Hardcoded fallback data
# -----------------------------------------------------------------------------
# Used only if config.json is missing, unreadable, or malformed. Mirrors
# exactly what config.json currently contains, so behavior is identical
# either way — this is a safety net, not a second source of truth to keep
# in sync by hand for normal changes (edit config.json for that).
#
# IMPORTANT (v4.6): this fallback dict is a safety net inside config.py
# itself. The user's actual config.json file (not tracked in this
# markdown-doc project) must ALSO gain a "chessdotcom" entry under
# "domains", shaped exactly like the "maps"/"whatsapp" entries below,
# or chessdotcom_ingest.py will only ever see the fallback path here
# rather than a user-editable one:
#
#   "chessdotcom": {
#     "input_dir": "Input/Chessdotcom",
#     "output_dataset_filename": "chessdotcom_dataset.json",
#     "output_full_dataset_filename": "chessdotcom_dataset_full.json"
#   }
#
# IMPORTANT (2026-09-14, money migration): same note applies to "money"
# below — except money's shape is deliberately smaller than the others
# (input_dir only, no output_dataset_filename/output_full_dataset_filename)
# because this domain no longer produces JSON output files at all (see
# money_ingest.py's module docstring — it writes 3 tables directly into
# the shared vault.db via ingest_engine.py).
#
# IMPORTANT (2026-09-15, instagram migration): same shape as "money"
# again (input_dir only) — instagram_ingest.py also writes straight into
# vault.db, no JSON output files. Unlike money, this input_dir is a
# PARENT folder: the project owner's export lands in a dated/versioned
# subfolder underneath it (e.g. "Input/instagram/instagram-leocampese-
# 2026-09-14-jzx0KPsP/"), because a re-export can arrive as a new
# subfolder without overwriting the previous one. instagram_ingest.py's
# own collect_input_files() walks every immediate subfolder of
# INSTAGRAM_INPUT_DIR, not just files directly inside it — see that
# module's docstring.
_FALLBACK_CONFIG_DATA = {
    "base": {"input_dir": "Input", "output_dir": "Output"},
    "domains": {
        "spotify": {
            "input_dir": "Input/Spotify",
            "output_dataset_filename": "spotify_dataset.json",
            "output_full_dataset_filename": "spotify_dataset_full.json",
        },
        "health": {
            "input_dir": "Input/Apple Health",
            "input_file": "Input/Apple Health/export.xml",
            "output_dataset_filename": "applehealth_dataset.json",
            "output_full_dataset_filename": "applehealth_dataset_full.json",
        },
        "bank": {
            "input_dir": "Input/Bank",
            "output_dataset_filename": "bank_dataset.json",
            "output_full_dataset_filename": "bank_dataset_full.json",
        },
        "money": {
            "input_dir": "Input/Money",
        },
        "instagram": {
            "input_dir": "Input/instagram",
        },
        "maps": {
            "input_dir": "Input/Maps",
            "output_dataset_filename": "maps_dataset.json",
            "output_full_dataset_filename": "maps_dataset_full.json",
        },
        "whatsapp": {
            "input_dir": "Input/WhatsApp",
            "output_dataset_filename": "whatsapp_dataset.json",
            "output_full_dataset_filename": "whatsapp_dataset_full.json",
        },
        "chessdotcom": {
            "input_dir": "Input/Chessdotcom",
            "output_dataset_filename": "chessdotcom_dataset.json",
            "output_full_dataset_filename": "chessdotcom_dataset_full.json",
        },
    },
}


def _load_config_data() -> dict:
    try:
        with _CONFIG_JSON_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Missing/unreadable/malformed config.json must not crash every
        # ingest that imports this module — fall back silently to the
        # data above, exactly like each ingest's own try/except fallback.
        return _FALLBACK_CONFIG_DATA


_data = _load_config_data()
_base = _data.get("base", _FALLBACK_CONFIG_DATA["base"])
_domains = _data.get("domains", _FALLBACK_CONFIG_DATA["domains"])
_spotify = _domains.get("spotify", _FALLBACK_CONFIG_DATA["domains"]["spotify"])
_health = _domains.get("health", _FALLBACK_CONFIG_DATA["domains"]["health"])
_bank = _domains.get("bank", _FALLBACK_CONFIG_DATA["domains"]["bank"])
_money = _domains.get("money", _FALLBACK_CONFIG_DATA["domains"]["money"])
_instagram = _domains.get("instagram", _FALLBACK_CONFIG_DATA["domains"]["instagram"])
_maps = _domains.get("maps", _FALLBACK_CONFIG_DATA["domains"]["maps"])
_whatsapp = _domains.get("whatsapp", _FALLBACK_CONFIG_DATA["domains"]["whatsapp"])
_chessdotcom = _domains.get("chessdotcom", _FALLBACK_CONFIG_DATA["domains"]["chessdotcom"])


# -----------------------------------------------------------------------------
# Base paths — used by main.py
# -----------------------------------------------------------------------------
INPUT_DIR = BASE_DIR / _base["input_dir"]
OUTPUT_DIR = BASE_DIR / _base["output_dir"]


# -----------------------------------------------------------------------------
# Spotify paths — used by spotify_ingest.py
# -----------------------------------------------------------------------------
SPOTIFY_INPUT_DIR = BASE_DIR / _spotify["input_dir"]
SPOTIFY_OUTPUT_DATASET_PATH = OUTPUT_DIR / _spotify["output_dataset_filename"]
SPOTIFY_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _spotify["output_full_dataset_filename"]


# -----------------------------------------------------------------------------
# Apple Health paths — used by health_ingest.py
# -----------------------------------------------------------------------------
HEALTH_INPUT_DIR = BASE_DIR / _health["input_dir"]
HEALTH_INPUT_FILE = BASE_DIR / _health["input_file"]
HEALTH_OUTPUT_DATASET_PATH = OUTPUT_DIR / _health["output_dataset_filename"]
HEALTH_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _health["output_full_dataset_filename"]


# -----------------------------------------------------------------------------
# Bank / investment paths — used by the OLD money_ingest.py (PRIMARY/FULL
# JSON system). Kept for reference/rollback only; the migrated
# money_ingest.py (below) does not import these.
# -----------------------------------------------------------------------------
BANK_INPUT_DIR = BASE_DIR / _bank["input_dir"]
BANK_OUTPUT_DATASET_PATH = OUTPUT_DIR / _bank["output_dataset_filename"]
BANK_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _bank["output_full_dataset_filename"]


# -----------------------------------------------------------------------------
# Money paths — used by money_ingest.py (2026-09-14, migrated to
# ingest_engine.py/vault.db — see that module's docstring). Only an input
# directory: this domain writes directly into the shared vault.db, it no
# longer has its own output dataset files, so there is no
# MONEY_OUTPUT_DATASET_PATH/MONEY_OUTPUT_FULL_DATASET_PATH to define.
# -----------------------------------------------------------------------------
MONEY_INPUT_DIR = BASE_DIR / _money["input_dir"]


# -----------------------------------------------------------------------------
# Instagram paths — used by instagram_ingest.py (2026-09-15, migrated to
# ingest_engine.py/vault.db from the start — there was never an old
# PRIMARY/FULL version of this domain). Only an input directory, same
# reasoning as MONEY_INPUT_DIR above. This is a PARENT directory: see the
# "instagram migration" note on _FALLBACK_CONFIG_DATA above — each export
# (there can be more than one over time) lives in its own subfolder
# underneath this path, and instagram_ingest.py walks all of them.
# -----------------------------------------------------------------------------
INSTAGRAM_INPUT_DIR = BASE_DIR / _instagram["input_dir"]


# -----------------------------------------------------------------------------
# Maps paths — MAPS_INPUT_DIR used by maps_ingest.py (2026-09-17, migrated to
# ingest_engine.py/vault.db — see that module's docstring). Only an input
# directory, same reasoning as MONEY_INPUT_DIR/INSTAGRAM_INPUT_DIR above: this
# domain writes directly into the shared vault.db, no more PRIMARY/FULL
# dataset files of its own.
#
# MAPS_OUTPUT_DATASET_PATH / MAPS_OUTPUT_FULL_DATASET_PATH below are the OLD
# v4.1 (PRIMARY/FULL JSON system) constants — kept for reference/rollback
# only, same as BANK_OUTPUT_* above. The migrated maps_ingest.py does not
# import them. The v4.1 output files themselves
# (output/maps_dataset*.json) are also left on disk, untouched.
# -----------------------------------------------------------------------------
MAPS_INPUT_DIR = BASE_DIR / _maps["input_dir"]
MAPS_OUTPUT_DATASET_PATH = OUTPUT_DIR / _maps["output_dataset_filename"]
MAPS_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _maps["output_full_dataset_filename"]


# -----------------------------------------------------------------------------
# WhatsApp paths — used by whatsapp_ingest.py (v4.4)
# -----------------------------------------------------------------------------
WHATSAPP_INPUT_DIR = BASE_DIR / _whatsapp["input_dir"]
WHATSAPP_OUTPUT_DATASET_PATH = OUTPUT_DIR / _whatsapp["output_dataset_filename"]
WHATSAPP_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _whatsapp["output_full_dataset_filename"]


# -----------------------------------------------------------------------------
# Chess.com paths — used by chessdotcom_ingest.py (v4.6)
# -----------------------------------------------------------------------------
CHESSDOTCOM_INPUT_DIR = BASE_DIR / _chessdotcom["input_dir"]
CHESSDOTCOM_OUTPUT_DATASET_PATH = OUTPUT_DIR / _chessdotcom["output_dataset_filename"]
CHESSDOTCOM_OUTPUT_FULL_DATASET_PATH = OUTPUT_DIR / _chessdotcom["output_full_dataset_filename"]


# =============================================================================
# SPOTIFY RAW FIELD REFERENCE (documentation only)
# =============================================================================
# This documents the RAW Spotify export field names themselves (legacy vs
# current generation), which is information about the INPUT format, not
# about the processed dataset. It is therefore complementary to, not
# duplicated by, spotify_ingest.py's own _schema/_logic blocks (timelive.md
# §31), which document the OUTPUT dataset instead. Kept here because it is
# a rich nested structure, a poor fit for plain config.json data, and
# because timelive.md §33 explicitly names this kind of content as staying
# in config.py under the hybrid model.
# =============================================================================

SPOTIFY_RAW_FIELD_REFERENCE = {
    "common_fields": {
        "endTime": {
            "meaning": "Legacy end-of-playback timestamp, often without an explicit timezone.",
            "logical_type": "string datetime",
            "notes": [
                "Present mostly in older export files.",
                "Format can vary between export vintages.",
            ],
        },
        "ts": {
            "meaning": "Playback timestamp in newer export formats — usually the most reliable temporal field.",
            "logical_type": "string datetime",
            "notes": [
                "Can appear instead of endTime.",
                "Usually ISO 8601 with timezone information.",
                "spotify_ingest.py tries ts before endTime when building end_timestamp.",
            ],
        },
        "artistName": {
            "meaning": "Artist name in legacy files.",
            "logical_type": "string",
            "notes": ["May be replaced by master_metadata_album_artist_name in newer files."],
        },
        "trackName": {
            "meaning": "Track title in legacy files.",
            "logical_type": "string",
            "notes": ["May be replaced by master_metadata_track_name in newer files."],
        },
        "msPlayed": {
            "meaning": "Milliseconds played, legacy field name.",
            "logical_type": "integer",
            "notes": ["Basis for played_seconds/played_minutes and the skip-likelihood heuristic."],
        },
        "ms_played": {
            "meaning": "Milliseconds played, current field name.",
            "logical_type": "integer",
            "notes": ["Canonical field in newer exports."],
        },
        "master_metadata_track_name": {
            "meaning": "Track title in newer exports.",
            "logical_type": "string",
        },
        "master_metadata_album_artist_name": {
            "meaning": "Artist name in newer exports.",
            "logical_type": "string",
        },
        "master_metadata_album_album_name": {
            "meaning": "Album name in newer exports.",
            "logical_type": "string",
            "notes": ["May be absent for podcasts or non-music content."],
        },
        "episode_name": {
            "meaning": "Podcast episode name, when the play is not music.",
            "logical_type": "string",
        },
        "episode_show_name": {
            "meaning": "Podcast/show name associated with the episode.",
            "logical_type": "string",
        },
        "platform": {
            "meaning": "Playback platform/device reported by Spotify in newer exports.",
            "logical_type": "string",
            "notes": ["Used as spotify_ingest.py's `device` field, falling back to media_type when absent."],
        },
        "offline": {
            "meaning": "Whether playback happened offline.",
            "logical_type": "boolean",
        },
        "incognito_mode": {
            "meaning": "Whether the session was in a supported private/incognito mode.",
            "logical_type": "boolean",
        },
    },
    "limitations": [
        "No Spotify API is used; nothing is enriched from external sources.",
        "media_type (audio/video) is inferred from the export filename, not file content.",
        "Timestamp formats vary across export vintages; parsing is best-effort (see spotify_ingest.parse_end_time).",
    ],
}


# =============================================================================
# MAPS RAW FIELD REFERENCE (documentation only, v4.1)
# =============================================================================
MAPS_RAW_FIELD_REFERENCE = {
    "record_shape": (
        "Each raw element has startTime/endTime plus exactly ONE of "
        "'visit', 'activity', 'timelinePath'."
    ),
    "visit_fields": {
        "topCandidate.semanticType": "Home/Work/Aliased Location/Searched Address/Unknown, or a custom label (e.g. a secondary 'Home AT') — kept 100% verbatim by maps_ingest.py.",
        "topCandidate.placeID": "Google place id — this vault's stable place identifier.",
        "topCandidate.placeLocation": "'geo:lat,lon' string.",
        "topCandidate.probability": "Google's native confidence in this place guess — kept as candidate_probability, never folded into confidence_rate.",
        "probability": "Segment-level native probability — kept as segment_probability.",
    },
    "activity_fields": {
        "topCandidate.type": "Transport mode (walking/cycling/in passenger vehicle/in train/in bus/in subway/flying/in tram, ...).",
        "distanceMeters": "Native unit: meters — never silently converted to km.",
        "start / end": "'geo:lat,lon' strings for the activity's start/end points.",
    },
    "timelinePath_fields": (
        "Raw GPS breadcrumb points — NOT ingested by maps_ingest.py (see "
        "the module docstring and timelive.md v4.1 changelog for why); "
        "its record count is preserved in FULL's _metadata for "
        "traceability only."
    ),
    "limitations": [
        "No reverse geocoding: semantic_type/place_id/coordinates are kept exactly as Google reports them (timelive.md §7).",
        "Only the current flat export shape is supported (bare list, or {'semanticSegments':[...],'rawSignals':[...]}); the old pre-2024 nested 'timelineObjects' format is out of scope.",
    ],
}


# =============================================================================
# CHESS.COM RAW FIELD REFERENCE (documentation only, v4.6)
# =============================================================================
# Documents chess.com's raw per-game PGN export field names (input format),
# kept separate from chessdotcom_dataset*.json's own _schema (which documents
# the processed OUTPUT), for the same reason SPOTIFY_RAW_FIELD_REFERENCE /
# MAPS_RAW_FIELD_REFERENCE above are kept separate from their own _schema.
#
# Derived by inspecting the project owner's real export (timelive.md §23):
# one file, 186 real games, May 2022 - Jan 2023, all with the exact same
# header shape below. No [Link], [ECO], [UTCDate]/[UTCTime], or %clk
# annotations were present anywhere in that file — see chessdotcom_ingest.py's
# module docstring for what this means for dedup/opening-classification/
# duration-estimation. This reference will need extending if the other two
# files (or future exports) show a header shape chess.com sometimes does
# include (Link/ECO/%clk are real, documented chess.com PGN fields — they
# simply didn't happen to appear in this particular export vintage).
# =============================================================================

CHESSDOTCOM_RAW_FIELD_REFERENCE = {
    "header_fields_observed": {
        "Event": "Always 'Live Chess' in the inspected file (chess.com PGN also uses other values for tournaments/daily games — not yet observed here).",
        "Site": "Always 'Chess.com'.",
        "Date": "Game date, 'YYYY.MM.DD', no time component.",
        "White": "White player's chess.com username (verbatim, native).",
        "Black": "Black player's chess.com username (verbatim, native).",
        "Result": "'1-0' / '0-1' / '1/2-1/2', standard PGN result token.",
        "WhiteElo": "chess.com's own internal rating for White at that time control — NOT an official FIDE/USCF Elo.",
        "BlackElo": "Same, for Black.",
        "TimeControl": "Either plain seconds ('600'), seconds+increment ('180+2'), or (not observed here, but a documented chess.com format) moves-per-period for daily/correspondence games ('1/172800').",
        "EndTime": "Local time-of-day plus an explicit GMT offset, e.g. '12:04:51 GMT+0000' — chess.com always reports this as UTC in the inspected file. Combined with Date, this is the only reliable per-game timestamp available.",
        "Termination": "Free-text sentence naming the winner (or 'Game drawn by ...') and the reason — parsed by chessdotcom_ingest.classify_win_method via keyword matching, not a fixed enum.",
    },
    "fields_not_observed_in_the_inspected_file": [
        "Link (the game's chess.com URL, which would have been a native per-game id for deduplication/full_ref traceability if present).",
        "ECO (opening classification code).",
        "%clk move comments (per-move remaining clock time).",
        "UTCDate / UTCTime (chess.com sometimes emits these as a redundant, explicitly-UTC-labeled pair alongside Date/EndTime).",
    ],
    "limitations": [
        "No opening classification (ECO) is available or computed — chessdotcom_ingest.py derives only a cheap opening_signature (first few SAN moves) for a by_opening aggregation breakdown, never a named opening (timelive.md §7: no external lookup service).",
        "No native per-game id: deduplication uses a composite key (timelive.md §25).",
        "No move-level clock data in the inspected file: per-game duration_seconds is therefore usually None (timestamp_begin = timestamp_end, an instantaneous-event convention per timelive.md §18) unless a future file does contain %clk, in which case chessdotcom_ingest.estimate_game_duration_seconds is used automatically.",
    ],
}


# -----------------------------------------------------------------------------
# How an AI agent should use these outputs
# -----------------------------------------------------------------------------
AI_USAGE_GUIDELINES = [
    "Each domain's _metadata/_schema/_logic (inside its own PRIMARY/FULL "
    "JSON output) is the authoritative description of that dataset — read "
    "those before this file's documentation, which only covers raw input "
    "field meanings and repository layout. Domains migrated to vault.db "
    "(chessdotcom, spotify, money, instagram) instead describe themselves "
    "through the bridge's describe_table(), not through _schema/_logic.",
    "Prefer PRIMARY over FULL whenever it answers the question; use "
    "full_ref to retrieve the matching FULL record only when PRIMARY is "
    "not enough (timelive.md §14). Not applicable to domains already "
    "migrated to vault.db — those have no PRIMARY/FULL split at all.",
    "confidence_rate follows one fixed scale across every domain "
    "(timelive.md §27): 1.0 native, 0.8 high-confidence inference, 0.5 "
    "medium, 0.2 low, absent/null = not an inference at all.",
    "Never assume a field exists just because it exists in one domain — "
    "domain-specific structure is expected (timelive.md §6); check each "
    "dataset's own _schema.",
]


# -----------------------------------------------------------------------------
# End of config.py
# -----------------------------------------------------------------------------
