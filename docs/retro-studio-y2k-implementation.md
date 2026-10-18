# Retro Studio × Y2K Hybrid UI (draft)

## Shipped in this feature branch
- Warm paper-like panels, restrained retro window borders, editorial type and vintage-computer accents.
- 1990s/early-2000s-inspired **text-based** interface glyphs/icons (offline, no externally downloaded icon packs or font assets).
- Restyled Today schedule into priority-coloured activity capsules, with all task titles and project metadata HTML-escaped. Underlying task CRUD and transactions unchanged.
- Decluttered sidebar descriptors, collapsed advanced calendar/timezone controls and new-task editor; one-click Research and Analytics navigation retained.
- Dark styling supported via theme tokens; responsive layout and native Streamlit keyboard widgets remain.
- Retains Today default page and all existing nine views, tests/selectors and live local data flows.

## Important limitations
This is a first live Streamlit integration, **not** a full drag-and-drop window manager or Figma-complete pixel icon system. It does not add third-party assets, background tasks, browser storage, external APIs or AI calls. Do not interpret CSS visuals as production-tested until local browsers and CI have been exercised. HTML injection is restricted to escaped task display values.

## Acceptance checklist
1. Test Today with an empty, unscheduled, due, scheduled, overdue, edited and completed task. Verify the scheduled start/end labels and task colors.
2. Create/edit/reschedule/complete task and reload app. Confirm persistence.
3. Expand calendar controls; switch Day/Week and timezone. Verify Week shows all relevant date buckets.
4. Open/close task editor and verify references/date/time validation errors still appear.
5. Test desktop 1440×900 and mobile 390×844. Sidebar/collapsed controls, forms and native focus/keyboard behavior must remain usable.
6. Open Ask, Library, Explore, Datasets and Analyse. Verify styling without chart/text contrast regressions in Light and Dark.
7. Run python unit tests and all synthetic Streamlit browser CI suites. Screenshot review required before merge.
8. No external icon images and no new sensitive files are committed.

## Follow-up
If the first live pass is accepted, design a licensed cohesive 16/32px icon sprite set, add meaningful minimalist retro frame components for Research and Analytics, and tune mobile typography with verified screenshots, without allowing decoration to hide source provenance or statistical assumptions.
