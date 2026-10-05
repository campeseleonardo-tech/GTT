# instagram_ingest.py
# =============================================================================
# INSTAGRAM INGEST — Personal Data Vault (SQLite / ingest_engine.py,
# fourth domain migrated, 2026-09-15 — see timelive.md §8 and
# EVOLUTION_LOG.md)
# =============================================================================
#
# SCOPE (Tier 1 — agreed explicitly with the project owner before writing
# this file, see chat 2026-09-15): posts/stories/reels/archived posts,
# comments made, likes given (posts + comments), followers, following,
# direct messages, login/logout activity. Deliberately OUT for this pass
# (parked, not forgotten — see EVOLUTION_LOG.md): ads/tracking data,
# story_interactions (polls/quizzes/emoji reactions), shopping,
# monetization, saved posts/collections, search/link history,
# apps_and_websites, profile/account metadata, and — explicitly, by the
# project owner's own decision — connections/contacts/synced_contacts.json
# (a synced phone contact list of people who never consented to being in
# this project, a materially different sensitivity class than a DM with
# an Instagram contact).
#
# REAL-DATA FINDINGS (timelive.md §7: inspect before designing schema —
# this domain needed it more than any before it)
# -----------------------------------------------------------------------
# 1. MOJIBAKE BUG (Meta's export, not this code): every non-ASCII string
#    in the raw JSON is UTF-8 bytes mis-decoded as Latin-1 by Instagram's
#    own export tool, e.g. a real message "Se vi interessa 🫶🏼" is written
#    as "Se vi interessa ð«¶ð¼". Fixed once, centrally, in fix_mojibake()
#    below, applied to every text field this domain stores. Round-trips
#    safely on already-clean text (falls back to the original string if
#    the latin1-encode/utf8-decode round trip fails).
# 2. Post-like content ("posts", "stories", "reels", "archived_posts",
#    "other_content" under your_instagram_activity/media/) is NOT one
#    consistent shape. Four real shapes were found in this export alone:
#      A. group + explicit caption/timestamp: {"media":[...], "title":
#         <caption>, "creation_timestamp": <ts>}                  (posts_1.json)
#      B. rich generic event shape: {"timestamp": <ts>, "media": [],
#         "label_values": [{"label": "Caption", "value": ...},
#         {"label": "Latitude"/"Longitude", "value": ...},
#         {"label": "Media", "media": [...]}, ...many more...]}    (posts.json,
#                                                                    other_content.json)
#      C. flat, no grouping — the media fields sit directly on the list
#         item, no "media" wrapper at all                          (stories.json)
#      D. group with no caption/timestamp of its own — only "media": [...],
#         caption lives on each media item's own "title"           (archived_posts.json,
#                                                                    reels.json)
#    All four are normalized by _iter_post_media_rows() below into the
#    same row shape. Shape B also revealed that some posts carry exact
#    GPS coordinates (Latitude/Longitude labels) — kept as-is (native,
#    it's the project owner's own posted content), see instagram_posts.
# 3. liked_posts.json is NOT just "target + timestamp" as assumed before
#    inspecting it — it carries the full caption AND the post owner's
#    name+username (Shape B again). liked_comments.json is comparatively
#    thin (username + timestamp + the liked comment's own text/emoji).
#    Both are kept as native content (public content someone else chose
#    to publish, a materially lower sensitivity than a private DM) — see
#    instagram_likes.
# 4. security_and_login_information/.../login_activity.json carries a raw
#    IP Address per login. Same decision already made for Spotify's
#    ip_addr: excluded from vault.db (a cloud-LLM-queryable database is a
#    real exposure path a raw file on disk is not), everything else in
#    that record (cookie name, user agent, language, port) is kept — the
#    project owner's explicit "let's not be too strict about it" applies
#    to those, not to the IP address itself.
# 5. DIRECT MESSAGES: ~790 real threads (inbox + message_requests). Full
#    message text is kept ONLY for the TOP_N_THREADS_FOR_FULL_TEXT busiest
#    threads (by message count), truncated to MAX_CHARS_PER_MESSAGE each —
#    an explicit MVP sampling decision by the project owner, expandable
#    later by changing those two constants (nothing else). Every thread,
#    sampled or not, still gets a metadata-only row in
#    instagram_direct_message_threads (participants, message_count,
#    first/last timestamp) — only the message-level text is gated.
#
# NO SESSIONS FOR THIS DOMAIN (project owner's explicit call, 2026-09-15):
# unlike chess.com/spotify, "session" grouping was judged not worth the
# design time here and dropped rather than half-built — timelive.md §4
# already treats per-domain session definitions as optional, not
# mandatory.
#
# NO notability_score FOR THIS DOMAIN, ON PURPOSE: every notability
# formula elsewhere in this project (chess.com, spotify) leans on a
# native signal the export doesn't provide here (game result quality,
# skip/duration) — Instagram's own data export contains no like/comment
# COUNTS on the project owner's own posts, only the individual
# interactions of OTHERS' content the project owner touched. Inventing a
# formula with no real signal behind it would violate timelive.md §7
# ("dati reali prima dello schema") the same way a guessed schema would —
# left out rather than faked.
#
# ENGINE CHANGES MADE ALONGSIDE THIS FILE (see ingest_engine.py's own
# module docstring for the reasoning): ColumnSpec.sensitive,
# register_table_spec()'s duplicate-name guard, truncate_text().
# =============================================================================

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from ingest_engine import (
    ColumnSpec,
    TableSpec,
    IngestReport,
    UpsertOutcome,
    create_schema_for_table,
    upsert_rows,
    register_table_spec,
    truncate_text,
)

logger = logging.getLogger("instagram_ingest")


# ============================================================================
# CONFIGURATION
# ============================================================================

try:
    from config import INSTAGRAM_INPUT_DIR  # type: ignore
except Exception:
    BASE_DIR = Path(__file__).resolve().parent.parent
    INSTAGRAM_INPUT_DIR = BASE_DIR / "Input" / "instagram"
INSTAGRAM_INPUT_DIR = Path(INSTAGRAM_INPUT_DIR)

SOURCE_PREFIX = "instagram"

# ----------------------------------------------------------------------------
# CONFIG — direct-message sampling (MVP, explicitly expandable — project
# owner, 2026-09-15: "un misto tra troncamento messaggi e troncamento
# numero chat, basta che sia espandibile dopo"). Changing these two
# numbers is the entire expansion path; no other logic needs touching.
# ----------------------------------------------------------------------------
TOP_N_THREADS_FOR_FULL_TEXT = 20
MAX_CHARS_PER_MESSAGE = 300


# ============================================================================
# TEXT / TIMESTAMP HELPERS
# ============================================================================


def fix_mojibake(text: Optional[str]) -> Optional[str]:
    """
    Reverses Instagram's own export bug (see module docstring, finding 1):
    UTF-8 bytes written out as if they were Latin-1. Safe on already-clean
    text — if the round trip isn't valid (i.e. the string wasn't actually
    mis-decoded), the original string is returned unchanged.
    """
    if not text:
        return text
    try:
        return text.encode("latin1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def unix_seconds_to_iso(value: Any) -> Optional[str]:
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return None
    if ts <= 0:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def unix_ms_to_iso(value: Any) -> Optional[str]:
    try:
        ts_ms = float(value)
    except (TypeError, ValueError):
        return None
    if ts_ms <= 0:
        return None
    return datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _unwrap_list(data: Any) -> List[Any]:
    """
    Instagram wraps most category files in a single named key
    (e.g. {"relationships_following": [...]}) but not all of them
    (post_comments_1.json, liked_posts.json are bare top-level lists).
    Handles both without the caller needing to know which shape a given
    file uses.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                return value
    return []


def _load_json(path: Path) -> Any:
    import json

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _glob_all(export_dirs: Iterable[Path], relative_pattern: str) -> Iterator[Path]:
    """Applies one glob pattern across every export snapshot folder (see
    collect_export_dirs) and yields matches from all of them, so a
    future second export drop is picked up automatically."""
    for export_dir in export_dirs:
        yield from sorted(export_dir.glob(relative_pattern))


def collect_export_dirs(base_input_dir: Path) -> List[Path]:
    """
    Each Instagram export the project owner downloads lives in its own
    subfolder under INSTAGRAM_INPUT_DIR (project owner's own convention,
    agreed 2026-09-15, because a re-export can arrive as a new subfolder
    without overwriting the previous one — see config.py's note on
    INSTAGRAM_INPUT_DIR). Every immediate subdirectory is treated as one
    export snapshot; overlapping data across snapshots is handled by
    record-level dedup_key, not by this function.
    """
    if not base_input_dir.exists():
        return []
    return sorted(p for p in base_input_dir.iterdir() if p.is_dir())


# ============================================================================
# TABLE DECLARATIONS (timelive.md §3)
# ============================================================================

POSTS_TABLE = TableSpec(
    name="instagram_posts",
    primary_key_column="post_media_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="post_timestamp",
    extra_indexed_columns=["content_kind"],
    columns=[
        ColumnSpec("post_media_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("content_kind", "TEXT", not_null=True,
                   semantic_note="one of: 'post', 'story', 'reel', 'archived_post', 'other' — which export category this row came from"),
        ColumnSpec("caption", "TEXT", semantic_note="native, the project owner's own caption — may be null (many stories/reels have none)"),
        ColumnSpec("media_uri", "TEXT", semantic_note="relative path into the raw export's media/ folder — a reference only, the file itself is never read or interpreted by this ingest"),
        ColumnSpec("media_index_in_group", "INTEGER", semantic_note="position of this media item within its post/carousel — 0 for the first"),
        ColumnSpec("latitude", "REAL", entity_hint="location", semantic_note="native GPS from the post's own metadata, present only on some geotagged posts (see module docstring, finding 2) — null otherwise, never inferred"),
        ColumnSpec("longitude", "REAL", entity_hint="location"),
        ColumnSpec("post_timestamp", "TEXT", not_null=True,
                   semantic_note="canonical timestamp — native, ISO 8601 UTC; group-level creation time when the export shape provides one, otherwise this media item's own"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

COMMENTS_TABLE = TableSpec(
    name="instagram_comments",
    primary_key_column="comment_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="comment_timestamp",
    extra_indexed_columns=["content_kind"],
    columns=[
        ColumnSpec("comment_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("content_kind", "TEXT", not_null=True, semantic_note="'post', 'reel', or 'story' — which media type this comment was made on"),
        ColumnSpec("comment_text", "TEXT", semantic_note="native, the project owner's own comment"),
        ColumnSpec("media_owner_username", "TEXT", entity_hint="person", semantic_note="native username of the account that owns the post/reel/story commented on — NOT the project owner"),
        ColumnSpec("media_uri", "TEXT", semantic_note="reference only, see instagram_posts.media_uri"),
        ColumnSpec("comment_timestamp", "TEXT", not_null=True, semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

LIKES_TABLE = TableSpec(
    name="instagram_likes",
    primary_key_column="like_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="like_timestamp",
    extra_indexed_columns=["content_kind"],
    columns=[
        ColumnSpec("like_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("content_kind", "TEXT", not_null=True, semantic_note="'post' or 'comment' — what was liked"),
        ColumnSpec("content_text", "TEXT", semantic_note="native — the liked post's own caption (content_kind='post') or the liked comment's own text (content_kind='comment'); public content someone else chose to publish, not a private message (see module docstring, finding 3)"),
        ColumnSpec("target_url", "TEXT", semantic_note="native permalink to the liked post/comment, when the export provides one"),
        ColumnSpec("owner_name", "TEXT", semantic_note="native display name of the post's owner — only populated for content_kind='post' (liked_posts.json carries it, liked_comments.json does not)"),
        ColumnSpec("owner_username", "TEXT", entity_hint="person", semantic_note="native username of the post/comment owner — NOT the project owner"),
        ColumnSpec("like_timestamp", "TEXT", not_null=True, semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

FOLLOWERS_TABLE = TableSpec(
    name="instagram_followers",
    primary_key_column="follower_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="followed_timestamp",
    columns=[
        ColumnSpec("follower_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("username", "TEXT", not_null=True, entity_hint="person", semantic_note="native — someone who follows the project owner"),
        ColumnSpec("profile_url", "TEXT", semantic_note="native"),
        ColumnSpec("followed_timestamp", "TEXT", semantic_note="canonical timestamp — native, ISO 8601 UTC; when this account started following the project owner"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

FOLLOWING_TABLE = TableSpec(
    name="instagram_following",
    primary_key_column="following_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="followed_timestamp",
    columns=[
        ColumnSpec("following_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("username", "TEXT", not_null=True, entity_hint="person", semantic_note="native — someone the project owner follows"),
        ColumnSpec("profile_url", "TEXT", semantic_note="native"),
        ColumnSpec("followed_timestamp", "TEXT", semantic_note="canonical timestamp — native, ISO 8601 UTC; when the project owner started following this account"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

DM_THREADS_TABLE = TableSpec(
    name="instagram_direct_message_threads",
    primary_key_column="thread_id",
    dedup_key_column="thread_path",
    canonical_timestamp_column="last_message_timestamp",
    columns=[
        ColumnSpec("thread_id", "INTEGER"),
        ColumnSpec("thread_path", "TEXT", not_null=True, semantic_note="native, unique per conversation — e.g. 'inbox/edoardocavassa_516770459720154'"),
        ColumnSpec("participants", "TEXT", entity_hint="person", semantic_note="native display names, '; '-joined — includes the project owner's own name (Instagram's export lists every participant, not just the other side), so a normal 1:1 DM already shows 2 names here; see is_group for the actual group/1:1 distinction"),
        ColumnSpec("is_group", "INTEGER", semantic_note="derived, deterministic: 1 when more than one participant besides the project owner, 0 otherwise"),
        ColumnSpec("message_count", "INTEGER", semantic_note="native — total messages in this thread across all message_*.json parts, counted regardless of sampling"),
        ColumnSpec("first_message_timestamp", "TEXT", semantic_note="native, ISO 8601 UTC"),
        ColumnSpec("last_message_timestamp", "TEXT", semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("is_sampled", "INTEGER", not_null=True,
                   semantic_note=f"1 if this is one of the {TOP_N_THREADS_FOR_FULL_TEXT} busiest threads (see instagram_ingest.TOP_N_THREADS_FOR_FULL_TEXT) — only those threads have matching rows in instagram_direct_messages; every other thread has metadata here only, by explicit MVP scoping, not a data gap"),
        ColumnSpec("thread_category", "TEXT", semantic_note="'inbox' or 'message_request'"),
        ColumnSpec("source_folder", "TEXT"),
    ],
)

DM_MESSAGES_TABLE = TableSpec(
    name="instagram_direct_messages",
    primary_key_column="message_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="message_timestamp",
    foreign_keys={"thread_path": "instagram_direct_message_threads(thread_path)"},
    columns=[
        ColumnSpec("message_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("thread_path", "TEXT", not_null=True),
        ColumnSpec("sender_name", "TEXT", entity_hint="person", semantic_note="native display name — the project owner's own name appears here too for messages they sent"),
        ColumnSpec("message_content", "TEXT", sensitive=True,
                   semantic_note=f"native message text, truncated to {MAX_CHARS_PER_MESSAGE} characters (MVP sampling — see instagram_ingest.MAX_CHARS_PER_MESSAGE; a trailing '…' marks a cut string). Only present for threads where instagram_direct_message_threads.is_sampled=1."),
        ColumnSpec("message_timestamp", "TEXT", not_null=True, semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("message_index_in_thread", "INTEGER", semantic_note="0-based position within the thread, chronological"),
        ColumnSpec("source_file", "TEXT"),
    ],
)

LOGIN_ACTIVITY_TABLE = TableSpec(
    name="instagram_login_activity",
    primary_key_column="login_event_id",
    dedup_key_column="dedup_key",
    canonical_timestamp_column="event_timestamp",
    extra_indexed_columns=["event_kind"],
    columns=[
        ColumnSpec("login_event_id", "INTEGER"),
        ColumnSpec("dedup_key", "TEXT", not_null=True, semantic_note="internal only"),
        ColumnSpec("event_kind", "TEXT", not_null=True, semantic_note="'login' or 'logout'"),
        ColumnSpec("cookie_name", "TEXT", semantic_note="native"),
        ColumnSpec("user_agent", "TEXT", semantic_note="native, verbatim — device/browser string"),
        ColumnSpec("language_code", "TEXT", semantic_note="native"),
        ColumnSpec("port", "TEXT", semantic_note="native, kept as text since the export's own formatting isn't guaranteed to be a plain integer"),
        ColumnSpec("event_timestamp", "TEXT", not_null=True, semantic_note="canonical timestamp — native, ISO 8601 UTC"),
        ColumnSpec("source_file", "TEXT"),
    ],
)
# Deliberately absent: an IP Address column. The raw export has one; it is
# never read into a record here at all (see module docstring, finding 4)
# — not stored-then-hidden, simply never extracted.

for _table in (
    POSTS_TABLE, COMMENTS_TABLE, LIKES_TABLE, FOLLOWERS_TABLE, FOLLOWING_TABLE,
    DM_THREADS_TABLE, DM_MESSAGES_TABLE, LOGIN_ACTIVITY_TABLE,
):
    register_table_spec(_table)


# ============================================================================
# PARSING — posts / stories / reels / archived / other (module docstring,
# finding 2: four raw shapes, normalized here into one row shape)
# ============================================================================


def _label_values_map(label_values: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Shape-B helper: {"label": X, "value": Y} entries become {X: Y}.
    Entries with no "value" (a bare toggle/flag) or a non-"value" payload
    ("media", "dict", "timestamp_value", "vec") are skipped here — callers
    that need those look at the raw list directly (see _iter_post_media_rows)."""
    result: Dict[str, Any] = {}
    for entry in label_values:
        label = entry.get("label")
        if label and "value" in entry:
            result[label] = entry.get("value")
    return result


def _find_label_entry(label_values: List[Dict[str, Any]], label: str) -> Optional[Dict[str, Any]]:
    for entry in label_values:
        if entry.get("label") == label:
            return entry
    return None


def _iter_post_media_rows(raw_items: List[Any], content_kind: str, source_file: str) -> Iterator[Dict[str, Any]]:
    for item_index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            continue

        if "label_values" in item:
            # Shape B: rich generic event (posts.json, other_content.json)
            label_values = item.get("label_values") or []
            labels = _label_values_map(label_values)
            group_caption = fix_mojibake(labels.get("Caption"))
            group_ts = unix_seconds_to_iso(item.get("timestamp"))
            media_entry = _find_label_entry(label_values, "Media")
            media_list = (media_entry or {}).get("media") or item.get("media") or []
            try:
                latitude = float(labels["Latitude"]) if labels.get("Latitude") not in (None, "") else None
            except (TypeError, ValueError):
                latitude = None
            try:
                longitude = float(labels["Longitude"]) if labels.get("Longitude") not in (None, "") else None
            except (TypeError, ValueError):
                longitude = None
        else:
            # Shapes A / C / D: item may itself be a media entry (C), or a
            # group wrapping a "media" list (A/D, caption/timestamp may or
            # may not be at the group level).
            group_caption = fix_mojibake(item.get("title"))
            group_ts = unix_seconds_to_iso(item.get("creation_timestamp"))
            media_list = item.get("media")
            if media_list is None:
                media_list = [item]  # Shape C: the item itself is the one media entry
            latitude = None
            longitude = None

        if not media_list:
            continue

        for index, media in enumerate(media_list):
            if not isinstance(media, dict):
                continue
            media_ts = unix_seconds_to_iso(media.get("creation_timestamp"))
            post_ts = group_ts or media_ts
            if not post_ts:
                continue  # no usable timestamp at all — can't place this row on the canonical axis
            caption = group_caption if group_caption else fix_mojibake(media.get("title"))
            media_uri = media.get("uri")
            # Uniqueness relies on (source_file, item_index, media_index), NOT on
            # (timestamp, uri) alone: real duplicates were found in this export
            # where two genuinely different raw records share both (e.g. several
            # other_content.json entries with an empty media list at the same
            # second). Same policy as spotify_ingest.py's dedup key (see its
            # module docstring): every raw record stays its own row; natural
            # fields are kept in the key for readability, not for uniqueness.
            dedup_key = "|".join([content_kind, post_ts, media_uri or "", source_file, str(item_index), str(index)])
            yield {
                "dedup_key": dedup_key,
                "content_kind": content_kind,
                "caption": caption or None,
                "media_uri": media_uri,
                "media_index_in_group": index,
                "latitude": latitude,
                "longitude": longitude,
                "post_timestamp": post_ts,
                "source_file": source_file,
            }


def parse_posts(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    file_kinds = [
        ("your_instagram_activity/media/posts*.json", "post"),
        ("your_instagram_activity/media/stories.json", "story"),
        ("your_instagram_activity/media/reels.json", "reel"),
        ("your_instagram_activity/media/archived_posts.json", "archived_post"),
        ("your_instagram_activity/media/other_content.json", "other"),
    ]
    for pattern, content_kind in file_kinds:
        for path in _glob_all(export_dirs, pattern):
            try:
                raw = _unwrap_list(_load_json(path))
            except Exception as exc:
                logger.warning("%s: read error: %s", path, exc)
                continue
            records.extend(_iter_post_media_rows(raw, content_kind, path.name))
    return records


# ============================================================================
# PARSING — comments
# ============================================================================


def parse_comments(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    file_kinds = [
        ("your_instagram_activity/comments/post_comments*.json", "post"),
        ("your_instagram_activity/comments/reels_comments.json", "reel"),
        ("your_instagram_activity/comments/hype.json", "story"),
    ]
    for pattern, content_kind in file_kinds:
        for path in _glob_all(export_dirs, pattern):
            try:
                raw = _unwrap_list(_load_json(path))
            except Exception as exc:
                logger.warning("%s: read error: %s", path, exc)
                continue
            for item_index, item in enumerate(raw):
                if not isinstance(item, dict):
                    continue
                string_map = item.get("string_map_data") or {}
                comment_text = fix_mojibake((string_map.get("Comment") or {}).get("value"))
                media_owner = fix_mojibake((string_map.get("Media Owner") or {}).get("value"))
                ts = unix_seconds_to_iso((string_map.get("Time") or {}).get("timestamp"))
                if not ts:
                    continue
                media_list = item.get("media_list_data") or []
                media_uri = media_list[0].get("uri") if media_list and isinstance(media_list[0], dict) else None
                # (source_file, item_index) tiebreak — see _iter_post_media_rows's
                # comment on why natural fields alone aren't trusted for uniqueness.
                dedup_key = "|".join([content_kind, ts, media_owner or "", path.name, str(item_index)])
                records.append({
                    "dedup_key": dedup_key,
                    "content_kind": content_kind,
                    "comment_text": comment_text or None,
                    "media_owner_username": media_owner or None,
                    "media_uri": media_uri or None,
                    "comment_timestamp": ts,
                    "source_file": path.name,
                })
    return records


# ============================================================================
# PARSING — likes (posts + comments)
# ============================================================================


def _extract_owner(label_values: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
    """liked_posts.json's Shape-B "Owner" label nests two dict levels down
    (module docstring, finding 3) — {"dict":[{"dict":[{"label":"Name",...},
    {"label":"Username",...}],...}],"title":"Owner"}."""
    owner_entry = None
    for entry in label_values:
        if entry.get("title") == "Owner":
            owner_entry = entry
            break
    if not owner_entry:
        return None, None
    outer = owner_entry.get("dict") or []
    if not outer or not isinstance(outer[0], dict):
        return None, None
    inner = outer[0].get("dict") or []
    inner_map = {e.get("label"): e.get("value") for e in inner if isinstance(e, dict)}
    return fix_mojibake(inner_map.get("Name")) or None, inner_map.get("Username") or None


def parse_likes(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    for path in _glob_all(export_dirs, "your_instagram_activity/likes/liked_posts.json"):
        try:
            raw = _unwrap_list(_load_json(path))
        except Exception as exc:
            logger.warning("%s: read error: %s", path, exc)
            continue
        for item_index, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            label_values = item.get("label_values") or []
            labels = _label_values_map(label_values)
            ts = unix_seconds_to_iso(item.get("timestamp"))
            if not ts:
                continue
            owner_name, owner_username = _extract_owner(label_values)
            caption = fix_mojibake(labels.get("Caption")) or None
            url = labels.get("URL")
            dedup_key = "|".join(["post", ts, url or owner_username or "", path.name, str(item_index)])
            records.append({
                "dedup_key": dedup_key,
                "content_kind": "post",
                "content_text": caption,
                "target_url": url,
                "owner_name": owner_name,
                "owner_username": owner_username,
                "like_timestamp": ts,
                "source_file": path.name,
            })

    for path in _glob_all(export_dirs, "your_instagram_activity/likes/liked_comments.json"):
        try:
            raw = _unwrap_list(_load_json(path))
        except Exception as exc:
            logger.warning("%s: read error: %s", path, exc)
            continue
        for item_index, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            owner_username = item.get("title") or None
            entries = item.get("string_list_data") or []
            entry = entries[0] if entries and isinstance(entries[0], dict) else {}
            ts = unix_seconds_to_iso(entry.get("timestamp"))
            if not ts:
                continue
            comment_text = fix_mojibake(entry.get("value")) or None
            url = entry.get("href")
            # Real finding: two DIFFERENT commenters can have their comment
            # liked on the same post at the same second (both dasdo84 and
            # elias_alias_messias here) — url+timestamp alone is not unique,
            # owner_username (the comment's author) is what actually
            # distinguishes them. Without it this silently dropped one of
            # the two real likes on the first ingest test — fixed here.
            dedup_key = "|".join(["comment", ts, url or "", owner_username or "", path.name, str(item_index)])
            records.append({
                "dedup_key": dedup_key,
                "content_kind": "comment",
                "content_text": comment_text,
                "target_url": url,
                "owner_name": None,
                "owner_username": owner_username,
                "like_timestamp": ts,
                "source_file": path.name,
            })

    return records


# ============================================================================
# PARSING — followers / following
# ============================================================================


def _parse_relationship_file(export_dirs: List[Path], glob_pattern: str) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in _glob_all(export_dirs, glob_pattern):
        try:
            raw = _unwrap_list(_load_json(path))
        except Exception as exc:
            logger.warning("%s: read error: %s", path, exc)
            continue
        for item in raw:
            if not isinstance(item, dict):
                continue
            entries = item.get("string_list_data") or []
            entry = entries[0] if entries and isinstance(entries[0], dict) else {}
            username = entry.get("value") or item.get("title") or None
            if not username:
                continue
            ts = unix_seconds_to_iso(entry.get("timestamp"))
            dedup_key = "|".join([username, ts or ""])
            records.append({
                "dedup_key": dedup_key,
                "username": username,
                "profile_url": entry.get("href"),
                "followed_timestamp": ts,
                "source_file": path.name,
            })
    return records


def parse_followers(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    return _parse_relationship_file(export_dirs, "connections/followers_and_following/followers*.json")


def parse_following(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    return _parse_relationship_file(export_dirs, "connections/followers_and_following/following.json")


# ============================================================================
# PARSING — direct messages (module docstring, finding 5)
# ============================================================================


def _load_thread_messages(thread_dir: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Merges every message_*.json part in a thread folder (a long-running
    thread can be split across several numbered files), sorted so parts
    interleave correctly by message timestamp."""
    all_messages: List[Dict[str, Any]] = []
    participants: List[str] = []
    for part_path in sorted(thread_dir.glob("message_*.json")):
        try:
            data = _load_json(part_path)
        except Exception as exc:
            logger.warning("%s: read error: %s", part_path, exc)
            continue
        if not participants:
            participants = [
                fix_mojibake(p.get("name")) for p in (data.get("participants") or []) if isinstance(p, dict) and p.get("name")
            ]
        all_messages.extend(data.get("messages") or [])
    all_messages.sort(key=lambda m: m.get("timestamp_ms") or 0)
    return participants, all_messages


def parse_direct_messages(export_dirs: List[Path]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Returns (thread_rows, message_rows). Every real thread gets a
    thread_row; only the TOP_N_THREADS_FOR_FULL_TEXT busiest get
    message_rows (see module docstring, finding 5)."""
    thread_candidates: List[Dict[str, Any]] = []  # one dict per thread, holds everything needed for both tables

    for category, subfolder in (("inbox", "inbox"), ("message_request", "message_requests")):
        for export_dir in export_dirs:
            base = export_dir / "your_instagram_activity" / "messages" / subfolder
            if not base.exists():
                continue
            for thread_dir in sorted(p for p in base.iterdir() if p.is_dir()):
                participants, messages = _load_thread_messages(thread_dir)
                if not messages:
                    continue
                timestamps = [unix_ms_to_iso(m.get("timestamp_ms")) for m in messages]
                timestamps = [t for t in timestamps if t]
                if not timestamps:
                    continue
                thread_candidates.append({
                    "thread_path": f"{subfolder}/{thread_dir.name}",
                    "participants": participants,
                    "messages": messages,
                    "message_count": len(messages),
                    "first_message_timestamp": min(timestamps),
                    "last_message_timestamp": max(timestamps),
                    "thread_category": category,
                    "source_folder": thread_dir.name,
                })

    thread_candidates.sort(key=lambda t: t["message_count"], reverse=True)
    sampled_paths = {t["thread_path"] for t in thread_candidates[:TOP_N_THREADS_FOR_FULL_TEXT]}

    thread_rows: List[Dict[str, Any]] = []
    message_rows: List[Dict[str, Any]] = []

    for thread in thread_candidates:
        is_sampled = thread["thread_path"] in sampled_paths
        thread_rows.append({
            "dedup_key": thread["thread_path"],
            "thread_path": thread["thread_path"],
            "participants": "; ".join(thread["participants"]) or None,
            # Real finding: Instagram's own "participants" list includes the
            # project owner too (a 1:1 DM has 2 entries, not 1 as first
            # assumed from a truncated debug sample) — so "group" means more
            # than one participant BESIDES the owner, i.e. more than 2 total.
            "is_group": 1 if len(thread["participants"]) > 2 else 0,
            "message_count": thread["message_count"],
            "first_message_timestamp": thread["first_message_timestamp"],
            "last_message_timestamp": thread["last_message_timestamp"],
            "is_sampled": 1 if is_sampled else 0,
            "thread_category": thread["thread_category"],
            "source_folder": thread["source_folder"],
        })

        if not is_sampled:
            continue

        for index, message in enumerate(thread["messages"]):
            ts = unix_ms_to_iso(message.get("timestamp_ms"))
            if not ts:
                continue
            sender = fix_mojibake(message.get("sender_name"))
            content = truncate_text(fix_mojibake(message.get("content")), MAX_CHARS_PER_MESSAGE)
            dedup_key = "|".join([thread["thread_path"], str(message.get("timestamp_ms")), sender or "", str(index)])
            message_rows.append({
                "dedup_key": dedup_key,
                "thread_path": thread["thread_path"],
                "sender_name": sender,
                "message_content": content,
                "message_timestamp": ts,
                "message_index_in_thread": index,
                "source_file": f"{thread['thread_path']}/message_*.json",
            })

    return thread_rows, message_rows


# ============================================================================
# PARSING — login / logout activity (module docstring, finding 4: no IP)
# ============================================================================


def _parse_account_history_file(export_dirs: List[Path], relative_path: str, event_kind: str) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for path in _glob_all(export_dirs, relative_path):
        try:
            raw = _unwrap_list(_load_json(path))
        except Exception as exc:
            logger.warning("%s: read error: %s", path, exc)
            continue
        for item_index, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            string_map = item.get("string_map_data") or {}
            ts = unix_seconds_to_iso((string_map.get("Time") or {}).get("timestamp"))
            if not ts:
                continue
            cookie_name = string_map.get("Cookie Name", {}).get("value")
            user_agent = string_map.get("User Agent", {}).get("value")
            language_code = string_map.get("Language Code", {}).get("value")
            port = string_map.get("Port", {}).get("value")
            # IP Address deliberately not read from string_map at all — see
            # module docstring, finding 4.
            dedup_key = "|".join([event_kind, ts, str(cookie_name), path.name, str(item_index)])
            records.append({
                "dedup_key": dedup_key,
                "event_kind": event_kind,
                "cookie_name": cookie_name,
                "user_agent": fix_mojibake(user_agent),
                "language_code": language_code,
                "port": str(port) if port is not None else None,
                "event_timestamp": ts,
                "source_file": path.name,
            })
    return records


def parse_login_activity(export_dirs: List[Path]) -> List[Dict[str, Any]]:
    records = _parse_account_history_file(
        export_dirs, "security_and_login_information/login_and_profile_creation/login_activity.json", "login"
    )
    records += _parse_account_history_file(
        export_dirs, "security_and_login_information/login_and_profile_creation/logout_activity.json", "logout"
    )
    return records


# ============================================================================
# MAIN ENTRYPOINT — the contract ingest_engine.py's CLI expects
# ============================================================================


def run_ingest(conn, dry_run: bool = False, verbose: bool = False) -> IngestReport:
    for table in (
        POSTS_TABLE, COMMENTS_TABLE, LIKES_TABLE, FOLLOWERS_TABLE, FOLLOWING_TABLE,
        DM_THREADS_TABLE, DM_MESSAGES_TABLE, LOGIN_ACTIVITY_TABLE,
    ):
        create_schema_for_table(conn, table)

    export_dirs = collect_export_dirs(INSTAGRAM_INPUT_DIR)
    logger.info("found %d export snapshot(s) in %s", len(export_dirs), INSTAGRAM_INPUT_DIR)

    posts = parse_posts(export_dirs)
    comments = parse_comments(export_dirs)
    likes = parse_likes(export_dirs)
    followers = parse_followers(export_dirs)
    following = parse_following(export_dirs)
    thread_rows, message_rows = parse_direct_messages(export_dirs)
    login_activity = parse_login_activity(export_dirs)

    logger.info(
        "parsed: %d post media row(s), %d comment(s), %d like(s), %d follower(s), "
        "%d following, %d DM thread(s) (%d sampled, %d message rows), %d login/logout event(s)",
        len(posts), len(comments), len(likes), len(followers), len(following),
        len(thread_rows), sum(1 for t in thread_rows if t["is_sampled"]), len(message_rows),
        len(login_activity),
    )

    rows_inserted = 0
    rows_already_present = 0
    tables_written: List[str] = []

    for table, records in (
        (POSTS_TABLE, posts),
        (COMMENTS_TABLE, comments),
        (LIKES_TABLE, likes),
        (FOLLOWERS_TABLE, followers),
        (FOLLOWING_TABLE, following),
        (DM_THREADS_TABLE, thread_rows),
        (DM_MESSAGES_TABLE, message_rows),
        (LOGIN_ACTIVITY_TABLE, login_activity),
    ):
        if not records:
            continue
        outcomes: List[UpsertOutcome] = upsert_rows(conn, table, records)
        rows_inserted += sum(1 for o in outcomes if o.was_new)
        rows_already_present += sum(1 for o in outcomes if not o.was_new)
        tables_written.append(table.name)

    return IngestReport(
        domain="instagram",
        tables_written=tables_written,
        rows_inserted=rows_inserted,
        rows_already_present=rows_already_present,
        dry_run=dry_run,
    )
