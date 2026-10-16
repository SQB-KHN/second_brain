# MIS Pack Builder

Turns a raw trial balance into a formatted management reporting workbook with grouped P&L, balance sheet, KPIs, a mapping sheet and a visible checks sheet.

---

## Who this is for

Anyone who produces a monthly management pack: management accountants, FP&A teams, accountants in practice producing packs for several clients, finance leads at startups and SMEs, and CFOs at companies too small to have a reporting team.

## The problem it solves

The trial balance comes out of the accounting system in minutes. Turning it into something a management team can read takes most of a day: regrouping accounts, rebuilding the same mapping from memory, formatting, then checking the tie-outs if there is time left.

This skill does the reshaping, keeps the mapping in the workbook so next month is a rerun rather than a rebuild, and proves the pack ties before handing it over. First month saves several hours. Every month after that saves most of a day.

---

## What you give it

A trial balance or ledger export. Excel or CSV.

**Minimum:** account names and balances.

**Each of these makes the pack materially better:**

| Extra data | What it unlocks |
|---|---|
| Account codes | Better automatic grouping and a more stable mapping across months |
| Prior month, prior year or budget columns | Comparative columns and a variance sheet |
| Cost centre, branch or segment | A segment view sheet |
| Opening and closing balances | Stronger tie-out checks |
| Last month's pack or an existing mapping file | It follows your format exactly instead of proposing its own |
| Inventory balances | Inventory days in the KPI sheet |

**Handled automatically:** Dr/Cr split columns, brackets for negatives, Indian digit grouping, group and subtotal rows, header rows that do not start on row 1, and account codes stored as text with leading zeros.

## What you get back

An `.xlsx` workbook with these sheets:

1. **Cover** with entity, period, currency, units and source
2. **P&L** grouped, with gross profit, EBITDA, EBIT, PBT and PAT subtotals
3. **Balance sheet** in Schedule III grouping or your own format
4. **KPIs**, only the ratios your data actually supports
5. **Segment view**, if the dimension exists in your file
6. **Variance**, if comparatives exist
7. **Mapping**, the full account-to-line map, so next month is one step
8. **Checks**, every tie-out with its result

Plus a short summary in chat covering mapping decisions, check results and anything left unmapped.

---

## How it protects accuracy

- It refuses to build on a trial balance that does not balance, and reports the difference instead
- Nothing is ever silently dropped. Any account it cannot map goes into a visible `Unmapped` section with its balance
- Every subtotal is a live Excel formula, not a pasted value, so you can click a cell and audit it
- The checks sheet is part of the workbook, not a private step, and covers TB balancing, balance sheet balancing, mapped total against TB total, and unmapped balance
- A failed check is stated at the top of the reply as well as in the sheet, never buried

The silent-drop failure is the one that matters most here. A pack that quietly loses two accounts looks finished and is wrong, and nobody notices until someone checks the totals in a board meeting.

## Where you stay in control

Mapping is the only judgement call, and it is yours. The skill proposes a mapping as a table and waits for your confirmation before building. If you supply last month's pack or a mapping file, it follows your structure exactly rather than improving it.

## What good output looks like

A strong pack opens with a checks sheet where every line reads pass and the Unmapped total is zero. Subtotals are live formulas, so clicking gross profit shows the sum behind it. The KPI sheet carries only ratios your data supports, and names the ones it left out and why.

Accounts sitting in Unmapped is the pack working, not failing. If the grouping does not look like your house format, you did not attach last month's pack or a mapping file, so it proposed its own.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. The workbook is generated in Python and will not build without it.
2. Download this folder, or make a folder named `finance-mis-pack` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload the trial balance and say what you need.

Examples that work:

- "Build the monthly MIS pack from this trial balance for March"
- "Turn this TB into a management pack with prior year comparatives"
- "Make this presentable for the board, same format as last month" (attach last month's pack)
- "Build the finance pack in lakhs, Schedule III balance sheet"

**Second month onward:** attach the mapping sheet from the previous pack along with the new TB. The rebuild becomes a single step with no mapping conversation.

---

## Limits worth knowing

- It reshapes and checks. It does not audit the underlying numbers.
- It does not decide accounting treatment, statutory classification or provisioning.
- It does not prepare statutory financial statements or anything meant for filing.
- It will not invent comparatives, budgets or missing balances. Absent data means an absent column, stated clearly.
- KPIs that need data you did not supply are omitted rather than estimated, and it tells you which ones and why.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| It refuses to build | The trial balance does not balance | It reports the difference. Fix the TB and rerun. |
| Accounts sitting in Unmapped | Names it could not classify with confidence | Map them in the mapping table and rerun. They are shown, never dropped. |
| Grouping does not match your house format | No reference pack supplied | Attach last month's pack or a mapping file. |
| Balance sheet does not balance | Source data issue, not a build issue | The checks sheet shows the failing line and amount. |
| Missing KPIs | Underlying data not present | It states which were omitted and what data each needs. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Finance skills](../README.md) in the [Claude Skills Library](../../README.md).
