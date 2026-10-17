# SecondSelf 2.2 Dataset Manager

Datasets stores local structured tables separately from document ingestion. It does
not create Markdown chunks, vectors, graph nodes, or AI prompts from dataset values.
The existing Capture document importer remains available for document-oriented
extraction, including its existing CSV/XLSX behavior and source citations.

## Run locally

Install the application dependencies in a virtual environment and select a private
local workspace (use its canonical absolute path, without symlink components):

```sh
python -m pip install -r requirements.txt
DEPLOY_MODE=false SECONDSELF_DATA_DIR=/absolute/private/workspace python -m streamlit run app.py
```

Open **Datasets**, upload a file, select a worksheet for XLSX, then click **Preview
dataset**. Review counts, inferred types, missingness, ambiguities and the bounded
sample before **Confirm dataset import**. Changing the file or worksheet invalidates
the preview. Naming changed content with the same dataset name creates the next
version. Identical bytes, format and parser options return the existing version,
even if the proposed dataset/source name differs. Worksheet selection is an import
option, so two sheets in the same workbook register separate versions while sharing
one original workbook blob. Names are case-sensitive; whitespace at either end is
trimmed. Versions are never overwritten.

Search the inventory by dataset or original filename. It shows 100 matching versions per page, newest first; use **Inventory page**
to inspect older versions. Select a version to inspect
it, edit descriptions and units in its metadata-only dictionary, or explicitly
reprofile it. **Refresh inventory** reloads disk state. Descriptive statistics are
saved locally and can be downloaded as JSON; selecting an earlier saved run does
not recompute it. The UI shows at most 50 saved runs per version (older runs remain in
SQLite). New versions begin with a blank dictionary.

## Architecture and persistence

- `dataset_parser.py`: input checks and a separate Python worker with a 30-second
  timeout; UTF-8 CSV via stdlib, XLSX via openpyxl (`read_only`, `data_only`, no
  external links), scalar Parquet via pyarrow with bounded batches and Thrift
  metadata limits. No formulas, uploaded code, query expressions or transformations
  are executed. Worker environment excludes application credentials.
- `dataset_profile.py`: deterministic type inference, missingness, duplicate rows,
  ambiguities and descriptive arithmetic. It imports no model/provider code.
- `dataset_registry.py`: a private `DATA_DIR/datasets/` directory, content-addressed
  original bytes (`<sha256>.source`) and SQLite registry. Registry rows include UUID,
  readable name/version, original filename, format, SHA-256, size, UTC creation time,
  local-upload origin, import options, schema/profile and editable dictionary.
  Statistics are separate immutable rows in the same database.
- `dataset_ui.py`: preview/confirmation, inventory, inspection, dictionary and saved
  statistics. Dataset operations never call ingestion, embeddings, Ask or Insights.

New source files are written to a private temporary file, flushed/fsynced and
published with an atomic, no-overwrite hard link; the directory is fsynced before
registry commit. SQLite `BEGIN IMMEDIATE`, uniqueness constraints and `synchronous=FULL`
serialize version allocation/deduplication and commit metadata atomically. Failed
transactions expose no partial records. A process crash can leave an unreferenced
complete blob or temporary file, never an inventory entry referencing a partial
write. Retrying reuses a verified complete blob. There is no automatic cleanup or
deletion. Back up the entire directory while the application is stopped.

Directory mode is 0700, registry mode 0600, published sources 0400. Inspection,
reprofiling, deduplication and statistics verify original size/SHA. Storage rejects
symlink components, unsafe registry paths, hard-linked sources and path-bearing
upload names. Upload names are metadata, never storage paths. All `datasets/`
directories inside the checkout are gitignored, including custom workspace paths.
The existing default-deny demo publisher does not include these files. In demo or
`DEPLOY_MODE=true`, both registry construction and UI reject access to datasets;
the UI returns before touching private storage. No cloud sync exists.

## Limits and supported inputs

| Resource | Ceiling |
| --- | --- |
| Uploaded bytes | 10 MiB per file (Streamlit itself also has its server upload limit) |
| Data rows / columns / cells | 20,000 / 100 / 100,000 |
| Cell / column-name characters | 4096 / 128 |
| Total decoded value characters | 2,000,000 |
| XLSX sheets / ZIP entries / expanded bytes | 20 / 1000 / 32 MiB |
| ZIP entry compression ratio | 200:1 |
| Parquet row groups / declared decoded size | 100 / 32 MiB |
| Parquet Thrift string / container limits | 1,000,000 / 100,000 |
| Worker wall time / CPU time (POSIX) | 30 seconds / 20 seconds |
| Worker address space (Linux) | 2 GiB |
| Worker output / output file | 16 MiB |
| Sample shown | 10 rows × 10 columns × 120 characters |
| Dictionary entry | 1000 characters each for description and units |

CSV requires a nonempty unique header and consistent row widths, UTF-8 (optional
BOM), comma delimiter and standard CSV quoting. Unsupported encodings fail explicitly;
there is no encoding guessing. XLSX requires an explicit sheet and a header in its
first row. Trailing missing worksheet cells are padded. Macros, encrypted packages,
external-link parts and extreme compression are rejected. Formula cells use only
stored cached values and may appear missing if no cached value exists. No formula
recalculation, formatting or merged-header interpretation is performed. The original
workbook and selected sheet identity are retained.

Parquet accepts scalar integers, floating point, decimals, booleans, strings, dates
and timestamps. Nested, binary, dictionary/extension and other complex types are
rejected rather than silently coerced. Selected-sheet XLSX parsing is bounded;
other sheets are retained in the immutable workbook but are not profiled.

## Statistical meaning and limitations

Types are inferred over the entire bounded selected table: finite numeric values,
ISO temporal values, categorical dimensions (at most 50 distinct values, each at
most 128 characters), otherwise text. Booleans are categorical. Mixed numeric/text
columns have an ambiguity warning and no numeric statistics. Leading-zero numeric
strings are flagged as possible identifiers. All-missing columns have unknown type.
Empty/whitespace cells, native nulls and native nonfinite floats count as missing;
literal CSV `NA`, `NaN` and `null` strings remain values. Duplicate counts compare
whole rows with scalar type identity; imports never remove duplicates.

Numeric statistics use finite Python floats: count, missing count/fraction, mean,
median, sample standard deviation (`ddof=1`; null for fewer than two observations),
min/max and quartiles with linear interpolation at `(n-1)*q`. Float conversion may
lose precision for large integers and decimals; this release is not exact decimal
accounting. Extreme numeric ranges that overflow arithmetic fail with a request to
rescale. Category counts include scalar type prefixes to avoid value collisions.
Text and temporal columns receive counts/missingness only. Outputs contain the
source SHA, dataset ID/version, selected columns, parser options, explicit statistical
parameters, Python/pyarrow/openpyxl/profile versions and UTC timestamp. Repeated
calculations have identical statistical payloads for the same inputs/software;
run IDs and timestamps differ. No tests, confidence intervals, regression,
prediction, inference or AI mathematical calculation are supplied.

This is a local application, not an adversarial sandbox or encrypted vault. The
worker provides timeout/CPU/application bounds and Linux address-space limits;
macOS does not enforce a hard worker address-space ceiling. Native parser bugs and
same-user filesystem attacks remain outside the isolation guarantee. The parser
has no networking logic, but no OS network sandbox is installed. Keep dependencies
updated and do not expose the local Streamlit server to untrusted users. Streamlit
holds uploaded bytes in memory; checks precede further parsing/copies, and accepted
tables are materialized only inside the documented ceilings. No streaming import
of larger tables, concurrent-user quotas, arbitrary SQL, deletion or automatic
cleanup is included. Inventory and saved runs can grow on disk over time.

Pyarrow is a substantial native wheel (tens of MiB, platform dependent); it is used
only for Parquet, not pandas. Openpyxl and defusedxml were already used by document
ingestion. Pyarrow is constrained to `>=19.0.1,<27`; all supported runtimes must have
a compatible wheel. Standard library SQLite and statistics add no dependencies.

## Synthetic demo and verification

All checks use temporary workspaces, generated CSV/XLSX/Parquet, and synthetic text.
No private source or live paid provider is required. To generate example files:

```sh
PYTHONPATH=.:tests python -c "from pathlib import Path; from test_datasets import CSV,workbook,parquet; p=Path('/tmp/secondself-synthetic'); p.mkdir(exist_ok=True); (p/'study.csv').write_bytes(CSV); (p/'book.xlsx').write_bytes(workbook()); (p/'arrow.parquet').write_bytes(parquet())"
```

Use a fresh temporary DATA_DIR for manual trials, then preview and confirm these
files in Datasets. The workbook contains `First` and `Second`; the CSV includes
missing, repeated and mixed-type values. Import the same CSV again to see dedup,
then change a measurement while retaining the dataset name to see versioning.

```sh
PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true python -B -m unittest discover -s tests -p 'test_*.py' -v
python -m pip install 'playwright>=1.50,<2'
python -m playwright install chromium
# Set SECONDSELF_TEST_CHROME to Chromium's executable if Chrome is not installed.
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true python -B tests/browser_dataset_check.py
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true python -B tests/browser_document_check.py
PYTHONPATH=.:tests PYTHON_DOTENV_DISABLED=1 DEPLOY_MODE=true python -B tests/browser_demo_check.py
```

CI runs the full unit/integration suite and real Chromium dataset, document and graph
checks. The graph regression fetches the existing pinned public rendering library;
dataset imports do not fetch anything. The document browser regression mocks provider
responses and checks the existing explicitly consented Ask behavior.

### Validation on 2026-10-17

- Full regression: 108 tests passed (93 existing and 15 dataset contract tests),
  with no skips, using Python 3.14 and pyarrow 26 locally.
- Real Chrome dataset acceptance: preview/confirm; valid CSV, sheet-selected XLSX
  and Parquet; deduplication/versioning; missingness/ambiguities; dictionary edits;
  saved statistics; reprofile; persistence across reload; all workspace views.
- Existing document browser regression passed: malformed PDF, PDF/CSV/XLSX previews
  and imports, deduplication, failed-index retry, Ask provenance/consent and imported
  evidence in Library/Graph/Insights.
- Existing graph browser regression passed: empty/populated graphs, filters, actual
  canvas node click and script-injection rendering checks.
- Existing Insights browser regression passed with synthetic notes and real local
  Ollama: generation, evidence, review persistence, restart, staleness and navigation.
- Whitespace checks and Python compilation passed. CI uses Python 3.11 on Linux;
  its results are reported on the draft PR, separately from local verification.

Storage targets Linux/macOS POSIX local filesystems. Windows and network-filesystem
atomicity/permission semantics are not supported by this implementation. Uploaded
Markdown-like column names are escaped before rendering expander labels.
