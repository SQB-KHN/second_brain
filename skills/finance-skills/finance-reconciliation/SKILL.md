---
name: finance-reconciliation
description: Match two files that should agree and produce a classified, aged exception list plus a statement that ties. Use for bank rec, GSTR-2B matching, vendor statements or any reconciliation.
---

# Reconciliation Exceptions

Reconciliation is the highest-volume manual task in finance and the one most often done by eye at eleven at night. The job is not to match the easy lines. It is to produce a short, correct list of what does not match and why.

## When to use this

Trigger on: reconcile, reconciliation, match these, tally these, bank rec, GST 2B matching, ITC reconciliation, vendor statement, intercompany, settlement matching, "find the difference between these two files".

## Before you start

Required: two files that are supposed to agree.

Ask, briefly, only what you cannot infer:
1. What each file is, and which is the reference. The bank statement, the GST portal file and the vendor's statement are external and are usually the reference. The ledger is usually the one being corrected.
2. Period covered by each file. Mismatched periods are the most common cause of a fake break.
3. Opening and closing balances per each side, if the files do not carry them.
4. Rounding tolerance. Default to one rupee unless told otherwise.

## Workflow

### 1. Profile both files first

Look at each file before transforming it. Check and report:

- Where the real header row sits
- Whether amounts use one signed column or split debit and credit columns
- Whether negatives use brackets
- Date formats on each side, which frequently differ. `03-04-2026` is 3 April in one file and 4 March in the other. Resolve this explicitly rather than letting a parser guess. If both readings are possible, ask.
- Whether either file includes opening balance, closing balance, subtotal or carried-forward rows. Exclude them from matching and use them as tie-outs.
- Row counts and total value per side, stated before matching begins

### 2. Compute in code, never in prose

Every normalisation, every match pass, every total and the reconciliation statement itself runs as Python. Matching done by eye is what this skill exists to replace, and arithmetic done in a sentence cannot be tied out.

### 3. Normalise before matching

Do this in code. Weak normalisation causes false breaks, and false breaks destroy trust in the output faster than anything else.

- **Amounts:** strip separators and currency symbols, convert brackets to negatives, unify Dr/Cr into a signed column, round to two decimals
- **Dates:** convert to a single ISO format after resolving the format question above
- **Reference numbers:** this matters more than anything else. Build a normalised key by upper-casing, stripping spaces, slashes, hyphens and leading zeros. `INV/2026-27/0042`, `inv 2026-27 42` and `INV20262742` should collide on the same key. Keep the original alongside so the output shows what the user recognises.
- **Party names:** upper-case, strip punctuation, and strip corporate suffixes such as PVT, LTD, LIMITED, PRIVATE, LLP, INC, and CO before comparing
- **GSTIN**, where present, is the strongest party key available. Use it ahead of name.

### 4. Match in passes, strongest first

Run these in order. Once a row is matched, remove it from the pool so later, looser passes cannot re-match it.

1. **Exact:** normalised reference plus amount
2. **Reference plus amount within tolerance:** catches rounding and small TDS or bank charge differences
3. **Amount plus date within a window:** default seven days, for entries with no usable reference
4. **Amount plus party name:** where date is unreliable
5. **One to many:** one payment settling several invoices. Look for a debit on one side matching a sum of credits on the other, within a reasonable window and party.
6. **Many to one:** several part payments against one invoice
7. **Reversals:** equal and opposite pairs on the same side, which cancel and should not appear as two separate breaks

Record which pass matched each row. The user needs to know that a match came from a fuzzy pass, not an exact one, before they act on it.

### 5. Classify every remaining break

An unmatched row is not an exception until it is classified. Put each into one of these:

- **Timing.** Present in one file, will appear in the other next period. Cheques issued but not presented, deposits in transit, invoices received after the cut-off. These need no correction, only disclosure.
- **Amount mismatch.** Same transaction, different value. Show both values and the difference. Common causes worth checking and naming: TDS deducted by the customer, bank charges, foreign exchange difference, rounding, partial payment.
- **Missing in ledger.** Present on the external side, absent from the books. This usually means an entry has to be passed.
- **Missing in external file.** Booked but not reflected. Often a duplicate booking or an entry against the wrong bank or vendor.
- **Duplicate.** Same reference, party and amount appearing twice on one side.
- **Suspected error.** Digit transposition is worth testing for specifically: if a difference is exactly divisible by nine, flag it as a possible transposed digit. This one test catches a surprising share of real errors.

### 6. Build the reconciliation statement

The exception list is not enough on its own. Produce the statement that proves the two sides tie:

```
Balance per external file          X
Add:   items in books not in file  X
Less:  items in file not in books  X
Add/Less: amount differences       X
Balance per books                  X
```

If this does not tie to the actual book balance, say so and show the unexplained residual as its own line. Never force it to zero. An unexplained residual that is reported honestly is useful. A hidden one is dangerous.

### 7. Age the breaks

Group by age: current period, one to three months, three to six months, over six months. Old breaks are the ones that matter. A six-month-old unmatched entry is usually a real error and often needs a write-off decision.

## GST specific handling

When reconciling GSTR-2B against the purchase register:

- Match on supplier GSTIN plus normalised invoice number plus invoice value. Invoice number formatting differs constantly between the portal file and the ERP, so normalisation carries the whole exercise.
- Compare taxable value and each tax head separately. CGST, SGST, IGST and cess can differ even when the invoice total agrees, and that difference is the finding.
- Classify separately: in 2B but not in books, in books but not in 2B, value differs, tax head differs, GSTIN differs.
- Flag invoices in books but absent from 2B as credit at risk, with the amount totalled. That total is the number the user actually needs.
- Report what you find. Do not advise on whether credit may be claimed, in which period, or under which rule. Eligibility depends on current law and the user's specific facts, and that is their tax advisor's call.

## Output format

**1. Summary.** Rows and value per side, matched count and value, break count and value, and the residual after the reconciliation statement.

**2. Reconciliation statement.** As above, in full.

**3. Exception list.** One row per break:

| Date | Reference | Party | Amount side A | Amount side B | Difference | Category | Age | Suggested action |

Sorted by value, descending.

**4. Matched pairs matched by a fuzzy pass.** Listed separately so they can be spot-checked before anyone relies on them.

**5. Data quality notes.** Rows dropped, dates that were ambiguous, references that were unusable.

Offer an Excel version with one sheet per category. Build it only if asked.

## Checks to run before delivering

- Matched plus unmatched equals total rows, on each side independently
- No row appears in more than one match
- Total value of matches agrees on both sides
- The reconciliation statement ties, or the residual is disclosed as its own line
- Fuzzy matches are labelled as fuzzy, never presented as certain

## What this skill does not do

- It does not post entries, adjust books or change either file
- It does not decide GST credit eligibility, tax treatment or write-offs
- It does not confirm a fuzzy match is correct. It surfaces it for a human to approve
- It cannot see anything outside the two files given
