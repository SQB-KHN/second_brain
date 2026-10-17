#!/usr/bin/env python3
"""Transactional, opt-in knowledge refresh. No network access during planning."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
import fcntl
import hashlib
import io
import json
import math
import os
from pathlib import Path
import tempfile
import uuid

import numpy as np

from config import DATA_DIR, EMBEDDING_MODEL, EMBEDDING_PROVIDER, PARA_FOLDERS, ROOT, SIMILARITY_THRESHOLD
from tools.embedding_provider import model_identity, create_embedder, validate_vector
from tools.embedding_freshness import classify_embedding, source_fingerprint, vector_fingerprint
from tools.verified_vectors import select_verified_vectors


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()


def scan(data_dir):
    """Strict scan: invalid notes and duplicate/unsafe IDs block publication."""
    from link import load_wiki_note
    notes, files = [], {}
    for para in PARA_FOLDERS:
        for path in sorted((data_dir / "wiki" / para).rglob("*.md")):
            if path.is_symlink() or not path.resolve().is_relative_to(data_dir.resolve()):
                raise ValueError("Symlink or escaped note path")
            raw = path.read_bytes()
            note = load_wiki_note(path)
            if note is None:
                raise ValueError("Invalid note; repair frontmatter before refresh")
            if not note.id or note.id in (".", "..") or any(c in note.id for c in '/\\\x00'):
                raise ValueError("Unsafe note ID")
            if any(n.id == note.id for n in notes):
                raise ValueError("Duplicate note ID")
            note = replace(note, root=data_dir)
            notes.append(note)
            files[note.wiki_path] = digest(raw)
    return notes, files


def current(data_dir, reference=None):
    data_dir = Path(data_dir).resolve()
    pointer = data_dir / "knowledge" / "current.json"
    if reference is None and not pointer.exists():
        return None
    ref = reference if reference is not None else json.loads(pointer.read_text())
    name = ref["generation"]
    if not isinstance(name, str) or len(name) != 32 or any(c not in '0123456789abcdef' for c in name):
        raise ValueError("Invalid generation pointer")
    directory = pointer.parent / "generations" / name
    manifest_bytes = (directory / "manifest.json").read_bytes()
    if digest(manifest_bytes) != ref["manifest_sha256"]:
        raise ValueError("Generation manifest checksum mismatch")
    manifest = json.loads(manifest_bytes)
    for filename in ("index.json", "graph.json", "relationships.json"):
        if digest((directory / filename).read_bytes()) != manifest["checksums"][filename]:
            raise ValueError("Generation artifact checksum mismatch")
    return directory, manifest


def inventory(data_dir, model=EMBEDDING_MODEL, provider=EMBEDDING_PROVIDER):
    model = model_identity(model, provider)
    data_dir = Path(data_dir).resolve()
    notes, files = scan(data_dir)
    active = current(data_dir)
    directory = active[0] if active else data_dir / "embeddings"
    index_file = directory / "index.json"
    index = json.loads(index_file.read_text()) if index_file.exists() else {}
    if not isinstance(index, dict):
        raise ValueError("Invalid embedding index")
    # A rename with stable ID and identical canonical text can reuse a verified vector.
    aligned = {key: dict(value) if isinstance(value, dict) else value for key, value in index.items()}
    renamed = []
    for note in notes:
        entry = aligned.get(note.id)
        if isinstance(entry, dict) and entry.get("wiki_path") != note.wiki_path:
            renamed.append(note.id)
            entry["wiki_path"] = note.wiki_path
    vectors, excluded = select_verified_vectors(notes, aligned, directory, model)
    if len({v.size for v in vectors.values()}) > 1:
        raise ValueError("Inconsistent embedding dimensions; change model or recover a valid generation")
    affected = [n for n in notes if n.id not in vectors]
    legacy = [n.id for n in affected if index.get(n.id) is not None and
              classify_embedding(index[n.id], source_sha256=source_fingerprint(n.embed_text),
                                 model=model, vector_sha256=None) == 'legacy_unknown']
    plan = {"model": model, "files": files, "base": active[0].name if active else None,
            "index_sha256": digest(encoded(index)), "affected": [n.id for n in affected],
            "deleted": sorted(set(index) - {n.id for n in notes}), "renamed": renamed,
            "legacy_unknown": legacy, "excluded": excluded,
            "input_token_upper_bound": sum(len(n.embed_text.encode('utf-8')) for n in affected)}
    plan["approval_digest"] = digest(encoded(plan))
    return notes, vectors, affected, plan


def verified_active_vectors(data_dir=DATA_DIR, model=EMBEDDING_MODEL, *, provider=EMBEDDING_PROVIDER, _active=None):
    """Shared fail-closed view for Ask, Graph and the UI."""
    model = model_identity(model, provider)
    data_dir = Path(data_dir).resolve()
    active = _active if _active is not None else current(data_dir)
    if not active:
        return [], {}, {"missing_generation": 1}
    notes, files = scan(data_dir)
    directory, manifest = active
    if files != manifest["files"] or model != manifest["model"]:
        return notes, {}, {"stale_generation": 1}
    index = json.loads((directory / "index.json").read_text())
    vectors, excluded = select_verified_vectors(notes, index, directory, model)
    if excluded or set(vectors) != {n.id for n in notes} or len({v.size for v in vectors.values()}) > 1:
        return notes, {}, excluded or {"invalid_generation": 1}
    return notes, vectors, {}


def active_graph(data_dir=DATA_DIR):
    active = current(Path(data_dir))
    if not active:
        return None
    _, _, excluded = verified_active_vectors(data_dir, _active=active)
    if excluded:
        return {"nodes": [], "edges": [], "meta": {"freshness": excluded}}
    return json.loads((active[0] / "graph.json").read_text())


@contextmanager
def writer_lock(directory):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "refresh.lock").open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError("Another refresh is running") from exc
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def durable_write(path, content):
    with path.open('wb') as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def refresh(data_dir=DATA_DIR, *, model=EMBEDDING_MODEL, allow_api=False,
            approve_plan=None, price_per_million=None, max_cost=None,
            migrate_legacy=False, provider=EMBEDDING_PROVIDER, threshold=SIMILARITY_THRESHOLD, embedder=None):
    data_dir = Path(data_dir).resolve()
    if data_dir == (ROOT / 'demo').resolve() or (ROOT / 'demo').resolve() in data_dir.parents:
        raise ValueError("Refresh cannot write the published demo")
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between zero and one")
    with writer_lock(data_dir / 'knowledge'):
        notes, vectors, affected, plan = inventory(data_dir, model, provider)
        reused = set(vectors)
        old = current(data_dir)
        old_path = old[0] / 'index.json' if old else data_dir / 'embeddings/index.json'
        old_index = json.loads(old_path.read_text()) if old_path.exists() else {}
        if affected:
            if provider == 'openai':
                if not allow_api or approve_plan != plan['approval_digest']:
                    raise ValueError("External embedding requires --allow-api and --approve-plan from dry-run")
                if any(x is None or not math.isfinite(x) or x < 0 for x in (price_per_million, max_cost)):
                    raise ValueError("Supply nonnegative --price-per-million and --max-cost")
                cost = plan['input_token_upper_bound'] * price_per_million / 1_000_000
                if cost > max_cost:
                    raise ValueError("Expected upper-bound cost exceeds approved budget")
            if approve_plan is not None and approve_plan != plan['approval_digest']:
                raise ValueError("Plan changed; run dry-run again")
            if plan['legacy_unknown'] and not migrate_legacy:
                raise ValueError("Legacy vectors require --migrate-legacy; they will be re-embedded")
            if embedder is None:
                embedder = create_embedder(model, provider)
            for note in affected:
                vector = validate_vector(embedder(note.embed_text))
                vectors[note.id] = vector
        if len({v.size for v in vectors.values()}) > 1:
            raise ValueError("Embedding dimension mismatch")
        from build_graph import (EdgeCollector, collect_explicit_edges, build_nodes,
                                 apply_node_degrees)
        from link import compute_all_similarity_pairs
        collector = EdgeCollector({n.id for n in notes})
        collect_explicit_edges(notes, {n.slug: n.id for n in notes}, collector)
        relationships = []
        for pair in compute_all_similarity_pairs(vectors):
            if pair.score >= threshold:
                relationships.append({'source': pair.source_id, 'target': pair.target_id,
                                      'weight': round(pair.score, 4), 'type': 'semantic'})
                collector.add_semantic(pair.source_id, pair.target_id, pair.score)
        name = uuid.uuid4().hex
        generations = data_dir / 'knowledge' / 'generations'
        generations.mkdir(exist_ok=True)
        directory = generations / name
        directory.mkdir()
        # Unpublished generations deliberately remain recoverable on any failure.
        index = {}
        now = datetime.now(timezone.utc).isoformat()
        for note in notes:
            stream = io.BytesIO()
            np.save(stream, vectors[note.id], allow_pickle=False)
            content = stream.getvalue()
            path = directory / (note.id + '.npy')
            durable_write(path, content)
            index[note.id] = {'schema_version': 1, 'note_id': note.id,
                'wiki_path': note.wiki_path, 'path': path.name,
                'source_sha256': source_fingerprint(note.embed_text), 'embedding_model': plan['model'],
                'embedding_dimensions': int(vectors[note.id].size),
                'vector_sha256': vector_fingerprint(content),
                'generated_at': old_index[note.id].get('generated_at', now) if note.id in reused else now}
        nodes = build_nodes(notes)
        apply_node_degrees(nodes, collector.edges)
        graph = {'nodes': nodes, 'edges': collector.edges,
                 'meta': {'generation': name, 'generated_at': now, 'node_count': len(nodes),
                          'edge_count': len(collector.edges), 'freshness': 'verified'}}
        checksums = {}
        for filename, value in [('index.json', index), ('graph.json', graph), ('relationships.json', relationships)]:
            content = encoded(value)
            durable_write(directory / filename, content)
            checksums[filename] = digest(content)
        manifest = encoded({'schema_version': 1, 'model': plan['model'], 'files': plan['files'],
                            'checksums': checksums, 'previous': plan['base']})
        durable_write(directory / 'manifest.json', manifest)
        selected, excluded = select_verified_vectors(notes, index, directory, plan['model'])
        if excluded or set(selected) != set(vectors):
            raise ValueError("Staged generation failed verification")
        if scan(data_dir)[1] != plan['files']:
            raise ValueError("Notes changed during refresh; run dry-run again")
        sync_directory(directory)
        sync_directory(generations)
        fd, temporary = tempfile.mkstemp(prefix='.current-', dir=data_dir / 'knowledge')
        os.close(fd)
        try:
            durable_write(Path(temporary), encoded({'generation': name, 'manifest_sha256': digest(manifest)}))
            os.replace(temporary, data_dir / 'knowledge' / 'current.json')
            sync_directory(data_dir / 'knowledge')
        finally:
            Path(temporary).unlink(missing_ok=True)
        return graph


def restore(data_dir, generation, model=EMBEDDING_MODEL, provider=EMBEDDING_PROVIDER):
    """Activate a complete retained generation only if it matches today's notes."""
    data_dir = Path(data_dir).resolve()
    if data_dir == (ROOT / 'demo').resolve() or (ROOT / 'demo').resolve() in data_dir.parents:
        raise ValueError("Restore cannot write the published demo")
    if len(generation) != 32 or any(c not in '0123456789abcdef' for c in generation):
        raise ValueError("Invalid generation ID")
    with writer_lock(data_dir / 'knowledge'):
        directory = data_dir / 'knowledge/generations' / generation
        reference = {'generation': generation,
                     'manifest_sha256': digest((directory / 'manifest.json').read_bytes())}
        active = current(data_dir, reference)
        _, _, excluded = verified_active_vectors(data_dir, model, provider=provider, _active=active)
        if excluded:
            raise ValueError("Recovery generation does not match current notes/model/vectors")
        fd, temporary = tempfile.mkstemp(prefix='.restore-', dir=data_dir / 'knowledge')
        os.close(fd)
        try:
            durable_write(Path(temporary), encoded(reference))
            os.replace(temporary, data_dir / 'knowledge/current.json')
            sync_directory(data_dir / 'knowledge')
        finally:
            Path(temporary).unlink(missing_ok=True)
        return reference


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['status', 'dry-run', 'refresh', 'restore'])
    parser.add_argument('--data-dir', type=Path, default=DATA_DIR)
    parser.add_argument('--generation')
    parser.add_argument('--model', default=EMBEDDING_MODEL)
    parser.add_argument('--provider', choices=['ollama', 'openai'], default=EMBEDDING_PROVIDER)
    parser.add_argument('--allow-api', action='store_true')
    parser.add_argument('--approve-plan')
    parser.add_argument('--migrate-legacy', action='store_true')
    parser.add_argument('--price-per-million', type=float)
    parser.add_argument('--max-cost', type=float)
    parser.add_argument('--threshold', type=float, default=SIMILARITY_THRESHOLD)
    args = parser.parse_args(argv)
    try:
        if args.command in ('status', 'dry-run'):
            plan = inventory(args.data_dir, args.model, args.provider)[3]
            if args.price_per_million is not None:
                if not math.isfinite(args.price_per_million) or args.price_per_million < 0:
                    raise ValueError('Price must be finite and nonnegative')
                plan['expected_cost_upper_bound'] = plan['input_token_upper_bound'] * args.price_per_million / 1_000_000
            print(json.dumps(plan, indent=2))
        elif args.command == 'restore':
            if not args.generation:
                raise ValueError('Restore requires --generation')
            print(json.dumps(restore(args.data_dir, args.generation, args.model, args.provider), indent=2))
        else:
            kwargs = vars(args).copy()
            kwargs.pop('generation')
            kwargs.pop('command')
            print(json.dumps(refresh(**kwargs)['meta'], indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'Refresh blocked: {exc}', file=__import__('sys').stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
