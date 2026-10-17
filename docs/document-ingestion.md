# Local document ingestion (SecondSelf 2.1)

In local Capture, expand **Import document**, select a PDF, CSV or XLSX, inspect
page/sheet references, extraction warnings and text, then click **Save & Index
document**. Preview never saves the source or calls a model. The original raw
capture inbox remains a separate workflow. Library text search includes imported
segments; Ask uses the existing verified vector retrieval and displays original
filename plus page or sheet/row references. Imported evidence is read-only; import
a changed source to create another version.

## Formats and bounds

- PDF: pypdf text extraction, up to 200 pages. Blank/image-only pages are reported;
  an entirely blank/scanned PDF fails. No OCR, layout reconstruction, table
  interpretation or line-perfect citation claims. Encrypted PDFs are unsupported.
- CSV: strict UTF-8/UTF-8 BOM parsing with the standard csv module. Quoted multiline
  fields count as one logical record; row references are record numbers, not physical
  file line numbers. CSV has no unique binary signature; binary/NUL and disguised
  PDF/ZIP content are rejected.
- XLSX: openpyxl read_only/data_only with external links disabled. Up to 20 sheets;
  formulas/macros never execute. Formula cells expose cached values only and can
  appear blank. Macro payloads are rejected. Legacy XLS and XLSM are unsupported.
- 25 MiB source, 1,000,000 extracted characters, 1,000 segments, 1,000 characters
  per segment; up to 10,000 rows and 100,000 cells per sheet. Wide/long rows can
  span segments sharing the same row reference. Preview shows the first 20 segments
  with a download of all extracted segments. Unsupported/over-limit files fail
  rather than silently truncating evidence.
- XLSX ZIP preflight: 2,000 entries, 50 MiB aggregate expansion, 20 MiB per entry,
  200:1 maximum expansion ratio; encrypted archives rejected. defusedxml is installed
  for XML entity protection. Archives are read in memory, never extracted to paths.

Bounds constrain accepted content, but parser CPU/memory use can exceed extracted
text size (especially complex PDFs). Extraction runs synchronously in the local app;
there is no OS process sandbox or parser timeout. Use trusted documents and a
maintained Python environment. This release does not benchmark or promise extraction
precision. Existing graph generation compares segment pairs, so indexing time grows
with total corpus size. Hybrid retrieval, reranking, OCR and background bulk ingestion
are future work.

## Privacy and security

Import requires local mode, enabled Capture/refresh, the Ollama embedding provider,
and a loopback Ollama endpoint. No paid calls or automatic external LLM classification
occur. Ask defaults to retrieving document sources locally without synthesis; its
unchecked consent box explicitly authorizes sending the current question and
retrieved excerpts to the configured external provider (including Grok/xAI), which
may cost money. CLI users must pass `--allow-document-external`. Ordinary notes keep
their existing Ask behavior. Source text is untrusted prompt evidence; the answer
model receives no execution or application-control tools. Prompt instructions are
not a guarantee that an external model will ignore every malicious passage.

Sources and recovery state live under ignored `data/imports/`; canonical segments
under ignored `data/wiki/resources/document-<id>/`. Names are sanitized and never
used as filesystem paths; content SHA-256 plus sanitized source name determines
identity. Identical bytes and name reuse the import, changed bytes create a new
version; renaming a source creates a separate identity. State includes source hash,
format, warnings, ordinal, and measured page or sheet/row references. No document
content is included in the committed synthetic demo. DEPLOY_MODE disables the import
UI and backend writes regardless of capture flags. Local source storage is plaintext;
protect the workstation and backups. No deletion operation is provided.

## Transactions and recovery

Confirmation durably stages source and state as an atomic directory rename. Complete
canonical segment sets are staged separately, then moved into the wiki under the
same writer lock used by verified refresh. Refresh retains all freshness, model,
legacy migration, checksums and generation publication checks. Partial segment
creation is never published. A normal indexing failure withdraws those new segments,
retaining the original source and error history for **Retry import**. Existing notes
and the previous generation remain intact and searchable. Provider errors are stored
as generic messages, without credentials or provider response content.

A process crash can leave staged files or segments before publication; Ask/Graph
fail closed if the canonical corpus does not match the active generation. Restart,
open Capture → Import history and retry that import. Retry reconciles a generation
already published before its status update; it revalidates source identity first.
If a source checksum fails, restore that bundle from a trusted backup. Incomplete
hidden `.stage-*` / `.notes-*` directories are never automatically published; retain
them for manual inspection (no automatic data deletion). An unrelated stale/legacy
corpus can block refresh; use the existing `refresh.py status` / `dry-run` and explicit
legacy migration workflow before retrying. Do not remove writer locks or manually
edit imported segments to force publication.

## Reproducible synthetic validation

Install `requirements.txt`, then run (all data generated in temporary workspaces):

```sh
PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true .venv/bin/python -m unittest discover -s tests -v
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true .venv/bin/python tests/browser_document_check.py
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true .venv/bin/python tests/browser_demo_check.py
```

Browser tests additionally require Playwright and Chrome; set
`SECONDSELF_TEST_CHROME` when Chrome is not installed at the macOS default path.
The document browser test mocks Ollama and answer synthesis, denies external browser
requests, creates synthetic multi-page/multi-sheet files and tests upload previews,
malformed input, duplicate detection, offline failure/retry and Ask consent/provenance.
It does not need API keys, a running Ollama, personal documents or a paid service.

Validation on 2026-10-17: all 88 unittest cases passed; the real Chrome document
upload/consent workflow and existing graph browser checks passed. Ollama embeddings
and answer synthesis were mocked; real local Ollama throughput and external model
answer quality were not measured. No paid APIs, deployment or personal data were
used. CI runs both browser scripts on this branch and pull requests.

### PR #19 integration verification (2026-10-17)

Merged `origin/main` including AI Insights into `document-ingestion-v1`, retaining
both features and both private-data ignore rules. Validation used temporary,
synthetic workspaces, without reading personal documents or sending cloud calls.

- Full automated suite: 93 tests passed, with no skips.
- Document browser suite: PDF/CSV/XLSX previews and uploads, malformed input,
  duplicate handling, indexing failure/retry, Ask consent and page citations passed.
- Combined browser regression: imported CSV evidence appears in Library (read-only),
  Explore graph node details, and an Insights potential contradiction.
- Graph browser suite: empty/populated graph, category filters, canvas node clicks,
  and hostile-content rendering passed with the actual pinned graph library.
- Insights browser suite: real local Ollama refresh, generation, evidence, review
  persistence across restart, stale-source detection, all views and mobile viewport
  passed.

Limits: local tests used Python 3.14 and Chrome; CI uses Python 3.11 and Chromium.
Document browser embeddings and external Ask synthesis are deterministic mocks;
real Ollama is exercised separately by the Insights browser suite. No live paid
LLM synthesis, OCR, deployment or production-data validation was performed.
