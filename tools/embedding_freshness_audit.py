"""Read-only audit of embedding freshness against source notes.

This script does not import link.py (whose vector validation may delete corrupt files).
It never calls embedding APIs, writes indexes, or changes vectors. Only counts are
printed; filenames, note bodies and source hashes stay private.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import yaml

from tools.embedding_freshness import classify_embedding, source_fingerprint, vector_fingerprint

PARAS = ("projects", "areas", "resources", "archives")


def _embed_text(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", raw, re.DOTALL)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    meta = yaml.safe_load(match.group(1))
    if not isinstance(meta, dict) or not str(meta.get("id", "")).strip():
        raise ValueError("Missing note id")
    body = raw[match.end():]
    title = str(meta.get("title") or path.stem).strip()
    summary = str(meta.get("summary") or "").strip()
    tags = meta.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    chunks = []
    if title:
        chunks.append(f"Title: {title}")
    if summary:
        chunks.append(f"Summary: {summary}")
    if tags:
        chunks.append(f"Tags: {', '.join(map(str, tags))}")
    if body.strip():
        chunks.append(body.strip())
    return str(meta["id"]), "\n\n".join(chunks).strip()


def audit(source_dir: Path, index_path: Path, model: str) -> dict[str, object]:
    """Conservative audit, no mutations. Treat identity and parse errors as unknown."""
    if not source_dir.is_dir():
        raise ValueError("Source wiki directory does not exist")
    raw_index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {}
    if not isinstance(raw_index, dict):
        raise ValueError("Index root must be an object")
    results = Counter()
    seen: set[str] = set()
    for para in PARAS:
        root = source_dir / para
        if not root.exists():
            continue
        if root.is_symlink() or not root.is_dir():
            raise ValueError("Unexpected wiki folder")
        for path in sorted(root.glob("*.md")):
            results["notes"] += 1
            if path.is_symlink():
                results["unknown"] += 1
                continue
            try:
                note_id, text = _embed_text(path)
                if note_id in seen:
                    results["unknown"] += 1
                    continue
                seen.add(note_id)
                entry = raw_index.get(note_id)
                if entry is not None and (not isinstance(entry, dict) or
                        entry.get("wiki_path") != path.relative_to(source_dir.parent.parent).as_posix()):
                    results["unknown"] += 1
                    continue
                vector_sha = None
                dims = None
                if isinstance(entry, dict) and isinstance(entry.get("path"), str):
                    # Only read the expected local path; reject untrusted index paths.
                    vector = index_path.parent / (note_id + ".npy")
                    if vector.is_file() and not vector.is_symlink():
                        content = vector.read_bytes()
                        vector_sha = vector_fingerprint(content)
                        arr = np.load(vector, allow_pickle=False)
                        if arr.ndim == 1 and arr.size > 0 and np.isfinite(arr).all():
                            dims = int(arr.size)
                        else:
                            vector_sha = None
                status = classify_embedding(entry, source_sha256=source_fingerprint(text),
                                            model=model, vector_sha256=vector_sha, dimensions=dims)
                # A match is valid only when dimension was independently verified.
                if status == "current" and dims is None:
                    status = "unknown"
            except (OSError, ValueError, yaml.YAMLError, TypeError, KeyError):
                status = "unknown"
            results[status] += 1
    results["orphan_index_entries"] = max(0, len(raw_index) - len(seen))
    return {name: results[name] for name in
            ("notes", "current", "stale", "missing", "legacy_unknown", "unknown",
             "orphan_index_entries")}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--wiki", type=Path, required=True)
    p.add_argument("--index", type=Path, required=True)
    p.add_argument("--model", required=True)
    args = p.parse_args()
    print(json.dumps(audit(args.wiki, args.index, args.model), indent=2))


if __name__ == "__main__":
    main()
