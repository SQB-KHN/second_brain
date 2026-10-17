# SecondSelf 2.1 — Intelligent document ingestion: acceptance specification

## User journey
In local Streamlit Capture, select **Import document**, upload a PDF, CSV or XLSX, review detected document name, pages/sheets, extracted text, warnings and privacy status, then explicitly **Save & Index**. Search and Ask must retrieve passages with a citation identifying original filename and page number or sheet/row. Imports must not be automatically sent to external LLMs. The existing raw capture queue remains separate.

## MVP functional requirements
1. Local processing only by default. PDF extraction via existing pypdf; CSV (UTF-8/UTF-8 BOM) via standard csv; XLSX using openpyxl read_only/data_only. Do not run macros, formulas or external links. Enforce per-file size, page/sheet/row/cell and extracted-text limits with clear failures.
2. Structure-aware segments: preserve source file name, SHA-256, source type, page (PDF) or sheet and row range (tabular), segment ordinal and extraction warnings. Use bounded chunks; mark scanned/image-only PDF pages as unsupported rather than fabricating text. No OCR in first release.
3. Pre-import preview and user confirmation; write source copy only after confirmation. Safe filenames and paths, content signature validation, ZIP bomb/decompression protections for XLSX, encoding errors reported clearly.
4. Stable identity and idempotency based on content hash + source metadata: identical reuploads do not create duplicate notes. Changed files create a new version (no silent overwrite). Atomic persistence; failures leave existing documents intact.
5. Integrate with **verified transactional refresh** and local Ollama, without weakening generation freshness, model provenance, link/graph consistency or writer locking. Each indexed segment is represented as canonical searchable knowledge with robust provenance. A partial failure must not publish incomplete index; note that source copy and staged segments may remain for recovery.
6. Retrieval and source display: show document title + exact page or sheet/row ranges alongside Ask results; avoid claiming line-perfect citations unless measured/recorded. Prevent prompt injection in uploaded text from gaining app-control powers. Preserve passage evidence through normal retrieval.
7. Local import history showing staged/indexed/errors, reviewable provenance, and a manual retry; no deletion feature in v1.
8. DEPLOY_MODE: import and local writes disabled; no personal documents included in synthetic demo. API keys never logged. Explain that asking via Grok/xAI sends retrieved excerpts externally and may cost money; require an explicit, informed user action before transmitting imported-document excerpts.
9. Test with temporary synthetic PDFs, CSVs, XLSX files; malformed/oversized files, duplicates, multi-sheet/page metadata, blank/scanned PDF, failure/recovery, injection-like text, notes still searchable, local Ollama mocked, user interface browser checks. Run all existing tests. No paid API calls.
10. Documentation must explain supported formats, limitations, security/privacy, reproducible synthetic demo, performance bounds, and operational recovery.

## Non-goals
No web crawling, automatic cloud OCR, bulk background syncing, external connector access, document interpretation that modifies source, autonomous execution or unapproved public deployment.

## Delivery
Implement one integrated feature branch and one draft PR. Keep personal data gitignored and do not merge or deploy without manual acceptance. Clearly label any unimplemented advanced retrieval as future work; don't claim hybrid search or extraction precision absent test evidence.
