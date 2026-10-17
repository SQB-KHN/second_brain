# SecondSelf workspace

Run `streamlit run app.py` from the repository's virtual environment. The sidebar opens Home, Capture, Ask, Explore, and Library. Appearance switches between light and dark; the sidebar collapses on small screens. Controls have text labels and visible keyboard focus.

- **Home:** note/connection/category counts, recent notes, and shortcuts.
- **Capture:** Markdown editor, explicit PARA category and comma-separated tags. Current text survives view changes. Keep session draft stores several drafts; Open draft restores one and New draft clears the editor. These drafts are session memory, not durable backups. Save & Index writes canonical Markdown with a stable ID, then publishes through the existing transactional verified-generation refresh. No classification service is required for manually categorized text.
- **Ask:** session conversation with cited note titles, categories, relevance scores, and summaries. Existing xAI/Grok, OpenAI and Groq synthesis and Ollama/local embedding behavior remains in the backend. Questions and retrieved excerpts leave the machine for the configured synthesis provider.
- **Explore:** large interactive graph, search/category/tag filters and keyboard-accessible full-note details below the graph. The embedded graph retains its own controls and node details. Its vis-network dependency loads from the existing CDN; an offline browser can still use Library and note details.
- **Library:** search title/text/tags, filter by category and tags, read and edit notes. Edits preserve identity, links, category and metadata. Concurrent changes are rejected; Reload from disk explicitly reloads the editor. Editing the category/moving notes remains a filesystem operation.

## Save, indexing and recovery

Successful Save & Index updates the graph and the same verified vectors used by Ask. The editor resets only after successful publication. If embedding fails, the canonical note remains saved and the UI offers Retry indexing; retry does not create another note. Graph and Ask retain the existing fail-closed freshness behavior while a saved change is unindexed. You can read the saved text in Library.

Ollama must be available with the configured model. External embedding providers still require plan digest and cost approval; the UI does not bypass these gates. If needed, run the approved CLI workflow in [phase2-operations.md](phase2-operations.md), then retry/refresh. Legacy migration also keeps its existing explicit approval requirement. A refresh may index other pending canonical notes as part of the same generation.

Demo mode is read-only for capture, import, editing and refresh even if capture flags are enabled. Demo data is never edited by this interface. Local writes require both ENABLE_CAPTURE and ENABLE_REFRESH_BRAIN. Imports of links/files retain the existing raw inbox workflow and require separate classification and refresh; the UI labels this distinction.

## Validation

`python -m unittest discover -s tests -q` includes isolated Streamlit AppTest navigation/chat/demo tests, draft retention, provider failure/retry, and synthetic save/edit → verified graph → cited Ask retrieval tests. Browser verification uses a temporary source copy and only committed demo content, with desktop and mobile viewports. No personal corpus or credentials are needed. Tests fake provider responses; they do not verify a live Ollama or Grok service.
