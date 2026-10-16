# Secure demo publication: Phase 1

## Design decision

Problem: public bundles can disclose private notes, metadata, vectors, and stale
artifacts because the existing publisher treats almost everything as public.

Constraints: retain Markdown, preserve local app behavior and private source data,
use no network or API, and make no hosting changes. This is a local batch build;
current and future corpus size are unknown. Non-goals: approving existing samples,
redaction, private-data migration, runtime capture controls, and deploying a bundle.

Options considered:

- Do nothing: preserves current demo functionality and requires no migration; only
  viable if publication is permanently stopped. It fails the publication objective.
- Path-only manifest: simplest boundary; useful for an immutable dedicated sample
  repository. In a mutable private corpus it silently approves future edits.
- Path plus content hash (chosen): small, explicit approval boundary that detects
  edited samples. Costs manual reapproval and does not prove content is safe.
- Dedicated sample corpus: strongest separation for frequent demo authoring; costs
  maintaining another corpus. Prefer it when ongoing sample editing justifies it.

Decision: an empty-by-default versioned manifest approves exact Markdown bytes.
No private index, graph, embedding, or ancillary artifact is copied. Reconstruct
index and graph from approved notes; reject unresolved explicit references and
local inline Markdown artifact links. No embeddings are required for graph display;
Ask remains unindexed. Graph schema follows existing app fields without importing
the pipeline, whose configuration and logging have local side effects.

Tradeoff: manual approval and reduced demo retrieval functionality in exchange for
an auditable boundary. Human review is load-bearing: hashes cannot detect private
text, sensitive URLs, or identifying metadata inside an explicitly approved note.
Unknown references in arbitrary prose or custom Markdown syntax cannot be inferred.
Approval must cover every byte, including frontmatter and external references.

Failure handling: stage in a fresh sibling directory; reject malformed approvals,
missing/changed notes, duplicate identities, symlink inputs, unsafe destination
relationships, and unresolved links before replacement. Swap using two directory
renames, restoring the previous directory on ordinary replacement failure. If
restoration also fails, preserve the previous bundle in the sibling
`.secondself-stage-*/previous` directory for manual recovery. Staging is removed
otherwise; no source is deleted. There is a brief rename gap, and abrupt process
termination/power loss is not transactionally recovered. Run this offline with one
publisher and stable inputs; concurrent writers and live serving are unsupported.
The source and approval manifest are trusted local inputs, not an adversarial
multiuser filesystem. Graph construction uses memory proportional to the approved
corpus; large corpora would warrant streaming and benchmarking.

Reversibility: revert publisher/docs/tests/manifest changes to undo the code change,
but do not run the old denylist publisher. No source schema migration occurs.
For bundle rollback, restore a separately retained, reviewed safe bundle, or build
from a previously reviewed manifest and matching samples. Never restore an old
bundle merely because it predates this change; it may contain private data.

Revisit if provenance-verified embeddings become necessary, sample edits become
frequent enough for a dedicated corpus, or live/concurrent publishing is required.
Open questions: repository maintainer owns sample approval, desired retrieval
support, expected corpus scale, and assignment of publication operations ownership.

## Readiness review

Verdict: ready for a review PR and isolated local bundle preparation under the
documented operating constraints. The recovered fixes for interruption recovery,
graph HTML serialization, reference validation, and symlink checks passed the
latest verification. Public deployment is not yet approved: the actual public
corpus and generated bundle still require maintainer/sample-reviewer approval.
No existing committed demo content was approved or regenerated here.

Verification evidence (synthetic data and isolated temporary directories):

- 22 unit/integration tests passed, with no failures, errors, or skips, including
  failed restoration, preserved recovery bundles, reference rejection, graph
  serialization, Streamlit empty/approved-note states, and CLI compatibility.
- 7 supplemental symlink probes passed: source root, wiki root, category ancestor,
  destination, manifest, note file, and dangling source.
- 3 real-Chrome scenarios passed: empty graph; approved-note canvas, filters, and
  node click; hostile script/image payload rendering without injected execution.
  The browser check initially failed on sandbox DNS resolution; an approved retry
  fetched the pinned graph library and passed. The publisher itself uses no network.
- `git diff --check` passed. These results are verification evidence, not a safety
  certification or approval to publish actual data.

Blast radius: a bad bundle could expose source content to all public demo visitors;
external copies cannot reliably be recalled. A failed/slow local build delays a
refresh; the prior output remains on ordinary validation/build errors. Stopping
the build and retaining a reviewed prior bundle is the workaround.

| Area | Item | Status | Evidence | Owner |
| --- | --- | --- | --- | --- |
| Observability | Build outcome without source content | Present | Count-only success and generic CLI failure; synthetic log test | Maintainer |
| Observability | Hosted alerts/dashboard | N-A | Local batch build; no hosted runtime changed | Maintainer |
| Failure handling | Input/write/validation/replacement failure | Present | Automated synthetic failure and recovery tests | Maintainer |
| Failure handling | Slow disk, concurrency, process crash | Partial | Slow disk blocks offline build; no network dependency; single-writer constraint; crash recovery manual | Maintainer |
| Rollback | Prior bundle survives replacement failure | Present | Injected rename failure test; no data schema migration | Maintainer |
| Operability | Manual recovery procedure | Present | Steps below preserve original backups and require approval verification | Maintainer |
| Data | Approved bytes and fresh artifacts only | Present | Hash check, rebuilt metadata, stale/removed sample tests | Sample reviewer |
| Operability | Named publication operator | Partial | Maintainer role documented; individual assignment pending | Repository owner |
| Capacity/cost | Offline build with no paid API | Present | No API calls or embedding generation; actual scale unmeasured | Maintainer |

Blocker: before public launch, the sample reviewer must approve all intended sample
bytes and review generated output. Without this, an operator cannot recall a
privacy disclosure at three in the morning. An empty manifest is intentionally safe
but is not a useful public demonstration. Existing hosted/committed artifacts
require separate review; this work cannot establish their safety.

Should have: repository owner should name the publisher and sample reviewer before
any launch (date: next proposed launch; no launch date supplied).

Known limitations proposed for acceptance: offline single-writer operation,
manual crash recovery, and no demo embeddings. Acceptance owner is the repository
maintainer; this review does not claim they have accepted these gaps.

Outstanding verification limits: interruption tests inject Python exceptions, not
`SIGKILL`, power loss, or filesystem failure. The after-install interruption test
uses equivalent old/new contents and does not establish changed-generation
selection. Concurrent writers, adversarial filesystem races, slow/full disks,
production capacity, running infrastructure, existing public copies, hosted capture
controls, alerts, and real corpus suitability remain unverified. Browser evidence
covers synthetic standalone graphs; Streamlit behavior was checked with AppTest,
not a hosted end-to-end browser session. The manual procedure below has not been
executed against an actual interrupted publication. No deployment or infrastructure
changes were performed. Team questions: who approves samples, who operates
publication, and is retrieval required before launch?

## Manual recovery steps

Use this procedure after interrupted replacement or a `RecoveryRequired` message.
The publication operator owns recovery; the sample reviewer owns content approval.
Do not assume the newest directory, an older bundle, or a successful-looking graph
is safe to publish.

1. **Stop publication and keep recovery offline.** Ensure no publisher is still
   running and no other process will write the destination, manifest, or samples.
   If the affected output is served, stop serving it through the separately
   authorized hosting procedure. Do not retry publication or clean temporary
   directories while investigating. Record the exact source, manifest, destination,
   reported recovery path, and error without logging note contents.
2. **Locate and preserve every candidate.** Inspect the destination and its sibling
   `.secondself-stage-*` directories without modifying them. `previous` holds the
   prior destination when retained; `bundle` may hold staged output. After abrupt
   termination there may be no diagnostic, so inspect all such sibling directories;
   do not select one solely by timestamp. Reject symlink paths/components and
   unexpected locations. Record an inventory and hashes, and retain a separate
   verified copy on trusted storage before changing directory placement. Never
   overwrite, move away, or delete the only good backup.
3. **Determine the replacement state.** If the destination is absent and `previous`
   exists, the old bundle was moved but installation or restoration did not finish.
   If both exist, installation may have completed before interruption; preserve and
   review both. If the destination exists without `previous`, automatic restoration
   may have succeeded, or publication may have completed: verify contents rather
   than inferring success. If neither exists, stop and locate a separately retained
   approved bundle or rebuild safely in isolation; do not invent a recovery source.
4. **Verify backup contents and approval.** Work on a copy. Check regular files and
   directories only, no symlinks, and compare file paths and SHA-256 digests with a
   trusted inventory of the previously approved bundle. Confirm every note's exact
   bytes against its retained approved manifest, then review metadata, graph nodes,
   edges, and index entries for approved identities/references only. A Phase 1
   bundle contains only approved Markdown, `wiki/.index.json`, `graph.json`,
   `README.md`, and an empty `embeddings/index.json`; unexpected files or vectors
   require investigation. Compare rebuilt artifacts with a fresh isolated build
   from the matching approved manifest and samples where available. A hash match
   establishes identity, not privacy approval. If approval provenance is missing,
   obtain a new full content review or leave the output unavailable.
5. **Resolve restoration failures before retrying.** Check destination/parent
   permissions, free space, storage health, and competing processes. Do not alter
   source notes, discard backups, or fall back to the old denylist publisher.
   Escalate storage or permission failures to the maintainer if unresolved. Preserve
   all recovery directories until a verified replacement and independent retained
   backup exist.
6. **Restore from a copy of a verified, previously approved bundle.** Prepare a
   uniquely named sibling recovery candidate and verify that the copy matches the
   approved backup inventory. Keep the original backup intact. If the destination
   exists, preserve it under a distinct unused quarantine name after ensuring it
   also has a retained copy; never merge directories or overwrite a candidate.
   With publication stopped and the destination absent, rename the verified recovery
   candidate into place on the same filesystem. If any step fails, stop, record
   the new state, and retain all copies; do not delete the only good copy to retry.
7. **Validate before resuming service.** Recheck installed file hashes, approved
   identities/references, graph display, and the expected unindexed Ask state using
   isolated copies first. Have the maintainer/sample reviewer approve the recovered
   output. Record which approved generation was restored. Retain the original
   verified backup and recovery evidence until an explicit retention/cleanup
   decision; restoration itself does not authorize public deployment. Resume
   publication or serving only through the separately authorized release process.
