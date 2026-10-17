# Phase 2 operations

Phase 2 keeps Markdown as the source of truth and uses local files, with no database. Run from the repository root with the requirements installed and your virtual environment activated. Always specify the local data directory during initial migration: automatic demo selection remains available when no local graph or knowledge generation exists.

## Capture and inspect

```bash
./capture.sh --text "your note"
./classify.sh --scan-only
```

Capture is local. Classification is a separate API operation: intentionally run `./classify.sh` only when you authorize sending queued captures to the configured LLM provider and its charges. Alternatively create/edit Markdown directly under `data/wiki/{projects,areas,resources,archives}/`; notes need unique stable `id`, `para`, and `summary` frontmatter fields. Refresh handles nested Markdown files too. Refresh never classifies captures automatically or sends raw captures to an API.

```bash
python refresh.py status --data-dir data
python refresh.py dry-run --data-dir data
```

Both commands are read-only and offline. The output lists affected, deleted and renamed IDs, exclusion reasons, source file fingerprints, model identity, a conservative input-token upper bound, and an approval digest. Treat this output as private. A rename retains its ID; a changed ID is a deletion plus a new note. Identical canonical text with a stable ID can reuse its verified vector after a rename. Invalid frontmatter, duplicate IDs and unsafe paths block refresh instead of silently deleting entries.

## Local embeddings (default)

Ollama must be running with `nomic-embed-text` installed. Run:

```bash
python refresh.py refresh --data-dir data
# Only when status reports unidentified legacy vectors:
python refresh.py refresh --data-dir data --migrate-legacy
```

Local refresh requires no OpenAI key, external API approval or paid budget.
`EMBEDDING_PROVIDER=ollama`, `EMBEDDING_MODEL=nomic-embed-text`, and
`OLLAMA_BASE_URL=http://localhost:11434` are defaults. Only loopback HTTP origins
are accepted, with redirects and environment proxies disabled. `/api/embed` gets
the exact canonical text with `truncate=false`; oversized inputs fail and leave
the active pointer unchanged. Ask embeds questions with this same adapter.

Identity includes provider and model (`ollama:nomic-embed-text` or
`openai:text-embedding-3-small`). Old unqualified identities are re-embedded;
they cannot mix with a new generation. Changing provider/model invalidates every
vector even when dimensions coincide. Keep model names pinned to fixed weights;
weight replacement under an unchanged name is not detectable. Old generations
and legacy embeddings remain untouched. Recovery requires the matching provider
and model via environment settings or `--provider` and `--model`.

## Approve external OpenAI embeddings and costs

Choose the exact model and obtain the provider's current input price per million tokens in your billing currency. No price is hardcoded. The following placeholders must be replaced with values you have reviewed:

```bash
python refresh.py dry-run --data-dir data --provider openai --model text-embedding-3-small --price-per-million RATE
python refresh.py refresh --data-dir data --provider openai --model text-embedding-3-small \
  --allow-api --approve-plan DIGEST_FROM_DRY_RUN \
  --price-per-million RATE --max-cost APPROVED_BUDGET
```

`--allow-api` approves sending affected canonical note text externally. The digest binds approval to the model, source snapshots, current index and affected IDs. A source/model/plan change requires another dry-run. The budget is checked before creating an API client. Estimated upper-bound cost is UTF-8 input bytes × supplied rate / 1,000,000; one token cannot exceed this byte count for these text inputs. This intentionally overestimates typical embedding tokens. The supplied rate must reflect your provider's actual billing; this is not a provider-side spending limit. One request is made per affected note with no automatic retries. Failed requests may still incur provider charges; rerunning after a failure can repeat charges because unpublished partial embeddings are not reused automatically.

Legacy vectors without valid provenance are `legacy_unknown`, never stamped current. Add `--migrate-legacy` to the same explicitly approved refresh to re-embed those notes. Existing legacy files and indexes remain intact. Migration does not infer the model, content version or ownership of historical links.

A refresh with only deletions, path changes or metadata/manual-link changes that do not alter canonical text needs no API permission:

```bash
python refresh.py refresh --data-dir data
```

Only affected notes are embedded. Changing the model invalidates all vectors. Set `EMBEDDING_PROVIDER` and `EMBEDDING_MODEL` to the same provider and model when launching Ask, Graph and the UI; a mismatched model fails verification. The CLI supports `--threshold` for generated semantic relationships. Generated edges are replaced in `relationships.json`; no Markdown or manual frontmatter links are rewritten. Indistinguishable links left by the historical linker remain authored/ambiguous links and require manual review if you want to remove them.

## Artifact and freshness contract

Canonical input version 1 reuses `link.build_embed_text`: title (first H1, or filename fallback), stripped summary, deduplicated tags in stored order, and stripped body, separated by two newlines with their existing labels. Files are decoded as UTF-8 with Python universal newline handling; internal whitespace is preserved. Frontmatter links and embedding bookkeeping are excluded. New generated relationships live entirely outside Markdown and cannot change this input. Historical Related sections remain part of the body because ownership cannot safely be inferred.

Each index entry records schema version 1, note ID, source SHA-256 of the exact API input, model identity, dimensions, checksum of persisted `.npy` bytes, embedding creation time, and source path. Vectors must be finite, nonzero real arrays with uniform dimensions. Source and artifact hashes detect changes/corruption, not malicious replacement by someone with write access to the entire knowledge directory.

A generation in `data/knowledge/generations/ID/` contains vectors, index, graph, generated relationships and a checksummed manifest of the entire source snapshot. A single atomically replaced `data/knowledge/current.json` selects the generation. Files and directories are flushed before publication. A writer lock prevents overlapping refreshes. Readers validate one generation, vector bytes and the current source snapshot; a changed note, manual link, deletion, rename or corrupt artifact makes the generation unavailable until refreshed. Ask makes no query API call when that gate fails. Loose legacy indexes/graphs cannot substitute for a complete verified generation. Graph displays no stale generation. Empty corpora can be refreshed without API calls.

Ask embeds queries locally by default. Answer synthesis uses xAI when `XAI_API_KEY` is set, otherwise OpenAI then Groq. `XAI_LLM_MODEL` defaults to `grok-3-mini` and is configurable. Answer synthesis sends the question and retrieved excerpts off the Mac and may incur charges; the UI and CLI disclose this. No answer key is required to refresh or view Graph. The local UI's Refresh action runs only the safe refresh command; when API approval is needed it reports the CLI requirement. Captured raw notes remain queued until separately classified. Public demo reads are preserved; refresh/restore refuses the committed demo directory.

`link.py` scan remains available; its embedding/link CLI modes delegate to safe refresh and cannot silently make paid calls or modify notes. Use `refresh.py` for cost approval and full-corpus updates. Legacy per-note, embed-only and directional link modes return an explicit migration error. Obsidian side-effect flags no longer trigger export. Obsidian export remains a separate explicit command. `build_graph.py` remains an export tool with verified semantic vectors; exports do not activate a knowledge generation. The local UI and Ask use the active generation; an exported `data/graph.json` is not its authority.

## Recovery

1. Stop repeated refresh attempts, retain the raw notes, legacy embeddings and entire `knowledge/` directory, and fix the reported frontmatter, dimension, filesystem, or provider error. Never delete note files to clear an artifact error.
2. A failed provider request or staged write leaves `current.json` unchanged. Unpublished generation directories are retained for inspection; no cleanup command runs automatically. Readers will still reject a previous generation if today's notes differ from it.
3. Run another dry-run and approve a new refresh if needed. A corrupted active vector can be re-embedded with normal approval. If manifest/index/graph corruption blocks inventory, restore a complete retained generation first.
4. To recover a damaged pointer, identify the 32-character generation ID under `data/knowledge/generations/`. The manifest's `previous` field records its predecessor. Restore checks every artifact and vector against today's source snapshot and configured model before atomically switching:

```bash
python refresh.py restore --data-dir data --generation GENERATION_ID
python refresh.py status --data-dir data
```

A stale generation cannot be restored as current. If needed, first restore matching Markdown from your own backup, then use the command. If no matching complete generation exists, keep a backup of `knowledge/`, move that directory aside locally, and run a fresh dry-run/approved migration from retained legacy embeddings or current notes. Moving aside artifacts must not remove raw/wiki data. No repair procedure certifies unidentified old vectors.

Generation files use relative vector filenames and survive moving a complete data directory. Keep backups: atomic replacement protects against interrupted application writes, not loss of the disk. Writers use POSIX `flock` and directory `fsync`; this release targets macOS/Linux local filesystems. Windows and network filesystem locking semantics are not validated. Avoid edits during refresh; the source snapshot is checked again before pointer replacement, and subsequent edits fail the reader freshness gate.

## Verification

```bash
DEPLOY_MODE=true PYTHON_DOTENV_DISABLED=1 OPENAI_API_KEY=synthetic-no-network-key \
  python -B -m unittest discover -s tests -p 'test_*.py' -v
DEPLOY_MODE=true PYTHON_DOTENV_DISABLED=1 OPENAI_API_KEY=synthetic-no-network-key \
  python -B tests/browser_demo_check.py
git diff --check
```

The suite uses temporary synthetic data and fake embedding/LLM responses. The optional browser check fetches the pinned public vis-network library and launches an isolated headless browser; it never uses personal notes or a personal browser profile. Automated tests make no live provider calls. A separate synthetic-only smoke check against the local Ollama server verified note refresh, question embeddings and Graph at 768 dimensions; no answer-provider API was called. No production corpus benchmark or real-account billing claim is made.
