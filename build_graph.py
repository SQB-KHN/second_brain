#!/usr/bin/env python3
"""
SecondSelf graph builder — export graph.json from wiki notes.

Phase 4 — Graph Construction:
  4.1 Walk wiki/**/*.md, parse YAML frontmatter
  4.2 Build node list
  4.3 Extract explicit edges (frontmatter links + [[wiki-links]])
  4.4 Add semantic edges from embedding similarity
  4.5 Deduplicate edges (same source-target pair)
  4.6 Write graph.json with meta block
  4.7 Compute node degree for visualization sizing
  4.8 Handle missing/broken frontmatter gracefully (skip + log)

Usage:
  python build_graph.py --scan-only
  python build_graph.py
  python build_graph.py --no-semantic
  python build_graph.py --threshold 0.85
  ./build_graph.sh
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from config import (
    GRAPH_FILE,
    GRAPH_HTML,
    PARA_FOLDERS,
    PIPELINE_LOG,
    ROOT,
    SIMILARITY_THRESHOLD,
    WIKI_DIR,
    WIKI_INDEX_FILE,
    ensure_directories,
)

REQUIRED_FRONTMATTER_FIELDS = ("id", "para", "summary")
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")


@dataclass(frozen=True)
class GraphNote:
    """A wiki markdown note parsed for graph construction."""

    id: str
    path: Path
    frontmatter: dict[str, Any]
    body: str
    title: str
    slug: str
    para: str
    tags: list[str]
    summary: str
    source_type: str
    created: str
    links: list[str]
    embedding_id: str

    @property
    def wiki_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


@dataclass
class ScanStats:
    """Summary of a wiki scan run (Phase 4.1 / 4.8)."""

    files_found: int = 0
    loaded: int = 0
    skipped: int = 0
    duplicate_ids: int = 0
    skip_reasons: dict[str, int] = field(default_factory=dict)

    def record_skip(self, reason: str) -> None:
        self.skipped += 1
        self.skip_reasons[reason] = self.skip_reasons.get(reason, 0) + 1


@dataclass
class GraphBuildStats:
    """Summary of graph construction (Phase 4.2–4.7)."""

    node_count: int = 0
    edge_count: int = 0
    explicit_edge_count: int = 0
    semantic_edge_count: int = 0
    orphan_edges: int = 0
    duplicate_edges_skipped: int = 0


@dataclass
class GraphBuildOptions:
    include_semantic: bool = True
    similarity_threshold: float = SIMILARITY_THRESHOLD


class EdgeCollector:
    """
    Collect directed graph edges with deduplication (Phase 4.5).

    One edge per (source, target) pair. Explicit edges take precedence over
    semantic edges for the same pair.
    """

    def __init__(self, valid_ids: set[str]) -> None:
        self._valid_ids = valid_ids
        self._pairs: dict[tuple[str, str], dict[str, Any]] = {}
        self.orphan_edges = 0
        self.duplicate_edges_skipped = 0

    @property
    def edges(self) -> list[dict[str, Any]]:
        return list(self._pairs.values())

    def add_explicit(self, source_id: str, target_id: str) -> None:
        self._add(source_id, target_id, "explicit", weight=None)

    def add_semantic(self, source_id: str, target_id: str, weight: float) -> None:
        key = (source_id, target_id)
        if key in self._pairs:
            self.duplicate_edges_skipped += 1
            return
        self._add(source_id, target_id, "semantic", weight=weight)

    def _add(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        weight: float | None,
    ) -> None:
        if source_id not in self._valid_ids or target_id not in self._valid_ids:
            self.orphan_edges += 1
            return
        if source_id == target_id:
            return

        key = (source_id, target_id)
        if key in self._pairs:
            existing = self._pairs[key]
            if existing["type"] == edge_type:
                self.duplicate_edges_skipped += 1
                return
            if existing["type"] == "explicit" and edge_type == "semantic":
                self.duplicate_edges_skipped += 1
                return

        edge: dict[str, Any] = {
            "source": source_id,
            "target": target_id,
            "type": edge_type,
        }
        if weight is not None:
            edge["weight"] = round(weight, 4)
        self._pairs[key] = edge


def setup_logging() -> logging.Logger:
    """Configure pipeline logger (file + stderr)."""
    ensure_directories()
    logger = logging.getLogger("secondself.build_graph")
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


def list_wiki_markdown_files() -> list[Path]:
    """Walk data/wiki/{para}/*.md and return sorted markdown paths."""
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


def extract_title(body: str, slug: str) -> str:
    """Extract note title from first markdown heading or filename slug."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return slug.replace("-", " ").title()


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


def normalize_created(raw_created: Any) -> str:
    """Normalize created timestamp from frontmatter to ISO-8601 Z format."""
    if raw_created is None:
        return ""

    if isinstance(raw_created, datetime):
        dt = raw_created
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    value = str(raw_created).strip()
    if not value:
        return ""

    if value.endswith("Z"):
        return value
    if "+" in value or value.endswith("+00:00"):
        return value.replace("+00:00", "Z")
    return f"{value}Z" if "T" in value else value


def load_wiki_note(path: Path) -> GraphNote | None:
    """
    Load and parse one wiki markdown note.

    Returns None when frontmatter is missing, invalid, or incomplete.
    """
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        LOGGER.warning("Skipping %s: cannot read file (%s)", path, exc)
        return None

    parsed = split_frontmatter(content)
    if parsed is None:
        LOGGER.warning("%s: invalid frontmatter", path.relative_to(ROOT))
        return None

    frontmatter, body = parsed
    note_id = str(frontmatter.get("id", "")).strip()
    if not note_id:
        LOGGER.warning("%s: missing id in frontmatter", path.relative_to(ROOT))
        return None

    missing = [
        field_name
        for field_name in REQUIRED_FRONTMATTER_FIELDS
        if not str(frontmatter.get(field_name, "")).strip()
    ]
    if missing:
        LOGGER.warning(
            "%s: missing required frontmatter field(s): %s",
            path.relative_to(ROOT),
            ", ".join(missing),
        )
        return None

    slug = path.stem
    return GraphNote(
        id=note_id,
        path=path,
        frontmatter=frontmatter,
        body=body,
        title=extract_title(body, slug),
        slug=slug,
        para=str(frontmatter.get("para", "")).strip(),
        tags=normalize_tags(frontmatter.get("tags")),
        summary=str(frontmatter.get("summary", "")).strip(),
        source_type=str(frontmatter.get("source_type", "note")).strip() or "note",
        created=normalize_created(frontmatter.get("created")),
        links=normalize_links(frontmatter.get("links")),
        embedding_id=str(frontmatter.get("embedding_id", "") or "").strip(),
    )


def scan_wiki_notes() -> tuple[list[GraphNote], ScanStats]:
    """
    Walk wiki/**/*.md, parse YAML frontmatter, and return valid notes.

    Skips invalid frontmatter (EC-GRF-001), missing ids (EC-GRF-002), and
    duplicate ids (EC-GRF-003).
    """
    stats = ScanStats()
    notes: list[GraphNote] = []
    seen_ids: set[str] = set()

    files = list_wiki_markdown_files()
    stats.files_found = len(files)

    for path in files:
        note = load_wiki_note(path)
        if note is None:
            stats.record_skip("invalid_or_incomplete")
            continue

        if note.id in seen_ids:
            LOGGER.warning(
                "%s: duplicate id %s (skipping duplicate file)",
                path.relative_to(ROOT),
                note.id,
            )
            stats.duplicate_ids += 1
            stats.record_skip("duplicate_id")
            continue

        seen_ids.add(note.id)
        notes.append(note)
        stats.loaded += 1

    LOGGER.info(
        "Scanned %d wiki file(s); %d loaded, %d skipped (%d duplicate id(s))",
        stats.files_found,
        stats.loaded,
        stats.skipped,
        stats.duplicate_ids,
    )
    return notes, stats


def print_note_summary(note: GraphNote) -> None:
    print(
        f"  {note.id}  [{note.para}]  {note.title}\n"
        f"    path: {note.wiki_path}\n"
        f"    created: {note.created or '(missing)'}\n"
        f"    tags: {', '.join(note.tags) or '(none)'}\n"
        f"    links: {len(note.links)} frontmatter link(s)"
    )


def iso_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def strip_code_sections(text: str) -> str:
    """Remove fenced and inline code so [[wiki-links]] in docs are not parsed."""
    without_fenced = FENCED_CODE_PATTERN.sub("", text)
    return INLINE_CODE_PATTERN.sub("", without_fenced)


def wiki_link_targets(body: str) -> list[str]:
    """Extract [[wiki-link]] slugs from note body, excluding code blocks."""
    searchable = strip_code_sections(body)
    seen: set[str] = set()
    targets: list[str] = []
    for match in WIKI_LINK_PATTERN.finditer(searchable):
        slug = match.group(1).strip()
        if slug and slug not in seen:
            seen.add(slug)
            targets.append(slug)
    return targets


def build_slug_index(notes: list[GraphNote]) -> dict[str, str]:
    """
    Map wiki-link slugs to note ids (EC-GRF-008).

    Uses note filenames and wiki/.index.json paths as slug sources.
    """
    slug_to_id = {note.slug: note.id for note in notes}

    if WIKI_INDEX_FILE.is_file():
        try:
            index = json.loads(WIKI_INDEX_FILE.read_text(encoding="utf-8"))
            entries = index.get("entries", index)
            if isinstance(entries, dict):
                for note_id, rel_path in entries.items():
                    slug = Path(str(rel_path)).stem
                    if slug and note_id in {note.id for note in notes}:
                        slug_to_id.setdefault(slug, str(note_id))
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            LOGGER.warning("Could not load wiki index for slug resolution (%s)", exc)

    return slug_to_id


def build_nodes(notes: list[GraphNote]) -> list[dict[str, Any]]:
    """Phase 4.2 — build node list for graph.json."""
    return [
        {
            "id": note.id,
            "label": note.title,
            "para": note.para,
            "tags": note.tags,
            "summary": note.summary,
            "path": note.wiki_path,
            "created": note.created,
            "slug": note.slug,
        }
        for note in notes
    ]


def collect_explicit_edges(
    notes: list[GraphNote],
    slug_to_id: dict[str, str],
    collector: EdgeCollector,
) -> int:
    """Phase 4.3 — extract explicit edges from frontmatter links and [[wiki-links]]."""
    notes_by_id = {note.id: note for note in notes}
    added = 0

    for note in notes:
        for target_id in note.links:
            if target_id in notes_by_id:
                before = len(collector.edges)
                collector.add_explicit(note.id, target_id)
                if len(collector.edges) > before:
                    added += 1
            else:
                collector.orphan_edges += 1
                LOGGER.warning(
                    "Orphan edge: %s links to missing note %s",
                    note.wiki_path,
                    target_id,
                )

        for slug in wiki_link_targets(note.body):
            target_id = slug_to_id.get(slug)
            if target_id:
                before = len(collector.edges)
                collector.add_explicit(note.id, target_id)
                if len(collector.edges) > before:
                    added += 1
            else:
                collector.orphan_edges += 1
                LOGGER.warning(
                    "Orphan wiki-link: %s -> [[%s]] (target not found)",
                    note.wiki_path,
                    slug,
                )

    return added


def collect_semantic_edges(
    note_ids: set[str],
    collector: EdgeCollector,
    *,
    threshold: float,
) -> int:
    """Phase 4.4 — add semantic edges from embedding cosine similarity."""
    try:
        from link import compute_all_similarity_pairs, filter_pairs_by_threshold, load_embedding_vectors
    except ImportError as exc:
        LOGGER.warning("Could not import link module for semantic edges (%s)", exc)
        return 0

    vectors = load_embedding_vectors()
    graph_note_vectors = {
        note_id: vector for note_id, vector in vectors.items() if note_id in note_ids
    }

    if len(graph_note_vectors) < 2:
        LOGGER.info(
            "Semantic edges skipped: need 2+ embeddings (%d available for graph nodes).",
            len(graph_note_vectors),
        )
        return 0

    pairs = filter_pairs_by_threshold(
        compute_all_similarity_pairs(graph_note_vectors),
        threshold,
    )
    added = 0
    for pair in pairs:
        before = len(collector.edges)
        collector.add_semantic(pair.source_id, pair.target_id, pair.score)
        if len(collector.edges) > before:
            added += 1

    LOGGER.info(
        "Semantic edges: %d pair(s) above threshold %.2f, %d edge(s) added.",
        len(pairs),
        threshold,
        added,
    )
    return added


def apply_node_degrees(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
    """Phase 4.7 — compute node degree (connection count) for visualization sizing."""
    degree: dict[str, int] = {node["id"]: 0 for node in nodes}
    for edge in edges:
        degree[edge["source"]] = degree.get(edge["source"], 0) + 1
        degree[edge["target"]] = degree.get(edge["target"], 0) + 1

    for node in nodes:
        node["degree"] = degree.get(node["id"], 0)


def build_graph(
    notes: list[GraphNote],
    scan_stats: ScanStats,
    options: GraphBuildOptions | None = None,
) -> tuple[dict[str, Any], GraphBuildStats]:
    """Build graph.json payload from scanned wiki notes."""
    opts = options or GraphBuildOptions()
    note_ids = {note.id for note in notes}
    slug_to_id = build_slug_index(notes)

    nodes = build_nodes(notes)
    collector = EdgeCollector(note_ids)

    explicit_added = collect_explicit_edges(notes, slug_to_id, collector)
    semantic_added = 0
    if opts.include_semantic:
        semantic_added = collect_semantic_edges(
            note_ids,
            collector,
            threshold=opts.similarity_threshold,
        )

    edges = collector.edges
    apply_node_degrees(nodes, edges)

    explicit_count = sum(1 for edge in edges if edge["type"] == "explicit")
    semantic_count = sum(1 for edge in edges if edge["type"] == "semantic")

    build_stats = GraphBuildStats(
        node_count=len(nodes),
        edge_count=len(edges),
        explicit_edge_count=explicit_count,
        semantic_edge_count=semantic_count,
        orphan_edges=collector.orphan_edges,
        duplicate_edges_skipped=collector.duplicate_edges_skipped,
    )

    graph = {
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "generated_at": iso_timestamp(),
            "node_count": build_stats.node_count,
            "edge_count": build_stats.edge_count,
            "explicit_edge_count": build_stats.explicit_edge_count,
            "semantic_edge_count": build_stats.semantic_edge_count,
            "skipped_files": scan_stats.skipped,
            "duplicate_ids": scan_stats.duplicate_ids,
            "orphan_edges": build_stats.orphan_edges,
            "duplicate_edges_skipped": build_stats.duplicate_edges_skipped,
        },
    }

    LOGGER.info(
        "Graph assembled: %d node(s), %d edge(s) (%d explicit, %d semantic, %d orphan skipped)",
        build_stats.node_count,
        build_stats.edge_count,
        build_stats.explicit_edge_count,
        build_stats.semantic_edge_count,
        build_stats.orphan_edges,
    )
    if explicit_added or semantic_added:
        LOGGER.info(
            "Edge sources: %d explicit link(s) added, %d semantic link(s) added",
            explicit_added,
            semantic_added,
        )

    return graph, build_stats


def write_graph(graph: dict[str, Any], graph_file: Path) -> None:
    """Phase 4.6 — write graph.json atomically (EC-GRF-007)."""
    graph_file.parent.mkdir(parents=True, exist_ok=True)
    temp_path = graph_file.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    temp_path.replace(graph_file)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build graph.json from wiki notes.")
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Walk wiki/**/*.md, parse frontmatter, and print note summaries.",
    )
    parser.add_argument(
        "--graph-file",
        type=Path,
        default=GRAPH_FILE,
        help=f"Output graph file (default: {GRAPH_FILE})",
    )
    parser.add_argument(
        "--no-semantic",
        action="store_true",
        help="Skip semantic edges from embedding similarity.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=SIMILARITY_THRESHOLD,
        metavar="SCORE",
        help=f"Cosine similarity threshold for semantic edges (default: {SIMILARITY_THRESHOLD}).",
    )
    parser.add_argument(
        "--no-obsidian",
        action="store_true",
        help="Skip Obsidian vault export after building graph.json.",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip graph.html generation after building graph.json.",
    )
    parser.add_argument(
        "--html-file",
        type=Path,
        default=GRAPH_HTML,
        help=f"Output graph.html path (default: {GRAPH_HTML})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_directories()

    if args.threshold < 0 or args.threshold > 1:
        print("Error: --threshold must be between 0 and 1.", file=sys.stderr)
        return 1

    notes, scan_stats = scan_wiki_notes()

    if scan_stats.files_found == 0:
        LOGGER.info("0 wiki files found.")
        print("0 wiki files found.")

    print(
        f"{scan_stats.loaded} note(s) loaded from "
        f"{scan_stats.files_found} wiki file(s) "
        f"({scan_stats.skipped} skipped)."
    )

    if args.scan_only:
        for note in notes:
            print_note_summary(note)
        return 0

    options = GraphBuildOptions(
        include_semantic=not args.no_semantic,
        similarity_threshold=args.threshold,
    )
    graph, build_stats = build_graph(notes, scan_stats, options)
    write_graph(graph, args.graph_file)

    meta = graph["meta"]
    LOGGER.info(
        "Graph built: %d node(s), %d edge(s) -> %s",
        meta["node_count"],
        meta["edge_count"],
        args.graph_file,
    )
    print(
        f"graph.json: {meta['node_count']} node(s), "
        f"{meta['edge_count']} edge(s) "
        f"({meta['explicit_edge_count']} explicit, {meta['semantic_edge_count']} semantic) "
        f"-> {args.graph_file}"
    )

    if not args.no_obsidian:
        from export_obsidian import export_vault

        export_vault(graph_file=args.graph_file)

    if not args.no_html:
        from render_graph import write_graph_html

        html_path = write_graph_html(graph=graph, output_file=args.html_file)
        print(f"graph.html -> {html_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
