# AI Insights v1

Open **Insights**, select all notes or a PARA category, choose 1–10 candidates,
then click **Generate Insights**. Generation is local and never edits notes or
creates tasks. A successful verified refresh is required. Existing Ollama vectors
are reused; generating insights makes no embedding requests.

Expand a source title/ID to inspect its verbatim excerpt and fingerprint. Cards
show the verified generation, rationale, uncertainty and a suggested next step.
Select New, Useful, Dismissed or Needs investigation, then click **Save review**.
The saved-status label confirms the persisted decision. Decisions and
source evidence persist in gitignored `data/insights/reviews.json` across UI
restarts. Preserve this file when moving a workspace. A duplicate candidate keeps
its review status. Changed evidence produces a new candidate; previous evidence
and decisions remain visible with a stale warning. Any generation change marks
old cards stale, including changes elsewhere in the corpus.

## What v1 can support

- Gaps are observed missing tags or creation dates in canonical metadata. They
  describe only indexed notes, never missing documents or real-world knowledge.
- Potential contradictions require explicit lines in the format below, with the
  same entity, field and date and different literal values. These are hypotheses;
  versions, corrections and context can explain the difference.
- Connections require the same explicit entity/date, complementary fields, cosine
  similarity of at least 0.82 and no existing explicit link. Generic topical
  similarity alone produces no suggestion.

```text
Atlas | retention | 2026-01-01: 30 days
Atlas | owner | 2026-01-01: Mira
```

Unstructured prose is not interpreted as a factual conflict. With fewer than
three scoped notes only metadata observations are offered. No candidates is a
valid result. This conservative grammar intentionally trades recall for evidence
that a person can inspect. Candidates are not validated facts.

Generation checks at most 500 scoped notes, the first 12,000 body characters and
30 structured facts per note, and five nearest subsequent neighbors per note.
Select a smaller category above 500 notes. The UI offers at most ten candidates
per run; retained history can contain more. Refresh a missing/stale index through
the existing approved refresh workflow. Missing Ollama models or an offline
server must be fixed before refresh can publish a verified generation. Invalid
metadata blocks generation rather than silently analyzing a partial corpus.

## Optional xAI processing

The default requires no cloud provider. Each card has a separate authorization
checkbox stating that excerpts leave the device and may cost money, followed by
an explicit send button. This sends only that card's first two excerpts, at most
600 characters each (payload capped at 3,000 characters), to the configured xAI
model. Output is capped at 20 tokens, with a 20-second timeout and no retries.
xAI can select one of three predefined review questions; arbitrary model prose
is rejected. It cannot add claims, evidence or citations. Stale cards cannot be
sent. Failures preserve all local evidence and decisions. No cloud processing
runs on page load, generation, review or refresh. Real xAI behavior is untested
here to avoid paid calls. Insights are disabled in DEPLOY_MODE and for demo data.

## Reproduce validation

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
# Requires local Ollama with nomic-embed-text and installed Chrome:
.venv/bin/python tests/browser_insights_check.py
.venv/bin/python tests/browser_demo_check.py
```

The Insights browser check copies code into a temporary isolated workspace,
creates five synthetic notes, performs a real Ollama refresh, opens evidence,
saves Useful and Dismissed reviews, restarts the server, checks persistence,
edits a source, checks stale warnings, and navigates all existing views plus a
mobile viewport. It has empty cloud credentials and never reads personal notes.
The existing browser suite fetches the pinned public vis-network library.
