SecondSelf Timeline Studio v2

This replaces the generic dashboard styling with a timeline-first design inspired by the supplied scheduling references, without copying their artwork.

Design principles:
- Today opens first, with day/week switch and seven-day picker.
- Connected coloured activity blocks, typography and restrained pastel colours.
- Desktop sidebar and two-column Today view; mobile bottom navigation.
- Research, Analytics and Projects one click away.
- All dates, tasks and priorities are sample-only: no persistent task store, calendar connection, real alerts or data access.
- Standalone offline HTML, no external assets or network.

Manual review:
Open docs/prototypes/timeline-studio-v2.html, test desktop and mobile, keyboard controls, day/week and view navigation. Compare visual hierarchy, colour rhythm, time structure and density against the provided references. This is not a verified production UI.

Figma handoff:
Use editable frames for desktop Today, mobile Today, week calendar and adjacent Research/Analytics screens, then develop reusable visual tokens and components. Figma integration is optional and must not be represented as completed until confirmed.

Future implementation after design approval:
1. Create a real persisted task, priority and event model.
2. Add timezone-aware local planning and safe task actions.
3. Design a responsive application interface on stable service boundaries.
4. Add optional consent-controlled calendar and notification integrations.

The previous prototype stays in project history as an exploration rather than the endorsed design.