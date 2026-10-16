---
name: health-revenue-analysis
description: Turn a billing export into payer mix, realisation against tariff, deductions, receivables ageing and unbilled leakage. Use for hospital or clinic revenue and collections review.
---

# Revenue, Payer Mix and Collections

A hospital or clinic knows what it billed and what it banked. The gap between those two numbers is where the business actually lives, and it is spread thin across payer deductions, concessions nobody approved, services that were delivered and never charged, and claims still sitting with a payer. Nobody reports the gap, because no single system holds all four pieces.

## When to use this

Trigger on: revenue analysis, payer mix, collections, realisation, TPA deductions, receivables ageing, revenue leakage, department-wise revenue, doctor-wise revenue, discount analysis, billing analysis, "why is collection down", "where are we losing money".

## Before you start

Required: a billing export with bill or encounter number, date, department or service, payer, gross amount, and amount collected or outstanding.

Ask, briefly:
1. **Whether this is billing or collections data.** What was raised and what was received are different files, and most revenue questions need both.
2. Payer categories in use: cash, insurance through a TPA, insurer direct, government scheme, corporate or PSU panel, staff. Each carries a different realisation and a different cycle.
3. **The tariff or rate list**, if they have one. This turns revenue reporting into realisation against tariff, which is the single biggest upgrade available to the output.
4. Whether billing is package-based, itemised, or both. The two cannot be compared line for line.
5. Their own definition of a completed encounter, since bills raised on discharge and bills raised on service date give different monthly totals.

## Check for patient identifiers first

Name the identifying fields: patient name, hospital or UHID number tied to an individual, phone, address, scheme or policy number.

Say once that **this analysis needs none of them.** It needs the bill or encounter number, department, payer, dates and amounts. Offer to run on a file with identifiers removed, then continue with whatever they choose. State it once and do not repeat it.

## Workflow

### 1. Profile the billing export

Healthcare billing exports carry traps of their own, and each one produces a confidently wrong revenue figure:

- **One row per bill against one row per bill line.** A file that repeats the bill total on every line inflates revenue by the number of lines. Detect which level you have and say so.
- **Cancelled, revised and re-raised bills** sitting alongside the originals. Counting cancelled bills is the commonest overstatement there is.
- **Credit notes and refunds** held as separate positive rows rather than negatives.
- **Advances and deposits** in the same file as bill collections. An advance is not revenue.
- **Package bills** where the package total sits on a header row and the component services also carry values. Counting both double counts.
- **Interim bills** in long-stay cases, superseded by the final bill.
- **Discount, concession and write-off columns** which may sit inside or outside the gross figure. Establish which before anything else.
- Header row position, brackets for negatives, Indian digit grouping.

State bill count, gross value, and the value excluded, before showing any analysis.

### 2. Compute in code, never in prose

Every rate, share, ageing bucket and reconciliation runs as Python. Nothing arithmetic is worked out inside a sentence.

### 3. Settle which revenue you are reporting, and say so

Four different numbers all get called revenue, and conversations go wrong because two people are holding different ones:

- **Gross billed.** Value of bills raised, before any deduction.
- **Net billed.** After approved discounts, concessions and package adjustments.
- **Realised.** Cash actually received against those bills.
- **Recognised.** What accounting will book, which may differ from all three.

Report the walk from gross to realised as a waterfall, with every deduction step and its value. That waterfall is the analysis. Mark each step controllable or not, because that is what makes it actionable rather than descriptive.

### 4. Analyse by payer, not only by department

Payer mix is the structure that governs healthcare revenue, and department-only reporting hides it completely. Per payer category:

- Share of gross billed, and share of realised. **These differ, and the difference is the finding.**
- Realisation rate
- Average deduction rate, and the top deduction reasons where the file carries them
- Days to payment, mean and worst case
- Outstanding, aged

A department can look like the best performer on billed value and the worst on realised value, because its case mix skews to a slow, high-deduction payer. That sentence is usually the most useful output of the whole exercise, and no department-wise report can produce it.

### 5. Measure realisation against tariff where a rate list exists

- Billed against tariff per service, which surfaces under-billing and unapproved rate use
- Realised against tariff, which is the true yield
- Concessions and discounts by approver and by department, with anything unattributed totalled separately. Unapproved concession is a standard leak and nobody looks until somebody does.

### 6. Hunt the unbilled

This is the finding administrators actually pay for, and no dashboard shows it. Look for encounters missing a service that almost always accompanies another:

- Consumables and implants against procedures that require them
- Oxygen, monitoring or intensive care charges against a stay that recorded them
- Investigation charges against a stay with recorded results
- Consultation charges against days of admission
- Procedures in the notes but absent from the bill

Report these as **candidates, with the pattern that flagged each one**, never as confirmed loss. Give the count and the value at tariff, and say plainly that each needs checking against the case file. An unbilled candidate is a question for the billing team, not a number for the board.

### 7. Age the receivables by payer and by status

Buckets: 0 to 30, 31 to 60, 61 to 90, 91 to 180, over 180 days. Age from bill date **and** from submission date where both exist, because a claim sitting unsubmitted for forty days is a completely different problem from one the payer is sitting on.

Split outstanding into not yet submitted, submitted and pending, queried and awaiting response, part-settled with a balance disputed, and rejected. Those five have five different owners, and a single ageing table hides all of them.

### 8. State the concentration in one sentence

"Two payers hold 71 percent of the over-90-day outstanding, and in both cases the query is for the same missing document." That sentence is worth more than the table under it.

## Output format

**1. Headline.** Gross billed, realised, realisation rate, and the largest single leak. Which revenue definition is being reported.

**2. Gross to realised waterfall.** Every step with its value, marked controllable or not.

**3. Payer mix.** Share of billed against share of realised, realisation rate, deduction rate, days to pay, outstanding.

**4. Department and consultant view.** Ranked on billed and on realised, since the two orders differ.

**5. Realisation against tariff.** Only where a rate list was supplied.

**6. Concessions and discounts.** By approver and department, with unattributed shown separately.

**7. Unbilled candidates.** Pattern, count, value at tariff, labelled as requiring verification.

**8. Receivables ageing.** By payer, by status, from bill date and from submission date.

**9. Concentration.** Where the money is stuck and what it points at.

**10. Data quality and exclusions.** Cancelled bills, advances, interim bills, credit notes, each with its value.

Offer the Excel version with one sheet per view. Build it only if asked.

## Checks to run before delivering

- Gross minus every deduction step equals realised plus outstanding, exactly
- Bill count and gross value match the file's own totals where it states them
- No bill counted twice through a package header plus its components
- Cancelled, interim and superseded bills are excluded with their value stated
- Advances and deposits are excluded from revenue and reported separately
- Payer shares sum to 100 percent, on billed and on realised independently
- Ageing buckets sum to total outstanding
- Unbilled items are labelled candidates with their flagging pattern, never as confirmed loss
- The revenue definition being reported is stated in the headline

## What this skill does not do

- It does not assign or verify a clinical code, and it does not decide what a service should have been billed as.
- It does not decide whether a payer deduction was contractually valid. It quantifies deductions and groups them by reason so somebody can take it up.
- It does not confirm an unbilled item. It flags the pattern for verification against the case file.
- It does not advise on GST, TDS or accounting treatment for healthcare services.
- It does not need patient identities, and it will say so. It runs on a de-identified export.
- It reads the export. It cannot see the case file, the claim portal or the bank.
