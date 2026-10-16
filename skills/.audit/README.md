# Library audit

Run before calling any domain done:

```
python3 .audit/audit.py
```

Checks: relative links resolve, no em dashes, `name:` matches folder, descriptions under 200,
the four required SKILL.md sections plus a checks-or-quality-bar section, the eight required
guide sections, one README plus five two-file folders per domain, and the length caps.

Length caps: guides 140, domain README 155, SKILL.md 150. A small number of earlier files
sit above the cap and are reported separately rather than failing the check.

**Never trim required content to hit a length number.** Cut prose, or accept the length.
