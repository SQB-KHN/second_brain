# AI skills library

This project already contains a knowledge-system application; the AI skills will live under `skills/` without changing existing application files.

The original archive is kept at the repository root. A review-branch workflow is intended to expand the archive into domain folders. **Review the expanded files before merging the pull request.**

## Installing individual skills

Each folder `skills/<domain>-skills/<skill-name>/` contains `SKILL.md` plus a supporting guide. Copy the whole individual folder into:

- Claude Code: `<project>/.claude/skills/<skill-name>/` (or `~/.claude/skills/<skill-name>/` for user-wide use).
- Codex: `<project>/.agents/skills/<skill-name>/` (or `~/.agents/skills/<skill-name>/` for user-wide use).

The archive has 55 skills across 11 domains: content, data, education, finance, health, marketing, operations, owner, sales, student, and technology.

Read each skill's instructions before enabling it. These markdown files are instructions rather than executable packages. The original `.audit/audit.py` is included for reference only and is not run by the extraction workflow.
