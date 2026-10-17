# SecondSelf 2.2 — Dataset Manager v1: implementation contract

## Goal
Add a local-first **Datasets** workspace for structured numerical data, separate from document-text ingestion. Do **not** convert complete numeric datasets into Markdown chunks or embeddings as a substitute for storing raw tables. The canonical dataset remains a typed table; metadata may be indexed for discovery in a later release.

## First release acceptance criteria
1. In Streamlit, a Datasets view offers upload of CSV, XLSX, and Parquet files with an explicit preview and confirmation step. Keep Home, Capture, Ask, Explore, Library and Insights functional; preserve source-provenance document ingestion. Show clear error states.
2. Store original bytes immutably in private, gitignored local storage under configured DATA_DIR. Maintain an atomic registry (SQLite recommended) with generated dataset ID, readable name, format, SHA-256, creation timestamp, file size, version, origin and schema/profile metadata. Do not write private files to the repository.
3. CSV UTF-8 and BOM, explicit error for unsupported encodings; XLSX sheet selection and bounded read_only/data_only values without macros/external-link fetching; Parquet use pyarrow with resource limits. Validate content and file extension; defend against path traversal, symlink abuse, corrupt files, excessive decompression and misleading extensions. Limit bytes, sheets, rows, columns, individual cell length and total preview output. Avoid loading unbounded files into process memory; document ceilings.
4. Identical content + import options must deduplicate. A changed upload with the same human-readable name creates a new version, not an overwrite. Existing versions remain immutable. Track provenance and hash each version. Registration failures must not expose partially committed records.
5. Preview row and column counts, column names, inferred types, null counts, duplicates and a bounded sample; distinguish numeric, categorical, temporal and textual types and show type ambiguities. XLSX preserves workbook and sheet identity. Supply a user-editable **metadata-only** data dictionary (description and units) without mutating original data.
6. Queryable local inventory with source name, versions, schema/profile summary and inspection of selected datasets. Explicit manual refresh/reprofile; import/validation errors actionable. Deletion and automatic cloud sync are not part of v1.
7. Provide safe, reproducible *descriptive statistics only* in v1: count, missingness, mean/median/std/min/max/quantiles for valid numeric columns, category counts for suitable dimensions; do not overclaim inferential statistics. Save outputs with dataset SHA, columns, parameters, software/library versions and timestamp. Statistical tests/regression belong to SecondSelf 3.1.
8. No paid API calls, no autonomous network fetch, no AI-based mathematical calculation. Dataset contents never sent to Grok/xAI without a later separately designed consent mechanism. DEPLOY_MODE and demo remain read-only, private datasets excluded.
9. CI and browser tests with synthetic CSV/XLSX/Parquet fixtures: valid imports, duplicates, versioning, previews, missingness, ambiguous typing, sheet selection, corrupt/oversized files, failure recovery, permissions and existing application regression. Test using temporary DATA_DIR, never real personal knowledge. Verify imports and existing ingestion operate together.
10. Update README and dedicated documentation: local run instructions, architecture, limitations, dependencies, security boundaries, performance limits and synthetic demo. Do not claim sandboxing or security guarantees that are not implemented.

## Engineering constraints
- Build on main after Document Ingestion PR #19 merge; existing AI Insights and source provenance must remain intact.
- Prefer a narrow, testable architecture: dataset_registry.py / dataset_parser.py / dataset_profile.py or equivalent and a Datasets UI view.
- Keep dependencies few and pinned/compatible through requirements as appropriate (pandas and pyarrow only if necessary, openpyxl for XLSX), and document dependency weight.
- Enforce constrained execution rather than letting uploaded content become executable code or dataframe query expressions.
- No external integrations, user-uploaded code execution, automatic transformations, training or predictive modelling in v1.
- Deliver one tested feature branch, one draft pull request against main; do not merge, deploy or alter actual personal files without explicit approval.
