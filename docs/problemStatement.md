# SecondSelf — Your Personal AI Second Brain

## Problem Statement

Every notes app fails the same way: you capture hundreds of notes, bookmarks, PDFs, and ideas — and then you never find them again. Information goes in, but nothing comes back out.

Notes sit in folders nobody re-reads. Bookmarks pile up unread. Knowledge doesn’t compound.

**Goal:** Build an end-to-end system where you can capture anything (a note, a link, a file), have AI automatically classify and file it, auto-link it to related knowledge, render it as a live interactive graph you can explore, and — most importantly — ask it any question in plain English and get an answer synthesized from your own accumulated knowledge. Then deploy it to a public URL anyone can open.

> Not a notes app. Not a chatbot. A brain that organizes itself and answers for you.

---
# Final System (4-Week Build)

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
        ↓
Deploy to a public URL
```

---

# Weekly Milestones

## Week 1 — The Archivist: Capture Everything, Lose Nothing

### Problem

Ideas, links, files, and notes are scattered across apps, browser tabs, and memory. Build one command that captures anything into one place.

### Build

* Create the project structure:

  * `raw/` — all raw captures
  * `wiki/` — organized notes (used later)
* Write a Python capture script that stores:

  * timestamp
  * unique ID
  * raw content
* Test with **10+ real personal notes/links/files**

### Deliverable

* One-command capture pipeline
* `raw/` populated with 10+ real captures
* **Badge:** The Archivist

### Acceptance Criteria

* [ ] `raw/` and `wiki/` folders exist
* [ ] One command captures a note, link, and file
* [ ] Every capture contains timestamp + unique ID
* [ ] 10+ real items captured

---

## Week 2 — The Librarian: Teach AI to Organize

### Problem

Raw captures are still a pile of information. Make AI organize them automatically.

### 2.1 Auto-Classify (The Sorting Hat)

For every capture, generate:

* PARA category

  * Projects
  * Areas
  * Resources
  * Archives
* Tags
* One-line summary

### 2.2 Auto-Link Related Notes (Connect the Dots)

* Generate embeddings
* Compare new captures with existing notes
* Automatically insert links when similarity exceeds a threshold

### Deliverable

* Self-organizing `wiki/`
* Auto-classification + auto-linking
* **Badge:** The Librarian

### Acceptance Criteria

* [ ] Automatic category
* [ ] Automatic tags
* [ ] Automatic summary
* [ ] PARA working
* [ ] Embeddings computed
* [ ] Related notes linked automatically
* [ ] 15+ real items organized

---

## Week 3 — The Cartographer: Visualize the Brain

### Problem

Knowledge is organized but invisible. Turn it into an interactive graph.

### 3.1 Graph Data Model

* Read every note
* Extract links
* Build:

  * Nodes
  * Edges
* Export JSON

### 3.2 Interactive Graph

Use **vis-network** or **Cytoscape.js**.

Features:

* Force-directed layout
* Hover popups
* Drag
* Zoom
* Animated / alive nodes

### Deliverable

* Interactive knowledge graph built from real notes
* **Badge:** The Cartographer

### Acceptance Criteria

* [ ] Nodes generated
* [ ] Edges generated
* [ ] JSON exported
* [ ] Hover works
* [ ] Drag works
* [ ] Zoom works
* [ ] Built from real notes

---

## Week 4 — The Oracle: Ask It Anything

### Problem

A graph is useful, but answers are the goal.

### 4.1 Natural Language Search

Implement `ask()` using:

* Embeddings
* Retrieved notes
* LLM synthesis

### 4.2 Streamlit App

Create one application containing:

* Interactive graph
* Ask-anything search bar

Deploy to:

* Streamlit Cloud
* Hugging Face Spaces

### Deliverable

Complete **SecondSelf** system deployed publicly.

**Badge:** The Oracle

### Acceptance Criteria

* [ ] Retrieval-augmented Q&A works
* [ ] Graph inside Streamlit
* [ ] Search inside Streamlit
* [ ] Public URL deployed
* [ ] End-to-end pipeline functional

---

# Final Deliverables

* [ ] Public GitHub repository
* [ ] Clean README
* [ ] Setup instructions
* [ ] Live deployed URL
* [ ] Verified end-to-end flow:

  * Capture
  * Classify
  * Link
  * Graph
  * Ask
* [ ] All four weekly milestones complete

---

# Suggested Repository Structure

```text
secondself/
├── raw/                    # Week 1: raw captures
├── wiki/                   # Week 2: organized notes
├── capture.py              # Week 1
├── classify.py             # Week 2
├── link.py                 # Week 2
├── build_graph.py          # Week 3
├── graph.json              # Week 3
├── ask.py                  # Week 4
├── app.py                  # Week 4
├── requirements.txt
└── README.md
```

---

# Recommended Build Order

1. Scaffold repository
2. `capture.py`
3. `classify.py`
4. `link.py`
5. `build_graph.py`
6. Graph visualization
7. `ask.py`
8. `app.py`
9. Deploy
10. Write documentation

---

# AI Tools

* Cursor
* Google Antigravity IDE
* Qoder
* Devin
* VS Code + Claude

---

# Documentation Files

Create the following documentation files:

```text
docs/
├── problemStatement.md
├── architecture.md
├── implementation-plan.md
└── edge-case.md
```

## Required Documents

### problemStatement.md

Store the project problem statement.

### architecture.md

Describe **how the system will be built**.

### implementation-plan.md

Create a phase-wise implementation plan.

### edge-case.md

Store all corner cases and edge scenarios.

---

# Implementation Phases

* Phase 0 — Setup
* Phase 1 — Capture Pipeline
* Phase 2 — Classification
* Phase 3 — Auto-Linking
* Phase 4 — Graph Construction
* Phase 5 — Graph Visualization
* Phase 6 — Local Testing
* Phase 7 — Integration Testing
* Phase 8 — Deployment
* Phase 9 — Final Validation

---

# Prompt Sequence

1. Generate a detailed architecture using `PROBLEM_STATEMENT.md`
2. Save it into `architecture.md`
3. Generate `implementation-plan.md`
4. Generate `edge-case.md`
5. Implement **Phase 0** from the implementation plan

---

**Project Name:** SecondSelf

**Vision:** A self-organizing personal AI knowledge system that captures, connects, visualizes, and answers using your own accumulated knowledge.
