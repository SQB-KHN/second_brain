---
name: ops-bill-audit
description: Audit vendor and transporter invoices against the PO, the GRN and the rate card, and return a valued exception list. Use for bill passing, three-way match or freight overcharges.
---

# Purchase and Freight Bill Audit

Bill passing is a signature at the end of a queue. The rate was agreed months ago by somebody else, the goods were received by somebody else, and the person approving has thirty invoices and an afternoon. Overcharges survive because nobody has time to check the only thing that matters: whether the amount billed is the amount owed.

## When to use this

Trigger on: bill passing, invoice verification, three-way match, PO vs GRN vs invoice, vendor overcharge, freight bill audit, transporter invoice check, rate card verification, detention and demurrage, duplicate payment, "are we being overbilled".

## Before you start

Required: the invoices, plus whatever states the entitlement. For purchases that is the purchase order and the goods receipt note. For freight it is the rate card or the contract.

Ask, briefly:
1. Which document is the entitlement and which is the charge. The PO and the rate card are the agreement; the invoice is the claim. Auditing in the wrong direction produces findings against yourself.
2. Tolerance. Most companies allow a small variance before flagging. Default to 1 percent or 100 rupees, whichever is lower, and say so.
3. Whether freight, packing, insurance and loading sit inside the PO rate or are billed separately. This one question resolves a large share of apparent overcharges.
4. Period, and whether partial deliveries against one PO are expected.

If they have invoices but no PO or rate card, say plainly that without the entitlement side this becomes a duplicate and arithmetic check rather than an audit. Then run that, and say what it can and cannot find.

## Workflow

### 1. Profile every file, and check the level first

- **Which level each row sits at.** PO header against PO line, invoice header against invoice line. Comparing a header total to a line rate is the most common false finding in this work.
- **Whether quantities share a unit of measure across all three documents.** A PO in boxes against an invoice in pieces shows a twelvefold overcharge that does not exist. Resolve this before comparing anything.
- **Tax separated from taxable value.** Compare taxable value first, then each tax head. A total-only comparison hides which side is actually wrong.
- **Reference formats**, which differ between systems. Normalise by upper-casing and stripping spaces, slashes, hyphens and leading zeros, keeping the original for display so the output shows what the user recognises.
- **What basis the rate card uses:** per kilogram, per unit, per trip, per pallet, or slab-based. Slab rates are where most freight overcharging hides.
- Header rows, brackets for negatives, Indian digit grouping.

### 2. Run the three-way match, testing each failure separately

Match invoice to PO to GRN on normalised reference plus line item. Then test each of these on its own, because each has a different owner and a different remedy:

- **Price variance.** Rate billed against rate on the PO. Report the per-unit difference and extend it to the quantity billed.
- **Quantity variance.** Quantity billed against quantity **received on the GRN**, not quantity ordered. Billing for what was ordered rather than what arrived is the most common overcharge in the set.
- **Cumulative over-billing.** Sum every invoice against one PO line and compare the total against the PO quantity. Each invoice can pass individually while the total exceeds the order, and line-by-line checking cannot catch it.
- **Unordered items.** Billed but not on the PO at all.
- **Received not billed.** The reverse. This is an unrecorded liability, not an overcharge. Report it separately and label it as such.
- **Missing GRN.** Invoiced with no receipt recorded. That is not a variance, it is an unverifiable invoice, and it should not be passed.

### 3. Detect duplicates on more than the invoice number

Same vendor plus same invoice number is the easy case and the rare one. Also test:

- Same vendor, same amount, same date, different invoice number
- The same invoice number with a suffix such as A, R, REV, or a trailing slash
- The same amount against a PO line already settled on an earlier invoice

Report each with both rows shown side by side, and label it a **candidate**. A recovered duplicate payment is real money. A false accusation to a vendor costs a relationship, so the human makes the call.

### 4. Audit freight against the rate card, test by test

Freight is where the leakage is largest and the examination thinnest.

- **Chargeable weight.** Transporters bill the higher of actual and volumetric weight. Recompute volumetric from the dimensions using the divisor **in the contract**, and check which was applied. A wrong divisor quietly inflates every bill on the lane.
- **Slab boundaries.** A 480 kg shipment billed at the 500 kg slab may be correct under the contract or may not. Check the contract's own rule rather than assuming.
- **Lane rate.** Origin and destination against the rate card, including whether the destination is inside the covered area. Out-of-delivery-area charges applied to a covered location are common and easy to miss.
- **Minimum charge.** Applied correctly, and not applied on top of a rate that already includes it.
- **Fuel surcharge.** Against the contracted formula and the correct period, not a rate carried over from last quarter.
- **Detention and demurrage.** Free time counted from the contracted event, arrival or unloading start, and working hours only where the contract says so. Check whether the delay happened at the user's own site, because that changes who owes what.
- **Accessorials.** Loading, unloading, waiting, multi-point delivery, appointment charges. Each must be in the contract or supported by evidence.

Quote the contract clause or rate card line behind every finding. A freight claim without the clause attached does not survive the vendor call.

### 5. Recompute every arithmetic line

Do not assume the invoice adds up. **Do all of this in code, never in prose.** Test quantity times rate against line value, line values against the subtotal, tax against taxable value at the stated rate, and subtotal plus tax against the invoice total. An arithmetic error worked out inside a sentence is how a recoverable claim turns into a wrong accusation in front of a vendor.

Rounding differences inside tolerance get netted and reported once as a single total, not listed line by line. Burying three real findings inside two hundred one-rupee differences is how an audit gets ignored.

### 6. Classify, value and rank

Every exception carries what was billed, what was owed, the difference, the category, the evidence it rests on, and who resolves it. Sort by rupee value.

Then split the total in two, and keep it split:

- **Recoverable.** Supported by a rate card line, a PO line or a GRN quantity. This is debit note material.
- **Unverifiable.** Missing a GRN, missing a rate, or resting on an ambiguous clause. This is a question for stores, procurement or the contract owner.

Mixing them makes the headline number look better than it is, and it falls apart in the first vendor meeting.

## Tax and classification

Report what the invoice shows against what the PO and rate card say, and flag differences in taxable value, rate applied, tax head and place of supply.

Do not decide eligibility, the correct rate, the correct head, or whether input credit can be claimed. Those depend on current law, the item's classification and both parties' registrations, and they belong to the user's tax advisor. Matching input credit against the portal is a reconciliation exercise, not a bill audit. Never assign or confirm an HS code or a customs classification.

## Output format

**1. Recoverable total.** One line, at the top. The value supported by evidence, and separately the value that cannot be verified.

**2. Summary.** Invoices tested, lines tested, exceptions found, pass rate.

**3. Exception list.**

| Invoice | Date | Vendor | PO | Category | Billed | Owed | Difference | Evidence | Action |

**4. Duplicate candidates.** Both rows shown, labelled as candidates.

**5. Freight findings.** Per test, each with the contract clause or rate card line it rests on.

**6. Received not billed.** The liability side, stated separately with its value.

**7. Unverifiable invoices.** What is missing, and who can supply it.

**8. Arithmetic differences.** Netted total for anything within tolerance, individual lines above it.

**9. Data quality notes.** Unit of measure conflicts, unmatched references, files supplied at mismatched levels.

Offer the Excel workbook with one sheet per category. Build it only if asked.

## Checks to run before delivering

- Every invoice line is either matched or listed as an exception, with none unaccounted for
- No line appears in two exception categories
- Quantity comparisons use the same unit of measure across all three documents, and any conversion applied is stated
- Cumulative billing per PO line has been tested, not only invoice by invoice
- Every recoverable amount traces to a specific rate card line, PO line or GRN quantity
- Duplicates are labelled as candidates, never as confirmed
- The recoverable total excludes everything unverifiable, and the two figures are reported separately

## What this skill does not do

- It does not raise a debit note, withhold a payment or contact a vendor. It produces the evidence for someone else to act on.
- It does not confirm a duplicate. It surfaces candidates with both rows for a human to compare.
- It does not decide tax rates, tax heads, input credit eligibility, or any customs or HS classification.
- It does not interpret a contract where the wording is genuinely ambiguous. It quotes the clause and names the question.
- It cannot audit against an entitlement it was not given. No rate card means no rate audit, and it will say so rather than inventing a comparison.
