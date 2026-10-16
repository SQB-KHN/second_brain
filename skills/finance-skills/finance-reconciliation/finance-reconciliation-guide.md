# Reconciliation Exceptions

Matches two files that should agree and returns a classified, aged exception list plus a reconciliation statement that ties.

---

## Who this is for

Anyone who reconciles as part of the job: accounts payable and receivable teams, accountants in practice, GST and compliance staff, controllers, and finance leads in small companies doing every rec themselves.

## The problem it solves

Reconciliation is the largest block of manual hours in a finance calendar. Most of it is mechanical matching that a person does by eye, and the genuinely useful output, a short list of what does not match and why, arrives late and tired.

This skill does the matching in passes, classifies every remaining break, ages it, and produces the statement that proves the two sides tie. Typical saving is two to six hours per reconciliation, more on GST matching.

---

## What it reconciles

| Pair | Reference side | Being corrected |
|---|---|---|
| Bank statement vs bank ledger | Statement | Ledger |
| GSTR-2B vs purchase register | Portal file | Register |
| Vendor statement vs AP ledger | Vendor statement | Ledger |
| Customer statement vs AR ledger | Customer statement | Ledger |
| Payment gateway settlement vs sales register | Settlement report | Sales register |
| Intercompany balances | Either | Both |
| Stock register vs physical count | Count sheet | Register |

Any two files that are supposed to agree will work.

## What you give it

Two files, Excel or CSV.

**Minimum per file:** a date, an amount, and something identifying the transaction, which can be a reference number, a party name, or a narration.

**Strengthens matching considerably:**

| Extra column | Why it matters |
|---|---|
| Invoice or voucher reference | Enables exact matching, the strongest pass available |
| GSTIN | The most reliable party identifier there is, far better than name |
| Opening and closing balances | Lets it build a reconciliation statement that provably ties |
| Separate tax columns (CGST, SGST, IGST) | Finds tax head differences that a total-only comparison hides |
| Due date or bill date alongside entry date | Improves timing classification |

**Handled automatically:** Dr/Cr split columns, brackets for negatives, Indian digit grouping, different date formats on each side, reference numbers formatted differently between systems such as `INV/2026-27/0042` against `INV20262742`, corporate suffixes in party names, and opening or closing balance rows that should not be matched.

## What you get back

1. Summary of rows and value per side, matched and unmatched
2. A reconciliation statement, with any unexplained residual shown honestly rather than forced to zero
3. The exception list, one row per break, classified and aged, sorted by value
4. Fuzzy matches listed separately so you can spot-check before relying on them
5. Data quality notes covering dropped rows and ambiguous dates

An Excel workbook with one sheet per category is offered at the end.

---

## How the matching works

Seven passes, strongest first, each removing matched rows from the pool so a looser pass cannot re-match them:

1. Exact reference plus amount
2. Reference plus amount within tolerance, default one rupee
3. Amount plus date within a window, default seven days
4. Amount plus party name
5. One payment against several invoices
6. Several part payments against one invoice
7. Reversals, which cancel rather than appearing as two breaks

Every break is then classified as timing, amount mismatch, missing in ledger, missing in the external file, duplicate, or suspected error. Differences exactly divisible by nine are flagged as possible transposed digits, which catches a real share of keying errors.

## GST reconciliation

For GSTR-2B against the purchase register, it matches on supplier GSTIN plus normalised invoice number plus value, compares each tax head separately rather than only the invoice total, and totals the invoices sitting in your books but absent from 2B as credit at risk.

It reports findings only. It does not advise on whether credit can be claimed or in which period. That depends on current law and your facts, and belongs with your tax advisor.

## What good output looks like

A strong result is a short exception list, not a long one. Most rows clear on the first two passes, the statement ties or names its residual as its own line, and every remaining break carries a category and an age: "Missing in ledger, 3.4 lakh, 94 days, vendor invoice never booked." Fuzzy matches sit in their own section, waiting for your eye.

If you get hundreds of breaks, the two files usually do not cover the same period, or your invoice references are formatted so differently that normalisation could not bridge them. Both show up in the data quality notes.

---

## Installing it

1. On claude.ai, turn on code execution in Settings, under Capabilities.
2. Download this folder, or make a folder named `finance-reconciliation` and put `SKILL.md` inside it. The guide does not need to go in.
3. Compress the folder to a `.zip`.
4. Go to Customize, then Skills, then add a skill and upload the zip.

## Using it

Upload both files and say what they are.

Examples that work:

- "Reconcile this bank statement against the ledger for March"
- "Match my GSTR-2B with the purchase register and tell me what credit is at risk"
- "This vendor says we owe 4.2 lakh, our books say 3.8, find the difference"
- "Compare these two files and give me the exception list"

Naming which file is which saves a round trip.

---

## How it protects accuracy

- Matched plus unmatched is proved to equal total rows, on each side independently
- No row can appear in more than one match, because each pass removes what it matched from the pool
- Every normalisation, match pass and total runs in code, never worked out in prose
- The reconciliation statement either ties or the residual is disclosed as its own line. It is never forced to zero
- Fuzzy matches are labelled as fuzzy and listed separately, so nothing uncertain is presented as settled
- Rows dropped and dates that were ambiguous are reported with their counts rather than handled silently

## Limits worth knowing

- It never posts entries or edits either file. Every action stays with you.
- A fuzzy match is a suggestion, not a conclusion. It is labelled as fuzzy so you can check it.
- It cannot see anything outside the two files. If a break needs the underlying voucher, it says so.
- It does not decide GST eligibility, tax treatment, or whether an old break should be written off.
- Very large files may need to be split by month.

## If something looks wrong

| What you see | Usual cause | Fix |
|---|---|---|
| Far too many breaks | Periods do not align, or reference formats differ badly | Check both files cover the same dates. It reports its normalisation, so you can see what happened. |
| Statement does not tie | Opening or closing balances missing | Supply both balances and rerun. |
| Dates read wrong | Ambiguous format such as 03-04-2026 | It asks when both readings are possible. Answer, or state the format upfront. |
| Real matches shown as breaks | Reference normalisation too strict for your numbering | Tell it your invoice numbering pattern. |
| Nothing happens on upload | Code execution is off | Turn it on in Settings, under Capabilities. |

---

Part of the [Finance skills](../README.md) in the [Claude Skills Library](../../README.md).
