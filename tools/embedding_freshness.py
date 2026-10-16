"""Pure, read-only freshness classification helpers for Phase 2B.

No filesystem access, network requests, or mutation. The caller provides canonical
embedding text, index metadata, model identity, and vector bytes.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

SCHEMA_VERSION = 1
HEX_256 = re.compile(r"^[0-9a-f]{64}$")


def source_fingerprint(embed_text: str) -> str:
    """Hash exactly the UTF-8 bytes handed to the embedding API.

    Normalization and exclusion of generated links remain the responsibility
    of a separately approved canonical-input builder.
    """
    return hashlib.sha256(embed_text.encode("utf-8")).hexdigest()


def vector_fingerprint(vector_bytes: bytes) -> str:
    """Fingerprint the persisted vector bytes, not its in-memory representation."""
    return hashlib.sha256(vector_bytes).hexdigest()


def classify_embedding(
    entry: Any, *, source_sha256: str, model: str,
    vector_sha256: str | None, dimensions: int | None = None
) -> str:
    """Return current, stale, missing, or legacy_unknown; fail closed.

    'current' means supplied provenance fields match; the caller must separately
    validate index-to-note identity and the actual vector bytes/dimensionality.
    """
    if entry is None:
        return "missing"
    if not isinstance(entry, dict):
        return "legacy_unknown"
    required = ("schema_version", "source_sha256", "embedding_model",
                "vector_sha256", "embedding_dimensions")
    if any(field not in entry for field in required):
        return "legacy_unknown"
    if entry["schema_version"] != SCHEMA_VERSION or type(entry["schema_version"]) is not int:
        return "legacy_unknown"
    if not all(isinstance(entry[k], str) and HEX_256.fullmatch(entry[k])
               for k in ("source_sha256", "vector_sha256")):
        return "legacy_unknown"
    if not isinstance(entry["embedding_model"], str) or not entry["embedding_model"]:
        return "legacy_unknown"
    if type(entry["embedding_dimensions"]) is not int or entry["embedding_dimensions"] <= 0:
        return "legacy_unknown"
    if (not isinstance(source_sha256, str) or not HEX_256.fullmatch(source_sha256)
            or not isinstance(model, str) or not model):
        raise ValueError("Valid current source fingerprint and model are required")
    if vector_sha256 is None:
        return "missing"
    if not isinstance(vector_sha256, str) or not HEX_256.fullmatch(vector_sha256):
        return "stale"
    if (entry["source_sha256"] != source_sha256
            or entry["embedding_model"] != model
            or entry["vector_sha256"] != vector_sha256
            or (dimensions is not None and entry["embedding_dimensions"] != dimensions)):
        return "stale"
    return "current"
