#!/usr/bin/env python3
"""
SecondSelf link CLI — embed wiki notes and auto-link related content.

Usage examples:
  python link.py              # embed unembedded notes (tasks 3.2+)
  python link.py --scan-only  # load and list wiki notes without embedding
  python link.py --embed-only # call embedding API for unembedded notes
  python link.py --link-only  # auto-link using saved embeddings
  python link.py --threshold 0.85  # override similarity threshold
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
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
    BIDIRECTIONAL_LINKS,
    EMBEDDING_MODEL,
    EMBEDDINGS_DIR,
    EMBEDDINGS_INDEX_FILE,
    OPENAI_API_KEY,
    PARA_FOLDERS,
    PIPELINE_LOG,
    ROOT,
    SIMILARITY_THRESHOLD,
    WIKI_DIR,
    ensure_directories,
)

REQUIRED_FRONTMATTER_FIELDS = ("id", "para", "summary")
MAX_EMBED_RETRIES = 3
RELATED_SECTION_HEADER = "## Related"
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class WikiNote:
    """A wiki markdown note with parsed frontmatter and body."""

    id: str
    path: Path
    frontmatter: dict[str, Any]
    body: str
    title: str
    para: str
    tags: list[str]
    summary: str
    source_type: str
    links: list[str]
    embedding_id: str

    @property
    def wiki_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()

    @property
    def embed_text(self) -> str:
        """Text used for embedding generation (summary, tags, title, body)."""
        return build_embed_text(self)

    @property
    def has_embeddable_content(self) -> bool:
        return bool(self.embed_text.strip())


@dataclass(frozen=True)
class EmbeddingResult:
    """Embedding vector returned for one wiki note."""

    note_id: str
    vector: np.ndarray
    model: str
    dimensions: int


@dataclass(frozen=True)
class SimilarityScore:
    """Cosine similarity between two note embeddings."""

    source_id: str
    target_id: str
    score: float


@dataclass
class LinkStats:
    """Summary of an auto-linking run."""

    candidates: int = 0
    new_links: int = 0
    notes_updated: int = 0


def setup_logging() -> logging.Logger:
    """Configure pipeline logger (file + stderr)."""
    ensure_directories()
    logger = logging.getLogger("secondself.link")
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


def list_wiki_note_files() -> list[Path]:
    """Return all wiki markdown files under data/wiki/{para}/."""
    return sorted(
        path
        for para in PARA_FOLDERS
        for path in (WIKI_DIR / para).glob("*.md")
        if path.is_file()
    )


def split_frontmatter(content: str) -> tuple[dict[str, Any], str] | None:
    """Split raw markdown into YAML frontmatter dict and body text."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None

    if not isinstance(frontmatter, dict):
        return None

    body = parts[2].lstrip("\n")
    return frontmatter, body


def extract_title(body: str, path: Path) -> str:
    """Extract note title from first markdown heading or filename."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()

    slug = path.stem.replace("-", " ").strip()
    return slug.title() if slug else path.name


def normalize_tags(raw_tags: Any) -> list[str]:
    if not isinstance(raw_tags, list):
        return []

    tags: list[str] = []
    for tag in raw_tags:
        value = str(tag).strip()
        if value and value not in tags:
            tags.append(value)
    return tags


def normalize_links(raw_links: Any) -> list[str]:
    if not isinstance(raw_links, list):
        return []

    links: list[str] = []
    for link in raw_links:
        value = str(link).strip()
        if value and value not in links:
            links.append(value)
    return links


def build_embed_text(note: WikiNote) -> str:
    """
    Build the text payload for embedding.

    Uses title, summary, tags, and body. Falls back to metadata when body is empty.
    """
    sections: list[str] = []

    if note.title:
        sections.append(f"Title: {note.title}")
    if note.summary:
        sections.append(f"Summary: {note.summary}")
    if note.tags:
        sections.append(f"Tags: {', '.join(note.tags)}")
    if note.body.strip():
        sections.append(note.body.strip())

    return "\n\n".join(sections).strip()


def load_wiki_note(path: Path) -> WikiNote | None:
    """Load and validate one wiki markdown note."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        LOGGER.warning("Skipping %s: cannot read file (%s)", path, exc)
        return None

    parsed = split_frontmatter(content)
    if parsed is None:
        LOGGER.warning("Skipping %s: invalid or missing YAML frontmatter", path)
        return None

    frontmatter, body = parsed
    missing = [field for field in REQUIRED_FRONTMATTER_FIELDS if not frontmatter.get(field)]
    if missing:
        LOGGER.warning(
            "Skipping %s: missing required frontmatter field(s): %s",
            path,
            ", ".join(missing),
        )
        return None

    note_id = str(frontmatter["id"])
    title = extract_title(body, path)
    note = WikiNote(
        id=note_id,
        path=path,
        frontmatter=frontmatter,
        body=body,
        title=title,
        para=str(frontmatter.get("para", "")),
        tags=normalize_tags(frontmatter.get("tags")),
        summary=str(frontmatter.get("summary", "")).strip(),
        source_type=str(frontmatter.get("source_type", "note")),
        links=normalize_links(frontmatter.get("links")),
        embedding_id=str(frontmatter.get("embedding_id", "") or ""),
    )

    if not note.has_embeddable_content:
        LOGGER.warning(
            "Skipping %s (%s): no embeddable content (empty body, summary, and tags)",
            path.name,
            note_id,
        )
        return None

    return note


def load_all_wiki_notes() -> list[WikiNote]:
    """Load every valid wiki note from data/wiki/."""
    notes: list[WikiNote] = []
    for path in list_wiki_note_files():
        note = load_wiki_note(path)
        if note is not None:
            notes.append(note)
    return notes


def iso_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def require_embedding_api_key() -> OpenAI:
    """Embeddings require OpenAI (text-embedding-3-small)."""
    if not OPENAI_API_KEY:
        LOGGER.error("OPENAI_API_KEY is not set")
        print(
            "Set OPENAI_API_KEY in .env (embeddings require OpenAI).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return OpenAI(api_key=OPENAI_API_KEY)


def embedding_vector_path(note_id: str) -> Path:
    return EMBEDDINGS_DIR / f"{note_id}.npy"


def load_embedding_index() -> dict[str, dict[str, Any]]:
    """Load embeddings/index.json (note id -> index entry)."""
    if not EMBEDDINGS_INDEX_FILE.exists():
        return {}

    try:
        data = json.loads(EMBEDDINGS_INDEX_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        LOGGER.warning("embeddings/index.json unreadable (%s); treating as empty", exc)
        return {}

    if not isinstance(data, dict):
        return {}

    index: dict[str, dict[str, Any]] = {}
    for note_id, entry in data.items():
        if isinstance(entry, dict):
            index[str(note_id)] = entry
    return index


def write_embedding_index(index: dict[str, dict[str, Any]]) -> None:
    """Write embeddings/index.json atomically."""
    payload = dict(sorted(index.items()))
    temp_path = EMBEDDINGS_INDEX_FILE.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(EMBEDDINGS_INDEX_FILE)


def validate_embedding_file(note_id: str) -> bool:
    """Return True if the saved .npy exists and is readable."""
    path = embedding_vector_path(note_id)
    if not path.exists():
        return False

    try:
        vector = np.load(path)
        if vector.ndim != 1 or vector.size == 0:
            raise ValueError("invalid vector shape")
        return True
    except (OSError, ValueError) as exc:
        LOGGER.warning("Corrupt embedding %s (%s); will re-embed", path.name, exc)
        path.unlink(missing_ok=True)
        return False


def load_embedding_vector(note_id: str) -> np.ndarray | None:
    """Load one embedding vector from disk."""
    path = embedding_vector_path(note_id)
    if not validate_embedding_file(note_id):
        return None
    return np.load(path)


def save_embedding_vector(note_id: str, vector: np.ndarray) -> Path:
    """Save one embedding vector to data/embeddings/{id}.npy atomically."""
    output_path = embedding_vector_path(note_id)
    temp_base = EMBEDDINGS_DIR / f".{note_id}.tmp"
    temp_path = Path(f"{temp_base}.npy")

    np.save(str(temp_base), np.asarray(vector, dtype=np.float32))
    temp_path.replace(output_path)
    return output_path


def make_index_entry(note: WikiNote, vector_path: Path) -> dict[str, str]:
    """Build one embeddings/index.json entry."""
    return {
        "path": vector_path.relative_to(ROOT).as_posix(),
        "wiki_path": note.wiki_path,
        "updated": iso_timestamp(),
    }


def save_embedding(
    note: WikiNote,
    result: EmbeddingResult,
    index: dict[str, dict[str, Any]],
) -> Path:
    """Save vector file and upsert index entry for one note."""
    vector_path = save_embedding_vector(result.note_id, result.vector)
    index[note.id] = make_index_entry(note, vector_path)
    LOGGER.info("Saved embedding: %s", vector_path.relative_to(ROOT))
    return vector_path


def is_note_embedded(note_id: str, index: dict[str, dict[str, Any]] | None = None) -> bool:
    """Return True if this note already has a valid saved embedding."""
    if index is None:
        index = load_embedding_index()

    if note_id in index:
        entry = index[note_id]
        rel_path = entry.get("path", "")
        if rel_path and (ROOT / rel_path).exists():
            return validate_embedding_file(note_id)

    return validate_embedding_file(note_id)


def find_unembedded_notes(notes: list[WikiNote]) -> list[WikiNote]:
    """Return wiki notes that do not yet have embeddings."""
    index = load_embedding_index()
    unembedded = [note for note in notes if not is_note_embedded(note.id, index)]
    LOGGER.info(
        "%d note(s) to embed (%d already embedded)",
        len(unembedded),
        len(notes) - len(unembedded),
    )
    return unembedded


def embed_text(client: OpenAI, text: str) -> np.ndarray:
    """Call the embedding API and return a float32 vector."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    vector = np.asarray(response.data[0].embedding, dtype=np.float32)
    if vector.ndim != 1 or vector.size == 0:
        raise ValueError("Embedding API returned an empty vector")
    return vector


def embed_note(client: OpenAI, note: WikiNote) -> EmbeddingResult:
    """Embed one wiki note with retries on transient API failures."""
    last_error: Exception | None = None

    for attempt in range(1, MAX_EMBED_RETRIES + 1):
        try:
            vector = embed_text(client, note.embed_text)
            return EmbeddingResult(
                note_id=note.id,
                vector=vector,
                model=EMBEDDING_MODEL,
                dimensions=int(vector.size),
            )
        except (APIConnectionError, RateLimitError, APIStatusError) as exc:
            last_error = exc
            if attempt == MAX_EMBED_RETRIES:
                break
            delay = 2 ** attempt
            LOGGER.warning(
                "Embedding API error for %s (attempt %d/%d): %s; retrying in %ss",
                note.id,
                attempt,
                MAX_EMBED_RETRIES,
                exc,
                delay,
            )
            time.sleep(delay)
        except ValueError as exc:
            raise RuntimeError(f"Invalid embedding response for {note.id}: {exc}") from exc

    raise RuntimeError(
        f"Embedding API failed for {note.id} after {MAX_EMBED_RETRIES} attempts: {last_error}"
    )


def embed_unembedded_notes(notes: list[WikiNote]) -> list[EmbeddingResult]:
    """Embed and persist each unembedded note."""
    if not notes:
        LOGGER.info("0 notes to embed.")
        print("0 notes to embed.")
        return []

    client = require_embedding_api_key()
    index = load_embedding_index()
    results: list[EmbeddingResult] = []
    failed_ids: list[str] = []

    LOGGER.info("Embedding %d note(s) with %s", len(notes), EMBEDDING_MODEL)
    print(f"Embedding {len(notes)} note(s) with {EMBEDDING_MODEL}...")

    for note in notes:
        try:
            result = embed_note(client, note)
            vector_path = save_embedding(note, result, index)
            results.append(result)
            LOGGER.info(
                "Embedded %s (%s) -> %d dimensions, saved %s",
                note.id,
                note.title,
                result.dimensions,
                vector_path.relative_to(ROOT),
            )
            print(
                f"  Saved: {note.id}  {note.title}  "
                f"({result.dimensions} dims) -> {vector_path.relative_to(ROOT)}"
            )
        except (RuntimeError, OSError) as exc:
            LOGGER.error("%s", exc)
            failed_ids.append(note.id)
            print(f"  Failed:   {note.id}  {note.title}", file=sys.stderr)

    if results:
        write_embedding_index(index)
        LOGGER.info("Updated %s (%d entries)", EMBEDDINGS_INDEX_FILE.relative_to(ROOT), len(index))

    if failed_ids:
        LOGGER.error("Failed to embed %d note(s): %s", len(failed_ids), failed_ids)
        print(f"Failed to embed {len(failed_ids)} note(s).", file=sys.stderr)

    print(f"Saved {len(results)} embedding(s) to {EMBEDDINGS_DIR.relative_to(ROOT)}/")
    return results


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    left = np.asarray(a, dtype=np.float32)
    right = np.asarray(b, dtype=np.float32)
    if left.shape != right.shape:
        raise ValueError(f"Vector shape mismatch: {left.shape} vs {right.shape}")

    denominator = float(np.linalg.norm(left) * np.linalg.norm(right))
    if denominator == 0.0:
        return 0.0
    return float(np.dot(left, right) / denominator)


def cosine_similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """Compute pairwise cosine similarity for a row-wise matrix (n x d)."""
    matrix = np.asarray(vectors, dtype=np.float32)
    if matrix.ndim != 2:
        raise ValueError(f"Expected 2D matrix, got shape {matrix.shape}")

    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized = matrix / norms
    return normalized @ normalized.T


def load_embedding_vectors(
    index: dict[str, dict[str, Any]] | None = None,
) -> dict[str, np.ndarray]:
    """Load all valid embedding vectors keyed by note id."""
    if index is None:
        index = load_embedding_index()

    vectors: dict[str, np.ndarray] = {}
    for note_id in sorted(index):
        vector = load_embedding_vector(note_id)
        if vector is not None:
            vectors[note_id] = np.asarray(vector, dtype=np.float32)
    return vectors


def _validate_vector_dimensions(vectors: dict[str, np.ndarray]) -> int:
    """Ensure all vectors share the same dimensionality."""
    if not vectors:
        return 0

    dimensions = {vector.shape[0] for vector in vectors.values()}
    if len(dimensions) != 1:
        raise ValueError(f"Embedding dimension mismatch: {sorted(dimensions)}")
    return next(iter(dimensions))


def compute_all_similarity_pairs(
    vectors: dict[str, np.ndarray],
    *,
    exclude_self: bool = True,
) -> list[SimilarityScore]:
    """Compute cosine similarity for all note pairs."""
    note_ids = sorted(vectors.keys())
    if len(note_ids) < 2:
        return []

    _validate_vector_dimensions(vectors)
    matrix = np.stack([vectors[note_id] for note_id in note_ids])
    similarity = cosine_similarity_matrix(matrix)

    pairs: list[SimilarityScore] = []
    for row, source_id in enumerate(note_ids):
        for col, target_id in enumerate(note_ids):
            if exclude_self and row == col:
                continue
            pairs.append(
                SimilarityScore(
                    source_id=source_id,
                    target_id=target_id,
                    score=float(similarity[row, col]),
                )
            )
    return pairs


def compute_similarities_for_note(
    note_id: str,
    vectors: dict[str, np.ndarray],
    *,
    exclude_self: bool = True,
) -> list[SimilarityScore]:
    """Compute cosine similarity between one note and all others."""
    if note_id not in vectors:
        raise KeyError(f"No embedding found for note id {note_id}")

    source = vectors[note_id]
    pairs: list[SimilarityScore] = []
    for target_id, target in vectors.items():
        if exclude_self and target_id == note_id:
            continue
        pairs.append(
            SimilarityScore(
                source_id=note_id,
                target_id=target_id,
                score=cosine_similarity(source, target),
            )
        )
    pairs.sort(key=lambda item: item.score, reverse=True)
    return pairs


def filter_pairs_by_threshold(
    pairs: list[SimilarityScore],
    threshold: float,
) -> list[SimilarityScore]:
    """Return pairs with cosine similarity at or above the threshold."""
    return [pair for pair in pairs if pair.score >= threshold]


def build_note_lookup(notes: list[WikiNote]) -> dict[str, WikiNote]:
    return {note.id: note for note in notes}


def wiki_link_slug(note: WikiNote) -> str:
    """Return the wiki-link slug for a note (filename without .md)."""
    return note.path.stem


def existing_wiki_link_slugs(body: str) -> set[str]:
    return {match.group(1).strip() for match in WIKI_LINK_PATTERN.finditer(body)}


def append_related_links(body: str, slugs: list[str]) -> tuple[str, list[str]]:
    """Append [[wiki-links]] to the Related section; return updated body and added slugs."""
    existing = existing_wiki_link_slugs(body)
    to_add = [slug for slug in slugs if slug and slug not in existing]
    if not to_add:
        return body, []

    link_lines = [f"- [[{slug}]]" for slug in to_add]
    if RELATED_SECTION_HEADER in body:
        updated = body.rstrip() + "\n" + "\n".join(link_lines) + "\n"
        return updated, to_add

    section = "\n".join([RELATED_SECTION_HEADER, ""] + link_lines) + "\n"
    updated = body.rstrip() + "\n\n" + section
    return updated, to_add


def render_wiki_file(frontmatter: dict[str, Any], body: str) -> str:
    yaml_block = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{yaml_block}\n---\n\n{body.rstrip()}\n"


def write_wiki_note_file(path: Path, frontmatter: dict[str, Any], body: str) -> None:
    """Write a wiki markdown file atomically."""
    temp_path = path.with_suffix(".tmp")
    temp_path.write_text(render_wiki_file(frontmatter, body), encoding="utf-8")
    temp_path.replace(path)


def merge_frontmatter_links(existing: list[str], new_ids: list[str]) -> list[str]:
    """Append new link ids without duplicates."""
    merged = list(existing)
    for note_id in new_ids:
        if note_id not in merged:
            merged.append(note_id)
    return merged


def add_links_to_note(
    note: WikiNote,
    targets: list[WikiNote],
) -> bool:
    """
    Add target note ids to frontmatter links and Related wiki-links.

    Never removes existing links (EC-LNK-009).
    """
    if not targets:
        return False

    new_ids = [target.id for target in targets if target.id not in note.links]
    new_slugs = [wiki_link_slug(target) for target in targets if target.id not in note.links]
    updated_body, added_slugs = append_related_links(note.body, new_slugs)

    if not new_ids and not added_slugs:
        return False

    frontmatter = dict(note.frontmatter)
    frontmatter["links"] = merge_frontmatter_links(note.links, new_ids)
    write_wiki_note_file(note.path, frontmatter, updated_body)
    return True


def find_link_candidates(
    vectors: dict[str, np.ndarray],
    threshold: float,
) -> list[SimilarityScore]:
    """Find all note pairs above the similarity threshold."""
    pairs = compute_all_similarity_pairs(vectors)
    return filter_pairs_by_threshold(pairs, threshold)


def apply_auto_links(
    notes: list[WikiNote],
    vectors: dict[str, np.ndarray],
    *,
    threshold: float = SIMILARITY_THRESHOLD,
    bidirectional: bool = BIDIRECTIONAL_LINKS,
) -> LinkStats:
    """Apply semantic links to wiki notes for pairs above threshold."""
    stats = LinkStats()
    if len(vectors) < 2:
        LOGGER.info("Need at least 2 embeddings to create links.")
        return stats

    note_lookup = {
        note.id: note for note in notes if note.id in vectors
    }
    candidates = find_link_candidates(vectors, threshold)
    stats.candidates = len(candidates)

    if not candidates:
        LOGGER.info("0 new links above threshold %.2f.", threshold)
        print(f"0 new links above threshold {threshold:.2f}.")
        return stats

    updated_ids: set[str] = set()

    for pair in sorted(candidates, key=lambda item: item.score, reverse=True):
        source = note_lookup.get(pair.source_id)
        target = note_lookup.get(pair.target_id)
        if source is None or target is None:
            continue

        if add_links_to_note(source, [target]):
            stats.new_links += 1
            updated_ids.add(source.id)
            LOGGER.info(
                "New link: %s -> %s (score=%.4f)",
                source.id,
                target.id,
                pair.score,
            )
            reloaded = load_wiki_note(source.path)
            if reloaded is not None:
                note_lookup[source.id] = reloaded

        if bidirectional:
            target = note_lookup.get(pair.target_id)
            source = note_lookup.get(pair.source_id)
            if target is None or source is None:
                continue
            if add_links_to_note(target, [source]):
                stats.new_links += 1
                updated_ids.add(target.id)
                LOGGER.info(
                    "New link: %s -> %s (score=%.4f, bidirectional)",
                    target.id,
                    source.id,
                    pair.score,
                )
                reloaded = load_wiki_note(target.path)
                if reloaded is not None:
                    note_lookup[target.id] = reloaded

    stats.notes_updated = len(updated_ids)
    LOGGER.info(
        "Auto-link complete: %d candidate pair(s), %d new link(s), %d note(s) updated",
        stats.candidates,
        stats.new_links,
        stats.notes_updated,
    )
    print(
        f"Created {stats.new_links} new link(s) across {stats.notes_updated} note(s) "
        f"(threshold={threshold:.2f})."
    )
    return stats


def print_similarity_summary(
    vectors: dict[str, np.ndarray],
    *,
    note_id: str | None = None,
    top_k: int = 5,
) -> None:
    """Print similarity results for inspection (task 3.4)."""
    if len(vectors) < 2:
        print("Need at least 2 embeddings to compute similarity.")
        return

    dimension = _validate_vector_dimensions(vectors)
    print(f"Loaded {len(vectors)} embedding(s) ({dimension} dimensions each).")

    if note_id:
        pairs = filter_pairs_by_threshold(
            compute_similarities_for_note(note_id, vectors),
            SIMILARITY_THRESHOLD,
        )
        print(
            f"\nTop {min(top_k, len(pairs))} similar to {note_id} "
            f"(threshold>={SIMILARITY_THRESHOLD}):"
        )
        for pair in pairs[:top_k]:
            print(f"  {pair.target_id}  score={pair.score:.4f}")
        return

    pairs = filter_pairs_by_threshold(compute_all_similarity_pairs(vectors), SIMILARITY_THRESHOLD)
    pairs.sort(key=lambda item: item.score, reverse=True)
    print(
        f"Computed {len(pairs)} pair(s) above threshold {SIMILARITY_THRESHOLD} "
        f"(from {len(vectors)} embeddings)."
    )
    print(f"\nTop {min(top_k, len(pairs))} pairs:")
    for pair in pairs[:top_k]:
        print(f"  {pair.source_id} -> {pair.target_id}  score={pair.score:.4f}")


def scan_wiki_notes() -> list[WikiNote]:
    """Load wiki notes and log scan summary."""
    files = list_wiki_note_files()
    notes = load_all_wiki_notes()
    skipped = len(files) - len(notes)

    LOGGER.info(
        "Scanned %d wiki file(s); %d loaded, %d skipped",
        len(files),
        len(notes),
        skipped,
    )
    return notes


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Embed wiki notes and auto-link related content.",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Load wiki notes and print a summary without embedding or linking.",
    )
    parser.add_argument(
        "--note-id",
        metavar="UUID",
        help="Limit to one note id (scan or embed).",
    )
    parser.add_argument(
        "--embed-only",
        action="store_true",
        help="Call embedding API for unembedded notes (no linking yet).",
    )
    parser.add_argument(
        "--similarity-only",
        action="store_true",
        help="Compute and print cosine similarities between saved embeddings.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        metavar="N",
        help="With --similarity-only, number of top matches to show (default: 5).",
    )
    parser.add_argument(
        "--link-only",
        action="store_true",
        help="Auto-link notes using saved embeddings (skip embedding API).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=SIMILARITY_THRESHOLD,
        metavar="SCORE",
        help=f"Cosine similarity threshold for auto-links (default: {SIMILARITY_THRESHOLD}).",
    )
    parser.add_argument(
        "--no-bidirectional",
        action="store_true",
        help="Disable bidirectional linking (default: enabled).",
    )
    parser.add_argument(
        "--no-obsidian",
        action="store_true",
        help="Skip Obsidian vault export after linking.",
    )
    return parser.parse_args(argv)


def print_note_summary(note: WikiNote) -> None:
    body_chars = len(note.body)
    embed_chars = len(note.embed_text)
    print(
        f"  {note.id}  [{note.para}]  {note.title}\n"
        f"    path: {note.wiki_path}\n"
        f"    tags: {', '.join(note.tags) or '(none)'}\n"
        f"    body: {body_chars} chars | embed_text: {embed_chars} chars"
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_directories()

    notes = scan_wiki_notes()
    count = len(notes)

    if count == 0:
        LOGGER.info("0 notes to process.")
        print("0 notes to process.")
        return 0

    LOGGER.info("%d note(s) loaded.", count)
    print(f"{count} note(s) loaded.")

    if args.scan_only:
        targets = notes
        if args.note_id:
            targets = [note for note in notes if note.id == args.note_id]
            if not targets:
                LOGGER.error("Note id %s not found in loaded wiki notes.", args.note_id)
                print(f"Error: note id {args.note_id} not found.", file=sys.stderr)
                return 1

        for note in targets:
            print_note_summary(note)
        return 0

    if args.similarity_only:
        vectors = load_embedding_vectors()
        if not vectors:
            LOGGER.error("No saved embeddings found. Run link.py --embed-only first.")
            print("No saved embeddings found. Run ./link.sh --embed-only first.", file=sys.stderr)
            return 1

        note_id = args.note_id
        if note_id and note_id not in vectors:
            LOGGER.error("Note id %s has no saved embedding.", note_id)
            print(f"Error: note id {note_id} has no saved embedding.", file=sys.stderr)
            return 1

        print_similarity_summary(vectors, note_id=note_id, top_k=max(1, args.top_k))
        return 0

    threshold = args.threshold
    if threshold < 0 or threshold > 1:
        print("Error: --threshold must be between 0 and 1.", file=sys.stderr)
        return 1

    bidirectional = BIDIRECTIONAL_LINKS and not args.no_bidirectional

    targets = notes
    if args.note_id:
        targets = [note for note in notes if note.id == args.note_id]
        if not targets:
            LOGGER.error("Note id %s not found in loaded wiki notes.", args.note_id)
            print(f"Error: note id {args.note_id} not found.", file=sys.stderr)
            return 1

    if not args.link_only:
        unembedded = find_unembedded_notes(targets)
        if unembedded:
            results = embed_unembedded_notes(unembedded)
            if not results:
                return 1
            if args.embed_only:
                return 0 if len(results) == len(unembedded) else 1
        else:
            print("0 notes to embed.")

    if args.embed_only:
        return 0

    vectors = load_embedding_vectors()
    if len(vectors) < 2:
        if vectors:
            print("Only 1 embedding saved; need 2+ for linking.")
        else:
            LOGGER.error("No saved embeddings found. Run link.py without --link-only first.")
            print("No saved embeddings found.", file=sys.stderr)
        return 1

    apply_auto_links(
        notes,
        vectors,
        threshold=threshold,
        bidirectional=bidirectional,
    )

    if not args.no_obsidian:
        from export_obsidian import export_vault

        export_vault()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
