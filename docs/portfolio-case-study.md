# Engineering case study — SecondSelf

## Problem

Research, project decisions, meeting notes, and scattered references become difficult to retrieve over time. Ordinary notes storage does not by itself provide reliable semantic retrieval or source-grounded answers. The objective was a personal application that keeps knowledge editable locally while making it searchable and navigable.

## Goals and measurable acceptance criteria

- Capture or edit a note in the browser without terminal commands.
- Preserve raw notes even if embedding generation fails.
- Generate embeddings locally and keep provider/model provenance consistent.
- Retrieve a relevant note and provide an answer with an identifiable source when an answer provider is explicitly configured.
- Display the same verified knowledge in Library/Explore and retrieval workflows.
- Prevent personal notes and credentials from entering the public demo by default.

## Iterative implementation

**First: baseline and security.** The application separated local personal data from publishable demonstration material. A default-deny sample manifest and browser graph safety tests were introduced.

**Second: consistency and provenance.** Note fingerprints, embedding provenance, transactional generations, a freshness gate, and recoverable refresh were introduced. Stale or mixed embeddings cannot silently form a valid active generation.

**Third: local-first indexing.** Ollama's `nomic-embed-text` became the default embedding backend for both notes and query vectors. A local smoke test returned vectors with 768 dimensions; optional OpenAI embeddings remained a separate explicit path.

**Fourth: daily usability.** The interface expanded into Home, Capture, Ask, Explore, and Library. A saved note can be indexed through the UI and become visible without manually editing Markdown or invoking scripts.

## Technical competencies demonstrated

- **Requirements and workflow design:** turning an ambiguous “second brain” concept into verifiable user journeys.
- **Python/data engineering:** structured notes, indexing, vector provenance, transactional file-based generations, recovery.
- **Applied AI:** local embeddings, semantic retrieval, optional retrieval-augmented answers through xAI.
- **Security-conscious product design:** loopback usage, opt-in cloud transfer, untracked personal datasets and secrets, synthetic demo boundaries.
- **Delivery and QA:** separate feature branches, code review via pull requests, CI, automated tests, browser tests, and manual acceptance checks.

## Evidence and limitations

- [PR #14 — local Ollama integration](https://github.com/SQB-KHN/second_brain/pull/14).
- [PR #15 — five-view workspace](https://github.com/SQB-KHN/second_brain/pull/15).
- The developer reported 80 passing automated tests and browser checks for the workspace work; GitHub CI passed.
- Manual acceptance included adding a note, seeing it in Library and Explore, and asking a sourced question.

These are evidence of a functioning **local prototype**, not proof of production scale, measured recall accuracy, enterprise privacy certification, or full production deployment.

## Development process and attribution

The implementation used **Codex AI-assisted coding**. The project demonstrates system specification, feature prioritization, integration decisions, operational validation, test interpretation, and iteration with AI tooling. Individual code authorship should not be overstated.

## Next evaluation

With a consented, synthetic benchmark corpus: compare retrieval relevance, citation correctness, indexing latency, draft usability, and error recovery across note volumes. Publish measured outcomes only after running and documenting reproducible experiments.
