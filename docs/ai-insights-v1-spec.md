# AI Insights — implementation specification (v1)

## User goal
Turn verified SecondSelf notes into reviewable **candidate** insights: missing evidence, potential contradictions, and non-obvious connections. This is not an autonomous decision-maker and must never silently edit notes or create tasks.

## Product
Add sixth workspace view **Insights**, with:
- Generate Insights button (never run automatic billable cloud calls on page load or after every refresh).
- Scope selector (all notes or PARA category), count cap (maximum 10 candidates per run), and a local-only default.
- Cards with type, short claim, rationale, source note IDs/titles and clickable/inspectable evidence excerpts, limitations, suggested question/action, and status: New, Useful, Dismissed, Needs investigation.
- Persist reviewed insights locally under gitignored data/ storage, associated with knowledge generation/source fingerprints. Preserve feedback across reruns, flag stale after notes change, and avoid duplicate suggestions.
- Empty/small corpus, missing model, provider unavailable, malformed metadata, and stale generation should be handled clearly. In particular with only two notes do **not** manufacture trends or contradictions.

## Analysis
- Scope only the verified active generation and canonical note metadata; never index draft/raw/unsafe content.
- Deterministic candidate generation before interpretation: metadata coverage checks; near-neighbor cosine candidates with provenance; potential conflicts via conservative comparable-entity/field/date heuristics rather than treating semantic similarity as a contradiction.
- Local-only default: produce evidence-backed candidates without xAI. Optional cloud-assisted synthesis may use existing xAI provider but must require a separate explicit, informed action indicating excerpts leave device and may cost money. Never submit unbounded full corpus; bound evidence and token sizes.
- Anchor each insight to verbatim note excerpts, IDs, fingerprints, generation ID, and clearly label **hypothesis** vs observed evidence. Do not claim a fact merely because an LLM wrote it.
- Do not fabricate missing documents: knowledge gaps represent missing information **within indexed notes**, not verified gaps in the real world.
- A relationship suggestion must justify more than generic topical overlap.

## Engineering
- Reuse app.py, workspace.py, refresh.py graph and vector provenance, verified generation APIs; avoid rebuilding embeddings and do not weaken the freshness gate.
- UI must be responsive, accessible, and follow existing theme. In DEPLOY_MODE no private writes, no cloud calls or privileged local reads.
- No new paid API calls or deployment during automated tests.
- Synthetic tests: new/missing/stale generation, note deletion/edits, unsupported claims, evidence citations, duplication, review persistence, security boundary, provider failure and 2-note no-fabrication.
- Existing unit/browser suites must pass; include user-facing docs and reproducible local test.
- Keep private knowledge and API secrets uncommitted. Do not modify the demo dataset. No auto-merge.

## Acceptance demonstration
Create 4-6 **synthetic** notes with explicit overlapping entities and differing stated terms; refresh using local Ollama. Open Insights, generate, review evidence, mark a candidate Useful and one Dismissed, restart UI and see persisted states, edit an underlying note and see stale warning. Verify Ask, Capture, Library and Explore still work.
