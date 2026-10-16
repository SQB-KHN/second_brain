# Agent skill setup

This repository keeps the full reference library under `skills/`.

Two example skills are installed in agent-discovery folders on this branch:
- `tech-design-doc`
- `tech-readiness-review`

`.claude/skills/<name>/SKILL.md` is the Claude Code project-local location. `.agents/skills/<name>/SKILL.md` is the Codex project-local location. Each skill is copied with its original companion guide to keep relative references working.

## Usage
Open this repository as a project in Claude Code or Codex. Ask the agent to write a technical design document or review technical readiness. Each environment should discover its respective project-local skill folder.

## Maintenance
The source of truth for all 55 skills remains under `skills/`. If you edit a source skill, mirror changes to the corresponding installed copies. Do not bulk-enable all 55 without review; skills can influence agent behavior and run locally depending on tool permissions.

This pull request only installs skills into this repository, **not** globally across your computer or your other projects.
