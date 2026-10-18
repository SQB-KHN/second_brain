# SecondSelf — Today v1: local timeline and priorities

## Product decision
The timeline-first design prototype in `docs/prototypes/timeline-studio-v2.html` (PR #24) is approved as visual direction. Implement a **functional local Today view** in the existing Streamlit app, without replacing its backend or pretending mobile/browser features already exist. Today becomes the startup/default view; Research (existing Ask/Library/Explore) and Analytics (Datasets/Analyse) remain one click away. Preserve all existing eight features and browser test selectors.

## MVP acceptance contract
1. Introduce local, private, immutable-ID task records: title, details, status (todo/doing/done), priority, scheduled start/end (optional), due date (optional), timezone identifier, project (optional label), related local knowledge/dataset/analysis references (optional, validated), recurrence (not in v1), creation/update timestamps and schema version. Distinguish **scheduled**, **due**, and **unscheduled** tasks—never manufacture scheduled times. Do not pull tasks from source notes without explicit confirmation.
2. Implement a small task service (SQLite with transactional migrations and constrained writes, or equally robust local storage), in the configured private DATA_DIR. Enforce file/directory permissions where POSIX supports them; deny symlinks/path escape; gitignore data. Writes disabled in DEPLOY_MODE. No network or paid API calls.
3. Today UI: day picker, visually differentiated schedule/time rail, ordered priority section, create/edit/complete/reschedule actions, day/week toggle. Use CSS based on v2 visual tokens, but keep forms readable and keyboard accessible. A week view can be a calendar/list if reliable drag-and-drop is out of scope; avoid claims of working drag/drop. Responsive on desktop/mobile.
4. New task form must support unscheduled tasks without asking for fictitious times. Use timezone-aware parsing; validate scheduled end after start, prevent invalid dates, and handle daylight-saving ambiguity explicitly. Source-of-truth is local task records. Use safe plain text for untrusted task fields.
5. Project and task statuses should be real persisted records. Save all changes atomically and record timestamp/status history for audit/recovery. No deletion in MVP; optional archive action with explicit confirmation.
6. Reuse existing `st.session_state.view` patterns. Update existing Streamlit routes so Today is the initial/default view; keep navigation for Home/Capture/Ask/Explore/Library/Insights/Datasets/Analyse accessible (do not silently remove existing views). Prefer not to change unrelated business logic.
7. Data safety: no real calendar connection, reminders, notifications, background sync, external OAuth or automatic xAI suggestions in v1. In read-only demo, render synthetic Today examples only and never touch private storage. Consent and privacy of existing Ask/import flows unchanged.
8. Automated tests: task lifecycle, date/time/timezone edge cases, migration, registry failures and transaction recovery, no writes in demo, no leaking private task details, sorting and priority, persistence across restart, backward compatible navigation. Add real browser Today tests with isolated synthetic data and retain all existing unit/graph/document/dataset/Analyse/Insights suites.
9. Documentation: user guide, limits, privacy, local backup, safe recovery, synthetic setup and architecture. Update README accurately and only claim functionality proven by tests.
10. Deliver one coherent implementation branch and one draft PR against main, full checks, no merge/deploy without review. Do not commit user personal data.

## Visual acceptance standards
Keep editorial typography, soft blush/paper backgrounds, activity colours by category, time as primary content, warm low-noise typography, and distinct desktop/mobile navigation. Do not clone proprietary artwork. Prioritise polished **day timeline** and **three priorities**; Research and Analytics remain reachable in one click. Test narrow (390px) and wide (1440px) viewports.

## Development checkpoints
A. Real local task model and tests.
B. Functional Today interface and navigation preserving old features.
C. Responsive polish and browser acceptance.
D. Documentation, CI, draft PR, user review.
