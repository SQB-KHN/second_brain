# Variance Commentary

Turns an actual vs budget or actual vs prior period file into a ranked variance table plus written commentary that explains the driver behind each movement.

---

## Who this is for

Finance professionals who write month-end commentary: FP&A analysts, management accountants, finance business partners, controllers, and finance leads in small companies who do the whole close themselves.

## The problem it solves

Producing the variance numbers takes minutes. Explaining them takes days. Most of that time goes into hunting for the driver behind each movement and then writing it up in language a non-finance reader can act on. This skill does both passes and leaves the judgement calls with you.

Typical saving is half a day to a full day per close.

---

## What you give it

One file. Excel or CSV. A P&L, trial balance, cost centre report or MIS extract.

**Minimum requirement:** line items in rows, and at least two comparable numeric columns, such as actual and budget, or current month and same month last year.

**Makes the output much stronger if present:**

| Extra data | What it unlocks |
|---|---|
| Quantity and rate columns | Volume, price and mix decomposition instead of a single lumped variance |
| Cost centre, region, branch or segment | Pinpoints which part of the business carries the movement |
| Sub-account detail under each head | Finds the specific account driving a group-level variance |
| Two or more prior periods | Separates a genuine shift from normal month-to-month noise |
| A YTD column alongside the month | Lets it say whether a monthly miss is recoverable |

**Export formats it handles:** Tally, Zoho Books, Busy, SAP, Oracle, NetSuite, QuickBooks, or anything hand-built in Excel. It handles group and subtotal rows, Dr/Cr split columns, brackets for negatives, Indian digit grouping such as 12,34,567, merged headers, and header rows that do not start on row 1.

## What you get back

1. A two-line headline: total variance, direction, biggest single driver
2. A ranked variance table, sorted by rupee impact, with favourable or adverse marked correctly per line
3. Written commentary, one paragraph per material line, cause first
4. A timing and one-off section that separates phasing from real performance
5. A list of the movements the data cannot explain, written as questions to put to the business

An Excel version is offered at the end, built only if you ask.

## What good output looks like

A strong output reads like a business person wrote it, not a spreadsheet. Each paragraph leads with the cause: "People costs ran 42 lakh above plan, of which 31 lakh is the Pune facility, which was budgeted but went live a month late, so it recurs from next month." Ten lines explained properly beats forty listed thinly, and the questions section carries amounts.

If the commentary restates the numbers instead of explaining them, your file had only totals. Re-export with sub-account, cost centre or quantity detail and the difference is immediate.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities. The skill runs Python for every calculation and will not work without it.
2. Download this folder, or make a folder named `finance-variance-commentary` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.
5. It is now available in Chat and Cowork on your account. Skills you upload are private to you.

## Using it

Upload your file and say what you want in plain language. The skill triggers on its own.

Examples that work:

- "Explain the variances in this month's P&L against budget"
- "Why did our costs go up this quarter compared to last year"
- "Write the MIS commentary for this cost centre report"
- "I have a review meeting tomorrow, prep the variance notes from this file"

If your file is unusual, one sentence of context saves a round trip: which column is budget, which is actual, and what period it covers.

---

## How it protects accuracy

- Every calculation runs as code, never as arithmetic written into a sentence
- Subtotal and group rows are detected and excluded so nothing is counted twice
- Favourable and adverse are decided from the nature of the line, not the arithmetic sign, so a cost saving never gets reported as a shortfall
- Percentages on a zero base are reported as not meaningful rather than as a false number
- Line variances are proved to sum to the total variance before anything is shown to you
- Every figure in the commentary traces back to a row in your file

If a check fails, it tells you it failed. It does not quietly present the number anyway.

---

## Limits worth knowing

- It reads the file you give it. It has no access to your ledger, so it cannot open a line to see the underlying entries.
- It never invents a business reason. If the data does not explain a movement, you get a question rather than a story.
- It does not judge whether performance is acceptable, decide accounting treatment, or advise on provisioning or tax.
- Decomposition into volume, price and mix only happens if quantity or rate data is in the file.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Totals do not match your own | Subtotal rows included or excluded differently | The skill states which rows it dropped. Correct it and rerun. |
| A cost saving shown as adverse | Line nature could not be identified | Tell it which lines are revenue and which are cost. |
| Commentary is generic | The file has only totals | Re-export with sub-account, cost centre or quantity detail. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |
| Numbers read wrong by a factor | Digit grouping or Dr/Cr columns misread | Say which column is debit and which is credit, then rerun. |

---

Part of the [Finance skills](../README.md) in the [Claude Skills Library](../../README.md).
