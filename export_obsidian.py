#!/usr/bin/env python3
"""
Export SecondSelf wiki notes to an Obsidian vault.

Regenerated automatically after link.py and build_graph.py, or run standalone:

  python export_obsidian.py
  ./export_obsidian.sh
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from config import (
    GRAPH_FILE,
    OBSIDIAN_VAULT_DIR,
    PARA_COLORS,
    PARA_FOLDERS,
    PIPELINE_LOG,
    ROOT,
    WIKI_DIR,
    ensure_directories,
)

WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
REQUIRED_FRONTMATTER_FIELDS = ("id", "para", "summary")
SKIP_TAG_LINKS = {"test-capture", "data-folder", "example-domain", "documentation"}
HUB_NOTE_NAME = "SecondSelf Knowledge Graph.md"


@dataclass(frozen=True)
class ExportNote:
    id: str
    slug: str
    title: str
    para: str
    tags: list[str]
    summary: str
    body: str
    links: list[str]
    path: Path


@dataclass
class ExportStats:
    note_count: int = 0
    edge_count: int = 0
    vault_dir: Path = OBSIDIAN_VAULT_DIR


def setup_logging() -> logging.Logger:
    ensure_directories()
    logger = logging.getLogger("secondself.export_obsidian")
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


def split_frontmatter(content: str) -> tuple[dict[str, Any], str] | None:
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

    return frontmatter, parts[2].lstrip("\n")


def extract_title(body: str, slug: str) -> str:
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


def list_wiki_note_files() -> list[Path]:
    return sorted(
        path
        for para in PARA_FOLDERS
        for path in (WIKI_DIR / para).glob("*.md")
        if path.is_file()
    )


def load_export_note(path: Path) -> ExportNote | None:
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

    slug = path.stem
    return ExportNote(
        id=str(frontmatter["id"]),
        slug=slug,
        title=extract_title(body, slug),
        para=str(frontmatter.get("para", "")),
        tags=normalize_tags(frontmatter.get("tags")),
        summary=str(frontmatter.get("summary", "")).strip(),
        body=body,
        links=normalize_links(frontmatter.get("links")),
        path=path,
    )


def load_export_notes() -> list[ExportNote]:
    notes: list[ExportNote] = []
    for path in list_wiki_note_files():
        note = load_export_note(path)
        if note is not None:
            notes.append(note)
    return notes


def wiki_link_targets(body: str) -> list[str]:
    seen: set[str] = set()
    targets: list[str] = []
    for match in WIKI_LINK_PATTERN.finditer(body):
        slug = match.group(1).strip()
        if slug and slug not in seen:
            seen.add(slug)
            targets.append(slug)
    return targets


def tag_related_slugs(note: ExportNote, notes_by_slug: dict[str, ExportNote]) -> list[str]:
    related: set[str] = set()
    for tag in note.tags:
        if tag in SKIP_TAG_LINKS:
            continue
        for other in notes_by_slug.values():
            if other.slug == note.slug:
                continue
            if tag in other.tags:
                related.add(other.slug)
    return sorted(related)


def build_edges(
    notes: list[ExportNote],
    graph_file: Path | None = None,
) -> list[tuple[str, str]]:
    """Return directed edges as (source_slug, target_slug) pairs."""
    notes_by_id = {note.id: note for note in notes}
    notes_by_slug = {note.slug: note for note in notes}
    edges: set[tuple[str, str]] = set()

    if graph_file and graph_file.is_file():
        try:
            graph = json.loads(graph_file.read_text(encoding="utf-8"))
            for edge in graph.get("edges", []):
                source = notes_by_id.get(str(edge.get("source", "")))
                target = notes_by_id.get(str(edge.get("target", "")))
                if source and target:
                    edges.add((source.slug, target.slug))
            if edges:
                return sorted(edges)
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            LOGGER.warning("Could not load %s for Obsidian export (%s)", graph_file, exc)

    for note in notes:
        for target_id in note.links:
            target = notes_by_id.get(target_id)
            if target:
                edges.add((note.slug, target.slug))

        for slug in wiki_link_targets(note.body):
            if slug in notes_by_slug and slug != note.slug:
                edges.add((note.slug, slug))

        for slug in tag_related_slugs(note, notes_by_slug):
            edges.add((note.slug, slug))

    return sorted(edges)


def mermaid_node_id(slug: str) -> str:
    node_id = re.sub(r"[^a-zA-Z0-9]", "", slug)[:24] or "node"
    if node_id[0].isdigit():
        node_id = f"n{node_id}"
    return node_id


def render_hub_note(notes: list[ExportNote], edges: list[tuple[str, str]]) -> str:
    notes_by_slug = {note.slug: note for note in notes}
    node_ids = {note.slug: mermaid_node_id(note.slug) for note in notes}

    mermaid_nodes = [
        f'    {node_ids[note.slug]}["{note.title}"]' for note in notes
    ]
    mermaid_edges = [
        f"    {node_ids[src]} --> {node_ids[tgt]}"
        for src, tgt in edges
        if src in node_ids and tgt in node_ids
    ]

    hub = f"""---
tags:
  - secondself
  - graph
  - hub
---

# SecondSelf Knowledge Graph

Open **Graph view** (`Cmd/Ctrl + G`) to explore connections.

## PARA legend

| Category | Color | Folder |
|----------|-------|--------|
| Projects | green | `projects/` |
| Areas | blue | `areas/` |
| Resources | orange | `resources/` |
| Archives | gray | `archives/` |

## Note graph ({len(notes)} notes, {len(edges)} links)

```mermaid
flowchart LR
    classDef projects fill:#22c55e22,stroke:#22c55e,color:#14532d
    classDef areas fill:#3b82f622,stroke:#3b82f6,color:#1e3a8a
    classDef resources fill:#f9731622,stroke:#f97316,color:#7c2d12
    classDef archives fill:#9ca3af22,stroke:#9ca3af,color:#374151

{chr(10).join(mermaid_nodes)}

{chr(10).join(mermaid_edges)}
"""

    for note in notes:
        para_class = note.para if note.para in PARA_COLORS else "resources"
        hub += f"    class {node_ids[note.slug]} {para_class}\n"

    hub += """```

## Pipeline architecture

```mermaid
flowchart TD
    A[User Input] --> B[capture.py]
    B --> C[raw/]
    C --> D[classify.py]
    D --> E[wiki/ PARA folders]
    E --> F[link.py]
    F --> G[embeddings/]
    F --> H[Wiki links]
    H --> I[build_graph.py]
    G --> I
    I --> J[graph.json]
    J --> K[Graph UI]
    G --> L[ask.py]
    E --> L
    L --> M[RAG Answer]
    K --> N[Streamlit app]
    M --> N
    I --> O[export_obsidian.py]
    F --> O
    O --> P[Obsidian vault]
```

## All notes

"""

    for para in PARA_FOLDERS:
        para_notes = [note for note in notes if note.para == para]
        if not para_notes:
            continue
        hub += f"\n### {para.title()}\n\n"
        for note in sorted(para_notes, key=lambda item: item.title):
            hub += f"- [[{note.slug}]] — {note.summary}\n"

    return hub


def render_obsidian_note(note: ExportNote) -> str:
    tag_line = " ".join(f"#{tag}" for tag in note.tags)
    yaml_block = yaml.safe_dump(
        {
            "para": note.para,
            "summary": note.summary,
            "id": note.id,
            "tags": note.tags,
        },
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    header = (
        f"---\n{yaml_block}\n---\n\n"
        f"# {note.title}\n\n"
        f"> {note.summary}\n\n"
    )
    if tag_line:
        header += f"{tag_line}\n\n"
    return header + note.body.rstrip() + "\n"


def write_vault_note(vault_dir: Path, note: ExportNote) -> None:
    para_dir = vault_dir / note.para
    para_dir.mkdir(parents=True, exist_ok=True)
    out_path = para_dir / f"{note.slug}.md"
    out_path.write_text(render_obsidian_note(note), encoding="utf-8")


def export_vault(
    vault_dir: Path | None = None,
    graph_file: Path | None = None,
) -> ExportStats:
    """Export wiki notes to an Obsidian vault and return summary stats."""
    target_dir = (vault_dir or OBSIDIAN_VAULT_DIR).resolve()
    graph_path = graph_file or GRAPH_FILE

    notes = load_export_notes()
    edges = build_edges(notes, graph_path)

    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True)

    for note in notes:
        write_vault_note(target_dir, note)

    hub_path = target_dir / HUB_NOTE_NAME
    hub_path.write_text(render_hub_note(notes, edges), encoding="utf-8")

    stats = ExportStats(
        note_count=len(notes),
        edge_count=len(edges),
        vault_dir=target_dir,
    )
    LOGGER.info(
        "Obsidian vault exported: %d note(s), %d link(s) -> %s",
        stats.note_count,
        stats.edge_count,
        stats.vault_dir,
    )
    print(
        f"Obsidian vault: {stats.note_count} note(s), {stats.edge_count} link(s) "
        f"-> {stats.vault_dir}"
    )
    return stats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export SecondSelf wiki notes to an Obsidian vault.",
    )
    parser.add_argument(
        "--vault-dir",
        type=Path,
        default=OBSIDIAN_VAULT_DIR,
        help=f"Output vault directory (default: {OBSIDIAN_VAULT_DIR})",
    )
    parser.add_argument(
        "--graph-file",
        type=Path,
        default=GRAPH_FILE,
        help=f"Optional graph.json for edge data (default: {GRAPH_FILE})",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ensure_directories()
    stats = export_vault(vault_dir=args.vault_dir, graph_file=args.graph_file)
    return 0 if stats.note_count >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
