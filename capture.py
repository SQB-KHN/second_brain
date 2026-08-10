#!/usr/bin/env python3
"""
SecondSelf capture CLI — store notes, links, and files in raw/.

Usage examples:
  python capture.py --text "Idea: use PARA for all captures"
  python capture.py --url "https://example.com/article"
  python capture.py --file "/path/to/document.pdf"
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "Missing dependencies. Run these commands first:\n"
        "  cd \"Second Braiin/secondself\"\n"
        "  python3 -m venv .venv\n"
        "  source .venv/bin/activate\n"
        "  pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

from config import (
    LEGACY_META_FILE,
    MAX_FILE_SIZE_MB,
    META_FILE,
    PIPELINE_LOG,
    RAW_ASSETS_DIR,
    RAW_DIR,
    ROOT,
    URL_MAX_REDIRECTS,
    URL_TIMEOUT_SECONDS,
    ensure_directories,
)

MAX_URL_BODY_CHARS = 10000
TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
    ".json",
    ".csv",
    ".html",
    ".htm",
    ".xml",
    ".py",
    ".js",
    ".ts",
    ".yaml",
    ".yml",
    ".rst",
}
SENSITIVE_PATH_PREFIXES = (
    "/etc",
    "/private/etc",
    "/usr",
    "/bin",
    "/sbin",
    "/var",
    "/System",
    "/Library/Keychains",
)
RESERVED_RAW_JSON = {"meta.json"}


def list_capture_files() -> list[Path]:
    """Return capture JSON files in data/raw/, excluding index and temp files."""
    files: list[Path] = []
    for path in sorted(RAW_DIR.glob("*.json")):
        if path.name in RESERVED_RAW_JSON or path.name.startswith("."):
            continue
        files.append(path)
    return files


def setup_logging() -> logging.Logger:
    """Configure pipeline logger (file + stderr)."""
    ensure_directories()
    logger = logging.getLogger("secondself.capture")
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


def generate_capture_id() -> str:
    return str(uuid.uuid4())


def generate_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def filename_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def write_capture(record: dict[str, Any]) -> Path:
    """Write capture JSON atomically to data/raw/{uuid}_{timestamp}.json."""
    capture_id = record["id"]
    output_path = RAW_DIR / f"{capture_id}_{filename_timestamp()}.json"
    temp_path = RAW_DIR / f".{capture_id}.tmp"
    capture_json_path = output_path.relative_to(ROOT).as_posix()

    metadata = record.setdefault("metadata", {})
    metadata["capture_file_path"] = capture_json_path

    try:
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temp_path.replace(output_path)
    except OSError as exc:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        LOGGER.error("Failed to write capture: %s", exc)
        raise

    update_meta_index(record, capture_json_path)
    return output_path


def meta_entry_from_record(
    record: dict[str, Any], capture_json_path: str
) -> dict[str, Any]:
    """Build one meta.json index entry for a capture."""
    entry: dict[str, Any] = {
        "id": record["id"],
        "type": record["type"],
        "timestamp": record["timestamp"],
        "file_path": capture_json_path,
    }
    if record.get("file_path"):
        entry["asset_file_path"] = record["file_path"]
    if record.get("source_url"):
        entry["source_url"] = record["source_url"]
    return entry


def write_meta_file(meta: dict[str, Any]) -> None:
    """Write data/meta.json atomically."""
    temp_path = META_FILE.with_suffix(".tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(meta, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        temp_path.replace(META_FILE)
    except OSError as exc:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)
        LOGGER.error("Failed to write meta.json: %s", exc)
        raise


def update_meta_index(record: dict[str, Any], capture_json_path: str) -> None:
    """Upsert a capture into data/meta.json."""
    if META_FILE.exists():
        meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    else:
        meta = {"updated_at": None, "count": 0, "captures": []}

    entry = meta_entry_from_record(record, capture_json_path)
    captures = [
        item for item in meta.get("captures", []) if item.get("id") != entry["id"]
    ]
    captures.append(entry)
    captures.sort(key=lambda item: item.get("timestamp", ""))

    meta["captures"] = captures
    meta["count"] = len(captures)
    meta["updated_at"] = generate_timestamp()
    write_meta_file(meta)
    LOGGER.info("Updated meta.json (%d captures)", meta["count"])


def rebuild_meta_from_raw() -> int:
    """Rebuild data/meta.json and backfill metadata.capture_file_path on all captures."""
    captures: list[dict[str, Any]] = []

    for path in list_capture_files():
        record = json.loads(path.read_text(encoding="utf-8"))
        capture_json_path = path.relative_to(ROOT).as_posix()

        metadata = record.setdefault("metadata", {})
        if metadata.get("capture_file_path") != capture_json_path:
            metadata["capture_file_path"] = capture_json_path
            path.write_text(
                json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        captures.append(meta_entry_from_record(record, capture_json_path))

    captures.sort(key=lambda item: item.get("timestamp", ""))
    meta = {
        "updated_at": generate_timestamp(),
        "count": len(captures),
        "captures": captures,
    }
    write_meta_file(meta)
    LOGGER.info("Rebuilt meta.json from %d raw captures", len(captures))
    return len(captures)


def ensure_meta_index() -> None:
    """Keep data/meta.json in sync with files in data/raw/."""
    capture_count = len(list_capture_files())

    if LEGACY_META_FILE.exists():
        LOGGER.warning(
            "Found legacy index at %s — rebuilding data/meta.json",
            LEGACY_META_FILE.relative_to(ROOT),
        )
        rebuild_meta_from_raw()
        LEGACY_META_FILE.unlink(missing_ok=True)
        return

    if not META_FILE.exists():
        if capture_count:
            rebuild_meta_from_raw()
        return

    try:
        meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        LOGGER.warning("data/meta.json is invalid — rebuilding from raw captures")
        rebuild_meta_from_raw()
        return

    if meta.get("count", 0) != capture_count:
        LOGGER.warning(
            "meta.json out of sync (%d indexed, %d files) — rebuilding",
            meta.get("count", 0),
            capture_count,
        )
        rebuild_meta_from_raw()


def capture_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        raise ValueError("Content cannot be empty.")

    capture_id = generate_capture_id()
    record: dict[str, Any] = {
        "id": capture_id,
        "timestamp": generate_timestamp(),
        "type": "note",
        "content": text,
        "metadata": {"content_length": len(text)},
    }
    LOGGER.info("Captured note (%d chars), id=%s", len(text), capture_id)
    return record


def fetch_url_content(url: str) -> tuple[str, dict[str, Any]]:
    """Fetch URL content; return body text and metadata."""
    metadata: dict[str, Any] = {"requested_url": url}
    try:
        response = requests.get(
            url,
            timeout=URL_TIMEOUT_SECONDS,
            allow_redirects=True,
            headers={"User-Agent": "SecondSelf/1.0 (personal capture bot)"},
        )
        metadata["final_url"] = response.url
        metadata["status_code"] = response.status_code
        metadata["content_type"] = response.headers.get("Content-Type", "")

        if response.history:
            metadata["redirect_count"] = len(response.history)
            if len(response.history) > URL_MAX_REDIRECTS:
                metadata["redirect_warning"] = (
                    f"Exceeded {URL_MAX_REDIRECTS} redirect hops"
                )

        content_type = metadata["content_type"].lower()
        body = response.text

        if "html" in content_type:
            soup = BeautifulSoup(body, "html.parser")
            title = soup.title.get_text(strip=True) if soup.title else ""
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            text = soup.get_text(separator="\n", strip=True)
            metadata["title"] = title
            if title:
                content = f"{title}\n\n{text}"
            else:
                content = text
        else:
            content = body
            metadata["non_html"] = True

        if len(content) > MAX_URL_BODY_CHARS:
            content = content[:MAX_URL_BODY_CHARS] + "\n\n[truncated]"
            metadata["truncated"] = True

        return content or url, metadata

    except requests.Timeout:
        metadata["fetch_error"] = "timeout"
        return f"[URL fetch timed out after {URL_TIMEOUT_SECONDS}s] {url}", metadata
    except requests.RequestException as exc:
        metadata["fetch_error"] = str(exc)
        return f"[URL fetch failed: {exc}] {url}", metadata


def capture_url(url: str) -> dict[str, Any]:
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must start with http:// or https://")

    capture_id = generate_capture_id()
    content, fetch_metadata = fetch_url_content(url.strip())

    record: dict[str, Any] = {
        "id": capture_id,
        "timestamp": generate_timestamp(),
        "type": "link",
        "content": content,
        "source_url": fetch_metadata.get("final_url", url.strip()),
        "metadata": fetch_metadata,
    }

    if fetch_metadata.get("fetch_error"):
        LOGGER.warning(
            "URL capture with fetch issue, id=%s url=%s error=%s",
            capture_id,
            url,
            fetch_metadata.get("fetch_error"),
        )
    else:
        LOGGER.info("Captured link, id=%s url=%s", capture_id, record["source_url"])

    return record


def is_sensitive_path(path: Path) -> bool:
    resolved = str(path.resolve())
    return any(
        resolved == prefix or resolved.startswith(prefix + "/")
        for prefix in SENSITIVE_PATH_PREFIXES
    )


def validate_file_path(file_arg: str) -> Path:
    path = Path(file_arg).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_arg}")

    resolved = path.resolve()
    if not resolved.is_file():
        raise ValueError(f"Not a file: {file_arg}")

    if is_sensitive_path(resolved):
        raise ValueError(f"Cannot capture from sensitive path: {file_arg}")

    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    size = resolved.stat().st_size
    if size > max_bytes:
        raise ValueError(
            f"File exceeds {MAX_FILE_SIZE_MB} MB limit "
            f"({size / (1024 * 1024):.1f} MB). "
            "Use --url for large files or split the document."
        )

    return resolved


def extract_pdf_text(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)

    if not pages:
        return "[PDF: no extractable text — scanned image]"

    return "\n\n".join(pages)


def extract_text_from_file(path: Path) -> tuple[str, dict[str, Any]]:
    metadata: dict[str, Any] = {
        "original_name": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size,
    }
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        try:
            text = extract_pdf_text(path)
            metadata["extraction"] = "pdf"
            return text, metadata
        except Exception as exc:
            metadata["extraction"] = "pdf_failed"
            metadata["extraction_error"] = str(exc)
            LOGGER.error("PDF extraction failed for %s: %s", path, exc)
            return f"[PDF extraction failed: {exc}]", metadata

    if suffix in TEXT_EXTENSIONS:
        try:
            text = path.read_text(encoding="utf-8")
            metadata["extraction"] = "text"
            return text, metadata
        except UnicodeDecodeError:
            text = path.read_text(encoding="latin-1")
            metadata["extraction"] = "text_latin1"
            return text, metadata

    metadata["extraction"] = "none"
    LOGGER.warning("No text extracted from %s", path.name)
    return f"[File captured: {path.name} — no text extracted]", metadata


def copy_file_to_assets(source: Path, capture_id: str) -> Path:
    dest = RAW_ASSETS_DIR / f"{capture_id}_{source.name}"
    shutil.copy2(source, dest)
    return dest


def capture_file(file_arg: str) -> dict[str, Any]:
    source = validate_file_path(file_arg)
    capture_id = generate_capture_id()

    content, extraction_metadata = extract_text_from_file(source)
    asset_path = copy_file_to_assets(source, capture_id)
    relative_path = asset_path.relative_to(ROOT).as_posix()

    record: dict[str, Any] = {
        "id": capture_id,
        "timestamp": generate_timestamp(),
        "type": "file",
        "content": content,
        "file_path": relative_path,
        "metadata": extraction_metadata,
    }

    LOGGER.info(
        "Captured file, id=%s path=%s (%d bytes)",
        capture_id,
        relative_path,
        extraction_metadata.get("size_bytes", 0),
    )
    return record


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture a note, link, or file into SecondSelf raw storage.",
        epilog=(
            "Examples:\n"
            "  python capture.py --text \"Meeting notes about PARA\"\n"
            "  python capture.py --url https://example.com\n"
            "  python capture.py --file ./document.pdf"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--text", help="Plain text note to capture")
    parser.add_argument("--url", help="URL / bookmark to capture")
    parser.add_argument("--file", dest="file_path", help="Path to file to capture")
    parser.add_argument(
        "--rebuild-meta",
        action="store_true",
        help="Rebuild data/meta.json from all captures in data/raw/",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all captures indexed in data/meta.json",
    )
    return parser.parse_args(argv)


def list_captures() -> int:
    """Print all indexed captures."""
    ensure_meta_index()
    if not META_FILE.exists():
        print("No captures yet. Use --text, --url, or --file to capture something.")
        return 0

    meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    print(f"Captures: {meta.get('count', 0)} (index: data/meta.json)")
    print(f"Storage:  {RAW_DIR.relative_to(ROOT)}/")
    print()
    for item in meta.get("captures", []):
        print(f"  [{item.get('type', '?'):4}] {item.get('id')}  {item.get('file_path')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list:
        return list_captures()

    if args.rebuild_meta:
        count = rebuild_meta_from_raw()
        if LEGACY_META_FILE.exists():
            LEGACY_META_FILE.unlink(missing_ok=True)
        print(f"Rebuilt data/meta.json ({count} captures)")
        return 0

    ensure_meta_index()

    inputs = [args.text, args.url, args.file_path]
    provided = sum(1 for value in inputs if value is not None)

    if provided == 0:
        parse_args(["--help"])
        return 1

    if provided > 1:
        LOGGER.error("Provide only one input type (--text, --url, or --file).")
        print("Error: Provide only one input type (--text, --url, or --file).", file=sys.stderr)
        return 1

    try:
        if args.text is not None:
            record = capture_text(args.text)
        elif args.url is not None:
            record = capture_url(args.url)
        else:
            record = capture_file(args.file_path)

        output_path = write_capture(record)
        print(f"Captured: {output_path}")
        print(f"ID: {record['id']}")
        print(f"Index: data/meta.json")
        print(f"File:  {record['metadata']['capture_file_path']}")
        return 0

    except (ValueError, FileNotFoundError) as exc:
        LOGGER.error("%s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        LOGGER.error("I/O error: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
