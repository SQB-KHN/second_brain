#!/usr/bin/env python3
"""
Prepare the committed demo bundle for public deployment.

Copies sanitized knowledge artifacts from data/ into demo/:
  - data/wiki/      -> demo/wiki/
  - data/embeddings -> demo/embeddings/ (if present)

Then rebuilds demo/graph.json and graph.html.

Usage:
  python prepare_deploy.py
  ./prepare_deploy.sh
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
DEFAULT_SOURCE = ROOT / "data"
DEFAULT_DEST = ROOT / "demo"

SKIP_WIKI_SLUGS = {
    "terminal-test-note",
    "test-capture-note",
    "data-folder-test-capture",
    "example-domain-information",
}


def copy_wiki_notes(source_wiki: Path, dest_wiki: Path) -> int:
    copied = 0
    for para_dir in ("projects", "areas", "resources", "archives"):
        src_para = source_wiki / para_dir
        dest_para = dest_wiki / para_dir
        dest_para.mkdir(parents=True, exist_ok=True)

        if not src_para.is_dir():
            continue

        for path in sorted(src_para.glob("*.md")):
            if path.stem in SKIP_WIKI_SLUGS:
                continue
            shutil.copy2(path, dest_para / path.name)
            copied += 1

    index_file = source_wiki / ".index.json"
    if index_file.is_file():
        index = json.loads(index_file.read_text(encoding="utf-8"))
        entries = index.get("entries", index if isinstance(index, dict) else {})
        if isinstance(entries, dict):
            filtered = {
                note_id: rel_path
                for note_id, rel_path in entries.items()
                if Path(str(rel_path)).stem not in SKIP_WIKI_SLUGS
            }
            rebuilt = {
                "updated_at": index.get("updated_at"),
                "count": len(filtered),
                "entries": filtered,
            }
            dest_wiki.mkdir(parents=True, exist_ok=True)
            dest_wiki.joinpath(".index.json").write_text(
                json.dumps(rebuilt, indent=2) + "\n",
                encoding="utf-8",
            )

    return copied


def copy_embeddings(source_emb: Path, dest_emb: Path) -> int:
    dest_emb.mkdir(parents=True, exist_ok=True)
    if not source_emb.is_dir():
        return 0

    count = 0
    for path in source_emb.iterdir():
        if path.name.startswith("."):
            continue
        if path.is_file():
            shutil.copy2(path, dest_emb / path.name)
            count += 1
    return count


def rebuild_demo_graph(dest: Path) -> tuple[int, int]:
    env = os.environ.copy()
    env["SECONDSELF_DATA_DIR"] = str(dest)
    env.pop("DEPLOY_MODE", None)

    result = subprocess.run(
        [sys.executable, "build_graph.py", "--no-obsidian"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError("build_graph.py failed while rebuilding demo graph")

    graph_file = dest / "graph.json"
    graph = json.loads(graph_file.read_text(encoding="utf-8"))
    meta = graph.get("meta", {})
    return int(meta.get("node_count", len(graph.get("nodes", [])))), int(
        meta.get("edge_count", len(graph.get("edges", [])))
    )


def write_demo_readme(dest: Path, note_count: int, embedding_files: int, nodes: int, edges: int) -> None:
    dest.joinpath("README.md").write_text(
        f"""# SecondSelf demo bundle

Public deployment data for Streamlit Cloud / Hugging Face Spaces.

- **Notes:** {note_count} wiki markdown files (sanitized sample corpus)
- **Graph:** {nodes} nodes, {edges} edges in `graph.json`
- **Embeddings:** {embedding_files} file(s) in `embeddings/`

Streamlit secrets (see `.streamlit/secrets.toml.example`):

```toml
DEPLOY_MODE = "true"
OPENAI_API_KEY = "sk-..."
```

Refresh locally: `./link.sh && python prepare_deploy.py`
""",
        encoding="utf-8",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare demo/ bundle for deployment.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument(
        "--skip-rebuild",
        action="store_true",
        help="Copy files only; do not rebuild graph.json in demo/.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source = args.source.resolve()
    dest = args.dest.resolve()

    if not (source / "wiki").is_dir():
        print(f"Error: wiki folder not found at {source / 'wiki'}", file=sys.stderr)
        return 1

    dest.mkdir(parents=True, exist_ok=True)
    note_count = copy_wiki_notes(source / "wiki", dest / "wiki")
    embedding_files = copy_embeddings(source / "embeddings", dest / "embeddings")

    nodes = edges = 0
    if not args.skip_rebuild:
        nodes, edges = rebuild_demo_graph(dest)
    elif (dest / "graph.json").is_file():
        graph = json.loads((dest / "graph.json").read_text(encoding="utf-8"))
        nodes = len(graph.get("nodes", []))
        edges = len(graph.get("edges", []))

    write_demo_readme(dest, note_count, embedding_files, nodes, edges)

    print(
        f"Demo bundle ready: {note_count} note(s), "
        f"{nodes} graph node(s), {edges} edge(s), "
        f"{embedding_files} embedding file(s)"
    )
    print(f"Output: {dest}")
    print("Deploy: set DEPLOY_MODE=true in Streamlit secrets, main file app.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
