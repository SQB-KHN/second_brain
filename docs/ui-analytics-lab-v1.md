# Analytics Lab UI 1.0

This branch is a **presentation-only redesign** for SecondSelf's eight-view Streamlit application. It introduces reusable UI tokens/helpers in `ui_analytics_lab.py`, a four-metric Home dashboard, quick workflow actions, refined responsive typography, button and card styling, and descriptive sidebar navigation labels. Existing navigation state `st.session_state.view` and the radio label `Workspace` are preserved for compatibility.

## Design direction
- Desktop-first, readable and professional: information hierarchy, clear surfaces, subdued blue accent, restrained shadows.
- Light and dark modes with responsive mobile spacing and visible keyboard focus.
- Existing Capture, Ask, Explore, Library, Insights, Datasets, Analyse semantics and safeguards unchanged.
- Home uses already loaded note and graph metadata; no new private dataset reads, cloud requests, downloads, refresh jobs or statistical computations.
- Untrusted knowledge text renders using safe Streamlit text/write components, not interpolated HTML. HTML hero/section arguments are escaped.

## Manual acceptance checklist
1. Run the application from `ui-analytics-lab-v1`; verify all eight sidebar choices navigate and back-and-forth view state persists.
2. Check Home metric cards, four quick actions, recent notes and graph status with a synthetic local workspace. Empty and nonempty data should both render.
3. Switch Light/Dark; inspect text contrast, focus state, chart/graph appearance, narrow viewport and long titles.
4. Import a synthetic document and verify previous preview, source provenance and explicit Ask consent remain intact.
5. Preview and register a synthetic dataset, open Analyse from Datasets and run the existing synthetic test workflow.
6. In `DEPLOY_MODE=true`, confirm only the approved synthetic demo renders and edit/import operations remain unavailable.
7. Run automated tests and browser suites; do not assume presentation tests prove visual polish. Capture real screenshots with synthetic data before portfolio publication.

## Scope and limitations
The navigation is still a single Streamlit radio control, now annotated with functional group captions. No custom JavaScript, injected widget values, remote fonts, network assets or dependency changes. Does not redesign complex Datasets and Analyse internal workflows; those belong to UI 1.1. The prior app-wide theme CSS remains; the new UI stylesheet layers on top so some third-party widgets may retain native Streamlit styling. This is not a full accessibility audit or a pixel-diff-tested redesign.
