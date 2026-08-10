# SecondSelf

A self-organizing personal AI knowledge system that captures, connects, visualizes, and answers using your own accumulated knowledge.

> Not a notes app. Not a chatbot. A brain that organizes itself and answers for you.

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
├── data/             # All knowledge storage
│   ├── raw/          # Raw captures (Week 1)
│   ├── wiki/         # PARA-organized notes (Week 2)
│   ├── embeddings/   # Vector store (Week 2)
│   └── graph.json    # Graph export (Week 3)
├── logs/             # Pipeline logs
├── capture.py        # Week 1 — capture CLI
├── classify.py       # Week 2 — auto-classify
├── link.py           # Week 2 — auto-link
├── build_graph.py    # Week 3 — graph.json
├── ask.py            # Week 4 — RAG Q&A
├── app.py            # Week 4 — Streamlit app
├── config.py         # Shared configuration
└── docs/             # Architecture and planning
```

## Documentation

- [Problem statement](docs/problemStatement.md)
- [Architecture](docs/architecture.md)
- [Implementation plan](docs/implementation-plan.md)
- [Edge cases](docs/edge-case.md)

## Pipeline commands

```bash
# Week 1 — capture (use ./capture.sh or activate .venv first)
./capture.sh --text "your note"
./capture.sh --url "https://example.com"
./capture.sh --file "./document.pdf"
./capture.sh --list
./capture.sh --rebuild-meta   # fix index if out of sync

# Coming in later phases
python classify.py
python link.py
python build_graph.py
python ask.py "What do I know about X?"
streamlit run app.py
```

## License

Personal project — add a license before public release.
