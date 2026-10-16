import pathlib, re, sys
fail = []

# ---- 1. every relative markdown link resolves
links = 0
for p in sorted(pathlib.Path('.').rglob('*.md')):
    for m in re.finditer(r'\[[^\]]+\]\(([^)#]+?)\)', p.read_text()):
        t = m.group(1)
        if t.startswith(('http://','https://','mailto:')): continue
        links += 1
        if not (p.parent / t).resolve().exists():
            fail.append(f"BROKEN LINK  {p}  ->  {t}")
print(f"1. relative links checked: {links}")

# ---- 2. no em dashes
for p in sorted(pathlib.Path('.').rglob('*.md')):
    if '—' in p.read_text(): fail.append(f"EM DASH  {p}")
print("2. em dashes: 0" if not any('EM DASH' in f for f in fail) else "2. EM DASHES FOUND")

# ---- 3. frontmatter: name matches folder, description under 200
skills = sorted(pathlib.Path('.').glob('*-skills/*/SKILL.md'))
for p in skills:
    t = p.read_text()
    name = re.search(r'^name: (.*)$', t, re.M).group(1).strip()
    desc = re.search(r'^description: (.*)$', t, re.M).group(1).strip()
    if name != p.parent.name: fail.append(f"NAME MISMATCH  {p}: {name} != {p.parent.name}")
    if len(desc) >= 200:      fail.append(f"DESC {len(desc)}  {p}")
print(f"3. skills checked: {len(skills)}  (name match + description < 200)")

# ---- 4. required sections
for p in skills:
    t = p.read_text()
    for s in ['## When to use this','## Workflow','## Output format','## What this skill does not do']:
        if s not in t and not (s == '## Workflow' and ('## Work down the funnel in order' in t or '## For a controlled test' in t or '## Plan mode' in t)):
            fail.append(f"MISSING {s}  {p}")
    if '## Checks to run before delivering' not in t and '## Quality bar' not in t:
        fail.append(f"MISSING checks/quality bar  {p}")
guides = sorted(pathlib.Path('.').glob('*-skills/*/*-guide.md'))
for p in guides:
    t = p.read_text()
    for s in ['## Who this is for','## The problem it solves','## What you give it','## What you get back',
              '## What good output looks like','## Installing it','## Using it','## If something looks wrong']:
        if s not in t: fail.append(f"MISSING {s}  {p}")
print(f"4. guides checked: {len(guides)}  (8 required sections each)")

# ---- 5. structure: 1 README + 5 folders per domain, 2 files per skill folder
for d in sorted(pathlib.Path('.').glob('*-skills')):
    if not (d/'README.md').exists(): fail.append(f"NO DOMAIN README  {d}")
    subs = sorted(x for x in d.iterdir() if x.is_dir())
    if len(subs) != 5: fail.append(f"{d} has {len(subs)} skill folders, expected 5")
    for s in subs:
        files = sorted(x.name for x in s.iterdir())
        if files != sorted(['SKILL.md', f'{s.name}-guide.md']):
            fail.append(f"{s} contains {files}")
print(f"5. domains checked: {len(list(pathlib.Path('.').glob('*-skills')))}")

# ---- 6. line counts
print("\n6. line counts")
for label, ps, lo, hi in [("SKILL.md", skills, 120, 200), ("guides", guides, 90, 140)]:
    n = [len(p.read_text().splitlines()) for p in ps]
    out = [f"{p.parent.name}={c}" for p, c in zip(ps, n) if not lo <= c <= hi]
    print(f"   {label}: min {min(n)}, max {max(n)}, target {lo}-{hi}"
          + (f"  outside: {', '.join(out)}" if out else "  all in range"))
r = {d.name: len((d/'README.md').read_text().splitlines()) for d in sorted(pathlib.Path('.').glob('*-skills'))}
print(f"   domain READMEs: {r}")

# ---- 7. hard length caps, enforced on domains built from 2026-09-08 onward
GRANDFATHERED = {"finance", "data", "marketing", "ops", "health", "content", "sales"}
CAPS = {"skill": 150, "guide": 140, "readme": 155}
print("\n7. length caps (guides 140, domain README 155, SKILL.md 150)")
over_new, over_old = [], []
for p in skills + guides:
    dom = p.parts[0].split("-")[0]
    kind = "skill" if p.name == "SKILL.md" else "guide"
    n = len(p.read_text().splitlines())
    if n > CAPS[kind]:
        (over_old if dom in GRANDFATHERED else over_new).append(f"{p.parent.name} {kind}={n}")
for d in sorted(pathlib.Path(".").glob("*-skills")):
    dom = d.name.split("-")[0]
    n = len((d / "README.md").read_text().splitlines())
    if n > CAPS["readme"]:
        (over_old if dom in GRANDFATHERED else over_new).append(f"{d.name} README={n}")
print(f"   grandfathered, over cap (allowed): {len(over_old)}" + (f"  {', '.join(over_old)}" if over_old else ""))
if over_new:
    fail.append("OVER LENGTH CAP: " + ", ".join(over_new))
    print(f"   NEW DOMAINS OVER CAP: {', '.join(over_new)}")
else:
    print("   new domains over cap: none")

# ---- 8. no quality bar item may appear in two domains (guards against boilerplate)
import collections
seen = collections.defaultdict(set)
qb_n = 0
for q in skills:
    m = re.search(r"## Quality bar\n(.*?)(?=\n## )", q.read_text(), re.S)
    if not m: continue
    for line in m.group(1).splitlines():
        if line.startswith("- "):
            qb_n += 1
            seen[line[2:].strip().lower()].add(q.parts[0].split("-")[0])
dupes = {k: v for k, v in seen.items() if len(v) > 1}
print(f"\n8. quality bar items: {qb_n}, duplicated across domains: {len(dupes)}")
for k, v in dupes.items():
    fail.append(f"DUPLICATE QUALITY BAR ITEM {sorted(v)}: {k[:70]}")

print("\n" + "="*60)
if fail:
    print(f"{len(fail)} PROBLEM(S):"); [print("  " + f) for f in fail]; sys.exit(1)
print("ALL CHECKS PASSED")
