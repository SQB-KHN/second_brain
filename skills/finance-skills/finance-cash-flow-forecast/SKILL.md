---
name: finance-cash-flow-forecast
description: Build a 13-week rolling cash forecast with three scenarios, dated shortfall warnings and ranked actions. Use for cash position, runway, collection planning or payroll cover.
---

# Cash Flow and Scenario Planning

Profit is an opinion, cash is a fact, and most finance professionals still forecast cash in a spreadsheet rebuilt from scratch each time. This skill builds the 13-week rolling view, stress tests it, and names the date things get tight.

## When to use this

Trigger on: cash flow forecast, rolling cash, 13-week cash, runway, "can we make payroll", collection plan, working capital, liquidity, "what if customers pay late", cash crunch.

## Before you start

Required: opening cash balance, plus receivables and payables detail.

Ask, briefly:
1. Opening cash and bank balance as at the forecast start date, and whether any of it is restricted or held as a margin deposit
2. Available overdraft or credit line, and how much is already drawn
3. Recurring fixed outflows not in the payables file, which almost always includes salaries, rent, EMIs and statutory payments
4. Any large known one-offs in the window, such as a capex payment, an advance tax instalment, a bonus payout or a loan repayment
5. Horizon, if not 13 weeks

If the user cannot answer everything, build with what exists and list every gap as a stated assumption. A forecast with visible assumptions is useful. A forecast with hidden ones is dangerous.

## Workflow

### 1. Profile the inputs

Handle the usual export issues: header row position, Dr/Cr columns, brackets for negatives, Indian digit grouping, ageing buckets held as text, subtotal rows.

For ageing files specifically, confirm whether the buckets are counted from invoice date or from due date. These give different answers and the files rarely say which. Ask if it is unclear.

### 2. Compute in code, never in prose

Every week's balance, every collection cohort and every scenario runs as Python. Nothing arithmetic is worked out inside a sentence. A forecast is a chain of dependent numbers, so a single slip propagates through all thirteen weeks silently.

### 3. Derive collection behaviour from history, not from hope

This is the difference between a forecast and a wish.

If historical collection data exists, compute actual behaviour: average days beyond due date, the share of invoices that pay on time, and the share that go past 90 days. Use those observed rates.

If no history exists, ask the user for their own estimate. If they cannot give one, use a stated default of 60 percent within terms, 30 percent within 30 days past due, 10 percent beyond, and label it clearly as an assumption rather than presenting it as analysis.

Never assume every invoice collects on its due date. It is the most common error in cash forecasting and it makes the forecast useless in exactly the weeks that matter.

Treat the oldest receivables separately. Anything over 120 days should be modelled at a heavily reduced collection probability, or excluded from the base case entirely with the excluded amount stated.

### 4. Build the weekly grid

Thirteen columns, one per week, with dates rather than week numbers so the output is directly usable.

Rows:
- Opening balance
- Collections from receivables, by ageing cohort
- Other inflows
- Payables due
- Salaries
- Rent and utilities
- Statutory payments
- Loan and EMI repayments
- One-off outflows
- Total inflows, total outflows, net movement
- Closing balance
- Headroom, which is closing balance plus undrawn credit line

Closing balance of each week is the opening balance of the next. Enforce that in code rather than by eye.

### 5. Statutory payments

Indian statutory outflows land on fixed dates and are easy to forget, which is exactly why they cause surprises. Prompt the user for their own dates and offer common ones as a starting point, clearly marked as needing confirmation: GST payment with the monthly return, TDS deposit early in the following month, PF and ESI mid-month, and advance tax quarterly.

Do not state these dates as settled fact and do not compute a tax liability. Deadlines change and vary by taxpayer category. Ask the user to confirm against their own compliance calendar. The skill's job is to place the outflow on the grid, not to advise on tax.

### 6. Run three scenarios

Vary one thing, collection speed, because that is what actually moves and what the user can partly influence.

- **Base:** observed or agreed collection behaviour
- **Downside:** collections slip by an additional 15 days across the board, and anything over 90 days collects nothing
- **Upside:** collection terms hold, with follow-up on the largest overdue accounts landing within the window

Keep outflows constant across all three. Most outflows are contractual, and varying both sides at once produces a forecast nobody can interpret.

State each scenario's assumption in a single line next to its result. A scenario without its assumption visible is just a number.

### 7. Find the pressure points

Report, for each scenario:
- Lowest closing balance in the window, and the week it occurs
- Any week where closing balance goes below zero, with the date and the shortfall amount
- Any week where closing balance falls below the user's stated minimum operating balance
- Weeks where headroom depends entirely on the credit line

Name the date. "Cash gets tight in week 7" is not usable. "Closing balance falls to a shortfall of 18 lakh in the week of 12 October" is.

### 8. Rank the actions

Do not produce generic advice. Produce specific actions from the actual file, ranked by rupee impact:

- The named overdue accounts whose collection closes the gap, largest first, with amounts and days overdue
- Payables that could be moved past the pressure week, with vendor and amount, flagged where the vendor is critical to operations
- The size and timing of credit line drawdown needed if collections do not improve
- Whether the shortfall is a timing problem or a structural one, which is the single most useful judgement in the whole output

## Output format

**1. Verdict.** Two lines. Can they cover the window, and if not, when it breaks and by how much.

**2. The 13-week table.** Base case, weeks as columns.

**3. Scenario comparison.** Lowest balance and shortfall week under each of the three, with the assumption for each stated.

**4. Pressure points.** Dated, with amounts.

**5. Actions.** Ranked by impact, naming specific accounts and amounts from the file.

**6. Assumptions.** Every one, listed plainly, including everything the user could not supply.

Offer the Excel version with the scenarios as switchable inputs. Build it only if asked.

## Checks to run before delivering

- Each week's opening balance equals the prior week's closing balance
- Total modelled collections do not exceed total receivables outstanding
- Receivables excluded from the base case are stated with their value
- Every recurring outflow the user named appears in the grid
- Scenario outputs differ only through the collection assumption

## What this skill does not do

- It does not compute tax liabilities or confirm statutory due dates. Those get confirmed against the user's compliance calendar.
- It does not recommend borrowing, refinancing, or any specific financial product. It sizes the gap and its timing.
- It does not advise on which vendor to delay as a matter of judgement. It shows the options and their impact.
- It cannot see bank balances or ledgers directly. It models the files it is given.
- It is a forecast, not a promise. Accuracy depends entirely on the collection assumption, which is why that assumption is always shown.
