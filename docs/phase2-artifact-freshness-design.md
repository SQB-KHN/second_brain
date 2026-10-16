# Phase 2 — Embedding freshness and knowledge consistency

Status: **Implemented on phase2-functional-integration.** See [operations](phase2-operations.md) for the final contract and recovery commands. The remainder records the original proposal. Phase 1 secure demo publication is already merged. This phase must not modify or publish `demo/`, private notes, or existing embedding artifacts as part of development tests.

## Problem and current evidence

- `link.py` checks whether an embedding file is present and readable before deciding a note is embedded; it does not verify that the current canonical note text and model match the stored vector.
- `link.py` appends automatically generated related links into Markdown; it cannot safely distinguish all old generated relationships from author-maintained relationships.
- `ask.py` uses saved embedding vectors directly for retrieval, whereas `build_graph.py` derives graph relationships separately. Their freshness can diverge.
- The project stores editable Markdown on disk and currently targets a personal knowledge owner. Avoid adding SQLite or a worker queue until measurements or reliability requirements justify them.

## Proposed contract

1. Define canonical embedding input as a deterministic function of manually authored note content and relevant metadata. Do not include generated related-link sections or generated link fields. Document encoding, whitespace normalization, and schema version before migration.
2. Each embedding index entry includes `schema_version`, `note_id`, `source_sha256`, `embedding_model`, `embedding_dimensions`, `vector_sha256`, and `generated_at`. Verify source and vector identity before reusing an entry.
3. Explicitly classify an entry as `current`, `stale`, `missing`, or `legacy_unknown`. Legacy entries are **not automatically trusted** and no silent destructive migration is allowed.
4. Detect deleted or renamed notes. Construct a proposed cleanup plan; perform mutation only through an explicit, reversible workflow. Never remove original user Markdown.
5. Keep user-authored links separate from machine-generated links. Prefer a designated generated block or sidecar over rewriting indistinguishable legacy links; preserve legacy links until ownership is resolved.
6. Retrieval and graph generation must reject or clearly flag stale vectors. Provide a read-only diagnostics mode showing freshness counts and affected IDs without dumping personal content.
7. Build artifacts in temporary/isolated generations and commit a complete verified generation only after validation; maintain prior readable artifacts on failure. Phase 3 will address broader cross-process coordination.

## Incremental work packages

### 2A — Inventory and tests (no mutation)
- Inspect `link.py`, `ask.py`, `build_graph.py`, config settings, and existing indexes using synthetic fixtures.
- Record index schema and links ownership ambiguities. Define a versioned canonicalization contract.
- Test unchanged, edited, deleted, renamed, corrupted-vector, model-changed, and legacy-index cases.

### 2B — Freshness-aware embeddings
- Add deterministic source fingerprints and model identity to new index entries.
- Reuse only validated vectors; stale or unknown entries must fail closed.
- Add dry-run and explicit rebuild flags. Report expected re-embedding API cost/external-data implications before executing network calls.
- Keep old indexes intact until a validated replacement can be committed.

### 2C — Generated link provenance
- Define and store generated relationships separately from authored ones.
- Recompute generated relationships from current validated vectors; do not remove ambiguous historical links.
- Verify that manual links survive relinking and that orphaned generated relationships disappear.

### 2D — Retrieval and graph consistency
- Ensure Ask and Graph read only verified current generations or explicitly report missing freshness.
- Test partial failure, interrupted update, index mismatch, and empty corpus using synthetic files.
- Benchmark 100, 1,000, and 5,000 **synthetic** notes before considering another datastore. Avoid claiming production performance from synthetic-only results.

## Non-negotiable acceptance tests

- Edit note: previous embedding is marked stale; it is not returned as current.
- Change embedding model: affected vectors invalidate deterministically.
- Delete note: no stale retrieval hit or generated edge remains after an approved regeneration.
- Manual links and note files survive all cleanup/rebuild scenarios.
- A failed refresh leaves the prior validated generation recoverable.
- Legacy indexes are identified and migration is opt-in.
- No test reads private knowledge or sends personal note data to an external provider.
- Existing Phase 1 GitHub Actions tests remain green.
- No build modifies `demo/` or enables public publishing.

## Decision points before implementation

- What is a realistic current and 12-month corpus size?
- Is changing providers/models expected, and is external embedding processing permitted for every note?
- How should legacy related links be classified as manual versus generated?
- What level of stale retrieval is acceptable? Recommended default: none, with explicit diagnostic fallback.

## Safe operating procedure

The release integrates all work packages in one draft pull request, per the release request, using synthetic fixtures and no embedding API calls. Review actual diffs and CI logs before merging; no deployment, private data migration, deletion, or mass re-embedding without explicit approval.
