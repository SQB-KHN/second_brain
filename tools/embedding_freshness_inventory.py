"""Read-only embedding index inventory. No API access and no file mutations.

This Phase 2A tool describes index shape, not freshness: legacy entries cannot
establish which note contents/model produced their vectors.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def inspect_index(index_path: Path) -> dict[str, Any]:
    """Inspect metadata only: never open notes or embedding vectors."""
    result: dict[str, Any] = {
        "index_exists": index_path.is_file(),
        "total_entries": 0,
        "legacy_unknown": 0,
        "versioned_candidate": 0,
        "invalid_entries": 0,
        "has_source_sha256": 0,
        "has_embedding_model": 0,
        "missing_vector_paths": 0,
        "schema_versions": {},
        "note_ids": [],  # populated ONLY in explicitly requested detail mode
    }
    if not index_path.is_file():
        return result
    data = json.loads(index_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Embedding index root must be a JSON object")
    versions: Counter[str] = Counter()
    for key, value in data.items():
        result["total_entries"] += 1
        if not isinstance(key, str) or not isinstance(value, dict):
            result["invalid_entries"] += 1
            continue
        if isinstance(value.get("source_sha256"), str):
            result["has_source_sha256"] += 1
        if isinstance(value.get("embedding_model"), str):
            result["has_embedding_model"] += 1
        if not isinstance(value.get("path"), str) or not value.get("path"):
            result["missing_vector_paths"] += 1
        v = value.get("schema_version")
        if isinstance(v, int) and not isinstance(v, bool) and v >= 1:
            versions[str(v)] += 1
        if (
            isinstance(v, int) and not isinstance(v, bool)
            and isinstance(value.get("source_sha256"), str)
            and isinstance(value.get("embedding_model"), str)
            and isinstance(value.get("vector_sha256"), str)
        ):
            # Fields are present; no assertion that they match current note/vector.
            result["versioned_candidate"] += 1
        else:
            result["legacy_unknown"] += 1
    result["schema_versions"] = dict(sorted(versions.items()))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True,
                        help="Path to an embedding index JSON file; never modified")
    args = parser.parse_args()
    try:
        summary = inspect_index(args.index)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Inventory failed: {exc}\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
