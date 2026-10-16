#!/usr/bin/env python3
"""Build a default-deny demo bundle, without importing the private pipeline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

import yaml

ROOT = Path(__file__).parent.resolve()
DEFAULT_SOURCE = ROOT / "data"
DEFAULT_DEST = ROOT / "demo"
DEFAULT_MANIFEST = ROOT / "demo-manifest.json"
PARA = {"projects", "areas", "resources", "archives"}


class PublicationError(Exception):
    """Safe to report without including source data or parser diagnostics."""


class RecoveryRequired(PublicationError):
    """The previous bundle remains on disk and must not be cleaned up."""


def checked_path(path: Path) -> Path:
    """Reject every symlink component before canonicalizing (including dangling links)."""
    path = path.absolute()
    if ".." in path.parts or any(p.is_symlink() for p in (path, *path.parents)):
        raise PublicationError("Symlink components and parent traversal are forbidden.")
    return path.resolve()


def unique_mapping(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PublicationError("Duplicate metadata key.")
        result[key] = value
    return result


class SampleLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    return unique_mapping(loader.construct_pairs(node, deep=True))


SampleLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)
IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")
WIKI_LINK = re.compile(r"\[\[([A-Za-z0-9][A-Za-z0-9_-]{0,127})\]\]")


def parse_sample(text: str, para: str) -> tuple[dict, str]:
    """Accept plain Markdown plus approved wiki links, and typed scalar metadata."""
    parts = text.split("\n---\n", 1)
    if not text.startswith("---\n") or len(parts) != 2:
        raise PublicationError("Invalid sample Markdown.")
    header, body = parts[0][4:], parts[1]
    if any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken, yaml.tokens.TagToken))
           for t in yaml.scan(header)):
        raise PublicationError("YAML aliases, anchors, and tags are unsupported.")
    meta = yaml.load(header, Loader=SampleLoader)
    allowed = {"id", "para", "summary", "links", "tags", "created"}
    if not isinstance(meta, dict) or set(meta) - allowed:
        raise PublicationError("Unsupported sample metadata field.")
    if any(not isinstance(meta.get(k), str) or not meta[k].strip() for k in ("id", "para", "summary")) or meta["para"] != para:
        raise PublicationError("Invalid sample metadata.")
    if not IDENTIFIER.fullmatch(meta["id"]):
        raise PublicationError("Invalid sample identifier.")
    for field in ("links", "tags"):
        values = meta.setdefault(field, [])
        if not isinstance(values, list) or any(not isinstance(v, str) or not IDENTIFIER.fullmatch(v) for v in values):
            raise PublicationError("Invalid sample metadata list.")
    # References are permitted only in typed links and body [[slug]] syntax.
    if re.search(r"[\[\]<>/\\:]", meta["summary"]):
        raise PublicationError("Summary must be plain prose without reference syntax.")
    if "created" in meta and (not isinstance(meta["created"], str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T[0-9:.+-]+Z?)?", meta["created"])):
        raise PublicationError("Created must be a quoted ISO date or timestamp.")
    if re.search(r"[\[\]<>]", WIKI_LINK.sub("", body)):
        raise PublicationError("Only wiki links are supported; Markdown links and HTML are forbidden.")
    return meta, body


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_bundle(source: Path, stage: Path, dest: Path, manifest: Path) -> int:
    spec = json.loads(manifest.read_text(encoding="utf-8"), object_pairs_hook=unique_mapping)
    if not isinstance(spec, dict) or set(spec) != {"version", "notes"} or type(spec["version"]) is not int or spec["version"] != 1 or not isinstance(spec["notes"], list):
        raise PublicationError("Invalid sample manifest.")
    notes = []
    seen_paths, seen_ids, seen_slugs = set(), set(), set()
    for entry in spec["notes"]:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
            raise PublicationError("Invalid sample approval.")
        if not isinstance(entry["path"], str) or not isinstance(entry["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
            raise PublicationError("Invalid sample approval types or digest.")
        rel = Path(entry["path"])
        if rel.is_absolute() or len(rel.parts) != 2 or rel.parts[0] not in PARA or rel.suffix != ".md" or rel.as_posix() != entry["path"] or not IDENTIFIER.fullmatch(rel.stem):
            raise PublicationError("Invalid sample path.")
        path = checked_path(source / "wiki" / rel)
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise PublicationError("Sample approval does not match current content.")
        meta, body = parse_sample(content.decode("utf-8"), rel.parts[0])
        if rel.as_posix() in seen_paths or meta["id"] in seen_ids or rel.stem in seen_slugs:
            raise PublicationError("Duplicate sample identity.")
        seen_paths.add(rel.as_posix())
        seen_ids.add(meta["id"])
        seen_slugs.add(rel.stem)
        target = stage / "wiki" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        notes.append((rel, meta, body))

    (stage / "wiki").mkdir(exist_ok=True)
    (stage / "embeddings").mkdir()
    write_json(stage / "embeddings" / "index.json", {})
    entries = {m["id"]: p.as_posix() for p, m, _ in notes}
    write_json(stage / "wiki" / ".index.json", {"count": len(entries), "entries": entries})
    slugs = {p.stem: m["id"] for p, m, _ in notes}
    nodes, edges = [], []
    for rel, meta, body in notes:
        links = meta["links"]
        if not isinstance(links, list) or any(not isinstance(link, str) or link not in seen_ids for link in links):
            raise PublicationError("Sample references an unapproved note.")
        targets = set(links)
        for slug in WIKI_LINK.findall(body):
            if slug not in slugs:
                raise PublicationError("Sample references an unapproved note.")
            targets.add(slugs[slug])
        title = next((line[2:].strip() for line in body.splitlines() if line.startswith("# ")), rel.stem.replace("-", " ").title())
        nodes.append({"id": meta["id"], "label": title, "para": meta["para"],
                      "summary": meta["summary"], "tags": meta.get("tags", []),
                      "created": str(meta.get("created", "")), "slug": rel.stem,
                      "path": (dest / "wiki" / rel).relative_to(ROOT).as_posix() if dest.is_relative_to(ROOT) else str(dest / "wiki" / rel)})
        edges.extend({"source": meta["id"], "target": t, "type": "explicit"} for t in sorted(targets) if t != meta["id"])
    for node in nodes:
        node["degree"] = sum(node["id"] in (e["source"], e["target"]) for e in edges)
    graph = {"nodes": nodes, "edges": edges, "meta": {"node_count": len(nodes), "edge_count": len(edges), "explicit_edge_count": len(edges), "semantic_edge_count": 0}}
    write_json(stage / "graph.json", graph)
    (stage / "README.md").write_text("# SecondSelf approved demo bundle\n\nBuilt from hash-approved Markdown only. Embeddings are intentionally absent.\n", encoding="utf-8")
    expected = {"graph.json", "README.md", "wiki/.index.json", "embeddings/index.json"} | {"wiki/" + p for p in seen_paths}
    if {p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file()} != expected:
        raise PublicationError("Unexpected bundle artifact.")
    return len(notes)


def publish(source: Path, dest: Path, manifest: Path) -> int:
    # Reject overlap before creating staging or moving any existing directory.
    source, dest, manifest = (checked_path(p) for p in (source, dest, manifest))
    checked_path(source / "wiki")
    if source == dest or source in dest.parents or dest in source.parents or dest == ROOT or dest in ROOT.parents or dest in manifest.parents:
        raise PublicationError("Unsafe publication destination.")
    if dest.exists() and not dest.is_dir():
        raise PublicationError("Destination must be a directory.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".secondself-stage-", dir=dest.parent))
    backup = temporary / "previous"
    committed = False
    try:
        stage = temporary / "bundle"
        stage.mkdir()
        count = build_bundle(source, stage, dest, manifest)
        # Establish the recovery guard before the first rename: interruption may
        # arrive after a syscall succeeded but before Python updates any flag.
        try:
            if dest.exists():
                dest.rename(backup)
            stage.rename(dest)
            committed = True
        except BaseException:
            if backup.exists() and not dest.exists():
                try:
                    backup.rename(dest)
                except BaseException:
                    raise RecoveryRequired(
                        f"Previous bundle retained at {backup}. Stop publication; follow docs/secure-demo-publication.md recovery steps."
                    ) from None
            elif backup.exists():
                raise RecoveryRequired(
                    f"Publication interrupted with output present; previous bundle retained at {backup}. Review both bundles before recovery."
                ) from None
            raise
    finally:
        # Never remove an uncommitted previous bundle, regardless of exception type.
        if committed or not backup.exists():
            shutil.rmtree(temporary)
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--skip-rebuild", action="store_true", help="Deprecated compatibility flag; the safe graph/index rebuild still runs.")
    args = parser.parse_args(argv)
    if args.skip_rebuild:
        print("--skip-rebuild is deprecated; rebuilding validated metadata for safety.", file=sys.stderr)
    try:
        count = publish(args.source, args.dest, args.manifest)
    except RecoveryRequired as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Demo publication interrupted; previous output restored if replacement had begun.", file=sys.stderr)
        return 130
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError, PublicationError):
        print("Demo publication failed; review the manifest, samples, and destination. No source content is logged.", file=sys.stderr)
        return 1
    print(f"Demo bundle ready: {count} approved note(s); no embeddings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
