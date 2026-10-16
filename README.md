# SecondSelf

A self-organising personal AI knowledge system that captures, connects, visualises, and answers using your own accumulated knowledge.

> Not a notes app. Not a chatbot. A brain that organises itself and answers for you.

## What it does

```text
Capture any note / link / file
        ↓
AI classifies & files it (PARA method)
        ↓
AI auto-links related notes (embeddings)
        ↓
Everything renders as a live interactive graph
        ↓
Ask it anything in plain English
        ↓
Answer synthesized from YOUR accumulated knowledge
```

## Quick start

### 1. Prerequisites

- Python 3.11 or newer
- OpenAI API key (for classification, embeddings, and Q&A)

### 2. Install

```bash
cd secondself
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

### 4. Verify setup

```bash
python -c "from config import RAW_DIR, WIKI_DIR; print('Setup OK', RAW_DIR, WIKI_DIR)"
```

### 5. Capture something

**Always run from the `secondself` folder with the virtualenv active:**

```bash
cd secondself
source .venv/bin/activate

# Or use the helper script (no need to activate venv):
./capture.sh --text "My first note"
./capture.sh --file "./samples/meeting-notes.txt"
./capture.sh --list          # see all captures
```

Captures are saved to **`data/raw/`** (not `raw/` at project root).  
The index is at **`data/meta.json`**.

## Project structure

```text
secondself/
├── demo/             # Committed public demo corpus (Streamlit Cloud)
├── data/             # Local personal knowledge (gitignored content)
│   ├── raw/          # Raw captures (Week 1)
│   ├── wiki/         # PARA-organized notes (Week 2)
│   ├── embeddings/   # Vector store (Week 2)
│   └── graph.json    # Graph export (Week 3)
├── logs/             # Pipeline logs
├── capture.py        # Capture CLI
├── classify.py       # Auto-classify
├── link.py           # Auto-link
├── build_graph.py    # Graph.json + Obsidian export
├── render_graph.py   # Interactive graph.html (vis-network)
├── prepare_deploy.py # Build demo/ bundle for cloud
├── export_obsidian.py # Obsidian vault export
├── ask.py            # RAG Q&A
├── app.py            # Streamlit app
├── config.py         # Shared configuration
└── docs/             # Architecture and planning
```

## Documentation

- [Problem statement](docs/problemStatement.md)
- [architecture](architecture.md)
- [Implementation plan](docs/implementation-plan.md)
- [Edge cases](docs/edge-case.md)

## Pipeline commands

```bash
# 1 — capture (use ./capture.sh or activate .venv first)
./capture.sh --text "your note"
./capture.sh --url "https://example.com"
./capture.sh --file "./document.pdf"
./capture.sh --list
./capture.sh --rebuild-meta   # fix index if out of sync

# 2 — classify (scanner ready; LLM classification in tasks 2.2+)
./classify.sh --scan-only
./classify.sh

# 2 — link (embed + auto-link)
./link.sh --embed-only
./link.sh --link-only
./link.sh --threshold 0.85
python link.py                    # also exports Obsidian vault
python link.py --no-obsidian        # skip vault export

# 3 — graph + Obsidian + visualization
python build_graph.py --scan-only   # walk wiki + parse frontmatter (Phase 4.1)
python build_graph.py               # graph.json + graph.html + Obsidian vault
python build_graph.py --no-semantic # explicit edges only
python build_graph.py --threshold 0.85
python build_graph.py --no-html     # skip graph.html generation
./build_graph.sh
python render_graph.py              # regenerate graph.html only
./render_graph.sh
open graph.html                     # or: python -m http.server 8000
python export_obsidian.py         # vault only (no graph.json)
./export_obsidian.sh
# Week 4 — ask + Streamlit app
./ask.sh "What projects am I working on?"
python ask.py "What do I know about PARA?" --top-k 5
streamlit run app.py              # http://localhost:8501
```

## Local web app (Phase 7)

```bash
cd secondself
source .venv/bin/activate

# Index your notes first (required for Ask)
./link.sh
./build_graph.sh

# Launch Streamlit UI (graph + ask)
streamlit run app.py
```

Open **http://localhost:8501** — graph on top, ask bar below, **Refresh brain** in the sidebar.

Requires:
- `OPENAI_API_KEY` for embeddings (`link.py`) and optionally for RAG answers
- `GROQ_API_KEY` works for RAG answers if OpenAI is not set for chat

## Deploy to Streamlit Cloud (Phase 8)

### 1. Prepare the demo bundle

Public deploy uses the committed `demo/` folder (sample notes only — never your private `data/`).

```bash
cd secondself
source .venv/bin/activate

# Build only explicitly approved sample notes
python prepare_deploy.py
# or: ./prepare_deploy.sh
```

`demo-manifest.json` defaults to an empty approval list. After reviewing the entire
sample (including frontmatter, URLs, and metadata), add an entry with `path`
(relative to `data/wiki/`, e.g. `resources/synthetic-example.md`) and `sha256`
(the SHA-256 digest of the exact file bytes). Changed samples need renewed review
and approval. Do not approve private notes or reuse hashes without review.

The publisher reads only listed notes, rebuilds the index and explicit graph,
and replaces `demo/` only after staging validation. Missing or changed samples,
excluded wiki references, and local Markdown artifact links fail closed.
Embeddings are intentionally omitted until a separate provenance-safe build is
available; demo Ask will report that the brain is not indexed. `--skip-rebuild`
is accepted for backwards compatibility, issues a deprecation warning, and still
performs validated rebuilding of the graph and index. The root `graph.html` and
private pipeline are untouched.
Use `--source`, `--dest`, and `--manifest` for isolated local builds. Run only one
publisher per destination, with source/manifest files held stable during the build.

Existing committed demo data is **not retroactively approved** by this change.
Review a newly generated bundle before any separately authorized publication.
See [the design and readiness review](docs/secure-demo-publication.md).

### 2. Streamlit Cloud settings

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Repository: `SQB-KHN/second_brain` (or your fork)
3. **Main file path:** `app.py`
4. **Secrets** (copy from `.streamlit/secrets.toml.example`):

```toml
DEPLOY_MODE = "true"
OPENAI_API_KEY = "sk-..."
GROQ_API_KEY = "gsk-..."
ENABLE_CAPTURE = "true"
ENABLE_REFRESH_BRAIN = "false"
ASK_RATE_LIMIT = "10"
```

5. Deploy → open the public URL

### 3. Environment variables

| Variable | Local | Cloud | Purpose |
|----------|-------|-------|---------|
| `OPENAI_API_KEY` | `.env` | Secrets | Embeddings + optional RAG |
| `GROQ_API_KEY` | `.env` | Secrets | Classify + RAG (alternative) |
| `DEPLOY_MODE` | `false` | `true` | Read `demo/` instead of `data/` |
| `ENABLE_CAPTURE` | `true` | `true` | Show capture box (`false` to hide on public demo) |
| `ENABLE_REFRESH_BRAIN` | `true` | `false` | Disable pipeline on public URL |
| `ASK_RATE_LIMIT` | `10` | `10` | Questions per minute |

### 4. Post-deploy checks

- [ ] Graph shows 13+ demo nodes
- [ ] Hover and click work on nodes
- [ ] Ask returns an answer with sources (requires embeddings in `demo/`)
- [ ] No personal notes exposed
- [ ] `git grep -i "sk-\|gsk_"` shows no real keys

### Live demo URL

_Add your Streamlit Cloud URL here after deploy._

## License

Personal project — add a license before public release.
