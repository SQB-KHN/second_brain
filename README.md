# SecondSelf — Local-first AI Knowledge Workspace

**Capture knowledge. Index it privately. Ask grounded questions. Explore connections.**

SecondSelf is an AI-assisted personal knowledge system built with Python and Streamlit. It combines a five-view workspace, structured Markdown notes, a verified local semantic index, an interactive knowledge graph, and optional cloud LLM answer generation.

**Project status:** working local application; not a hosted public product. Private notes remain on the user's machine. A public demo is **not** being claimed here.

[Architecture](docs/portfolio-architecture.md) · [Engineering case study](docs/portfolio-case-study.md) · [Workspace guide](docs/workspace.md) · [Indexing operations](docs/phase2-operations.md)

## Application screenshots

These are real screenshots of the local SecondSelf application, captured using test notes. No live public demo is implied.

| Home | Capture |
| --- | --- |
| ![SecondSelf Home dashboard](docs/media/home.png) | ![SecondSelf note capture](docs/media/capture.png) |

| Library | Knowledge graph |
| --- | --- |
| ![SecondSelf Library](docs/media/library.png) | ![SecondSelf knowledge graph](docs/media/explore.png) |

**Explore — search and filtering**

![SecondSelf Explore filters](docs/media/explore-filters.png)

## What it demonstrates

| Capability | Implementation |
| --- | --- |
| Product design | Home, Capture, Ask, Explore, Library; responsive Streamlit workspace |
| Data workflows | Note creation, editing, drafts, PARA categorization, local persistence |
| Applied AI / RAG | Ollama `nomic-embed-text` semantic embeddings; source-backed retrieval |
| Knowledge discovery | Interactive note graph and semantic relationships |
| Reliability | Transactional generations, fingerprints, freshness checks, recovery |
| API integration | Optional xAI Grok answer generation and optional OpenAI embedding backend |
| Quality engineering | Python tests, browser-based graph safety checks, GitHub Actions |

### Product walkthrough

1. **Capture:** write a titled note, categorize it, and choose Save Draft or **Save & Index**.
2. **Library:** find, review, and edit saved notes.
3. **Explore:** browse the graph of indexed knowledge and connections.
4. **Ask:** retrieve relevant notes locally; optionally generate a cited answer via a configured LLM.
5. **Home:** see recent activity and knowledge status.

> **Privacy boundary:** Ollama embeddings run locally. With xAI configured, question and retrieved note excerpts are sent to xAI for answer synthesis; provider charges may apply. Classification of queued raw captures is separate and deliberately opt-in.

## Architecture at a glance

```text
Local Streamlit workspace
  ├── Capture / Library → Markdown notes (data/wiki/)
  ├── Save & Index → transactional refresh → Ollama embeddings
  │                        ↓
  │                verified generation (index + vectors + graph)
  ├── Explore ← verified graph
  └── Ask → local semantic retrieval → optional xAI Grok answer + sources

Other inputs: links / files → review queue → explicit classification
Public demo: isolated synthetic data, default-deny publication controls
```

Read the [architecture and design trade-offs](docs/portfolio-architecture.md).

## Run locally (macOS)

Requires Python 3.11+, Ollama, and a suitable Python virtual environment. Commands assume this repository is cloned into `~/second_brain`; adapt the directory to your checkout.

```bash
cd ~/second_brain
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Install Ollama separately from https://ollama.com/download/mac
ollama pull nomic-embed-text
curl -s http://localhost:11434/api/tags

python refresh.py status --data-dir data
streamlit run app.py --server.address 127.0.0.1
```

Open **http://localhost:8501** and use Capture → **Save & Index**. The UI indexes notes with Ollama when the service is running; no embedding API key is required.

To use Ask for generated answers, optionally add `XAI_API_KEY` to an untracked `.env`. Do **not** commit keys; the question and retrieved passages leave your machine when invoking xAI.

For command-line indexing and recovery:

```bash
python refresh.py dry-run --data-dir data
python refresh.py refresh --data-dir data
python ask.py "What is SecondSelf?"
```

The final command requires a configured LLM answer provider. See [operations](docs/phase2-operations.md) for legacy migration, external API approvals, and failure recovery.

## Engineering evidence

- **Local integration:** a real Ollama smoke test returned 768-dimensional vectors from `nomic-embed-text`.
- **Functional acceptance:** Save & Index, Library visibility, Explore visibility, and an Ask response with a cited local note were manually verified in development.
- **Automated checks:** a reported 80-test suite and browser checks passed during the daily workspace PR; CI passed for that merged change. These are development checks, **not** independent production quality benchmarks.
- **Delivery history:** [Ollama integration PR #14](https://github.com/SQB-KHN/second_brain/pull/14) and [workspace PR #15](https://github.com/SQB-KHN/second_brain/pull/15).

### Screenshots and short demo

See [portfolio media checklist](docs/portfolio-media.md). Add **actual screenshots** from a synthetic local dataset only after checking for secrets, names, private notes, and identifying paths. Illustrative mockups are not product screenshots. No public URL is advertised until an isolated sample deployment has been verified.

## Engineering approach and attribution

This project was built with **AI-assisted development (Codex)** alongside requirements specification, architectural review, manual acceptance testing, security constraints, and GitHub-based delivery. The case study distinguishes tested behavior from future goals; it does not claim that all code was handwritten.

## Security, privacy, and limitations

- `data/` personal knowledge, generated local indexes, `.env*` secrets, and local logs are excluded from commits by repository ignore rules; **review staged files before every push**.
- Public demo publication is isolated and requires explicit synthetic content approval. No live cloud demo is implied.
- A single-note graph has no semantic edges; usefulness grows with a larger knowledge corpus.
- Search relevance, model hallucinations, multi-user access control, and production-scale performance have not been comprehensively benchmarked.
- The repository does not yet advertise an open-source license. Do not assume reuse rights.

## Tech stack

Python · Streamlit · Ollama · nomic-embed-text · vector similarity search · interactive knowledge graphs · optional xAI Grok/OpenAI · pytest · Playwright · GitHub Actions

## Project documentation

- [Five-view workspace guide](docs/workspace.md)
- [Architecture](docs/portfolio-architecture.md)
- [Case study](docs/portfolio-case-study.md)
- [Portfolio media / demonstration checklist](docs/portfolio-media.md)
- [Verified refresh and operations](docs/phase2-operations.md)
