---
name: finance-variance-commentary
description: Turn an actual vs budget export into a ranked variance table and commentary explaining the driver behind each movement. Use for variance analysis, month-end commentary or review prep.
---

# Variance Commentary

Finance teams spend the first week of every month explaining what moved and why. The numbers are easy. The explanation is the work. This skill produces the ranked table and the written commentary that goes with it.

## When to use this

Trigger on any of: variance analysis, budget vs actual, actual vs prior period, month-end commentary, MIS notes, "why did costs go up", "explain the P&L movement", review meeting prep.

## Before you start

Ask only for what is missing. Do not interrogate the user.

Required: a file containing line items with at least two comparable columns (actual and budget, or current period and prior period).

Ask if not obvious from the file:
1. Which columns are the comparison base and which are the current actuals
2. Period covered, and whether they want the month, the year to date, or both
3. Who reads this: their own finance head, a CEO, a board, or an auditor

If the user gives no materiality threshold, use the default in the rules below and say so in the output.

## Workflow

### 1. Profile the file before parsing it

Open the file and look at it before writing any transformation. Indian accounting exports carry predictable traps:

- **Group and subtotal rows.** Tally, Zoho Books and SAP exports often include both the group row and its children. Summing everything double counts. Detect subtotal rows by checking whether a row's value equals the sum of the rows beneath it, or by indentation and label patterns such as "Total", "Sub Total", or an all-caps group heading. Exclude them from the line-level analysis and use them only as tie-out checks.
- **Dr/Cr columns.** Some exports split debit and credit into two columns instead of using signs. Convert to a single signed column before doing anything else.
- **Brackets for negatives.** `(1,23,456)` means negative.
- **Indian digit grouping.** `12,34,567` is 1234567, not 1,234,567 read the Western way. Strip separators rather than assuming a grouping pattern.
- **Merged headers and blank rows.** Real headers are often on row 3 to 8, not row 1.
- **Text in numeric columns.** Dashes, "NA", "-", and blank cells all mean zero or missing. Decide which and say which.

State what you found in one short paragraph before showing results. If you dropped rows, say how many and why.

### 2. Compute in code, never in prose

Write and run Python for every calculation. Do not do arithmetic inside your answer text. Numbers written by a model in a sentence are the single largest source of error in finance output.

### 3. Get the sign convention right

This is where variance analysis is most often wrong, so be deliberate.

- **Revenue and other income:** actual above base is favourable
- **Costs and expenses:** actual below base is favourable
- Never label a variance favourable or adverse from the arithmetic sign alone. Decide from the line's nature first.
- If you cannot tell whether a line is revenue or cost, say so and leave it unlabelled rather than guessing.

Percentage variance uses the comparison base as the denominator. If the base is zero, report the absolute movement and write "n/m" for the percentage instead of producing infinity or a meaningless number.

### 4. Rank by materiality, not by size of percentage

A 400 percent variance on a line worth twelve thousand rupees is noise. Rank on absolute value of the variance first, then apply the percentage as a secondary filter.

Default threshold, used unless the user gives their own: a line is material if the absolute variance is at least 5 percent of the base **and** is among the movements that together explain 80 percent of the total variance. Say in the output which threshold you used.

Cover the material lines properly rather than covering every line thinly. Ten explained lines beat forty listed ones.

### 5. Find the driver before writing a word

Commentary that restates the number is worthless. "Sales were 12 percent below budget" tells the reader nothing they cannot see in the table.

Work down this ladder for each material line:

1. **Decompose if the data allows it.** Where quantity and rate exist, split the movement into volume, price and mix. Volume variance is the change in quantity at the base rate. Price variance is the change in rate at actual quantity. State the split.
2. **Look inside the line.** If sub-accounts, cost centres, regions or customers are present, find which one carries most of the movement. A single concentrated driver is far more useful than a total.
3. **Check timing.** Many variances are phasing, not performance. An expense booked in March instead of April is not an overspend. Look for a matching opposite movement in the prior or next period and call it out as timing when present.
4. **Check one-offs.** Large round numbers, provisions, reversals, write-offs and year-end adjustments distort trends. Flag them and show the underlying number with the one-off excluded.
5. **If the data does not explain it, say so.** Write the question the user should ask the business owner. Never invent a cause.

### 6. Write the commentary

One short paragraph per material line. Each one carries: what moved, by how much, what caused it, and whether it repeats next period.

Rules that make the difference between commentary and filler:

- Lead with the cause, not the number
- Every claim carries a figure traceable to a row in the file
- Say whether the movement is one-off or recurring, because that is what the reader actually needs
- No hedging language. "Appears to be partly driven by" means nothing. Either the data shows it or you flag it as a question
- Plain business English. Write for a CEO, not for an auditor

## Output format

Deliver in this order.

**1. Headline.** Two lines maximum. Total variance, direction, and the single biggest driver.

**2. Ranked variance table.**

| Line item | Base | Actual | Variance | Variance % | F/A | Driver |

Sorted by absolute variance, descending. Material lines only, with the rest collapsed into one "All other lines" row so the table still foots.

**3. Commentary.** One paragraph per material line, in the same order as the table.

**4. Timing and one-off adjustments.** A short section separating true performance from phasing, with an adjusted variance figure.

**5. Questions to ask the business.** The movements the file cannot explain, written as specific questions with the amount attached.

Offer the workbook version at the end. Do not build it unless asked.

## Checks to run before delivering

Run these in code and state the result. If a check fails, fix it or say plainly that it failed.

- Sum of individual line variances equals the total variance
- Actual column total and base column total each match the file's own totals, where the file gives them
- No line counted twice through an included subtotal row
- No percentage computed on a zero base
- Every number in the commentary traces to a row in the source file
- Favourable and adverse labels match the nature of each line, not the arithmetic sign

## What this skill does not do

- It does not judge whether performance is acceptable. It explains movement.
- It does not invent business reasons. Unexplained movements become questions, not narrative.
- It does not touch accounting treatment, provisioning judgement or tax positions.
- It works on the file it is given. It cannot see the ledger behind it.
