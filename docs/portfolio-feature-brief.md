# SecondSelf — Portfolio Feature Brief

## Executive overview
**SecondSelf** is a local-first personal knowledge, document-evidence and statistical-analysis workspace built in Python and Streamlit, developed using AI-assisted coding with Codex and human-directed product architecture, specifications, verification and delivery. It is a working **local application**, not a publicly deployed SaaS product.

## Demonstrated product capabilities
| Capability | Engineering implementation | Status |
| --- | --- | --- |
| Knowledge capture and retrieval | Markdown notes, Ollama vector embeddings, transactional verified generations, local retrieval, optional explicit xAI answer synthesis | Merged |
| Source-aware ingestion | Preview and explicit import for PDF, CSV, XLSX; PDF page and sheet/row references; duplicate detection, recovery/history | PR #19 merged |
| Local AI Insights | Evidence-backed candidate gaps, potential contradictions and connections with explicit user review and persisted feedback | PR #18 merged |
| Dataset Manager | CSV, XLSX and scalar Parquet imports, immutable SHA-256 source storage, SQLite version history, metadata dictionaries, quality profiling and saved descriptive statistics | PR #20 merged |
| Analyse | SciPy/statsmodels-based descriptives, Pearson/Spearman correlation, paired and independent t-tests, chi-square, OLS/logistic regression, diagnostics, chart/export support and saved reproducible run manifests | PR #21 draft; not merged to main |

## Architecture and technical decisions
- **Two separate data paths:** evidence documents create traceable searchable excerpts; structured datasets remain canonical typed tables. Statistical procedures operate on dataset versions, not semantic embeddings.
- **Local-first defaults:** personal data stays in gitignored local workspace directories. Ollama handles local embedding; external xAI question answering is optional and requires user action/consent for imported excerpts.
- **Provenance:** document page/sheet/row references; dataset source SHA-256, immutable versions and metadata; analysis manifests tied to precise dataset versions and chosen procedures.
- **Reliability:** transactional refresh generations for knowledge, atomic dataset registry and immutable source bytes, guarded read-only demo mode, bounded imports and execution, retained review/analysis histories.
- **Methodological boundaries:** statistical results are calculated by numerical libraries, not written by an LLM. Regression is not automatically causal; assumptions and diagnostics matter. Arbitrary uploaded code is not executed.

## End-to-end demonstration scenarios (synthetic data only)
1. **Source intelligence:** import a public or synthetic PDF, inspect a page preview, index it locally, ask a sourced question and check the exact page reference.
2. **Data management:** import synthetic CSV/XLSX/Parquet, inspect types/missingness, edit column descriptions, reimport identical content to demonstrate deduplication, then revise data to show version history.
3. **Statistical research (PR #21):** select a registered synthetic dataset version, run a supported statistical test or model, inspect sample exclusions and diagnostics, and export its chart and saved reproducible manifest.
4. **Knowledge insight:** generate a local reviewable Insight from synthetic notes, verify supporting excerpts and save/reopen a review.

## Validation and honest limitations
- PR #21 developer-reported final validation: **124 local automated tests passed** and **five browser suites passed**; GitHub CI for its latest head was independently checked as successful.
- Dataset Manager PR #20 developer-reported **108 local tests** and four browser suites; merged CI passed.
- Document Ingestion PR #19 developer-reported **93 tests** after branch reconciliation and browser checks; merged CI passed.
- These are synthetic/software acceptance results, not independent statistical method audits, production performance measurements, penetration tests or results on real datasets.
- No OCR for scanned PDFs; no fully sandboxed parser or arbitrary external code execution. Limits exist on upload volume, tables and workers; same-user OS process threats and parser vulnerabilities are not eliminated.
- No autonomous browsing or agentic desktop access, no real multi-user system, no hosted public demo, no verified production-scale workload.
- Advanced methods (panel/time-series/Bayesian/causal inference), complete AI statistical interpretation and connector-based automated actions remain future work.

## Evidence and artifacts
- [Repository and screenshots](https://github.com/SQB-KHN/second_brain)
- [AI Insights PR #18](https://github.com/SQB-KHN/second_brain/pull/18)
- [Document Ingestion PR #19](https://github.com/SQB-KHN/second_brain/pull/19)
- [Dataset Manager PR #20](https://github.com/SQB-KHN/second_brain/pull/20)
- [Statistical Engine PR #21](https://github.com/SQB-KHN/second_brain/pull/21)
- [Architecture](portfolio-architecture.md) · [Engineering case study](portfolio-case-study.md) · [Document ingestion](document-ingestion.md) · [Datasets](dataset-manager.md) · [Statistical engine](statistical-engine.md)

## Suggested portfolio positioning
**Project:** SecondSelf — Evidence-grounded Personal Research and Statistical Intelligence Workspace

**Role:** Product owner and AI-assisted developer; requirements engineering, architecture direction, GitHub delivery, manual acceptance and verification.

**Stack:** Python, Streamlit, SQLite, NumPy, SciPy, statsmodels, pyarrow, openpyxl, pypdf, Ollama, optional xAI Grok, GitHub Actions, browser test automation.

**Value:** One local workflow that connects source provenance, reproducible dataset management and auditable statistical analyses, while making cloud AI use explicit.
