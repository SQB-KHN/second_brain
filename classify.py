#!/usr/bin/env python3
"""
SecondSelf classify CLI — auto-classify raw captures into PARA wiki notes.

Usage examples:
  python classify.py              # classify all unprocessed captures
  python classify.py --scan-only  # list unprocessed captures without classifying
  python classify.py --show-prompt  # preview LLM prompts for the next capture
  python classify.py --dry-run      # classify without writing wiki files
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

try:
    from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError
except ImportError:
    print(
        "Missing dependencies. Run:\n"
        "  pip install -r requirements.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)

from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_LLM_MODEL,
    LLM_MODEL,
    OPENAI_API_KEY,
    PARA_FOLDERS,
    PIPELINE_LOG,
    RAW_DIR,
    ROOT,
    WIKI_DIR,
    WIKI_INDEX_FILE,
    ensure_directories,
)

RESERVED_RAW_JSON = {"meta.json"}
REQUIRED_CAPTURE_FIELDS = ("id", "timestamp", "type")
VALID_CAPTURE_TYPES = ("note", "link", "file")
MAX_PROMPT_CONTENT_CHARS = 24_000
MAX_EXISTING_TAGS = 40
MAX_API_RETRIES = 3
PARA_ALIASES = {
    "project": "projects",
    "projects": "projects",
    "area": "areas",
    "areas": "areas",
    "resource": "resources",
    "resources": "resources",
    "archive": "archives",
    "archives": "archives",
}
STRICT_JSON_SUFFIX = (
    "\n\nReturn only a single JSON object. "
    "Do not wrap the JSON in markdown code fences."
)


@dataclass(frozen=True)
class RawCapture:
    """A validated raw capture loaded from data/raw/."""

    id: str
    path: Path
    record: dict[str, Any]


@dataclass(frozen=True)
class ClassificationPrompt:
    """OpenAI chat messages for classifying one raw capture."""

    system: str
    user: str

    def as_messages(self) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user},
        ]


@dataclass(frozen=True)
class ClassificationResult:
    """Parsed LLM classification for one capture."""

    title: str
    para: str
    tags: list[str]
    summary: str


PARA_CATEGORY_GUIDE = """
PARA categories (pick exactly one):

1. projects — Active work with a clear outcome and deadline.
   Examples:
   - "Build SecondSelf MVP for demo day"
   - "Write Q3 product roadmap"
   - "Renovate kitchen before December"

2. areas — Ongoing responsibilities or standards to maintain over time.
   Examples:
   - "Personal health and fitness habits"
   - "Team leadership and 1:1s"
   - "Household budgeting"

3. resources — Reference material, ideas, or topics useful later but not active work.
   Examples:
   - "Article about the PARA method"
   - "Python asyncio cheatsheet"
   - "Interesting podcast on knowledge management"

4. archives — Inactive or completed items no longer relevant to active work.
   Examples:
   - "Completed hackathon submission notes"
   - "Old job onboarding checklist"
   - "Past conference talk that is no longer maintained"
""".strip()

CLASSIFICATION_RESPONSE_SCHEMA = textwrap.dedent(
    """
    {
      "title": "Short descriptive title for the note (5-12 words)",
      "para": "projects | areas | resources | archives",
      "tags": ["kebab-case-tag", "another-tag"],
      "summary": "One-line summary of the capture (max 160 characters)"
    }
    """
).strip()

CLASSIFICATION_SYSTEM_PROMPT = f"""You are a personal knowledge librarian for SecondSelf.

Your job is to classify one raw capture into the PARA method and return structured JSON only.

{PARA_CATEGORY_GUIDE}

Classification rules:
- Choose the single best PARA category for the capture's current relevance.
- Prefer projects when there is an active goal, deadline, or deliverable.
- Prefer areas for enduring responsibilities without a finish line.
- Prefer resources for reference links, articles, files, and saved ideas.
- Prefer archives only when the item is clearly completed, outdated, or inactive.
- Generate 1-5 concise lowercase tags (use hyphens for multi-word tags).
- Write summary as one plain sentence, no markdown.
- Write title in title case, no quotes.

Respond with valid JSON only — no markdown fences, no commentary.
The JSON must match this schema exactly:
{CLASSIFICATION_RESPONSE_SCHEMA}
"""


def setup_logging() -> logging.Logger:
    """Configure pipeline logger (file + stderr)."""
    ensure_directories()
    logger = logging.getLogger("secondself.classify")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(PIPELINE_LOG, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


LOGGER = setup_logging()


def list_raw_capture_files() -> list[Path]:
    """Return capture JSON files in data/raw/, excluding index and temp files."""
    files: list[Path] = []
    for path in sorted(RAW_DIR.glob("*.json")):
        if path.name in RESERVED_RAW_JSON or path.name.startswith("."):
            continue
        files.append(path)
    return files


def load_raw_capture(path: Path) -> RawCapture | None:
    """Load and validate one raw capture file. Returns None if invalid."""
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        LOGGER.warning("Skipping %s: invalid JSON (%s)", path.name, exc)
        return None

    if not isinstance(record, dict):
        LOGGER.warning("Skipping %s: expected JSON object", path.name)
        return None

    missing = [field for field in REQUIRED_CAPTURE_FIELDS if not record.get(field)]
    if missing:
        LOGGER.warning(
            "Skipping %s: missing required field(s): %s",
            path.name,
            ", ".join(missing),
        )
        return None

    capture_id = str(record["id"])
    return RawCapture(id=capture_id, path=path, record=record)


def load_all_raw_captures() -> list[RawCapture]:
    """Load every valid raw capture from data/raw/."""
    captures: list[RawCapture] = []
    for path in list_raw_capture_files():
        capture = load_raw_capture(path)
        if capture is not None:
            captures.append(capture)
    return captures


def _wiki_markdown_files() -> list[Path]:
    return sorted(
        path
        for para in PARA_FOLDERS
        for path in (WIKI_DIR / para).glob("*.md")
        if path.is_file()
    )


def parse_frontmatter(path: Path) -> dict[str, Any] | None:
    """Parse YAML frontmatter from a wiki markdown file."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        LOGGER.warning("Skipping %s: cannot read file (%s)", path, exc)
        return None

    if not content.startswith("---"):
        LOGGER.warning("Skipping %s: missing YAML frontmatter", path)
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        LOGGER.warning("Skipping %s: malformed frontmatter", path)
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        LOGGER.warning("Skipping %s: invalid YAML frontmatter (%s)", path, exc)
        return None

    if not isinstance(frontmatter, dict):
        LOGGER.warning("Skipping %s: frontmatter is not a mapping", path)
        return None

    return frontmatter


def rebuild_wiki_index_from_files() -> dict[str, str]:
    """Rebuild id → wiki path mapping by scanning wiki markdown frontmatter."""
    index: dict[str, str] = {}

    for path in _wiki_markdown_files():
        frontmatter = parse_frontmatter(path)
        if frontmatter is None:
            continue

        note_id = frontmatter.get("id")
        if not note_id:
            LOGGER.warning("Skipping %s: frontmatter missing id", path)
            continue

        note_id = str(note_id)
        wiki_path = path.relative_to(ROOT).as_posix()

        if note_id in index and index[note_id] != wiki_path:
            LOGGER.warning(
                "Duplicate wiki id %s: keeping %s, ignoring %s",
                note_id,
                index[note_id],
                wiki_path,
            )
            continue

        index[note_id] = wiki_path

    return index


def load_wiki_index() -> dict[str, str]:
    """
    Load wiki/.index.json (id → relative wiki path).

    If the index file is missing or invalid, rebuild it from wiki frontmatter.
    """
    if WIKI_INDEX_FILE.exists():
        try:
            data = json.loads(WIKI_INDEX_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            LOGGER.warning(
                "wiki/.index.json is unreadable (%s); rebuilding from wiki files",
                exc,
            )
            return rebuild_wiki_index_from_files()

        if isinstance(data, dict):
            if "entries" in data and isinstance(data["entries"], dict):
                entries = data["entries"]
            else:
                entries = {
                    key: value
                    for key, value in data.items()
                    if not key.startswith("_") and key not in {"updated_at", "count"}
                }

            index = {str(note_id): str(path) for note_id, path in entries.items()}
            if index or not _wiki_markdown_files():
                return index

            LOGGER.warning(
                "wiki/.index.json is empty but wiki notes exist; rebuilding from files"
            )
            return rebuild_wiki_index_from_files()

        LOGGER.warning(
            "wiki/.index.json has unexpected format; rebuilding from wiki files"
        )

    return rebuild_wiki_index_from_files()


def get_classified_ids() -> set[str]:
    """Return capture IDs that already have wiki entries."""
    return set(load_wiki_index())


def find_unprocessed_captures(
    captures: list[RawCapture] | None = None,
    classified_ids: set[str] | None = None,
) -> list[RawCapture]:
    """Return raw captures whose id is not yet present in the wiki index."""
    if captures is None:
        captures = load_all_raw_captures()
    if classified_ids is None:
        classified_ids = get_classified_ids()

    unprocessed = [capture for capture in captures if capture.id not in classified_ids]
    unprocessed.sort(key=lambda item: item.record.get("timestamp", ""))
    return unprocessed


def truncate_for_prompt(text: str, max_chars: int = MAX_PROMPT_CONTENT_CHARS) -> tuple[str, bool]:
    """Truncate long capture text for the LLM prompt budget."""
    if len(text) <= max_chars:
        return text, False

    head = max_chars // 2
    tail = max_chars - head
    truncated = f"{text[:head]}\n\n[... truncated {len(text) - max_chars} characters ...]\n\n{text[-tail:]}"
    return truncated, True


def collect_existing_tags(limit: int = MAX_EXISTING_TAGS) -> list[str]:
    """Collect unique tags already used in the wiki corpus for prompt context."""
    tags: list[str] = []
    seen: set[str] = set()

    for path in _wiki_markdown_files():
        frontmatter = parse_frontmatter(path)
        if frontmatter is None:
            continue

        raw_tags = frontmatter.get("tags", [])
        if not isinstance(raw_tags, list):
            continue

        for tag in raw_tags:
            normalized = str(tag).strip().lower()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            tags.append(normalized)
            if len(tags) >= limit:
                return tags

    return tags


def format_capture_metadata(capture: RawCapture) -> list[str]:
    """Build metadata lines to include when content is sparse or empty."""
    record = capture.record
    lines = [
        f"id: {capture.id}",
        f"type: {record.get('type', 'unknown')}",
        f"timestamp: {record.get('timestamp', '')}",
    ]

    if record.get("source_url"):
        lines.append(f"source_url: {record['source_url']}")
    if record.get("file_path"):
        lines.append(f"file_path: {record['file_path']}")

    metadata = record.get("metadata", {})
    if isinstance(metadata, dict):
        for key in ("title", "source_url", "original_filename", "content_type"):
            value = metadata.get(key)
            if value:
                lines.append(f"{key}: {value}")

    return lines


def format_capture_body(capture: RawCapture) -> str:
    """Format raw capture content for the LLM user prompt."""
    record = capture.record
    content = str(record.get("content", "") or "").strip()
    metadata_lines = format_capture_metadata(capture)

    if content:
        content, truncated = truncate_for_prompt(content)
        sections = ["Capture metadata:", *metadata_lines, "", "Capture content:", content]
        if truncated:
            sections.append("")
            sections.append(
                f"(Note: content truncated to {MAX_PROMPT_CONTENT_CHARS} characters for classification.)"
            )
        return "\n".join(sections)

    fallback_summary_hint = (
        f"Empty capture — {record.get('type', 'unknown')}."
        if record.get("type") in VALID_CAPTURE_TYPES
        else "Empty capture — unknown."
    )
    return "\n".join(
        [
            "Capture metadata:",
            *metadata_lines,
            "",
            "Capture content:",
            "(empty)",
            "",
            "The capture has no body text. Classify using metadata only.",
            f"If needed, use a summary like: {fallback_summary_hint}",
        ]
    )


def build_classification_system_prompt(existing_tags: list[str] | None = None) -> str:
    """Build the system prompt, optionally including tags already used in the wiki."""
    if not existing_tags:
        return CLASSIFICATION_SYSTEM_PROMPT

    tag_hint = ", ".join(existing_tags[:MAX_EXISTING_TAGS])
    return (
        f"{CLASSIFICATION_SYSTEM_PROMPT}\n\n"
        "Existing tags in this knowledge base (reuse when appropriate, "
        "but you may create new tags):\n"
        f"{tag_hint}"
    )


def build_classification_user_prompt(capture: RawCapture) -> str:
    """Build the user prompt for one raw capture."""
    body = format_capture_body(capture)
    return (
        "Classify this raw capture into PARA.\n\n"
        f"{body}\n\n"
        "Return JSON with keys: title, para, tags, summary."
    )


def build_classification_prompt(
    capture: RawCapture,
    existing_tags: list[str] | None = None,
) -> ClassificationPrompt:
    """Build the full prompt pair for classifying one capture."""
    if existing_tags is None:
        existing_tags = collect_existing_tags()

    return ClassificationPrompt(
        system=build_classification_system_prompt(existing_tags),
        user=build_classification_user_prompt(capture),
    )


def print_classification_prompt(capture: RawCapture) -> None:
    """Print the system and user prompts for one capture."""
    prompt = build_classification_prompt(capture)
    print(f"=== Capture {capture.id} ({capture.path.name}) ===")
    print(f"Model: {LLM_MODEL}")
    print("\n--- SYSTEM ---")
    print(prompt.system)
    print("\n--- USER ---")
    print(prompt.user)
    print()


def iso_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def require_api_key() -> tuple[OpenAI, str]:
    if OPENAI_API_KEY:
        return OpenAI(api_key=OPENAI_API_KEY), LLM_MODEL
    if GROQ_API_KEY:
        LOGGER.info("Using Groq API (OPENAI_API_KEY not set)")
        return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL), GROQ_LLM_MODEL

    LOGGER.error("No LLM API key configured")
    print("Set OPENAI_API_KEY or GROQ_API_KEY in .env", file=sys.stderr)
    raise SystemExit(1)


def get_openai_client() -> tuple[OpenAI, str]:
    return require_api_key()


def extract_json_object(text: str) -> dict[str, Any]:
    """Parse JSON from an LLM response, tolerating fenced code blocks."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError("LLM response is not a JSON object")
    return data


def normalize_para(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    mapped = PARA_ALIASES.get(normalized)
    if mapped:
        if mapped != normalized:
            LOGGER.info("Normalized para %r -> %r", value, mapped)
        return mapped
    LOGGER.warning("Unknown para %r; falling back to resources", value)
    return "resources"


def normalize_tags(tags: Any) -> list[str]:
    if not isinstance(tags, list):
        return ["unclassified"]

    normalized: list[str] = []
    for tag in tags:
        slug = re.sub(r"[^a-z0-9]+", "-", str(tag).strip().lower()).strip("-")
        if slug and slug not in normalized:
            normalized.append(slug)

    return normalized or ["unclassified"]


def parse_classification_result(data: dict[str, Any]) -> ClassificationResult:
    title = str(data.get("title", "")).strip() or "Untitled Capture"
    para = normalize_para(data.get("para"))
    tags = normalize_tags(data.get("tags"))
    summary = str(data.get("summary", "")).strip() or title
    return ClassificationResult(title=title, para=para, tags=tags, summary=summary)


def fallback_classification(capture: RawCapture) -> ClassificationResult:
    record = capture.record
    content = str(record.get("content", "") or "").strip()
    capture_type = str(record.get("type", "note"))
    summary = content[:100] if content else f"Empty capture — {capture_type}."
    return ClassificationResult(
        title=f"Note {capture.id[:8]}",
        para="resources",
        tags=["unclassified"],
        summary=summary,
    )


def call_classification_llm(
    client: OpenAI,
    prompt: ClassificationPrompt,
    model: str,
    *,
    strict: bool = False,
) -> ClassificationResult:
    messages = prompt.as_messages()
    if strict:
        messages = [
            messages[0],
            {"role": "user", "content": messages[1]["content"] + STRICT_JSON_SUFFIX},
        ]

    last_error: Exception | None = None
    for attempt in range(1, MAX_API_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            content = response.choices[0].message.content or ""
            return parse_classification_result(extract_json_object(content))
        except (APIConnectionError, RateLimitError, APIStatusError) as exc:
            last_error = exc
            if attempt == MAX_API_RETRIES:
                break
            delay = 2 ** attempt
            LOGGER.warning(
                "LLM API error (attempt %d/%d): %s; retrying in %ss",
                attempt,
                MAX_API_RETRIES,
                exc,
                delay,
            )
            time.sleep(delay)
        except (json.JSONDecodeError, ValueError, KeyError, IndexError) as exc:
            raise ValueError(str(exc)) from exc

    raise RuntimeError(f"LLM API failed after {MAX_API_RETRIES} attempts: {last_error}")


def classify_capture_with_llm(
    capture: RawCapture,
    client: OpenAI,
    model: str,
    existing_tags: list[str] | None = None,
) -> ClassificationResult:
    prompt = build_classification_prompt(capture, existing_tags=existing_tags)
    try:
        return call_classification_llm(client, prompt, model)
    except ValueError as exc:
        LOGGER.warning(
            "Invalid LLM JSON for %s (%s); retrying with stricter prompt",
            capture.id,
            exc,
        )
        try:
            return call_classification_llm(client, prompt, model, strict=True)
        except (ValueError, RuntimeError) as retry_exc:
            LOGGER.warning(
                "Classification failed for %s after retry (%s); using fallback",
                capture.id,
                retry_exc,
            )
            return fallback_classification(capture)
    except RuntimeError as exc:
        LOGGER.error("Classification failed for %s: %s", capture.id, exc)
        raise


def slugify(title: str, capture_id: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        slug = f"note-{capture_id[:8]}"
    return slug[:80]


def existing_slugs(para: str) -> set[str]:
    return {path.stem for path in (WIKI_DIR / para).glob("*.md")}


def make_unique_slug(para: str, title: str, capture_id: str) -> str:
    base = slugify(title, capture_id)
    slug = base
    taken = existing_slugs(para)
    counter = 2
    while slug in taken:
        slug = f"{base}-{counter}"
        counter += 1
    return slug


def note_body(capture: RawCapture, title: str) -> str:
    record = capture.record
    content = str(record.get("content", "") or "").strip()
    lines = [f"# {title}", ""]

    if content:
        lines.append(content)
    else:
        if record.get("source_url"):
            lines.append(f"Source: {record['source_url']}")
        if record.get("file_path"):
            lines.append(f"File: {record['file_path']}")
        if len(lines) == 2:
            lines.append("_No capture body text._")

    return "\n".join(lines).rstrip() + "\n"


def render_wiki_markdown(capture: RawCapture, result: ClassificationResult) -> str:
    frontmatter = {
        "id": capture.id,
        "created": capture.record.get("timestamp", iso_timestamp()),
        "para": result.para,
        "tags": result.tags,
        "summary": result.summary,
        "source_type": capture.record.get("type", "note"),
        "links": [],
        "embedding_id": "",
    }
    yaml_block = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{yaml_block}\n---\n\n{note_body(capture, result.title)}"


def write_wiki_index(index: dict[str, str]) -> None:
    payload = {
        "updated_at": iso_timestamp(),
        "count": len(index),
        "entries": dict(sorted(index.items())),
    }
    temp_path = WIKI_INDEX_FILE.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(WIKI_INDEX_FILE)


def write_wiki_note(
    capture: RawCapture,
    result: ClassificationResult,
    wiki_index: dict[str, str],
) -> Path:
    slug = make_unique_slug(result.para, result.title, capture.id)
    output_path = WIKI_DIR / result.para / f"{slug}.md"
    output_path.write_text(render_wiki_markdown(capture, result), encoding="utf-8")
    wiki_index[capture.id] = output_path.relative_to(ROOT).as_posix()
    return output_path


def classify_captures(
    captures: list[RawCapture],
    *,
    dry_run: bool = False,
) -> list[Path]:
    if not captures:
        return []

    client, model = get_openai_client()
    existing_tags = collect_existing_tags()
    wiki_index = load_wiki_index()
    written: list[Path] = []
    failed_ids: list[str] = []

    for capture in captures:
        try:
            result = classify_capture_with_llm(capture, client, model, existing_tags)
            slug = make_unique_slug(result.para, result.title, capture.id)
            target = WIKI_DIR / result.para / f"{slug}.md"

            if dry_run:
                print(
                    f"[dry-run] {capture.id} -> {target.relative_to(ROOT)} "
                    f"({result.para}, tags={result.tags})"
                )
                continue

            path = write_wiki_note(capture, result, wiki_index)
            existing_tags = list(dict.fromkeys([*existing_tags, *result.tags]))
            written.append(path)
            LOGGER.info(
                "Classified %s -> %s [%s]",
                capture.id,
                path.relative_to(ROOT),
                result.para,
            )
            print(f"Classified: {path.relative_to(ROOT)}")
        except RuntimeError:
            failed_ids.append(capture.id)

    if written and not dry_run:
        write_wiki_index(wiki_index)

    if failed_ids:
        LOGGER.error("Failed to classify %d capture(s): %s", len(failed_ids), failed_ids)
        print(f"Failed to classify {len(failed_ids)} capture(s).", file=sys.stderr)

    return written


def scan_unprocessed_captures() -> list[RawCapture]:
    """Scan data/raw/ and return captures that still need classification."""
    all_captures = load_all_raw_captures()
    classified_ids = get_classified_ids()
    unprocessed = find_unprocessed_captures(all_captures, classified_ids)

    LOGGER.info(
        "Scanned %d raw capture(s); %d already classified, %d unprocessed",
        len(all_captures),
        len(classified_ids),
        len(unprocessed),
    )
    return unprocessed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify raw captures into PARA-organized wiki notes.",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Only scan for unprocessed captures; do not classify yet.",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Print LLM system/user prompts for unprocessed captures (no API call).",
    )
    parser.add_argument(
        "--capture-id",
        metavar="UUID",
        help="With --show-prompt, preview prompts for one capture id only.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Classify captures but do not write wiki files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_directories()

    unprocessed = scan_unprocessed_captures()
    count = len(unprocessed)

    if count == 0:
        LOGGER.info("0 captures to classify.")
        print("0 captures to classify.")
        return 0

    LOGGER.info("%d capture(s) to classify.", count)
    print(f"{count} capture(s) to classify.")

    if args.scan_only:
        for capture in unprocessed:
            print(f"  {capture.id}  {capture.path.name}")
        return 0

    if args.show_prompt:
        targets = unprocessed
        if args.capture_id:
            targets = [c for c in unprocessed if c.id == args.capture_id]
            if not targets:
                LOGGER.error("Capture id %s not found in unprocessed queue.", args.capture_id)
                print(f"Error: capture id {args.capture_id} not in unprocessed queue.", file=sys.stderr)
                return 1

        for capture in targets:
            print_classification_prompt(capture)
        return 0

    targets = unprocessed
    if args.capture_id:
        targets = [c for c in unprocessed if c.id == args.capture_id]
        if not targets:
            LOGGER.error("Capture id %s not found in unprocessed queue.", args.capture_id)
            print(f"Error: capture id {args.capture_id} not in unprocessed queue.", file=sys.stderr)
            return 1

    written = classify_captures(targets, dry_run=args.dry_run)
    if args.dry_run:
        print(f"[dry-run] Would classify {len(targets)} capture(s).")
        return 0

    print(f"Created {len(written)} wiki note(s).")
    return 0 if len(written) == len(targets) or not targets else 1


if __name__ == "__main__":
    raise SystemExit(main())
