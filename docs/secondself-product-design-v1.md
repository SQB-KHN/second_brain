# SecondSelf — Responsive Product Prototype v1

## Purpose
Explore the next user experience **before** changing the existing Streamlit application. The chosen direction is a **desktop-first research and productivity workspace with an excellent mobile experience**. The product should be calm for capturing and organising ideas, precise for research and statistical analysis, and practical for prioritising work.

## Open the prototype
Download or clone the repository, then open `docs/prototypes/secondself-concept-v1.html` in a browser. Use the desktop sidebar or mobile bottom navigation to switch among **Overview**, **Research**, **Analytics**, and **Today**. The link hash also selects a view (for example, `#analytics`). No build step, API key, data import, network service, server, or database is required.

All metric counts, references, charts, timelines and source names are **illustrative sample content**. The prototype is not wired to real SecondSelf data, statistics, calendar or task storage.

## Concept-to-current-product mapping
| Proposed design mode | Existing implementation | Planned improvement |
|---|---|---|
| Overview | Streamlit Home, Capture, Insights | Better cross-workspace orientation, quick capture, recent evidence and verified health |
| Research | Ask, Library, Explore, Document Ingestion | Three-panel question, source list and provenance inspector; user-controlled external AI consent |
| Analytics | Datasets, Analyse | Guided dataset/version selection, method configuration, diagnostics, provenance, results and exports |
| Today | No persisted task/calendar product exists | Later: explicit task storage, due dates, review and optional user-authorized calendar integrations |

## Desktop vs mobile
- Desktop: persistent side navigation, two/three-column working areas, roomy data and evidence panels, keyboard-accessible actions.
- Mobile: compact single-column cards and fixed bottom navigation; quick review and capture over dense statistical configuration.
- Reduced motion preferences are respected for the subtle view transition.
- Real product must maintain a usable accessible fallback for graphs, tables and long charts.

## Design constraints
- **No backend replacement in this PR.** Current verified refresh, source provenance, private dataset storage, statistical engine, audit boundaries and explicit external-provider consent remain untouched.
- No remote assets or external JavaScript libraries. The prototype has no network fetch and does not access personal data.
- Do not present prototype charts as measured findings; numeric values are labeled synthetic or illustrative.
- Do not advertise the proposed Today timeline as an available feature.
- Do not begin Next.js/API/authentication work until UI feedback and service boundaries have been reviewed.
- Adapt the design visually rather than copying any reference application's artwork, handwriting or proprietary layouts.

## Acceptance review
1. Desktop viewport (1440×900 and 1024×768): sidebar, all four tabs, research evidence inspector and analytics table remain legible.
2. Mobile viewports (390×844 and 320×700): no unusable horizontal overflow, bottom navigation is readable, all pages accessible.
3. Keyboard: each navigation button receives focus; Enter/Space switches view; focus indicators are visible.
4. Deep links: `#overview`, `#research`, `#analytics`, `#today` open the intended page.
5. Screens have strong headings and adequate distinction between actual, sample and future capabilities.
6. Verify the HTML functions with JavaScript disabled as a graceful limitation: static content only; production implementation must not depend on this prototype's navigation.
7. Before implementation, gather review feedback and decide on Streamlit refinement versus a new frontend with API/authentication boundaries.

## Next release candidate
**UI 1.2 — Research workspace refinement:** implement a real source-inspection panel inside the existing local-first application, behind synthetic acceptance tests. The separate **Today / action system** requires a real data model, persistence, access controls and task semantics before it becomes an operational feature.
