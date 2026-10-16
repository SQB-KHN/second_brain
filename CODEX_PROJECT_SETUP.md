# Install skills in Codex: project by project

## Prerequisites

Install Git and Codex CLI on your computer. In Terminal, verify:

```bash
git --version
codex --version
```

If Codex is not installed, follow the current official installation guide at https://developers.openai.com/codex/cli/ . Do not paste API keys into source files.

## Test this repository (macOS/Linux)

```bash
git clone https://github.com/SQB-KHN/second_brain.git
cd second_brain
git pull --ff-only
find .agents/skills -name SKILL.md -print
codex
```

If you already cloned this repository, skip `git clone` and `cd` into the existing checkout. In Codex, ask:

> List the available project-local skills and their paths. Then use $tech-design-doc to outline an architecture decision for this repository. Do not change files.

Review its answer and check it references `.agents/skills/tech-design-doc/SKILL.md`. If Codex was already open when skills were added, start a new session.

## Install ONE skill into another project

Open Terminal and replace both paths below with actual local directories (never a GitHub HTTPS URL). For example, to enable `owner-unit-economics` for your separate rice-distribution project:

```bash
LIBRARY="$HOME/projects/second_brain"
PROJECT="$HOME/projects/rice-distribution"
SKILL="owner-unit-economics"
CATEGORY="owner-skills"
mkdir -p "$PROJECT/.agents/skills/$SKILL"
cp -R "$LIBRARY/skills/$CATEGORY/$SKILL/." "$PROJECT/.agents/skills/$SKILL/"
```

This copies the entire skill directory, including its `SKILL.md` and guide. Check the skill before opening Codex:

```bash
cat "$PROJECT/.agents/skills/$SKILL/SKILL.md"
cd "$PROJECT"
codex
```

Ask Codex: `Use $owner-unit-economics to explain the unit economics for this project, without editing any files.`

**Do not copy the entire 55-skill catalog** into `.agents/skills/`; review and install only the skills appropriate to each project.

## Discover additional skills

Browse `skills/<category>-skills/<name>/SKILL.md`. To list skill names locally:

```bash
find skills -name SKILL.md -print | sort
```

Common candidates: `data-sql-writer`, `owner-unit-economics`, `ops-supplier-scorecard`, `tech-design-doc`, and `tech-readiness-review`.

## Update or remove a project skill

To update a copied skill, review changes in the source catalog before copying it again. To deactivate a skill, remove only that skill's directory from that project's `.agents/skills/` and restart the Codex session. Removing an installed copy does not remove it from the source catalog.

## Notes

- These instructions configure **repository-local** skills only. They do not change global Codex settings.
- `AGENTS.md` provides repository instructions; `SKILL.md` provides optional task-specific workflows.
- Skills may ask for actions, so check tool permissions and review scripts before executing them.
- GitHub connection in ChatGPT is separate from Codex CLI's local access.
