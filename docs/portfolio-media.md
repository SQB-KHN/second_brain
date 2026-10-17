# Portfolio media and demonstration plan

No screenshots or video are included in this PR because the actual local application runs on the user's Mac and may show private knowledge. **Do not fabricate screenshots or publish illustrative stock mockups as real app output.**

## Capture real product evidence

Use a **synthetic-only** local note set, with no names, private work material, real client details, secrets, or identifiable file paths visible.

Record 4–5 screenshots:
1. Home — working application and navigation.
2. Capture — synthetic titled note before saving.
3. Library — saved note, category and indexing status.
4. Explore — graph with at least two synthetic notes; single-note graphs have no relationships.
5. Ask — synthetic question and source-grounded response; confirm no API key/logs are on screen.

Recommended file names: `docs/media/home.png`, `capture.png`, `library.png`, `explore.png`, `ask.png`. When files have been carefully reviewed and added, link them from README.

## 60–90 second demo script

- 0–10s: state the problem and open SecondSelf.
- 10–30s: capture a synthetic note and Save & Index.
- 30–45s: show Library and verified indexing.
- 45–60s: open Explore and inspect the note and links.
- 60–80s: ask a question, inspect the source citation, and explain local embeddings versus external answer synthesis.
- 80–90s: show repo's tests and architecture documentation.

## Before publishing

- Inspect every frame for secrets, personal notes, team IDs, browser tabs, local paths and notifications.
- Confirm the Git diff does not include `.env`, `.env.save`, local `data/`, logs or unexpected binary files.
- Ensure demo sample content was explicitly approved and cannot leak private knowledge.
- Do not claim a live public demo URL or hosting arrangement before it exists.
