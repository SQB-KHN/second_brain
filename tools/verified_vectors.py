"""Read-only selection of verified embedding vectors for future Ask/Graph integration.

Legacy vectors are excluded; never delete, overwrite, migrate or regenerate data.
This module does not import link.py because its legacy validation can unlink files.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Iterable
import numpy as np

from tools.embedding_freshness import (
    classify_embedding, source_fingerprint, vector_fingerprint,
)


def select_verified_vectors(
    notes: Iterable[Any],
    index: dict[str, Any],
    vector_dir: Path,
    model: str,
) -> tuple[dict[str, np.ndarray], dict[str, int]]:
    """Verify exact embed_text, note identity, stored bytes and dimensions.

    Note objects must expose id, embed_text and wiki_path, matching link.WikiNote.
    Untrusted paths in the index are never followed: files are found by note id
    only, and note IDs with path separators are refused.
    """
    selected: dict[str, np.ndarray] = {}
    counts: Counter[str] = Counter()
    seen: set[str] = set()
    for note in notes:
        note_id = str(note.id)
        if note_id in seen or not note_id or note_id in (".", "..") or (
            "/" in note_id or "\\" in note_id
        ):
            counts["unknown"] += 1
            continue
        seen.add(note_id)
        entry = index.get(note_id)
        if entry is not None and (
            not isinstance(entry, dict)
            or entry.get("wiki_path") != str(note.wiki_path)
            or entry.get("path") not in (
                (vector_dir / (note_id + ".npy")).as_posix(),
                (Path("data") / "embeddings" / (note_id + ".npy")).as_posix(),
            )
        ):
            counts["unknown"] += 1
            continue
        path = vector_dir / (note_id + ".npy")
        digest = None
        vector = None
        dimensions = None
        if path.is_file() and not path.is_symlink():
            try:
                content = path.read_bytes()
                digest = vector_fingerprint(content)
                with path.open("rb") as stream:
                    candidate = np.load(stream, allow_pickle=False)
                if (candidate.ndim == 1 and candidate.size > 0
                        and np.issubdtype(candidate.dtype, np.number)
                        and np.isfinite(candidate).all()):
                    vector = candidate
                    dimensions = int(candidate.size)
                else:
                    digest = None
            except (OSError, ValueError, TypeError):
                digest = None
        status = classify_embedding(
            entry, source_sha256=source_fingerprint(str(note.embed_text)),
            model=model, vector_sha256=digest, dimensions=dimensions,
        )
        if status == "current" and vector is not None:
            selected[note_id] = np.asarray(vector, dtype=np.float32)
        else:
            counts[status if status != "current" else "unknown"] += 1
    return selected, dict(counts)
