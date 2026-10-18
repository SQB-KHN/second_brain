# SecondSelf 3.0 — Frontend Modernisation Implementation Plan

**Status:** proposed, implementation not started.  
**Design reference:** https://www.figma.com/design/SSOGo1tHxsRK05k9yhjIAj?node-id=1-2  
**Product intent:** desktop-first research/productivity workspace with a strong mobile experience.  
**Core principle:** implement and validate a fully functional Today before migrating the other workspaces.

## Baseline and constraints
- Existing Streamlit app in `app.py`, Today UI in `today_ui.py`, transactional SQLite planner in `task_service.py`.
- Existing Capture, Ask, Explore, Library, Insights, Datasets and Analyse functionality must remain available throughout migration.
- Maintain local-first ownership of notes, task records, dataset versions, statistical results and references.
- No speculative calendar integration, paid AI calls, network sync or replacement of local data stores.
- Current Figma desktop target is an **editable starting composition, not yet an approved pixel-perfect final source**. Compare/revise it against the user's original reference and current screenshots. Design the mobile reference explicitly.
- The Y2K/Retro UI draft PR #26 is merged into main; do not assume its CSS is the desired frontend implementation.

## Architectural decision
Use **React + TypeScript + Vite** for the interactive visual frontend, supported by a **thin local FastAPI service** over the Python planner engine; keep Streamlit working until migration exit gates pass. Build a single cohesive monorepo, not distributed microservices. Do not introduce a replacement database.

Proposed structure (validate against the repository before creating):
```
frontend/
  src/
    app/                # shell, navigation, routing
    components/         # retro window, icons, capsule, status bar
    features/today/     # today / week / task editor / priority list
    lib/api/            # typed client, error handling
    styles/             # tokens and responsive foundations
  public/               # original or licensed icon assets
service/
  app.py                # thin API assembly
  routes/tasks.py       # task operations only
  schemas.py            # request/response contracts
tests/
  # existing Python tests preserved
  # new API contract + frontend E2E tests
```

## Phase 0 — Figma reconciliation and design specification (1–3 days)
**Deliver:** Figma desktop Today reference at 1440×900; second desktop breakpoint; mobile Today frame at 390×844; colour, typography, spacing, icon and component rules; design-to-code measurement sheet.
- Reconcile Figma against the user's screenshot reference: top OS title bar, compact rail, patterned warm canvas, illustrated activity capsules, real window titlebars, priorities, sticky-note treatment.
- Specify visual behaviours for real/empty/loading/error/overdue/done states and editable forms.
- Establish icon assets with clear license provenance; don't mix unrelated asset packs or copy the example's exact proprietary icons.
- Audit contrast, focus indication, touch target sizes and text wrapping.
**Gate:** user signs off on actual Figma screens and screenshots. No frontend implementation before sign-off.

## Phase 1 — Task API boundary (3–5 days)
**Deliver:** FastAPI adapter that invokes existing `task_service.py` functions; schemas and integration tests.
- Proposed endpoints: GET /api/v1/tasks?from=&to=&tz=; POST /api/v1/tasks; PATCH /api/v1/tasks/{id}; GET /api/v1/projects; PATCH /api/v1/projects/{id}; GET /api/v1/health (non-sensitive).
- Inspect current `Tasks.save`, `Tasks.list`, `for_day`, timezone and optimistic concurrency semantics before defining detailed contracts; do not invent capabilities.
- Keep task ID, update/version checking, datetime parsing, validation, references and SQLite transaction boundaries.
- Local binding to 127.0.0.1 only by default. Explicit allowed origins, protections against cross-site mutations/CSRF, no unauthenticated public binding. If remote/mobile access from another device is needed, design explicit auth/TLS first; avoid assuming localhost is accessible from phones.
- Respect DEPLOY_MODE read-only boundaries; no access to private data in a public demo.
**Gate:** contract tests for create/update/complete, timezones including DST gaps/folds, read-only mode, conflict handling, malicious inputs and persistence. Streamlit continues operating.

## Phase 2 — Frontend and retro system (3–5 days)
**Deliver:** React/TypeScript app with reusable shell and controlled design tokens.
- Build top OS title bar, compact left icon navigation, responsive mobile navigation, retro window container, typography, activity capsules, status and dialogs.
- Desktop rails and panes match Figma. Mobile layout is designed, not simply shrunk; no decorative nonfunctional close/maximise controls.
- Include loading, empty, error and offline indicators; avoid fake time/status displays.
- Keyboard, screen-reader labels, reduced motion and responsive breakpoints.
- Use a cohesive icon set (licensed/original) with 16/32px styles, no unverified remote-font requirements.
**Gate:** Storybook or comparable component fixtures plus screenshot baselines at 1440x900, 1024x768 and 390x844. Visual discrepancies documented.

## Phase 3 — Functional Today vertical slice (5–8 days)
**Deliver:** real timeline and tasks, wired end-to-end.
- Day and week selection, real scheduled times, separate due and unscheduled queues.
- Priority panel from actual incomplete tasks; interactive create/edit/complete/reschedule with validation and persistence.
- Task actions show pending/success/failure and handle optimistic-concurrency conflicts.
- Accessible form/dialog or drawer; advanced fields progressive rather than always visible.
- Use user-selected IANA timezone; no fabricated events; visibly distinguish real tasks from suggestions/demo fixtures.
- Preserve source links and project labels where data contracts support them.
**Gate:** functional E2E tests with synthetic fixture database, restart/persistence verification and no regressions in Python engine.

## Phase 4 — Visual, accessibility, safety acceptance (3–5 days)
**Deliver:** verified Today release candidate.
- Compare Playwright screenshots to approved Figma reference at each target viewport; review visual difference not just test exit status.
- Check task panel geometry, rails, icons, typography, spacing, timeline density, focus and mobile overflow.
- Run automated accessibility checks plus manual keyboard, zoom, touch and reduced-motion checks.
- Confirm localhost binding, request validation, no secret exposure, private-data isolation, and no external calls without consent.
- Preserve rollback to existing Streamlit Today while new frontend is in review.
**Gate:** user visually approves screenshot comparisons; all mandatory tests and CI green; release candidate PR reviewed.

## Phase 5 — Incremental workspace migration (per-slice planning after Today approval)
Migrate in slices, maintaining a one-click route and existing engine:
1. **Research:** Ask + source inspection + Explore; keep citation provenance and explicit external LLM consent. Audit existing provider consent controls before integrating.
2. **Knowledge:** Capture + Library + Insights; preserve import/idempotency, notes/indexing, saved reviews, privacy.
3. **Analytics:** Datasets + Analyse; never replace SciPy/statsmodels computation with generated answers. Preserve dataset version hashes, diagnostics, exports and audit records.
4. **Projects + settings:** only after real API capabilities and information architecture are specified.

Each slice needs its own Figma reference, isolated backend adapter, fixture tests, screenshot approval and draft PR. Do not remove Streamlit routes until feature parity verified.

## Pull-request sequence
- PR A: planning document (this PR).
- PR B: signed-off design tokens and frontend architecture skeleton, only after Phase 0.
- PR C: local task API + tests.
- PR D: frontend UI shell.
- PR E: functioning Today end-to-end.
- PR F: visual acceptance fixes and release readiness.
- Later: one coherent PR per workspace migration, with separate architecture changes only when necessary.

Keep PRs reviewable, maintain `main` as known working state, never merge based solely on CI. All data in screenshots, tests, prototype builds and public demos is synthetic.

## Risks / decisions
- **Visual mismatch:** use actual Figma screenshots and measured component layout as the contract, not CSS approximations.
- **Complexity:** do not introduce SSR or a heavyweight framework just for a local desktop-style SPA; Vite is sufficient until deployment constraints change.
- **Local-vs-mobile:** a web app on another device cannot directly access laptop loopback; remote access requires a separately designed secure setup.
- **Regression:** retain Streamlit as fallback until every migrated capability is accepted.
- **Scope creep:** notifications, calendars, drag/drop multiwindow desktop, OAuth and AI planning are out of scope for Today v1.
- **Project reality:** treat estimated days as capacity planning, not promises.

## Codex starting instruction
First inspect `task_service.py`, `today_ui.py`, `app.py`, existing tests and CI. Do not code the API or frontend yet. Audit the linked Figma design against the user's target screenshot and report missing screens, required components, styling tokens, and interaction states. Propose any contract adjustments for approval. Start implementation only after visual acceptance of Phase 0.
