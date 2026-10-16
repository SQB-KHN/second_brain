---
name: finance-mis-pack
description: Build a formatted Excel management pack from a trial balance, with grouped P&L, balance sheet, KPIs and a visible checks sheet. Use for monthly MIS, management packs or board numbers.
---

# MIS Pack Builder

Every month the same trial balance gets reshaped into the same reporting pack by hand. The mapping is rebuilt from memory, the formatting is redone, and the tie-outs are checked at the end if there is time. This skill produces the pack and makes the mapping reusable so the second month takes minutes.

## When to use this

Trigger on: monthly MIS, management pack, board pack, management reporting, "make this trial balance presentable", formatted P&L, reporting workbook, "build the finance pack".

## Before you start

Required: a trial balance or ledger export with account names and balances.

Ask, briefly:
1. Period, and whether comparatives are wanted for prior month, prior year, budget, or all three
2. Whether they have an existing mapping file or a pack from last month to follow. If they do, follow their structure exactly. Their format is not up for improvement unless they ask.
3. Reporting currency and units. Rupees, thousands, lakhs or crores.
4. Whether the balance sheet should follow Schedule III grouping or their own internal format

If comparative columns are absent from the file, build the current period only and say what a comparative would add. Do not stall.

## Workflow

### 1. Profile the trial balance

Same discipline as any accounting export. Check for and report: real header row position, Dr/Cr split columns versus a signed column, brackets for negatives, Indian digit grouping, group and subtotal rows, and account codes held as text with leading zeros that Excel may have stripped.

State the row count and the debit and credit totals before doing anything else.

### 2. Prove the trial balance balances

Before any mapping work, check total debits equal total credits.

If it does not balance, stop and report the difference. Do not proceed to build a pack on a trial balance that does not tie. A pack built on a broken TB is worse than no pack, because it looks finished.

### 3. Map accounts to reporting lines

If the user supplied a mapping, apply it exactly.

If not, propose one. Group by account name and code pattern into the standard structure:

- **P&L:** Revenue, Other income, Cost of goods sold or cost of services, Employee benefits, Rent and utilities, Selling and marketing, Administrative expenses, Depreciation and amortisation, Finance cost, Tax
- **Balance sheet:** Equity, Reserves, Borrowings, Trade payables, Other current liabilities, Provisions, Fixed assets, Investments, Inventory, Trade receivables, Cash and bank, Loans and advances, Other current assets

Show the proposed mapping as a table and get it confirmed before building. Mapping is the one judgement call in this skill, and it belongs to the user.

**The rule that matters most:** never silently drop an account. Any account you cannot map goes into an explicit `Unmapped` section, visible in the workbook, with its balance. A pack that quietly loses two accounts is the failure mode that destroys trust in the whole output, and it is invisible until someone checks the totals.

### 4. Build the workbook

Write it with `openpyxl`. Sheets, in order:

1. **Cover.** Entity, period, currency and units, date prepared, and a one-line statement of source, such as trial balance as at a date.
2. **P&L.** Grouped lines with subtotals: gross profit, EBITDA, EBIT, profit before tax, profit after tax. Columns for current period, comparatives, and variance where comparatives exist.
3. **Balance sheet.** Grouped per the format chosen, with a total assets and total equity and liabilities line.
4. **KPI sheet.** Only ratios the data actually supports. Gross margin, EBITDA margin, net margin, revenue growth, expense to revenue, current ratio, debtor days, creditor days, inventory days where inventory exists. If a ratio needs data that is not present, omit it rather than estimating. State which were omitted and why.
5. **Segment or cost centre view.** Only if the file carries that dimension.
6. **Variance.** Only if budget or prior period columns exist.
7. **Mapping.** The full account-to-line mapping, so the pack is auditable and next month is a rerun rather than a rebuild.
8. **Checks.** Every tie-out with its result, visible, not buried.

### 5. Formatting rules

- Live formulas for every subtotal and total, not pasted values. Finance people audit packs by clicking a cell. A pack of hardcoded numbers cannot be checked and will not be trusted.
- Number format matching the chosen units, with the Indian digit grouping where the user works in that convention
- Negatives in brackets, which is the finance convention, not with a minus sign
- One accent colour, bold headers, frozen panes, sensible column widths
- No merged cells inside data ranges. They break every downstream filter and pivot.
- Print setup done: fit to one page wide, repeat header rows, landscape for wide sheets

### 6. Fill the checks sheet

Run every check listed at the end of this skill in code, and write each result into the sheet as pass or fail with the figure beside it. The checks sheet ships inside the workbook. It is not a private step.

If any check fails, say so at the top of the answer as well as in the sheet. Never bury a failed tie-out inside a workbook and describe the pack as complete.

## Output format

Deliver the `.xlsx` file, then report these in chat. The workbook is the deliverable, but nobody opens a workbook without knowing what to look at first.

**1. What was built.** Entity, period, units, and the sheets included. One or two lines.

**2. Check results.** Every tie-out with its result and its figure. State these in chat as well as in the sheet, and lead with any that failed.

**3. Mapping decisions.** The groupings that required a judgement call, and the accounts where the name alone was not conclusive. Not the whole mapping, which is already in the workbook.

**4. Unmapped accounts.** Listed with their balances, or an explicit line confirming the total is zero. Never omit this section on the grounds that it is empty. A stated zero is the reassurance.

**5. Ratios omitted.** Which KPIs were left out and what data each would need.

**6. Next month.** Supplying this pack's mapping sheet alongside the new trial balance turns the rebuild into a single step with no mapping conversation.

## Checks to run before delivering

- Total debits equal total credits in the source
- Balance sheet balances: total assets equal total equity and liabilities
- P&L profit after tax agrees with the movement in reserves, where the file allows this to be tested
- Sum of every mapped line equals the trial balance total, so nothing was lost in mapping
- Unmapped accounts total, which should be zero, and is stated even when it is
- Comparative columns foot to their own totals

## What this skill does not do

- It does not decide accounting treatment, classification for statutory purposes, or provisioning
- It does not prepare statutory financial statements or anything for filing
- It does not audit the underlying numbers. It reshapes what it is given and checks internal consistency
- It does not invent comparatives, budgets or missing balances
- It does not post entries, change your accounting system, or file anything. It produces a workbook for you to review
